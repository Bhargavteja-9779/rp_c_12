---
title: "Supplementary Material — Machine-learning models of hydrothermal biomass conversion trained on literature data: transfer to unseen studies and study-calibrated prediction intervals"
---

# S1. Literature screening

PubMed was queried on 2026-11-10 for machine-learning studies of hydrothermal liquefaction or carbonization published 2015–2026 (query string in `supplementary/literature/pubmed_corpus.py`). Titles and abstracts of the {{lit_n_primary}} primary studies were screened with pre-defined regular expressions for the validation design, uncertainty quantification and physical constraints. Only {{lit_n_grouped}} abstracts mentioned grouped, study-level or external validation and {{lit_n_uq}} mentioned any form of uncertainty quantification. Abstract-level screening under-counts practices that appear only in the full text; the counts are therefore lower bounds.

{{TABLE:tableS1_literature}}

# S2. Pre-registered protocol and deviations

The analysis protocol (`code/config/PROTOCOL.md`) was committed to version control before any model was fitted, together with the locked list of 38 test studies. Deviations, each logged with date and reason: (i) the tabular foundation model could not be run because its weights require a personal licence acceptance; (ii) clarification that every learner was tuned separately for each feature set; (iii) the ridge-penalty grid of the meta-regression was widened after its selected value hit the registered upper bound, and three univariate study-level tests were added as secondary analyses; (iv) an exploratory, post-hoc locally adaptive variant of the study-calibrated intervals (SC-N, Section S4) was added after pipeline verification showed that constant-width study-calibrated intervals are wide. GPBoost was run as registered; its study random intercept absorbed most of the variance because feedstock descriptors are nearly constant within a study, so its out-of-study predictions reverted towards a nearly flat fixed-effect function.

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

# S6. Reproducibility

`python run_all.py --mode full` regenerates every result file, table and figure; `python manuscript/src/build_manuscript.py` regenerates this document and the manuscript from those files. Environment details (library versions, CPU) are written to `results/experiment_logs/environment.json` at run time.
