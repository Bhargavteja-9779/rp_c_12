"""E9 (review rounds 1/4/8): is STRATA model-agnostic, and does the ML model add anything over the mean?

STRATA (RC vs SC coverage, width, k-shot with k = 0 and 3) is re-run on the development outer study-folds
(seed 11, 10 folds, base + P features) with alternative base learners, including the mean predictor
(intervals = training mean ± study-calibrated quantile) as a 'no-ML' reference. Locked studies are not used.
"""
import os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data.load import load_target
from src.evaluation.core import grouped_folds, rmse
from src.models.strata import coverage
from src.utils import out_dirs, load_config, get_logger
from experiments.common import load_cell, nested_fit, kshot_eval

LEARNERS = ["mean", "ridge", "knn", "rf", "et", "lgbm", "xgb"]


def run(mode="full"):
    cfg, D = load_config(mode), out_dirs(mode); log = get_logger("e9_base_learners", D["logs"])
    a = cfg["alpha"]; rows, krows = [], []
    for t in ["biooil", "solid"]:
        ds = load_target(t, "dev"); X = ds.X[ds.base_features + ds.protocol_features]
        for ln in LEARNERS if mode == "full" else ["mean", "lgbm"]:
            params = load_cell(D, t, "base+P", ln)["params"]
            P = []
            for fi, (tr, te) in enumerate(grouped_folds(ds.groups, k=cfg["outer_folds"], seed=cfg["outer_seeds"][0])):
                nf = nested_fit(ln, params, X.iloc[tr], ds.y[tr], ds.groups[tr], X.iloc[te], inner_k=cfg["inner_folds"], seed=fi, n_jobs=cfg["n_jobs"], alphas=[a])
                P.append(pd.DataFrame(dict(y=ds.y[te], pred=nf["pred"], study=ds.groups[te], qRC=nf["q"][a]["RC"], qSC=nf["q"][a]["SC"])))
                ks = kshot_eval(ds.y[te], nf["pred"], ds.groups[te], nf, [0, 3], a, cfg["kshot_draws"], modes=("eb",), min_n=max(cfg["k_values"]) + 1)
                krows.extend([dict(target=t, learner=ln, fold=fi, **r) for r in ks])
            p = pd.concat(P)
            ps = p.groupby("study").apply(lambda g: float(np.sqrt(np.mean((g.y - g.pred) ** 2))), include_groups=False)
            for cal in ["RC", "SC"]:
                hit = (np.abs(p.y - p.pred) <= p[f"q{cal}"]).astype(float); w = 1 / p.study.map(p.study.value_counts())
                rows.append(dict(target=t, learner=ln, calibration=cal, rmse=rmse(p.y, p.pred), median_study_rmse=float(ps.median()),
                                 coverage_studies=float((w * hit).sum() / w.sum()), width=float(2 * p[f"q{cal}"].mean())))
            log.info(f"{t} {ln} done")
    out = pd.DataFrame(rows); out.to_csv(os.path.join(D["results"], "e9_base_learners.csv"), index=False)
    k = pd.DataFrame(krows).groupby(["target", "learner", "k"]).agg(median_study_rmse=("rmse", "median"), coverage=("coverage", "mean"), width=("width", "mean")).reset_index()
    k.to_csv(os.path.join(D["results"], "e9_base_learners_kshot.csv"), index=False)
    print(out.round(3).to_string()); print(k.round(3).to_string())


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "full")
