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
