# OXYCOK Dataset Authority Doctrine

## Core Rule

DATA AVAILABILITY != DATA AUTHORITY

A public dataset may prove that an algorithm or pipeline works.

It does not prove that the resulting behavior applies to OXYCOK customers.

---

## Dataset Classes

### CLASS A — FIRST_PARTY_TRUTH

OXYCOK Shopify and validated first-party behavioral data.

Eligible for:

- production hypothesis generation;
- local model training;
- business evaluation;
- qualified decision support.

Subject to instrumentation, identity, leakage and quality gates.

---

### CLASS B — INDUSTRY_RESEARCH_FIXTURE

Examples:

- Alibaba/Taobao official datasets;
- JDsearch;
- Criteo datasets.

Eligible for:

- architecture qualification;
- model reproduction;
- algorithm comparison;
- scale testing;
- failure discovery;
- benchmark testing.

Not sufficient alone for OXYCOK production promotion.

---

### CLASS C — CROSS_DOMAIN_FIXTURE

Examples:

Amazon recommendation datasets.

Eligible for:

- generalization testing;
- cold-start experiments;
- pipeline testing;
- robustness challenges.

No OXYCOK business authority.

---

### CLASS D — UNVERIFIED_MIRROR

Examples:

unverified Tmall or AliExpress mirrors.

State:

QUARANTINED

Required before use:

- provenance;
- exact dataset identity;
- source;
- license/terms;
- schema;
- hash;
- publication linkage.

---

## Dataset Promotion

DISCOVERED
↓
IDENTITY_VERIFIED
↓
PROVENANCE_VERIFIED
↓
USAGE_TERMS_RECORDED
↓
SCHEMA_PROFILED
↓
QUALITY_PROFILED
↓
PURPOSE_ASSIGNED
↓
FROZEN
↓
EXPERIMENT_ELIGIBLE

There is no automatic path from external dataset to
FIRST_PARTY_TRUTH.