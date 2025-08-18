from __future__ import annotations
import numpy as np
from typing import Tuple
from constants import mu_saturn, mu_titan, a_titan, circ_speed

def turn_angle(vinf_t: float, rp: float, mu_t: float = mu_titan) -> float:
    """
    Flyby turn angle δ (radians) given Titan-relative v∞ and periapsis radius rp.
    δ = 2 * atan( μ / (rp * v∞^2) )
    """
    return 2.0 * np.arctan(mu_t / (rp * vinf_t**2))

def rp_from_turn(vinf_t: float, delta: float, mu_t: float = mu_titan) -> float:
    """
    Invert the turn-angle relation to get required periapsis radius rp.
    """
    return mu_t / (vinf_t**2 * np.tan(delta / 2.0))

def titan_orbital_speed() -> float:
    """Titan's circular speed around Saturn (m/s)."""
    return circ_speed(mu_saturn, a_titan)

def post_flyby_vinf_saturn(
    vinf_saturn: float,
    psi: float,
    h_peri: float,
    mu_t: float = mu_titan,
    prograde: bool = True,
) -> Tuple[float, float, float]:
    """
    Patched-conics quick-look: incoming Saturn-relative v∞ with magnitude V,
    Titan orbital speed VT, and alignment angle psi (angle between V and VT).
    We rotate the Titan-relative incoming v∞ by ±δ at periapsis, then add back VT.

    Args:
        vinf_saturn : |V| Saturn-relative incoming v∞ (m/s)
        psi         : angle between V and VT in the Saturn frame [rad]
        h_peri      : flyby periapsis altitude above Titan surface [m]
        prograde    : if True rotate by +δ, else by -δ

    Returns:
        (V_out_mag, vinf_t_in, delta)
    """
    VT = titan_orbital_speed()

    # Put V along +x; VT at angle psi
    Vx, Vy = vinf_saturn, 0.0
    VTx, VTy = VT * np.cos(psi), VT * np.sin(psi)

    # Titan-relative incoming v∞
    vin_t_in = np.array([Vx - VTx, Vy - VTy])
    vinf_t_in = float(np.linalg.norm(vin_t_in))

    # Periapsis radius (Titan radius ~ 2_575 km)
    R_TITAN = 2_575_000.0
    rp = R_TITAN + h_peri
    delta = float(turn_angle(vinf_t_in, rp, mu_t))

    # Rotate incoming Titan-relative v∞ by ±δ
    s = +1.0 if prograde else -1.0
    c, sgn = np.cos(s * delta), np.sin(s * delta)
    R = np.array([[c, -sgn], [sgn, c]])
    vout_t = R @ vin_t_in

    # Back to Saturn frame
    vout_s = vout_t + np.array([VTx, VTy])
    Vout = float(np.linalg.norm(vout_s))
    return Vout, vinf_t_in, delta
