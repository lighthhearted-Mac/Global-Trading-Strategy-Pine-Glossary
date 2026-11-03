/* How often does the Sortino column show a meaningless number? (V2.2, v1.76.7)

   MEASUREMENT, NOT A GATE.

   THE DEFECT. signal-miner.html computes

       sortino = meanAll / (negStd + 1e-9) * sqrt(252)

   and negStd is the ddof=1 standard deviation of the NEGATIVE returns only. A
   standard deviation with ddof=1 is undefined below two observations, and the
   code says so in its own structure: `nNeg > 1` computes it, `nNeg === 1` sets
   it to exactly 0, and nNeg === 0 leaves it at its initial 0. In both of those
   cases the epsilon is the entire denominator, so the ratio is not a large
   Sortino, it is meanAll multiplied by a billion. An undefined quantity is
   being rendered as a very confident one.

   WHY THIS IS NOT JUST A DISPLAY BUG, WHICH IS THE POINT OF MEASURING IT. The
   Pass 1 admission rule is `m.total > 0 && isFinite(sortino) && isFinite(calmar)`
   (lines 1585 and 1718). A degenerate Sortino is FINITE, so these specs are
   admitted today and compete for leaderboard slots. Making the quantity NaN,
   which is what it mathematically is, would therefore also EVICT them from the
   store. That is a change to which rows exist, not only to how one column
   prints, and it must not be made blind. This harness measures the size of the
   eviction before anything is changed.

   WHAT IT REPORTS.
     - How many admitted specs carry a degenerate Sortino, as a share of the
       store.
     - How many of them reach the DISPLAYED rows under the shipped default sort
       (calmar, descending), which is what a visitor sees without touching
       anything.
     - How many reach the displayed rows when the visitor clicks the Sortino
       column, which is the worst case and the reason this matters: sorting by a
       broken metric ranks the brokenness to the top.
     - Whether any degenerate row would ALSO be lost from a calmar-sorted
       leaderboard if the fix evicts it, which is the actual cost of the fix.

   DETECTING DEGENERACY FROM OUTSIDE backtest(). The harness cannot see nNeg,
   because the hook exposes backtest but not its internals. It does not need to.
   When negStd is exactly 0 the result is meanAll * 1e9 * sqrt(252), roughly
   1.6e10 * meanAll, and meanAll is a daily mean return of order 1e-4. So the
   degenerate cases land near 1e6 and above, while a real annualised Sortino
   lives between roughly 0 and 5 and cannot plausibly exceed a few hundred. The
   harness reports the full distribution rather than asserting a cut, so the
   separation is visible rather than assumed, and it counts against several
   thresholds so the answer does not depend on picking one.
*/
(function () {
  const OUT = [];
  const log = m => OUT.push(m);
  let fails = 0;
  const chk = (ok, msg) => { if (!ok) { fails++; log('FAIL ' + msg); } else log('ok   ' + msg); };

  window.confirm = () => true;

  const CFG = window.__cfg || {};
  const TARGET = CFG.target || 'QQQ';
  const SIGNALS = CFG.signals || ['SPY', 'QQQ', 'TLT'];
  const MINP = CFG.minp || 12;
  const SAMPLE = CFG.sample || 20000;
  const SHOWN = CFG.shown || 100;   // DISPLAY_CAP, what a visitor actually sees

  const f2 = v => (isFinite(v) ? v.toFixed(2) : 'n/a');
  function pct(sorted, q) {
    if (!sorted.length) return NaN;
    const i = (sorted.length - 1) * q;
    const lo = Math.floor(i), hi = Math.ceil(i);
    return lo === hi ? sorted[lo] : sorted[lo] + (sorted[hi] - sorted[lo]) * (i - lo);
  }

  async function main() {
    const T = window.__t;
    log('Signal Miner Sortino degeneracy, V2.2');
    log('target ' + TARGET + ' · signals ' + SIGNALS.join(',') +
        ' · min period ' + MINP + ' · shown ' + SHOWN);
    log('');

    const fams = {};
    T.FAMILIES.forEach(f => { fams[f.id] = true; });
    const W = T.activeWindows(MINP);
    const universe = [...new Set([TARGET, ...SIGNALS])];
    const win = T.windowInfo(universe, W[W.length - 1]);
    const cache = T.buildCaches(universe, T.neededIndicators(fams), W);
    const specs = T.buildSpecs(SIGNALS, fams, W);
    const N = T.N;

    log('lattice        ' + specs.n.toLocaleString() + ' specs');
    log('scored window  ' + win.len.toLocaleString() + ' days from index ' + win.s0);

    const stride = Math.max(1, Math.floor(specs.n / SAMPLE));
    const idx = [];
    for (let s = 0; s < specs.n; s += stride) idx.push(s);
    log('sample         ' + idx.length.toLocaleString() + ' specs (every ' + stride + 'th)');

    // ---- evaluate, applying Pass 1's admission rule exactly as shipped ----
    const lret = cache[TARGET].lret;
    const buf = new Uint8Array(N);
    const rows = [];
    for (const s of idx) {
      const a = T.evalSpecAt(specs, s, cache, buf);
      const m = T.backtest(a, lret, win.s0, win.len);
      // The shipped rule, verbatim in meaning: finite Sortino, finite Calmar,
      // positive total. A degenerate Sortino passes this today.
      if (m.total > 0 && m.sortino === m.sortino && m.calmar === m.calmar &&
          isFinite(m.sortino) && isFinite(m.calmar)) {
        rows.push({ sortino: m.sortino, calmar: m.calmar, tim: m.tim });
      }
    }
    log('admitted       ' + rows.length.toLocaleString() + ' of ' + idx.length.toLocaleString());
    chk(rows.length > 100, 'the store is large enough to rank');

    // ---- the distribution, so the separation is visible not assumed ----
    const sv = rows.map(r => r.sortino).sort((a, b) => a - b);
    log('');
    log('SORTINO DISTRIBUTION across admitted rows');
    log('  p50 ' + f2(pct(sv, 0.5)) + '  p90 ' + f2(pct(sv, 0.9)) +
        '  p99 ' + f2(pct(sv, 0.99)) + '  max ' + sv[sv.length - 1].toExponential(2));

    log('');
    log('COUNT ABOVE THRESHOLD (a real annualised Sortino lives near 0 to 5)');
    for (const t of [10, 100, 1000, 1e5, 1e6]) {
      const c = rows.filter(r => r.sortino > t).length;
      log('  > ' + String(t).padStart(9) + '   ' + String(c).padStart(6) +
          '   ' + (100 * c / rows.length).toFixed(2) + '% of the store');
    }

    // Degenerate = above 1e5. Reported as a choice, with the neighbouring
    // thresholds above so a reader can see it is not a knife edge.
    const DEG = CFG.deg || 1e5;
    const deg = rows.filter(r => r.sortino > DEG);
    log('');
    log('DEGENERATE (> ' + DEG + ') ' + deg.length.toLocaleString() + ' rows, ' +
        (100 * deg.length / rows.length).toFixed(2) + '% of the store');
    if (deg.length) {
      const dt = deg.map(r => r.tim).sort((a, b) => a - b);
      log('  their time in market  p50 ' + (100 * pct(dt, 0.5)).toFixed(2) + '%' +
          '  max ' + (100 * dt[dt.length - 1]).toFixed(2) + '%');
      log('  (a rule with almost no losing days is normally a rule that barely fires)');
    }

    // ---- what a visitor actually sees ----
    const byCal = rows.slice().sort((a, b) => b.calmar - a.calmar).slice(0, SHOWN);
    const bySor = rows.slice().sort((a, b) => b.sortino - a.sortino).slice(0, SHOWN);
    const dCal = byCal.filter(r => r.sortino > DEG).length;
    const dSor = bySor.filter(r => r.sortino > DEG).length;

    log('');
    log('WHAT A VISITOR SEES, top ' + SHOWN + ' displayed rows');
    log('  default sort (calmar desc)   ' + dCal + ' of ' + byCal.length + ' carry a meaningless Sortino');
    log('  after clicking Sortino       ' + dSor + ' of ' + bySor.length + ' carry a meaningless Sortino');

    // ---- the cost of the fix ----
    // If a degenerate Sortino becomes NaN, the admission rule evicts the row.
    // For the calmar-sorted leaderboard, that is a row a visitor would have
    // seen and now will not. That is the number that decides whether the fix
    // is free or has a real cost.
    log('');
    log('COST OF MAKING IT NaN (which evicts the row via the admission rule)');
    log('  rows lost from the store        ' + deg.length.toLocaleString() +
        ' (' + (100 * deg.length / rows.length).toFixed(2) + '%)');
    log('  rows lost from the DEFAULT view ' + dCal + ' of ' + SHOWN);
    const backfill = rows.filter(r => r.sortino <= DEG)
                         .sort((a, b) => b.calmar - a.calmar).slice(0, SHOWN);
    log('  the default view still fills to ' + backfill.length + ' rows after eviction');
    chk(backfill.length === SHOWN || rows.length < SHOWN * 2,
        'evicting degenerate rows still leaves a full leaderboard');

    log('');
    log(fails ? '*** ' + fails + ' FAILURES ***' : 'DONE');
    const d = document.createElement('pre');
    d.id = 'HARNESS'; d.textContent = OUT.join('\n');
    document.body.appendChild(d);
  }

  main().catch(e => {
    const d = document.createElement('pre');
    d.id = 'HARNESS';
    d.textContent = 'HARNESS EXCEPTION: ' + (e && e.message) + '\n' + (e && e.stack) + '\n' + OUT.join('\n');
    document.body.appendChild(d);
  });
})();
