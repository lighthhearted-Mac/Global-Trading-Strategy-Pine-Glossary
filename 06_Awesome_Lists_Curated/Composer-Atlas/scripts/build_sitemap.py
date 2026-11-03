#!/usr/bin/env python3
"""
build_sitemap.py: Regenerate sitemap.xml from what the site actually serves.

Why this exists: robots.txt has advertised https://composeratlas.com/sitemap.xml
since the file was written, and until 2026-08-24 that URL 404'd on both hosts.
This script generates the real thing rather than leaving a hand-written file to
go stale the next time a page or a strategy is added.

What goes in:

1. Every top-level .html page that is genuinely indexable. The list is derived,
   not hardcoded, so a new page appears in the sitemap without anyone
   remembering this script exists. Three exclusion rules, each for a reason:
     - 404.html          error document, not content
     - _*.html           local mockups and harness pages, gitignored and listed
                         in .assetsignore
     - any page carrying <meta name="robots" content="noindex">
                         currently signal-lab.html, superseded by
                         signal-miner.html
2. One URL per curated strategy, as strategies.html?slug=<slug>. These are real
   distinct pages despite sharing one HTML file: strategies.html sets a per-slug
   <title> and meta description at render time (see strategies.html, the
   renderStrategy path), so each slug is its own document to a crawler that runs
   JS. The database is deliberately NOT enumerated this way; 6,669 query-string
   URLs of thin, near-identical rows is exactly the sort of thing that gets a
   sitemap ignored.

lastmod comes from the data where the data knows: each strategy carries its own
`last_updated`. For pages it comes from the file's last commit date via git,
and is simply omitted if git is unavailable or the file is untracked. An absent
lastmod is fine; a wrong one is worse than none.

changefreq and priority are deliberately not emitted. Google has stated it
ignores both, and every value anyone picks for them is a guess.

Canonical host is composeratlas.com (Cloudflare Pages). The GitHub Pages mirror
at azqato.github.io/composer/ is not given its own sitemap on purpose: it serves
the same content and should not compete for it.

Usage:
    python scripts/build_sitemap.py

Run it after adding a page, or after any run of scripts/update_metrics.py or
anything else that changes the curated set in data/strategies.json.
"""

import json
import re
import subprocess
from pathlib import Path
from xml.sax.saxutils import escape

BASE_DIR = Path(__file__).resolve().parent.parent
STRATEGIES_JSON_PATH = BASE_DIR / "data" / "strategies.json"
GUIDES_JSON_PATH = BASE_DIR / "data" / "guides.json"
SITEMAP_PATH = BASE_DIR / "sitemap.xml"

SITE_URL = "https://composeratlas.com"

EXCLUDED_PAGES = {"404.html"}

NOINDEX_RE = re.compile(
    r"""<meta\s[^>]*name=["']robots["'][^>]*content=["'][^"']*noindex""",
    re.IGNORECASE,
)

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def git_last_modified(path):
    """The file's last commit date as YYYY-MM-DD, or None if git cannot say."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", str(path.relative_to(BASE_DIR))],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    date = result.stdout.strip()
    return date if DATE_RE.match(date) else None


def is_indexable(path):
    if path.name in EXCLUDED_PAGES or path.name.startswith("_"):
        return False
    return not NOINDEX_RE.search(path.read_text(encoding="utf-8"))


def collect_pages():
    """Every indexable top-level page, index.html first and the rest sorted."""
    pages = sorted(p for p in BASE_DIR.glob("*.html") if is_indexable(p))
    pages.sort(key=lambda p: (p.name != "index.html", p.name))
    return pages


def collect_strategies():
    entries = json.loads(STRATEGIES_JSON_PATH.read_text(encoding="utf-8"))
    urls = []
    for entry in entries:
        slug = entry.get("slug")
        if not slug:
            print(f"  skipped (no slug): {entry.get('name', '?')}")
            continue
        # Hidden strategies are unlisted on the site, so the sitemap must not
        # advertise them either. The page itself still resolves by direct URL.
        if entry.get("hidden"):
            print(f"  skipped (hidden): {slug}")
            continue
        lastmod = entry.get("last_updated")
        if not (isinstance(lastmod, str) and DATE_RE.match(lastmod)):
            lastmod = None
        urls.append((f"{SITE_URL}/strategies?slug={slug}", lastmod))
    return urls


def collect_guides():
    """One URL per guide, as guides.html?slug=<slug>.

    Same reasoning as collect_strategies(): guides.html sets a per-slug title
    and meta description, so each slug is a distinct document to a crawler that
    runs JavaScript. These are long-form pages and the whole point of them is
    being findable.

    NOTE, and it is a real gap rather than a decision: glossary.html?slug=
    pages are NOT in this sitemap and never have been. There are 28 of them,
    built the same way. Adding them is a separate change because it would alter
    the sitemap for content that has been live for months, and that deserves
    its own verification rather than riding along with a new section.
    """
    if not GUIDES_JSON_PATH.exists():
        print("  skipped: data/guides.json not found")
        return []
    entries = json.loads(GUIDES_JSON_PATH.read_text(encoding="utf-8"))
    urls = []
    for entry in entries:
        slug = entry.get("slug")
        if not slug:
            print(f"  skipped (no slug): {entry.get('title', '?')}")
            continue
        lastmod = entry.get("last_updated")
        if not (isinstance(lastmod, str) and DATE_RE.match(lastmod)):
            lastmod = None
        urls.append((f"{SITE_URL}/guides?slug={slug}", lastmod))
    return urls


def build_entry(loc, lastmod):
    lines = ["  <url>", f"    <loc>{escape(loc)}</loc>"]
    if lastmod:
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
    lines.append("  </url>")
    return "\n".join(lines)


def main():
    urls = []

    for page in collect_pages():
        # index.html is served at the bare root. Every other page is listed
        # without ".html": Cloudflare's default asset HTML handling answers
        # /page.html with a 307 to /page, and a sitemap must list the final URL
        # or Search Console reports each one as "Page with redirect" (found
        # 2026-10-18 while setting up Search Console).
        loc = SITE_URL + "/" + ("" if page.name == "index.html" else page.stem)
        urls.append((loc, git_last_modified(page)))
    page_count = len(urls)

    urls.extend(collect_strategies())
    strategy_count = len(urls) - page_count

    urls.extend(collect_guides())
    guide_count = len(urls) - page_count - strategy_count

    body = "\n".join(build_entry(loc, lastmod) for loc, lastmod in urls)
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n"
        "</urlset>\n"
    )
    SITEMAP_PATH.write_text(xml, encoding="utf-8")

    print(f"Wrote {len(urls)} URLs to {SITEMAP_PATH.name}")
    print(f"  {page_count} page(s)")
    print(f"  {strategy_count} strategy page(s)")
    print(f"  {guide_count} guide page(s)")
    print(f"  {SITEMAP_PATH.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
