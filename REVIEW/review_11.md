# Review round 11 (v2) — Reviewer #11: hydrothermal-conversion chemist (domain plausibility)

Scope: the v2 additions (trend atlas E13, contrasts E12, ranking E14) judged from the standpoint of HTL/HTC chemistry.

| # | Severity | Issue | Response / fix | Status |
|---|---|---|---|---|
| 11.1 | MAJOR | E13 pools conventional and solvothermal HTL. Solvent-derived carbon and different temperature windows could create spurious pooled trends. | Stratified E13 by process subtype (scripted: `e13_empirical_trends.by_process`). Below 300 °C every stratum shows the same direction: bio-oil positive (HTL 78–100 %, solvothermal 88 % of studies same sign), solid negative (HTC, HTL, solvothermal 82–100 %). Supplementary Table S14 + sentence in §3.4. | **Fixed** |
| 11.2 | MAJOR | Are the recovered trends chemically plausible? | Bio-oil increases up to ~300 °C, plateaus at 300–350 °C and tends to fall above 350 °C; solid yield decreases with temperature, most steeply below 250 °C — consistent with the HTL/HTC reviews cited (Gollakota 2018; Funke & Ziegler 2010). Stated without over-claiming mechanisms. | Addressed |
| 11.3 | MODERATE | "Pairs differing only in temperature" in batch reactors also differ in autogenous pressure and heat-up time. | These are inherent to a temperature change in batch HTL and are part of what a practitioner changes; noted implicitly (the slope is the *operational* temperature effect). | Accepted, noted here |
| 11.4 | MODERATE | Residence-time slopes mix very short and very long times. | Reported as "no consistent effect" with CI; not over-interpreted. | Accepted |
| 11.5 | MINOR | The 325 °C rule of thumb was derived from the same development data (E13). | Disclosed in Methods (centre of the E13 optimum band); this favours the rule, so the comparison is conservative for the models. | Disclosed |
