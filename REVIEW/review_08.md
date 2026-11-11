# Review round 8 — Reviewer #8 (competing researcher; developed the conservation-informed HTL surrogate)

Goal: show the contribution is incremental, explained by another factor, or unfairly compared.

| # | Severity | Criticism | Response / fix | Status |
|---|---|---|---|---|
| 8.1 | MAJOR | "We already showed publication-aware heterogeneity and that five local runs halve the error." | Acknowledged explicitly in the Introduction and §3.5. Differences: (i) decomposition with CIs (τ², share 0.65/0.49); (ii) pre-registered test that recorded work-up/reporting descriptors explain offsets — negative; (iii) demonstration that *row-calibrated conformal intervals of the type both of our groups reported* under-cover new studies (0.46–0.61), with the mechanism (learner capacity, E9); (iv) shrinkage + study-calibrated *intervals* for k-shot (point recalibration alone gives no valid uncertainty); (v) locked, temporal, family and external validation; (vi) solid-yield and HTC targets. | Clarified. |
| 8.2 | MAJOR | "Your base learner violates mass closure; ours does not." | Correct; STRATA is not a surrogate. Limitation now says STRATA *could* wrap an admissible surrogate but this was **not tested** (the first draft said "can be combined"). | **Fixed** (claim weakened). |
| 8.3 | MAJOR | "Your bio-oil target mixes HTL and solvothermal HTL, whose bio-oil includes solvent-derived carbon; that inflates heterogeneity." | Partly valid. Process subtype is a feature; error analysis shows solvothermal runs have the largest errors (RMSE 18.5 wt%). A separate HTL-only analysis was **not** run; noted as limitation in this review. | Not fixed (limitation). |
| 8.4 | MODERATE | "Random-split numbers in your Table 2 are lower than what tuned models in the literature report." | Best random-split R² = 0.82 (bio-oil) is close to typical literature values (median best R² in abstracts 0.93, different data sets); tuning budget equal for all learners; no learner deliberately weakened. | Responded. |
| 8.5 | MODERATE | "Your duplicates audit shows the database has leakage-prone duplicates — is the dataset reliable?" | E10 quantifies them (≈7 %) and shows conclusions are unchanged; recommended to curators. | Addressed. |
| 8.6 | MINOR | "Your P descriptors are parsed with regular expressions — noisy." | Acknowledged as one of the two readings of the null result. | ✓ |

Conclusion of this reviewer: the paper is complementary rather than duplicative once 8.1 and 8.2 are explicit; 8.3 remains a limitation.
