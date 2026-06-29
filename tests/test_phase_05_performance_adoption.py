"""Phase 5 invariants for risk-adjusted performance-based adoption."""

import numpy as np
import pytest

from reflexive_market import adoption, simulate


def test_performance_switching_zero_score_returns_baseline_logistic():
    rng = np.random.default_rng(0)
    state = np.zeros(20_000, dtype=int)
    out = adoption.performance_switching_step(
        state, ce_score=0.0, alpha=0.0, beta=1.0, rng=rng
    )
    assert abs(out.mean() - 0.5) < 0.02


def test_performance_switching_high_score_saturates_non_adopters():
    rng = np.random.default_rng(1)
    state = np.zeros(2_000, dtype=int)
    out = adoption.performance_switching_step(
        state, ce_score=1.0, alpha=0.0, beta=10.0, rng=rng
    )
    assert out.mean() > 0.99


def test_performance_switching_does_not_drop_adopters():
    rng = np.random.default_rng(2)
    state = np.ones(500, dtype=int)
    out = adoption.performance_switching_step(
        state, ce_score=-100.0, alpha=0.0, beta=10.0, rng=rng
    )
    np.testing.assert_array_equal(out, state)


def test_simulate_run_rejects_both_adoption_modes():
    with pytest.raises(ValueError):
        simulate.run(
            T=100, N=10, mu=0.05, phi=0.10, sigma_news=0.01, sigma_q=1.0,
            rng=np.random.default_rng(0),
            forecast_window=20, forecast_p=1, risk_scale=0.001, q_cap=1.0,
            adoption_pi=0.01,
            switching_window=20, switching_beta=1.0,
        )


def test_simulate_run_with_switching_grows_adoption_when_score_positive():
    out = simulate.run(
        T=4000, N=200, mu=0.05, phi=0.25, sigma_news=0.01, sigma_q=1.0,
        rng=np.random.default_rng(43),
        forecast_window=250, forecast_p=1, risk_scale=0.001, q_cap=0.05,
        switching_window=500,
        switching_a=1.0,
        switching_alpha=-5.0,
        switching_beta=10000.0,
        adoption_start_t=1250,
    )
    assert np.all(out["adoption_share"][:1250] == 0.0)
    assert out["adoption_share"][-1] > 0.5
    # Switching score should be positive on average post-warm-up given a
    # forecast that beats the null rule.
    valid = out["switching_score"][~np.isnan(out["switching_score"])]
    assert valid.mean() > 0.0


def test_switching_args_with_no_firing_do_not_change_market_path():
    """Same paired-shocks invariant as phase 4: switching args must not
    change the realised market path when adoption_start_t holds switching
    off for the entire run."""
    common = dict(
        T=400, N=64, mu=0.05, phi=0.10, sigma_news=0.01, sigma_q=1.0,
        forecast_window=50, forecast_p=1, risk_scale=0.001, q_cap=1.0,
    )
    base = simulate.run(rng=np.random.default_rng(13), **common)
    with_switching = simulate.run(
        rng=np.random.default_rng(13),
        switching_window=50,
        switching_a=1.0,
        switching_alpha=-5.0,
        switching_beta=10000.0,
        adoption_start_t=10_000,
        **common,
    )
    np.testing.assert_array_equal(base["returns"], with_switching["returns"])
