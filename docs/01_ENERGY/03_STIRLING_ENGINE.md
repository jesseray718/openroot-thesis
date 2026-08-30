# Stirling Engine Integration — Section 3.2

> ⚠️ **THEORETICAL** — Commercial low-ΔT Stirling engines exist at these output levels. The specific integration with a passive ventilation chimney as heat source is the novel aspect requiring prototype validation.

*From THESIS.md Section 3.2*

---

## Stirling Cycle Fundamentals

The Stirling cycle is a closed regenerative thermodynamic cycle operating between two temperature reservoirs. Unlike internal combustion engines, Stirling engines:
- Use **any** external heat source (including low-grade solar heat)
- Operate **silently**
- Have theoretical efficiencies approaching the Carnot limit
- Have **no combustion** — zero emissions in operation

### The Four Processes

1. **Isothermal Expansion** — Gas expands at T_H, absorbing heat from chimney wall
2. **Isochoric Cooling** — Gas cools at constant volume; heat stored in regenerator
3. **Isothermal Compression** — Gas compressed at T_C, rejecting heat to cooled air
4. **Isochoric Heating** — Gas reheated at constant volume from regenerator

---

## Proposed Integration

A beta-configuration Stirling engine is mounted at the junction between:
- **Hot side:** Chimney wall surface (T_H ≈ 80–100°C under solar loading)
- **Cold side:** Evaporatively cooled air stream (T_C ≈ 20–25°C)

The ΔT of 55–75°C drives the engine.

---

## Theoretical Power Output

```
P_theoretical = η × Q_input_rate

η ≈ 0.50 × η_Carnot = 0.50 × (1 − 298/373) = 0.10

Q_input_rate ≈ 2–3 kW (solar flux on chimney absorber area)

P_theoretical = 0.10 × 2,500 W = 250 W
```

**Target operating range:** 150–400W continuous electrical output during peak solar hours (6–8 hours/day).

**⚠ This calculation requires prototype validation.** Key unknowns:
- Actual chimney wall temperature under operating airflow conditions
- Thermal resistance at engine hot-side interface
- Cold-side temperature stability with varying evaporative cooling load

---

## Prior Art on Low-ΔT Stirling Engines

Commercial and research low-ΔT Stirling generators have been demonstrated at these output levels with comparable temperature differentials. The AeroCement integration uses the passive chimney as heat source — this is the novel design element.

References: Kongtragool & Wongwises (2003), Kolin (1991), Senft (1993).

---

← [Thermodynamic Analysis](02_THERMODYNAMIC_ANALYSIS.md) | → [Grid Comparison](04_VS_GRID_INFRASTRUCTURE.md)
