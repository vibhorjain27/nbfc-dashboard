/* ==========================================================================
   NBFC Market & Valuation — app logic
   ========================================================================== */

import { LineChart } from './chart.js';

const D = window.NBFC_DATA;
const BY_SYMBOL = Object.fromEntries(D.companies.map((c) => [c.symbol, c]));
const ALL_SYMBOLS = D.companies.map((c) => c.symbol);
const DEFAULT_CMP = ['BAJFINANCE.NS', 'SHRIRAMFIN.NS', 'LTF.NS', 'POONAWALLA.NS'];

const API = '/api/yahoo';

/* Period label -> { range: Yahoo range to fetch, days: client-side slice } */
const P_PRICE = {
  '1W': { range: '5d',  days: 7 },
  '1M': { range: '1mo', days: 31 },
  '3M': { range: '3mo', days: 93 },
  '6M': { range: '6mo', days: 186 },
  '1Y': { range: '1y',  days: 366 },
  '3Y': { range: '5y',  days: 1096 },
  '5Y': { range: '5y',  days: 1827 },
};
const P_VAL = {
  '1Y': { range: '1y', days: 366 },
  '2Y': { range: '2y', days: 731 },
  '3Y': { range: '5y', days: 1096 },
  '5Y': { range: '5y', days: 1827 },
};

const state = {
  histSymbol: 'POONAWALLA.NS',
  histPeriod: '1Y',
  cmpSymbols: new Set(DEFAULT_CMP),
  cmpPeriod: '1Y',
  valSymbols: new Set(DEFAULT_CMP),
  valPeriod: '2Y',
  quotes: {},
};

/* ── theme-aware series colour ──────────────────────────────────────────── */
function isDark() {
  const stamped = document.documentElement.getAttribute('data-theme');
  if (stamped) return stamped === 'dark';
  return matchMedia('(prefers-color-scheme: dark)').matches;
}
/** Series hues are stepped for the surface they sit on — not flipped. */
const hue = (c) => (isDark() ? c.colorDark || c.color : c.color);

/* ── formatting ─────────────────────────────────────────────────────────── */
const inr = (v, dp = 2) =>
  v == null ? '—' : v.toLocaleString('en-IN', { minimumFractionDigits: dp, maximumFractionDigits: dp });

function fmtVol(v) {
  if (!v) return '—';
  if (v >= 1e7) return `${(v / 1e7).toFixed(1)}Cr`;
  if (v >= 1e5) return `${(v / 1e5).toFixed(1)}L`;
  if (v >= 1e3) return `${(v / 1e3).toFixed(1)}K`;
  return String(Math.round(v));
}

function fmtMcap(v) {
  if (!v) return '—';
  if (v >= 1e12) return `₹${(v / 1e12).toFixed(2)}L.Cr`;
  if (v >= 1e9) return `₹${(v / 1e9).toFixed(1)}K.Cr`;
  return `₹${(v / 1e7).toFixed(0)}Cr`;
}

/* ── data fetching (cached per Yahoo range) ─────────────────────────────── */
const cache = new Map();

async function fetchRange(range, force = false) {
  if (!force && cache.has(range)) return cache.get(range);
  const url = `${API}?symbols=${encodeURIComponent(ALL_SYMBOLS.join(','))}&range=${range}&interval=1d`;
  const p = fetch(url, { cache: force ? 'reload' : 'default' })
    .then((r) => { if (!r.ok) throw new Error(`HTTP ${r.status}`); return r.json(); })
    .then((j) => {
      if (!j.ok) throw new Error(j.error || 'upstream error');
      return j;
    })
    .catch((err) => { cache.delete(range); throw err; });
  cache.set(range, p);
  return p;
}

/** Points for a symbol, sliced to the last `days`. */
function pointsFor(payload, symbol, days) {
  const s = payload.series?.[symbol];
  if (!s || s.error || !s.t?.length) return [];
  const cutoff = Date.now() - days * 86400000;
  const out = [];
  for (let i = 0; i < s.t.length; i += 1) {
    const t = s.t[i] * 1000;
    if (t < cutoff) continue;
    out.push({ t, y: s.c[i] });
  }
  return out;
}

/* ── chip / period builders ─────────────────────────────────────────────── */
function buildChips(host, { multi, selected, onChange }) {
  host.replaceChildren();
  for (const c of D.companies) {
    const b = document.createElement('button');
    b.className = 'chip';
    b.type = 'button';
    b.setAttribute('aria-pressed', String(selected.has ? selected.has(c.symbol) : selected === c.symbol));

    const dot = document.createElement('span');
    dot.className = 'dot';
    dot.style.background = hue(c);
    b.appendChild(dot);
    b.appendChild(document.createTextNode(c.short));

    b.addEventListener('click', () => {
      if (multi) {
        if (selected.has(c.symbol)) {
          if (selected.size === 1) return;      // never leave the chart empty
          selected.delete(c.symbol);
        } else selected.add(c.symbol);
      }
      onChange(c.symbol);
    });
    host.appendChild(b);
  }
}

function syncChips(host, selected) {
  [...host.children].forEach((b, i) => {
    const sym = D.companies[i].symbol;
    b.setAttribute('aria-pressed', String(selected.has ? selected.has(sym) : selected === sym));
  });
}

function buildPeriods(host, keys, active, onPick) {
  host.replaceChildren();
  for (const k of keys) {
    const b = document.createElement('button');
    b.className = 'chip';
    b.type = 'button';
    b.textContent = k;
    b.setAttribute('aria-pressed', String(k === active()));
    b.addEventListener('click', () => {
      onPick(k);
      [...host.children].forEach((x) => x.setAttribute('aria-pressed', String(x.textContent === k)));
    });
    host.appendChild(b);
  }
}

/* ── charts ─────────────────────────────────────────────────────────────── */
const histChart = new LineChart(document.getElementById('hist-chart'), {
  fmt: (v) => `₹${v >= 1000 ? Math.round(v).toLocaleString('en-IN') : v.toFixed(0)}`,
  height: 240,
});
const cmpChart = new LineChart(document.getElementById('cmp-chart'), {
  fmt: (v) => v.toFixed(0),
  refLine: 100,
  refLabel: 'start = 100',
  height: 260,
});
const pbChart = new LineChart(document.getElementById('pb-chart'), {
  fmt: (v) => `${v.toFixed(1)}x`,
  refLine: 1,
  refLabel: 'book value 1.0x',
  yMin: 0,
  height: 230,
});
// P/E across these names spans ~12x to ~200x (Poonawalla's recovery-year trailing
// earnings). On a linear axis that outlier flattens every other line into the
// baseline, so this one is log-scaled — standard for ratios spanning a decade.
const peChart = new LineChart(document.getElementById('pe-chart'), {
  fmt: (v) => `${v >= 100 ? v.toFixed(0) : v.toFixed(0)}x`,
  log: true,
  height: 230,
});

function setLoading(id, on) {
  document.getElementById(id).classList.toggle('loading', on);
}

function showEmpty(hostId, msg) {
  const host = document.getElementById(hostId);
  let e = host.querySelector('.empty');
  if (!e) { e = document.createElement('div'); e.className = 'empty'; host.appendChild(e); }
  e.textContent = msg;
  e.hidden = false;
}
function hideEmpty(hostId) {
  const e = document.getElementById(hostId).querySelector('.empty');
  if (e) e.hidden = true;
}

/* ── PRICES ─────────────────────────────────────────────────────────────── */
async function renderTiles(force = false) {
  const host = document.getElementById('tiles');
  const banner = document.getElementById('price-banner');
  const btn = document.getElementById('refresh-btn');
  btn.classList.add('spin');

  let payload;
  try {
    payload = await fetchRange('1mo', force);
  } catch (err) {
    btn.classList.remove('spin');
    host.replaceChildren();
    banner.replaceChildren();
    const b = document.createElement('div');
    b.className = 'banner';
    b.textContent = `Could not reach the price feed (${err.message}). Charts below use the last data loaded.`;
    banner.appendChild(b);
    return;
  }

  banner.replaceChildren();
  state.quotes = payload.series;
  host.replaceChildren();

  let missing = 0;
  for (const c of D.companies) {
    const s = payload.series[c.symbol];
    const meta = s?.meta;
    const closes = s?.c || [];
    const price = meta?.price ?? (closes.length ? closes[closes.length - 1] : null);
    // Previous *session* close — the second-to-last daily bar. NOT meta.prevClose,
    // which Yahoo defines as the close before the requested range began (a month
    // ago here) and would render a 1-month move as if it were today's.
    const prev = closes.length > 1 ? closes[closes.length - 2] : null;
    if (price == null) missing += 1;

    const chg = price != null && prev ? price - prev : null;
    const pct = chg != null && prev ? (chg / prev) * 100 : null;
    const up = pct != null && pct >= 0;

    const tile = document.createElement('div');
    tile.className = `tile ${pct == null ? '' : up ? 'up' : 'down'}`;

    const nm = document.createElement('div');
    nm.className = 'tile-name';
    nm.textContent = c.short;
    tile.appendChild(nm);

    const tk = document.createElement('div');
    tk.className = 'tile-tkr';
    tk.textContent = c.ticker;
    tile.appendChild(tk);

    const pr = document.createElement('div');
    pr.className = 'tile-price';
    pr.textContent = price == null ? '—' : `₹${inr(price)}`;
    tile.appendChild(pr);

    const ch = document.createElement('div');
    ch.className = `tile-chg ${pct == null ? '' : up ? 'up' : 'down'}`;
    ch.textContent = pct == null ? '—' : `${up ? '▲' : '▼'} ${Math.abs(pct).toFixed(2)}%  ${up ? '+' : '−'}₹${inr(Math.abs(chg))}`;
    tile.appendChild(ch);

    const mt = document.createElement('div');
    mt.className = 'tile-meta';
    const v = document.createElement('span');
    v.textContent = `Vol ${fmtVol(meta?.volume)}`;
    const m = document.createElement('span');
    m.textContent = price != null && c.shares ? fmtMcap(price * c.shares) : '—';
    mt.append(v, m);
    tile.appendChild(mt);

    host.appendChild(tile);
  }

  const when = new Date(payload.fetchedAt);
  const stamp = `Live NSE · updated ${when.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' })}` +
    (missing ? ` · ${missing} unavailable` : '');
  document.getElementById('stamp').textContent = stamp;
  document.getElementById('foot-stamp').textContent =
    `Fundamentals as of ${D.generated} · quarters ${D.quarters[0]}–${D.quarters[D.quarters.length - 1]}`;

  btn.classList.remove('spin');
}

async function renderHist() {
  const cfg = P_PRICE[state.histPeriod];
  setLoading('hist-chart', true);
  try {
    const payload = await fetchRange(cfg.range);
    const c = BY_SYMBOL[state.histSymbol];
    const pts = pointsFor(payload, state.histSymbol, cfg.days);
    if (pts.length < 2) { histChart.render([]); showEmpty('hist-chart', 'No price history for this window.'); return; }
    hideEmpty('hist-chart');
    histChart.render([{ name: c.name, short: c.short, color: hue(c), points: pts }]);
  } catch {
    showEmpty('hist-chart', 'Could not load price history.');
  } finally {
    setLoading('hist-chart', false);
  }
}

/* ── COMPARE ────────────────────────────────────────────────────────────── */
async function renderCompare() {
  const cfg = P_PRICE[state.cmpPeriod];
  setLoading('cmp-chart', true);
  const tbody = document.querySelector('#cmp-table tbody');

  try {
    const payload = await fetchRange(cfg.range);
    const series = [];
    const rows = [];

    for (const sym of ALL_SYMBOLS) {
      if (!state.cmpSymbols.has(sym)) continue;
      const c = BY_SYMBOL[sym];
      const pts = pointsFor(payload, sym, cfg.days);
      if (pts.length < 2) continue;

      const base = pts[0].y;
      const last = pts[pts.length - 1].y;
      series.push({
        name: c.name, short: c.short, color: hue(c),
        points: pts.map((p) => ({
          t: p.t,
          y: (p.y / base) * 100,
          label: `${((p.y / base) * 100).toFixed(1)}  (₹${inr(p.y, 0)})`,
        })),
      });
      rows.push({ c, base, last, ret: ((last - base) / base) * 100, idx: (last / base) * 100 });
    }

    if (!series.length) {
      cmpChart.render([]);
      showEmpty('cmp-chart', 'No data for the selected companies in this window.');
    } else {
      hideEmpty('cmp-chart');
      cmpChart.render(series);
    }

    // window label
    if (series.length) {
      const a = new Date(series[0].points[0].t);
      const b = new Date(series[0].points[series[0].points.length - 1].t);
      const f = (d) => d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: '2-digit' });
      document.getElementById('cmp-range').textContent = `${f(a)} → ${f(b)}`;
    }

    // table (sorted best → worst)
    rows.sort((x, y) => y.ret - x.ret);
    tbody.replaceChildren();
    for (const r of rows) {
      const tr = document.createElement('tr');

      const td0 = document.createElement('td');
      td0.className = 'name';
      const sw = document.createElement('span');
      sw.className = 'swatch';
      sw.style.background = hue(r.c);
      td0.append(sw, document.createTextNode(r.c.short));
      tr.appendChild(td0);

      for (const txt of [`₹${inr(r.base, 0)}`, `₹${inr(r.last, 0)}`]) {
        const td = document.createElement('td');
        td.textContent = txt;
        tr.appendChild(td);
      }

      const tdR = document.createElement('td');
      tdR.textContent = `${r.ret >= 0 ? '+' : '−'}${Math.abs(r.ret).toFixed(1)}%`;
      tdR.style.color = r.ret >= 0 ? 'var(--pos)' : 'var(--neg)';
      tdR.style.fontWeight = '700';
      tr.appendChild(tdR);

      const tdI = document.createElement('td');
      tdI.textContent = r.idx.toFixed(1);
      tr.appendChild(tdI);

      tbody.appendChild(tr);
    }
  } catch {
    showEmpty('cmp-chart', 'Could not load comparison data.');
  } finally {
    setLoading('cmp-chart', false);
  }
}

/* ── VALUATION ──────────────────────────────────────────────────────────── */
const Q_END_MS = D.quarterEnds.map((s) => Date.parse(`${s}T00:00:00Z`));

/** Index of the most recent quarter whose end date is on or before `t`. */
function quarterAt(t) {
  let idx = -1;
  for (let i = 0; i < Q_END_MS.length; i += 1) if (Q_END_MS[i] <= t) idx = i; else break;
  return idx;
}

function ratioSeries(payload, sym, days, field) {
  const c = BY_SYMBOL[sym];
  const arr = c[field];
  const pts = [];
  for (const p of pointsFor(payload, sym, days)) {
    const qi = quarterAt(p.t);
    if (qi < 0) continue;
    const denom = arr[qi];
    if (denom == null || denom <= 0) continue;
    pts.push({
      t: p.t,
      y: p.y / denom,
      label: `${(p.y / denom).toFixed(2)}x  (₹${inr(p.y, 0)} / ₹${inr(denom, 0)})`,
    });
  }
  return pts;
}

function latestDefined(arr) {
  for (let i = arr.length - 1; i >= 0; i -= 1) if (arr[i] != null) return arr[i];
  return null;
}

async function renderValuation() {
  const cfg = P_VAL[state.valPeriod];
  setLoading('pb-chart', true);
  setLoading('pe-chart', true);

  try {
    const payload = await fetchRange(cfg.range);
    const pb = [];
    const pe = [];
    const rows = [];

    for (const sym of ALL_SYMBOLS) {
      if (!state.valSymbols.has(sym)) continue;
      const c = BY_SYMBOL[sym];
      const base = { name: c.name, short: c.short, color: hue(c) };

      const pbPts = ratioSeries(payload, sym, cfg.days, 'bvps');
      if (pbPts.length > 1) pb.push({ ...base, points: pbPts });

      const pePts = ratioSeries(payload, sym, cfg.days, 'eps');
      if (pePts.length > 1) pe.push({ ...base, points: pePts });

      const live = payload.series[sym]?.meta?.price ?? null;
      const bv = latestDefined(c.bvps);
      const ep = latestDefined(c.eps);
      rows.push({
        c, price: live, bv, ep,
        pbv: live && bv ? live / bv : null,
        pex: live && ep ? live / ep : null,
      });
    }

    pb.length ? hideEmpty('pb-chart') : showEmpty('pb-chart', 'No book-value data for this selection.');
    pe.length ? hideEmpty('pe-chart') : showEmpty('pe-chart', 'No trailing-earnings data for this selection.');
    pbChart.render(pb);
    peChart.render(pe);

    const tbody = document.querySelector('#val-table tbody');
    rows.sort((a, b) => (b.pbv ?? -1) - (a.pbv ?? -1));
    tbody.replaceChildren();
    for (const r of rows) {
      const tr = document.createElement('tr');

      const td0 = document.createElement('td');
      td0.className = 'name';
      const sw = document.createElement('span');
      sw.className = 'swatch';
      sw.style.background = hue(r.c);
      td0.append(sw, document.createTextNode(r.c.short));
      tr.appendChild(td0);

      const cells = [
        r.price == null ? '—' : `₹${inr(r.price, 0)}`,
        r.bv == null ? '—' : `₹${inr(r.bv, 0)}`,
        r.pbv == null ? '—' : `${r.pbv.toFixed(2)}x`,
        r.ep == null ? '—' : `₹${inr(r.ep, 1)}`,
        r.pex == null ? '—' : `${r.pex.toFixed(1)}x`,
      ];
      cells.forEach((txt, i) => {
        const td = document.createElement('td');
        td.textContent = txt;
        if (i === 2 || i === 4) td.style.fontWeight = '700';
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    }
  } catch {
    showEmpty('pb-chart', 'Could not load valuation data.');
    showEmpty('pe-chart', 'Could not load valuation data.');
  } finally {
    setLoading('pb-chart', false);
    setLoading('pe-chart', false);
  }
}

/* ── tabs / chrome ──────────────────────────────────────────────────────── */
const PANELS = ['prices', 'compare', 'valuation'];
const rendered = new Set();

function selectTab(key) {
  for (const k of PANELS) {
    document.getElementById(`tab-${k}`).setAttribute('aria-selected', String(k === key));
    document.getElementById(`panel-${k}`).hidden = k !== key;
  }
  if (!rendered.has(key)) {
    rendered.add(key);
    if (key === 'compare') renderCompare();
    if (key === 'valuation') renderValuation();
  }
  window.scrollTo({ top: 0, behavior: 'instant' });
  try { history.replaceState(null, '', `#${key}`); } catch { /* file:// */ }
}

for (const k of PANELS) {
  document.getElementById(`tab-${k}`).addEventListener('click', () => selectTab(k));
}

/** Re-tint every colour-bearing element for the current surface. */
function repaintForTheme() {
  for (const id of ['hist-chips', 'cmp-chips', 'val-chips']) {
    const host = document.getElementById(id);
    [...host.children].forEach((b, i) => {
      const dot = b.querySelector('.dot');
      if (dot) dot.style.background = hue(D.companies[i]);
    });
  }
  renderHist();
  if (rendered.has('compare')) renderCompare();
  if (rendered.has('valuation')) renderValuation();
}

document.getElementById('theme-btn').addEventListener('click', () => {
  const cur = document.documentElement.getAttribute('data-theme');
  const next = cur === 'dark' ? 'light' : cur === 'light' ? 'dark'
    : (matchMedia('(prefers-color-scheme: dark)').matches ? 'light' : 'dark');
  document.documentElement.setAttribute('data-theme', next);
  try { localStorage.setItem('nbfc-theme', next); } catch { /* private mode */ }
  repaintForTheme();
});

// Follow the OS switching itself, unless the viewer has stamped a preference.
matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
  if (!document.documentElement.getAttribute('data-theme')) repaintForTheme();
});

document.getElementById('refresh-btn').addEventListener('click', async () => {
  cache.clear();
  rendered.clear();
  rendered.add(PANELS.find((k) => !document.getElementById(`panel-${k}`).hidden));
  await renderTiles(true);
  await renderHist();
  const open = PANELS.find((k) => !document.getElementById(`panel-${k}`).hidden);
  if (open === 'compare') renderCompare();
  if (open === 'valuation') renderValuation();
});

// Refresh quotes when the phone comes back to the app after 5+ minutes.
let hiddenAt = 0;
document.addEventListener('visibilitychange', () => {
  if (document.hidden) { hiddenAt = Date.now(); return; }
  if (hiddenAt && Date.now() - hiddenAt > 300000) {
    cache.delete('1mo');
    renderTiles(true);
  }
});

/* ── boot ───────────────────────────────────────────────────────────────── */
try {
  const saved = localStorage.getItem('nbfc-theme');
  if (saved) document.documentElement.setAttribute('data-theme', saved);
} catch { /* ignore */ }

buildChips(document.getElementById('hist-chips'), {
  multi: false,
  selected: state.histSymbol,
  onChange: (sym) => {
    state.histSymbol = sym;
    syncChips(document.getElementById('hist-chips'), { has: (s) => s === sym });
    renderHist();
  },
});
buildPeriods(document.getElementById('hist-periods'), Object.keys(P_PRICE), () => state.histPeriod, (k) => {
  state.histPeriod = k; renderHist();
});

buildChips(document.getElementById('cmp-chips'), {
  multi: true,
  selected: state.cmpSymbols,
  onChange: () => { syncChips(document.getElementById('cmp-chips'), state.cmpSymbols); renderCompare(); },
});
buildPeriods(document.getElementById('cmp-periods'), Object.keys(P_PRICE), () => state.cmpPeriod, (k) => {
  state.cmpPeriod = k; renderCompare();
});
document.getElementById('cmp-reset').addEventListener('click', () => {
  state.cmpSymbols = new Set(DEFAULT_CMP);
  syncChips(document.getElementById('cmp-chips'), state.cmpSymbols);
  renderCompare();
});

buildChips(document.getElementById('val-chips'), {
  multi: true,
  selected: state.valSymbols,
  onChange: () => { syncChips(document.getElementById('val-chips'), state.valSymbols); renderValuation(); },
});
buildPeriods(document.getElementById('val-periods'), Object.keys(P_VAL), () => state.valPeriod, (k) => {
  state.valPeriod = k; renderValuation();
});

const startTab = PANELS.includes(location.hash.slice(1)) ? location.hash.slice(1) : 'prices';
selectTab(startTab);
rendered.add('prices');

renderTiles().then(renderHist);
