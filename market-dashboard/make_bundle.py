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

If prices are missing, see the next section — it is almost certainly the feed, not
the deploy. You can confirm the function itself deployed under **Site configuration
→ Functions**, where `market` should be listed.

## Important: live prices need an API key

Yahoo Finance rate-limits cloud/datacenter IP addresses — which is exactly where
this function runs. It answers `HTTP 429` more or less permanently from Netlify,
even though the same request works from a home machine. (That is why the Streamlit
dashboard is unaffected: it runs on your own laptop.)

The fix is a free **Twelve Data** key. It is built to be called from servers and
carries all nine NSE tickers under identical codes.

1. Sign up at twelvedata.com (free tier: 800 API credits/day)
2. Netlify -> **Site configuration -> Environment variables -> Add**
3. Key `TWELVEDATA_API_KEY`, value your key
4. **Deploys -> Trigger deploy**

The function switches over automatically. A full trading day costs roughly 500 of
the 800 free daily credits.

**Without a key** the page falls back to the dated price snapshot baked into
`assets/data.js` and says so at the top. Book value, P/B and P/E still work
normally, because those come from filings rather than the live feed.

## What is live vs baked in

- **Live (with an API key):** prices, day change, volume, market cap and the
  window movement percentages.
- **Baked in:** book value per share and trailing earnings (used for P/B and P/E),
  plus a dated fallback price snapshot. These come from company filings and change
  only when a quarter is reported.

To refresh either, run these in the main repo and re-drag the folder:

```
python market-dashboard/bake_snapshot.py    # refresh the price snapshot
python market-dashboard/generate_data.py    # refresh book value / earnings
python market-dashboard/make_bundle.py      # rebuild this folder
```

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
