"""Top-level simulation loop.

Runs T periods following the intra-period timing fixed in section 3.6 of the
proposal:

    1. Agents form forecasts using returns up to and including period t.
    2. Adopters and non-adopters submit orders.
    3. The market maker absorbs aggregate demand and moves the quote.
    4. The exogenous news shock and residual AR term realise.

Phase 1 adds the loop with null traders only. Later phases add the forecast,
adoption, and switching steps.
"""

import numpy as np

from . import market, traders


def run(T, N, mu, phi, sigma_news, sigma_q, rng):
    """Run the baseline market for T periods with all traders using the null rule.

    Parameters
    ----------
    T : int
        Number of periods to simulate.
    N : int
        Number of traders.
    mu : float
        Market-maker price-impact coefficient (equation 5).
    phi : float
        Reduced-form residual AR(1) coefficient in the return law (equation 6).
    sigma_news : float
        Standard deviation of the exogenous news shock.
    sigma_q : float
        Standard deviation of individual null orders (equation 8).
    rng : numpy.random.Generator
        Source of randomness.

    Returns
    -------
    dict
        prices : ndarray of shape (T + 1,), log prices with p_0 = 0.
        returns : ndarray of shape (T,), one-period returns.
        demand : ndarray of shape (T,), aggregate demand each period.
    """
    prices = np.zeros(T + 1)
    returns = np.zeros(T)
    demand = np.zeros(T)

    r_prev = 0.0
    for t in range(T):
        orders = traders.null_orders(N, sigma_q, rng)
        D_t = market.aggregate_demand(orders)
        epsilon = rng.standard_normal()
        r_new = market.next_return(r_prev, D_t, mu, phi, sigma_news, epsilon)
        prices[t + 1] = prices[t] + r_new
        returns[t] = r_new
        demand[t] = D_t
        r_prev = r_new

    return {"prices": prices, "returns": returns, "demand": demand}
