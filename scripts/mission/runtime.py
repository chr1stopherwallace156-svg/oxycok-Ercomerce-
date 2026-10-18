#!/usr/bin/env python3
"""OXYCOK bounded, resumable inspection/learning/construction mission coordinator."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import subprocess

from providers import inventory, python_static, rea_static, bounded_process
from store import Store, canonical, digest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/transfer"))
import contract
import evidence_runtime
import construction_runtime

STAGES = ("NEW", "INSPECTED", "ABSTRACTED", "CONSTRUCTED", "TESTED", "RECORDED", "COMPLETE")


def implementation_identity():
    files = []
    for folder in ("scripts/mission", "scripts/transfer", "scripts/knowledge", "knowledge",
                   "tests/knowledge", "tests/transfer", "tests/mission"):
        for p in sorted((ROOT / folder).rglob("*")):
            if p.is_file() and "__pycache__" not in p.parts:
                files.append((p.relative_to(ROOT).as_posix(), hashlib.sha256(p.read_bytes()).hexdigest()))
    for name in ("docs/rea/QUALIFICATION_DENOMINATOR_V1.json",
                 "docs/knowledge_transfer/source_manifest.json"):
        p = ROOT / name
        files.append((p.relative_to(ROOT).as_posix(), hashlib.sha256(p.read_bytes()).hexdigest()))
    return digest(files)


def start(store, target, provider, domain, mechanisms, facts, attempt=1, rea_executable=None):
    target = Path(target).resolve(strict=True)
    if store.root == target or store.root.is_relative_to(target) or target.is_relative_to(store.root):
        raise ValueError("STATE_TARGET_OVERLAP")
    if provider not in ("python", "rea") or type(attempt) is not int or attempt < 1:
        raise ValueError("INVALID_PROVIDER_OR_ATTEMPT")
    # Validate task semantics before retaining a mission. No source is executed.
    evidence_runtime.analyze(domain=domain, mechanisms=mechanisms, facts=facts)
    subject = inventory(target)
    request = {"target": str(target), "subject_sha256": subject["sha256"],
               "provider": provider, "domain": domain, "mechanisms": mechanisms,
               "facts": facts, "attempt": attempt, "rea_executable": rea_executable,
               "implementation_sha256": implementation_identity()}
    mid = digest(request)
    store.db.execute("BEGIN IMMEDIATE")
    try:
        old = store.db.execute("SELECT id FROM missions WHERE id=?", (mid,)).fetchone()
        if not old:
            store.db.execute("INSERT INTO missions VALUES(?,?,?,?,NULL)",
                             (mid, canonical(request), "NEW", "{}"))
            store.event(mid, "ADMITTED", request)
            store.edge(mid, mid, "INSPECTS_SUBJECT", subject["sha256"])
        store.db.commit()
    except Exception:
        store.db.rollback()
        raise
    return store.status(mid)


def project_path(store, mid):
    return store.root / "projects" / mid


def verify_project(project, brief):
    if project.is_symlink() or not project.is_dir():
        raise ValueError("CANDIDATE_MISSING")
    if set(p.name for p in project.iterdir()) != {
            "runtime.py", "contract.json", "README.md", "construction_receipt.json"}:
        raise ValueError("CANDIDATE_FILE_SET_MISMATCH")
    for path in project.iterdir():
        if path.is_symlink() or not path.is_file():
            raise ValueError("CANDIDATE_INVALID_ENTRY")
    receipt = json.loads((project / "construction_receipt.json").read_text())
    if receipt["brief_sha256"] != brief["brief_sha256"]:
        raise ValueError("CANDIDATE_BRIEF_MISMATCH")
    actual = contract.parse((project / "contract.json").read_bytes())
    if actual != brief or (project / "runtime.py").read_text() != construction_runtime.PLANNER:
        raise ValueError("CANDIDATE_SUBJECT_DRIFT")
    for name in ("runtime.py", "contract.json", "README.md"):
        if hashlib.sha256((project / name).read_bytes()).hexdigest() != receipt["files"][name]:
            raise ValueError("CANDIDATE_HASH_MISMATCH")
    return receipt


def qualify_planner(project, brief):
    # Behavioral guard exam, not reproduction-equivalence or independent qualification.
    cases = []
    for rule in brief["rules"]:
        required = rule["requires_all"]
        cases.append((required, rule["id"], "EVIDENCE_INCOMPLETE"
                      if brief.get("target_evidence", {}).get("coverage_status") == "UNKNOWN"
                      else "REVIEW_REQUIRED"))
        cases.append((required[:-1], rule["id"], "NEEDS_CONTEXT"))
        if rule["excludes_any"]:
            cases.append((required + [rule["excludes_any"][0]], rule["id"], "EXCLUDED"))
    if not cases:
        raise ValueError("EMPTY_QUALIFICATION_DENOMINATOR")
    import tempfile
    import subprocess
    results = []
    for facts, rid, expected in cases:
        # Generated executable is project-authored and integrity-checked by the
        # caller. Target applications are never launched by this qualification.
        result = subprocess.run([sys.executable, str(project / "runtime.py")],
                                input=json.dumps(facts).encode(), capture_output=True,
                                timeout=5, cwd=project)
        if result.returncode or len(result.stdout) > 1_000_000:
            raise ValueError("CANDIDATE_EXECUTION_FAILED")
        reply = json.loads(result.stdout)
        rows = {row["id"]: row for row in reply["rules"]}
        passed = (reply.get("authority") == "NONE"
                  and reply.get("action_authorized") is False
                  and reply.get("qualification") == "NOT_ESTABLISHED"
                  and rows[rid]["state"] == expected)
        results.append({"rule": rid, "expected": expected, "passed": passed})
    return {"verdict": "PASS" if all(x["passed"] for x in results) else "FAIL",
            "scope": "GENERATED_PLANNER_BEHAVIORAL_GUARDS_ONLY", "cases": results,
            "independent": False, "authority": "NONE"}


def step(store, mid):
    store.db.execute("BEGIN IMMEDIATE")
    try:
        state = store.status(mid)
        if state["stage"] in ("BLOCKED", "COMPLETE"):
            store.db.commit()
            return state
        request, outputs, stage = state["request"], state["outputs"], state["stage"]
        try:
            if request["implementation_sha256"] != implementation_identity():
                raise ValueError("IMPLEMENTATION_SUBJECT_DRIFT")
            if inventory(request["target"])["sha256"] != request["subject_sha256"]:
                raise ValueError("TARGET_SUBJECT_DRIFT")
            if stage == "NEW":
                observation = (python_static(request["target"]) if request["provider"] == "python"
                               else rea_static(request["target"], request["rea_executable"] or ""))
                key = store.put(observation)
                outputs["observation"] = key
                store.edge(mid, key, "OBSERVED_FROM", request["subject_sha256"])
                for edge in observation["edges"]:
                    store.edge(mid, edge["source"], edge["relation"], edge["target"])
            elif stage == "INSPECTED":
                observation = store.get(outputs["observation"])
                target_evidence = {
                    "artifact_sha256": request["subject_sha256"],
                    "observation_sha256": outputs["observation"],
                    "provider": observation["provider"],
                    "coverage_status": observation["coverage_status"],
                    "limitations": observation["limitations"],
                }
                brief = evidence_runtime.analyze(domain=request["domain"],
                    mechanisms=request["mechanisms"], facts=request["facts"],
                    target_evidence=target_evidence)
                key = store.put(brief)
                outputs["brief"] = key
                store.edge(mid, key, "USES_OBSERVATION", outputs["observation"])
            elif stage == "ABSTRACTED":
                brief = store.get(outputs["brief"])
                project = project_path(store, mid)
                project.parent.mkdir(exist_ok=True)
                if not project.exists():
                    construction_runtime.construct(contract.canonical(brief), project)
                receipt = verify_project(project, brief)
                key = store.put(receipt)
                outputs["candidate"] = key
                store.edge(mid, key, "CONSTRUCTED_FROM", outputs["brief"])
            elif stage == "CONSTRUCTED":
                brief = store.get(outputs["brief"])
                verify_project(project_path(store, mid), brief)
                report = qualify_planner(project_path(store, mid), brief)
                outputs["qualification"] = store.put(report)
                store.edge(mid, outputs["qualification"], "EXAMINES", outputs["candidate"])
                if report["verdict"] != "PASS":
                    raise ValueError("BEHAVIORAL_GUARD_FAILURE")
            elif stage == "TESTED":
                report = store.get(outputs["qualification"])
                learning = {
                    "outcome": report["verdict"], "subject": request["subject_sha256"],
                    "candidate": outputs["candidate"],
                    "lesson_ids": [r["id"] for r in store.get(outputs["brief"])["rules"]],
                    "positive": "Applicable/missing/excluded conditions preserved by a generated consumer.",
                    "negative": "Static inspection and guard PASS do not establish target behavior equivalence.",
                    "unknowns": ["Independent unfamiliar transfer not run.",
                                 "General code reconstruction not implemented.",
                                 "Legal clearance not established."],
                    "authority": "NONE", "promotion": "NONE",
                }
                outputs["learning"] = store.put(learning)
                store.edge(mid, outputs["learning"], "LEARNS_FROM", outputs["qualification"])
            elif stage == "RECORDED":
                # Revalidate all retained objects before declaring bounded workflow completion.
                for value in outputs.values():
                    store.get(value)
                verify_project(project_path(store, mid), store.get(outputs["brief"]))
            next_stage = STAGES[STAGES.index(stage) + 1]
            store.db.execute("UPDATE missions SET stage=?,outputs=? WHERE id=?",
                             (next_stage, canonical(outputs), mid))
            store.event(mid, "TRANSITION", {"from": stage, "to": next_stage, "outputs": outputs})
        except (ValueError, OSError, TypeError, KeyError, SyntaxError, subprocess.SubprocessError) as exc:
            if hasattr(exc, "evidence"):
                outputs["provider_failure"] = store.put(exc.evidence)
                store.edge(mid, outputs["provider_failure"], "FAILED_OBSERVATION_OF", request["subject_sha256"])
            store.db.execute("UPDATE missions SET stage='BLOCKED',outputs=?,error=? WHERE id=?",
                             (canonical(outputs), str(exc), mid))
            store.event(mid, "FAILURE_PRESERVED", {"stage": stage, "reason": str(exc),
                                                "subject": request["subject_sha256"]})
        store.db.commit()
        return store.status(mid)
    except Exception:
        store.db.rollback()
        raise


def run(store, mid, max_steps):
    if type(max_steps) is not int or not 1 <= max_steps <= 20:
        raise ValueError("STEP_BUDGET_INVALID")
    for _ in range(max_steps):
        state = step(store, mid)
        if state["stage"] in ("COMPLETE", "BLOCKED"):
            break
    return state


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-root", required=True)
    sub = parser.add_subparsers(dest="command", required=True)
    start_p = sub.add_parser("start")
    start_p.add_argument("--target", required=True)
    start_p.add_argument("--provider", choices=["python", "rea"], required=True)
    start_p.add_argument("--rea-executable")
    start_p.add_argument("--domain", required=True)
    start_p.add_argument("--mechanism", action="append", required=True)
    start_p.add_argument("--fact", action="append", default=[])
    start_p.add_argument("--attempt", type=int, default=1)
    for name in ("step", "run", "status", "events", "graph"):
        p = sub.add_parser(name)
        p.add_argument("--mission-id", required=True)
        if name == "run":
            p.add_argument("--max-steps", type=int, default=6)
    args = parser.parse_args()
    store = None
    try:
        if args.command == "start":
            target, state_path = Path(args.target).resolve(), Path(args.state_root).resolve()
            if target == state_path or state_path.is_relative_to(target) or target.is_relative_to(state_path):
                raise ValueError("STATE_TARGET_OVERLAP")
        store = Store(args.state_root)
        if args.command == "start":
            result = start(store, args.target, args.provider, args.domain, args.mechanism,
                           args.fact, args.attempt, args.rea_executable)
        elif args.command == "run":
            result = run(store, args.mission_id, args.max_steps)
        else:
            result = {"step": lambda: step(store, args.mission_id),
                      "status": lambda: store.status(args.mission_id),
                      "events": lambda: store.history(args.mission_id),
                      "graph": lambda: store.graph(args.mission_id)}[args.command]()
        print(json.dumps(result, indent=2, sort_keys=True))
        return 2 if isinstance(result, dict) and result.get("stage") == "BLOCKED" else 0
    except (ValueError, OSError, TypeError, KeyError) as exc:
        print(json.dumps({"status": "BLOCKED", "authority": "NONE", "error": str(exc)}),
              file=sys.stderr)
        return 2
    finally:
        if store:
            store.close()


if __name__ == "__main__":
    sys.exit(main())
