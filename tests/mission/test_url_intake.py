import json
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from urllib import error, request

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/mission"))
import url_intake


class UrlIntakeTests(unittest.TestCase):
    def test_rea_github_url_selects_method_without_rehearsal(self):
        result = url_intake.resolve_url(
            "https://github.com/morluto/rea", rehearse=False)
        self.assertEqual(result["status"], "READY")
        self.assertEqual(result["disposition"], "METHOD_REFERENCE_SELECTED")
        self.assertEqual(result["method"]["repository"], "morluto/rea")
        self.assertEqual(result["domain"], "nordvpn")

    def test_rea_url_variants_normalize(self):
        result = url_intake.resolve_url(
            "github.com/morluto/rea.git", rehearse=False)
        self.assertEqual(result["url"], "https://github.com/morluto/rea")

    def test_rea_url_can_rehearse_owned_surface(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = url_intake.resolve_url(
                "https://github.com/morluto/rea/",
                rehearse=True,
                state_root=tmp,
            )
        self.assertEqual(result["status"], "READY")
        self.assertEqual(result["rehearsal"]["stage"], "COMPLETE")
        self.assertEqual(
            result["claims"]["nordvpn_product_reverse_engineering"],
            "NOT_PERFORMED",
        )

    def test_nordvpn_product_url_is_blocked(self):
        with self.assertRaisesRegex(ValueError, "PROPRIETARY_NORDVPN_URL_NOT_AUTHORIZED"):
            url_intake.resolve_url("https://nordvpn.com/download", rehearse=False)

    def test_unknown_url_is_blocked(self):
        with self.assertRaisesRegex(ValueError, "URL_NOT_AUTHORIZED"):
            url_intake.resolve_url("https://example.com/app", rehearse=False)

    def test_http_server_serves_page_and_start_api(self):
        server = url_intake.ThreadingHTTPServer(
            ("127.0.0.1", 0), url_intake.IntakeHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        host, port = server.server_address
        try:
            page = request.urlopen(f"http://{host}:{port}/", timeout=5).read()
            self.assertIn(b"Paste a URL", page)
            self.assertIn(b"OXY", page)
            self.assertIn(b'method="post"', page.lower())
            req = request.Request(
                f"http://{host}:{port}/api/start",
                data=json.dumps({
                    "url": "https://github.com/morluto/rea",
                    "rehearse": False,
                }).encode(),
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                method="POST",
            )
            body = json.loads(request.urlopen(req, timeout=10).read())
            self.assertEqual(body["disposition"], "METHOD_REFERENCE_SELECTED")
            form = request.Request(
                f"http://{host}:{port}/api/start",
                data=b"url=https%3A%2F%2Fgithub.com%2Fmorluto%2Frea&rehearse=0",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                method="POST",
            )
            form_resp = request.urlopen(form, timeout=10)
            self.assertIn("text/html", form_resp.headers.get("Content-Type", ""))
            html = form_resp.read()
            self.assertIn(b"<h1>Ready</h1>", html)
            self.assertIn(b"REA selected", html)
            with self.assertRaises(error.HTTPError) as ctx:
                bad = request.Request(
                    f"http://{host}:{port}/api/start",
                    data=json.dumps({"url": "https://nordvpn.com"}).encode(),
                    headers={
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    },
                    method="POST",
                )
                request.urlopen(bad, timeout=5)
            self.assertEqual(ctx.exception.code, 403)
        finally:
            server.shutdown()
            server.server_close()


    def test_cli_resolve_blocks_unauthorized(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts/mission/url_intake.py"),
             "resolve", "--url", "https://example.com", "--no-rehearse"],
            capture_output=True, text=True,
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("URL_NOT_AUTHORIZED", proc.stderr)


if __name__ == "__main__":
    unittest.main()
