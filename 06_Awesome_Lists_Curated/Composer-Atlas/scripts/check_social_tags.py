# -*- coding: utf-8 -*-
"""Read-only compliance check for Open Graph and Twitter Card tags.

NOT A DEPLOY GATE. Whether it becomes one is PRD Section 25, open question 27,
and is explicitly not a decision for whoever writes the checker. The precedent
is the V1.20 item 10 validator, written and left manual pending an owner ruling.

What it asserts, per docs/PRD.md Section 27:
  - every page in sitemap.xml carries all six required tags
  - og:title at most 70 characters, flagged over the 60 target
  - og:description at most 200, flagged over the 150 target
  - og:site_name at most 20
  - og:title does not repeat og:site_name
  - og:url absolute, https, and unique across the site
  - og:url and <link rel="canonical"> both equal the page's sitemap URL
  - og:* uses property=, twitter:* uses name=
  - with no og:image, twitter:card is "summary"
  - the tag block sits above any inline <style>

WHAT IT CANNOT CHECK, and this is the important half: the no-drifting-numbers
rule. Prose cannot be machine-separated into measurements and constants. "10-day
RSI" is a constant of the indicator and is fine; "the 20 ETF tickers" is a
measurement read from a data file and goes stale silently. That rule is enforced
at review, which is why Section 27 writes it out at length rather than encoding
it here. A passing run of this script means the cheap half of the policy holds.
"""
from __future__ import print_function

import io
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TITLE_TARGET, TITLE_MAX = 60, 70
DESC_TARGET, DESC_MAX = 150, 200
SITE_MAX = 20

REQUIRED = ['og:type', 'og:site_name', 'og:url', 'og:title', 'og:description']


def sitemap_pages():
    """The pages in scope: every sitemap entry that is a real HTML file.

    Query-string entries are strategy pages, all resolving to strategies.html
    and rendered in JavaScript, so they share one card no matter what is
    written. That is recorded as out of scope in Section 14, V2.5.
    """
    src = io.open(os.path.join(REPO, 'sitemap.xml'), encoding='utf-8').read()
    out = []
    for loc in re.findall(r'<loc>([^<]+)</loc>', src):
        path = loc.split('composeratlas.com/', 1)[-1]
        if '?' in path:
            continue
        # sitemap URLs are extensionless (Cloudflare 307s /page.html to /page),
        # so /about is about.html. A page that cannot be found is an error, not
        # a skip: silently skipping is how this check once passed on nothing.
        fn = (path + '.html') if path else 'index.html'
        if not os.path.exists(os.path.join(REPO, fn)):
            raise SystemExit('sitemap entry %r has no file %s' % (loc, fn))
        out.append((fn, loc))
    return out


def tags_in(src):
    """Every meta tag, keyed by property= or name=, with which attribute was used."""
    found = {}
    for m in re.finditer(r'<meta\s+([^>]*?)/?>', src, re.I):
        attrs = m.group(1)
        key = re.search(r'\b(property|name)\s*=\s*"([^"]+)"', attrs, re.I)
        val = re.search(r'\bcontent\s*=\s*"([^"]*)"', attrs, re.I)
        if not key or not val:
            continue
        found[key.group(2).lower()] = (key.group(1).lower(), val.group(1), m.start())
    return found


def main():
    fails, warns = [], []
    seen_urls = {}
    pages = sitemap_pages()
    if not pages:
        print('FAIL: no pages resolved from sitemap.xml')
        return 1

    for fn, loc in pages:
        src = io.open(os.path.join(REPO, fn), encoding='utf-8').read()
        t = tags_in(src)

        def bad(msg):
            fails.append('%s: %s' % (fn, msg))

        for key in REQUIRED:
            if key not in t:
                bad('missing %s' % key)
        if 'twitter:card' not in t:
            bad('missing twitter:card')

        # og:* takes property=, twitter:* takes name=. A tag written the wrong
        # way validates as HTML, renders nothing, and reports no error.
        for key, (attr, _v, _p) in t.items():
            if key.startswith('og:') and attr != 'property':
                bad('%s uses %s=, must be property=' % (key, attr))
            if key.startswith('twitter:') and attr != 'name':
                bad('%s uses %s=, must be name=' % (key, attr))

        title = t.get('og:title', (None, '', 0))[1]
        desc = t.get('og:description', (None, '', 0))[1]
        site = t.get('og:site_name', (None, '', 0))[1]

        if len(title) > TITLE_MAX:
            bad('og:title is %d chars, over the %d ceiling' % (len(title), TITLE_MAX))
        elif len(title) > TITLE_TARGET:
            warns.append('%s: og:title is %d chars, over the %d target'
                         % (fn, len(title), TITLE_TARGET))
        if len(desc) > DESC_MAX:
            bad('og:description is %d chars, over the %d ceiling' % (len(desc), DESC_MAX))
        elif len(desc) > DESC_TARGET:
            warns.append('%s: og:description is %d chars, over the %d target'
                         % (fn, len(desc), DESC_TARGET))
        if len(site) > SITE_MAX:
            bad('og:site_name is %d chars, over %d' % (len(site), SITE_MAX))
        if site and site.lower() in title.lower():
            bad('og:title repeats og:site_name (%r)' % site)

        url = t.get('og:url', (None, '', 0))[1]
        if url and not url.startswith('https://'):
            bad('og:url is not absolute https: %r' % url)
        if url in seen_urls:
            bad('og:url duplicates %s (a copied head block)' % seen_urls[url])
        elif url:
            seen_urls[url] = fn
        if url and url != loc:
            bad('og:url %r does not match its sitemap entry %r' % (url, loc))
        canon = re.search(r'<link\s+rel="canonical"\s+href="([^"]*)"', src)
        if not canon:
            bad('no <link rel="canonical">')
        elif canon.group(1) != loc:
            bad('canonical %r does not match its sitemap entry %r' % (canon.group(1), loc))

        # Text-only policy: no image, so the card must be the small one. A
        # summary_large_image with no image renders as a blank slab.
        card = t.get('twitter:card', (None, '', 0))[1]
        if 'og:image' not in t and card != 'summary':
            bad('no og:image, so twitter:card must be "summary", got %r' % card)

        # Placement. Some scrapers read only the first few KB, and overfit.html
        # carries roughly seventy lines of inline CSS in its head.
        style = src.find('<style')
        if style != -1 and 'og:title' in t and t['og:title'][2] > style:
            bad('og:title sits below the inline <style>, inside the window a '
                'scraper may never read')

        # One description per page: the meta description and og:description
        # must not disagree, or two different sentences describe one page.
        m = re.search(r'<meta name="description" content="([^"]*)"', src)
        if m and desc and m.group(1) != desc:
            bad('meta description and og:description differ')

    for w in warns:
        print('WARN: ' + w)
    for f in fails:
        print('FAIL: ' + f)
    print('%s: %d pages checked, %d failures, %d warnings'
          % ('FAIL' if fails else 'PASS', len(pages), len(fails), len(warns)))
    print('note: the no-drifting-numbers rule is NOT checked here and cannot be; '
          'it is enforced at review (PRD Section 27).')
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
