# REA reference and Industrial qualification review

REA is now resolved: https://github.com/morluto/rea — Reverse Engineer Anything.
Reference commit: c12d9eda87aa5a022ee7e18ea96d8d03bfd12e96.
Installed tool probe: rea-agents 6.7.0, registry integrity in SOURCE_PINS_V1.json.
A matching package version does not prove package bytes equal the inspected Git commit.

## Scope and custody

Read-only review of selected architecture, contracts, tests, and historical
qualification receipts. This is not a complete REA or Industrial audit.
Industrial source subject: f2573f95bfa988e358d89d4180a783059b70a21d.
No Industrial mutations and no raw private source documents are published.
Source paths and full blob identities survive in SOURCE_PINS_V1.json.
Recorded source test counts are historical reported evidence; those source suites
were not rerun here and their passes do not qualify OXYCOK.

## What REA actually provides

REA separates CLI/MCP entrypoints, shared application workflows, session/provider
selection, evidence/unknown records, pure domain representations, and external
inspection tools. Supported surfaces are much broader than this OXYCOK increment.
Its agent consumes tool findings to investigate or construct an implementation;
the inspection tool itself is not a general independent application author.

The current adapter invokes one fixed static JavaScript directory analysis
command through a caller-supplied, version-checked REA executable. OXYCOK neither
copies REA's implementation nor pretends to reproduce its native/binary,
browser, managed-code, Android or other provider families.

## Patterns recovered from Industrial

| Source evidence | Pattern | Concrete OXYCOK implementation |
| --- | --- | --- |
| ETR task runtime | Method is infrastructure; domain/source are parameters | One coordinator binds inspection, abstraction, construction, testing and recording |
| Failure Trap hostile tests | Preserve failure identity; duplicate admission and restart must be explicit | Mission IDs, unique admission, persistent stages, terminal red events and distinct successor attempts |
| Method-transfer tests | False analogy and authority limits survive formalization | Existing hard negatives and scoped relation candidates retained in the brief |
| Proving Ground qualifier | Bounded operations, stops, context and honest environment status matter | Fixed provider commands, time/output/step budgets, no arbitrary target execution, no fallback success |
| B3B.1 FAIL attempt 1 | Test execution can mutate the subject and invalidate pristine qualification | State kept outside target; target and implementation identity checked before each step |
| B3B.1 attempt 2 PASS, later stale | A pass stays valid only for its exact subject/envelope | Changed target or runtime blocks unfinished continuation; failed attempts remain retained |
| B3B full continuous receipt | One supervisor can compose stages, persist identity and resume across processes | One mission runtime with separately callable stages; no background daemon required |
| Same continuous receipt limits | Continuous workflow is not 24/7 supervision, blanket capture or authority | Bounded run/step with explicit restart; authority NONE; no host-supervision claim |

The historical continuous receipt reports 24 hostile tests, a 100-iteration
soak and fresh-process resume for its sealed subject. It explicitly excludes
HOST_SUPERVISION_24_7. The older FAIL and stale-PASS receipts remain different
historical facts; they are not compressed into a final green result.

## Rights and originality boundary

REA's own LICENSE is MIT, with notice conditions. Its third-party notices identify
separate dependency and external-tool licenses; REA does not grant commercial
tool entitlements. See the pinned upstream LICENSE and THIRD_PARTY_NOTICES.md.
No upstream source code or binaries are vendored into OXYCOK in this change.
The external installation retains its package notices. If source is reused in a
future implementation, preserve applicable licenses and notices and record that
reuse honestly. No transformation can automatically erase third-party rights.

OXYCOK's orchestration, custody store, static Python inspector, target-aware brief
bridge and planner template are project-authored code. The constructor continues
to accept abstract requirements only. Running a licensed external tool is
different from claiming its implementation as newly authored OXYCOK code.

## Actual external result

The real 6.7.0 CLI was invoked on an owned JavaScript fixture, not an unauthorized
target. It exited nonzero. Its process-ownership prerequisite attempted
procps-compatible ps and received: `fatal library error, lookup self`.
REA returned capability_unavailable with partial observations.
The full retained diagnostic, target identity and mission event chain are in
evidence/REA_HOST_FAILURE_V2.json; the first failure remains in V1. This result is RED/ENVIRONMENT_BLOCKED,
not successful provider qualification. No ownership check was bypassed.

OXYCOK's own Python static provider completes the connected mission. Passing its
tests and demonstrating failed-closed REA integration do not establish successful
real REA operation on this host.

## Remaining implementation

The current constructor emits an applicability planner. It does not reconstruct
arbitrary inspected features or establish behavioral equivalence with a target.
The graph is a provenance and syntax-relationship graph, not a complete runtime
call graph. The method corpus is still a seed, not all Industrial knowledge.
Next work must expand authorized adapters and method coverage, resolve the real
REA host prerequisite on a supported host, define feature-level behavioral
contracts, add original implementation workers, and independently qualify them.
