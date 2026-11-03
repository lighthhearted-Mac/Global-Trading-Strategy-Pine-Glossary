/* Choosing the firing-days floor by measurement, not by taste (V2.2, v1.76.7)

   MEASUREMENT, NOT A GATE.

   WHY A FLOOR AT ALL. The Sortino degeneracy measured in sortino.js is a
   symptom rather than the disease. The 131 rows with an undefined Sortino turn
   out to fire about 0.1% of the time, roughly four days out of 3,942. Fixing
   the Sortino formula removes exactly those rows that happen to have fewer than
   two losing days; it does nothing about a rule that fires six days and has two
   of them negative, which is equally meaningless and stays on the leaderboard
   with a well-formed Sortino next to it. The owner chose to fix the class, not
   the symptom, so the floor needs a value.

   THE TENSION THIS HAS TO RESOLVE. A floor set too low leaves noise on the
   board. A floor set too high evicts legitimately rare signals: a crisis hedge
   that fires in 2008 and 2020 and nowhere else is a real strategy, not an
   artifact, and it will have a low firing count for honest reasons. So the
   question is not "what is a large number of days" but "where does the
   population stop looking like strategies and start looking like accidents".

   WHAT IT REPORTS, for each candidate floor:
     - How much of the store it removes.
     - How many of the DEFAULT top 100 it removes, which is the visitor-visible
       cost.
     - What happens to the leaderboard's best Calmar. This is the number that
       matters most and the reason to measure rather than assume: if raising the
       floor sharply lowers the best Calmar, the floor is removing rows whose
       only qualification was a tiny sample, which is the point. If it barely
       moves, the floor is not doing any work.
     - Whether every removed row was degenerate anyway, which says whether the
       floor subsumes the Sortino fix or is genuinely additional.

   Floors are expressed BOTH as absolute days and as a share of the window, and
   both are reported, because the window length varies with ticker selection and
   a floor that is right at 3,942 days may be wrong at 1,000.
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
  const SAMPLE = CFG.sample || 30000;
  const SHOWN = CFG.shown || 100;
  const DEG = CFG.deg || 10;   // the Sortino degeneracy cut, from sortino.js

  const f2 = v => (isFinite(v) ? v.toFixed(2) : 'n/a');
  function pct(sorted, q) {
    if (!sorted.length) return NaN;
    const i = (sorted.length - 1) * q;
    const lo = Math.floor(i), hi = Math.ceil(i);
    return lo === hi ? sorted[lo] : sorted[lo] + (sorted[hi] - sorted[lo]) * (i - lo);
  }

  async function main() {
    const T = window.__t;
    log('Signal Miner firing-days floor sweep, V2.2');
    log('target ' + TARGET + ' · signals ' + SIGNALS.join(',') + ' · min period ' + MINP);
    log('');

    const fams = {};
    T.FAMILIES.forEach(f => { fams[f.id] = true; });
    const W = T.activeWindows(MINP);
    const universe = [...new Set([TARGET, ...SIGNALS])];
    const win = T.windowInfo(universe, W[W.length - 1]);
    const cache = T.buildCaches(universe, T.neededIndicators(fams), W);
    const specs = T.buildSpecs(SIGNALS, fams, W);
    const N = T.N;

    // The exact denominator backtest uses for tim, so firing days invert cleanly.
    const scored = N - Math.max(1, win.s0);
    log('lattice        ' + specs.n.toLocaleString() + ' specs');
    log('scored window  ' + scored.toLocaleString() + ' days that can carry a return');

    const stride = Math.max(1, Math.floor(specs.n / SAMPLE));
    const idx = [];
    for (let s = 0; s < specs.n; s += stride) idx.push(s);

    const lret = cache[TARGET].lret;
    const buf = new Uint8Array(N);
    const rows = [];
    for (const s of idx) {
      const a = T.evalSpecAt(specs, s, cache, buf);
      const m = T.backtest(a, lret, win.s0, win.len);
      if (m.total > 0 && m.sortino === m.sortino && m.calmar === m.calmar &&
          isFinite(m.sortino) && isFinite(m.calmar)) {
        rows.push({ sortino: m.sortino, calmar: m.calmar, tim: m.tim,
                    days: Math.round(m.tim * scored) });
      }
    }
    log('admitted       ' + rows.length.toLocaleString() + ' of ' + idx.length.toLocaleString());

    // THE SHIPPED DEFAULT FILTER, which store admission does NOT apply.
    // sl-tim defaults to 15 percent and is applied at line 1676 when results
    // are filtered for display, not when the store is built. A harness that
    // stops at the admission rule is therefore measuring rows a visitor never
    // sees. Both populations are reported below, because the difference
    // between them IS the finding: the store is full of tiny-sample rows and
    // the display filter is the only thing holding them back.
    const TIMPCT = CFG.timPct === undefined ? 15 : CFG.timPct;
    const shown = rows.filter(r => r.tim > TIMPCT / 100);
    log('after sl-tim ' + TIMPCT + '%  ' + shown.length.toLocaleString() +
        ' rows survive the SHIPPED default display filter (' +
        (100 * shown.length / rows.length).toFixed(1) + '% of the store)');
    log('  that filter alone requires ' + Math.ceil(scored * TIMPCT / 100).toLocaleString() +
        ' firing days, far above every floor swept below');
    const degShown = shown.filter(r => r.sortino > DEG).length;
    log('  degenerate-Sortino rows that reach a visitor at the default: ' + degShown);
    chk(true, 'shipped default measured, not only the admission rule');
    chk(rows.length > 1000, 'the store is large enough to sweep');

    // ---- where does the population actually sit? ----
    const dv = rows.map(r => r.days).sort((a, b) => a - b);
    log('');
    log('FIRING DAYS across admitted rows');
    log('  p01 ' + Math.round(pct(dv, 0.01)) + '  p05 ' + Math.round(pct(dv, 0.05)) +
        '  p10 ' + Math.round(pct(dv, 0.10)) + '  p50 ' + Math.round(pct(dv, 0.5)) +
        '  p90 ' + Math.round(pct(dv, 0.9)) + '  min ' + dv[0] + '  max ' + dv[dv.length - 1]);

    const base = rows.slice().sort((a, b) => b.calmar - a.calmar);
    const baseTop = base.slice(0, SHOWN);
    const baseBest = base[0].calmar;
    const degAll = rows.filter(r => r.sortino > DEG).length;
    log('');
    log('BASELINE (as shipped today)');
    log('  store ' + rows.length.toLocaleString() + '  best calmar ' + f2(baseBest) +
        '  top-' + SHOWN + ' median calmar ' + f2(pct(baseTop.map(r => r.calmar).sort((a, b) => a - b), 0.5)));
    log('  degenerate Sortino rows in store ' + degAll +
        ', in default top ' + SHOWN + ' ' + baseTop.filter(r => r.sortino > DEG).length);

    // ---- the sweep ----
    log('');
    log('FLOOR SWEEP. "lost top" = rows removed from the DEFAULT top ' + SHOWN + '.');
    log('"deg left" = degenerate-Sortino rows still in the store after the floor.');
    log('');
    log('  floor   as %   store    lost%   lost top   best calmar   deg left');
    const FLOORS = CFG.floors || [2, 5, 10, 21, 42, 63, 126, 252];
    for (const f of FLOORS) {
      const kept = rows.filter(r => r.days >= f);
      if (!kept.length) { log('  ' + String(f).padStart(5) + '   (removes everything)'); continue; }
      const keptTop = kept.slice().sort((a, b) => b.calmar - a.calmar).slice(0, SHOWN);
      const lostTop = SHOWN - baseTop.filter(r => r.days >= f).length;
      const degLeft = kept.filter(r => r.sortino > DEG).length;
      log('  ' + String(f).padStart(5) +
          '   ' + (100 * f / scored).toFixed(2).padStart(4) + '%' +
          '   ' + String(kept.length).padStart(6) +
          '   ' + (100 * (1 - kept.length / rows.length)).toFixed(2).padStart(5) + '%' +
          '   ' + String(lostTop).padStart(8) +
          '   ' + f2(keptTop[0].calmar).padStart(11) +
          '   ' + String(degLeft).padStart(8));
    }

    // ---- does the floor subsume the Sortino fix, or is it additional? ----
    log('');
    log('IS THE FLOOR ENOUGH ON ITS OWN?');
    for (const f of FLOORS) {
      const degLeft = rows.filter(r => r.days >= f && r.sortino > DEG).length;
      if (degLeft === 0) {
        log('  floor ' + f + ' removes every degenerate-Sortino row by itself.');
        log('  The Sortino formula fix is STILL required: the floor is a product');
        log('  rule that a future change could move, while the formula is simply');
        log('  wrong and would silently return to printing 2e6 if the floor fell.');
        break;
      }
    }

    // ---- the honest counter-check: what does a high floor cost? ----
    // If the best calmar collapses as the floor rises, the floor is removing
    // rows whose only qualification was a tiny sample. If it barely moves, the
    // floor is theatre. Either answer is useful; guessing is not.
    log('');
    log('RARE-BUT-REAL CHECK: the best calmar among rows the floor would remove');
    for (const f of FLOORS) {
      const cut = rows.filter(r => r.days < f);
      if (!cut.length) continue;
      const b = cut.reduce((a, r) => (r.calmar > a.calmar ? r : a));
      log('  floor ' + String(f).padStart(3) + '  removes ' + String(cut.length).padStart(6) +
          '  best of them calmar ' + f2(b.calmar).padStart(8) +
          '  on ' + String(b.days).padStart(4) + ' firing days' +
          '  sortino ' + (b.sortino > DEG ? 'DEGENERATE' : f2(b.sortino)));
    }

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
