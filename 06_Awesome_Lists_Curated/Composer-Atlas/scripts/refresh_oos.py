# -*- coding: utf-8 -*-
"""Fetch true out-of-sample statistics for the Leaderboard's candidate set.

Writes data/oos.json and its .js twin, keyed by symphony_id. See docs/PRD.md
V1.18 for the design and the decisions behind it.

WHY THIS IS A SEPARATE SCRIPT AND A SEPARATE WORKFLOW.
    refresh_full_database.py already runs 4.5 to 5 hours against GitHub's
    6-hour job ceiling. A second API call per row does not fit beside it, so
    this runs on its own day, over its own scoped set of rows.

WHAT "OUT OF SAMPLE" MEANS HERE.
    `oos_date` is the symphony's last logic edit (`last_semantic_update_at`).
    Every day after it is a day the author did not tune against, so a backtest
    starting there is a genuine out-of-sample record. This is the only sense of
    out-of-sample the data supports, and it has a property worth stating: it
    rewards leaving a symphony alone, and resets the moment its logic is
    edited.

THE TRAP THIS SCRIPT EXISTS TO AVOID.
    The API honours `start_date` and `end_date`. It SILENTLY IGNORES `start`
    and `end`, returning the full backtest with a 200 and no warning of any
    kind. A version of this script with the wrong key name would look like it
    worked perfectly and would publish in-sample numbers labelled
    out-of-sample, which would make the Leaderboard look validated precisely
    where it is not. Every response is therefore checked against the window it
    was asked for, and a row that fails is discarded rather than stored. See
    check_window().

Usage:
    python scripts/refresh_oos.py            # the whole candidate set
    python scripts/refresh_oos.py 300        # first 300 due rows, for a smoke run
    python scripts/refresh_oos.py --force    # refetch even rows already current
"""
import datetime as dt
import io
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
# ADVANCED_METRICS, not the Simplified set: the candidate cutoff has to be
# derived from the IN-SAMPLE model, because the out-of-sample pillar is the
# thing this script is about to go and fetch. Scoring the candidate set on a
# model that already reads data/oos.json would make the selection depend on
# whatever the last run happened to cover.
from analyze_leaderboard import (  # noqa: E402  (path set above)
    ADVANCED_METRICS, eligible, load_entries, oos_days, score_pool,
)

BASE_DIR = Path(__file__).resolve().parent.parent
PRICES = BASE_DIR / "data" / "prices.json"
STRATEGIES = BASE_DIR / "data" / "strategies.json"
JSON_PATH = BASE_DIR / "data" / "oos.json"
JS_PATH = BASE_DIR / "data" / "oos.js"

API_BASE = "https://api.composer.trade"
UA = "Mozilla/5.0 (compatible; ComposerAtlas/1.0; +https://composeratlas.com)"
BODY = {
    "capital": 10000,
    "broker": "alpaca",
    "slippage_percent": 0.0005,
    "apply_reg_fee": True,
    "apply_taf_fee": True,
}

# Matches refresh_full_database.py. Calls take about a second; the rest is a
# politeness margin, and it is not reduced without evidence that would have to
# come from deliberately probing someone else's rate limiter.
API_CALL_DELAY_SECONDS = 2
CHECKPOINT_EVERY = 10

# Candidate set (PRD V1.18). A row with no out-of-sample data scores zero on
# that pillar, and a row with data scores at least zero, so fetching can only
# raise a score. A row sitting further below the cutoff for rank PROTECT_TOP
# than the pillar is worth therefore cannot reach that rank however good its
# out-of-sample record, and needs no call.
#
# PILLAR_WEIGHT is deliberately generous while the model shape is undecided:
# over-fetching costs time and nothing else, while under-fetching means
# discovering later that the rows you skipped were the interesting ones. Tighten
# it once the shape is settled.
PROTECT_TOP = 250
PILLAR_WEIGHT = 300

# Below this there is no out-of-sample record worth measuring. Raised from 30 to
# 90 on 2026-09-06 when the model shape settled: the Simplified model puts 35 of
# its 100 points on a single out-of-sample number, and a four-week record is too
# thin a thing to hang that much on. It was also the noisiest duration group by a
# distance. Those rows score zero on the pillar, which is what the model already
# does with missing data everywhere else, and they cannot clear the 365-day tier
# floor in any case.
MIN_OOS_DAYS = 90

# Fields kept from the API's 27. Deliberately wider than any single candidate
# model needs, so settling the model shape does not mean refetching 3,000 rows.
KEEP_STATS = [
    "annualized_rate_of_return",
    "cumulative_return",
    "max_drawdown",
    "standard_deviation",
    "sharpe_ratio",
    "sortino_ratio",
    "calmar_ratio",
    "win_rate",
    "size",
]

EPOCH = dt.date(1970, 1, 1)
PERMANENT_CODES = {"404", "422"}


def epoch_to_date(n):
    return EPOCH + dt.timedelta(days=int(n))


def post(url, body):
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": UA},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        return json.loads(resp.read().decode("utf-8"))


def load_spy():
    """SPY closes by date. The benchmark side of every comparison is computed
    locally and exactly, because data/prices.json already ships SPY back to
    2010 for the Signal Miner."""
    px = json.loads(PRICES.read_text(encoding="utf-8"))
    return px["dates"], px["tickers"]["SPY"]["closes"]


def spy_return(dates, closes, start_iso, end_iso):
    """SPY's return over [start, end], using the first close on or after the
    start and the last on or before the end. Returns None when the span starts
    before the price history does, rather than silently comparing a symphony's
    full span against a shorter slice of SPY."""
    if start_iso < dates[0]:
        return None
    lo = next((i for i, d in enumerate(dates) if d >= start_iso), None)
    hi = None
    for i in range(len(dates) - 1, -1, -1):
        if dates[i] <= end_iso:
            hi = i
            break
    if lo is None or hi is None or hi <= lo:
        return None
    return closes[hi] / closes[lo] - 1.0


def check_window(result, want_start, want_end):
    """Confirm the response really covers the window we asked for.

    Not an equality test on the start date, because the API snaps a start
    forward to the next trading day: a symphony last edited on a Saturday
    legitimately comes back beginning on the Monday. The bound is what matters.
    If `start_date` had been ignored, `first_day` would be the symphony's own
    inception, typically years earlier, so a window of a few days catches that
    decisively while tolerating a long holiday weekend.

    Returns None when the response is good, or a string describing the problem.
    """
    first = result.get("first_day")
    last = result.get("last_market_day")
    if first is None or last is None:
        return "response carries no first_day/last_market_day"
    got_start, got_end = epoch_to_date(first), epoch_to_date(last)
    if got_start < want_start:
        return ("window ignored: got %s, asked for %s (start_date had no effect)"
                % (got_start, want_start))
    if (got_start - want_start).days > 10:
        return "start drifted: got %s, asked for %s" % (got_start, want_start)
    if got_end > want_end:
        return "end overshot: got %s, asked for %s" % (got_end, want_end)
    return None


def curated_ids():
    """Every symphony with a hand-written page on the site.

    These are exempt from the score cutoff below. The cutoff asks whether a row
    could plausibly reach the top of the Leaderboard, which is the right
    question for ranking and the wrong one for the Overfit Check: a curated
    strategy gets written about whatever it scores, and its page is where a
    missing out-of-sample record is most conspicuous. Measured 2026-09-08, 11 of
    the 24 visible curated strategies had no re-run for exactly this reason,
    seven of them with over a year of untouched history sitting unused. The
    exemption costs about a dozen extra calls a week."""
    try:
        rows = json.loads(io.open(STRATEGIES, encoding="utf-8").read())
    except (OSError, ValueError):
        return set()
    return {r["symphony_id"] for r in rows if r.get("symphony_id")}


def select_candidates(pool):
    """The rows worth spending a call on, best first so a run cut short has
    still covered the top of the board."""
    scores, _parts = score_pool(pool, ADVANCED_METRICS)
    ranked = sorted(scores, reverse=True)
    cutoff = ranked[min(PROTECT_TOP, len(ranked)) - 1] - PILLAR_WEIGHT
    curated = curated_ids()
    picked = [(scores[i], e) for i, e in enumerate(pool)
              if (scores[i] >= cutoff or e.get("symphony_id") in curated)
              and e.get("symphony_id")
              and (oos_days(e) or 0) >= MIN_OOS_DAYS]
    picked.sort(key=lambda t: -t[0])
    return [e for _s, e in picked], cutoff


def write_out(store):
    payload = {
        "generated": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "protect_top": PROTECT_TOP,
        "pillar_weight": PILLAR_WEIGHT,
        "min_oos_days": MIN_OOS_DAYS,
        "series": store,
    }
    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    JSON_PATH.write_text(text, encoding="utf-8")
    JS_PATH.write_text(
        "// Out-of-sample statistics, loaded as a script tag so database.html works\n"
        "// with the file:// protocol. To update: run scripts/refresh_oos.py\n"
        "window.OOS_DATA = " + text.rstrip("\n") + ";\n",
        encoding="utf-8",
    )


def main():
    # Symphony names carry emoji and accented characters, and a Windows console
    # defaults to cp1252, so printing a progress line can kill a run that is
    # otherwise working perfectly. Killed one at row 72 of a 300-row smoke test.
    # GitHub's runners are UTF-8 already, which is why refresh_full_database.py
    # has never hit this despite printing the same names.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

    args = sys.argv[1:]
    force = "--force" in args
    args = [a for a in args if a != "--force"]
    limit = int(args[0]) if args else None

    dates, closes = load_spy()
    want_end = dt.date.fromisoformat(dates[-1])   # align both sides on one day

    pool = eligible(load_entries())
    candidates, cutoff = select_candidates(pool)
    print("pool %d, candidates %d (score cutoff %.1f, min OOS %dd), benchmark end %s"
          % (len(pool), len(candidates), cutoff, MIN_OOS_DAYS, want_end))

    store = {}
    if JSON_PATH.exists():
        store = json.loads(JSON_PATH.read_text(encoding="utf-8")).get("series", {})

    def current(e):
        """A stored row is current when it was measured over the window this run
        would ask for. Both ends matter: a new logic edit moves the start, and a
        fresh week of prices moves the end."""
        old = store.get(e["symphony_id"])
        return bool(old
                    and old.get("requested_start") == str(e.get("oos_date"))
                    and old.get("requested_end") == want_end.isoformat())

    due = candidates if force else [e for e in candidates if not current(e)]
    if limit:
        due = due[:limit]
    print("fetching %d of %d candidates%s"
          % (len(due), len(candidates), " (limited)" if limit else ""))

    ok = skipped = failed = 0
    try:
        for i, e in enumerate(due):
            if i:
                time.sleep(API_CALL_DELAY_SECONDS)
            sid = e["symphony_id"]
            want_start = dt.date.fromisoformat(str(e["oos_date"])[:10])
            label = (e.get("name") or sid)[:44]
            print("[%d/%d] %s ... " % (i + 1, len(due), label), end="", flush=True)

            body = dict(BODY)
            body["start_date"] = want_start.isoformat()
            body["end_date"] = want_end.isoformat()
            try:
                res = post("%s/api/v0.1/symphonies/%s/backtest" % (API_BASE, sid), body)
            except urllib.error.HTTPError as err:
                failed += 1
                print("FAILED HTTP %s" % err.code)
                # Permanent failures stay out of the file; a transient one is
                # simply absent and gets picked up by the next run.
                if str(err.code) in PERMANENT_CODES:
                    store.pop(sid, None)
                continue
            except Exception as err:              # noqa: BLE001 (log and move on)
                failed += 1
                print("FAILED %s: %s" % (type(err).__name__, err))
                continue

            problem = check_window(res, want_start, want_end)
            if problem:
                skipped += 1
                print("DISCARDED (%s)" % problem)
                store.pop(sid, None)
                continue

            stats = res.get("stats") or {}
            got_start = epoch_to_date(res["first_day"])
            got_end = epoch_to_date(res["last_market_day"])
            row = {
                "requested_start": want_start.isoformat(),
                "requested_end": want_end.isoformat(),
                "start": got_start.isoformat(),
                "end": got_end.isoformat(),
                "oos_calendar_days": (got_end - got_start).days,
            }
            for f in KEEP_STATS:
                v = stats.get(f)
                row[f] = v if isinstance(v, (int, float)) else None
            # Composer reports max_drawdown unsigned; the database stores it
            # negative, and the Leaderboard scores it "higher is better".
            if row["max_drawdown"] is not None:
                row["max_drawdown"] = -abs(row["max_drawdown"])
            row["spy_return"] = spy_return(dates, closes, row["start"], row["end"])
            if row["spy_return"] is not None and row["cumulative_return"] is not None:
                row["excess_return"] = row["cumulative_return"] - row["spy_return"]
            else:
                row["excess_return"] = None
            store[sid] = row
            ok += 1
            print("OK %dd  ret %+.2f%%  vs SPY %s"
                  % (row["oos_calendar_days"],
                     100 * (row["cumulative_return"] or 0),
                     "n/a" if row["excess_return"] is None
                     else "%+.2fpp" % (100 * row["excess_return"])))

            if (i + 1) % CHECKPOINT_EVERY == 0:
                write_out(store)
                print("  -- checkpoint at %d rows --" % (i + 1))
    finally:
        write_out(store)
        print("\nSaved %d rows to data/oos.json. OK=%d DISCARDED=%d FAILED=%d"
              % (len(store), ok, skipped, failed))


if __name__ == "__main__":
    main()
