#!/usr/bin/env python3
"""
Weak-node uplift workflow for AeroCement design-day simulation.

Identifies the weakest hourly nodes in the baseline simulation and applies
targeted passive-system uplift factors to raise minimum performance.
"""

from dataclasses import dataclass, replace

from thermodynamic_ledger import (
    DEFAULT_DOME,
    DomeGeometry,
    ThermalState,
    calculate_thermal_state,
    export_json,
    generate_design_day_conditions,
    run_design_day,
)


@dataclass
class UpliftPolicy:
    """Parameters controlling weak-node identification and uplift strength."""
    weak_fraction: float = 0.25
    chimney_absorptance_boost: float = 0.06
    stirling_fraction_boost: float = 0.08
    evap_eff_boost: float = 0.08
    chimney_height_boost: float = 0.10
    chimney_area_boost: float = 0.12


def _score_state(state: ThermalState, baselines: dict) -> float:
    cool = state.cooling_power_w / baselines["max_cooling_power_w"]
    ach = state.air_changes_per_hour / baselines["max_air_changes_per_hour"]
    stirl = state.stirling_power_w / baselines["max_stirling_power_w"]
    temp = (baselines["max_interior_temp_c"] - state.interior_temp_estimate_c) / baselines["temp_span_c"]
    return (cool + ach + stirl + temp) / 4.0


def _baseline_metrics(states: list[ThermalState]) -> dict:
    max_cooling = max(max(s.cooling_power_w for s in states), 1e-6)
    max_ach = max(max(s.air_changes_per_hour for s in states), 1e-6)
    max_stirling = max(max(s.stirling_power_w for s in states), 1e-6)
    max_interior = max(s.interior_temp_estimate_c for s in states)
    min_interior = min(s.interior_temp_estimate_c for s in states)
    return {
        "max_cooling_power_w": max_cooling,
        "max_air_changes_per_hour": max_ach,
        "max_stirling_power_w": max_stirling,
        "max_interior_temp_c": max_interior,
        "temp_span_c": max(max_interior - min_interior, 1e-6),
    }


def identify_weak_nodes(states: list[ThermalState], policy: UpliftPolicy) -> list[int]:
    metrics = _baseline_metrics(states)
    active_states = [
        (idx, state)
        for idx, state in enumerate(states)
        if state.cooling_power_w > 0.0 or state.stirling_power_w > 0.0 or state.air_changes_per_hour > 0.0
    ]
    candidates = active_states if active_states else list(enumerate(states))
    scored = [(idx, _score_state(state, metrics)) for idx, state in candidates]
    scored.sort(key=lambda x: x[1])  # lower score = weaker node
    weak_count = max(1, int(round(len(states) * policy.weak_fraction)))
    weak_count = min(weak_count, len(scored))
    return sorted(idx for idx, _ in scored[:weak_count])


def _boosted_dome(dome: DomeGeometry, policy: UpliftPolicy) -> DomeGeometry:
    return replace(
        dome,
        evap_saturation_eff=min(0.98, dome.evap_saturation_eff + policy.evap_eff_boost),
        chimney_height_m=dome.chimney_height_m * (1.0 + policy.chimney_height_boost),
        chimney_area_m2=dome.chimney_area_m2 * (1.0 + policy.chimney_area_boost),
    )


def uplift_weak_nodes(
    dome: DomeGeometry = DEFAULT_DOME,
    policy: UpliftPolicy = UpliftPolicy(),
    peak_temp_c: float = 40.0,
    peak_rh: float = 0.20,
    peak_irradiance_wm2: float = 900.0,
    hours: int = 24,
) -> tuple[list[ThermalState], list[ThermalState], list[int]]:
    baseline_states = run_design_day(
        dome=dome,
        peak_temp_c=peak_temp_c,
        peak_rh=peak_rh,
        peak_irradiance_wm2=peak_irradiance_wm2,
        hours=hours,
    )
    weak_indices = identify_weak_nodes(baseline_states, policy)
    weak_set = set(weak_indices)

    uplifted_states: list[ThermalState] = []
    boosted_dome = _boosted_dome(dome, policy)
    boosted_absorptance = min(0.98, 0.90 + policy.chimney_absorptance_boost)
    boosted_stirling_fraction = min(0.85, 0.50 + policy.stirling_fraction_boost)

    for idx, site in enumerate(
        generate_design_day_conditions(
            peak_temp_c=peak_temp_c,
            peak_rh=peak_rh,
            peak_irradiance_wm2=peak_irradiance_wm2,
            hours=hours,
        )
    ):
        if idx in weak_set:
            uplifted_states.append(
                calculate_thermal_state(
                    site,
                    boosted_dome,
                    chimney_solar_absorptance=boosted_absorptance,
                    stirling_fraction_of_carnot=boosted_stirling_fraction,
                )
            )
        else:
            uplifted_states.append(baseline_states[idx])

    return baseline_states, uplifted_states, weak_indices


def _print_floor_comparison(before: list[ThermalState], after: list[ThermalState]) -> None:
    print("\nBottom-floor metrics (higher is better except interior temp):")
    print(f"  Min cooling power (W):      {min(s.cooling_power_w for s in before):7.1f} -> {min(s.cooling_power_w for s in after):7.1f}")
    print(f"  Min ACH:                    {min(s.air_changes_per_hour for s in before):7.2f} -> {min(s.air_changes_per_hour for s in after):7.2f}")
    print(f"  Min Stirling power (W):     {min(s.stirling_power_w for s in before):7.1f} -> {min(s.stirling_power_w for s in after):7.1f}")
    print(f"  Max interior temp (°C):     {max(s.interior_temp_estimate_c for s in before):7.2f} -> {max(s.interior_temp_estimate_c for s in after):7.2f}")
    active_before = [s for s in before if s.cooling_power_w > 0.0 or s.stirling_power_w > 0.0 or s.air_changes_per_hour > 0.0]
    active_after = [s for s in after if s.cooling_power_w > 0.0 or s.stirling_power_w > 0.0 or s.air_changes_per_hour > 0.0]
    if active_before and active_after:
        print("\nActive-node floor metrics:")
        print(f"  Min cooling power (W):      {min(s.cooling_power_w for s in active_before):7.1f} -> {min(s.cooling_power_w for s in active_after):7.1f}")
        print(f"  Min ACH:                    {min(s.air_changes_per_hour for s in active_before):7.2f} -> {min(s.air_changes_per_hour for s in active_after):7.2f}")
        print(f"  Min Stirling power (W):     {min(s.stirling_power_w for s in active_before):7.1f} -> {min(s.stirling_power_w for s in active_after):7.1f}")


def _print_weak_node_table(before: list[ThermalState], after: list[ThermalState], weak_nodes: list[int]) -> None:
    print("\nWeak-node uplift results:")
    print(f"{'Hour':>4} {'Cool_W':>8} {'ACH':>6} {'Stirl_W':>8} {'T_int':>7}   ->   {'Cool_W':>8} {'ACH':>6} {'Stirl_W':>8} {'T_int':>7}")
    print("-" * 90)
    for hour in weak_nodes:
        b = before[hour]
        a = after[hour]
        print(
            f"{hour:>4} {b.cooling_power_w:>8.1f} {b.air_changes_per_hour:>6.2f} {b.stirling_power_w:>8.1f} {b.interior_temp_estimate_c:>7.2f}"
            f"   ->   {a.cooling_power_w:>8.1f} {a.air_changes_per_hour:>6.2f} {a.stirling_power_w:>8.1f} {a.interior_temp_estimate_c:>7.2f}"
        )


if __name__ == "__main__":
    print("AeroCement Weak-Node Uplift")
    print("=" * 50)
    baseline, uplifted, weak_nodes = uplift_weak_nodes()
    print(f"Weak nodes selected: {weak_nodes}")
    _print_weak_node_table(baseline, uplifted, weak_nodes)
    _print_floor_comparison(baseline, uplifted)

    export_json(baseline, "design_day_baseline.json")
    export_json(uplifted, "design_day_uplifted.json")
