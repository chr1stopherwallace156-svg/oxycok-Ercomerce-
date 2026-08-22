# OXYCOK Commerce — Business Implementation Blueprint

## Execution Rule

Build the smallest trustworthy capability that proves the next architectural requirement.

Advanced models do not receive priority merely because they are more sophisticated.

Every major capability must define:

- business objective;
- source data;
- baseline;
- proposed method;
- authority level;
- test method;
- rollback;
- success metric;
- failure conditions.

---

# Phase 0 — Shopify Backbone

## Objective

Establish reliable commerce truth and event capture.

## Build

- Shopify GraphQL Admin API client
- explicit API version
- secure environment configuration
- product retrieval
- order retrieval
- customer retrieval
- inventory retrieval
- webhook receiver
- HMAC verification
- event identity
- idempotency
- durable event storage
- structured logging

## Initial Webhooks

Start with only the events we actually need:

- products/update
- orders/create
- inventory_levels/update
- customers/create

Expand later.

## Exit Criteria

- Shopify connectivity verified
- webhook verification verified
- duplicate webhook does not duplicate business effect
- secrets absent from Git
- event persists successfully

---

# Phase 1 — Behavioral Data + Recommendation Baseline

## Objective

Measure user behavior and establish simple recommendation baselines.

## Capture

- page_view
- product_view
- add_to_cart
- purchase
- optional dwell/scroll signals if justified

## Baselines

Before ML:

- top sellers
- trending products
- co-purchase
- recently viewed
- category affinity

## Exit Criteria

At least one baseline recommendation system is measurable and testable.

---

# Phase 2 — AI-Assisted Merchandising and Content

## Objective

Use AI for low-risk recommendation and drafting tasks.

## Capabilities

- product description drafts
- SEO title/meta drafts
- collection recommendations
- merchandising recommendations
- content ideation

## Authority

Draft/recommend only.

No automatic publishing initially.

## Exit Criteria

AI outputs are grounded, reviewable, and measured against a baseline.

---

# Phase 3 — Retention and Experimentation

## Objective

Increase repeat purchase and AOV through controlled experiments.

## Capabilities

- abandoned-cart candidate generation
- post-purchase cross-sell
- segmentation
- loyalty experiments
- pricing experiments

## Pricing Rule

No adaptive pricing model until:

- traffic is sufficient
- baseline pricing performance is measured
- elasticity can be estimated
- experiment guardrails exist

## Exit Criteria

Experiments are logged and outcomes measured.

---

# Phase 4 — Research Intelligence

## Objective

Integrate external research without allowing research findings to self-promote into production.

## Flow

SOURCE
↓
VERIFIED FINDING
↓
LOCAL HYPOTHESIS
↓
EXPERIMENT
↓
RESULT
↓
PROMOTE / REJECT

## Sources

- Chinese academic research
- industry research
- platform trend data
- competitor observations
- internal outcomes

## Exit Criteria

Research can generate structured implementation candidates without bypassing qualification.

---

# Phase 5 — Bounded Automation

## Objective

Promote proven low-risk capabilities into constrained automation.

## Requirements

- authority registry
- policy checks
- state revalidation
- idempotency
- audit trail
- rollback
- kill switch
- monitoring

## Exit Criteria

At least one low-risk capability executes automatically inside a declared operating envelope.

---

# Modeling Policy

Use advanced ML only when it beats simpler baselines.

Examples:

Recommendation progression:

MOST_POPULAR
↓
CO-PURCHASE
↓
CONTENT SIMILARITY
↓
MATRIX FACTORIZATION
↓
GRAPH MODEL / LIGHTGCN
↓
RERANKING

Pricing progression:

STATIC
↓
RULE TEST
↓
A/B TEST
↓
ELASTICITY MODEL
↓
ADAPTIVE MODEL
↓
RL ONLY IF JUSTIFIED

---

# Drift Policy

A drift signal triggers investigation.

It does not automatically trigger production retraining.

DRIFT
↓
DIAGNOSE
↓
RETRAIN CANDIDATE
↓
OFFLINE EVALUATION
↓
SHADOW / CANARY
↓
PROMOTION

---

# Revenue Measurement

Revenue improvements must be measured locally.

Do not assume published uplift transfers to OXYCOK.

Track:

- conversion rate
- AOV
- repeat purchase rate
- revenue per visitor
- gross margin
- refund rate
- unsubscribe rate
- customer complaints
- recommendation CTR
- add-to-cart rate

---

# Current Priority

1. Shopify API connection
2. Webhook verification
3. Event persistence
4. behavioral events
5. simple recommendation baseline
6. first AI drafting capability