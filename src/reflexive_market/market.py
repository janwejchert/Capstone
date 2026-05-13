"""Aggregate demand, market-maker price update, and the return law.

Implements equations (4), (5), (6) from the proposal. Functions are added
phase by phase. Phase 1 introduces the price update and the return law for
a market with null traders only.
"""

import numpy as np


def aggregate_demand(orders):
    """Equation (4): D_t = (1/N) sum_i q_{i,t}."""
    return float(np.mean(orders))


def next_return(r_prev, demand, mu, phi, sigma_news, epsilon):
    """Equation (6): r_{t+1} = phi * r_t + mu * D_t + sigma * epsilon_{t+1}.

    The intra-period order is fixed in section 3.6 of the proposal: traders
    submit orders, the market maker moves the quote by mu * D_t, and then the
    autoregressive term phi*r_prev plus the exogenous news shock realise.
    """
    return phi * r_prev + mu * demand + sigma_news * epsilon
