# ─── SHAREHOLDING PATTERN DATA ─────────────────────────────────────────────────
# Source: Screener.in consolidated shareholding pattern
# Quarters: Q4FY24 → Q4FY26 + Apr'26  (10 periods, index 0 = oldest)
# Quarter mapping: Q4FY24=Mar-24, Q1FY25=Jun-24, Q2FY25=Sep-24, Q3FY25=Dec-24,
#                  Q4FY25=Mar-25, Q1FY26=Jun-25, Q2FY26=Sep-25, Q3FY26=Dec-25,
#                  Q4FY26=Mar-26, Apr'26=Apr-26 (separate — significant stake change)

SH_QUARTERS = [
    "Q4FY24", "Q1FY25", "Q2FY25", "Q3FY25",
    "Q4FY25", "Q1FY26", "Q2FY26", "Q3FY26",
    "Q4FY26", "Apr'26",
]

# Category colours (shared across all NBFCs)
CATEGORY_COLORS = {
    "Promoter": "#10b981",   # emerald
    "FII":      "#0284c7",   # sky blue
    "DII":      "#f97316",   # orange
    "Public":   "#94a3b8",   # slate
}

# Named-entity category badge colours (background)
ENTITY_CATEGORY_COLORS = {
    "Promoter":          "#10b981",
    "FII":               "#0284c7",
    "DII – MF":          "#fde68a",   # pastel honey amber
    "DII – Insurance":   "#fecdd3",   # pastel rose  (warm, not alarming)
    "DII – Pension":     "#8b5cf6",
    "DII – Other":       "#64748b",
}

# Override text colour for badges whose background is too light for white text
ENTITY_BADGE_TEXT_COLORS = {
    "DII – MF":        "#78350f",   # amber-900
    "DII – Insurance": "#9f1239",   # rose-900
}

SHAREHOLDING = {

    # ── SHRIRAM FINANCE ────────────────────────────────────────────────────────
    # NSE: SHRIRAMFIN · Source: Screener.in consolidated shareholding
    # Notable: MUFG Bank Limited acquired ~20% in April 2026 (open offer);
    # Promoter stake fell from 25.38% (Mar-26) to 20.30% (Apr-26).
    # Array positions: [Q4FY24, Q1FY25, Q2FY25, Q3FY25, Q4FY25, Q1FY26, Q2FY26, Q3FY26, Q4FY26, Apr'26]
    #                  [Mar-24, Jun-24, Sep-24, Dec-24, Mar-25, Jun-25, Sep-25, Dec-25, Mar-26, Apr-26]
    "Shriram Finance": {

        "category_pct": {
            "Promoter": [25.42, 25.41, 25.40, 25.40, 25.39, 25.39, 25.39, 25.38, 25.38, 20.30],
            "FII":      [53.90, 54.28, 53.29, 53.08, 53.58, 52.61, 49.61, 47.21, 45.15, 56.14],
            "DII":      [15.69, 15.24, 16.21, 15.93, 15.34, 16.32, 18.65, 21.29, 23.29, 18.62],
            "Public":   [ 5.00,  5.07,  5.07,  5.58,  5.68,  5.64,  6.34,  6.11,  6.18,  4.94],
        },

        # Named shareholders ≥1% at any point in Mar-24 → Apr-26.
        # None = below 1% disclosure threshold that quarter.
        "named_entities": [

            # ── Promoter Group ──────────────────────────────────────────────
            {
                "name":     "Shriram Capital Private Limited",
                "category": "Promoter",
                "pct": [17.87, 17.86, 17.86, 17.86, 17.85, 17.85, 17.85, 17.84, 17.84, 14.27],
            },
            {
                "name":     "Shriram Value Services Limited",
                "category": "Promoter",
                "pct": [ 5.53,  7.12,  7.11,  7.11,  7.11,  7.11,  7.11,  7.11,  7.11,  5.69],
            },

            # ── FII ─────────────────────────────────────────────────────────
            # MUFG Bank: new entry Apr-26 via open offer (formerly Sanlam held stake)
            {
                "name":     "MUFG Bank Limited",
                "category": "FII",
                "pct": [ None,  None,  None,  None,  None,  None,  None,  None,  None, 20.02],
            },
            {
                "name":     "Government of Singapore",
                "category": "FII",
                "pct": [ 6.10,  6.67,  6.40,  6.11,  5.67,  5.41,  4.73,  4.66,  4.47,  3.58],
            },
            {
                "name":     "Govt Pension Fund Global (Norges Bank)",
                "category": "FII",
                "pct": [ 1.69,  1.33,  1.19,  1.13,  None,  1.31,  1.41,  1.29,  1.50,  1.20],
            },
            {
                "name":     "New World Fund Inc",
                "category": "FII",
                "pct": [ 1.47,  1.47,  1.83,  1.52,  1.63,  1.21,  None,  None,  1.11,  None],
            },
            {
                "name":     "Kotak Funds – India Midcap Fund",
                "category": "FII",
                "pct": [ 1.18,  1.22,  1.20,  1.16,  1.13,  None,  None,  None,  None,  None],
            },
            {
                "name":     "Monetary Authority of Singapore (A/c 1)",
                "category": "FII",
                "pct": [ 1.26,  1.29,  1.30,  None,  None,  None,  None,  None,  None,  None],
            },
            {
                "name":     "Monetary Authority of Singapore (A/c 2)",
                "category": "FII",
                "pct": [ 1.03,  None,  None,  None,  None,  1.24,  1.20,  1.03,  None,  None],
            },
            {
                "name":     "Vanguard Intl Stock Index Fund",
                "category": "FII",
                "pct": [ 1.02,  1.03,  1.04,  None,  None,  None,  None,  None,  None,  None],
            },
            {
                "name":     "Vanguard Total Intl Stock Index Fund",
                "category": "FII",
                "pct": [ None,  None,  None,  None,  None,  None,  None,  None,  None,  1.09],
            },
            {
                "name":     "Vanguard Emerging Markets Index Fund",
                "category": "FII",
                "pct": [ None,  None,  None,  None,  None,  None,  None,  None,  None,  1.03],
            },

            # ── DII – Mutual Funds ──────────────────────────────────────────
            {
                "name":     "Aditya Birla Sun Life Trustee",
                "category": "DII – MF",
                "pct": [ 1.44,  1.53,  1.49,  1.42,  1.15,  None,  None,  None,  None,  None],
            },
            {
                "name":     "Kotak Equity Hybrid Fund",
                "category": "DII – MF",
                "pct": [ 1.54,  1.67,  None,  None,  None,  None,  None,  None,  None,  None],
            },
            {
                "name":     "SBI Nifty 50 ETF",
                "category": "DII – MF",
                "pct": [ None,  1.45,  1.46,  1.72,  None,  None,  None,  None,  None,  None],
            },
            {
                "name":     "SBI Mutual Fund",
                "category": "DII – MF",
                "pct": [ None,  None,  None,  1.58,  1.61,  1.85,  2.33,  2.05,  None,  1.64],
            },
            {
                "name":     "Kotak Mutual Fund",
                "category": "DII – MF",
                "pct": [ None,  None,  None,  None,  1.18,  1.48,  2.09,  1.94,  2.32,  1.85],
            },
            {
                "name":     "Motilal Oswal Mutual Fund",
                "category": "DII – MF",
                "pct": [ None,  None,  None,  None,  None,  None,  None,  None,  1.51,  1.21],
            },
            {
                "name":     "UTI Mutual Fund",
                "category": "DII – MF",
                "pct": [ None,  None,  None,  None,  None,  None,  None,  None,  1.21,  None],
            },
            {
                "name":     "UTI Mid Cap Fund",
                "category": "DII – MF",
                "pct": [ None,  None,  None,  None,  None,  None,  None,  1.11,  None,  None],
            },

            # ── DII – Insurance ─────────────────────────────────────────────
            {
                "name":     "LIC of India",
                "category": "DII – Insurance",
                "pct": [ None,  None,  None,  None,  None,  None,  1.29,  None,  None,  None],
            },
            {
                "name":     "SBI Life Insurance Co. Ltd",
                "category": "DII – Insurance",
                "pct": [ None,  None,  None,  None,  None,  None,  None,  1.01,  None,  None],
            },

            # ── DII – Pension / NPS ─────────────────────────────────────────
            {
                "name":     "NPS Trust",
                "category": "DII – Pension",
                "pct": [ 1.11,  1.19,  1.36,  1.67,  1.81,  1.91,  2.18,  2.29,  1.83,  None],
            },
        ],
    },

    # ── POONAWALLA FINCORP ─────────────────────────────────────────────────────
    # NSE: POONAWALLA · Source: Screener.in consolidated shareholding
    # "Others" (warrants/ESOPs 0.52–0.66%) excluded — Screener shows separately.
    # Array positions: [Q4FY24, Q1FY25, Q2FY25, Q3FY25, Q4FY25, Q1FY26, Q2FY26, Q3FY26, Q4FY26, Apr'26]
    #                  [Mar-24, Jun-24, Sep-24, Dec-24, Mar-25, Jun-25, Sep-25, Dec-25, Mar-26, Apr-26]
    "Poonawalla Fincorp": {

        "category_pct": {
            "Promoter": [62.13,  62.09,  61.87,  62.36,  62.53,  62.46,  63.96,  63.95,  63.93,  59.03],
            "FII":      [ 7.76,   7.85,   7.72,   8.19,   9.99,  10.76,  10.56,  10.61,  10.21,  11.25],
            "DII":      [ 5.81,   6.77,   9.63,  11.82,  11.12,  12.26,  12.28,  12.22,  12.14,  16.67],
            "Public":   [23.79,  22.64,  20.12,  16.98,  15.71,  13.86,  12.58,  12.62,  13.15,  12.49],
        },

        "named_entities": [

            # ── Promoter Group ──────────────────────────────────────────────────
            {
                "name":     "Rising Sun Holdings Pvt Ltd",
                "category": "Promoter",
                "pct": [62.13,  62.09,  61.87,  62.36,  62.53,  62.46,  63.96,  63.95,  63.93,  59.03],
            },

            # ── FII ─────────────────────────────────────────────────────────────
            {
                "name":     "Amansa Holdings Private Limited",
                "category": "FII",
                "pct": [ 2.20,   2.05,   2.07,   1.95,   1.95,   1.92,   1.75,   1.51,   1.51,   1.29],
            },
            {
                "name":     "Franklin Templeton – Franklin India Fund",
                "category": "FII",
                "pct": [ None,   None,   None,   None,   None,   1.19,   1.14,   1.14,   1.14,   1.05],
            },
            {
                "name":     "Bank Muscat India Fund",
                "category": "FII",
                "pct": [ 1.13,   1.13,   1.13,   1.13,   1.13,   1.12,   1.08,   1.08,   1.08,   None],
            },

            # ── DII – Mutual Funds ──────────────────────────────────────────────
            # Kotak shifted from Multicap → Midcap Fund between Q3FY26 and Q4FY26
            {
                "name":     "Kotak Midcap Fund",
                "category": "DII – MF",
                "pct": [ None,   None,   None,   None,   None,   None,   None,   None,   4.91,   6.40],
            },
            {
                "name":     "Kotak Multicap Fund",
                "category": "DII – MF",
                "pct": [ None,   None,   None,   2.43,   2.81,   3.34,   4.24,   4.17,   None,   None],
            },
            {
                "name":     "Quant Mutual Fund – Quant Mid Cap Fund",
                "category": "DII – MF",
                "pct": [ 1.91,   1.91,   1.90,   1.90,   None,   None,   None,   None,   None,   None],
            },
            {
                "name":     "Bandhan Value Fund",
                "category": "DII – MF",
                "pct": [ None,   None,   None,   None,   None,   1.05,   1.13,   1.23,   1.40,   1.70],
            },
            {
                "name":     "Bandhan Sterling Value Fund",
                "category": "DII – MF",
                "pct": [ None,   None,   1.06,   None,   1.02,   None,   None,   None,   None,   None],
            },
            {
                "name":     "Nippon Life India Trustee – Nippon India Small Cap",
                "category": "DII – MF",
                "pct": [ None,   None,   None,   None,   None,   None,   None,   None,   None,   1.07],
            },

            # ── DII – Insurance ─────────────────────────────────────────────────
            {
                "name":     "Life Insurance Corporation Of India",
                "category": "DII – Insurance",
                "pct": [ None,   1.47,   1.80,   1.97,   2.93,   3.21,   3.08,   3.07,   2.92,   2.70],
            },
            {
                "name":     "SBI Life Insurance Co. Ltd",
                "category": "DII – Insurance",
                "pct": [ None,   None,   2.66,   2.66,   2.44,   2.53,   1.80,   1.56,   None,   None],
            },

            # ── Public ──────────────────────────────────────────────────────────
            # Mayank Poddar holds via two separate demat accounts; shown separately.
            {
                "name":     "Mayank Poddar (A/c 1)",
                "category": "Public",
                "pct": [ 1.11,   1.11,   1.11,   1.11,   1.11,   1.11,   1.06,   1.06,   None,   None],
            },
            {
                "name":     "Mayank Poddar (A/c 2)",
                "category": "Public",
                "pct": [ 1.01,   1.01,   1.01,   1.01,   1.01,   1.01,   None,   None,   None,   None],
            },
        ],
    },

    # ── BAJAJ FINANCE ──────────────────────────────────────────────────────────
    # NSE: BAJFINANCE · Source: Screener.in consolidated shareholding
    # Screener shows through Q4FY26 (Mar-26); no Apr'26 data available yet.
    # Government (~0.07–0.09%) and Others (~0.05–0.16%) shown as separate categories on Screener;
    # not merged into DII/Public here (prior data had them merged — values corrected).
    # Array positions: [Q4FY24, Q1FY25, Q2FY25, Q3FY25, Q4FY25, Q1FY26, Q2FY26, Q3FY26, Q4FY26, Apr'26]
    #                  [Mar-24, Jun-24, Sep-24, Dec-24, Mar-25, Jun-25, Sep-25, Dec-25, Mar-26, None  ]
    "Bajaj Finance": {

        "category_pct": {
            "Promoter": [54.69,  54.70,  54.70,  54.70,  54.73,  54.73,  54.67,  54.70,  54.71,  54.71],
            "FII":      [20.55,  21.08,  20.81,  20.79,  21.45,  21.71,  21.97,  21.49,  21.33,  21.33],
            "DII":      [14.33,  14.23,  15.01,  15.08,  14.78,  14.52,  14.39,  14.86,  15.10,  15.10],
            "Public":   [10.19,   9.83,   9.36,   9.32,   8.84,   8.92,   8.78,   8.77,   8.73,   8.73],
        },

        "named_entities": [

            # ── Promoter Group ──────────────────────────────────────────────────
            {
                "name":     "Bajaj Finserv Limited",
                "category": "Promoter",
                "pct": [51.34,  51.34,  51.34,  51.34,  51.39,  51.39,  51.32,  51.32,  51.32,  51.32],
            },
            {
                "name":     "Maharashtra Scooters Limited",
                "category": "Promoter",
                "pct": [ 3.07,   3.07,   3.07,   3.07,   3.05,   3.05,   3.05,   3.05,   3.06,   3.06],
            },

            # ── FII ─────────────────────────────────────────────────────────────
            # Screener shows two sub-accounts: "E" only appeared in Dec-23 (outside range).
            # "E - 2" is the active account for our full range.
            {
                "name":     "Government of Singapore",
                "category": "FII",
                "pct": [ 3.36,   3.41,   3.31,   3.08,   3.03,   2.55,   2.42,   2.50,   2.16,   2.16],
            },

            # ── DII – Mutual Funds ──────────────────────────────────────────────
            {
                "name":     "SBI Mutual Fund",
                "category": "DII – MF",
                "pct": [ 3.21,   3.06,   2.76,   2.61,   2.53,   2.37,   2.04,   1.98,   2.31,   2.31],
            },
            {
                "name":     "Axis Mutual Fund",
                "category": "DII – MF",
                "pct": [ 2.00,   1.64,   1.40,   1.32,   1.04,   1.07,   1.08,   1.05,   None,   None],
            },
            {
                "name":     "UTI Mutual Fund",
                "category": "DII – MF",
                "pct": [ 1.03,   1.05,   1.05,   1.06,   1.03,   None,   1.13,   1.14,   1.13,   1.13],
            },

            # ── DII – Insurance ─────────────────────────────────────────────────
            {
                "name":     "Life Insurance Corporation Of India",
                "category": "DII – Insurance",
                "pct": [ 1.51,   1.93,   2.49,   2.84,   2.77,   2.62,   2.35,   2.38,   2.75,   2.75],
            },

            # ── DII – Pension / NPS ─────────────────────────────────────────────
            {
                "name":     "NPS Trust",
                "category": "DII – Pension",
                "pct": [ None,   None,   None,   None,   None,   None,   None,   1.07,   1.37,   1.37],
            },
        ],
    },

    # ── CHOLAMANDALAM FINANCE ───────────────────────────────────────────────────
    # BSE code 511243 · NSE: CHOLAFIN · Murugappa Group NBFC
    # Source: NSE corporate-share-holdings API (fetched Feb 2026)
    "Cholamandalam Finance": {

        "category_pct": {
            #                Q4FY24  Q1FY25  Q2FY25  Q3FY25  Q4FY25  Q1FY26  Q2FY26  Q3FY26
            "Promoter": [50.35,  50.33,  50.24,  49.93,  49.92,  49.90,  49.88,  49.72,   None,   None],
            "FII":      [26.00,  26.62,  27.18,  27.43,  28.23,  27.96,  26.85,  26.55,   None,   None],
            "DII":      [17.04,  16.86,  16.58,  16.10,  15.49,  16.06,  17.27,  17.55,   None,   None],
            "Public":   [ 6.61,   6.19,   6.01,   6.54,   6.36,   6.08,   6.00,   6.17,   None,   None],
        },

        # Named shareholders ≥1% at any point across the 8 quarters.
        # None = below 1% threshold / not separately disclosed that quarter.
        "named_entities": [

            # ── Promoter Group ──────────────────────────────────────────────────
            {
                "name":     "Cholamandalam Financial Holdings Ltd",
                "category": "Promoter",
                #             Q4FY24  Q1FY25  Q2FY25  Q3FY25  Q4FY25  Q1FY26  Q2FY26  Q3FY26
                "pct": [44.39,  44.38,  44.37,  44.35,  44.34,  44.33,  44.32,  44.18,   None,   None],
            },
            {
                "name":     "Ambadi Investments Limited",
                "category": "Promoter",
                "pct": [ 4.01,   4.01,   4.01,   4.01,   4.01,   4.01,   4.01,   4.00,   None,   None],
            },

            # ── FII ─────────────────────────────────────────────────────────────
            {
                "name":     "New World Fund Inc (Capital Group)",
                "category": "FII",
                "pct": [ 1.71,   1.90,   1.94,   2.02,   1.86,   1.72,   1.72,   1.71,   None,   None],
            },
            {
                "name":     "Smallcap World Fund, Inc (Capital Group)",
                "category": "FII",
                "pct": [ 1.44,   1.38,   1.38,   1.34,   1.31,   1.29,   1.29,   1.07,   None,   None],
            },
            {
                "name":     "Government Pension Fund Global (Norges)",
                "category": "FII",
                "pct": [ 1.19,   1.24,   1.07,   1.63,   1.39,   1.09,   1.12,   1.06,   None,   None],
            },
            {
                "name":     "EuroPacific Growth Fund (Capital Group)",
                "category": "FII",
                "pct": [ 1.01,   1.15,   1.15,   None,   None,   None,   None,   None,   None,   None],
            },

            # ── DII – Mutual Funds ──────────────────────────────────────────────
            {
                "name":     "Axis Mutual Fund",
                "category": "DII – MF",
                "pct": [ 3.98,   3.86,   3.43,   2.57,   2.39,   2.23,   2.04,   1.93,   None,   None],
            },
            {
                "name":     "SBI Mutual Fund",
                "category": "DII – MF",
                "pct": [ 1.57,   2.02,   1.82,   1.54,   1.62,   1.50,   1.39,   1.22,   None,   None],
            },
            {
                "name":     "HDFC Mutual Fund",
                "category": "DII – MF",
                "pct": [ 1.23,   1.21,   1.22,   1.33,   1.25,   1.12,   None,   None,   None,   None],
            },
            {
                "name":     "Aditya Birla Sun Life Mutual Fund",
                "category": "DII – MF",
                "pct": [ 1.15,   1.09,   1.00,   1.03,   1.02,   None,   None,   None,   None,   None],
            },
            {
                "name":     "Canara Robeco Mutual Fund",
                "category": "DII – MF",
                "pct": [ None,   1.08,   1.24,   1.13,   None,   None,   None,   None,   None,   None],
            },
            {
                "name":     "Invesco India Mutual Fund",
                "category": "DII – MF",
                "pct": [ None,   None,   None,   None,   None,   1.01,   1.20,   1.21,   None,   None],
            },
            {
                "name":     "Motilal Oswal Mutual Fund",
                "category": "DII – MF",
                "pct": [ None,   None,   None,   None,   None,   1.14,   1.15,   1.08,   None,   None],
            },
            {
                "name":     "Kotak Mahindra Mutual Fund",
                "category": "DII – MF",
                "pct": [ None,   None,   None,   None,   None,   None,   None,   1.16,   None,   None],
            },

            # ── DII – Pension / NPS ─────────────────────────────────────────────
            {
                "name":     "NPS Trust (SBI Pension Fund)",
                "category": "DII – Pension",
                "pct": [ None,   None,   None,   None,   None,   1.31,   1.31,   2.56,   None,   None],
            },
        ],
    },

    # ── L&T FINANCE ────────────────────────────────────────────────────────────
    # BSE code 533519 · NSE: LTF · L&T Group NBFC
    # Source: NSE corporate-share-holdings API (fetched Feb 2026)
    "L&T Finance": {

        "category_pct": {
            #                Q4FY24  Q1FY25  Q2FY25  Q3FY25  Q4FY25  Q1FY26  Q2FY26  Q3FY26
            "Promoter": [65.86,  66.37,  66.29,  66.25,  66.24,  66.16,  66.10,  66.03,   None,   None],
            "FII":      [11.05,   7.33,   6.73,   5.30,   5.48,   6.19,   6.41,   6.66,   None,   None],
            "DII":      [ 8.70,  11.64,  12.33,  12.17,  13.29,  14.11,  14.32,  15.33,   None,   None],
            "Public":   [14.40,  14.65,  14.65,  16.27,  15.00,  13.54,  13.17,  11.98,   None,   None],
        },

        "named_entities": [

            # ── Promoter Group ──────────────────────────────────────────────────
            {
                "name":     "Larsen and Toubro Limited",
                "category": "Promoter",
                #             Q4FY24  Q1FY25  Q2FY25  Q3FY25  Q4FY25  Q1FY26  Q2FY26  Q3FY26
                "pct": [65.86,  66.37,  66.29,  66.25,  66.24,  66.16,  66.10,  66.03,   None,   None],
            },

            # ── FII ─────────────────────────────────────────────────────────────
            # BNP Paribas held via ODI (Offshore Derivative Instrument);
            # exited after Q4FY24 — coincided with broader FII unwind from ~11% to ~7%.
            {
                "name":     "BNP Paribas Financial Markets (ODI)",
                "category": "FII",
                "pct": [ 2.43,   None,   None,   None,   None,   None,   None,   None,   None,   None],
            },

            # ── DII – Mutual Funds ──────────────────────────────────────────────
            {
                "name":     "Mirae Asset Large & Midcap Fund",
                "category": "DII – MF",
                "pct": [ None,   1.74,   2.57,   2.88,   3.46,   3.47,   2.88,   1.80,   None,   None],
            },
            {
                "name":     "Invesco India Mutual Fund",
                "category": "DII – MF",
                "pct": [ None,   1.23,   1.07,   1.17,   1.29,   1.65,   1.72,   1.75,   None,   None],
            },
            {
                "name":     "Kotak Midcap Fund",
                "category": "DII – MF",
                "pct": [ None,   None,   None,   None,   None,   None,   1.31,   1.80,   None,   None],
            },
            {
                "name":     "Axis Mutual Fund",
                "category": "DII – MF",
                "pct": [ None,   None,   None,   None,   None,   None,   1.10,   1.29,   None,   None],
            },
            {
                "name":     "Motilal Oswal Mutual Fund",
                "category": "DII – MF",
                "pct": [ None,   None,   None,   None,   None,   None,   None,   1.63,   None,   None],
            },

            # ── DII – Insurance ─────────────────────────────────────────────────
            {
                "name":     "Life Insurance Corporation Of India",
                "category": "DII – Insurance",
                "pct": [ 1.94,   1.94,   1.94,   2.07,   2.28,   1.70,   None,   None,   None,   None],
            },
            {
                "name":     "ICICI Prudential Life Insurance",
                "category": "DII – Insurance",
                "pct": [ 1.51,   1.50,   1.46,   1.44,   1.44,   1.47,   None,   1.17,   None,   None],
            },
            {
                "name":     "Tata AIA Life Insurance",
                "category": "DII – Insurance",
                "pct": [ None,   None,   None,   1.46,   1.54,   1.58,   None,   None,   None,   None],
            },
        ],
    },
}
