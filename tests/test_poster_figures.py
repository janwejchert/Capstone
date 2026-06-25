import os, sys
import numpy as np
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "poster"))
import figures

NPZ = os.path.join(HERE, "results", "data", "phase_04_stochastic_adoption.npz")

def test_summary_row_reproduces_npz_fast_and_control():
    summ = np.load(NPZ)["summary"]  # rows: zero, slow, fast
    # control (pi=0) is row 0, fast (pi=1e-3) is row 2; seed 71 as in the notebook
    out0, P = figures.run_regime(0.0, seed=71)
    row0 = figures.summary_row(out0, P)
    np.testing.assert_allclose(row0, summ[0], atol=1e-6)
    out2, P = figures.run_regime(1e-3, seed=71)
    row2 = figures.summary_row(out2, P)
    np.testing.assert_allclose(row2, summ[2], atol=1e-6)


def test_saturation_plateau_levels():
    # cheap check on the plateau using a few seeds and the post-ramp tail
    out, P = figures.run_regime(1e-3, seed=figures.SAT_BASE_SEED, T=figures.T_LONG)
    tail = slice(10000, figures.T_LONG)
    assert 0.13 < float(np.nanmean(out["r2_realised"][tail])) < 0.21
    assert -0.01 < float(np.nanmean(out["r2_da"][tail])) < 0.06


def test_dual_channel_svg_written(tmp_path, monkeypatch):
    figures.set_style()
    # speed: tiny MC by monkeypatching the seed count
    monkeypatch.setattr(figures, "NUM_SEEDS_MC", 3)
    cache = os.path.join(figures.CACHE, "phase4_mc_fast.npz")
    if os.path.exists(cache):
        os.remove(cache)
    figures.make_dual_channel(recompute=True)
    p = os.path.join(figures.ASSETS, "fig_dual_channel.svg")
    assert os.path.getsize(p) > 5000
    head = open(p).read(400).lower()
    assert "<svg" in head or "<?xml" in head
