#!/usr/bin/env python3
"""Check that no file Cloudflare would serve exceeds its per-file upload limit.

Why this exists. On 2026-09-01 commit 90f6dcf grew `data/symphony_scores.json`
from 22.8 MB to 26.3 MB as part of a routine metrics refresh. That is 210 KB
over Cloudflare's 25 MiB per-file limit, and the next deployment failed. Nothing
in the repo noticed: the file is not referenced by any page, `deploy.yml` already
excluded it from the GitHub Pages build, and the four deploy gates check data
correctness rather than deliverability. The site simply stopped updating, and the
only signal was a red build in a dashboard nobody was watching.

The failure shape is the one this project keeps designing against: a routine,
correct, automated change that breaks something downstream silently.

What it checks. Every tracked file that `.assetsignore` does NOT exclude, against
the 25 MiB limit. Also warns at 70%, not 80%, so a file on its way up is visible before it
is a broken deploy. That threshold is calibrated on what actually happened:
`symphony_scores.json` went from 87% of the limit to over it in ten days, so 80%
would have given roughly a fortnight's notice. `data/database.json` and its `.js`
twin are 19 MiB each and growing weekly, and they are the next candidates.

Usage:
    python scripts/check_asset_sizes.py

Exit code is non-zero if any served file is over the limit. **Wired into
.github/workflows/deploy.yml as the fifth gate** by owner ruling on PRD item 10b,
2026-09-02; check_risk_profiles.py and check_stat_drift.py stay advisory under the
same ruling.

One honest limitation. That workflow deploys to GitHub Pages, which is not the
live path: Cloudflare builds independently from the same push, so a failure here
cannot actually stop a bad deploy. It converts an opaque Cloudflare failure into a
red check naming the file and its size, which is the difference between noticing
in minutes and noticing in a day.

The walk uses `git ls-files`, which is the right list rather than a compromise:
Cloudflare builds from a clean clone, so an untracked local file never reaches it
and a tracked one always does.
"""

import fnmatch
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LIMIT = 25 * 1024 * 1024
WARN_AT = 0.70


def assetsignore_patterns():
    """gitignore-style patterns from .assetsignore, as Cloudflare reads them."""
    path = BASE_DIR / ".assetsignore"
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(line)
    return out


def is_ignored(rel, patterns):
    for pat in patterns:
        # A trailing slash means a directory and everything under it.
        if pat.endswith("/"):
            if rel == pat[:-1] or rel.startswith(pat):
                return True
        elif fnmatch.fnmatch(rel, pat) or rel == pat:
            return True
        # A bare directory name with no slash still covers its contents.
        elif "/" not in pat and rel.startswith(pat + "/"):
            return True
    return False


def tracked_files():
    out = subprocess.run(
        ["git", "ls-files", "-z"], cwd=BASE_DIR,
        capture_output=True, check=True,
    ).stdout.decode("utf-8")
    return [p for p in out.split("\0") if p]


def main():
    patterns = assetsignore_patterns()
    over, warn, served = [], [], 0

    for rel in tracked_files():
        if is_ignored(rel, patterns):
            continue
        path = BASE_DIR / rel
        if not path.exists():
            continue
        served += 1
        size = path.stat().st_size
        if size > LIMIT:
            over.append((rel, size))
        elif size > LIMIT * WARN_AT:
            warn.append((rel, size))

    over.sort(key=lambda x: -x[1])
    warn.sort(key=lambda x: -x[1])

    for rel, size in warn:
        print("WARN: %s is %.2f MiB, %.0f%% of the %d MiB limit."
              % (rel, size / 1048576, size / LIMIT * 100, LIMIT // 1048576))

    if over:
        for rel, size in over:
            print("FAIL: %s is %.2f MiB, %.0f KB OVER the %d MiB limit."
                  % (rel, size / 1048576, (size - LIMIT) / 1024, LIMIT // 1048576))
        print("\nCloudflare rejects the whole deployment over this, so the site\n"
              "stops updating with no other symptom. Either shrink the file or add\n"
              "it to .assetsignore if no page actually serves it. Check first:\n"
              "    grep -rn '<name>' --include=*.html --include=*.js .")
        return 1

    print("PASS: %d served files, none over the %d MiB limit%s."
          % (served, LIMIT // 1048576,
             ", %d approaching it" % len(warn) if warn else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
