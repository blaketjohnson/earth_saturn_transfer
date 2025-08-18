"""
Hohmann transfer utilities for circular heliocentric orbits.
Usage:
    from transfers import hohmann_dv, vis_viva
"""
from __future__ import annotations
import numpy as np
from typing import Tuple

def hohmann_dv(r1: float, r2: float, mu: float) -> Tuple[float, float, float]:
    """
    Hohmann transfer between circular orbits of radii r1 -> r2 (about same primary).
    Returns:
        dv1 : injection Δv at r1 (m/s)
        dv2 : circularization Δv at r2 (m/s)
        tof : time of flight (s)
    """
    a_t = 0.5 * (r1 + r2)                           # transfer semi-major axis
    v1  = np.sqrt(mu / r1)                          # circular speeds
    v2  = np.sqrt(mu / r2)
    v_peri = np.sqrt(mu * (2.0 / r1 - 1.0 / a_t))   # transfer speeds
    v_apo  = np.sqrt(mu * (2.0 / r2 - 1.0 / a_t))
    dv1 = abs(v_peri - v1)
    dv2 = abs(v2 - v_apo)
    tof = np.pi * np.sqrt(a_t**3 / mu)              # half an ellipse
    return float(dv1), float(dv2), float(tof)

def vis_viva(mu: float, r: float, a: float) -> float:
    """Speed from vis-viva at radius r on an orbit with semi-major axis a around GM=mu."""
    return float(np.sqrt(mu * (2.0 / r - 1.0 / a)))

__all__ = ["hohmann_dv", "vis_viva"]
