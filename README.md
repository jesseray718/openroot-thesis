# AeroCement Ecosystem: Civilization 2.0

> ⚠️ **THEORETICAL ARCHITECTURE — VALIDATION REQUIRED**  
> Individual components (stack effect, evaporative cooling, Stirling cycle, geopolymer) are proven. The **complete integrated system at scale has NOT been built or instrumented.** All performance claims require prototype validation. See [THESIS.md](THESIS.md) for full disclaimer.

A comprehensive open-source framework for passive solar-thermal human habitation integrating thermodynamic shelter, biointensive food production, and a proof-of-physical-work token economy.

**License:** CC-BY-SA 4.0 (Hardware/Documentation) | GPL v3 (Software)

---

## What is the AeroCement Ecosystem?

The AeroCement Ecosystem proposes integrating four well-understood systems into a single self-sufficient habitat:

| Pillar | What It Does |
|--------|-------------|
| ⚡ [Energy](docs/01_ENERGY/README.md) | Passive solar-thermal loop (stack effect + evaporative cooling + Stirling engine) eliminates grid dependency |
| 🏗️ [Shelter](docs/02_SHELTER/README.md) | Lightweight fly-ash geopolymer geodesic dome with integrated thermal mass |
| 🌱 [Life](docs/03_LIFE/README.md) | Black locust silviculture + quail protein towers + aquaponics + seed banking |
| 💰 [Economy](docs/04_ECONOMY/README.md) | Proof-of-Physical-Work token protocol anchored to verified infrastructure |

---

## Full Thesis

📄 **[THESIS.md](THESIS.md)** — Complete thesis with all thermodynamic calculations, material specifications, build protocols, and governance design.

---

## Documentation Structure

```
docs/
├── 01_ENERGY/           ← Solar thermal loop, Stirling engine, thermodynamic analysis
├── 02_SHELTER/          ← AeroCement material, geodesic geometry, urban applications
├── 03_LIFE/             ← Black locust, quail towers, aquaponics, seed banking
├── 04_ECONOMY/          ← Proof-of-Physical-Work, DAO governance, bounty system
├── 05_BUILD_PROTOCOLS/  ← Hard constraints, complete build sequence
└── 06_GOVERNANCE/       ← Defensive publication, open-source licensing strategy
```

### ⚡ Energy — [docs/01_ENERGY/](docs/01_ENERGY/README.md)
- [Solar Thermal Loop](docs/01_ENERGY/01_SOLAR_THERMAL_LOOP.md) — Stack effect, evaporative cooling, thermal mass integration
- [Thermodynamic Analysis](docs/01_ENERGY/02_THERMODYNAMIC_ANALYSIS.md) — First and second law analysis, efficiency calculations
- [Stirling Engine](docs/01_ENERGY/03_STIRLING_ENGINE.md) — Integration with passive chimney heat source
- [AeroCement vs. Grid](docs/01_ENERGY/04_VS_GRID_INFRASTRUCTURE.md) — Comparative performance and economic analysis

### 🏗️ Shelter — [docs/02_SHELTER/](docs/02_SHELTER/README.md)
- [Material System](docs/02_SHELTER/01_MATERIAL_SYSTEM.md) — Geopolymer chemistry, mix design, properties
- [Geodesic Geometry](docs/02_SHELTER/02_GEODESIC_GEOMETRY.md) — Structural analysis, hub design, frequency selection
- [Urban Applications](docs/02_SHELTER/03_URBAN_APPLICATIONS.md) — Rooftop, retrofit, and village configurations
- [Material Specifications](docs/02_SHELTER/MATERIAL_SPECIFICATIONS.md) — Mix designs, evaporative media specs

### 🌱 Life — [docs/03_LIFE/](docs/03_LIFE/README.md)
- [Black Locust](docs/03_LIFE/01_BLACK_LOCUST_KEYSTONE.md) — Nitrogen fixation, timber, fodder, coppice management
- [Quail Towers](docs/03_LIFE/02_QUAIL_TOWERS.md) — Protein integration, metabolic heat, waste cycling
- [Aquaponics](docs/03_LIFE/03_AQUAPONICS.md) — Tilapia + leafy greens + nitrogen cycle
- [Seed Banking](docs/03_LIFE/04_SEED_BANKING.md) — Seed sovereignty, storage protocols

### 💰 Economy — [docs/04_ECONOMY/](docs/04_ECONOMY/README.md)
- [Proof of Physical Work](docs/04_ECONOMY/01_PROOF_OF_PHYSICAL_WORK.md) — Protocol design and token mechanics
- [DAO Governance](docs/04_ECONOMY/02_DAO_GOVERNANCE.md) — Technical council, validators, token assembly
- [Bounty System](docs/04_ECONOMY/03_BOUNTY_SYSTEM.md) — Research, build, and open-source bounties

### 🔧 Build Protocols — [docs/05_BUILD_PROTOCOLS/](docs/05_BUILD_PROTOCOLS/README.md)
- [Hard Constraints](docs/05_BUILD_PROTOCOLS/01_HARD_CONSTRAINTS.md) — Non-negotiable design limits
- [Build Sequence](docs/05_BUILD_PROTOCOLS/02_BUILD_SEQUENCE.md) — Phase-by-phase construction protocol

### ⚖️ Governance — [docs/06_GOVERNANCE/](docs/06_GOVERNANCE/README.md)
- [Defensive Publication](docs/06_GOVERNANCE/DEFENSIVE_PUBLICATION.md) — Prior art strategy
- [Licensing Strategy](docs/06_GOVERNANCE/LICENSING_STRATEGY.md) — CC-BY-SA 4.0 + GPL v3

---

## Code

```
code/
└── python/
    └── thermodynamic_ledger.py   ← Thermal simulation: stack effect, evap cooling, Stirling
```

Run the design-day simulation:
```bash
python3 code/python/thermodynamic_ledger.py
```

---

## How to Contribute

1. **Build and measure** — The most valuable contribution is prototype construction with instrumented data. Use the build protocols in [docs/05_BUILD_PROTOCOLS/](docs/05_BUILD_PROTOCOLS/README.md).
2. **Validate calculations** — Run `thermodynamic_ledger.py` against real data; open a PR with comparison.
3. **Translate** — See translation bounties in [docs/04_ECONOMY/03_BOUNTY_SYSTEM.md](docs/04_ECONOMY/03_BOUNTY_SYSTEM.md).
4. **Open issues** — Use GitHub Issues for technical questions, corrections, and regional adaptation needs.
5. **Fork freely** — CC-BY-SA 4.0 means you can adapt this for your climate, geography, or community as long as you share back under the same license.

---

## License

| Component | License |
|-----------|---------|
| Hardware designs, specifications, drawings | [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) |
| Software, algorithms, code | [GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html) |
| Documentation, thesis | [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) |

This repository constitutes a **defensive publication** establishing prior art. No component of this design may be patented by any party. See [docs/06_GOVERNANCE/DEFENSIVE_PUBLICATION.md](docs/06_GOVERNANCE/DEFENSIVE_PUBLICATION.md).

---

## Quickstart

New here? → **[QUICKSTART.md](QUICKSTART.md)**
