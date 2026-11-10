# Literature analysis, gap analysis and novelty map

All bibliographic data were verified against Crossref (DOI), arXiv, JMLR or NeurIPS proceedings
(`references_verified.json`, `nondoi_verification.json`). Content statements about papers rely on their
**abstracts** (PubMed/Crossref); full texts of Elsevier papers could not be retrieved from this environment.
Where a property is "not stated", it may still be present in the full text.

## 1. Systematic corpus
PubMed query (`pubmed_corpus.py`, retrieved 2026-11-10): ML terms × (hydrothermal liquefaction | hydrothermal
carbonization | hydrochar | biocrude), 2015–2026 → 52 records, 44 primary studies (20 in *Bioresource Technology*).
Abstract-level screening (`literature_matrix_corpus.csv`):

| Practice mentioned in title/abstract | Studies (of 44) |
|---|---|
| Grouped / study-level / external validation | 2 |
| Random split or k-fold CV explicitly | 4 |
| Any uncertainty quantification | 4 |
| Physics / mass-balance constraints | 2 |
| Experimental validation | 6 |
| Reported R² in abstract (median of best values) | 15 studies; median best R² = 0.93 |

This is a lower bound (abstracts omit details), but it shows that unseen-study validity is rarely examined.

## 2. Detailed matrix — closest works
| Paper | Venue | Problem | Data | Methods | Validation | UQ | Physics | Key limitation relevant here |
|---|---|---|---|---|---|---|---|---|
| Zhang et al., 2021 (10.1016/j.biortech.2021.126011) | Bioresour. Technol. | HTL of algae: bio-oil yield/properties, optimisation | literature-compiled (n.s. in abstract) | GBR, RF | n.s. | n.s. | n.s. | no unseen-study evaluation reported in abstract |
| Leng et al., 2022 (10.1016/j.biortech.2022.127791) | Bioresour. Technol. | N-heterocycles in HTL bio-oil | literature | RF, GBR | n.s. | n.s. | n.s. | idem |
| Katongtung et al., 2024 (10.1007/s12155-024-10773-0) | BioEnergy Res. | HTL of lignocellulose | literature | ML ensemble | n.s. | n.s. | n.s. | idem |
| Gungor et al., 2025 (10.1007/s12155-025-10906-z) | BioEnergy Res. | biocrude yield from HHV + conditions | literature | interpretable ML | n.s. | n.s. | n.s. | idem |
| Tian et al., 2025 (10.1016/j.energy.2025.136708) | Energy | bio-oil properties via GNN molecular structure | literature | GNN | n.s. | n.s. | n.s. | idem |
| Djandja et al., 2027 (10.1016/j.fuel.2026.141091) | Fuel | HTL of lignocellulose: yield, ratios, carbon retention, HHV | curated literature database | MLP, SVR, DT, RF, XGB (PSO tuning) | n.s. (abstract) | bootstrap MC + residual conformal | n.s. | secondary outputs "exhibited limited generalization"; water-fill ratio key predictor |
| Elfetni et al., 2026 SSRN (10.2139/ssrn.6816225) | preprint | energy/carbon routing; same 3,693-record DB | 187 papers, 433 biomasses | RF and other ensembles | test split (abstract) | ensemble + conformal | n.s. | intervals calibrated on exchangeable rows |
| **Elfetni et al., 2026 (10.1016/j.biortech.2026.135587)** | **Bioresour. Technol.** | four-phase HTL yields as one composition vector | 680 closure-valid records, 60 papers (same DB) | XGBoost teacher + softmax admissibility + conservation penalties | random 408/136/136 + publication-aware validation; k-shot local calibration (median vector RMSE 13.91→7.10 with k = 5) | split-conformal 90 %: phase-wise coverage 0.875–0.956 (random test) | closure, carbon, HHV | heterogeneity *documented but not explained*; conformal coverage reported on random test split; local calibration is point-only |
| Jang et al., 2026 (10.1111/gcbb.70173) | GCB Bioenergy | leakage in biochar ML (64 studies) | 5 re-analysed datasets | review + re-analysis | random vs grouped | — | — | biochar only; no modelling remedy beyond grouped splits; no UQ |
| Kapoor & Narayanan, 2023 (10.1016/j.patter.2023.100804) | Patterns | leakage taxonomy across ML-based science | — | survey | — | — | — | generic |

## 3. Gaps (precise)
* **WHAT EXISTS**: accurate *in-distribution* surrogates (R² ≈ 0.8–0.95); physically admissible four-phase surrogates (Elfetni 2026); documentation that publication-aware validation is much worse and that a few local runs help (Elfetni 2026); row-calibrated conformal intervals (Elfetni 2026; Djandja 2027); leakage audits for biochar (Jang 2026).
* **WHAT IS NOT ADDRESSED**: (G1) *why* models fail on new studies — how much of the error is a study-level offset and whether recorded work-up/reporting conventions explain it; (G2) whether conformal intervals keep their nominal coverage for an unseen study, and how to calibrate them at the study level; (G3) how to combine a few runs from the new study with valid intervals and principled shrinkage when k is very small; (G4) multi-target (bio-oil and solid) and multi-process (HTL, solvothermal, HTC) assessment with a locked study-level test set, temporal and external validation.
* **WHY IT MATTERS**: published surrogates are used to screen feedstocks/conditions for *new* laboratories and plants; an interval that covers 90 % of random rows but far fewer runs of a new study yields over-confident screening decisions.
* **WHAT THIS WORK ADDS**: a quantified decomposition of transfer error, a test of the reporting-convention hypothesis, study-calibrated conformal intervals, and k-shot empirical-Bayes adaptation with conformal validity, evaluated on a locked study-level test set plus temporal and external validation.
* **HOW VERIFIED**: E1–E8 in `code/config/PROTOCOL.md`.

## 4. Novelty map
| Work | Contribution | Overlap with this work | Genuinely different element here |
|---|---|---|---|
| Elfetni 2026 BT | conservation-admissible surrogate; publication-aware validation; point k-shot calibration; random-split conformal | same database; heterogeneity observed; k-shot idea | study-level *decomposition and explanation* of heterogeneity (protocol descriptors, meta-regression); conformal validity *at study level*; EB-shrunk k-shot offsets *with intervals*; locked test + temporal + external validation; HTC and solid yields included |
| Djandja 2027 Fuel | HTL yield ML + bootstrap/conformal UQ | UQ for HTL | new-study coverage assessment; study-level calibration |
| Jang 2026 GCBB | leakage audit (biochar) | random vs grouped splits | hydrothermal domain; model-agnostic remedies for intervals and adaptation |
| Dunn et al. 2023 JASA | conformal sets for two-layer hierarchical models | study-weighted CDF pooling | first application/assessment for literature-derived process data (to our knowledge, within the corpus examined); combination with EB k-shot offsets |
| Sigrist 2022 JMLR (GPBoost) | boosting with random effects | random study effects | used as a competing baseline, not claimed |

## 5. Claims we will NOT make
* "First to use grouped validation for HTL" — false (Elfetni 2026).
* "Physics-consistent HTL surrogate" — already done (Elfetni 2026); not part of our contribution.
* "Conformal prediction for HTL" — already done; our claim is restricted to study-level validity and k-shot adaptation.
