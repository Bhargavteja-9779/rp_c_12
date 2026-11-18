"""Simulated deployment in a new laboratory (PROTOCOL Addendum D, E15).

For a study, the first k runs under an ordering rule are 'measured' (support); the query set is fixed as the runs after
position QPOS (= 5) so that all k are evaluated on the same runs and support never enters the query.
Strategies:
    A  literature model, no adaptation
    B  STRATA: literature model + empirical-Bayes offset  k/(k+lam) * mean(y_s - f_s)
    C  local only: mean of the k support yields
Conformal half-widths are obtained by replaying the identical procedure (same rule, same k) on calibration studies.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from src.models.strata import weighted_conformal_quantile

QPOS = 5


def order_study(T, logt, rule, rng=None):
    """Return a permutation (local positions) of a study's runs."""
    n = len(T); idx = np.arange(n)
    if rule == "reported":
        return idx
    if rule == "random":
        return rng.permutation(n)
    if rule != "design":
        raise ValueError(rule)
    Tf = np.where(np.isfinite(T), T, np.nanmedian(T) if np.isfinite(T).any() else 0.0)
    tf = np.where(np.isfinite(logt), logt, np.nanmedian(logt) if np.isfinite(logt).any() else 0.0)
    rngT = (Tf.max() - Tf.min()) or 1.0; rngt = (tf.max() - tf.min()) or 1.0
    Z = np.c_[(Tf - Tf.min()) / rngT, (tf - tf.min()) / rngt]
    chosen = [int(np.argmin(np.abs(Tf - np.median(Tf))))]          # centre point
    for cand in (int(np.argmin(Tf)), int(np.argmax(Tf))):           # extremes of the temperature range
        if cand not in chosen and len(chosen) < n:
            chosen.append(cand)
    while len(chosen) < n:                                          # maximin space filling
        rest = [i for i in idx if i not in chosen]
        d = np.min(np.linalg.norm(Z[rest][:, None, :] - Z[chosen][None, :, :], axis=2), axis=1)
        chosen.append(int(rest[int(np.argmax(d))]))
    return np.array(chosen)


def simulate(y, f, groups, T, logt, k, lam, rule, min_n, rng=None):
    """Apply strategies A/B/C to every study with >= min_n runs. Returns a DataFrame of query rows."""
    y, f, g = np.asarray(y, float), np.asarray(f, float), np.asarray(groups)
    out = []
    for s in pd.unique(g):
        loc = np.flatnonzero(g == s)
        if len(loc) < min_n or len(loc) <= QPOS:
            continue
        o = loc[order_study(np.asarray(T)[loc], np.asarray(logt)[loc], rule, rng)]
        sup, qry = o[:k], o[QPOS:]
        off = (k / (k + lam) if (k > 0 and np.isfinite(lam)) else 0.0) * (np.mean(y[sup] - f[sup]) if k > 0 else 0.0)
        pc = np.mean(y[sup]) if k > 0 else np.nan
        out.append(pd.DataFrame({"study": s, "y": y[qry], "A": f[qry], "B": f[qry] + off, "C": pc, "pos": np.arange(QPOS, len(o))}))
    return pd.concat(out, ignore_index=True) if out else pd.DataFrame(columns=["study", "y", "A", "B", "C", "pos"])


def quantiles(cal_df, alpha):
    """Study-weighted conformal half-widths for A, B, C from a simulated calibration DataFrame."""
    w = 1.0 / cal_df["study"].map(cal_df["study"].value_counts()).to_numpy(float)
    q = {}
    for m in ["A", "B", "C"]:
        r = np.abs(cal_df["y"].to_numpy() - cal_df[m].to_numpy())
        ok = np.isfinite(r)
        q[m] = weighted_conformal_quantile(r[ok], w[ok], alpha) if ok.any() else np.nan
    return q


def per_study_metrics(df, q):
    rows = []
    for s, t in df.groupby("study"):
        for m in ["A", "B", "C"]:
            e = t["y"] - t[m]
            if not np.isfinite(e).all():
                continue
            rows.append(dict(study=s, strategy=m, n_query=len(t), rmse=float(np.sqrt(np.mean(e ** 2))), mae=float(np.mean(np.abs(e))),
                             coverage=float(np.mean(np.abs(e) <= q[m])), width=float(2 * q[m])))
    return rows
