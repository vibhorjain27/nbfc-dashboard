/* ==========================================================================
   Minimal dependency-free SVG time-series chart.
   Built for touch first: crosshair snaps to the nearest date, one tooltip
   lists every series, vertical page scroll still passes through the plot.
   ========================================================================== */

const NS = 'http://www.w3.org/2000/svg';

function el(tag, attrs) {
  const n = document.createElementNS(NS, tag);
  for (const k in attrs) n.setAttribute(k, attrs[k]);
  return n;
}

/** "Nice" axis ticks — 1/2/5 × 10^n steps covering [lo, hi]. */
function niceTicks(lo, hi, target) {
  if (!isFinite(lo) || !isFinite(hi)) return { ticks: [0, 1], lo: 0, hi: 1 };
  if (lo === hi) { lo -= 1; hi += 1; }
  const raw = (hi - lo) / Math.max(2, target);
  const mag = Math.pow(10, Math.floor(Math.log10(raw)));
  const norm = raw / mag;
  const step = (norm <= 1 ? 1 : norm <= 2 ? 2 : norm <= 5 ? 5 : 10) * mag;
  const start = Math.floor(lo / step) * step;
  const end = Math.ceil(hi / step) * step;
  const ticks = [];
  for (let v = start; v <= end + step * 0.5; v += step) {
    ticks.push(Math.abs(v) < step * 1e-9 ? 0 : v);
  }
  return { ticks, lo: start, hi: end };
}

/** Log-scale ticks at 1/2/5 x 10^n covering [lo, hi] (both > 0). */
function logTicks(lo, hi) {
  const ticks = [];
  const from = Math.floor(Math.log10(lo));
  const to = Math.ceil(Math.log10(hi));
  for (let e = from; e <= to; e += 1) {
    for (const mant of [1, 2, 5]) {
      const v = mant * Math.pow(10, e);
      if (v >= lo * 0.999 && v <= hi * 1.001) ticks.push(v);
    }
  }
  return ticks.length >= 2 ? ticks : [lo, hi];
}

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

function fmtTick(ms, spanDays) {
  const d = new Date(ms);
  if (spanDays <= 14) return `${d.getDate()} ${MONTHS[d.getMonth()]}`;
  // Month + year right through a 5-year span: year-only ticks repeat themselves
  // on any multi-year window (…2025, 2025, 2026, 2026…) and read as a mistake.
  if (spanDays <= 2000) return `${MONTHS[d.getMonth()]} ${String(d.getFullYear()).slice(2)}`;
  return String(d.getFullYear());
}

function fmtFull(ms) {
  const d = new Date(ms);
  return `${d.getDate()} ${MONTHS[d.getMonth()]} ${d.getFullYear()}`;
}

export class LineChart {
  /**
   * @param {HTMLElement} host        wrapper element (position:relative)
   * @param {object}      opts
   * @param {(v:number)=>string} opts.fmt      y-value formatter (axis + tooltip)
   * @param {number}      [opts.refLine]       optional horizontal reference (e.g. P/B = 1)
   * @param {string}      [opts.refLabel]
   * @param {number}      [opts.height]        plot height in px (portrait default)
   */
  constructor(host, opts = {}) {
    this.host = host;
    this.fmt = opts.fmt || ((v) => v.toFixed(2));
    this.refLine = opts.refLine;
    this.refLabel = opts.refLabel || '';
    this.height = opts.height || 250;
    this.yMin = opts.yMin;          // hard floor for the y-domain (e.g. 0 for ratios)
    this.log = !!opts.log;          // log y-axis — for ratios spanning an order of magnitude
    this.series = [];

    this.svg = el('svg', { preserveAspectRatio: 'none' });
    this.host.appendChild(this.svg);

    this.tip = document.createElement('div');
    this.tip.className = 'tip';
    this.host.appendChild(this.tip);

    this._onMove = this._onMove.bind(this);
    this._onLeave = this._onLeave.bind(this);
    host.addEventListener('pointermove', this._onMove);
    host.addEventListener('pointerdown', this._onMove);
    host.addEventListener('pointerleave', this._onLeave);
    host.addEventListener('pointercancel', this._onLeave);

    this._ro = new ResizeObserver(() => this.draw());
    this._ro.observe(host);
  }

  /** @param {{name,short,color,points:{t:number,y:number,meta?:any}[]}[]} series */
  render(series) {
    let list = series || [];
    if (this.log) {
      // log10 is undefined at or below zero — drop those samples rather than
      // silently plotting them at the floor.
      list = list.map((s) => ({ ...s, points: s.points.filter((p) => p.y > 0) }));
    }
    this.series = list.filter((s) => s.points && s.points.length > 1);
    this.draw();
  }

  destroy() {
    this._ro.disconnect();
    this.host.removeEventListener('pointermove', this._onMove);
    this.host.removeEventListener('pointerdown', this._onMove);
    this.host.removeEventListener('pointerleave', this._onLeave);
    this.host.removeEventListener('pointercancel', this._onLeave);
  }

  draw() {
    const svg = this.svg;
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    this.tip.classList.remove('on');

    const W = Math.max(240, this.host.clientWidth - 12);
    const H = this.height;
    svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
    svg.setAttribute('height', H);

    if (!this.series.length) { this._geom = null; return; }

    // Direct-label the line ends only when the chart is legible with them
    // (≤4 series, and only on wide-enough viewports).
    const labelEnds = this.series.length <= 4 && W >= 300;

    const m = { t: 12, r: labelEnds ? 46 : 12, b: 22, l: 42 };
    const pw = W - m.l - m.r;
    const ph = H - m.t - m.b;
    if (pw <= 10 || ph <= 10) return;

    // ── domains ──────────────────────────────────────────────────────────
    let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
    for (const s of this.series) {
      for (const p of s.points) {
        if (p.t < x0) x0 = p.t;
        if (p.t > x1) x1 = p.t;
        if (p.y < y0) y0 = p.y;
        if (p.y > y1) y1 = p.y;
      }
    }
    if (this.refLine !== undefined) {
      y0 = Math.min(y0, this.refLine);
      y1 = Math.max(y1, this.refLine);
    }

    // Domain: linear (optionally floored) or log10 for ratios spanning a decade.
    let yTicks, dLo, dHi, toY;
    if (this.log) {
      const lo = Math.max(y0, 0.05);
      const hi = Math.max(y1, lo * 2);
      dLo = Math.log10(lo) - 0.05;
      dHi = Math.log10(hi) + 0.05;
      yTicks = logTicks(Math.pow(10, dLo), Math.pow(10, dHi));
      toY = (v) => Math.log10(Math.max(v, 1e-6));
    } else {
      const pad = (y1 - y0) * 0.08 || 1;
      let lo = y0 - pad;
      if (this.yMin !== undefined) lo = Math.max(lo, this.yMin);
      const ny = niceTicks(lo, y1 + pad, ph < 200 ? 4 : 5);
      dLo = this.yMin !== undefined ? Math.max(ny.lo, this.yMin) : ny.lo;
      dHi = ny.hi;
      yTicks = ny.ticks.filter((t) => t >= dLo - 1e-9);
      toY = (v) => v;
    }

    const sx = (t) => m.l + ((t - x0) / (x1 - x0 || 1)) * pw;
    const sy = (v) => m.t + ph - ((toY(v) - dLo) / (dHi - dLo || 1)) * ph;
    this._geom = { m, pw, ph, x0, x1, sx, sy, W, H };

    // ── grid + y axis ────────────────────────────────────────────────────
    for (const tv of yTicks) {
      const y = sy(tv);
      if (y < m.t - 1 || y > m.t + ph + 1) continue;
      svg.appendChild(el('line', {
        x1: m.l, x2: m.l + pw, y1: y, y2: y,
        stroke: 'var(--grid)', 'stroke-width': 1, 'shape-rendering': 'crispEdges',
      }));
      const tx = el('text', {
        x: m.l - 6, y: y + 3.5, 'text-anchor': 'end',
        fill: 'var(--ink-muted)', 'font-size': 10, 'font-family': 'var(--mono)',
      });
      tx.textContent = this.fmt(tv);
      svg.appendChild(tx);
    }

    // ── x axis ───────────────────────────────────────────────────────────
    const spanDays = (x1 - x0) / 86400000;
    const nX = pw < 300 ? 3 : pw < 480 ? 4 : 6;
    svg.appendChild(el('line', {
      x1: m.l, x2: m.l + pw, y1: m.t + ph, y2: m.t + ph,
      stroke: 'var(--axis)', 'stroke-width': 1, 'shape-rendering': 'crispEdges',
    }));
    for (let i = 0; i <= nX; i += 1) {
      const t = x0 + ((x1 - x0) * i) / nX;
      const anchor = i === 0 ? 'start' : i === nX ? 'end' : 'middle';
      const tx = el('text', {
        x: sx(t), y: m.t + ph + 14, 'text-anchor': anchor,
        fill: 'var(--ink-muted)', 'font-size': 10, 'font-family': 'var(--mono)',
      });
      tx.textContent = fmtTick(t, spanDays);
      svg.appendChild(tx);
    }

    // ── reference line ───────────────────────────────────────────────────
    if (this.refLine !== undefined) {
      const y = sy(this.refLine);
      if (y > m.t && y < m.t + ph) {
        svg.appendChild(el('line', {
          x1: m.l, x2: m.l + pw, y1: y, y2: y,
          stroke: 'var(--ink-muted)', 'stroke-width': 1.5, 'stroke-dasharray': '4 4',
        }));
        if (this.refLabel) {
          // Right-aligned at the plot edge — the left side is where lines
          // originate, so a label there collides with the data.
          const tx = el('text', {
            x: m.l + pw - 3, y: y - 5, 'text-anchor': 'end',
            fill: 'var(--ink-muted)', 'font-size': 9.5, 'font-family': 'var(--mono)',
          });
          tx.textContent = this.refLabel;
          svg.appendChild(tx);
        }
      }
    }

    // ── series paths ─────────────────────────────────────────────────────
    for (const s of this.series) {
      const d = new Array(s.points.length);
      for (let i = 0; i < s.points.length; i += 1) {
        const p = s.points[i];
        d[i] = `${i ? 'L' : 'M'}${sx(p.t).toFixed(1)} ${sy(p.y).toFixed(1)}`;
      }
      svg.appendChild(el('path', {
        d: d.join(' '), fill: 'none', stroke: s.color,
        'stroke-width': 2, 'stroke-linejoin': 'round', 'stroke-linecap': 'round',
      }));
    }

    // ── direct end labels (collision-nudged) ─────────────────────────────
    if (labelEnds) {
      const items = this.series.map((s) => {
        const last = s.points[s.points.length - 1];
        return { s, y: sy(last.y), v: last.y };
      }).sort((a, b) => a.y - b.y);

      const MIN = 12;
      for (let i = 1; i < items.length; i += 1) {
        if (items[i].y - items[i - 1].y < MIN) items[i].y = items[i - 1].y + MIN;
      }
      const over = items.length ? items[items.length - 1].y - (m.t + ph) : 0;
      if (over > 0) for (const it of items) it.y -= over;

      for (const it of items) {
        const tx = el('text', {
          x: m.l + pw + 5, y: Math.max(m.t + 4, it.y) + 3.5,
          fill: it.s.color, 'font-size': 10, 'font-weight': 700,
          'font-family': 'var(--mono)',
        });
        tx.textContent = this.fmt(it.v);
        svg.appendChild(tx);
      }
    }

    // ── crosshair (hidden until pointer) ─────────────────────────────────
    this.cross = el('line', {
      y1: m.t, y2: m.t + ph, stroke: 'var(--axis)', 'stroke-width': 1,
      opacity: 0, 'shape-rendering': 'crispEdges',
    });
    svg.appendChild(this.cross);
    this.dots = el('g', { opacity: 0 });
    svg.appendChild(this.dots);
  }

  _onMove(ev) {
    const g = this._geom;
    if (!g || !this.series.length) return;

    const rect = this.host.getBoundingClientRect();
    const px = ((ev.clientX - rect.left) / rect.width) * g.W;
    if (px < g.m.l - 8 || px > g.m.l + g.pw + 8) return this._onLeave();

    const t = g.x0 + ((px - g.m.l) / (g.pw || 1)) * (g.x1 - g.x0);

    // nearest sample per series (binary search on sorted timestamps)
    const hits = [];
    let snapT = null, bestD = Infinity;
    for (const s of this.series) {
      const pts = s.points;
      let lo = 0, hi = pts.length - 1;
      while (lo < hi) {
        const mid = (lo + hi) >> 1;
        if (pts[mid].t < t) lo = mid + 1; else hi = mid;
      }
      const c = pts[lo];
      const prev = pts[lo - 1];
      const p = prev && Math.abs(prev.t - t) < Math.abs(c.t - t) ? prev : c;
      hits.push({ s, p });
      const d = Math.abs(p.t - t);
      if (d < bestD) { bestD = d; snapT = p.t; }
    }
    if (snapT === null) return;

    const cx = g.sx(snapT);
    this.cross.setAttribute('x1', cx);
    this.cross.setAttribute('x2', cx);
    this.cross.setAttribute('opacity', 1);

    while (this.dots.firstChild) this.dots.removeChild(this.dots.firstChild);
    for (const h of hits) {
      this.dots.appendChild(el('circle', {
        cx: g.sx(h.p.t), cy: g.sy(h.p.y), r: 3.5,
        fill: h.s.color, stroke: 'var(--surface-1)', 'stroke-width': 2,
      }));
    }
    this.dots.setAttribute('opacity', 1);

    // ── tooltip: value leads, name follows; line key, not a box ──────────
    hits.sort((a, b) => b.p.y - a.p.y);
    const tip = this.tip;
    tip.replaceChildren();

    const dateEl = document.createElement('div');
    dateEl.className = 'tip-date';
    dateEl.textContent = fmtFull(snapT);
    tip.appendChild(dateEl);

    for (const h of hits) {
      const row = document.createElement('div');
      row.className = 'tip-row';

      const key = document.createElement('span');
      key.className = 'tip-key';
      key.style.background = h.s.color;
      row.appendChild(key);

      const nm = document.createElement('span');
      nm.className = 'tip-name';
      nm.textContent = h.s.short || h.s.name;   // untrusted → textContent
      row.appendChild(nm);

      const val = document.createElement('span');
      val.className = 'tip-val';
      val.textContent = h.p.label || this.fmt(h.p.y);
      row.appendChild(val);

      tip.appendChild(row);
    }

    tip.classList.add('on');
    const tw = tip.offsetWidth;
    const hostW = this.host.clientWidth;
    let left = (cx / g.W) * hostW + 14;
    if (left + tw > hostW - 4) left = (cx / g.W) * hostW - tw - 14;
    tip.style.left = `${Math.max(4, left)}px`;
    tip.style.top = '10px';
  }

  _onLeave() {
    this.tip.classList.remove('on');
    if (this.cross) this.cross.setAttribute('opacity', 0);
    if (this.dots) this.dots.setAttribute('opacity', 0);
  }
}
