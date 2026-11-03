#!/usr/bin/env python3
"""
check_risk_profiles.py: validate the shape of every strategy's `risk_profile`.

V1.20 item 10 splits `risk_profile` from one string into named categories. The
rewrite ships one strategy at a time behind an owner sign-off, so **both shapes
are valid and coexist by design**: a string is the pre-item-10 form and renders
exactly as it always did.

Why this check exists. A typo in a category key does not crash anything. It
renders a Risk Profile section with that category silently missing, still HTTP
200 and still laid out correctly. That is the same failure shape that took the
Signal Miner down in v1.22.2 and the reason check_html_js.py exists, and no
other gate can see it: the four deploy gates check HTML/JS pairing, the ladder,
database keys and the strategy_extras join, and none of them reads this field.

**NOT wired into .github/workflows/deploy.yml.** Whether it should be a fifth
gate is an open question for the owner, recorded in docs/PRD.md item 10. Adding
a deploy gate changes what can block a release, which is not a call to make as
a side effect of a content edit.

Usage:
    python scripts/check_risk_profiles.py

Exit 0 on pass, 1 on failure.
"""

import io
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STRATEGIES = BASE_DIR / "data" / "strategies.json"

# Must match RISK_CATEGORIES in strategies.html, plus the two fields that are
# not rendered as categories: `verdict` (its own badge) and `suitability` (an
# optional tail note).
KNOWN_KEYS = {
    "verdict",
    "leverage",
    "backtest_limits",
    "signal",
    "hedge",
    "concentration",
    "suitability",
}


def main():
    strategies = json.loads(io.open(STRATEGIES, encoding="utf-8").read())
    problems = []
    strings = 0
    objects = 0

    for s in strategies:
        slug = s.get("slug", "<no slug>")
        rp = s.get("risk_profile")

        if rp is None:
            problems.append("%s: no risk_profile at all" % slug)
            continue

        if isinstance(rp, str):
            strings += 1
            if not rp.strip():
                problems.append("%s: risk_profile is an empty string" % slug)
            continue

        if not isinstance(rp, dict):
            problems.append("%s: risk_profile is %s, expected str or object"
                            % (slug, type(rp).__name__))
            continue

        objects += 1

        # The typo case this script exists for.
        unknown = sorted(set(rp) - KNOWN_KEYS)
        if unknown:
            problems.append(
                "%s: unknown risk_profile key(s) %s. These render as nothing at "
                "all, silently. Known keys: %s"
                % (slug, ", ".join(unknown), ", ".join(sorted(KNOWN_KEYS)))
            )

        # verdict is the one required field: it opens all 31 original strings and
        # is the only part the page renders outside the category list.
        if not (rp.get("verdict") or "").strip():
            problems.append("%s: object risk_profile with no verdict" % slug)

        for key, value in sorted(rp.items()):
            if key in KNOWN_KEYS and not isinstance(value, str):
                problems.append("%s: risk_profile.%s is %s, expected str"
                                % (slug, key, type(value).__name__))
            elif isinstance(value, str) and not value.strip():
                # An absent category must be ABSENT, not empty. The page prints an
                # explicit "no hedge leg" line for a missing key; an empty string
                # is truthy-checked as missing but says the author meant something.
                problems.append(
                    "%s: risk_profile.%s is empty. Omit the key instead, so the "
                    "page prints its explicit absence line." % (slug, key)
                )

    print("Checked %d strategies: %d categorised, %d still single strings."
          % (len(strategies), objects, strings))

    if problems:
        print("\nFAIL: %d problem(s)" % len(problems))
        for p in problems:
            print("  - %s" % p)
        return 1

    print("PASS: every risk_profile is a non-empty string or a valid object.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
