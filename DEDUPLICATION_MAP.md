# Appendix A: Deduplication Map & Regional Lineage Dictionary

> This dictionary cross-references published renames, regional variants (China, Russia/CIS, MT4/MQL5), and retail clone indicators to their canonical generative trading strategy.

| Canonical ID | Canonical Strategy System | Collapsed Clones, Regional Renames & Variants Eliminated |
|:---:|---|---|
| **TR-01** | **Donchian Channel Breakout** | • Turtle S1/S2; CN 海龟策略 templates (JoinQuant, myquant.cn); RU «Пробой канала» robots; vn.py TurtleSignalStrategy. |
| **TR-02** | **Turtle Trading System (S1/S2)** | • 海龟交易法则 implementations on JoinQuant/BigQuant/vn.py (TurtleSignalStrategy); RU «Система Черепах» on Si/RTS futures; original Turtle Rules PDF archive. |
| **TR-03** | **Dual Moving Average Crossover (Golden Cross)** | • CN 双均线策略 (JoinQuant/myquant default demo, DoubleMaStrategy in vn.py); RU «Пересечение SMA 50/200»; MQL5 CodeBase MA-cross EAs. |
| **TR-04** | **Granville Eight Rules of Moving Averages** | • JoinQuant 双均线-格兰维交易 strategy; CN 移动平均线战法 variants; RU «Правила Гранвиля» tutorials (no separate robot). |
| **TR-05** | **MACD Trend and Histogram System** | • MACD+EMA combos in MQL5 CodeBase; CN MACD背离战法; vn.py MACD demo strategies. |
| **TR-06** | **Parabolic SAR Flip System** | • PSAR+EMA200+MACD signal packs (multiple GitHub repos); CN SAR跟踪策略; RU «Параболик» robots. |
| **TR-07** | **ADX/DMI Trend Filter System** | • ADX gates inside CN CTA templates (文华/TB); RU «ADX-фильтр» modules; generic MT4 ADX EAs. |
| **TR-08** | **SuperTrend** | • CN 超级趋势 (JoinQuant/文华); RU «Супертренд» TradingView scripts; countless 'ST + filter' hybrids on MQL5. |
| **TR-09** | **UT Bot Alerts (ATR Trailing Stop on Close)** | • Original 'ATR Trailing Stops' scripts (R	thomson bands, 2018); RU 'Универсальный трейлинг' packs; UT Bot + EMA 200 variants (QuantNomad). |
| **TR-10** | **Chandelier Exit** | • ATR Trailing Stops (Wilders-based); 'QQE trailing' variants; CN 吊灯止损 modules in CTA templates. |
| **TR-11** | **Ichimoku Kinko Hyo** | • CN 一目均衡表 strategy packs; RU Ишимоку school variants (see RU-10); MT4 Ichimoku EAs. |
| **TR-12** | **Kaufman Adaptive Moving Average (KAMA)** | • KAMA modules in CN CTA kits (文华/TB); RU «АМА Кауфмана» robots; KAMA+filter packs on MQL5. |
| **TR-13** | **VIDYA (Variable Index Dynamic Average)** | • VIDYA in MetaStock/AmiBroker libraries (the 1990s archive era); MT4 VIDYA indicators; RU VIDYA forks. |
| **TR-14** | **FRAMA (Fractal Adaptive Moving Average)** | • FRAMA ports in TASC Traders' Tips archive; MT4/MT5 FRAMA; CN 分形均线 experiments. |
| **TR-15** | **Guppy Multiple Moving Averages (GMMA)** | • CN 顾比均线 templates (通达信/同花顺 formulas); RU «Вееры Ганна/Гаппи» ribbon packs. |
| **TR-16** | **Heikin-Ashi Trend Flip** | • HA smoothing packs (every platform); CN Heikin-Ashi策略; RU «Хейкин Аши» scalping variants. |
| **TR-17** | **Time-Series Momentum (TSMOM)** | • Cross-sectional momentum (ST-04); CTA trend replication funds; CN 商品CTA趋势 replication research. |
| **TR-18** | **CANSLIM Momentum / Leading-Stock Playbook** | • IBD-style screeners; CN 龙头战法 (structurally similar); RU «рост на лидерах» screeners. |
| **MR-01** | **Connors RSI(2) Pullback** | • RSI(3)/RSI(4) variants; CN 短线超卖反弹 templates; RU 'RSI отскок' MT4 robots. |
| **MR-02** | **Bollinger Band Reversion (%B Fade)** | • CN 布林带下轨抄底 (ETF/股票); RU «торговля от границ Боллинджера»; Bollinger %B factor research. |
| **MR-03** | **Double 7s / 3-Day High-Low Pullback** | • 3-Day High/Low; 'TFSE' Connors variants; CN 七日新低反弹 scripts. |
| **MR-04** | **Keltner Channel Pullback** | • vn.py KingKeltnerStrategy (breakout form, cross-ref BK-13); CN 肯特纳通道 scripts; RU каналы Кельтнера. |
| **MR-05** | **TTM Squeeze / Squeeze Momentum** | • Squeeze Momentum Indicator [LazyBear]; Squeeze Pro (LuxAlgo, cross-ref BK-11); CN 布林收口战法; RU «сжатие волатильности» scripts. |
| **MR-06** | **QQE (Qualitative Quantitative Estimation)** | • QQE MOD (Glaz, Mihkel00 ports); RU QQE-форекс советники; CN QQE+MACD hybrids. |
| **MR-07** | **WaveTrend Oscillator** | • WaveTrend [WT] (LazyBear); SJ WaveTrend and dozens of forks; CN WT+VWAP scalping dashboards; RU WaveTrend forks on MQL5. |
| **MR-08** | **Fisher Transform Reversal** | • Fisher in Ehlers' book suite (Cybernetic Analysis, 2002); MT4/MT5 Fisher; CN 费雪指标 scripts. |
| **MR-09** | **RSI Regular Divergence System** | • Hidden divergence variants; CN MACD/RSI背离战法; RU 'дивергенция' robots on MQL5. |
| **MR-10** | **Stochastic Oversold System** | • RU «Стохастик + RSI» комбо-роботы; CN KDJ战法 (the CN KDJ is a stochastic variant); MT4 stochastic packs. |
| **MR-11** | **Pivot Point Reversion** | • CN 分时均线/枢轴 strategies; RU 'пивот-уровни' robots; every MT4 pivot indicator pack. |
| **MR-12** | **Intraday VWAP Mean Reversion** | • CN 分时VWAP回归; RU «откат к VWAP» скрипты; every VWAP-bands pack on TradingView. |
| **MR-13** | **Z-Score Spread Reversion** | • RU «Z-score роботы»; CN 标准化偏离策略; Pairs-trading single-leg approximations. |
| **MR-14** | **Williams %R Fade** | • RU %R-роботы; CN 威廉指标战法; bundled in every platform's default indicator set. |
| **MR-15** | **Money-Flow Reversion (CMF/MFI)** | • CN 资金流指标策略; RU «денежный поток» индикаторные системы; OBV-family hybrids (cross VO-02). |
| **BK-01** | **Opening Range Breakout (ORB)** | • CN 开盘区间突破 (股票/股指); RU «Пробой открытия» intraday robots; ICT opening-range variants (cross PA-09). |
| **BK-02** | **Narrow Range 7 / Inside Day Patterns** | • CN 窄幅整理突破; RU 'узкий диапазон' scripts; ID/NR4 variants. |
| **BK-03** | **Volatility Contraction Pattern (VCP)** | • Minervini scan packs; Qullamägi EP/gap momentum (cousin); CN 强势股缩量整理突破. |
| **BK-04** | **Darvas Box** | • CN 箱体突破; RU «Метод Дарваса»; box-drawing scripts across all platforms. |
| **BK-05** | **Bill Williams Alligator + Fractals** | • RU «Аллигатор Вильямса» robots (enormous MQL4/5 corpus); CN 鳄鱼线战法; Awesome/AC oscillator combos (BK-06). |
| **BK-06** | **Awesome Oscillator / Accelerator System** | • RU «Система Билла Вильямса» full-suite robots; CN AO/AC战法; MACD-equivalent logic (cross TR-05). |
| **BK-07** | **Aroon Breakout** | • Aroon cross robots on MQL5; CN 阿隆指标 templates. |
| **BK-08** | **Range Breakout with Volume Surge (放量突破)** | • BK-09 consolidation breakout; RU «пробой с объёмом»; OBV/CMF breakout hybrids. |
| **BK-09** | **Consolidation Box Breakout** | • CN 平台突破/整理突破; RU «пробой консолидации»; Darvas and NR7 (same mechanism). |
| **BK-10** | **Gap Playbook (Fade / Continue)** | • CN 缺口回补策略; RU гэп-роботы; ORB gap variants (cross BK-01). |
| **BK-11** | **Squeeze Pro / Multi-Threshold Squeeze** | • TTM Squeeze (MR-05) as the parent; LazyBear Hi-Lo squeezes; CN 多档收口实验性 scripts. |
| **BK-12** | **High-of-Day Break & Retest** | • CN 日内新高策略; RU intraday HOD scripts; IB opening-drive variants. |
| **BK-13** | **Volatility Expansion Breakout (Keltner/ATR form)** | • vn.py KingKeltnerStrategy; CN 肯特纳突破 CTA templates; RU канальные пробойные роботы. |
| **PA-01** | **Wyckoff Accumulation/Distribution & Spring (V-Hook)** | • Wyckoff [theUltimator5] schematic indicator; CN 威科夫吸筹 materials; RU Вайкофф course translations; Linda Raschke's Turtle Soup (PA-10) is the fade-cousin; this workspace's V-Hook agent is a direct implementation. |
| **PA-02** | **Effort vs Result / Composite Operator Reading** | • VSA (VO-01) is the formalized descendant; CN 量价背离 reading; RU «усилие-результат» school. |
| **PA-03** | **Pin Bar / Hammer Rejection** | • RU «пинбар» schools (every RU PA course); CN 长下影/锤子线战法; hammer/shooting-star mechanical scripts. |
| **PA-04** | **Engulfing & Inside-Bar Momentum Patterns** | • MT4 engulfing EAs; CN 阳包阴战法; RU «поглощение» robots. |
| **PA-05** | **Al Brooks Bar-by-Bar Price Action** | • Brooks-method scan scripts; RU «бар-за баром» translations; second-entry fan implementations. |
| **PA-06** | **Fakey / False-Breakout Inside-Bar** | • Turtle Soup (PA-10); stop-run/'spoofy' scripts; RU «ложный пробой» scripts. |
| **PA-07** | **Supply & Demand Zones (Set-and-Forget)** | • Order block overlaps (PA-08); CN 供需区域 scripts; RU «зоны спроса/предложения» packs. |
| **PA-08** | **Smart Money Concepts (BOS / CHoCH / Order Blocks / FVG)** | • LuxAlgo SMC [ML] and dozens of forks; ICT order-block scripts; CN 主力结构 (SMART概念) scripts; RU SMC переводы — the framework is one concept despite hundreds of branded scripts. |
| **PA-09** | **ICT Kill Zones, Silver Bullet & Time-Based Liquidity** | • ICT concepts scripts (dozens); PA-08 SMC (shared vocabulary); SE-01 Asia-range sweep (shared mechanism). |
| **PA-10** | **Turtle Soup / Fake Breakout Fade** | • Fakey (PA-06); 'stop hunt fade' scripts; CN 假突破反打. |
| **PA-11** | **Harmonic Patterns (Gartley / Bat / Butterfly / AB=CD)** | • Pesavento vs Carney naming disputes (same patterns); RU «Гартли/летучая мышь» packs; CN 谐波形态 scripts. |
| **PA-12** | **Elliott Wave (Mechanized Approaches)** | • RU Эллиотт-школы (large following); CN 波浪理论 automated drafts; every 'EW auto-count' indicator. |
| **PA-13** | **Wolfe Waves** | • Wolfe Wave scripts on MQL5/TradingView; RU «волны Вольфа» robots. |
| **PA-14** | **Classical Reversal Patterns Automated (Double Top, H&S)** | • CN 双头双底/头肩顶 scripts; RU «голова-плечи» роботы; every platform's built-in pattern detection. |
| **PA-15** | **Trendline & Channel Break Automation** | • RU «пробой трендовой» роботы; CN 趋势线突破 scripts; linreg channel packs. |
| **PA-16** | **Round Numbers / Psychological Levels** | • CN 整数关口战法; RU «круглые цифры» robots; FX 'big figure' trading. |
| **IH-01** | **MESA Adaptive MA (MAMA / FAMA)** | • MAMA/FAMA ports (TradeStation->MT4->Pine); CN 自适应均线 experiments. |
| **IH-02** | **Instantaneous Trendline & Sine Wave** | • Ehlers book-code ports; MT4/MT5 Hilbert suites. |
| **IH-03** | **Cyber Cycle** | • Ports in the Ehlers TASC archive; CN 循环指标 experiments. |
| **IH-04** | **Ehlers SuperSmoother / Roofing Filter** | • SuperSmoother ports everywhere; CN 超平滑滤波 scripts. |
| **IH-05** | **Vortex Indicator** | • Vortex packs on all platforms; CN 涡流指标; RU Вортекс robots. |
| **IH-06** | **True Strength Index (TSI)** | • TSI packs everywhere; CN TSI策略; RU TSI форекс-роботы. |
| **IH-07** | **Schaff Trend Cycle** | • STC ports across MT4/MT5/Pine; CN STC experiments. |
| **IH-08** | **Connors RSI (Composite)** | • CRSI packs; CN 复合RSI; RU CRSI-роботы. |
| **IH-09** | **Stochastic RSI** | • Everywhere; CN KDJ-of-RSI variants; RU stochRSI скальпинг packs. |
| **IH-10** | **Commodity Channel Index Systems** | • CN CCI战法; RU CCI-советники; Woodie CCI variant (distinct calc, same idea). |
| **IH-11** | **Chande Momentum Oscillator** | • CMO in MetaStock-era libraries; CN CMO模板. |
| **IH-12** | **Ultimate Oscillator** | • UO packs; CN 终极指标; RU UO-роботы. |
| **IH-13** | **Long-Cycle Momentum Composites (KST / Coppock)** | • Coppock screeners; RU «кривая Коппока» long-term followers. |
| **IH-14** | **Detrended Price Oscillator & Cycle Projection** | • Bressert cycle tools; CN DPO周期模板; RU цикловый анализ. |
| **VO-01** | **Volume Spread Analysis (VSA)** | • VSA scripts (dozens of packs); CN 量价分析 school; RU VSA-сообщество (Smart-Lab's volume tradition); Wyckoff bar-reading (PA-02). |
| **VO-02** | **On-Balance Volume Divergence** | • OBV in every platform; CN 能量潮战法; RU OBV-роботы; CMF/ADL cousins (MR-15). |
| **VO-03** | **Chaikin Money Flow / Accumulation-Distribution Line** | • ADL/CMF packs; CN CMF资金流策略; RU CMF-роботы. |
| **VO-04** | **Money Flow Index** | • MFI everywhere; CN MFI资金策略; RU MFI-скрипты. |
| **VO-05** | **Volume Profile Nodes (HVN/LVN/POC)** | • Volume profile packs (LuxAlgo, multiple); CN 成交量分布策略; RU объёмный профиль community. |
| **VO-06** | **Market Profile TPO (Steidlmayer)** | • TPO chart packs; RU аукционная теория followers; CN 市场轮廓 study groups. |
| **VO-07** | **VWAP Deviation Bands (Execution-Grade)** | • VWAP band packs; CN VWAP通道; RU VWAP-стратегии; anchored-VWAP variants (VO-08). |
| **VO-08** | **Anchored VWAP (AVWAP)** | • AVWAP packs (Shannon-affiliated and clones); CN 锚定VWAP; RU якорный VWAP. |
| **VO-09** | **Cumulative Delta Divergence (CVD)** | • CVD packs; CN 订单流/德尔塔 scripts; RU дельта-анализ (footprint communities). |
| **VO-10** | **Klinger Volume Oscillator** | • KVO packs; CN KVO指标; RU Klinger robots. |
| **VO-11** | **Ease of Movement** | • EMV in classic libraries; CN EMV模板. |
| **VO-12** | **Volume-Weighted Momentum Breakout** | • BK-08; VO-02/03 combos; RU «пробой с потоком» scripts. |
| **SE-01** | **Asia Range Sweep & London Reversal** | • ICT Judas swing (PA-09); RU «съём лоув/хай Азии» scripts; CN 亚盘区间策略. |
| **SE-02** | **London Breakout («Лондонский взрыв»)** | • RU «Пробой утреннего флэта» (RU-09, same mechanism on MOEX hours); CN 伦敦突破; every MT4 London-bot. |
| **SE-03** | **NY Open Momentum (10:00 Rule)** | • IB/ORB variants (BK-01); CN 美股开盘策略; RU «Нью-Йорк открытие» bots. |
| **SE-04** | **Overnight vs Intraday Edge (Tug of War)** | • Buy-the-close-sell-the-open papers; CN 隔夜效应研究; RU овернайт-стратегии on SPB panel. |
| **SE-05** | **Turn-of-Month / Turn-of-Quarter Effect** | • TOQ/TOY variants; CN 月末效应研究; RU месячные окна стратегии. |
| **SE-06** | **Sell in May / Halloween Indicator** | • Seasonal rotation ETF strategies; CN 五穷六绝七翻身 folklore systematized; RU сезонность studies. |
| **SE-07** | **Pre-FOMC Announcement Drift** | • ECB/pre-announcement drift follow-up studies; CN 美联储会议策略; RU пред-FOMC стратегии. |
| **SE-08** | **Hour-of-Day Volatility Breakout** | • Session-filter modules in CN/RU robots; ICT kill zones (PA-09) overlap. |
| **SE-09** | **Crypto Weekend & Funding Window Effects** | • Funding-window bots; CN 周末行情策略; RU крипто-сезонность notes. |
| **GR-01** | **Classic Spot Grid Bot** | • CN 网格交易 (myquant/JoinQuant templates, E大网格体系); RU «сеточные роботы» (Binance/Bybit RU marketplaces); every Pionex/3Commas preset. |
| **GR-02** | **Martingale / Averaging-Down Systems** | • Ilan 1.6/2.0 & Apocalypse (RU-02); CN 马丁/扛单 systems; every 'recovery zone' EA on MQL5 market. |
| **GR-03** | **Anti-Martingale Pyramiding** | • Turtle pyramiding (TR-02); trend-add modules in CN CTA kits; RU «доливка по тренду» practice. |
| **GR-04** | **DCA & Smart DCA Bots** | • CN 基金定投+止盈体系; RU T-Bank auto-invest strategies; 3Commas DCA presets. |
| **GR-05** | **Fibonacci Grid** | • RU «сетка по Фибо» robots; CN 斐波那契网格 experiments; MT4 Fibo-grid EAs. |
| **GR-06** | **ATR-Adaptive Grid** | • Volatility-grid presets in bot marketplaces; CN 自适应网格研究; RU адаптивные сетки. |
| **GR-07** | **Portfolio Rebalancing Bot** | • Shannon's demon writeups; BitUniverse battles; CN 定投再平衡 hybrids; RU ребалансировка боты. |
| **CN-01** | **Chan Theory (缠论): Fractals, Pens, Pivots & Three Buy/Sell Points** | • czsc (waditu/czsc — 200+ signal functions, Rust core); chanlun-pro (gaoxiaojun) with JoinQuant/Broker adapters; 缠论 indicator packs on 通达信; no western equivalent (pivot-breakout SMC is a loose cousin). |
| **CN-02** | **Limit-Up Board Tactics (打板：首板/连板/接力)** | • Every A-share 打板 screener (同花顺/通达信 formulas); BigQuant limit-up factors; not replicable on unlimited markets (the limit IS the edge). |
| **CN-03** | **Limit-Up Pullback Re-entry (涨停回马枪)** | • 回踩战法 variants; 强势股回调买入 templates; TDX 回马枪 formulas (same pattern). |
| **CN-04** | **Dragon-Head Leading-Stock Tactics (龙头战法)** | • CANSLIM (TR-18) structural cousin; CN 主升浪战法; 打板 (CN-02) entry mechanics. |
| **CN-05** | **Sentiment Cycle Model (情绪周期)** | • 连板高度 monitoring dashboards; BigQuant sentiment factors; no direct western analog (closest: breadth-thrust regime models). |
| **CN-06** | **Chip Distribution (筹码分布 / CYQ)** | • CYQ/SCR indicator clones; 筹码峰 formulas in TDX; volume-profile (VO-05) is the western statistical cousin. |
| **CN-07** | **Dragon-Tiger List Following (龙虎榜跟随)** | • 席位跟踪 dashboards (问财/开盘啦); not portable without disclosure data. |
| **CN-08** | **Northbound Capital Following (北向资金跟随)** | • 北向资金实时 tracking tools (pre-2024); 外资流入 strategies on JoinQuant/BigQuant. |
| **CN-09** | **Margin Balance Sentiment (融资融券情绪)** | • 两融数据 factor studies (华泰金工 reports); platform sentiment factors. |
| **CN-10** | **Double-Low Convertible Bonds (双低可转债)** | • 集思录轮动 dashboards; 双低 variants (低价/低溢价 separable); CB wheel strategies. |
| **CN-11** | **Large/Small-Cap Rotation (大小盘轮动)** | • 行业轮动 (CN-12) at sector scale; global size-factor rotation (ST-04/05). |
| **CN-12** | **Sector Rotation (行业轮动)** | • ST-04 cross-sectional momentum (same mechanism); US sector-rotation literature. |
| **CN-13** | **Index Enhancement (指数增强)** | • ST-08/09 factor overlays; global 'index-plus' products. |
| **CN-14** | **Alpha Strategy with Index-Futures Hedge (阿尔法策略)** | • ST statistical arb at index level; global 130/30 and market-neutral funds. |
| **CN-15** | **Multi-Factor Stock Selection (多因子选股)** | • ST-04..ST-11 factor entries (the global canon of the same idea); WorldQuant 101 Alphas (ST-10). |
| **CN-16** | **MA Convergence Breakout (均线粘合突破)** | • BK-09 box breakout (same coiling mechanism); CN 平台突破 with MA flavor. |
| **CN-17** | **N-Structure Tactics (N字战法)** | • PA-05 Brooks H1/H2; flag patterns; 缠论笔结构 (CN-01) at coarser granularity. |
| **CN-18** | **Rising Pullback System (上升回档)** | • MR-04 Keltner pullback; CN 波段王 (CN-20) overlap. |
| **CN-19** | **Main-Force Accumulation Tracking (主力吸筹跟踪)** | • PA-01/PA-02 Wyckoff; VO-03 CMF accumulation reads; CN-06 chip distribution confirmation. |
| **CN-20** | **Swing Band System (波段操作 / 波段王)** | • MR-04/BK-13 Keltner forms; CN-18 rising pullback (same anatomy). |
| **CN-21** | **Intraday T+0 Around Base Position (底仓做T)** | • VO-07/SE-08 intraday shells; CN-13 enhancement module. |
| **CN-22** | **Call-Auction & Tail-Session Tactics (集合竞价/尾盘战法)** | • SE-03 open-momentum logic; CN-02 continuation boards. |
| **CN-23** | **Calendar Spread Arbitrage (跨期套利)** | • ST-01/02 stat-arb machinery; CN-24/25 sibling arb forms. |
| **CN-24** | **Cross-Commodity Spreads (跨品种套利)** | • ST-01 pairs (statistical form); RU Brent-Urals (RU-12) — same construct, different commodities. |
| **CN-25** | **Futures-Cash Basis Arbitrage (期现套利)** | • ST-16 roll yield (related mechanics); global index-arb literature. |
| **CN-26** | **Valuation-Band Rotation (估值分位轮动)** | • CN-11 rotation (momentum flavor); global value-timing research; GR-04 smart DCA anchors. |
| **RU-01** | **Elder's Triple Screen** | • Countless RU/EN course versions; HTF-filter trend-pullback hybrids globally; SafeZone stops are Elder's exit companion (RU-04). |
| **RU-02** | **Ilan Family (RSI + CCI Martingale Advisors)** | • GR-02 martingale (the mechanism); 'Apocalypse' and every Ilan fork; CN 扛单 systems (same geometry). |
| **RU-03** | **Sniper Method («Снайпер», Дмитриев / Байнов)** | • PA-07 supply/demand zones; «Мясо» (parent system); RU Sniper X derivatives. |
| **RU-04** | **Elder SafeZone Stops & Elder Ray** | • Chandelier exit (TR-10) — same adaptive-stop family; ATR-trail systems. |
| **RU-05** | **Order-Book (Стакан) Scalping on MOEX Futures** | • VO-09 CVD (Pine proxy of the same information); HFT spoofing-detection literature. |
| **RU-06** | **Synthetic Bond Arbitrage («SyntheticBondsArbitrage»)** | • ST-16 roll-yield; CR-02 cash-and-carry; RU-12 spread family. |
| **RU-07** | **Dividend-Gap Trading (Дивидендный гэп)** | • BK-10 gap playbook (general form); CN 分红除权 practices (structurally similar, different regime). |
| **RU-08** | **Pairs Trading on MOEX Equities** | • ST-01/ST-03 (the general mechanism); CN-24 cross-commodity analog. |
| **RU-09** | **Morning Flat Breakout («Пробой утреннего флэта»)** | • SE-02 London breakout (same mechanism); BK-01 ORB (session-open family). |
| **RU-10** | **Russian Ichimoku Schools (Ишимоку-школы)** | • TR-11 Ichimoku (the parent); RU/UA course forks. |
| **RU-11** | **Automated Fibonacci Level Robots** | • GR-05 Fibonacci grid (the averaging form); RU-03 Sniper (level-logic cousin). |
| **RU-12** | **Brent-Urals & Calendar Spread Trading (TSLab)** | • CN-24 cross-commodity spreads; ST-01/02 stat-arb; RU-06 synthetic bonds (rate-spread cousin). |
| **RU-13** | **Book + Tape Hybrid (Стакан + Лента) Automation** | • RU-05 (manual form); VO-09 (Pine proxy); HFT microstructure literature. |
| **RU-14** | **Smart-Lab Community Trend Robots (Si/RTS)** | • TR-01/TR-02 (mechanism parents); RU-09 (session variant). |
| **RU-15** | **T-Bank Community Auto-Strategies (Tinkoff API era)** | • GR-04 DCA; GR-07 rebalancing (mechanisms); RU-07 dividend calendar integration. |
| **RU-16** | **Academic Quant Lineage (ВШЭ / МФТИ factor studies)** | • ST-04..ST-11 (the global canon it replicates); CN-15 (the CN counterpart lineage). |
| **ST-01** | **Pairs Trading (Distance Method)** | • RU-08 MOEX pairs; CN-24 commodity spreads; RU «парный трейдинг» community (mechanism identical). |
| **ST-02** | **Statistical Arbitrage (Avellaneda-Lee)** | • ST-01 (simplified ancestor); institutional stat-desk literature. |
| **ST-03** | **Kalman-Filter Hedge Ratio (Dynamic Pairs)** | • ST-01/02 implementations; RU Kalman-пары threads. |
| **ST-04** | **Cross-Sectional Momentum (Jegadeesh-Titman)** | • CN-12/CN-15 (CN implementations); TR-17 TSMOM (time-series form); RU-16 (MOEX replication). |
| **ST-05** | **Value Factor (HML) & Value-Momentum Combination** | • CN-26 (valuation timing); ST-09 quality-value hybrids; global smart-beta products. |
| **ST-06** | **FX Carry Trade** | • CR-01 crypto funding carry (the perp analog); ST-16 commodity carry. |
| **ST-07** | **Low-Volatility Anomaly** | • ST-08 BAB (leverage-neutrality framing); min-variance portfolios; RU-16 replication. |
| **ST-08** | **Betting Against Beta (BAB)** | • ST-07 (the unlevered view); global smart-beta funds. |
| **ST-09** | **Quality / Profitability Factor (QMJ)** | • ST-05 (value pairing); Piotroski F-Score screens (cousin); CN-15 factor suite. |
| **ST-10** | **WorldQuant 101 Formulaic Alphas** | • CN-15 (the CN platform implementations); BRAIN community alphas; DolphinDB 101-alpha ports. |
| **ST-11** | **The Factor Zoo & Multiple-Testing Corrections** | • ST-04..10 (the zoo's residents); CN-15/RU-16 (regional replications). |
| **ST-12** | **COT Positioning Strategies** | • Positioning analytics vendors; RU «отчёты COT» study groups; crypto COT-era analogs (BTC futures). |
| **ST-13** | **Dispersion Trading (Index vs Constituents)** | • VRP (ST-14) at index level; dispersion desks' literature. |
| **ST-14** | **Volatility Risk Premium Harvesting** | • ST-13 (correlation cousin); SE-07 (event-calendar de-risking). |
| **ST-15** | **Gamma Scalping (Long-Gamma Rebalancing)** | • ST-14 (the short side); dealer-flow research notes. |
| **ST-16** | **Commodity Roll Yield / Contango Harvest** | • ST-06 carry; RU-06 synthetic bonds (financing-rate analog); CN-25 basis arb. |
| **ST-17** | **Risk Parity & Volatility Targeting** | • ST-07/08 (risk-based tilts); GR-07 rebalancing (the retail cousin). |
| **ST-18** | **Commodity Seasonality** | • SE-05/06 (equity seasonality); RU grain-market seasonal notes; CN 农产品季节性 studies. |
| **CR-01** | **Funding-Rate Arbitrage (Delta-Neutral Carry)** | • ST-06 carry (the general form); CR-02 (dated-futures version). |
| **CR-02** | **Cash-and-Carry / Futures Basis Trade** | • CR-01 (perp version); ST-16 (commodity roll analog); CN-25 (CN index-futures version). |
| **CR-03** | **Liquidation-Cascade Fade** | • PA-01 spring (mechanism); VO-09 delta flush (informational cousin). |
| **CR-04** | **Open-Interest Regime Model (OI + Price Matrix)** | • VO-12 volume-confirmed breakout (tradfi analog); CR-03 (event special case). |
| **CR-05** | **On-Chain Whale & Flow Following** | • CN-07/08 (flow-copy logic in tradfi clothes); VO order-flow family. |
| **CR-06** | **BTC Dominance / Altcoin Rotation** | • CN-11 cap rotation (tradfi analog); TR-17 momentum machinery. |
| **CR-07** | **Crypto Volatility Breakout (Donchian + Funding Filter)** | • TR-01/TR-02 (parents); SE-09 (session overlays); RU/CN crypto-bot presets. |
| **CR-08** | **Triangular Arbitrage** | • CR-11 (cross-venue variant); RU-13 (latency-bound scalping lessons). |
| **CR-09** | **DeFi Concentrated Liquidity Market-Making** | • GR-01 grid (the AMM is a grid at heart); VO order-flow family (inventory logic). |
| **CR-10** | **MEV Extraction (Sandwich / Backrun) — Documented, Not Endorsed** | • CR-08 (latency family); regulatory grey-zone literature. |
| **CR-11** | **Cross-Exchange Latency Arbitrage** | • CR-08 (same-latency family); CN-era '搬砖' (brick-moving) practice — the CN name for exactly this trade. |
| **ML-01** | **Gradient-Boosted Factor Models (XGBoost/LightGBM Alpha)** | • CN-15 (the linear factor parent); ST-10 (expression-alphas as features); JoinQuant ML templates. |
| **ML-02** | **LSTM / Sequence Models for Direction** | • ML-01 (tabular vs sequence); transformer-era successors (2021+). |
| **ML-03** | **Reinforcement Learning Portfolios (FinRL lineage)** | • ML-01/02 (supervised relatives); execution-RL literature (child domain). |
| **ML-04** | **HMM Regime Switching** | • SE-08 (calendar regimes); TR-07 ADX gates (the indicator-flavored ancestor). |
| **ML-05** | **NLP Sentiment & News Trading** | • CN-05 (sentiment regime cousin); ST-04 (momentum on information flow). |
| **ML-06** | **Genetic Algorithms & Parameter Search** | • ML-07 (the evaluation discipline); RU «генетический оптимизатор» MT4 heritage. |
| **ML-07** | **Walk-Forward, Deflated Sharpe & Overfitting Control** | • ML-06 (the search it disciplines); postcheck for every CN/RU platform strategy. |
| **RX-01** | **Fixed Fractional / Percent-Risk Sizing** | • TR-02 Turtle units (the volatility-normalized ancestor); every platform's default sizing. |
| **RX-02** | **Kelly & Half-Kelly Criterion** | • RX-01 (the practical constrained form); prop-firm sizing policies. |
| **RX-03** | **Volatility-Targeted Sizing (ATR Units)** | • TR-02/TR-17 (the parents); ST-17 (portfolio level). |
| **RX-04** | **Portfolio Heat & Correlation Limits** | • RX-01/03 (per-trade forms); ST-17 (allocation form). |
| **RX-05** | **Breakeven Ratchet & Scale-Out Exits** | • TR-10 trailing stops (the pure trail); GR-03 pyramids' exit side. |
| **RX-06** | **Time Stops & Opportunity-Cost Exits** | • CN-02 board time-stop; BK-01 session-flat rule (time stop by clock). |
| **RX-07** | **Execution Algorithms (TWAP / VWAP / POV) & Slippage Budgets** | • VO-07/08 (VWAP as signal — same benchmark, different job); RU-13/CR-08 (latency-bound execution domains). |