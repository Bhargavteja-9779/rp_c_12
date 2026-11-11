**Table S. Per-study RMSE of each learner vs the best learner under grouped CV (Wilcoxon, Holm).**

| target   | features   | learner   | reference   |   n |   median_diff |   ci_low |   ci_high |   rank_biserial |      p |   p_holm |
|:---------|:-----------|:----------|:------------|----:|--------------:|---------:|----------:|----------------:|-------:|---------:|
| biooil   | base       | gpboost   | rf          | 122 |        0.4153 |  -0.4452 |    2.1135 |          0.2166 | 0.0379 |   0.0758 |
| biooil   | base       | lgbm      | rf          | 122 |        0.2408 |  -0.6774 |    0.6364 |          0.0079 | 0.9399 |   0.9399 |
| biooil   | base       | mean      | rf          | 122 |        0.5691 |  -0.2284 |    2.3849 |          0.2379 | 0.0226 |   0.0678 |
| biooil   | base       | ridge     | rf          | 122 |        1.3573 |   0.5737 |    2.662  |          0.3349 | 0.0013 |   0.0053 |
| biooil   | base+P     | gpboost   | lgbm        | 122 |        0.4819 |  -0.6516 |    2.1025 |          0.1955 | 0.0609 |   0.1218 |
| biooil   | base+P     | mean      | lgbm        | 122 |        0.7579 |  -0.6918 |    2.3941 |          0.215  | 0.0393 |   0.118  |
| biooil   | base+P     | rf        | lgbm        | 122 |        0.1731 |  -0.4097 |    0.8277 |          0.0881 | 0.3984 |   0.3984 |
| biooil   | base+P     | ridge     | lgbm        | 122 |        2.4994 |   1.1214 |    3.6098 |          0.3893 | 0.0002 |   0.0008 |
| solid    | base       | gpboost   | lgbm        | 120 |        5.0689 |   3.4966 |    6.7756 |          0.6366 | 0      |   0      |
| solid    | base       | mean      | lgbm        | 120 |        5.3652 |   3.7036 |    6.999  |          0.6554 | 0      |   0      |
| solid    | base       | rf        | lgbm        | 120 |       -0.0261 |  -0.5077 |    0.7554 |          0.089  | 0.3976 |   0.3976 |
| solid    | base       | ridge     | lgbm        | 120 |        1.4838 |   0.6513 |    2.1398 |          0.3961 | 0.0002 |   0.0003 |
| solid    | base+P     | gpboost   | rf          | 120 |        4.6399 |   3.9838 |    6.4694 |          0.6837 | 0      |   0      |
| solid    | base+P     | lgbm      | rf          | 120 |        0.0613 |  -0.489  |    0.6782 |          0.005  | 0.9624 |   0.9624 |
| solid    | base+P     | mean      | rf          | 120 |        5.0361 |   4.131  |    6.8588 |          0.7014 | 0      |   0      |
| solid    | base+P     | ridge     | rf          | 120 |        1.7791 |   0.8484 |    3.1644 |          0.3975 | 0.0002 |   0.0003 |
