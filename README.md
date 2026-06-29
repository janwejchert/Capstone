# Reflexive Forecast Adoption in a Single-Asset Market

A capstone project that builds a small agent-based market and studies how
adoption of a shared autoregressive forecasting rule affects two distinct
quantities: realised-return predictive performance (the metric a deployed
forecaster actually sees) and the independent demand-adjusted signal (a
counterfactual that strips out the contemporaneous self-fulfilment channel). A
third quantity, net trading value relative to a null benchmark, was an intended
economic endpoint; the cost and profit analysis behind it was attempted but not
fully conducted and is left for future work.

The simulator identifies a **dual-channel result**: adoption *raises*
realised-return predictive performance through the self-fulfilment channel
(adopter demand pushes realised returns in the forecast direction) while
*reducing* the independent demand-adjusted signal that the forecast was
originally designed to exploit. The economic endpoint (net trading value under
transaction costs) is left for future work: the analysis was attempted but, with
the null-relative comparison confounded by the position-size asymmetry between
the sigma_q-sized null rule and the capped adopter rule, was not carried far
enough to report as a settled result.

The full research proposal is in
[`docs/proposal/reflexive_forecast_proposal_v4.pdf`](docs/proposal/reflexive_forecast_proposal_v4.pdf).
The working agreement and the phased implementation plan are in
[`CLAUDE.md`](CLAUDE.md). All seven phase notebooks exist; phases 1 to 6 are
reported, and the phase 7 transaction-cost extension is left for future work.

## Findings (one paragraph)

Across phases 4 to 6 of the implemented simulator the dual-channel result holds robustly. In the fast-diffusion regime, rolling out-of-sample R^2 against realised returns reaches ~0.19 at full adoption, against ~0.07 for the zero-adoption control on the same shocks (self-fulfilment); the same forecast's R^2 against the demand-adjusted return `x = r - mu D` falls to ~0.04, against ~0.08 under the control (independent-signal erosion); and the rolling effective AR coefficient rises to ~0.45, against ~0.28 under the control (the mechanical cause of the demand-adjusted decline). Across the phase 6 sweep of `(mu, phi, w, p)` cells the target-specific A* values disagree by design: `A*_{R2,da,rel}` is reached in roughly half the grid at a mean adoption share of ~0.27, while `A*_{R2,realised,rel}` is reached in only ~26% of cells and always at very low A (mean ~0.07, max ~0.24). The realised-A* hits are noise crossings inside the weak-signal corner of the grid, not real erosion: when the baseline realised R^2 is already near zero, the half-baseline threshold sits at zero and rolling noise can satisfy it spuriously. The substantive finding is that realised R^2 does not systematically erode under adoption, in contrast to the demand-adjusted channel which does. The transaction-cost extension and its economic endpoint (`A*_{profit}`, adopter net trading value against the null benchmark) were attempted but not fully conducted: the null-relative comparison is confounded by the position-size asymmetry between the uncapped null rule and the capped adopter rule, which a faithful economic reading must first neutralise, so the cost and profit analysis is left for future work. The one-line summary is therefore: adoption raises realised-return predictive performance through the self-fulfilment channel while reducing the independent demand-adjusted signal.

## Quick start

```
pip install -r requirements.txt
pip install -e .
jupyter notebook notebooks/
```

The second command installs the local `reflexive_market` package so the
notebooks can import it. Open the phase you want to run. Each notebook starts
with a parameters cell you can edit to explore variations.

To run the tests:

```
pytest -q
```

## Layout

```
docs/proposal/      proposal PDF and design notes
notebooks/          one notebook per phase
src/reflexive_market/   pure-numpy simulation modules
tests/              pytest invariants
results/            saved figures and data summaries
```

## Phases (notebooks 1 to 7 exist; 1 to 6 reported, 7 deferred to future work)

1. Baseline market with null traders only
2. Benchmark validation across seeds
3. Rolling AR forecasting rule, no adoption
4. Forecast-based trading with stochastic adoption (the dual-channel result first appears here)
5. Risk-adjusted performance-based adoption (CE-rule switching, on paired shocks)
6. Parameter sweep and relative demand-adjusted-erosion thresholds `A*_{R2,da,rel}` and `A*_{phi,rel}`; `A*_{R2,realised}` is mostly not reached, with the finite hits being weak-signal noise crossings rather than systematic erosion
7. Evaluation and an attempted extension; the transaction-cost extension and its economic endpoint (`A*_{profit}`) were attempted but not fully conducted (the null-relative comparison is confounded by position-size asymmetry between the uncapped null rule and the capped adopter rule) and are left for future work

See `CLAUDE.md` for what each phase delivers and the order of construction, and
section 4 of the proposal for the endpoint definitions.
