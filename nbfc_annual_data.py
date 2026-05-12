# Annual (full-year) data for NBFC Dashboard — Year-on-Year tab
# Source: Screener.in AI summaries, investor presentations
# Metrics: AUM (₹ Cr), PAT (₹ Cr), ROA (%), ROE (%)
# Period: FY23 – FY26  (FY = April–March)
# Keys match CACHE_KEY values in nbfc_dashboard_v1.py

ANNUAL_YEARS = ["FY23", "FY24", "FY25", "FY26"]

NBFC_ANNUAL = {
    # ── Poonawalla Fincorp ─────────────────────────────────────────────────────
    # Source: Screener.in AI summary (usage/1696560)
    # FY25 PAT/ROA/ROE reflect one-time ₹666 Cr provision impact
    "Poonawalla Fincorp": {
        "aum_cr":  [16143, 25003, 35631, 60348],
        "pat_cr":  [585,   1027,  -98,   542  ],
        "roa_pct": [4.4,   5.24,  -0.35, 1.14 ],
        "roe_pct": [9.7,   13.4,  -1.2,  5.9  ],
    },
    # ── Bajaj Finance ─────────────────────────────────────────────────────────
    "Bajaj Finance": {
        "aum_cr":  [None, None, None, None],
        "pat_cr":  [None, None, None, None],
        "roa_pct": [None, None, None, None],
        "roe_pct": [None, None, None, None],
    },
    # ── Shriram Finance ───────────────────────────────────────────────────────
    # Source: Screener.in AI summary (usage/1696752)
    "Shriram Finance": {
        "aum_cr":  [185683, 232510, 263190, 302274],
        "pat_cr":  [6020,   7399,   9576,   10024 ],
        "roa_pct": [3.41,   3.22,   3.53,   3.26  ],
        "roe_pct": [17.30,  16.08,  18.16,  16.39 ],
    },
    # ── L&T Finance ───────────────────────────────────────────────────────────
    "L&T Finance": {
        "aum_cr":  [None, None, None, None],
        "pat_cr":  [None, None, None, None],
        "roa_pct": [None, None, None, None],
        "roe_pct": [None, None, None, None],
    },
    # ── Chola Finance ─────────────────────────────────────────────────────────
    "Chola Finance": {
        "aum_cr":  [None, None, None, None],
        "pat_cr":  [None, None, None, None],
        "roa_pct": [None, None, None, None],
        "roe_pct": [None, None, None, None],
    },
    # ── Aditya Birla Capital ──────────────────────────────────────────────────
    "Aditya Birla Capital": {
        "aum_cr":  [None, None, None, None],
        "pat_cr":  [None, None, None, None],
        "roa_pct": [None, None, None, None],
        "roe_pct": [None, None, None, None],
    },
    # ── Piramal Finance ───────────────────────────────────────────────────────
    "Piramal Finance": {
        "aum_cr":  [None, None, None, None],
        "pat_cr":  [None, None, None, None],
        "roa_pct": [None, None, None, None],
        "roe_pct": [None, None, None, None],
    },
    # ── Muthoot Finance ───────────────────────────────────────────────────────
    "Muthoot Finance": {
        "aum_cr":  [None, None, None, None],
        "pat_cr":  [None, None, None, None],
        "roa_pct": [None, None, None, None],
        "roe_pct": [None, None, None, None],
    },
    # ── Mahindra Finance ──────────────────────────────────────────────────────
    "Mahindra Finance": {
        "aum_cr":  [None, None, None, None],
        "pat_cr":  [None, None, None, None],
        "roa_pct": [None, None, None, None],
        "roe_pct": [None, None, None, None],
    },
}
