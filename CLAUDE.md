# CLAUDE.md

This file gives the working agreement for building the project described in
`docs/proposal/reflexive_forecast_proposal_v2.pdf`. Read the proposal first.
Everything below exists to make that proposal implementable in clean stages.

## What we are building

A single-asset agent-based market that tests one mechanism: when a shared
autoregressive forecast is adopted by more and more traders, does the forecast
lose predictive and economic value because adopter trades crowd the predictable
component out of next-period returns?

The market combines two well-known building blocks from the heterogeneous-agent
literature. Trader demand is mean-variance with constant absolute risk aversion,
following Brock and Hommes (1998). Price formation is a risk-neutral market
maker that absorbs net order flow, following Beja and Goldman (1980) and Farmer
and Joshi (2002). The headline summary statistic is the critical adoption share
A*, the smallest adoption level at which the rule stops paying off out of
sample.

## Repository layout

```
docs/proposal/      the proposal PDF and any short design notes
notebooks/          one notebook per phase, parameters at the top
src/reflexive_market/   small pure-numpy modules that notebooks import
tests/              pytest invariants, kept minimal
results/figures/    saved plots, named by phase
results/data/       small npz summaries
.github/workflows/  one CI workflow that runs pytest
```

Each `src/` module maps to a small slice of the proposal:

| Module        | What it implements                              | Proposal eqs |
|---------------|-------------------------------------------------|--------------|
| `market.py`   | aggregate demand, price update, return law      | (4), (5), (6) |
| `traders.py`  | null random rule, demand mapping with cap       | (1), (2), (3), (8) |
| `forecast.py` | rolling AR(p) fit and out-of-sample forecast    | (9), (10) |
| `adoption.py` | stochastic diffusion, CE-based switching        | (11)-(15) |
| `metrics.py`  | MSFE, OOS R^2, effective phi, sync, A*          | section 4 |
| `simulate.py` | one function that runs T steps end to end       | section 3.6 timing |

## Implementation phases

Phases are strictly ordered. Do not start phase N until phase N-1 runs end to
end and is committed. This is the same staging used in section 5 of the
proposal.

### Phase 1: baseline market with null traders only
Implements equations (1), (2), (4), (5), (6), (7), (8). Every trader uses the
random null rule. The notebook runs the simulator, plots a sample price path
and return series, and confirms the empirical AR(1) coefficient of returns
matches the input phi within sampling error.

Notebook: `notebooks/phase_01_baseline_market.ipynb`
Done when: a single seed produces a clean price path, return series, and a
return histogram that looks roughly Gaussian, and the empirical lag-1
autocorrelation is close to phi.

### Phase 2: benchmark validation
No AR rule, no adoption. Runs the simulator across many seeds. Shows that the
descriptive statistics (mean, variance, lag-1 autocorrelation, kurtosis) are
stable across seeds, and that a rolling estimate of the effective AR
coefficient does not drift over time.

Notebook: `notebooks/phase_02_benchmark_validation.ipynb`
Done when: per-seed statistics cluster tightly and the rolling effective phi
estimate is flat in expectation. This is the no-adoption, no-drift control we
need before any erosion claim is meaningful.

### Phase 3: AR forecasting rule, no adoption yet
Adds rolling AR fitting in `forecast.py`. Runs the null market, then fits the
forecast offline against realised returns and reports rolling MSFE and rolling
out-of-sample R^2 for w in {50, 100, 250}. No trader uses the forecast yet;
this phase only checks that the rule recovers a small positive R^2 driven by
the phi term.

Notebook: `notebooks/phase_03_ar_forecast.ipynb`
Done when: rolling out-of-sample R^2 is positive and stable, and longer windows
give lower variance estimates of the AR coefficient.

### Phase 4: forecast-based trading and stochastic adoption
Adopters now trade per equations (1) and (3). Adoption follows the stochastic
diffusion in (11) and (12). Compares three regimes: zero adoption, slow
diffusion, fast diffusion. The headline plot shows rolling out-of-sample R^2
versus adoption share, and rolling effective phi versus adoption share, on the
same x-axis. This is the first phase where the central mechanism becomes
visible.

Notebook: `notebooks/phase_04_stochastic_adoption.ipynb`
Done when: at high adoption shares, the rolling out-of-sample R^2 is visibly
lower than at low adoption shares, with effective phi shrinking in step.

### Phase 5: risk-adjusted performance-based adoption
Replaces the diffusion rule with the certainty-equivalent switching rule in
(13), (14), (15). Compares against phase 4 to see whether endogenous switching
accelerates or dampens erosion.

Notebook: `notebooks/phase_05_performance_adoption.ipynb`
Done when: the comparison plot makes the difference between exogenous and
endogenous adoption clear.

### Phase 6: experiments and the critical adoption share A*
Sweeps mu, phi, and the rolling window length w. For each combination, finds
the smallest adoption share at which out-of-sample R^2 crosses zero or net
profit crosses zero. Produces two heatmaps and a small summary table. This is
the compact headline result of the project.

Notebook: `notebooks/phase_06_experiments_threshold.ipynb`
Done when: the heatmaps tell a coherent story about which parameter
combinations make the forecast self-eroding and which do not.

### Phase 7: evaluation and one extension
Summarises primary findings, reports the diagnostics in section 4.2 of the
proposal, and adds one extension from section 3.7. The natural choice is
transaction costs, since it directly tests whether statistical erosion shows up
economically. A second optional extension is heterogeneous trader ecology
(trend followers and contrarians replacing the random null), if time allows.

Notebook: `notebooks/phase_07_evaluation_extensions.ipynb`
Done when: the report cell at the top of the notebook clearly states which
findings are core, which are robustness, and what the boundary conditions of
the mechanism are.

## Notebook conventions

Every notebook follows the same skeleton.

1. **Title cell** in markdown: phase number, one-line goal, link to the
   relevant proposal section.
2. **Parameters cell** in code: a single block at the top containing every
   knob the notebook uses, with a short comment for each. This is the only
   place numeric values should appear. Changing a parameter and re-running
   should be enough to see a different variation.
3. **Imports cell**: numpy, matplotlib, and the local package only. No pandas,
   scipy, statsmodels, or sklearn unless a phase clearly justifies it.
4. **Setup cell**: build a `numpy.random.default_rng(seed)` and any derived
   constants.
5. **Run cell**: call `simulate.run(...)` once. Keep this short.
6. **Metrics cell**: compute the metrics this phase cares about.
7. **Plots cells**: one figure per concept. Plain English in titles, axis
   labels, and legends.
8. **Save cell**: save figures to `results/figures/phase_NN_<name>.png` and
   any small numeric summaries to `results/data/phase_NN_<name>.npz`.

Cells stay short. One idea per cell. No hidden state across notebooks.

## Code conventions

- Pure numpy for math. Use `np.linalg.lstsq` for AR fitting.
- All randomness goes through a `numpy.random.Generator` passed in as an
  argument. Never call `np.random.<...>` at module level.
- Functions in `src/` are small, deterministic given the seed, and never plot
  or print.
- No pandas, scipy, statsmodels, or sklearn anywhere in `src/`. Notebooks may
  use them only if a clear need shows up.
- No em dashes anywhere, in code, comments, markdown, or notebooks. Use
  commas, colons, periods, or parentheses instead.
- Default to no comments. Add one only when the why is non-obvious.
- No unused imports. No commented-out code. No print statements left behind.

## Reproducibility

- Every notebook has a `seed` parameter in the parameters cell.
- Every figure filename includes the phase number and a short name. Same
  seed and same parameters produce the same figure.
- Small numeric outputs are saved as `.npz` so a reader can reproduce a
  table without rerunning the whole notebook.

## Intra-period timing

The proposal fixes a strict order of events inside each period (section 3.6).
The simulator must follow it exactly.

1. Agents observe returns up to and including period t and form forecasts.
2. Adopters and non-adopters submit orders for period t.
3. The market maker absorbs aggregate demand and moves the quote immediately.
4. The exogenous news shock and the residual autoregressive term realise.

Forecast success is evaluated against the residual return remaining after the
contemporaneous demand impact. Do not change this ordering when adding new
features.

## What not to do at this stage

- Do not introduce machine-learning forecasters before phase 7.
- Do not add transaction costs to the baseline. They are an extension in
  phase 7.
- Do not add multiple assets. This is single-asset only.
- Do not refactor `src/` for premature generality. Keep modules small until a
  second use case shows up.
- Do not add features the current phase does not need. Stay disciplined.

## How to work on a phase

1. Open the phase's notebook in `notebooks/`.
2. If `src/` modules need new functions, add them with the smallest possible
   signature. Keep them pure-numpy and deterministic given the seed.
3. Run the notebook end to end. Confirm the "done when" condition above.
4. Save figures and data summaries to `results/`.
5. Commit with a message like `phase 3: rolling AR forecast and OOS R^2`.
6. Open the next phase only after the current one is committed.
