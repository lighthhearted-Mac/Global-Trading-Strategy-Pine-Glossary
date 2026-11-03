#!/usr/bin/env python3
"""Check the shape of the `signals` schema after V1.20 item 11.

Why this exists. `type` and `indicator` render through `signalType()` and
`signalIndicator()` in strategies.html, and both degrade quietly by design: an
absent or unrecognised value renders "not categorised" or "none" rather than
throwing. That is right for the hidden strategies, which still carry the
pre-item-11 shape, and it is exactly wrong for a typo. "Trend " with a trailing
space, or "Momentum" instead of "Trend", produces a page that is HTTP 200,
correctly laid out, and silently mislabelled. No existing gate can see it.

What it checks, on visible strategies only:
  - every signal is an object with name, tag, description
  - `type` is one of the four known values, exactly
  - `indicator` is a list of strings, empty only where type is Composition
  - `indicator` labels look like a known function, with or without a window

What it deliberately does NOT check: whether an indicator label matches the
strategy's symphony tree. That is the real guarantee, and it was established
once at authoring time by scratchpad/verify_signals.py walking all 24 cached
trees. The trees are not in the repo, so re-deriving it here is not possible.

Advisory, not a gate: the owner's 2026-09-02 ruling on PRD item 10b gated
check_asset_sizes.py alone and left the rest reporting.

Usage:
    python scripts/check_signal_types.py
"""

import json
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TYPES = {"Threshold", "Trend", "Selection", "Composition"}
FUNCS = {"RSI", "MA", "MA return", "EMA", "Return", "Volatility",
         "Drawdown", "Price", "Std dev price"}
LABEL = re.compile(r"^([A-Za-z ]+?)(?:\((\d+)\))?$")


def main():
    data = json.loads((BASE_DIR / "data" / "strategies.json").read_text(encoding="utf-8"))
    problems = []
    checked = legacy = 0

    for s in data:
        signals = s.get("signals") or []
        for i, sig in enumerate(signals):
            where = "%s signals[%d]" % (s["slug"], i)
            if not isinstance(sig, dict):
                problems.append("%s: not an object" % where)
                continue
            for key in ("name", "tag", "description"):
                if not str(sig.get(key) or "").strip():
                    problems.append("%s: empty %s" % (where, key))

            if s.get("hidden"):
                # The pre-item-11 shape is intended here, but a half-migration
                # is not: one field without the other is a mistake either way.
                if ("type" in sig) != ("indicator" in sig):
                    problems.append("%s: half-migrated, has one of type/indicator" % where)
                legacy += 1
                continue

            checked += 1
            ty = sig.get("type")
            if ty not in TYPES:
                problems.append("%s: type %r not one of %s"
                                % (where, ty, ", ".join(sorted(TYPES))))
            ind = sig.get("indicator")
            if not isinstance(ind, list) or any(not isinstance(x, str) for x in ind):
                problems.append("%s: indicator is not a list of strings" % where)
                continue
            if not ind and ty != "Composition":
                problems.append("%s: %s row with no indicator" % (where, ty))
            for label in ind:
                m = LABEL.match(label)
                if not m or m.group(1).strip() not in FUNCS:
                    problems.append("%s: indicator %r is not a known function"
                                    % (where, label))

    for p in problems:
        print("  " + p)
    print("Checked %d categorised signals and %d on hidden strategies."
          % (checked, legacy))
    if problems:
        print("FAIL: %d problems in the signals schema." % len(problems))
        return 1
    print("PASS: every signal has a known type and verifiable indicator labels.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
