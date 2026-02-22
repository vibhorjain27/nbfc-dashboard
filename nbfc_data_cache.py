# NBFC Peer Data Cache
# Source: Screener.in investor presentations
# Period: Q3 FY26 (Oct–Dec 2025) — latest available quarter
# Last updated: Feb 2026
# Notes:
#   - Piramal ROA = RoAUM on Growth Business (not consolidated ROA)
#   - Muthoot GNPA = Stage-3 proxy; NNPA not separately disclosed
#   - Bajaj NIM not explicitly disclosed; ROA/ROE are annualized
#   - Mahindra ROA/ROE = 9M FY26 annualized; D/E = 9M FY26
#   - Poonawalla ROE = not reported; NIM not disclosed in quarterly press releases
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
