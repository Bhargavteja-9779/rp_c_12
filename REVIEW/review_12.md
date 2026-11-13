# Review round 12 (v2) — Reviewer #12: pre-registration / research-integrity auditor

Checked the git history (`git log`) against the claims of pre-registration.

| Claim | Evidence (commit, UTC) | Verdict |
|---|---|---|
| Locked study list created before any model | 04a5079, 2026-11-10 21:44 | ✓ |
| Protocol before any model fitting | d40eac3, 21:52 (first E1 log 22:00) | ✓ |
| Decisions frozen before the locked evaluation | 69ccfd1 03:36 → 639845a 03:37 | ✓ |
| Addendum A before E12 | d24f01c 2026-11-13 11:58 → E12 launched 12:02 | ✓ |
| Addendum A2 before quality-target runs | 2f4af56 12:05 → runs started ≈12:39 | ✓ |
| Addendum B registered after seeing E12 development results | 71a1d8f 12:37 (states this explicitly) | ✓ exploratory, disclosed |
| Addendum C before any locked E12/E14 evaluation | 9668526 12:39 → locked runs after | ✓ |
| E13 pre-registered? | **No** — run at ≈12:04 and committed with A2 at 12:05 without being described in an addendum | **Issue** |

## Issues
| # | Severity | Issue | Fix | Status |
|---|---|---|---|---|
| 12.1 | MAJOR | E13 was presented alongside registered analyses without stating that it was not registered. | Methods now labels E13 "descriptive, not pre-registered". | **Fixed** |
| 12.2 | MAJOR | Readers cannot verify timestamps without the repository. | Supplementary Table S16 lists the commits (generated from `git log`). | **Fixed** |
| 12.3 | MODERATE | The locked studies' *level* results were seen before Addendum A; knowledge of which locked studies are atypical could, in principle, influence later choices. | Disclosed in Addendum A; no model, feature or hyper-parameter was changed afterwards (E12 reuses E1 hyper-parameters). | Disclosed |
| 12.4 | MODERATE | Many analyses → garden of forking paths. | All registered hypotheses are reported regardless of outcome; exploratory analyses are labelled; the one exploratory positive finding was submitted to a locked confirmation and failed — reported. | Addressed |
| 12.5 | MINOR | Two v2 analyses (process stratification, study-weighted R²) were first computed ad hoc. | Moved into scripts; outputs verified byte-identical. | **Fixed** |
