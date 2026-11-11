# Review round 6 — Reviewer #6 (computational cost, scalability, deployment)

## Issues

| # | Severity | Issue | Required fix | Status |
|---|---|---|---|---|
| 6.1 | MAJOR | STRATA's overhead was *estimated* ("about one order of magnitude"), not measured. | Measure wall-clock of the full procedure vs the bare learner. | **Fixed** — E11: 2.3–7.0 s vs 0.3–0.5 s (XGBoost, all development studies, 1 and 4 threads). |
| 6.2 | MODERATE | Peak-memory numbers for some learners are 0 MB because `ru_maxrss` measures the process peak, dominated by data loading. | Clarify that the metric is the increase over the post-loading baseline. | **Fixed** — Table 8 column is "Peak RSS increase"; note in caption. |
| 6.3 | MODERATE | GPBoost could not be serialised with pickle (size reported as n/a). | Report as n/a. | Accepted. |
| 6.4 | MINOR | Is the method worth its cost? The cost is seconds; the benefit (valid intervals) is decisive for screening. | — | Stated. |
| 6.5 | MINOR | Hardware: 4-core CPU, no GPU; no accelerator needed. | State in §2.8. | ✓ |

No scalability concern: the data set has ~2,000 runs per target; all steps are O(n log n) or tree-ensemble fits.
