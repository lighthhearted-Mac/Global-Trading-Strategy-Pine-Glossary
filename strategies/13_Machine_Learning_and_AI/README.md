# Family ML: Machine Learning & AI Systems

**Total Strategies in Family:** 7  
**Pine Script v5 Implementations:** 0  

## Strategies Overview

| ID | Strategy Name | Alternative Names | Has Pine Code |
|---|---|---|:---:|
| **ML-01** | [Gradient-Boosted Factor Models (XGBoost/LightGBM Alpha)](#ml-01--gradient_boosted_factor_models_xgboostlightgbm_alpha) | 机器学习多因子选股 · XGBoost/LightGBM альфа | 📖 Logic-only |
| **ML-02** | [LSTM / Sequence Models for Direction](#ml-02--lstm_sequence_models_for_direction) | 长短期记忆网络方向预测 · LSTM-прогноз | 📖 Logic-only |
| **ML-03** | [Reinforcement Learning Portfolios (FinRL lineage)](#ml-03--reinforcement_learning_portfolios_finrl_lineage) | 强化学习组合管理 · RL-портфели | 📖 Logic-only |
| **ML-04** | [HMM Regime Switching](#ml-04--hmm_regime_switching) | 隐马尔可夫状态切换 · HMM-режимы | 📖 Logic-only |
| **ML-05** | [NLP Sentiment & News Trading](#ml-05--nlp_sentiment_news_trading) | 新闻情绪量化 · NLP-сентимент | 📖 Logic-only |
| **ML-06** | [Genetic Algorithms & Parameter Search](#ml-06--genetic_algorithms_parameter_search) | 遗传算法参数寻优 · Генетическая оптимизация | 📖 Logic-only |
| **ML-07** | [Walk-Forward, Deflated Sharpe & Overfitting Control](#ml-07--walk_forward_deflated_sharpe_overfitting_control) | 滚动前推与紧缩夏普 · Контроль переобучения | 📖 Logic-only |

---

### ML-01 · Gradient-Boosted Factor Models (XGBoost/LightGBM Alpha)
*机器学习多因子选股 · XGBoost/LightGBM альфа*

- **Origin & Lineage:** 华泰证券金工 '人工智能选股' series (2017+); JoinQuant/BigQuant template canon; Kaggle-era ubiquity.
- **Core Hypothesis:** Feed hundreds of factors into gradient-boosted trees to predict next-month relative returns, with purged walk-forward validation and industry neutralization; CN broker research published extensive public backtests making this the most-documented ML workflow in Chinese. Trees handle nonlinear factor interactions and missing data gracefully, which is why they beat linear IC-weighting in CN studies — when validation is honest.
- **Execution Rules:** Feature matrix = factor panel; label = forward returns; train with purged k-fold; trade top-decile predictions monthly; monitor feature importance drift.
- **Key Parameters:** Depth 3-6; learning rate 0.05-0.1; purge gap = label horizon; retrain quarterly.
- **Duplicates Eliminated:** CN-15 (the linear factor parent); ST-10 (expression-alphas as features); JoinQuant ML templates.

---

### ML-02 · LSTM / Sequence Models for Direction
*长短期记忆网络方向预测 · LSTM-прогноз*

- **Origin & Lineage:** Academic literature surge 2017-2020 (Fischer & Krauss LSTM on DAX, 2018, the canonical citation).
- **Core Hypothesis:** Sequence models ingest windows of returns/volumes and classify next-period direction; the canonical result shows in-sample promise and fast post-publication decay as the edge is regime-specific. Honest deployments treat the model as one ensemble vote with strict walk-forward and transaction-cost stress, not an oracle. The family's lesson is statistical: sequence overfitting is spectacular and easy.
- **Execution Rules:** Window 30-60 bars of normalized features; binary/ternary direction labels; purged walk-forward; ensemble with simpler signals; deploy at reduced size.
- **Key Parameters:** Hidden 32-128; dropout 0.2-0.5; retrain cadence; cost-adjusted threshold tuning.
- **Duplicates Eliminated:** ML-01 (tabular vs sequence); transformer-era successors (2021+).

---

### ML-03 · Reinforcement Learning Portfolios (FinRL lineage)
*强化学习组合管理 · RL-портфели*

- **Origin & Lineage:** FinRL (AI4Finance, 2020+) and the deep-RL trading literature (2018+).
- **Core Hypothesis:** An agent learns allocation/sizing policies against simulated environments with transaction costs, optimizing risk-adjusted objectives rather than supervised labels. Research results are mixed and environment design dominates outcomes: realistic fills, costs, and regime shifts decide whether learned policies generalize. Its lasting contribution is the environment library that forces honest simulation.
- **Execution Rules:** Define state (prices/positions), action space (weights), reward (Sharpe or CVaR-adjusted); train on regime-diverse data; paper-trade learned policies before capital.
- **Key Parameters:** PPO/SAC agents; cost model fidelity; out-of-distribution guards.
- **Duplicates Eliminated:** ML-01/02 (supervised relatives); execution-RL literature (child domain).

---

### ML-04 · HMM Regime Switching
*隐马尔可夫状态切换 · HMM-режимы*

- **Origin & Lineage:** Hamilton's regime-switching econometrics (1989); quant-blog standardization (2010s).
- **Core Hypothesis:** A hidden Markov model fits latent market states (bull/bear/chop) from return-volatility emissions; regime probabilities gate other strategies — enabling trend systems only in trending states, reversion in chop. It is the statistical formalization of 'the market changes character', and its biggest value is honest uncertainty: low-confidence regimes trigger de-risking rather than guessing.
- **Execution Rules:** Fit 2-4 state HMM on returns/vol; gate strategy family by state probability > threshold; de-risk in transition uncertainty.
- **Key Parameters:** States 2-4; emissions gaussian/t; retrain monthly; smoothing lag.
- **Duplicates Eliminated:** SE-08 (calendar regimes); TR-07 ADX gates (the indicator-flavored ancestor).

---

### ML-05 · NLP Sentiment & News Trading
*新闻情绪量化 · NLP-сентимент*

- **Origin & Lineage:** FinBERT lineage (2019+); CN snownlp-era sentiment factors; RU SMM-sentiment studies.
- **Core Hypothesis:** Score news/social text with domain-tuned language models and trade the sentiment-return relationship: announcement-day drift after strong sentiment, headline-momentum on novel information. Latency and event deduplication decide viability — much of the exploitable signal lives in the first seconds, which retail pipelines cannot reach; the slower tail (analyst reports, regulatory filings) is more accessible.
- **Execution Rules:** Ingest/score text; deduplicate events; trade drift windows (hours-days) on sentiment extremes with trend/liquidity gates.
- **Key Parameters:** Model domain-tuning; decay half-life of signal; event-window definitions.
- **Duplicates Eliminated:** CN-05 (sentiment regime cousin); ST-04 (momentum on information flow).

---

### ML-06 · Genetic Algorithms & Parameter Search
*遗传算法参数寻优 · Генетическая оптимизация*

- **Origin & Lineage:** 1990s EA-era practice (MT4 strategy tester 'genetic mode'); Adaptrade-style tools; RU/CN optimizer culture.
- **Core Hypothesis:** Evolutionary search over parameter spaces maximizes backtest fitness — powerful, and the single fastest way to overfit if fitness is raw P&L on one sample. Disciplined forms optimize on rolling windows with walk-forward scoring, penalty for parameter cliffs, and ensemble-over-parameters deployment. Documented as methodology rather than a strategy per se.
- **Execution Rules:** Encode parameters; evolve on training windows; score out-of-sample; select plateau regions (robust sets) not peaks; ensemble survivors.
- **Key Parameters:** Population/generations modest; fitness = walk-forward Sharpe with cost stress; plateau selection.
- **Duplicates Eliminated:** ML-07 (the evaluation discipline); RU «генетический оптимизатор» MT4 heritage.

---

### ML-07 · Walk-Forward, Deflated Sharpe & Overfitting Control
*滚动前推与紧缩夏普 · Контроль переобучения*

- **Origin & Lineage:** Robert Pardo (walk-forward, 1992); Bailey & López de Prado deflated Sharpe / probability of backtest overfitting (2014-2017).
- **Core Hypothesis:** The meta-strategy of the whole glossary: validate by rolling re-optimization out-of-sample, correct Sharpe for the number of trials attempted, and estimate the probability that the best-of-N backtest is luck. These tools — not any single entry signal — separate the surviving quant funds from the graveyard. Every entry above should be run through this discipline before capital.
- **Execution Rules:** Walk-forward with anchored/rolling windows; count all trials for deflated Sharpe; require PBO < threshold; prefer parameter plateaus.
- **Key Parameters:** Window ratios (train 4x test typical); trials ledger; Sharpe hurdle adjusted by N.
- **Duplicates Eliminated:** ML-06 (the search it disciplines); postcheck for every CN/RU platform strategy.

---
