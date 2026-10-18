#!/usr/bin/env python3
"""Domain-parameterized reconstruction campaign and structural coverage audit."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

RELATIONS = {"DEPENDS_ON", "COMPOSES_WITH", "TESTS", "DERIVED_FROM"}
CONTRACT_FIELDS = ("inputs", "outputs", "invariants", "failure_modes",
                   "hard_negatives", "side_effects", "measurements")
DESIGN_FIELDS = ("owner", "original_design", "alternatives", "reuse_boundary")


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def text(value):
    return isinstance(value, str) and bool(value.strip())


def strings(value, nonempty=False):
    return (isinstance(value, list) and (bool(value) or not nonempty)
            and all(text(v) for v in value) and len(set(value)) == len(value))


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True,
        separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def read(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "DUPLICATE_JSON_KEY")
            result[key] = value
        return result
    return json.loads(Path(path).read_text(), object_pairs_hook=unique)


def validate_census(census):
    require(isinstance(census, dict) and census.get("version") == 1
            and census.get("kind") == "PINNED_REPOSITORY_CENSUS", "INVALID_CENSUS")
    require(census.get("upstream_truncated") is False, "TRUNCATED_CENSUS")
    require(text(census.get("repository")), "MISSING_REPOSITORY")
    for key in ("commit", "tree_sha"):
        require(isinstance(census.get(key), str)
                and re.fullmatch("[0-9a-f]{40}", census[key]), "UNPINNED_CENSUS")
    rows = census.get("entries")
    require(isinstance(rows, list) and rows, "EMPTY_CENSUS")
    paths = set()
    for row in rows:
        require(isinstance(row, dict), "INVALID_ENTRY")
        path = row.get("path")
        require(text(path) and not PurePosixPath(path).is_absolute()
                and ".." not in PurePosixPath(path).parts and path not in paths,
                "INVALID_OR_DUPLICATE_PATH")
        paths.add(path)
        require(row.get("type") in ("tree", "blob", "commit"), "UNKNOWN_ENTRY_TYPE")
        require(isinstance(row.get("sha"), str) and re.fullmatch("[0-9a-f]{40}", row["sha"]),
                "INVALID_ENTRY_IDENTITY")
        require(row.get("mode") in ("040000", "100644", "100755", "120000", "160000"),
                "UNSUPPORTED_ENTRY_MODE")
        require((row["type"] == "tree" and row["mode"] == "040000") or
                (row["type"] == "commit" and row["mode"] == "160000") or
                (row["type"] == "blob" and row["mode"] in ("100644", "100755", "120000")),
                "ENTRY_TYPE_MODE_MISMATCH")
    return census


def create(census, domain, capabilities):
    validate_census(census)
    require(text(domain) and strings(capabilities, True), "DOMAIN_AND_CAPABILITIES_REQUIRED")
    return {
        "version": 1, "kind": "ORIGINAL_RECONSTRUCTION_CAMPAIGN",
        "domain": domain, "authority": "NONE",
        "method": "REFERENCE_EVIDENCE_TO_ABSTRACT_REQUIREMENTS_TO_ORIGINAL_DESIGN",
        "reference": {"repository": census["repository"], "commit": census["commit"],
                      "census_sha256": digest(census)},
        "scope": "WHOLE_PINNED_TREE", "file_reviews": {},
        "capabilities": [{
            "id": "CAP-" + str(i + 1).zfill(3), "objective": name,
            "reference_paths": [],
            "contract": {key: [] for key in CONTRACT_FIELDS},
            "design": {key: "" for key in DESIGN_FIELDS},
            "implementation": {"status": "NOT_IMPLEMENTED", "subject_sha256": None,
                               "artifact_refs": []},
            "qualification": {"status": "NOT_RUN", "evidence_refs": [],
                              "broken_control_refs": [], "holdout_refs": []},
        } for i, name in enumerate(capabilities)],
        "graph_edges": [], "lessons": [], "unknowns": [
            "Source understanding is not established by enumeration.",
            "Source tests have not been run by this campaign.",
            "Original implementation and independent target qualification remain open.",
        ],
        "rights": {"source_code_translation": "NOT_A_CONSTRUCTION_METHOD",
                   "legal_clearance": "NOT_ESTABLISHED",
                   "third_party_reuse": "EXPLICITLY_RECORD_LICENSE_AND_ATTRIBUTION"},
    }


def audit(census, campaign):
    validate_census(census)
    require(isinstance(campaign, dict) and campaign.get("version") == 1
            and campaign.get("kind") == "ORIGINAL_RECONSTRUCTION_CAMPAIGN", "INVALID_CAMPAIGN")
    require(campaign.get("authority") == "NONE", "AUTHORITY_ESCALATION")
    require(text(campaign.get("domain")), "DOMAIN_REQUIRED")
    require(campaign.get("reference") == {
        "repository": census["repository"], "commit": census["commit"],
        "census_sha256": digest(census)}, "CENSUS_BINDING_DRIFT")
    require(campaign.get("scope") == "WHOLE_PINNED_TREE", "UNDECLARED_SCOPE_REDUCTION")
    reviews = campaign.get("file_reviews")
    require(isinstance(reviews, dict), "INVALID_REVIEW_REGISTRY")
    leaves = {row["path"]: row for row in census["entries"] if row["type"] != "tree"}
    require(set(reviews) <= set(leaves), "UNKNOWN_REVIEW_PATH")
    pending, excluded, blocked = [], [], []
    for path, source in leaves.items():
        row = reviews.get(path)
        if row is None:
            pending.append(path)
            continue
        require(isinstance(row, dict) and row.get("source_sha") == source["sha"],
                "REVIEW_SUBJECT_DRIFT:" + path)
        disposition = row.get("disposition")
        require(disposition in ("ANALYZED", "EXCLUDED_WITH_BASIS", "BLOCKED"),
                "INVALID_REVIEW_DISPOSITION")
        require(strings(row.get("evidence_refs"), True) and text(row.get("basis")),
                "REVIEW_EVIDENCE_REQUIRED")
        if disposition == "ANALYZED":
            require(text(row.get("mechanism_summary")), "MECHANISM_REQUIRED")
            if source["type"] == "commit":
                require(text(row.get("nested_campaign_ref")), "SUBMODULE_CONTENT_NOT_REVIEWED")
        elif disposition == "EXCLUDED_WITH_BASIS":
            excluded.append(path)
        else:
            blocked.append(path)
    caps = campaign.get("capabilities")
    require(isinstance(caps, list) and caps, "NO_CAPABILITIES")
    ids, gaps = set(), []
    for cap in caps:
        require(isinstance(cap, dict) and text(cap.get("id")) and cap["id"] not in ids,
                "INVALID_CAPABILITY_ID")
        ids.add(cap["id"])
        require(text(cap.get("objective")), "CAPABILITY_OBJECTIVE_REQUIRED")
        require(strings(cap.get("reference_paths")), "INVALID_REFERENCE_PATHS")
        require(set(cap["reference_paths"]) <= set(leaves), "UNKNOWN_CAPABILITY_SOURCE")
        missing = []
        if not cap["reference_paths"]:
            missing.append("source_mapping")
        for field in CONTRACT_FIELDS:
            require(isinstance(cap.get("contract"), dict)
                    and strings(cap["contract"].get(field)), "INVALID_BEHAVIOR_CONTRACT")
            if not cap["contract"][field]:
                missing.append("contract." + field)
        for field in DESIGN_FIELDS:
            require(isinstance(cap.get("design"), dict)
                    and isinstance(cap["design"].get(field), str), "INVALID_DESIGN")
            if not cap["design"][field].strip():
                missing.append("design." + field)
        implementation, qualification = cap.get("implementation"), cap.get("qualification")
        require(isinstance(implementation, dict) and implementation.get("status") in
                ("NOT_IMPLEMENTED", "CANDIDATE"), "UNSUPPORTED_IMPLEMENTATION_PROMOTION")
        require(strings(implementation.get("artifact_refs")), "INVALID_IMPLEMENTATION_REFS")
        if implementation["status"] != "CANDIDATE":
            missing.append("original_implementation")
        else:
            require(isinstance(implementation.get("subject_sha256"), str) and
                    re.fullmatch("[0-9a-f]{64}", implementation["subject_sha256"]),
                    "IMPLEMENTATION_SUBJECT_REQUIRED")
            if not implementation["artifact_refs"]:
                missing.append("implementation_evidence")
        require(isinstance(qualification, dict) and qualification.get("status") in
                ("NOT_RUN", "WORKER_RECORDED"), "QUALIFICATION_NOT_GRANTED_BY_THIS_AUDIT")
        for key in ("evidence_refs", "broken_control_refs", "holdout_refs"):
            require(strings(qualification.get(key)), "INVALID_QUALIFICATION_REFS")
            if not qualification[key]:
                missing.append(key)
        if qualification["status"] != "WORKER_RECORDED":
            missing.append("qualification_record")
        if missing:
            gaps.append({"capability": cap["id"], "missing": missing})
    edges = campaign.get("graph_edges")
    require(isinstance(edges, list), "INVALID_GRAPH")
    for edge in edges:
        require(isinstance(edge, dict) and edge.get("from") in ids and edge.get("to") in ids
                and edge.get("relation") in RELATIONS, "UNBOUND_GRAPH_EDGE")
    if len(caps) > 1 and not edges:
        gaps.append({"capability": "SYSTEM", "missing": ["cross_component_graph"]})
    require(isinstance(campaign.get("lessons"), list)
            and strings(campaign.get("unknowns")), "INVALID_LEARNING_SURFACE")
    for lesson in campaign["lessons"]:
        require(isinstance(lesson, dict) and all(text(lesson.get(key)) for key in
                ("failure", "positive_method", "hard_negative", "inheritance", "evidence_ref")),
                "INCOMPLETE_LEARNING")
    if not campaign["lessons"]:
        gaps.append({"capability": "SYSTEM", "missing": ["positive_negative_learning"]})
    return {
        "authority": "NONE",
        "status": "RECONSTRUCTION_OPEN" if pending or blocked or gaps else
                  "WORKER_RECORDS_READY_FOR_INDEPENDENT_REVIEW",
        "repository": census["repository"], "commit": census["commit"],
        "inventory_entries": len(census["entries"]), "review_units": len(leaves),
        "pending_review_count": len(pending), "excluded_count": len(excluded),
        "blocked_count": len(blocked), "capability_gaps": gaps,
        "pending_preview": pending[:20], "pending_preview_truncated": len(pending) > 20,
        "submodule_references": sum(r["type"] == "commit" for r in leaves.values()),
        "whole_source_semantic_understanding": "NOT_ESTABLISHED_BY_STRUCTURAL_AUDIT",
        "originality_and_legal_clearance": "NOT_ESTABLISHED",
        "independent_qualification": "NOT_GRANTED",
        "note": "Evidence references are worker assertions, not automatically verified evidence.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--census", required=True)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("new")
    p.add_argument("--domain", required=True)
    p.add_argument("--capability", action="append", required=True)
    p.add_argument("--output", required=True)
    p = sub.add_parser("audit")
    p.add_argument("--campaign", required=True)
    args = parser.parse_args()
    try:
        census = read(args.census)
        if args.command == "new":
            campaign = create(census, args.domain, args.capability)
            with Path(args.output).open("x") as file:
                file.write(json.dumps(campaign, indent=2) + "\n")
            print(json.dumps({"status": "CREATED", "authority": "NONE"}))
        else:
            result = audit(census, read(args.campaign))
            print(json.dumps(result, indent=2))
            return 3 if result["status"] == "RECONSTRUCTION_OPEN" else 0
        return 0
    except (ValueError, OSError, TypeError, KeyError) as exc:
        print(json.dumps({"status": "BLOCKED", "error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
