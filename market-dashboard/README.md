# NBFC Market & Valuation — mobile dashboard

A standalone, phone-first dashboard for sharing with the MD. Static site (no
Streamlit), three list views, **no charts** — every number is legible at a glance
in portrait.

| Tab | Contents | Controls |
|---|---|---|
| **Prices** | All 9 companies, one per row: price, day change, volume, market cap | none |
| **Movement** | % move over a chosen window, large type, ranked best → worst, with start → end prices | time window only |
| **P/B** | Price-to-book today, ranked richest → cheapest, with P/E, price and BVPS | none |

The Streamlit dashboard in the repo root is **untouched** — this is an additional
deliverable, not a replacement.

---

## ⚠️ Read this first: the price feed

**Yahoo Finance rate-limits cloud/datacenter IP addresses**, which is exactly
where a Netlify function runs. It answers `HTTP 429` more or less permanently
from there. This was verified directly:

- Querying the deployed endpoint returned `{"ok":false,"error":"HTTP 429"}`
- After both were throttled, a residential machine recovered in ~8 minutes while
  Netlify stayed blocked for 20+ minutes **with zero traffic hitting it**
- Even from a residential IP, Yahoo recovers only in narrow windows — often one
  request gets through before it blocks again

The Streamlit dashboard is unaffected because it runs on your own machine.

### The fix: `TWELVEDATA_API_KEY` (recommended)

[Twelve Data](https://twelvedata.com/pricing) is built to be called from servers,
so there is no datacenter block. All nine NSE tickers exist there under identical
codes (`BAJFINANCE`, `LTF`, `M&MFIN`, …) — verified against their symbol registry.

1. Sign up (free tier: 800 API credits/day)
2. Netlify → **Site configuration → Environment variables → Add**
3. Key `TWELVEDATA_API_KEY`, value your key
4. **Deploys → Trigger deploy**

The function picks it up automatically and reports `provider: "twelvedata"` in its
response. Budget: one call per ticker per upstream refresh = 9 credits; with the
10-minute CDN cache a full trading day costs roughly 500 of the 800 free credits.

With no key set, the function falls back to Yahoo — which works from a residential
IP but generally will not from Netlify.

### The safety net: a baked snapshot

`assets/data.js` carries a dated price snapshot. If the live feed fails entirely,
the dashboard renders those numbers and says *"Showing saved prices from &lt;date&gt;"*
rather than showing an empty page.

Refresh it from a machine that can reach Yahoo (i.e. your own):

```bash
python market-dashboard/bake_snapshot.py     # incremental, survives throttling
python market-dashboard/make_bundle.py       # rebuild the deployable zip
```

`bake_snapshot.py` grabs whatever tickers it can on each pass, writes each one to
disk the moment it lands, and keeps retrying only the ones still missing — which
is what Yahoo's narrow recovery windows require.

---

## Deploying to Netlify

### Option A — drag and drop

Download **`nbfc-market-dashboard.zip`** from the repo root, unzip, and drag the
`nbfc-market-dashboard` folder onto app.netlify.com. It is self-contained and
carries its own `netlify.toml` with `publish = "."`. Full steps in `DEPLOY.md`
inside the zip.

Rebuild the zip after any change here:

```bash
python market-dashboard/make_bundle.py
```

### Option B — connect the Git repo (auto-deploys on push)

`netlify.toml` at the repo root already points Netlify at this folder, so leave
the build command empty and there is nothing to configure in the UI.

---

## Local preview

```bash
python market-dashboard/devserver.py 8000            # real data
python market-dashboard/devserver.py 8000 --mock     # synthetic, for UI work
```

`devserver.py` implements `/api/market` with the same contract as the Netlify
function. `--mock` returns deterministic fake numbers so the UI can be exercised
while upstream is throttled; production has no such path.

---

## Updating the fundamentals

Book value and earnings are baked in at build time from `nbfc_data_cache.py` —
the **same source of truth as the Streamlit dashboard**, so the two cannot drift.

```bash
python market-dashboard/generate_data.py                  # rewrites assets/data.js
python market-dashboard/generate_data.py --no-snapshot    # skip the price refresh
python market-dashboard/generate_data.py --refresh-shares # also re-pull share counts
```

---

## How the numbers are computed

- **Day change** — last close vs the previous session's close. Yahoo's
  `chartPreviousClose` is deliberately *not* used: it means "close before the
  requested range began", which reported a five-year-old move as if it were today's.
- **Window movement** — `(price ÷ close nearest the window start − 1) × 100`. The
  row footer shows both prices and the exact start date, so the number is checkable.
- **P/B** — live price ÷ most recently reported quarterly BVPS. Same method as
  `make_pb_chart()` in the Streamlit app.
- **P/E** — live price ÷ trailing-twelve-month EPS (last four quarters of reported
  PAT ÷ shares outstanding). Needs four consecutive quarters, so it begins at Q3FY25.
- **Market cap** — live price × shares outstanding.

### Known data gaps

Gaps in the underlying filings, shown as `—` rather than guessed:

| Company | Gap |
|---|---|
| Piramal Finance | BVPS only for the last 2 quarters (entity restructured post-DHFL) |
| Aditya Birla Capital | BVPS for 5 of 9 quarters |
| Mahindra Finance | BVPS 7 of 9; Q4FY26 PAT not yet reported, so TTM EPS stops at Q3FY26 |

---

## Design notes

- Portrait phone is the primary target: one row per company, large figures,
  44px touch targets, safe-area padding for notched iPhones. Above 620px the rows
  become two columns; nothing else changes.
- Long names wrap rather than truncate — "Cholamandalam Finance" stays readable
  next to a wide price.
- Colour is never the only signal: every row carries a sign (`+`/`−`), a rank
  number where ranked, and the underlying figures in the footer.
- Dark mode follows the OS and can be overridden with the moon button
  (remembered on the device).
