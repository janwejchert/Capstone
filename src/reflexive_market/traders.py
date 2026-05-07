"""Trader demand mapping and the null random rule.

Implements equations (1), (2), (3), (8) from the proposal. Phase 1 adds the
null rule. Phase 4 adds the demand mapping with position cap for adopters.
"""

import numpy as np


def null_orders(N, sigma_q, rng):
    """Equation (8): q_{i,t}^(0) = xi_{i,t}, xi ~ N(0, sigma_q^2).

    Returns an array of length N, one independent draw per trader.
    """
    return rng.normal(0.0, sigma_q, size=N)


def advanced_order(forecast, risk_scale, q_cap):
    """Equation (3): q_{i,t}^(A) = clip(forecast / (a sigma^2), -q_cap, q_cap).

    The proposal writes the denominator as a * sigma^2 (risk aversion times
    perceived variance); only the product enters demand, so it is passed in
    as a single ``risk_scale`` parameter.

    Returns 0.0 when the forecast is not finite, so warm-up periods leave
    adopters effectively inactive without inflating downstream demand.
    """
    if not np.isfinite(forecast):
        return 0.0
    return float(np.clip(forecast / risk_scale, -q_cap, q_cap))
