# Reflexive Forecast Adoption in a Single-Asset Market

A capstone project that builds a small agent-based market and studies how
adoption of a shared autoregressive forecasting rule affects three distinct
quantities: realised-return predictive performance, residual predictive content
after removing contemporaneous price impact, and net trading value relative to
a null benchmark.

The simulator identifies a **dual-channel result**: adoption of the shared
forecast erodes residual predictive content (the forecast loses its grip on the
underlying return process) while simultaneously amplifying realised-return
performance and per-trade P&L (adopter demand pushes realised returns in the
forecast direction). Economic value does not visibly erode in the cost-free
baseline, and transaction costs shift profit levels but do not reverse the
adoption-amplification pattern in the regimes tested.

The full research proposal is in
[`docs/proposal/reflexive_forecast_proposal_v3.pdf`](docs/proposal/reflexive_forecast_proposal_v3.pdf).
The working agreement and the phased implementation plan are in
[`CLAUDE.md`](CLAUDE.md). All seven phases are implemented.

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
6. Parameter sweep and relative residual-erosion thresholds `A*_{R2,resid,rel}` and `A*_{phi,rel}`
7. Evaluation and the transaction-cost extension; reports `A*_{profit}` against zero (absolute) and against the null benchmark (proposal's primary economic endpoint)

See `CLAUDE.md` for what each phase delivers and the order of construction, and
section 4 of the proposal for the endpoint definitions.
