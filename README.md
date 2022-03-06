# RM-MEDA-PY3
Python 3 version of RM-MEDA algorithm

Original Project (Python 2): https://github.com/ahcheriet/RM-MEDA_py

Local PCA and Generate: The code is translated from Matlab PlatEMO framework.


Requirements:

1- Numpy and matplotlib

2- PyGMO 2

### P-Distance
| problem   | MACO          | MOEA/D        | NSGA-II       | NSPSO         | RM-MEDA       |
|:----------|:--------------|:--------------|:--------------|:--------------|:--------------|
| ZDT-1     | 0.311 (0.273) | 0.215 (0.043) | 0.011 (0.001) | 0.051 (0.018) | 0.401 (0.043) |
| ZDT-2     | 0.466 (0.226) | 0.201 (0.047) | 0.008 (0.001) | 0.024 (0.016) | 0.455 (0.099) |
| ZDT-3     | 0.592 (0.443) | 0.373 (0.021) | 0.019 (0.002) | 0.393 (0.156) | 1.045 (0.059) |

### Crowding Distance
| problem   | MACO          | MOEA/D        | NSGA-II       | NSPSO         | RM-MEDA       |
|:----------|:--------------|:--------------|:--------------|:--------------|:--------------|
| ZDT-1     | 0.057 (0.005) | 0.029 (0.003) | 0.020 (0.000) | 0.049 (0.009) | 0.049 (0.004) |
| ZDT-2     | 0.366 (0.133) | 0.049 (0.006) | 0.020 (0.001) | 0.045 (0.010) | 0.156 (0.135) |
| ZDT-3     | 0.058 (0.004) | 0.034 (0.005) | 0.020 (0.000) | 0.174 (0.034) | 0.079 (0.011) |