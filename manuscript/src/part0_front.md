---
title: "From literature to laboratory: an uncertainty-aware framework for transferring machine-learning models of hydrothermal biomass conversion and planning first experiments"
---

**Authors:** P N Bhargav Teja^a^, [Second author name]^b,\*^

^a^ [Affiliation of P N Bhargav Teja: department, institution, city, postal code, country]

^b^ [Affiliation of the second author: department, institution, city, postal code, country]

\* Corresponding author: [Second author name], [postal address]. E-mail address: [corresponding author e-mail]

# Highlights

- Literature-trained HTL/HTC models were tested as a new laboratory would use them
- Random data splits overstated accuracy about two-fold for unseen studies
- Study-calibrated 90% intervals covered {{cov_range_SC}}; row-calibrated {{cov_range_RC}}
- Three designed local runs cut the median yield error by {{gain3_min}}–{{gain3_max}} wt%
- For locked bio-oil studies, local runs alone beat literature-anchored models

# Abstract

Machine-learning models of hydrothermal liquefaction (HTL) and carbonization (HTC) are trained on literature data and validated by random splits, yet are meant to help laboratories whose studies they have never seen. This deployment problem was evaluated for bio-oil and solid yields using a curated database of 3,693 runs from 188 studies, 38 studies locked before modelling, an external hydrochar database and a protocol fixed in advance. Random splitting overstated accuracy about two-fold, and study-level offsets, which reported work-up descriptors did not explain, made up {{solid_share}}–{{biooil_share}} of out-of-study error variance. Conformal intervals calibrated across studies covered {{cov_range_SC}} of new-study runs (row-calibrated: {{cov_range_RC}}). In a retrospective simulated deployment, a laboratory measured up to five runs in a screening design. Combining three runs with the literature model (STRATA) lowered the median per-study error from {{dep_dev_biooil_design_0_A_rmse}} to {{dep_dev_biooil_design_3_B_rmse}} wt% (bio-oil) and from {{dep_dev_solid_design_0_A_rmse}} to {{dep_dev_solid_design_3_B_rmse}} wt% (solid) for unseen development studies, outperforming the local runs alone, and from {{dep_locked_solid_design_0_A_rmse}} to {{dep_locked_solid_design_3_B_rmse}} wt% for locked solid studies. For locked bio-oil studies, however, the local runs alone were more accurate, and an applicability-domain score did not anticipate this. With one to five local runs, 90% interval half-widths remained ±{{hw_solid_5}}–{{hw_biooil_1}} wt%, so these models support screening, not optimisation. The resulting STRATA-Lab workflow — study-calibrated intervals, a few designed local runs and an explicit comparison with local-only estimates — is proposed as minimum practice for transferring literature-trained bioresource models.

**Keywords:** hydrothermal liquefaction; hydrothermal carbonization; machine learning; conformal prediction; model transferability; experimental planning
