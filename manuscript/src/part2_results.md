# 3. Results and discussion

## 3.1. Random splits overstate accuracy for new studies

Fig. 1 summarises the study design and Fig. 2 the data: most studies contributed between a few and a few dozen runs, a few contributed more than 100, and the source studies span four decades. Under random-row CV the gradient-boosting learners reproduced the accuracy typically reported in the literature (best bio-oil R² = {{biooil_best_random_r2}}, RMSE = {{biooil_best_random_rmse}} wt%, {{biooil_best_random_learner}}; best solid-yield RMSE = {{solid_best_random_rmse}} wt%) (Table 2, Fig. 3). When every study was predicted by a model that had not seen it, RMSE roughly doubled for all flexible learners: the ratio of study-grouped to random-row RMSE ranged from {{biooil_ratio_min}} to {{biooil_ratio_max}} for bio-oil (median {{biooil_ratio_median}}) and from {{solid_ratio_min}} to {{solid_ratio_max}} for solid yield (median {{solid_ratio_median}}). The best study-grouped RMSE was {{biooil_best_grouped_rmse}} wt% for bio-oil ({{biooil_best_grouped_learner}}, R² = {{biooil_best_grouped_r2}}) and {{solid_best_grouped_rmse}} wt% for solid yield ({{solid_best_grouped_learner}}, R² = {{solid_best_grouped_r2}}), compared with {{biooil_mean_rmse}} and {{solid_mean_rmse}} wt% for a model that always predicts the training mean. Ratios close to one were obtained only by learners that fit the data poorly in both schemes (mean predictor, ridge regression, GPBoost), i.e. the optimism of random splitting grows with the capacity of a learner to memorise study-specific patterns. Parity plots show that the near-diagonal agreement under random splitting is replaced by wide, partly systematic scatter for unseen studies (Fig. 10).

{{TABLE:table2_benchmark}}

{{FIG:fig01_workflow|Study design. A locked set of 38 source studies is held out before modelling; all development analyses use study-grouped folds; STRATA adds study-calibrated conformal intervals and *k*-shot empirical-Bayes adaptation to any point predictor.}}

{{FIG:fig02_dataset|Development data. (a) Number of runs contributed per source study; (b) yield distributions; (c) publication years of all 188 source studies (dashed line: temporal split).}}

{{FIG:fig03_random_vs_grouped|Root-mean-square error of 12 learners under random-row five-fold CV (circles) and study-grouped ten-fold CV (squares; mean of three seeds), base features.}}

Among learners, differences under study-grouped CV were small relative to the gap between schemes: for bio-oil, {{biooil_n_learners_not_sig_vs_best}} learners were not significantly worse than the best one ({{biooil_best_ref}}) after Holm correction on per-study RMSE (Supplementary Table S3), and the multilayer perceptron extrapolated poorly to unseen studies (RMSE {{biooil_mlp_grouped_rmse}} wt%) despite competitive random-split accuracy ({{biooil_mlp_random_rmse}} wt%). GPBoost, which models a study random intercept, gained nothing for unseen studies: because feedstock descriptors are nearly constant within a study, the random intercept absorbed most of the variance and its fixed-effect component — the only part available for a new study — was nearly flat (Supplementary Section S2). This illustrates that, in literature-compiled data, study identity and feedstock chemistry are strongly confounded, which limits how much of the between-study variation any model can attribute to chemistry.

## 3.2. Most out-of-study error is a study-level offset

For the STRATA base learner ({{strata_learner_label}}), study offsets were large and spread on both sides of zero (Fig. 4). The between-study share of out-of-study residual variance was {{biooil_share}} (95% CI {{biooil_share_lo}}–{{biooil_share_hi}}) for bio-oil and {{solid_share}} ({{solid_share_lo}}–{{solid_share_hi}}) for solid yield; the standard deviation of study offsets ($\hat\tau$) was {{biooil_tau}} and {{solid_tau}} wt%, against within-study residual standard deviations ($\hat\sigma_w$) of {{biooil_sigw}} and {{solid_sigw}} wt% (Table 3). A model that is well calibrated on average can therefore be biased by more than 10 wt% for an individual study, and errors for runs of the same study are strongly correlated — which is why randomly held-out runs, whose study offsets were already learnt, give an optimistic picture.

{{FIG:fig04_study_offsets|Mean out-of-study residual (observed − predicted) of each development study with 95% intervals of the mean, STRATA base learner with base features. The annotated share is the between-study fraction of residual variance with its study-cluster bootstrap CI.}}

## 3.3. {{P_heading}}

Because bio-oil yield is operationally defined by the recovery solvent and the reporting basis [@Valdez2011; @Watson2019], study offsets were expected to depend on the recorded work-up. {{P_sentence}} Adding the protocol descriptors changed the median per-study RMSE from {{biooil_P_med_base}} to {{biooil_P_med_baseP}} wt% for bio-oil (median paired difference {{biooil_P_diff}} wt%, 95% CI {{biooil_P_lo}} to {{biooil_P_hi}}; one-sided Wilcoxon *p* {{biooil_P_p}}; *n* = {{biooil_P_n}} studies) and from {{solid_P_med_base}} to {{solid_P_med_baseP}} wt% for solid yield (*p* {{solid_P_p}}) (Table 3). {{P_all_learners_sentence}} Consistently, a ridge meta-regression of the study offsets on the study-level descriptors had no out-of-study predictive value (leave-one-study-out R² = {{biooil_mr_r2}}, permutation *p* {{biooil_mr_p}} for bio-oil; R² = {{solid_mr_r2}}, *p* {{solid_mr_p}} for solids), and offsets did not differ significantly between the dominant extraction solvents ({{kw_sentence}}). {{ea_sentence}}

{{TABLE:table3_heterogeneity}}

This negative result has two readings, which the data cannot separate. Either work-up conventions matter less than chemistry and conditions that the curated fields do not capture (feedstock batch, particle size, reactor heat-up, quenching and product-handling details), or the coarse, partly missing descriptors that can be parsed from publications are too noisy to reveal their effect — {{none_named_pct}}% of development bio-oil runs named no extraction solvent. In both cases the practical conclusion is the same: the offset of a new study is not predictable from what studies currently report, so it has to be either measured (Section 3.5) or represented in the uncertainty (Section 3.4).

## 3.4. Row-calibrated intervals under-cover new studies; study calibration restores coverage

Intervals calibrated on randomly held-out runs are narrow because the residuals of seen studies omit the study offset. For unseen development studies, nominal 90% row-calibrated intervals covered {{biooil_cov_RC}} (bio-oil; 95% CI {{biooil_cov_RC_lo}}–{{biooil_cov_RC_hi}}) and {{solid_cov_RC}} (solids) of runs with equal study weights, and {{biooil_below80_RC}}% and {{solid_below80_RC}}% of studies had coverage below 0.80 (Table 4, Fig. 5). Calibrating on out-of-study residuals with equal study weights gave {{biooil_cov_SC}} ({{biooil_cov_SC_lo}}–{{biooil_cov_SC_hi}}) and {{solid_cov_SC}}; the improvement was significant across studies (one-sided Wilcoxon on per-study coverage, *p* {{biooil_covtest_p}} for bio-oil and {{solid_covtest_p}} for solids). The price is width: {{biooil_width_SC}} vs {{biooil_width_RC}} wt% for bio-oil and {{solid_width_SC}} vs {{solid_width_RC}} wt% for solids. These widths are not a defect of the method but an honest statement of how little a literature-trained model knows about a study it has not seen. The same pattern held for α = 0.05 and 0.20, with 5 instead of 10 outer folds (Supplementary Tables S4–S5), {{gen_cov_sentence}}

{{TABLE:table4_coverage}}

{{FIG:fig05_coverage|Study-weighted empirical coverage of nominal 90% prediction intervals calibrated on random rows (RC) or on studies (SC) across validation settings (base + P features). Dashed line: nominal level.}}

## 3.5. A few local runs reduce error and interval width

When *k* runs of the new study are available, its offset can be estimated. For the {{biooil_k_nstudies}} development studies with at least 11 bio-oil runs, the median per-study RMSE fell from {{biooil_k0_none_rmse}} wt% (*k* = 0) to {{biooil_k1_eb_rmse}}, {{biooil_k3_eb_rmse}} and {{biooil_k10_eb_rmse}} wt% with *k* = 1, 3 and 10 shrunk offsets, and the study-calibrated interval width fell from {{biooil_k0_none_width}} to {{biooil_k3_eb_width}} wt% at *k* = 3 while study-weighted coverage stayed at {{biooil_k3_eb_cov}} (Table 5, Fig. 6). For solids the corresponding RMSE values were {{solid_k0_none_rmse}}, {{solid_k1_eb_rmse}}, {{solid_k3_eb_rmse}} and {{solid_k10_eb_rmse}} wt%. {{kshot_eb_sentence}} The estimated shrinkage constant ($\hat\lambda = \hat\sigma_w^2/\hat\tau^2$, median over folds {{biooil_lam_median}} for bio-oil) is small, so the shrunk and raw offsets converge after a few runs; shrinkage matters mainly for *k* = 1–2, which is exactly the regime of a laboratory screening a new feedstock. These results quantify, with valid intervals, the observation of Elfetni et al. [@Elfetni2026BT] that local calibration runs reduce the error of literature-trained HTL surrogates.

{{TABLE:table5_kshot}}

{{FIG:fig06_kshot|*k*-shot adaptation to a new study (development studies with ≥ 11 runs, base + P features, 20 random support sets per study and *k*). Top: median per-study RMSE of the remaining runs; bottom: width of the re-calibrated 90% interval. *k* = 0 is the unadapted model.}}

## 3.6. Generalisation, robustness and cost

{{locked_paragraph}}

{{TABLE:table6_locked_test}}

{{generalisation_paragraph}}

{{TABLE:table7_generalisation}}

{{robustness_paragraph}}

{{FIG:fig07_robustness|Robustness of the STRATA base learner (base + P features). Top: RMSE (mean ± SD over outer folds) with Gaussian noise added to continuous test features or with fewer training studies. Bottom: study-weighted coverage of RC and SC 90% intervals.}}

{{efficiency_paragraph}}

{{TABLE:table8_efficiency}}

{{FIG:fig08_efficiency|Accuracy for unseen studies versus single-thread fit time on the development set (bio-oil, base features).}}

## 3.7. Error analysis and implications

{{error_paragraph}}

{{FIG:fig09_error_by_solvent|Mean out-of-study residual by extraction solvent named in the source study (groups with ≥ 3 studies; base features, seed-averaged outer-fold predictions).}}

{{FIG:fig10_parity|Observed versus predicted yields for the STRATA base learner under random-row CV and study-grouped CV (seed 11).}}

For practitioners, three recommendations follow. First, literature-trained hydrothermal surrogates should be validated with folds defined by source study (or by laboratory), and random-split metrics should not be used to claim predictive ability for new feedstocks or plants. Second, reported prediction intervals should be calibrated across studies; for the present database this means honest intervals of roughly ±{{biooil_halfwidth_SC}} wt% for bio-oil yield of a new study, which is wide enough to rule out fine-grained optimisation from literature data alone. Third, a handful of runs on the target feedstock and reactor are worth more than additional model complexity: three local runs reduced the median error more than any change of learner (Sections 3.1 and 3.5). For data curators, the null result for work-up descriptors suggests recording richer, standardised metadata (product-recovery procedure, quench, mass-balance closure, uncertainty of the yield measurement) so that the sources of between-study variation can eventually be modelled rather than absorbed.

## 3.8. Limitations

The study relies on one curated literature database; its extraction and harmonisation choices, imputed feedstock fractions and residual transcription errors propagate into all results, although they affect random and study-grouped evaluation alike. The protocol descriptors were parsed from free-text fields and are coarse. Study-level conformal validity assumes that a new study is exchangeable with the calibration studies; a study that differs systematically (a new reactor concept, unusual feedstock or catalyst) may be under-covered, as the family-out and external analyses partly show. The external database lacks study identifiers, so feedstock series were used as pseudo-studies. The *k*-shot analysis assumes that the first *k* runs of a study are exchangeable with its remaining runs; in practice laboratories choose runs deliberately. Physical admissibility across phases was not enforced here and can be combined with STRATA, which is model-agnostic. Finally, no new experiments were performed: the conclusions concern the transferability of literature-trained models, not the chemistry of hydrothermal conversion itself.

