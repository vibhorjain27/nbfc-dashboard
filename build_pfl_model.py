#!/usr/bin/env python3
"""
Poonawalla Fincorp (PFL) Financial Model Builder
Sources: Q4FY26 Investor Presentation (May 2026) + Q3FY26 Investor Presentation (Jan 2026)
Output:  pfl_financial_model.xlsx
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, LineChart, Reference

wb = openpyxl.Workbook()

# ── Palette ──────────────────────────────────────────────────────────────────
NAVY   = "0A2540"
BLUE   = "1E40AF"
LBLUE  = "DBEAFE"
XBLUE  = "EFF6FF"
GREEN  = "15803D"
LGREEN = "DCFCE7"
RED    = "B91C1C"
LRED   = "FEE2E2"
AMBER  = "92400E"
LAMBER = "FEF3C7"
GRAY   = "374151"
LGRAY  = "F9FAFB"
MGRAY  = "E5E7EB"
WHITE  = "FFFFFF"
YELLOW = "FDE047"

# ── Style helpers ─────────────────────────────────────────────────────────────
def F(bold=False, color=NAVY, size=9, italic=False):
    return Font(name="Calibri", bold=bold, color=color, size=size, italic=italic)

def FILL(c): return PatternFill("solid", fgColor=c)

def B(style="thin"):
    s = Side(style=style)
    return Border(left=s, right=s, top=s, bottom=s)

def A(h="center", v="center", wrap=False, indent=0):
    return Alignment(horizontal=h, vertical=v, wrap_text=wrap, indent=indent)

def cell(ws, r, c, val=None, bold=False, color=NAVY, size=9, fill=None,
         align_h="center", align_v="center", wrap=False, indent=0,
         border=None, fmt=None, italic=False):
    cl = ws.cell(row=r, column=c, value=val)
    cl.font = Font(name="Calibri", bold=bold, color=color, size=size, italic=italic)
    cl.alignment = Alignment(horizontal=align_h, vertical=align_v,
                             wrap_text=wrap, indent=indent)
    if fill:   cl.fill   = FILL(fill)
    if border: cl.border = B(border)
    if fmt:    cl.number_format = fmt
    return cl

def merge(ws, r1, c1, r2, c2, val=None, bold=False, color=NAVY, size=9,
          fill=None, align_h="center", align_v="center", wrap=False, fmt=None):
    ws.merge_cells(start_row=r1, start_column=c1, end_row=r2, end_column=c2)
    cl = ws.cell(row=r1, column=c1, value=val)
    cl.font = Font(name="Calibri", bold=bold, color=color, size=size)
    cl.alignment = Alignment(horizontal=align_h, vertical=align_v, wrap_text=wrap)
    if fill: cl.fill = FILL(fill)
    if fmt:  cl.number_format = fmt
    return cl

def col_w(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

def row_h(ws, heights):
    for r, h in heights.items():
        ws.row_dimensions[r].height = h

def hide_gridlines(ws):
    ws.sheet_view.showGridLines = False

# Number formats
PCT  = "0.0%"
PCT2 = "0.00%"
CR0  = '#,##0'
CR1  = '#,##0.0'
XFMT = '0.00"x"'
RS   = '"₹"#,##0'
EPS  = '"₹"#,##0.00'

# ─────────────────────────────────────────────────────────────────────────────
# SHEET 1 — COVER
# ─────────────────────────────────────────────────────────────────────────────
ws_cov = wb.active
ws_cov.title = "Cover"
hide_gridlines(ws_cov)
col_w(ws_cov, [2, 18, 14, 14, 14, 14, 14, 14, 14, 14, 2])
row_h(ws_cov, {1:8, 2:10, 3:45, 4:28, 5:24, 6:20, 7:16, 8:42, 9:16,
               10:16, 11:60, 12:16, 13:40, 14:40, 15:40, 16:40, 17:16,
               18:40, 19:40, 20:16, 21:16})

# Banner
merge(ws_cov, 3, 2, 3, 10, "POONAWALLA FINCORP LIMITED",
      bold=True, color=WHITE, size=24, fill=NAVY, align_h="center")
merge(ws_cov, 4, 2, 4, 10, "Financial Model & Projections  |  FY27E – FY30E",
      bold=False, color="93C5FD", size=13, fill=NAVY, align_h="center")
merge(ws_cov, 5, 2, 5, 10, "Data Sources: Q4FY26 Investor Presentation (May 2026)  |  Q3FY26 Investor Presentation (Jan 2026)  |  Built: May 2026",
      bold=False, color="64748B", size=9, fill=NAVY, align_h="center")

# KPI row
kpis = [
    ("AUM\n(FY26A)", "₹60,348 Cr", LBLUE, BLUE),
    ("PAT\n(FY26A)", "₹542 Cr", LGREEN, GREEN),
    ("ROA\n(Q4FY26 ann.)", "1.81%", LGREEN, GREEN),
    ("GNPA\n(Mar-26)", "1.44%", LAMBER, AMBER),
    ("D/E Post-QIP\n(Apr-26)", "3.78x", LBLUE, BLUE),
    ("AUM CAGR\nTarget", "35–40%", LGREEN, GREEN),
    ("Rating\nCRISIL/CARE", "AAA/A1+", LBLUE, BLUE),
    ("QIP\n(Apr-26)", "₹2,500 Cr", LGREEN, GREEN),
]
for i, (lbl, val, bg, fg) in enumerate(kpis):
    col = 2 + i
    merge(ws_cov, 8, col, 8, col, f"{lbl}\n{val}",
          bold=True, color=fg, size=10, fill=bg, align_h="center", wrap=True)
    ws_cov.cell(8, col).border = B()

# Spacer
merge(ws_cov, 9, 2, 9, 10, "", fill=WHITE)

# Section: About
merge(ws_cov, 10, 2, 10, 10, "COMPANY OVERVIEW",
      bold=True, color=WHITE, size=10, fill=NAVY, align_h="left")
about = [
    ("Business", "India's fastest-growing NBFC; retail-focused lender across 13 product categories including personal loans, LAP, vehicle finance, education, and SME lending"),
    ("Promoter", "Adar Poonawalla (Serum Institute of India chairman). MD & CEO: Arvind Kapil (ex-HDFC Bank Group Head, Mortgages)"),
    ("Strategy", '"Solidify → Expand → Scale" roadmap. FY25: cleanup & rebuild. FY26: expand. FY27+: scale with 35-40% AUM CAGR target'),
    ("Listing", "NSE/BSE. Market cap ~₹30,000 Cr. ~81 Cr shares outstanding (FV ₹2). Credit rating: AAA (CRISIL/CARE)"),
    ("Key Edge", "Digital-first (10-second loan approvals), HDFC Bank DNA leadership, AAA-rated borrower, QIP-strengthened capital"),
]
for i, (k, v) in enumerate(about):
    r = 11 + i
    cell(ws_cov, r, 2, k, bold=True, color=WHITE, fill=BLUE, align_h="left",
         align_v="center", border="thin", indent=1)
    merge(ws_cov, r, 3, r, 10, v, bold=False, color=NAVY, size=9,
          fill=XBLUE, align_h="left")
    ws_cov.cell(r, 3).border = B()

# Model sheet index
merge(ws_cov, 17, 2, 17, 10, "MODEL NAVIGATION",
      bold=True, color=WHITE, size=10, fill=NAVY, align_h="left")
tabs = [
    ("Assumptions", "All key input parameters — Base / Bull / Bear scenarios per year"),
    ("Historical P&L", "Quarterly & annual P&L for FY25A and FY26A (actuals from presentations)"),
    ("Historical BS", "Balance sheet snapshots: Dec-24, Mar-25, Sep-25, Dec-25, Mar-26"),
    ("P&L Projections", "Projected income statements FY27E–FY30E across 3 scenarios"),
    ("BS Projections", "Projected balance sheets FY27E–FY30E"),
    ("Ratio Dashboard", "All key operating & financial ratios historical + projected"),
    ("Valuation", "P/BV, P/E multiples + DCF-based intrinsic value estimate"),
    ("Scenario Summary", "One-page Bull / Base / Bear comparison table"),
]
tab_colors = [LBLUE, LGREEN, LBLUE, LGREEN, LBLUE, LGREEN, LAMBER, LAMBER]
for i, (tab, desc) in enumerate(tabs):
    r = 18 + i
    cell(ws_cov, r, 2, tab, bold=True, color=BLUE, fill=tab_colors[i],
         align_h="left", border="thin", indent=1)
    merge(ws_cov, r, 3, r, 10, desc, color=GRAY, size=9,
          fill=LGRAY, align_h="left")
    ws_cov.cell(r, 3).border = B("hair")

# ─────────────────────────────────────────────────────────────────────────────
# SHEET 2 — ASSUMPTIONS
# ─────────────────────────────────────────────────────────────────────────────
ws_ass = wb.create_sheet("Assumptions")
hide_gridlines(ws_ass)
col_w(ws_ass, [1, 38, 13, 13, 13, 13, 13, 13, 13, 1])
row_h(ws_ass, {1: 8, 2: 30})

# Title
merge(ws_ass, 1, 2, 1, 9, "KEY MODEL ASSUMPTIONS  |  All monetary values in ₹ Crore",
      bold=True, color=WHITE, size=11, fill=NAVY)

# Column headers
hdrs = ["Parameter", "FY26A\n(Actual)", "FY27E\nBase", "FY27E\nBull", "FY27E\nBear",
        "FY28E\nBase", "FY29E\nBase", "FY30E\nBase"]
for i, h in enumerate(hdrs):
    c = ws_ass.cell(row=2, column=i+2, value=h)
    c.font = Font(name="Calibri", bold=True, color=WHITE, size=9)
    c.fill = FILL(BLUE if i != 3 else GREEN if i != 4 else RED)
    if h == "FY27E\nBull":
        c.fill = FILL("065F46")
    elif h == "FY27E\nBear":
        c.fill = FILL(RED)
    else:
        c.fill = FILL(NAVY)
    c.alignment = A(wrap=True)
    c.border = B()

# Note row
merge(ws_ass, 3, 2, 3, 9,
      "⚠  Yellow = input cells you can change. All projections in P&L/BS/Ratios sheets pull from here.",
      bold=False, color=AMBER, size=9, fill=LAMBER, align_h="left")

def ass_section(ws, row, title):
    merge(ws, row, 2, row, 9, f"  {title}",
          bold=True, color=WHITE, size=9, fill=GRAY, align_h="left")

def ass_row(ws, row, label, vals, fmts, bold=False, calculated=False):
    bg = LGRAY if calculated else YELLOW
    c = ws.cell(row=row, column=2, value=label)
    c.font = Font(name="Calibri", bold=bold, color=NAVY, size=9)
    c.alignment = A("left", indent=1)
    c.border = B("hair")
    c.fill = FILL(MGRAY if bold else WHITE)
    for i, (v, fmt) in enumerate(zip(vals, fmts)):
        col = i + 3
        cl = ws.cell(row=row, column=col, value=v)
        cl.font = Font(name="Calibri", bold=bold, color=NAVY, size=9)
        cl.alignment = A()
        cl.border = B("hair")
        if fmt: cl.number_format = fmt
        # Color actual vs input vs calculated
        if i == 0:    cl.fill = FILL(MGRAY)  # FY26A actual
        elif calculated: cl.fill = FILL(LGRAY)
        elif i in (2, 3):  # Bull / Bear
            cl.fill = FILL(LGREEN if i == 2 else LRED)
        else:
            cl.fill = FILL("FFFDE7")  # input yellow

# ── AUM & Growth ─────────────────────────────────────────────────────────────
r = 4
ass_section(ws_ass, r, "1. AUM & GROWTH"); r += 1

ass_row(ws_ass, r, "AUM (₹ Cr) — Opening",
        [35631, 60348, 60348, 60348, None, None, None],
        [CR0]*7, calculated=True); r += 1
ass_row(ws_ass, r, "AUM Growth (YoY %)",
        [0.694, 0.370, 0.400, 0.280, 0.300, 0.250, 0.220],
        [PCT]*7); r += 1
ass_row(ws_ass, r, "AUM (₹ Cr) — Closing [=prior × (1+growth)]",
        [60348, None, None, None, None, None, None],
        [CR0, "* calc *", "* calc *", "* calc *", "* calc *", "* calc *", "* calc *"],
        bold=True, calculated=True); r += 1
ass_row(ws_ass, r, "On-BS Loans / AUM (%)",
        [0.927, 0.920, 0.920, 0.920, 0.915, 0.910, 0.905],
        [PCT]*7); r += 1

# ── Yield & Spread ────────────────────────────────────────────────────────────
ass_section(ws_ass, r, "2. YIELD & SPREAD"); r += 1
ass_row(ws_ass, r, "Gross Yield on Loans (%)",
        [0.142, 0.138, 0.140, 0.136, 0.133, 0.129, 0.125],
        [PCT2]*7); r += 1
ass_row(ws_ass, r, "Cost of Borrowing (%)",
        [0.0763, 0.0740, 0.0725, 0.0760, 0.0710, 0.0685, 0.0660],
        [PCT2]*7); r += 1
ass_row(ws_ass, r, "  → Spread (Gross Yield – CoB) — derived",
        [None]*7, [PCT2]*7, calculated=True); r += 1
ass_row(ws_ass, r, "Fee & Other Income / AUM (%)",
        [0.0154, 0.0165, 0.0180, 0.0148, 0.0178, 0.0192, 0.0205],
        [PCT2]*7); r += 1
ass_row(ws_ass, r, "  (Cross-sell + Servicing + Gains on derecognition)",
        [None]*7, [None]*7, calculated=True); r += 1

# ── Efficiency ────────────────────────────────────────────────────────────────
ass_section(ws_ass, r, "3. OPERATING EFFICIENCY"); r += 1
ass_row(ws_ass, r, "Opex / Average AUM (%)",
        [0.0347, 0.0365, 0.0355, 0.0390, 0.0330, 0.0305, 0.0285],
        [PCT2]*7); r += 1
ass_row(ws_ass, r, "Cost-to-Income Ratio (%) — reference only",
        [0.520, 0.460, 0.440, 0.495, 0.415, 0.375, 0.350],
        [PCT]*7, calculated=True); r += 1

# ── Asset Quality ─────────────────────────────────────────────────────────────
ass_section(ws_ass, r, "4. ASSET QUALITY"); r += 1
ass_row(ws_ass, r, "Credit Cost / Average AUM (%)",
        [0.0201, 0.0210, 0.0175, 0.0255, 0.0175, 0.0155, 0.0140],
        [PCT2]*7); r += 1
ass_row(ws_ass, r, "GNPA (%)",
        [0.0144, 0.0128, 0.0105, 0.0155, 0.0105, 0.0085, 0.0070],
        [PCT2]*7); r += 1
ass_row(ws_ass, r, "NNPA (%)",
        [0.0074, 0.0062, 0.0048, 0.0078, 0.0048, 0.0038, 0.0030],
        [PCT2]*7); r += 1
ass_row(ws_ass, r, "Provision Coverage Ratio (%)",
        [0.490, 0.515, 0.540, 0.495, 0.540, 0.555, 0.570],
        [PCT]*7); r += 1

# ── Capital ───────────────────────────────────────────────────────────────────
ass_section(ws_ass, r, "5. CAPITAL & LEVERAGE"); r += 1
ass_row(ws_ass, r, "Opening Equity (₹ Cr) — Mar-26 + QIP",
        [8124, 12798, 12798, 12798, None, None, None],
        [CR0]*7, calculated=True); r += 1
ass_row(ws_ass, r, "  QIP Apr-26 (₹ Cr)",
        [0, 2500, 2500, 2500, 0, 0, 0],
        [CR0]*7); r += 1
ass_row(ws_ass, r, "Dividend Payout Ratio (%)",
        [0.00, 0.00, 0.00, 0.00, 0.05, 0.10, 0.10],
        [PCT]*7); r += 1
ass_row(ws_ass, r, "Target Leverage — Debt/Equity (x)",
        [3.78, 4.00, 3.80, 4.20, 4.00, 3.80, 3.60],
        [XFMT]*7); r += 1
ass_row(ws_ass, r, "Capital Adequacy Ratio — CAR (%)",
        [0.1683, 0.172, 0.178, 0.167, 0.178, 0.183, 0.188],
        [PCT]*7); r += 1

# ── Tax & Misc ────────────────────────────────────────────────────────────────
ass_section(ws_ass, r, "6. TAX & SHARES"); r += 1
ass_row(ws_ass, r, "Effective Tax Rate (%)",
        [0.252, 0.252, 0.252, 0.252, 0.252, 0.252, 0.252],
        [PCT]*7); r += 1
ass_row(ws_ass, r, "Shares Outstanding (Cr) — pre-QIP 81 Cr",
        [81.0, 87.6, 87.6, 87.6, 87.6, 87.6, 87.6],
        [CR1]*7); r += 1
ass_row(ws_ass, r, "  QIP shares issued @ ₹380/share (approx.)",
        [0, 6.6, 6.6, 6.6, 0, 0, 0],
        [CR1]*7, calculated=True); r += 1

# ── Valuation multiples ───────────────────────────────────────────────────────
ass_section(ws_ass, r, "7. VALUATION REFERENCE MULTIPLES"); r += 1
ass_row(ws_ass, r, "P/BV Multiple (x) — Base target",
        [None, 2.5, 3.0, 2.0, 2.8, 3.0, 3.2],
        [XFMT]*7); r += 1
ass_row(ws_ass, r, "P/E Multiple (x) — Base target",
        [None, 22, 25, 18, 20, 18, 16],
        [XFMT]*7); r += 1
ass_row(ws_ass, r, "Risk-Free Rate (%) — for DCF",
        [None, 0.068, 0.068, 0.068, 0.068, 0.068, 0.068],
        [PCT2]*7); r += 1
ass_row(ws_ass, r, "Cost of Equity (%) — CAPM estimate",
        [None, 0.130, 0.130, 0.130, 0.130, 0.130, 0.130],
        [PCT2]*7); r += 1
ass_row(ws_ass, r, "Terminal Growth Rate (%) — for DCF",
        [None, 0.050, 0.060, 0.040, 0.050, 0.050, 0.050],
        [PCT2]*7); r += 1

# Notes
r += 1
merge(ws_ass, r, 2, r, 9,
      "NOTES:  FY26A data sourced from Q4FY26 & Q3FY26 Investor Presentations. "
      "FY22-FY24 historical data requires Annual Report (not yet uploaded). "
      "Bull = upside scenario; Bear = downside scenario for FY27 only.",
      bold=False, color=GRAY, size=8, fill=LGRAY, align_h="left")

# ─────────────────────────────────────────────────────────────────────────────
# SHEET 3 — HISTORICAL P&L
# ─────────────────────────────────────────────────────────────────────────────
ws_pl = wb.create_sheet("Historical P&L")
hide_gridlines(ws_pl)
col_w(ws_pl, [1, 34, 1, 12, 12, 12, 12, 1, 12, 12, 12, 12, 1, 14, 14, 1])
row_h(ws_pl, {1: 8, 2: 28, 3: 40, 4: 16})

merge(ws_pl, 1, 2, 1, 15,
      "HISTORICAL PROFIT & LOSS STATEMENT  |  ₹ Crore  |  Source: Q4FY26 & Q3FY26 Investor Presentations",
      bold=True, color=WHITE, size=11, fill=NAVY)

# Quarter labels
merge(ws_pl, 2, 4, 2, 7, "FY25 (Quarters)", bold=True, color=WHITE, size=9, fill=BLUE)
merge(ws_pl, 2, 9, 2, 12, "FY26 (Quarters)", bold=True, color=WHITE, size=9, fill=BLUE)
merge(ws_pl, 2, 14, 2, 15, "Annual Totals", bold=True, color=WHITE, size=9, fill=GREEN)

cols_fy25_q = ["Q1FY25\nApr-Jun 24", "Q2FY25\nJul-Sep 24", "Q3FY25\nOct-Dec 24", "Q4FY25\nJan-Mar 25"]
cols_fy26_q = ["Q1FY26\nApr-Jun 25", "Q2FY26\nJul-Sep 25", "Q3FY26\nOct-Dec 25", "Q4FY26\nJan-Mar 26"]
cols_ann    = ["FY25A\n(Full Year)", "FY26A\n(Full Year)"]

for i, h in enumerate(["Particulars (₹ Cr)"] + [""] + cols_fy25_q + [""] + cols_fy26_q + [""] + cols_ann):
    if h == "": continue
    ci = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15][i] if i < 14 else i+2
    c = ws_pl.cell(row=3, column=[2, 4, 5, 6, 7, 9, 10, 11, 12, 14, 15][
        [0,1,2,3,4,5,6,7,8,9,10].index(i) if i < 11 else 9], value=h)

# Redo headers cleanly
all_cols = [
    (2,  "Particulars (₹ Cr)", NAVY, True),
    (4,  "Q1FY25\nApr-Jun 24", GRAY, False),
    (5,  "Q2FY25\nJul-Sep 24", GRAY, False),
    (6,  "Q3FY25\nOct-Dec 24", BLUE, True),
    (7,  "Q4FY25\nJan-Mar 25", BLUE, True),
    (9,  "Q1FY26\nApr-Jun 25", BLUE, True),
    (10, "Q2FY26\nJul-Sep 25", BLUE, True),
    (11, "Q3FY26\nOct-Dec 25", BLUE, True),
    (12, "Q4FY26\nJan-Mar 26", NAVY, True),
    (14, "FY25A\n(Full Year)", GREEN, True),
    (15, "FY26A\n(Full Year)", GREEN, True),
]
for col, text, bg, bold in all_cols:
    c = ws_pl.cell(row=3, column=col, value=text)
    c.font = Font(name="Calibri", bold=bold, color=WHITE, size=9)
    c.fill = FILL(bg)
    c.alignment = A(wrap=True)
    c.border = B()

# Divider cols
for dc in [3, 8, 13]:
    ws_pl.column_dimensions[get_column_letter(dc)].width = 0.5
    ws_pl.cell(3, dc).fill = FILL(MGRAY)

NA = "—"  # Not available / to be sourced from Annual Report

# P&L data rows
# Format: (label, bold, is_section, Q1FY25, Q2FY25, Q3FY25, Q4FY25, Q1FY26, Q2FY26, Q3FY26, Q4FY26, FY25A, FY26A, fmt)
pl_rows = [
    # INCOME
    ("INCOME", True, True, None, None, None, None, None, None, None, None, None, None, None),
    ("Total Interest Income", False, False,
     NA, NA, 999, 1068, 1180, 1402, 1660, 1894,
     NA, 6136, CR0),
    ("  Interest Expenses", False, False,
     NA, NA, 385, 458, 515, 638, 739, 844,
     NA, 2736, CR0),
    ("Net Interest Income (NII — pure)", True, False,
     NA, NA, 614, 610, 665, 764, 921, 1050,
     NA, 3400, CR0),
    ("  Cross-sell Income", False, False,
     NA, NA, 23, 36, 36, 68, 70, 72,
     NA, 246, CR0),
    ("  Servicing Income", False, False,
     NA, NA, 35, 34, 33, 37, 47, 67,
     NA, 184, CR0),
    ("  Net Gain on Derecognition", False, False,
     NA, NA, None, 27, 34, 35, 41, 78,
     NA, 188, CR0),
    ("  Other Income", False, False,
     NA, NA, None, 7, None, None, None, 9,
     NA, None, CR0),
    ("NII incl. Fees & Other Income", True, False,
     NA, NA, 672, 715, 768, 905, 1080, 1276,
     NA, 4029, CR0),
    # EXPENSES
    ("EXPENSES", True, True, None, None, None, None, None, None, None, None, None, None, None),
    ("Operating Expenses (Opex)", False, False,
     NA, NA, 299, 382, 443, 518, 552, 582,
     NA, 2095, CR0),
    # PROFITABILITY
    ("PROFITABILITY", True, True, None, None, None, None, None, None, None, None, None, None, None),
    ("Pre-Provision Operating Profit (PPoP)", True, False,
     NA, NA, 373, 333, 325, 387, 528, 695,
     NA, 1935, CR0),
    ("  Credit Cost / Provisions", False, False,
     NA, NA, 348, 253, 242, 288, 328, 354,
     NA, 1212, CR0),
    ("Profit Before Tax (PBT)", True, False,
     NA, NA, 25, 80, 83, 99, 200, 341,
     NA, 723, CR0),
    ("  Tax", False, False,
     NA, NA, 6, 18, 20, 25, 50, 86,
     NA, 181, CR0),
    ("Profit After Tax (PAT)", True, False,
     NA, NA, 19, 62, 63, 74, 150, 255,
     NA, 542, CR0),
    # KEY RATIOS
    ("KEY OPERATING RATIOS", True, True, None, None, None, None, None, None, None, None, None, None, None),
    ("AUM (₹ Cr) — end of quarter", False, False,
     NA, NA, 30984, 35631, 41273, 47701, 55017, 60348,
     35631, 60348, CR0),
    ("ROA (annualised %)", False, False,
     NA, NA, 0.0026, 0.0078, 0.0068, 0.0069, 0.0120, 0.0181,
     NA, 0.0114, PCT2),
    ("Opex / Average AUM (%)", False, False,
     NA, NA, 0.041, 0.0476, 0.048, 0.0481, 0.0441, 0.0413,
     NA, 0.0347, PCT2),
    ("Cost to Income Ratio (%)", False, False,
     NA, NA, 0.445, 0.534, 0.577, 0.573, 0.511, 0.456,
     NA, 0.520, PCT2),
    ("Credit Cost / Average AUM (%)", False, False,
     NA, NA, 0.048, 0.031, 0.026, 0.027, 0.026, 0.025,
     NA, 0.0201, PCT2),
    ("Cost of Borrowing (%)", False, False,
     NA, NA, 0.0806, 0.0807, 0.0804, 0.0769, 0.0765, 0.0763,
     NA, 0.0763, PCT2),
    ("NIM (NII pure / Avg AUM, annualised %)", False, False,
     NA, NA, None, None, None, None, None, 0.073,
     NA, None, PCT2),
    ("GNPA (%)", False, False,
     NA, NA, 0.0185, 0.0184, 0.0184, 0.0159, 0.0151, 0.0144,
     NA, 0.0144, PCT2),
    ("NNPA (%)", False, False,
     NA, NA, 0.0081, 0.0085, 0.0085, 0.0081, 0.0080, 0.0074,
     NA, 0.0074, PCT2),
    ("PCR (%)", False, False,
     NA, NA, 0.5679, 0.5447, 0.5393, 0.4965, 0.4775, 0.490,
     NA, 0.490, PCT2),
    ("PBT (₹ Cr)", False, False,
     NA, NA, 25, 80, 83, 99, 200, 341,
     NA, 723, CR0),
    ("PAT (₹ Cr)", True, False,
     NA, NA, 19, 62, 63, 74, 150, 255,
     NA, 542, CR0),
]

r = 4
bg_section = LGRAY
for row_data in pl_rows:
    label, bold, is_section = row_data[0], row_data[1], row_data[2]
    vals = list(row_data[3:12])  # Q1FY25..Q4FY26 (9 vals, but we have Q1-Q4 for both = 8)
    # Actually: Q1FY25, Q2FY25, Q3FY25, Q4FY25, Q1FY26, Q2FY26, Q3FY26, Q4FY26, FY25A, FY26A
    data_vals = row_data[3:13]
    fmt = row_data[13]
    col_map = [4, 5, 6, 7, 9, 10, 11, 12, 14, 15]

    if is_section:
        merge(ws_pl, r, 2, r, 15, f"  {label}",
              bold=True, color=WHITE, size=9, fill=GRAY, align_h="left")
        r += 1
        continue

    c = ws_pl.cell(row=r, column=2, value=label)
    c.font = Font(name="Calibri", bold=bold, color=NAVY, size=9)
    c.alignment = A("left", indent=1 if not bold else 0)
    c.border = B("hair")
    c.fill = FILL(MGRAY if bold else WHITE)

    for i, (dv, col) in enumerate(zip(data_vals, col_map)):
        cl = ws_pl.cell(row=r, column=col, value=dv)
        cl.font = Font(name="Calibri", bold=bold, color=NAVY, size=9)
        cl.alignment = A()
        cl.border = B("hair")
        if fmt and dv not in (None, NA): cl.number_format = fmt
        # Shading
        if col in (14, 15):  cl.fill = FILL(LGREEN if not bold else "A7F3D0")
        elif col in (4, 5):   cl.fill = FILL(LGRAY)   # Estimated
        elif col == 12:        cl.fill = FILL(LBLUE if not bold else "BFDBFE")
        else:                  cl.fill = FILL(WHITE)
        if dv == NA:
            cl.font = Font(name="Calibri", color="9CA3AF", size=9, italic=True)
            cl.value = "▪ AR req."
    r += 1

# Note row
merge(ws_pl, r+1, 2, r+1, 15,
      "▪ AR req. = Data requires Annual Report (FY22–FY24 and full FY25).  "
      "Q1FY25/Q2FY25 data estimated from public guidance & trend interpolation.  "
      "Q1FY26 interest income/expense are estimates; NII, PPoP, PAT are from presentation slides.",
      bold=False, color=GRAY, size=8, fill=LAMBER, align_h="left")

# ─────────────────────────────────────────────────────────────────────────────
# SHEET 4 — HISTORICAL BALANCE SHEET
# ─────────────────────────────────────────────────────────────────────────────
ws_bs = wb.create_sheet("Historical BS")
hide_gridlines(ws_bs)
col_w(ws_bs, [1, 36, 14, 14, 14, 14, 14, 14, 1])
row_h(ws_bs, {1: 8, 2: 28, 3: 36})

merge(ws_bs, 1, 2, 1, 8,
      "HISTORICAL BALANCE SHEET  |  ₹ Crore  |  Source: Q3FY26 & Q4FY26 Investor Presentations",
      bold=True, color=WHITE, size=11, fill=NAVY)

bs_date_hdrs = ["Particulars (₹ Cr)", "Dec-24\n(Q3FY25)", "Mar-25\n(FY25 End)",
                "Sep-25\n(Q2FY26)", "Dec-25\n(Q3FY26)", "Mar-26\n(FY26 End)"]
for i, h in enumerate(bs_date_hdrs):
    cl = ws_bs.cell(row=3, column=i+2, value=h)
    cl.font = Font(name="Calibri", bold=True, color=WHITE, size=9)
    cl.fill = FILL(NAVY if i in (0, 5) else BLUE)
    cl.alignment = A(wrap=True)
    cl.border = B()

bs_rows = [
    ("ASSETS", True, True, None, None, None, None, None),
    ("Cash & Bank Balances", False, False, 114, 32, 126, 306, 294),
    ("Receivables", False, False, 30, 19, 40, 42, 38),
    ("Loans (net)", True, False, 27962, 32695, 43910, 51107, 55951),
    ("Investments", False, False, 1215, 1256, 1656, 1456, 2490),
    ("Other Financial Assets", False, False, 199, 185, 345, 406, 677),
    ("Non-Financial Assets", False, False, 697, 707, 832, 876, 770),
    ("Total Assets", True, False, 30217, 34894, 46909, 54193, 60221),
    ("", False, True, None, None, None, None, None),
    ("LIABILITIES & EQUITY", True, True, None, None, None, None, None),
    ("Borrowings", True, False, 21338, 25881, 35717, 42498, 48098),
    ("  of which: Term Loans", False, False, None, None, None, None, None),
    ("  of which: NCDs", False, False, None, None, None, None, None),
    ("  of which: CP", False, False, None, None, None, None, None),
    ("  of which: CC/WCDL", False, False, None, None, None, None, None),
    ("  of which: ECB", False, False, None, None, None, None, None),
    ("  of which: Sub-Debt", False, False, None, None, None, None, None),
    ("Other Liabilities", False, False, 823, 889, 1369, 1699, 1825),
    ("Total Liabilities", True, False, 22161, 26770, 37086, 44197, 49923),
    ("", False, True, None, None, None, None, None),
    ("SHAREHOLDERS' EQUITY", True, True, None, None, None, None, None),
    ("Share Capital (FV ₹2)", False, False, 155, 155, 161, 162, 162),
    ("Reserves & Surplus", False, False, 7902, 7969, 9661, 9834, 10136),
    ("Total Equity", True, False, 8057, 8124, 9822, 9996, 10298),
    ("Total Liabilities + Equity", True, False, 30217, 34894, 46909, 54193, 60221),
    ("", False, True, None, None, None, None, None),
    ("KEY METRICS", True, True, None, None, None, None, None),
    ("AUM (₹ Cr)", False, False, 30984, 35631, 47701, 55017, 60348),
    ("Debt / Equity (x)", False, False,
     round(21338/8057, 2), round(25881/8124, 2),
     round(35717/9822, 2), round(42498/9996, 2), round(48098/10298, 2)),
    ("Post-QIP D/E (x) — Apr-26 QIP ₹2,500 Cr", False, False,
     None, None, None, None, 3.78),
    ("CAR (%)", False, False, None, None, None, 0.1817, 0.1683),
    ("Tier-1 CAR (%)", False, False, None, None, None, None, None),
    ("Liquidity (₹ Cr)", False, False, None, None, None, 6488, None),
    ("Book Value / Share (₹)", False, False,
     round(8057/81, 1), round(8124/81, 1),
     round(9822/81, 1), round(9996/81, 1), round(10298/81, 1)),
]

r = 4
for row_data in bs_rows:
    label, bold, is_section = row_data[0], row_data[1], row_data[2]
    vals = row_data[3:]

    if is_section:
        if label:
            merge(ws_bs, r, 2, r, 8, f"  {label}",
                  bold=True, color=WHITE, size=9, fill=GRAY, align_h="left")
        else:
            ws_bs.row_dimensions[r].height = 6
        r += 1
        continue

    cl = ws_bs.cell(row=r, column=2, value=label)
    cl.font = Font(name="Calibri", bold=bold, color=NAVY, size=9)
    cl.alignment = A("left", indent=1 if not bold else 0)
    cl.border = B("hair")
    cl.fill = FILL(MGRAY if bold else WHITE)

    for i, v in enumerate(vals):
        col = i + 3
        c2 = ws_bs.cell(row=r, column=col, value=v)
        c2.font = Font(name="Calibri", bold=bold, color=NAVY, size=9)
        c2.alignment = A()
        c2.border = B("hair")
        if v is not None:
            if isinstance(v, float) and v < 30:
                c2.number_format = PCT2 if v < 1 else XFMT
            elif isinstance(v, (int, float)):
                c2.number_format = CR1
        if col == 7:    c2.fill = FILL("BFDBFE" if bold else LBLUE)
        elif bold:      c2.fill = FILL(MGRAY)
        else:           c2.fill = FILL(WHITE)
    r += 1

# Borrowing mix note
merge(ws_bs, r+1, 2, r+1, 8,
      "BORROWING MIX (Q3FY26 — ₹42,498 Cr total):  "
      "Term Loans 38% | NCDs 28% | CC/WCDL 13% | CP 7% | ECB 7% | Sub-Debt 4% | Others 3%.  "
      "Banks 57% | Mutual Funds 23% | Insurance 8% | FII/FPI 5% | Others 7%",
      bold=False, color=GRAY, size=8, fill=LGRAY, align_h="left")

# ─────────────────────────────────────────────────────────────────────────────
# SHEET 5 — P&L PROJECTIONS
# ─────────────────────────────────────────────────────────────────────────────
ws_proj = wb.create_sheet("P&L Projections")
hide_gridlines(ws_proj)
col_w(ws_proj, [1, 36, 14, 1, 14, 14, 14, 1, 14, 1, 14, 1])
row_h(ws_proj, {1: 8, 2: 28, 3: 28})

merge(ws_proj, 1, 2, 1, 11,
      "PROJECTED P&L STATEMENTS  |  ₹ Crore  |  Base / Bull / Bear Scenarios",
      bold=True, color=WHITE, size=11, fill=NAVY)

merge(ws_proj, 2, 2, 2, 2, "Particulars (₹ Cr)", bold=True, color=WHITE, size=9, fill=NAVY)
merge(ws_proj, 2, 3, 2, 3, "FY26A\n(Actual)", bold=True, color=WHITE, size=9, fill=GRAY)
for j, (col, text, bg) in enumerate([
    (5, "FY27E — BASE", BLUE),   (6, "FY27E — BULL", "065F46"),   (7, "FY27E — BEAR", RED),
    (9, "FY28E — BASE", BLUE),   (11, "FY30E — BASE", NAVY),
]):
    c = ws_proj.cell(row=2, column=col, value=text)
    c.font = Font(name="Calibri", bold=True, color=WHITE, size=9)
    c.fill = FILL(bg)
    c.alignment = A(wrap=True)
    c.border = B()

# AUM assumptions for projections
# FY26A AUM = 60,348
# FY27E: Base +37%, Bull +40%, Bear +28%
# FY28E: Base +30%;  FY29E: +25%;  FY30E: +22%
AUM = {
    "FY26A": 60348,
    "FY27B": 60348 * 1.37,   # Base
    "FY27U": 60348 * 1.40,   # Bull
    "FY27D": 60348 * 1.28,   # Bear
    "FY28B": 60348 * 1.37 * 1.30,
    "FY29B": 60348 * 1.37 * 1.30 * 1.25,
    "FY30B": 60348 * 1.37 * 1.30 * 1.25 * 1.22,
}

def proj_pl(aum_open, aum_close, yield_pct, cob_pct, fee_pct, opex_pct, cc_pct, tax_rt,
            on_bs=0.920):
    avg_aum = (aum_open + aum_close) / 2
    avg_loans = avg_aum * on_bs
    avg_borrows = avg_loans * 0.86  # ~borrowings/loans ratio
    int_inc = avg_loans * yield_pct
    int_exp = avg_borrows * cob_pct
    nii_pure = int_inc - int_exp
    fee_inc = avg_aum * fee_pct
    nii_total = nii_pure + fee_inc
    opex = avg_aum * opex_pct
    ppop = nii_total - opex
    cc = avg_aum * cc_pct
    pbt = ppop - cc
    tax = pbt * tax_rt if pbt > 0 else 0
    pat = pbt - tax
    return {
        "int_inc": int_inc, "int_exp": int_exp, "nii_pure": nii_pure,
        "fee_inc": fee_inc, "nii_total": nii_total, "opex": opex,
        "ppop": ppop, "cc": cc, "pbt": pbt, "tax": tax, "pat": pat,
        "avg_aum": avg_aum, "aum": aum_close,
        "roa": pat / avg_aum if avg_aum > 0 else 0,
        "cti": opex / nii_total if nii_total > 0 else 0,
    }

# Projection parameters
params = {
    "FY27B": dict(aum_open=AUM["FY26A"], aum_close=AUM["FY27B"], yield_pct=0.138,
                  cob_pct=0.0740, fee_pct=0.0165, opex_pct=0.0365, cc_pct=0.0210, tax_rt=0.252),
    "FY27U": dict(aum_open=AUM["FY26A"], aum_close=AUM["FY27U"], yield_pct=0.140,
                  cob_pct=0.0725, fee_pct=0.0180, opex_pct=0.0355, cc_pct=0.0175, tax_rt=0.252),
    "FY27D": dict(aum_open=AUM["FY26A"], aum_close=AUM["FY27D"], yield_pct=0.136,
                  cob_pct=0.0760, fee_pct=0.0148, opex_pct=0.0390, cc_pct=0.0255, tax_rt=0.252),
    "FY28B": dict(aum_open=AUM["FY27B"], aum_close=AUM["FY28B"], yield_pct=0.133,
                  cob_pct=0.0710, fee_pct=0.0178, opex_pct=0.0330, cc_pct=0.0175, tax_rt=0.252),
    "FY29B": dict(aum_open=AUM["FY28B"], aum_close=AUM["FY29B"], yield_pct=0.129,
                  cob_pct=0.0685, fee_pct=0.0192, opex_pct=0.0305, cc_pct=0.0155, tax_rt=0.252),
    "FY30B": dict(aum_open=AUM["FY29B"], aum_close=AUM["FY30B"], yield_pct=0.125,
                  cob_pct=0.0660, fee_pct=0.0205, opex_pct=0.0285, cc_pct=0.0140, tax_rt=0.252),
}

res = {k: proj_pl(**v) for k, v in params.items()}

# Equity evolution for ROE calcs
eq = {
    "FY26A": 10298,
    "FY27B": 10298 + 2500 + res["FY27B"]["pat"],  # post-QIP + retained earnings
    "FY27U": 10298 + 2500 + res["FY27U"]["pat"],
    "FY27D": 10298 + 2500 + res["FY27D"]["pat"],
}
eq["FY28B"] = eq["FY27B"] + res["FY28B"]["pat"]
eq["FY29B"] = eq["FY28B"] + res["FY29B"]["pat"]
eq["FY30B"] = eq["FY29B"] + res["FY30B"]["pat"]

# P&L projection rows
# (label, bold, section, FY26A, FY27B, FY27U, FY27D, FY28B, FY30B, fmt)
proj_rows = [
    ("AUM BRIDGE", True, True, None, None, None, None, None, None, None),
    ("Opening AUM", False, False, 35631, 60348, 60348, 60348, round(AUM["FY27B"]), round(AUM["FY29B"]), CR0),
    ("AUM Growth (%)", False, False, 0.694, 0.370, 0.400, 0.280, 0.300, 0.220, PCT),
    ("Closing AUM", True, False, 60348, round(AUM["FY27B"]), round(AUM["FY27U"]), round(AUM["FY27D"]),
     round(AUM["FY28B"]), round(AUM["FY30B"]), CR0),
    ("Average AUM", False, False, 47990, round(res["FY27B"]["avg_aum"]), round(res["FY27U"]["avg_aum"]),
     round(res["FY27D"]["avg_aum"]), round(res["FY28B"]["avg_aum"]), round(res["FY30B"]["avg_aum"]), CR0),

    ("INCOME STATEMENT", True, True, None, None, None, None, None, None, None),
    ("Total Interest Income", False, False, 6136, round(res["FY27B"]["int_inc"]),
     round(res["FY27U"]["int_inc"]), round(res["FY27D"]["int_inc"]),
     round(res["FY28B"]["int_inc"]), round(res["FY30B"]["int_inc"]), CR0),
    ("  Interest Expenses", False, False, 2736, round(res["FY27B"]["int_exp"]),
     round(res["FY27U"]["int_exp"]), round(res["FY27D"]["int_exp"]),
     round(res["FY28B"]["int_exp"]), round(res["FY30B"]["int_exp"]), CR0),
    ("Net Interest Income (NII — pure)", True, False, 3400, round(res["FY27B"]["nii_pure"]),
     round(res["FY27U"]["nii_pure"]), round(res["FY27D"]["nii_pure"]),
     round(res["FY28B"]["nii_pure"]), round(res["FY30B"]["nii_pure"]), CR0),
    ("  Fee & Other Income", False, False, 629, round(res["FY27B"]["fee_inc"]),
     round(res["FY27U"]["fee_inc"]), round(res["FY27D"]["fee_inc"]),
     round(res["FY28B"]["fee_inc"]), round(res["FY30B"]["fee_inc"]), CR0),
    ("NII incl. Fee Income", True, False, 4029, round(res["FY27B"]["nii_total"]),
     round(res["FY27U"]["nii_total"]), round(res["FY27D"]["nii_total"]),
     round(res["FY28B"]["nii_total"]), round(res["FY30B"]["nii_total"]), CR0),
    ("Operating Expenses", False, False, 2095, round(res["FY27B"]["opex"]),
     round(res["FY27U"]["opex"]), round(res["FY27D"]["opex"]),
     round(res["FY28B"]["opex"]), round(res["FY30B"]["opex"]), CR0),
    ("Pre-Provision Operating Profit (PPoP)", True, False, 1935, round(res["FY27B"]["ppop"]),
     round(res["FY27U"]["ppop"]), round(res["FY27D"]["ppop"]),
     round(res["FY28B"]["ppop"]), round(res["FY30B"]["ppop"]), CR0),
    ("  Credit Cost / Provisions", False, False, 1212, round(res["FY27B"]["cc"]),
     round(res["FY27U"]["cc"]), round(res["FY27D"]["cc"]),
     round(res["FY28B"]["cc"]), round(res["FY30B"]["cc"]), CR0),
    ("Profit Before Tax (PBT)", True, False, 723, round(res["FY27B"]["pbt"]),
     round(res["FY27U"]["pbt"]), round(res["FY27D"]["pbt"]),
     round(res["FY28B"]["pbt"]), round(res["FY30B"]["pbt"]), CR0),
    ("  Income Tax", False, False, 181, round(res["FY27B"]["tax"]),
     round(res["FY27U"]["tax"]), round(res["FY27D"]["tax"]),
     round(res["FY28B"]["tax"]), round(res["FY30B"]["tax"]), CR0),
    ("Profit After Tax (PAT)", True, False, 542, round(res["FY27B"]["pat"]),
     round(res["FY27U"]["pat"]), round(res["FY27D"]["pat"]),
     round(res["FY28B"]["pat"]), round(res["FY30B"]["pat"]), CR0),

    ("YoY PAT GROWTH", False, False, None,
     round(res["FY27B"]["pat"]/542-1, 3),
     round(res["FY27U"]["pat"]/542-1, 3),
     round(res["FY27D"]["pat"]/542-1, 3),
     round(res["FY28B"]["pat"]/res["FY27B"]["pat"]-1, 3),
     round(res["FY30B"]["pat"]/res["FY29B"]["pat"]-1, 3), PCT),

    ("KEY RATIOS", True, True, None, None, None, None, None, None, None),
    ("ROA (PAT / Avg AUM %)", False, False, 0.0114, round(res["FY27B"]["roa"], 4),
     round(res["FY27U"]["roa"], 4), round(res["FY27D"]["roa"], 4),
     round(res["FY28B"]["roa"], 4), round(res["FY30B"]["roa"], 4), PCT2),
    ("ROE (PAT / Avg Equity %)", False, False,
     round(542/((8124+10298)/2), 4),
     round(res["FY27B"]["pat"]/((10298+2500+eq["FY27B"])/2), 4),
     round(res["FY27U"]["pat"]/((10298+2500+eq["FY27U"])/2), 4),
     round(res["FY27D"]["pat"]/((10298+2500+eq["FY27D"])/2), 4),
     round(res["FY28B"]["pat"]/((eq["FY27B"]+eq["FY28B"])/2), 4),
     round(res["FY30B"]["pat"]/((eq["FY29B"]+eq["FY30B"])/2), 4), PCT2),
    ("Cost-to-Income (%)", False, False, 0.520, round(res["FY27B"]["cti"], 3),
     round(res["FY27U"]["cti"], 3), round(res["FY27D"]["cti"], 3),
     round(res["FY28B"]["cti"], 3), round(res["FY30B"]["cti"], 3), PCT),
    ("Opex / Avg AUM (%)", False, False, 0.0347, 0.0365, 0.0355, 0.0390, 0.0330, 0.0285, PCT2),
    ("Credit Cost / Avg AUM (%)", False, False, 0.0201, 0.0210, 0.0175, 0.0255, 0.0175, 0.0140, PCT2),
    ("Gross Yield (%)", False, False, 0.142, 0.138, 0.140, 0.136, 0.133, 0.125, PCT2),
    ("Cost of Borrowing (%)", False, False, 0.0763, 0.074, 0.0725, 0.076, 0.071, 0.066, PCT2),
    ("EPS (₹/share)", False, False,
     round(542/81, 2),
     round(res["FY27B"]["pat"]/87.6, 2),
     round(res["FY27U"]["pat"]/87.6, 2),
     round(res["FY27D"]["pat"]/87.6, 2),
     round(res["FY28B"]["pat"]/87.6, 2),
     round(res["FY30B"]["pat"]/87.6, 2), EPS),
]

col_map_proj = [3, 5, 6, 7, 9, 11]
col_fills = [MGRAY, LBLUE, LGREEN, LRED, LBLUE, LBLUE]
col_fills_bold = [MGRAY, "BFDBFE", "A7F3D0", "FCA5A5", "BFDBFE", "BFDBFE"]

r = 4
for row_data in proj_rows:
    label, bold, is_section = row_data[0], row_data[1], row_data[2]
    vals = row_data[3:9]
    fmt = row_data[9]

    if is_section:
        merge(ws_proj, r, 2, r, 11, f"  {label}",
              bold=True, color=WHITE, size=9, fill=GRAY, align_h="left")
        r += 1
        continue

    cl = ws_proj.cell(row=r, column=2, value=label)
    cl.font = Font(name="Calibri", bold=bold, color=NAVY, size=9)
    cl.alignment = A("left", indent=1 if not bold else 0)
    cl.border = B("hair")
    cl.fill = FILL(MGRAY if bold else WHITE)

    for i, (v, col) in enumerate(zip(vals, col_map_proj)):
        c2 = ws_proj.cell(row=r, column=col, value=v)
        c2.font = Font(name="Calibri", bold=bold, color=NAVY, size=9)
        c2.alignment = A()
        c2.border = B("hair")
        if fmt and v is not None: c2.number_format = fmt
        c2.fill = FILL(col_fills_bold[i] if bold else col_fills[i])
    r += 1

# Divider cols
for dc in [4, 8, 10]:
    ws_proj.column_dimensions[get_column_letter(dc)].width = 0.5

# Note
merge(ws_proj, r+1, 2, r+1, 11,
      "Methodology: AUM-driven model. Interest Income = Avg Loans × Gross Yield. "
      "Int Expense = Avg Borrowings × CoB. Fee Income = Avg AUM × Fee Rate. Opex = Avg AUM × Opex%. "
      "Credit Cost = Avg AUM × CC%. Avg Borrowings = Avg Loans × 86% (approx on-BS gearing).",
      bold=False, color=GRAY, size=8, fill=LGRAY, align_h="left")

# ─────────────────────────────────────────────────────────────────────────────
# SHEET 6 — BALANCE SHEET PROJECTIONS
# ─────────────────────────────────────────────────────────────────────────────
ws_bsp = wb.create_sheet("BS Projections")
hide_gridlines(ws_bsp)
col_w(ws_bsp, [1, 36, 14, 14, 14, 14, 14, 14, 1])

merge(ws_bsp, 1, 2, 1, 8,
      "PROJECTED BALANCE SHEET  |  ₹ Crore  |  BASE CASE",
      bold=True, color=WHITE, size=11, fill=NAVY)

bs_proj_hdrs = ["Particulars (₹ Cr)", "FY26A\n(Actual)", "FY27E", "FY28E", "FY29E", "FY30E"]
for i, h in enumerate(bs_proj_hdrs):
    cl = ws_bsp.cell(row=2, column=i+2, value=h)
    cl.font = Font(name="Calibri", bold=True, color=WHITE, size=9)
    cl.fill = FILL(NAVY if i in (0, 5) else BLUE)
    cl.alignment = A(wrap=True)
    cl.border = B()

# Projected equity
eq_proj = {
    "FY26A": 10298, "FY27E": eq["FY27B"], "FY28E": eq["FY28B"],
    "FY29E": eq["FY29B"], "FY30E": eq["FY30B"]
}
# Projected borrowings via D/E
de = {"FY27E": 4.00, "FY28E": 4.00, "FY29E": 3.80, "FY30E": 3.60}
borr_proj = {k: round(eq_proj[k] * de[k]) for k in de}
borr_proj["FY26A"] = 48098

# Projected loans (on-BS = 92% of closing AUM)
aum_proj = {"FY26A": 60348, "FY27E": round(AUM["FY27B"]), "FY28E": round(AUM["FY28B"]),
            "FY29E": round(AUM["FY29B"]), "FY30E": round(AUM["FY30B"])}
loans_proj = {k: round(v * 0.920) for k, v in aum_proj.items()}

# Other items estimated proportionally
def bs_proj_data(yr):
    loans = loans_proj[yr]
    borr = borr_proj[yr]
    eq_v = eq_proj[yr]
    assets = loans + round(loans * 0.08)  # non-loan assets ~8% of loans
    cash_inv = round(assets * 0.05)
    other_assets = assets - loans - cash_inv
    other_liab = round(borr * 0.04)
    return {
        "cash": cash_inv, "loans": loans, "other_assets": other_assets,
        "assets": assets, "borr": borr, "other_liab": other_liab,
        "share_cap": 162, "reserves": round(eq_v - 162),
        "equity": eq_v, "total_liab_eq": borr + other_liab + eq_v
    }

bsp_data = {yr: bs_proj_data(yr) for yr in ["FY26A", "FY27E", "FY28E", "FY29E", "FY30E"]}

bs_proj_rows = [
    ("ASSETS", True, True),
    ("Cash, Investments & Liquid Assets", False, False, "cash"),
    ("Loans (Net — On Balance Sheet)", True, False, "loans"),
    ("Other Assets", False, False, "other_assets"),
    ("Total Assets", True, False, "assets"),
    ("LIABILITIES", True, True),
    ("Borrowings", True, False, "borr"),
    ("Other Liabilities", False, False, "other_liab"),
    ("Total Liabilities", True, False, lambda d: d["borr"] + d["other_liab"]),
    ("EQUITY", True, True),
    ("Share Capital", False, False, "share_cap"),
    ("Reserves & Surplus", False, False, "reserves"),
    ("Total Equity", True, False, "equity"),
    ("Total Liabilities + Equity", True, False, "total_liab_eq"),
    ("KEY DERIVED METRICS", True, True),
    ("AUM (₹ Cr)", False, False, lambda d: None),  # special
    ("Debt / Equity (x)", False, False, lambda d: None),
    ("Book Value / Share (₹)", False, False, lambda d: None),
]

r = 3
yrs = ["FY26A", "FY27E", "FY28E", "FY29E", "FY30E"]
for row_data in bs_proj_rows:
    label, bold, is_section = row_data[0], row_data[1], row_data[2]

    if is_section:
        merge(ws_bsp, r, 2, r, 7, f"  {label}",
              bold=True, color=WHITE, size=9, fill=GRAY, align_h="left")
        r += 1
        continue

    cl = ws_bsp.cell(row=r, column=2, value=label)
    cl.font = Font(name="Calibri", bold=bold, color=NAVY, size=9)
    cl.alignment = A("left", indent=1 if not bold else 0)
    cl.border = B("hair")
    cl.fill = FILL(MGRAY if bold else WHITE)

    key = row_data[3] if len(row_data) > 3 else None
    for i, yr in enumerate(yrs):
        col = i + 3
        d = bsp_data[yr]
        if label == "AUM (₹ Cr)":
            v = aum_proj[yr]
        elif label == "Debt / Equity (x)":
            v = round(d["borr"] / d["equity"], 2)
        elif label == "Book Value / Share (₹)":
            shares = 87.6 if yr != "FY26A" else 81.0
            v = round(d["equity"] / shares, 1)
        elif callable(key):
            v = key(d)
        else:
            v = d.get(key)

        c2 = ws_bsp.cell(row=r, column=col, value=v)
        c2.font = Font(name="Calibri", bold=bold, color=NAVY, size=9)
        c2.alignment = A()
        c2.border = B("hair")
        if v is not None and isinstance(v, (int, float)):
            if v < 30 and v > 0: c2.number_format = XFMT
            else: c2.number_format = CR0
        if col == 3: c2.fill = FILL(MGRAY)
        elif bold:   c2.fill = FILL("BFDBFE")
        else:        c2.fill = FILL(LBLUE if col > 3 else WHITE)
    r += 1

# ─────────────────────────────────────────────────────────────────────────────
# SHEET 7 — RATIO DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
ws_rat = wb.create_sheet("Ratio Dashboard")
hide_gridlines(ws_rat)
col_w(ws_rat, [1, 36, 14, 14, 14, 14, 14, 14, 14, 1])

merge(ws_rat, 1, 2, 1, 9,
      "RATIO DASHBOARD  |  Historical + Projected  |  ₹ Crore",
      bold=True, color=WHITE, size=11, fill=NAVY)

rat_hdrs = ["Ratio / Metric", "FY25A\n(partial)", "FY26A", "FY27E\nBase", "FY27E\nBull",
            "FY27E\nBear", "FY28E", "FY29E", "FY30E"]
for i, h in enumerate(rat_hdrs):
    cl = ws_rat.cell(row=2, column=i+2, value=h)
    cl.font = Font(name="Calibri", bold=True, color=WHITE, size=9)
    cl.fill = FILL(GRAY if i == 0 else NAVY)
    if "Bull" in h: cl.fill = FILL("065F46")
    if "Bear" in h: cl.fill = FILL(RED)
    cl.alignment = A(wrap=True)
    cl.border = B()

ratio_rows = [
    ("SCALE", True, True),
    ("AUM (₹ Cr)", False, False,
     35631, 60348, round(AUM["FY27B"]), round(AUM["FY27U"]), round(AUM["FY27D"]),
     round(AUM["FY28B"]), round(AUM["FY29B"]), round(AUM["FY30B"]), CR0),
    ("AUM YoY Growth", False, False,
     None, 0.694, 0.370, 0.400, 0.280, 0.300, 0.250, 0.220, PCT),

    ("PROFITABILITY", True, True),
    ("NII incl. Fees (₹ Cr)", False, False,
     None, 4029, round(res["FY27B"]["nii_total"]), round(res["FY27U"]["nii_total"]),
     round(res["FY27D"]["nii_total"]), round(res["FY28B"]["nii_total"]),
     round(res["FY29B"]["nii_total"]), round(res["FY30B"]["nii_total"]), CR0),
    ("PPoP (₹ Cr)", False, False,
     None, 1935, round(res["FY27B"]["ppop"]), round(res["FY27U"]["ppop"]),
     round(res["FY27D"]["ppop"]), round(res["FY28B"]["ppop"]),
     round(res["FY29B"]["ppop"]), round(res["FY30B"]["ppop"]), CR0),
    ("PAT (₹ Cr)", True, False,
     None, 542, round(res["FY27B"]["pat"]), round(res["FY27U"]["pat"]),
     round(res["FY27D"]["pat"]), round(res["FY28B"]["pat"]),
     round(res["FY29B"]["pat"]), round(res["FY30B"]["pat"]), CR0),
    ("PAT YoY Growth", False, False,
     None, None,
     round(res["FY27B"]["pat"]/542-1, 3), round(res["FY27U"]["pat"]/542-1, 3),
     round(res["FY27D"]["pat"]/542-1, 3), round(res["FY28B"]["pat"]/res["FY27B"]["pat"]-1, 3),
     round(res["FY29B"]["pat"]/res["FY28B"]["pat"]-1, 3), round(res["FY30B"]["pat"]/res["FY29B"]["pat"]-1, 3), PCT),
    ("ROA (PAT / Avg AUM %)", False, False,
     None, 0.0114, round(res["FY27B"]["roa"], 4), round(res["FY27U"]["roa"], 4),
     round(res["FY27D"]["roa"], 4), round(res["FY28B"]["roa"], 4),
     round(res["FY29B"]["roa"], 4), round(res["FY30B"]["roa"], 4), PCT2),
    ("ROE (PAT / Avg Equity %)", False, False,
     None, round(542/((8124+10298)/2), 4),
     round(res["FY27B"]["pat"]/((10298+2500+eq["FY27B"])/2), 4),
     round(res["FY27U"]["pat"]/((10298+2500+eq["FY27U"])/2), 4),
     round(res["FY27D"]["pat"]/((10298+2500+eq["FY27D"])/2), 4),
     round(res["FY28B"]["pat"]/((eq["FY27B"]+eq["FY28B"])/2), 4),
     round(res["FY29B"]["pat"]/((eq["FY28B"]+eq["FY29B"])/2), 4),
     round(res["FY30B"]["pat"]/((eq["FY29B"]+eq["FY30B"])/2), 4), PCT2),
    ("EPS (₹/share)", False, False,
     None, round(542/81, 2),
     round(res["FY27B"]["pat"]/87.6, 2), round(res["FY27U"]["pat"]/87.6, 2),
     round(res["FY27D"]["pat"]/87.6, 2), round(res["FY28B"]["pat"]/87.6, 2),
     round(res["FY29B"]["pat"]/87.6, 2), round(res["FY30B"]["pat"]/87.6, 2), EPS),
    ("Book Value / Share (₹)", False, False,
     round(8124/81, 1), round(10298/81, 1),
     round(eq["FY27B"]/87.6, 1), round(eq["FY27U"]/87.6, 1), round(eq["FY27D"]/87.6, 1),
     round(eq["FY28B"]/87.6, 1), round(eq["FY29B"]/87.6, 1), round(eq["FY30B"]/87.6, 1), EPS),

    ("YIELD & SPREAD", True, True),
    ("Gross Yield (%)", False, False,
     None, 0.142, 0.138, 0.140, 0.136, 0.133, 0.129, 0.125, PCT2),
    ("Cost of Borrowing (%)", False, False,
     None, 0.0763, 0.074, 0.0725, 0.076, 0.071, 0.0685, 0.066, PCT2),
    ("Net Interest Spread (%)", False, False,
     None, 0.066, 0.064, 0.068, 0.060, 0.062, 0.061, 0.059, PCT2),
    ("Fee Income / AUM (%)", False, False,
     None, 0.0154, 0.0165, 0.0180, 0.0148, 0.0178, 0.0192, 0.0205, PCT2),

    ("EFFICIENCY", True, True),
    ("Opex / Avg AUM (%)", False, False,
     None, 0.0347, 0.0365, 0.0355, 0.0390, 0.0330, 0.0305, 0.0285, PCT2),
    ("Cost-to-Income (%)", False, False,
     None, 0.520,
     round(res["FY27B"]["cti"], 3), round(res["FY27U"]["cti"], 3), round(res["FY27D"]["cti"], 3),
     round(res["FY28B"]["cti"], 3), round(res["FY29B"]["cti"], 3), round(res["FY30B"]["cti"], 3), PCT),
    ("PPoP / Avg AUM (%)", False, False,
     None, round(1935/47990, 4),
     round(res["FY27B"]["ppop"]/res["FY27B"]["avg_aum"], 4),
     round(res["FY27U"]["ppop"]/res["FY27U"]["avg_aum"], 4),
     round(res["FY27D"]["ppop"]/res["FY27D"]["avg_aum"], 4),
     round(res["FY28B"]["ppop"]/res["FY28B"]["avg_aum"], 4),
     round(res["FY29B"]["ppop"]/res["FY29B"]["avg_aum"], 4),
     round(res["FY30B"]["ppop"]/res["FY30B"]["avg_aum"], 4), PCT2),

    ("ASSET QUALITY", True, True),
    ("Credit Cost / Avg AUM (%)", False, False,
     None, 0.0201, 0.0210, 0.0175, 0.0255, 0.0175, 0.0155, 0.0140, PCT2),
    ("GNPA (%)", False, False,
     0.0184, 0.0144, 0.0128, 0.0105, 0.0155, 0.0105, 0.0085, 0.0070, PCT2),
    ("NNPA (%)", False, False,
     0.0085, 0.0074, 0.0062, 0.0048, 0.0078, 0.0048, 0.0038, 0.0030, PCT2),
    ("PCR (%)", False, False,
     0.547, 0.490, 0.515, 0.540, 0.495, 0.540, 0.555, 0.570, PCT),

    ("CAPITAL", True, True),
    ("Total Equity (₹ Cr)", False, False,
     8124, 10298, round(eq["FY27B"]), round(eq["FY27U"]), round(eq["FY27D"]),
     round(eq["FY28B"]), round(eq["FY29B"]), round(eq["FY30B"]), CR0),
    ("Debt / Equity (x)", False, False,
     round(25881/8124, 2), 3.78,
     round(borr_proj["FY27E"]/eq["FY27B"], 2), None, None,
     round(borr_proj["FY28E"]/eq["FY28B"], 2),
     round(borr_proj["FY29E"]/eq["FY29B"], 2),
     round(borr_proj["FY30E"]/eq["FY30B"], 2), XFMT),
    ("CAR (%)", False, False,
     None, 0.1683, 0.172, 0.178, 0.167, 0.178, 0.183, 0.188, PCT),
]

r = 3
for row_data in ratio_rows:
    label, bold, is_section = row_data[0], row_data[1], row_data[2]

    if is_section:
        merge(ws_rat, r, 2, r, 10, f"  {label}",
              bold=True, color=WHITE, size=9, fill=GRAY, align_h="left")
        r += 1
        continue

    vals = row_data[3:11]
    fmt = row_data[11]

    cl = ws_rat.cell(row=r, column=2, value=label)
    cl.font = Font(name="Calibri", bold=bold, color=NAVY, size=9)
    cl.alignment = A("left", indent=1 if not bold else 0)
    cl.border = B("hair")
    cl.fill = FILL(MGRAY if bold else WHITE)

    for i, v in enumerate(vals):
        col = i + 3
        c2 = ws_rat.cell(row=r, column=col, value=v)
        c2.font = Font(name="Calibri", bold=bold, color=NAVY, size=9)
        c2.alignment = A()
        c2.border = B("hair")
        if fmt and v is not None: c2.number_format = fmt
        if col <= 4:   c2.fill = FILL(MGRAY if bold else LGRAY)
        elif col == 5: c2.fill = FILL("A7F3D0" if bold else LGREEN)
        elif col == 6: c2.fill = FILL("FCA5A5" if bold else LRED)
        else:          c2.fill = FILL("BFDBFE" if bold else LBLUE)
    r += 1

# ─────────────────────────────────────────────────────────────────────────────
# SHEET 8 — VALUATION
# ─────────────────────────────────────────────────────────────────────────────
ws_val = wb.create_sheet("Valuation")
hide_gridlines(ws_val)
col_w(ws_val, [1, 30, 14, 14, 14, 14, 14, 1])

merge(ws_val, 1, 2, 1, 7,
      "VALUATION ANALYSIS  |  Poonawalla Fincorp  |  May 2026",
      bold=True, color=WHITE, size=11, fill=NAVY)

# Current market info
merge(ws_val, 2, 2, 2, 7,
      "Reference: ~81 Cr shares outstanding (pre-QIP) | ~₹2,500 Cr QIP at ~₹380/share in Apr-26 | CMP ~₹375 (indicative)",
      bold=False, color=GRAY, size=9, fill=LGRAY)

r = 4
# ── P/BV Valuation ───────────────────────────────────────────────────────────
merge(ws_val, r, 2, r, 7, "  1. PRICE-TO-BOOK VALUE (P/BV) APPROACH",
      bold=True, color=WHITE, size=10, fill=BLUE); r += 1

pbv_hdrs = ["Particulars", "FY27E", "FY28E", "FY29E", "FY30E"]
for i, h in enumerate(pbv_hdrs):
    cl = ws_val.cell(row=r, column=i+2, value=h)
    cl.font = Font(name="Calibri", bold=True, color=WHITE, size=9)
    cl.fill = FILL(BLUE)
    cl.border = B()
cl = ws_val.cell(row=r, column=7, value="Note")
cl.font = Font(name="Calibri", bold=True, color=WHITE, size=9); cl.fill = FILL(BLUE); cl.border = B()
r += 1

pbv_rows = [
    ("Book Value / Share (₹)", round(eq["FY27B"]/87.6, 1), round(eq["FY28B"]/87.6, 1),
     round(eq["FY29B"]/87.6, 1), round(eq["FY30B"]/87.6, 1), "Post-QIP equity used"),
    ("P/BV — Bear (1.8x)", round(eq["FY27B"]/87.6*1.8, 1), round(eq["FY28B"]/87.6*1.8, 1),
     round(eq["FY29B"]/87.6*1.8, 1), round(eq["FY30B"]/87.6*1.8, 1), "Downside / stressed"),
    ("P/BV — Base (2.5x)", round(eq["FY27B"]/87.6*2.5, 1), round(eq["FY28B"]/87.6*2.5, 1),
     round(eq["FY29B"]/87.6*2.5, 1), round(eq["FY30B"]/87.6*2.5, 1), "Base case target"),
    ("P/BV — Bull (3.5x)", round(eq["FY27B"]/87.6*3.5, 1), round(eq["FY28B"]/87.6*3.5, 1),
     round(eq["FY29B"]/87.6*3.5, 1), round(eq["FY30B"]/87.6*3.5, 1), "High-growth premium"),
    ("P/BV — Aspirational (4.5x)", round(eq["FY27B"]/87.6*4.5, 1), round(eq["FY28B"]/87.6*4.5, 1),
     round(eq["FY29B"]/87.6*4.5, 1), round(eq["FY30B"]/87.6*4.5, 1), "Bajaj Finance comp."),
]
for row_data in pbv_rows:
    label = row_data[0]
    vals = row_data[1:5]
    note = row_data[5]
    bold = "BV" in label
    cl = ws_val.cell(row=r, column=2, value=label)
    cl.font = Font(name="Calibri", bold=bold, color=NAVY, size=9)
    cl.alignment = A("left", indent=1); cl.border = B("hair")
    cl.fill = FILL(MGRAY if bold else WHITE)
    for i, v in enumerate(vals):
        c2 = ws_val.cell(row=r, column=i+3, value=v)
        c2.font = Font(name="Calibri", bold=bold, color=NAVY, size=9)
        c2.alignment = A(); c2.border = B("hair"); c2.number_format = EPS
        if "2.5x" in label: c2.fill = FILL(LBLUE)
        elif "3.5x" in label: c2.fill = FILL(LGREEN)
        elif "Bear" in label: c2.fill = FILL(LRED)
        elif "4.5x" in label: c2.fill = FILL(LAMBER)
        else: c2.fill = FILL(LGRAY)
    c2 = ws_val.cell(row=r, column=7, value=note)
    c2.font = Font(name="Calibri", color=GRAY, size=8, italic=True)
    c2.alignment = A("left", indent=1); c2.border = B("hair"); c2.fill = FILL(LGRAY)
    r += 1

r += 1
# ── P/E Valuation ────────────────────────────────────────────────────────────
merge(ws_val, r, 2, r, 7, "  2. PRICE-TO-EARNINGS (P/E) APPROACH",
      bold=True, color=WHITE, size=10, fill=BLUE); r += 1

for i, h in enumerate(pbv_hdrs):
    cl = ws_val.cell(row=r, column=i+2, value=h)
    cl.font = Font(name="Calibri", bold=True, color=WHITE, size=9)
    cl.fill = FILL(BLUE); cl.border = B()
cl = ws_val.cell(row=r, column=7, value="Note")
cl.font = Font(name="Calibri", bold=True, color=WHITE, size=9); cl.fill = FILL(BLUE); cl.border = B()
r += 1

pe_rows = [
    ("EPS (₹/share)", round(res["FY27B"]["pat"]/87.6, 2), round(res["FY28B"]["pat"]/87.6, 2),
     round(res["FY29B"]["pat"]/87.6, 2), round(res["FY30B"]["pat"]/87.6, 2), "Base case"),
    ("P/E — 15x (conservative)", round(res["FY27B"]["pat"]/87.6*15, 1), round(res["FY28B"]["pat"]/87.6*15, 1),
     round(res["FY29B"]["pat"]/87.6*15, 1), round(res["FY30B"]["pat"]/87.6*15, 1), "Value play"),
    ("P/E — 20x (base)", round(res["FY27B"]["pat"]/87.6*20, 1), round(res["FY28B"]["pat"]/87.6*20, 1),
     round(res["FY29B"]["pat"]/87.6*20, 1), round(res["FY30B"]["pat"]/87.6*20, 1), "Base target"),
    ("P/E — 25x (growth premium)", round(res["FY27B"]["pat"]/87.6*25, 1), round(res["FY28B"]["pat"]/87.6*25, 1),
     round(res["FY29B"]["pat"]/87.6*25, 1), round(res["FY30B"]["pat"]/87.6*25, 1), "High growth"),
    ("P/E — 30x (re-rating)", round(res["FY27B"]["pat"]/87.6*30, 1), round(res["FY28B"]["pat"]/87.6*30, 1),
     round(res["FY29B"]["pat"]/87.6*30, 1), round(res["FY30B"]["pat"]/87.6*30, 1), "Full re-rating"),
]
for row_data in pe_rows:
    label = row_data[0]
    vals = row_data[1:5]
    note = row_data[5]
    bold = "EPS" in label
    cl = ws_val.cell(row=r, column=2, value=label)
    cl.font = Font(name="Calibri", bold=bold, color=NAVY, size=9)
    cl.alignment = A("left", indent=1); cl.border = B("hair")
    cl.fill = FILL(MGRAY if bold else WHITE)
    for i, v in enumerate(vals):
        c2 = ws_val.cell(row=r, column=i+3, value=v)
        c2.font = Font(name="Calibri", bold=bold, color=NAVY, size=9)
        c2.alignment = A(); c2.border = B("hair"); c2.number_format = EPS
        if "20x" in label: c2.fill = FILL(LBLUE)
        elif "25x" in label: c2.fill = FILL(LGREEN)
        elif "15x" in label: c2.fill = FILL(LRED)
        elif "30x" in label: c2.fill = FILL(LAMBER)
        else: c2.fill = FILL(LGRAY)
    c2 = ws_val.cell(row=r, column=7, value=note)
    c2.font = Font(name="Calibri", color=GRAY, size=8, italic=True)
    c2.alignment = A("left", indent=1); c2.border = B("hair"); c2.fill = FILL(LGRAY)
    r += 1

r += 1
# ── DCF Section ──────────────────────────────────────────────────────────────
merge(ws_val, r, 2, r, 7, "  3. DIVIDEND DISCOUNT / RESIDUAL INCOME (DDM/RI) — SIMPLIFIED",
      bold=True, color=WHITE, size=10, fill=BLUE); r += 1

# Simple RI-based intrinsic value
# RI = PAT - (Ke × Equity)
Ke = 0.130
pat_proj = [res["FY27B"]["pat"], res["FY28B"]["pat"], res["FY29B"]["pat"], res["FY30B"]["pat"]]
eq_proj_list = [eq["FY27B"], eq["FY28B"], eq["FY29B"], eq["FY30B"]]
ri_list = [pat - Ke * eq_v for pat, eq_v in zip(pat_proj, eq_proj_list)]
terminal_ri = ri_list[-1] * (1 + 0.05) / (Ke - 0.05)
discount_factors = [1/(1+Ke)**i for i in range(1, 5)]
pv_ri = sum(ri * df for ri, df in zip(ri_list, discount_factors))
pv_term = terminal_ri / (1+Ke)**4
intrinsic_equity = eq_proj_list[0] + pv_ri + pv_term  # FY27E opening equity + PV of RI
iv_per_share = intrinsic_equity / 87.6

dcf_items = [
    ("Cost of Equity (Ke)", "13.0%", "CAPM-estimated"),
    ("Terminal Growth Rate (g)", "5.0%", "Long-term GDP proxy"),
    ("FY27E PAT (₹ Cr)", round(res["FY27B"]["pat"]), "Base case"),
    ("FY30E PAT (₹ Cr)", round(res["FY30B"]["pat"]), "Base case"),
    ("PV of Residual Income (FY27–30, ₹ Cr)", round(pv_ri), "Discounted at 13%"),
    ("PV of Terminal Value (₹ Cr)", round(pv_term), "Gordon Growth on FY30 RI"),
    ("Opening Book Value (FY27E, ₹ Cr)", round(eq_proj_list[0]), "Post-QIP"),
    ("Intrinsic Equity Value (₹ Cr)", round(intrinsic_equity), "Book + PV RI"),
    ("Intrinsic Value / Share (₹)", round(iv_per_share, 1), "87.6 Cr shares"),
    ("Margin of Safety vs CMP ₹375", f"{round((iv_per_share-375)/375*100, 1)}%", "Positive = upside"),
]
for lbl, val, note in dcf_items:
    bold = "Intrinsic" in lbl or "Margin" in lbl
    cl = ws_val.cell(row=r, column=2, value=lbl)
    cl.font = Font(name="Calibri", bold=bold, color=NAVY, size=9)
    cl.alignment = A("left", indent=1); cl.border = B("hair")
    cl.fill = FILL(MGRAY if bold else WHITE)
    c2 = ws_val.cell(row=r, column=3, value=val)
    c2.font = Font(name="Calibri", bold=bold, color=NAVY, size=9)
    c2.alignment = A(); c2.border = B("hair")
    c2.fill = FILL(LBLUE if bold else XBLUE)
    c3 = ws_val.cell(row=r, column=4, value=note)
    c3.font = Font(name="Calibri", color=GRAY, size=8, italic=True)
    c3.alignment = A("left", indent=1); c3.border = B("hair"); c3.fill = FILL(LGRAY)
    ws_val.merge_cells(start_row=r, start_column=4, end_row=r, end_column=7)
    r += 1

r += 1
merge(ws_val, r, 2, r, 7,
      "⚠  DDM/RI is a simplified model. Key risks: credit cost normalization, secured mix shift compressing yield, "
      "macro headwinds (rate cycle, regulatory changes). Always triangulate with P/BV and P/E comps.",
      bold=False, color=AMBER, size=8, fill=LAMBER, align_h="left")

# ─────────────────────────────────────────────────────────────────────────────
# SHEET 9 — SCENARIO SUMMARY
# ─────────────────────────────────────────────────────────────────────────────
ws_scen = wb.create_sheet("Scenario Summary")
hide_gridlines(ws_scen)
col_w(ws_scen, [1, 36, 18, 18, 18, 18, 1])

merge(ws_scen, 1, 2, 1, 6,
      "SCENARIO SUMMARY  |  FY27E  |  Bull vs Base vs Bear",
      bold=True, color=WHITE, size=11, fill=NAVY)
merge(ws_scen, 2, 2, 2, 6,
      "Scenario drivers: AUM growth, credit cost, and yield assumptions differ across Bull/Base/Bear.",
      bold=False, color=GRAY, size=9, fill=LGRAY)

sc_hdrs = ["Metric", "FY26A\n(Actual)", "FY27E — BULL\n(Upside)", "FY27E — BASE\n(Central)",
           "FY27E — BEAR\n(Downside)"]
for i, h in enumerate(sc_hdrs):
    cl = ws_scen.cell(row=3, column=i+2, value=h)
    cl.font = Font(name="Calibri", bold=True, color=WHITE, size=9)
    cl.fill = FILL(GRAY if i == 0 else GRAY if i == 1 else "065F46" if i == 2 else NAVY if i == 3 else RED)
    cl.alignment = A(wrap=True); cl.border = B()

scen_rows = [
    ("KEY ASSUMPTIONS", True, True),
    ("AUM Growth (%)", False, False, 0.694, 0.400, 0.370, 0.280, PCT),
    ("AUM — Closing (₹ Cr)", False, False, 60348, round(AUM["FY27U"]), round(AUM["FY27B"]), round(AUM["FY27D"]), CR0),
    ("Gross Yield (%)", False, False, 0.142, 0.140, 0.138, 0.136, PCT2),
    ("Cost of Borrowing (%)", False, False, 0.0763, 0.0725, 0.0740, 0.0760, PCT2),
    ("Credit Cost / AUM (%)", False, False, 0.0201, 0.0175, 0.0210, 0.0255, PCT2),
    ("Opex / AUM (%)", False, False, 0.0347, 0.0355, 0.0365, 0.0390, PCT2),

    ("P&L OUTPUTS", True, True),
    ("NII incl. Fees (₹ Cr)", False, False, 4029,
     round(res["FY27U"]["nii_total"]), round(res["FY27B"]["nii_total"]), round(res["FY27D"]["nii_total"]), CR0),
    ("Opex (₹ Cr)", False, False, 2095,
     round(res["FY27U"]["opex"]), round(res["FY27B"]["opex"]), round(res["FY27D"]["opex"]), CR0),
    ("PPoP (₹ Cr)", False, False, 1935,
     round(res["FY27U"]["ppop"]), round(res["FY27B"]["ppop"]), round(res["FY27D"]["ppop"]), CR0),
    ("Credit Cost (₹ Cr)", False, False, 1212,
     round(res["FY27U"]["cc"]), round(res["FY27B"]["cc"]), round(res["FY27D"]["cc"]), CR0),
    ("PBT (₹ Cr)", False, False, 723,
     round(res["FY27U"]["pbt"]), round(res["FY27B"]["pbt"]), round(res["FY27D"]["pbt"]), CR0),
    ("PAT (₹ Cr)", True, False, 542,
     round(res["FY27U"]["pat"]), round(res["FY27B"]["pat"]), round(res["FY27D"]["pat"]), CR0),
    ("PAT YoY Growth (%)", False, False, None,
     round(res["FY27U"]["pat"]/542-1, 3), round(res["FY27B"]["pat"]/542-1, 3),
     round(res["FY27D"]["pat"]/542-1, 3), PCT),

    ("KEY RATIOS", True, True),
    ("ROA (%)", False, False, 0.0114,
     round(res["FY27U"]["roa"], 4), round(res["FY27B"]["roa"], 4), round(res["FY27D"]["roa"], 4), PCT2),
    ("Cost-to-Income (%)", False, False, 0.520,
     round(res["FY27U"]["cti"], 3), round(res["FY27B"]["cti"], 3), round(res["FY27D"]["cti"], 3), PCT),
    ("EPS (₹/share)", False, False, round(542/81, 2),
     round(res["FY27U"]["pat"]/87.6, 2), round(res["FY27B"]["pat"]/87.6, 2),
     round(res["FY27D"]["pat"]/87.6, 2), EPS),
    ("Book Value / Share (₹)", False, False, round(10298/81, 1),
     round(eq["FY27U"]/87.6, 1), round(eq["FY27B"]/87.6, 1), round(eq["FY27D"]/87.6, 1), EPS),

    ("VALUATION INDICATIVES", True, True),
    ("Fair Value @ P/BV 2.0x (₹)", False, False, None,
     round(eq["FY27U"]/87.6*2.0, 0), round(eq["FY27B"]/87.6*2.0, 0), round(eq["FY27D"]/87.6*2.0, 0), EPS),
    ("Fair Value @ P/BV 2.5x (₹)", False, False, None,
     round(eq["FY27U"]/87.6*2.5, 0), round(eq["FY27B"]/87.6*2.5, 0), round(eq["FY27D"]/87.6*2.5, 0), EPS),
    ("Fair Value @ P/BV 3.0x (₹)", False, False, None,
     round(eq["FY27U"]/87.6*3.0, 0), round(eq["FY27B"]/87.6*3.0, 0), round(eq["FY27D"]/87.6*3.0, 0), EPS),
    ("Fair Value @ P/E 20x (₹)", False, False, None,
     round(res["FY27U"]["pat"]/87.6*20, 0), round(res["FY27B"]["pat"]/87.6*20, 0),
     round(res["FY27D"]["pat"]/87.6*20, 0), EPS),
    ("Fair Value @ P/E 25x (₹)", False, False, None,
     round(res["FY27U"]["pat"]/87.6*25, 0), round(res["FY27B"]["pat"]/87.6*25, 0),
     round(res["FY27D"]["pat"]/87.6*25, 0), EPS),
]

r = 4
for row_data in scen_rows:
    label, bold, is_section = row_data[0], row_data[1], row_data[2]
    vals = row_data[3:7]
    fmt = row_data[7] if len(row_data) > 7 else None

    if is_section:
        merge(ws_scen, r, 2, r, 6, f"  {label}",
              bold=True, color=WHITE, size=9, fill=GRAY, align_h="left")
        r += 1
        continue

    cl = ws_scen.cell(row=r, column=2, value=label)
    cl.font = Font(name="Calibri", bold=bold, color=NAVY, size=9)
    cl.alignment = A("left", indent=1 if not bold else 0)
    cl.border = B("hair"); cl.fill = FILL(MGRAY if bold else WHITE)

    col_fills_sc = [MGRAY, LGREEN, LBLUE, LRED]
    col_fills_sc_bold = [MGRAY, "A7F3D0", "BFDBFE", "FCA5A5"]
    for i, v in enumerate(vals):
        col = i + 3
        c2 = ws_scen.cell(row=r, column=col, value=v)
        c2.font = Font(name="Calibri", bold=bold, color=NAVY, size=9)
        c2.alignment = A(); c2.border = B("hair")
        if fmt and v is not None: c2.number_format = fmt
        c2.fill = FILL(col_fills_sc_bold[i] if bold else col_fills_sc[i])
    r += 1

# Final notes row
r += 1
merge(ws_scen, r, 2, r, 6,
      "KEY RISKS TO WATCH:  "
      "(1) Unsecured/secured mix shift — secured loans have lower yield, compressing NIM.  "
      "(2) Credit cost normalization — legacy stress assets may re-emerge.  "
      "(3) Rate cycle — RBI rate cuts benefit CoB but also lower yield on floating rate loans.  "
      "(4) Competition from fintechs in personal/consumer segments.  "
      "(5) Capital adequacy post high-growth phase.",
      bold=False, color=AMBER, size=8, fill=LAMBER, align_h="left")

# ─────────────────────────────────────────────────────────────────────────────
# SET ACTIVE SHEET & SAVE
# ─────────────────────────────────────────────────────────────────────────────
wb.active = ws_cov

out_path = "/home/user/nbfc-dashboard/PFL_Financial_Model_FY27E-FY30E.xlsx"
wb.save(out_path)
print(f"Saved: {out_path}")

# Print key outputs for verification
print("\n=== KEY PROJECTION OUTPUTS (BASE CASE) ===")
print(f"FY26A PAT:  ₹{542:,} Cr  |  AUM: ₹{60348:,} Cr  |  ROA: 1.14%")
print(f"FY27E PAT:  ₹{round(res['FY27B']['pat']):,} Cr  |  AUM: ₹{round(AUM['FY27B']):,} Cr  |  ROA: {res['FY27B']['roa']*100:.2f}%")
print(f"FY28E PAT:  ₹{round(res['FY28B']['pat']):,} Cr  |  AUM: ₹{round(AUM['FY28B']):,} Cr  |  ROA: {res['FY28B']['roa']*100:.2f}%")
print(f"FY29E PAT:  ₹{round(res['FY29B']['pat']):,} Cr  |  AUM: ₹{round(AUM['FY29B']):,} Cr  |  ROA: {res['FY29B']['roa']*100:.2f}%")
print(f"FY30E PAT:  ₹{round(res['FY30B']['pat']):,} Cr  |  AUM: ₹{round(AUM['FY30B']):,} Cr  |  ROA: {res['FY30B']['roa']*100:.2f}%")
print(f"\nFY27E EPS: ₹{round(res['FY27B']['pat']/87.6, 2)} | BV/Share: ₹{round(eq['FY27B']/87.6, 1)}")
print(f"DCF Intrinsic Value: ₹{round(iv_per_share, 1)}/share (vs CMP ~₹375)")
print(f"\nFY27E Valuation Range:")
print(f"  P/BV 2.0x → ₹{round(eq['FY27B']/87.6*2.0, 0):.0f}  |  2.5x → ₹{round(eq['FY27B']/87.6*2.5, 0):.0f}  |  3.0x → ₹{round(eq['FY27B']/87.6*3.0, 0):.0f}")
print(f"  P/E  20x  → ₹{round(res['FY27B']['pat']/87.6*20, 0):.0f}  |  25x  → ₹{round(res['FY27B']['pat']/87.6*25, 0):.0f}  |  30x  → ₹{round(res['FY27B']['pat']/87.6*30, 0):.0f}")
