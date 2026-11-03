#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run one of the Signal Miner headless-Edge harnesses.

    python scripts/run_harness.py verify      # spec lockstep + dual-path equality
    python scripts/run_harness.py live        # end-to-end run, window, rendering
    python scripts/run_harness.py inertness   # cross-ticker operand degeneracy
    python scripts/run_harness.py memory      # peak heap
    python scripts/run_harness.py settings    # persistence and the Default button
    python scripts/run_harness.py plateau     # parameter plateau scoring (V2.2 item A)
    python scripts/run_harness.py all         # the four gates

`verify`, `live`, `settings` and `plateau` gate a change to signal-miner.html.
`inertness`
and `memory` are measurement tools, run when a number in docs/PRD.md needs
re-establishing rather than on every edit.

Timing is deliberately NOT here: see scripts/measure_throughput.py for why a
timed run cannot use this rig at all.

Exits non-zero if a harness reports a failure, so this is CI-shaped.

See scripts/harness/_edge.py for the four traps this all rests on, and
scripts/harness/README.md for what each harness actually checks.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / 'harness'))
import _edge  # noqa: E402

HARNESSES = {
    'settings':  dict(driver='settings.js', timeout=900),
    'verify':    dict(driver='verify_specs.js', timeout=1200),
    'plateau':   dict(driver='plateau.js', timeout=1800),
    'live':      dict(driver='live_run.js', timeout=1800),
    'inertness': dict(driver='inertness.js', timeout=1800),
    'memory':    dict(driver='memory.js', timeout=3600,
                      flags=('--enable-precise-memory-info',)),
}

GATES = ['verify', 'live', 'settings', 'plateau']

# `settings` is the odd one out: it tests localStorage, so it needs two Edge
# invocations over the SAME profile, and the first of them needs that profile to
# be empty. Everything else here runs once on a throwaway profile.
# The name is per-invocation, not a fixed 'settings'. A fixed name is a trap:
# a killed or backgrounded harness leaves msedge.exe holding that directory, the
# rmtree below silently fails, and the next run's Edge exits in a tenth of a
# second against the locked profile. That surfaces as NO HARNESS OUTPUT, which
# reads exactly like a broken driver and sent a long debugging session down the
# wrong hole. A fresh name per run cannot collide with a leftover; the two
# phases still share it, which is the only thing this harness actually needs.
SETTINGS_PROFILE = 'settings-%d' % os.getpid()


def run_settings(timeout=900):
    import shutil
    import tempfile
    prof = Path(tempfile.gettempdir()) / ('composer-harness-' + SETTINGS_PROFILE)
    shutil.rmtree(prof, ignore_errors=True)      # phase 1 must start from nothing
    if prof.exists():
        # Say so rather than letting phase 1 assert against inherited storage.
        return 'could not clear the profile at ' + prof + ' (is an msedge.exe still holding it?)'
    try:
        out = []
        for phase in (1, 2):
            out.append(_edge.run('settings.js', timeout=timeout,
                                 profile=SETTINGS_PROFILE, config={'phase': phase}))
    finally:
        shutil.rmtree(prof, ignore_errors=True)
    return '\n'.join(out)


def one(name):
    print('=' * 70)
    print(name)
    print('=' * 70)
    if name == 'settings':
        txt = run_settings()
    else:
        cfg = dict(HARNESSES[name])
        driver = cfg.pop('driver')
        txt = _edge.run(driver, **cfg)
    print(txt)
    bad = ('FAIL' in txt or 'EXCEPTION' in txt or 'NO HARNESS OUTPUT' in txt
           or not ('ALL CHECKS PASSED' in txt or 'DONE' in txt))
    # A two-phase harness must pass BOTH phases; one 'ALL CHECKS PASSED' in the
    # concatenated output is not enough.
    if name == 'settings' and txt.count('ALL CHECKS PASSED') != 2:
        bad = True
    print(('FAILED: ' if bad else 'ok: ') + name)
    return not bad


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    names = GATES if which == 'all' else [which]
    for n in names:
        if n not in HARNESSES:
            raise SystemExit('unknown harness %r; pick from %s or "all"'
                             % (n, ', '.join(sorted(HARNESSES))))
    ok = True
    for n in names:
        ok = one(n) and ok
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
