# NBFC Peer Data Cache
# Source: Screener.in investor presentations
# Period: Q3 FY26 (Oct–Dec 2025) — latest available quarter
# Last updated: Feb 2026
# Notes:
#   - Piramal ROA = RoAUM on Growth Business (not consolidated ROA)
#   - Muthoot GNPA = Stage-3 proxy; NNPA not separately disclosed
#   - Bajaj NIM = annualised net total income / avg AUM (screener.in, full 8Q); ROA/ROE are annualized
#   - Mahindra ROA/ROE = 9M FY26 annualized; D/E = 9M FY26
#   - Poonawalla ROE = not reported; NIM = NII/Avg-AUM annualized (screener.in, full 8Q now available)
#   - AB Capital CAR = not disclosed separately in investor deck
#   - Piramal PCR = Stage-3 PCR (27.9%); total provisions/AUM = 2.1%

NBFC_Q3FY26 = [
    {
        "name": "Bajaj Finance",
        "ticker": "BAJFINANCE",
        "segment": "Diversified Retail",
        "aum_cr": 485883,
        "pat_cr": 5317,
        "nim_pct": None,          # Not disclosed explicitly
        "roa_pct": 4.6,
        "roe_pct": 19.6,
        "gnpa_pct": 1.21,
        "nnpa_pct": 0.47,
        "pcr_pct": 61.0,
        "cost_of_borrowing_pct": 7.45,
        "d_e_ratio": 4.75,
        "car_pct": 21.45,
        "bvps_inr": 170,          # Approx
        "net_worth_cr": 107731,
    },
    {
        "name": "Shriram Finance",
        "ticker": "SHRIRAMFIN",
        "segment": "CV / Rural Lending",
        "aum_cr": 291709,
        "pat_cr": 2522,
        "nim_pct": 8.58,
        "roa_pct": 3.09,
        "roe_pct": 16.33,
        "gnpa_pct": 4.54,
        "nnpa_pct": 2.38,
        "pcr_pct": 48.77,
        "cost_of_borrowing_pct": 8.0,
        "d_e_ratio": 4.05,
        "car_pct": 20.27,
        "bvps_inr": 330,
        "net_worth_cr": None,
    },
    {
        "name": "Chola Finance",
        "ticker": "CHOLAFIN",
        "segment": "Vehicle / Home / SME",
        "aum_cr": 227770,
        "pat_cr": 1288,
        "nim_pct": 8.0,
        "roa_pct": 3.2,           # PBT ROA
        "roe_pct": 19.1,
        "gnpa_pct": 3.36,
        "nnpa_pct": 1.91,
        "pcr_pct": 43.0,
        "cost_of_borrowing_pct": 6.7,
        "d_e_ratio": 7.5,
        "car_pct": 19.16,
        "bvps_inr": 327,
        "net_worth_cr": 27577,
    },
    {
        "name": "Muthoot Finance",
        "ticker": "MUTHOOTFIN",
        "segment": "Gold Loans",
        "aum_cr": 164720,
        "pat_cr": 2824,
        "nim_pct": 12.77,
        "roa_pct": 7.59,
        "roe_pct": 32.03,
        "gnpa_pct": 1.58,         # Stage-3 proxy
        "nnpa_pct": None,         # Not disclosed
        "pcr_pct": None,          # Stage-3 PCR not separately given
        "cost_of_borrowing_pct": 8.9,
        "d_e_ratio": 3.40,
        "car_pct": None,
        "bvps_inr": 859,
        "net_worth_cr": None,
    },
    {
        "name": "Aditya Birla Capital",
        "ticker": "ABCAPITAL",
        "segment": "Diversified (NBFC+HFC+Insurance)",
        "aum_cr": 148182,
        "pat_cr": 772,
        "nim_pct": 6.12,
        "roa_pct": 2.25,
        "roe_pct": 15.2,
        "gnpa_pct": 1.51,
        "nnpa_pct": 0.84,
        "pcr_pct": 44.3,
        "cost_of_borrowing_pct": 6.56,
        "d_e_ratio": 4.59,
        "car_pct": None,
        "bvps_inr": 106,
        "net_worth_cr": 27723,
    },
    {
        "name": "Mahindra Finance",
        "ticker": "M&MFIN",
        "segment": "Vehicle / Rural",
        "aum_cr": 128965,
        "pat_cr": 810,
        "nim_pct": 7.5,
        "roa_pct": 1.9,           # 9M FY26 annualized
        "roe_pct": 11.8,          # 9M FY26 annualized
        "gnpa_pct": 3.80,
        "nnpa_pct": 1.82,
        "pcr_pct": 53.0,
        "cost_of_borrowing_pct": 6.0,
        "d_e_ratio": 4.87,
        "car_pct": None,
        "bvps_inr": 171,
        "net_worth_cr": None,
    },
    {
        "name": "L&T Finance",
        "ticker": "LTF",
        "segment": "Rural / Consumer / SME",
        "aum_cr": 114285,
        "pat_cr": 760,
        "nim_pct": 8.58,
        "roa_pct": 2.37,
        "roe_pct": 11.38,
        "gnpa_pct": 3.19,
        "nnpa_pct": 0.92,
        "pcr_pct": 72.0,
        "cost_of_borrowing_pct": 7.25,
        "d_e_ratio": 3.78,
        "car_pct": None,
        "bvps_inr": 108,
        "net_worth_cr": None,
    },
    {
        "name": "Piramal Finance",
        "ticker": "PIRAMALENT",
        "segment": "Retail / Wholesale Lending",
        "aum_cr": 96690,
        "pat_cr": 401,
        "nim_pct": 6.3,
        "roa_pct": 1.9,           # RoAUM on growth business
        "roe_pct": None,
        "gnpa_pct": 2.6,
        "nnpa_pct": 1.9,
        "pcr_pct": 27.9,          # Stage-3 PCR; total prov/AUM = 2.1%
        "cost_of_borrowing_pct": 8.9,
        "d_e_ratio": 2.71,
        "car_pct": None,
        "bvps_inr": 1232,
        "net_worth_cr": 27872,
    },
    {
        "name": "Poonawalla Fincorp",
        "ticker": "POONAWALLA",
        "segment": "Consumer / SME Loans",
        "aum_cr": 55017,
        "pat_cr": 150,
        "nim_pct": None,          # Not disclosed in quarterly press releases
        "roa_pct": 1.20,
        "roe_pct": None,          # Not reported
        "gnpa_pct": 1.51,
        "nnpa_pct": 0.80,
        "pcr_pct": 47.75,
        "cost_of_borrowing_pct": 7.65,
        "d_e_ratio": 4.25,
        "car_pct": 18.17,
        "bvps_inr": 124,
        "net_worth_cr": 9996,
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# 8-QUARTER TIME SERIES  (Q4FY24 → Q3FY26)
# Source: Screener.in AI presentations per company  |  Last updated: Feb 2026
# Conventions:
#   None  = not disclosed / not available in source
#   ~     = estimate / interpolated (flagged in comment)
#   (neg) = negative value e.g. Poonawalla Q2FY25 PAT loss
# ─────────────────────────────────────────────────────────────────────────────

QUARTERS = ["Q4FY24", "Q1FY25", "Q2FY25", "Q3FY25", "Q4FY25", "Q1FY26", "Q2FY26", "Q3FY26"]

# Each entry: list of 8 values aligned to QUARTERS above
# None = not available

NBFC_TIMESERIES = {
    "Poonawalla Fincorp": {
        "aum_cr":                [25003,  26972,  28396,  30984,  35631,  41273,  47701,  55017 ],
        "gnpa_pct":              [1.16,   0.67,   2.10,   1.85,   1.84,   1.84,   1.59,   1.51  ],
        "nnpa_pct":              [0.59,   0.32,   0.33,   0.81,   0.85,   0.85,   0.81,   0.80  ],
        "pcr_pct":               [49.39,  52.53,  84.47,  56.79,  54.47,  53.93,  49.65,  47.75 ],
        "pat_cr":                [332,    292,    -471,   19,     62,     63,     74,     150   ],
        "nim_pct":               [10.90,  10.40,  9.30,   9.00,   8.60,   8.00,   8.10,   8.40  ],  # screener.in NII/Avg-AUM annualized
        "roa_pct":               [5.73,   4.62,   0.00,   0.26,   0.76,   0.68,   0.69,   1.20  ],  # Q2FY25 = 0 (negative PAT quarter, avoids line break)
        "roe_pct":               [None,   None,   None,   None,   None,   None,   None,   None  ],  # not reported
        "cost_of_borrowing_pct": [8.17,   8.16,   8.10,   8.06,   8.07,   8.04,   7.69,   7.65  ],
        "d_e_ratio":             [1.86,   2.05,   2.26,   2.65,   3.19,   3.72,   3.64,   4.25  ],  # screener.in
        "car_pct":               [33.80,  31.57,  29.22,  25.89,  22.94,  20.55,  20.85,  18.17 ],  # screener.in
        "bvps_inr":              [105.03, 108.21, 103.74, 103.15, 105.12, 106.12, 121.66, 123.75],
    },
    "Bajaj Finance": {
        "aum_cr":                [330615, 354192, 373924, 398043, 416661, 441450, 462261, 485883],
        "gnpa_pct":              [0.85,   0.86,   1.06,   1.12,   0.96,   1.03,   1.24,   1.21  ],
        "nnpa_pct":              [0.37,   0.38,   0.46,   0.48,   0.44,   0.50,   0.60,   0.47  ],
        "pcr_pct":               [57,     56,     57,     57,     54,     52,     52,     61    ],
        "pat_cr":                [3825,   3912,   4014,   4308,   4546,   4765,   4948,   5317  ],
        "nim_pct":               [12.20,  12.17,  12.02,  12.10,  11.84,  11.76,  11.68,  11.71 ],  # screener.in (annualised net total income / avg AUM)
        "roa_pct":               [4.8,    4.6,    4.5,    4.5,    4.6,    4.5,    4.5,    4.6   ],
        "roe_pct":               [20.5,   19.9,   19.1,   19.1,   19.1,   19.0,   19.1,   19.6  ],
        "cost_of_borrowing_pct": [7.86,   7.94,   7.97,   7.96,   7.99,   7.79,   7.52,   7.45  ],
        "d_e_ratio":             [4.90,   4.90,   4.90,   4.90,   4.90,   4.70,   4.70,   4.75  ],  # screener.in (Q3FY26 = 4.7–4.8 range → 4.75)
        "car_pct":               [22.52,  21.65,  21.69,  21.57,  21.93,  21.96,  21.23,  21.45 ],  # screener.in
        "bvps_inr":              [150,    152,    155,    158,    160,    162,    165,    170   ],  # estimates (~)
    },
    "Shriram Finance": {
        "aum_cr":                [224862, 236000, 243043, 254470, 263190, 272249, 281309, 291709],
        "gnpa_pct":              [5.45,   5.40,   5.32,   5.38,   4.55,   4.53,   4.57,   4.54  ],  # Q1FY25 ~
        "nnpa_pct":              [2.80,   2.70,   2.64,   2.68,   2.64,   2.57,   2.49,   2.38  ],  # Q4FY24-Q1FY25 ~
        "pcr_pct":               [48,     50,     51.70,  51.64,  43.28,  44.31,  46.70,  48.77 ],  # Q4FY24-Q1FY25 ~
        "pat_cr":                [1939,   1981,   2071,   2080,   2348,   2156,   2307,   2522  ],  # Q4FY24-Q1FY25,Q3-Q4FY25 ~
        "nim_pct":               [8.60,   8.70,   8.74,   8.48,   8.55,   8.11,   8.19,   8.58  ],  # Q4FY24-Q1FY25 ~
        "roa_pct":               [3.3,    3.0,    3.06,   2.88,   2.98,   2.76,   2.89,   3.09  ],  # Q4FY24-Q1FY25,Q3FY25 ~
        "roe_pct":               [15.0,   15.5,   16.00,  15.41,  15.75,  15.07,  15.40,  16.33 ],  # Q4FY24-Q1FY25,Q3FY25 ~
        "cost_of_borrowing_pct": [8.7,    8.6,    8.5,    8.4,    8.3,    8.2,    8.1,    8.0   ],  # Q4FY24-Q2FY26 ~
        "d_e_ratio":             [4.30,   4.1,    3.99,   4.06,   4.16,   4.15,   3.88,   4.05  ],  # Q1FY25 ~
        "car_pct":               [None,   None,   None,   None,   None,   None,   None,   20.27 ],
        "bvps_inr":              [260,    272,    277,    292,    299,    311,    321,    330   ],  # Q4FY24-Q1FY25 ~
    },
    "Chola Finance": {
        "aum_cr":                [153718, 155442, 164642, 174567, 199876, 192148, 199159, 227770],
        "gnpa_pct":              [2.48,   None,   None,   2.91,   2.81,   3.16,   3.35,   3.36  ],  # Q1-Q2FY25 not reported
        "nnpa_pct":              [1.33,   None,   None,   1.65,   1.54,   1.78,   1.90,   1.91  ],  # Q1-Q2FY25 not reported; Q1FY26 ~
        "pcr_pct":               [44,     45.5,   44.5,   44.1,   45.3,   43.7,   43.2,   43.0  ],  # Q4FY24,Q2FY25 ~
        "pat_cr":                [1336,   942,    963,    1087,   1587,   1136,   1155,   1288  ],  # Q4FY24,Q4FY25 ~
        "nim_pct":               [7.5,    7.6,    7.5,    7.7,    7.7,    7.8,    7.9,    8.0   ],  # Q4FY24,Q4FY25 ~
        "roa_pct":               [2.8,    3.2,    3.0,    3.2,    2.39,   3.1,    3.0,    3.2   ],  # Q4FY24 ~
        "roe_pct":               [20.6,   18.9,   18.2,   19.7,   19.8,   18.9,   18.1,   19.1  ],  # Q4FY24 ~
        "cost_of_borrowing_pct": [6.9,    7.0,    7.1,    7.1,    7.1,    7.0,    6.8,    6.7   ],  # Q4FY24 ~
        "d_e_ratio":             [7.1,    7.4,    7.4,    7.4,    7.7,    7.6,    7.4,    7.5   ],  # Q1FY26,Q2FY26 ~
        "car_pct":               [None,   None,   None,   None,   None,   None,   None,   19.16 ],
        "bvps_inr":              [232,    243,    252,    267,    280,    292,    306,    327   ],  # Q4FY24-Q2FY26 ~; Q3FY26 confirmed
    },
    "Aditya Birla Capital": {
        "aum_cr":                [None,   107306, 114710, 119437, 126351, 131227, 139585, 148182],  # Q4FY24 missing
        "gnpa_pct":              [None,   2.54,   2.50,   2.30,   2.24,   2.27,   1.68,   1.51  ],
        "nnpa_pct":              [None,   1.28,   1.38,   1.25,   1.23,   1.34,   0.94,   0.84  ],
        "pcr_pct":               [None,   49.5,   46.0,   45.6,   45.0,   41.2,   44.2,   44.3  ],
        "pat_cr":                [None,   621,    629,    600,    652,    689,    714,    772   ],
        "nim_pct":               [None,   6.56,   6.28,   6.00,   6.07,   5.97,   6.06,   6.12  ],
        "roa_pct":               [None,   2.41,   2.34,   2.10,   2.25,   2.25,   2.20,   2.25  ],
        "roe_pct":               [None,   None,   None,   None,   14.2,   14.4,   14.2,   15.2  ],  # only from Q4FY25
        "cost_of_borrowing_pct": [None,   6.95,   6.85,   6.91,   6.83,   6.74,   6.62,   6.56  ],
        "d_e_ratio":             [None,   None,   None,   None,   4.41,   4.40,   4.55,   4.59  ],  # only from Q4FY25
        "car_pct":               [None,   None,   None,   None,   None,   None,   None,   None  ],  # not disclosed
        "bvps_inr":              [None,   None,   None,   None,   96,     99,     103,    106   ],  # only from Q4FY25
    },
    "L&T Finance": {
        "aum_cr":                [85565,  88717,  93015,  95120,  97762,  102314, 107096, 114285],
        "gnpa_pct":              [3.20,   3.20,   3.20,   3.23,   3.29,   3.31,   3.29,   3.19  ],  # Q4FY24-Q2FY26 ~
        "nnpa_pct":              [0.79,   0.96,   0.97,   0.97,   0.99,   1.00,   1.00,   0.92  ],
        "pcr_pct":               [75,     71,     71,     71,     71,     70,     72,     72    ],
        "pat_cr":                [686,    696,    626,    636,    701,    735,    760,    760   ],
        "nim_pct":               [9.31,   8.94,   8.50,   8.15,   8.24,   8.42,   8.58,   8.58  ],
        "roa_pct":               [2.68,   2.60,   2.27,   2.22,   2.37,   2.41,   2.41,   2.37  ],
        "roe_pct":               [10.5,   10.86,  11.65,  10.2,   10.5,   11.33,  11.33,  11.38 ],  # Q4FY24,Q3FY25,Q4FY25 ~
        "cost_of_borrowing_pct": [7.68,   7.84,   7.83,   7.80,   7.68,   7.40,   7.32,   7.25  ],  # Q4FY24-Q1FY26 ~
        "d_e_ratio":             [3.46,   3.50,   3.50,   3.46,   3.66,   3.71,   3.78,   3.78  ],
        "car_pct":               [None,   None,   None,   None,   None,   None,   None,   None  ],  # not disclosed
        "bvps_inr":              [97.4,   97.4,   99.9,   99.9,   102.4,  105.4,  108.3,  108.3 ],
    },
    "Piramal Finance": {
        "aum_cr":                [None,   None,   None,   None,   None,   None,   85756,  96690 ],  # only Q2-Q3FY26 from screener
        "gnpa_pct":              [None,   None,   None,   2.8,    2.8,    None,   2.8,    2.6   ],
        "nnpa_pct":              [None,   None,   None,   None,   1.9,    None,   2.0,    1.9   ],
        "pcr_pct":               [None,   None,   None,   None,   None,   None,   None,   27.9  ],  # Stage-3 PCR
        "pat_cr":                [137,    181,    163,    39,     102,    276,    327,    401   ],
        "nim_pct":               [4.6,    4.9,    5.1,    5.8,    5.8,    5.9,    6.1,    6.3   ],  # older ~estimate from yield data
        "roa_pct":               [None,   None,   None,   None,   None,   None,   None,   1.9   ],  # RoAUM on growth book, Q3FY26 only
        "roe_pct":               [None,   None,   None,   None,   2.0,    None,   2.0,    None  ],
        "cost_of_borrowing_pct": [None,   None,   None,   None,   None,   None,   None,   8.9   ],
        "d_e_ratio":             [None,   None,   None,   None,   None,   None,   None,   2.71  ],
        "car_pct":               [None,   None,   None,   None,   None,   None,   None,   None  ],
        "bvps_inr":              [None,   None,   None,   None,   None,   None,   None,   1232  ],
    },
    "Muthoot Finance": {
        "aum_cr":                [89079,  98048,  104149, 111308, 122181, 133938, 147673, 164720],
        "gnpa_pct":              [3.28,   3.98,   4.30,   4.22,   3.41,   2.58,   2.25,   1.58  ],  # Stage-3 proxy
        "nnpa_pct":              [None,   None,   None,   None,   None,   None,   None,   None  ],  # not disclosed
        "pcr_pct":               [None,   None,   None,   None,   None,   None,   None,   None  ],  # not disclosed
        "pat_cr":                [1182,   1196,   1321,   1392,   1444,   1974,   2412,   2824  ],
        "nim_pct":               [11.62,  11.51,  11.54,  11.60,  11.27,  12.15,  12.66,  12.77 ],
        "roa_pct":               [5.86,   5.39,   5.74,   5.81,   5.85,   7.16,   7.44,   7.59  ],
        "roe_pct":               [18.09,  17.73,  19.99,  20.70,  21.76,  28.28,  30.61,  32.03 ],
        "cost_of_borrowing_pct": [8.51,   8.74,   9.01,   8.81,   8.99,   8.68,   8.90,   8.85  ],
        "d_e_ratio":             [2.29,   2.61,   2.66,   2.75,   2.95,   3.18,   3.27,   3.40  ],
        "car_pct":               [None,   None,   None,   None,   None,   None,   None,   None  ],  # not reported
        "bvps_inr":              [604.95, 607.21, 639.67, 672.47, 708.26, 733.64, 793.09, 859.33],
    },
    "Mahindra Finance": {
        "aum_cr":                [102597, 106339, 112454, 115126, 119673, 122008, 127246, 128965],
        "gnpa_pct":              [3.40,   3.56,   3.83,   3.93,   3.69,   3.85,   3.94,   3.80  ],
        "nnpa_pct":              [1.28,   1.46,   1.59,   2.00,   1.84,   1.91,   1.89,   1.82  ],
        "pcr_pct":               [63.2,   59.8,   59.5,   50.1,   51.2,   51.4,   53.0,   53.0  ],
        "pat_cr":                [619,    513,    369,    899,    563,    530,    569,    810   ],
        "nim_pct":               [7.1,    6.6,    6.5,    6.6,    6.5,    6.7,    7.0,    7.5   ],
        "roa_pct":               [1.7,    1.4,    1.5,    2.0,    1.9,    1.6,    None,   1.9   ],  # Q2FY26 not reported
        "roe_pct":               [10.0,   11.1,   9.7,    12.7,   12.4,   9.8,    None,   11.8  ],  # Q2FY26 not reported
        "cost_of_borrowing_pct": [6.2,    6.3,    6.3,    6.4,    6.3,    6.3,    6.0,    6.0   ],
        "d_e_ratio":             [5.08,   5.10,   5.65,   5.44,   5.70,   4.75,   None,   4.87  ],  # Q2FY26 not reported
        "car_pct":               [None,   None,   None,   None,   None,   None,   None,   None  ],  # not disclosed
        "bvps_inr":              [147.0,  151.2,  148.0,  155.6,  160.4,  168.0,  None,   171.4 ],  # Q2FY26 not reported
    },
}

# ── Data quality flags ─────────────────────────────────────────────────────────
# ~ = estimated / interpolated from adjacent quarters or rating reports
# Piramal AUM: only Q2FY26+ confirmed; earlier quarters need Excel data sheet
# AB Capital: Q4FY24 entirely absent from screener source
# Bajaj Finance: BVPS all estimated (~); NIM/CAR/D/E now full 8Q from screener.in
# Muthoot Finance: NNPA and PCR not disclosed at all
# Poonawalla: ROE not reported; NIM = NII/Avg-AUM annualized, full 8Q from screener.in; CAR full 8Q now available
# L&T Finance: CAR not disclosed in investor deck
# Shriram/Chola Q4FY24-Q1FY25: several metrics ~estimated

# ── Metric-based cross-NBFC lookup (convenience) ──────────────────────────────
NBFC_ORDER = [
    "Poonawalla Fincorp",
    "Bajaj Finance",
    "Shriram Finance",
    "Chola Finance",
    "Aditya Birla Capital",
    "L&T Finance",
    "Piramal Finance",
    "Muthoot Finance",
    "Mahindra Finance",
]

def get_metric_table(metric: str) -> dict:
    """
    Returns {quarter: {nbfc_name: value}} for the given metric key.
    Missing values are None.
    """
    result = {}
    for i, q in enumerate(QUARTERS):
        result[q] = {}
        for nbfc in NBFC_ORDER:
            result[q][nbfc] = NBFC_TIMESERIES[nbfc][metric][i]
    return result

# ── Metadata for display ──────────────────────────────────────────────────────
METRIC_LABELS = {
    "aum_cr":                  ("AUM",                "₹ Cr"),
    "pat_cr":                  ("PAT",                "₹ Cr"),
    "nim_pct":                 ("NIM",                "%"),
    "roa_pct":                 ("ROA",                "%"),
    "roe_pct":                 ("ROE",                "%"),
    "gnpa_pct":                ("GNPA",               "%"),
    "nnpa_pct":                ("NNPA",               "%"),
    "pcr_pct":                 ("PCR",                "%"),
    "cost_of_borrowing_pct":   ("Cost of Borrowing",  "%"),
    "d_e_ratio":               ("D/E Ratio",          "x"),
    "car_pct":                 ("CAR",                "%"),
    "bvps_inr":                ("BVPS",               "₹"),
    "net_worth_cr":            ("Net Worth",          "₹ Cr"),
}
