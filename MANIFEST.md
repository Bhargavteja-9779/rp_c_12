# Target_Journal_Submission — file manifest

The repository root is the submission package for ***Bioresource Technology*** (Elsevier).

```
/ (Target_Journal_Submission)
├── journal_selection/
│   ├── selected_journal.md          # decision record (JCR status, measured acceptance times, guidelines, risks)
│   ├── journal_comparison.md        # 46 journals screened (PubMed/Crossref history dates)
│   ├── journal_verification.md      # method + legitimacy checks + unverifiable items
│   ├── scripts/                     # pm_times.py, cr_times.py, ml_subset.py, run_screen.py
│   └── data/                        # raw measurement outputs (JSON)
├── manuscript/
│   ├── Final_Manuscript.docx        # Elsevier submission layout (A4, double-spaced, line numbers, native equations)
│   ├── Final_Manuscript.pdf
│   ├── Supplementary_Material.docx / .pdf
│   ├── Highlights.docx              # separate file (journal requirement)
│   ├── Graphical_Abstract.png / .pdf# separate file (journal requirement; 1328:531 ratio)
│   ├── cover_letter.docx
│   ├── build_log.json               # every value inserted into the text, with cited reference keys
│   └── src/                         # templates, value generator, verified-reference builder, DOCX/PDF builder
├── code/                            # complete research code (see code/README.md)
│   ├── src/  experiments/  tests/  config/  data/raw/
│   ├── run_all.py   requirements.txt   environment.yml   README.md   LICENSE
├── results/
│   ├── raw_results.csv              # all per-run rows of every experiment
│   ├── metrics.json  statistics.json
│   ├── statistics/                  # meta-regression, paired tests, locked sensitivity
│   ├── predictions/                 # out-of-fold and locked-test predictions
│   └── experiment_logs/             # logs, E1 cell cache, environment
├── figures/                         # fig01–fig13 + graphical abstracts (PNG 300 dpi + PDF); fig07–fig10 appear as Figs. S1–S4
├── tables/                          # all manuscript and supplementary tables (CSV + Markdown)
├── supplementary/literature/        # PubMed corpus, literature matrix, verified references, abstracts
├── REVIEW/
│   ├── review_01.md … review_15.md  # 10 rounds (v1) + 5 rounds (v2)
│   ├── citation_audit.md
│   ├── final_audit.md
│   └── rejection_risk_report.md
├── PROGRESS.md                      # resume log
└── MANIFEST.md
```
