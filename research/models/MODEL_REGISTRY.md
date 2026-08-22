# OXYCOK Commerce — Model Research Registry

> Registry of external machine-learning architectures evaluated for possible use inside OXYCOK Commerce.

---

# 1. Core Rule

External models are research candidates.

They do not become production architecture merely because:

- they are widely cited;
- they were deployed by Alibaba, Tencent, JD, Google, or another major company;
- they outperform a benchmark;
- source code exists;
- an AI agent recommends them.

Required progression:

RESEARCH SOURCE
    ↓
IDENTITY VERIFIED
    ↓
MODEL UNDERSTOOD
    ↓
DATA REQUIREMENTS UNDERSTOOD
    ↓
BASELINE REPRODUCTION
    ↓
OXYCOK FIT ASSESSMENT
    ↓
LOCAL EXPERIMENT
    ↓
QUALIFICATION
    ↓
PRODUCTION CANDIDATE

---

# 2. Model Status Vocabulary

Use:

DISCOVERED

IDENTITY_VERIFIED

FORMULA_VERIFIED

REFERENCE_CODE_AVAILABLE

REPRODUCED

LOCAL_BASELINE_TESTED

LOCAL_VALUE_SUPPORTED

QUALIFIED

REJECTED

RETIRED

A model may stop at any state.

---

# 3. MODEL-LIGHTGCN-001

Name:

LightGCN: Simplifying and Powering Graph Convolution Network for Recommendation

Publication:

SIGIR 2020

Authors:

- Xiangnan He
- Kuan Deng
- Xiang Wang
- Yan Li
- Yongdong Zhang
- Meng Wang

DOI:

10.1145/3397271.3401063

Status:

IDENTITY_VERIFIED

Domain:

Collaborative filtering / recommendation

Primary idea:

Represent users and items as a bipartite interaction graph and propagate embeddings through neighborhood aggregation.

LightGCN deliberately removes feature transformation and nonlinear activation from conventional graph convolution used for collaborative filtering.

Conceptual propagation:

e_u^(k+1)
=
sum over i in N(u)
[
1 / sqrt(|N(u)| |N(i)|)
]
e_i^(k)

Final embedding:

e_u
=
sum from k=0 to K
alpha_k e_u^(k)

The original implementation commonly uses uniform layer weights:

alpha_k = 1 / (K + 1)

Typical objective:

Bayesian Personalized Ranking (BPR)

Research relevance:

HIGH

Potential OXYCOK use:

- personalized recommendation;
- product ranking;
- collaborative product discovery;
- cross-sell candidate generation.

Requirements:

- sufficient user-item interactions;
- stable user identity;
- stable item identity;
- meaningful implicit feedback;
- appropriate train/test temporal split.

Major limitations:

- cold-start users;
- cold-start products;
- sparse first-party data;
- interaction popularity bias;
- offline ranking performance may not equal business lift.

Production authority:

NONE

Current next step:

Do not implement before simpler recommendation baselines exist.

Required local baseline comparisons:

- most popular;
- trending;
- co-purchase;
- recently viewed;
- category affinity;
- matrix factorization.

---

# 4. MODEL-NGCF-001

Name:

Neural Graph Collaborative Filtering

Publication:

SIGIR 2019

Authors:

- Xiang Wang
- Xiangnan He
- Meng Wang
- Fuli Feng
- Tat-Seng Chua

DOI:

10.1145/3331184.3331267

Status:

IDENTITY_VERIFIED

Domain:

Graph collaborative filtering

Primary idea:

Encode high-order collaborative signals by propagating embeddings across a user-item bipartite graph.

Historical importance:

NGCF is an important predecessor to LightGCN.

Research relevance:

MEDIUM-HIGH

Potential OXYCOK use:

Primarily as:

- benchmark;
- architectural reference;
- historical comparison.

Important finding:

LightGCN research suggests that several neural operations used by NGCF are unnecessary or detrimental for collaborative filtering under tested conditions.

Production authority:

NONE

Current disposition:

BENCHMARK_CANDIDATE

---

# 5. MODEL-DIN-001

Name:

Deep Interest Network for Click-Through Rate Prediction

Publication:

KDD 2018

Organization:

Alibaba

Status:

IDENTITY_VERIFIED

Domain:

CTR prediction / behavioral recommendation

Primary idea:

A user's historical behavior should not be compressed into one fixed representation independent of the candidate item.

DIN uses a local activation mechanism so different candidate items activate different parts of a user's behavioral history.

Potential OXYCOK use:

- personalized ranking;
- recommendation reranking;
- marketing candidate ranking;
- predicted click probability.

Data requirements:

- user behavior sequence;
- item identity/features;
- candidate item;
- click/non-click labels;
- sufficiently large impression history.

Risk:

Our Shopify store may initially have nowhere near the traffic volume required to justify DIN.

Production authority:

NONE

Current disposition:

FUTURE_CANDIDATE

---

# 6. MODEL-DIEN-001

Name:

Deep Interest Evolution Network

Status:

DISCOVERED

Domain:

Sequential behavioral recommendation

Expected purpose:

Model how user interests evolve through behavioral sequences.

Verification requirement:

Primary publication identity, formulas, implementation, dataset, and evaluation must be verified before promotion to IDENTITY_VERIFIED.

No production implementation authorized.

---

# 7. MODEL-BST-001

Name:

Behavior Sequence Transformer

Status:

DISCOVERED

Domain:

Sequential recommendation

Expected purpose:

Use Transformer-style attention over user behavior histories.

Verification required before any canonical technical claims are attached.

---

# 8. MODEL-ESMM-001

Name:

Entire Space Multi-Task Model

Status:

DISCOVERED

Domain:

CTR / CVR multi-task learning

Expected architectural idea:

Jointly model click-through and click-to-conversion behavior across the full impression space to address sample-selection bias in CVR modeling.

Important:

Exact loss semantics must be extracted from the primary paper before implementation.

Do not use simplified secondary formulas as canonical model definitions.

---

# 9. MODEL-PLE-001

Name:

Progressive Layered Extraction

Status:

DISCOVERED

Organization association:

Tencent research

Domain:

Multi-task learning

Expected use:

Separate task-specific and shared representation learning through layered expert/gating structures.

Potential commerce uses:

- CTR + CVR;
- conversion + revenue;
- engagement + retention;
- recommendation multi-objective learning.

No production implementation authorized.

---

# 10. MODEL-MMOE-001

Name:

Multi-gate Mixture-of-Experts

Status:

DISCOVERED

Domain:

Multi-task learning

Potential role:

Benchmark against PLE when multi-task modeling becomes justified.

---

# 11. MODEL-SARIMA-001

Name:

Seasonal ARIMA

Status:

METHOD_KNOWN

Domain:

Demand forecasting

Purpose:

Provide a classical statistical baseline.

Important:

SARIMA should be tested before more complex neural forecasting when seasonality and history support it.

Potential OXYCOK use:

- daily demand;
- weekly seasonality;
- inventory forecasting.

---

# 12. MODEL-LSTM-FORECAST-001

Name:

LSTM Demand Forecasting

Status:

METHOD_KNOWN

Potential OXYCOK use:

Sequential demand forecasting.

Promotion requirement:

Must outperform simpler forecasting baselines on time-based holdout data.

Required baselines:

- naive last value;
- seasonal naive;
- moving average;
- exponential smoothing;
- SARIMA.

---

# 13. MODEL-DQN-PRICING-001

Name:

Deep Q-Network Dynamic Pricing

Status:

RESEARCH_ONLY

Risk class:

HIGH

Current authority:

PRODUCTION_PROHIBITED

Reason:

Dynamic pricing is a financially consequential decision problem involving:

- causal attribution;
- exploration cost;
- fairness;
- customer trust;
- inventory;
- seasonality;
- competitor effects;
- delayed reward;
- partial observability.

A DQN must not be introduced merely because the Q-learning formulation is available.

Required progression:

STATIC PRICING
    ↓
PRICE EXPERIMENTS
    ↓
ELASTICITY ESTIMATION
    ↓
CONTEXTUAL DECISION MODEL
    ↓
OFFLINE POLICY EVALUATION
    ↓
SHADOW
    ↓
BOUNDED PILOT

Only then may reinforcement-learning pricing be reconsidered.

---

# 14. Formula Authority

A formula copied from:

- an AI answer;
- blog;
- secondary article;
- unofficial implementation;

is not canonical.

Formula status:

UNVERIFIED

PRIMARY_SOURCE_VERIFIED

IMPLEMENTATION_VERIFIED

REPRODUCED

Each important formula should eventually bind to a source.

---

# 15. Code Authority

External GitHub code is reference material.

It should not automatically become OXYCOK production code.

Required evaluation:

LICENSE
    ↓
MODEL/PAPER IDENTITY
    ↓
DEPENDENCIES
    ↓
SECURITY
    ↓
REPRODUCIBILITY
    ↓
ARCHITECTURE EXTRACTION
    ↓
LOCAL IMPLEMENTATION OR APPROVED DEPENDENCY

Reference code may be obsolete.

For example, older recommender implementations may depend on outdated TensorFlow or Python environments.

---

# 16. Baseline-First Doctrine

No complex model is permitted to claim value without comparison to a simpler baseline.

Recommendation hierarchy:

MOST_POPULAR
    ↓
TRENDING
    ↓
CO-PURCHASE
    ↓
CONTENT SIMILARITY
    ↓
MATRIX FACTORIZATION
    ↓
GRAPH COLLABORATIVE FILTERING
    ↓
SEQUENTIAL / MULTI-TASK MODELS

Forecasting hierarchy:

NAIVE
    ↓
SEASONAL_NAIVE
    ↓
MOVING_AVERAGE
    ↓
EXPONENTIAL_SMOOTHING
    ↓
SARIMA
    ↓
ML
    ↓
DEEP_SEQUENCE_MODEL

Pricing hierarchy:

STATIC
    ↓
RULED EXPERIMENT
    ↓
ELASTICITY MODEL
    ↓
CONTEXTUAL OPTIMIZATION
    ↓
RL ONLY IF EARNED

---

# 17. Offline ≠ Online

Offline performance metrics may include:

- Recall@K;
- Precision@K;
- NDCG@K;
- Hit Rate;
- AUC;
- Log Loss;
- RMSE;
- MAE.

These are engineering evidence.

They are not automatically business outcomes.

Required progression:

OFFLINE IMPROVEMENT
    ↓
SHADOW EVALUATION
    ↓
CONTROLLED ONLINE EXPERIMENT
    ↓
BUSINESS OUTCOME

---

# 18. Business Metrics

Recommendation systems should ultimately be evaluated against appropriate business metrics including:

- recommendation CTR;
- add-to-cart rate;
- conversion;
- revenue per session;
- AOV;
- gross margin;
- returns;
- recommendation diversity;
- repeat purchase;
- customer complaints where relevant.

A recommendation model maximizing clicks but reducing purchases is not necessarily better.

---

# 19. Data Leakage Protection

Model training must explicitly guard against:

- future-event leakage;
- post-purchase information appearing in pre-purchase features;
- train/test user overlap issues where inappropriate;
- temporal leakage;
- target encoding leakage;
- duplicated events;
- experiment treatment leakage.

Time-dependent commerce systems should generally use temporal evaluation rather than arbitrary random splitting when the goal is future prediction.

---

# 20. Cold Start

Every recommendation system must define behavior for:

NEW USER

NEW PRODUCT

NO HISTORY

ANONYMOUS SESSION

SPARSE HISTORY

Fallback behavior must be deterministic and testable.

---

# 21. Model Promotion

Model promotion requires:

IDENTITY
    ↓
REPRODUCTION
    ↓
BASELINE COMPARISON
    ↓
LOCAL DATA
    ↓
HOLDOUT
    ↓
ROBUSTNESS
    ↓
BUSINESS EXPERIMENT
    ↓
GUARDRAILS
    ↓
REPLICATION
    ↓
OPERATING ENVELOPE

Only then:

QUALIFIED_MODEL