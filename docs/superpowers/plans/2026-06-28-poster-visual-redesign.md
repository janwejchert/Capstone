# Poster Visual Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the A0 poster around a top-to-bottom narrative spine with two real data-driven SVG figures (a price path and a dual-channel result curve), a two-card return decomposition that explains `x_{t+1}` in plain words, plain-language KPI labels, and an enlarged steady-state diagram.

**Architecture:** All poster content stays in `poster/poster.template.html` + `poster/poster.css` as inline SVG (the established pattern). `poster/figures.py` gains pure-numpy helpers that regenerate the fast-diffusion result curve from the simulator, cache it to `results/data/poster_result_curve.npz`, and write SVG polyline strings plus formatted labels into `poster/assets/figure_values.json`. `poster/build.mjs` substitutes `{{val:...}}` (last, over the assembled HTML) so the tokens inside the inline SVGs resolve. Numbers shown more than once trace to one saved source.

**Tech Stack:** Python 3 + numpy + the local `reflexive_market` package (figures); HTML/CSS/inline SVG + KaTeX (poster); Node `build.mjs` with `puppeteer-core` + Chrome (PDF render); pytest (invariants).

## Global Constraints

- A0 portrait page: `@page { size: 841mm 1189mm }`. The rendered PDF must be exactly **one page**, page size **2383.94 x 3370.39 pts (±3)**.
- Palette (verbatim): navy `#1F4E79`, blue `#1B6FC4` (realised / self-fulfilment), red `#C62828` (demand-adjusted / erosion), gold `#B8860B` (effective phi), ink `#1A1A1A`, mute `#5B6670`, hairline `#DDE3EA`, panel `#F5F8FB`, tints `#EAF2FB` / `#FBEAEA` / `#FBF3DF`.
- Fonts: Fraunces (serif headings), Inter (sans body), IBM Plex Mono (numbers). KaTeX for the model equations.
- **No em dashes anywhere** (code, comments, markdown, SVG, copy). British spelling (self-fulfilment).
- All poster figures are crisp on-brand inline SVG. **No embedded matplotlib PNGs.**
- `figures.py` is pure numpy + `reflexive_market` only; no pandas/scipy/sklearn/statsmodels; no plotting; all randomness through a `numpy.random.Generator`; deterministic given the seed.
- Every shown number is traceable to saved results under `results/data/`.
- Phase-4 fast-diffusion parameters (single source for the poster curve, copied from `notebooks/phase_04_stochastic_adoption.ipynb`): `N=200`, `mu=0.05`, `phi=0.25`, `sigma_news=0.01`, `sigma_q=1.0`, `forecast_window=250`, `forecast_p=1`, `risk_scale=0.001`, `q_cap=0.05`, `eval_window=1000`, `adoption_start_t=1250`, fast `adoption_pi=1e-3`, `adoption_delta=0.0`, saturation horizon `T_long=30000`, `mc_saturation_base_seed=5000`, `n_seeds_mc_saturation=50`.

## Number-sourcing decision (locked; flag to user if undesired)

- **KPI strip stays sourced from the phase-4 cross-regime summary** (`results/data/phase_04_stochastic_adoption.npz`), unchanged: realised `0.07 -> 0.19`, demand-adjusted `0.08 -> 0.04`, effective phi `0.28 -> 0.45`. This keeps the headline numbers identical to the report.
- **The headline result curve and the steady-state plateaus** come from the within-run saturated MC (`poster_result_curve.npz`). They are mutually consistent (the curve's high-adoption end equals the steady-state plateau). They are labelled with their **own** values (expected ~`0.17` realised, ~`0.02` demand-adjusted) and a one-line "extended saturated MC" caption; they are **not** relabelled to the KPI numbers. No single number appears twice with two different values.

## File Structure

- `poster/figures.py` (modify): add `make_polyline`, the fast-diffusion run + `compute_result_curve` + `load_or_compute_result_curve` + `write_figure_geometry`; keep `write_values`; wire `--recompute`; add src path + simulator/metrics imports.
- `results/data/poster_result_curve.npz` (create, generated): aggregated mean trajectories, the vs-adoption curve arrays, plateau/endpoint scalars.
- `poster/assets/figure_values.json` (modify, generated): gains polyline `d` strings, plot bounds, and formatted labels.
- `poster/poster.template.html` (modify): KPI sub-labels; setup row (two-card decomposition + relocated feedback loop on the left, price-path SVG on the right); full-width result-curve SVG replacing the before/after bars; enlarged steady-state SVG in column two; sharpened question hook; trimmed prose.
- `poster/poster.css` (modify): styles for the two-card decomposition, price-path and result-curve figures, enlarged steady-state, and KPI sub-labels.
- `poster/build.mjs`: no logic change expected (verify only).
- `tests/test_poster_figures.py` (replace): stale; rewrite against the new `figures.py` API.
- `tests/test_poster_template.py` (modify): stale token list; update to the new tokens + sections.

## Module geometry constants (single source of truth)

These viewBox/plot rectangles are referenced by both `figures.py` (to map data and to compute the steady-state line heights) and the template SVGs (axis lines, ticks, `<g transform>`). They MUST match between the two.

- **Result curve SVG:** `viewBox="0 0 320 160"`. Plot rect: translate `(40,16)`, width `270`, height `120` (bottom y=136, right x=310). Adoption x-axis `0..1`; R^2 y-axis `0..0.2`.
- **Price path SVG:** `viewBox="0 0 320 120"`. Plot rect: translate `(8,8)`, width `304`, height `104`.
- **Steady-state SVG:** `viewBox="0 0 320 200"`. Plot rect: translate `(44,24)`, width `250`, height `150` (bottom y=174). R^2 y-axis `0..0.2`. Plateau line pixel-y (absolute, in viewBox coords): `y = 24 + (1 - value/0.2) * 150`.

---

### Task 1: SVG polyline helper in `figures.py`

**Files:**
- Modify: `poster/figures.py`
- Test: `tests/test_poster_figures.py`

**Interfaces:**
- Produces: `make_polyline(xs, ys, x0, x1, y0, y1, w, h, decimals=2) -> str` returning an SVG path `d` string (`"M x,y L x,y ..."`), mapping data `(xs,ys)` from `[x0,x1] x [y0,y1]` into a `w x h` box with the y-axis flipped (SVG origin top-left).

- [ ] **Step 1: Replace the stale test file with a fresh header + the first failing test**

Overwrite `tests/test_poster_figures.py` (the current contents reference a removed API and already fail):

```python
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "poster"))
import figures  # noqa: E402


def test_make_polyline_maps_and_flips_y():
    d = figures.make_polyline([0, 1, 2], [0, 1, 0], 0, 2, 0, 1, 100, 50)
    assert d == "M0.0,50.0 L50.0,0.0 L100.0,50.0"
```

- [ ] **Step 2: Run it to confirm it fails**

Run: `python3 -m pytest tests/test_poster_figures.py::test_make_polyline_maps_and_flips_y -q`
Expected: FAIL with `AttributeError: module 'figures' has no attribute 'make_polyline'`.

- [ ] **Step 3: Add the src path + imports + `make_polyline` to `figures.py`**

At the top of `poster/figures.py`, after the existing `import numpy as np`, add the src path and simulator imports (needed by later tasks too):

```python
import sys

sys.path.insert(0, os.path.join(HERE, "..", "src"))

from reflexive_market import simulate  # noqa: E402
from reflexive_market.metrics import rolling_oos_r2  # noqa: E402
```

(`HERE` already exists in the module.) Then add the helper:

```python
def make_polyline(xs, ys, x0, x1, y0, y1, w, h, decimals=2):
    """Map data coordinates to an SVG path 'd' string in a w x h box.

    The y-axis is flipped so larger data y values sit higher in the SVG
    (which has its origin at the top-left).
    """
    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)
    px = (xs - x0) * (w / (x1 - x0))
    py = h - (ys - y0) * (h / (y1 - y0))
    pts = [f"{round(float(a), decimals)},{round(float(b), decimals)}"
           for a, b in zip(px, py)]
    return "M" + " L".join(pts)
```

- [ ] **Step 4: Run it to confirm it passes**

Run: `python3 -m pytest tests/test_poster_figures.py::test_make_polyline_maps_and_flips_y -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add poster/figures.py tests/test_poster_figures.py
git commit -m "poster: add SVG polyline helper, reset stale figures test"
```

---

### Task 2: Regenerate the dual-channel result curve

**Files:**
- Modify: `poster/figures.py`
- Create (generated): `results/data/poster_result_curve.npz`
- Test: `tests/test_poster_figures.py`

**Interfaces:**
- Consumes: `simulate.run`, `rolling_oos_r2`, `make_polyline` (Task 1).
- Produces:
  - `compute_result_curve(num_seeds=NUM_SEEDS_MC, T=T_LONG, span=1500) -> dict` with keys `adopt_curve, r2_real_vs_a, r2_da_vs_a` (1-D arrays, the vs-adoption curve), `mean_r2_real_t, mean_r2_da_t, mean_A_t` (length-T arrays), `low_real, high_real, low_da, high_da, low_A, high_A, plateau_real, plateau_da` (floats), `num_seeds, T` (ints).
  - `load_or_compute_result_curve(recompute=False) -> dict` (loads the npz unless `recompute` or missing).
  - Module constants `NUM_SEEDS_MC=50`, `T_LONG=30000`, `SAT_BASE_SEED=5000`, `RESULT_NPZ` (path).

- [ ] **Step 1: Add the failing tests**

Append to `tests/test_poster_figures.py`:

```python
def test_compute_result_curve_shows_dual_channel():
    # Tiny MC for speed; the dual-channel effect is strong enough to show.
    data = figures.compute_result_curve(num_seeds=4, T=6000, span=400)
    for k in ["adopt_curve", "r2_real_vs_a", "r2_da_vs_a",
              "low_real", "high_real", "low_da", "high_da",
              "plateau_real", "plateau_da"]:
        assert k in data, k
    # Realised R^2 rises with adoption; demand-adjusted R^2 falls.
    assert data["r2_real_vs_a"][-1] > data["r2_real_vs_a"][0]
    assert data["r2_da_vs_a"][-1] < data["r2_da_vs_a"][0]
    assert data["high_real"] > data["low_real"]
    assert data["high_da"] < data["low_da"]


def test_load_or_compute_result_curve_roundtrips(tmp_path, monkeypatch):
    npz = tmp_path / "curve.npz"
    monkeypatch.setattr(figures, "RESULT_NPZ", str(npz))
    monkeypatch.setattr(figures, "NUM_SEEDS_MC", 3)
    monkeypatch.setattr(figures, "T_LONG", 5000)
    d1 = figures.load_or_compute_result_curve(recompute=True)
    assert npz.exists()
    d2 = figures.load_or_compute_result_curve(recompute=False)
    np.testing.assert_allclose(d1["adopt_curve"], d2["adopt_curve"])
```

- [ ] **Step 2: Run to confirm failure**

Run: `python3 -m pytest tests/test_poster_figures.py -q -k "result_curve"`
Expected: FAIL with `AttributeError: module 'figures' has no attribute 'compute_result_curve'`.

- [ ] **Step 3: Implement the regeneration in `figures.py`**

Add the phase-4 constants near the top (after the existing `DATA` definition):

```python
# Phase-4 fast-diffusion parameters (notebooks/phase_04_stochastic_adoption.ipynb).
P4_N = 200
P4_MU = 0.05
P4_PHI = 0.25
P4_SIGMA_NEWS = 0.01
P4_SIGMA_Q = 1.0
P4_FORECAST_WINDOW = 250
P4_FORECAST_P = 1
P4_RISK_SCALE = 0.001
P4_Q_CAP = 0.05
P4_EVAL_WINDOW = 1000
P4_ADOPTION_START_T = P4_FORECAST_WINDOW + P4_EVAL_WINDOW  # 1250
FAST_PI = 1e-3
FAST_DELTA = 0.0
T_LONG = 30000
SAT_BASE_SEED = 5000
NUM_SEEDS_MC = 50
RESULT_NPZ = os.path.join(DATA, "poster_result_curve.npz")
```

Then the functions:

```python
def _run_fast(seed, T):
    rng = np.random.default_rng(seed)
    out = simulate.run(
        T=T, N=P4_N, mu=P4_MU, phi=P4_PHI,
        sigma_news=P4_SIGMA_NEWS, sigma_q=P4_SIGMA_Q, rng=rng,
        forecast_window=P4_FORECAST_WINDOW, forecast_p=P4_FORECAST_P,
        risk_scale=P4_RISK_SCALE, q_cap=P4_Q_CAP,
        adoption_pi=FAST_PI, adoption_delta=FAST_DELTA,
        adoption_start_t=P4_ADOPTION_START_T,
    )
    da = out["returns"] - P4_MU * out["demand"]
    r2_real = rolling_oos_r2(out["returns"], out["forecasts"], P4_EVAL_WINDOW)
    r2_da = rolling_oos_r2(da, out["forecasts"], P4_EVAL_WINDOW)
    return r2_real, r2_da, out["adoption_share"]


def compute_result_curve(num_seeds=NUM_SEEDS_MC, T=T_LONG, span=1500):
    r2r = np.full((num_seeds, T), np.nan)
    r2d = np.full((num_seeds, T), np.nan)
    adopt = np.full((num_seeds, T), np.nan)
    for s in range(num_seeds):
        r2r[s], r2d[s], adopt[s] = _run_fast(SAT_BASE_SEED + s, T)
    mean_r2r = np.nanmean(r2r, axis=0)
    mean_r2d = np.nanmean(r2d, axis=0)
    mean_A = np.nanmean(adopt, axis=0)

    finite = np.isfinite(mean_r2r) & np.isfinite(mean_r2d) & np.isfinite(mean_A)
    fin_idx = np.flatnonzero(finite)
    lo = fin_idx[:span]
    hi = fin_idx[-span:]
    low_real, high_real = float(mean_r2r[lo].mean()), float(mean_r2r[hi].mean())
    low_da, high_da = float(mean_r2d[lo].mean()), float(mean_r2d[hi].mean())
    low_A, high_A = float(mean_A[lo].mean()), float(mean_A[hi].mean())

    # Bin the finite samples by adoption share into a clean vs-adoption curve.
    nb = 50
    edges = np.linspace(0.0, 1.0, nb + 1)
    centres = 0.5 * (edges[:-1] + edges[1:])
    a_vals, yr, yd = mean_A[finite], mean_r2r[finite], mean_r2d[finite]
    which = np.clip(np.digitize(a_vals, edges) - 1, 0, nb - 1)
    ca, cr, cd = [], [], []
    for k in range(nb):
        m = which == k
        if m.any():
            ca.append(float(centres[k]))
            cr.append(float(yr[m].mean()))
            cd.append(float(yd[m].mean()))

    return {
        "adopt_curve": np.array(ca), "r2_real_vs_a": np.array(cr),
        "r2_da_vs_a": np.array(cd),
        "mean_r2_real_t": mean_r2r, "mean_r2_da_t": mean_r2d, "mean_A_t": mean_A,
        "low_real": low_real, "high_real": high_real,
        "low_da": low_da, "high_da": high_da, "low_A": low_A, "high_A": high_A,
        "plateau_real": high_real, "plateau_da": high_da,
        "num_seeds": int(num_seeds), "T": int(T),
    }


def load_or_compute_result_curve(recompute=False):
    if not recompute and os.path.exists(RESULT_NPZ):
        d = np.load(RESULT_NPZ)
        return {k: d[k] for k in d.files}
    data = compute_result_curve()
    np.savez(RESULT_NPZ, **{k: np.asarray(v) for k, v in data.items()})
    return data
```

- [ ] **Step 4: Run to confirm pass**

Run: `python3 -m pytest tests/test_poster_figures.py -q -k "result_curve"`
Expected: PASS (a few seconds for the tiny MC runs).

- [ ] **Step 5: Generate the real cached npz once**

Run: `cd poster && python3 -c "import figures; figures.load_or_compute_result_curve(recompute=True); print('ok')" && cd ..`
Expected: prints `ok`, writes `results/data/poster_result_curve.npz` (this is the full 50-seed / 30000-step run; allow ~1 minute).
Then sanity-check the saturated levels:
Run: `python3 -c "import numpy as np; d=np.load('results/data/poster_result_curve.npz'); print('real', round(float(d['high_real']),3), 'da', round(float(d['high_da']),3))"`
Expected: realised roughly `0.15..0.20`, demand-adjusted roughly `0.00..0.05`.

- [ ] **Step 6: Commit**

```bash
git add poster/figures.py tests/test_poster_figures.py results/data/poster_result_curve.npz
git commit -m "poster: regenerate dual-channel result curve from the simulator"
```

---

### Task 3: Emit figure geometry into `figure_values.json`

**Files:**
- Modify: `poster/figures.py`
- Test: `tests/test_poster_figures.py`

**Interfaces:**
- Consumes: `make_polyline`, `load_or_compute_result_curve`, `results/data/phase_01_baseline.npz` (`prices`).
- Produces: `write_figure_geometry(data)` merging these keys into `figure_values.json`: `price_path_d`; `result_real_d`, `result_da_d`, `result_high_real`, `result_high_da`, `result_low_real`, `result_low_da`; `plateau_real`, `plateau_da`, `steady_real_y`, `steady_da_y`.

- [ ] **Step 1: Add the failing test**

Append to `tests/test_poster_figures.py`:

```python
def test_write_figure_geometry_populates_json(tmp_path, monkeypatch):
    import json
    out = tmp_path / "figure_values.json"
    out.write_text("{}")
    monkeypatch.setattr(figures, "ASSETS", str(tmp_path))
    data = figures.compute_result_curve(num_seeds=3, T=6000, span=400)
    figures.write_figure_geometry(data)
    vals = json.loads(out.read_text())
    for k in ["price_path_d", "result_real_d", "result_da_d",
              "result_high_real", "result_high_da",
              "plateau_real", "plateau_da", "steady_real_y", "steady_da_y"]:
        assert k in vals, k
    assert vals["price_path_d"].startswith("M")
    assert vals["result_real_d"].startswith("M")
    # plateau labels formatted to two decimals, geometry within the steady viewBox
    assert vals["plateau_real"].count(".") == 1
    assert 24.0 <= float(vals["steady_real_y"]) <= 174.0
```

- [ ] **Step 2: Run to confirm failure**

Run: `python3 -m pytest tests/test_poster_figures.py::test_write_figure_geometry_populates_json -q`
Expected: FAIL with `AttributeError: ... 'write_figure_geometry'`.

- [ ] **Step 3: Implement `write_figure_geometry`**

Add to `figures.py`. Geometry constants match the template (see "Module geometry constants"):

```python
# Result-curve plot rect (matches the template SVG).
RC_W, RC_H = 270, 120
RC_YMAX = 0.2
# Price-path plot rect.
PP_W, PP_H = 304, 104
# Steady-state plot rect (absolute viewBox coords).
SS_TOP, SS_H, SS_YMAX = 24, 150, 0.2


def write_figure_geometry(data):
    prices = np.load(os.path.join(DATA, "phase_01_baseline.npz"))["prices"]
    step = max(1, prices.size // 300)
    idx = np.arange(0, prices.size, step)
    pmin, pmax = float(prices.min()), float(prices.max())
    pad = (pmax - pmin) * 0.05
    price_d = make_polyline(idx, prices[idx], 0, prices.size - 1,
                            pmin - pad, pmax + pad, PP_W, PP_H)

    real_d = make_polyline(data["adopt_curve"], data["r2_real_vs_a"],
                           0, 1, 0, RC_YMAX, RC_W, RC_H)
    da_d = make_polyline(data["adopt_curve"], data["r2_da_vs_a"],
                         0, 1, 0, RC_YMAX, RC_W, RC_H)

    plat_real = float(data["plateau_real"])
    plat_da = float(data["plateau_da"])
    geom = {
        "price_path_d": price_d,
        "result_real_d": real_d,
        "result_da_d": da_d,
        "result_high_real": f"{float(data['high_real']):.2f}",
        "result_high_da": f"{float(data['high_da']):.2f}",
        "result_low_real": f"{float(data['low_real']):.2f}",
        "result_low_da": f"{float(data['low_da']):.2f}",
        "plateau_real": f"{plat_real:.2f}",
        "plateau_da": f"{plat_da:.2f}",
        "steady_real_y": round(SS_TOP + (1 - plat_real / SS_YMAX) * SS_H, 1),
        "steady_da_y": round(SS_TOP + (1 - plat_da / SS_YMAX) * SS_H, 1),
    }
    out = os.path.join(ASSETS, "figure_values.json")
    existing = json.load(open(out)) if os.path.exists(out) else {}
    existing.update(geom)
    json.dump(existing, open(out, "w"), indent=2)
```

Then wire `main()` to run all three and respect `--recompute`:

```python
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--recompute", action="store_true")
    args = ap.parse_args()
    write_values()
    data = load_or_compute_result_curve(recompute=args.recompute)
    write_figure_geometry(data)
    print("wrote figure_values.json")
```

- [ ] **Step 4: Run to confirm pass**

Run: `python3 -m pytest tests/test_poster_figures.py -q`
Expected: PASS (all tests in the file).

- [ ] **Step 5: Regenerate the real `figure_values.json`**

Run: `cd poster && python3 figures.py && cd ..`
Expected: prints `wrote figure_values.json`; the file now contains the new keys alongside the existing KPI numbers.
Run: `python3 -c "import json; v=json.load(open('poster/assets/figure_values.json')); print(sorted(v))"`
Expected: includes `price_path_d`, `result_real_d`, `result_da_d`, `plateau_real`, `steady_real_y`, and the original `r2_real_high` etc.

- [ ] **Step 6: Commit**

```bash
git add poster/figures.py tests/test_poster_figures.py poster/assets/figure_values.json
git commit -m "poster: emit price-path and result-curve geometry into figure_values.json"
```

---

### Task 4: Restructure the poster template (HTML)

**Files:**
- Modify: `poster/poster.template.html`
- Modify: `tests/test_poster_template.py`

**Interfaces:**
- Consumes: tokens emitted in Task 3 plus existing `{{eq:...}}`, `{{val:r2_real_high}}` etc., `{{logo}}`.

Geometry literals in the SVGs below MUST match the "Module geometry constants" used in `figures.py`.

- [ ] **Step 1: Update the template test to the new reality first**

Replace `tests/test_poster_template.py` with:

```python
import os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(HERE, "poster")


def test_template_has_required_content():
    html = open(os.path.join(P, "poster.template.html"), encoding="utf-8").read()
    for s in ["Nacho Molina Clemente", "IE School of Science and Technology",
              "MSc in Business Analytics and Data Science", "July 2026",
              "jan.wejchert@student.ie.edu",
              "One forecast, two channels", "Self-fulfilment",
              "Independent signal", "one simulated market",
              "As adoption rises"]:
        assert s in html, s
    for tok in ["{{eq:decomposition}}", "{{eq:return_law}}",
                "{{val:r2_real_high}}", "{{val:price_path_d}}",
                "{{val:result_real_d}}", "{{val:result_da_d}}",
                "{{val:plateau_real}}", "{{logo}}"]:
        assert tok in html, tok
    assert "—" not in html  # no em dash


def test_css_is_a0_portrait():
    css = open(os.path.join(P, "poster.css"), encoding="utf-8").read()
    assert "841mm 1189mm" in css
    assert "print-color-adjust" in css
    assert "—" not in css
```

- [ ] **Step 2: Run to confirm the new template test fails**

Run: `python3 -m pytest tests/test_poster_template.py::test_template_has_required_content -q`
Expected: FAIL (current template lacks the new strings/tokens).

- [ ] **Step 3: Add plain-word sub-labels to the KPI strip**

In `poster/poster.template.html`, replace the `.kpi-strip` section (lines ~21-25) with:

```html
  <section class="kpi-strip">
    <div class="kpi kpi-blue"><span class="n">{{val:r2_real_low}} &rarr; {{val:r2_real_high}}</span><span class="l">what a live forecaster sees (rises)</span><span class="sl">realised-return R&sup2;</span></div>
    <div class="kpi kpi-red"><span class="n">{{val:r2_da_low}} &rarr; {{val:r2_da_high}}</span><span class="l">the genuinely independent signal (falls)</span><span class="sl">demand-adjusted R&sup2;</span></div>
    <div class="kpi kpi-gold"><span class="n">{{val:phi_low}} &rarr; {{val:phi_high}}</span><span class="l">the market's memory stiffens</span><span class="sl">effective persistence &phi;</span></div>
  </section>
```

- [ ] **Step 4: Replace the hero band with the setup row (two-card decomposition + price path)**

Replace the entire `<section class="hero">...</section>` block (lines ~27-75) with:

```html
  <section class="setup">
    <div class="setup-left">
      <h2 class="hero-h">One forecast, two channels</h2>
      <div class="eq decomposition">{{eq:decomposition}}</div>
      <div class="channel-cards">
        <div class="cc cc-blue">
          <span class="cc-title">Self-fulfilment</span>
          <span class="cc-sym">&mu;D<sub>t</sub></span>
          <span class="cc-text">the price move the adopters' own coordinated trades create. The forecast bends the market toward itself.</span>
        </div>
        <div class="cc cc-red">
          <span class="cc-title">Independent signal</span>
          <span class="cc-sym">x<sub>t+1</sub></span>
          <span class="cc-text">what tomorrow's return would have been with no crowd pushing the price. The genuine, gradeable skill.</span>
        </div>
      </div>
      <div class="fig feedback">
        <svg viewBox="0 0 240 58" font-family="Inter, sans-serif">
          <rect x="2" y="6" width="60" height="24" rx="3" fill="#fff" stroke="#1F4E79" stroke-width="1.4"/>
          <text x="32" y="22" font-size="9" text-anchor="middle" fill="#1F4E79">forecast</text>
          <rect x="90" y="6" width="60" height="24" rx="3" fill="#fff" stroke="#1F4E79" stroke-width="1.4"/>
          <text x="120" y="22" font-size="9" text-anchor="middle" fill="#1F4E79">demand</text>
          <rect x="178" y="6" width="60" height="24" rx="3" fill="#fff" stroke="#1F4E79" stroke-width="1.4"/>
          <text x="208" y="22" font-size="9" text-anchor="middle" fill="#1F4E79">price move</text>
          <line x1="62" y1="18" x2="86" y2="18" stroke="#1F4E79" stroke-width="1.6"/>
          <polygon points="86,15 90,18 86,21" fill="#1F4E79"/>
          <line x1="150" y1="18" x2="174" y2="18" stroke="#1F4E79" stroke-width="1.6"/>
          <polygon points="174,15 178,18 174,21" fill="#1F4E79"/>
          <path d="M208,30 q0,20 -106,20 q-100,0 -100,-20" fill="none" stroke="#5B6670" stroke-width="1.3" stroke-dasharray="3 3"/>
          <polygon points="5,33 2,30 8,30" fill="#5B6670"/>
          <text x="60" y="56" font-size="8" fill="#5B6670">adopters' demand feeds back into price</text>
        </svg>
      </div>
    </div>
    <div class="setup-right">
      <h2 class="hero-h">One simulated market</h2>
      <div class="fig price-path">
        <svg viewBox="0 0 320 120" font-family="Inter, sans-serif">
          <line x1="8" y1="112" x2="312" y2="112" stroke="#DDE3EA" stroke-width="1"/>
          <g transform="translate(8,8)">
            <path d="{{val:price_path_d}}" fill="none" stroke="#1B6FC4" stroke-width="1.6"/>
          </g>
        </svg>
      </div>
      <p class="cap">one simulated market: the price wanders, one-period returns look like noise. Every figure flows from one reproducible seed.</p>
    </div>
  </section>

  <section class="headline">
    <h2 class="hero-h headline-h">As adoption rises, one forecast earns two verdicts</h2>
    <div class="fig result-curve">
      <svg viewBox="0 0 320 160" font-family="Inter, sans-serif">
        <line x1="40" y1="136" x2="310" y2="136" stroke="#5B6670" stroke-width="1.2"/>
        <line x1="40" y1="16" x2="40" y2="136" stroke="#5B6670" stroke-width="1.2"/>
        <text x="34" y="20" text-anchor="end" font-size="8" fill="#5B6670">0.2</text>
        <text x="34" y="139" text-anchor="end" font-size="8" fill="#5B6670">0</text>
        <text x="40" y="150" text-anchor="middle" font-size="8" fill="#5B6670">0</text>
        <text x="175" y="150" text-anchor="middle" font-size="8" fill="#5B6670">adoption share</text>
        <text x="310" y="150" text-anchor="middle" font-size="8" fill="#5B6670">1</text>
        <g transform="translate(40,16)">
          <path d="{{val:result_da_d}}" fill="none" stroke="#C62828" stroke-width="2.4"/>
          <path d="{{val:result_real_d}}" fill="none" stroke="#1B6FC4" stroke-width="2.4"/>
        </g>
        <text x="300" y="40" text-anchor="end" font-size="9" font-weight="700" fill="#1B6FC4">realised R&sup2; rises to {{val:result_high_real}}</text>
        <text x="300" y="128" text-anchor="end" font-size="9" font-weight="700" fill="#C62828">demand-adjusted R&sup2; falls to {{val:result_high_da}}</text>
      </svg>
    </div>
    <p class="cap">rolling out-of-sample R&sup2; against each target, extended saturated regime (T = 30,000). The two readings of the same forecast pull apart as the crowd grows.</p>
  </section>
```

- [ ] **Step 5: Sharpen the question hook (column 1)**

Replace the "The question" paragraph (line ~82) with a leading one-line hook:

```html
        <p><b>If everyone trades on the same forecast, does it get better, or just bend the market into agreeing?</b> Publish one forecast of tomorrow's return and traders begin acting on it. Their coordinated buying and selling pushes the very price the forecast will later be graded against.</p>
```

- [ ] **Step 6: Replace column two's small steady-state with the enlarged version**

In column two, replace the existing `<section>` containing `A steady state, not a transient` and its small SVG (lines ~109-130) with:

```html
      <section>
        <h2>A steady state, not a transient</h2>
        <div class="fig steady">
          <svg viewBox="0 0 320 200" font-family="Inter, sans-serif">
            <text x="6" y="14" fill="#1F4E79" font-size="11" font-weight="700">Run 30,000 steps: both readings stay put</text>
            <line x1="44" y1="24" x2="44" y2="174" stroke="#5B6670" stroke-width="1.2"/>
            <line x1="44" y1="174" x2="304" y2="174" stroke="#5B6670" stroke-width="1.2"/>
            <text x="38" y="28" text-anchor="end" fill="#5B6670" font-size="8">0.2</text>
            <text x="38" y="176" text-anchor="end" fill="#5B6670" font-size="8">0</text>
            <line x1="44" y1="{{val:steady_real_y}}" x2="304" y2="{{val:steady_real_y}}" stroke="#1B6FC4" stroke-width="3"/>
            <text x="300" y="{{val:steady_real_y}}" dy="-5" text-anchor="end" fill="#1B6FC4" font-size="10" font-weight="700">realised &#8776; {{val:plateau_real}}</text>
            <line x1="44" y1="{{val:steady_da_y}}" x2="304" y2="{{val:steady_da_y}}" stroke="#C62828" stroke-width="3"/>
            <text x="300" y="{{val:steady_da_y}}" dy="-5" text-anchor="end" fill="#C62828" font-size="10" font-weight="700">demand-adjusted &#8776; {{val:plateau_da}}</text>
            <line x1="120" y1="{{val:steady_real_y}}" x2="120" y2="{{val:steady_da_y}}" stroke="#1F4E79" stroke-width="1.3"/>
            <text x="128" y="110" fill="#1F4E79" font-size="10" font-weight="700">gap stays open</text>
            <text x="44" y="192" fill="#5B6670" font-size="8">time period &#8594; 30,000 &#183; 50 seeds &#183; not a start-up transient</text>
          </svg>
        </div>
      </section>
```

- [ ] **Step 7: Run the template test**

Run: `python3 -m pytest tests/test_poster_template.py -q`
Expected: PASS (`test_template_has_required_content` and `test_css_is_a0_portrait`).

- [ ] **Step 8: Commit**

```bash
git add poster/poster.template.html tests/test_poster_template.py
git commit -m "poster: narrative-spine template with real price path and result curve"
```

---

### Task 5: Style the new blocks (CSS)

**Files:**
- Modify: `poster/poster.css`

- [ ] **Step 1: Add the KPI sub-label style**

In `poster/poster.css`, after the `.kpi .l { ... }` rule (line ~39), add:

```css
.kpi .sl { font-size:7.5mm; color:var(--mute); margin-top:1mm; display:block; font-family:var(--mono); opacity:.8; }
```

- [ ] **Step 2: Replace the `.hero` rules with `.setup` + `.headline` + channel-card + figure rules**

Replace the "Hero band" block (lines ~44-55) with:

```css
/* Setup row */
.setup { display:grid; grid-template-columns:1fr 1fr; gap:18mm; padding:11mm 24mm; background:var(--panel); border-bottom:1.5mm solid var(--hair); align-items:start; }
.setup-left, .setup-right { display:flex; flex-direction:column; }
.hero-h { font-family:var(--serif); color:var(--navy); font-size:13mm; margin:0 0 4mm; }
.fig { width:100%; }
.fig svg { width:100%; height:auto; display:block; }
.eq.decomposition { font-size:16mm; text-align:center; margin:1mm 0 4mm; }

/* Two named decomposition cards */
.channel-cards { display:grid; grid-template-columns:1fr 1fr; gap:8mm; margin:0 0 5mm; }
.cc { background:#fff; border-radius:5mm; padding:6mm 7mm; border-top:2.4mm solid; display:flex; flex-direction:column; gap:2mm; }
.cc-blue { border-color:var(--blue); } .cc-red { border-color:var(--red); }
.cc-title { font-weight:700; font-size:9mm; text-transform:uppercase; letter-spacing:.03em; }
.cc-blue .cc-title { color:var(--blue); } .cc-red .cc-title { color:var(--red); }
.cc-sym { font-family:var(--serif); font-size:12mm; }
.cc-blue .cc-sym { color:var(--blue); } .cc-red .cc-sym { color:var(--red); }
.cc-text { font-size:8.6mm; color:#34404d; line-height:1.3; }
.feedback { max-width:300mm; margin:2mm auto 0; }
.price-path { margin-top:1mm; }

/* Full-width headline result curve */
.headline { padding:9mm 24mm 11mm; background:var(--panel); border-bottom:1.5mm solid var(--hair); }
.headline-h { text-align:center; }
.result-curve { max-width:560mm; margin:0 auto; }
```

- [ ] **Step 3: Enlarge the steady-state figure**

Replace the `.steady { ... }` rule (line ~68) with:

```css
.steady { max-width:none; margin-top:1mm; }
.steady svg { max-height:none; }
```

(The enlarged viewBox does the sizing; this just removes any height clamp.)

- [ ] **Step 4: Commit**

```bash
git add poster/poster.css
git commit -m "poster: style decomposition cards, headline curve, enlarged steady state"
```

---

### Task 6: Build, verify, and visual review

**Files:**
- Produces: `poster/poster.html`, `results/poster/poster.pdf`, preview PNG.

- [ ] **Step 1: Regenerate values + render the PDF**

Run: `cd poster && python3 figures.py && node build.mjs && cd ..`
Expected: prints `wrote figure_values.json` then `wrote results/poster/poster.pdf`. If `node build.mjs` errors on a missing module, run `cd poster && npm install && cd ..` first; if it errors on Chrome, confirm `/Applications/Google Chrome.app` exists.

- [ ] **Step 2: Confirm no unfilled tokens and a single A0 page**

Run: `python3 -m pytest tests/test_poster_pdf.py -q`
Expected: PASS (`test_pdf_is_single_a0_page`, `test_no_unfilled_tokens`).

- [ ] **Step 3: Run the full poster test suite**

Run: `python3 -m pytest tests/ -q -k poster`
Expected: PASS for all poster tests (template, figures, pdf, assets, schematic). No remaining failures from the stale set.

- [ ] **Step 4: Render a preview PNG and review it visually**

Run: `cd poster && node -e "import('puppeteer-core').then(async p=>{const b=await p.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true,args:['--no-sandbox']});const pg=await b.newPage();await pg.goto('file://'+process.cwd()+'/poster.html',{waitUntil:'networkidle0'});await pg.setViewport({width:1416,height:2000,deviceScaleFactor:1});await pg.screenshot({path:'../results/poster/poster_preview.png',fullPage:true});await b.close()})" && cd ..`
Expected: writes `results/poster/poster_preview.png`.
Then Read the preview PNG and check against this plan: (a) the two decomposition cards render with blue/red top borders and readable plain text; (b) the price path shows a clean blue wandering line; (c) the full-width result curve shows blue rising and red falling against adoption share with endpoint labels; (d) the steady-state is visibly larger with its two plateau lines at the data-driven heights and the "gap stays open" marker; (e) the KPI sub-labels read in plain words; (f) no clipped content, no empty corners, single page.

- [ ] **Step 5: Push the preview to the visual companion (if the brainstorm server is still up) and iterate**

If `/Users/janwejchert/Desktop/Capstone/Capstone/.superpowers/brainstorm/*/state/server-info` exists and no `server-stopped` sibling, write an `<img>` screen referencing the preview via the server's `/files/` route so the user can see the rendered poster, and adjust geometry literals (SVG plot rects, font sizes, paddings) against the render. Re-run Step 1 after any tweak.

- [ ] **Step 6: Final commit**

```bash
git add poster/poster.html results/poster/poster.pdf results/poster/poster_preview.png
git commit -m "poster: build narrative-spine redesign, single A0 page verified"
```

---

## Self-Review

**Spec coverage:**
- More visual / market simulation shown -> Tasks 2-4 (price path + result curve as real SVG). Covered.
- Plain-language basics -> Task 4 Steps 3, 5 (KPI sub-labels, question hook) + the two-card decomposition. Covered.
- Return decomposition explains `x_{t+1}` -> Task 4 Step 4 (two named cards). Covered.
- Steady-state bigger -> Task 4 Step 6 + Task 5 Step 3. Covered.
- On-brand SVG, not matplotlib PNG -> Tasks 1-4 all render SVG. Covered.
- Reproducibility / saved data -> Task 2 (`poster_result_curve.npz`), Task 3 (geometry from saved npz + phase_01 prices). Covered.
- Number reconciliation -> "Number-sourcing decision" section: KPI from cross-regime summary, curve/steady-state from the within-run MC, labelled with their own values. Covered.
- Build mechanics / single A0 page -> Task 6. Covered.
- Stale failing tests -> repaired in Task 1 (figures) and Task 4 (template). Covered.

**Placeholder scan:** No TBD/TODO. The only open item is the carried-over logo swap (out of scope here, noted in the spec).

**Type/name consistency:** `make_polyline` signature, the `compute_result_curve` dict keys, `RESULT_NPZ`, `ASSETS`, and the `{{val:...}}` token names (`price_path_d`, `result_real_d`, `result_da_d`, `result_high_real`, `result_high_da`, `plateau_real`, `plateau_da`, `steady_real_y`, `steady_da_y`) are used identically in `figures.py` (Tasks 2-3), the tests, and the template (Task 4). Geometry constants (result rect 40/16/270/120; steady rect 44/24/250/150; ymax 0.2) match between `figures.py` and the template SVGs.
