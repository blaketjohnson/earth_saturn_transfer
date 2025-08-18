"""
Earth→Saturn Hohmann transfer quick-look with Δv, TOF, and arrival v∞ estimates.
Generates: docs/hohmann_earth_saturn.png
Run (flat src layout):
    PYTHONPATH=src python examples/earth_to_saturn_hohmann.py
"""
from __future__ import annotations
import os
from constants import a_earth, a_saturn, mu_sun
from transfers import hohmann_dv
from patched_conics import arrival_vinf_heliocentric, titan_relative_vinf_bounds
from plotting import plot_hohmann_orbits

def main() -> None:
    r1, r2 = a_earth, a_saturn

    # Hohmann Δv and time of flight (Sun-centered, circular orbits)
    dv1, dv2, tof = hohmann_dv(r1, r2, mu_sun)
    a_t = 0.5 * (r1 + r2)

    # Arrival v∞ at Saturn (spacecraft vs planet circular speed at r2)
    vinf_saturn = arrival_vinf_heliocentric(r2, a_t, mu_sun)

    # Simple Titan-relative v∞ bounds (not a full trajectory solution)
    vinf_titan_lo, vinf_titan_hi = titan_relative_vinf_bounds(vinf_saturn)

    # Print a compact summary
    print("=== Earth → Saturn Hohmann (quick-look) ===")
    print(f"Δv1 (inject)           : {dv1/1000:.3f} km/s")
    print(f"Δv2 (circularize)      : {dv2/1000:.3f} km/s")
    print(f"TOF (transfer)         : {tof/(365.25*24*3600):.2f} years")
    print(f"v∞ at Saturn (helioc.) : {vinf_saturn/1000:.3f} km/s")
    print(f"v∞ at Titan (bounds)   : {vinf_titan_lo/1000:.3f} – {vinf_titan_hi/1000:.3f} km/s")

    # Save a simple heliocentric transfer plot for the README/docs
    os.makedirs("docs", exist_ok=True)
    plot_hohmann_orbits(r1, r2, a_t, fname="docs/hohmann_earth_saturn.png")
    print("Saved figure -> docs/hohmann_earth_saturn.png")

if __name__ == "__main__":
    main()
