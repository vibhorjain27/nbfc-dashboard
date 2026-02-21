#!/usr/bin/env python3
"""
Data pipeline: Downloads Poonawalla Fincorp investor presentations from BSE India
and extracts key financial metrics for the NBFC dashboard.

Run quarterly after new results are published:
    python3 fetch_presentations.py

Extend to other NBFCs by adding entries to COMPANIES dict.
"""

import os, re, json, sys
import requests
import fitz  # PyMuPDF
from datetime import datetime

# ─── CONFIG ────────────────────────────────────────────────────────────────────

COMPANIES = {
    'poonawalla': {
        'name':        'Poonawalla Fincorp',
        'bse_code':    '524000',
        'face_value':  2,       # ₹ per share
        'nse_symbol':  'POONAWALLA',
    },
}

PDF_DIR  = os.path.join(os.path.dirname(__file__), 'data', 'pdfs')
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
NUM_QUARTERS = 5

BSE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept':     'application/json, text/plain, */*',
    'Referer':    'https://www.bseindia.com/corporates/ann.html',
    'Origin':     'https://www.bseindia.com',
}

# ─── BSE DISCOVERY ─────────────────────────────────────────────────────────────

def fetch_presentation_list(bse_code, from_year=2022):
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
            if 'Investor Presentation' in subj and 'Intimation' not in subj and 'Meet' not in subj:
                presentations.append({
                    'date':       e.get('NEWS_DT', '')[:10],
                    'attachment': e.get('ATTACHMENTNAME', ''),
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


# ─── PDF PARSING ───────────────────────────────────────────────────────────────

def safe_float(s):
    if s is None: return None
    try:
        return float(str(s).replace(',', '').replace('₹', '').replace('(', '-')
                     .replace(')', '').strip())
    except:
        return None


def page_rows(page, y_tol=8):
    """Return rows of (word, x_mid) sorted by y then x_mid."""
    rows = {}
    for (x0, y0, x1, y1, word, *_) in page.get_text("words"):
        y_key = round((y0 + y1) / 2 / y_tol) * y_tol
        x_mid = (x0 + x1) / 2
        rows.setdefault(y_key, []).append((word, x_mid))
    return [sorted(rows[k], key=lambda t: t[1]) for k in sorted(rows)]


# Quarter label pattern e.g. Q3FY26
_QTR_PAT   = re.compile(r'Q[1-4]FY\d{2}')
# Month name for balance-sheet date columns e.g. "Dec", "Mar", "Jun", "Sep"
_MONTH_PAT = re.compile(r'^(Dec|Mar|Jun|Sep)$')


def find_col_xs(rows, patterns):
    """
    Find x-midpoints of column headers.
    Handles quarter labels (Q3FY26) and date rows (Jun 30, 2024 / Jun-25).
    Returns sorted list of x-mids, or None.
    """
    for row in rows:
        row_text = ' '.join(w for w, _ in row)

        # Quarter labels: Q1FY25, Q4FY25, Q1FY26 …
        if _QTR_PAT.search(row_text):
            xs = [x for w, x in row if _QTR_PAT.search(w)]
            if len(xs) >= 2:
                return sorted(xs)

        # Date columns: "Jun 30, 2024  Mar 31, 2025  Jun 30, 2025"
        # or short form: "Jun-25  Dec-24"
        months = [(w, x) for w, x in row
                  if _MONTH_PAT.match(w) or re.match(r'(Dec|Mar|Jun|Sep)-\d{2}$', w)]
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
    return bool(re.match(r'^-?[\d,()]+$', w)) and any(c.isdigit() for c in w)


def parse_pdf(pdf_path, face_value=2):
    """
    Parse one investor presentation PDF.
    Returns dict with all extractable quarterly metrics.
    """
    doc  = fitz.open(pdf_path)
    data = {}

    for page_num in range(len(doc)):
        page      = doc[page_num]
        page_text = page.get_text()
        rows      = page_rows(page)

        # ── AUM from Financial Highlights page ─────────────────────────────────
        if 'Financial Highlights' in page_text and 'AUM' in page_text:
            for row in rows:
                for word, x in row:
                    # AUM appears as ₹55,017 or ₹30,984 etc.
                    if word.startswith('₹'):
                        n = safe_float(word[1:])   # strip ₹
                        if n and 5_000 < n < 500_000:
                            data.setdefault('aum_cr', n)
                            break

        # ── Balance Sheet ───────────────────────────────────────────────────────
        if 'Balance Sheet' in page_text:
            # Find date column headers like Dec-24, Sep-25, Jun-25 ...
            col_xs = find_col_xs(rows, [r'(Dec|Mar|Jun|Sep)-\d{2}'])
            if col_xs:
                for row in rows:
                    row_text = ' '.join(w for w, _ in row)
                    num_ws   = [(w, x) for w, x in row if is_numeric_word(w)]

                    if re.search(r'\bShare\b.*\bCapital\b', row_text, re.I):
                        vals = assign_col(num_ws, col_xs)
                        if vals and vals[-1]: data['share_capital_cr'] = vals[-1]

                    if re.search(r'\bReserve', row_text, re.I) and re.search(r'\bSurplus\b', row_text, re.I):
                        vals = assign_col(num_ws, col_xs)
                        if vals and vals[-1]: data['reserves_cr'] = vals[-1]

        # ── Profit & Loss (current quarter = rightmost column) ─────────────────
        if 'Profit/(Loss) after Tax' in page_text or 'Profit after Tax' in page_text:
            col_xs = find_col_xs(rows, [r'Q[1-4]FY\d{2}'])
            if col_xs:
                for row in rows:
                    row_text = ' '.join(w for w, _ in row)
                    num_ws   = [(w, x) for w, x in row if is_numeric_word(w)]

                    # Use the "excl. exceptional" line when both variants present
                    if ('after Tax' in row_text and 'Incld' not in row_text and
                            'Exceptional' not in row_text and 'Exception' not in row_text):
                        vals = assign_col(num_ws, col_xs)
                        if vals and vals[-1] and 'pat_cr' not in data:
                            data['pat_cr'] = abs(vals[-1])

                    if 'NII (inc.' in row_text or ('NII' in row_text and 'fees' in row_text):
                        vals = assign_col(num_ws, col_xs)
                        if vals and vals[-1] and 'nii_cr' not in data:
                            data['nii_cr'] = vals[-1]

        # ── Asset Quality ───────────────────────────────────────────────────────
        if 'Gross NPA (%)' in page_text:
            for row in rows:
                row_text = ' '.join(w for w, _ in row)
                if 'Gross NPA (%)' in row_text:
                    pcts = re.findall(r'([\d.]+)%', row_text)
                    if pcts: data['gnpa_pct'] = float(pcts[-1])
                if 'Net NPA (%)' in row_text:
                    pcts = re.findall(r'([\d.]+)%', row_text)
                    if pcts: data['nnpa_pct'] = float(pcts[-1])

        # ── ROA ─────────────────────────────────────────────────────────────────
        if 'RoA' in page_text and 'roa_pct' not in data:
            # Look specifically in a row where RoA is a standalone label
            for row in rows:
                row_text = ' '.join(w for w, _ in row)
                m = re.match(r'^RoA\s+([\d.]+)%', row_text)
                if m:
                    data['roa_pct'] = float(m.group(1))
                    break

    doc.close()

    # ── Compute Book Value per Share ────────────────────────────────────────────
    sc  = data.get('share_capital_cr')
    res = data.get('reserves_cr')
    if sc and res and sc > 0:
        shares            = (sc * 1e7) / face_value
        net_worth         = sc + res
        data['net_worth_cr']         = round(net_worth, 1)
        data['shares_outstanding']   = int(shares)
        data['book_value_per_share'] = round((net_worth * 1e7) / shares, 2)

    return data


# ─── MAIN PIPELINE ─────────────────────────────────────────────────────────────

def run(company_key='poonawalla'):
    cfg   = COMPANIES[company_key]
    code  = cfg['bse_code']
    fv    = cfg['face_value']
    name  = cfg['name']

    pdf_company_dir = os.path.join(PDF_DIR, company_key)
    os.makedirs(pdf_company_dir, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"Pipeline: {name}  (BSE {code})")
    print(f"{'='*60}")

    # Step 1 — discover
    print("\n[1] Fetching presentation list from BSE API …")
    presentations = fetch_presentation_list(code)
    print(f"    Found {len(presentations)} investor presentations")

    # Deduplicate by filing month (keep first/latest per month)
    seen_months = set()
    unique_pres = []
    for p in presentations:
        m = p['date'][:7]   # YYYY-MM
        if m not in seen_months:
            seen_months.add(m)
            unique_pres.append(p)
    
    target = unique_pres[:NUM_QUARTERS]
    print(f"    Using most recent {len(target)} unique quarters:")
    for p in target:
        print(f"      {p['date']}  {p['attachment']}")

    # Step 2 — download
    print("\n[2] Downloading PDFs …")
    pdf_paths = []
    for p in target:
        date_str  = p['date'][:7].replace('-', '')   # YYYYMM
        out_path  = os.path.join(pdf_company_dir, f"{date_str}.pdf")
        pdf_paths.append((p['date'], out_path))
        if os.path.exists(out_path):
            print(f"    {date_str}.pdf  already cached ({os.path.getsize(out_path):,} B)")
        else:
            ok = download_pdf(p['attachment'], out_path)
            sz = os.path.getsize(out_path) if ok else 0
            print(f"    {date_str}.pdf  {'OK' if ok else 'FAILED'}  ({sz:,} B)")

    # Step 3 — parse
    print("\n[3] Parsing PDFs …")
    quarters = []
    for filing_date, pdf_path in pdf_paths:
        if not os.path.exists(pdf_path):
            print(f"    SKIP {pdf_path} (missing)")
            continue
        print(f"    Parsing {os.path.basename(pdf_path)} …", end=' ', flush=True)
        metrics = parse_pdf(pdf_path, face_value=fv)
        metrics['filing_date'] = filing_date
        quarters.append(metrics)
        bv = metrics.get('book_value_per_share', '?')
        aum = metrics.get('aum_cr', '?')
        pat = metrics.get('pat_cr', '?')
        print(f"AUM={aum}  PAT={pat}  BV/share=₹{bv}")

    # Step 4 — write JSON
    output = {
        'company':       name,
        'bse_code':      code,
        'nse_symbol':    cfg['nse_symbol'],
        'face_value':    fv,
        'last_updated':  datetime.now().isoformat(),
        'quarters':      quarters,
    }
    out_file = os.path.join(DATA_DIR, f'{company_key}.json')
    with open(out_file, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\n[4] Saved → {out_file}  ({len(quarters)} quarters)")
    return output


if __name__ == '__main__':
    company = sys.argv[1] if len(sys.argv) > 1 else 'poonawalla'
    result  = run(company)
    print("\nFinal extracted data:")
    for q in result['quarters']:
        print(f"\n  Filing: {q.get('filing_date')}")
        for k in ['aum_cr','nii_cr','pat_cr','gnpa_pct','nnpa_pct','roa_pct',
                  'share_capital_cr','reserves_cr','book_value_per_share']:
            print(f"    {k:30s}: {q.get(k, '—')}")
