"""
Titan-relative v∞ sanity bounds given a Saturn-relative v∞.
This is a quick vector-add bound, not a full patched-conics flyby solution.
Run (flat src layout):
    PYTHONPATH=src python examples/titan_flyby_sanity.py
"""
from __future__ import annotations
from patched_conics import titan_relative_vinf_bounds

def main() -> None:
    # Example: pick a representative Saturn v∞ (e.g., from the Hohmann quick-look)
    vinf_saturn = 5.5e3  # m/s  (≈ 5.5 km/s)
    vlow, vhigh = titan_relative_vinf_bounds(vinf_saturn)

    print("=== Titan v∞ sanity bounds (given Saturn v∞) ===")
    print(f"Saturn v∞ : {vinf_saturn/1000:.2f} km/s")
    print(f"Titan v∞  : {vlow/1000:.2f} – {vhigh/1000:.2f} km/s")

if __name__ == "__main__":
    main()
