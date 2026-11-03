#!/usr/bin/env python3
"""
export_summary.py: Regenerate data/database_summary.json and
data/database_summary.js from data/database.json.

Performance Fix (V1.16, PRD.md Section 14): database.json is ~11MB.
The site's documented <500KB page-weight target (Section 10) is scoped
to the homepage specifically, not this page, but an 11MB fetch still
hurts load time and the Lighthouse/LCP targets that do apply broadly.

Two things drive the size down, neither is dropping fields alone (that
only saved ~26%, most of the weight isn't any single field, it's JSON
format overhead):

1. Columnar layout: one `fields` header array plus a `rows` array of
   plain value arrays, instead of repeating every field name as a key
   on every one of 6,488 objects. This alone is the biggest win.
2. Float rounding to 4 decimal places: these are percentages and
   ratios: 4 decimal places (e.g. 0.1234 = 12.34%) is far more
   precision than any UI ever displays.

Also drops fields unused by any list/filter/score view: cumulative_return,
mean, min, max, active_asset_nodes, total_costs, annualized_turnover,
herfindahl_index (see docs/PRD.md V1.13 for why each is excluded from
scoring; they're not displayed anywhere either, so they're dropped here
too).

Net effect measured on the live dataset: ~11.5MB -> ~2.3MB uncompressed,
~540KB gzipped (what a browser actually transfers; Cloudflare Pages
serves gzip/brotli automatically in production).

Run this after any run of scripts/refresh_full_database.py so the
summary file stays in sync with the full one.

Usage:
    python scripts/export_summary.py
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FULL_JSON_PATH = BASE_DIR / "data" / "database.json"
SUMMARY_JSON_PATH = BASE_DIR / "data" / "database_summary.json"
SUMMARY_JS_PATH = BASE_DIR / "data" / "database_summary.js"

FLOAT_DIGITS = 4

DROPPED_FIELDS = {
    "cumulative_return",
    "mean",
    "min",
    "max",
    "active_asset_nodes",
    "total_costs",
    "annualized_turnover",
    "herfindahl_index",
}


def round_floats(obj):
    if isinstance(obj, float):
        return round(obj, FLOAT_DIGITS)
    if isinstance(obj, dict):
        return {k: round_floats(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [round_floats(v) for v in obj]
    return obj


def collect_fields(entries):
    """Every field any entry carries, in first-seen order, minus the dropped ones.

    This used to read entries[0].keys() alone. Every entry happens to carry an
    identical key set today, so the two agree, but the old form would silently
    drop a field the day one was added to later entries without backfilling the
    first: the column would vanish from the summary with no error anywhere, and
    the site reads the summary, not database.json. First-seen order is preserved
    so the column layout stays byte-stable when nothing has changed.
    """
    fields = []
    seen = set()
    for entry in entries:
        for k in entry.keys():
            if k not in seen:
                seen.add(k)
                fields.append(k)
    return [k for k in fields if k not in DROPPED_FIELDS]


def main():
    entries = json.loads(FULL_JSON_PATH.read_text(encoding="utf-8"))

    fields = collect_fields(entries)
    rows = [round_floats([entry.get(f) for f in fields]) for entry in entries]
    payload = {"fields": fields, "rows": rows}

    SUMMARY_JSON_PATH.write_text(
        json.dumps(payload, separators=(",", ":"), ensure_ascii=False), encoding="utf-8"
    )
    print(f"Wrote {len(rows)} rows x {len(fields)} fields to {SUMMARY_JSON_PATH.name}")

    comment = (
        "// Slim, columnar summary of database.json for list/filter/score views (Performance Fix, V1.16).\n"
        "// Shape: { fields: [...], rows: [[...], ...] }, reconstruct objects client-side (see js/app.js or database.html).\n"
        "// To update: run scripts/export_summary.py after scripts/refresh_full_database.py.\n"
    )
    SUMMARY_JS_PATH.write_text(
        comment + f"window.DATABASE_SUMMARY_DATA = {json.dumps(payload, separators=(',', ':'), ensure_ascii=False)};\n",
        encoding="utf-8",
    )
    print(f"Wrote {SUMMARY_JS_PATH.name}")

    full_size = FULL_JSON_PATH.stat().st_size
    summary_size = SUMMARY_JSON_PATH.stat().st_size
    print(f"\nFull:    {full_size / 1024:.1f} KB")
    print(f"Summary: {summary_size / 1024:.1f} KB")
    print(f"Reduction: {(1 - summary_size / full_size) * 100:.1f}%")


if __name__ == "__main__":
    main()
