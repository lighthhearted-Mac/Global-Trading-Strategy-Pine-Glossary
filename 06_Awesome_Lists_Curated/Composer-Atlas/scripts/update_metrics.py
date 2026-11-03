#!/usr/bin/env python3
"""
update_metrics.py: Fetch fresh data from the Composer API and update:
  - data/strategies.json + data/strategies.js  (backtest metrics for all strategies)
  - data/daily_returns.json + .js               (daily return series, visible strategies)
  - data/symphony_scores.json                   (full logic trees for all symphonies)

Symphony scores are stored for AI analysis and future reference only.
They are NOT served to the website.

Usage:
    python scripts/update_metrics.py

No API key required. Run from the project root or the scripts/ folder.
Run regularly (daily, or after any symphony logic changes).

Strategies whose last_updated is less than STALE_AFTER_DAYS old are skipped,
so this script can be run daily and will only refresh what's actually due
(and automatically retry any strategy that failed on a previous run).
"""

import json
import time
import urllib.request
from datetime import date, timedelta
from pathlib import Path

# ---- Paths ----
BASE_DIR        = Path(__file__).resolve().parent.parent
STRATEGIES_JSON = BASE_DIR / "data" / "strategies.json"
STRATEGIES_JS   = BASE_DIR / "data" / "strategies.js"
SCORES_JSON     = BASE_DIR / "data" / "symphony_scores.json"
DAILY_JSON      = BASE_DIR / "data" / "daily_returns.json"
DAILY_JS        = BASE_DIR / "data" / "daily_returns.js"

# ---- Backtest parameters ----
BACKTEST_PARAMS = {
    "capital": 10000,
    "broker": "alpaca",
    "slippage_percent": 0.0005,
    "apply_reg_fee": True,
    "apply_taf_fee": True,
}

API_BASE = "https://api.composer.trade"

STALE_AFTER_DAYS = 7
API_CALL_DELAY_SECONDS = 2

# V1.20 item 16. The backtest response carries a full daily portfolio-value
# series in `dvm_capital` that this script used to read straight past. Keeping
# it as daily returns is what makes worst month, VaR, CVaR, time in market and
# the year-jackknife computable rather than unavailable.
#
# Six decimal places, decided by measurement rather than taste: against the full
# unrounded series, recomputed Sharpe moves by 7.7e-7 and annualized return by
# 1.5e-6, while the file is 20% smaller than at 8dp. Lossless for every use this
# data has.
DAILY_RETURN_DIGITS = 6

# Visible strategies only, by owner ruling 2026-09-03. 24 of the 36, roughly
# 35 KB each, so about 0.9 MB. The same storage for the 6,668 community database
# rows would be 233 MB, which is why this is scoped to strategies and stays so.
DAILY_RETURNS_VISIBLE_ONLY = True

# Fields in the API stats object that map 1:1 to our schema
DIRECT_FIELDS = [
    "annualized_rate_of_return",
    "cumulative_return",
    "calmar_ratio",
    "sharpe_ratio",
    "standard_deviation",
    "min",
    "mean",
    "median",
    "max",
    "trailing_one_month_return",
    "trailing_three_month_return",
    "trailing_one_year_return",
]


# Composer's edge (Cloudflare) blocks requests without a browser-like
# User-Agent (error code 1010), so every request needs one set explicitly.
USER_AGENT = "Mozilla/5.0 (compatible; composer-metrics-updater/1.0)"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def post(url, body):
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": USER_AGENT},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


# ---- Daily return series (V1.20 item 16) ----

def extract_daily_returns(result, symphony_id):
    """Turn the backtest's `dvm_capital` map into aligned day and return arrays.

    `dvm_capital` is keyed by symphony id, then by epoch day (days since
    1970-01-01) holding the portfolio value on that day. Those are trading days,
    so they are NOT contiguous: the gaps are weekends and market holidays.
    Storing an explicit day array rather than a start date plus a stride is what
    keeps that honest, and it costs about 20 KB per strategy.

    `days[i]` is the day `returns[i]` was earned on, so the two arrays are the
    same length and the first point in the series has no return, as it should
    not: there is nothing before it to measure against.
    """
    capital = (result.get("dvm_capital") or {}).get(symphony_id)
    if capital is None:
        # One entry is unambiguous even under a key we did not expect; more
        # than one is not, so refuse rather than guess.
        values = list((result.get("dvm_capital") or {}).values())
        if len(values) != 1:
            raise ValueError("dvm_capital has %d series, expected 1" % len(values))
        capital = values[0]

    order = sorted(int(k) for k in capital)
    if len(order) < 2:
        raise ValueError("series has %d points, need at least 2" % len(order))

    days, returns = [], []
    prev = capital[str(order[0])]
    for day in order[1:]:
        value = capital[str(day)]
        if prev == 0:
            raise ValueError("zero portfolio value before day %d" % day)
        days.append(day)
        returns.append(round(value / prev - 1, DAILY_RETURN_DIGITS))
        prev = value
    return days, returns


def load_daily_returns():
    if DAILY_JSON.exists():
        return json.loads(DAILY_JSON.read_text(encoding="utf-8"))
    return {"generated": None, "series": {}}


def write_daily_returns(daily):
    """Write the series file and its .js twin.

    Written compactly, with no indent. Indenting an array of 90,000 numbers puts
    each on its own line and multiplies the file roughly fivefold for a
    readability nobody benefits from: nothing reads this by eye.
    """
    daily["generated"] = date.today().isoformat()
    body = json.dumps(daily, ensure_ascii=False, separators=(",", ":"))
    DAILY_JSON.write_text(body + "\n", encoding="utf-8")
    print(f"Wrote {DAILY_JSON.name} ({len(body) / 1e6:.2f} MB, "
          f"{len(daily['series'])} strategies)")

    comment = (
        "// Daily return series - loaded as a script tag so the site works with file:// protocol.\n"
        "// To update: run scripts/update_metrics.py\n"
    )
    DAILY_JS.write_text(comment + f"window.DAILY_RETURNS_DATA = {body};\n",
                        encoding="utf-8")
    print(f"Wrote {DAILY_JS.name}")


# ---- Backtest metrics ----

def update_strategies():
    strategies = json.loads(STRATEGIES_JSON.read_text(encoding="utf-8"))
    daily = load_daily_returns()
    today = date.today().isoformat()
    stale_cutoff = date.today() - timedelta(days=STALE_AFTER_DAYS)
    failed = []
    series_failed = []
    calls_made = 0

    for s in strategies:
        sym_id = s["symphony_id"]

        # Fresh metrics are no longer a reason to skip on their own: a visible
        # strategy with no stored daily series still has to be fetched once.
        # Folding that into the existing staleness check is what makes the item
        # 16 backfill cost zero extra API calls, now and for anything added
        # later. `wants_series` is False for hidden strategies, so those skip on
        # freshness exactly as before.
        wants_series = not (DAILY_RETURNS_VISIBLE_ONLY and s.get("hidden"))
        has_series = s["slug"] in daily["series"]
        last_updated = s.get("last_updated")
        fresh = last_updated and date.fromisoformat(last_updated) > stale_cutoff
        if fresh and (has_series or not wants_series):
            continue

        if calls_made > 0:
            time.sleep(API_CALL_DELAY_SECONDS)
        calls_made += 1

        print(f"  {s['name']} ... ", end="", flush=True)
        try:
            result = post(
                f"{API_BASE}/api/v0.1/symphonies/{sym_id}/backtest",
                BACKTEST_PARAMS,
            )
            stats = result["stats"]

            for field in DIRECT_FIELDS:
                if field in stats:
                    s[field] = stats[field]

            # API returns max_drawdown as positive; schema stores it negative
            s["max_drawdown"] = -abs(stats["max_drawdown"])

            # API calls it "size"; schema calls it backtest_days
            s["backtest_days"] = stats["size"]

            s["last_updated"] = today

            if wants_series:
                # A failure here must not throw away the metrics just fetched,
                # and must not leave a strategy silently without a series.
                try:
                    days, returns = extract_daily_returns(result, sym_id)
                    daily["series"][s["slug"]] = {
                        "symphony_id": sym_id,
                        "days": days,
                        "returns": returns,
                        "last_updated": today,
                    }
                except Exception as exc:
                    series_failed.append(f"{s['name']}: {exc}")

            print(
                f"ARR {stats['annualized_rate_of_return']:+.1%}  "
                f"DD -{stats['max_drawdown']:.1%}  "
                f"Sharpe {stats['sharpe_ratio']:.2f}"
            )

        except Exception as exc:
            print(f"FAILED: {exc}")
            failed.append(s["name"])

    if calls_made == 0:
        print(f"  Nothing due (all strategies updated within the last {STALE_AFTER_DAYS} days)")

    if failed:
        print(f"\nWARNING: {len(failed)} strategies failed:")
        for name in failed:
            print(f"  - {name}")

    if series_failed:
        print(f"\nWARNING: {len(series_failed)} daily series failed "
              f"(metrics for these were still updated):")
        for note in series_failed:
            print(f"  - {note}")

    # A strategy that was deleted or newly hidden should not keep its series
    # forever: the file would quietly diverge from what the site shows.
    wanted = {s["slug"] for s in strategies
              if not (DAILY_RETURNS_VISIBLE_ONLY and s.get("hidden"))}
    for slug in [k for k in daily["series"] if k not in wanted]:
        del daily["series"][slug]
        print(f"  dropped stale series: {slug}")

    return strategies, daily


def write_strategies_json(strategies):
    STRATEGIES_JSON.write_text(
        json.dumps(strategies, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"\nWrote {STRATEGIES_JSON.name}")


def write_strategies_js(strategies):
    comment = (
        "// Strategies data - loaded as a script tag so the site works with file:// protocol.\n"
        "// To update metrics: run scripts/update_metrics.py\n"
    )
    body = f"window.STRATEGIES_DATA = {json.dumps(strategies, indent=2, ensure_ascii=False)};\n"
    STRATEGIES_JS.write_text(comment + body, encoding="utf-8")
    print(f"Wrote {STRATEGIES_JS.name}")


# ---- Symphony logic trees ----

def update_scores(strategies):
    # Start from the existing file so a failed fetch keeps the last-known
    # score instead of being dropped from the output.
    scores = json.loads(SCORES_JSON.read_text(encoding="utf-8")) if SCORES_JSON.exists() else {}
    failed = []

    for i, s in enumerate(strategies):
        slug   = s["slug"]
        sym_id = s["symphony_id"]

        if i > 0:
            time.sleep(API_CALL_DELAY_SECONDS)

        print(f"  {s['name']} ... ", end="", flush=True)
        try:
            score = get(
                f"{API_BASE}/api/v0.1/symphonies/{sym_id}/score?score_version=v1"
            )
            scores[slug] = score
            print("OK")
        except Exception as exc:
            print(f"FAILED: {exc}")
            failed.append(s["name"])

    if failed:
        print(f"\nWARNING: {len(failed)} scores failed:")
        for name in failed:
            print(f"  - {name}")

    return scores


def write_scores_json(scores):
    SCORES_JSON.write_text(
        json.dumps(scores, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {SCORES_JSON.name}")


# ---- Main ----

if __name__ == "__main__":
    print("── Backtest metrics ──────────────────────────")
    strategies, daily = update_strategies()
    write_strategies_json(strategies)
    write_strategies_js(strategies)
    write_daily_returns(daily)

    print("\n── Symphony logic trees ──────────────────────")
    scores = update_scores(strategies)
    write_scores_json(scores)

    print("\nDone.")
