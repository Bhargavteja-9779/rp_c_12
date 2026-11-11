**Table 8. Computational cost (bio-oil, development set, single thread).**

| Learner       |   Fit time (s) |   Predict (ms / 1000 rows) |   Peak RSS increase (MB) |   Serialized size (MB) |
|:--------------|---------------:|---------------------------:|-------------------------:|-----------------------:|
| Mean          |          0.006 |                      0.024 |                    0     |                  0     |
| Ridge         |          0.013 |                      0.525 |                    0     |                  0.003 |
| k-NN          |          0.013 |                     16.627 |                    0     |                  0.624 |
| SVR           |          0.169 |                     68.935 |                    2.488 |                  0.438 |
| MLP           |          9.265 |                      1.186 |                    0     |                  0.146 |
| Random forest |          1.54  |                     35.689 |                   14.715 |                 25.699 |
| Extra trees   |          0.919 |                     45.194 |                   17.254 |                 28.432 |
| HistGB        |          1.295 |                     25.176 |                    0     |                  2.672 |
| LightGBM      |          0.577 |                     81.663 |                    9.906 |                  3.214 |
| XGBoost       |          0.194 |                      4.017 |                    5.891 |                  0.867 |
| CatBoost      |          3.445 |                      1.236 |                   39.953 |                  3.705 |
| GPBoost       |          0.448 |                     46.436 |                   17.918 |                nan     |
