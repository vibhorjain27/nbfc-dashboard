"""
NBFC Dashboard — FastAPI Backend
Serves static HTML and JSON API endpoints for all 10 dashboard tabs.
Run with: uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from typing import Optional
from pathlib import Path
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import sys, os

sys.path.insert(0, str(Path(__file__).parent))

import yfinance as yf
import pandas as pd
import numpy as np

from nbfc_data_cache import (
    NBFC_TIMESERIES, QUARTERS, METRIC_LABELS, NBFC_Q3FY26
)
from nbfc_ai_data import NBFC_AI_INITIATIVES, FUNCTION_TAXONOMY
from shareholding_data import (
    SHAREHOLDING, SH_QUARTERS,
    CATEGORY_COLORS, ENTITY_CATEGORY_COLORS, ENTITY_BADGE_TEXT_COLORS,
)

# ─── APP SETUP ─────────────────────────────────────────────────────────────────

app = FastAPI(title="NBFC Dashboard")
STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# ─── CONSTANTS ─────────────────────────────────────────────────────────────────

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

PERIOD_DELTA = {
    '1W': timedelta(weeks=1),
    '1M': timedelta(days=30),
    '3M': timedelta(days=91),
    '6M': timedelta(days=182),
    '1Y': timedelta(days=365),
    '3Y': timedelta(days=365 * 3),
    '5Y': timedelta(days=365 * 5),
}

QUARTER_ENDS = [
    ('2024-03-31', 0),
    ('2024-06-30', 1),
    ('2024-09-30', 2),
    ('2024-12-31', 3),
    ('2025-03-31', 4),
    ('2025-06-30', 5),
    ('2025-09-30', 6),
    ('2025-12-31', 7),
]

# ─── HTML ROUTE ────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def root():
    return (STATIC_DIR / "index.html").read_text(encoding="utf-8")

# ─── STATIC DATA ENDPOINTS ─────────────────────────────────────────────────────

@app.get("/api/financials")
async def get_financials():
    """All 8-quarter time-series data + Q3FY26 snapshot for all 9 NBFCs."""
    latest_map = {item["name"]: {k: v for k, v in item.items()} for item in NBFC_Q3FY26}
    return {
        "quarters":  QUARTERS,
        "data":      NBFC_TIMESERIES,
        "cache_key": CACHE_KEY,
        "colors":    COLORS,
        "nbfc_list": list(NBFCS.keys()),
        "latest":    latest_map,
        "metric_labels": {k: list(v) for k, v in METRIC_LABELS.items()},
    }


@app.get("/api/ai")
async def get_ai():
    """51 AI/GenAI initiatives across 9 NBFCs."""
    return {
        "initiatives": NBFC_AI_INITIATIVES,
        "functions":   FUNCTION_TAXONOMY,
        "nbfc_list":   list(NBFC_AI_INITIATIVES.keys()),
    }


@app.get("/api/shareholding")
async def get_shareholding():
    """Shareholding pattern data — 8 quarters, 5 NBFCs."""
    serializable = {}
    for nbfc, d in SHAREHOLDING.items():
        serializable[nbfc] = {
            "category_pct":   d["category_pct"],
            "named_entities": d["named_entities"],
        }
    return {
        "data":                   serializable,
        "quarters":               SH_QUARTERS,
        "category_colors":        CATEGORY_COLORS,
        "entity_category_colors": ENTITY_CATEGORY_COLORS,
        "entity_badge_text":      ENTITY_BADGE_TEXT_COLORS,
    }

# ─── LIVE DATA ENDPOINTS ────────────────────────────────────────────────────────

@app.get("/api/prices")
async def get_prices():
    """Live NSE closing prices, daily change, volume, market cap for all 9 NBFCs."""
    symbols  = list(NBFCS.values())
    name_map = {v: k for k, v in NBFCS.items()}
    rows: dict = {}

    # Batch download (faster, avoids per-ticker rate-limits)
    try:
        raw = yf.download(
            symbols, period='5d', group_by='ticker',
            auto_adjust=True, progress=False, threads=False,
        )
        if raw is not None and not raw.empty:
            for sym in symbols:
                try:
                    df = raw[sym] if len(symbols) > 1 else raw
                    df = df.dropna(subset=['Close'])
                    if len(df) < 2:
                        continue
                    cur  = float(df['Close'].iloc[-1])
                    prev = float(df['Close'].iloc[-2])
                    chg  = cur - prev
                    rows[sym] = {
                        'name':       name_map[sym],
                        'symbol':     sym.replace('.NS', ''),
                        'price':      round(cur,  2),
                        'change_abs': round(chg,  2),
                        'change_pct': round(chg / prev * 100, 2),
                        'volume':     int(df['Volume'].iloc[-1]) if 'Volume' in df.columns else 0,
                        'market_cap': None,
                    }
                except Exception:
                    continue
    except Exception:
        pass

    # Retry any missed individually
    for sym in [s for s in symbols if s not in rows]:
        try:
            h = yf.Ticker(sym).history(period='5d').dropna(subset=['Close'])
            if len(h) < 2:
                continue
            cur  = float(h['Close'].iloc[-1])
            prev = float(h['Close'].iloc[-2])
            chg  = cur - prev
            rows[sym] = {
                'name':       name_map[sym],
                'symbol':     sym.replace('.NS', ''),
                'price':      round(cur,  2),
                'change_abs': round(chg,  2),
                'change_pct': round(chg / prev * 100, 2),
                'volume':     int(h['Volume'].iloc[-1]) if 'Volume' in h.columns else 0,
                'market_cap': None,
            }
        except Exception:
            continue

    # Enrich market cap in parallel
    def _mc(sym):
        try:
            mc = yf.Ticker(sym).fast_info.market_cap
            return sym, int(mc) if mc and mc > 0 else None
        except Exception:
            return sym, None

    with ThreadPoolExecutor(max_workers=len(rows) or 1) as ex:
        for sym, mc in ex.map(_mc, list(rows.keys())):
            rows[sym]['market_cap'] = mc

    return [rows[s] for s in symbols if s in rows]


@app.get("/api/performance")
async def get_performance(
    period:     str           = "6M",
    tickers:    str           = "",
    start_date: Optional[str] = None,
    end_date:   Optional[str] = None,
):
    """Indexed-to-100 performance chart data."""
    selected = [t.strip() for t in tickers.split(',') if t.strip() and t.strip() in NBFCS]
    if not selected:
        selected = list(NBFCS.keys())

    use_custom = bool(start_date and end_date)
    if use_custom:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt   = datetime.strptime(end_date,   '%Y-%m-%d')
    else:
        end_dt   = datetime.now()
        start_dt = end_dt - PERIOD_DELTA.get(period, timedelta(days=182))

    result = {}
    for name in selected:
        sym = NBFCS[name]
        try:
            hist = yf.Ticker(sym).history(
                start=start_dt.strftime('%Y-%m-%d'),
                end=end_dt.strftime('%Y-%m-%d'),
            )
            if hist is None or hist.empty:
                continue
            closes = hist['Close'].dropna()
            if len(closes) < 2:
                continue
            base = float(closes.iloc[0])
            result[name] = {
                'dates':  [str(d.date()) for d in closes.index],
                'values': [round(float(v) / base * 100, 2) for v in closes],
                'color':  COLORS[name],
            }
        except Exception:
            continue

    return result


@app.get("/api/mktcap")
async def get_mktcap(tickers: str = ""):
    """1-year daily market cap trend (₹ Lakh Crore) for selected NBFCs."""
    selected = [t.strip() for t in tickers.split(',') if t.strip() and t.strip() in NBFCS]
    if not selected:
        selected = list(NBFCS.keys())

    def _shares(item):
        name, sym = item
        try:
            s = yf.Ticker(sym).fast_info.shares
            return name, sym, int(s) if s and s > 0 else None
        except Exception:
            return name, sym, None

    shares_map = {}
    with ThreadPoolExecutor(max_workers=len(selected)) as ex:
        for name, sym, sh in ex.map(_shares, [(n, NBFCS[n]) for n in selected]):
            if sh:
                shares_map[name] = (sym, sh)

    result = {}
    for name, (sym, shares) in shares_map.items():
        try:
            hist = yf.Ticker(sym).history(period='1y')
            if hist is None or hist.empty:
                continue
            mc = (hist['Close'] * shares) / 1e12
            result[name] = {
                'dates':  [str(d.date()) for d in hist.index],
                'values': [round(float(v), 4) for v in mc.values],
                'color':  COLORS[name],
            }
        except Exception:
            continue

    return result


@app.get("/api/pb")
async def get_pb(tickers: str = ""):
    """2-year daily P/B ratio data using stepped quarterly BVPS."""
    selected = [t.strip() for t in tickers.split(',') if t.strip() and t.strip() in NBFCS]
    if not selected:
        selected = ['Poonawalla Fincorp']

    result = {}
    for name in selected:
        ck        = CACHE_KEY[name]
        bvps_vals = NBFC_TIMESERIES[ck]['bvps_inr']
        sym       = NBFCS[name]
        try:
            hist = yf.Ticker(sym).history(period='2y')
            if hist is None or hist.empty:
                continue

            dates, pb_vals, prices_list, bvps_list = [], [], [], []
            for dt, row in hist.iterrows():
                try:
                    price = float(row['Close'])
                    if price <= 0:
                        continue
                    date_str = str(pd.Timestamp(dt).date())

                    bvps = None
                    for qend, idx in reversed(QUARTER_ENDS):
                        if date_str >= qend:
                            bv = bvps_vals[idx]
                            if bv is not None and bv > 0:
                                bvps = bv
                            break
                    if bvps is None:
                        continue

                    dates.append(date_str)
                    pb_vals.append(round(price / bvps, 3))
                    prices_list.append(round(price, 2))
                    bvps_list.append(bvps)
                except Exception:
                    continue

            if dates:
                result[name] = {
                    'dates':  dates,
                    'pb':     pb_vals,
                    'prices': prices_list,
                    'bvps':   bvps_list,
                    'color':  COLORS[name],
                }
        except Exception:
            continue

    return result
