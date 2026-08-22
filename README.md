# OXYCOK Commerce

> Evidence-driven, AI-native commerce infrastructure built around controlled automation, durable institutional memory, measurable outcomes, and explicit authority.

---

## Project Status

**Stage:** Foundation / Gen0  
**Repository role:** Canonical source of truth  
**Primary commerce platform:** Shopify  
**Architecture:** Event-driven, AI-assisted, progressively autonomous  
**Operating principle:** Evidence before automation

This repository is in active development.

Do not interpret the existence of a component, test, agent, integration, or experiment as evidence that it is production-qualified.

---

# 1. Mission

OXYCOK Commerce is being built as a fully functional AI-native e-commerce operating system.

The objective is not merely to add AI features to an online store.

The objective is to build a commerce platform capable of:

- observing the business;
- preserving important events and evidence;
- understanding products, customers, orders, inventory, campaigns, and outcomes;
- detecting problems and opportunities;
- producing traceable recommendations;
- preparing actions;
- executing explicitly authorized actions;
- measuring the consequences of those actions;
- learning from successful and failed interventions;
- converting repeated methodology into reusable capabilities;
- increasing automation only when evidence justifies it;
- preserving enough durable state that another engineer or AI agent can resume the project without depending on conversation history.

The long-term system should require progressively less procedural prompting from the owner.

The owner should increasingly define:

- objectives;
- strategy;
- risk tolerance;
- business constraints;
- high-impact approvals;

while the repository preserves and enforces the methodology required to operate toward those objectives.

---

# 2. Core Philosophy

The repository is not merely where code lives.

It is the project's:

- durable memory;
- operating constitution;
- evidence system;
- decision history;
- experiment ledger;
- failure record;
- qualification laboratory;
- capability registry;
- authority map;
- reproducibility mechanism;
- handoff system.

Important project knowledge must not exist only inside an AI conversation, developer memory, terminal session, or local machine.

If information is necessary to:

- reproduce a result;
- understand a decision;
- validate an artifact;
- operate the system safely;
- continue development;
- understand current project state;

it should eventually have a durable, discoverable representation in the repository.

---

# 3. Operating Doctrine

## 3.1 Repository = Durable Memory

Session-local knowledge is not project knowledge.

Important decisions, assumptions, interfaces, failures, qualification results, operating rules, and current state must survive the session that created them.

---

## 3.2 Evidence Before Belief

A convincing AI response is not evidence.

Where appropriate, conclusions should be traceable to:

- Shopify state;
- API responses;
- webhook events;
- database records;
- deterministic calculations;
- experiment results;
- tests;
- external authoritative sources;
- versioned artifacts;
- human approvals.

Important artifacts should carry identity and provenance appropriate to their risk.

---

## 3.3 Observation ≠ Interpretation ≠ Authority

These states must remain distinguishable.

A system may:

1. observe something;
2. interpret the observation;
3. derive additional information;
4. recommend an action;
5. possess authority to execute that action.

These are not equivalent.

Example:

> Conversion declined after a price increase.

may be an observation.

> The price increase caused the decline.

is an interpretation requiring additional evidence.

> Lower the price to $89.

is a recommendation.

> Change the Shopify price to $89.

is a mutation requiring explicit authority.

No component should gain mutation authority merely because it can generate analysis.

---

## 3.4 Freeze Before Improvement

When investigating a failure or weakness, preserve the pre-change state whenever practical.

A meaningful improvement requires a meaningful baseline.

Do not quietly modify:

- fixtures;
- expected outputs;
- evaluation criteria;
- datasets;
- thresholds;

and then claim improvement against the modified test.

---

## 3.5 Agreement Is Not Truth

Agreement between:

- multiple AI models;
- multiple agents;
- multiple prompts;
- multiple generated analyses;

does not independently establish correctness.

Where the consequence warrants it, truth should be adjudicated through stronger evidence such as:

- deterministic checks;
- authoritative data;
- independent measurements;
- controlled experiments;
- actual business outcomes;
- human review.

---

## 3.6 Attack Success

PASS does not mean truth.

PASS means:

> The system passed the declared test under the declared conditions.

Successful capabilities should eventually be challenged against:

- unseen data;
- different products;
- different customer segments;
- different traffic regimes;
- different stores;
- different seasons;
- malformed events;
- stale state;
- contradictory state;
- missing evidence;
- API failures;
- retries;
- duplicate events;
- concurrency;
- adversarial inputs.

The purpose of qualification is not to prove the system is good.

It is to discover where the system is still wrong.

---

## 3.7 Fix Mechanisms, Not Examples

Do not patch isolated examples when they reveal a general failure class.

Bad:

```text
if product_id == "example":
    special_case()
```

Better:

```text
failure
    ↓
classify mechanism
    ↓
implement smallest general correction
    ↓
test original failure
    ↓
test unseen cases
    ↓
regression test
```

A discovered failure should ideally leave behind a reusable capability.

---

## 3.8 Fail Closed Where False Confidence Is Dangerous

UNKNOWN should remain UNKNOWN.

Missing evidence should remain missing.

Contradiction should remain contradiction.

Unauthorized actions should remain unauthorized.

Failed validation should not silently become success.

Systems should not invent certainty merely to continue a workflow.

---

## 3.9 Protect Truth Owners

Not every component may mutate canonical state.

The architecture should explicitly identify:

- observation producers;
- candidate producers;
- validators;
- policy evaluators;
- canonical writers;
- mutation sinks;
- human approval points.

Derived analysis must not silently rewrite authoritative commerce state.

---

## 3.10 Optimize Review, Not Merely Accuracy

More AI calls do not automatically produce a better system.

Use the smallest sufficient resolver.

A problem may require:

- deterministic code;
- database lookup;
- Shopify lookup;
- targeted AI analysis;
- external research;
- human review;
- or an explicit unresolved state.

Escalation should be intentional.

---

## 3.11 Every Failure Should Leave the System Stronger

A legitimate failure should ideally produce one or more of:

- a regression test;
- a new fixture;
- a better invariant;
- a stronger validator;
- improved observability;
- a new failure classification;
- a better authority boundary;
- improved documentation;
- a reusable capability.

Failure is information about architecture.

---

## 3.12 No Architecture for Architecture's Sake

Do not invent complexity merely because it sounds sophisticated.

Build enough architecture to protect correctness and enable growth.

Then allow real commerce problems to expose the next missing capability.

---

## 3.13 Repeated Instructions Are Architecture Signals

Repeated owner prompting should be treated as evidence of missing system capability.

If an instruction repeatedly appears in prompts, determine whether it belongs in:

```text
Owner preference       → configuration
Business policy        → policy registry
Safety constraint      → runtime guard
Authority restriction  → authority model
Known methodology      → reusable capability
Validation requirement → qualification
Data requirement       → schema / contract
Repeated workflow      → orchestration
Known failure          → regression test
Project state           → repository state
```

The long-term objective is not to make the owner better at prompting.

It is to make the system require less procedural prompting.

---

## 3.14 Automation Must Be Earned

Automation is not granted because an AI appears intelligent.

Authority should increase only after demonstrated reliability within a declared operating envelope.

Conceptually:

```text
MANUAL
  ↓
OBSERVE
  ↓
ANALYZE
  ↓
RECOMMEND
  ↓
DRAFT
  ↓
HUMAN-APPROVED EXECUTION
  ↓
BOUNDED AUTOMATION
  ↓
QUALIFIED AUTOMATION
  ↓
CONTINUOUSLY MONITORED AUTOMATION
```

Different capabilities may permanently have different authority ceilings.

---

# 4. Commerce Source of Truth

Shopify is initially the authoritative transactional commerce platform.

Primary integration:

**Shopify GraphQL Admin API**

Expected domains include:

- products;
- variants;
- collections;
- inventory;
- locations;
- orders;
- customers;
- discounts;
- fulfillment;
- metafields;
- relevant store configuration.

Shopify webhooks provide the initial event stream used to observe important commerce state changes.

The AI layer does **not** replace Shopify as transactional truth.

It operates around Shopify as an intelligence, policy, memory, experimentation, and orchestration system.

---

# 5. High-Level Architecture

```text
CUSTOMER / STOREFRONT
        │
        ▼
SHOPIFY
        │
        ├── GraphQL Admin API
        │
        └── Webhooks
        │
        ▼
EVENT INGESTION
        │
        ▼
NORMALIZATION
        │
        ▼
COMMERCE MEMORY
        │
        ├── state
        ├── history
        ├── evidence
        ├── decisions
        ├── experiments
        └── outcomes
        │
        ▼
AI / INTELLIGENCE CAPABILITIES
        │
        ▼
POLICY + AUTHORITY ENGINE
        │
        ▼
ACTION CANDIDATE
        │
        ▼
VALIDATION
        │
        ▼
APPROVAL / AUTHORIZED AUTOMATION
        │
        ▼
CONTROLLED MUTATION SINK
        │
        ▼
SHOPIFY / EXTERNAL SYSTEM
        │
        ▼
RESULT RECEIPT
        │
        ▼
OUTCOME MEASUREMENT
        │
        ▼
EXPERIMENT / KNOWLEDGE LOOP
```

---

# 6. AI Capability Domains

The architecture should eventually support specialized capabilities rather than one unrestricted general-purpose agent.

Potential domains include:

### Merchandising

- collection optimization;
- product ranking;
- product relationships;
- cross-sell discovery;
- upsell discovery;
- underperforming-product diagnosis.

### Product Intelligence

- product enrichment;
- description drafting;
- attribute normalization;
- taxonomy;
- claim consistency;
- missing-data detection.

### Customer Intelligence

- segmentation;
- churn risk;
- lifecycle analysis;
- repeat-purchase analysis;
- customer-value analysis.

### Inventory Intelligence

- low-stock detection;
- demand forecasting;
- reorder recommendations;
- inventory anomaly detection;
- stockout-risk analysis.

### Pricing Intelligence

- price-performance analysis;
- elasticity experiments;
- promotion analysis;
- discount effectiveness.

### Marketing

- campaign drafting;
- audience recommendations;
- SEO analysis;
- email/SMS drafting;
- campaign postmortems.

### Customer Support

- support triage;
- response drafting;
- order-context retrieval;
- escalation recommendations.

### Operations

- anomaly detection;
- fulfillment monitoring;
- returns analysis;
- operational diagnostics.

These are capability domains, not automatic authorization grants.

---

# 7. Authority Model

AI capabilities should operate under explicit authority.

Initial conceptual levels:

```text
LEVEL 0 — OBSERVE
Read only.

LEVEL 1 — ANALYZE
Generate interpretations and diagnostics.

LEVEL 2 — RECOMMEND
Propose actions.

LEVEL 3 — DRAFT
Prepare an action without executing it.

LEVEL 4 — APPROVAL_REQUIRED
Execution requires explicit human approval.

LEVEL 5 — BOUNDED_AUTOMATION
Execution is permitted within explicit constraints.

LEVEL 6 — QUALIFIED_AUTONOMY
Execution is permitted inside a validated operating envelope.
```

Authority should be capability-specific.

Examples:

Automatically adding a low-risk internal tag may eventually qualify for bounded automation.

Changing a high-value product's price may remain approval-controlled.

Issuing a large refund may require human approval regardless of broader system maturity.

---

# 8. Decision Traceability

For consequential automated or AI-assisted actions, the system should eventually be able to answer:

```text
WHAT happened?

WHEN did it happen?

WHAT evidence existed?

WHAT produced the observation?

WHAT capability performed the analysis?

WHAT conclusion was reached?

WHY was that conclusion reached?

WHAT policy applied?

WHAT authority level existed?

WHAT action was proposed?

WHO or WHAT approved it?

WHAT changed?

WHAT was the previous state?

CAN the change be reversed?

WHAT was the result?

DID the expected outcome occur?

WHAT did the system learn?

SHOULD that lesson generalize?

HAS the generalization been qualified?
```

The exact implementation will evolve.

The requirement for traceability should not.

---

# 9. Event-Driven Foundation

The system should react to commerce events rather than depend exclusively on periodic full-store scans.

Examples:

```text
PRODUCT_CREATED
PRODUCT_UPDATED

INVENTORY_CHANGED

ORDER_CREATED
ORDER_PAID
ORDER_CANCELLED
ORDER_REFUNDED

CUSTOMER_CREATED
CUSTOMER_UPDATED

FULFILLMENT_CREATED
FULFILLMENT_UPDATED

DISCOUNT_CHANGED
```

Actual webhook subscriptions must be based on Shopify's supported API contracts and the needs demonstrated by real workflows.

Events must be designed for:

- verification;
- idempotency;
- retries;
- duplicate delivery;
- ordering ambiguity;
- replay;
- failure recovery;
- auditability.

A webhook arriving twice must not automatically mean an action occurs twice.

---

# 10. Commerce Memory

The platform needs durable memory beyond current Shopify state.

Shopify can tell us what is true now.

The intelligence system often needs to know:

- what was true previously;
- what changed;
- what the system believed at the time;
- what recommendation was made;
- what action occurred;
- what experiment was running;
- what outcome followed.

This historical layer becomes the basis for increasingly capable reasoning.

---

# 11. Learning Loop

The desired loop is:

```text
CONTEXT
   ↓
OBSERVATION
   ↓
ANALYSIS
   ↓
DECISION
   ↓
CONTROLLED ACTION
   ↓
OUTCOME
   ↓
MEASUREMENT
   ↓
LESSON
   ↓
QUALIFICATION
   ↓
POLICY / CAPABILITY IMPROVEMENT
   ↓
NEXT DECISION
```

Repeated success should trigger investigation just as repeated failure does.

The system should ask:

- Why did this work?
- Under what conditions?
- Does it generalize?
- When does it fail?
- Can the successful mechanism become reusable?
- Is there sufficient evidence to increase its authority?

---

# 12. Qualification Doctrine

A green test suite is necessary but not sufficient for high-impact capabilities.

Qualification should increasingly include:

- unit tests;
- integration tests;
- contract tests;
- frozen fixtures;
- malformed inputs;
- mutation testing where useful;
- adversarial cases;
- duplicate-event tests;
- replay tests;
- stale-state tests;
- concurrency tests;
- authorization tests;
- regression tests;
- unseen examples;
- false-positive measurement;
- false-negative measurement.

A capability should be evaluated against its declared purpose and risk.

---

# 13. Experiment Doctrine

Business optimization should not become undocumented trial and error.

Experiments should eventually record:

```text
hypothesis
baseline
target metric
population
intervention
start time
end condition
guardrails
result
confidence
side effects
disposition
```

Possible dispositions:

```text
REJECTED
INCONCLUSIVE
OBSERVE
REPLICATE
VALIDATED
QUALIFIED
PROMOTED
RETIRED
```

Failed experiments are durable knowledge.

They should not disappear merely because they failed.

---

# 14. Protected Mutation

No arbitrary AI component should directly mutate critical commerce state.

The intended pattern is:

```text
AI / ANALYSIS
      ↓
ACTION CANDIDATE
      ↓
SCHEMA VALIDATION
      ↓
POLICY CHECK
      ↓
AUTHORITY CHECK
      ↓
OPTIONAL HUMAN APPROVAL
      ↓
MUTATION SINK
      ↓
EXTERNAL API
      ↓
RESULT RECEIPT
```

This allows the intelligence layer to evolve without giving every component unrestricted production authority.

---

# 15. Initial Repository Direction

The repository will grow according to demonstrated need.

The conceptual structure is expected to evolve toward:

```text
/
├── README.md
├── CURRENT_STATE.md
├── ROADMAP.md
├── CHANGELOG.md
│
├── doctrine/
│   ├── OPERATING_CONSTITUTION.md
│   ├── AUTHORITY_MODEL.md
│   ├── EVIDENCE_MODEL.md
│   ├── FAILURE_POLICY.md
│   └── AI_AGENT_RULES.md
│
├── registry/
│   ├── capabilities.json
│   ├── authorities.json
│   ├── artifacts.json
│   └── experiments.json
│
├── src/
│   ├── commerce/
│   ├── events/
│   ├── intelligence/
│   ├── policy/
│   └── actions/
│
├── scripts/
│   ├── preflight/
│   ├── validation/
│   └── qualification/
│
├── qualification/
│   ├── fixtures/
│   ├── frozen_baselines/
│   ├── attacks/
│   ├── regressions/
│   └── returns/
│
├── tests/
│
├── artifacts/
│   ├── indexes/
│   └── manifests/
│
└── handoff/
    ├── CURRENT_HANDOFF.md
    └── ZERO_CONTEXT_ENTRY.md
```

This is a direction, not permission to create empty architecture for appearance.

Directories should be introduced when their responsibilities become real.

---

# 16. Initial Technical Priorities

The first engineering stages are:

### Stage 0 — Repository Foundation

Establish:

- current-state tracking;
- operating doctrine;
- authority rules;
- evidence rules;
- AI-agent rules;
- Git discipline;
- zero-context recovery.

### Stage 1 — Shopify Connectivity

Establish:

- secure configuration;
- Shopify GraphQL Admin API client;
- authentication;
- API-version management;
- connectivity verification;
- deterministic error handling.

### Stage 2 — Event Ingestion

Establish:

- Shopify webhook endpoint;
- webhook authenticity verification;
- event normalization;
- event identity;
- idempotency;
- durable event storage;
- retry/failure behavior.

### Stage 3 — Commerce Memory

Establish durable representations for:

- commerce entities;
- event history;
- decisions;
- actions;
- receipts;
- experiments;
- outcomes.

### Stage 4 — First AI Capability

Introduce one bounded capability.

It must demonstrate the complete architecture:

```text
evidence
  ↓
analysis
  ↓
candidate
  ↓
authority
  ↓
approval
  ↓
controlled action
  ↓
receipt
  ↓
outcome
```

Do not begin with unrestricted autonomous commerce.

### Stage 5 — Qualification

Attack the first capability.

Determine:

- where it fails;
- what assumptions were hidden;
- what should generalize;
- what should remain human-controlled.

### Stage 6 — Capability Expansion

Only then expand into additional commerce intelligence domains.

---

# 17. Security Principles

Never commit secrets.

This includes:

- Shopify access tokens;
- API secrets;
- webhook secrets;
- database passwords;
- OAuth credentials;
- private keys;
- service-account credentials.

Secrets belong in approved environment or secret-management systems.

Example environment files must contain placeholders only.

The repository should eventually include automated secret scanning and security checks.

---

# 18. Git Discipline

Important work should become durable.

Normal development should eventually follow:

```text
inspect
  ↓
change
  ↓
validate
  ↓
test
  ↓
review diff
  ↓
commit
  ↓
push
  ↓
verify remote state
  ↓
update handoff/current state
```

A generated file is not considered durable merely because an AI says it created it.

Important repository closure should verify actual Git state.

---

# 19. Durability

The project should eventually support an automated durability check answering questions such as:

```text
Is the working tree clean?

Are required artifacts present?

Are manifests valid?

Are protected files valid?

Are tests passing?

Are authority boundaries intact?

Are there unexpected files?

Is important work uncommitted?

Are commits unpushed?

Does local state agree with remote state?

Can a clean checkout reproduce the required state?

Can a zero-context agent determine what to do next?
```

The goal is not simply backup.

The goal is reproducibility and continuation.

---

# 20. Zero-Context Recovery

A capable engineer or AI agent entering the repository without previous conversation history should eventually be able to determine:

- what the project is;
- what is currently implemented;
- what is not implemented;
- what is authoritative;
- what is experimental;
- what is blocked;
- what tests matter;
- how to validate the repository;
- what the next exact engineering action is.

Conversation history may provide useful context.

It must not become a required dependency for operating the project.

---

# 21. Definition of PASS

Unless a more specific contract overrides it:

> PASS means the declared acceptance criteria passed under the declared test conditions.

PASS does **not** mean:

- universally correct;
- production safe;
- autonomous;
- free from unknown failure modes;
- proven under conditions that were not tested.

---

# 22. Definition of DONE

A feature is not necessarily DONE because code exists.

Depending on risk, DONE may require:

- implementation;
- tests;
- integration;
- validation;
- documentation;
- observability;
- authority definition;
- failure handling;
- security review;
- rollback behavior;
- durable Git state;
- handoff update.

The required closure should match the consequence of failure.

---

# 23. Universal Improvement Loop

The project's preferred improvement cycle is:

```text
REAL PROBLEM
    ↓
OBSERVE
    ↓
PRESERVE EVIDENCE
    ↓
ESTABLISH BASELINE
    ↓
ATTACK
    ↓
CLASSIFY FAILURE
    ↓
FIND GENERAL MECHANISM
    ↓
IMPLEMENT SMALLEST GENERAL FIX
    ↓
ADVERSARIAL TEST
    ↓
REGRESSION TEST
    ↓
CHECK FALSE POSITIVES / FALSE NEGATIVES
    ↓
CHECK AUTHORITY / PROVENANCE
    ↓
DURABILITY CHECK
    ↓
CLEAN CHECKOUT REPRODUCTION
    ↓
COMMIT + PUSH
    ↓
INDEX + HANDOFF
    ↓
RETURN TO REAL WORK
    ↓
WAIT FOR REALITY TO EXPOSE NEXT FAILURE
```

Two rules accompany this loop:

```text
FAIL ≠ embarrassment
FAIL = information about the architecture
```

and:

```text
PASS ≠ truth
PASS = passed this declared test
```

---

# 24. Architectural Question

Every substantial implementation should eventually be evaluated at multiple levels:

```text
IMMEDIATE
What problem are we solving?

SYSTEM
What architecture should own it?

GENERALIZATION
Is this an instance of a reusable problem?

MEMORY
What existing knowledge should automatically apply?

AUTOMATION
Is the owner manually requesting behavior the system should inherit?

CHALLENGE
How could this apparently successful mechanism fail?

EFFICIENCY
What work are we repeating unnecessarily?

AUTHORITY
Can this be automated without weakening control?

FUTURE
What happens at 10× or 100× scale?

NEXT BOTTLENECK
If this problem disappears, what becomes limiting next?
```

This prevents the repository from becoming a collection of isolated successful features.

---

# 25. Long-Term Target

The long-term target is a governed commerce intelligence platform where:

```text
REAL COMMERCE
      ↓
EVENTS + EVIDENCE
      ↓
SPECIALIZED CAPABILITIES
      ↓
CONTROLLED DECISIONS
      ↓
AUTHORIZED ACTIONS
      ↓
BUSINESS OUTCOMES
      ↓
EXPERIMENTS
      ↓
LESSONS
      ↓
QUALIFICATION
      ↓
REPOSITORY KNOWLEDGE
      ↓
BETTER FUTURE OPERATION
```

The owner controls strategy and consequential authority.

The system increasingly handles repeatable methodology.

The repository remembers what both have learned.

---

# Current Next Step

After this README is established, create:

```text
CURRENT_STATE.md
```

That file will define the exact current truth of the repository and prevent this README's long-term architecture from being confused with functionality that already exists.

---

**OXYCOK Commerce**

Build from evidence.  
Preserve what matters.  
Automate what earns authority.  
Make every legitimate failure improve the system.