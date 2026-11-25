"""Within-study meta-analysis of process and feedstock effects (PROTOCOL Addendum E).

Effects are estimated only from comparisons between runs of the same study that differ in a single factor ("cells"), so that
study-level (laboratory) offsets cancel. Study-level effects are pooled with a random-effects model (REML, Hartung-Knapp-Sidik-Jonkman CI,
prediction interval).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats

from src.data.load import read_raw, build_features, catalyst_class, medium_class, locked_test_studies

OUTCOMES = {
    "biooil": dict(col="Yield_biooil_wt_pct", proc=("HTL", "HTL_solvothermal"), rng=(0, 100), unit="wt%"),
    "solid": dict(col="Yield_char_wt_pct", proc=("HTL", "HTL_solvothermal", "HTC"), rng=(0, 100), unit="wt%"),
    "aqueous": dict(col="Yield_aqueous_wt_pct", proc=("HTL", "HTL_solvothermal", "HTC"), rng=(0, 100), unit="wt%"),
    "gas": dict(col="Yield_gas_wt_pct", proc=("HTL", "HTL_solvothermal", "HTC"), rng=(0, 100), unit="wt%"),
    "hhv_biooil": dict(col="HHV_biooil_MJ_per_kg", proc=("HTL", "HTL_solvothermal"), rng=(5, 50), unit="MJ/kg", computed="HHV_biooil_method"),
    "energy_biooil": dict(col="_ER_biooil", proc=("HTL", "HTL_solvothermal"), rng=(0, 150), unit="%"),  # computed in frame()
    "n_biooil": dict(col="N_biooil_wt_pct", proc=("HTL", "HTL_solvothermal"), rng=(0, 20), unit="wt%"),
}
PRIMARY = ["biooil", "solid"]
T_BANDS = [(0, 250), (250, 300), (300, 350), (350, 1000)]
BAND_LABEL = {(0, 250): "<250 °C", (250, 300): "250–300 °C", (300, 350): "300–350 °C", (350, 1000): "≥350 °C"}
COMP = ["feed_lignin", "feed_cellulose", "feed_hemicellulose", "feed_ash", "feed_N"]
CAT_CLASSES = ["alkali_carbonate", "alkali_hydroxide", "acid", "metal_supported", "other"]
MED_CLASSES = ["water_alcohol", "alcohol", "water_with_donor", "other_organic"]
ROUND = {"T": 0, "t": 2, "load": 1}
MIN_STEP = {"T": 5.0, "t": 0.25, "load": 1.0}  # °C, log2 units, percentage points


def frame(split: str = "dev") -> pd.DataFrame:
    """One row per run with condition columns and all outcomes (NaN where not applicable)."""
    d = read_raw()
    lock = locked_test_studies()
    d = d[~d["DOI"].isin(lock)] if split == "dev" else (d[d["DOI"].isin(lock)] if split == "test" else d)
    d = d.reset_index(drop=True)
    f, base, _ = build_features(d)
    out = pd.DataFrame({"study": d["DOI"].values, "feed": d["Feedstock"].astype(str).str.strip().str.lower().values,
                        "family": d["Family_std"].values, "proc": d["process_subtype"].values})
    for c in COMP + ["feed_C", "feed_H", "feed_O"]:
        out[c] = f[c].values
    out["T"] = f["T_C"].values
    tmin = pd.to_numeric(d["t_residence_min"], errors="coerce")
    out["log2t"] = np.log2(tmin.where(tmin > 0)).values
    out["load"] = f["solid_loading_wt_pct"].values
    out["hr"] = f["heating_rate_C_min"].values
    out["cat"] = d["catalyst"].fillna("none").astype(str).map(catalyst_class).values
    out["cat_ratio"] = f["cat_ratio"].values
    out.loc[out.cat == "none", "cat_ratio"] = 0.0
    out["med"] = d["solvent_or_medium"].fillna("").astype(str).map(medium_class).values
    out["atm"] = d["atmosphere"].fillna("").astype(str).str.lower().str.strip().values
    out["gas_p"] = f["gas_pressurised"].values
    # energy recovery to bio-oil (%) = yield x measured bio-oil HHV / feed HHV (deviation E-2: the database column
    # Energy_yield_biooil_pct equals yield x HHV / 100, i.e. MJ per kg feed, not a recovery)
    hhv_ok = d["HHV_biooil_method"].isna()
    d["_ER_biooil"] = (pd.to_numeric(d["Yield_biooil_wt_pct"], errors="coerce") * pd.to_numeric(d["HHV_biooil_MJ_per_kg"], errors="coerce").where(hhv_ok)
                       / pd.to_numeric(d["HHV_feed_MJ_per_kg"], errors="coerce"))
    carbon_basis = d["yield_basis"].fillna("").str.lower().str.contains(r"feed carbon|carbon-basis|carbon basis|c-basis").values
    for k, s in OUTCOMES.items():
        y = pd.to_numeric(d[s["col"]], errors="coerce")
        ok = y.between(*s["rng"]) & d["process_subtype"].isin(s["proc"])
        if k in ("biooil", "solid", "aqueous", "gas"):
            ok &= ~carbon_basis
        if s.get("computed"):
            ok &= d[s["computed"]].isna()
        out[k] = y.where(ok).values
    return out


CONDS = ["feed", "feed_lignin", "feed_cellulose", "feed_hemicellulose", "feed_ash", "feed_N", "T", "log2t", "load", "hr", "cat", "cat_ratio",
         "med", "atm", "gas_p", "proc"]
FACTOR_COLS = {"T": ["T"], "t": ["log2t"], "load": ["load"], "cat": ["cat", "cat_ratio"], "med": ["med"],
               "feed": ["feed", "feed_lignin", "feed_cellulose", "feed_hemicellulose", "feed_ash", "feed_N"]}


def cell_keys(F: pd.DataFrame, factor: str) -> pd.Series:
    others = [c for c in CONDS if c not in FACTOR_COLS[factor]]
    k = F[others].copy()
    for c in others:
        k[c] = k[c].round(4) if k[c].dtype.kind == "f" else k[c]
    parts = [k[c].map(lambda x: "nan" if (x is None or (isinstance(x, float) and np.isnan(x))) else str(x)) for c in others]
    key = F["study"].astype(str) + "§"
    for p_ in parts:
        key = key + "|" + p_
    return key


def contrasts(F: pd.DataFrame, factor: str, outcome: str) -> pd.DataFrame:
    """Observed within-study contrasts. Columns: study, cell, level (band/class), effect, plus run indices i, j (for prediction)."""
    q = F[F[outcome].notna()].copy()
    if factor in ("T", "t", "load"):
        col = FACTOR_COLS[factor][0]
        q = q[q[col].notna()]
    q["_cell"] = cell_keys(q, factor).values
    rows = []
    for cell, c in q.groupby("_cell"):
        if len(c) < 2:
            continue
        s = c.study.iloc[0]
        if factor in ("T", "t", "load"):
            col = FACTOR_COLS[factor][0]
            c = c.assign(**{col: c[col].round(ROUND[factor])})
            g = c.groupby(col)
            lv = g[outcome].mean(); idx = g.apply(lambda z: list(z.index))
            xs = lv.index.to_numpy()
            if len(xs) < 2:
                continue
            for a, b in zip(xs[:-1], xs[1:]):
                if b - a < MIN_STEP[factor]:
                    continue  # numerical guard (deviation log, Addendum E): ignore near-identical levels
                unit = {"T": 10.0, "t": 1.0, "load": 10.0}[factor]
                eff = (lv[b] - lv[a]) / ((b - a) / unit)
                mid = 0.5 * (a + b) if factor == "T" else float(c["T"].iloc[0])
                band = next(BAND_LABEL[bb] for bb in T_BANDS if bb[0] <= mid < bb[1]) if factor == "T" else "all"
                rows.append(dict(study=s, cell=cell, level=band, effect=float(eff), x_lo=float(a), x_hi=float(b), T=float(mid),
                                 i=idx[a], j=idx[b], dy=float(lv[b] - lv[a])))
        elif factor == "cat":
            base = c[c.cat == "none"]
            if base.empty:
                continue
            for cl in CAT_CLASSES:
                tr = c[(c.cat == cl) & (c.cat_ratio != 0)]
                if tr.empty:
                    continue
                rows.append(dict(study=s, cell=cell, level=cl, effect=float(tr[outcome].mean() - base[outcome].mean()), T=float(c["T"].iloc[0]),
                                 i=list(base.index), j=list(tr.index), dy=float(tr[outcome].mean() - base[outcome].mean())))
        elif factor == "med":
            base = c[c.med == "water"]
            if base.empty:
                continue
            for cl in MED_CLASSES:
                tr = c[c.med == cl]
                if tr.empty:
                    continue
                rows.append(dict(study=s, cell=cell, level=cl, effect=float(tr[outcome].mean() - base[outcome].mean()), T=float(c["T"].iloc[0]),
                                 i=list(base.index), j=list(tr.index), dy=float(tr[outcome].mean() - base[outcome].mean())))
    return pd.DataFrame(rows)


def study_effects(C: pd.DataFrame, min_studies: int = 5) -> pd.DataFrame:
    """Study-level mean effects and variances s2_w / m_j (s2_w pooled within-study variance of contrasts), per level."""
    out = []
    for lv, q in C.groupby("level"):
        g = q.groupby("study").effect
        m = g.size(); mu = g.mean()
        dev = q.effect - q.study.map(mu)
        dfw = int((m - 1).clip(lower=0).sum())
        s2w = max(float((dev ** 2).sum() / dfw), 1e-6) if dfw > 0 else np.nan
        if len(mu) < min_studies or not np.isfinite(s2w):
            continue
        out.append(pd.DataFrame({"level": lv, "study": mu.index, "y": mu.values, "m": m.values, "v": s2w / m.values, "s2w": s2w}))
    return pd.concat(out, ignore_index=True) if out else pd.DataFrame(columns=["level", "study", "y", "m", "v", "s2w"])


def reml(y, v, max_iter=200, tol=1e-10):
    """Random-effects meta-analysis (REML tau^2; HKSJ CI; prediction interval; I^2 from Q)."""
    y, v = np.asarray(y, float), np.asarray(v, float); k = len(y)
    w0 = 1 / v; mu0 = np.sum(w0 * y) / np.sum(w0); Q = float(np.sum(w0 * (y - mu0) ** 2))
    tau2 = max(0.0, (Q - (k - 1)) / (np.sum(w0) - np.sum(w0 ** 2) / np.sum(w0)))  # DL start
    for _ in range(max_iter):
        w = 1 / (v + tau2); mu = np.sum(w * y) / np.sum(w)
        new = max(0.0, np.sum(w ** 2 * ((y - mu) ** 2 - v + 1 / np.sum(w))) / np.sum(w ** 2))
        if abs(new - tau2) < tol:
            tau2 = new; break
        tau2 = new
    w = 1 / (v + tau2); mu = float(np.sum(w * y) / np.sum(w))
    qhk = float(np.sum(w * (y - mu) ** 2) / (k - 1)) if k > 1 else np.nan
    se = float(np.sqrt(qhk / np.sum(w))); tcrit = stats.t.ppf(0.975, k - 1)
    p = float(2 * stats.t.sf(abs(mu / se), k - 1)) if se > 0 else np.nan
    sp = float(np.sqrt(tau2 + se ** 2)); tpi = stats.t.ppf(0.975, max(k - 2, 1))
    I2 = max(0.0, (Q - (k - 1)) / Q) if Q > 0 else 0.0
    return dict(k=k, mu=mu, se=se, ci_lo=mu - tcrit * se, ci_hi=mu + tcrit * se, p=p, tau2=float(tau2), tau=float(np.sqrt(tau2)),
                pi_lo=mu - tpi * sp, pi_hi=mu + tpi * sp, I2=float(I2), Q=Q, p_benefit=float(stats.norm.cdf(mu / sp)) if sp > 0 else np.nan)


def pm_tau2(y, v):
    from statsmodels.stats.meta_analysis import combine_effects
    r = combine_effects(np.asarray(y, float), np.asarray(v, float), method_re="iterated", use_t=True)
    return float(r.tau2), float(r.mean_effect_re)


def egger(y, v):
    y, s = np.asarray(y, float), np.sqrt(np.asarray(v, float))
    if len(y) < 10 or np.allclose(s, s[0]):
        return np.nan
    X = np.column_stack([np.ones_like(s), 1 / s]); z = y / s
    beta, *_ = np.linalg.lstsq(X, z, rcond=None); r = z - X @ beta; df = len(z) - 2
    cov = (r @ r / df) * np.linalg.inv(X.T @ X)
    return float(2 * stats.t.sf(abs(beta[0] / np.sqrt(cov[0, 0])), df))


def feedstock_regression(F: pd.DataFrame, outcome: str, min_studies: int = 10):
    """F6: within-cell regression of y on feedstock composition (cell-demeaned), cluster-robust SE by study. Coefficients per +10 wt%."""
    q = F[F[outcome].notna()].dropna(subset=COMP).copy()
    q["_cell"] = cell_keys(q, "feed").values
    nfeed = q.groupby("_cell").feed.transform("nunique")
    q = q[nfeed >= 2]
    if q.study.nunique() < min_studies:
        return None
    Z = q[COMP + [outcome]] - q.groupby("_cell")[COMP + [outcome]].transform("mean")
    X = Z[COMP].to_numpy() / 10.0; y = Z[outcome].to_numpy()
    keep = X.std(axis=0) > 0
    X = X[:, keep]; names = [c for c, k_ in zip(COMP, keep) if k_]
    beta, *_ = np.linalg.lstsq(X, y, rcond=None); r = y - X @ beta
    bread = np.linalg.pinv(X.T @ X); meat = np.zeros((X.shape[1], X.shape[1]))
    for s in q.study.unique():
        m = (q.study == s).to_numpy(); u = X[m].T @ r[m]; meat += np.outer(u, u)
    G = q.study.nunique(); n, p = X.shape
    cov = bread @ meat @ bread * G / (G - 1) * (n - 1) / (n - p)
    se = np.sqrt(np.diag(cov)); t = beta / se
    pv = 2 * stats.t.sf(np.abs(t), G - 1)
    return pd.DataFrame(dict(outcome=outcome, term=names, coef_per_10wt=beta, se=se, ci_lo=beta - stats.t.ppf(0.975, G - 1) * se,
                             ci_hi=beta + stats.t.ppf(0.975, G - 1) * se, p=pv, n_runs=n, n_studies=G, n_cells=q._cell.nunique()))
