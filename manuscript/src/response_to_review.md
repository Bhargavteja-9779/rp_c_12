---
title: "Response to the pre-submission review"
---

We thank the reviewer for a detailed and constructive pre-submission review. Every point was addressed; the new analyses were specified in a protocol addendum (Addendum D) that was committed before any of them was run. Below, reviewer comments are paraphrased in bold, followed by our response and the location of the change. Numbers are those of the revised manuscript.

**1. Reposition the paper around the problem of a new laboratory deploying a literature-trained model, and present a framework (STRATA-Lab).**

Done. The title, abstract, highlights and introduction were rewritten around the new-laboratory deployment problem (Section 1, second paragraph), which is defined by four needs: a prediction before any experiment, an honest uncertainty, guidance on the first runs, and knowing when to trust the literature model versus local runs. STRATA-Lab is introduced as a six-step workflow ({{FREF:fig16_strata_lab_workflow}}) and evaluated in the new Sections 3.4–3.6 and 3.9. New title: "From literature to laboratory: an uncertainty-aware framework for transferring machine-learning models of hydrothermal biomass conversion and planning first experiments". We did not use "reliable hydrothermal biomass conversion" from the suggested title, because the work evaluates models and planning, not process reliability.

**2. Improvement 1 — sequential local adaptation with strict support/query separation, k = 0, 1, 2, 3, 5; RMSE, MAE, coverage and width; call it simulated if no prospective order exists.**

Done (E15; Section 2.6, Section 3.4, {{TREF:table_v3_deployment}}, {{FREF:fig14_deployment}}, {{TREF:table_v3_deployment_other_orders}} and {{TREF:table_v3_deployment_tests}}). For every study with ≥ 11 runs, the first *k* runs in a given order are measured and the runs from position 6 onward form a fixed query set, identical for all *k*, so support and query never overlap. Three orders were evaluated: a screening design (centre, lowest and highest temperature, then maximin), the reported order and 20 random orders. Because the database order is not chronological, the analysis is labelled a *retrospective simulated deployment* throughout. Intervals are re-calibrated for each *k*, order and strategy by replaying the identical procedure on calibration studies. Results are reported for unseen development studies, once for the locked studies and for the external hydrochar database. For example, for unseen development studies the median per-study RMSE for bio-oil was {{dep_dev_biooil_design_0_A_rmse}} wt% without local runs and {{dep_dev_biooil_design_1_B_rmse}}, {{dep_dev_biooil_design_3_B_rmse}} and {{dep_dev_biooil_design_5_B_rmse}} wt% with one, three and five runs; Study-weighted coverage and width are in {{TREF:table_v3_deployment}} and MAE in {{TREF:table_v3_deployment_long}}.

**3. Improvement 2 — an uncertainty-based decision system with thresholds derived from validation data.**

Done (E16; Section 3.5, {{TREF:table_v3_decision}}). (a) An applicability-domain score with a threshold fixed in advance as the 95th percentile of development scores; (b) the number of local runs needed for a 90% half-width of ±10, ±15 or ±20 wt%, read from development results and checked on locked studies; (c) a rule "local-only if flagged, otherwise STRATA". We report the results as they came out: the score correlated with error on development studies (ρ = {{ad_biooil_rho}} and {{ad_solid_rho}}), but the pre-registered threshold flagged no locked study ({{ad_biooil_lflag}}/{{ad_biooil_lnst}} and {{ad_solid_lflag}}/{{ad_solid_lnst}}), so the decision rule could not be tested; ±20 wt% was reached after {{need_solid_20}} run for solids and not within five runs for bio-oil. These negative results shaped the final workflow, which asks the laboratory to compare literature-anchored and local-only predictions rather than rely on a distance flag.

**4. Improvement 3 — either model all four phases with closure or limit the claims explicitly (Option A).**

Option A was adopted. The scope statement is in the last paragraph of the Introduction, {{TREF:table_v3_novelty}} and the Limitations: only bio-oil and solid yields are modelled; aqueous and gas phases and mass closure are not, and no four-phase claim is made.

**5. Improvement 4 — a laboratory case study comparing A (literature only), B (STRATA) and C (local only): error, coverage, measurements required, error reduction per measurement, regret.**

Done (E17; Section 3.6, {{TREF:table_v3_case_study}}, {{FREF:fig15_case_study}}). One locked study per target was selected by a pre-specified rule (≥ 11 runs, most distinct temperatures). Runs are measured one at a time in screening-design order and all remaining runs are predicted after each measurement; the table reports error of A, B and C, coverage and half-width of B and the regret of choosing the predicted-best run, against random choice. The two cases show the two regimes found across studies: for duckweed HTC STRATA was best and narrowed its interval from ±{{case_solid_0_halfwidth_B}} to ±{{case_solid_5_halfwidth_B}} wt% with full coverage, whereas for *Spirulina* HTL the local mean was best from the second run. Error reduction per measurement is reported for all settings in Section 3.4 (e.g. {{gainper_dev_biooil_1}} wt% for the first bio-oil run in development; {{gainper_locked_solid_1}} wt% for the first solid run in locked studies). We also report a data artefact found in the solid case (a 20 °C entry in the source database) rather than removing it.

**6. Novelty relative to Elfetni et al. (Bioresour. Technol., online August 2026) and the SSRN preprint; a direct comparison table; disclosure of shared authorship or overlap.**

Done ({{TREF:table_v3_novelty}} and Section 1, third paragraph). The table compares data, targets, validation, pre-specification, uncertainty, local adaptation, decision support and physical admissibility, using the abstracts of both works. None of the present authors is an author of either work; the overlap is the shared, openly licensed database, which is stated in the text, the table and the cover letter. The differences claimed are: coverage evaluated on unseen, locked and external studies; literature-anchored vs local-only comparison with re-calibrated intervals at each *k* and in realistic run orders; decision-support analyses; and a locked test set. We state explicitly that local calibration reducing error was already shown by Elfetni et al. (2027).

**7. Remove placeholders and unfinished statements.**

Done. All "(to be completed by the authors)" notes were removed; CRediT, funding, competing-interest and data-availability statements are complete. The only remaining placeholders are the second author's name, affiliation and e-mail and the first author's affiliation, which the authors will insert at submission.

**8. Reproducibility and repository claims must be accurate.**

Done. The claim of a public repository and a fresh-clone test was removed. The Data availability statement now gives the DOIs of both public datasets, and states that code, the locked study list, configuration files and result files are available from the corresponding author on reasonable request (Section 2.9, Supplementary Section S10).

**9. Label the validation as retrospective; state that no experimental validation was performed.**

Done in the abstract ("retrospective simulated deployment"), Section 1 (last paragraph), Section 2.6 (first sentence), Section 3.10 (first sentence) and the cover letter.

**10. Literature search beyond PubMed, with full search strings, eligibility criteria, dates and a reproducible selection.**

Done (Section 1, first paragraph; Supplementary Section S1 and {{TREF:tableS_v3_prisma}}). A scripted search of PubMed, Crossref and OpenAlex was run on {{lit3_date}}; OpenAlex refused anonymous requests on that date and contributed no records, which is reported. All strings, the window, rule-based eligibility criteria E1–E4 and the record flow ({{lit3_total}} identified, {{lit3_dedup}} after de-duplication, {{lit3_included}} included) are given; raw records are stored for re-screening. Two screening rules were corrected after a check and re-applied to the stored records; this is disclosed in Supplementary Section S2.

**11. Be transparent about pre-registration.**

Done (Section 2.2, Supplementary Section S2, {{TREF:table_v2_timeline}}). We now state that the protocol was registered by timestamped commits in a version-controlled repository hosted on GitHub, not in a public registry, that this is weaker than formal pre-registration, which addenda were exploratory, and which analyses were added after results were known. Addendum D (this revision) was committed before E15–E17 were run.

**12. Make interval width a central outcome.**

Done. Width is reported for every setting ({{TREF:table4_coverage}}, {{TREF:table_v3_deployment}}, {{TREF:table_v3_decision}}, {{TREF:table_v3_case_study}}), discussed as the central quantity in Section 3.3 and used for the runs-needed analysis (Section 3.5). The conclusion that literature models support screening rather than optimisation rests on the half-widths of ±{{hw_solid_5}}–{{hw_biooil_1}} wt% remaining after one to five local runs.

**13. Restructure: condense the failed trend and ranking analyses, expand uncertainty and adaptation, add case-study and decision sections.**

Done. Trend and ranking results were condensed into Section 3.8 (one paragraph) with figures and tables moved to Supplementary Section S7; the metadata analysis was merged into Section 3.2; new Sections 3.4 (sequential adaptation), 3.5 (decision support), 3.6 (case studies) and 3.9 (STRATA-Lab in practice) were added.

**14. Suggested figures (transferability across feedstock families, improvement with local measurements, workflow, predicted vs observed with intervals).**

Added: workflow ({{FREF:fig16_strata_lab_workflow}}), improvement with local measurements ({{FREF:fig14_deployment}}), predicted vs observed with intervals for locked studies ({{FREF:fig17_pred_obs_intervals}}) and case studies ({{FREF:fig15_case_study}}). Transferability across feedstock families, time, locked studies and the external database is shown by the coverage figure ({{FREF:fig05_coverage}}) and the generalisation tables ({{TREF:table6_locked_test}}; {{TREF:table7_generalisation}}).

**15. Do not report monetary savings.**

No monetary savings are reported; Section 3.9 states why.

**Journal choice.** We retained *Bioresource Technology*: its scope covers thermochemical conversion and the application of machine learning to bioresource processes, and the closest prior work appeared there.
