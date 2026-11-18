"""E16 (PROTOCOL Addendum D): decision support for a new laboratory.

(a) Applicability domain (AD): study score = median over its runs of the mean Euclidean distance to the 5 nearest
    training runs (base features; training medians imputed; standardised with training mean/SD). Threshold = 95th
    percentile of development out-of-study study scores (outer folds, seed 11). D1: locked studies above the threshold
    have higher per-study RMSE of the unadapted model A (Mann–Whitney, one-sided).
(b) Runs needed: smallest k (screening-design order, development) whose STRATA (B) 90 % half-width <= h, h in {10,15,20}
    wt%; validated by the coverage and RMSE at that k on locked studies.
(c) Rule 'C if flagged else B' vs always-B on locked studies at k = 3 (design order): D2, Wilcoxon two-sided.
"""
from __future__ import annotations

import json, os, sys
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, spearmanr
from sklearn.neighbors import NearestNeighbors

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data.load import load_target
from src.evaluation.core import grouped_folds
from src.statistics.stats import paired_comparison
from src.utils import out_dirs, load_config, dump

K_NN = 5


def ad_scores(Xtr, Xte, gte):
    med = Xtr.median(); A = Xtr.fillna(med); B = Xte.fillna(med)
    mu, sd = A.mean(), A.std(ddof=0).replace(0, 1.0)
    A = ((A - mu) / sd).to_numpy(); B = ((B - mu) / sd).to_numpy()
    d, _ = NearestNeighbors(n_neighbors=K_NN).fit(A).kneighbors(B)
    return pd.Series(d.mean(axis=1)).groupby(np.asarray(gte)).median()


def run(mode="full"):
    cfg, D = load_config(mode), out_dirs(mode); R = D["results"]; out = {}
    e15d = pd.read_csv(os.path.join(R, "e15_deploy_dev.csv")); e15l = pd.read_csv(os.path.join(R, "e15_deploy_locked.csv"))
    for t in ["biooil", "solid"]:
        dev = load_target(t, "dev"); te = load_target(t, "test"); cols = dev.base_features
        # (a) AD threshold from development out-of-study scores
        sc = [ad_scores(dev.X[cols].iloc[tr], dev.X[cols].iloc[ts], dev.groups[ts]) for tr, ts in grouped_folds(dev.groups, k=cfg["outer_folds"], seed=cfg["outer_seeds"][0])]
        sc = pd.concat(sc); thr = float(np.quantile(sc, 0.95))
        dA = e15d[(e15d.target == t) & (e15d.order == "design") & (e15d.k == 0) & (e15d.strategy == "A") & (e15d.seed == cfg["outer_seeds"][0])].set_index("study").rmse
        a, b = sc.align(dA, join="inner")
        rho = spearmanr(a, b)
        lsc = ad_scores(dev.X[cols], te.X[cols], te.groups)
        lA = e15l[(e15l.target == t) & (e15l.order == "design") & (e15l.k == 0) & (e15l.strategy == "A")].set_index("study").rmse
        fl = (lsc > thr)
        x, y = lA[lA.index.isin(fl[fl].index)], lA[lA.index.isin(fl[~fl].index)]
        mw = mannwhitneyu(x, y, alternative="greater") if len(x) and len(y) else None
        out[t] = dict(ad_threshold=thr, dev_spearman_ad_vs_rmse=float(rho.statistic), dev_spearman_p=float(rho.pvalue), dev_n=int(len(a)),
                      locked_n_studies=int(len(lsc)), locked_flagged=int(fl.sum()), locked_flagged_studies=sorted(fl[fl].index.tolist()),
                      locked_eval_studies=int(len(lA)), locked_flagged_eval=int(len(x)),
                      median_rmse_A_flagged=float(x.median()) if len(x) else None, median_rmse_A_unflagged=float(y.median()) if len(y) else None,
                      D1_mannwhitney_p=float(mw.pvalue) if mw else None)
        # exploratory (added after seeing that the pre-registered threshold flagged no locked study): rank association on locked studies
        a2, b2 = lsc.align(lA, join="inner"); r2 = spearmanr(a2, b2)
        out[t].update(locked_exploratory_spearman_ad_vs_rmse=float(r2.statistic), locked_exploratory_spearman_p=float(r2.pvalue),
                      locked_max_score=float(lsc.max()), locked_score_q90=float(np.quantile(lsc, 0.9)))
        # (b) runs needed for a tolerance, from development (design order), validated on locked
        g = e15d[(e15d.target == t) & (e15d.order == "design") & (e15d.strategy == "B")]
        hw = g.groupby("k").width.mean() / 2; med = g.groupby(["k", "study"]).rmse.mean().groupby("k").median()
        gl = e15l[(e15l.target == t) & (e15l.order == "design") & (e15l.strategy == "B")]
        need = []
        for h in [10, 15, 20]:
            ok = hw[hw <= h]
            k = int(ok.index.min()) if len(ok) else None
            row = dict(tolerance_halfwidth=h, k_needed=k, dev_halfwidth=float(hw.loc[k]) if k is not None else None,
                       dev_median_rmse=float(med.loc[k]) if k is not None else None)
            if k is not None:
                q = gl[gl.k == k]
                w = 1 / q.n_query; row.update(locked_coverage=float((q.coverage * q.n_query * w).sum() / (q.n_query * w).sum()),
                                              locked_median_rmse=float(q.rmse.median()), locked_halfwidth=float(q.width.mean() / 2))
            need.append(row)
        out[t]["runs_needed"] = need
        out[t]["dev_halfwidth_by_k"] = {int(k): float(v) for k, v in hw.items()}
        # (c) rule vs always-B on locked, k = 3, design order
        l3 = e15l[(e15l.target == t) & (e15l.order == "design") & (e15l.k == 3)].pivot_table(index="study", columns="strategy", values="rmse")
        rule = np.where(l3.index.isin(fl[fl].index), l3["C"], l3["B"])
        out[t]["D2_rule_vs_B"] = dict(median_rule=float(np.median(rule)), median_B=float(l3["B"].median()), median_C=float(l3["C"].median()),
                                      n_flagged_in_eval=int(l3.index.isin(fl[fl].index).sum()),
                                      **{k_: v for k_, v in paired_comparison(rule, l3["B"].to_numpy()).items() if k_ in ("p", "median_diff", "n")})
    dump(out, os.path.join(D["stats"], "e16_decision.json"))
    print(json.dumps(out, indent=1, default=str)[:4000])


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "full")
