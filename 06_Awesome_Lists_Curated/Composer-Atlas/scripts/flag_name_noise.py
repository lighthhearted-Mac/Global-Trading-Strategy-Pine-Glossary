#!/usr/bin/env python3
"""
flag_name_noise.py: Flags non-strategy noise rows in data/database.json
by name pattern - TESTPORT # test ports and [Work]/STILL BUILDING
work-in-progress markers (V1.14 Part A, docs/PRD.md Section 14).

Reuses the existing "excluded" flag level rather than introducing a new
one: these rows aren't real strategies and shouldn't appear in default
views, the same practical outcome as a permanently-failing 404/422 row,
even though the reason is different (name pattern vs. API failure).
`error` records which pattern matched, for traceability.

Run before scripts/dedupe_symphonies.py: flagging these first removes
them from the dedup candidate pool entirely, so a TESTPORT-prefixed row
can never win a dedup tiebreak and become the sole surviving copy of a
strategy. This is a sequencing choice, not a tiebreak special-case.

Does not delete anything. Safe to re-run: only touches rows whose flag
is currently null (won't overwrite an existing excluded/caution/retry/
duplicate flag from a different cause).

MANUAL-ONLY, NEVER AUTOMATE: do not add this to any GitHub Actions
workflow or other CI/scheduled job, for the same reason as
scripts/dedupe_symphonies.py (see that script's docstring) - none of
the full-database maintenance scripts in this directory are wired into
CI today, and none of them should be. This particular script makes no
API calls itself, but it directly feeds the dedup pipeline that does.

Usage:
    python scripts/flag_name_noise.py
"""

import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = BASE_DIR / "data" / "database.json"
JS_PATH = BASE_DIR / "data" / "database.js"

TESTPORT_RE = re.compile(r"TESTPORT\s*#\d+", re.I)
WIP_RE = re.compile(r"\[Work\]|STILL BUILDING", re.I)


def classify(name):
    if not name:
        return None
    if TESTPORT_RE.search(name):
        return "TESTPORT # test port"
    if WIP_RE.search(name):
        return "[Work]/STILL BUILDING marker"
    return None


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
    entries = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    flagged = 0
    for e in entries:
        if e.get("flag") is not None:
            continue
        reason = classify(e.get("name"))
        if reason:
            e["flag"] = "excluded"
            e["error"] = f"Non-strategy noise: {reason}"
            flagged += 1

    JSON_PATH.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_js(entries)
    print(f"Flagged {flagged} name-pattern noise rows as excluded")


if __name__ == "__main__":
    main()
