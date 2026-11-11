**Table 8. Computational cost (bio-oil, development set, single thread).**

| Learner       |   Fit time (s) |   Predict (ms / 1000 rows) |   Peak RSS increase (MB) |   Serialized size (MB) |
|:--------------|---------------:|---------------------------:|-------------------------:|-----------------------:|
| Mean          |          0.008 |                      0.028 |                    0     |                  0     |
| Ridge         |          0.011 |                      0.461 |                    0     |                  0.003 |
| Random forest |          2.849 |                     31.855 |                    6.727 |                 18.286 |
| LightGBM      |          0.249 |                     32.046 |                    0     |                  0.972 |
| GPBoost       |          0.4   |                     26.981 |                   17.203 |                nan     |
