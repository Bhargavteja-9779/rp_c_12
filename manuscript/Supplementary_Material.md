---
title: "Supplementary Material — From literature to laboratory: an uncertainty-aware framework for transferring machine-learning models of hydrothermal biomass conversion and planning first experiments"
---


# S1. Literature search

A reproducible multi-database search was run on 2026-11-18 with a script that stores the raw records, the search strings and the run date. PubMed was queried with a Boolean title/abstract query, Crossref with 16 bibliographic queries (four machine-learning terms × four hydrothermal terms, 200 journal-article records each) and OpenAlex with a title-and-abstract search; OpenAlex refused anonymous requests on the run date (HTTP 429) and contributed no records. Records were de-duplicated by DOI, else by normalised title. Eligibility was applied by rule to titles and abstracts, so that the selection is reproducible: E1, the record contains a machine-learning and a hydrothermal-conversion term; E2, primary research (not a review, editorial, erratum or retraction); E3, a product yield or property is predicted; E4, published from 2015 to the year after the run date (journal issue years can run one year ahead of online publication). Records without an abstract were screened on the title. Search strings and record flow are given in Table S1. Abstract-level extraction under-counts practices that appear only in the full text; the counts of validation and uncertainty practices are therefore lower bounds. Table S2 lists the earlier PubMed-only corpus from which the median reported R² quoted in the Introduction was extracted.


**Table S1.** Reproducible multi-database literature search: search strings, dates, eligibility criteria (E1–E4, applied by rule to titles and abstracts) and record flow.

| Step | Value |
|---|---|
| Run date | 2026-11-18 |
| PubMed query (title/abstract, publication date 2015-01-01 to run date) | ("machine learning"[tiab] OR "deep learning"[tiab] OR "neural network"[tiab] OR "random forest"[tiab] OR "gradient boosting"[tiab] OR xgboost[tiab] OR "support vector"[tiab]) AND ("hydrothermal liquefaction"[tiab] OR "hydrothermal carbonization"[tiab] OR "hydrothermal carbonisation"[tiab] OR hydrochar[tiab] OR biocrude[tiab] OR "bio-crude"[tiab]) |
| OpenAlex query (title_and_abstract.search) | ("machine learning" OR "deep learning" OR "neural network" OR "random forest" OR "gradient boosting" OR xgboost OR "support vector") AND ("hydrothermal liquefaction" OR "hydrothermal carbonization" OR "hydrothermal carbonisation" OR hydrochar OR biocrude OR "bio-crude") — not retrievable on the run date (anonymous API requests refused, HTTP 429); 0 records |
| Crossref queries (query.bibliographic, journal articles, 200 records each) | machine learning hydrothermal liquefaction; machine learning hydrothermal carbonization; machine learning hydrochar; machine learning biocrude; neural network hydrothermal liquefaction; neural network hydrothermal carbonization; neural network hydrochar; neural network biocrude; random forest hydrothermal liquefaction; random forest hydrothermal carbonization; random forest hydrochar; random forest biocrude; gradient boosting hydrothermal liquefaction; gradient boosting hydrothermal carbonization; gradient boosting hydrochar; gradient boosting biocrude |
| Records identified | PubMed 53; OpenAlex 0; Crossref 3200 (total 3253) |
| After de-duplication (DOI, else normalised title) | 1388 |
| Excluded: no machine-learning or no hydrothermal term in title/abstract (E1) | 1265 |
| Excluded: review or non-primary (E2) | 11 |
| Excluded: no predicted yield or property (E3) | 19 |
| Excluded: outside 2015 to run year + 1 (E4) | 0 |
| Included primary studies | 93 (51 with an abstract; 18 in Bioresource Technology) |
| Included abstracts mentioning grouped / external validation | 2 |
| Included abstracts mentioning uncertainty quantification | 4 |




**Table S2.** PubMed-indexed ML studies of hydrothermal conversion (abstract-level screening; n.s. = not stated in abstract).

| Year | Journal | First author | DOI | Target(s) | Methods | Validation (abstract) | R² in abstract | UQ | Physics |
|---|---|---|---|---|---|---|---|---|---|
| 2018 | Bioresour Technol | Li | 10.1016/j.biortech.2018.04.066 | hydrochar yield/properties | RF | n.s. | n.s. | n.s. | n.s. |
| 2019 | Waste Manag | Ismail | 10.1016/j.wasman.2018.12.044 | carbon recovery | ANN/MLP | n.s. | n.s. | n.s. | n.s. |
| 2021 | Bioresour Technol | Zhang | 10.1016/j.biortech.2021.126011 | bio-oil/biocrude yield; N content/heterocycles | RF; GBR/GBM | n.s. | n.s. | n.s. | n.s. |
| 2022 | Bioresour Technol | Katongtung | 10.1016/j.biortech.2021.126278 | bio-oil/biocrude yield; HHV/energy | XGB; GBR/GBM | random/k-fold | n.s. | n.s. | n.s. |
| 2022 | Bioresour Technol | Zhou | 10.1016/j.biortech.2021.126354 | n.s. | RF | n.s. | n.s. | n.s. | n.s. |
| 2022 | Bioresour Technol | Zhou | 10.1016/j.biortech.2022.126923 | n.s. | SVR | n.s. | n.s. | n.s. | n.s. |
| 2022 | Bioresour Technol | Leng | 10.1016/j.biortech.2022.127791 | bio-oil/biocrude yield; N content/heterocycles | RF | n.s. | 0.92;0.82 | n.s. | n.s. |
| 2022 | Bioresour Technol | Gruber | 10.1016/j.biortech.2022.128071 | hydrochar yield/properties | ANN/MLP | n.s. | 0.997;0.978 | n.s. | n.s. |
| 2022 | Water Sci Technol | Divband Hafshejani | 10.2166/wst.2022.264 | hydrochar yield/properties; adsorption | ANN/MLP; SVR | n.s. | n.s. | n.s. | n.s. |
| 2022 | Open Res Eur | Haarlemmer | 10.12688/openreseurope.14915.2 | bio-oil/biocrude yield | n.s. | n.s. | n.s. | n.s. | n.s. |
| 2023 | Chemosphere | Yoo | 10.1016/j.chemosphere.2022.137074 | hydrochar yield/properties; adsorption | ANN/MLP | n.s. | n.s. | n.s. | n.s. |
| 2023 | Bioresour Technol | Zhu | 10.1016/j.biortech.2022.128454 | hydrochar yield/properties; HHV/energy; carbon recovery | n.s. | n.s. | 0.983 | n.s. | n.s. |
| 2023 | Bioresour Technol | Chen | 10.1016/j.biortech.2023.128893 | n.s. | RF; ANN/MLP; SVR | n.s. | n.s. | n.s. | n.s. |
| 2023 | Bioresour Technol | Zhao | 10.1016/j.biortech.2023.129223 | hydrochar yield/properties; adsorption | GBR/GBM; DT | n.s. | 0.93 | n.s. | n.s. |
| 2023 | Heliyon | Kohzadi | 10.1016/j.heliyon.2023.e21258 | hydrochar yield/properties; adsorption | ANN/MLP | n.s. | n.s. | n.s. | n.s. |
| 2023 | Commun Chem | Wang | 10.1038/s42004-023-01077-z | n.s. | n.s. | n.s. | n.s. | n.s. | n.s. |
| 2024 | Sci Total Environ | Ma | 10.1016/j.scitotenv.2023.168279 | n.s. | n.s. | n.s. | n.s. | n.s. | n.s. |
| 2024 | Bioresour Technol | Liu | 10.1016/j.biortech.2023.130073 | hydrochar yield/properties | RF; XGB; GBR/GBM; SVR | n.s. | n.s. | n.s. | n.s. |
| 2024 | Chemosphere | Vinayagam | 10.1016/j.chemosphere.2024.141130 | adsorption | ANN/MLP | n.s. | 0.99 | n.s. | n.s. |
| 2024 | Sci Total Environ | Liu | 10.1016/j.scitotenv.2024.170779 | HHV/energy; N content/heterocycles | RF; GBR/GBM | n.s. | n.s. | n.s. | n.s. |
| 2024 | Chemosphere | Mahmoud | 10.1016/j.chemosphere.2024.141746 | hydrochar yield/properties; adsorption | ANN/MLP | n.s. | 0.989 | n.s. | n.s. |
| 2024 | Sci Total Environ | Lahori | 10.1016/j.scitotenv.2024.172810 | hydrochar yield/properties | linear/ridge | n.s. | n.s. | n.s. | n.s. |
| 2024 | J Phys Chem A | Srinivasan | 10.1021/acs.jpca.4c01592 | n.s. | ANN/MLP | n.s. | n.s. | n.s. | n.s. |
| 2024 | Sci Total Environ | Zhang | 10.1016/j.scitotenv.2024.173939 | n.s. | GBR/GBM | n.s. | 0.99;0.80;0.89 | n.s. | n.s. |
| 2024 | J Hazard Mater | Liu | 10.1016/j.jhazmat.2024.135853 | hydrochar yield/properties; adsorption | GBR/GBM | n.s. | n.s. | n.s. | n.s. |
| 2024 | Sci Total Environ | Tong | 10.1016/j.scitotenv.2024.176780 | hydrochar yield/properties | RF; GBR/GBM | n.s. | 0.86 | n.s. | n.s. |
| 2024 | F1000Res | Katongtung | 10.12688/f1000research.156514.3 | n.s. | n.s. | n.s. | n.s. | n.s. | n.s. |
| 2025 | Environ Res | Xiong | 10.1016/j.envres.2025.122168 | hydrochar yield/properties | RF | n.s. | n.s. | n.s. | n.s. |
| 2025 | Waste Manag | Biswas | 10.1016/j.wasman.2025.115054 | hydrochar yield/properties | ANN/MLP | random/k-fold | n.s. | n.s. | n.s. |
| 2025 | Bioresour Bioprocess | Hou | 10.1186/s40643-025-00979-1 | hydrochar yield/properties; HHV/energy | XGB; GBR/GBM; ANN/MLP; DT; linear/ridge | n.s. | 0.98;0.94 | yes | n.s. |
| 2026 | Bioresour Technol | Igwegbe | 10.1016/j.biortech.2025.133282 | hydrochar yield/properties; HHV/energy; carbon recovery | XGB; SVR; linear/ridge | n.s. | 0.87;0.938;0.85 | n.s. | n.s. |
| 2026 | Bioresour Technol | Yan | 10.1016/j.biortech.2025.133451 | hydrochar yield/properties; carbon recovery | n.s. | n.s. | n.s. | n.s. | n.s. |
| 2026 | Bioresour Technol | Liu | 10.1016/j.biortech.2026.133921 | hydrochar yield/properties; N content/heterocycles | RF | grouped/external | 0.882;0.877;0.894 | n.s. | n.s. |
| 2026 | Bioresour Technol | Lu | 10.1016/j.biortech.2026.134279 | N content/heterocycles | GBR/GBM | n.s. | n.s. | n.s. | n.s. |
| 2026 | Bioresour Technol | Gao | 10.1016/j.biortech.2026.134360 | n.s. | RF; GBR/GBM | n.s. | 0.82;0.79;0.65 | n.s. | n.s. |
| 2026 | Environ Sci Technol | Guo | 10.1021/acs.est.6c01833 | hydrochar yield/properties; HHV/energy | n.s. | n.s. | n.s. | n.s. | n.s. |
| 2026 | RSC Adv | Do | 10.1039/d6ra01824f | adsorption | ANN/MLP | n.s. | n.s. | n.s. | n.s. |
| 2026 | Bioresour Technol | Khan | 10.1016/j.biortech.2026.134909 | hydrochar yield/properties | n.s. | random/k-fold | 0.85 | yes | n.s. |
| 2026 | Bioresour Technol | Li | 10.1016/j.biortech.2026.135052 | hydrochar yield/properties | linear/ridge | n.s. | n.s. | n.s. | n.s. |
| 2026 | RSC Adv | Asim | 10.1039/d6ra05073e | adsorption | n.s. | n.s. | n.s. | n.s. | n.s. |
| 2026 | J Environ Manage | Ma | 10.1016/j.jenvman.2026.130813 | hydrochar yield/properties; HHV/energy | GBR/GBM | n.s. | 0.890;0.831 | yes | n.s. |
| 2026 | Bioresour Technol | Huang | 10.1016/j.biortech.2026.136066 | hydrochar yield/properties; adsorption | n.s. | n.s. | n.s. | n.s. | yes |
| 2026 | Environ Sci Technol | Liu | 10.1021/acs.est.6c05758 | HHV/energy | n.s. | n.s. | n.s. | n.s. | n.s. |
| 2027 | Bioresour Technol | Elfetni | 10.1016/j.biortech.2026.135587 | HHV/energy | XGB | grouped/externalrandom/k-fold | 0.844 | yes | yes |



# S2. Protocol, addenda and deviations

The analysis protocol (research questions, metrics, statistical tests, seeds) and the locked list of 38 test studies were committed to a version-controlled repository hosted on GitHub before any model was fitted. The protocol was not deposited in a public registry; the order of registration and analysis is documented by the commit history (Table S3), and the repository is available from the corresponding author on request. Addenda: A (within-study trends) and A2 (product-quality targets), each registered before its analysis; B (contrast types and rules of thumb), registered after the development results of A had been seen and therefore exploratory; C (one-time locked confirmation of A and B); and D (sequential deployment E15, decision support E16 and laboratory case studies E17), registered after an external pre-submission review and before any of these analyses was run. Deviations, each logged with date and reason: (i) the tabular foundation model could not be run because its weights require a personal licence acceptance; (ii) every learner was tuned separately for each feature set; (iii) the ridge-penalty grid of the meta-regression was widened after its selected value hit the registered upper bound, and three univariate study-level tests were added as secondary analyses; (iv) post-hoc review analyses E9 (base learners), E10 (cross-study duplicate audit) and E11 (overhead), and a post-hoc sensitivity analysis of the locked test excluding the study with the largest squared-error share; (v) an exploratory locally adaptive interval variant (Section S4); (vi) the model-free trend analysis E13 was not registered and is descriptive; (vii) because the pre-registered applicability-domain threshold flagged no locked study, an exploratory rank correlation between the score and the error on locked studies was added after this result was known (main-text Table 7); (viii) the literature search was extended from PubMed to a multi-database search after the external review; when the screening was checked, two rules were corrected and re-applied to the stored records without new queries — the publication window was widened to the year after the run date because an included 2026 article carries a 2027 issue year, and 'publication-aware/-level' was added to the pattern for grouped validation. GPBoost was run as registered; its study random intercept absorbed most of the variance because feedstock descriptors are nearly constant within a study, so its out-of-study predictions reverted towards a nearly flat fixed-effect function.


**Table S3.** Audit trail: version-control commits establishing that the protocol, the locked study list and each addendum preceded the analyses they govern.

| Commit | Time (UTC) | Event |
|---|---|---|
| 04a5079 | 2026-11-10 21:44 | Initialize research repository: vendored CC-BY datasets, journal-screen scripts, locked study-level test split |
| d40eac3 | 2026-11-10 21:52 | Pre-register analysis protocol (before any model fitting); literature corpus and matrix |
| 69ccfd1 | 2026-11-11 03:36 | All development experiments complete (E1-E8, E3b); all modelling decisions frozen BEFORE the single locked-test evaluation |
| 639845a | 2026-11-11 03:37 | Locked test evaluated once (38 studies) |
| d24f01c | 2026-11-13 11:58 | Pre-register Addendum A (v2): trend-transfer / offset-invariant learning experiment E12, before running it |
| b54cfa1 | 2026-11-13 12:02 | E12 implementation: offset-invariant contrast models (A/W/PD), trend metrics, anchoring, contrast conformal; unit tests |
| 2f4af56 | 2026-11-13 12:05 | Addendum A2 (quality targets) registered; loader extended; E13 model-free within-study trend analysis |
| 71a1d8f | 2026-11-13 12:37 | E12 development results (T1-T3 not supported); register exploratory Addendum B (E14) before running |
| 9668526 | 2026-11-13 12:39 | Register Addendum C (confirmatory locked-study tests for ranking and E12) before any locked evaluation of E12/E14; E14 locked mode |
| 19982f0 | 2026-11-13 12:56 | v2 experiments complete: E12 dev/locked (yields 3 learners; HHV/C), E13, E14 dev + locked confirmation; v2 analysis and figure code |



# S3. Additional benchmark and sensitivity results


**Table S4.** Benchmark with base + protocol (P) features.

| Target | Learner | Random CV RMSE | Grouped CV RMSE | Grouped CV R² |
|---|---|---|---|---|
| Bio-oil | LightGBM | 7.53 | 16.01 | 0.209 |
| Bio-oil | Random forest | 8.33 | 16.23 | 0.188 |
| Bio-oil | XGBoost | 7.65 | 16.33 | 0.178 |
| Bio-oil | Extra trees | 8.33 | 16.35 | 0.176 |
| Bio-oil | SVR | 11.04 | 16.45 | 0.165 |
| Bio-oil | CatBoost | 7.66 | 16.62 | 0.148 |
| Bio-oil | HistGB | 7.81 | 16.9 | 0.119 |
| Bio-oil | k-NN | 10.01 | 17.15 | 0.093 |
| Bio-oil | GPBoost | 17.29 | 17.61 | 0.044 |
| Bio-oil | Ridge | 14.15 | 17.73 | 0.03 |
| Bio-oil | Mean | 18.02 | 18.12 | -0.013 |
| Bio-oil | MLP | 8.63 | 23.32 | -0.681 |
| Solid | LightGBM | 7.03 | 13.65 | 0.544 |
| Solid | XGBoost | 7.06 | 14.08 | 0.516 |
| Solid | HistGB | 7.07 | 14.17 | 0.51 |
| Solid | Random forest | 8.6 | 14.22 | 0.506 |
| Solid | CatBoost | 7.66 | 14.64 | 0.476 |
| Solid | Extra trees | 8.18 | 15.3 | 0.428 |
| Solid | SVR | 9.12 | 16.31 | 0.35 |
| Solid | Ridge | 13.44 | 16.63 | 0.324 |
| Solid | k-NN | 9.95 | 16.74 | 0.316 |
| Solid | GPBoost | 19.14 | 19.85 | 0.038 |
| Solid | MLP | 8.03 | 20.35 | -0.012 |
| Solid | Mean | 20.25 | 20.63 | -0.039 |




**Table S5.** Per-study RMSE of each learner vs the best learner under grouped CV (Wilcoxon, Holm).

| target | features | learner | reference | n | median_diff | ci_low | ci_high | rank_biserial | p | p_holm |
|---|---|---|---|---|---|---|---|---|---|---|
| biooil | base | cat | et | 122 | -0.2216 | -0.8093 | 0.7455 | 0.0585 | 0.5749 | 1.0 |
| biooil | base | gpboost | et | 122 | 0.9174 | 0.1383 | 2.3352 | 0.2656 | 0.0109 | 0.0973 |
| biooil | base | hgb | et | 122 | 0.3776 | -0.319 | 1.0831 | 0.098 | 0.3478 | 1.0 |
| biooil | base | knn | et | 122 | 0.188 | -0.3295 | 0.7372 | 0.0649 | 0.5338 | 1.0 |
| biooil | base | lgbm | et | 122 | -0.36 | -1.0746 | 0.441 | -0.0801 | 0.4426 | 1.0 |
| biooil | base | mean | et | 122 | 1.1666 | 0.324 | 2.7974 | 0.3197 | 0.0022 | 0.0218 |
| biooil | base | mlp | et | 122 | 1.4015 | 0.8269 | 2.3835 | 0.4064 | 0.0001 | 0.0011 |
| biooil | base | rf | et | 122 | -0.1996 | -0.9058 | 0.2122 | -0.0641 | 0.5389 | 1.0 |
| biooil | base | ridge | et | 122 | 0.7065 | -0.0266 | 1.4461 | 0.2659 | 0.0108 | 0.0973 |
| biooil | base | svr | et | 122 | 0.2585 | -0.1276 | 1.0054 | 0.0964 | 0.3557 | 1.0 |
| biooil | base | xgb | et | 122 | -0.6037 | -1.2874 | 0.4911 | -0.135 | 0.1956 | 1.0 |
| biooil | base+P | cat | lgbm | 122 | 0.4598 | -0.0338 | 1.0689 | 0.2486 | 0.0172 | 0.1204 |
| biooil | base+P | et | lgbm | 122 | 0.6415 | -0.0084 | 1.3662 | 0.1651 | 0.1135 | 0.3404 |
| biooil | base+P | gpboost | lgbm | 122 | 1.5691 | 0.4798 | 2.3756 | 0.3024 | 0.0037 | 0.03 |
| biooil | base+P | hgb | lgbm | 122 | 0.3768 | -0.0465 | 0.8419 | 0.2104 | 0.0437 | 0.2184 |
| biooil | base+P | knn | lgbm | 122 | 1.0143 | -0.0005 | 2.0762 | 0.2219 | 0.0334 | 0.2005 |
| biooil | base+P | mean | lgbm | 122 | 1.8974 | 0.2815 | 2.9184 | 0.3261 | 0.0018 | 0.0159 |
| biooil | base+P | mlp | lgbm | 122 | 3.008 | 2.1817 | 4.5248 | 0.5223 | 0.0 | 0.0 |
| biooil | base+P | rf | lgbm | 122 | -0.1483 | -0.4438 | 0.6064 | 0.0566 | 0.5872 | 0.6294 |
| biooil | base+P | ridge | lgbm | 122 | 1.9552 | 0.7435 | 2.5843 | 0.3347 | 0.0013 | 0.0134 |
| biooil | base+P | svr | lgbm | 122 | 1.0249 | -0.2102 | 1.5866 | 0.1889 | 0.0703 | 0.2811 |
| biooil | base+P | xgb | lgbm | 122 | 0.1263 | -0.1065 | 0.5132 | 0.1049 | 0.3147 | 0.6294 |
| solid | base | cat | lgbm | 120 | 0.2643 | -0.0284 | 0.5413 | 0.1388 | 0.1869 | 0.3737 |
| solid | base | et | lgbm | 120 | 0.5281 | 0.1758 | 1.169 | 0.2642 | 0.012 | 0.0601 |
| solid | base | gpboost | lgbm | 120 | 4.5226 | 3.3612 | 6.0919 | 0.7085 | 0.0 | 0.0 |
| solid | base | hgb | lgbm | 120 | 0.5105 | -0.0365 | 0.7768 | 0.1994 | 0.058 | 0.2318 |
| solid | base | knn | lgbm | 120 | 1.3354 | 0.2329 | 2.1963 | 0.3204 | 0.0023 | 0.0139 |
| solid | base | mean | lgbm | 120 | 5.4683 | 4.3418 | 6.7941 | 0.7358 | 0.0 | 0.0 |
| solid | base | mlp | lgbm | 120 | 2.007 | 1.2778 | 3.6872 | 0.614 | 0.0 | 0.0 |
| solid | base | rf | lgbm | 120 | 0.234 | -0.1967 | 0.5777 | 0.0829 | 0.4305 | 0.4305 |
| solid | base | ridge | lgbm | 120 | 1.6468 | 0.8181 | 2.6226 | 0.4556 | 0.0 | 0.0001 |
| solid | base | svr | lgbm | 120 | 0.9475 | 0.1213 | 1.7558 | 0.3295 | 0.0017 | 0.0121 |
| solid | base | xgb | lgbm | 120 | 0.3587 | 0.0882 | 0.5465 | 0.1964 | 0.0619 | 0.2318 |
| solid | base+P | cat | lgbm | 120 | 0.3388 | -0.0327 | 0.9523 | 0.2011 | 0.0559 | 0.1677 |
| solid | base+P | et | lgbm | 120 | 0.9511 | 0.0248 | 1.5519 | 0.3215 | 0.0022 | 0.009 |
| solid | base+P | gpboost | lgbm | 120 | 4.9142 | 3.3016 | 6.3658 | 0.6986 | 0.0 | 0.0 |
| solid | base+P | hgb | lgbm | 120 | 0.2709 | 0.0949 | 0.5406 | 0.3397 | 0.0012 | 0.0062 |
| solid | base+P | knn | lgbm | 120 | 1.8679 | 1.0058 | 3.4828 | 0.4909 | 0.0 | 0.0 |
| solid | base+P | mean | lgbm | 120 | 5.5907 | 4.1452 | 6.9488 | 0.7331 | 0.0 | 0.0 |
| solid | base+P | mlp | lgbm | 120 | 3.5439 | 2.9145 | 4.2279 | 0.7449 | 0.0 | 0.0 |
| solid | base+P | rf | lgbm | 120 | 0.3941 | -0.2203 | 0.8728 | 0.1598 | 0.1288 | 0.2576 |
| solid | base+P | ridge | lgbm | 120 | 1.7981 | 0.9084 | 2.6774 | 0.5245 | 0.0 | 0.0 |
| solid | base+P | svr | lgbm | 120 | 1.7353 | 0.6701 | 2.2464 | 0.4623 | 0.0 | 0.0001 |
| solid | base+P | xgb | lgbm | 120 | 0.0466 | -0.2548 | 0.2825 | 0.0843 | 0.4229 | 0.4229 |




**Table S6.** Coverage for all α levels and settings.

| Target | Setting | α | Calibration | Coverage (rows) | Coverage (studies) | Width (wt%) | Studies <0.8 coverage |
|---|---|---|---|---|---|---|---|
| Bio-oil | Development CV (unseen studies) | 0.05 | RC | 0.758 | 0.73 | 33.1 | 0.42 |
| Bio-oil | Development CV (unseen studies) | 0.1 | RC | 0.612 | 0.57 | 22.8 | 0.66 |
| Bio-oil | Development CV (unseen studies) | 0.2 | RC | 0.442 | 0.398 | 14.5 | 0.85 |
| Bio-oil | Development CV (unseen studies) | 0.05 | SC | 0.965 | 0.953 | 76.4 | 0.08 |
| Bio-oil | Development CV (unseen studies) | 0.1 | SC | 0.93 | 0.909 | 59.1 | 0.16 |
| Bio-oil | Development CV (unseen studies) | 0.2 | SC | 0.852 | 0.822 | 42.9 | 0.26 |
| Solid | Development CV (unseen studies) | 0.05 | RC | 0.748 | 0.752 | 29.0 | 0.48 |
| Solid | Development CV (unseen studies) | 0.1 | RC | 0.615 | 0.614 | 20.6 | 0.66 |
| Solid | Development CV (unseen studies) | 0.2 | RC | 0.461 | 0.454 | 13.4 | 0.82 |
| Solid | Development CV (unseen studies) | 0.05 | SC | 0.95 | 0.955 | 60.1 | 0.08 |
| Solid | Development CV (unseen studies) | 0.1 | SC | 0.901 | 0.908 | 46.7 | 0.16 |
| Solid | Development CV (unseen studies) | 0.2 | SC | 0.807 | 0.815 | 33.4 | 0.35 |
| Bio-oil | Locked test | 0.05 | RC | 0.678 | 0.726 | 33.5 | 0.43 |
| Bio-oil | Locked test | 0.05 | SC | 0.874 | 0.95 | 68.8 | 0.11 |
| Bio-oil | Locked test | 0.1 | RC | 0.565 | 0.603 | 22.7 | 0.61 |
| Bio-oil | Locked test | 0.1 | SC | 0.82 | 0.895 | 54.8 | 0.21 |
| Bio-oil | Locked test | 0.2 | RC | 0.426 | 0.428 | 14.8 | 0.93 |
| Bio-oil | Locked test | 0.2 | SC | 0.748 | 0.801 | 39.7 | 0.32 |
| Solid | Locked test | 0.05 | RC | 0.591 | 0.582 | 28.5 | 0.63 |
| Solid | Locked test | 0.05 | SC | 0.908 | 0.882 | 59.0 | 0.17 |
| Solid | Locked test | 0.1 | RC | 0.44 | 0.457 | 21.0 | 0.77 |
| Solid | Locked test | 0.1 | SC | 0.864 | 0.821 | 46.7 | 0.23 |
| Solid | Locked test | 0.2 | RC | 0.289 | 0.292 | 13.3 | 0.93 |
| Solid | Locked test | 0.2 | SC | 0.707 | 0.677 | 35.4 | 0.57 |
| Bio-oil | Leave-family-out (mean) | 0.05 | RC | 0.738 | 0.722 | 32.4 | 0.44 |
| Bio-oil | Leave-family-out (mean) | 0.05 | SC | 0.93 | 0.942 | 74.1 | 0.09 |
| Bio-oil | Leave-family-out (mean) | 0.1 | RC | 0.569 | 0.554 | 22.5 | 0.62 |
| Bio-oil | Leave-family-out (mean) | 0.1 | SC | 0.888 | 0.894 | 57.6 | 0.16 |
| Bio-oil | Leave-family-out (mean) | 0.2 | RC | 0.335 | 0.329 | 14.5 | 0.83 |
| Bio-oil | Leave-family-out (mean) | 0.2 | SC | 0.815 | 0.804 | 41.8 | 0.29 |
| Bio-oil | Temporal (≤2018 → >2018) | 0.05 | RC | 0.574 | 0.55 | 29.6 | 0.69 |
| Bio-oil | Temporal (≤2018 → >2018) | 0.05 | SC | 0.885 | 0.906 | 75.9 | 0.17 |
| Bio-oil | Temporal (≤2018 → >2018) | 0.1 | RC | 0.456 | 0.422 | 21.9 | 0.84 |
| Bio-oil | Temporal (≤2018 → >2018) | 0.1 | SC | 0.846 | 0.853 | 64.1 | 0.28 |
| Bio-oil | Temporal (≤2018 → >2018) | 0.2 | RC | 0.306 | 0.286 | 13.5 | 0.97 |
| Bio-oil | Temporal (≤2018 → >2018) | 0.2 | SC | 0.748 | 0.743 | 46.1 | 0.41 |
| Solid | Leave-family-out (mean) | 0.05 | RC | 0.683 | 0.744 | 28.7 | 0.37 |
| Solid | Leave-family-out (mean) | 0.05 | SC | 0.89 | 0.926 | 58.9 | 0.12 |
| Solid | Leave-family-out (mean) | 0.1 | RC | 0.548 | 0.596 | 20.5 | 0.57 |
| Solid | Leave-family-out (mean) | 0.1 | SC | 0.858 | 0.896 | 46.5 | 0.16 |
| Solid | Leave-family-out (mean) | 0.2 | RC | 0.35 | 0.369 | 13.3 | 0.87 |
| Solid | Leave-family-out (mean) | 0.2 | SC | 0.748 | 0.795 | 34.2 | 0.33 |
| Solid | Temporal (≤2018 → >2018) | 0.05 | RC | 0.648 | 0.692 | 25.7 | 0.53 |
| Solid | Temporal (≤2018 → >2018) | 0.05 | SC | 0.909 | 0.925 | 58.6 | 0.14 |
| Solid | Temporal (≤2018 → >2018) | 0.1 | RC | 0.521 | 0.559 | 18.7 | 0.72 |
| Solid | Temporal (≤2018 → >2018) | 0.1 | SC | 0.877 | 0.897 | 49.0 | 0.14 |
| Solid | Temporal (≤2018 → >2018) | 0.2 | RC | 0.384 | 0.418 | 12.7 | 0.88 |
| Solid | Temporal (≤2018 → >2018) | 0.2 | SC | 0.809 | 0.832 | 39.4 | 0.27 |
| Solid | External 4TU | 0.05 | RC | 0.681 | 0.724 | 28.7 | 0.49 |
| Solid | External 4TU | 0.05 | SC | 0.964 | 0.948 | 55.4 | 0.12 |
| Solid | External 4TU | 0.1 | RC | 0.534 | 0.549 | 20.7 | 0.7 |
| Solid | External 4TU | 0.1 | SC | 0.934 | 0.918 | 47.3 | 0.16 |
| Solid | External 4TU | 0.2 | RC | 0.404 | 0.416 | 13.2 | 0.83 |
| Solid | External 4TU | 0.2 | SC | 0.783 | 0.809 | 34.2 | 0.32 |




**Table S7.** Sensitivity of coverage and accuracy to α and to the number of outer folds (seed 11).

| target | features | outer_folds | alpha | calibration | Coverage (studies) | Width (wt%) | RMSE |
|---|---|---|---|---|---|---|---|
| Bio-oil | base | 5.0 | 0.05 | RC | 0.704 | 32.054 | 15.609 |
| Bio-oil | base | 5.0 | 0.05 | SC | 0.962 | 77.906 | 15.609 |
| Bio-oil | base | 5.0 | 0.1 | RC | 0.556 | 22.655 | 15.609 |
| Bio-oil | base | 5.0 | 0.1 | SC | 0.921 | 58.656 | 15.609 |
| Bio-oil | base | 5.0 | 0.2 | RC | 0.396 | 14.545 | 15.609 |
| Bio-oil | base | 5.0 | 0.2 | SC | 0.837 | 43.221 | 15.609 |
| Bio-oil | base | 10.0 | 0.05 | RC | 0.702 | 31.687 | 15.588 |
| Bio-oil | base | 10.0 | 0.05 | SC | 0.948 | 69.763 | 15.588 |
| Bio-oil | base | 10.0 | 0.1 | RC | 0.547 | 22.587 | 15.588 |
| Bio-oil | base | 10.0 | 0.1 | SC | 0.902 | 54.794 | 15.588 |
| Bio-oil | base | 10.0 | 0.2 | RC | 0.406 | 14.899 | 15.588 |
| Bio-oil | base | 10.0 | 0.2 | SC | 0.813 | 40.993 | 15.588 |
| Bio-oil | base+P | 5.0 | 0.05 | RC | 0.689 | 32.286 | 16.422 |
| Bio-oil | base+P | 5.0 | 0.05 | SC | 0.954 | 79.124 | 16.422 |
| Bio-oil | base+P | 5.0 | 0.1 | RC | 0.545 | 22.851 | 16.422 |
| Bio-oil | base+P | 5.0 | 0.1 | SC | 0.909 | 60.165 | 16.422 |
| Bio-oil | base+P | 5.0 | 0.2 | RC | 0.369 | 14.546 | 16.422 |
| Bio-oil | base+P | 5.0 | 0.2 | SC | 0.826 | 44.653 | 16.422 |
| Bio-oil | base+P | 10.0 | 0.05 | RC | 0.714 | 32.104 | 15.654 |
| Bio-oil | base+P | 10.0 | 0.05 | SC | 0.951 | 74.833 | 15.654 |
| Bio-oil | base+P | 10.0 | 0.1 | RC | 0.556 | 22.555 | 15.654 |
| Bio-oil | base+P | 10.0 | 0.1 | SC | 0.904 | 58.574 | 15.654 |
| Bio-oil | base+P | 10.0 | 0.2 | RC | 0.394 | 14.439 | 15.654 |
| Bio-oil | base+P | 10.0 | 0.2 | SC | 0.808 | 42.157 | 15.654 |
| Solid | base | 5.0 | 0.05 | RC | 0.722 | 28.444 | 14.043 |
| Solid | base | 5.0 | 0.05 | SC | 0.962 | 62.917 | 14.043 |
| Solid | base | 5.0 | 0.1 | RC | 0.588 | 20.277 | 14.043 |
| Solid | base | 5.0 | 0.1 | SC | 0.914 | 48.778 | 14.043 |
| Solid | base | 5.0 | 0.2 | RC | 0.433 | 13.061 | 14.043 |
| Solid | base | 5.0 | 0.2 | SC | 0.813 | 35.711 | 14.043 |
| Solid | base | 10.0 | 0.05 | RC | 0.747 | 28.414 | 14.165 |
| Solid | base | 10.0 | 0.05 | SC | 0.961 | 61.863 | 14.165 |
| Solid | base | 10.0 | 0.1 | RC | 0.6 | 20.358 | 14.165 |
| Solid | base | 10.0 | 0.1 | SC | 0.902 | 47.455 | 14.165 |
| Solid | base | 10.0 | 0.2 | RC | 0.438 | 13.135 | 14.165 |
| Solid | base | 10.0 | 0.2 | SC | 0.817 | 34.51 | 14.165 |
| Solid | base+P | 5.0 | 0.05 | RC | 0.729 | 28.583 | 14.107 |
| Solid | base+P | 5.0 | 0.05 | SC | 0.961 | 63.523 | 14.107 |
| Solid | base+P | 5.0 | 0.1 | RC | 0.589 | 20.371 | 14.107 |
| Solid | base+P | 5.0 | 0.1 | SC | 0.915 | 49.307 | 14.107 |
| Solid | base+P | 5.0 | 0.2 | RC | 0.438 | 13.383 | 14.107 |
| Solid | base+P | 5.0 | 0.2 | SC | 0.815 | 34.849 | 14.107 |
| Solid | base+P | 10.0 | 0.05 | RC | 0.74 | 28.562 | 13.938 |
| Solid | base+P | 10.0 | 0.05 | SC | 0.959 | 60.668 | 13.938 |
| Solid | base+P | 10.0 | 0.1 | RC | 0.602 | 20.562 | 13.938 |
| Solid | base+P | 10.0 | 0.1 | SC | 0.913 | 46.926 | 13.938 |
| Solid | base+P | 10.0 | 0.2 | RC | 0.439 | 13.415 | 13.938 |
| Solid | base+P | 10.0 | 0.2 | SC | 0.804 | 33.714 | 13.938 |




**Table S8.** k-shot results with method-of-moments vs REML estimates of the between-study variance.

| target | features | estimator | k | Median study RMSE | Median study coverage | Width (wt%) |
|---|---|---|---|---|---|---|
| Bio-oil | base | MoM | 0.0 | 12.343 | 1.0 | 55.749 |
| Bio-oil | base | MoM | 1.0 | 9.447 | 0.978 | 40.956 |
| Bio-oil | base | MoM | 2.0 | 8.691 | 0.97 | 37.729 |
| Bio-oil | base | MoM | 3.0 | 8.523 | 0.967 | 36.551 |
| Bio-oil | base | MoM | 5.0 | 8.015 | 0.98 | 35.879 |
| Bio-oil | base | MoM | 10.0 | 7.847 | 0.972 | 33.629 |
| Bio-oil | base | REML | 0.0 | 12.343 | 1.0 | 55.749 |
| Bio-oil | base | REML | 1.0 | 9.335 | 0.97 | 40.504 |
| Bio-oil | base | REML | 2.0 | 8.718 | 0.971 | 37.64 |
| Bio-oil | base | REML | 3.0 | 8.474 | 0.965 | 36.256 |
| Bio-oil | base | REML | 5.0 | 8.005 | 0.973 | 35.931 |
| Bio-oil | base | REML | 10.0 | 7.845 | 0.967 | 33.755 |
| Bio-oil | base+P | MoM | 0.0 | 12.613 | 1.0 | 58.715 |
| Bio-oil | base+P | MoM | 1.0 | 10.057 | 0.98 | 42.279 |
| Bio-oil | base+P | MoM | 2.0 | 8.838 | 0.979 | 38.928 |
| Bio-oil | base+P | MoM | 3.0 | 8.4 | 0.973 | 37.576 |
| Bio-oil | base+P | MoM | 5.0 | 8.065 | 0.983 | 36.164 |
| Bio-oil | base+P | MoM | 10.0 | 7.59 | 0.975 | 33.853 |
| Bio-oil | base+P | REML | 0.0 | 12.613 | 1.0 | 58.715 |
| Bio-oil | base+P | REML | 1.0 | 9.371 | 0.98 | 42.301 |
| Bio-oil | base+P | REML | 2.0 | 8.812 | 0.974 | 38.887 |
| Bio-oil | base+P | REML | 3.0 | 8.416 | 0.965 | 37.413 |
| Bio-oil | base+P | REML | 5.0 | 8.073 | 0.981 | 36.142 |
| Bio-oil | base+P | REML | 10.0 | 7.584 | 0.975 | 33.958 |
| Solid | base | MoM | 0.0 | 10.537 | 1.0 | 46.419 |
| Solid | base | MoM | 1.0 | 8.876 | 0.992 | 39.127 |
| Solid | base | MoM | 2.0 | 8.268 | 0.996 | 35.71 |
| Solid | base | MoM | 3.0 | 7.749 | 0.995 | 35.146 |
| Solid | base | MoM | 5.0 | 7.136 | 0.995 | 33.432 |
| Solid | base | MoM | 10.0 | 6.721 | 1.0 | 34.108 |
| Solid | base | REML | 0.0 | 10.537 | 1.0 | 46.419 |
| Solid | base | REML | 1.0 | 9.192 | 0.998 | 44.343 |
| Solid | base | REML | 2.0 | 8.612 | 0.997 | 39.718 |
| Solid | base | REML | 3.0 | 8.594 | 0.997 | 38.939 |
| Solid | base | REML | 5.0 | 8.312 | 0.999 | 36.034 |
| Solid | base | REML | 10.0 | 7.747 | 1.0 | 35.651 |
| Solid | base+P | MoM | 0.0 | 10.674 | 1.0 | 46.636 |
| Solid | base+P | MoM | 1.0 | 8.89 | 0.994 | 39.247 |
| Solid | base+P | MoM | 2.0 | 8.161 | 0.991 | 35.68 |
| Solid | base+P | MoM | 3.0 | 7.876 | 0.992 | 34.247 |
| Solid | base+P | MoM | 5.0 | 7.742 | 0.992 | 32.88 |
| Solid | base+P | MoM | 10.0 | 6.933 | 0.999 | 33.515 |
| Solid | base+P | REML | 0.0 | 10.674 | 1.0 | 46.636 |
| Solid | base+P | REML | 1.0 | 9.335 | 1.0 | 42.411 |
| Solid | base+P | REML | 2.0 | 8.457 | 0.999 | 39.1 |
| Solid | base+P | REML | 3.0 | 8.424 | 0.999 | 37.731 |
| Solid | base+P | REML | 5.0 | 8.294 | 1.0 | 35.803 |
| Solid | base+P | REML | 10.0 | 8.064 | 1.0 | 35.138 |




**Table S9.** Study-grouped CV of the STRATA base learner with tuned vs library-default hyper-parameters.

| target | features | config | rmse | r2 | median_study_rmse |
|---|---|---|---|---|---|
| Bio-oil | base | tuned | 15.848 | 0.226 | 12.729 |
| Bio-oil | base | default | 16.046 | 0.206 | 12.418 |
| Bio-oil | base+P | tuned | 16.181 | 0.193 | 12.244 |
| Bio-oil | base+P | default | 17.206 | 0.087 | 13.555 |
| Solid | base | tuned | 14.076 | 0.516 | 10.835 |
| Solid | base | default | 14.035 | 0.519 | 10.078 |
| Solid | base+P | tuned | 13.818 | 0.534 | 10.913 |
| Solid | base+P | default | 14.821 | 0.463 | 11.439 |




**Table S10.** k-shot adaptation to a new study (studies with ≥ 11 runs; 20 random support sets per study).

| Target | k | Offset | Median study RMSE | Coverage (studies) | Width (wt%) | Studies | EB vs raw: Δ median; p_Holm |
|---|---|---|---|---|---|---|---|
| Bio-oil | 0 | — | 12.37 | 0.926 | 59.3 | 80 |  |
| Bio-oil | 1 | EB shrinkage | 9.22 | 0.908 | 42.6 | 80 | -0.75; <0.001 |
| Bio-oil | 1 | raw mean | 10.23 | 0.907 | 45.9 | 80 |  |
| Bio-oil | 2 | EB shrinkage | 8.78 | 0.914 | 39.0 | 80 | -0.29; <0.001 |
| Bio-oil | 2 | raw mean | 9.17 | 0.911 | 39.9 | 80 |  |
| Bio-oil | 3 | EB shrinkage | 8.47 | 0.913 | 37.2 | 80 | -0.14; <0.001 |
| Bio-oil | 3 | raw mean | 8.7 | 0.91 | 37.7 | 80 |  |
| Bio-oil | 5 | EB shrinkage | 8.19 | 0.918 | 36.3 | 80 | -0.07; <0.001 |
| Bio-oil | 5 | raw mean | 8.29 | 0.915 | 36.5 | 80 |  |
| Bio-oil | 10 | EB shrinkage | 7.63 | 0.902 | 33.4 | 80 | -0.02; 0.004 |
| Bio-oil | 10 | raw mean | 7.63 | 0.903 | 33.9 | 80 |  |
| Solid | 0 | — | 11.05 | 0.898 | 46.6 | 72 |  |
| Solid | 1 | EB shrinkage | 8.84 | 0.908 | 39.3 | 72 | -0.92; <0.001 |
| Solid | 1 | raw mean | 9.18 | 0.911 | 45.7 | 72 |  |
| Solid | 2 | EB shrinkage | 8.18 | 0.899 | 35.8 | 72 | -0.34; 0.002 |
| Solid | 2 | raw mean | 8.31 | 0.901 | 38.2 | 72 |  |
| Solid | 3 | EB shrinkage | 7.66 | 0.899 | 34.6 | 72 | -0.19; 0.003 |
| Solid | 3 | raw mean | 7.87 | 0.9 | 35.9 | 72 |  |
| Solid | 5 | EB shrinkage | 7.48 | 0.898 | 33.0 | 72 | -0.09; 0.007 |
| Solid | 5 | raw mean | 7.38 | 0.899 | 33.6 | 72 |  |
| Solid | 10 | EB shrinkage | 7.02 | 0.904 | 33.6 | 72 | -0.03; 0.006 |
| Solid | 10 | raw mean | 6.99 | 0.903 | 33.7 | 72 |  |




**Table S11.** Temporal, feedstock-family and external generalisation of the STRATA base learner.

| Target | Features | Scheme | RMSE | R² | Median study RMSE |
|---|---|---|---|---|---|
| Bio-oil | base | temporal | 19.41 | -0.399 | 14.81 |
| Bio-oil | base+P | temporal | 22.66 | -0.907 | 16.96 |
| Solid | base | temporal | 16.54 | 0.269 | 10.58 |
| Solid | base+P | temporal | 16.56 | 0.268 | 10.83 |
| Bio-oil | base | family_out (mean over families) | 17.17 | -0.419 | 12.93 |
| Bio-oil | base+P | family_out (mean over families) | 17.48 | -0.237 | 12.05 |
| Solid | base | family_out (mean over families) | 16.35 | -0.221 | 10.79 |
| Solid | base+P | family_out (mean over families) | 15.5 | -0.03 | 10.28 |
| Solid | base | external_4TU_all_dev_processes | 13.3 | 0.31 | 10.93 |
| Solid | base | external_4TU_HTC_dev_only | 16.66 | -0.082 | 11.59 |



# S4. Exploratory: locally adaptive study-calibrated intervals (post hoc)

Motivation: constant-width study-calibrated intervals are wide. Hypothesis: out-of-study errors are heteroscedastic, so dividing conformity scores by a learned difficulty $\hat\sigma(\mathbf{x})$ narrows intervals for easy regimes without losing study-level coverage. A shallow gradient-boosting model of $\log(|r| + 0.5)$ was cross-fitted by study on the out-of-study residuals of the training studies; scores $|r|/\hat\sigma$ were calibrated with the same study-weighted quantile, and intervals were $f(\mathbf{x}) \pm \hat q\,\hat\sigma(\mathbf{x})$. For bio-oil, SC-N gave study-weighted coverage 0.91 (SC 0.91) with median width 55.6 vs 59.5 wt% and mean interval score 84.2 vs 77.3; for solids, coverage 0.92 vs 0.91, median width 53.3 vs 45.7 wt%, interval score 69.5 vs 65.2. The adaptive variant therefore did not improve interval efficiency — both widths and interval scores were worse — although coverage across process subtypes became more uniform (largest deviation from 0.90: 0.03 vs 0.07 for solids). This negative result is consistent with the main finding that the dominant error component is a study offset that input features cannot localise. Because this variant was added after inspecting pipeline-verification results, it is reported as exploratory and is not part of the main claims.


**Table S12.** Exploratory (post hoc): constant-width vs locally adaptive study-calibrated intervals (α = 0.1, base+P).

| target | method | coverage_rows | coverage_studies | mean_width | median_width | winkler | coverage_by_process | max_abs_process_dev |
|---|---|---|---|---|---|---|---|---|
| Bio-oil | RC | 0.612 | 0.57 | 22.832 | 22.756 | 107.655 | {'HTL': 0.609, 'HTL_solvothermal': 0.52} | 0.38 |
| Bio-oil | SC | 0.93 | 0.909 | 59.079 | 59.499 | 77.294 | {'HTL': 0.932, 'HTL_solvothermal': 0.881} | 0.032 |
| Bio-oil | SC-N | 0.915 | 0.914 | 63.008 | 55.638 | 84.231 | {'HTL': 0.929, 'HTL_solvothermal': 0.897} | 0.029 |
| Solid | RC | 0.615 | 0.614 | 20.564 | 20.554 | 93.706 | {'HTC': 0.527, 'HTL': 0.644, 'HTL_solvothermal': 0.577} | 0.373 |
| Solid | SC | 0.901 | 0.908 | 46.672 | 45.651 | 65.196 | {'HTC': 0.827, 'HTL': 0.916, 'HTL_solvothermal': 0.905} | 0.073 |
| Solid | SC-N | 0.921 | 0.92 | 57.302 | 53.283 | 69.497 | {'HTC': 0.868, 'HTL': 0.925, 'HTL_solvothermal': 0.92} | 0.032 |



# S5. Error analysis by subgroup


**Table S13.** Out-of-study errors by subgroup (seed-averaged outer-fold predictions, base features).

| target | dimension | level | n | n_studies | rmse | bias | mae |
|---|---|---|---|---|---|---|---|
| Bio-oil | family | Agricultural Residues | 804 | 56 | 14.0 | -1.21 | 10.47 |
| Bio-oil | family | Animal Manure | 36 | 4 | 14.7 | -11.29 | 11.63 |
| Bio-oil | family | Aquatic Biomass | 19 | 3 | 20.23 | -9.17 | 19.07 |
| Bio-oil | family | Herbaceous Biomass | 4 | 1 | 20.98 | -14.32 | 17.42 |
| Bio-oil | family | Lignin-rich Streams (Technical) | 189 | 17 | 17.52 | 0.24 | 13.88 |
| Bio-oil | family | Mixed Biomass | 205 | 16 | 16.63 | -2.93 | 12.93 |
| Bio-oil | family | Other | 91 | 6 | 33.89 | 14.33 | 25.89 |
| Bio-oil | family | Plastics / Polymer Blends | 11 | 2 | 33.62 | -31.14 | 31.14 |
| Bio-oil | family | Waste Biomass / Sludge | 40 | 6 | 12.78 | -6.31 | 9.65 |
| Bio-oil | family | Waste Wood / Construction | 33 | 5 | 19.41 | 0.27 | 16.48 |
| Bio-oil | family | Woody Biomass / Hardwood | 417 | 27 | 12.43 | -0.38 | 8.58 |
| Bio-oil | family | Woody Biomass / Softwood | 352 | 29 | 10.72 | -4.15 | 7.94 |
| Bio-oil | family | Woody Biomass / Unspecified | 60 | 9 | 16.24 | 5.1 | 11.97 |
| Bio-oil | process | HTL | 1513 | 91 | 13.85 | -1.99 | 10.09 |
| Bio-oil | process | HTL_solvothermal | 748 | 46 | 18.5 | 0.33 | 13.36 |
| Bio-oil | extraction_solvent | acetone | 783 | 47 | 12.94 | -2.07 | 9.61 |
| Bio-oil | extraction_solvent | alcohol | 191 | 14 | 13.92 | -0.41 | 12.32 |
| Bio-oil | extraction_solvent | chlorinated_other | 2 | 1 | 10.22 | 9.25 | 9.25 |
| Bio-oil | extraction_solvent | dcm | 365 | 24 | 16.47 | -3.35 | 12.63 |
| Bio-oil | extraction_solvent | diethyl_ether | 46 | 6 | 14.21 | -9.52 | 13.4 |
| Bio-oil | extraction_solvent | ethyl_acetate | 179 | 10 | 14.67 | -6.55 | 12.03 |
| Bio-oil | extraction_solvent | hydrocarbon | 149 | 6 | 10.81 | 0.32 | 8.13 |
| Bio-oil | extraction_solvent | none_named | 514 | 31 | 19.8 | 2.7 | 12.34 |
| Bio-oil | extraction_solvent | thf | 32 | 4 | 19.29 | 9.71 | 13.66 |
| Bio-oil | temperature_bin | 250-300 | 1129 | 95 | 13.35 | -1.7 | 9.96 |
| Bio-oil | temperature_bin | 300-350 | 565 | 76 | 15.7 | 1.0 | 11.15 |
| Bio-oil | temperature_bin | <=250 | 354 | 50 | 21.12 | -1.13 | 15.01 |
| Bio-oil | temperature_bin | >350 | 213 | 36 | 14.96 | -4.76 | 11.27 |
| Bio-oil | catalyst_present | no | 1061 | 104 | 15.02 | -1.97 | 11.11 |
| Bio-oil | catalyst_present | yes | 1200 | 91 | 15.99 | -0.56 | 11.23 |
| Bio-oil | yield_basis_daf | daf | 332 | 17 | 13.35 | -0.48 | 9.27 |
| Bio-oil | yield_basis_daf | dry/other | 1929 | 106 | 15.89 | -1.35 | 11.5 |
| Solid | family | Agricultural Residues | 781 | 55 | 12.45 | 1.7 | 9.73 |
| Solid | family | Animal Manure | 33 | 3 | 10.25 | -4.69 | 9.06 |
| Solid | family | Aquatic Biomass | 19 | 3 | 17.15 | -12.64 | 15.62 |
| Solid | family | Herbaceous Biomass | 44 | 4 | 18.34 | -11.52 | 13.57 |
| Solid | family | Lignin-rich Streams (Technical) | 221 | 21 | 14.86 | -6.18 | 11.12 |
| Solid | family | Mixed Biomass | 196 | 15 | 12.99 | 2.26 | 10.27 |
| Solid | family | Model Compound | 5 | 1 | 4.69 | -1.35 | 4.18 |
| Solid | family | Other | 67 | 7 | 31.91 | -3.95 | 27.2 |
| Solid | family | Waste Biomass / Sludge | 72 | 5 | 19.44 | 8.84 | 16.81 |
| Solid | family | Waste Wood / Construction | 31 | 4 | 7.36 | 1.37 | 6.0 |
| Solid | family | Woody Biomass / Hardwood | 304 | 23 | 12.36 | -1.21 | 8.98 |
| Solid | family | Woody Biomass / Softwood | 350 | 23 | 10.21 | 2.08 | 7.34 |
| Solid | family | Woody Biomass / Unspecified | 33 | 7 | 11.07 | -1.85 | 8.32 |
| Solid | process | HTC | 380 | 16 | 14.93 | -0.99 | 11.49 |
| Solid | process | HTL | 1180 | 80 | 12.66 | -1.05 | 9.0 |
| Solid | process | HTL_solvothermal | 596 | 40 | 15.16 | 3.07 | 11.9 |
| Solid | extraction_solvent | acetone | 690 | 42 | 13.81 | 1.63 | 9.52 |
| Solid | extraction_solvent | alcohol | 153 | 13 | 10.8 | -0.99 | 9.05 |
| Solid | extraction_solvent | dcm | 306 | 21 | 13.02 | -0.92 | 9.87 |
| Solid | extraction_solvent | diethyl_ether | 39 | 3 | 13.95 | -5.95 | 11.64 |
| Solid | extraction_solvent | ethyl_acetate | 111 | 8 | 17.08 | -4.3 | 14.0 |
| Solid | extraction_solvent | hydrocarbon | 80 | 2 | 17.52 | 14.17 | 16.13 |
| Solid | extraction_solvent | none_named | 745 | 37 | 13.86 | -1.14 | 10.24 |
| Solid | extraction_solvent | thf | 32 | 4 | 7.83 | -1.59 | 5.28 |
| Solid | temperature_bin | 250-300 | 962 | 89 | 13.74 | 1.03 | 10.4 |
| Solid | temperature_bin | 300-350 | 458 | 70 | 12.66 | -1.19 | 8.8 |
| Solid | temperature_bin | <=250 | 546 | 61 | 14.88 | -0.24 | 11.24 |
| Solid | temperature_bin | >350 | 190 | 29 | 13.57 | -0.56 | 10.04 |
| Solid | catalyst_present | no | 1291 | 104 | 13.43 | -0.01 | 10.23 |
| Solid | catalyst_present | yes | 865 | 81 | 14.34 | 0.25 | 10.26 |
| Solid | yield_basis_daf | daf | 418 | 16 | 14.31 | 1.08 | 11.28 |
| Solid | yield_basis_daf | dry/other | 1738 | 105 | 13.68 | -0.14 | 9.99 |



# S6. STRATA with different base learners (E9)


**Table S14.** STRATA with different base learners (development study-folds, seed 11, base + P features, α = 0.1). The mean predictor is the 'no-ML' reference.

| Target | Base learner | Coverage RC | Coverage SC | Width RC (wt%) | Width SC (wt%) | Pooled RMSE | Median study RMSE k=0 | Median study RMSE k=3 (EB) |
|---|---|---|---|---|---|---|---|---|
| Bio-oil | Extra trees | 0.575 | 0.903 | 25.1 | 54.062 | 16.264 | 13.175 | 8.216 |
| Bio-oil | k-NN | 0.647 | 0.91 | 30.43 | 58.999 | 16.935 | 13.392 | 8.831 |
| Bio-oil | LightGBM | 0.553 | 0.904 | 22.542 | 53.69 | 15.869 | 12.512 | 8.415 |
| Bio-oil | Mean | 0.86 | 0.901 | 54.59 | 63.046 | 18.078 | 13.355 | 9.15 |
| Bio-oil | Random forest | 0.588 | 0.904 | 24.544 | 53.502 | 16.09 | 12.286 | 8.183 |
| Bio-oil | Ridge | 0.8 | 0.899 | 43.064 | 58.986 | 17.523 | 14.159 | 8.727 |
| Bio-oil | XGBoost | 0.559 | 0.904 | 22.495 | 58.394 | 16.181 | 12.244 | 8.4 |
| Solid | Extra trees | 0.672 | 0.899 | 25.849 | 49.029 | 15.237 | 11.016 | 8.545 |
| Solid | k-NN | 0.727 | 0.909 | 33.243 | 50.757 | 16.438 | 13.815 | 10.325 |
| Solid | LightGBM | 0.605 | 0.913 | 20.15 | 45.962 | 13.837 | 10.548 | 7.849 |
| Solid | Mean | 0.935 | 0.904 | 63.637 | 59.37 | 20.599 | 16.982 | 9.889 |
| Solid | Random forest | 0.7 | 0.919 | 26.475 | 47.45 | 14.158 | 10.865 | 7.856 |
| Solid | Ridge | 0.846 | 0.893 | 43.308 | 50.622 | 16.973 | 13.035 | 9.19 |
| Solid | XGBoost | 0.602 | 0.913 | 20.768 | 46.847 | 13.818 | 10.913 | 7.876 |



# S7. Trend, ranking and anchoring analyses (Addenda A, A2, B, C)

*Within-study contrasts (E12).* For two runs *a* and *b* of the same study, the contrast is $\Delta_{ab} = y_a - y_b$; a study offset cancels in $\Delta_{ab}$. Three learners predicted contrasts for every pair of runs within each unseen study: the absolute model A by differencing, $\hat\Delta_{ab} = f(\mathbf{x}_a) - f(\mathbf{x}_b)$; a within-study model W, trained on study-centred targets $y - \bar y_{\text{study}}$ with features $[\mathbf{x}, \mathbf{x} - \bar{\mathbf{x}}_{\text{study}}]$; and a pairwise-difference model PD, trained on pairs of runs of the same training study with inputs $[\mathbf{x}_a, \mathbf{x}_b, \mathbf{x}_a - \mathbf{x}_b]$ and target $\Delta_{ab}$ (at most 30 random partners per run), antisymmetrised as $\hat\Delta_{ab} = \tfrac{1}{2}[h(a,b) - h(b,a)]$. All three used the E1 hyper-parameters of XGBoost, extra trees and LightGBM. Contrast accuracy was summarised by $R^2_\Delta = 1 - \sum(\hat\Delta - \Delta)^2 / \sum \Delta^2$, relative to the 'no-change' predictor. Hypotheses: contrasts are predicted better than levels (T1); W and PD predict contrasts better than A (T2, one-sided Wilcoxon on per-study contrast RMSE, Holm); anchoring on *k* = 1–3 measured runs, $\hat y_i = \tfrac{1}{k}\sum_a (y_a + \hat\Delta_{ia})$, beats STRATA's shrunk offset (T3); study-calibrated intervals for contrasts are valid and narrower than for levels (T4); and models rank the runs of a study usefully (T5). The same analysis was repeated for bio-oil higher heating value (1,019 development runs from 106 studies, 245 locked runs) and bio-oil carbon content (1,036 runs, 110 studies; 227 locked runs) (Addendum A2).

*Model-free trends (E13; descriptive).* Within each development study, pairs of runs that differ only in temperature (all other base features and the feedstock identical) or only in residence time were identified, and their slopes summarised per study and temperature band; medians across studies were bootstrapped over studies. Below 250 °C bio-oil yield changed by +1.31 wt% per 10 °C (95% same sign), at 250–300 °C by +0.87 wt%, at 300–350 °C by -0.14 wt% and above 350 °C by -0.79 wt%; solid yield changed by -2.66, -1.70, -0.62 and -0.35 wt% per 10 °C. Doubling the residence time had no consistent effect on bio-oil yield (-0.06 wt%; 50% same sign) and a small negative effect on solid yield (-0.49 wt%).

*Contrast results.* For unseen development studies, contrast $R^2_\Delta$ was 0.14–0.22 for bio-oil (level R² 0.15–0.19) and 0.25–0.43 for solids (levels 0.36–0.47); weighting studies equally, the median per-study $R^2_\Delta$ was 0.06–0.10 for bio-oil and 0.23–0.32 for solids. On locked studies offset-invariant models retained contrast skill where the absolute model failed (bio-oil $R^2_\Delta$ -0.30 for A vs 0.21 for W and 0.30 for PD), but two studies accounted for 65% of the squared contrast error of A, and per-study comparisons were not significant (0 of 12 after Holm). With one measured run, the median per-study RMSE was 9.60 wt% for STRATA, 10.20 for W and 9.41 for PD (bio-oil, XGBoost; T3 not supported). Intervals for contrasts covered 0.90 (bio-oil) and 0.91 (solids) of unseen-study pairs (T4).

*Ranking (E14).* For unseen development studies, all three model types picked bio-oil conditions with lower regret than the 325 °C rule of thumb (median regret 7.0–8.7 vs 12.8 wt%; random choice 12.7 wt%); for solids none beat the lowest-temperature rule. On 25 locked bio-oil studies the advantage was not confirmed (median regret 11.9–12.5 wt% for the models, 14.6 wt% for the rule and 12.5 wt% for random choice).


![**Fig. S1.** Model-free trend atlas. Median change in yield per +10 °C across development studies, computed from pairs of runs of the same study that differ only in temperature; error bars are 95% study-bootstrap CIs, annotations give the share of studies whose slope has the same sign as the median.](/home/user/rp_c_12/figures/fig11_trend_atlas.png){width=16cm}



![**Fig. S2.** Accuracy of absolute-yield predictions (levels, model A) and of within-study contrasts (models A, W and PD; XGBoost) for unseen development studies and for the locked test studies, for four targets. R² of contrasts is relative to the no-change predictor.](/home/user/rp_c_12/figures/fig12_levels_vs_contrasts.png){width=16cm}



![**Fig. S3.** Regret of choosing the run predicted to give the highest yield within a study for models A, W and PD, a rule of thumb and random choice. Left: development studies (exploratory); right: locked studies (pre-registered confirmatory test).](/home/user/rp_c_12/figures/fig13_ranking_regret.png){width=16cm}



**Table S15.** Model-free within-study trends: slopes from run pairs of the same study that differ only in temperature or only in residence time (development studies; 95% study-bootstrap CIs).

| Target | Variable | Unit | Band (°C) | Studies | Pairs | Median slope [95% CI] | Studies with same sign | Between-study SD of slope |
|---|---|---|---|---|---|---|---|---|
| Bio-oil yield | Temperature | per +10 °C | 150-250 | 21 | 220 | +1.31 [+0.97, +1.64] | 0.95 | 2.75 |
| Bio-oil yield | Temperature | per +10 °C | 250-300 | 63 | 1283 | +0.87 [+0.71, +1.27] | 0.81 | 2.28 |
| Bio-oil yield | Temperature | per +10 °C | 300-350 | 53 | 1119 | -0.14 [-0.48, +0.12] | 0.55 | 2.22 |
| Bio-oil yield | Temperature | per +10 °C | 350-450 | 21 | 172 | -0.79 [-1.56, +0.19] | 0.62 | 2.03 |
| Bio-oil yield | Residence time | per doubling of residence time | all | 58 | 1138 | -0.06 [-0.66, +0.61] | 0.5 | 5.35 |
| Solid yield | Temperature | per +10 °C | 150-250 | 28 | 600 | -2.66 [-3.34, -2.09] | 0.86 | 2.54 |
| Solid yield | Temperature | per +10 °C | 250-300 | 65 | 1242 | -1.70 [-1.94, -1.49] | 0.86 | 2.05 |
| Solid yield | Temperature | per +10 °C | 300-350 | 50 | 1094 | -0.62 [-0.86, -0.48] | 0.72 | 1.26 |
| Solid yield | Temperature | per +10 °C | 350-450 | 18 | 140 | -0.35 [-0.91, +0.13] | 0.61 | 2.2 |
| Solid yield | Residence time | per doubling of residence time | all | 52 | 1209 | -0.49 [-1.02, -0.13] | 0.62 | 6.9 |




**Table S16.** Level vs within-study contrast accuracy for models A, W and PD (XGBoost), with study-calibrated contrast and level interval coverage/width (α = 0.1).

| Target | Setting | Model | Level R² | Contrast R² | Median within-study Spearman | Contrast interval coverage | Contrast interval width | Level interval width |
|---|---|---|---|---|---|---|---|---|
| Bio-oil yield | Development (unseen studies) | A | 0.184 | 0.214 | 0.404 | 0.9 | 44.901 | 55.753 |
| Bio-oil yield | Development (unseen studies) | PD |  | 0.165 | 0.407 | 0.898 | 44.795 | 55.753 |
| Bio-oil yield | Development (unseen studies) | W |  | 0.14 | 0.389 | 0.897 | 45.152 | 55.753 |
| Solid yield | Development (unseen studies) | A | 0.44 | 0.434 | 0.452 | 0.908 | 45.187 | 46.64 |
| Solid yield | Development (unseen studies) | PD |  | 0.368 | 0.584 | 0.908 | 45.956 | 46.64 |
| Solid yield | Development (unseen studies) | W |  | 0.367 | 0.603 | 0.91 | 44.354 | 46.64 |
| Bio-oil yield | Locked test | A | -0.954 | -0.301 | 0.071 | 0.943 | 44.383 | 53.71 |
| Bio-oil yield | Locked test | PD |  | 0.297 | 0.086 | 0.931 | 43.762 | 53.71 |
| Bio-oil yield | Locked test | W |  | 0.205 | 0.271 | 0.947 | 45.676 | 53.71 |
| Solid yield | Locked test | A | 0.295 | 0.434 | 0.541 | 0.891 | 44.716 | 46.536 |
| Solid yield | Locked test | PD |  | 0.551 | 0.469 | 0.885 | 44.124 | 46.536 |
| Solid yield | Locked test | W |  | 0.56 | 0.632 | 0.89 | 43.564 | 46.536 |
| Bio-oil C | Development (unseen studies) | A | 0.091 | 0.107 | 0.367 | 0.898 | 20.838 | 26.619 |
| Bio-oil C | Development (unseen studies) | PD |  | 0.172 | 0.435 | 0.899 | 20.245 | 26.619 |
| Bio-oil C | Development (unseen studies) | W |  | 0.129 | 0.478 | 0.904 | 20.016 | 26.619 |
| Bio-oil HHV | Development (unseen studies) | A | 0.206 | 0.388 | 0.389 | 0.902 | 12.316 | 16.917 |
| Bio-oil HHV | Development (unseen studies) | PD |  | 0.38 | 0.561 | 0.902 | 12.306 | 16.917 |
| Bio-oil HHV | Development (unseen studies) | W |  | 0.319 | 0.497 | 0.902 | 12.611 | 16.917 |
| Bio-oil C | Locked test | A | 0.242 | -0.067 | 0.342 | 0.957 | 21.557 | 28.321 |
| Bio-oil C | Locked test | PD |  | 0.221 | 0.681 | 0.966 | 20.877 | 28.321 |
| Bio-oil C | Locked test | W |  | 0.189 | 0.436 | 0.962 | 20.808 | 28.321 |
| Bio-oil HHV | Locked test | A | 0.249 | -0.099 | 0.42 | 0.922 | 12.573 | 16.711 |
| Bio-oil HHV | Locked test | PD |  | -0.003 | 0.528 | 0.909 | 12.177 | 16.711 |
| Bio-oil HHV | Locked test | W |  | -0.054 | 0.289 | 0.899 | 12.558 | 16.711 |




**Table S17.** Regret of choosing the run predicted best within a study vs rules of thumb (development: exploratory, two-sided; locked: pre-registered confirmatory, one-sided for bio-oil). Holm-corrected p.

| Setting | Target | Model | Rule of thumb | Studies | Median regret, model (wt%) | Median regret, rule (wt%) | Median paired difference [95% CI] | p (Holm) | Test |
|---|---|---|---|---|---|---|---|---|---|
| Development (exploratory) | Bio-oil yield | A | T300 | 110 | 8.74 | 13.55 | -3.95 [-6.48, -2.38] | 0.0 | two-sided |
| Development (exploratory) | Bio-oil yield | A | T325 | 110 | 8.74 | 12.77 | -3.98 [-6.13, -2.12] | 0.0 | two-sided |
| Development (exploratory) | Bio-oil yield | W | T300 | 110 | 7.2877 | 13.55 | -3.59 [-5.55, -2.04] | 0.0001 | two-sided |
| Development (exploratory) | Bio-oil yield | W | T325 | 110 | 7.2877 | 12.77 | -3.61 [-5.39, -1.13] | 0.0001 | two-sided |
| Development (exploratory) | Bio-oil yield | PD | T300 | 110 | 7.0 | 13.55 | -3.95 [-6.72, +0.00] | 0.0 | two-sided |
| Development (exploratory) | Bio-oil yield | PD | T325 | 110 | 7.0 | 12.77 | -3.38 [-5.69, -0.13] | 0.0 | two-sided |
| Development (exploratory) | Solid yield | A | lowest_T | 109 | 3.04 | 2.25 | +0.00 [+0.00, +0.00] | 0.6628 | two-sided |
| Development (exploratory) | Solid yield | W | lowest_T | 109 | 1.6133 | 2.25 | +0.00 [+0.00, +0.00] | 0.3022 | two-sided |
| Development (exploratory) | Solid yield | PD | lowest_T | 109 | 1.34 | 2.25 | +0.00 [+0.00, +0.00] | 0.1359 | two-sided |
| Locked test (confirmatory) | Bio-oil yield | A | T325 | 25 | 11.93 | 14.6 | -0.86 [-7.55, +2.99] | 0.6173 | less |
| Locked test (confirmatory) | Bio-oil yield | W | T325 | 25 | 12.5 | 14.6 | +0.00 [-3.55, +3.90] | 0.6612 | less |
| Locked test (confirmatory) | Bio-oil yield | PD | T325 | 25 | 11.93 | 14.6 | +0.00 [-7.55, +3.90] | 0.6612 | less |
| Locked test (confirmatory) | Solid yield | A | lowest_T | 27 | 1.85 | 5.5 | +0.00 [-0.40, +0.00] | 0.1401 | two-sided |
| Locked test (confirmatory) | Solid yield | W | lowest_T | 27 | 0.449 | 5.5 | +0.00 [-0.40, +0.00] | 0.1005 | two-sided |
| Locked test (confirmatory) | Solid yield | PD | lowest_T | 27 | 0.08 | 5.5 | +0.00 [+0.00, +0.00] | 0.3824 | two-sided |




**Table S18.** Model-free temperature slopes stratified by process subtype (development studies; 95% study-bootstrap CIs; strata with ≥ 5 studies).

| Target | Process | Band (°C) | Studies | Median slope (wt% per +10 °C) | CI low | CI high | Studies with same sign |
|---|---|---|---|---|---|---|---|
| Bio-oil yield | HTL | 150-250 | 13 | 1.31 | 0.76 | 1.68 | 1.0 |
| Bio-oil yield | HTL | 250-300 | 41 | 0.79 | 0.6 | 1.32 | 0.78 |
| Bio-oil yield | HTL | 300-350 | 35 | -0.31 | -0.63 | 0.11 | 0.6 |
| Bio-oil yield | HTL | 350-450 | 16 | -1.01 | -1.56 | 0.19 | 0.62 |
| Bio-oil yield | HTL_solvothermal | 150-250 | 8 | 1.4 | 0.97 | 3.38 | 0.88 |
| Bio-oil yield | HTL_solvothermal | 250-300 | 25 | 1.23 | 0.84 | 1.37 | 0.88 |
| Bio-oil yield | HTL_solvothermal | 300-350 | 19 | 0.06 | -0.31 | 0.61 | 0.53 |
| Bio-oil yield | HTL_solvothermal | 350-450 | 5 | -0.4 | -3.3 | 0.51 | 0.6 |
| Solid yield | HTC | 150-250 | 9 | -2.09 | -3.28 | -1.43 | 0.89 |
| Solid yield | HTC | 250-300 | 6 | -1.97 | -2.31 | -1.29 | 1.0 |
| Solid yield | HTL | 150-250 | 12 | -3.04 | -5.24 | -2.44 | 0.83 |
| Solid yield | HTL | 250-300 | 38 | -1.44 | -1.56 | -1.22 | 0.87 |
| Solid yield | HTL | 300-350 | 31 | -0.49 | -0.69 | -0.24 | 0.68 |
| Solid yield | HTL | 350-450 | 13 | -0.09 | -0.82 | 0.44 | 0.54 |
| Solid yield | HTL_solvothermal | 150-250 | 7 | -2.52 | -3.64 | -1.86 | 0.86 |
| Solid yield | HTL_solvothermal | 250-300 | 22 | -2.4 | -3.01 | -1.75 | 0.82 |
| Solid yield | HTL_solvothermal | 300-350 | 18 | -0.93 | -1.41 | -0.7 | 0.83 |
| Solid yield | HTL_solvothermal | 350-450 | 5 | -0.78 | -2.27 | -0.01 | 0.8 |




**Table S19.** Study-weighted within-study contrast accuracy (median over studies of the per-study contrast R²; XGBoost). Pooled values in Table S12 weight large studies by their number of pairs.

| Setting | Target | Model | Studies (≥ 5 runs) | Median per-study contrast R² | Studies with R² > 0 |
|---|---|---|---|---|---|
| dev | Bio-oil yield | A | 110 | 0.095 | 0.59 |
| dev | Bio-oil yield | PD | 110 | 0.056 | 0.56 |
| dev | Bio-oil yield | W | 110 | 0.082 | 0.61 |
| dev | Solid yield | A | 109 | 0.236 | 0.67 |
| dev | Solid yield | PD | 109 | 0.23 | 0.67 |
| dev | Solid yield | W | 109 | 0.32 | 0.68 |
| locked | Bio-oil yield | A | 25 | -0.278 | 0.24 |
| locked | Bio-oil yield | PD | 25 | -0.183 | 0.4 |
| locked | Bio-oil yield | W | 25 | -0.039 | 0.44 |
| locked | Solid yield | A | 27 | 0.16 | 0.74 |
| locked | Solid yield | PD | 27 | 0.138 | 0.67 |
| locked | Solid yield | W | 27 | 0.308 | 0.81 |
| dev_quality | Bio-oil carbon | A | 81 | -0.016 | 0.43 |
| dev_quality | Bio-oil carbon | PD | 81 | -0.0 | 0.44 |
| dev_quality | Bio-oil carbon | W | 81 | 0.015 | 0.53 |
| dev_quality | Bio-oil HHV | A | 80 | 0.0 | 0.5 |
| dev_quality | Bio-oil HHV | PD | 80 | 0.142 | 0.56 |
| dev_quality | Bio-oil HHV | W | 80 | 0.164 | 0.59 |
| locked_quality | Bio-oil carbon | A | 19 | 0.003 | 0.53 |
| locked_quality | Bio-oil carbon | PD | 19 | 0.219 | 0.79 |
| locked_quality | Bio-oil carbon | W | 19 | 0.134 | 0.63 |
| locked_quality | Bio-oil HHV | A | 21 | -0.034 | 0.43 |
| locked_quality | Bio-oil HHV | PD | 21 | 0.095 | 0.62 |
| locked_quality | Bio-oil HHV | W | 21 | 0.089 | 0.62 |



# S8. Additional figures and cost


![**Fig. S4.** Development data. (a) Number of runs contributed per source study; (b) yield distributions; (c) publication years of all 188 source studies (dashed line: temporal split).](/home/user/rp_c_12/figures/fig02_dataset.png){width=16cm}



![**Fig. S5.** *k*-shot adaptation to a new study with random support sets (development studies with ≥ 11 runs, base + P features, 20 random support sets per study and *k*). Top: median per-study RMSE of the remaining runs; bottom: width of the re-calibrated 90% interval.](/home/user/rp_c_12/figures/fig06_kshot.png){width=16cm}



![**Fig. S6.** Robustness of the STRATA base learner (base + P features). Top: RMSE (mean ± SD over outer folds) with Gaussian noise added to continuous test features or with fewer training studies. Bottom: study-weighted coverage of RC and SC 90% intervals.](/home/user/rp_c_12/figures/fig07_robustness.png){width=16cm}



![**Fig. S7.** Accuracy for unseen studies versus single-thread fit time on the development set (bio-oil, base features).](/home/user/rp_c_12/figures/fig08_efficiency.png){width=16cm}



![**Fig. S8.** Mean out-of-study residual by extraction solvent named in the source study (groups with ≥ 3 studies; base features, seed-averaged outer-fold predictions).](/home/user/rp_c_12/figures/fig09_error_by_solvent.png){width=16cm}



![**Fig. S9.** Observed versus predicted yields for the STRATA base learner under random-row CV and study-grouped CV (seed 11).](/home/user/rp_c_12/figures/fig10_parity.png){width=16cm}



**Table S20.** Computational cost (bio-oil, development set, single thread). Peak RSS increase is measured relative to the process peak after data loading.

| Learner | Fit time (s) | Predict (ms / 1000 rows) | Peak RSS increase (MB) | Serialized size (MB) |
|---|---|---|---|---|
| Mean | 0.006 | 0.024 | 0.0 | 0.0 |
| Ridge | 0.013 | 0.525 | 0.0 | 0.003 |
| k-NN | 0.013 | 16.627 | 0.0 | 0.624 |
| SVR | 0.169 | 68.935 | 2.488 | 0.438 |
| MLP | 9.265 | 1.186 | 0.0 | 0.146 |
| Random forest | 1.54 | 35.689 | 14.715 | 25.699 |
| Extra trees | 0.919 | 45.194 | 17.254 | 28.432 |
| HistGB | 1.295 | 25.176 | 0.0 | 2.672 |
| LightGBM | 0.577 | 81.663 | 9.906 | 3.214 |
| XGBoost | 0.194 | 4.017 | 5.891 | 0.867 |
| CatBoost | 3.445 | 1.236 | 39.953 | 3.705 |
| GPBoost | 0.448 | 46.436 | 17.918 |  |



# S9. Additional deployment results (Addendum D)


**Table S21.** Retrospective simulated deployment in screening-design order, long format with median per-study MAE (otherwise as in the main deployment table).

| Setting | Target | Local runs k | Strategy | Studies | Median RMSE (wt%) | Median MAE (wt%) | Coverage of 90% PI | PI width (wt%) |
|---|---|---|---|---|---|---|---|---|
| Development (unseen studies) | Bio-oil yield | 0 | A · literature only | 80 | 12.39 | 10.15 | 0.94 | 60.9 |
| Development (unseen studies) | Bio-oil yield | 1 | A · literature only | 80 | 12.39 | 10.15 | 0.94 | 60.9 |
| Development (unseen studies) | Bio-oil yield | 1 | B · STRATA (literature + local runs) | 80 | 8.84 | 7.64 | 0.94 | 49.24 |
| Development (unseen studies) | Bio-oil yield | 1 | C · local runs only | 80 | 10.44 | 8.46 | 0.93 | 61.92 |
| Development (unseen studies) | Bio-oil yield | 3 | A · literature only | 80 | 12.39 | 10.15 | 0.94 | 60.9 |
| Development (unseen studies) | Bio-oil yield | 3 | B · STRATA (literature + local runs) | 80 | 8.77 | 6.87 | 0.94 | 44.3 |
| Development (unseen studies) | Bio-oil yield | 3 | C · local runs only | 80 | 9.91 | 8.41 | 0.92 | 49.51 |
| Development (unseen studies) | Bio-oil yield | 5 | A · literature only | 80 | 12.39 | 10.15 | 0.94 | 60.9 |
| Development (unseen studies) | Bio-oil yield | 5 | B · STRATA (literature + local runs) | 80 | 8.41 | 6.43 | 0.92 | 42.02 |
| Development (unseen studies) | Bio-oil yield | 5 | C · local runs only | 80 | 9.5 | 7.99 | 0.92 | 46.57 |
| Development (unseen studies) | Solid yield | 0 | A · literature only | 72 | 9.38 | 8.6 | 0.89 | 45.61 |
| Development (unseen studies) | Solid yield | 1 | A · literature only | 72 | 9.38 | 8.6 | 0.89 | 45.61 |
| Development (unseen studies) | Solid yield | 1 | B · STRATA (literature + local runs) | 72 | 8.8 | 7.05 | 0.9 | 39.54 |
| Development (unseen studies) | Solid yield | 1 | C · local runs only | 72 | 11.2 | 8.76 | 0.9 | 55.76 |
| Development (unseen studies) | Solid yield | 3 | A · literature only | 72 | 9.38 | 8.6 | 0.89 | 45.61 |
| Development (unseen studies) | Solid yield | 3 | B · STRATA (literature + local runs) | 72 | 7.76 | 6.37 | 0.89 | 38.19 |
| Development (unseen studies) | Solid yield | 3 | C · local runs only | 72 | 10.46 | 9.18 | 0.89 | 48.96 |
| Development (unseen studies) | Solid yield | 5 | A · literature only | 72 | 9.38 | 8.6 | 0.89 | 45.61 |
| Development (unseen studies) | Solid yield | 5 | B · STRATA (literature + local runs) | 72 | 7.71 | 6.33 | 0.89 | 34.02 |
| Development (unseen studies) | Solid yield | 5 | C · local runs only | 72 | 9.99 | 8.51 | 0.88 | 42.83 |
| Locked studies | Bio-oil yield | 0 | A · literature only | 19 | 10.3 | 8.02 | 0.9 | 58.02 |
| Locked studies | Bio-oil yield | 1 | A · literature only | 19 | 10.3 | 8.02 | 0.9 | 58.02 |
| Locked studies | Bio-oil yield | 1 | B · STRATA (literature + local runs) | 19 | 8.15 | 6.74 | 0.97 | 48.75 |
| Locked studies | Bio-oil yield | 1 | C · local runs only | 19 | 6.43 | 5.15 | 1.0 | 62.28 |
| Locked studies | Bio-oil yield | 3 | A · literature only | 19 | 10.3 | 8.02 | 0.9 | 58.02 |
| Locked studies | Bio-oil yield | 3 | B · STRATA (literature + local runs) | 19 | 7.96 | 6.72 | 0.92 | 43.49 |
| Locked studies | Bio-oil yield | 3 | C · local runs only | 19 | 5.97 | 4.68 | 1.0 | 48.87 |
| Locked studies | Bio-oil yield | 5 | A · literature only | 19 | 10.3 | 8.02 | 0.9 | 58.02 |
| Locked studies | Bio-oil yield | 5 | B · STRATA (literature + local runs) | 19 | 7.34 | 6.22 | 0.94 | 41.09 |
| Locked studies | Bio-oil yield | 5 | C · local runs only | 19 | 6.35 | 4.8 | 0.99 | 45.88 |
| Locked studies | Solid yield | 0 | A · literature only | 18 | 13.44 | 11.96 | 0.85 | 45.2 |
| Locked studies | Solid yield | 1 | A · literature only | 18 | 13.44 | 11.96 | 0.85 | 45.2 |
| Locked studies | Solid yield | 1 | B · STRATA (literature + local runs) | 18 | 7.66 | 6.84 | 0.8 | 37.43 |
| Locked studies | Solid yield | 1 | C · local runs only | 18 | 9.85 | 8.24 | 0.9 | 55.4 |
| Locked studies | Solid yield | 3 | A · literature only | 18 | 13.44 | 11.96 | 0.85 | 45.2 |
| Locked studies | Solid yield | 3 | B · STRATA (literature + local runs) | 18 | 7.08 | 6.1 | 0.84 | 38.64 |
| Locked studies | Solid yield | 3 | C · local runs only | 18 | 8.49 | 7.04 | 0.89 | 49.36 |
| Locked studies | Solid yield | 5 | A · literature only | 18 | 13.44 | 11.96 | 0.85 | 45.2 |
| Locked studies | Solid yield | 5 | B · STRATA (literature + local runs) | 18 | 6.94 | 6.31 | 0.86 | 34.24 |
| Locked studies | Solid yield | 5 | C · local runs only | 18 | 8.08 | 6.96 | 0.9 | 42.84 |
| External 4TU (independent) | Solid yield | 0 | A · literature only | 14 | 11.58 | 10.1 | 0.96 | 45.13 |
| External 4TU (independent) | Solid yield | 1 | A · literature only | 14 | 11.58 | 10.1 | 0.96 | 45.13 |
| External 4TU (independent) | Solid yield | 1 | B · STRATA (literature + local runs) | 14 | 9.44 | 7.94 | 0.95 | 37.42 |
| External 4TU (independent) | Solid yield | 1 | C · local runs only | 14 | 8.68 | 7.3 | 0.97 | 55.4 |
| External 4TU (independent) | Solid yield | 3 | A · literature only | 14 | 11.58 | 10.1 | 0.96 | 45.13 |
| External 4TU (independent) | Solid yield | 3 | B · STRATA (literature + local runs) | 14 | 6.26 | 5.4 | 0.94 | 36.47 |
| External 4TU (independent) | Solid yield | 3 | C · local runs only | 14 | 7.98 | 6.88 | 0.94 | 49.36 |
| External 4TU (independent) | Solid yield | 5 | A · literature only | 14 | 11.58 | 10.1 | 0.96 | 45.13 |
| External 4TU (independent) | Solid yield | 5 | B · STRATA (literature + local runs) | 14 | 6.3 | 4.66 | 0.92 | 33.16 |
| External 4TU (independent) | Solid yield | 5 | C · local runs only | 14 | 7.86 | 6.34 | 0.93 | 42.84 |




**Table S22.** Retrospective simulated deployment in the reported run order and in 20 random run orders (otherwise as in the main deployment table).

| target | order | k | strategy | median_rmse | median_mae | coverage | width | n_studies | setting |
|---|---|---|---|---|---|---|---|---|---|
| Bio-oil yield | random | 0 | A | 12.31 | 10.15 | 0.93 | 59.8 | 80 | Development (unseen studies) |
| Bio-oil yield | random | 0 | B | 12.31 | 10.15 | 0.93 | 59.8 | 80 | Development (unseen studies) |
| Bio-oil yield | random | 1 | A | 12.31 | 10.15 | 0.93 | 59.8 | 80 | Development (unseen studies) |
| Bio-oil yield | random | 1 | B | 9.63 | 8.08 | 0.92 | 44.09 | 80 | Development (unseen studies) |
| Bio-oil yield | random | 1 | C | 10.57 | 8.71 | 0.9 | 49.91 | 80 | Development (unseen studies) |
| Bio-oil yield | random | 2 | A | 12.31 | 10.15 | 0.93 | 59.8 | 80 | Development (unseen studies) |
| Bio-oil yield | random | 2 | B | 8.68 | 7.19 | 0.92 | 40.02 | 80 | Development (unseen studies) |
| Bio-oil yield | random | 2 | C | 9.34 | 7.53 | 0.9 | 42.59 | 80 | Development (unseen studies) |
| Bio-oil yield | random | 3 | A | 12.31 | 10.15 | 0.93 | 59.8 | 80 | Development (unseen studies) |
| Bio-oil yield | random | 3 | B | 8.4 | 6.89 | 0.92 | 38.3 | 80 | Development (unseen studies) |
| Bio-oil yield | random | 3 | C | 8.84 | 7.36 | 0.9 | 39.95 | 80 | Development (unseen studies) |
| Bio-oil yield | random | 5 | A | 12.31 | 10.15 | 0.93 | 59.8 | 80 | Development (unseen studies) |
| Bio-oil yield | random | 5 | B | 8.07 | 6.5 | 0.92 | 36.68 | 80 | Development (unseen studies) |
| Bio-oil yield | random | 5 | C | 8.63 | 7.23 | 0.9 | 38.1 | 80 | Development (unseen studies) |
| Bio-oil yield | reported order | 0 | A | 12.02 | 10.21 | 0.93 | 59.02 | 80 | Development (unseen studies) |
| Bio-oil yield | reported order | 0 | B | 12.02 | 10.21 | 0.93 | 59.02 | 80 | Development (unseen studies) |
| Bio-oil yield | reported order | 1 | A | 12.02 | 10.21 | 0.93 | 59.02 | 80 | Development (unseen studies) |
| Bio-oil yield | reported order | 1 | B | 9.48 | 7.73 | 0.93 | 47.05 | 80 | Development (unseen studies) |
| Bio-oil yield | reported order | 1 | C | 11.84 | 10.18 | 0.91 | 51.02 | 80 | Development (unseen studies) |
| Bio-oil yield | reported order | 2 | A | 12.02 | 10.21 | 0.93 | 59.02 | 80 | Development (unseen studies) |
| Bio-oil yield | reported order | 2 | B | 8.98 | 7.28 | 0.92 | 44.7 | 80 | Development (unseen studies) |
| Bio-oil yield | reported order | 2 | C | 11.4 | 9.68 | 0.91 | 50.34 | 80 | Development (unseen studies) |
| Bio-oil yield | reported order | 3 | A | 12.02 | 10.21 | 0.93 | 59.02 | 80 | Development (unseen studies) |
| Bio-oil yield | reported order | 3 | B | 9.21 | 7.7 | 0.92 | 44.54 | 80 | Development (unseen studies) |
| Bio-oil yield | reported order | 3 | C | 10.99 | 9.51 | 0.9 | 49.64 | 80 | Development (unseen studies) |
| Bio-oil yield | reported order | 5 | A | 12.02 | 10.21 | 0.93 | 59.02 | 80 | Development (unseen studies) |
| Bio-oil yield | reported order | 5 | B | 8.29 | 6.83 | 0.92 | 40.78 | 80 | Development (unseen studies) |
| Bio-oil yield | reported order | 5 | C | 10.27 | 8.69 | 0.9 | 44.55 | 80 | Development (unseen studies) |
| Solid yield | random | 0 | A | 10.94 | 8.85 | 0.91 | 48.07 | 72 | Development (unseen studies) |
| Solid yield | random | 0 | B | 10.94 | 8.85 | 0.91 | 48.07 | 72 | Development (unseen studies) |
| Solid yield | random | 1 | A | 10.94 | 8.85 | 0.91 | 48.07 | 72 | Development (unseen studies) |
| Solid yield | random | 1 | B | 8.93 | 7.32 | 0.9 | 38.79 | 72 | Development (unseen studies) |
| Solid yield | random | 1 | C | 12.02 | 9.84 | 0.89 | 52.46 | 72 | Development (unseen studies) |
| Solid yield | random | 2 | A | 10.94 | 8.85 | 0.91 | 48.07 | 72 | Development (unseen studies) |
| Solid yield | random | 2 | B | 8.18 | 6.63 | 0.9 | 35.81 | 72 | Development (unseen studies) |
| Solid yield | random | 2 | C | 10.54 | 8.46 | 0.89 | 45.02 | 72 | Development (unseen studies) |
| Solid yield | random | 3 | A | 10.94 | 8.85 | 0.91 | 48.07 | 72 | Development (unseen studies) |
| Solid yield | random | 3 | B | 8.08 | 6.43 | 0.9 | 34.35 | 72 | Development (unseen studies) |
| Solid yield | random | 3 | C | 10.21 | 7.95 | 0.89 | 42.18 | 72 | Development (unseen studies) |
| Solid yield | random | 5 | A | 10.94 | 8.85 | 0.91 | 48.07 | 72 | Development (unseen studies) |
| Solid yield | random | 5 | B | 7.53 | 6.14 | 0.89 | 33.18 | 72 | Development (unseen studies) |
| Solid yield | random | 5 | C | 9.49 | 7.42 | 0.89 | 39.55 | 72 | Development (unseen studies) |
| Solid yield | reported order | 0 | A | 10.98 | 8.89 | 0.89 | 46.54 | 72 | Development (unseen studies) |
| Solid yield | reported order | 0 | B | 10.98 | 8.89 | 0.89 | 46.54 | 72 | Development (unseen studies) |
| Solid yield | reported order | 1 | A | 10.98 | 8.89 | 0.89 | 46.54 | 72 | Development (unseen studies) |
| Solid yield | reported order | 1 | B | 10.06 | 8.76 | 0.89 | 40.81 | 72 | Development (unseen studies) |
| Solid yield | reported order | 1 | C | 16.4 | 14.49 | 0.89 | 71.4 | 72 | Development (unseen studies) |
| Solid yield | reported order | 2 | A | 10.98 | 8.89 | 0.89 | 46.54 | 72 | Development (unseen studies) |
| Solid yield | reported order | 2 | B | 9.29 | 8.12 | 0.9 | 41.57 | 72 | Development (unseen studies) |
| Solid yield | reported order | 2 | C | 15.0 | 13.32 | 0.89 | 64.64 | 72 | Development (unseen studies) |
| Solid yield | reported order | 3 | A | 10.98 | 8.89 | 0.89 | 46.54 | 72 | Development (unseen studies) |
| Solid yield | reported order | 3 | B | 9.17 | 7.92 | 0.89 | 40.89 | 72 | Development (unseen studies) |
| Solid yield | reported order | 3 | C | 14.53 | 12.22 | 0.89 | 61.23 | 72 | Development (unseen studies) |
| Solid yield | reported order | 5 | A | 10.98 | 8.89 | 0.89 | 46.54 | 72 | Development (unseen studies) |
| Solid yield | reported order | 5 | B | 8.45 | 7.54 | 0.88 | 39.06 | 72 | Development (unseen studies) |
| Solid yield | reported order | 5 | C | 11.07 | 9.61 | 0.87 | 55.08 | 72 | Development (unseen studies) |
| Bio-oil yield | random | 0 | A | 10.83 | 9.12 | 0.88 | 58.34 | 19 | Locked studies |
| Bio-oil yield | random | 0 | B | 10.83 | 9.12 | 0.88 | 58.34 | 19 | Locked studies |
| Bio-oil yield | random | 1 | A | 10.83 | 9.12 | 0.88 | 58.34 | 19 | Locked studies |
| Bio-oil yield | random | 1 | B | 9.07 | 7.6 | 0.91 | 41.48 | 19 | Locked studies |
| Bio-oil yield | random | 1 | C | 8.94 | 7.38 | 0.97 | 49.61 | 19 | Locked studies |
| Bio-oil yield | random | 2 | A | 10.83 | 9.12 | 0.88 | 58.34 | 19 | Locked studies |
| Bio-oil yield | random | 2 | B | 8.53 | 7.1 | 0.93 | 38.1 | 19 | Locked studies |
| Bio-oil yield | random | 2 | C | 7.39 | 6.15 | 0.97 | 43.0 | 19 | Locked studies |
| Bio-oil yield | random | 3 | A | 10.83 | 9.12 | 0.88 | 58.34 | 19 | Locked studies |
| Bio-oil yield | random | 3 | B | 7.76 | 6.58 | 0.93 | 36.74 | 19 | Locked studies |
| Bio-oil yield | random | 3 | C | 7.16 | 5.96 | 0.98 | 40.43 | 19 | Locked studies |
| Bio-oil yield | random | 5 | A | 10.83 | 9.12 | 0.88 | 58.34 | 19 | Locked studies |
| Bio-oil yield | random | 5 | B | 7.61 | 6.25 | 0.94 | 35.37 | 19 | Locked studies |
| Bio-oil yield | random | 5 | C | 6.84 | 5.51 | 0.97 | 38.2 | 19 | Locked studies |
| Bio-oil yield | reported order | 0 | A | 10.3 | 8.44 | 0.91 | 58.02 | 19 | Locked studies |
| Bio-oil yield | reported order | 0 | B | 10.3 | 8.44 | 0.91 | 58.02 | 19 | Locked studies |
| Bio-oil yield | reported order | 1 | A | 10.3 | 8.44 | 0.91 | 58.02 | 19 | Locked studies |
| Bio-oil yield | reported order | 1 | B | 11.21 | 10.06 | 0.89 | 45.62 | 19 | Locked studies |
| Bio-oil yield | reported order | 1 | C | 10.78 | 9.22 | 0.94 | 51.0 | 19 | Locked studies |
| Bio-oil yield | reported order | 2 | A | 10.3 | 8.44 | 0.91 | 58.02 | 19 | Locked studies |
| Bio-oil yield | reported order | 2 | B | 10.09 | 7.8 | 0.88 | 42.32 | 19 | Locked studies |
| Bio-oil yield | reported order | 2 | C | 11.05 | 8.78 | 0.94 | 50.61 | 19 | Locked studies |
| Bio-oil yield | reported order | 3 | A | 10.3 | 8.44 | 0.91 | 58.02 | 19 | Locked studies |
| Bio-oil yield | reported order | 3 | B | 10.08 | 7.82 | 0.94 | 42.79 | 19 | Locked studies |
| Bio-oil yield | reported order | 3 | C | 9.63 | 8.39 | 0.99 | 49.33 | 19 | Locked studies |
| Bio-oil yield | reported order | 5 | A | 10.3 | 8.44 | 0.91 | 58.02 | 19 | Locked studies |
| Bio-oil yield | reported order | 5 | B | 10.33 | 8.83 | 0.91 | 40.0 | 19 | Locked studies |
| Bio-oil yield | reported order | 5 | C | 8.75 | 7.57 | 0.98 | 44.36 | 19 | Locked studies |
| Solid yield | random | 0 | A | 14.03 | 12.68 | 0.85 | 47.52 | 18 | Locked studies |
| Solid yield | random | 0 | B | 14.03 | 12.68 | 0.85 | 47.52 | 18 | Locked studies |
| Solid yield | random | 1 | A | 14.03 | 12.68 | 0.85 | 47.52 | 18 | Locked studies |
| Solid yield | random | 1 | B | 8.76 | 8.16 | 0.87 | 38.38 | 18 | Locked studies |
| Solid yield | random | 1 | C | 9.68 | 7.7 | 0.9 | 52.6 | 18 | Locked studies |
| Solid yield | random | 2 | A | 14.03 | 12.68 | 0.85 | 47.52 | 18 | Locked studies |
| Solid yield | random | 2 | B | 7.28 | 6.18 | 0.88 | 35.68 | 18 | Locked studies |
| Solid yield | random | 2 | C | 8.61 | 6.58 | 0.9 | 44.95 | 18 | Locked studies |
| Solid yield | random | 3 | A | 14.03 | 12.68 | 0.85 | 47.52 | 18 | Locked studies |
| Solid yield | random | 3 | B | 7.16 | 5.83 | 0.89 | 34.25 | 18 | Locked studies |
| Solid yield | random | 3 | C | 8.08 | 6.39 | 0.91 | 41.66 | 18 | Locked studies |
| Solid yield | random | 5 | A | 14.03 | 12.68 | 0.85 | 47.52 | 18 | Locked studies |
| Solid yield | random | 5 | B | 7.0 | 5.68 | 0.89 | 32.86 | 18 | Locked studies |
| Solid yield | random | 5 | C | 7.66 | 6.08 | 0.91 | 39.23 | 18 | Locked studies |
| Solid yield | reported order | 0 | A | 14.97 | 13.34 | 0.85 | 46.0 | 18 | Locked studies |
| Solid yield | reported order | 0 | B | 14.97 | 13.34 | 0.85 | 46.0 | 18 | Locked studies |
| Solid yield | reported order | 1 | A | 14.97 | 13.34 | 0.85 | 46.0 | 18 | Locked studies |
| Solid yield | reported order | 1 | B | 8.72 | 7.83 | 0.84 | 39.43 | 18 | Locked studies |
| Solid yield | reported order | 1 | C | 11.32 | 9.79 | 0.88 | 70.94 | 18 | Locked studies |
| Solid yield | reported order | 2 | A | 14.97 | 13.34 | 0.85 | 46.0 | 18 | Locked studies |
| Solid yield | reported order | 2 | B | 7.96 | 7.24 | 0.87 | 41.7 | 18 | Locked studies |
| Solid yield | reported order | 2 | C | 10.97 | 9.75 | 0.92 | 64.6 | 18 | Locked studies |
| Solid yield | reported order | 3 | A | 14.97 | 13.34 | 0.85 | 46.0 | 18 | Locked studies |
| Solid yield | reported order | 3 | B | 7.66 | 7.03 | 0.88 | 39.39 | 18 | Locked studies |
| Solid yield | reported order | 3 | C | 11.5 | 9.44 | 0.92 | 61.2 | 18 | Locked studies |
| Solid yield | reported order | 5 | A | 14.97 | 13.34 | 0.85 | 46.0 | 18 | Locked studies |
| Solid yield | reported order | 5 | B | 6.98 | 6.13 | 0.91 | 40.82 | 18 | Locked studies |
| Solid yield | reported order | 5 | C | 9.14 | 7.99 | 0.93 | 55.2 | 18 | Locked studies |
| Solid yield | random | 0 | A | 12.46 | 10.62 | 0.96 | 48.58 | 14 | External 4TU (independent) |
| Solid yield | random | 0 | B | 12.46 | 10.62 | 0.96 | 48.58 | 14 | External 4TU (independent) |
| Solid yield | random | 1 | A | 12.46 | 10.62 | 0.96 | 48.58 | 14 | External 4TU (independent) |
| Solid yield | random | 1 | B | 9.06 | 7.98 | 0.95 | 39.17 | 14 | External 4TU (independent) |
| Solid yield | random | 1 | C | 11.78 | 10.02 | 0.92 | 52.6 | 14 | External 4TU (independent) |
| Solid yield | random | 2 | A | 12.46 | 10.62 | 0.96 | 48.58 | 14 | External 4TU (independent) |
| Solid yield | random | 2 | B | 7.97 | 7.0 | 0.94 | 35.88 | 14 | External 4TU (independent) |
| Solid yield | random | 2 | C | 10.65 | 9.03 | 0.91 | 44.95 | 14 | External 4TU (independent) |
| Solid yield | random | 3 | A | 12.46 | 10.62 | 0.96 | 48.58 | 14 | External 4TU (independent) |
| Solid yield | random | 3 | B | 6.91 | 6.18 | 0.94 | 34.8 | 14 | External 4TU (independent) |
| Solid yield | random | 3 | C | 9.74 | 8.21 | 0.9 | 41.66 | 14 | External 4TU (independent) |
| Solid yield | random | 5 | A | 12.46 | 10.62 | 0.96 | 48.58 | 14 | External 4TU (independent) |
| Solid yield | random | 5 | B | 5.79 | 4.79 | 0.94 | 33.12 | 14 | External 4TU (independent) |
| Solid yield | random | 5 | C | 8.88 | 7.54 | 0.9 | 39.23 | 14 | External 4TU (independent) |
| Solid yield | reported order | 0 | A | 10.27 | 9.19 | 0.97 | 45.24 | 14 | External 4TU (independent) |
| Solid yield | reported order | 0 | B | 10.27 | 9.19 | 0.97 | 45.24 | 14 | External 4TU (independent) |
| Solid yield | reported order | 1 | A | 10.27 | 9.19 | 0.97 | 45.24 | 14 | External 4TU (independent) |
| Solid yield | reported order | 1 | B | 8.68 | 7.26 | 0.87 | 37.54 | 14 | External 4TU (independent) |
| Solid yield | reported order | 1 | C | 13.19 | 12.11 | 0.82 | 70.94 | 14 | External 4TU (independent) |
| Solid yield | reported order | 2 | A | 10.27 | 9.19 | 0.97 | 45.24 | 14 | External 4TU (independent) |
| Solid yield | reported order | 2 | B | 7.08 | 6.45 | 0.89 | 39.88 | 14 | External 4TU (independent) |
| Solid yield | reported order | 2 | C | 14.29 | 13.33 | 0.85 | 64.6 | 14 | External 4TU (independent) |
| Solid yield | reported order | 3 | A | 10.27 | 9.19 | 0.97 | 45.24 | 14 | External 4TU (independent) |
| Solid yield | reported order | 3 | B | 7.2 | 6.25 | 0.95 | 41.38 | 14 | External 4TU (independent) |
| Solid yield | reported order | 3 | C | 12.97 | 11.94 | 0.88 | 61.2 | 14 | External 4TU (independent) |
| Solid yield | reported order | 5 | A | 10.27 | 9.19 | 0.97 | 45.24 | 14 | External 4TU (independent) |
| Solid yield | reported order | 5 | B | 5.6 | 4.34 | 0.96 | 39.77 | 14 | External 4TU (independent) |
| Solid yield | reported order | 5 | C | 10.9 | 9.71 | 0.94 | 55.2 | 14 | External 4TU (independent) |




**Table S23.** Paired comparisons of per-study RMSE (Wilcoxon signed-rank, two-sided; Holm correction within each setting × target × run order). Negative median differences favour B (STRATA).

| setting | target | order | k | comparison | n | p | median_diff | ci_low | ci_high | rank_biserial | p_holm |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Development (unseen studies) | Bio-oil yield | screening design | 1 | B_vs_A | 80 | 0.0 | -1.7537 | -2.7973 | -0.5346 | -0.5407 | 0.0001 |
| Development (unseen studies) | Bio-oil yield | screening design | 1 | B_vs_C | 80 | 0.0037 | -1.1983 | -2.0097 | -0.5559 | -0.3741 | 0.011 |
| Development (unseen studies) | Bio-oil yield | screening design | 2 | B_vs_A | 80 | 0.0 | -1.2347 | -3.099 | -0.6298 | -0.5907 | 0.0 |
| Development (unseen studies) | Bio-oil yield | screening design | 2 | B_vs_C | 80 | 0.0024 | -1.1204 | -1.9668 | -0.0271 | -0.3914 | 0.0094 |
| Development (unseen studies) | Bio-oil yield | screening design | 3 | B_vs_A | 80 | 0.0 | -2.2296 | -3.474 | -1.0023 | -0.6895 | 0.0 |
| Development (unseen studies) | Bio-oil yield | screening design | 3 | B_vs_C | 80 | 0.0163 | -0.7459 | -1.5018 | 0.3199 | -0.3093 | 0.0325 |
| Development (unseen studies) | Bio-oil yield | screening design | 5 | B_vs_A | 80 | 0.0 | -2.4939 | -4.1855 | -1.2134 | -0.721 | 0.0 |
| Development (unseen studies) | Bio-oil yield | screening design | 5 | B_vs_C | 80 | 0.0178 | -0.4903 | -1.1358 | 0.2276 | -0.3049 | 0.0325 |
| Development (unseen studies) | Bio-oil yield | random | 1 | B_vs_A | 80 | 0.0 | -1.4737 | -2.345 | -0.4793 | -0.6167 | 0.0 |
| Development (unseen studies) | Bio-oil yield | random | 1 | B_vs_C | 80 | 0.0019 | -1.6687 | -2.4004 | -0.8429 | -0.3994 | 0.0077 |
| Development (unseen studies) | Bio-oil yield | random | 2 | B_vs_A | 80 | 0.0 | -2.077 | -3.0585 | -1.0268 | -0.7599 | 0.0 |
| Development (unseen studies) | Bio-oil yield | random | 2 | B_vs_C | 80 | 0.0144 | -0.6288 | -1.3816 | -0.15 | -0.3148 | 0.0433 |
| Development (unseen studies) | Bio-oil yield | random | 3 | B_vs_A | 80 | 0.0 | -2.3005 | -3.3358 | -1.237 | -0.8136 | 0.0 |
| Development (unseen studies) | Bio-oil yield | random | 3 | B_vs_C | 80 | 0.0328 | -0.3625 | -1.0622 | -0.016 | -0.2747 | 0.0656 |
| Development (unseen studies) | Bio-oil yield | random | 5 | B_vs_A | 80 | 0.0 | -2.6855 | -3.7481 | -1.328 | -0.887 | 0.0 |
| Development (unseen studies) | Bio-oil yield | random | 5 | B_vs_C | 80 | 0.042 | -0.3643 | -1.0833 | 0.0878 | -0.2617 | 0.0656 |
| Development (unseen studies) | Bio-oil yield | reported order | 1 | B_vs_A | 80 | 0.0007 | -0.8877 | -2.441 | -0.3686 | -0.4358 | 0.0014 |
| Development (unseen studies) | Bio-oil yield | reported order | 1 | B_vs_C | 80 | 0.0004 | -1.8851 | -2.9702 | -0.7041 | -0.4525 | 0.0013 |
| Development (unseen studies) | Bio-oil yield | reported order | 2 | B_vs_A | 80 | 0.0 | -1.2632 | -3.1476 | -0.5414 | -0.5667 | 0.0001 |
| Development (unseen studies) | Bio-oil yield | reported order | 2 | B_vs_C | 80 | 0.0001 | -1.3868 | -2.3921 | -0.5498 | -0.5086 | 0.0004 |
| Development (unseen studies) | Bio-oil yield | reported order | 3 | B_vs_A | 80 | 0.0 | -1.7816 | -3.1425 | -0.6105 | -0.5531 | 0.0001 |
| Development (unseen studies) | Bio-oil yield | reported order | 3 | B_vs_C | 80 | 0.0002 | -0.7402 | -1.5425 | -0.5262 | -0.4728 | 0.001 |
| Development (unseen studies) | Bio-oil yield | reported order | 5 | B_vs_A | 80 | 0.0 | -1.6848 | -3.4663 | -0.5333 | -0.6062 | 0.0 |
| Development (unseen studies) | Bio-oil yield | reported order | 5 | B_vs_C | 80 | 0.0132 | -0.4775 | -1.6951 | 0.2051 | -0.3191 | 0.0132 |
| Development (unseen studies) | Solid yield | screening design | 1 | B_vs_A | 72 | 0.0018 | -0.7931 | -1.8498 | -0.0692 | -0.4224 | 0.0018 |
| Development (unseen studies) | Solid yield | screening design | 1 | B_vs_C | 72 | 0.0 | -2.4791 | -4.027 | -1.3612 | -0.6263 | 0.0 |
| Development (unseen studies) | Solid yield | screening design | 2 | B_vs_A | 72 | 0.0008 | -0.9305 | -2.0498 | -0.2 | -0.4559 | 0.0016 |
| Development (unseen studies) | Solid yield | screening design | 2 | B_vs_C | 72 | 0.0 | -4.4331 | -6.0009 | -2.8436 | -0.691 | 0.0 |
| Development (unseen studies) | Solid yield | screening design | 3 | B_vs_A | 72 | 0.0 | -1.1155 | -2.2542 | -0.4118 | -0.5548 | 0.0001 |
| Development (unseen studies) | Solid yield | screening design | 3 | B_vs_C | 72 | 0.0 | -2.2904 | -3.5826 | -1.3049 | -0.586 | 0.0001 |
| Development (unseen studies) | Solid yield | screening design | 5 | B_vs_A | 72 | 0.0 | -1.1111 | -2.4022 | -0.3086 | -0.5807 | 0.0001 |
| Development (unseen studies) | Solid yield | screening design | 5 | B_vs_C | 72 | 0.0 | -1.5768 | -2.7437 | -1.0505 | -0.5594 | 0.0001 |
| Development (unseen studies) | Solid yield | random | 1 | B_vs_A | 72 | 0.0005 | -0.6454 | -1.3289 | 0.0667 | -0.4718 | 0.0005 |
| Development (unseen studies) | Solid yield | random | 1 | B_vs_C | 72 | 0.0 | -3.4982 | -4.4601 | -1.9805 | -0.6674 | 0.0 |
| Development (unseen studies) | Solid yield | random | 2 | B_vs_A | 72 | 0.0 | -1.0589 | -2.0119 | -0.2671 | -0.6035 | 0.0 |
| Development (unseen studies) | Solid yield | random | 2 | B_vs_C | 72 | 0.0 | -2.1596 | -3.4745 | -1.273 | -0.6043 | 0.0 |
| Development (unseen studies) | Solid yield | random | 3 | B_vs_A | 72 | 0.0 | -1.1953 | -2.2789 | -0.3875 | -0.6644 | 0.0 |
| Development (unseen studies) | Solid yield | random | 3 | B_vs_C | 72 | 0.0 | -1.8475 | -2.8898 | -1.0671 | -0.5936 | 0.0 |
| Development (unseen studies) | Solid yield | random | 5 | B_vs_A | 72 | 0.0 | -1.4042 | -2.4733 | -0.4773 | -0.7344 | 0.0 |
| Development (unseen studies) | Solid yield | random | 5 | B_vs_C | 72 | 0.0 | -1.6904 | -2.6584 | -0.8001 | -0.5921 | 0.0 |
| Development (unseen studies) | Solid yield | reported order | 1 | B_vs_A | 72 | 0.0184 | -0.5926 | -1.2449 | 0.0266 | -0.3196 | 0.0553 |
| Development (unseen studies) | Solid yield | reported order | 1 | B_vs_C | 72 | 0.0 | -5.9579 | -10.7026 | -3.4262 | -0.7184 | 0.0 |
| Development (unseen studies) | Solid yield | reported order | 2 | B_vs_A | 72 | 0.0368 | -0.5227 | -1.1874 | -0.0464 | -0.2831 | 0.0717 |
| Development (unseen studies) | Solid yield | reported order | 2 | B_vs_C | 72 | 0.0 | -5.7945 | -8.6135 | -3.2974 | -0.7511 | 0.0 |
| Development (unseen studies) | Solid yield | reported order | 3 | B_vs_A | 72 | 0.0133 | -0.5928 | -1.285 | -0.0784 | -0.3356 | 0.0533 |
| Development (unseen studies) | Solid yield | reported order | 3 | B_vs_C | 72 | 0.0 | -5.6958 | -6.9833 | -3.0411 | -0.71 | 0.0 |
| Development (unseen studies) | Solid yield | reported order | 5 | B_vs_A | 72 | 0.0358 | -0.5335 | -1.4133 | 0.2545 | -0.2846 | 0.0717 |
| Development (unseen studies) | Solid yield | reported order | 5 | B_vs_C | 72 | 0.0 | -3.861 | -4.8125 | -2.8741 | -0.6104 | 0.0 |
| Locked studies | Bio-oil yield | screening design | 1 | B_vs_A | 19 | 0.023 | -1.453 | -9.6862 | 0.3541 | -0.5895 | 0.1225 |
| Locked studies | Bio-oil yield | screening design | 1 | B_vs_C | 19 | 0.0204 | 1.3765 | 0.6951 | 2.9864 | 0.6 | 0.1225 |
| Locked studies | Bio-oil yield | screening design | 2 | B_vs_A | 19 | 0.2253 | -0.5157 | -9.8405 | 1.0498 | -0.3263 | 0.2253 |
| Locked studies | Bio-oil yield | screening design | 2 | B_vs_C | 19 | 0.0014 | 2.0474 | 0.7026 | 3.6133 | 0.7895 | 0.0099 |
| Locked studies | Bio-oil yield | screening design | 3 | B_vs_A | 19 | 0.0663 | -0.7218 | -11.6598 | -0.0175 | -0.4842 | 0.1326 |
| Locked studies | Bio-oil yield | screening design | 3 | B_vs_C | 19 | 0.0012 | 1.3522 | 0.3647 | 2.9325 | 0.8 | 0.0094 |
| Locked studies | Bio-oil yield | screening design | 5 | B_vs_A | 19 | 0.0204 | -2.8788 | -11.5308 | -0.4145 | -0.6 | 0.1225 |
| Locked studies | Bio-oil yield | screening design | 5 | B_vs_C | 19 | 0.0401 | 1.205 | -0.1727 | 1.6249 | 0.5368 | 0.1225 |
| Locked studies | Bio-oil yield | random | 1 | B_vs_A | 19 | 0.0204 | -1.2253 | -8.9501 | 0.0516 | -0.6 | 0.0371 |
| Locked studies | Bio-oil yield | random | 1 | B_vs_C | 19 | 0.0124 | 1.2297 | 0.0406 | 3.4174 | 0.6421 | 0.0371 |
| Locked studies | Bio-oil yield | random | 2 | B_vs_A | 19 | 0.016 | -1.7421 | -9.9864 | 0.0425 | -0.6211 | 0.0371 |
| Locked studies | Bio-oil yield | random | 2 | B_vs_C | 19 | 0.001 | 1.7794 | 0.3594 | 2.4118 | 0.8105 | 0.0058 |
| Locked studies | Bio-oil yield | random | 3 | B_vs_A | 19 | 0.0014 | -1.8233 | -10.4929 | -0.2019 | -0.7895 | 0.0059 |
| Locked studies | Bio-oil yield | random | 3 | B_vs_C | 19 | 0.0012 | 1.7095 | 0.7078 | 2.3705 | 0.8 | 0.0059 |
| Locked studies | Bio-oil yield | random | 5 | B_vs_A | 19 | 0.0003 | -1.8585 | -10.2223 | -0.2432 | -0.8632 | 0.0027 |
| Locked studies | Bio-oil yield | random | 5 | B_vs_C | 19 | 0.0008 | 1.6583 | 0.72 | 2.3728 | 0.8211 | 0.0055 |
| Locked studies | Bio-oil yield | reported order | 1 | B_vs_A | 19 | 0.7381 | -0.2749 | -4.4124 | 2.1957 | -0.0947 | 1.0 |
| Locked studies | Bio-oil yield | reported order | 1 | B_vs_C | 19 | 0.1232 | 0.8463 | -0.0833 | 2.6489 | 0.4105 | 0.7391 |
| Locked studies | Bio-oil yield | reported order | 2 | B_vs_A | 19 | 0.6507 | -0.2139 | -5.6521 | 2.2831 | -0.1263 | 1.0 |
| Locked studies | Bio-oil yield | reported order | 2 | B_vs_C | 19 | 0.1336 | 1.8555 | -1.1573 | 3.8671 | 0.4 | 0.7391 |
| Locked studies | Bio-oil yield | reported order | 3 | B_vs_A | 19 | 0.418 | -0.1559 | -5.7468 | 1.274 | -0.2211 | 1.0 |
| Locked studies | Bio-oil yield | reported order | 3 | B_vs_C | 19 | 0.0799 | 1.5181 | -0.7328 | 3.7338 | 0.4632 | 0.5591 |
| Locked studies | Bio-oil yield | reported order | 5 | B_vs_A | 19 | 0.1956 | -1.3454 | -4.3909 | 0.6734 | -0.3474 | 0.7825 |
| Locked studies | Bio-oil yield | reported order | 5 | B_vs_C | 19 | 0.0108 | 1.3841 | 0.272 | 3.1549 | 0.6526 | 0.0866 |
| Locked studies | Solid yield | screening design | 1 | B_vs_A | 18 | 0.0077 | -3.7481 | -6.5514 | -1.2681 | -0.6959 | 0.0461 |
| Locked studies | Solid yield | screening design | 1 | B_vs_C | 18 | 0.3927 | -2.2467 | -3.2046 | 2.4203 | -0.2398 | 1.0 |
| Locked studies | Solid yield | screening design | 2 | B_vs_A | 18 | 0.0104 | -3.7798 | -7.9843 | -1.8638 | -0.6725 | 0.052 |
| Locked studies | Solid yield | screening design | 2 | B_vs_C | 18 | 0.2645 | -1.084 | -2.8238 | 1.4844 | -0.3099 | 1.0 |
| Locked studies | Solid yield | screening design | 3 | B_vs_A | 18 | 0.0019 | -3.752 | -8.9156 | -1.8115 | -0.7895 | 0.0135 |
| Locked studies | Solid yield | screening design | 3 | B_vs_C | 18 | 0.2645 | -1.0555 | -3.7799 | 0.5884 | -0.3099 | 1.0 |
| Locked studies | Solid yield | screening design | 5 | B_vs_A | 18 | 0.001 | -4.7536 | -11.1988 | -1.9408 | -0.8246 | 0.0084 |
| Locked studies | Solid yield | screening design | 5 | B_vs_C | 18 | 0.4423 | -0.9177 | -2.4325 | 0.4376 | -0.2164 | 1.0 |
| Locked studies | Solid yield | random | 1 | B_vs_A | 18 | 0.0004 | -2.9916 | -6.4203 | -1.7241 | -0.8713 | 0.0021 |
| Locked studies | Solid yield | random | 1 | B_vs_C | 18 | 0.5226 | -0.6738 | -2.6428 | 2.3672 | -0.1813 | 0.6694 |
| Locked studies | Solid yield | random | 2 | B_vs_A | 18 | 0.0003 | -3.8037 | -8.8725 | -1.8582 | -0.883 | 0.002 |
| Locked studies | Solid yield | random | 2 | B_vs_C | 18 | 0.2837 | -1.0956 | -2.1766 | 0.9466 | -0.2982 | 0.6694 |
| Locked studies | Solid yield | random | 3 | B_vs_A | 18 | 0.0002 | -4.1617 | -9.6501 | -2.2382 | -0.9064 | 0.0015 |
| Locked studies | Solid yield | random | 3 | B_vs_C | 18 | 0.2121 | -1.2138 | -2.3993 | 0.4573 | -0.345 | 0.6694 |
| Locked studies | Solid yield | random | 5 | B_vs_A | 18 | 0.0002 | -4.5257 | -10.5102 | -2.5421 | -0.9064 | 0.0015 |
| Locked studies | Solid yield | random | 5 | B_vs_C | 18 | 0.1674 | -0.8927 | -2.3336 | 0.2437 | -0.3801 | 0.6694 |
| Locked studies | Solid yield | reported order | 1 | B_vs_A | 18 | 0.0056 | -3.824 | -6.3238 | -0.9158 | -0.7193 | 0.028 |
| Locked studies | Solid yield | reported order | 1 | B_vs_C | 18 | 0.3692 | -0.603 | -3.2847 | 1.209 | -0.2515 | 0.3692 |
| Locked studies | Solid yield | reported order | 2 | B_vs_A | 18 | 0.0028 | -4.3943 | -8.5184 | -0.7254 | -0.7661 | 0.0197 |
| Locked studies | Solid yield | reported order | 2 | B_vs_C | 18 | 0.0898 | -1.1476 | -4.6714 | 0.2293 | -0.462 | 0.2443 |
| Locked studies | Solid yield | reported order | 3 | B_vs_A | 18 | 0.0028 | -4.1302 | -9.5881 | -0.6894 | -0.7661 | 0.0197 |
| Locked studies | Solid yield | reported order | 3 | B_vs_C | 18 | 0.0304 | -1.852 | -4.3708 | 0.1141 | -0.5789 | 0.1215 |
| Locked studies | Solid yield | reported order | 5 | B_vs_A | 18 | 0.0008 | -4.4194 | -10.2657 | -0.6968 | -0.8363 | 0.0067 |
| Locked studies | Solid yield | reported order | 5 | B_vs_C | 18 | 0.0814 | -1.33 | -4.274 | 0.3964 | -0.4737 | 0.2443 |
| External 4TU (independent) | Solid yield | screening design | 1 | B_vs_A | 14 | 0.0166 | -1.4207 | -6.2424 | 0.1284 | -0.7143 | 0.0996 |
| External 4TU (independent) | Solid yield | screening design | 1 | B_vs_C | 14 | 0.1937 | -1.691 | -4.6713 | 1.865 | -0.4095 | 0.2378 |
| External 4TU (independent) | Solid yield | screening design | 2 | B_vs_A | 14 | 0.1189 | -1.2038 | -7.0176 | 0.4719 | -0.4857 | 0.2378 |
| External 4TU (independent) | Solid yield | screening design | 2 | B_vs_C | 14 | 0.0052 | -3.1002 | -8.3318 | -1.4652 | -0.8095 | 0.042 |
| External 4TU (independent) | Solid yield | screening design | 3 | B_vs_A | 14 | 0.0166 | -1.1113 | -7.1545 | -0.1437 | -0.7143 | 0.0996 |
| External 4TU (independent) | Solid yield | screening design | 3 | B_vs_C | 14 | 0.0166 | -1.5956 | -4.6917 | -0.0777 | -0.7143 | 0.0996 |
| External 4TU (independent) | Solid yield | screening design | 5 | B_vs_A | 14 | 0.0134 | -2.2392 | -8.2892 | -0.2303 | -0.7333 | 0.094 |
| External 4TU (independent) | Solid yield | screening design | 5 | B_vs_C | 14 | 0.0245 | -3.0996 | -4.7732 | -0.4558 | -0.6762 | 0.0996 |
| External 4TU (independent) | Solid yield | random | 1 | B_vs_A | 14 | 0.0295 | -0.8112 | -5.8425 | -0.054 | -0.6571 | 0.0811 |
| External 4TU (independent) | Solid yield | random | 1 | B_vs_C | 14 | 0.0203 | -4.2605 | -5.7819 | -1.1339 | -0.6952 | 0.0811 |
| External 4TU (independent) | Solid yield | random | 2 | B_vs_A | 14 | 0.0419 | -1.316 | -7.0115 | -0.1869 | -0.619 | 0.0811 |
| External 4TU (independent) | Solid yield | random | 2 | B_vs_C | 14 | 0.0067 | -3.9735 | -4.9112 | -1.6592 | -0.7905 | 0.0403 |
| External 4TU (independent) | Solid yield | random | 3 | B_vs_A | 14 | 0.0245 | -1.4023 | -7.2402 | -0.487 | -0.6762 | 0.0811 |
| External 4TU (independent) | Solid yield | random | 3 | B_vs_C | 14 | 0.0067 | -3.6731 | -4.9889 | -1.8633 | -0.7905 | 0.0403 |
| External 4TU (independent) | Solid yield | random | 5 | B_vs_A | 14 | 0.004 | -1.6917 | -7.5662 | -0.6378 | -0.8286 | 0.0322 |
| External 4TU (independent) | Solid yield | random | 5 | B_vs_C | 14 | 0.004 | -3.3641 | -4.6508 | -1.741 | -0.8286 | 0.0322 |
| External 4TU (independent) | Solid yield | reported order | 1 | B_vs_A | 14 | 0.6698 | -0.2191 | -6.1087 | 2.3428 | -0.1429 | 1.0 |
| External 4TU (independent) | Solid yield | reported order | 1 | B_vs_C | 14 | 0.0023 | -6.735 | -18.4154 | -4.2656 | -0.8667 | 0.0116 |
| External 4TU (independent) | Solid yield | reported order | 2 | B_vs_A | 14 | 0.6257 | -0.7033 | -7.6435 | 4.2375 | -0.1619 | 1.0 |
| External 4TU (independent) | Solid yield | reported order | 2 | B_vs_C | 14 | 0.0009 | -7.9694 | -13.4816 | -3.9517 | -0.9238 | 0.006 |
| External 4TU (independent) | Solid yield | reported order | 3 | B_vs_A | 14 | 0.4263 | -1.0018 | -6.8558 | 2.0862 | -0.2571 | 1.0 |
| External 4TU (independent) | Solid yield | reported order | 3 | B_vs_C | 14 | 0.0017 | -7.9721 | -13.0393 | -3.6414 | -0.8857 | 0.0103 |
| External 4TU (independent) | Solid yield | reported order | 5 | B_vs_A | 14 | 0.1353 | -2.4399 | -8.3181 | 1.3212 | -0.4667 | 0.541 |
| External 4TU (independent) | Solid yield | reported order | 5 | B_vs_C | 14 | 0.0002 | -6.5848 | -7.7752 | -2.8107 | -0.981 | 0.002 |



# S10. Reproducibility and availability

A single command regenerates every result file, table and figure from the public data, and a second command regenerates the manuscript and this document from those files; library versions and CPU details are written to a log at run time. The code, the locked test-study list, configuration files, result files and per-run predictions are available from the corresponding author on reasonable request.


