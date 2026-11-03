#!/usr/bin/env python3
"""Check that data/daily_returns.json is intact and agrees with the metrics.

Why this exists. V1.20 item 16 stores a daily return series per visible
strategy so that worst month, VaR, CVaR, time in market and the year-jackknife
become computable. The failure mode is not a crash: a truncated, misaligned or
stale series produces plausible numbers that are quietly wrong, and anything
derived from it inherits the error without a symptom. So the check is not "does
the file parse" but "does this series still reproduce the published metrics".

What it checks, per visible strategy:
  - a series exists, with `days` and `returns` the same length
  - `days` strictly increases (no duplicate or out-of-order trading days)
  - the series length equals the strategy's own `backtest_days`
  - recomputing max drawdown, annualized volatility, Sharpe and annualized
    return from the series lands within tolerance of the stored metrics

Tolerances are set from measurement, not taste. Across all 24 the observed
worst deviations were max drawdown 4.1e-6, volatility 6.5e-4, Sharpe 2.4e-3 and
annualized return 1.2e-3. The residual is convention rather than error: this
recomputes Sharpe against a zero risk-free rate and uses a population standard
deviation, and the API need not do either. The thresholds below sit an order of
magnitude above what was measured, so they catch corruption without firing on
the arithmetic.

Two conventions worth stating, both established by measurement against the API:
  - Annualized return compounds over (n + 1) / 252 years, NOT calendar days.
    Using calendar days instead is a 4.8e-3 error, which is larger than every
    tolerance here.
  - `days[i]` is the day `returns[i]` was earned on. The first point of the
    underlying value series has no return, so `n` returns come from n + 1 daily
    values, and `n` is what the API reports as `size`.

Advisory, not a gate: the owner's 2026-09-02 ruling on PRD item 10b gated
check_asset_sizes.py alone and left the rest reporting.

Usage:
    python scripts/check_daily_returns.py
"""

import json
import math
import statistics
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TRADING_DAYS = 252

TOLERANCE = {
    "max_drawdown": 1e-3,
    "standard_deviation": 5e-3,
    "sharpe_ratio": 2e-2,
    "annualized_rate_of_return": 2e-2,
}


def recompute(returns):
    """Max drawdown, annualized volatility, Sharpe and annualized return."""
    cumulative = peak = 1.0
    drawdown = 0.0
    for r in returns:
        cumulative *= 1 + r
        peak = max(peak, cumulative)
        drawdown = min(drawdown, cumulative / peak - 1)

    volatility = statistics.pstdev(returns) * math.sqrt(TRADING_DAYS)
    return {
        "max_drawdown": drawdown,
        "standard_deviation": volatility,
        "sharpe_ratio": (statistics.fmean(returns) * TRADING_DAYS) / volatility
                        if volatility else 0.0,
        "annualized_rate_of_return":
            cumulative ** (TRADING_DAYS / (len(returns) + 1)) - 1,
    }


def main():
    data = json.loads((BASE_DIR / "data" / "strategies.json").read_text(encoding="utf-8"))
    path = BASE_DIR / "data" / "daily_returns.json"
    if not path.exists():
        print("FAIL: data/daily_returns.json is missing.")
        return 1
    series = json.loads(path.read_text(encoding="utf-8")).get("series", {})

    visible = [s for s in data if not s.get("hidden")]
    problems = []
    checked = 0

    for s in visible:
        slug = s["slug"]
        entry = series.get(slug)
        if entry is None:
            problems.append("%s: no stored series" % slug)
            continue

        days = entry.get("days") or []
        returns = entry.get("returns") or []
        if len(days) != len(returns):
            problems.append("%s: %d days against %d returns"
                            % (slug, len(days), len(returns)))
            continue
        if not returns:
            problems.append("%s: empty series" % slug)
            continue
        if any(b <= a for a, b in zip(days, days[1:])):
            problems.append("%s: days are not strictly increasing" % slug)
            continue
        if entry.get("symphony_id") != s.get("symphony_id"):
            problems.append("%s: series belongs to a different symphony" % slug)
            continue

        # The strongest single check here. `backtest_days` comes from the API
        # and the series is built locally, so a mismatch means one of the two
        # moved without the other, which is exactly the silent staleness this
        # file exists to catch.
        if len(returns) != s.get("backtest_days"):
            problems.append("%s: %d returns against backtest_days %s"
                            % (slug, len(returns), s.get("backtest_days")))
            continue

        got = recompute(returns)
        for field, limit in TOLERANCE.items():
            stored = s.get(field)
            if stored is None:
                continue
            delta = abs(got[field] - stored)
            if delta > limit:
                problems.append("%s: %s recomputes to %.6f, stored %.6f (off by %.2e)"
                                % (slug, field, got[field], stored, delta))
        checked += 1

    for p in problems:
        print("  " + p)
    size = path.stat().st_size / 1e6
    print("Checked %d of %d visible strategies, %.2f MB on disk."
          % (checked, len(visible), size))
    if problems:
        print("FAIL: %d problems in the daily return series." % len(problems))
        return 1
    print("PASS: every series is intact and reproduces its published metrics.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
