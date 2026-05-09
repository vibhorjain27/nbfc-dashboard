# NBFC Peer Data Cache
# Source: Investor presentations (Q4FY26); Screener.in for prior quarters
# Period: Q4 FY26 (Jan–Mar 2026) — latest available quarter
# Last updated: May 2026
# Notes:
#   - Piramal ROA = RoAUM on Growth Business (not consolidated ROA)
#   - Muthoot GNPA = Stage-3 proxy; NNPA not separately disclosed
#   - Bajaj NIM = annualised net total income / avg AUM (before one-time actions); ROA/ROE annualized Q4
#   - Bajaj ROA/ROE = consolidated Q4 FY26 annualized, before one-time actions
#   - Poonawalla ROE = annualised estimate (PAT×4/Avg Equity, Screener.in); NIM = NII/Avg-AUM annualized
#   - AB Capital CAR/T1/T2 = investor deck; NNPA derived (GNPA × (1−PCR)); T2 = CAR−T1
#   - L&T Finance NIM = NIM + Fees (from RoA trajectory table in Q4FY26 investor deck); CAR/T1/T2 = investor deck Q4FY26
#   - Chola Finance, Muthoot Finance, Mahindra Finance: Q4FY26 PDFs pending — Q3FY26 values retained
#   - Piramal CAR = investor deck (consolidated); T1/T2 not disclosed; CoB = explicit 6.41%
#   - Piramal PCR = Stage-3 PCR (29.6%); total provisions/AUM higher

NBFC_Q4FY26 = [
    {
        "name": "Bajaj Finance",
        "ticker": "BAJFINANCE",
        "segment": "Diversified Retail",
        "aum_cr": 509975,
        "pat_cr": 5660,           # consolidated Q4, before one-time actions
        "nim_pct": 11.62,         # annualised Q4 NTI / avg AUM, before one-time
        "roa_pct": 4.65,          # consolidated Q4 annualized, before one-time
        "roe_pct": 20.0,          # consolidated Q4 annualized, before one-time
        "gnpa_pct": 1.01,         # consolidated
        "nnpa_pct": 0.41,         # consolidated
        "pcr_pct": 60.0,          # consolidated
        "cost_of_borrowing_pct": 7.42,
        "d_e_ratio": 4.8,
        "car_pct": 21.6,          # standalone
        "bvps_inr": 177,          # estimate (standalone equity / shares)
        "net_worth_cr": None,
    },
    {
        "name": "Shriram Finance",
        "ticker": "SHRIRAMFIN",
        "segment": "CV / Rural Lending",
        "aum_cr": 302274,
        "pat_cr": 3014,
        "nim_pct": 8.61,
        "roa_pct": 3.63,
        "roe_pct": 19.13,
        "gnpa_pct": 4.58,
        "nnpa_pct": 2.33,
        "pcr_pct": 50.34,
        "cost_of_borrowing_pct": 8.59,
        "d_e_ratio": 3.82,
        "car_pct": 20.40,
        "bvps_inr": 349,
        "net_worth_cr": None,
    },
    {
        "name": "Chola Finance",
        "ticker": "CHOLAFIN",
        "segment": "Vehicle / Home / SME",
        "aum_cr": 227770,         # Q3FY26 retained — Q4FY26 PDF pending
        "pat_cr": 1288,
        "nim_pct": 8.0,
        "roa_pct": 3.2,
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
        "aum_cr": 164720,         # Q3FY26 retained — Q4FY26 PDF pending
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
        "aum_cr": 159916,
        "pat_cr": 825,
        "nim_pct": 6.08,
        "roa_pct": 2.31,
        "roe_pct": 15.8,
        "gnpa_pct": 1.33,
        "nnpa_pct": 0.69,         # derived: GNPA × (1 − PCR)
        "pcr_pct": 47.8,
        "cost_of_borrowing_pct": 6.57,
        "d_e_ratio": 4.82,
        "car_pct": 16.79,
        "bvps_inr": 109,
        "net_worth_cr": None,
    },
    {
        "name": "Mahindra Finance",
        "ticker": "M&MFIN",
        "segment": "Vehicle / Rural",
        "aum_cr": 128965,         # Q3FY26 retained — Q4FY26 PDF pending
        "pat_cr": 810,
        "nim_pct": 7.5,
        "roa_pct": 1.9,
        "roe_pct": 11.8,
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
        "aum_cr": 121728,
        "pat_cr": 807,
        "nim_pct": 10.47,         # NIM + Fees
        "roa_pct": 2.40,
        "roe_pct": 11.71,
        "gnpa_pct": 2.88,
        "nnpa_pct": 0.96,
        "pcr_pct": 67.0,
        "cost_of_borrowing_pct": 7.17,
        "d_e_ratio": 3.93,
        "car_pct": 18.34,
        "bvps_inr": 111.7,
        "net_worth_cr": None,
    },
    {
        "name": "Piramal Finance",
        "ticker": "PIRAMALENT",
        "segment": "Retail / Wholesale Lending",
        "aum_cr": 101230,
        "pat_cr": 502,
        "nim_pct": 6.5,
        "roa_pct": 2.1,           # RoAUM on growth business
        "roe_pct": None,
        "gnpa_pct": 2.3,
        "nnpa_pct": 1.6,
        "pcr_pct": 29.6,          # Stage-3 PCR
        "cost_of_borrowing_pct": 6.41,
        "d_e_ratio": 2.8,
        "car_pct": 19.8,
        "bvps_inr": 1247,
        "net_worth_cr": None,
    },
    {
        "name": "Poonawalla Fincorp",
        "ticker": "POONAWALLA",
        "segment": "Consumer / SME Loans",
        "aum_cr": 60348,
        "pat_cr": 255,
        "nim_pct": 9.05,
        "roa_pct": 1.81,
        "roe_pct": 10.1,          # annualised: PAT×4/Avg Equity (Screener.in)
        "gnpa_pct": 1.44,
        "nnpa_pct": 0.74,
        "pcr_pct": 49.0,
        "cost_of_borrowing_pct": 7.63,
        "d_e_ratio": 4.67,
        "car_pct": 16.83,
        "bvps_inr": 146.13,
        "net_worth_cr": None,
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

QUARTERS = ["Q4FY24", "Q1FY25", "Q2FY25", "Q3FY25", "Q4FY25", "Q1FY26", "Q2FY26", "Q3FY26", "Q4FY26"]

# Each entry: list of 8 values aligned to QUARTERS above
# None = not available

NBFC_TIMESERIES = {
    "Poonawalla Fincorp": {
        "aum_cr":                [25003,  26972,  28396,  30984,  35631,  41273,  47701,  55017,  60348 ],
        "gnpa_pct":              [1.16,   0.67,   2.10,   1.85,   1.84,   1.84,   1.59,   1.51,   1.44  ],
        "nnpa_pct":              [0.59,   0.32,   0.33,   0.81,   0.85,   0.85,   0.81,   0.80,   0.74  ],
        "pcr_pct":               [49.39,  52.53,  84.47,  56.79,  54.47,  53.93,  49.65,  47.75,  49.0  ],
        "pat_cr":                [332,    292,    -471,   19,     62,     63,     74,     150,    255   ],
        "nim_pct":               [10.90,  10.40,  9.30,   9.00,   8.60,   8.32,   8.40,   8.62,   9.05  ],  # Q4FY24–Q4FY25 estimated; Q1FY26+ official
        "roa_pct":               [5.73,   4.62,   0.00,   0.26,   0.76,   0.68,   0.69,   1.20,   1.81  ],  # Q2FY25 = 0 (negative PAT quarter, avoids line break)
        "roe_pct":               [16.4,   14.2,   -23.0,  0.9,    3.1,    3.1,    3.3,    6.1,    10.1  ],  # annualised: PAT×4/Avg Equity (Screener.in estimate)
        "cost_of_borrowing_pct": [8.17,   8.16,   8.10,   8.06,   8.07,   8.04,   7.69,   7.65,   7.63  ],
        "d_e_ratio":             [1.86,   2.05,   2.26,   2.65,   3.19,   3.72,   3.64,   4.25,   4.67  ],
        "car_pct":               [33.80,  31.57,  29.22,  25.89,  22.94,  20.55,  20.85,  18.17,  16.83 ],
        "t1_pct":                [32.28,  30.09,  27.75,  24.46,  21.67,  19.02,  19.63,  17.15,  15.90 ],
        "t2_pct":                [1.52,   1.48,   1.47,   1.43,   1.27,   1.53,   1.22,   1.02,   0.93  ],  # derived: CAR − T1
        "bvps_inr":              [105.03, 108.21, 103.74, 103.15, 105.12, 106.12, 121.66, 123.75, 146.13],
    },
    "Bajaj Finance": {
        "aum_cr":                [330615, 354192, 373924, 398043, 416661, 441450, 462261, 485883, 509975],
        "gnpa_pct":              [0.85,   0.86,   1.06,   1.12,   0.96,   1.03,   1.24,   1.21,   1.01  ],  # consolidated
        "nnpa_pct":              [0.37,   0.38,   0.46,   0.48,   0.44,   0.50,   0.60,   0.47,   0.41  ],  # consolidated
        "pcr_pct":               [57,     56,     57,     57,     54,     52,     52,     61,     60    ],  # consolidated
        "pat_cr":                [3825,   3912,   4014,   4308,   4546,   4765,   4948,   5317,   5660  ],  # consolidated, before one-time
        "nim_pct":               [12.20,  12.17,  12.02,  12.10,  11.84,  11.76,  11.68,  11.71,  11.62 ],  # annualised Q4 NTI / avg AUM
        "roa_pct":               [4.8,    4.6,    4.5,    4.5,    4.6,    4.5,    4.5,    4.6,    4.65  ],  # Q4 annualized, before one-time
        "roe_pct":               [20.5,   19.9,   19.1,   19.1,   19.1,   19.0,   19.1,   19.6,   20.0  ],  # Q4 annualized, before one-time
        "cost_of_borrowing_pct": [7.86,   7.94,   7.97,   7.96,   7.99,   7.79,   7.52,   7.45,   7.42  ],  # consolidated annualized
        "d_e_ratio":             [4.90,   4.90,   4.90,   4.90,   4.90,   4.70,   4.70,   4.75,   4.8   ],  # consolidated leverage
        "car_pct":               [22.52,  21.65,  21.69,  21.57,  21.93,  21.96,  21.23,  21.45,  21.6  ],  # standalone
        "t1_pct":                [21.51,  20.73,  20.90,  20.79,  21.09,  21.19,  20.60,  20.60,  20.7  ],  # standalone
        "t2_pct":                [1.01,   0.92,   0.79,   0.78,   0.84,   0.77,   0.63,   0.85,   0.9   ],  # standalone
        "bvps_inr":              [150,    152,    155,    158,    160,    162,    165,    170,    177   ],  # estimate (standalone equity / shares)
    },
    "Shriram Finance": {
        "aum_cr":                [224862, 236000, 243043, 254470, 263190, 272249, 281309, 291709, 302274],
        "gnpa_pct":              [5.45,   5.40,   5.32,   5.38,   4.55,   4.53,   4.57,   4.54,   4.58  ],
        "nnpa_pct":              [2.80,   2.70,   2.64,   2.68,   2.64,   2.57,   2.49,   2.38,   2.33  ],
        "pcr_pct":               [48,     50,     51.70,  51.64,  43.28,  44.31,  46.70,  48.77,  50.34 ],
        "pat_cr":                [1939,   1981,   2071,   2080,   2348,   2156,   2307,   2522,   3014  ],
        "nim_pct":               [8.60,   8.70,   8.74,   8.48,   8.55,   8.11,   8.19,   8.58,   8.61  ],
        "roa_pct":               [3.3,    3.0,    3.06,   2.88,   2.98,   2.76,   2.89,   3.09,   3.63  ],
        "roe_pct":               [15.0,   15.5,   16.00,  15.41,  15.75,  15.07,  15.40,  16.33,  19.13 ],
        "cost_of_borrowing_pct": [9.08,   9.10,   9.06,   9.00,   8.96,   8.87,   8.83,   8.69,   8.59  ],
        "d_e_ratio":             [4.30,   4.1,    3.99,   4.06,   4.16,   4.15,   3.88,   4.05,   3.82  ],
        "car_pct":               [20.30,  20.29,  20.16,  21.00,  20.66,  20.79,  20.68,  20.27,  20.40 ],
        "t1_pct":                [19.55,  19.47,  19.36,  20.34,  20.03,  20.16,  19.98,  19.66,  19.80 ],
        "t2_pct":                [0.75,   0.82,   0.80,   0.66,   0.63,   0.63,   0.70,   0.61,   0.60  ],
        "bvps_inr":              [260,    272,    277,    292,    299,    311,    321,    330,    349   ],
    },
    "Chola Finance": {
        "aum_cr":                [153718, 155442, 164642, 174567, 199876, 192148, 199159, 227770, None  ],  # Q4FY26 pending
        "gnpa_pct":              [2.48,   None,   None,   2.91,   2.81,   3.16,   3.35,   3.36,   None  ],
        "nnpa_pct":              [1.33,   None,   None,   1.65,   1.54,   1.78,   1.90,   1.91,   None  ],
        "pcr_pct":               [44,     45.5,   44.5,   44.1,   45.3,   43.7,   43.2,   43.0,   None  ],
        "pat_cr":                [1336,   942,    963,    1087,   1587,   1136,   1155,   1288,   None  ],
        "nim_pct":               [7.5,    7.6,    7.5,    7.7,    7.7,    7.8,    7.9,    8.0,    None  ],
        "roa_pct":               [2.8,    3.2,    3.0,    3.2,    2.39,   3.1,    3.0,    3.2,    None  ],
        "roe_pct":               [20.6,   18.9,   18.2,   19.7,   19.8,   18.9,   18.1,   19.1,   None  ],
        "cost_of_borrowing_pct": [6.9,    7.0,    7.1,    7.1,    7.1,    7.0,    6.8,    6.7,    None  ],
        "d_e_ratio":             [7.1,    7.4,    7.4,    7.4,    7.7,    7.6,    7.4,    7.5,    None  ],
        "car_pct":               [18.56,  19.0,   19.5,   19.7,   19.75,  19.96,  20.00,  19.16,  None  ],
        "t1_pct":                [15.09,  14.8,   14.5,   14.4,   14.41,  14.31,  14.59,  14.21,  None  ],
        "t2_pct":                [3.47,   4.2,    5.0,    5.3,    5.34,   5.65,   5.41,   4.95,   None  ],
        "bvps_inr":              [232,    243,    252,    267,    280,    292,    306,    327,    None  ],
    },
    "Aditya Birla Capital": {
        "aum_cr":                [105639, 107306, 114710, 119437, 126351, 131227, 139585, 148182, 159916],
        "gnpa_pct":              [3.12,   2.54,   2.50,   2.27,   2.24,   2.27,   1.68,   1.51,   1.33  ],
        "nnpa_pct":              [None,   1.28,   1.38,   1.25,   1.23,   1.34,   0.94,   0.84,   0.69  ],  # Q4FY26 derived (GNPA × (1−PCR))
        "pcr_pct":               [46.2,   49.5,   46.0,   45.6,   45.0,   41.2,   44.2,   44.3,   47.8  ],
        "pat_cr":                [585,    621,    629,    600,    652,    689,    714,    772,    825   ],
        "nim_pct":               [6.86,   6.56,   6.28,   6.00,   6.07,   5.97,   6.06,   6.12,   6.08  ],
        "roa_pct":               [2.40,   2.41,   2.34,   2.10,   2.25,   2.25,   2.20,   2.25,   2.31  ],
        "roe_pct":               [None,   None,   None,   None,   14.2,   14.4,   14.2,   15.2,   15.8  ],
        "cost_of_borrowing_pct": [6.90,   6.95,   6.85,   6.91,   6.83,   6.74,   6.62,   6.56,   6.57  ],
        "d_e_ratio":             [6.05,   6.03,   5.85,   5.85,   None,   4.40,   4.55,   4.59,   4.82  ],
        "car_pct":               [16.24,  16.55,  16.48,  16.77,  None,   18.11,  17.98,  17.34,  16.79 ],
        "t1_pct":                [14.13,  14.48,  14.47,  14.43,  None,   15.62,  15.39,  14.56,  13.82 ],
        "t2_pct":                [2.11,   2.07,   2.01,   2.34,   None,   2.49,   2.59,   2.78,   2.97  ],  # Q4FY26 = CAR − T1
        "bvps_inr":              [None,   None,   None,   None,   96,     99,     103,    106,    109   ],
    },
    "L&T Finance": {
        "aum_cr":                [85565,  88717,  93015,  95120,  97762,  102314, 107096, 114285, 121728],
        "gnpa_pct":              [3.20,   3.20,   3.20,   3.23,   3.29,   3.31,   3.29,   3.19,   2.88  ],
        "nnpa_pct":              [0.79,   0.96,   0.97,   0.97,   0.99,   1.00,   1.00,   0.92,   0.96  ],
        "pcr_pct":               [75,     71,     71,     71,     71,     70,     72,     72,     67    ],
        "pat_cr":                [686,    696,    626,    636,    701,    735,    760,    760,    807   ],
        "nim_pct":               [11.25,  11.08,  10.86,  10.33,  10.15,  10.22,  10.22,  10.41,  10.47 ],  # NIM + Fees, from Q4FY26 investor deck (RoA trajectory table)
        "roa_pct":               [2.68,   2.60,   2.27,   2.22,   2.37,   2.41,   2.41,   2.37,   2.40  ],
        "roe_pct":               [10.5,   10.86,  11.65,  10.2,   10.5,   11.33,  11.33,  11.38,  11.71 ],
        "cost_of_borrowing_pct": [7.68,   7.84,   7.83,   7.80,   7.68,   7.40,   7.32,   7.25,   7.17  ],  # WACB from Q4FY26 investor deck (ALM slide)
        "d_e_ratio":             [3.46,   3.50,   3.50,   3.46,   3.66,   3.71,   3.78,   3.78,   3.93  ],
        "car_pct":               [22.84,  22.10,  22.16,  22.0,   22.27,  20.68,  20.0,   19.10,  18.34 ],
        "t1_pct":                [21.02,  20.37,  20.53,  None,   20.76,  19.54,  None,   18.43,  17.60 ],
        "t2_pct":                [1.82,   1.73,   1.63,   None,   1.51,   1.14,   None,   0.67,   0.74  ],
        "bvps_inr":              [97.4,   97.4,   99.9,   99.9,   102.4,  105.4,  108.3,  108.3,  111.7 ],
    },
    "Piramal Finance": {
        "aum_cr":                [None,   None,   None,   None,   None,   None,   85756,  96690,  101230],
        "gnpa_pct":              [None,   None,   None,   2.8,    2.8,    None,   2.8,    2.6,    2.3   ],
        "nnpa_pct":              [None,   None,   None,   None,   1.9,    None,   2.0,    1.9,    1.6   ],
        "pcr_pct":               [None,   None,   None,   None,   None,   None,   None,   27.9,   29.6  ],  # Stage-3 PCR
        "pat_cr":                [137,    181,    163,    39,     102,    276,    327,    401,    502   ],
        "nim_pct":               [4.6,    4.9,    5.1,    5.8,    5.8,    5.9,    6.1,    6.3,    6.5   ],
        "roa_pct":               [None,   None,   None,   None,   None,   None,   None,   1.9,    2.1   ],  # RoAUM on growth book
        "roe_pct":               [None,   None,   None,   None,   2.0,    None,   2.0,    None,   None  ],
        "cost_of_borrowing_pct": [None,   None,   None,   None,   None,   None,   None,   8.9,    6.41  ],  # Q4FY26 explicitly stated in deck
        "d_e_ratio":             [None,   None,   None,   None,   None,   None,   None,   2.71,   2.8   ],
        "car_pct":               [25.60,  24.4,   23.3,   23.7,   23.6,   19.3,   20.7,   None,   19.8  ],
        "t1_pct":                [None,   None,   None,   None,   None,   None,   None,   None,   None  ],  # not disclosed
        "t2_pct":                [None,   None,   None,   None,   None,   None,   None,   None,   None  ],  # not disclosed
        "bvps_inr":              [None,   None,   None,   None,   None,   None,   None,   1232,   1247  ],
    },
    "Muthoot Finance": {
        "aum_cr":                [89079,  98048,  104149, 111308, 122181, 133938, 147673, 164720, None  ],  # Q4FY26 pending
        "gnpa_pct":              [3.28,   3.98,   4.30,   4.22,   3.41,   2.58,   2.25,   1.58,   None  ],  # Stage-3 proxy
        "nnpa_pct":              [None,   None,   None,   None,   None,   None,   None,   None,   None  ],  # not disclosed
        "pcr_pct":               [None,   None,   None,   None,   None,   None,   None,   None,   None  ],  # not disclosed
        "pat_cr":                [1182,   1196,   1321,   1392,   1444,   1974,   2412,   2824,   None  ],
        "nim_pct":               [11.62,  11.51,  11.54,  11.60,  11.27,  12.15,  12.66,  12.77,  None  ],
        "roa_pct":               [5.86,   5.39,   5.74,   5.81,   5.85,   7.16,   7.44,   7.59,   None  ],
        "roe_pct":               [18.09,  17.73,  19.99,  20.70,  21.76,  28.28,  30.61,  32.03,  None  ],
        "cost_of_borrowing_pct": [8.51,   8.74,   9.01,   8.81,   8.99,   8.68,   8.90,   8.85,   None  ],
        "d_e_ratio":             [2.29,   2.61,   2.66,   2.75,   2.95,   3.18,   3.27,   3.40,   None  ],
        "car_pct":               [None,   None,   None,   None,   None,   None,   None,   None,   None  ],  # not reported
        "t1_pct":                [None,   None,   None,   None,   None,   None,   None,   None,   None  ],  # not reported
        "t2_pct":                [None,   None,   None,   None,   None,   None,   None,   None,   None  ],  # not reported
        "bvps_inr":              [604.95, 607.21, 639.67, 672.47, 708.26, 733.64, 793.09, 859.33, None  ],
    },
    "Mahindra Finance": {
        "aum_cr":                [102597, 106339, 112454, 115126, 119673, 122008, 127246, 128965, None  ],  # Q4FY26 pending
        "gnpa_pct":              [3.40,   3.56,   3.83,   3.93,   3.69,   3.85,   3.94,   3.80,   None  ],
        "nnpa_pct":              [1.28,   1.46,   1.59,   2.00,   1.84,   1.91,   1.89,   1.82,   None  ],
        "pcr_pct":               [63.2,   59.8,   59.5,   50.1,   51.2,   51.4,   53.0,   53.0,   None  ],
        "pat_cr":                [619,    513,    369,    899,    563,    530,    569,    810,    None  ],
        "nim_pct":               [7.1,    6.6,    6.5,    6.6,    6.5,    6.7,    7.0,    7.5,    None  ],
        "roa_pct":               [1.7,    1.4,    1.5,    2.0,    1.9,    1.6,    None,   1.9,    None  ],
        "roe_pct":               [10.0,   11.1,   9.7,    12.7,   12.4,   9.8,    None,   11.8,   None  ],
        "cost_of_borrowing_pct": [6.2,    6.3,    6.3,    6.4,    6.3,    6.3,    6.0,    6.0,    None  ],
        "d_e_ratio":             [5.08,   5.10,   5.65,   5.44,   5.70,   4.75,   None,   4.87,   None  ],
        "car_pct":               [None,   None,   None,   None,   None,   None,   None,   None,   None  ],  # not disclosed
        "t1_pct":                [None,   None,   None,   None,   None,   None,   None,   None,   None  ],  # not disclosed
        "t2_pct":                [None,   None,   None,   None,   None,   None,   None,   None,   None  ],  # not disclosed
        "bvps_inr":              [147.0,  151.2,  148.0,  155.6,  160.4,  168.0,  None,   171.4,  None  ],
    },
}

# ── Data quality flags ─────────────────────────────────────────────────────────
# ~ = estimated / interpolated from adjacent quarters or rating reports
# Chola Finance / Muthoot Finance / Mahindra Finance: Q4FY26 PDFs not yet received; None values in Q9
# Bajaj Finance Q4FY26: consolidated basis; BVPS estimate from standalone equity/shares; NIM = annualised Q4 NTI/avg AUM
# AB Capital Q4FY26: NNPA derived (GNPA × (1−PCR)); T2 = CAR − T1
# Piramal AUM: Q1-Q1FY26 not from screener; only Q2FY26+ confirmed
# Muthoot Finance: NNPA and PCR not disclosed at all
# Poonawalla: ROE not reported; NIM = NII/Avg-AUM annualized
# L&T Finance Q4FY26: all metrics from investor deck; CoB = WACB 7.17% (ALM slide)
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
    "t1_pct":                  ("Tier 1 Capital",     "%"),
    "t2_pct":                  ("Tier 2 Capital",     "%"),
    "bvps_inr":                ("BVPS",               "₹"),
    "net_worth_cr":            ("Net Worth",          "₹ Cr"),
}
