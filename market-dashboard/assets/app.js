/* ==========================================================================
   NBFC Market & Valuation — three list views, no charts.
   Plain script (no modules) so it also runs from file:// if opened directly.
   ========================================================================== */
(function () {
  'use strict';

  var D = window.NBFC_DATA;
  var COMPANIES = D.companies;
  var BY_SYM = {};
  COMPANIES.forEach(function (c) { BY_SYM[c.symbol] = c; });

  var PERIODS = ['1W', '1M', '3M', '6M', '1Y', '3Y', '5Y'];
  var state = { period: '1Y', market: null };

  /* ── helpers ──────────────────────────────────────────────────────────── */
  function isDark() {
    var s = document.documentElement.getAttribute('data-theme');
    return s ? s === 'dark' : window.matchMedia('(prefers-color-scheme: dark)').matches;
  }

  function inr(v, dp) {
    if (v == null) return '—';
    return v.toLocaleString('en-IN', { minimumFractionDigits: dp, maximumFractionDigits: dp });
  }

  function fmtVol(v) {
    if (!v) return '—';
    if (v >= 1e7) return (v / 1e7).toFixed(2) + ' Cr';
    if (v >= 1e5) return (v / 1e5).toFixed(2) + ' L';
    if (v >= 1e3) return (v / 1e3).toFixed(1) + ' K';
    return String(Math.round(v));
  }

  function fmtMcap(v) {
    if (!v) return '—';
    if (v >= 1e12) return '₹' + (v / 1e12).toFixed(2) + ' L.Cr';
    if (v >= 1e9) return '₹' + (v / 1e9).toFixed(1) + ' K.Cr';
    return '₹' + Math.round(v / 1e7).toLocaleString('en-IN') + ' Cr';
  }

  function fmtDate(ms) {
    var d = new Date(ms);
    return d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: '2-digit' });
  }

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;      // untrusted labels never via innerHTML
    return n;
  }

  function latest(arr) {
    for (var i = arr.length - 1; i >= 0; i -= 1) if (arr[i] != null) return arr[i];
    return null;
  }

  /**
   * Build one list row.
   *  big  — the headline figure (right, large)
   *  sub  — smaller figure under it
   *  meta — [left, right] footer strings
   *  tone — 'up' | 'down' | 'flat'
   */
  function makeRow(opts) {
    var row = el('div', 'row ' + (opts.tone || ''));

    var name = el('div', 'r-name');
    if (opts.rank != null) name.appendChild(el('span', 'r-rank', String(opts.rank)));
    name.appendChild(document.createTextNode(opts.name));
    row.appendChild(name);

    row.appendChild(el('div', 'r-tkr', opts.ticker));

    var big = el('div', 'r-big ' + (opts.bigTone || ''));
    big.appendChild(document.createTextNode(opts.big));
    if (opts.unit) big.appendChild(el('span', 'unit', opts.unit));
    row.appendChild(big);

    if (opts.sub) row.appendChild(el('div', 'r-sub ' + (opts.subTone || ''), opts.sub));

    if (opts.meta) {
      var meta = el('div', 'r-meta');
      meta.appendChild(el('span', null, opts.meta[0]));
      meta.appendChild(el('span', null, opts.meta[1]));
      row.appendChild(meta);
    }
    return row;
  }

  function tone(pct) { return pct == null ? 'flat' : pct >= 0 ? 'up' : 'down'; }
  function signed(pct, dp) {
    if (pct == null) return '—';
    return (pct >= 0 ? '+' : '−') + Math.abs(pct).toFixed(dp == null ? 2 : dp) + '%';
  }

  /* ── data ─────────────────────────────────────────────────────────────── */
  function loadMarket(force) {
    var url = '/api/market' + (force ? '?t=' + Date.now() : '');
    return fetch(url, { cache: force ? 'reload' : 'default' })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        if (!j.companies) throw new Error(j.error || 'no data');
        state.market = j;
        return j;
      });
  }

  /** Live quote for a symbol, or the baked snapshot if the feed is down. */
  function quote(sym) {
    var live = state.market && state.market.companies && state.market.companies[sym];
    if (live && !live.error) return live;
    var c = BY_SYM[sym];
    return c && c.snapshot ? c.snapshot : null;
  }

  function usingSnapshot() {
    if (!state.market || !state.market.companies) return true;
    var n = 0;
    COMPANIES.forEach(function (c) {
      var q = state.market.companies[c.symbol];
      if (q && !q.error) n += 1;
    });
    return n === 0;
  }

  /* ── 1 · PRICES ───────────────────────────────────────────────────────── */
  function renderPrices() {
    var host = document.getElementById('price-list');
    host.replaceChildren();

    COMPANIES.forEach(function (c) {
      var q = quote(c.symbol);
      if (!q) {
        host.appendChild(makeRow({
          name: c.name, ticker: c.ticker, big: '—', tone: 'flat',
          meta: ['unavailable', ''],
        }));
        return;
      }
      var mcap = q.price && c.shares ? q.price * c.shares : null;
      host.appendChild(makeRow({
        name: c.name,
        ticker: c.ticker,
        big: '₹' + inr(q.price, 2),
        tone: tone(q.changePct),
        sub: signed(q.changePct) + '  ' + (q.changeAbs >= 0 ? '+' : '−') + '₹' + inr(Math.abs(q.changeAbs), 2),
        subTone: tone(q.changePct),
        meta: ['Vol ' + fmtVol(q.volume), 'MCap ' + fmtMcap(mcap)],
      }));
    });
  }

  /* ── 2 · MOVEMENT ─────────────────────────────────────────────────────── */
  function renderMovement() {
    var host = document.getElementById('mv-list');
    host.replaceChildren();

    var rows = [];
    COMPANIES.forEach(function (c) {
      var q = quote(c.symbol);
      var w = q && q.windows ? q.windows[state.period] : null;
      rows.push({ c: c, q: q, w: w, pct: w ? w.pct : null });
    });

    // Ranked best to worst; anything without data sinks to the bottom.
    rows.sort(function (a, b) {
      if (a.pct == null && b.pct == null) return 0;
      if (a.pct == null) return 1;
      if (b.pct == null) return -1;
      return b.pct - a.pct;
    });

    var stamped = null;
    rows.forEach(function (r, i) {
      if (!r.w) {
        host.appendChild(makeRow({
          name: r.c.name, ticker: r.c.ticker, big: '—', tone: 'flat',
          meta: ['no data for this window', ''],
        }));
        return;
      }
      if (stamped == null) stamped = r.w.at;
      host.appendChild(makeRow({
        rank: i + 1,
        name: r.c.name,
        ticker: r.c.ticker,
        big: signed(r.pct, 1),
        bigTone: tone(r.pct),
        tone: tone(r.pct),
        meta: ['₹' + inr(r.w.from, 0) + '  →  ₹' + inr(r.q.price, 0), fmtDate(r.w.at)],
      }));
    });

    var note = document.getElementById('mv-range');
    note.textContent = stamped
      ? fmtDate(stamped) + '  →  today   ·   ' + rows.filter(function (r) { return r.w; }).length + ' of ' + COMPANIES.length + ' companies'
      : '';
  }

  /* ── 3 · PRICE TO BOOK ────────────────────────────────────────────────── */
  function renderPB() {
    var host = document.getElementById('pb-list');
    host.replaceChildren();

    var rows = [];
    COMPANIES.forEach(function (c) {
      var q = quote(c.symbol);
      var bv = latest(c.bvps);
      var ep = latest(c.eps);
      rows.push({
        c: c, q: q, bv: bv, ep: ep,
        pb: q && q.price && bv ? q.price / bv : null,
        pe: q && q.price && ep ? q.price / ep : null,
      });
    });

    // Richest first, cheapest last — the MD reads top-down for "expensive".
    rows.sort(function (a, b) {
      if (a.pb == null && b.pb == null) return 0;
      if (a.pb == null) return 1;
      if (b.pb == null) return -1;
      return b.pb - a.pb;
    });

    rows.forEach(function (r) {
      if (r.pb == null) {
        host.appendChild(makeRow({
          name: r.c.name, ticker: r.c.ticker, big: '—', tone: 'flat',
          meta: [r.bv ? 'price unavailable' : 'book value not reported', ''],
        }));
        return;
      }
      host.appendChild(makeRow({
        name: r.c.name,
        ticker: r.c.ticker,
        big: r.pb.toFixed(2),
        unit: 'x',
        tone: 'flat',
        sub: r.pe ? 'P/E ' + r.pe.toFixed(1) + 'x' : 'P/E —',
        meta: ['₹' + inr(r.q.price, 0) + '  /  BVPS ₹' + inr(r.bv, 0), r.ep ? 'EPS ₹' + inr(r.ep, 1) : ''],
      }));
    });
  }

  /* ── chrome ───────────────────────────────────────────────────────────── */
  function renderAll() {
    renderPrices();
    renderMovement();
    renderPB();
  }

  function setBanner(msg, isErr) {
    var host = document.getElementById('banner');
    host.replaceChildren();
    if (!msg) return;
    host.appendChild(el('div', 'banner' + (isErr ? ' err' : ''), msg));
  }

  function setStamp() {
    var stamp = document.getElementById('stamp');
    var m = state.market;

    if (usingSnapshot()) {
      stamp.textContent = D.snapshotAt
        ? 'Showing saved prices from ' + D.snapshotAt
        : 'Live prices unavailable';
      return;
    }
    var when = new Date(m.fetchedAt);
    var t = when.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });
    var bits = ['Live NSE · ' + t];
    if (m.stale) bits.push('cached');
    if (m.good != null && m.good < m.total) bits.push(m.good + '/' + m.total + ' loaded');
    stamp.textContent = bits.join(' · ');
  }

  var PANELS = ['prices', 'movement', 'pb'];
  function selectTab(key) {
    PANELS.forEach(function (k) {
      document.getElementById('tab-' + k).setAttribute('aria-selected', String(k === key));
      document.getElementById('panel-' + k).hidden = k !== key;
    });
    window.scrollTo(0, 0);
    try { history.replaceState(null, '', '#' + key); } catch (e) { /* file:// */ }
  }
  PANELS.forEach(function (k) {
    document.getElementById('tab-' + k).addEventListener('click', function () { selectTab(k); });
  });

  // period picker
  (function buildPeriods() {
    var host = document.getElementById('mv-periods');
    PERIODS.forEach(function (p) {
      var b = el('button', null, p);
      b.type = 'button';
      b.setAttribute('aria-pressed', String(p === state.period));
      b.addEventListener('click', function () {
        state.period = p;
        [].forEach.call(host.children, function (x) {
          x.setAttribute('aria-pressed', String(x.textContent === p));
        });
        renderMovement();
      });
      host.appendChild(b);
    });
  }());

  document.getElementById('theme-btn').addEventListener('click', function () {
    var cur = document.documentElement.getAttribute('data-theme');
    var next = cur === 'dark' ? 'light' : cur === 'light' ? 'dark' : (isDark() ? 'light' : 'dark');
    document.documentElement.setAttribute('data-theme', next);
    try { localStorage.setItem('nbfc-theme', next); } catch (e) { /* private mode */ }
  });

  function refresh(force) {
    var btn = document.getElementById('refresh-btn');
    btn.classList.add('spin');
    return loadMarket(force)
      .then(function (j) {
        if (usingSnapshot()) {
          setBanner('Live prices are temporarily unavailable (the exchange feed is rate-limiting). '
            + 'Showing saved prices from ' + (D.snapshotAt || 'the last update') + '. Tap ↻ to retry.', true);
        } else if (j.stale) {
          setBanner('Live feed is throttling — showing the most recent successful fetch ('
            + Math.round((j.ageSec || 0) / 60) + ' min old).', false);
        } else if (j.good != null && j.good < j.total) {
          setBanner((j.total - j.good) + ' of ' + j.total + ' companies did not return a price this time.', false);
        } else {
          setBanner(null);
        }
      })
      .catch(function () {
        setBanner('Could not reach the price feed. Showing saved prices from '
          + (D.snapshotAt || 'the last update') + '. Tap ↻ to retry.', true);
      })
      .then(function () {
        renderAll();
        setStamp();
        btn.classList.remove('spin');
      });
  }

  document.getElementById('refresh-btn').addEventListener('click', function () { refresh(true); });

  var hiddenAt = 0;
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) { hiddenAt = Date.now(); return; }
    if (hiddenAt && Date.now() - hiddenAt > 300000) refresh(true);
  });

  /* ── boot ─────────────────────────────────────────────────────────────── */
  try {
    var saved = localStorage.getItem('nbfc-theme');
    if (saved) document.documentElement.setAttribute('data-theme', saved);
  } catch (e) { /* ignore */ }

  document.getElementById('foot-stamp').textContent =
    'Book value & earnings as of ' + D.generated + ' · ' + D.quarters[D.quarters.length - 1];

  selectTab(PANELS.indexOf(location.hash.slice(1)) >= 0 ? location.hash.slice(1) : 'prices');
  renderAll();     // paint the baked snapshot immediately, then swap in live
  refresh(false);
}());
