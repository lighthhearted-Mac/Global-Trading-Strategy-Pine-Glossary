#!/usr/bin/env python3
"""
refresh_prices.py: Fetch full daily adjusted-close history for the Signal Miner
ticker universe and write:
  - data/prices.json
  - data/prices.js   (window.PRICES_DATA, for file:// compatibility)

The Signal Miner page (signal-miner.html) reads this committed data and runs the
entire signal-generation + backtest in the browser. No live fetching happens
client-side (Yahoo's chart API is CORS-blocked from browsers and rate-limits
datacenter traffic), so this script plays the same role refresh_rsi.py plays
for the RSI page: a server-side (or local) fetch that commits static data.

Usage:
    python scripts/refresh_prices.py

No API key required. Run from the project root. Intended to run on a weekly
schedule via a GitHub Action; safe to run manually any time.
"""

import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PRICES_JSON = BASE_DIR / "data" / "prices.json"
PRICES_JS = BASE_DIR / "data" / "prices.js"

# Only keep history from this date onward. This is purely a file-size bound.
#
# Moved from 2018-01-01 to 2010-01-01 in v1.20.1. 2010 covers the entire
# leveraged-ETF era (SPXL 2008, TQQQ 2010, TNA and FAS 2008), so the funds
# most people actually mine signals on now have their full history. Going back
# further mostly adds nulls: very few of this universe existed before 2010, and
# Signal Miner's common sample window starts at the LATEST first-valid date
# among the selected tickers, so one modern ticker in a selection collapses the
# window back anyway. The cost is paid by every visitor on page load.
#
# KNOWN AND ACCEPTED (owner decision, 2026-08-20): a few tickers do not mean the
# same thing this far back. SVXY was reformed in Feb 2018 from -1x to -0.5x, and
# Yahoo's VXX is the Series B ETN that launched in 2018 after the original was
# retired. Their pre-2018 rows therefore describe a different product. This was
# raised and explicitly waived, so there are deliberately NO per-ticker
# earliest-valid-date overrides here. See docs/PRD.md. If that decision is ever
# revisited, this is the place to add them.
START_DATE = "2010-01-01"
API_CALL_DELAY_SECONDS = 1
USER_AGENT = "Mozilla/5.0 (compatible; composer-atlas-signal-miner/1.0)"

# Signal Miner universe, grouped. The third field drives the chip groups and the
# per-group "All" buttons on signal-miner.html; it is carried through prices.json
# so the page never needs its own copy of the grouping.
#
# Adding a ticker: append it here with a group, re-run this script, and commit the
# regenerated data/prices.json and data/prices.js. Nothing in the HTML changes.
TICKERS = [
    # --- Broad market ---
    ("SPY",  "SPDR S&P 500 ETF",                         "Broad market"),
    ("QQQ",  "Invesco QQQ Trust",                        "Broad market"),
    ("QQQE", "Direxion NASDAQ-100 Equal Weighted",       "Broad market"),
    ("VTI",  "Vanguard Total Stock Market ETF",          "Broad market"),
    ("DIA",  "SPDR Dow Jones Industrial Average ETF",    "Broad market"),
    ("IWM",  "iShares Russell 2000 ETF",                 "Broad market"),
    ("MDY",  "SPDR S&P MidCap 400 ETF",                  "Broad market"),
    ("IOO",  "iShares Global 100 ETF",                   "Broad market"),
    # --- Value & Dividend ---
    ("SPYV", "SPDR Portfolio S&P 500 Value",             "Value & Dividend"),
    ("VIG",  "Vanguard Dividend Appreciation ETF",       "Value & Dividend"),
    ("VIGI", "Vanguard International Dividend Apprec.",  "Value & Dividend"),
    ("SCHD", "Schwab US Dividend Equity ETF",            "Value & Dividend"),
    ("SCHG", "Schwab US Large-Cap Growth ETF",           "Value & Dividend"),
    ("SPHB", "Invesco S&P 500 High Beta ETF",            "Value & Dividend"),
    ("VTV",  "Vanguard Value ETF",                       "Value & Dividend"),
    ("VOOV", "Vanguard S&P 500 Value ETF",               "Value & Dividend"),
    ("VOOG", "Vanguard S&P 500 Growth ETF",              "Value & Dividend"),
    # --- Sector ---
    ("XLK",  "Technology Select Sector SPDR",            "Sector"),
    ("XLE",  "Energy Select Sector SPDR",                "Sector"),
    ("XLF",  "Financial Select Sector SPDR",             "Sector"),
    ("XLB",  "Materials Select Sector SPDR",             "Sector"),
    ("XLI",  "Industrial Select Sector SPDR",            "Sector"),
    ("XLY",  "Consumer Discretionary Select Sector SPDR","Sector"),
    ("XLP",  "Consumer Staples Select Sector SPDR",      "Sector"),
    ("VOX",  "Vanguard Communication Services ETF",      "Sector"),
    ("SMH",  "VanEck Semiconductor ETF",                 "Sector"),
    # --- International ---
    ("EEM",  "iShares MSCI Emerging Markets ETF",        "International"),
    ("EFA",  "iShares MSCI EAFE ETF",                    "International"),
    ("VXUS", "Vanguard Total International Stock ETF",   "International"),
    ("FXI",  "iShares China Large-Cap ETF",              "International"),
    # --- Bonds ---
    ("TLT",  "iShares 20+ Year Treasury Bond ETF",       "Bonds"),
    ("IEF",  "iShares 7-10 Year Treasury Bond ETF",      "Bonds"),
    ("IEI",  "iShares 3-7 Year Treasury Bond ETF",       "Bonds"),
    ("SHY",  "iShares 1-3 Year Treasury Bond ETF",       "Bonds"),
    ("SHV",  "iShares Short Treasury Bond ETF",          "Bonds"),
    ("LQD",  "iShares iBoxx Investment Grade Corporate", "Bonds"),
    ("BND",  "Vanguard Total Bond Market ETF",           "Bonds"),
    ("BNDW", "Vanguard Total World Bond ETF",            "Bonds"),
    ("BSV",  "Vanguard Short-Term Bond ETF",             "Bonds"),
    ("BIL",  "SPDR Bloomberg 1-3 Month T-Bill",          "Bonds"),
    # --- Commodities, FX & crypto ---
    ("GLD",  "SPDR Gold Shares",                         "Commodities, FX & crypto"),
    ("SLV",  "iShares Silver Trust",                     "Commodities, FX & crypto"),
    ("DBC",  "Invesco DB Commodity Index Tracking",      "Commodities, FX & crypto"),
    ("UUP",  "Invesco DB US Dollar Index Bullish",       "Commodities, FX & crypto"),
    ("IBIT", "iShares Bitcoin Trust ETF",                "Commodities, FX & crypto"),
    ("ETHA", "iShares Ethereum Trust ETF",               "Commodities, FX & crypto"),
    # --- Volatility & hedge ---
    ("VIXM", "ProShares VIX Mid-Term Futures",           "Volatility & hedge"),
    ("VXX",  "iPath Series B S&P 500 VIX Short-Term",    "Volatility & hedge"),
    ("UVXY", "ProShares Ultra VIX Short-Term Futures",   "Volatility & hedge"),
    ("SVXY", "ProShares Short VIX Short-Term Futures",   "Volatility & hedge"),
    ("BTAL", "AGFiQ US Market Neutral Anti-Beta",        "Volatility & hedge"),
    ("KMLM", "KFA Mount Lucas Managed Futures",          "Volatility & hedge"),
    ("DBMF", "iMGP DBi Managed Futures Strategy",        "Volatility & hedge"),
    # --- Leverage ---
    ("TQQQ", "ProShares UltraPro QQQ 3x",                "Leverage"),
    ("QLD",  "ProShares Ultra QQQ 2x",                   "Leverage"),
    ("SPXL", "Direxion Daily S&P 500 Bull 3x",           "Leverage"),
    ("SSO",  "ProShares Ultra S&P500 2x",                "Leverage"),
    ("UDOW", "ProShares UltraPro Dow30 3x",              "Leverage"),
    ("SOXL", "Direxion Daily Semiconductor Bull 3x",     "Leverage"),
    ("USD",  "ProShares Ultra Semiconductors 2x",        "Leverage"),
    ("TECL", "Direxion Daily Technology Bull 3x",        "Leverage"),
    ("RETL", "Direxion Daily Retail Bull 3x",            "Leverage"),
    ("FAS",  "Direxion Daily Financial Bull 3x",         "Leverage"),
    ("LABU", "Direxion Daily S&P Biotech Bull 3x",       "Leverage"),
    ("TNA",  "Direxion Daily Small Cap Bull 3x",         "Leverage"),
    ("YINN", "Direxion Daily FTSE China Bull 3x",        "Leverage"),
    ("TMF",  "Direxion Daily 20+ Year Treasury Bull 3x", "Leverage"),
    ("GDXU", "MicroSectors Gold Miners 3x Leveraged",    "Leverage"),
    # --- Inverse ---
    ("SQQQ", "ProShares UltraPro Short QQQ 3x",          "Inverse"),
    ("PSQ",  "ProShares Short QQQ",                      "Inverse"),
    ("SPXU", "ProShares UltraPro Short S&P500 3x",       "Inverse"),
    ("SH",   "ProShares Short S&P500",                   "Inverse"),
    ("SDS",  "ProShares UltraShort S&P500",              "Inverse"),
    ("SOXS", "Direxion Daily Semiconductor Bear 3x",     "Inverse"),
    ("TMV",  "Direxion Daily 20+ Year Treasury Bear 3x", "Inverse"),
    ("GDXD", "MicroSectors Gold Miners -3x Inverse",     "Inverse"),
]


def _start_epoch():
    """START_DATE as a UTC epoch second, for the chart API's period1 bound."""
    d = datetime.strptime(START_DATE, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return int(d.timestamp())


def fetch_daily_closes(symbol):
    """Returns {date_iso: adjusted_close} from START_DATE onward.

    Uses explicit period1/period2 bounds rather than a `range` shorthand. A
    fixed `range=10y` was used until v1.20.1, which silently capped every
    series at ten years: START_DATE could only ever narrow that window, never
    widen it, so moving START_DATE back past the cap did nothing at all. Bugs
    of this shape are invisible in the output (the data looks fine, there is
    just less of it than asked for), so if you change the window, check the
    reported first date actually moved.
    """
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        f"?period1={_start_epoch()}&period2={int(time.time())}"
        f"&interval=1d&events=div,splits"
    )
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    result = data["chart"]["result"][0]
    timestamps = result["timestamp"]
    quote = result["indicators"]["quote"][0]
    adjclose = result["indicators"].get("adjclose", [{}])[0].get("adjclose", quote["close"])

    out = {}
    for ts, close in zip(timestamps, adjclose):
        if close is None:
            continue
        d = datetime.fromtimestamp(ts, tz=timezone.utc).date().isoformat()
        if d >= START_DATE:
            out[d] = round(float(close), 4)
    return out


def refresh():
    """Returns (master_dates, {symbol: {name, closes_aligned_to_master}})."""
    fetched = {}
    failed = []

    for i, (symbol, name, group) in enumerate(TICKERS):
        if i > 0:
            time.sleep(API_CALL_DELAY_SECONDS)
        print(f"  {symbol} ... ", end="", flush=True)
        try:
            series = fetch_daily_closes(symbol)
            fetched[symbol] = {"name": name, "group": group, "series": series}
            first = min(series) if series else "?"
            print(f"{len(series)} rows (from {first})")
        except Exception as exc:
            print(f"FAILED: {exc}")
            failed.append(symbol)

    if failed:
        print(f"\nWARNING: {len(failed)} tickers failed: {', '.join(failed)}")

    # Master date axis = sorted union of every ticker's trading days.
    all_dates = set()
    for info in fetched.values():
        all_dates.update(info["series"].keys())
    master = sorted(all_dates)

    # Align each ticker onto the master axis; None where the ticker has no bar.
    tickers_out = {}
    for symbol, info in fetched.items():
        series = info["series"]
        closes = [series.get(d) for d in master]
        tickers_out[symbol] = {"name": info["name"], "group": info["group"], "closes": closes}

    return master, tickers_out


def write_output(master, tickers_out):
    payload = {
        "refreshed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "start": START_DATE,
        "dates": master,
        "tickers": tickers_out,
    }

    # Compact separators keep the file small (it is mostly numbers).
    text = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
    PRICES_JSON.write_text(text + "\n", encoding="utf-8")
    print(f"\nWrote {PRICES_JSON.name} ({len(text) // 1024} KB, {len(master)} dates, {len(tickers_out)} tickers)")

    comment = (
        "// Signal Miner price history - loaded as a script tag so the page works with file:// protocol.\n"
        "// To update: run scripts/refresh_prices.py\n"
    )
    body = f"window.PRICES_DATA = {text};\n"
    PRICES_JS.write_text(comment + body, encoding="utf-8")
    print(f"Wrote {PRICES_JS.name}")


if __name__ == "__main__":
    print("-- Signal Miner Price Refresh --------------------")
    master, tickers_out = refresh()
    if not tickers_out:
        raise SystemExit("No tickers succeeded; refusing to write empty output.")
    write_output(master, tickers_out)
    print("\nDone.")
