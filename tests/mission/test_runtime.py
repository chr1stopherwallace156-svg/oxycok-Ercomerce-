import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/mission"))
import runtime
import providers
from store import Store
import construction_runtime


class MissionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.target = self.root / "target"
        self.target.mkdir()
        (self.target / "example.py").write_text("def add(a, b):\n    return a + b\n")
        self.store = Store(self.root / "state")

    def tearDown(self):
        self.store.close()
        self.temp.cleanup()

    def admit(self, **kwargs):
        options = dict(target=self.target, provider="python", domain="commerce",
                       mechanisms=["evidence-consumption"],
                       facts=["artifact-produced", "downstream-consumer"])
        options.update(kwargs)
        return runtime.start(self.store, **options)["mission_id"]

    def test_bounded_end_to_end_preserves_target_and_learning(self):
        before = providers.inventory(self.target)
        mid = self.admit()
        result = runtime.run(self.store, mid, 6)
        self.assertEqual(result["stage"], "COMPLETE")
        self.assertEqual(before, providers.inventory(self.target))
        self.assertEqual(len(self.store.history(mid)), 7)
        lesson = self.store.get(result["outputs"]["learning"])
        self.assertTrue(lesson["positive"])
        self.assertTrue(lesson["negative"])
        self.assertTrue(lesson["unknowns"])
        self.assertEqual(lesson["promotion"], "NONE")

    def test_resume_and_duplicate_start_keep_identity(self):
        mid = self.admit()
        self.assertEqual(mid, self.admit())
        self.assertEqual(len(self.store.history(mid)), 1)
        runtime.step(self.store, mid)
        self.store.close()
        self.store = Store(self.root / "state")
        self.assertEqual(runtime.run(self.store, mid, 6)["stage"], "COMPLETE")
        count = len(self.store.history(mid))
        runtime.run(self.store, mid, 6)
        self.assertEqual(len(self.store.history(mid)), count)

    def test_fresh_process_cli_resume(self):
        cmd = [sys.executable, str(ROOT / "scripts/mission/runtime.py"),
               "--state-root", str(self.root / "cli-state")]
        first = subprocess.run(cmd + ["start", "--target", str(self.target),
            "--provider", "python", "--domain", "commerce", "--mechanism",
            "evidence-consumption"], capture_output=True, check=True)
        mid = json.loads(first.stdout)["mission_id"]
        step = subprocess.run(cmd + ["step", "--mission-id", mid],
                              capture_output=True, check=True)
        self.assertEqual(json.loads(step.stdout)["stage"], "INSPECTED")
        resume = subprocess.run(cmd + ["run", "--mission-id", mid],
                                capture_output=True, check=True)
        self.assertEqual(json.loads(resume.stdout)["stage"], "COMPLETE")

    def test_changed_subject_is_blocked_and_failure_is_not_rewritten(self):
        mid = self.admit()
        (self.target / "example.py").write_text("def subtract(a,b): return a-b\n")
        red = runtime.run(self.store, mid, 6)
        self.assertEqual(red["stage"], "BLOCKED")
        self.assertEqual(red["error"], "TARGET_SUBJECT_DRIFT")
        successor = self.admit(attempt=2)
        self.assertNotEqual(mid, successor)
        self.assertEqual(runtime.run(self.store, successor, 6)["stage"], "COMPLETE")
        self.assertEqual(self.store.status(mid)["stage"], "BLOCKED")
        self.assertEqual(self.store.history(mid)[-1]["kind"], "FAILURE_PRESERVED")

    def test_observation_corruption_blocks_abstraction(self):
        mid = self.admit()
        state = runtime.step(self.store, mid)
        self.store.db.execute("UPDATE artifacts SET body='{}' WHERE digest=?",
                              (state["outputs"]["observation"],))
        self.store.db.commit()
        red = runtime.step(self.store, mid)
        self.assertEqual(red["stage"], "BLOCKED")
        self.assertIn("ARTIFACT_HASH_MISMATCH", red["error"])

    def test_partial_constructor_output_is_preserved_and_blocked(self):
        mid = self.admit()
        runtime.run(self.store, mid, 2)
        path = runtime.project_path(self.store, mid)
        path.parent.mkdir()
        path.mkdir()
        (path / "runtime.py").write_text("partial")
        state = runtime.step(self.store, mid)
        self.assertEqual(state["stage"], "BLOCKED")
        self.assertEqual((path / "runtime.py").read_text(), "partial")

    def test_valid_constructor_orphan_is_recovered(self):
        mid = self.admit()
        state = runtime.run(self.store, mid, 2)
        path = runtime.project_path(self.store, mid)
        path.parent.mkdir()
        brief = self.store.get(state["outputs"]["brief"])
        construction_runtime.construct(runtime.contract.canonical(brief), path)
        self.assertEqual(runtime.run(self.store, mid, 6)["stage"], "COMPLETE")

    def test_static_inspection_never_executes_target(self):
        marker = self.root / "executed"
        (self.target / "bad.py").write_text(
            "from pathlib import Path\nPath(" + repr(str(marker)) + ").write_text('ran')\n")
        mid = self.admit()
        self.assertEqual(runtime.run(self.store, mid, 6)["stage"], "COMPLETE")
        self.assertFalse(marker.exists())
        graph = self.store.graph(mid)
        self.assertTrue(any(e["relation"] == "SYNTAX_CALL_TARGET" for e in graph))

    def test_graph_connects_all_mission_artifacts(self):
        mid = self.admit()
        runtime.run(self.store, mid, 6)
        relations = {e["relation"] for e in self.store.graph(mid)}
        self.assertTrue({"INSPECTS_SUBJECT", "OBSERVED_FROM", "USES_OBSERVATION",
                         "CONSTRUCTED_FROM", "EXAMINES", "LEARNS_FROM"} <= relations)

    def test_unknown_evidence_changes_generated_consumer_result(self):
        observation = providers.python_static(self.target)
        observation["coverage_status"] = "UNKNOWN"
        with patch.object(runtime, "python_static", return_value=observation):
            mid = self.admit()
            state = runtime.run(self.store, mid, 6)
        self.assertEqual(state["stage"], "COMPLETE")
        report = self.store.get(state["outputs"]["qualification"])
        self.assertEqual(report["cases"][0]["expected"], "EVIDENCE_INCOMPLETE")
        self.assertEqual(report["verdict"], "PASS")
        self.assertFalse(report["independent"])

    def test_broken_control_fails_behavioral_gate(self):
        mid = self.admit()
        state = runtime.run(self.store, mid, 3)
        path = runtime.project_path(self.store, mid)
        (path / "runtime.py").write_text(
            "import json\nprint(json.dumps({'authority':'NONE','action_authorized':False,"
            "'qualification':'NOT_ESTABLISHED','rules':[{'id':'UKL-002','state':'REVIEW_REQUIRED'}]}))\n")
        report = runtime.qualify_planner(path, self.store.get(state["outputs"]["brief"]))
        self.assertEqual(report["verdict"], "FAIL")

    def test_runtime_subject_change_blocks_unfinished_mission(self):
        mid = self.admit()
        with patch.object(runtime, "implementation_identity", return_value="changed"):
            state = runtime.step(self.store, mid)
        self.assertEqual(state["error"], "IMPLEMENTATION_SUBJECT_DRIFT")

    def test_two_workers_commit_distinct_transitions(self):
        mid = self.admit()
        def worker():
            store = Store(self.root / "state")
            try:
                return runtime.step(store, mid)["stage"]
            finally:
                store.close()
        with concurrent.futures.ThreadPoolExecutor(2) as pool:
            stages = list(pool.map(lambda _: worker(), range(2)))
        self.assertEqual(set(stages), {"INSPECTED", "ABSTRACTED"})
        self.assertEqual(len(self.store.history(mid)), 3)

    def test_missing_rea_provider_blocks_without_success_fallback(self):
        mid = self.admit(provider="rea", rea_executable="/nonexistent/rea")
        result = runtime.run(self.store, mid, 6)
        self.assertEqual(result["stage"], "BLOCKED")
        self.assertIn("REA_EXECUTABLE_UNAVAILABLE", result["error"])

    def test_provider_failure_retains_original_diagnostic(self):
        mid = self.admit(provider="rea", rea_executable="/nonexistent/rea")
        failure = providers.ProviderFailure("UPSTREAM_HOST_FAILURE",
                                            {"diagnostic": {"code": "capability_unavailable"}})
        with patch.object(runtime, "rea_static", side_effect=failure):
            result = runtime.step(self.store, mid)
        key = result["outputs"]["provider_failure"]
        self.assertEqual(self.store.get(key)["diagnostic"]["code"], "capability_unavailable")
        self.assertEqual(result["stage"], "BLOCKED")

    def test_state_cannot_be_written_inside_target_via_cli(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/mission/runtime.py"),
            "--state-root", str(self.target / "state"), "start", "--target", str(self.target),
            "--provider", "python", "--domain", "commerce", "--mechanism", "evidence-consumption"],
            capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.target / "state").exists())

    def test_symlink_target_entry_is_rejected(self):
        (self.target / "link").symlink_to(self.root / "state")
        with self.assertRaisesRegex(ValueError, "UNSUPPORTED_TARGET_ENTRY"):
            providers.inventory(self.target)

    def test_output_budget_and_timeout_are_not_green(self):
        with self.assertRaisesRegex(ValueError, "PROVIDER_OUTPUT_BUDGET"):
            providers.bounded_process([sys.executable, "-c", "print('x'*100000)"], max_bytes=100)
        with self.assertRaisesRegex(ValueError, "PROVIDER_TIMEOUT"):
            providers.bounded_process([sys.executable, "-c", "import time;time.sleep(2)"], timeout=0.05)

    def test_malformed_rea_reply_rejected(self):
        with patch.object(providers, "bounded_process", side_effect=[b"6.7.0", b'{"foo":1}']):
            with self.assertRaisesRegex(ValueError, "REA_INVALID"):
                providers.rea_static(self.target, sys.executable)

    def test_empty_or_unsupported_target_does_not_pass(self):
        (self.target / "example.py").unlink()
        (self.target / "README.txt").write_text("not a Python module")
        mid = self.admit()
        self.assertEqual(runtime.run(self.store, mid, 6)["stage"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
