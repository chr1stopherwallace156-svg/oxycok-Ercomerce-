import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/mission"))
sys.path.insert(0, str(ROOT / "scripts/reconstruction"))
import campaign as reconstruction_campaign
import nordvpn_application
import providers


class NordVpnApplicationTests(unittest.TestCase):
    def setUp(self):
        self.surface = ROOT / "tests/mission/fixtures/owned_nordvpn_surface"
        self.rights = nordvpn_application.load_rights()

    def test_rights_bind_rea_method_and_owned_surface(self):
        self.assertEqual(self.rights["method_reference"]["repository"], "morluto/rea")
        self.assertEqual(self.rights["destination_domain"], "nordvpn")
        self.assertEqual(self.rights["authority"], "NONE")
        pinned = self.rights["authorized_targets"][0]["subject_sha256"]
        self.assertEqual(pinned, providers.inventory(self.surface)["sha256"])

    def test_owned_surface_is_admitted(self):
        admission = nordvpn_application.admit_target(self.surface, self.rights)
        self.assertEqual(admission["disposition"], "AUTHORIZED")
        self.assertEqual(admission["authorization_id"], "AUTH-OWNED-SURFACE-001")

    def test_proprietary_named_path_is_blocked(self):
        with tempfile.TemporaryDirectory(prefix="nordvpn-client-") as tmp:
            Path(tmp, "app.bin").write_text("not authorized")
            with self.assertRaisesRegex(ValueError, "PROPRIETARY_NORDVPN_TARGET_NOT_AUTHORIZED"):
                nordvpn_application.admit_target(tmp, self.rights)

    def test_unlisted_path_is_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "session.py").write_text("def x():\n    return 1\n")
            with self.assertRaisesRegex(ValueError, "ANALYSIS_TARGET_NOT_AUTHORIZED"):
                nordvpn_application.admit_target(tmp, self.rights)

    def test_subject_drift_on_authorized_path_is_blocked(self):
        rights = json.loads(json.dumps(self.rights))
        rights["authorized_targets"][0]["subject_sha256"] = "a" * 64
        with self.assertRaisesRegex(ValueError, "AUTHORIZED_TARGET_SUBJECT_DRIFT"):
            nordvpn_application.admit_target(self.surface, rights)

    def test_campaign_audit_stays_open_and_not_qualified(self):
        census = reconstruction_campaign.read(
            ROOT / "reconstruction/subjects/nordvpn/CENSUS_V1.json")
        plan = reconstruction_campaign.read(
            ROOT / "reconstruction/subjects/nordvpn/CAMPAIGN_V1.json")
        result = reconstruction_campaign.audit(census, plan)
        self.assertEqual(result["status"], "RECONSTRUCTION_OPEN")
        self.assertEqual(result["independent_qualification"], "NOT_GRANTED")
        self.assertEqual(result["originality_and_legal_clearance"], "NOT_ESTABLISHED")
        self.assertEqual(plan["domain"], "nordvpn")
        self.assertEqual(plan["rights"]["nordvpn_product_inspection"], "NOT_AUTHORIZED")

    def test_rehearsal_completes_without_claiming_product_re(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = nordvpn_application.rehearse(tmp, self.surface, max_steps=6)
        self.assertEqual(result["mission"]["stage"], "COMPLETE")
        self.assertEqual(result["claims"]["nordvpn_product_reverse_engineering"],
                         "NOT_PERFORMED")
        self.assertEqual(result["claims"]["legal_clearance"], "NOT_ESTABLISHED")
        self.assertEqual(result["mission"]["request"]["domain"], "nordvpn")

    def test_cli_blocks_proprietary_target(self):
        with tempfile.TemporaryDirectory(prefix="nordvpn-") as tmp:
            Path(tmp, "x").write_text("x")
            proc = subprocess.run(
                [sys.executable, str(ROOT / "scripts/mission/nordvpn_application.py"),
                 "admit", "--target", tmp],
                capture_output=True, text=True)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("PROPRIETARY_NORDVPN_TARGET_NOT_AUTHORIZED", proc.stderr)


if __name__ == "__main__":
    unittest.main()
