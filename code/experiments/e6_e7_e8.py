"""E6 efficiency, E7 sensitivity, E8 error analysis (+ meta-regression of study offsets for RQ3).

E6: each learner (E1-tuned, base features, bio-oil) fitted on all development rows in a fresh
    subprocess; wall-clock fit/predict time, peak resident memory increase, serialized size.
E7: (a) alpha in {0.05, 0.1, 0.2}; (b) tau^2 estimator (method of moments vs REML via statsmodels MixedLM)
    for the k-shot shrinkage; (c) number of outer folds (5 vs 10); (d) untuned default vs tuned learner.
E8: error analysis of outer-fold predictions (family, process, medium, catalyst, extraction solvent, T bins,
    worst studies) and meta-regression of study offsets on study-level protocol descriptors.
"""
from __future__ import annotations

import os, sys, json, pickle, subprocess, time
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data.load import load_target
from src.evaluation.core import grouped_folds, oof_predict, summary, restore, rmse
from src.models.registry import Learner, available
from src.models.strata import variance_components, coverage
from src.utils import out_dirs, load_config, get_logger, dump, CODE
from experiments.common import choose_base_learner, load_cell, nested_fit, kshot_eval

_E6_CHILD = r'''
import os, sys, json, pickle, time, resource
sys.path.insert(0, {code!r})
import numpy as np
from src.data.load import load_target
from src.models.registry import Learner
from src.evaluation.core import restore
ds = load_target("biooil", "dev"); X = ds.X[ds.base_features]
params = restore(json.loads({params!r}))
r0 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
t0 = time.perf_counter(); m = Learner({name!r}, params, seed=0, n_jobs=1).fit(X, ds.y, ds.groups); t1 = time.perf_counter()
reps = 20; t2 = time.perf_counter()
for _ in range(reps): m.predict(X)
t3 = time.perf_counter()
r1 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
try: size = len(pickle.dumps(m))
except Exception: size = None
print(json.dumps(dict(fit_s=t1 - t0, predict_ms_per_1000_rows=1000 * (t3 - t2) / reps / len(X) * 1000,
                      peak_rss_increase_MB=(r1 - r0) / 1024, model_size_MB=None if size is None else size / 2**20, n_train=len(X))))
'''


def efficiency(cfg, D, log):
    rows = []
    for name in cfg["learners"]:
        f = os.path.join(D["logs"], "e1_cells", f"biooil__base__{name}.json")
        if not os.path.exists(f) or not available(name):
            continue
        params = json.dumps(json.load(open(f))["params"])
        code = _E6_CHILD.format(code=CODE, params=params, name=name)
        r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=3600,
                           env={**os.environ, "OMP_NUM_THREADS": "1"})
        try:
            out = json.loads(r.stdout.strip().splitlines()[-1]); rows.append(dict(learner=name, **out))
            log.info(f"efficiency {name}: {out}")
        except Exception:
            log.error(f"efficiency {name} failed: {r.stderr[-500:]}")
    pd.DataFrame(rows).to_csv(os.path.join(D["results"], "e6_efficiency.csv"), index=False)


def _reml_lambda(res, groups):
    import statsmodels.formula.api as smf
    d = pd.DataFrame({"r": res, "g": groups})
    m = smf.mixedlm("r ~ 1", d, groups=d["g"]).fit(reml=True, method="lbfgs")
    tau2 = float(m.cov_re.iloc[0, 0]); s2 = float(m.scale)
    return s2 / tau2 if tau2 > 0 else np.inf, tau2, s2


def sensitivity(cfg, D, log, learner):
    rows = []
    for target in ["biooil", "solid"]:
        ds = load_target(target, "dev")
        for fs in ["base", "base+P"]:
            cols = ds.base_features + (ds.protocol_features if fs == "base+P" else [])
            X = ds.X[cols]
            params = load_cell(D, target, fs, learner)["params"]
            # (b) tau^2 estimator for k-shot shrinkage, (c) 5 vs 10 outer folds
            for nfold in sorted({5, cfg["outer_folds"]}):
                for fi, (tr, te) in enumerate(grouped_folds(ds.groups, k=nfold, seed=cfg["outer_seeds"][0])):
                    nf = nested_fit(learner, params, X.iloc[tr], ds.y[tr], ds.groups[tr], X.iloc[te], inner_k=cfg["inner_folds"],
                                    seed=fi, n_jobs=cfg["n_jobs"], alphas=cfg["alphas"])
                    for a in cfg["alphas"]:
                        for c in ["RC", "SC"]:
                            rows.append(dict(target=target, features=fs, analysis="outer_folds_alpha", outer_folds=nfold, fold=fi, alpha=a,
                                             calibration=c, rmse=rmse(ds.y[te], nf["pred"]), **coverage(ds.y[te], nf["pred"], nf["q"][a][c], ds.groups[te])))
                    if nfold == cfg["outer_folds"]:
                        lam_reml, t2, s2 = _reml_lambda(nf["res_sc"], nf["g_cal"])
                        for est, lam in [("MoM", nf["vc"]["lam"]), ("REML", lam_reml)]:
                            ks = kshot_eval(ds.y[te], nf["pred"], ds.groups[te], nf, cfg["k_values"], cfg["alpha"], cfg["kshot_draws"],
                                            modes=("eb",), min_n=max(cfg["k_values"]) + 1, lam_override=lam)
                            for r in ks:
                                rows.append(dict(target=target, features=fs, analysis="tau2_estimator", estimator=est, fold=fi, **r))
            # (d) untuned defaults vs tuned
            for label, p in [("tuned", restore(params)), ("default", {})]:
                for s in cfg["outer_seeds"][:1]:
                    pr, _, _ = oof_predict(learner, p, X, ds.y, ds.groups, grouped_folds(ds.groups, k=cfg["outer_folds"], seed=s), n_jobs=cfg["n_jobs"])
                    rows.append(dict(target=target, features=fs, analysis="tuning", config=label, **summary(ds.y, pr, ds.groups)))
            log.info(f"sensitivity {target} {fs} done")
    pd.DataFrame(rows).to_csv(os.path.join(D["results"], "e7_sensitivity.csv"), index=False)


def error_analysis(cfg, D, log):
    from src.data.load import read_raw
    out = []
    for target in ["biooil", "solid"]:
        ds = load_target(target, "dev")
        p = pd.read_csv(os.path.join(D["pred"], f"e3_{target}__base.csv.gz"))
        p = p.groupby("idx", as_index=False).agg(y=("y", "first"), pred=("pred", "mean"), study=("study", "first"))
        m = ds.meta.iloc[p["idx"]].reset_index(drop=True)
        X = ds.X.iloc[p["idx"]].reset_index(drop=True)
        p["resid"] = p["y"] - p["pred"]
        ex = np.array(["none_named"] * len(X), dtype=object)
        for c in [c for c in X.columns if c.startswith("P_extract_") and c != "P_extract_none_named"]:
            ex[X[c].to_numpy() == 1] = c.replace("P_extract_", "")
        tbin = pd.cut(X["T_C"], [0, 250, 300, 350, 700], labels=["<=250", "250-300", "300-350", ">350"]).astype(str)
        for dim, vals in [("family", m["family"].fillna("Unknown")), ("process", m["process"]), ("extraction_solvent", ex),
                          ("temperature_bin", tbin), ("catalyst_present", np.where(X["cat_ratio"] > 0, "yes", "no")),
                          ("yield_basis_daf", np.where(X["P_basis_daf"] == 1, "daf", "dry/other"))]:
            df = pd.DataFrame({"v": np.asarray(vals), "r": p["resid"], "s": p["study"]})
            for v, t in df.groupby("v"):
                out.append(dict(target=target, dimension=dim, level=v, n=len(t), n_studies=t["s"].nunique(),
                                rmse=float(np.sqrt(np.mean(t["r"] ** 2))), bias=float(t["r"].mean()), mae=float(t["r"].abs().mean())))
        # worst studies
        st = p.groupby("study").agg(n=("resid", "size"), bias=("resid", "mean"), rmse=("resid", lambda r: float(np.sqrt(np.mean(r ** 2))))).reset_index()
        raw = read_raw()
        info = raw.groupby("DOI").agg(year=("year", "first"), process=("process_subtype", "first"), basis=("yield_basis", "first"),
                                      separation=("separation_method", "first"), family=("Family_std", "first"))
        st = st.merge(info, left_on="study", right_index=True, how="left").sort_values("rmse", ascending=False)
        st.to_csv(os.path.join(D["results"], f"e8_study_errors_{target}.csv"), index=False)
    pd.DataFrame(out).to_csv(os.path.join(D["results"], "e8_error_analysis.csv"), index=False)
    log.info("error analysis done")


def meta_regression(cfg, D, log, n_perm=1000):
    """RQ3(b): do study-level protocol descriptors predict the study offsets of a base-feature model?
    Ridge regression, leave-one-study-out predictions, R^2; permutation test (offsets shuffled across studies)."""
    from sklearn.linear_model import RidgeCV
    res = []
    for target in ["biooil", "solid"]:
        ds = load_target(target, "dev")
        p = pd.read_csv(os.path.join(D["pred"], f"e3_{target}__base.csv.gz"))
        p["resid"] = p["y"] - p["pred"]
        off = p.groupby("study")["resid"].mean()
        P = ds.X[ds.protocol_features].copy(); P["study"] = ds.groups
        Z = P.groupby("study").mean().loc[off.index]
        Z = Z.fillna(Z.median())
        Zs = ((Z - Z.mean()) / Z.std(ddof=0).replace(0, 1)).to_numpy()
        yv = off.to_numpy()

        def loso_r2(yy):
            pr = np.empty_like(yy)
            for i in range(len(yy)):
                msk = np.arange(len(yy)) != i
                m = RidgeCV(alphas=np.logspace(-2, 3, 20)).fit(Zs[msk], yy[msk]); pr[i] = m.predict(Zs[i:i + 1])[0]
            return 1 - np.sum((yy - pr) ** 2) / np.sum((yy - yy.mean()) ** 2), pr

        r2_obs, pr = loso_r2(yv)
        rng = np.random.default_rng(0)
        null = [loso_r2(rng.permutation(yv))[0] for _ in range(n_perm)]
        pval = (1 + np.sum(np.array(null) >= r2_obs)) / (1 + n_perm)
        coef = RidgeCV(alphas=np.logspace(-2, 3, 20)).fit(Zs, yv)
        res.append(dict(target=target, n_studies=len(yv), offset_sd=float(yv.std()), loso_r2=float(r2_obs), perm_p=float(pval),
                        n_perm=n_perm, null_r2_q95=float(np.quantile(null, 0.95)), ridge_alpha=float(coef.alpha_),
                        coefficients={c: float(v) for c, v in zip(Z.columns, coef.coef_)}))
        log.info(f"meta-regression {target}: LOSO R2={r2_obs:.3f} perm p={pval:.4f}")
    dump(res, os.path.join(D["stats"], "meta_regression.json"))


def run(mode="full", parts=("efficiency", "sensitivity", "error", "meta")):
    cfg, D = load_config(mode), out_dirs(mode)
    log = get_logger("e6_e7_e8", D["logs"])
    learner, _ = choose_base_learner(D)
    if "efficiency" in parts: efficiency(cfg, D, log)
    if "sensitivity" in parts: sensitivity(cfg, D, log, learner)
    if "error" in parts: error_analysis(cfg, D, log)
    if "meta" in parts: meta_regression(cfg, D, log, n_perm=1000 if mode == "full" else 50)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    parts = sys.argv[2].split(",") if len(sys.argv) > 2 else ("efficiency", "sensitivity", "error", "meta")
    run(mode, parts)
