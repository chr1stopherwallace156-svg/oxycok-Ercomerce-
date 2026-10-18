import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/reconstruction"))
from learning import audit, retrieve, preserve, scan, verify_custody


class LearningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = ROOT / "reconstruction/subjects/rea/learning"
        cls.report = json.loads((cls.directory / "AUDIT_V1.json").read_text())
        cls.inventory = json.loads((ROOT / cls.report["inventory_ref"]).read_text())
        cls.records = json.loads((cls.directory / "RECORDS_V1.json").read_text())

    def test_whole_record_set_validates_but_remains_open(self):
        result = audit(self.inventory, self.records)
        self.assertEqual(result["status"], "OPEN")
        self.assertGreater(result["remaining_semantic_review_units"], 4000)
        self.assertFalse(result["repository_learning_closed"])

    def test_dropped_surface_cannot_reduce_denominator(self):
        changed = copy.deepcopy(self.inventory); changed["entries"].pop()
        with self.assertRaisesRegex(ValueError, "INVENTORY_TREE_MISMATCH"):
            audit(changed, self.records)

    def test_stale_source_pin_is_rejected(self):
        rows = copy.deepcopy(self.records); rows[0]["source_paths"][0]["sha"] = "0" * 40
        with self.assertRaisesRegex(ValueError, "SOURCE_PATH_PIN_DRIFT"):
            audit(self.inventory, rows)

    def test_source_pass_cannot_promote_destination_record(self):
        rows = copy.deepcopy(self.records); rows[0]["maturity"] = "L5_RUNTIME_DEFAULT"
        with self.assertRaisesRegex(ValueError, "PROMOTION_NOT_SUPPORTED"):
            audit(self.inventory, rows)

    def test_presence_cannot_close_learning(self):
        rows = copy.deepcopy(self.records); rows[0]["repository_learning_closed"] = True
        with self.assertRaisesRegex(ValueError, "CLOSURE_REQUIRES"):
            audit(self.inventory, rows)

    def test_hard_negative_excludes_otherwise_matching_method(self):
        result = retrieve(self.inventory, self.records,
                          ["resource-cleanup", "primary-error", "no-owned-resource"])
        row = next(r for r in result["candidates"] if r["id"] == "REA-LRN-002")
        self.assertEqual(row["state"], "EXCLUDED")

    def test_missing_context_is_not_pass(self):
        self.assertTrue(all(r["state"] == "NEEDS_CONTEXT"
                            for r in retrieve(self.inventory, self.records, [])["candidates"]))

    def test_positive_match_changes_consumer_brief(self):
        before = retrieve(self.inventory, self.records, [])
        after = retrieve(self.inventory, self.records, ["resource-cleanup", "primary-error"])
        self.assertNotEqual(before, after)
        row = next(r for r in after["candidates"] if r["id"] == "REA-LRN-002")
        self.assertEqual(row["state"], "REVIEW_REQUIRED")
        self.assertIn("primary", row["consumer_effect"])

    def test_evidence_is_create_only_and_corruption_is_not_repaired_in_place(self):
        with tempfile.TemporaryDirectory() as d:
            first = preserve(d, {"status": "FAIL"}); red = first.read_bytes()
            second = preserve(d, {"status": "PASS", "predecessor": first.name})
            self.assertNotEqual(first, second); self.assertEqual(first.read_bytes(), red)
            first.write_text("corrupted")
            with self.assertRaisesRegex(ValueError, "EXISTING_EVIDENCE_CORRUPTED"):
                preserve(d, {"status": "FAIL"})

    def test_empty_corpus_is_not_vacuously_valid(self):
        with self.assertRaisesRegex(ValueError, "EMPTY_LEARNING_CORPUS"):
            audit(self.inventory, [])

    def test_preserved_campaign_custody(self):
        index = json.loads((self.directory / "CUSTODY_V1.json").read_text())
        self.assertEqual(verify_custody(ROOT, index)["status"], "VERIFIED_BYTES_ONLY")
        bad = copy.deepcopy(index); bad["files"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "EVIDENCE_BYTES_DRIFT"):
            verify_custody(ROOT, bad)

    def test_custody_path_escape_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "UNSAFE_EVIDENCE_PATH"):
            verify_custody(ROOT, {"files": [{"path": "../outside", "sha256": "0" * 64, "bytes": 0}]})

    def test_failure_without_hard_negative_is_rejected(self):
        rows = copy.deepcopy(self.records); rows[0]["analysis"]["hard_negatives"] = []
        with self.assertRaisesRegex(ValueError, "INCOMPLETE_FAILURE_ANALYSIS"):
            audit(self.inventory, rows)

    def test_immutable_git_scan_ignores_dirty_worktree(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            def git(*args):
                return subprocess.check_output(["git", "-C", str(root), *args])
            git("init", "-q"); git("config", "user.name", "Fixture"); git("config", "user.email", "fixture@example.invalid")
            (root / "code.py").write_text("raise ValueError('example')\n")
            git("add", "code.py"); git("commit", "-qm", "fixture")
            commit = git("rev-parse", "HEAD").decode().strip()
            before = scan(root, commit, "fixture/repository")
            (root / "code.py").write_text("different worktree\n")
            self.assertEqual(before, scan(root, commit, "fixture/repository"))
            self.assertEqual(before["entries"][0]["signal_lines"]["error"], [1])
            self.assertEqual(before["semantic_exhaustion"], "NOT_ESTABLISHED")


if __name__ == "__main__":
    unittest.main()
