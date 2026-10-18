# Reuse Elektron in OXYCOK — executable transfer boundary v1

The owner requires existing Elektron software, B3B, failure knowledge, positive
methods and learned protections to benefit every new reference/domain task in
OXYCOK. This is more than copying doctrine or writing another small substitute.
Industrial remains strictly read-only.

## What is now implemented

1. A read-only Git snapshot materializer for a local authorized source checkout.
   It reads one exact commit with Git tree/blob commands, writes to a new private
   destination outside the source and public OXYCOK project, and verifies every
   tracked blob plus the complete Git tree. It does not checkout/reset/clean/
   fetch/push, alter the source index, copy dirty/untracked files, or rewrite refs.
2. A real-owner adapter for the pinned B3BRuntimeSupervisor. It imports the
   materialized source owner, directs corpus/output state to separate paths and
   preserves its independent-review gate. It is not a replacement B3B classifier.
3. A configured standard entrypoint, scripts/oxycok.py, that requires the private
   Elektron snapshot and automatically selects it for each new mission. When selected,
   OXYCOK invokes the actual core before static inspection, records the result as
   a mission artifact, and adds a graph edge. Missing/failed core blocks; there is
   no silent fallback to the earlier standalone path.
4. Access to the copied main-tree failure corpus: 39 records in the observed
   analysis package. Four explicit candidate destination bindings use declared
   facts to block stale exam subjects, exam-to-production configuration escape,
   evidence nonconsumption and repeated local repair without an effect surface.

These four bindings are not a claim that every source record has already become
an executable destination guard. Missing facts are not a PASS, and unknown/new
families are not forced into known labels. Source qualification and canonical
claim ceilings remain historical source facts, not destination qualification.

## Full transfer versus the real probe

The selected Industrial main tree contains 9,233 tracked files and 673,221,796
bytes, including runtime code, data, tests, evidence, UI and archives. The
materializer accounts for all tracked files in that exact tree; it never silently
drops an inconvenient file. Unsupported symlink/submodule modes or budget
exhaustion block staging rather than pretending completeness.

The full 673 MB snapshot has NOT been materialized in this session: the host has
connector reads, not an authenticated local checkout of the source Git database.
The real execution proof instead used a private, explicitly bounded analysis
copy of 70 exact Python source files and 64 exact data files. Every source/data
blob was checked against its original Git blob identity before execution.
The bounded copy requires --allow-bounded-analysis and cannot pass default
full-transfer verification. No raw private source code is published in OXYCOK.

OWNER_TRANSFER_MAP_V1.json inventories principal software owners. Whole-tree
materialization makes their files available; it does not make all of them active
or requalified. ACI, RLR, ETR, Proving Ground, Failure Trap, System Continuity and
other owners still require owner-specific destination integration and tests.
Newer unmerged source branches need separately pinned snapshots and lineage
review. One main-tree snapshot is not all branches, stashes or Git history.

## Real failure, repair and successor

The first composed probe reached B3B DEAD_LETTER: OXYCOK supplied a raw hash as
mission_id, which violated the existing IDENTIFIER grammar. The bridge returned
the object without checking that stage, so the outer study mission completed.
That false-green composition result is preserved in
evidence/ACTUAL_B3B_MISSION_FAIL_ATTEMPT_001.json (and its original V1 record).

Destination repair only:
- namespace source-facing mission/target IDs with an alphabetic prefix while
  retaining the complete original identity;
- reject nonadmission, DEAD_LETTER, unexpected stages, failed stages and errors;
- retain the original source result in the typed bridge diagnostic;
- add identifier-boundary and dead-letter negative controls.

The original Industrial files were not patched. The repaired real-owner probe
completed OXYCOK's bounded study workflow while B3B correctly remained
REVIEW_PENDING_INDEPENDENT after OBSERVED, MEASURED and CLASSIFIED. Its next
review/experiment stages were not self-certified. Earlier red evidence remains
separate from this successor. See the V3 final successor evidence, preserved V2 and learning record.

## Apply already-known failures to new work

Reference failure records are loaded before dispatch. Current bindings:
- RFL-2026-022: current_subject differs from exam_subject → block.
- RFL-2026-024: production_mode with exam_override_active → block.
- RFL-2026-028: evidence_produced without consumer_semantic_effect_observed → block.
- RFL-2026-032: two or more fresh same-family failures without a frozen effect
  surface reference → block another closure repair.

Facts are caller-declared; these adapters do not independently prove the facts.
A nontriggered guard is NOT_TRIGGERED_OR_MISSING_CONTEXT_NEVER_A_PASS.
No exact originating fixture answer or repository name is necessary for the
mechanism to apply. Tests include unfamiliar-domain identities and a one-off
negative case that must not activate systemic-repair escalation.

This is the first concrete set of bindings, not all 39 records integrated into
every worker. Future bindings must use the existing legitimate owners and
preserve applicability, exclusions, uncertainty and authority. Merely loading
or counting a lesson is not proof of semantic use.

## Stage on a machine with the source checkout

Keep the destination private and outside both Git repositories:
```bash
python3 scripts/elektron_bridge/snapshot.py stage --source-checkout /absolute/path/to/oxyballs-Industrial --commit f2573f95bfa988e358d89d4180a783059b70a21d --repository chr1stopherwallace156-svg/oxyballs-Industrial --destination /absolute/private/path/elektron-snapshot
python3 scripts/elektron_bridge/snapshot.py verify --snapshot /absolute/private/path/elektron-snapshot
```

The default size budget is 1 GB. Staging may be expensive. All source bytes are
read from immutable Git objects, so an existing dirty working tree is preserved.
The destination is create-only. A failed partial copy is preserved for inspection;
it is never called a complete snapshot and is never silently erased.

Example mission selection:
```bash
python3 scripts/mission/runtime.py --state-root /absolute/private/path/oxycok-state start --target /absolute/path/to/owned-target --provider python --domain new-software-domain --mechanism evidence-consumption --elektron-snapshot /absolute/private/path/elektron-snapshot
```

Then use the existing step/run/status/events/graph commands. Operational state
and B3B outputs stay separate from the source snapshot. Snapshot verification
checks bytes and declared executable modes before/after invocation. The pinned
source profile also checks the expected full source tree. The bounded analysis
mode deliberately does not establish full-tree transfer.

The bridge executes trusted owner-selected source code with the user's process
permissions; it is not a security sandbox. Environment/dependency portability and
other owner activation surfaces remain unqualified. The source is not given
new production authority and no protected record is promoted by this adapter.

## Current qualification

Tests prove read-only snapshot behavior on real synthetic Git repositories,
including dirty-source preservation, hidden tracked files, full-tree identity,
size/overlap/overwrite controls, corruption/mode drift and incomplete-copy
rejection. These fixture tests are not represented as an executed full Industrial
snapshot. The separate B3B evidence is an actual source-owner execution.
Independent destination qualification and full-core activation remain open.

## Standard OXYCOK entrypoint

Configure once using private absolute paths outside this public checkout:

```sh
python3 -B scripts/oxycok.py --config /private/oxycok/config.json configure --snapshot /private/elektron-snapshot --state-root /private/oxycok/state
python3 -B scripts/oxycok.py --config /private/oxycok/config.json start --target /owned/target --provider python --domain your-domain --mechanism evidence-consumption --fact artifact-produced --fact downstream-consumer
python3 -B scripts/oxycok.py --config /private/oxycok/config.json run --mission-id RETURNED_ID --max-steps 6
```

The bounded analysis package additionally requires explicit --allow-bounded-analysis
at configuration; full snapshot verification is the default. Missing configuration
blocks. Configuration overrides through mission arguments block. The lower-level
mission CLI remains a standalone diagnostic, and does not imply core inheritance.
The V4 frontdoor probe preserves the actual core's REVIEW_PENDING_INDEPENDENT
result even when the bounded outer mission completes.
