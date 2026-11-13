# STRATA — study-level transfer and calibrated uncertainty for literature-trained hydrothermal-conversion models

Code and data to reproduce every number, table and figure of the manuscript
*"What can machine-learning models trained on published hydrothermal-conversion data tell a new laboratory? A pre-registered
audit with locked test studies"*
(submitted to *Bioresource Technology*).

## 1. Install
```bash
conda env create -f environment.yml && conda activate strata-htl
# or: python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```
Tested: Python 3.13, Linux x86-64, 4 CPU cores, 15 GB RAM, no GPU. No accelerator is needed; `src/utils.py`
detects CPU / CUDA / Apple-Silicon MPS but none of the reported learners uses an accelerator.

## 2. Data (included, CC BY 4.0)
| File | Source | Licence | Checksum |
|---|---|---|---|
| `data/raw/htt_radar_v1/master_dataset.csv` | Elfetni, S. (2026). *Unified, curated dataset of biomass hydrothermal treatment/liquefaction experiments …* Version 1.0.0. RADAR4Chem. doi:10.22000/8bnbhqccf4aq7kea | CC BY 4.0 (see `NOTICE.md`, `LICENSE`) | sha256 `c8827a378879ce9d8d1ed7539e451b7b741eec30c5cc070487e3f467a4a42a6b` (verified at load time) |
| `data/raw/htc_4tu/Full DatabaseX.xlsx` | 4TU.ResearchData, doi:10.4121/834c3f22-f46a-4808-a0fe-46298be6a133.v1 | CC BY 4.0 | — |

To re-download instead of using the vendored copies:
```bash
curl -L -o radar.tar "https://www.radar-service.eu/radar-backend/archives/8bnbhqccf4aq7kea/versions/1/content"
tar -xf radar.tar   # master_dataset.csv is under 10.22000-8bnbhqccf4aq7kea/data/dataset/RADAR_dataset_release_v1.0.0/
curl -L -o "Full DatabaseX.xlsx" "https://data.4tu.nl/file/834c3f22-f46a-4808-a0fe-46298be6a133/f946de47-9c58-45cc-8e0d-e4bbe6b05620"
```

## 3. Locked test split
`config/locked_test_studies.json` lists the 38 source publications (20 %, seed 20261110) held out **before any model
was fitted** (see git history). `src/data/lock_split.py` refuses to regenerate it. Quick mode never touches it.

## 4. Run
```bash
python run_all.py --mode quick     # ~12 min on 4 cores (measured from a fresh clone): pipeline check; outputs in code/_quick/
python run_all.py --mode full      # full study (roughly 1.5–2 h of compute on 4 cores); outputs in ../results ../figures ../tables
python run_all.py --mode full --only analyze tables figures   # regenerate statistics/tables/figures from saved results
python -m pytest -q tests          # unit tests (checksum, split disjointness, conformal maths, k-shot masking, Holm)
```
Stages: `e1` benchmark (12 learners × 2 targets × 2 feature sets; random vs study-grouped CV) → `e3` STRATA nested
evaluation (heterogeneity, protocol ablation, RC vs SC conformal, k-shot) → `e5` robustness, temporal, family-out,
external, locked test → `e678` efficiency, sensitivity, error analysis, meta-regression → post-hoc/review analyses `e3b`
(adaptive intervals), `e9` (base learners), `e10` (cross-study duplicate audit), `e11` (STRATA overhead) → `analyze` → `tables` → `figures`.
The manuscript, supplementary material and cover letter are rebuilt from these files with
`python ../manuscript/src/build_manuscript.py` (requires pandoc and LibreOffice incl. `libreoffice-math` for the PDF).

## 5. Where each manuscript number comes from
| Manuscript item | File |
|---|---|
| Table 1 | `tables/table1_data.md` |
| Table 2, Fig. 3, Fig. 10 | `tables/table2_benchmark.md`, `results/e1_benchmark.csv`, `results/predictions/e1_*.csv.gz` |
| Table 3, Fig. 4 | `results/statistics.json → e3.<target>.heterogeneity / protocol_ablation`, `results/statistics/meta_regression.json` |
| Table 4, Fig. 5 | `results/statistics.json → e3.<target>.coverage`, `results/e5*_coverage.csv` |
| Table 5, Fig. 6 | `results/statistics.json → e3.<target>.kshot_summary / kshot_tests` |
| Table 6 | `results/e5a_locked_test_metrics.csv` |
| Table 7 | `results/e5bc_temporal_family_metrics.csv`, `results/e5d_external_metrics.csv` |
| Table 8, Fig. 8 | `results/e6_efficiency.csv` |
| Fig. 7 | `results/e4_robustness.csv` |
| Fig. 9 | `results/e8_error_analysis.csv` |
| Sensitivity (Supplementary) | `results/e7_sensitivity.csv` |
| Table S10 (base learners) | `results/e9_base_learners*.csv` |
| Duplicate audit (Sect. 3.6) | `results/e10_duplicate_audit.json` |
| Overhead (Sect. 3.6) | `results/e11_overhead.csv` |
| Adaptive intervals (Suppl. S4) | `results/e3b_adaptive_summary.csv` |

## 6. Configuration
`config/default.yaml` (seeds, folds, budgets, α, k values) and `config/PROTOCOL.md` (pre-registered analysis plan with
deviations log). Changing a seed or budget changes results; reported results use the committed values.

## 7. Layout
```
code/
  run_all.py  requirements.txt  environment.yml  README.md
  config/     default.yaml, PROTOCOL.md, locked_test_studies.json
  data/raw/   vendored CC-BY datasets
  src/data            loading, exclusions, feature construction (row-wise, leakage-free)
  src/preprocessing   (fold-dependent preprocessing lives inside each learner pipeline; see src/models/registry.py)
  src/models          registry.py (12 learners), strata.py (conformal quantiles, variance components, k-shot EB)
  src/evaluation      core.py (splits, metrics, tuning, OOF prediction)
  src/statistics      stats.py (Wilcoxon, Holm, bootstrap), analyze.py (→ statistics.json, metrics.json, raw_results.csv)
  src/visualization   figures.py, tables.py
  experiments/        e1_benchmark.py, e3_strata.py, e5_generalization.py, e6_e7_e8.py, common.py
  tests/              test_core.py
```

## 8. Licence
Code: MIT. Data: CC BY 4.0 (original authors; see data folders).
