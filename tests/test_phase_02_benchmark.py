"""Phase 2 invariants for benchmark validation across seeds."""

import numpy as np

from reflexive_market import simulate
from reflexive_market.metrics import kurtosis, lag1_autocorr, rolling_phi


def test_kurtosis_gaussian_near_zero():
    rng = np.random.default_rng(0)
    x = rng.standard_normal(50_000)
    assert abs(kurtosis(x)) < 0.1


def test_kurtosis_constant_returns_nan():
    x = np.full(10, 3.0)
    assert np.isnan(kurtosis(x))


def test_rolling_phi_shape_and_leading_nans():
    returns = np.linspace(-1.0, 1.0, 200)
    out = rolling_phi(returns, window=50)
    assert out.shape == (200,)
    assert np.all(np.isnan(out[:49]))
    assert not np.any(np.isnan(out[49:]))


def test_rolling_phi_recovers_input_phi_on_synthetic_ar1():
    rng = np.random.default_rng(11)
    T = 5000
    phi = 0.30
    eps = rng.standard_normal(T)
    r = np.zeros(T)
    for t in range(1, T):
        r[t] = phi * r[t - 1] + eps[t]
    out = rolling_phi(r, window=1000)
    tail = out[~np.isnan(out)]
    assert abs(tail.mean() - phi) < 0.05


def test_per_seed_stats_cluster_tightly():
    """The benchmark control: across many seeds the descriptive statistics
    should cluster around their theoretical values, with no drift."""
    params = dict(T=2000, N=128, mu=0.05, phi=0.10,
                  sigma_news=0.01, sigma_q=1.0)
    means = []
    rhos = []
    for seed in range(20):
        out = simulate.run(rng=np.random.default_rng(seed), **params)
        means.append(out["returns"].mean())
        rhos.append(lag1_autocorr(out["returns"]))
    means = np.array(means)
    rhos = np.array(rhos)
    assert abs(means.mean()) < 0.001
    assert abs(rhos.mean() - 0.10) < 0.05
    assert rhos.std() < 0.05
