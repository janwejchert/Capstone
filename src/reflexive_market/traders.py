"""Trader demand mapping and the null random rule.

Implements equations (1), (2), (3), (8) from the proposal. Phase 1 adds the
null rule. Phase 4 adds the demand mapping with position cap for adopters.
"""


def null_orders(N, sigma_q, rng):
    """Equation (8): q_{i,t}^(0) = xi_{i,t}, xi ~ N(0, sigma_q^2).

    Returns an array of length N, one independent draw per trader.
    """
    return rng.normal(0.0, sigma_q, size=N)
