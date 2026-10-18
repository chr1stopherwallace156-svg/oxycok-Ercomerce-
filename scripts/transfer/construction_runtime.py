#!/usr/bin/env python3
"""Runtime B: create a new offline planner from an abstract brief, never source code."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

from contract import canonical, parse

# Project-authored template. Brief text remains JSON data and is never Python code.
PLANNER = '''#!/usr/bin/env python3
"""Generated local applicability planner; produces obligations, never actions."""
import json
from pathlib import Path
import sys


def evaluate(contract, facts):
    if not isinstance(facts, list) or not all(isinstance(x, str) for x in facts):
        raise ValueError("FACTS_MUST_BE_STRINGS")
    known = set(facts)
    rows = []
    for rule in contract["rules"]:
        exclusions = sorted(known.intersection(rule["excludes_any"]))
        missing = sorted(set(rule["requires_all"]).difference(known))
        state = "EXCLUDED" if exclusions else "NEEDS_CONTEXT" if missing else "REVIEW_REQUIRED"
        rows.append({"id": rule["id"], "state": state, "missing": missing,
                     "exclusions": exclusions, "obligations": rule["test_obligations"]
                     if state == "REVIEW_REQUIRED" else []})
    return {"authority": "NONE", "action_authorized": False, "rules": rows,
            "qualification": "NOT_ESTABLISHED"}


if __name__ == "__main__":
    try:
        contract = json.loads((Path(__file__).parent / "contract.json").read_text())
        print(json.dumps(evaluate(contract, json.load(sys.stdin)), sort_keys=True))
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "BLOCKED", "error": str(exc)}), file=sys.stderr)
        sys.exit(2)
'''


def construct(raw, output):
    brief = parse(raw)
    output = Path(output).absolute()
    resolved = output.resolve()
    if any(part.casefold() == "oxyballs-industrial" for part in resolved.parts):
        raise ValueError("SOURCE_REPOSITORY_WRITE_FORBIDDEN")
    if output.is_symlink() or output.exists():
        raise ValueError("DESTINATION_MUST_BE_NEW")
    if not output.parent.is_dir():
        raise ValueError("DESTINATION_PARENT_REQUIRED")
    contract = canonical(brief) + b"\n"
    files = {
        "runtime.py": PLANNER.encode(),
        "contract.json": contract,
        "README.md": (
            "# OXYCOK generated applicability planner\n\n"
            "Python 3.10+, standard library only. Read facts as a JSON string array from stdin.\n"
            "Example: python3 runtime.py < facts.json\n\n"
            "This project was emitted from an abstract requirements brief and a project-authored\n"
            "template. It does not reproduce reference source code or implement a full business.\n"
            "It returns applicability blockers and test obligations, never executes them.\n"
            "Missing facts remain unknown. Exclusions override positive conditions.\n"
            "Relations remain scoped candidates; no automated theorem proving is claimed.\n"
            "Legal clearance and independent target qualification remain NOT_ESTABLISHED.\n"
        ).encode(),
    }
    receipt = {
        "version": 1, "authority": "NONE", "action_authorized": False,
        "brief_sha256": brief["brief_sha256"],
        "construction": "PROJECT_AUTHORED_DECLARATIVE_PLANNER_TEMPLATE",
        "qualification": "NOT_ESTABLISHED", "legal_clearance": "NOT_ESTABLISHED",
        "files": {name: hashlib.sha256(data).hexdigest() for name, data in files.items()},
    }
    files["construction_receipt.json"] = canonical(receipt) + b"\n"
    # Exclusive directory and file creation. Failure preserves partial output for inspection.
    output.mkdir(exist_ok=False)
    for name, data in files.items():
        with (output / name).open("xb") as target:
            target.write(data)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--brief", required=True, help="Abstract brief JSON; no source repository input")
    parser.add_argument("--output", required=True, help="New local output directory")
    args = parser.parse_args()
    try:
        with Path(args.brief).open("rb") as source:
            raw = source.read(1_000_001)
        print(json.dumps(construct(raw, args.output), indent=2, sort_keys=True))
        return 0
    except (ValueError, OSError, TypeError, KeyError) as exc:
        print(json.dumps({"status": "BLOCKED", "authority": "NONE", "error": str(exc)}),
              file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
