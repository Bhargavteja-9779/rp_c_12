"""E3: STRATA on development studies (RQ2-RQ5): outer study-grouped CV with nested calibration.

Outputs (per target × feature set):
  results/predictions/e3_{target}__{fs}.csv.gz  — outer-test predictions, RC/SC half-widths per alpha
  results/e3_kshot_{target}__{fs}.csv           — k-shot per study/k/mode (averaged over draws, per seed)
  results/e3_varcomp_{target}__{fs}.csv         — inner variance components per outer fold
"""
from __future__ import annotations

import os, sys, json
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data.load import load_target
from src.evaluation.core import grouped_folds
from src.utils import out_dirs, load_config, get_logger, dump
from experiments.common import choose_base_learner, load_cell, nested_fit, kshot_eval


def run(mode="full"):
    cfg, D = load_config(mode), out_dirs(mode)
    log = get_logger("e3_strata", D["logs"])
    learner, v = choose_base_learner(D)
    dump(dict(learner=learner, grouped_cv_rmse_biooil_base=v, rule="PROTOCOL §6"), os.path.join(D["results"], "strata_base_learner.json"))
    log.info(f"STRATA base learner = {learner} (grouped RMSE {v:.3f})")
    kmax = max(cfg["k_values"])
    for target in ["biooil", "solid"]:
        ds = load_target(target, "dev")
        for fs in ["base", "base+P"]:
            tag = f"{target}__{fs}"
            fpred = os.path.join(D["pred"], f"e3_{tag}.csv.gz")
            if os.path.exists(fpred):
                log.info(f"cached {tag}"); continue
            params = load_cell(D, target, fs, learner)["params"]
            cols = ds.base_features + (ds.protocol_features if fs == "base+P" else [])
            X = ds.X[cols]
            P, K, V = [], [], []
            for seed in cfg["outer_seeds"]:
                for fi, (tr, te) in enumerate(grouped_folds(ds.groups, k=cfg["outer_folds"], seed=seed)):
                    nf = nested_fit(learner, params, X.iloc[tr], ds.y[tr], ds.groups[tr], X.iloc[te],
                                    inner_k=cfg["inner_folds"], seed=seed * 100 + fi, n_jobs=cfg["n_jobs"], alphas=cfg["alphas"])
                    row = pd.DataFrame({"idx": te, "y": ds.y[te], "pred": nf["pred"], "study": ds.groups[te], "seed": seed, "fold": fi})
                    for a in cfg["alphas"]:
                        row[f"qRC_{a}"] = nf["q"][a]["RC"]; row[f"qSC_{a}"] = nf["q"][a]["SC"]
                    P.append(row)
                    V.append(dict(seed=seed, fold=fi, **nf["vc"]))
                    ks = kshot_eval(ds.y[te], nf["pred"], ds.groups[te], nf, cfg["k_values"], cfg["alpha"], cfg["kshot_draws"],
                                    min_n=kmax + 1)
                    K.extend([dict(seed=seed, fold=fi, **r) for r in ks])
                log.info(f"{tag} seed {seed} done")
            pd.concat(P).to_csv(fpred, index=False)
            pd.DataFrame(K).to_csv(os.path.join(D["results"], f"e3_kshot_{tag}.csv"), index=False)
            pd.DataFrame(V).to_csv(os.path.join(D["results"], f"e3_varcomp_{tag}.csv"), index=False)


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "full")
