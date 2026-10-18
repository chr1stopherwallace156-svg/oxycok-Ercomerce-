#!/usr/bin/env python3
"""REA method application toward the Nord VPN domain with an ownership gate.

Starts from the pinned REA method/reference and admits only explicitly
authorized analysis targets. Proprietary NordVPN product binaries are blocked
until a separately recorded authorized pin exists.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/mission"))
sys.path.insert(0, str(ROOT / "scripts/reconstruction"))
import campaign as reconstruction_campaign
import providers
import runtime
from store import Store

SUBJECT_DIR = ROOT / "reconstruction" / "subjects" / "nordvpn"
RIGHTS_PATH = SUBJECT_DIR / "RIGHTS_V1.json"
OWNED_SURFACE = ROOT / "tests" / "mission" / "fixtures" / "owned_nordvpn_surface"
PROPRIETARY_NAME_MARKERS = (
    "nordvpn",
    "nord_vpn",
    "nord-vpn",
    "nordsecurity",
    "nord_security",
)


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def read_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, "DUPLICATE_JSON_KEY")
            result[key] = value
        return result

    return json.loads(Path(path).read_text(), object_pairs_hook=unique)


def load_rights(path=RIGHTS_PATH):
    rights = read_json(path)
    require(rights.get("version") == 1, "INVALID_RIGHTS_VERSION")
    require(rights.get("kind") == "NORDVPN_APPLICATION_RIGHTS", "INVALID_RIGHTS_KIND")
    require(rights.get("authority") == "NONE", "AUTHORITY_ESCALATION")
    require(rights.get("method_reference", {}).get("repository") == "morluto/rea",
            "REA_METHOD_REFERENCE_REQUIRED")
    require(isinstance(rights.get("authorized_targets"), list)
            and rights["authorized_targets"], "AUTHORIZED_TARGETS_REQUIRED")
    require(isinstance(rights.get("forbidden"), list) and rights["forbidden"],
            "FORBIDDEN_SURFACE_REQUIRED")
    return rights


def git_blob_sha(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def build_owned_census(surface=OWNED_SURFACE):
    root = Path(surface).resolve(strict=True)
    entries = [{"path": ".", "type": "tree", "sha": "0" * 40, "mode": "040000"}]
    files = sorted(p for p in root.rglob("*") if p.is_file() and ".git" not in p.parts)
    require(files, "EMPTY_OWNED_SURFACE")
    for path in files:
        rel = path.relative_to(root).as_posix()
        mode = "100755" if path.stat().st_mode & 0o111 else "100644"
        entries.append({
            "path": rel,
            "type": "blob",
            "sha": git_blob_sha(path),
            "mode": mode,
        })
    # Deterministic synthetic tree/commit pins for the owned fixture census.
    body = json.dumps(
        [{"path": e["path"], "sha": e["sha"], "mode": e["mode"]} for e in entries
         if e["type"] == "blob"],
        sort_keys=True, separators=(",", ":"),
    ).encode()
    commit = hashlib.sha1(b"oxycok-owned-nordvpn-surface\0" + body).hexdigest()
    tree = hashlib.sha1(b"tree\0" + body).hexdigest()
    entries[0]["sha"] = tree
    return {
        "version": 1,
        "kind": "PINNED_REPOSITORY_CENSUS",
        "repository": "oxycok/owned-nordvpn-surface",
        "commit": commit,
        "tree_sha": tree,
        "upstream_truncated": False,
        "entries": entries,
        "note": "Owned OXYCOK fixture census. Not NordVPN product source.",
    }


def target_matches_authorized(target, rights):
    root = Path(target).resolve(strict=True)
    inventory = providers.inventory(root)
    for row in rights["authorized_targets"]:
        require(isinstance(row, dict), "INVALID_AUTHORIZED_TARGET")
        if row.get("kind") == "OWNED_FIXTURE_PATH":
            expected = (ROOT / row["relative_path"]).resolve()
            if root == expected:
                pinned = row.get("subject_sha256")
                if pinned and pinned != inventory["sha256"]:
                    raise ValueError("AUTHORIZED_TARGET_SUBJECT_DRIFT")
                return {
                    "disposition": "AUTHORIZED",
                    "basis": row.get("basis", "owned fixture path"),
                    "target": str(root),
                    "subject_sha256": inventory["sha256"],
                    "authorization_id": row["id"],
                }
        if row.get("kind") == "OWNED_FIXTURE_HASH":
            if inventory["sha256"] == row.get("subject_sha256"):
                return {
                    "disposition": "AUTHORIZED",
                    "basis": row.get("basis", "owned fixture hash"),
                    "target": str(root),
                    "subject_sha256": inventory["sha256"],
                    "authorization_id": row["id"],
                }
    return None


def looks_proprietary_nordvpn(target):
    text = str(Path(target).resolve()).lower()
    return any(marker in text for marker in PROPRIETARY_NAME_MARKERS)


def admit_target(target, rights=None):
    rights = rights or load_rights()
    root = Path(target).resolve(strict=True)
    matched = target_matches_authorized(root, rights)
    if matched:
        return matched
    if looks_proprietary_nordvpn(root):
        raise ValueError("PROPRIETARY_NORDVPN_TARGET_NOT_AUTHORIZED")
    raise ValueError("ANALYSIS_TARGET_NOT_AUTHORIZED")


def create_application_campaign(census, capabilities):
    return reconstruction_campaign.create(census, "nordvpn", capabilities)


def rehearse(state_root, target, rights=None, max_steps=6):
    rights = rights or load_rights()
    admission = admit_target(target, rights)
    store = Store(Path(state_root).resolve())
    try:
        started = runtime.start(
            store,
            target=Path(target).resolve(),
            provider="python",
            domain="nordvpn",
            mechanisms=["evidence-consumption", "failure-learning-dual-closure"],
            facts=["artifact-produced", "downstream-consumer", "owned-fixture-rehearsal"],
        )
        finished = runtime.run(store, started["mission_id"], max_steps)
        return {
            "authority": "NONE",
            "admission": admission,
            "mission": finished,
            "claims": {
                "nordvpn_product_reverse_engineering": "NOT_PERFORMED",
                "rea_method_reference": rights["method_reference"],
                "legal_clearance": "NOT_ESTABLISHED",
                "independent_qualification": "NOT_GRANTED",
            },
        }
    finally:
        store.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("admit")
    p.add_argument("--target", required=True)

    p = sub.add_parser("census")
    p.add_argument("--surface", default=str(OWNED_SURFACE))
    p.add_argument("--output", required=True)

    p = sub.add_parser("campaign-new")
    p.add_argument("--census", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--capability", action="append", required=True)

    p = sub.add_parser("rehearse")
    p.add_argument("--target", required=True)
    p.add_argument("--state-root", required=True)
    p.add_argument("--max-steps", type=int, default=6)

    p = sub.add_parser("validate-rights")
    p.add_argument("--rights", default=str(RIGHTS_PATH))

    args = parser.parse_args()
    try:
        if args.command == "validate-rights":
            rights = load_rights(Path(args.rights))
            print(json.dumps({
                "status": "VALID",
                "authority": rights["authority"],
                "authorized_target_count": len(rights["authorized_targets"]),
                "forbidden_count": len(rights["forbidden"]),
            }))
            return 0
        if args.command == "admit":
            print(json.dumps(admit_target(args.target), indent=2))
            return 0
        if args.command == "census":
            census = build_owned_census(args.surface)
            reconstruction_campaign.validate_census(census)
            out = Path(args.output)
            with out.open("x") as file:
                file.write(json.dumps(census, indent=2) + "\n")
            print(json.dumps({
                "status": "CREATED",
                "repository": census["repository"],
                "commit": census["commit"],
                "entries": len(census["entries"]),
            }))
            return 0
        if args.command == "campaign-new":
            plan = create_application_campaign(
                reconstruction_campaign.read(args.census), args.capability)
            with Path(args.output).open("x") as file:
                file.write(json.dumps(plan, indent=2) + "\n")
            print(json.dumps({"status": "CREATED", "domain": plan["domain"],
                              "authority": plan["authority"]}))
            return 0
        if args.command == "rehearse":
            print(json.dumps(rehearse(args.state_root, args.target,
                                      max_steps=args.max_steps), indent=2))
            return 0
        raise ValueError("UNKNOWN_COMMAND")
    except (ValueError, OSError, TypeError, KeyError) as exc:
        print(json.dumps({"status": "BLOCKED", "error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
