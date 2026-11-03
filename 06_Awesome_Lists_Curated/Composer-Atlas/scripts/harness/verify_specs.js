/* Lockstep + sizing verifier. countSpecs() must equal buildSpecs().n exactly
   for every family across a spread of ticker counts and window floors, and the
   evaluated series must be identical through the object and columnar paths. */
(function () {
  const OUT = [];
  const log = m => OUT.push(m);
  let fails = 0;
  const chk = (ok, msg) => { if (!ok) { fails++; log('FAIL ' + msg); } };

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
    await waitFor(() => window.__t && window.__t.PD, 60000);
    const T = window.__t, TK = Object.keys(T.PD.tickers);

    // ---- 1. lockstep, per family and combined
    let cases = 0;
    for (const nT of [1, 2, 5, 8, 20]) {
      const list = TK.slice(0, nT);
      for (const minP of [5, 10, 21, 63, 252]) {
        const W = T.activeWindows(minP);
        for (const f of T.FAMILIES) {
          const fams = {}; fams[f.id] = true;
          const want = T.countSpecs(nT, fams, W);
          const got = T.buildSpecs(list, fams, W).n;
          chk(want === got, `${f.id} n=${nT} minP=${minP}: count ${want} vs build ${got}`);
          cases++;
        }
        const all = {}; T.FAMILIES.forEach(f => all[f.id] = true);
        chk(T.countSpecs(nT, all, W) === T.buildSpecs(list, all, W).n,
            `ALL n=${nT} minP=${minP}`);
        cases++;
      }
    }
    log(`lockstep: ${cases} cases, ${fails} failures`);

    // ---- 2. same-ticker families really never leave the ticker
    for (const f of T.FAMILIES) {
      if (!f.same) continue;
      const fams = {}; fams[f.id] = true;
      const list = TK.slice(0, 8);
      const sp = T.buildSpecs(list, fams, T.activeWindows(10));
      let bad = 0;
      for (let i = 0; i < sp.n; i++) if (sp.a[i] !== sp.b[i]) bad++;
      chk(bad === 0, `${f.id}: ${bad} cross-ticker specs survived`);
      log(`${f.id}: ${sp.n} specs, all same-ticker`);
    }

    // ---- 3. object path vs columnar path produce identical series
    const list8 = TK.slice(0, 8);
    const W10 = T.activeWindows(10);
    for (const f of T.FAMILIES) {
      const fams = {}; fams[f.id] = true;
      const sp = T.buildSpecs(list8, fams, W10);
      const cache = T.buildCaches(list8, T.neededIndicators(fams), W10);
      let diff = 0;
      const step = Math.max(1, Math.floor(sp.n / 40));
      for (let i = 0; i < sp.n; i += step) {
        const a = T.evalSpec(T.specAt(sp, i), cache);
        const b = T.evalSpecAt(sp, i, cache, null);
        for (let k = 0; k < a.length; k++) if (a[k] !== b[k]) { diff++; break; }
      }
      chk(diff === 0, `${f.id}: ${diff} sampled specs differ between paths`);
    }
    log('dual-path: checked all ' + T.FAMILIES.length + ' families');

    // ---- 4. sizing at the real universe
    const dflt = {}, all = {};
    T.FAMILIES.forEach(f => { dflt[f.id] = !!f.on; all[f.id] = true; });
    for (const [name, fams] of [['default', dflt], ['all', all]]) {
      for (const minP of [5, 10]) {
        const W = T.activeWindows(minP);
        log(`sizing ${name} minP=${minP}: 72tk=${T.countSpecs(72, fams, W).toLocaleString()} ` +
            `20tk=${T.countSpecs(20, fams, W).toLocaleString()} ` +
            `8tk=${T.countSpecs(8, fams, W).toLocaleString()} ` +
            `4tk=${T.countSpecs(4, fams, W).toLocaleString()}`);
      }
    }
    const W10b = T.activeWindows(10);
    for (const f of T.FAMILIES) {
      const one = {}; one[f.id] = true;
      log(`  family ${f.id} (${f.kind}${f.same ? ',same' : ''}): ${T.countSpecs(72, one, W10b).toLocaleString()}`);
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
