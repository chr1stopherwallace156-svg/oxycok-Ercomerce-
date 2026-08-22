# OXYCOK Commerce — Market Intelligence Protocol

## Purpose

Continuously discover potentially valuable product, category,
market, geographic and seasonal opportunities without confusing
external popularity with local profitability.

---

## Core Invariants

TREND != DEMAND

DEMAND != PURCHASE

PURCHASE != PROFIT

REVENUE != CONTRIBUTION

EXTERNAL SUCCESS != OXYCOK SUCCESS

---

## Signal Families

### Search

Examples:

- search interest;
- search growth;
- keyword expansion;
- geographic interest.

Authority:

EXTERNAL_CONTEXT

---

### Social

Examples:

- video engagement;
- creator activity;
- product mentions;
- advertising activity;
- content velocity.

Authority:

EXTERNAL_CONTEXT

---

### Marketplace

Examples:

- visible assortment;
- price;
- ranking;
- product velocity indicators;
- review activity.

Authority:

MARKET_OBSERVATION

---

### First Party

Examples:

- Shopify orders;
- product views;
- recommendation impressions;
- carts;
- purchases;
- returns;
- refunds;
- contribution margin.

Authority:

FIRST_PARTY / TRANSACTIONAL

---

### Supplier

Examples:

- unit cost;
- MOQ;
- lead time;
- shipping;
- defect rate;
- payment terms.

Authority:

SUPPLY_EVIDENCE

---

## Opportunity Dimensions

A product opportunity may include:

DEMAND_GROWTH
DEMAND_STABILITY
LOCAL_CONVERSION
GROSS_MARGIN
CONTRIBUTION_MARGIN
COMPETITIVE_DENSITY
PRICE_HEADROOM
LOGISTICS
RETURN_RISK
SUPPLY_RISK
SEASONALITY
CONTENT_FIT
REPEAT_PURCHASE
DIFFERENTIATION
TEST_COST

No single dimension establishes an opportunity.

---

## Margin Doctrine

Do not use generic category margin percentages as business truth.

Required calculation:

REVENUE
-
PRODUCT COST
-
INBOUND FREIGHT
-
OUTBOUND FULFILLMENT
-
PAYMENT FEES
-
PLATFORM FEES
-
DISCOUNTS
-
RETURNS
-
REFUNDS
-
CREATOR / AFFILIATE COST
-
VARIABLE SUPPORT COST
-
VARIABLE AD COST
=
CONTRIBUTION

Gross margin is useful.

Contribution margin is closer to operating truth.

---

## Trend Doctrine

External popularity should be decomposed into:

LEVEL
VELOCITY
ACCELERATION
PERSISTENCE
VOLATILITY
GEOGRAPHIC BREADTH
SOURCE AGREEMENT

A one-day spike is not equivalent to persistent demand growth.

---

## Cross-Source Confirmation

Prefer candidates appearing independently in multiple source families.

Example:

GOOGLE SEARCH ↑
+
SOCIAL MENTIONS ↑
+
MARKETPLACE ACTIVITY ↑
+
LOCAL PRODUCT VIEWS ↑

is stronger evidence than one viral video.

Cross-source agreement still does not establish profitability.

---

## Geographic Rule

Do not assume a product winning in one market transfers.

Evaluate:

COUNTRY
LANGUAGE
CLIMATE
SEASON
INCOME / PRICE POINT
SHIPPING COST
DELIVERY TIME
REGULATORY REQUIREMENTS
CULTURAL FIT
LOCAL COMPETITION

---

## Candidate Progression

DISCOVERED
↓
MULTI_SOURCE_SUPPORTED
↓
ECONOMICALLY_PLAUSIBLE
↓
SUPPLY_FEASIBLE
↓
TESTABLE
↓
LOCAL_PILOT
↓
UNIT_ECONOMICS_VERIFIED
↓
REPLICATED
↓
QUALIFIED

---

## Kill Conditions

A candidate may be rejected for:

negative contribution margin;
unreliable supplier;
excessive return risk;
unacceptable delivery time;
regulatory constraints;
fragile demand;
extreme competition;
insufficient differentiation;
customer-trust risk;
poor local experiment result.

---

## Final Rule

The purpose of market intelligence is not to find products
that look exciting.

It is to find opportunities whose economics survive contact
with real customers.