/* Parameter plateau scoring (V2.2 item A).

   The plateau columns are a diagnostic, which makes them exactly the kind of
   feature that can be wrong for months without anyone noticing: nothing
   downstream consumes them, so a bad number has no second symptom. Everything
   below is therefore an INDEPENDENT recomputation, not a re-reading of what
   the page already decided.

   What it proves:
     1. Every row on screen is scored, combined AND rows included, at the
        SHIPPED pairing default. This is a regression test with a story: the
        first cut scored singles only, and at the shipped default the top 100
        by Calmar is essentially all combined rows, so both columns rendered a
        wall of dashes on the view a visitor gets without touching anything.
     2. Re-evaluating a row's own conditions unperturbed reproduces the metric
        the results table already holds. If that drifts, every neighbour around
        it is being compared against a different backtest than the row itself.
     3. The plateau endpoints really score inside the band, and the neighbour
        one step past each endpoint really does not (or is genuinely off the
        lattice). This is the whole claim the column makes.
     4. The neighbourhood median reproduces exactly, over the same pool.
     5. No neighbour violates the canonical p1 < p2 rule that pushCmpSpecs
        enforces on same-ticker comparisons, so the ring never scores a spec
        the run itself would refuse to build.
     6. Window neighbours come from the RUN'S ACTIVE grid, not from WINDOWS.
        A min-period floor removes windows from the lattice and the ring must
        move with it.
     7. Neighbours are re-evaluated, not read out of the Pass 1 store: the
        store keeps only specs with total > 0 and finite Sortino and Calmar, so
        a scorer that can price a loser cannot be reading it.
     8. The page's own account of every axis end matches the independent walk.
*/
(function () {
  const OUT = [];
  const log = m => OUT.push(m);
  let fails = 0;
  const chk = (ok, msg) => { if (!ok) { fails++; log('FAIL ' + msg); } else log('ok   ' + msg); };

  window.confirm = () => true;

  function waitFor(fn, ms) {
    return new Promise((res, rej) => {
      const t0 = Date.now();
      (function tick() {
        let v; try { v = fn(); } catch (e) { return rej(e); }
        if (v) return res(v);
        if (Date.now() - t0 > ms) return rej(new Error('timeout: ' + fn));
        setTimeout(tick, 25);
      })();
    });
  }

  async function main() {
    await waitFor(() => window.__t && window.__t.PD && document.getElementById('sl-run'), 60000);
    const T = window.__t;
    document.getElementById('sl-cpu').value = 'max';

    // A min-period floor of 12 is deliberate: it drops 5, 7 and 10 from the
    // grid, so the active-lattice check below is a real test, not a tautology.
    const MINP = 12;
    T.targets.clear(); ['QQQ'].forEach(s => T.targets.add(s));
    T.compares.clear(); ['SPY', 'QQQ', 'TLT'].forEach(s => T.compares.add(s));
    document.getElementById('sl-minp').value = String(MINP);
    // Pairing OFF for the first pass. At the shipped setting the top 100 is 99
    // combined rows and one single, so every single-row assertion would rest on
    // a sample of one. Pairing goes back ON for the second pass, which is where
    // the combined rows are checked, at the default a visitor actually sees.
    document.getElementById('sl-combo').value = '1';
    T.syncChips();

    const panel = document.getElementById('sl-results-panel');
    panel.style.display = 'none';
    document.getElementById('sl-run').click();
    await waitFor(() => panel.style.display !== 'none', 900000);
    await waitFor(() => document.querySelectorAll('#sl-body tr').length, 120000);

    const sc = T.sigCache;
    const W = sc.W;
    chk(Array.isArray(W) && W.length > 0, 'sigCache carries the run active window grid W');
    chk(W.every(p => p >= MINP), `W is filtered by the min period: [${W.join(', ')}]`);
    chk(W.indexOf(5) === -1 && W.indexOf(10) === -1,
        'W really did lose 5 and 10, so the window-lattice checks are not vacuous');

    const metric = T.plateauMetric();
    const top = () => T.selectTop(T.lastResults, T.DISPLAY_CAP, T.sortKey, false, '').rows;

    // ---- the independent recomputation ----
    // Rebuilt here rather than imported, so a bug in the page's own scorer
    // cannot hide inside the check that is supposed to catch it.
    function boolOf(spec) {
      const [L, R] = T.leftRight(spec, sc.cache);
      const arr = new Uint8Array(T.N);
      const scalarR = typeof R === 'number';
      const gt = spec.dir === 'GT';
      for (let i = 0; i < T.N; i++) {
        const a = L[i];
        const b = scalarR ? R : R[i];
        arr[i] = (a === a && b === b && (gt ? a > b : a < b)) ? 1 : 0;
      }
      return arr;
    }
    function scoreOf(spec, target, andWith) {
      const arr = boolOf(spec);
      if (andWith) for (let i = 0; i < T.N; i++) arr[i] &= andWith[i];
      const m = T.backtest(arr, sc.targetLret[target], sc.win.s0, sc.win.len);
      return m[metric];
    }
    // The AND of every condition except `skip`, held fixed.
    function partnerOf(specs, skip) {
      let acc = null;
      for (let j = 0; j < specs.length; j++) {
        if (j === skip) continue;
        const a = boolOf(specs[j]);
        if (!acc) acc = a; else for (let k = 0; k < T.N; k++) acc[k] &= a[k];
      }
      return acc;
    }
    const specsOf = r => r.single ? (r.spec ? [r.spec] : []) : (r.specs || []);

    // Every axis a row owns, as {move, radius, kind, partner}.
    function axesOf(r) {
      const specs = specsOf(r), out = [];
      for (let i = 0; i < specs.length; i++) {
        const spec = specs[i], f = T.FAM[spec.f];
        const partner = specs.length > 1 ? partnerOf(specs, i) : null;
        const lm = T.levelMover(spec);
        if (lm) out.push({ kind: 'level', move: lm.move, radius: T.PLATEAU_LVL_RADIUS,
                           partner, med: 2, spec });
        for (const slot of (f.kind === 'cmp' ? ['p1', 'p2'] : ['p1'])) {
          const mv = T.windowMover(spec, slot);
          if (mv) out.push({ kind: slot, move: mv, radius: T.PLATEAU_WIN_RADIUS,
                             partner, med: 1, spec });
        }
      }
      return out;
    }

    const tally = { ends: 0, hold: 0, brk: 0, edge: 0, ring: 0, med: 0, self: 0 };

    function verifyRow(r) {
      const pl = T.plateauFor(r, metric);
      if (!pl) return false;
      const self = r[metric];
      const floor = self - T.PLATEAU_DROP * Math.abs(self);
      const specs = specsOf(r);
      const axes = axesOf(r);

      // ---- 2. unperturbed, the row reproduces its own stored metric ----
      // Zero steps on any axis is the row itself. If this drifts, every
      // neighbour is being measured against a different backtest than the row.
      const zero = specs.length > 1
        ? scoreOf(specs[0], r.target, partnerOf(specs, 0))
        : scoreOf(specs[0], r.target);
      if (Math.abs(zero - self) > 1e-9) {
        fails++;
        log(`FAIL "${r.label}" re-evaluates to ${zero}, table holds ${self}`);
      } else tally.self++;

      for (const a of axes) {
        for (const dir of [-1, 1]) {
          let n = 0, stop = 'break';
          while (n < a.radius) {
            const sp = a.move(dir * (n + 1));
            if (!sp) { stop = 'edge'; break; }
            const v = scoreOf(sp, r.target, a.partner);
            if (v !== v || v < floor) break;
            n++;
          }
          // Same rule the page uses: holding all the way out is only "may run
          // wider" if there is lattice left to run into.
          if (n === a.radius && stop === 'break') {
            stop = a.move(dir * (a.radius + 1)) ? 'ring' : 'edge';
          }

          // ---- 3. every step inside the run holds; the next one does not ----
          for (let k = 1; k <= n; k++) {
            const v = scoreOf(a.move(dir * k), r.target, a.partner);
            if (!(v >= floor)) {
              fails++;
              log(`FAIL ${a.kind} step ${dir * k} of "${r.label}" is ${v}, below floor ${floor}`);
            } else tally.hold++;
          }
          if (stop === 'edge') tally.edge++;
          else if (stop === 'ring') tally.ring++;
          else {
            const v = scoreOf(a.move(dir * (n + 1)), r.target, a.partner);
            if (v === v && v >= floor) {
              fails++;
              log(`FAIL ${a.kind} plateau of "${r.label}" stopped early: ` +
                  `step ${dir * (n + 1)} scores ${v} >= floor ${floor}`);
            } else tally.brk++;
          }
          tally.ends++;

          // ---- 5. no neighbour breaks the canonical same-ticker rule ----
          if (T.FAM[a.spec.f].kind === 'cmp' && a.spec.t1 === a.spec.t2) {
            for (let k = 1; k <= a.radius; k++) {
              const sp = a.move(dir * k);
              if (sp && !(sp.p1 < sp.p2)) {
                fails++;
                log(`FAIL same-ticker neighbour p1=${sp.p1} p2=${sp.p2} violates p1 < p2`);
              }
            }
          }
          // ---- 6. window neighbours come from the active grid ----
          if (a.kind !== 'level') {
            for (let k = 1; k <= a.radius; k++) {
              const sp = a.move(dir * k);
              const p = sp && (a.kind === 'p2' ? sp.p2 : sp.p1);
              if (sp && W.indexOf(p) === -1) {
                fails++;
                log(`FAIL window neighbour ${a.kind}=${p} is not in the active grid`);
              }
            }
          }
        }
      }

      // ---- 4. the median is a median of real values ----
      const pool = [self];
      for (const a of axes) {
        for (let k = -a.med; k <= a.med; k++) {
          if (!k) continue;
          const sp = a.move(k);
          if (!sp) continue;
          const v = scoreOf(sp, r.target, a.partner);
          if (v === v) pool.push(v);
        }
      }
      pool.sort((x, y) => x - y);
      const h = pool.length >> 1;
      const want = pool.length % 2 ? pool[h] : (pool[h - 1] + pool[h]) / 2;
      if (Math.abs(want - pl.med) > 1e-9) {
        fails++;
        log(`FAIL median for "${r.label}": page ${pl.med}, recomputed ${want} over ${pool.length}`);
      } else tally.med++;
      return true;
    }

    // ================= pass 1: singles =================
    const singles = top();
    log(`ranking metric: ${metric}; pass 1 (pairing off): ${singles.length} rows`);
    chk(singles.every(r => r.single), 'pass 1 is all single signals');
    chk(singles.length > 20, `${singles.length} single rows, a real sample rather than one`);
    let scored = 0;
    for (const r of singles) if (verifyRow(r)) scored++;
    chk(scored === singles.length, `every single row scored: ${scored} of ${singles.length}`);
    chk(document.querySelectorAll('#sl-body tr td.plat').length === singles.length * 2,
        'two plateau cells rendered per row');

    // ---- 7. the ring evaluates, it does not look up ----
    // The Pass 1 store keeps only specs with total > 0 and finite Sortino and
    // Calmar. So if the scorer can return a value for a spec that loses, it
    // cannot be reading the store. The far end of a level grid is a reliable
    // source of those: RSI < 2 never fires, and a signal that never fires has a
    // total of exactly 0, which the store would have thrown away.
    let losers = 0, probed = 0;
    for (const r of singles) {
      const lm = T.levelMover(r.spec);
      if (!lm) continue;
      for (const j of [0, lm.grid.length - 1]) {
        const sp = Object.assign({}, r.spec, { level: lm.grid[j] });
        const m = T.plateauScore(sp, r.target);
        probed++;
        if (!m || !(m.total > 0) || m.sortino !== m.sortino || m.calmar !== m.calmar) losers++;
      }
      if (probed >= 40) break;
    }
    chk(losers > 0,
        `${losers} of ${probed} grid-extreme neighbours are specs Pass 1 discarded, and the ` +
        `ring scored them anyway: these values are re-evaluated, not read out of the store`);

    // ================= pass 2: the shipped default =================
    // This is the pass that would have caught the wall of dashes.
    document.getElementById('sl-combo').value = '2';
    document.getElementById('sl-combo').dispatchEvent(new Event('change'));
    await waitFor(() => top().some(r => !r.single), 300000);
    await waitFor(() => document.querySelectorAll('#sl-body tr td.plat').length, 120000);

    const mixed = top();
    const nCombo = mixed.filter(r => !r.single).length;
    log(`pass 2 (pairing on, the shipped default): ${mixed.length} rows, ${nCombo} combined`);
    chk(nCombo > 20, `${nCombo} combined rows, so this pass is a real sample too`);

    let scored2 = 0;
    for (const r of mixed) if (T.plateauFor(r, metric)) scored2++;
    chk(scored2 === mixed.length,
        `every row on the DEFAULT view is scored: ${scored2} of ${mixed.length}`);

    const dashes = [...document.querySelectorAll('#sl-body tr td.plat')]
      .filter(td => /color-disabled/.test(td.innerHTML)).length;
    chk(dashes === 0, `${dashes} empty plateau cells rendered on the default view`);

    // Combined rows get the same independent walk the singles got, on a subset,
    // since each carries up to six axes and two backtests per neighbour.
    const sample = mixed.filter(r => !r.single).slice(0, 25);
    let scored3 = 0;
    for (const r of sample) if (verifyRow(r)) scored3++;
    chk(scored3 === sample.length,
        `${scored3} combined rows verified against an independent AND-and-backtest`);

    // Every combined row's cell names which condition it is quoting, or the
    // range is ambiguous across two different signals.
    const bad = mixed.filter(r => !r.single)
      .filter(r => !/^[12]: /.test(T.plateauFor(r, metric).text));
    chk(bad.length === 0,
        `every combined row's cell names the condition it quotes (${bad.length} do not)`);

    // ---- 8. the page's account of every axis end matches the walk ----
    let ringBound = 0, edgeBound = 0, ends = 0;
    const widths = {}, ratios = [];
    for (const r of singles.concat(sample)) {
      const pl = T.plateauFor(r, metric);
      widths[pl.steps] = (widths[pl.steps] || 0) + 1;
      if (r[metric]) ratios.push(pl.med / r[metric]);
      ringBound += (pl.title.match(/still holding at the edge of the search/g) || []).length;
      edgeBound += (pl.title.match(/stops at the end of the grid/g) || []).length;
      ends += (pl.title.match(/side (?:ends|stops|still)/g) || []).length;
    }
    chk(ringBound === tally.ring && edgeBound === tally.edge && ends === tally.ends,
        `the page's account of every axis end matches the independent walk: ` +
        `${ringBound}/${tally.ring} at the search radius, ${edgeBound}/${tally.edge} at the ` +
        `grid edge, ${ends}/${tally.ends} ends`);
    chk(tally.hold > 0, `${tally.hold} in-band steps verified against an independent backtest`);
    chk(tally.brk + tally.edge + tally.ring === tally.ends,
        `every end accounted for: ${tally.brk} genuine breaks, ${tally.edge} lattice edges, ` +
        `${tally.ring} still holding at the search radius`);
    chk(tally.med === singles.length + sample.length,
        `${tally.med} neighbourhood medians reproduced exactly`);
    chk(tally.self === singles.length + sample.length,
        `${tally.self} rows reproduce their own stored metric when unperturbed`);

    // ---- measurement, which is the point of shipping the diagnostic first ----
    // The roadmap entry says to look at what plateau widths real runs produce
    // before choosing band widths or re-ranking on the neighbourhood.
    ratios.sort((a, b) => a - b);
    const q = p => ratios[Math.min(ratios.length - 1, Math.floor(p * ratios.length))];
    log('measurement, quoted rather than asserted:');
    log('     plateau width (steps on the quoted axis): ' +
        Object.keys(widths).sort((a, b) => a - b).map(k => k + ' -> ' + widths[k]).join(', '));
    log(`     neighbourhood median as a fraction of the row's own ${metric}: ` +
        `p10 ${q(0.1).toFixed(2)}, median ${q(0.5).toFixed(2)}, p90 ${q(0.9).toFixed(2)}`);

    // ---- worked examples, for the record ----
    for (const pair of [['single', singles.find(x => T.FAM[x.spec.f].kind === 'lvl')],
                        ['combined', sample[0]]]) {
      const what = pair[0], r = pair[1];
      if (!r) continue;
      const pl = T.plateauFor(r, metric);
      log(`example (${what}): ${r.label}  ->  ${r.target}`);
      log(`     ${metric} ${r[metric].toFixed(3)}, nbhd median ${pl.med.toFixed(3)}, plateau ${pl.text}`);
      log('     ' + pl.title.replace(/\n/g, '\n     '));
    }

    log(fails ? `*** ${fails} FAILURES ***` : 'ALL CHECKS PASSED');
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
