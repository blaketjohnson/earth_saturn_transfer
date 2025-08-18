from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
from titan_flyby import post_flyby_vinf_saturn, titan_orbital_speed

def main() -> None:
    V_in = 5_500.0  # m/s at Saturn from your quick-look
    VT = titan_orbital_speed()

    # Sweep alignment angle psi in [0, π] and altitude 100–4000 km
    ps = np.linspace(0.0, np.pi, 181)
    hs = np.linspace(100e3, 4000e3, 121)

    # Heatmap of outgoing Saturn-relative v∞ after a prograde turn
    H = np.zeros((hs.size, ps.size))
    for i, h in enumerate(hs):
        for j, p in enumerate(ps):
            Vout, vinf_t_in, delta = post_flyby_vinf_saturn(V_in, p, h, prograde=True)
            H[i, j] = Vout

    plt.figure(figsize=(8,4.8))
    im = plt.imshow(
        H/1000.0, origin="lower",
        extent=[0.0, 180.0, hs[0]/1000.0, hs[-1]/1000.0],
        aspect="auto"
    )
    cbar = plt.colorbar(im, label="|v∞| after flyby (km/s)")
    plt.contour(
        np.degrees(ps), hs/1000.0, H/1000.0,
        levels=np.arange(0.0, (V_in+VT)/1000.0+0.5, 0.5),
        colors="k", alpha=0.2, linewidths=0.6
    )
    plt.xlabel("Alignment ψ (deg)  [ψ=0 → VT aligned with V_in]")
    plt.ylabel("Periapsis altitude h (km)")
    plt.title("Saturn→Titan patched-conics quick-look (prograde turn)")
    plt.tight_layout()
    plt.savefig("figures/vinf_after_flyby.png", dpi=300)
    print("Saved -> figures/vinf_after_flyby.png")

if __name__ == "__main__":
    main()
