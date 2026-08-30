# Energy System — Overview

> ⚠️ **THEORETICAL** — Based on established thermodynamic principles. Complete integrated system requires prototype validation.

The AeroCement energy system is a passive solar-thermal loop that requires no grid connection, no compressor, and no fuel. It drives cooling, ventilation, and mechanical/electrical work using only solar radiation and the temperature difference between the sun-heated chimney and the evaporatively cooled air stream.

---

## The Four Energy Subsystems

| Subsystem | Role | Physics Basis |
|-----------|------|--------------|
| Stack Effect Chimney | Drives airflow passively | Buoyancy (density differential) |
| Evaporative Cooling Tower | Conditions incoming air | Latent heat of vaporization |
| Thermal Mass Shell | Moderates temperature swings | Sensible heat storage |
| Stirling Engine | Converts ΔT to electricity | Closed regenerative cycle |

These four subsystems form an integrated thermodynamic circuit driven entirely by solar input.

---

## Documents in This Section

| File | Contents |
|------|----------|
| [01_SOLAR_THERMAL_LOOP.md](01_SOLAR_THERMAL_LOOP.md) | Stack effect, evaporative cooling, thermal mass, nighttime radiation — Thesis Sections 2.1–2.7 |
| [02_THERMODYNAMIC_ANALYSIS.md](02_THERMODYNAMIC_ANALYSIS.md) | First and second law analysis, efficiency calculations — Thesis Section 3 |
| [03_STIRLING_ENGINE.md](03_STIRLING_ENGINE.md) | Stirling cycle, integration design, power output — Thesis Section 3.2 |
| [04_VS_GRID_INFRASTRUCTURE.md](04_VS_GRID_INFRASTRUCTURE.md) | Comparative analysis vs. grid-connected housing — Thesis Section 3.4 |

---

## Key Performance Targets (Theoretical)

| Parameter | Target | Validation Status |
|-----------|--------|------------------|
| Passive cooling offset | >80% vs. conventional AC | ❌ Not yet validated |
| Interior temperature (35–45°C ambient) | 18–26°C | ❌ Not yet validated |
| Stirling electrical output | 150–400W (peak solar hours) | ❌ Not yet validated |
| Air changes per hour | 4–6 ACH passive | ❌ Not yet validated |
| Water use (evaporative) | 8–15 L/hour (arid peak) | ❌ Not yet validated |

---

## Thermodynamic Simulation

Run the Python simulation to calculate design-day performance for your specific dome geometry and climate:

```bash
python3 code/python/thermodynamic_ledger.py
```

See [Appendix A in THESIS.md](../../THESIS.md#appendix-a-thermodynamic-ledger) for full code documentation.

---

← [Back to Repository Root](../../README.md)
