# NBFC P/B &amp; Prices — mobile dashboard

A phone-first dashboard showing, for nine listed NBFCs: **live NSE price, day
move, and price-to-book**. One screen, one row per company, tap for the
arithmetic.

Book values are yours to set — they live in `book-values.json` and nowhere else.

This is a **separate site with its own URL**. It does not touch the Streamlit
dashboard in the repo root, or the `market-dashboard/` site.

---

## 1 · Get a Twelve Data key

Yahoo Finance (what `yfinance` and the Streamlit app use) rate-limits datacenter
IP addresses, which is exactly where any hosted site runs — it answers `HTTP 429`
more or less permanently from there. Verified again while building this. So the
hosted dashboard uses [Twelve Data](https://twelvedata.com/pricing) instead, which
is built to be called from servers and carries all nine NSE tickers under the
same codes.

1. Sign up — the free tier is enough (see the budget below)
2. Copy your API key

## 2 · Deploy it

Point a **new** Netlify site at this repo:

1. app.netlify.com → **Add new site → Import an existing project**
2. Pick this repository
3. **Base directory: `pb-dashboard`** ← the one setting that matters. Netlify then
   reads `pb-dashboard/netlify.toml` instead of the root one, so this site and the
   existing one stay independent.
4. Leave build command empty, publish directory `.`
5. **Site configuration → Environment variables → Add**: key `TWELVEDATA_API_KEY`,
   value your key
6. Deploy

Until the key is set the dashboard loads and tells you exactly what is missing,
rather than showing a blank page.

Add it to a phone home screen with Share → *Add to Home Screen*; it opens
full-screen with its own icon.

---

## 3 · Updating a book value

This is the whole workflow:

```bash
python pb-dashboard/tools/set_book_value.py CHOLAFIN 392 --as-of Q2FY27
git add pb-dashboard/book-values.json
git commit -m "book value: Chola Q2FY27 392"
git push
```

Netlify redeploys on push and the dashboard picks it up. No build step, no code
change. `book-values.json` is served with `must-revalidate`, so nothing stale is
cached.

Editing the JSON by hand does the same thing — the script just guards against
typos (it flags a move over 50% in one quarter, which is usually a fat finger or
a capital event worth confirming).

Other fields:

```bash
python pb-dashboard/tools/set_book_value.py --list                    # show the store
python pb-dashboard/tools/set_book_value.py SHRIRAMFIN 470 \
    --as-of Q2FY27 --shares 2600000000 --note "Post-MUFG share count"
```

`shares` only feeds **market cap** in the expanded row. It never touches P/B, which
divides price by `bvps` directly.

### Seeded values

Q1FY27, taken from `nbfc_data_cache.py` — the same source of truth as the
Streamlit dashboard, so the two agree on day one. Two carry caveats, recorded in
the file and shown when a row is expanded:

| Company | Caveat |
|---|---|
| Shriram Finance | BVPS jumped 349 → 462 on the Apr-2026 MUFG infusion. The stored share count predates the raise, so **market cap is understated** until refreshed. P/B is correct. |
| Aditya Birla Capital | BVPS is the NBFC entity; the share count is the listed group. P/B and market cap are on different bases. |

---

## 4 · The credit budget

Twelve Data's free tier is **800 API credits/day and 8 credits/minute**, where one
symbol costs one credit. Nine companies therefore **cannot** be fetched in one
burst — that is 9 credits in a minute, and Twelve Data rejects the whole batch
rather than trimming it. Splitting into 5+4 inside one request does not help
either; the cap is a rolling minute.

So `/api/quotes` refreshes the **stalest 5 symbols** per invocation and merges them
into a store that survives on the warm instance. Every symbol comes round within
about ten minutes — far finer than a P/B ratio actually moves.

| | |
|---|---|
| Trading day (CDN revalidates every 5 min) | ~390 credits |
| Overnight and weekends (every 60 min) | ~90 credits |
| **Total** | **~480 of 800** |

The function knows NSE hours (09:15–15:30 IST, Mon–Fri) and lengthens its cache
when the market is shut, which is where most of that saving comes from.

On a paid plan (Grow = 55 credits/min) set `TWELVEDATA_BATCH=9` and every
invocation refreshes everything at once.

---

## 5 · Local preview

```bash
python pb-dashboard/tools/devserver.py 8000 --mock     # synthetic, no credits spent
TWELVEDATA_API_KEY=... python pb-dashboard/tools/devserver.py 8000
```

The dev server implements `/api/quotes` with the same contract and the same
rotating-batch behaviour as the deployed function, so local behaviour matches
production. `--mock` returns deterministic fake numbers for UI work; production
has no such path.

---

## 6 · The fallback

`snapshot.json` holds dated prices that render when the live feed is unreachable,
so the page is never blank — clearly labelled *"Saved prices from &lt;date&gt;"*.
It ships empty; fill it once you have a key:

```bash
TWELVEDATA_API_KEY=... python pb-dashboard/tools/refresh_snapshot.py
python pb-dashboard/tools/refresh_snapshot.py --yahoo    # from a home IP only
```

One run costs 9 credits and takes about a minute (it waits out the per-minute
window between batches). Symbols that fail keep their previous values rather than
being blanked.

---

## 7 · How the numbers are computed

- **P/B** — live price ÷ `bvps` from `book-values.json`. Same method as
  `make_pb_chart()` in the Streamlit app, so the two agree.
- **Median P/B** — the middle value across companies that have both a price and a
  book value. Median, not mean, so one 0.78x or one 7.78x cannot drag it.
- **Day move** — Twelve Data's `percent_change`, i.e. last price vs the previous
  session's close.
- **P/B at 52w high / low** — that price ÷ **today's** book value. It answers "what
  would this multiple have been", not "what was it then"; the row says so.
- **Move to 1.0x book** — the price change that would take P/B to exactly 1.0.
- **Market cap** — price × stored share count. See the share-count caveat above.

Missing figures render as `—`. Nothing is estimated or carried forward silently.

---

## 8 · Design notes

- Portrait phone first: one row per company, 44px touch targets, safe-area padding
  for notched iPhones, no horizontal scroll at 390px. Above 520px the detail facts
  go to three columns; nothing else changes.
- **One hero figure** — median P/B. Everything else is subordinate to it.
- Colour is never the only signal: every change carries an explicit `+` or `−` and
  every row a rank number. The up/down pair is the only semantically loaded colour
  and both steps clear 4.5:1 on their own surface (light 7.35 / 4.68, dark
  5.19 / 5.39).
- Dark mode follows the OS and can be overridden with the ◐ button, remembered per
  device. The toggle wins over the OS setting in both directions.
- Long names wrap rather than truncate — "Cholamandalam Finance" stays readable
  next to a wide number.

## 9 · Files

| Path | What it is |
|---|---|
| `book-values.json` | **The store you edit.** BVPS, as-of quarter, share count, per-company notes. |
| `snapshot.json` | Dated fallback prices. |
| `index.html`, `assets/` | The dashboard. No dependencies, no build step. |
| `netlify/functions/quotes.mjs` | `/api/quotes` — the credit-aware Twelve Data proxy. |
| `tools/set_book_value.py` | Safe edits to the store. |
| `tools/refresh_snapshot.py` | Refresh the fallback prices. |
| `tools/devserver.py` | Local preview, with `--mock`. |
