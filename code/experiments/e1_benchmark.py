"""E1 + E2: main evaluation and baseline comparison (RQ1, RQ3-across-learners).

For every target × feature set × learner: equal-budget tuning (grouped CV on development studies),
then out-of-fold predictions under (a) random row 5-fold CV and (b) study-grouped 10-fold CV × 3 seeds.
Each cell is cached in results/experiment_logs/e1_cells/ so interrupted runs resume.
"""
from __future__ import annotations

import os, sys, json, traceback
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data.load import load_target
from src.evaluation.core import grouped_folds, random_folds, oof_predict, tune, summary, restore
from src.models.registry import available
from src.utils import out_dirs, load_config, get_logger, dump, Timer

FEATURE_SETS = ["base", "base+P"]


def cols_for(ds, fs):
    return ds.base_features + (ds.protocol_features if fs == "base+P" else [])


def run(mode="full"):
    cfg, D = load_config(mode), out_dirs(mode)
    log = get_logger("e1_benchmark", D["logs"])
    cell_dir = os.path.join(D["logs"], "e1_cells"); os.makedirs(cell_dir, exist_ok=True)
    rows = []
    for target in ["biooil", "solid"]:
        ds = load_target(target, "dev")
        dump(ds.exclusions, os.path.join(D["results"], f"exclusions_{target}_dev.json"))
        for fs in FEATURE_SETS:
            X = ds.X[cols_for(ds, fs)]
            for name in cfg["learners"]:
                cell = os.path.join(cell_dir, f"{target}__{fs}__{name}.json")
                if os.path.exists(cell):
                    rows.extend(json.load(open(cell))["rows"]); continue
                if not available(name):
                    log.info(f"SKIP {name}: package not installed"); continue
                try:
                    tlog = []
                    with Timer() as tt:
                        params, tscore = tune(name, X, ds.y, ds.groups, n_iter=cfg["tune_iter"], k=cfg["tune_folds"],
                                              seed=0, n_jobs=cfg["n_jobs"], log=tlog)
                    params = restore(params)
                    preds = pd.DataFrame({"y": ds.y, "study": ds.groups})
                    cell_rows = []
                    rf = random_folds(len(ds.y), k=cfg["random_folds"], seed=cfg["random_seed"])
                    p, ft, pt = oof_predict(name, params, X, ds.y, ds.groups, rf, n_jobs=cfg["n_jobs"])
                    preds["random"] = p
                    cell_rows.append(dict(target=target, features=fs, learner=name, scheme="random_row_cv", seed=cfg["random_seed"],
                                          fit_s=ft, predict_s=pt, **summary(ds.y, p, ds.groups)))
                    for s in cfg["outer_seeds"]:
                        gf = grouped_folds(ds.groups, k=cfg["outer_folds"], seed=s)
                        p, ft, pt = oof_predict(name, params, X, ds.y, ds.groups, gf, n_jobs=cfg["n_jobs"])
                        preds[f"grouped_{s}"] = p
                        cell_rows.append(dict(target=target, features=fs, learner=name, scheme="grouped_study_cv", seed=s,
                                              fit_s=ft, predict_s=pt, **summary(ds.y, p, ds.groups)))
                    preds.to_csv(os.path.join(D["pred"], f"e1_{target}__{fs}__{name}.csv.gz"), index=False)
                    dump(dict(rows=cell_rows, params=params, tune_rmse=tscore, tune_seconds=tt.s, tune_log=tlog), cell)
                    rows.extend(cell_rows)
                    g = np.mean([r["rmse"] for r in cell_rows if r["scheme"] == "grouped_study_cv"])
                    log.info(f"{target:6s} {fs:6s} {name:8s} random RMSE={cell_rows[0]['rmse']:.2f} grouped RMSE={g:.2f} tune {tt.s:.0f}s")
                except Exception as e:
                    log.error(f"FAIL {target} {fs} {name}: {e}\n{traceback.format_exc()}")
                    dump(dict(rows=[], error=str(e)), cell + ".failed")
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(D["results"], "e1_benchmark.csv"), index=False)
    return df


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "full")
