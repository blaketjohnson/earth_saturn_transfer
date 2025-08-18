# Titan Mission Design 🚀🪐

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/build-passing-brightgreen)
![Docs](https://img.shields.io/badge/docs-pdf-orange)
![Figures](https://img.shields.io/badge/plots-available-blueviolet)

Preliminary mission design studies for **Earth → Saturn → Titan** trajectories, using
patched-conic methods and classical mission design tools.  

This repository demonstrates how to build quick-look interplanetary transfer analyses
with Python, including:

- Hohmann transfers
- Porkchop plots of launch Δv and arrival v∞
- Titan flyby geometry and turning-angle analysis
- Patched-conic approximations

The methods here were used to support the work described in:  
👉 [Mission Design Paper](docs/Proposal%20for%20the%20Geological%20and%20Atmospheric%20Data%20Expansion%20of%20Titan.pdf)

---

## 📊 Example Results

### Earth → Saturn Hohmann Transfer
![Hohmann Transfer](figures/hohmann_earth_saturn.png)

### Titan Flyby Turning Angle
![Titan Flyby](figures/titan_turn_angle.png)

### Titan Flyby Post-Flyby v∞ Mapping
![Post Flyby v∞](figures/vinf_after_flyby.png)

### Porkchop Plot (Earth → Saturn)
![Porkchop](figures/porkchop_earth_saturn.png)

---

## 📂 Repository Structure

```
titan_proposal/
├── src/                # Core Python modules (constants, patched_conics, plotting, transfers)
├── examples/           # Runnable scripts (Hohmann, Titan flyby, porkchop, etc.)
├── figures/            # Generated plots
├── docs/               # Documentation and presentations
└── README.md           # This file
```

---

## ⚡ Quick Start

1. Clone this repo:
   ```bash
   git clone https://github.com/YOUR_USERNAME/titan-mission-design.git
   cd titan-mission-design
   ```

2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Run an example:
   ```bash
   export PYTHONPATH=src   # (Linux/macOS)
   python examples/porkchop_earth_saturn.py
   ```

4. Figures will appear in the `figures/` folder.

---

## ✨ Features
- Circular-coplanar ephemerides (quick-look design).
- Lambert solver with universal variables.
- Porkchop plots of Δv from 300 km LEO and arrival v∞ at Saturn.
- Titan flyby geometry sanity checks.

---

## 🔮 Future Work
- Swap circular orbits for real planetary ephemerides (SPICE/Horizons).
- Multi-rev Lambert solver.
- Capture Δv at Saturn/Titan.
- Mission scenario design case studies.
