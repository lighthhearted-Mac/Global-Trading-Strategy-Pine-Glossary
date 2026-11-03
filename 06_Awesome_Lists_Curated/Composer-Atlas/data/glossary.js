// To update content: edit this file and data/glossary.json in sync.
window.GLOSSARY_DATA = [
  {
    "slug": "rsi",
    "name": "RSI",
    "category": "indicator",
    "description": "A momentum oscillator that measures the speed and magnitude of recent price changes, ranging from 0 to 100.",
    "formula": "RSI = 100 − (100 / (1 + RS)), where RS = average gain / average loss over N periods",
    "related_tags": [
      "rsi"
    ],
    "last_updated": "2026-06-08",
    "sections": [
      {
        "title": "Definition",
        "paragraphs": [
          "RSI (Relative Strength Index) is a momentum oscillator that measures how fast and how much an asset's price has moved over a recent period, expressed as a number between 0 and 100. Developed by J. Welles Wilder in 1978, it remains one of the most widely used indicators in technical analysis.",
          "A high RSI suggests the asset has risen quickly and may be overextended. A low RSI suggests it has fallen quickly and may be oversold."
        ]
      },
      {
        "title": "How It Works",
        "paragraphs": [
          "RSI is calculated over a lookback window, the standard is 14 periods (days, weeks, or bars depending on the chart timeframe).",
          "For each period, identify whether the close was higher or lower than the previous close. Separate these into gains and losses. Calculate the average gain and average loss over the lookback window. Divide average gain by average loss to get the Relative Strength (RS). Apply the formula: RSI = 100 − (100 / (1 + RS)).",
          "Example: If over 14 trading days, average daily gain = 1.2% and average daily loss = 0.6%, then RS = 2.0 and RSI = 100 − (100 / 3) = 66.7.",
          "The result is always between 0 and 100. The closer to 100, the stronger the recent upward momentum. The closer to 0, the stronger the recent downward momentum."
        ]
      },
      {
        "title": "In Practice",
        "paragraphs": [
          "RSI is one of the most commonly used signals in Composer.trade symphonies. Strategy authors use it to filter entries and exits.",
          "If RSI(14) < 30, buy: the asset is considered oversold; potential recovery opportunity. If RSI(14) > 70, sell or reduce, the asset is considered overbought; reduce risk exposure.",
          "Some strategies use RSI as a confirmation signal alongside trend indicators. For example, a strategy might only buy TQQQ when the price is above its 200-day moving average AND the RSI is below 70 (not overbought). This combination reduces the chance of entering at the peak of a short-term surge.",
          "In the zoop's strategy library on Composer Atlas, RSI is used by the Holy Grail, Sometimes TQQQ, Manhattan Project, and Leveraged TQQQ Symphony strategies as a precision timing tool."
        ],
        "table": {
          "headers": [
            "RSI Level",
            "Interpretation"
          ],
          "rows": [
            [
              "< 30",
              "Oversold: historically associated with potential recovery"
            ],
            [
              "30 – 50",
              "Weak / recovering momentum"
            ],
            [
              "50 – 70",
              "Neutral to strong momentum"
            ],
            [
              "> 70",
              "Overbought: historically associated with potential pullback"
            ]
          ]
        }
      },
      {
        "title": "Limitations",
        "paragraphs": [
          "RSI can stay extreme: During sustained trends, RSI can remain above 70 or below 30 for weeks or months. Using RSI crossings as standalone buy/sell signals produces many false positives.",
          "Lookback sensitivity: A 14-period RSI on a daily chart behaves completely differently from a 14-period RSI on a weekly chart. Always specify the timeframe.",
          "Does not predict magnitude: RSI signals direction tendency, not how much a price will move or for how long.",
          "Prone to divergence misinterpretation: RSI divergence from price is often cited as a reversal signal, but many divergences fail to produce reversals."
        ]
      },
      {
        "title": "Building with RSI in Composer.trade",
        "paragraphs": [
          "RSI is the most deployable oscillator in Composer.trade's signal library because it translates complex momentum dynamics into a single, actionable number. Unlike trend indicators like the 200-day moving average, which tell you the broad direction of the market, RSI tells you how stretched that trend has become. A strategy built on trend signals alone will often enter a position after a large run-up and get punished; RSI prevents this by filtering out entries where the asset has already moved too far, too fast. This makes it especially powerful as a secondary confirmation layer that protects trend-following logic from buying at exhaustion points.",
          "The most productive use of RSI in Composer.trade is as an entry quality filter. Rather than using RSI as the primary signal, high-performing symphonies use it as a gating condition that the primary signal must clear. A symphony holding TQQQ whenever QQQ is above its 200-day moving average would benefit from adding an RSI condition that prevents entry when RSI(14) is above 70. This does not change the strategy's directional thesis, it still believes QQQ is in an uptrend, but it avoids entering leveraged positions at the most dangerous moments, when momentum is overextended and a mean-reversion pullback is statistically more likely.",
          "RSI also enables a completely different strategy type: mean reversion. In a mean-reversion symphony, you are not following the trend but betting against short-term overextension. When RSI drops below 30, the asset is considered oversold and a bounce is expected; the symphony enters a long position. When RSI rises above 70, the asset is overbought and the symphony exits or rotates to something with lower RSI. This works particularly well for broad indices like QQQ or SPY because they tend to revert after short-term extremes. Pure mean-reversion symphonies are rare in practice, but RSI-based conditions appear in almost every sophisticated symphony in Composer.trade as a timing precision tool.",
          "For leveraged ETF symphonies specifically, RSI is not optional, it is a survival mechanism. A 3x leveraged instrument like TQQQ amplifies not just returns but also the cost of buying at the wrong time. If you buy TQQQ when QQQ's RSI is at 80 and a 15% correction follows, the leveraged position will lose approximately 45%. Had the same symphony required RSI to be below 70 at entry, it would have either avoided that entry or entered at a more favorable price during the subsequent pullback. Over many years, this RSI gate compounds significantly: fewer bad entries means fewer deep drawdowns, and fewer deep drawdowns means more capital available to compound during the favorable periods.",
          "A practical Composer.trade symphony incorporating RSI might look like this: the primary signal is QQQ crossing above its 200-day moving average, establishing that the market is in a bull trend. Within that regime, the strategy checks RSI(14) of QQQ before every rebalance. If RSI is below 70, the strategy holds TQQQ for full 3x leverage exposure. If RSI is above 70, the strategy holds QQQ directly, reducing leverage while maintaining market exposure. If QQQ falls below its 200-day moving average, the strategy exits entirely to BIL. This three-tier structure, full leveraged, unlevered, cash, uses RSI to add a middle state between maximum exposure and full exit, reducing whipsaw compared to a binary on/off system."
        ]
      }
    ]
  },
  {
    "slug": "200d-ma",
    "name": "200-Day Moving Average",
    "category": "indicator",
    "description": "A long-term trend indicator calculated as the average closing price over the past 200 trading days, used to identify bull and bear market regimes.",
    "formula": "200d MA = (Sum of closing prices over 200 trading days) / 200",
    "related_tags": [
      "200d-ma"
    ],
    "last_updated": "2026-06-08",
    "sections": [
      {
        "title": "Definition",
        "paragraphs": [
          "The 200-Day Moving Average (200d MA) is one of the most widely followed trend indicators in finance. It calculates the average closing price of an asset over the most recent 200 trading days (roughly 40 calendar weeks or 10 months).",
          "When an asset's current price is above its 200d MA, the asset is generally considered to be in a long-term uptrend. When the price is below the 200d MA, it is considered to be in a long-term downtrend."
        ]
      },
      {
        "title": "How It Works",
        "paragraphs": [
          "The calculation is straightforward: add up the closing prices from the last 200 trading days and divide by 200. As each new day passes, the oldest day drops off and the newest is added, this is why it's called a \"moving\" average.",
          "The 200d MA moves slowly because it averages such a long period. This makes it resistant to short-term noise, but also means it lags behind rapid price changes. When a market sells off sharply, the 200d MA will still be far above the current price for some time.",
          "Key crossover signals: Price crosses above 200d MA, bullish regime signal, often marks the transition from bear to bull market. Price crosses below 200d MA, bearish regime signal, often marks the transition from bull to bear market."
        ],
        "table": {
          "headers": [
            "Signal",
            "Interpretation"
          ],
          "rows": [
            [
              "Price > 200d MA",
              "Long-term uptrend: risk-on"
            ],
            [
              "Price = 200d MA",
              "Inflection zone: signals mixed"
            ],
            [
              "Price < 200d MA",
              "Long-term downtrend: risk-off"
            ],
            [
              "50d MA crosses above 200d MA",
              "\"Golden Cross\": bullish medium-term signal"
            ],
            [
              "50d MA crosses below 200d MA",
              "\"Death Cross\": bearish medium-term signal"
            ]
          ]
        }
      },
      {
        "title": "In Practice",
        "paragraphs": [
          "The 200d MA is used in Composer.trade symphonies as a regime filter, deciding whether to hold risky assets at all. A common pattern: If QQQ price > QQQ 200d MA → hold TQQQ (leveraged upside exposure). If QQQ price < QQQ 200d MA → hold BIL or cash (defensive posture).",
          "This single rule has historically been one of the most effective ways to avoid holding leveraged ETFs through major bear markets (2000–2002, 2008–2009, early 2020). The strategy accepts being whipsawed during choppy markets in exchange for avoiding the devastating compounding losses of 3x leverage in a sustained downtrend.",
          "The TQQQ 200d MA 3x Leverage strategy on Composer Atlas is the most transparent example of this approach, it uses this single signal with no additional filters."
        ]
      },
      {
        "title": "Limitations",
        "paragraphs": [
          "Lags badly during rapid reversals: The 200d MA can be 15–25% above a market that is currently in free-fall. By the time it signals a downtrend, significant losses may have already occurred.",
          "Produces whipsaw in sideways markets: When prices oscillate near the 200d MA without a clear trend, the signal generates repeated false crossings, each causing a trade.",
          "Does not predict duration: Being above the 200d MA does not tell you how much further prices will rise before reversing.",
          "Different assets require recalibration: A 200d MA works well for major equity indices but may be poorly suited for high-volatility individual sectors or cryptocurrencies."
        ]
      },
      {
        "title": "Building with the 200-Day MA in Composer.trade",
        "paragraphs": [
          "The 200-day moving average is the single most impactful signal available in Composer.trade because it gives systematic investors a clear, objective definition of a bull market versus a bear market. Without this regime filter, a strategy has no way to distinguish between a healthy market environment where risk-taking is rewarded and a deteriorating one where leveraged exposure leads to catastrophic losses. The 200d MA solves this problem elegantly: when the price of your target asset is above its 200-day average, you are operating in a regime where historical evidence strongly favors equity exposure; when price is below, you rotate to safety. No other signal accomplishes this macro-level regime classification with comparable simplicity and effectiveness.",
          "The foundational use of the 200d MA in Composer.trade is as a binary gate on leveraged ETF exposure. The most durable symphonies follow this structure: evaluate whether QQQ is trading above its 200-day moving average at each rebalance date, if yes, hold TQQQ; if no, hold a defensive asset such as BIL or SHY. This one rule, applied consistently, has historically avoided the three most devastating leveraged ETF periods: the dot-com bust (2000–2002), the global financial crisis (2008–2009), and the COVID crash (early 2020). In each case, QQQ dropped below its 200d MA weeks before the most severe losses, providing a systematic exit signal that a discretionary investor would likely have ignored.",
          "One of the most powerful decisions a symphony builder can make is which asset's 200d MA to use as the signal. The obvious choice is the asset you are trading, use QQQ's 200d MA to gate TQQQ exposure. But more sophisticated approaches use a broader market filter: apply the S&P 500's 200d MA as a macro regime gate, even when the symphony trades TQQQ. The logic is that bear markets tend to be broad, when the S&P 500 enters a downtrend, Nasdaq leveraged instruments typically fall harder and faster. Comparing both variants in Composer.trade's backtester helps identify which gate provides better protection for the specific instrument being traded.",
          "Combining the 200d MA with a second signal dramatically increases a symphony's precision. A common and effective combination pairs the 200d MA as a regime filter with RSI as a timing layer: the symphony requires price to be above the 200d MA (confirming the trend) and RSI to be below 70 (confirming the entry is not overbought). Another powerful combination pairs the 200d MA with a short-term momentum trigger: the symphony enters leveraged exposure only when price is above its 200d MA and has also closed above its 50-day moving average, using the 50d MA as a faster-reacting confirmation signal. These combinations require more conditions to be met before entering, which means fewer trades, but each trade has higher historical quality.",
          "A fully-realized Composer.trade symphony built around the 200d MA might implement a tiered response system rather than a binary on/off. Consider three tiers: when QQQ is more than 2% above its 200d MA, hold TQQQ at full allocation, this is the clearest bull signal. When QQQ is within 2% of its 200d MA in either direction, hold QQQ directly (unlevered), the ambiguous zone reduces leverage risk during potential crossover volatility. When QQQ is more than 2% below its 200d MA, hold BIL, confirmed downtrend calls for full defensive posture. This buffer zone approach reduces whipsaw significantly: instead of triggering a new trade every time price crosses the 200d MA by a tick, the symphony only changes allocation when price moves meaningfully into a new tier."
        ]
      }
    ]
  },
  {
    "slug": "momentum",
    "name": "Momentum Investing",
    "category": "strategy-concept",
    "description": "A strategy that buys assets with strong recent performance and sells assets with weak recent performance, based on the empirical tendency for trends to persist.",
    "formula": null,
    "related_tags": [
      "momentum"
    ],
    "last_updated": "2026-06-08",
    "sections": [
      {
        "title": "Definition",
        "paragraphs": [
          "Momentum investing is a strategy based on the empirical observation that assets which have performed well recently tend to continue performing well in the near term, and assets that have performed poorly tend to continue performing poorly.",
          "This persistence of returns: known as momentum, has been documented across asset classes, geographies, and time periods in academic research dating back to the early 1990s."
        ]
      },
      {
        "title": "How It Works",
        "paragraphs": [
          "Momentum strategies typically measure recent performance over a lookback window (commonly 3, 6, or 12 months) and rank assets from best to worst performers. The strategy then buys the top performers and avoids or short-sells the bottom performers.",
          "Time-Series Momentum (Absolute Momentum): Compares the asset's recent return to a threshold (often zero or the risk-free rate). If the asset's 12-month return is positive, hold it. If negative, exit to cash. This captures whether an asset is trending up or down.",
          "Cross-Sectional Momentum (Relative Momentum): Ranks multiple assets against each other. Hold the top X% of performers and avoid the bottom X%. This captures which assets are leading vs. lagging in a given period.",
          "Most Composer.trade symphonies use a blend of both: they filter for an uptrend (time-series) and then pick the leading instrument within that trend (cross-sectional)."
        ]
      },
      {
        "title": "In Practice",
        "paragraphs": [
          "In the context of leveraged ETF strategies, momentum typically manifests as: holding TQQQ when QQQ is trending up (the Nasdaq is in momentum and the leveraged ETF amplifies it), and rotating away when momentum weakens, exiting to a defensive asset when recent returns fall below a threshold or when a faster-moving asset takes the lead.",
          "The simplest momentum signal is comparing recent price to a moving average (e.g., the 200d MA). More sophisticated approaches use rate-of-change calculations over a fixed lookback window, normalized by volatility.",
          "Every strategy in the Composer Atlas library is fundamentally a momentum strategy, they all seek to hold leveraged equity when equity momentum is positive and rotate to defensive assets when it isn't."
        ]
      },
      {
        "title": "Limitations",
        "paragraphs": [
          "Momentum crashes: Momentum strategies can suffer sudden, severe reversals during rapid market rotations. When a downtrend reverses sharply (e.g., March 2020 COVID recovery), momentum strategies holding short or defensive positions can be caught on the wrong side.",
          "Transaction costs: Strategies that rebalance frequently to capture momentum can accumulate significant transaction costs that erode the edge.",
          "Crowding: When too many investors follow the same momentum signals, they create crowded trades that amplify crashes when those positions unwind simultaneously.",
          "Lookback sensitivity: A 3-month momentum signal can produce completely different signals than a 12-month signal for the same asset. Results vary significantly based on the chosen lookback period."
        ]
      },
      {
        "title": "Building Momentum Strategies in Composer.trade",
        "paragraphs": [
          "Momentum is not just one signal among many in Composer.trade, it is the underlying principle that makes the entire platform's approach to systematic investing work. Every symphony on Composer.trade is, at its core, a momentum strategy: they all seek to hold assets when they are trending positively and rotate away when momentum deteriorates. The academic evidence for momentum is unusually strong: it has been documented in U.S. equities since the 1920s, in international markets, in bonds, in commodities, and across virtually every studied asset class. Unlike many market anomalies that disappear after publication, momentum has persisted for decades of out-of-sample testing, making it one of the most durable foundations for systematic strategy design.",
          "Time-series momentum: also called absolute momentum, is the simplest and most reliable starting point for a Composer.trade symphony. The core idea: if an asset's return over a recent period is positive, hold it; if negative, exit to cash or bonds. A symphony implementing pure 12-month absolute momentum would buy QQQ when its 12-month return is positive and switch to BIL when it is negative. Backtested over decades, this single rule avoids the worst bear market losses while capturing most bull market gains. Bear markets almost always build up over many months, meaning 12-month momentum turns negative before the most catastrophic losses occur, providing a reliable early exit signal that requires no interpretation.",
          "Cross-sectional momentum: choosing the best-performing asset from a universe of options, is what separates good symphonies from great ones. Instead of just asking whether an asset is trending up, cross-sectional momentum asks which asset in the universe is trending up the most. A symphony might evaluate TQQQ, UPRO, and GLD at each rebalance date and allocate 100% to whichever has the highest trailing 3-month return. This produces a symphony that adapts to changing market leadership: in tech bull markets it holds TQQQ, during equity downturns it might rotate to gold, and in uncertain environments it holds whichever segment is showing the most resilience. The power is that it does not require predicting which asset will lead, it simply follows demonstrated leadership.",
          "Lookback period selection is one of the most important decisions in building a momentum symphony, and Composer.trade's backtester makes it possible to systematically compare options. A 1-month lookback is reactive and captures very short-term momentum but produces many whipsaw trades. A 12-month lookback is slow and smooth but misses rapid trend changes. Most practitioners find that 3–6 month lookback periods strike the best balance for equity ETF symphonies: fast enough to exit before bear markets deepen but slow enough to avoid being shaken out by normal corrections. When using momentum to rotate among leveraged instruments, a shorter lookback (1–3 months) often works better because leveraged ETFs can move dramatically in short periods.",
          "A sophisticated Composer.trade symphony using multiple momentum timeframes might work as follows: a 12-month momentum filter confirms the macro trend is positive (the strategy is active). Within that filter, a 3-month relative momentum ranking selects among TQQQ, UPRO, and KMLM, holding whichever has the highest 3-month return. If no asset in the universe shows positive 12-month momentum, the strategy defaults to BIL. This two-layer structure uses long-term absolute momentum to control overall risk, only active when the broad trend is positive, and short-term relative momentum to select the best opportunity within that positive regime. The result is a symphony that avoids prolonged bear markets while rotating to the leading instrument during bull phases, capturing more of the uptrend than a single-asset strategy."
        ]
      }
    ]
  },
  {
    "slug": "vix-tiers",
    "name": "VIX Tiers",
    "category": "strategy-concept",
    "description": "A volatility regime framework that segments the CBOE VIX index into distinct tiers to determine appropriate risk allocation, aggressive in low-VIX environments, defensive in high-VIX environments.",
    "formula": null,
    "related_tags": [
      "vix-tiers"
    ],
    "last_updated": "2026-06-08",
    "sections": [
      {
        "title": "Definition",
        "paragraphs": [
          "VIX tiers is a systematic approach to position-sizing and asset allocation that uses the CBOE Volatility Index (VIX) as a regime indicator. Rather than treating every market environment the same, tier-based VIX strategies recognize that the optimal level of risk-taking differs significantly when markets are calm versus when they are in distress.",
          "High VIX levels historically signal elevated fear and increased probability of continued volatility, exactly when leveraged ETF exposure is most dangerous."
        ]
      },
      {
        "title": "How It Works",
        "paragraphs": [
          "The VIX (often called the \"fear gauge\") measures the market's expected 30-day volatility for the S&P 500, derived from options prices.",
          "A VIX tier strategy maps each tier to a specific allocation: Low tier (< 15), full leveraged equity exposure (e.g., hold TQQQ). Moderate tier (15–20), partial leverage or standard equity. High tier (> 25), reduce or eliminate leveraged positions; rotate to defensive assets. Extreme tier (> 35), full defensive posture (cash, BIL, or inverse ETFs)."
        ],
        "table": {
          "headers": [
            "VIX Level",
            "Tier",
            "Interpretation"
          ],
          "rows": [
            [
              "< 15",
              "Low / Calm",
              "Markets are complacent; low fear; bull market context"
            ],
            [
              "15 – 20",
              "Moderate",
              "Normal uncertainty; default operating environment"
            ],
            [
              "20 – 25",
              "Elevated",
              "Heightened concern; increased probability of volatility ahead"
            ],
            [
              "25 – 35",
              "High / Stressed",
              "Significant fear; markets pricing in meaningful downside risk"
            ],
            [
              "> 35",
              "Extreme",
              "Crisis-level fear; historical context: COVID crash, GFC, flash crashes"
            ]
          ]
        }
      },
      {
        "title": "In Practice",
        "paragraphs": [
          "In Composer.trade symphonies, VIX tier rules often appear as nested conditional logic: If VIX < 20, hold TQQQ. Else if VIX < 30, hold SPY (unlevered). Else, hold BIL (cash equivalent).",
          "This structure allows a strategy to be aggressive in benign conditions while systematically reducing risk as volatility rises. Critically, this happens automatically, the strategy doesn't require a judgment call when markets are most stressful.",
          "The Safety Checks and Manhattan Project strategies in Composer Atlas incorporate VIX tier logic as one of their multi-signal confirmation gates."
        ]
      },
      {
        "title": "Limitations",
        "paragraphs": [
          "VIX spikes are often brief: A VIX spike that triggers a defensive rotation may last only a few days before markets recover. By the time the strategy exits and re-enters, the best recovery gains may already be captured by others.",
          "VIX measures implied, not realized, volatility: High VIX signals fear and uncertainty but does not guarantee that realized volatility will follow. Markets sometimes recover sharply even from elevated VIX levels.",
          "Regime boundaries are arbitrary: The choice of 20, 25, or 30 as tier thresholds is not derived from a universal formula. Different strategies use different thresholds, and the \"right\" threshold depends heavily on the lookback period and asset class.",
          "VIX applies to S&P 500 options: VIX is constructed from S&P 500 implied volatility. It may be less indicative of risk in semiconductor (SOXL) or Nasdaq-heavy (TQQQ) strategies."
        ]
      },
      {
        "title": "Building VIX-Tiered Symphonies in Composer.trade",
        "paragraphs": [
          "VIX tiers represent the most sophisticated approach to risk management available in Composer.trade, because they respond to the market's own assessment of future danger rather than simply measuring what has already happened. Moving averages and momentum signals are inherently backward-looking, they tell you about what prices have done. The VIX, by contrast, is forward-looking by construction: it measures how much uncertainty options market participants are pricing into the next 30 days. When the VIX spikes, sophisticated, large-capital market participants are buying insurance against losses they fear are coming. A VIX-tiered symphony respects this collective intelligence and automatically adjusts its leverage exposure before the feared losses actually arrive.",
          "The most powerful use of VIX tiers in Composer.trade is as a dynamic leverage governor. Rather than a single on/off switch for TQQQ exposure, a VIX-tiered symphony maps different VIX levels to different allocation levels: at low VIX (under 15), the market is calm and TQQQ at full allocation is appropriate. At moderate VIX (15–20), the atmosphere is shifting and stepping down to QQQ reduces risk without eliminating market exposure. At elevated VIX (20–30), the strategy moves to BIL, protecting capital while uncertainty passes. At extreme VIX (above 30), the strategy may allocate to VIXY or a volatility instrument that profits from continued fear, turning the risk signal into a return opportunity. This graduated response produces far fewer whipsaw trades than a binary on/off system.",
          "VIX tiers work exceptionally well as a complement to trend-following signals because they fire at different times. Trend signals like the 200d MA respond slowly to deteriorating conditions; VIX responds immediately. Combining them creates a system where the fast signal catches rapid deteriorations that trend signals miss, while the slow signal handles gradual long-term regime shifts. A Composer.trade symphony implementing this combination might use: if QQQ is above its 200d MA and VIX is below 20, hold TQQQ. If QQQ is above its 200d MA but VIX is above 20, hold QQQ. If QQQ is below its 200d MA or VIX is above 30, hold BIL. The logic requires both conditions to be favorable for full leveraged exposure, either signal deteriorating reduces risk.",
          "Position sizing based on VIX tiers allows symphonies to maintain some equity exposure even during uncertain periods, rather than going fully to cash. Instead of allocating 100% to TQQQ at low VIX and 0% at high VIX, a VIX-tiered sizing model might allocate: 100% TQQQ at VIX under 15, 70% TQQQ plus 30% BIL at VIX 15–20, 40% TQQQ plus 60% BIL at VIX 20–25, and 100% BIL above VIX 25. This gradual scaling approach reduces the whipsaw problem, a VIX spike to 21 triggers a partial reduction, not a complete exit, while still meaningfully cutting risk as volatility rises.",
          "A practical example of a complete VIX-tiered Composer.trade symphony: the primary universe is TQQQ and KMLM (managed futures, performs well in volatile or bear regimes). The VIX tier determines the allocation, VIX under 18: 100% TQQQ. VIX 18–25: 60% TQQQ, 40% KMLM. VIX above 25: 100% KMLM. This structure leverages the historically complementary relationship between leveraged equity (which suffers during high-VIX periods) and managed futures (which often thrives during high-VIX periods when trends emerge in commodities, currencies, and bonds). The VIX threshold drives the rotation, creating a symphony that is long volatility in the defensive posture and long equity during low-fear regimes."
        ]
      }
    ]
  },
  {
    "slug": "leveraged-etfs",
    "name": "Leveraged ETFs",
    "category": "asset-class",
    "description": "Exchange-traded funds that use derivatives to deliver multiples (2x or 3x) of the daily return of an underlying index, enabling amplified gains and amplified losses.",
    "formula": null,
    "related_tags": [
      "leveraged-etfs"
    ],
    "last_updated": "2026-06-08",
    "sections": [
      {
        "title": "Definition",
        "paragraphs": [
          "Leveraged ETFs are exchange-traded funds engineered to deliver a multiple of the daily return of an underlying benchmark index. A 3x leveraged ETF targeting the Nasdaq 100 will aim to return +3% when the index returns +1%, and −3% when the index returns −1%, before fees.",
          "The most prominent examples in the Composer Atlas library are TQQQ (3x QQQ/Nasdaq 100), UPRO (3x S&P 500/SPY), and SOXL (3x SOXX/Semiconductors)."
        ]
      },
      {
        "title": "How It Works",
        "paragraphs": [
          "Leveraged ETFs achieve their multiple through daily rebalancing using derivatives (futures, swaps, and options). At the end of each trading day, the fund resets its leverage ratio to maintain the target multiple for the next day.",
          "This daily reset has a critical consequence: compounding over time does not equal the simple multiple of the index's return. This effect, sometimes called volatility decay or beta decay, means: in a steadily rising market, a 3x ETF compounds faster than 3x the index; in a volatile, sideways market, a 3x ETF loses value even if the index ends flat; in a declining market, a 3x ETF loses far more than 3x.",
          "Example of volatility decay: Day 1: Index rises 10%. 3x ETF rises 30%. $100 → $130. Day 2: Index falls 10%. 3x ETF falls 30%. $130 → $91. Index net: flat. 3x ETF net: -9% from where it started."
        ],
        "table": {
          "headers": [
            "ETF",
            "Underlying",
            "Leverage",
            "Notes"
          ],
          "rows": [
            [
              "TQQQ",
              "Nasdaq 100 (QQQ)",
              "3x",
              "Most widely held; high tech concentration"
            ],
            [
              "UPRO",
              "S&P 500 (SPY)",
              "3x",
              "Broader diversification than TQQQ"
            ],
            [
              "SOXL",
              "Semiconductors (SOXX)",
              "3x",
              "Highest volatility; sector concentration"
            ]
          ]
        }
      },
      {
        "title": "In Practice",
        "paragraphs": [
          "Every strategy in the Composer Atlas library uses leveraged ETFs as its primary risk-on instrument. The common pattern: monitor signals (200d MA, RSI, VIX, momentum). When signals are favorable: hold TQQQ, UPRO, or SOXL for amplified gains. When signals deteriorate: exit to a defensive asset (BIL, cash, bonds) to avoid amplified losses.",
          "The key insight all these strategies share: holding a 3x leveraged ETF through a 50% drawdown in the underlying index produces approximately an 80–90% loss in the leveraged fund, depending on the path. Systematic exits protect against this compounding catastrophe."
        ]
      },
      {
        "title": "Limitations",
        "paragraphs": [
          "Not designed for long-term buy-and-hold: Due to daily rebalancing and volatility decay, leveraged ETFs held passively underperform 3x their benchmark over long, volatile periods.",
          "Require active management: Their value comes only when paired with systematic signals that prevent holding them through sustained bear markets.",
          "Expense ratios are high: TQQQ charges ~0.88% annually. Over years, this compounds.",
          "Liquidity risk in extreme events: During flash crashes or market halts, the bid-ask spread on leveraged ETFs can widen dramatically, making rapid exits costly.",
          "Not suitable for most retail investors: The SEC requires leveraged ETF product disclosure acknowledging that these products are not appropriate for all investors."
        ]
      },
      {
        "title": "Building Systematic Leveraged ETF Symphonies in Composer.trade",
        "paragraphs": [
          "Leveraged ETFs are the engine of the highest-returning strategies in Composer.trade, but they are an engine that destroys itself if left running unsupervised. The daily-rebalancing mechanism that makes 3x leverage possible also creates an inevitable erosion of value during volatile, sideways markets, a phenomenon called volatility decay. A symphony builder who understands this mechanism stops thinking of TQQQ as QQQ but better, and starts thinking of it as a precision instrument that performs brilliantly in specific conditions (sustained, low-volatility uptrends) and catastrophically in others (volatile bear markets). The entire architecture of every successful leveraged ETF symphony in Composer.trade is a system for being in the instrument when conditions are favorable and out of it when they are not.",
          "The first design decision for a leveraged ETF symphony is the exit rule, and it deserves more thought than the entry rule. This is counterintuitive: most investors obsess over when to buy and barely think about when to sell. But for 3x instruments, the exit rule is existential. A 50% drawdown in QQQ produces roughly an 80–90% drawdown in TQQQ; recovery from such a loss would take years even at TQQQ's exceptional compounding rate. The exit rule must be objective (no interpretation required), systematic (it fires every time conditions are met), and fast enough to catch trend breaks before they become catastrophic losses. The 200d MA is the most widely-used exit trigger; VIX tiers provide a faster secondary exit; RSI can prevent re-entry after a trend break until conditions stabilize.",
          "Choosing between TQQQ, UPRO, and SOXL for a Composer.trade symphony is a fundamental risk/return tradeoff decision. TQQQ tracks the Nasdaq 100, which is heavily concentrated in mega-cap technology, this concentration drives exceptional bull market returns but creates deeper drawdowns during tech sector corrections. UPRO tracks the S&P 500, which is more diversified across sectors, it produces lower absolute returns but also lower drawdowns and standard deviation. SOXL tracks the semiconductor sector specifically, which has produced extraordinary gains over the past decade due to AI and data center buildout, but its 65%+ max drawdown in the Composer Atlas library reflects the sector's extreme volatility. Symphony builders should match the instrument to their drawdown tolerance.",
          "Symphony architecture for leveraged ETFs follows a consistent three-stage pattern that can be adapted to any signal combination. Stage one is the regime filter: a slow-moving, reliable signal that answers whether this is a safe environment for leveraged equity, the 200d MA is the standard choice. Stage two is the confirmation signal: a faster signal that answers whether this is a good specific moment to enter or maintain exposure, RSI, short-term momentum, or a VIX check. Stage three is the defensive asset: when stage one or two fails, what does the symphony hold? The best defensive choices are BIL (near-zero risk), SHY (short-term bonds), or KMLM (managed futures, may profit during the conditions that triggered the exit). The sophistication of the symphony lies in the logic connecting these three stages.",
          "An advanced Composer.trade symphony using a leveraged ETF might incorporate regime-adjusted position sizing rather than a binary in/out signal. Consider a symphony that evaluates three conditions: the 200d MA trend status of QQQ, the current VIX level, and the 3-month momentum rank of TQQQ versus BIL. When all three are favorable, the symphony holds 100% TQQQ. When two of three are favorable, it holds 50% TQQQ and 50% QQQ, reducing leverage while maintaining equity exposure. When one or fewer are favorable, it holds 100% BIL. This vote-based system means no single indicator can force a full leveraged position, all three must agree. It also means the symphony gradually scales out as conditions deteriorate rather than exiting all at once, reducing the impact of false signals."
        ]
      }
    ]
  },
  {
    "slug": "sharpe-ratio",
    "name": "Sharpe Ratio",
    "category": "risk-metric",
    "description": "A measure of risk-adjusted return that divides excess return above the risk-free rate by the standard deviation of returns, higher is better.",
    "formula": "Sharpe Ratio = (Rp − Rf) / σp",
    "related_tags": [
      "sharpe-ratio"
    ],
    "last_updated": "2026-06-08",
    "sections": [
      {
        "title": "Definition",
        "paragraphs": [
          "The Sharpe Ratio, developed by economist William Sharpe in 1966, measures how much excess return an investment earns per unit of risk taken. It answers the question: \"For every 1% of volatility I'm accepting, how much return above the risk-free rate am I getting?\"",
          "A higher Sharpe ratio means better risk-adjusted performance, more return per unit of risk."
        ]
      },
      {
        "title": "Formula",
        "paragraphs": [
          "Sharpe Ratio = (Rp − Rf) / σp. Where: Rp = Portfolio return (annualized), Rf = Risk-free rate (often 3-month Treasury bill yield), σp = Standard deviation of portfolio returns (annualized).",
          "Example: A strategy with a 50% annualized return, a 3% risk-free rate, and a 40% annualized standard deviation has a Sharpe ratio of (0.50 − 0.03) / 0.40 = 1.175."
        ]
      },
      {
        "title": "How It Works",
        "paragraphs": [
          "The Sharpe ratio has two components: the numerator measures how much the strategy earns above \"doing nothing\" (holding the risk-free asset). The denominator penalizes for volatility, the wider the swings in returns, the lower the Sharpe ratio for a given return level.",
          "A strategy that earns 15% per year with very low volatility may have a higher Sharpe than one earning 25% per year with wild swings. This is why a simple S&P 500 index fund can have a competitive Sharpe ratio compared to many actively managed strategies."
        ],
        "table": {
          "headers": [
            "Sharpe Ratio",
            "Quality"
          ],
          "rows": [
            [
              "< 0.5",
              "Poor: not compensating for risk taken"
            ],
            [
              "0.5 – 1.0",
              "Adequate: basic risk compensation"
            ],
            [
              "1.0 – 1.5",
              "Good: solid risk-adjusted performance"
            ],
            [
              "1.5 – 2.0",
              "Very Good: strong returns for the risk taken"
            ],
            [
              "> 2.0",
              "Excellent: elite risk-adjusted performance"
            ]
          ]
        }
      },
      {
        "title": "In Practice",
        "paragraphs": [
          "When comparing two strategies with similar return profiles, the Sharpe ratio tells you which is doing more with less risk. The strategies in Composer Atlas range from Sharpe ratios of roughly 1.10 to 3.04, all above 1.0, reflecting systematic exits that reduce volatility compared to holding leveraged ETFs passively.",
          "For portfolios where stability matters, a strategy with lower absolute returns but higher Sharpe may be preferable, it means the returns are more consistent and predictable."
        ]
      },
      {
        "title": "Limitations",
        "paragraphs": [
          "Assumes normal distribution: The Sharpe ratio treats upside and downside volatility identically. A strategy with many large positive outliers and few negative ones looks \"riskier\" under Sharpe than it actually is. The Sortino ratio addresses this.",
          "Sensitive to the risk-free rate used: Sharpe ratios calculated using different risk-free rates are not directly comparable.",
          "Backtests can be misleading: Optimizing a strategy to maximize Sharpe ratio in backtests often produces overfitting, the high Sharpe does not persist out-of-sample.",
          "Not comparable across timeframes: Daily, monthly, and annual Sharpe ratios are calculated differently and cannot be compared directly."
        ]
      },
      {
        "title": "Using Sharpe Ratio to Build Better Symphonies in Composer.trade",
        "paragraphs": [
          "The Sharpe ratio is the most important number in Composer.trade's backtesting output, not because it is the most exciting, but because it is the most honest. Annualized return tells you how fast a strategy grew but says nothing about how terrifying the ride was. Cumulative return tells you the final destination but hides whether the strategy took one harrowing 70% drawdown or a series of small, tolerable dips. The Sharpe ratio accounts for both: it divides the return above the risk-free rate by the volatility of returns, producing a single number that answers the question every rational investor should ask, how much am I being paid for each unit of risk I'm accepting? A strategy earning 50% per year with a Sharpe of 0.8 is taking far more risk per unit of return than a strategy earning 30% per year with a Sharpe of 2.0, and the first strategy's returns will feel much worse in practice.",
          "For Composer.trade symphony builders, the Sharpe ratio is the primary tool for comparing signal variants during strategy development. When testing a new condition, such as adding an RSI filter to an existing trend-following symphony, the correct question is not whether this increases annualized return, but whether it increases the Sharpe ratio. A new condition that reduces returns by 5% but cuts volatility by 30% is a significant improvement; the Sharpe will show this clearly while a raw return comparison would suggest the change was harmful. This methodology, optimizing for risk-adjusted return rather than raw return, is what separates strategies that perform well out-of-sample from those that look good in backtests but fail in live trading.",
          "Sharpe ratio is particularly valuable for comparing leveraged ETF strategies with unlevered alternatives. Holding TQQQ passively over long periods has historically produced exceptional returns, but its Sharpe ratio is modest because the volatility is enormous. A symphony that holds TQQQ only during favorable conditions, and exits to BIL otherwise, will often have a lower total return than passive TQQQ over a long bull market, but its Sharpe ratio will be dramatically higher. This comparison reveals the core value of systematic symphonies: they are not just return-seeking machines, they are risk-adjusted return optimizers. The goal is not maximum return but maximum return per unit of volatility accepted, and Sharpe ratio is the measurement of that objective.",
          "Understanding what constitutes a good Sharpe score for a specific strategy type matters when evaluating Composer.trade symphonies. A leveraged ETF symphony with a Sharpe of 1.7 is exceptional, typical passive holdings of TQQQ produce a Sharpe under 1.0 over most periods. A diversified multi-asset symphony with lower gross returns but a Sharpe of 2.5 represents elite risk-adjusted performance. The strategies in the Composer Atlas library range from roughly 1.10 to 3.04, all above 1.0, meaning each provides substantial compensation for the volatility it produces. A symphony with a Sharpe below 1.0 should be treated with skepticism; it means the strategy's volatility is not justified by the returns it generates.",
          "Building specifically to maximize Sharpe ratio in Composer.trade requires attention to three levers simultaneously. The first lever is return enhancement: adding conditions that increase the fraction of time the strategy spends in high-returning positions. The second lever is volatility reduction: adding conditions that reduce the frequency of large swings, particularly on the downside. The third lever is defensive asset quality: when the strategy exits a leveraged position, holding BIL (near risk-free yield) rather than pure cash adds a small but consistent return contribution that improves the Sharpe calculation. A symphony that earns 1–4% annualized on its defensive portion rather than 0% on cash will show a meaningfully higher Sharpe over long backtests, because the baseline earns money even during the protected periods."
        ]
      }
    ]
  },
  {
    "slug": "calmar-ratio",
    "name": "Calmar Ratio",
    "category": "risk-metric",
    "description": "A risk-adjusted return metric that divides annualized return by maximum drawdown, measuring how much annual return is earned per unit of peak-to-trough loss risk.",
    "formula": "Calmar Ratio = Annualized Return / |Max Drawdown|",
    "related_tags": [
      "calmar-ratio"
    ],
    "last_updated": "2026-06-08",
    "sections": [
      {
        "title": "Definition",
        "paragraphs": [
          "The Calmar Ratio (named after California Managed Account Reports, where it was first published) measures how much annualized return a strategy generates relative to its worst peak-to-trough loss.",
          "It is particularly useful for comparing leveraged or momentum strategies where drawdown risk is the primary concern, not just general volatility. A Calmar ratio above 1.0 means the strategy earns more in annual return than its worst drawdown ever subtracted."
        ]
      },
      {
        "title": "Formula",
        "paragraphs": [
          "Calmar Ratio = Annualized Rate of Return / |Max Drawdown|. Example: ARR = 31.2% (0.312), Max Drawdown = -18.7% (-0.187), Calmar = 0.312 / 0.187 = 1.67.",
          "A Calmar ratio of 1.67 means: for every 1% of maximum drawdown risk, the strategy earns 1.67% per year."
        ]
      },
      {
        "title": "How It Works",
        "paragraphs": [
          "Unlike the Sharpe ratio, which uses standard deviation as its risk measure, the Calmar ratio uses maximum drawdown, the single worst loss experienced from peak to trough. This makes it more intuitive for many investors: \"If I hold this strategy and it eventually hits its worst historical loss, how many years of normal returns would it take to recover?\"",
          "A Calmar ratio of 1.0 means a full recovery takes approximately one year of normal returns. A Calmar ratio of 5.0 means recovery would take only about 2.5 months of normal returns."
        ],
        "table": {
          "headers": [
            "Calmar Ratio",
            "Quality"
          ],
          "rows": [
            [
              "< 0.5",
              "Poor: drawdowns far outpace annual returns"
            ],
            [
              "0.5 – 1.0",
              "Adequate: recovery takes more than a year"
            ],
            [
              "1.0 – 2.0",
              "Good: returns and drawdowns are reasonably balanced"
            ],
            [
              "2.0 – 4.0",
              "Very Good: strategy recovers quickly from worst losses"
            ],
            [
              "> 4.0",
              "Excellent: exceptional balance of return and drawdown"
            ]
          ]
        }
      },
      {
        "title": "In Practice",
        "paragraphs": [
          "The KMLM Switcher posts one of the highest Calmar ratios in the Composer Atlas library at 9.52, remarkable even considering its shorter backtest period. The 2026 Frontrunner (4.23) and Sometimes TQQQ (5.22) also stand out.",
          "Calmar ratios are especially meaningful for leveraged ETF strategies because drawdown risk is disproportionately damaging, a 50% drawdown requires a 100% gain just to recover. Strategies with higher Calmar ratios manage to avoid or minimize these deep losses while still capturing strong compounding."
        ]
      },
      {
        "title": "Limitations",
        "paragraphs": [
          "Depends entirely on the worst observed drawdown: If a strategy is tested over a favorable period that avoids its true worst-case loss, its Calmar ratio will be artificially high. Longer backtests reduce but do not eliminate this risk.",
          "Does not account for the duration of drawdowns: A Calmar ratio doesn't distinguish between a sharp 6-week drawdown and a slow 2-year grind lower. For investors with cash flow needs, duration matters.",
          "Not comparable across different time periods: A strategy backtested from 2010–2026 avoids the 2008 crisis entirely, making its Calmar ratio incomparable to one that includes 2008."
        ]
      },
      {
        "title": "Using Calmar Ratio to Design Better Symphonies in Composer.trade",
        "paragraphs": [
          "The Calmar ratio asks the question that matters most to investors who have actually lived through a major drawdown: if this strategy hits its worst historical loss, how quickly can I recover? Unlike the Sharpe ratio, which treats all volatility as equally bad, the Calmar ratio focuses exclusively on the worst loss, making it especially relevant for leveraged strategies where drawdowns are not just painful but mathematically crippling. A 50% drawdown requires a 100% gain to recover; a 65% drawdown requires a 186% gain. The Calmar ratio converts this intuition into a single number: a Calmar of 4.0 means the strategy earns 4x its worst drawdown in annual returns, implying roughly a 3-month recovery even from the worst historical scenario. This framing makes Calmar the most emotionally resonant risk metric for long-term investors building leveraged symphonies in Composer.trade.",
          "For Composer.trade symphony builders, the Calmar ratio is the most useful metric for comparing strategies that target different drawdown profiles. Consider two symphonies: Symphony A earns 120% annualized with a max drawdown of -50% (Calmar 2.4) and Symphony B earns 80% annualized with a max drawdown of -20% (Calmar 4.0). A raw return comparison favors Symphony A. But the Calmar comparison reveals that Symphony B is far more capital-efficient from a loss-recovery perspective: its worst scenario requires only 25% of the time to recover that Symphony A's worst scenario would require. For investors who may need to withdraw capital or who have limited tolerance for deep losses, the Calmar ratio is the decisive metric.",
          "The clearest way to improve a symphony's Calmar ratio is to focus the exit logic on preventing drawdowns specifically, rather than reducing overall volatility. These are related but different objectives. An exit signal triggered by broad volatility (high VIX) may cause the strategy to exit before profitable periods if VIX rises during a bull market run. But an exit signal triggered by a genuine trend break (price falling below 200d MA) is specifically correlated with the scenarios that produce large drawdowns. When building in Composer.trade, adding conditions that specifically detect trend deterioration, rather than just general volatility, tends to improve Calmar ratio more than adding conditions that respond to noise. The goal is to cut the denominator (max drawdown) as much as possible while minimally reducing the numerator (annual return).",
          "Calmar ratio also provides an intuitive framework for selecting among symphonies as portfolio building blocks. If you are constructing a multi-symphony portfolio and have limited drawdown capacity, say, you cannot tolerate a portfolio drawdown exceeding 25%, Calmar ratios allow you to select the components that maximize return within that drawdown constraint. A symphony with a Calmar of 5.0 and an expected drawdown of 30% could be sized at 83% of portfolio weight to keep the expected contribution to portfolio drawdown under 25%. Calmar thus becomes the key input to position sizing in a multi-symphony portfolio, enabling systematic risk budgeting rather than arbitrary allocation.",
          "The KMLM Switcher in the Composer Atlas library illustrates a deliberate Calmar-maximizing design. By rotating between TQQQ (high return, concentrated risk) and KMLM (managed futures, historically performs well during equity bear markets), the symphony seeks to maintain return potential while specifically preventing the scenario that would produce a catastrophic drawdown: holding TQQQ through a sustained equity bear market. The rotation trigger fires before the worst TQQQ drawdowns occur, because KMLM tends to start outperforming TQQQ during the early stages of equity deterioration. The result is a Calmar ratio of 9.52 in the backtest: for every 1% of max drawdown risk, the strategy earns 9.52% per year. This extraordinary efficiency is the goal of Calmar-aware symphony design."
        ]
      }
    ]
  },
  {
    "slug": "max-drawdown",
    "name": "Max Drawdown",
    "category": "risk-metric",
    "description": "The largest peak-to-trough decline in portfolio value observed over the backtest period, the single worst loss an investor would have experienced if they bought at the worst possible peak.",
    "formula": null,
    "related_tags": [
      "max-drawdown"
    ],
    "last_updated": "2026-06-08",
    "sections": [
      {
        "title": "Definition",
        "paragraphs": [
          "Maximum drawdown (MDD) is the largest single loss from a portfolio's peak value to its subsequent trough, measured over a specified time period. It answers the question: \"What is the worst thing that could have happened to me if I held this strategy through its worst period?\"",
          "It is expressed as a negative percentage: a max drawdown of -40% means the portfolio lost 40% of its value from its high before recovering."
        ]
      },
      {
        "title": "How It Works",
        "paragraphs": [
          "Maximum drawdown is calculated by scanning the return series for all peak-to-trough sequences. At each point in the return history, identify the running maximum portfolio value (the \"peak\"). Calculate the drawdown at each point: (current value − peak value) / peak value. The maximum drawdown is the most negative drawdown value observed across the entire history.",
          "Example: Portfolio reaches $1,000,000 (peak). Falls to $600,000 (trough). Recovers to $1,200,000. Max Drawdown = ($600,000 − $1,000,000) / $1,000,000 = −40%.",
          "Note: the eventual recovery to $1.2M does not change the max drawdown, it was -40% during the trough period, regardless of what came after."
        ]
      },
      {
        "title": "Why It Matters for Leveraged ETF Strategies",
        "paragraphs": [
          "Drawdowns are disproportionately damaging in leveraged portfolios because of the mathematics of recovery. A 10% drawdown requires an 11.1% gain to recover. A 50% drawdown requires a 100% gain. A 65% drawdown (similar to SOXL Growth's max) requires a 185.7% gain just to return to breakeven.",
          "This is why systematic exit strategies are critical for leveraged ETFs, a single unprotected bear market can destroy years of compounding."
        ],
        "table": {
          "headers": [
            "Drawdown",
            "Required gain to recover"
          ],
          "rows": [
            [
              "-10%",
              "+11.1%"
            ],
            [
              "-25%",
              "+33.3%"
            ],
            [
              "-50%",
              "+100%"
            ],
            [
              "-65%",
              "+185.7%"
            ],
            [
              "-80%",
              "+400%"
            ]
          ]
        }
      },
      {
        "title": "In Practice",
        "paragraphs": [
          "Max drawdown is used in Composer Atlas to contextualize each strategy's risk level. Strategies range from -21% (2026 Frontrunner) to -86% (Inside Nancy Pelosi's Chips), reflecting the spectrum from moderate-aggressive to extremely aggressive.",
          "When evaluating a strategy, consider max drawdown alongside your personal capacity to stay invested: Can you psychologically hold through a -40% drawdown without selling? Does your time horizon allow for recovery? A -40% drawdown may take 1–3 years to recover."
        ]
      },
      {
        "title": "Limitations",
        "paragraphs": [
          "Historical max drawdown is a floor, not a ceiling: The worst loss in the backtest period is not necessarily the worst loss possible. Future market conditions could produce deeper drawdowns than anything seen historically.",
          "Path dependency: A strategy that avoided 2008 in its backtest period will show a lower max drawdown than one that includes it, even if the underlying strategy logic is identical.",
          "Does not capture duration: Max drawdown tells you how deep the worst loss was, not how long it lasted. A -30% drawdown that lasted 1 month is very different from a -30% drawdown that lasted 3 years."
        ]
      },
      {
        "title": "Managing Max Drawdown When Building Symphonies in Composer.trade",
        "paragraphs": [
          "Max drawdown is the metric that separates sustainable Composer.trade symphonies from those that look good in theory but cannot be held in practice. Human investors have a well-documented tendency to abandon strategies during deep drawdowns, typically selling near the bottom and missing the recovery. A symphony with a 65% max drawdown may produce extraordinary long-term returns in backtests, but if no real investor can psychologically hold through that loss, the backtest returns are irrelevant, they will never be realized. When building a symphony, targeting an acceptable max drawdown is not just a risk management exercise; it is the foundation of behavioral sustainability. A strategy you can actually hold through its worst periods will outperform a theoretically superior strategy that you abandon when conditions turn adverse.",
          "The most direct way to reduce max drawdown in a Composer.trade symphony is to add an exit trigger that fires before the deepest losses accumulate. The 200-day moving average is the most reliable such trigger for large-cap equity strategies: QQQ's 200d MA break has historically preceded the majority of the worst TQQQ drawdowns by several weeks, providing enough warning to exit before catastrophic losses compound. A secondary approach is using the VIX as an early warning system: extreme VIX readings above 30 almost always coincide with or precede the periods that produce the largest drawdowns. Combining both, exit when QQQ breaks its 200d MA or when VIX exceeds 30, whichever comes first, provides a dual-exit system where either trigger is sufficient to protect capital.",
          "The mathematics of drawdown recovery is the core argument for investing time in drawdown management, and it deserves to be internalized by every Composer.trade symphony builder. The relationship between drawdown and required recovery is not linear, it is convex and accelerating. A 10% loss requires 11.1% to recover; a 30% loss requires 42.9%; a 50% loss requires 100%; a 70% loss requires 233%. For leveraged instruments like TQQQ, the losses are amplified relative to the underlying index: a 35% QQQ drawdown can produce a 70% TQQQ drawdown. This means that reducing the drawdown from -70% to -40% does not just feel better, it reduces the recovery hurdle from 233% to 67%, compressing the recovery timeline from years to months and freeing the compounding engine to build new wealth rather than rebuild lost wealth.",
          "Drawdown-aware symphony design in Composer.trade involves deliberately trading some upside potential for a reduction in worst-case downside. Every signal added to protect against drawdowns will, at some times, cause the symphony to exit a position that ultimately continues to rise, this is the unavoidable cost of protection. The question for the builder is at what tradeoff the protection is worth it. The Calmar ratio provides the quantitative answer: a strategy that earns 80% annually instead of 120% annually, but has a max drawdown of -25% instead of -55%, is almost certainly the better choice for most investors. The difference in annual return sounds significant; the difference between a 25% drawdown and a 55% drawdown is the difference between a manageable setback and an existential crisis for the portfolio.",
          "When backtesting a Composer.trade symphony specifically to evaluate drawdown, it is essential to stress-test across the full available history including all major bear markets. A symphony backtested only from 2010 to 2026 avoids the 2008 financial crisis entirely, the most severe test of leveraged ETF strategies in modern history. During 2008–2009, the S&P 500 fell approximately 57% peak-to-trough; UPRO-equivalent leverage would have produced roughly an 85% drawdown. Any symphony claiming a max drawdown below 30% that was backtested only from 2010 onwards should be treated with significant skepticism, its claimed max drawdown reflects favorable backtest period selection, not robust risk management. Composer.trade allows backtests extending to the limits of available data for most major ETFs; always extend the backtest as far back as possible to capture the full spectrum of historical market regimes."
        ]
      }
    ]
  },
  {
    "slug": "sma",
    "name": "Simple Moving Average (SMA)",
    "category": "indicator",
    "description": "The unweighted average of an asset's closing prices over a specified lookback window, the foundational trend signal used by nearly every strategy in this library.",
    "formula": "SMA(N) = (P1 + P2 + ... + PN) / N",
    "related_tags": [
      "200d-ma"
    ],
    "last_updated": "2026-06-15",
    "sections": [
      {
        "title": "Definition",
        "paragraphs": [
          "The Simple Moving Average (SMA) is calculated by summing an asset's closing prices over a fixed number of past trading days and dividing by that count. As each new day is added, the oldest day drops off, this rolling window is why it is called a moving average.",
          "SMAs smooth out day-to-day price noise to reveal the underlying direction of a trend. A longer period produces a smoother, slower-moving average; a shorter period is more reactive to recent price action."
        ]
      },
      {
        "title": "How It Works",
        "paragraphs": [
          "For a 10-day SMA: add the last 10 closing prices and divide by 10. The next day, drop the oldest price, add today's close, and recalculate. Every day in the window is weighted equally, regardless of how recent.",
          "Key properties: Equal weighting: every day has identical influence on the average; Lag, the SMA always trails current price, more so with longer periods; Smoothing, short-term noise is averaged away, making underlying trends more visible.",
          "The standard interpretation: price above the SMA signals an uptrend; price below signals a downtrend. When a shorter-period SMA crosses above a longer one, it signals potential trend strengthening. The opposite cross signals potential weakening."
        ],
        "table": {
          "headers": [
            "Period",
            "Common Use"
          ],
          "rows": [
            [
              "10–20 day SMA",
              "Short-term regime gate; reactive to recent momentum"
            ],
            [
              "50-day SMA",
              "Intermediate trend; medium-term regime confirmation"
            ],
            [
              "200-day SMA",
              "Long-term bull/bear regime; the most widely watched SMA in markets"
            ]
          ]
        }
      },
      {
        "title": "In Practice",
        "paragraphs": [
          "Nearly every strategy in the Composer Atlas library uses an SMA as its primary regime gate. The standard pattern: compare an ETF's current price to its own SMA, if above, the strategy is in bull mode and holds leveraged equity; if below, it shifts to defensive assets or inverse ETF positions.",
          "Strategies differ in which asset's SMA they use as the reference. TQQQ 200d MA 3x Leverage checks TQQQ's own price vs. its SMA. Holy Grail and Sometimes TQQQ use SPY's SMA. TQQQ For The Long Term uses SPY's 200d SMA as the macro gate and TQQQ's 20d SMA for shorter-term routing in bear mode. Each reference asset creates different sensitivity and lag characteristics.",
          "Several strategies also compare two SMAs of different lengths rather than comparing price directly to an SMA. When the short-period SMA crosses above the long-period SMA, it confirms an emerging uptrend, the technique used to construct golden cross and death cross alerts."
        ]
      },
      {
        "title": "Limitations",
        "paragraphs": [
          "Equal weighting is both a strength and a limitation: a price from 200 days ago influences the SMA just as much as yesterday's close, even though yesterday's price is far more relevant to current conditions. The Exponential Moving Average (EMA) addresses this by giving higher weight to recent prices.",
          "Whipsaw in sideways markets: when price oscillates near the SMA without establishing a clear trend, it crosses back and forth repeatedly. Each crossing triggers a rebalance, and in flat markets these trades collectively erode returns.",
          "Lag: the SMA reflects the past, not the present. During a sharp market reversal, the SMA can be 15–25% away from the current price before it begins to confirm the new trend direction."
        ]
      },
      {
        "title": "Building with SMAs in Composer.trade",
        "paragraphs": [
          "The SMA defines the fundamental question every symphony must answer: is this market environment one where leveraged risk-taking is rewarded, or one where capital preservation takes priority? This binary, above the SMA versus below, is a probabilistic filter based on the empirical observation that assets in sustained uptrends historically continue to outperform more often than not. Every successful symphony in this library is built on this foundation.",
          "The most consequential SMA decision a Composer.trade builder makes is which asset's SMA to use as the primary regime signal. Using TQQQ's own SMA creates a narrower, more reactive signal, 3x leverage amplifies every daily swing, so TQQQ's SMA breaks below more frequently. Using SPY's 200-day SMA is smoother and more stable: the broad market trend is less prone to whipsaw. Both approaches are valid but produce different hold periods and signal frequencies.",
          "Combining SMAs of different lookback periods creates a richer regime classification than a single SMA alone. The most common two-SMA structure pairs a 200-day SMA with a 20-day SMA: price above both signals a strong bull regime; above 200d but below 20d signals short-term weakness within a broader uptrend; below both signals a confirmed bear. The Four Horsemen implements this alongside a primary SPY 200d MA framework.",
          "SMA period selection involves a tradeoff between responsiveness and whipsaw resistance. A 20-day SMA responds quickly to trend changes but generates more false signals in choppy markets. A 200-day SMA generates almost no false crossings because it requires a sustained trend to cross, but it responds slowly to genuine regime changes. For leveraged ETF symphonies, the 200-day period is the empirical sweet spot: it misses some early bear-market decline, but the whipsaw reduction and holding-period consistency more than compensate."
        ]
      }
    ]
  },
  {
    "slug": "ema",
    "name": "Exponential Moving Average (EMA)",
    "category": "indicator",
    "description": "A moving average that applies exponentially greater weight to recent prices, making it more responsive than the Simple Moving Average while still smoothing short-term noise.",
    "formula": "EMA = Price × k + EMA(prev) × (1 − k), where k = 2 / (N + 1)",
    "related_tags": [
      "200d-ma"
    ],
    "last_updated": "2026-06-15",
    "sections": [
      {
        "title": "Definition",
        "paragraphs": [
          "The Exponential Moving Average (EMA) is a moving average that assigns exponentially greater weight to recent prices and exponentially less to older ones. Unlike the Simple Moving Average (SMA), which weights every day in the lookback window equally, the EMA makes recent price action matter more, allowing it to react faster to new market information.",
          "EMAs are preferred when responsiveness to recent price action is more important than smoothness. They are the building blocks of the MACD indicator and appear in several strategies in this library as faster-reacting trend signals and crossover components."
        ]
      },
      {
        "title": "How It Works",
        "paragraphs": [
          "The smoothing factor k = 2 / (N + 1) determines how quickly the EMA responds to new prices. For a 10-day EMA, k = 2/11 ≈ 0.182. Each new EMA value is: today's price × k plus the previous EMA × (1 − k). Today's price contributes about 18.2% of the new value; the accumulated history contributes 81.8%.",
          "Unlike the SMA, which drops a day entirely once it falls outside the lookback window, the EMA technically carries influence from all past prices with exponentially declining weight. This makes the EMA more sensitive to recent moves than the SMA of the same period.",
          "Comparing EMA to SMA on the same asset: when the EMA is above the SMA, recent prices are running higher than the historical average, a sign of accelerating momentum. When EMA is below SMA, recent prices are falling behind the historical average. Several strategies use this EMA-vs-SMA comparison as a momentum acceleration signal."
        ],
        "table": {
          "headers": [
            "Property",
            "EMA",
            "SMA"
          ],
          "rows": [
            [
              "Weight to recent prices",
              "Higher (exponential decay)",
              "Equal (flat weighting)"
            ],
            [
              "Responsiveness",
              "Faster reaction to new data",
              "Slower, more stable"
            ],
            [
              "Whipsaw tendency",
              "More prone in choppy markets",
              "Less prone; more noise-resistant"
            ],
            [
              "Best used for",
              "Shorter-period timing signals",
              "Longer-period regime gates"
            ]
          ]
        }
      },
      {
        "title": "In Practice",
        "paragraphs": [
          "EMAs appear in two distinct roles in the Composer Atlas library. First, Super Semiconductors uses an 8-day EMA of SPY compared to SPY's 200-day SMA as its primary trend gate, the short EMA smooths very recent price action and creates a faster-reacting signal than a raw price-vs-SMA comparison.",
          "Second, EMAs are the backbone of MACD signals: Super Semiconductors uses SMH's 12-day EMA vs. 26-day EMA as a MACD crossover to classify semiconductor sector momentum. When EMA(12) is above EMA(26), sector momentum is positive; when below, it is deteriorating.",
          "The Manhattan Project uses an SPY EMA-vs-SMA acceleration signal, comparing the exponential moving average to the simple moving average to detect whether recent price momentum is accelerating (EMA above SMA) or decelerating (EMA below SMA), as a regime signal for cross-asset routing decisions."
        ]
      },
      {
        "title": "Limitations",
        "paragraphs": [
          "Greater responsiveness produces more false signals. An EMA reacts faster to price changes, which means it also reacts faster to temporary noise and one-day spikes. In volatile, sideways markets, EMA-based signals generate more whipsaw trades than comparable SMA signals.",
          "No universal right period: the 12/26 EMA combination was popularized by Gerald Appel in the 1970s but was not derived from first principles for all asset types. Different periods produce meaningfully different signals on the same asset.",
          "Infinite memory: unlike the SMA, which forgets data older than N days entirely, the EMA technically carries influence from all past prices with diminishing weight. This means the starting EMA value influences subsequent values, making very early backtest readings less reliable until sufficient data accumulates."
        ]
      },
      {
        "title": "Building with EMAs in Composer.trade",
        "paragraphs": [
          "EMAs are most valuable in Composer.trade when a faster-reacting trend signal is needed without the noise of comparing raw daily price to a moving average. Super Semiconductors demonstrates this: instead of comparing SPY's current price directly to its 200d SMA, it uses an 8-day EMA of SPY as the comparison point. The 8-day EMA smooths out single-day noise while still reflecting recent price action, making the gate react faster to genuine trend shifts while filtering out one-day anomalies.",
          "The EMA-as-accelerator technique: comparing EMA vs. SMA of the same asset, captures rate of change in addition to direction. When a short-period EMA crosses above a longer-period SMA, it means recent prices are running ahead of the historical average, a sign of accelerating momentum. The Manhattan Project uses this SPY EMA-vs-SMA comparison to distinguish between markets where trend momentum is building versus deteriorating.",
          "When choosing between an EMA and SMA for a Composer.trade regime gate, the core question is whether you want the gate to react faster (EMA) or be more stable (SMA). For the primary long-term regime gate, the 200-day SMA is almost always superior to a 200-day EMA because stability and whipsaw resistance matter more than responsiveness at this timeframe. Best practice: use the SMA for the macro gate, EMA for secondary timing signals within that gate."
        ]
      }
    ]
  },
  {
    "slug": "macd",
    "name": "MACD",
    "category": "indicator",
    "description": "Moving Average Convergence Divergence: a momentum indicator measuring the spread between two EMAs, used to detect trend changes through crossovers and momentum shifts.",
    "formula": "MACD = EMA(12) − EMA(26); Signal Line = EMA(9) of MACD",
    "related_tags": [
      "macd"
    ],
    "last_updated": "2026-06-15",
    "sections": [
      {
        "title": "Definition",
        "paragraphs": [
          "MACD (Moving Average Convergence Divergence), developed by Gerald Appel in the late 1970s, measures the relationship between two exponential moving averages of an asset's price. When the fast EMA is pulling away from the slow EMA, momentum is accelerating. When they converge, momentum is weakening.",
          "The indicator consists of three components: the MACD line (the difference between a fast and slow EMA), a signal line (a shorter EMA of the MACD line itself), and a histogram (the difference between the MACD line and signal line). Crossovers between the MACD line and signal line are interpreted as potential trend changes."
        ]
      },
      {
        "title": "How It Works",
        "paragraphs": [
          "Standard settings: EMA(12) as the fast line, EMA(26) as the slow line, EMA(9) of the MACD line as the signal line. MACD = EMA(12) − EMA(26). When MACD crosses above the signal line, it is a bullish momentum signal. When it crosses below, it is a bearish signal.",
          "In Composer.trade, MACD logic is typically implemented as a direct EMA comparison: SMH EMA(12) greater than SMH EMA(26) is equivalent to SMH MACD being positive. The strategy evaluates the core crossover, is short-term momentum above or below medium-term momentum, and branches on that boolean.",
          "A positive MACD (fast EMA above slow EMA) indicates the asset has gained more in recent periods than in the longer historical window, upward momentum. A negative MACD indicates the reverse, downward or decelerating momentum."
        ],
        "table": {
          "headers": [
            "MACD Condition",
            "Interpretation"
          ],
          "rows": [
            [
              "EMA(12) above EMA(26): MACD positive",
              "Short-term momentum is bullish; trend accelerating up"
            ],
            [
              "EMA(12) below EMA(26): MACD negative",
              "Short-term momentum is bearish; trend decelerating or reversing"
            ],
            [
              "MACD crossing above signal line",
              "Momentum shifting bullish: potential entry signal"
            ],
            [
              "MACD crossing below signal line",
              "Momentum shifting bearish: potential exit signal"
            ]
          ]
        }
      },
      {
        "title": "In Practice",
        "paragraphs": [
          "In the Composer Atlas library, MACD logic appears explicitly in Super Semiconductors. The strategy compares SMH's 12-day EMA against its 26-day EMA to classify semiconductor sector momentum within the broader bull regime. A bullish crossover (EMA12 above EMA26) unlocks the most aggressive mode: selecting the top 3 semiconductor stocks by 90-day momentum from a 19-company universe. A bearish crossover (EMA12 below EMA26) triggers partial hedging, either an SMH/SHY split or a SOXL dip-buy depending on additional RSI conditions.",
          "MACD is used here as a sector momentum classifier within an already-confirmed macro bull regime (SPY above its 200d SMA), not as a standalone buy/sell signal. This two-layer approach, macro trend gate plus sector MACD, creates more precise conditions for entering the aggressive stock-picking mode and avoids the false-signal problem of using MACD alone."
        ]
      },
      {
        "title": "Limitations",
        "paragraphs": [
          "MACD is a lagging indicator: it is built from EMAs, which are themselves smoothed historical data. MACD crossovers confirm that a trend change has begun, not that one is about to begin. In fast-moving markets, a crossover signal can arrive well after the optimal entry or exit point.",
          "The 12/26/9 default settings are not universal and were developed for daily charts of broad stock indices. For faster-moving assets like leveraged sector ETFs, shorter periods may be more appropriate but require calibration against historical data.",
          "Frequent false signals in ranging markets: MACD generates crossovers whenever the two EMAs oscillate, which happens often in sideways consolidation periods. Strategies in this library mitigate this by requiring the macro trend to be confirmed before evaluating sector-level MACD signals."
        ]
      },
      {
        "title": "Building with MACD in Composer.trade",
        "paragraphs": [
          "MACD's primary value in Composer.trade is as a sector-level momentum classifier within an already-established macro trend. The most productive use is as a second-layer signal that only becomes active after the primary regime gate has confirmed a bull market. Within a confirmed bull market, the MACD on the target sector ETF answers a more specific question: is this sector currently showing positive momentum, or is it lagging? This makes MACD a precision tool for allocating within a bull regime, not a gate for entering or exiting the overall risk-on/risk-off stance.",
          "Implementing MACD in Composer.trade does not require computing the full indicator. The core signal, is short-term momentum positive or negative?, reduces to a simple comparison: is EMA(12) above EMA(26)? In Composer.trade's signal builder, this translates directly to comparing two moving averages of different periods on any asset. The strategy can branch on this directly, without computing the signal line or histogram.",
          "MACD is particularly effective for sector-rotation decisions within a broader multi-signal framework. A symphony allocating among semiconductor, technology, energy, and bond ETFs can compute MACD on each sector ETF to identify which sectors currently have positive momentum. Ranking sectors by their MACD, positive vs. negative, or by the magnitude of EMA spread, is a concrete implementation of cross-sectional momentum that automatically rotates toward the sectors with the strongest recent trend and away from those losing momentum."
        ]
      }
    ]
  },
  {
    "slug": "mean-reversion",
    "name": "Mean Reversion",
    "category": "strategy-concept",
    "description": "A strategy that bets an asset's price will return toward its historical average after an extreme move, buying sharp drops and selling or shorting sharp rallies at statistical extremes.",
    "formula": null,
    "related_tags": [
      "mean-reversion"
    ],
    "last_updated": "2026-06-15",
    "sections": [
      {
        "title": "Definition",
        "paragraphs": [
          "Mean reversion is the tendency of an asset's price to return toward its historical average after an extreme departure in either direction. A mean-reversion strategy systematically exploits this tendency: it buys when an asset has fallen sharply, expecting a bounce, and sells or shorts when an asset has risen sharply, expecting a pullback.",
          "Mean reversion is the philosophical opposite of momentum investing. Momentum bets that trends persist; mean reversion bets that extremes are temporary. Both have empirical support: momentum tends to dominate over intermediate timeframes (weeks to months), while mean reversion tends to dominate over very short timeframes and very long ones (years)."
        ]
      },
      {
        "title": "How It Works",
        "paragraphs": [
          "Mean-reversion strategies quantify how far an asset has moved from its average using oscillators or deviation measures. The most common signal in this library is RSI, an RSI below 30 indicates an extreme downward move (oversold), and the strategy enters long expecting a bounce. An RSI above 70 or 80 indicates an extreme upward move (overbought), and the strategy exits or shorts.",
          "A pure mean-reversion approach asks only: how far has this asset moved from normal? It is inherently contrarian, always buying weakness and selling strength, and requires no view on whether the overall trend is up or down.",
          "Blended approaches are more common in this library: strategies that use a primary trend filter (200d MA) to avoid mean-reverting against a strong bear trend, but then use RSI-based mean-reversion logic to time entries within the confirmed trend."
        ]
      },
      {
        "title": "In Practice",
        "paragraphs": [
          "Several strategies in the Composer Atlas library use mean reversion as their primary mechanism. The s90 Half Low Catch catches catastrophic drops in leveraged ETFs using RSI thresholds far below the standard oversold level: LABU below RSI 22, YINN below 14, UDOW below 18. These extreme thresholds only trigger in genuine market panics, not ordinary corrections.",
          "SOXX Group's 30-20-10 Double Pop system is a multi-timeframe mean-reversion cascade on semiconductor ETFs. After a large single-day move, the strategy evaluates SMH's RSI across three lookback windows (30d, 20d, 10d). If RSI confirms overbought at any timeframe, it holds SOXS, betting the pop will fade. If RSI is oversold, it holds SOXL, betting the drop will recover.",
          "Wooden ARKK Machine 2.2 applies cross-sectional mean reversion: within a defined universe of leveraged ETFs, it always buys the single worst recent performer. The thesis is that the most beaten-down asset in any universe tends to produce the strongest bounce when sentiment stabilizes, and in its bear pool, this extends to buying the worst-performing inverse ETF, betting even short positions mean-revert."
        ]
      },
      {
        "title": "Limitations",
        "paragraphs": [
          "The biggest risk of mean reversion: there is no mean to revert to if the asset's fundamental value has permanently declined. Buying every large drop in an individual company can be catastrophic if the company fails. For broad indices and liquid ETFs, mean reversion is more reliable because indices reconstitute and cannot fall to zero.",
          "RSI-based mean reversion using very tight thresholds (RSI below 15 or 20) fires infrequently by design, only at true market panics. This means the strategy spends most of its time in BIL, limiting compounding opportunities during calm bull markets.",
          "Mean reversion competes directly with momentum. A strategy buying at RSI 20 is buying exactly when a momentum strategy is selling at a trendline break. In sustained downtrends, mean-reversion entries at oversold RSI levels frequently produce brief bounces followed by continued declines."
        ]
      },
      {
        "title": "Building Mean-Reversion Symphonies in Composer.trade",
        "paragraphs": [
          "Pure mean-reversion symphonies in Composer.trade work best when targeting assets with well-documented bounce behavior at RSI extremes. Broad equity indices (SPY, QQQ) and heavily-traded sector ETFs (SMH, SOXX) have decades of data showing consistent mean-reversion after extreme RSI readings. Leveraged ETFs amplify this: when TQQQ's RSI falls below 30, the underlying QQQ has likely dropped 10%+ in a short period, compressing a spring that historically releases sharply.",
          "RSI threshold selection is the most critical parameter. Standard oversold is RSI below 30, but the most extreme mean-reversion strategies in this library use thresholds far tighter: below 14 (YINN), below 15 (FAS), below 22 (LABU). These levels fire rarely, but when they do, the subsequent mean-reversion is historically both more reliable and larger in magnitude. The tradeoff is significant time in BIL.",
          "The most effective mean-reversion symphonies combine the contrarian entry signal with a macro regime filter to avoid catching falling knives during sustained bear markets. Adding a constraint that mean-reversion entries only fire when the broader market is within a defined range of its 200d MA creates macro-qualified mean reversion: the strategy bets on bounces only when the market is not in a confirmed long-term downtrend.",
          "Sizing is unusually important in mean-reversion symphonies because positions are entered into falling assets. A full 100% allocation to TQQQ at RSI 20 is a concentrated bet that the bottom is in, if wrong, losses compound quickly. The strategies in this library typically address this with a 50/50 structure alongside a more conservative component, so even if a mean-reversion entry proves early, the combined portfolio loss is approximately half what a full allocation would suffer."
        ]
      }
    ]
  },
  {
    "slug": "volatility-decay",
    "name": "Volatility Decay",
    "category": "strategy-concept",
    "description": "The mathematical erosion of a leveraged ETF's value caused by daily rebalancing, in volatile sideways markets, the fund loses value even when the underlying index ends flat.",
    "formula": "Approximate annual decay ≈ −0.5 × Leverage² × Annual Variance",
    "related_tags": [
      "leveraged-etfs"
    ],
    "last_updated": "2026-06-15",
    "sections": [
      {
        "title": "Definition",
        "paragraphs": [
          "Volatility decay (also called beta decay or compounding drag) is the phenomenon where a leveraged ETF loses value in volatile sideways markets, even when the underlying index ends flat. It is a mathematical consequence of daily leverage rebalancing, specifically, the asymmetry between percentage gains and percentage losses.",
          "The core insight: a 10% gain followed by a 10% loss does not return to the starting point. $100 × 1.10 × 0.90 = $99. For a 3x leveraged ETF, a 10% index move in either direction becomes a 30% fund move. $100 × 1.30 × 0.70 = $91, the leveraged fund loses 9% while the underlying index is flat."
        ]
      },
      {
        "title": "How It Works",
        "paragraphs": [
          "Volatility decay is proportional to the variance of daily returns and the square of the leverage multiple. The approximate annual decay: Loss ≈ −0.5 × L² × σ², where L is the leverage multiple and σ² is the annual variance of the underlying index.",
          "For a 3x ETF with 20% annual index volatility: Annual decay ≈ −0.5 × 9 × 0.04 = −0.18, or roughly −18% per year from decay alone, before any directional movement from the underlying trend.",
          "This decay becomes catastrophic in bear markets because it compounds with directional loss. Not only does the leveraged fund fall further than 3x the index drop, but the daily swings during the decline add additional decay. This is why a 50% drop in QQQ can produce an 80–90% drop in TQQQ."
        ],
        "table": {
          "headers": [
            "Market Condition",
            "Volatility Decay Effect"
          ],
          "rows": [
            [
              "Steadily rising, low volatility",
              "Minimal decay; compounding amplifies gains above 3x index"
            ],
            [
              "Sideways, high volatility",
              "Significant decay even with zero net index movement"
            ],
            [
              "Declining, high volatility",
              "Directional loss + compounding decay: far more than 3x index loss"
            ],
            [
              "V-shaped crash and recovery",
              "Decay during the crash means recovery requires far more than 3x the index gain"
            ]
          ]
        }
      },
      {
        "title": "Why It Matters for Strategy Design",
        "paragraphs": [
          "Volatility decay is the single most important concept for understanding why leveraged ETFs require systematic management. A buy-and-hold investor in TQQQ is not simply getting 3x the long-term return of QQQ, they are getting 3x the return minus accumulated decay from all volatile sideways periods. In choppy, mean-reverting markets, this decay can be severe enough to turn positive index returns into negative leveraged fund returns.",
          "Systematic exit strategies address decay by removing the leveraged fund from risk during the periods when decay is worst: high-volatility environments where the market moves violently in both directions without making net progress. By exiting to BIL during these periods, the strategy avoids both the compounding erosion and the directional downside if the volatility is driven by a genuine bear market."
        ]
      },
      {
        "title": "Limitations",
        "paragraphs": [
          "Volatility decay is not always the dominant effect. In strongly trending markets, the 2009–2021 bull run, the 2023–2025 AI rally, the compounding gains from 3x leverage easily outpace decay. Many investors overweight decay as a reason to avoid leveraged ETFs entirely, missing the periods where leverage provides extraordinary compounding.",
          "The decay formula is an approximation. Actual decay depends on the specific sequence of daily returns (path dependency), not just average volatility. A year with the same average volatility can produce very different decay depending on whether the volatile days cluster together or spread out evenly.",
          "Expense ratios and swap costs are already incorporated into the ETF's NAV. Investors do not need to separately account for these costs, they are embedded in the price. Volatility decay is additional to, not the same as, these embedded fees."
        ]
      },
      {
        "title": "Designing for Volatility Decay in Composer.trade",
        "paragraphs": [
          "Understanding volatility decay transforms how a Composer.trade builder thinks about exit signals. The primary purpose of the 200d MA gate is not just to avoid directional losses, it is to avoid the high-volatility sideways periods when decay compounds. When QQQ breaks below its 200d MA, the market typically enters a phase of elevated volatility and choppy price action. Exiting to BIL avoids both the directional loss and the decay, the gain in risk-adjusted return from this exit comes from two sources, not one.",
          "Volatility decay creates an asymmetry that makes high-conviction trend-following more valuable for leveraged ETF strategies than for unlevered ones. For a 3x leveraged position, even a false exit has significant value: during the choppy period that triggered the exit, decay would have accumulated regardless of whether the market ultimately recovered. The math consistently favors erring on the side of exiting leveraged positions when volatility rises.",
          "The least understood implication of volatility decay is that TQQQ is not simply a better version of QQQ for a long-term investor. Over 20 years including the 2000–2002 crash and 2008–2009 crisis, passive TQQQ would have destroyed virtually all capital despite QQQ eventually recovering to all-time highs. The decay during those extended volatile bear markets is irreversible, a 90% loss requires a 900% gain to recover. This is precisely why the entire framework of systematic leveraged ETF investing exists."
        ]
      }
    ]
  },
  {
    "slug": "standard-deviation",
    "name": "Standard Deviation",
    "category": "risk-metric",
    "description": "A measure of how widely an investment's returns vary around their average, the most common quantification of volatility and the denominator of the Sharpe ratio.",
    "formula": "σ = √[ Σ(Rᵢ − R̄)² / N ]",
    "related_tags": [
      "standard-deviation"
    ],
    "last_updated": "2026-06-15",
    "sections": [
      {
        "title": "Definition",
        "paragraphs": [
          "Standard deviation measures the average distance of individual return observations from the mean return. A high standard deviation means returns swing widely around the average, the experience is volatile and unpredictable. A low standard deviation means returns cluster near the average, the experience is smoother and more consistent.",
          "In finance, standard deviation is the most widely used measure of investment risk. When annualized, it approximates the range within which returns will fall about 68% of the time (within one standard deviation of the mean) and about 95% of the time (within two standard deviations), assuming roughly normal return distributions."
        ]
      },
      {
        "title": "How It Works",
        "paragraphs": [
          "To calculate: find the mean daily return over the period; subtract the mean from each day's return; square each difference; average the squared differences; take the square root to return to the original units.",
          "Annualizing: daily standard deviation × √252 (trading days per year) = annualized standard deviation. This is how the figures on Composer Atlas strategy cards are computed.",
          "The strategies in this library range from approximately 40.5% (2026 Frontrunner, which spends most of its time in BIL) to 84.6% annualized standard deviation (SOXL Growth RL, with 3x semiconductor leverage and RL-optimized thresholds). This spread reflects the spectrum from minimal-time-in-risk strategies to fully leveraged semiconductor exposure."
        ],
        "table": {
          "headers": [
            "Annualized Std Dev",
            "Volatility Classification"
          ],
          "rows": [
            [
              "Below 15%",
              "Low: comparable to a diversified bond fund"
            ],
            [
              "15–25%",
              "Moderate: comparable to a broad equity index fund"
            ],
            [
              "25–40%",
              "High: sector-concentrated equity or moderate leverage"
            ],
            [
              "40–65%",
              "Very High: leveraged ETF territory"
            ],
            [
              "Above 65%",
              "Extreme: 3x semiconductor or concentrated sector leverage"
            ]
          ]
        }
      },
      {
        "title": "In Practice",
        "paragraphs": [
          "Standard deviation is displayed on every strategy card in Composer Atlas and is the denominator of the Sharpe ratio, dividing excess return by standard deviation produces the risk-adjusted return comparison.",
          "Several strategies in this library use standard deviation as a live trading signal, not just as a post-hoc risk measurement. SOXL Growth and SOXL Growth RL evaluate the standard deviation of TQQQ and SOXL daily returns as regime classifiers: when StdDev(SOXL, 30d) exceeds a threshold, the market is in an elevated-volatility regime where leveraged ETF decay is most severe, triggering defensive routing or position reduction."
        ]
      },
      {
        "title": "Limitations",
        "paragraphs": [
          "Standard deviation treats upside and downside volatility identically. A strategy that occasionally generates very large positive returns will show high standard deviation even if it has never produced a large negative return. The Sortino ratio addresses this by only penalizing downside volatility.",
          "Normal distribution assumption: standard deviation is most interpretable when returns follow a bell curve. Leveraged ETF returns do not, they are skewed and have fat tails, meaning extreme daily moves occur more frequently than a normal distribution would predict.",
          "Backward-looking: standard deviation summarizes past variability. Future volatility can differ substantially from historical, especially around major macro events. A strategy with low historical standard deviation in a bull market may experience very high standard deviation in the next bear market."
        ]
      },
      {
        "title": "Using Standard Deviation When Building in Composer.trade",
        "paragraphs": [
          "Standard deviation is most useful in Composer.trade as a comparative tool when evaluating strategies of similar return levels. Two strategies with the same ARR but different standard deviations will feel very different to hold: the lower-std-dev strategy has smaller day-to-day swings and more predictable short-term performance. When testing whether to add a new condition to a symphony, the correct question is rarely 'does this improve return?' and more often 'does this improve return per unit of standard deviation?', the Sharpe ratio answers this directly.",
          "Using standard deviation as a live signal within a Composer.trade symphony is an advanced technique demonstrated by SOXL Growth and SOXL Growth RL. When the standard deviation of recent returns exceeds a threshold, the market is in a high-volatility regime where leveraged ETF decay is most severe. Exiting or reducing leverage when realized volatility is high is a systematic implementation of the principle to reduce size when volatility spikes.",
          "For investors comparing strategies on Composer Atlas, standard deviation provides context that ARR alone cannot. SOXL Growth has a higher ARR than the 2026 Frontrunner, but its standard deviation is roughly 70% higher (68.7% vs. 40.5%). Whether the higher return justifies the higher volatility is a personal decision, but the standard deviation figure is the clearest way to quantify that tradeoff, and the Sharpe ratio converts it into a single risk-adjusted comparison."
        ]
      }
    ]
  },
  {
    "slug": "annualized-return",
    "name": "Annualized Rate of Return (ARR)",
    "category": "risk-metric",
    "description": "The compound annual growth rate of a strategy: how much $1 invested would grow per year if the total backtest return compounded uniformly over the holding period.",
    "formula": "ARR = (Final Value / Initial Value)^(252 / Trading Days) − 1",
    "related_tags": [],
    "last_updated": "2026-06-15",
    "sections": [
      {
        "title": "Definition",
        "paragraphs": [
          "Annualized Rate of Return (ARR), also called Compound Annual Growth Rate (CAGR), converts a strategy's total return over any time period into a standardized annual percentage. This allows strategies with different backtest lengths to be compared on equal footing: a 5-year backtest and a 14-year backtest both express performance as a per-year figure.",
          "ARR answers the question: if this strategy's total return compounded evenly each year, what annual growth rate would produce that result? It is the primary headline metric shown on each strategy card in Composer Atlas."
        ]
      },
      {
        "title": "How It Works",
        "paragraphs": [
          "ARR = (Final Value / Initial Value)^(252 / Total Trading Days) − 1. The exponent (252 / days) converts from the actual holding period to an annual basis using 252 as the standard number of trading days per year.",
          "Example: A strategy grew from $1.00 to $100.00 over 3,563 trading days (≈14.2 years). ARR = (100)^(252 / 3563) − 1 ≈ 37.9% per year. Compounding 37.9% per year for 14.2 years produces exactly $100 from $1.",
          "The relationship between ARR and cumulative return is extremely non-linear. Small differences in ARR over long periods produce enormous differences in cumulative return due to compounding. A 100% ARR over 14 years produces approximately $16,384 from $1. A 150% ARR produces approximately $9,313,000 from $1 over the same period."
        ],
        "table": {
          "headers": [
            "ARR",
            "10-Year Growth of $1"
          ],
          "rows": [
            [
              "10%",
              "$2.59"
            ],
            [
              "25%",
              "$9.31"
            ],
            [
              "50%",
              "$57.67"
            ],
            [
              "100%",
              "$1,024"
            ],
            [
              "150%",
              "$9,313"
            ]
          ]
        }
      },
      {
        "title": "In Practice",
        "paragraphs": [
          "The strategies in the Composer Atlas library show ARRs ranging from approximately 73% (Nancy Pelosi's Chips, SPY Energy Chips) to 735% (s90 Half Low Catch, over only ~2.2 years). Among the zoop strategies, backtested annualized returns range from ~91% (2026 Frontrunner) to ~280% (KMLM Switcher), though backtest lengths vary from ~5.5 to ~14.2 years.",
          "These figures are extraordinary by conventional standards: the S&P 500 has historically returned approximately 10% per year, and professional hedge funds rarely sustain 20–30% annualized over multi-year periods. The strategies achieve these figures through 3x leverage on the Nasdaq 100 combined with systematic risk management that avoids the worst bear market periods."
        ]
      },
      {
        "title": "Limitations",
        "paragraphs": [
          "ARR says nothing about the journey. A strategy with 100% ARR that dropped 80% halfway through and recovered looks identical to one that grew smoothly. Max drawdown, standard deviation, and Sharpe ratio are essential complements for understanding the actual experience of holding the strategy.",
          "Backtest ARR is not a forward projection. Strategies do not maintain their historical ARR going forward. Exceptional backtested ARR often reflects favorable period selection, overfitting to historical data, or market conditions that may not recur.",
          "Short backtests produce unreliable ARR. A strategy showing 500% ARR over 18 months has barely survived one market regime. Never compare ARR across strategies without first comparing their backtest lengths, a 735% ARR over 2.2 years and a 182% ARR over 14.2 years are not comparable headline numbers."
        ]
      },
      {
        "title": "Interpreting ARR in the Composer Atlas Library",
        "paragraphs": [
          "The right way to read the ARR on a strategy card is as a starting point for further investigation, not a terminal conclusion. A high ARR is a necessary but insufficient condition for a strategy worth using. You must also assess whether the ARR was earned at acceptable risk levels (Sharpe ratio), whether the drawdowns were survivable (max drawdown), and whether the backtest period was long enough to include genuine bear market stress. A strategy with 200% ARR and a 50% max drawdown requires a very different investment commitment than one with 100% ARR and a 20% max drawdown.",
          "ARR figures cannot be fairly compared across strategies with very different backtest lengths. The s90 Half Low Catch's 735% ARR over 2.2 years and Sometimes TQQQ's 182% ARR over 14.2 years are not directly comparable: the short-backtest strategy has not been tested through a full market cycle, while the long-backtest strategy has survived multiple bear markets, rate cycles, and sector rotations. When allocating real capital, prioritize strategies with the longest backtests and most consistent multi-year performance.",
          "Cumulative return: also shown on strategy cards, is the total growth of $1 invested from the start of the backtest. ARR is most useful for comparing strategies of different lengths on equal footing. Cumulative return is most useful for communicating the absolute magnitude of compounding, Sometimes TQQQ's cumulative return of over 2,000,000× over 14.2 years reflects 182% annual compounding sustained across multiple market cycles, which is a more visceral demonstration of the compounding power of systematic leveraged investing than the percentage figure alone conveys."
        ]
      }
    ]
  },
  {
    "slug": "managed-futures",
    "name": "Managed Futures",
    "category": "asset-class",
    "description": "An alternative asset class that systematically trades futures contracts across equities, bonds, commodities, and currencies using trend-following algorithms, historically performing well when equities are in sustained bear markets.",
    "formula": null,
    "related_tags": [
      "managed-futures"
    ],
    "last_updated": "2026-06-15",
    "sections": [
      {
        "title": "Definition",
        "paragraphs": [
          "Managed futures is an investment strategy that uses futures contracts, standardized agreements to buy or sell an asset at a future date, to take long or short positions across a diversified set of asset classes: equity indices, government bonds, commodities (oil, gold, agricultural), and currencies. The 'managed' aspect refers to systematic, algorithmic trading rules rather than discretionary human decisions.",
          "In the Composer Atlas library, the primary managed futures instrument is KMLM (KFA Mount Lucas Managed Futures Index Strategy ETF), which gives retail investors daily-tradeable access to a diversified managed futures strategy through a single ETF."
        ]
      },
      {
        "title": "How It Works",
        "paragraphs": [
          "Most managed futures strategies are trend-following: they identify whether prices in each market are trending up or down, take long positions in uptrending markets and short positions in downtrending markets, and hold until the trend changes. The diversification across many uncorrelated markets is a key structural feature.",
          "When equity markets trend strongly downward (bear markets), commodity markets, bond markets, or currency markets often trend in the opposite direction, providing the managed futures strategy with profitable positions that partially offset the equity decline. This is the source of managed futures' historically low or negative correlation to equities during bear markets.",
          "KMLM specifically tracks the KFA Mount Lucas Managed Futures Index across 22 futures markets spanning commodities, interest rates, and currencies. It is rebalanced monthly and does not hold equities directly, making it fundamentally different in risk profile from the leveraged equity ETFs it is paired with in this library."
        ],
        "table": {
          "headers": [
            "Market Condition",
            "Typical KMLM Behavior"
          ],
          "rows": [
            [
              "Strong equity bull market",
              "May underperform; equity trend is positive but KMLM lacks equity exposure"
            ],
            [
              "Equity bear market with sustained trend",
              "Often outperforms; bond and commodity futures trend alongside the equity decline"
            ],
            [
              "Sideways, range-bound markets",
              "Underperforms; trend signals produce whipsaw losses across 22 markets"
            ],
            [
              "Inflationary commodity cycle",
              "Strong outperformance; long commodity futures in trend"
            ],
            [
              "Rising interest rate cycle",
              "Outperformance; short bond futures in trend"
            ]
          ]
        }
      },
      {
        "title": "In Practice",
        "paragraphs": [
          "In the Composer Atlas library, KMLM appears in the KMLM Switcher strategy as the defensive alternative to a 4-ETF leveraged equity basket. The thesis: KMLM has historically performed well precisely during the periods when TQQQ performs worst, sustained equity bear markets with high volatility, because those environments produce strong, tradeable trends in bonds, commodities, and currencies.",
          "The strategy's 2022 bear market performance illustrates the concept: KMLM returned approximately +24% while TQQQ fell approximately −80%. This negative correlation during equity stress is the core diversification argument for managed futures alongside leveraged equity, not as a replacement for equity exposure during normal conditions, but as the defensive position that potentially profits from the same conditions that cause the equity position to lose money."
        ]
      },
      {
        "title": "Limitations",
        "paragraphs": [
          "KMLM launched in November 2020, giving it only approximately 5.5 years of live history. The strategy's exceptional 2022 performance was its first major test; extended out-of-sample periods across multiple market regimes are needed to validate the long-run correlation structure.",
          "Managed futures underperform in sideways, range-bound markets. When bonds, commodities, currencies, and equities all chop within ranges without sustained trends, the strategy generates whipsaw losses from repeated failed trend signals. Much of the 2010s represented this challenging environment for trend-following managed futures.",
          "The correlation benefit is regime-dependent, not constant. KMLM's negative correlation to equities is highest during trending bear markets but approaches zero or positive during bull markets. Investors expecting consistent diversification from KMLM in all market conditions will be disappointed.",
          "Expense ratio: KMLM charges 0.90% annually, slightly above most equity index ETFs but reasonable for the complexity of its underlying systematic strategy."
        ]
      },
      {
        "title": "Building with Managed Futures in Composer.trade",
        "paragraphs": [
          "Managed futures are the most powerful defensive diversifier available to Composer.trade symphony builders because they can profit in both bull and bear markets through trend-following across uncorrelated asset classes. This makes KMLM uniquely valuable compared to bonds (which underperformed during 2022's simultaneous equity-bond bear market) or cash (which earns yield but does not benefit from bear market trends). A symphony rotating between TQQQ in bull markets and KMLM in bear markets is not simply moving from offensive to defensive, it is actively seeking profits in both regimes through fundamentally different mechanisms.",
          "The rotation trigger between leveraged equity and managed futures is one of the most important design decisions in a KMLM-inclusive symphony. Using a trend signal on equities (like the 200d MA on SPY) creates a binary switch: bull regime holds TQQQ, bear regime holds KMLM. Using a relative momentum comparison between TQQQ and KMLM directly, holding whichever has the stronger recent return, creates a more dynamic switch that responds to actual relative performance rather than requiring a specific SMA crossover event.",
          "The KMLM Switcher in this library achieves its exceptional Calmar ratio (9.52) and Sharpe (2.63) by combining the managed futures rotation with the full suite of RSI-based dip-buy signals from the Frontrunner component. When no dip-buy signal is active and tech sector momentum (XLK RSI) is positive, the strategy holds the 4-ETF leveraged equity basket for maximum upside. When tech momentum weakens, it rotates to KMLM, which may continue generating returns from non-equity trends."
        ]
      }
    ]
  },
  {
    "slug": "inverse-etfs",
    "name": "Inverse ETFs",
    "category": "asset-class",
    "description": "Exchange-traded funds engineered to deliver the opposite of their benchmark's daily return, used as defensive positions, active hedges, or directional bets on declining markets without requiring a margin account.",
    "formula": null,
    "related_tags": [
      "inverse-etfs"
    ],
    "last_updated": "2026-06-15",
    "sections": [
      {
        "title": "Definition",
        "paragraphs": [
          "Inverse ETFs deliver the negative of their benchmark's daily return. A 1x inverse ETF targeting the S&P 500 (SH) returns +1% when the S&P 500 falls 1%, and −1% when it rises 1%. A 3x inverse ETF (SQQQ) returns +3% when the Nasdaq 100 falls 1%, and −3% when it rises 1%.",
          "Like leveraged long ETFs, inverse ETFs rebalance daily to maintain their target multiple. This daily reset creates the same compounding non-linearity, they are not designed for long-term holding but for short-term tactical positioning during confirmed downtrends or specific hedging conditions."
        ]
      },
      {
        "title": "How It Works",
        "paragraphs": [
          "Inverse ETFs achieve their negative exposure through derivatives: short futures contracts, swap agreements, or put options on the underlying index. Each day, the fund rebalances these positions to maintain exactly −1x or −3x the benchmark's return for that day.",
          "The daily rebalancing creates the same volatility decay problem as leveraged long ETFs, but in reverse. In a declining market, the inverse ETF compounds gains faster than −1x (favorable). In a volatile, sideways market, the inverse ETF decays in value even if the underlying index ends flat (unfavorable). This makes inverse ETFs effective as short-term tactical tools during confirmed downtrends, but costly as permanent hedges against equity exposure."
        ],
        "table": {
          "headers": [
            "ETF",
            "Benchmark",
            "Leverage",
            "Common Use in This Library"
          ],
          "rows": [
            [
              "SH",
              "S&P 500",
              "−1x",
              "Primary defensive position in most bear-mode branches"
            ],
            [
              "SQQQ",
              "Nasdaq 100 (QQQ)",
              "−3x",
              "Aggressive bear-mode short in momentum filters"
            ],
            [
              "PSQ",
              "Nasdaq 100",
              "−1x",
              "Conservative inverse QQQ for bear-market signal matching"
            ],
            [
              "SPXU / SPXS",
              "S&P 500",
              "−3x",
              "3x inverse S&P; used in UVXY-triggered defensive routing"
            ],
            [
              "SOXS",
              "Semiconductors (SOXX)",
              "−3x",
              "Fading semiconductor overbought signals in sector strategies"
            ],
            [
              "TMV",
              "20-Year Treasury",
              "−3x",
              "Profiting from rising long-term interest rates"
            ],
            [
              "SARK",
              "ARKK Innovation",
              "−1x",
              "Bear pool anchor in Wooden ARKK Machine's risk-on regime"
            ]
          ]
        }
      },
      {
        "title": "In Practice",
        "paragraphs": [
          "Inverse ETFs serve different functional roles across the library. SH (ProShares Short S&P500) is the most widely used defensive position, most zoop strategies default to SH in bear conditions rather than BIL. Unlike BIL (which preserves capital at the risk-free rate), SH actively profits from S&P 500 declines. Using SH instead of BIL is a directional bet that when bull-mode conditions fail, the market will likely continue falling.",
          "SQQQ and PSQ appear in strategies pressing the short trade during confirmed Nasdaq bear markets. The Holy Grail and TQQQ For The Long Term both run relative RSI filters between SQQQ and a bond ETF (BSV or TLT) in bear mode, selecting whichever has stronger momentum: either continuing the Nasdaq short or rotating to bonds for capital preservation.",
          "SOXS (3x inverse semiconductors) is used by SOXX Group and Nancy Pelosi's Chips as a mean-reversion fade signal: when semiconductor ETFs reach extreme overbought RSI readings, the strategy positions in SOXS expecting the pop to fade. Wooden ARKK Machine 2.2 demonstrates the most sophisticated inverse ETF usage: its entire risk-on bear pool consists of inverse ETFs (SARK, PSQ, TMV, DRV, TYO), and the strategy selects the single worst-performing inverse ETF, applying cross-sectional mean-reversion logic to short positions."
        ]
      },
      {
        "title": "Limitations",
        "paragraphs": [
          "Volatility decay applies in reverse: inverse ETFs decay in volatile, sideways markets just as leveraged long ETFs do. Holding SH through a sideways market that eventually recovers produces a net loss even if the S&P 500 ends at the same level.",
          "Not suitable for long-term hedging: the compounding decay makes inverse ETFs ineffective as permanent portfolio hedges. A portfolio holding both TQQQ and SQQQ simultaneously does not cancel out, both instruments lose value in volatile, sideways markets.",
          "3x inverse ETFs carry extreme directional risk. SQQQ, SPXU, and SOXS are the most dangerous instruments in this library if the underlying trend reverses. A sharp 10% market rally produces a 30% loss in a 3x inverse ETF, making them costly to hold if the bear market ends in a sudden, unexpected recovery."
        ]
      },
      {
        "title": "Building with Inverse ETFs in Composer.trade",
        "paragraphs": [
          "The choice between SH (1x inverse) and BIL (T-bills) as the bear-mode defensive position has important implications for symphony behavior. BIL earns the current risk-free rate with virtually zero volatility, pure capital preservation. SH earns returns inversely correlated to the S&P 500, it can significantly outperform BIL during bear markets but underperforms during recoveries and flat markets. Choosing SH as the default defensive asset is an implicit directional bet that when bull-mode conditions fail, the market will continue falling.",
          "The relative RSI filter between an inverse ETF and a bond ETF, as used in Holy Grail's SQQQ vs. BSV comparison and TQQQ For The Long Term's SQQQ vs. TLT comparison, is one of the most sophisticated signal patterns in this library. When SQQQ has higher RSI than the bond ETF, the short-Nasdaq trade has been generating gains recently: press the short. When the bond ETF has higher RSI, the short trade has cooled and capital preservation via bonds is the stronger momentum choice: rotate to safety.",
          "Using SH versus SQQQ in bear mode represents a leverage tradeoff for defensive positioning that mirrors the TQQQ vs. QQQ choice in bull mode. SQQQ amplifies bear-market gains by 3x, just as TQQQ amplifies bull-market gains by 3x. But SQQQ's volatility decay is equally severe, if the market declines 20% and then recovers 20%, SQQQ produces a significant net loss through the round trip. For this reason, most strategies in this library use SH (1x inverse) as their default bear-mode hold, reserving SQQQ for specific RSI-filtered momentum conditions where a directional short has high conviction."
        ]
      }
    ]
  },
  {
    "slug": "zoop",
    "name": "zoop's Strategies",
    "category": "strategy-concept",
    "description": "A curated collection of Composer.trade symphonies built by zoop (Azqato), an investor, developer, and community builder who shares systematic leveraged ETF strategies on Twitch and YouTube.",
    "formula": null,
    "related_tags": [
      "zoop"
    ],
    "last_updated": "2026-06-15",
    "sections": [
      {
        "title": "Who Is zoop?",
        "paragraphs": [
          "zoop, also known online as Azqato, is an investor, developer, and community builder who creates content across Twitch and YouTube covering gaming, investing, and music production. He is the founder of B5TA, a gaming community built around RuneScape and Discord, and the creator of the Composer.trade symphonies documented in this library.",
          "zoop approaches investing the same way he approaches game development and community-building: systematically, iteratively, and with a focus on sharing the process with others. The strategies in this library are the result of years of research into leveraged ETF behavior, regime-detection signals, and risk management techniques, refined through community feedback and live performance tracking.",
          "More about zoop: https://azqato.com/about.html"
        ]
      },
      {
        "title": "The Strategy Suite",
        "paragraphs": [
          "The zoops-* strategies are zoop's primary Composer.trade symphony collection, each built around a shared philosophy: use 3x leveraged Nasdaq ETFs (primarily TQQQ) during confirmed bull markets, and rotate to defensive or inverse positions when trend signals break. The 12 strategies in this collection span a spectrum from capital-preservation-first (2026 Frontrunner) to high-conviction aggressive (Sometimes TQQQ, Leveraged TQQQ Symphony).",
          "Each strategy shares a common lineage: the 2026 Frontrunner is the base layer, using RSI-triggered dip-buy signals on a universe of leveraged ETFs with BIL as the default. The other strategies layer additional macro signals, sector momentum filters, and bear-mode intelligence on top of this foundation, each one a different answer to the question of how aggressively to pursue returns within a risk-managed framework.",
          "Across the 12 zoops-* strategies, the backtested annualized return ranges from ~92% (2026 Frontrunner) to ~280% (KMLM Switcher), with Sharpe ratios from ~1.63 to ~2.63 and max drawdowns from ~−22% (2026 Frontrunner) to ~−66% (SOXL Growth). Backtest lengths vary, the 2026 Frontrunner spans ~8.4 years and the KMLM Switcher ~5.5 years, while the remaining strategies cover ~14.2 years, so headline figures are not all measured over the same window. This spread reflects the spectrum of risk tolerance the collection is designed to address."
        ],
        "table": {
          "headers": [
            "Strategy",
            "ARR",
            "Sharpe",
            "Max DD"
          ],
          "rows": [
            [
              "2026 Frontrunner",
              "~91%",
              "~1.78",
              "~−22%"
            ],
            [
              "Holy Grail 2026",
              "~113%",
              "~1.65",
              "~−45%"
            ],
            [
              "TQQQ Long Term 2026",
              "~111%",
              "~1.63",
              "~−46%"
            ],
            [
              "Excellent Adventure 2026",
              "~122%",
              "~1.82",
              "~−46%"
            ],
            [
              "Sometimes TQQQ 2026",
              "~182%",
              "~2.47",
              "~−35%"
            ],
            [
              "Safety Checks 2026",
              "~103%",
              "~1.63",
              "~−43%"
            ],
            [
              "Manhattan Project 2026",
              "~154%",
              "~2.10",
              "~−35%"
            ],
            [
              "KMLM Switcher 2026",
              "~280%",
              "~2.63",
              "~−29%"
            ],
            [
              "UPRO FTLT 2026",
              "~94%",
              "~1.64",
              "~−33%"
            ],
            [
              "Leveraged TQQQ Symphony 2026",
              "~109%",
              "~1.64",
              "~−48%"
            ],
            [
              "TQQQ 200d MA 3x 2026",
              "~109%",
              "~1.65",
              "~−39%"
            ],
            [
              "SOXL Growth 2026",
              "~164%",
              "~1.75",
              "~−66%"
            ]
          ]
        }
      },
      {
        "title": "Design Philosophy",
        "paragraphs": [
          "zoop's strategies share several design principles that distinguish them as a coherent system rather than a collection of unrelated symphonies. First: the primary defense mechanism is always a combination of macro trend confirmation (SPY or QQQ above key moving averages) and RSI-based dip-buy signals, both protective and opportunistic at the same time. The strategy exits leveraged positions when the macro trend breaks, but actively re-enters at panic RSI levels rather than waiting passively in cash.",
          "Second: SH (1x inverse S&P 500) is the default bear-mode hold across most zoops-* strategies, not BIL. This is an explicit directional view: when the bull-regime conditions break, the market is more likely continuing to fall than recovering, so holding SH generates returns from that decline rather than sitting at the risk-free rate. This distinguishes the zoops-* strategies from purely trend-following approaches that use cash as the defensive position.",
          "Third: each strategy in the collection is designed to be held as a single portfolio allocation, not combined with each other. The strategies overlap significantly in signal logic, combining two zoops-* strategies would create correlated double-exposure rather than meaningful diversification. The collection exists to give investors of different risk tolerances a single appropriate choice, not to be held simultaneously."
        ]
      },
      {
        "title": "Community and Transparency",
        "paragraphs": [
          "zoop publishes and discusses his strategies publicly, sharing the signal logic, backtest methodology, and performance tracking openly with his community on Twitch and YouTube. Composer Atlas was built to document this library in one organized, searchable place, providing the in-depth explanations, signal breakdowns, and risk metric comparisons that aren't possible within Composer.trade's interface alone.",
          "The strategies are identified in Composer.trade with the 'zoops-' prefix, making them discoverable and attributable. The '2026' suffix in each strategy name reflects the year these versions were refined and published, zoop iterates on his strategy suite over time, and the year suffix helps track which version a given backtest represents.",
          "To follow zoop's strategy updates, community discussions, and live performance tracking, visit https://azqato.com or find him as Azqato on Twitch and YouTube."
        ]
      }
    ]
  },
  {
    "slug": "backtesting",
    "name": "Backtesting",
    "category": "strategy-concept",
    "description": "The process of simulating a trading strategy against historical data to evaluate how it would have performed, without risking real capital.",
    "formula": null,
    "related_tags": [
      "backtesting"
    ],
    "last_updated": "2026-06-15",
    "sections": [
      {
        "title": "Definition",
        "paragraphs": [
          "Backtesting is the process of applying a trading strategy to historical price data to see how it would have performed in the past. Instead of risking real money to test whether an idea works, a backtest simulates every trade the strategy would have made, logging entries, exits, position sizes, and resulting returns, across years of historical data.",
          "The output is a performance record: total return, annualized return, maximum drawdown, Sharpe ratio, and similar metrics. A strong backtest suggests the strategy has historically earned returns commensurate with its risk. A weak one suggests the opposite, or reveals conditions where the strategy would have suffered deeply.",
          "Backtesting does not guarantee future performance. It is an evaluation tool, not a prediction. Its value is in filtering out ideas that fail on historical data before they can fail in real markets with real money."
        ]
      },
      {
        "title": "How It Works",
        "paragraphs": [
          "At each point in the historical data, the strategy's logic is evaluated exactly as it would be in a live account, using only information available on that date. The strategy's signals fire (or don't), positions are entered or exited, and the resulting portfolio value is tracked day by day.",
          "A rigorous backtest accounts for all relevant costs and mechanics: transaction fees, bid-ask spreads, and in leveraged ETF strategies, the daily compounding effect that creates volatility decay. Ignoring these costs can make a mediocre strategy look exceptional on paper.",
          "The quality of a backtest depends heavily on the data range. A backtest covering only a bull market will overstate returns for long-biased strategies. The best backtests span multiple market regimes, bull markets, bear markets, and sideways chop, so results reflect a range of conditions rather than a single favorable environment."
        ]
      },
      {
        "title": "Common Backtesting Pitfalls",
        "paragraphs": [
          "Survivorship bias: If the backtest dataset only includes assets that still exist today, it artificially inflates returns. Companies that went bankrupt or were delisted are excluded, leaving only the winners. This distorts the simulation because in real markets, investors held those failed assets too.",
          "Look-ahead bias: Using information that would not have been available on the date of a historical trade. For example, using end-of-day closing prices to decide trades that would have needed to be placed mid-day, or using revised economic data rather than the data as originally reported. Look-ahead bias is often subtle and can invisibly inflate backtest performance.",
          "Overfitting (data dredging): Testing hundreds of parameter combinations against the same dataset until one looks exceptional, then claiming that combination is the optimal strategy. A strategy tuned to fit one dataset will often collapse when exposed to new data it was never trained on. The fix is to validate on separate out-of-sample data: run the strategy on a dataset it was never optimized against and see if the results hold.",
          "Curve fitting: A variant of overfitting where the strategy is made so complex, with so many conditions, that it perfectly explains past data but has no predictive power. Simple strategies with few parameters backtest less impressively but tend to be more robust in live trading."
        ]
      },
      {
        "title": "Backtesting vs. Forward Testing",
        "paragraphs": [
          "Forward testing (also called paper trading) is the complement to backtesting. After a strategy passes backtesting, it is run in a live market environment using hypothetical funds, recording every trade and outcome in real time without actual capital at risk. Forward testing validates whether the backtest results hold in a live environment with real fills, real spreads, and real market conditions.",
          "The two processes test different things. Backtesting answers whether the strategy would have worked historically. Forward testing answers whether it works now, catching issues like execution lag, data feed differences, or regime changes that post-date the backtest window.",
          "A strategy that backtests well but fails in forward testing is a signal that the backtest was overfitted to historical conditions or that the market has changed in a way the historical data did not capture. Strong strategies show consistency across both tests."
        ]
      },
      {
        "title": "How Composer.trade Runs Backtests",
        "paragraphs": [
          "Composer.trade's built-in backtest engine simulates every rebalance a symphony would have triggered across the available historical data for its assets. On each rebalance date, the engine evaluates the symphony's conditional logic using the same price and indicator data available on that historical date, then calculates what the portfolio would have looked like the following day after the simulated trade executed.",
          "Rebalance frequency matters significantly. Composer symphonies typically rebalance daily: the signal is evaluated at the close of each trading day, and the position change is assumed to execute at the next day's open. This means there is a one-day lag between a signal firing and the position reflecting it. In a sharp market move, that lag can be the difference between catching a signal and missing a swing.",
          "Composer's backtests use adjusted price data: accounting for stock splits, dividends, and ETF distributions, so the historical return series is comparable across different time periods. This is standard for backtesting tools and ensures a stock split doesn't look like a price crash in the simulation.",
          "One critical limitation: Composer's backtest does not deduct transaction costs, expense ratios, or tax drag by default. The expense ratios on leveraged ETFs (0.75%–0.95% annually for TQQQ, UPRO, etc.) are embedded in the price data through daily NAV adjustments, so they do appear in the simulation, but brokerage commissions and bid-ask spreads are not modeled. For long-term hold strategies this is a minor issue; for high-turnover symphonies that rotate frequently, unmodeled spreads can meaningfully flatter backtest performance."
        ]
      },
      {
        "title": "Reading a Composer Backtest",
        "paragraphs": [
          "Composer displays the backtest output as a performance chart, alongside summary metrics: total return, annualized return (CAGR), maximum drawdown, and Sharpe ratio. Each of these tells a different part of the story. Total return and CAGR describe how much the strategy made; maximum drawdown describes the worst-case loss a real investor would have experienced; Sharpe ratio summarizes the return per unit of risk taken.",
          "The benchmark comparison is essential. Composer defaults to comparing against SPY (S&P 500). A symphony that returned 40% annualized over 5 years sounds impressive, until you see SPY returned 38% over the same period. Outperformance matters more than absolute return, and on a risk-adjusted basis, many strategies that look good in absolute terms do not justify the additional drawdown they impose.",
          "The time range of the backtest matters as much as the results. TQQQ was launched in February 2010, so any strategy holding TQQQ cannot backtest before that date. Many leveraged ETFs have shorter histories, LABU (Biotech Bull 3x) launched in 2015, NAIL (Homebuilders Bull 3x) in 2015, FAS (Financials Bull 3x) in 2008 but with limited reliable data before 2010. A short backtest window that happened to overlap with a bull market run will make almost any long-biased strategy look strong.",
          "Strong backtests share several characteristics: they span at least one full market cycle (bull and bear), they show the strategy surviving a significant drawdown event (2020 COVID crash, 2022 rate hike selloff, or 2008 financial crisis for older strategies), and they demonstrate that the Sharpe ratio is above 1.0, meaning the strategy earned more than one unit of return for each unit of risk."
        ],
        "table": {
          "headers": [
            "Metric",
            "What It Tells You"
          ],
          "rows": [
            [
              "CAGR",
              "Annualized return: how much the strategy grew per year on average"
            ],
            [
              "Max Drawdown",
              "Worst peak-to-trough loss: the pain a real investor would have endured"
            ],
            [
              "Sharpe Ratio",
              "Return per unit of risk: above 1.0 is generally considered strong"
            ],
            [
              "Calmar Ratio",
              "CAGR divided by max drawdown: higher means better return per unit of drawdown risk"
            ]
          ]
        }
      },
      {
        "title": "Limitations of Backtesting",
        "paragraphs": [
          "The fundamental limitation of backtesting is that past performance does not equal future performance. Markets change. Correlations break down. Strategies that worked because of a specific macro regime (persistent low interest rates, for instance) may perform very differently when that regime ends.",
          "In Composer specifically, the available backtest history for leveraged ETFs is relatively short. TQQQ has roughly 15 years of history as of 2026, enough to cover a few cycles, but not enough to make definitive claims about multi-decade robustness. A strategy's backtest starts on the date its most recently launched asset began trading, which can make a strategy appear untested under conditions that occurred before its components existed.",
          "Overfitting is the most persistent risk. Composer makes it easy to add conditions, RSI thresholds, moving average filters, multi-asset ranking logic, and each added condition offers more knobs to turn during optimization. A symphony tuned until its backtest looks perfect is a symphony fit to historical noise, not a strategy with genuine forward-looking edge.",
          "The most honest interpretation of a Composer backtest: it shows you what would have happened if you had run this exact logic on this exact data. That's valuable information. It tells you how the strategy handles stress, what kind of drawdowns it tolerates, and whether its return profile matches your risk appetite. But it is the beginning of strategy evaluation, not the end of it."
        ]
      }
    ]
  },
  {
    "slug": "out-of-sample",
    "name": "Out Of Sample (OOS)",
    "category": "strategy-concept",
    "description": "Data a strategy was not tuned on. Performance out of sample is the honest test of whether a backtest's edge is real or was fitted to the past.",
    "formula": null,
    "related_tags": [
      "backtesting"
    ],
    "last_updated": "2026-10-19",
    "sections": [
      {
        "title": "Definition",
        "paragraphs": [
          "Out of sample (OOS) means data the strategy never saw while it was being built. Every choice in a strategy, which indicator, which window, which threshold, is made by looking at some stretch of history. That stretch is the in-sample period. Anything outside it is out of sample.",
          "The distinction matters because a strategy can always be made to look good on the data it was tuned against. Add enough conditions and almost any history can be explained after the fact. Out-of-sample results are the check: if the edge was real, it should survive on data the builder could not have fitted to."
        ]
      },
      {
        "title": "How It Works",
        "paragraphs": [
          "The classic method is a holdout. Split the history in two, tune the strategy on the first part, then run it unchanged on the second. If the second part looks roughly like the first, the strategy has passed. If returns collapse, the first result was mostly fitting.",
          "Time itself is the cleanest holdout. Any day after the strategy's logic was last changed is out of sample by construction, because nobody could have tuned against a day that had not happened yet. The longer that window, the more weight the comparison carries.",
          "A short out-of-sample window proves little either way. A few weeks of strong results can be luck, and a few weeks of weak results can be an unfavourable regime. Treat the comparison as evidence that accumulates, not a verdict on day one."
        ]
      },
      {
        "title": "In Practice",
        "paragraphs": [
          "On Composer.trade, a symphony's factsheet shows a backtest across its full history, including the years it was tuned on. That number is in sample and will usually flatter the strategy.",
          "This site's Overfit Check measures out-of-sample performance from the date of a symphony's last logic edit and compares it with what the backtest promised over its fitted history. A large gap between the two is the signature of overfitting.",
          "There is a second, stricter sense of the term: live trading. A backtest re-run over recent days still uses simulated fills. Real trades meet real spreads, rebalance timing and slippage. Comparing live daily returns against the backtest over the same days shows how faithfully the simulation tracks reality, which is what the planned Twitch Check tool is designed to measure."
        ]
      }
    ]
  },
  {
    "slug": "original",
    "name": "Original Strategies",
    "category": "strategy-concept",
    "description": "Marks a strategy as the original, unmodified version of its logic, before later editions remixed it with additional layers like frontrunner dip-buys or extra risk checks.",
    "formula": null,
    "related_tags": [
      "original"
    ],
    "last_updated": "2026-07-06",
    "sections": [
      {
        "title": "What 'Original' Means",
        "paragraphs": [
          "The 'Original' tag marks a strategy as the baseline, unmodified version of its trading logic, the form it took before anyone layered additional conditions on top of it. Later editions of the same strategy often add things the original build never had: a frontrunner-style RSI dip-buy layer, extra overbought or volatility guards, additional asset legs, or tighter regime-detection rules. The original entry is what the strategy looked like before any of that was added.",
          "Four strategies currently carry this tag: The Holy Grail, TQQQ For The Long Term, SOXL Growth, and Simon's KMLM Switcher. Each also has a remixed edition elsewhere in this library that builds on the original by adding its own dip-buy layers and risk-management refinements."
        ]
      },
      {
        "title": "Why It's Useful",
        "paragraphs": [
          "Keeping the original version documented alongside its remixed edition lets readers see exactly what changed and why: which conditions were added, which assets were introduced, and how those additions affected the backtested metrics. Without the original for comparison, it's easy to assume a strategy's full rule set was there from the start, when in practice much of the risk management was added later.",
          "This also makes it easier to evaluate a modification on its own merits. If a remixed edition outperforms the original, the 'Original' tag lets a reader trace that improvement back to a specific added layer rather than crediting the strategy's core logic for gains that came from a later addition."
        ]
      }
    ]
  },
  {
    "slug": "sortino-ratio",
    "name": "Sortino Ratio",
    "category": "risk-metric",
    "description": "A variant of the Sharpe ratio that divides excess return by downside deviation only, so upside volatility is not treated as risk.",
    "formula": "Sortino Ratio = (Rp - Rf) / sigma_down",
    "related_tags": [
      "sharpe-ratio",
      "standard-deviation"
    ],
    "last_updated": "2026-08-28",
    "sections": [
      {
        "title": "Definition",
        "paragraphs": [
          "The Sortino ratio measures return per unit of downside risk. It is the Sharpe ratio with one change: the denominator counts only returns below a target (usually zero), rather than the spread of all returns.",
          "The argument for it is that an investor does not experience a large gain as risk. Standard deviation punishes a strategy for a spectacular week exactly as hard as for a terrible one, and the Sortino ratio removes that symmetry."
        ]
      },
      {
        "title": "Formula",
        "paragraphs": [
          "Sortino Ratio = (Rp - Rf) / sigma_down. Where: Rp = portfolio return (annualized), Rf = risk-free rate, sigma_down = standard deviation computed using only periods with returns below the target.",
          "Because the denominator discards roughly half the observations, the Sortino ratio is almost always larger than the Sharpe ratio for the same strategy. Comparing a Sortino to a Sharpe across two strategies is meaningless; compare like with like."
        ]
      },
      {
        "title": "How It Works",
        "paragraphs": [
          "Two strategies can share a Sharpe ratio while behaving completely differently. One grinds out steady small gains and occasionally falls off a cliff; the other is flat most of the time and occasionally jumps. Standard deviation sees the same number for both. Downside deviation separates them.",
          "A large gap between a strategy's Sharpe and Sortino ratios is itself information: it means the volatility is lopsided. A strategy with a Sharpe of 1.6 and a Sortino of 5.7 is generating most of its variance on the upside."
        ]
      },
      {
        "title": "In Practice",
        "paragraphs": [
          "Leveraged and volatility-linked strategies frequently show a flattering Sortino ratio, because a long volatility position produces rare enormous up days that inflate total variance without contributing any downside deviation.",
          "Read it alongside max drawdown. Downside deviation treats a series of small losses and one catastrophic loss as broadly similar if the totals match, while drawdown does not."
        ]
      },
      {
        "title": "Limitations",
        "paragraphs": [
          "Discarding the upside halves the sample, so the estimate is noisier than a Sharpe ratio computed over the same window, and it becomes unstable for strategies that rarely lose.",
          "It says nothing about the order of losses. Ten scattered bad days and ten consecutive bad days produce the same downside deviation, and only one of them is a drawdown a holder would sit through.",
          "A strategy that is out of the market most of the time can post an excellent Sortino ratio simply by not participating, which is a statement about time in market rather than skill."
        ]
      },
      {
        "title": "Using the Sortino Ratio in Composer.trade",
        "paragraphs": [
          "Composer reports Sortino alongside Sharpe on the symphony details page. The useful habit is to look at the two together rather than picking whichever is higher.",
          "When a symphony's Sortino greatly exceeds its Sharpe, check what is producing the upside variance. Frequently it is a hedge sleeve that spikes during crises, and that sleeve is also the part decaying quietly the rest of the time."
        ]
      }
    ]
  },
  {
    "slug": "win-rate",
    "name": "Win Rate",
    "category": "risk-metric",
    "description": "The share of periods with a positive return. On its own it says nothing about whether a strategy makes money.",
    "formula": "Win Rate = winning periods / total periods",
    "related_tags": [
      "backtesting"
    ],
    "last_updated": "2026-08-28",
    "sections": [
      {
        "title": "Definition",
        "paragraphs": [
          "Win rate is the fraction of periods, usually days, in which a strategy returned more than zero. A 55% win rate means 55 of every 100 days closed up.",
          "It is the most intuitive statistic on any strategy page and one of the least informative in isolation, because it deliberately ignores the size of each win and loss."
        ]
      },
      {
        "title": "Formula",
        "paragraphs": [
          "Win Rate = number of periods with return > 0 / total number of periods.",
          "Example: a strategy with 2,050 up days out of 3,741 trading days has a win rate of 54.8%."
        ]
      },
      {
        "title": "How It Works",
        "paragraphs": [
          "Win rate only becomes meaningful when paired with the average size of a win against the average size of a loss. A strategy winning 40% of the time with wins twice the size of losses is profitable; one winning 70% of the time with occasional catastrophic losses is not.",
          "This is why trend-following strategies routinely post win rates below 50% and still compound, while strategies that sell volatility post high win rates and periodically lose years of gains in a week."
        ]
      },
      {
        "title": "In Practice",
        "paragraphs": [
          "Daily win rates cluster tightly. Almost every long-biased equity strategy lands between 52% and 58%, because it is dominated by the underlying market's own up-day frequency. A win rate inside that band tells you very little about the logic on top.",
          "The number becomes interesting when it is far outside the band, or when it is paired with outlier dependence: a 55% win rate combined with the best 5% of days producing more than the total return means most winning days are trivial and a handful carry everything."
        ]
      },
      {
        "title": "Limitations",
        "paragraphs": [
          "It is trivially gameable. Any strategy can raise its win rate by taking small frequent profits and letting losses run, which improves the statistic while worsening the outcome.",
          "It is sensitive to the period chosen. The same strategy measured monthly rather than daily will report a different, usually higher, win rate, so a win rate quoted without its period is not comparable to anything.",
          "It ignores position size entirely, so a strategy in cash on most days can post whatever win rate its few active days happen to produce."
        ]
      },
      {
        "title": "Reading Win Rate in the Composer Atlas Library",
        "paragraphs": [
          "Win rates in this library are computed on daily returns across the full backtest window, so they are comparable across strategies here but not against a figure quoted elsewhere on a monthly basis.",
          "Treat it as a texture statistic rather than a quality one. It describes what holding the strategy feels like day to day, not whether it works."
        ]
      }
    ]
  },
  {
    "slug": "skewness",
    "name": "Skewness",
    "category": "risk-metric",
    "description": "A measure of asymmetry in the return distribution. Positive skew means rare large gains; negative skew means rare large losses.",
    "formula": "Skewness = E[(R - mu)^3] / sigma^3",
    "related_tags": [
      "standard-deviation",
      "leveraged-etfs"
    ],
    "last_updated": "2026-08-28",
    "sections": [
      {
        "title": "Definition",
        "paragraphs": [
          "Skewness describes which tail of the return distribution is longer. A symmetric distribution has a skew of zero. Positive skew means the extreme moves are mostly upward; negative skew means they are mostly downward.",
          "It is one of the few statistics that speaks directly to the shape of a bad outcome rather than its frequency."
        ]
      },
      {
        "title": "Formula",
        "paragraphs": [
          "Skewness = E[(R - mu)^3] / sigma^3, the third standardized moment of the return series. Where: R = period return, mu = mean return, sigma = standard deviation.",
          "Cubing the deviations is what makes the measure directional: negative deviations stay negative when cubed, so a few large losses drag the whole statistic below zero."
        ]
      },
      {
        "title": "How It Works",
        "paragraphs": [
          "Most equity strategies carry mild negative skew, because markets fall faster than they rise. Strategies that sell insurance of any kind, including short volatility positions, carry pronounced negative skew: many small gains funded by rare large losses.",
          "Strongly positive skew usually indicates a long volatility or long options position, where the strategy bleeds slowly and occasionally makes a great deal at once."
        ]
      },
      {
        "title": "In Practice",
        "paragraphs": [
          "A very large positive skew on a leveraged strategy in this library is normally the signature of a volatility hedge sleeve. It is not a sign of safety; it means the return series is dominated by a small number of enormous days.",
          "Skew and outlier dependence tell the same story from different directions. If the best 5% of days account for more than the total return, the skew will be strongly positive, and both numbers are saying the record rests on a handful of sessions."
        ]
      },
      {
        "title": "Limitations",
        "paragraphs": [
          "It is extremely unstable in small samples. A single extraordinary day can move the skew of a multi-year series substantially, so a skew computed over four years of history should not be treated as a property of the strategy.",
          "Cubing exaggerates outliers by construction, which means skewness is close to a restatement of the largest few observations rather than a summary of the whole distribution.",
          "Positive skew is not automatically desirable. A strategy that loses steadily and wins rarely has attractive skew and an unattractive outcome."
        ]
      },
      {
        "title": "Reading Skewness in Composer.trade Strategies",
        "paragraphs": [
          "Check skew before assuming a high Sortino ratio means safety. The two are related: a strategy with large positive skew will show a flattering Sortino because its variance sits on the upside.",
          "For symphonies that route into volatility products, expect large positive skew and read it as a description of the hedge, not as evidence the hedge is cheap."
        ]
      }
    ]
  },
  {
    "slug": "kurtosis",
    "name": "Kurtosis",
    "category": "risk-metric",
    "description": "A measure of how much of a return series comes from extreme moves. High kurtosis means fat tails and a record built on a few sessions.",
    "formula": "Kurtosis = E[(R - mu)^4] / sigma^4",
    "related_tags": [
      "standard-deviation",
      "leveraged-etfs"
    ],
    "last_updated": "2026-08-28",
    "sections": [
      {
        "title": "Definition",
        "paragraphs": [
          "Kurtosis measures the weight of the tails of a return distribution relative to a normal distribution, which has a kurtosis of 3. Values well above 3 mean extreme moves are far more common than a normal distribution would predict.",
          "In plain terms it answers: how much of what this strategy did came from a handful of exceptional days?"
        ]
      },
      {
        "title": "Formula",
        "paragraphs": [
          "Kurtosis = E[(R - mu)^4] / sigma^4, the fourth standardized moment. Raising to the fourth power makes every deviation positive, so unlike skewness it does not distinguish between good and bad extremes, only their size.",
          "Some sources report excess kurtosis, which subtracts 3 so that a normal distribution reads zero. Check which convention a figure uses before comparing it to another."
        ]
      },
      {
        "title": "How It Works",
        "paragraphs": [
          "Financial returns always have fat tails. This is a universal property of markets, not a defect of a particular strategy, which is why a high kurtosis on its own is not a finding.",
          "What matters is the degree. A kurtosis in the tens is ordinary for a leveraged strategy. A kurtosis in the hundreds means the series is effectively a small number of enormous observations surrounded by noise, and every other statistic computed from it, including Sharpe and standard deviation, is resting on very few data points."
        ]
      },
      {
        "title": "In Practice",
        "paragraphs": [
          "Read kurtosis together with the outlier-dependence figures. They are two views of the same fact, and the arithmetic version, such as the best 5% of days producing more than the total return, is the more legible one.",
          "Extremely high kurtosis is a warning that the backtest window contained one or two regime events, and that the strategy's record is really a claim about those events repeating."
        ]
      },
      {
        "title": "Limitations",
        "paragraphs": [
          "Testing whether returns are normally distributed is not a useful exercise. They never are, for good strategies and bad ones alike, so a normality test would reject essentially every row and carry no information.",
          "Like skewness, kurtosis is dominated by the few largest observations and is unstable across windows. Adding or removing one crisis changes it substantially.",
          "It says nothing about direction. A strategy with fat tails on the upside and one with fat tails on the downside can report the same kurtosis."
        ]
      },
      {
        "title": "Reading Kurtosis in the Composer Atlas Library",
        "paragraphs": [
          "Use it as a prompt rather than a score: a high value means go and look at how concentrated the returns are in time before trusting the headline figures.",
          "A strategy whose edge disappears when the largest few days are removed is a strategy fitted to those days, and kurtosis is the fastest way to notice that is worth checking."
        ]
      }
    ]
  },
  {
    "slug": "tail-ratio",
    "name": "Tail Ratio",
    "category": "risk-metric",
    "description": "The size of a strategy's best extreme returns relative to its worst, comparing the right tail of the distribution against the left.",
    "formula": "Tail Ratio = abs(95th percentile return) / abs(5th percentile return)",
    "related_tags": [
      "standard-deviation"
    ],
    "last_updated": "2026-08-28",
    "sections": [
      {
        "title": "Definition",
        "paragraphs": [
          "Tail ratio compares how large a strategy's best outcomes are against how large its worst ones are, usually by dividing the 95th percentile return by the absolute value of the 5th percentile return.",
          "A ratio of 1 means the good and bad extremes are the same size. Above 1 means the upside tail is larger; below 1 means losses are more extreme than gains."
        ]
      },
      {
        "title": "Formula",
        "paragraphs": [
          "Tail Ratio = abs(95th percentile of returns) / abs(5th percentile of returns).",
          "Example: a strategy whose 95th percentile daily return is +6.8% and whose 5th percentile is -3.4% has a tail ratio of 2.0, meaning its good extremes are twice the size of its bad ones."
        ]
      },
      {
        "title": "How It Works",
        "paragraphs": [
          "Where skewness and kurtosis are moments dominated by the single most extreme observations, tail ratio uses percentiles, which makes it noticeably more stable. One remarkable day moves it far less.",
          "It is best read as a statement about payoff shape: a strategy with a high tail ratio wins big and loses small when it moves at all, regardless of how often it does either."
        ]
      },
      {
        "title": "In Practice",
        "paragraphs": [
          "A high tail ratio pairs naturally with a low win rate. Trend-following and long volatility strategies typically show both: they are wrong often and cheaply, and right rarely and expensively.",
          "The reverse combination, a high win rate with a tail ratio below 1, describes a strategy collecting small premiums against occasional large losses, and is worth identifying before rather than after a bad month."
        ]
      },
      {
        "title": "Limitations",
        "paragraphs": [
          "It ignores everything between the fifth and ninety-fifth percentiles, which is 90% of the strategy's history.",
          "It says nothing about frequency. A strategy with an excellent tail ratio can still lose money if the small losses arrive often enough.",
          "Percentile estimates need a reasonable sample. On a short backtest the fifth and ninety-fifth percentiles are themselves estimated from relatively few observations."
        ]
      },
      {
        "title": "Reading Tail Ratio in Composer.trade Strategies",
        "paragraphs": [
          "Read it beside win rate. The pair together describes the payoff profile far better than either does alone, and the combination is what determines whether a strategy is psychologically holdable.",
          "For symphonies with a volatility hedge, expect a tail ratio above 1 and recognise that the cost of that shape is the steady decay of the hedge during the long stretches when nothing happens."
        ]
      }
    ]
  },
  {
    "slug": "herfindahl-index",
    "name": "Herfindahl Index",
    "category": "risk-metric",
    "description": "A concentration measure. Applied to a portfolio it reports how much of the position sits in a single holding, from diversified to entirely concentrated.",
    "formula": "HHI = sum of squared portfolio weights",
    "related_tags": [
      "leveraged-etfs"
    ],
    "last_updated": "2026-08-28",
    "sections": [
      {
        "title": "Definition",
        "paragraphs": [
          "The Herfindahl index, borrowed from competition economics where it measures market concentration, is the sum of the squared weights of the components of a portfolio.",
          "It runs from close to zero for a very evenly spread portfolio up to 1.0 for a portfolio holding a single asset. A value of 1.0 means everything is in one position."
        ]
      },
      {
        "title": "Formula",
        "paragraphs": [
          "HHI = sum of w_i squared, where w_i is the fraction of the portfolio in holding i.",
          "Example: an equal-weighted four-asset portfolio has weights of 0.25 each, so HHI = 4 x 0.0625 = 0.25. A portfolio entirely in one asset has HHI = 1.0. The reciprocal, 1 / HHI, gives the effective number of holdings, which is often the more intuitive way to state it."
        ]
      },
      {
        "title": "How It Works",
        "paragraphs": [
          "Squaring the weights is what makes the measure useful: it grows disproportionately as any single position dominates, so a portfolio with one 90% holding and ten small ones scores as concentrated rather than diversified.",
          "The reciprocal is worth computing. An HHI of 0.25 means an effective four holdings; an HHI of 0.5 means an effective two, whatever the raw count of tickers."
        ]
      },
      {
        "title": "In Practice",
        "paragraphs": [
          "Most Composer symphonies rotate between a small number of positions and hold exactly one at a time, so an HHI at or very near 1.0 is normal here rather than alarming. It reflects the switching design.",
          "The number is more informative when it is not 1.0, and when read against the ticker universe: a symphony that can hold eight instruments but concentrates fully into one at any moment carries the risk of a single-position portfolio while appearing diversified in its asset list."
        ]
      },
      {
        "title": "Limitations",
        "paragraphs": [
          "It is a snapshot of weights and knows nothing about correlation. Eight leveraged US technology funds held in equal weight would score as diversified while behaving as one position.",
          "Measured on a single day, it says nothing about how concentrated the strategy is over time. A rotating strategy is fully concentrated every day and well spread across a year.",
          "It treats a cash position as a holding like any other, so a strategy sitting in Treasury bills can look concentrated when it is in fact not invested."
        ]
      },
      {
        "title": "Reading Concentration in the Composer Atlas Library",
        "paragraphs": [
          "Pair the index with the ticker universe shown on a strategy page. The universe describes what the logic can reach; the index describes how much of it is in use right now.",
          "Where correlation matters more than count, judge the universe directly: a list of eight tickers all expressing one leveraged view on the same index is a concentrated strategy no matter what the arithmetic says."
        ]
      }
    ]
  },
  {
    "slug": "annualized-turnover",
    "name": "Annualized Turnover",
    "category": "risk-metric",
    "description": "How many times a year a strategy replaces its entire position. High turnover drives trading costs, slippage, and short-term tax treatment.",
    "formula": "Annualized Turnover = annual value traded / average portfolio value",
    "related_tags": [
      "backtesting"
    ],
    "last_updated": "2026-08-28",
    "sections": [
      {
        "title": "Definition",
        "paragraphs": [
          "Annualized turnover measures how much trading a strategy does, expressed as the number of times per year it replaces its entire portfolio. A turnover of 1x means the strategy rebuilds its position once a year; 50x means roughly once a week.",
          "It is the bridge between a backtest and what actually reaches an account, because every unit of turnover carries cost."
        ]
      },
      {
        "title": "Formula",
        "paragraphs": [
          "Annualized Turnover = total value traded over a year / average portfolio value.",
          "Example: a strategy that rotates fully between two instruments every fortnight trades its whole book about 26 times a year, giving a turnover near 26x."
        ]
      },
      {
        "title": "How It Works",
        "paragraphs": [
          "Turnover translates into three separate costs. Commissions and fees are the most visible and often the smallest. Bid-ask spread is paid on every entry and exit and is far larger for leveraged and volatility products than for broad index funds. Slippage grows with position size.",
          "A backtest that models none of these will overstate a high-turnover strategy far more than a low-turnover one, so turnover is a good proxy for how much a paper record is likely to shrink in practice."
        ]
      },
      {
        "title": "In Practice",
        "paragraphs": [
          "Threshold-based symphonies that switch on a daily signal generate turnover in the tens of times a year, and tiered designs that scale between several states can generate considerably more.",
          "Turnover also determines tax treatment. A strategy that holds nothing for a year produces short-term capital gains taxed as ordinary income, which can be a larger drag than trading costs and does not appear in any backtest."
        ]
      },
      {
        "title": "Limitations",
        "paragraphs": [
          "It counts trades without regard to what they cost. Rotating between two liquid large-cap funds and rotating between two thin leveraged products produce the same turnover and very different bills.",
          "It is an average and hides clustering. A strategy that sits still for months and then trades every day during a crisis reports a moderate figure while concentrating its costs at the worst possible moment.",
          "It does not capture the difference between a scheduled rebalance and a signal that whipsaws in and out of the same position repeatedly."
        ]
      },
      {
        "title": "Reading Turnover in Composer.trade Symphonies",
        "paragraphs": [
          "Compare turnover against the instruments in the strategy's universe. High turnover in liquid index funds is manageable; the same figure in leveraged volatility products is a much larger real cost.",
          "Read it alongside the K-1 and tax considerations for the holdings involved. A high-turnover strategy in commodity pool funds combines short-term gains with a Schedule K-1, and both arrive after the fact."
        ]
      }
    ]
  }
];
