#!/usr/bin/env python3
"""
sync_storage_to_database.py: Add any URL present in data/storage.csv but
missing from data/database.json as a new, unrefreshed entry.

data/storage.csv is the durable backup: URLs get pasted into it whenever
a symphony is discussed, referenced, or added anywhere on the site,
independent of whether it's ever made it into the database. This script
is the other direction, promoting storage.csv entries into database.json
so they actually get picked up by scripts/refresh_full_database.py.

New entries are added with every field null except name (also null,
matching how originally-unscraped rows look), symphony_url, and
symphony_id, so they're indistinguishable from any other not-yet-
refreshed row and will be picked up by the next refresh run.

Safe to re-run: symphonies already in database.json are skipped. The skip is
keyed on symphony_id, not on the URL string, because Composer serves the same
symphony under more than one path (/details, /factsheet). Until v1.25.2 this
check compared URLs, which let a second URL for an existing symphony through as
a new row; scripts/check_database_keys.py now gates that invariant on the
artifact itself.

WARNING: do not run this while scripts/refresh_full_database.py is running
in the background. That script loads database.json into memory once at
startup and periodically overwrites the whole file with that in-memory
copy; running this script in the meantime gets silently clobbered on the
refresh script's next checkpoint. Stop any running refresh first.

Usage:
    python scripts/sync_storage_to_database.py
"""

import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_PATH = BASE_DIR / "data" / "storage.csv"
JSON_PATH = BASE_DIR / "data" / "database.json"
JS_PATH = BASE_DIR / "data" / "database.js"


def extract_id(url):
    if not url or "/symphony/" not in url:
        return None
    return url.split("/symphony/")[1].split("/")[0]


def main():
    with open(STORAGE_PATH, encoding="utf-8", newline="") as f:
        storage_urls = [row["url"] for row in csv.DictReader(f)]

    entries = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    template_keys = list(entries[0].keys())

    # Key on symphony_id, not on the URL string. Composer serves the same
    # symphony under more than one path (/details and /factsheet at least), so
    # a URL-keyed check reads a second URL for a symphony already in the
    # database as a brand new symphony. That is exactly how chkrQ6BnXCw31n7OIEaK
    # ended up in database.json twice; see v1.25.2 in docs/PATCHNOTES.md.
    # Falls back to the URL only when no id can be parsed, which should not
    # happen for a real Composer link and is better than dropping the row.
    def key_for(url):
        return extract_id(url) or url

    seen = {key_for(e["symphony_url"]) for e in entries if e.get("symphony_url")}
    seen.update(e["symphony_id"] for e in entries if e.get("symphony_id"))
    already = len(seen)

    new_urls = []
    for url in storage_urls:
        key = key_for(url)
        if key in seen:
            continue
        seen.add(key)          # so storage.csv listing the same symphony twice adds it once
        new_urls.append(url)

    print(f"{len(storage_urls)} URLs in storage.csv, {already} symphonies already in database.json, {len(new_urls)} new")

    for url in new_urls:
        entry = {k: None for k in template_keys}
        entry["symphony_url"] = url
        entry["symphony_id"] = extract_id(url)
        entries.append(entry)

    JSON_PATH.write_text(
        json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Wrote {len(entries)} total entries to {JSON_PATH.name} (+{len(new_urls)})")

    comment = (
        "// Full database data - loaded as a script tag so database.html works with file:// protocol.\n"
        "// To update: run scripts/refresh_full_database.py\n"
    )
    JS_PATH.write_text(
        comment + f"window.DATABASE_DATA = {json.dumps(entries, indent=2, ensure_ascii=False)};\n",
        encoding="utf-8",
    )
    print(f"Wrote {JS_PATH.name}")


if __name__ == "__main__":
    main()
