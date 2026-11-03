#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lint what Cloudflare actually serves, rather than what git says was pushed.

Cloudflare Pages deploys independently of the GitHub Actions gate, and the
build command cannot be changed from here, so "pushed" and "live" are
genuinely different states. This has been checked by hand more than once; it
is twenty lines and belongs in the deploy runbook.

    python scripts/check_live.py                  # check every page
    python scripts/check_live.py signal-miner     # check one

For each page it:
  1. fetches the live clean URL,
  2. compares it byte-for-byte against the committed file,
  3. checks the markers that must be present and the ones that must be absent.

Exits non-zero on any mismatch, so it can gate a release.
"""
import io
import re
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BASE = 'https://composeratlas.com'

# page slug -> (local file, [markers that MUST be present], [markers that MUST NOT be])
#
# Present-markers should name the newest shipped behaviour, so a stale deploy
# is caught even when the byte-compare is confused by a trailing newline.
# Absent-markers should name things a previous version had and this one must
# not, which is what catches a deploy that rolled backwards.
PAGES = {
    'signal-miner': (
        'signal-miner.html',
        [
            'SIGNAL_WARN_CAP = 1200000',              # v1.24.2 thresholds
            'SIGNAL_WARN_SOFT',
            'function windowInfo(syms, warm)',        # v1.24.1 warm-up
            'lost to warm-up',
            'indicator warm-up so every row',
            'busyTotal',                              # v1.24.3 measured duty
            "same: true",                             # v1.24.0 price-scale families
            'function pushCmpSpecs(sp, fi, nT, windows, sameOnly)',
            '23 nanoseconds per unit of work',        # v1.24.4 measured throughput
            'SETTINGS_STORE_KEY',                     # v1.24.7 settings persistence
            'const DEFAULT_SETTINGS',
            "'sl-cpu': 'high'",                       # the new default CPU load
            'Max Drawdown floor (%)',                 # unsigned percent units
        ],
        [
            'SIGNAL_WARN_CAP = 100000',               # the old threshold
            'const COMPOSER_FN',                      # deleted in v1.23.0
            'roughly 4.5',                            # the throughput figure v1.24.4 corrected
            'value="-0.8"',                           # the old signed drawdown input
        ],
    ),
    'index': ('index.html', ['Composer Atlas'], []),
    'strategies': ('strategies.html', [], []),
    'database': ('database.html', [], []),
    'glossary': ('glossary.html', [], []),
    'rsi': ('rsi.html', [], []),
    'converter': ('converter.html', [], []),
    'nodes': ('nodes.html', ['Count nodes'], []),
    'k1': ('k1.html', ['K1 Lookup'], []),
    'about': ('about.html', [], []),
}


BEACON_RE = re.compile(
    '<script[^>]*static[.]cloudflareinsights[.]com[^>]*></script>[\\n]?', re.I)


def strip_injected(text):
    """Remove anything Cloudflare adds at serve time.

    Returns (text, bytes_removed). This is deliberately a short, explicit
    list rather than a fuzzy comparison: the whole point of this script is
    that an unexplained difference between committed and live is a problem.
    """
    out = BEACON_RE.sub('', text)
    return out, len(text) - len(out)


def fetch(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'composer-atlas-check-live/1.0',
        'Cache-Control': 'no-cache',
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def check(slug):
    local_name, must, must_not = PAGES[slug]
    url = BASE + ('/' if slug == 'index' else '/' + slug)
    local_path = REPO / local_name

    try:
        live_bytes = fetch(url)
    except Exception as e:                                   # noqa: BLE001
        print('  FAIL %-14s could not fetch %s: %s' % (slug, url, e))
        return False

    live = live_bytes.decode('utf-8', 'replace')
    committed = io.open(local_path, encoding='utf-8').read()

    ok = True
    # Normalise line endings before comparing: the working copy is CRLF on
    # Windows and what Cloudflare serves is whatever git stored.
    a = committed.replace('\r\n', '\n')
    b = live.replace('\r\n', '\n')

    # Cloudflare injects its Web Analytics beacon at serve time, so every live
    # page is legitimately ~359 bytes longer than the committed one. Strip it
    # before comparing, rather than reporting a diff on every page forever.
    # It is still reported as a note, because the day it stops appearing (or
    # something else starts being injected) is worth knowing.
    b, injected = strip_injected(b)
    if injected:
        print('  note %-14s Cloudflare beacon injected at serve time (+%d bytes)'
              % (slug, injected))

    if a != b:
        print('  DIFF %-14s live is %d bytes, committed is %d bytes '
              '(after stripping injections)' % (slug, len(b), len(a)))
        ok = False

    for m in must:
        if m not in live:
            print('  FAIL %-14s missing marker: %s' % (slug, m))
            ok = False
    for m in must_not:
        if m in live:
            print('  FAIL %-14s stale marker present: %s' % (slug, m))
            ok = False

    if ok:
        print('  ok   %-14s %s' % (slug, url))
    return ok


def main():
    which = sys.argv[1:] or sorted(PAGES)
    for s in which:
        if s not in PAGES:
            raise SystemExit('unknown page %r; pick from %s' % (s, ', '.join(sorted(PAGES))))
    print('checking %s' % BASE)
    results = [check(s) for s in which]
    bad = results.count(False)
    print('%d checked, %d failed' % (len(results), bad))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
