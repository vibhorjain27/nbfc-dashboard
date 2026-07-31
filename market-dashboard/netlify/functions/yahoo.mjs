/**
 * Yahoo Finance proxy.
 *
 * The browser cannot call query1.finance.yahoo.com directly — it sends no CORS
 * headers. This function is a thin server-side pass-through to the SAME v8 chart
 * endpoint that the `yfinance` Python package uses internally, so the mobile
 * dashboard and the Streamlit dashboard read identical numbers from identical
 * source data.
 *
 *   GET /api/yahoo?symbols=BAJFINANCE.NS,LTF.NS&range=1y&interval=1d
 *
 * Response:
 *   { ok, fetchedAt, series: { "<symbol>": { meta:{...}, t:[epoch…], c:[close…] } | { error } } }
 */

const HOSTS = [
  'https://query1.finance.yahoo.com',
  'https://query2.finance.yahoo.com',
];

const VALID_RANGE = new Set(['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']);
const VALID_INTERVAL = new Set(['1m', '5m', '15m', '30m', '1h', '1d', '1wk', '1mo']);

// Only these tickers may be proxied — stops the function being used as an open relay.
const ALLOWED = new Set([
  'POONAWALLA.NS', 'BAJFINANCE.NS', 'SHRIRAMFIN.NS', 'LTF.NS', 'CHOLAFIN.NS',
  'ABCAPITAL.NS', 'PIRAMALFIN.NS', 'MUTHOOTFIN.NS', 'M&MFIN.NS',
]);

const UA =
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 ' +
  '(KHTML, like Gecko) Chrome/124.0 Safari/537.36';

async function fetchOne(symbol, range, interval) {
  const qs = new URLSearchParams({ range, interval, includePrePost: 'false' });
  const path = `/v8/finance/chart/${encodeURIComponent(symbol)}?${qs}`;

  let lastErr = 'unknown';
  for (const host of HOSTS) {
    try {
      const res = await fetch(host + path, {
        headers: { 'User-Agent': UA, Accept: 'application/json' },
        signal: AbortSignal.timeout(9000),
      });
      if (!res.ok) { lastErr = `HTTP ${res.status}`; continue; }

      const json = await res.json();
      const result = json?.chart?.result?.[0];
      if (!result) { lastErr = json?.chart?.error?.description || 'empty result'; continue; }

      const meta = result.meta ?? {};
      const stamps = result.timestamp ?? [];
      const closes = result.indicators?.quote?.[0]?.close ?? [];
      const volumes = result.indicators?.quote?.[0]?.volume ?? [];

      // Drop nulls (holidays / halted sessions) so the client never plots gaps.
      const t = [];
      const c = [];
      const v = [];
      for (let i = 0; i < stamps.length; i += 1) {
        if (closes[i] === null || closes[i] === undefined) continue;
        t.push(stamps[i]);
        c.push(Number(closes[i].toFixed(4)));
        v.push(volumes?.[i] ?? 0);
      }

      return {
        meta: {
          symbol:       meta.symbol ?? symbol,
          name:         meta.longName ?? meta.shortName ?? symbol,
          currency:     meta.currency ?? 'INR',
          price:        meta.regularMarketPrice ?? null,
          prevClose:    meta.chartPreviousClose ?? meta.previousClose ?? null,
          dayHigh:      meta.regularMarketDayHigh ?? null,
          dayLow:       meta.regularMarketDayLow ?? null,
          volume:       meta.regularMarketVolume ?? null,
          fiftyTwoHigh: meta.fiftyTwoWeekHigh ?? null,
          fiftyTwoLow:  meta.fiftyTwoWeekLow ?? null,
          marketTime:   meta.regularMarketTime ?? null,
          exchange:     meta.fullExchangeName ?? 'NSE',
        },
        t, c, v,
      };
    } catch (err) {
      lastErr = err?.name === 'TimeoutError' ? 'timeout' : String(err?.message || err);
    }
  }
  return { error: lastErr };
}

export default async (req) => {
  const url = new URL(req.url);

  const symbols = (url.searchParams.get('symbols') || '')
    .split(',')
    .map((s) => s.trim())
    .filter((s) => ALLOWED.has(s))
    .slice(0, 12);

  const range = VALID_RANGE.has(url.searchParams.get('range')) ? url.searchParams.get('range') : '1mo';
  const interval = VALID_INTERVAL.has(url.searchParams.get('interval')) ? url.searchParams.get('interval') : '1d';

  if (!symbols.length) {
    return Response.json({ ok: false, error: 'no valid symbols' }, { status: 400 });
  }

  const settled = await Promise.all(symbols.map((s) => fetchOne(s, range, interval)));
  const series = Object.fromEntries(symbols.map((s, i) => [s, settled[i]]));
  const ok = settled.some((r) => !r.error);

  // Intraday data gets a short TTL; daily history is cached harder. stale-while-revalidate
  // keeps the dashboard instant on the MD's phone even while a refresh is in flight.
  const ttl = interval === '1d' && range !== '1d' ? 300 : 60;

  return Response.json(
    { ok, fetchedAt: Date.now(), series },
    {
      headers: {
        'Cache-Control': `public, max-age=${ttl}, s-maxage=${ttl}, stale-while-revalidate=600`,
        'Access-Control-Allow-Origin': '*',
      },
    },
  );
};

export const config = { path: '/api/yahoo' };
