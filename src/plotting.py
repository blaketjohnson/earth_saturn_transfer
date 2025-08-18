"""
Plot helper(s) for Earth→Saturn Hohmann quick-look.
Usage:
    from plotting import plot_hohmann_orbits
"""
from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt

def plot_hohmann_orbits(r1: float, r2: float, a_t: float, fname: str | None = None) -> None:
    """
    Plot two circular orbits of radii r1 and r2 and the Hohmann transfer ellipse between them.

    Args:
        r1, r2 : initial and final circular-orbit radii (m)
        a_t    : transfer ellipse semi-major axis (m)
        fname  : optional path to save the figure (PNG)
    """
    # Circles for the two orbits
    th = np.linspace(0.0, 2.0 * np.pi, 600)
    x1, y1 = r1 * np.cos(th), r1 * np.sin(th)
    x2, y2 = r2 * np.cos(th), r2 * np.sin(th)

    # Transfer ellipse in polar form: r(θ) = a(1-e^2)/(1 + e cos θ), periapsis at +x
    e = abs(r2 - r1) / (r1 + r2)
    th_t = np.linspace(0.0, np.pi, 400)  # half-ellipse from periapsis to apoapsis
    r_theta = a_t * (1.0 - e**2) / (1.0 + e * np.cos(th_t))
    xt, yt = r_theta * np.cos(th_t), r_theta * np.sin(th_t)

    plt.figure(figsize=(6, 6))
    plt.plot(x1, y1, label="Earth orbit (1 AU)")
    plt.plot(x2, y2, label="Saturn orbit (9.537 AU)")
    plt.plot(xt, yt, "--", label="Hohmann transfer")
    # Mark periapsis and apoapsis points
    plt.scatter([r1, -r2], [0.0, 0.0], s=20, zorder=3)

    plt.axis("equal")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.title("Earth→Saturn Hohmann (heliocentric)")
    plt.legend()

    if fname:
        plt.savefig(fname, dpi=300, bbox_inches="tight")
    # Do not call plt.show(); let caller decide
