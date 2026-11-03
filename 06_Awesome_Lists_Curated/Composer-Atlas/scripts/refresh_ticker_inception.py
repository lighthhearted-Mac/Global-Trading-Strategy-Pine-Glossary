#!/usr/bin/env python3
"""
refresh_ticker_inception.py: fetch a real first-trade date for each ticker and
write:
  - data/ticker_inception.json
  - data/ticker_inception.js   (window.TICKER_INCEPTION_DATA, file:// twin)

Why this file exists rather than reusing data/prices.json. V1.20 item 9 needs
one true inception date per ticker so a strategy page can say WHY its backtest
window is the length it is. prices.json cannot answer that, for two independent
reasons, and the second one is fatal:

  1. It covers the Signal Miner universe, which overlaps the featured
     strategies' 105 held tickers on only 44 of them.
  2. It starts at 2010-01-04, so every ticker that listed earlier reports
     2010-01-04 as its first close. Measured: 48 of its 72 tickers do exactly
     that. It cannot tell "listed in 2010" from "listed in 1993", so a readout
     built on it would report SPY as starting in 2010 when it launched in 1993.

That is not a coverage gap that more tickers would fix. It is the wrong
instrument. Hence a separate artifact holding one date per ticker, roughly 25
bytes each, fetched once and refreshed rarely because inception dates do not
change.

Source: the Yahoo chart API's `meta.firstTradeDate`, an epoch second the API
returns alongside any price request. Asking for `range=1d` keeps each response
tiny: we want one field, not a price history, so there is no reason to download
one. Spot-checked against known launches: SPY 1993-01-29, QQQ 1999-03-10,
TQQQ 2010-02-11, IBIT 2024-01-11.

Usage:
    python scripts/refresh_ticker_inception.py            # featured set (~105)
    python scripts/refresh_ticker_inception.py --all      # every held ticker
    python scripts/refresh_ticker_inception.py --missing  # only unfetched ones

Runs are ADDITIVE: existing entries are kept and merged, so `--all` after
`--featured` extends the file rather than replacing it, and an interrupted run
loses only the tickers it had not reached. No API key required.
"""

import json
import sys
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE = BASE_DIR / "data" / "database.json"
EXTRAS = BASE_DIR / "data" / "strategy_extras.json"
OUT_JSON = BASE_DIR / "data" / "ticker_inception.json"
OUT_JS = BASE_DIR / "data" / "ticker_inception.js"

API_CALL_DELAY_SECONDS = 2

# Write the file every this many tickers. The featured run is ~4 minutes and
# would not need this, but --all is ~2 hours over 3,680 tickers, and a run that
# only wrote at the end would lose two hours of work to one dropped connection.
# Runs are additive, so a checkpointed file is a resumable one: rerunning skips
# every ticker already carrying a date.
CHECKPOINT_EVERY = 50
USER_AGENT = "Mozilla/5.0 (compatible; composer-atlas-inception/1.0)"

# The cash sleeve is a position, not a security with an inception date.
CASH = "$USD"

# Composer writes class shares with a slash; Yahoo uses a hyphen. Only the
# request is rewritten, never the stored key, so the join back to holdings
# stays exact.
def yahoo_symbol(ticker):
    return ticker.replace("/", "-")


# Epoch arithmetic, NOT datetime.fromtimestamp. firstTradeDate is negative for
# anything listed before 1970, and on Windows fromtimestamp raises
# "[Errno 22] Invalid argument" on a negative value rather than returning a
# date. KO is the featured set's only pre-1970 ticker (-252322200, 1962-01-02)
# and it failed exactly this way on the first run. Across the full database the
# blast radius is much larger: every legacy stock would have been dropped, and
# dropped as a *fetch failure*, which reads like a network problem rather than
# a date-handling bug. timedelta arithmetic has no such floor on any platform.
def epoch_date(epoch):
    return (datetime(1970, 1, 1, tzinfo=timezone.utc)
            + timedelta(seconds=epoch)).date().isoformat()


def fetch_inception(ticker):
    """Returns an ISO date string, or None if Yahoo does not report one."""
    url = (
        "https://query1.finance.yahoo.com/v8/finance/chart/%s"
        "?range=1d&interval=1d" % yahoo_symbol(ticker)
    )
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    meta = data["chart"]["result"][0]["meta"]
    epoch = meta.get("firstTradeDate")
    if epoch is None:
        return None
    return epoch_date(epoch)


def featured_tickers():
    extras = json.loads(EXTRAS.read_text(encoding="utf-8"))
    out = set()
    for entry in extras.values():
        out.update(t for t in entry.get("holdings", {}) if t != CASH)
    return sorted(out)


def all_tickers():
    database = json.loads(DATABASE.read_text(encoding="utf-8"))
    out = set()
    for row in database:
        holdings = row.get("last_market_days_holdings") or {}
        out.update(t for t in holdings if t != CASH)
    return sorted(out)


def load_existing():
    if not OUT_JSON.exists():
        return {}
    return json.loads(OUT_JSON.read_text(encoding="utf-8")).get("tickers", {})


def write_output(tickers):
    payload = {
        "refreshed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "Yahoo chart API, meta.firstTradeDate",
        "tickers": dict(sorted(tickers.items())),
    }
    body = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=False)
    OUT_JSON.write_text(body + "\n", encoding="utf-8")
    OUT_JS.write_text(
        "// Ticker inception dates: one real first-trade date per ticker, used by\n"
        "// build_strategy_extras.py to name the holding that limits a backtest window.\n"
        "// To update: run scripts/refresh_ticker_inception.py\n"
        "window.TICKER_INCEPTION_DATA = " + body + ";\n",
        encoding="utf-8",
    )
    known = sum(1 for v in tickers.values() if v)
    size = len(body) // 1024
    print("\nWrote %s and %s (%d KB, %d tickers, %d with a date)"
          % (OUT_JSON.name, OUT_JS.name, size, len(tickers), known))


def main():
    args = sys.argv[1:]
    existing = load_existing()

    named = [a.strip().upper() for a in args if not a.startswith("-") and a.strip()]

    if named:
        # Explicit tickers, for symbols the sweeps cannot reach. Both sweeps read
        # held tickers, and the K-1 database is NOT a subset of those: DBS and DBV
        # are in k1.json and held by no symphony, so --all would never date them.
        wanted = named
        scope = "explicitly named ticker(s)"
    elif "--all" in args:
        wanted = all_tickers()
        scope = "every ticker held anywhere in the database"
    else:
        wanted = featured_tickers()
        scope = "tickers held by the featured strategies"

    # A ticker already carrying a date is never refetched: inception dates do
    # not change. A stored null IS retried, because a null is usually a
    # transient fetch failure rather than a security with no start date.
    todo = [t for t in wanted if not existing.get(t)]
    if "--missing" in args:
        todo = [t for t in todo if t not in existing]

    print("Scope: %s (%d tickers)" % (scope, len(wanted)))
    print("Already dated: %d. To fetch: %d.\n" % (len(wanted) - len(todo), len(todo)))
    if not todo:
        write_output(existing)
        return 0

    minutes = len(todo) * API_CALL_DELAY_SECONDS / 60.0
    print("Estimated %.0f minutes at %ds per call.\n" % (minutes, API_CALL_DELAY_SECONDS))

    failed = []
    for i, ticker in enumerate(todo):
        if i > 0:
            time.sleep(API_CALL_DELAY_SECONDS)
        try:
            date = fetch_inception(ticker)
        except Exception as exc:
            print("  %-8s FAILED: %s" % (ticker, exc))
            existing[ticker] = None
            failed.append(ticker)
            continue
        existing[ticker] = date
        if date is None:
            print("  %-8s no firstTradeDate reported" % ticker)
            failed.append(ticker)
        else:
            print("  %-8s %s" % (ticker, date))

        if (i + 1) % CHECKPOINT_EVERY == 0:
            write_output(existing)
            print("  ... checkpoint at %d of %d" % (i + 1, len(todo)))

    write_output(existing)
    if failed:
        print("WARNING: %d ticker(s) without a date: %s"
              % (len(failed), ", ".join(failed)))
        print("  Rerun to retry them. A stored null is retried on the next run.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
