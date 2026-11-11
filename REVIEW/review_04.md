# Review round 4 — Reviewer #4 (ML methodology, implementation, code ↔ paper consistency)

Code inspected: `src/data/load.py`, `src/models/registry.py`, `src/models/strata.py`, `src/evaluation/core.py`, `experiments/*.py`, `tests/test_core.py`.

## Consistency checks (paper statement → code)
| Paper | Code | OK? |
|---|---|---|
| Inner study-grouped 5-fold CV for SC residuals | `nested_fit(inner_k=cfg["inner_folds"]=5)` with `grouped_folds` | ✓ |
| RC = unweighted quantile of random-row OOF residuals | `row_quantile(res_rc)`; `random_folds` | ✓ |
| SC = study-weighted quantile (weights 1/n_j) with finite-sample correction | `study_quantile` → `weighted_conformal_quantile` (adds mean-weight test mass) | ✓ (unit-tested) |
| λ = σ²_w/τ² by unbalanced ANOVA MoM | `variance_components` (unit-tested against simulation) | ✓ |
| k-shot: 20 support sets, studies with ≥ 11 runs, support excluded from evaluation | `kshot_eval(min_n=kmax+1)`, `kshot_split` (unit-tested) | ✓ |
| Equal tuning budget, 20 configs, grouped 5-fold | `tune(n_iter=20, k=5)` | ✓ |
| Fold-internal imputation/scaling | pipelines in `registry.py` | ✓ |
| DOI/year never features | `test_no_identifier_features` | ✓ |
| Locked test once | git history; quick mode uses pseudo-split | ✓ |

## Issues

| # | Severity | Issue | Required fix | Status |
|---|---|---|---|---|
| 4.1 | MAJOR | Parts of E10 (locked-vs-dev duplicates, reference values) were produced by an ad-hoc command, not by a script — not reproducible. | Move into `e10_duplicate_audit.py`; verify identical output. | **Fixed** — rerun produced identical JSON. |
| 4.2 | MAJOR | `e11_overhead.py` ignored `--mode`, so `run_all --mode quick` would write into the full results. | Accept mode argument. | **Fixed**. |
| 4.3 | MODERATE | GPBoost behaviour (random effect absorbs signal) could be a misuse. | Inspected: default joint estimation; σ²_study ≈ 270 vs σ²_ε ≈ 80; documented as expected behaviour under confounding of study and feedstock. | Documented (S2). |
| 4.4 | MODERATE | HistGradientBoosting difficulty model in E3b oversubscribed threads when run in parallel with other jobs. | `threadpool_limits(2)` | **Fixed** (affects runtime only). |
| 4.5 | MODERATE | The k-shot quantile uses calibration studies with n ≥ k + 1, a set that changes with k, whereas evaluation uses studies with n ≥ 11 for all k. | Acceptable (calibration uses all eligible information; evaluation uses a common set for comparability); state in Methods. | **Fixed** — documented here and in code docstring. |
| 4.6 | MINOR | Feature parsing of catalysts mis-classifies a few labels with Unicode subscripts (e.g. "Ca(OH)₂" → other). | Minor; affects < 0.2 % of runs. | Accepted, noted. |
| 4.7 | MINOR | `analyze.py` reported p = 0.0 as float underflow for some tests. | Displayed as "< 0.001". | ✓ |

Unit tests: `python -m pytest -q tests` → 14 passed.
