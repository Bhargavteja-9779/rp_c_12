"""E17 (PROTOCOL Addendum D): laboratory case study on locked studies selected by a pre-specified rule.

Rule: among locked studies with >= 11 runs, the one with the most distinct temperatures (ties -> most runs), per target.
A new laboratory measures runs one at a time in the screening-design order. After each measurement (k = 0..n-1) the
remaining, unmeasured runs are predicted by A (literature), B (STRATA) and C (local mean); intervals are calibrated as in
E15 (identical procedure on the development calibration studies, with the remaining-runs query definition).
Outputs: results/e17_case_study.csv (per step), results/predictions/e17_case_runs.csv.gz, results/statistics/e17_selection.json
"""
from __future__ import annotations

import os, sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data.load import load_target
from src.models.deploy import order_study
from src.models.strata import weighted_conformal_quantile
from src.utils import out_dirs, load_config, dump
from experiments.common import choose_base_learner, load_cell, nested_fit

ALPHA = 0.1


def stepwise(y, f, T, logt, k, lam):
    """Measured = first k runs in design order; predictions for the remaining runs."""
    o = order_study(T, logt, "design"); sup, rest = o[:k], o[k:]
    off = (k / (k + lam) if (k > 0 and np.isfinite(lam)) else 0.0) * (np.mean(y[sup] - f[sup]) if k else 0.0)
    return o, sup, rest, f[rest], f[rest] + off, (np.full(len(rest), np.mean(y[sup])) if k else np.full(len(rest), np.nan))


def calib_quantiles(y, f, g, T, t, k, lam):
    res = {"A": [], "B": [], "C": []}; wts = []
    for s in pd.unique(g):
        loc = np.flatnonzero(g == s)
        if len(loc) <= k:
            continue
        _, _, rest, pa, pb, pc = stepwise(y[loc], f[loc], T[loc], t[loc], k, lam)
        yr = y[loc][rest]
        res["A"].append(np.abs(yr - pa)); res["B"].append(np.abs(yr - pb)); res["C"].append(np.abs(yr - pc)); wts.append(np.full(len(rest), 1 / len(rest)))
    w = np.concatenate(wts)
    out = {}
    for m in res:
        r = np.concatenate(res[m]); ok = np.isfinite(r)
        out[m] = weighted_conformal_quantile(r[ok], w[ok], ALPHA) if ok.any() else np.nan
    return out


def run(mode="full"):
    cfg, D = load_config(mode), out_dirs(mode); learner, _ = choose_base_learner(D)
    steps, runs, sel = [], [], {}
    for t in ["biooil", "solid"]:
        dev, te = load_target(t, "dev"), load_target(t, "test")
        cols = dev.base_features + dev.protocol_features
        cand = pd.DataFrame({"study": te.groups, "T": te.X["T_C"].to_numpy()}).groupby("study").agg(n=("T", "size"), nT=("T", "nunique"))
        cand = cand[cand.n >= 11].sort_values(["nT", "n"], ascending=False)
        s = cand.index[0]
        m = te.groups == s
        meta = te.meta[m].iloc[0]
        sel[t] = dict(study=s, n_runs=int(cand.loc[s, "n"]), n_temperatures=int(cand.loc[s, "nT"]), family=str(meta["family"]), process=str(meta["process"]),
                      feedstock=str(meta["feedstock"]), medium=str(meta["medium"]), n_candidates=int(len(cand)))
        nf = nested_fit(learner, load_cell(D, t, "base+P", learner)["params"], dev.X[cols], dev.y, dev.groups, te.X[cols][m], inner_k=cfg["inner_folds"],
                        seed=7, n_jobs=cfg["n_jobs"], alphas=[ALPHA])
        lam = nf["vc"]["lam"]; f_cal = dev.y - nf["res_sc"]
        y, f = te.y[m], nf["pred"]; T, lt = te.X["T_C"].to_numpy()[m], te.X["log_t_min"].to_numpy()[m]
        Tc, tc = dev.X["T_C"].to_numpy(), dev.X["log_t_min"].to_numpy()
        for k in range(0, len(y)):
            o, sup, rest, pa, pb, pc = stepwise(y, f, T, lt, k, lam)
            q = calib_quantiles(dev.y, f_cal, dev.groups, Tc, tc, k, lam)
            yr = y[rest]
            row = dict(target=t, study=s, k=k, n_remaining=len(rest))
            for name, p in [("A", pa), ("B", pb), ("C", pc)]:
                if np.isfinite(p).all():
                    e = yr - p
                    row.update({f"rmse_{name}": float(np.sqrt(np.mean(e ** 2))), f"cov_{name}": float(np.mean(np.abs(e) <= q[name])), f"halfwidth_{name}": float(q[name]),
                                f"regret_{name}": float(yr.max() - yr[np.argmax(p)]) if name != "C" else np.nan})
            row["regret_random"] = float(yr.max() - yr.mean())
            steps.append(row)
            if k in (0, 1, 3):
                runs.append(pd.DataFrame({"target": t, "study": s, "k": k, "T": T, "logt": lt, "y": y, "measured": np.isin(np.arange(len(y)), sup),
                                          "order_pos": np.argsort(o), "A": f, "B": f + (pb[0] - pa[0] if len(rest) else 0), "C": (pc[0] if len(rest) else np.nan),
                                          "q_A": q["A"], "q_B": q["B"], "q_C": q["C"]}))
    pd.DataFrame(steps).to_csv(os.path.join(D["results"], "e17_case_study.csv"), index=False)
    pd.concat(runs).to_csv(os.path.join(D["pred"], "e17_case_runs.csv.gz"), index=False)
    dump(sel, os.path.join(D["stats"], "e17_selection.json"))
    print(sel); print(pd.DataFrame(steps).round(2).head(30).to_string())


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "full")
