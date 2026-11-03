#!/usr/bin/env python3
"""
sync_database_to_storage.py: Append any data/database.json symphony whose URL is
missing from data/storage.csv.

This is the mirror of sync_storage_to_database.py, and the two are not
symmetrical in risk. That one promotes archived URLs into the approved database,
which is an approval decision and can resurrect symphonies that were purged as
dead. This one only widens the archive, which is what the archive is for.

Why it exists: storage.csv is meant to hold every symphony URL ever seen, alive
or dead, and to never lose one. database.json holds only the symphonies approved
for the site (docs/PRD.md Section 12). So database.json should always be a subset
of storage.csv, and it was not: five approved symphonies had no archived URL at
v1.25.4, four of them the same ones missing from database_summary.json until
v1.25.1. One cause behind both: the hand-run addition routes (the AddSymphony.csv
workflow, ad-hoc cluster corrections) write database.json and stop, updating
neither the archive before it nor the derived summary after it.

Run this after adding anything to database.json by hand. It is idempotent, and
scripts/check_database_keys.py gates the invariant either way, so forgetting is
caught at deploy time rather than discovered months later.

Keyed on symphony_id, not the URL string: Composer serves the same symphony under
more than one path (/details, /factsheet), so URL comparison reads a second URL
for a known symphony as a new one. That is what put a duplicate in database.json
before v1.25.2, and archiving a redundant second URL for a symphony already held
would be the same mistake in a file that never deletes anything.

New rows are appended at the end rather than merged into sorted position, which
is how the file has grown since it was seeded, and it keeps the diff to the lines
actually added.

WARNING: do not run this while scripts/refresh_full_database.py is running in the
background, for the usual reason (see that script's docstring). It only reads
database.json, so nothing here is clobbered, but it can read a half-written
checkpoint and archive a URL that the refresh is about to change.

Usage:
    python scripts/sync_database_to_storage.py
"""

import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_PATH = BASE_DIR / "data" / "storage.csv"
JSON_PATH = BASE_DIR / "data" / "database.json"

# storage.csv is written with CRLF, like every other committed text file in the
# repo on the machine that maintains it. Appending with "\n" here would leave a
# file with mixed endings and a diff on every subsequent line.
LINE_ENDING = "\r\n"


def extract_id(url):
    if not url or "/symphony/" not in url:
        return None
    return url.split("/symphony/")[1].split("/")[0]


def key_for(url):
    return extract_id(url) or url


def main():
    entries = json.loads(JSON_PATH.read_text(encoding="utf-8"))

    with open(STORAGE_PATH, encoding="utf-8", newline="") as f:
        archived = {key_for(row["url"]) for row in csv.DictReader(f)}

    missing = []
    seen = set(archived)
    for entry in entries:
        url = entry.get("symphony_url")
        if not url:
            continue
        key = entry.get("symphony_id") or key_for(url)
        if key in seen:
            continue
        seen.add(key)
        missing.append((entry.get("name"), url))

    print(
        f"{len(entries)} entries in database.json, "
        f"{len(archived)} symphonies in storage.csv, {len(missing)} to archive"
    )

    if not missing:
        print("Nothing to do: every approved symphony already has an archived URL.")
        return

    for name, url in missing:
        print(f"  + {url}  ({name or 'unnamed'})")

    with open(STORAGE_PATH, "a", encoding="utf-8", newline="") as f:
        for _, url in missing:
            f.write(url + LINE_ENDING)

    print(f"Appended {len(missing)} URL(s) to {STORAGE_PATH.name}")
    print("storage.csv is append-only: nothing is ever removed from it.")


if __name__ == "__main__":
    main()
