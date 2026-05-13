"""Top-level simulation loop.

Runs T periods following the intra-period timing fixed in section 3.6 of the
proposal:

    1. Agents form forecasts using returns up to and including period t.
    2. Adopters and non-adopters submit orders.
    3. The market maker absorbs aggregate demand and moves the quote.
    4. The exogenous news shock and the autoregressive term phi*r_prev realise.

Phase 1 added the loop with null traders only. Phase 4 extends the same
function with the rolling AR forecast, the BH98 advanced order with cap, and
stochastic adoption diffusion. Phase 5 adds the certainty-equivalent
performance-based switching rule. The defaults reduce the function back to
the phase 1-3 baseline.
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
    adoption_start_t=0,
    switching_window=None,
    switching_a=0.0,
    switching_alpha=0.0,
    switching_beta=0.0,
):
    """Run the market for T periods.

    With the phase 1-3 defaults (no forecast_window, zero adoption) every
    trader uses the random null rule and the loop is the original baseline
    simulator. Pass a forecast_window plus adoption parameters to run the
    phase 4 stochastic setup, or a forecast_window plus switching parameters
    for the phase 5 certainty-equivalent setup.

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
    adoption_start_t : int
        Index at which adoption transitions begin. Before this index the
        adoption indicators stay at their initial values. Lets phase 4 and 5
        align the adoption onset with metric warm-up.
    switching_window : int or None
        Rolling window length for certainty-equivalent computation
        (equation 13). When set, equations (13)-(15) replace the stochastic
        diffusion. Cannot be combined with non-zero adoption_pi or
        adoption_delta.
    switching_a : float
        Risk-aversion coefficient ``a`` in CE = mean - (a/2) * var (eq 13).
    switching_alpha : float
        Baseline adoption term in equation (15).
    switching_beta : float
        Sensitivity to recent performance in equation (15).

    Returns
    -------
    dict with keys
        prices, returns, demand : as in the phase 1 baseline.
        forecasts : ndarray of shape (T,), one-period-ahead AR forecast each
            period (NaN before the warm-up).
        adoption_share : ndarray of shape (T,), share of adopters that drove
            returns[t]/demand[t]/null_profit[t]/advanced_profit[t]. Recorded
            before the end-of-period transition fires, so adoption_share[t]
            is the state used to generate period t's outcomes.
        null_profit, advanced_profit : ndarray of shape (T,), per-period
            realised profit of a representative trader following each rule
            (eq 7). For the null rule, the representative trader is the
            lowest-indexed non-adopter at period t, so null_profit[t] has
            per-trader mean and variance independent of the adoption share.
            null_profit[t] is NaN at periods where every trader is an adopter
            (no non-adopter representative exists). Used by the phase 5 CE
            computation and the phase 7 null-relative profit endpoint.
        switching_score : ndarray of shape (T,), score S_t from eq 14 each
            period switching is performed; NaN otherwise.
    """
    using_switching = switching_window is not None
    using_stochastic = adoption_pi > 0.0 or adoption_delta > 0.0
    if using_switching and using_stochastic:
        raise ValueError(
            "stochastic diffusion and CE-based switching cannot both be active"
        )

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
    null_profit = np.zeros(T)
    advanced_profit = np.zeros(T)
    switching_score = np.full(T, np.nan)

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
            q_adv = 0.0
            orders = null

        D_t = market.aggregate_demand(orders)
        epsilon = rng.standard_normal()
        r_new = market.next_return(r_prev, D_t, mu, phi, sigma_news, epsilon)

        prices[t + 1] = prices[t] + r_new
        returns[t] = r_new
        demand[t] = D_t
        r_prev = r_new

        # Per-period realised profit of a representative trader following
        # each rule (equation 7). The advanced rule's representative profit
        # is q_adv times the realised return, common across all adopters
        # since the forecast is public. The null rule's representative is
        # the lowest-indexed non-adopter: their realised order is null[i]
        # and their realised profit is null[i] * r_new. Using a single
        # representative non-adopter (rather than the population mean of
        # all N null draws) gives per-trader mean and variance that do not
        # depend on the adoption share; the population-mean version
        # decays linearly in (1 - A) in expectation and has variance scaled
        # by 1/N, which biases both the phase 5 CE risk penalty and the
        # phase 7 null-relative profit endpoint. When every trader is an
        # adopter there is no non-adopter representative and null_profit
        # is NaN; downstream code already handles NaN inputs.
        non_adopter_idx = np.flatnonzero(adoption == 0)
        if non_adopter_idx.size > 0:
            null_profit[t] = float(null[non_adopter_idx[0]]) * r_new
        else:
            null_profit[t] = np.nan
        advanced_profit[t] = q_adv * r_new

        # Record the adopter state that actually drove returns[t],
        # demand[t], null_profit[t], and advanced_profit[t]. This must
        # happen BEFORE the end-of-period transition, otherwise adoption
        # plots and A* thresholds end up one period ahead of the outcomes
        # they bin. Edge case: with adoption_pi = 1, returns[0] is
        # generated under zero adoption, so adoption_share[0] must be 0.
        adoption_share[t] = adoption.mean()

        if t < adoption_start_t:
            continue

        if using_stochastic:
            adoption = adoption_mod.stochastic_diffusion_step(
                adoption, adoption_pi, adoption_delta, adoption_rng
            )
        elif using_switching and t >= switching_window - 1:
            start = t - switching_window + 1
            seg_null = null_profit[start : t + 1]
            seg_adv = advanced_profit[start : t + 1]
            # nan-safe: null_profit is NaN at periods where every trader is
            # an adopter (no non-adopter representative). The CE statistics
            # then skip those entries instead of poisoning the whole window.
            # When the entire window is NaN (full adoption throughout the
            # window) the score is NaN and the logistic switch step at full
            # adoption is a no-op anyway.
            seg_null_finite = seg_null[np.isfinite(seg_null)]
            if seg_null_finite.size > 0:
                ce_null = float(seg_null_finite.mean() - 0.5 * switching_a * seg_null_finite.var())
            else:
                ce_null = float("nan")
            ce_adv = float(seg_adv.mean() - 0.5 * switching_a * seg_adv.var())
            score = ce_adv - ce_null
            switching_score[t] = score
            adoption = adoption_mod.performance_switching_step(
                adoption, score, switching_alpha, switching_beta, adoption_rng
            )

    return {
        "prices": prices,
        "returns": returns,
        "demand": demand,
        "forecasts": forecasts,
        "adoption_share": adoption_share,
        "null_profit": null_profit,
        "advanced_profit": advanced_profit,
        "switching_score": switching_score,
    }
