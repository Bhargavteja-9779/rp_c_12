# Review round 2 — Reviewer #2 (novelty, prior art, contribution)

Perspective: is the gap genuine and is the contribution more than a re-application of existing techniques?

## Prior-art check performed by this reviewer
* Elfetni et al. (2027, *Bioresour. Technol.*) — same database, publication-aware validation, *k*-shot point recalibration, split-conformal on a random test split.
* Dunn, Wasserman & Ramdas (2022/2023, *JASA*) — conformal prediction for two-layer hierarchical data (CDF pooling).
* **Fisch et al. (2021, ICML)** — few-shot conformal prediction by meta-learning over exchangeable auxiliary tasks (verified via arXiv 2102.08898).
* **Bersson & Hoff (2024, *J. Surv. Stat. Methodol.*)** — conformal prediction for small areas using indirect (empirical-Bayes-type) information (verified via Crossref 10.1093/jssam/smae010).
* Jang et al. (2026, *GCB Bioenergy*) — leakage in biochar ML.

## Issues

| # | Severity | Issue | Required fix | Status |
|---|---|---|---|---|
| 2.1 | MAJOR | The *k*-shot component (shrinkage + re-calibration by simulation over calibration groups) is conceptually close to meta-learned few-shot conformal prediction (Fisch 2021) and to FAB/small-area conformal prediction (Bersson & Hoff 2024), neither of which was cited. Presenting STRATA as a new method overclaims. | Cite both; describe STRATA as an assembly of established constructions; move the claimed novelty to the bioresource evaluation (decomposition, reporting hypothesis, validity across 7 learners and 4 shift types). | **Fixed** — contribution (iii) rewritten; both references added (verified). |
| 2.2 | MAJOR | Overlap with Elfetni et al. (2027) is large (same data, publication-aware validation, local calibration). | Make the differentiation explicit and quantitative. | **Fixed/clarified** — Introduction states what was already shown; §3.5 states that STRATA "quantifies, with valid intervals" their k-shot observation; new results not in that paper: variance decomposition, reporting-descriptor test (negative), coverage failure of row calibration across 7 learners and its mechanism, locked/temporal/family/external validation, solid-yield and HTC targets. |
| 2.3 | MODERATE | The "reporting descriptors" hypothesis is the only domain-specific idea and it failed. Is a negative result enough? | Present it as a pre-registered hypothesis test with adequate power discussion and two interpretations. | **Partly fixed** — two readings are discussed; formal power analysis not done (limitation: 122 studies, offset SD ≈ 12 wt%; the CI of the P effect, −0.38 to 0.60 wt%, excludes improvements larger than ~0.4 wt% in median per-study RMSE). Sentence on CI added via Table 3. |
| 2.4 | MODERATE | The abstract-level literature screen cannot prove that "most" studies use random splits. | State as lower bound; avoid "most". | **Already compliant** — text reports counts and "lower bound"; no "most studies" claim about splits in the abstract. |
| 2.5 | MINOR | "To our knowledge" claims. | Remove unless verified. | **Compliant** — none used. |

## Verdict
The work is not a new algorithm; it is a carefully executed evaluation that establishes, for the journal's domain, how and why literature-trained surrogates fail on new studies and gives a validated recipe. After fix 2.1 the novelty claim is defensible.
