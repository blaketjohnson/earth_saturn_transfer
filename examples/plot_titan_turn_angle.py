from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from titan_flyby import turn_angle

def main() -> None:
    R_TITAN = 2_575_000.0  # m
    hs = np.linspace(100e3, 4000e3, 400)  # 100 km to 4000 km
    vinfs = [1e3, 3e3, 6e3, 9e3, 11e3]    # 1,3,6,9,11 km/s

    plt.figure(figsize=(7,5))
    for v in vinfs:
        deltas = [turn_angle(v, R_TITAN + h) for h in hs]
        plt.plot(hs/1000.0, np.degrees(deltas), label=f"{v/1000:.0f} km/s")

    plt.xlabel("Periapsis altitude above Titan (km)")
    plt.ylabel("Turn angle δ (deg)")
    plt.title("Titan flyby: turn angle vs periapsis altitude")
    plt.grid(True, alpha=0.3)
    plt.legend(title="v∞,T")
    plt.tight_layout()
    plt.savefig("figures/titan_turn_angle.png", dpi=300)
    print("Saved -> figures/titan_turn_angle.png")

if __name__ == "__main__":
    main()
