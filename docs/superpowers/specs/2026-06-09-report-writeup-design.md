# Capstone report writeup: staged plan

**Author:** Jan Jacek Wejchert
**Date:** 2026-06-09
**Target:** `docs/Report/report.tex` (compiled to `report.pdf`)
**Source material:** `docs/proposal/reflexive_forecast_proposal_v4.pdf`, `notebooks/phase_*.ipynb`, `results/figures/`, `results/data/`

## Goal

Turn the existing skeleton `docs/Report/report.tex` into an exceptional final report by writing it carefully, one subsection at a time, over the course of a couple of weeks. Every claim is traced to a source artifact; no recalled numbers, no recalled definitions.

## Constraints

- **Page count:** 10-30 pages (target middle of range, ~22 pages).
- **Format:** 12pt Times New Roman, 1.0 line spacing.
- **Style:**
  - No em dashes anywhere (use commas, colons, periods, parentheses).
  - Surname is allowed on this academic deliverable (the global "first name only" rule does not apply to formal university submissions).
  - Plain English in titles, captions, body.
- **Authoritative sources:**
  - The proposal v4 PDF is the contract for symbols, endpoints, and definitions. If the report and proposal disagree, the proposal wins until explicitly revised.
  - The `results/data/phase_*.npz` files and notebook cells are the contract for numbers. No quantitative claim goes into the report without a traceable source.
  - Equation numbering follows the compiled v4 PDF: decomposition (7), profit (8), null rule (9), AR (10) and (11), diffusion (12) and (13), CE (14), logistic switch (15). The repo was reconciled to this numbering on the fable branch. Three prose cross-references in the proposal's section 5 table were fixed in the tex only, so recompile the proposal PDF before Stage 10 lifts equations.

## Strategy

Write **bottom-up**, one subsection per stage. The order respects two facts:
1. The Results section is the most concretely defined right now (numbers are in the .npz files). Writing it first locks in what Discussion, Intro, and Abstract must accurately reference.
2. Framing chapters (Background, Intro, Conclusion, Abstract) are sharper when written last, because all the technical content has already been articulated.

**High-level order:**
Format setup → Results (6.1-6.6) → Implementation (5.1-5.3) → Model (3.1-3.6) → Metrics (4.1-4.5) → Discussion (7.1-7.4) → Background (2.1-2.4) → Introduction (1.1-1.4) → Conclusion (8.1-8.3) → Appendices + References + Abstract polish + read-through.

## Stage 0: format setup (do before any prose)

Change the report.tex preamble so we write into the final format from the start:

- `\documentclass[12pt]{article}` (was 11pt).
- Replace `\usepackage{XCharter}` with `\usepackage{mathptmx}` (Times Roman for text and math).
- Add `\linespread{1.0}` explicitly.
- Switch from `\parskip`-style spacing to traditional `\parindent 1em` with `\parskip 0pt` (standard for single-spaced academic papers).
- Add `\usepackage{natbib}` with `\bibliographystyle{plainnat}`.
- Create `docs/Report/references.bib` (empty file with a header comment).
- Verify a clean test compile of the unchanged-content skeleton before any prose is written.

Word budget guideline for ~22 pages mid-range:

| Section        | Words |
|----------------|------:|
| Abstract       |   200 |
| 1 Introduction |   800 |
| 2 Background   |  1200 |
| 3 Model        |  1700 |
| 4 Metrics      |  1200 |
| 5 Implementation | 800 |
| 6 Results      |  3000 |
| 7 Discussion   |  1300 |
| 8 Conclusion   |   500 |
| References + Appendices | variable |

These budgets total ~10,200 words of body text, roughly 21 to 22 pages at
12pt single spacing, leaving room for at most about 10 figures in the main
text before the 30-page cap binds; every other figure goes to Appendix B.
Check the compiled page count after each section group and trim Results,
Model, and Metrics first if it tracks above 28 pages.

## Cross-check protocol per stage (definition of done)

Every subsection must pass all four checks before it is committed:

1. **Numbers traced.** Every quantitative claim points to a specific `results/data/phase_NN_*.npz` field or a specific notebook cell that produced it. Use an inline LaTeX comment with the source, e.g. `% src: phase_06_a_star_grid.npz['a_star_R2_da']`. No recalled numbers.
2. **Definitions match proposal v4.** Any symbol, endpoint, or term (μ, φ, A*, demand-adjusted return, etc.) is checked against `docs/proposal/reflexive_forecast_proposal_v4.pdf`. If the report and proposal disagree, the disagreement is resolved before moving on.
3. **Figures verified.** Any `\includegraphics{...}` references a file that actually exists in `results/figures/`, and the surrounding prose accurately describes the figure (open the PNG and check, do not rely on recall).
4. **Style pass.** No em dashes; plain English; equations render correctly in compile.

Each stage ends with: `git commit -m "report: <subsection title>"`. One stage = one commit so any single stage can be reverted without losing the rest.

## The stages (29 total: Stage 0 plus 28 content stages)

```
Stage 0:  Format setup (12pt Times, 1.0 spacing, BibTeX, test compile)

RESULTS (6): write first because numbers are concrete:
Stage 1:  6.1 Baseline market and benchmark validation (phases 1, 2)
Stage 2:  6.2 AR forecast performance without adoption (phase 3)
Stage 3:  6.3 Dual-channel result under stochastic adoption (phase 4)
Stage 4:  6.4 Endogenous CE-based switching (phase 5)
Stage 5:  6.5 Parameter sweep and critical adoption shares (phase 6)
Stage 6:  6.6 Transaction-cost extension and economic endpoint (phase 7)

IMPLEMENTATION (5):
Stage 7:  5.1 Software architecture
Stage 8:  5.2 Phased construction
Stage 9:  5.3 Reproducibility

MODEL (3):
Stage 10: 3.1 Single-asset market with linear price impact
Stage 11: 3.2 Trader behaviour: belief, decision, switching layers
Stage 12: 3.3 Null rule and rolling AR forecasting rule
Stage 13: 3.4 Adoption mechanisms (3.4.1 stochastic, 3.4.2 CE)
Stage 14: 3.5 Intra-period timing
Stage 15: 3.6 Realised vs demand-adjusted decomposition

METRICS (4):
Stage 16: 4.1 Primary forecast-performance endpoints (realised + DA R^2)
Stage 17: 4.2 Primary economic endpoint
Stage 18: 4.3 Effective AR coefficient diagnostic
Stage 19: 4.4 Target-specific critical adoption shares
Stage 20: 4.5 Simulation protocol, seeds, parameter grid

DISCUSSION (7):
Stage 21: 7.1 Interpretation of dual-channel mechanism
Stage 22: 7.2 Why effective AR coefficient rises with adoption
Stage 23: 7.3 Boundary conditions and realised-channel non-result
Stage 24: 7.4 Limitations

FRAMING:
Stage 25: 2.1-2.4 Background (one stage, four short subsections)
Stage 26: 1.1-1.4 Introduction (one stage, four short subsections)
Stage 27: 8.1-8.3 Conclusion (one stage, three short subsections)

WRAP:
Stage 28: Appendices A/B/C + finalize references.bib + abstract polish + full read-through compile
```

Three stages bundle multiple short subsections (Background, Intro, Conclusion) because the per-subsection content is light. If any of those gets heavy in practice we can split it later.

## Pace

Targeting 1-3 stages per day, this completes in 10-28 working days. The pace is the user's call per day; the plan does not assume any particular cadence.

## Out of scope

- No new analyses or experiments. The results are frozen as of phase 7.
- No refactoring of `src/reflexive_market/`. The code is shipped.
- No second extension (heterogeneous trader ecology). Phase 7 transaction-cost extension is the only extension reported.
- No machine-learning forecasters, no multiple assets.

## After this spec

The next step is the `writing-plans` skill, which will produce the per-stage detailed plan (what each stage produces, exact sources to look up, expected word count, expected pitfalls, commit message template).
