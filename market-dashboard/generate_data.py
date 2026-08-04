#!/usr/bin/env python3
"""
Generate assets/data.js for the mobile market dashboard.

Reads the SAME source of truth as the main Streamlit dashboard
(nbfc_data_cache.py) so the two can never drift, and bakes the
valuation inputs into a static JS file:

  * BVPS series (quarterly)      -> drives P/B
  * TTM EPS series (derived)     -> drives P/E
  * shares outstanding           -> converts PAT (Cr) into per-share EPS

P/B and P/E are then computed IN THE BROWSER as:
    daily NSE close / most-recently-reported quarterly BVPS (or TTM EPS)

which is exactly the methodology make_pb_chart() uses in the main
dashboard, so the numbers agree.

Run:  python market-dashboard/generate_data.py
"""

import json
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nbfc_data_cache import NBFC_TIMESERIES, QUARTERS, quarter_end_date  # noqa: E402

# ── Registry — mirrors nbfc_dashboard_v1.py exactly ───────────────────────────
NBFCS = {
    'Poonawalla Fincorp':    'POONAWALLA.NS',
    'Bajaj Finance':         'BAJFINANCE.NS',
    'Shriram Finance':       'SHRIRAMFIN.NS',
    'L&T Finance':           'LTF.NS',
    'Cholamandalam Finance': 'CHOLAFIN.NS',
    'Aditya Birla Capital':  'ABCAPITAL.NS',
    'Piramal Finance':       'PIRAMALFIN.NS',
    'Muthoot Finance':       'MUTHOOTFIN.NS',
    'Mahindra Finance':      'M&MFIN.NS',
}

# nbfc_data_cache uses a slightly different key for Chola
CACHE_KEY = {
    'Poonawalla Fincorp':    'Poonawalla Fincorp',
    'Bajaj Finance':         'Bajaj Finance',
    'Shriram Finance':       'Shriram Finance',
    'L&T Finance':           'L&T Finance',
    'Cholamandalam Finance': 'Chola Finance',
    'Aditya Birla Capital':  'Aditya Birla Capital',
    'Piramal Finance':       'Piramal Finance',
    'Muthoot Finance':       'Muthoot Finance',
    'Mahindra Finance':      'Mahindra Finance',
}

# Same 9 hues as the main dashboard (validated: passes lightness band, chroma
# floor, CVD separation and normal-vision floor; orange + green carry a
# sub-3:1 contrast WARN, relieved by direct labels + the table view).
COLORS = {
    'Poonawalla Fincorp':    '#0284c7',
    'Bajaj Finance':         '#f97316',
    'Shriram Finance':       '#10b981',
    'L&T Finance':           '#8b5cf6',
    'Cholamandalam Finance': '#ef4444',
    'Aditya Birla Capital':  '#0891b2',
    'Piramal Finance':       '#be123c',
    'Muthoot Finance':       '#65a30d',
    'Mahindra Finance':      '#7c3aed',
}

# Dark-surface steps of the same nine hues — selected, not an automatic flip.
# Validated against surface #1a1a19: lightness band, chroma floor, normal-vision
# floor and 3:1 contrast all PASS. Worst adjacent CVD pair is Muthoot lime vs
# Piramal crimson at ΔE 6.3 (deutan) — inside the 6–8 band, which is legal here
# because every series also carries secondary encoding: named chips with dots,
# direct value labels at the line ends, and a full table view.
COLORS_DARK = {
    'Poonawalla Fincorp':    '#0284c7',
    'Bajaj Finance':         '#e0690c',
    'Shriram Finance':       '#0d9e6e',
    'L&T Finance':           '#8b5cf6',
    'Cholamandalam Finance': '#ef4444',
    'Aditya Birla Capital':  '#0891b2',
    'Piramal Finance':       '#e11d48',
    'Muthoot Finance':       '#65a30d',
    'Mahindra Finance':      '#7c3aed',
}

SHORT = {
    'Poonawalla Fincorp':    'Poonawalla',
    'Bajaj Finance':         'Bajaj Fin',
    'Shriram Finance':       'Shriram',
    'L&T Finance':           'L&T Fin',
    'Cholamandalam Finance': 'Chola',
    'Aditya Birla Capital':  'AB Capital',
    'Piramal Finance':       'Piramal',
    'Muthoot Finance':       'Muthoot',
    'Mahindra Finance':      'M&M Fin',
}

# Shares outstanding, from yfinance fast_info.shares (same source the main
# dashboard uses for its market-cap trend). Refresh with --refresh-shares.
SHARES_FALLBACK = {
    'POONAWALLA.NS':  875_682_194,
    'BAJFINANCE.NS':  6_217_876_336,
    'SHRIRAMFIN.NS':  2_352_948_439,
    'LTF.NS':         2_506_045_818,
    'CHOLAFIN.NS':    854_013_036,
    'ABCAPITAL.NS':   2_736_107_195,
    'PIRAMALFIN.NS':  226_004_925,
    'MUTHOOTFIN.NS':  401_468_476,
    'M&MFIN.NS':      1_389_545_161,
}

# Quarter-end dates aligned to QUARTERS, derived from the labels so the rolling
# window never needs a code change here.
QUARTER_END_DATES = [quarter_end_date(q).isoformat() for q in QUARTERS]


def ttm_eps_series(pat_cr, shares):
    """Trailing-twelve-month EPS (₹/share) per quarter.

    TTM PAT at quarter i = sum(PAT[i-3 .. i]); needs 4 consecutive quarters, so
    the series starts at index 3. PAT is in ₹ Crore (1 Cr = 1e7).
    """
    out = [None] * len(pat_cr)
    if not shares:
        return out
    for i in range(3, len(pat_cr)):
        window = pat_cr[i - 3:i + 1]
        if any(v is None for v in window):
            continue
        out[i] = round(sum(window) * 1e7 / shares, 4)
    return out


WINDOWS = {'1W': 7, '1M': 30, '3M': 91, '6M': 182, '1Y': 365, '3Y': 1095, '5Y': 1825}

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')


def fetch_snapshot(symbol):
    """One ticker's prices + window moves, shaped exactly like /api/market.

    Baked into data.js as a fallback so the dashboard always renders real
    numbers — clearly dated — even when the live feed is rate-limiting.
    Returns None on failure; the caller keeps any previous snapshot.
    """
    import json as _json
    import urllib.request
    import urllib.parse

    url = ('https://query1.finance.yahoo.com/v8/finance/chart/'
           f'{urllib.parse.quote(symbol)}?range=5y&interval=1d')
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/json'})
    try:
        res = _json.load(urllib.request.urlopen(req, timeout=25))['chart']['result'][0]
    except Exception:
        return None

    meta = res.get('meta') or {}
    stamps = res.get('timestamp') or []
    q = ((res.get('indicators') or {}).get('quote') or [{}])[0]
    raw_c, raw_v = q.get('close') or [], q.get('volume') or []

    t, c, v = [], [], []
    for i, ts in enumerate(stamps):
        if i >= len(raw_c) or raw_c[i] is None:
            continue
        t.append(ts * 1000)
        c.append(float(raw_c[i]))
        v.append(raw_v[i] if i < len(raw_v) and raw_v[i] is not None else 0)
    if len(c) < 2:
        return None

    price = meta.get('regularMarketPrice') or c[-1]
    prev = c[-2]
    now = t[-1]

    windows = {}
    for label, days in WINDOWS.items():
        target = now - days * 86400000
        if t[0] > target + 86400000 * 7:
            continue
        i = min(range(len(t)), key=lambda k: abs(t[k] - target))
        base = c[i]
        if not base:
            continue
        windows[label] = {
            'from': round(base, 2),
            'at': t[i],
            'pct': round((price - base) / base * 100, 2),
        }

    return {
        'price': round(price, 2),
        'prevClose': round(prev, 2),
        'changeAbs': round(price - prev, 2),
        'changePct': round((price - prev) / prev * 100, 2),
        'volume': meta.get('regularMarketVolume') or (v[-1] if v else 0),
        'windows': windows,
    }


def load_existing_snapshots(path):
    """Keep the previous snapshot for any ticker that fails this run."""
    try:
        with open(path, encoding='utf-8') as fh:
            blob = fh.read().split('window.NBFC_DATA = ', 1)[1].rstrip().rstrip(';')
        prev = json.loads(blob)
        return ({c['symbol']: c.get('snapshot') for c in prev.get('companies', [])},
                prev.get('snapshotAt'))
    except Exception:
        return {}, None


def refresh_shares():
    """Re-pull shares outstanding from yfinance."""
    import yfinance as yf
    fresh = {}
    for name, sym in NBFCS.items():
        try:
            s = yf.Ticker(sym).fast_info.shares
            fresh[sym] = int(s) if s else SHARES_FALLBACK.get(sym)
            print(f'  {name:24s} {sym:16s} {fresh[sym]:,}')
        except Exception as exc:
            fresh[sym] = SHARES_FALLBACK.get(sym)
            print(f'  {name:24s} {sym:16s} FAILED ({type(exc).__name__}) — kept fallback')
    return fresh


def main():
    shares_map = refresh_shares() if '--refresh-shares' in sys.argv else dict(SHARES_FALLBACK)

    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'data.js')

    old_snaps, old_snap_at = load_existing_snapshots(out_path)

    # Refresh the baked price snapshot unless told not to. Failures keep the
    # previous values rather than blanking them.
    snaps = dict(old_snaps)
    snap_at = old_snap_at
    if '--no-snapshot' not in sys.argv:
        import time as _time
        fresh = 0
        print('Refreshing price snapshot…')
        for name, sym in NBFCS.items():
            got = fetch_snapshot(sym)
            if got:
                snaps[sym] = got
                fresh += 1
                print(f'  {name:24s} ₹{got["price"]:>10,.2f}  {got["changePct"]:+.2f}%')
            else:
                print(f'  {name:24s} failed — keeping previous snapshot')
            _time.sleep(0.35)      # sequential + jitter; bursts trip Yahoo's limiter
        if fresh:
            snap_at = date.today().isoformat()
        print(f'  → {fresh}/{len(NBFCS)} refreshed\n')

    companies = []
    for name, sym in NBFCS.items():
        ck = CACHE_KEY[name]
        series = NBFC_TIMESERIES.get(ck, {})
        bvps = list(series.get('bvps_inr', [None] * len(QUARTERS)))
        pat = list(series.get('pat_cr', [None] * len(QUARTERS)))
        shares = shares_map.get(sym)

        companies.append({
            'name':   name,
            'short':  SHORT[name],
            'symbol': sym,
            'ticker': sym.replace('.NS', ''),
            'color':     COLORS[name],
            'colorDark': COLORS_DARK[name],
            'shares': shares,
            'bvps':   bvps,
            'eps':    ttm_eps_series(pat, shares),
            'snapshot': snaps.get(sym),
        })

    payload = {
        'generated':    date.today().isoformat(),
        'quarters':     list(QUARTERS),
        'quarterEnds':  QUARTER_END_DATES,
        'snapshotAt':   snap_at,
        'companies':    companies,
    }

    with open(out_path, 'w', encoding='utf-8') as fh:
        fh.write('// AUTO-GENERATED by generate_data.py — do not edit by hand.\n')
        fh.write('// Source of truth: nbfc_data_cache.py (same as the Streamlit dashboard).\n')
        fh.write('window.NBFC_DATA = ')
        json.dump(payload, fh, indent=2, ensure_ascii=False)
        fh.write(';\n')

    # ── report ────────────────────────────────────────────────────────────────
    print(f'\nWrote {out_path}')
    print(f'{"Company":24s} {"BVPS":>6s} {"TTM EPS":>8s}   latest BVPS / EPS')
    print('-' * 66)
    for c in companies:
        nb = sum(1 for v in c['bvps'] if v is not None)
        ne = sum(1 for v in c['eps'] if v is not None)
        lb = next((v for v in reversed(c['bvps']) if v is not None), None)
        le = next((v for v in reversed(c['eps']) if v is not None), None)
        print(f'{c["name"]:24s} {nb:>4d}/9 {ne:>6d}/9   '
              f'₹{lb if lb else "—"} / ₹{le if le else "—"}')


if __name__ == '__main__':
    main()
