import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/transfer"))
import contract
import evidence_runtime as evidence
import construction_runtime as construction


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.brief = evidence.analyze(domain="commerce",
            mechanisms=["evidence-consumption"],
            facts=["artifact-produced", "downstream-consumer"])

    def raw(self, brief=None):
        return contract.canonical(self.brief if brief is None else brief)

    def resign(self, brief):
        brief["brief_sha256"] = contract.digest({k: v for k, v in brief.items()
                                                if k != "brief_sha256"})
        return brief

    def test_evidence_preserves_failure_success_exclusions_and_relations(self):
        rule = self.brief["rules"][0]
        self.assertTrue(rule["failure"])
        self.assertTrue(rule["positive"])
        self.assertTrue(rule["excludes_any"])
        self.assertEqual(self.brief["relations"][0]["relation"], "DOES_NOT_IMPLY")
        self.assertEqual(self.brief["rights"]["code_reuse"], "PROHIBITED")

    def test_each_seed_builds_a_scoped_brief(self):
        _, catalog = evidence.knowledge.load(ROOT)
        for lesson in catalog["lessons"]:
            with self.subTest(lesson=lesson["id"]):
                brief = evidence.analyze(domain="unseen-domain",
                    mechanisms=[lesson["mechanism"]], facts=[])
                self.assertEqual(brief["rules"][0]["id"], lesson["id"])
                self.assertTrue(brief["relations"][0]["conditions"])

    def test_separate_processes_construct_without_knowledge_checkout(self):
        # Runtime A produces the brief, then Runtime B operates from only its two
        # own implementation modules and the brief in an isolated directory.
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            result = subprocess.run([sys.executable,
                str(ROOT / "scripts/transfer/evidence_runtime.py"),
                "--domain", "laboratory", "--mechanism", "evidence-consumption"],
                capture_output=True, check=True)
            (root / "brief.json").write_bytes(result.stdout)
            for name in ["contract.py", "construction_runtime.py"]:
                (root / name).write_bytes((ROOT / "scripts/transfer" / name).read_bytes())
            subprocess.run([sys.executable, str(root / "construction_runtime.py"),
                "--brief", str(root / "brief.json"), "--output", str(root / "project")],
                cwd=root, capture_output=True, check=True)
            runtime = root / "project/runtime.py"
            def evaluate(facts):
                proc = subprocess.run([sys.executable, str(runtime)],
                    input=json.dumps(facts).encode(), capture_output=True, check=True,
                    cwd=root)
                return json.loads(proc.stdout)
            ready = evaluate(["artifact-produced", "downstream-consumer"])
            unknown = evaluate(["artifact-produced"])
            excluded = evaluate(["artifact-produced", "downstream-consumer",
                                 "storage-only-contract"])
            self.assertEqual(ready["rules"][0]["state"], "REVIEW_REQUIRED")
            self.assertTrue(ready["rules"][0]["obligations"])
            self.assertEqual(unknown["rules"][0]["state"], "NEEDS_CONTEXT")
            self.assertEqual(excluded["rules"][0]["state"], "EXCLUDED")
            self.assertFalse(ready["action_authorized"])
            self.assertEqual(ready["qualification"], "NOT_ESTABLISHED")
            self.assertEqual(ready, evaluate(["artifact-produced", "downstream-consumer"]))

    def test_no_match_does_not_produce_empty_success_project(self):
        with self.assertRaises(contract.ContractError):
            evidence.analyze(domain="x", mechanisms=["unknown"], facts=[])

    def test_hash_drift_rejected(self):
        self.brief["domain"] = "changed"
        with self.assertRaisesRegex(contract.ContractError, "BRIEF_HASH"):
            contract.parse(self.raw())

    def test_raw_code_field_rejected_even_if_hash_recomputed(self):
        self.brief["source_code"] = "print('untrusted')"
        with self.assertRaises(contract.ContractError):
            contract.parse(self.raw(self.resign(self.brief)))

    def test_authority_escalation_rejected(self):
        self.brief["action_authorized"] = True
        with self.assertRaisesRegex(contract.ContractError, "AUTHORITY"):
            contract.parse(self.raw(self.resign(self.brief)))

    def test_legal_clearance_cannot_be_inferred(self):
        self.brief["rights"]["legal_clearance"] = "CLEARED"
        with self.assertRaisesRegex(contract.ContractError, "RIGHTS"):
            contract.parse(self.raw(self.resign(self.brief)))

    def test_unknown_relation_or_unscoped_equivalence_rejected(self):
        for relation, conditions in [("EQUALS", ["condition"]),
                                     ("EQUIVALENT_UNDER_CONDITIONS", [])]:
            brief = copy.deepcopy(self.brief)
            brief["relations"][0].update(relation=relation, conditions=conditions)
            with self.assertRaises(contract.ContractError):
                contract.parse(self.raw(self.resign(brief)))

    def test_source_strings_are_never_executed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.brief["rules"][0]["principle"] = "__import__('os').system('false')"
            construction.construct(self.raw(self.resign(self.brief)), root / "out")
            self.assertEqual((root / "out/runtime.py").read_text(), construction.PLANNER)
            self.assertIn("__import__", (root / "out/contract.json").read_text())

    def test_existing_output_cannot_be_overwritten(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "project"
            construction.construct(self.raw(), root)
            original = (root / "runtime.py").read_bytes()
            with self.assertRaisesRegex(ValueError, "DESTINATION"):
                construction.construct(self.raw(), root)
            self.assertEqual((root / "runtime.py").read_bytes(), original)

    def test_named_source_repository_write_is_blocked(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "oxyballs-Industrial"
            root.mkdir()
            with self.assertRaisesRegex(ValueError, "SOURCE_REPOSITORY"):
                construction.construct(self.raw(), root / "generated")
            self.assertEqual(list(root.iterdir()), [])

    def test_oversized_or_duplicate_key_input_rejected(self):
        with self.assertRaises(contract.ContractError):
            contract.parse(b"x" * 1_000_001)
        with self.assertRaises(contract.ContractError):
            contract.parse(b'{"version":1,"version":1}')

    def test_generated_runtime_rejects_malformed_facts(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "project"
            construction.construct(self.raw(), root)
            result = subprocess.run([sys.executable, str(root / "runtime.py")],
                input=b'{"artifact-produced":true}', capture_output=True)
            self.assertEqual(result.returncode, 2)

    def test_independence_of_created_artifact_hashes(self):
        import hashlib
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "project"
            receipt = construction.construct(self.raw(), root)
            for name, sha in receipt["files"].items():
                self.assertEqual(hashlib.sha256((root / name).read_bytes()).hexdigest(), sha)


if __name__ == "__main__":
    unittest.main()
