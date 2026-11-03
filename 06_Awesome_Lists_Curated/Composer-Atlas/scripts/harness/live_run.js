/* End-to-end live run: does the page still run, render, and report the window
   correctly now that warm-up is charged to the sample start? */
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

    // warm-up should scale with the min period floor: floor 252 means the only
    // active window IS 252, floor 5 means the grid still reaches 252.
    for (const minP of [10, 252]) {
      T.targets.clear(); ['QQQ'].forEach(s => T.targets.add(s));
      T.compares.clear(); ['SPY', 'QQQ', 'TLT', 'SMH'].forEach(s => T.compares.add(s));
      document.getElementById('sl-minp').value = String(minP);
      T.syncChips();

      const est = document.getElementById('sl-est').textContent;
      log(`minP=${minP} estimate: ${est}`);
      chk(/lost to warm-up/.test(est), `minP=${minP}: estimate names the warm-up cost`);

      const panel = document.getElementById('sl-results-panel');
      panel.style.display = 'none';
      document.getElementById('sl-run').click();
      await waitFor(() => panel.style.display !== 'none', 600000);

      const sc = T.sigCache, w = sc.win;
      const expWarm = T.activeWindows(minP).slice(-1)[0];
      chk(w.warm === expWarm, `minP=${minP}: win.warm ${w.warm} === longest active window ${expWarm}`);
      const bare = T.windowInfo(['SPY', 'QQQ', 'TLT', 'SMH'], 0);
      chk(w.s0 === Math.min(T.N, bare.s0 + expWarm),
          `minP=${minP}: s0 ${w.s0} = listing ${bare.s0} + warm ${expWarm}`);
      chk(w.len === T.N - w.s0, `minP=${minP}: len ${w.len} = N - s0`);

      // renderResults() is debounced through requestRender(), so the panel
      // becomes visible BEFORE the table body is filled. Waiting on the panel
      // alone is a race that virtual time makes intermittent.
      let rows = 0;
      try {
        rows = await waitFor(() => document.querySelectorAll('#sl-body tr').length, 60000);
      } catch (e) { /* leave rows at 0 and let the check report it */ }
      chk(rows > 0, `minP=${minP}: ${rows} result rows rendered`);
      const meta = document.getElementById('sl-meta').textContent;
      chk(/indicator warm-up/.test(meta), `minP=${minP}: meta line explains the warm-up`);
      log(`     meta: ${meta}`);
      log(`     specs=${sc.store.specs.n.toLocaleString()} rows=${sc.store.n.toLocaleString()} days=${w.len}`);
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
