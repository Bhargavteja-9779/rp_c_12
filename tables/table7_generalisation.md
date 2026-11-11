**Table 7. Temporal, feedstock-family and external generalisation of the STRATA base learner.**

| Target   | Features   | Scheme                          |   RMSE |     R² |   Median study RMSE |
|:---------|:-----------|:--------------------------------|-------:|-------:|--------------------:|
| Bio-oil  | base       | temporal                        |  19.41 | -0.399 |               14.81 |
| Bio-oil  | base+P     | temporal                        |  22.66 | -0.907 |               16.96 |
| Solid    | base       | temporal                        |  16.54 |  0.269 |               10.58 |
| Solid    | base+P     | temporal                        |  16.56 |  0.268 |               10.83 |
| Bio-oil  | base       | family_out (mean over families) |  17.17 | -0.419 |               12.93 |
| Bio-oil  | base+P     | family_out (mean over families) |  17.48 | -0.237 |               12.05 |
| Solid    | base       | family_out (mean over families) |  16.35 | -0.221 |               10.79 |
| Solid    | base+P     | family_out (mean over families) |  15.5  | -0.03  |               10.28 |
| Solid    | base       | external_4TU_all_dev_processes  |  13.3  |  0.31  |               10.93 |
| Solid    | base       | external_4TU_HTC_dev_only       |  16.66 | -0.082 |               11.59 |
