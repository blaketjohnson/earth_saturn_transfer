"""
Basic constants for Titan mission quick-look studies (SI units).
Usage:
    from constants import AU, mu_sun, a_earth, a_saturn, a_titan, circ_speed
"""
from __future__ import annotations
import numpy as np

# Grav. parameters (GM) in m^3/s^2 (approx standard values)
mu_sun: float    = 1.32712440018e20
mu_earth: float  = 3.986004418e14
mu_saturn: float = 3.7931187e16
mu_titan: float  = 8.978e12

# Distances
AU: float       = 1.495978707e11           # Astronomical Unit [m]
a_earth: float  = 1.000 * AU               # Earth heliocentric mean distance [m]
a_saturn: float = 9.537 * AU               # Saturn heliocentric mean distance [m]
a_titan: float  = 1_221_870e3              # Titan orbital radius about Saturn [m] (~1.22187e6 km)

def circ_speed(mu: float, r: float) -> float:
    """Circular orbital speed at radius r around body with GM=mu."""
    return float(np.sqrt(mu / r))

__all__ = [
    "mu_sun", "mu_earth", "mu_saturn", "mu_titan",
    "AU", "a_earth", "a_saturn", "a_titan",
    "circ_speed",
]
