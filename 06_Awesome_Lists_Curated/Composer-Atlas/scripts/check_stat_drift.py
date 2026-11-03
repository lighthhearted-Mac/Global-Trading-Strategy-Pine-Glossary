#!/usr/bin/env python3
"""
check_stat_drift.py: find performance statistics quoted in prose that no longer
match the live metrics.

Why this exists. `scripts/update_metrics.py` refreshes every strategy's metrics
nightly and **cannot rewrite prose**. Any figure duplicated into a written field
is therefore correct only on the day it was typed, and it degrades silently: the
page still renders, still returns 200, and still reads fluently while telling the
reader something false.

This is not hypothetical. When this script was first written it found **88 stale
figures across 29 of 31 strategies** in `ai_summary` alone, including
`s90-half-low-catch` advertising a Calmar of 24.81 against a live 11.69 and a
30% max drawdown against a live 41%: a strategy overstated in both directions at
once, on the same page that displays the correct numbers in a table.

The durable fix is not to re-type the numbers. It is to keep bare statistics out
of prose entirely and let the metrics table own them, which is the rule V1.20
item 10 applied to `risk_profile`. This script is how that rule stays enforced,
and how any figure that does creep back in gets caught while it is still true.

**NOT wired into .github/workflows/deploy.yml.** Whether it should be a gate is
an open question for the owner, recorded in docs/PRD.md alongside the same
question for check_risk_profiles.py.

Usage:
    python scripts/check_stat_drift.py          # report drift
    python scripts/check_stat_drift.py --all    # also list claims that match

Exit 0 when no claim has drifted, 1 otherwise.
"""

import io
import json
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STRATEGIES = BASE_DIR / "data" / "strategies.json"

# Fields that are prose. Everything else in a strategy record is either a metric,
# an identifier, or structured data that is regenerated rather than written.
PROSE_FIELDS = [
    "ai_summary",
    "description",
    "how_it_works",
    "author_note",
    "risk_profile",
    "signals",
    "tldr",
    "regimes",
    "assumptions",
]

# A claim is only checkable when the prose names the metric. Bare percentages
# ("SOXL can lose 80 to 90 percent", "RSI below 30") are design facts, not
# portfolio statistics, and are deliberately not matched.
#
# Each entry: metric key, regex, multiplier from the live value to prose units.
# Every regex captures the number in group 1 or group 2 so either word order
# works ("2.18 Sharpe" and "Sharpe ratio of 2.18").
CLAIMS = [
    (
        "sharpe_ratio",
        re.compile(r"(\d[\d,]*(?:\.\d+)?)\s+Sharpe\b|\bSharpe(?:\s+ratio)?\s+(?:of\s+)?\(?(\d[\d,]*(?:\.\d+)?)", re.I),
        1.0,
    ),
    (
        "calmar_ratio",
        re.compile(r"(\d[\d,]*(?:\.\d+)?)\s+Calmar\b|\bCalmar(?:\s+ratio)?\s+(?:of\s+)?\(?(\d[\d,]*(?:\.\d+)?)", re.I),
        1.0,
    ),
    (
        "sortino_ratio",
        re.compile(r"(\d[\d,]*(?:\.\d+)?)\s+Sortino\b|\bSortino(?:\s+ratio)?\s+(?:of\s+)?\(?(\d[\d,]*(?:\.\d+)?)", re.I),
        1.0,
    ),
    (
        "max_drawdown",
        re.compile(
            r"(\d[\d,]*(?:\.\d+)?)%\s+max(?:imum)?\s+drawdown|\bmax(?:imum)?\s+drawdown\s+(?:of\s+)?"
            r"(?:-\s*)?(\d[\d,]*(?:\.\d+)?)%",
            re.I,
        ),
        100.0,
    ),
    (
        "standard_deviation",
        re.compile(
            r"(\d[\d,]*(?:\.\d+)?)%\s+(?:annuali[sz]ed\s+)?(?:volatility|standard deviation)"
            r"|\b(?:volatility|standard deviation)\s+(?:of\s+)?(\d[\d,]*(?:\.\d+)?)%",
            re.I,
        ),
        100.0,
    ),
    (
        "annualized_rate_of_return",
        # "annualized" also appears in "annualized standard deviation" and
        # "annualized volatility", which is a different metric entirely. Requiring
        # a return word on one side or the other keeps those out; without this
        # guard the 90.0% volatility figure on gold-miner-original is read as a
        # 90% return and reported as wildly stale.
        re.compile(
            r"(\d[\d,]*(?:\.\d+)?)%\s+annuali[sz]ed(?!\s+(?:standard deviation|volatility|std))"
            r"|\bannuali[sz]ed\s+return\s+(?:of\s+)?(\d[\d,]*(?:\.\d+)?)%"
            r"|\bannuali[sz]e[sd]?\s+at\s+(\d[\d,]*(?:\.\d+)?)%",
            re.I,
        ),
        100.0,
    ),
]


def walk(value, path, out):
    """Collect (path, text) for every string anywhere under a prose field."""
    if isinstance(value, str):
        out.append((path, value))
    elif isinstance(value, list):
        for i, item in enumerate(value):
            walk(item, "%s[%d]" % (path, i), out)
    elif isinstance(value, dict):
        for key in sorted(value):
            walk(value[key], "%s.%s" % (path, key), out)


def decimals(text):
    return len(text.split(".")[1]) if "." in text else 0


def context(text, match):
    start = max(0, match.start() - 55)
    end = min(len(text), match.end() + 55)
    return ("..." if start else "") + text[start:end].strip() + ("..." if end < len(text) else "")


def main():
    show_all = "--all" in sys.argv[1:]
    strategies = json.loads(io.open(STRATEGIES, encoding="utf-8").read())

    checked = 0
    drifted = []
    matched = []
    unverifiable = []

    for strategy in strategies:
        slug = strategy.get("slug", "<no slug>")
        texts = []
        for field in PROSE_FIELDS:
            if field in strategy:
                walk(strategy[field], field, texts)

        for path, text in texts:
            for metric, pattern, multiplier in CLAIMS:
                for match in pattern.finditer(text):
                    raw = next(g for g in match.groups() if g)
                    # No try/except here on purpose. Swallowing a malformed number is
                    # how a stale figure hides: an earlier version of the number
                    # pattern captured the sentence-ending period, float() raised, and
                    # the claim was skipped in silence, so every figure that ended a
                    # sentence was invisible to this script. If this ever raises, the
                    # regex is wrong and that must be loud.
                    claimed = float(raw.replace(",", ""))
                    live = strategy.get(metric)
                    if live is None:
                        unverifiable.append((slug, path, metric, raw))
                        continue
                    checked += 1
                    live = abs(live) * multiplier
                    # Tolerance is the prose's own rounding: a claim written to
                    # one decimal is wrong only if it rounds to something else.
                    places = decimals(raw)
                    rounded = round(live, places)
                    if abs(rounded - claimed) > 0.51 / (10 ** places):
                        drifted.append((slug, path, metric, raw, rounded, context(text, match)))
                    else:
                        matched.append((slug, path, metric, raw, rounded))

    print("Scanned %d strategies across %d prose field(s)." % (len(strategies), len(PROSE_FIELDS)))
    print("Checkable numeric claims found: %d" % checked)
    print("  matching live metrics: %d" % len(matched))
    print("  drifted:               %d" % len(drifted))
    if unverifiable:
        print("  named a metric this strategy does not carry: %d" % len(unverifiable))
        for slug, path, metric, raw in unverifiable:
            print("      %s %s: %s = %s, but %s is null" % (slug, path, metric, raw, metric))

    if show_all and matched:
        print("\nStill accurate (%d):" % len(matched))
        for slug, path, metric, raw, live in matched:
            print("  %-32s %-22s %-26s %s" % (slug, path, metric, raw))

    if drifted:
        by_slug = {}
        for row in drifted:
            by_slug.setdefault(row[0], []).append(row)
        print("\nFAIL: %d stale figure(s) across %d strategy page(s)."
              % (len(drifted), len(by_slug)))
        print("These render as fact and are wrong. update_metrics.py refreshes the")
        print("metrics nightly and cannot rewrite prose, so a quoted figure is only")
        print("correct on the day it was typed. Remove it and let the metrics table")
        print("own the number, or restate it.\n")
        for slug in sorted(by_slug):
            print("  %s" % slug)
            for _, path, metric, raw, live, ctx in by_slug[slug]:
                print("    %-26s prose=%-10s live=%-10s  (%s)" % (metric, raw, live, path))
                print("      %s" % ctx)
        return 1

    print("\nPASS: every performance figure quoted in prose matches the live metrics.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
