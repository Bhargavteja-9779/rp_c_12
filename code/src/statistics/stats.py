"""Statistical procedures (PROTOCOL §10). Unit of analysis = source study."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon


def holm(pvals):
    """Holm step-down adjusted p-values (as described in Demšar, 2006)."""
    p = np.asarray(pvals, float); m = len(p); o = np.argsort(p)
    adj = np.empty(m); run = 0.0
    for rank, i in enumerate(o):
        run = max(run, (m - rank) * p[i]); adj[i] = min(1.0, run)
    return adj


def rank_biserial(diff):
    """Matched-pairs rank-biserial correlation (positive = first argument larger)."""
    d = np.asarray(diff, float); d = d[d != 0]
    if len(d) == 0:
        return 0.0
    from scipy.stats import rankdata
    r = rankdata(np.abs(d))
    return float((r[d > 0].sum() - r[d < 0].sum()) / r.sum())


def cluster_bootstrap_ci(values_by_study: pd.DataFrame, stat, n_boot=2000, seed=0, level=0.95):
    """values_by_study: DataFrame with one row per *row* incl. column 'study'; stat(df)->float.
    Resamples studies with replacement."""
    rng = np.random.default_rng(seed)
    studies = values_by_study["study"].unique()
    idx = {s: np.flatnonzero(values_by_study["study"].to_numpy() == s) for s in studies}
    est = []
    for _ in range(n_boot):
        pick = rng.choice(studies, size=len(studies), replace=True)
        rows = np.concatenate([idx[s] for s in pick])
        est.append(stat(values_by_study.iloc[rows]))
    lo, hi = np.nanquantile(est, [(1 - level) / 2, 1 - (1 - level) / 2])
    return float(lo), float(hi)


def paired_bootstrap_median_ci(diff, n_boot=2000, seed=0, level=0.95):
    rng = np.random.default_rng(seed); d = np.asarray(diff, float)
    b = [np.median(rng.choice(d, size=len(d), replace=True)) for _ in range(n_boot)]
    lo, hi = np.quantile(b, [(1 - level) / 2, 1 - (1 - level) / 2])
    return float(lo), float(hi)


def paired_comparison(a, b, alternative="two-sided", seed=0):
    """Compare per-study metrics a vs b (aligned arrays). Returns Wilcoxon statistic, p, effect sizes."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    diff = a - b
    if np.allclose(diff, 0):
        return dict(n=len(diff), W=float("nan"), p=1.0, median_diff=0.0, ci_low=0.0, ci_high=0.0, rank_biserial=0.0)
    W, p = wilcoxon(a, b, alternative=alternative, zero_method="wilcox")
    lo, hi = paired_bootstrap_median_ci(diff, seed=seed)
    return dict(n=int(len(diff)), W=float(W), p=float(p), median_diff=float(np.median(diff)), ci_low=lo, ci_high=hi,
                rank_biserial=rank_biserial(diff), test="Wilcoxon signed-rank", alternative=alternative)
