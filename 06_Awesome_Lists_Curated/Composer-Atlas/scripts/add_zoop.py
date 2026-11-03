#!/usr/bin/env python3
"""
add_zoop.py: One-time script that added the "Zoop's Strategies" glossary entry
(slug: zoop) and applied the 'zoop' tag to all 12 zoops-* strategies in
data/strategies.json.

Already applied as of v1.5.3 (2026-06-15). Safe to re-run, duplicate-slug check
will abort without writing if entry is already present.

Usage:
    python scripts/add_zoop.py
"""

import json
from pathlib import Path

BASE_DIR      = Path(__file__).resolve().parent.parent
GLOSSARY_JSON = BASE_DIR / "data" / "glossary.json"
GLOSSARY_JS   = BASE_DIR / "data" / "glossary.js"
STRATEGIES_JSON = BASE_DIR / "data" / "strategies.json"
STRATEGIES_JS   = BASE_DIR / "data" / "strategies.js"

ZOOP_ENTRY = {
  "slug": "zoop",
  "name": "Zoop's Strategies",
  "category": "strategy-concept",
  "description": "A curated collection of Composer.trade symphonies built by Zoop (Azqato), an investor, developer, and community builder who shares systematic leveraged ETF strategies on Twitch and YouTube.",
  "formula": None,
  "related_tags": ["zoop"],
  "last_updated": "2026-06-15",
  "sections": [
    {
      "title": "Who Is Zoop?",
      "paragraphs": [
        "Zoop, also known online as Azqato, is an investor, developer, and community builder who creates content across Twitch and YouTube covering gaming, investing, and music production. He is the founder of B5TA, a gaming community built around RuneScape and Discord, and the creator of the Composer.trade symphonies documented in this library.",
        "Zoop approaches investing the same way he approaches game development and community-building: systematically, iteratively, and with a focus on sharing the process with others. The strategies in this library are the result of years of research into leveraged ETF behavior, regime-detection signals, and risk management techniques, refined through community feedback and live performance tracking.",
        "More about Zoop: https://azqato.com/about.html"
      ]
    },
    {
      "title": "The Strategy Suite",
      "paragraphs": [
        "The zoops-* strategies are Zoop's primary Composer.trade symphony collection, each built around a shared philosophy: use 3x leveraged Nasdaq ETFs (primarily TQQQ) during confirmed bull markets, and rotate to defensive or inverse positions when trend signals break. The 12 strategies in this collection span a spectrum from capital-preservation-first (2026 Frontrunner) to high-conviction aggressive (Sometimes TQQQ, Leveraged TQQQ Symphony).",
        "Each strategy shares a common lineage: the 2026 Frontrunner is the base layer, using RSI-triggered dip-buy signals on a universe of leveraged ETFs with BIL as the default. The other strategies layer additional macro signals, sector momentum filters, and bear-mode intelligence on top of this foundation, each one a different answer to the question of how aggressively to pursue returns within a risk-managed framework.",
        "Across the 12 zoops-* strategies, the backtested annualized return ranges from ~92% (2026 Frontrunner) to ~280% (KMLM Switcher), with Sharpe ratios from ~1.63 to ~2.63 and max drawdowns from ~−22% (2026 Frontrunner) to ~−66% (SOXL Growth). Backtest lengths vary, the 2026 Frontrunner spans ~8.4 years and the KMLM Switcher ~5.5 years, while the remaining strategies cover ~14.2 years, so headline figures are not all measured over the same window. This spread reflects the spectrum of risk tolerance the collection is designed to address."
      ],
      "table": {
        "headers": ["Strategy", "ARR", "Sharpe", "Max DD"],
        "rows": [
          ["2026 Frontrunner", "~91%", "~1.78", "~−22%"],
          ["Holy Grail 2026", "~113%", "~1.65", "~−45%"],
          ["TQQQ Long Term 2026", "~111%", "~1.63", "~−46%"],
          ["Excellent Adventure 2026", "~122%", "~1.82", "~−46%"],
          ["Sometimes TQQQ 2026", "~182%", "~2.47", "~−35%"],
          ["Safety Checks 2026", "~103%", "~1.63", "~−43%"],
          ["Manhattan Project 2026", "~154%", "~2.10", "~−35%"],
          ["KMLM Switcher 2026", "~280%", "~2.63", "~−29%"],
          ["UPRO FTLT 2026", "~94%", "~1.64", "~−33%"],
          ["Leveraged TQQQ Symphony 2026", "~109%", "~1.64", "~−48%"],
          ["TQQQ 200d MA 3x 2026", "~109%", "~1.65", "~−39%"],
          ["SOXL Growth 2026", "~164%", "~1.75", "~−66%"]
        ]
      }
    },
    {
      "title": "Design Philosophy",
      "paragraphs": [
        "Zoop's strategies share several design principles that distinguish them as a coherent system rather than a collection of unrelated symphonies. First: the primary defense mechanism is always a combination of macro trend confirmation (SPY or QQQ above key moving averages) and RSI-based dip-buy signals, both protective and opportunistic at the same time. The strategy exits leveraged positions when the macro trend breaks, but actively re-enters at panic RSI levels rather than waiting passively in cash.",
        "Second: SH (1x inverse S&P 500) is the default bear-mode hold across most zoops-* strategies, not BIL. This is an explicit directional view: when the bull-regime conditions break, the market is more likely continuing to fall than recovering, so holding SH generates returns from that decline rather than sitting at the risk-free rate. This distinguishes the zoops-* strategies from purely trend-following approaches that use cash as the defensive position.",
        "Third: each strategy in the collection is designed to be held as a single portfolio allocation, not combined with each other. The strategies overlap significantly in signal logic, combining two zoops-* strategies would create correlated double-exposure rather than meaningful diversification. The collection exists to give investors of different risk tolerances a single appropriate choice, not to be held simultaneously."
      ]
    },
    {
      "title": "Community and Transparency",
      "paragraphs": [
        "Zoop publishes and discusses his strategies publicly, sharing the signal logic, backtest methodology, and performance tracking openly with his community on Twitch and YouTube. Composer Atlas was built to document this library in one organized, searchable place, providing the in-depth explanations, signal breakdowns, and risk metric comparisons that aren't possible within Composer.trade's interface alone.",
        "The strategies are identified in Composer.trade with the 'zoops-' prefix, making them discoverable and attributable. The '2026' suffix in each strategy name reflects the year these versions were refined and published, Zoop iterates on his strategy suite over time, and the year suffix helps track which version a given backtest represents.",
        "To follow Zoop's strategy updates, community discussions, and live performance tracking, visit https://azqato.com or find him as Azqato on Twitch and YouTube."
      ]
    }
  ]
}

ZOOPS_SLUGS = [
    'zoops-2026-frontrunner',
    'zoops-holy-grail-2026',
    'zoops-tqqq-long-term-2026',
    'zoops-excellent-adventure-2026',
    'zoops-sometimes-tqqq-2026',
    'zoops-safety-checks-2026',
    'zoops-manhattan-project-2026',
    'zoops-kmlm-switcher-2026',
    'zoops-upro-ftlt-2026',
    'zoops-leveraged-tqqq-symphony-2026',
    'zoops-tqqq-200d-ma-3x-2026',
    'zoops-soxl-growth-2026',
]


def main():
    # ---- glossary.json ----
    glossary = json.loads(GLOSSARY_JSON.read_text(encoding="utf-8"))

    if any(e['slug'] == 'zoop' for e in glossary):
        print('ABORT: zoop slug already exists in glossary')
        return

    glossary.append(ZOOP_ENTRY)
    GLOSSARY_JSON.write_text(
        json.dumps(glossary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f'glossary.json: {len(glossary)} entries')

    # ---- glossary.js ----
    content = GLOSSARY_JSON.read_text(encoding="utf-8")
    js = (
        "// To update content: edit this file and data/glossary.json in sync.\n"
        f"window.GLOSSARY_DATA = {content.rstrip()};\n"
    )
    GLOSSARY_JS.write_text(js, encoding="utf-8")
    print('glossary.js written')

    # ---- strategies.json ----
    strategies = json.loads(STRATEGIES_JSON.read_text(encoding="utf-8"))
    slug_map = {s['slug']: i for i, s in enumerate(strategies)}

    for slug in ZOOPS_SLUGS:
        if slug not in slug_map:
            print(f'WARNING: strategy slug not found: {slug}')
            continue
        tags = strategies[slug_map[slug]].setdefault('tags', [])
        if 'zoop' not in tags:
            tags.append('zoop')
            print(f'Added zoop tag to {slug}')

    STRATEGIES_JSON.write_text(
        json.dumps(strategies, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print('strategies.json written')

    # ---- strategies.js ----
    header = STRATEGIES_JS.read_text(encoding="utf-8").split('\n')[0]
    s_content = STRATEGIES_JSON.read_text(encoding="utf-8")
    s_js = header + "\nwindow.STRATEGIES_DATA = " + s_content.rstrip() + ";\n"
    STRATEGIES_JS.write_text(s_js, encoding="utf-8")
    print('strategies.js written')


if __name__ == "__main__":
    main()
