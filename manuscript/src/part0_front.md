---
title: "What can machine-learning models trained on published hydrothermal-conversion data tell a new laboratory? A pre-registered audit with locked test studies"
---

**Authors:** [Author 1]^a,\*^, [Author 2]^b^, [Author 3]^a^

^a^ [Affiliation 1, full postal address, country]
^b^ [Affiliation 2, full postal address, country]

\* Corresponding author. E-mail address: [corresponding author e-mail]

# Highlights

- Pre-registered audit of literature-trained HTL/HTC models; 38 studies held out
- Yields of unseen studies were barely predictable; random splits hid this
- Laboratories agree on the direction of temperature effects, not on yield levels
- Trend-, ranking- and metadata-based shortcuts failed on held-out studies
- Study-calibrated intervals and a few local runs gave honest predictions

# Abstract

Machine-learning surrogates of hydrothermal liquefaction (HTL) and carbonization (HTC) are trained on runs compiled from the literature and usually validated by random splits. This work audited what such models can deliver for a laboratory whose study they have not seen, using a curated database of 3,693 runs from 188 studies, a pre-registered protocol and 38 studies locked away before modelling. Across 12 learners, the best bio-oil-yield RMSE rose from {{biooil_best_random_rmse}} wt% under random splitting to {{biooil_best_grouped_rmse}} wt% for unseen studies (R² {{biooil_best_random_r2}} → {{biooil_best_grouped_r2}}), and on locked studies no learner predicted bio-oil yields substantially better than the training mean. Study-level offsets made up {{solid_share}}–{{biooil_share}} of out-of-study error variance and were not explained by recorded work-up or yield-basis descriptors. Model-free within-study comparisons showed that laboratories agree on the direction of the temperature response below 300 °C (bio-oil {{biooil_slope_250_300}} wt% per 10 °C at 250–300 °C, same sign in {{biooil_sign_250_300}}% of studies), yet models predicted within-study changes no better than absolute yields, and an exploratory advantage in choosing the best planned run {{c1_sentence}} on locked studies. What held was honest uncertainty and local anchoring: conformal intervals calibrated across studies covered {{cov_range_SC}} of new-study runs (row-calibrated: {{cov_range_RC}}), and three measured runs lowered the median per-study bio-oil error from {{biooil_k0_none_rmse}} to {{biooil_k3_eb_rmse}} wt%. Literature-trained hydrothermal models should be validated by study, reported with study-calibrated intervals and anchored with local runs.

**Keywords:** hydrothermal liquefaction; hydrothermal carbonization; machine learning; conformal prediction; pre-registration; transferability
