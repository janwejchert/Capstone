"""Regenerate the poster figures as vector SVG from results/data and the
local simulator. Run as a script: python figures.py [--recompute].
"""
import os
import sys
import json
import argparse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

from reflexive_market import simulate
from reflexive_market.metrics import rolling_oos_r2, rolling_phi

ASSETS = os.path.join(HERE, "assets")
CACHE = os.path.join(ASSETS, "cache")
DATA = os.path.join(HERE, "..", "results", "data")

NAVY = "#1F4E79"
BLUE = "#1B6FC4"   # realised, self-fulfilment
RED = "#C62828"    # demand-adjusted, erosion
GOLD = "#B8860B"   # effective phi
INK = "#1A1A1A"
MUTE = "#5B6670"
HAIR = "#DDE3EA"


def set_style():
    fam = "DejaVu Sans"
    fdir = os.path.join(ASSETS, "fonts")
    if os.path.isdir(fdir):
        for fn in os.listdir(fdir):
            if fn.lower().endswith(".ttf") and "inter" in fn.lower():
                try:
                    font_manager.fontManager.addfont(os.path.join(fdir, fn))
                except Exception:
                    pass
        if any(f.name == "Inter" for f in font_manager.fontManager.ttflist):
            fam = "Inter"
    plt.rcParams.update({
        "font.family": fam,
        "font.size": 22,
        "axes.titlesize": 24,
        "axes.labelsize": 22,
        "axes.edgecolor": MUTE,
        "axes.linewidth": 1.2,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "xtick.labelsize": 19,
        "ytick.labelsize": 19,
        "axes.grid": True,
        "grid.color": HAIR,
        "grid.linewidth": 1.0,
        "legend.fontsize": 19,
        "legend.frameon": False,
        "savefig.dpi": 300,
        "svg.fonttype": "path",
    })
    return fam


def run_regime(pi, seed, T=8000):
    P = dict(N=200, mu=0.05, phi=0.25, sigma_news=0.01, sigma_q=1.0,
             forecast_window=250, forecast_p=1, risk_scale=0.001, q_cap=0.05,
             eval_window=1000, summary_span=1500)
    P["adoption_start_t"] = P["forecast_window"] + P["eval_window"]
    rng = np.random.default_rng(seed)
    out = simulate.run(
        T=T, N=P["N"], mu=P["mu"], phi=P["phi"],
        sigma_news=P["sigma_news"], sigma_q=P["sigma_q"], rng=rng,
        forecast_window=P["forecast_window"], forecast_p=P["forecast_p"],
        risk_scale=P["risk_scale"], q_cap=P["q_cap"],
        adoption_pi=pi, adoption_delta=0.0,
        adoption_start_t=P["adoption_start_t"],
    )
    out["da"] = out["returns"] - P["mu"] * out["demand"]
    out["r2_realised"] = rolling_oos_r2(out["returns"], out["forecasts"], P["eval_window"])
    out["r2_da"] = rolling_oos_r2(out["da"], out["forecasts"], P["eval_window"])
    out["phi"] = rolling_phi(out["returns"], P["eval_window"])
    return out, P


def summary_row(out, P):
    T = out["returns"].size
    warm = P["forecast_window"] + P["eval_window"]
    span = P["summary_span"]
    lo = slice(warm, warm + span)
    hi = slice(T - span, T)
    f = lambda a, s: float(np.nanmean(a[s]))
    return (
        f(out["adoption_share"], lo), f(out["adoption_share"], hi),
        f(out["r2_realised"], lo), f(out["r2_realised"], hi),
        f(out["r2_da"], lo), f(out["r2_da"], hi),
        f(out["phi"], lo), f(out["phi"], hi),
    )


def bin_stats(x, y, edges):
    inds = np.clip(np.digitize(x, edges) - 1, 0, len(edges) - 2)
    nb = len(edges) - 1
    means = np.full(nb, np.nan)
    stds = np.full(nb, np.nan)
    counts = np.zeros(nb, dtype=int)
    for i in range(nb):
        m = inds == i
        c = int(m.sum())
        counts[i] = c
        if c > 1:
            means[i] = y[m].mean()
            stds[i] = y[m].std()
    return means, stds, counts


NUM_SEEDS_MC = 100
MC_BASE_SEED = 1000


def compute_mc_fast(recompute=False):
    """Pooled post-warm-up observations for the fast-diffusion regime across
    NUM_SEEDS_MC seeds. Cached to assets/cache so re-renders are fast."""
    cache = os.path.join(CACHE, "phase4_mc_fast.npz")
    if os.path.exists(cache) and not recompute:
        d = np.load(cache)
        return d["A"], d["r2_real"], d["r2_da"], d["phi"]
    A, r2r, r2x, rp = [], [], [], []
    for s in range(NUM_SEEDS_MC):
        out, P = run_regime(1e-3, seed=MC_BASE_SEED + s)
        mask = np.isfinite(out["r2_realised"]) & np.isfinite(out["r2_da"]) & np.isfinite(out["phi"])
        A.append(out["adoption_share"][mask])
        r2r.append(out["r2_realised"][mask])
        r2x.append(out["r2_da"][mask])
        rp.append(out["phi"][mask])
    A = np.concatenate(A); r2r = np.concatenate(r2r)
    r2x = np.concatenate(r2x); rp = np.concatenate(rp)
    os.makedirs(CACHE, exist_ok=True)
    np.savez(cache, A=A, r2_real=r2r, r2_da=r2x, phi=rp)
    return A, r2r, r2x, rp


def make_dual_channel(recompute=False):
    A, r2r, r2x, rp = compute_mc_fast(recompute)
    edges = np.linspace(0.0, 1.0, 31)
    centers = 0.5 * (edges[:-1] + edges[1:])
    mr, sr, cr = bin_stats(A, r2r, edges)
    mx, sx, cx = bin_stats(A, r2x, edges)
    mp, sp, cp = bin_stats(A, rp, edges)
    vr, vx, vp = cr > 10, cx > 10, cp > 10

    fig, ax = plt.subplots(figsize=(9.5, 6.6))
    ax.plot(centers[vr], mr[vr], color=BLUE, linewidth=3.0,
            label="realised return (self-fulfilment)")
    ax.fill_between(centers[vr], mr[vr] - sr[vr], mr[vr] + sr[vr], color=BLUE, alpha=0.15)
    ax.plot(centers[vx], mx[vx], color=RED, linewidth=3.0,
            label="demand-adjusted (independent signal)")
    ax.fill_between(centers[vx], mx[vx] - sx[vx], mx[vx] + sx[vx], color=RED, alpha=0.15)
    ax.axhline(0.0, color=MUTE, linewidth=1.0)
    ax.set_xlabel("Adoption share")
    ax.set_ylabel("Rolling out-of-sample $R^2$")
    ax.set_xlim(0, 1)
    ax.legend(loc="upper center")
    ax.annotate("up: self-fulfilment", xy=(0.9, mr[vr][-1]), color=BLUE,
                fontsize=18, ha="right", va="bottom")
    ax.annotate("down: erosion", xy=(0.9, mx[vx][-1]), color=RED,
                fontsize=18, ha="right", va="top")

    inset = ax.inset_axes([0.13, 0.10, 0.34, 0.30])
    inset.plot(centers[vp], mp[vp], color=GOLD, linewidth=2.4)
    inset.axhline(0.25, color=MUTE, linewidth=1.0, linestyle="--")
    inset.set_title("effective $\\varphi$", fontsize=15, color=GOLD)
    inset.tick_params(labelsize=12)
    inset.set_xlim(0, 1)

    fig.tight_layout()
    fig.savefig(os.path.join(ASSETS, "fig_dual_channel.svg"))
    plt.close(fig)


N_SEEDS_SAT = 50
SAT_BASE_SEED = 5000
T_LONG = 30000


def compute_saturation(recompute=False):
    cache = os.path.join(CACHE, "phase4_saturation.npz")
    if os.path.exists(cache) and not recompute:
        d = np.load(cache)
        return d["t"], d["mr"], d["sr"], d["mx"], d["sx"], d["mA"]
    rr = np.full((N_SEEDS_SAT, T_LONG), np.nan)
    xx = np.full((N_SEEDS_SAT, T_LONG), np.nan)
    AA = np.full((N_SEEDS_SAT, T_LONG), np.nan)
    for s in range(N_SEEDS_SAT):
        out, P = run_regime(1e-3, seed=SAT_BASE_SEED + s, T=T_LONG)
        rr[s] = out["r2_realised"]
        xx[s] = out["r2_da"]
        AA[s] = out["adoption_share"]
    t = np.arange(T_LONG)
    mr, sr = np.nanmean(rr, axis=0), np.nanstd(rr, axis=0)
    mx, sx = np.nanmean(xx, axis=0), np.nanstd(xx, axis=0)
    mA = np.nanmean(AA, axis=0)
    os.makedirs(CACHE, exist_ok=True)
    np.savez(cache, t=t, mr=mr, sr=sr, mx=mx, sx=sx, mA=mA)
    return t, mr, sr, mx, sx, mA


def make_saturation(recompute=False):
    t, mr, sr, mx, sx, mA = compute_saturation(recompute)
    STEP = 10
    t, mr, sr, mx, sx, mA = t[::STEP], mr[::STEP], sr[::STEP], mx[::STEP], sx[::STEP], mA[::STEP]
    kr = np.isfinite(mr)
    kx = np.isfinite(mx)
    fig, ax = plt.subplots(figsize=(9.5, 5.2))
    ax.plot(t[kr], mr[kr], color=BLUE, linewidth=2.6, label="realised $R^2$")
    ax.fill_between(t[kr], mr[kr] - sr[kr], mr[kr] + sr[kr], color=BLUE, alpha=0.15)
    ax.plot(t[kx], mx[kx], color=RED, linewidth=2.6, label="demand-adjusted $R^2$")
    ax.fill_between(t[kx], mx[kx] - sx[kx], mx[kx] + sx[kx], color=RED, alpha=0.15)
    ax.axhline(0.0, color=MUTE, linewidth=1.0)
    ax.set_xlabel("Time period")
    ax.set_ylabel("Rolling out-of-sample $R^2$")
    ax.legend(loc="center right")
    ax2 = ax.twinx()
    ax2.plot(t, mA, color=MUTE, linewidth=1.4, linestyle="--", alpha=0.8)
    ax2.set_ylabel("Adoption share", color=MUTE)
    ax2.set_ylim(-0.02, 1.02)
    ax2.tick_params(axis="y", colors=MUTE)
    ax2.grid(False)
    fig.tight_layout()
    fig.savefig(os.path.join(ASSETS, "fig_saturation.svg"))
    plt.close(fig)


def _heatmap(ax, values, hit, mu_grid, phi_grid, title):
    im = ax.imshow(values, origin="lower", cmap="viridis_r", vmin=0.0, vmax=1.0, aspect="auto")
    ax.set_xticks(range(len(mu_grid)))
    ax.set_xticklabels([f"{m:g}" for m in mu_grid])
    ax.set_yticks(range(len(phi_grid)))
    ax.set_yticklabels([f"{p:.2f}" for p in phi_grid])
    ax.set_xlabel("$\\mu$ (price impact)")
    ax.set_ylabel("$\\varphi$ (input persistence)")
    ax.set_title(title)
    ax.grid(False)
    for i in range(len(phi_grid)):
        for j in range(len(mu_grid)):
            v = values[i, j]
            if not np.isfinite(v):
                text, color = f"hit {hit[i, j]:.1f}", "black"
            else:
                text, color = f"{v:.2f}", ("white" if v < 0.5 else "black")
            ax.text(j, i, text, ha="center", va="center", color=color, fontsize=15)
    return im


def make_threshold_heatmaps():
    d = np.load(os.path.join(DATA, "phase_06_a_star_grid.npz"))
    mu_grid, phi_grid = d["mu_grid"], d["phi_grid"]
    kw = 1  # w = 250
    specs = [
        ("a_star_R2_da", "hit_rate_R2_da", "fig_threshold_r2.svg",
         "$A^{*}_{R^2,\\mathrm{da}}$  (signal halved)"),
        ("a_star_phi", "hit_rate_phi", "fig_threshold_phi.svg",
         "$A^{*}_{\\varphi}$  (persistence x1.5)"),
    ]
    for vkey, hkey, fname, title in specs:
        vals = d[vkey][0, kw]   # AR(1) is p index 0
        hit = d[hkey][0, kw]
        fig, ax = plt.subplots(figsize=(6.6, 4.3))
        im = _heatmap(ax, vals, hit, mu_grid, phi_grid, title)
        cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cb.set_label("critical adoption share $A^{*}$")
        fig.tight_layout()
        fig.savefig(os.path.join(ASSETS, fname))
        plt.close(fig)


def write_values():
    """Headline numbers for the template, read from the saved npz so the poster
    text matches the report exactly."""
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
    set_style()
    make_dual_channel(args.recompute)
    make_saturation(args.recompute)
    make_threshold_heatmaps()
    write_values()
    print("wrote fig_dual_channel.svg, fig_saturation.svg, fig_threshold_r2.svg, fig_threshold_phi.svg and figure_values.json")


if __name__ == "__main__":
    main()
