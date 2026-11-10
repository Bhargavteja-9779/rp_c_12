# Selected target journal — Bioresource Technology (Elsevier)

Retrieved / measured: 2026-11-10. Measurement scripts and raw outputs are in
`journal_selection/scripts/` and `journal_selection/data/`.

| Item | Value | Verification status |
|---|---|---|
| TARGET JOURNAL | *Bioresource Technology* | — |
| PUBLISHER | Elsevier Ltd. | ISSN 0960-8524 (print), 1873-2976 (online); in PubMed/MEDLINE ("Bioresour Technol") |
| JCR STATUS | Indexed in Clarivate JCR (SCIE) | Consistent across secondary sources; the Clarivate JCR portal requires institutional login and could **not** be accessed from this environment |
| JCR QUARTILE | Q1 | Reported by secondary sources (Wikipedia, Manusights, journalmetrics.org); **not directly verified in JCR** |
| JOURNAL IMPACT FACTOR | 8.2 (2025 JIF, JCR released June 2026); prior-year value ≈ 9.0 | Secondary sources conflict (8.2 vs 9.0). **Must be confirmed by the authors in JCR before quoting.** |
| JCR SUBJECT CATEGORY | Agricultural Engineering; Biotechnology & Applied Microbiology; Energy & Fuels (category list from secondary sources) | Not directly verified |
| VERIFIED REVIEW/DECISION TIMELINE | Not separately measured (first-decision times are not used anywhere in this selection) | — |
| VERIFIED ACCEPTANCE TIMELINE (submission→acceptance) | **All research articles, pub. Jul 2025–Oct 2026: median 76 d (IQR 59–101), 46 % ≤ 72 d (n = 399).** **ML/chemometrics papers in the same window: median 70.5 d (IQR 54–97), 55 % ≤ 72 d (n = 142).** **ML papers on hydrothermal conversion (closest precedent; n = 20, 2018–2026): median 53.5 d (IQR 38–70), 80 % ≤ 72 d.** | Measured from PubMed `History` `received`/`accepted` dates (publisher-deposited). These are *empirical distributions*, not guarantees. The median for comparable papers is below the 72-day ceiling, but roughly one-fifth to one-half of comparable papers exceeded 72 days. |
| APC | Subscription journal with optional gold OA; no charge for subscription route. OA APC not verified (Elsevier pages blocked from this environment) | Unverified |
| SCOPE FIT | Biomass conversion (thermochemical/hydrothermal), bioenergy, data-driven process modelling — the journal published 20 PubMed-indexed ML papers on hydrothermal conversion, including the direct predecessor of this work (Elfetni et al., 2026, doi:10.1016/j.biortech.2026.135587) | Verified from PubMed corpus (`supplementary/literature/pubmed_ml_hydrothermal_corpus.json`) |
| RESEARCH FIT | The manuscript addresses transferability and uncertainty of literature-trained hydrothermal-conversion models — a methodological limitation of the journal's own recent ML literature | — |
| KEY AUTHOR GUIDELINES | Abstract ≤ 250 words; 3–5 highlights, ≤ 85 characters each incl. spaces, separate file; graphical abstract required at submission (separate file); keywords; Elsevier declarations (competing interests, CRediT, data availability, **declaration of generative-AI use**) | Abstract/highlight/graphical-abstract rules confirmed via search snippets of the official guide; full official guide could not be fetched (Cloudflare block) |
| KEY REJECTION RISKS | (1) Desk rejection as "incremental to Elfetni et al. 2026"; (2) "no new experiments" (purely data-driven); (3) "ML methods paper, not bioresource science" scope objection; (4) reviewers from the dataset-curating group | Addressed in manuscript design (see REVIEW/) |

## Why not an Oxford University Press journal

Every OUP journal measured had a submission→acceptance median far above 72 days:
Bioinformatics 149 d, Briefings in Bioinformatics 127 d, JAMIA 120 d, Nucleic Acids Research 138 d,
Database 167 d, GigaScience 198 d, NAR Genomics & Bioinformatics 155 d, Bioinformatics Advances 126 d
(`data/pubmed_all_articles.json`). OUP does not deposit history dates in Crossref, so journals not in
PubMed (e.g., *Journal of Computational Design and Engineering*) could not be measured at all.
No OUP journal therefore satisfied the ≤ 72-day requirement with verifiable evidence.

## Requirements that could not be fully satisfied/verified

1. JIF and quartile were not verified in Clarivate JCR itself (portal access unavailable).
2. The acceptance timeline is a measured historical distribution; no journal guarantees a decision time.
3. APC and complete current guide-for-authors text could not be fetched from Elsevier (blocked).
