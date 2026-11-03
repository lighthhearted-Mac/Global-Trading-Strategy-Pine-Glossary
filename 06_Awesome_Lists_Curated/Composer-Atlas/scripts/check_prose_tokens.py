#!/usr/bin/env python3
"""Deploy gate for metric tokens in authored prose.

Prose may quote a performance figure, but only through a token: `{sharpe_ratio}`
rather than a typed "2.89". `resolveStrategyTokens` in js/app.js substitutes them
at render time from the same object the metrics table reads.

Why the rule exists. Every performance figure in the library's prose was typed by
hand, and the ones worth quoting are exactly the ones scripts/update_metrics.py
rewrites nightly. Those were wrong within days of being written and nothing said
so. scripts/check_stat_drift.py catches a stale quote after the fact; a token
cannot go stale in the first place. v1.45.0 converted 125 citations across all 36
strategies, which is why the advisory list below is currently empty.

A token may carry a precision: {max_drawdown_abs} is "78.3%" and
{max_drawdown_abs:0} is "78%", because the library's prose voice rounds.

What this checks:

  1. Every token that appears in prose is one js/app.js actually defines. A typo
     like {sharp_ratio} renders as itself on the page, which is ugly but honest;
     this stops it reaching a reader at all.
  2. Every token used resolves to a real value on that strategy. A token is only
     as good as the field behind it, and a null renders as the literal token.
  3. Advisory, not fatal: literal figures still typed into prose that read as a
     nightly-rewritten field, i.e. ones that should have been tokens. This is now
     a regression check rather than a migration aid: it is at zero, and a new
     hand-typed figure is what would push it off zero.

The token list is PARSED FROM js/app.js rather than restated here. Two copies of
a whitelist drift, and the whole point of this file is that a number has one home.

Usage:
    python scripts/check_prose_tokens.py

Exit code is non-zero for problems 1 and 2, so it can gate a deploy. Whether it
becomes a deploy gate is the open PRD item 10b ruling.
"""

import json
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STRATEGIES = BASE_DIR / "data" / "strategies.json"
APP_JS = BASE_DIR / "js" / "app.js"

TOKEN_RE = re.compile(r"\{([a-z_]+)(?::(\d))?\}")

# Which strategy field each token reads, so a null can be reported before the
# page renders the token as literal text. Presentation lives in app.js; this is
# only the dependency, which is what a null check needs.
TOKEN_FIELD = {
    "sharpe_ratio": "sharpe_ratio",
    "calmar_ratio": "calmar_ratio",
    "annualized_rate_of_return": "annualized_rate_of_return",
    "cumulative_return": "cumulative_return",
    "standard_deviation": "standard_deviation",
    "trailing_one_year_return": "trailing_one_year_return",
    "max_drawdown": "max_drawdown",
    "max_drawdown_abs": "max_drawdown",
    "worst_day": "min",
    "best_day": "max",
    "mean_day": "mean",
    "median_day": "median",
    "backtest_days": "backtest_days",
    "backtest_years": "backtest_days",
}

# Fields update_metrics.py rewrites: how a literal quote of one would look, and a
# word that has to appear near it before the quote is believed to be that metric.
#
# The keyword guard exists because a bare number proves nothing.
# zoops-manhattan-project-2026 writes "Frontrunner (50% weight)" and its standard
# deviation is also 50%; without the guard that line is flagged on every run
# forever, and an advisory nobody can clear is an advisory nobody reads.
#
# Both the one-decimal and the rounded form are listed, because the library's
# prose voice rounds ("a 47% max drawdown") and the rounded figure drifts exactly
# as fast as the precise one.
NEAR = 45

DRIFTY = {
    "sharpe_ratio": (lambda v: ["%.2f" % v], r"sharpe"),
    "calmar_ratio": (lambda v: ["%.2f" % v], r"calmar"),
    "annualized_rate_of_return": (
        lambda v: ["%.1f%%" % (v * 100), "%d%%" % round(v * 100)],
        r"annualiz|compounds|returns?|cagr"),
    "max_drawdown": (
        lambda v: ["%.1f%%" % (v * 100), "%.1f%%" % (abs(v) * 100),
                   "%d%%" % round(abs(v) * 100)],
        r"drawdown|peak value|drop|lost"),
    "standard_deviation": (
        lambda v: ["%.1f%%" % (v * 100), "%d%%" % round(v * 100)],
        r"volatil|standard deviation|vol"),
    "trailing_one_year_return": (
        lambda v: ["%.1f%%" % (v * 100), "%d%%" % round(v * 100)],
        r"trailing|past (year|12)|one[- ]year return|last (year|12)"),
    "backtest_days": (lambda v: ["{:,}".format(v)], r"trading day|[- ]day\)|backtest"),
}


def defined_tokens():
    """The keys of PROSE_TOKENS in js/app.js, so there is one whitelist."""
    src = APP_JS.read_text(encoding="utf-8")
    m = re.search(r"const PROSE_TOKENS = \{(.*?)\n\};", src, re.S)
    if not m:
        raise SystemExit(
            "FAIL: could not find `const PROSE_TOKENS = {` in js/app.js.\n"
            "      This checker parses that object so the whitelist has one home.\n"
            "      If it was renamed, update this parser rather than restating the list."
        )
    return set(re.findall(r"^\s{2}([a-z_]+):", m.group(1), re.M))


def strings(entry):
    """(field path, text) for every authored string on a strategy."""
    for f in ("description", "author_note", "regime_note"):
        if isinstance(entry.get(f), str):
            yield f, entry[f]
    for f in ("ai_summary", "how_it_works", "tldr", "assumptions", "regimes", "signals"):
        v = entry.get(f)
        if isinstance(v, str):
            yield f, v
        elif isinstance(v, list):
            for i, item in enumerate(v):
                if isinstance(item, str):
                    yield "%s[%d]" % (f, i), item
                elif isinstance(item, dict):
                    for k, vv in item.items():
                        if isinstance(vv, str):
                            yield "%s[%d].%s" % (f, i, k), vv
                        elif isinstance(vv, list):
                            for j, x in enumerate(vv):
                                if isinstance(x, str):
                                    yield "%s[%d].%s[%d]" % (f, i, k, j), x
        elif isinstance(v, dict):
            for k, vv in v.items():
                if isinstance(vv, str):
                    yield "%s.%s" % (f, k), vv
                elif isinstance(vv, list):
                    for j, x in enumerate(vv):
                        if isinstance(x, str):
                            yield "%s.%s[%d]" % (f, k, j), x
    rp = entry.get("risk_profile")
    if isinstance(rp, str):
        yield "risk_profile", rp
    elif isinstance(rp, dict):
        for k, v in rp.items():
            if isinstance(v, str):
                yield "risk_profile.%s" % k, v


def main():
    known = defined_tokens()
    strategies = json.loads(STRATEGIES.read_text(encoding="utf-8"))

    problems, advisory = [], []
    used = {}

    for s in strategies:
        for field, text in strings(s):
            for tok, _prec in TOKEN_RE.findall(text):
                used[tok] = used.get(tok, 0) + 1
                if tok not in known:
                    problems.append(
                        "%s [%s]: unknown token {%s}. js/app.js defines: %s"
                        % (s["slug"], field, tok, ", ".join(sorted(known))))
                    continue
                val = s.get(TOKEN_FIELD.get(tok, tok))
                if val is None:
                    problems.append(
                        "%s [%s]: token {%s} reads `%s`, which is null on this strategy"
                        % (s["slug"], field, tok, TOKEN_FIELD.get(tok, tok)))

        for where, text in strings(s):
            for field, (forms, keyword) in DRIFTY.items():
                v = s.get(field)
                if v is None:
                    continue
                for lit in forms(v):
                    # Not inside a token already, and not part of a longer number.
                    for m in re.finditer(
                            r"(?<![\d.,{:])" + re.escape(lit) + r"(?![\d])", text):
                        ctx = text[max(0, m.start() - NEAR):m.end() + NEAR]
                        if re.search(keyword, ctx, re.I):
                            advisory.append(
                                "%s [%s]: literal %r reads as %s, should be a token"
                                % (s["slug"], where, lit, field))
                            break

    if used:
        print("Tokens in use: %s" % ", ".join(
            "%s x%d" % (k, n) for k, n in sorted(used.items(), key=lambda x: -x[1])))
    else:
        print("Tokens in use: none yet.")

    if advisory:
        print("\n%d literal figure(s) still typed in prose that a token would own:"
              % len(advisory))
        for a in advisory[:40]:
            print("  ADVISORY: %s" % a)
        if len(advisory) > 40:
            print("  ... and %d more" % (len(advisory) - 40))

    if problems:
        print()
        for p in problems:
            print("FAIL: %s" % p)
        return 1

    print("\nPASS: %d strategies, every token resolves.%s"
          % (len(strategies),
             "" if not advisory else " %d literal(s) flagged above, not fatal." % len(advisory)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
