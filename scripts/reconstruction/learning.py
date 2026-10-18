#!/usr/bin/env python3
"""Reusable evidence/learning records under the existing reconstruction campaign.

Lexical scan is navigation, not semantic understanding or defect detection.
No reference code is executed by this module. No runtime-default promotion.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

from campaign import read, require, digest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "elektron_bridge"))
from snapshot import tree_sha

SIGNALS = {
    "error": r"\b(?:throw|raise|except|catch)\b",
    "recovery": r"\b(?:retry|rollback|recover|cleanup|dispose|finally)\w*\b",
    "uncertainty": r"\b(?:unknown|unsupported|truncated|unavailable)\w*\b",
    "effects": r"\b(?:writeFile|rename|unlink|mkdir|spawn|execFile|fetch|send|commit)\w*\b",
    "test": r"\b(?:it|test|describe)\s*(?:\.[\w]+)*\s*\(",
}
KINDS = {"FAILURE", "POSITIVE_METHOD", "HARD_NEGATIVE", "UNKNOWN"}
CLASSIFICATIONS = {"SAME_FAMILY", "NEW_FAMILY", "NON_FAMILY_BOUNDED_DEFECT",
                   "CENSUS_METHODOLOGY_FAILURE", "PRE_EXISTING_BASELINE",
                   "ENVIRONMENT", "OBSERVATION_ONLY", "NOT_ESTABLISHED"}
ANALYSIS_FIELDS = ("local_manifestation", "violated_assumption", "root_mechanism",
    "shared_owner", "exposed_capabilities", "bounded_same_family_instances",
    "hard_negatives", "historical_artifacts_predating_fix",
    "downstream_authority_impact", "guard_adversarial_failures",
    "inherited_behavior")


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args])


def scan(root, commit, repository):
    """Read immutable Git objects, including every blob, never worktree bytes."""
    require(re.fullmatch(r"[a-f0-9]{40}", commit) is not None, "FULL_COMMIT_REQUIRED")
    require(git(root, "rev-parse", commit + "^{commit}").decode().strip() == commit,
            "COMMIT_IDENTITY_MISMATCH")
    tree = git(root, "rev-parse", commit + "^{tree}").decode().strip()
    raw = git(root, "ls-tree", "-r", "-z", "-l", commit)
    entries = []
    for item in raw.split(b"\0"):
        if not item:
            continue
        meta, path = item.split(b"\t", 1)
        mode, kind, sha, size = meta.decode().split()
        entries.append({"path": path.decode("utf-8"), "mode": mode,
                        "type": kind, "sha": sha, "bytes": None if size == "-" else int(size)})
    process = subprocess.Popen(["git", "-C", str(root), "cat-file", "--batch"],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    try:
        for row in entries:
            row["semantic_review"] = "PENDING"
            if row["type"] != "blob":
                row["scan"] = "NESTED_SCOPE_NOT_MATERIALIZED"
                continue
            process.stdin.write((row["sha"] + "\n").encode()); process.stdin.flush()
            identity, kind, size = process.stdout.readline().decode().split()
            require(identity == row["sha"] and kind == "blob", "BLOB_HEADER_MISMATCH")
            body = process.stdout.read(int(size))
            require(process.stdout.read(1) == b"\n", "BLOB_FRAME_MISMATCH")
            actual = hashlib.sha1(b"blob " + str(len(body)).encode() + b"\0" + body).hexdigest()
            require(actual == identity and len(body) == row["bytes"], "BLOB_IDENTITY_MISMATCH")
            row["sha256"] = hashlib.sha256(body).hexdigest()
            try:
                text = body.decode("utf-8")
                require("\0" not in text, "BINARY_CONTENT")
            except (UnicodeDecodeError, ValueError):
                row["scan"] = "BINARY_BYTES_VERIFIED"
                continue
            row["scan"] = "TEXT_LEXICALLY_SCANNED"
            lines = text.splitlines()
            row["lines"] = len(lines)
            row["signal_lines"] = {key: [n for n, line in enumerate(lines, 1)
                if re.search(pattern, line, re.I)] for key, pattern in SIGNALS.items()}
    finally:
        process.stdin.close(); process.stdout.close(); process.wait()
    require(process.returncode == 0, "BLOB_READER_FAILED")
    return {"version": 1, "kind": "LEARNING_SURFACE_INVENTORY", "authority": "NONE",
        "reference": {"repository": repository, "commit": commit, "tree": tree},
        "entries": entries, "counts": dict(Counter(row["scan"] for row in entries)),
        "semantic_exhaustion": "NOT_ESTABLISHED",
        "limits": "Lexical hits may include comments or miss dynamic effects. All blobs read; nested gitlinks and history excluded."}


def validate_record(row, reference, paths):
    require(isinstance(row, dict), "RECORD_OBJECT_REQUIRED")
    require(row.get("kind") in KINDS and row.get("authority") == "NONE", "INVALID_KIND_OR_AUTHORITY")
    require(row.get("reference") == reference, "STALE_REFERENCE")
    require(row.get("classification") in CLASSIFICATIONS, "INVALID_CLASSIFICATION")
    for key in ("id", "mechanism", "observation", "positive_method", "consumer_effect", "rollback"):
        require(isinstance(row.get(key), str) and row[key].strip(), "MISSING_" + key.upper())
    for key in ("applicability", "exclusions", "evidence_refs", "test_obligations", "unknowns"):
        require(isinstance(row.get(key), list) and row[key]
                and all(isinstance(v, str) and v.strip() for v in row[key]), "MISSING_" + key.upper())
    require(row.get("maturity") == "TRANSFER_CANDIDATE", "PROMOTION_NOT_SUPPORTED")
    require(row.get("local_problem_closed") is False and row.get("repository_learning_closed") is False,
            "CLOSURE_REQUIRES_SEPARATE_OWNER_REVIEW")
    require(isinstance(row.get("source_paths"), list) and row["source_paths"], "SOURCE_PATHS_REQUIRED")
    for pin in row["source_paths"]:
        require(pin.get("path") in paths and paths[pin["path"]] == pin.get("sha"), "SOURCE_PATH_PIN_DRIFT")
    if row["kind"] == "FAILURE":
        analysis = row.get("analysis", {})
        for key in ANALYSIS_FIELDS:
            require(bool(analysis.get(key)) and analysis[key] != "NOT_ESTABLISHED",
                    "INCOMPLETE_FAILURE_ANALYSIS:" + key)
        require(isinstance(analysis.get("forward_holdout_warranted"), bool), "HOLDOUT_DISPOSITION_REQUIRED")
    return row


def audit(inventory, records):
    require(inventory.get("kind") == "LEARNING_SURFACE_INVENTORY" and inventory.get("entries"), "INVALID_INVENTORY")
    paths = {r["path"]: r["sha"] for r in inventory["entries"]}
    require(len(paths) == len(inventory["entries"]), "DUPLICATE_SURFACE")
    require(tree_sha({r["path"]: {"mode": r["mode"], "git_blob_sha": r["sha"]}
                      for r in inventory["entries"]}) == inventory["reference"]["tree"],
            "INVENTORY_TREE_MISMATCH")
    require(isinstance(records, list) and records, "EMPTY_LEARNING_CORPUS")
    ids = set()
    for row in records:
        validate_record(row, inventory["reference"], paths)
        require(row["id"] not in ids, "DUPLICATE_LEARNING_ID"); ids.add(row["id"])
    reviewed = {pin["path"] for row in records for pin in row["source_paths"]}
    return {"version": 1, "status": "OPEN", "authority": "NONE",
        "inventory_sha256": digest(inventory), "records_sha256": digest(records),
        "reference": inventory["reference"], "record_count": len(records),
        "worker_reviewed_files": len(reviewed), "total_units": len(paths),
        "remaining_semantic_review_units": len(set(paths) - reviewed),
        "independent_qualification": "NOT_ESTABLISHED",
        "repository_learning_closed": False, "runtime_default_promotion": False}


def retrieve(inventory, records, facts):
    audit(inventory, records)
    candidates = []
    for row in records:
        needed, excluded = set(row["applicability"]), set(row["exclusions"]) & set(facts)
        state = "EXCLUDED" if excluded else "NEEDS_CONTEXT" if needed - set(facts) else "REVIEW_REQUIRED"
        candidates.append({"id": row["id"], "state": state,
            "missing": sorted(needed - set(facts)), "exclusions_triggered": sorted(excluded),
            "mechanism": row["mechanism"], "positive_method": row["positive_method"],
            "consumer_effect": row["consumer_effect"], "evidence_refs": row["evidence_refs"],
            "test_obligations": row["test_obligations"], "authority": "NONE"})
    return {"authority": "NONE", "fact_basis": "CALLER_DECLARED", "candidates": candidates,
            "unknown_facts": sorted(set(facts) - {f for row in records for f in row["applicability"] + row["exclusions"]}),
            "qualification": "NOT_ESTABLISHED"}


def preserve(directory, payload):
    """Create-only content-addressed evidence; a changed observation gets a new file."""
    directory = Path(directory); directory.mkdir(parents=True, exist_ok=True)
    identity = digest(payload); target = directory / (identity + ".json")
    serialized = json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    try:
        with target.open("x", encoding="utf-8") as out: out.write(serialized)
    except FileExistsError:
        require(target.read_text() == serialized, "EXISTING_EVIDENCE_CORRUPTED")
    return target


def verify_custody(root, index):
    root = Path(root).resolve()
    require(isinstance(index.get("files"), list) and index["files"], "EMPTY_CUSTODY_INDEX")
    seen = set()
    for row in index["files"]:
        relative = Path(row["path"])
        require(not relative.is_absolute() and ".." not in relative.parts,
                "UNSAFE_EVIDENCE_PATH")
        path = root / relative
        require(path.resolve().is_relative_to(root) and not path.is_symlink(), "EVIDENCE_PATH_ESCAPE")
        require(row["path"] not in seen, "DUPLICATE_EVIDENCE_PATH"); seen.add(row["path"])
        body = path.read_bytes()
        require(hashlib.sha256(body).hexdigest() == row["sha256"]
                and len(body) == row["bytes"], "EVIDENCE_BYTES_DRIFT:" + row["path"])
    return {"status": "VERIFIED_BYTES_ONLY", "files": len(seen), "authority": "NONE",
            "semantic_qualification": "NOT_ESTABLISHED"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    p = sub.add_parser("scan"); p.add_argument("--root", required=True); p.add_argument("--commit", required=True)
    p.add_argument("--repository", required=True); p.add_argument("--output-dir", required=True)
    p = sub.add_parser("verify-custody"); p.add_argument("--root", required=True); p.add_argument("--index", required=True)
    for action in ("audit", "retrieve"):
        p = sub.add_parser(action); p.add_argument("--inventory", required=True); p.add_argument("--records", required=True)
        if action == "retrieve": p.add_argument("--fact", action="append", default=[])
    args = parser.parse_args()
    try:
        if args.action == "scan":
            root = Path(args.root).resolve(); output = Path(args.output_dir).resolve()
            require(not output.is_relative_to(root), "OUTPUT_INSIDE_REFERENCE_FORBIDDEN")
            result = {"evidence_path": str(preserve(output, scan(root, args.commit, args.repository)))}
        elif args.action == "verify-custody":
            result = verify_custody(args.root, read(args.index))
        else:
            inventory, records = read(args.inventory), read(args.records)
            result = audit(inventory, records) if args.action == "audit" else retrieve(inventory, records, args.fact)
        print(json.dumps(result, indent=2)); return 3 if args.action == "audit" else 0
    except (ValueError, OSError, KeyError, TypeError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"status": "INVALID", "authority": "NONE", "error": str(exc)})); return 2


if __name__ == "__main__":
    sys.exit(main())
