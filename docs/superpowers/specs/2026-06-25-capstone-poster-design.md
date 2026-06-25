# Capstone poster design spec

Date: 2026-06-25
Status: approved (design), pending implementation plan
Author of work: Jan Jacek Wejchert
Owner: this repository, branch `palm`

## 1. Goal and deliverable

Produce a single, submission-ready scientific poster for the capstone
"Performative Prediction in a Single-Asset Market".

- Format: A0 (841 x 1189 mm), portrait orientation, single page.
- Output: PDF, print resolution, fonts embedded, renders identically offline.
- Aesthetic: clean academic, IE-branded, elevated typography. Not a stock
  LaTeX poster look and not a busy template.
- Build: HTML and CSS rendered to PDF via headless Google Chrome (already
  installed at `/Applications/Google Chrome.app`).
- Reproducible: same data and same source produce the same PDF, by one command.

The poster summarises the report at `docs/Report/report.tex` (compiled
`report.pdf`). It is a standalone visual artifact, not a reformatting of the
report prose.

## 2. Source material

- Report source of truth: `docs/Report/report.tex`, `docs/Report/report.pdf`.
- Numeric results: `results/data/*.npz` (regenerate figures from these, do not
  reuse the existing report PNGs).
- Brand asset: `docs/Report/IELogo.jpeg`, IE accent navy `#1F4E79`.
- Project framing constraints (from CLAUDE.md and saved project memory):
  - The study has TWO channels, not three. The economic endpoint (transaction
    costs, profit, `A*_{profit}`) is future work, never reported as a settled
    result.
  - No em dashes anywhere in any repo artifact, including this poster and its
    source. Use commas, colons, periods, or parentheses.

## 3. Headline story and exact numbers

One mechanism, two readings. As adoption of a shared rolling AR(1) forecast
rises, coordinated adopter demand lifts the realised-return out-of-sample R^2
through self-fulfilment, while the demand-adjusted R^2 (the same forecast scored
against a counterfactual that strips out contemporaneous price impact) erodes on
the same path. Effective return persistence rises in step and links the two.

Headline numbers (baseline configuration, phase 4, zero-adoption control versus
near-full adoption). Source: `results/data/phase_04_stochastic_adoption.npz`,
array `summary`.

| Quantity                        | Low adoption | High adoption | Display      |
|---------------------------------|--------------|---------------|--------------|
| Realised-return OOS R^2 (blue)  | 0.0695       | 0.1904        | 0.07 -> 0.19 |
| Demand-adjusted OOS R^2 (red)   | 0.0821       | 0.0386        | 0.08 -> 0.04 |
| Effective AR coefficient (gold) | 0.2821       | 0.4470        | 0.28 -> 0.45 |

Supporting facts available for the poster:

- Input persistence phi = 0.25; market N = 200, T = 8000, mu = 0.05,
  sigma = 0.01, sigma_q = 1.0, q_cap = 0.05, risk scale a*sigma^2 = 0.001,
  trailing metric window = 1000.
- Steady state, not transient: extending the fast-diffusion regime to T = 30000
  across 50 seeds, the readings hold separated plateaus, realised near 0.17 and
  demand-adjusted near 0.02 (phase 4 saturation).
- Mechanism survives endogenous certainty-equivalent switching (phase 5): at
  matched adoption shares both mechanisms give the same erosion and the same
  persistence amplification.
- Parameter sweep (phase 6): 3600 runs across
  mu in {0.025, 0.05, 0.075, 0.10, 0.15},
  phi in {0.05, 0.10, 0.15, 0.20, 0.25, 0.30},
  w in {100, 250, 500}, p in {1, 2, 5, 10}, 10 seeds.
  - Relative demand-adjusted threshold A*_{R2,da,rel} (half the low-adoption
    baseline) reached in 67 of 90 AR(1) cells, mean detected share 0.29.
  - Relative persistence threshold A*_{phi,rel} (1.5x baseline) reached in 82
    of 90 cells, mean share 0.38.
  - Realised threshold A*_{R2,realised,rel} reached in only 28 of 90 cells, all
    weak-signal noise crossings at near-zero baselines (median baseline 0.014,
    26 of 28 at phi <= 0.20). This is the designed non-result: the realised
    channel does not erode systematically.
- Practical lesson (take-home): realised-return R^2, the only score a deployed
  forecaster can compute, over-reports skill once the forecast has users with
  price impact. Both readings should be reported together, and their gap
  measures the deployment-driven component of measured accuracy.

Key equations for the model block (rendered with KaTeX):

- Aggregate demand: D_t = (1/N) sum_i q_{i,t}
- Price update: p_{t+1} = p_t + mu D_t + sigma eps_{t+1}
- Return law: r_{t+1} = phi r_t + mu D_t + sigma eps_{t+1}
- Mean-variance demand (capped): z_{i,t} = r_hat_{i,t+1} / (a sigma^2)
- Decomposition: r_{t+1} = mu D_t + x_{t+1}, with
  x_{t+1} = r_{t+1} - mu D_t = phi r_t + sigma eps_{t+1}

Literature anchors (compact reference list): Soros 1987; Perdomo et al. 2020;
Brock and Hommes 1998; Beja and Goldman 1980; Farmer and Joshi 2002; Diebold and
Mariano 1995.

## 4. Visual system

Semantic color system, used consistently across prose, equations, and figures so
the poster reads from a distance:

- Realised return, self-fulfilling channel, goes up: channel blue, approx
  `#1B6FC4`.
- Demand-adjusted signal, erosion channel, goes down: channel red, approx
  `#C62828`.
- Effective persistence phi, the linking diagnostic, goes up: gold, approx
  `#B8860B`.
- Brand and structure: IE navy `#1F4E79` for the title, section heads, and
  hairline rules.
- Body ink `#1A1A1A`, muted neutral `#5B6670`, hairlines `#DDE3EA`, panel tint
  `#F5F8FB`.

Exact hex values may be tuned slightly during implementation for print contrast,
but the role assignments (blue realised, red demand-adjusted, gold phi, navy
brand) are fixed.

Typography (creative but disciplined, all open-licensed, embedded locally as
woff2):

- Fraunces: poster title and section headings. A modern serif with optical
  sizing and real character, scholarly rather than generic.
- Inter: body text, captions, and all figure labels. The matplotlib figures use
  Inter so type is unified across prose and charts.
- IBM Plex Mono: the large result numbers and parameter values (for example
  `0.07 -> 0.19`), giving the quantitative findings a distinct precise voice.

Fallback if embedding is undesirable: Georgia (serif), Helvetica Neue (sans),
both already on the machine.

Branding: IE logo and IE navy present in the title band and footer. Otherwise
free design within A0 portrait.

## 5. Layout

A0 portrait grid: full-width title band, a one-glance headline strip, the
mechanism explained once near the top, three columns of supporting depth, and a
take-home footer band. Generous whitespace, hairline navy rules between blocks.

```
+==========================================================================+
|  [IE]   PERFORMATIVE PREDICTION IN A SINGLE-ASSET MARKET                  |
|         Self-fulfilment and signal erosion under forecast adoption        |
|         Jan Jacek Wejchert  |  Supervisor: Nacho Molina Clemente          |
|         IE School of Science and Technology  |  MSc BA and DS  |  July 2026|
+==========================================================================+
|  ONE FORECAST, TWO VERDICTS, AS ADOPTION RISES                           |
|   realised R^2 0.07 -> 0.19 (blue up)   demand-adj R^2 0.08 -> 0.04 (red dn)
|   effective persistence phi 0.28 -> 0.45 (gold up)                       |
+----------------------------+---------------------------------------------+
|   FEEDBACK-LOOP SCHEMATIC   |   r_{t+1} = [ mu D_t ] + [ x_{t+1} ]         |
|   forecast -> demand ->     |        self-fulfilment    independent signal |
|   impact -> return ->       |        (blue box)         (red box)          |
|   scored two ways           |                                              |
+--------------+--------------+---------------------------+-----------------+
| COLUMN 1     | COLUMN 2                                 | COLUMN 3        |
| Motivation   | Metrics: two R^2 targets + effective phi | Threshold map   |
| and question |                                          | heatmaps        |
| The model    | DUAL-CHANNEL HERO CHART                  | A*_{R2,da,rel}  |
| eq (5) (6)   | realised up, demand-adjusted down        | A*_{phi,rel}    |
| Decomposition| Saturation: separation is a steady state | Robustness vs p |
| Timing 1..4  | (T = 30000 plateau)                       | Conclusion      |
|              |                                          | Future work     |
|              |                                          | References      |
+--------------+------------------------------------------+-----------------+
|  TAKE-HOME: realised R^2 over-reports skill once a forecast has users.    |
|  Report both readings; their gap is the deployment-driven component.      |
|  Reproducible single-asset agent-based simulator  |  IE Capstone 2026     |
|  jan.wejchert@student.ie.edu                                              |
+==========================================================================+
```

Minimum body text around 24 pt so the poster is legible at roughly 1.5 m.

## 6. Section content (concise poster copy)

Short blocks, not report paragraphs. Final wording drafted during
implementation, drawn from the report abstract, results, discussion, and
conclusion.

- Title band: title, subtitle, author, supervisor, affiliation, program, date,
  IE logo. Contact in the footer.
- Headline strip: the three color-coded result transitions, one line of plain
  English framing.
- Mechanism row: the feedback-loop schematic plus the color-coded decomposition
  equation, the thesis in one picture.
- Column 1: motivation (a published forecast acquires users whose trading enters
  the returns it is scored on), research question, the minimal market
  (Brock-Hommes mean-variance demand against a Beja-Goldman and Farmer-Joshi
  market maker), the return law and the realised versus demand-adjusted
  decomposition, the four-step intra-period timing.
- Column 2: the two evaluation targets and the effective-persistence diagnostic,
  the dual-channel hero chart, the saturation result (the separation is a steady
  state, not a transient of the adoption ramp).
- Column 3: the threshold heatmaps across the (mu, phi) grid, robustness across
  AR order p, the realised-channel non-result (weak-signal noise crossings),
  conclusion and the measurement lesson, future work (economic endpoint and
  heterogeneous ecology, both deferred), compact references.
- Footer: take-home message, reproducibility note, contact, IE line.

The economic endpoint stays strictly in future work. The framing is two
channels, not three.

## 7. Figures, regenerated poster-grade from npz

Write `poster/figures.py` that reads `results/data/*.npz` and emits vector SVG in
one unified style (Inter labels, the semantic color system, despined axes,
hairline grid, large fonts). SVG keeps figures razor sharp at A0.

1. Dual-channel hero: realised R^2 (blue, rising) and demand-adjusted R^2 (red,
   falling) versus adoption share, Monte Carlo means with plus or minus 1 SD
   bands, endpoints annotated 0.07 to 0.19 and 0.08 to 0.04. Source
   `phase_04_stochastic_adoption.npz`.
2. Effective phi versus adoption: gold, rising, input phi = 0.25 dashed. Same
   source. May be an inset of figure 1 or a small standalone panel.
3. Steady-state saturation: both readings holding separated plateaus over
   T = 30000. Source phase 4 saturation data or recompute per the notebook
   parameters.
4. Threshold heatmaps: A*_{R2,da,rel} and A*_{phi,rel} across the (mu, phi) grid,
   refined sequential colormap, hit-rate convention for unreached cells. Source
   `phase_06_a_star_grid.npz`.
5. Optional robustness-by-p strip showing the mechanism survives AR order.

If a needed array is not directly in an npz, recompute deterministically from the
documented notebook parameters and seeds (the report already does this for some
figures). Prefer reading the npz where the value exists.

## 8. Custom signature graphics

- Feedback-loop schematic, hand-authored SVG: forecast r_hat to adopter demand q
  to aggregate demand D_t to price impact mu D_t to realised return r_{t+1}, then
  scored two ways. A blue tap on the realised target and a red tap on the
  demand-adjusted counterfactual x = r - mu D. This single diagram carries the
  whole thesis.
- Decomposition equation as a motif: r_{t+1} = mu D_t + x_{t+1} rendered large
  with mu D_t boxed blue (self-fulfilment, price impact) and x_{t+1} boxed red
  (independent signal). Reused as the visual key wherever the two colors appear.

## 9. Build pipeline and file layout

```
poster/
  figures.py        # npz -> styled SVG assets, deterministic
  assets/
    fonts/          # Fraunces, Inter, IBM Plex Mono woff2
    katex/          # local KaTeX css and fonts
    ielogo.*        # IE logo, possibly cleaned
    fig_*.svg       # generated figures
    schematic.svg   # hand-authored feedback loop
  poster.html       # structure, content, KaTeX math
  poster.css        # @page A0 (841mm x 1189mm), grid, color system, type
  render.sh         # headless Chrome --print-to-pdf -> the deliverable
  build.sh          # figures.py then render.sh, one command
  README.md         # how to rebuild
results/poster/
  poster.pdf        # the submission-ready deliverable
  poster_preview.png# quick visual check
```

Render approach:

- CSS `@page { size: 841mm 1189mm; margin: 0 }` and
  `-webkit-print-color-adjust: exact` so backgrounds and colors print.
- Primary render: headless Google Chrome,
  `--headless=new --no-pdf-header-footer --print-to-pdf` against a `file://` URL.
- Verify the output is exactly A0 with `mutool info` or `pdfinfo` after each
  build. If Chrome CLI mis-sizes, fall back to a small Playwright or Puppeteer
  script using the installed Chrome channel with explicit
  `width: 841mm, height: 1189mm, printBackground: true`.
- Embed all fonts (subset or full woff2) so the PDF is portable and identical
  offline. Register Inter with matplotlib so figure text matches.

## 10. Constraints and conventions

- A0 portrait, single page, PDF, fonts embedded.
- No em dashes anywhere in poster source or content.
- Two-channel framing only. Economic endpoint and heterogeneous ecology are
  future work.
- IE branding: logo plus navy `#1F4E79`. Header content exactly as in section 5.
- Figures regenerated from npz, vector SVG, unified style. Do not embed the old
  report PNGs.
- Keep the poster build self-contained under `poster/`, deliverable under
  `results/poster/`. Do not modify `src/`, the notebooks, or the report.

## 11. Risks and mitigations

- Chrome CLI A0 sizing quirks: mitigate with the Playwright or Puppeteer fallback
  and a post-build dimension check.
- Local KaTeX assets: vendor the KaTeX css and fonts under `poster/assets/katex`
  so math renders offline.
- matplotlib font embedding: register the Inter ttf and set rcParams, verify the
  SVG references Inter, not a fallback.
- IE logo is a JPEG with a white background: place on white, or source a cleaner
  asset if the edges look poor at A0. Not a blocker.

## 12. Acceptance criteria (done when)

- `results/poster/poster.pdf` opens as a single A0 portrait page measuring
  841 x 1189 mm (verified with `mutool info` or `pdfinfo`).
- All fonts embedded; the PDF renders identically on a machine with no network.
- Every data figure is vector and generated by `poster/figures.py` from the npz
  files, in the unified style and semantic colors.
- The two custom graphics (feedback-loop schematic and color-coded decomposition)
  are present and legible.
- The header content matches section 5 exactly, including July 2026 and the
  contact email, with the IE logo and navy accent.
- The poster reads cleanly at roughly 1.5 m, body text at least about 24 pt.
- No em dashes anywhere; two-channel framing throughout; economic endpoint only
  in future work.
- One command (`poster/build.sh`) regenerates figures and the PDF from the data.
