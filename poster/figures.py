"""Write the headline numbers for the poster template from saved results.

The poster figures are hand-authored schematic SVG inlined in
poster.template.html. This script only refreshes assets/figure_values.json so
every number on the poster matches results/data (and therefore the report).
Run as a script: python figures.py [--recompute is accepted and ignored].
"""
import os
import json
import argparse
import warnings

import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.join(HERE, "..", "src"))

from reflexive_market import simulate  # noqa: E402
from reflexive_market.metrics import rolling_oos_r2  # noqa: E402

ASSETS = os.path.join(HERE, "assets")
DATA = os.path.join(HERE, "..", "results", "data")

# Phase-4 fast-diffusion parameters (notebooks/phase_04_stochastic_adoption.ipynb).
P4_N = 200
P4_MU = 0.05
P4_PHI = 0.25
P4_SIGMA_NEWS = 0.01
P4_SIGMA_Q = 1.0
P4_FORECAST_WINDOW = 250
P4_FORECAST_P = 1
P4_RISK_SCALE = 0.001
P4_Q_CAP = 0.05
P4_EVAL_WINDOW = 1000
P4_ADOPTION_START_T = P4_FORECAST_WINDOW + P4_EVAL_WINDOW  # 1250
FAST_PI = 1e-3
FAST_DELTA = 0.0
T_LONG = 30000
SAT_BASE_SEED = 5000
NUM_SEEDS_MC = 50
RESULT_NPZ = os.path.join(DATA, "poster_result_curve.npz")


def make_polyline(xs, ys, x0, x1, y0, y1, w, h, decimals=2):
    """Map data coordinates to an SVG path 'd' string in a w x h box.

    The y-axis is flipped so larger data y values sit higher in the SVG
    (which has its origin at the top-left).
    """
    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)
    px = (xs - x0) * (w / (x1 - x0))
    py = h - (ys - y0) * (h / (y1 - y0))
    pts = [f"{round(float(a), decimals)},{round(float(b), decimals)}"
           for a, b in zip(px, py)]
    return "M" + " L".join(pts)


def _run_fast(seed, T):
    rng = np.random.default_rng(seed)
    out = simulate.run(
        T=T, N=P4_N, mu=P4_MU, phi=P4_PHI,
        sigma_news=P4_SIGMA_NEWS, sigma_q=P4_SIGMA_Q, rng=rng,
        forecast_window=P4_FORECAST_WINDOW, forecast_p=P4_FORECAST_P,
        risk_scale=P4_RISK_SCALE, q_cap=P4_Q_CAP,
        adoption_pi=FAST_PI, adoption_delta=FAST_DELTA,
        adoption_start_t=P4_ADOPTION_START_T,
    )
    da = out["returns"] - P4_MU * out["demand"]
    r2_real = rolling_oos_r2(out["returns"], out["forecasts"], P4_EVAL_WINDOW)
    r2_da = rolling_oos_r2(da, out["forecasts"], P4_EVAL_WINDOW)
    return r2_real, r2_da, out["adoption_share"]


def compute_result_curve(num_seeds=NUM_SEEDS_MC, T=T_LONG, span=1500):
    r2r = np.full((num_seeds, T), np.nan)
    r2d = np.full((num_seeds, T), np.nan)
    adopt = np.full((num_seeds, T), np.nan)
    for s in range(num_seeds):
        r2r[s], r2d[s], adopt[s] = _run_fast(SAT_BASE_SEED + s, T)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        mean_r2r = np.nanmean(r2r, axis=0)
        mean_r2d = np.nanmean(r2d, axis=0)
        mean_A = np.nanmean(adopt, axis=0)

    finite = np.isfinite(mean_r2r) & np.isfinite(mean_r2d) & np.isfinite(mean_A)
    fin_idx = np.flatnonzero(finite)
    lo = fin_idx[:span]
    hi = fin_idx[-span:]
    low_real, high_real = float(mean_r2r[lo].mean()), float(mean_r2r[hi].mean())
    low_da, high_da = float(mean_r2d[lo].mean()), float(mean_r2d[hi].mean())
    low_A, high_A = float(mean_A[lo].mean()), float(mean_A[hi].mean())

    # Bin the finite samples by adoption share into a clean vs-adoption curve.
    nb = 50
    edges = np.linspace(0.0, 1.0, nb + 1)
    centres = 0.5 * (edges[:-1] + edges[1:])
    a_vals, yr, yd = mean_A[finite], mean_r2r[finite], mean_r2d[finite]
    which = np.clip(np.digitize(a_vals, edges) - 1, 0, nb - 1)
    ca, cr, cd = [], [], []
    for k in range(nb):
        m = which == k
        if m.any():
            ca.append(float(centres[k]))
            cr.append(float(yr[m].mean()))
            cd.append(float(yd[m].mean()))

    return {
        "adopt_curve": np.array(ca), "r2_real_vs_a": np.array(cr),
        "r2_da_vs_a": np.array(cd),
        "mean_r2_real_t": mean_r2r, "mean_r2_da_t": mean_r2d, "mean_A_t": mean_A,
        "low_real": low_real, "high_real": high_real,
        "low_da": low_da, "high_da": high_da, "low_A": low_A, "high_A": high_A,
        "plateau_real": high_real, "plateau_da": high_da,
        "num_seeds": int(num_seeds), "T": int(T),
    }


def load_or_compute_result_curve(recompute=False):
    if not recompute and os.path.exists(RESULT_NPZ):
        d = np.load(RESULT_NPZ)
        return {k: d[k] for k in d.files}
    data = compute_result_curve(num_seeds=NUM_SEEDS_MC, T=T_LONG)
    np.savez(RESULT_NPZ, **{k: np.asarray(v) for k, v in data.items()})
    return data


# Result-curve plot rect (matches the template SVG).
RC_W, RC_H = 270, 120
RC_YMAX = 0.2
# Price-path plot rect.
PP_W, PP_H = 304, 104
# Steady-state plot rect (absolute viewBox coords).
SS_TOP, SS_H, SS_YMAX = 24, 150, 0.2


def write_figure_geometry(data):
    prices = np.load(os.path.join(DATA, "phase_01_baseline.npz"))["prices"]
    step = max(1, prices.size // 300)
    idx = np.arange(0, prices.size, step)
    pmin, pmax = float(prices.min()), float(prices.max())
    pad = (pmax - pmin) * 0.05
    price_d = make_polyline(idx, prices[idx], 0, prices.size - 1,
                            pmin - pad, pmax + pad, PP_W, PP_H)

    real_d = make_polyline(data["adopt_curve"], data["r2_real_vs_a"],
                           0, 1, 0, RC_YMAX, RC_W, RC_H)
    da_d = make_polyline(data["adopt_curve"], data["r2_da_vs_a"],
                         0, 1, 0, RC_YMAX, RC_W, RC_H)

    plat_real = float(data["plateau_real"])
    plat_da = float(data["plateau_da"])
    geom = {
        "price_path_d": price_d,
        "result_real_d": real_d,
        "result_da_d": da_d,
        "result_high_real": f"{float(data['high_real']):.2f}",
        "result_high_da": f"{float(data['high_da']):.2f}",
        "result_low_real": f"{float(data['low_real']):.2f}",
        "result_low_da": f"{float(data['low_da']):.2f}",
        "plateau_real": f"{plat_real:.2f}",
        "plateau_da": f"{plat_da:.2f}",
        "steady_real_y": round(SS_TOP + (1 - plat_real / SS_YMAX) * SS_H, 1),
        "steady_da_y": round(SS_TOP + (1 - plat_da / SS_YMAX) * SS_H, 1),
    }
    out = os.path.join(ASSETS, "figure_values.json")
    existing = json.load(open(out)) if os.path.exists(out) else {}
    existing.update(geom)
    json.dump(existing, open(out, "w"), indent=2)


def write_values():
    summ = np.load(os.path.join(DATA, "phase_04_stochastic_adoption.npz"))["summary"]
    vals = {
        "r2_real_low": round(float(summ[0, 2]), 2),
        "r2_real_high": round(float(summ[2, 3]), 2),
        "r2_da_low": round(float(summ[0, 4]), 2),
        "r2_da_high": round(float(summ[2, 5]), 2),
        "phi_low": round(float(summ[0, 6]), 2),
        "phi_high": round(float(summ[2, 7]), 2),
    }
    g = np.load(os.path.join(DATA, "phase_06_a_star_grid.npz"))
    da0, phi0, real0 = g["a_star_R2_da"][0], g["a_star_phi"][0], g["a_star_R2_realised"][0]
    vals.update({
        "n_da_hit": int(np.isfinite(da0).sum()), "n_da_cells": int(da0.size),
        "a_da_mean": round(float(np.nanmean(da0)), 2),
        "n_phi_hit": int(np.isfinite(phi0).sum()),
        "a_phi_mean": round(float(np.nanmean(phi0)), 2),
        "n_real_hit": int(np.isfinite(real0).sum()),
        "n_runs": int(g["mu_grid"].size * g["phi_grid"].size * g["w_grid"].size
                      * g["forecast_p_grid"].size * int(g["num_seeds"])),
    })
    out = os.path.join(ASSETS, "figure_values.json")
    existing = {}
    if os.path.exists(out):
        existing = json.load(open(out))
    existing.update(vals)
    json.dump(existing, open(out, "w"), indent=2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--recompute", action="store_true")
    args = ap.parse_args()
    write_values()
    data = load_or_compute_result_curve(recompute=args.recompute)
    write_figure_geometry(data)
    print("wrote figure_values.json")


if __name__ == "__main__":
    main()
