# OXYCOK — Chinese / Industrial Recommender Research Pack

## Status

PACK_STATUS = PRIMARY_SOURCES_VERIFIED
PRODUCTION_AUTHORITY = NONE
LOCAL_VALUE = UNPROVEN

---

## MODEL-ESMM-001

Title:
Entire Space Multi-Task Model:
An Effective Approach for Estimating Post-Click Conversion Rate

Organization:
Alibaba

Venue:
SIGIR 2018

Problem:
Post-click CVR estimation suffers from:
- sample-selection bias;
- sparse conversion labels.

Required behavioral chain:

IMPRESSION
→ CLICK
→ CONVERSION

Core relation:

P(CTCVR) = P(CTR) × P(CVR)

OXYCOK prerequisite:

- actual impression telemetry;
- deterministic impression identity;
- clicks;
- Shopify-confirmed conversion labels;
- attribution rules;
- temporal feature cutoff.

Primary OXYCOK role:

FIRST ADVANCED CTR/CVR MODEL CANDIDATE

Current state:

IDENTITY_VERIFIED
LOCAL_DATA_NOT_READY
PRODUCTION_PROHIBITED

---

## MODEL-PLE-001

Title:
Progressive Layered Extraction (PLE)

Organization:
Tencent

Venue:
RecSys 2020

Problem:

Multi-task models can suffer negative transfer / seesaw behavior,
where improving one task harms another.

Mechanism:

- shared experts;
- task-specific experts;
- task-specific gates;
- progressive extraction across layers.

OXYCOK prerequisite:

Evidence that simpler shared-bottom / ESMM / MMoE architecture
experiences meaningful task conflict.

Primary OXYCOK role:

NEGATIVE_TRANSFER_CHALLENGER

Current state:

IDENTITY_VERIFIED
LOCAL_NEED_UNPROVEN
PRODUCTION_PROHIBITED

---

## MODEL-DIN-001

Title:
Deep Interest Network for Click-Through Rate Prediction

Organization:
Alibaba

Venue:
KDD 2018

Problem:

Fixed user embeddings can fail to represent diverse interests
relevant to different candidate products.

Mechanism:

Candidate-conditioned activation over historical user behavior.

OXYCOK prerequisite:

- ordered behavioral history;
- stable product identity;
- candidate identity;
- sufficient interaction volume.

Primary role:

BEHAVIORAL CTR / RANKING CANDIDATE

Current state:

IDENTITY_VERIFIED
LOCAL_NEED_UNPROVEN

---

## MODEL-DIEN-001

Title:
Deep Interest Evolution Network for Click-Through Rate Prediction

Organization:
Alibaba

Venue:
AAAI 2019

Problem:

User interests change over time and explicit behaviors are imperfect
representations of latent interest.

Mechanism:

- sequential interest extractor;
- auxiliary loss;
- attention-aware interest evolution.

OXYCOK prerequisite:

- sufficiently long ordered user behavior sequences;
- reliable timestamps;
- stable identity;
- evidence DIN-like static history representation is inadequate.

Primary role:

SEQUENTIAL USER-INTEREST CHALLENGER

Current state:

IDENTITY_VERIFIED
LOCAL_NEED_UNPROVEN

---

## MODEL-MMOE-001

Title:
Modeling Task Relationships in Multi-task Learning with
Multi-gate Mixture-of-Experts

Organization:
Google

Venue:
KDD 2018

Problem:

Different prediction tasks may have varying levels of relatedness.

Mechanism:

Shared experts + separate learned gate per task.

OXYCOK prerequisite:

Multiple targets whose task relationships need to be learned.

Primary role:

MULTI-TASK BASELINE / PLE CHALLENGER

Current state:

IDENTITY_VERIFIED
LOCAL_NEED_UNPROVEN

---

# Required Local Comparison Ladder

B0 = popularity / deterministic ranking
B1 = logistic regression
B2 = single-task MLP
B3 = shared-bottom multi-task model
B4 = ESMM
B5 = MMoE
B6 = PLE

DIN / DIEN form a separate sequential-interest branch and should only
enter comparison when behavior-history evidence warrants them.

---

# Promotion Rule

PRIMARY PAPER
↓
REFERENCE IMPLEMENTATION REVIEW
↓
FORMULA REPRODUCTION
↓
DATA CONTRACT
↓
BASELINE REPRODUCTION
↓
LOCAL OFFLINE TEST
↓
LEAKAGE ATTACK
↓
CALIBRATION
↓
SHADOW
↓
ONLINE EXPERIMENT
↓
GUARDRAIL METRICS
↓
REPLICATION
↓
QUALIFIED

No model may skip directly from paper verification to production.

---

# Stop Rule

A more complex model is rejected when it fails to produce sufficient
incremental value relative to the simpler qualified alternative after
accounting for:

- latency;
- maintenance;
- training cost;
- inference cost;
- feature complexity;
- operational risk;
- explainability;
- data requirements.

MODEL_COMPLEXITY must earn itself.