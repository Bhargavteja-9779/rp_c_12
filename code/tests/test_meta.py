import numpy as np, pandas as pd
from src.meta.within_study import reml, pm_tau2, contrasts, study_effects, CONDS


def test_reml_homogeneous_and_heterogeneous():
    rng = np.random.default_rng(0)
    v = rng.uniform(0.5, 2, 200); y = 3 + rng.normal(0, np.sqrt(v))
    r = reml(y, v); assert abs(r["mu"] - 3) < 0.3 and r["tau2"] < 0.3
    y2 = 3 + rng.normal(0, np.sqrt(v + 4.0)); r2 = reml(y2, v)
    assert 2.5 < r2["tau2"] < 6.0
    t_pm, _ = pm_tau2(y2, v); assert abs(t_pm - r2["tau2"]) < 1.5
    assert r2["pi_lo"] < r2["ci_lo"] < r2["mu"] < r2["ci_hi"] < r2["pi_hi"]


def _toy():
    base = {c: 0.0 for c in CONDS}; base.update(feed="a", cat="none", med="water", atm="", proc="HTL")
    rows = []
    for s, off in [("s1", 0.0), ("s2", 30.0)]:
        for T in [250, 270, 290]:
            r = dict(base, study=s, T=float(T), biooil=off + 0.1 * T); rows.append(r)
        rows.append(dict(base, study=s, T=270.0, cat="alkali_carbonate", cat_ratio=0.05, biooil=off + 0.1 * 270 + 5))
    return pd.DataFrame(rows)


def test_contrasts_cancel_study_offset():
    F = _toy()
    C = contrasts(F, "T", "biooil")
    assert len(C) == 4 and np.allclose(C.effect, 1.0)  # 0.1 wt% per °C -> 1.0 per 10 °C, offsets cancel
    K = contrasts(F, "cat", "biooil")
    assert len(K) == 2 and np.allclose(K.effect, 5.0)


def test_study_effects_min_studies():
    F = _toy(); C = contrasts(F, "T", "biooil")
    assert study_effects(C, min_studies=5).empty
    assert len(study_effects(C, min_studies=2)) == 2
