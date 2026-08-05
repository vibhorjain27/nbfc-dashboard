#!/usr/bin/env python3
"""
Roll nbfc_data_cache.py forward by one quarter, keeping a fixed 8-quarter window.

Appends a new quarter to every series in NBFC_TIMESERIES, then drops the oldest
columns so the dashboard always shows the last 8 quarters. Rewrites the file in
place, preserving alignment and every trailing source comment.

Usage
-----
  # 1. put the quarter's numbers in a JSON file (see QUARTER_TEMPLATE below)
  python roll_quarter.py --quarter Q1FY27 --data q1fy27.json

  # dry run — prints the diff without touching the file
  python roll_quarter.py --quarter Q1FY27 --data q1fy27.json --dry-run

  # emit a blank template to fill in
  python roll_quarter.py --template > q1fy27.json

JSON shape: {"<company>": {"<metric>": value|null, ...}, ...}
Companies not listed, or metrics set to null, are stored as None (a gap) —
never interpolated.
"""

import argparse
import ast
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, 'nbfc_data_cache.py')

KEEP = 8          # rolling window: how many quarters the dashboard shows

METRICS = [
    'aum_cr', 'gnpa_pct', 'nnpa_pct', 'pcr_pct', 'pat_cr', 'nim_pct',
    'roa_pct', 'roe_pct', 'cost_of_borrowing_pct', 'd_e_ratio',
    'car_pct', 't1_pct', 't2_pct', 'bvps_inr',
]

COMPANIES = [
    'Poonawalla Fincorp', 'Bajaj Finance', 'Shriram Finance', 'Chola Finance',
    'Aditya Birla Capital', 'L&T Finance', 'Piramal Finance', 'Muthoot Finance',
    'Mahindra Finance',
]

# A metric line inside NBFC_TIMESERIES, e.g.
#     "aum_cr":                [25003,  26972,  … ],  # optional comment
LINE_RE = re.compile(
    r'^(?P<indent>\s*)"(?P<metric>\w+)":(?P<pad>\s*)'
    r'\[(?P<values>[^\]]*)\](?P<comma>,)(?P<comment>\s*#.*)?$'
)
COMPANY_RE = re.compile(r'^\s{4}"(?P<name>[^"]+)":\s*\{\s*$')
QUARTERS_RE = re.compile(r'^QUARTERS\s*=\s*\[.*\]\s*$')


def fmt(v):
    """Render one cell the way the file already writes them."""
    if v is None:
        return 'None'
    if isinstance(v, float):
        s = f'{v:.2f}'.rstrip('0').rstrip('.')
        return s if s else '0'
    return str(v)


def render(values, indent, metric, pad):
    """Rebuild a metric line body with column alignment.

    Every cell except the last carries its separating comma *before* padding,
    so the columns line up and the list stays valid Python.
    """
    raw = [fmt(v) for v in values]
    width = max(max((len(c) for c in raw), default=1) + 2, 7)
    cells = [(c + ',').ljust(width) for c in raw[:-1]] + [raw[-1]]
    return f'{indent}"{metric}":{pad}[{"".join(cells)}]'


def roll(text, new_quarter, data, keep=KEEP):
    lines = text.split('\n')
    out = []
    company = None
    in_series = False
    changed = 0
    report = []

    for line in lines:
        if QUARTERS_RE.match(line):
            quarters = ast.literal_eval(line.split('=', 1)[1].strip())
            if new_quarter in quarters:
                raise SystemExit(f'{new_quarter} is already present — nothing to do.')
            quarters = (quarters + [new_quarter])[-keep:]
            out.append('QUARTERS = ' + json.dumps(quarters).replace('", "', '", "'))
            report.append(f'QUARTERS -> {quarters}')
            continue

        if 'NBFC_TIMESERIES' in line and '=' in line:
            in_series = True
        if in_series:
            m = COMPANY_RE.match(line)
            if m:
                company = m.group('name')

        m = LINE_RE.match(line) if in_series else None
        if m and company and m.group('metric') in METRICS:
            values = ast.literal_eval('[' + m.group('values') + ']')
            new_val = (data.get(company) or {}).get(m.group('metric'))
            values = (values + [new_val])[-keep:]
            rebuilt = render(values, m.group('indent'), m.group('metric'), m.group('pad'))
            out.append(rebuilt + m.group('comma') + (m.group('comment') or ''))
            changed += 1
            continue

        # keep the "list of N values" note honest
        if re.match(r'^# Each entry: list of \d+ values', line):
            out.append(f'# Each entry: list of {keep} values aligned to QUARTERS above')
            continue

        out.append(line)

    return '\n'.join(out), changed, report


def fill(text, quarter, data):
    """Write values into an EXISTING quarter column, leaving the window alone.

    Companies report on different dates, so the usual flow is: roll the window
    once when the first company reports, then fill the rest in as they arrive.
    Only metrics present in `data` are touched — everything else keeps its
    current value, so re-running is safe.
    """
    lines = text.split('\n')
    out = []
    company = None
    in_series = False
    touched = 0
    idx = None

    for line in lines:
        if QUARTERS_RE.match(line):
            quarters = ast.literal_eval(line.split('=', 1)[1].strip())
            if quarter not in quarters:
                raise SystemExit(
                    f'{quarter} is not in the current window {quarters}.\n'
                    f'Use the default roll mode to add it.')
            idx = quarters.index(quarter)
            out.append(line)
            continue

        if 'NBFC_TIMESERIES' in line and '=' in line:
            in_series = True
        if in_series:
            m = COMPANY_RE.match(line)
            if m:
                company = m.group('name')

        m = LINE_RE.match(line) if in_series else None
        if m and company and m.group('metric') in METRICS and idx is not None:
            metric = m.group('metric')
            entry = data.get(company) or {}
            if metric in entry:
                values = ast.literal_eval('[' + m.group('values') + ']')
                values[idx] = entry[metric]
                rebuilt = render(values, m.group('indent'), metric, m.group('pad'))
                out.append(rebuilt + m.group('comma') + (m.group('comment') or ''))
                touched += 1
                continue

        out.append(line)

    return '\n'.join(out), touched, idx


def coverage(text, quarter):
    """{company: count of non-None metrics} for `quarter`, read off file text."""
    lines = text.split('\n')
    counts = {c: 0 for c in COMPANIES}
    company = None
    in_series = False
    idx = None

    for line in lines:
        if QUARTERS_RE.match(line):
            quarters = ast.literal_eval(line.split('=', 1)[1].strip())
            idx = quarters.index(quarter) if quarter in quarters else None
            continue
        if 'NBFC_TIMESERIES' in line and '=' in line:
            in_series = True
        if in_series:
            m = COMPANY_RE.match(line)
            if m:
                company = m.group('name')
            m2 = LINE_RE.match(line)
            if m2 and company in counts and m2.group('metric') in METRICS and idx is not None:
                values = ast.literal_eval('[' + m2.group('values') + ']')
                if idx < len(values) and values[idx] is not None:
                    counts[company] += 1
    return counts


def template():
    return json.dumps({c: {m: None for m in METRICS} for c in COMPANIES}, indent=2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--quarter', help='new quarter label, e.g. Q1FY27')
    ap.add_argument('--data', help='JSON file of {company: {metric: value}}')
    ap.add_argument('--keep', type=int, default=KEEP)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--template', action='store_true')
    ap.add_argument('--fill', action='store_true',
                    help='fill an existing quarter column instead of rolling a new one')
    a = ap.parse_args()

    if a.template:
        print(template())
        return 0
    if not a.quarter or not a.data:
        ap.error('--quarter and --data are required (or use --template)')

    with open(a.data, encoding='utf-8') as fh:
        data = json.load(fh)

    unknown = [c for c in data if c not in COMPANIES]
    if unknown:
        raise SystemExit(f'Unknown company key(s): {unknown}\nExpected one of: {COMPANIES}')

    with open(CACHE, encoding='utf-8') as fh:
        text = fh.read()

    if a.fill:
        new_text, changed, idx = fill(text, a.quarter, data)
        print(f'Filled {a.quarter} (column {idx}) — {changed} values written for '
              f'{", ".join(sorted(data))}')
    else:
        new_text, changed, report = roll(text, a.quarter, data, a.keep)
        for r in report:
            print(r)
        print(f'{changed} metric lines rewritten '
              f'({len(COMPANIES)} companies x {len(METRICS)} metrics)')

    filled = coverage(new_text, a.quarter)

    # Coverage is read back off the RESULT, not the input file — otherwise a
    # fill for one company looks like every other company just lost its data.
    print(f'\n{a.quarter} coverage (whole file after this change):')
    for c in COMPANIES:
        n = filled[c]
        flag = '' if n == len(METRICS) else ('  <- none yet' if n == 0 else '  <- partial')
        print(f'  {c:24s} {n:>2d}/{len(METRICS)}{flag}')
    total = sum(filled.values())
    print(f'  {"":24s} {total:>2d}/{len(COMPANIES) * len(METRICS)} overall')

    if a.dry_run:
        print('\n(dry run — file not written)')
        return 0

    with open(CACHE, 'w', encoding='utf-8') as fh:
        fh.write(new_text)
    print(f'\nWrote {CACHE}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
