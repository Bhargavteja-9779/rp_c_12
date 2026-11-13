# 4. Conclusions

Machine-learning models trained on published hydrothermal-conversion data predict runs of studies they have seen far better than runs of a new study: random splitting overstated accuracy about two-fold, and on locked studies no learner predicted bio-oil yields substantially better than the training mean. Half to two-thirds of the out-of-study error variance was a study-level offset that recorded work-up and yield-basis descriptors did not explain. Laboratories agree on the direction of the temperature response, but models did not predict within-study changes better than absolute yields, and an exploratory advantage in choosing conditions did not replicate on held-out studies. What did hold was honest uncertainty — conformal intervals calibrated across studies raised coverage from {{cov_range_RC}} to {{cov_range_SC}} — and the correction of predictions with a few local runs. Study-grouped validation with a locked test set, study-calibrated intervals and local anchoring runs are recommended as minimum practice (Table 9), and claims about trends or optimal conditions should be supported by held-out-study evidence.

# CRediT authorship contribution statement

[Author 1]: Conceptualization, Methodology, Software, Formal analysis, Writing – original draft. [Author 2]: Validation, Writing – review & editing. [Author 3]: Supervision, Writing – review & editing. *(To be completed by the authors.)*

# Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper. *(To be confirmed by the authors.)*

# Declaration of generative AI and AI-assisted technologies in the manuscript preparation process

During the preparation of this work the authors used an AI assistant (Claude, Anthropic) to search and verify literature metadata, write analysis code, run the computational experiments and draft the manuscript text. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the published article. *(The authors must verify, adapt and confirm this statement before submission.)*

# Data availability

All data analysed are publicly available under CC BY 4.0 [@Elfetni2026data; @TU4data]. The complete code, the locked test-study list, configuration files, raw result files and the scripts that generate every table and figure are available at [repository URL to be inserted; archived DOI to be minted at acceptance].

# Acknowledgements

The authors thank the curators of the hydrothermal treatment/liquefaction database and of the 4TU hydrochar database for releasing their data openly. *(Funding: to be completed by the authors.)*

# Appendix A. Supplementary data

Supplementary material (Sections S1–S9, Tables S1–S17, Figs. S1–S4: literature screening, protocol and addenda, additional benchmark and sensitivity results, exploratory adaptive intervals, error analysis by subgroup, STRATA with different base learners, trend and ranking analyses, reproducibility) accompanies this article.

# References

<<REFERENCES>>
