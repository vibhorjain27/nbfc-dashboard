#!/usr/bin/env python3
"""
Local preview server — serves market-dashboard/ and implements /api/market with
the same contract as netlify/functions/market.mjs, so local behaviour matches
production.

    python market-dashboard/devserver.py 8000
"""

import json
import os
import random
import sys
import time
import urllib.parse
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from generate_data import NBFCS, fetch_snapshot  # noqa: E402

SYMBOLS = list(NBFCS.values())

# Last good payload, mirroring the module-level snapshot in market.mjs.
_snapshot = {'at': 0, 'companies': None, 'good': 0}


def mock_payload():
    """Deterministic synthetic data for UI testing when upstream is throttled.

    Enabled with `--mock`. Never used in production — market.mjs has no such path.
    """
    import hashlib
    now = int(time.time() * 1000)
    companies = {}
    for sym in SYMBOLS:
        seed = int(hashlib.md5(sym.encode()).hexdigest()[:8], 16)
        price = 200 + (seed % 3000)
        chg = ((seed % 900) / 100.0) - 4.5
        prev = round(price / (1 + chg / 100), 2)
        windows = {}
        for k, days in (('1W', 7), ('1M', 30), ('3M', 91), ('6M', 182),
                        ('1Y', 365), ('3Y', 1095), ('5Y', 1825)):
            pct = (((seed >> (days % 17)) % 1600) / 10.0) - 45
            windows[k] = {'from': round(price / (1 + pct / 100), 2),
                          'at': now - days * 86400000, 'pct': round(pct, 2)}
        companies[sym] = {
            'price': float(price), 'prevClose': prev,
            'changeAbs': round(price - prev, 2), 'changePct': round(chg, 2),
            'volume': 10000 + seed % 9000000, 'windows': windows,
        }
    return {'ok': True, 'stale': False, 'fetchedAt': now,
            'good': len(SYMBOLS), 'total': len(SYMBOLS), 'companies': companies}


def build_payload():
    if '--mock' in sys.argv:
        return mock_payload()

    companies = {}
    good = 0
    for i, sym in enumerate(SYMBOLS):
        got = fetch_snapshot(sym)
        if got:
            companies[sym] = got
            good += 1
        else:
            companies[sym] = {'error': 'upstream unavailable'}
        if i < len(SYMBOLS) - 1:
            time.sleep(0.18 + random.random() * 0.16)

    now = int(time.time() * 1000)
    if good:
        _snapshot.update(at=now, companies=companies, good=good)
        return {'ok': True, 'stale': False, 'fetchedAt': now,
                'good': good, 'total': len(SYMBOLS), 'companies': companies}

    if _snapshot['companies']:
        return {'ok': True, 'stale': True, 'fetchedAt': _snapshot['at'],
                'ageSec': round((now - _snapshot['at']) / 1000),
                'good': _snapshot['good'], 'total': len(SYMBOLS),
                'companies': _snapshot['companies']}

    return {'ok': False, 'error': 'upstream unavailable', 'companies': companies}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def log_message(self, fmt, *args):
        if '/api/' in (self.path or ''):
            sys.stderr.write(f'  api  {self.path.split("?")[0]}\n')

    def do_GET(self):
        if urllib.parse.urlparse(self.path).path != '/api/market':
            return super().do_GET()

        body = json.dumps(build_payload()).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print(f'Serving {ROOT} on http://localhost:{port}  (Ctrl-C to stop)')
    ThreadingHTTPServer(('0.0.0.0', port), Handler).serve_forever()
