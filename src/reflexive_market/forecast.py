"""Rolling autoregressive forecast.

Implements equations (10), (11) from the proposal. Estimation uses
np.linalg.lstsq on a lagged design matrix. Added in phase 3.
"""

import numpy as np


def ar_design(returns, p=1):
    """Build the lagged design matrix for an AR(p) model with an intercept."""
    returns = np.asarray(returns, dtype=float)
    if p < 1:
        raise ValueError("p must be at least 1")
    if returns.size <= p:
        raise ValueError("returns must contain more observations than p")

    y = returns[p:]
    x = np.ones((y.size, p + 1))
    for j in range(1, p + 1):
        x[:, j] = returns[p - j : returns.size - j]
    return x, y


def fit_ar(returns, p=1):
    """Estimate equation (10), returning [intercept, phi_1, ..., phi_p]."""
    x, y = ar_design(returns, p)
    params, *_ = np.linalg.lstsq(x, y, rcond=None)
    return params


def forecast_next(history, params):
    """Forecast the next return from recent history and fitted AR parameters."""
    history = np.asarray(history, dtype=float)
    params = np.asarray(params, dtype=float)
    p = params.size - 1
    if p < 1:
        raise ValueError(
            "params must include an intercept and at least one AR coefficient"
        )
    if history.size < p:
        raise ValueError("history must contain at least p observations")

    lags = history[-1 : -p - 1 : -1]
    return float(params[0] + np.dot(params[1:], lags))


def rolling_ar_forecast(returns, window, p=1):
    """Generate one-step-ahead rolling AR forecasts without look-ahead.

    At index t, the model is fit on returns[t - window:t], then forecasts
    returns[t]. The first window entries are NaN.

    Returns
    -------
    forecasts : ndarray of shape (T,)
        One-step-ahead forecasts aligned with the realised return index.
    params : ndarray of shape (T, p + 1)
        Rolling fitted [intercept, phi_1, ..., phi_p] values.
    """
    returns = np.asarray(returns, dtype=float)
    if p < 1:
        raise ValueError("p must be at least 1")
    if window <= p:
        raise ValueError("window must be greater than p")

    n = returns.size
    forecasts = np.full(n, np.nan)
    params = np.full((n, p + 1), np.nan)
    for t in range(window, n):
        history = returns[t - window : t]
        fitted = fit_ar(history, p)
        params[t] = fitted
        forecasts[t] = forecast_next(history, fitted)
    return forecasts, params
