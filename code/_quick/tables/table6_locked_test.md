**Table 6. Single evaluation on the 38 locked test studies (models trained on all development studies, base features).**

| Target   | Learner       |   Runs |   Studies |   RMSE |     R² |   Median study RMSE |
|:---------|:--------------|-------:|----------:|-------:|-------:|--------------------:|
| Bio-oil  | Random forest |    556 |        25 | 20.124 | -0.005 |               9.331 |
| Bio-oil  | GPBoost       |    556 |        25 | 20.264 | -0.019 |              12.538 |
| Bio-oil  | Mean          |    556 |        25 | 20.393 | -0.032 |              12.673 |
| Bio-oil  | LightGBM      |    556 |        25 | 21.524 | -0.15  |              12.063 |
| Bio-oil  | Ridge         |    556 |        25 | 22.34  | -0.239 |              12.678 |
| Solid    | LightGBM      |    441 |        24 | 16.489 |  0.178 |              11.462 |
| Solid    | Ridge         |    441 |        24 | 16.712 |  0.156 |              12.381 |
| Solid    | Random forest |    441 |        24 | 17.994 |  0.021 |              12.55  |
| Solid    | GPBoost       |    441 |        24 | 18.163 |  0.003 |              17.602 |
| Solid    | Mean          |    441 |        24 | 18.375 | -0.021 |              17.904 |
