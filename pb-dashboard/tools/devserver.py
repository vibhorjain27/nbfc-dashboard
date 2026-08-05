#!/usr/bin/env python3
"""
Local preview for the P/B dashboard.

    python pb-dashboard/tools/devserver.py 8000            # real quotes
    python pb-dashboard/tools/devserver.py 8000 --mock     # synthetic quotes

Serves the static files and implements /api/quotes with the same response
contract as the Netlify function, including the rotating-batch behaviour, so
what you see locally is what deploys.

--mock returns deterministic fake numbers so the UI can be worked on without
spending API credits. Production has no such path.
"""

import hashlib
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from http.server import HTTPServer, SimpleHTTPRequestHandler

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENDPOINT = 'https://api.twelvedata.com/quote'

MOCK = '--mock' in sys.argv
BATCH = int(os.environ.get('TWELVEDATA_BATCH', '5'))

with open(os.path.join(ROOT, 'book-values.json'), encoding='utf-8') as fh:
    SYMBOLS = [c['symbol'] for c in json.load(fh)['companies']]

# symbol -> (quote_dict, fetched_at) for the rotating refresh
STORE = {}


def market_open(now=None):
    """NSE: 09:15-15:30 IST, Mon-Fri. IST is UTC+5:30 with no DST."""
    t = time.gmtime((now or time.time()) + 5.5 * 3600)
    if t.tm_wday >= 5:
        return False
    mins = t.tm_hour * 60 + t.tm_min
    return 555 <= mins <= 930


def num(v):
    try:
        f = float(v)
        return f if f == f else None      # filter NaN
    except (TypeError, ValueError):
        return None


def shape(raw):
    price = num(raw.get('close'))
    if price is None:
        return None
    fw = raw.get('fifty_two_week') or {}
    return {
        'price': price,
        'prevClose': num(raw.get('previous_close')),
        'changeAbs': num(raw.get('change')),
        'changePct': num(raw.get('percent_change')),
        'volume': num(raw.get('volume')) or 0,
        'open': num(raw.get('open')),
        'high': num(raw.get('high')),
        'low': num(raw.get('low')),
        'weekHigh52': num(fw.get('high')),
        'weekLow52': num(fw.get('low')),
        'isOpen': raw.get('is_market_open') is True,
        'at': raw.get('datetime'),
    }


def mock_quote(sym):
    """Deterministic per symbol, so screenshots are stable between runs."""
    h = int(hashlib.sha256(sym.encode()).hexdigest()[:8], 16)
    price = round(120 + (h % 90000) / 55.0, 2)
    pct = round(((h >> 8) % 900) / 100.0 - 4.5, 2)
    prev = round(price / (1 + pct / 100), 2)
    return {
        'price': price,
        'prevClose': prev,
        'changeAbs': round(price - prev, 2),
        'changePct': pct,
        'volume': (h % 4_000_000) + 120_000,
        'open': round(prev * 1.002, 2),
        'low': round(min(price, prev) * 0.988, 2),
        'high': round(max(price, prev) * 1.011, 2),
        'weekLow52': round(price * 0.66, 2),
        'weekHigh52': round(price * 1.38, 2),
        'isOpen': market_open(),
        'at': time.strftime('%Y-%m-%d %H:%M:%S'),
    }


def fetch_batch(symbols, key):
    qs = urllib.parse.urlencode({'symbol': ','.join(symbols), 'exchange': 'NSE', 'apikey': key})
    req = urllib.request.Request(f'{ENDPOINT}?{qs}', headers={'Accept': 'application/json'})
    try:
        body = json.load(urllib.request.urlopen(req, timeout=15))
    except Exception as exc:                                  # noqa: BLE001
        return {}, f'{type(exc).__name__}: {exc}'

    if isinstance(body, dict) and body.get('status') == 'error':
        return {}, str(body.get('message') or body.get('code'))[:120]

    entries = [(symbols[0], body)] if len(symbols) == 1 else list(body.items())
    got = {}
    for k, v in entries:
        if not isinstance(v, dict) or v.get('status') == 'error':
            continue
        s = shape(v)
        if s:
            got[str(v.get('symbol') or k).upper()] = s
    return got, None if got else 'no usable quotes in response'


def build_payload():
    if MOCK:
        now = time.time()
        for s in SYMBOLS:
            STORE[s] = (mock_quote(s), now)
        got, err = {s: STORE[s][0] for s in SYMBOLS}, None
    else:
        key = os.environ.get('TWELVEDATA_API_KEY')
        if not key:
            return {
                'ok': False,
                'error': 'TWELVEDATA_API_KEY is not set on this site.',
                'hint': 'export TWELVEDATA_API_KEY=... before starting, or use --mock.',
                'companies': {},
            }
        due = sorted(SYMBOLS, key=lambda s: STORE.get(s, (None, 0))[1])[:max(1, min(len(SYMBOLS), BATCH))]
        got, err = fetch_batch(due, key)
        now = time.time()
        for sym, q in got.items():
            STORE[sym] = (q, now)

    now = time.time()
    companies = {}
    oldest = None
    for s in SYMBOLS:
        if s not in STORE:
            continue
        q, at = STORE[s]
        companies[s] = dict(q, ageSec=round(now - at))
        oldest = at if oldest is None else min(oldest, at)

    if not companies:
        return {'ok': False, 'error': err or 'no quotes available',
                'marketOpen': market_open(), 'companies': {}}

    payload = {
        'ok': True,
        'provider': 'mock' if MOCK else 'twelvedata',
        'fetchedAt': int(now * 1000),
        'marketOpen': market_open(),
        'refreshed': sorted(got.keys()),
        'have': len(companies),
        'total': len(SYMBOLS),
        'oldestSec': None if oldest is None else round(now - oldest),
        'companies': companies,
    }
    if err:
        payload['warning'] = err
    return payload


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def do_GET(self):                                          # noqa: N802
        if self.path.split('?')[0] == '/api/quotes':
            body = json.dumps(build_payload()).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def end_headers(self):
        if self.path.endswith('.json'):
            self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write('  %s\n' % (fmt % args))


def main():
    port = 8000
    for a in sys.argv[1:]:
        if a.isdigit():
            port = int(a)
    mode = 'MOCK quotes' if MOCK else (
        'live Twelve Data' if os.environ.get('TWELVEDATA_API_KEY') else 'NO API KEY — set TWELVEDATA_API_KEY or use --mock')
    print(f'P/B dashboard  →  http://localhost:{port}   ({mode})')
    HTTPServer(('', port), Handler).serve_forever()


if __name__ == '__main__':
    main()
