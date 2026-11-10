# Unified, curated dataset of biomass hydrothermal treatment/liquefaction experiments for lignocellulosic and lignin-rich biomass

**RADAR Version 1 — corrected release**

> **Version 1 supersedes Version 0 and provides the complete publication dataset
> comprising 3,693 records and 145 documented variables.**

## Overview

A harmonized, provenance-tracked database of hydrothermal conversion records,
centered on lignocellulosic and lignin-rich biomass (lignocellulosic-dominant),
with mixed and boundary feedstocks also present. It is compiled from scientific
literature and institutional research sources. It underpins an associated
research manuscript on uncertainty-aware prediction of energy and carbon routing
in hydrothermal biomass conversion.

The dataset comprises 3,693 literature-derived records covering 433 biomass
samples. Source title and identifier are provided for every record; more
granular `Provenance` and `Ref` information is retained where available.

| Property | Value |
|---|---|
| Records | **3,693** |
| Variables (columns) | **145** |
| Distinct biomass samples | **433** |
| Temporal coverage | **1982–2026** |
| Process subtypes | HTL 2,166 · HTL_solvothermal 994 · HTC 524 · APR 9 |
| Reaction temperature (actual range) | **20–603 °C** (typical window 200–400 °C) |
| Residence time (actual range) | **0–2,640 min** |
| License (dataset) | **CC BY 4.0** |
| `master_dataset.csv` SHA-256 | `c8827a378879ce9d8d1ed7539e451b7b741eec30c5cc070487e3f467a4a42a6b` |

> **Actual vs. typical ranges.** The numbers above are the *actual* extremes
> present in the data. Most runs sit in the 200–400 °C hydrothermal window, but
> the dataset deliberately includes milder and supercritical points; do not read
> 200–400 °C as the full range.

## Quick start

```python
import pandas as pd

df = pd.read_csv("master_dataset.csv")
print(len(df), "records ×", df.shape[1], "columns")
print("Years:", df["year"].min(), "-", df["year"].max())

# HTL runs above 350 C
htl = df[df["process_subtype"].str.contains("HTL", na=False)]
print((htl["T_reaction_C"] >= 350).sum(), "HTL runs >= 350 C")
```

The package includes two fully executed notebooks and matching static HTML
exports in `examples/`. The HTML files can be viewed without installing Python.
Re-executing the notebooks requires pandas, NumPy, Matplotlib, and a Jupyter
environment.

## Package contents

```
master_dataset.csv        Primary dataset (3,693 × 145), UTF-8 CSV
README.md                 This file
CITATION.cff              Machine-readable citation metadata (CFF 1.2.0)
LICENSE                   CC BY 4.0 (dataset)
NOTICE.md                 Licensing / third-party rights notice
CHANGELOG.md              Version history
VERSION                   Version string
MANIFEST-SHA256.txt       SHA-256 of every packaged file
metadata/                 Machine-readable metadata and column documentation
examples/                 Executed visual notebooks + static HTML exports
```

## Examples

Two fully executed notebooks (with embedded outputs) and matching self-contained
HTML exports are provided in [`examples/`](examples/). Both open independently,
require no network access, and open `master_dataset.csv` read-only:

- [`dataset_overview.ipynb`](examples/dataset_overview.ipynb) /
  [`dataset_overview.html`](examples/dataset_overview.html) — executed visual
  summary of coverage, process composition, operating conditions, completeness,
  product yields, a feedstock Van Krevelen plot, and QA diagnostics.
- [`curation_traceability.ipynb`](examples/curation_traceability.ipynb) /
  [`curation_traceability.html`](examples/curation_traceability.html) — selected
  curation and normalization pathways (table extraction, figure digitization,
  and documented calculated/imputed values) shown on fixed example records.

## Data organization (column groups)

- **Provenance** — `paper_title`, `DOI`, `year`, `Provenance`, `Ref`
- **Feedstock identity** — `Feedstock`, `Family_std`
- **Feedstock composition** — ultimate analysis (C, H, O, N, S, Ash),
  lignocellulosic fractions (lignin, cellulose, hemicellulose, extractives), HHV,
  O/C & H/C molar ratios, Lignin Readiness Index (LRI)
- **Quality / closure** — elemental and polymer mass-balance sums and flags
- **Process conditions** — temperature, residence/ramp time, pressure, solvent,
  catalyst, reactor, atmosphere, loading, heating rate, yield basis
- **Yields** — biocrude, hydrochar/solid residue, aqueous, gas; energy yields
- **Biocrude properties** — elemental composition, HHV, O/C & H/C, carbon yield
- **Hydrochar/solid-residue properties** — elemental composition, HHV, O/C & H/C,
  carbon yield
- **Derived descriptors** — engineered features and readiness indices
- **Tracking** — measurement methods, imputation flags, and derivation sources

Every column is documented in [`metadata/column_metadata.csv`](metadata/column_metadata.csv)
(name, description, unit, dtype, group, completeness).

> **Legacy column names** containing `biooil`, `biochar` or `char` are retained
> for backward compatibility with the analysis pipeline. Narrative documentation
> uses **biocrude** and **hydrochar/solid residue** according to process context.

## Units

| Property | Unit | Basis |
|---|---|---|
| Temperature | °C | — |
| Time | min | — |
| Pressure | MPa (or `autogenous`) | — |
| Composition | wt% | dry or daf (see `yield_basis`) |
| Yields | wt% | initial dry feedstock |
| Energy | MJ/kg | dry basis |
| Ratios | — | molar |

## Data quality & imputation

Core descriptors (C, O, temperature, time) exceed 98 % completeness;
lignocellulosic composition ≈ 96 %; product yields ≈ 70–80 %; detailed product
composition ≈ 20–40 %. Oxygen is taken by difference where not measured; HHV is
estimated with the Channiwala–Parikh correlation where not reported; selected
descriptors are imputed with Random Forest models or family medians. Selected
imputed and derived variables are accompanied by explicit `*_imputed`,
`*_method`, or `*_source` tracking fields, while deterministic derived variables
are documented in the column metadata.

## Data-quality note

Version 1 preserves the record structure used in the associated analysis. Exact
repeated rows are present in the release. Users constructing independent
condition-level subsets should apply and document an analysis-appropriate
deduplication rule.

## Source publications

Bibliographic information and extracted facts originate from the cited primary
literature; source title and identifier are provided for every record, and more
granular `Provenance` and `Ref` information is retained where available. **The
source-publication PDFs are
not redistributed** (copyright of the respective publishers). See
[`NOTICE.md`](NOTICE.md). When using this dataset, please cite **both** this
dataset **and** the relevant primary publications.

## License

The **dataset and its original documentation** are licensed **CC BY 4.0**
(<https://creativecommons.org/licenses/by/4.0/>). See [`LICENSE`](LICENSE) and
[`NOTICE.md`](NOTICE.md). Third-party source articles remain under their own
rights and are **not** relicensed. The dataset is provided as a FAIR-oriented
resource with machine-readable metadata.

## Citation

See [`CITATION.cff`](CITATION.cff). The authoritative Version 1 DOI is provided
on the RADAR landing page and in the repository metadata. This release supersedes
the previous version (RADAR Version 0), DOI `10.22000/0b7ffmw1jtca3gw3`
(relation: IsNewVersionOf).

## Contact

**Seifallah Elfetni** · CTC gGmbH · ORCID
[0000-0003-3615-627X](https://orcid.org/0000-0003-3615-627X)
