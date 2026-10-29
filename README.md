# Global Trading Strategy & Pine Script Glossary
### A Deduplicated Compendium of 189 Unique Trading Systems across 14 Families with 43 Pine Script v5 Reference Implementations

> **Research Compendium — October 2026 Edition**  
> Derived from global corpora (TradingView, LuxAlgo, PineCoders, MQL5, SSRN, arXiv q-fin, NBER), China quant platforms (JoinQuant, vn.py, myquant, BigQuant, Taoguba), and Russia/CIS algorithmic communities (Smart-Lab, TSLab, MOEX, QUIK).

---

## 📊 Executive Summary & Taxonomy

| Family | Code | Strategies | Pine Script v5 | Primary Edge & Asset Universe |
|---|:---:|:---:|:---:|---|
| [**Breakout & Volatility Expansion**](strategies/03_Breakout_and_Volatility_Expansion/README.md) | `BK` | **13** | **3** | Opening Range Breakouts (ORB), Volatility Expansion, Range Contraction (NR7) |
| [**China-Specific Systems (A-Share & CN Futures)**](strategies/09_China_Specific_A_Share_and_Futures/README.md) | `CN` | **26** | **4** | A-Share Limit Up/Down Auction, Dragon Tiger Board, Convertibles (Jisilu), vn.py |
| [**Crypto-Native Systems (Perp & DEX)**](strategies/12_Crypto_Native_Perpetual_and_DEX/README.md) | `CR` | **11** | **0** | Perpetual Funding Rate Arbitrage, DEX AMM LP Hedging, MEV Sandwich Defense |
| [**Grid, Martingale & Averaging Systems**](strategies/08_Grid_Martingale_and_Averaging/README.md) | `GR` | **7** | **2** | Geometric Grid Trading, Martingale Risk Analysis, Dynamic DCA Geometry |
| [**Indicator Hybrids & Cycles**](strategies/05_Indicator_Hybrids_and_Cycles/README.md) | `IH` | **14** | **3** | Ehlers Cycle Theory, WaveTrend, QQE, Fisher Transform, Trend/Oscillator Hybrids |
| [**Machine Learning & AI Systems**](strategies/13_Machine_Learning_and_AI/README.md) | `ML` | **7** | **0** | Walk-Forward Matrix, Deflated Sharpe, k-NN Pattern Classification, Overfitting Gates |
| [**Mean Reversion & Oscillators**](strategies/02_Mean_Reversion_and_Oscillators/README.md) | `MR` | **15** | **7** | Bollinger Bands, RSI, Oscillators, Mean Reversion, Statistical Overextension |
| [**Price Action & Smart Money**](strategies/04_Price_Action_and_Smart_Money/README.md) | `PA` | **16** | **4** | Wyckoff Phase Accumulation, SMC / Liquidity Sweeps, Order Blocks, Price Action |
| [**Russia/CIS-Specific Systems (MOEX & Si)**](strategies/10_Russia_CIS_Specific_MOEX_Systems/README.md) | `RU` | **16** | **2** | MOEX Dividend Gap Recovery, Elder Triple Screen, Si Futures Order Book Scalping |
| [**Risk, Sizing & Execution Models**](strategies/14_Risk_Sizing_and_Execution/README.md) | `RX` | **7** | **2** | Fixed Fractional Risk, Half-Kelly Sizing, Volatility Units (ATR), TWAP/VWAP |
| [**Session, Time & Calendar Edges**](strategies/07_Session_Time_and_Calendar_Edges/README.md) | `SE` | **9** | **1** | Asia/London/NY Session Brackets, Day-of-Week Edges, Month-End Rebalancing |
| [**Statistical, Factor & Arbitrage Systems**](strategies/11_Statistical_Factor_and_Arbitrage/README.md) | `ST` | **18** | **1** | Cointegration Pairs Trading, PCA Statistical Arbitrage, Dispersion, Cross-Sectional |
| [**Trend Following & Momentum**](strategies/01_Trend_Following_and_Momentum/README.md) | `TR` | **18** | **12** | Futures, FX, Trend Following, Donchian, Turtle, Adaptive Averages (KAMA/FRAMA) |
| [**Volume, Order Flow & Market Profile**](strategies/06_Volume_Order_Flow_and_Profile/README.md) | `VO` | **12** | **2** | Volume Profile, Order Flow, VWAP StDev Bands, Cumulative Volume Delta (CVD) |

**Total: 189 Unique Strategies | 43 Pine Script v5 Implementations | 14 Specialized Families**

---

## 🗂️ Master Strategy Index (189 Unique Systems)

| ID | Canonical Strategy | Family | Multilingual Names | Pine v5 Code |
|---|---|:---:|---|:---:|
| **BK-01** | [Opening Range Breakout (ORB)](strategies/03_Breakout_and_Volatility_Expansion/README.md#bk-01--opening_range_breakout_orb) | `BK` | 开盘区间突破 · Пробой диапазона открытия | [`bk-01_opening_range_breakout_orb.pine`](strategies/03_Breakout_and_Volatility_Expansion/bk-01_opening_range_breakout_orb.pine) |
| **BK-02** | [Narrow Range 7 / Inside Day Patterns](strategies/03_Breakout_and_Volatility_Expansion/README.md#bk-02--narrow_range_7_inside_day_patterns) | `BK` | 窄幅整理形态 · Внутренний день / узкий диапазон | 📖 Logic-only |
| **BK-03** | [Volatility Contraction Pattern (VCP)](strategies/03_Breakout_and_Volatility_Expansion/README.md#bk-03--volatility_contraction_pattern_vcp) | `BK` | 波动收缩形态 · Модель сжатия волатильности | [`bk-03_volatility_contraction_pattern_vcp.pine`](strategies/03_Breakout_and_Volatility_Expansion/bk-03_volatility_contraction_pattern_vcp.pine) |
| **BK-04** | [Darvas Box](strategies/03_Breakout_and_Volatility_Expansion/README.md#bk-04--darvas_box) | `BK` | 达瓦斯箱体 · Ящик Дарваса | 📖 Logic-only |
| **BK-05** | [Bill Williams Alligator + Fractals](strategies/03_Breakout_and_Volatility_Expansion/README.md#bk-05--bill_williams_alligator_fractals) | `BK` | 比尔·威廉姆斯鳄鱼线+分形 · Аллигатор и фракталы Вильямса | [`bk-05_bill_williams_alligator_fractals.pine`](strategies/03_Breakout_and_Volatility_Expansion/bk-05_bill_williams_alligator_fractals.pine) |
| **BK-06** | [Awesome Oscillator / Accelerator System](strategies/03_Breakout_and_Volatility_Expansion/README.md#bk-06--awesome_oscillator_accelerator_system) | `BK` | 神奇震荡指标系统 · Система по AO/AC | 📖 Logic-only |
| **BK-07** | [Aroon Breakout](strategies/03_Breakout_and_Volatility_Expansion/README.md#bk-07--aroon_breakout) | `BK` | 阿隆指标突破 · Система по Aroon | 📖 Logic-only |
| **BK-08** | [Range Breakout with Volume Surge (放量突破)](strategies/03_Breakout_and_Volatility_Expansion/README.md#bk-08--range_breakout_with_volume_surge) | `BK` | 放量突破平台 · Пробой флэта с объёмом | 📖 Logic-only |
| **BK-09** | [Consolidation Box Breakout](strategies/03_Breakout_and_Volatility_Expansion/README.md#bk-09--consolidation_box_breakout) | `BK` | 平台整理突破 · Пробой боковика | 📖 Logic-only |
| **BK-10** | [Gap Playbook (Fade / Continue)](strategies/03_Breakout_and_Volatility_Expansion/README.md#bk-10--gap_playbook_fade_continue) | `BK` | 跳空缺口策略 · Стратегии гэпов | 📖 Logic-only |
| **BK-11** | [Squeeze Pro / Multi-Threshold Squeeze](strategies/03_Breakout_and_Volatility_Expansion/README.md#bk-11--squeeze_pro_multi_threshold_squeeze) | `BK` | 多档挤压指标 · Squeeze Pro | 📖 Logic-only |
| **BK-12** | [High-of-Day Break & Retest](strategies/03_Breakout_and_Volatility_Expansion/README.md#bk-12--high_of_day_break_retest) | `BK` | 日内新高突破回踩 · Пробой максимума дня с ретестом | 📖 Logic-only |
| **BK-13** | [Volatility Expansion Breakout (Keltner/ATR form)](strategies/03_Breakout_and_Volatility_Expansion/README.md#bk-13--volatility_expansion_breakout_keltneratr_form) | `BK` | 波动扩张突破 · Пробой расширения волатильности | 📖 Logic-only |
| **CN-01** | [Chan Theory (缠论): Fractals, Pens, Pivots & Three Buy/Sell Points](strategies/09_China_Specific_A_Share_and_Futures/README.md#cn-01--chan_theory_fractals_pens_pivots_three_buysell_points) | `CN` | 缠论：分型、笔、中枢与三类买卖点 | [`cn-01_chan_theory_fractals_pens_pivots_three_buysell_points.pine`](strategies/09_China_Specific_A_Share_and_Futures/cn-01_chan_theory_fractals_pens_pivots_three_buysell_points.pine) |
| **CN-02** | [Limit-Up Board Tactics (打板：首板/连板/接力)](strategies/09_China_Specific_A_Share_and_Futures/README.md#cn-02--limit_up_board_tactics) | `CN` | 涨停板战法 | [`cn-02_limit_up_board_tactics.pine`](strategies/09_China_Specific_A_Share_and_Futures/cn-02_limit_up_board_tactics.pine) |
| **CN-03** | [Limit-Up Pullback Re-entry (涨停回马枪)](strategies/09_China_Specific_A_Share_and_Futures/README.md#cn-03--limit_up_pullback_re_entry) | `CN` | 涨停回马枪 | [`cn-03_limit_up_pullback_re_entry.pine`](strategies/09_China_Specific_A_Share_and_Futures/cn-03_limit_up_pullback_re_entry.pine) |
| **CN-04** | [Dragon-Head Leading-Stock Tactics (龙头战法)](strategies/09_China_Specific_A_Share_and_Futures/README.md#cn-04--dragon_head_leading_stock_tactics) | `CN` | 龙头战法 | 📖 Logic-only |
| **CN-05** | [Sentiment Cycle Model (情绪周期)](strategies/09_China_Specific_A_Share_and_Futures/README.md#cn-05--sentiment_cycle_model) | `CN` | 情绪周期：冰点→发酵→高潮→退潮 | 📖 Logic-only |
| **CN-06** | [Chip Distribution (筹码分布 / CYQ)](strategies/09_China_Specific_A_Share_and_Futures/README.md#cn-06--chip_distribution_cyq) | `CN` | 筹码分布与SCR指标 | 📖 Logic-only |
| **CN-07** | [Dragon-Tiger List Following (龙虎榜跟随)](strategies/09_China_Specific_A_Share_and_Futures/README.md#cn-07--dragon_tiger_list_following) | `CN` | 龙虎榜策略 | 📖 Logic-only |
| **CN-08** | [Northbound Capital Following (北向资金跟随)](strategies/09_China_Specific_A_Share_and_Futures/README.md#cn-08--northbound_capital_following) | `CN` | 北向资金策略 | 📖 Logic-only |
| **CN-09** | [Margin Balance Sentiment (融资融券情绪)](strategies/09_China_Specific_A_Share_and_Futures/README.md#cn-09--margin_balance_sentiment) | `CN` | 两融情绪策略 | 📖 Logic-only |
| **CN-10** | [Double-Low Convertible Bonds (双低可转债)](strategies/09_China_Specific_A_Share_and_Futures/README.md#cn-10--double_low_convertible_bonds) | `CN` | 双低转债策略 | 📖 Logic-only |
| **CN-11** | [Large/Small-Cap Rotation (大小盘轮动)](strategies/09_China_Specific_A_Share_and_Futures/README.md#cn-11--largesmall_cap_rotation) | `CN` | 大小盘轮动策略 | 📖 Logic-only |
| **CN-12** | [Sector Rotation (行业轮动)](strategies/09_China_Specific_A_Share_and_Futures/README.md#cn-12--sector_rotation) | `CN` | 行业轮动策略 | 📖 Logic-only |
| **CN-13** | [Index Enhancement (指数增强)](strategies/09_China_Specific_A_Share_and_Futures/README.md#cn-13--index_enhancement) | `CN` | 指数增强策略 | 📖 Logic-only |
| **CN-14** | [Alpha Strategy with Index-Futures Hedge (阿尔法策略)](strategies/09_China_Specific_A_Share_and_Futures/README.md#cn-14--alpha_strategy_with_index_futures_hedge) | `CN` | 阿尔法策略 | 📖 Logic-only |
| **CN-15** | [Multi-Factor Stock Selection (多因子选股)](strategies/09_China_Specific_A_Share_and_Futures/README.md#cn-15--multi_factor_stock_selection) | `CN` | 多因子选股策略 | 📖 Logic-only |
| **CN-16** | [MA Convergence Breakout (均线粘合突破)](strategies/09_China_Specific_A_Share_and_Futures/README.md#cn-16--ma_convergence_breakout) | `CN` | 均线粘合突破战法 | [`cn-16_ma_convergence_breakout.pine`](strategies/09_China_Specific_A_Share_and_Futures/cn-16_ma_convergence_breakout.pine) |
| **CN-17** | [N-Structure Tactics (N字战法)](strategies/09_China_Specific_A_Share_and_Futures/README.md#cn-17--n_structure_tactics_n) | `CN` | N字战法 | 📖 Logic-only |
| **CN-18** | [Rising Pullback System (上升回档)](strategies/09_China_Specific_A_Share_and_Futures/README.md#cn-18--rising_pullback_system) | `CN` | 上升回档模式 | 📖 Logic-only |
| **CN-19** | [Main-Force Accumulation Tracking (主力吸筹跟踪)](strategies/09_China_Specific_A_Share_and_Futures/README.md#cn-19--main_force_accumulation_tracking) | `CN` | 主力吸筹战法 | 📖 Logic-only |
| **CN-20** | [Swing Band System (波段操作 / 波段王)](strategies/09_China_Specific_A_Share_and_Futures/README.md#cn-20--swing_band_system) | `CN` | 波段王 | 📖 Logic-only |
| **CN-21** | [Intraday T+0 Around Base Position (底仓做T)](strategies/09_China_Specific_A_Share_and_Futures/README.md#cn-21--intraday_t0_around_base_position_t) | `CN` | 底仓做T策略 | 📖 Logic-only |
| **CN-22** | [Call-Auction & Tail-Session Tactics (集合竞价/尾盘战法)](strategies/09_China_Specific_A_Share_and_Futures/README.md#cn-22--call_auction_tail_session_tactics) | `CN` | 集合竞价与尾盘战法 | 📖 Logic-only |
| **CN-23** | [Calendar Spread Arbitrage (跨期套利)](strategies/09_China_Specific_A_Share_and_Futures/README.md#cn-23--calendar_spread_arbitrage) | `CN` | 跨期套利 | 📖 Logic-only |
| **CN-24** | [Cross-Commodity Spreads (跨品种套利)](strategies/09_China_Specific_A_Share_and_Futures/README.md#cn-24--cross_commodity_spreads) | `CN` | 跨品种套利 | 📖 Logic-only |
| **CN-25** | [Futures-Cash Basis Arbitrage (期现套利)](strategies/09_China_Specific_A_Share_and_Futures/README.md#cn-25--futures_cash_basis_arbitrage) | `CN` | 期现套利与ETF套利 | 📖 Logic-only |
| **CN-26** | [Valuation-Band Rotation (估值分位轮动)](strategies/09_China_Specific_A_Share_and_Futures/README.md#cn-26--valuation_band_rotation) | `CN` | 估值分位轮动策略 | 📖 Logic-only |
| **CR-01** | [Funding-Rate Arbitrage (Delta-Neutral Carry)](strategies/12_Crypto_Native_Perpetual_and_DEX/README.md#cr-01--funding_rate_arbitrage_delta_neutral_carry) | `CR` | 资金费率套利 · Арбитраж фандинга | 📖 Logic-only |
| **CR-02** | [Cash-and-Carry / Futures Basis Trade](strategies/12_Crypto_Native_Perpetual_and_DEX/README.md#cr-02--cash_and_carry_futures_basis_trade) | `CR` | 期现基差套利 · Кэш-энд-керри | 📖 Logic-only |
| **CR-03** | [Liquidation-Cascade Fade](strategies/12_Crypto_Native_Perpetual_and_DEX/README.md#cr-03--liquidation_cascade_fade) | `CR` | 爆仓瀑布反打 · Фейд каскада ликвидаций | 📖 Logic-only |
| **CR-04** | [Open-Interest Regime Model (OI + Price Matrix)](strategies/12_Crypto_Native_Perpetual_and_DEX/README.md#cr-04--open_interest_regime_model_oi_price_matrix) | `CR` | 持仓量状态模型 · Режимная модель OI | 📖 Logic-only |
| **CR-05** | [On-Chain Whale & Flow Following](strategies/12_Crypto_Native_Perpetual_and_DEX/README.md#cr-05--on_chain_whale_flow_following) | `CR` | 链上巨鲸跟踪 · Следование за китами | 📖 Logic-only |
| **CR-06** | [BTC Dominance / Altcoin Rotation](strategies/12_Crypto_Native_Perpetual_and_DEX/README.md#cr-06--btc_dominance_altcoin_rotation) | `CR` | BTC占比与山寨轮动 · Ротация BTC-альты | 📖 Logic-only |
| **CR-07** | [Crypto Volatility Breakout (Donchian + Funding Filter)](strategies/12_Crypto_Native_Perpetual_and_DEX/README.md#cr-07--crypto_volatility_breakout_donchian_funding_filter) | `CR` | 加密波动突破 · Крипто-пробой | 📖 Logic-only |
| **CR-08** | [Triangular Arbitrage](strategies/12_Crypto_Native_Perpetual_and_DEX/README.md#cr-08--triangular_arbitrage) | `CR` | 三角套利 · Треугольный арбитраж | 📖 Logic-only |
| **CR-09** | [DeFi Concentrated Liquidity Market-Making](strategies/12_Crypto_Native_Perpetual_and_DEX/README.md#cr-09--defi_concentrated_liquidity_market_making) | `CR` | DeFi做市策略 · DeFi ММ (Uniswap v3) | 📖 Logic-only |
| **CR-10** | [MEV Extraction (Sandwich / Backrun) — Documented, Not Endorsed](strategies/12_Crypto_Native_Perpetual_and_DEX/README.md#cr-10--mev_extraction_sandwich_backrun_documented_not_endorsed) | `CR` | MEV抢跑与三明治攻击 | 📖 Logic-only |
| **CR-11** | [Cross-Exchange Latency Arbitrage](strategies/12_Crypto_Native_Perpetual_and_DEX/README.md#cr-11--cross_exchange_latency_arbitrage) | `CR` | 跨所延迟套利 · Межбиржевой арбитраж | 📖 Logic-only |
| **GR-01** | [Classic Spot Grid Bot](strategies/08_Grid_Martingale_and_Averaging/README.md#gr-01--classic_spot_grid_bot) | `GR` | 网格交易机器人 · Сеточный робот | [`gr-01_classic_spot_grid_bot.pine`](strategies/08_Grid_Martingale_and_Averaging/gr-01_classic_spot_grid_bot.pine) |
| **GR-02** | [Martingale / Averaging-Down Systems](strategies/08_Grid_Martingale_and_Averaging/README.md#gr-02--martingale_averaging_down_systems) | `GR` | 马丁格尔加仓 · Мартингейл / усреднение | [`gr-02_martingale_averaging_down_systems.pine`](strategies/08_Grid_Martingale_and_Averaging/gr-02_martingale_averaging_down_systems.pine) |
| **GR-03** | [Anti-Martingale Pyramiding](strategies/08_Grid_Martingale_and_Averaging/README.md#gr-03--anti_martingale_pyramiding) | `GR` | 反马丁加仓 · Анти-мартингейл | 📖 Logic-only |
| **GR-04** | [DCA & Smart DCA Bots](strategies/08_Grid_Martingale_and_Averaging/README.md#gr-04--dca_smart_dca_bots) | `GR` | 定投与智能定投机器人 · DCA-боты | 📖 Logic-only |
| **GR-05** | [Fibonacci Grid](strategies/08_Grid_Martingale_and_Averaging/README.md#gr-05--fibonacci_grid) | `GR` | 斐波那契网格 · Фибо-сетка | 📖 Logic-only |
| **GR-06** | [ATR-Adaptive Grid](strategies/08_Grid_Martingale_and_Averaging/README.md#gr-06--atr_adaptive_grid) | `GR` | ATR自适应网格 · Адаптивная сетка по ATR | 📖 Logic-only |
| **GR-07** | [Portfolio Rebalancing Bot](strategies/08_Grid_Martingale_and_Averaging/README.md#gr-07--portfolio_rebalancing_bot) | `GR` | 组合再平衡机器人 · Ребаланс-боты | 📖 Logic-only |
| **IH-01** | [MESA Adaptive MA (MAMA / FAMA)](strategies/05_Indicator_Hybrids_and_Cycles/README.md#ih-01--mesa_adaptive_ma_mama_fama) | `IH` | MESA自适应均线 · Адаптивная MESA | 📖 Logic-only |
| **IH-02** | [Instantaneous Trendline & Sine Wave](strategies/05_Indicator_Hybrids_and_Cycles/README.md#ih-02--instantaneous_trendline_sine_wave) | `IH` | 瞬时趋势线与正弦波 · Мгновенная линия тренда | 📖 Logic-only |
| **IH-03** | [Cyber Cycle](strategies/05_Indicator_Hybrids_and_Cycles/README.md#ih-03--cyber_cycle) | `IH` | 赛博周期 · Кибер-цикл | 📖 Logic-only |
| **IH-04** | [Ehlers SuperSmoother / Roofing Filter](strategies/05_Indicator_Hybrids_and_Cycles/README.md#ih-04--ehlers_supersmoother_roofing_filter) | `IH` | 超级平滑器 · Супер-сглаживатель | [`ih-04_ehlers_supersmoother_roofing_filter.pine`](strategies/05_Indicator_Hybrids_and_Cycles/ih-04_ehlers_supersmoother_roofing_filter.pine) |
| **IH-05** | [Vortex Indicator](strategies/05_Indicator_Hybrids_and_Cycles/README.md#ih-05--vortex_indicator) | `IH` | 涡流指标 · Индикатор Вортекс | [`ih-05_vortex_indicator.pine`](strategies/05_Indicator_Hybrids_and_Cycles/ih-05_vortex_indicator.pine) |
| **IH-06** | [True Strength Index (TSI)](strategies/05_Indicator_Hybrids_and_Cycles/README.md#ih-06--true_strength_index_tsi) | `IH` | 真实强度指数 · Индекс истинной силы | [`ih-06_true_strength_index_tsi.pine`](strategies/05_Indicator_Hybrids_and_Cycles/ih-06_true_strength_index_tsi.pine) |
| **IH-07** | [Schaff Trend Cycle](strategies/05_Indicator_Hybrids_and_Cycles/README.md#ih-07--schaff_trend_cycle) | `IH` | 沙夫趋势循环 · Трендовый цикл Шаффа | 📖 Logic-only |
| **IH-08** | [Connors RSI (Composite)](strategies/05_Indicator_Hybrids_and_Cycles/README.md#ih-08--connors_rsi_composite) | `IH` | 康纳斯复合RSI · Композитный RSI Коннорса | 📖 Logic-only |
| **IH-09** | [Stochastic RSI](strategies/05_Indicator_Hybrids_and_Cycles/README.md#ih-09--stochastic_rsi) | `IH` | 随机RSI · Stochastic RSI | 📖 Logic-only |
| **IH-10** | [Commodity Channel Index Systems](strategies/05_Indicator_Hybrids_and_Cycles/README.md#ih-10--commodity_channel_index_systems) | `IH` | CCI顺势/回归系统 · Системы по CCI | 📖 Logic-only |
| **IH-11** | [Chande Momentum Oscillator](strategies/05_Indicator_Hybrids_and_Cycles/README.md#ih-11--chande_momentum_oscillator) | `IH` | 钱德动量摆动指标 · Осциллятор Чанде | 📖 Logic-only |
| **IH-12** | [Ultimate Oscillator](strategies/05_Indicator_Hybrids_and_Cycles/README.md#ih-12--ultimate_oscillator) | `IH` | 终极摆动指标 · Ультимативный осциллятор | 📖 Logic-only |
| **IH-13** | [Long-Cycle Momentum Composites (KST / Coppock)](strategies/05_Indicator_Hybrids_and_Cycles/README.md#ih-13--long_cycle_momentum_composites_kst_coppock) | `IH` | 长周期动量合成指标 · Долгосрочные осцилляторы | 📖 Logic-only |
| **IH-14** | [Detrended Price Oscillator & Cycle Projection](strategies/05_Indicator_Hybrids_and_Cycles/README.md#ih-14--detrended_price_oscillator_cycle_projection) | `IH` | 去趋势价格振荡器 · DPO и проекция циклов | 📖 Logic-only |
| **ML-01** | [Gradient-Boosted Factor Models (XGBoost/LightGBM Alpha)](strategies/13_Machine_Learning_and_AI/README.md#ml-01--gradient_boosted_factor_models_xgboostlightgbm_alpha) | `ML` | 机器学习多因子选股 · XGBoost/LightGBM альфа | 📖 Logic-only |
| **ML-02** | [LSTM / Sequence Models for Direction](strategies/13_Machine_Learning_and_AI/README.md#ml-02--lstm_sequence_models_for_direction) | `ML` | 长短期记忆网络方向预测 · LSTM-прогноз | 📖 Logic-only |
| **ML-03** | [Reinforcement Learning Portfolios (FinRL lineage)](strategies/13_Machine_Learning_and_AI/README.md#ml-03--reinforcement_learning_portfolios_finrl_lineage) | `ML` | 强化学习组合管理 · RL-портфели | 📖 Logic-only |
| **ML-04** | [HMM Regime Switching](strategies/13_Machine_Learning_and_AI/README.md#ml-04--hmm_regime_switching) | `ML` | 隐马尔可夫状态切换 · HMM-режимы | 📖 Logic-only |
| **ML-05** | [NLP Sentiment & News Trading](strategies/13_Machine_Learning_and_AI/README.md#ml-05--nlp_sentiment_news_trading) | `ML` | 新闻情绪量化 · NLP-сентимент | 📖 Logic-only |
| **ML-06** | [Genetic Algorithms & Parameter Search](strategies/13_Machine_Learning_and_AI/README.md#ml-06--genetic_algorithms_parameter_search) | `ML` | 遗传算法参数寻优 · Генетическая оптимизация | 📖 Logic-only |
| **ML-07** | [Walk-Forward, Deflated Sharpe & Overfitting Control](strategies/13_Machine_Learning_and_AI/README.md#ml-07--walk_forward_deflated_sharpe_overfitting_control) | `ML` | 滚动前推与紧缩夏普 · Контроль переобучения | 📖 Logic-only |
| **MR-01** | [Connors RSI(2) Pullback](strategies/02_Mean_Reversion_and_Oscillators/README.md#mr-01--connors_rsi2_pullback) | `MR` | 康纳斯RSI(2)回调 · Система RSI(2) Коннорса | [`mr-01_connors_rsi2_pullback.pine`](strategies/02_Mean_Reversion_and_Oscillators/mr-01_connors_rsi2_pullback.pine) |
| **MR-02** | [Bollinger Band Reversion (%B Fade)](strategies/02_Mean_Reversion_and_Oscillators/README.md#mr-02--bollinger_band_reversion_b_fade) | `MR` | 布林带回归 · Отскок от границ Боллинджера | [`mr-02_bollinger_band_reversion_b_fade.pine`](strategies/02_Mean_Reversion_and_Oscillators/mr-02_bollinger_band_reversion_b_fade.pine) |
| **MR-03** | [Double 7s / 3-Day High-Low Pullback](strategies/02_Mean_Reversion_and_Oscillators/README.md#mr-03--double_7s_3_day_high_low_pullback) | `MR` | 双七策略 · Система 'двойная семёрка' | 📖 Logic-only |
| **MR-04** | [Keltner Channel Pullback](strategies/02_Mean_Reversion_and_Oscillators/README.md#mr-04--keltner_channel_pullback) | `MR` | 肯特纳通道回调 · Откат по каналам Кельтнера | 📖 Logic-only |
| **MR-05** | [TTM Squeeze / Squeeze Momentum](strategies/02_Mean_Reversion_and_Oscillators/README.md#mr-05--ttm_squeeze_squeeze_momentum) | `MR` | 布林-KC挤压 · Сжатие Боллинджера и Кельтнера | [`mr-05_ttm_squeeze_squeeze_momentum.pine`](strategies/02_Mean_Reversion_and_Oscillators/mr-05_ttm_squeeze_squeeze_momentum.pine) |
| **MR-06** | [QQE (Qualitative Quantitative Estimation)](strategies/02_Mean_Reversion_and_Oscillators/README.md#mr-06--qqe_qualitative_quantitative_estimation) | `MR` | QQE指标系统 · QQE-система | [`mr-06_qqe_qualitative_quantitative_estimation.pine`](strategies/02_Mean_Reversion_and_Oscillators/mr-06_qqe_qualitative_quantitative_estimation.pine) |
| **MR-07** | [WaveTrend Oscillator](strategies/02_Mean_Reversion_and_Oscillators/README.md#mr-07--wavetrend_oscillator) | `MR` | 波形震荡器 · Волновой осциллятор WaveTrend | [`mr-07_wavetrend_oscillator.pine`](strategies/02_Mean_Reversion_and_Oscillators/mr-07_wavetrend_oscillator.pine) |
| **MR-08** | [Fisher Transform Reversal](strategies/02_Mean_Reversion_and_Oscillators/README.md#mr-08--fisher_transform_reversal) | `MR` | 费雪变换反转 · Преобразование Фишера | [`mr-08_fisher_transform_reversal.pine`](strategies/02_Mean_Reversion_and_Oscillators/mr-08_fisher_transform_reversal.pine) |
| **MR-09** | [RSI Regular Divergence System](strategies/02_Mean_Reversion_and_Oscillators/README.md#mr-09--rsi_regular_divergence_system) | `MR` | RSI背离系统 · Дивергенции по RSI | [`mr-09_rsi_regular_divergence_system.pine`](strategies/02_Mean_Reversion_and_Oscillators/mr-09_rsi_regular_divergence_system.pine) |
| **MR-10** | [Stochastic Oversold System](strategies/02_Mean_Reversion_and_Oscillators/README.md#mr-10--stochastic_oversold_system) | `MR` | 随机指标超卖系统 · Система по стохастику | 📖 Logic-only |
| **MR-11** | [Pivot Point Reversion](strategies/02_Mean_Reversion_and_Oscillators/README.md#mr-11--pivot_point_reversion) | `MR` | 枢轴点回归 · Торговля от пивотов | 📖 Logic-only |
| **MR-12** | [Intraday VWAP Mean Reversion](strategies/02_Mean_Reversion_and_Oscillators/README.md#mr-12--intraday_vwap_mean_reversion) | `MR` | VWAP日内均值回归 · Возврат к VWAP | 📖 Logic-only |
| **MR-13** | [Z-Score Spread Reversion](strategies/02_Mean_Reversion_and_Oscillators/README.md#mr-13--z_score_spread_reversion) | `MR` | Z分数价差回归 · Z-score возврат спреда | 📖 Logic-only |
| **MR-14** | [Williams %R Fade](strategies/02_Mean_Reversion_and_Oscillators/README.md#mr-14--williams_r_fade) | `MR` | 威廉指标回归 · Уильямс %R | 📖 Logic-only |
| **MR-15** | [Money-Flow Reversion (CMF/MFI)](strategies/02_Mean_Reversion_and_Oscillators/README.md#mr-15--money_flow_reversion_cmfmfi) | `MR` | 资金流回归 · Возврат по денежному потоку | 📖 Logic-only |
| **PA-01** | [Wyckoff Accumulation/Distribution & Spring (V-Hook)](strategies/04_Price_Action_and_Smart_Money/README.md#pa-01--wyckoff_accumulationdistribution_spring_v_hook) | `PA` | 威科夫吸筹与弹簧效应 · Метод Вайкоффа | [`pa-01_wyckoff_accumulationdistribution_spring_v_hook.pine`](strategies/04_Price_Action_and_Smart_Money/pa-01_wyckoff_accumulationdistribution_spring_v_hook.pine) |
| **PA-02** | [Effort vs Result / Composite Operator Reading](strategies/04_Price_Action_and_Smart_Money/README.md#pa-02--effort_vs_result_composite_operator_reading) | `PA` | 量价背离的威科夫读法 · Соотнесение усилия и результата | 📖 Logic-only |
| **PA-03** | [Pin Bar / Hammer Rejection](strategies/04_Price_Action_and_Smart_Money/README.md#pa-03--pin_bar_hammer_rejection) | `PA` | 长影线反转 · Пинбар | 📖 Logic-only |
| **PA-04** | [Engulfing & Inside-Bar Momentum Patterns](strategies/04_Price_Action_and_Smart_Money/README.md#pa-04--engulfing_inside_bar_momentum_patterns) | `PA` | 吞没与内包形态 · Паттерны поглощения и внутреннего бара | [`pa-04_engulfing_inside_bar_momentum_patterns.pine`](strategies/04_Price_Action_and_Smart_Money/pa-04_engulfing_inside_bar_momentum_patterns.pine) |
| **PA-05** | [Al Brooks Bar-by-Bar Price Action](strategies/04_Price_Action_and_Smart_Money/README.md#pa-05--al_brooks_bar_by_bar_price_action) | `PA` | 布鲁克斯逐K线价格行为 · Прайс-экшн по Бруксу | 📖 Logic-only |
| **PA-06** | [Fakey / False-Breakout Inside-Bar](strategies/04_Price_Action_and_Smart_Money/README.md#pa-06--fakey_false_breakout_inside_bar) | `PA` | 假突破内包形态 · Фейки (ложный пробой) | 📖 Logic-only |
| **PA-07** | [Supply & Demand Zones (Set-and-Forget)](strategies/04_Price_Action_and_Smart_Money/README.md#pa-07--supply_demand_zones_set_and_forget) | `PA` | 供需区域策略 · Зоны спроса и предложения | [`pa-07_supply_demand_zones_set_and_forget.pine`](strategies/04_Price_Action_and_Smart_Money/pa-07_supply_demand_zones_set_and_forget.pine) |
| **PA-08** | [Smart Money Concepts (BOS / CHoCH / Order Blocks / FVG)](strategies/04_Price_Action_and_Smart_Money/README.md#pa-08--smart_money_concepts_bos_choch_order_blocks_fvg) | `PA` | 聪明钱结构交易 · Умные деньги (SMC) | [`pa-08_smart_money_concepts_bos_choch_order_blocks_fvg.pine`](strategies/04_Price_Action_and_Smart_Money/pa-08_smart_money_concepts_bos_choch_order_blocks_fvg.pine) |
| **PA-09** | [ICT Kill Zones, Silver Bullet & Time-Based Liquidity](strategies/04_Price_Action_and_Smart_Money/README.md#pa-09--ict_kill_zones_silver_bullet_time_based_liquidity) | `PA` | ICT时区流动性策略 · ICT Килл-зоны | 📖 Logic-only |
| **PA-10** | [Turtle Soup / Fake Breakout Fade](strategies/04_Price_Action_and_Smart_Money/README.md#pa-10--turtle_soup_fake_breakout_fade) | `PA` | 海龟汤反向策略 · Контрпробой 'Turtle Soup' | 📖 Logic-only |
| **PA-11** | [Harmonic Patterns (Gartley / Bat / Butterfly / AB=CD)](strategies/04_Price_Action_and_Smart_Money/README.md#pa-11--harmonic_patterns_gartley_bat_butterfly_abcd) | `PA` | 谐波形态 · Гармонические паттерны | 📖 Logic-only |
| **PA-12** | [Elliott Wave (Mechanized Approaches)](strategies/04_Price_Action_and_Smart_Money/README.md#pa-12--elliott_wave_mechanized_approaches) | `PA` | 艾略特波浪（机械化） · Волны Эллиотта | 📖 Logic-only |
| **PA-13** | [Wolfe Waves](strategies/04_Price_Action_and_Smart_Money/README.md#pa-13--wolfe_waves) | `PA` | 沃尔夫波浪 · Волны Вольфа | 📖 Logic-only |
| **PA-14** | [Classical Reversal Patterns Automated (Double Top, H&S)](strategies/04_Price_Action_and_Smart_Money/README.md#pa-14--classical_reversal_patterns_automated_double_top_hs) | `PA` | 经典反转形态自动化 · Автоматизация классических паттернов | 📖 Logic-only |
| **PA-15** | [Trendline & Channel Break Automation](strategies/04_Price_Action_and_Smart_Money/README.md#pa-15--trendline_channel_break_automation) | `PA` | 趋势线突破自动化 · Автопробой трендовых линий | 📖 Logic-only |
| **PA-16** | [Round Numbers / Psychological Levels](strategies/04_Price_Action_and_Smart_Money/README.md#pa-16--round_numbers_psychological_levels) | `PA` | 整数关口 · Круглые уровни | 📖 Logic-only |
| **RU-01** | [Elder's Triple Screen](strategies/10_Russia_CIS_Specific_MOEX_Systems/README.md#ru-01--elders_triple_screen) | `RU` | Система «Три экрана» Элдера | [`ru-01_elders_triple_screen.pine`](strategies/10_Russia_CIS_Specific_MOEX_Systems/ru-01_elders_triple_screen.pine) |
| **RU-02** | [Ilan Family (RSI + CCI Martingale Advisors)](strategies/10_Russia_CIS_Specific_MOEX_Systems/README.md#ru-02--ilan_family_rsi_cci_martingale_advisors) | `RU` | Советники «Илан» (RSI+CCI мартингейл) | [`ru-02_ilan_family_rsi_cci_martingale_advisors.pine`](strategies/10_Russia_CIS_Specific_MOEX_Systems/ru-02_ilan_family_rsi_cci_martingale_advisors.pine) |
| **RU-03** | [Sniper Method («Снайпер», Дмитриев / Байнов)](strategies/10_Russia_CIS_Specific_MOEX_Systems/README.md#ru-03--sniper_method) | `RU` | Стратегия «Снайпер» | 📖 Logic-only |
| **RU-04** | [Elder SafeZone Stops & Elder Ray](strategies/10_Russia_CIS_Specific_MOEX_Systems/README.md#ru-04--elder_safezone_stops_elder_ray) | `RU` | SafeZone-стопы и Elder Ray | 📖 Logic-only |
| **RU-05** | [Order-Book (Стакан) Scalping on MOEX Futures](strategies/10_Russia_CIS_Specific_MOEX_Systems/README.md#ru-05--order_book_scalping_on_moex_futures) | `RU` | Стаканный скальпинг (фьючерсы МосБиржи) | 📖 Logic-only |
| **RU-06** | [Synthetic Bond Arbitrage («SyntheticBondsArbitrage»)](strategies/10_Russia_CIS_Specific_MOEX_Systems/README.md#ru-06--synthetic_bond_arbitrage_syntheticbondsarbitrage) | `RU` | Синтетические облигации (арбитраж) | 📖 Logic-only |
| **RU-07** | [Dividend-Gap Trading (Дивидендный гэп)](strategies/10_Russia_CIS_Specific_MOEX_Systems/README.md#ru-07--dividend_gap_trading) | `RU` | Стратегия дивидендного гэпа | 📖 Logic-only |
| **RU-08** | [Pairs Trading on MOEX Equities](strategies/10_Russia_CIS_Specific_MOEX_Systems/README.md#ru-08--pairs_trading_on_moex_equities) | `RU` | Парный трейдинг на акциях МосБиржи | 📖 Logic-only |
| **RU-09** | [Morning Flat Breakout («Пробой утреннего флэта»)](strategies/10_Russia_CIS_Specific_MOEX_Systems/README.md#ru-09--morning_flat_breakout) | `RU` | Пробой утреннего флэта | 📖 Logic-only |
| **RU-10** | [Russian Ichimoku Schools (Ишимоку-школы)](strategies/10_Russia_CIS_Specific_MOEX_Systems/README.md#ru-10--russian_ichimoku_schools) | `RU` | Ишимоку: русские школы системы | 📖 Logic-only |
| **RU-11** | [Automated Fibonacci Level Robots](strategies/10_Russia_CIS_Specific_MOEX_Systems/README.md#ru-11--automated_fibonacci_level_robots) | `RU` | Роботы по уровням Фибоначчи | 📖 Logic-only |
| **RU-12** | [Brent-Urals & Calendar Spread Trading (TSLab)](strategies/10_Russia_CIS_Specific_MOEX_Systems/README.md#ru-12--brent_urals_calendar_spread_trading_tslab) | `RU` | Спред Брент-Юралс и календарные спреды | 📖 Logic-only |
| **RU-13** | [Book + Tape Hybrid (Стакан + Лента) Automation](strategies/10_Russia_CIS_Specific_MOEX_Systems/README.md#ru-13--book_tape_hybrid_automation) | `RU` | Связка «стакан + лента» | 📖 Logic-only |
| **RU-14** | [Smart-Lab Community Trend Robots (Si/RTS)](strategies/10_Russia_CIS_Specific_MOEX_Systems/README.md#ru-14--smart_lab_community_trend_robots_sirts) | `RU` | Трендовые роботы сообщества Smart-Lab | 📖 Logic-only |
| **RU-15** | [T-Bank Community Auto-Strategies (Tinkoff API era)](strategies/10_Russia_CIS_Specific_MOEX_Systems/README.md#ru-15--t_bank_community_auto_strategies_tinkoff_api_era) | `RU` | Стратегии сообщества Т-Банк (Tinkoff API) | 📖 Logic-only |
| **RU-16** | [Academic Quant Lineage (ВШЭ / МФТИ factor studies)](strategies/10_Russia_CIS_Specific_MOEX_Systems/README.md#ru-16--academic_quant_lineage_factor_studies) | `RU` | Академический квант-трек (ВШЭ, МФТИ) | 📖 Logic-only |
| **RX-01** | [Fixed Fractional / Percent-Risk Sizing](strategies/14_Risk_Sizing_and_Execution/README.md#rx-01--fixed_fractional_percent_risk_sizing) | `RX` | 固定比例风险仓位 · Фикс-фракционное позиционирование | 📖 Logic-only |
| **RX-02** | [Kelly & Half-Kelly Criterion](strategies/14_Risk_Sizing_and_Execution/README.md#rx-02--kelly_half_kelly_criterion) | `RX` | 凯利公式与半凯利 · Критерий Келли | [`rx-02_kelly_half_kelly_criterion.pine`](strategies/14_Risk_Sizing_and_Execution/rx-02_kelly_half_kelly_criterion.pine) |
| **RX-03** | [Volatility-Targeted Sizing (ATR Units)](strategies/14_Risk_Sizing_and_Execution/README.md#rx-03--volatility_targeted_sizing_atr_units) | `RX` | 波动率目标仓位 · Волатильно-таргетированный размер | 📖 Logic-only |
| **RX-04** | [Portfolio Heat & Correlation Limits](strategies/14_Risk_Sizing_and_Execution/README.md#rx-04--portfolio_heat_correlation_limits) | `RX` | 组合热度与相关性限制 · Портфельный «нагрев» | 📖 Logic-only |
| **RX-05** | [Breakeven Ratchet & Scale-Out Exits](strategies/14_Risk_Sizing_and_Execution/README.md#rx-05--breakeven_ratchet_scale_out_exits) | `RX` | 保本推进与分批止盈 · Безубыток и частичная фиксация | [`rx-05_breakeven_ratchet_scale_out_exits.pine`](strategies/14_Risk_Sizing_and_Execution/rx-05_breakeven_ratchet_scale_out_exits.pine) |
| **RX-06** | [Time Stops & Opportunity-Cost Exits](strategies/14_Risk_Sizing_and_Execution/README.md#rx-06--time_stops_opportunity_cost_exits) | `RX` | 时间止损 · Временной стоп | 📖 Logic-only |
| **RX-07** | [Execution Algorithms (TWAP / VWAP / POV) & Slippage Budgets](strategies/14_Risk_Sizing_and_Execution/README.md#rx-07--execution_algorithms_twap_vwap_pov_slippage_budgets) | `RX` | 算法交易与滑点预算 · Алго-исполнение | 📖 Logic-only |
| **SE-01** | [Asia Range Sweep & London Reversal](strategies/07_Session_Time_and_Calendar_Edges/README.md#se-01--asia_range_sweep_london_reversal) | `SE` | 亚洲区间扫荡 · Съём азиатского диапазона | 📖 Logic-only |
| **SE-02** | [London Breakout («Лондонский взрыв»)](strategies/07_Session_Time_and_Calendar_Edges/README.md#se-02--london_breakout) | `SE` | 伦敦突破 · Лондонский взрыв | [`se-02_london_breakout.pine`](strategies/07_Session_Time_and_Calendar_Edges/se-02_london_breakout.pine) |
| **SE-03** | [NY Open Momentum (10:00 Rule)](strategies/07_Session_Time_and_Calendar_Edges/README.md#se-03--ny_open_momentum_1000_rule) | `SE` | 纽约开盘动量 · Моментум открытия Нью-Йорка | 📖 Logic-only |
| **SE-04** | [Overnight vs Intraday Edge (Tug of War)](strategies/07_Session_Time_and_Calendar_Edges/README.md#se-04--overnight_vs_intraday_edge_tug_of_war) | `SE` | 隔夜与日内收益差 · Овернайт-эффект | 📖 Logic-only |
| **SE-05** | [Turn-of-Month / Turn-of-Quarter Effect](strategies/07_Session_Time_and_Calendar_Edges/README.md#se-05--turn_of_month_turn_of_quarter_effect) | `SE` | 月末效应 · Эффект конца месяца | 📖 Logic-only |
| **SE-06** | [Sell in May / Halloween Indicator](strategies/07_Session_Time_and_Calendar_Edges/README.md#se-06--sell_in_may_halloween_indicator) | `SE` | 五月卖出效应 · Эффект 'Продавай в мае' | 📖 Logic-only |
| **SE-07** | [Pre-FOMC Announcement Drift](strategies/07_Session_Time_and_Calendar_Edges/README.md#se-07--pre_fomc_announcement_drift) | `SE` | 美联储议息前漂移 · Пре-FOMC дрифт | 📖 Logic-only |
| **SE-08** | [Hour-of-Day Volatility Breakout](strategies/07_Session_Time_and_Calendar_Edges/README.md#se-08--hour_of_day_volatility_breakout) | `SE` | 时段波动突破 · Внутричасовой пробой | 📖 Logic-only |
| **SE-09** | [Crypto Weekend & Funding Window Effects](strategies/07_Session_Time_and_Calendar_Edges/README.md#se-09--crypto_weekend_funding_window_effects) | `SE` | 加密周末与资金费率窗口 · Крипто-сезонность | 📖 Logic-only |
| **ST-01** | [Pairs Trading (Distance Method)](strategies/11_Statistical_Factor_and_Arbitrage/README.md#st-01--pairs_trading_distance_method) | `ST` | 配对交易 · Парный трейдинг | 📖 Logic-only |
| **ST-02** | [Statistical Arbitrage (Avellaneda-Lee)](strategies/11_Statistical_Factor_and_Arbitrage/README.md#st-02--statistical_arbitrage_avellaneda_lee) | `ST` | 统计套利 · Стат-арб Авellaneda | 📖 Logic-only |
| **ST-03** | [Kalman-Filter Hedge Ratio (Dynamic Pairs)](strategies/11_Statistical_Factor_and_Arbitrage/README.md#st-03--kalman_filter_hedge_ratio_dynamic_pairs) | `ST` | 卡尔曼滤波对冲比率 · Фильтр Калмана в парах | 📖 Logic-only |
| **ST-04** | [Cross-Sectional Momentum (Jegadeesh-Titman)](strategies/11_Statistical_Factor_and_Arbitrage/README.md#st-04--cross_sectional_momentum_jegadeesh_titman) | `ST` | 横截面动量因子 · Кросс-секционный моментум | 📖 Logic-only |
| **ST-05** | [Value Factor (HML) & Value-Momentum Combination](strategies/11_Statistical_Factor_and_Arbitrage/README.md#st-05--value_factor_hml_value_momentum_combination) | `ST` | 价值因子与价值动量组合 · Фактор стоимости | 📖 Logic-only |
| **ST-06** | [FX Carry Trade](strategies/11_Statistical_Factor_and_Arbitrage/README.md#st-06--fx_carry_trade) | `ST` | 利差交易 · Керри-трейд | 📖 Logic-only |
| **ST-07** | [Low-Volatility Anomaly](strategies/11_Statistical_Factor_and_Arbitrage/README.md#st-07--low_volatility_anomaly) | `ST` | 低波动异象 · Аномалия низкой волатильности | 📖 Logic-only |
| **ST-08** | [Betting Against Beta (BAB)](strategies/11_Statistical_Factor_and_Arbitrage/README.md#st-08--betting_against_beta_bab) | `ST` | 贝塔对冲因子 · Betting Against Beta | 📖 Logic-only |
| **ST-09** | [Quality / Profitability Factor (QMJ)](strategies/11_Statistical_Factor_and_Arbitrage/README.md#st-09--quality_profitability_factor_qmj) | `ST` | 质量因子 · Фактор качества | 📖 Logic-only |
| **ST-10** | [WorldQuant 101 Formulaic Alphas](strategies/11_Statistical_Factor_and_Arbitrage/README.md#st-10--worldquant_101_formulaic_alphas) | `ST` | WorldQuant 101 Alpha库 | [`st-10_worldquant_101_formulaic_alphas.pine`](strategies/11_Statistical_Factor_and_Arbitrage/st-10_worldquant_101_formulaic_alphas.pine) |
| **ST-11** | [The Factor Zoo & Multiple-Testing Corrections](strategies/11_Statistical_Factor_and_Arbitrage/README.md#st-11--the_factor_zoo_multiple_testing_corrections) | `ST` | 因子动物园与多重检验校正 · Факторный зоопарк | 📖 Logic-only |
| **ST-12** | [COT Positioning Strategies](strategies/11_Statistical_Factor_and_Arbitrage/README.md#st-12--cot_positioning_strategies) | `ST` | CFTC持仓报告策略 · Стратегии по COT | 📖 Logic-only |
| **ST-13** | [Dispersion Trading (Index vs Constituents)](strategies/11_Statistical_Factor_and_Arbitrage/README.md#st-13--dispersion_trading_index_vs_constituents) | `ST` | 离散度交易 · Дисперсионный трейдинг | 📖 Logic-only |
| **ST-14** | [Volatility Risk Premium Harvesting](strategies/11_Statistical_Factor_and_Arbitrage/README.md#st-14--volatility_risk_premium_harvesting) | `ST` | 波动率风险溢价收割 · Сбор премии за волатильность | 📖 Logic-only |
| **ST-15** | [Gamma Scalping (Long-Gamma Rebalancing)](strategies/11_Statistical_Factor_and_Arbitrage/README.md#st-15--gamma_scalping_long_gamma_rebalancing) | `ST` | Гамма-скальпинг | 📖 Logic-only |
| **ST-16** | [Commodity Roll Yield / Contango Harvest](strategies/11_Statistical_Factor_and_Arbitrage/README.md#st-16--commodity_roll_yield_contango_harvest) | `ST` | 商品展期收益 · Ролл-доходность | 📖 Logic-only |
| **ST-17** | [Risk Parity & Volatility Targeting](strategies/11_Statistical_Factor_and_Arbitrage/README.md#st-17--risk_parity_volatility_targeting) | `ST` | 风险平价与波动率目标 · Паритет риска | 📖 Logic-only |
| **ST-18** | [Commodity Seasonality](strategies/11_Statistical_Factor_and_Arbitrage/README.md#st-18--commodity_seasonality) | `ST` | 商品季节性策略 · Сезонность сырья | 📖 Logic-only |
| **TR-01** | [Donchian Channel Breakout](strategies/01_Trend_Following_and_Momentum/README.md#tr-01--donchian_channel_breakout) | `TR` | 唐奇安通道突破 · Прорыв канала Дончиана | [`tr-01_donchian_channel_breakout.pine`](strategies/01_Trend_Following_and_Momentum/tr-01_donchian_channel_breakout.pine) |
| **TR-02** | [Turtle Trading System (S1/S2)](strategies/01_Trend_Following_and_Momentum/README.md#tr-02--turtle_trading_system_s1s2) | `TR` | 海龟交易法则 · Система «Черепах» | [`tr-02_turtle_trading_system_s1s2.pine`](strategies/01_Trend_Following_and_Momentum/tr-02_turtle_trading_system_s1s2.pine) |
| **TR-03** | [Dual Moving Average Crossover (Golden Cross)](strategies/01_Trend_Following_and_Momentum/README.md#tr-03--dual_moving_average_crossover_golden_cross) | `TR` | 双均线金叉死叉 · Пересечение скользящих средних | [`tr-03_dual_moving_average_crossover_golden_cross.pine`](strategies/01_Trend_Following_and_Momentum/tr-03_dual_moving_average_crossover_golden_cross.pine) |
| **TR-04** | [Granville Eight Rules of Moving Averages](strategies/01_Trend_Following_and_Momentum/README.md#tr-04--granville_eight_rules_of_moving_averages) | `TR` | 格兰维尔八大法则 · Восемь правил Гранвиля | 📖 Logic-only |
| **TR-05** | [MACD Trend and Histogram System](strategies/01_Trend_Following_and_Momentum/README.md#tr-05--macd_trend_and_histogram_system) | `TR` | MACD趋势+柱状图系统 · Система по MACD | [`tr-05_macd_trend_and_histogram_system.pine`](strategies/01_Trend_Following_and_Momentum/tr-05_macd_trend_and_histogram_system.pine) |
| **TR-06** | [Parabolic SAR Flip System](strategies/01_Trend_Following_and_Momentum/README.md#tr-06--parabolic_sar_flip_system) | `TR` | 抛物线SAR系统 · Система по Параболику SAR | [`tr-06_parabolic_sar_flip_system.pine`](strategies/01_Trend_Following_and_Momentum/tr-06_parabolic_sar_flip_system.pine) |
| **TR-07** | [ADX/DMI Trend Filter System](strategies/01_Trend_Following_and_Momentum/README.md#tr-07--adxdmi_trend_filter_system) | `TR` | ADX/DMI趋势过滤系统 · Система на ADX/DMI | 📖 Logic-only |
| **TR-08** | [SuperTrend](strategies/01_Trend_Following_and_Momentum/README.md#tr-08--supertrend) | `TR` | 超级趋势 · Супертренд | [`tr-08_supertrend.pine`](strategies/01_Trend_Following_and_Momentum/tr-08_supertrend.pine) |
| **TR-09** | [UT Bot Alerts (ATR Trailing Stop on Close)](strategies/01_Trend_Following_and_Momentum/README.md#tr-09--ut_bot_alerts_atr_trailing_stop_on_close) | `TR` | UT Bot · ATR трейлинг-стоп | [`tr-09_ut_bot_alerts_atr_trailing_stop_on_close.pine`](strategies/01_Trend_Following_and_Momentum/tr-09_ut_bot_alerts_atr_trailing_stop_on_close.pine) |
| **TR-10** | [Chandelier Exit](strategies/01_Trend_Following_and_Momentum/README.md#tr-10--chandelier_exit) | `TR` | 吊灯止损 · Chandelier-выход | [`tr-10_chandelier_exit.pine`](strategies/01_Trend_Following_and_Momentum/tr-10_chandelier_exit.pine) |
| **TR-11** | [Ichimoku Kinko Hyo](strategies/01_Trend_Following_and_Momentum/README.md#tr-11--ichimoku_kinko_hyo) | `TR` | 一目均衡表 · 一目均衡表 (Ишимоку) | [`tr-11_ichimoku_kinko_hyo.pine`](strategies/01_Trend_Following_and_Momentum/tr-11_ichimoku_kinko_hyo.pine) |
| **TR-12** | [Kaufman Adaptive Moving Average (KAMA)](strategies/01_Trend_Following_and_Momentum/README.md#tr-12--kaufman_adaptive_moving_average_kama) | `TR` | 卡玛自适应均线 · Адаптивная средняя Кауфмана | [`tr-12_kaufman_adaptive_moving_average_kama.pine`](strategies/01_Trend_Following_and_Momentum/tr-12_kaufman_adaptive_moving_average_kama.pine) |
| **TR-13** | [VIDYA (Variable Index Dynamic Average)](strategies/01_Trend_Following_and_Momentum/README.md#tr-13--vidya_variable_index_dynamic_average) | `TR` | VIDYA可变动指数平均 · VIDYA | 📖 Logic-only |
| **TR-14** | [FRAMA (Fractal Adaptive Moving Average)](strategies/01_Trend_Following_and_Momentum/README.md#tr-14--frama_fractal_adaptive_moving_average) | `TR` | 分形自适应均线 · FRAMA | 📖 Logic-only |
| **TR-15** | [Guppy Multiple Moving Averages (GMMA)](strategies/01_Trend_Following_and_Momentum/README.md#tr-15--guppy_multiple_moving_averages_gmma) | `TR` | 顾比复合移动平均线 · GMMA Ганна Гаппи | [`tr-15_guppy_multiple_moving_averages_gmma.pine`](strategies/01_Trend_Following_and_Momentum/tr-15_guppy_multiple_moving_averages_gmma.pine) |
| **TR-16** | [Heikin-Ashi Trend Flip](strategies/01_Trend_Following_and_Momentum/README.md#tr-16--heikin_ashi_trend_flip) | `TR` | 平均K线趋势翻转 · Торговля по Хейкин-Аши | [`tr-16_heikin_ashi_trend_flip.pine`](strategies/01_Trend_Following_and_Momentum/tr-16_heikin_ashi_trend_flip.pine) |
| **TR-17** | [Time-Series Momentum (TSMOM)](strategies/01_Trend_Following_and_Momentum/README.md#tr-17--time_series_momentum_tsmom) | `TR` | 时间序列动量 · Моментум по времени | 📖 Logic-only |
| **TR-18** | [CANSLIM Momentum / Leading-Stock Playbook](strategies/01_Trend_Following_and_Momentum/README.md#tr-18--canslim_momentum_leading_stock_playbook) | `TR` | 欧奈尔CANSLIM选股法 · CANSLIM | 📖 Logic-only |
| **VO-01** | [Volume Spread Analysis (VSA)](strategies/06_Volume_Order_Flow_and_Profile/README.md#vo-01--volume_spread_analysis_vsa) | `VO` | 量价分析法 · Объёмно-спредовый анализ (VSA) | 📖 Logic-only |
| **VO-02** | [On-Balance Volume Divergence](strategies/06_Volume_Order_Flow_and_Profile/README.md#vo-02--on_balance_volume_divergence) | `VO` | 能量潮背离 · Дивергенция OBV | [`vo-02_on_balance_volume_divergence.pine`](strategies/06_Volume_Order_Flow_and_Profile/vo-02_on_balance_volume_divergence.pine) |
| **VO-03** | [Chaikin Money Flow / Accumulation-Distribution Line](strategies/06_Volume_Order_Flow_and_Profile/README.md#vo-03--chaikin_money_flow_accumulation_distribution_line) | `VO` | 蔡金资金流 · Линия A/D и CMF | 📖 Logic-only |
| **VO-04** | [Money Flow Index](strategies/06_Volume_Order_Flow_and_Profile/README.md#vo-04--money_flow_index) | `VO` | 资金流量指数 · Индекс денежного потока | 📖 Logic-only |
| **VO-05** | [Volume Profile Nodes (HVN/LVN/POC)](strategies/06_Volume_Order_Flow_and_Profile/README.md#vo-05--volume_profile_nodes_hvnlvnpoc) | `VO` | 成交量分布节点 · Объёмный профиль (POC/HVN/LVN) | 📖 Logic-only |
| **VO-06** | [Market Profile TPO (Steidlmayer)](strategies/06_Volume_Order_Flow_and_Profile/README.md#vo-06--market_profile_tpo_steidlmayer) | `VO` | 市场轮廓TPO · Маркет-профиль (TPO) | 📖 Logic-only |
| **VO-07** | [VWAP Deviation Bands (Execution-Grade)](strategies/06_Volume_Order_Flow_and_Profile/README.md#vo-07--vwap_deviation_bands_execution_grade) | `VO` | VWAP偏差通道 · Полосы VWAP | [`vo-07_vwap_deviation_bands_execution_grade.pine`](strategies/06_Volume_Order_Flow_and_Profile/vo-07_vwap_deviation_bands_execution_grade.pine) |
| **VO-08** | [Anchored VWAP (AVWAP)](strategies/06_Volume_Order_Flow_and_Profile/README.md#vo-08--anchored_vwap_avwap) | `VO` | 锚定VWAP · Якорный VWAP | 📖 Logic-only |
| **VO-09** | [Cumulative Delta Divergence (CVD)](strategies/06_Volume_Order_Flow_and_Profile/README.md#vo-09--cumulative_delta_divergence_cvd) | `VO` | 累计成交量差背离 · Кумулятивная дельта (CVD) | 📖 Logic-only |
| **VO-10** | [Klinger Volume Oscillator](strategies/06_Volume_Order_Flow_and_Profile/README.md#vo-10--klinger_volume_oscillator) | `VO` | 克林格成交量振荡器 · Осциллятор Клингера | 📖 Logic-only |
| **VO-11** | [Ease of Movement](strategies/06_Volume_Order_Flow_and_Profile/README.md#vo-11--ease_of_movement) | `VO` | 简易波动指标 · Индекс лёгкости движения | 📖 Logic-only |
| **VO-12** | [Volume-Weighted Momentum Breakout](strategies/06_Volume_Order_Flow_and_Profile/README.md#vo-12--volume_weighted_momentum_breakout) | `VO` | 量价动量突破 · Объёмно-взвешенный пробой | 📖 Logic-only |

---

## 🔬 Methodology & Deduplication Pipeline
1. **Generative Core Extraction:** Published trading strategies suffer from massive community repackaging and renaming. This compendium collapses cosmetic variations into 189 canonical economic hypotheses.
2. **Four Strict Deduplication Gates:**
   - Identical entry/exit mechanics collapse into the earliest documented canonical source.
   - Pure parameter tweaks of existing mechanics are listed as variants, not separate strategies.
   - Regional ecosystems (China, Russia/CIS) retain distinct status only where market microstructure (e.g. T+1, price limits, MOEX clearing) imposes unique mechanical constraints.
   - Structural cross-family dependencies are maintained via explicit bi-directional handles.
3. **Pine Script v5 Standard:** All 43 code listings are clean, reproducible, self-contained Pine Script v5 reference implementations designed for execution benchmarking.

---

## 📦 Repository Structure
```
├── catalog.json                                # Complete structured database of all 189 strategies
├── docs/
│   └── Global_Trading_Strategy_Pine_Glossary.docx # Source manuscript compendium
├── strategies/
│   ├── 01_Trend_Following_and_Momentum/        # TR-01 to TR-18 + 12 .pine implementations
│   ├── 02_Mean_Reversion_and_Oscillators/      # MR-01 to MR-15 + 7 .pine implementations
│   ├── 03_Breakout_and_Volatility_Expansion/   # BK-01 to BK-13 + 3 .pine implementations
│   ├── 04_Price_Action_and_Smart_Money/        # PA-01 to PA-16 + 4 .pine implementations
│   ├── 05_Indicator_Hybrids_and_Cycles/        # IH-01 to IH-14 + 3 .pine implementations
│   ├── 06_Volume_Order_Flow_and_Profile/       # VO-01 to VO-12 + 2 .pine implementations
│   ├── 07_Session_Time_and_Calendar_Edges/     # SE-01 to SE-09 + 1 .pine implementation
│   ├── 08_Grid_Martingale_and_Averaging/       # GR-01 to GR-07 + 2 .pine implementations
│   ├── 09_China_Specific_A_Share_and_Futures/  # CN-01 to CN-26 + 4 .pine implementations
│   ├── 10_Russia_CIS_Specific_MOEX_Systems/    # RU-01 to RU-16 + 2 .pine implementations
│   ├── 11_Statistical_Factor_and_Arbitrage/    # ST-01 to ST-18 + 1 .pine implementation
│   ├── 12_Crypto_Native_Perpetual_and_DEX/     # CR-01 to CR-11 (Perp funding, DEX LP)
│   ├── 13_Machine_Learning_and_AI/             # ML-01 to ML-07 (Walk-forward, gates)
│   └── 14_Risk_Sizing_and_Execution/           # RX-01 to RX-07 + 2 .pine implementations
└── README.md                                   # Master Navigation and Taxonomy
```

---
Compiled for Institutional Systematic Research.