#!/usr/bin/env python3
"""Read immutable Git blobs into a separate private snapshot; never mutate source."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

PUBLIC_ROOT = Path(__file__).resolve().parents[2]
MANIFEST = "OXYCOK_SNAPSHOT_MANIFEST.json"


def git(source, *args):
    return subprocess.check_output(["git", "-C", str(source), *args])


def blob_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def safe_relative(value):
    p = PurePosixPath(value)
    if p.is_absolute() or ".." in p.parts or not p.parts or "\\" in value:
        raise ValueError("UNSAFE_SNAPSHOT_PATH")
    return p


def outside(path, other):
    return path != other and not path.is_relative_to(other) and not other.is_relative_to(path)


def tree_sha(entries):
    root = {}
    for path, entry in entries.items():
        parts = safe_relative(path).parts
        node = root
        for part in parts[:-1]:
            node = node.setdefault(part, {})
            if not isinstance(node, dict) or "git_blob_sha" in node:
                raise ValueError("TREE_PATH_COLLISION")
        if parts[-1] in node:
            raise ValueError("TREE_PATH_COLLISION")
        node[parts[-1]] = entry
    def encode_tree(node):
        rows = []
        for name, value in node.items():
            directory = "git_blob_sha" not in value
            mode = "40000" if directory else value["mode"]
            identity = encode_tree(value) if directory else value["git_blob_sha"]
            rows.append((name.encode() + (b"/" if directory else b""),
                         mode.encode() + b" " + name.encode() + b"\0" + bytes.fromhex(identity)))
        body = b"".join(row[1] for row in sorted(rows))
        return hashlib.sha1(b"tree " + str(len(body)).encode() + b"\0" + body).hexdigest()
    return encode_tree(root)


def stage(source, commit, destination, repository, max_bytes=1_000_000_000):
    source = Path(source).resolve(strict=True)
    destination = Path(destination).absolute()
    resolved = destination.resolve()
    if not re.fullmatch("[0-9a-f]{40}", commit):
        raise ValueError("EXACT_COMMIT_REQUIRED")
    if not outside(resolved, source):
        raise ValueError("SOURCE_DESTINATION_OVERLAP")
    if not outside(resolved, PUBLIC_ROOT):
        raise ValueError("PRIVATE_SOURCE_MUST_STAY_OUTSIDE_PUBLIC_PROJECT")
    if destination.exists() or destination.is_symlink():
        raise ValueError("DESTINATION_MUST_BE_NEW")
    if not destination.parent.is_dir():
        raise ValueError("DESTINATION_PARENT_REQUIRED")
    # Git tree/blob reads, not checkout/reset/clean/fetch or an index update.
    actual = git(source, "rev-parse", commit + "^{commit}").decode().strip()
    if actual != commit:
        raise ValueError("COMMIT_IDENTITY_MISMATCH")
    tree = git(source, "ls-tree", "-r", "-z", "-l", commit)
    entries = {}
    total = 0
    for row in tree.split(b"\0"):
        if not row:
            continue
        header, rawpath = row.split(b"\t", 1)
        mode, kind, sha, size = header.decode().split()
        path = rawpath.decode("utf-8")
        safe_relative(path)
        if kind != "blob" or mode not in ("100644", "100755"):
            raise ValueError("UNSUPPORTED_SOURCE_ENTRY_REQUIRES_EXPLICIT_CLOSURE")
        if path == MANIFEST or path in entries:
            raise ValueError("SNAPSHOT_PATH_COLLISION")
        count = int(size)
        total += count
        entries[path] = {"git_blob_sha": sha, "bytes": count, "mode": mode}
    if not entries or total > max_bytes:
        raise ValueError("EMPTY_OR_OVER_BUDGET_SNAPSHOT")
    destination.mkdir(mode=0o700)
    process = subprocess.Popen(["git", "-C", str(source), "cat-file", "--batch"],
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    seen = set()
    try:
        for path, expected in entries.items():
            process.stdin.write((expected["git_blob_sha"] + "\n").encode())
            process.stdin.flush()
            header = process.stdout.readline().decode().strip().split()
            if header != [expected["git_blob_sha"], "blob", str(expected["bytes"])]:
                raise ValueError("BATCH_BLOB_HEADER_MISMATCH")
            target = destination / path
            target.parent.mkdir(parents=True, exist_ok=True)
            remaining = expected["bytes"]
            identity = hashlib.sha1(b"blob " + str(remaining).encode() + b"\0")
            content_hash = hashlib.sha256()
            with target.open("xb") as output:
                while remaining:
                    chunk = process.stdout.read(min(remaining, 1_000_000))
                    if not chunk:
                        raise ValueError("INCOMPLETE_BLOB_READ")
                    output.write(chunk)
                    identity.update(chunk)
                    content_hash.update(chunk)
                    remaining -= len(chunk)
            if process.stdout.read(1) != b"\n" or identity.hexdigest() != expected["git_blob_sha"]:
                raise ValueError("BATCH_BLOB_IDENTITY_MISMATCH")
            target.chmod(0o755 if expected["mode"] == "100755" else 0o644)
            expected["sha256"] = content_hash.hexdigest()
            seen.add(path)
        process.stdin.close()
        if process.wait(timeout=30) != 0 or seen != set(entries):
            raise ValueError("INCOMPLETE_SOURCE_SNAPSHOT")
        source_tree = git(source, "rev-parse", commit + "^{tree}").decode().strip()
        if tree_sha(entries) != source_tree:
            raise ValueError("FULL_SOURCE_TREE_MISMATCH")
        manifest = {"version": 1, "kind": "PRIVATE_ELEKTRON_SNAPSHOT",
                    "scope": "FULL_TRACKED_GIT_SNAPSHOT", "repository": repository,
                    "commit": commit, "source_tree": source_tree, "files": entries, "bytes": total,
                    "source_mutation": "NONE", "destination_qualification": "NOT_ESTABLISHED"}
        with (destination / MANIFEST).open("x") as output:
            json.dump(manifest, output, indent=2)
            output.write("\n")
        return manifest
    finally:
        if process.poll() is None:
            process.kill()
            process.wait()
        if process.stdin and not process.stdin.closed:
            process.stdin.close()
        if process.stdout:
            process.stdout.close()
        if process.stderr:
            process.stderr.close()
        # Preserve partial snapshots on failure for inspection; never silently delete.


def verify(root, allow_bounded=False):
    root = Path(root).resolve(strict=True)
    manifest = json.loads((root / MANIFEST).read_text())
    if manifest.get("kind") != "PRIVATE_ELEKTRON_SNAPSHOT" or manifest.get("version") != 1:
        raise ValueError("INVALID_SNAPSHOT_MANIFEST")
    if manifest.get("scope") != "FULL_TRACKED_GIT_SNAPSHOT" and not (
            allow_bounded and manifest.get("scope") == "BOUNDED_ANALYSIS_CLOSURE"):
        raise ValueError("FULL_TRANSFER_NOT_ESTABLISHED")
    if not re.fullmatch("[0-9a-f]{40}", manifest.get("commit", "")):
        raise ValueError("UNPINNED_SNAPSHOT")
    entries = manifest.get("files")
    if not isinstance(entries, dict) or not entries:
        raise ValueError("EMPTY_SNAPSHOT")
    for name, expected in entries.items():
        safe_relative(name)
        path = root / name
        if path.is_symlink() or not path.resolve().is_relative_to(root) or not path.is_file():
            raise ValueError("INVALID_SNAPSHOT_ENTRY")
        if (path.stat().st_mode & 0o777) != (0o755 if expected["mode"] == "100755" else 0o644):
            raise ValueError("SNAPSHOT_MODE_DRIFT:" + name)
        data = path.read_bytes()
        if (len(data) != expected["bytes"] or blob_sha(data) != expected["git_blob_sha"]
                or hashlib.sha256(data).hexdigest() != expected["sha256"]):
            raise ValueError("SNAPSHOT_CONTENT_DRIFT:" + name)
    if manifest["scope"] == "FULL_TRACKED_GIT_SNAPSHOT" and tree_sha(entries) != manifest.get("source_tree"):
        raise ValueError("SNAPSHOT_TREE_IDENTITY_MISMATCH")
    actual = set()
    for path in root.rglob("*"):
        if path.is_symlink():
            raise ValueError("SNAPSHOT_SYMLINK")
        if path.is_file():
            actual.add(path.relative_to(root).as_posix())
    if actual != set(entries) | {MANIFEST}:
        raise ValueError("UNDECLARED_SNAPSHOT_FILE")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    p = sub.add_parser("stage")
    p.add_argument("--source-checkout", required=True)
    p.add_argument("--commit", required=True)
    p.add_argument("--repository", required=True)
    p.add_argument("--destination", required=True)
    p.add_argument("--max-bytes", type=int, default=1_000_000_000)
    p = sub.add_parser("verify")
    p.add_argument("--snapshot", required=True)
    p.add_argument("--allow-bounded-analysis", action="store_true")
    args = parser.parse_args()
    try:
        if args.action == "stage":
            result = stage(args.source_checkout, args.commit, args.destination,
                           args.repository, args.max_bytes)
        else:
            result = verify(args.snapshot, args.allow_bounded_analysis)
        print(json.dumps({"scope": result["scope"], "commit": result["commit"],
                          "files": len(result["files"]),
                          "destination_qualification": "NOT_ESTABLISHED"}))
        return 0
    except (ValueError, OSError, KeyError, subprocess.SubprocessError) as exc:
        print(json.dumps({"status": "BLOCKED", "error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
