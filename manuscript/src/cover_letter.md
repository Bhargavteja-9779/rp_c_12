[Date]

The Editor-in-Chief
*Bioresource Technology*
Elsevier

**Submission of a Full Length Article: "Machine-learning models of hydrothermal biomass conversion trained on literature data: transfer to unseen studies and study-calibrated prediction intervals"**

Dear Editor,

We submit the above manuscript for consideration as a Full Length Article in *Bioresource Technology*.

Machine-learning surrogates of hydrothermal liquefaction and carbonization trained on literature-compiled data are now common in the journal, but they are almost always validated by splitting experimental runs at random. We asked what such models can actually deliver for a laboratory whose study they have not seen. Using the largest public curated hydrothermal database (3,693 runs, 188 studies), a pre-registered analysis plan and 38 studies locked away before any modelling, we tested five capabilities on held-out studies: predicting absolute yields, explaining study offsets from reported metadata, predicting within-study trends, choosing the best of planned runs, and providing honest uncertainty with local anchoring.

The answer is sobering but useful. Random splitting overstated accuracy about two-fold; on locked studies no learner predicted bio-oil yields substantially better than the training mean; and pre-registered hypotheses that would let literature models do more — trend transfer with offset-invariant learners, metadata-explained offsets, model-guided choice of conditions — were not supported on held-out studies, all of which we report. A model-free analysis nevertheless shows that laboratories agree on the direction of the temperature response, and two practices worked: conformal intervals calibrated across studies (coverage {{cov_range_SC}} instead of {{cov_range_RC}}) and anchoring predictions with a few local runs. We condense this into a capability matrix and a minimum validation checklist intended to help authors and reviewers of the many literature-trained bioresource models submitted to the journal.

The work builds on, and is complementary to, recent contributions in this journal — in particular the physically admissible HTL surrogates of Elfetni et al. (2027, doi:10.1016/j.biortech.2026.135587), which documented inter-study heterogeneity.

All analyses are reproducible from public CC-BY data with the supplied code; every number in the manuscript is generated programmatically from the result files. The analysis protocol and locked test set were committed before modelling, and all deviations are reported.

We confirm that this manuscript is original, has not been published previously, and is not under consideration for publication elsewhere. All authors have approved the manuscript and agree with its submission. The study used only published, openly licensed data and involved no human participants or animals; no ethical approval was required. The authors declare no competing interests. The use of generative AI in preparing this work is disclosed in the manuscript as required by Elsevier policy.

Suggested reviewers (optional): [to be completed by the authors].

Yours sincerely,

[Corresponding author name]
[Affiliation, address]
[E-mail] · [ORCID]
On behalf of all co-authors
