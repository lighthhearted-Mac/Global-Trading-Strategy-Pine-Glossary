# -*- coding: utf-8 -*-
"""Derive data/overfit.json (+ .js twin) for the Overfit Check page (V2.4).

Three things come out of this: the population findings the page leads with, the
"par" curve the Overfit Score is read against, and a compact per-symphony index
so a pasted URL or ID can be looked up in the browser without shipping the 19MB
database.

**Why two population cohorts and not one.** They measure different things and
the page reports both side by side, per owner decision 2026-09-07:

  trailing  Every symphony whose logic has gone at least a year unedited, with
            its backtested annual return compared against the actual return of
            the last twelve months. Unbiased: it includes the whole database,
            weak rows and all. But the backtest window still overlaps the year
            being measured, so it is out-of-sample with respect to *editing*
            rather than a clean holdout.

  true_oos  The rows in data/oos.json, each re-backtested over its own untouched
            period alone, so the window genuinely excludes everything the author
            could have fitted to. Strictly better per row, and **biased as a
            population**: those rows were selected by in-sample score for the
            Leaderboard's candidate set, so this cohort is roughly the stronger
            half of the database. Any figure from it describes that half, not
            the database, and the page must say so.

**THE FITTED-ERA SPLIT, added 2026-09-08.** The full backtest RUNS THROUGH
TODAY, so it already contains the out-of-sample window inside it. Comparing the
two directly compares a period against a superset of itself, which drags them
together and understates the degradation. The full window is the fitted era
chained onto the untouched era, so the fitted era is recoverable by arithmetic
rather than by another 3,000 API calls:

    (1 + cum_full) = (1 + cum_fitted) * (1 + cum_oos)
    years          = ln(1 + cumulative_return) / ln(1 + annualized_rate_of_return)

Window length comes from that log ratio and NOT from `backtest_days`, which is
in *trading* days (1704 = 6.77 years) and would need a conversion factor that is
itself an assumption. Verified to 3.55e-15 log points against the stored full
cumulative, on 3,236 of 3,257 rows.

**THE OVERFIT SCORE (compounding scale since the 2026-10-15 audit).**
`100 * (1 - ln(1 + delivered) / ln(1 + fitted))`, clamped to 0..100, where both
terms are annualized rates over their own eras. The ratio of simple annual
rates (the pre-audit definition, 100 minus Pardo's walk-forward efficiency)
exaggerates decay for extreme backtests and piled the top decile against 100;
the ratio of compounding rates does not. It is deliberately
**one measured quantity with no weights**: docs/PRD.md rules out a composite
score because its weights would be unfalsifiable and would invite the very
optimisation the page exists to detect. A single ratio has no weights to tune,
is reversible (the reader can recover the inputs, which are printed beside it),
and can be checked against outcomes.

**THE VERDICT IS A CONE TEST AGAINST THE SYMPHONY'S OWN BACKTEST** (docs/PRD.md,
"Overfit Method Audit"). Par, a sliding median of other symphonies' scores, was
retired as the yardstick: on our data the distance from par was ~86% noise, and
par excused the very reversion the literature defines as overfitting. The call
now uses no population data and no weights:

    kept  = ln(1 + live) / ln(1 + fitted)
    range = kept +/- 1.96 * (live_sd / sqrt(live_years)) / ln(1 + fitted)
    Fell short   whole range below 100%
    Beat it      whole range above 100%
    Too early    range covers both 0% and 100%
    Consistent   otherwise

The population appears only as base rates (what share of backtests this size
fell short), which warn rather than excuse, and as individual warning signs,
never combined.

**Costs are already inside the backtest.** `total_costs` is reported by the same
backtest that produced `annualized_rate_of_return`, and refresh_full_database.py
requests it with slippage and both fee flags on. So the in-sample figure is net
of modelled costs, and the turnover result below is not simply "the backtest
ignored trading costs". Real slippage on a high-turnover strategy can still
exceed the model, which is why the page reports an association and not a cause.

Read-only against the database. Writes only its two output files.

    python scripts/build_overfit.py
"""
import datetime as dt
import io
import json
import math
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE = BASE_DIR / "data" / "database.json"
OOS = BASE_DIR / "data" / "oos.json"
JSON_PATH = BASE_DIR / "data" / "overfit.json"
JS_PATH = BASE_DIR / "data" / "overfit.js"
PRICES_PATH = BASE_DIR / "data" / "prices.json"

NOISE_FLAGS = ("caution", "excluded", "duplicate")
MIN_OOS_DAYS = 365          # a year unedited, matching the spec's cohort
QUINTILES = 5
MIN_FITTED_YEARS = 0.5      # below this, annualizing a stub window explodes
MIN_LIVE_TRADING_DAYS = 63  # ~3 months: the floor under the cone test
CASH_LIKE_SD = 0.03         # live volatility below this is a cash proxy, not a strategy
BASE_RATE_MIN_YEARS = 1.0   # base rates use symphonies with a year or more live
ALIGN_DAYS = 7              # OOS end vs backtest end, for the moment decomposition
Z95 = 1.96
PRICES = None               # loaded in main()
CEILING_MIN_FITTED_YEARS = 5.0   # removes short-window noise from the ceiling

TODAY = dt.date.today()


def num(v):
    return v if isinstance(v, (int, float)) else None


def oos_days(row):
    raw = row.get("oos_date")
    if not raw:
        return None
    try:
        return (TODAY - dt.date.fromisoformat(str(raw).split("[")[0][:10])).days
    except ValueError:
        return None


def median(xs):
    xs = sorted(xs)
    n = len(xs)
    if not n:
        return None
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2.0


def r4(v):
    """Round for transport. Four decimals on a return fraction is a hundredth of
    a percentage point, far finer than anything the page displays."""
    return None if v is None else round(v, 4)


def load(path):
    return json.loads(io.open(path, encoding="utf-8").read())


def share(rows, pred):
    return round(100.0 * sum(1 for r in rows if pred(r)) / len(rows), 1) if rows else None


def years_of(cum, arr):
    """Window length implied by a cumulative return and its annualized rate.

    Preferred over backtest_days, which is in trading days and would need an
    assumed conversion factor."""
    if cum is None or arr is None or cum <= -1 or arr <= -1 or arr == 0:
        return None
    try:
        return math.log1p(cum) / math.log1p(arr)
    except ValueError:
        return None


def fitted_era(row, o):
    """(fitted_arr, fitted_years) for the era the author could tune against, or
    None when the split cannot be taken honestly."""
    cf, af = num(row.get("cumulative_return")), num(row.get("annualized_rate_of_return"))
    co, ao = num(o.get("cumulative_return")), num(o.get("annualized_rate_of_return"))
    yf, yo = years_of(cf, af), years_of(co, ao)
    if None in (cf, af, co, ao, yf, yo):
        return None
    yi = yf - yo
    if yi < MIN_FITTED_YEARS:
        return None
    ratio = (1.0 + cf) / (1.0 + co)
    if ratio <= 0:
        return None
    return (ratio ** (1.0 / yi) - 1.0, yi)


def overfit_score(delivered, fitted):
    """How much of the fitted era's compounding rate failed to survive, 0..100.

    One quantity, no weights, no population input. A negative fitted rate has no
    promise to break, so it is not scored."""
    if delivered is None or fitted is None or fitted <= 0 or delivered <= -1:
        return None
    return max(0.0, min(100.0, 100.0 * (1.0 - math.log1p(delivered) / math.log1p(fitted))))


def live_years(o):
    n = num(o.get("size"))
    return n / 252.0 if n else None


def cone(delivered, fitted, sd, years, trading_days):
    """(label, lo, mid, hi) on the share of the compounding rate kept, or
    (reason, None, None, None) when no call can be made. Mirrors coneCall() in
    overfit.html exactly; change both or neither."""
    if None in (delivered, fitted, sd, years, trading_days) or fitted <= 0 or delivered <= -1:
        return ("unscored", None, None, None)
    if trading_days < MIN_LIVE_TRADING_DAYS:
        return ("short", None, None, None)
    if sd < CASH_LIKE_SD:
        return ("cash", None, None, None)
    gi, go = math.log1p(fitted), math.log1p(delivered)
    se = sd / math.sqrt(years)
    lo, mid, hi = (go - Z95 * se) / gi, go / gi, (go + Z95 * se) / gi
    if hi < 1:
        lab = "fell_short"
    elif lo > 1:
        lab = "beat"
    elif lo <= 0:
        lab = "too_early"
    else:
        lab = "consistent"
    return (lab, lo, mid, hi)


def spy_rate(d0, d1):
    """SPY annualized rate between two ISO dates, None outside price coverage."""
    if PRICES is None or not d0 or not d1:
        return None
    dates, closes = PRICES
    if d0 < dates[0] or d1 > dates[-1]:
        return None
    import bisect
    i0 = bisect.bisect_left(dates, d0)
    i1 = bisect.bisect_right(dates, d1) - 1
    if i1 <= i0:
        return None
    yrs = (dt.date.fromisoformat(dates[i1]) - dt.date.fromisoformat(dates[i0])).days / 365.25
    if yrs < 0.25:
        return None
    return (closes[i1] / closes[i0]) ** (1.0 / yrs) - 1.0


def fitted_sharpe(r, o):
    """Fitted-era Sharpe by moment decomposition (docs/PRD.md, Overfit Method
    Audit). Composer's Sharpe is mean_daily * 252 / sd_annual, no risk-free
    rate. Only taken where the OOS re-run ends within ALIGN_DAYS of the full
    backtest, so the two describe the same days."""
    nf, mf, sf = num(r.get("backtest_days")), num(r.get("mean")), num(r.get("standard_deviation"))
    no, sro, so = num(o.get("size")), num(o.get("sharpe_ratio")), num(o.get("standard_deviation"))
    rd, oe = r.get("refresh_date"), o.get("end")
    if None in (nf, mf, sf, no, sro, so) or not rd or not oe or no <= 0:
        return None
    try:
        gap = abs((dt.date.fromisoformat(rd[:10]) - dt.date.fromisoformat(oe[:10])).days)
    except ValueError:
        return None
    ni = nf - no
    if gap > ALIGN_DAYS or ni < 126:
        return None
    sfd, sod = sf / math.sqrt(252), so / math.sqrt(252)
    mo = sro * so / 252.0
    mi = (nf * mf - no * mo) / ni
    vi = (nf * (sfd ** 2 + mf ** 2) - no * (sod ** 2 + mo ** 2)) / ni - mi ** 2
    if vi <= 0:
        return None
    return mi / math.sqrt(vi) * math.sqrt(252)


def ranks(v):
    o = sorted(range(len(v)), key=lambda i: v[i])
    out = [0.0] * len(v)
    i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]:
            j += 1
        for k in range(i, j + 1):
            out[o[k]] = (i + j) / 2.0
        i = j + 1
    return out


def spearman(x, y):
    pr = [(a, b) for a, b in zip(x, y) if a is not None and b is not None]
    if len(pr) < 30:
        return None
    a, b = ranks([p[0] for p in pr]), ranks([p[1] for p in pr])
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    sab = sum((u - ma) * (w - mb) for u, w in zip(a, b))
    sa = math.sqrt(sum((u - ma) ** 2 for u in a))
    sb = math.sqrt(sum((w - mb) ** 2 for w in b))
    return round(sab / (sa * sb), 2) if sa and sb else None


def trailing_cohort(usable):
    """Backtested annual return against the actual last twelve months, for every
    symphony whose logic has gone a year untouched."""
    c = [r for r in usable
         if (oos_days(r) or 0) >= MIN_OOS_DAYS
         and num(r.get("trailing_one_year_return")) is not None]
    arr = "annualized_rate_of_return"
    t1y = "trailing_one_year_return"
    return c, {
        "n": len(c),
        "median_backtest": r4(median([r[arr] for r in c])),
        "median_actual": r4(median([r[t1y] for r in c])),
        "delivered_full": share(c, lambda r: r[t1y] >= r[arr]),
        "delivered_half": share(c, lambda r: r[t1y] >= 0.5 * r[arr]),
        "positive": share(c, lambda r: r[t1y] > 0),
    }


def true_oos_cohort(usable, series):
    """The same comparison against a real out-of-sample backtest."""
    arr = "annualized_rate_of_return"
    pairs = [(r, series[r["symphony_id"]]) for r in usable if r["symphony_id"] in series]
    pairs = [(r, o) for r, o in pairs if num(o.get(arr)) is not None]
    return pairs, {
        "n": len(pairs),
        "median_backtest": r4(median([r[arr] for r, _o in pairs])),
        "median_actual": r4(median([o[arr] for _r, o in pairs])),
        "delivered_full": share(pairs, lambda p: p[1][arr] >= p[0][arr]),
        "delivered_half": share(pairs, lambda p: p[1][arr] >= 0.5 * p[0][arr]),
        "positive": share(pairs, lambda p: p[1][arr] > 0),
        "beat_spy": share(pairs, lambda p: (num(p[1].get("excess_return")) or 0) > 0),
        "median_days": median([o.get("oos_calendar_days") or 0 for _r, o in pairs]),
    }


def split_cohort(usable, series):
    """Every row where the fitted era can be recovered, with its score."""
    out = []
    for r in usable:
        o = series.get(r.get("symphony_id"))
        if not o:
            continue
        fe = fitted_era(r, o)
        ao = num(o.get("annualized_rate_of_return"))
        if fe is None or ao is None:
            continue
        fitted, fyears = fe
        if fitted <= 0:
            continue
        sd, yrs, tdays = num(o.get("standard_deviation")), live_years(o), num(o.get("size"))
        spy_live = spy_rate(o.get("start"), o.get("end"))
        out.append({
            "row": r, "oos": o, "fitted": fitted, "fitted_years": fyears,
            "delivered": ao, "score": overfit_score(ao, fitted),
            "cone": cone(ao, fitted, sd, yrs, tdays), "live_years": yrs,
            "excess_ann": (ao - spy_live) if spy_live is not None else None,
            "signs": signs_of(r, o, fyears),
        })
    out.sort(key=lambda x: x["fitted"])
    return out


SIGNS = (
    # key, label, direction text. Shown one at a time on the page, never combined.
    ("fitted_sharpe", "Backtest Sharpe ratio"),
    ("turnover", "Annualized turnover"),
    ("universe", "Tickers it can hold"),
    ("fitted_years", "Backtest length (years)"),
)


def signs_of(r, o, fyears):
    h = r.get("last_market_days_holdings")
    t = num(r.get("annualized_turnover"))
    fs = fitted_sharpe(r, o) if o else None
    return {
        "fitted_sharpe": round(fs, 2) if fs is not None else None,
        "turnover": round(t, 1) if t is not None else None,
        "universe": len(h) if isinstance(h, dict) and h else None,
        "fitted_years": round(fyears, 2) if fyears is not None else None,
    }


def fifths(rows, key):
    """Fifths of `rows` by key, each with the share that fell short of their own
    backtest and the median share kept. Rows need a decisive-capable cone and a
    year or more live, so a base rate is not diluted by "too early"."""
    c = sorted((x for x in rows if key(x) is not None), key=key)
    n = len(c)
    out, bounds = [], []
    for q in range(QUINTILES):
        g = c[q * n // QUINTILES:(q + 1) * n // QUINTILES]
        if not g:
            continue
        if q < QUINTILES - 1:
            bounds.append(r4(key(g[-1])))
        out.append({
            "n": len(g), "lo": r4(key(g[0])), "hi": r4(key(g[-1])),
            "fell_short": share(g, lambda x: x["cone"][0] == "fell_short"),
            "median_kept": r4(median([x["cone"][2] for x in g])),
        })
    return {"bounds": bounds, "fifths": out, "n": n}


def base_rate_rows(split):
    return [x for x in split
            if x["cone"][2] is not None and (x["live_years"] or 0) >= BASE_RATE_MIN_YEARS]


def base_rates(split):
    """What par became: of backtests this size, how many fell short of their own
    promise. A prior that warns, not a yardstick that excuses."""
    return fifths(base_rate_rows(split), lambda x: x["fitted"])


def sign_rates(split):
    rows = base_rate_rows(split)
    return {k: dict(fifths(rows, lambda x, k=k: x["signs"][k]), label=lab) for k, lab in SIGNS}


def verdict_mix(split):
    rows = [x for x in split if x["cone"][2] is not None]
    labs = ("fell_short", "consistent", "too_early", "beat")
    return dict({l: share(rows, lambda x, l=l: x["cone"][0] == l) for l in labs}, n=len(rows))


def caveat_checks(split):
    """Figures the page's caveats quote, computed every build so they cannot go
    stale the way the hard-coded +0.93 and -0.56 did."""
    return {
        "score_vs_fitted": spearman([x["score"] for x in split], [x["fitted"] for x in split]),
        "score_vs_excess": spearman([x["score"] for x in split], [x["excess_ann"] for x in split]),
    }


def score_distribution(split):
    s = sorted(x["score"] for x in split)
    n = len(s)
    if not n:
        return {}
    q = lambda p: round(s[min(n - 1, int(p / 100.0 * n))], 1)
    return {
        "n": n, "p10": q(10), "p25": q(25), "p50": q(50), "p75": q(75), "p90": q(90),
        "at_zero": round(100.0 * sum(1 for x in s if x <= 0) / n, 1),
        "at_hundred": round(100.0 * sum(1 for x in s if x >= 100) / n, 1),
    }


def ceiling_table(split):
    """Median untouched return by fitted-rate decile, restricted to long fitted
    windows so short-window noise cannot drive it.

    The finding: a better backtest predicts a better future right up to roughly
    +240% a year, and above that it reverses, with the top decile delivering
    less than the most modest one."""
    long = [x for x in split if x["fitted_years"] >= CEILING_MIN_FITTED_YEARS]
    n = len(long)
    if n < 100:
        return {"n": 0, "bins": [], "min_fitted_years": CEILING_MIN_FITTED_YEARS}
    bins = []
    for d in range(10):
        g = long[d * n // 10:(d + 1) * n // 10]
        if not g:
            continue
        bins.append({
            "fitted": r4(median([x["fitted"] for x in g])),
            "delivered": r4(median([x["delivered"] for x in g])),
            "n": len(g),
        })
    peak = max(bins, key=lambda b: b["delivered"]) if bins else None
    return {
        "n": n, "bins": bins,
        "min_fitted_years": CEILING_MIN_FITTED_YEARS,
        "peak_fitted": peak["fitted"] if peak else None,
        "peak_delivered": peak["delivered"] if peak else None,
        "top_fitted": bins[-1]["fitted"] if bins else None,
        "top_delivered": bins[-1]["delivered"] if bins else None,
        "bottom_fitted": bins[0]["fitted"] if bins else None,
        "bottom_delivered": bins[0]["delivered"] if bins else None,
    }


def turnover_table(cohort):
    """Quintiles of annualized turnover against how much of the backtest
    survived. The strongest predictor in the database, and the one nobody
    reaches for when asked about overfitting."""
    c = [r for r in cohort if num(r.get("annualized_turnover")) is not None]
    c.sort(key=lambda r: r["annualized_turnover"])
    n = len(c)
    arr, t1y = "annualized_rate_of_return", "trailing_one_year_return"
    out, bounds = [], []
    for q in range(QUINTILES):
        g = c[q * n // QUINTILES:(q + 1) * n // QUINTILES]
        if not g:
            continue
        if q < QUINTILES - 1:
            bounds.append(round(g[-1]["annualized_turnover"], 1))
        out.append({
            "n": len(g),
            "lo": round(g[0]["annualized_turnover"], 1),
            "hi": round(g[-1]["annualized_turnover"], 1),
            "median_backtest": r4(median([r[arr] for r in g])),
            "median_actual": r4(median([r[t1y] for r in g])),
            "median_gap": r4(median([r[t1y] - r[arr] for r in g])),
        })
    return {"bounds": bounds, "quintiles": out, "n": n}


def build_index(usable, series):
    """Columnar, because 6,700 symphony ids as JSON object keys cost more than
    every number attached to them. Parallel arrays, one entry per id, nulls
    where a field is missing. The page rebuilds a Map on load.

    Names are carried despite costing more than every other column combined
    (194KB gzipped without them, 289KB with). Without a name the result is a
    wall of numbers about an opaque 20-character id, and the reader has no way
    to tell whether the thing they pasted resolved to the thing they meant."""
    cols = {k: [] for k in (
        "ids", "names", "backtest_arr", "trailing_year", "oos_days", "turnover",
        "true_oos_arr", "true_oos_excess", "true_oos_days", "true_oos_cumulative",
        "true_oos_spy", "fitted_arr", "fitted_years", "score",
        "oos_sd", "oos_trading_days", "spy_fitted", "spy_live",
        "fitted_sharpe", "universe")}
    for r in usable:
        sid = r.get("symphony_id")
        if not sid:
            continue
        o = series.get(sid) or {}
        cols["ids"].append(sid)
        cols["names"].append(r.get("name") or "")
        cols["backtest_arr"].append(r4(num(r.get("annualized_rate_of_return"))))
        cols["trailing_year"].append(r4(num(r.get("trailing_one_year_return"))))
        cols["oos_days"].append(oos_days(r))
        cols["turnover"].append(round(r["annualized_turnover"], 1)
                                if num(r.get("annualized_turnover")) is not None else None)
        ao = num(o.get("annualized_rate_of_return"))
        cols["true_oos_arr"].append(r4(ao))
        cols["true_oos_excess"].append(r4(num(o.get("excess_return"))))
        cols["true_oos_days"].append(num(o.get("oos_calendar_days")))
        # Cumulative over the untouched window, and SPY's cumulative over the
        # same window. An annualized rate alone is easy to misread across a
        # multi-year window, and excess_return is itself cumulative, so showing
        # it beside an annualized figure without its cumulative sibling puts two
        # different units next to each other under similar labels.
        cols["true_oos_cumulative"].append(r4(num(o.get("cumulative_return"))))
        cols["true_oos_spy"].append(r4(num(o.get("spy_return"))))
        fe = fitted_era(r, o) if o else None
        cols["fitted_arr"].append(r4(fe[0]) if fe else None)
        cols["fitted_years"].append(round(fe[1], 2) if fe else None)
        sc = overfit_score(ao, fe[0]) if fe else None
        cols["score"].append(round(sc, 1) if sc is not None else None)
        # The cone's inputs, printed so a reader can recover the call.
        cols["oos_sd"].append(r4(num(o.get("standard_deviation"))))
        cols["oos_trading_days"].append(num(o.get("size")))
        # SPY in each era, so a reader can see when the market changed rather
        # than the strategy. The fitted era ends where the untouched one begins.
        spy_f = None
        if fe and o.get("start"):
            try:
                s0 = dt.date.fromisoformat(o["start"][:10])
                f0 = (s0 - dt.timedelta(days=round(fe[1] * 365.25))).isoformat()
                spy_f = spy_rate(f0, s0.isoformat())
            except ValueError:
                spy_f = None
        cols["spy_fitted"].append(r4(spy_f))
        cols["spy_live"].append(r4(spy_rate(o.get("start"), o.get("end"))) if o else None)
        sg = signs_of(r, o, fe[1] if fe else None)
        cols["fitted_sharpe"].append(sg["fitted_sharpe"])
        cols["universe"].append(sg["universe"])
    return cols


def main():
    global PRICES
    pr = load(PRICES_PATH)
    PRICES = (pr["dates"], pr["tickers"]["SPY"]["closes"])
    rows = load(DATABASE)
    series = load(OOS).get("series", {})

    usable = [r for r in rows
              if r.get("flag") not in NOISE_FLAGS
              and num(r.get("annualized_rate_of_return")) is not None]

    trailing, trailing_stats = trailing_cohort(usable)
    _pairs, true_stats = true_oos_cohort(usable, series)
    split = split_cohort(usable, series)
    turnover = turnover_table(trailing)
    index = build_index(usable, series)

    payload = {
        "generated": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "reference_date": TODAY.isoformat(),
        "pool": len(usable),
        "min_oos_days": MIN_OOS_DAYS,
        "cohorts": {"trailing": trailing_stats, "true_oos": true_stats},
        "turnover": turnover,
        "cone": {"z": Z95, "min_trading_days": MIN_LIVE_TRADING_DAYS,
                 "cash_like_sd": CASH_LIKE_SD, "base_rate_min_years": BASE_RATE_MIN_YEARS},
        "base_rates": base_rates(split),
        "signs": sign_rates(split),
        "verdict_mix": verdict_mix(split),
        "checks": caveat_checks(split),
        "score_distribution": score_distribution(split),
        "ceiling": ceiling_table(split),
        "index": index,
    }

    text = json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n"
    JSON_PATH.write_text(text, encoding="utf-8")
    JS_PATH.write_text(
        "// Overfit Check data, loaded as a script tag so overfit.html works\n"
        "// with the file:// protocol. To update: run scripts/build_overfit.py\n"
        "window.OVERFIT_DATA = " + text.rstrip("\n") + ";\n",
        encoding="utf-8")

    d = payload["score_distribution"]
    print("pool %d, trailing %d, true-OOS %d, fitted split %d, index %d rows"
          % (len(usable), trailing_stats["n"], true_stats["n"], len(split), len(index["ids"])))
    print("score p10/p50/p90 = %.1f / %.1f / %.1f" % (d["p10"], d["p50"], d["p90"]))
    print("verdict mix %s" % payload["verdict_mix"])
    print("base rates %s" % [f["fell_short"] for f in payload["base_rates"]["fifths"]])
    print("checks %s" % payload["checks"])
    print("wrote %s (%.0f KB) and its .js twin"
          % (JSON_PATH.name, JSON_PATH.stat().st_size / 1024.0))


if __name__ == "__main__":
    main()
