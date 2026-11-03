#!/usr/bin/env python3
"""Structural check for the Signal Miner's combined-symphony export.

Background: v1.22.0 through v1.22.4 shipped a combined export Composer would
not accept. It emitted ONE `if` step holding every selected signal as a
sibling `if-child`, with the last flagged `is-else-condition?: true`. Composer
does not work that way. An `if` step takes EXACTLY TWO children, a condition
branch and an else, and rung N+1 nests INSIDE rung N's else.

The single-row export was never broken, because with one rung the flat and
nested shapes are identical. That is precisely why the bug lasted five
versions.

Two things run here:

  1. A source guard over signal-miner.html, confirming the builder still has
     the shape this file mirrors. Without it, someone could rewrite the
     exporter and this port would keep passing against its own stale copy,
     which is the failure the original version of this check had: it asserted
     the shape the builder produced rather than the shape Composer requires.

  2. A Python port of buildComposerLadder, walked to assert the invariant
     directly: every `if` has exactly two children, every else holds exactly
     one thing, rungs nest in Calmar order with NaN last, each rung keeps its
     own target and conditions, and the deepest else is the cash proxy.

There is no JS runtime in this toolchain, so the port cannot execute the real
function. The guard is what keeps the two honest.

Usage:
    python scripts/check_composer_ladder.py
"""
import itertools
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'signal-miner.html'

# Substrings the exporter must still contain for this port to describe it.
# Whitespace-insensitive; each is a regex.
GUARD = [
    (r'function\s+composerLadderIf\s*\(\s*rows\s*,\s*i\s*\)',
     'composerLadderIf is gone or changed signature'),
    (r'composerIfNode\s*\(\s*composerThenChild\s*\(\s*rows\[i\]\s*\)\s*,\s*composerElseChild\s*\(\s*rest\s*\)\s*\)',
     'a rung is no longer built as if(then, else)'),
    (r'children:\s*\[\s*thenChild\s*,\s*elseChild\s*\]',
     'an if step no longer takes exactly two children, which is the whole bug'),
    (r'composerLadderIf\s*\(\s*ordered\s*,\s*0\s*\)',
     'buildComposerLadder no longer starts the recursion'),
    (r"ELSE_TICKER\s*=\s*'BIL'",
     'the cash proxy is no longer BIL'),
]


def guard():
    src = open(SOURCE, encoding='utf-8').read()
    bad = []
    for pattern, why in GUARD:
        if not re.search(pattern, src):
            bad.append(why)
    if bad:
        print('source guard FAILED against signal-miner.html:')
        for why in bad:
            print('  - ' + why)
        print('The exporter changed. Update this port to match, then re-run.')
        return False
    print('source guard: exporter still has the shape this port mirrors')
    return True


_ids = itertools.count(1)
uid = lambda: 'id-' + str(next(_ids))
ELSE_TICKER = 'BIL'
COMPOSER_FN = {
    'rsi_thresh': 'relative-strength-index', 'rsi_cmp': 'relative-strength-index',
    'cum_lvl': 'cumulative-return', 'cum_cmp': 'cumulative-return',
    'ma_cmp': 'moving-average-return', 'std_cmp': 'standard-deviation-return',
}


def condition(sp):
    fn = COMPOSER_FN[sp['f']]
    lhs = {'fn': fn, 'params': {'window': sp['p1']}, 'ticker': '%'}
    if sp['f'] == 'rsi_thresh':
        rhs = {'constant': sp['level']}
    elif sp['f'] == 'cum_lvl':
        rhs = {'constant': round(sp['level'] * 100, 2)}
    else:
        rhs = {'fn': fn, 'params': {'window': sp['p2']}, 'ticker': sp['t2']}
    return {'condition-type': 'binary-compound', 'operator': 'any', 'tickers': [sp['t1']],
            'lhs': lhs, 'comparator': 'gt' if sp['dir'] == 'GT' else 'lt', 'rhs': rhs}


def then_child(row):
    specs = [row['spec']] if row['single'] else row['specs']
    return {'id': uid(), 'step': 'if-child', 'name': 'If',
            'children': [{'id': uid(), 'step': 'asset', 'ticker': row['target']}],
            'is-else-condition?': False,
            'condition': {'condition-type': 'compound', 'operator': 'all',
                          'conditions': [condition(s) for s in specs]}}


def else_child(children):
    return {'id': uid(), 'step': 'if-child', 'name': 'Else',
            'children': children, 'is-else-condition?': True}


def cash():
    return {'id': uid(), 'step': 'asset', 'ticker': ELSE_TICKER}


def if_node(then_c, else_c):
    return {'id': uid(), 'step': 'if', 'name': 'Condition',
            'weight': {'num': 100, 'den': 100}, 'children': [then_c, else_c]}


def ladder_if(rows, i):
    rest = [ladder_if(rows, i + 1)] if i + 1 < len(rows) else [cash()]
    return if_node(then_child(rows[i]), else_child(rest))


def ladder(rows):
    ordered = sorted(rows, key=lambda r: -(r['calmar'] if r['calmar'] == r['calmar'] else -1e18))
    weight = {'id': uid(), 'step': 'wt-cash-equal', 'name': 'Weight',
              'children': [ladder_if(ordered, 0)]}
    targets = list(dict.fromkeys(r['target'] for r in ordered))
    return {'id': 'short', 'step': 'root',
            'name': 'Frontrunner: ' + str(len(ordered)) + ' signals by Calmar to '
                    + ', '.join(targets),
            'children': [weight], 'rebalance': 'daily'}, ordered


NAN = float('nan')
ROWS = [
    {'single': True,  'target': 'TQQQ', 'label': 'A', 'calmar': 0.52,
     'spec': {'f': 'rsi_thresh', 'dir': 'LT', 't1': 'QQQ', 'p1': 10, 'level': 30}},
    {'single': True,  'target': 'SOXL', 'label': 'B', 'calmar': 1.31,
     'spec': {'f': 'ma_cmp', 'dir': 'GT', 't1': 'SPY', 'p1': 20, 't2': 'TLT', 'p2': 50}},
    {'single': False, 'target': 'TECL', 'label': 'C', 'calmar': 0.88,
     'specs': [{'f': 'rsi_cmp', 'dir': 'GT', 't1': 'XLK', 'p1': 10, 't2': 'SPY', 'p2': 20},
               {'f': 'cum_lvl', 'dir': 'LT', 't1': 'KMLM', 'p1': 5, 'level': -0.05}]},
    {'single': True,  'target': 'TQQQ', 'label': 'D', 'calmar': NAN,
     'spec': {'f': 'std_cmp', 'dir': 'LT', 't1': 'IWM', 'p1': 10, 't2': 'DIA', 'p2': 20}},
]


def structure():
    sym, ordered = ladder(ROWS)

    print('rung order (Calmar desc):')
    for i, r in enumerate(ordered):
        c = r['calmar']
        shown = 'NaN' if c != c else format(c, '.2f')
        print('  ' + str(i + 1) + '. ' + r['label'] + '  calmar=' + shown
              + '  -> ' + r['target'])

    node = sym['children'][0]['children'][0]
    depth = 0
    print('nesting:')
    while True:
        assert node['step'] == 'if', 'expected an if step, got ' + node['step']
        kids = node['children']
        assert len(kids) == 2, ('if at depth ' + str(depth) + ' has '
                                + str(len(kids)) + ' children, must be 2')
        then_c, else_c = kids
        assert then_c['is-else-condition?'] is False
        assert else_c['is-else-condition?'] is True
        assert then_c['condition']['conditions'], 'rung has no condition'
        r = ordered[depth]
        assert then_c['children'][0]['ticker'] == r['target'], 'rung holds the wrong target'
        nspec = 1 if r['single'] else len(r['specs'])
        assert len(then_c['condition']['conditions']) == nspec, 'rung lost a condition'
        inner = else_c['children']
        assert len(inner) == 1, 'an else must hold exactly one thing'
        print('  depth ' + str(depth) + ': if ' + r['label'] + ' -> ' + r['target']
              + ', else -> ' + inner[0]['step'])
        depth += 1
        if inner[0]['step'] == 'asset':
            assert inner[0]['ticker'] == 'BIL', 'deepest else must be the cash proxy'
            break
        node = inner[0]

    assert depth == len(ROWS), 'nested ' + str(depth) + ' rungs, expected ' + str(len(ROWS))
    assert [r['label'] for r in ordered] == ['B', 'C', 'A', 'D'], 'wrong priority order'
    assert ordered[-1]['calmar'] != ordered[-1]['calmar'], 'NaN must sort last'

    ids = []

    def walk(n):
        if isinstance(n, dict):
            if 'id' in n:
                ids.append(n['id'])
            for v in n.values():
                walk(v)
        elif isinstance(n, list):
            for v in n:
                walk(v)

    walk(sym)
    assert len(ids) == len(set(ids)), 'duplicate node ids'
    json.dumps(sym)   # must serialise

    print('every if has exactly 2 children, every else holds exactly one thing,')
    print('rungs nest in Calmar order with NaN last, deepest else is BIL, ids unique')
    return True


def main():
    ok = guard()
    try:
        ok &= structure()
    except AssertionError as e:
        print('structure FAILED: ' + str(e))
        ok = False
    print('PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
