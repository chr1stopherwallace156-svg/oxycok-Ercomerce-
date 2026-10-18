#!/usr/bin/env python3
"""Runtime A: turn curated evidence into a source-code-free declarative brief."""
import argparse
import json
from pathlib import Path
import sys

from contract import RIGHTS, digest, validate

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/knowledge"))
import knowledge


def analyze(*, domain, mechanisms, facts, root=ROOT):
    manifest, catalog = knowledge.load(root)
    retrieval = knowledge.retrieve(manifest, catalog, domain=domain,
                                   mechanisms=mechanisms, facts=facts)
    relations = knowledge.read_json(Path(root) / "knowledge/relations.json")
    knowledge.require(relations.get("version") == 1 and relations.get("authority") == "NONE",
                      "INVALID_RELATION_REGISTRY")
    selected = retrieval["lessons"]
    ids = {lesson["id"] for lesson in selected}
    brief = {
        "version": 1, "kind": "ABSTRACT_TRANSFER_BRIEF", "authority": "NONE",
        "action_authorized": False, "domain": domain, "facts": facts,
        "facts_basis": retrieval["facts_basis"], "rights": dict(RIGHTS),
        "coverage": retrieval["coverage"],
        "rules": [{
            "id": lesson["id"], "mechanism": lesson["mechanism"],
            "requires_all": lesson["requires_all"], "excludes_any": lesson["excludes_any"],
            "principle": lesson["principle"], "failure": lesson["failure"],
            "positive": lesson["positive"], "adapter": lesson["adapter"],
            "test_obligations": lesson["tests"], "status": lesson["target_status"],
        } for lesson in selected],
        "relations": [r for r in relations["relations"] if r["lesson_id"] in ids],
        "evidence_pins": [{k: s[k] for k in ("id", "repository", "commit", "path", "git_blob_sha")}
                          for s in retrieval["sources"]],
    }
    brief["brief_sha256"] = digest(brief)
    return validate(brief)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--domain", required=True)
    parser.add_argument("--mechanism", action="append", required=True)
    parser.add_argument("--fact", action="append", default=[])
    args = parser.parse_args()
    try:
        print(json.dumps(analyze(domain=args.domain, mechanisms=args.mechanism,
                                 facts=args.fact), indent=2, sort_keys=True))
        return 0
    except (ValueError, OSError, TypeError, KeyError) as exc:
        print(json.dumps({"status": "BLOCKED", "authority": "NONE", "error": str(exc)}),
              file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
