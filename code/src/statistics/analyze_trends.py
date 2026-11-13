"""Statistics for E12 (PROTOCOL Addendum A, hypotheses T1–T5). Unit of analysis = study.

Writes results/statistics_trends_{split}.json and tables/table_trends_*_{split}.csv.
"""
from __future__ import annotations

import json, os, sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.statistics.stats import paired_comparison, holm
from src.utils import out_dirs, dump


def run(mode="full", split="dev"):
    D = out_dirs(mode)
    m = pd.read_csv(os.path.join(D["results"], f"e12_study_metrics_{split}.csv"))
    a = pd.read_csv(os.path.join(D["results"], f"e12_anchor_{split}.csv"))
    out = {"split": split}
    # ---------- T1: contrast R² vs level R² (pooled over studies, per seed then averaged)
    t1 = []
    for (t, ln, mod), g in m.groupby(["target", "learner", "model"]):
        r2c = g.groupby("seed").apply(lambda q: 1 - q.sse_contrast.sum() / q.ss_contrast.sum(), include_groups=False).mean()
        row = dict(target=t, learner=ln, model=mod, contrast_r2=float(r2c), n_studies=int(g.study.nunique()),
                   n_pairs=int(g.groupby("seed").n_pairs.sum().mean()),
                   median_study_contrast_rmse=float(g.groupby("study").rmse_contrast.mean().median()))
        if mod == "A":
            row["level_r2_same_studies"] = float(g.groupby("seed").apply(lambda q: 1 - q.sse_level.sum() / q.ss_level_about_mean.sum(), include_groups=False).mean())
            row["level_rmse_same_studies"] = float(np.sqrt(g.groupby("seed").apply(lambda q: q.sse_level.sum() / q.n_runs.sum(), include_groups=False).mean()))
        rk = g.dropna(subset=["spearman"])
        if len(rk):
            ps = rk.groupby("study")[["spearman", "regret", "regret_random", "range_y"]].mean()
            row.update(median_spearman=float(ps.spearman.median()), frac_spearman_gt_0_5=float((ps.spearman > 0.5).mean()),
                       median_regret=float(ps.regret.median()), median_regret_random=float(ps.regret_random.median()),
                       median_rel_regret=float((ps.regret / ps.range_y.replace(0, np.nan)).median()), n_rank_studies=int(len(ps)))
            tr = paired_comparison(ps.regret.values, ps.regret_random.values, alternative="less")
            row.update(regret_vs_random_p=tr["p"], regret_vs_random_median_diff=tr["median_diff"])
        if "contrast_cov" in g and g.contrast_cov.notna().any():
            c = g.dropna(subset=["contrast_cov"])
            row.update(contrast_coverage_studies=float(c.groupby("seed").contrast_cov.mean().mean()),
                       contrast_width=float(c.contrast_width.mean()), level_width=float(c.level_width.mean()))
        t1.append(row)
    T1 = pd.DataFrame(t1)
    out["T1_T4_T5_summary"] = T1.to_dict("records")
    # ---------- T2: W / PD vs A per-study contrast RMSE (seed-averaged), one-sided, Holm over all comparisons
    ps = m.groupby(["target", "learner", "model", "study"]).rmse_contrast.mean().unstack("model")
    t2 = []
    for (t, ln), g in ps.groupby(level=[0, 1]):
        for alt in ["W", "PD"]:
            q = g[["A", alt]].dropna()
            t2.append(dict(target=t, learner=ln, comparison=f"{alt}_vs_A", **paired_comparison(q[alt].values, q["A"].values, alternative="less"),
                           median_A=float(q["A"].median()), median_alt=float(q[alt].median())))
    for r, p in zip(t2, holm([r["p"] for r in t2])):
        r["p_holm"] = float(p)
    out["T2"] = t2
    # ---------- T3: anchored prediction vs A-EB (two-sided, Holm)
    pa = a.groupby(["target", "learner", "k", "method", "study"]).rmse.mean().unstack("method")
    t3, summ = [], []
    for (t, ln, k), g in pa.groupby(level=[0, 1, 2]):
        summ.append(dict(target=t, learner=ln, k=int(k), **{f"median_{c}": float(g[c].median()) for c in g.columns}, n_studies=int(len(g))))
        for alt in ["W-anchor", "PD-anchor"]:
            q = g[["A-EB", alt]].dropna()
            t3.append(dict(target=t, learner=ln, k=int(k), comparison=f"{alt}_vs_A-EB", **paired_comparison(q[alt].values, q["A-EB"].values)))
    for r, p in zip(t3, holm([r["p"] for r in t3])):
        r["p_holm"] = float(p)
    out["T3"] = t3; out["T3_summary"] = summ
    dump(out, os.path.join(D["results"], f"statistics_trends_{split}.json"))
    T1.to_csv(os.path.join(D["tables"], f"table_trends_summary_{split}.csv"), index=False)
    pd.DataFrame(t2).to_csv(os.path.join(D["tables"], f"table_trends_T2_{split}.csv"), index=False)
    pd.DataFrame(summ).to_csv(os.path.join(D["tables"], f"table_trends_anchor_{split}.csv"), index=False)
    pd.DataFrame(t3).to_csv(os.path.join(D["tables"], f"table_trends_T3_{split}.csv"), index=False)
    return out


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "full", sys.argv[2] if len(sys.argv) > 2 else "dev")
