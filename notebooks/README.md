# Notebooks

One notebook per phase. Run them in order. See `../CLAUDE.md` for what each
phase delivers and the order of construction, and `../docs/proposal/reflexive_forecast_proposal_v3.pdf`
for the endpoint definitions. All seven phases are implemented.

| Phase | Status  | File                                       | Goal                                                                              |
|-------|---------|--------------------------------------------|-----------------------------------------------------------------------------------|
| 1     | done    | `phase_01_baseline_market.ipynb`           | Baseline market with null traders only                                            |
| 2     | done    | `phase_02_benchmark_validation.ipynb`      | Stable descriptive stats across seeds                                             |
| 3     | done    | `phase_03_ar_forecast.ipynb`               | Rolling AR forecast offline, no adoption                                          |
| 4     | done    | `phase_04_stochastic_adoption.ipynb`       | Forecast-based trading; the dual-channel R^2 result first appears                 |
| 5     | done    | `phase_05_performance_adoption.ipynb`      | Risk-adjusted CE-based switching, compared to stochastic on paired shocks         |
| 6     | done    | `phase_06_experiments_threshold.ipynb`     | Sweep (mu, phi, w, p); locate `A*_{R2,resid,rel}` and `A*_{phi,rel}` heatmaps     |
| 7     | done    | `phase_07_evaluation_extensions.ipynb`     | Summary plus transaction-cost extension; `A*_{profit}` against zero and the null  |

Every notebook starts with a parameters cell. Edit those values to explore
variations. Do not hard-code numbers later in the notebook.
