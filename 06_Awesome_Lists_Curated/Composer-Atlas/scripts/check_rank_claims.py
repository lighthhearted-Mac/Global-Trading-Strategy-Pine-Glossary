#!/usr/bin/env python3
"""Re-derive every library-wide rank claim in authored prose from live metrics.

Why this exists. Strategy pages make comparative claims about the library:
"the fourth shallowest drawdown among the 24 strategies", "a Sharpe that ranks
9th of 24", "the deepest drawdown of any strategy in this library". Every one of
those is a fact about all 24 visible strategies at once, so a weekly metrics
refresh can falsify a sentence on a page nobody touched. Nothing else in the
repo can see that: `check_stat_drift.py` compares figures a page quotes about
ITSELF, and the tokens it validates resolve at render time.

This is not hypothetical. On 2026-09-03 this check found `gold-miner-original`
claiming the highest annualized volatility in the library when Beta Ballers had
been higher for some time. It had survived the full 24-page audit in v1.68.2,
because that audit re-derived the rank claims in the four narrative sections and
this claim sits in `risk_profile.leverage`.

How it reads a sentence. Not by parsing English. It matches five explicit
templates covering the phrasings actually in use, and requires a library-scope
phrase near each match:

    "Sharpe and Calmar both rank 12th of 24"           two metrics, one rank
    "Sharpe and Calmar are both the highest of the 24" two metrics, implicit 1st
    "a {sharpe_ratio} Sharpe ranks 9th of 24"          metric then rank
    "the fourth shallowest drawdown among the 24"      rank then metric
    "{standard_deviation} volatility the fourth lowest" metric then rank

This is deliberately precision-first. An earlier draft walked the sentence
pairing every metric marker with every rank marker, and it invented claims: "the
worst single day in the record" became a rank claim about record length, and a
"both" early in a sentence leaked onto every later rank in it. A claim this
misses is one nobody was checking anyway. A claim it invents teaches the reader
to ignore the checker, which is worse than not having one.

What it will not judge. Hedged comparatives carry no position to check ("among
the deepest in this library", "among the lowest here"), and are counted and
reported but never failed. Making those precise would mean inventing a threshold
for "among", and a wrong threshold produces false failures on true sentences.

Advisory, not a gate: the owner's 2026-09-02 ruling on PRD item 10b gated
check_asset_sizes.py alone and left the rest reporting.

Usage:
    python scripts/check_rank_claims.py [--verbose]
"""

import json
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# (metric field, is a bigger number "better"/first for this wording)
# Direction is decided by the superlative next to the metric, not by the metric
# itself, so both orderings are kept for every field.
METRICS = [
    (r"\bsharpe\b", "sharpe_ratio"),
    (r"\bcalmar\b", "calmar_ratio"),
    (r"\b(?:max(?:imum)? )?drawdown\b", "max_drawdown"),
    (r"\b(?:annuali[sz]ed )?(?:standard deviation|volatility)\b", "standard_deviation"),
    # The bare "annualized" alternative has to refuse the volatility wording or
    # it steals "annualized volatility" from the field above, which was the
    # first version's largest source of false failures.
    (r"\b(?:annuali[sz]ed|annual) (?:return|rate of return)\b"
     r"|\bannuali[sz]ed\b(?!\s+(?:volatility|standard deviation))",
     "annualized_rate_of_return"),
    (r"\b(?:trading days|record|window|backtest)\b", "backtest_days"),
    (r"\btrailing (?:one[- ])?year\b|\btrailing year\b", "trailing_one_year_return"),
]

# Superlatives, and whether they mean "largest stored value first".
HIGH_FIRST = {
    "highest": True, "lowest": False,
    "deepest": False, "shallowest": True,      # drawdowns are stored negative
    "largest": True, "smallest": False,
    "longest": True, "shortest": False,
    "best": True, "worst": False,
    "strongest": True, "weakest": False,
    "steepest": False,
}

# Drawdowns are stored negative but always discussed by magnitude, so "the
# lowest max drawdown" means the shallowest, not the most negative. Reading
# those words literally inverts the answer on every drawdown claim in the
# library, so the field overrides the general table.
DRAWDOWN_OVERRIDE = {
    "lowest": True, "smallest": True, "best": True,
    "highest": False, "largest": False, "worst": False,
}

ORDINALS = {
    "first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 6,
    "seventh": 7, "eighth": 8, "ninth": 9, "tenth": 10, "eleventh": 11,
    "twelfth": 12, "thirteenth": 13, "fourteenth": 14, "fifteenth": 15,
    "sixteenth": 16, "seventeenth": 17, "eighteenth": 18, "nineteenth": 19,
    "twentieth": 20,
}
ORDINAL_RE = r"(?:%s|\d+(?:st|nd|rd|th))" % "|".join(ORDINALS)
SUPERLATIVE_RE = "|".join(HIGH_FIRST)

# A sentence only counts as a library-wide claim if it says so. Without this the
# checker would try to rank a strategy's own holdings against the library.
LIBRARY_RE = re.compile(
    r"\b(?:of|among|in|across)\s+(?:the\s+)?(?:24|twenty-four)\b"
    r"|\bin this library\b|\bof any strategy\b|\bof the strategies\b"
    r"|\bof any other strategy\b|\banywhere in this library\b", re.I)

HEDGE_RE = re.compile(r"\bamong the (?:%s)\b|\bone of the\b" % SUPERLATIVE_RE, re.I)

# One alternation over every metric phrase, used to build the templates below.
METRIC_RE = "|".join("(?:%s)" % p for p, _ in METRICS)

# A match only counts if the library is named close by. Without this proximity
# rule, one "of the 24" anywhere in a sentence licenses every superlative in it,
# which is how "the worst single day in the record" became a claim about record
# length.
SCOPE_WINDOW = 90


def metric_of(phrase):
    for pattern, field in METRICS:
        if re.search(pattern, phrase, re.I):
            return field
    return None


# A superlative that trails its metric must be the end of the thought. If a noun
# follows it, the superlative belongs to that noun and not to the metric behind
# it: "trading days ... which is the highest turnover" is a claim about turnover,
# and "annualized volatility, and the worst single day" is a claim about a day.
# Both were read as rank claims about the metric before them until this existed.
TRAILING_END = r"(?=\s*(?:[,.;:)*]|$|\bin\b|\bof\b|\bhere\b|\bamong\b|\bacross\b|\bat\b))"

TEMPLATES = [
    # "Sharpe and Calmar both rank 12th", "... are both the highest".
    # The ordinal or the superlative is required: a bare "both" is a conjunction
    # ("it beats all three on return, on drawdown and on both risk-adjusted
    # ratios"), not a rank claim.
    (r"(%s)[^.]{0,40}?\band\b[^.]{0,40}?(%s)[^.]{0,30}?\bboth\b\s*(?:rank(?:s|ed)?|are|is)?"
     r"\s*(?:the\s+)?(?:(%s)\s*(%s)?|(%s)?\s*(%s))"
     % (METRIC_RE, METRIC_RE, ORDINAL_RE, SUPERLATIVE_RE, ORDINAL_RE, SUPERLATIVE_RE),
     "pair"),
    # "a Sharpe ranks 9th", "annualized ranks 22nd"
    (r"(%s)[^.]{0,25}?\brank(?:s|ed)?\s+(%s)" % (METRIC_RE, ORDINAL_RE), "trailing_rank"),
    # "the fourth shallowest drawdown", "the deepest drawdown"
    (r"\bthe\s+(?:(%s)\s+)?(%s)\s+(%s)" % (ORDINAL_RE, SUPERLATIVE_RE, METRIC_RE), "leading"),
    # "volatility the fourth lowest", "volatility is the lowest in this library"
    (r"(%s)[^.]{0,20}?\b(?:is|are|was)?\s*(?:the\s+)?(%s)?\s*(%s)\b%s"
     % (METRIC_RE, ORDINAL_RE, SUPERLATIVE_RE, TRAILING_END), "trailing_super"),
]


def prose_fields(s):
    """Every authored string on a strategy, with a path for reporting."""
    out = []

    def walk(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, "%s.%s" % (path, k))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, "%s[%d]" % (path, i))
        elif isinstance(node, str):
            out.append((path, node))

    for key in ("tldr", "assumptions", "regimes", "regime_note", "risk_profile",
                "how_it_works", "author_note", "description"):
        if key in s and s[key]:
            walk(s[key], key)
    return out


def rankings(visible):
    """rank[(field, high_first)][slug] -> 1-based position, ties shared.

    Competition ranking, so two strategies with identical records are both #1
    and neither is #2. Without it "ties for the longest record in this library"
    fails on whichever of the pair sorts second, which is a true sentence being
    called false.
    """
    out = {}
    for _, field in METRICS:
        for high_first in (True, False):
            values = [(s["slug"], s.get(field, 0)) for s in visible]
            table = {}
            for slug, value in values:
                if high_first:
                    better = sum(1 for _, other in values if other > value)
                else:
                    better = sum(1 for _, other in values if other < value)
                table[slug] = better + 1
            out[(field, high_first)] = table
    return out


def to_int(token):
    token = token.lower()
    if token in ORDINALS:
        return ORDINALS[token]
    return int(re.sub(r"\D", "", token))


def in_scope(sentence, start, end):
    """Is the library named close enough to this match to be its scope?"""
    window = sentence[max(0, start - SCOPE_WINDOW):min(len(sentence), end + SCOPE_WINDOW)]
    return bool(LIBRARY_RE.search(window))


def claims(sentence):
    """Every (field, position, high_first) this sentence actually asserts."""
    out = []
    seen = set()
    for pattern, kind in TEMPLATES:
        for m in re.finditer(pattern, sentence, re.I):
            if not in_scope(sentence, m.start(), m.end()):
                continue
            groups = m.groups()
            if kind == "pair":
                fields = [metric_of(groups[0]), metric_of(groups[1])]
                # Two arrangements share this template: "both rank 12th" puts
                # the ordinal in group 3, "are both the highest" puts the
                # superlative in group 5 with its own optional ordinal in 4.
                ordinal = groups[2] or groups[4]
                position = to_int(ordinal) if ordinal else 1
                word = (groups[3] or groups[5] or "").lower()
            elif kind == "trailing_rank":
                fields = [metric_of(groups[0])]
                position = to_int(groups[1])
                word = ""
            elif kind == "leading":
                fields = [metric_of(groups[2])]
                position = to_int(groups[0]) if groups[0] else 1
                word = groups[1].lower()
            else:
                fields = [metric_of(groups[0])]
                position = to_int(groups[1]) if groups[1] else 1
                word = groups[2].lower()

            for field in fields:
                if not field:
                    continue
                if word:
                    high_first = HIGH_FIRST[word]
                    if field == "max_drawdown" and word in DRAWDOWN_OVERRIDE:
                        high_first = DRAWDOWN_OVERRIDE[word]
                else:
                    high_first = None
                key = (field, position, high_first)
                if key not in seen:
                    seen.add(key)
                    out.append(key)
    return out


def default_direction(field, high_first):
    """A bare "ranks 9th" carries no superlative, so pick the natural order."""
    if high_first is not None:
        return high_first
    # Ranking without a direction word means "best first" in every observed use.
    return field != "max_drawdown"


def main():
    verbose = "--verbose" in sys.argv
    data = json.loads((BASE_DIR / "data" / "strategies.json").read_text(encoding="utf-8"))
    visible = [s for s in data if not s.get("hidden")]
    rank = rankings(visible)

    checked = hedged = 0
    problems = []

    for s in visible:
        for path, text in prose_fields(s):
            for sentence in re.split(r"(?<=[.!?])\s+", text):
                if not LIBRARY_RE.search(sentence):
                    continue
                if HEDGE_RE.search(sentence) and not re.search(
                        r"\brank(?:s|ed)?\s+%s\b" % ORDINAL_RE, sentence, re.I):
                    hedged += 1
                    continue
                for field, position, high_first in claims(sentence):
                    if field not in {f for _, f in METRICS}:
                        continue
                    actual = rank[(field, default_direction(field, high_first))][s["slug"]]
                    checked += 1
                    if actual != position:
                        problems.append(
                            "%s %s: claims %s is #%d, live metrics say #%d\n      %s"
                            % (s["slug"], path, field, position, actual,
                               sentence.strip()[:150]))
                    elif verbose:
                        print("  ok  %-30s %-26s #%d" % (s["slug"], field, position))

    for p in problems:
        print("  " + p)
    print("Checked %d library-wide rank claims across %d strategies "
          "(%d hedged comparatives not checkable)." % (checked, len(visible), hedged))
    if problems:
        print("FAIL: %d rank claims disagree with the live metrics." % len(problems))
        return 1
    print("PASS: every checkable rank claim matches the live metrics.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
