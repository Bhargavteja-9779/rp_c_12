"""Splitting, metrics, tuning and out-of-fold evaluation (PROTOCOL §6, §9)."""
from __future__ import annotations

import time
import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from sklearn.model_selection import GroupKFold, KFold, ParameterSampler

from src.models.registry import Learner, search_space


# ------------------------------------------------------------------ splits
def random_folds(n, k=5, seed=11):
    return list(KFold(n_splits=k, shuffle=True, random_state=seed).split(np.arange(n)))


def grouped_folds(groups, k=10, seed=11):
    """Study-level folds: every study appears in exactly one test fold (shuffled GroupKFold)."""
    return list(GroupKFold(n_splits=k, shuffle=True, random_state=seed).split(np.zeros(len(groups)), groups=groups))


# ------------------------------------------------------------------ metrics
def rmse(y, p):
    y, p = np.asarray(y), np.asarray(p)
    return float(np.sqrt(np.mean((y - p) ** 2)))


def r2(y, p):
    y, p = np.asarray(y), np.asarray(p)
    return float(1 - np.sum((y - p) ** 2) / np.sum((y - np.mean(y)) ** 2))


def per_study(y, p, groups) -> pd.DataFrame:
    d = pd.DataFrame({"y": y, "p": p, "g": groups})
    out = d.groupby("g").apply(lambda t: pd.Series({"n": len(t), "rmse": rmse(t.y, t.p), "mae": float(np.mean(np.abs(t.y - t.p))),
                                                   "bias": float(np.mean(t.y - t.p))}), include_groups=False)
    return out.reset_index().rename(columns={"g": "study"})


def summary(y, p, groups) -> dict:
    ps = per_study(y, p, groups)
    return dict(n=int(len(y)), n_studies=int(len(ps)), rmse=rmse(y, p), mae=float(np.mean(np.abs(np.asarray(y) - p))),
                r2=r2(y, p), median_study_rmse=float(ps["rmse"].median()), mean_study_rmse=float(ps["rmse"].mean()))


# ------------------------------------------------------------------ fitting helpers
def _fit_predict(name, params, seed, Xtr, ytr, gtr, Xte):
    t0 = time.perf_counter()
    m = Learner(name, params, seed=seed, n_jobs=1).fit(Xtr, ytr, gtr)
    t1 = time.perf_counter()
    p = m.predict(Xte)
    return p, t1 - t0, time.perf_counter() - t1


def oof_predict(name, params, X, y, groups, folds, seed=0, n_jobs=4):
    """Out-of-fold predictions for a fixed configuration; returns (pred, fit_seconds, predict_seconds)."""
    res = Parallel(n_jobs=n_jobs)(delayed(_fit_predict)(name, params, seed, X.iloc[tr], y[tr], groups[tr], X.iloc[te])
                                  for tr, te in folds)
    pred = np.full(len(y), np.nan)
    for (tr, te), (p, _, _) in zip(folds, res):
        pred[te] = p
    return pred, float(sum(r[1] for r in res)), float(sum(r[2] for r in res))


def tune(name, X, y, groups, n_iter=20, k=5, seed=0, n_jobs=4, log=None):
    """Equal-budget random search scored by grouped k-fold RMSE on the development set."""
    space = search_space(name)
    cands = [{}] if not space else list(ParameterSampler(space, n_iter=n_iter, random_state=seed))
    folds = grouped_folds(groups, k=k, seed=seed + 1000)
    jobs = [(i, tr, te) for i in range(len(cands)) for tr, te in folds]
    res = Parallel(n_jobs=n_jobs)(delayed(_fit_predict)(name, cands[i], 0, X.iloc[tr], y[tr], groups[tr], X.iloc[te]) for i, tr, te in jobs)
    preds = [np.full(len(y), np.nan) for _ in cands]
    for (i, tr, te), (p, _, _) in zip(jobs, res):
        preds[i][te] = p
    scores = [rmse(y, p) for p in preds]
    best = int(np.argmin(scores))
    if log is not None:
        for c, s in zip(cands, scores):
            log.append({"learner": name, "params": _jsonable(c), "grouped_cv_rmse": s})
    return _jsonable(cands[best]), float(scores[best])


def _jsonable(d):
    out = {}
    for k, v in d.items():
        if isinstance(v, (np.integer,)):
            v = int(v)
        elif isinstance(v, (np.floating,)):
            v = float(v)
        elif isinstance(v, tuple):
            v = list(v)
        out[k] = v
    return out


def restore(params):
    """Inverse of _jsonable for tuple-valued hyper-parameters."""
    p = dict(params)
    if "hidden_layer_sizes" in p:
        p["hidden_layer_sizes"] = tuple(p["hidden_layer_sizes"])
    return p
