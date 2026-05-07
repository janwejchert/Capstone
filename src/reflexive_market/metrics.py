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
