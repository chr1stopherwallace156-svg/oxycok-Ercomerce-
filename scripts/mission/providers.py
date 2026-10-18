"""Bounded, read-only inspection providers. No target imports or shell commands."""
import ast
import hashlib
import json
import os
from pathlib import Path
import signal
import stat
import subprocess
import tempfile
import time

MAX_FILES = 512
MAX_BYTES = 4_000_000
REA_VERSION = "6.7.0"


class ProviderFailure(ValueError):
    def __init__(self, reason, evidence):
        super().__init__(reason)
        self.evidence = evidence



def sha(data):
    return hashlib.sha256(data).hexdigest()


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def inventory(target):
    root = Path(target).resolve(strict=True)
    if not root.is_dir():
        raise ValueError("TARGET_DIRECTORY_REQUIRED")
    records, total = [], 0
    for directory, dirs, files in os.walk(root, followlinks=False):
        dirs.sort()
        files.sort()
        if ".git" in dirs:
            dirs.remove(".git")
        for name in dirs + files:
            p = Path(directory) / name
            mode = p.lstat().st_mode
            if stat.S_ISLNK(mode) or not (stat.S_ISDIR(mode) or stat.S_ISREG(mode)):
                raise ValueError("UNSUPPORTED_TARGET_ENTRY")
        for name in files:
            path = Path(directory) / name
            with os.fdopen(os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
                                  | getattr(os, "O_NONBLOCK", 0)), "rb") as stream:
                if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
                    raise ValueError("UNSUPPORTED_TARGET_ENTRY")
                data = stream.read(MAX_BYTES + 1)
            total += len(data)
            if total > MAX_BYTES or len(records) >= MAX_FILES:
                raise ValueError("TARGET_BUDGET_EXCEEDED")
            records.append({"path": path.relative_to(root).as_posix(),
                            "sha256": sha(data), "bytes": len(data)})
    if not records:
        raise ValueError("EMPTY_TARGET")
    return {"scope": "REGULAR_WORKTREE_FILES_EXCLUDING_GIT", "files": records,
            "bytes": total, "sha256": sha(encode(records))}


def python_static(target):
    before = inventory(target)
    modules, edges = [], []
    for record in before["files"]:
        if not record["path"].endswith(".py"):
            continue
        path = Path(target) / record["path"]
        tree = ast.parse(path.read_bytes(), filename=record["path"])
        symbols = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                symbols.append({"name": node.name, "line": node.lineno})
            if isinstance(node, ast.Call):
                name = ast.unparse(node.func)
                edges.append({"source": record["path"] + ":" + str(node.lineno),
                              "relation": "SYNTAX_CALL_TARGET", "target": name})
        modules.append({"path": record["path"], "symbols": symbols})
    if not modules:
        raise ValueError("NO_PYTHON_MODULES")
    if inventory(target)["sha256"] != before["sha256"]:
        raise ValueError("TARGET_CHANGED_DURING_INSPECTION")
    return {"provider": "OXYCOK_PYTHON_AST_V1", "target_sha256": before["sha256"],
            "coverage_status": "BOUNDED_STATIC", "scope": before["scope"],
            "limitations": ["Syntax relationships do not prove runtime call resolution or behavior."],
            "metrology": {"files": len(before["files"]), "bytes": before["bytes"],
                          "modules": len(modules), "call_sites": len(edges)},
            "modules": modules, "edges": edges}


def bounded_process(command, timeout=60, max_bytes=2_000_000, cwd=None):
    # Files bound memory use; polling and group termination bound retained output
    # and elapsed time. This is process supervision, not a security sandbox.
    with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
        process = subprocess.Popen(command, cwd=cwd, stdout=out, stderr=err,
                                   stdin=subprocess.DEVNULL, start_new_session=True)
        deadline = time.monotonic() + timeout
        reason = None
        while process.poll() is None:
            if time.monotonic() >= deadline:
                reason = "PROVIDER_TIMEOUT"
                break
            if os.fstat(out.fileno()).st_size + os.fstat(err.fileno()).st_size > max_bytes:
                reason = "PROVIDER_OUTPUT_BUDGET"
                break
            time.sleep(0.02)
        # Kill remaining descendants in the owned group even if the leader exited.
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()
        size = os.fstat(out.fileno()).st_size + os.fstat(err.fileno()).st_size
        if reason or size > max_bytes:
            raise ValueError(reason or "PROVIDER_OUTPUT_BUDGET")
        out.seek(0)
        err.seek(0)
        stdout, stderr = out.read(max_bytes + 1), err.read(max_bytes + 1)
        if process.returncode:
            try:
                diagnostic = json.loads(stdout)
            except ValueError:
                diagnostic = {"stdout": stdout.decode(errors="replace")}
            raise ProviderFailure("PROVIDER_EXIT_" + str(process.returncode),
                                  {"diagnostic": diagnostic,
                                   "stderr": stderr.decode(errors="replace")})
        return stdout


def rea_static(target, executable):
    executable = Path(executable)
    if not executable.is_absolute() or not executable.is_file():
        raise ValueError("REA_EXECUTABLE_UNAVAILABLE")
    version = bounded_process([str(executable), "--version"], timeout=30).decode().strip()
    if version != REA_VERSION:
        raise ValueError("REA_VERSION_MISMATCH")
    before = inventory(target)
    raw = bounded_process([str(executable), "analyze-javascript-application",
                           str(Path(target).resolve()), "--json"], timeout=60, cwd="/tmp")
    result = json.loads(raw)
    if (not isinstance(result, dict) or "error" in result or result.get("isError") is True
            or result.get("ok") is False or not isinstance(result.get("evidence_id"), str)
            or not isinstance(result.get("normalized_result"), dict)):
        raise ValueError("REA_INVALID_OR_ERROR_ENVELOPE")
    if inventory(target)["sha256"] != before["sha256"]:
        raise ValueError("TARGET_CHANGED_DURING_INSPECTION")
    # Retain the complete provider JSON locally; it is untrusted data. The abstract
    # boundary consumes only identity, scope and explicit unknown coverage.
    return {"provider": "REA_CLI_" + version, "target_sha256": before["sha256"],
            "coverage_status": "UNKNOWN", "scope": before["scope"],
            "limitations": ["CLI evidence retained; semantic coverage is not yet normalized by this adapter.",
                            "No target behavior or reconstruction equivalence established."],
            "metrology": {"files": len(before["files"]), "bytes": before["bytes"],
                          "provider_reply_bytes": len(raw)},
            "modules": [], "edges": [], "provider_result": result}
