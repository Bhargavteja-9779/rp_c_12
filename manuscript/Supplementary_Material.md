---
title: "Supplementary Material — Process effects versus laboratory effects in hydrothermal liquefaction and carbonization of lignocellulosic biomass: a within-study meta-analysis"
---

# S1. Literature search

A reproducible multi-database search was run on 2026-11-18 with a script that stores the raw records, the search strings and the run date. PubMed was queried with a Boolean title/abstract query, Crossref with 16 bibliographic queries (four machine-learning terms × four hydrothermal terms, 200 journal-article records each) and OpenAlex with a title-and-abstract search; OpenAlex refused anonymous requests on the run date (HTTP 429) and contributed no records. Records were de-duplicated by DOI, else by normalised title. Eligibility was applied by rule to titles and abstracts: E1, the record contains a machine-learning and a hydrothermal-conversion term; E2, primary research; E3, a product yield or property is predicted; E4, published from 2015 to the year after the run date. Table S1 gives the strings and record flow. To check for existing meta-analyses of HTL/HTC process effects, PubMed was searched on 2026-11-25 for (meta-analysis OR "meta analysis" OR "quantitative synthesis") AND ("hydrothermal liquefaction" OR "hydrothermal carbonization" OR hydrochar OR biocrude) in title/abstract (4 records, none a meta-analysis of process effects) and Crossref with three bibliographic queries (meta-analysis + HTL bio-crude yield; meta-analysis + HTC hydrochar yield; round robin + HTL); no meta-analysis of HTL/HTC process effects was found. The two earlier analyses of the same database (Elfetni et al., 2027; Elfetni et al., 2026) develop physically admissible multi-phase surrogates and energy/carbon routing models; they do not estimate within-study process effects or between-laboratory heterogeneity. None of the present authors is an author of either work.


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



# S2. Protocol, addenda and deviations

The analysis protocol and the list of 38 locked studies were committed to a version-controlled repository hosted on GitHub before any model was fitted in our earlier work; later analyses were registered as addenda before they were run (Table S2). The meta-analysis reported here is Addendum E, registered on 2026-11-25 after the previous version of this work had been rejected and before any effect size was computed; only the number of available contrasts per factor and outcome had been counted. Deviations: (E-1) after the first development run, absurd solid-loading slopes were traced to floating-point noise that created near-identical "different" levels; levels are now rounded (temperature to 1 °C, log~2~ time to 0.01, loading to 0.1 percentage points) and adjacent steps smaller than 5 °C, 0.25 log~2~ units or 1 percentage point are not used; the first-run output is archived. (E-2) The database column labelled energy yield equals bio-oil yield × bio-oil HHV / 100 (correlation 0.9998), i.e. MJ per kg feed; energy recovery was therefore computed as yield × measured bio-oil HHV / feed HHV. (E-3) A linear mixed model was added as a second estimator of the laboratory effect; a study-level bootstrap and response ratios were added during internal review. Addendum F (catalyst dose–response, feedstock-family moderators; exploratory) was registered after the Addendum E results were known and before it was computed. Both E-1 and E-2 were made before the locked studies were analysed. The protocol was not deposited in a public registry; the repository and its commit history are available from the corresponding author on request.


**Table S2.** Audit trail: version-control commits establishing that the protocol, the locked study list and each addendum preceded the analyses they govern.

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



# S3. Data


**Table S3.** Data used for each target after pre-specified exclusions.

| Target | Split | Runs | Studies | Median runs/study | Yield mean ± SD (wt%) | Excluded (carbon basis / missing inputs / single-run study) |
|---|---|---|---|---|---|---|
| Bio-oil | Development | 2261 | 122 | 15 | 30.8 ± 18.0 | 3 / 11 / 4 |
| Bio-oil | Locked test | 556 | 28 | 12 | 26.9 ± 13.1 | 0 / 1 / 0 |
| Solid | Development | 2156 | 120 | 13 | 33.4 ± 20.2 | 0 / 12 / 5 |
| Solid | Locked test | 457 | 30 | 12 | 40.0 ± 22.1 | 0 / 0 / 1 |



# S4. Sensitivity and moderator analyses


**Table S4.** Sensitivity of the meta-analytic means to the τ² estimator, to using one contrast per study and to leaving out single studies; 95% CI from 2,000 bootstrap resamples of studies (post hoc); Egger-type test for small-study effects (≥ 10 studies).

| Outcome | Change | REML | Paule–Mandel | One per study (median) | Leave-one-study-out range | Study-bootstrap 95% CI | Egger p |
|---|---|---|---|---|---|---|---|
| Bio-oil yield (wt%) | T +10 °C (250–300 °C) | 1.07 | 1.08 | 1.05 | 0.92 to 1.18 | 0.66 to 1.53 | 0.61 |
| Bio-oil yield (wt%) | T +10 °C (300–350 °C) | -0.75 | -0.75 | -0.83 | -0.83 to -0.56 | -1.38 to -0.2 | 0.04 |
| Bio-oil yield (wt%) | T +10 °C (<250 °C) | 1.76 | 1.77 | 1.86 | 1.29 to 1.99 | 0.7 to 3.0 | 0.59 |
| Bio-oil yield (wt%) | T +10 °C (≥350 °C) | -0.5 | -0.51 | -0.69 | -0.72 to -0.34 | -1.23 to 0.29 | 0.55 |
| Bio-oil yield (wt%) | Residence time ×2 | -0.64 | -0.64 | -0.28 | -0.76 to -0.5 | -1.41 to 0.18 | 0.54 |
| Bio-oil yield (wt%) | Solid loading +10 pp | -6.18 | -6.3 | -7.1 | -6.88 to -2.64 | -16.6 to -0.45 | 0.48 |
| Bio-oil yield (wt%) | Acid | 8.52 | 8.52 | 8.41 | 6.39 to 10.28 | 2.12 to 15.02 | — |
| Bio-oil yield (wt%) | Alkali carbonate | 5.46 | 5.46 | 5.76 | 4.62 to 6.02 | 2.68 to 8.26 | 0.53 |
| Bio-oil yield (wt%) | Alkali hydroxide | 6.61 | 6.62 | 7.04 | 5.17 to 7.45 | 1.7 to 12.13 | 0.86 |
| Bio-oil yield (wt%) | Metal / supported metal | 8.48 | 8.53 | 8.84 | 7.29 to 8.83 | 5.63 to 11.97 | 0.01 |
| Bio-oil yield (wt%) | Other catalyst | 6.83 | 6.83 | 6.92 | 3.57 to 8.35 | -0.08 to 15.43 | 0.35 |
| Bio-oil yield (wt%) | Alcohol (vs water) | 9.17 | 9.17 | 9.33 | 1.69 to 16.09 | -9.86 to 26.4 | — |
| Bio-oil yield (wt%) | Water–alcohol (vs water) | 4.39 | 4.36 | 3.61 |  | -4.05 to 12.19 | — |
| Solid yield (wt%) | T +10 °C (250–300 °C) | -1.74 | -1.73 | -1.74 | -1.82 to -1.65 | -2.2 to -1.31 | 0.11 |
| Solid yield (wt%) | T +10 °C (300–350 °C) | -0.59 | -0.59 | -0.64 | -0.65 to -0.49 | -1.05 to -0.24 | 0.75 |
| Solid yield (wt%) | T +10 °C (<250 °C) | -2.62 | -2.62 | -2.78 | -2.8 to -2.48 | -3.36 to -1.77 | 0.80 |
| Solid yield (wt%) | T +10 °C (≥350 °C) | -0.51 | -0.5 | -0.19 | -0.74 to -0.29 | -1.3 to 0.4 | 0.32 |
| Solid yield (wt%) | Residence time ×2 | -1.95 | -2.03 | -2.41 | -2.06 to -1.05 | -4.87 to -0.39 | 0.27 |
| Solid yield (wt%) | Solid loading +10 pp | 5.96 | 5.96 | 5.43 | 5.26 to 6.72 | 2.72 to 9.34 | 0.31 |
| Solid yield (wt%) | Acid | -16.01 | -16.01 | -16.0 | -19.91 to -5.98 | -36.95 to -1.92 | — |
| Solid yield (wt%) | Alkali carbonate | -6.88 | -6.91 | -7.75 | -7.46 to -5.7 | -10.86 to -3.74 | 0.37 |
| Solid yield (wt%) | Alkali hydroxide | -4.53 | -4.43 | -6.01 | -5.22 to -2.97 | -8.57 to -1.0 | 0.18 |
| Solid yield (wt%) | Metal / supported metal | -8.24 | -8.25 | -8.52 | -8.8 to -7.04 | -12.49 to -4.58 | 0.44 |
| Solid yield (wt%) | Other catalyst | -5.82 | -5.82 | -5.75 | -9.39 to -0.27 | -18.98 to 5.54 | 0.46 |
| Solid yield (wt%) | Alcohol (vs water) | 11.77 | 11.79 | 11.53 | 9.35 to 14.68 | 3.28 to 19.22 | — |
| Solid yield (wt%) | Water–alcohol (vs water) | -4.78 | -4.62 | -3.27 |  | -7.21 to -1.15 | — |
| Aqueous-phase yield (wt%) | T +10 °C (250–300 °C) | -0.13 | -0.19 | -0.03 | -0.3 to 0.07 | -0.75 to 0.51 | 0.17 |
| Aqueous-phase yield (wt%) | T +10 °C (300–350 °C) | 0.07 | 0.09 | 0.23 | -0.16 to 0.19 | -0.52 to 0.85 | 0.31 |
| Aqueous-phase yield (wt%) | T +10 °C (<250 °C) | 0.62 | 0.63 | 1.05 | 0.5 to 0.76 | 0.25 to 1.24 | 0.34 |
| Aqueous-phase yield (wt%) | T +10 °C (≥350 °C) | -0.52 | -0.5 | -0.4 | -0.8 to -0.4 | -1.09 to 0.24 | 0.34 |
| Aqueous-phase yield (wt%) | Residence time ×2 | -0.19 | -0.17 | -0.82 | -0.48 to 0.04 | -1.4 to 1.1 | 0.17 |
| Aqueous-phase yield (wt%) | Solid loading +10 pp | -4.54 | -4.54 | -4.76 | -4.88 to -4.29 | -7.08 to -2.32 | — |
| Aqueous-phase yield (wt%) | Alkali carbonate | 3.63 | 3.64 | 3.71 | 2.13 to 5.22 | -0.82 to 8.2 | 0.87 |
| Aqueous-phase yield (wt%) | Alkali hydroxide | 8.36 | 8.36 | 8.39 | 6.53 to 9.66 | 3.27 to 13.89 | — |
| Aqueous-phase yield (wt%) | Metal / supported metal | 2.41 | 2.41 | 2.52 | 1.07 to 3.37 | -1.2 to 6.59 | 0.91 |
| Gas yield (wt%) | T +10 °C (250–300 °C) | 0.54 | 0.54 | 0.55 | 0.36 to 0.78 | -0.27 to 1.2 | 0.60 |
| Gas yield (wt%) | T +10 °C (300–350 °C) | 1.37 | 1.38 | 1.44 | 1.11 to 1.44 | 0.85 to 2.1 | 0.42 |
| Gas yield (wt%) | T +10 °C (<250 °C) | 0.81 | 0.82 | 0.82 | 0.65 to 0.87 | 0.4 to 1.3 | 0.48 |
| Gas yield (wt%) | T +10 °C (≥350 °C) | 2.15 | 2.16 | 2.28 | 1.77 to 2.46 | 1.07 to 3.58 | — |
| Gas yield (wt%) | Residence time ×2 | 3.39 | 3.41 | 3.37 | 1.53 to 3.59 | 0.97 to 7.28 | 0.06 |
| Gas yield (wt%) | Solid loading +10 pp | 2.52 | 2.59 | 2.31 | 0.44 to 3.29 | -0.42 to 5.71 | 0.69 |
| Gas yield (wt%) | Alkali carbonate | -0.79 | -0.78 | -0.56 | -1.49 to -0.18 | -3.33 to 1.63 | 0.47 |
| Gas yield (wt%) | Alkali hydroxide | -2.12 | -2.15 | -1.82 | -2.5 to -0.44 | -4.94 to -0.08 | 0.68 |
| Gas yield (wt%) | Metal / supported metal | 0.35 | 0.35 | 0.36 | -0.1 to 0.91 | -1.68 to 2.4 | 0.85 |
| Gas yield (wt%) | Other catalyst | -3.13 | -3.13 | -3.13 | -3.86 to -1.56 | -6.62 to -0.15 | — |
| Bio-oil HHV (MJ/kg) | T +10 °C (250–300 °C) | 0.44 | 0.44 | 0.44 | 0.41 to 0.47 | 0.3 to 0.58 | 0.98 |
| Bio-oil HHV (MJ/kg) | T +10 °C (300–350 °C) | 0.3 | 0.3 | 0.33 | 0.26 to 0.35 | 0.13 to 0.48 | 0.45 |
| Bio-oil HHV (MJ/kg) | T +10 °C (<250 °C) | 0.39 | 0.4 | 0.44 | 0.29 to 0.54 | -0.06 to 0.79 | — |
| Bio-oil HHV (MJ/kg) | T +10 °C (≥350 °C) | 0.2 | 0.2 | 0.08 | 0.09 to 0.29 | -0.18 to 0.45 | 0.14 |
| Bio-oil HHV (MJ/kg) | Residence time ×2 | 0.35 | 0.35 | 0.32 | 0.31 to 0.4 | 0.13 to 0.57 | 0.45 |
| Bio-oil HHV (MJ/kg) | Solid loading +10 pp | 0.2 | 0.2 | 0.21 | 0.1 to 0.28 | -0.04 to 0.58 | — |
| Bio-oil HHV (MJ/kg) | Acid | 2.37 | 2.38 | 2.26 |  | 0.87 to 4.74 | — |
| Bio-oil HHV (MJ/kg) | Alkali carbonate | 1.23 | 1.31 | 1.58 | 1.1 to 1.33 | 0.65 to 2.08 | 0.36 |
| Bio-oil HHV (MJ/kg) | Alkali hydroxide | 0.45 | 0.43 | 0.85 | 0.16 to 0.76 | -0.77 to 1.69 | 0.41 |
| Bio-oil HHV (MJ/kg) | Metal / supported metal | 1.21 | 1.21 | 1.19 | 0.98 to 1.46 | 0.16 to 2.22 | 0.78 |
| Bio-oil HHV (MJ/kg) | Other catalyst | -0.59 | -0.59 | -0.57 | -0.93 to -0.21 | -1.7 to 0.48 | — |
| Energy recovery to bio-oil (%) | T +10 °C (250–300 °C) | 1.98 | 1.98 | 2.74 | 1.75 to 2.13 | 1.3 to 2.9 | 0.04 |
| Energy recovery to bio-oil (%) | T +10 °C (300–350 °C) | -0.62 | -0.61 | -0.49 | -0.87 to -0.39 | -1.61 to 0.51 | 0.67 |
| Energy recovery to bio-oil (%) | T +10 °C (<250 °C) | 3.08 | 3.08 | 2.97 | 2.14 to 3.67 | 0.95 to 5.12 | — |
| Energy recovery to bio-oil (%) | T +10 °C (≥350 °C) | -1.81 | -1.81 | -2.36 | -2.51 to -1.44 | -3.47 to -0.07 | 0.28 |
| Energy recovery to bio-oil (%) | Residence time ×2 | 0.84 | 0.84 | 0.13 | 0.34 to 1.28 | -1.48 to 2.74 | 0.92 |
| Energy recovery to bio-oil (%) | Solid loading +10 pp | -2.69 | -2.7 | -3.35 | -5.05 to 1.75 | -11.02 to 4.13 | — |
| Energy recovery to bio-oil (%) | Alkali carbonate | 13.13 | 12.78 | 15.73 | 11.72 to 14.32 | 7.31 to 18.91 | 0.03 |
| Energy recovery to bio-oil (%) | Alkali hydroxide | 12.14 | 12.29 | 15.08 | 7.64 to 14.1 | 2.68 to 24.43 | 0.13 |
| Energy recovery to bio-oil (%) | Metal / supported metal | 19.64 | 19.66 | 20.39 | 16.71 to 20.87 | 11.75 to 29.1 | 0.08 |
| Energy recovery to bio-oil (%) | Other catalyst | 0.94 | 0.95 | 1.42 | -0.95 to 3.51 | -6.02 to 7.62 | — |
| Bio-oil N (wt%) | T +10 °C (250–300 °C) | -0.0 | -0.0 | 0.01 | -0.01 to 0.01 | -0.02 to 0.01 | 0.04 |
| Bio-oil N (wt%) | T +10 °C (300–350 °C) | 0.01 | 0.01 | 0.01 | 0.01 to 0.01 | -0.0 to 0.02 | 0.78 |
| Bio-oil N (wt%) | T +10 °C (<250 °C) | -0.03 | -0.03 | -0.03 |  | -0.07 to 0.0 | — |
| Bio-oil N (wt%) | T +10 °C (≥350 °C) | 0.0 | 0.0 | -0.0 | -0.0 to 0.01 | -0.02 to 0.02 | 0.31 |
| Bio-oil N (wt%) | Residence time ×2 | 0.07 | 0.07 | -0.01 | 0.02 to 0.09 | -0.01 to 0.23 | 0.93 |
| Bio-oil N (wt%) | Solid loading +10 pp | -0.14 | -0.14 | -0.09 |  | -0.34 to -0.04 | — |
| Bio-oil N (wt%) | Acid | -0.12 | -0.12 | -0.12 |  | -0.23 to -0.02 | — |
| Bio-oil N (wt%) | Alkali carbonate | -0.05 | -0.05 | -0.03 | -0.09 to 0.01 | -0.2 to 0.12 | 0.16 |
| Bio-oil N (wt%) | Alkali hydroxide | 0.28 | 0.29 | 0.27 | 0.09 to 0.33 | -0.04 to 0.67 | 0.91 |
| Bio-oil N (wt%) | Metal / supported metal | -0.01 | -0.01 | -0.01 | -0.05 to 0.0 | -0.08 to 0.08 | 0.65 |
| Bio-oil N (wt%) | Other catalyst | -0.2 | -0.23 | -0.13 | -0.22 to -0.09 | -0.38 to -0.01 | — |




**Table S5.** Pre-specified moderator analyses of catalyst effects (temperature of the cell, process subtype, feedstock lignin content); differences between subgroup means with z-tests, Holm-corrected within outcome × factor.

| Outcome | Catalyst | Moderator | Group A (k) | Effect A | Group B (k) | Effect B | p | p (Holm) |
|---|---|---|---|---|---|---|---|---|
| Bio-oil yield (wt%) | Alkali carbonate | temperature | <300 °C (15) | 1.88 | ≥300 °C (26) | 6.93 | 0.048 | 0.382 |
| Bio-oil yield (wt%) | Alkali carbonate | lignin | lignin ≤ 21 wt% (15) | 7.13 | lignin > 21 wt% (19) | 4.63 | 0.367 | 1.0 |
| Bio-oil yield (wt%) | Alkali hydroxide | temperature | <300 °C (10) | 4.83 | ≥300 °C (17) | 7.9 | 0.56 | 1.0 |
| Bio-oil yield (wt%) | Alkali hydroxide | lignin | lignin ≤ 24 wt% (13) | 10.22 | lignin > 24 wt% (14) | 5.44 | 0.395 | 1.0 |
| Bio-oil yield (wt%) | Metal / supported metal | temperature | <300 °C (21) | 6.31 | ≥300 °C (29) | 7.99 | 0.509 | 1.0 |
| Bio-oil yield (wt%) | Metal / supported metal | lignin | lignin ≤ 22 wt% (18) | 8.64 | lignin > 22 wt% (22) | 8.29 | 0.913 | 1.0 |
| Bio-oil yield (wt%) | Other catalyst | temperature | <300 °C (5) | 8.04 | ≥300 °C (10) | 5.8 | 0.743 | 1.0 |
| Bio-oil yield (wt%) | Other catalyst | lignin | lignin ≤ 27 wt% (7) | 12.08 | lignin > 27 wt% (7) | 1.78 | 0.195 | 1.0 |
| Solid yield (wt%) | Alkali carbonate | temperature | <300 °C (10) | -3.13 | ≥300 °C (23) | -7.81 | 0.077 | 0.54 |
| Solid yield (wt%) | Alkali carbonate | lignin | lignin ≤ 21 wt% (12) | -8.28 | lignin > 21 wt% (16) | -6.47 | 0.656 | 1.0 |
| Solid yield (wt%) | Alkali hydroxide | temperature | <300 °C (6) | -6.82 | ≥300 °C (15) | -4.59 | 0.556 | 1.0 |
| Solid yield (wt%) | Alkali hydroxide | lignin | lignin ≤ 26 wt% (11) | -8.84 | lignin > 26 wt% (10) | -1.98 | 0.048 | 0.386 |
| Solid yield (wt%) | Metal / supported metal | temperature | <300 °C (20) | -7.78 | ≥300 °C (26) | -8.26 | 0.883 | 1.0 |
| Solid yield (wt%) | Metal / supported metal | lignin | lignin ≤ 22 wt% (17) | -9.73 | lignin > 22 wt% (20) | -7.0 | 0.52 | 1.0 |
| Solid yield (wt%) | Other catalyst | temperature | <300 °C (5) | -10.82 | ≥300 °C (9) | -2.7 | 0.649 | 1.0 |
| Solid yield (wt%) | Other catalyst | lignin | lignin ≤ 27 wt% (7) | -9.14 | lignin > 27 wt% (6) | -1.9 | 0.573 | 1.0 |
| Aqueous-phase yield (wt%) | Alkali carbonate | lignin | lignin ≤ 23 wt% (6) | -1.44 | lignin > 23 wt% (8) | 5.08 | 0.121 | 0.121 |
| Gas yield (wt%) | Alkali carbonate | temperature | <300 °C (5) | 1.01 | ≥300 °C (12) | -1.35 | 0.269 | 1.0 |
| Gas yield (wt%) | Alkali carbonate | lignin | lignin ≤ 23 wt% (6) | -0.17 | lignin > 23 wt% (9) | -0.14 | 0.991 | 1.0 |
| Gas yield (wt%) | Alkali hydroxide | lignin | lignin ≤ 27 wt% (6) | -0.71 | lignin > 27 wt% (5) | -2.97 | 0.404 | 1.0 |
| Gas yield (wt%) | Metal / supported metal | temperature | <300 °C (11) | -0.24 | ≥300 °C (12) | 1.47 | 0.388 | 1.0 |
| Gas yield (wt%) | Metal / supported metal | lignin | lignin ≤ 23 wt% (8) | 0.6 | lignin > 23 wt% (11) | -0.06 | 0.758 | 1.0 |
| Bio-oil HHV (MJ/kg) | Alkali carbonate | lignin | lignin ≤ 21 wt% (12) | 1.24 | lignin > 21 wt% (11) | 1.45 | 0.802 | 1.0 |
| Bio-oil HHV (MJ/kg) | Alkali hydroxide | temperature | <300 °C (5) | 0.42 | ≥300 °C (11) | 0.48 | 0.963 | 1.0 |
| Bio-oil HHV (MJ/kg) | Alkali hydroxide | lignin | lignin ≤ 23 wt% (8) | 1.33 | lignin > 23 wt% (9) | 0.28 | 0.419 | 1.0 |
| Bio-oil HHV (MJ/kg) | Metal / supported metal | temperature | <300 °C (12) | 2.1 | ≥300 °C (23) | 0.67 | 0.165 | 0.827 |
| Bio-oil HHV (MJ/kg) | Metal / supported metal | lignin | lignin ≤ 23 wt% (15) | 1.77 | lignin > 23 wt% (17) | 0.71 | 0.327 | 1.0 |
| Energy recovery to bio-oil (%) | Alkali carbonate | lignin | lignin ≤ 21 wt% (10) | 19.83 | lignin > 21 wt% (12) | 7.86 | 0.022 | 0.066 |
| Energy recovery to bio-oil (%) | Alkali hydroxide | lignin | lignin ≤ 23 wt% (7) | 26.42 | lignin > 23 wt% (9) | 2.45 | 0.012 | 0.048 |
| Energy recovery to bio-oil (%) | Metal / supported metal | temperature | <300 °C (10) | 22.13 | ≥300 °C (18) | 15.82 | 0.464 | 0.464 |
| Energy recovery to bio-oil (%) | Metal / supported metal | lignin | lignin ≤ 22 wt% (12) | 25.96 | lignin > 22 wt% (13) | 13.53 | 0.162 | 0.324 |
| Bio-oil N (wt%) | Alkali carbonate | lignin | lignin ≤ 20 wt% (10) | -0.1 | lignin > 20 wt% (10) | 0.05 | 0.291 | 0.872 |
| Bio-oil N (wt%) | Alkali hydroxide | temperature | <300 °C (5) | -0.06 | ≥300 °C (11) | 0.41 | 0.06 | 0.302 |
| Bio-oil N (wt%) | Alkali hydroxide | lignin | lignin ≤ 27 wt% (9) | 0.51 | lignin > 27 wt% (8) | 0.01 | 0.107 | 0.429 |
| Bio-oil N (wt%) | Metal / supported metal | temperature | <300 °C (9) | 0.05 | ≥300 °C (14) | -0.03 | 0.371 | 0.872 |
| Bio-oil N (wt%) | Metal / supported metal | lignin | lignin ≤ 23 wt% (10) | -0.05 | lignin > 23 wt% (11) | 0.03 | 0.333 | 0.872 |




**Table S6.** Catalyst effects on a relative scale (response ratio: ratio of the mean outcome with catalyst to that without, pooled on the log scale and back-transformed to a percentage change). Post-hoc analysis added during internal review.

| Outcome | Catalyst | k | Relative change (%) | 95% CI | 95% PI | I² |
|---|---|---|---|---|---|---|
| Bio-oil yield (wt%) | Acid | 8 | 15.5 | -25.9 to 80.2 | -68 to 316 | 87% |
| Bio-oil yield (wt%) | Alkali carbonate | 32 | 27.0 | 14.2 to 41.1 | -20 to 101 | 60% |
| Bio-oil yield (wt%) | Alkali hydroxide | 24 | 25.5 | 4.0 to 51.6 | -43 to 178 | 79% |
| Bio-oil yield (wt%) | Metal / supported metal | 39 | 32.1 | 19.3 to 46.3 | -21 to 121 | 69% |
| Bio-oil yield (wt%) | Other catalyst | 14 | 12.8 | -19.8 to 58.7 | -66 to 275 | 81% |
| Solid yield (wt%) | Acid | 7 | -32.3 | -65.1 to 31.4 | -90 to 347 | 92% |
| Solid yield (wt%) | Alkali carbonate | 26 | -25.1 | -37.0 to -10.9 | -63 to 54 | 75% |
| Solid yield (wt%) | Alkali hydroxide | 19 | -11.3 | -23.1 to 2.4 | -23 to 2 | 0% |
| Solid yield (wt%) | Metal / supported metal | 36 | -28.1 | -37.8 to -17.0 | -65 to 48 | 74% |
| Solid yield (wt%) | Other catalyst | 13 | -19.2 | -43.5 to 15.7 | -79 to 211 | 99% |
| Aqueous-phase yield (wt%) | Alkali carbonate | 13 | 20.5 | -6.9 to 55.9 | -52 to 200 | 89% |
| Aqueous-phase yield (wt%) | Alkali hydroxide | 8 | 43.6 | -3.0 to 112.6 | -56 to 373 | 96% |
| Aqueous-phase yield (wt%) | Metal / supported metal | 11 | 18.1 | -3.6 to 44.9 | -37 to 121 | 79% |
| Gas yield (wt%) | Alkali carbonate | 13 | -5.4 | -28.6 to 25.3 | -36 to 39 | 0% |
| Gas yield (wt%) | Alkali hydroxide | 8 | -7.8 | -28.1 to 18.2 | -44 to 52 | 18% |
| Gas yield (wt%) | Metal / supported metal | 18 | 19.0 | -0.2 to 41.9 | -20 to 78 | 17% |
| Gas yield (wt%) | Other catalyst | 5 | -14.5 | -35.3 to 13.0 | -61 to 87 | 100% |
| Bio-oil HHV (MJ/kg) | Acid | 5 | 8.9 | -4.0 to 23.6 | -21 to 50 | 81% |
| Bio-oil HHV (MJ/kg) | Alkali carbonate | 22 | 4.3 | 1.7 to 7.1 | 2 to 7 | 32% |
| Bio-oil HHV (MJ/kg) | Alkali hydroxide | 15 | 2.3 | -3.1 to 8.0 | -10 to 16 | 29% |
| Bio-oil HHV (MJ/kg) | Metal / supported metal | 32 | 3.8 | -0.3 to 8.1 | -15 to 27 | 79% |
| Bio-oil HHV (MJ/kg) | Other catalyst | 9 | -2.1 | -7.4 to 3.5 | -8 to 4 | 14% |
| Energy recovery to bio-oil (%) | Alkali carbonate | 21 | 40.0 | 23.4 to 58.8 | 23 to 59 | 0% |
| Energy recovery to bio-oil (%) | Alkali hydroxide | 14 | 26.3 | 6.3 to 50.1 | -7 to 72 | 12% |
| Energy recovery to bio-oil (%) | Metal / supported metal | 25 | 47.6 | 30.1 to 67.5 | -9 to 140 | 60% |
| Energy recovery to bio-oil (%) | Other catalyst | 8 | -13.3 | -45.9 to 38.9 | -76 to 214 | 76% |
| Bio-oil N (wt%) | Acid | 5 | -25.8 | -43.0 to -3.4 | -45 to 0 | 0% |
| Bio-oil N (wt%) | Alkali carbonate | 17 | 0.4 | -19.3 to 24.8 | -56 to 129 | 82% |
| Bio-oil N (wt%) | Alkali hydroxide | 14 | 9.6 | -19.2 to 48.6 | -61 to 210 | 75% |
| Bio-oil N (wt%) | Metal / supported metal | 18 | -2.9 | -20.9 to 19.2 | -59 to 131 | 93% |
| Bio-oil N (wt%) | Other catalyst | 8 | -26.8 | -51.0 to 9.4 | -66 to 59 | 40% |




**Table S7.** Exploratory catalyst dose–response (Addendum F): within-study change per doubling of the catalyst-to-biomass ratio, for the same catalyst class at otherwise identical conditions (classes with ≥ 5 studies).

| Outcome | Catalyst | Studies | Contrasts | Effect per doubling of loading | 95% CI | 95% PI | I² |
|---|---|---|---|---|---|---|---|
| Bio-oil yield (wt%) | Alkali carbonate | 7 | 51 | 0.51 | -4.99 to 6.0 | -11.4 to 12.4 | 63% |
| Bio-oil yield (wt%) | Alkali hydroxide | 5 | 12 | 0.34 | -7.58 to 8.26 | -20.6 to 21.3 | 88% |
| Bio-oil yield (wt%) | Metal / supported metal | 14 | 40 | 4.51 | 0.01 to 9.02 | -10.4 to 19.4 | 77% |
| Solid yield (wt%) | Metal / supported metal | 10 | 29 | -2.3 | -5.22 to 0.61 | -5.3 to 0.7 | 15% |
| Bio-oil HHV (MJ/kg) | Metal / supported metal | 5 | 22 | 0.36 | -2.27 to 2.99 | -4.5 to 5.2 | 44% |
| Energy recovery to bio-oil (%) | Metal / supported metal | 5 | 22 | 4.62 | -3.45 to 12.69 | -16.7 to 25.9 | 85% |




**Table S8.** Exploratory feedstock-family moderators (Addendum F): random-effects mean effects (number of studies) for agricultural residues, woody biomass and technical lignin; Q-test for differences between families, Holm-corrected within outcome × factor.

| Outcome | Change | Agricultural residues (k) | Woody biomass (k) | Technical lignin (k) | Q (df) | p | p (Holm) |
|---|---|---|---|---|---|---|---|
| Bio-oil yield (wt%) | T +10 °C (250–300 °C) | 1.00 (25) | 1.03 (20) | 1.77 (6) | 0.29 (2) | 0.866 | 1.0 |
| Bio-oil yield (wt%) | T +10 °C (300–350 °C) | -0.87 (22) | -0.64 (15) | -1.69 (8) | 1.31 (2) | 0.52 | 1.0 |
| Bio-oil yield (wt%) | Alkali carbonate | 8.16 (15) | 4.90 (11) | — | 1.41 (1) | 0.235 | 0.471 |
| Bio-oil yield (wt%) | Alkali hydroxide | 8.50 (10) | 12.28 (8) | — | 0.28 (1) | 0.594 | 0.594 |
| Bio-oil yield (wt%) | Metal / supported metal | 5.39 (16) | 11.61 (15) | — | 2.88 (1) | 0.09 | 0.27 |
| Solid yield (wt%) | T +10 °C (250–300 °C) | -1.71 (28) | -1.80 (20) | -0.59 (6) | 4.26 (2) | 0.119 | 0.139 |
| Solid yield (wt%) | T +10 °C (300–350 °C) | -0.53 (19) | -1.16 (14) | 0.20 (8) | 5.34 (2) | 0.069 | 0.139 |
| Solid yield (wt%) | Alkali carbonate | -6.05 (11) | -10.84 (10) | — | 1.01 (1) | 0.314 | 0.314 |
| Solid yield (wt%) | Alkali hydroxide | -2.33 (8) | -9.60 (7) | — | 2.95 (1) | 0.086 | 0.172 |
| Solid yield (wt%) | Metal / supported metal | -3.21 (16) | -15.36 (12) | — | 6.22 (1) | 0.013 | 0.038 |



# S5. Nitrogen content of bio-oil


**Table S9.** Within-study meta-analysis for the nitrogen content of bio-oil (wt%).

| Outcome | Change | Effect | 95% CI | 95% PI | k | Contrasts | I² | P(increase) |
|---|---|---|---|---|---|---|---|---|
| Bio-oil N (wt%) | T +10 °C (<250 °C) | -0.03 | -0.08 to 0.03 | -0.15 to 0.10 | 5 | 14 | 55% | 0.24 |
| Bio-oil N (wt%) | T +10 °C (250–300 °C) | -0.0 | -0.02 to 0.01 | -0.02 to 0.01 | 23 | 70 | 0% | 0.31 |
| Bio-oil N (wt%) | T +10 °C (300–350 °C) | 0.01 | -0.00 to 0.02 | -0.03 to 0.05 | 20 | 67 | 47% | 0.73 |
| Bio-oil N (wt%) | T +10 °C (≥350 °C) | 0.0 | -0.02 to 0.02 | -0.03 to 0.03 | 11 | 20 | 25% | 0.61 |
| Bio-oil N (wt%) | Residence time ×2 | 0.07 | -0.05 to 0.19 | -0.05 to 0.19 | 18 | 78 | 0% | 0.9 |
| Bio-oil N (wt%) | Solid loading +10 pp | -0.14 | -0.36 to 0.07 | -0.39 to 0.11 | 5 | 17 | 0% | 0.03 |
| Bio-oil N (wt%) | Alkali carbonate | -0.05 | -0.20 to 0.11 | -0.63 to 0.54 | 19 | 43 | 71% | 0.43 |
| Bio-oil N (wt%) | Alkali hydroxide | 0.28 | -0.13 to 0.70 | -1.23 to 1.80 | 15 | 31 | 83% | 0.66 |
| Bio-oil N (wt%) | Metal / supported metal | -0.01 | -0.10 to 0.08 | -0.19 to 0.18 | 21 | 27 | 0% | 0.46 |
| Bio-oil N (wt%) | Acid | -0.12 | -0.27 to 0.02 | -0.43 to 0.18 | 5 | 13 | 27% | 0.1 |
| Bio-oil N (wt%) | Other catalyst | -0.2 | -0.42 to 0.02 | -0.69 to 0.30 | 9 | 12 | 16% | 0.17 |



# S6. Transfer of literature-trained machine-learning models to new studies

Earlier analyses of the same database, carried out under the original protocol and its addenda A–D, evaluated twelve learners for bio-oil and solid yields with study-grouped cross-validation, on the 38 locked studies and on an external hydrochar database (Abdeldayem et al., 2025). They are summarised here because they establish the size of the laboratory effect used in Section 3.5 and the value of local runs used in Section 3.8. Random splitting of runs overstated accuracy about two-fold compared with predicting unseen studies (Table S10, Fig. S1). The between-study share of out-of-study residual variance was 0.65 (95% CI 0.53–0.76) for bio-oil and 0.49 (0.40–0.61) for solid yield (Table S11), with offset standard deviations of 12.5 and 9.7 wt%; reported work-up and yield-basis descriptors did not explain these offsets. Conformal prediction intervals calibrated across studies covered 0.82–0.91 of runs of new studies, compared with 0.46–0.61 for intervals calibrated on random runs (Table S12). In a retrospective simulated deployment, three runs measured in a screening design and combined with the literature model reduced the median per-study error by 1.6–6.4 wt% across development, locked and external settings, although for locked bio-oil studies the local runs alone were more accurate (Table S13, Fig. S2).


**Table S10.** Random-row versus study-grouped cross-validation on development studies (base features; grouped CV averaged over 3 seeds).

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




**Table S11.** Decomposition of out-of-study error and contribution of work-up/reporting descriptors (P).

| Target | τ² (between) | σ²w (within) | Between-study share [95% CI] | Median study RMSE base → base+P | Δ median [95% CI]; p (one-sided) | Rank-biserial | Meta-regression LOSO R² (perm. p) |
|---|---|---|---|---|---|---|---|
| Bio-oil | 156.7 | 85.6 | 0.65 [0.53, 0.76] | 12.45 → 12.84 | 0.04 [-0.38, 0.60]; 0.804 | 0.09 | -0.031 (0.714) |
| Solid | 94.6 | 97.7 | 0.49 [0.40, 0.61] | 10.86 → 11.05 | 0.05 [-0.15, 0.25]; 0.545 | 0.01 | -0.047 (0.910) |




**Table S12.** Empirical coverage of 90% prediction intervals: row-calibrated (RC) vs study-calibrated (SC).

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




**Table S13.** Retrospective simulated deployment (E15): a new laboratory measures k runs in screening-design order, and the runs from position 6 onward are predicted by A (literature model only), B (STRATA: literature model shifted by the shrunk mean residual of the k runs) or C (mean of the k local runs). RMSE: median per-study RMSE (wt%); Cov.: study-weighted coverage of 90% intervals re-calibrated for each k and strategy; ±HW: mean interval half-width (wt%). Dev.: unseen development studies in study-grouped CV (3 seeds); Locked: studies held out before modelling (≥ 11 runs); 4TU: external hydrochar database (feedstock series as pseudo-studies). MAE is given in the supplementary deployment table.

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




![**Fig. S1.** Root-mean-square error of 12 learners under random-row five-fold cross-validation (circles) and study-grouped ten-fold cross-validation (squares; mean of three seeds), base features.](/home/user/rp_c_12/figures/fig03_random_vs_grouped.png){width=16cm}



![**Fig. S2.** Retrospective simulated deployment (screening-design run order): median per-study RMSE of the remaining runs and half-width of re-calibrated 90% intervals for the literature model alone (A), the literature model anchored by k local runs (B) and the local runs alone (C).](/home/user/rp_c_12/figures/fig14_deployment.png){width=16cm}


# S7. Reproducibility

A single command regenerates every result file, table and figure from the public data, and a second command regenerates the manuscript and this document from those files; library versions and CPU details are written to a log at run time. The meta-analysis is implemented in `src/meta/within_study.py` and `experiments/e18_meta.py`, with unit tests that verify that laboratory offsets cancel in the contrasts and that the random-effects estimator agrees with an independent implementation. The code, the locked study list, configuration files, result files and per-contrast data are available from the corresponding author on reasonable request.


