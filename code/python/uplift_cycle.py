#!/usr/bin/env python3
"""uplift_cycle.py — Deficit-first uplift cycle.
Ranks nodes by REMAINING comfort deficit, not delivered yield.
Comfortable dormant hours are protected, not boosted. Patches the
weak-node selection in uplift_weak_nodes.py and re-runs it.
Stdlib only, idempotent, backs up before touching anything."""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path("/home/jesse/src/openroot-thesis/code/python")
UPLIFT_SCRIPT = BASE_DIR / "uplift_weak_nodes.py"
COMFORT_MAX_C = 27.0
N_TARGETS = 6

def load_records(path: Path):
    if not path.is_file():
        sys.exit(f"ERROR: missing {path}")
    data = json.loads(path.read_text())
    if isinstance(data, dict):
        for k in ("records", "hours", "data", "rows"):
            if isinstance(data.get(k), list):
                return data[k]
        sys.exit(f"ERROR: unrecognized structure in {path}: {list(data)}")
    return data

def main():
    base = load_records(BASE_DIR / "design_day_baseline.json")
    up = load_records(BASE_DIR / "design_day_uplifted.json")
    if len(base) != len(up):
        sys.exit("ERROR: baseline/uplifted record count mismatch")

    scored = []
    for i, (b, u) in enumerate(zip(base, up)):
        cw = float(u.get("cooling_power_w", 0))
        sw = float(u.get("stirling_power_w", 0))
        t = float(u.get("interior_temp_estimate_c", 0))
        deficit = max(0.0, t - COMFORT_MAX_C)
        dormant = cw <= 0 and sw <= 0
        # Deficit-first: idle-and-comfortable nodes cost 0 to skip,
        # active-but-hot nodes are the only ones worth intervention.
        priority = deficit + (0.25 * deficit if dormant and deficit > 0 else 0.0)
        scored.append({"hour": i, "t_int": t, "deficit_c": round(deficit, 2),
                       "dormant": dormant, "priority": round(priority, 3)})

    scored.sort(key=lambda r: (-r["priority"], r["hour"]))
    targets = sorted(r["hour"] for r in scored[:N_TARGETS] if r["priority"] > 0)

    print("DEFICIT-FIRST CYCLE PLAN")
    print("=" * 60)
    for r in scored[:N_TARGETS]:
        tag = "dormant-hot" if r["dormant"] else "active"
        print(f"  hr {r['hour']:>2}  T={r['t_int']:>5.2f}C  "
              f"deficit={r['deficit_c']:.2f}C  ({tag})")
    print(f"\nSelected targets: {targets}")

    out = BASE_DIR / "cycle_targets.json"
    out.write_text(json.dumps(scored, indent=2))
    print(f"Full ranking -> {out}")

    if not targets:
        print("All nodes within comfort band. Nothing to uplift. GREEN.")
        return

    # Patch the weak-node selection in uplift_weak_nodes.py
    src = UPLIFT_SCRIPT.read_text()
    patterns = [
        (r"weak_nodes\s*=\s*\[[^\]]*\]",
         "weak_nodes = " + json.dumps(targets)),
        (r"weak_nodes\s*=\s*list\(range\([^)]*\)\)",
         "weak_nodes = " + json.dumps(targets)),
    ]
    patched = src
    matched = False
    for pat, rep in patterns:
        new, n = re.subn(pat, rep, patched, count=1)
        if n:
            patched, matched = new, True
            break
    if not matched:
        sys.exit("ERROR: could not locate weak_nodes assignment in "
                 f"{UPLIFT_SCRIPT.name}. Open it and set "
                 f"weak_nodes = {targets} manually.")
    if patched != src:
        backup = UPLIFT_SCRIPT.with_suffix(".py.bak")
        shutil.copy2(UPLIFT_SCRIPT, backup)
        UPLIFT_SCRIPT.write_text(patched)
        print(f"Patched selection (backup -> {backup.name})")

    # Syntax gate, then run
    chk = subprocess.run([sys.executable, "-m", "py_compile", str(UPLIFT_SCRIPT)],
                         capture_output=True, text=True)
    if chk.returncode != 0:
        UPLIFT_SCRIPT.write_text(src)
        sys.exit(f"ERROR: syntax gate failed, reverted.\n{chk.stderr}")
    run = subprocess.run([sys.executable, str(UPLIFT_SCRIPT)])
    sys.exit(run.returncode)

if __name__ == "__main__":
    main()
