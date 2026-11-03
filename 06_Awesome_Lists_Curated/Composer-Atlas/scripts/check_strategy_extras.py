#!/usr/bin/env python3
"""Deploy gate for data/strategy_extras.json and its .js twin.

The join in build_strategy_extras.py is cheap and deterministic, so the gate
does not inspect the committed file for plausibility: it rebuilds the join in
memory and demands byte equality. That catches all three ways this pair goes
wrong, and the third is the one that has actually happened on this project:

  1. A featured strategy has no row in data/database.json. The build itself
     raises on this, so running it here surfaces it before deploy.
  2. The committed file is stale, because database.json or k1.json was
     refreshed and the build was not rerun.
  3. The .json and the .js twin disagree. `data/database.js` shipped one entry
     behind `data/database.json` at v1.27.9 and check_database_keys.py passed
     anyway, because it checks keys rather than whether the twins match.

Usage:
    python scripts/check_strategy_extras.py

Exit code is non-zero if anything is off, so it can gate a deploy.
"""

import importlib.util
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = BASE_DIR / "data" / "strategy_extras.json"
JS_PATH = BASE_DIR / "data" / "strategy_extras.js"
BUILDER = BASE_DIR / "scripts" / "build_strategy_extras.py"

JS_PREFIX = "window.STRATEGY_EXTRAS_DATA = "


def load_builder():
    spec = importlib.util.spec_from_file_location("build_strategy_extras", BUILDER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    problems = []

    for path in (JSON_PATH, JS_PATH):
        if not path.exists():
            problems.append("%s is missing. Run scripts/build_strategy_extras.py." % path.name)
    if problems:
        print("\n".join("FAIL: " + p for p in problems))
        return 1

    builder = load_builder()
    # A join miss raises SystemExit out of build(), which is the loud failure
    # the V1.20 item asked for. Let it through rather than reformatting it.
    _, extras, _ = builder.build()
    expected = builder.payload(extras)

    on_disk_json = JSON_PATH.read_text(encoding="utf-8")
    if on_disk_json != expected + "\n":
        problems.append(
            "data/strategy_extras.json does not match a fresh join. It is stale.\n"
            "      Run scripts/build_strategy_extras.py and commit both files."
        )

    on_disk_js = JS_PATH.read_text(encoding="utf-8")
    if JS_PREFIX not in on_disk_js:
        problems.append("data/strategy_extras.js does not assign %s" % JS_PREFIX.strip())
    else:
        body = on_disk_js.split(JS_PREFIX, 1)[1]
        if not body.endswith(";\n"):
            problems.append("data/strategy_extras.js does not end with a semicolon and a newline")
        elif body[:-2] != expected:
            problems.append(
                "data/strategy_extras.js and data/strategy_extras.json disagree.\n"
                "      Commit both or neither. Run scripts/build_strategy_extras.py."
            )

    if problems:
        print("\n".join("FAIL: " + p for p in problems))
        return 1

    print("PASS: strategy_extras.json and .js match a fresh join of %d strategies."
          % len(extras))
    return 0


if __name__ == "__main__":
    sys.exit(main())
