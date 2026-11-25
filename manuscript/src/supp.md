---
title: "Supplementary Material — Process effects versus laboratory effects in hydrothermal liquefaction and carbonization of lignocellulosic biomass: a within-study meta-analysis"
---

# S1. Literature search

A reproducible multi-database search was run on {{lit3_date}} with a script that stores the raw records, the search strings and the run date. PubMed was queried with a Boolean title/abstract query, Crossref with 16 bibliographic queries (four machine-learning terms × four hydrothermal terms, 200 journal-article records each) and OpenAlex with a title-and-abstract search; OpenAlex refused anonymous requests on the run date (HTTP 429) and contributed no records. Records were de-duplicated by DOI, else by normalised title. Eligibility was applied by rule to titles and abstracts: E1, the record contains a machine-learning and a hydrothermal-conversion term; E2, primary research; E3, a product yield or property is predicted; E4, published from 2015 to the year after the run date. {{TREF:tableS_v3_prisma}} gives the strings and record flow. To check for existing meta-analyses of HTL/HTC process effects, PubMed was searched on 2026-11-25 for (meta-analysis OR "meta analysis" OR "quantitative synthesis") AND ("hydrothermal liquefaction" OR "hydrothermal carbonization" OR hydrochar OR biocrude) in title/abstract (4 records, none a meta-analysis of process effects) and Crossref with three bibliographic queries (meta-analysis + HTL bio-crude yield; meta-analysis + HTC hydrochar yield; round robin + HTL); no meta-analysis of HTL/HTC process effects was found. The two earlier analyses of the same database [@Elfetni2026BT; @Elfetni2026SSRN] develop physically admissible multi-phase surrogates and energy/carbon routing models; they do not estimate within-study process effects or between-laboratory heterogeneity. None of the present authors is an author of either work.

{{TABLE:tableS_v3_prisma}}

# S2. Protocol, addenda and deviations

The analysis protocol and the list of 38 locked studies were committed to a version-controlled repository hosted on GitHub before any model was fitted in our earlier work; later analyses were registered as addenda before they were run ({{TREF:table_v2_timeline}}). The meta-analysis reported here is Addendum E, registered on 2026-11-25 after the previous version of this work had been rejected and before any effect size was computed; only the number of available contrasts per factor and outcome had been counted. Deviations: (E-1) after the first development run, absurd solid-loading slopes were traced to floating-point noise that created near-identical "different" levels; levels are now rounded (temperature to 1 °C, log~2~ time to 0.01, loading to 0.1 percentage points) and adjacent steps smaller than 5 °C, 0.25 log~2~ units or 1 percentage point are not used; the first-run output is archived. (E-2) The database column labelled energy yield equals bio-oil yield × bio-oil HHV / 100 (correlation 0.9998), i.e. MJ per kg feed; energy recovery was therefore computed as yield × measured bio-oil HHV / feed HHV. (E-3) A linear mixed model was added as a second estimator of the laboratory effect; a study-level bootstrap and response ratios were added during internal review. Addendum F (catalyst dose–response, feedstock-family moderators; exploratory) was registered after the Addendum E results were known and before it was computed. Both E-1 and E-2 were made before the locked studies were analysed. The protocol was not deposited in a public registry; the repository and its commit history are available from the corresponding author on request.

{{TABLE:table_v2_timeline}}

# S3. Data

{{TABLE:table1_data}}

# S4. Sensitivity and moderator analyses

{{TABLE:table_v4_sensitivity}}

{{TABLE:table_v4_moderators}}

{{TABLE:table_v4_relative}}

{{TABLE:table_v4_dose}}

{{TABLE:table_v4_family}}

# S5. Nitrogen content of bio-oil

{{TABLE:table_v4_meta_nitrogen}}

# S6. Transfer of literature-trained machine-learning models to new studies

Earlier analyses of the same database, carried out under the original protocol and its addenda A–D, evaluated twelve learners for bio-oil and solid yields with study-grouped cross-validation, on the 38 locked studies and on an external hydrochar database [@TU4data]. They are summarised here because they establish the size of the laboratory effect used in Section 3.5 and the value of local runs used in Section 3.8. Random splitting of runs overstated accuracy about two-fold compared with predicting unseen studies ({{TREF:table2_benchmark}}, {{FREF:fig03_random_vs_grouped}}). The between-study share of out-of-study residual variance was {{biooil_share}} (95% CI {{biooil_share_lo}}–{{biooil_share_hi}}) for bio-oil and {{solid_share}} ({{solid_share_lo}}–{{solid_share_hi}}) for solid yield ({{TREF:table3_heterogeneity}}), with offset standard deviations of {{biooil_tau}} and {{solid_tau}} wt%; reported work-up and yield-basis descriptors did not explain these offsets. Conformal prediction intervals calibrated across studies covered {{cov_range_SC}} of runs of new studies, compared with {{cov_range_RC}} for intervals calibrated on random runs ({{TREF:table4_coverage}}). In a retrospective simulated deployment, three runs measured in a screening design and combined with the literature model reduced the median per-study error by {{gain3_min}}–{{gain3_max}} wt% across development, locked and external settings, although for locked bio-oil studies the local runs alone were more accurate ({{TREF:table_v3_deployment}}, {{FREF:fig14_deployment}}).

{{TABLE:table2_benchmark}}

{{TABLE:table3_heterogeneity}}

{{TABLE:table4_coverage}}

{{TABLE:table_v3_deployment}}

{{FIG:fig03_random_vs_grouped|Root-mean-square error of 12 learners under random-row five-fold cross-validation (circles) and study-grouped ten-fold cross-validation (squares; mean of three seeds), base features.}}

{{FIG:fig14_deployment|Retrospective simulated deployment (screening-design run order): median per-study RMSE of the remaining runs and half-width of re-calibrated 90% intervals for the literature model alone (A), the literature model anchored by k local runs (B) and the local runs alone (C).}}

# S7. Reproducibility

A single command regenerates every result file, table and figure from the public data, and a second command regenerates the manuscript and this document from those files; library versions and CPU details are written to a log at run time. The meta-analysis is implemented in `src/meta/within_study.py` and `experiments/e18_meta.py`, with unit tests that verify that laboratory offsets cancel in the contrasts and that the random-effects estimator agrees with an independent implementation. The code, the locked study list, configuration files, result files and per-contrast data are available from the corresponding author on reasonable request.
