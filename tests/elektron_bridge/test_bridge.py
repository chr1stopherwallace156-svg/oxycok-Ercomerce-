import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/"scripts/elektron_bridge"))
import snapshot
import run_owner


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root/"source"
        self.source.mkdir()
        self.git("init","-q")
        (self.source/"module.py").write_text("value = 1\n")
        (self.source/"docs").mkdir()
        (self.source/"docs/.hidden").write_text("record\n")
        self.git("add",".")
        self.git("-c","user.name=fixture","-c","user.email=fixture@example.invalid","commit","-qm","fixture")
        self.commit = self.git("rev-parse","HEAD").decode().strip()

    def tearDown(self):
        self.temp.cleanup()

    def git(self,*args):
        return subprocess.check_output(["git","-C",str(self.source),*args],stderr=subprocess.DEVNULL)

    def stage(self):
        return snapshot.stage(self.source,self.commit,self.root/"copy","example/source")

    def records(self):
        return [{"source_record":"records/"+rid+"-example.json"}
                for rid in ["RFL-2026-022","RFL-2026-024","RFL-2026-028","RFL-2026-032"]]

    def test_full_immutable_snapshot_includes_hidden_files_and_preserves_dirty_source(self):
        (self.source/"module.py").write_text("dirty work preserved\n")
        before=self.git("status","--porcelain")
        manifest=self.stage()
        self.assertEqual((self.root/"copy/module.py").read_text(),"value = 1\n")
        self.assertTrue((self.root/"copy/docs/.hidden").exists())
        self.assertEqual(before,self.git("status","--porcelain"))
        self.assertEqual((self.source/"module.py").read_text(),"dirty work preserved\n")
        self.assertEqual(snapshot.verify(self.root/"copy")["source_tree"],manifest["source_tree"])

    def test_source_overlap_is_rejected_before_mutation(self):
        with self.assertRaisesRegex(ValueError,"OVERLAP"):
            snapshot.stage(self.source,self.commit,self.source/"copy","example/source")
        self.assertFalse((self.source/"copy").exists())

    def test_existing_destination_never_overwritten(self):
        self.stage()
        with self.assertRaisesRegex(ValueError,"MUST_BE_NEW"):
            self.stage()

    def test_budget_is_not_silent_partial_transfer(self):
        with self.assertRaisesRegex(ValueError,"BUDGET"):
            snapshot.stage(self.source,self.commit,self.root/"copy","example/source",1)
        self.assertFalse((self.root/"copy").exists())

    def test_changed_blob_invalidates_snapshot(self):
        self.stage()
        (self.root/"copy/module.py").write_text("changed")
        with self.assertRaisesRegex(ValueError,"CONTENT_DRIFT"):
            snapshot.verify(self.root/"copy")

    def test_executable_mode_drift_invalidates_snapshot(self):
        self.stage()
        (self.root/"copy/module.py").chmod(0o755)
        with self.assertRaisesRegex(ValueError,"MODE_DRIFT"):
            snapshot.verify(self.root/"copy")

    def test_undeclared_file_invalidates_snapshot(self):
        self.stage()
        (self.root/"copy/extra").write_text("unrecorded")
        with self.assertRaisesRegex(ValueError,"UNDECLARED"):
            snapshot.verify(self.root/"copy")

    def test_bounded_analysis_copy_cannot_claim_full_transfer(self):
        self.stage()
        p=self.root/"copy"/snapshot.MANIFEST
        manifest=json.loads(p.read_text());manifest["scope"]="BOUNDED_ANALYSIS_CLOSURE"
        p.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError,"FULL_TRANSFER"):
            snapshot.verify(self.root/"copy")
        self.assertEqual(snapshot.verify(self.root/"copy",True)["scope"],"BOUNDED_ANALYSIS_CLOSURE")

    def test_mutated_manifest_cannot_hide_deleted_file_from_full_tree(self):
        self.stage()
        p=self.root/"copy"/snapshot.MANIFEST
        manifest=json.loads(p.read_text());manifest["files"].pop("module.py")
        (self.root/"copy/module.py").unlink();p.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError,"TREE_IDENTITY"):
            snapshot.verify(self.root/"copy")

    def test_source_symlink_is_explicitly_blocked(self):
        (self.source/"link").symlink_to("module.py")
        self.git("add","link")
        self.git("-c","user.name=fixture","-c","user.email=fixture@example.invalid","commit","-qm","symlink")
        commit=self.git("rev-parse","HEAD").decode().strip()
        with self.assertRaisesRegex(ValueError,"UNSUPPORTED_SOURCE_ENTRY"):
            snapshot.stage(self.source,commit,self.root/"copy","example/source")

    def test_known_subject_failure_blocks_a_different_domain(self):
        result=run_owner.failure_preflight({"payload":{"domain":"unseen-domain",
            "current_subject":"new","exam_subject":"old"}},self.records())
        self.assertEqual(result["blockers"][0]["lesson"],"RFL-2026-022")

    def test_known_evidence_nonconsumption_is_not_hidden_by_presence(self):
        result=run_owner.failure_preflight({"payload":{"evidence_produced":True,
            "consumer_semantic_effect_observed":False}},self.records())
        self.assertEqual(result["blockers"][0]["lesson"],"RFL-2026-028")

    def test_negative_case_does_not_activate_systemic_repair_escalation(self):
        result=run_owner.failure_preflight({"payload":{"fresh_same_family_failures":1}},self.records())
        self.assertEqual(result["blockers"],[])

    def test_repeated_family_requires_surface_but_not_a_fixture_answer(self):
        red=run_owner.failure_preflight({"payload":{"fresh_same_family_failures":2}},self.records())
        allowed=run_owner.failure_preflight({"payload":{"fresh_same_family_failures":2,
            "frozen_effect_surface_ref":"new-domain-evidence"}},self.records())
        self.assertEqual(red["blockers"][0]["lesson"],"RFL-2026-032")
        self.assertEqual(allowed["blockers"],[])

    def test_missing_failure_memory_never_becomes_empty_green(self):
        with self.assertRaisesRegex(ValueError,"CORPUS_INCOMPLETE"):
            run_owner.failure_preflight({"payload":{}},[])

    def test_unknown_facts_are_not_called_a_pass(self):
        result=run_owner.failure_preflight({"payload":{}},self.records())
        self.assertIn("MISSING_CONTEXT",result["untriggered_rules"])
        self.assertNotIn("PASS",result["untriggered_rules"].split("_")[:1])

    def test_dead_letter_object_is_not_success(self):
        red = {"admitted":True,"work_item":{"current_stage":"DEAD_LETTER", "last_error":"grammar"}}
        with self.assertRaises(run_owner.CoreResultError) as raised:
            run_owner.require_usable_core_result(red)
        self.assertEqual(raised.exception.source_result,red)

    def test_independent_review_boundary_is_not_mislabeled_qualification(self):
        pending={"admitted":True,"work_item":{"current_stage":"REVIEW_PENDING_INDEPENDENT",
                                             "last_error":None,"failed_stages":[]}}
        self.assertEqual(run_owner.require_usable_core_result(pending),pending)
        with self.assertRaises(run_owner.CoreResultError):
            run_owner.require_usable_core_result({"admitted":False})

    def test_exam_configuration_escape_reuses_existing_failure_family(self):
        result=run_owner.failure_preflight({"payload":{"production_mode":True,
            "exam_override_active":True}},self.records())
        self.assertEqual(result["blockers"][0]["lesson"],"RFL-2026-024")


if __name__=="__main__":
    unittest.main()
