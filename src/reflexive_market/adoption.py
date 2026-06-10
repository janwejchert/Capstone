"""Adoption mechanisms.

Implements equations (12), (13) for stochastic diffusion (added in phase 4)
and equations (14) and (15) for risk-adjusted performance-based switching
(added in phase 5).
"""

import numpy as np


def stochastic_diffusion_step(adoption, pi, delta, rng):
    """Equations (12) and (13): one period of independent per-agent transitions.

    Each non-adopter switches to adopter with probability ``pi``. Each
    adopter exits to non-adopter with probability ``delta``. Transitions
    are independent across agents, matching the BH98 discrete-choice spirit
    while keeping the mechanism analytically simple.
    """
    adoption = np.asarray(adoption, dtype=int)
    new = adoption.copy()
    if pi > 0.0:
        u = rng.random(adoption.size)
        new[(adoption == 0) & (u < pi)] = 1
    if delta > 0.0:
        u = rng.random(adoption.size)
        new[(adoption == 1) & (u < delta)] = 0
    return new


def performance_switching_step(adoption, ce_score, alpha, beta, rng):
    """Equation (15): non-adopters switch with logistic probability in the
    certainty-equivalent score gap S = CE^(A) - CE^(0).

    The proposal specifies only the entry direction, P(a_{i,t+1} = 1 |
    a_{i,t} = 0) = Lambda(alpha + beta * S). Adopters keep their state.
    This matches the asymmetric form used by stochastic diffusion in
    equations (12) and (13) and lets per-period rates stay slow even when
    Lambda would otherwise jump near 0.5.
    """
    adoption = np.asarray(adoption, dtype=int)
    # Clip the logit so that extreme score gaps do not overflow np.exp.
    logit = float(np.clip(alpha + beta * ce_score, -500.0, 500.0))
    p_up = 1.0 / (1.0 + np.exp(-logit))
    new = adoption.copy()
    u = rng.random(adoption.size)
    new[(adoption == 0) & (u < p_up)] = 1
    return new
