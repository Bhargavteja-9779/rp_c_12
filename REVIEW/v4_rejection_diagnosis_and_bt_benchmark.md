# v4 — Rejection diagnosis and benchmark against Bioresource Technology papers (2026-11-25)

Decision on v3: desk rejection, "no novelty, not at the level of the journal / its readers".

## Benchmark corpus
`journal_selection/bt_benchmark/bt_abstracts.json` (PubMed, fetched with fetch_bt.py): 28 BT papers 2022–2027 on ML for hydrothermal
conversion, 17 BT meta-analyses, 37 BT ML papers on pyrolysis/gasification/biochar (2025–2026).

## What accepted BT papers do (observed in abstracts)
1. Lead with a bioresource/process question ("what drives X", "how to maximise Y"), not with a modelling or validation critique.
2. Report quantitative process insight: effect sizes (% gain), optimal windows (e.g. "217–220 °C, 1–1.5 h"), control regimes, mechanisms.
3. Meta-analyses are an accepted genre in BT (anaerobic digestion microaeration, microplastics in AD, manure-composting C/N losses,
   biochar Cd/GHG with boosted regression trees, outdoor microalgae productivity): N studies, pooled effects with moderators,
   practical recommendations. None exists for hydrothermal liquefaction/carbonization (PubMed and Crossref checks, 2026-11-25).
4. ML papers: literature dataset + GBDT/XGBoost + SHAP + optimisation (+ web tool or experimental validation), with test R² 0.9+.
   Their weakness (pooled data, random splits, SHAP on confounded data) is exactly what our earlier work quantified.
5. Abstracts 140–250 words, positive framing, final sentence on practical/theoretical value.

## Why v3 failed (our diagnosis)
- Framed as an audit of other people's models; main messages negative ("barely predictable", "did not transfer").
- Contribution perceived as statistical methodology (conformal, empirical Bayes) — outside the core interest of BT readers.
- Overlap with Elfetni et al. (2027) in the same journal (same database, local calibration).
- No new process knowledge about hydrothermal conversion itself.

## v4 strategy
Turn the same database into the first quantitative meta-analysis of HTL/HTC: process and feedstock effects estimated only from
within-study comparisons (laboratory effects cancel), with heterogeneity, prediction intervals and "probability of benefit" for a new
laboratory; quantify the laboratory effect relative to process effects; show where pooled ML/SHAP (the dominant approach in BT) is
confounded; confirm on locked studies. Earlier STRATA results become a short practical section.
