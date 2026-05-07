"""Evaluation metrics.

Covers section 4 of the proposal. Primary endpoints: rolling MSFE, rolling
out-of-sample R^2, rolling effective AR coefficient, position synchronization,
and the critical adoption share A*. Added incrementally as each phase needs
new metrics.
"""

import numpy as np


def lag1_autocorr(returns):
    """Empirical first-order autocorrelation of a return series.

    Used in phase 1 to confirm the simulator reproduces the input phi within
    sampling error, and as a diagnostic in later phases (section 4.2).
    """
    if len(returns) < 2:
        return float("nan")
    return float(np.corrcoef(returns[:-1], returns[1:])[0, 1])


def kurtosis(x):
    """Excess kurtosis (Fisher's definition: Gaussian gives 0).

    Used in phase 2 to confirm the per-seed return distribution is close to
    Gaussian, as expected when null orders and the news shock are both Gaussian.
    """
    x = np.asarray(x, dtype=float)
    if x.size < 2:
        return float("nan")
    m = x.mean()
    var = float(((x - m) ** 2).mean())
    if var == 0.0:
        return float("nan")
    return float(((x - m) ** 4).mean() / (var ** 2) - 3.0)


def rolling_phi(returns, window):
    """Rolling lag-1 autocorrelation of returns over a sliding window.

    Phase 2 uses this to show the effective AR coefficient does not drift in
    expectation when no one is trading on a forecast. Later phases reuse it
    to track erosion as adoption rises.

    Output has the same length as ``returns``. The first ``window - 1``
    entries are NaN. Each later entry is the lag-1 autocorrelation of the
    most recent ``window`` returns ending at that index.
    """
    returns = np.asarray(returns, dtype=float)
    n = returns.size
    out = np.full(n, np.nan)
    if window < 2 or n < window:
        return out
    for i in range(window - 1, n):
        seg = returns[i - window + 1 : i + 1]
        out[i] = float(np.corrcoef(seg[:-1], seg[1:])[0, 1])
    return out


def msfe(actual, forecast):
    """Mean squared forecast error over finite aligned observations."""
    actual = np.asarray(actual, dtype=float)
    forecast = np.asarray(forecast, dtype=float)
    if actual.shape != forecast.shape:
        raise ValueError("actual and forecast must have the same shape")

    mask = np.isfinite(actual) & np.isfinite(forecast)
    if not np.any(mask):
        return float("nan")
    errors = actual[mask] - forecast[mask]
    return float(np.mean(errors ** 2))


def rolling_msfe(actual, forecast, window):
    """Rolling mean squared forecast error over finite trailing windows."""
    actual = np.asarray(actual, dtype=float)
    forecast = np.asarray(forecast, dtype=float)
    if actual.shape != forecast.shape:
        raise ValueError("actual and forecast must have the same shape")

    n = actual.size
    out = np.full(n, np.nan)
    if window < 1 or n < window:
        return out

    sq_error = (actual - forecast) ** 2
    finite = np.isfinite(sq_error)
    for i in range(window - 1, n):
        seg = sq_error[i - window + 1 : i + 1]
        seg_finite = finite[i - window + 1 : i + 1]
        if np.all(seg_finite):
            out[i] = float(np.mean(seg))
    return out


def rolling_oos_r2(actual, forecast, window):
    """Rolling out-of-sample R^2 against a constant-mean benchmark."""
    actual = np.asarray(actual, dtype=float)
    forecast = np.asarray(forecast, dtype=float)
    if actual.shape != forecast.shape:
        raise ValueError("actual and forecast must have the same shape")

    n = actual.size
    out = np.full(n, np.nan)
    if window < 2 or n < window:
        return out

    sq_error = (actual - forecast) ** 2
    finite = np.isfinite(sq_error)
    for i in range(window - 1, n):
        start = i - window + 1
        seg_actual = actual[start : i + 1]
        seg_error = sq_error[start : i + 1]
        seg_finite = finite[start : i + 1] & np.isfinite(seg_actual)
        if not np.all(seg_finite):
            continue
        denom = float(np.sum((seg_actual - seg_actual.mean()) ** 2))
        if denom > 0.0:
            out[i] = 1.0 - float(np.sum(seg_error)) / denom
    return out


def sign_accuracy(actual, forecast):
    """Share of finite forecasts with the same non-zero sign as actual returns."""
    actual = np.asarray(actual, dtype=float)
    forecast = np.asarray(forecast, dtype=float)
    if actual.shape != forecast.shape:
        raise ValueError("actual and forecast must have the same shape")

    mask = np.isfinite(actual) & np.isfinite(forecast)
    mask &= actual != 0.0
    mask &= forecast != 0.0
    if not np.any(mask):
        return float("nan")
    return float(np.mean(np.sign(actual[mask]) == np.sign(forecast[mask])))
