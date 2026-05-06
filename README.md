# Reflexive Forecast Adoption in a Single-Asset Market

A capstone project that builds a small agent-based market and tests whether a
shared autoregressive forecast loses predictive and economic value as more
traders adopt it.

The full research proposal is in
[`docs/proposal/reflexive_forecast_proposal_v2.pdf`](docs/proposal/reflexive_forecast_proposal_v2.pdf).
The working agreement and the phased implementation plan are in
[`CLAUDE.md`](CLAUDE.md).

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

## Phases

1. Baseline market with null traders only
2. Benchmark validation across seeds
3. Rolling AR forecasting rule, no adoption
4. Forecast-based trading with stochastic adoption
5. Risk-adjusted performance-based adoption
6. Experiments and the critical adoption share A*
7. Evaluation and one extension (transaction costs)

See `CLAUDE.md` for what each phase delivers and the order of construction.
