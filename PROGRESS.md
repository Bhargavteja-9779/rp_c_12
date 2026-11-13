# PROGRESS (resume file)

Branch: claude/autonomous-research-discovery-1uqqmr. Resume by reading this file + `git log`.

## Decisions (final)
* Target journal: **Bioresource Technology** (see journal_selection/).
* Topic: transferability of literature-trained ML models for hydrothermal conversion of biomass to *unseen source studies*:
  between-study heterogeneity decomposition, work-up/reporting descriptors, study-valid conformal uncertainty, k-shot empirical-Bayes study adaptation.
* Data: RADAR4Chem HTT/HTL v1.0.0 (doi:10.22000/8bnbhqccf4aq7kea, CC BY 4.0, sha256 c8827a37...), external: 4TU hydrochar DB (doi:10.4121/834c3f22-..., CC BY 4.0).
* Locked study-level test split: code/config/locked_test_studies.json (38 studies, 755 rows). NEVER regenerate. Do not inspect test results until the final run.
* Closest prior art: Elfetni et al. 2026 Bioresour Technol 10.1016/j.biortech.2026.135587 (conservation surrogate, publication-aware validation, k-shot point recalibration, random-split conformal).

## Phase status
- [x] Phase 0-2 journal + topic
- [x] Phase 3-5 literature matrix / novelty / RQs  (supplementary/literature/)
- [x] Phase 6 protocol pre-registration (code/config/PROTOCOL.md)
- [x] Phase 9-10 implementation, run_all (quick mode verification in progress)
- [x] Experiments (E1–E11, locked test once at commit 639845a)
- [x] Manuscript, reviews 1-10, DOCX/PDF, supplementary, highlights, graphical abstract, cover letter, audits, risk report

## STATUS: COMPLETE (2026-11-11). Decision: READY FOR SUBMISSION conditional on author actions (see REVIEW/rejection_risk_report.md).

## Running state (update as you go)
* 2026-11-11 03:15 UTC: E1 full DONE (48 cells). STRATA learner = xgb. E3 full running. Then: E3b full (exploratory), E5 parts robustness,temporal_family,external, E6-8 full, THEN locked test once (`e5_generalization.py full locked`), analyze, tables, figures, build manuscript, reviews.
* Full E1 launched 22:00 UTC 2026-11-10: `cd code && python3 experiments/e1_benchmark.py full` (cells cached in results/experiment_logs/e1_cells; rerun resumes).
* Next full stages: e3_strata.py full -> e5_generalization.py full (locked test LAST, after all decisions) -> e6_e7_e8.py full -> analyze -> tables -> figures.
* Manuscript sources: manuscript/src/*.md (tokens {{...}} filled by builder from results); references built by manuscript/src/build_refs.py ONLY from verified metadata.

## UPGRADE v2 (started 2026-11-13, user: "it will get rejected, improvise to max level")
* Addendum A (E12 trend transfer, T1–T5), A2 (HHV, C targets), B (E14 exploratory), C (locked confirmation) registered in code/config/PROTOCOL.md before each run.
* Results: T1–T3 NOT supported (dev); ranking beat rules of thumb in dev (exploratory) but NOT confirmed on locked (C1 p_Holm 0.62);
  locked contrast R² favours W/PD but driven by 2 studies (n.s. per study). E13 model-free: temperature-trend directions agree across labs.
* v2 framing: pre-registered capability audit (levels, trends, ranking, uncertainty, anchoring) + trend atlas + reporting checklist.
* Next: manuscript rewrite (v2 tokens/tables/figures), rebuild, re-review rounds 11-15, audits, push.
