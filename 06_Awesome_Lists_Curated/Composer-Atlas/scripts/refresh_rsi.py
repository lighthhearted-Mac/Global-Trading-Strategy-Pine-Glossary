#!/usr/bin/env python3
"""
refresh_rsi.py: Fetch daily adjusted closes for the Frontrunner signal-ticker
universe and compute 10-period RSI (Wilder's smoothing), writing:
  - data/rsi.json
  - data/rsi.js  (window.RSI_DATA, for file:// compatibility)

Usage:
    python scripts/refresh_rsi.py

No API key required. Run from the project root. Intended to run 3x/day on
weekdays via .github/workflows/refresh-rsi.yml; safe to run manually any time.
"""

import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RSI_JSON = BASE_DIR / "data" / "rsi.json"
RSI_JS = BASE_DIR / "data" / "rsi.js"

RSI_PERIOD = 10
# ~1 trading year: enough for Wilder smoothing to settle, so values match
# Composer and the RSI Backtester, which use the full price history.
LOOKBACK_DAYS = 250
API_CALL_DELAY_SECONDS = 1

USER_AGENT = "Mozilla/5.0 (compatible; composer-atlas-rsi-updater/1.0)"

# Frontrunner signal universe (locked per docs/PRD.md V2.1), plus IWM and DIA
TICKERS = [
    ("XLF", "Financial Select Sector SPDR"),
    ("SPYV", "SPDR Portfolio S&P 500 Value"),
    ("VTV", "Vanguard Value ETF"),
    ("SPY", "SPDR S&P 500 ETF"),
    ("IOO", "iShares Global 100 ETF"),
    ("UUP", "Invesco DB US Dollar Index Bullish"),
    ("FXI", "iShares China Large-Cap ETF"),
    ("QQQE", "Direxion NASDAQ-100 Equal Weighted"),
    ("XLK", "Technology Select Sector SPDR"),
    ("QQQ", "Invesco QQQ Trust"),
    ("XLE", "Energy Select Sector SPDR"),
    ("VOX", "Vanguard Communication Services ETF"),
    ("TECL", "Direxion Daily Technology Bull 3x"),
    ("SOXX", "iShares Semiconductor ETF"),
    ("RETL", "Direxion Daily Retail Bull 3x"),
    ("XLY", "Consumer Discretionary Select Sector SPDR"),
    ("EEM", "iShares MSCI Emerging Markets ETF"),
    ("GLD", "SPDR Gold Shares"),
    ("XLP", "Consumer Staples Select Sector SPDR"),
    ("TLT", "iShares 20+ Year Treasury Bond ETF"),
    # broad index funds, added at the owner's request 2026-10-16
    ("IWM", "iShares Russell 2000 ETF"),
    ("DIA", "SPDR Dow Jones Industrial Average ETF"),
]


def fetch_daily_closes(symbol):
    """Returns (dates, adjusted_closes) for the last LOOKBACK_DAYS trading days."""
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        f"?range=2y&interval=1d&events=div,splits"
    )
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    result = data["chart"]["result"][0]
    timestamps = result["timestamp"]
    quote = result["indicators"]["quote"][0]
    adjclose = result["indicators"].get("adjclose", [{}])[0].get("adjclose", quote["close"])
    raw = quote.get("close") or [None] * len(timestamps)

    dates, closes = [], []
    for k, (ts, close) in enumerate(zip(timestamps, adjclose)):
        # In the evening Yahoo can leave the newest day's adjusted close blank
        # while it processes the day; skipping it silently rolled the page back
        # a day (2026-10-16). The newest day has no pending adjustment, so its
        # plain close is the right value.
        if close is None and k == len(timestamps) - 1:
            close = raw[k]
        if close is None:
            continue
        dates.append(datetime.fromtimestamp(ts, tz=timezone.utc).date().isoformat())
        closes.append(close)

    return dates[-LOOKBACK_DAYS:], closes[-LOOKBACK_DAYS:]


def wilders_rsi(closes, period=RSI_PERIOD):
    changes = [closes[i] - closes[i - 1] for i in range(1, len(closes))]

    gains = [max(c, 0.0) for c in changes]
    losses = [max(-c, 0.0) for c in changes]

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    for gain, loss in zip(gains[period:], losses[period:]):
        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period

    if avg_loss == 0:
        return 100.0
    if avg_gain == 0:
        return 0.0

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def refresh():
    rows = []
    failed = []

    for i, (symbol, name) in enumerate(TICKERS):
        if i > 0:
            time.sleep(API_CALL_DELAY_SECONDS)

        print(f"  {symbol} ... ", end="", flush=True)
        try:
            dates, closes = fetch_daily_closes(symbol)
            rsi = wilders_rsi(closes)
            rows.append({
                "symbol": symbol,
                "name": name,
                "rsi_10": round(rsi, 1),
                "price": round(closes[-1], 2),
                "price_date": dates[-1],
            })
            print(f"RSI {rsi:.1f}  price {closes[-1]:.2f}  ({dates[-1]})")
        except Exception as exc:
            print(f"FAILED: {exc}")
            failed.append(symbol)

    if failed:
        print(f"\nWARNING: {len(failed)} tickers failed:")
        for symbol in failed:
            print(f"  - {symbol}")

    return rows


def keep_newer(rows):
    """Never replace a ticker's saved row with one from an earlier close."""
    try:
        old = {r["symbol"]: r for r in json.loads(RSI_JSON.read_text(encoding="utf-8"))["tickers"]}
    except (OSError, ValueError, KeyError):
        return rows
    out = []
    for r in rows:
        prev = old.get(r["symbol"])
        if prev and prev.get("price_date", "") > r["price_date"]:
            print(f"  {r['symbol']}: fetched {r['price_date']} is older than saved {prev['price_date']}; keeping saved")
            r = prev
        out.append(r)
    return out


def write_output(rows):
    payload = {
        "refreshed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tickers": rows,
    }

    RSI_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nWrote {RSI_JSON.name}")

    comment = (
        "// RSI signals data - loaded as a script tag so the site works with file:// protocol.\n"
        "// To update: run scripts/refresh_rsi.py\n"
    )
    body = f"window.RSI_DATA = {json.dumps(payload, indent=2, ensure_ascii=False)};\n"
    RSI_JS.write_text(comment + body, encoding="utf-8")
    print(f"Wrote {RSI_JS.name}")


if __name__ == "__main__":
    print("── RSI Signals Refresh ────────────────────────")
    rows = refresh()
    if not rows:
        raise SystemExit("No tickers succeeded; refusing to write empty output.")
    write_output(keep_newer(rows))
    print("\nDone.")
