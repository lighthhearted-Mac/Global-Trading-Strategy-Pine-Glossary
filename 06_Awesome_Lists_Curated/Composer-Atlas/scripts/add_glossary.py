#!/usr/bin/env python3
"""
add_glossary.py: One-time script that appended 9 new glossary entries (SMA, EMA,
MACD, Mean Reversion, Volatility Decay, Standard Deviation, ARR, Managed Futures,
Inverse ETFs) to data/glossary.json and data/glossary.js.

Already applied as of v1.5.2 (2026-06-15). Safe to re-run, duplicate-slug check
will abort without writing if entries are already present.

Usage:
    python scripts/add_glossary.py
"""

import json
from pathlib import Path

BASE_DIR     = Path(__file__).resolve().parent.parent
GLOSSARY_JSON = BASE_DIR / "data" / "glossary.json"
GLOSSARY_JS   = BASE_DIR / "data" / "glossary.js"

NEW_ENTRIES = [
  {
    "slug": "sma",
    "name": "Simple Moving Average (SMA)",
    "category": "indicator",
    "description": "The unweighted average of an asset's closing prices over a specified lookback window, the foundational trend signal used by nearly every strategy in this library.",
    "formula": "SMA(N) = (P1 + P2 + ... + PN) / N",
    "related_tags": ["200d-ma"],
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
          "headers": ["Period", "Common Use"],
          "rows": [
            ["10-20 day SMA", "Short-term regime gate; reactive to recent momentum"],
            ["50-day SMA", "Intermediate trend; medium-term regime confirmation"],
            ["200-day SMA", "Long-term bull/bear regime; the most widely watched SMA in markets"]
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
          "Lag: the SMA reflects the past, not the present. During a sharp market reversal, the SMA can be 15-25% away from the current price before it begins to confirm the new trend direction."
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
    "formula": "EMA = Price x k + EMA(prev) x (1 - k), where k = 2 / (N + 1)",
    "related_tags": ["200d-ma"],
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
          "The smoothing factor k = 2 / (N + 1) determines how quickly the EMA responds to new prices. For a 10-day EMA, k = 2/11 approximately 0.182. Each new EMA value is: today's price x k plus the previous EMA x (1 - k). Today's price contributes about 18.2% of the new value; the accumulated history contributes 81.8%.",
          "Unlike the SMA, which drops a day entirely once it falls outside the lookback window, the EMA technically carries influence from all past prices with exponentially declining weight. This makes the EMA more sensitive to recent moves than the SMA of the same period.",
          "Comparing EMA to SMA on the same asset: when the EMA is above the SMA, recent prices are running higher than the historical average, a sign of accelerating momentum. When EMA is below SMA, recent prices are falling behind the historical average. Several strategies use this EMA-vs-SMA comparison as a momentum acceleration signal."
        ],
        "table": {
          "headers": ["Property", "EMA", "SMA"],
          "rows": [
            ["Weight to recent prices", "Higher (exponential decay)", "Equal (flat weighting)"],
            ["Responsiveness", "Faster reaction to new data", "Slower, more stable"],
            ["Whipsaw tendency", "More prone in choppy markets", "Less prone; more noise-resistant"],
            ["Best used for", "Shorter-period timing signals", "Longer-period regime gates"]
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
    "description": "Moving Average Convergence Divergence, a momentum indicator measuring the spread between two EMAs, used to detect trend changes through crossovers and momentum shifts.",
    "formula": "MACD = EMA(12) - EMA(26); Signal Line = EMA(9) of MACD",
    "related_tags": ["macd"],
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
          "Standard settings: EMA(12) as the fast line, EMA(26) as the slow line, EMA(9) of the MACD line as the signal line. MACD = EMA(12) - EMA(26). When MACD crosses above the signal line, it is a bullish momentum signal. When it crosses below, it is a bearish signal.",
          "In Composer.trade, MACD logic is typically implemented as a direct EMA comparison: SMH EMA(12) greater than SMH EMA(26) is equivalent to SMH MACD being positive. The strategy evaluates the core crossover, is short-term momentum above or below medium-term momentum, and branches on that boolean.",
          "A positive MACD (fast EMA above slow EMA) indicates the asset has gained more in recent periods than in the longer historical window, upward momentum. A negative MACD indicates the reverse, downward or decelerating momentum."
        ],
        "table": {
          "headers": ["MACD Condition", "Interpretation"],
          "rows": [
            ["EMA(12) above EMA(26): MACD positive", "Short-term momentum is bullish; trend accelerating up"],
            ["EMA(12) below EMA(26): MACD negative", "Short-term momentum is bearish; trend decelerating or reversing"],
            ["MACD crossing above signal line", "Momentum shifting bullish, potential entry signal"],
            ["MACD crossing below signal line", "Momentum shifting bearish, potential exit signal"]
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
    "formula": None,
    "related_tags": ["mean-reversion"],
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
    "formula": "Approximate annual decay = -0.5 x Leverage^2 x Annual Variance",
    "related_tags": ["leveraged-etfs"],
    "last_updated": "2026-06-15",
    "sections": [
      {
        "title": "Definition",
        "paragraphs": [
          "Volatility decay (also called beta decay or compounding drag) is the phenomenon where a leveraged ETF loses value in volatile sideways markets, even when the underlying index ends flat. It is a mathematical consequence of daily leverage rebalancing, specifically, the asymmetry between percentage gains and percentage losses.",
          "The core insight: a 10% gain followed by a 10% loss does not return to the starting point. $100 x 1.10 x 0.90 = $99. For a 3x leveraged ETF, a 10% index move in either direction becomes a 30% fund move. $100 x 1.30 x 0.70 = $91, the leveraged fund loses 9% while the underlying index is flat."
        ]
      },
      {
        "title": "How It Works",
        "paragraphs": [
          "Volatility decay is proportional to the variance of daily returns and the square of the leverage multiple. The approximate annual decay: Loss = -0.5 x L^2 x sigma^2, where L is the leverage multiple and sigma^2 is the annual variance of the underlying index.",
          "For a 3x ETF with 20% annual index volatility: Annual decay is approximately -0.5 x 9 x 0.04 = -0.18, or roughly -18% per year from decay alone, before any directional movement from the underlying trend.",
          "This decay becomes catastrophic in bear markets because it compounds with directional loss. Not only does the leveraged fund fall further than 3x the index drop, but the daily swings during the decline add additional decay. This is why a 50% drop in QQQ can produce an 80-90% drop in TQQQ."
        ],
        "table": {
          "headers": ["Market Condition", "Volatility Decay Effect"],
          "rows": [
            ["Steadily rising, low volatility", "Minimal decay; compounding amplifies gains above 3x index"],
            ["Sideways, high volatility", "Significant decay even with zero net index movement"],
            ["Declining, high volatility", "Directional loss + compounding decay, far more than 3x index loss"],
            ["V-shaped crash and recovery", "Decay during the crash means recovery requires far more than 3x the index gain"]
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
          "Volatility decay is not always the dominant effect. In strongly trending markets, the 2009-2021 bull run, the 2023-2025 AI rally, the compounding gains from 3x leverage easily outpace decay. Many investors overweight decay as a reason to avoid leveraged ETFs entirely, missing the periods where leverage provides extraordinary compounding.",
          "The decay formula is an approximation. Actual decay depends on the specific sequence of daily returns (path dependency), not just average volatility. A year with the same average volatility can produce very different decay depending on whether the volatile days cluster together or spread out evenly.",
          "Expense ratios and swap costs are already incorporated into the ETF's NAV. Investors do not need to separately account for these costs, they are embedded in the price. Volatility decay is additional to, not the same as, these embedded fees."
        ]
      },
      {
        "title": "Designing for Volatility Decay in Composer.trade",
        "paragraphs": [
          "Understanding volatility decay transforms how a Composer.trade builder thinks about exit signals. The primary purpose of the 200d MA gate is not just to avoid directional losses, it is to avoid the high-volatility sideways periods when decay compounds. When QQQ breaks below its 200d MA, the market typically enters a phase of elevated volatility and choppy price action. Exiting to BIL avoids both the directional loss and the decay, the gain in risk-adjusted return from this exit comes from two sources, not one.",
          "Volatility decay creates an asymmetry that makes high-conviction trend-following more valuable for leveraged ETF strategies than for unlevered ones. For a 3x leveraged position, even a false exit has significant value: during the choppy period that triggered the exit, decay would have accumulated regardless of whether the market ultimately recovered. The math consistently favors erring on the side of exiting leveraged positions when volatility rises.",
          "The least understood implication of volatility decay is that TQQQ is not simply a better version of QQQ for a long-term investor. Over 20 years including the 2000-2002 crash and 2008-2009 crisis, passive TQQQ would have destroyed virtually all capital despite QQQ eventually recovering to all-time highs. The decay during those extended volatile bear markets is irreversible, a 90% loss requires a 900% gain to recover. This is precisely why the entire framework of systematic leveraged ETF investing exists."
        ]
      }
    ]
  },
  {
    "slug": "standard-deviation",
    "name": "Standard Deviation",
    "category": "risk-metric",
    "description": "A measure of how widely an investment's returns vary around their average, the most common quantification of volatility and the denominator of the Sharpe ratio.",
    "formula": "sigma = sqrt( sum((Ri - R_mean)^2) / N )",
    "related_tags": ["standard-deviation"],
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
          "Annualizing: daily standard deviation x sqrt(252) (trading days per year) = annualized standard deviation. This is how the figures on Composer Atlas strategy cards are computed.",
          "The strategies in this library range from approximately 40.5% (2026 Frontrunner, which spends most of its time in BIL) to 84.6% annualized standard deviation (SOXL Growth RL, with 3x semiconductor leverage and RL-optimized thresholds). This spread reflects the spectrum from minimal-time-in-risk strategies to fully leveraged semiconductor exposure."
        ],
        "table": {
          "headers": ["Annualized Std Dev", "Volatility Classification"],
          "rows": [
            ["Below 15%", "Low: comparable to a diversified bond fund"],
            ["15-25%", "Moderate: comparable to a broad equity index fund"],
            ["25-40%", "High: sector-concentrated equity or moderate leverage"],
            ["40-65%", "Very High: leveraged ETF territory"],
            ["Above 65%", "Extreme: 3x semiconductor or concentrated sector leverage"]
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
    "description": "The compound annual growth rate of a strategy, how much $1 invested would grow per year if the total backtest return compounded uniformly over the holding period.",
    "formula": "ARR = (Final Value / Initial Value)^(252 / Trading Days) - 1",
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
          "ARR = (Final Value / Initial Value)^(252 / Total Trading Days) - 1. The exponent (252 / days) converts from the actual holding period to an annual basis using 252 as the standard number of trading days per year.",
          "Example: A strategy grew from $1.00 to $100.00 over 3,563 trading days (approximately 14.2 years). ARR = (100)^(252 / 3563) - 1, approximately 37.9% per year. Compounding 37.9% per year for 14.2 years produces exactly $100 from $1.",
          "The relationship between ARR and cumulative return is extremely non-linear. Small differences in ARR over long periods produce enormous differences in cumulative return due to compounding. A 100% ARR over 14 years produces approximately $16,384 from $1. A 150% ARR produces approximately $9,313,000 from $1 over the same period."
        ],
        "table": {
          "headers": ["ARR", "10-Year Growth of $1"],
          "rows": [
            ["10%", "$2.59"],
            ["25%", "$9.31"],
            ["50%", "$57.67"],
            ["100%", "$1,024"],
            ["150%", "$9,313"]
          ]
        }
      },
      {
        "title": "In Practice",
        "paragraphs": [
          "The strategies in the Composer Atlas library show ARRs ranging from approximately 73% (Nancy Pelosi's Chips, SPY Energy Chips) to 735% (s90 Half Low Catch, over only ~2.2 years). Among the zoop strategies, backtested annualized returns range from ~91% (2026 Frontrunner) to ~280% (KMLM Switcher), though backtest lengths vary from ~5.5 to ~14.2 years.",
          "These figures are extraordinary by conventional standards: the S&P 500 has historically returned approximately 10% per year, and professional hedge funds rarely sustain 20-30% annualized over multi-year periods. The strategies achieve these figures through 3x leverage on the Nasdaq 100 combined with systematic risk management that avoids the worst bear market periods."
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
          "Cumulative return: also shown on strategy cards, is the total growth of $1 invested from the start of the backtest. ARR is most useful for comparing strategies of different lengths on equal footing. Cumulative return is most useful for communicating the absolute magnitude of compounding, Sometimes TQQQ's cumulative return of over 2,000,000x over 14.2 years reflects 182% annual compounding sustained across multiple market cycles, which is a more visceral demonstration of the compounding power of systematic leveraged investing than the percentage figure alone conveys."
        ]
      }
    ]
  },
  {
    "slug": "managed-futures",
    "name": "Managed Futures",
    "category": "asset-class",
    "description": "An alternative asset class that systematically trades futures contracts across equities, bonds, commodities, and currencies using trend-following algorithms, historically performing well when equities are in sustained bear markets.",
    "formula": None,
    "related_tags": ["managed-futures"],
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
          "headers": ["Market Condition", "Typical KMLM Behavior"],
          "rows": [
            ["Strong equity bull market", "May underperform; equity trend is positive but KMLM lacks equity exposure"],
            ["Equity bear market with sustained trend", "Often outperforms; bond and commodity futures trend alongside the equity decline"],
            ["Sideways, range-bound markets", "Underperforms; trend signals produce whipsaw losses across 22 markets"],
            ["Inflationary commodity cycle", "Strong outperformance; long commodity futures in trend"],
            ["Rising interest rate cycle", "Outperformance; short bond futures in trend"]
          ]
        }
      },
      {
        "title": "In Practice",
        "paragraphs": [
          "In the Composer Atlas library, KMLM appears in the KMLM Switcher strategy as the defensive alternative to a 4-ETF leveraged equity basket. The thesis: KMLM has historically performed well precisely during the periods when TQQQ performs worst, sustained equity bear markets with high volatility, because those environments produce strong, tradeable trends in bonds, commodities, and currencies.",
          "The strategy's 2022 bear market performance illustrates the concept: KMLM returned approximately +24% while TQQQ fell approximately -80%. This negative correlation during equity stress is the core diversification argument for managed futures alongside leveraged equity, not as a replacement for equity exposure during normal conditions, but as the defensive position that potentially profits from the same conditions that cause the equity position to lose money."
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
    "formula": None,
    "related_tags": ["inverse-etfs"],
    "last_updated": "2026-06-15",
    "sections": [
      {
        "title": "Definition",
        "paragraphs": [
          "Inverse ETFs deliver the negative of their benchmark's daily return. A 1x inverse ETF targeting the S&P 500 (SH) returns +1% when the S&P 500 falls 1%, and -1% when it rises 1%. A 3x inverse ETF (SQQQ) returns +3% when the Nasdaq 100 falls 1%, and -3% when it rises 1%.",
          "Like leveraged long ETFs, inverse ETFs rebalance daily to maintain their target multiple. This daily reset creates the same compounding non-linearity, they are not designed for long-term holding but for short-term tactical positioning during confirmed downtrends or specific hedging conditions."
        ]
      },
      {
        "title": "How It Works",
        "paragraphs": [
          "Inverse ETFs achieve their negative exposure through derivatives: short futures contracts, swap agreements, or put options on the underlying index. Each day, the fund rebalances these positions to maintain exactly -1x or -3x the benchmark's return for that day.",
          "The daily rebalancing creates the same volatility decay problem as leveraged long ETFs, but in reverse. In a declining market, the inverse ETF compounds gains faster than -1x (favorable). In a volatile, sideways market, the inverse ETF decays in value even if the underlying index ends flat (unfavorable). This makes inverse ETFs effective as short-term tactical tools during confirmed downtrends, but costly as permanent hedges against equity exposure."
        ],
        "table": {
          "headers": ["ETF", "Benchmark", "Leverage", "Common Use in This Library"],
          "rows": [
            ["SH", "S&P 500", "-1x", "Primary defensive position in most bear-mode branches"],
            ["SQQQ", "Nasdaq 100 (QQQ)", "-3x", "Aggressive bear-mode short in momentum filters"],
            ["PSQ", "Nasdaq 100", "-1x", "Conservative inverse QQQ for bear-market signal matching"],
            ["SPXU / SPXS", "S&P 500", "-3x", "3x inverse S&P; used in UVXY-triggered defensive routing"],
            ["SOXS", "Semiconductors (SOXX)", "-3x", "Fading semiconductor overbought signals in sector strategies"],
            ["TMV", "20-Year Treasury", "-3x", "Profiting from rising long-term interest rates"],
            ["SARK", "ARKK Innovation", "-1x", "Bear pool anchor in Wooden ARKK Machine's risk-on regime"]
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
  }
]


def main():
    data = json.loads(GLOSSARY_JSON.read_text(encoding="utf-8"))
    print(f"Loaded {len(data)} existing entries")

    existing_slugs = {e["slug"] for e in data}
    new_slugs = [e["slug"] for e in NEW_ENTRIES]
    dupes = [s for s in new_slugs if s in existing_slugs]

    if dupes:
        print(f"ABORT: slugs already exist: {dupes}")
        return

    data.extend(NEW_ENTRIES)

    GLOSSARY_JSON.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {GLOSSARY_JSON.name} ({len(data)} entries)")

    js = (
        "// To update content: edit this file and data/glossary.json in sync.\n"
        f"window.GLOSSARY_DATA = {json.dumps(data, indent=2, ensure_ascii=False)};\n"
    )
    GLOSSARY_JS.write_text(js, encoding="utf-8")
    print(f"Wrote {GLOSSARY_JS.name}")


if __name__ == "__main__":
    main()
