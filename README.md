# Reflexive Forecast Adoption in a Single-Asset Market

A capstone project that builds a small agent-based market and studies how
adoption of a shared autoregressive forecasting rule affects three distinct
quantities: realised-return predictive performance (the metric a deployed
forecaster actually sees), independent demand-adjusted signal (a counterfactual
that strips out the contemporaneous self-fulfilment channel), and net trading
value relative to a null benchmark.

The simulator identifies a **dual-channel result**: adoption *raises*
realised-return predictive performance through the self-fulfilment channel
(adopter demand pushes realised returns in the forecast direction) while
*reducing* the independent demand-adjusted signal that the forecast was
originally designed to exploit. Mean adopter profit grows with adoption in the
cost-free baseline, and transaction costs shift profit levels but do not
reverse that pattern in the regimes tested. The proposal's null-relative
economic endpoint is dominated by the position-size asymmetry between the
sigma_q-sized null rule and the capped adopter rule (see phase 7).

The full research proposal is in
[`docs/proposal/reflexive_forecast_proposal_v4.pdf`](docs/proposal/reflexive_forecast_proposal_v4.pdf).
The working agreement and the phased implementation plan are in
[`CLAUDE.md`](CLAUDE.md). All seven phases are implemented.

## Findings (one paragraph)

Across phases 4 to 7 of the implemented simulator the dual-channel result holds robustly. In the fast-diffusion regime, rolling out-of-sample R^2 against realised returns reaches ~0.19 at full adoption, against ~0.07 for the zero-adoption control on the same shocks (self-fulfilment); the same forecast's R^2 against the demand-adjusted return `x = r - mu D` falls to ~0.04, against ~0.08 under the control (independent-signal erosion); and the rolling effective AR coefficient rises to ~0.45, against ~0.28 under the control (the mechanical cause of the demand-adjusted decline). Across the phase 6 sweep of `(mu, phi, w, p)` cells the target-specific A* values disagree by design: `A*_{R2,da,rel}` is reached in roughly half the grid at a mean adoption share of ~0.27, while `A*_{R2,realised,rel}` is reached in only ~26% of cells and always at very low A (mean ~0.07, max ~0.24). The realised-A* hits are noise crossings inside the weak-signal corner of the grid, not real erosion: when the baseline realised R^2 is already near zero, the half-baseline threshold sits at zero and rolling noise can satisfy it spuriously. The substantive finding is that realised R^2 does not systematically erode under adoption, in contrast to the demand-adjusted channel which does. In the phase 7 transaction-cost extension, adopter mean profit grows with adoption at every tested cost level; the absolute `A*_{profit,abs}` crossing exists only in the c ~ 0.003 to 0.004 band, and it is a from-below profitability onset (the rule starts paying once adoption is high enough), the reverse of the proposal's from-above erosion reading. The null-relative endpoint is dominated by position-size asymmetry: at c = 0 the adopter sits slightly below the null benchmark at every observed adoption share, because a null trader books own-impact paper profit (E[null profit] = mu sigma_q^2 / N) on a position roughly 16x the adopter cap, and at every positive cost level the adopter sits uniformly above it because the null pays cost on that same larger position. The correct one-line summary is therefore: adoption raises realised-return predictive performance through the self-fulfilment channel while reducing the independent demand-adjusted signal; adopter profit is amplified rather than eroded in the cost-free baseline, with the null-relative comparison confounded by position size.

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

## Phases (all implemented)

1. Baseline market with null traders only
2. Benchmark validation across seeds
3. Rolling AR forecasting rule, no adoption
4. Forecast-based trading with stochastic adoption (the dual-channel result first appears here)
5. Risk-adjusted performance-based adoption (CE-rule switching, on paired shocks)
6. Parameter sweep and relative demand-adjusted-erosion thresholds `A*_{R2,da,rel}` and `A*_{phi,rel}`; `A*_{R2,realised}` is mostly not reached, with the finite hits being weak-signal noise crossings rather than systematic erosion
7. Evaluation and the transaction-cost extension; reports `A*_{profit}` against zero (absolute) and against the null benchmark (proposal's primary economic endpoint), with direction and null-self-impact caveats stated in the notebook

See `CLAUDE.md` for what each phase delivers and the order of construction, and
section 4 of the proposal for the endpoint definitions.
