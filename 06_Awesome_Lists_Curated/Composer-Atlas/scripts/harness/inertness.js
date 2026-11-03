/* Roadmap item 2 measurement: how degenerate are cross-ticker operand pairs in
   the three price-scale families (map_cmp, ema_cmp, stdp_cmp)?

   A spec is "degenerate" if it is true on more than 99% or fewer than 1% of the
   days both operands are defined: it separates almost nothing, so it costs a
   full Pass 1 slot and self-prunes at the end for no gain.

   Controls: rsi_cmp and cum_cmp are scale-free and must NOT show the same
   pattern. If they do, the measurement is wrong, not the families. */
(function () {
  const OUT = [];
  const log = m => OUT.push(m);

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
    const T = window.__t, PD = T.PD;
    const TK = Object.keys(PD.tickers);
    const W = [5, 21, 63, 252];
    log('tickers=' + TK.length + ' windows=' + JSON.stringify(W));

    // Families measured, plus two scale-free controls.
    const FAMS = ['map_cmp', 'ema_cmp', 'stdp_cmp', 'rsi_cmp', 'cum_cmp'];
    const inds = [];
    for (const id of FAMS) inds.push(T.FAM[id].a);

    const cache = T.buildCaches(TK, inds, W);
    const N = T.N;

    // Flatten to operands: [tickerIndex, window] -> series
    for (const id of FAMS) {
      const ind = T.FAM[id].a;
      const ops = [];
      for (let i = 0; i < TK.length; i++)
        for (const p of W) ops.push({ t: i, p: p, s: cache[TK[i]][ind][p] });

      let xN = 0, xDeg = 0, xDead = 0, xInert = 0, xCross = [];   // cross-ticker
      let sN = 0, sDeg = 0, sDead = 0, sInert = 0, sCross = [];   // same-ticker, different window
      for (let a = 0; a < ops.length; a++) {
        const A = ops[a];
        for (let b = 0; b < ops.length; b++) {
          if (a === b) continue;
          const B = ops[b];
          if (A.t !== B.t && A.p !== B.p) continue;   // sample: cross pairs at equal window only
          let n = 0, tr = 0, cross = 0, prev = -1;
          for (let k = 0; k < N; k++) {
            const l = A.s[k], r = B.s[k];
            if (l !== l || r !== r) continue;
            n++;
            const cur = l > r ? 1 : 0;
            if (cur) tr++;
            if (prev !== -1 && cur !== prev) cross++;
            prev = cur;
          }
          if (n < 250) continue;
          const f = tr / n;
          const deg = (f > 0.99 || f < 0.01);
          const dead = (f === 1 || f === 0);
          // A pair that flips fewer than 12 times in ~16 years is a regime
          // marker, not a signal: it is "before/after 2018" wearing a
          // condition's clothes, and it is exactly what over-fits.
          const inert = cross < 12;
          if (A.t === B.t) { sN++; if (deg) sDeg++; if (dead) sDead++; if (inert) sInert++; sCross.push(cross); }
          else { xN++; if (deg) xDeg++; if (dead) xDead++; if (inert) xInert++; xCross.push(cross); }
        }
      }
      const pc = (a, b) => b ? (100 * a / b).toFixed(1) + '%' : 'n/a';
      const med = a => { if (!a.length) return 'n/a'; a.sort((x, y) => x - y); return a[a.length >> 1]; };
      log(id + ' | CROSS n=' + xN + ' deg=' + pc(xDeg, xN) + ' dead=' + pc(xDead, xN) +
          ' inert(<12 flips)=' + pc(xInert, xN) + ' medFlips=' + med(xCross) +
          ' || SAME n=' + sN + ' deg=' + pc(sDeg, sN) + ' dead=' + pc(sDead, sN) +
          ' inert=' + pc(sInert, sN) + ' medFlips=' + med(sCross));
    }
    log('DONE');
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
