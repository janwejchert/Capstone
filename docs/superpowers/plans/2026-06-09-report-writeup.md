# Capstone Report Writeup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fill in `docs/Report/report.tex` from a section/subsection skeleton to a complete, citation-backed, format-compliant final capstone report, one subsection at a time, with every quantitative claim traced to a source artifact.

**Architecture:** Bottom-up writing order (Results first, framing chapters last). Each subsection is a self-contained stage of work that ends with a commit. A shared four-point cross-check protocol gates every stage: numbers traced to `.npz` fields, definitions matched to proposal v4, figures verified against `results/figures/`, style pass (no em dashes, plain English).

**Tech Stack:** LaTeX (article class), `mathptmx` (Times Roman text and math), `natbib` + `plainnat` for citations, `graphicx` for figures, `amsmath`/`amssymb` for equations, BibTeX bibliography in `docs/Report/references.bib`. Source artifacts: `notebooks/phase_*.ipynb`, `results/data/phase_*.npz`, `results/figures/phase_*.png`, `docs/proposal/reflexive_forecast_proposal_v4.pdf`, `src/reflexive_market/*.py`.

---

## File Structure

**Modified throughout:**
- `docs/Report/report.tex`: the report itself, one subsection added per stage. The skeleton already exists with title page, abstract, and full section/subsection structure.
- `docs/Report/references.bib`: bibliography file, populated incrementally as each stage cites a source.

**Created in Stage 0:**
- `docs/Report/references.bib` (empty seed file with header comment).

**Read-only sources:**
- `docs/proposal/reflexive_forecast_proposal_v4.pdf`: the authoritative contract for symbols, endpoints, and definitions.
- `docs/proposal/reflexive_forecast_proposal_v4.tex`: the LaTeX source, useful for grabbing equation snippets and exact wording.
- `notebooks/phase_*.ipynb`: the analysis code that produced each figure and each `.npz` summary.
- `results/data/phase_*.npz`: quantitative summaries (field-level catalog at the bottom of this plan).
- `results/figures/phase_*.png`: saved figures (full list at the bottom of this plan).
- `src/reflexive_market/*.py`: implementation modules (~588 lines total across 7 files).
- `CLAUDE.md`: the working agreement and phased construction summary.

**Output:**
- `docs/Report/report.pdf`: compiled at the end of every stage; final read-through at Stage 28.

---

## Shared cross-check protocol

Every content stage ends with the same four checks. They are not optional. The stage is not "done" and is not committed until all four pass.

1. **Numbers traced.** Every quantitative claim in the prose carries an inline LaTeX comment with its source. Format: `% src: phase_06_a_star_grid.npz['a_star_R2_da']`, or `% src: notebooks/phase_04_stochastic_adoption.ipynb cell 12`. If a number is recalled and the source cannot be located, the number is removed until verified.
2. **Definitions match proposal v4.** Any symbol, endpoint, term, or equation reference is checked against `docs/proposal/reflexive_forecast_proposal_v4.pdf`. Disagreements are resolved (almost always: bring the report into line with the proposal).
3. **Figures verified.** For every `\includegraphics{...}`: confirm the file exists at `results/figures/<name>.png`, open the PNG, and confirm the surrounding prose accurately describes what the figure shows. Captions are written from the actual image, not from memory.
4. **Style pass.** No em dashes anywhere (use commas, colons, periods, parentheses). Plain English in body and captions. Compile the report, open the PDF, and skim the new subsection to catch rendering issues (broken refs, overfull boxes, math display issues).

The commit at the end of each stage uses the message format: `report: <subsection number> <subsection title>` (for example, `report: 6.3 dual-channel result under stochastic adoption`).

---

## Page-count control

The format cap is 30 pages and the target is ~22. The word budgets in the
spec total ~10,200 words of body text (roughly 21 to 22 pages at 12pt single
spacing), which leaves room for at most about 10 figures in the main text;
every other figure goes to Appendix B. Recommended main-text set: one figure
for 6.1, one for 6.2, two for 6.3 (`phase_04_oos_r2_vs_adoption_mc`,
`phase_04_phi_vs_adoption_mc`), one for 6.4 (`phase_05_erosion_vs_adoption`),
two or three for 6.5 (`phase_06_a_star_R2_heatmap`,
`phase_06_a_star_phi_heatmap`, optionally `phase_06_r2_da_heatmap`), and two
for 6.6. After committing each section group (Results, Model, Metrics,
Discussion, framing), compile and check the running page count; if it tracks
above 28 pages, trim Results prose and demote figures to Appendix B before
writing the next group.

---

## Stage 0: Format setup

**Files:**
- Modify: `docs/Report/report.tex` (preamble lines 1-35)
- Create: `docs/Report/references.bib`

**Goal:** Switch the document to 12pt Times Roman with 1.0 line spacing and natbib citations before any prose is written, so every subsequent stage compiles directly into the final format.

- [x] **Step 1: Open report.tex preamble and inspect current state**

Run: `head -36 docs/Report/report.tex`
Expected: confirms `\documentclass[11pt]{article}`, `\usepackage{XCharter}`, `\setlength{\parskip}{0.55em}`, `\setlength{\parindent}{0pt}`.

- [x] **Step 2: Change document class to 12pt**

Edit `docs/Report/report.tex` line 1:

```latex
\documentclass[12pt]{article}
```

- [x] **Step 3: Replace XCharter with Times Roman (text and math)**

Edit `docs/Report/report.tex` line 5 (XCharter line). Replace:

```latex
\usepackage{XCharter}
```

with:

```latex
\usepackage{mathptmx}
```

- [x] **Step 4: Switch to traditional indented paragraph style with 1.0 spacing**

Edit `docs/Report/report.tex` lines 32-33 (parskip/parindent). Replace:

```latex
\setlength{\parskip}{0.55em}
\setlength{\parindent}{0pt}
```

with:

```latex
\linespread{1.0}
\setlength{\parskip}{0pt}
\setlength{\parindent}{1em}
```

- [x] **Step 5: Add natbib and bibliography style to preamble**

Add after the `\usepackage{hyperref}` line (around line 17):

```latex
\usepackage{natbib}
\bibliographystyle{plainnat}
```

- [x] **Step 6: Create the empty references.bib seed file**

Create `docs/Report/references.bib` with:

```bibtex
% Bibliography for the capstone report.
% Entries are added incrementally as each subsection cites a source.
% Use natbib's \citet{key} for inline author citations and \citep{key} for parenthetical.
```

- [x] **Step 7: Add \bibliography command at the bottom of report.tex**

Find the existing `\section*{References}` line (around line 180) and replace it with:

```latex
\bibliography{references}
```

(natbib will generate the References heading automatically.)

- [x] **Step 8: Compile and verify the test PDF renders cleanly**

Run from `docs/Report/`:

```bash
cd docs/Report && pdflatex -interaction=nonstopmode report.tex && bibtex report && pdflatex -interaction=nonstopmode report.tex && pdflatex -interaction=nonstopmode report.tex
```

Open `docs/Report/report.pdf`. Verify:
- Body text is visibly Times Roman (serifs, classic proportions).
- Title page renders with the IE logo and your full name (Jan Jacek Wejchert).
- Abstract is present.
- TOC shows all sections.
- No compile errors (BibTeX may warn "no bibliography", acceptable while references.bib is empty).

- [x] **Step 9: Commit**

```bash
git add docs/Report/report.tex docs/Report/references.bib
git commit -m "report: format setup (12pt Times, 1.0 spacing, natbib)"
```

---

## RESULTS: Section 6

The Results section is written first because the numbers are concrete and frozen in the `.npz` files. Doing this first locks in what every later section must cite accurately.

### Stage 1: §6.1 Baseline market and benchmark validation (phases 1 and 2)

**Files:**
- Modify: `docs/Report/report.tex` (insert prose under `\subsection{Baseline market and benchmark validation (phases 1 and 2)}`)

**Word budget:** ~400 words plus 2 figures.

**Source artifacts:**
- `notebooks/phase_01_baseline_market.ipynb`
- `notebooks/phase_02_benchmark_validation.ipynb`
- `results/data/phase_01_baseline.npz`, fields: `prices` (5001,), `returns` (5000,), `demand` (5000,), `phi_input`, `phi_empirical`, `seed`
- `results/data/phase_02_benchmark.npz`, fields: `mean_per_seed` (100,), `std_per_seed` (100,), `rho_per_seed` (100,), `kurt_per_seed` (100,), `mean_phi_trace` (5000,), `std_phi_trace` (5000,), `phi_input`, `rolling_window`, `seeds`
- `results/figures/phase_01_price_path.png`, `phase_01_return_series.png`, `phase_01_return_histogram.png`
- `results/figures/phase_02_rolling_phi.png`, `phase_02_seed_mean.png`, `phase_02_seed_std.png`, `phase_02_seed_lag1.png`, `phase_02_seed_kurtosis.png`

- [ ] **Step 1: Read the source notebooks' parameters cells and report cells**

Open both phase 01 and phase 02 notebooks. Note the parameters (`N`, `T`, `phi`, `sigma`, seed values, rolling window length). Note what each notebook concludes in its final markdown cell.

- [ ] **Step 2: Load the .npz summaries and confirm the numbers you will cite**

Run:

```bash
python3 -c "
import numpy as np
d1 = np.load('results/data/phase_01_baseline.npz')
d2 = np.load('results/data/phase_02_benchmark.npz')
print('phi_input vs phi_empirical:', d1['phi_input'], d1['phi_empirical'])
print('mean_per_seed stats:', d2['mean_per_seed'].mean(), d2['mean_per_seed'].std())
print('rho_per_seed stats:',  d2['rho_per_seed'].mean(),  d2['rho_per_seed'].std())
print('rolling phi flatness: range over time:', d2['mean_phi_trace'].max() - d2['mean_phi_trace'].min())
"
```

Record the output. These are the numbers the subsection will cite.

- [ ] **Step 3: Draft the prose (target ~400 words)**

Two paragraphs. First paragraph describes phase 1: null-trader baseline, the AR(1) input parameter `phi_input`, the empirical lag-1 autocorrelation matches within sampling error, returns look roughly Gaussian. Second paragraph describes phase 2: stability of per-seed descriptive stats (mean, std, lag-1 autocorrelation, kurtosis) across the 100-seed sweep, and the absence of drift in the rolling effective `phi` estimate over T=5000 steps. End with the role of this section: this is the no-adoption, no-drift control needed before any erosion claim is meaningful.

Insert into `report.tex` at `\subsection{Baseline market and benchmark validation (phases 1 and 2)}`. Use inline source comments on each numeric claim.

- [ ] **Step 4: Add two figures**

Choose the two strongest. Recommended:
- `phase_01_return_histogram.png` (shows null-trader return distribution).
- `phase_02_rolling_phi.png` (shows no drift in the rolling `phi` estimate over time, the central control claim).

Add via:

```latex
\begin{figure}[h]
\centering
\includegraphics[width=0.78\textwidth]{../../results/figures/phase_01_return_histogram.png}
\caption{Histogram of one-step returns in the null-trader baseline, T=5000 steps, seed [value]. The bell shape confirms a roughly Gaussian return distribution; the empirical lag-1 autocorrelation is [value], matching the input $\phi=[value]$ within sampling error.}
\label{fig:phase01-hist}
\end{figure}
```

Fill the bracketed values from Step 2's output. Same shape for the second figure.

- [ ] **Step 5: Add citation entries for proposal section references**

The subsection should reference proposal section 3.1 (market) and section 3.3 (null rule). No external citations needed in this subsection beyond the proposal itself.

- [ ] **Step 6: Compile and check rendering**

Run the four-command pdflatex sequence from Stage 0 Step 8. Open the PDF and verify the new subsection prose, both figures, captions, and cross-refs render cleanly.

- [ ] **Step 7: Cross-check protocol**

  - [ ] **Numbers traced:** every numeric claim has an inline `% src:` comment pointing to a specific `.npz` field or notebook cell.
  - [ ] **Definitions match proposal v4:** `phi`, `r_t`, `D_t`, "null rule" terminology consistent with proposal section 3.1-3.2.
  - [ ] **Figures verified:** both PNG files exist at the cited paths; captions describe what is actually in the image (open and look).
  - [ ] **Style pass:** no em dashes; plain English; PDF compiles cleanly.

- [ ] **Step 8: Commit**

```bash
git add docs/Report/report.tex
git commit -m "report: 6.1 baseline market and benchmark validation"
```

---

### Stage 2: §6.2 AR forecast performance without adoption (phase 3)

**Files:**
- Modify: `docs/Report/report.tex` under `\subsection{AR forecast performance without adoption (phase 3)}`

**Word budget:** ~400 words plus 2 figures.

**Source artifacts:**
- `notebooks/phase_03_ar_forecast.ipynb`
- `results/data/phase_03_ar_forecast.npz`, fields: `summary` (3, 5), `ar_windows` (3,) typically `[50, 100, 250]`, `ar_order`, `eval_window`, `phi_input`, `seed`
- `results/figures/phase_03_ar_coefficients.png`, `phase_03_rolling_msfe.png`, `phase_03_rolling_oos_r2.png`

- [ ] **Step 1: Open phase_03 notebook and inspect the structure of `summary`**

Open the notebook. Find the cell that builds the `summary` array and note what each of the 5 columns means (likely: window, mean MSFE, std MSFE, mean OOS R^2, std OOS R^2, or similar). Confirm by reading the cell text.

- [ ] **Step 2: Load .npz and extract the numbers**

```bash
python3 -c "
import numpy as np
d = np.load('results/data/phase_03_ar_forecast.npz')
print('ar_windows:', d['ar_windows'])
print('summary:')
print(d['summary'])
print('phi_input:', d['phi_input'], 'ar_order:', d['ar_order'])
"
```

Record the OOS R^2 by window length. These are the central numbers in the subsection.

- [ ] **Step 3: Draft the prose (target ~400 words)**

One paragraph on the setup (rolling AR(1) fit, no trader uses the forecast yet, simulate from the null market, then post-hoc evaluate the forecast on realised returns). One paragraph on the result: a small positive rolling OOS R^2 driven by the `phi` term, lower variance for longer windows, AR coefficient estimates that cluster near `phi_input`. End with the framing point: this confirms the rule recovers the linear-persistence signal before any adoption is introduced.

Insert into report.tex with inline source comments.

- [ ] **Step 4: Add figures**

Recommended:
- `phase_03_rolling_oos_r2.png`: central evidence (positive, stable, low for small windows).
- `phase_03_ar_coefficients.png`: shows AR coefficient estimates clustering around `phi_input`.

Same figure-block format as Stage 1.

- [ ] **Step 5: Compile and check rendering**

Same pdflatex sequence. Open PDF and verify.

- [ ] **Step 6: Cross-check protocol** (all four checks, as in Stage 1)

- [ ] **Step 7: Commit**

```bash
git add docs/Report/report.tex
git commit -m "report: 6.2 AR forecast performance without adoption"
```

---

### Stage 3: §6.3 Dual-channel result under stochastic adoption (phase 4)

**Files:**
- Modify: `docs/Report/report.tex` under `\subsection{Dual-channel result under stochastic adoption (phase 4)}`

**Word budget:** ~700 words plus 3 figures. This is the most important results subsection in the whole report: the dual-channel result first appears here.

**Source artifacts:**
- `notebooks/phase_04_stochastic_adoption.ipynb`
- `results/data/phase_04_stochastic_adoption.npz`, fields: `summary` (3, 8), `regime_pi` (3,), `regime_delta` (3,), `regime_names` (3,), likely `['zero', 'slow', 'fast']`, `phi_input`, `mu`, `risk_scale`, `q_cap`, `forecast_window`, `eval_window`, `T`, `N`, `seed`
- 9 figures in `results/figures/phase_04_*.png` (full list at bottom of plan).

- [ ] **Step 1: Open notebook and identify the 8 summary columns**

Open phase_04 notebook. Find the cell that builds the (3, 8) `summary` array. The 8 columns likely cover: regime name, regime adoption parameters, mean adoption share, OOS R^2 against realised at low vs high adoption, OOS R^2 against demand-adjusted at low vs high adoption, effective phi at low vs high adoption.

- [ ] **Step 2: Load the .npz and extract numbers per regime**

```bash
python3 -c "
import numpy as np
d = np.load('results/data/phase_04_stochastic_adoption.npz')
print('regimes:', d['regime_names'])
print('pi:', d['regime_pi'])
print('delta:', d['regime_delta'])
print('summary:')
print(d['summary'])
print('mu:', d['mu'], 'phi:', d['phi_input'])
"
```

Record the actual rolling OOS R^2 values at low and high adoption for both targets, plus the effective phi at low and high adoption. Anchor the low-adoption side to the zero-adoption control row (realised 0.0695, demand-adjusted 0.0821, phi 0.2821): the fast regime's own low window already averages adoption ~0.5, which is why the README quotes 0.07 to 0.19, 0.08 to 0.04, and 0.28 to 0.45 against the control rather than the ramp window.

- [ ] **Step 3: Draft the prose (target ~700 words)**

Suggested four paragraphs:

  1. **Setup.** Three adoption regimes (zero, slow, fast diffusion), parameter values `pi` and `delta`. Each regime runs the same simulator with the same seeds; adopters trade per equations (1) and (3) of the proposal, non-adopters use the null rule.
  2. **Realised-return channel.** As adoption rises (in the fast-diffusion regime), rolling OOS R^2 against realised returns climbs from ~[low] to ~[high]. State the mechanism in one sentence: coordinated adopter demand pushes realised returns in the forecast direction.
  3. **Demand-adjusted channel.** The same forecast's R^2 against the demand-adjusted return `x_{t+1} = r_{t+1} - mu D_t` falls from ~[low] to ~[high]. Re-state the definition of the demand-adjusted return inline so a reader can interpret the figure without flipping back.
  4. **Effective AR coefficient.** The rolling effective phi rises from ~[low] to ~[high], which is the mechanical cause of the demand-adjusted decline.

End with the one-line headline: adoption raises realised predictive performance through the self-fulfilment channel while reducing the independent demand-adjusted signal.

- [ ] **Step 4: Add two figures**

Recommended:
- `phase_04_oos_r2_vs_adoption_mc.png`: Monte Carlo dual-channel plot.
- `phase_04_phi_vs_adoption_mc.png`: effective phi rising with adoption.

The time-series view `phase_04_oos_r2_over_time.png` goes to Appendix B.

Same figure-block format as Stage 1. Captions describe what is *actually shown*, not what the prose says.

- [ ] **Step 5: Compile and check rendering**

Same pdflatex sequence.

- [ ] **Step 6: Cross-check protocol** (all four checks)

  - [ ] **Numbers traced:** every "from X to Y" claim points to a specific row/column of `summary` or a notebook cell.
  - [ ] **Definitions match proposal v4:** `x_{t+1} = r_{t+1} - mu D_t` is the demand-adjusted return, NOT the full regression residual (proposal section 3.6). Get this exactly right.
  - [ ] **Figures verified:** all three PNG files opened, captions accurate.
  - [ ] **Style pass:** no em dashes, plain English, compile clean.

- [ ] **Step 7: Commit**

```bash
git add docs/Report/report.tex
git commit -m "report: 6.3 dual-channel result under stochastic adoption"
```

---

### Stage 4: §6.4 Endogenous CE-based switching (phase 5)

**Files:**
- Modify: `docs/Report/report.tex` under `\subsection{Endogenous CE-based switching (phase 5)}`

**Word budget:** ~500 words plus 2 figures.

**Source artifacts:**
- `notebooks/phase_05_performance_adoption.ipynb`
- `results/data/phase_05_performance_adoption.npz`, fields: `summary` (2, 6), `regime_names` (2,), likely `['stochastic', 'CE-switching']`, `phi_input`, `mu`, `risk_scale`, `q_cap`, `forecast_window`, `eval_window`, `stochastic_pi`, `switching_window`, `switching_a`, `switching_alpha`, `switching_beta`, `T`, `N`, `seed`
- `results/figures/phase_05_adoption_share.png`, `phase_05_erosion_vs_adoption.png`, `phase_05_switching_score.png`

- [ ] **Step 1: Open notebook and inspect 6-column summary**

Open phase_05. Identify what the 6 columns of `summary` mean for the two regimes.

- [ ] **Step 2: Load .npz**

```bash
python3 -c "
import numpy as np
d = np.load('results/data/phase_05_performance_adoption.npz')
print('regimes:', d['regime_names'])
print('summary:')
print(d['summary'])
print('switching params: a=', d['switching_a'], 'alpha=', d['switching_alpha'], 'beta=', d['switching_beta'])
"
```

- [ ] **Step 3: Draft the prose (target ~500 words)**

Three paragraphs:
  1. The CE switching rule (proposal equations 13-15). Each agent compares forecast and null certainty-equivalent net of risk penalty and switches with logistic intensity.
  2. Paired-shock comparison against the fast stochastic regime: both regimes show the demand-adjusted R^2 decline and the effective-phi amplification, with quantitative comparisons from `summary`.
  3. Interpretive line: endogenous switching does not change the underlying erosion path, which means the dual-channel mechanism is not an artefact of exogenous diffusion.

- [ ] **Step 4: Add one figure**

Recommended:
- `phase_05_erosion_vs_adoption.png`: the central comparison.

`phase_05_switching_score.png` (the CE switching signal driving adoption)
goes to Appendix B.

- [ ] **Step 5: Compile and check rendering**

- [ ] **Step 6: Cross-check protocol** (all four checks)

- [ ] **Step 7: Commit**

```bash
git add docs/Report/report.tex
git commit -m "report: 6.4 endogenous CE-based switching"
```

---

### Stage 5: §6.5 Parameter sweep and critical adoption shares (phase 6)

**Files:**
- Modify: `docs/Report/report.tex` under `\subsection{Parameter sweep and critical adoption shares (phase 6)}`

**Word budget:** ~800 words plus 3-4 figures. This is the second-largest results subsection because the threshold analysis is dense.

**Source artifacts:**
- `notebooks/phase_06_experiments_threshold.ipynb`
- `results/data/phase_06_a_star_grid.npz`: fields (note the 4D shape: forecast_p × window × phi × mu):
  - Axes: `mu_grid` (5,), `phi_grid` (6,), `w_grid` (3,), `forecast_p_grid` (4,) = [1, 2, 5, 10]
  - Thresholds: `a_star_R2_realised`, `a_star_R2_da`, `a_star_phi` each (4, 3, 6, 5)
  - Hit rates: `hit_rate_R2_realised`, `hit_rate_R2_da`, `hit_rate_phi` each (4, 3, 6, 5)
  - Baselines: `baseline_R2_realised_grid`, `baseline_R2_da_grid`, `baseline_phi_grid`
  - Tail (high-adoption) values: `tail_R2_realised_grid`, `tail_R2_da_grid`
  - Line curves: `line_curve_adoption_share` (8000,), `line_curve_da_r2` (4, 8000), `line_curve_phi` (4, 8000)
  - Thresholds-of-thresholds: `r2_threshold_factor` (typically 0.5), `phi_threshold_factor` (typically 1.5), `min_hit_rate`
- 12 figures in `results/figures/phase_06_*.png` (full list at bottom of plan).

- [ ] **Step 1: Open notebook and confirm threshold definitions**

Re-read the cells that compute `a_star_R2_da_rel` and `a_star_phi_rel`. Confirm: `A*_{R2,da,rel}` is the smallest adoption share at which rolling DA R^2 has fallen to `r2_threshold_factor × baseline`, and `A*_{phi,rel}` is the smallest adoption share at which effective phi has grown to `phi_threshold_factor × baseline`.

- [ ] **Step 2: Load .npz and compute summary numbers**

```bash
python3 -c "
import numpy as np
d = np.load('results/data/phase_06_a_star_grid.npz')
# AR(1) slice = forecast_p_grid index 0
ar1 = 0
print('mu grid:', d['mu_grid'])
print('phi grid:', d['phi_grid'])
print('w grid:', d['w_grid'])
print('forecast_p grid:', d['forecast_p_grid'])
print('AR(1) A*_R2_da_rel grid (w=middle, all phi, all mu):')
print(d['a_star_R2_da'][ar1, 1])
print('hit rate R2_da AR(1):', d['hit_rate_R2_da'][ar1].mean())
print('hit rate R2_realised AR(1):', d['hit_rate_R2_realised'][ar1].mean())
print('mean A* R2_realised over hits AR(1):', np.nanmean(d['a_star_R2_realised'][ar1]))
print('r2_threshold_factor:', d['r2_threshold_factor'])
print('phi_threshold_factor:', d['phi_threshold_factor'])
"
```

The README references hit rates "~26%" for realised and "~50%" for demand-adjusted. Verify against this output.

- [ ] **Step 3: Draft the prose (target ~800 words)**

Suggested five paragraphs:
  1. Sweep design: (mu, phi, w, p) grid sizes, what each axis varies, AR(1) as baseline plus p in {2, 5, 10} for robustness.
  2. Definition of the relative thresholds, with the threshold factors used (`r2_threshold_factor=0.5`, `phi_threshold_factor=1.5`).
  3. Headline AR(1) results: `A*_{R2,da,rel}` hit in roughly half the grid at mean adoption share around the value from Step 2. State the mu gradient accurately: larger `mu` deepens the high-adoption erosion (cite the tail DA R^2 heatmap) and pulls `A*_{phi,rel}` earlier at moderate-to-high phi, while the `A*_{R2,da,rel}` crossing itself is roughly flat in `mu` because the relative threshold scales with the baseline. Also state the measurement caveat: rolling metrics lag adoption by up to eval_window periods, so A* values are detection points (upper bounds), not erosion onsets.
  4. Realised channel non-result: `A*_{R2,realised}` is mostly not reached; the finite hits cluster at very low A in the weak-signal corner of the grid (low `mu` and/or low `phi`) and are noise crossings, not erosion. Explain why: when baseline realised R^2 is near zero, the half-baseline threshold sits at zero and rolling noise can satisfy it spuriously.
  5. By-p robustness: the dual-channel pattern is present for all p tested; the delta-from-AR(1) figure shows the magnitude of the effect.

- [ ] **Step 4: Add 2-3 figures**

Recommended:
- `phase_06_a_star_R2_heatmap.png`: `A*_{R2,da,rel}` heatmap.
- `phase_06_a_star_phi_heatmap.png`: `A*_{phi,rel}` heatmap.
- Optional: `phase_06_r2_da_heatmap.png`, the tail-depth view that carries the mu gradient, if the page count allows.

`phase_06_delta_a_star_r2_from_ar1.png` goes to Appendix B.

- [ ] **Step 5: Compile and check rendering**

- [ ] **Step 6: Cross-check protocol** (all four checks)

  - [ ] **Numbers traced:** hit rate numbers, mean A* values, baseline references.
  - [ ] **Definitions match proposal v4:** `A*` definitions match section 4.3; the "relative" qualifier matches the proposal's pre-registration discussion.
  - [ ] **Figures verified:** all 3-4 heatmaps opened and verified.
  - [ ] **Style pass.**

- [ ] **Step 7: Commit**

```bash
git add docs/Report/report.tex
git commit -m "report: 6.5 parameter sweep and critical adoption shares"
```

---

### Stage 6: §6.6 Transaction-cost extension and economic endpoint (phase 7)

**Files:**
- Modify: `docs/Report/report.tex` under `\subsection{Transaction-cost extension and economic endpoint (phase 7)}`

**Word budget:** ~500 words plus 2 figures.

**Source artifacts:**
- `notebooks/phase_07_evaluation_extensions.ipynb`
- `results/data/phase_07_transaction_costs.npz`, fields: `c_grid` (8,), `bin_centers` (30,), `binned_abs_means` (8, 30), `binned_abs_stds` (8, 30), `binned_rel_means` (8, 30), `binned_rel_stds` (8, 30), `binned_counts` (8, 30), `a_star_profit_abs` (8,), `a_star_profit_rel` (8,), `null_mean_abs`, `summary` (8, 5), `phi`, `mu`, `risk_scale`, `q_cap`, `forecast_window`, `eval_window`, `adoption_pi`, `T`, `N`, `num_seeds`, `base_seed`
- `results/figures/phase_07_a_star_profit_vs_cost.png`, `phase_07_net_profit_vs_adoption.png`

- [ ] **Step 1: Open notebook and inspect summary**

Open phase_07 notebook. The 5 columns of `summary` are: cost level, pooled mean absolute net profit at A < 0.2 and at A > 0.6, pooled mean null-relative net profit at A < 0.2 and at A > 0.6.

- [ ] **Step 2: Load .npz**

```bash
python3 -c "
import numpy as np
d = np.load('results/data/phase_07_transaction_costs.npz')
print('c_grid:', d['c_grid'])
print('a_star_profit_abs:', d['a_star_profit_abs'])
print('a_star_profit_rel:', d['a_star_profit_rel'])
print('null_mean_abs:', d['null_mean_abs'])
print('summary:')
print(d['summary'])
"
```

- [ ] **Step 3: Draft the prose (target ~500 words)**

Three paragraphs:
  1. Setup: linear transaction cost `c` applied to every trade, sweep over `c_grid`. Define `A*_{profit,abs}` (smallest A where adopter net profit crosses zero) and `A*_{profit,rel}` (smallest A where adopter net profit crosses `null_mean_abs`, the proposal's primary economic endpoint).
  2. Results: at zero cost adopter profit rises with adoption; `A*_{profit,abs}` crosses zero only in the c ~ 0.003 to 0.004 band, and the crossing is from below (a profitability onset), the reverse of the proposal's from-above erosion reading; say so explicitly. The null-relative curve is uniformly positive at every positive cost level and slightly negative everywhere at c = 0.
  3. Interpretation: the null benchmark books own-impact paper profit E[null profit] = mu sigma_q^2 / N = 2.5e-4 per period on a position roughly 16x the adopter cap, which is why the c = 0 null-relative mean is systematically (slightly) negative at every observed adoption share; the single binned crossing at A ~ 0.68 is noise around that mean, not a threshold. At c > 0 the same size asymmetry flips sign through the null's larger cost bill. Present the null-relative endpoint as faithful to the proposal but dominated by position-size asymmetry in both directions; the absolute endpoint is the cleaner economic read in this baseline, and adopter mean profit grows with adoption at every cost level tested.

- [ ] **Step 4: Add 2 figures**

- `phase_07_a_star_profit_vs_cost.png`: central economic-endpoint result.
- `phase_07_net_profit_vs_adoption.png`: adopter net profit vs adoption across costs.

- [ ] **Step 5: Compile and check rendering**

- [ ] **Step 6: Cross-check protocol** (all four checks)

  - [ ] **Definitions match proposal v4:** `A*_{profit}` definitions match proposal section 4.3 and section 3.7 (transaction-cost extension).

- [ ] **Step 7: Commit**

```bash
git add docs/Report/report.tex
git commit -m "report: 6.6 transaction-cost extension and economic endpoint"
```

---

## IMPLEMENTATION: Section 5

### Stage 7: §5.1 Software architecture

**Files:** Modify `report.tex` under `\subsection{Software architecture}`.

**Word budget:** ~300 words plus 1 small table or module list.

**Source artifacts:**
- `src/reflexive_market/__init__.py` (7 lines), `adoption.py` (47 lines), `forecast.py` (75 lines), `market.py` (30 lines), `metrics.py` (150 lines), `simulate.py` (249 lines), `traders.py` (30 lines). Total 588 lines.
- `CLAUDE.md` module-to-proposal-equation table (lines ~48-58).

- [ ] **Step 1: Read each module's docstring and public functions**

```bash
for f in src/reflexive_market/*.py; do echo "=== $f ==="; head -30 "$f"; done
```

- [ ] **Step 2: Reproduce the module table from CLAUDE.md in LaTeX**

The table maps each module to its responsibility and the proposal equations it implements. Use `tabularx` (already in preamble).

- [ ] **Step 3: Draft prose (~300 words) around the table**

One paragraph naming the design constraints (pure numpy, no pandas/scipy/sklearn in `src/`, deterministic given seed, no module-level randomness, functions never print or plot), followed by the table.

- [ ] **Step 4: Compile and check rendering**

- [ ] **Step 5: Cross-check protocol** (all four checks)

  - [ ] **Numbers traced:** the module-to-equation mapping matches `CLAUDE.md` and the line counts match the checkout.
  - [ ] **Definitions match proposal v4:** equation numbers in the table match the proposal.

- [ ] **Step 6: Commit**

```bash
git add docs/Report/report.tex
git commit -m "report: 5.1 software architecture"
```

---

### Stage 8: §5.2 Phased construction

**Files:** Modify `report.tex` under `\subsection{Phased construction}`.

**Word budget:** ~400 words.

**Source artifacts:**
- `CLAUDE.md` phase-definitions section (lines ~60-155).
- `notebooks/README.md` phase status table.

- [ ] **Step 1: Read CLAUDE.md phases and notebooks/README.md**

- [ ] **Step 2: Draft a numbered list of the seven phases**

One paragraph framing the staging discipline (no phase N starts until N-1 is committed). Then the seven-phase list, each phase with its name and one-line goal. Mirrors the format of section 5 of the proposal.

- [ ] **Step 3: Compile and check rendering**

- [ ] **Step 4: Cross-check protocol** (all four checks)

- [ ] **Step 5: Commit**

```bash
git add docs/Report/report.tex
git commit -m "report: 5.2 phased construction"
```

---

### Stage 9: §5.3 Reproducibility

**Files:** Modify `report.tex` under `\subsection{Reproducibility}`.

**Word budget:** ~250 words.

**Source artifacts:**
- `CLAUDE.md` reproducibility section.
- `requirements.txt`, `pyproject.toml`.

- [ ] **Step 1: Inspect `requirements.txt` and `pyproject.toml`**

```bash
cat requirements.txt pyproject.toml
```

- [ ] **Step 2: Draft prose (~250 words)**

Cover: every notebook has a `seed` parameter; every `.npz` is named with phase + name; same seed + same parameters reproduce the same figure; CI runs pytest on every commit (link to `.github/workflows/`); Python version; pure-numpy commitment.

- [ ] **Step 3: Compile and check rendering**

- [ ] **Step 4: Cross-check protocol** (all four checks)

- [ ] **Step 5: Commit**

```bash
git add docs/Report/report.tex
git commit -m "report: 5.3 reproducibility"
```

---

## MODEL: Section 3

### Stage 10: §3.1 Single-asset market with linear price impact

**Files:** Modify `report.tex` under `\subsection{Single-asset market with linear price impact}`.

**Word budget:** ~400 words plus 3-4 displayed equations.

**Source artifacts:**
- Proposal v4 section 2.1, section 3.1, equations (4), (5), (6).
- `src/reflexive_market/market.py`.

- [ ] **Step 1: Read proposal section 3.1 and `market.py`**

- [ ] **Step 2: Lift equations (4), (5), (6) into the subsection**

Copy from `docs/proposal/reflexive_forecast_proposal_v4.tex` directly to preserve exact symbol usage. Number them locally.

- [ ] **Step 3: Draft prose (~400 words)**

One paragraph framing the Beja-Goldman / Farmer-Joshi market-maker setup (citation `\citep{beja1980,farmerjoshi2002}`). One paragraph stating equations (4)-(6) with their interpretations: aggregate demand, price update, return law.

- [ ] **Step 4: Add Beja-Goldman and Farmer-Joshi BibTeX entries**

Add to `references.bib`:

```bibtex
@article{beja1980,
  author  = {Beja, A. and Goldman, M. B.},
  title   = {On the Dynamic Behavior of Prices in Disequilibrium},
  journal = {Journal of Finance},
  volume  = {35},
  number  = {2},
  pages   = {235--248},
  year    = {1980}
}

@article{farmerjoshi2002,
  author  = {Farmer, J. D. and Joshi, S.},
  title   = {The Price Dynamics of Common Trading Strategies},
  journal = {Journal of Economic Behavior \& Organization},
  volume  = {49},
  number  = {2},
  pages   = {149--171},
  year    = {2002}
}
```

- [ ] **Step 5: Compile and check rendering** (bibtex must run cleanly with the new entries; check the References section appears)

- [ ] **Step 6: Cross-check protocol** (all four checks)

- [ ] **Step 7: Commit**

```bash
git add docs/Report/report.tex docs/Report/references.bib
git commit -m "report: 3.1 single-asset market with linear price impact"
```

---

### Stage 11: §3.2 Trader behaviour: belief, decision, switching layers

**Files:** Modify `report.tex` under `\subsection{Trader behaviour: belief, decision, and switching layers}`.

**Word budget:** ~500 words plus 2 equations.

**Source artifacts:**
- Proposal v4 section 3.2 and equations (1), (2), (3), (8).
- `src/reflexive_market/traders.py`.

- [ ] **Step 1: Read proposal section 3.2 and `traders.py`**

- [ ] **Step 2: Draft prose**

Three short paragraphs covering: belief layer (forecast value), decision layer (mean-variance demand mapping per Brock-Hommes), switching layer (binary adopter status). Equations (1), (2), and (3) for the demand mapping and the position cap.

- [ ] **Step 3: Add Brock-Hommes BibTeX entry**

```bibtex
@article{brockhommes1998,
  author  = {Brock, W. A. and Hommes, C. H.},
  title   = {Heterogeneous Beliefs and Routes to Chaos in a Simple Asset Pricing Model},
  journal = {Journal of Economic Dynamics and Control},
  volume  = {22},
  number  = {8-9},
  pages   = {1235--1274},
  year    = {1998}
}
```

- [ ] **Step 4: Compile and check rendering**

- [ ] **Step 5: Cross-check protocol** (all four checks)

- [ ] **Step 6: Commit**

```bash
git add docs/Report/report.tex docs/Report/references.bib
git commit -m "report: 3.2 trader behaviour"
```

---

### Stage 12: §3.3 Null rule and rolling AR forecasting rule

**Files:** Modify `report.tex` under `\subsection{Null rule and rolling AR forecasting rule}`.

**Word budget:** ~350 words plus 1-2 equations.

**Source artifacts:**
- Proposal v4 sections 3.3 and 3.4, equations (9), (10), (11).
- `src/reflexive_market/forecast.py`.

- [ ] **Step 1: Read proposal section 3.3 and `forecast.py`**

- [ ] **Step 2: Draft prose**

One paragraph on the null random rule (zero-mean i.i.d. order noise, equation (9); the null rule has no position cap). One paragraph on the AR(p) rule (equations (10) and (11): rolling least-squares fit on a window of size w, one-step-ahead OOS forecast, parameter `p` defaults to 1).

- [ ] **Step 3: Compile and check rendering**

- [ ] **Step 4: Cross-check protocol** (all four checks)

- [ ] **Step 5: Commit**

```bash
git add docs/Report/report.tex
git commit -m "report: 3.3 null rule and rolling AR forecasting rule"
```

---

### Stage 13: §3.4 Adoption mechanisms (3.4.1 stochastic, 3.4.2 CE)

**Files:** Modify `report.tex` under `\subsection{Adoption mechanisms}` with both subsubsections.

**Word budget:** ~400 words plus equations (11)-(15).

**Source artifacts:**
- Proposal v4 section 3.5, equations (12)-(15).
- `src/reflexive_market/adoption.py`.

- [ ] **Step 1: Read proposal section 3.4 and `adoption.py`**

- [ ] **Step 2: Draft 3.4.1 Stochastic diffusion**

Equations (12) and (13). Discrete-time Bernoulli adoption with rate `pi`. One paragraph (~150 words).

- [ ] **Step 3: Draft 3.4.2 Certainty-equivalent switching**

Equations (14) and (15). The certainty equivalent CE = mean - (a/2) var per rule, the score S_t = CE^(A) - CE^(0), and the logistic switch probability Lambda(alpha + beta S_t). One paragraph (~250 words).

- [ ] **Step 4: Compile and check rendering**

- [ ] **Step 5: Cross-check protocol** (all four checks)

- [ ] **Step 6: Commit**

```bash
git add docs/Report/report.tex
git commit -m "report: 3.4 adoption mechanisms"
```

---

### Stage 14: §3.5 Intra-period timing

**Files:** Modify `report.tex` under `\subsection{Intra-period timing}`.

**Word budget:** ~250 words plus an enumerated timing list.

**Source artifacts:**
- Proposal v4 section 3.6.
- `CLAUDE.md` intra-period timing section.

- [ ] **Step 1: Read proposal section 3.6**

- [ ] **Step 2: Draft prose**

One short paragraph framing why intra-period timing matters in agent-based markets (order of operations is not given by the equations alone). Then the four-step enumeration: observe returns, submit orders, market maker absorbs demand and moves the quote, exogenous shock and AR term realise. Word-for-word match to CLAUDE.md and to proposal section 3.6.

- [ ] **Step 3: Compile and check rendering**

- [ ] **Step 4: Cross-check protocol** (all four checks)

- [ ] **Step 5: Commit**

```bash
git add docs/Report/report.tex
git commit -m "report: 3.5 intra-period timing"
```

---

### Stage 15: §3.6 Realised vs demand-adjusted decomposition

**Files:** Modify `report.tex` under `\subsection{The realised vs demand-adjusted decomposition}`.

**Word budget:** ~400 words plus 2 equations.

**Source artifacts:**
- Proposal v4 equation (7) and section 3.6 (definition of `x_{t+1}`).
- `CLAUDE.md` (the "not the full regression residual" caveat in the overview).

- [ ] **Step 1: Read both sources carefully**

- [ ] **Step 2: Draft prose**

Two paragraphs. First: define realised return `r_{t+1}` and demand-adjusted return `x_{t+1} = r_{t+1} - mu D_t`. Display both equations. Explain why this decomposition matters: realised R^2 is what a deployed forecaster sees, demand-adjusted R^2 is the counterfactual that strips out contemporaneous price impact. Second: the caveat. `x_{t+1}` is NOT the full regression residual `sigma eps = r_{t+1} - phi r_t - mu D_t`. It strips out only the contemporaneous adopter-demand channel, leaving the lagged-return persistence channel intact. This distinction is important because it is the source of the "demand-adjusted erosion" channel name.

- [ ] **Step 3: Compile and check rendering**

- [ ] **Step 4: Cross-check protocol** (all four checks)

  - [ ] **Definitions match proposal v4:** the `x_{t+1}` formula and the residual caveat are verbatim from the proposal.

- [ ] **Step 5: Commit**

```bash
git add docs/Report/report.tex
git commit -m "report: 3.6 realised vs demand-adjusted decomposition"
```

---

## METRICS: Section 4

### Stage 16: §4.1 Primary forecast-performance endpoints (realised + DA R^2)

**Files:** Modify `report.tex` under `\subsection{Primary forecast-performance endpoints}` with both subsubsections.

**Word budget:** ~500 words plus 2 equations.

**Source artifacts:**
- Proposal v4 section 4.1.
- `src/reflexive_market/metrics.py`.

- [ ] **Step 1: Read proposal section 4.1 and `metrics.py`**

- [ ] **Step 2: Draft 4.1.1 Realised-return R^2**

The standard OOS R^2 formula against `r_{t+1}`. Rolling over a window of `eval_window` steps. Include the formula. State the benchmark convention once: metrics.rolling_oos_r2 uses the trailing window's in-sample mean as the constant benchmark, not a real-time prevailing mean (negligible at near-zero-mean returns).

- [ ] **Step 3: Draft 4.1.2 Demand-adjusted-return R^2**

Same formula but against `x_{t+1}` (referencing the definition from §3.6). One sentence on why the same forecast can have different R^2 on the same path against the two targets.

- [ ] **Step 4: Compile and check rendering**

- [ ] **Step 5: Cross-check protocol** (all four checks)

- [ ] **Step 6: Commit**

```bash
git add docs/Report/report.tex
git commit -m "report: 4.1 primary forecast-performance endpoints"
```

---

### Stage 17: §4.2 Primary economic endpoint

**Files:** Modify `report.tex` under `\subsection{Primary economic endpoint}`.

**Word budget:** ~250 words plus 1 equation.

**Source artifacts:** Proposal v4 section 4.1, transaction-cost extension in section 3.7.

- [ ] **Step 1: Read proposal sections 4.1 and 3.7**

- [ ] **Step 2: Draft prose**

Define adopter net profit per period (gross PnL minus transaction cost on volume traded). State the null-relative criterion: adopter net profit minus the null benchmark `null_profit_t - c * E|q^(0)|`, where E|q^(0)| = sqrt(2/pi) * sigma_q is stored as `null_mean_abs` in the phase 7 npz. State that the null benchmark's gross P&L has positive mean mu * sigma_q^2 / N from own price impact and that both legs of the comparison scale with the null's roughly 16x larger position; motivate why the proposal prefers the null-relative view and why phase 7 reports it with the size-asymmetry caveat.

- [ ] **Step 3: Compile and check rendering**

- [ ] **Step 4: Cross-check protocol** (all four checks)

- [ ] **Step 5: Commit**

```bash
git add docs/Report/report.tex
git commit -m "report: 4.2 primary economic endpoint"
```

---

### Stage 18: §4.3 Effective AR coefficient diagnostic

**Files:** Modify `report.tex` under `\subsection{Effective AR coefficient as a market-dynamics diagnostic}`.

**Word budget:** ~250 words.

**Source artifacts:** Proposal v4 section 4.2.

- [ ] **Step 1: Read proposal section 4.2**

- [ ] **Step 2: Draft prose**

Effective phi is a rolling AR(1) coefficient on realised returns, fit independently of the forecast. Under adoption it should rise above the input `phi` because adopter demand pushes realised returns in the forecast direction (the same mechanism behind the realised-R^2 climb in §6.3).

- [ ] **Step 3: Compile and check rendering**

- [ ] **Step 4: Cross-check protocol** (all four checks)

- [ ] **Step 5: Commit**

```bash
git add docs/Report/report.tex
git commit -m "report: 4.3 effective AR coefficient diagnostic"
```

---

### Stage 19: §4.4 Target-specific critical adoption shares

**Files:** Modify `report.tex` under `\subsection{Target-specific critical adoption shares}`.

**Word budget:** ~400 words plus a small table mapping each A* to its definition.

**Source artifacts:** Proposal v4 section 4.3.

- [ ] **Step 1: Read proposal section 4.3**

- [ ] **Step 2: Build the A* definition table**

| Symbol | Target | Definition |
|--------|--------|------------|
| `A*_{R2,realised}` | realised-return R^2 | proposal definition: smallest A where realised R^2 crosses zero from above (typically not reached) |
| `A*_{R2,realised,rel}` | realised-return R^2 | operational analogue: half its low-A baseline (fires only on weak-signal noise crossings) |
| `A*_{R2,da,rel}` | demand-adjusted R^2 | smallest A where DA R^2 falls to half its low-A baseline |
| `A*_{phi,rel}` | effective phi | smallest A where effective phi rises to 1.5x its baseline |
| `A*_{profit,abs}` | adopter profit | smallest A where adopter mean net profit crosses zero (in this regime a from-below onset, not erosion) |
| `A*_{profit,rel}` | adopter profit | smallest A where adopter net profit exceeds the null benchmark (null gross P&L minus its own cost) |
| `A*_{vol}` | (optional) | smallest A where realised vol crosses a threshold |

- [ ] **Step 3: Draft prose around the table**

Two paragraphs: motivation for "target-specific" thresholds (different targets, different stories); a note on the "relative" qualifier (pre-registered when the absolute zero-crossing never occurs in the cost-free baseline).

- [ ] **Step 4: Compile and check rendering**

- [ ] **Step 5: Cross-check protocol** (all four checks)

- [ ] **Step 6: Commit**

```bash
git add docs/Report/report.tex
git commit -m "report: 4.4 target-specific critical adoption shares"
```

---

### Stage 20: §4.5 Simulation protocol, seeds, parameter grid

**Files:** Modify `report.tex` under `\subsection{Simulation protocol, seed handling, and parameter grid}`.

**Word budget:** ~400 words plus a parameter table.

**Source artifacts:**
- Notebook parameter cells across all 7 phases.
- `results/data/phase_06_a_star_grid.npz` for grid sizes (`mu_grid`, `phi_grid`, `w_grid`, `forecast_p_grid`).

- [ ] **Step 1: Collect default parameter values from each notebook**

```bash
for nb in notebooks/phase_*.ipynb; do
  echo "=== $nb ==="
  python3 -c "
import json
with open('$nb') as f: data = json.load(f)
for cell in data['cells'][:5]:
    if cell['cell_type'] == 'code': print(''.join(cell['source'])[:600])
"
done
```

- [ ] **Step 2: Draft a parameter table**

| Parameter | Symbol | Default | Range tested |
|-----------|--------|---------|--------------|
| Trader count | N | [value] | [single] |
| Periods | T | [value] | [single] |
| Price impact | mu | [value] | mu_grid |
| AR coefficient (input) | phi | [value] | phi_grid |
| Forecast window | w | [value] | w_grid |
| Forecast order | p | 1 | forecast_p_grid |
| Adoption rate (stochastic) | pi | [value] | [as tested] |
| Risk scale | a | [value] | [single] |
| Demand cap | q_cap | [value] | [single] |

- [ ] **Step 3: Draft prose around the table**

One paragraph on seed handling (one master seed per phase, derivative seeds per Monte Carlo run, paired shocks across regimes where applicable). One paragraph on the parameter grid for the sweep.

- [ ] **Step 4: Compile and check rendering**

- [ ] **Step 5: Cross-check protocol** (all four checks)

- [ ] **Step 6: Commit**

```bash
git add docs/Report/report.tex
git commit -m "report: 4.5 simulation protocol, seeds, parameter grid"
```

---

## DISCUSSION: Section 7

### Stage 21: §7.1 Interpretation of the dual-channel mechanism

**Files:** Modify `report.tex` under `\subsection{Interpretation of the dual-channel mechanism}`.

**Word budget:** ~500 words. No new figures; reference figures from §6.3 and §6.5.

- [ ] **Step 1: Re-read §6.3 and the proposal's section 4.5 (if it discusses interpretation)**

- [ ] **Step 2: Draft prose**

Three paragraphs:
  1. Re-state the dual-channel finding in interpretive language (not as a result). Adoption is self-fulfilling for the realised-return target but degrading for the demand-adjusted target.
  2. Why this matters for deployed forecasters: realised R^2 over-reports the "true" forecasting signal under adoption because it conflates the signal-the-forecast-was-trained-on with the price-impact channel created by the forecast's own users.
  3. Why this matters for theory: classical performative-prediction results often assume the forecaster can decompose performance into stable and adoption-driven parts. The dual-channel result quantifies that decomposition in a market with price impact.

- [ ] **Step 3: Compile and check rendering**

- [ ] **Step 4: Cross-check protocol** (all four checks)

- [ ] **Step 5: Commit**

```bash
git add docs/Report/report.tex
git commit -m "report: 7.1 interpretation of the dual-channel mechanism"
```

---

### Stage 22: §7.2 Why effective AR coefficient rises with adoption

**Files:** Modify `report.tex` under `\subsection{Why the effective AR coefficient rises with adoption}`.

**Word budget:** ~350 words.

- [ ] **Step 1: Re-read §6.3 and §4.3**

- [ ] **Step 2: Draft prose**

Trace the mechanism in plain English: the AR forecast at time t uses `r_t` as a predictor. Adopters take positions proportional to that forecast, so the aggregate adopter demand at time t is proportional to `r_t`. Price impact `mu D_t` then pushes `r_{t+1}` in the direction of `r_t`, which is exactly an increase in the lag-1 autocorrelation, i.e. effective phi. The relationship is mechanical.

- [ ] **Step 3: Compile and check rendering**

- [ ] **Step 4: Cross-check protocol** (all four checks)

- [ ] **Step 5: Commit**

```bash
git add docs/Report/report.tex
git commit -m "report: 7.2 why effective AR coefficient rises with adoption"
```

---

### Stage 23: §7.3 Boundary conditions and realised-channel non-result

**Files:** Modify `report.tex` under `\subsection{Boundary conditions and the realised-channel non-result}`.

**Word budget:** ~400 words.

- [ ] **Step 1: Re-read §6.5 paragraph 4 (the realised non-result)**

- [ ] **Step 2: Draft prose**

Two paragraphs:
  1. The realised-R^2 channel does not systematically erode under adoption in the regimes tested. Across the (mu, phi) sweep, `A*_{R2,realised}` is reached in only ~26% of cells and the hits cluster at very low A in the weak-signal corner of the grid. These are noise crossings: when baseline realised R^2 is already near zero, the half-baseline threshold sits at zero and rolling noise can satisfy it spuriously.
  2. The boundary conditions: the demand-adjusted erosion claim holds across the bulk of the grid; the realised-channel amplification claim holds in the high-mu, high-phi corner where the dual-channel pattern is most visible; outside that corner the realised channel is essentially flat or noisy.

- [ ] **Step 3: Compile and check rendering**

- [ ] **Step 4: Cross-check protocol** (all four checks)

- [ ] **Step 5: Commit**

```bash
git add docs/Report/report.tex
git commit -m "report: 7.3 boundary conditions and realised-channel non-result"
```

---

### Stage 24: §7.4 Limitations

**Files:** Modify `report.tex` under `\subsection{Limitations}`.

**Word budget:** ~250 words.

- [ ] **Step 1: Draft a short bulleted list of limitations**

Four-to-six bullets. Examples:
- Single-asset market only; cross-asset and portfolio effects are out of scope.
- Linear price impact `mu D_t` only; non-linear impact (e.g. square-root law) is not tested.
- AR(p) forecast only; ML/non-parametric forecasters are not tested.
- Discrete-time setup; continuous-time effects (latency, microstructure) are not modelled.
- Homogeneous non-adopter pool (random null rule); heterogeneous trader ecology (trend followers, contrarians) is mentioned as an optional second extension but not implemented.
- Transaction costs are linear and symmetric; market-impact-of-trade and inventory costs are not modelled.
- Profit is marked at the post-impact quote and unwinds never re-enter the order flow, so all profit figures are paper profits under the model's accounting; the null benchmark books own-impact profit mu sigma_q^2 / N on a position roughly 16x the adopter cap, which dominates the null-relative endpoint at c = 0.
- The market maker absorbs position levels rather than position changes (Beja-Goldman style rather than Farmer-Joshi order flow), which strengthens the persistence channel.
- With the baseline risk_scale and q_cap the position cap binds almost every period, so adopters are effectively fixed-size sign traders.
- The CE switching risk aversion (switching_a = 1) is set independently of the demand layer's implied risk aversion (~7 at the realised return variance).

- [ ] **Step 2: Compile and check rendering**

- [ ] **Step 3: Cross-check protocol** (all four checks)

- [ ] **Step 4: Commit**

```bash
git add docs/Report/report.tex
git commit -m "report: 7.4 limitations"
```

---

## FRAMING: Sections 2, 1, 8

### Stage 25: §2 Background (all four subsections)

**Files:** Modify `report.tex` under `\subsection{Reflexivity and performative prediction}`, `\subsection{Heterogeneous-agent finance and price formation}`, `\subsection{Forecast evaluation under self-fulfilment}`, `\subsection{Key concepts and notation}`.

**Word budget:** ~1500 words total across four subsections.

- [ ] **Step 1: Draft §2.1 Reflexivity and performative prediction (~400 words)**

Cite Soros' reflexivity concept; cite the performative-prediction literature (Perdomo et al. 2020 if available, or the equivalent foundational paper). Frame: when forecasts move the market they describe, evaluating them with off-shelf metrics no longer measures only forecast skill.

- [ ] **Step 2: Add Soros and Perdomo et al. BibTeX entries**

```bibtex
@book{soros1987,
  author = {Soros, George},
  title  = {The Alchemy of Finance},
  publisher = {Simon \& Schuster},
  year   = {1987}
}

@inproceedings{perdomo2020,
  author    = {Perdomo, Juan C. and Zrnic, Tijana and Mendler-D{\"u}nner, Celestine and Hardt, Moritz},
  title     = {Performative Prediction},
  booktitle = {Proceedings of the 37th International Conference on Machine Learning},
  year      = {2020}
}
```

- [ ] **Step 3: Draft §2.2 Heterogeneous-agent finance and price formation (~400 words)**

Cite Brock-Hommes (already in bib), Beja-Goldman (already in bib), Farmer-Joshi (already in bib). One paragraph on mean-variance demand with CARA, one on market-maker price impact.

- [ ] **Step 4: Draft §2.3 Forecast evaluation under self-fulfilment (~350 words)**

The OOS R^2 / MSFE tradition assumes the target is exogenous of the forecast. State the issue: under adoption the target inherits the forecast, so the standard metric mixes channels. Position the report's contribution as: explicit decomposition into realised and demand-adjusted targets on the same path.

- [ ] **Step 5: Draft §2.4 Key concepts and notation (~350 words)**

A small notation table: `r_t`, `D_t`, `mu`, `phi`, `pi`, `A`, `A*`, `x_{t+1}`, `w`, `p`. Plus a one-paragraph glossary of "adoption share", "realised return", "demand-adjusted return", "effective AR coefficient".

- [ ] **Step 6: Compile and check rendering**

- [ ] **Step 7: Cross-check protocol** (all four checks)

- [ ] **Step 8: Commit**

```bash
git add docs/Report/report.tex docs/Report/references.bib
git commit -m "report: 2 background (all four subsections)"
```

---

### Stage 26: §1 Introduction (all four subsections)

**Files:** Modify `report.tex` under `\subsection{Motivation}`, `\subsection{Relation to previous work}`, `\subsection{Research question and contribution}`, `\subsection{Report roadmap}`.

**Word budget:** ~800 words total across four subsections.

- [ ] **Step 1: Draft §1.1 Motivation (~200 words)**

Lead with the practical scenario: a forecasting service is deployed; users start trading on its signal; performance metrics change. Pose the question: is the change a measurement artefact or a real shift in the underlying signal?

- [ ] **Step 2: Draft §1.2 Relation to previous work (~250 words)**

Position against three traditions: (a) reflexivity / performative prediction (Soros, Perdomo et al.), (b) heterogeneous-agent finance (Brock-Hommes, Beja-Goldman, Farmer-Joshi), (c) classical forecast evaluation (Diebold-Mariano-style OOS testing).

- [ ] **Step 3: Draft §1.3 Research question and contribution (~250 words)**

State the question: how does adoption of a shared autoregressive forecast affect realised vs demand-adjusted predictive performance and economic value, in a tractable single-asset agent-based market? State the contribution: a clean simulator demonstrating the dual-channel result and quantifying it across (mu, phi, w, p).

- [ ] **Step 4: Draft §1.4 Report roadmap (~100 words)**

One paragraph signposting sections 2-8.

- [ ] **Step 5: Compile and check rendering**

- [ ] **Step 6: Cross-check protocol** (all four checks)

- [ ] **Step 7: Commit**

```bash
git add docs/Report/report.tex
git commit -m "report: 1 introduction (all four subsections)"
```

---

### Stage 27: §8 Conclusion (all three subsections)

**Files:** Modify `report.tex` under `\subsection{Summary of findings}`, `\subsection{Implications for forecasting under adoption}`, `\subsection{Directions for future work}`.

**Word budget:** ~500 words total.

- [ ] **Step 1: Draft §8.1 Summary of findings (~200 words)**

Two sentences on the dual-channel result. Two sentences on the economic-endpoint finding. One sentence on the realised-channel non-result.

- [ ] **Step 2: Draft §8.2 Implications for forecasting under adoption (~200 words)**

State the practical takeaway: realised R^2 over-reports under adoption; demand-adjusted R^2 is the cleaner signal for measuring whether the underlying forecasting hypothesis still holds; both should be reported when adoption is plausible.

- [ ] **Step 3: Draft §8.3 Directions for future work (~100 words)**

Two-to-three sentences. Examples: non-linear price impact, heterogeneous trader ecology, ML forecasters, multi-asset extensions.

- [ ] **Step 4: Compile and check rendering**

- [ ] **Step 5: Cross-check protocol** (all four checks)

- [ ] **Step 6: Commit**

```bash
git add docs/Report/report.tex
git commit -m "report: 8 conclusion (all three subsections)"
```

---

## WRAP

### Stage 28: Appendices, references finalisation, abstract polish, final read-through

**Files:** Modify `report.tex` under `\section{Model equations and derivations}`, `\section{Additional figures}`, `\section{Parameter tables and reproducibility details}`. Modify the abstract (lines ~65-69). Finalise `references.bib`.

**Word budget:** ~1500 words across the three appendices plus the abstract polish.

- [ ] **Step 1: Appendix A: Model equations and derivations**

Re-display equations (1)-(15) from the proposal in one place, with brief connecting prose. This is for a reader who wants the full set on one page without flipping through §3-§4.

- [ ] **Step 2: Appendix B: Additional figures**

Include the supplementary figures not used in §6, e.g.:
- `phase_04_adoption_share.png` (adoption trajectory plots).
- `phase_04_demand_contribution.png`.
- `phase_04_oos_r2_saturation_mc.png`.
- `phase_06_r2_realised_heatmap.png`.
- `phase_06_baseline_r2_by_p.png`.
- `phase_06_a_star_r2_lines_by_p.png`.

Each with a one-sentence caption.

- [ ] **Step 3: Appendix C: Parameter tables and reproducibility details**

Full parameter table by phase (mirrors what each notebook's parameters cell contains). Repo URL placeholder if not yet known. Python version. Pure-numpy commitment. CI pointer.

- [ ] **Step 4: Re-read the abstract against the now-complete body**

Open `report.tex` lines 65-69. Verify every numeric claim in the abstract matches the body (the "0.07 to 0.19", "0.08 to 0.04", "0.28 to 0.45" numbers anchored to the zero-adoption control in particular). If any number in the abstract was recalled rather than sourced, fix it now.

- [ ] **Step 5: Finalise references.bib**

Scan the report for every `\cite{}` and confirm an entry exists. Run:

```bash
cd docs/Report && bibtex report 2>&1 | grep -i "warning\|error"
```

Resolve any "warning: I didn't find a database entry for ..." messages by adding the missing entry.

- [ ] **Step 6: Full read-through compile**

Run the four-command pdflatex sequence one more time, then open `report.pdf`. Read every section in order. Note any:
- Overfull/underfull boxes (in the .log).
- Broken cross-references (`??` in the PDF).
- Inconsistencies between abstract / intro / conclusion / results.
- Page count outside 10-30 range.

Fix any issues found.

- [ ] **Step 7: Final commit**

```bash
git add docs/Report/report.tex docs/Report/references.bib docs/Report/report.pdf
git commit -m "report: appendices, references finalisation, abstract polish, final read-through"
```

---

## Source reference appendix

This section is a glossary of source artifacts so each stage can refer back to it.

### `.npz` field catalog

#### `phase_01_baseline.npz`
- `prices` (5001,), `returns` (5000,), `demand` (5000,)
- `phi_input` scalar, `phi_empirical` scalar, `seed` scalar

#### `phase_02_benchmark.npz`
- Per-seed (100 seeds): `mean_per_seed`, `std_per_seed`, `rho_per_seed`, `kurt_per_seed`
- Rolling trace (T=5000): `mean_phi_trace`, `std_phi_trace`
- Scalars: `phi_input`, `rolling_window`, `seeds`

#### `phase_03_ar_forecast.npz`
- `summary` (3, 5): 3 windows × 5 stats
- `ar_windows` (3,), `ar_order`, `eval_window`, `phi_input`, `seed`

#### `phase_04_stochastic_adoption.npz`
- `summary` (3, 8): 3 regimes × 8 stats
- `regime_pi` (3,), `regime_delta` (3,), `regime_names` (3,)
- Scalars: `phi_input`, `mu`, `risk_scale`, `q_cap`, `forecast_window`, `eval_window`, `T`, `N`, `seed`

#### `phase_05_performance_adoption.npz`
- `summary` (2, 6), `regime_names` (2,)
- Scalars: `phi_input`, `mu`, `risk_scale`, `q_cap`, `forecast_window`, `eval_window`, `stochastic_pi`, `switching_window`, `switching_a`, `switching_alpha`, `switching_beta`, `T`, `N`, `seed`

#### `phase_06_a_star_grid.npz`
- Grid axes: `mu_grid` (5,), `phi_grid` (6,), `w_grid` (3,), `forecast_p_grid` (4,) = [1, 2, 5, 10]
- A* arrays (4, 3, 6, 5) = (p, w, phi, mu): `a_star_R2_realised`, `a_star_R2_da`, `a_star_phi`
- Hit rates (same shape): `hit_rate_R2_realised`, `hit_rate_R2_da`, `hit_rate_phi`
- Baselines (same shape): `baseline_R2_realised_grid`, `baseline_R2_da_grid`, `baseline_phi_grid`
- Tail (same shape): `tail_R2_realised_grid`, `tail_R2_da_grid`
- Line curves: `line_curve_adoption_share` (8000,), `line_curve_da_r2` (4, 8000), `line_curve_phi` (4, 8000)
- Thresholds: `r2_threshold_factor`, `phi_threshold_factor`, `min_hit_rate`, `baseline_span`, `tail_window_span`
- Scalars: `T`, `N`, `num_seeds`, `base_seed`, `eval_window`, `risk_scale`, `q_cap`, `adoption_pi`

#### `phase_07_transaction_costs.npz`
- `c_grid` (8,), `bin_centers` (30,)
- Binned profits (8, 30): `binned_abs_means`, `binned_abs_stds`, `binned_rel_means`, `binned_rel_stds`, `binned_counts`
- A* (8,): `a_star_profit_abs`, `a_star_profit_rel`
- Scalars: `null_mean_abs`, `phi`, `mu`, `risk_scale`, `q_cap`, `forecast_window`, `eval_window`, `adoption_pi`, `T`, `N`, `num_seeds`, `base_seed`
- `summary` (8, 5)

### Figure catalog (`results/figures/`)

```
Phase 1: phase_01_price_path, phase_01_return_series, phase_01_return_histogram
Phase 2: phase_02_rolling_phi, phase_02_seed_mean, phase_02_seed_std, phase_02_seed_lag1, phase_02_seed_kurtosis
Phase 3: phase_03_ar_coefficients, phase_03_rolling_msfe, phase_03_rolling_oos_r2
Phase 4: phase_04_adoption_share, phase_04_demand_contribution,
         phase_04_oos_r2_over_time, phase_04_oos_r2_over_time_single,
         phase_04_oos_r2_saturation_mc, phase_04_oos_r2_saturation_single,
         phase_04_oos_r2_vs_adoption_mc, phase_04_oos_r2_vs_adoption,
         phase_04_phi_vs_adoption_mc, phase_04_phi_vs_adoption
Phase 5: phase_05_adoption_share, phase_05_erosion_vs_adoption, phase_05_switching_score
Phase 6: phase_06_a_star_phi_by_p, phase_06_a_star_phi_heatmap,
         phase_06_a_star_r2_by_p, phase_06_a_star_R2_heatmap,
         phase_06_a_star_r2_lines_by_p, phase_06_baseline_r2_by_p,
         phase_06_da_r2_vs_adoption_by_p, phase_06_delta_a_star_r2_from_ar1,
         phase_06_r2_da_by_p, phase_06_r2_da_heatmap,
         phase_06_r2_realised_by_p, phase_06_r2_realised_heatmap
Phase 7: phase_07_a_star_profit_vs_cost, phase_07_net_profit_vs_adoption
```

### Source module catalog (`src/reflexive_market/`)

| Module | LoC | Responsibility | Proposal eqs |
|--------|-----|----------------|--------------|
| `__init__.py` | 7 | package init |   |
| `market.py` | 30 | aggregate demand, price update, return law | (4), (5), (6) |
| `traders.py` | 30 | null rule, demand mapping, cap | (1), (2), (3), (9) |
| `adoption.py` | 47 | stochastic diffusion, CE switching | (12)-(15) |
| `forecast.py` | 75 | rolling AR(p) fit and OOS forecast | (10), (11) |
| `metrics.py` | 150 | MSFE, OOS R^2 (realised + DA), effective phi | §4 |
| `simulate.py` | 249 | end-to-end run | §3.6 timing |
