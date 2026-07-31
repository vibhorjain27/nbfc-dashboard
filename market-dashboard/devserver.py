#!/usr/bin/env python3
"""
Local preview server — serves market-dashboard/ and implements /api/yahoo
with the same contract as netlify/functions/yahoo.mjs, so the dashboard can be
exercised end-to-end without the Netlify CLI.

    python market-dashboard/devserver.py 8000
    open http://localhost:8000
"""

import json
import os
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from time import time

ROOT = os.path.dirname(os.path.abspath(__file__))
HOSTS = ['https://query1.finance.yahoo.com', 'https://query2.finance.yahoo.com']
UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')
ALLOWED = {
    'POONAWALLA.NS', 'BAJFINANCE.NS', 'SHRIRAMFIN.NS', 'LTF.NS', 'CHOLAFIN.NS',
    'ABCAPITAL.NS', 'PIRAMALFIN.NS', 'MUTHOOTFIN.NS', 'M&MFIN.NS',
}


def fetch_one(symbol, rng, interval):
    qs = urllib.parse.urlencode({'range': rng, 'interval': interval, 'includePrePost': 'false'})
    path = f'/v8/finance/chart/{urllib.parse.quote(symbol)}?{qs}'
    last = 'unknown'
    for host in HOSTS:
        try:
            req = urllib.request.Request(host + path, headers={'User-Agent': UA, 'Accept': 'application/json'})
            data = json.load(urllib.request.urlopen(req, timeout=12))
            res = (data.get('chart') or {}).get('result') or []
            if not res:
                last = 'empty result'
                continue
            r = res[0]
            meta = r.get('meta') or {}
            stamps = r.get('timestamp') or []
            q = ((r.get('indicators') or {}).get('quote') or [{}])[0]
            closes, vols = q.get('close') or [], q.get('volume') or []

            t, c, v = [], [], []
            for i, ts in enumerate(stamps):
                if i >= len(closes) or closes[i] is None:
                    continue
                t.append(ts)
                c.append(round(float(closes[i]), 4))
                v.append(vols[i] if i < len(vols) and vols[i] is not None else 0)

            return {
                'meta': {
                    'symbol': meta.get('symbol', symbol),
                    'name': meta.get('longName') or meta.get('shortName') or symbol,
                    'currency': meta.get('currency', 'INR'),
                    'price': meta.get('regularMarketPrice'),
                    'prevClose': meta.get('chartPreviousClose') or meta.get('previousClose'),
                    'dayHigh': meta.get('regularMarketDayHigh'),
                    'dayLow': meta.get('regularMarketDayLow'),
                    'volume': meta.get('regularMarketVolume'),
                    'fiftyTwoHigh': meta.get('fiftyTwoWeekHigh'),
                    'fiftyTwoLow': meta.get('fiftyTwoWeekLow'),
                    'marketTime': meta.get('regularMarketTime'),
                    'exchange': meta.get('fullExchangeName', 'NSE'),
                },
                't': t, 'c': c, 'v': v,
            }
        except Exception as exc:
            last = f'{type(exc).__name__}: {exc}'
    return {'error': last}


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def log_message(self, fmt, *args):
        if '/api/' in (self.path or ''):
            sys.stderr.write(f'  api  {self.path.split("?")[0]}  {args[1] if len(args) > 1 else ""}\n')

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != '/api/yahoo':
            return super().do_GET()

        qs = urllib.parse.parse_qs(parsed.query)
        symbols = [s for s in (qs.get('symbols', [''])[0]).split(',') if s in ALLOWED][:12]
        rng = (qs.get('range', ['1mo'])[0])
        interval = (qs.get('interval', ['1d'])[0])

        if not symbols:
            body = json.dumps({'ok': False, 'error': 'no valid symbols'}).encode()
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        with ThreadPoolExecutor(max_workers=min(9, len(symbols))) as ex:
            results = list(ex.map(lambda s: fetch_one(s, rng, interval), symbols))

        payload = {
            'ok': any('error' not in r for r in results),
            'fetchedAt': int(time() * 1000),
            'series': dict(zip(symbols, results)),
        }
        body = json.dumps(payload).encode()
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
