"""Learner registry: factories and equal-budget hyper-parameter search spaces (PROTOCOL §7).

Every learner exposes ``fit(X, y, groups=None)`` and ``predict(X)``.  Preprocessing that estimates
statistics (median imputation, scaling) is part of the estimator, so it is refitted inside every
training fold and never sees test data.
"""
from __future__ import annotations

import importlib.util
import numpy as np
import pandas as pd
from scipy.stats import loguniform, randint, uniform
from sklearn.base import BaseEstimator, RegressorMixin, clone
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import ExtraTreesRegressor, HistGradientBoostingRegressor, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR

NAN_NATIVE = {"hgb", "lgbm", "xgb", "cat", "gpboost"}


def _imp(scale: bool):
    steps = [SimpleImputer(strategy="median", add_indicator=True, keep_empty_features=True)]
    if scale:
        steps.append(StandardScaler())
    return steps


class Learner(BaseEstimator, RegressorMixin):
    """Thin uniform wrapper; ``name`` selects the underlying estimator, ``params`` its hyper-parameters."""

    def __init__(self, name: str = "lgbm", params: dict | None = None, seed: int = 0, n_jobs: int = 1):
        self.name, self.params, self.seed, self.n_jobs = name, params, seed, n_jobs

    # ------------------------------------------------------------------
    def _make(self):
        p = dict(self.params or {})
        s, nj = self.seed, self.n_jobs
        n = self.name
        if n == "mean":
            return DummyRegressor(strategy="mean")
        if n == "ridge":
            return make_pipeline(*_imp(True), Ridge(**p))
        if n == "knn":
            return make_pipeline(*_imp(True), KNeighborsRegressor(n_jobs=nj, **p))
        if n == "svr":
            return make_pipeline(*_imp(True), SVR(**p))
        if n == "mlp":
            return make_pipeline(*_imp(True), MLPRegressor(random_state=s, early_stopping=True, max_iter=2000,
                                                           n_iter_no_change=30, **p))
        if n == "rf":
            return make_pipeline(*_imp(False), RandomForestRegressor(n_estimators=500, random_state=s, n_jobs=nj, **p))
        if n == "et":
            return make_pipeline(*_imp(False), ExtraTreesRegressor(n_estimators=500, random_state=s, n_jobs=nj, **p))
        if n == "hgb":
            return HistGradientBoostingRegressor(random_state=s, **p)
        if n == "lgbm":
            import lightgbm as lgb
            return lgb.LGBMRegressor(random_state=s, n_jobs=nj, verbose=-1, subsample_freq=1, **p)
        if n == "xgb":
            import xgboost as xgb
            return xgb.XGBRegressor(random_state=s, n_jobs=nj, tree_method="hist", **p)
        if n == "cat":
            from catboost import CatBoostRegressor
            return CatBoostRegressor(random_seed=s, thread_count=nj, verbose=False, allow_writing_files=False, **p)
        if n == "gpboost":
            return _GPBoost(seed=s, n_jobs=nj, **p)
        if n == "tabpfn":
            from tabpfn import TabPFNRegressor
            return TabPFNRegressor(random_state=s, device="auto", **p)
        raise ValueError(n)

    def fit(self, X, y, groups=None):
        self.model_ = self._make()
        Xv = X.to_numpy(float) if isinstance(X, pd.DataFrame) else np.asarray(X, float)
        if self.name == "gpboost":
            self.model_.fit(Xv, np.asarray(y, float), groups)
        else:
            self.model_.fit(Xv, np.asarray(y, float))
        return self

    def predict(self, X):
        Xv = X.to_numpy(float) if isinstance(X, pd.DataFrame) else np.asarray(X, float)
        return np.asarray(self.model_.predict(Xv), float).ravel()


class _GPBoost:
    """Tree boosting with a grouped (study) random intercept (Sigrist, 2022).

    For unseen studies the predicted random effect is its prior mean (0), i.e. the fixed-effect function.
    """

    def __init__(self, seed=0, n_jobs=1, learning_rate=0.05, num_leaves=31, min_data_in_leaf=20,
                 num_boost_round=300, lambda_l2=0.0, feature_fraction=1.0):
        self.kw = dict(learning_rate=learning_rate, num_leaves=num_leaves, min_data_in_leaf=min_data_in_leaf,
                       lambda_l2=lambda_l2, feature_fraction=feature_fraction, seed=seed, num_threads=n_jobs, verbose=-1)
        self.rounds = int(num_boost_round)

    def fit(self, X, y, groups):
        import gpboost as gpb
        if groups is None:
            raise ValueError("gpboost requires study groups")
        self.gp_ = gpb.GPModel(group_data=np.asarray(groups), likelihood="gaussian")
        self.bst_ = gpb.train(params=self.kw, train_set=gpb.Dataset(X, y), gp_model=self.gp_, num_boost_round=self.rounds)
        return self

    def predict(self, X):
        new = np.array(["__unseen_study__"] * len(X))
        out = self.bst_.predict(data=X, group_data_pred=new, predict_var=False, pred_latent=False)
        return np.asarray(out["response_mean"], float)


def search_space(name: str) -> dict:
    """Equal-size random-search spaces (sampled 20× with seed 0 in full mode)."""
    return {
        "mean": {},
        "ridge": {"alpha": loguniform(1e-3, 1e3)},
        "knn": {"n_neighbors": randint(3, 40), "weights": ["uniform", "distance"]},
        "svr": {"C": loguniform(0.3, 300), "gamma": loguniform(1e-3, 0.3), "epsilon": uniform(0.1, 3.0)},
        "mlp": {"hidden_layer_sizes": [(64,), (128,), (128, 64), (256, 128)], "alpha": loguniform(1e-5, 1e-1),
                "learning_rate_init": loguniform(3e-4, 3e-3), "batch_size": [32, 64, 128]},
        "rf": {"max_features": [0.3, 0.5, 0.7, 1.0], "min_samples_leaf": randint(1, 10), "max_depth": [None, 8, 16]},
        "et": {"max_features": [0.3, 0.5, 0.7, 1.0], "min_samples_leaf": randint(1, 10), "max_depth": [None, 8, 16]},
        "hgb": {"learning_rate": loguniform(0.02, 0.2), "max_leaf_nodes": randint(7, 64), "min_samples_leaf": randint(5, 50),
                "l2_regularization": loguniform(1e-3, 3.0), "max_iter": randint(200, 1000)},
        "lgbm": {"learning_rate": loguniform(0.01, 0.1), "num_leaves": randint(7, 64), "min_child_samples": randint(5, 50),
                 "subsample": uniform(0.6, 0.4), "colsample_bytree": uniform(0.5, 0.5), "reg_lambda": loguniform(1e-3, 10),
                 "n_estimators": randint(200, 1200)},
        "xgb": {"learning_rate": loguniform(0.01, 0.1), "max_depth": randint(3, 9), "min_child_weight": loguniform(1, 20),
                "subsample": uniform(0.6, 0.4), "colsample_bytree": uniform(0.5, 0.5), "reg_lambda": loguniform(1e-3, 10),
                "n_estimators": randint(200, 1200)},
        "cat": {"learning_rate": loguniform(0.02, 0.15), "depth": randint(4, 9), "l2_leaf_reg": loguniform(1, 10),
                "iterations": randint(300, 1200)},
        "gpboost": {"learning_rate": loguniform(0.01, 0.1), "num_leaves": randint(7, 64), "min_data_in_leaf": randint(5, 50),
                    "lambda_l2": loguniform(1e-3, 10), "feature_fraction": uniform(0.5, 0.5), "num_boost_round": randint(200, 1000)},
        "tabpfn": {},
    }[name]


def available(name: str) -> bool:
    mod = {"lgbm": "lightgbm", "xgb": "xgboost", "cat": "catboost", "gpboost": "gpboost", "tabpfn": "tabpfn"}.get(name)
    return mod is None or importlib.util.find_spec(mod) is not None


ALL_LEARNERS = ["mean", "ridge", "knn", "svr", "mlp", "rf", "et", "hgb", "lgbm", "xgb", "cat", "gpboost", "tabpfn"]
