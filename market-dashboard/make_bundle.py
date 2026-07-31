#!/usr/bin/env python3
"""
Build nbfc-market-dashboard.zip — a self-contained folder that can be dragged
straight onto Netlify, with no Git connection and no build step.

The difference from the repo layout is only paths: in the bundle this folder IS
the site root, so netlify.toml uses publish = "." instead of pointing at a
subdirectory. Everything else is copied verbatim.

    python market-dashboard/make_bundle.py
"""

import os
import shutil
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
NAME = 'nbfc-market-dashboard'
STAGE = os.path.join(HERE, '.bundle-stage')
OUT = os.path.join(REPO, f'{NAME}.zip')

FILES = [
    ('index.html', 'index.html'),
    ('assets/app.js', 'assets/app.js'),
    ('assets/data.js', 'assets/data.js'),
    ('assets/styles.css', 'assets/styles.css'),
    ('netlify/functions/market.mjs', 'netlify/functions/market.mjs'),
]

NETLIFY_TOML = '''\
# Standalone deploy of the NBFC Market & Valuation dashboard.
# This folder IS the site root, so publish is "." — do not nest it.

[build]
  publish   = "."
  functions = "netlify/functions"
  command   = ""

[functions]
  node_bundler = "esbuild"

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "SAMEORIGIN"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"

[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=300, must-revalidate"
'''

DEPLOY_MD = '''\
# NBFC Market & Valuation — deploy to Netlify

Self-contained. Nothing to build, no npm install, no dependencies to fetch.

## Deploy

1. Go to **app.netlify.com** → log in.
2. Open the **Sites** tab.
3. Drag **this whole `nbfc-market-dashboard` folder** onto the drop zone that says
   *"Drag and drop your project output folder here"*.
4. Wait ~20 seconds. You get a URL like `https://random-name-123.netlify.app`.
5. Optional: **Site configuration → Change site name** to something like
   `nbfc-market`, giving you `https://nbfc-market.netlify.app`.

Send that URL to the MD. On an iPhone, Safari → Share → **Add to Home Screen**
makes it open full-screen like an app.

> **Drag the folder itself — not its contents, and not a zip of it.**
> Netlify needs to see `netlify.toml` and the `netlify/functions` folder sitting
> next to `index.html`, or live prices will not load.

## Checking it worked

Open the site. The **Prices** tab should list all nine companies with rupee prices.

If you instead see an orange banner saying *"the /api/market function is not
deployed"*, the serverless function did not come across. Re-drag the folder and
confirm `netlify.toml` and `netlify/functions/market.mjs` are inside it. You can
verify from the Netlify dashboard under **Site configuration → Functions** —
`market` should be listed.

## Why there is a function at all

The browser cannot call Yahoo Finance directly — Yahoo sends no CORS headers, so
the request is blocked. `netlify/functions/market.mjs` is a small server-side
pass-through to the same Yahoo endpoint the Python `yfinance` package uses, which
is what the main Streamlit dashboard reads. Both dashboards therefore show the
same numbers.

It only proxies the nine whitelisted NBFC tickers, and replies are cached at the
CDN for 10 minutes, so all visitor traffic collapses into a handful of upstream
fetches per hour and the page loads instantly.

## What is live vs baked in

- **Live on every load:** prices, day change, volume, market cap and the window
  movement percentages.
- **Baked in:** book value per share and trailing earnings (used for P/B and P/E),
  plus a dated fallback price snapshot so the page still shows real numbers if the
  exchange feed is throttling. These come from company filings and only change when
  a quarter is reported.

To refresh the fundamentals later, regenerate `assets/data.js` from the main repo
(`python market-dashboard/generate_data.py`) and rebuild this bundle with
`python market-dashboard/make_bundle.py`.

## Updating later

Drag the folder again onto the **same site** (Deploys tab → drag onto the drop
zone). It replaces the previous deploy and the URL stays the same.

If you would rather it update automatically on every push, connect the GitHub repo
instead: **Add new site → Import an existing project** → pick the repo → leave the
build command empty. The `netlify.toml` at the repo root already points Netlify at
the right folder.
'''


def main():
    root = os.path.join(STAGE, NAME)
    if os.path.exists(STAGE):
        shutil.rmtree(STAGE)

    for src, dst in FILES:
        s = os.path.join(HERE, src)
        d = os.path.join(root, dst)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(s, d)

    with open(os.path.join(root, 'netlify.toml'), 'w', encoding='utf-8') as fh:
        fh.write(NETLIFY_TOML)
    with open(os.path.join(root, 'DEPLOY.md'), 'w', encoding='utf-8') as fh:
        fh.write(DEPLOY_MD)

    if os.path.exists(OUT):
        os.remove(OUT)
    with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
        for folder, _, names in os.walk(root):
            for n in sorted(names):
                full = os.path.join(folder, n)
                z.write(full, os.path.relpath(full, STAGE))

    shutil.rmtree(STAGE)

    with zipfile.ZipFile(OUT) as z:
        entries = [n for n in sorted(z.namelist()) if not n.endswith('/')]
        print(f'Wrote {OUT}  ({os.path.getsize(OUT) / 1024:.0f} KB)')
        for n in entries:
            print(f'  {z.getinfo(n).file_size:>7,}  {n}')


if __name__ == '__main__':
    main()
