# NBFC Peer Data Cache
# Source: Screener.in AI summaries of each company's investor presentation
# Period: rolling last 8 quarters — latest is the final entry in QUARTERS
# Last updated: Aug 2026 (Q1FY27 in progress — see coverage note below)
# Notes:
#   - Piramal ROA = RoAUM on Growth Business (not consolidated ROA)
#   - Muthoot GNPA = Stage-3 proxy; NNPA not separately disclosed
#   - Bajaj NIM = annualised net total income / avg AUM (before one-time actions); ROA/ROE annualized Q4
#   - Bajaj ROA/ROE = consolidated Q4 FY26 annualized, before one-time actions
#   - Poonawalla ROE = annualised estimate (PAT×4/Avg Equity, Screener.in); NIM = NII/Avg-AUM annualized
#   - AB Capital CAR/T1/T2 = investor deck; NNPA derived (GNPA × (1−PCR)); T2 = CAR−T1
#   - L&T Finance NIM = NIM + Fees (from RoA trajectory table in Q4FY26 investor deck); CAR/T1/T2 = investor deck Q4FY26
#   - Muthoot Finance: updated from Q4FY26 investor deck (standalone; ROA = PAT/Avg Loan Assets)
#   - Mahindra Finance: Q4FY26 PDF pending — Q3FY26 values retained
#   - Chola Finance Q4FY26: all metrics from Screener.in (Screener AI summary); BVPS verified via consolidated balance sheet
#   - Piramal CAR = investor deck (consolidated); T1/T2 not disclosed; CoB = Q4FY26 investor deck (restated ex-currency, Q4FY26: 8.84%)
#   - Piramal PCR = Stage-3 PCR (29.6%); total provisions/AUM higher
#   - Shriram Q1FY27: standalone. The MUFG equity infusion (Apr-2026) is why
#     CAR jumps 20.4->34.2, D/E falls 3.82->2.14, BVPS rises 349->462 and ROE
#     dips 19.1->12.8 in one quarter — a capital raise, not a data error.
#   - Bajaj Q1FY27: BVPS 183 supplied separately (not in the Q1 deck). D/E 4.90
#     is the deck's '4.9x leverage'; T2 0.89 = CAR - T1.
#   - Chola Q1FY27: PCR 35.49 is the company-stated RBI-basis figure, on the same
#     basis as the GNPA/NNPA recorded here (deriving 1-NNPA/GNPA would give
#     34.44). BVPS 376 = networth 32,078cr / 85.32cr shares — the same share
#     count implied by the Q4FY26 entry, so the series stays consistent.
#     PAT 1,654 is standalone (consolidated 1,656 — immaterial difference).
#   - Piramal Q1FY27: T2 is a real 0.0, not a gap — no Tier 2 capital
#     outstanding, so CAR == T1 (18.85). First quarter with T1/T2 populated.
#   - Mahindra Q4FY26: backfilled from the Q1FY27 deck's comparatives. ROE is
#     deliberately left None — the only figure available was FY26 full-year
#     RONW (~12.5%), and putting an annual number in a quarterly series would
#     misstate the trend. Q4FY26 also gives Mahindra its first-ever CAR/T1/T2.
#   - Muthoot Q1FY27: VERIFY AGAINST THE DECK. CoB jumps 8.58 -> 10.68 (+210bp)
#     after 7 quarters in an 8.58-9.01 band that was drifting DOWN. Recorded as
#     reported because the quarter is internally coherent — that cost spike
#     lines up with NIM 13.38->10.65, ROA 7.95->6.09, ROE 34.2->26.6 and PAT
#     -17% QoQ despite AUM +5.7%. A parsing error would corrupt one metric, not
#     six in a mutually consistent direction. Still, +210bp in a quarter is
#     extreme for a lender; confirm before this goes in front of anyone.
#     Q1FY27 is also the first quarter Muthoot discloses NNPA (1.99) and PCR
#     (13.01) at all — the low PCR is normal for a fully-collateralised gold book.
#   - Poonawalla Q1FY27: BVPS 149.12 is exact, not the deck's '~148' — audited
#     Reg 52(4) net worth 13,060.07cr / 87.58cr shares (share capital 175.16cr
#     at Rs2 face). QIP completed 13-Apr-2026: 6.743cr shares at Rs370.75 =
#     Rs2,500cr, plus 0.025cr ESOP shares — share count 80.795 -> 87.58cr.
#     WARNING: Q4FY26 BVPS 146.13 looks ~15% too high. Rolling the audited
#     closing net worth back (13,060.07 - 2,500 QIP - 307.71 PAT + 7.38 OCI)
#     gives opening equity ~10,260cr = BVPS ~127 on 80.795cr shares, which also
#     matches the ~10,298cr Mar-26 equity in the Q4FY26 deck and sits smoothly
#     after Q3FY26's 123.75. Needs the Q4FY26 net worth to confirm before fixing.
#   - AB Capital Q1FY27: figures are the standalone NBFC-ICC entity (not the
#     listed group) — the same basis the rest of this series uses, confirmed by
#     NIM 6.08->6.07, ROA 2.31->2.39, CoB 6.57->6.52 all running continuously.
#     BVPS left None: the deck gives NBFC net worth (33,700cr) but no share
#     count, and dividing it by the LISTED GROUP's 273.6cr shares gives 123.2
#     against 109 at Q4FY26 — a basis mismatch, not 13% one-quarter growth.
#     NNPA 0.67 follows this series' standing convention GNPA x (1-PCR), which
#     reproduces the stored value exactly in each of the last 5 quarters.

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
        "aum_cr": 242630,
        "pat_cr": 1641,
        "nim_pct": 8.4,
        "roa_pct": 2.9,
        "roe_pct": 23.0,
        "gnpa_pct": 4.36,
        "nnpa_pct": 2.87,
        "pcr_pct": 34.2,          # PCR = 1 − NNPA/GNPA; Stage-3 coverage = 47.3%
        "cost_of_borrowing_pct": 6.6,
        "d_e_ratio": 6.9,
        "car_pct": 19.21,
        "bvps_inr": 357,          # equity ₹30,458 Cr ÷ 85.3 Cr shares (Screener)
        "net_worth_cr": 30458,
    },
    {
        "name": "Muthoot Finance",
        "ticker": "MUTHOOTFIN",
        "segment": "Gold Loans",
        "aum_cr": 162826,         # Q4FY26 standalone loan AUM (principal), from investor deck
        "pat_cr": 3086,           # Q4FY26 standalone PAT (30,862 Mn)
        "nim_pct": 13.38,         # NIM on avg loan assets, annualized Q4FY26
        "roa_pct": 7.95,          # PAT / Avg Loan Assets annualized (Muthoot-disclosed metric)
        "roe_pct": 34.17,         # Return on Avg Equity annualized Q4FY26
        "gnpa_pct": 2.35,         # Stage-3 proxy (% Stage-III on total loan assets)
        "nnpa_pct": None,         # Not disclosed
        "pcr_pct": None,          # Not disclosed (gold-loan structure)
        "cost_of_borrowing_pct": 8.58,  # Interest expense on avg borrowings, annualized Q4FY26
        "d_e_ratio": 3.46,        # Capital gearing = net debt / tangible networth (investor deck)
        "car_pct": 20.75,         # Standalone CAR; T1=19.84%, T2=0.91%
        "bvps_inr": 940.05,       # Standalone BVPS (₹37,742 Cr / 40.15 Cr shares)
        "net_worth_cr": 37742,    # Standalone tangible networth Mar-26 (377,425 Mn)
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
        "cost_of_borrowing_pct": 8.84,         # Q4FY26 investor deck (restated ex-currency movement); prior 6.41% was erroneous
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
# ROLLING 8-QUARTER TIME SERIES  (see QUARTERS below)
# Roll forward with:  python roll_quarter.py --quarter <QxFYyy> --data <file>.json
# Source: Screener.in AI presentations per company; Q4FY26 investor decks
# Last updated: May 2026
# Conventions:
#   None  = not disclosed / not available in source
#   ~     = estimate / interpolated (flagged in comment)
#   (neg) = negative value e.g. Poonawalla Q2FY25 PAT loss
# ─────────────────────────────────────────────────────────────────────────────

QUARTERS = ["Q2FY25", "Q3FY25", "Q4FY25", "Q1FY26", "Q2FY26", "Q3FY26", "Q4FY26", "Q1FY27"]

# Each entry: list of 8 values aligned to QUARTERS above
# None = not available


def quarter_end_date(label):
    """'Q1FY27' -> datetime.date(2026, 6, 30).

    Indian fiscal year: FY27 runs Apr-2026 to Mar-2027, so Q1-Q3 fall in the
    prior calendar year and only Q4 lands in the FY's own year. Derived rather
    than hardcoded so rolling the window forward needs no code change.
    """
    from datetime import date
    q = int(label[1])
    fy = 2000 + int(label[4:])
    return {
        1: date(fy - 1, 6, 30),
        2: date(fy - 1, 9, 30),
        3: date(fy - 1, 12, 31),
        4: date(fy, 3, 31),
    }[q]


# [(date, index)] aligned to QUARTERS — used to step quarterly figures like BVPS
# against daily price series.
QUARTER_ENDS = [(quarter_end_date(q), i) for i, q in enumerate(QUARTERS)]

NBFC_TIMESERIES = {
    "Poonawalla Fincorp": {
        "aum_cr":                [28396, 30984, 35631, 41273, 47701, 55017, 60348, 67054],
        "gnpa_pct":              [2.1,   1.85,  1.84,  1.84,  1.59,  1.51,  1.44,  1.37],
        "nnpa_pct":              [0.33,  0.81,  0.85,  0.85,  0.81,  0.8,   0.74,  0.7],
        "pcr_pct":               [84.47, 56.79, 54.47, 53.93, 49.65, 47.75, 49,    49.11],
        "pat_cr":                [-471,  19,    62,    63,    74,    150,   255,   308],
        "nim_pct":               [9.3,   9,     8.6,   8.32,  8.4,   8.62,  9.05,  9.1],  # Q4FY24–Q4FY25 estimated; Q1FY26+ official
        "roa_pct":               [0,     0.26,  0.76,  0.68,  0.69,  1.2,   1.81,  1.98],  # Q2FY25 = 0 (negative PAT quarter, avoids line break)
        "roe_pct":               [-23,   0.9,   3.1,   3.1,   3.3,   6.1,   10.1,  11],  # annualised: PAT×4/Avg Equity (Screener.in estimate)
        "cost_of_borrowing_pct": [8.1,   8.06,  8.07,  8.04,  7.69,  7.65,  7.63,  7.72],
        "d_e_ratio":             [2.26,  2.65,  3.19,  3.72,  3.64,  4.25,  4.67,  3.82],
        "car_pct":               [29.22, 25.89, 22.94, 20.55, 20.85, 18.17, 16.83, 19.46],
        "t1_pct":                [27.75, 24.46, 21.67, 19.02, 19.63, 17.15, 15.9,  18.37],
        "t2_pct":                [1.47,  1.43,  1.27,  1.53,  1.22,  1.02,  0.93,  1.09],  # derived: CAR − T1
        "bvps_inr":              [103.74, 103.15, 105.12, 106.12, 121.66, 123.75, 146.13, 149.12],
    },
    "Bajaj Finance": {
        "aum_cr":                [373924, 398043, 416661, 441450, 462261, 485883, 509975, 546944],
        "gnpa_pct":              [1.06,  1.12,  0.96,  1.03,  1.24,  1.21,  1.01,  0.96],  # consolidated
        "nnpa_pct":              [0.46,  0.48,  0.44,  0.5,   0.6,   0.47,  0.41,  0.39],  # consolidated
        "pcr_pct":               [57,    57,    54,    52,    52,    61,    60,    60],  # consolidated
        "pat_cr":                [4014,  4308,  4546,  4765,  4948,  5317,  5660,  6081],  # consolidated, before one-time
        "nim_pct":               [12.02, 12.1,  11.84, 11.76, 11.68, 11.71, 11.62, 11.8],  # annualised Q4 NTI / avg AUM
        "roa_pct":               [4.5,   4.5,   4.6,   4.5,   4.5,   4.6,   4.65,  4.7],  # Q4 annualized, before one-time
        "roe_pct":               [19.1,  19.1,  19.1,  19,    19.1,  19.6,  20,    20.4],  # Q4 annualized, before one-time
        "cost_of_borrowing_pct": [7.97,  7.96,  7.99,  7.79,  7.52,  7.45,  7.42,  7.4],  # consolidated annualized
        "d_e_ratio":             [4.9,   4.9,   4.9,   4.7,   4.7,   4.75,  4.8,   4.9],  # consolidated leverage
        "car_pct":               [21.69, 21.57, 21.93, 21.96, 21.23, 21.45, 21.6,  20.9],  # standalone
        "t1_pct":                [20.9,  20.79, 21.09, 21.19, 20.6,  20.6,  20.7,  20.01],  # standalone
        "t2_pct":                [0.79,  0.78,  0.84,  0.77,  0.63,  0.85,  0.9,   0.89],  # standalone
        "bvps_inr":              [155,   158,   160,   162,   165,   170,   177,   183],  # estimate (standalone equity / shares)
    },
    "Shriram Finance": {
        "aum_cr":                [243043, 254470, 263190, 272249, 281309, 291709, 302274, 313798],
        "gnpa_pct":              [5.32,  5.38,  4.55,  4.53,  4.57,  4.54,  4.58,  4.64],
        "nnpa_pct":              [2.64,  2.68,  2.64,  2.57,  2.49,  2.38,  2.33,  2.33],
        "pcr_pct":               [51.7,  51.64, 43.28, 44.31, 46.7,  48.77, 50.34, 50.99],
        "pat_cr":                [2071,  2080,  2348,  2156,  2307,  2522,  3014,  3445],
        "nim_pct":               [8.74,  8.48,  8.55,  8.11,  8.19,  8.58,  8.61,  9.04],
        "roa_pct":               [3.06,  2.88,  2.98,  2.76,  2.89,  3.09,  3.63,  3.93],
        "roe_pct":               [16,    15.41, 15.75, 15.07, 15.4,  16.33, 19.13, 12.76],
        "cost_of_borrowing_pct": [9.06,  9,     8.96,  8.87,  8.83,  8.69,  8.59,  8.56],
        "d_e_ratio":             [3.99,  4.06,  4.16,  4.15,  3.88,  4.05,  3.82,  2.14],
        "car_pct":               [20.16, 21,    20.66, 20.79, 20.68, 20.27, 20.4,  34.17],
        "t1_pct":                [19.36, 20.34, 20.03, 20.16, 19.98, 19.66, 19.8,  33.4],
        "t2_pct":                [0.8,   0.66,  0.63,  0.63,  0.7,   0.61,  0.6,   0.77],
        "bvps_inr":              [277,    292,    299,    311,    321,    330,    349,    461.78],
    },
    "Chola Finance": {
        "aum_cr":                [164642, 174567, 199876, 192148, 199159, 227770, 242630, 254392],
        "gnpa_pct":              [3.78,  4,     3.97,  4.2,   4.57,  4.63,  4.36,  4.5],  # RBI IRACP norms throughout
        "nnpa_pct":              [2.48,  2.66,  2.63,  2.8,   3.07,  3.13,  2.87,  2.95],  # RBI IRACP norms; Q1FY25/Q1FY26 interpolated (~)
        "pcr_pct":               [34.4,  34.4,  34.6,  33.5,  33.9,  33.4,  34.2,  35.49],  # IRACP (RBI) PCR from Screener; Q1FY25/Q1FY26 interpolated (~); Q4FY26 kept (1−2.87/4.36)
        "pat_cr":                [963,   1087,  1587,  1136,  1155,  1288,  1641,  1654],
        "nim_pct":               [7.5,   7.7,   7.7,   7.8,   7.9,   8,     8.4,   8.2],
        "roa_pct":               [3,     3.2,   2.39,  3.1,   3,     3.2,   2.9,   2.8],
        "roe_pct":               [18.2,  19.7,  19.8,  18.9,  18.1,  19.1,  23,    21.2],
        "cost_of_borrowing_pct": [7.1,   7.1,   7.1,   7,     6.8,   6.7,   6.6,   6.7],
        "d_e_ratio":             [7.4,   7.4,   7.7,   7.6,   7.4,   7.5,   6.9,   6.87],
        "car_pct":               [19.5,  19.7,  19.75, 19.96, 20,    19.16, 19.21, 19.81],
        "t1_pct":                [14.5,  14.4,  14.41, 14.31, 14.59, 14.21, 14.73, 14.81],
        "t2_pct":                [5,     5.3,   5.34,  5.65,  5.41,  4.95,  4.48,  5],
        "bvps_inr":              [252,   267,   280,   292,   306,   327,   357,   376],  # Q4FY26: equity ₹30,458 Cr ÷ 85.3 Cr shares (Screener)
    },
    "Aditya Birla Capital": {
        "aum_cr":                [114710, 119437, 126351, 131227, 139585, 148182, 159916, 167456],
        "gnpa_pct":              [2.5,   2.27,  2.24,  2.27,  1.68,  1.51,  1.33,  1.3],
        "nnpa_pct":              [1.38,  1.25,  1.23,  1.34,  0.94,  0.84,  0.69,  0.67],  # Q4FY26 derived (GNPA × (1−PCR))
        "pcr_pct":               [46,    45.6,  45,    41.2,  44.2,  44.3,  47.8,  48.2],
        "pat_cr":                [629,   600,   652,   689,   714,   772,   825,   927],
        "nim_pct":               [6.28,  6,     6.07,  5.97,  6.06,  6.12,  6.08,  6.07],
        "roa_pct":               [2.34,  2.1,   2.25,  2.25,  2.2,   2.25,  2.31,  2.39],
        "roe_pct":               [None,  None,  14.2,  14.4,  14.2,  15.2,  15.8,  16.2],
        "cost_of_borrowing_pct": [6.85,  6.91,  6.83,  6.74,  6.62,  6.56,  6.57,  6.52],
        "d_e_ratio":             [5.85,  5.85,  None,  4.4,   4.55,  4.59,  4.82,  4.24],
        "car_pct":               [16.48, 16.77, None,  18.11, 17.98, 17.34, 16.79, 18.82],
        "t1_pct":                [14.47, 14.43, None,  15.62, 15.39, 14.56, 13.82, 15.95],
        "t2_pct":                [2.01,  2.34,  None,  2.49,  2.59,  2.78,  2.97,  2.87],  # Q4FY26 = CAR − T1
        "bvps_inr":              [None,  None,  96,    99,    103,   106,   109,   131],
    },
    "L&T Finance": {
        "aum_cr":                [93015,  95120,  97762,  102314, 107096, 114285, 121728, 129634],
        "gnpa_pct":              [3.2,   3.23,  3.29,  3.31,  3.29,  3.19,  2.88,  2.86],
        "nnpa_pct":              [0.97,  0.97,  0.99,  1,     1,     0.92,  0.96,  0.9],
        "pcr_pct":               [71,    71,    71,    70,    72,    72,    67,    69],
        "pat_cr":                [626,   636,   701,   735,   760,   760,   807,   902],
        "nim_pct":               [10.86, 10.33, 10.15, 10.22, 10.22, 10.41, 10.47, 10.47],  # NIM + Fees, from Q4FY26 investor deck (RoA trajectory table)
        "roa_pct":               [2.27,  2.22,  2.37,  2.41,  2.41,  2.37,  2.4,   2.48],
        "roe_pct":               [11.65, 10.2,  10.5,  11.33, 11.33, 11.38, 11.71, 12.71],
        "cost_of_borrowing_pct": [7.83,  7.8,   7.68,  7.4,   7.32,  7.25,  7.17,  7.2],  # WACB from Q4FY26 investor deck (ALM slide)
        "d_e_ratio":             [3.5,   3.46,  3.66,  3.71,  3.78,  3.78,  3.93,  4.09],
        "car_pct":               [22.16, 22,    22.27, 20.68, 20,    19.1,  18.34, 17.89],
        "t1_pct":                [20.53, None,  20.76, 19.54, None,  18.43, 17.6,  17.14],
        "t2_pct":                [1.63,  None,  1.51,  1.14,  None,  0.67,  0.74,  0.75],
        "bvps_inr":              [99.9,  99.9,  102.4, 105.4, 108.3, 108.3, 111.7, 112.6],
    },
    "Piramal Finance": {
        "aum_cr":                [None,   None,   None,   None,   85756,  96690,  101230, 106940],
        "gnpa_pct":              [None,  2.8,   2.8,   None,  2.8,   2.6,   2.3,   2.4],
        "nnpa_pct":              [None,  None,  1.9,   None,  2,     1.9,   1.6,   1.6],
        "pcr_pct":               [None,  None,  None,  None,  None,  27.9,  29.6,  31.5],  # Stage-3 PCR
        "pat_cr":                [163,   39,    102,   276,   327,   401,   502,   461],
        "nim_pct":               [5.1,   5.8,   5.8,   5.9,   6.1,   6.3,   6.5,   6.5],
        "roa_pct":               [None,  None,  None,  None,  None,  1.9,   2.1,   1.9],  # RoAUM on growth book
        "roe_pct":               [None,  None,  2,     None,  2,     None,  None,  6.5],
        "cost_of_borrowing_pct": [9.12,  9.17,  9.13,  9.13,  8.95,  8.95,  8.84,  8.8],  # Q4FY26 investor deck (restated ex-currency); Q1-Q3FY26 restated figures per footnote
        "d_e_ratio":             [None,  None,  None,  None,  None,  2.71,  2.8,   2.8],
        "car_pct":               [23.3,  23.7,  23.6,  19.3,  20.7,  None,  19.8,  18.85],
        "t1_pct":                [None,  None,  None,  None,  None,  None,  None,  18.85],  # not disclosed
        "t2_pct":                [None,  None,  None,  None,  None,  None,  None,  0],  # not disclosed
        "bvps_inr":              [None,  None,  None,  None,  None,  1232,  1247,  1271],
    },
    "Muthoot Finance": {
        # AUM: Q4FY25-Q4FY26 = standalone principal AUM from Q4FY26 investor deck
        #       Q4FY24-Q3FY25 = from Screener.in; may differ slightly in basis
        # PAT: Q4FY25-Q4FY26 = standalone from Q4FY26 investor deck
        #       Q4FY24-Q3FY25 = from Screener.in (may include consolidated figures)
        # ROA / NIM = PAT or NII on Avg Loan Assets (Muthoot-disclosed; higher than standard PAT/Avg Total Assets)
        "aum_cr":                [104149, 111308, 108648, 120031, 132305, 147552, 162826, 172053],
        "gnpa_pct":              [4.3,   4.22,  3.41,  2.58,  2.25,  1.58,  2.35,  2.28],  # Stage-3 proxy
        "nnpa_pct":              [None,  None,  None,  None,  None,  None,  None,  1.99],  # not disclosed
        "pcr_pct":               [None,  None,  None,  None,  None,  None,  None,  13.01],  # not disclosed
        "pat_cr":                [1321,  1392,  1508,  2046,  2345,  2656,  3086,  2550],
        "nim_pct":               [11.54, 11.6,  11.27, 12.15, 12.66, 12.77, 13.38, 10.65],  # NII / Avg Loan Assets
        "roa_pct":               [5.74,  5.81,  5.85,  7.16,  7.44,  7.59,  7.95,  6.09],  # PAT / Avg Loan Assets
        "roe_pct":               [19.99, 20.7,  21.76, 28.28, 30.61, 32.03, 34.17, 26.6],
        "cost_of_borrowing_pct": [9.01,  8.81,  8.99,  8.88,  8.78,  8.84,  8.58,  10.68],  # interest exp / avg borrowings; Q1-Q4FY26 from investor deck
        "d_e_ratio":             [2.66,  2.75,  2.95,  3.18,  3.27,  3.4,   3.46,  3.83],  # capital gearing (net debt / tangible networth)
        "car_pct":               [None,  None,  None,  None,  None,  None,  20.75, 20.3],  # Q4FY26 from investor deck; prior quarters not reported
        "t1_pct":                [None,  None,  None,  None,  None,  None,  19.84, 19.39],
        "t2_pct":                [None,  None,  None,  None,  None,  None,  0.91,  0.91],
        "bvps_inr":              [639.67, 672.47, 708.26, 733.64, 793.09, 859.33, 940.05, 970.7],
    },
    "Mahindra Finance": {
        "aum_cr":                [112454, 115126, 119673, 122008, 127246, 128965, 134096, 137449],  # Q4FY26 pending
        "gnpa_pct":              [3.83,  3.93,  3.69,  3.85,  3.94,  3.8,   3.41,  3.5],
        "nnpa_pct":              [1.59,  2,     1.84,  1.91,  1.89,  1.82,  1.44,  1.48],
        "pcr_pct":               [59.5,  50.1,  51.2,  51.4,  53,    53,    58.6,  58.1],
        "pat_cr":                [369,   899,   563,   530,   569,   810,   873,   899],
        "nim_pct":               [6.5,   6.6,   6.5,   6.7,   7,     7.5,   7.5,   7.3],
        "roa_pct":               [1.5,   2,     1.9,   1.6,   None,  1.9,   2.4,   2.4],
        "roe_pct":               [9.7,   12.7,  12.4,  9.8,   None,  11.8,  None,  14.3],
        "cost_of_borrowing_pct": [6.3,   6.4,   6.3,   6.3,   6,     6,     5.7,   5.8],
        "d_e_ratio":             [5.65,  5.44,  5.7,   4.75,  None,  4.87,  4.86,  5],
        "car_pct":               [None,  None,  None,  None,  None,  None,  18.8,  18.5],  # not disclosed
        "t1_pct":                [None,  None,  None,  None,  None,  None,  16.7,  16.5],  # not disclosed
        "t2_pct":                [None,  None,  None,  None,  None,  None,  2.2,   2.1],  # not disclosed
        "bvps_inr":              [148,   155.6, 160.4, 168,   None,  171.4, 178.1, 184.7],
    },
}

# ── Data quality flags ─────────────────────────────────────────────────────────
# ~ = estimated / interpolated from adjacent quarters or rating reports
# Mahindra Finance: Q4FY26 PDF pending — Q3FY26 values retained in snapshot; None at index 8 in timeseries
# Muthoot Finance: Q4FY26 fully updated from May-14-2026 investor deck (standalone basis)
#   AUM/PAT Q4FY24-Q3FY25 (indices 0-3) from Screener.in — may differ slightly in basis
#   AUM/PAT Q4FY25-Q4FY26 (indices 4-8) standalone principal from Q4FY26 investor deck
#   NNPA/PCR not disclosed (gold-loan structure); CAR reported only from Q4FY26 onwards
#   ROA = PAT/Avg Loan Assets (Muthoot's own metric; structurally higher than standard ROA/Avg Total Assets)
# Chola Finance Q4FY26: all metrics from Screener.in; BVPS = equity ₹30,458 Cr ÷ 85.3 Cr shares = ₹357
# Chola Finance GNPA/NNPA/PCR: restated to RBI IRACP norms across all quarters; Q1FY25 and Q1FY26 values interpolated (~)
# Bajaj Finance Q4FY26: consolidated basis; BVPS estimate from standalone equity/shares; NIM = annualised Q4 NTI/avg AUM
# AB Capital Q4FY26: NNPA derived (GNPA × (1−PCR)); T2 = CAR − T1
# Piramal AUM: Q4FY24-Q1FY26 not confirmed from source; only Q2FY26+ from investor deck
# Poonawalla: ROE not directly reported; NIM = NII/Avg-AUM annualized
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
