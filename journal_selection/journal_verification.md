# Journal verification log

## Method for acceptance timelines (why it is trustworthy)
Publisher-deposited article history dates were used instead of marketing statistics:
* **PubMed** `<History><PubMedPubDate PubStatus="received|accepted">` — deposited by Elsevier, ACS, OUP, Springer for MEDLINE/PubMed journals (`scripts/pm_times.py`).
* **Crossref** `assertion` fields `received`/`accepted` — deposited by Springer Nature (`scripts/cr_times.py`).
* Elsevier and OUP do **not** deposit history dates in Crossref; journals of these publishers that are not in PubMed cannot be verified this way.
* The measured quantity is **submission (received) → acceptance**, which is what the user constraint refers to. It is *not* first-decision time and *not* acceptance→online time.
* Limitation: "received" may be the date of the final (revised) submission for some publishers/articles; for Elsevier it is the original submission date.

## Legitimacy / integrity checks — Bioresource Technology
* Published by Elsevier since 1991 (formerly *Biological Wastes*); MEDLINE-indexed; in the Clarivate Master Journal List (secondary confirmation).
* Not on any hijacked-journal list encountered; no publication-integrity concern found in searches.
* Editorial standards: peer-reviewed; the journal's recent ML papers include grouped validation and conformal UQ (Elfetni et al., 2026), indicating reviewers who will scrutinise validation design.

## Unverifiable items (stated honestly)
* 2025 JIF (8.2 vs 9.0 conflict across secondary sources) and quartile were **not** read from Clarivate JCR directly.
* Official guide-for-authors page blocked (Cloudflare error 1000-series); rules taken from search snippets of the official page.
* APC for gold OA not verified.

## Sources consulted (secondary, for JIF/quartile/guide snippets)
* https://en.wikipedia.org/wiki/Bioresource_Technology
* https://manusights.com/blog/bioresource-technology-impact-factor
* https://www.journalmetrics.org/journal/bioresource-technology
* https://www.sciencedirect.com/journal/bioresource-technology/publish/guide-for-authors (snippets via search engine)
* https://www.ucm.es/quimica_analitica/file/anal-chem-jcr-journalresults-08-2026 (Analytica Chimica Acta JIF)
