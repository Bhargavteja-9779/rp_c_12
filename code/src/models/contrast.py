"""Offset-invariant ('trend') models for within-study contrasts (PROTOCOL Addendum A).

All models expose
    fit(X, y, groups)
    contrast(Xa, Xb, ga)  -> predicted y_a - y_b for pairs of runs of the same study (ga = their study ids)
    score(X, groups)      -> within-study ranking score (higher = higher predicted yield)
    prepare(X, groups)    -> cache study-dependent quantities for a test set (W needs the study means of the inputs)

A  : absolute model f;                contrast = f(x_a) - f(x_b)
W  : within-study model g on [x, x - xbar_study] with target y - ybar_study; contrast = g(a) - g(b).
     xbar is computed from the study's *inputs* only (no labels), so it is available for a new study.
PD : pairwise-difference model h on [x_a, x_b, x_a - x_b] -> y_a - y_b (PADRE-type; Tynes et al., 2021), trained on
     pairs of runs from the same training study; antisymmetrised: (h(a,b) - h(b,a)) / 2.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from src.models.registry import Learner


def _np(X):
    return X.to_numpy(float) if isinstance(X, pd.DataFrame) else np.asarray(X, float)


def study_center(X: np.ndarray, groups: np.ndarray) -> np.ndarray:
    """x - mean_x over the runs of the same study (NaN-aware; NaN deviations stay NaN)."""
    df = pd.DataFrame(X); m = df.groupby(np.asarray(groups)).transform("mean").to_numpy()
    return X - m


class AbsoluteModel:
    name = "A"

    def __init__(self, learner, params, seed=0, n_jobs=1):
        self.m = Learner(learner, params, seed=seed, n_jobs=n_jobs)

    def fit(self, X, y, groups):
        self.m.fit(X, y, groups); return self

    def prepare(self, X, groups):
        self._p = self.m.predict(X); return self

    def predict(self, X, groups=None):
        return self.m.predict(X)

    def contrast_idx(self, ia, ib):
        return self._p[ia] - self._p[ib]

    def score(self):
        return self._p


class WithinStudyModel:
    name = "W"

    def __init__(self, learner, params, seed=0, n_jobs=1):
        self.m = Learner(learner, params, seed=seed, n_jobs=n_jobs)

    @staticmethod
    def _feat(X, groups):
        Xv = _np(X)
        return np.hstack([Xv, study_center(Xv, groups)])

    def fit(self, X, y, groups):
        y = np.asarray(y, float)
        yc = y - pd.Series(y).groupby(np.asarray(groups)).transform("mean").to_numpy()
        self.m.fit(self._feat(X, groups), yc, groups); return self

    def prepare(self, X, groups):
        self._p = self.m.predict(self._feat(X, groups)); return self

    def contrast_idx(self, ia, ib):
        return self._p[ia] - self._p[ib]

    def score(self):
        return self._p


class PairwiseDiffModel:
    name = "PD"

    def __init__(self, learner, params, seed=0, n_jobs=1, max_partners=30):
        self.m = Learner(learner, params, seed=seed, n_jobs=n_jobs); self.seed = seed; self.k = max_partners

    @staticmethod
    def _pairfeat(Xa, Xb):
        return np.hstack([Xa, Xb, Xa - Xb])

    def fit(self, X, y, groups):
        Xv, y, g = _np(X), np.asarray(y, float), np.asarray(groups)
        rng = np.random.default_rng(self.seed); A, B = [], []
        for s in np.unique(g):
            idx = np.flatnonzero(g == s)
            if len(idx) < 2:
                continue
            for i in idx:
                others = idx[idx != i]
                part = others if len(others) <= self.k else rng.choice(others, self.k, replace=False)
                A.extend([i] * len(part)); B.extend(part.tolist())
        A, B = np.array(A), np.array(B)
        self.n_pairs_ = len(A)
        self.m.fit(self._pairfeat(Xv[A], Xv[B]), y[A] - y[B], g[A]); return self

    def prepare(self, X, groups):
        self._X = _np(X); self._g = np.asarray(groups); return self

    def contrast_idx(self, ia, ib):
        Xa, Xb = self._X[ia], self._X[ib]
        out = np.empty(len(ia)); step = 200_000
        for s in range(0, len(ia), step):
            sl = slice(s, s + step)
            out[sl] = 0.5 * (self.m.predict(self._pairfeat(Xa[sl], Xb[sl])) - self.m.predict(self._pairfeat(Xb[sl], Xa[sl])))
        return out

    def score(self):
        """PADRE-style score: mean predicted contrast of each run against the other runs of its study."""
        sc = np.zeros(len(self._g))
        for s in np.unique(self._g):
            idx = np.flatnonzero(self._g == s)
            if len(idx) < 2:
                continue
            ia = np.repeat(idx, len(idx)); ib = np.tile(idx, len(idx)); keep = ia != ib
            c = self.contrast_idx(ia[keep], ib[keep])
            sc[idx] = pd.Series(c).groupby(ia[keep]).mean().reindex(idx).to_numpy()
        return sc


MODELS = {"A": AbsoluteModel, "W": WithinStudyModel, "PD": PairwiseDiffModel}


def within_pairs(groups, min_n=3):
    """All unordered pairs (a < b) of runs within each study with >= min_n runs."""
    g = np.asarray(groups); A, B = [], []
    for s in np.unique(g):
        idx = np.flatnonzero(g == s)
        if len(idx) < min_n:
            continue
        ia, ib = np.triu_indices(len(idx), 1)
        A.append(idx[ia]); B.append(idx[ib])
    if not A:
        return np.array([], int), np.array([], int)
    return np.concatenate(A), np.concatenate(B)


def anchored_predictions(model, y, groups, support, query):
    """Level prediction for query runs from the measured support (anchor) runs of the same study:
    y_hat_i = mean_a ( y_a + contrast(i, a) )."""
    g = np.asarray(groups); out = np.full(len(g), np.nan)
    for s in np.unique(g[query]):
        q = np.flatnonzero(query & (g == s)); a = np.flatnonzero(support & (g == s))
        if len(a) == 0:
            continue
        ia = np.repeat(q, len(a)); ib = np.tile(a, len(q))
        c = model.contrast_idx(ia, ib) + np.asarray(y)[ib]
        out[q] = c.reshape(len(q), len(a)).mean(axis=1)
    return out
