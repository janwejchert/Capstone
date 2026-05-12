"""Phase 3 invariants for rolling AR forecasts."""

import numpy as np

from reflexive_market import forecast, simulate
from reflexive_market.metrics import (
    msfe,
    rolling_msfe,
    rolling_oos_r2,
    sign_accuracy,
)


def test_ar_design_aligns_targets_and_lags():
    x, y = forecast.ar_design(np.array([1.0, 2.0, 4.0, 8.0]), p=2)

    expected_x = np.array([
        [1.0, 2.0, 1.0],
        [1.0, 4.0, 2.0],
    ])
    expected_y = np.array([4.0, 8.0])

    np.testing.assert_allclose(x, expected_x)
    np.testing.assert_allclose(y, expected_y)


def test_fit_ar_recovers_synthetic_ar1_parameters():
    rng = np.random.default_rng(4)
    intercept = 0.01
    phi = 0.35
    returns = np.zeros(8000)
    for t in range(1, returns.size):
        returns[t] = intercept + phi * returns[t - 1] + rng.normal(0.0, 0.02)

    params = forecast.fit_ar(returns, p=1)

    assert abs(params[0] - intercept) < 0.002
    assert abs(params[1] - phi) < 0.03


def test_rolling_ar_forecast_shape_and_warmup():
    returns = np.linspace(-1.0, 1.0, 200)

    forecasts, params = forecast.rolling_ar_forecast(returns, window=50, p=1)

    assert forecasts.shape == (200,)
    assert params.shape == (200, 2)
    assert np.all(np.isnan(forecasts[:50]))
    assert np.all(np.isnan(params[:50]))
    assert np.all(np.isfinite(forecasts[50:]))
    assert np.all(np.isfinite(params[50:]))


def test_rolling_ar_forecast_shape_with_higher_order():
    returns = np.linspace(-1.0, 1.0, 200)

    forecasts, params = forecast.rolling_ar_forecast(returns, window=50, p=3)

    assert forecasts.shape == (200,)
    assert params.shape == (200, 4)
    assert np.all(np.isnan(forecasts[:50]))
    assert np.all(np.isnan(params[:50]))
    assert np.all(np.isfinite(forecasts[50:]))
    assert np.all(np.isfinite(params[50:]))


def test_rolling_ar_forecast_uses_only_past_returns():
    base = np.sin(np.arange(100) / 10.0)
    altered_future = base.copy()
    altered_future[30:] += 100.0

    base_forecasts, _ = forecast.rolling_ar_forecast(base, window=20, p=1)
    altered_forecasts, _ = forecast.rolling_ar_forecast(
        altered_future, window=20, p=1
    )

    assert base_forecasts[30] == altered_forecasts[30]


def test_msfe_and_sign_accuracy_ignore_missing_forecasts():
    actual = np.array([1.0, -2.0, 3.0, 4.0])
    predicted = np.array([1.5, np.nan, -1.0, 5.0])

    assert msfe(actual, predicted) == np.mean([0.5 ** 2, 4.0 ** 2, 1.0 ** 2])
    assert sign_accuracy(actual, predicted) == 2 / 3


def test_rolling_msfe_and_oos_r2_shapes_and_leading_nans():
    actual = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    predicted = np.array([np.nan, 2.1, 2.9, 4.2, 4.8])

    error = rolling_msfe(actual, predicted, window=3)
    r2 = rolling_oos_r2(actual, predicted, window=3)

    assert error.shape == actual.shape
    assert r2.shape == actual.shape
    assert np.all(np.isnan(error[:3]))
    assert np.all(np.isnan(r2[:3]))
    assert np.all(np.isfinite(error[3:]))
    assert np.all(np.isfinite(r2[3:]))


def test_phase3_forecast_has_positive_oos_r2_on_predictable_null_market():
    rng = np.random.default_rng(9)
    out = simulate.run(
        T=6000,
        N=200,
        mu=0.05,
        phi=0.25,
        sigma_news=0.01,
        sigma_q=1.0,
        rng=rng,
    )
    returns = out["returns"]
    forecasts, _ = forecast.rolling_ar_forecast(returns, window=250, p=1)
    r2 = rolling_oos_r2(returns, forecasts, window=1000)

    assert np.nanmean(r2[-1000:]) > 0.02
