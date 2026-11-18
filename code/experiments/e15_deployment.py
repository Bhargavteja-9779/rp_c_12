"""E15 (PROTOCOL Addendum D): sequential local adaptation in a simulated new laboratory.

Settings: development (study-grouped 10-fold × seeds 11/22/33), locked studies (once), external 4TU hydrochar DB (solid).
Writes results/e15_deploy_{setting}.csv (per study × target × order × k × strategy [× draw for random]) and
results/predictions/e15_locked_design_runs.csv.gz (per-run predictions for the case study, E17).
"""
from __future__ import annotations

import os, sys
import numpy as np
import pandas as pd
from joblib import Parallel, delayed

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data.load import load_target
from src.evaluation.core import grouped_folds
from src.models.deploy import simulate, quantiles, per_study_metrics, QPOS
from src.utils import out_dirs, load_config, get_logger
from experiments.common import choose_base_learner, load_cell, nested_fit

KS = [0, 1, 2, 3, 5]
ORDERS = ["reported", "design", "random"]
N_RANDOM = 20
ALPHA = 0.1
MIN_N = 11


def evaluate(target, setting, Xtr, ytr, gtr, Xte, yte, gte, learner, params, cfg, seed, fold, keep_runs=False):
    nf = nested_fit(learner, params, Xtr, ytr, gtr, Xte, inner_k=cfg["inner_folds"], seed=seed * 100 + fold, n_jobs=1, alphas=[ALPHA])
    lam = nf["vc"]["lam"]; f_cal = ytr - nf["res_sc"]; f_te = nf["pred"]
    Tc, tc = Xtr["T_C"].to_numpy(), Xtr["log_t_min"].to_numpy(); Tt, tt = Xte["T_C"].to_numpy(), Xte["log_t_min"].to_numpy()
    rows, runs = [], []
    for order in ORDERS:
        draws = range(N_RANDOM) if order == "random" else [0]
        for k in KS:
            for d in draws:
                rng_c = np.random.default_rng(1000 + d); rng_t = np.random.default_rng(2000 + d)
                cal = simulate(ytr, f_cal, gtr, Tc, tc, k, lam, order, min_n=QPOS + 1, rng=rng_c)
                te = simulate(yte, f_te, gte, Tt, tt, k, lam, order, min_n=MIN_N, rng=rng_t)
                if te.empty:
                    continue
                q = quantiles(cal, ALPHA)
                for r in per_study_metrics(te, q):
                    rows.append(dict(target=target, setting=setting, seed=seed, fold=fold, order=order, k=k, draw=d, lam=lam, **r))
                if keep_runs and order == "design":
                    tmp = te.copy(); tmp["k"] = k
                    for m in ["A", "B", "C"]:
                        tmp[f"q_{m}"] = q[m]
                    runs.append(tmp)
    return rows, runs


def load_external(dev):
    from experiments.e5_generalization import load_4tu, overlap_audit
    from src.data.load import read_raw
    Xe, ye, ge, _ = load_4tu(dev)
    dup = overlap_audit(Xe, ye, read_raw())
    return Xe[~dup].reset_index(drop=True), ye[~dup], ge[~dup]


def run(mode="full", settings=("dev", "locked", "external")):
    cfg, D = load_config(mode), out_dirs(mode); log = get_logger("e15_deployment", D["logs"])
    learner, _ = choose_base_learner(D)
    for setting in settings:
        rows, runs = [], []
        for target in (["solid"] if setting == "external" else ["biooil", "solid"]):
            dev = load_target(target, "dev")
            fs = "base" if setting == "external" else "base+P"
            cols = dev.base_features + (dev.protocol_features if fs == "base+P" else [])
            params = load_cell(D, target, fs, learner)["params"]
            if setting == "dev":
                X = dev.X[cols]
                jobs = [(s, fi, tr, te) for s in cfg["outer_seeds"] for fi, (tr, te) in enumerate(grouped_folds(dev.groups, k=cfg["outer_folds"], seed=s))]
                out = Parallel(n_jobs=cfg["n_jobs"])(delayed(evaluate)(target, setting, X.iloc[tr], dev.y[tr], dev.groups[tr], X.iloc[te], dev.y[te],
                                                                       dev.groups[te], learner, params, cfg, s, fi) for s, fi, tr, te in jobs)
            elif setting == "locked":
                te_ds = load_target(target, "test")
                out = [evaluate(target, setting, dev.X[cols], dev.y, dev.groups, te_ds.X[cols], te_ds.y, te_ds.groups, learner, params, cfg, 0, 0, keep_runs=True)]
            else:
                Xe, ye, ge = load_external(dev)
                out = [evaluate(target, setting, dev.X[cols], dev.y, dev.groups, Xe[cols], ye, ge, learner, params, cfg, 0, 0)]
            for r, ru in out:
                rows.extend(r)
                for x in ru:
                    x["target"] = target; runs.append(x)
            log.info(f"E15 {setting} {target} done")
        pd.DataFrame(rows).to_csv(os.path.join(D["results"], f"e15_deploy_{setting}.csv"), index=False)
        if runs:
            pd.concat(runs).to_csv(os.path.join(D["pred"], "e15_locked_design_runs.csv.gz"), index=False)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    settings = sys.argv[2].split(",") if len(sys.argv) > 2 else ("dev", "locked", "external")
    run(mode, settings)
