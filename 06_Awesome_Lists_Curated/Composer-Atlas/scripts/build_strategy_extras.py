#!/usr/bin/env python3
"""
build_strategy_extras.py: join the 31 featured strategies to the full database
and to the K-1 database, and write the result as a small file the strategy
pages can load directly.

    data/strategies.json  +  data/database.json  +  data/k1.json
      +  data/ticker_inception.json
        -> data/strategy_extras.json  +  data/strategy_extras.js

Why a build step and not a browser join. `data/database.json` is 6,669 entries
and roughly 5 MB. Shipping it to a strategy page so that page could read one
row out of it would undo the page-weight work done in v1.16. The join key is
`symphony_id`, it is stable, and it changes only when the featured set changes,
so it belongs in a build artifact rather than in every visitor's browser.

Why it fails loudly. A missing `symphony_id` would otherwise render a strategy
page with an empty metrics block: still HTTP 200, still laid out correctly,
simply missing the sections. That is the same failure shape that took the
Signal Miner down in v1.22.2 and it is the reason check_html_js.py exists. So a
join miss here is a non-zero exit, not a warning.

Usage:
    python scripts/build_strategy_extras.py

Run it after any refresh that touches data/database.json or data/k1.json, and
after adding or removing a featured strategy. scripts/check_strategy_extras.py
rebuilds this in memory and fails the deploy if the committed file disagrees,
so a forgotten run is caught rather than shipped.

This script is deliberately NOT wired into .github/workflows/update-metrics.yml.
A join miss must fail the person who caused it, at their desk, rather than
breaking the nightly metrics job and its sitemap commit for everyone.
"""

import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STRATEGIES = BASE_DIR / "data" / "strategies.json"
DATABASE = BASE_DIR / "data" / "database.json"
K1 = BASE_DIR / "data" / "k1.json"
INCEPTION = BASE_DIR / "data" / "ticker_inception.json"
PRICES = BASE_DIR / "data" / "prices.json"
OUT_JSON = BASE_DIR / "data" / "strategy_extras.json"
OUT_JS = BASE_DIR / "data" / "strategy_extras.js"

# Fields carried over from the database row. Everything here is already
# computed by the Composer API and stored; none of it is derived by this
# script. Items 2, 3, 6 and 8 of the V1.20 roadmap consume the ones the pages
# do not render yet, which is why they are carried now rather than added later
# one at a time.
CARRY = [
    "oos_date",
    "refresh_date",
    "top_one_day_contribution",
    "top_five_percent_day_contribution",
    "top_ten_percent_day_contribution",
    "sortino_ratio",
    "win_rate",
    "skewness",
    "kurtosis",
    "tail_ratio",
    "herfindahl_index",
    "annualized_turnover",
    "total_costs",
]

# The cash sleeve is a position, not a holding anyone receives a tax form for.
CASH = "$USD"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def best_day_share(closes):
    """Share of the summed daily return produced by the best 5% of days.

    The same statistic Composer reports as `top_five_percent_day_contribution`,
    computed the additive way: sum simple daily returns, take the best 5% of
    them, divide by the total. Returns None rather than a number whenever the
    result would be meaningless.
    """
    rets = [b / a - 1.0 for a, b in zip(closes, closes[1:]) if a and b and a > 0]
    if len(rets) < 60:
        return None
    total = sum(rets)
    if total <= 0:
        # A flat or negative window makes the denominator useless: the ratio
        # explodes or flips sign for reasons that say nothing about outliers.
        return None
    n5 = max(1, int(round(len(rets) * 0.05)))
    return sum(sorted(rets, reverse=True)[:n5]) / total


def spy_baseline(spy_closes, backtest_days):
    """What SPY itself scores on the best-days measure over the SAME window.

    PRD item 4a. The raw figure is uninterpretable alone, because its
    denominator is NET return, a small residual under a much larger gross:
    plain buy-and-hold SPY scores 202% over its full history and TLT 729%.
    Benchmarking gives the number an anchor a reader can actually use.

    Returns None when data/prices.json does not reach far enough back to cover
    the strategy's window. Three featured strategies backtest roughly 27 years
    against 16 years of stored SPY closes, and quietly comparing a 27-year
    strategy figure to a 16-year SPY figure would be a new wrong number in
    place of the old misleading one. Those pages fall back to the plain figure.
    """
    if not spy_closes or not backtest_days:
        return None
    need = int(backtest_days) + 1
    if len(spy_closes) < need:
        return None
    share = best_day_share(spy_closes[-need:])
    if share is None:
        return None
    # Rounded so an appended close cannot churn the committed file through
    # float noise alone. check_strategy_extras.py demands byte equality.
    return {"days": need - 1, "top_five_percent_day_contribution": round(share, 6)}


def build():
    strategies = load(STRATEGIES)
    database = load(DATABASE)
    k1 = load(K1)["tickers"]
    inception = load(INCEPTION)["tickers"] if INCEPTION.exists() else {}
    spy = (load(PRICES)["tickers"].get("SPY") or {}).get("closes") or [] \
        if PRICES.exists() else []

    by_id = {}
    for row in database:
        by_id[row["symphony_id"]] = row

    missing = [s["slug"] for s in strategies if s["symphony_id"] not in by_id]
    if missing:
        raise SystemExit(
            "FAIL: %d featured strateg%s have no row in data/database.json: %s\n"
            "The strategy page for each of these would render with its new sections\n"
            "silently empty. Add the symphony to the database and refresh it, or\n"
            "remove it from data/strategies.json." % (
                len(missing), "y" if len(missing) == 1 else "ies", ", ".join(missing))
        )

    extras = {}
    unknown = set()

    for s in strategies:
        row = by_id[s["symphony_id"]]
        holdings = row.get("last_market_days_holdings") or {}
        tickers = sorted(t for t in holdings if t != CASH)

        # `last_market_days_holdings` keys are the ticker universe the logic can
        # reach; its values are today's position, and most of them are 0.0. So a
        # ticker appearing here means the strategy CAN hold it, not that it does,
        # and the page must not claim otherwise. `held` carries the distinction.
        k1_holdings = []
        etn_holdings = []
        for t in tickers:
            fund = k1.get(t)
            if fund is None:
                # Expected for individual stocks, which were deliberately purged
                # from the K-1 database in v1.27.5: a stock never issues a K-1.
                # Reported in the run summary rather than failing, because this
                # script cannot tell a stock from a fund nobody has checked yet.
                unknown.add(t)
                continue
            if fund.get("k1") is True:
                k1_holdings.append({
                    "ticker": t,
                    "name": fund.get("name"),
                    "tax_form": fund.get("tax_form") or "Schedule K-1",
                    "held": bool(holdings.get(t)),
                })
            if (fund.get("structure") or "").upper() == "ETN":
                etn_holdings.append({
                    "ticker": t,
                    "name": fund.get("name"),
                    "held": bool(holdings.get(t)),
                })

        entry = {"symphony_id": s["symphony_id"]}
        for key in CARRY:
            entry[key] = row.get(key)
        entry["holdings"] = {t: holdings[t] for t in tickers}
        # Per-ticker inception for the Assets section (V1.20 item 6). Only the
        # strategy's own tickers, so this adds a few hundred entries across the
        # 31 rather than shipping the whole inception file to the browser.
        entry["holdings_inception"] = {
            t: inception[t] for t in tickers if inception.get(t)
        }
        entry["backtest_floor"] = backtest_floor(tickers, inception)
        entry["spy_best_day_baseline"] = spy_baseline(spy, s.get("backtest_days"))
        entry["k1_holdings"] = k1_holdings
        entry["etn_holdings"] = etn_holdings
        extras[s["slug"]] = entry

    return strategies, extras, sorted(unknown)


def backtest_floor(tickers, inception):
    """The earliest date this strategy could possibly have been backtested from.

    A strategy cannot be tested over a period in which one of its holdings did
    not exist, so the latest inception date among its holdings is a hard floor
    on the window. Reported as a BOUND, never as the cause of the window's
    actual length, because measurement says those are different things:

      Across the 31 featured strategies, not one backtest starts before its
      floor, so the bound is real. But not one starts AT it either. 18 of 31
      begin within a year of it and the limiting holding genuinely explains
      their window; the other 13 begin well after, up to 5.6 years late for
      `zoops-kmlm-switcher-2026`. V1.20 item 9 specified the wording "14.8
      years, limited by UVXY" for every strategy. That sentence is true for
      roughly half of them and asserts a false cause for the rest.

    `dated` vs `total` is carried so the page can refuse to name a limiter it
    cannot stand behind: one undated holding could be the real floor, and a
    floor computed from a subset would be silently too early.
    """
    dated = sorted(((inception[t], t) for t in tickers if inception.get(t)), reverse=True)
    out = {"dated": len(dated), "total": len(tickers)}
    if not dated:
        out["date"] = None
        out["tickers"] = []
        return out
    floor = dated[0][0]
    # Ties are kept rather than collapsed to one. Whole leveraged families
    # launched on the same day (SOXL and SOXS both 2010-03-11, GDXU and GDXD
    # both 2020-12-03), and picking one arbitrarily would name a different
    # ticker on a rerun for no reason a reader could see.
    out["date"] = floor
    out["tickers"] = sorted(t for d, t in dated if d == floor)
    return out


def payload(extras):
    return json.dumps(extras, indent=2, ensure_ascii=False, sort_keys=True)


def main():
    strategies, extras, unknown = build()
    body = payload(extras)

    OUT_JSON.write_text(body + "\n", encoding="utf-8")
    OUT_JS.write_text(
        "// Strategy extras: the featured strategies joined to the full database and the\n"
        "// K-1 database at build time. Loaded as a script tag so strategies.html works\n"
        "// with the file:// protocol.\n"
        "// To update: run scripts/build_strategy_extras.py\n"
        "window.STRATEGY_EXTRAS_DATA = " + body + ";\n",
        encoding="utf-8",
    )

    k1_count = sum(1 for e in extras.values() if e["k1_holdings"])
    etn_count = sum(1 for e in extras.values() if e["etn_holdings"])
    no_oos = sorted(k for k, e in extras.items() if not e.get("oos_date"))
    outlier = sorted(
        k for k, e in extras.items()
        if (e.get("top_five_percent_day_contribution") or 0) > 1
    )
    no_base = sorted(k for k, e in extras.items() if not e.get("spy_best_day_baseline"))
    above_spy = sorted(
        k for k, e in extras.items()
        if e.get("spy_best_day_baseline")
        and (e.get("top_five_percent_day_contribution") or 0)
        > e["spy_best_day_baseline"]["top_five_percent_day_contribution"]
    )

    floored = sum(1 for e in extras.values() if e["backtest_floor"]["date"])
    partial = sorted(k for k, e in extras.items()
                     if e["backtest_floor"]["dated"] < e["backtest_floor"]["total"])

    print("Joined %d of %d featured strategies, 0 misses." % (len(extras), len(strategies)))
    print("  with an inception floor:  %d" % floored)
    print("  holding a K-1 issuer: %d" % k1_count)
    print("  holding an ETN:       %d" % etn_count)
    print("  best 5%% of days above 100%% of total return: %d" % len(outlier))
    print("  more reliant on its best days than SPY over the same window: %d" % len(above_spy))
    if no_base:
        print("  no SPY baseline, so these render the plain figure (%d): %s"
              % (len(no_base), ", ".join(no_base)))
        print("    Expected when the backtest window predates data/prices.json.")
    if no_oos:
        print("  no oos_date (the panel renders as \"not recorded\"): %s" % ", ".join(no_oos))
    if partial:
        print("  incomplete inception coverage, so no limiter is named on these")
        print("    pages (%d): %s" % (len(partial), ", ".join(partial)))
        print("    Fix: run scripts/refresh_ticker_inception.py")
    if unknown:
        print("  held but not in the K-1 database (%d): %s" % (len(unknown), ", ".join(unknown)))
        print("    Expected for individual stocks. Anything here that is a fund is a real gap:")
        print("    add it to data/k1_seed.txt and rerun scripts/refresh_k1.py.")
    print("Wrote %s and %s" % (OUT_JSON.name, OUT_JS.name))
    return 0


if __name__ == "__main__":
    sys.exit(main())
