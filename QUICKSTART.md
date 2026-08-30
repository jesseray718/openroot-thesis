# Quickstart — AeroCement Ecosystem

Welcome. This is your entry point.

> ⚠️ Everything here is a **theoretical design framework** grounded in established physics. The complete integrated system has not been built at scale. Build small, measure everything, share your data.

---

## Step 1: Understand the Full Vision

Read **[THESIS.md](THESIS.md)** — this is the complete technical document. It contains:
- All thermodynamic calculations
- Material specifications
- Build protocols
- Token economy design
- Governance strategy

Expected reading time: 45–90 minutes for full depth.

---

## Step 2: Explore by Pillar

After reading the thesis, go deeper on your area of interest:

### If you want to understand the energy system:
→ **[docs/01_ENERGY/README.md](docs/01_ENERGY/README.md)**  
Start with the solar thermal loop, then read the Stirling engine integration.

### If you want to build a shelter:
→ **[docs/02_SHELTER/README.md](docs/02_SHELTER/README.md)**  
Start with the material system, then geodesic geometry, then the build sequence.

### If you want to grow food:
→ **[docs/03_LIFE/README.md](docs/03_LIFE/README.md)**  
Start with black locust (your soil foundation), then aquaponics and quail towers.

### If you want to understand the token economy:
→ **[docs/04_ECONOMY/README.md](docs/04_ECONOMY/README.md)**  
Start with Proof of Physical Work, then DAO governance.

### If you're ready to build:
→ **[docs/05_BUILD_PROTOCOLS/README.md](docs/05_BUILD_PROTOCOLS/README.md)**  
Read hard constraints first — these are non-negotiable. Then follow the build sequence.

---

## Step 3: Run the Calculations

```bash
git clone https://github.com/jesseray718/openroot-thesis.git
cd openroot-thesis
python3 code/python/thermodynamic_ledger.py
```

This runs a 24-hour design-day simulation for a 6m dome in 40°C / 20% RH conditions.  
Outputs: cooling power, Stirling electrical output, water consumption, interior temperature estimate.

Modify `DEFAULT_DOME` in the script to model your specific geometry.

---

## Step 4: Contribute

The most valuable thing you can do is **build a prototype and measure it.**

- Open a GitHub Issue with your site conditions, build plan, or questions
- Fork this repo and submit a PR with measured data vs. calculated predictions
- Earn THERM tokens when the DAO launches by contributing validated measurements (see [bounty system](docs/04_ECONOMY/03_BOUNTY_SYSTEM.md))

---

## Step 5: Understand the License

Everything here is **open source by design:**
- Hardware designs: CC-BY-SA 4.0 (use freely, share alike)
- Code: GPL v3 (use freely, keep open)
- This is a defensive publication — nobody can patent these ideas

See [docs/06_GOVERNANCE/LICENSING_STRATEGY.md](docs/06_GOVERNANCE/LICENSING_STRATEGY.md) for details.

---

## Where to Ask Questions

→ [GitHub Issues](https://github.com/jesseray718/openroot-thesis/issues) — technical questions, corrections, regional adaptations

---

*The physics works. The question is execution. Start small, measure everything, publish your results.*
