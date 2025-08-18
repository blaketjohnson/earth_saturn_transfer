from __future__ import annotations
from pathlib import Path
from constants import a_earth, a_saturn, mu_sun
from transfers import hohmann_dv
from plotting import plot_hohmann_orbits

def main() -> None:
    r1, r2 = a_earth, a_saturn
    dv1, dv2, tof = hohmann_dv(r1, r2, mu_sun)
    a_t = 0.5 * (r1 + r2)

    out = Path("figures/hohmann_earth_saturn.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    plot_hohmann_orbits(r1, r2, a_t, fname=str(out))

    print("=== Earth → Saturn Hohmann (geometry) ===")
    print(f"Δv1 (inject):        {dv1/1000:.3f} km/s")
    print(f"Δv2 (circularize):   {dv2/1000:.3f} km/s")
    print(f"TOF (transfer):      {tof/86400/365.25:.2f} years")
    print(f"Saved figure -> {out}")

if __name__ == "__main__":
    main()
