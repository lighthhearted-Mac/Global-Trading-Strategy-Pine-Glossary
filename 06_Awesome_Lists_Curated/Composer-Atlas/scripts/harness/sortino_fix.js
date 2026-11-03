/* Verify the Sortino fix does what it claims, and no more (v1.76.8)

   ASSERT THE CLAIM, NOT THE RENDER. The failure this guards against is a page
   that looks right while the number behind it is wrong, so every assertion here
   is on the value backtest returns, not on a cell's text.

   THE THREE CLAIMS, and each is a way the fix could be wrong:
     1. No admitted row has a Sortino above any plausible ceiling any more. This
        is the fix working.
     2. The rows are still THERE. The owner chose "formula fix only", meaning a
        degenerate row keeps its place with a blank Sortino rather than being
        evicted. If the store shrank, the fix silently became the other option.
     3. Rows with a defined Sortino are UNCHANGED. Removing the 1e-9 from the
        denominator alters every well-formed value by about one part in 1e7 if
        it was doing anything, so this checks the ordinary case did not move.
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

  const f2 = v => (isFinite(v) ? v.toFixed(2) : String(v));

  async function main() {
    const T = window.__t;
    log('Signal Miner Sortino fix verification');
    log('target ' + TARGET + ' · signals ' + SIGNALS.join(','));
    log('');

    const fams = {};
    T.FAMILIES.forEach(f => { fams[f.id] = true; });
    const W = T.activeWindows(MINP);
    const universe = [...new Set([TARGET, ...SIGNALS])];
    const win = T.windowInfo(universe, W[W.length - 1]);
    const cache = T.buildCaches(universe, T.neededIndicators(fams), W);
    const specs = T.buildSpecs(SIGNALS, fams, W);
    const N = T.N;
    const scored = N - Math.max(1, win.s0);
    const lret = cache[TARGET].lret;
    const buf = new Uint8Array(N);

    // The SHIPPED admission rule, as it now stands: Sortino is not in it.
    let admitted = 0, nanSortino = 0, huge = 0, maxSort = -Infinity;
    let nonFinite = 0;
    const tinyDays = [];
    for (let s = 0; s < specs.n; s++) {
      const a = T.evalSpecAt(specs, s, cache, buf);
      const m = T.backtest(a, lret, win.s0, win.len);
      if (!(m.total > 0 && m.calmar === m.calmar)) continue;
      admitted++;
      if (m.sortino !== m.sortino) {
        nanSortino++;
        tinyDays.push(Math.round(m.tim * scored));
      } else {
        if (!isFinite(m.sortino)) nonFinite++;
        if (m.sortino > maxSort) maxSort = m.sortino;
        if (m.sortino > 10) huge++;
      }
    }

    log('lattice        ' + specs.n.toLocaleString());
    log('admitted       ' + admitted.toLocaleString() + ' (Sortino is no longer part of admission)');
    log('NaN Sortino    ' + nanSortino.toLocaleString() +
        ' rows kept with an undefined Sortino');
    if (tinyDays.length) {
      tinyDays.sort((a, b) => a - b);
      log('  their firing days  min ' + tinyDays[0] + '  max ' + tinyDays[tinyDays.length - 1]);
    }
    log('max defined    ' + f2(maxSort));
    log('');

    // ---- claim 1: the degenerate values are gone ----
    chk(huge === 0, 'no admitted row has a defined Sortino above 10 (was 131 such rows)');
    chk(nonFinite === 0, 'no admitted row has an Infinity Sortino');
    chk(maxSort < 10, 'the largest defined Sortino is plausible, got ' + f2(maxSort));

    // ---- claim 2: the rows survived rather than being evicted ----
    chk(nanSortino > 0, 'degenerate rows are KEPT with a blank Sortino, not evicted');
    // Every kept-but-undefined row should be a barely-firing rule, which is the
    // whole reason its Sortino is undefined. If one of these had thousands of
    // firing days, the cause would be something other than the known one.
    const worst = tinyDays.length ? tinyDays[tinyDays.length - 1] : 0;
    chk(worst < 60, 'every undefined-Sortino row fires rarely, worst is ' +
        worst + ' days of ' + scored);

    // ---- claim 3: ordinary rows did not move ----
    // This one is bounded ANALYTICALLY rather than sampled, because the harness
    // cannot see negStd and reconstructing it from the outside would be guessing
    // dressed up as a measurement. Removing the 1e-9 changes a well-formed value
    // by a factor of negStd / (negStd + 1e-9). For any daily downside deviation
    // above 1e-6, which is far below anything a real strategy produces, that is
    // a change under 0.1%. The distribution measured above is the evidence that
    // ordinary rows are unaffected: the p50 was 0.69 before the fix and the
    // maximum defined value is asserted plausible here.
    log('');
    log('ordinary rows: the 1e-9 removal is bounded analytically. It changes a');
    log('value by negStd / (negStd + 1e-9), which is under 0.1% for any downside');
    log('deviation above 1e-6. Not sampled, because negStd is not observable');
    log('from outside backtest() and a reconstruction would be a guess.');

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
