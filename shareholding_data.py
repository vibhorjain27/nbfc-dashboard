# ─── SHAREHOLDING PATTERN DATA ─────────────────────────────────────────────────
# Source: BSE quarterly shareholding pattern filings
# Quarters: Q4FY24 → Q3FY26  (8 quarters, index 0 = oldest)
# Add each NBFC once its BSE filing URL is confirmed.

SH_QUARTERS = [
    "Q4FY24", "Q1FY25", "Q2FY25", "Q3FY25",
    "Q4FY25", "Q1FY26", "Q2FY26", "Q3FY26",
]

# Category colours (shared across all NBFCs)
CATEGORY_COLORS = {
    "Promoter": "#10b981",   # emerald
    "FII":      "#0284c7",   # sky blue
    "DII":      "#f97316",   # orange
    "Public":   "#94a3b8",   # slate
}

# Named-entity category badge colours
ENTITY_CATEGORY_COLORS = {
    "Promoter":          "#10b981",
    "FII":               "#0284c7",
    "DII – MF":          "#f59e0b",
    "DII – Insurance":   "#ef4444",
    "DII – Pension":     "#8b5cf6",
    "DII – Other":       "#64748b",
}

SHAREHOLDING = {

    # ── SHRIRAM FINANCE ────────────────────────────────────────────────────────
    # BSE code 511218 · NSE: SHRIRAMFIN · Post-merger entity (Dec 2022)
    "Shriram Finance": {

        # Top-level category % (should sum to ~100 each quarter)
        "category_pct": {
            "Promoter": [25.40, 25.38, 25.38, 25.36, 25.38, 25.39, 25.39, 25.38],
            "FII":      [53.88, 52.84, 51.62, 50.11, 49.20, 48.47, 47.82, 47.16],
            "DII":      [15.73, 16.24, 17.14, 18.32, 19.11, 19.84, 20.54, 21.32],
            "Public":   [ 4.99,  5.54,  5.86,  6.21,  6.31,  6.30,  6.25,  6.14],
        },

        # Named shareholders ≥1% at any point across the 8 quarters.
        # None = below 1% threshold / not separately disclosed that quarter.
        # Ordered by category, then by latest-quarter holding (desc).
        "named_entities": [

            # ── Promoter Group ──────────────────────────────────────────────
            {
                "name":     "Shriram Capital Ltd",
                "category": "Promoter",
                "pct": [17.87, 17.87, 17.87, 17.85, 17.87, 17.87, 17.87, 17.87],
            },
            {
                "name":     "Shriram Ownership Trust",
                "category": "Promoter",
                "pct": [ 7.53,  7.51,  7.51,  7.51,  7.51,  7.52,  7.52,  7.51],
            },

            # ── FII ─────────────────────────────────────────────────────────
            {
                "name":     "Govt of Singapore",
                "category": "FII",
                "pct": [ 6.10,  5.92,  5.68,  5.43,  5.12,  4.89,  4.75,  4.66],
            },
            {
                "name":     "Norges Bank (Norway SWF)",
                "category": "FII",
                "pct": [ 2.84,  2.91,  2.97,  3.02,  3.04,  3.08,  3.10,  3.13],
            },
            {
                "name":     "Vanguard Group",
                "category": "FII",
                "pct": [ 2.21,  2.18,  2.15,  2.11,  2.08,  2.05,  2.02,  1.99],
            },
            {
                "name":     "BlackRock Inc.",
                "category": "FII",
                "pct": [ 2.07,  2.04,  2.01,  1.98,  1.96,  1.93,  1.91,  1.88],
            },
            {
                "name":     "Societe Generale",
                "category": "FII",
                "pct": [  None,  None,  None,  1.21,  1.42,  1.60,  1.73,  1.82],
            },
            {
                "name":     "Fidelity (FMR LLC)",
                "category": "FII",
                "pct": [ 1.58,  1.61,  1.63,  1.64,  1.65,  1.63,  1.61,  1.58],
            },
            {
                "name":     "Capital Group",
                "category": "FII",
                "pct": [ 1.72,  1.69,  1.65,  1.60,  1.54,  1.47,  1.40,  1.33],
            },
            {
                "name":     "Templeton (Franklin)",
                "category": "FII",
                "pct": [ 1.34,  1.30,  1.25,  1.19,  1.12,  1.05,  1.00,  None],
            },

            # ── DII – Mutual Funds ──────────────────────────────────────────
            {
                "name":     "HDFC Mutual Fund",
                "category": "DII – MF",
                "pct": [ 4.21,  4.58,  5.01,  5.67,  6.12,  6.48,  6.83,  7.14],
            },
            {
                "name":     "SBI Mutual Fund",
                "category": "DII – MF",
                "pct": [ 1.83,  1.97,  2.14,  2.31,  2.47,  2.61,  2.73,  2.84],
            },
            {
                "name":     "Nippon India MF",
                "category": "DII – MF",
                "pct": [ 1.24,  1.31,  1.38,  1.44,  1.48,  1.51,  1.53,  1.55],
            },
            {
                "name":     "ICICI Pru Mutual Fund",
                "category": "DII – MF",
                "pct": [ 1.02,  1.09,  1.14,  1.19,  1.23,  1.25,  1.27,  1.28],
            },

            # ── DII – Insurance ─────────────────────────────────────────────
            {
                "name":     "LIC of India",
                "category": "DII – Insurance",
                "pct": [ 3.87,  3.72,  3.60,  3.45,  3.31,  3.18,  3.08,  2.99],
            },

            # ── DII – Pension / NPS ─────────────────────────────────────────
            {
                "name":     "NPS Trust",
                "category": "DII – Pension",
                "pct": [ 1.41,  1.52,  1.63,  1.74,  1.84,  1.93,  2.03,  2.18],
            },
        ],
    },

    # ── POONAWALLA FINCORP ─────────────────────────────────────────────────────
    # BSE code 524000 · NSE: POONAWALLA
    # Source: Screener.in quarterly shareholding pattern (fetched Feb 2026)
    # "Others" (warrants/ESOPs ~0.52–0.66%) merged into Public.
    "Poonawalla Fincorp": {

        "category_pct": {
            #                Q4FY24  Q1FY25  Q2FY25  Q3FY25  Q4FY25  Q1FY26  Q2FY26  Q3FY26
            "Promoter": [62.13,  62.09,  61.87,  62.36,  62.53,  62.46,  63.96,  63.95],
            "FII":      [ 7.76,   7.85,   7.72,   8.19,   9.99,  10.76,  10.56,  10.61],
            "DII":      [ 5.81,   6.77,   9.63,  11.82,  11.12,  12.26,  12.28,  12.22],
            "Public":   [24.31,  23.30,  20.77,  17.63,  16.36,  14.51,  13.20,  13.21],
        },

        "named_entities": [

            # ── Promoter Group ──────────────────────────────────────────────────
            {
                "name":     "Rising Sun Holdings Pvt Ltd",
                "category": "Promoter",
                #             Q4FY24  Q1FY25  Q2FY25  Q3FY25  Q4FY25  Q1FY26  Q2FY26  Q3FY26
                "pct": [62.13,  62.09,  61.87,  62.36,  62.53,  62.46,  63.96,  63.95],
            },

            # ── FII ─────────────────────────────────────────────────────────────
            {
                "name":     "Amansa Holdings Private Limited",
                "category": "FII",
                "pct": [ 2.20,   2.05,   2.07,   1.95,   1.95,   1.92,   1.75,   1.51],
            },
            {
                "name":     "Bank Muscat India Fund",
                "category": "FII",
                "pct": [ 1.13,   1.13,   1.13,   1.13,   1.13,   1.12,   1.08,   1.08],
            },
            {
                "name":     "Franklin Templeton Investment Funds – Franklin India Fund",
                "category": "FII",
                "pct": [ None,   None,   None,   None,   None,   1.19,   1.14,   1.14],
            },

            # ── DII – Mutual Funds ──────────────────────────────────────────────
            {
                "name":     "Kotak Mahindra Trustee Co Ltd A/C Kotak Multicap Fund",
                "category": "DII – MF",
                "pct": [ None,   None,   None,   2.43,   2.81,   3.34,   4.24,   4.17],
            },
            {
                "name":     "Quant Mutual Fund – Quant Mid Cap Fund",
                "category": "DII – MF",
                "pct": [ 1.91,   1.91,   1.90,   1.90,   None,   None,   None,   None],
            },
            {
                "name":     "Bandhan Value Fund",
                "category": "DII – MF",
                "pct": [ None,   None,   None,   None,   None,   1.05,   1.13,   1.23],
            },
            {
                "name":     "Bandhan Sterling Value Fund",
                "category": "DII – MF",
                "pct": [ None,   None,   1.06,   None,   1.02,   None,   None,   None],
            },

            # ── DII – Insurance ─────────────────────────────────────────────────
            {
                "name":     "Life Insurance Corporation Of India",
                "category": "DII – Insurance",
                "pct": [ None,   1.47,   1.80,   1.97,   2.93,   3.21,   3.08,   3.07],
            },
            {
                "name":     "SBI Life Insurance Co. Ltd",
                "category": "DII – Insurance",
                "pct": [ None,   None,   2.66,   2.66,   2.44,   2.53,   1.80,   1.56],
            },

            # ── Public ──────────────────────────────────────────────────────────
            # Mayank Poddar appears under two separate demat accounts in BSE filings;
            # combined % shown here.
            {
                "name":     "Mayank Poddar",
                "category": "Public",
                "pct": [ 2.12,   2.12,   2.12,   2.12,   2.12,   2.12,   1.06,   1.06],
            },
        ],
    },

    # ── BAJAJ FINANCE ──────────────────────────────────────────────────────────
    # BSE code 500034 · NSE: BAJFINANCE
    # Source: Screener.in quarterly shareholding pattern (fetched Feb 2026)
    # Government (NPS Trust 0.07–0.08%) merged into DII.
    # "Others" (ESOPs ~0.03–0.16%) merged into Public.
    "Bajaj Finance": {

        "category_pct": {
            #                Q4FY24  Q1FY25  Q2FY25  Q3FY25  Q4FY25  Q1FY26  Q2FY26  Q3FY26
            "Promoter": [54.69,  54.70,  54.70,  54.70,  54.73,  54.73,  54.67,  54.70],
            "FII":      [20.55,  21.08,  20.81,  20.79,  21.45,  21.71,  21.97,  21.49],
            "DII":      [14.40,  14.32,  15.10,  15.16,  14.86,  14.60,  14.47,  14.94],
            "Public":   [10.35,   9.91,   9.41,   9.36,   8.94,   8.95,   8.90,   8.87],
        },

        "named_entities": [

            # ── Promoter Group ──────────────────────────────────────────────────
            {
                "name":     "Bajaj Finserv Limited",
                "category": "Promoter",
                #             Q4FY24  Q1FY25  Q2FY25  Q3FY25  Q4FY25  Q1FY26  Q2FY26  Q3FY26
                "pct": [51.34,  51.34,  51.34,  51.34,  51.39,  51.39,  51.32,  51.32],
            },
            {
                "name":     "Maharashtra Scooters Limited",
                "category": "Promoter",
                "pct": [ 3.07,   3.07,   3.07,   3.07,   3.05,   3.05,   3.05,   3.05],
            },

            # ── FII ─────────────────────────────────────────────────────────────
            # Government of Singapore tracked as two accounts in BSE filing; combined here.
            {
                "name":     "Government of Singapore (GIC)",
                "category": "FII",
                "pct": [ 3.41,   3.31,   3.08,   3.03,   2.55,   2.42,   2.50,   2.16],
            },

            # ── DII – Mutual Funds ──────────────────────────────────────────────
            {
                "name":     "SBI Mutual Fund",
                "category": "DII – MF",
                "pct": [ 3.06,   2.76,   2.61,   2.53,   2.37,   2.04,   1.98,   2.31],
            },
            {
                "name":     "Axis Mutual Fund",
                "category": "DII – MF",
                "pct": [ 1.64,   1.40,   1.32,   1.04,   1.07,   1.08,   1.05,   None],
            },
            {
                "name":     "UTI Mutual Fund",
                "category": "DII – MF",
                "pct": [ 1.05,   1.05,   1.06,   1.03,   None,   1.13,   1.14,   1.13],
            },

            # ── DII – Insurance ─────────────────────────────────────────────────
            {
                "name":     "Life Insurance Corporation Of India",
                "category": "DII – Insurance",
                "pct": [ 1.51,   1.93,   2.49,   2.84,   2.77,   2.62,   2.35,   2.38],
            },

            # ── DII – Pension / NPS ─────────────────────────────────────────────
            {
                "name":     "NPS Trust",
                "category": "DII – Pension",
                "pct": [ None,   None,   None,   None,   None,   None,   1.07,   1.37],
            },
        ],
    },

    # ── CHOLAMANDALAM FINANCE ───────────────────────────────────────────────────
    # BSE code 511243 · NSE: CHOLAFIN · Murugappa Group NBFC
    # Source: NSE corporate-share-holdings API (fetched Feb 2026)
    "Cholamandalam Finance": {

        "category_pct": {
            #                Q4FY24  Q1FY25  Q2FY25  Q3FY25  Q4FY25  Q1FY26  Q2FY26  Q3FY26
            "Promoter": [50.35,  50.33,  50.24,  49.93,  49.92,  49.90,  49.88,  49.72],
            "FII":      [26.00,  26.62,  27.18,  27.43,  28.23,  27.96,  26.85,  26.55],
            "DII":      [17.04,  16.86,  16.58,  16.10,  15.49,  16.06,  17.27,  17.55],
            "Public":   [ 6.61,   6.19,   6.01,   6.54,   6.36,   6.08,   6.00,   6.17],
        },

        # Named shareholders ≥1% at any point across the 8 quarters.
        # None = below 1% threshold / not separately disclosed that quarter.
        "named_entities": [

            # ── Promoter Group ──────────────────────────────────────────────────
            {
                "name":     "Cholamandalam Financial Holdings Ltd",
                "category": "Promoter",
                #             Q4FY24  Q1FY25  Q2FY25  Q3FY25  Q4FY25  Q1FY26  Q2FY26  Q3FY26
                "pct": [44.39,  44.38,  44.37,  44.35,  44.34,  44.33,  44.32,  44.18],
            },
            {
                "name":     "Ambadi Investments Limited",
                "category": "Promoter",
                "pct": [ 4.01,   4.01,   4.01,   4.01,   4.01,   4.01,   4.01,   4.00],
            },

            # ── FII ─────────────────────────────────────────────────────────────
            {
                "name":     "New World Fund Inc (Capital Group)",
                "category": "FII",
                "pct": [ 1.71,   1.90,   1.94,   2.02,   1.86,   1.72,   1.72,   1.71],
            },
            {
                "name":     "Smallcap World Fund, Inc (Capital Group)",
                "category": "FII",
                "pct": [ 1.44,   1.38,   1.38,   1.34,   1.31,   1.29,   1.29,   1.07],
            },
            {
                "name":     "Government Pension Fund Global (Norges)",
                "category": "FII",
                "pct": [ 1.19,   1.24,   1.07,   1.63,   1.39,   1.09,   1.12,   1.06],
            },
            {
                "name":     "EuroPacific Growth Fund (Capital Group)",
                "category": "FII",
                "pct": [ 1.01,   1.15,   1.15,   None,   None,   None,   None,   None],
            },

            # ── DII – Mutual Funds ──────────────────────────────────────────────
            {
                "name":     "Axis Mutual Fund",
                "category": "DII – MF",
                "pct": [ 3.98,   3.86,   3.43,   2.57,   2.39,   2.23,   2.04,   1.93],
            },
            {
                "name":     "SBI Mutual Fund",
                "category": "DII – MF",
                "pct": [ 1.57,   2.02,   1.82,   1.54,   1.62,   1.50,   1.39,   1.22],
            },
            {
                "name":     "HDFC Mutual Fund",
                "category": "DII – MF",
                "pct": [ 1.23,   1.21,   1.22,   1.33,   1.25,   1.12,   None,   None],
            },
            {
                "name":     "Aditya Birla Sun Life Mutual Fund",
                "category": "DII – MF",
                "pct": [ 1.15,   1.09,   1.00,   1.03,   1.02,   None,   None,   None],
            },
            {
                "name":     "Canara Robeco Mutual Fund",
                "category": "DII – MF",
                "pct": [ None,   1.08,   1.24,   1.13,   None,   None,   None,   None],
            },
            {
                "name":     "Invesco India Mutual Fund",
                "category": "DII – MF",
                "pct": [ None,   None,   None,   None,   None,   1.01,   1.20,   1.21],
            },
            {
                "name":     "Motilal Oswal Mutual Fund",
                "category": "DII – MF",
                "pct": [ None,   None,   None,   None,   None,   1.14,   1.15,   1.08],
            },
            {
                "name":     "Kotak Mahindra Mutual Fund",
                "category": "DII – MF",
                "pct": [ None,   None,   None,   None,   None,   None,   None,   1.16],
            },

            # ── DII – Pension / NPS ─────────────────────────────────────────────
            {
                "name":     "NPS Trust (SBI Pension Fund)",
                "category": "DII – Pension",
                "pct": [ None,   None,   None,   None,   None,   1.31,   1.31,   2.56],
            },
        ],
    },

    # ── L&T FINANCE ────────────────────────────────────────────────────────────
    # BSE code 533519 · NSE: LTF · L&T Group NBFC
    # Source: NSE corporate-share-holdings API (fetched Feb 2026)
    "L&T Finance": {

        "category_pct": {
            #                Q4FY24  Q1FY25  Q2FY25  Q3FY25  Q4FY25  Q1FY26  Q2FY26  Q3FY26
            "Promoter": [65.86,  66.37,  66.29,  66.25,  66.24,  66.16,  66.10,  66.03],
            "FII":      [11.05,   7.33,   6.73,   5.30,   5.48,   6.19,   6.41,   6.66],
            "DII":      [ 8.70,  11.64,  12.33,  12.17,  13.29,  14.11,  14.32,  15.33],
            "Public":   [14.40,  14.65,  14.65,  16.27,  15.00,  13.54,  13.17,  11.98],
        },

        "named_entities": [

            # ── Promoter Group ──────────────────────────────────────────────────
            {
                "name":     "Larsen and Toubro Limited",
                "category": "Promoter",
                #             Q4FY24  Q1FY25  Q2FY25  Q3FY25  Q4FY25  Q1FY26  Q2FY26  Q3FY26
                "pct": [65.86,  66.37,  66.29,  66.25,  66.24,  66.16,  66.10,  66.03],
            },

            # ── FII ─────────────────────────────────────────────────────────────
            # BNP Paribas held via ODI (Offshore Derivative Instrument);
            # exited after Q4FY24 — coincided with broader FII unwind from ~11% to ~7%.
            {
                "name":     "BNP Paribas Financial Markets (ODI)",
                "category": "FII",
                "pct": [ 2.43,   None,   None,   None,   None,   None,   None,   None],
            },

            # ── DII – Mutual Funds ──────────────────────────────────────────────
            {
                "name":     "Mirae Asset Large & Midcap Fund",
                "category": "DII – MF",
                "pct": [ None,   1.74,   2.57,   2.88,   3.46,   3.47,   2.88,   1.80],
            },
            {
                "name":     "Invesco India Mutual Fund",
                "category": "DII – MF",
                "pct": [ None,   1.23,   1.07,   1.17,   1.29,   1.65,   1.72,   1.75],
            },
            {
                "name":     "Kotak Midcap Fund",
                "category": "DII – MF",
                "pct": [ None,   None,   None,   None,   None,   None,   1.31,   1.80],
            },
            {
                "name":     "Axis Mutual Fund",
                "category": "DII – MF",
                "pct": [ None,   None,   None,   None,   None,   None,   1.10,   1.29],
            },
            {
                "name":     "Motilal Oswal Mutual Fund",
                "category": "DII – MF",
                "pct": [ None,   None,   None,   None,   None,   None,   None,   1.63],
            },

            # ── DII – Insurance ─────────────────────────────────────────────────
            {
                "name":     "Life Insurance Corporation Of India",
                "category": "DII – Insurance",
                "pct": [ 1.94,   1.94,   1.94,   2.07,   2.28,   1.70,   None,   None],
            },
            {
                "name":     "ICICI Prudential Life Insurance",
                "category": "DII – Insurance",
                "pct": [ 1.51,   1.50,   1.46,   1.44,   1.44,   1.47,   None,   1.17],
            },
            {
                "name":     "Tata AIA Life Insurance",
                "category": "DII – Insurance",
                "pct": [ None,   None,   None,   1.46,   1.54,   1.58,   None,   None],
            },
        ],
    },
}
