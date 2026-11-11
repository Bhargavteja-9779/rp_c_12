**Table 6. Single evaluation on the 38 locked test studies (models trained on all development studies, base features).**

| Target   | Learner       |   Runs |   Studies |   RMSE |     R² |   Median study RMSE |
|:---------|:--------------|-------:|----------:|-------:|-------:|--------------------:|
| Bio-oil  | k-NN          |    556 |        28 | 12.878 |  0.029 |              11.935 |
| Bio-oil  | Ridge         |    556 |        28 | 12.965 |  0.016 |              11.992 |
| Bio-oil  | GPBoost       |    556 |        28 | 13.209 | -0.021 |              10.769 |
| Bio-oil  | CatBoost      |    556 |        28 | 13.389 | -0.049 |              10.778 |
| Bio-oil  | Mean          |    556 |        28 | 13.634 | -0.088 |              11.123 |
| Bio-oil  | SVR           |    556 |        28 | 13.913 | -0.133 |              11.882 |
| Bio-oil  | Extra trees   |    556 |        28 | 14.643 | -0.255 |              11.336 |
| Bio-oil  | Random forest |    556 |        28 | 15.692 | -0.441 |               9.709 |
| Bio-oil  | XGBoost       |    556 |        28 | 18.273 | -0.954 |               9.597 |
| Bio-oil  | LightGBM      |    556 |        28 | 20.122 | -1.37  |               9.648 |
| Bio-oil  | MLP           |    556 |        28 | 22.521 | -1.969 |              14.511 |
| Bio-oil  | HistGB        |    556 |        28 | 22.839 | -2.053 |               9.766 |
| Solid    | MLP           |    457 |        30 | 14.416 |  0.573 |              10.978 |
| Solid    | Extra trees   |    457 |        30 | 16.546 |  0.438 |              12.349 |
| Solid    | SVR           |    457 |        30 | 17.052 |  0.403 |              12.653 |
| Solid    | k-NN          |    457 |        30 | 18.401 |  0.305 |              11.857 |
| Solid    | XGBoost       |    457 |        30 | 18.528 |  0.295 |              13.71  |
| Solid    | Ridge         |    457 |        30 | 18.744 |  0.279 |              14.67  |
| Solid    | LightGBM      |    457 |        30 | 18.889 |  0.268 |              12.971 |
| Solid    | HistGB        |    457 |        30 | 19.196 |  0.244 |              13.187 |
| Solid    | Random forest |    457 |        30 | 19.316 |  0.234 |              12.56  |
| Solid    | CatBoost      |    457 |        30 | 19.809 |  0.194 |              13.243 |
| Solid    | GPBoost       |    457 |        30 | 21.937 |  0.012 |              17.291 |
| Solid    | Mean          |    457 |        30 | 23.03  | -0.089 |              17.925 |
