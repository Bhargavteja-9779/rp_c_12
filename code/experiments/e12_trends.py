"""E12 (PROTOCOL Addendum A): do literature-trained models transfer within-study *trends* to unseen studies?

Per outer study-fold (development: grouped 10-fold × seeds 11/22/33; locked: dev → locked once):
  * fit A (absolute), W (within-study), PD (pairwise-difference) on the training studies;
  * contrasts for all within-study pairs of every test study (studies with ≥ 3 runs);
  * levels for A; within-study ranking (Spearman ρ) and regret of picking the predicted-best run (studies with ≥ 5 runs);
  * anchored prediction with k ∈ {1,2,3} measured runs (studies with ≥ 11 runs; 20 random anchor sets), vs STRATA-EB on A;
  * (primary learner only) study-calibrated conformal intervals for contrasts from inner study-grouped 5-fold OOF on training studies.
Outputs: results/e12_study_metrics_{split}.csv, results/e12_anchor_{split}.csv, results/e12_contrast_cov_{split}.csv
"""
from __future__ import annotations

import os, sys, json, time
import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from scipy.stats import spearmanr

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data.load import load_target
from src.evaluation.core import grouped_folds, restore
from src.models.contrast import MODELS, within_pairs, anchored_predictions
from src.models.strata import variance_components, weighted_conformal_quantile, study_quantile, kshot_split, shrink_factor
from src.utils import out_dirs, load_config, get_logger, dump
from experiments.common import choose_base_learner, load_cell

LEARNERS = ["xgb", "et", "lgbm"]
K_ANCHOR = [1, 2, 3]
N_DRAWS = 20
ALPHA = 0.1


def _fit_all(learner, params, X, y, g, which=("A", "W", "PD")):
    return {m: MODELS[m](learner, params, seed=0, n_jobs=1).fit(X, y, g) for m in which}


def _contrast_scores(models, X, y, g):
    """|Δ̂ - Δ| scores and study weights for all within-study pairs of a calibration set."""
    ia, ib = within_pairs(g, min_n=2)
    out = {}
    if len(ia) == 0:
        return out
    dy = y[ia] - y[ib]
    w = 1.0 / pd.Series(g[ia]).map(pd.Series(g[ia]).value_counts()).to_numpy(float)
    for m, mod in models.items():
        mod.prepare(X, g); out[m] = (np.abs(mod.contrast_idx(ia, ib) - dy), w)
    return out


def run_fold(target, learner, params, X, y, g, tr, te, seed, fold, calibrate):
    t0 = time.perf_counter()
    Xtr, ytr, gtr, Xte, yte, gte = X.iloc[tr], y[tr], g[tr], X.iloc[te], y[te], g[te]
    # ---- inner study-grouped OOF on training studies: lambda (A) and, for the primary learner, contrast scores
    inner = grouped_folds(gtr, k=5, seed=seed * 100 + fold + 500)
    res_A = np.empty(len(ytr)); cal = {m: ([], []) for m in ("A", "W", "PD")}
    for itr, ite in inner:
        mods = _fit_all(learner, params, Xtr.iloc[itr], ytr[itr], gtr[itr], which=("A", "W", "PD") if calibrate else ("A",))
        res_A[ite] = ytr[ite] - mods["A"].predict(Xtr.iloc[ite])
        if calibrate:
            sc = _contrast_scores(mods, Xtr.iloc[ite], ytr[ite], gtr[ite])
            for m, (s, w) in sc.items():
                cal[m][0].append(s); cal[m][1].append(w)
    vc = variance_components(res_A, gtr); lam = vc["lam"]
    q_level = study_quantile(res_A, gtr, ALPHA)
    q_contrast = {m: weighted_conformal_quantile(np.concatenate(s), np.concatenate(w), ALPHA) for m, (s, w) in cal.items() if s} if calibrate else {}
    # ---- outer models
    mods = _fit_all(learner, params, Xtr, ytr, gtr)
    for mod in mods.values():
        mod.prepare(Xte, gte)
    predA = mods["A"].predict(Xte)
    rows, arows, crows = [], [], []
    ia, ib = within_pairs(gte, min_n=3)
    dy = yte[ia] - yte[ib]; pst = gte[ia]
    for m, mod in mods.items():
        dc = mod.contrast_idx(ia, ib); err = dc - dy
        df = pd.DataFrame({"s": pst, "e2": err ** 2, "d2": dy ** 2, "hit": (np.abs(err) <= q_contrast.get(m, np.inf)).astype(float)})
        agg = df.groupby("s").agg(n_pairs=("e2", "size"), sse_c=("e2", "sum"), ss_c=("d2", "sum"), cov_c=("hit", "mean"))
        score = mod.score()
        for s, r in agg.iterrows():
            idx = np.flatnonzero(gte == s)
            d = dict(target=target, learner=learner, model=m, seed=seed, fold=fold, study=s, n_runs=len(idx), n_pairs=int(r.n_pairs),
                     sse_contrast=float(r.sse_c), ss_contrast=float(r.ss_c), rmse_contrast=float(np.sqrt(r.sse_c / r.n_pairs)))
            if m == "A":
                d.update(sse_level=float(np.sum((yte[idx] - predA[idx]) ** 2)), ss_level_about_mean=float(np.sum((yte[idx] - yte.mean()) ** 2)))
            if len(idx) >= 5:
                ys, ps = yte[idx], score[idx]
                rho = spearmanr(ps, ys).statistic if np.std(ps) > 0 and np.std(ys) > 0 else np.nan
                d.update(spearman=float(rho), regret=float(ys.max() - ys[np.argmax(ps)]), regret_random=float(ys.max() - ys.mean()),
                         range_y=float(ys.max() - ys.min()))
            if calibrate and m in q_contrast:
                d.update(contrast_cov=float(r.cov_c), contrast_width=2 * q_contrast[m], level_width=2 * q_level)
            rows.append(d)
    # ---- anchored prediction
    keep = pd.Series(gte).map(pd.Series(gte).value_counts()).to_numpy() >= 11
    rA = yte - predA
    for k in K_ANCHOR:
        for dr in range(N_DRAWS):
            rng = np.random.default_rng(20_000 + dr)
            sup, qry = kshot_split(gte, k, rng); qry &= keep; sup &= keep
            if not qry.any():
                continue
            off = pd.Series(np.where(sup, rA, np.nan)).groupby(gte).transform("mean").fillna(0).to_numpy()
            preds = {"A-EB": predA + shrink_factor(k, lam, "eb") * off, "A-raw": predA + off}
            for m in ("W", "PD"):
                preds[f"{m}-anchor"] = anchored_predictions(mods[m], yte, gte, sup, qry)
            for name, p in preds.items():
                e = (yte - p)[qry]
                for s, ee in pd.Series(e).groupby(gte[qry]):
                    arows.append(dict(target=target, learner=learner, seed=seed, fold=fold, k=k, draw=dr, method=name, study=s,
                                      rmse=float(np.sqrt(np.mean(ee ** 2)))))
    return rows, arows, dict(target=target, learner=learner, seed=seed, fold=fold, lam=lam, q_level=q_level,
                             **{f"q_contrast_{m}": q for m, q in q_contrast.items()}, seconds=time.perf_counter() - t0,
                             n_pairs_PD=getattr(mods["PD"], "n_pairs_", None))


def run(mode="full", split="dev"):
    cfg, D = load_config(mode), out_dirs(mode); log = get_logger("e12_trends", D["logs"])
    primary, _ = choose_base_learner(D)
    learners = LEARNERS if mode == "full" else [primary]
    seeds = cfg["outer_seeds"]
    R, A, F = [], [], []
    for target in ["biooil", "solid"]:
        dev = load_target(target, "dev")
        cols = dev.base_features
        for ln in learners:
            params = restore(load_cell(D, target, "base", ln)["params"])
            if split == "dev":
                jobs = [(s, fi, tr, te) for s in seeds for fi, (tr, te) in enumerate(grouped_folds(dev.groups, k=cfg["outer_folds"], seed=s))]
                X, y, g = dev.X[cols], dev.y, dev.groups
            else:  # locked test once: train on all development studies
                te_ds = load_target(target, "test")
                X = pd.concat([dev.X[cols], te_ds.X[cols]], ignore_index=True); y = np.r_[dev.y, te_ds.y]; g = np.r_[dev.groups, te_ds.groups]
                jobs = [(0, 0, np.arange(len(dev.y)), np.arange(len(dev.y), len(y)))]
            out = Parallel(n_jobs=cfg["n_jobs"])(delayed(run_fold)(target, ln, params, X, y, g, tr, te, s, fi, ln == primary)
                                                 for s, fi, tr, te in jobs)
            for r, a, f in out:
                R.extend(r); A.extend(a); F.append(f)
            log.info(f"{split} {target} {ln} done ({sum(f['seconds'] for _, _, f in out):.0f} s fold-time)")
    pd.DataFrame(R).to_csv(os.path.join(D["results"], f"e12_study_metrics_{split}.csv"), index=False)
    A = pd.DataFrame(A).groupby(["target", "learner", "k", "method", "study", "seed"], as_index=False)["rmse"].mean()
    A.to_csv(os.path.join(D["results"], f"e12_anchor_{split}.csv"), index=False)
    pd.DataFrame(F).to_csv(os.path.join(D["results"], f"e12_folds_{split}.csv"), index=False)


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "full", sys.argv[2] if len(sys.argv) > 2 else "dev")
