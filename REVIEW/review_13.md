# Review round 13 (v2) — Reviewer #13: statistician (contrast metrics and dependence)

| # | Severity | Issue | Fix / response | Status |
|---|---|---|---|---|
| 13.1 | MAJOR | Pooled contrast R² sums over all within-study pairs, so a study with *n* runs contributes ~*n*²/2 pairs; a few large studies dominate. | Added study-weighted contrast R² (median per-study R² over studies with ≥ 5 runs). It is lower than the pooled value (bio-oil development 0.06–0.10; solids 0.23–0.32; locked bio-oil negative), strengthening the conclusion that within-study changes are not predicted well. Supplementary Table S15 + sentence in §3.4. | **Fixed** |
| 13.2 | MAJOR | Pairs within a study are dependent; tests on pairs would be anti-conservative. | All tests use per-study aggregates (Wilcoxon over studies, Holm). Contrast-interval quantiles weight each study equally. | ✓ |
| 13.3 | MODERATE | Locked-study contrast results driven by two studies (65 % of A's squared contrast error). | Stated in §3.4; per-study tests reported as non-significant. | ✓ |
| 13.4 | MODERATE | Regret has a floor at 0 and many ties for solids (median paired difference 0). | Wilcoxon with zero-difference exclusion (wilcox method) as in all tests; medians and IQRs shown (Fig. 7). | Accepted |
| 13.5 | MINOR | Confirmatory test C1 uses 25 studies; power is limited. | Stated implicitly via CI in Table S13; the conclusion is "not confirmed", not "refuted". Wording checked: "did not replicate", "not established". | ✓ |
