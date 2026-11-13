# Final audit (Phases 22, 23, 34, 35, 41, 42)

## A. Claim → evidence map (Phase 22)
Every number in the manuscript is inserted by `manuscript/src/build_manuscript.py` from result files via
`manuscript_values.py` (369 values; log in `manuscript/build_log.json`). Unresolved tokens abort the build.
Direction-dependent sentences (e.g. whether P helped, whether shrinkage beat the raw offset) are generated from
the test outcomes, not written in advance. Hard-coded numbers in the templates were listed programmatically; all
are design facts (3,693 runs, 188 studies, 38 locked studies, seeds, folds, 2,000 bootstrap replicates, 1,000
permutations, nominal 0.90).

| Claim (abstract / highlights / conclusions) | Evidence | Experiment | Table / Figure |
|---|---|---|---|
| Random splits overstate accuracy ~two-fold (flexible learners; ratio 1.52–2.61 bio-oil) | `tables/table_e1_benchmark_wide.csv` | E1 | Table 2, Fig. 3, Fig. 10 |
| Study offsets = 0.65 (0.53–0.76) and 0.49 (0.40–0.61) of out-of-study error variance | `statistics.json → e3.*.heterogeneity` | E3 | Table 3, Fig. 4 |
| Work-up / yield-basis descriptors did not reduce error | `e3.*.protocol_ablation`, `statistics/meta_regression.json`, locked ablation | E3, E8 | Table 3 |
| RC intervals under-cover (0.57/0.61 dev; 0.60/0.46 locked) | `e3.*.coverage`, `locked_coverage_ci` | E3, E5 | Table 4, Fig. 5 |
| SC raises coverage to 0.82–0.91 | idem | E3, E5 | Table 4, Fig. 5 |
| SC valid for all 7 base learners; RC failure grows with capacity | `results/e9_base_learners.csv` | E9 | Table S10 |
| k = 3 EB offset: 12.37 → 8.47 wt% (bio-oil), coverage 0.91 | `e3.*.kshot_summary/kshot_tests` | E3 | Table 5, Fig. 6 |
| On locked studies no learner predicted bio-oil yield substantially better than the mean | `e5a_locked_test_metrics.csv` | E5a | Table 6 |
| Cross-study duplicates make grouped estimates slightly optimistic | `e10_duplicate_audit.json` | E10 | §3.6 |
| STRATA overhead seconds | `e11_overhead.csv` | E11 | §3.6 |

Statements weakened or removed after audit/review: "all flexible learners" range; "restores coverage" → "largely
restores / raised to 0.82–0.91"; "can be combined with physically admissible surrogates" → "could be applied …
not tested"; temporal "in line with" → computed comparison; novelty of STRATA → assembly of established
constructions; two error-analysis sentences that were not computed were replaced by computed statements.

## B. Citation audit (Phase 23)
See `REVIEW/citation_audit.md`. 41 references, every one generated from verified metadata (Crossref DOI with
title similarity ≥ 0.9, arXiv API, JMLR/NeurIPS/PMLR pages, DataCite). One reference initially typed from memory
(wrong title/authors) was deleted before use; the reference list is never hand-written. Holm (1979) could not
be verified and is not cited (the procedure is cited via Demšar, 2006).

## C. Consistency audit (Phase 34)
| Link | Check | Result |
|---|---|---|
| Title ↔ abstract ↔ contributions | transfer to unseen studies + study-calibrated intervals | consistent |
| Method ↔ code | review_04 table | consistent |
| Equations ↔ code | MoM τ²/σ²_w (`variance_components`), weighted quantile (`weighted_conformal_quantile`), shrinkage k/(k+λ) (`shrink_factor`) | consistent; unit-tested |
| Experiments mentioned ↔ exist | E1–E11 scripts and outputs present | yes |
| Tables ↔ data | generated from CSV/JSON | yes |
| Figures ↔ data | generated from result files (Fig. 1 is a schematic) | yes |
| Numbers ↔ results | token build | yes |

## D. Reproducibility audit (Phase 35)
Fresh clone of the pushed branch → `python run_all.py --mode quick` (result recorded below by the audit run).
Data are vendored with checksums; the locked list is committed; quick mode never touches the locked studies.
Manuscript rebuild needs pandoc + LibreOffice (incl. `libreoffice-math`).

**Result (2026-11-11):** fresh clone of the pushed branch → `python run_all.py --mode quick` completed all 12 stages
(14 unit tests passed) in 344 s on 4 CPU cores. In the same clone, `python run_all.py --mode full --only analyze tables figures`
followed by `python manuscript/src/build_manuscript.py` regenerated the manuscript from the committed raw results:
**all 369 inserted values were identical** to the submitted build (0 differences). Re-running the full experiments
(E1–E11) from scratch was not repeated in the clone (≈1.5–2 h); it uses the same code and seeds.

## E. Final self-decision (Phase 42)
See `REVIEW/rejection_risk_report.md` §Decision.


## v2 addendum (2026-11-13)
* Claims added in v2 (trend atlas, contrast accuracy, ranking, quality targets, capability matrix) are generated from
  `results/statistics_v2.json`, `results/e13*`, `results/e12_*`, `results/e14*` via `manuscript_values.py` (647 values).
* Directional headings of §3.4/§3.5 were checked against the outcomes (T1–T3 not supported; C1 not confirmed).
* Figure numbering is now symbolic (`{{FIGREF:…}}`) and resolved at build time; supplementary references were checked one by one.
* Two review analyses first computed ad hoc were moved into scripts and verified byte-identical (review_12.md, 12.5).
* Fresh-clone quick run of the v2 pipeline: all 20 stages exit 0 in 736 s (`results/experiment_logs/repro_quick.json`).
* Pre-registration audit trail: Supplementary Table S16 (generated from `git log`).
