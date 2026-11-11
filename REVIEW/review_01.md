# Review round 1 — Reviewer #1 (general, *Bioresource Technology*)

Manuscript version: first complete build (commit cff741d). Perspective: overall soundness and value to the journal's readers.

## Issues

| # | Severity | Issue | Required fix | Status |
|---|---|---|---|---|
| 1.1 | MAJOR | STRATA is called "model-agnostic", but only XGBoost was used. On the locked bio-oil studies XGBoost had a pooled RMSE (18.3 wt%) *worse than the mean predictor* (13.6 wt%). The claim and the usefulness of the base model are unsupported. | Re-run STRATA with several base learners, including the mean predictor as a "no-ML" reference; report coverage, width and *k*-shot error for each. | **Fixed** — E9 (7 learners). SC coverage 0.90–0.91 (bio-oil) and 0.89–0.92 (solids) for all learners; Supplementary Table S10; new paragraph in §3.4. |
| 1.2 | MAJOR | Does the ML model add anything over predicting the mean once honest intervals are used? The paper never asks. | Compare the width of SC intervals with the mean predictor + SC. | **Fixed** — best learner narrows SC intervals by 15 % (bio-oil) and 23 % (solids) relative to the mean; stated as "real but modest". |
| 1.3 | MAJOR | Several sentences overstated results: "RMSE roughly doubled for all flexible learners" quoted a ratio range starting at 1.02 (GPBoost); "study calibration restores coverage" although locked solids reached 0.82. | Restrict the ratio range to flexible learners; weaken headings and highlights. | **Fixed** — range now 1.52–2.61 (bio-oil); heading "largely restores"; highlight gives the measured ranges. |
| 1.4 | MODERATE | Temporal result compared base+P temporal RMSE with base-feature grouped CV (mixed feature sets). | Use the same feature set. | **Fixed** — both base features; wording now computed ("higher than"). |
| 1.5 | MODERATE | Narrative citations rendered as "Elfetni et al. (Elfetni et al., 2027)". | Add narrative citation syntax. | **Fixed** in builder (`@Key` → "Author et al. (Year)"). |
| 1.6 | MODERATE | Sensitivity analyses (τ² estimator, tuning) existed only in the supplement without being mentioned. | Summarise them in §3.5. | **Fixed** — two generated sentences. |
| 1.7 | MINOR | "R² = -0.00", "<=250 °C", lower-case sentence start, "changed from 0.90 to 0.90". | Formatting. | **Fixed**. |
| 1.8 | MINOR | The claim "three local runs reduced the median error more than any change of learner" was asserted, not computed. | Compute and state both numbers. | **Fixed** — 3.9 vs ≤0.6 wt% (bio-oil), 3.4 vs ≤1.6 wt% (solids, competitive learners). |

## Recommendation of this reviewer before fixes
Major revision. After fixes: issues 1.1–1.8 resolved; no fatal issue identified.
