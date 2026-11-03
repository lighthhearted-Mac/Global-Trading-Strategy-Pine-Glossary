/* Do the section-3 settings survive a refresh, and does Default put them back?

   This is the second harness that needs TWO Edge invocations sharing one
   --user-data-dir, because the thing under test is localStorage and a single
   invocation cannot observe a reload. `window.__cfg.phase` selects which half
   runs; scripts/run_harness.py drives both with profile='settings'.

   Phase 1: run_harness.py deletes the profile first, so this is a browser that
   has never seen the page. Check the shipped HTML matches DEFAULT_SETTINGS,
   then change every control to a distinct non-default value and let the change
   listeners persist it.
   Phase 2: a fresh browser process over the same profile. The controls must
   come back changed, and clicking Default must put every one of them back and
   write that through to storage.

   Signal families are covered too (v1.24.7): they persist as a list of the ids
   that are ON, so a family added to FAMILIES later defaults to OFF for a
   returning visitor rather than silently switching itself on. The test toggles
   one family each way, because a family turned OFF is the case a naive
   "remember the overrides" scheme gets wrong. */
(function () {
  const OUT = [];
  const log = m => OUT.push(m);
  let fails = 0;
  const ok = (cond, msg) => { log((cond ? 'ok   ' : 'FAIL ') + msg); if (!cond) fails++; };

  function report() {
    log(fails ? fails + ' CHECK(S) FAILED' : 'ALL CHECKS PASSED');
    const p = document.createElement('pre');
    p.id = 'HARNESS'; p.textContent = OUT.join('\n');
    document.body.appendChild(p);
  }
  function waitFor(fn, polls) {
    return new Promise((res, rej) => {
      let n = 0;
      (function tick() {
        let v; try { v = fn(); } catch (e) { return rej(e); }
        if (v) return res(v);
        if (++n > (polls || 200000)) return rej(new Error('gave up'));
        setTimeout(tick, 25);
      })();
    });
  }

  // Distinct from every default, and each value legal for its own control.
  const CHANGED = {
    'sl-combo': '1',
    'sl-minp': '21',
    'sl-tim': '33.5',
    'sl-mdd': '42',
    'sl-quant': '0.5',
    'sl-cpu': 'low',
  };

  const read = id => (document.getElementById(id) || {}).value;
  const famBox = id => [...document.querySelectorAll('#sl-families input')].find(i => i.value === id);
  const famsOn = () => [...document.querySelectorAll('#sl-families input')]
    .filter(i => i.checked).map(i => i.value).sort();

  // One family that ships ON and one that ships OFF, so the test covers both
  // directions. Turning a family off is the case that a naive "store the ones
  // that are on" scheme gets right and a "store overrides" scheme gets wrong.
  const FAM_OFF = 'rsi_cmp';    // on by default
  const FAM_ON = 'ema_cmp';     // off by default

  async function main() {
    await waitFor(() => window.__t && window.__t.PD && document.getElementById('sl-run'));
    const T = window.__t;
    const D = T.DEFAULT_SETTINGS;
    const phase = (window.__cfg || {}).phase;
    log('phase ' + phase);

    if (phase === 1) {
      // Phase 1 only means anything on a browser that has never seen this page,
      // so run_harness.py deletes the shared profile directory before starting.
      // Reloading from inside the driver cannot substitute for that: __cfg is
      // re-injected on every load, so a self-reload would loop forever.
      let pre = null;
      try { pre = localStorage.getItem(T.SETTINGS_STORE_KEY); } catch (e) { /* ignore */ }
      ok(pre === null, 'phase 1 started with empty storage (profile was cleared)');

      // The shipped HTML attributes must agree with DEFAULT_SETTINGS. If they
      // drift, a first-time visitor sees different values from what Default
      // restores, which is the exact bug the single source of truth prevents.
      for (const id of T.SETTING_IDS) {
        ok(read(id) === D[id], 'first load ' + id + ' = ' + read(id) + ' (want ' + D[id] + ')');
      }
      // The owner's specified defaults, asserted by value so a silent edit to
      // DEFAULT_SETTINGS cannot pass this harness.
      ok(D['sl-minp'] === '10', 'default min period is 10');
      ok(D['sl-tim'] === '15', 'default time in market is 15 (percent)');
      ok(D['sl-mdd'] === '69', 'default drawdown floor is 69 (percent, unsigned)');
      ok(D['sl-quant'] === '0', 'default prune quantile is 0');
      ok(D['sl-cpu'] === 'high', 'default CPU load is high');

      // The number inputs must be able to hold their defaults: a value outside
      // min/max renders but reports as out of range in some browsers.
      for (const id of ['sl-tim', 'sl-mdd', 'sl-quant']) {
        const el = document.getElementById(id);
        ok(el.checkValidity(), id + ' default is inside its own min/max');
      }

      // Families ship at their FAMILIES defaults.
      const shipped = FAMILIES_DEFAULT(T);
      ok(famsOn().join(',') === shipped.join(','), 'first load families match FAM defaults');
      ok(!!famBox(FAM_OFF) && famBox(FAM_OFF).checked, FAM_OFF + ' ships on');
      ok(!!famBox(FAM_ON) && !famBox(FAM_ON).checked, FAM_ON + ' ships off');

      // Now change everything and let the listeners persist it.
      for (const id of T.SETTING_IDS) {
        const el = document.getElementById(id);
        el.value = CHANGED[id];
        el.dispatchEvent(new Event('change', { bubbles: true }));
      }
      for (const id of T.SETTING_IDS) ok(read(id) === CHANGED[id], 'changed ' + id + ' to ' + CHANGED[id]);

      // Toggle one family each way, through the real change listener.
      famBox(FAM_OFF).checked = false;
      famBox(FAM_OFF).dispatchEvent(new Event('change', { bubbles: true }));
      famBox(FAM_ON).checked = true;
      famBox(FAM_ON).dispatchEvent(new Event('change', { bubbles: true }));
      const wantFams = famsOn();
      ok(wantFams.indexOf(FAM_OFF) === -1 && wantFams.indexOf(FAM_ON) !== -1,
         'toggled ' + FAM_OFF + ' off and ' + FAM_ON + ' on');

      let raw = null;
      try { raw = localStorage.getItem(T.SETTINGS_STORE_KEY); } catch (e) { /* ignore */ }
      ok(!!raw, 'settings written to localStorage');
      if (raw) {
        const v = JSON.parse(raw);
        ok(T.SETTING_IDS.every(id => v[id] === CHANGED[id]), 'stored object matches the controls');
        ok(Array.isArray(v.families) && v.families.slice().sort().join(',') === wantFams.join(','),
           'stored families match the checkboxes');
      }
      report();
      return;
    }

    // ---- phase 2: a new browser process over the same profile ----
    for (const id of T.SETTING_IDS) {
      ok(read(id) === CHANGED[id], 'survived reload ' + id + ' = ' + read(id) + ' (want ' + CHANGED[id] + ')');
    }

    ok(!famBox(FAM_OFF).checked, 'survived reload: ' + FAM_OFF + ' still off');
    ok(famBox(FAM_ON).checked, 'survived reload: ' + FAM_ON + ' still on');

    // The min period drives the estimate, so a restored value that never
    // reached the estimate would be a silent half-restore.
    ok(String(T.activeWindows(parseInt(read('sl-minp'), 10))[0]) === '21',
       'restored min period reached activeWindows');

    document.getElementById('sl-default').click();
    await waitFor(() => read('sl-cpu') === D['sl-cpu']);
    for (const id of T.SETTING_IDS) {
      ok(read(id) === D[id], 'Default button reset ' + id + ' = ' + read(id));
    }

    const shipped2 = FAMILIES_DEFAULT(T);
    ok(famsOn().join(',') === shipped2.join(','), 'Default button reset families to FAM defaults');

    let raw2 = null;
    try { raw2 = localStorage.getItem(T.SETTINGS_STORE_KEY); } catch (e) { /* ignore */ }
    ok(!!raw2, 'Default button wrote through to storage');
    if (raw2) {
      const v = JSON.parse(raw2);
      ok(T.SETTING_IDS.every(id => v[id] === D[id]), 'stored object is back to defaults');
    }
    report();
  }

  function FAMILIES_DEFAULT(T) {
    return T.FAMILIES.filter(f => f.on).map(f => f.id).sort();
  }

  main().catch(e => { log('HARNESS EXCEPTION: ' + (e && e.message)); report(); });
})();
