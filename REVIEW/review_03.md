# Review round 3 — Reviewer #3 (statistics, fairness, splitting, leakage)

## Checks performed
* Unit of analysis: source study for all tests (Wilcoxon on per-study metrics, cluster bootstrap) — appropriate for clustered data.
* Seeds pre-specified in `config/default.yaml` (outer {11,22,33}; learner 0; bootstrap 0; k-shot draws 0–19) and committed before running (git history).
* Multiplicity: Holm within each family (learner comparisons per target/feature set; k-shot tests per target/feature set).
* Locked test: list committed in the first commit; evaluated once, after the "decisions frozen" commit (69ccfd1 → 639845a).

## Issues

| # | Severity | Issue | Required fix | Status |
|---|---|---|---|---|
| 3.1 | MAJOR | Coverage CIs on development folds are computed for seed 11 only, while point estimates average three seeds. | State this explicitly in table/figure notes. | **Fixed** — Results text reports CIs "(seed 11)" through the coverage table definition; statistics.json key `coverage_studies_ci_seed1`. Sentence added to Methods §2.7 below. |
| 3.2 | MAJOR | The conformal guarantee of CDF pooling is approximate, marginal over studies, and the calibration residuals come from inner models (CV-style). The first draft implied exact validity. | Qualify in Methods. | **Fixed** — §2.5 now states approximate, marginal validity and the CV approximation. |
| 3.3 | MAJOR | Hyper-parameters were tuned on all development studies with grouped CV, so development-CV estimates are mildly optimistic. | Acknowledge; rely on locked test for unbiased numbers. | **Already stated** (§2.4 "frozen"; PROTOCOL §6); locked results reported in Table 6 and are worse, consistent with this. |
| 3.4 | MODERATE | The SC-vs-RC coverage test has rank-biserial 1.0 — every study improved. That is mechanical (SC quantile ≥ RC quantile). Is the test meaningful? | Report it as descriptive confirmation; the key quantity is coverage relative to nominal with CI. | **Fixed** — emphasis is on coverage with CIs; the test is kept but not used as main evidence. |
| 3.5 | MODERATE | k-shot comparisons pool studies with ≥ 11 runs only (80/72 studies), a selected subset. | State; note that results may not transfer to studies with very few runs. | **Fixed** — stated in §3.5 ("development studies with at least 11 runs"). |
| 3.6 | MODERATE | Locked-test coverage rests on 28–30 studies; CIs are wide (solid SC 0.70–0.92). | Report CIs. | **Fixed** — cluster-bootstrap CIs reported. |
| 3.7 | MINOR | Wilcoxon *p* reported as "< 0.001" — fine; but some k-shot Holm-adjusted *p* are tiny for differences of 0.02 wt% (k = 10). Statistical vs practical significance. | Note that differences at large k are negligible in practice. | **Fixed** — §3.5 states shrinkage matters mainly for k = 1–2. |
| 3.8 | MINOR | Random-row CV for the literature-practice comparison uses one seed. | Acceptable (it serves as reference); stated in Table 2 caption. | Accepted. |

Added to Methods §2.7: "Coverage CIs on development folds were computed for the first outer seed; point estimates average the three seeds."
