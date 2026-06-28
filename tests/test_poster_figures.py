import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "poster"))
import figures  # noqa: E402


def test_make_polyline_maps_and_flips_y():
    d = figures.make_polyline([0, 1, 2], [0, 1, 0], 0, 2, 0, 1, 100, 50)
    assert d == "M0.0,50.0 L50.0,0.0 L100.0,50.0"


def test_compute_result_curve_shows_dual_channel():
    # Tiny MC for speed; the dual-channel effect is strong enough to show.
    data = figures.compute_result_curve(num_seeds=4, T=6000, span=400)
    for k in ["adopt_curve", "r2_real_vs_a", "r2_da_vs_a",
              "low_real", "high_real", "low_da", "high_da",
              "plateau_real", "plateau_da"]:
        assert k in data, k
    # Realised R^2 rises with adoption; demand-adjusted R^2 falls.
    assert data["r2_real_vs_a"][-1] > data["r2_real_vs_a"][0]
    assert data["r2_da_vs_a"][-1] < data["r2_da_vs_a"][0]
    assert data["high_real"] > data["low_real"]
    assert data["high_da"] < data["low_da"]


def test_load_or_compute_result_curve_roundtrips(tmp_path, monkeypatch):
    npz = tmp_path / "curve.npz"
    monkeypatch.setattr(figures, "RESULT_NPZ", str(npz))
    monkeypatch.setattr(figures, "NUM_SEEDS_MC", 3)
    monkeypatch.setattr(figures, "T_LONG", 5000)
    d1 = figures.load_or_compute_result_curve(recompute=True)
    assert npz.exists()
    d2 = figures.load_or_compute_result_curve(recompute=False)
    np.testing.assert_allclose(d1["adopt_curve"], d2["adopt_curve"])
