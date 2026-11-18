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
- Study-calibrated 90% intervals covered 0.82–0.91; row-calibrated 0.46–0.61
- Three designed local runs cut the median yield error by 1.6–6.4 wt%
- For locked bio-oil studies, local runs alone beat literature-anchored models

# Abstract

Machine-learning models of hydrothermal liquefaction (HTL) and carbonization (HTC) are trained on literature data and validated by random splits, yet are meant to help laboratories whose studies they have never seen. This deployment problem was evaluated for bio-oil and solid yields using a curated database of 3,693 runs from 188 studies, 38 studies locked before modelling, an external hydrochar database and a protocol fixed in advance. Random splitting overstated accuracy about two-fold, and study-level offsets, which reported work-up descriptors did not explain, made up 0.49–0.65 of out-of-study error variance. Conformal intervals calibrated across studies covered 0.82–0.91 of new-study runs (row-calibrated: 0.46–0.61). In a retrospective simulated deployment, a laboratory measured up to five runs in a screening design. Combining three runs with the literature model (STRATA) lowered the median per-study error from 12.4 to 8.8 wt% (bio-oil) and from 9.4 to 7.8 wt% (solid) for unseen development studies, outperforming the local runs alone, and from 13.4 to 7.1 wt% for locked solid studies. For locked bio-oil studies, however, the local runs alone were more accurate, and an applicability-domain score did not anticipate this. With one to five local runs, 90% interval half-widths remained ±17.0–24.6 wt%, so these models support screening, not optimisation. The resulting STRATA-Lab workflow — study-calibrated intervals, a few designed local runs and an explicit comparison with local-only estimates — is proposed as minimum practice for transferring literature-trained bioresource models.

**Keywords:** hydrothermal liquefaction; hydrothermal carbonization; machine learning; conformal prediction; model transferability; experimental planning


# 1. Introduction

Hydrothermal liquefaction (HTL) and hydrothermal carbonization (HTC) convert wet lignocellulosic and residual biomass into bio-oil (biocrude), a carbon-rich solid (hydrochar or char), an aqueous phase and gas, without prior drying (Toor et al., 2011; Elliott et al., 2015; Funke and Ziegler, 2010; Libra et al., 2011). Product yields depend non-linearly on feedstock composition, temperature, residence time, solid loading, catalysts and co-solvents (Gollakota et al., 2018), and each experiment is costly. Machine-learning (ML) models trained on runs compiled from the literature have therefore become a common tool for predicting yields and for screening operating windows (Zhang et al., 2021; Leng et al., 2022; Katongtung et al., 2024; Gungor et al., 2025; Tian et al., 2025; Djandja et al., 2027). A reproducible search of PubMed and Crossref (run 2026-11-18; full strings, eligibility rules and record flow in Supplementary Table S1) identified 93 primary ML studies of hydrothermal conversion published since 2015, 18 of them in *Bioresource Technology*. Of the 51 with an abstract, 2 mentioned grouped or external validation and 4 any form of uncertainty quantification; in a PubMed subset reporting R², the median best R² was 0.93 (15 studies; Supplementary Table S2).

Such models are built to be used by a laboratory that was not part of the training data — a group that has a new feedstock and reactor and must decide which conditions to run first. For this *new-laboratory deployment problem* four things matter: a prediction of the yields before any experiment, an honest statement of its uncertainty, guidance on how many and which first runs to perform, and a way to tell whether the literature model or the laboratory's own first runs should be trusted. Random splits of literature data answer none of these questions. Literature-compiled data are clustered: each source publication contributes a series of runs that share the feedstock batch, reactor, analytical work-up and the authors' definition of a "yield". When runs of the same study fall on both sides of a random split, the test set no longer represents a new laboratory, and accuracy is overstated — a form of group leakage documented across ML-based science (Kapoor and Narayanan, 2023) and for biochar studies (Jang et al., 2026). Bio-oil yield is, moreover, operationally defined by the recovery solvent and the reporting basis (Valdez et al., 2011; Watson et al., 2019), so study-specific offsets are expected.

Two recent studies used the same public database (Elfetni, 2026) and partly address these issues. Elfetni et al. (2027) built physically admissible four-phase HTL surrogates on a closure-valid subset of 680 experiments, reported that publication-aware validation exposes inter-study heterogeneity, showed that five local records reduced the median error of the publications eligible for local calibration, and reported split-conformal coverage on a random test partition. A preprint by the same group (Elfetni et al., 2026) modelled energy and carbon routing with ensemble and conformal uncertainty for screening and experimental prioritisation. Bootstrap and Monte Carlo uncertainty has also been propagated through HTL yield models (Djandja et al., 2027). What these studies leave open, and what a new laboratory needs to know, is (i) whether prediction intervals keep their nominal coverage for studies that were never seen, and how wide honest intervals are; (ii) whether combining a few local runs with the literature model is better than simply using the local runs, at each number of runs, when the runs are chosen as a laboratory would choose them and intervals are re-calibrated accordingly; (iii) whether a laboratory can tell in advance that the literature model will mislead it; and (iv) whether anything beyond a level shift — effects of conditions, or the ranking of candidate runs — transfers between laboratories. Table 1 sets out how the present work relates to the two studies; none of the present authors is an author of either study, and the overlap is the openly licensed database.


**Table 1.** Relation of this work to the two studies that use the same database. Information on the two studies is taken from their abstracts (Bioresour. Technol. article online 17 August 2026; SSRN preprint 2026). None of the present authors is an author of either study; the overlap is the shared, openly licensed database.

| Aspect | Elfetni et al. (2027), Bioresour. Technol. | Elfetni et al. (2026), SSRN preprint | This work |
|---|---|---|---|
| Data | Curated corpus of 3,693 records; 680 closure-valid HTL and solvothermal experiments from 60 publications used for modelling | 3,693 HTL/HTC experiments from 187 papers | Same public database (v1.0.0; 3,693 runs, 188 studies) for bio-oil and solid yields; independent 4TU hydrochar database for external validation |
| Targets | Four phase yields as one composition vector; carbon and HHV residuals | Mass, energy and carbon partitioning; HHV of condensed phases | Bio-oil and solid yields only; aqueous and gas phases and mass closure not modelled |
| Main validation | Common 408/136/136 training/calibration/test partition; publication-aware validation reported in addition | Test R² ≈ 0.8 for yields (partition not stated in the abstract) | Study-grouped CV; 38 studies locked before modelling and evaluated once; temporal, feedstock-family and external tests |
| Pre-specified protocol | Not stated in the abstract | Not stated in the abstract | Protocol, locked list and five addenda committed to a version-controlled repository before the analyses they govern |
| Uncertainty | Phase-wise 90% split-conformal intervals (coverage 0.875–0.956 on the test set) | Ensemble and conformal uncertainty | Row- vs study-calibrated conformal intervals compared on unseen, locked and external studies; interval width treated as a primary outcome |
| Local adaptation | k = 5 local records for 38 publications: median vector RMSE 13.91 → 7.10 wt% | Not stated in the abstract | k = 0–5 runs in three run orders; literature only (A) vs literature + local runs (B, STRATA) vs local runs only (C); intervals re-calibrated for every k; Holm-corrected tests |
| Decision support | Screening within represented data support | Uncertainty-aware screening and experimental prioritisation | Applicability-domain score with a pre-registered threshold; runs needed for a target interval width; case studies selected by a pre-specified rule |
| Physical admissibility | Core contribution (non-negativity, exact closure) | Not stated | Not addressed |



This work addresses (i)–(iv) with a framework called STRATA-Lab (Fig. 1). Its statistical core, STRATA, assembles established constructions — study-weighted conformal calibration for hierarchical data (Dunn et al., 2022), empirical-Bayes shrinkage of a study offset (Efron and Morris, 1975) and re-calibration over exchangeable calibration groups as in meta-learned and small-area conformal prediction (Fisch et al., 2021; Bersson and Hoff, 2024) — around any point predictor. STRATA-Lab adds the deployment steps: a literature prediction with a study-calibrated interval, an applicability-domain score, first runs placed by a simple screening design, a comparison of literature-anchored and local-only estimates, and the number of runs needed for a target interval width. The framework was evaluated by retrospective simulated deployment on published data — on unseen development studies, on 38 studies locked away before any model was fitted, and on an independent hydrochar database — and illustrated with two laboratory case studies selected by a pre-specified rule. The scope is limited to bio-oil and solid yields; aqueous and gas phases and mass closure, addressed by Elfetni et al. (2027), are not modelled, and no new experiments were performed. All analyses specified in advance are reported, including those whose hypotheses failed.


![**Fig. 1.** STRATA-Lab workflow for a new laboratory. Steps 3–4 were validated retrospectively on development, locked and external studies; step 5 is limited to screening because development interval half-widths remained ±17.0–24.6 wt% after one to five local runs.](/home/user/rp_c_12/figures/fig16_strata_lab_workflow.png){width=16cm}


# 2. Materials and methods

## 2.1. Data

The primary data were the Version 1.0.0 release of the curated hydrothermal treatment/liquefaction database (Elfetni, 2026) (CC BY 4.0; 3,693 runs from 188 source publications, 1982–2026; SHA-256 of the file verified at every load). Each run records the source DOI, feedstock ultimate, proximate and lignocellulosic composition, operating conditions, catalyst, reaction medium, the reported yield basis and separation procedure, and product yields. Two targets were modelled: bio-oil yield (HTL and solvothermal HTL runs) and solid-product yield (HTL, solvothermal HTL and HTC runs), both in wt%. Pre-specified exclusions were: aqueous-phase reforming runs; yields outside 0–100 wt%; yields reported on a carbon basis; missing feedstock C or O, temperature or residence time; and studies contributing a single run to a target (Table 2). An independent external data set — a 4TU.ResearchData hydrochar database (Abdeldayem et al., 2025) (CC BY 4.0) without study identifiers — was used only for external validation of solid yield (Sections 2.6–2.7).


**Table 2.** Data used for each target after pre-specified exclusions.

| Target | Split | Runs | Studies | Median runs/study | Yield mean ± SD (wt%) | Excluded (carbon basis / missing inputs / single-run study) |
|---|---|---|---|---|---|---|
| Bio-oil | Development | 2261 | 122 | 15 | 30.8 ± 18.0 | 3 / 11 / 4 |
| Bio-oil | Locked test | 556 | 28 | 12 | 26.9 ± 13.1 | 0 / 1 / 0 |
| Solid | Development | 2156 | 120 | 13 | 33.4 ± 20.2 | 0 / 12 / 5 |
| Solid | Locked test | 457 | 30 | 12 | 40.0 ± 22.1 | 0 / 0 / 1 |



## 2.2. Locked study-level test set, pre-specification and leakage controls

Before any model was fitted, 20% of the source publications (38 studies, seed 20261110) were drawn at random and locked. They were evaluated once per registered analysis, after all modelling decisions for that analysis had been frozen, with models trained on all development studies. The analysis protocol (research questions, metrics, statistical tests, seeds and the locked list) and five later addenda were registered as timestamped commits in a version-controlled repository hosted on GitHub before the analyses they govern were run; the protocol was not deposited in a public registry, so this is weaker than formal pre-registration, and the commit history is reported for verification (Supplementary Table S3). Addendum D, which specifies the deployment analyses of Section 2.6, was registered after an external pre-submission review and before any of those analyses was run. Deviations are listed in Supplementary Section S2. Leakage controls were: the unit of splitting is the source publication; DOI, title and publication year are never model inputs; all statistics-estimating preprocessing (median imputation with missing-value indicators, standardisation) is refitted inside each training fold; the external database was screened for runs that duplicate runs of the primary database (36 potential duplicates removed); and cross-study duplicate runs in the primary database were audited (Section 3.7).

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

## 2.6. STRATA-Lab: retrospective simulated deployment (Addendum D)

All deployment analyses are retrospective simulations on published runs: a study that was not used for training plays the role of a new laboratory, and its reported runs play the role of the experiments it would perform. The learner was the STRATA base learner with base and protocol features, and the nominal miscoverage was α = 0.10.

*Sequential local adaptation (E15).* For every unseen study with at least 11 runs, the runs were put in an order and the first *k* ∈ {0, 1, 2, 3, 5} were treated as measured (support runs). The runs from position 6 onward formed a fixed query set, identical for all *k*, so that support and query runs never overlap. Three orders were used: a *screening design* (main analysis) — first the run whose temperature is closest to the study's median temperature, then the lowest- and the highest-temperature runs, and further runs by maximin distance in standardised temperature and log residence time; the *reported order* of the runs in the database, which follows the source tables and is not chronological; and 20 *random* orders. Three strategies predicted the query runs: A, the literature model without adaptation; B, STRATA, the literature model shifted by the shrunk mean residual of the *k* support runs (Section 2.5); and C, local only, the mean of the *k* support runs. For each strategy, order and *k*, the 90% interval was calibrated by applying exactly the same procedure — same order rule, same *k*, same query definition — to the calibration studies (out-of-study predictions for A and B, observed yields for C) and taking the study-weighted quantile of the absolute query residuals. Metrics were per-study RMSE and MAE on the query runs, study-weighted coverage and mean interval width. The evaluation was run on unseen development studies (study-grouped ten-fold CV, three seeds), once on the locked studies, and on the external hydrochar database (solid yield; feedstock series as pseudo-studies; base features; model trained on all development studies). B was compared with A and with C at each *k* by two-sided Wilcoxon signed-rank tests on per-study RMSE, with Holm correction within each setting × target × order.

*Decision support (E16).* (a) An applicability-domain (AD) score was computed for each study as the median, over its runs, of the mean Euclidean distance to the five nearest training runs in standardised base features. The threshold was fixed in advance as the 95th percentile of the scores of development studies in out-of-study folds; hypothesis D1 was that locked studies above the threshold have a larger error of strategy A (one-sided Mann–Whitney test). (b) The number of local runs needed for a target 90% half-width *h* ∈ {10, 15, 20} wt% was read from the development results of strategy B (screening-design order) and checked for coverage on the locked studies. (c) The rule "use C if a study is flagged, otherwise B" was compared with always using B on the locked studies at *k* = 3 (D2).

*Laboratory case studies (E17).* For each target, the locked study with at least 11 runs and the largest number of distinct temperatures (ties broken by the number of runs) was selected by rule before results were inspected. Its runs were measured one at a time in screening-design order, and after each run all remaining runs were predicted by A, B and C with intervals calibrated as in E15 (remaining-runs query definition). Reported are the error after each run, interval width and coverage, and the regret of choosing the remaining run with the highest predicted yield (best observed yield minus observed yield of the chosen run). Because B adds a constant offset, it ranks runs exactly as A does.

## 2.7. Further analyses

E1/E2 (accuracy and baselines) compared twelve learners under random-row and study-grouped CV with both feature sets. E3 (STRATA) produced the heterogeneity decomposition, the row- versus study-calibrated interval comparison and the earlier *k*-shot evaluation with random support sets (Supplementary Table S10). Robustness (E4: input noise, fewer training studies), generalisation (E5: locked studies, studies published after 2018 predicted from earlier ones, leave-one-feedstock-family-out, external database), cost (E6, E11), sensitivity (E7: α, $\tau^2$ estimator, number of folds, tuning) and error analysis by subgroup (E8) followed the registered protocol. E9 (STRATA with six other base learners), E10 (cross-study duplicate audit) and E11 were added during internal review after the main results were known and are reported as such. Addenda A, A2, B and C tested whether within-study *changes* transfer better than absolute yields: within-study contrasts $\Delta_{ab} = y_a - y_b$, in which a study offset cancels, were predicted by the absolute model, a within-study-centred model and a pairwise-difference model (Tynes et al., 2021); model-free temperature slopes were computed from pairs of runs of the same study that differ only in temperature (E13, descriptive, not pre-registered); and the run predicted to give the highest yield was compared with rules of thumb (E14, exploratory, then tested once on locked studies). Details are given in Supplementary Section S7.

## 2.8. Statistical analysis

The unit of analysis for all inference was the source study. Learners and STRATA variants were compared through per-study RMSE (averaged over seeds) with the Wilcoxon signed-rank test (Wilcoxon, 1945); families of comparisons were corrected with Holm's step-down procedure as described by Demšar (2006). Effect sizes are the median paired difference with a 95% bootstrap CI over studies and the matched-pairs rank-biserial correlation. One-sided tests were used only for directional hypotheses registered in advance (P reduces error; SC coverage exceeds RC coverage). Coverage was summarised both over runs and with equal study weights, with 95% cluster-bootstrap CIs; on development folds, point estimates average the three outer seeds and CIs were computed for the first seed. Statistical significance is claimed only for Holm-adjusted *p* < 0.05.

## 2.9. Software and availability of code

All analyses ran on a 4-core CPU without GPU using Python 3.13, scikit-learn, LightGBM, XGBoost, CatBoost, GPBoost, statsmodels and SciPy (exact versions recorded with the code). A single command regenerates every number, table and figure from the public data; a quick mode verified the whole pipeline in 12 minutes, and the full analysis reproduced every value in this article. All values reported in this article are inserted programmatically from the generated result files. The code, the locked study list, the configuration files and the result files are available from the corresponding author on reasonable request.


# 3. Results and discussion

## 3.1. Random splits overstate accuracy for new studies

Fig. 2 summarises the study design. Under random-row CV the gradient-boosting learners reproduced the accuracy typically reported in the literature (best bio-oil R² = 0.82, RMSE = 7.6 wt%, LightGBM; best solid-yield RMSE = 7.0 wt%) (Table 3, Fig. 3). When every study was predicted by a model that had not seen it, RMSE roughly doubled for the flexible learners: the ratio of study-grouped to random-row RMSE ranged from 1.52 to 2.61 for bio-oil (median 2.02) and from 1.50 to 2.28 for solid yield (median 1.97). The best study-grouped RMSE was 15.7 wt% for bio-oil (extra trees, R² = 0.24) and 13.7 wt% for solid yield (LightGBM, R² = 0.54), compared with 18.1 and 20.6 wt% for a model that always predicts the training mean. Ratios close to one were obtained only by learners that fit the data poorly in both schemes (mean predictor, ridge regression, GPBoost); the optimism of random splitting grows with the capacity of a learner to memorise study-specific patterns. Differences between learners under study-grouped CV were small relative to the gap between schemes (9 learners not significantly worse than the best for bio-oil; Supplementary Table S5).


**Table 3.** Random-row versus study-grouped cross-validation on development studies (base features; grouped CV averaged over 3 seeds).

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




![**Fig. 2.** Study design. A locked set of 38 source studies is held out before modelling; all development analyses use study-grouped folds; STRATA adds study-calibrated conformal intervals and *k*-shot empirical-Bayes adaptation to any point predictor.](/home/user/rp_c_12/figures/fig01_workflow.png){width=16cm}



![**Fig. 3.** Root-mean-square error of 12 learners under random-row five-fold CV (circles) and study-grouped ten-fold CV (squares; mean of three seeds), base features.](/home/user/rp_c_12/figures/fig03_random_vs_grouped.png){width=16cm}


## 3.2. Most out-of-study error is a study offset that reported metadata do not explain

For the STRATA base learner (XGBoost), study offsets were large and spread on both sides of zero (Fig. 4). The between-study share of out-of-study residual variance was 0.65 (95% CI 0.53–0.76) for bio-oil and 0.49 (0.40–0.61) for solid yield; the standard deviation of study offsets ($\hat\tau$) was 12.5 and 9.7 wt%, against within-study residual standard deviations ($\hat\sigma_w$) of 9.3 and 9.9 wt% (Table 4). A model that is well calibrated on average can therefore be biased by more than 10 wt% for an individual laboratory, and errors for runs of the same study are strongly correlated.

However, adding the parsed work-up and reporting descriptors (P) did not significantly reduce the error for unseen studies for either target after Holm correction. Adding the protocol descriptors changed the median per-study RMSE from 12.45 to 12.84 wt% for bio-oil (one-sided Wilcoxon *p* = 0.804; *n* = 122 studies) and from 10.86 to 11.05 wt% for solid yield (*p* = 0.545). A ridge meta-regression of the study offsets on study-level descriptors had no out-of-study predictive value (leave-one-study-out R² = -0.031 and -0.047), and offsets did not differ significantly between the dominant extraction solvents (Kruskal–Wallis *p* = 0.104 for bio-oil; Kruskal–Wallis *p* = 0.951 for solids). Either work-up conventions matter less than unrecorded details (feedstock batch, particle size, heat-up, quenching, product handling), or the coarse descriptors that can be parsed from publications — 23% of development bio-oil runs named no extraction solvent — are too noisy to reveal their effect. In both cases the offset of a new laboratory is not predictable from what studies currently report: it must be represented in the uncertainty (Section 3.3) or measured (Section 3.4).


**Table 4.** Decomposition of out-of-study error and contribution of work-up/reporting descriptors (P).

| Target | τ² (between) | σ²w (within) | Between-study share [95% CI] | Median study RMSE base → base+P | Δ median [95% CI]; p (one-sided) | Rank-biserial | Meta-regression LOSO R² (perm. p) |
|---|---|---|---|---|---|---|---|
| Bio-oil | 156.7 | 85.6 | 0.65 [0.53, 0.76] | 12.45 → 12.84 | 0.04 [-0.38, 0.60]; 0.804 | 0.09 | -0.031 (0.714) |
| Solid | 94.6 | 97.7 | 0.49 [0.40, 0.61] | 10.86 → 11.05 | 0.05 [-0.15, 0.25]; 0.545 | 0.01 | -0.047 (0.910) |




![**Fig. 4.** Mean out-of-study residual (observed − predicted) of each development study with 95% intervals of the mean, STRATA base learner with base features. The annotated share is the between-study fraction of residual variance with its study-cluster bootstrap CI.](/home/user/rp_c_12/figures/fig04_study_offsets.png){width=16cm}


## 3.3. Study-calibrated intervals keep their coverage for new studies, at the price of width

Intervals calibrated on randomly held-out runs are narrow because the residuals of seen studies omit the study offset. For unseen development studies, nominal 90% row-calibrated intervals covered 0.57 (bio-oil; 95% CI 0.52–0.64) and 0.61 (solids) of runs with equal study weights, and 66% and 66% of studies had coverage below 0.80 (Table 5, Fig. 5). Calibrating on out-of-study residuals with equal study weights gave 0.91 (0.87–0.94) and 0.91 (one-sided Wilcoxon on per-study coverage, *p* < 0.001 and < 0.001). The same pattern held for α = 0.05 and 0.20, with 5 instead of 10 outer folds (Supplementary Table S6), and on the locked test studies (bio-oil RC 0.60 vs SC 0.89; solids RC 0.46 vs SC 0.82), for left-out feedstock families (mean) (bio-oil RC 0.55 vs SC 0.89; solids RC 0.60 vs SC 0.90), for temporally later studies (bio-oil RC 0.42 vs SC 0.85; solids RC 0.56 vs SC 0.90), on the external hydrochar database (solids RC 0.55 vs SC 0.92).

Interval width is the central quantity for a laboratory, because it states how much the prediction can be trusted before any experiment. Study-calibrated intervals were 59.1 wt% wide for bio-oil and 46.7 wt% for solids, against 22.8 and 20.6 wt% for row-calibrated ones — an honest half-width of roughly ±30 wt% for the bio-oil yield of a new study, which rules out fine-grained optimisation from literature data alone. With seven base learners (E9; Supplementary Table S14), study-calibrated coverage was 0.90–0.91 for bio-oil with every learner, including the training mean, whereas row-calibrated coverage fell with learner capacity from 0.86 (mean predictor) to 0.55–0.59 (tree ensembles): flexible learners absorb the offsets of studies they have seen. Relative to the 'no-ML' reference, the best learner narrowed valid intervals by 15% for bio-oil and 23% for solids — a real but modest gain. An exploratory, post-hoc variant with locally adaptive widths (Supplementary Section S4) did not narrow the intervals (mean width 63.0 vs 59.1 wt% for bio-oil) and worsened the interval score, consistent with an error dominated by an unpredictable study offset.


**Table 5.** Empirical coverage of 90% prediction intervals: row-calibrated (RC) vs study-calibrated (SC).

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




![**Fig. 5.** Study-weighted empirical coverage of nominal 90% prediction intervals calibrated on random rows (RC) or on studies (SC) across validation settings, including left-out feedstock families, later studies, locked studies and the external database (base + P features). Dashed line: nominal level.](/home/user/rp_c_12/figures/fig05_coverage.png){width=16cm}


## 3.4. Sequential local adaptation: literature, literature plus local runs, or local runs only

Table 6 and Fig. 6 show what a new laboratory would have obtained after measuring *k* runs in the screening-design order. For unseen development studies, STRATA (B) was more accurate than the literature model alone (A) and than the local runs alone (C) at every *k* and for both targets (8 of 8 and 8 of 8 Holm-corrected comparisons significant; Supplementary Table S23). For bio-oil, the median per-study RMSE fell from 12.4 wt% (A) to 8.8, 8.8 and 8.4 wt% with one, three and five runs, against 10.4, 9.9 and 9.5 wt% for C; for solids, from 9.4 to 8.8, 7.8 and 7.7 wt% (C: 11.2, 10.5, 10.0 wt%). The first run carried most of the gain for bio-oil (3.5 wt%), whereas for solids the error fell more gradually (0.6 wt% after one run, 1.6 wt% after three). Study-weighted coverage of the re-calibrated intervals stayed at 0.94 (bio-oil) and 0.89 (solids) at *k* = 3, and the half-width shrank from ±30.4 to ±22.2 wt% (bio-oil) and from ±22.8 to ±19.1 wt% (solids). Local-only intervals were wider than those of B at every *k*, because a mean of one to five runs says nothing about how yields vary with conditions.


**Table 6.** Retrospective simulated deployment (E15): a new laboratory measures k runs in screening-design order, and the runs from position 6 onward are predicted by A (literature model only), B (STRATA: literature model shifted by the shrunk mean residual of the k runs) or C (mean of the k local runs). RMSE: median per-study RMSE (wt%); Cov.: study-weighted coverage of 90% intervals re-calibrated for each k and strategy; ±HW: mean interval half-width (wt%). Dev.: unseen development studies in study-grouped CV (3 seeds); Locked: studies held out before modelling (≥ 11 runs); 4TU: external hydrochar database (feedstock series as pseudo-studies). MAE is given in the supplementary deployment table.

| Setting | Target | k | Studies | RMSE A | RMSE B | RMSE C | Cov. A | Cov. B | Cov. C | ±HW A | ±HW B | ±HW C |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Dev. | Bio-oil | 0 | 80 | 12.4 | — | — | 0.94 | — | — | 30.4 | — | — |
| Dev. | Bio-oil | 1 | 80 | 12.4 | 8.8 | 10.4 | 0.94 | 0.94 | 0.93 | 30.4 | 24.6 | 31.0 |
| Dev. | Bio-oil | 3 | 80 | 12.4 | 8.8 | 9.9 | 0.94 | 0.94 | 0.92 | 30.4 | 22.2 | 24.8 |
| Dev. | Bio-oil | 5 | 80 | 12.4 | 8.4 | 9.5 | 0.94 | 0.92 | 0.92 | 30.4 | 21.0 | 23.3 |
| Dev. | Solid | 0 | 72 | 9.4 | — | — | 0.89 | — | — | 22.8 | — | — |
| Dev. | Solid | 1 | 72 | 9.4 | 8.8 | 11.2 | 0.89 | 0.9 | 0.9 | 22.8 | 19.8 | 27.9 |
| Dev. | Solid | 3 | 72 | 9.4 | 7.8 | 10.5 | 0.89 | 0.89 | 0.89 | 22.8 | 19.1 | 24.5 |
| Dev. | Solid | 5 | 72 | 9.4 | 7.7 | 10.0 | 0.89 | 0.89 | 0.88 | 22.8 | 17.0 | 21.4 |
| Locked | Bio-oil | 0 | 19 | 10.3 | — | — | 0.9 | — | — | 29.0 | — | — |
| Locked | Bio-oil | 1 | 19 | 10.3 | 8.2 | 6.4 | 0.9 | 0.97 | 1.0 | 29.0 | 24.4 | 31.1 |
| Locked | Bio-oil | 3 | 19 | 10.3 | 8.0 | 6.0 | 0.9 | 0.92 | 1.0 | 29.0 | 21.7 | 24.4 |
| Locked | Bio-oil | 5 | 19 | 10.3 | 7.3 | 6.3 | 0.9 | 0.94 | 0.99 | 29.0 | 20.5 | 22.9 |
| Locked | Solid | 0 | 18 | 13.4 | — | — | 0.85 | — | — | 22.6 | — | — |
| Locked | Solid | 1 | 18 | 13.4 | 7.7 | 9.9 | 0.85 | 0.8 | 0.9 | 22.6 | 18.7 | 27.7 |
| Locked | Solid | 3 | 18 | 13.4 | 7.1 | 8.5 | 0.85 | 0.84 | 0.89 | 22.6 | 19.3 | 24.7 |
| Locked | Solid | 5 | 18 | 13.4 | 6.9 | 8.1 | 0.85 | 0.86 | 0.9 | 22.6 | 17.1 | 21.4 |
| 4TU | Solid | 0 | 14 | 11.6 | — | — | 0.96 | — | — | 22.6 | — | — |
| 4TU | Solid | 1 | 14 | 11.6 | 9.4 | 8.7 | 0.96 | 0.95 | 0.97 | 22.6 | 18.7 | 27.7 |
| 4TU | Solid | 3 | 14 | 11.6 | 6.3 | 8.0 | 0.96 | 0.94 | 0.94 | 22.6 | 18.2 | 24.7 |
| 4TU | Solid | 5 | 14 | 11.6 | 6.3 | 7.9 | 0.96 | 0.92 | 0.93 | 22.6 | 16.6 | 21.4 |



On held-out data the picture was more differentiated. For the locked solid studies, B reduced the median error from 13.4 to 7.7 wt% with one run and 7.1 wt% with three (B vs A, Holm *p* = 0.014 at *k* = 3), and on the external hydrochar database from 11.6 to 6.3 wt% (Holm *p* = 0.100, not significant; 14 pseudo-studies); B was not significantly different from C in either setting after correction except for the external database at *k* = 2 (*p* = 0.042). For the locked bio-oil studies, however, the local runs alone were more accurate than STRATA: median RMSE 6.0 (C) vs 8.0 wt% (B) at *k* = 3 (Holm *p* = 0.009; also at *k* = 2, *p* = 0.010), and B was not significantly better than A (10.3 wt%). Why literature anchoring did not help for these 19 studies could not be established. Their yields varied somewhat less within a study (median within-study SD 6.4 vs 8.0 wt% for the development studies), which favours a local mean, but the locked solid studies showed a similar difference (7.0 vs 8.7 wt%) without the same effect. Coverage of B on locked studies was 0.92 (bio-oil) and 0.84 (solids) at *k* = 3 — below nominal for solids, as for the unadapted intervals (Section 3.7). The same conclusions held for random run orders and, with smaller differences, for the reported order (Supplementary Table S22).

Fig. 7 shows the effect at run level for the locked studies. Pooled over all query runs, the RMSE was 21.7 wt% for A, 10.4 wt% for B and 7.7 wt% for C with three runs (bio-oil), and 16.4, 10.9 and 13.2 wt% (solids); run-level coverage was 0.81 (A) and 0.95 (B) for bio-oil and 0.91 and 0.91 for solids. The large pooled error of A comes from a few studies whose yields lie far from the bulk of the training data; anchoring removes most of their offset, but a constant shift cannot correct a within-study pattern that the model gets wrong. The practical reading is that a few local runs are worth more than further model refinement, but whether to combine them with the literature model is an empirical question for each laboratory: across the five target × setting combinations, B had a lower median error than C at every *k* ≥ 2 in four, and C had the lower median error in one (locked bio-oil studies).


![**Fig. 6.** Retrospective simulated deployment (screening-design run order). Top: median per-study RMSE of the query runs (runs 6 onward) for the literature model alone (A), STRATA (B: literature model plus the shrunk offset of *k* local runs) and the local runs alone (C). Bottom: half-width of the 90% interval re-calibrated for each strategy and *k*. Development: unseen studies in study-grouped CV; locked: 38 studies held out before modelling; external: 4TU hydrochar database.](/home/user/rp_c_12/figures/fig14_deployment.png){width=16cm}



![**Fig. 7.** Observed versus predicted yields of the query runs of the locked studies with 90% intervals: literature model without local runs (A, *k* = 0) and STRATA after three screening-design runs (B, *k* = 3). Titles give run-level coverage.](/home/user/rp_c_12/figures/fig17_pred_obs_intervals.png){width=16cm}


## 3.5. Decision support: can a laboratory tell in advance, and how many runs does it need?

The applicability-domain score ranked the risk of a large error: for development studies its Spearman correlation with the error of the unadapted model was 0.46 for bio-oil (*p* = 1.8 × 10^−5^; 80 studies) and 0.49 for solids (*p* = 1.2 × 10^−5^) (Table 7). The pre-registered threshold, however, flagged 0 of 28 locked bio-oil studies and 0 of 30 locked solid studies (largest scores 4.62 and 5.09 against thresholds 5.69 and 5.93), so hypothesis D1 could not be tested and the rule "use local runs if flagged" reduced to always using STRATA. In an exploratory analysis added after this result, the score still correlated with the error on locked bio-oil studies (ρ = 0.55, *p* = 0.02; 19 studies) but not on locked solid studies (ρ = 0.25, *p* = 0.32). The score did not identify the locked bio-oil studies for which local runs alone were better (Section 3.4): being close to the training data in feedstock and conditions does not guarantee that a laboratory's yields behave like the literature average. A laboratory should therefore not rely on a distance-based flag alone but compare literature-anchored and local-only predictions once its first runs are available, as STRATA-Lab prescribes (Fig. 1).

How many runs are needed depends on the precision required. With STRATA, the development half-width of the 90% interval was ±30.4, ±24.6, ±23.9, ±22.2 and ±21.0 wt% for bio-oil after 0, 1, 2, 3 and 5 runs, and ±22.8, ±19.8, ±19.5, ±19.1 and ±17.0 wt% for solids. A half-width of ±20 wt% was reached for solids after 1 run (locked coverage 0.80, median RMSE 7.7 wt%) but for bio-oil not within five runs, and ±10 or ±15 wt% was not reached for either target. Literature-trained models anchored by a few runs therefore support screening — deciding whether a feedstock is promising and which temperature region to explore — but not the optimisation of conditions to within a few wt%, which requires a local experimental design.


**Table 7.** Decision support for a new laboratory (E16): applicability-domain (AD) score, pre-registered threshold and the number of local runs needed for a target 90% interval half-width. Exploratory items were added after the pre-registered threshold flagged no locked study.

| Target | Item | Result |
|---|---|---|
| Bio-oil yield | Applicability-domain score vs out-of-study error (development; Spearman ρ) | ρ = 0.46 (p = 1.8e-05; 80 studies) |
| Bio-oil yield | Pre-registered threshold (95th percentile of development scores) on locked studies | 0 of 28 locked studies flagged (max score 4.62 vs threshold 5.69); test D1 not possible |
| Bio-oil yield | Exploratory: score vs error on locked studies (Spearman ρ) | ρ = 0.55 (p = 0.02; 19 studies) |
| Bio-oil yield | STRATA 90% half-width after k local runs (development; k = 0, 1, 2, 3, 5) | ±30.4, ±24.6, ±23.9, ±22.2, ±21.0 wt% |
| Bio-oil yield | Local runs needed for a 90% half-width ≤ ±10 wt% | not reached within 5 local runs |
| Bio-oil yield | Local runs needed for a 90% half-width ≤ ±15 wt% | not reached within 5 local runs |
| Bio-oil yield | Local runs needed for a 90% half-width ≤ ±20 wt% | not reached within 5 local runs |
| Solid yield | Applicability-domain score vs out-of-study error (development; Spearman ρ) | ρ = 0.49 (p = 1.2e-05; 72 studies) |
| Solid yield | Pre-registered threshold (95th percentile of development scores) on locked studies | 0 of 30 locked studies flagged (max score 5.09 vs threshold 5.93); test D1 not possible |
| Solid yield | Exploratory: score vs error on locked studies (Spearman ρ) | ρ = 0.25 (p = 0.32; 18 studies) |
| Solid yield | STRATA 90% half-width after k local runs (development; k = 0, 1, 2, 3, 5) | ±22.8, ±19.8, ±19.5, ±19.1, ±17.0 wt% |
| Solid yield | Local runs needed for a 90% half-width ≤ ±10 wt% | not reached within 5 local runs |
| Solid yield | Local runs needed for a 90% half-width ≤ ±15 wt% | not reached within 5 local runs |
| Solid yield | Local runs needed for a 90% half-width ≤ ±20 wt% | k = 1 (development median RMSE 8.8; locked coverage 0.80, median RMSE 7.7) |



## 3.6. Laboratory case studies

The pre-specified rule selected, among 19 eligible locked bio-oil studies, the HTL of *Spirulina platensis* (68 runs at 14 temperatures; doi:10.1016/j.energy.2020.117550) and, among 18 eligible locked solid studies, the HTC of duckweed (*Lemna* sp.; 25 runs at 10 temperatures; doi:10.1016/j.biortech.2012.08.106) (Table 8, Fig. 8). The two cases illustrate the two regimes found in Section 3.4.

For the microalga, the literature model without local runs had an RMSE of 10.2 wt% with intervals of ±27.4 wt% that covered all runs. The first screening run (340 °C) gave 36.7 wt%, well above both the model's 18.9 wt% and the study's median of 22.6 wt%; shifting the model by this offset made STRATA worse (17.3 wt%, coverage 0.78), and it remained worse than the literature model up to five runs (12.2 wt%) before converging at about ten (9.5 wt%). The local mean of the first runs was more accurate than both from the second run onward (8.0 wt% at *k* = 2, 7.6 wt% at *k* = 5), because the literature model's run-to-run pattern did not match this study (correlation between predicted and observed yields across its runs -0.27), so that a study mean was the better predictor. For duckweed HTC, the literature model was already accurate (5.7 wt%); STRATA kept the error at 5.2–5.7 wt% with full coverage while its half-width narrowed from ±23.4 to ±17.3 wt% after five runs, whereas the local mean was poor (10.3–21.0 wt%; predicted and observed yields correlated at 0.84 across the runs of this study, so the model's temperature pattern carried real information). The database records one run of this study at 20 °C (78.3 wt% solid), which the screening design selected as the lowest-temperature run; it is retained as recorded, it inflates the local mean at *k* = 2–3, and it makes the regret of the model-chosen run trivially zero at *k* = 0–1. Choosing the run with the highest predicted yield gave a regret of 10.4 wt% for bio-oil (random choice 16.2 wt%) and, once the 20 °C entry had been measured, 11.0 wt% for solids (random 12.8 wt%) — at best modestly better than chance, consistent with Section 3.8.


**Table 8.** Laboratory case studies (E17): one locked study per target selected by a pre-specified rule (≥ 11 runs, most distinct temperatures). Runs are measured one at a time in screening-design order; all remaining runs are predicted. Regret: best observed yield among the remaining runs minus the observed yield of the run predicted to be best (A and B rank runs identically because B adds a constant offset); random: expected regret of a random choice. RMSE, ±HW (90% half-width of B) and regret in wt%; Cov. B: coverage of the remaining runs by the interval of B.

| Case | k | Runs predicted | RMSE A | RMSE B | RMSE C | Cov. B | ±HW B | Regret A/B | Regret random |
|---|---|---|---|---|---|---|---|---|---|
| Bio-oil, Spirulina HTL | 0 | 68 | 10.19 | 10.19 |  | 1.0 | 27.39 | 10.4 | 16.16 |
| Bio-oil, Spirulina HTL | 1 | 67 | 10.03 | 17.32 | 16.31 | 0.78 | 21.74 | 10.4 | 16.37 |
| Bio-oil, Spirulina HTL | 2 | 66 | 10.1 | 12.77 | 8.01 | 0.92 | 22.09 | 10.4 | 16.23 |
| Bio-oil, Spirulina HTL | 3 | 65 | 10.08 | 13.96 | 8.44 | 0.8 | 19.1 | 10.4 | 16.31 |
| Bio-oil, Spirulina HTL | 5 | 63 | 9.74 | 12.24 | 7.56 | 0.89 | 19.5 | 10.4 | 16.29 |
| Bio-oil, Spirulina HTL | 10 | 58 | 9.7 | 9.52 | 8.02 | 0.91 | 17.54 | 10.4 | 15.62 |
| Solid, duckweed HTC | 0 | 25 | 5.68 | 5.68 |  | 1.0 | 23.36 | 0.0 | 41.84 |
| Solid, duckweed HTC | 1 | 24 | 5.72 | 5.16 | 10.3 | 1.0 | 20.57 | 0.0 | 41.68 |
| Solid, duckweed HTC | 2 | 23 | 5.71 | 5.97 | 21.0 | 1.0 | 19.65 | 11.0 | 12.89 |
| Solid, duckweed HTC | 3 | 22 | 5.82 | 5.71 | 13.87 | 1.0 | 18.83 | 11.0 | 12.83 |
| Solid, duckweed HTC | 5 | 20 | 5.78 | 5.21 | 9.33 | 1.0 | 17.28 | 10.8 | 12.91 |
| Solid, duckweed HTC | 10 | 15 | 6.01 | 5.65 | 6.6 | 1.0 | 17.26 | 7.1 | 13.27 |




![**Fig. 8.** Laboratory case studies (locked studies selected by a pre-specified rule). Observed yields (black), literature model without local runs (A, grey, with 90% intervals), STRATA after the three circled screening-design runs (B, blue) and the local mean of those runs (C, dashed line with its 90% band).](/home/user/rp_c_12/figures/fig15_case_study.png){width=16cm}


## 3.7. Generalisation across studies, time, feedstock families and databases

The locked test studies, evaluated once after all modelling decisions had been frozen, gave a more pessimistic picture than development CV. For bio-oil yield (556 runs, 28 studies) the STRATA base learner reached RMSE = 18.3 wt% (R² = -0.95; best learner k-nearest neighbours, 12.9 wt%; mean predictor 13.6 wt%); for solid yield (457 runs, 30 studies) the STRATA base learner reached RMSE = 18.5 wt% (R² = 0.30; best learner MLP, 14.4 wt%; mean predictor 23.0 wt%). For bio-oil, only 4 of the 11 non-trivial learners had a lower pooled RMSE than the mean predictor, although 6 had a lower median per-study RMSE: pooled errors were dominated by a few studies outside the bulk of the training distribution — for XGBoost, a single solvothermal series of 90 runs contributed 54% of the squared error, and excluding it (post hoc) lowered the RMSE from 18.3 to 13.6 wt% (R² = 0.00). Study-weighted coverage of row-calibrated 90% intervals was 0.60 (95% CI 0.47–0.73) for bio-oil and 0.46 (95% CI 0.34–0.58) for solids; study-calibrated intervals reached 0.89 (95% CI 0.81–0.97) and 0.82 (95% CI 0.70–0.92) (Table 9, Fig. 5). Study calibration thus removed most, but for solids not all, of the under-coverage; with 28–30 locked studies the intervals are wide, and the solid-yield shortfall reflects a few studies with feedstocks (technical lignin, plastic–biomass blends) that are rare in the training data.


**Table 9.** Single evaluation on the 38 locked test studies (models trained on all development studies, base features).

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



Predicting studies published after 2018 from earlier studies gave RMSE = 19.4 (bio-oil; higher than the study-grouped CV value of 15.8 wt%) and 16.5 wt% (solids; higher than 14.1 wt%), i.e. models trained on older literature transfer no better to newer studies than to randomly chosen unseen studies. Leaving out one feedstock family at a time gave mean RMSE of 17.2 and 16.3 wt%, with the largest errors for the 'Other' category (bio-oil, 32.6 wt%) and 'Other' (solids, 29.8 wt%). On the independent 4TU hydrochar database (502 runs after removing 36 potential duplicates; 69 feedstock series), a solid-yield model trained on all development studies reached RMSE = 13.3 wt% (R² = 0.31), whereas training on the 16 HTC development studies alone gave 16.7 wt% (R² = -0.08), showing that the small HTC subset of the primary database does not by itself support transfer to other HTC compilations (Supplementary Table S11). Coverage of study-calibrated intervals across these settings is shown in Fig. 5. Adding Gaussian noise of 20% of the training standard deviation to continuous test features increased the bio-oil RMSE from 15.7 to 16.6 wt% and the solid RMSE from 13.9 to 15.4 wt%, while SC coverage was 0.90 without and 0.90 with noise (bio-oil) — the error budget for unseen studies is dominated by the study offset, not by input noise. Training on 25% instead of all training studies raised the bio-oil RMSE from 15.7 to 20.3 wt%, and SC coverage remained 0.89, whereas RC coverage stayed at 0.45–0.56 (Supplementary Fig. S6). All learners trained in at most 9 s on one CPU thread (MLP); the STRATA base learner took 0.2 s and predicted 1,000 runs in 4 ms (Supplementary Table S20, Supplementary Fig. S7). The complete STRATA procedure — two inner five-fold cross-validations, quantiles, variance components and k-shot quantiles for all k — took 2.3–7.0 s on all development studies, against 0.3–0.5 s for fitting the base learner alone (measured, 1 and 4 threads); this overhead is negligible compared with the cost of a single hydrothermal experiment.

Because literature compilations can contain the same experiment reported in several papers, the development data were audited (E10): 166 bio-oil runs (7.3%, 16 studies) and 143 solid-yield runs (6.6%) had an identical counterpart in another study. Removing them increased the study-grouped RMSE of the STRATA base learner from 15.8 to 16.6 wt% (bio-oil) and from 14.1 to 14.6 wt% (solids); cross-study duplicates therefore make study-grouped estimates slightly optimistic and do not affect the conclusions. Out-of-study errors were largest for Other feedstocks among families (bio-oil RMSE 33.9 wt%, 6 studies), for the ≤250 °C temperature band (21.1 wt%) and for HTL solvothermal runs (18.5 wt%) (Supplementary Table S13). The five worst-predicted bio-oil studies had per-study RMSE between 35.1 and 61.4 wt% and absolute mean offsets of 26.7–60.9 wt% (processes: HTL 3, HTC 1, HTL solvothermal 1). Across extraction-solvent groups with at least three studies, the bio-oil RMSE ranged from 10.8 (hydrocarbon) to 19.8 wt% (none named) and the mean residual from -9.5 to +9.7 wt% (Supplementary Fig. S8).

## 3.8. What did not transfer: within-study trends and the choice of conditions

If most of the error for a new laboratory is an offset, *changes* between runs of the same study might transfer even when absolute yields do not. Model-free, laboratories agreed on the direction of the temperature response below 300 °C: bio-oil yield rose by +0.87 wt% per 10 °C at 250–300 °C (same sign in 81% of studies) and solid yield fell (86% same sign) (Supplementary Fig. S1, Supplementary Table S15), but the between-study standard deviation of the bio-oil slope was 2.6 times its median. Contrary to the pre-registered hypotheses, learners did not predict within-study changes better than absolute yields: contrast $R^2_\Delta$ for unseen development studies was 0.14–0.22 for bio-oil and 0.25–0.43 for solids, offset-invariant learners were better than the absolute model in 1 of 12 Holm-corrected comparisons, and anchoring with offset-invariant models did not improve on the STRATA offset (Supplementary Fig. S2, Supplementary Table S16). An exploratory advantage of the models over a 325 °C rule of thumb in choosing the best of a study's planned bio-oil runs was not confirmed on the locked studies (median regret 11.9–12.5 wt% vs 14.6 wt% for the rule; one-sided Holm-corrected *p* = 0.661; Supplementary Fig. S3). Directional knowledge is thus a robust prior for planning, but literature-trained models should not be trusted to quantify the effect of a planned change or to select optimal conditions in a new laboratory.

## 3.9. STRATA-Lab in practice

Table 10 condenses the evidence. Of the capabilities a new laboratory might expect from a literature-trained hydrothermal model, three were supported on held-out studies: honest uncertainty, provided intervals are calibrated across studies; the correction of predictions with a few local runs; and, as a model-free observation, the direction of the temperature effect. Absolute bio-oil yields of a new study were barely predictable, offsets were not explained by reported metadata, within-study changes and rankings did not transfer, the applicability-domain threshold flagged no failing study, and for one held-out set the local runs alone outperformed literature anchoring.


**Table 10.** What literature-trained hydrothermal models can and cannot do for a new study (development: unseen studies in study-grouped CV; locked: 38 studies held out before modelling).

| Capability | Development studies (unseen) | 38 locked studies | Verdict |
|---|---|---|---|
| Predict the absolute yield of a run in a new study | best R² 0.24 (bio-oil), 0.54 (solid) | best R² 0.03 (bio-oil), 0.57 (solid) | Poor (bio-oil); moderate (solid) |
| Explain a study's offset from reported work-up / yield basis | P ablation p = 0.80, 0.54; meta-regression R² -0.03, -0.05 | 0 of 24 learner–target tests significant | No |
| Predict how yield changes between two runs of a new study (within-study contrast) | contrast R² 0.14–0.21 (bio-oil), 0.37–0.43 (solid); offset-invariant models better in 1/12 tests | contrast R² -0.30–0.30 (bio-oil), 0.43–0.56 (solid) | Weak; not better than levels (pre-registered T1–T3 not supported) |
| Direction of the temperature effect below 300 °C (model-free, within studies) | same sign in 81%–95% of studies (bio-oil ↑, solid ↓) | not applicable (descriptive) | Consistent across laboratories |
| Pick the best of a new study's planned runs (bio-oil) | better than T≈325 °C rule (median regret 7.0–8.7 vs 12.8 wt%; exploratory) | not confirmed (p_Holm ≥ 0.62; regret 11.9–12.5 vs 14.6 wt%) | Not established |
| Honest 90% prediction intervals for a new study | row-calibrated 0.57/0.61; study-calibrated 0.91/0.91 | row-calibrated 0.60/0.46; study-calibrated 0.89/0.82 | Yes, if calibrated across studies (wide: ±23–30 wt%) |
| Use 1–3 measured runs of the new study to correct predictions | median study RMSE 12.4→8.5 (bio-oil), 11.1→7.7 (solid) with 3 runs | median study RMSE 10.9→7.8 (bio-oil), 14.2→7.4 (solid) | Yes — error and interval width fall with each run |
| Combine 1–3 screening-design runs with the literature model (STRATA, B) instead of using them alone (C) | k = 3: B 8.8 vs C 9.9 (bio-oil), 7.8 vs C 10.5 wt% (solid); B better at every k | k = 3: B 8.0 vs C 6.0 (bio-oil, C better), B 7.1 vs C 8.5 wt% (solid, n.s.) | Usually yes; not for locked bio-oil studies, where local runs alone were better |
| Flag in advance a study for which the literature model will mislead (applicability-domain score) | Spearman ρ with error 0.46 (bio-oil), 0.49 (solid) | pre-registered threshold flagged 0 and 0 studies | Ranks risk, but the pre-registered threshold detected no failing study |



A laboratory starting with a new feedstock can therefore proceed as follows (Fig. 1). (1) Obtain the literature prediction with a study-calibrated interval (about ±30.4 wt% for bio-oil and ±22.8 wt% for solid yield) and read it as a screening statement, not as an optimum. (2) Compute the applicability-domain score; a high score is a warning, but a low score is no guarantee. (3) Measure one to three runs in a screening design — centre, lowest and highest temperature of the intended window. (4) Compare the STRATA prediction with the local mean of these runs; where they diverge, as for the locked bio-oil studies and the microalga case, weight the local evidence and extend the local design rather than the model. (5) Report predictions with the re-calibrated intervals and the number of runs on which they rest. Table 11 lists the corresponding minimum validation and reporting practice for authors and reviewers of literature-trained bioresource models. Monetary savings were not estimated, because experimental costs vary too widely between laboratories for a general figure to be meaningful.


**Table 11.** Minimum validation and reporting checklist for literature-trained bioresource surrogates intended for use by a new laboratory.

| Item | Minimum practice | Why (evidence in this study) |
|---|---|---|
| 1. Splitting unit | Hold out whole source studies (or laboratories); report random-split metrics only as a reference | Random splits overstated accuracy about two-fold (Section 3.1) |
| 2. Locked test | Fix a list of held-out studies before modelling and evaluate it once | Locked results differed from development CV (Section 3.7) |
| 3. Duplicates | Audit identical runs reported in several studies before splitting | ~7 % of runs were cross-study duplicates (Section 3.7) |
| 4. Accuracy metrics | Report per-study errors and the mean-predictor baseline next to pooled R² | Pooled metrics were dominated by a few studies (Section 3.7) |
| 5. Uncertainty | Calibrate prediction intervals across studies, not across random runs | Row-calibrated 90 % intervals covered 0.46–0.61 (Section 3.3) |
| 6. Trend / optimum claims | Support claims about effects of conditions or optimal conditions with held-out-study contrasts or rankings | Within-study changes and rankings did not transfer (Section 3.8) |
| 7. Local anchoring | Plan 1–3 local runs in a screening design; report literature-only, anchored and local-only predictions with re-calibrated intervals | Three screening-design runs reduced the median error by 1.6–6.4 wt%, but local-only data were better for locked bio-oil studies (Sections 3.4–3.6) |
| 8. Metadata | Record product-recovery solvent, yield basis, fraction definitions, mass-balance closure and reactor details in curated databases | Coarse parsed descriptors did not explain offsets (Section 3.2) |
| 9. Openness | Make code, the held-out study list and per-run predictions available (openly or on request) | Enables re-analysis of the above |



## 3.10. Limitations

All validation is retrospective: published runs of held-out studies played the role of a new laboratory's experiments, and no new experiments were performed. The reported order of runs in the database follows the source tables and is not the chronological order of the experiments; the screening-design order is an idealisation of how a laboratory would choose its first runs, and a laboratory that chooses runs differently may see different gains. The study relies on one curated literature database, whose extraction and harmonisation choices, imputed feedstock fractions and residual transcription errors (for example, the 20 °C entry of the solid-yield case study) propagate into all results. Only bio-oil and solid yields were modelled; aqueous and gas phases, product quality and mass closure were not. Study-level conformal validity assumes that a new study is exchangeable with the calibration studies; studies that differ systematically were under-covered, as the locked solid-yield studies show. The external database lacks study identifiers, so feedstock series were used as pseudo-studies. The applicability-domain threshold flagged no locked study, so its value as a decision rule could not be tested. With 18–19 eligible locked studies per target, the held-out deployment comparisons have limited power. The protocol was registered by timestamped repository commits rather than in a public registry, and several analyses (E9–E11, the adaptive-interval variant and the exploratory locked correlation of the applicability-domain score) were added after results were known.


# 4. Conclusions

Machine-learning models trained on published hydrothermal-conversion data were evaluated as a new laboratory would use them. Random splitting overstated accuracy about two-fold, and most out-of-study error was a study offset that reported work-up descriptors did not explain. Conformal intervals calibrated across studies largely restored coverage for new studies (0.82–0.91, against 0.46–0.61 for row-calibrated intervals) but were ±22.8–30.4 wt% wide. In a retrospective simulated deployment, three runs placed by a screening design and combined with the literature model reduced the median per-study error by 1.6–6.4 wt% and narrowed the intervals; this combination outperformed the local runs alone for unseen development studies, but not for the locked bio-oil studies, and an applicability-domain threshold did not anticipate that case. Within-study trends and the choice of optimal conditions did not transfer. Literature-trained hydrothermal models are therefore screening tools: they should be validated by study, reported with study-calibrated intervals, anchored with a few designed local runs and checked against local-only estimates before they guide experiments in a new laboratory.

# CRediT authorship contribution statement

**P N Bhargav Teja:** Conceptualization, Methodology, Software, Validation, Formal analysis, Investigation, Data curation, Visualization, Writing – original draft, Writing – review & editing. **[Second author name]:** Supervision, Writing – review & editing.

# Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

# Funding

This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.

# Declaration of generative AI and AI-assisted technologies in the manuscript preparation process

During the preparation of this work the authors used an AI assistant (Claude, Anthropic) to search and verify literature metadata, write analysis code, run the computational experiments and draft the manuscript text. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the published article.

# Data availability

All data analysed in this study are publicly available under the CC BY 4.0 licence: the curated hydrothermal treatment/liquefaction database, Version 1.0.0 (RADAR4Chem; https://doi.org/10.22000/8bnbhqccf4aq7kea) (Elfetni, 2026), and the hydrochar database used for external validation (4TU.ResearchData; https://doi.org/10.4121/834c3f22-f46a-4808-a0fe-46298be6a133.v1) (Abdeldayem et al., 2025). The analysis code, the list of locked test studies, configuration files, processed result files and per-run predictions will be made available by the corresponding author on reasonable request.

# Acknowledgements

The authors thank the curators of the hydrothermal treatment/liquefaction database and of the 4TU hydrochar database for releasing their data openly.

# Appendix A. Supplementary data

Supplementary material (Sections S1–S10: literature search, protocol and deviations, additional benchmark and sensitivity results, exploratory adaptive intervals, error analysis by subgroup, STRATA with different base learners, trend and ranking analyses, additional figures, additional deployment results, reproducibility) accompanies this article.

# References

::: {custom-style="Bibliography"}
Abdeldayem, O., Al-Sakkari, E., Ortiz, D., Dupont, C., Ferras, D., Ouali, M.-S., Ragab, A., Kennedy, M., 2025. Database underlying the research for the development of machine learning models for predicting the physicochemical properties of hydrochar [dataset]. 4TU.ResearchData. https://doi.org/10.4121/834c3f22-f46a-4808-a0fe-46298be6a133.v1
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
Tynes, M., Gao, W., Burrill, D.J., Batista, E.R., Perez, D., Yang, P., Lubbers, N., 2021. Pairwise Difference Regression: A Machine Learning Meta-algorithm for Improved Prediction and Uncertainty Quantification in Chemical Search. J. Chem. Inf. Model. 61(8), 3846-3857. https://doi.org/10.1021/acs.jcim.1c00670
:::

::: {custom-style="Bibliography"}
Valdez, P.J., Dickinson, J.G., Savage, P.E., 2011. Characterization of product fractions from hydrothermal liquefaction of Nannochloropsis sp. and the influence of solvents. Energy Fuels 25(7), 3235-3243. https://doi.org/10.1021/ef2004046
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



