# -*- coding: utf-8 -*-
"""Measure the live Leaderboard pool. Manual only, never in CI.

Every number in docs/PRD.md V1.18 comes from this script. It exists so those
numbers can be re-derived rather than trusted, and so the same measurements can
be re-run once the model shape is settled.

It mirrors database.html's scoring engine exactly: the same clamp constant, the
same average-rank tie handling, the same fixed denominators, the same tier cuts,
and since V1.18 both shipped models rather than one. If that engine changes,
ADVANCED_METRICS, SIMPLIFIED_METRICS and CLAMP_Q here must change with it or the
output silently describes a model the site no longer runs.

Read-only. It touches no API and writes no file.

    python scripts/analyze_leaderboard.py
"""
import datetime as dt
import json
import math
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SUMMARY = BASE_DIR / "data" / "database_summary.json"
PRICES = BASE_DIR / "data" / "prices.json"
OOS = BASE_DIR / "data" / "oos.json"

# Mirrors database.html. CLAMP_Q 0.14 means only the top ~14% of a metric earns
# full marks and the bottom ~14% earns zero, with a straight ramp between.
CLAMP_Q = 0.14
ADVANCED_METRICS = [
    ("arr", 99, True, "annualized_rate_of_return"),
    ("max_dd", 98, True, "max_drawdown"),
    ("backtest", 97, True, "backtest_days"),
    ("calmar", 96, True, "calmar_ratio"),
    ("sharpe", 85, True, "sharpe_ratio"),
    ("sortino", 75, True, "sortino_ratio"),
    ("t1y", 64, True, "trailing_one_year_return"),
    ("median", 59, True, "median"),
    ("win_rate", 48, True, "win_rate"),
    ("top1day", 43, False, "top_one_day_contribution"),
    ("skew", 37, True, "skewness"),
    ("t3m", 32, True, "trailing_three_month_return"),
    ("top5pct", 32, False, "top_five_percent_day_contribution"),
    ("tail_ratio", 27, True, "tail_ratio"),
    ("oos", 25, True, "@oos_days"),
    ("std_dev", 25, False, "standard_deviation"),
    ("top10pct", 21, False, "top_ten_percent_day_contribution"),
    ("t1m", 16, True, "trailing_one_month_return"),
    ("t2w", 11, True, "trailing_two_week_return"),
    ("kurtosis", 10, False, "kurtosis"),
]

# The Simplified model (V1.18). Five metrics, 100 points, 35 of them on the one
# figure a backtest cannot flatter. The fifth element is the peer-group function:
# a metric that carries one is percentiled inside its group rather than across
# the pool, and a row whose group is None is left out of the ranking entirely.
OOS_SERIES = json.loads(OOS.read_text(encoding="utf-8"))["series"] if OOS.exists() else {}
OOS_TIER_FLOOR_DAYS = 365


def oos_group(e):
    r = OOS_SERIES.get(e.get("symphony_id"))
    d = r and r.get("oos_calendar_days")
    if not isinstance(d, (int, float)):
        return None
    return "730+" if d >= 730 else ("365-729" if d >= 365 else "90-364")


SIMPLIFIED_METRICS = [
    ("oos_excess", 35, True, "@oos_excess", oos_group),
    ("arr", 25, True, "annualized_rate_of_return"),
    ("backtest", 15, True, "backtest_days"),
    ("max_dd", 15, True, "max_drawdown"),
    ("std_dev", 10, False, "standard_deviation"),
]
TIER_CUTS = [("S+", 0.0025), ("S", 0.10), ("A", 0.20), ("B", 0.50), ("C", 0.75)]

# The trailing windows, longest first, with the calendar days of OOS history a
# row needs before that window sits entirely after its last logic edit, and the
# trading days SPY is measured over to match it.
WINDOWS = [
    ("1y", "trailing_one_year_return", 365, 252),
    ("3m", "trailing_three_month_return", 90, 63),
    ("1m", "trailing_one_month_return", 30, 21),
    ("2w", "trailing_two_week_return", 14, 10),
]

TIER_CUTS_ORDER = {label: i for i, (label, _q) in enumerate(TIER_CUTS)}
TIER_CUTS_ORDER["F"] = len(TIER_CUTS)

TODAY = dt.date.today()


def load_entries():
    d = json.loads(SUMMARY.read_text(encoding="utf-8"))
    fields = d["fields"]
    return [dict(zip(fields, row)) for row in d["rows"]]


def oos_days(e):
    """Days since the last logic edit, matching oosDaysValue in database.html."""
    raw = e.get("oos_date")
    if not raw:
        return None
    try:
        return (TODAY - dt.date.fromisoformat(str(raw).split("[")[0][:10])).days
    except ValueError:
        return None


def eligible(entries):
    """The Leaderboard's pool: unflagged, and refreshed at least once."""
    return [e for e in entries
            if e.get("flag") not in ("caution", "excluded", "duplicate")
            and isinstance(e.get("sharpe_ratio"), (int, float))]


def value_of(e, field):
    if field == "@oos_days":
        return oos_days(e)
    if field == "@oos_excess":
        r = OOS_SERIES.get(e.get("symphony_id"))
        v = r and r.get("excess_return")
        return v if isinstance(v, (int, float)) else None
    v = e.get(field)
    return v if isinstance(v, (int, float)) else None


def points(pct, cap):
    return max(0.0, min(cap, cap * (pct - CLAMP_Q) / (1 - 2 * CLAMP_Q)))


def score_pool(pool, metrics):
    """Returns (scores, parts). Ties take the average rank, exactly as the page
    does, so a run of identical values all score the same rather than being
    ordered arbitrarily by input position."""
    parts = [{} for _ in pool]
    for m in metrics:
        key, cap, higher, field = m[0], m[1], m[2], m[3]
        group_fn = m[4] if len(m) > 4 else None
        buckets = {}
        for i, e in enumerate(pool):
            v = value_of(e, field)
            if v is None:
                continue
            g = group_fn(e) if group_fn else ""
            if g is None:
                continue
            buckets.setdefault(g, []).append((i, v))
        for vals in buckets.values():
            n = len(vals)
            if not n:
                continue
            vals.sort(key=lambda t: t[1])
            i = 0
            while i < n:
                j = i
                while j + 1 < n and vals[j + 1][1] == vals[i][1]:
                    j += 1
                pct = ((i + j) / 2.0) / (n - 1) if n > 1 else 0.5
                if not higher:
                    pct = 1 - pct
                p = points(pct, cap)
                for k in range(i, j + 1):
                    parts[vals[k][0]][key] = p
                i = j + 1
    # Unrounded, matching database.html: the page ranks on the full precision
    # and rounds only for display. Rounding before the sort invents ties.
    scores = [sum(p.values()) for p in parts]
    return scores, parts


def tiers_for(pool, scores, floor=False):
    """Tier label per pool index, mirroring computeTiers in database.html: cuts
    by rank with ties rounding up, then the out-of-sample floor demoting S+ and
    S to A without touching rank."""
    order = sorted(range(len(pool)), key=lambda i: -scores[i])
    n = len(order)
    cuts = [max(1, round(q * n)) for _label, q in TIER_CUTS]
    for k in range(len(cuts)):
        j = min(cuts[k], n) - 1
        boundary = scores[order[j]]
        while j + 1 < n and scores[order[j + 1]] == boundary:
            j += 1
        cuts[k] = j + 1
        if k > 0 and cuts[k] < cuts[k - 1]:
            cuts[k] = cuts[k - 1]
    out = {}
    ci = 0
    for r, i in enumerate(order):
        while ci < len(cuts) and r >= cuts[ci]:
            ci += 1
        t = TIER_CUTS[ci][0] if ci < len(TIER_CUTS) else "F"
        if floor and t in ("S+", "S"):
            d = oos_days(pool[i])
            if d is None or d < OOS_TIER_FLOOR_DAYS:
                t = "A"
        out[i] = t
    return order, out


def quantile(sorted_xs, q):
    return sorted_xs[min(len(sorted_xs) - 1, int(q * len(sorted_xs)))]


def spearman(a, b):
    """Rank correlation over the rows where both values are present."""
    pairs = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    if len(pairs) < 30:
        return float("nan")

    def ranked(xs):
        idx = sorted(range(len(xs)), key=lambda i: xs[i])
        out = [0.0] * len(xs)
        i = 0
        while i < len(idx):
            j = i
            while j + 1 < len(idx) and xs[idx[j + 1]] == xs[idx[i]]:
                j += 1
            avg = (i + j) / 2.0
            for k in range(i, j + 1):
                out[idx[k]] = avg
            i = j + 1
        return out

    ra, rb = ranked([p[0] for p in pairs]), ranked([p[1] for p in pairs])
    ma, mb = sum(ra) / len(ra), sum(rb) / len(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    da = math.sqrt(sum((x - ma) ** 2 for x in ra))
    db = math.sqrt(sum((y - mb) ** 2 for y in rb))
    return num / (da * db) if da and db else float("nan")


def section(title):
    print("\n" + title)
    print("-" * len(title))


def main():
    pool = eligible(load_entries())
    scores, _parts = score_pool(pool, ADVANCED_METRICS)
    total = sum(m[1] for m in ADVANCED_METRICS)
    order = sorted(range(len(pool)), key=lambda i: -scores[i])
    ranked = sorted(scores, reverse=True)
    print("eligible pool: %d rows, scored out of %d, as of %s"
          % (len(pool), total, TODAY))

    # ---- how long has each row been out of sample ----
    section("OOS duration")
    for label, lo, hi in [("365+", 365, 10 ** 9), ("90-364", 90, 365),
                          ("30-89", 30, 90), ("under 30", 0, 30)]:
        c = sum(1 for e in pool
                if oos_days(e) is not None and lo <= oos_days(e) < hi)
        print("  %-9s %5d  %5.1f%%" % (label, c, 100.0 * c / len(pool)))
    missing = sum(1 for e in pool if oos_days(e) is None)
    print("  %-9s %5d  %5.1f%%" % ("no date", missing, 100.0 * missing / len(pool)))

    # ---- out-of-sample performance against SPY ----
    # Uses the longest trailing window that fits entirely inside the row's OOS
    # period. Superseded for scoring by the windowed API backtest (PRD V1.18),
    # but kept here because it needs no API call and it is what established that
    # the median symphony loses to SPY out of sample.
    px = json.loads(PRICES.read_text(encoding="utf-8"))
    spy = px["tickers"]["SPY"]["closes"]
    # The database stores returns as FRACTIONS, not percents. Keep SPY in the
    # same units or every comparison below is wrong by two orders of magnitude.
    spy_ret = {k: spy[-1] / spy[-1 - td] - 1.0 for k, _f, _cal, td in WINDOWS}

    section("OOS performance against SPY, by longest fully-OOS trailing window")
    print("  SPY closes through %s" % px["dates"][-1])
    print("  %-6s %6s %9s %11s %11s %11s %7s"
          % ("window", "rows", "SPY", "median", "excess p10", "excess p90", "beat"))
    covered = 0
    for k, field, cal, _td in WINDOWS:
        group = [e for e in pool
                 if (oos_days(e) or -1) >= cal
                 and isinstance(e.get(field), (int, float))
                 and not any((oos_days(e) or -1) >= c2
                             for _k2, _f2, c2, _t2 in WINDOWS if c2 > cal)]
        if not group:
            continue
        covered += len(group)
        excess = sorted(e[field] - spy_ret[k] for e in group)
        med = quantile(sorted(e[field] for e in group), 0.5)
        beat = 100.0 * sum(1 for x in excess if x > 0) / len(group)
        print("  %-6s %6d %+8.2f%% %+10.2f%% %+10.2f%% %+10.2f%% %6.1f%%"
              % (k, len(group), 100 * spy_ret[k], 100 * med,
                 100 * quantile(excess, 0.10), 100 * quantile(excess, 0.90), beat))
    print("  covered: %d of %d rows (%.1f%%)"
          % (covered, len(pool), 100.0 * covered / len(pool)))

    # ---- redundancy: are we paying for the same ordering more than once ----
    section("Most redundant metric pairs (Spearman)")
    cols = {key: [value_of(e, field) for e in pool]
            for key, _cap, _hi, field in ADVANCED_METRICS}
    keys = [m[0] for m in ADVANCED_METRICS]
    pairs = []
    for a in range(len(keys)):
        for b in range(a + 1, len(keys)):
            c = spearman(cols[keys[a]], cols[keys[b]])
            if c == c:
                pairs.append((abs(c), c, keys[a], keys[b]))
    for _ac, c, x, y in sorted(pairs, reverse=True)[:12]:
        print("  %-11s %-11s %+.3f" % (x, y, c))

    # ---- does each metric's weight match its influence ----
    # Drop one metric, re-score, and see how far the top 500 moves. A metric
    # with a large cap and a small movement is buying an ordering the model
    # already had from somewhere else.
    section("Drop-one sensitivity: mean absolute rank move in the top 500")
    base_rank = {j: r for r, j in enumerate(order)}
    top500 = order[:500]
    rows = []
    for key, cap, _hi, _field in ADVANCED_METRICS:
        s2, _ = score_pool(pool, [m for m in ADVANCED_METRICS if m[0] != key])
        o2 = sorted(range(len(pool)), key=lambda i: -s2[i])
        r2 = {j: r for r, j in enumerate(o2)}
        move = sum(abs(r2[j] - base_rank[j]) for j in top500) / len(top500)
        rows.append((move, key, cap, len(set(top500) - set(o2[:500]))))
    for move, key, cap, churn in sorted(rows, reverse=True):
        print("  %-11s cap %3d  move %7.1f  %3d of 500 leave the top 500"
              % (key, cap, move, churn))

    # ---- how large must the OOS candidate set be ----
    # A row with no OOS data scores zero on the OOS pillar, and a row with data
    # scores at least zero, so fetching can only raise a score. A row further
    # than the pillar's full weight below the cutoff for rank D therefore cannot
    # reach rank D however good its OOS record is, and needs no API call.
    section("Candidate set sizing for the OOS refresh (PRD V1.18)")
    print("  %-16s %-10s %9s %11s %8s"
          % ("protect top", "pillar", "cutoff", "candidates", "share"))
    for depth in (100, 250, 500):
        for weight in (150, 250):
            cut = ranked[depth - 1] - weight
            c = sum(1 for x in scores if x >= cut)
            print("  %-16d %-10d %9.1f %11d %7.1f%%"
                  % (depth, weight, cut, c, 100.0 * c / len(pool)))

    # ---- the Simplified model as shipped (V1.18) ----
    section("Simplified model (V1.18): coverage, ties, tiers, and disagreement")
    if not OOS_SERIES:
        print("  data/oos.json is missing or empty, skipping")
    else:
        s_scores, s_parts = score_pool(pool, SIMPLIFIED_METRICS)
        s_order, s_tier = tiers_for(pool, s_scores, floor=True)
        a_order, a_tier = tiers_for(pool, scores, floor=False)
        s_total = sum(m[1] for m in SIMPLIFIED_METRICS)

        have = sum(1 for e in pool if e.get("symphony_id") in OOS_SERIES)
        print("  out-of-sample rows: %d of %d in the pool (%.1f%%), scored out of %d"
              % (have, len(pool), 100.0 * have / len(pool), s_total))
        groups = Counter(oos_group(e) for e in pool)
        for g in ("90-364", "365-729", "730+", None):
            print("    group %-8s %5d" % (g if g else "none", groups.get(g, 0)))

        # The open question from the design session: does a five-metric model
        # leave the top of the table full of shared scores?
        top100 = [s_scores[i] for i in s_order[:100]]
        dupes = sum(c - 1 for c in Counter(top100).values() if c > 1)
        print("  ties in the top 100: %d rows share a rounded score with another"
              % dupes)
        top500 = [s_scores[i] for i in s_order[:500]]
        print("  ties in the top 500: %d"
              % sum(c - 1 for c in Counter(top500).values() if c > 1))

        # What the 365-day floor actually costs.
        blocked = sum(1 for r, i in enumerate(s_order[:max(1, round(0.10 * len(pool)))])
                      if s_tier[i] == "A")
        print("  demoted to A by the %d-day floor, inside the top 10%%: %d"
              % (OOS_TIER_FLOOR_DAYS, blocked))
        print("  tier counts: %s"
              % ", ".join("%s %d" % (t, c) for t, c in
                          sorted(Counter(s_tier.values()).items(),
                                 key=lambda kv: TIER_CUTS_ORDER.get(kv[0], 9))))

        # How much are the two models actually saying differently?
        s_rank = {i: r for r, i in enumerate(s_order)}
        a_rank = {i: r for r, i in enumerate(a_order)}
        rel = [i for i in range(len(pool))
               if min(s_rank[i], a_rank[i]) < 500]
        agree = sum(1 for i in rel if abs(a_rank[i] - s_rank[i]) <= 50)
        print("  top-500 union: %d rows, %d within 50 places of each other (%.0f%%)"
              % (len(rel), agree, 100.0 * agree / max(1, len(rel))))
        print("  rank correlation over the whole pool: %+.3f"
              % spearman([s_scores[i] for i in range(len(pool))],
                         [scores[i] for i in range(len(pool))]))

        section("Simplified top 20")
        for r, i in enumerate(s_order[:20]):
            e = pool[i]
            row = OOS_SERIES.get(e.get("symphony_id")) or {}
            ex = row.get("excess_return")
            print("  %-3d %-6.1f %-3s %5sd %9s  %s"
                  % (r + 1, s_scores[i], s_tier[i],
                     row.get("oos_calendar_days", "-"),
                     ("%+.1fpp" % (100 * ex)) if isinstance(ex, float) else "no data",
                     (e.get("name") or "")[:44]))

    # ---- the rows anyone will actually look at ----
    section("Current top 20")
    n = len(pool)
    cuts = [(label, max(1, round(q * n))) for label, q in TIER_CUTS]
    for r, i in enumerate(order[:20]):
        e = pool[i]
        tier = next((label for label, c in cuts if r < c), "F")
        od = oos_days(e)
        print("  %-3d %-6.1f %-3s %5s  %s"
              % (r + 1, scores[i], tier, od if od is not None else "-",
                 (e.get("name") or "")[:52]))


if __name__ == "__main__":
    main()
