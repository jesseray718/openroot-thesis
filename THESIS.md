> ⚠️ THEORETICAL ARCHITECTURE — VALIDATION REQUIRED
>
> This thesis presents the AeroCement Ecosystem as a theoretical integrated system based on established thermodynamic principles (stack effect, evaporative cooling, sensible heat transfer, Stirling cycle). Individual components are proven. The COMPLETE INTEGRATED SYSTEM at scale has NOT been constructed or instrumented.
>
> All performance claims require real-world prototype validation with:
> - Instrumented measurements of thermal flows
> - Long-term structural monitoring
> - Integration testing of subsystems
> - Soil and water interaction studies
>
> This is a research proposal and design framework, not a proven product. Builders should validate at prototype scale before full deployment.

---

# AeroCement Ecosystem: Civilization 2.0

## A Comprehensive Thesis on Passive Solar-Thermal Infrastructure for Open-Source Human Survival

**Version:** 3.0  
**License:** CC-BY-SA 4.0 (Hardware) | GPL v3 (Software)  
**Repository:** https://github.com/jesseray718/openroot-thesis

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Solar Thermal Loop — The Energy Foundation](#2-solar-thermal-loop)
   - 2.1 [Stack Effect Chimney](#21-stack-effect-chimney)
   - 2.2 [Evaporative Cooling Tower](#22-evaporative-cooling-tower)
   - 2.3 [Thermal Mass Integration](#23-thermal-mass-integration)
   - 2.4 [Passive Ventilation Circuit](#24-passive-ventilation-circuit)
   - 2.5 [Nighttime Radiative Cooling](#25-nighttime-radiative-cooling)
   - 2.6 [Thermal Energy Storage](#26-thermal-energy-storage)
   - 2.7 [System Integration Summary](#27-system-integration-summary)
3. [Thermodynamic Analysis](#3-thermodynamic-analysis)
   - 3.1 [First and Second Law Analysis](#31-first-and-second-law-analysis)
   - 3.2 [Stirling Engine Integration](#32-stirling-engine-integration)
   - 3.3 [Thermal Efficiency Calculations](#33-thermal-efficiency-calculations)
   - 3.4 [AeroCement vs. Grid Infrastructure](#34-aerocement-vs-grid-infrastructure)
4. [Shelter System — AeroCement Shell](#4-shelter-system)
   - 4.1 [Material System](#41-material-system)
   - 4.2 [Geodesic Geometry](#42-geodesic-geometry)
   - 4.3 [Urban Applications](#43-urban-applications)
5. [Life Support Systems](#5-life-support-systems)
   - 5.1 [Black Locust as Keystone Species](#51-black-locust-as-keystone-species)
   - 5.2 [Quail Towers — Protein Integration](#52-quail-towers)
   - 5.3 [Aquaponics Integration](#53-aquaponics-integration)
   - 5.4 [Seed Banking](#54-seed-banking)
6. [Build Protocols and Hard Constraints](#6-build-protocols)
7. [Token Economy — Proof of Physical Work](#7-token-economy)
   - 7.1 [Proof of Physical Work Protocol](#71-proof-of-physical-work)
   - 7.2 [Token Mechanics](#72-token-mechanics)
   - 7.3 [DAO Governance](#73-dao-governance)
   - 7.4 [Bounty System](#74-bounty-system)
8. [Defensive Publication and Open-Source Strategy](#8-defensive-publication)
9. [Conclusion](#9-conclusion)

**Appendices:**
- [Appendix A: Thermodynamic Ledger (Python)](#appendix-a-thermodynamic-ledger)
- [Appendix B: Material Specifications](#appendix-b-material-specifications)
- [Appendix C: Build Sequence](#appendix-c-build-sequence)

---

## 1. Executive Summary

The AeroCement Ecosystem is a proposed integrated framework for off-grid human habitation that combines passive thermodynamic systems, bio-based structural materials, integrated food production, and a cryptographic token economy anchored to verifiable physical labor.

The system addresses four fundamental human needs simultaneously:
- **Energy:** Passive solar-thermal loop driving cooling, heating, and mechanical work
- **Shelter:** Lightweight geopolymer dome with integrated thermal mass
- **Life Support:** Integrated food, water, and biological systems
- **Economy:** Proof-of-Physical-Work token protocol for community coordination

### Core Theoretical Claim

The AeroCement Ecosystem proposes that by integrating well-understood thermodynamic phenomena — stack effect, evaporative cooling, thermal mass, and the Stirling cycle — into a single coherent building system, it becomes possible to meet a family's basic energy, shelter, food, and water needs from a sub-acre footprint with zero fossil fuel inputs.

**Each individual component is based on established physics.** The integration of these components at the specific scales and configurations proposed here constitutes the theoretical contribution requiring validation.

### Performance Targets (Theoretical — Require Validation)

| Parameter | Proposed Target | Basis |
|-----------|----------------|-------|
| Interior temperature range | 18–26°C in ambient 35–45°C | Stack effect + evaporative cooling |
| Passive cooling load offset | >80% vs. conventional AC | Thermal mass + ventilation |
| Food production | >50% of caloric needs on 0.1 acre | Aquaponics + quail protein |
| Water recovery | >60% from evaporative systems | Condensate recovery |
| Stirling electrical output | 200–500W continuous | ΔT of 40–60°C across shell |

---

## 2. Solar Thermal Loop — The Energy Foundation

### 2.1 Stack Effect Chimney

**Principle (Established Physics):**  
The stack effect (also called chimney effect) is a well-documented thermodynamic phenomenon. When a column of air is heated, its density decreases relative to ambient air, creating a buoyancy-driven pressure differential that drives airflow upward.

**Governing Equation:**

```
ΔP = C × h × g × (ρ_outside − ρ_inside)
```

Where:
- ΔP = pressure difference driving airflow (Pa)
- C = discharge coefficient (~0.65 for typical openings)
- h = vertical height of air column (m)
- g = gravitational acceleration (9.81 m/s²)
- ρ_outside = ambient air density (kg/m³)
- ρ_inside = heated interior air density (kg/m³)

**Proposed Configuration:**

The AeroCement dome incorporates a central thermal chimney that rises 4–6 meters above the dome apex. Solar radiation heats the chimney's dark absorber surface, raising interior chimney air temperature 15–25°C above ambient. This drives a continuous passive airflow of approximately 0.3–0.8 m/s through the building.

**Theoretical Air Exchange Rate:**

For a dome diameter of 6m and chimney height of 5m:
```
V_flow ≈ A_chimney × v_air
V_flow ≈ 0.2 m² × 0.5 m/s = 0.1 m³/s = 360 m³/hour
```

A 6m dome has interior volume of approximately 75 m³, yielding ~4.8 air changes per hour — consistent with comfortable passive ventilation. **This calculation requires instrumented validation.**

### 2.2 Evaporative Cooling Tower

**Principle (Established Physics):**  
Evaporative cooling exploits the latent heat of vaporization of water (2,257 kJ/kg at 100°C; approximately 2,430 kJ/kg at 25°C). As water evaporates, it absorbs this latent heat from the surrounding air, reducing air temperature.

The wet-bulb temperature represents the theoretical minimum achievable via evaporative cooling:

```
T_wb = T_db × arctan[0.151977 × (RH + 8.313659)^0.5]
     + arctan(T_db + RH)
     − arctan(RH − 1.676331)
     + 0.00391838 × RH^1.5 × arctan(0.023101 × RH)
     − 4.686035
```

(Stull, 2011 approximation)

**Proposed Configuration:**

Incoming air drawn by the stack effect passes through a wetted-media evaporative section before entering the dome. At 40°C ambient and 20% relative humidity (arid conditions), the wet-bulb temperature is approximately 22°C — providing up to 18°C of passive cooling with no mechanical energy input.

**Efficiency Factor:**

Real-world evaporative coolers achieve 70–90% of theoretical wet-bulb depression. Proposed system target: 75% saturation efficiency.

```
T_supply = T_ambient − (0.75 × (T_ambient − T_wet_bulb))
T_supply = 40 − (0.75 × 18) = 40 − 13.5 = 26.5°C
```

**Validation requirement:** Water consumption rate, actual saturation efficiency at target airflow, and media clogging resistance all require prototype measurement.

### 2.3 Thermal Mass Integration

**Principle (Established Physics):**  
Thermal mass stores sensible heat and releases it with a time delay, shifting peak thermal loads and moderating diurnal temperature swings.

```
Q_stored = m × Cp × ΔT
```

Where:
- Q_stored = heat stored (kJ)
- m = mass of thermal storage medium (kg)
- Cp = specific heat capacity (kJ/kg·K)
- ΔT = temperature change (K)

**AeroCement Shell Properties (Proposed):**

The AeroCement shell (see Section 4.1) incorporates fly ash geopolymer with density ~1,800 kg/m³ and specific heat ~0.85 kJ/kg·K. For a dome shell of 6m diameter, 75mm thickness:

```
Shell volume ≈ 4πr² × t = 4π(3)² × 0.075 ≈ 8.5 m³
Shell mass ≈ 8.5 × 1,800 = 15,300 kg
Q_storage = 15,300 × 0.85 × 8 = 104,040 kJ (for 8°C swing)
```

This provides approximately 29 kWh of thermal storage — sufficient to maintain interior temperatures within 4°C of target through 12 hours of peak solar loading. **Shell mass and thermal properties require measurement from actual AeroCement mix.**

### 2.4 Passive Ventilation Circuit

The complete proposed ventilation circuit operates as follows:

1. **Intake:** Cool, humid air enters at ground level through earthen bermed intake tunnel (subsoil pre-conditioning reduces incoming air temperature by 5–10°C via ground coupling at 1.5m depth)
2. **Treatment:** Air passes through evaporative media section
3. **Distribution:** Cooled air rises through living space via floor-level registers
4. **Extraction:** Warm, stale air is drawn upward into the stack chimney
5. **Exhaust:** Chimney discharges above dome apex, creating negative pressure that sustains the circuit

**Design Note:** This circuit is analogous to wind-catcher (malqaf) systems used in traditional Persian and Egyptian architecture for millennia. The proposed innovation is integration with the AeroCement structural system and Stirling engine heat recovery. The underlying passive ventilation physics is well-established; the specific integration geometry requires prototype validation.

### 2.5 Nighttime Radiative Cooling

**Principle:**  
Clear-sky radiative cooling allows surfaces to emit longwave radiation to the cold sky vault (effective sky temperature can be 10–20°C below ambient on clear nights). This can passively cool surfaces below ambient temperature.

**Application:**  
The dome's roof surface, treated with high-emissivity coating (ε > 0.9), radiates heat to the night sky, pre-cooling the thermal mass for the following day's loading. Estimated nighttime cooling capacity: 30–60 W/m² under clear conditions.

**Limitation:** Effective only under clear skies; cloud cover eliminates this benefit. Geographic validation required.

### 2.6 Thermal Energy Storage

Beyond the shell itself, the proposed system incorporates:

**Phase-Change Material (PCM) Panels:**  
Fatty acid eutectics (e.g., capric-lauric acid, melting point ~21°C) embedded in floor slabs store latent heat at near-comfort temperature. Heat of fusion: ~120–150 kJ/kg. For 200 kg of PCM:

```
Q_latent = 200 × 135 = 27,000 kJ = 7.5 kWh
```

**Underground Thermal Storage:**  
Interconnected earthen cisterns at 2m depth provide thermal inertia from ground-coupled mass. Ground temperature at 2m depth varies only ±2–3°C seasonally in most climates.

### 2.7 System Integration Summary

The energy subsystems form a thermodynamic circuit:

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

The Stirling engine (Section 3.2) recovers mechanical/electrical work from the temperature differential across the chimney wall. Water condensed from the evaporative system is recovered for irrigation. The system is proposed to operate as a closed-loop thermodynamic engine driven entirely by solar input.

**Critical Validation Point:** No full integrated system of this type has been instrumented at scale. The interactions between subsystems — particularly the water balance of the evaporative system and the airflow dynamics with the Stirling engine load — require prototype study.

---

## 3. Thermodynamic Analysis

### 3.1 First and Second Law Analysis

**First Law (Energy Conservation):**

The system energy balance over 24 hours:

```
Q_solar = Q_interior_cooling + Q_stirling_work + Q_evap_losses + Q_radiation + Q_ground
```

Where:
- Q_solar = incident solar energy captured by dome surface and chimney (~5–7 kWh/m²/day in target climates)
- Q_interior_cooling = sensible cooling delivered to living space
- Q_stirling_work = mechanical/electrical work extracted by Stirling engine
- Q_evap_losses = energy consumed by water evaporation
- Q_radiation = nighttime radiative losses
- Q_ground = ground-coupled heat exchange

**Second Law (Entropy):**

The system operates between a hot reservoir (solar-heated chimney, T_H ≈ 80–120°C) and a cold reservoir (evaporatively cooled air, T_C ≈ 20–28°C). The Carnot efficiency limit:

```
η_Carnot = 1 − (T_C / T_H) = 1 − (298 K / 373 K) = 0.201 = 20.1%
```

Real Stirling engines achieve 40–70% of Carnot efficiency. Proposed system target: 50% of Carnot = ~10% thermal-to-electrical efficiency on the chimney ΔT.

### 3.2 Stirling Engine Integration

**Principle:**  
The Stirling cycle is a closed regenerative thermodynamic cycle operating between two temperature reservoirs. Unlike internal combustion engines, Stirling engines use any external heat source, operate silently, and have theoretical efficiencies approaching Carnot limits.

**The Stirling cycle consists of four processes:**
1. **Isothermal Expansion:** Gas expands at T_H, absorbing heat
2. **Isochoric Cooling:** Gas cools at constant volume, heat stored in regenerator
3. **Isothermal Compression:** Gas compressed at T_C, rejecting heat
4. **Isochoric Heating:** Gas reheated at constant volume from regenerator

**Proposed Integration:**

A beta-configuration Stirling engine is mounted at the junction between the hot chimney wall (T_H ≈ 80–100°C under solar loading) and the evaporatively cooled air stream (T_C ≈ 20–25°C). The ΔT of 55–75°C drives the engine.

**Theoretical Power Output:**

```
P_theoretical = η × Q_input_rate
η ≈ 0.50 × η_Carnot = 0.50 × (1 − 298/373) = 0.10
Q_input_rate ≈ 2–3 kW (solar flux on chimney absorber area)
P_theoretical = 0.10 × 2,500 W = 250 W
```

Target operating range: 150–400W continuous electrical output during peak solar hours (6–8 hours/day).

**Note:** Commercial low-ΔT Stirling generators exist and have been demonstrated at these output levels with comparable temperature differentials. The novel aspect is integration with the passive ventilation chimney as the heat source. This integration requires prototype testing.

### 3.3 Thermal Efficiency Calculations

**Cooling System COP (Coefficient of Performance):**

The passive system delivers cooling without a compressor. The "COP" is defined differently from conventional refrigeration:

```
COP_passive = Q_cooling_delivered / W_mechanical_input
```

Since W_mechanical_input ≈ 0 (no compressor), the effective COP is theoretically infinite. However, the system has real costs: water consumption for evaporation, and fan power if supplemental airflow is needed.

**Water Consumption Estimate:**

At 0.1 m³/s airflow through evaporative media at 75% saturation efficiency in 40°C/20% RH ambient:

```
ΔW = 0.75 × (W_sat(40°C) − W_ambient)
W_sat(40°C) ≈ 0.0491 kg/kg_dry_air
W_ambient(40°C, 20% RH) ≈ 0.00934 kg/kg_dry_air
ΔW = 0.75 × (0.0491 − 0.00934) = 0.0298 kg water / kg dry air
Air mass flow = 0.1 m³/s × 1.1 kg/m³ = 0.11 kg/s
Water consumption = 0.11 × 0.0298 = 0.00328 kg/s = 11.8 kg/hour
```

Approximately 12 liters of water per hour during peak operation in arid conditions. This is a significant water requirement that must be met from rainwater harvesting, condensate recovery, or aquifer access. **This is a critical system constraint requiring site-specific analysis.**

### 3.4 AeroCement vs. Grid Infrastructure

**Comparative Analysis (Theoretical):**

| Parameter | Conventional House (Grid) | AeroCement Ecosystem (Proposed) |
|-----------|--------------------------|----------------------------------|
| Cooling energy | 2,000–5,000 kWh/year | ~0 (passive) |
| Heating energy | 3,000–8,000 kWh/year | ~200 kWh/year (supplemental) |
| Water use | 200–400 L/person/day | 50–100 L/person/day (target) |
| Construction materials | ~50 tons CO₂ embodied | ~5 tons CO₂ (fly ash based) |
| Infrastructure dependency | Grid, municipal water, gas | Self-contained |
| Build cost (materials) | $80–200/sq ft | Target: $8–25/sq ft |
| Lifetime | 30–50 years typical | Target: 100+ years (geopolymer) |

**Critical Note:** The AeroCement column represents design targets, not measured performance. All values require validation against instrumented prototype data.

**Economic Analysis:**

At $0.12/kWh grid electricity and 3,500 kWh/year cooling savings:
```
Annual savings = 3,500 × $0.12 = $420/year
10-year savings = $4,200
20-year savings = $8,400 (not inflation-adjusted)
```

Against a materials cost target of $10,000–15,000 for complete dome shell, simple payback on cooling alone: **12–18 years.** With food production value included (Section 5), payback shortens considerably.

---

## 4. Shelter System — AeroCement Shell

### 4.1 Material System

**AeroCement Defined:**

AeroCement is the working name for a lightweight geopolymer composite proposed as the primary structural and thermal material for dome construction. It is not a single patented material but a class of formulations sharing these characteristics:
- Fly ash or metakaolin as alumino-silicate precursor
- Alkaline activator (sodium hydroxide + sodium silicate solution)
- Lightweight aggregate (perlite, pumice, or recycled expanded glass)
- Fiber reinforcement (basalt fiber or recycled PET)

**Properties (Target — Require Laboratory Verification):**

| Property | AeroCement Target | OPC Concrete Reference |
|----------|-------------------|------------------------|
| Compressive strength | 15–25 MPa | 20–40 MPa |
| Density | 1,200–1,800 kg/m³ | 2,300 kg/m³ |
| Thermal conductivity | 0.3–0.6 W/m·K | 1.0–1.7 W/m·K |
| Embodied CO₂ | 0.1–0.2 kg CO₂/kg | 0.4–0.8 kg CO₂/kg |
| Water absorption | <5% | 5–15% |
| Fire resistance | Class A | Class A |

**Geopolymer Chemistry:**

The geopolymerization reaction:
```
Al-Si source + Alkaline solution → [SiO₄]⁴⁻ + [AlO₄]⁵⁻ monomers
                                          ↓
                              Polycondensation
                                          ↓
                         3D aluminosilicate polymer network
                         (zeolite-like amorphous structure)
```

Geopolymer chemistry is well-established in academic literature (Davidovits, 1991; Provis & van Deventer, 2009). The specific formulation targeting 0.3–0.6 W/m·K thermal conductivity with structural adequacy requires iterative mix design and testing.

**Ferrocement Substrate Option:**

For builders without access to geopolymer precursors, a ferrocement substrate (1:1.5 cement:sand with 2-layer chicken wire mesh) provides a proven low-cost alternative. Ferrocement domes have been built successfully since the 1960s (Nervi, Waterhouse). The AeroCement formulation is proposed as an improvement on ferrocement for thermal performance.

### 4.2 Geodesic Geometry

**Why Geodesic?**

The geodesic dome geometry is chosen for AeroCement construction based on:
1. **Structural efficiency:** Triangulated surface distributes loads through membrane action, minimizing bending moments
2. **Surface-to-volume ratio:** Minimizes material use and heat transfer surface relative to enclosed volume
3. **Self-supporting thin shell:** Enables the 50–75mm shell thickness target
4. **Wind resistance:** Curved form deflects wind loads efficiently

**Frequency Selection:**

A 3V geodesic subdivision is recommended for domes under 8m diameter. Higher frequency (4V, 5V) increases structural efficiency but adds construction complexity.

For a 6m diameter 3V geodesic dome:
- 80 triangular panels
- 3 strut lengths (a, b, c)
- 35 vertices

**Hub Connection Detail:**

Proposed hub design: cast AeroCement hub with embedded stainless steel connecting plates. Hub radius: 75mm. Strut-to-hub connection: stainless bolt through cast insert.

**Shell-to-Foundation Interface:**

Critical detail: geodesic domes generate outward horizontal thrust at the base ring. The base tension ring (welded steel or cast AeroCement ring beam) must resist this thrust. Design thrust for 6m dome under 1.5 kPa live load:

```
H_thrust ≈ q × r² / (2 × h) ≈ 1,500 × 9 / (2 × 3) = 2,250 N/m
```

Base ring must be designed for 2.25 kN/m hoop tension minimum.

### 4.3 Urban Applications

The AeroCement shell system is proposed for three urban deployment contexts:

**Urban Rooftop Modules:**  
6–9m dome units placed on existing flat-roof structures in dense urban areas. Each unit provides 28–64 m² of conditioned living space plus thermal mass benefit to the building below.

**Suburban Retrofit:**  
Dome shell placed over existing single-story structure, creating a "double-envelope" with passive thermal buffer zone. The buffer zone operates as the evaporative cooling intake and winter solar gain collector.

**Greenfield Village Clusters:**  
5–15 dome units arranged around shared thermal chimney and aquaponics core. Shared infrastructure reduces per-unit cost. Village layout follows permaculture zone design principles.

**Structural Note for Urban Use:**  
Roof load capacity of existing buildings must be verified by qualified structural engineer before rooftop installation. AeroCement dome shell weight estimate: 15,000–20,000 kg for 6m diameter. This is a significant point load requiring careful structural analysis.

---

## 5. Life Support Systems

### 5.1 Black Locust as Keystone Species

*Robinia pseudoacacia* is proposed as the primary ecosystem species for AeroCement settlements based on the following properties:

**Nitrogen Fixation:**  
Black locust is a nitrogen-fixing legume capable of fixing 40–100 kg N/ha/year via Rhizobium symbiosis. In a settlement context, this reduces or eliminates synthetic nitrogen fertilizer requirements.

**Structural Timber:**  
Black locust produces hardwood with:
- Density: 770 kg/m³
- Modulus of elasticity: 14–16 GPa
- Natural durability Class 1 (EN 350) — 80–100 year lifespan in ground contact without treatment
- Compressive strength: 60–70 MPa

This makes it suitable for framing, posts, foundation piles, and fuel.

**Fodder and Apiculture:**  
Black locust flowers produce abundant nectar (monofloral honey), and leaves are high-protein fodder (21–24% crude protein). Flowers are edible for humans.

**Rapid Growth:**  
Reaches harvestable diameter (12–15cm) in 8–12 years. Coppices vigorously, enabling 20–25 year coppice rotation cycles.

**Invasion Caution:**  
Black locust is aggressive and can outcompete native species in some bioregions. Site-specific ecological assessment is required before large-scale planting. Alternative nitrogen-fixing trees (honey locust, alder, acacia species) may be more appropriate in sensitive ecosystems.

**Proposed Planting Density:**  
50–200 trees per acre in alley cropping configuration with food crops in between rows. Annual yield after establishment: 5–10 cords wood + nitrogen fertility + fodder.

### 5.2 Quail Towers — Protein Integration

**Coturnix coturnix japonica** (Japanese quail) is proposed as the primary animal protein source based on:
- Feed conversion ratio: 2.5:1 (feed:egg by weight)
- Egg production: 250–300 eggs/year per hen
- Space requirement: 0.05–0.1 m² per bird (>50× more space-efficient than chickens)
- Maturation: 6–8 weeks to laying age
- Noise: minimal (important for urban applications)
- Disease resistance: robust

**Tower Design:**

Vertical stacking of quail cages along the south wall of the dome provides:
1. Passive heating from metabolic heat in winter (body heat ≈ 5W/bird × 100 birds = 500W)
2. CO₂ enrichment for attached greenhouse/aquaponics zone
3. High-nitrogen liquid waste for aquaponics fertilization
4. Protein production in minimal footprint

**50 m² tower can support 500–1,000 birds, producing:**
- 350–700 eggs/day
- 2–4 kg meat/week (culled males/excess females)
- 50–100 L nitrogen-rich liquid waste/day (aquaponics input)

**Validation Note:** These stocking densities are within industry norms. The integration of quail towers with dome thermal mass and aquaponics inputs represents the novel system architecture requiring integrated management protocols.

### 5.3 Aquaponics Integration

**System Proposed:**  
Coupled aquaponics combining:
- Tilapia (*Oreochromis niloticus*) as primary fish species — hardy, fast-growing, tolerant of high density
- Leafy greens and herbs in floating raft beds (NFT or DWC)
- Quail waste liquid as ammonia source supplementing fish waste

**Nitrogen Cycle:**
```
Quail Waste → NH₃ → Nitrosomonas bacteria → NO₂⁻ → Nitrobacter bacteria → NO₃⁻ → Plant uptake
Fish Waste   ↗                                                              ↗
```

**Target System Size for Family of 4:**
- Fish tank: 2,000–4,000 L
- Grow beds: 20–40 m²
- Fish stocking: 40–80 tilapia (harvest cycle: 6–9 months)
- Yield: 15–25 kg fish/month + 200–400g leafy greens/day

**Energy Input:**  
Aquaponics requires water pump energy. Target: gravity-fed or air-lift pump driven by Stirling engine output. Estimated pump power: 50–150W.

**Water Efficiency:**  
Aquaponics uses 90–95% less water than soil agriculture for equivalent yield (Somerville et al., FAO 2014).

### 5.4 Seed Banking

**Principle:**  
Seed sovereignty — the ability to reproduce the entire food system from open-pollinated seed — is a core design requirement. The system does not rely on hybrid or patented seed stock.

**Proposed Seed Vault Integration:**

An underground seed vault at 1.5m depth (using ground temperature stability) stores:
- All vegetable and grain varieties grown on-site
- Cover crop and green manure seed
- Medicinal herb seed
- Emergency food reserves (dried grain)

**Storage Conditions (Target):**
- Temperature: 8–12°C (using ground coupling)
- Humidity: <40% RH (sealed mylar packets with desiccant)
- Viability targets: >80% germination at 5 years for most species

**Recommended Species List:**  
Open-pollinated varieties of: tomato, pepper, squash, bean, corn, sunflower, kale, brassicas, root vegetables, culinary herbs. Emphasis on heat-tolerant, drought-resistant landrace varieties.

---

## 6. Build Protocols and Hard Constraints

### 6.1 Non-Negotiable Design Constraints

The following constraints are defined as hard limits — system configurations violating these constraints are not considered compliant with the AeroCement Ecosystem protocol:

**Structural:**
1. Minimum shell thickness: 50mm for spans <6m; 75mm for 6–9m spans
2. Base ring must be continuous and closed (no gaps in tension ring)
3. All penetrations (windows, doors, chimney) must be framed with continuity of tension ring
4. Hub connections must include positive mechanical lock (bolt or wedge; adhesive-only is prohibited)
5. Foundation must bear on undisturbed soil or engineered fill; no bearing on made ground without geotechnical assessment

**Thermal:**
6. Chimney cross-section must be ≥0.15 m² for dome diameter 4–6m
7. Evaporative media depth: minimum 100mm at design airflow velocity
8. Thermal mass minimum: 200 kg/m² of floor area
9. All windows must be double-glazed or double-film; single-pane prohibited in climate zones with >40°C ambient

**Water:**
10. All water systems must have overflow and drainage directed away from foundation
11. Aquaponics must have emergency bypass to prevent fish loss during power or pump failure
12. Potable water storage minimum: 200L/person emergency reserve

**Biological:**
13. No pesticide application within 10m of aquaponics or seed bank
14. Composting toilet or equivalent waste system required; no flush connection to aquaponics without triple-stage treatment

### 6.2 Recommended Build Sequence

See Appendix C for detailed build sequence. Summary:

**Phase 1 — Site and Foundation (Weeks 1–4)**
- Site survey and soil assessment
- Foundation footprint laid out
- Earthwork for berm, intake tunnel, underground cisterns
- Tension ring cast or welded

**Phase 2 — Shell Construction (Weeks 5–12)**
- Geodesic frame erected (if using form-and-spray method, skip to Phase 2b)
- Mesh applied to frame
- First AeroCement coat applied (15–20mm)
- Cure 7 days minimum before additional coats
- Final coat + waterproofing membrane
- Chimney integration

**Phase 3 — Systems Integration (Weeks 13–20)**
- Evaporative cooling tower
- Stirling engine mounting and commissioning
- Electrical distribution (12V/24V DC primary)
- Aquaponics tank installation and cycling
- Quail tower framing

**Phase 4 — Biological Establishment (Months 6–18)**
- Black locust planting
- Aquaponics stocking (plants first, fish after biological cycle stabilizes)
- Seed bank population

---

## 7. Token Economy — Proof of Physical Work

### 7.1 Proof of Physical Work Protocol

**Problem Statement:**

Existing cryptocurrency proof-of-work systems consume energy producing no useful physical output. Proof-of-stake systems concentrate governance in proportion to existing wealth. Neither mechanism rewards physical contribution to real-world infrastructure.

**Proposed Solution:**

The Proof of Physical Work (PoPW) protocol anchors token issuance to verifiable physical labor and material deployment on AeroCement Ecosystem infrastructure.

**Core Mechanism:**

```
Token Issuance = f(Verified_Physical_Work, Thermodynamic_Output, Peer_Attestation)
```

Where:
- **Verified_Physical_Work** = GPS-verified labor hours + photographic documentation at each build phase
- **Thermodynamic_Output** = measured data from instrumented dome (temperature differential, Stirling output, food production)
- **Peer_Attestation** = multi-signature confirmation from existing node operators that build meets specifications

### 7.2 Token Mechanics

**Token Structure:**

| Token Class | Issuance Trigger | Supply Cap |
|-------------|-----------------|------------|
| BUILD | Per completed dome shell milestone | 1,000 per dome |
| THERM | Per kWh equivalent passive cooling verified | Unlimited (backed by energy) |
| HARVEST | Per kg food produced, certified | Unlimited (backed by food) |
| SEED | Per variety deposited to verified seed bank | 100 per variety |

**BUILD Token Issuance Schedule:**

| Milestone | BUILD Tokens |
|-----------|-------------|
| Foundation + Tension Ring complete | 100 |
| Shell complete, first coat | 200 |
| Shell complete, weathertight | 300 |
| Systems commissioned (water, thermal) | 200 |
| First harvest (food system operational) | 200 |
| **Total per dome** | **1,000** |

### 7.3 DAO Governance

**Structure:**

The AeroCement DAO is proposed as a multi-tiered governance system:

**Technical Council (TC):**
- 7 members elected by BUILD token holders
- Responsible for: protocol specification updates, build standard amendments, dispute resolution
- Term: 2 years, staggered
- Quorum: 5/7 for standard decisions, 7/7 for protocol hard forks

**Build Validators (BV):**
- Elected by regional token holders
- Conduct on-site verification for BUILD token issuance
- Bonded (stake required to prevent fraudulent attestation)
- One BV per 50 domes in region

**Token Holder Assembly (THA):**
- All token holders
- Vote on: DAO treasury allocation, TC elections, ecosystem fund deployments
- Minimum holding to vote: 10 BUILD or equivalent

**Treasury:**

10% of all BUILD token issuance goes to DAO treasury. Treasury funds:
- Protocol development (open-source)
- Build validator training
- Seed bank maintenance
- Emergency resilience reserves

### 7.4 Bounty System

**Proposed Bounty Categories:**

**Research Bounties** (THERM tokens):
- "Validate stack effect at 4m chimney height, 35°C ambient, 6m dome" — 5,000 THERM
- "Characterize AeroCement mix (fly ash 60%/metakaolin 40%) thermal conductivity" — 3,000 THERM
- "Quail tower waste nitrogen yield per 100 birds at 90-day measurement" — 2,000 THERM

**Build Bounties** (BUILD tokens):
- "First dome in sub-Saharan Africa" — 500 BUILD bonus
- "First dome serving >10 people as primary residence for >1 year" — 1,000 BUILD bonus
- "First fully solar-powered build documentation" — 500 BUILD bonus

**Open Source Bounties** (SEED tokens):
- "Port thermodynamic_ledger.py to embedded microcontroller" — 500 SEED
- "Develop automated dome geometry calculator (web app)" — 300 SEED
- "Translate complete thesis to [language]" — 200 SEED per language

---

## 8. Defensive Publication and Open-Source Strategy

### 8.1 Purpose of Defensive Publication

This thesis constitutes a defensive publication — a formal public disclosure of intellectual property for the purpose of establishing prior art. By making the complete design, calculations, and specifications publicly available before any patent filing, this publication:

1. **Prevents patent enclosure** of the AeroCement Ecosystem concepts by any party
2. **Establishes prior art** that invalidates any subsequent patent claims on the disclosed concepts
3. **Places the technology in the public domain** permanently under the disclosed license

**Legal Note:** Defensive publication is an established strategy used by major technology companies (IBM Technical Disclosure Bulletins, Google defensive patents) and academic institutions. The public availability of this document creates a prior art record that patent examiners must consider.

### 8.2 License Strategy

**Hardware (Physical Designs, Specifications, Drawings):**  
Creative Commons Attribution-ShareAlike 4.0 International (CC-BY-SA 4.0)

This means:
- ✅ Free to use, modify, and distribute
- ✅ Commercial use permitted
- ✅ Must credit original authors
- ✅ Derivative works must use same license (ShareAlike clause prevents proprietary enclosure)

**Software (Code, Algorithms, Smart Contracts):**  
GNU General Public License v3 (GPL v3)

This means:
- ✅ Free to use, modify, and distribute
- ✅ Commercial use permitted
- ✅ Source code must be provided with distributions
- ✅ Derivative software must also be GPL v3

**Documentation (Thesis, Technical Manuals):**  
CC-BY-SA 4.0

**Seed Varieties:**  
Open-pollinated varieties are in the public domain. No proprietary seed varieties are specified or endorsed.

### 8.3 What This Publication Covers

This defensive publication covers the following novel combinations and integrations (individual components are prior art):

1. The integrated use of a passive stack-effect chimney as both ventilation driver and Stirling engine heat source within a geodesic geopolymer dome
2. The specific integration of quail tower metabolic heat with dome heating load offset and aquaponics nitrogen cycling
3. The BUILD/THERM/HARVEST/SEED token structure tied to instrumented physical measurements
4. The combined use of fly ash geopolymer with lightweight aggregate targeting <0.5 W/m·K in a load-bearing dome shell
5. The underground seed vault integrated with ground-coupled temperature stabilization within the dome thermal system

---

## 9. Conclusion

The AeroCement Ecosystem represents a theoretical framework for integrating passive thermodynamic principles, bio-based structural systems, closed-loop food production, and cryptographic coordination into a self-sufficient human habitat.

**What has been established here:**

1. The thermodynamic principles underlying each subsystem are well-established and individually validated in existing literature and practice
2. The proposed integration creates a logical thermodynamic circuit with no fundamental physical impossibilities
3. The material science for geopolymer construction is established; the specific AeroCement formulation is a detailed mix design proposal requiring laboratory optimization
4. The economic and ecological calculations suggest viability if performance targets are met

**What remains to be proven:**

1. The integrated system performance at full scale under real operating conditions
2. The specific AeroCement mix achieving target mechanical and thermal properties simultaneously
3. The water balance of the evaporative system across seasons and climates
4. Long-term durability of the geopolymer shell in varied exposure conditions
5. The social and governance dynamics of the DAO/PoPW token system

**Call to Action:**

This document is a starting point. The most valuable contribution any reader can make is to **build a prototype, measure it, and publish the data.** The bounty system (Section 7.4) is designed to reward exactly this. The open-source license ensures that whatever you build and learn belongs to everyone.

The physics works. The question is execution.

---

## Appendix A: Thermodynamic Ledger

The complete Python implementation of the thermodynamic ledger is maintained at:  
`/code/python/thermodynamic_ledger.py`

```python
#!/usr/bin/env python3
"""
AeroCement Ecosystem — Thermodynamic Ledger
==========================================
Calculates and records thermal flows, Stirling engine output,
evaporative cooling performance, and stack effect airflow.

License: GPL v3
"""

import math
import json
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


# ── Physical Constants ──────────────────────────────────────────────────────
G = 9.81          # gravitational acceleration (m/s²)
R_AIR = 287.05    # specific gas constant for dry air (J/kg·K)
CP_AIR = 1005.0   # specific heat of air at constant pressure (J/kg·K)
RHO_WATER = 1000.0  # density of water (kg/m³)
L_WATER = 2430000.0  # latent heat of vaporization at 25°C (J/kg)


@dataclass
class SiteConditions:
    """Ambient site conditions for a given calculation period."""
    timestamp: str
    ambient_temp_c: float       # dry-bulb temperature (°C)
    relative_humidity: float    # fractional (0.0–1.0)
    solar_irradiance_wm2: float # W/m²
    wind_speed_ms: float        # m/s


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
    """Calculate moist air density (kg/m³)."""
    temp_k = temp_c + 273.15
    # Saturation vapor pressure (Magnus formula)
    p_sat = 610.78 * math.exp(17.27 * temp_c / (temp_c + 237.3))
    p_vapor = rh * p_sat
    p_dry = pressure_pa - p_vapor
    # Moist air density
    rho = (p_dry / (R_AIR * temp_k)) + (p_vapor / (461.5 * temp_k))
    return rho


def wet_bulb_temperature(temp_c: float, rh: float) -> float:
    """
    Estimate wet-bulb temperature using Stull (2011) approximation.
    Valid for: -20°C < T < 50°C, 5% < RH < 99%.
    """
    rh_pct = rh * 100.0
    tw = (temp_c * math.atan(0.151977 * math.sqrt(rh_pct + 8.313659))
          + math.atan(temp_c + rh_pct)
          - math.atan(rh_pct - 1.676331)
          + 0.00391838 * rh_pct ** 1.5 * math.atan(0.023101 * rh_pct)
          - 4.686035)
    return tw


def saturation_humidity_ratio(temp_c: float, pressure_pa: float = 101325.0) -> float:
    """Calculate saturation humidity ratio (kg water / kg dry air)."""
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
    """
    C = 0.65  # discharge coefficient
    rho_out = air_density(outdoor_temp_c, outdoor_rh)
    rho_in = air_density(chimney_temp_c, 0.0)
    delta_p = C * chimney_height_m * G * (rho_out - rho_in)
    return max(delta_p, 0.0)  # cannot be negative (no reverse stack)


def airflow_from_pressure(
    pressure_pa: float,
    area_m2: float,
    cd: float = 0.65
) -> float:
    """
    Calculate volumetric airflow (m³/s) from pressure differential.
    Uses orifice equation: Q = Cd × A × sqrt(2 × ΔP / ρ)
    """
    rho = 1.2  # approximate air density
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
    Calculate the complete thermal state of the AeroCement dome.

    Parameters
    ----------
    site : SiteConditions
        Current ambient conditions.
    dome : DomeGeometry
        Physical dome parameters.
    chimney_solar_absorptance : float
        Solar absorptance of chimney surface (0–1).
    stirling_fraction_of_carnot : float
        Stirling engine performance as fraction of Carnot efficiency.

    Returns
    -------
    ThermalState
        Calculated thermal state.
    """
    # ── 1. Chimney temperature ──────────────────────────────────────────────
    # Solar gain on chimney wall raises air temperature
    chimney_perimeter = math.sqrt(dome.chimney_area_m2) * 4  # approximate
    chimney_wall_area = chimney_perimeter * dome.chimney_height_m
    solar_gain_w = site.solar_irradiance_wm2 * chimney_solar_absorptance * chimney_wall_area
    # Approximate chimney air temperature rise from solar gain
    mass_flow_approx = 0.1  # kg/s initial estimate
    delta_t_chimney = solar_gain_w / (mass_flow_approx * CP_AIR + 1e-6)
    chimney_temp_c = site.ambient_temp_c + min(delta_t_chimney, 50.0)  # cap at +50°C

    # ── 2. Stack effect ─────────────────────────────────────────────────────
    stack_p = stack_effect_pressure(
        dome.chimney_height_m,
        site.ambient_temp_c,
        chimney_temp_c,
        site.relative_humidity
    )
    airflow_m3s = airflow_from_pressure(stack_p, dome.chimney_area_m2)
    dome_volume = (2.0 / 3.0) * math.pi * (dome.diameter_m / 2) ** 3  # hemisphere
    ach = (airflow_m3s * 3600) / dome_volume

    # ── 3. Evaporative cooling ──────────────────────────────────────────────
    t_wb = wet_bulb_temperature(site.ambient_temp_c, site.relative_humidity)
    t_supply = site.ambient_temp_c - (
        dome.evap_saturation_eff * (site.ambient_temp_c - t_wb)
    )
    air_mass_flow = airflow_m3s * air_density(site.ambient_temp_c, site.relative_humidity)
    cooling_power = air_mass_flow * CP_AIR * max(site.ambient_temp_c - t_supply, 0.0)

    # Water consumption
    w_sat = saturation_humidity_ratio(site.ambient_temp_c)
    w_in = saturation_humidity_ratio(site.ambient_temp_c) * site.relative_humidity
    delta_w = dome.evap_saturation_eff * (w_sat - w_in)
    water_kg_s = air_mass_flow * delta_w
    water_kg_h = water_kg_s * 3600

    # ── 4. Stirling engine ──────────────────────────────────────────────────
    t_hot_k = (chimney_temp_c + 273.15)
    t_cold_k = (t_supply + 273.15)
    if t_hot_k > t_cold_k:
        carnot_eff = 1.0 - (t_cold_k / t_hot_k)
    else:
        carnot_eff = 0.0
    stirling_eff = stirling_fraction_of_carnot * carnot_eff
    # Stirling engine input = solar gain on chimney
    stirling_power = stirling_eff * solar_gain_w

    # ── 5. Thermal mass ─────────────────────────────────────────────────────
    shell_surface = 2 * math.pi * (dome.diameter_m / 2) ** 2  # hemisphere
    shell_volume = shell_surface * dome.shell_thickness_m
    shell_mass = shell_volume * dome.shell_density_kgm3
    # Daily thermal swing (assume 10°C)
    delta_t_mass = 10.0
    heat_stored_kj = shell_mass * dome.shell_cp_jkgk * delta_t_mass / 1000.0

    # ── 6. Interior temperature estimate ───────────────────────────────────
    # Simplified: supply air temperature modified by thermal mass buffer
    interior_temp = t_supply + 2.0  # +2°C for internal gains and mixing

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
) -> list[ThermalState]:
    """
    Simulate a design-day thermal performance profile.

    Models temperature, humidity, and irradiance variation over 24 hours
    using simplified sinusoidal profiles.
    """
    results = []
    for hour in range(hours):
        # Sinusoidal profiles: peak at hour 14 for temperature, hour 12 for solar
        temp_c = peak_temp_c - 8.0 + 8.0 * math.sin(math.pi * (hour - 6) / 12)
        rh = peak_rh + (0.35 - peak_rh) * (1 - math.sin(math.pi * (hour - 6) / 12))
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


def print_summary(states: list[ThermalState]) -> None:
    """Print a summary table of thermal state results."""
    print(f"\n{'Hour':>4} {'T_amb':>6} {'T_supp':>7} {'T_int':>6} {'ACH':>5} "
          f"{'Cool_W':>7} {'Stirl_W':>8} {'H2O_L/h':>8}")
    print("-" * 65)
    for i, s in enumerate(states):
        # Recover ambient from supply (approximate)
        print(f"{i:>4} {s.supply_air_temp_c + 8:>6.1f} {s.supply_air_temp_c:>7.1f} "
              f"{s.interior_temp_estimate_c:>6.1f} {s.air_changes_per_hour:>5.1f} "
              f"{s.cooling_power_w:>7.0f} {s.stirling_power_w:>8.0f} "
              f"{s.water_consumption_kgh:>8.2f}")


def export_json(states: list[ThermalState], filename: str) -> None:
    """Export thermal state results to JSON."""
    data = [asdict(s) for s in states]
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Exported {len(states)} records to {filename}")


# ── Default dome configuration ──────────────────────────────────────────────
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
    print(f"  Diameter:       {DEFAULT_DOME.diameter_m} m")
    print(f"  Chimney height: {DEFAULT_DOME.chimney_height_m} m")
    print(f"  Chimney area:   {DEFAULT_DOME.chimney_area_m2} m²")
    print(f"  Shell:          {DEFAULT_DOME.shell_thickness_m*1000:.0f} mm "
          f"@ {DEFAULT_DOME.shell_k_wm2k} W/m·K")
    print(f"  Evap efficiency:{DEFAULT_DOME.evap_saturation_eff*100:.0f}%")

    states = run_design_day(DEFAULT_DOME)
    print_summary(states)

    # Peak performance stats
    peak_cool = max(s.cooling_power_w for s in states)
    peak_stirl = max(s.stirling_power_w for s in states)
    peak_h2o = max(s.water_consumption_kgh for s in states)
    avg_int = sum(s.interior_temp_estimate_c for s in states) / len(states)

    print(f"\n── Peak Performance ─────────────────────────────")
    print(f"Peak cooling power:    {peak_cool:.0f} W")
    print(f"Peak Stirling output:  {peak_stirl:.0f} W")
    print(f"Peak water use:        {peak_h2o:.2f} L/h")
    print(f"Average interior temp: {avg_int:.1f}°C")
    print(f"\n⚠  These are THEORETICAL calculations requiring prototype validation.")
```

---

## Appendix B: Material Specifications

### AeroCement Mix Design Proposals

**Mix A: High-Fly-Ash Structural**

| Component | Mass Fraction | Notes |
|-----------|--------------|-------|
| Class F Fly Ash | 60% | Low-calcium preferred |
| Metakaolin | 10% | Reactive Al-Si source |
| Perlite (expanded) | 25% | Lightweight aggregate |
| Basalt Fiber | 3% | 12mm chopped |
| Polypropylene Fiber | 2% | 6mm chopped, fire resistance |

**Activator Solution (Mix A):**
- Sodium Hydroxide: 10M solution
- Sodium Silicate (waterglass): Na₂SiO₃, modulus 2.0–2.5
- NaOH:Na₂SiO₃ mass ratio: 1:2.5
- Solution:Binder mass ratio: 0.35–0.40

**Target Properties (Lab Verification Required):**
- 28-day compressive strength: ≥15 MPa
- Density: 1,400–1,600 kg/m³
- Thermal conductivity: 0.35–0.50 W/m·K

**Mix B: Ferrocement Fallback**

For sites where fly ash is unavailable:
- Portland cement: 1 part
- Sharp sand: 1.5 parts
- Water:cement ratio: 0.38–0.42
- Admixture: latex polymer modifier (5% by cement weight)
- Reinforcement: 2-layer galvanized welded mesh, 12.5mm × 12.5mm × 1.2mm wire

**Target Properties:**
- 28-day compressive strength: ≥25 MPa
- Density: ~2,100 kg/m³
- Thermal conductivity: ~1.0 W/m·K (significantly worse than Mix A)

**Note:** Mix B provides structural equivalence but loses the thermal advantage. External insulation layer required if using Mix B in hot climates.

### Evaporative Media Specifications

| Property | Target | Acceptable Range |
|----------|--------|-----------------|
| Surface area per unit volume | >500 m²/m³ | 300–800 m²/m³ |
| Pressure drop at 0.5 m/s | <30 Pa/m | <50 Pa/m |
| Water retention | >5 L/m³ | 3–10 L/m³ |
| Material | Cellulose pad or rigid plastic media | |
| Depth | 150mm | 100–200mm |
| Maintenance interval | 6 months | Climate dependent |

---

## Appendix C: Build Sequence

### Complete Phase-by-Phase Build Protocol

**Pre-Construction:**
- [ ] Site analysis: solar access, wind, soil bearing capacity, water table
- [ ] Climate data collection: peak summer temperature, wet bulb, humidity, solar irradiance
- [ ] Local material sourcing: fly ash availability, activator chemicals, mesh
- [ ] Local authority consultation: planning, building permits
- [ ] Foundation design: verify bearing capacity ≥50 kPa minimum

**Phase 1: Foundation and Ground Works (Weeks 1–4)**
- [ ] Mark out dome footprint (circle + berm access tunnel)
- [ ] Excavate for foundation ring beam (300mm wide × 400mm deep)
- [ ] Excavate underground cisterns (2–4m³ each, below frost line)
- [ ] Excavate earthen intake tunnel (600mm × 600mm minimum cross-section, 5–8m long)
- [ ] Place and compact engineered fill if needed
- [ ] Cast foundation ring beam with embedded anchor bolts (M16 minimum) at 600mm centers
- [ ] Install base tension ring (50mm × 6mm continuous steel flat bar, or 100mm cast AeroCement ring beam)
- [ ] Waterproof underground cisterns (crystalline waterproofing compound)
- [ ] Install cistern overflow and drainage
- [ ] Backfill and compact berm

**Phase 2: Dome Shell (Weeks 5–12)**

*Option A: Hub-and-Strut with Shotcrete/Spray*
- [ ] Erect geodesic strut framework (timber or steel)
- [ ] Apply primary mesh layer (chicken wire or welded mesh)
- [ ] Apply secondary mesh layer, overlapping 100mm
- [ ] First AeroCement coat: 15–20mm by hand or spray
- [ ] Cure under wet burlap for minimum 7 days (do not allow to dry rapidly)
- [ ] Second coat: 20–25mm
- [ ] Cure 7 days
- [ ] Final finish coat: 10–15mm
- [ ] Apply waterproofing membrane (bituminous or cementitious)
- [ ] Apply reflective or high-emissivity coating appropriate to climate

*Option B: Earthbag Form*
- [ ] Stack earthbags in dome form (temporary formwork)
- [ ] Apply mesh over earthbag form
- [ ] Spray/apply AeroCement over mesh
- [ ] Cure as above
- [ ] Remove earthbags after 14 days (use as berming or insulation)

**Phase 3: Penetrations and Fittings (Weeks 9–14)**
- [ ] Cut and frame door opening with continuous lintel and side jambs
- [ ] Install window frames with thermal break
- [ ] Fabricate and install chimney tube (steel or AeroCement with steel liner)
- [ ] Fabricate and install evaporative media housing at intake
- [ ] Install Stirling engine mounting brackets (vibration isolated)
- [ ] Install all electrical conduit before any internal finishing

**Phase 4: Systems Commissioning (Weeks 13–20)**
- [ ] Install evaporative cooling media and water distribution header
- [ ] Commission water supply and drainage for evaporative section
- [ ] Mount Stirling engine; pressure-test working gas circuit
- [ ] Wire Stirling generator to charge controller and battery bank
- [ ] Install 12V/24V DC distribution panel
- [ ] Flush and fill aquaponics system; establish biological nitrogen cycle (4–6 weeks minimum before stocking fish)
- [ ] Install quail tower frame and hardware cloth
- [ ] Commission water distribution to quail tower

**Phase 5: Biological Establishment (Months 5–18)**
- [ ] Plant black locust in alley-cropping pattern
- [ ] Establish cover crops between alleys
- [ ] Stock aquaponics with plants after nitrogen cycle confirmed
- [ ] Stock aquaponics with fish after plant establishment
- [ ] Introduce quail after quail tower commissioning complete
- [ ] Populate seed bank from first harvest
- [ ] Document all yields for HARVEST token issuance

**Instrumentation Requirements (for Token Validation):**
- [ ] Install interior/exterior thermocouple pair (log at 15-minute intervals minimum)
- [ ] Install chimney air temperature sensor
- [ ] Install supply air temperature/humidity sensor
- [ ] Install Stirling output power meter
- [ ] Install water consumption meter on evaporative system
- [ ] Install aquaponics water quality sensors (pH, EC, temperature)
- [ ] Establish photographic documentation protocol: 1 photo per week minimum, GPS-tagged

---

*End of THESIS.md*

**Repository:** https://github.com/jesseray718/openroot-thesis  
**License:** CC-BY-SA 4.0 (Hardware/Documentation) | GPL v3 (Software)  
**Version:** 3.0 | Published for Defensive Prior Art
