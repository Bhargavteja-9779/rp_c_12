---
title: "Process effects versus laboratory effects in hydrothermal liquefaction and carbonization of lignocellulosic biomass: a within-study meta-analysis"
---

# Highlights

- First meta-analysis of hydrothermal liquefaction and carbonization process effects
- Effects estimated only within studies, so laboratory differences cancel out
- Catalysts raised bio-oil yield by 5.5–8.5 wt% and energy recovery by 12.1–19.6 points
- Laboratory effects (SD 12.5–15.8 wt%) exceeded every catalyst effect
- Effects vary widely between laboratories; a new laboratory should test them locally

# Abstract

Hundreds of studies have examined how temperature, residence time, catalysts and solvents affect hydrothermal liquefaction (HTL) and carbonization (HTC), yet their results are pooled qualitatively or by machine-learning models that mix laboratory differences with process effects. This study reports, to our knowledge, the first quantitative meta-analysis of HTL/HTC process effects. From a curated database of 3,693 experiments on mainly lignocellulosic biomass, 5,830 within-study comparisons from 127 development studies — runs of the same study that differ in one factor only — were synthesised with random-effects models under a protocol registered beforehand; 38 further studies were held out. Raising the temperature by 10 °C within 250–300 °C increased bio-oil yield by 1.07 wt% (62 studies) and decreased solid yield by 1.74 wt%. Catalysts raised bio-oil yield by 5.5 (alkali carbonates) to 8.5 wt% (metal/supported catalysts), lowered solid yield by 4.5–8.2 wt% and raised energy recovery to bio-oil by 12.1–19.6 percentage points. Between-laboratory heterogeneity was large (median I² 68%): catalysts are expected to increase bio-oil yield in only 71%–84% of new laboratories, and laboratory offsets (SD 12.5–15.8 wt%) exceeded every catalyst effect. A pooled machine-learning model reproduced the mean effects (Spearman ρ = 0.92) but not their spread, and in held-out studies the mean effects predicted individual outcomes no better than assuming no change. Process effects in HTL/HTC are real but laboratory-specific; data-driven guidance should report prediction intervals and be confirmed locally.

**Keywords:** hydrothermal liquefaction; hydrothermal carbonization; meta-analysis; catalyst; bio-oil yield; reproducibility


# 1. Introduction

Hydrothermal liquefaction (HTL) and hydrothermal carbonization (HTC) convert wet biomass and residues into bio-oil (biocrude), a carbon-rich solid (hydrochar or char), an aqueous phase and gas without prior drying (Toor et al., 2011; Elliott et al., 2015; Funke and Ziegler, 2010; Libra et al., 2011). Because product yields depend on feedstock composition, temperature, residence time, solid loading, catalysts and co-solvents, a large experimental literature has varied these factors one or a few at a time, and reviews have summarised the resulting trends qualitatively (Akhtar and Amin, 2011; Peterson et al., 2008; Gollakota et al., 2018; Dimitriadis and Bezergianni, 2017). More recently, machine-learning (ML) models trained on hundreds of literature-derived runs have been used to rank the importance of these factors and to optimise conditions (Zhang et al., 2021; Leng et al., 2022; Katongtung et al., 2024; Gungor et al., 2025; Tian et al., 2025; Djandja et al., 2027).

Both approaches face the same obstacle: results from different laboratories are not directly comparable. Each study uses its own feedstock batch, reactor, heating profile, product work-up and definition of a "yield"; bio-oil yield in particular depends on the recovery solvent (Valdez et al., 2011). Even analyses of identical liquefaction oils vary between laboratories (Bulsink et al., 2020). When experiments from many studies are pooled, differences between laboratories are therefore mixed with the effects of the process variables. In an earlier analysis of the same database, study-level offsets made up 0.49–0.65 of the error of literature-trained ML models for a study they had not seen (Supplementary Section S6; see also Elfetni et al. (2027)). How large the effects of the main process variables are once laboratory differences are removed, and how consistent they are from one laboratory to the next, has not been quantified.

Meta-analysis answers such questions in other fields of bioresource research, for example for microaeration in anaerobic digestion (Febroni et al., 2026), microplastics in anaerobic digestion (Jiang et al., 2026) and carbon and nitrogen losses during composting (Hussain et al., 2027). A systematic search of PubMed and Crossref found no meta-analysis of HTL or HTC process effects (Supplementary Section S1). The HTL/HTC literature offers an unusual opportunity: most studies vary one factor while holding the others constant. Laboratories differ far more in their absolute yields than in how their yields respond to such changes — in the ten longest temperature series of the database, bio-oil yields at 300 °C ranged from 12.1 to 63.2 wt%, whereas yields within each series changed much less with temperature (Fig. 1). The effect of a factor can therefore be estimated *within* each study, where laboratory-specific offsets cancel, and then synthesised across studies with random-effects models that quantify the remaining between-laboratory heterogeneity (DerSimonian and Laird, 1986; Higgins and Thompson, 2002; Riley et al., 2011).

This study applies this design to the largest public curated hydrothermal database (3,693 experiments from 188 studies) (Elfetni, 2026). Five questions were addressed under a protocol registered before any effect was computed: (1) How large are the within-study effects of temperature, residence time, solid loading, catalysts and reaction media on bio-oil and solid yields, and on the aqueous and gas phases, bio-oil heating value, energy recovery and nitrogen content? (2) How consistent are these effects between laboratories, and how likely is a given change to help in a new laboratory? (3) How large is the laboratory effect compared with the process effects? (4) Do pooled ML models and their importance measures, as commonly reported, recover the within-study effects? (5) Do the effects replicate in 38 studies that were held out from the start?


![**Fig. 1.** Bio-oil yield versus temperature in the ten development studies with the longest single-factor temperature series (feedstock and all other conditions constant within a line). Absolute yields differ between studies — through feedstock and laboratory — far more than they change with temperature within a study; the meta-analysis therefore uses only within-study changes.](/home/user/rp_c_12/figures/fig24_within_study_design.png){width=16cm}


# 2. Materials and methods

## 2.1. Data source and study selection

The data were the Version 1.0.0 release of the curated hydrothermal treatment/liquefaction database (Elfetni, 2026) (CC BY 4.0; 3,693 runs from 188 source publications, 1982–2026; file checksum verified at every load). Each run records the source study, feedstock composition (ultimate, proximate and lignocellulosic analysis), temperature, residence time, solid loading, heating rate, catalyst and loading, reaction medium, atmosphere, process subtype (HTL, solvothermal HTL, HTC), yield basis, product separation procedure, product yields and product properties. Before any model was fitted in our earlier work on this database, 38 source studies (20%, seed 20261110) were drawn at random and locked away. They had been used in earlier evaluations of machine-learning transfer (Supplementary Section S6) but in no meta-analytic computation; here they were used once, for the replication test (Section 2.6). The remaining 150 studies formed the development set. Outcomes were bio-oil and solid yields (primary; wt%), and aqueous-phase and gas yields, bio-oil higher heating value (HHV; measured values only), energy recovery to bio-oil (yield × bio-oil HHV / feed HHV, %) and bio-oil nitrogen content (secondary). Yields reported on a carbon basis and values outside physical ranges were excluded. The database targets lignocellulosic and lignin-rich biomass: 93% of the 150 development studies processed agricultural residues, wood, technical lignins or mixtures of these, and the rest manures, sludges, polymers or other feedstocks; 2516 development runs were HTL or solvothermal HTL and 413 HTC. The reproducible literature search used to establish novelty and the relation of this work to earlier analyses of the same database (Elfetni et al., 2027; Elfetni et al., 2026) are described in Supplementary Section S1.

## 2.2. Within-study contrasts

Runs of the same study with identical values of every recorded condition except the factor of interest — feedstock identity and composition, temperature, residence time, solid loading, heating rate, catalyst class and loading, reaction medium, atmosphere and process subtype — form a *cell*. Five factors were analysed (Table 1). For temperature, residence time and solid loading, the effect is the slope between adjacent levels within a cell: change in the outcome per +10 °C (assigned to the band of the pair midpoint: < 250, 250–300, 300–350, ≥ 350 °C), per doubling of residence time and per +10 percentage points of solid loading. For catalysts, the effect is the mean outcome of runs with a given catalyst class (alkali carbonate, alkali hydroxide, acid, metal or supported metal, other) minus the mean outcome of uncatalysed runs in the same cell; for reaction media, the mean outcome with a co-solvent class (water–alcohol, alcohol, water with hydrogen donor, other organic) minus that in water. Feedstock effects were estimated by regressing the outcome on feedstock lignin, cellulose, hemicellulose, ash and nitrogen contents across runs of the same cell that differ only in feedstock, with cell fixed effects and standard errors clustered by study. Because every contrast compares runs of the same study, laboratory-specific offsets — reactor, work-up, yield definition, analyst — cancel.

## 2.3. Synthesis

For each outcome, factor and level, the study-level effect was the mean of the study's contrasts, with sampling variance $s_w^2/m_j$, where $m_j$ is the number of contrasts of study $j$ and $s_w^2$ the pooled within-study variance of contrasts (experimental replicates are rarely reported, so within-study scatter of contrasts is the available measure of precision). Study effects were pooled with a random-effects model: the between-study variance $\tau^2$ was estimated by restricted maximum likelihood (Viechtbauer, 2005; Veroniki et al., 2015), confidence intervals used the Hartung–Knapp–Sidik–Jonkman correction (Hartung and Knapp, 2001; Sidik and Jonkman, 2002), and 95% prediction intervals (PI), which describe the range of effects expected in a new study, were computed with $k-2$ degrees of freedom (Riley et al., 2011; IntHout et al., 2016). Heterogeneity was summarised by $\tau$ and $I^2$ (Higgins and Thompson, 2002). The probability that a change increases the outcome in a new laboratory, P(increase), was computed from the predictive distribution $N(\hat\mu, \hat\tau^2 + \mathrm{SE}^2)$. Results were reported when at least five studies contributed. Sensitivity analyses were the Paule–Mandel $\tau^2$ estimator, a one-contrast-per-study (median) estimator, leave-one-study-out ranges and an Egger-type test for small-study effects (Egger et al., 1997) (≥ 10 studies). Pre-specified moderators of catalyst effects (cell temperature < 300 vs ≥ 300 °C, process subtype, feedstock lignin content above vs below the median) were tested with z-tests and Holm correction within outcome × factor.

## 2.4. Laboratory effect

The laboratory effect was quantified in two ways: (i) as the standard deviation $\hat\tau$ of study-level offsets of out-of-study residuals of a gradient-boosting model that uses feedstock composition and all recorded conditions (method of moments; Supplementary Section S6), and (ii) as the random-intercept standard deviation of a linear mixed model with the same inputs (piecewise-linear temperature, log residence time, loading, heating rate, catalyst and medium classes, feedstock composition, process subtype; fitted by REML). Both estimate the between-study variation in yield that is not explained by the recorded feedstock and conditions, and both were compared with the meta-analytic process effects.

## 2.5. Pooled models and importance measures

To test whether the pooled analyses common in the literature recover the within-study effects, three models were fitted to all development runs of each primary outcome: a pooled XGBoost model (Chen and Guestrin, 2016) with hyper-parameters tuned by study-grouped cross-validation, a pooled linear model, and a linear model with study fixed effects (within transformation). Model-implied effects were computed on the scale of the meta-analytic effects: for XGBoost as partial-dependence differences (Friedman, 2001) averaged over all runs (temperature between band limits; residence time and loading between their quartiles; catalyst class at its median loading versus none; medium class versus water), for the linear models from their coefficients. Agreement with the meta-analytic means was summarised by sign agreement for effects whose CI excluded zero, Spearman correlation and the share of model-implied effects outside the meta-analytic CI. TreeSHAP importances (Lundberg and Lee, 2017) of the XGBoost model were summed within factor groups.

## 2.6. Replication in held-out studies

The 38 locked studies were analysed once, after all development analyses had been fixed. Their within-study contrasts were computed with the same definitions and predicted by (a) the development meta-analytic mean effect, (b) the pooled XGBoost model trained on all development runs (difference of its predictions for the two sides of the contrast) and (c) no change. The pre-registered primary test compared per-study root-mean-square errors of these predictions (one-sided Wilcoxon signed-rank tests, Holm correction); the coverage of the 95% PIs for the locked studies' effects was also recorded.

## 2.7. Protocol, deviations and software

The original protocol, the locked study list and five addenda were committed to a version-controlled repository before the analyses they govern; this meta-analysis was specified in Addendum E, registered before any effect size was computed (only the number of available contrasts had been counted). Two deviations were made after the first development run and before the locked analysis and are reported in Supplementary Section S2: levels closer than 5 °C, 0.25 log~2~ units of time or 1 percentage point of loading were not used as contrasts, because floating-point noise had produced near-zero denominators; and energy recovery was computed from yield and HHVs because the database's energy-yield column turned out to be yield × HHV/100 (MJ per kg feed). The protocol was not deposited in a public registry. Analyses used Python 3.13 with NumPy, pandas, SciPy, statsmodels and XGBoost; the random-effects estimator was validated against the Paule–Mandel implementation of statsmodels and with unit tests. All numbers in this article are inserted programmatically from the result files.


# 3. Results and discussion

## 3.1. Evidence base

Of the 150 development studies, 127 contained at least one within-study contrast, giving 5,830 contrasts across seven outcomes (1,494 for bio-oil yield from 106 studies and 1,575 for solid yield from 109 studies). Temperature (up to 64 studies per band), residence time and catalysts were studied most often; solid loading and reaction media much less (Fig. 2). Of the 77 outcome × factor × level combinations with at least five studies, 31 had a 95% confidence interval that excluded zero. The pooled means were robust to the choice of the $\tau^2$ estimator (largest difference between REML and Paule–Mandel 0.34 units), to using one contrast per study and to leaving out single studies, and to resampling whole studies (a study-level bootstrap removed significance from 0 of the 31 effects whose CI excluded zero, and was less conservative than the Hartung–Knapp intervals for 12 combinations with few studies, for which the more conservative intervals are reported), and 5 of 56 Egger-type tests indicated small-study effects at *p* < 0.05, close to the number expected by chance (Supplementary Table S4).


![**Fig. 2.** Evidence base of the meta-analysis: number of development studies that contribute within-study contrasts for each factor (rows) and outcome (columns). Blank cells: fewer than five studies (not synthesised).](/home/user/rp_c_12/figures/fig18_evidence_map.png){width=16cm}


## 3.2. Temperature and residence time

Within studies, bio-oil yield rose with temperature up to 300 °C — by 1.76 wt% per 10 °C below 250 °C (95% CI 0.53 to 2.98; 21 studies) and 1.07 wt% at 250–300 °C (0.65 to 1.50; 62 studies) — and then declined slightly, by −0.75 wt% per 10 °C at 300–350 °C (−1.39 to −0.11) and −0.50 wt% above 350 °C (CI including zero) (Fig. 3, Table 1). Solid yield fell most steeply at low temperature (−2.62 and −1.74 wt% per 10 °C below 250 and at 250–300 °C) and only slightly above 300 °C (−0.59 wt%). These within-study estimates quantify the optimum window of 300–350 °C that reviews have described qualitatively (Akhtar and Amin, 2011; Gollakota et al., 2018): the gain in bio-oil from 250 to 300 °C is about 5.4 wt%, and nothing is gained above 300 °C on average. At the same time, gas yield increased with temperature, most clearly above 300 °C (by 1.37 wt% per 10 °C at 300–350 °C and 2.15 wt% above 350 °C), and the HHV of bio-oil rose by 0.44 MJ kg^−1^ per 10 °C at 250–300 °C with no detectable heterogeneity (I² = 0%) (Table 2). Energy recovery to bio-oil therefore increased by 1.98 percentage points per 10 °C at 250–300 °C but not above 300 °C. The bio-oil temperature effect at 250–300 °C was comparatively consistent between laboratories (I² = 45%; P(increase) = 0.83), whereas above 300 °C laboratories disagreed on the sign (I² = 83%).

Doubling the residence time did not change bio-oil yield on average (−0.64 wt%, −1.43 to 0.15; 56 studies) and tended to lower solid yield (−1.95 wt%, −4.23 to 0.33), while it raised bio-oil HHV by 0.35 MJ kg^−1^. For most HTL studies, holding time is therefore a lever for oil quality rather than for oil yield.


![**Fig. 3.** Within-study effects on bio-oil and solid yields. Diamonds: random-effects means; blue bars: 95% confidence intervals; grey lines: 95% prediction intervals for a new study. k: number of studies; I²: share of variance due to between-study heterogeneity; P(>0): probability that the change increases the yield in a new study. Upper panels: per +10 °C in the stated band or per doubling of residence time; lower panels: catalysts versus uncatalysed runs and co-solvents versus water at otherwise identical conditions, and solid loading per +10 percentage points.](/home/user/rp_c_12/figures/fig19_effect_atlas.png){width=16cm}



**Table 1.** Within-study meta-analysis of process effects on bio-oil and solid yields (development studies). Effect: random-effects mean change (REML, Hartung–Knapp–Sidik–Jonkman CI); PI: 95% prediction interval for the effect in a new study; k: studies; I²: share of variance due to between-study heterogeneity; P(increase): probability that the change increases the outcome in a new study, from the predictive distribution. Temperature effects per +10 °C in the stated band; catalysts vs uncatalysed runs and media vs water at otherwise identical conditions.

| Outcome | Change | Effect | 95% CI | 95% PI | k | Contrasts | I² | P(increase) |
|---|---|---|---|---|---|---|---|---|
| Bio-oil yield (wt%) | T +10 °C (<250 °C) | 1.8 | 0.5 to 3.0 | -3.2 to 6.7 | 21 | 73 | 78% | 0.77 |
| Bio-oil yield (wt%) | T +10 °C (250–300 °C) | 1.1 | 0.6 to 1.5 | -1.2 to 3.4 | 62 | 287 | 45% | 0.83 |
| Bio-oil yield (wt%) | T +10 °C (300–350 °C) | -0.8 | -1.4 to -0.1 | -4.9 to 3.4 | 53 | 208 | 83% | 0.36 |
| Bio-oil yield (wt%) | T +10 °C (≥350 °C) | -0.5 | -1.4 to 0.4 | -4.3 to 3.3 | 23 | 88 | 79% | 0.39 |
| Bio-oil yield (wt%) | Residence time ×2 | -0.6 | -1.4 to 0.1 | -1.4 to 0.1 | 56 | 285 | 0% | 0.05 |
| Bio-oil yield (wt%) | Solid loading +10 pp | -6.2 | -15.1 to 2.7 | -44.7 to 32.4 | 23 | 146 | 85% | 0.37 |
| Bio-oil yield (wt%) | Alkali carbonate | 5.5 | 2.5 to 8.4 | -9.0 to 19.9 | 32 | 127 | 78% | 0.78 |
| Bio-oil yield (wt%) | Alkali hydroxide | 6.6 | 0.8 to 12.4 | -18.6 to 31.9 | 24 | 71 | 84% | 0.71 |
| Bio-oil yield (wt%) | Metal / supported metal | 8.5 | 5.3 to 11.6 | -8.8 to 25.8 | 39 | 101 | 79% | 0.84 |
| Bio-oil yield (wt%) | Acid | 8.5 | 0.2 to 16.8 | -15.9 to 33.0 | 8 | 19 | 91% | 0.8 |
| Bio-oil yield (wt%) | Other catalyst | 6.8 | -2.0 to 15.6 | -25.0 to 38.7 | 14 | 20 | 86% | 0.68 |
| Bio-oil yield (wt%) | Water–alcohol (vs water) | 4.4 | -9.5 to 18.3 | -31.6 to 40.4 | 5 | 22 | 87% | 0.65 |
| Bio-oil yield (wt%) | Alcohol (vs water) | 9.2 | -16.8 to 35.2 | -64.6 to 82.9 | 6 | 28 | 99% | 0.63 |
| Solid yield (wt%) | T +10 °C (<250 °C) | -2.6 | -3.5 to -1.8 | -6.1 to 0.9 | 28 | 205 | 69% | 0.06 |
| Solid yield (wt%) | T +10 °C (250–300 °C) | -1.7 | -2.2 to -1.3 | -3.8 to 0.3 | 64 | 299 | 32% | 0.04 |
| Solid yield (wt%) | T +10 °C (300–350 °C) | -0.6 | -1.0 to -0.2 | -2.9 to 1.7 | 50 | 203 | 71% | 0.3 |
| Solid yield (wt%) | T +10 °C (≥350 °C) | -0.5 | -1.4 to 0.4 | -3.9 to 2.9 | 20 | 80 | 77% | 0.38 |
| Solid yield (wt%) | Residence time ×2 | -2.0 | -4.2 to 0.3 | -15.4 to 11.4 | 52 | 325 | 79% | 0.38 |
| Solid yield (wt%) | Solid loading +10 pp | 6.0 | 2.2 to 9.7 | -7.5 to 19.4 | 16 | 112 | 81% | 0.83 |
| Solid yield (wt%) | Alkali carbonate | -6.9 | -10.8 to -3.0 | -24.2 to 10.4 | 26 | 108 | 80% | 0.21 |
| Solid yield (wt%) | Alkali hydroxide | -4.5 | -8.3 to -0.8 | -13.6 to 4.5 | 19 | 52 | 21% | 0.15 |
| Solid yield (wt%) | Metal / supported metal | -8.2 | -12.4 to -4.1 | -32.4 to 15.9 | 36 | 93 | 91% | 0.24 |
| Solid yield (wt%) | Acid | -16.0 | -41.6 to 9.6 | -91.9 to 59.9 | 7 | 18 | 100% | 0.29 |
| Solid yield (wt%) | Other catalyst | -5.8 | -20.4 to 8.8 | -61.0 to 49.3 | 13 | 19 | 100% | 0.41 |
| Solid yield (wt%) | Water–alcohol (vs water) | -4.8 | -9.2 to -0.4 | -11.8 to 2.2 | 5 | 26 | 42% | 0.02 |
| Solid yield (wt%) | Alcohol (vs water) | 11.8 | -0.4 to 23.9 | -22.2 to 45.7 | 7 | 33 | 92% | 0.81 |



## 3.3. Catalysts and reaction media redistribute products

All three well-studied catalyst classes increased bio-oil yield within studies: alkali carbonates by 5.5 wt% (2.5 to 8.4; 32 studies), alkali hydroxides by 6.6 wt% (0.8 to 12.4; 24 studies) and metal or supported-metal catalysts by 8.5 wt% (5.3 to 11.6; 39 studies). On a relative scale these are increases of 27%, 26% and 32% over the uncatalysed yield (Supplementary Table S6). The same catalysts reduced solid yield by 6.9, 4.5 and 8.2 wt%, and alkali hydroxides increased the aqueous-phase yield by 8.4 wt% (1.5 to 15.2), whereas gas yields did not change significantly (Fig. 4). Catalysts thus act mainly by shifting mass from the solid to the liquid products rather than by additional gasification, consistent with the commonly proposed suppression of char-forming condensation reactions (Akhtar and Amin, 2011; Peterson et al., 2008); single-study investigations of alkali catalysts (Zhu et al., 2015) can now be placed against a cross-study average. Because carbonates and metal catalysts also raised bio-oil HHV (by 1.2 and 1.2 MJ kg^−1^), the energy recovered in bio-oil increased by 13.1 (alkali carbonate), 12.1 (alkali hydroxide) and 19.6 percentage points (metal/supported) — the largest process effects found in this study (relative increases of 40–48%). Bio-oil nitrogen content changed by less than 0.28 wt% with any catalyst class or 10 °C temperature step (Supplementary Table S7), so catalysts in these studies did not measurably reduce the nitrogen burden of the oil.

The pre-specified moderator analyses found no catalyst effect that depended on temperature, process subtype or feedstock lignin content after Holm correction for the primary outcomes (1 of 36 tests significant after correction, for energy recovery with alkali hydroxides: a larger gain for low-lignin feedstocks; Supplementary Table S5). Co-solvents were studied in too few laboratories for firm conclusions: water–alcohol mixtures lowered solid yield by 4.8 wt% (5 studies), and the confidence intervals of all other medium effects included zero.


![**Fig. 4.** Redistribution of products by temperature and catalysts: within-study mean effects (95% CI) on the yields of bio-oil, solid, aqueous phase and gas. Each phase is estimated from the studies that report it.](/home/user/rp_c_12/figures/fig20_phase_redistribution.png){width=16cm}



**Table 2.** Within-study meta-analysis for the aqueous and gas phases, bio-oil higher heating value (measured values only) and energy recovery to bio-oil (yield × bio-oil HHV / feed HHV). Definitions as in the primary table.

| Outcome | Change | Effect | 95% CI | 95% PI | k | Contrasts | I² | P(increase) |
|---|---|---|---|---|---|---|---|---|
| Aqueous-phase yield (wt%) | T +10 °C (<250 °C) | 0.6 | 0.1 to 1.2 | 0.1 to 1.2 | 11 | 71 | 2% | 0.99 |
| Aqueous-phase yield (wt%) | T +10 °C (250–300 °C) | -0.1 | -0.7 to 0.5 | -2.1 to 1.8 | 24 | 121 | 28% | 0.44 |
| Aqueous-phase yield (wt%) | T +10 °C (300–350 °C) | 0.1 | -0.7 to 0.8 | -2.6 to 2.7 | 19 | 94 | 79% | 0.52 |
| Aqueous-phase yield (wt%) | T +10 °C (≥350 °C) | -0.5 | -1.3 to 0.2 | -2.8 to 1.8 | 11 | 49 | 81% | 0.31 |
| Aqueous-phase yield (wt%) | Residence time ×2 | -0.2 | -1.6 to 1.3 | -5.8 to 5.4 | 23 | 141 | 68% | 0.47 |
| Aqueous-phase yield (wt%) | Solid loading +10 pp | -4.5 | -6.9 to -2.1 | -7.0 to -2.1 | 9 | 73 | 44% | 0.0 |
| Aqueous-phase yield (wt%) | Alkali carbonate | 3.6 | -1.1 to 8.4 | -10.1 to 17.4 | 13 | 35 | 52% | 0.72 |
| Aqueous-phase yield (wt%) | Alkali hydroxide | 8.4 | 1.5 to 15.2 | -12.4 to 29.1 | 8 | 18 | 96% | 0.84 |
| Aqueous-phase yield (wt%) | Metal / supported metal | 2.4 | -2.1 to 6.9 | -10.9 to 15.7 | 11 | 23 | 75% | 0.66 |
| Gas yield (wt%) | T +10 °C (<250 °C) | 0.8 | 0.3 to 1.3 | -0.9 to 2.6 | 15 | 86 | 70% | 0.84 |
| Gas yield (wt%) | T +10 °C (250–300 °C) | 0.5 | -0.2 to 1.3 | -3.6 to 4.7 | 32 | 169 | 88% | 0.6 |
| Gas yield (wt%) | T +10 °C (300–350 °C) | 1.4 | 0.6 to 2.1 | -1.0 to 3.8 | 21 | 78 | 57% | 0.88 |
| Gas yield (wt%) | T +10 °C (≥350 °C) | 2.1 | 0.5 to 3.8 | -1.8 to 6.1 | 8 | 24 | 63% | 0.91 |
| Gas yield (wt%) | Residence time ×2 | 3.4 | -0.2 to 7.0 | -15.2 to 22.0 | 29 | 161 | 89% | 0.65 |
| Gas yield (wt%) | Solid loading +10 pp | 2.5 | -0.5 to 5.5 | -6.0 to 11.0 | 10 | 67 | 60% | 0.75 |
| Gas yield (wt%) | Alkali carbonate | -0.8 | -3.5 to 1.9 | -9.4 to 7.8 | 14 | 38 | 67% | 0.42 |
| Gas yield (wt%) | Alkali hydroxide | -2.1 | -5.2 to 1.0 | -11.6 to 7.4 | 10 | 30 | 80% | 0.3 |
| Gas yield (wt%) | Metal / supported metal | 0.3 | -1.9 to 2.6 | -8.6 to 9.3 | 18 | 42 | 87% | 0.53 |
| Gas yield (wt%) | Other catalyst | -3.1 | -7.9 to 1.6 | -16.7 to 10.5 | 6 | 7 | 100% | 0.26 |
| Bio-oil HHV (MJ/kg) | T +10 °C (<250 °C) | 0.4 | -0.3 to 1.0 | -1.2 to 2.0 | 7 | 20 | 68% | 0.74 |
| Bio-oil HHV (MJ/kg) | T +10 °C (250–300 °C) | 0.4 | 0.3 to 0.6 | 0.3 to 0.6 | 33 | 91 | 0% | 1.0 |
| Bio-oil HHV (MJ/kg) | T +10 °C (300–350 °C) | 0.3 | 0.1 to 0.5 | -0.5 to 1.1 | 27 | 86 | 67% | 0.77 |
| Bio-oil HHV (MJ/kg) | T +10 °C (≥350 °C) | 0.2 | -0.1 to 0.6 | -0.2 to 0.6 | 12 | 20 | 2% | 0.9 |
| Bio-oil HHV (MJ/kg) | Residence time ×2 | 0.4 | 0.1 to 0.6 | 0.1 to 0.6 | 25 | 92 | 0% | 1.0 |
| Bio-oil HHV (MJ/kg) | Solid loading +10 pp | 0.2 | -0.3 to 0.7 | -0.3 to 0.7 | 8 | 28 | 0% | 0.82 |
| Bio-oil HHV (MJ/kg) | Alkali carbonate | 1.2 | 0.5 to 2.0 | 0.5 to 2.0 | 22 | 42 | 25% | 1.0 |
| Bio-oil HHV (MJ/kg) | Alkali hydroxide | 0.5 | -0.9 to 1.8 | -1.3 to 2.2 | 15 | 32 | 0% | 0.71 |
| Bio-oil HHV (MJ/kg) | Metal / supported metal | 1.2 | 0.1 to 2.3 | -4.6 to 7.0 | 32 | 54 | 85% | 0.66 |
| Bio-oil HHV (MJ/kg) | Acid | 2.4 | -1.0 to 5.7 | -5.9 to 10.7 | 5 | 13 | 77% | 0.82 |
| Bio-oil HHV (MJ/kg) | Other catalyst | -0.6 | -2.1 to 0.9 | -2.1 to 1.0 | 9 | 12 | 0% | 0.18 |
| Energy recovery to bio-oil (%) | T +10 °C (<250 °C) | 3.1 | 0.4 to 5.8 | -4.3 to 10.5 | 7 | 20 | 86% | 0.86 |
| Energy recovery to bio-oil (%) | T +10 °C (250–300 °C) | 2.0 | 1.0 to 3.0 | 1.0 to 3.0 | 29 | 76 | 0% | 1.0 |
| Energy recovery to bio-oil (%) | T +10 °C (300–350 °C) | -0.6 | -1.9 to 0.6 | -5.6 to 4.4 | 23 | 75 | 72% | 0.4 |
| Energy recovery to bio-oil (%) | T +10 °C (≥350 °C) | -1.8 | -3.8 to 0.2 | -3.9 to 0.2 | 11 | 19 | 0% | 0.02 |
| Energy recovery to bio-oil (%) | Residence time ×2 | 0.8 | -1.3 to 3.0 | -1.4 to 3.0 | 22 | 85 | 0% | 0.79 |
| Energy recovery to bio-oil (%) | Solid loading +10 pp | -2.7 | -12.5 to 7.1 | -26.6 to 21.2 | 6 | 26 | 62% | 0.38 |
| Energy recovery to bio-oil (%) | Alkali carbonate | 13.1 | 7.5 to 18.7 | -1.3 to 27.5 | 21 | 41 | 20% | 0.97 |
| Energy recovery to bio-oil (%) | Alkali hydroxide | 12.1 | 0.1 to 24.2 | -24.8 to 49.1 | 14 | 28 | 64% | 0.76 |
| Energy recovery to bio-oil (%) | Metal / supported metal | 19.6 | 10.6 to 28.7 | -22.7 to 62.0 | 25 | 45 | 85% | 0.83 |
| Energy recovery to bio-oil (%) | Other catalyst | 0.9 | -7.9 to 9.8 | -14.7 to 16.6 | 8 | 11 | 25% | 0.56 |



## 3.4. Feedstock composition and solid loading

Studies that processed several feedstocks under identical conditions allow composition effects to be estimated free of laboratory offsets (Table 3). For bio-oil yield (27 studies, 89 cells), none of the five composition variables had a significant effect once the others were held constant (lignin −1.32 wt% per +10 wt%, 95% CI −4.24 to 1.61). Solid yield decreased with hemicellulose content (−8.68 wt% per +10 wt%, −14.12 to −3.25; 22 studies), and bio-oil nitrogen increased with feedstock nitrogen (3.95 wt% per +10 wt% feed N, i.e. about 0.40 wt% of oil N per wt% of feed N) and ash. Higher solid loading increased solid yield by 6.0 wt% per +10 percentage points (2.2 to 9.7; 16 studies), whereas its effect on bio-oil yield was inconsistent (−6.2 wt%, CI −15.1 to 2.7). The within-study evidence on composition comes from fewer studies and a narrower composition range than the pooled data, so the absence of a significant composition effect on bio-oil yield does not rule out a moderate one.


**Table 3.** Feedstock composition effects estimated from runs of the same study at identical conditions that differ only in feedstock (within-cell regression with cell fixed effects; cluster-robust standard errors by study). Coefficients per +10 wt% of the component, adjusted for the other components.

| Outcome | Component | Effect per +10 wt% | 95% CI | p | Studies | Cells |
|---|---|---|---|---|---|---|
| Bio-oil yield (wt%) | Lignin | -1.32 | -4.24 to 1.61 | 0.363 | 27 | 89 |
| Bio-oil yield (wt%) | Cellulose | 1.15 | -1.35 to 3.65 | 0.354 | 27 | 89 |
| Bio-oil yield (wt%) | Hemicellulose | 1.88 | -2.03 to 5.79 | 0.333 | 27 | 89 |
| Bio-oil yield (wt%) | Ash | -1.53 | -7.04 to 3.98 | 0.573 | 27 | 89 |
| Bio-oil yield (wt%) | Nitrogen | -0.97 | -16.68 to 14.74 | 0.900 | 27 | 89 |
| Solid yield (wt%) | Lignin | -0.78 | -5.86 to 4.29 | 0.751 | 22 | 85 |
| Solid yield (wt%) | Cellulose | -1.23 | -5.08 to 2.61 | 0.512 | 22 | 85 |
| Solid yield (wt%) | Hemicellulose | -8.68 | -14.12 to -3.25 | 0.003 | 22 | 85 |
| Solid yield (wt%) | Ash | 5.15 | -1.56 to 11.87 | 0.126 | 22 | 85 |
| Solid yield (wt%) | Nitrogen | 37.02 | -34.3 to 108.35 | 0.293 | 22 | 85 |
| Gas yield (wt%) | Lignin | -0.29 | -0.62 to 0.04 | 0.075 | 10 | 29 |
| Gas yield (wt%) | Cellulose | 0.36 | -0.27 to 1.0 | 0.230 | 10 | 29 |
| Gas yield (wt%) | Hemicellulose | 0.26 | -0.88 to 1.41 | 0.613 | 10 | 29 |
| Gas yield (wt%) | Ash | -0.33 | -1.31 to 0.65 | 0.462 | 10 | 29 |
| Gas yield (wt%) | Nitrogen | -22.73 | -33.06 to -12.4 | <0.001 | 10 | 29 |
| Bio-oil HHV (MJ/kg) | Lignin | 0.02 | -0.49 to 0.54 | 0.923 | 22 | 46 |
| Bio-oil HHV (MJ/kg) | Cellulose | -0.14 | -1.05 to 0.77 | 0.755 | 22 | 46 |
| Bio-oil HHV (MJ/kg) | Hemicellulose | -0.71 | -2.09 to 0.67 | 0.298 | 22 | 46 |
| Bio-oil HHV (MJ/kg) | Ash | 0.49 | -0.5 to 1.49 | 0.316 | 22 | 46 |
| Bio-oil HHV (MJ/kg) | Nitrogen | 3.68 | -4.97 to 12.33 | 0.386 | 22 | 46 |
| Energy recovery to bio-oil (%) | Lignin | -5.41 | -12.2 to 1.37 | 0.112 | 22 | 46 |
| Energy recovery to bio-oil (%) | Cellulose | 3.45 | -1.18 to 8.07 | 0.136 | 22 | 46 |
| Energy recovery to bio-oil (%) | Hemicellulose | -4.44 | -14.39 to 5.52 | 0.364 | 22 | 46 |
| Energy recovery to bio-oil (%) | Ash | 3.02 | -5.21 to 11.25 | 0.454 | 22 | 46 |
| Energy recovery to bio-oil (%) | Nitrogen | -9.99 | -36.43 to 16.45 | 0.441 | 22 | 46 |
| Bio-oil N (wt%) | Lignin | -0.02 | -0.1 to 0.07 | 0.659 | 18 | 38 |
| Bio-oil N (wt%) | Cellulose | 0.03 | -0.22 to 0.28 | 0.789 | 18 | 38 |
| Bio-oil N (wt%) | Hemicellulose | 0.08 | -0.36 to 0.52 | 0.717 | 18 | 38 |
| Bio-oil N (wt%) | Ash | 0.59 | 0.32 to 0.86 | <0.001 | 18 | 38 |
| Bio-oil N (wt%) | Nitrogen | 3.95 | 2.39 to 5.52 | <0.001 | 18 | 38 |



## 3.5. Effects vary between laboratories, and the laboratory itself matters more

Heterogeneity was the rule rather than the exception: the median I² was 68%, and for catalysts the 95% prediction intervals for a new study spanned zero (bio-oil, alkali carbonate: −9.0 to 19.9 wt%; metal/supported: −8.8 to 25.8 wt%). Expressed as probabilities, adding an alkali carbonate, an alkali hydroxide or a metal catalyst is expected to increase bio-oil yield in 78%, 71% and 84% of new laboratories, and raising the temperature from 250 towards 300 °C in 83%. In other words, the direction of the main process effects is reliable on average, but a laboratory has a 15–30% chance that a change which helps elsewhere will not help in its own system.

The laboratory effect itself was larger than any process effect (Fig. 5). After accounting for feedstock composition and all recorded conditions, the standard deviation of study-level offsets was 12.5 wt% for bio-oil yield when estimated from out-of-study residuals of a gradient-boosting model, and 15.8 wt% in a linear mixed model (intraclass correlation 0.76); for solid yield it was 9.7 and 14.7 wt% (intraclass correlation 0.71). A one-standard-deviation difference between laboratories is thus 1.5–2.9 times the effect of adding a catalyst on bio-oil yield and corresponds to a temperature change of about 117–148 °C at the 250–300 °C slope — more than the whole range over which temperature raises yields. The laboratory effect comprises everything that is constant within a study and not captured by the recorded inputs: unrecorded feedstock properties, reactor heat-up and quenching, product recovery and the definition of yields. Inter-laboratory differences of this kind are known for the analysis of liquefaction oils (Bulsink et al., 2020); the present results show that they also dominate yields, and explain why literature-trained models predict new studies poorly (Supplementary Section S6).


![**Fig. 5.** Laboratory effect versus process effects. Blue: absolute within-study effects of a 50 °C increase within 250–300 °C, of catalysts and of doubling the residence time; orange: standard deviation of study-level offsets not explained by recorded feedstock and conditions, estimated from out-of-study residuals of a gradient-boosting model and by a linear mixed model.](/home/user/rp_c_12/figures/fig21_lab_vs_process.png){width=16cm}


## 3.6. What pooled machine-learning models get right and wrong

Pooled ML models are widely used to infer process effects from literature data. Here, the partial-dependence effects of a pooled XGBoost model agreed well with the within-study meta-analysis (Fig. 6, Table 4): Spearman ρ = 0.92 across 26 effects, no sign reversal among the 15 effects whose CI excluded zero, and 8% of model-implied effects outside the meta-analytic CI. A pooled linear model performed worse (ρ = 0.87; 38% outside the CI; 1 sign reversal, for bio-oil yield, T 300–350 °C: 0.4 vs −0.8 wt%), whereas adding study fixed effects to the linear model restored agreement (ρ = 0.91; 4% outside the CI). Flexible pooled models therefore recovered average process effects reasonably well — presumably because, with many studies, laboratory offsets act largely as noise that averages out — what they cannot provide is the between-laboratory spread, which a single partial-dependence curve or SHAP plot hides. Their importance measures should also be read with care: TreeSHAP ranked feedstock composition as the most important factor group for both yields (mean |SHAP| 8.55 wt% for bio-oil, against 4.69 wt% for catalysts and 2.21 wt% for temperature, which ranked 5th), whereas within-study comparisons of feedstocks under identical conditions found no significant composition effect on bio-oil yield (Section 3.4). Because feedstock and laboratory are strongly confounded in literature data — most studies use one or two feedstocks — part of the importance attributed to feedstock composition is likely to reflect laboratory differences.


![**Fig. 6.** Effects implied by pooled models fitted to all development runs (vertical axis) versus within-study meta-analytic effects with 95% CI (horizontal axis) for bio-oil and solid yields. Diagonal: perfect agreement.](/home/user/rp_c_12/figures/fig22_pooled_vs_meta.png){width=16cm}



**Table 4.** Agreement of effects implied by pooled models fitted to all development runs (partial dependence for XGBoost; coefficients for linear models) with the within-study meta-analytic effects (26 factor-level items for bio-oil and solid yields).

| Model | Items compared | Meta effects with CI excluding 0 | Sign reversals (of those) | Spearman ρ | Outside meta-analytic 95% CI | Median |difference| (wt%) |
|---|---|---|---|---|---|---|
| pooled XGBoost | 26 | 15 | 0 | 0.92 | 8% | 0.95 |
| pooled linear | 26 | 15 | 1 | 0.87 | 38% | 1.61 |
| study fixed-effects linear | 26 | 15 | 0 | 0.91 | 4% | 0.95 |



## 3.7. Replication in held-out studies

In the 38 locked studies, 621 within-study contrasts from 30 studies were available. Temperature effects replicated closely: the median locked-study effect of +10 °C at 250–300 °C was 0.89 wt% for bio-oil (14 studies; development mean 1.07) and −1.19 wt% for solids (15 studies; development −1.74) (Fig. 7). Catalyst effects in the few locked studies that tested them were scattered within the wide prediction intervals, with a median of 4.77 wt% for metal catalysts on bio-oil (6 studies). Overall, 0.86 of the 134 locked-study effects fell within the 95% prediction intervals — fewer than nominal, so the intervals are, if anything, too narrow. The pre-registered confirmatory test was not supported: predicting each locked study's contrasts with the meta-analytic mean gave a median per-study RMSE of 5.32 wt%, against 5.61 wt% for the pooled XGBoost model and 5.39 wt% for assuming no change (Holm-corrected *p* = 0.94 and 0.94; Table 5). Average effects, however well estimated, do not predict what a particular laboratory will observe, because between-laboratory variation and run-to-run scatter are as large as the effects themselves.


![**Fig. 7.** Replication in held-out studies: development meta-analysis (diamond: mean; blue: 95% CI; grey: 95% prediction interval) and the effects observed in the 38 locked studies (orange circles, one per study).](/home/user/rp_c_12/figures/fig23_locked_replication.png){width=16cm}



**Table 5.** Pre-registered confirmatory test on the 38 locked studies: prediction of their within-study changes (all factors, bio-oil and solid yields) by the development meta-analytic mean effect, by a pooled XGBoost model and by 'no change'.

| Predictor of locked within-study changes | Median per-study RMSE (wt%) | Sign agreement | One-sided Wilcoxon vs meta (Holm p) |
|---|---|---|---|
| Meta-analytic mean effect | 5.32 | 0.60 | — |
| Pooled XGBoost (counterfactual difference) | 5.61 | 0.64 | 0.94 |
| No change (zero) | 5.39 | — | 0.94 |



## 3.8. Implications for experimental planning, data-driven models and reporting

For laboratories planning HTL or HTC experiments, the effect sizes in Table 1 and Table 2 provide quantitative priors: operate HTL at 300–350 °C rather than at 250 °C (about +5.4 wt% bio-oil from 250 to 300 °C, no average gain above 300 °C, higher HHV), use residence time to adjust oil quality rather than yield, and expect a catalyst to raise bio-oil yield by about 5–9 wt% and energy recovery by 12–20 percentage points. The prediction intervals and probabilities of increase state how much confidence these priors deserve in a new system, and the laboratory effect implies that absolute yields reported elsewhere cannot be expected in one's own reactor. A few local runs at the intended conditions are therefore indispensable; in our earlier evaluation of literature-trained models, three locally measured runs reduced the median error for a new study by 1.6–6.4 wt% (Supplementary Section S6).

For data-driven modelling, the results support three practices: validate models on held-out studies rather than random runs; report effects with between-study prediction intervals rather than single partial-dependence curves; and do not interpret SHAP importance of feedstock descriptors as a causal effect without within-study evidence. For experimental reporting, the dominance of laboratory effects argues for recording the product-recovery solvent and yield basis, the heating and quenching profile, mass-balance closure and replicate variability — information that would allow future meta-analyses to explain, rather than only measure, between-laboratory variation.

## 3.9. Limitations

The analysis rests on one curated database; its harmonisation choices and any transcription errors propagate into all estimates. Within-study contrasts remove laboratory offsets but not confounding by factors that change together within a study; cells were defined by all recorded conditions, but unrecorded differences between runs (for example, a changed heating rate) cannot be excluded. Sampling variances were derived from the scatter of contrasts within studies because replicate standard deviations are rarely reported, and contrasts of the same study share runs; the one-contrast-per-study sensitivity analysis gave similar means, but the confidence intervals may be somewhat narrow. Catalyst classes are broad and catalyst loading was not modelled as a dose; co-solvent, acid-catalyst and loading effects rest on few studies. The laboratory effect is estimated relative to the recorded inputs and includes unrecorded feedstock and process differences. The protocol was registered by timestamped repository commits rather than in a public registry, two implementation deviations were made after the first development run (Section 2.7), and the locked studies had been used in earlier, unrelated analyses of model transfer. No new experiments were performed.


# 4. Conclusions

A within-study meta-analysis of 127 hydrothermal liquefaction and carbonization studies separated process effects from laboratory effects. Within studies, bio-oil yield rose by about 1.07 wt% per 10 °C up to 300 °C and not beyond, solid yield fell most steeply below 300 °C, and catalysts raised bio-oil yield by 5.5–8.5 wt% and energy recovery by 12.1–19.6 percentage points by shifting mass from the solid to the liquid products. These average effects were robust, and temperature effects replicated in held-out studies, but their size varied strongly between laboratories, and laboratory offsets (12.5–15.8 wt% for bio-oil) exceeded every process effect on bio-oil yield. Pooled machine-learning models reproduced the average effects but not their variability, and average effects did not predict individual held-out studies better than assuming no change. Quantitative guidance for HTL and HTC should therefore be stated with between-laboratory prediction intervals and confirmed by a few local experiments.

# Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper.

# Funding

This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.

# Declaration of generative AI and AI-assisted technologies in the manuscript preparation process

During the preparation of this work the authors used an AI assistant (Claude, Anthropic) to search and verify literature metadata, write analysis code, run the computational experiments and draft the manuscript text. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the published article.

# Data availability

All data analysed in this study are publicly available under the CC BY 4.0 licence: the curated hydrothermal treatment/liquefaction database, Version 1.0.0 (RADAR4Chem; https://doi.org/10.22000/8bnbhqccf4aq7kea) (Elfetni, 2026), and the hydrochar database used for external validation (4TU.ResearchData; https://doi.org/10.4121/834c3f22-f46a-4808-a0fe-46298be6a133.v1) (Abdeldayem et al., 2025). The analysis code, the list of locked test studies, configuration files, processed result files and per-run predictions will be made available by the corresponding author on reasonable request (contact details on the title page).

# Appendix A. Supplementary data

Supplementary material (Sections S1–S7: literature search, protocol and deviations, data, sensitivity and moderator analyses, nitrogen content, transfer of literature-trained machine-learning models to new studies, reproducibility) accompanies this article.

# References

::: {custom-style="Bibliography"}
Abdeldayem, O., Al-Sakkari, E., Ortiz, D., Dupont, C., Ferras, D., Ouali, M.-S., Ragab, A., Kennedy, M., 2025. Database underlying the research for the development of machine learning models for predicting the physicochemical properties of hydrochar [dataset]. 4TU.ResearchData. https://doi.org/10.4121/834c3f22-f46a-4808-a0fe-46298be6a133.v1
:::

::: {custom-style="Bibliography"}
Akhtar, J., Amin, N.A.S., 2011. A review on process conditions for optimum bio-oil yield in hydrothermal liquefaction of biomass. Renew. Sustain. Energy Rev. 15(3), 1615-1624. https://doi.org/10.1016/j.rser.2010.11.054
:::

::: {custom-style="Bibliography"}
Bulsink, P., de Miguel Mercader, F., Sandström, L., van de Beld, B., Preto, F., Zacher, A., Oasmaa, A., Dahmen, N., Funke, A., Bronson, B., 2020. Results of the International Energy Agency Bioenergy Round Robin on the Analysis of Heteroatoms in Biomass Liquefaction Oils. Energy Fuels 34(9), 11123-11133. https://doi.org/10.1021/acs.energyfuels.0c02090
:::

::: {custom-style="Bibliography"}
Chen, T., Guestrin, C., 2016. XGBoost: A scalable tree boosting system, in: Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 785-794. https://doi.org/10.1145/2939672.2939785
:::

::: {custom-style="Bibliography"}
DerSimonian, R., Laird, N., 1986. Meta-analysis in clinical trials. Control. Clin. Trials 7(3), 177-188. https://doi.org/10.1016/0197-2456(86)90046-2
:::

::: {custom-style="Bibliography"}
Dimitriadis, A., Bezergianni, S., 2017. Hydrothermal liquefaction of various biomass and waste feedstocks for biocrude production: A state of the art review. Renew. Sustain. Energy Rev. 68, 113-125. https://doi.org/10.1016/j.rser.2016.09.120
:::

::: {custom-style="Bibliography"}
Djandja, O.S., Hu, Y., Zeng, Y., He, Q.S., 2027. Predicting bio-oil yield from hydrothermal liquefaction of lignocellulosic biomass: machine learning approach and uncertainty propagation via joint bootstrap Monte Carlo. Fuel 430, 141091. https://doi.org/10.1016/j.fuel.2026.141091
:::

::: {custom-style="Bibliography"}
Egger, M., Smith, G.D., Schneider, M., Minder, C., 1997. Bias in meta-analysis detected by a simple, graphical test. BMJ 315(7109), 629-634. https://doi.org/10.1136/bmj.315.7109.629
:::

::: {custom-style="Bibliography"}
Elfetni, S., 2026. Unified, curated dataset of biomass hydrothermal treatment/liquefaction experiments for lignocellulosic and lignin-rich biomass — Version 1.0.0 [dataset]. Center for the Transformation of Chemistry. https://doi.org/10.22000/8bnbhqccf4aq7kea
:::

::: {custom-style="Bibliography"}
Elfetni, S., Thinius, S., Dwivedi, P., Seeberger, P.H., Tyrikos-Ergas, T., 2026. Energy and carbon routing in hydrothermal lignocellulosic biomass conversion: an uncertainty-aware machine-learning framework. Elsevier BV. https://doi.org/10.2139/ssrn.6816225
:::

::: {custom-style="Bibliography"}
Elfetni, S., Thinius, S., Dwivedi, P., Seeberger, P.H., Tyrikos-Ergas, T., 2027. Conservation-informed machine learning for physically admissible four-phase hydrothermal liquefaction surrogate modelling. Bioresour. Technol. 463, 135587. https://doi.org/10.1016/j.biortech.2026.135587
:::

::: {custom-style="Bibliography"}
Elliott, D.C., Biller, P., Ross, A.B., Schmidt, A.J., Jones, S.B., 2015. Hydrothermal liquefaction of biomass: Developments from batch to continuous process. Bioresour. Technol. 178, 147-156. https://doi.org/10.1016/j.biortech.2014.09.132
:::

::: {custom-style="Bibliography"}
Febroni, L.V., Rosa, A.P., Borges, A.C., 2026. Microaeration enhances methane production in anaerobic digestion: A systematic review and meta-analysis. Bioresour. Technol. 459, 135162. https://doi.org/10.1016/j.biortech.2026.135162
:::

::: {custom-style="Bibliography"}
Friedman, J.H., 2001. Greedy function approximation: A gradient boosting machine. Ann. Stat. 29(5), 1189-1232. https://doi.org/10.1214/aos/1013203451
:::

::: {custom-style="Bibliography"}
Funke, A., Ziegler, F., 2010. Hydrothermal carbonization of biomass: A summary and discussion of chemical mechanisms for process engineering. Biofuels Bioprod. Biorefin. 4(2), 160-177. https://doi.org/10.1002/bbb.198
:::

::: {custom-style="Bibliography"}
Gollakota, A., Kishore, N., Gu, S., 2018. A review on hydrothermal liquefaction of biomass. Renew. Sustain. Energy Rev. 81, 1378-1392. https://doi.org/10.1016/j.rser.2017.05.178
:::

::: {custom-style="Bibliography"}
Gungor, S., Insel, M.A., Sadikoglu, H., Melikoglu, M., 2025. Prediction of Biocrude Oil Yield From Biomass Hydrothermal Liquefaction Via Interpretable Machine Learning Using Higher Heating Value and Process Parameters. BioEnergy Res. 18(1), 100. https://doi.org/10.1007/s12155-025-10906-z
:::

::: {custom-style="Bibliography"}
Hartung, J., Knapp, G., 2001. On tests of the overall treatment effect in meta‐analysis with normally distributed responses. Stat. Med. 20(12), 1771-1782. https://doi.org/10.1002/sim.791
:::

::: {custom-style="Bibliography"}
Higgins, J.P.T., Thompson, S.G., 2002. Quantifying heterogeneity in a meta‐analysis. Stat. Med. 21(11), 1539-1558. https://doi.org/10.1002/sim.1186
:::

::: {custom-style="Bibliography"}
Hussain, T., Ji, M., Xi, Z., Bai, H., Li, R., Liu, Q., Yang, X., Pan, J., 2027. A quantitative synthesis of carbon and nitrogen losses during animal and poultry manure composting: drivers, pathways, and mitigation. Bioresour. Technol. 465, 136142. https://doi.org/10.1016/j.biortech.2026.136142
:::

::: {custom-style="Bibliography"}
IntHout, J., Ioannidis, J.P.A., Rovers, M.M., Goeman, J.J., 2016. Plea for routinely presenting prediction intervals in meta-analysis. BMJ Open 6(7), e010247. https://doi.org/10.1136/bmjopen-2015-010247
:::

::: {custom-style="Bibliography"}
Jiang, C., Pang, R., Wang, W., Xie, B., Zhan, M., Luo, J., Su, Y., 2026. Microplastics divert carbon flow in anaerobic digestion: a meta-analysis reveals product-specific effects. Bioresour. Technol. 449, 134381. https://doi.org/10.1016/j.biortech.2026.134381
:::

::: {custom-style="Bibliography"}
Katongtung, T., Phromphithak, S., Onsree, T., Tippayawong, N., 2024. Machine Learning Approach for Predicting Hydrothermal Liquefaction of Lignocellulosic Biomass. BioEnergy Res. 17(4), 2246-2258. https://doi.org/10.1007/s12155-024-10773-0
:::

::: {custom-style="Bibliography"}
Leng, L., Zhang, W., Chen, Q., Zhou, J., Peng, H., Zhan, H., Li, H., 2022. Machine learning prediction of nitrogen heterocycles in bio-oil produced from hydrothermal liquefaction of biomass. Bioresour. Technol. 362, 127791. https://doi.org/10.1016/j.biortech.2022.127791
:::

::: {custom-style="Bibliography"}
Libra, J.A., Ro, K.S., Kammann, C., Funke, A., Berge, N.D., Neubauer, Y., Titirici, M.-M., Fühner, C., Bens, O., Kern, J., Emmerich, K.-H., 2011. Hydrothermal carbonization of biomass residuals: a comparative review of the chemistry, processes and applications of wet and dry pyrolysis. Biofuels 2(1), 71-106. https://doi.org/10.4155/bfs.10.81
:::

::: {custom-style="Bibliography"}
Lundberg, S., Lee, S.-I., 2017. A Unified Approach to Interpreting Model Predictions, in: Adv. Neural Inf. Process. Syst. 30. arXiv:1705.07874
:::

::: {custom-style="Bibliography"}
Peterson, A.A., Vogel, F., Lachance, R.P., Fröling, M., Antal, J.M.J., Tester, J.W., 2008. Thermochemical biofuel production in hydrothermal media: A review of sub- and supercritical water technologies. Energy Environ. Sci. 1(1), 32. https://doi.org/10.1039/b810100k
:::

::: {custom-style="Bibliography"}
Riley, R.D., Higgins, J.P.T., Deeks, J.J., 2011. Interpretation of random effects meta-analyses. BMJ 342(feb10 2), d549-d549. https://doi.org/10.1136/bmj.d549
:::

::: {custom-style="Bibliography"}
Sidik, K., Jonkman, J.N., 2002. A simple confidence interval for meta‐analysis. Stat. Med. 21(21), 3153-3159. https://doi.org/10.1002/sim.1262
:::

::: {custom-style="Bibliography"}
Tian, Y., Kim, J., Liu, Y., 2025. Interpretable machine learning model for bio-oil property prediction from hydrothermal liquefaction of biomass via graph neural networks-based molecular structure. Energy 329, 136708. https://doi.org/10.1016/j.energy.2025.136708
:::

::: {custom-style="Bibliography"}
Toor, S.S., Rosendahl, L., Rudolf, A., 2011. Hydrothermal liquefaction of biomass: A review of subcritical water technologies. Energy 36(5), 2328-2342. https://doi.org/10.1016/j.energy.2011.03.013
:::

::: {custom-style="Bibliography"}
Valdez, P.J., Dickinson, J.G., Savage, P.E., 2011. Characterization of product fractions from hydrothermal liquefaction of Nannochloropsis sp. and the influence of solvents. Energy Fuels 25(7), 3235-3243. https://doi.org/10.1021/ef2004046
:::

::: {custom-style="Bibliography"}
Veroniki, A.A., Jackson, D., Viechtbauer, W., Bender, R., Bowden, J., Knapp, G., Kuss, O., Higgins, J.P., Langan, D., Salanti, G., 2015. Methods to estimate the between‐study variance and its uncertainty in meta‐analysis. Res. Synth. Methods 7(1), 55-79. https://doi.org/10.1002/jrsm.1164
:::

::: {custom-style="Bibliography"}
Viechtbauer, W., 2005. Bias and Efficiency of Meta-Analytic Variance Estimators in the Random-Effects Model. J. Educ. Behav. Stat. 30(3), 261-293. https://doi.org/10.3102/10769986030003261
:::

::: {custom-style="Bibliography"}
Zhang, W., Li, J., Liu, T., Leng, S., Yang, L., Peng, H., Jiang, S., Zhou, W., Leng, L., Li, H., 2021. Machine learning prediction and optimization of bio-oil production from hydrothermal liquefaction of algae. Bioresour. Technol. 342, 126011. https://doi.org/10.1016/j.biortech.2021.126011
:::

::: {custom-style="Bibliography"}
Zhu, Z., Toor, S.S., Rosendahl, L., Yu, D., Chen, G., 2015. Influence of alkali catalyst on product yield and properties via hydrothermal liquefaction of barley straw. Energy 80, 284-292. https://doi.org/10.1016/j.energy.2014.11.071
:::



