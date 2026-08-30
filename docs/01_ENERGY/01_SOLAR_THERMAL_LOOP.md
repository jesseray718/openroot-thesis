# Solar Thermal Loop — Sections 2.1–2.7

> ⚠️ **THEORETICAL** — Each subsystem is based on established physics. The integrated loop has not been built and instrumented at scale.

*From THESIS.md Sections 2.1–2.7*

---

## 2.1 Stack Effect Chimney

**Principle (Established Physics):**  
The stack effect is a well-documented thermodynamic phenomenon. When a column of air is heated, its density decreases, creating a buoyancy-driven pressure differential that drives airflow upward.

**Governing Equation:**

```
ΔP = C × h × g × (ρ_outside − ρ_inside)
```

Where:
- ΔP = pressure difference driving airflow (Pa)
- C = discharge coefficient (~0.65)
- h = chimney height (m)
- g = 9.81 m/s²
- ρ_outside, ρ_inside = air densities (kg/m³)

**Proposed Configuration:**

Central thermal chimney rising 4–6m above dome apex. Solar radiation heats the chimney's dark absorber surface, raising interior chimney air temperature 15–25°C above ambient. This drives ~0.3–0.8 m/s continuous passive airflow.

**Theoretical Air Exchange Rate (6m dome, 5m chimney):**

```
V_flow ≈ 0.2 m² × 0.5 m/s = 0.1 m³/s = 360 m³/hour
Dome volume ≈ 75 m³
ACH ≈ 4.8 air changes/hour
```

**⚠ Requires instrumented validation.**

---

## 2.2 Evaporative Cooling Tower

**Principle (Established Physics):**  
Evaporative cooling exploits the latent heat of vaporization (~2,430 kJ/kg at 25°C). The wet-bulb temperature is the theoretical minimum achievable.

**Performance in Arid Conditions:**

At 40°C ambient / 20% RH:
- Wet-bulb ≈ 22°C
- Theoretical cooling potential: 18°C
- At 75% saturation efficiency: supply air ≈ 26.5°C

```
T_supply = 40 − (0.75 × (40 − 22)) = 26.5°C
```

**Water Consumption at Peak:**

```
≈ 12 L/hour at 0.1 m³/s airflow, 40°C / 20% RH
```

This is a critical site-specific constraint. Water source (rainwater, condensate, groundwater) must be confirmed before system deployment.

---

## 2.3 Thermal Mass Integration

**Thermal Storage in Shell:**

```
Q_stored = m × Cp × ΔT
```

For 6m dome shell at AeroCement target density (1,800 kg/m³):
```
Shell mass ≈ 15,300 kg
Q_storage ≈ 15,300 × 0.85 × 8 = 104,040 kJ ≈ 29 kWh
```

This moderates interior temperatures through 12 hours of peak loading.  
**Shell mass and thermal properties require measurement from actual AeroCement mix.**

---

## 2.4 Passive Ventilation Circuit

Complete ventilation circuit (theoretical):

1. **Intake** → Subsoil pre-conditioning tunnel at 1.5m depth (−5–10°C from ground coupling)
2. **Treatment** → Evaporative media section
3. **Distribution** → Cool air rises through living space via floor registers
4. **Extraction** → Warm air drawn into stack chimney
5. **Exhaust** → Chimney discharge above dome apex sustains negative pressure

This circuit is analogous to traditional Persian wind-catcher (malqaf) systems. The novel aspect is integration with the AeroCement shell and Stirling engine heat recovery.

---

## 2.5 Nighttime Radiative Cooling

Clear-sky radiative cooling allows high-emissivity (ε > 0.9) surfaces to emit longwave radiation to the sky vault (sky effective temperature can be 10–20°C below ambient on clear nights).

**Estimated nighttime cooling capacity:** 30–60 W/m² under clear conditions.

**Limitation:** Cloud cover eliminates this benefit. Geographic validation required.

---

## 2.6 Thermal Energy Storage

**Phase-Change Material (PCM):**  
Fatty acid eutectics (~21°C melting point) embedded in floor slabs:
```
Q_latent = 200 kg × 135 kJ/kg = 27,000 kJ = 7.5 kWh
```

**Underground Thermal Storage:**  
Earthen cisterns at 2m depth — ground temperature varies only ±2–3°C seasonally.

---

## 2.7 System Integration Summary

```
Solar Input → Chimney Heating → Stack Draft → Ventilation Airflow
                                                      ↓
                                          Evaporative Cooling Tower
                                                      ↓
                                          Conditioned Air to Interior
                                                      ↓
                                          Thermal Mass Absorption
                                                      ↓
                                          Nighttime Radiation to Sky
                                                      ↓
                                          Pre-cooled Mass → Repeat
```

The Stirling engine recovers electrical work from the temperature differential across the chimney wall. Condensed water is recovered for irrigation.

**Critical Validation Point:** No full integrated system of this type has been instrumented at scale. Subsystem interactions — particularly evaporative water balance and airflow dynamics with Stirling engine load — require prototype study.

---

← [Energy Overview](README.md) | → [Thermodynamic Analysis](02_THERMODYNAMIC_ANALYSIS.md)
