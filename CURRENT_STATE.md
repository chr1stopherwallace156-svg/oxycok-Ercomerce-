# OXYCOK Commerce — Current State

> Canonical snapshot of what is actually implemented, what is planned, what is authoritative, and what should happen next.

---

## 1. Purpose of This File

`CURRENT_STATE.md` exists to prevent architectural intent from being confused with implemented reality.

The repository may contain:

- plans;
- proposed architecture;
- experiments;
- partially implemented capabilities;
- qualification fixtures;
- future-state documentation.

Their existence does not mean those capabilities are operational.

When determining the current implementation state of OXYCOK Commerce, begin here and then verify the repository itself.

If this file disagrees with executable repository evidence, the executable evidence wins and this file must be corrected.

---

# 2. Current Classification

```text
PROJECT_STAGE = GEN0_FOUNDATION
PRODUCTION_STATUS = NOT_PRODUCTION_READY
AUTONOMY_STATUS = NO_AUTONOMOUS_COMMERCE_AUTHORIZED
SHOPIFY_RUNTIME = NOT_YET_VERIFIED
WEBHOOK_RUNTIME = NOT_YET_VERIFIED
COMMERCE_MEMORY = NOT_YET_IMPLEMENTED
AI_COMMERCE_RUNTIME = NOT_YET_IMPLEMENTED
PROTECTED_MUTATION = NOT_YET_IMPLEMENTED
QUALIFICATION_STATUS = FOUNDATION_PENDING
```

These classifications must not be promoted merely because code has been written.

Promotion requires evidence appropriate to the capability.

---

# 3. Current Repository Truth

At this stage, the repository is being established as the canonical home of the OXYCOK Commerce platform.

The initial repository foundation includes or is in the process of establishing:

- project mission;
- operating doctrine;
- repository-first development;
- evidence-driven engineering;
- explicit authority boundaries;
- progressive automation;
- durability requirements;
- zero-context recovery;
- Shopify as the initial transactional commerce platform.

The repository must remain honest about what has actually been implemented.

---

# 4. What Exists Now

## Repository

The GitHub repository exists and is the intended canonical source of truth for OXYCOK Commerce.

Initial foundational documentation is being created.

## Operating Doctrine

The root `README.md` defines the initial:

- project mission;
- evidence philosophy;
- authority philosophy;
- automation philosophy;
- qualification philosophy;
- durability philosophy;
- high-level commerce architecture.

These are architectural requirements and operating principles.

They are not proof of runtime implementation.

---

# 5. What Does NOT Yet Exist

Unless subsequently proven by repository evidence, the following must currently be treated as **NOT IMPLEMENTED**.

## Shopify Runtime

Not yet established:

- production Shopify GraphQL Admin API client;
- verified Shopify authentication;
- API-version policy;
- product synchronization;
- order synchronization;
- customer synchronization;
- inventory synchronization;
- collection synchronization;
- discount synchronization;
- fulfillment synchronization.

---

## Webhook Runtime

Not yet established:

- production webhook receiver;
- Shopify webhook authenticity verification;
- event normalization;
- event persistence;
- idempotency enforcement;
- duplicate-event protection;
- replay handling;
- retry handling;
- dead-letter handling;
- webhook observability.

---

## Commerce Memory

Not yet established:

- canonical internal commerce history;
- event ledger;
- decision ledger;
- action ledger;
- outcome ledger;
- experiment ledger;
- durable AI observation history.

---

## AI Runtime

No production AI commerce capability is currently authorized.

Not yet established:

- merchandising agent;
- product intelligence agent;
- pricing agent;
- inventory agent;
- marketing agent;
- customer intelligence agent;
- customer support agent;
- operations agent;
- autonomous business controller.

Names appearing in plans or documentation do not imply implementation.

---

## Authority Runtime

Not yet established:

- executable authority registry;
- policy engine;
- capability-specific permissions;
- human approval workflow;
- bounded automation enforcement;
- canonical mutation sink;
- protected production writes.

---

## Qualification Runtime

Not yet established:

- frozen commerce fixtures;
- adversarial qualification suite;
- replay qualification;
- mutation qualification;
- false-positive tracking;
- false-negative tracking;
- authority-boundary attacks;
- clean-checkout qualification.

---

# 6. Current Authority

At Gen0, the default authority policy is:

```text
AI_DEFAULT_AUTHORITY = OBSERVE_ONLY
PRODUCTION_MUTATION = PROHIBITED_UNLESS_EXPLICITLY_IMPLEMENTED_AND_AUTHORIZED
AUTONOMOUS_PRICING = PROHIBITED
AUTONOMOUS_REFUNDS = PROHIBITED
AUTONOMOUS_DISCOUNTS = PROHIBITED
AUTONOMOUS_CUSTOMER_MESSAGING = PROHIBITED
AUTONOMOUS_AD_SPEND = PROHIBITED
AUTONOMOUS_INVENTORY_PURCHASING = PROHIBITED
```

This is intentionally conservative.

Automation authority will be earned capability by capability.

---

# 7. Initial Source-of-Truth Model

The initial intended truth hierarchy is:

```text
SHOPIFY
    │
    ├── transactional commerce truth
    │
    ▼
OXYCOK EVENT + MEMORY LAYER
    │
    ├── historical truth
    ├── observations
    ├── decisions
    ├── experiments
    └── outcomes
    │
    ▼
AI CAPABILITIES
    │
    ├── interpretation
    ├── recommendation
    └── candidates
    │
    ▼
AUTHORITY + POLICY
    │
    ▼
CONTROLLED ACTION
```

AI-generated interpretation does not automatically become transactional truth.

---

# 8. Canonical External Platform

Initial commerce platform:

```text
PLATFORM = SHOPIFY
PRIMARY_ADMIN_INTERFACE = SHOPIFY_GRAPHQL_ADMIN_API
EVENT_INTERFACE = SHOPIFY_WEBHOOKS
```

Shopify API contracts must be verified against the API version actually used by the implementation.

Do not hard-code assumptions from stale documentation.

---

# 9. Initial Engineering Objective

The immediate engineering objective is **not**:

> Build every AI agent.

It is:

> Establish a trustworthy commerce backbone upon which increasingly capable AI systems can operate.

That backbone requires:

```text
SHOPIFY
   ↓
VERIFIED CONNECTIVITY
   ↓
WEBHOOK INGESTION
   ↓
EVENT IDENTITY
   ↓
DURABLE STORAGE
   ↓
COMMERCE MEMORY
   ↓
OBSERVABILITY
   ↓
FIRST BOUNDED AI CAPABILITY
   ↓
CONTROLLED ACTION
   ↓
RESULT RECEIPT
   ↓
OUTCOME MEASUREMENT
```

---

# 10. Gen0 Foundation Work

The initial foundation should establish the following durable files.

```text
README.md
CURRENT_STATE.md
ROADMAP.md
CHANGELOG.md

doctrine/
    OPERATING_CONSTITUTION.md
    AUTHORITY_MODEL.md
    EVIDENCE_MODEL.md
    FAILURE_POLICY.md
    AI_AGENT_RULES.md

handoff/
    ZERO_CONTEXT_ENTRY.md
    CURRENT_HANDOFF.md
```

Additional directories should be created when their implementation responsibilities become real.

Do not create architecture merely to make the repository appear mature.

---

# 11. Gen1 Target

The first runtime milestone should prove basic Shopify connectivity.

Required evidence should eventually include:

```text
configuration loads
        ↓
credentials remain outside Git
        ↓
Shopify authentication succeeds
        ↓
GraphQL request succeeds
        ↓
known shop data is returned
        ↓
errors are deterministic
        ↓
API version is explicit
        ↓
test/verification command exists
```

Proposed classification after successful qualification:

```text
SHOPIFY_CONNECTIVITY = VERIFIED
```

That classification must not be used before evidence exists.

---

# 12. Gen2 Target

Establish webhook ingestion.

Minimum concerns:

- authenticity;
- identity;
- normalization;
- persistence;
- duplicate delivery;
- retries;
- replay;
- failure handling.

A webhook endpoint that merely returns HTTP 200 is not sufficient.

---

# 13. Gen3 Target

Establish durable commerce memory.

The system should begin distinguishing:

```text
CURRENT STATE

EVENT HISTORY

OBSERVATIONS

INTERPRETATIONS

DECISIONS

ACTION CANDIDATES

APPROVALS

EXECUTED ACTIONS

RESULT RECEIPTS

OUTCOMES

EXPERIMENTS
```

These categories must not collapse into one undifferentiated AI memory store.

---

# 14. Gen4 Target

Implement the first bounded AI capability.

The first capability should be deliberately narrow.

It should demonstrate the architecture rather than maximize feature count.

Preferred characteristics:

- useful;
- measurable;
- reversible or low-risk;
- supported by strong evidence;
- easy to review;
- capable of producing a clear outcome.

The first capability should initially operate without autonomous production mutation.

---

# 15. Gen5 Target

Introduce controlled production action.

Required conceptual path:

```text
OBSERVATION
    ↓
ANALYSIS
    ↓
ACTION CANDIDATE
    ↓
VALIDATION
    ↓
POLICY
    ↓
AUTHORITY
    ↓
APPROVAL
    ↓
MUTATION SINK
    ↓
SHOPIFY
    ↓
RECEIPT
```

No AI agent should bypass this path merely because it possesses Shopify credentials.

---

# 16. Gen6+ Direction

Only after real workflows expose the need should the system expand into broader autonomous commerce.

Potential future capabilities include:

- product optimization;
- merchandising;
- pricing experiments;
- inventory forecasting;
- lifecycle marketing;
- customer segmentation;
- support assistance;
- SEO;
- promotion optimization;
- conversion analysis;
- anomaly detection;
- operational planning.

These are not current implementation claims.

---

# 17. Known Architectural Risks

The following risks should be expected from the beginning.

## Duplicate Events

Shopify or infrastructure may deliver the same logical event more than once.

The system must not assume:

```text
one delivery = one business event
```

---

## Event Ordering

Events may not always be processed in the intuitive business order.

Later state must not be overwritten blindly by stale events.

---

## API Failure

Shopify or another dependency may:

- timeout;
- reject requests;
- rate limit;
- return partial failures;
- change available API behavior.

Failure handling must be explicit.

---

## AI Hallucination

AI output is not authoritative commerce state.

Claims requiring factual store state should be grounded in actual commerce data.

---

## Authority Leakage

A component designed for recommendation must not accidentally gain mutation capability.

---

## Prompt Injection

External content may eventually contain instructions designed to manipulate AI behavior.

Untrusted commerce/customer/content data must not silently override system authority.

---

## Stale State

An action may be valid when proposed but invalid by execution time.

High-impact actions may require state revalidation before mutation.

---

## Retry Amplification

Retries must not multiply:

- refunds;
- discounts;
- messages;
- inventory changes;
- fulfillment actions;
- API mutations.

---

## Silent Partial Success

Multi-step operations must not report complete success when only part of the operation succeeded.

---

## Configuration Drift

Development, staging, and production behavior must not silently diverge.

---

# 18. Security State

Current rule:

```text
NO SECRETS IN GIT
```

Never commit:

```text
SHOPIFY_ADMIN_ACCESS_TOKEN
SHOPIFY_API_SECRET
SHOPIFY_WEBHOOK_SECRET
DATABASE_PASSWORD
OPENAI_API_KEY
PRIVATE_KEYS
SERVICE_ACCOUNT_CREDENTIALS
```

A future `.env.example` may document required variable names, but it must contain placeholders only.

---

# 19. Data Responsibility

Customer and order data should be treated as sensitive business data.

The architecture should minimize unnecessary propagation of:

- names;
- email addresses;
- phone numbers;
- addresses;
- payment-related information;
- order histories;
- customer notes.

AI components should receive only the information required for their declared function.

---

# 20. Git State Doctrine

Before significant implementation work:

1. inspect repository state;
2. understand existing files;
3. preserve prior work;
4. avoid destructive replacement without evidence;
5. make bounded changes;
6. run applicable validation;
7. review the diff;
8. commit intentionally;
9. push;
10. verify remote state.

---

# 21. No Silent Destruction

Agents and scripts must not casually:

- delete databases;
- reset canonical state;
- overwrite ledgers;
- remove unknown files;
- force-push protected history;
- regenerate authoritative artifacts destructively.

Destructive operations require explicit justification and appropriate authorization.

---

# 22. Repeated-Prompt Detection

As development proceeds, repeated owner instructions should be captured.

Examples:

```text
"Check Shopify before answering."
"Don't change production automatically."
"Verify the webhook."
"Make sure everything is pushed."
"Don't lose the previous version."
"Test it against something different."
```

Repeated instructions are candidates for conversion into:

- runtime guards;
- preflight checks;
- repository doctrine;
- tests;
- registries;
- automation;
- handoff requirements.

The owner should not permanently serve as missing middleware.

---

# 23. Current Qualification Rule

At the present stage:

```text
DOCUMENTED ≠ IMPLEMENTED

IMPLEMENTED ≠ TESTED

TESTED ≠ QUALIFIED

QUALIFIED ≠ AUTONOMOUS

AUTONOMOUS ≠ UNIVERSALLY SAFE
```

These distinctions must remain visible throughout development.

---

# 24. Current Definition of Success

The Gen0 foundation succeeds when a zero-context engineer or AI agent can enter the repository and determine:

- what OXYCOK Commerce is;
- what currently exists;
- what does not exist;
- what the architectural principles are;
- what authority AI currently possesses;
- what the next milestone is;
- what must not be done;
- where future durable knowledge belongs.

---

# 25. Current Next Actions

The current sequence is:

```text
1. README.md
      ↓
2. CURRENT_STATE.md
      ↓
3. ROADMAP.md
      ↓
4. doctrine/OPERATING_CONSTITUTION.md
      ↓
5. doctrine/AUTHORITY_MODEL.md
      ↓
6. doctrine/EVIDENCE_MODEL.md
      ↓
7. doctrine/AI_AGENT_RULES.md
      ↓
8. doctrine/FAILURE_POLICY.md
      ↓
9. handoff/ZERO_CONTEXT_ENTRY.md
      ↓
10. Initial executable backend
      ↓
11. Shopify GraphQL connectivity
      ↓
12. Webhook ingestion
```

Do not skip directly to broad autonomous AI agents.

---

# 26. Next Exact Action

After committing this file:

```text
CREATE ROADMAP.md
```

The roadmap should convert the architectural destination into explicit implementation gates so that future agents cannot confuse activity with progress.

---

# 27. Current State Summary

```text
REPOSITORY
    = ESTABLISHED

DOCTRINE
    = FOUNDATION_IN_PROGRESS

SHOPIFY
    = PLANNED / NOT_RUNTIME_VERIFIED

WEBHOOKS
    = PLANNED / NOT_RUNTIME_VERIFIED

DATABASE
    = NOT_SELECTED / NOT_IMPLEMENTED

COMMERCE_MEMORY
    = NOT_IMPLEMENTED

AI CAPABILITIES
    = NOT_IMPLEMENTED

PRODUCTION AI AUTHORITY
    = NONE

QUALIFICATION
    = FOUNDATION_PENDING

CURRENT PRIORITY
    = BUILD DURABLE FOUNDATION THEN SHOPIFY BACKBONE
```

---

## State Integrity Rule

Whenever implementation materially changes repository truth, this file must be evaluated for update.

A stale `CURRENT_STATE.md` is itself a repository defect.

---

**Last established stage:** Gen0 Foundation  
**Next exact artifact:** `ROADMAP.md`