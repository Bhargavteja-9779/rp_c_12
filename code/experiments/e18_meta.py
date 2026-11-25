"""E18 (PROTOCOL Addendum E): within-study meta-analysis of process and feedstock effects, laboratory effect, pooled-model comparison,
SHAP importance and the one-time confirmatory test on the locked studies.

python experiments/e18_meta.py full [dev|locked|all]
"""
from __future__ import annotations

import json, os, sys
import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.meta.within_study import (OUTCOMES, PRIMARY, CAT_CLASSES, MED_CLASSES, T_BANDS, BAND_LABEL, COMP, frame, contrasts, study_effects,
                                   reml, pm_tau2, egger, feedstock_regression)
from src.statistics.stats import holm
from src.utils import out_dirs, dump
from experiments.common import load_cell

FACTORS = ["T", "t", "load", "cat", "med"]
UNIT = {"T": "per +10 °C", "t": "per doubling of residence time", "load": "per +10 percentage points of solid loading",
        "cat": "catalyst vs none", "med": "medium vs water"}


def meta_table(F, outcomes):
    rows, allC, allS = [], [], []
    for o in outcomes:
        for fac in FACTORS:
            C = contrasts(F, fac, o)
            if C.empty:
                continue
            C["outcome"], C["factor"] = o, fac
            allC.append(C)
            S = study_effects(C)
            if S.empty:
                continue
            S["outcome"], S["factor"] = o, fac; allS.append(S)
            for lv, q in S.groupby("level"):
                r = reml(q.y, q.v)
                t_pm, mu_pm = pm_tau2(q.y, q.v)
                # one-contrast-per-study (median) estimator: equal variances
                med = C[C.level == lv].groupby("study").effect.median()
                r1 = reml(med.values, np.full(len(med), q.s2w.iloc[0]))
                loo = [reml(q.y.drop(i), q.v.drop(i))["mu"] for i in q.index] if len(q) > 5 else [np.nan]
                rows.append(dict(outcome=o, factor=fac, level=lv, unit=UNIT[fac], n_contrasts=int((C.level == lv).sum()), **r,
                                 tau2_pm=t_pm, mu_pm=mu_pm, mu_median_estimator=r1["mu"], loo_min=float(np.nanmin(loo)), loo_max=float(np.nanmax(loo)),
                                 egger_p=egger(q.y, q.v), s2w=float(q.s2w.iloc[0])))
    return pd.DataFrame(rows), pd.concat(allC, ignore_index=True), pd.concat(allS, ignore_index=True)


def moderators(F, C_all, outcomes):
    """Pre-specified subgroup analyses for catalyst and medium effects (>= 10 studies)."""
    lig_med = {}
    out = []
    for o in outcomes:
        for fac in ["cat", "med"]:
            C = C_all[(C_all.outcome == o) & (C_all.factor == fac)].copy()
            if C.empty:
                continue
            first = C.i.map(lambda ix: ix[0] if isinstance(ix, list) else ix)
            C["proc"] = F.loc[first.values, "proc"].values
            C["lignin"] = F.loc[first.values, "feed_lignin"].values
            fam = []
            for lv, q in C.groupby("level"):
                if q.study.nunique() < 10:
                    continue
                lm = q.groupby("study").lignin.first().median()
                splits = {"temperature": (q["T"] < 300, "<300 °C", "≥300 °C"), "process": (q.proc == "HTC", "HTC", "HTL"),
                          "lignin": (q.lignin <= lm, f"lignin ≤ {lm:.0f} wt%", f"lignin > {lm:.0f} wt%")}
                for mod, (mask, a, b) in splits.items():
                    res = {}
                    for name, sub in [(a, q[mask.fillna(False)]), (b, q[~mask.fillna(False)])]:
                        S = study_effects(sub.assign(level="x"))
                        res[name] = reml(S.y, S.v) if len(S) >= 5 else None
                    if all(res.values()):
                        ra, rb = res[a], res[b]
                        z = (ra["mu"] - rb["mu"]) / np.sqrt(ra["se"] ** 2 + rb["se"] ** 2)
                        fam.append(dict(outcome=o, factor=fac, level=lv, moderator=mod, group_a=a, mu_a=ra["mu"], k_a=ra["k"], group_b=b, mu_b=rb["mu"],
                                        k_b=rb["k"], diff=ra["mu"] - rb["mu"], p=float(2 * stats.norm.sf(abs(z)))))
            for r, pa in zip(fam, holm([x["p"] for x in fam]) if fam else []):
                r["p_holm"] = float(pa)
            out.extend(fam)
    return pd.DataFrame(out)


# ------------------------------------------------------------------ pooled models (E3, E4)
def design(F):
    X = pd.DataFrame(index=F.index)
    for c in ["feed_C", "feed_H", "feed_O"] + COMP + ["T", "log2t", "load", "hr", "cat_ratio", "gas_p"]:
        X[c] = F[c].astype(float)
    for c in CAT_CLASSES:
        X[f"cat_{c}"] = (F.cat == c).astype(float)
    for c in MED_CLASSES + ["ketone", "other"]:
        X[f"med_{c}"] = (F.med == c).astype(float)
    X["proc_solvothermal"] = (F.proc == "HTL_solvothermal").astype(float); X["proc_HTC"] = (F.proc == "HTC").astype(float)
    return X


def fit_xgb(X, y, params):
    import xgboost as xgb
    m = xgb.XGBRegressor(random_state=0, n_jobs=4, tree_method="hist", **params); m.fit(X.to_numpy(float), y); return m


def model_effects(predict, X, F, outcome):
    """Partial-dependence-style effects implied by a fitted pooled model, on the scale of the meta-analytic effects."""
    out = []
    P = lambda Z: predict(Z)
    for (lo, hi) in T_BANDS:
        a, b = (200, 250) if lo == 0 else ((350, 400) if hi == 1000 else (lo, hi))
        Za, Zb = X.copy(), X.copy(); Za["T"], Zb["T"] = a, b
        out.append(dict(factor="T", level=BAND_LABEL[(lo, hi)], effect=float(np.mean(P(Zb) - P(Za)) / ((b - a) / 10))))
    for fac, col, unit in [("t", "log2t", 1.0), ("load", "load", 10.0)]:
        x = X[col].dropna()
        if x.nunique() < 3:
            continue
        a, b = np.quantile(x, [0.25, 0.75])
        Za, Zb = X.copy(), X.copy(); Za[col], Zb[col] = a, b
        out.append(dict(factor=fac, level="all", effect=float(np.mean(P(Zb) - P(Za)) / ((b - a) / unit))))
    for c in CAT_CLASSES:
        r = F.loc[F.cat == c, "cat_ratio"]; r = float(r[r > 0].median()) if (r > 0).any() else 0.1
        Za, Zb = X.copy(), X.copy()
        for cc in CAT_CLASSES:
            Za[f"cat_{cc}"] = 0.0; Zb[f"cat_{cc}"] = float(cc == c)
        Za["cat_ratio"], Zb["cat_ratio"] = 0.0, r
        out.append(dict(factor="cat", level=c, effect=float(np.mean(P(Zb) - P(Za)))))
    for m in MED_CLASSES:
        Za, Zb = X.copy(), X.copy()
        for mm in MED_CLASSES + ["ketone", "other"]:
            Za[f"med_{mm}"] = 0.0; Zb[f"med_{mm}"] = float(mm == m)
        out.append(dict(factor="med", level=m, effect=float(np.mean(P(Zb) - P(Za)))))
    return pd.DataFrame(out)


def linear_design(X):
    Z = X.copy()
    for h in [250, 300, 350]:
        Z[f"T_hinge{h}"] = np.maximum(Z["T"] - h, 0)
    miss = Z.isna()
    for c in Z.columns:
        if miss[c].any():
            Z[c + "_na"] = miss[c].astype(float); Z[c] = Z[c].fillna(Z[c].median())
    return Z.loc[:, Z.std() > 0]


def linear_effects(X, y, groups, fe):
    Z = linear_design(X)
    if fe:  # within transformation = study fixed effects
        Zv = Z - Z.groupby(groups).transform("mean"); yv = y - pd.Series(y, index=Z.index).groupby(groups).transform("mean").to_numpy()
        Zv = Zv.loc[:, Zv.std() > 1e-9]
    else:
        Zv = Z.assign(const=1.0); yv = y
    beta = pd.Series(np.linalg.lstsq(Zv.to_numpy(), yv, rcond=None)[0], index=Zv.columns)
    g = lambda k: float(beta.get(k, 0.0))
    out = []
    slope = g("T")
    for (lo, hi), h in zip(T_BANDS, [None, 250, 300, 350]):
        s = g("T") + sum(g(f"T_hinge{hh}") for hh in [250, 300, 350] if hh < hi and hh >= 250 and hh <= lo)
        out.append(dict(factor="T", level=BAND_LABEL[(lo, hi)], effect=10 * s))
    out.append(dict(factor="t", level="all", effect=g("log2t")))
    out.append(dict(factor="load", level="all", effect=10 * g("load")))
    for c in CAT_CLASSES:
        out.append(dict(factor="cat", level=c, effect=g(f"cat_{c}") + g("cat_ratio") * float(np.nanmedian(X.loc[X[f"cat_{c}"] == 1, "cat_ratio"]) if (X[f"cat_{c}"] == 1).any() else 0)))
    for m in MED_CLASSES:
        out.append(dict(factor="med", level=m, effect=g(f"med_{m}")))
    return pd.DataFrame(out)


SHAP_GROUPS = {"temperature": ["T"], "residence time": ["log2t"], "solid loading": ["load"], "heating rate": ["hr"],
               "catalyst": ["cat_ratio"] + [f"cat_{c}" for c in CAT_CLASSES], "reaction medium": [f"med_{m}" for m in MED_CLASSES + ["ketone", "other"]],
               "feedstock composition": ["feed_C", "feed_H", "feed_O"] + COMP, "process / gas": ["proc_solvothermal", "proc_HTC", "gas_p"]}


def shap_importance(model, X):
    import xgboost as xgb
    contrib = model.get_booster().predict(xgb.DMatrix(X.to_numpy(float)), pred_contribs=True)[:, :-1]
    imp = pd.Series(np.abs(contrib).mean(axis=0), index=X.columns)
    return {g: float(imp[[c for c in cols if c in imp.index]].sum()) for g, cols in SHAP_GROUPS.items()}


def run_dev(D):
    F = frame("dev")
    M, C, S = meta_table(F, list(OUTCOMES))
    M.to_csv(os.path.join(D["results"], "e18_meta_dev.csv"), index=False)
    C.drop(columns=["i", "j"]).to_csv(os.path.join(D["results"], "e18_contrasts_dev.csv.gz"), index=False)
    S.to_csv(os.path.join(D["results"], "e18_study_effects_dev.csv"), index=False)
    mods = moderators(F, C, list(OUTCOMES)); mods.to_csv(os.path.join(D["results"], "e18_moderators_dev.csv"), index=False)
    fr = [r for o in OUTCOMES if (r := feedstock_regression(F, o)) is not None]
    FR = pd.concat(fr) if fr else pd.DataFrame(); FR.to_csv(os.path.join(D["results"], "e18_feedstock_dev.csv"), index=False)
    # E3/E4: pooled models on all development runs of each primary outcome
    comp, shap = [], {}
    for o in PRIMARY:
        q = F[F[o].notna()]; X = design(q); y = q[o].to_numpy()
        params = load_cell(D, o, "base", "xgb")["params"]
        m = fit_xgb(X, y, params)
        e_x = model_effects(lambda Z: m.predict(Z.to_numpy(float)), X, q, o).assign(model="pooled XGBoost")
        e_l = linear_effects(X, y, q.study.to_numpy(), fe=False).assign(model="pooled linear")
        e_f = linear_effects(X, y, q.study.to_numpy(), fe=True).assign(model="study fixed-effects linear")
        comp.append(pd.concat([e_x, e_l, e_f]).assign(outcome=o))
        shap[o] = shap_importance(m, X)
    P = pd.concat(comp, ignore_index=True)
    P = P.merge(M[["outcome", "factor", "level", "k", "mu", "ci_lo", "ci_hi", "pi_lo", "pi_hi"]], on=["outcome", "factor", "level"], how="inner")
    P.to_csv(os.path.join(D["results"], "e18_pooled_vs_meta_dev.csv"), index=False)
    summ = []
    for mdl, q in P.groupby("model"):
        sig = q[(q.ci_lo > 0) | (q.ci_hi < 0)]
        summ.append(dict(model=mdl, n_items=int(len(q)), n_sig_meta=int(len(sig)), sign_agree_sig=float((np.sign(sig.effect) == np.sign(sig.mu)).mean()) if len(sig) else np.nan,
                         n_sign_reversal_sig=int((np.sign(sig.effect) != np.sign(sig.mu)).sum()), spearman=float(stats.spearmanr(q.effect, q.mu).statistic),
                         share_outside_ci=float(((q.effect < q.ci_lo) | (q.effect > q.ci_hi)).mean()),
                         median_abs_diff=float(np.median(np.abs(q.effect - q.mu)))))
    res = dict(pooled_summary=summ, shap_group_importance=shap)
    dump(res, os.path.join(D["stats"], "e18_dev.json"))
    print(M[M.outcome.isin(PRIMARY)][["outcome", "factor", "level", "k", "mu", "ci_lo", "ci_hi", "pi_lo", "pi_hi", "I2", "p_benefit"]].round(2).to_string())
    print(pd.DataFrame(summ).round(3).to_string()); print(json.dumps(shap, indent=1))
    return M


def run_locked(D):
    """E5: one-time confirmatory test on the locked studies."""
    M = pd.read_csv(os.path.join(D["results"], "e18_meta_dev.csv"))
    Fd, Ft = frame("dev"), frame("test")
    rows = []
    for o in PRIMARY:
        q = Fd[Fd[o].notna()]; m = fit_xgb(design(q), q[o].to_numpy(), load_cell(D, o, "base", "xgb")["params"])
        Xt = design(Ft); ft = pd.Series(m.predict(Xt.to_numpy(float)), index=Ft.index)
        for fac in FACTORS:
            C = contrasts(Ft, fac, o)
            for r in C.itertuples():
                mm = M[(M.outcome == o) & (M.factor == fac) & (M.level == r.level)]
                if mm.empty:
                    continue
                mu = float(mm.mu.iloc[0])
                scale = ((r.x_hi - r.x_lo) / {"T": 10.0, "t": 1.0, "load": 10.0}[fac]) if fac in ("T", "t", "load") else 1.0
                ii, jj = (r.i if isinstance(r.i, list) else [r.i]), (r.j if isinstance(r.j, list) else [r.j])
                rows.append(dict(outcome=o, factor=fac, level=r.level, study=r.study, dy=r.dy, pred_meta=mu * scale,
                                 pred_xgb=float(ft[jj].mean() - ft[ii].mean()), pred_zero=0.0, effect=r.effect,
                                 pi_lo=float(mm.pi_lo.iloc[0]), pi_hi=float(mm.pi_hi.iloc[0])))
    L = pd.DataFrame(rows); L.to_csv(os.path.join(D["results"], "e18_locked_contrasts.csv"), index=False)
    per = L.groupby("study").apply(lambda z: pd.Series({k: float(np.sqrt(np.mean((z.dy - z[k]) ** 2))) for k in ["pred_meta", "pred_xgb", "pred_zero"]}))
    from src.statistics.stats import paired_comparison
    t1 = stats.wilcoxon(per.pred_meta, per.pred_xgb, alternative="less"); t2 = stats.wilcoxon(per.pred_meta, per.pred_zero, alternative="less")
    ph = holm([t1.pvalue, t2.pvalue])
    se = L.groupby(["outcome", "factor", "level", "study"]).agg(effect=("effect", "mean"), pi_lo=("pi_lo", "first"), pi_hi=("pi_hi", "first")).reset_index()
    cov = float(((se.effect >= se.pi_lo) & (se.effect <= se.pi_hi)).mean())
    sign = L[L.pred_meta != 0]
    res = dict(n_contrasts=int(len(L)), n_studies=int(per.shape[0]), median_rmse=per.median().to_dict(),
               meta_vs_xgb=dict(p=float(t1.pvalue), p_holm=float(ph[0]), **{k: v for k, v in paired_comparison(per.pred_meta.values, per.pred_xgb.values).items() if k in ("median_diff", "ci_low", "ci_high", "n")}),
               meta_vs_zero=dict(p=float(t2.pvalue), p_holm=float(ph[1]), **{k: v for k, v in paired_comparison(per.pred_meta.values, per.pred_zero.values).items() if k in ("median_diff", "ci_low", "ci_high", "n")}),
               pi_coverage_study_effects=cov, n_study_effects=int(len(se)),
               sign_agreement_meta=float((np.sign(sign.dy) == np.sign(sign.pred_meta)).mean()),
               sign_agreement_xgb=float((np.sign(sign.dy) == np.sign(sign.pred_xgb)).mean()))
    per.to_csv(os.path.join(D["results"], "e18_locked_per_study.csv"))
    dump(res, os.path.join(D["stats"], "e18_locked.json")); print(json.dumps(res, indent=1, default=str))


def lab_effect_mixedlm(D):
    """E2 sensitivity (added with the analysis, not in Addendum E): linear mixed model y ~ conditions + composition + (1 | study)."""
    import statsmodels.api as sm
    F = frame("dev"); out = {}
    for o in OUTCOMES:
        q = F[F[o].notna()]
        if q.study.nunique() < 20:
            continue
        Z = linear_design(design(q)); y = q[o].to_numpy()
        Z = Z.loc[:, Z.std() > 0]; Z = (Z - Z.mean()) / Z.std()
        from scipy.linalg import qr
        _, R_, piv = qr(Z.to_numpy(float), mode="economic", pivoting=True)
        rank = int((np.abs(np.diag(R_)) > 1e-8 * np.abs(R_[0, 0])).sum()); Z = Z.iloc[:, sorted(piv[:rank])]
        Zc = sm.add_constant(Z.to_numpy(float))
        try:
            m = sm.MixedLM(y, Zc, groups=q.study.to_numpy()).fit(reml=True, method="lbfgs")
            tau = float(np.sqrt(np.asarray(m.cov_re)[0, 0])); sig = float(np.sqrt(m.scale))
            out[o] = dict(tau=tau, sigma=sig, icc=tau ** 2 / (tau ** 2 + sig ** 2), n_runs=int(len(y)), n_studies=int(q.study.nunique()))
        except Exception as e:
            out[o] = dict(error=str(e))
    dump(out, os.path.join(D["stats"], "e18_lab_effect_mixedlm.json")); print(json.dumps(out, indent=1))


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"; part = sys.argv[2] if len(sys.argv) > 2 else "dev"
    D = out_dirs(mode)
    if part in ("dev", "all"):
        run_dev(D)
    if part in ("locked", "all"):
        run_locked(D)
    if part in ("lab", "dev", "all"):
        lab_effect_mixedlm(D)
