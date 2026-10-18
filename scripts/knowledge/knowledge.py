#!/usr/bin/env python3
"""Offline, read-only mechanism retrieval. No commerce imports or action sinks."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]


class KnowledgeError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise KnowledgeError(message)


def text(value):
    return isinstance(value, str) and bool(value.strip())


def strings(value, nonempty=False):
    return (isinstance(value, list) and (bool(value) or not nonempty)
            and all(text(item) for item in value) and len(value) == len(set(value)))


def read_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "DUPLICATE_JSON_KEY:" + key)
            result[key] = value
        return result
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)


def load(root=ROOT):
    root = Path(root).resolve()
    manifest = read_json(root / "docs/knowledge_transfer/source_manifest.json")
    catalog = read_json(root / "knowledge/lessons.json")
    for obj in (manifest, catalog):
        require(isinstance(obj, dict) and obj.get("version") == 1
                and obj.get("authority") == "NONE", "INVALID_ROOT_CONTRACT")
    require(isinstance(manifest.get("sources"), list) and manifest["sources"],
            "EMPTY_SOURCES")
    sources = {}
    allowed_repos = {
        "chr1stopherwallace156-svg/oxyballs-Industrial",
        "chr1stopherwallace156-svg/oxycok-Ercomerce-",
    }
    for source in manifest["sources"]:
        require(isinstance(source, dict), "INVALID_SOURCE")
        sid = source.get("id")
        require(text(sid) and sid not in sources, "DUPLICATE_OR_INVALID_SOURCE_ID")
        require(source.get("repository") in allowed_repos, "UNREGISTERED_REPOSITORY")
        require(text(source.get("path")), "MISSING_SOURCE_PATH")
        require(isinstance(source.get("commit"), str)
                and re.fullmatch(r"[0-9a-f]{40}", source["commit"]), "UNPINNED_SOURCE")
        require(isinstance(source.get("git_blob_sha"), str)
                and re.fullmatch(r"[0-9a-f]{40}", source["git_blob_sha"]), "INVALID_BLOB_PIN")
        if source["repository"].endswith("/oxyballs-Industrial"):
            require(source.get("evidence_mode") == "PRIVATE_REFERENCE_PIN_ONLY"
                    and not any(key in source for key in ("snapshot", "content", "excerpt")),
                    "PRIVATE_SOURCE_PUBLICATION_BLOCKED")
            require(isinstance(source.get("source_sha256"), str)
                    and re.fullmatch(r"[0-9a-f]{64}", source["source_sha256"]),
                    "INVALID_PRIVATE_SOURCE_HASH_PIN")
            sources[sid] = source
            continue
        require(source.get("evidence_mode") == "PUBLIC_EXACT_SNAPSHOT", "INVALID_EVIDENCE_MODE")
        snapshot = source.get("snapshot")
        require(text(snapshot), "MISSING_SNAPSHOT")
        path = (root / snapshot).resolve()
        directory = (root / "docs/knowledge_transfer/sources").resolve()
        require(path.is_relative_to(directory) and path.is_relative_to(root),
                "SNAPSHOT_PATH_ESCAPE")
        data = path.read_bytes()
        require(hashlib.sha256(data).hexdigest() == source.get("snapshot_sha256"),
                "SNAPSHOT_HASH_MISMATCH:" + sid)
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        require(source.get("snapshot_representation") == "EXACT_BLOB"
                and blob == source.get("git_blob_sha")
                and blob == source.get("snapshot_git_blob_sha"),
                "SOURCE_BLOB_MISMATCH:" + sid)
        sources[sid] = source
    require(isinstance(catalog.get("lessons"), list) and catalog["lessons"],
            "EMPTY_LESSONS")
    ids = set()
    for lesson in catalog["lessons"]:
        require(isinstance(lesson, dict), "INVALID_LESSON")
        lid = lesson.get("id")
        require(text(lid) and lid not in ids, "DUPLICATE_OR_INVALID_LESSON_ID")
        ids.add(lid)
        require(lesson.get("authority") == "NONE"
                and lesson.get("target_status") == "TRANSFER_CANDIDATE"
                and lesson.get("source_status") == "SOURCE_RECORD_ONLY_NOT_REQUALIFIED",
                "UNSUPPORTED_PROMOTION:" + lid)
        for key in ("mechanism", "principle", "failure", "positive", "adapter", "limits"):
            require(text(lesson.get(key)), "MISSING_LESSON_FIELD:" + key)
        for key in ("sources", "requires_all", "tests"):
            require(strings(lesson.get(key), nonempty=True), "INVALID_LESSON_LIST:" + key)
        require(strings(lesson.get("excludes_any")), "INVALID_EXCLUSIONS")
        require(not set(lesson["requires_all"]) & set(lesson["excludes_any"]),
                "CONTRADICTORY_APPLICABILITY")
        require(all(s in sources for s in lesson["sources"]), "UNKNOWN_SOURCE_REFERENCE")
    return manifest, catalog


def retrieve(manifest, catalog, *, domain, mechanisms, facts):
    require(text(domain), "DOMAIN_REQUIRED")
    require(strings(mechanisms, nonempty=True), "MECHANISM_REQUIRED")
    require(strings(facts), "INVALID_FACTS")
    known = set(facts)
    results = []
    for lesson in sorted(catalog["lessons"], key=lambda row: row["id"]):
        if lesson["mechanism"] not in mechanisms:
            continue
        excluded = sorted(known & set(lesson["excludes_any"]))
        missing = sorted(set(lesson["requires_all"]) - known)
        disposition = ("EXCLUDED" if excluded else
                       "NEEDS_CONTEXT" if missing else "APPLICABLE_CANDIDATE")
        results.append({**lesson, "disposition": disposition,
                        "matched_exclusions": excluded, "missing_facts": missing})
    used_sources = {sid for lesson in results for sid in lesson["sources"]}
    return {
        "version": 1,
        "authority": "NONE",
        "action_authorized": False,
        "target_domain": domain,
        "retrieval_mode": "EXACT_MECHANISM_TAGS_WITH_DECLARED_FACTS",
        "facts_basis": "CALLER_DECLARED_NOT_INDEPENDENTLY_VERIFIED",
        "status": "CANDIDATES_RETURNED" if results else "NO_MATCH",
        "coverage": "BOUNDED_SEED_NOT_EXHAUSTIVE",
        "warning": "Retrieval is not evidence of consumer use, factual truth or transfer qualification.",
        "lessons": results,
        "sources": [s for s in manifest["sources"] if s["id"] in used_sources],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    query = sub.add_parser("retrieve")
    query.add_argument("--domain", required=True)
    query.add_argument("--mechanism", action="append", required=True)
    query.add_argument("--fact", action="append", default=[])
    args = parser.parse_args(argv)
    try:
        manifest, catalog = load()
        if args.command == "validate":
            result = {"status": "VALID", "sources": len(manifest["sources"]),
                      "lessons": len(catalog["lessons"]), "authority": "NONE",
                      "public_snapshots": sum(s["evidence_mode"] == "PUBLIC_EXACT_SNAPSHOT" for s in manifest["sources"]),
                      "private_source_pins": sum(s["evidence_mode"] == "PRIVATE_REFERENCE_PIN_ONLY" for s in manifest["sources"])}
        else:
            result = retrieve(manifest, catalog, domain=args.domain,
                              mechanisms=args.mechanism, facts=args.fact)
        print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
        return 0
    except (KnowledgeError, OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({"status": "BLOCKED", "authority": "NONE",
                          "action_authorized": False, "error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
