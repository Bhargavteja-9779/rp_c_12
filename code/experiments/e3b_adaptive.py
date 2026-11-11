"""E3b (Phase-19 improvement, post hoc — logged in PROTOCOL §12): locally adaptive study-calibrated conformal (SC-N).

Hypothesis: out-of-study error is heteroscedastic, so normalising conformity scores by a learned difficulty
sigma(x) narrows intervals for easy regimes while retaining study-level coverage.
Procedure per outer study-fold (training studies only):
  1. inner study-grouped OOF residuals r (as in E3);
  2. difficulty model g: shallow gradient boosting on log(|r| + 0.5), cross-fitted by study (grouped 5-fold) so
     that every calibration score uses a g that did not see that study; final g fitted on all training studies;
  3. scores s = |r| / sigma_oof, study-weighted conformal quantile q;  interval = f(x) ± q * sigma(x).
Compared with SC (constant width) and RC on: coverage (rows/studies), mean width, interval (Winkler) score and
coverage by process subtype (conditional coverage).
"""
from __future__ import annotations

import os, sys
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data.load import load_target
from src.evaluation.core import grouped_folds
from src.models.strata import study_quantile, weighted_conformal_quantile
from src.utils import out_dirs, load_config, get_logger
from experiments.common import choose_base_learner, load_cell, nested_fit

EPS = 0.5


def difficulty_model(seed=0):
    return HistGradientBoostingRegressor(max_depth=3, max_iter=200, learning_rate=0.05, min_samples_leaf=40, random_state=seed)


def fit_sigma(X, r, groups, seed=0):
    """Cross-fitted sigma for calibration rows + a final model for new rows."""
    z = np.log(np.abs(r) + EPS)
    oof = np.empty(len(r))
    for tr, te in grouped_folds(groups, k=5, seed=seed + 900):
        oof[te] = difficulty_model(seed).fit(X.iloc[tr], z[tr]).predict(X.iloc[te])
    final = difficulty_model(seed).fit(X, z)
    return np.exp(oof), final


def winkler(y, lo, hi, alpha):
    w = hi - lo
    return w + (2 / alpha) * (lo - y) * (y < lo) + (2 / alpha) * (y - hi) * (y > hi)


def run(mode="full"):
    cfg, D = load_config(mode), out_dirs(mode)
    log = get_logger("e3b_adaptive", D["logs"])
    learner, _ = choose_base_learner(D)
    a = cfg["alpha"]; rows = []
    for target in ["biooil", "solid"]:
        ds = load_target(target, "dev")
        fs = "base+P"
        X = ds.X[ds.base_features + ds.protocol_features]
        params = load_cell(D, target, fs, learner)["params"]
        for seed in cfg["outer_seeds"]:
            for fi, (tr, te) in enumerate(grouped_folds(ds.groups, k=cfg["outer_folds"], seed=seed)):
                nf = nested_fit(learner, params, X.iloc[tr], ds.y[tr], ds.groups[tr], X.iloc[te], inner_k=cfg["inner_folds"],
                                seed=seed * 100 + fi, n_jobs=cfg["n_jobs"], alphas=[a])
                sig_cal, g = fit_sigma(X.iloc[tr], nf["res_sc"], ds.groups[tr], seed=fi)
                s = np.abs(nf["res_sc"]) / sig_cal
                gser = pd.Series(ds.groups[tr]); w = 1 / gser.map(gser.value_counts()).to_numpy(float)
                qn = weighted_conformal_quantile(s, w, a)
                sig_te = np.exp(g.predict(X.iloc[te]))
                yte, p = ds.y[te], nf["pred"]
                for method, half in [("RC", np.full(len(te), nf["q"][a]["RC"])), ("SC", np.full(len(te), nf["q"][a]["SC"])), ("SC-N", qn * sig_te)]:
                    lo, hi = p - half, p + half
                    rows.append(pd.DataFrame(dict(target=target, seed=seed, fold=fi, method=method, y=yte, lo=lo, hi=hi, study=ds.groups[te],
                                                  process=ds.meta["process"].to_numpy()[te], hit=((yte >= lo) & (yte <= hi)).astype(float),
                                                  width=hi - lo, winkler=winkler(yte, lo, hi, a))))
            log.info(f"{target} seed {seed} done")
    df = pd.concat(rows)
    df.to_csv(os.path.join(D["pred"], "e3b_adaptive_intervals.csv.gz"), index=False)
    summ = []
    for (t, m), g in df.groupby(["target", "method"]):
        w = 1 / g.groupby(["seed", "study"])["hit"].transform("count")
        per_proc = g.groupby("process").apply(lambda q: float((q["hit"] / q.groupby(["seed", "study"])["hit"].transform("count")).sum() /
                                                               (1 / q.groupby(["seed", "study"])["hit"].transform("count")).sum()), include_groups=False)
        summ.append(dict(target=t, method=m, coverage_rows=float(g["hit"].mean()), coverage_studies=float((w * g["hit"]).sum() / w.sum()),
                         mean_width=float(g["width"].mean()), median_width=float(g["width"].median()), winkler=float(g["winkler"].mean()),
                         coverage_by_process=per_proc.round(3).to_dict(), max_abs_process_dev=float((per_proc - (1 - a)).abs().max())))
    pd.DataFrame(summ).to_csv(os.path.join(D["results"], "e3b_adaptive_summary.csv"), index=False)
    print(pd.DataFrame(summ).drop(columns=["coverage_by_process"]).round(3).to_string())


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "full")
