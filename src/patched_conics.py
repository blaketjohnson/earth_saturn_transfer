"""
Simple patched-conics helpers for Saturn/Titan arrival quick-look.
Usage:
    from patched_conics import arrival_vinf_heliocentric, titan_relative_vinf_bounds
"""
from __future__ import annotations
import numpy as np
from typing import Tuple
from constants import mu_sun, mu_saturn, a_titan, circ_speed

def arrival_vinf_heliocentric(r_arrive: float, a_transfer: float, mu: float = mu_sun) -> float:
    """
    Hyperbolic excess speed at planet arrival relative to planet's circular heliocentric frame.
    Args:
        r_arrive    : planet heliocentric radius (m)
        a_transfer  : semi-major axis of the heliocentric transfer ellipse (m)
        mu          : primary GM (default Sun) (m^3/s^2)
    Returns:
        v_inf at the planet (m/s), computed as |v_sc - v_planet|.
    """
    v_sc = np.sqrt(mu * (2.0 / r_arrive - 1.0 / a_transfer))  # spacecraft speed on transfer
    v_planet = np.sqrt(mu / r_arrive)                         # planet circular speed
    return float(abs(v_sc - v_planet))

def titan_relative_vinf_bounds(vinf_saturn: float) -> Tuple[float, float]:
    """
    Crude bounds on Titan-relative v∞ given Saturn-relative v∞ (vector-add/sub Titan orbital speed).
    This is a direction-dependent bound, not a full trajectory solution.
    Args:
        vinf_saturn : Saturn-relative hyperbolic excess speed (m/s)
    Returns:
        (v_inf_min, v_inf_max) relative to Titan (m/s)
    """
    v_titan = circ_speed(mu_saturn, a_titan)
    vmin = max(0.0, vinf_saturn - v_titan)
    vmax = vinf_saturn + v_titan
    return float(vmin), float(vmax)

__all__ = ["arrival_vinf_heliocentric", "titan_relative_vinf_bounds"]
