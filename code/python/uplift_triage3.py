#!/usr/bin/env python3
"""uplift_triage3.py — Node triage pinned to the verified export schema.
Ranked by reach: max good / most nodes / least effort. Stdlib only, idempotent."""

import json
import sys
import re
from datetime import datetime
from pathlib import Path

BASE_DIR = Path("/home/jesse/src/openroot-thesis/code/python")
SCHEMA = {
    "cool_w":  "cooling_power_w",
    "ach":     "air_changes_per_hour",
    "stirl_w": "stirling_power_w",
    "t_int":   "interior_temp_estimate_c",
}

def load_records(path: Path):
    if not path.is_file():
        sys.exit(f"ERROR: missing {path}")
    data = json.loads(path.read_text())
    if isinstance(data, dict):
        for k in ("records", "hours", "data", "design_day", "rows"):
            if isinstance(data.get(k), list):
                return data[k]
        sys.exit(f"ERROR: unrecognized structure in {path}, keys: {list(data)[:12]}")
    if not isinstance(data, list) or not data:
        sys.exit(f"ERROR: empty record list in {path}")
    return data

def hour_of(rec, idx):
    ts = rec.get("timestamp")
    if isinstance(ts, (int, float)) and 0 <= ts < 86400:
        return int(ts) // 3600
    if isinstance(ts, str):
        m = re.match(r"(\d{1,2}):", ts.strip())
        if m:
            return int(m.group(1)) % 24
        try:
            return datetime.fromisoformat(ts.replace("Z", "")).hour
        except ValueError:
            pass
    return idx  # chronological-order fallback: row i == hour i

def val(rec, canon):
    v = rec.get(SCHEMA[canon], 0.0)
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0

def main():
    base = load_records(BASE_DIR / "design_day_baseline.json")
    up = load_records(BASE_DIR / "design_day_uplifted.json")
    if len(base) != len(up):
        sys.exit(f"ERROR: record count mismatch: baseline {len(base)} vs uplifted {len(up)}")

    bm = {hour_of(r, i): r for i, r in enumerate(base)}
    um = {hour_of(r, i): r for i, r in enumerate(up)}
    hours = sorted(set(bm) & set(um))

    scored = []
    for h in hours:
        b, u = bm[h], um[h]
        cw_b, cw_u = val(b, "cool_w"), val(u, "cool_w")
        sw_b, sw_u = val(b, "stirl_w"), val(u, "stirl_w")
        t_int = val(u, "t_int")
        delta_wh = (cw_u - cw_b) + (sw_u - sw_b)
        dormant = cw_b <= 0 and sw_b <= 0
        weight = 0.5 if dormant else (1.0 + (cw_u / cw_b if cw_b > 0 else 1.0))
        deficit = max(0.0, t_int - 27.0)
        scored.append({
            "hour": h,
            "cool_w": cw_u,
            "stirl_w": sw_u,
            "ach": val(u, "ach"),
            "t_int": round(t_int, 2),
            "was_dormant": dormant,
            "delta_delivered_wh": round(delta_wh, 1),
            "yield_per_effort": round(delta_wh / weight, 1),
            "comfort_deficit_c": round(deficit, 2),
            "reach_priority": round(delta_wh / weight + 40.0 * deficit
                                    + (250.0 if (dormant and cw_u > 0) else 0.0), 1),
        })
    scored.sort(key=lambda r: (-r["reach_priority"], r["hour"]))
    out = BASE_DIR / "uplift_priority.json"
    out.write_text(json.dumps(scored, indent=2))

    print("NODE TRIAGE — ranked by reach (max good / most nodes / least effort)")
    print("=" * 74)
    print(f"{'Hr':>3} {'Cool_W':>8} {'Stirl_W':>8} {'T_int':>6} {'yld/eff':>8}  flag")
    print("-" * 74)
    for r in scored:
        flag = "NEW-NODE" if (r["was_dormant"] and r["cool_w"] > 0) else (
               "dormant" if r["was_dormant"] else "active")
        print(f"{r['hour']:>3} {r['cool_w']:>8.1f} {r['stirl_w']:>8.1f} "
              f"{r['t_int']:>6.2f} {r['yield_per_effort']:>8.1f}  {flag}")
    print("-" * 74)
    dor = [r for r in scored if r["was_dormant"]]
    hot = [r["hour"] for r in scored if r["comfort_deficit_c"] > 0]
    print(f"Total {len(scored)} nodes: {len(scored)-len(dor)} active, {len(dor)} dormant")
    print(f"Comfort violations >27C: {hot if hot else 'none'}")
    print(f"Next weak-node set (top 6): {[r['hour'] for r in scored[:6]]}")
    print(f"Exported -> {out}")

if __name__ == "__main__":
    main()
