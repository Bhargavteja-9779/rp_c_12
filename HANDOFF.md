# HANDOFF — how to continue this project from a new account/session

Repository: `bhargavteja-9779/rp_c_12`, branch `claude/autonomous-research-discovery-1uqqmr` (everything is committed and pushed).
Author of record: P N Bhargav Teja (first author); second author = supervisor, corresponding author (name/affiliation/e-mail placeholders).
Declarations requested by the author: no funding; no competing interests; data = public DOIs; code available on request; CRediT: first
author all roles except supervision; second author supervision + review & editing.

## History
- v1–v2 (Nov 2026): pre-registered audit of literature-trained ML for HTL/HTC (locked 38 studies, STRATA intervals, trend/ranking tests).
- v3 (2026-11-18): reframed after a professor's review (STRATA-Lab, deployment simulation E15–E17). Submitted to Bioresource
  Technology → **desk-rejected 2026-11-25: "no novelty / not at the level of the journal and its readers"**.
- v4 (from 2026-11-25): new primary contribution = **first within-study meta-analysis of HTL/HTC process effects** (PROTOCOL Addendum E,
  registered before any effect was computed; deviations E-1, E-2 logged). See REVIEW/v4_rejection_diagnosis_and_bt_benchmark.md.

## Where things are
- Protocol and all addenda/deviations: `code/config/PROTOCOL.md`
- Data (vendored, SHA-256 checked): `code/data/raw/` (RADAR4Chem doi:10.22000/8bnbhqccf4aq7kea; 4TU doi:10.4121/834c3f22-f46a-4808-a0fe-46298be6a133.v1)
- Meta-analysis code: `code/src/meta/within_study.py`, `code/experiments/e18_meta.py` (`python experiments/e18_meta.py full dev|locked|lab`),
  tests `code/tests/test_meta.py`. Figures/tables: `code/src/visualization/figures_v4.py`.
- Results: `results/e18_*`, `results/statistics/e18_*.json`; tables `tables/table_v4_*`; figures `figures/fig18–fig23`, `graphical_abstract_v4`.
- Manuscript sources: `manuscript/src/*.md` (tokens {{...}} filled from result files by `manuscript_values.py`; build with
  `python manuscript/src/build_manuscript.py`; references only from verified metadata `references.json` built by `build_refs.py`
  from `supplementary/literature/references_verified.json` (add DOIs with `verify_refs.py <batch.json>`).
- Previous versions' manuscript text is in git history (v3 commit 41673c4).
- BT benchmark corpus: `journal_selection/bt_benchmark/bt_abstracts.json`.

## Key v4 results (development = 150 studies; locked = 38 studies, one look)
- Within-study effects (REML, HKSJ CI, 95% PI): bio-oil +1.07 wt% per 10 °C at 250–300 °C (k=62), −0.75 at 300–350 °C; solid −1.74 at
  250–300 °C (k=64); catalysts raise bio-oil by +5.5 (alkali carbonate, k=32) to +8.5 wt% (metal/supported, k=39), lower solid by 4.5–8.2
  wt%, raise energy recovery by 12–20 points; heterogeneity large (I² ≈ 0.8; PIs span zero for catalysts).
- Laboratory effect: SD of between-study offsets 12.5 (ML) / 15.8 (mixed model) wt% bio-oil; 9.7 / 14.7 wt% solid (ICC ≈ 0.7–0.76).
- Pooled XGBoost partial-dependence effects agree in sign with all 15 significant meta effects (ρ = 0.92); pooled linear model: 1 reversal,
  38 % outside CI.
- Pre-registered locked test (E5): meta mean effects did NOT predict locked within-study changes better than XGBoost or zero (Holm p ≈ 0.94);
  temperature effects replicated in locked studies; PI coverage of locked study effects 0.86.

## Standing instructions from the author
Keep improving until the paper is top quality; compare with BT papers and match their style; save everything; continue autonomously.
Journal constraint: Q1, high IF, not MDPI, verified final acceptance ≤ 72 days. Never fabricate results or citations.
If a session limit is reached, schedule a resume reminder (~5h15m) and continue from PROGRESS.md / this file.

## Status at end of session (2026-11-25)
- v4 manuscript complete and built: manuscript/Final_Manuscript.{docx,pdf}, Manuscript_anonymised, Supplementary_Material, Title_Page,
  Highlights, cover_letter, Graphical_Abstract; ZIP: submission/BioresourceTechnology_submission_v4.zip.
- Review log: REVIEW/review_v4_rounds.md; risk report: REVIEW/rejection_risk_report.md (v4 section on top).
- Journal: Bioresource Technology remains the best verified fit (median received→accepted 75 d for all research articles; fallbacks
  measured slower: journal_selection/data/fallback_timelines_v4.json). No journal can guarantee ≤ 72 d.
- Ideas for further strengthening (not done): extract additional HTL/HTC experiments published after the database cut-off (2026) as a
  truly prospective replication; three-level/robust-variance meta-analysis as additional sensitivity; mechanistic discussion with
  full-text-verified literature; experimental validation of the catalyst prior in the author's laboratory (would most raise impact).
