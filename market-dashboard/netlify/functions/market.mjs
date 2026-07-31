/**
 * /api/market — one compact endpoint that serves the whole dashboard.
 *
 * Why this shape:
 *   The previous design had the browser fire nine parallel requests per page
 *   load, one per ticker, and again for every time window. Yahoo rate-limits per
 *   source IP and answered 429 from Netlify almost immediately. Here the
 *   function fetches each ticker ONCE (5y of daily closes), computes every
 *   number the UI needs, and returns ~3 KB. With s-maxage on the response the
 *   CDN collapses all visitor traffic into roughly six upstream fetches an hour,
 *   which sits far under any sane rate limit.
 *
 * Resilience, in order:
 *   1. sequential fetches with jitter, not a nine-way burst
 *   2. a Yahoo session cookie + crumb, the way yfinance does it
 *   3. one retry with backoff on 429/5xx, alternating query1/query2
 *   4. a module-level snapshot of the last good payload — Netlify keeps
 *      instances warm, so a throttled upstream still serves real numbers,
 *      flagged with stale:true and the age in seconds
 */

const HOSTS = ['https://query1.finance.yahoo.com', 'https://query2.finance.yahoo.com'];

const SYMBOLS = [
  'POONAWALLA.NS', 'BAJFINANCE.NS', 'SHRIRAMFIN.NS', 'LTF.NS', 'CHOLAFIN.NS',
  'ABCAPITAL.NS', 'PIRAMALFIN.NS', 'MUTHOOTFIN.NS', 'M&MFIN.NS',
];

const WINDOWS = { '1W': 7, '1M': 30, '3M': 91, '6M': 182, '1Y': 365, '3Y': 1095, '5Y': 1825 };

const UA =
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 ' +
  '(KHTML, like Gecko) Chrome/124.0 Safari/537.36';

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/** Last successful payload, kept across invocations on a warm instance. */
let snapshot = null;

/* ── Yahoo session ─────────────────────────────────────────────────────── */
async function getSession() {
  const session = { cookie: '', crumb: '' };
  try {
    const res = await fetch('https://fc.yahoo.com', {
      headers: { 'User-Agent': UA },
      redirect: 'manual',
      signal: AbortSignal.timeout(5000),
    });
    const raw = res.headers.get('set-cookie');
    if (raw) session.cookie = raw.split(',').map((c) => c.split(';')[0].trim()).join('; ');
  } catch { /* cookie is best-effort */ }

  if (session.cookie) {
    try {
      const res = await fetch('https://query2.finance.yahoo.com/v1/test/getcrumb', {
        headers: { 'User-Agent': UA, Cookie: session.cookie },
        signal: AbortSignal.timeout(5000),
      });
      if (res.ok) {
        const c = (await res.text()).trim();
        if (c && c.length < 32 && !c.includes('<')) session.crumb = c;
      }
    } catch { /* crumb is best-effort */ }
  }
  return session;
}

async function fetchChart(symbol, session, attempt = 0) {
  const host = HOSTS[attempt % HOSTS.length];
  const qs = new URLSearchParams({ range: '5y', interval: '1d', includePrePost: 'false' });
  if (session.crumb) qs.set('crumb', session.crumb);

  const headers = { 'User-Agent': UA, Accept: 'application/json' };
  if (session.cookie) headers.Cookie = session.cookie;

  try {
    const res = await fetch(`${host}/v8/finance/chart/${encodeURIComponent(symbol)}?${qs}`, {
      headers,
      signal: AbortSignal.timeout(8000),
    });

    if ((res.status === 429 || res.status >= 500) && attempt < 2) {
      await sleep(600 * (attempt + 1));
      return fetchChart(symbol, session, attempt + 1);
    }
    if (!res.ok) return { error: `HTTP ${res.status}` };

    const result = (await res.json())?.chart?.result?.[0];
    if (!result) return { error: 'empty result' };
    return parse(result, symbol);
  } catch (err) {
    if (attempt < 2) {
      await sleep(600 * (attempt + 1));
      return fetchChart(symbol, session, attempt + 1);
    }
    return { error: err?.name === 'TimeoutError' ? 'timeout' : String(err?.message || err) };
  }
}

/* ── shape one ticker into the numbers the UI renders ──────────────────── */
function parse(result, symbol) {
  const meta = result.meta ?? {};
  const stamps = result.timestamp ?? [];
  const quote = result.indicators?.quote?.[0] ?? {};
  const rawC = quote.close ?? [];
  const rawV = quote.volume ?? [];

  const t = [];
  const c = [];
  const v = [];
  for (let i = 0; i < stamps.length; i += 1) {
    if (rawC[i] == null) continue;
    t.push(stamps[i] * 1000);
    c.push(rawC[i]);
    v.push(rawV[i] ?? 0);
  }
  if (c.length < 2) return { error: 'insufficient history' };

  return shape({
    price: meta.regularMarketPrice ?? c[c.length - 1],
    // Previous *session* close. Deliberately not meta.chartPreviousClose, which
    // means "close before the requested range began" — five years ago here.
    prevClose: c[c.length - 2],
    volume: meta.regularMarketVolume ?? v[v.length - 1] ?? 0,
    t,
    c,
    extra: {
      fiftyTwoHigh: meta.fiftyTwoWeekHigh ?? null,
      fiftyTwoLow: meta.fiftyTwoWeekLow ?? null,
    },
  });
}

/* ── provider 2: Twelve Data ───────────────────────────────────────────────
 * Yahoo blocks cloud/datacenter IP ranges, which is exactly where this function
 * runs — it answers 429 from Netlify indefinitely. Twelve Data is built to be
 * called from servers and carries all nine NSE tickers under the same codes
 * (minus the .NS suffix). Set TWELVEDATA_API_KEY in the Netlify UI to use it.
 *
 * Budget: one time_series call per ticker = 9 credits per upstream refresh.
 * With s-maxage=600 the CDN triggers at most ~6 refreshes an hour, so a full
 * trading day costs roughly 500 of the free tier's 800 daily credits.
 */
async function fetchTwelve(symbol, key) {
  const td = symbol.replace('.NS', '');
  const qs = new URLSearchParams({
    symbol: td, exchange: 'NSE', interval: '1day',
    outputsize: '1300', order: 'ASC', apikey: key,
  });
  try {
    const res = await fetch(`https://api.twelvedata.com/time_series?${qs}`, {
      signal: AbortSignal.timeout(9000),
    });
    if (!res.ok) return { error: `HTTP ${res.status}` };
    const j = await res.json();
    if (j.status === 'error') return { error: String(j.message || 'api error').slice(0, 90) };

    const values = j.values || [];
    if (values.length < 2) return { error: 'insufficient history' };

    const t = [];
    const c = [];
    const v = [];
    for (const row of values) {
      const close = parseFloat(row.close);
      if (!isFinite(close)) continue;
      t.push(Date.parse(row.datetime + 'T00:00:00Z'));
      c.push(close);
      v.push(parseFloat(row.volume) || 0);
    }
    if (c.length < 2) return { error: 'insufficient history' };

    return shape({
      price: c[c.length - 1],
      prevClose: c[c.length - 2],
      volume: v[v.length - 1],
      t, c,
    });
  } catch (err) {
    return { error: err?.name === 'TimeoutError' ? 'timeout' : String(err?.message || err) };
  }
}

/** Common shaping for both providers. */
function shape({ price, prevClose, volume, t, c, extra }) {
  const now = t[t.length - 1];
  const windows = {};
  for (const [label, days] of Object.entries(WINDOWS)) {
    const target = now - days * 86400000;
    if (t[0] > target + 86400000 * 7) continue;

    let lo = 0;
    let hi = t.length - 1;
    while (lo < hi) {
      const mid = (lo + hi) >> 1;
      if (t[mid] < target) lo = mid + 1; else hi = mid;
    }
    const i = lo > 0 && Math.abs(t[lo - 1] - target) < Math.abs(t[lo] - target) ? lo - 1 : lo;
    const base = c[i];
    if (!base) continue;
    windows[label] = {
      from: Number(base.toFixed(2)),
      at: t[i],
      pct: Number((((price - base) / base) * 100).toFixed(2)),
    };
  }
  return {
    price: Number(price.toFixed(2)),
    prevClose: Number(prevClose.toFixed(2)),
    changeAbs: Number((price - prevClose).toFixed(2)),
    changePct: Number((((price - prevClose) / prevClose) * 100).toFixed(2)),
    volume: volume || 0,
    windows,
    ...(extra || {}),
  };
}

/* ── handler ───────────────────────────────────────────────────────────── */
export default async () => {
  const key = process.env.TWELVEDATA_API_KEY;
  const provider = key ? 'twelvedata' : 'yahoo';
  const session = key ? null : await getSession();
  const companies = {};
  let good = 0;

  for (let i = 0; i < SYMBOLS.length; i += 1) {
    const sym = SYMBOLS[i];
    const res = key ? await fetchTwelve(sym, key) : await fetchChart(sym, session);
    companies[sym] = res;
    if (!res.error) good += 1;
    // Jitter between tickers — a nine-way burst is what tripped the limiter.
    if (i < SYMBOLS.length - 1) await sleep(180 + Math.floor(Math.random() * 160));
  }

  if (good > 0) {
    snapshot = { fetchedAt: Date.now(), companies, good, provider };
    return Response.json(
      { ok: true, stale: false, provider, fetchedAt: snapshot.fetchedAt, good, total: SYMBOLS.length, companies },
      {
        headers: {
          // The CDN, not the browser, is what keeps upstream traffic low.
          'Cache-Control': 'public, max-age=120, s-maxage=600, stale-while-revalidate=3600',
          'Access-Control-Allow-Origin': '*',
        },
      },
    );
  }

  // Upstream is throttling. Serve the last good numbers rather than an empty page.
  if (snapshot) {
    return Response.json(
      {
        ok: true,
        stale: true,
        fetchedAt: snapshot.fetchedAt,
        ageSec: Math.round((Date.now() - snapshot.fetchedAt) / 1000),
        good: snapshot.good,
        provider: snapshot.provider,
        total: SYMBOLS.length,
        companies: snapshot.companies,
      },
      { headers: { 'Cache-Control': 'public, max-age=60', 'Access-Control-Allow-Origin': '*' } },
    );
  }

  const reason = companies[SYMBOLS[0]]?.error || 'upstream unavailable';
  return Response.json(
    { ok: false, provider, error: reason, companies },
    { status: 200, headers: { 'Cache-Control': 'no-store', 'Access-Control-Allow-Origin': '*' } },
  );
};

export const config = { path: '/api/market' };
