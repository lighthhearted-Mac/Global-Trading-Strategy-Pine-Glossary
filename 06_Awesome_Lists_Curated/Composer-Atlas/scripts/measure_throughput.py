#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Measure how fast Pass 1 actually is, timed from OUTSIDE the browser.

    python scripts/measure_throughput.py [sizes...]

Why this is a separate script rather than another harness: a timed run cannot
use the rig in scripts/harness/_edge.py at all. That rig depends on
--virtual-time-budget so that --dump-dom waits for asynchronous work, and under
virtual time the page clock stops being a clock (see the header of
scripts/harness/throughput.js for the measurements that establish it, including
the 16-ticker run that Edge shut down mid-flight).

So this launches Edge itself, in real time, with no --dump-dom. The driver
reports through console.info; Edge writes console output to stderr as it
happens; this process reads those lines and timestamps them with its own clock.
The driver logs START immediately before clicking Run, so browser startup, page
parse and the price-data load are outside the measured interval.

The figure is CPU-unthrottled (FACTOR forced to 0 by _edge.build). To project a
real run, divide by the duty of the chosen CPU setting: Max 80%, High 40%,
Medium 20%, Low 10%.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / 'harness'))
import _edge  # noqa: E402

SIZES = [8, 16, 24, 32]
LINE = re.compile(r'HARNESS (START|DONE|FAIL)(.*)')


def one(n, timeout=1800):
    """Run one Pass 1 at `n` compare tickers. Returns (seconds, meta)."""
    html_path, js_path = _edge.build('throughput.js', out_prefix='_harness_throughput',
                                     config={'tickers': n, 'targets': ['QQQ']})
    prof = tempfile.mkdtemp(prefix='composer-harness-')
    url = 'file:///' + html_path.replace(os.sep, '/').replace(' ', '%20')
    argv = [_edge.edge_path(), '--headless=new', '--disable-gpu', '--no-sandbox',
            '--user-data-dir=' + prof, '--enable-logging=stderr', '--log-level=0',
            # A headless tab counts as hidden, and a hidden tab has its timers
            # clamped to roughly one per second. Pass 1 yields through setTimeout
            # between batches, so without these three flags a run does about one
            # batch per second and the measurement is of the clamp, not the code.
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-renderer-backgrounding',
            # A fresh --user-data-dir is NOT a clean browser: Edge still loads the
            # machine's extensions, which log constantly and open their own tabs.
            # That is noise in the stderr channel and competition for the CPU
            # being measured.
            '--disable-extensions', '--no-first-run', '--no-default-browser-check',
            url]

    proc = subprocess.Popen(argv, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    started, secs, meta = None, None, None
    deadline = time.time() + timeout
    try:
        for raw in iter(proc.stderr.readline, b''):
            now = time.time()
            m = LINE.search(raw.decode('utf-8', 'replace'))
            if m:
                tag, rest = m.group(1), m.group(2)
                if tag == 'START':
                    started = now
                elif tag == 'DONE':
                    secs = now - started
                    meta = json.loads(re.search(r'\{.*\}', rest).group(0))
                    break
                else:
                    raise SystemExit('driver failed at %d tickers:%s' % (n, rest))
            if now > deadline:
                raise SystemExit('timed out at %d tickers' % n)
    finally:
        proc.kill()
        proc.stderr.close()
        for f in (html_path, js_path):
            try:
                os.remove(f)
            except OSError:
                pass
        import shutil
        shutil.rmtree(prof, ignore_errors=True)

    if meta is None:
        raise SystemExit('no result at %d tickers (Edge exited before reporting)' % n)
    return secs, meta


def main(argv):
    sizes = [int(a) for a in argv] or SIZES
    rows = []
    for n in sizes:
        secs, d = one(n)
        d['secs'] = secs
        rows.append(d)
        print('tickers=%-3d specs=%-10s days=%-5d work=%-15s run=%7.2fs  %5.2f ns/unit'
              % (n, '{:,}'.format(d['specs']), d['days'], '{:,}'.format(d['work']),
                 secs, secs * 1e9 / d['work']))

    # Least squares on secs = intercept + slope * work. The intercept should now
    # be small, because startup is already outside the measured interval; a large
    # one means there is a per-run fixed cost worth naming (cache building).
    xs = [r['work'] for r in rows]
    ys = [r['secs'] for r in rows]
    k = len(xs)
    mx, my = sum(xs) / k, sum(ys) / k
    den = sum((x - mx) ** 2 for x in xs)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den if den else 0
    intercept = my - slope * mx

    print()
    print('fixed cost per run : %.2f s (cache building, render, anything not per-spec)'
          % intercept)
    print('marginal cost      : %.2f ns per spec-target-day (unthrottled)' % (slope * 1e9))
    print()
    print('Projected run time, one target over a 3,930-day sample:')
    for specs in (91232, 600000, 1200000, 2064072, 3936096):
        secs = intercept + slope * specs * 3930
        print('  %-10s %7.1fs unthrottled   %6.1f min at Medium (20%%)'
              % ('{:,}'.format(specs), secs, secs / 0.2 / 60))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
