#!/usr/bin/env python3
"""iPhone-simple URL intake for the REA → Nord VPN application seed.

Paste a URL. Known REA method URL selects the method and can run the owned
rehearsal. Unauthorized product URLs stay blocked.
"""
from __future__ import annotations

import argparse
import json
import re
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
WEB_ROOT = ROOT / "web" / "rea-intake"
import sys

sys.path.insert(0, str(ROOT / "scripts/mission"))
import nordvpn_application

REA_METHOD_HOST = "github.com"
URL_RE = re.compile(r"^https?://", re.IGNORECASE)


def normalize_url(raw):
    if not isinstance(raw, str) or not raw.strip():
        raise ValueError("URL_REQUIRED")
    text = raw.strip()
    if text.startswith("github.com/"):
        text = "https://" + text
    if not URL_RE.match(text):
        raise ValueError("URL_MUST_BE_HTTP_OR_HTTPS")
    parsed = urlparse(text)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("URL_INVALID")
    if parsed.username or parsed.password:
        raise ValueError("URL_USERINFO_FORBIDDEN")
    path = parsed.path.rstrip("/") or ""
    if path.endswith(".git"):
        path = path[:-4]
    normalized = f"{parsed.scheme.lower()}://{parsed.netloc.lower()}{path}"
    return normalized, parsed


def is_rea_method_url(normalized, parsed):
    host = parsed.netloc.lower()
    path = (parsed.path.rstrip("/") or "").lower()
    if path.endswith(".git"):
        path = path[:-4]
    return host == REA_METHOD_HOST and path in {"/morluto/rea"}


def resolve_url(raw, rehearse=True, state_root=None):
    normalized, parsed = normalize_url(raw)
    rights = nordvpn_application.load_rights()
    if is_rea_method_url(normalized, parsed):
        result = {
            "status": "READY",
            "authority": "NONE",
            "disposition": "METHOD_REFERENCE_SELECTED",
            "url": normalized,
            "method": {
                "name": "REA",
                "repository": "morluto/rea",
                "commit": rights["method_reference"]["commit"],
                "source_url": "https://github.com/morluto/rea",
            },
            "domain": "nordvpn",
            "message": "REA selected as the method reference.",
            "claims": {
                "nordvpn_product_reverse_engineering": "NOT_PERFORMED",
                "legal_clearance": "NOT_ESTABLISHED",
                "independent_qualification": "NOT_GRANTED",
            },
        }
        if rehearse:
            root = Path(state_root) if state_root else Path(
                tempfile.mkdtemp(prefix="oxycok-url-intake-"))
            rehearsal = nordvpn_application.rehearse(
                root, nordvpn_application.OWNED_SURFACE, rights=rights)
            result["rehearsal"] = {
                "state_root": str(root),
                "mission_id": rehearsal["mission"]["mission_id"],
                "stage": rehearsal["mission"]["stage"],
                "admission": rehearsal["admission"],
            }
            result["message"] = (
                "REA selected. Authorized owned-surface rehearsal finished."
                if rehearsal["mission"]["stage"] == "COMPLETE"
                else "REA selected. Rehearsal did not complete.")
            if rehearsal["mission"]["stage"] != "COMPLETE":
                result["status"] = "BLOCKED"
                result["error"] = rehearsal["mission"].get("error") or "REHEARSAL_INCOMPLETE"
        return result

    host = parsed.netloc.lower()
    if "nordvpn" in host or "nordsecurity" in host:
        raise ValueError("PROPRIETARY_NORDVPN_URL_NOT_AUTHORIZED")
    raise ValueError("URL_NOT_AUTHORIZED")


class IntakeHandler(BaseHTTPRequestHandler):
    server_version = "OXYCOKUrlIntake/1.0"

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def _send(self, code, body, content_type="application/json; charset=utf-8"):
        payload = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            page = (WEB_ROOT / "index.html").read_bytes()
            return self._send(200, page, "text/html; charset=utf-8")
        if path == "/health":
            return self._send(200, json.dumps({"status": "ok", "authority": "NONE"}))
        return self._send(404, json.dumps({"status": "BLOCKED", "error": "NOT_FOUND"}))

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        if path != "/api/start":
            return self._send(404, json.dumps({"status": "BLOCKED", "error": "NOT_FOUND"}))
        length = int(self.headers.get("Content-Length") or "0")
        if length <= 0 or length > 8192:
            return self._send(400, json.dumps({"status": "BLOCKED", "error": "BAD_BODY"}))
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return self._send(400, json.dumps({"status": "BLOCKED", "error": "BAD_JSON"}))
        try:
            result = resolve_url(payload.get("url"),
                                 rehearse=bool(payload.get("rehearse", True)))
            return self._send(200, json.dumps(result))
        except (ValueError, OSError, TypeError, KeyError) as exc:
            return self._send(403, json.dumps({"status": "BLOCKED", "error": str(exc)}))


def serve(host="127.0.0.1", port=8787):
    if not (WEB_ROOT / "index.html").is_file():
        raise FileNotFoundError("WEB_INTAKE_MISSING")
    httpd = ThreadingHTTPServer((host, port), IntakeHandler)
    print(json.dumps({"status": "LISTENING", "url": f"http://{host}:{port}/",
                      "authority": "NONE"}))
    httpd.serve_forever()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("resolve")
    p.add_argument("--url", required=True)
    p.add_argument("--no-rehearse", action="store_true")
    p = sub.add_parser("serve")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8787)
    args = parser.parse_args()
    try:
        if args.command == "resolve":
            print(json.dumps(resolve_url(args.url, rehearse=not args.no_rehearse),
                             indent=2))
            return 0
        if args.command == "serve":
            serve(args.host, args.port)
            return 0
        raise ValueError("UNKNOWN_COMMAND")
    except (ValueError, OSError, TypeError, KeyError) as exc:
        print(json.dumps({"status": "BLOCKED", "error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
