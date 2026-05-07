"""Adoption mechanisms.

Implements equations (11), (12) for stochastic diffusion (added in phase 4)
and equations (13), (14), (15) for risk-adjusted performance-based switching
(added in phase 5).
"""

import numpy as np


def stochastic_diffusion_step(adoption, pi, delta, rng):
    """Equations (11) and (12): one period of independent per-agent transitions.

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
