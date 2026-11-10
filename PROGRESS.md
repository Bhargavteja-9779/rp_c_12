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
- [ ] Experiments
- [ ] Manuscript, reviews 1-10, DOCX, cover letter, risk report

## Running state (update as you go)
* Full E1 launched 22:00 UTC 2026-11-10: `cd code && python3 experiments/e1_benchmark.py full` (cells cached in results/experiment_logs/e1_cells; rerun resumes).
* Next full stages: e3_strata.py full -> e5_generalization.py full (locked test LAST, after all decisions) -> e6_e7_e8.py full -> analyze -> tables -> figures.
* Manuscript sources: manuscript/src/*.md (tokens {{...}} filled by builder from results); references built by manuscript/src/build_refs.py ONLY from verified metadata.
