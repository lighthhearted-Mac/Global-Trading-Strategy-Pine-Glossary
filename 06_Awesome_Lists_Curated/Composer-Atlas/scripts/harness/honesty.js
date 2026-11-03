/* The honesty check (v1.79.0), verified end to end.

   THIS HARNESS EXISTS BECAUSE OF A SPECIFIC PAST FAILURE. An earlier round of
   work on this page passed 24 render assertions on a verdict that was flatly
   false: everything was checked except whether the number being displayed was
   the right number. So this file does two separate jobs, and the second is the
   one that matters.

     1. RENDER. The panel appears, sits above the results table, and carries a
        bucket class.
     2. THE CLAIM. The whole check is recomputed here, independently, from the
        page's own primitives, and compared against what the panel printed. If
        the page's sample, its rotations, or its arithmetic are wrong, the two
        disagree and this fails.

   Job 2 hardcodes HON_SAMPLE, HON_ROTATIONS and the shuffle seed, which are
   page-side constants this harness cannot read. That is deliberate: if someone
   changes them in the page without changing them here, this harness fails
   loudly, which is the correct outcome for a measurement whose constants are
   part of what it means.
*/
(function () {
  const OUT = [];
  const log = m => OUT.push(m);
  let fails = 0;
  const chk = (ok, msg) => { if (!ok) { fails++; log('FAIL ' + msg); } else log('ok   ' + msg); };

  const HON_SAMPLE = 1500;
  const HON_ROTATIONS = 8;

  window.confirm = () => true;

  function waitFor(fn, ms) {
    return new Promise((res, rej) => {
      const t0 = Date.now();
      (function tick() {
        let v; try { v = fn(); } catch (e) { return rej(e); }
        if (v) return res(v);
        if (Date.now() - t0 > ms) return rej(new Error('timeout'));
        setTimeout(tick, 25);
      })();
    });
  }

  async function main() {
    await waitFor(() => window.__t && window.__t.PD && document.getElementById('sl-run'), 60000);
    const T = window.__t;
    document.getElementById('sl-cpu').value = 'max';

    T.targets.clear(); ['QQQ'].forEach(s => T.targets.add(s));
    T.compares.clear(); ['SPY', 'QQQ', 'TLT', 'SMH'].forEach(s => T.compares.add(s));
    document.getElementById('sl-minp').value = '10';
    T.syncChips();

    const panel = document.getElementById('sl-results-panel');
    panel.style.display = 'none';
    document.getElementById('sl-run').click();
    await waitFor(() => panel.style.display !== 'none', 900000);
    await waitFor(() => document.querySelectorAll('#sl-body tr').length, 120000);

    const el = document.getElementById('sl-honesty');

    // ---------------------------------------------------------------- render
    chk(!!el, 'the panel element exists');
    chk(el.style.display !== 'none', 'the panel is visible after a run');
    chk(el.textContent.trim().length > 100, 'the panel has real copy in it');
    const cls = (el.className.match(/q-(good|fair|poor|bad)/) || [])[0];
    chk(!!cls, 'the panel carries exactly one bucket class: ' + cls);

    // It must sit ABOVE the table. A warning a reader meets after the numbers
    // is not a warning, it is a footnote.
    const tbl = document.getElementById('sl-table');
    chk(el.compareDocumentPosition(tbl) & Node.DOCUMENT_POSITION_FOLLOWING,
        'the panel precedes the results table in document order');

    // ------------------------------------------------- the coarseness rule
    // No number carrying a decimal point may appear in the VERDICT. The
    // components below it are the measured figures and are supposed to be
    // exact; the interpretation on top of them is not allowed to imply a
    // precision the measurement does not have. The percentile moved from 38 to
    // 63 between two runs of one configuration, which is the whole reason.
    const head = el.querySelector('.sl-h-head').textContent;
    const comp = el.querySelector('.sl-h-comp');
    const verdict = head + ' ' + Array.from(el.childNodes)
      .filter(nd => nd.nodeType === 3).map(nd => nd.textContent).join(' ');
    chk(!/\d+\.\d/.test(verdict), 'the verdict contains no number with a decimal point');
    chk(!/\d+\s*(?:th|st|nd|rd)\s+percentile/i.test(verdict), 'the verdict quotes no percentile');
    chk(!!comp && /Best Calmar in a sample of/.test(comp.textContent),
        'the components are shown alongside the verdict');
    log('     verdict: ' + verdict.replace(/\s+/g, ' ').trim().slice(0, 200));
    log('     components: ' + comp.textContent.replace(/\s+/g, ' ').trim());

    // -------------------------------------------------------------- the claim
    // Recompute the entire check from the page's own primitives and require
    // the page's printed figures to match.
    const sc = T.sigCache, win = sc.win, N = sc.N;
    const specs = sc.store.specs;
    const target = sc.tgt[0];
    const lret = sc.targetLret[target];
    const s0 = Math.max(1, win.s0);

    const stride = Math.max(1, Math.floor(specs.n / HON_SAMPLE));
    const idx = [];
    for (let i = 0; i < specs.n; i += stride) idx.push(i);
    let seed = 0x9e3779b9;
    const rnd = () => {
      seed ^= seed << 13; seed ^= seed >>> 17; seed ^= seed << 5;
      return ((seed >>> 0) / 4294967296);
    };
    for (let i = idx.length - 1; i > 0; i--) {
      const j = Math.floor(rnd() * (i + 1));
      const t = idx[i]; idx[i] = idx[j]; idx[j] = t;
    }
    const buf = new Uint8Array(N);
    const arrs = idx.map(i => Uint8Array.from(T.evalSpecAt(specs, i, sc.cache, buf)));
    // Admission AND the shipped display filter, mirroring the page. Reading
    // these from the live controls rather than hardcoding 15 is deliberate: a
    // harness that pins its own setting is how a feature ships invisible.
    const timPct = parseFloat(document.getElementById('sl-tim').value);
    const mddPct = parseFloat(document.getElementById('sl-mdd').value);
    const TIM = isFinite(timPct) ? timPct / 100 : 0;
    const MDD = isFinite(mddPct) ? -(mddPct / 100) : -1;
    chk(timPct === 15, `the run used the SHIPPED default Min Time in Market (${timPct}%)`);
    const bestOf = (l) => {
      let best = -Infinity;
      for (let i = 0; i < arrs.length; i++) {
        const m = T.backtest(arrs[i], l, win.s0, win.len);
        if (m.total > 0 && m.calmar === m.calmar && m.tim > TIM && m.maxDD > MDD
            && m.calmar > best) best = m.calmar;
      }
      return best;
    };
    const span = N - s0;
    const rot = (off) => {
      const out = Float64Array.from(lret);
      for (let i = 0; i < span; i++) out[s0 + i] = lret[s0 + ((i + off) % span)];
      return out;
    };
    const real = bestOf(lret);
    const nulls = [];
    for (let r = 0; r < HON_ROTATIONS; r++) {
      const b = bestOf(rot(Math.floor(span * (r + 1) / (HON_ROTATIONS + 1))));
      if (isFinite(b)) nulls.push(b);
    }
    nulls.sort((a, b) => a - b);
    let beat = 0;
    for (const v of nulls) if (real > v) beat++;

    const txt = comp.textContent;
    const pBeat = (txt.match(/beat (\d+) of (\d+)/) || []);
    chk(pBeat.length === 3, 'the components state a beat count');
    chk(Number(pBeat[2]) === nulls.length,
        `rotation count: page ${pBeat[2]} === recomputed ${nulls.length}`);
    chk(Number(pBeat[1]) === beat,
        `THE CLAIM: page says it beat ${pBeat[1]} of ${pBeat[2]}, recomputed ${beat}`);

    const pReal = Number((txt.match(/signals: (-?\d+(?:\.\d+)?)/) || [])[1]);
    const fmt = v => (Math.abs(v) >= 100 ? v.toFixed(0) : v.toFixed(2));
    chk(pReal === Number(fmt(real)),
        `THE CLAIM: page's real best ${pReal} === recomputed ${fmt(real)}`);
    const pMed = Number((txt.match(/median (-?\d+(?:\.\d+)?)/) || [])[1]);
    chk(pMed === Number(fmt(nulls[Math.floor(nulls.length / 2)])),
        `THE CLAIM: page's null median ${pMed} === recomputed ${fmt(nulls[Math.floor(nulls.length / 2)])}`);

    // The bucket must follow from the count, not be chosen separately.
    const want = beat === nulls.length ? 'q-good'
               : beat >= nulls.length - 2 ? 'q-fair'
               : beat > 1 ? 'q-poor' : 'q-bad';
    chk(cls === want, `the bucket follows the count: ${cls} === ${want} for ${beat}/${nulls.length}`);

    // A sample cannot beat the full search it was drawn from.
    // The store keys its metrics under .m, and holds a row per (spec, target),
    // so rows for other targets are excluded by ti. With one target selected
    // that is every row, but the filter is written for the general case rather
    // than for this harness's selection.
    let full = -Infinity;
    for (let i = 0; i < sc.store.n; i++) {
      if (sc.store.ti[i] !== 0) continue;
      if (!(sc.store.m.tim[i] > TIM && sc.store.m.maxDD[i] > MDD)) continue;
      const c = sc.store.m.calmar[i];
      if (c === c && c > full) full = c;
    }
    chk(real <= full + 1e-9,
        `the sampled best ${fmt(real)} does not exceed the full search's best ${fmt(full)}`);
    chk(arrs.length <= specs.n, `sample ${arrs.length} <= lattice ${specs.n}`);
    log(`     lattice=${specs.n.toLocaleString()} sample=${arrs.length} rotations=${nulls.length}`);

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
