/* ==========================================================================
   NBFC P/B & Prices.

   Plain script, no modules, no dependencies — it also runs from file://.
   Book values are fetched at runtime from book-values.json, so updating one
   is a file edit and a push: no build step, no code change.
   ========================================================================== */
(function () {
  'use strict';

  var state = {
    book: null,        // book-values.json
    snap: null,        // snapshot.json — dated fallback prices
    live: null,        // /api/quotes response
    sort: 'pb-desc',
    open: {},          // symbol -> detail expanded?
  };

  var SORTS = [
    { key: 'pb-desc', label: 'Richest' },
    { key: 'pb-asc',  label: 'Cheapest' },
    { key: 'day',     label: 'Day move' },
    { key: 'name',    label: 'A–Z' },
  ];

  /* ── formatting ───────────────────────────────────────────────────────── */
  function inr(v, dp) {
    if (v == null || !isFinite(v)) return '—';
    return v.toLocaleString('en-IN', { minimumFractionDigits: dp, maximumFractionDigits: dp });
  }

  function rupee(v, dp) {
    if (v == null || !isFinite(v)) return '—';
    return '₹' + inr(v, dp == null ? 2 : dp);
  }

  function signed(v, dp) {
    if (v == null || !isFinite(v)) return '—';
    return (v >= 0 ? '+' : '−') + Math.abs(v).toFixed(dp == null ? 2 : dp) + '%';
  }

  function tone(v) { return v == null || !isFinite(v) ? 'flat' : v > 0 ? 'up' : v < 0 ? 'down' : 'flat'; }

  function vol(v) {
    if (!v) return '—';
    if (v >= 1e7) return (v / 1e7).toFixed(2) + ' Cr';
    if (v >= 1e5) return (v / 1e5).toFixed(2) + ' L';
    if (v >= 1e3) return (v / 1e3).toFixed(1) + ' K';
    return String(Math.round(v));
  }

  function mcap(v) {
    if (!v || !isFinite(v)) return '—';
    if (v >= 1e12) return '₹' + (v / 1e12).toFixed(2) + ' L.Cr';
    if (v >= 1e9) return '₹' + (v / 1e9).toFixed(1) + ' K.Cr';
    return '₹' + Math.round(v / 1e7).toLocaleString('en-IN') + ' Cr';
  }

  function clockOf(ms) {
    return new Date(ms).toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' });
  }

  function median(nums) {
    var a = nums.filter(function (n) { return n != null && isFinite(n); }).sort(function (x, y) { return x - y; });
    if (!a.length) return null;
    var m = Math.floor(a.length / 2);
    return a.length % 2 ? a[m] : (a[m - 1] + a[m]) / 2;
  }

  /* ── DOM helpers — text only, never innerHTML ─────────────────────────── */
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function fact(label, value) {
    var d = el('div', 'fact');
    d.appendChild(el('dt', null, label));
    d.appendChild(el('dd', null, value));
    return d;
  }

  /* ── data ─────────────────────────────────────────────────────────────── */
  function getJSON(url) {
    return fetch(url, { cache: 'no-cache' }).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    });
  }

  /** Live quote if we have one, else the dated snapshot. */
  function quote(sym) {
    var live = state.live && state.live.companies && state.live.companies[sym];
    if (live && live.price != null) return { q: live, live: true };
    var s = state.snap && state.snap.companies && state.snap.companies[sym];
    if (s && s.price != null) return { q: s, live: false };
    return { q: null, live: false };
  }

  /** One row's worth of derived numbers. */
  function computeRows() {
    return state.book.companies.map(function (c) {
      var got = quote(c.symbol);
      var q = got.q;
      var price = q ? q.price : null;
      var bv = c.bvps;
      return {
        c: c,
        q: q,
        isLive: got.live,
        price: price,
        pb: price != null && bv ? price / bv : null,
        day: q ? q.changePct : null,
        mcap: price != null && c.shares ? price * c.shares : null,
      };
    });
  }

  function sortRows(rows) {
    var s = state.sort;
    var out = rows.slice();
    out.sort(function (a, b) {
      if (s === 'name') return a.c.name.localeCompare(b.c.name);
      var av = s === 'day' ? a.day : a.pb;
      var bv = s === 'day' ? b.day : b.pb;
      // Anything without a number sinks to the bottom regardless of direction.
      if (av == null && bv == null) return a.c.name.localeCompare(b.c.name);
      if (av == null) return 1;
      if (bv == null) return -1;
      return s === 'pb-asc' ? av - bv : bv - av;
    });
    return out;
  }

  /* ── render: hero + tiles ─────────────────────────────────────────────── */
  function renderSummary(rows) {
    var withPb = rows.filter(function (r) { return r.pb != null; });
    var med = median(withPb.map(function (r) { return r.pb; }));

    document.getElementById('hero-pb').textContent = med == null ? '—' : med.toFixed(2);
    document.getElementById('hero-meta').textContent = med == null
      ? 'No book values available'
      : 'across ' + withPb.length + ' of ' + rows.length + ' companies';

    var byPb = withPb.slice().sort(function (a, b) { return a.pb - b.pb; });
    var cheap = byPb[0];
    var rich = byPb[byPb.length - 1];

    document.getElementById('t-cheap-v').textContent = cheap ? cheap.c.short : '—';
    document.getElementById('t-cheap-m').textContent = cheap ? cheap.pb.toFixed(2) + 'x' : '';
    document.getElementById('t-rich-v').textContent = rich ? rich.c.short : '—';
    document.getElementById('t-rich-m').textContent = rich ? rich.pb.toFixed(2) + 'x' : '';

    var medDay = median(rows.map(function (r) { return r.day; }));
    var dv = document.getElementById('t-day-v');
    dv.textContent = signed(medDay);
    dv.className = 't-value ' + tone(medDay);
    var ups = rows.filter(function (r) { return r.day != null && r.day > 0; }).length;
    var downs = rows.filter(function (r) { return r.day != null && r.day < 0; }).length;
    document.getElementById('t-day-m').textContent = (ups || downs) ? ups + ' up · ' + downs + ' down' : '';
  }

  /* ── render: one company ──────────────────────────────────────────────── */
  function renderRow(r, rank) {
    var sym = r.c.symbol;
    var item = el('li', 'item');
    var detailId = 'd-' + sym.replace(/[^A-Z0-9]/gi, '');

    var btn = el('button', 'row');
    btn.type = 'button';
    btn.setAttribute('aria-expanded', String(!!state.open[sym]));
    btn.setAttribute('aria-controls', detailId);

    btn.appendChild(el('span', 'r-rank', String(rank)));

    var mid = el('span', 'r-id');
    mid.appendChild(el('span', 'r-name', r.c.name));
    var book = r.c.bvps
      ? 'BVPS ' + rupee(r.c.bvps, r.c.bvps >= 100 ? 0 : 2) + ' · ' + (r.c.asOf || 'latest')
      : 'book value not set';
    mid.appendChild(el('span', 'r-book', book));
    btn.appendChild(mid);

    var nums = el('span', 'r-nums');
    var pb = el('span', 'r-pb');
    pb.appendChild(document.createTextNode(r.pb == null ? '—' : r.pb.toFixed(2)));
    if (r.pb != null) pb.appendChild(el('span', 'unit', 'x'));
    nums.appendChild(pb);

    var px = el('span', 'r-px');
    if (r.price == null) {
      px.appendChild(document.createTextNode('price unavailable'));
    } else {
      px.appendChild(document.createTextNode(rupee(r.price) + '  '));
      px.appendChild(el('span', 'r-chg ' + tone(r.day), signed(r.day)));
    }
    nums.appendChild(px);
    btn.appendChild(nums);

    btn.appendChild(el('span', 'caret', '▾'));
    item.appendChild(btn);

    var detail = renderDetail(r);
    detail.id = detailId;
    detail.hidden = !state.open[sym];
    item.appendChild(detail);

    btn.addEventListener('click', function () {
      state.open[sym] = !state.open[sym];
      btn.setAttribute('aria-expanded', String(state.open[sym]));
      detail.hidden = !state.open[sym];
    });

    return item;
  }

  function renderDetail(r) {
    var d = el('div', 'detail');
    var q = r.q;

    // The arithmetic, spelled out — so the number on the row is checkable.
    var calc = el('p', 'calc');
    if (r.pb != null) {
      calc.appendChild(document.createTextNode(rupee(r.price) + ' ÷ ' + rupee(r.c.bvps, 2) + ' = '));
      calc.appendChild(el('b', null, r.pb.toFixed(2) + 'x'));
    } else if (!r.c.bvps) {
      calc.textContent = 'Set a book value in book-values.json to get a P/B here.';
    } else {
      calc.textContent = 'No price available for ' + r.c.symbol + '.';
    }
    d.appendChild(calc);

    // 52-week position. Only drawn when the range is real and contains the price.
    if (q && q.weekLow52 != null && q.weekHigh52 != null && q.weekHigh52 > q.weekLow52 && r.price != null) {
      var span = q.weekHigh52 - q.weekLow52;
      var posPct = Math.max(0, Math.min(100, ((r.price - q.weekLow52) / span) * 100));

      var range = el('div', 'range');
      var head = el('div', 'range-head');
      head.appendChild(el('span', null, '52-week range'));
      head.appendChild(el('span', null, Math.round(posPct) + '% of range'));
      range.appendChild(head);

      var bar = el('div', 'range-bar');
      var mark = el('span', 'range-mark');
      mark.style.left = posPct + '%';
      bar.appendChild(mark);
      range.appendChild(bar);

      var foot = el('div', 'range-foot');
      foot.appendChild(el('span', null, rupee(q.weekLow52, 0)));
      foot.appendChild(el('span', null, rupee(q.weekHigh52, 0)));
      range.appendChild(foot);
      d.appendChild(range);
    }

    var facts = el('dl', 'facts');
    if (q && q.low != null && q.high != null) {
      facts.appendChild(fact("Day's range", rupee(q.low, 0) + ' – ' + rupee(q.high, 0)));
    }
    if (q && q.volume) facts.appendChild(fact('Volume', vol(q.volume)));
    if (r.mcap != null) {
      facts.appendChild(fact('Market cap', mcap(r.mcap)));
    }
    if (r.c.bvps && q && q.weekHigh52 != null) {
      facts.appendChild(fact('P/B at 52w high', (q.weekHigh52 / r.c.bvps).toFixed(2) + 'x'));
    }
    if (r.c.bvps && q && q.weekLow52 != null) {
      facts.appendChild(fact('P/B at 52w low', (q.weekLow52 / r.c.bvps).toFixed(2) + 'x'));
    }
    if (r.pb != null) {
      facts.appendChild(fact('Move to 1.0x book', signed((r.c.bvps / r.price - 1) * 100, 1)));
    }

    var notes = [];
    if (r.c.bvps && q && q.weekHigh52 != null) {
      notes.push('52-week P/B applies today’s book value to past prices.');
    }
    if (r.mcap != null && r.c.sharesAsOf) {
      notes.push('Market cap uses the share count as of ' + r.c.sharesAsOf + '.');
    }
    if (!r.isLive && r.price != null) {
      notes.push('Price from the saved snapshot, not live.');
    }
    if (r.c.note) notes.push(r.c.note);
    // One line per caveat — run together they read as a single confused sentence.
    notes.forEach(function (n) { facts.appendChild(el('p', 'note', n)); });

    if (facts.childNodes.length) d.appendChild(facts);
    return d;
  }

  /* ── render: everything ───────────────────────────────────────────────── */
  function render() {
    var rows = computeRows();
    renderSummary(rows);

    var host = document.getElementById('list');
    host.replaceChildren();
    sortRows(rows).forEach(function (r, i) { host.appendChild(renderRow(r, i + 1)); });

    var b = state.book;
    var asOf = b.companies.map(function (c) { return c.asOf; }).filter(Boolean);
    var uniq = asOf.filter(function (v, i) { return asOf.indexOf(v) === i; });
    document.getElementById('foot-book').textContent =
      'Book values: ' + (uniq.length === 1 ? uniq[0] : uniq.join(', ')) +
      (b.updated ? ' · updated ' + b.updated : '');

    setStamp(rows);
  }

  function setStamp(rows) {
    var stamp = document.getElementById('stamp');
    var liveN = rows.filter(function (r) { return r.isLive; }).length;
    var priced = rows.filter(function (r) { return r.price != null; }).length;
    var bits = [];

    if (liveN && state.live) {
      bits.push('Updated ' + clockOf(state.live.fetchedAt));
      bits.push(liveN + ' of ' + rows.length + ' live');
      bits.push(state.live.marketOpen ? 'NSE open' : 'NSE closed');
    } else if (priced) {
      bits.push('Saved prices' + (state.snap && state.snap.generated ? ' from ' + state.snap.generated : ''));
    } else {
      bits.push('No prices available');
    }
    stamp.textContent = bits.join(' · ');
  }

  function setBanner(node) {
    var host = document.getElementById('banner');
    host.replaceChildren();
    if (node) host.appendChild(node);
  }

  function banner(text, isErr, boldPrefix) {
    var n = el('div', 'banner' + (isErr ? ' err' : ''));
    if (boldPrefix) n.appendChild(el('b', null, boldPrefix + ' '));
    n.appendChild(document.createTextNode(text));
    return n;
  }

  /* ── refresh ──────────────────────────────────────────────────────────── */
  function refresh() {
    var btn = document.getElementById('refresh-btn');
    btn.classList.add('spin');

    return getJSON('/api/quotes?t=' + Date.now())
      .then(function (j) {
        if (j.ok) {
          state.live = j;
          if (j.have < j.total) {
            setBanner(banner(
              (j.total - j.have) + ' of ' + j.total + ' companies are still refreshing — the free '
              + 'data plan allows 8 symbols a minute, so they arrive on the next pass.', false));
          } else if (j.warning) {
            setBanner(banner(j.warning, false, 'Feed note:'));
          } else {
            setBanner(null);
          }
        } else if (/TWELVEDATA_API_KEY/.test(j.error || '')) {
          setBanner(banner(
            'No price feed is configured yet. Add TWELVEDATA_API_KEY in Netlify → Site '
            + 'configuration → Environment variables, then redeploy.', true, 'Setup needed.'));
        } else {
          setBanner(banner(String(j.error || 'the price feed did not respond')
            + '. Showing saved prices.', true, 'Live prices unavailable:'));
        }
      })
      .catch(function () {
        setBanner(banner('Could not reach the price feed. Showing saved prices — tap ↻ to retry.',
          true, 'Offline?'));
      })
      .then(function () {
        render();
        btn.classList.remove('spin');
      });
  }

  /* ── chrome ───────────────────────────────────────────────────────────── */
  function buildSorts() {
    var host = document.getElementById('sorts');
    SORTS.forEach(function (s) {
      var b = el('button', null, s.label);
      b.type = 'button';
      b.setAttribute('aria-pressed', String(s.key === state.sort));
      b.addEventListener('click', function () {
        state.sort = s.key;
        [].forEach.call(host.children, function (x) {
          x.setAttribute('aria-pressed', String(x === b));
        });
        try { localStorage.setItem('pb-sort', s.key); } catch (e) { /* private mode */ }
        render();
      });
      host.appendChild(b);
    });
  }

  document.getElementById('theme-btn').addEventListener('click', function () {
    var cur = document.documentElement.getAttribute('data-theme');
    var sysDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    var next = cur === 'dark' ? 'light' : cur === 'light' ? 'dark' : (sysDark ? 'light' : 'dark');
    document.documentElement.setAttribute('data-theme', next);
    try { localStorage.setItem('pb-theme', next); } catch (e) { /* private mode */ }
  });

  document.getElementById('refresh-btn').addEventListener('click', function () { refresh(); });

  // Coming back to a backgrounded tab after a while should not show a stale time.
  var hiddenAt = 0;
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) { hiddenAt = Date.now(); return; }
    if (hiddenAt && Date.now() - hiddenAt > 300000) refresh();
  });

  /* ── boot ─────────────────────────────────────────────────────────────── */
  try {
    var savedTheme = localStorage.getItem('pb-theme');
    if (savedTheme) document.documentElement.setAttribute('data-theme', savedTheme);
    var savedSort = localStorage.getItem('pb-sort');
    if (savedSort && SORTS.some(function (s) { return s.key === savedSort; })) state.sort = savedSort;
  } catch (e) { /* private mode */ }

  buildSorts();

  getJSON('book-values.json')
    .then(function (b) {
      state.book = b;
      // Optional: a dated price snapshot so the page is never blank.
      return getJSON('snapshot.json').catch(function () { return null; });
    })
    .then(function (s) {
      state.snap = s;
      render();          // paint whatever we have immediately
      return refresh();  // then swap in live prices
    })
    .catch(function (err) {
      document.getElementById('stamp').textContent = '';
      setBanner(banner('Could not load book-values.json (' + err.message + '). '
        + 'The dashboard cannot compute P/B without it.', true, 'Data missing.'));
    });
}());
