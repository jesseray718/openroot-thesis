# Thermodynamic Analysis — Section 3

> ⚠️ **THEORETICAL** — All efficiency values and outputs require prototype validation.

*From THESIS.md Section 3*

---

## 3.1 First and Second Law Analysis

### First Law (Energy Conservation)

24-hour system energy balance:

```
Q_solar = Q_interior_cooling + Q_stirling_work + Q_evap_losses + Q_radiation + Q_ground
```

- Q_solar: 5–7 kWh/m²/day in target climates
- Q_stirling_work: mechanical/electrical work extracted
- Q_evap_losses: energy consumed by water evaporation
- Q_radiation: nighttime longwave emission
- Q_ground: ground-coupled exchange

### Second Law (Entropy and Carnot Limit)

System operates between:
- **Hot reservoir:** Solar-heated chimney, T_H ≈ 80–120°C (353–393 K)
- **Cold reservoir:** Evaporatively cooled air, T_C ≈ 20–28°C (293–301 K)

**Carnot efficiency limit:**
```
η_Carnot = 1 − (T_C / T_H) = 1 − (298/373) = 20.1%
```

Real Stirling engines achieve 40–70% of Carnot. Proposed system target: 50% of Carnot ≈ **10% thermal-to-electrical efficiency** on chimney ΔT.

---

## 3.3 Thermal Efficiency Calculations

### Passive Cooling COP

The passive system delivers cooling without a compressor. Since W_mechanical ≈ 0, effective COP is theoretically unbounded. Real costs: water consumption and any supplemental fan power.

### Water Consumption Estimate

At 0.1 m³/s airflow, 40°C / 20% RH, 75% saturation efficiency:

```
ΔW ≈ 0.0298 kg water / kg dry air
Air mass flow ≈ 0.11 kg/s
Water consumption ≈ 0.00328 kg/s ≈ 11.8 L/hour (peak)
```

**This is a critical system constraint.** Water supply must be confirmed for the deployment site before construction.

---

*See [Stirling Engine](03_STIRLING_ENGINE.md) for Section 3.2 and [Grid Comparison](04_VS_GRID_INFRASTRUCTURE.md) for Section 3.4.*

← [Solar Thermal Loop](01_SOLAR_THERMAL_LOOP.md) | → [Stirling Engine](03_STIRLING_ENGINE.md)
