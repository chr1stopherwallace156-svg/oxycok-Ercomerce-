#!/usr/bin/env python3
"""Invoke the actual pinned Elektron B3B owner, never a replacement classifier."""
import argparse
import json
import re
from pathlib import Path
import sys

from snapshot import verify, outside, PUBLIC_ROOT

SOURCE_REPOSITORY = "chr1stopherwallace156-svg/oxyballs-Industrial"
SOURCE_COMMIT = "f2573f95bfa988e358d89d4180a783059b70a21d"
SOURCE_TREE = "17b5b46ee47e21001d0024263867d23311173c86"


class CoreResultError(ValueError):
    def __init__(self, reason, result):
        super().__init__(reason)
        self.source_result = result


def require_usable_core_result(result):
    item = result.get("work_item") or {}
    if (result.get("admitted") is not True or item.get("current_stage") not in
            {"REVIEW_PENDING_INDEPENDENT", "COMPLETE"} or item.get("last_error")
            or item.get("failed_stages")):
        raise CoreResultError("ELEKTRON_OWNER_DID_NOT_REACH_VALID_REVIEW_BOUNDARY", result)
    return result


def known_failures(snapshot):
    root = Path(snapshot)
    directory = root / "docs/doctrine/failure_learning/learning_records"
    files = sorted(directory.glob("RFL-*.json"))
    if not files:
        raise ValueError("KNOWN_FAILURE_CORPUS_MISSING")
    records = []
    for path in files:
        row = json.loads(path.read_text())
        records.append({
            "source_record": path.relative_to(root).as_posix(),
            "id": row.get("RFL_ID") or row.get("document_id") or row.get("analysis_id"),
            "failure_class": row.get("FAILURE_CLASS", "NOT_ESTABLISHED"),
            "mechanism": row.get("root_mechanism", "NOT_ESTABLISHED"),
            "hard_negatives": row.get("hard_negatives", []),
            "claim": "REFERENCE_LESSON_NOT_AUTOMATIC_TARGET_FACT_OR_REGRESSION",
        })
    return records


def failure_preflight(event, records):
    """Candidate destination bindings of preserved mechanisms; not source qualification."""
    available = {re.search(r"RFL-\d{4}-\d{3}", row["source_record"]).group(0) for row in records
                 if re.search(r"RFL-\d{4}-\d{3}", row["source_record"])}
    required = {"RFL-2026-022", "RFL-2026-024", "RFL-2026-028", "RFL-2026-032"}
    if not required <= available:
        raise ValueError("FAILURE_BINDING_CORPUS_INCOMPLETE")
    facts = event.get("payload") or {}
    blockers = []
    if (facts.get("current_subject") and facts.get("exam_subject")
            and facts["current_subject"] != facts["exam_subject"]):
        blockers.append({"lesson":"RFL-2026-022", "reason":"EXAM_SUBJECT_DIFFERS_FROM_CURRENT"})
    if facts.get("production_mode") is True and facts.get("exam_override_active") is True:
        blockers.append({"lesson":"RFL-2026-024", "reason":"EXAM_CONTROL_ESCAPED_INTO_PRODUCTION"})
    if (facts.get("evidence_produced") is True
            and facts.get("consumer_semantic_effect_observed") is False):
        blockers.append({"lesson":"RFL-2026-028", "reason":"PRODUCED_EVIDENCE_NOT_CONSUMED"})
    count = facts.get("fresh_same_family_failures")
    if isinstance(count, int) and not isinstance(count, bool) and count >= 2 and not facts.get("frozen_effect_surface_ref"):
        blockers.append({"lesson":"RFL-2026-032", "reason":"SYSTEMIC_SURFACE_REQUIRED_BEFORE_CLOSURE_REPAIR"})
    return {"authority":"NONE", "bindings":"DESTINATION_CANDIDATES_NOT_IMPORTED_QUALIFICATION",
            "fact_basis":"CALLER_DECLARED_NOT_INDEPENDENTLY_VERIFIED",
            "blockers":blockers, "reference_record_count":len(records),
            "untriggered_rules":"NOT_TRIGGERED_OR_MISSING_CONTEXT_NEVER_A_PASS"}


def execute(snapshot, state_root, event, allow_bounded=False):
    snapshot = Path(snapshot).resolve(strict=True)
    state = Path(state_root).resolve()
    if not outside(state, snapshot) or not outside(state, PUBLIC_ROOT):
        raise ValueError("STATE_MUST_BE_SEPARATE_PRIVATE_RUNTIME_ROOT")
    manifest = verify(snapshot, allow_bounded)
    if (manifest.get("repository") != SOURCE_REPOSITORY or manifest["commit"] != SOURCE_COMMIT
            or manifest.get("source_tree") != SOURCE_TREE):
        raise ValueError("UNREVIEWED_SOURCE_PROFILE")
    if not isinstance(event, dict):
        raise ValueError("TYPED_EVENT_REQUIRED")
    records = known_failures(snapshot)
    preflight = failure_preflight(event, records)
    if preflight["blockers"]:
        raise ValueError("KNOWN_FAILURE_PROTECTION_BLOCKED:" + json.dumps(preflight["blockers"]))
    # Keep imports and operational state in a separate process. The CLI caller
    # sets PYTHONDONTWRITEBYTECODE so importing cannot add caches to the snapshot.
    sys.dont_write_bytecode = True
    sys.path[:0] = [str(snapshot), str(snapshot / "scripts")]
    from scripts.ai_worker_observatory.supervisor import B3BRuntimeSupervisor
    owner = B3BRuntimeSupervisor(
        state_root=state / "operational",
        observations_dir=state / "observations",
        metrics_dir=state / "metrics",
        classifications_dir=state / "classifications",
        reviews_dir=state / "reviews",
        index_path=state / "indexes/observations.json",
        rebuild_indexes=False,
        require_independent_review=True,
    )
    result = owner.run_pipeline_for_event(event, capture_mode="QUALIFICATION")
    require_usable_core_result(result)
    # Any incidental mutation of the copied source is a failed transfer boundary.
    verify(snapshot, allow_bounded)
    return {"authority": "NONE", "scope": manifest["scope"],
            "source_commit": manifest["commit"],
            "actual_owner": "scripts.ai_worker_observatory.supervisor.B3BRuntimeSupervisor",
            "source_result": result, "failure_preflight":preflight,
            "destination_qualification": "NOT_ESTABLISHED",
            "known_failure_record_count": len(records),
            "qualification_note": "Observed/ measured/ classified is not independent review or experiment qualification."}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--snapshot", required=True)
    p.add_argument("--state-root")
    p.add_argument("--event")
    p.add_argument("--allow-bounded-analysis", action="store_true")
    p.add_argument("--list-known-failures", action="store_true")
    args = p.parse_args()
    try:
        if args.list_known_failures:
            verify(args.snapshot, args.allow_bounded_analysis)
            result = {"authority": "NONE", "records": known_failures(args.snapshot)}
        else:
            if not args.state_root or not args.event:
                raise ValueError("STATE_AND_EVENT_REQUIRED")
            with Path(args.event).open() as f:
                event = json.load(f)
            result = execute(args.snapshot, args.state_root, event, args.allow_bounded_analysis)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (ValueError, OSError, KeyError, ImportError) as exc:
        print(json.dumps({"status": "BLOCKED", "authority": "NONE", "error": str(exc),
                          "source_result": getattr(exc, "source_result", None)}),
              file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
