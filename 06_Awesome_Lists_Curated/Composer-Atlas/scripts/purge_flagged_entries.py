#!/usr/bin/env python3
"""
purge_flagged_entries.py: Remove all data/database.json entries whose
`flag` matches one of the given levels, e.g. permanently-dead 404/422
symphonies. Reusable for any future cleanse along the same lines.

Safety invariant: a purged entry's symphony_url must already be present
in data/storage.csv (the durable URL backup) before it's removed from
database.json, so nothing is ever lost outright - it can always be
re-promoted into database.json later via sync_storage_to_database.py.
Aborts with no changes made if any purge candidate's URL is missing from
storage.csv.

After purging, regenerates every downstream artifact that derives from
database.json: database.js, database_summary.json/.js, and
"Full Database.xlsx" (via scripts/export_summary.py and
scripts/export_full_database_to_xlsx.py).

WARNING: do not run this while scripts/refresh_full_database.py is
running in the background - same clobbering risk described in that
script's docstring. Stop any running refresh first. "Full Database.xlsx"
must not be open in Excel or the xlsx re-export step will fail with a
PermissionError; close it and re-run scripts/export_full_database_to_
xlsx.py by hand if that happens.

Usage:
    python scripts/purge_flagged_entries.py excluded
    python scripts/purge_flagged_entries.py excluded retry caution
"""

import csv
import json
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = BASE_DIR / "data" / "database.json"
JS_PATH = BASE_DIR / "data" / "database.js"
STORAGE_PATH = BASE_DIR / "data" / "storage.csv"

VALID_LEVELS = {"excluded", "caution", "retry"}


def write_js(entries):
    comment = (
        "// Full database data - loaded as a script tag so database.html works with file:// protocol.\n"
        "// To update: run scripts/refresh_full_database.py\n"
    )
    JS_PATH.write_text(
        comment + f"window.DATABASE_DATA = {json.dumps(entries, indent=2, ensure_ascii=False)};\n",
        encoding="utf-8",
    )


def main():
    levels = set(sys.argv[1:])
    if not levels or not levels.issubset(VALID_LEVELS):
        print(f"Usage: python {Path(__file__).name} <level> [<level> ...]")
        print(f"Valid levels: {', '.join(sorted(VALID_LEVELS))}")
        sys.exit(1)

    entries = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    with open(STORAGE_PATH, encoding="utf-8", newline="") as f:
        storage_urls = {row["url"] for row in csv.DictReader(f)}

    to_purge = [e for e in entries if e.get("flag") in levels]
    missing = [e["symphony_url"] for e in to_purge if e.get("symphony_url") not in storage_urls]
    if missing:
        print(f"ABORTED: {len(missing)} purge candidate(s) are missing from storage.csv, no changes made.")
        print("Add them to storage.csv first (or investigate why they're absent):")
        for url in missing[:10]:
            print(f"  {url}")
        if len(missing) > 10:
            print(f"  ... and {len(missing) - 10} more")
        sys.exit(1)

    kept = [e for e in entries if e.get("flag") not in levels]
    JSON_PATH.write_text(json.dumps(kept, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_js(kept)
    print(f"Purged {len(to_purge)} entries with flag in {sorted(levels)}. Remaining: {len(kept)}")
    print("(all purged URLs were already present in storage.csv - nothing lost)")

    print("\nRegenerating downstream exports...")
    subprocess.run([sys.executable, str(BASE_DIR / "scripts" / "export_summary.py")], check=True)
    result = subprocess.run(
        [sys.executable, str(BASE_DIR / "scripts" / "export_full_database_to_xlsx.py")]
    )
    if result.returncode != 0:
        print(
            "\nNOTE: xlsx export failed (likely 'Full Database.xlsx' is open in Excel). "
            "Close it and re-run: python scripts/export_full_database_to_xlsx.py"
        )


if __name__ == "__main__":
    main()
