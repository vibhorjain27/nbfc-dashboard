# NBFC Market & Valuation — mobile dashboard

A standalone, phone-first dashboard covering **only** the market and valuation
material, built to be shared with the MD. It is a static site (no Streamlit), so
it loads instantly on a phone and needs no server session.

Three tabs:

| Tab | Contents |
|---|---|
| **Prices** | Live NSE price tiles for all 9 NBFCs (price, day change, volume, market cap) + a single-company price history chart with 1W–5Y windows |
| **Compare** | Relative performance indexed to 100 over 1W–5Y, multi-select companies, plus a returns table |
| **Valuation** | P/B and P/E over time (1Y–5Y) plus a current-multiples table |

The Streamlit dashboard in the repo root is **untouched** — this is an additional
deliverable, not a replacement.

---

## Deploying to Netlify

### Option A — drag and drop (no Git connection)

Download **`nbfc-market-dashboard.zip`** from the repo root, unzip it, and drag the
resulting `nbfc-market-dashboard` folder onto app.netlify.com. It is self-contained
and carries its own `netlify.toml` with `publish = "."`. Instructions are in
`DEPLOY.md` inside the zip.

Rebuild that zip after changing anything here:

```bash
python market-dashboard/make_bundle.py
```

### Option B — connect the Git repo (auto-deploys on push)

`netlify.toml` at the repo root already points Netlify at this folder, so there is
nothing to configure in the UI.

1. Netlify → **Add new site → Import an existing project** → pick this repo.
2. Branch: `claude/review-project-codebase-awUPX` (or `main` once merged).
3. Leave build command empty; publish directory and functions are read from
   `netlify.toml`. Click **Deploy**.

That's it. Netlify serves `market-dashboard/` as the site and deploys
`market-dashboard/netlify/functions/yahoo.mjs` as `/api/yahoo`.

### Why a function is needed

The browser cannot call `query1.finance.yahoo.com` directly — Yahoo sends no CORS
headers, so the request is blocked. `yahoo.mjs` is a thin server-side pass-through
to the **same v8 chart endpoint that the `yfinance` Python package uses
internally**, which is what the Streamlit dashboard reads. Both dashboards
therefore show the same numbers from the same upstream source.

The function only proxies the 9 whitelisted tickers, and responses are cached at
the CDN (60s intraday, 300s for daily history) so the MD's phone loads instantly
and Yahoo is not hammered.

---

## Local preview

```bash
python market-dashboard/devserver.py 8000
# then open http://localhost:8000
```

`devserver.py` serves the static files and implements `/api/yahoo` with the same
contract as the Netlify function, so local behaviour matches production.

---

## Updating the fundamentals

Price data is live. Book value and earnings are baked in at build time from
`nbfc_data_cache.py` — the **same source of truth as the Streamlit dashboard**, so
the two can never drift.

After editing `nbfc_data_cache.py`, regenerate and commit:

```bash
python market-dashboard/generate_data.py                  # rewrites assets/data.js
python market-dashboard/generate_data.py --refresh-shares # also re-pulls share counts
```

Netlify redeploys on push.

---

## How the numbers are computed

- **Day change** — last daily close vs the previous session's close (identical to
  the Streamlit tiles). Yahoo's `chartPreviousClose` is deliberately *not* used: it
  means "close before the requested range began", which would report a one-month
  move as if it were today's.
- **Indexed to 100** — `(price ÷ price on the first day of the window) × 100`.
- **P/B** — daily close ÷ most recently reported quarterly BVPS, stepping at each
  quarter end. Same method as `make_pb_chart()` in the Streamlit app.
- **P/E** — daily close ÷ trailing-twelve-month EPS, where TTM EPS is the last four
  quarters of reported PAT ÷ shares outstanding. Because it needs four consecutive
  quarters, the P/E series begins at Q3FY25 (Dec 2024).
- **Market cap** — live price × shares outstanding.

### Known data gaps

These are gaps in the underlying filings data, and show up as shorter lines:

| Company | Gap |
|---|---|
| Piramal Finance | BVPS only for the last 2 quarters (entity restructured post-DHFL) |
| Aditya Birla Capital | BVPS for 5 of 9 quarters |
| Mahindra Finance | BVPS 7 of 9; Q4FY26 PAT not yet reported, so TTM EPS stops at Q3FY26 |

---

## Design notes

- **Portrait phone is the primary target.** Two-column price tiles, horizontally
  scrolling company chips, full-width period buttons, 44px touch targets, and
  safe-area padding for notched iPhones. Landscape and desktop widen progressively.
- **P/E uses a log axis.** These names span ~12x to ~200x (Poonawalla's
  recovery-year trailing earnings). On a linear axis that outlier flattens every
  other line onto the baseline.
- **Charts are hand-rolled SVG** — no charting library, so the page stays small and
  touch behaviour is exactly what a phone needs (crosshair snaps to the nearest
  date, one tooltip lists every series, vertical page scroll still passes through).
- **Colours match the Streamlit dashboard** so the two read as one system. The
  9-hue palette was validated for colourblind separation and contrast against both
  the light and dark surfaces; dark mode uses its own steps rather than an
  automatic flip. Every series also carries its name on a chip, a direct value
  label at the line end, and a row in the table, so identity is never colour-alone.
- **Dark mode** follows the OS and can be overridden with the moon button
  (remembered on the device).
