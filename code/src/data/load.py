"""Loading, cleaning and feature construction for the hydrothermal-conversion database.

Implements PROTOCOL.md §3-§5.  All operations here are *row-wise deterministic* (no statistics are
estimated from the data), so they cannot leak information between training and test folds.
Fold-dependent preprocessing (imputation, scaling) lives in ``src.preprocessing.pipeline``.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RAW = os.path.join(ROOT, "data", "raw", "htt_radar_v1", "master_dataset.csv")
LOCK = os.path.join(ROOT, "config", "locked_test_studies.json")
EXPECTED_SHA256 = "c8827a378879ce9d8d1ed7539e451b7b741eec30c5cc070487e3f467a4a42a6b"

TARGETS = {
    "biooil": dict(col="Yield_biooil_wt_pct", processes=("HTL", "HTL_solvothermal"), range=(0, 100)),
    "solid": dict(col="Yield_char_wt_pct", processes=("HTL", "HTL_solvothermal", "HTC"), range=(0, 100)),
    # secondary product-quality targets (PROTOCOL Addendum A2)
    "hhv_biooil": dict(col="HHV_biooil_MJ_per_kg", processes=("HTL", "HTL_solvothermal"), range=(5, 50), exclude_computed="HHV_biooil_method"),
    "c_biooil": dict(col="C_biooil_wt_pct", processes=("HTL", "HTL_solvothermal"), range=(20, 95)),
}

# ----------------------------------------------------------------------------------------------
# categorical harmonisation (regular expressions on the curated free-text fields)
# ----------------------------------------------------------------------------------------------
CATALYST_CLASSES = [
    ("none", r"^\s*(none|no catalyst|h2o|water|-)?\s*$"),
    ("alkali_carbonate", r"k2co3|na2co3|carbonate|khco3|nahco3|k3po4"),
    ("alkali_hydroxide", r"naoh|koh|ca\(oh\)2|lioh|hydroxide|naoh"),
    ("acid", r"h2so4|hcl|acetic acid|formic acid|h3po4|oxalic|citric|zncl2|acid"),
    ("metal_supported", r"ni|co|mo|ru|pt|pd|fe|cu|zn|ce|zeolite|zsm|al2o3|sba|hβ|h-beta|/c\b|mg|mn|la|zr|ti|w"),
]
MEDIUM_CLASSES = [
    ("water_alcohol", r"(water|h2o).*(ethanol|methanol|propanol|butanol|etoh|meoh)|(ethanol|methanol|propanol|butanol|etoh|meoh).*(water|h2o)"),
    ("water_with_donor", r"(water|h2o).*(formic|glycerol|phenol|tetralin|h2)|(formic|glycerol).*(water|h2o)"),
    ("alcohol", r"ethanol|methanol|propanol|butanol|etoh|meoh|glycerol|ethylene glycol"),
    ("ketone", r"aceton|ketone|mibk"),
    ("other_organic", r"tetralin|thf|dioxane|toluene|phenol|cresol|dmso|gamma|γ|valerolactone|oil"),
    ("water", r"water|h2o|deioni|distilled|hot-compressed|sludge|was\b"),
]
EXTRACTION_SOLVENTS = {
    "dcm": r"dcm|dichloromethane|methylene chloride",
    "acetone": r"aceton",
    "ethyl_acetate": r"ethyl acetate|etoac|\bea\b",
    "diethyl_ether": r"diethyl ether|\bether\b",
    "thf": r"\bthf\b|tetrahydrofuran",
    "alcohol": r"methanol|ethanol|meoh|etoh",
    "hydrocarbon": r"hexane|toluene|benzene|heptane|cyclohexane",
    "chlorinated_other": r"chloroform",
}


def _match_first(text: str, classes) -> str:
    t = text.lower() if isinstance(text, str) else ""
    for name, pat in classes:
        if re.search(pat, t):
            return name
    return "other"


def catalyst_class(s: str) -> str:
    t = s.lower().strip() if isinstance(s, str) else "none"
    if t in ("", "none", "no catalyst", "nan", "h2o", "water", "-"):
        return "none"
    return _match_first(t, CATALYST_CLASSES[1:])


def medium_class(s: str) -> str:
    return _match_first(s, MEDIUM_CLASSES)


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ----------------------------------------------------------------------------------------------
@dataclass
class Dataset:
    target: str
    X: pd.DataFrame          # all candidate features (base + protocol)
    y: np.ndarray
    groups: np.ndarray       # study identifier (DOI)
    year: np.ndarray
    meta: pd.DataFrame       # descriptive columns for error analysis (not features)
    base_features: list
    protocol_features: list
    exclusions: dict = field(default_factory=dict)

    def subset(self, mask) -> "Dataset":
        mask = np.asarray(mask)
        return Dataset(self.target, self.X.loc[mask].reset_index(drop=True), self.y[mask], self.groups[mask],
                       self.year[mask], self.meta.loc[mask].reset_index(drop=True), self.base_features,
                       self.protocol_features, self.exclusions)


def read_raw(check_hash: bool = True) -> pd.DataFrame:
    if check_hash:
        h = sha256(RAW)
        if h != EXPECTED_SHA256:
            raise RuntimeError(f"Dataset checksum mismatch: {h}")
    return pd.read_csv(RAW, low_memory=False)


def locked_test_studies() -> set:
    return set(json.load(open(LOCK))["test_studies"])


def build_features(d: pd.DataFrame) -> tuple[pd.DataFrame, list, list]:
    """Row-wise deterministic feature construction (PROTOCOL §5)."""
    f = pd.DataFrame(index=d.index)
    # --- base: feedstock chemistry ------------------------------------------------------------
    for src, dst in [("C_feed_wt_pct", "feed_C"), ("H_feed_wt_pct", "feed_H"), ("O_feed_wt_pct", "feed_O"),
                     ("N_feed_wt_pct", "feed_N"), ("Ash_feed_wt_pct", "feed_ash"), ("Lignin_feed_wt_pct", "feed_lignin"),
                     ("Cellulose_feed_wt_pct", "feed_cellulose"), ("Hemicellulose_feed_wt_pct", "feed_hemicellulose")]:
        f[dst] = pd.to_numeric(d[src], errors="coerce")
    # --- base: conditions --------------------------------------------------------------------
    f["T_C"] = pd.to_numeric(d["T_reaction_C"], errors="coerce")
    f["log_t_min"] = np.log1p(pd.to_numeric(d["t_residence_min"], errors="coerce").clip(lower=0))
    f["solid_loading_wt_pct"] = pd.to_numeric(d["IC_feed_wt_pct_slurry"], errors="coerce")
    f["heating_rate_C_min"] = pd.to_numeric(d["heating_rate_C_per_min"], errors="coerce")
    f["cat_ratio"] = pd.to_numeric(d["cat_biomass_ratio_kg_kg"], errors="coerce").fillna(0.0)
    cat = d["catalyst"].fillna("none").astype(str).map(catalyst_class)
    f.loc[f["cat_ratio"] <= 0, "cat_ratio"] = 0.0
    for c in ["alkali_carbonate", "alkali_hydroxide", "acid", "metal_supported", "other"]:
        f[f"cat_{c}"] = (cat == c).astype(float)
    med = d["solvent_or_medium"].fillna("").astype(str).map(medium_class)
    for c in ["water_alcohol", "water_with_donor", "alcohol", "ketone", "other_organic", "other"]:
        f[f"medium_{c}"] = (med == c).astype(float)
    p = d["pressure_reaction_MPa"].fillna("").astype(str).str.lower()
    f["gas_pressurised"] = p.str.contains(r"h2|n2|ar\b|argon|nitrogen|hydrogen|co\b|initial", regex=True).astype(float)
    f["proc_solvothermal"] = (d["process_subtype"] == "HTL_solvothermal").astype(float)
    f["proc_HTC"] = (d["process_subtype"] == "HTC").astype(float)
    base = list(f.columns)
    # --- protocol / reporting descriptors (P) -------------------------------------------------
    yb = d["yield_basis"].fillna("").astype(str).str.lower()
    sep = d["separation_method"].fillna("").astype(str).str.lower()
    both = yb + " | " + sep
    f["P_basis_daf"] = yb.str.contains(r"ash-free|ash free|\bdaf\b|ash/catalyst-free|ash- and|organic matter", regex=True).astype(float)
    f["P_basis_incl_coreactant"] = yb.str.contains(r"\+|glycerol|formic|phenol|solvent\)|biomass\+|as loaded|air-dried", regex=True).astype(float)
    f["P_multi_fraction_product"] = both.str.contains(r"\blo\b|\bho\b|light oil|heavy oil|wso|water-soluble oil|fraction|ho\+|lo\+", regex=True).astype(float)
    f["P_by_difference"] = both.str.contains(r"by difference|difference|subtraction|100 ?[−-]", regex=True).astype(float)
    named = np.zeros(len(d), dtype=bool)
    for k, pat in EXTRACTION_SOLVENTS.items():
        m = sep.str.contains(pat, regex=True).to_numpy()
        f[f"P_extract_{k}"] = m.astype(float)
        named |= m
    f["P_extract_none_named"] = (~named).astype(float)
    f["P_separation_not_stated"] = (sep.str.strip() == "").astype(float)
    vol = d["reactor"].fillna("").astype(str).str.extract(r"(\d+\.?\d*)\s*(ml|mL|L|l)\b")
    v = pd.to_numeric(vol[0], errors="coerce")
    v = np.where(vol[1].str.lower().eq("l"), v * 1000.0, v)
    f["P_log10_reactor_mL"] = np.log10(pd.to_numeric(pd.Series(v, index=d.index), errors="coerce"))
    protocol = [c for c in f.columns if c.startswith("P_")]
    return f, base, protocol


def load_target(target: str, split: str = "dev", df: pd.DataFrame | None = None) -> Dataset:
    """split in {'dev', 'test', 'all'}; dev/test defined by the locked study list."""
    spec = TARGETS[target]
    d = read_raw() if df is None else df
    ex = {"rows_total": int(len(d))}
    lock = locked_test_studies()
    in_test = d["DOI"].isin(lock)
    d = d[in_test] if split == "test" else (d[~in_test] if split == "dev" else d)
    ex["rows_in_split"] = int(len(d))
    d = d[d["process_subtype"].isin(spec["processes"])]
    ex["rows_after_process_filter"] = int(len(d))
    y = pd.to_numeric(d[spec["col"]], errors="coerce")
    d = d[y.notna()]; y = y[y.notna()]
    ex["rows_with_target"] = int(len(d))
    lo, hi = spec.get("range", (0, 100))
    ok = (y >= lo) & (y <= hi)
    ex["excluded_target_out_of_range"] = int((~ok).sum()); d, y = d[ok], y[ok]
    if spec.get("exclude_computed"):
        comp = d[spec["exclude_computed"]].notna().to_numpy()
        ex["excluded_computed_target"] = int(comp.sum()); d, y = d[~comp], y[~comp]
    carbon_basis = d["yield_basis"].fillna("").str.lower().str.contains(r"feed carbon|carbon-basis|carbon basis|c-basis")
    ex["excluded_carbon_basis"] = int(carbon_basis.sum()); d, y = d[~carbon_basis], y[~carbon_basis]
    need = d["C_feed_wt_pct"].notna() & d["O_feed_wt_pct"].notna() & d["T_reaction_C"].notna() & d["t_residence_min"].notna()
    ex["excluded_missing_core_inputs"] = int((~need).sum()); d, y = d[need], y[need]
    cnt = d.groupby("DOI")["DOI"].transform("size")
    ex["excluded_single_row_studies"] = int((cnt < 2).sum()); d, y = d[cnt >= 2], y[cnt >= 2]
    ex["rows_final"] = int(len(d)); ex["studies_final"] = int(d["DOI"].nunique())
    X, base, protocol = build_features(d)
    meta = pd.DataFrame({
        "DOI": d["DOI"].values, "year": d["year"].values, "family": d["Family_std"].values,
        "process": d["process_subtype"].values, "feedstock": d["Feedstock"].values,
        "medium": d["solvent_or_medium"].values, "catalyst": d["catalyst"].values,
    })
    return Dataset(target, X.reset_index(drop=True), y.to_numpy(float), d["DOI"].astype(str).to_numpy(),
                   d["year"].to_numpy(int), meta, base, protocol, ex)


if __name__ == "__main__":
    for t in TARGETS:
        ds = load_target(t, "dev")
        print(t, ds.X.shape, ds.exclusions)
        print("  protocol prevalence:", {c: round(float(ds.X[c].mean()), 3) for c in ds.protocol_features if not c.startswith("P_log")})
