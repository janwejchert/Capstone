# Poster redesign: real visuals and a narrative spine

Date: 2026-06-28
Status: approved design, ready for implementation plan
Scope: the A0 portrait poster under `poster/` only. The report, the simulator,
`src/`, and the deferred economic endpoint are all out of scope.

This is the second poster iteration. The 2026-06-25 spec
(`2026-06-25-poster-schematic-redesign-design.md`) produced the current
schematic poster. That poster builds cleanly to a single A0 page but the user
finds it too text-heavy and not visual enough, with one specific copy fault.

## Problem

The current poster has no picture of the actual simulated market: every figure
is a schematic (before/after bars, a box-and-arrow loop, a small gap diagram).
Four concrete faults the user flagged:

1. Not visual enough. A passer-by meets three dense text columns before any
   concrete image of what the market or the result looks like.
2. No "market simulation" visual. The simulator is never shown in action.
3. The return-decomposition copy is opaque: `r_{t+1} = mu D_t + x_{t+1}` is
   shown with `x_{t+1}` unexplained, and in the render its colour labels collide
   with the feedback-loop caption.
4. The steady-state ("gap stays open") diagram is a cramped little SVG in
   column two; the user wants it shown bigger.

## Goal

A more visual, faster-to-read A0 poster that keeps the existing identity and
every number accurate, built around one top-to-bottom narrative spine with a
single dominant headline figure, two real data-driven figures, and a clearer
plain-language on-ramp for a non-expert.

## Locked decisions

### Aesthetic (unchanged from the 2026-06-25 spec)
- Palette: navy `#1F4E79`, blue `#1B6FC4` (realised, self-fulfilment), red
  `#C62828` (demand-adjusted, erosion), gold `#B8860B` (effective persistence),
  ink `#1A1A1A`, mute `#5B6670`, hairline `#DDE3EA`, panel `#F5F8FB`, tints
  `#EAF2FB` / `#FBEAEA` / gold-tint.
- Fonts: Fraunces (serif headings), Inter (sans body), IBM Plex Mono (numbers),
  already vendored under `poster/assets/fonts`. KaTeX for the model equations.

### Layout: narrative spine (chosen, "Option A")
Top to bottom on the A0 portrait page:

1. **Title bar** (full-width navy). Unchanged.
2. **KPI strip**: the three monospace numbers, each gaining a plain-word line so
   the reading lands without jargon.
   - `0.07 -> 0.19` blue tint, label "what a live forecaster sees (rises)".
   - `0.08 -> 0.04` red tint, label "the genuinely independent signal (falls)".
   - `0.28 -> 0.45` gold tint, label "the market's memory stiffens".
   The technical names (realised-return R squared, demand-adjusted R squared,
   effective persistence phi) stay as a secondary sub-label so the link to the
   report is unambiguous.
3. **Setup row** (two columns, panel background).
   - Left: the decomposition rendered as **two named cards** (the "T3"
     treatment). Heading "One forecast, two channels". A single equation line
     `r_{t+1} = mu D_t + x_{t+1}` (KaTeX, colour-coded) sits above two cards:
     - Blue card, title "Self-fulfilment", symbol `mu D_t`, plain text: the
       price move the adopters' own coordinated trades create; the forecast
       bends the market toward itself.
     - Red card, title "Independent signal", symbol `x_{t+1}`, plain text: what
       tomorrow's return would have been with no crowd pushing the price; the
       genuine, gradeable skill.
     The small forecast -> demand -> price-move feedback loop moves beneath the
     cards, where its caption no longer collides with the term labels.
   - Right: **NEW real price path** figure. One simulated market's log-price
     line over time, drawn on-brand from `results/data/phase_01_baseline.npz`
     (`prices`). One-line caption, e.g. "one simulated market: the price wanders,
     one-period returns look like noise". Optional thin returns strip beneath the
     price line, decided at build time if it does not crowd the panel.
4. **Headline figure** (full width). **NEW real dual-channel result curve**:
   rolling out-of-sample R squared as a function of adoption share, realised
   (blue, rising) and demand-adjusted (red, falling), drawn on-brand from
   regenerated data (see Data below). Title "As adoption rises, one forecast
   earns two verdicts". This **replaces the current before/after hero bars**,
   which were a weaker schematic of the same comparison. The low-adoption and
   high-adoption endpoints are labelled; see Number reconciliation below for how
   they relate to the KPI strip.
5. **Three-column body** (text, lighter than today).
   - Col 1: "The question" (a sharpened one-line plain-language hook leading the
     paragraph) and "The model" (the three KaTeX equations with their existing
     one-line glosses, kept compact).
   - Col 2: "Two evaluation targets" and the **enlarged steady-state diagram**.
     The steady-state figure is rolling R squared versus time, two flat plateaus
     (realised and demand-adjusted) with a "gap stays open" marker, given real
     vertical room. Its plateau labels are driven from the regenerated data so
     they match the headline curve's high-adoption end. Caption stresses
     permanence: 30,000 steps, 50 seeds, not a start-up transient.
   - Col 3: "The dual-channel result" (prose) and "Conclusion" plus the
     reference line.
6. **Footer** (full-width contact strip). Unchanged.

The headline figure (R squared versus adoption share) and the steady-state
figure (R squared versus time) use deliberately different x-axes so they are
complementary, not redundant: one shows the two readings diverging as adoption
rises, the other shows the resulting gap is permanent.

### Plain-language scaffolding ("the very basics")
The KPI plain-word lines, the two named decomposition cards, the price-path
caption, and the sharpened question hook together let the core idea land before
any equation is read. British spelling (self-fulfilment). No em dashes anywhere.

## Data and reproducibility

Every shown number and every drawn curve must trace to saved results, matching
the report.

- **Price path**: data already saved in `results/data/phase_01_baseline.npz`
  (`prices`, 5001 points). Downsampled to an SVG polyline at build time.
- **Result curve and steady-state plateaus**: the 30,000-step, 50-seed mean
  trajectories are not currently saved (only a 3x8 endpoint summary in
  `results/data/phase_04_stochastic_adoption.npz`). They will be regenerated and
  saved to a new `results/data/poster_result_curve.npz` so the poster is
  reproducible and consistent with phase 4:
  - Reuse the **stored phase-4 fast-diffusion parameters** from
    `phase_04_stochastic_adoption.npz` (`phi_input`, `mu`, `risk_scale`,
    `q_cap`, `forecast_window`, `eval_window`, `T`, `N`, `seed`, and the fast
    regime's `regime_pi` / `regime_delta`, index 2) so numbers match the
    notebook rather than drifting.
  - Run `simulate.run(...)` across the 50 seeds. For each, compute realised
    rolling OOS R squared `rolling_oos_r2(returns, forecasts, eval_window)` and
    demand-adjusted rolling OOS R squared
    `rolling_oos_r2(returns - mu * demand, forecasts, eval_window)`, plus the
    `adoption_share` path. Average across seeds.
  - Save the mean realised R squared, mean demand-adjusted R squared, and mean
    adoption share versus time, the derived R squared versus adoption-share
    curves, and the late-time plateau values, to `poster_result_curve.npz`.
- **Build-time injection**: figure shapes (SVG polyline `d` attributes and axis
  bounds) and endpoint numbers are written into `poster/assets/figure_values.json`
  as `{{val:...}}` tokens. `build.mjs` already substitutes `{{val:...}}` last,
  over the fully assembled HTML, so tokens inside inline SVGs resolve. No reader
  ever sees a hand-typed number or curve that has drifted from the data.

### Number reconciliation
The headline curve and the steady-state plateaus are both derived from the same
`poster_result_curve.npz` (the within-run fast-diffusion adoption sweep), so they
are mutually consistent by construction. The current KPI numbers
(0.07 -> 0.19 realised, 0.08 -> 0.04 demand-adjusted) come from phase 4's
cross-regime summary, a different computation, and the within-run sweep may
plateau at slightly different high-adoption values (closer to the saturation
figure's 0.17 / 0.02). The qualitative dual-channel claim (realised rises,
demand-adjusted falls) holds for both. The implementation plan must decide one
coherent source for any number shown more than once rather than silently mixing
the two; if the KPI high values shift to the within-run sweep, that is an
acceptable, more-coherent change, and it stays traceable to saved data.

## Implementation mapping

- `poster/figures.py`: keep `write_values()`. Add a function that loads the
  phase-4 params, regenerates the fast-diffusion MC mean trajectories, saves
  `results/data/poster_result_curve.npz`, and writes the derived SVG polyline
  path strings, axis bounds, and endpoint/plateau values into
  `figure_values.json`. Add a price-path polyline generator from the phase-1
  npz. Wire the existing `--recompute` flag: regenerate the MC when set or when
  the npz is absent, otherwise load the cached npz so rebuilds stay fast. Pure
  numpy plus the local `reflexive_market` package; no plotting, no new heavy
  dependencies.
- `poster/poster.template.html`: restructure the setup row to the two-card
  decomposition plus relocated feedback loop on the left and the new price-path
  SVG on the right; replace the before/after hero bars with the full-width
  result-curve SVG; enlarge the steady-state SVG and move it into column two as
  specified; add the KPI plain-word lines; sharpen the question hook; trim
  result/conclusion prose to fit. New inline SVGs use `{{val:...}}` tokens for
  paths, bounds, and labels.
- `poster/poster.css`: styles for the two-card decomposition, the price-path and
  result-curve figures, the enlarged steady-state, and the KPI sub-labels. Keep
  the `@page` A0 size and the font-face block.
- `poster/build.mjs`: no logic change expected (KaTeX for the three model
  equations and the decomposition line; `{{val:...}}` substitution already runs
  last). Add the decomposition equation to the `EQ` map if it is not already a
  rendered token.

## Verification

- `cd poster && node build.mjs` (or `./build.sh`) regenerates
  `figure_values.json`, the result-curve npz, and `results/poster/poster.pdf`
  plus the preview PNG.
- Exactly one A0 page (`pdfinfo`), no clipped content, no empty corners, all
  three columns filled.
- The price path and result curve render as crisp on-brand SVG (not embedded
  matplotlib). Any number shown more than once (KPI strip, headline-curve
  endpoints, steady-state plateaus) is consistent across the poster and traceable
  to saved data, per Number reconciliation above.
- Visual review of the preview PNG against this spec, iterating on the real
  render rather than a mockup.

## Out of scope / non-goals

- No change to the report, the simulator, `src/`, or the phase notebooks.
- No embedded matplotlib PNGs on the poster; all figures stay crisp SVG.
- No generative-AI imagery.
- No transaction-cost or profit content (the economic endpoint stays deferred).
- No new colour system or fonts beyond the existing identity.

## Open to-dos (carried from the prior spec)

- Swap a vector or high-resolution official IE logo into the title-bar chip
  before final printing. The current `ielogo.jpeg` is a small raster.
