#!/usr/bin/env python3
"""uplift_triage2.py — Schema-adaptive node triage. Discovers the actual
field names in design_day_baseline.json / design_day_uplifted.json at
runtime (alias tables + signature-value fingerprinting from known
console output), then ranks every hour-node by yield-per-effort.
Stdlib only. Idempotent. Fails LOUDLY, never silently."""

import json
import sys
from pathlib import Path

BASE_DIR = Path("/home/jesse/src/openroot-thesis/code/python")

# Known fingerprints from validated console output: hour 7 baseline.
SIGNATURES = {"cool_w": 2439.8, "ach": 14.61, "stirl_w": 80.3, "t_int": 26.81}
ALIASES = {
    "hour":     ["hour", "hr", "h", "t", "time", "local_hour"],
    "cool_w":   ["cool_w", "cooling_w", "q_cool", "cool", "cooling", "clg_w", "evap_w"],
    "ach":      ["ach", "air_changes", "air_changes_per_hour", "vent"],
    "stirl_w":  ["stirl_w", "stirling_w", "stir_w", "stirl", "stirling", "power_w", "elec_w"],
    "t_int":    ["t_int", "tint", "t_internal", "t_in", "interior_t", "temp_int"],
}

def load(path: Path):
    if not path.is_file():
        sys.exit(f"ERROR: missing {path}")
    data = json.loads(path.read_text())
    if isinstance(data, dict):
        for k in ("records", "hours", "data", "design_day", "rows"):
            if isinstance(data.get(k), list):
                data = data[k]
                break
        else:
            if all(isinstance(v, dict) for v in data.values()) and data:
                data = [dict(v, _k=k) if "hour" not in v else v
                        for k, v in sorted(data.items(), key=lambda kv: str(kv[0]))]
    if not isinstance(data, list) or not data:
        sys.exit(f"ERROR: unrecognized structure in {path}.\n"
                 f"Top-level type: {type(data).__name__}.\n"
                 f"If dict, keys: {list(data)[:12]}")
    return data

def discover_schema(records):
    """Map canonical field -> actual key. Alias match first, signature fallback."""
    keys = set(records[0].keys())
    schema, missing = {}, []
    for canon, cands in ALIASES.items():
        for c in cands:
            if c in keys:
                schema[canon] = c
                break
        else:
            schema[canon] = None
            missing.append(canon)
    if schema["hour"] is None:
        # hour is mandatory: fall back to any int-valued 0-23 field, else row index
        for k in keys:
            vals = [r.get(k) for r in records[:5]]
            if all(isinstance(v, int) and 0 <= v <= 23 for v in vals if v is not None):
                schema["hour"] = k
                missing.remove("hour")
                break
        else:
            schema["hour"] = "_row"
            missing.remove("hour")
    # signature fingerprinting for anything still unmatched
    if missing:
        for rec in records:
            if schema["hour"] == "_row":
                continue
            try:
                if int(rec[schema["hour"]]) != 7:
                    continue
            except (TypeError, ValueError):
                continue
            for canon in list(missing):
                target = SIGNATURES[canon]
                for k, v in rec.items():
                    if isinstance(v, (int, float)):
                        try:
                            if abs(float(v) - target) < 0.05:
                                schema[canon] = k
                                missing.remove(canon)
                                break
                        except (TypeError, ValueError):
                            pass
    return schema, missing, keys

def g(rec, schema, canon, default=0.0):
    key = schema[canon]
    if key is None or key == "_row":
        return default
    v = rec.get(key, default)
    try:
        return float(v)
    except (TypeError, ValueError):
        return default

def hour_of(rec, schema, idx):
    if schema["hour"] == "_row":
        return idx
    try:
        return int(rec[schema["hour"]])
    except (KeyError, TypeError, ValueError):
        return idx

def main():
    base_raw = load(BASE_DIR / "design_day_baseline.json")
    up_raw = load(BASE_DIR / "design_day_uplifted.json")

    schema, missing, keys = discover_schema(base_raw)
    print("SCHEMA DISCOVERY")
    print("=" * 60)
    for canon, key in schema.items():
        print(f"  {canon:<8} <- {key if key else '(UNRESOLVED)'}")
    if missing:
        print(f"\nCould not resolve: {missing}")
        print(f"All keys present in records: {sorted(keys)}")
        print("Add the actual key name(s) to ALIASES and re-run.")
        sys.exit(2)

    def to_map(records):
        return {hour_of(r, schema, i): r for i, r in enumerate(records)}

    base, up = to_map(base_raw), to_map(up_raw)
    hours = sorted(set(base) & set(up))

    scored = []
    for h in hours:
        b, u = base[h], up[h]
        cw_b, cw_u = g(b, schema, "cool_w"), g(u, schema, "cool_w")
        sw_b, sw_u = g(b, schema, "stirl_w"), g(u, schema, "stirl_w")
        ach_u, t_int = g(u, schema, "ach"), g(u, schema, "t_int")
        delta_j = (cw_u - cw_b) + (sw_u - sw_b)
        dormant = cw_b <= 0 and sw_b <= 0
        weight = 0.5 if dormant else (1.0 + (cw_u / cw_b if cw_b > 0 else 1.0))
        deficit = max(0.0, t_int - 27.0)
        scored.append({
            "hour": h, "cool_w": cw_u, "ach": ach_u, "stirl_w": sw_u,
            "t_int": round(t_int, 2), "was_dormant": dormant,
            "delta_delivered_wh": round(delta_j, 1),
            "yield_per_effort": round(delta_j / weight, 1),
            "comfort_deficit_c": round(deficit, 2),
            "reach_priority": round(
                delta_j / weight + 40.0 * deficit
                + (250.0 if (dormant and cw_u > 0) else 0.0), 1),
        })
    scored.sort(key=lambda r: (-r["reach_priority"], r["hour"]))
    out = BASE_DIR / "uplift_priority.json"
    out.write_text(json.dumps(scored, indent=2))

    print("\nNODE TRIAGE — ranked by reach (max good / max nodes / least effort)")
    print("=" * 60)
    print(f"{'Hr':>3} {'Cool_W':>8} {'Stirl_W':>8} {'T_int':>6} {'yld/eff':>8}  flag")
    for r in scored:
        flag = "NEW-NODE" if (r["was_dormant"] and r["cool_w"] > 0) else \
               ("dormant" if r["was_dormant"] else "active")
        print(f"{r['hour']:>3} {r['cool_w']:>8.1f} {r['stirl_w']:>8.1f} "
              f"{r['t_int']:>6.2f} {r['yield_per_effort']:>8.1f}  {flag}")
    print("-" * 60)
    dor = [r for r in scored if r["was_dormant"]]
    hot = [r["hour"] for r in scored if r["comfort_deficit_c"] > 0]
    print(f"Total {len(scored)}: {len(scored)-len(dor)} active, {len(dor)} dormant")
    print(f"Comfort violations >27C: {hot if hot else 'none'}")
    print(f"Next weak-node set (top 6): {[r['hour'] for r in scored[:6]]}")
    print(f"Exported -> {out}")

if __name__ == "__main__":
    main()
