"""Rolling autoregressive forecast.

Implements equations (9), (10) from the proposal. Estimation uses
np.linalg.lstsq on a lagged design matrix. Added in phase 3.
"""
