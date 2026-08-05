/**
 * /api/quotes — live NSE quotes for the P/B dashboard.
 *
 * ── Why this fetches in rotating batches ──────────────────────────────────────
 * Twelve Data's free tier allows 800 API credits/day and **8 credits/minute**,
 * where one symbol costs one credit. We track nine companies, so asking for all
 * nine at once is 9 credits in one minute — over the per-minute cap, and Twelve
 * Data rejects the WHOLE batch rather than trimming it. Splitting into 5+4 within
 * the same invocation does not help: the cap is a rolling minute, not per request.
 *
 * So each invocation refreshes the STALEST `BATCH` symbols (default 5) in a single
 * batched call and merges them into a store that survives on the warm instance.
 * With the CDN cache below, every symbol refreshes inside ~10 minutes, which is far
 * finer than a P/B ratio actually moves. On a paid plan (Grow = 55 credits/min) set
 * TWELVEDATA_BATCH=9 and every invocation refreshes everything.
 *
 * Cost: ~390 credits on a full trading day, ~90 overnight — inside the free 800.
 *
 * ── Resilience, in order ──────────────────────────────────────────────────────
 *   1. warm-instance store, so a symbol not refreshed this pass still has a price
 *   2. a cold instance returns only what it just fetched; the browser fills the
 *      rest from the dated snapshot.json it already loaded
 *   3. total upstream failure returns ok:false and the browser runs on snapshot.json
 */

import book from '../../book-values.json';

const SYMBOLS = book.companies.map((c) => c.symbol);
const ENDPOINT = 'https://api.twelvedata.com/quote';

/** symbol -> { q, at } for every symbol fetched by THIS instance. */
const store = new Map();

/* ── NSE trading hours: 09:15–15:30 IST, Mon–Fri ──────────────────────────── */
function marketOpen(now = new Date()) {
  // IST is UTC+5:30 year-round — no DST to account for.
  const ist = new Date(now.getTime() + 5.5 * 3600 * 1000);
  const day = ist.getUTCDay();
  if (day === 0 || day === 6) return false;
  const mins = ist.getUTCHours() * 60 + ist.getUTCMinutes();
  return mins >= 555 && mins <= 930;
}

function num(v) {
  const n = parseFloat(v);
  return Number.isFinite(n) ? n : null;
}

/** Twelve Data's quote payload -> the flat shape the UI renders. */
function shape(raw) {
  const price = num(raw.close);
  const prev = num(raw.previous_close);
  if (price == null) return null;

  const fw = raw.fifty_two_week || {};
  return {
    price,
    prevClose: prev,
    changeAbs: num(raw.change),
    changePct: num(raw.percent_change),
    volume: num(raw.volume) || 0,
    open: num(raw.open),
    high: num(raw.high),
    low: num(raw.low),
    weekHigh52: num(fw.high),
    weekLow52: num(fw.low),
    isOpen: raw.is_market_open === true,
    at: raw.datetime || null,
  };
}

/**
 * One batched /quote call. Twelve Data keys a multi-symbol response by symbol and
 * returns a bare object for a single symbol — both shapes are handled.
 * Returns { got: Map, error } — a partial result is still a useful result.
 */
async function fetchBatch(symbols, key) {
  const qs = new URLSearchParams({
    symbol: symbols.join(','),
    exchange: 'NSE',
    apikey: key,
  });

  let res;
  try {
    res = await fetch(`${ENDPOINT}?${qs}`, { signal: AbortSignal.timeout(9000) });
  } catch (err) {
    return { got: new Map(), error: err?.name === 'TimeoutError' ? 'timeout' : String(err?.message || err) };
  }
  if (!res.ok) return { got: new Map(), error: `HTTP ${res.status}` };

  let body;
  try {
    body = await res.json();
  } catch {
    return { got: new Map(), error: 'bad JSON from provider' };
  }

  // Whole-request failure arrives as HTTP 200 with an error body — 429 for the
  // credit cap, 401 for a bad key. Surface it rather than silently serving stale.
  if (body && body.status === 'error') {
    return { got: new Map(), error: String(body.message || `code ${body.code}`).slice(0, 120) };
  }

  const got = new Map();
  const entries = symbols.length === 1 ? [[symbols[0], body]] : Object.entries(body || {});
  for (const [k, v] of entries) {
    if (!v || typeof v !== 'object') continue;
    if (v.status === 'error') continue;          // one bad symbol, rest still good
    const shaped = shape(v);
    if (!shaped) continue;
    // Prefer the symbol echoed back by the provider; fall back to the response key.
    got.set(String(v.symbol || k).toUpperCase(), shaped);
  }
  return { got, error: got.size ? null : 'no usable quotes in response' };
}

export default async () => {
  const key = process.env.TWELVEDATA_API_KEY;
  const open = marketOpen();

  const cacheHeaders = (h) => ({
    'Cache-Control': h,
    'Access-Control-Allow-Origin': '*',
    'X-Content-Type-Options': 'nosniff',
  });
  // Traffic-driven refresh: the CDN, not the browser, is what bounds credit spend.
  const CACHE = open
    ? 'public, max-age=60, s-maxage=300, stale-while-revalidate=900'
    : 'public, max-age=300, s-maxage=3600, stale-while-revalidate=86400';

  if (!key) {
    return Response.json(
      {
        ok: false,
        error: 'TWELVEDATA_API_KEY is not set on this site.',
        hint: 'Netlify → Site configuration → Environment variables, then redeploy.',
        companies: {},
      },
      { headers: cacheHeaders('no-store') },
    );
  }

  const batchSize = Math.max(1, Math.min(SYMBOLS.length, parseInt(process.env.TWELVEDATA_BATCH || '5', 10) || 5));

  // Stalest first, so every symbol comes round within a couple of invocations.
  const due = [...SYMBOLS]
    .sort((a, b) => (store.get(a)?.at ?? 0) - (store.get(b)?.at ?? 0))
    .slice(0, batchSize);

  const { got, error } = await fetchBatch(due, key);
  const now = Date.now();
  for (const [sym, q] of got) store.set(sym, { q, at: now });

  const companies = {};
  let oldest = null;
  for (const sym of SYMBOLS) {
    const hit = store.get(sym);
    if (!hit) continue;
    companies[sym] = { ...hit.q, ageSec: Math.round((now - hit.at) / 1000) };
    if (oldest == null || hit.at < oldest) oldest = hit.at;
  }

  const have = Object.keys(companies).length;
  if (!have) {
    return Response.json(
      { ok: false, error: error || 'no quotes available', marketOpen: open, companies: {} },
      { headers: cacheHeaders('no-store') },
    );
  }

  return Response.json(
    {
      ok: true,
      provider: 'twelvedata',
      fetchedAt: now,
      marketOpen: open,
      refreshed: [...got.keys()],       // which symbols are brand new this pass
      have,
      total: SYMBOLS.length,
      oldestSec: oldest == null ? null : Math.round((now - oldest) / 1000),
      ...(error ? { warning: error } : {}),
      companies,
    },
    { headers: cacheHeaders(CACHE) },
  );
};

export const config = { path: '/api/quotes' };
