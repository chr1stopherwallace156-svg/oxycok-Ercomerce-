# OXYCOK Commerce — Advantage Discovery Protocol

> Systematic discovery, testing, qualification, and institutionalization of commercial advantages.

---

# 1. Purpose

OXYCOK should continuously search for opportunities created by gaps between:

- current customer experience and better experience;
- market behavior and competitor behavior;
- customer intent and available products;
- supply and demand;
- inventory and purchasing;
- content and attention;
- product discovery and customer need;
- operational cost and operational efficiency;
- current knowledge and emerging evidence.

The objective is not exploitation for its own sake.

The objective is durable competitive advantage.

---

# 2. Advantage Classes

Every candidate advantage should be classified before testing.

```text
ADV-BEHAVIORAL
Customer decision behavior

ADV-MERCHANDISING
Product discovery, presentation and bundling

ADV-PRICING
Price architecture and promotions

ADV-CONTENT
Creative, educational and social content

ADV-SEARCH
SEO, internal search and discovery

ADV-SOCIAL
Social proof, creators and community

ADV-RETENTION
Repeat purchase and lifecycle

ADV-INVENTORY
Stock allocation and replenishment

ADV-SUPPLY
Sourcing, payment terms and procurement

ADV-LOGISTICS
Delivery and fulfillment

ADV-TIMING
Time-of-day, seasonality and event timing

ADV-MARKET
Geography, culture and market differences

ADV-DATA
Information and measurement advantage

ADV-AUTOMATION
Operational automation

ADV-EXPERIENCE
Store UX and customer service
```

---

# 3. Candidate State Machine

```text
DISCOVERED
    ↓
SOURCE_VERIFIED
    ↓
MECHANISM_IDENTIFIED
    ↓
LOCAL_RELEVANCE_ASSESSED
    ↓
TESTABLE
    ↓
EXPERIMENT_REGISTERED
    ↓
TESTING
    ↓
SUPPORTED / REJECTED / INCONCLUSIVE
    ↓
REPLICATED
    ↓
QUALIFIED
    ↓
CAPABILITY / POLICY
```

No candidate may jump directly:

```text
ARTICLE
→
PRODUCTION
```

---

# 4. Advantage Record

Each candidate should record:

```text
advantage_id
title
class
description

source_refs
source_quality

proposed_mechanism

customer_value
business_value

primary_metric
secondary_metrics
guardrail_metrics

required_data
required_capabilities

authority_required

expected_cost
expected_upside

known_risks
unknowns
contradictions

experimentability

local_status
qualification_status
```

---

# 5. Evidence Rule

Claims found in:

- academic papers;
- social posts;
- videos;
- case studies;
- marketing articles;
- competitor commentary;
- AI-generated research;
- leaked or allegedly leaked material;

must not receive equal authority.

Use:

```text
PRIMARY VERIFIED
SECONDARY VERIFIED
INDUSTRY REPORT
CASE STUDY
ANECDOTAL
UNVERIFIED CLAIM
```

Numerical uplift claims require source verification before being recorded as evidence.

---

# 6. Mechanism Before Tactic

Do not store only:

```text
"add countdown timer"
```

Store:

```text
MECHANISM:
loss aversion / urgency

TACTIC:
countdown timer

CONDITIONS:
real expiration

RISK:
false scarcity / trust damage

METRICS:
conversion
refund
complaints
repeat purchase
```

This allows future experimentation with the mechanism without hard-coding one tactic.

---

# 7. Truthfulness Constraint

Scarcity, urgency, social proof, reviews and pricing references must reflect truthful underlying conditions.

Examples:

```text
"Only 3 left"
requires actual eligible inventory state.

"Sale ends tonight"
requires a real end condition.

"10,000 customers"
requires supportable evidence.

"Was $100"
requires legitimate pricing history/reference basis.
```

Synthetic urgency is not a qualified advantage.

---

# 8. Behavioral Intervention Classes

Every behavioral intervention must receive a classification.

```text
ASSISTIVE

PERSUASIVE

HIGH_PRESSURE

MANIPULATIVE

PROHIBITED
```

Promotion criteria become stricter as pressure increases.

---

# 9. Candidate Behavioral Mechanisms

Potential mechanisms include:

```text
social proof

commitment

loss aversion

anchoring

reciprocity

mere exposure

default effects

choice architecture

goal gradients

habit formation

community identity

perceived scarcity

trust

perceived value

reduced cognitive load

personal relevance
```

Mechanisms themselves have no production authority.

---

# 10. Trust Counter-Metric

Every conversion optimization should ask:

```text
Did the intervention increase transactions
while damaging future customer value?
```

Where applicable track:

```text
refund rate
return rate
cancellations
complaints
unsubscribe
spam complaints
repeat purchase
retention
support contacts
negative reviews
```

---

# 11. Social Proof

Allowed research directions include:

- review quality;
- review quantity;
- creator credibility;
- customer photographs;
- verified purchase signals;
- community participation;
- UGC performance.

Prohibited behavior includes:

- fabricated reviews;
- fabricated customer counts;
- fabricated inventory;
- misleading endorsement claims.

---

# 12. Creator / KOC Research

Do not assume:

```text
nano influencer
=
better creator
```

Measure:

```text
cost per qualified visit
CTR
conversion
revenue
gross margin
new-customer rate
return rate
repeat purchase
```

Creator size is a feature, not the result.

---

# 13. Gamification

Gamification candidates may include:

- progress;
- challenges;
- rewards;
- loyalty;
- referrals;
- collections;
- streaks where appropriate.

Evaluate:

```text
incremental revenue
cost of reward
customer retention
abuse/fraud
customer sentiment
```

Avoid systems dependent on deceptive near-wins or coercive mechanics.

---

# 14. Referral / Sharing

A referral candidate should distinguish:

```text
REFERRER
REFEREE
INVITATION
QUALIFIED REFERRAL
CONVERSION
REWARD
```

Referral reward issuance must be idempotent.

---

# 15. Content Advantage

Optimize beyond likes.

Potential content metrics:

```text
hook retention
completion
rewatch
shares
comments
profile visits
qualified site visits
product views
add to cart
purchase
revenue per viewer
```

Platform ranking assumptions remain research hypotheses unless verified.

---

# 16. Search Advantage

SEO and internal search should be measured by:

```text
query impressions
rank
CTR
landing engagement
conversion
revenue
```

Long-tail keywords are candidates, not automatically superior keywords.

Programmatically generated pages must provide actual user value rather than exist purely for index volume.

---

# 17. Inventory Advantage

Potential mechanisms:

```text
small-batch testing
reorder optimization
stockout prediction
dead-stock identification
inventory reallocation
```

Required business metrics:

```text
sell-through
stockout rate
inventory turns
gross margin
markdown rate
holding cost
```

---

# 18. Supply Advantage

Potential mechanisms:

```text
supplier comparison
payment terms
lead-time reduction
MOQ optimization
backup suppliers
quality variation detection
```

Supplier financing is a cash-flow tool, not free capital.

Record:

```text
terms
cost
risk
dependency
late-payment consequence
```

---

# 19. Fulfillment Advantage

Evaluate:

```text
delivery promise
actual delivery time
shipping cost
damage rate
return rate
repeat purchase
```

Do not assume faster shipping always dominates economics.

---

# 20. Timing Advantage

Potential dimensions:

```text
hour
weekday
month
season
holiday
pay cycle
product lifecycle
campaign lifecycle
customer lifecycle
```

External timing research generates priors.

First-party outcomes adjudicate local value.

---

# 21. Cultural Transferability

A behavior observed in one market must not automatically be translated into another.

```text
CHINA RESULT
≠
US RESULT
```

Evaluate:

```text
market
language
culture
platform
customer demographics
product category
price point
purchase context
```

Cultural concepts may inspire hypotheses but must not become stereotypes.

---

# 22. Brand Philosophy

Narrative frameworks may be explored where authentic to the brand.

Examples:

```text
simplicity
care
craft
balance
community
self-expression
ritual
premium experience
```

Philosophy should support the actual brand rather than become fabricated cultural decoration.

---

# 23. Competitive Intelligence

Allowed inputs may include:

- publicly visible prices;
- product assortments;
- promotions;
- shipping promises;
- content;
- messaging;
- public reviews;
- public advertising libraries;
- authorized market-data providers.

Every source must comply with the data-source policy.

---

# 24. Opportunity Score

Do not rank ideas using expected revenue alone.

Conceptual score:

```text
OPPORTUNITY
=
EXPECTED_VALUE
× EVIDENCE_STRENGTH
× TESTABILITY
× REVERSIBILITY
× STRATEGIC_FIT

divided by

COST
× RISK
× COMPLEXITY
```

The exact formula must be validated before automation.

---

# 25. Portfolio Rule

Do not test only high-upside ideas.

Maintain a balanced experiment portfolio:

```text
LOW RISK / FAST
MEDIUM RISK
STRATEGIC
EXPLORATORY
```

This prevents optimization from becoming dependent on speculative experiments.

---

# 26. Experiment Requirements

Every meaningful intervention should define:

```text
hypothesis
mechanism
population
control
treatment
primary metric
secondary metrics
guardrails
minimum duration
sample requirement
stopping rule
```

Do not determine the success criteria after seeing the result.

---

# 27. Advantage Memory

Rejected candidates must survive.

The system must be able to answer:

```text
Have we tried this?

When?

Under what conditions?

Why did it fail?

Would changed conditions justify retesting?
```

This prevents repeated rediscovery.

---

# 28. Contradiction Search

For every high-value candidate ask:

```text
What evidence suggests this tactic fails?
```

Actively seek:

- contrary studies;
- category differences;
- customer backlash;
- unintended effects;
- platform restrictions;
- long-run effects.

---

# 29. Scale Challenge

A successful 5% traffic test does not automatically support full deployment.

Promotion ladder:

```text
OFFLINE
↓
INTERNAL
↓
1–5%
↓
10–20%
↓
LARGER CANARY
↓
FULL ELIGIBLE POPULATION
```

Scale based on consequence and evidence.

---

# 30. Institutionalization

Repeated successful mechanisms should move from experimentation into capability.

```text
DISCOVERY
↓
EXPERIMENT
↓
REPLICATION
↓
GENERAL MECHANISM
↓
CAPABILITY
↓
POLICY
↓
AUTOMATIC INHERITANCE
```

This is the primary reason this protocol exists.

---

# 31. Weekly Advantage Search

The system should eventually search across:

```text
ACADEMIC RESEARCH
PLATFORM DOCUMENTATION
MARKET DATA
COMPETITOR OBSERVATION
CUSTOMER FEEDBACK
INTERNAL ANALYTICS
FAILED EXPERIMENTS
SUCCESSFUL EXPERIMENTS
SUPPLY CHAIN
OPERATIONS
```

The objective is not maximum document volume.

The objective is maximum useful unexplored opportunity coverage.

---

# 32. Final Rule

```text
A TACTIC IS NOT AN ADVANTAGE.

AN ADVANTAGE IS A MECHANISM
THAT REPEATEDLY CREATES NET BUSINESS VALUE
UNDER DECLARED CONDITIONS
WITHOUT VIOLATING ITS GUARDRAILS.
```