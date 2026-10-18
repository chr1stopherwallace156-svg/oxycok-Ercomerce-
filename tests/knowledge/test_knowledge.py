import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts/knowledge/knowledge.py"
spec = importlib.util.spec_from_file_location("knowledge", SCRIPT)
knowledge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(knowledge)


class KnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.manifest, self.catalog = knowledge.load(ROOT)

    def query(self, **kwargs):
        args = dict(domain="commerce", mechanisms=["evidence-consumption"],
                    facts=["artifact-produced", "downstream-consumer"])
        args.update(kwargs)
        return knowledge.retrieve(self.manifest, self.catalog, **args)

    def test_positive_mechanism_with_traceable_sources(self):
        result = self.query()
        self.assertEqual(result["lessons"][0]["disposition"], "APPLICABLE_CANDIDATE")
        self.assertEqual(result["sources"][0]["id"], "industrial-028")
        self.assertFalse(result["action_authorized"])
        self.assertEqual(result["authority"], "NONE")

    def test_missing_context_stays_unknown(self):
        result = self.query(facts=["artifact-produced"])
        lesson = result["lessons"][0]
        self.assertEqual(lesson["disposition"], "NEEDS_CONTEXT")
        self.assertEqual(lesson["missing_facts"], ["downstream-consumer"])

    def test_hard_negative_overrides_positive(self):
        result = self.query(facts=["artifact-produced", "downstream-consumer",
                                   "storage-only-contract"])
        self.assertEqual(result["lessons"][0]["disposition"], "EXCLUDED")

    def test_counterfactual_retrieval_changes_semantic_context(self):
        positive = self.query()
        withheld = self.query(mechanisms=["unknown-mechanism"])
        def consumer(result):
            return [row["tests"] for row in result["lessons"]
                    if row["disposition"] == "APPLICABLE_CANDIDATE"]
        self.assertTrue(consumer(positive))
        self.assertEqual(consumer(withheld), [])
        # This proves only this test consumer, not the commerce runtime.
        self.assertEqual(withheld["status"], "NO_MATCH")

    def test_open_domain_does_not_claim_universal_proof(self):
        result = self.query(domain="unseen-laboratory-scheduling")
        self.assertEqual(result["target_domain"], "unseen-laboratory-scheduling")
        self.assertEqual(result["lessons"][0]["target_status"], "TRANSFER_CANDIDATE")
        self.assertEqual(result["coverage"], "BOUNDED_SEED_NOT_EXHAUSTIVE")

    def test_unrelated_facts_do_not_change_applicability(self):
        result = self.query(facts=["artifact-produced", "downstream-consumer",
                                   "unrelated-marketing-observation"])
        self.assertEqual(result["lessons"][0]["disposition"], "APPLICABLE_CANDIDATE")

    def test_systemic_repair_excludes_independently_bounded_local_bug(self):
        result = self.query(mechanisms=["systemic-repair"],
                            facts=["repeated-same-family-fresh-failure",
                                   "transitive-effects", "independently-bounded-local-bug"])
        self.assertEqual(result["lessons"][0]["disposition"], "EXCLUDED")

    def altered(self, mutate):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(ROOT / "docs/knowledge_transfer", root / "docs/knowledge_transfer")
            shutil.copytree(ROOT / "knowledge", root / "knowledge")
            mutate(root)
            with self.assertRaises(knowledge.KnowledgeError):
                knowledge.load(root)

    def catalog_mutation(self, mutate):
        def change(root):
            path = root / "knowledge/lessons.json"
            data = json.loads(path.read_text())
            mutate(data)
            path.write_text(json.dumps(data))
        self.altered(change)

    def test_corrupted_source_is_blocked(self):
        self.altered(lambda root: (root / next(s["snapshot"] for s in self.manifest["sources"] if "snapshot" in s)).write_text("changed"))

    def test_duplicate_lesson_id_is_blocked(self):
        self.catalog_mutation(lambda data: data["lessons"].append(copy.deepcopy(data["lessons"][0])))

    def test_forged_target_qualification_is_blocked(self):
        self.catalog_mutation(lambda data: data["lessons"][0].update(target_status="QUALIFIED"))

    def test_unknown_source_is_blocked(self):
        self.catalog_mutation(lambda data: data["lessons"][0].update(sources=["invented-source"]))

    def test_vacuous_applicability_is_blocked(self):
        self.catalog_mutation(lambda data: data["lessons"][0].update(requires_all=[]))

    def test_source_blob_identity_is_checked_even_if_sha256_updated(self):
        def change(root):
            path = root / "docs/knowledge_transfer/source_manifest.json"
            data = json.loads(path.read_text())
            source = next(s for s in data["sources"] if "snapshot" in s)
            (root / source["snapshot"]).write_bytes(b"substitution")
            source["snapshot_sha256"] = hashlib.sha256(b"substitution").hexdigest()
            path.write_text(json.dumps(data))
        self.altered(change)

    def test_snapshot_path_escape_is_blocked(self):
        def change(root):
            path = root / "docs/knowledge_transfer/source_manifest.json"
            data = json.loads(path.read_text())
            next(s for s in data["sources"] if "snapshot" in s)["snapshot"] = "../outside.txt"
            path.write_text(json.dumps(data))
        self.altered(change)

    def test_duplicate_json_key_is_blocked(self):
        self.altered(lambda root: (root / "knowledge/lessons.json").write_text(
            '{"version":1,"version":1,"authority":"NONE","lessons":[]}'))

    def test_private_source_bytes_are_not_accepted(self):
        def change(root):
            path = root / "docs/knowledge_transfer/source_manifest.json"
            data = json.loads(path.read_text())
            data["sources"][0]["content"] = "private original text"
            path.write_text(json.dumps(data))
        self.altered(change)

    def test_private_pins_and_public_snapshot_have_distinct_validation(self):
        private = [s for s in self.manifest["sources"] if s["evidence_mode"] == "PRIVATE_REFERENCE_PIN_ONLY"]
        public = [s for s in self.manifest["sources"] if s["evidence_mode"] == "PUBLIC_EXACT_SNAPSHOT"]
        self.assertEqual(len(private), 6)
        self.assertEqual(len(public), 1)
        self.assertTrue(all("snapshot" not in s for s in private))

    def test_empty_query_is_blocked(self):
        with self.assertRaises(knowledge.KnowledgeError):
            self.query(mechanisms=[])
        with self.assertRaises(knowledge.KnowledgeError):
            self.query(domain="")

    def test_separate_process_replay_is_deterministic_and_read_only(self):
        before = {p: hashlib.sha256(p.read_bytes()).hexdigest()
                  for folder in ["knowledge", "docs/knowledge_transfer"]
                  for p in (ROOT / folder).rglob("*") if p.is_file()}
        command = [sys.executable, str(SCRIPT), "retrieve", "--domain", "commerce",
                   "--mechanism", "evidence-consumption", "--fact", "artifact-produced",
                   "--fact", "downstream-consumer"]
        first = subprocess.run(command, cwd=tempfile.gettempdir(), capture_output=True, check=True)
        second = subprocess.run(command, cwd=tempfile.gettempdir(), capture_output=True, check=True)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(json.loads(first.stdout)["authority"], "NONE")
        self.assertEqual(before, {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in before})


if __name__ == "__main__":
    unittest.main()
