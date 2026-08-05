#!/usr/bin/env python3
"""
Refresh snapshot.json — the dated fallback prices the dashboard shows when the
live feed is unreachable.

    TWELVEDATA_API_KEY=... python pb-dashboard/tools/refresh_snapshot.py
    python pb-dashboard/tools/refresh_snapshot.py --yahoo     # from a home IP only

Twelve Data's free tier allows 8 API credits a minute and one symbol costs one,
so nine symbols cannot go out at once: this fetches in batches of 5 and waits out
the minute in between. One run costs 9 credits and takes about a minute.

--yahoo skips Twelve Data entirely. Yahoo rate-limits datacenter IPs and answers
429 more or less permanently from a cloud host, so use it only from your own
machine.
"""

import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE = os.path.join(ROOT, 'book-values.json')
OUT = os.path.join(ROOT, 'snapshot.json')

UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/124.0 Safari/537.36')


def num(v):
    try:
        f = float(v)
        return f if f == f else None
    except (TypeError, ValueError):
        return None


def get_json(url, headers=None, timeout=20):
    req = urllib.request.Request(url, headers=headers or {'Accept': 'application/json'})
    return json.load(urllib.request.urlopen(req, timeout=timeout))


# ── Twelve Data ───────────────────────────────────────────────────────────────
def fetch_twelve(symbols, key, batch=5):
    out = {}
    groups = [symbols[i:i + batch] for i in range(0, len(symbols), batch)]
    for n, group in enumerate(groups):
        if n:
            print(f'  waiting 62s for the per-minute credit window…')
            time.sleep(62)
        qs = urllib.parse.urlencode({'symbol': ','.join(group), 'exchange': 'NSE', 'apikey': key})
        try:
            body = get_json(f'https://api.twelvedata.com/quote?{qs}')
        except Exception as exc:                              # noqa: BLE001
            print(f'  batch {n + 1} failed: {type(exc).__name__}: {exc}')
            continue
        if isinstance(body, dict) and body.get('status') == 'error':
            print(f'  batch {n + 1} rejected: {body.get("message")}')
            continue

        entries = [(group[0], body)] if len(group) == 1 else list(body.items())
        for k, v in entries:
            if not isinstance(v, dict) or v.get('status') == 'error':
                print(f'  {k}: {v.get("message") if isinstance(v, dict) else "bad payload"}')
                continue
            price = num(v.get('close'))
            if price is None:
                continue
            fw = v.get('fifty_two_week') or {}
            sym = str(v.get('symbol') or k).upper()
            out[sym] = {
                'price': price,
                'prevClose': num(v.get('previous_close')),
                'changeAbs': num(v.get('change')),
                'changePct': num(v.get('percent_change')),
                'volume': num(v.get('volume')) or 0,
                'open': num(v.get('open')),
                'high': num(v.get('high')),
                'low': num(v.get('low')),
                'weekHigh52': num(fw.get('high')),
                'weekLow52': num(fw.get('low')),
            }
            print(f'  {sym:<12} ₹{price:>10,.2f}  {num(v.get("percent_change")) or 0:+.2f}%')
    return out


# ── Yahoo (home machines only) ────────────────────────────────────────────────
def fetch_yahoo(symbols):
    out = {}
    for sym in symbols:
        url = ('https://query1.finance.yahoo.com/v8/finance/chart/'
               f'{urllib.parse.quote(sym + ".NS")}?range=1y&interval=1d')
        try:
            res = get_json(url, headers={'User-Agent': UA, 'Accept': 'application/json'}, timeout=25)
            r = res['chart']['result'][0]
        except Exception as exc:                              # noqa: BLE001
            print(f'  {sym:<12} failed ({type(exc).__name__})')
            time.sleep(0.4)
            continue

        meta = r.get('meta') or {}
        q = ((r.get('indicators') or {}).get('quote') or [{}])[0]
        closes = [c for c in (q.get('close') or []) if c is not None]
        if len(closes) < 2:
            print(f'  {sym:<12} insufficient history')
            continue

        price = meta.get('regularMarketPrice') or closes[-1]
        prev = closes[-2]
        out[sym.upper()] = {
            'price': round(float(price), 2),
            'prevClose': round(float(prev), 2),
            'changeAbs': round(float(price) - float(prev), 2),
            'changePct': round((float(price) - float(prev)) / float(prev) * 100, 2),
            'volume': meta.get('regularMarketVolume') or 0,
            'open': None,
            'high': None,
            'low': None,
            'weekHigh52': meta.get('fiftyTwoWeekHigh'),
            'weekLow52': meta.get('fiftyTwoWeekLow'),
        }
        print(f'  {sym:<12} ₹{float(price):>10,.2f}')
        time.sleep(0.4)                                       # bursts trip the limiter
    return out


def main():
    with open(STORE, encoding='utf-8') as fh:
        symbols = [c['symbol'] for c in json.load(fh)['companies']]

    use_yahoo = '--yahoo' in sys.argv
    key = os.environ.get('TWELVEDATA_API_KEY')

    if use_yahoo:
        print(f'Fetching {len(symbols)} symbols from Yahoo…')
        got = fetch_yahoo(symbols)
    elif key:
        print(f'Fetching {len(symbols)} symbols from Twelve Data…')
        got = fetch_twelve(symbols, key)
    else:
        print('error: set TWELVEDATA_API_KEY, or pass --yahoo to use Yahoo from a home IP.',
              file=sys.stderr)
        return 1

    if not got:
        print('\nNothing fetched — leaving snapshot.json untouched.', file=sys.stderr)
        return 1

    # Keep any symbol that failed this run rather than blanking it.
    try:
        with open(OUT, encoding='utf-8') as fh:
            prev = json.load(fh)
    except Exception:                                          # noqa: BLE001
        prev = {}

    companies = dict(prev.get('companies') or {})
    companies.update(got)

    with open(OUT, 'w', encoding='utf-8') as fh:
        json.dump({
            '_readme': prev.get('_readme') or
                       'Dated fallback prices, so the dashboard never renders an empty page.',
            'generated': date.today().isoformat(),
            'companies': companies,
        }, fh, indent=2, ensure_ascii=False)
        fh.write('\n')

    print(f'\n{len(got)}/{len(symbols)} refreshed → {OUT}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
