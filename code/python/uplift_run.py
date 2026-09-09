#!/usr/bin/env python3
"""uplift_run.py — CWD-immune launcher for uplift_weak_nodes.py.
Locates the newest copy of the script across all known node paths,
then execs it in-process. Idempotent, zero dependencies."""

import os
import sys
import runpy
from pathlib import Path

CANDIDATE_ROOTS = [
    "/home/jesse/src/openroot-thesis/code/python",
    "/home/jesse/github-mirror/openroot-thesis/code/python",
    "/home/jesse/repo_audit_workspace/openroot-thesis/code/python",
    "/data/archive/openroot-thesis/code/python",
]
TARGET = "uplift_weak_nodes.py"


def locate() -> Path:
    """Pick the most recently modified candidate; src clone wins ties by priority order."""
    hits = []
    for prio, root in enumerate(CANDIDATE_ROOTS):
        p = Path(root) / TARGET
        if p.is_file():
            hits.append((-p.stat().st_mtime, prio, p))
    if not hits:
        print("ERROR: uplift_weak_nodes.py not found in any known root:", file=sys.stderr)
        for r in CANDIDATE_ROOTS:
            print(f"  {r}", file=sys.stderr)
        sys.exit(1)
    hits.sort()
    return hits[0][2]


if __name__ == "__main__":
    script = locate()
    print(f"[uplift_run] executing {script} (mtime={script.stat().st_mtime})")
    os.chdir(script.parent)  # JSON exports land beside the script, deterministically
    sys.argv = [str(script)] + sys.argv[1:]
    runpy.run_path(str(script), run_name="__main__")
