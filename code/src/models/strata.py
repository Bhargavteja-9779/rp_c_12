"""STRATA uncertainty components (PROTOCOL §8).

* Row-calibrated conformal (RC): unweighted split-conformal quantile of absolute residuals obtained by
  *random-row* out-of-fold prediction on the training data (current literature practice).
* Study-calibrated conformal (SC): absolute residuals obtained by *study-grouped* out-of-fold prediction,
  quantile computed with every calibration study given equal total weight (CDF pooling; Dunn et al., 2023).
* k-shot empirical-Bayes adaptation (KS): with k labelled runs of a new study the prediction is shifted by
  the shrunken mean residual  k/(k+lambda) * mean(r_support),  lambda = sigma_w^2 / tau^2, and the interval
  quantile is re-calibrated by simulating exactly this procedure on the calibration studies.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


# ------------------------------------------------------------------ quantiles
def weighted_conformal_quantile(scores, weights, alpha):
    """Smallest s such that the weighted empirical CDF (with a +1 test-point mass of the mean weight
    pushed to +inf, i.e. the usual (1+1/m) finite-sample correction) reaches 1-alpha."""
    s = np.asarray(scores, float); w = np.asarray(weights, float)
    o = np.argsort(s); s, w = s[o], w[o]
    w_test = w.mean() if len(w) else 1.0
    cdf = np.cumsum(w) / (w.sum() + w_test)
    idx = np.searchsorted(cdf, 1 - alpha, side="left")
    return float(s[idx]) if idx < len(s) else float("inf")


def row_quantile(residuals, alpha):
    r = np.abs(residuals)
    return weighted_conformal_quantile(r, np.ones_like(r), alpha)


def study_quantile(residuals, groups, alpha):
    r = np.abs(residuals); g = pd.Series(groups)
    w = 1.0 / g.map(g.value_counts()).to_numpy(float)
    return weighted_conformal_quantile(r, w, alpha)


# ------------------------------------------------------------------ heterogeneity (method of moments)
def variance_components(residuals, groups):
    """One-way random-effects ANOVA (unbalanced) method-of-moments estimates of tau^2 (between-study)
    and sigma_w^2 (within-study) for residuals r_ij = u_j + e_ij."""
    d = pd.DataFrame({"r": np.asarray(residuals, float), "g": np.asarray(groups)})
    n_j = d.groupby("g")["r"].size().to_numpy(float)
    m_j = d.groupby("g")["r"].mean().to_numpy(float)
    N, J = n_j.sum(), len(n_j)
    grand = d["r"].mean()
    ssw = float(((d["r"] - d.groupby("g")["r"].transform("mean")) ** 2).sum())
    ssb = float((n_j * (m_j - grand) ** 2).sum())
    msw = ssw / (N - J)
    msb = ssb / (J - 1)
    n0 = (N - (n_j ** 2).sum() / N) / (J - 1)
    tau2 = max((msb - msw) / n0, 0.0)
    return dict(tau2=tau2, sigma2_w=msw, share_between=tau2 / (tau2 + msw) if tau2 + msw > 0 else 0.0,
                n_studies=J, n=int(N), lam=(msw / tau2) if tau2 > 0 else np.inf)


# ------------------------------------------------------------------ k-shot adaptation
def shrink_factor(k, lam, mode):
    if mode == "none" or k == 0:
        return 0.0
    if mode == "raw":
        return 1.0
    if mode == "eb":
        return 0.0 if not np.isfinite(lam) else k / (k + lam)
    raise ValueError(mode)


def kshot_split(groups, k, rng):
    """For every study with n_j >= k+1 draw a support set of size k; return boolean support mask and
    a mask of evaluable (query) rows.  Studies with n_j <= k are excluded from k-shot evaluation."""
    g = np.asarray(groups)
    support = np.zeros(len(g), bool); query = np.zeros(len(g), bool)
    for s in np.unique(g):
        idx = np.flatnonzero(g == s)
        if len(idx) < k + 1:
            continue
        sup = rng.choice(idx, size=k, replace=False) if k > 0 else np.array([], int)
        support[sup] = True
        query[np.setdiff1d(idx, sup)] = True
    return support, query


def kshot_adjust(residuals, groups, support, factor):
    """Per-study offset = factor * mean residual on the support rows (0 when k = 0)."""
    r = pd.Series(np.where(support, residuals, np.nan)); g = pd.Series(groups)
    off = r.groupby(g).transform("mean").fillna(0.0).to_numpy() * factor
    return off


def kshot_quantile(cal_residuals, cal_groups, k, lam, mode, alpha, n_draws=20, seed=0):
    """Simulate the k-shot procedure on calibration studies; study-weighted conformal quantile of
    |residual - offset| over query rows pooled across draws."""
    f = shrink_factor(k, lam, mode)
    scores, weights = [], []
    for d in range(n_draws if k > 0 else 1):
        rng = np.random.default_rng(seed + d)
        sup, qry = kshot_split(cal_groups, k, rng)
        off = kshot_adjust(cal_residuals, cal_groups, sup, f)
        s = np.abs(cal_residuals - off)[qry]
        g = pd.Series(np.asarray(cal_groups)[qry])
        w = 1.0 / g.map(g.value_counts()).to_numpy(float)
        scores.append(s); weights.append(w)
    return weighted_conformal_quantile(np.concatenate(scores), np.concatenate(weights), alpha)


# ------------------------------------------------------------------ coverage summaries
def coverage(y, pred, q, groups):
    y, pred = np.asarray(y), np.asarray(pred)
    q = np.broadcast_to(np.asarray(q, float), y.shape)
    hit = np.abs(y - pred) <= q
    g = pd.Series(np.asarray(groups))
    w = 1.0 / g.map(g.value_counts()).to_numpy(float)
    per = pd.Series(hit).groupby(g.values).mean()
    return dict(coverage_rows=float(hit.mean()), coverage_studies=float(np.sum(w * hit) / np.sum(w)),
                width=float(np.mean(2 * q)), frac_studies_below_80=float((per < 0.8).mean()))
