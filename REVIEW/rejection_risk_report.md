# Rejection-risk report — v4 (2026-11-25), after desk rejection of v3 by Bioresource Technology

v4 is a different paper: the first within-study meta-analysis of HTL/HTC process effects (Addenda E, F), written in the style of BT
meta-analyses (benchmark: REVIEW/v4_rejection_diagnosis_and_bt_benchmark.md).

| # | Risk | Severity | Mitigation / status |
|---|---|---|---|
| 1 | Editor sees "same authors, same database, rejected before" | Moderate | Different question, positive process findings; cover letter discloses the earlier rejection honestly |
| 2 | "Meta-analysis of one curated database, not a systematic review" | Moderate–high | Stated in methods and limitations; novelty search documented; scope restricted to lignocellulosic biomass |
| 3 | Dependence/variance approximation of contrasts | Moderate | Bootstrap, one-per-study estimator, PM τ², LOO; limitation stated |
| 4 | Failed confirmatory locked test | Moderate | Reported transparently; interpreted (heterogeneity), temperature effects replicated |
| 5 | No new experiments | Moderate for BT | Usual for BT meta-analyses; stated |
| 6 | Mechanistic depth (why catalysts shift solid → liquid) | Moderate | Cautious, cited to reviews; no unsupported mechanism claims |
| 7 | Timeline ≤ 72 d not guaranteed | — | BT all-article median 75 d (46 % ≤ 72 d); ML-hydrothermal subset faster; BT meta-analyses 57–206 d in the benchmark; fallbacks measured slower (Waste Manag 112 d, Biotechnol Biofuels Bioprod 101 d, Green Chem 86 d) |
| 8 | Placeholders (second author, affiliations) and AI declaration | Blocking until filled | Author action |

---

# Rejection-risk report — updated for v3 (2026-11-18), after an external pre-submission review

## What changed in v3
A professor's pre-submission review asked for a deployment framing, sequential local adaptation, a decision system, a laboratory case
study, explicit scope (bio-oil and solid only), a novelty table versus Elfetni et al., an accurate availability statement, a multi-database
literature search and transparent pre-registration. All were implemented (Addendum D committed before E15–E17 ran; see
manuscript/Response_to_Review). Key new results: STRATA beat literature-only and local-only for unseen development studies at every k;
on locked solid studies it beat literature-only (Holm p = 0.014 at k = 3); on locked bio-oil studies local-only beat STRATA (p = 0.009);
the pre-registered applicability-domain threshold flagged no locked study (decision rule untestable).

| # | Risk (v3) | Severity | Mitigation | Status |
|---|---|---|---|---|
| A | Novelty vs Elfetni et al. 2027 (local calibration already shown there) | Moderate | Table 1 comparison; claims limited to coverage on unseen studies, literature-vs-local comparison with re-calibrated intervals, decision analyses, locked/external tests | Partly (inherent) |
| B | No new experiments; retrospective simulation only | Moderate–high for an experimental journal | Stated in abstract, methods, limitations, cover letter; case studies on locked studies | Disclosed |
| C | Decision system largely negative (AD threshold flagged none) | Moderate | Reported as such; workflow changed to compare B vs C | Disclosed |
| D | Mixed held-out results (locked bio-oil favours local-only) | Moderate | Presented as a finding with practical consequence | Disclosed |
| E | Pre-registration only via repository commits | Low–moderate | Stated explicitly; commit table in supplement | Disclosed |
| F | Code only on request (user's choice) | Low–moderate (some reviewers prefer open code) | Data DOIs given; code offered on request | Author choice |
| G | Placeholders: second author's name/affiliation/e-mail and first author's affiliation | **Blocking until filled** | Fill before submission | Requires author action |
| H | AI-assistance declaration | High if undisclosed | Section included; authors must verify and adapt | Requires author action |
| I | Peer-review type of the journal not verified (official guide blocked) | Low | Both a manuscript with author details and an anonymised manuscript plus a separate title page are supplied | Mitigated |

---

# Final rejection-risk report (Phase 41) — updated for v2 (2026-11-13)

## What changed in v2 and why
The user judged v1 likely to be rejected. Diagnosis: v1's message was largely negative and close to Elfetni et al. (2027).
v2 tested, under pre-registered addenda, whether literature models can do more for a new laboratory (transfer within-study
trends, rank planned runs) — the constructive question. The answer was mostly negative (T1–T3 not supported; an exploratory ranking
advantage failed its pre-registered locked confirmation), but v2 adds a model-free, process-robust finding that laboratories agree on the
direction of temperature effects, and turns the paper into a capability audit with a checklist for the journal's authors and reviewers.
This raises novelty and practical value relative to v1 and to the prior art; it cannot remove the risk that editors dislike a
predominantly negative study.


No manuscript can be guaranteed acceptance; risks below are those that remain after fifteen review rounds (10 for v1, 5 for v2).

| # | Risk | Evidence | Severity | Mitigation | Fixed? |
|---|---|---|---|---|---|
| 1 | Novelty (incremental to Elfetni et al. 2027; STRATA assembled from known parts) | Same database; publication-aware validation and k-shot point calibration already published; Fisch 2021, Bersson & Hoff 2024, Dunn 2023. v2 adds trend/ranking audit, trend atlas, checklist | **Moderate** (was High in v1) | Contribution re-framed as evaluation + validated workflow; six results not in prior work listed in review_08; prior art cited | Partly (inherent) |
| 2 | Methodology | Nested study-level design, locked test, pre-registration | Low | — | Yes |
| 3 | Dataset (single curated literature DB; ~7 % cross-study duplicates; imputed fractions) | E10 | Moderate | External DB, duplicate audit, limitations | Partly |
| 4 | Statistical (approximate conformal validity; locked n = 28–30 studies; post-hoc analyses) | CIs; post-hoc labels | Moderate | Claims stated as approximate/marginal; CIs; post-hoc flagged | Yes (disclosed) |
| 5 | Reproducibility | One-command pipeline, vendored data, tests, fresh-clone audit | Low | — | Yes |
| 6 | Baselines | 12 learners, equal budget; TabPFN not run (licence) | Low–moderate | Reported as deviation | Partly |
| 7 | Generalisation (locked solids SC coverage 0.82; HTC subset 0.83; temporal shift) | Table 4 | Moderate | Reported, claims weakened | Disclosed |
| 8 | Writing (number-dense abstract; long Table 4) | review_07 | Low | — | Mostly |
| 9 | Journal formatting (reference-style rule for first submission not verified from the official guide; AI declaration wording) | Guide page blocked | Low–moderate | Consistent author–year style; Elsevier "declaration of generative AI" section included | Partly |
| 10 | Citation | All verified; abstract-level support checks | Low | citation_audit.md | Yes |
| 11 | Journal scope ("statistics paper", no experiments) | review_09 | **Moderate–high** | Domain discussion, practitioner/curator recommendations, cover letter | Partly |
| 12 | Reviewer from the dataset-curating group | Most relevant expert group | Moderate | Respectful, explicit differentiation; their work acknowledged | Partly |
| 13 | Publication integrity / compliance (extensive AI assistance; authorship placeholders) | Elsevier AI policy requires disclosure and author responsibility | **High if undisclosed** | Declaration drafted; authors must verify every result, adapt the statement, complete CRediT/affiliations/funding, and confirm originality before submission | Requires author action |
| 14 | Predominantly negative findings | Most capability hypotheses failed on held-out studies | **Moderate–high** | Framed as audit with constructive outputs (capability matrix, trend atlas, checklist); all failures reported | Partly (inherent) |

## Target-journal facts relevant to the decision
* Measured submission→acceptance for comparable papers (ML on hydrothermal conversion in *Bioresource Technology*, n = 20): median 53.5 d (IQR 38–70), 80 % ≤ 72 d. For all ML papers in the journal (Jul 2025–Oct 2026): median 70.5 d, 55 % ≤ 72 d. These are historical distributions, **not guarantees**; a major revision would very likely push acceptance beyond 72 days.
* JIF 8.2 (2025; secondary sources, conflicting 9.0) and Q1 — **not verified in JCR directly**.

## Decision (Phase 42)
**READY FOR SUBMISSION (v2) — conditional on author actions**, scientifically: all pre-registered experiments, the
locked evaluation, fifteen review rounds, the review-driven experiments (E9–E11) and the pre-registered v2 analyses (E12–E14, with locked confirmation) are complete; every claim is
traceable to generated results; remaining weaknesses are inherent to a computational study on one curated
database and are disclosed.

Before submission the human authors must: (1) independently check the analyses and the manuscript; (2) complete
author names, affiliations, CRediT, funding, competing-interest statement and repository URL/DOI; (3) review and
adapt the generative-AI declaration to describe their actual use truthfully; (4) verify the 2025 JIF/quartile and the
current guide for authors (reference style at first submission) on the official sites; (5) optionally add suggested
reviewers in the cover letter.
