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
- [ ] Phase 3-5 literature matrix / novelty / RQs  (supplementary/literature/)
- [ ] Phase 6 protocol pre-registration (code/config/PROTOCOL.md)
- [ ] Phase 9-10 implementation, run_all
- [ ] Experiments
- [ ] Manuscript, reviews 1-10, DOCX, cover letter, risk report
