from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from pathlib import Path

# --- repo constants (SI) ---
from constants import mu_sun, a_earth, a_saturn  # [m^3/s^2], [m], [m]

DAY  = 86400.0
YEAR = 365.25 * DAY

# ================================
# Circular, coplanar ephemerides
# ================================
def circ_pos_vel(a: float, t: float, mu: float) -> tuple[np.ndarray, np.ndarray]:
    n = np.sqrt(mu / a**3)
    c, s = np.cos(n * t), np.sin(n * t)
    r = np.array([a * c, a * s, 0.0])
    v = np.array([-a * n * s, a * n * c, 0.0])
    return r, v

# ================================
# Stumpff functions
# ================================
def stumpC(z: float) -> float:
    if z > 0:  return (1 - np.cos(np.sqrt(z))) / z
    if z < 0:  return (np.cosh(np.sqrt(-z)) - 1) / (-z)
    return 0.5

def stumpS(z: float) -> float:
    if z > 0:
        s = np.sqrt(z)
        return (s - np.sin(s)) / (s**3)
    if z < 0:
        s = np.sqrt(-z)
        return (np.sinh(s) - s) / (s**3)
    return 1.0 / 6.0

# ================================
# Single-rev Lambert (universal variables)
# ================================
def lambert_universal(r1: np.ndarray, r2: np.ndarray, dt: float, mu: float,
                      long_way: bool = False) -> tuple[np.ndarray, np.ndarray]:
    r1n, r2n = np.linalg.norm(r1), np.linalg.norm(r2)
    cos_dnu = np.clip(np.dot(r1, r2) / (r1n * r2n), -1.0, 1.0)
    dnu = np.arccos(cos_dnu)
    if long_way:
        dnu = 2*np.pi - dnu

    A = np.sin(dnu) * np.sqrt(r1n * r2n / (1 - np.cos(dnu)))
    if np.isclose(A, 0.0):
        raise RuntimeError("Lambert: A≈0")

    z = 0.0
    z_low, z_up = -40.0, 40.0
    for _ in range(120):
        C, S = stumpC(z), stumpS(z)
        if C <= 0:  z += 0.1; continue
        y = r1n + r2n + A * (z*S - 1) / np.sqrt(C)
        if y <= 0:  z += 0.1; continue

        chi = np.sqrt(y / C)
        F = chi**3 * S + A * np.sqrt(y) - np.sqrt(mu) * dt
        if abs(F) < 1e-8: break

        if z == 0.0:
            dC, dS = -1/6, -1/120
        else:
            dC = (0.5*z*(S - 2*C) - C) / z
            dS = (0.5*z*(1 - 4*C) - 3*S) / (3*z)

        dy_dz   = (A/(2*np.sqrt(C))) * (S + z*dS) - (A*(z*S - 1)*dC) / (2*C**1.5)
        dchi_dz = (0.5/np.sqrt(y*C)) * (dy_dz*C - y*dC) / C
        dFdz    = 3*chi**2*dchi_dz*S + chi**3*dS + (A/(2*np.sqrt(y))) * dy_dz

        if not np.isfinite(dFdz) or dFdz == 0:
            if F > 0: z_up = min(z_up, z)
            else:     z_low = max(z_low, z)
            z = 0.5*(z_low + z_up)
        else:
            z_new = z - F/dFdz
            if F > 0: z_up = min(z_up, z)
            else:     z_low = max(z_low, z)
            z = 0.5*(z_low + z_up) if (z_new < z_low or z_new > z_up) else z_new

    C, S = stumpC(z), stumpS(z)
    y = r1n + r2n + A * (z*S - 1) / np.sqrt(C)
    if y <= 0: raise RuntimeError("Lambert: y<=0")

    f = 1 - y / r1n
    g = A * np.sqrt(y / mu)
    gdot = 1 - y / r2n
    v1 = (r2 - f*r1) / g
    v2 = (gdot*r2 - r1) / g
    return v1, v2

# ================================
# Plot helpers
# ================================
def setup_date_axis(ax):
    loc = mdates.AutoDateLocator(minticks=5, maxticks=10)
    ax.xaxis.set_major_locator(loc)
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(loc))

def auto_levels(masked_mat: np.ma.MaskedArray, n: int = 24, pct=(5, 95)) -> np.ndarray:
    vals = masked_mat.compressed()
    if vals.size == 0:
        return np.linspace(0.0, 1.0, n)
    vmin, vmax = np.percentile(vals, pct)
    if not np.isfinite(vmin) or not np.isfinite(vmax) or vmin == vmax:
        vmin, vmax = float(vals.min()), float(vals.max()) + 1e-6
    return np.linspace(vmin, vmax, n)

# LEO departure Δv from v∞
def dv_from_leo(vinf: float, h_leo_km: float = 300.0) -> float:
    muE = 3.986004418e14  # m^3/s^2
    RE  = 6378.0e3        # m
    r   = RE + h_leo_km*1e3
    v_circ = np.sqrt(muE / r)
    v_esc  = np.sqrt(2.0 * muE / r)
    return np.sqrt(vinf**2 + v_esc**2) - v_circ  # m/s

# ================================
# Main
# ================================
def main():
    # ---- knobs ----
    USE_LONG_WAY = False
    LEO_ALT_KM   = 300.0
    epoch0       = datetime(2030, 1, 1)
    dep_start    = datetime(2030, 1, 1)
    dep_end      = datetime(2035, 1, 1)
    tof_min_yr, tof_max_yr = 4.0, 11.0
    n_dep, n_tof = 140, 110  # a touch denser

    # tuned contour steps (readable valley)
    DV_LEVELS = np.arange(4.0, 15.01, 0.25)   # km/s
    VA_LEVELS = np.arange(5.0, 14.01, 0.25)   # km/s

    # synodic lines (~1.03 yr)
    SYNC_YEARS = 1.035
    syno_dates = []
    d = dep_start
    while d <= dep_end:
        syno_dates.append(d)
        d += timedelta(days=int(SYNC_YEARS*365.25))

    # grids
    dep_dates  = np.array([dep_start + i*(dep_end-dep_start)/(n_dep-1) for i in range(n_dep)])
    tofs_years = np.linspace(tof_min_yr, tof_max_yr, n_tof)

    DV_LEO   = np.full((n_tof, n_dep), np.nan)  # km/s
    VINF_ARR = np.full((n_tof, n_dep), np.nan)  # km/s

    # sweep
    for j, t_dep in enumerate(dep_dates):
        t1 = (t_dep - epoch0).total_seconds()
        r1, vE = circ_pos_vel(a_earth, t1, mu_sun)

        for i, tof_y in enumerate(tofs_years):
            dt = float(tof_y * YEAR)
            t2 = t1 + dt
            r2, vS = circ_pos_vel(a_saturn, t2, mu_sun)

            try:
                v1s, v2s = lambert_universal(r1, r2, dt, mu_sun, long_way=False)
                v1, v2 = v1s, v2s
                if USE_LONG_WAY:
                    v1l, v2l = lambert_universal(r1, r2, dt, mu_sun, long_way=True)
                    dv_s = dv_from_leo(np.linalg.norm(v1s - vE), LEO_ALT_KM)
                    dv_l = dv_from_leo(np.linalg.norm(v1l - vE), LEO_ALT_KM)
                    v1, v2 = (v1l, v2l) if dv_l < dv_s else (v1s, v2s)
            except Exception:
                continue

            vinf_dep = np.linalg.norm(v1 - vE)  # m/s
            vinf_arr = np.linalg.norm(v2 - vS)  # m/s
            DV_LEO[i, j]   = dv_from_leo(vinf_dep, LEO_ALT_KM) / 1000.0
            VINF_ARR[i, j] = vinf_arr / 1000.0

    # plotting
    D, T = np.meshgrid(dep_dates, tofs_years)  # (n_tof, n_dep)

    DVm = np.ma.masked_invalid(DV_LEO)
    VAm = np.ma.masked_invalid(VINF_ARR)

    fig, axs = plt.subplots(1, 2, figsize=(16.2, 6.2), constrained_layout=True)

    # Left: Δv from LEO
    cs1 = axs[0].contourf(D, T, DVm, levels=DV_LEVELS, cmap="viridis", extend="both", antialiased=True)
    axs[0].contour(D, T, DVm, levels=DV_LEVELS, colors="k", linewidths=0.35, alpha=0.45)
    axs[0].set_title(f"Earth→Saturn porkchop: departure Δv from LEO ({LEO_ALT_KM:.0f} km)")
    axs[0].set_ylabel("Time of flight (years)")
    axs[0].grid(True, alpha=0.2, linestyle=":")
    setup_date_axis(axs[0])
    cb1 = fig.colorbar(cs1, ax=axs[0], label="Δv_dep (km/s)")

    # Right: arrival v∞
    cs2 = axs[1].contourf(D, T, VAm, levels=VA_LEVELS, cmap="plasma", extend="both", antialiased=True)
    axs[1].contour(D, T, VAm, levels=VA_LEVELS, colors="k", linewidths=0.35, alpha=0.45)
    axs[1].set_title("Arrival v∞ at Saturn (km/s)")
    axs[1].set_ylabel("Time of flight (years)")
    axs[1].grid(True, alpha=0.2, linestyle=":")
    setup_date_axis(axs[1])
    cb2 = fig.colorbar(cs2, ax=axs[1], label="v∞,arrival (km/s)")

    # Hatch infeasible cells
    nan_mask = ~np.isfinite(DV_LEO)
    for ax in axs:
        ax.contourf(D, T, nan_mask, levels=[0.5, 1.5], hatches=["///"], colors="none", alpha=0)

    # ---- Optimal "valley" line (argmin over TOF for each departure) ----
    valley_tof = np.full(n_dep, np.nan)
    for j in range(n_dep):
        col = DV_LEO[:, j]
        if np.isfinite(col).any():
            valley_tof[j] = tofs_years[np.nanargmin(col)]

    # Plot the dashed valley on both panels
    axs[0].plot(dep_dates, valley_tof, ls="--", lw=2.0, color="w", alpha=0.9, label="Δv valley")
    axs[1].plot(dep_dates, valley_tof, ls="--", lw=2.0, color="w", alpha=0.9)

    # Mark global minima
    if np.isfinite(DV_LEO).any():
        i_dv, j_dv = np.unravel_index(np.nanargmin(DV_LEO), DV_LEO.shape)
        axs[0].plot(dep_dates[j_dv], tofs_years[i_dv], "o", ms=6, mfc="w", mec="k")
        axs[0].annotate(
            f"min Δv_dep = {DV_LEO[i_dv, j_dv]:.2f} km/s\nTOF={tofs_years[i_dv]:.2f} y",
            (dep_dates[j_dv], tofs_years[i_dv]), xytext=(10, 10),
            textcoords="offset points", fontsize=8,
            bbox=dict(boxstyle="round,pad=0.2", fc="w", alpha=0.85)
        )
        axs[1].plot(dep_dates[j_dv], tofs_years[i_dv], "o", ms=6, mfc="w", mec="k")

    if np.isfinite(VINF_ARR).any():
        i_va, j_va = np.unravel_index(np.nanargmin(VINF_ARR), VINF_ARR.shape)
        axs[1].plot(dep_dates[j_va], tofs_years[i_va], "s", ms=6, mfc="w", mec="k")
        axs[1].annotate(
            f"min v∞ = {VINF_ARR[i_va, j_va]:.2f} km/s\nTOF={tofs_years[i_va]:.2f} y",
            (dep_dates[j_va], tofs_years[i_va]), xytext=(10, -18),
            textcoords="offset points", fontsize=8,
            bbox=dict(boxstyle="round,pad=0.2", fc="w", alpha=0.85)
        )

    # Synodic cycle guide lines
    for ax in axs:
        for dline in syno_dates:
            ax.axvline(dline, color="w", lw=0.8, ls=":", alpha=0.35)

    axs[0].set_xlabel("Departure date")
    axs[1].set_xlabel("Departure date")
    axs[0].legend(loc="upper left", fontsize=8, frameon=True)

    out = Path("figures/porkchop_earth_saturn.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out, dpi=300)
    print(f"Saved -> {out}")

if __name__ == "__main__":
    main()



