import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/reconstruction"))
import campaign


class CampaignTests(unittest.TestCase):
    def setUp(self):
        self.census = {"version": 1, "kind": "PINNED_REPOSITORY_CENSUS",
                       "repository": "example/unfamiliar", "commit": "a"*40,
                       "tree_sha": "b"*40, "upstream_truncated": False,
                       "entries": [{"path": "source.py", "type": "blob", "sha": "c"*40, "mode": "100644"},
                                   {"path": "external", "type": "commit", "sha": "d"*40, "mode": "160000"}]}
        self.plan = campaign.create(self.census, "unseen-scientific-domain", ["Inspect"])

    def test_domain_is_a_parameter_and_enumeration_is_not_understanding(self):
        result = campaign.audit(self.census, self.plan)
        self.assertEqual(result["pending_review_count"], 2)
        self.assertEqual(result["status"], "RECONSTRUCTION_OPEN")
        self.assertEqual(result["independent_qualification"], "NOT_GRANTED")
        self.assertEqual(self.plan["domain"], "unseen-scientific-domain")

    def test_truncated_tree_cannot_be_whole_repository(self):
        self.census["upstream_truncated"] = True
        with self.assertRaisesRegex(ValueError, "TRUNCATED"):
            campaign.create(self.census, "another-domain", ["Inspect"])

    def test_changed_census_invalidates_existing_campaign(self):
        self.census["entries"][0]["sha"] = "e"*40
        with self.assertRaisesRegex(ValueError, "BINDING_DRIFT"):
            campaign.audit(self.census, self.plan)

    def test_file_review_cannot_borrow_another_blob(self):
        self.plan["file_reviews"]["source.py"] = {
            "source_sha": "e"*40, "disposition": "ANALYZED",
            "basis": "review", "evidence_refs": ["source"], "mechanism_summary": "method"}
        with self.assertRaisesRegex(ValueError, "REVIEW_SUBJECT_DRIFT"):
            campaign.audit(self.census, self.plan)

    def test_exclusion_does_not_become_full_understanding(self):
        self.plan["file_reviews"]["source.py"] = {
            "source_sha": "c"*40, "disposition": "EXCLUDED_WITH_BASIS",
            "basis": "declared exclusion", "evidence_refs": ["decision"]}
        result = campaign.audit(self.census, self.plan)
        self.assertEqual(result["excluded_count"], 1)
        self.assertEqual(result["pending_review_count"], 1)
        self.assertEqual(result["whole_source_semantic_understanding"],
                         "NOT_ESTABLISHED_BY_STRUCTURAL_AUDIT")

    def test_submodule_pin_is_not_its_contents(self):
        self.plan["file_reviews"]["external"] = {
            "source_sha": "d"*40, "disposition": "ANALYZED", "basis": "review",
            "evidence_refs": ["pointer"], "mechanism_summary": "external behavior"}
        with self.assertRaisesRegex(ValueError, "SUBMODULE_CONTENT"):
            campaign.audit(self.census, self.plan)

    def test_unknown_graph_owner_blocks(self):
        self.plan["graph_edges"] = [{"from":"CAP-001", "to":"invented", "relation":"DEPENDS_ON"}]
        with self.assertRaisesRegex(ValueError, "UNBOUND_GRAPH"):
            campaign.audit(self.census, self.plan)

    def test_qualified_label_does_not_replace_evidence(self):
        self.plan["capabilities"][0]["qualification"]["status"] = "QUALIFIED"
        with self.assertRaisesRegex(ValueError, "QUALIFICATION_NOT_GRANTED"):
            campaign.audit(self.census, self.plan)

    def test_originality_is_not_inferred_from_implementation_label(self):
        cap = self.plan["capabilities"][0]
        cap["implementation"] = {"status": "CANDIDATE", "subject_sha256":"e"*64,
                                 "artifact_refs":["candidate"]}
        result = campaign.audit(self.census, self.plan)
        self.assertEqual(result["originality_and_legal_clearance"], "NOT_ESTABLISHED")
        self.assertEqual(result["status"], "RECONSTRUCTION_OPEN")

    def test_duplicate_paths_are_rejected(self):
        self.census["entries"].append(copy.deepcopy(self.census["entries"][0]))
        with self.assertRaisesRegex(ValueError, "DUPLICATE_PATH"):
            campaign.validate_census(self.census)

    def test_cli_never_overwrites_existing_campaign(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/"census.json").write_text(json.dumps(self.census))
            (root/"out.json").write_text("preserve")
            proc = subprocess.run([sys.executable, str(ROOT/"scripts/reconstruction/campaign.py"),
                "--census", str(root/"census.json"), "new", "--domain", "other",
                "--capability", "Inspect", "--output", str(root/"out.json")],
                capture_output=True)
            self.assertEqual(proc.returncode, 2)
            self.assertEqual((root/"out.json").read_text(), "preserve")

    def test_complete_worker_records_can_progress_without_claiming_qualification(self):
        for row in self.census["entries"]:
            self.plan["file_reviews"][row["path"]] = {
                "source_sha": row["sha"], "disposition": "ANALYZED", "basis": "worker review",
                "evidence_refs": ["record"], "mechanism_summary": "bounded mechanism",
                "nested_campaign_ref": "nested worker record"}
        cap = self.plan["capabilities"][0]
        cap["reference_paths"] = ["source.py"]
        cap["contract"] = {key:["declared behavior"] for key in campaign.CONTRACT_FIELDS}
        cap["design"] = {key:"worker-authored design" for key in campaign.DESIGN_FIELDS}
        cap["implementation"] = {"status":"CANDIDATE", "subject_sha256":"f"*64,
                                 "artifact_refs":["candidate"]}
        cap["qualification"] = {"status":"WORKER_RECORDED", "evidence_refs":["run"],
                                "broken_control_refs":["red"], "holdout_refs":["holdout"]}
        self.plan["lessons"] = [{key:"worker evidence" for key in
            ("failure", "positive_method", "hard_negative", "inheritance", "evidence_ref")}]
        result = campaign.audit(self.census, self.plan)
        self.assertEqual(result["status"], "WORKER_RECORDS_READY_FOR_INDEPENDENT_REVIEW")
        self.assertEqual(result["independent_qualification"], "NOT_GRANTED")
        self.assertEqual(result["originality_and_legal_clearance"], "NOT_ESTABLISHED")

    def test_entry_type_cannot_hide_a_file_as_a_directory(self):
        self.census["entries"][0]["type"] = "tree"
        with self.assertRaisesRegex(ValueError, "TYPE_MODE"):
            campaign.validate_census(self.census)

    def test_open_audit_cli_returns_nonzero_instead_of_false_green(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/"census.json").write_text(json.dumps(self.census))
            (root/"plan.json").write_text(json.dumps(self.plan))
            proc = subprocess.run([sys.executable, str(ROOT/"scripts/reconstruction/campaign.py"),
                "--census", str(root/"census.json"), "audit", "--campaign", str(root/"plan.json")],
                capture_output=True)
            self.assertEqual(proc.returncode, 3)
            self.assertEqual(json.loads(proc.stdout)["status"], "RECONSTRUCTION_OPEN")

    def test_positive_negative_learning_is_required(self):
        result = campaign.audit(self.census, self.plan)
        self.assertTrue(any("positive_negative_learning" in row["missing"]
                            for row in result["capability_gaps"]))


if __name__ == "__main__":
    unittest.main()
