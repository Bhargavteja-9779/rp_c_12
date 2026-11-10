# Pre-registered analysis protocol (written before any model was fitted)

Version 1.0 — 2026-11-10. Any later deviation is logged in §12 with date and reason.

## 1. Hypothesis
Machine-learning models trained on literature-compiled hydrothermal-conversion data (HTL, solvothermal HTL, HTC)
are evaluated almost exclusively with random row splits. Because rows are clustered within source studies,
(i) random-split metrics overstate accuracy for a *new* study, (ii) a substantial share of the out-of-study error
is a study-level offset, (iii) part of that offset is attributable to how studies operationally define and report
yields (work-up solvent, yield basis, product-fraction definitions, reactor scale), and (iv) prediction intervals
calibrated on exchangeable rows under-cover for new studies, whereas intervals calibrated at the study level
(with optional k-shot empirical-Bayes adaptation) attain nominal coverage.

## 2. Research questions → experiments
| RQ | Question | Experiment(s) | Primary metric | Pre-specified hypothesis |
|---|---|---|---|---|
| RQ1 | How optimistic are random-split estimates relative to unseen-study performance? | E1 main, E2 baselines | RMSE, R² (random 5-fold vs grouped 10-fold vs locked test) | RMSE(grouped)/RMSE(random) > 1.3 for the best model on both targets |
| RQ2 | What share of out-of-study error variance is between-study? | E-HET decomposition | τ²/(τ²+σ²_w) of out-of-study residuals (method of moments) | share > 0.4 |
| RQ3 | Do work-up/reporting descriptors reduce out-of-study error / explain study offsets? | E3 ablation (P on/off), meta-regression of study offsets | per-study RMSE (paired Wilcoxon across studies); meta-regression grouped-CV R² | P reduces median per-study RMSE (one-sided p<0.05 after Holm) |
| RQ4 | Are row-calibrated conformal intervals valid for unseen studies; does study-level calibration fix them? | E-UQ | empirical coverage of 90 % intervals on unseen studies (study-weighted), mean width | row-level coverage < 0.85; study-level coverage ∈ [0.875, 0.925] |
| RQ5 | How much do k labelled runs of a new study help, and does EB shrinkage beat the raw mean offset at small k? | E-KS (k = 0,1,2,3,5,10) | per-study RMSE of held-out runs, coverage, width | shrinkage ≤ raw mean RMSE for k ≤ 3; coverage ≥ 0.875 for all k |
| RQ6 | Robustness/generalisation | E4 robustness (feature noise, fewer training studies), E5 generalisation (leave-feedstock-family-out, temporal ≤2018→≥2019, external 4TU hydrochar DB) | RMSE, coverage | report all; no favourable selection |
| RQ7 | Cost | E6 efficiency | fit/predict time, peak memory, model size | — |
| — | Sensitivity | E7 (α ∈ {0.05,0.1,0.2}, τ² estimator, hyper-parameter budget, number of outer folds) | — | — |
| — | Error analysis | E8 (per family, process, solvent, worst studies) | — | — |

## 3. Data
* Primary: RADAR4Chem HTT/HTL v1.0.0 (doi:10.22000/8bnbhqccf4aq7kea), CC BY 4.0, sha256 `c8827a37…a42a6b`, 3,693 rows, 188 source publications (DOI).
* External: 4TU.ResearchData hydrochar database (doi:10.4121/834c3f22-f46a-4808-a0fe-46298be6a133.v1), CC BY 4.0, 543 + 27 rows, HTC only, no study identifiers.
* Unit of analysis for all inference = **source study (DOI)**.

## 4. Targets and inclusion
* T1 bio-oil (biocrude) yield, wt % — process subtypes HTL and HTL_solvothermal.
* T2 solid-product yield (char/hydrochar/solid residue), wt % — HTL, HTL_solvothermal, HTC.
* Exclusions (pre-specified): APR rows; target outside [0, 100]; yield basis on a **carbon** basis (`feed carbon`/`carbon-basis`); missing feedstock C or O; missing temperature or residence time; studies contributing < 2 rows for the target (cannot form a study offset). Exclusion counts are logged.

## 5. Features
* **Base (chemistry + conditions):** feedstock C, H, O, N, ash (wt %); lignin, cellulose, hemicellulose (as provided incl. curator imputations); temperature (°C); residence time (log1p min); solid loading (wt %); catalyst class (none / alkali carbonate / alkali hydroxide / acid / metal or supported metal / other) and catalyst:biomass ratio; reaction-medium class (water / alcohol / ketone / water–alcohol / other organic / with H-donor or co-reactant); process subtype; heating rate (if reported); H₂ or inert gas pressure flag.
* **Protocol/reporting descriptors (P):** yield basis is dry-ash-free; basis includes co-reactant/solvent mass; product defined as multiple combined fractions (light/heavy oil, WSO); aqueous/gas obtained by difference; extraction solvent class (DCM, acetone, ethyl acetate, diethyl ether, THF, alcohol, hydrocarbon, none named); reactor volume (log10 mL); separation route not stated.
* All transformations are fitted inside training folds only (imputation medians, scalers).
* `year` and DOI are **never** model features (year is used only for the temporal split).

## 6. Splits
* **Locked test**: 38 studies (20 %, seed 20261110), created before modelling (`locked_test_studies.json`). Evaluated **once**, at the end, with models trained on all development studies.
* **Development evaluation**: (a) random row-level 5-fold CV (the common literature practice; reported only to quantify optimism); (b) grouped 10-fold CV by study, repeated with seeds {11, 22, 33}.
* **Tuning**: each learner receives the same budget — 20 random hyper-parameter configurations (seed 0) scored by grouped 5-fold CV on the development set. The selected configuration is then frozen. (This makes development-CV estimates mildly optimistic *for every model equally*; the locked test is unaffected.)
* **Base learner for the proposed framework**: the learner with the lowest grouped-CV RMSE on T1 among those that support missing values natively; fixed before E3–E5.

## 7. Models (baselines)
Mean predictor; ridge regression; k-nearest neighbours; SVR (RBF); random forest; extra trees; histogram gradient boosting; LightGBM; XGBoost; CatBoost; MLP; GPBoost (boosting + study random effect; random effect set to 0 for unseen studies); TabPFN v2 if weights are obtainable and CPU inference is feasible (otherwise reported as not run). No baseline is deliberately weakened; all share preprocessing and budget.

## 8. Proposed framework (STRATA: STudy-level Reporting-Aware Transfer with cAlibrated uncertainty)
1. **P**: base learner trained on base + protocol descriptors.
2. **SC (study-level conformal)**: calibration residuals obtained out-of-study (grouped CV); interval half-width q = weighted (1−α)(1+1/m) quantile of |residuals| with each calibration study weighted equally (each row weight 1/n_j; CDF pooling of Dunn et al., 2023). Comparator **RC**: unweighted quantile of residuals from a *random-row* calibration split (current literature practice).
3. **KS (k-shot empirical-Bayes adaptation)**: with k labelled runs of the new study, offset δ̂ = k/(k+λ)·mean residual, λ = σ²_w/τ² estimated by method of moments from out-of-study residuals of the training studies. Interval quantile recomputed by simulating the k-shot procedure on calibration studies (random support sets, seed-fixed), study-weighted.
* Ablations: −P, −SC (→RC), −shrinkage (raw mean offset), −KS (k=0); pairwise combinations where meaningful.

## 9. Metrics
RMSE, MAE, R² (pooled and per study), median per-study RMSE; coverage (row-weighted and study-weighted) and mean width of 90 % intervals; interval score; fit/predict time, peak memory, serialized size.

## 10. Statistics
* Paired comparisons between methods: per-study RMSE, two-sided Wilcoxon signed-rank (one-sided only for the pre-specified directional hypotheses in §2), Holm step-down correction within each family of comparisons; effect size = matched-pairs rank-biserial correlation and median paired difference with 95 % study-cluster bootstrap CI (2,000 resamples, seed 0).
* Coverage: study-cluster bootstrap 95 % CI.
* Heterogeneity: method-of-moments (DerSimonian–Laird-type) τ², I²-style share, cluster-bootstrap CI.
* Statistical significance is claimed only where the corrected p < 0.05.

## 11. Seeds
Outer grouped-CV seeds {11, 22, 33}; learner seeds 0; bootstrap seed 0; k-shot support sampling seeds 0–19. All fixed in `config/default.yaml` before running.

## 12. Deviations log
(empty at registration)
* 2026-11-10 — TabPFN v2 (tabpfn 9.2.0) could not be run: model weights require a one-time licence acceptance with a personal Prior Labs account (`TabPFNLicenseError`). As pre-specified in §7, it is reported as "not run". No other learner was affected.
* 2026-11-10 — Clarification of §6: in E1/E2 every learner is tuned separately for each feature set (base; base+P) with the same budget, so that the P ablation is not biased by hyper-parameters tuned on one set only.
* 2026-11-10 — GPBoost note (no protocol change): with default joint estimation the study random intercept absorbs most variance (estimated σ²_study ≈ 270 vs σ²_ε ≈ 80 on bio-oil yield); for unseen studies its prediction reverts towards the fixed-effect function, which is nearly flat. Reported as observed.
