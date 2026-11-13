"""E13: model-free check of 'trends transfer, levels do not' (secondary, descriptive; added with Addendum A).

Within each development study, find run pairs that differ ONLY in temperature (all other base features identical,
same feedstock) and pairs that differ only in residence time. For each such pair compute the observed slope
(Δy per +10 °C, or per doubling of residence time). Per study, the median slope in a condition band is a
'measured trend'. Compare between-study dispersion of trends with between-study dispersion of levels at
comparable conditions (study means of y within the same band).
"""
from __future__ import annotations

import os, sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data.load import load_target
from src.statistics.stats import cluster_bootstrap_ci
from src.utils import out_dirs, load_config, dump

T_BANDS = [(150, 250), (250, 300), (300, 350), (350, 450)]


def pairs_differing_only_in(X, groups, var, others):
    """Pairs (i, j) of the same study with identical values (rounded) of every column in `others` and different `var`."""
    key = X[others].round(4).fillna(-999).astype(str).agg("|".join, axis=1)
    out = []
    for (s, k), idx in pd.Series(np.arange(len(X))).groupby([groups, key.values]):
        idx = idx.to_numpy()
        if len(idx) < 2:
            continue
        v = X[var].to_numpy()[idx]
        for a in range(len(idx)):
            for b in range(a + 1, len(idx)):
                if np.isfinite(v[a]) and np.isfinite(v[b]) and v[a] != v[b]:
                    i, j = (idx[a], idx[b]) if v[a] < v[b] else (idx[b], idx[a])
                    out.append((s, i, j))
    return out


def run(mode="full"):
    cfg, D = load_config(mode), out_dirs(mode)
    res, rows = {}, []
    for target in ["biooil", "solid"]:
        ds = load_target(target, "dev"); X = ds.X[ds.base_features].copy(); y = ds.y; g = ds.groups
        for var, unit, transform in [("T_C", "per +10 °C", lambda a, b: (b - a) / 10.0), ("log_t_min", "per doubling of residence time", lambda a, b: (b - a) / np.log(2))]:
            others = [c for c in ds.base_features if c != var]
            prs = pairs_differing_only_in(X, g, var, others)
            if not prs:
                continue
            P = pd.DataFrame(prs, columns=["study", "i", "j"])
            xi, xj = X[var].to_numpy()[P.i], X[var].to_numpy()[P.j]
            P["slope"] = (y[P.j] - y[P.i]) / transform(xi, xj)
            P["mid_T"] = 0.5 * (X["T_C"].to_numpy()[P.i] + X["T_C"].to_numpy()[P.j])
            P["level"] = 0.5 * (y[P.i] + y[P.j])
            for lo, hi in (T_BANDS if var == "T_C" else [(0, 1000)]):
                q = P[(P.mid_T >= lo) & (P.mid_T < hi)]
                st = q.groupby("study").agg(slope=("slope", "median"), level=("level", "mean"), n=("slope", "size"))
                if len(st) < 5:
                    continue
                sd_slope, sd_level = float(st.slope.std()), float(st.level.std())
                med = float(st.slope.median())
                frac_same_sign = float((np.sign(st.slope) == np.sign(med)).mean()) if med != 0 else float("nan")
                boot = cluster_bootstrap_ci(q.rename(columns={"study": "study"}), lambda d: float(d.groupby("study").slope.median().median()),
                                            n_boot=cfg["bootstrap"], seed=0)
                rows.append(dict(target=target, variable=var, unit=unit, band=f"{lo}-{hi}" if var == "T_C" else "all", n_studies=int(len(st)),
                                 n_pairs=int(len(q)), median_slope=med, slope_ci_low=boot[0], slope_ci_high=boot[1],
                                 frac_studies_same_sign=frac_same_sign, sd_slope_between_studies=sd_slope, sd_level_between_studies=sd_level,
                                 # effect of a typical step (10 °C or one doubling) relative to the spread of levels
                                 sd_step_effect_over_sd_level=sd_slope / sd_level if sd_level > 0 else float("nan")))
    df = pd.DataFrame(rows); df.to_csv(os.path.join(D["results"], "e13_empirical_trends.csv"), index=False)
    print(df.round(3).to_string())
    by_process(cfg, D)


def by_process(cfg, D):
    """Review round 11: temperature slopes stratified by process subtype (HTL, solvothermal HTL, HTC)."""
    out = []
    for t in ["biooil", "solid"]:
        ds = load_target(t, "dev"); X = ds.X[ds.base_features]; y = ds.y; g = ds.groups; proc = ds.meta["process"].to_numpy()
        P = pd.DataFrame(pairs_differing_only_in(X, g, "T_C", [c for c in ds.base_features if c != "T_C"]), columns=["study", "i", "j"])
        P["slope"] = (y[P.j] - y[P.i]) / ((X.T_C.values[P.j] - X.T_C.values[P.i]) / 10)
        P["mid"] = (X.T_C.values[P.i] + X.T_C.values[P.j]) / 2; P["proc"] = proc[P.i]
        for pr in sorted(P.proc.unique()):
            for lo, hi in T_BANDS:
                q = P[(P.proc == pr) & (P.mid >= lo) & (P.mid < hi)]; st = q.groupby("study").slope.median()
                if len(st) < 5:
                    continue
                med = st.median()
                ci = cluster_bootstrap_ci(q, lambda d: float(d.groupby("study").slope.median().median()), n_boot=cfg["bootstrap"], seed=0)
                out.append(dict(target=t, process=pr, band=f"{lo}-{hi}", n_studies=len(st), median_slope=round(med, 2), ci_low=round(ci[0], 2),
                                ci_high=round(ci[1], 2), frac_same_sign=round(float((np.sign(st) == np.sign(med)).mean()), 2)))
    pd.DataFrame(out).to_csv(os.path.join(D["results"], "e13b_trends_by_process.csv"), index=False)


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "full")
