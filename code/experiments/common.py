"""Shared nested engine for STRATA experiments (E3-E8, locked test).

For a training set (studies S_train) and a test set (S_test):
  1. inner study-grouped OOF residuals on S_train  -> SC quantile, variance components (lambda)
  2. inner random-row OOF residuals on S_train      -> RC quantile
  3. final model on all of S_train                  -> predictions for S_test
No information from S_test enters steps 1-3.
"""
from __future__ import annotations

import json, os, sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.evaluation.core import grouped_folds, random_folds, oof_predict, restore, rmse
from src.models.registry import Learner, NAN_NATIVE
from src.models.strata import (row_quantile, study_quantile, variance_components, kshot_quantile, kshot_split,
                               kshot_adjust, shrink_factor, coverage)


def cells_dir(D):
    return os.path.join(D["logs"], "e1_cells")


def load_cell(D, target, fs, name):
    return json.load(open(os.path.join(cells_dir(D), f"{target}__{fs}__{name}.json")))


def choose_base_learner(D, target="biooil", fs="base"):
    """PROTOCOL §6: lowest mean grouped-CV RMSE on T1 among NaN-native learners (fixed before E3-E5)."""
    best, best_v = None, np.inf
    for n in sorted(NAN_NATIVE):
        f = os.path.join(cells_dir(D), f"{target}__{fs}__{n}.json")
        if not os.path.exists(f):
            continue
        rows = [r for r in json.load(open(f))["rows"] if r["scheme"] == "grouped_study_cv"]
        if not rows:
            continue
        v = float(np.mean([r["rmse"] for r in rows]))
        if v < best_v:
            best, best_v = n, v
    return best, best_v


def nested_fit(name, params, Xtr, ytr, gtr, Xte, inner_k=5, seed=0, n_jobs=4, alphas=(0.1,)):
    params = restore(params)
    gf = grouped_folds(gtr, k=inner_k, seed=seed + 500)
    r_sc_pred, _, _ = oof_predict(name, params, Xtr, ytr, gtr, gf, n_jobs=n_jobs)
    rf = random_folds(len(ytr), k=inner_k, seed=seed + 600)
    r_rc_pred, _, _ = oof_predict(name, params, Xtr, ytr, gtr, rf, n_jobs=n_jobs)
    model = Learner(name, params, seed=0, n_jobs=n_jobs).fit(Xtr, ytr, gtr)
    pred = model.predict(Xte)
    res_sc = ytr - r_sc_pred
    res_rc = ytr - r_rc_pred
    vc = variance_components(res_sc, gtr)
    q = {a: dict(RC=row_quantile(res_rc, a), SC=study_quantile(res_sc, gtr, a)) for a in alphas}
    return dict(pred=pred, res_sc=res_sc, res_rc=res_rc, g_cal=np.asarray(gtr), vc=vc, q=q, model=model)


def kshot_eval(y, pred, groups, nf, k_values, alpha, n_draws, modes=("raw", "eb"), min_n=None, lam_override=None):
    """Evaluate k-shot adaptation on test studies. Returns per-(study, k, mode) rows averaged over draws.
    min_n: only studies with n_j >= min_n are evaluated (common evaluable set across k)."""
    y, pred, groups = np.asarray(y), np.asarray(pred), np.asarray(groups)
    lam = nf["vc"]["lam"] if lam_override is None else lam_override
    r = y - pred
    keep = pd.Series(groups).map(pd.Series(groups).value_counts()).to_numpy() >= (min_n or 1)
    out = []
    for k in k_values:
        for mode in (("none",) if k == 0 else modes):
            qk = kshot_quantile(nf["res_sc"], nf["g_cal"], k, lam, mode, alpha, n_draws=n_draws, seed=0)
            f = shrink_factor(k, lam, mode)
            acc = {}
            for d in range(n_draws if k > 0 else 1):
                rng = np.random.default_rng(10_000 + d)
                sup, qry = kshot_split(groups, k, rng)
                qry &= keep
                off = kshot_adjust(r, groups, sup, f)
                e = (r - off)[qry]; gq = groups[qry]
                for s in np.unique(gq):
                    m = gq == s
                    a = acc.setdefault(s, [[], [], 0])
                    a[0].append(float(np.sqrt(np.mean(e[m] ** 2))))
                    a[1].append(float(np.mean(np.abs(e[m]) <= qk)))
                    a[2] = int(m.sum())
            for s, (rm, cv, n) in acc.items():
                out.append(dict(study=s, k=k, mode=mode, rmse=float(np.mean(rm)), coverage=float(np.mean(cv)),
                                width=2 * qk, n_query=n, lam=lam))
    return out
