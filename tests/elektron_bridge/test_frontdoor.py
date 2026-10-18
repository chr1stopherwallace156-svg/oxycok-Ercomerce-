import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location("oxycok_entry",ROOT/"scripts/oxycok.py")
entry=importlib.util.module_from_spec(spec);spec.loader.exec_module(entry)


class FrontdoorTests(unittest.TestCase):
    def config(self):
        return {"snapshot":"/private/core","state_root":"/private/state","allow_bounded_analysis":False}

    def test_standard_start_always_selects_configured_core(self):
        command=entry.command(self.config(),"start",["--domain","unfamiliar"])
        self.assertIn("--elektron-snapshot",command)
        self.assertEqual(command[command.index("--elektron-snapshot")+1],"/private/core")

    def test_caller_cannot_silently_remove_core_selection(self):
        with self.assertRaisesRegex(ValueError,"OVERRIDDEN"):
            entry.command(self.config(),"start",["--elektron-snapshot=/different"])

    def test_missing_config_is_not_standalone_fallback(self):
        with self.assertRaises(OSError):
            entry.load_config("/nonexistent/oxycok-config")

    def test_incomplete_config_is_blocked(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"config.json";path.write_text(json.dumps({"version":1,"source_commit":entry.SOURCE_COMMIT}))
            with self.assertRaisesRegex(ValueError,"CORE_AND_STATE"):
                entry.load_config(path)

    def test_bounded_analysis_requires_explicit_saved_configuration(self):
        config=self.config()
        self.assertNotIn("--elektron-allow-bounded-analysis",entry.command(config,"start",[]))
        config["allow_bounded_analysis"]=True
        self.assertIn("--elektron-allow-bounded-analysis",entry.command(config,"start",[]))


if __name__=="__main__":
    unittest.main()
