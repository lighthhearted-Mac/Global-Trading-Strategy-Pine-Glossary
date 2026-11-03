#!/usr/bin/env python3
"""
id_to_url.py: Convert Composer symphony ids to their canonical URL, and back.

Two files disagree on what a symphony's key is, on purpose (docs/PRD.md
Section 14): data/database.json is keyed on `symphony_id`, while
data/storage.csv is keyed on `url`. Anything that moves symphonies between
the two, or ingests a bare list of ids (the AddSymphony.csv workflow), has
to convert one to the other, and the URL form matters: Composer serves the
same symphony under more than one path (`/details`, `/factsheet`), and
storage.csv has always stored the `/details` form. Standardizing that here
keeps every ingest route emitting the same string, so a symphony never
lands in storage twice under two different URLs.

Reusable as a module (`from id_to_url import id_to_url, url_to_id`) or from
the command line.

Usage:
    python scripts/id_to_url.py ID [ID ...]        # ids  -> URLs
    python scripts/id_to_url.py --reverse URL ...   # URLs -> ids
    python scripts/id_to_url.py --view factsheet ID # /factsheet instead of /details
    ... | python scripts/id_to_url.py               # ids from stdin, one per line

Ids are 20-character alphanumeric strings; anything else is reported to
stderr and skipped rather than silently emitting a malformed URL.
"""

import argparse
import re
import sys

URL_TEMPLATE = "https://app.composer.trade/symphony/{id}/{view}"
ID_RE = re.compile(r"^[A-Za-z0-9]{20}$")
URL_ID_RE = re.compile(r"/symphony/([A-Za-z0-9]{20})")


def id_to_url(symphony_id, view="details"):
    """Return the canonical Composer URL for a symphony id (default /details view)."""
    symphony_id = (symphony_id or "").strip()
    if not ID_RE.match(symphony_id):
        raise ValueError(f"not a valid symphony id: {symphony_id!r}")
    return URL_TEMPLATE.format(id=symphony_id, view=view)


def url_to_id(url):
    """Extract the symphony id from a Composer URL, or None if there isn't one."""
    if not url:
        return None
    match = URL_ID_RE.search(url)
    return match.group(1) if match else None


def _read_inputs(args):
    if args.values:
        return args.values
    return [line.strip() for line in sys.stdin if line.strip()]


def main():
    parser = argparse.ArgumentParser(description="Convert Composer symphony ids <-> URLs.")
    parser.add_argument("values", nargs="*", help="ids (or URLs with --reverse); reads stdin if omitted")
    parser.add_argument("--reverse", action="store_true", help="convert URLs to ids instead")
    parser.add_argument("--view", default="details", help="URL view segment (default: details)")
    args = parser.parse_args()

    ok = bad = 0
    for value in _read_inputs(args):
        if args.reverse:
            result = url_to_id(value)
            if result is None:
                print(f"no id found in: {value}", file=sys.stderr)
                bad += 1
                continue
        else:
            try:
                result = id_to_url(value, view=args.view)
            except ValueError as e:
                print(e, file=sys.stderr)
                bad += 1
                continue
        print(result)
        ok += 1

    if bad:
        print(f"({ok} converted, {bad} skipped)", file=sys.stderr)
    return 1 if bad and not ok else 0


if __name__ == "__main__":
    sys.exit(main())
