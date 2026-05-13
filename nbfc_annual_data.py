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
    # Source: Screener.in AI summary (usage/1697958); AUM from AB Capital press releases
    # AUM = total lending portfolio (NBFC + HFC), consistent with Bajaj Finance consolidated
    #   FY23: AB Capital FY23 PR (NBFC ₹80,556 + HFC ₹13,808 = ₹94,364 Cr)
    #   FY24: AB Capital Q4FY24 PR (NBFC+HFC combined = ₹1,24,059 Cr)
    #   FY25: AB Capital Q4FY25 PR (NBFC ₹1,26,351 + HFC ₹31,053 = ₹1,57,404 Cr)
    #   FY26: AB Capital Q4FY26 results (NBFC+HFC = ₹2,07,368 Cr)
    # FY23 PAT/ROA/ROE normalized (ex one-time ₹2,739 Cr health-ins. fair-value gain)
    # FY26 ROA/ROE: N/A (consolidated balance sheet data unavailable)
    "Aditya Birla Capital": {
        "aum_cr":  [94364,  124059, 157404, 207368],
        "pat_cr":  [2057,   3335,   3332,   3764  ],
        "roa_pct": [1.28,   1.62,   1.30,   None  ],
        "roe_pct": [11.5,   14.16,  11.65,  None  ],
    },
    # ── Piramal Finance ───────────────────────────────────────────────────────
    # Source: Screener.in AI summary (usage/1700511)
    # FY23: large loss from DHFL legacy clean-up / one-time provisions (~₹7,400 Cr)
    # FY23–FY25 ROA/ROE: not computable (PEL amalgamation restatements, missing opening B/S)
    # FY26: first year with reliable audited consolidated financials post-amalgamation
    "Piramal Finance": {
        "aum_cr":  [64000,  69000,  81000,  101230],
        "pat_cr":  [-7400,  383,    485,    1506  ],
        "roa_pct": [None,   None,   None,   1.47  ],
        "roe_pct": [None,   None,   None,   5.45  ],
    },
    # ── Muthoot Finance ───────────────────────────────────────────────────────
    # Source: Screener.in AI summary (usage/1697996); consolidated basis
    # FY26: full-year results not yet declared as of May 2026
    "Muthoot Finance": {
        "aum_cr":  [71502,  89079,  122000, None  ],
        "pat_cr":  [3670,   4468,   5352,   None  ],
        "roa_pct": [4.69,   5.06,   4.67,   None  ],
        "roe_pct": [18.15,  18.50,  19.62,  None  ],
    },
    # ── Mahindra Finance ──────────────────────────────────────────────────────
    # Source: Screener.in AI summary (usage/1697997); consolidated (includes MRHFL)
    # FY23/FY24 AUM interpolated (~); ROA/ROE derived from PAT / avg assets & equity
    "Mahindra Finance": {
        "aum_cr":  [90105,  110026, 119673, 139264],
        "pat_cr":  [2072,   1933,   2262,   2861  ],
        "roa_pct": [2.3,    1.7,    1.7,    1.9   ],
        "roe_pct": [12.1,   10.0,   10.9,   11.9  ],
    },
}
