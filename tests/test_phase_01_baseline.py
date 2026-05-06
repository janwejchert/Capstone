"""Phase 1 invariants for the baseline market with null traders."""

import numpy as np

from reflexive_market import simulate
from reflexive_market.metrics import lag1_autocorr


def _params():
    return dict(T=300, N=64, mu=0.05, phi=0.10, sigma_news=0.01, sigma_q=1.0)


def test_output_shapes():
    rng = np.random.default_rng(0)
    out = simulate.run(rng=rng, **_params())
    assert out["prices"].shape == (301,)
    assert out["returns"].shape == (300,)
    assert out["demand"].shape == (300,)
    assert out["prices"][0] == 0.0


def test_same_seed_same_output():
    a = simulate.run(rng=np.random.default_rng(7), **_params())
    b = simulate.run(rng=np.random.default_rng(7), **_params())
    np.testing.assert_array_equal(a["returns"], b["returns"])
    np.testing.assert_array_equal(a["prices"], b["prices"])


def test_returns_match_price_diffs():
    out = simulate.run(rng=np.random.default_rng(1), **_params())
    np.testing.assert_allclose(out["returns"], np.diff(out["prices"]))


def test_zero_phi_gives_near_zero_lag1_autocorr():
    rng = np.random.default_rng(3)
    out = simulate.run(T=20000, N=200, mu=0.05, phi=0.0,
                       sigma_news=0.01, sigma_q=1.0, rng=rng)
    rho = lag1_autocorr(out["returns"])
    assert abs(rho) < 0.05


def test_empirical_phi_recovers_input_phi():
    rng = np.random.default_rng(5)
    out = simulate.run(T=20000, N=200, mu=0.05, phi=0.20,
                       sigma_news=0.01, sigma_q=1.0, rng=rng)
    rho = lag1_autocorr(out["returns"])
    assert abs(rho - 0.20) < 0.05
