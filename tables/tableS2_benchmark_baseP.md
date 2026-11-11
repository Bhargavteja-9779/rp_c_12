**Table S2. Benchmark with base + protocol (P) features.**

| Target   | Learner       |   Random CV RMSE |   Grouped CV RMSE |   Grouped CV R² |
|:---------|:--------------|-----------------:|------------------:|----------------:|
| Bio-oil  | LightGBM      |             7.53 |             16.01 |           0.209 |
| Bio-oil  | Random forest |             8.33 |             16.23 |           0.188 |
| Bio-oil  | XGBoost       |             7.65 |             16.33 |           0.178 |
| Bio-oil  | Extra trees   |             8.33 |             16.35 |           0.176 |
| Bio-oil  | SVR           |            11.04 |             16.45 |           0.165 |
| Bio-oil  | CatBoost      |             7.66 |             16.62 |           0.148 |
| Bio-oil  | HistGB        |             7.81 |             16.9  |           0.119 |
| Bio-oil  | k-NN          |            10.01 |             17.15 |           0.093 |
| Bio-oil  | GPBoost       |            17.29 |             17.61 |           0.044 |
| Bio-oil  | Ridge         |            14.15 |             17.73 |           0.03  |
| Bio-oil  | Mean          |            18.02 |             18.12 |          -0.013 |
| Bio-oil  | MLP           |             8.63 |             23.32 |          -0.681 |
| Solid    | LightGBM      |             7.03 |             13.65 |           0.544 |
| Solid    | XGBoost       |             7.06 |             14.08 |           0.516 |
| Solid    | HistGB        |             7.07 |             14.17 |           0.51  |
| Solid    | Random forest |             8.6  |             14.22 |           0.506 |
| Solid    | CatBoost      |             7.66 |             14.64 |           0.476 |
| Solid    | Extra trees   |             8.18 |             15.3  |           0.428 |
| Solid    | SVR           |             9.12 |             16.31 |           0.35  |
| Solid    | Ridge         |            13.44 |             16.63 |           0.324 |
| Solid    | k-NN          |             9.95 |             16.74 |           0.316 |
| Solid    | GPBoost       |            19.14 |             19.85 |           0.038 |
| Solid    | MLP           |             8.03 |             20.35 |          -0.012 |
| Solid    | Mean          |            20.25 |             20.63 |          -0.039 |
