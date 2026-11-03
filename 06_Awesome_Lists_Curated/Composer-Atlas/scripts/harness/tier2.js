/* V2.4 Tier 2 structural read: assert the numbers, not the markup (v1.77.0)

   The tree below is CONSTRUCTED so that every measure has one correct answer
   that can be worked out by hand, rather than sampled from a real symphony
   where a wrong answer and a right one both look plausible. That is the whole
   point: a render test on real data passes on a verdict that is flatly false.

   The fixture, and what each part of it is for:
     - RSI gates at 79, 30 and 28. 79 and 28 are off the conventional levels,
       30 is on one, so "threshold choice" must find exactly 2.
     - 28 and 30 are two apart on the same indicator, so "near-duplicate gates"
       must find exactly 1 pair, and must NOT pair 79 with either.
     - Windows 10, 70 and 75. 75 and 70 are five apart, so "lookback windows"
       must find exactly 1 close pair and must not pair 10 with 70.
     - Three distinct tickers, one of them held down two different branches, so
       the asset count must be 3 and not 4.
     - Three real conditions plus one else, so the condition count must be 3:
       an else branch carries no threshold and is not a decision.
     - Depth is exactly 3 from root to asset.
*/
(function () {
  var OUT = [];
  function log(m) { OUT.push(m); }
  var fails = 0;
  function chk(ok, msg) { if (!ok) { fails++; log('FAIL ' + msg); } else log('ok   ' + msg); }
  function eq(got, want, msg) {
    chk(got === want, msg + ' (got ' + got + ', want ' + want + ')');
  }

  function asset(t) { return { step: 'asset', ticker: t, name: t }; }
  function cond(fn, tkr, win, cmp, rhs, kid) {
    return {
      step: 'if-child', 'is-else-condition?': false, 'rhs-fixed-value?': true,
      'lhs-fn': fn, 'lhs-val': tkr, 'lhs-fn-params': { window: win },
      comparator: cmp, 'rhs-val': String(rhs), children: [kid]
    };
  }
  var RSI = 'relative-strength-index';
  var FIXTURE = {
    step: 'root', name: 'Fixture', children: [{
      step: 'if', children: [
        cond(RSI, 'SPY', 10, 'gt', 79, asset('SOXL')),
        cond(RSI, 'QQQ', 70, 'lt', 30, asset('TQQQ')),
        cond(RSI, 'QQQ', 75, 'lt', 28, asset('TQQQ')),
        { step: 'if-child', 'is-else-condition?': true, children: [asset('BIL')] }
      ]
    }]
  };

  try {
    var T = window.__of;
    if (!T) throw new Error('hook missing');
    log('V2.4 Tier 2 structural read');
    log('');

    var o = T.walkTree(FIXTURE);
    eq(o.conds, 3, 'three conditions, the else is not one');
    eq(o.elses, 1, 'one else branch');
    eq(o.nAssets, 3, 'three distinct assets, TQQQ held twice counts once');
    eq(o.depth, 3, 'depth is 3 from root to asset');
    eq(o.thresholds.length, 3, 'three fixed thresholds');
    eq(Object.keys(o.windows).length, 3, 'three distinct windows');
    eq(T.freeParams(o), 6, 'free parameters = 3 thresholds + 3 distinct windows');

    var odd = T.offConvention(o.thresholds);
    eq(odd.length, 2, 'two RSI gates sit off convention');
    chk(odd.indexOf(30) === -1, '30 is conventional and is not flagged');
    chk(odd.indexOf(79) !== -1 && odd.indexOf(28) !== -1, '79 and 28 are flagged');

    var dup = T.nearDuplicates(o.thresholds);
    eq(dup.length, 1, 'one near-duplicate pair');
    chk(/28 and 30/.test(dup[0]), 'the pair is 28 and 30, got ' + dup[0]);

    // ---- a distinct window used twice must still count once ----
    var reused = {
      step: 'root', children: [{
        step: 'if', children: [
          cond(RSI, 'SPY', 14, 'gt', 70, asset('A')),
          cond(RSI, 'QQQ', 14, 'lt', 30, asset('B')),
          { step: 'if-child', 'is-else-condition?': true, children: [asset('BIL')] }
        ]
      }]
    };
    var o2 = T.walkTree(reused);
    eq(Object.keys(o2.windows).length, 1, 'a window reused in two branches counts once');
    eq(T.freeParams(o2), 3, 'free params = 2 thresholds + 1 distinct window');

    // ---- a comparison between two indicators has no tunable constant ----
    var noFixed = {
      step: 'root', children: [{
        step: 'if', children: [{
          step: 'if-child', 'is-else-condition?': false, 'rhs-fixed-value?': false,
          'lhs-fn': RSI, 'lhs-val': 'SPY', 'lhs-fn-params': { window: 10 },
          'rhs-fn': RSI, 'rhs-val': 'QQQ', 'rhs-fn-params': { window: 10 },
          comparator: 'gt', children: [asset('A')]
        }, { step: 'if-child', 'is-else-condition?': true, children: [asset('BIL')] }]
      }]
    };
    var o3 = T.walkTree(noFixed);
    eq(o3.thresholds.length, 0, 'comparing two indicators contributes no threshold');
    eq(o3.conds, 1, 'it is still a condition');

    // ---- parseSymphony accepts the shapes that actually arrive ----
    chk(T.parseSymphony('not json') === null, 'plain text is not a symphony');
    chk(T.parseSymphony('{bad') === null, 'malformed JSON returns null, does not throw');
    chk(T.parseSymphony(JSON.stringify(FIXTURE)) !== null, 'a bare tree parses');
    chk(T.parseSymphony(JSON.stringify({ symphony: FIXTURE })) !== null, 'a wrapped tree parses');
    var url = 'https://app.composer.trade/symphony/4aI4kVT5cEc0XJpTLei3/details';
    chk(T.parseSymphony(url) === null, 'a URL is not treated as JSON');
    eq(T.extractId(url), '4aI4kVT5cEc0XJpTLei3', 'the URL still yields its ID');

    // ---- the rendered panel must say it is unvalidated ----
    // Not a style check: the PRD requires Tier 2 never be presented as a
    // verdict, and that requirement lives in the words on the page.
    var html = T.renderStructure(FIXTURE, 12.5);
    chk(/observations about construction/.test(html), 'the panel calls itself observations');
    chk(/not a verdict/.test(html), 'the panel denies being a verdict');
    chk(/none of them has been tested/.test(html), 'the panel states it is untested');
    chk(html.indexOf('12.5 years') !== -1, 'the fitted era is used as the denominator');
    chk(/2\.1 years/.test(html), '12.5 years over 6 parameters reads as 2.1 years each');
    chk(T.renderStructure({ step: 'root', children: [] }, null) === '',
        'an empty tree renders nothing rather than an empty panel');
  } catch (e) {
    fails++;
    log('THREW ' + (e && e.message) + '\n' + (e && e.stack));
  }

  log('');
  log(fails ? '*** ' + fails + ' FAILURES ***' : 'DONE');
  var d = document.createElement('pre');
  d.id = 'HARNESS'; d.textContent = OUT.join('\n');
  document.body.appendChild(d);
})();
