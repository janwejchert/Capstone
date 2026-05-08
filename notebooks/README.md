# Notebooks

One notebook per phase. Run them in order. See `../CLAUDE.md` for what each
phase delivers and the order of construction. Phases 1-5 are implemented
so far. Phases 6-7 are planned and listed for reference.

| Phase | Status  | File                                       | Goal                                            |
|-------|---------|--------------------------------------------|-------------------------------------------------|
| 1     | done    | `phase_01_baseline_market.ipynb`           | Baseline market with null traders only          |
| 2     | done    | `phase_02_benchmark_validation.ipynb`      | Stable descriptive stats across seeds           |
| 3     | done    | `phase_03_ar_forecast.ipynb`               | Rolling AR forecast, no adoption                |
| 4     | done    | `phase_04_stochastic_adoption.ipynb`       | Forecast-based trading and stochastic adoption  |
| 5     | done    | `phase_05_performance_adoption.ipynb`      | Risk-adjusted performance-based adoption        |
| 6     | planned | `phase_06_experiments_threshold.ipynb`     | Sweep parameters, locate the critical share A*  |
| 7     | planned | `phase_07_evaluation_extensions.ipynb`     | Summary plus one extension                      |

Every notebook starts with a parameters cell. Edit those values to explore
variations. Do not hard-code numbers later in the notebook.
