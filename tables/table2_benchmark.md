**Table 2. Random-row versus study-grouped cross-validation on development studies (base features; grouped CV averaged over 3 seeds).**

| Target   | Learner       |   Random CV RMSE |   Random CV R² |   Grouped CV RMSE |   Grouped CV R² |   RMSE ratio (grouped/random) |
|:---------|:--------------|-----------------:|---------------:|------------------:|----------------:|------------------------------:|
| Bio-oil  | Extra trees   |             8.64 |          0.77  |             15.73 |           0.237 |                          1.82 |
| Bio-oil  | SVR           |            10.38 |          0.668 |             15.8  |           0.23  |                          1.52 |
| Bio-oil  | XGBoost       |             7.81 |          0.812 |             15.8  |           0.23  |                          2.02 |
| Bio-oil  | Random forest |             8.45 |          0.78  |             16.01 |           0.21  |                          1.89 |
| Bio-oil  | LightGBM      |             7.61 |          0.821 |             16.11 |           0.2   |                          2.12 |
| Bio-oil  | k-NN          |            10.27 |          0.675 |             16.26 |           0.185 |                          1.58 |
| Bio-oil  | CatBoost      |             7.68 |          0.818 |             16.54 |           0.156 |                          2.15 |
| Bio-oil  | HistGB        |             7.8  |          0.812 |             16.74 |           0.136 |                          2.15 |
| Bio-oil  | Ridge         |            15.02 |          0.304 |             17.51 |           0.054 |                          1.17 |
| Bio-oil  | GPBoost       |            17.32 |          0.075 |             17.61 |           0.043 |                          1.02 |
| Bio-oil  | Mean          |            18.02 |         -0.001 |             18.12 |          -0.013 |                          1.01 |
| Bio-oil  | MLP           |             9.19 |          0.74  |             23.95 |          -0.77  |                          2.61 |
| Solid    | LightGBM      |             6.96 |          0.882 |             13.7  |           0.541 |                          1.97 |
| Solid    | XGBoost       |             7.02 |          0.88  |             14.14 |           0.511 |                          2.02 |
| Solid    | HistGB        |             7.03 |          0.879 |             14.15 |           0.511 |                          2.01 |
| Solid    | Random forest |             8.61 |          0.819 |             14.42 |           0.492 |                          1.67 |
| Solid    | CatBoost      |             7.12 |          0.876 |             14.48 |           0.488 |                          2.03 |
| Solid    | k-NN          |             9.84 |          0.764 |             14.77 |           0.467 |                          1.5  |
| Solid    | SVR           |             9.56 |          0.777 |             15.01 |           0.45  |                          1.57 |
| Solid    | Extra trees   |             8.23 |          0.835 |             15.07 |           0.445 |                          1.83 |
| Solid    | Ridge         |            13.96 |          0.524 |             16.34 |           0.348 |                          1.17 |
| Solid    | MLP           |             8.57 |          0.821 |             19.51 |           0.07  |                          2.28 |
| Solid    | GPBoost       |            19.13 |          0.106 |             19.81 |           0.042 |                          1.04 |
| Solid    | Mean          |            20.25 |         -0.001 |             20.63 |          -0.039 |                          1.02 |
