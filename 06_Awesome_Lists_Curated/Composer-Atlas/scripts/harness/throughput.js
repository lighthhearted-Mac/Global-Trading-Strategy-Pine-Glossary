/* One Pass-1 run per Edge invocation, timed by the PARENT process.

   Timing a run is the one thing the normal harness rig cannot do, and the
   reason is worth writing down because it looks like a bug for a long time.

   All the other harnesses run under --virtual-time-budget, which is what lets
   --dump-dom wait for asynchronous work instead of dumping at the load event.
   Under that flag the page clock is not a clock. It is paused during
   synchronous compute and fast-forwarded through idle gaps, and the
   fast-forwarding is wildly non-linear: an identical driver reported 1,154 ms
   of `performance.now()` elapsed for a 4-ticker run and 4,095,136 ms for an
   8-ticker one. Summed compute time is no better (63 ms and 70 ms across those
   same two runs, i.e. it is not measuring the compute either). At 16 tickers
   the accumulated virtual time exceeded the 2e9 ms budget, Edge shut the
   browser down mid-run, and the harness reported no output at all.

   So this driver does not use virtual time. It runs in real time, with no
   --dump-dom, and reports through `console.info`, which Edge writes to stderr
   the moment it happens when launched with --enable-logging=stderr. The parent
   reads those lines as they arrive and timestamps them with its own clock.

   Reporting START separately from DONE means browser startup, page parse and
   the price-data load fall outside the measured interval, so no line fitting
   is needed to subtract them.

   `window.__cfg` is injected by _edge.py: { tickers: N, targets: [...] }. */
(function () {
  const cfg = window.__cfg || { tickers: 20, targets: ['QQQ'] };
  const say = m => console.info('HARNESS ' + m);

  function waitFor(fn, polls) {
    return new Promise((res, rej) => {
      let n = 0;
      (function tick() {
        let v; try { v = fn(); } catch (e) { return rej(e); }
        if (v) return res(v);
        if (++n > (polls || 4000000)) return rej(new Error('gave up after ' + n + ' polls'));
        setTimeout(tick, 25);
      })();
    });
  }

  async function main() {
    await waitFor(() => window.__t && window.__t.PD && document.getElementById('sl-run'));
    const T = window.__t;
    const TK = Object.keys(T.PD.tickers);

    // Full-history tickers only, so the common sample window does not collapse
    // and cases at different sizes stay comparable.
    const FULL = TK.filter(t => {
      const c = T.PD.tickers[t].closes;
      let f = 0; while (f < c.length && c[f] == null) f++;
      return (c.length - f) / c.length >= 0.99;
    });

    document.getElementById('sl-cpu').value = 'max';
    T.targets.clear(); cfg.targets.forEach(s => T.targets.add(s));
    T.compares.clear(); FULL.slice(0, cfg.tickers).forEach(s => T.compares.add(s));
    T.syncChips();

    const panel = document.getElementById('sl-results-panel');
    panel.style.display = 'none';

    say('START');
    document.getElementById('sl-run').click();
    await waitFor(() => panel.style.display !== 'none');
    await waitFor(() => document.querySelectorAll('#sl-body tr').length);

    const sc = T.sigCache;
    say('DONE ' + JSON.stringify({
      tickers: cfg.tickers, targets: sc.tgt.length,
      specs: sc.store.specs.n, rows: sc.store.n, days: sc.win.len,
      work: sc.store.specs.n * sc.tgt.length * sc.win.len,
    }));
  }

  main().catch(e => say('FAIL ' + (e && e.message)));
})();
