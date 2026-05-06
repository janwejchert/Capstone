# Notebooks

One notebook per phase. Run them in order. See `../CLAUDE.md` for what each
phase delivers and the order of construction.

| Phase | File                                       | Goal                                            |
|-------|--------------------------------------------|-------------------------------------------------|
| 1     | `phase_01_baseline_market.ipynb`           | Baseline market with null traders only          |
| 2     | `phase_02_benchmark_validation.ipynb`      | Stable descriptive stats across seeds           |
| 3     | `phase_03_ar_forecast.ipynb`               | Rolling AR forecast, no adoption                |
| 4     | `phase_04_stochastic_adoption.ipynb`       | Forecast-based trading and stochastic adoption  |
| 5     | `phase_05_performance_adoption.ipynb`      | Risk-adjusted performance-based adoption        |
| 6     | `phase_06_experiments_threshold.ipynb`     | Sweep parameters, locate the critical share A*  |
| 7     | `phase_07_evaluation_extensions.ipynb`     | Summary plus one extension                      |

Every notebook starts with a parameters cell. Edit those values to explore
variations. Do not hard-code numbers later in the notebook.
