---
title: "Supplementary Material — From literature to laboratory: an uncertainty-aware framework for transferring machine-learning models of hydrothermal biomass conversion and planning first experiments"
---


# S1. Literature search

A reproducible multi-database search was run on {{lit3_date}} with a script that stores the raw records, the search strings and the run date. PubMed was queried with a Boolean title/abstract query, Crossref with 16 bibliographic queries (four machine-learning terms × four hydrothermal terms, 200 journal-article records each) and OpenAlex with a title-and-abstract search; OpenAlex refused anonymous requests on the run date (HTTP 429) and contributed no records. Records were de-duplicated by DOI, else by normalised title. Eligibility was applied by rule to titles and abstracts, so that the selection is reproducible: E1, the record contains a machine-learning and a hydrothermal-conversion term; E2, primary research (not a review, editorial, erratum or retraction); E3, a product yield or property is predicted; E4, published from 2015 to the year after the run date (journal issue years can run one year ahead of online publication). Records without an abstract were screened on the title. Search strings and record flow are given in Table S1. Abstract-level extraction under-counts practices that appear only in the full text; the counts of validation and uncertainty practices are therefore lower bounds. Table S2 lists the earlier PubMed-only corpus from which the median reported R² quoted in the Introduction was extracted.

{{TABLE:tableS_v3_prisma}}

{{TABLE:tableS1_literature}}

# S2. Protocol, addenda and deviations

The analysis protocol (research questions, metrics, statistical tests, seeds) and the locked list of 38 test studies were committed to a version-controlled repository hosted on GitHub before any model was fitted. The protocol was not deposited in a public registry; the order of registration and analysis is documented by the commit history ({{TREF:table_v2_timeline}}), and the repository is available from the corresponding author on request. Addenda: A (within-study trends) and A2 (product-quality targets), each registered before its analysis; B (contrast types and rules of thumb), registered after the development results of A had been seen and therefore exploratory; C (one-time locked confirmation of A and B); and D (sequential deployment E15, decision support E16 and laboratory case studies E17), registered after an external pre-submission review and before any of these analyses was run. Deviations, each logged with date and reason: (i) the tabular foundation model could not be run because its weights require a personal licence acceptance; (ii) every learner was tuned separately for each feature set; (iii) the ridge-penalty grid of the meta-regression was widened after its selected value hit the registered upper bound, and three univariate study-level tests were added as secondary analyses; (iv) post-hoc review analyses E9 (base learners), E10 (cross-study duplicate audit) and E11 (overhead), and a post-hoc sensitivity analysis of the locked test excluding the study with the largest squared-error share; (v) an exploratory locally adaptive interval variant (Section S4); (vi) the model-free trend analysis E13 was not registered and is descriptive; (vii) because the pre-registered applicability-domain threshold flagged no locked study, an exploratory rank correlation between the score and the error on locked studies was added after this result was known (main-text {{TREF:table_v3_decision}}); (viii) the literature search was extended from PubMed to a multi-database search after the external review; when the screening was checked, two rules were corrected and re-applied to the stored records without new queries — the publication window was widened to the year after the run date because an included 2026 article carries a 2027 issue year, and 'publication-aware/-level' was added to the pattern for grouped validation. GPBoost was run as registered; its study random intercept absorbed most of the variance because feedstock descriptors are nearly constant within a study, so its out-of-study predictions reverted towards a nearly flat fixed-effect function.

{{TABLE:table_v2_timeline}}

# S3. Additional benchmark and sensitivity results

{{TABLE:tableS2_benchmark_baseP}}

{{TABLE:tableS_paired_learner_tests}}

{{TABLE:tableS_coverage_all_alpha}}

{{TABLE:tableS3_sensitivity_alpha_folds}}

{{TABLE:tableS4_sensitivity_tau2}}

{{TABLE:tableS5_sensitivity_tuning}}

{{TABLE:table5_kshot}}

{{TABLE:table7_generalisation}}

# S4. Exploratory: locally adaptive study-calibrated intervals (post hoc)

Motivation: constant-width study-calibrated intervals are wide. Hypothesis: out-of-study errors are heteroscedastic, so dividing conformity scores by a learned difficulty $\hat\sigma(\mathbf{x})$ narrows intervals for easy regimes without losing study-level coverage. A shallow gradient-boosting model of $\log(|r| + 0.5)$ was cross-fitted by study on the out-of-study residuals of the training studies; scores $|r|/\hat\sigma$ were calibrated with the same study-weighted quantile, and intervals were $f(\mathbf{x}) \pm \hat q\,\hat\sigma(\mathbf{x})$. {{adaptive_sentence}}

{{TABLE:tableS7_adaptive}}

# S5. Error analysis by subgroup

{{TABLE:tableS6_error_analysis}}

# S6. STRATA with different base learners (E9)

{{TABLE:tableS10_base_learners}}

# S7. Trend, ranking and anchoring analyses (Addenda A, A2, B, C)

*Within-study contrasts (E12).* For two runs *a* and *b* of the same study, the contrast is $\Delta_{ab} = y_a - y_b$; a study offset cancels in $\Delta_{ab}$. Three learners predicted contrasts for every pair of runs within each unseen study: the absolute model A by differencing, $\hat\Delta_{ab} = f(\mathbf{x}_a) - f(\mathbf{x}_b)$; a within-study model W, trained on study-centred targets $y - \bar y_{\text{study}}$ with features $[\mathbf{x}, \mathbf{x} - \bar{\mathbf{x}}_{\text{study}}]$; and a pairwise-difference model PD, trained on pairs of runs of the same training study with inputs $[\mathbf{x}_a, \mathbf{x}_b, \mathbf{x}_a - \mathbf{x}_b]$ and target $\Delta_{ab}$ (at most 30 random partners per run), antisymmetrised as $\hat\Delta_{ab} = \tfrac{1}{2}[h(a,b) - h(b,a)]$. All three used the E1 hyper-parameters of XGBoost, extra trees and LightGBM. Contrast accuracy was summarised by $R^2_\Delta = 1 - \sum(\hat\Delta - \Delta)^2 / \sum \Delta^2$, relative to the 'no-change' predictor. Hypotheses: contrasts are predicted better than levels (T1); W and PD predict contrasts better than A (T2, one-sided Wilcoxon on per-study contrast RMSE, Holm); anchoring on *k* = 1–3 measured runs, $\hat y_i = \tfrac{1}{k}\sum_a (y_a + \hat\Delta_{ia})$, beats STRATA's shrunk offset (T3); study-calibrated intervals for contrasts are valid and narrower than for levels (T4); and models rank the runs of a study usefully (T5). The same analysis was repeated for bio-oil higher heating value ({{n_hhv_biooil_dev}} development runs from {{s_hhv_biooil_dev}} studies, {{n_hhv_biooil_test}} locked runs) and bio-oil carbon content ({{n_c_biooil_dev}} runs, {{s_c_biooil_dev}} studies; {{n_c_biooil_test}} locked runs) (Addendum A2).

*Model-free trends (E13; descriptive).* Within each development study, pairs of runs that differ only in temperature (all other base features and the feedstock identical) or only in residence time were identified, and their slopes summarised per study and temperature band; medians across studies were bootstrapped over studies. Below 250 °C bio-oil yield changed by {{biooil_slope_150_250}} wt% per 10 °C ({{biooil_sign_150_250}}% same sign), at 250–300 °C by {{biooil_slope_250_300}} wt%, at 300–350 °C by {{biooil_slope_300_350}} wt% and above 350 °C by {{biooil_slope_350_450}} wt%; solid yield changed by {{solid_slope_150_250}}, {{solid_slope_250_300}}, {{solid_slope_300_350}} and {{solid_slope_350_450}} wt% per 10 °C. Doubling the residence time had no consistent effect on bio-oil yield ({{biooil_tslope}} wt%; {{biooil_tsign}}% same sign) and a small negative effect on solid yield ({{solid_tslope}} wt%).

*Contrast results.* For unseen development studies, contrast $R^2_\Delta$ was {{biooil_d_c_r2_min}}–{{biooil_d_c_r2_max}} for bio-oil (level R² {{biooil_d_l_r2_min}}–{{biooil_d_l_r2_max}}) and {{solid_d_c_r2_min}}–{{solid_d_c_r2_max}} for solids (levels {{solid_d_l_r2_min}}–{{solid_d_l_r2_max}}); weighting studies equally, the median per-study $R^2_\Delta$ was {{biooil_d_sw_min}}–{{biooil_d_sw_max}} for bio-oil and {{solid_d_sw_min}}–{{solid_d_sw_max}} for solids. On locked studies offset-invariant models retained contrast skill where the absolute model failed (bio-oil $R^2_\Delta$ {{biooil_l_c_r2_A}} for A vs {{biooil_l_c_r2_W}} for W and {{biooil_l_c_r2_PD}} for PD), but two studies accounted for {{lk_c_top2_share}}% of the squared contrast error of A, and per-study comparisons were not significant ({{t2_locked_sig}} of {{t2_locked_n}} after Holm). With one measured run, the median per-study RMSE was {{biooil_k1_AEB}} wt% for STRATA, {{biooil_k1_W}} for W and {{biooil_k1_PD}} for PD (bio-oil, XGBoost; T3 not supported). Intervals for contrasts covered {{biooil_d_ccov}} (bio-oil) and {{solid_d_ccov}} (solids) of unseen-study pairs (T4).

*Ranking (E14).* For unseen development studies, all three model types picked bio-oil conditions with lower regret than the 325 °C rule of thumb (median regret {{biooil_rk_d_PD}}–{{biooil_rk_d_A}} vs {{biooil_rk_d_rule}} wt%; random choice {{biooil_rk_d_rand}} wt%); for solids none beat the lowest-temperature rule. On {{biooil_rk_l_n}} locked bio-oil studies the advantage {{c1_sentence}} (median regret {{biooil_rk_l_A}}–{{biooil_rk_l_W}} wt% for the models, {{biooil_rk_l_rule}} wt% for the rule and {{biooil_rk_l_rand}} wt% for random choice).

{{FIG:fig11_trend_atlas|Model-free trend atlas. Median change in yield per +10 °C across development studies, computed from pairs of runs of the same study that differ only in temperature; error bars are 95% study-bootstrap CIs, annotations give the share of studies whose slope has the same sign as the median.}}

{{FIG:fig12_levels_vs_contrasts|Accuracy of absolute-yield predictions (levels, model A) and of within-study contrasts (models A, W and PD; XGBoost) for unseen development studies and for the locked test studies, for four targets. R² of contrasts is relative to the no-change predictor.}}

{{FIG:fig13_ranking_regret|Regret of choosing the run predicted to give the highest yield within a study for models A, W and PD, a rule of thumb and random choice. Left: development studies (exploratory); right: locked studies (pre-registered confirmatory test).}}

{{TABLE:table_v2_empirical_trends}}

{{TABLE:table_v2_levels_vs_contrasts}}

{{TABLE:table_v2_ranking}}

{{TABLE:table_v2_trends_by_process}}

{{TABLE:table_v2_study_weighted_contrasts}}

# S8. Additional figures and cost

{{FIG:fig02_dataset|Development data. (a) Number of runs contributed per source study; (b) yield distributions; (c) publication years of all 188 source studies (dashed line: temporal split).}}

{{FIG:fig06_kshot|*k*-shot adaptation to a new study with random support sets (development studies with ≥ 11 runs, base + P features, 20 random support sets per study and *k*). Top: median per-study RMSE of the remaining runs; bottom: width of the re-calibrated 90% interval.}}

{{FIG:fig07_robustness|Robustness of the STRATA base learner (base + P features). Top: RMSE (mean ± SD over outer folds) with Gaussian noise added to continuous test features or with fewer training studies. Bottom: study-weighted coverage of RC and SC 90% intervals.}}

{{FIG:fig08_efficiency|Accuracy for unseen studies versus single-thread fit time on the development set (bio-oil, base features).}}

{{FIG:fig09_error_by_solvent|Mean out-of-study residual by extraction solvent named in the source study (groups with ≥ 3 studies; base features, seed-averaged outer-fold predictions).}}

{{FIG:fig10_parity|Observed versus predicted yields for the STRATA base learner under random-row CV and study-grouped CV (seed 11).}}

{{TABLE:table8_efficiency}}

# S9. Additional deployment results (Addendum D)

{{TABLE:table_v3_deployment_long}}

{{TABLE:table_v3_deployment_other_orders}}

{{TABLE:table_v3_deployment_tests}}

# S10. Reproducibility and availability

A single command regenerates every result file, table and figure from the public data, and a second command regenerates the manuscript and this document from those files; library versions and CPU details are written to a log at run time. The code, the locked test-study list, configuration files, result files and per-run predictions are available from the corresponding author on reasonable request.
