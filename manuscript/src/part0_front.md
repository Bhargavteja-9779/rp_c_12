---
title: "Machine-learning models of hydrothermal biomass conversion trained on literature data: transfer to unseen studies and study-calibrated prediction intervals"
---

**Authors:** [Author 1]^a,\*^, [Author 2]^b^, [Author 3]^a^

^a^ [Affiliation 1, full postal address, country]
^b^ [Affiliation 2, full postal address, country]

\* Corresponding author. E-mail address: [corresponding author e-mail]

# Highlights

- Random splits overstate HTL/HTC yield-model accuracy on new studies ~two-fold
- Study-level offsets make up half to two-thirds of the error on unseen studies
- Recorded work-up and yield-basis descriptors did not explain the study offsets
- Row-calibrated conformal intervals under-cover runs from new studies
- Study-level calibration and k-shot shrinkage restore near-nominal coverage

# Abstract

Machine-learning models of hydrothermal liquefaction (HTL) and carbonization (HTC) are trained on runs compiled from published studies but are usually validated by splitting runs at random. Using a curated database of 3,693 runs from 188 studies, with 38 studies locked away before modelling, this work quantified how such models transfer to unseen studies. Across 12 learners, the RMSE of the best bio-oil yield models rose from {{biooil_best_random_rmse}} wt% under random splitting to {{biooil_best_grouped_rmse}} wt% for unseen studies (R² {{biooil_best_random_r2}} → {{biooil_best_grouped_r2}}); solid yields behaved similarly ({{solid_best_random_rmse}} → {{solid_best_grouped_rmse}} wt%). Between-study offsets accounted for {{biooil_share}} (95% CI {{biooil_share_lo}}–{{biooil_share_hi}}) of the out-of-study error variance for bio-oil and {{solid_share}} for solids. Descriptors of product work-up and yield basis did not reduce this error. Conformal intervals calibrated on randomly held-out runs covered {{biooil_cov_RC}} (bio-oil) and {{solid_cov_RC}} (solids) of runs from unseen studies instead of 0.90; calibrating at the study level restored coverage to {{biooil_cov_SC}} and {{solid_cov_SC}}, at the cost of {{biooil_width_SC}}- and {{solid_width_SC}}-wt%-wide intervals. With three runs from the new study, an empirical-Bayes offset reduced the median per-study RMSE for bio-oil from {{biooil_k0_none_rmse}} to {{biooil_k3_eb_rmse}} wt% while keeping coverage at {{biooil_k3_eb_cov}}. {{abstract_locked_sentence}} Literature-trained surrogates should therefore be validated by study, reported with study-calibrated intervals and anchored with a few local runs before use in new settings.

**Keywords:** hydrothermal liquefaction; hydrothermal carbonization; machine learning; conformal prediction; data leakage; transferability
