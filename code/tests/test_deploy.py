import os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.models.deploy import order_study, simulate, QPOS


def test_design_order_centre_then_extremes():
    T = np.array([250, 300, 350, 280, 320, 260, 340.0]); t = np.zeros(7)
    o = order_study(T, t, "design")
    assert T[o[0]] == 300 and T[o[1]] == 250 and T[o[2]] == 350
    assert sorted(o.tolist()) == list(range(7))


def test_support_never_in_query_and_offsets():
    n = 12; y = np.arange(n, dtype=float) + 10; f = np.full(n, 5.0); g = np.array(["s"] * n)
    T = np.linspace(200, 350, n); t = np.zeros(n)
    df = simulate(y, f, g, T, t, k=3, lam=0.0, rule="reported", min_n=11)
    assert len(df) == n - QPOS and set(df.pos) == set(range(QPOS, n))
    # raw offset (lam = 0): mean(y_s - f_s) over first 3 runs = (10+11+12)/3 - 5 = 6
    assert np.allclose(df.B, 5 + 6) and np.allclose(df.C, 11)
    df0 = simulate(y, f, g, T, t, k=0, lam=1.0, rule="reported", min_n=11)
    assert np.allclose(df0.B, df0.A) and df0.C.isna().all()


def test_shrinkage_and_min_n():
    n = 12; y = np.full(n, 20.0); f = np.full(n, 10.0); g = np.array(["s"] * n)
    df = simulate(y, f, g, np.arange(n), np.zeros(n), k=2, lam=2.0, rule="reported", min_n=11)
    assert np.allclose(df.B, 10 + 0.5 * 10)
    assert simulate(y[:8], f[:8], g[:8], np.arange(8), np.zeros(8), 2, 1.0, "reported", min_n=11).empty
