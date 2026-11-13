import os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.models.contrast import within_pairs, study_center, AbsoluteModel, WithinStudyModel, PairwiseDiffModel, anchored_predictions


def _toy(seed=0, J=30, n=8):
    rng = np.random.default_rng(seed)
    g = np.repeat(np.arange(J), n).astype(str)
    x = rng.uniform(0, 1, (J * n, 2)); off = rng.normal(0, 10, J)[np.repeat(np.arange(J), n)]
    y = 20 * x[:, 0] + off + rng.normal(0, 0.5, J * n)
    return pd.DataFrame(x, columns=["a", "b"]), y, g


def test_within_pairs():
    g = np.array(["s1"] * 3 + ["s2"] * 2 + ["s3"] * 4)
    ia, ib = within_pairs(g, min_n=3)
    assert len(ia) == 3 + 6 and np.all(g[ia] == g[ib]) and np.all(ia < ib)


def test_study_center_zero_mean():
    X, y, g = _toy()
    c = study_center(X.to_numpy(), g)
    assert np.allclose(pd.DataFrame(c).groupby(g).mean().to_numpy(), 0)


def test_pd_antisymmetric_and_anchor():
    X, y, g = _toy()
    m = PairwiseDiffModel("ridge", {"alpha": 1e-3}, max_partners=7).fit(X, y, g)
    m.prepare(X, g)
    ia, ib = within_pairs(g)
    assert np.allclose(m.contrast_idx(ia, ib), -m.contrast_idx(ib, ia))
    # contrast model learns the slope (offset cancels): close to 20 * (x_a - x_b)
    assert np.corrcoef(m.contrast_idx(ia, ib), 20 * (X.a.values[ia] - X.a.values[ib]))[0, 1] > 0.99


def test_within_model_ignores_offsets_and_anchor_recovers_levels():
    X, y, g = _toy(1)
    w = WithinStudyModel("ridge", {"alpha": 1e-3}).fit(X, y, g)
    Xt, yt, gt = _toy(2)
    w.prepare(Xt, gt)
    sup = np.zeros(len(yt), bool); sup[::8] = True; qry = ~sup
    p = anchored_predictions(w, yt, gt, sup, qry)
    assert np.sqrt(np.nanmean((yt[qry] - p[qry]) ** 2)) < 2.0          # offsets (SD 10) removed by the anchor
    a = AbsoluteModel("ridge", {"alpha": 1e-3}).fit(X, y, g)
    assert np.sqrt(np.mean((yt - a.predict(Xt)) ** 2)) > 5.0            # absolute model cannot know new offsets
