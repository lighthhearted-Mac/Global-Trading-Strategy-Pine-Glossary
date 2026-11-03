/* Empirical null for the Signal Miner search (V2.2 item C, the N-adjustment).

   MEASUREMENT, NOT A GATE. This exists to answer a question the tool cannot
   currently answer about itself: the Miner searches millions of candidates and
   reports the single best number it found, which is the maximum of a very large
   sample and optimistic by construction. How optimistic?

   THE NULL, AND WHY IT IS BUILT THIS WAY.
   The target's log-return series is rotated circularly inside the run's scored
   window, and the same search is run against the rotated target. Rotation is
   chosen over drawing random signals for three reasons that each matter:

     1. It preserves the TARGET exactly: its return distribution, its volatility
        clustering, and its drawdown structure all survive, because it is the
        same series read from a different starting point. A synthetic target
        would have to model all three and would be wrong about at least one.
     2. It preserves every SIGNAL exactly, including its firing rate and its run
        lengths. A random boolean array with matched time-in-market would not:
        real signals fire in blocks, and block structure is most of what drives
        max drawdown, which is the denominator of Calmar.
     3. It preserves the DEPENDENCE BETWEEN CANDIDATES, because it is the same
        lattice of specs being searched. This is the one that decides the whole
        design. docs/PRD.md Section 14 item C warns that closed-form
        multiple-testing adjustments "assume independence that a dense lattice
        badly violates". Searching the real lattice against a scrambled target
        makes no independence assumption at all: whatever correlation the
        candidates have with each other, they still have it here.

   The only thing rotation destroys is the ALIGNMENT between signal and target,
   which is precisely the relationship being tested. That is what a null is.

   THE ONE ARTIFACT, STATED RATHER THAN HIDDEN. A circular rotation splices the
   end of the window onto its start, creating one artificial day-to-day join per
   rotation. Over a window of several thousand days that is one joined day out
   of thousands, and it is the standard cost of a rotation test. It is not
   swept under the rug: the harness reports the window length so the ratio is
   visible.

   WHY ROTATION IS BOUNDED INSIDE THE WINDOW. `lret` carries NaN before a
   ticker's listing date, and `backtest` maps NaN to a zero return. Rotating the
   whole axis would drag those NaNs into the scored window and quietly convert
   them to flat days, biasing the null DOWNWARD, which is the dangerous
   direction: a suppressed null makes a real row look better than it is. So only
   [s0, N) is rotated, which is exactly the span `backtest` reads.

   WHAT IT REPORTS.
     - The best-of-k curve for the real target and for the null, at several k,
       so the growth of the maximum with search size is measured rather than
       assumed.
     - The real search's best against the distribution of null bests, as a
       percentile. This is the honest headline: if the real best sits at the
       50th percentile of what the same search finds on scrambled data, the
       search found nothing.
     - The same for the median row, to show the effect is about the MAXIMUM and
       not a level shift across the board.
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
  const SAMPLE = CFG.sample || 20000;     // specs drawn from the lattice
  const ROTATIONS = CFG.rotations || 30;  // null draws
  const METRIC = CFG.metric || 'calmar';
  // The shipped sl-tim default, as a fraction. This is a DISPLAY filter, not an
  // admission rule, so it has to be applied here explicitly or the harness
  // measures rows the page would never show.
  const TIMF = (CFG.timPct === undefined ? 15 : CFG.timPct) / 100;

  function pct(sorted, q) {
    if (!sorted.length) return NaN;
    const i = (sorted.length - 1) * q;
    const lo = Math.floor(i), hi = Math.ceil(i);
    return lo === hi ? sorted[lo] : sorted[lo] + (sorted[hi] - sorted[lo]) * (i - lo);
  }
  const f2 = v => (isFinite(v) ? v.toFixed(2) : 'n/a');

  async function main() {
    const T = window.__t;
    log('Signal Miner empirical null, V2.2 item C');
    log('target ' + TARGET + ' · signals ' + SIGNALS.join(',') +
        ' · min period ' + MINP + ' · metric ' + METRIC +
        ' · sl-tim ' + (TIMF * 100).toFixed(1) + '% (shipped display filter)');
    log('');

    // ---- set the run up exactly as the page would ----
    const fams = {};
    T.FAMILIES.forEach(f => { fams[f.id] = true; });
    const W = T.activeWindows(MINP);
    const universe = [...new Set([TARGET, ...SIGNALS])];
    const win = T.windowInfo(universe, W[W.length - 1]);
    const need = T.neededIndicators(fams);
    const cache = T.buildCaches(universe, need, W);
    const specs = T.buildSpecs(SIGNALS, fams, W);
    const N = T.N;

    log('lattice        ' + specs.n.toLocaleString() + ' specs');
    log('scored window  ' + win.len.toLocaleString() + ' days from index ' + win.s0);
    chk(specs.n > 1000, 'the lattice is large enough for a maximum to be interesting');
    chk(win.len > 500, 'the window is long enough to rotate meaningfully');

    // ---- a uniform sample across the whole lattice ----
    // Every k-th spec rather than a random draw: the lattice is ordered by
    // family then ticker then window then level, so a stride samples every
    // family and every window evenly, where a random draw of the same size
    // would leave holes by luck alone.
    const stride = Math.max(1, Math.floor(specs.n / SAMPLE));
    const idx = [];
    for (let s = 0; s < specs.n; s += stride) idx.push(s);

    // Then SHUFFLE the sample, which is not cosmetic. The stride gives a sample
    // that is uniform over the lattice, but the lattice is ordered by family,
    // then ticker, then window, then level, so the sample's PREFIX is not
    // uniform: its first hundred entries are all one family. best-of-k reads a
    // prefix, so without this the k=100 row would report the best of one family
    // and call it the best of a hundred candidates. The first run of this
    // harness did exactly that and reported a suspiciously flat 1.00 for both
    // k=100 and k=300. Seeded, so two runs of the same configuration are
    // comparable rather than merely similar.
    let seed = 0x9e3779b9;
    const rnd = () => {
      seed ^= seed << 13; seed ^= seed >>> 17; seed ^= seed << 5;
      return ((seed >>> 0) / 4294967296);
    };
    for (let i = idx.length - 1; i > 0; i--) {
      const j = Math.floor(rnd() * (i + 1));
      const t = idx[i]; idx[i] = idx[j]; idx[j] = t;
    }
    log('sample         ' + idx.length.toLocaleString() +
        ' specs (every ' + stride.toLocaleString() + 'th, then shuffled)');

    // ---- evaluate each sampled spec ONCE, keep the boolean arrays ----
    // Signals do not change under the null; only the target does. Evaluating
    // once and reusing across rotations is what makes this affordable.
    const sigs = [];
    const buf = new Uint8Array(N);
    for (const s of idx) {
      const a = T.evalSpecAt(specs, s, cache, buf);
      sigs.push(Uint8Array.from(a));
    }
    log('evaluated      ' + sigs.length.toLocaleString() + ' signal arrays');

    const lret = cache[TARGET].lret;
    const s0 = Math.max(1, win.s0);
    const span = N - s0;

    // Rotate [s0, N) circularly by `off`, leaving everything before s0 alone.
    function rotated(off) {
      const out = Float64Array.from(lret);
      for (let i = 0; i < span; i++) out[s0 + i] = lret[s0 + ((i + off) % span)];
      return out;
    }

    // Returns values in SAMPLE ORDER, with a non-admitted spec as -Infinity.
    // Sample order is what makes an honest best-of-k possible: the stride
    // sample is uniform over the lattice, so its first k entries are themselves
    // a uniform sample of size k, and a running maximum over them is a real
    // best-of-k rather than an order statistic inferred from a formula.
    function search(l) {
      const vals = new Float64Array(sigs.length);
      for (let i = 0; i < sigs.length; i++) {
        const m = T.backtest(sigs[i], l, win.s0, win.len);
        const v = m[METRIC];
        // Pass 1's own admission rule, so the null is filtered exactly as the
        // real store is. Without this the null would include losing rows the
        // real search never keeps, and its median would stop being comparable.
        // Pass 1 admission AND the shipped display filter. sl-tim defaults to
        // 15 percent and is applied at line 1676 when results are filtered for
        // display, not when the store is built. An earlier version of this
        // harness stopped at the admission rule and so measured a population a
        // visitor never sees: its "real best" came from a spec firing five days
        // out of 3,942, which the default filter discards. Both sides of the
        // comparison always used the same rule, so the percentile was sound,
        // but the absolute figures were store figures. TIMF defaults to the
        // shipped 15 percent; set it to 0 to measure the raw store instead.
        vals[i] = (m.total > 0 && m.sortino === m.sortino && v === v &&
                   m.tim > TIMF) ? v : -Infinity;
      }
      return vals;
    }
    const admitted = v => Array.from(v).filter(x => x > -Infinity).sort((a, b) => a - b);
    // Running maximum at each k in KS, over the sample's first k entries.
    const KS = [100, 300, 1000, 3000, 10000, 30000].filter(k => k <= sigs.length);
    if (KS[KS.length - 1] !== sigs.length) KS.push(sigs.length);
    function bestOfK(v) {
      const out = []; let mx = -Infinity, j = 0;
      for (let i = 0; i < v.length; i++) {
        if (v[i] > mx) mx = v[i];
        if (j < KS.length && i + 1 === KS[j]) { out.push(mx); j++; }
      }
      while (out.length < KS.length) out.push(mx);
      return out;
    }

    // ---- the real search ----
    const realRaw = search(lret);
    const real = admitted(realRaw);
    const realK = bestOfK(realRaw);
    log('');
    log('REAL   kept ' + real.length.toLocaleString() + ' of ' + sigs.length.toLocaleString() +
        ' · best ' + f2(real[real.length - 1]) + ' · p50 ' + f2(pct(real, 0.5)));

    // ---- the null ----
    const nullBest = [], nullMed = [], nullKept = [];
    const nullK = KS.map(() => []);
    for (let r = 0; r < ROTATIONS; r++) {
      // Offsets spread evenly rather than drawn at random, so no two rotations
      // land near each other by luck and the draws cover the whole circle.
      const off = Math.floor(span * (r + 1) / (ROTATIONS + 1));
      const raw = search(rotated(off));
      const v = admitted(raw);
      if (!v.length) continue;
      nullBest.push(v[v.length - 1]);
      nullMed.push(pct(v, 0.5));
      nullKept.push(v.length);
      bestOfK(raw).forEach((b, i) => { if (isFinite(b)) nullK[i].push(b); });
    }
    nullBest.sort((a, b) => a - b);
    nullMed.sort((a, b) => a - b);
    nullKept.sort((a, b) => a - b);
    nullK.forEach(a => a.sort((x, y) => x - y));

    log('NULL   ' + nullBest.length + ' rotations · kept p50 ' +
        Math.round(pct(nullKept, 0.5)).toLocaleString());
    log('  best-of-search   p10 ' + f2(pct(nullBest, 0.1)) + '  p50 ' + f2(pct(nullBest, 0.5)) +
        '  p90 ' + f2(pct(nullBest, 0.9)) + '  max ' + f2(nullBest[nullBest.length - 1]));
    log('  median row       p50 ' + f2(pct(nullMed, 0.5)));

    // ---- the headline ----
    const realBest = real[real.length - 1];
    let beat = 0;
    for (const v of nullBest) if (realBest > v) beat++;
    const percentile = 100 * beat / nullBest.length;
    log('');
    log('HEADLINE');
    log('  real best        ' + f2(realBest));
    log('  null best p50    ' + f2(pct(nullBest, 0.5)));
    log('  edge             ' + f2(realBest - pct(nullBest, 0.5)));
    log('  percentile       ' + percentile.toFixed(0) + ' of ' + nullBest.length + ' rotations');
    log('  median row real  ' + f2(pct(real, 0.5)) + '  vs null ' + f2(pct(nullMed, 0.5)));

    // ---- how the maximum grows with search size ----
    // The whole point of an N-adjustment is that the bar RISES with how many
    // candidates were searched. Measuring the curve says by how much, rather
    // than asserting a closed form that assumes independence the lattice does
    // not have.
    log('');
    log('BEST-OF-k GROWTH (' + METRIC + '), k = specs examined');
    log('        k      real   null p50   null p90      edge');
    KS.forEach((k, i) => {
      const np50 = pct(nullK[i], 0.5), np90 = pct(nullK[i], 0.9);
      log('  ' + String(k).padStart(7) + '   ' + f2(realK[i]).padStart(7) +
          '   ' + f2(np50).padStart(8) + '   ' + f2(np90).padStart(8) +
          '   ' + f2(realK[i] - np50).padStart(7));
    });

    chk(nullBest.length >= Math.min(10, ROTATIONS), 'enough rotations produced a result');
    chk(pct(nullBest, 0.5) > 0, 'the null finds a positive best, which is the whole point');

    log('');
    log(fails ? `*** ${fails} FAILURES ***` : 'DONE');
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
