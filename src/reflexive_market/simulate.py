"""Top-level simulation loop.

Runs T periods following the intra-period timing fixed in section 3.6 of the
proposal:

    1. Agents form forecasts using returns up to and including period t.
    2. Adopters and non-adopters submit orders.
    3. The market maker absorbs aggregate demand and moves the quote.
    4. The exogenous news shock and residual AR term realise.

Phase 1 added the loop with null traders only. Phase 4 extends the same
function with the rolling AR forecast, the BH98 advanced order with cap, and
stochastic adoption diffusion. The defaults reduce the function back to the
phase 1-3 baseline.
"""

import numpy as np

from . import adoption as adoption_mod
from . import forecast as forecast_mod
from . import market, traders


def run(
    T,
    N,
    mu,
    phi,
    sigma_news,
    sigma_q,
    rng,
    forecast_window=None,
    forecast_p=1,
    risk_scale=None,
    q_cap=None,
    adoption_pi=0.0,
    adoption_delta=0.0,
    initial_adoption_share=0.0,
):
    """Run the market for T periods.

    With the phase 1-3 defaults (no forecast_window, zero adoption) every
    trader uses the random null rule and the loop is the original baseline
    simulator. Pass a forecast_window plus adoption parameters to run the
    phase 4 setup with reflexive adoption.

    Parameters
    ----------
    T, N, mu, phi, sigma_news, sigma_q, rng :
        Phase 1 parameters. See equations (5), (6), (8).
    forecast_window : int or None
        Rolling AR window length. None disables forecasting; adopters then
        always trade the null rule.
    forecast_p : int
        AR order. Defaults to 1, matching equations (9), (10).
    risk_scale : float or None
        Combined ``a * sigma^2`` denominator from equation (3). Required when
        forecast_window is set.
    q_cap : float or None
        Per-trader position cap from equation (3). Required when
        forecast_window is set.
    adoption_pi, adoption_delta : float
        Per-period transition probabilities for equations (11), (12).
    initial_adoption_share : float
        Fraction of agents who already use the advanced rule at t = 0.

    Returns
    -------
    dict with keys
        prices, returns, demand : as in the phase 1 baseline.
        forecasts : ndarray of shape (T,), one-period-ahead AR forecast each
            period (NaN before the warm-up).
        adoption_share : ndarray of shape (T,), share of adopters at the end
            of each period after the diffusion step.
    """
    # Spawn an independent rng for adoption draws so adoption parameters
    # cannot advance the market shock stream. With this split, no-op
    # adoption settings (pi = delta = 0, no initial adopters) leave the
    # realised market path identical to a call without any adoption args,
    # and across-regime comparisons stay paired on the same shocks.
    adoption_rng = np.random.default_rng(rng.integers(0, 2**63 - 1))

    prices = np.zeros(T + 1)
    returns = np.zeros(T)
    demand = np.zeros(T)
    forecasts = np.full(T, np.nan)
    adoption_share = np.zeros(T)

    forecasting_on = forecast_window is not None
    if forecasting_on and (risk_scale is None or q_cap is None):
        raise ValueError(
            "risk_scale and q_cap are required when forecast_window is set"
        )

    adoption = np.zeros(N, dtype=int)
    if initial_adoption_share > 0.0:
        n_initial = int(round(initial_adoption_share * N))
        if n_initial > 0:
            initial_idx = adoption_rng.choice(N, size=n_initial, replace=False)
            adoption[initial_idx] = 1

    r_prev = 0.0
    for t in range(T):
        if forecasting_on and t >= forecast_window:
            history = returns[t - forecast_window : t]
            fitted = forecast_mod.fit_ar(history, p=forecast_p)
            forecasts[t] = forecast_mod.forecast_next(history, fitted)

        null = traders.null_orders(N, sigma_q, rng)
        if forecasting_on:
            q_adv = traders.advanced_order(forecasts[t], risk_scale, q_cap)
            orders = (1 - adoption) * null + adoption * q_adv
        else:
            orders = null

        D_t = market.aggregate_demand(orders)
        epsilon = rng.standard_normal()
        r_new = market.next_return(r_prev, D_t, mu, phi, sigma_news, epsilon)

        prices[t + 1] = prices[t] + r_new
        returns[t] = r_new
        demand[t] = D_t
        r_prev = r_new

        if adoption_pi > 0.0 or adoption_delta > 0.0:
            adoption = adoption_mod.stochastic_diffusion_step(
                adoption, adoption_pi, adoption_delta, adoption_rng
            )
        adoption_share[t] = adoption.mean()

    return {
        "prices": prices,
        "returns": returns,
        "demand": demand,
        "forecasts": forecasts,
        "adoption_share": adoption_share,
    }
