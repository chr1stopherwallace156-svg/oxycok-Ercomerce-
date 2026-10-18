#!/usr/bin/env python3
"""OXYCOK entrypoint: configured Elektron core inheritance for every mission."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts/elektron_bridge"))
from snapshot import verify, outside
from run_owner import SOURCE_COMMIT, SOURCE_REPOSITORY, SOURCE_TREE


def configure(path, snapshot, state_root, allow_bounded=False):
    path = Path(path).absolute()
    snapshot = Path(snapshot).resolve(strict=True)
    state = Path(state_root).resolve()
    if not outside(path.resolve(), ROOT) or not outside(path.resolve(), snapshot):
        raise ValueError("CONFIG_MUST_STAY_OUTSIDE_PUBLIC_PROJECT_AND_SNAPSHOT")
    if not outside(state, ROOT) or not outside(state, snapshot):
        raise ValueError("STATE_MUST_BE_SEPARATE_PRIVATE_ROOT")
    manifest = verify(snapshot, allow_bounded)
    if (manifest.get("repository"), manifest.get("commit"), manifest.get("source_tree")) != (
            SOURCE_REPOSITORY, SOURCE_COMMIT, SOURCE_TREE):
        raise ValueError("UNREVIEWED_SOURCE_PROFILE")
    config = {"version":1, "snapshot":str(snapshot), "state_root":str(state),
              "allow_bounded_analysis":bool(allow_bounded), "source_commit":SOURCE_COMMIT}
    with path.open("x") as output:
        json.dump(config, output, indent=2)
        output.write("\n")
    return config


def load_config(path):
    config = json.loads(Path(path).read_text())
    if config.get("version") != 1 or config.get("source_commit") != SOURCE_COMMIT:
        raise ValueError("CONFIG_PROFILE_INVALID")
    if not config.get("snapshot") or not config.get("state_root"):
        raise ValueError("CORE_AND_STATE_REQUIRED")
    return config


def command(config, action, extra):
    if action not in {"start","step","run","status","events","graph"}:
        raise ValueError("UNKNOWN_MISSION_ACTION")
    reserved = {"--state-root","--elektron-snapshot","--elektron-allow-bounded-analysis"}
    if any(arg.split("=",1)[0] in reserved for arg in extra):
        raise ValueError("CONFIGURED_CORE_CANNOT_BE_SILENTLY_OVERRIDDEN")
    cmd = [sys.executable,"-B",str(ROOT/"scripts/mission/runtime.py"),
           "--state-root",config["state_root"],action] + list(extra)
    if action == "start":
        cmd += ["--elektron-snapshot",config["snapshot"]]
        if config["allow_bounded_analysis"]:
            cmd.append("--elektron-allow-bounded-analysis")
    return cmd


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config",required=True)
    parser.add_argument("action",choices=["configure","start","step","run","status","events","graph"])
    args, extra = parser.parse_known_args()
    try:
        if args.action == "configure":
            p = argparse.ArgumentParser()
            p.add_argument("--snapshot",required=True)
            p.add_argument("--state-root",required=True)
            p.add_argument("--allow-bounded-analysis",action="store_true")
            options = p.parse_args(extra)
            config = configure(args.config,options.snapshot,options.state_root,options.allow_bounded_analysis)
            print(json.dumps({"status":"CONFIGURED","source_commit":config["source_commit"],
                              "qualification":"NOT_ESTABLISHED"}))
            return 0
        return subprocess.run(command(load_config(args.config),args.action,extra)).returncode
    except (ValueError,OSError,KeyError) as exc:
        print(json.dumps({"status":"BLOCKED","authority":"NONE","error":str(exc)}),file=sys.stderr)
        return 2


if __name__=="__main__":
    sys.exit(main())
