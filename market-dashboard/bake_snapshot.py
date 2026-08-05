#!/usr/bin/env python3
"""
Incrementally bake the fallback price snapshot into assets/data.js.

Yahoo rate-limits hard and recovers in narrow windows — often only one request
gets through before it blocks again. Fetching all nine tickers in one pass
therefore fails almost every time. This script instead grabs whatever it can on
each pass, writes it to disk immediately, and keeps retrying only the tickers
still missing. Progress survives restarts.

    python market-dashboard/bake_snapshot.py            # until complete
    python market-dashboard/bake_snapshot.py --once     # single pass
    python market-dashboard/bake_snapshot.py --gap 90   # seconds between tries
"""

import json
import os
import sys
import time
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from generate_data import NBFCS, fetch_snapshot  # noqa: E402

DATA = os.path.join(HERE, 'assets', 'data.js')
PREFIX = 'window.NBFC_DATA = '


def load():
    with open(DATA, encoding='utf-8') as fh:
        text = fh.read()
    head, blob = text.split(PREFIX, 1)
    return head, json.loads(blob.rstrip().rstrip(';'))


def save(head, payload):
    tmp = DATA + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh:
        fh.write(head)
        fh.write(PREFIX)
        json.dump(payload, fh, indent=2, ensure_ascii=False)
        fh.write(';\n')
    os.replace(tmp, DATA)          # atomic: never leave a half-written data.js


def main():
    gap = 75
    if '--gap' in sys.argv:
        gap = int(sys.argv[sys.argv.index('--gap') + 1])
    once = '--once' in sys.argv

    head, payload = load()
    by_sym = {c['symbol']: c for c in payload['companies']}

    for attempt in range(1, 200):
        missing = [s for s in NBFCS.values() if not by_sym[s].get('snapshot')]
        if not missing:
            print(f'All {len(NBFCS)} snapshots present — done.')
            return 0

        stamp = time.strftime('%H:%M:%S')
        print(f'{stamp}  pass {attempt}: {len(missing)} missing', flush=True)

        got_any = False
        for sym in missing:
            snap = fetch_snapshot(sym)
            if snap:
                by_sym[sym]['snapshot'] = snap
                payload['snapshotAt'] = date.today().isoformat()
                save(head, payload)          # persist the moment it lands
                got_any = True
                print(f'    {sym:16s} ₹{snap["price"]:>10,.2f}  {snap["changePct"]:+.2f}%  '
                      f'({len(snap["windows"])} windows)  saved', flush=True)
                time.sleep(2)
            else:
                # Window closed again — stop this pass and wait it out.
                print(f'    {sym:16s} throttled', flush=True)
                break

        if once:
            break
        remaining = [s for s in NBFCS.values() if not by_sym[s].get('snapshot')]
        if not remaining:
            print(f'All {len(NBFCS)} snapshots present — done.')
            return 0
        time.sleep(5 if got_any else gap)

    return 1


if __name__ == '__main__':
    sys.exit(main())
