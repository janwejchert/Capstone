# CLAUDE.md

This file gives the working agreement for building the project described in
`docs/proposal/reflexive_forecast_proposal_v4.pdf`. Read the proposal first.
Everything below exists to make that proposal implementable in clean stages.

## What we are building

A single-asset agent-based market that studies how adoption of a shared
autoregressive forecast affects three distinct quantities: realised-return
predictive performance (the metric a deployed forecaster sees), independent
demand-adjusted signal (counterfactual stripping out contemporaneous price
impact), and net trading value relative to a null benchmark. The proposal
anticipates and the implemented simulator confirms a **dual-channel result**:
adoption *raises* realised-return R^2 (self-fulfilling channel) while *lowering*
demand-adjusted R^2 (demand-adjusted-erosion channel) on the same path, and
mean adopter profit grows with adoption in the cost-free baseline. The
null-relative economic endpoint is confounded by position-size asymmetry
(the null rule trades ~sigma_q while adopters are capped at q_cap, so the
null books larger own-impact paper profit at c = 0 and a larger cost bill
at c > 0); phase 7 reports it with that caveat.

The market combines two well-known building blocks from the heterogeneous-agent
literature. Trader demand is mean-variance with constant absolute risk aversion,
following Brock and Hommes (1998). Price formation is a risk-neutral market
maker that absorbs net order flow, following Beja and Goldman (1980) and Farmer
and Joshi (2002). The compact summary statistics are the target-specific
critical adoption shares from section 4.3 of the proposal:
`A*_{R2,realised}` (mostly not reached; the finite hits are weak-signal noise
crossings rather than systematic erosion), `A*_{R2,da}` (demand-adjusted erosion of the independent signal),
`A*_{profit}` (economic endpoint), and the optional `A*_{vol}` (volatility
threshold). In the cost-free baseline `A*_{R2,da}` never reaches an absolute
zero crossing, so phase 6 reports a pre-registered relative analogue
`A*_{R2,da,rel}` (half the low-adoption baseline) plus the analogous
`A*_{phi,rel}` on the effective AR coefficient diagnostic. Note that the
demand-adjusted return `x_{t+1} = r_{t+1} - mu D_t` is a counterfactual that
removes contemporaneous price impact only; it is *not* the full regression
residual, which would be `sigma eps = r_{t+1} - phi r_t - mu D_t`.

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
| `traders.py`  | null random rule, demand mapping with cap       | (1), (2), (3), (9) |
| `forecast.py` | rolling AR(p) fit and out-of-sample forecast    | (10), (11) |
| `adoption.py` | stochastic diffusion, CE-based switching        | (12)-(15) |
| `metrics.py`  | MSFE, OOS R^2 (realised and demand-adjusted), effective phi | section 4 |
| `simulate.py` | one function that runs T steps end to end       | section 3.6 timing |

## Implementation phases

Phases are strictly ordered. Do not start phase N until phase N-1 runs end to
end and is committed. This is the same staging used in section 5 of the
proposal.

### Phase 1: baseline market with null traders only
Implements equations (1), (2), (4), (5), (6), (8), (9). Every trader uses the
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
diffusion in (12) and (13). Compares three regimes: zero adoption, slow
diffusion, fast diffusion. Headline plots show the rolling OOS R^2 against the
realised return and against the demand-adjusted return, side by side, plus
rolling effective phi versus adoption share. This is the first phase where the
dual-channel result becomes visible.

Notebook: `notebooks/phase_04_stochastic_adoption.ipynb`
Done when: at high adoption shares, the rolling OOS R^2 against realised
returns is visibly higher than at low adoption (self-fulfilling channel) while
the rolling OOS R^2 against demand-adjusted returns is visibly lower
(demand-adjusted-erosion channel), with effective phi rising in step.

### Phase 5: risk-adjusted performance-based adoption
Replaces the diffusion rule with the certainty-equivalent switching rule in
(14) and (15). Compares against phase 4 on the demand-adjusted-channel R^2
and effective-phi diagnostics (paired shocks) to see whether endogenous
switching follows the same underlying erosion path as exogenous diffusion.

Notebook: `notebooks/phase_05_performance_adoption.ipynb`
Done when: the comparison plot makes the difference between exogenous and
endogenous adoption clear, and both regimes display the demand-adjusted-R^2
decline and effective-phi amplification pattern.

### Phase 6: experiments and the relative demand-adjusted-erosion thresholds
Sweeps mu, phi, rolling window length w, and AR order p (p = 1 baseline; p
in {2, 5, 10} robustness). For each (p, w, phi, mu) cell, locates the relative
analogues of the proposal's target-specific A* values in the cost-free
baseline. Two relative thresholds are reported: `A*_{R2,da,rel}`, the
smallest A at which the rolling demand-adjusted R^2 has fallen to half its
low-adoption baseline; and `A*_{phi,rel}`, the smallest A at which effective
phi has grown to 1.5x its baseline. The realised-return threshold
`A*_{R2,realised}` is mostly not reached; the finite hits are weak-signal
noise crossings rather than systematic realised-R^2 erosion. Produces AR(1) headline heatmaps, by-p
robustness grids, a delta-from-AR(1) heatmap, and a representative
erosion-path figure.

Notebook: `notebooks/phase_06_experiments_threshold.ipynb`
Done when: the AR(1) heatmaps populate the bulk of the (mu, phi) grid, larger
mu deepens the high-adoption demand-adjusted erosion and pulls the
effective-phi threshold `A*_{phi,rel}` earlier (the `A*_{R2,da,rel}` crossing
itself is roughly flat in mu because the relative threshold scales with the
baseline), and the by-p robustness grids demonstrate the mechanism is not
specific to AR(1).

### Phase 7: evaluation and one extension
Summarises primary findings under the dual-channel framing, reports the
diagnostics in section 4.2 of the proposal, and adds the transaction-cost
extension from section 3.7. Holds AR order at p = 1 to remain on the proposal's
baseline rule. Reports two views of `A*_{profit}`: an absolute view (smallest
A at which adopter net profit crosses zero; in this regime a from-below
profitability onset, the reverse of the proposal's from-above erosion
reading) and the null-relative view that is the proposal's primary economic
endpoint (read it with the null self-impact and position-size caveats stated
in the notebook). A second optional extension is
heterogeneous trader ecology (trend followers and contrarians replacing the
random null), if time allows.

Notebook: `notebooks/phase_07_evaluation_extensions.ipynb`
Done when: the report cell at the top of the notebook clearly states which
findings are core, which are robustness, and what the boundary conditions of
the dual-channel mechanism are.

## Notebook conventions

Every notebook follows the same skeleton.

1. **Title cell** in markdown: phase number, one-line goal, link to the
   relevant proposal section.
2. **Parameters cell** in code: a single block at the top containing every
   knob the notebook uses, with a short comment for each. This is the only
   place numeric values should appear. Changing a parameter and re-running
   should be enough to see a different variation.
3. **Imports cell**: starts with two lines that prepend `../src` to `sys.path`
   so the local checkout imports win even if an older `reflexive_market` is
   already installed in the kernel. Then numpy, matplotlib, and the local
   package only. No pandas, scipy, statsmodels, or sklearn unless a phase
   clearly justifies it.

   ```
   import sys
   sys.path.insert(0, "../src")

   import numpy as np
   import matplotlib.pyplot as plt
   from reflexive_market import simulate
   ```
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
4. The exogenous news shock and the autoregressive term realise.

Forecast success is evaluated against two distinct targets and both readings
are reported: the realised return `r_{t+1}` (self-fulfilling channel) and the
demand-adjusted return `x_{t+1} = r_{t+1} - mu D_t = phi r_t + sigma eps_{t+1}`
(demand-adjusted-erosion channel). The demand-adjusted return is a
counterfactual, not the full regression residual (which would be
`sigma eps = r_{t+1} - phi r_t - mu D_t`). Do not change this ordering when
adding new features.

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
