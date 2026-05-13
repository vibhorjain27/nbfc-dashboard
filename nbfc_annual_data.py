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
    # Source: Screener.in AI summary (usage/1697821)
    # ROA/ROE = core (before one-time items); FY23/FY24 AUM interpolated (~)
    "Bajaj Finance": {
        "aum_cr":  [247400, 330600, 416661, 509975],
        "pat_cr":  [11508,  14451,  16779,  19332 ],
        "roa_pct": [5.3,    5.1,    4.5,    4.6   ],
        "roe_pct": [23.5,   22.1,   19.1,   19.2  ],
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
    # Source: Screener.in AI summary (usage/1697879)
    "L&T Finance": {
        "aum_cr":  [80893,  81359,  97762,  121728],
        "pat_cr":  [1623,   2320,   2644,   2981  ],
        "roa_pct": [1.52,   2.32,   2.44,   2.37  ],
        "roe_pct": [7.83,   10.35,  10.87,  11.25 ],
    },
    # ── Chola Finance ─────────────────────────────────────────────────────────
    # Source: Screener.in AI summary (usage/1697950)
    # AUM = Business AUM from corporate presentations; ROA/ROE company-disclosed
    "Chola Finance": {
        "aum_cr":  [112782, 153718, 199876, 242630],
        "pat_cr":  [2666,   3423,   4259,   5220  ],
        "roa_pct": [2.8,    2.6,    2.4,    2.5   ],
        "roe_pct": [20.6,   20.6,   19.8,   19.7  ],
    },
    # ── Aditya Birla Capital ──────────────────────────────────────────────────
    # Source: Screener.in AI summary (usage/1697958); AUM from press releases / quarterly cache
    # AUM = NBFC lending book only (Aditya Birla Finance / ABFL), excluding HFC and AMC
    #   FY23: AB Capital FY23 results press release (Mar 2023)
    #   FY24–FY26: quarterly cache Q4 values (105,639 / 126,351 / 159,916)
    # FY23 PAT/ROA/ROE normalized (ex one-time ₹2,739 Cr health-ins. fair-value gain)
    # FY26 ROA/ROE: N/A (consolidated balance sheet data unavailable)
    "Aditya Birla Capital": {
        "aum_cr":  [80556,  105639, 126351, 159916],
        "pat_cr":  [2057,   3335,   3332,   3764  ],
        "roa_pct": [1.28,   1.62,   1.30,   None  ],
        "roe_pct": [11.5,   14.16,  11.65,  None  ],
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
