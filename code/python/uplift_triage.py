#!/usr/bin/env python3
"""uplift_triage.py — Maximum-nodes-per-effort triage for the AeroCement design day.
Reads baseline + uplifted records, scores each hour-node by:
  dead_mass  = joules of unrealized demand (zero-cooling/stirling hours)
  marginal_y = d(cooling_j + stirling_j) / d(factor) from last cycle
  eta_node   = reachable-joules / (1 + dead_hours)   <- highest yield, least effort
Exports uplift_priority.json and prints a ranked table. Stdlib only, idempotent."""

import json
import sys
from pathlib import Path

BASE_DIR = Path("/home/jesse/src/openroot-thesis/code/python")
BASELINE = BASE_DIR / "design_day_baseline.json"
UPLIFTED = BASE_DIR / "design_day_uplifted.json"
OUT = BASE_DIR / "uplift_priority.json"


def load(path: Path):
    if not path.is_file():
        sys.exit(f"ERROR: missing {path}")
    return json.loads(path.read_text())


def norm(records):
    """Accept either a bare list or {'records': [...]} wrapper; index by hour."""
    if isinstance(records, dict):
        records = records.get("records", [])
    return {int(r["hour"]): r for r in records}


def main():
    base = norm(load(BASELINE))
    up = norm(load(UPLIFTED))
    if not base or not up:
        sys.exit("ERROR: empty record set(s)")

    hours = sorted(set(base) & set(up))
    scored = []

    for h in hours:
        b, u = base[h], up[h]
        cw_b, cw_u = float(b.get("cool_w", 0)), float(u.get("cool_w", 0))
        sw_b, sw_u = float(b.get("stirl_w", 0)), float(u.get("stirl_u", u.get("stirl_w", 0)))
        ach_b, ach_u = float(b.get("ach", 0)), float(u.get("ach", 0))
        t_int = float(u.get("t_int", u.get("tint", 0)))

        delta_j = (cw_u - cw_b) + (sw_u - sw_b)          # delivered joule gain (W-hours)
        dead = 1.0 if (cw_b == 0 and sw_b == 0) else 0.0  # hour-node was dormant pre-cycle
        gain_per_factor = delta_per_pct = None
        if cw_u > cw_b:  # factor of last cycle reconstructed from cooling ratio
            factor = cw_u / cw_b
            gain_per_factor = delta_j / factor
        # yield ratio: joules actually reached / intervention weight (boosted hours cost more)
        weight = 1.0 + factor if cw_u > 0 else 0.5  # dormant targets are cheap to activate
        eta_node = (cw_u + sw_u) / weight
        t_ok = 1.0 if t_int <= 27.0 else max(0.0, (29.5 - t_int))  # comfort-band credit

        scored.append({
            "hour": h,
            "cool_w": cw_u,
            "ach": ach_u,
            "stirl_w": sw_u,
            "t_int": round(t_int, 2),
            "was_dormant": bool(sw_b == 0 and cw_b == 0),
            "delta_delivered_j": round(delta_j, 1),
            "gain_per_unit_effort": round(delta_j / weight, 1),
            "eta_node": round(eta_node, 1),
            "comfort_deficit": round(max(0.0, t_int - 27.0), 2),
            "reach_priority": round((delta_j / weight) + 40.0 * max(0.0, t_int - 27.0)
                                    + (250.0 if (cw_b == 0 and cw_u > 0) else 0.0), 1),
        })

    # Extra dormant bonus: a previously-zero node reaching nonzero = NEW node activated
    # (largest possible network gain per intervention) — already folded into reach_priority.

    scored.sort(key=lambda r: (-r["reach_priority"], r["hour"]))
    OUT.write_text(json.dumps(scored, indent=2))

    act = [r for r in scored if not r["was_doudmant"]] if False else [r for r in scored if not r["was_dormant"]]
    dor = [r for r in scored if r["was_dormant"]]

    print("AeroCement Node Triage — reach-ranked (highest node-yield first)")
    print("=" * 78)
    hdr = f"{'Hr':>3} {'Cool_W':>8} {'ACH':>6} {'Stirl_W':>8} {'T_int':>6}  {'yield/eff':>9}  flag"
    print(hdr)
    print("-" * 78)
    for r in scored:
        flag = "NEW-NODE" if (r["was_dormant"] and r["cool_w"] > 0) else ("dormant" if r["was_dormant"] else "active")
        print(f"{r['hour']:>3} {r['cool_w']:>8.1f} {r['ach']:>8.2f} {r['stirl_w']:>8.1f} "
              f"{r['t_int']:>6.2f}  {r['gain_per_unit_effort']:>9.1f}  {flag}")

    n_act, n_dor = len(act), len(dor)
    tot_new = sum(1 for r in scored if r["was_dormant"] and r["cool_w"] > 0)
    hot = [r["hour"] for r in scored if r["comfort_deficit"] > 0]
    print("-" * 78)
    print(f"Nodes network total   : {len(scored)}  (active {n_act}, dormant {n_dou})" if False else
          f"Nodes total: {len(scored)}  active {n_act}  dormant {n_dor}")
    print(f"Newly activated nodes : {tot_new}")
    print(f"Comfort-band violations (>27 C): {hot if hot else 'none'}")
    print(f"Top-3 next targets: {[r['hour'] for r in scored[:3]]}")
    print(f"Ranked export -> {OUT}  ({len(scored)} records)")


if __name__ == "__main__":
    main()
