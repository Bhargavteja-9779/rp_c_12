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
- Study-calibrated intervals raised coverage from 0.46–0.61 to 0.82–0.91

# Abstract

Machine-learning models of hydrothermal liquefaction (HTL) and carbonization (HTC) are trained on runs compiled from published studies but are usually validated by splitting runs at random. Using a curated database of 3,693 runs from 188 studies, with 38 studies locked away before modelling, this work quantified how such models transfer to unseen studies. Across 12 learners, the RMSE of the best bio-oil yield models rose from 7.6 wt% under random splitting to 15.7 wt% for unseen studies (R² 0.82 → 0.24); solid yields behaved similarly (7.0 → 13.7 wt%). Between-study offsets accounted for 0.65 (95% CI 0.53–0.76) of the out-of-study error variance for bio-oil and 0.49 for solids. Descriptors of product work-up and yield basis did not reduce this error. Conformal intervals calibrated on randomly held-out runs covered 0.57 (bio-oil) and 0.61 (solids) of runs from unseen studies instead of 0.90; calibrating at the study level raised coverage to 0.91 and 0.91, at the cost of 59.1- and 46.7-wt%-wide intervals. With three runs from the new study, an empirical-Bayes offset reduced the median per-study RMSE for bio-oil from 12.37 to 8.47 wt% while keeping coverage at 0.91. On 38 locked studies, study-calibrated intervals covered 0.89 (bio-oil) and 0.82 (solids) of runs, versus 0.60 and 0.46 for row-calibrated intervals, and no learner predicted bio-oil yields of new studies substantially better than the training mean. Literature-trained surrogates should therefore be validated by study, reported with study-calibrated intervals and anchored with a few local runs before use in new settings.

**Keywords:** hydrothermal liquefaction; hydrothermal carbonization; machine learning; conformal prediction; data leakage; transferability


# 1. Introduction

Hydrothermal liquefaction (HTL) and hydrothermal carbonization (HTC) convert wet lignocellulosic and residual biomass into bio-oil (biocrude), a carbon-rich solid (hydrochar or char), an aqueous phase and gas, without prior drying (Toor et al., 2011; Elliott et al., 2015; Funke and Ziegler, 2010; Libra et al., 2011). Product yields depend non-linearly on feedstock composition, temperature, residence time, solid loading, catalysts and co-solvents (Gollakota et al., 2018), and experiments are costly. Machine-learning (ML) surrogates trained on data compiled from the literature have therefore become a common tool for predicting yields and product properties and for screening operating windows (Zhang et al., 2021; Leng et al., 2022; Katongtung et al., 2024; Gungor et al., 2025; Tian et al., 2025; Djandja et al., 2027). In a systematic PubMed search of ML studies on hydrothermal conversion (2015–2026; 44 primary studies, 20 of them in *Bioresource Technology*), the median of the best coefficient of determination reported in the abstracts was 0.93 (Supplementary Table S1).

Most of these surrogates are evaluated by randomly partitioning experimental runs into training and test sets. Literature-compiled data, however, are clustered: each source publication contributes a series of runs that share the feedstock batch, reactor, analytical work-up and the authors' definition of a "yield". When runs from the same study fall on both sides of a random split, the test set no longer represents a new study, and accuracy is overstated — a form of group leakage that has been documented across ML-based science (Kapoor and Narayanan, 2023) and, recently, for biochar studies (Jang et al., 2026). For HTL specifically, Elfetni et al. (2027) curated a database of 3,693 hydrothermal experiments (Elfetni, 2026), built physically admissible four-phase surrogates, and showed that publication-aware validation exposes large inter-study heterogeneity that a few local calibration runs can partly remove. Prediction intervals have also been added to HTL surrogates (Elfetni et al., 2026; Djandja et al., 2027), but their coverage has been assessed on randomly held-out runs.

Three questions that matter for anyone applying a published surrogate to a new laboratory, feedstock or plant remain open. First, how much of the error on an unseen study is a study-level offset rather than run-to-run scatter, and can it be traced to recorded differences in how studies work up and report their products (extraction solvent, yield basis, fraction definitions, reactor scale)? Bio-oil yield is an operationally defined quantity: it depends on the solvent used to recover the oil and on the basis of the reported mass fraction (Valdez et al., 2011; Watson et al., 2019). Second, do conformal prediction intervals (Vovk et al., 2022; Lei et al., 2018; Angelopoulos and Bates, 2023), whose validity rests on exchangeability between calibration and test points, keep their nominal coverage when the test point comes from a new study? Exchangeability holds across studies, not across runs of a clustered data set (Dunn et al., 2022; Barber et al., 2023). Third, when a laboratory has measured only a handful of runs, how should these runs be combined with a literature-trained model so that both the prediction and its interval remain trustworthy?

This work addresses these questions on the largest public curated hydrothermal database (Elfetni, 2026) using a locked set of 38 source publications held out before any model was fitted, plus temporal, feedstock-family and external validation. The contributions are: (i) a benchmark of 12 learner families showing how much random-row validation overstates accuracy for new studies, for both bio-oil and solid yields; (ii) a decomposition of out-of-study error into between- and within-study variance and a test of whether work-up and reporting descriptors explain the study-level part; (iii) STRATA (STudy-level, Reporting-Aware Transfer with cAlibrated uncertainty), a model-agnostic procedure that assembles established statistical constructions — study-weighted conformal calibration for hierarchical data (Dunn et al., 2022), empirical-Bayes shrinkage of a study offset (Efron and Morris, 1975) and re-calibration by simulation over exchangeable calibration groups, as in meta-learned and small-area conformal prediction (Fisch et al., 2021; Bersson and Hoff, 2024) — into a workflow for literature-trained bioresource surrogates, and its evaluation with seven base learners, on locked, temporal, feedstock-family and external data. Physical admissibility of multi-phase predictions, already addressed by Elfetni et al. (2027), is not a contribution of this study.

# 2. Materials and methods

## 2.1. Data

The primary data were the Version 1.0.0 release of the curated hydrothermal treatment/liquefaction database (Elfetni, 2026) (CC BY 4.0; 3,693 runs from 188 source publications, 1982–2026; SHA-256 of the file verified at every load). Each run records the source DOI, feedstock ultimate, proximate and lignocellulosic composition, operating conditions, catalyst, reaction medium, the reported yield basis and separation procedure, and product yields. Two targets were modelled: bio-oil yield (HTL and solvothermal HTL runs) and solid-product yield (HTL, solvothermal HTL and HTC runs), both in wt%. Pre-specified exclusions were: aqueous-phase reforming runs; yields outside 0–100 wt%; yields reported on a carbon basis; missing feedstock C or O, temperature or residence time; and studies contributing a single run to a target (Table 1). An independent external data set — a 4TU.ResearchData hydrochar database (Abdeldayem et al., 2025) (CC BY 4.0) without study identifiers — was used only for external validation of solid yield (Section 2.6).


**Table 1.** Data used for each target after pre-specified exclusions.

| Target | Split | Runs | Studies | Median runs/study | Yield mean ± SD (wt%) | Excluded (carbon basis / missing inputs / single-run study) |
|---|---|---|---|---|---|---|
| Bio-oil | Development | 2261 | 122 | 15 | 30.8 ± 18.0 | 3 / 11 / 4 |
| Bio-oil | Locked test | 556 | 28 | 12 | 26.9 ± 13.1 | 0 / 1 / 0 |
| Solid | Development | 2156 | 120 | 13 | 33.4 ± 20.2 | 0 / 12 / 5 |
| Solid | Locked test | 457 | 30 | 12 | 40.0 ± 22.1 | 0 / 0 / 1 |



## 2.2. Locked study-level test set and leakage controls

Before any model was fitted, 20% of the source publications (38 studies, seed 20261110) were drawn at random and locked (`locked_test_studies.json`, committed to version control before the first model fit). They were evaluated once, after all modelling decisions had been frozen, with models trained on all development studies. The analysis protocol, research questions, metrics, statistical tests and seeds were registered in the repository before experiments were run; three deviations are documented in Supplementary Section S2. Leakage controls were: the unit of splitting is the source publication; DOI, title and publication year are never model inputs (year is used only to define the temporal split); all statistics-estimating preprocessing (median imputation with missing-value indicators, standardisation) is refitted inside each training fold; the external database was screened for runs that duplicate runs of the primary database (36 potential duplicates removed); and the primary database was audited for identical runs reported in more than one source study (Section 2.6, E10).

## 2.3. Features

*Base features* describe chemistry and conditions: feedstock C, H, O, N and ash; lignin, cellulose and hemicellulose; temperature; log residence time; solid loading; heating rate; catalyst class (alkali carbonate, alkali hydroxide, acid, metal/supported metal, other) and catalyst-to-biomass ratio; reaction-medium class (water, alcohol, water–alcohol, water with hydrogen donor or co-reactant, ketone, other organic); gas pre-pressurisation; and process subtype. *Protocol/reporting descriptors* (P) encode how a study defined and recovered its products, parsed deterministically from the curated yield-basis and separation fields: dry-ash-free basis; basis including co-reactant or solvent mass; product defined as several combined fractions; aqueous or gas phase obtained by difference; extraction solvent (dichloromethane, acetone, ethyl acetate, diethyl ether, tetrahydrofuran, alcohol, hydrocarbon, other chlorinated, none named); separation route not stated; and log reactor volume. Parsing rules are in `src/data/load.py` and unit-tested.

## 2.4. Learners, tuning and evaluation schemes

Twelve learners were compared: mean predictor, ridge regression, *k*-nearest neighbours, support-vector regression, multilayer perceptron, random forest (Breiman, 2001), extra trees (Geurts et al., 2006), histogram gradient boosting (Pedregosa et al., 2011), LightGBM (Ke et al., 2017), XGBoost (Chen and Guestrin, 2016), CatBoost (Prokhorenkova et al., 2018) and GPBoost, which adds a study-level random intercept to tree boosting (Sigrist, 2022). A tabular foundation model (Hollmann et al., 2025) was pre-specified but could not be run because its weights require a personal licence acceptance (Supplementary Section S2). Every learner received the same tuning budget — 20 random hyper-parameter configurations scored by study-grouped five-fold cross-validation (CV) on the development studies — separately for each feature set; the selected configuration was then frozen. Each learner was evaluated by (a) random-row five-fold CV, the prevailing practice, and (b) study-grouped ten-fold CV repeated with three pre-specified seeds, in which every development study is predicted by a model that has never seen any of its runs (Roberts et al., 2017). Metrics were RMSE, MAE and R² over all runs and the RMSE of each study.

## 2.5. STRATA

STRATA wraps any point predictor $f$. Let $r_{ij} = y_{ij} - f(\mathbf{x}_{ij})$ be the residual of run $i$ of study $j$ obtained *out of study*, i.e. from a model that did not see study $j$ (inner study-grouped five-fold CV on the training studies).

*Heterogeneity decomposition.* Residuals are modelled as $r_{ij} = u_j + \varepsilon_{ij}$ with study offset $u_j$ (variance $\tau^2$) and within-study error $\varepsilon_{ij}$ (variance $\sigma_w^2$). Both are estimated by the unbalanced one-way ANOVA method of moments (DerSimonian and Laird, 1986),
$$\hat\sigma_w^2 = \mathrm{MS}_W, \qquad \hat\tau^2 = \max\!\left(0, \frac{\mathrm{MS}_B - \mathrm{MS}_W}{n_0}\right), \qquad n_0 = \frac{N - \sum_j n_j^2 / N}{J - 1},$$
and the between-study share is $\hat\tau^2/(\hat\tau^2+\hat\sigma_w^2)$, analogous to $I^2$ in meta-analysis (Higgins and Thompson, 2002); 95% CIs are obtained by resampling studies (2,000 cluster-bootstrap replicates (Efron, 1979)). To test whether P explains study offsets, the mean out-of-study residual of each development study (base-feature model) was regressed on the study means of P by ridge regression with leave-one-study-out prediction; significance was assessed by permuting offsets across studies (1,000 permutations).

*Study-calibrated conformal intervals (SC).* For a new run the interval is $f(\mathbf{x}) \pm \hat q$, where $\hat q$ is the weighted $(1-\alpha)$ empirical quantile of $|r_{ij}|$ in which every calibration study receives the same total weight (run weight $1/n_j$), with the usual finite-sample correction. This is the CDF-pooling construction for two-layer hierarchical data of Dunn et al. (2022), under which the target of validity is a run from a new study that is exchangeable with the calibration studies; its guarantee is approximate rather than exact in finite samples, and it holds marginally over studies, not for every individual study. As in cross-validation-based conformal methods, the calibration residuals come from inner models fitted on subsets of the training studies, whereas test predictions come from the model fitted on all training studies — a standard, slightly conservative approximation. The comparator, *row-calibrated* intervals (RC), uses the unweighted quantile of residuals from random-row CV — the construction implied when conformal calibration is performed on a random split.

*k-shot empirical-Bayes adaptation (KS).* When $k$ runs of the new study have been measured, the predictions for its remaining runs are shifted by
$$\hat\delta_k = \frac{k}{k + \hat\lambda}\,\bar r_{S}, \qquad \hat\lambda = \hat\sigma_w^2 / \hat\tau^2,$$
where $\bar r_S$ is the mean residual of the $k$ support runs. This is the posterior mean of $u_j$ under a normal random-intercept model, a James–Stein-type shrinkage (Efron and Morris, 1975) that tends to the raw mean offset as $k$ grows and to zero when studies are homogeneous. The interval half-width $\hat q_k$ is re-calibrated by applying exactly this procedure to the calibration studies (20 random support sets per study) and taking the study-weighted quantile of the adjusted residuals of their query runs. The ablation compares no offset ($k=0$), the raw mean offset and the shrunk offset.

## 2.6. Experiments

E1/E2 (accuracy and baselines) applied the two evaluation schemes to all learners and both feature sets. E3 (STRATA) used the study-grouped outer folds: for each fold, inner random-row and inner study-grouped CV on the training studies produced RC and SC calibration residuals and $\hat\lambda$; the outer test studies were then predicted, and for studies with at least 11 runs the *k*-shot procedure was evaluated for $k \in \{1,2,3,5,10\}$ with 20 random support sets per study (identical studies for all $k$). The base learner for STRATA was fixed by a pre-specified rule as the native-missing-value learner with the lowest study-grouped CV RMSE on bio-oil yield (XGBoost). Robustness (E4) was assessed by adding Gaussian noise (5–20% of the training standard deviation) to continuous test features and by training on 25–100% of the training studies. Generalisation (E5) was assessed on the locked test studies, temporally (studies published up to 2018 → studies published after 2018), by leaving out one feedstock family at a time (families with ≥ 3 studies), and externally on the 4TU hydrochar database (solid yield; runs sharing an identical feedstock composition treated as one pseudo-study). E6 measured single-thread fit and prediction time, peak resident memory and serialized model size. E7 varied α (0.05, 0.10, 0.20), the $\tau^2$ estimator (method of moments vs. restricted maximum likelihood), the number of outer folds (5 vs. 10) and tuning (tuned vs. library defaults). E8 analysed out-of-study errors by feedstock family, process, extraction solvent, temperature, catalyst use and yield basis. Three further analyses were added during internal review, after the main results were known, and are reported as such: E9 repeated the STRATA evaluation with six other base learners, including the training mean as a 'no-ML' reference (development folds only); E10 audited runs that occur with identical feedstock composition, conditions and yield in more than one source study, and repeated the study-grouped evaluation without them; E11 measured the wall-clock overhead of STRATA.

## 2.7. Statistical analysis

The unit of analysis for all inference was the source study. Learners and STRATA variants were compared through per-study RMSE (averaged over seeds) with the Wilcoxon signed-rank test (Wilcoxon, 1945); families of comparisons were corrected with Holm's step-down procedure as described by Demšar (2006). Effect sizes are the median paired difference with a 95% bootstrap CI over studies and the matched-pairs rank-biserial correlation. One-sided tests were used only for directional hypotheses registered in advance (P reduces error; SC coverage exceeds RC coverage). Coverage was summarised both over runs and with equal study weights, with 95% cluster-bootstrap CIs; on development folds, point estimates average the three outer seeds and CIs were computed for the first seed. Statistical significance is claimed only for Holm-adjusted *p* < 0.05.

## 2.8. Software and reproducibility

All analyses ran on a 4-core CPU without GPU using Python 3.13, scikit-learn, LightGBM, XGBoost, CatBoost, GPBoost, statsmodels and SciPy (exact versions in `requirements.txt`). A single command (`python run_all.py --mode full`) regenerates every number, table and figure from the vendored data; a quick mode verifies the pipeline in about 15 minutes. All values reported in this article are inserted programmatically from the generated result files.


# 3. Results and discussion

## 3.1. Random splits overstate accuracy for new studies

Fig. 1 summarises the study design and Fig. 2 the data: most studies contributed between a few and a few dozen runs, a few contributed more than 100, and the source studies span four decades. Under random-row CV the gradient-boosting learners reproduced the accuracy typically reported in the literature (best bio-oil R² = 0.82, RMSE = 7.6 wt%, LightGBM; best solid-yield RMSE = 7.0 wt%) (Table 2, Fig. 3). When every study was predicted by a model that had not seen it, RMSE roughly doubled for the flexible learners (tree ensembles, boosting, k-NN, SVR, MLP): the ratio of study-grouped to random-row RMSE ranged from 1.52 to 2.61 for bio-oil (median 2.02) and from 1.50 to 2.28 for solid yield (median 1.97). The best study-grouped RMSE was 15.7 wt% for bio-oil (extra trees, R² = 0.24) and 13.7 wt% for solid yield (LightGBM, R² = 0.54), compared with 18.1 and 20.6 wt% for a model that always predicts the training mean. Ratios close to one were obtained only by learners that fit the data poorly in both schemes (mean predictor, ridge regression, GPBoost), i.e. the optimism of random splitting grows with the capacity of a learner to memorise study-specific patterns. Parity plots show that the near-diagonal agreement under random splitting is replaced by wide, partly systematic scatter for unseen studies (Fig. 10).


**Table 2.** Random-row versus study-grouped cross-validation on development studies (base features; grouped CV averaged over 3 seeds).

| Target | Learner | Random CV RMSE | Random CV R² | Grouped CV RMSE | Grouped CV R² | RMSE ratio (grouped/random) |
|---|---|---|---|---|---|---|
| Bio-oil | Extra trees | 8.64 | 0.77 | 15.73 | 0.237 | 1.82 |
| Bio-oil | SVR | 10.38 | 0.668 | 15.8 | 0.23 | 1.52 |
| Bio-oil | XGBoost | 7.81 | 0.812 | 15.8 | 0.23 | 2.02 |
| Bio-oil | Random forest | 8.45 | 0.78 | 16.01 | 0.21 | 1.89 |
| Bio-oil | LightGBM | 7.61 | 0.821 | 16.11 | 0.2 | 2.12 |
| Bio-oil | k-NN | 10.27 | 0.675 | 16.26 | 0.185 | 1.58 |
| Bio-oil | CatBoost | 7.68 | 0.818 | 16.54 | 0.156 | 2.15 |
| Bio-oil | HistGB | 7.8 | 0.812 | 16.74 | 0.136 | 2.15 |
| Bio-oil | Ridge | 15.02 | 0.304 | 17.51 | 0.054 | 1.17 |
| Bio-oil | GPBoost | 17.32 | 0.075 | 17.61 | 0.043 | 1.02 |
| Bio-oil | Mean | 18.02 | -0.001 | 18.12 | -0.013 | 1.01 |
| Bio-oil | MLP | 9.19 | 0.74 | 23.95 | -0.77 | 2.61 |
| Solid | LightGBM | 6.96 | 0.882 | 13.7 | 0.541 | 1.97 |
| Solid | XGBoost | 7.02 | 0.88 | 14.14 | 0.511 | 2.02 |
| Solid | HistGB | 7.03 | 0.879 | 14.15 | 0.511 | 2.01 |
| Solid | Random forest | 8.61 | 0.819 | 14.42 | 0.492 | 1.67 |
| Solid | CatBoost | 7.12 | 0.876 | 14.48 | 0.488 | 2.03 |
| Solid | k-NN | 9.84 | 0.764 | 14.77 | 0.467 | 1.5 |
| Solid | SVR | 9.56 | 0.777 | 15.01 | 0.45 | 1.57 |
| Solid | Extra trees | 8.23 | 0.835 | 15.07 | 0.445 | 1.83 |
| Solid | Ridge | 13.96 | 0.524 | 16.34 | 0.348 | 1.17 |
| Solid | MLP | 8.57 | 0.821 | 19.51 | 0.07 | 2.28 |
| Solid | GPBoost | 19.13 | 0.106 | 19.81 | 0.042 | 1.04 |
| Solid | Mean | 20.25 | -0.001 | 20.63 | -0.039 | 1.02 |




![**Fig. 1.** Study design. A locked set of 38 source studies is held out before modelling; all development analyses use study-grouped folds; STRATA adds study-calibrated conformal intervals and *k*-shot empirical-Bayes adaptation to any point predictor.](/home/user/rp_c_12/figures/fig01_workflow.png){width=16cm}



![**Fig. 2.** Development data. (a) Number of runs contributed per source study; (b) yield distributions; (c) publication years of all 188 source studies (dashed line: temporal split).](/home/user/rp_c_12/figures/fig02_dataset.png){width=16cm}



![**Fig. 3.** Root-mean-square error of 12 learners under random-row five-fold CV (circles) and study-grouped ten-fold CV (squares; mean of three seeds), base features.](/home/user/rp_c_12/figures/fig03_random_vs_grouped.png){width=16cm}


Among learners, differences under study-grouped CV were small relative to the gap between schemes: for bio-oil, 9 learners were not significantly worse than the best one (extra trees) after Holm correction on per-study RMSE (Supplementary Table S3), and the multilayer perceptron extrapolated poorly to unseen studies (RMSE 24.0 wt%) despite competitive random-split accuracy (9.2 wt%). GPBoost, which models a study random intercept, gained nothing for unseen studies: because feedstock descriptors are nearly constant within a study, the random intercept absorbed most of the variance and its fixed-effect component — the only part available for a new study — was nearly flat (Supplementary Section S2). This illustrates that, in literature-compiled data, study identity and feedstock chemistry are strongly confounded, which limits how much of the between-study variation any model can attribute to chemistry.

## 3.2. Most out-of-study error is a study-level offset

For the STRATA base learner (XGBoost), study offsets were large and spread on both sides of zero (Fig. 4). The between-study share of out-of-study residual variance was 0.65 (95% CI 0.53–0.76) for bio-oil and 0.49 (0.40–0.61) for solid yield; the standard deviation of study offsets ($\hat\tau$) was 12.5 and 9.7 wt%, against within-study residual standard deviations ($\hat\sigma_w$) of 9.3 and 9.9 wt% (Table 3). A model that is well calibrated on average can therefore be biased by more than 10 wt% for an individual study, and errors for runs of the same study are strongly correlated — which is why randomly held-out runs, whose study offsets were already learnt, give an optimistic picture.


![**Fig. 4.** Mean out-of-study residual (observed − predicted) of each development study with 95% intervals of the mean, STRATA base learner with base features. The annotated share is the between-study fraction of residual variance with its study-cluster bootstrap CI.](/home/user/rp_c_12/figures/fig04_study_offsets.png){width=16cm}


## 3.3. Work-up and reporting descriptors do not explain the offsets

Because bio-oil yield is operationally defined by the recovery solvent and the reporting basis (Valdez et al., 2011; Watson et al., 2019), study offsets were expected to depend on the recorded work-up. However, adding the parsed work-up and reporting descriptors (P) did not significantly reduce the error for unseen studies for either target after Holm correction. Adding the protocol descriptors changed the median per-study RMSE from 12.45 to 12.84 wt% for bio-oil (median paired difference 0.04 wt%, 95% CI -0.38 to 0.60; one-sided Wilcoxon *p* = 0.804; *n* = 122 studies) and from 10.86 to 11.05 wt% for solid yield (*p* = 0.545) (Table 3). On the locked test studies, P significantly reduced per-study RMSE for 0 and significantly increased it for 0 of the 24 learner–target combinations (Holm-corrected Wilcoxon tests). Consistently, a ridge meta-regression of the study offsets on the study-level descriptors had no out-of-study predictive value (leave-one-study-out R² = -0.031, permutation *p* = 0.714 for bio-oil; R² = -0.047, *p* = 0.910 for solids), and offsets did not differ significantly between the dominant extraction solvents (Kruskal–Wallis *p* = 0.104 for bio-oil; Kruskal–Wallis *p* = 0.951 for solids). The most negative median offset for bio-oil occurred for studies using ethyl acetate (median offset -12.7 wt%, 7 studies), but such groups are small and the differences were not significant.


**Table 3.** Decomposition of out-of-study error and contribution of work-up/reporting descriptors (P).

| Target | τ² (between) | σ²w (within) | Between-study share [95% CI] | Median study RMSE base → base+P | Δ median [95% CI]; p (one-sided) | Rank-biserial | Meta-regression LOSO R² (perm. p) |
|---|---|---|---|---|---|---|---|
| Bio-oil | 156.7 | 85.6 | 0.65 [0.53, 0.76] | 12.45 → 12.84 | 0.04 [-0.38, 0.60]; 0.804 | 0.09 | -0.031 (0.714) |
| Solid | 94.6 | 97.7 | 0.49 [0.40, 0.61] | 10.86 → 11.05 | 0.05 [-0.15, 0.25]; 0.545 | 0.01 | -0.047 (0.910) |



This negative result has two readings, which the data cannot separate. Either work-up conventions matter less than chemistry and conditions that the curated fields do not capture (feedstock batch, particle size, reactor heat-up, quenching and product-handling details), or the coarse, partly missing descriptors that can be parsed from publications are too noisy to reveal their effect — 23% of development bio-oil runs named no extraction solvent. In both cases the practical conclusion is the same: the offset of a new study is not predictable from what studies currently report, so it has to be either measured (Section 3.5) or represented in the uncertainty (Section 3.4).

## 3.4. Row-calibrated intervals under-cover new studies; study calibration largely restores coverage

Intervals calibrated on randomly held-out runs are narrow because the residuals of seen studies omit the study offset. For unseen development studies, nominal 90% row-calibrated intervals covered 0.57 (bio-oil; 95% CI 0.52–0.64) and 0.61 (solids) of runs with equal study weights, and 66% and 66% of studies had coverage below 0.80 (Table 4, Fig. 5). Calibrating on out-of-study residuals with equal study weights gave 0.91 (0.87–0.94) and 0.91; the improvement was significant across studies (one-sided Wilcoxon on per-study coverage, *p* < 0.001 for bio-oil and < 0.001 for solids). The price is width: 59.1 vs 22.8 wt% for bio-oil and 46.7 vs 20.6 wt% for solids. These widths are not a defect of the method but an honest statement of how little a literature-trained model knows about a study it has not seen. The same pattern held for α = 0.05 and 0.20, with 5 instead of 10 outer folds (Supplementary Tables S4–S5), and on the locked test studies (bio-oil RC 0.60 vs SC 0.89; solids RC 0.46 vs SC 0.82), for left-out feedstock families (mean) (bio-oil RC 0.55 vs SC 0.89; solids RC 0.60 vs SC 0.90), for temporally later studies (bio-oil RC 0.42 vs SC 0.85; solids RC 0.56 vs SC 0.90), on the external hydrochar database (solids RC 0.55 vs SC 0.92). An exploratory, post-hoc variant with locally adaptive widths (Supplementary Section S4) did not narrow the intervals (mean width 63.0 vs 59.1 wt% for bio-oil) and worsened the interval score, consistent with an error dominated by an unpredictable study offset.

Whether this holds for other base learners, and what the machine-learning model adds, was tested by repeating the evaluation with seven base learners (E9; Supplementary Table S10). Study-calibrated coverage was 0.90–0.91 for bio-oil and 0.89–0.92 for solids with every base learner, including the training mean. Row-calibrated coverage, by contrast, deteriorated with the capacity of the learner: 0.86 for the mean predictor, 0.80 for ridge regression, 0.65 for *k*-NN and 0.55–0.59 for the tree ensembles (bio-oil). This is the mechanism behind the failure of row calibration: flexible learners absorb the offsets of studies they have seen, so residuals of randomly held-out runs no longer contain the offset that a new study will carry. Relative to the 'no-ML' reference, the best learner narrowed valid intervals by 15% for bio-oil (53.5 vs 63.0 wt%, random forest) and 23% for solids (46.0 vs 59.4 wt%) — a real but modest gain — and after three local runs the median per-study RMSE was 8.18 vs 9.15 wt% (bio-oil) and 7.85 vs 9.89 wt% (solids).


**Table 4.** Empirical coverage of 90% prediction intervals: row-calibrated (RC) vs study-calibrated (SC).

| Target | Setting | α | Calibration | Coverage (rows) | Coverage (studies) | Width (wt%) | Studies <0.8 coverage |
|---|---|---|---|---|---|---|---|
| Bio-oil | Development CV (unseen studies) | 0.1 | RC | 0.612 | 0.57 | 22.8 | 0.66 |
| Bio-oil | Development CV (unseen studies) | 0.1 | SC | 0.93 | 0.909 | 59.1 | 0.16 |
| Solid | Development CV (unseen studies) | 0.1 | RC | 0.615 | 0.614 | 20.6 | 0.66 |
| Solid | Development CV (unseen studies) | 0.1 | SC | 0.901 | 0.908 | 46.7 | 0.16 |
| Bio-oil | Locked test | 0.1 | RC | 0.565 | 0.603 | 22.7 | 0.61 |
| Bio-oil | Locked test | 0.1 | SC | 0.82 | 0.895 | 54.8 | 0.21 |
| Solid | Locked test | 0.1 | RC | 0.44 | 0.457 | 21.0 | 0.77 |
| Solid | Locked test | 0.1 | SC | 0.864 | 0.821 | 46.7 | 0.23 |
| Bio-oil | Leave-family-out (mean) | 0.1 | RC | 0.569 | 0.554 | 22.5 | 0.62 |
| Bio-oil | Leave-family-out (mean) | 0.1 | SC | 0.888 | 0.894 | 57.6 | 0.16 |
| Bio-oil | Temporal (≤2018 → >2018) | 0.1 | RC | 0.456 | 0.422 | 21.9 | 0.84 |
| Bio-oil | Temporal (≤2018 → >2018) | 0.1 | SC | 0.846 | 0.853 | 64.1 | 0.28 |
| Solid | Leave-family-out (mean) | 0.1 | RC | 0.548 | 0.596 | 20.5 | 0.57 |
| Solid | Leave-family-out (mean) | 0.1 | SC | 0.858 | 0.896 | 46.5 | 0.16 |
| Solid | Temporal (≤2018 → >2018) | 0.1 | RC | 0.521 | 0.559 | 18.7 | 0.72 |
| Solid | Temporal (≤2018 → >2018) | 0.1 | SC | 0.877 | 0.897 | 49.0 | 0.14 |
| Solid | External 4TU | 0.1 | RC | 0.534 | 0.549 | 20.7 | 0.7 |
| Solid | External 4TU | 0.1 | SC | 0.934 | 0.918 | 47.3 | 0.16 |




![**Fig. 5.** Study-weighted empirical coverage of nominal 90% prediction intervals calibrated on random rows (RC) or on studies (SC) across validation settings (base + P features). Dashed line: nominal level.](/home/user/rp_c_12/figures/fig05_coverage.png){width=16cm}


## 3.5. A few local runs reduce error and interval width

When *k* runs of the new study are available, its offset can be estimated. For the 80 development studies with at least 11 bio-oil runs, the median per-study RMSE fell from 12.37 wt% (*k* = 0) to 9.22, 8.47 and 7.63 wt% with *k* = 1, 3 and 10 shrunk offsets, and the study-calibrated interval width fell from 59.3 to 37.2 wt% at *k* = 3 while study-weighted coverage stayed at 0.91 (Table 5, Fig. 6). For solids the corresponding RMSE values were 11.05, 8.84, 7.66 and 7.02 wt%. Shrinkage lowered the per-study RMSE relative to the raw mean offset at k = 1, 2, 3, 5, 10 (Holm-corrected Wilcoxon, bio-oil) and was never significantly worse. The estimated shrinkage constant ($\hat\lambda = \hat\sigma_w^2/\hat\tau^2$, median over folds 0.48 for bio-oil) is small, so the shrunk and raw offsets converge after a few runs; shrinkage matters mainly for *k* = 1–2, which is exactly the regime of a laboratory screening a new feedstock. Estimating $\tau^2$ by restricted maximum likelihood instead of the method of moments gave median per-study RMSE at k = 1 of 9.37 vs 10.06 wt% (bio-oil) and 9.33 vs 8.89 wt% (solids; Supplementary Table S6). Replacing the tuned hyper-parameters of the base learner by library defaults changed its study-grouped RMSE by 0.0–1.0 wt% (Supplementary Table S7), so the conclusions do not hinge on tuning. These results quantify, with valid intervals, the observation of Elfetni et al. (2027) that local calibration runs reduce the error of literature-trained HTL surrogates.


**Table 5.** k-shot adaptation to a new study (studies with ≥ 11 runs; 20 random support sets per study).

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




![**Fig. 6.** *k*-shot adaptation to a new study (development studies with ≥ 11 runs, base + P features, 20 random support sets per study and *k*). Top: median per-study RMSE of the remaining runs; bottom: width of the re-calibrated 90% interval. *k* = 0 is the unadapted model.](/home/user/rp_c_12/figures/fig06_kshot.png){width=16cm}


## 3.6. Generalisation, robustness and cost

The locked test studies, evaluated once after all modelling decisions had been frozen, gave a more pessimistic picture than development CV. For bio-oil yield (556 runs, 28 studies) the STRATA base learner reached RMSE = 18.3 wt% (R² = -0.95; best learner k-nearest neighbours, 12.9 wt%; mean predictor 13.6 wt%); for solid yield (457 runs, 30 studies) the STRATA base learner reached RMSE = 18.5 wt% (R² = 0.30; best learner MLP, 14.4 wt%; mean predictor 23.0 wt%). For bio-oil, only 4 of the 11 non-trivial learners had a lower pooled RMSE than the mean predictor, although 6 had a lower median per-study RMSE: pooled errors were dominated by a few studies outside the bulk of the training distribution — for XGBoost, a single solvothermal series of 90 runs contributed 54% of the squared error, and excluding it (post hoc) lowered the RMSE from 18.3 to 13.6 wt% (R² = 0.00). Study-weighted coverage of row-calibrated 90% intervals was 0.60 (95% CI 0.47–0.73) for bio-oil and 0.46 (95% CI 0.34–0.58) for solids; study-calibrated intervals reached 0.89 (95% CI 0.81–0.97) and 0.82 (95% CI 0.70–0.92) (Table 6, Fig. 5). Study calibration thus removed most, but for solids not all, of the under-coverage; with 28–30 locked studies the intervals are wide, and the solid-yield shortfall reflects a few studies with feedstocks (technical lignin, plastic–biomass blends) that are rare in the training data.


**Table 6.** Single evaluation on the 38 locked test studies (models trained on all development studies, base features).

| Target | Learner | Runs | Studies | RMSE | R² | Median study RMSE |
|---|---|---|---|---|---|---|
| Bio-oil | k-NN | 556 | 28 | 12.878 | 0.029 | 11.935 |
| Bio-oil | Ridge | 556 | 28 | 12.965 | 0.016 | 11.992 |
| Bio-oil | GPBoost | 556 | 28 | 13.209 | -0.021 | 10.769 |
| Bio-oil | CatBoost | 556 | 28 | 13.389 | -0.049 | 10.778 |
| Bio-oil | Mean | 556 | 28 | 13.634 | -0.088 | 11.123 |
| Bio-oil | SVR | 556 | 28 | 13.913 | -0.133 | 11.882 |
| Bio-oil | Extra trees | 556 | 28 | 14.643 | -0.255 | 11.336 |
| Bio-oil | Random forest | 556 | 28 | 15.692 | -0.441 | 9.709 |
| Bio-oil | XGBoost | 556 | 28 | 18.273 | -0.954 | 9.597 |
| Bio-oil | LightGBM | 556 | 28 | 20.122 | -1.37 | 9.648 |
| Bio-oil | MLP | 556 | 28 | 22.521 | -1.969 | 14.511 |
| Bio-oil | HistGB | 556 | 28 | 22.839 | -2.053 | 9.766 |
| Solid | MLP | 457 | 30 | 14.416 | 0.573 | 10.978 |
| Solid | Extra trees | 457 | 30 | 16.546 | 0.438 | 12.349 |
| Solid | SVR | 457 | 30 | 17.052 | 0.403 | 12.653 |
| Solid | k-NN | 457 | 30 | 18.401 | 0.305 | 11.857 |
| Solid | XGBoost | 457 | 30 | 18.528 | 0.295 | 13.71 |
| Solid | Ridge | 457 | 30 | 18.744 | 0.279 | 14.67 |
| Solid | LightGBM | 457 | 30 | 18.889 | 0.268 | 12.971 |
| Solid | HistGB | 457 | 30 | 19.196 | 0.244 | 13.187 |
| Solid | Random forest | 457 | 30 | 19.316 | 0.234 | 12.56 |
| Solid | CatBoost | 457 | 30 | 19.809 | 0.194 | 13.243 |
| Solid | GPBoost | 457 | 30 | 21.937 | 0.012 | 17.291 |
| Solid | Mean | 457 | 30 | 23.03 | -0.089 | 17.925 |



Predicting studies published after 2018 from earlier studies gave RMSE = 19.4 (bio-oil; higher than the study-grouped CV value of 15.8 wt%) and 16.5 wt% (solids; higher than 14.1 wt%), i.e. models trained on older literature transfer no better to newer studies than to randomly chosen unseen studies. Leaving out one feedstock family at a time gave mean RMSE of 17.2 and 16.3 wt%, with the largest errors for the 'Other' category (bio-oil, 32.6 wt%) and 'Other' (solids, 29.8 wt%). On the independent 4TU hydrochar database (502 runs after removing 36 potential duplicates; 69 feedstock series), a solid-yield model trained on all development studies reached RMSE = 13.3 wt% (R² = 0.31), whereas training on the 16 HTC development studies alone gave 16.7 wt% (R² = -0.08), showing that the small HTC subset of the primary database does not by itself support transfer to other HTC compilations (Table 7).


**Table 7.** Temporal, feedstock-family and external generalisation of the STRATA base learner.

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



Adding Gaussian noise of 20% of the training standard deviation to continuous test features increased the bio-oil RMSE from 15.7 to 16.6 wt% and the solid RMSE from 13.9 to 15.4 wt%, while SC coverage was 0.90 without and 0.90 with noise (bio-oil) — the error budget for unseen studies is dominated by the study offset, not by input noise. Training on 25% instead of all training studies raised the bio-oil RMSE from 15.7 to 20.3 wt%, and SC coverage remained 0.89, whereas RC coverage stayed at 0.45–0.56 (Fig. 7).


![**Fig. 7.** Robustness of the STRATA base learner (base + P features). Top: RMSE (mean ± SD over outer folds) with Gaussian noise added to continuous test features or with fewer training studies. Bottom: study-weighted coverage of RC and SC 90% intervals.](/home/user/rp_c_12/figures/fig07_robustness.png){width=16cm}


All learners trained in at most 9 s on one CPU thread (MLP); the STRATA base learner took 0.2 s and predicted 1,000 runs in 4 ms (Table 8, Fig. 8). The complete STRATA procedure — two inner five-fold cross-validations, quantiles, variance components and k-shot quantiles for all k — took 2.3–7.0 s on all development studies, against 0.3–0.5 s for fitting the base learner alone (measured, 1 and 4 threads); this overhead is negligible compared with the cost of a single hydrothermal experiment.


**Table 8.** Computational cost (bio-oil, development set, single thread). Peak RSS increase is measured relative to the process peak after data loading.

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




![**Fig. 8.** Accuracy for unseen studies versus single-thread fit time on the development set (bio-oil, base features).](/home/user/rp_c_12/figures/fig08_efficiency.png){width=16cm}


Because literature compilations can contain the same experiment reported in several papers, which would leak information across study-grouped folds, the development data were audited (E10): 166 bio-oil runs (7.3%, 16 studies) and 143 solid-yield runs (6.6%) had an identical counterpart in another study. Removing them increased the study-grouped RMSE of the STRATA base learner from 15.8 to 16.6 wt% (bio-oil) and from 14.1 to 14.6 wt% (solids), with between-study shares of 0.65 and 0.52; 10 bio-oil and 18 solid locked-test runs matched development runs. Cross-study duplicates therefore make study-grouped estimates slightly optimistic and do not affect the conclusions.

## 3.7. Error analysis and implications

Out-of-study errors were largest for Other feedstocks among families (bio-oil RMSE 33.9 wt%, 6 studies), for the ≤250 °C temperature band (21.1 wt%) and for HTL solvothermal runs (18.5 wt%) (Supplementary Table S9). The five worst-predicted bio-oil studies had per-study RMSE between 35.1 and 61.4 wt% and absolute mean offsets of 26.7–60.9 wt% (processes: HTL 3, HTC 1, HTL solvothermal 1). Across extraction-solvent groups with at least three studies, the bio-oil RMSE ranged from 10.8 (hydrocarbon) to 19.8 wt% (none named) and the mean residual from -9.5 to +9.7 wt% (Fig. 9).


![**Fig. 9.** Mean out-of-study residual by extraction solvent named in the source study (groups with ≥ 3 studies; base features, seed-averaged outer-fold predictions).](/home/user/rp_c_12/figures/fig09_error_by_solvent.png){width=16cm}



![**Fig. 10.** Observed versus predicted yields for the STRATA base learner under random-row CV and study-grouped CV (seed 11).](/home/user/rp_c_12/figures/fig10_parity.png){width=16cm}


For practitioners, three recommendations follow. First, literature-trained hydrothermal surrogates should be validated with folds defined by source study (or by laboratory), and random-split metrics should not be used to claim predictive ability for new feedstocks or plants. Second, reported prediction intervals should be calibrated across studies; for the present database this means honest intervals of roughly ±30 wt% for bio-oil yield of a new study, which is wide enough to rule out fine-grained optimisation from literature data alone. Third, a handful of runs on the target feedstock and reactor are worth more than additional model complexity: three local runs reduced the median per-study error by 3.9 wt% (bio-oil) and 3.4 wt% (solids), whereas the median per-study errors of the competitive learners differed by at most 0.6 and 1.6 wt% (Sections 3.1 and 3.5). For data curators, the null result for work-up descriptors suggests recording richer, standardised metadata (product-recovery procedure, quench, mass-balance closure, uncertainty of the yield measurement) so that the sources of between-study variation can eventually be modelled rather than absorbed.

## 3.8. Limitations

The study relies on one curated literature database; its extraction and harmonisation choices, imputed feedstock fractions and residual transcription errors propagate into all results, although they affect random and study-grouped evaluation alike. The protocol descriptors were parsed from free-text fields and are coarse. Study-level conformal validity assumes that a new study is exchangeable with the calibration studies; a study that differs systematically (a new reactor concept, unusual feedstock or catalyst) may be under-covered, as the locked solid-yield studies (coverage 0.82) and the HTC subset of the development studies (coverage 0.83 for solids) show. The external database lacks study identifiers, so feedstock series were used as pseudo-studies. The *k*-shot analysis assumes that the first *k* runs of a study are exchangeable with its remaining runs; in practice laboratories choose runs deliberately. Physical admissibility across phases was not enforced here; because STRATA only requires out-of-study residuals of a point predictor (Supplementary Table S10), it could be applied to physically admissible surrogates, but this was not tested. Cross-study duplicate runs (Section 3.6) were retained in the main analyses, which makes the reported study-grouped accuracy slightly optimistic. Three analyses (E9–E11), the adaptive-interval variant and the locked-test sensitivity analysis were added after the main results were known. Finally, no new experiments were performed: the conclusions concern the transferability of literature-trained models, not the chemistry of hydrothermal conversion itself.



# 4. Conclusions

Literature-trained models of hydrothermal conversion predict runs from studies they have seen far better than runs from new studies, and on locked studies none predicted bio-oil yield substantially better than the training mean: random splitting overstated accuracy about two-fold across learner families, and half to two-thirds of the remaining error variance was a study-level offset that recorded work-up and yield-basis descriptors did not explain. Conformal intervals calibrated on random rows were over-confident for new studies, whereas calibrating at the level of studies raised coverage from 0.46–0.61 to 0.82–0.91 across development and locked test studies, and a few runs from the new study combined through empirical-Bayes shrinkage narrowed both errors and intervals. Study-grouped validation, study-calibrated intervals and local anchoring runs are recommended as minimum practice for literature-trained bioresource surrogates.

# CRediT authorship contribution statement

[Author 1]: Conceptualization, Methodology, Software, Formal analysis, Writing – original draft. [Author 2]: Validation, Writing – review & editing. [Author 3]: Supervision, Writing – review & editing. *(To be completed by the authors.)*

# Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper. *(To be confirmed by the authors.)*

# Declaration of generative AI and AI-assisted technologies in the manuscript preparation process

During the preparation of this work the authors used an AI assistant (Claude, Anthropic) to search and verify literature metadata, write analysis code, run the computational experiments and draft the manuscript text. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the published article. *(The authors must verify, adapt and confirm this statement before submission.)*

# Data availability

All data analysed are publicly available under CC BY 4.0 (Elfetni, 2026; Abdeldayem et al., 2025). The complete code, the locked test-study list, configuration files, raw result files and the scripts that generate every table and figure are available at [repository URL to be inserted; archived DOI to be minted at acceptance].

# Acknowledgements

The authors thank the curators of the hydrothermal treatment/liquefaction database and of the 4TU hydrochar database for releasing their data openly. *(Funding: to be completed by the authors.)*

# Appendix A. Supplementary data

Supplementary material (Sections S1–S7, Tables S1–S10: literature screening, protocol deviations, additional benchmark and sensitivity results, exploratory adaptive intervals, error analysis by subgroup, STRATA with different base learners, reproducibility) accompanies this article.

# References

::: {custom-style="Bibliography"}
Abdeldayem, O., Al-Sakkari, E., Ortiz, D., Dupont, C., Ferras, D., Ouali, M.-S., Ragab, A., Kennedy, M., 2025. Database underlying the research for the development of machine learning models for predicting the physicochemical properties of hydrochar [dataset]. 4TU.ResearchData. https://doi.org/10.4121/834c3f22-f46a-4808-a0fe-46298be6a133.v1
:::

::: {custom-style="Bibliography"}
Angelopoulos, A.N., Bates, S., 2023. Conformal Prediction: A Gentle Introduction. Now Publishers. https://doi.org/10.1561/9781638281597
:::

::: {custom-style="Bibliography"}
Barber, R.F., Candès, E.J., Ramdas, A., Tibshirani, R.J., 2023. Conformal prediction beyond exchangeability. Ann. Stat. 51(2), 816-845. https://doi.org/10.1214/23-aos2276
:::

::: {custom-style="Bibliography"}
Bersson, E., Hoff, P.D., 2024. Optimal Conformal Prediction for Small Areas. J. Surv. Stat. Methodol. 12(5), 1464-1488. https://doi.org/10.1093/jssam/smae010
:::

::: {custom-style="Bibliography"}
Breiman, L., 2001. Random Forests. Mach. Learn. 45(1), 5-32. https://doi.org/10.1023/a:1010933404324
:::

::: {custom-style="Bibliography"}
Chen, T., Guestrin, C., 2016. XGBoost: A scalable tree boosting system, in: Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 785-794. https://doi.org/10.1145/2939672.2939785
:::

::: {custom-style="Bibliography"}
Demšar, J., 2006. Statistical Comparisons of Classifiers over Multiple Data Sets. J. Mach. Learn. Res. 7(1), 1–30. https://jmlr.org/papers/v7/demsar06a.html
:::

::: {custom-style="Bibliography"}
DerSimonian, R., Laird, N., 1986. Meta-analysis in clinical trials. Control. Clin. Trials 7(3), 177-188. https://doi.org/10.1016/0197-2456(86)90046-2
:::

::: {custom-style="Bibliography"}
Djandja, O.S., Hu, Y., Zeng, Y., He, Q.S., 2027. Predicting bio-oil yield from hydrothermal liquefaction of lignocellulosic biomass: machine learning approach and uncertainty propagation via joint bootstrap Monte Carlo. Fuel 430, 141091. https://doi.org/10.1016/j.fuel.2026.141091
:::

::: {custom-style="Bibliography"}
Dunn, R., Wasserman, L., Ramdas, A., 2022. Distribution-Free Prediction Sets for Two-Layer Hierarchical Models. J. Am. Stat. Assoc. 118(544), 2491-2502. https://doi.org/10.1080/01621459.2022.2060112
:::

::: {custom-style="Bibliography"}
Efron, B., 1979. Bootstrap Methods: Another Look at the Jackknife. Ann. Stat. 7(1), 1-26. https://doi.org/10.1214/aos/1176344552
:::

::: {custom-style="Bibliography"}
Efron, B., Morris, C., 1975. Data Analysis Using Stein's Estimator and its Generalizations. J. Am. Stat. Assoc. 70(350), 311-319. https://doi.org/10.1080/01621459.1975.10479864
:::

::: {custom-style="Bibliography"}
Elfetni, S., 2026. Unified, curated dataset of biomass hydrothermal treatment/liquefaction experiments for lignocellulosic and lignin-rich biomass — Version 1.0.0 [dataset]. Center for the Transformation of Chemistry. https://doi.org/10.22000/8bnbhqccf4aq7kea
:::

::: {custom-style="Bibliography"}
Elfetni, S., Thinius, S., Dwivedi, P., Seeberger, P.H., Tyrikos-Ergas, T., 2026. Energy and carbon routing in hydrothermal lignocellulosic biomass conversion: an uncertainty-aware machine-learning framework. Elsevier BV. https://doi.org/10.2139/ssrn.6816225
:::

::: {custom-style="Bibliography"}
Elfetni, S., Thinius, S., Dwivedi, P., Seeberger, P.H., Tyrikos-Ergas, T., 2027. Conservation-informed machine learning for physically admissible four-phase hydrothermal liquefaction surrogate modelling. Bioresour. Technol. 463, 135587. https://doi.org/10.1016/j.biortech.2026.135587
:::

::: {custom-style="Bibliography"}
Elliott, D.C., Biller, P., Ross, A.B., Schmidt, A.J., Jones, S.B., 2015. Hydrothermal liquefaction of biomass: Developments from batch to continuous process. Bioresour. Technol. 178, 147-156. https://doi.org/10.1016/j.biortech.2014.09.132
:::

::: {custom-style="Bibliography"}
Fisch, A., Schuster, T., Jaakkola, T., Barzilay, R., 2021. Few-shot Conformal Prediction with Auxiliary Tasks, in: Proc. 38th Int. Conf. Mach. Learn., PMLR 139. arXiv:2102.08898
:::

::: {custom-style="Bibliography"}
Funke, A., Ziegler, F., 2010. Hydrothermal carbonization of biomass: A summary and discussion of chemical mechanisms for process engineering. Biofuels Bioprod. Biorefin. 4(2), 160-177. https://doi.org/10.1002/bbb.198
:::

::: {custom-style="Bibliography"}
Geurts, P., Ernst, D., Wehenkel, L., 2006. Extremely randomized trees. Mach. Learn. 63(1), 3-42. https://doi.org/10.1007/s10994-006-6226-1
:::

::: {custom-style="Bibliography"}
Gollakota, A., Kishore, N., Gu, S., 2018. A review on hydrothermal liquefaction of biomass. Renew. Sustain. Energy Rev. 81, 1378-1392. https://doi.org/10.1016/j.rser.2017.05.178
:::

::: {custom-style="Bibliography"}
Gungor, S., Insel, M.A., Sadikoglu, H., Melikoglu, M., 2025. Prediction of Biocrude Oil Yield From Biomass Hydrothermal Liquefaction Via Interpretable Machine Learning Using Higher Heating Value and Process Parameters. BioEnergy Res. 18(1), 100. https://doi.org/10.1007/s12155-025-10906-z
:::

::: {custom-style="Bibliography"}
Higgins, J.P.T., Thompson, S.G., 2002. Quantifying heterogeneity in a meta‐analysis. Stat. Med. 21(11), 1539-1558. https://doi.org/10.1002/sim.1186
:::

::: {custom-style="Bibliography"}
Hollmann, N., Müller, S., Purucker, L., Krishnakumar, A., Körfer, M., Hoo, S.B., Schirrmeister, R.T., Hutter, F., 2025. Accurate predictions on small data with a tabular foundation model. Nature 637(8045), 319-326. https://doi.org/10.1038/s41586-024-08328-6
:::

::: {custom-style="Bibliography"}
Jang, H.J., Ng, W., Chen, S., Setia, R., Minasny, B., 2026. Illusions of Accuracy: Widespread Data Leakage Distorts Machine Learning Results in Biochar Research. GCB Bioenergy 18(9), e70173. https://doi.org/10.1111/gcbb.70173
:::

::: {custom-style="Bibliography"}
Kapoor, S., Narayanan, A., 2023. Leakage and the reproducibility crisis in machine-learning-based science. Patterns 4(9), 100804. https://doi.org/10.1016/j.patter.2023.100804
:::

::: {custom-style="Bibliography"}
Katongtung, T., Phromphithak, S., Onsree, T., Tippayawong, N., 2024. Machine Learning Approach for Predicting Hydrothermal Liquefaction of Lignocellulosic Biomass. BioEnergy Res. 17(4), 2246-2258. https://doi.org/10.1007/s12155-024-10773-0
:::

::: {custom-style="Bibliography"}
Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., Liu, T.-Y., 2017. LightGBM: A Highly Efficient Gradient Boosting Decision Tree, in: Advances in Neural Information Processing Systems. https://papers.nips.cc/paper_files/paper/2017/hash/6449f44a102fde848669bdd9eb6b76fa-Abstract.html
:::

::: {custom-style="Bibliography"}
Lei, J., G’Sell, M., Rinaldo, A., Tibshirani, R.J., Wasserman, L., 2018. Distribution-Free Predictive Inference for Regression. J. Am. Stat. Assoc. 113(523), 1094-1111. https://doi.org/10.1080/01621459.2017.1307116
:::

::: {custom-style="Bibliography"}
Leng, L., Zhang, W., Chen, Q., Zhou, J., Peng, H., Zhan, H., Li, H., 2022. Machine learning prediction of nitrogen heterocycles in bio-oil produced from hydrothermal liquefaction of biomass. Bioresour. Technol. 362, 127791. https://doi.org/10.1016/j.biortech.2022.127791
:::

::: {custom-style="Bibliography"}
Libra, J.A., Ro, K.S., Kammann, C., Funke, A., Berge, N.D., Neubauer, Y., Titirici, M.-M., Fühner, C., Bens, O., Kern, J., Emmerich, K.-H., 2011. Hydrothermal carbonization of biomass residuals: a comparative review of the chemistry, processes and applications of wet and dry pyrolysis. Biofuels 2(1), 71-106. https://doi.org/10.4155/bfs.10.81
:::

::: {custom-style="Bibliography"}
Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., Duchesnay, É., 2011. Scikit-learn: Machine Learning in Python. J. Mach. Learn. Res. 12(85), 2825–2830. https://jmlr.org/papers/v12/pedregosa11a.html
:::

::: {custom-style="Bibliography"}
Prokhorenkova, L., Gusev, G., Vorobev, A., Dorogush, A.V., Gulin, A., 2018. CatBoost: unbiased boosting with categorical features, in: Adv. Neural Inf. Process. Syst. 31. arXiv:1706.09516
:::

::: {custom-style="Bibliography"}
Roberts, D.R., Bahn, V., Ciuti, S., Boyce, M.S., Elith, J., Guillera‐Arroita, G., Hauenstein, S., Lahoz‐Monfort, J.J., Schröder, B., Thuiller, W., Warton, D.I., Wintle, B.A., Hartig, F., Dormann, C.F., 2017. Cross‐validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. Ecography 40(8), 913-929. https://doi.org/10.1111/ecog.02881
:::

::: {custom-style="Bibliography"}
Sigrist, F., 2022. Gaussian Process Boosting. J. Mach. Learn. Res. 23(232), 1–46. https://jmlr.org/papers/v23/20-322.html
:::

::: {custom-style="Bibliography"}
Tian, Y., Kim, J., Liu, Y., 2025. Interpretable machine learning model for bio-oil property prediction from hydrothermal liquefaction of biomass via graph neural networks-based molecular structure. Energy 329, 136708. https://doi.org/10.1016/j.energy.2025.136708
:::

::: {custom-style="Bibliography"}
Toor, S.S., Rosendahl, L., Rudolf, A., 2011. Hydrothermal liquefaction of biomass: A review of subcritical water technologies. Energy 36(5), 2328-2342. https://doi.org/10.1016/j.energy.2011.03.013
:::

::: {custom-style="Bibliography"}
Valdez, P.J., Dickinson, J.G., Savage, P.E., 2011. Characterization of product fractions from hydrothermal liquefaction of Nannochloropsis sp. and the influence of solvents. Energy Fuels 25(7), 3235-3243. https://doi.org/10.1021/ef2004046
:::

::: {custom-style="Bibliography"}
Vovk, V., Gammerman, A., Shafer, G., 2022. Algorithmic Learning in a Random World, 2nd ed. Springer, Cham. https://doi.org/10.1007/978-3-031-06649-8
:::

::: {custom-style="Bibliography"}
Watson, J., Lu, J., de Souza, R., Si, B., Zhang, Y., Liu, Z., 2019. Effects of the extraction solvents in hydrothermal liquefaction processes: Biocrude oil quality and energy conversion efficiency. Energy 167, 189-197. https://doi.org/10.1016/j.energy.2018.11.003
:::

::: {custom-style="Bibliography"}
Wilcoxon, F., 1945. Individual Comparisons by Ranking Methods. Biom. Bull. 1(6), 80. https://doi.org/10.2307/3001968
:::

::: {custom-style="Bibliography"}
Zhang, W., Li, J., Liu, T., Leng, S., Yang, L., Peng, H., Jiang, S., Zhou, W., Leng, L., Li, H., 2021. Machine learning prediction and optimization of bio-oil production from hydrothermal liquefaction of algae. Bioresour. Technol. 342, 126011. https://doi.org/10.1016/j.biortech.2021.126011
:::



