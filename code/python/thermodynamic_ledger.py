#!/usr/bin/env python3
"""
AeroCement Ecosystem — Thermodynamic Ledger
==========================================
Calculates and records thermal flows, Stirling engine output,
evaporative cooling performance, and stack effect airflow for
the AeroCement passive solar dome system.

⚠  THEORETICAL MODEL — All outputs require prototype validation.

License: GPL v3
Repository: https://github.com/jesseray718/openroot-thesis
"""

import math
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


# ── Physical Constants ──────────────────────────────────────────────────────
G = 9.81            # gravitational acceleration (m/s²)
R_AIR = 287.05      # specific gas constant for dry air (J/kg·K)
CP_AIR = 1005.0     # specific heat of air at constant pressure (J/kg·K)
RHO_WATER = 1000.0  # density of water (kg/m³)
L_WATER = 2430000.0 # latent heat of vaporization at 25°C (J/kg)


@dataclass
class SiteConditions:
    """Ambient site conditions for a given calculation period."""
    timestamp: str
    ambient_temp_c: float        # dry-bulb temperature (°C)
    relative_humidity: float     # fractional (0.0–1.0)
    solar_irradiance_wm2: float  # W/m²
    wind_speed_ms: float         # m/s


@dataclass
class DomeGeometry:
    """Physical parameters of the AeroCement dome."""
    diameter_m: float           # dome base diameter (m)
    chimney_height_m: float     # chimney height above apex (m)
    chimney_area_m2: float      # chimney cross-sectional area (m²)
    shell_thickness_m: float    # shell thickness (m)
    shell_density_kgm3: float   # shell material density (kg/m³)
    shell_cp_jkgk: float        # shell specific heat (J/kg·K)
    shell_k_wm2k: float         # shell thermal conductivity (W/m·K)
    evap_media_depth_m: float   # evaporative media depth (m)
    evap_saturation_eff: float  # saturation efficiency (0.0–1.0)


@dataclass
class ThermalState:
    """Computed thermal state of the dome at a point in time."""
    timestamp: str
    # Stack effect
    chimney_air_temp_c: float
    stack_pressure_pa: float
    airflow_m3s: float
    air_changes_per_hour: float
    # Evaporative cooling
    wet_bulb_temp_c: float
    supply_air_temp_c: float
    cooling_power_w: float
    water_consumption_kgh: float
    # Stirling engine
    t_hot_k: float
    t_cold_k: float
    carnot_efficiency: float
    stirling_efficiency: float
    stirling_power_w: float
    # Thermal mass
    heat_stored_kj: float
    # Summary
    interior_temp_estimate_c: float


def air_density(temp_c: float, rh: float = 0.0, pressure_pa: float = 101325.0) -> float:
    """
    Calculate moist air density (kg/m³).

    Parameters
    ----------
    temp_c : float
        Dry-bulb temperature (°C).
    rh : float
        Relative humidity, fractional (0.0–1.0).
    pressure_pa : float
        Atmospheric pressure (Pa).
    """
    temp_k = temp_c + 273.15
    # Saturation vapor pressure via Magnus formula
    p_sat = 610.78 * math.exp(17.27 * temp_c / (temp_c + 237.3))
    p_vapor = rh * p_sat
    p_dry = pressure_pa - p_vapor
    rho = (p_dry / (R_AIR * temp_k)) + (p_vapor / (461.5 * temp_k))
    return rho


def wet_bulb_temperature(temp_c: float, rh: float) -> float:
    """
    Estimate wet-bulb temperature (°C) using Stull (2011) approximation.

    Valid for: -20°C < T < 50°C, 5% < RH < 99%.

    Reference: Stull, R. (2011). Wet-Bulb Temperature from Relative Humidity
    and Air Temperature. Journal of Applied Meteorology and Climatology, 50(11).
    """
    rh_pct = rh * 100.0
    tw = (temp_c * math.atan(0.151977 * math.sqrt(rh_pct + 8.313659))
          + math.atan(temp_c + rh_pct)
          - math.atan(rh_pct - 1.676331)
          + 0.00391838 * rh_pct ** 1.5 * math.atan(0.023101 * rh_pct)
          - 4.686035)
    return tw


def saturation_humidity_ratio(temp_c: float, pressure_pa: float = 101325.0) -> float:
    """
    Calculate saturation humidity ratio (kg water / kg dry air).

    Parameters
    ----------
    temp_c : float
        Temperature (°C).
    pressure_pa : float
        Atmospheric pressure (Pa).
    """
    p_sat = 610.78 * math.exp(17.27 * temp_c / (temp_c + 237.3))
    return 0.62198 * p_sat / (pressure_pa - p_sat)


def stack_effect_pressure(
    chimney_height_m: float,
    outdoor_temp_c: float,
    chimney_temp_c: float,
    outdoor_rh: float = 0.0
) -> float:
    """
    Calculate stack effect pressure differential (Pa).

    ΔP = C × h × g × (ρ_outside − ρ_inside)

    Parameters
    ----------
    chimney_height_m : float
        Vertical height of chimney air column (m).
    outdoor_temp_c : float
        Outdoor dry-bulb temperature (°C).
    chimney_temp_c : float
        Air temperature inside chimney (°C).
    outdoor_rh : float
        Outdoor relative humidity, fractional (0.0–1.0).
    """
    C = 0.65  # discharge coefficient (typical for rectangular openings)
    rho_out = air_density(outdoor_temp_c, outdoor_rh)
    rho_in = air_density(chimney_temp_c, 0.0)
    delta_p = C * chimney_height_m * G * (rho_out - rho_in)
    return max(delta_p, 0.0)


def airflow_from_pressure(
    pressure_pa: float,
    area_m2: float,
    cd: float = 0.65
) -> float:
    """
    Calculate volumetric airflow (m³/s) from pressure differential.

    Uses orifice equation: Q = Cd × A × sqrt(2 × ΔP / ρ)

    Parameters
    ----------
    pressure_pa : float
        Driving pressure differential (Pa).
    area_m2 : float
        Opening area (m²).
    cd : float
        Discharge coefficient.
    """
    rho = 1.2  # approximate standard air density (kg/m³)
    if pressure_pa <= 0:
        return 0.0
    velocity = math.sqrt(2 * pressure_pa / rho)
    return cd * area_m2 * velocity


def calculate_thermal_state(
    site: SiteConditions,
    dome: DomeGeometry,
    chimney_solar_absorptance: float = 0.90,
    stirling_fraction_of_carnot: float = 0.50
) -> ThermalState:
    """
    Calculate the complete theoretical thermal state of the AeroCement dome.

    ⚠  All outputs are theoretical estimates based on simplified models.
    Prototype measurement is required to validate these calculations.

    Parameters
    ----------
    site : SiteConditions
        Current ambient conditions.
    dome : DomeGeometry
        Physical dome parameters.
    chimney_solar_absorptance : float
        Solar absorptance of chimney surface (0–1). Default 0.90 for dark surface.
    stirling_fraction_of_carnot : float
        Stirling engine actual efficiency as fraction of Carnot. Default 0.50.

    Returns
    -------
    ThermalState
        Calculated thermal state at given conditions.
    """
    # ── 1. Chimney temperature estimate ────────────────────────────────────
    chimney_perimeter = math.sqrt(dome.chimney_area_m2) * 4  # approximate square
    chimney_wall_area = chimney_perimeter * dome.chimney_height_m
    solar_gain_w = site.solar_irradiance_wm2 * chimney_solar_absorptance * chimney_wall_area
    # Temperature rise estimate: simplified single-pass heat exchanger
    mass_flow_approx = 0.1  # kg/s initial approximation
    delta_t_chimney = solar_gain_w / (mass_flow_approx * CP_AIR + 1e-6)
    chimney_temp_c = site.ambient_temp_c + min(delta_t_chimney, 50.0)

    # ── 2. Stack effect and airflow ─────────────────────────────────────────
    stack_p = stack_effect_pressure(
        dome.chimney_height_m,
        site.ambient_temp_c,
        chimney_temp_c,
        site.relative_humidity
    )
    airflow_m3s = airflow_from_pressure(stack_p, dome.chimney_area_m2)
    dome_volume = (2.0 / 3.0) * math.pi * (dome.diameter_m / 2) ** 3  # hemisphere
    ach = (airflow_m3s * 3600.0) / dome_volume

    # ── 3. Evaporative cooling ──────────────────────────────────────────────
    t_wb = wet_bulb_temperature(site.ambient_temp_c, site.relative_humidity)
    t_supply = site.ambient_temp_c - (
        dome.evap_saturation_eff * (site.ambient_temp_c - t_wb)
    )
    air_mass_flow = airflow_m3s * air_density(site.ambient_temp_c, site.relative_humidity)
    cooling_power = air_mass_flow * CP_AIR * max(site.ambient_temp_c - t_supply, 0.0)

    # Water consumption estimate
    w_sat = saturation_humidity_ratio(site.ambient_temp_c)
    w_in = w_sat * site.relative_humidity  # approximation
    delta_w = dome.evap_saturation_eff * (w_sat - w_in)
    water_kg_s = air_mass_flow * delta_w
    water_kg_h = water_kg_s * 3600.0

    # ── 4. Stirling engine ──────────────────────────────────────────────────
    t_hot_k = chimney_temp_c + 273.15
    t_cold_k = t_supply + 273.15
    if t_hot_k > t_cold_k and t_cold_k > 0:
        carnot_eff = 1.0 - (t_cold_k / t_hot_k)
    else:
        carnot_eff = 0.0
    stirling_eff = stirling_fraction_of_carnot * carnot_eff
    stirling_power = stirling_eff * solar_gain_w

    # ── 5. Thermal mass heat storage ────────────────────────────────────────
    shell_surface = 2.0 * math.pi * (dome.diameter_m / 2) ** 2  # hemisphere
    shell_volume = shell_surface * dome.shell_thickness_m
    shell_mass = shell_volume * dome.shell_density_kgm3
    delta_t_mass = 10.0  # assume 10°C diurnal swing
    heat_stored_kj = shell_mass * dome.shell_cp_jkgk * delta_t_mass / 1000.0

    # ── 6. Interior temperature estimate ───────────────────────────────────
    interior_temp = t_supply + 2.0  # +2°C for internal gains and mixing imperfection

    return ThermalState(
        timestamp=site.timestamp,
        chimney_air_temp_c=round(chimney_temp_c, 2),
        stack_pressure_pa=round(stack_p, 2),
        airflow_m3s=round(airflow_m3s, 4),
        air_changes_per_hour=round(ach, 2),
        wet_bulb_temp_c=round(t_wb, 2),
        supply_air_temp_c=round(t_supply, 2),
        cooling_power_w=round(cooling_power, 1),
        water_consumption_kgh=round(water_kg_h, 3),
        t_hot_k=round(t_hot_k, 2),
        t_cold_k=round(t_cold_k, 2),
        carnot_efficiency=round(carnot_eff, 4),
        stirling_efficiency=round(stirling_eff, 4),
        stirling_power_w=round(stirling_power, 1),
        heat_stored_kj=round(heat_stored_kj, 1),
        interior_temp_estimate_c=round(interior_temp, 2),
    )


def run_design_day(
    dome: DomeGeometry,
    peak_temp_c: float = 40.0,
    peak_rh: float = 0.20,
    peak_irradiance_wm2: float = 900.0,
    hours: int = 24
) -> list:
    """
    Simulate a design-day thermal performance profile over 24 hours.

    Uses sinusoidal approximations for temperature, humidity, and irradiance
    variation. Temperature peaks at hour 14, solar at hour 12.

    Parameters
    ----------
    dome : DomeGeometry
        Physical dome parameters.
    peak_temp_c : float
        Peak ambient dry-bulb temperature (°C). Default 40°C.
    peak_rh : float
        Minimum relative humidity (at peak temperature). Default 0.20.
    peak_irradiance_wm2 : float
        Peak solar irradiance (W/m²). Default 900 W/m².
    hours : int
        Number of hours to simulate. Default 24.

    Returns
    -------
    list[ThermalState]
        Hourly thermal states over the design day.
    """
    results = []
    for hour in range(hours):
        # Simplified sinusoidal profiles
        temp_c = (peak_temp_c - 8.0) + 8.0 * math.sin(math.pi * (hour - 6) / 12)
        rh = peak_rh + (0.35 - peak_rh) * (1.0 - math.sin(math.pi * (hour - 6) / 12))
        irradiance = max(0.0, peak_irradiance_wm2 * math.sin(math.pi * (hour - 6) / 12))

        site = SiteConditions(
            timestamp=f"design-day T+{hour:02d}h",
            ambient_temp_c=temp_c,
            relative_humidity=max(0.05, min(rh, 0.99)),
            solar_irradiance_wm2=irradiance,
            wind_speed_ms=2.0
        )
        state = calculate_thermal_state(site, dome)
        results.append(state)
    return results


def print_summary(states: list) -> None:
    """Print a formatted summary table of hourly thermal states."""
    print(f"\n{'Hour':>4} {'T_amb':>6} {'T_supp':>7} {'T_int':>6} {'ACH':>5} "
          f"{'Cool_W':>7} {'Stirl_W':>8} {'H2O_L/h':>8}")
    print("-" * 65)
    for i, s in enumerate(states):
        print(f"{i:>4} {s.supply_air_temp_c + 8.0:>6.1f} {s.supply_air_temp_c:>7.1f} "
              f"{s.interior_temp_estimate_c:>6.1f} {s.air_changes_per_hour:>5.1f} "
              f"{s.cooling_power_w:>7.0f} {s.stirling_power_w:>8.0f} "
              f"{s.water_consumption_kgh:>8.2f}")


def export_json(states: list, filename: str) -> None:
    """
    Export thermal state results to JSON file.

    Parameters
    ----------
    states : list[ThermalState]
        Thermal states to export.
    filename : str
        Output file path.
    """
    data = [asdict(s) for s in states]
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Exported {len(states)} records to {filename}")


# ── Default dome configuration (6m diameter) ────────────────────────────────
DEFAULT_DOME = DomeGeometry(
    diameter_m=6.0,
    chimney_height_m=5.0,
    chimney_area_m2=0.20,
    shell_thickness_m=0.075,
    shell_density_kgm3=1800.0,
    shell_cp_jkgk=850.0,
    shell_k_wm2k=0.45,
    evap_media_depth_m=0.15,
    evap_saturation_eff=0.75,
)


if __name__ == "__main__":
    print("AeroCement Ecosystem — Thermodynamic Ledger")
    print("=" * 50)
    print("Design-Day Simulation: 40°C peak, 20% RH, 900 W/m² peak irradiance")
    print("\nDome Parameters:")
    print(f"  Diameter:        {DEFAULT_DOME.diameter_m} m")
    print(f"  Chimney height:  {DEFAULT_DOME.chimney_height_m} m")
    print(f"  Chimney area:    {DEFAULT_DOME.chimney_area_m2} m²")
    print(f"  Shell thickness: {DEFAULT_DOME.shell_thickness_m * 1000:.0f} mm")
    print(f"  Shell k:         {DEFAULT_DOME.shell_k_wm2k} W/m·K")
    print(f"  Evap efficiency: {DEFAULT_DOME.evap_saturation_eff * 100:.0f}%")

    states = run_design_day(DEFAULT_DOME)
    print_summary(states)

    peak_cool = max(s.cooling_power_w for s in states)
    peak_stirl = max(s.stirling_power_w for s in states)
    peak_h2o = max(s.water_consumption_kgh for s in states)
    avg_int = sum(s.interior_temp_estimate_c for s in states) / len(states)

    print(f"\n── Peak Performance ─────────────────────────────────────")
    print(f"Peak cooling power:    {peak_cool:.0f} W")
    print(f"Peak Stirling output:  {peak_stirl:.0f} W")
    print(f"Peak water use:        {peak_h2o:.2f} L/h")
    print(f"Average interior temp: {avg_int:.1f}°C")
    print(f"\n⚠  THEORETICAL — These calculations require prototype validation.")
    print(f"   See THESIS.md and docs/01_ENERGY/ for methodology.")
