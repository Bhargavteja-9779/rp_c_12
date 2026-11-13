---
title: "Supplementary Material — Machine-learning models of hydrothermal biomass conversion trained on literature data: transfer to unseen studies and study-calibrated prediction intervals"
---

# S1. Literature screening

PubMed was queried on 2026-11-10 for machine-learning studies of hydrothermal liquefaction or carbonization published 2015–2026 (query string in `supplementary/literature/pubmed_corpus.py`). Titles and abstracts of the {{lit_n_primary}} primary studies were screened with pre-defined regular expressions for the validation design, uncertainty quantification and physical constraints. Only {{lit_n_grouped}} abstracts mentioned grouped, study-level or external validation and {{lit_n_uq}} mentioned any form of uncertainty quantification. Abstract-level screening under-counts practices that appear only in the full text; the counts are therefore lower bounds.

{{TABLE:tableS1_literature}}

# S2. Pre-registered protocol and deviations

The analysis protocol (`code/config/PROTOCOL.md`) was committed to version control before any model was fitted, together with the locked list of 38 test studies. Deviations, each logged with date and reason: (i) the tabular foundation model could not be run because its weights require a personal licence acceptance; (ii) clarification that every learner was tuned separately for each feature set; (iii) the ridge-penalty grid of the meta-regression was widened after its selected value hit the registered upper bound, and three univariate study-level tests were added as secondary analyses; (iv) protocol addenda A (within-study trends), A2 (product-quality targets) and C (locked confirmation), each registered before its analysis, and the exploratory addendum B registered after seeing the development results of A; (v) post-hoc review analyses E9 (base learners), E10 (cross-study duplicate audit) and E11 (overhead), and a post-hoc sensitivity analysis of the locked test excluding the single study with the largest squared-error share; (vi) an exploratory, post-hoc locally adaptive variant of the study-calibrated intervals (SC-N, Section S4) was added after pipeline verification showed that constant-width study-calibrated intervals are wide. GPBoost was run as registered; its study random intercept absorbed most of the variance because feedstock descriptors are nearly constant within a study, so its out-of-study predictions reverted towards a nearly flat fixed-effect function.

# S3. Additional benchmark and sensitivity results

{{TABLE:tableS2_benchmark_baseP}}

{{TABLE:tableS_paired_learner_tests}}

{{TABLE:tableS_coverage_all_alpha}}

{{TABLE:tableS3_sensitivity_alpha_folds}}

{{TABLE:tableS4_sensitivity_tau2}}

{{TABLE:tableS5_sensitivity_tuning}}

# S4. Exploratory: locally adaptive study-calibrated intervals (post hoc)

Motivation: constant-width study-calibrated intervals are wide. Hypothesis: out-of-study errors are heteroscedastic, so dividing conformity scores by a learned difficulty $\hat\sigma(\mathbf{x})$ narrows intervals for easy regimes without losing study-level coverage. A shallow gradient-boosting model of $\log(|r| + 0.5)$ was cross-fitted by study on the out-of-study residuals of the training studies; scores $|r|/\hat\sigma$ were calibrated with the same study-weighted quantile, and intervals were $f(\mathbf{x}) \pm \hat q\,\hat\sigma(\mathbf{x})$. {{adaptive_sentence}}

{{TABLE:tableS7_adaptive}}

# S5. Error analysis by subgroup

{{TABLE:tableS6_error_analysis}}

# S6. STRATA with different base learners (E9)

{{TABLE:tableS10_base_learners}}

# S7. Trend, ranking and anchoring analyses (Addenda A, A2, B, C)

Protocol addenda were committed to version control before the corresponding analyses were run (git history of `code/config/PROTOCOL.md`). Addendum B (contrast types, rules of thumb) was registered after the development results of Addendum A had been seen and is exploratory; its ranking result was tested once on the locked studies under Addendum C and was not confirmed. Full per-study results: `results/e12_*`, `results/e14*`; tests: `results/statistics_v2.json`.

{{TABLE:table_v2_empirical_trends}}

{{TABLE:table_v2_levels_vs_contrasts}}

{{TABLE:table_v2_ranking}}

{{TABLE:table_v2_trends_by_process}}

{{TABLE:table_v2_study_weighted_contrasts}}

{{TABLE:table_v2_timeline}}

# S8. Additional figures and cost

{{FIG:fig07_robustness|Robustness of the STRATA base learner (base + P features). Top: RMSE (mean ± SD over outer folds) with Gaussian noise added to continuous test features or with fewer training studies. Bottom: study-weighted coverage of RC and SC 90% intervals.}}

{{FIG:fig08_efficiency|Accuracy for unseen studies versus single-thread fit time on the development set (bio-oil, base features).}}

{{FIG:fig09_error_by_solvent|Mean out-of-study residual by extraction solvent named in the source study (groups with ≥ 3 studies; base features, seed-averaged outer-fold predictions).}}

{{FIG:fig10_parity|Observed versus predicted yields for the STRATA base learner under random-row CV and study-grouped CV (seed 11).}}

{{TABLE:table8_efficiency}}

# S9. Reproducibility

`python run_all.py --mode full` regenerates every result file, table and figure; `python manuscript/src/build_manuscript.py` regenerates this document and the manuscript from those files. Environment details (library versions, CPU) are written to `results/experiment_logs/environment.json` at run time.
