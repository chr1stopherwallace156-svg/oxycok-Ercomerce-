# Universal reconstruction method v1

The owner wants OXYCOK to learn a reference system's underlying engineering
patterns and build an implementation of its own, with REA as the first subject.
Using upstream as a library, pasting its source, or renaming the same code is
not the requested product. MIT licensing is not a reason to substitute those
activities for reconstruction.

## Invariant method; parameterized subject

PROTOCOL_V1.json defines the method. scripts/reconstruction/campaign.py generates
the campaign template for an arbitrary domain and capability list.
REA-specific data lives only under subjects/rea. The protocol and auditor do not
import REA, invoke its CLI, assume a programming language, or depend on Industrial.
Industrial remains a read-only methodology/evidence reference.

| Stable infrastructure | Subject-specific parameters |
| --- | --- |
| Evidence custody and exact subject identity | Repository, revision, files, formats and dependencies |
| Source and requirement coverage accounting | Capability universe and declared exclusions |
| Mechanism extraction and negative-case discipline | Actual source behavior, implementation and failure paths |
| Typed ownership/data/state/effect graphs | Components, consumers, interfaces and state transitions |
| Abstract behavioral contracts | Inputs, outputs, invariants, failure modes and measurements |
| Original design and isolated implementation | Target language, architecture, storage and worker choices |
| Hostile qualification and immutable red history | Broken controls, unfamiliar holdouts and actual runtime subjects |
| Learning, inheritance and resumable handoff | Positive methods, exceptions, unknowns and next work |

The intended loop is: reference evidence → explanatory model → abstract behavior
contract → original design → new implementation → hostile examination →
independent qualification → reusable learning → continued mission.

This is not a source-to-source translator. The existing mission runtime remains
the owner of bounded execution and durable evidence; the campaign owns
long-horizon reconstruction scope and worker records. Campaign evidence_refs can
identify mission artifacts. A campaign is not an alternative authority registry.

## Understand mechanisms, not just vocabulary

For every important capability, recover:
- problem and observable behavior;
- owner, dependencies, consumer path and data representation;
- lifecycle, persistence, recovery, concurrency and authority;
- why an implementation choice works and its alternatives;
- failures, repairs, negative cases, boundaries and remaining unknowns;
- the difference between a recorded artifact and an actual consumer effect.

Then specify the target in behavior terms and choose the destination design
deliberately. Do not carry source structure, naming, comments or expression by
default. Do not claim independence merely because identifiers or wording differ.
If any third-party code is reused, record it as reuse with the applicable
license/notice obligations rather than calling it newly authored code.

Universal here means a reusable procedure, records and interfaces across
domains. It does not mean that every domain has already been understood or that
all implementations have the same architecture.

## Exact claims that must remain separate

ENUMERATED ≠ CONTENT_READ ≠ MECHANISM_ANALYZED ≠ BEHAVIOR_CONTRACTED.
ORIGINAL_DESIGN_AUTHORED ≠ IMPLEMENTED ≠ EXECUTED ≠ INDEPENDENTLY_QUALIFIED.
INDEPENDENTLY_QUALIFIED ≠ AUTHORIZED.
SIMILARITY ≠ EQUIVALENCE. A shared mechanism requires applicability and exclusions.

These are distinct evidence claims, not a promise that one automatically
produces the next. Both failure-derived and successful methods require future
consumer inheritance tests. A reference repository's PASS does not qualify the
destination's different implementation.

## Whole-source coverage

REA's pinned recursive Git tree is preserved in subjects/rea/CENSUS_V1.json:
4,340 file entries, 367 tree entries and five submodule references, 4,712 entries
in total. The upstream response was not truncated. The census contains paths,
modes and object identities, not copied implementation bodies.

The declared review universe has 4,345 non-directory units. Submodule references
do not include their contents; each needs a nested pinned campaign or an explicit
blocked/exclusion disposition. Generated/vendor/site/assets files also need
explicit scope decisions; they must not silently disappear from the count.

Each review binds its exact source object and states ANALYZED,
EXCLUDED_WITH_BASIS or BLOCKED with evidence references and rationale.
Missing reviews remain pending. Six earlier source readings have worker
dispositions; they do not establish full-source reconstruction.

The initial 15 capability objectives are a study outline, not an exhaustive
verified capability graph. Their architecture-document anchors are navigation,
not proof that all owning code and tests are mapped. All target behavior/design,
implementation and qualification requirements remain open.

## Structural audit, not semantic certification

The auditor checks pinned scope, nontruncated inventory, exact review bindings,
submodule disposition, capability contracts, original-design fields, candidate
identity, graphs, lessons and required qualification records. It blocks silent
scope reduction, stale review identity and qualification-label promotion.

It does not fetch or interpret source content, authenticate arbitrary evidence
references, independently execute source/target tests, prove authorship, or
decide legal rights. Its strongest result is
WORKER_RECORDS_READY_FOR_INDEPENDENT_REVIEW; it never grants independent
qualification or universal semantic understanding. Worker records require
independent challenge against the actual cited evidence.

Renaming or paraphrasing is not an originality test. The U.S. Copyright Office
distinguishes functional ideas/methods from protected expression:
https://www.copyright.gov/register/tx-programs.html
An original implementation can itself carry copyright. Rights compliance and
provenance remain separate from technical reconstruction.

## Run and reuse

Audit the real REA campaign:
```bash
python3 scripts/reconstruction/campaign.py --census reconstruction/subjects/rea/CENSUS_V1.json audit --campaign reconstruction/subjects/rea/CAMPAIGN_V1.json
```

For another authorized reference, create a PINNED_REPOSITORY_CENSUS from its
complete Git tree using the same schema, then generate a new campaign:
```bash
python3 scripts/reconstruction/campaign.py --census /path/to/other-census.json new --domain another-software-domain --capability "First observable capability" --capability "Second observable capability" --output /path/to/new-campaign.json
```

Audit exits 3 while reconstruction is open, 2 for invalid data, and 0 only when
worker records are ready for independent review. Exit 0 still grants no qualification.
New refuses to overwrite a campaign. Its initialized fields remain explicitly
incomplete. Neither command reconstructs a program automatically.

## Current result and next work

The REA campaign is RECONSTRUCTION_OPEN, with 4,339 pending units, four blocked
by incomplete analysis and two carrying earlier worker analysis. This is a
whole-tree accounting baseline, not a claim to have read all 4,340 files.
The earlier external REA host failure remains preserved; this universal
source-study layer does not require running REA to begin source analysis.

Next: perform complete source/effect-path reviews family by family, replace the
navigation-only capability outline with evidence-bound contracts and graphs,
freeze a bounded target capability's behavioral exam, then author and execute
that original implementation. Preserve all earlier subjects and compare the new
target against independent expectations rather than simply changing source
names. Whole-system reconstruction and general implementation generation remain
open.
