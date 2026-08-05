#!/usr/bin/env python3
"""
Update a book value in book-values.json without hand-editing JSON.

    python pb-dashboard/tools/set_book_value.py CHOLAFIN 392 --as-of Q2FY27
    python pb-dashboard/tools/set_book_value.py SHRIRAMFIN 470 --as-of Q2FY27 --shares 2600000000
    python pb-dashboard/tools/set_book_value.py --list

Rewrites only the fields you pass, keeps key order and the file's comments, and
prints the before/after so a typo is obvious before you commit. Then:

    git add pb-dashboard/book-values.json && git commit && git push
"""

import argparse
import json
import os
import sys
from datetime import date

STORE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'book-values.json')


def load():
    with open(STORE, encoding='utf-8') as fh:
        return json.load(fh)


def save(data):
    with open(STORE, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write('\n')


def show(data):
    print(f'{"SYMBOL":<12} {"BVPS":>10}  {"AS OF":<8} COMPANY')
    print('-' * 58)
    for c in data['companies']:
        bv = f'{c["bvps"]:,.2f}' if c.get('bvps') else '—'
        print(f'{c["symbol"]:<12} {bv:>10}  {c.get("asOf") or "—":<8} {c["name"]}')
    print(f'\nupdated: {data.get("updated")}')


def main():
    p = argparse.ArgumentParser(description='Update a book value for the P/B dashboard.')
    p.add_argument('symbol', nargs='?', help='NSE symbol, e.g. CHOLAFIN')
    p.add_argument('bvps', nargs='?', type=float, help='Book value per share, in ₹')
    p.add_argument('--as-of', dest='as_of', help="Quarter the figure came from, e.g. Q2FY27")
    p.add_argument('--shares', type=int, help='Shares outstanding (market cap only, never P/B)')
    p.add_argument('--note', help='Free-text note shown when the row is expanded')
    p.add_argument('--list', action='store_true', help='Show the current store and exit')
    args = p.parse_args()

    data = load()

    if args.list or not args.symbol:
        show(data)
        return 0

    sym = args.symbol.upper()
    match = next((c for c in data['companies'] if c['symbol'].upper() == sym), None)
    if match is None:
        known = ', '.join(c['symbol'] for c in data['companies'])
        print(f'error: {sym} is not in the store.\nKnown symbols: {known}', file=sys.stderr)
        return 1

    if args.bvps is None and args.shares is None and args.note is None and args.as_of is None:
        print(f'error: nothing to change. Pass a BVPS value, --as-of, --shares or --note.', file=sys.stderr)
        return 1

    if args.bvps is not None and args.bvps <= 0:
        print('error: BVPS must be positive.', file=sys.stderr)
        return 1

    before = dict(match)

    if args.bvps is not None:
        old = match.get('bvps')
        match['bvps'] = args.bvps
        # A book value that moves more than half in one quarter is usually a typo
        # or a capital event — worth a look either way.
        if old:
            chg = (args.bvps - old) / old * 100
            if abs(chg) > 50:
                print(f'  ! {sym} BVPS moves {chg:+.0f}% ({old:,.2f} -> {args.bvps:,.2f}). '
                      f'Confirm this is a real capital event, not a typo.')
    if args.as_of:
        match['asOf'] = args.as_of
    if args.shares is not None:
        match['shares'] = args.shares
        match['sharesAsOf'] = date.today().strftime('%Y-%m')
    if args.note is not None:
        match['note'] = args.note

    data['updated'] = date.today().isoformat()
    save(data)

    print(f'{match["name"]} ({sym})')
    for field in ('bvps', 'asOf', 'shares', 'sharesAsOf', 'note'):
        if before.get(field) != match.get(field):
            print(f'  {field:<11} {before.get(field)!r}  ->  {match.get(field)!r}')
    print(f'\nWrote {STORE}')
    print('Commit and push — Netlify redeploys and the dashboard picks it up.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
