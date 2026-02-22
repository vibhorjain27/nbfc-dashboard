#!/usr/bin/env python3
"""
Data pipeline: Downloads NBFC investor presentations from BSE India
and extracts key financial metrics for the NBFC dashboard.

Run quarterly after new results are published:
    python3 fetch_presentations.py             # all companies
    python3 fetch_presentations.py poonawalla  # single company

Metrics extracted (where available):
  aum_cr, nii_cr, nim_pct, pat_cr, gnpa_pct, nnpa_pct,
  roa_pct, roe_pct, car_pct, disbursements_cr,
  share_capital_cr, reserves_cr, book_value_per_share
"""

import os, re, json, sys
import requests
import fitz  # PyMuPDF
from datetime import datetime

# ─── CONFIG ────────────────────────────────────────────────────────────────────

COMPANIES = {
    'poonawalla': {
        'name':       'Poonawalla Fincorp',
        'bse_code':   '524000',
        'nse_symbol': 'POONAWALLA',
        'face_value': 2,
    },
    'bajaj': {
        'name':       'Bajaj Finance',
        'bse_code':   '500034',
        'nse_symbol': 'BAJFINANCE',
        'face_value': 2,
    },
    'shriram': {
        'name':       'Shriram Finance',
        'bse_code':   '511218',
        'nse_symbol': 'SHRIRAMFIN',
        'face_value': 10,
    },
    'ltf': {
        'name':       'L&T Finance',
        'bse_code':   '533519',
        'nse_symbol': 'LTF',
        'face_value': 10,
    },
    'chola': {
        'name':       'Cholamandalam Finance',
        'bse_code':   '511243',
        'nse_symbol': 'CHOLAFIN',
        'face_value': 2,
    },
    'abcapital': {
        'name':       'Aditya Birla Capital',
        'bse_code':   '540691',
        'nse_symbol': 'ABCAPITAL',
        'face_value': 2,
        'lending_only': True,   # exclude AMC / insurance segments
    },
    'piramal': {
        'name':       'Piramal Finance',
        'bse_code':   '500302',        # Piramal Enterprises Limited (parent co)
        'nse_symbol': 'PEL',
        'face_value': 2,
        'lending_only': True,   # parent also has pharma; use finance segment data
    },
    'muthoot': {
        'name':       'Muthoot Finance',
        'bse_code':   '533398',
        'nse_symbol': 'MUTHOOTFIN',
        'face_value': 10,
    },
    'mahindra': {
        'name':       'Mahindra Finance',
        'bse_code':   '532720',
        'nse_symbol': 'M&MFIN',
        'face_value': 2,
    },
}

PDF_DIR      = os.path.join(os.path.dirname(__file__), 'data', 'pdfs')
DATA_DIR     = os.path.join(os.path.dirname(__file__), 'data')
NUM_QUARTERS = 5

BSE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept':     'application/json, text/plain, */*',
    'Referer':    'https://www.bseindia.com/corporates/ann.html',
    'Origin':     'https://www.bseindia.com',
}

# ─── BSE DISCOVERY ─────────────────────────────────────────────────────────────

def fetch_presentation_list(bse_code, from_year=2023):
    """Return list of investor presentation dicts {date, attachment} newest-first."""
    s = requests.Session()
    s.headers.update(BSE_HEADERS)
    s.get(f'https://www.bseindia.com/corporates/ann.html?scrip={bse_code}', timeout=15)

    presentations = []
    for page in range(1, 20):
        params = {
            'strScrip':    bse_code,
            'strCat':      '-1',
            'strPrevDate': f'{from_year}0101',
            'strToDate':   datetime.now().strftime('%Y%m%d'),
            'strType':     'C',
            'strSearch':   'P',
            'pageno':      str(page),
        }
        r = s.get('https://api.bseindia.com/BseIndiaAPI/api/AnnSubCategoryGetData/w',
                  params=params, timeout=20)
        data = r.json()
        if not data.get('Table'):
            break
        for e in data['Table']:
            subj = e.get('NEWSSUB', '')
            if ('Investor Presentation' in subj
                    and 'Intimation' not in subj
                    and 'Meet' not in subj):
                presentations.append({
                    'date':       e.get('NEWS_DT', '')[:10],
                    'attachment': e.get('ATTACHMENTNAME', ''),
                    'subject':    subj,
                })

    return sorted(presentations, key=lambda x: x['date'], reverse=True)


def download_pdf(attachment, out_path):
    """Download a BSE PDF. Tries AttachLive first, then AttachHis."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    for base in ['https://www.bseindia.com/xml-data/corpfiling/AttachLive/',
                 'https://www.bseindia.com/xml-data/corpfiling/AttachHis/']:
        try:
            r = requests.get(base + attachment, headers=headers, timeout=60)
            if r.status_code == 200 and 'pdf' in r.headers.get('Content-Type', '').lower():
                with open(out_path, 'wb') as f:
                    f.write(r.content)
                return True
        except Exception:
            continue
    return False


# ─── PDF PARSING UTILITIES ─────────────────────────────────────────────────────

def safe_float(s):
    if s is None:
        return None
    try:
        cleaned = str(s).replace(',', '').replace('₹', '').replace('%', '')
        cleaned = cleaned.replace('(', '-').replace(')', '').strip()
        return float(cleaned)
    except Exception:
        return None


def page_rows(page, y_tol=8):
    """Return rows of (word, x_mid) sorted by y then x_mid."""
    rows = {}
    for (x0, y0, x1, y1, word, *_) in page.get_text("words"):
        y_key = round((y0 + y1) / 2 / y_tol) * y_tol
        x_mid = (x0 + x1) / 2
        rows.setdefault(y_key, []).append((word, x_mid))
    return [sorted(rows[k], key=lambda t: t[1]) for k in sorted(rows)]


# Quarter label e.g. Q3FY26, and month names used as balance-sheet col headers
_QTR_PAT   = re.compile(r'Q[1-4]FY\d{2}')
_MONTH_PAT = re.compile(r'^(Dec|Mar|Jun|Sep)$')
_DATE_PAT  = re.compile(r'(Dec|Mar|Jun|Sep)-\d{2}$')


def find_col_xs(rows):
    """
    Find x-midpoints of column headers.
    Handles: Q3FY26 quarter labels and Jun-25 / Jun 30, 2024 date formats.
    Returns sorted list of x-mids (≥2 columns), or None.
    """
    for row in rows:
        row_text = ' '.join(w for w, _ in row)

        # Quarter labels: Q1FY25, Q4FY25 …
        if _QTR_PAT.search(row_text):
            xs = [x for w, x in row if _QTR_PAT.search(w)]
            if len(xs) >= 2:
                return sorted(xs)

        # Date columns: "Jun-25", "Dec-24" or month-word "Jun" "Dec" "Mar"
        months = [(w, x) for w, x in row
                  if _MONTH_PAT.match(w) or _DATE_PAT.match(w)]
        if len(months) >= 2:
            return sorted(x for _, x in months)

    return None


def assign_col(num_words, col_xs):
    """Assign each numeric word to nearest column x-mid."""
    n = len(col_xs)
    cols = [[] for _ in range(n)]
    for word, x in num_words:
        best = min(range(n), key=lambda i: abs(x - col_xs[i]))
        cols[best].append(word)
    return [safe_float(''.join(c)) for c in cols]


def is_numeric_word(w):
    return bool(re.match(r'^-?[\d,()]+\.?\d*$', w)) and any(c.isdigit() for c in w)


def extract_pct_from_row(row_text):
    """Extract all percentage values from a row of text."""
    return [float(m) for m in re.findall(r'([\d]+\.[\d]+)%?', row_text)
            if 0 < float(m) < 100]


def find_number_in_range(row_text, lo, hi):
    """Find first number in row_text that falls within [lo, hi]."""
    nums = re.findall(r'[\d,]+(?:\.\d+)?', row_text)
    for n in nums:
        v = safe_float(n)
        if v is not None and lo <= v <= hi:
            return v
    return None


# ─── GENERIC MULTI-FORMAT PARSER ───────────────────────────────────────────────

# Pattern: "₹ 4,066 crore" / "₹1,64,720 Crores" / "Rs.2,10,722 Cr"
_NARRATIVE_AMT = re.compile(
    r'(?:₹|Rs\.?)\s*([\d,]+(?:\.\d+)?)\s*(?:lakh\s*(?:Cr|crore)s?|Cr|Crs|crore|Crores?)\b',
    re.I
)
# Inline ₹ token without space: "₹55,017"
_INLINE_RS = re.compile(r'^₹([\d,]+(?:\.\d+)?)$')


def _parse_amount(text):
    """
    Extract first monetary amount in crore from a text snippet.
    Handles: ₹55,017  /  ₹ 4,066 crore  /  Rs.2,10,722 Cr  /  1,64,720 Crores
    Returns value in Cr, or None.
    """
    # lakh crore special case (multiply by 1e5)
    m = re.search(r'(?:₹|Rs\.?)\s*([\d,.]+)\s*lakh\s*(?:Cr|crore)s?', text, re.I)
    if m:
        v = safe_float(m.group(1))
        if v:
            return round(v * 1e5, 0)
    # Standard "₹/Rs + number + Cr" narrative
    m = _NARRATIVE_AMT.search(text)
    if m:
        return safe_float(m.group(1))
    return None


def _find_narrative_value(page_text, keyword_patterns, lo, hi, window=250):
    """
    Search for keyword in page text; return first numeric amount in [lo,hi]
    found within `window` characters after the keyword.
    """
    for kw_pat in keyword_patterns:
        for km in re.finditer(kw_pat, page_text, re.I):
            snippet = page_text[km.start(): km.start() + window]
            v = _parse_amount(snippet)
            if v and lo <= v <= hi:
                return v
            # Also check plain numbers followed by Cr in the snippet
            for nm in re.finditer(r'([\d,]+(?:\.\d+)?)\s*(?:Cr|crore)s?\b', snippet, re.I):
                v2 = safe_float(nm.group(1))
                if v2 and lo <= v2 <= hi:
                    return v2
    return None


def parse_pdf(pdf_path, face_value=2, lending_only=False):
    """
    Parse one investor presentation PDF.
    Returns dict of extracted quarterly metrics.
    Uses column-based parsing for structured tables + narrative extraction fallback.
    """
    doc = fitz.open(pdf_path)
    data = {}

    all_pages = [(i, doc[i], doc[i].get_text()) for i in range(len(doc))]

    # Find offset page for decks where first N pages are regulatory filings
    # (e.g. Shriram: investor update starts at p35 after financial statements)
    deck_start = _find_deck_start(all_pages)

    for page_num, page, page_text in all_pages[deck_start:]:
        rows = page_rows(page)

        # ── AUM / Loan Book ────────────────────────────────────────────────────
        if 'aum_cr' not in data and any(kw in page_text for kw in
                ['AUM', 'Assets Under Management', 'Loan Book', 'Gross Loan Book',
                 'Loan AUM', 'Business AUM', 'Retail Book']):
            aum = _extract_aum(rows, page_text, lending_only)
            if aum:
                data['aum_cr'] = aum

        # ── P&L: NII and PAT ──────────────────────────────────────────────────
        pl_keywords = [r'net interest income', r'profit after tax',
                       r'profit/\(loss\) after tax', r'\bnii\b', r'\bpat\b']
        if any(re.search(kw, page_text, re.I) for kw in pl_keywords):
            _extract_pl_page(rows, page_text, data, lending_only)

        # ── NIM % ─────────────────────────────────────────────────────────────
        if 'nim_pct' not in data and ('NIM' in page_text or 'NIMs' in page_text):
            for row in rows:
                rt = ' '.join(w for w, _ in row)
                if re.search(r'\bNIMs?\b', rt):
                    # Take LAST pct in range (latest quarter in a trend row)
                    pcts = [float(p) for p in re.findall(r'([\d]+\.[\d]+)', rt)
                            if 1 < float(p) < 20]
                    if pcts:
                        data['nim_pct'] = pcts[-1]

        # ── GNPA / NNPA % ─────────────────────────────────────────────────────
        if 'gnpa_pct' not in data or 'nnpa_pct' not in data:
            _extract_npa(rows, page_text, data)

        # ── ROA % ─────────────────────────────────────────────────────────────
        if 'roa_pct' not in data and re.search(r'Ro?A\b', page_text):
            for row in rows:
                rt = ' '.join(w for w, _ in row)
                if re.search(r'\bRo?A\b', rt, re.I) and not re.search(r'annuali[sz]', rt, re.I):
                    # Take last pct in range for trend rows; first for highlight rows
                    pcts = [float(p) for p in re.findall(r'([\d]+\.[\d]+)', rt)
                            if 0 < float(p) < 10]
                    if pcts:
                        data['roa_pct'] = pcts[-1]

        # ── ROE % ─────────────────────────────────────────────────────────────
        if 'roe_pct' not in data and re.search(r'Ro?E\b', page_text):
            for row in rows:
                rt = ' '.join(w for w, _ in row)
                if re.search(r'\bRo?E\b', rt, re.I):
                    pcts = [float(p) for p in re.findall(r'([\d]+\.[\d]+)', rt)
                            if 0 < float(p) < 80]
                    if pcts:
                        data['roe_pct'] = pcts[-1]

        # ── CAR / CRAR % ──────────────────────────────────────────────────────
        if 'car_pct' not in data and re.search(r'CRAR|Capital Adequacy', page_text):
            for row in rows:
                rt = ' '.join(w for w, _ in row)
                if re.search(r'CRAR|Capital\s+Adequacy', rt, re.I):
                    pcts = [float(p) for p in re.findall(r'([\d]+\.[\d]+)', rt)
                            if 10 < float(p) < 60]
                    if pcts:
                        data['car_pct'] = pcts[-1]

        # ── Disbursements ─────────────────────────────────────────────────────
        if 'disbursements_cr' not in data and 'Disbursement' in page_text:
            v = _find_narrative_value(
                page_text,
                [r'Disbursement'],
                500, 500_000
            )
            if v:
                data['disbursements_cr'] = v

        # ── Balance Sheet ─────────────────────────────────────────────────────
        if 'Balance Sheet' in page_text:
            col_xs = find_col_xs(rows)
            if col_xs:
                for row in rows:
                    rt = ' '.join(w for w, _ in row)
                    num_ws = [(w, x) for w, x in row if is_numeric_word(w)]
                    if not num_ws:
                        continue
                    if re.search(r'\bShare\b.*\bCapital\b', rt, re.I):
                        vals = assign_col(num_ws, col_xs)
                        if vals and vals[-1] and 'share_capital_cr' not in data:
                            data['share_capital_cr'] = vals[-1]
                    if re.search(r'\bReserve', rt, re.I) and re.search(r'\bSurplus\b', rt, re.I):
                        vals = assign_col(num_ws, col_xs)
                        if vals and vals[-1] and 'reserves_cr' not in data:
                            data['reserves_cr'] = vals[-1]

    doc.close()

    # ── Derived: Book Value per Share ──────────────────────────────────────────
    sc  = data.get('share_capital_cr')
    res = data.get('reserves_cr')
    if sc and res and sc > 0 and face_value:
        shares                       = (sc * 1e7) / face_value
        net_worth                    = sc + res
        data['net_worth_cr']         = round(net_worth, 1)
        data['shares_outstanding']   = int(shares)
        data['book_value_per_share'] = round((net_worth * 1e7) / shares, 2)

    return data


def _find_deck_start(all_pages):
    """
    Some PDFs (e.g. Shriram) bundle regulatory filings before the investor deck.
    Find the page index where the actual investor presentation slides begin.
    """
    markers = ['Investor Update', 'Investor Presentation', 'Q3 FY26',
               'Financial Highlights', 'Key Highlights']
    for i, (_, _, txt) in enumerate(all_pages):
        if any(m in txt for m in markers):
            return i
    return 0


def _extract_aum(rows, page_text, lending_only):
    """
    Extract AUM / Loan Book value in Crore.
    Handles: ₹ prefix (direct/space), Rs. prefix, lakh Cr, plain Cr suffix.

    Strategy:
    1. Row-based: find rows with AUM label + inline value.
    2. Page-wide: on pages with AUM keywords, take the LARGEST ₹/Rs value
       in [5_000, 800_000] Cr range (AUM is usually the biggest number shown).
    3. Narrative: keyword → look forward/backward for amount.
    """
    SKIP = ['Housing', 'Wealth', 'Insurance', 'AMC', 'Broking']
    AUM_LABELS = [
        r'\bAUM\b', r'Assets\s+Under\s+Management', r'Loan\s+AUM',
        r'Business\s+AUM', r'Gross\s+Loan\s+Book', r'Loan\s+Book',
        r'Retail\s+Book', r'Book\s+Size',
    ]

    if not any(re.search(lbl, page_text, re.I) for lbl in AUM_LABELS):
        return None

    # ── Collect ALL candidates from the full page ─────────────────────────────
    # AUM is typically the LARGEST number on its highlights page.
    # We collect all plausible values and return the maximum.
    candidates = []

    # Lakh crore patterns (highest priority — largest unit)
    for m in re.finditer(r'(?:₹|Rs\.?)\s*([\d,.]+)\s*lakh\s*(?:Cr|crore)', page_text, re.I):
        ctx = page_text[max(0, m.start()-80): m.start()]
        # Skip milestone/historical context ("crossed", "surpassed", etc.)
        if re.search(r'crossed|surpassed|milestone|first time|achieve', ctx, re.I):
            continue
        v = safe_float(m.group(1))
        if v:
            candidates.append(v * 1e5)

    # ₹XX,XXX (direct token) or ₹ XX,XXX (₹ separate word from number)
    for row in rows:
        rt = ' '.join(w for w, _ in row)
        if lending_only and any(kw in rt for kw in SKIP):
            continue
        for j, (word, x) in enumerate(row):
            if word == '₹' or _INLINE_RS.match(word):
                num_word = word if _INLINE_RS.match(word) else (row[j+1][0] if j+1 < len(row) else '')
                n = safe_float(num_word.lstrip('₹'))
                if n and 5_000 < n < 800_000:
                    candidates.append(n)

    # "Rs.2,10,722 Cr" or plain "2,10,722 Cr" patterns anywhere on page
    for m in re.finditer(r'Rs\.?\s*([\d,]+(?:\.\d+)?)\s*(?:Cr|crore)', page_text, re.I):
        v = safe_float(m.group(1))
        if v and 5_000 < v < 800_000:
            candidates.append(v)

    if candidates:
        return max(candidates)  # AUM is the largest financial figure on the page

    return None


def _extract_pl_page(rows, page_text, data, lending_only):
    """Extract NII and PAT from this page — handles column tables and narratives."""
    SKIP = ['Housing', 'Wealth', 'Insurance', 'AMC']

    col_xs = find_col_xs(rows)
    if col_xs:
        n_header_cols = sum(
            1 for row in rows
            for w, _ in row
            if _QTR_PAT.search(w)
        )
        # For annual P&L with 5 cols (Q4FY25), current quarter is 3rd column
        use_col_idx = 2 if n_header_cols >= 4 else -1

        # Track best NII: prefer "inc. fees" over plain NII
        nii_plain, nii_with_fees = None, None
        # Track best PAT: prefer "excl." over "incld."
        pat_plain, pat_excl = None, None

        for row in rows:
            rt = ' '.join(w for w, _ in row)
            if lending_only and any(kw in rt for kw in SKIP):
                continue
            num_ws = [(w, x) for w, x in row if is_numeric_word(w)]
            if not num_ws:
                continue
            vals = assign_col(num_ws, col_xs)

            def pick(vs):
                if not vs:
                    return None
                i = min(use_col_idx, len(vs)-1) if use_col_idx >= 0 else len(vs) + use_col_idx
                i = max(0, min(i, len(vs)-1))
                return vs[i]

            if _is_nii_row(rt):
                v = pick(vals)
                if v and 10 < v < 50_000:
                    if 'fee' in rt.lower() or 'inc.' in rt.lower():
                        nii_with_fees = v
                    else:
                        nii_plain = v

            if _is_pat_row(rt):
                v = pick(vals)
                if v is not None and abs(v) < 20_000:
                    if 'excl' in rt.lower():
                        pat_excl = v
                    elif 'incld' not in rt.lower():
                        pat_plain = v

        if 'nii_cr' not in data:
            nii = nii_with_fees or nii_plain
            if nii:
                data['nii_cr'] = nii
        if 'pat_cr' not in data:
            pat = pat_excl if pat_excl is not None else pat_plain
            if pat is not None:
                data['pat_cr'] = pat

    # Narrative fallback for companies using "₹ X,XXX crore" format (Bajaj, Muthoot)
    if 'nii_cr' not in data:
        nii = _find_narrative_value(
            page_text,
            [r'Net\s+Interest\s+Income', r'\bNII\b'],
            50, 50_000
        )
        if nii:
            data['nii_cr'] = nii

    if 'pat_cr' not in data:
        # Prefer "standalone" PAT over "consolidated" in narrative
        # Search for "Profit after tax.*?₹ X,XXX crore" or similar
        pat = _find_narrative_value(
            page_text,
            [r'[Ss]tandalone\s+[Pp]rofit\s+[Aa]fter\s+[Tt]ax',
             r'[Pp]rofit\s+after\s+[Tt]ax.*?Q3',
             r'[Pp]rofit\s+after\s+[Tt]ax.*?quarter',
             r'[Pp]rofit\s+after\s+[Tt]ax\s*\(PAT\)',
             r'consolidated\s+profit\s+after\s+tax.*?Q3'],
            10, 20_000
        )
        if pat is not None:
            data['pat_cr'] = pat


def _extract_npa(rows, page_text, data):
    """Extract GNPA% and NNPA% from NPA section rows."""
    for row in rows:
        rt = ' '.join(w for w, _ in row)
        if re.search(r'Gross\s+NPA\s*\(%\)|GNPA\s*\(%\)', rt):
            pcts = re.findall(r'([\d]+\.[\d]+)', rt)
            if pcts and 'gnpa_pct' not in data:
                data['gnpa_pct'] = float(pcts[-1])
        if re.search(r'Net\s+NPA\s*\(%\)|NNPA\s*\(%\)', rt):
            pcts = re.findall(r'([\d]+\.[\d]+)', rt)
            if pcts and 'nnpa_pct' not in data:
                data['nnpa_pct'] = float(pcts[-1])

    # Narrative: "GNPA & NNPA stood at 1.21% & 0.47%"  (first = GNPA, second = NNPA)
    if 'gnpa_pct' not in data or 'nnpa_pct' not in data:
        m = re.search(
            r'GNPA\s*[&and,]+\s*NNPA\D{0,20}([\d]+\.[\d]+)\s*%\s*[&and,]+\s*([\d]+\.[\d]+)\s*%',
            page_text, re.I)
        if m:
            g, n = float(m.group(1)), float(m.group(2))
            if 0 < g < 20 and 'gnpa_pct' not in data:
                data['gnpa_pct'] = g
            if 0 < n < 20 and 'nnpa_pct' not in data:
                data['nnpa_pct'] = n

    if 'gnpa_pct' not in data:
        for pat in [r'GNPA\D{0,20}([\d]+\.[\d]+)\s*%',
                    r'Gross\s+NPA[^%\d]{0,30}([\d]+\.[\d]+)\s*%']:
            m = re.search(pat, page_text, re.I)
            if m:
                v = float(m.group(1))
                if 0 < v < 20:
                    data['gnpa_pct'] = v
                    break

    if 'nnpa_pct' not in data:
        for pat in [r'NNPA\D{0,20}([\d]+\.[\d]+)\s*%',
                    r'Net\s+NPA[^%\d]{0,30}([\d]+\.[\d]+)\s*%']:
            m = re.search(pat, page_text, re.I)
            if m:
                v = float(m.group(1))
                if 0 < v < 20:
                    data['nnpa_pct'] = v
                    break

    # Stage 3 proxy when standard NPA labels absent
    if 'gnpa_pct' not in data:
        for row in rows:
            rt = ' '.join(w for w, _ in row)
            if 'Stage 3' in rt and re.search(r'Ratio|%|Asset', rt):
                pcts = re.findall(r'([\d]+\.[\d]+)', rt)
                if pcts:
                    v = float(pcts[-1])
                    if 0 < v < 20:
                        data['gnpa_pct'] = v
                        data['gnpa_note'] = 'Stage 3 ratio'
                        break


def _count_header_cols(rows):
    """Count number of quarter/date column headers found."""
    for row in rows:
        rt = ' '.join(w for w, _ in row)
        if _QTR_PAT.search(rt):
            return len([w for w, _ in row if _QTR_PAT.search(w)])
    return 2


def _is_nii_row(row_text):
    return bool(
        re.search(r'\bNII\b', row_text) or
        re.search(r'Net\s+Interest\s+Income', row_text, re.I)
    )


def _is_pat_row(row_text):
    # Fix: use \b and allow non-space between Profit and Tax (Profit/(Loss) after Tax)
    return bool(
        re.search(r'\bProfit\b.{0,25}\bTax\b', row_text, re.I) and
        'before' not in row_text.lower()
    )


# ─── MAIN PIPELINE ─────────────────────────────────────────────────────────────

def run(company_key):
    cfg  = COMPANIES[company_key]
    code = cfg['bse_code']
    fv   = cfg.get('face_value', 2)
    name = cfg['name']
    lo   = cfg.get('lending_only', False)

    pdf_company_dir = os.path.join(PDF_DIR, company_key)
    os.makedirs(pdf_company_dir, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  {name}  (BSE {code})")
    print(f"{'='*60}")

    # 1 — discover
    print("[1] Fetching presentation list …")
    presentations = fetch_presentation_list(code)
    print(f"    {len(presentations)} presentations found")

    # Deduplicate by filing month (keep latest per month)
    seen_months, unique_pres = set(), []
    for p in presentations:
        m = p['date'][:7]
        if m not in seen_months:
            seen_months.add(m)
            unique_pres.append(p)

    target = unique_pres[:NUM_QUARTERS]
    for p in target:
        print(f"    {p['date']}  {p['attachment'][:40]}")

    # 2 — download
    print("[2] Downloading PDFs …")
    pdf_paths = []
    for p in target:
        date_str = p['date'][:7].replace('-', '')
        out_path = os.path.join(pdf_company_dir, f"{date_str}.pdf")
        pdf_paths.append((p['date'], out_path))
        if os.path.exists(out_path):
            print(f"    {date_str}.pdf  cached ({os.path.getsize(out_path):,} B)")
        else:
            ok = download_pdf(p['attachment'], out_path)
            sz = os.path.getsize(out_path) if ok else 0
            print(f"    {date_str}.pdf  {'OK' if ok else 'FAILED'}  ({sz:,} B)")

    # 3 — parse
    print("[3] Parsing …")
    quarters = []
    for filing_date, pdf_path in pdf_paths:
        if not os.path.exists(pdf_path):
            print(f"    SKIP {pdf_path}")
            continue
        print(f"    {os.path.basename(pdf_path)} … ", end='', flush=True)
        metrics = parse_pdf(pdf_path, face_value=fv, lending_only=lo)
        metrics['filing_date'] = filing_date
        quarters.append(metrics)
        aum = metrics.get('aum_cr', '?')
        nii = metrics.get('nii_cr', '?')
        pat = metrics.get('pat_cr', '?')
        bv  = metrics.get('book_value_per_share', '?')
        print(f"AUM={aum}  NII={nii}  PAT={pat}  BV=₹{bv}")

    # 4 — write JSON
    output = {
        'company':      name,
        'bse_code':     code,
        'nse_symbol':   cfg['nse_symbol'],
        'face_value':   fv,
        'last_updated': datetime.now().isoformat(),
        'quarters':     quarters,
    }
    out_file = os.path.join(DATA_DIR, f'{company_key}.json')
    with open(out_file, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"[4] Saved → {out_file}  ({len(quarters)} quarters)\n")
    return output


def run_all():
    results = {}
    for key in COMPANIES:
        try:
            results[key] = run(key)
        except Exception as e:
            print(f"ERROR processing {key}: {e}")
    return results


def print_summary_table(all_results):
    """Print a cross-company metrics table to stdout."""
    METRICS = [
        ('aum_cr',              'AUM (₹Cr)'),
        ('nii_cr',              'NII (₹Cr)'),
        ('nim_pct',             'NIM %'),
        ('pat_cr',              'PAT (₹Cr)'),
        ('gnpa_pct',            'GNPA %'),
        ('nnpa_pct',            'NNPA %'),
        ('roa_pct',             'ROA %'),
        ('roe_pct',             'ROE %'),
        ('car_pct',             'CAR %'),
        ('disbursements_cr',    'Disbursements (₹Cr)'),
        ('book_value_per_share','BV/Share (₹)'),
    ]

    companies_order = list(COMPANIES.keys())
    short_names = {
        'poonawalla': 'Poonawalla',
        'bajaj':      'Bajaj Fin',
        'shriram':    'Shriram',
        'ltf':        'L&T Fin',
        'chola':      'Chola',
        'abcapital':  'AB Capital',
        'piramal':    'Piramal',
        'muthoot':    'Muthoot',
        'mahindra':   'Mahindra',
    }

    print("\n" + "="*120)
    print("LATEST QUARTER METRICS (Q3FY26 wherever available)")
    print("="*120)

    # Header
    header = f"{'Metric':<26}" + ''.join(f"{short_names.get(k,'?'):>12}" for k in companies_order)
    print(header)
    print("-"*120)

    for field, label in METRICS:
        row = f"{label:<26}"
        for key in companies_order:
            res = all_results.get(key, {})
            qtrs = res.get('quarters', [{}])
            latest = qtrs[0] if qtrs else {}
            val = latest.get(field)
            if val is None:
                row += f"{'—':>12}"
            elif field in ('aum_cr', 'nii_cr', 'pat_cr', 'disbursements_cr'):
                row += f"{val:>12,.0f}"
            elif field == 'book_value_per_share':
                row += f"{val:>12.2f}"
            else:
                row += f"{val:>11.2f}%"
        print(row)

    print("\n" + "="*120)
    print("5-QUARTER AUM TREND (₹ Cr) — newest to oldest")
    print("="*120)
    print(f"{'Quarter':<26}" + ''.join(f"{short_names.get(k,'?'):>12}" for k in companies_order))
    print("-"*120)
    for q_idx in range(NUM_QUARTERS):
        row = f"{'Q'+str(q_idx+1):<26}"
        for key in companies_order:
            qtrs = all_results.get(key, {}).get('quarters', [])
            val = qtrs[q_idx].get('aum_cr') if q_idx < len(qtrs) else None
            row += f"{val:>12,.0f}" if val else f"{'—':>12}"
        print(row)

    print("\n" + "="*120)
    print("5-QUARTER PAT TREND (₹ Cr)")
    print("="*120)
    print(f"{'Quarter':<26}" + ''.join(f"{short_names.get(k,'?'):>12}" for k in companies_order))
    print("-"*120)
    for q_idx in range(NUM_QUARTERS):
        row = f"{'Q'+str(q_idx+1):<26}"
        for key in companies_order:
            qtrs = all_results.get(key, {}).get('quarters', [])
            val = qtrs[q_idx].get('pat_cr') if q_idx < len(qtrs) else None
            row += f"{val:>12,.0f}" if val is not None else f"{'—':>12}"
        print(row)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in COMPANIES:
        results = {sys.argv[1]: run(sys.argv[1])}
    else:
        results = run_all()
    print_summary_table(results)
