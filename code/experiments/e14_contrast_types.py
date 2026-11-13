"""E14 (PROTOCOL Addendum B, exploratory): contrast accuracy by contrast type (a) and ranking vs domain heuristics (b)."""
from __future__ import annotations
import os, sys
import numpy as np, pandas as pd
from joblib import Parallel, delayed
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data.load import load_target
from src.evaluation.core import grouped_folds, restore
from src.models.contrast import MODELS, within_pairs
from src.utils import out_dirs, load_config
from experiments.common import load_cell
from experiments.e13_empirical_trends import pairs_differing_only_in


def fold(target, params, X, y, g, tr, te, seed, fi, Tvals):
    mods = {m: MODELS[m]("xgb", params, n_jobs=1).fit(X.iloc[tr], y[tr], g[tr]) for m in ("A", "W", "PD")}
    Xte, yte, gte = X.iloc[te].reset_index(drop=True), y[te], g[te]
    for md in mods.values():
        md.prepare(Xte, gte)
    ia, ib = within_pairs(gte, min_n=2)
    typ = np.array(["other"] * len(ia), dtype=object)
    for var, lab in [("T_C", "temperature_only"), ("log_t_min", "time_only")]:
        sel = {(i, j) for _, i, j in pairs_differing_only_in(Xte, gte, var, [c for c in Xte.columns if c != var])}
        sel |= {(j, i) for i, j in sel}
        typ[[k for k, (a, b) in enumerate(zip(ia, ib)) if (a, b) in sel]] = lab
    dy = yte[ia] - yte[ib]
    rows = []
    for m, md in mods.items():
        e = md.contrast_idx(ia, ib) - dy
        for t in np.unique(typ):
            k = typ == t
            rows.append(dict(target=target, model=m, seed=seed, fold=fi, type=t, n=int(k.sum()), sse=float((e[k] ** 2).sum()), ss=float((dy[k] ** 2).sum())))
    # (b) ranking vs heuristics
    rk = []
    T = Xte["T_C"].to_numpy()
    for s in np.unique(gte):
        idx = np.flatnonzero(gte == s)
        if len(idx) < 5:
            continue
        ys = yte[idx]
        cand = {m: idx[np.argmax(md.score()[idx])] for m, md in mods.items()}
        if target == "biooil":
            cand["rule_T300"] = idx[np.argmin(np.abs(T[idx] - 300))]; cand["rule_T325"] = idx[np.argmin(np.abs(T[idx] - 325))]
        else:
            cand["rule_lowest_T"] = idx[np.argmin(T[idx])]
        for name, c in cand.items():
            rk.append(dict(target=target, seed=seed, fold=fi, study=s, method=name, regret=float(ys.max() - yte[c]), random=float(ys.max() - ys.mean())))
    return rows, rk


def run(mode="full", split="dev"):
    cfg, D = load_config(mode), out_dirs(mode)
    R, K = [], []
    for target in ["biooil", "solid"]:
        ds = load_target(target, "dev"); params = restore(load_cell(D, target, "base", "xgb")["params"])
        if split == "dev":
            X, y, g = ds.X[ds.base_features], ds.y, ds.groups
            jobs = [(s, fi, tr, te) for s in cfg["outer_seeds"] for fi, (tr, te) in enumerate(grouped_folds(ds.groups, k=cfg["outer_folds"], seed=s))]
        else:
            te_ds = load_target(target, "test")
            X = pd.concat([ds.X[ds.base_features], te_ds.X[ds.base_features]], ignore_index=True)
            y = np.r_[ds.y, te_ds.y]; g = np.r_[ds.groups, te_ds.groups]
            jobs = [(0, 0, np.arange(len(ds.y)), np.arange(len(ds.y), len(y)))]
        out = Parallel(n_jobs=cfg["n_jobs"])(delayed(fold)(target, params, X, y, g, tr, te, s, fi, None) for s, fi, tr, te in jobs)
        for r, k in out:
            R.extend(r); K.extend(k)
    R = pd.DataFrame(R); K = pd.DataFrame(K)
    sfx = "" if split == "dev" else "_locked"
    R.to_csv(os.path.join(D["results"], f"e14a_contrast_types{sfx}.csv"), index=False); K.to_csv(os.path.join(D["results"], f"e14b_ranking_heuristics{sfx}.csv"), index=False)
    s = R.groupby(["target", "model", "type", "seed"]).agg(sse=("sse", "sum"), ss=("ss", "sum"), n=("n", "sum")).reset_index()
    s["r2"] = 1 - s.sse / s.ss
    print(s.groupby(["target", "type", "model"]).agg(r2=("r2", "mean"), n_pairs=("n", "mean")).round(3).to_string())
    print(K.groupby(["target", "study", "method"]).regret.mean().unstack().groupby(level=0).median().round(2).to_string())


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "full", sys.argv[2] if len(sys.argv) > 2 else "dev")
