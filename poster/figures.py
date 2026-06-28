"""Write the headline numbers for the poster template from saved results.

The poster figures are hand-authored schematic SVG inlined in
poster.template.html. This script only refreshes assets/figure_values.json so
every number on the poster matches results/data (and therefore the report).
Run as a script: python figures.py [--recompute is accepted and ignored].
"""
import os
import json
import argparse

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
DATA = os.path.join(HERE, "..", "results", "data")


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
    ap.parse_args()
    write_values()
    print("wrote figure_values.json")


if __name__ == "__main__":
    main()
