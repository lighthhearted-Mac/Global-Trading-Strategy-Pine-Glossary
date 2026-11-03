#!/usr/bin/env python3
"""
dedupe_symphonies.py: Flags near-identical name-cluster duplicates in
data/database.json with flag="duplicate" (V1.14 Part A, docs/PRD.md
Section 14). Nothing is deleted - duplicate rows stay in the database,
filterable via the "Duplicates" toggle in database.html.

Pipeline:
1. Candidate pool: entries with flag == null only (excludes already-
   excluded/caution/retry/duplicate rows from consideration this pass).
2. Clustering (candidate-finding only, never the actual decision):
   normalize names - strip "TESTPORT #N:" prefix, leading "Copy of "
   chains, and "(Invest Copy)"/"(Buy Copy)" suffixes - and group rows
   sharing what's left. Run scripts/flag_name_noise.py first so a
   TESTPORT-prefixed row is never in the candidate pool to begin with;
   this script does not special-case TESTPORT names in its own logic.
3. Primary identity check: fetch each candidate's logic tree via
   GET /symphonies/{id}/score?score_version=v1 (one lightweight GET,
   no backtest execution). Strip every "id" field (root + nested nodes
   - Composer assigns a unique UUID to every node, even on literal
   clones) and the root "name" field, then hash the canonical JSON.
   Matching hashes within a cluster = genuinely the same strategy logic.
4. Fallback (only when the logic-tree fetch fails for a row): compare
   metrics among same-refresh_date rows only. "Identical" = within 3
   percentage points absolute for annualized_rate_of_return/
   max_drawdown/trailing_one_year_return, or 3% relative for
   cumulative_return/sharpe_ratio/calmar_ratio/backtest_days. If a
   fetch-failed row's refresh_date doesn't match any group's, it's left
   ungrouped (skipped) rather than forcing a fresh refresh mid-run.
5. Tiebreak within each identical sub-group (2+ members): keep the row
   with the longest oos_date (smallest/oldest calendar date - a null
   oos_date is treated as worst). Tie -> lexicographically earliest
   symphony_id. No name-based priority (confirmed decision - the
   symphony_id sort is used exactly as-is even when it produces a
   counterintuitive keeper).
6. Every other row in the sub-group gets flag="duplicate",
   error="Duplicate of <kept symphony_id>".

Rate-limited to 1 call per 2 seconds (same proven-safe throttle as
refresh_full_database.py) against the logic-tree endpoint. Checkpoints
every CHECKPOINT_EVERY clusters. Safe to re-run: only touches rows
whose flag is currently null.

WARNING: do not run while scripts/refresh_full_database.py is active in
the background - same clobbering risk as other scripts that write
database.json.

MANUAL-ONLY, NEVER AUTOMATE: do not add this to any GitHub Actions
workflow or other CI/scheduled job. It makes ~1 live API call per
candidate row (hundreds per run) against Composer's unauthenticated
API and can take 20-30+ minutes; running it unattended on a schedule
risks silently hammering that API far more often than a human would
choose to, with no one watching for rate-limit or correctness issues.
The existing deploy workflow (.github/workflows/) already excludes
scripts/ entirely, and update-metrics.yml only ever runs
update_metrics.py (the curated 25 strategies, a different, lighter
pipeline) - keep it that way. Same rule applies to
scripts/flag_name_noise.py and every other full-database maintenance
script in this directory; none of them are wired into CI today and
none of them should be.

Usage:
    python scripts/dedupe_symphonies.py [LIMIT]

    LIMIT: optional int, max number of candidate clusters to process
    this run (default: all).
"""

import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = BASE_DIR / "data" / "database.json"
JS_PATH = BASE_DIR / "data" / "database.js"

API_BASE = "https://api.composer.trade"
UA = "Mozilla/5.0 (compatible; composer-metrics-updater/1.0)"
API_CALL_DELAY_SECONDS = 2
CHECKPOINT_EVERY = 10

TESTPORT_RE = re.compile(r"^(TESTPORT\s*#\d+(\.\d+)?:\s*)", re.I)
COPY_OF_RE = re.compile(r"^(Copy of\s*)+", re.I)
SUFFIX_RE = re.compile(r"\s*\((Invest Copy|Buy Copy)\)\s*", re.I)
WS_RE = re.compile(r"\s+")

PCT_FIELDS = ["annualized_rate_of_return", "max_drawdown", "trailing_one_year_return"]
RATIO_FIELDS = ["cumulative_return", "sharpe_ratio", "calmar_ratio", "backtest_days"]
PCT_TOLERANCE = 0.03
REL_TOLERANCE = 0.03


def normalize_name(name):
    if not name:
        return None
    n = TESTPORT_RE.sub("", name)
    n = COPY_OF_RE.sub("", n)
    n = SUFFIX_RE.sub(" ", n)
    n = WS_RE.sub(" ", n).strip().lower()
    return n or None


def strip_ids(obj):
    if isinstance(obj, dict):
        return {k: strip_ids(v) for k, v in obj.items() if k != "id"}
    if isinstance(obj, list):
        return [strip_ids(x) for x in obj]
    return obj


def fetch_tree_hash(symphony_id):
    import hashlib
    url = f"{API_BASE}/api/v0.1/symphonies/{symphony_id}/score?score_version=v1"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as resp:
        tree = json.loads(resp.read().decode("utf-8"))
    tree.pop("name", None)
    stripped = strip_ids(tree)
    canon = json.dumps(stripped, sort_keys=True)
    return hashlib.sha256(canon.encode()).hexdigest()


def metrics_close(a, b):
    for f in PCT_FIELDS:
        va, vb = a.get(f), b.get(f)
        if not isinstance(va, (int, float)) or not isinstance(vb, (int, float)):
            return False
        if abs(va - vb) > PCT_TOLERANCE:
            return False
    for f in RATIO_FIELDS:
        va, vb = a.get(f), b.get(f)
        if not isinstance(va, (int, float)) or not isinstance(vb, (int, float)):
            return False
        denom = max(abs(va), abs(vb)) or 1
        if abs(va - vb) / denom > REL_TOLERANCE:
            return False
    return True


def oos_sort_key(entry):
    v = entry.get("oos_date")
    try:
        d = date.fromisoformat(v) if v else date.max
    except ValueError:
        d = date.max
    return (d, entry["symphony_id"])


def build_clusters(entries):
    clusters = {}
    for e in entries:
        if not e.get("symphony_id") or e.get("flag") is not None:
            continue
        norm = normalize_name(e.get("name"))
        if not norm:
            continue
        clusters.setdefault(norm, []).append(e)
    return {k: v for k, v in clusters.items() if len(v) >= 2}


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
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None

    entries = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    clusters = build_clusters(entries)
    cluster_items = list(clusters.items())
    if limit:
        cluster_items = cluster_items[:limit]

    total_rows = sum(len(v) for _, v in cluster_items)
    print(f"Processing {len(cluster_items)} candidate clusters ({total_rows} rows)...")

    flagged_total = 0
    fetch_failures = 0
    call_count = 0

    try:
        for ci, (norm, members) in enumerate(cluster_items):
            # subgroup by structural hash (or metrics fallback)
            subgroups = []  # list of (hash_or_None, [members])
            for m in members:
                if call_count > 0:
                    time.sleep(API_CALL_DELAY_SECONDS)
                call_count += 1
                try:
                    h = fetch_tree_hash(m["symphony_id"])
                    m["_hash"] = h
                except Exception as e:
                    fetch_failures += 1
                    m["_hash"] = None
                    print(f"  WARNING: logic-tree fetch failed for {m['symphony_id']} ({m.get('name')!r}): {e}")

            hashed = [m for m in members if m.get("_hash")]
            unhashed = [m for m in members if not m.get("_hash")]

            by_hash = {}
            for m in hashed:
                by_hash.setdefault(m["_hash"], []).append(m)

            # fallback: try to fit unhashed rows into an existing hash-group via metrics
            for m in unhashed:
                placed = False
                for group in by_hash.values():
                    rep = group[0]
                    if rep.get("refresh_date") == m.get("refresh_date") and metrics_close(rep, m):
                        group.append(m)
                        placed = True
                        break
                if not placed:
                    pass  # left ungrouped, no dedup for this row this pass

            for m in members:
                m.pop("_hash", None)

            for group in by_hash.values():
                if len(group) < 2:
                    continue
                keeper = min(group, key=oos_sort_key)
                for loser in group:
                    if loser is keeper:
                        continue
                    loser["flag"] = "duplicate"
                    loser["error"] = f"Duplicate of {keeper['symphony_id']}"
                    flagged_total += 1
                print(f"  cluster {ci+1}: kept {keeper['symphony_id']} ({keeper.get('name')!r}), "
                      f"flagged {len(group)-1} duplicate(s)")

            if (ci + 1) % CHECKPOINT_EVERY == 0:
                JSON_PATH.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
                print(f"  -- checkpoint saved at {ci + 1}/{len(cluster_items)} clusters --")
    finally:
        JSON_PATH.write_text(json.dumps(entries, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        write_js(entries)
        print(f"\nSaved. Flagged {flagged_total} duplicates. Logic-tree fetch failures: {fetch_failures}")


if __name__ == "__main__":
    main()
