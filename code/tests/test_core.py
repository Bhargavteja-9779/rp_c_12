"""Unit tests for leakage-critical and statistical components. Run: python -m pytest -q tests"""
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data.load import load_target, locked_test_studies, sha256, RAW, EXPECTED_SHA256, catalyst_class, medium_class
from src.evaluation.core import grouped_folds, random_folds, rmse, r2
from src.models.strata import (variance_components, weighted_conformal_quantile, study_quantile, row_quantile,
                               kshot_split, kshot_adjust, shrink_factor, coverage)
from src.statistics.stats import holm, rank_biserial


def test_dataset_checksum():
    assert sha256(RAW) == EXPECTED_SHA256


def test_locked_split_disjoint_and_stable():
    lock = locked_test_studies()
    assert len(lock) == 38
    for t in ("biooil", "solid"):
        dev, te = load_target(t, "dev"), load_target(t, "test")
        assert set(dev.groups).isdisjoint(set(te.groups))
        assert set(te.groups) <= lock


def test_no_identifier_features():
    ds = load_target("biooil", "dev")
    banned = {"DOI", "year", "paper_title", "Ref", "Provenance"}
    assert not banned & set(ds.X.columns)
    assert all(not c.lower().startswith(("doi", "year")) for c in ds.X.columns)


def test_grouped_folds_keep_studies_together():
    g = np.repeat(np.arange(30), 5)
    for tr, te in grouped_folds(g, k=10, seed=11):
        assert set(g[tr]).isdisjoint(set(g[te]))


def test_random_folds_cover_all_rows():
    f = random_folds(100, k=5, seed=11)
    assert sorted(np.concatenate([te for _, te in f]).tolist()) == list(range(100))


def test_variance_components_recovers_truth():
    rng = np.random.default_rng(0)
    J, n = 400, 8
    u = rng.normal(0, 2.0, J); g = np.repeat(np.arange(J), n)
    r = u[g] + rng.normal(0, 1.0, J * n)
    vc = variance_components(r, g)
    assert abs(vc["tau2"] - 4.0) < 0.8 and abs(vc["sigma2_w"] - 1.0) < 0.1


def test_conformal_quantile_finite_sample():
    s = np.arange(1, 20, dtype=float)  # 19 scores
    q = weighted_conformal_quantile(s, np.ones(19), alpha=0.1)  # ceil(0.9*20)=18th
    assert q == 18.0
    assert weighted_conformal_quantile(np.arange(5.), np.ones(5), 0.01) == float("inf")


def test_study_quantile_equal_study_weights():
    # one big study with tiny residuals must not dominate the study-weighted quantile
    r = np.r_[np.full(1000, 0.1), np.full(10, 5.0), np.full(10, 6.0)]
    g = np.r_[np.zeros(1000), np.ones(10), np.full(10, 2)]
    assert row_quantile(r, 0.1) < 1.0
    assert study_quantile(r, g, 0.1) >= 5.0


def test_coverage_exchangeable_simulation():
    rng = np.random.default_rng(1)
    J, n = 300, 6
    g = np.repeat(np.arange(J), n); u = rng.normal(0, 3, J)
    r = u[g] + rng.normal(0, 1, J * n)
    cal = g < 200
    q = study_quantile(r[cal], g[cal], 0.1)
    cov = coverage(r[~cal], np.zeros((~cal).sum()), q, g[~cal])
    assert 0.85 < cov["coverage_studies"] < 0.95
    q_row = row_quantile(r[cal], 0.1)
    assert abs(q - q_row) < 1.5  # same distribution here; difference arises only under clustering of calibration


def test_kshot_support_excluded_from_query():
    g = np.repeat(np.arange(10), 4)
    sup, qry = kshot_split(g, 2, np.random.default_rng(0))
    assert not np.any(sup & qry)
    assert sup.sum() == 20 and qry.sum() == 20
    off = kshot_adjust(np.ones(40), g, sup, 0.5)
    assert np.allclose(off, 0.5)


def test_shrink_factor_limits():
    assert shrink_factor(0, 1.0, "eb") == 0.0
    assert shrink_factor(3, 1.0, "raw") == 1.0
    assert abs(shrink_factor(3, 1.0, "eb") - 0.75) < 1e-12


def test_holm_and_rank_biserial():
    adj = holm([0.01, 0.04, 0.03])
    assert np.allclose(adj, [0.03, 0.06, 0.06])
    assert rank_biserial([1, 2, 3]) == 1.0 and rank_biserial([-1, -2]) == -1.0


def test_metrics():
    assert rmse([0, 0], [3, 4]) == np.sqrt(12.5)
    assert r2([1, 2, 3], [1, 2, 3]) == 1.0


def test_category_mappers():
    assert catalyst_class("K2CO3") == "alkali_carbonate"
    assert catalyst_class("none") == "none"
    assert catalyst_class(float("nan")) == "none"
    assert medium_class("Water") == "water"
    assert medium_class("Ethanol–Water") == "water_alcohol"
