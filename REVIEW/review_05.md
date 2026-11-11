# Review round 5 — Reviewer #5 (dataset validity, generalisation, external validity)

Attempt to invalidate the central claim ("random splits overstate accuracy for new studies; SC restores coverage").

## Issues

| # | Severity | Issue | Required fix | Status |
|---|---|---|---|---|
| 5.1 | MAJOR | Literature compilations often contain the same experiment reported in two papers. Such cross-study duplicates leak information *across* study folds and could make study-grouped results optimistic — or contaminate the locked test. | Audit and re-evaluate without duplicates; count locked-test contamination. | **Fixed** — E10: 166 bio-oil (7.3 %) and 143 solid (6.6 %) development runs duplicated across studies; removing them *increases* grouped RMSE (15.8 → 16.6 wt% bio-oil; 14.1 → 14.6 wt% solids); between-study share unchanged (0.65 / 0.52); 10 bio-oil and 18 solid locked runs match development runs (2 and 1 studies). Reported in §3.6 and Limitations. |
| 5.2 | MAJOR | Single primary database curated by one group; imputed lignocellulosic fractions. | Limitation + external validation. | **Addressed** — 4TU external DB (different curators); limitation stated. External SC coverage 0.92. |
| 5.3 | MAJOR | Locked bio-oil results are dominated by one solvothermal study (54 % of squared error for XGBoost). Is the conclusion an artefact of one study? | Sensitivity excluding the top study. | **Fixed** — post-hoc sensitivity: RMSE 18.3 → 13.6 wt%, R² ≈ 0; conclusions unchanged; reported as post hoc. |
| 5.4 | MODERATE | Solid-yield SC coverage on locked studies (0.82) and for the HTC subset (0.83) is below nominal. | Report honestly; explain (rare feedstocks: technical lignin, plastic blends); weaken claims. | **Fixed** — highlight/abstract give ranges; limitation added. |
| 5.5 | MODERATE | External DB has no study IDs; pseudo-studies by identical feedstock composition may merge or split real studies. | Limitation. | Stated. |
| 5.6 | MODERATE | Temporal shift: models trained ≤2018 do worse on later studies (bio-oil 19.4 vs 15.8 wt%). Practical deployment on new research is harder than random-study CV suggests. | Report. | Reported (Table 7, §3.6). |
| 5.7 | MINOR | Yield definitions (dry vs daf basis) are mixed in the target itself. | The P-ablation tests this; noted in Limitations. | Addressed. |

Central claim survives all checks: RC under-coverage appears in every setting (dev, locked, temporal, family-out, external) and for every flexible base learner.
