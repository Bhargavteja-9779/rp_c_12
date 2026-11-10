"""E4 robustness + E5 generalisation + the single evaluation on the LOCKED test studies.

E5a locked test     : train on all development studies -> 38 locked studies (run once).
E5b temporal        : development studies published <= cutoff -> studies published > cutoff.
E5c family shift    : leave-one-feedstock-family-out over development studies.
E5d external        : 4TU hydrochar database (HTC, independent compilation) for solid yield.
E4a feature noise   : Gaussian noise (level × training SD) added to continuous test features.
E4b fewer studies   : random subsets of training studies (fractions) within grouped outer folds.
All learners in E5a use their E1-tuned configuration; STRATA uses the protocol-selected learner.
"""
from __future__ import annotations

import os, sys, json
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data.load import load_target, ROOT
from src.evaluation.core import grouped_folds, summary, restore, rmse, r2
from src.models.registry import Learner, available
from src.models.strata import coverage
from src.utils import out_dirs, load_config, get_logger, dump
from experiments.common import choose_base_learner, load_cell, nested_fit, kshot_eval

FS = ["base", "base+P"]


def cols(ds, fs):
    return ds.base_features + (ds.protocol_features if fs == "base+P" else [])


def _strata_eval(learner, params, Xtr, ytr, gtr, Xte, yte, gte, cfg, tag, extra=None):
    nf = nested_fit(learner, params, Xtr, ytr, gtr, Xte, inner_k=cfg["inner_folds"], seed=7, n_jobs=cfg["n_jobs"], alphas=cfg["alphas"])
    rows = []
    for a in cfg["alphas"]:
        for c in ["RC", "SC"]:
            rows.append(dict(tag=tag, alpha=a, calibration=c, **coverage(yte, nf["pred"], nf["q"][a][c], gte), **(extra or {})))
    pred = pd.DataFrame({"y": yte, "pred": nf["pred"], "study": gte})
    return nf, rows, pred


# ---------------------------------------------------------------- E5a locked test
def locked_test(cfg, D, log, learner, pseudo=False):
    """pseudo=True (quick mode): exercise the code path on a development pseudo-split so that the locked
    studies are never looked at before the single final evaluation."""
    out_m, out_c, out_k, preds = [], [], [], []
    for target in ["biooil", "solid"]:
        if pseudo:
            full = load_target(target, "dev")
            tr, tt = grouped_folds(full.groups, k=5, seed=99)[0]
            m_tr = np.zeros(len(full.y), bool); m_tr[tr] = True
            dev, te = full.subset(m_tr), full.subset(~m_tr)
        else:
            dev, te = load_target(target, "dev"), load_target(target, "test")
        dump(te.exclusions, os.path.join(D["results"], f"exclusions_{target}_test.json"))
        for fs in FS:
            for name in cfg["learners"]:
                f = os.path.join(D["logs"], "e1_cells", f"{target}__{fs}__{name}.json")
                if not os.path.exists(f) or not available(name):
                    continue
                params = restore(json.load(open(f))["params"])
                m = Learner(name, params, seed=0, n_jobs=cfg["n_jobs"]).fit(dev.X[cols(dev, fs)], dev.y, dev.groups)
                p = m.predict(te.X[cols(te, fs)])
                out_m.append(dict(target=target, features=fs, learner=name, **summary(te.y, p, te.groups)))
                preds.append(pd.DataFrame({"target": target, "features": fs, "learner": name, "y": te.y, "pred": p, "study": te.groups}))
            params = load_cell(D, target, fs, learner)["params"]
            nf, rows, _ = _strata_eval(learner, params, dev.X[cols(dev, fs)], dev.y, dev.groups, te.X[cols(te, fs)], te.y, te.groups,
                                       cfg, "locked", dict(target=target, features=fs))
            out_c.extend(rows)
            ks = kshot_eval(te.y, nf["pred"], te.groups, nf, cfg["k_values"], cfg["alpha"], cfg["kshot_draws"], min_n=max(cfg["k_values"]) + 1)
            out_k.extend([dict(target=target, features=fs, **r) for r in ks])
            log.info(f"locked {target} {fs} done")
    pd.DataFrame(out_m).to_csv(os.path.join(D["results"], "e5a_locked_test_metrics.csv"), index=False)
    pd.DataFrame(out_c).to_csv(os.path.join(D["results"], "e5a_locked_test_coverage.csv"), index=False)
    pd.DataFrame(out_k).to_csv(os.path.join(D["results"], "e5a_locked_test_kshot.csv"), index=False)
    pd.concat(preds).to_csv(os.path.join(D["pred"], "e5a_locked_test_predictions.csv.gz"), index=False)


# ---------------------------------------------------------------- E5b temporal, E5c family
def temporal_and_family(cfg, D, log, learner):
    rows_m, rows_c = [], []
    for target in ["biooil", "solid"]:
        ds = load_target(target, "dev")
        for fs in FS:
            params = load_cell(D, target, fs, learner)["params"]
            X = ds.X[cols(ds, fs)]
            # temporal
            tr = ds.year <= cfg["temporal_cutoff"]; te = ~tr
            nf, rc, _ = _strata_eval(learner, params, X[tr], ds.y[tr], ds.groups[tr], X[te], ds.y[te], ds.groups[te], cfg, "temporal",
                                     dict(target=target, features=fs, n_train_studies=len(set(ds.groups[tr])), n_test_studies=len(set(ds.groups[te]))))
            rows_c.extend(rc)
            rows_m.append(dict(target=target, features=fs, scheme="temporal", **summary(ds.y[te], nf["pred"], ds.groups[te])))
            # leave-one-family-out (families with >= 3 studies)
            fam = ds.meta["family"].fillna("Unknown").to_numpy()
            fam_ok = [f for f in np.unique(fam) if len(set(ds.groups[fam == f])) >= 3]
            allp = []
            for f in fam_ok:
                te = fam == f; tr = ~te
                nf, rc, pr = _strata_eval(learner, params, X[tr], ds.y[tr], ds.groups[tr], X[te], ds.y[te], ds.groups[te], cfg, "family_out",
                                          dict(target=target, features=fs, family=f))
                rows_c.extend(rc); pr["family"] = f; allp.append(pr)
                rows_m.append(dict(target=target, features=fs, scheme="family_out", family=f, **summary(ds.y[te], nf["pred"], ds.groups[te])))
            log.info(f"temporal/family {target} {fs} done")
    pd.DataFrame(rows_m).to_csv(os.path.join(D["results"], "e5bc_temporal_family_metrics.csv"), index=False)
    pd.DataFrame(rows_c).to_csv(os.path.join(D["results"], "e5bc_temporal_family_coverage.csv"), index=False)


# ---------------------------------------------------------------- E5d external 4TU hydrochar DB
def load_4tu(dev_solid):
    x = pd.read_excel(os.path.join(ROOT, "data", "raw", "htc_4tu", "Full DatabaseX.xlsx"), sheet_name=0)
    x = x[x["Yield_h"].notna()].reset_index(drop=True)
    X = pd.DataFrame(np.nan, index=x.index, columns=dev_solid.X.columns)
    X["feed_C"], X["feed_H"], X["feed_O"], X["feed_N"], X["feed_ash"] = x["C_B"], x["H_B"], x["O_B"], x["N_B"], x["Ash_B"]
    X["T_C"] = x["T"]; X["log_t_min"] = np.log1p(x["RT"])
    X["solid_loading_wt_pct"] = 100 * x["BW"] / (1 + x["BW"])  # BW = biomass:water mass ratio
    for c in [c for c in X.columns if c.startswith(("cat_", "medium_"))]:
        X[c] = 0.0
    X["cat_ratio"] = 0.0; X["gas_pressurised"] = 0.0; X["proc_solvothermal"] = 0.0; X["proc_HTC"] = 1.0
    # pseudo-studies: identical feedstock composition = one feedstock series (no study IDs in this DB)
    g = x[["C_B", "H_B", "N_B", "O_B", "Ash_B"]].round(2).astype(str).agg("|".join, axis=1).to_numpy()
    return X, x["Yield_h"].to_numpy(float), g, x


def overlap_audit(Xext, yext, dev_all):
    """Rows of the external DB that coincide (feedstock C/H/O + T + time + yield within rounding) with any
    row of the primary DB (dev or test) are treated as potential duplicates and removed."""
    key = lambda C, H, O, T, t, y: (np.round(C, 0), np.round(H, 0), np.round(O, 0), np.round(T, -1), np.round(t, 1), np.round(y, 0))
    prim = set(zip(*key(dev_all["C_feed_wt_pct"], dev_all["H_feed_wt_pct"], dev_all["O_feed_wt_pct"], dev_all["T_reaction_C"],
                       np.log1p(dev_all["t_residence_min"].clip(lower=0)), dev_all["Yield_char_wt_pct"])))
    ext = list(zip(*key(Xext["feed_C"], Xext["feed_H"], Xext["feed_O"], Xext["T_C"], Xext["log_t_min"], yext)))
    return np.array([k in prim for k in ext])


def external(cfg, D, log, learner):
    from src.data.load import read_raw
    dev = load_target("solid", "dev")
    Xe, ye, ge, raw = load_4tu(dev)
    dup = overlap_audit(Xe, ye, read_raw())
    dump(dict(external_rows=int(len(ye)), potential_duplicates_removed=int(dup.sum()), pseudo_studies=int(len(set(ge[~dup])))),
         os.path.join(D["results"], "e5d_external_overlap_audit.json"))
    Xe, ye, ge = Xe[~dup], ye[~dup], ge[~dup]
    rows_m, rows_c = [], []
    params = load_cell(D, "solid", "base", learner)["params"]
    X = dev.X[dev.base_features]
    nf, rc, pr = _strata_eval(learner, params, X, dev.y, dev.groups, Xe[dev.base_features], ye, ge, cfg, "external_4TU", dict(target="solid", features="base"))
    rows_c.extend(rc)
    rows_m.append(dict(target="solid", features="base", scheme="external_4TU_all_dev_processes", **summary(ye, nf["pred"], ge)))
    htc = dev.X["proc_HTC"].to_numpy() == 1
    nf2, rc2, _ = _strata_eval(learner, params, X[htc], dev.y[htc], dev.groups[htc], Xe[dev.base_features], ye, ge, cfg, "external_4TU_HTCtrain",
                               dict(target="solid", features="base"))
    rows_c.extend(rc2)
    rows_m.append(dict(target="solid", features="base", scheme="external_4TU_HTC_dev_only", n_train=int(htc.sum()),
                       n_train_studies=int(len(set(dev.groups[htc]))), **summary(ye, nf2["pred"], ge)))
    pr.to_csv(os.path.join(D["pred"], "e5d_external_predictions.csv.gz"), index=False)
    pd.DataFrame(rows_m).to_csv(os.path.join(D["results"], "e5d_external_metrics.csv"), index=False)
    pd.DataFrame(rows_c).to_csv(os.path.join(D["results"], "e5d_external_coverage.csv"), index=False)
    log.info("external done")


# ---------------------------------------------------------------- E4 robustness
def robustness(cfg, D, log, learner):
    rows = []
    for target in ["biooil", "solid"]:
        ds = load_target(target, "dev")
        for fs in FS:
            params = load_cell(D, target, fs, learner)["params"]
            X = ds.X[cols(ds, fs)]
            cont = [c for c in X.columns if X[c].nunique() > 2]
            seed = cfg["outer_seeds"][0]
            for fi, (tr, te) in enumerate(grouped_folds(ds.groups, k=cfg["outer_folds"], seed=seed)):
                rng = np.random.default_rng(fi)
                for frac in cfg["study_fractions"]:
                    st = np.unique(ds.groups[tr])
                    keep = set(rng.choice(st, size=max(5, int(round(frac * len(st)))), replace=False)) if frac < 1 else set(st)
                    trs = tr[np.isin(ds.groups[tr], list(keep))]
                    nf = nested_fit(learner, params, X.iloc[trs], ds.y[trs], ds.groups[trs], X.iloc[te], inner_k=cfg["inner_folds"],
                                    seed=fi, n_jobs=cfg["n_jobs"], alphas=[cfg["alpha"]])
                    if frac == 1.0:
                        sd = X.iloc[trs][cont].std()
                        for lv in cfg["noise_levels"]:
                            Xn = X.iloc[te].copy()
                            nrng = np.random.default_rng(1000 + fi)
                            Xn[cont] = Xn[cont] + nrng.normal(0, 1, Xn[cont].shape) * (lv * sd.to_numpy())
                            p = nf["model"].predict(Xn)
                            for c in ["RC", "SC"]:
                                cv = coverage(ds.y[te], p, nf["q"][cfg["alpha"]][c], ds.groups[te])
                                rows.append(dict(target=target, features=fs, experiment="feature_noise", level=lv, fold=fi, calibration=c,
                                                 rmse=rmse(ds.y[te], p), **cv))
                    for c in ["RC", "SC"]:
                        cv = coverage(ds.y[te], nf["pred"], nf["q"][cfg["alpha"]][c], ds.groups[te])
                        rows.append(dict(target=target, features=fs, experiment="training_studies", level=frac, fold=fi, calibration=c,
                                         n_train_studies=len(keep), rmse=rmse(ds.y[te], nf["pred"]), **cv))
            log.info(f"robustness {target} {fs} done")
    pd.DataFrame(rows).to_csv(os.path.join(D["results"], "e4_robustness.csv"), index=False)


def run(mode="full", parts=("robustness", "temporal_family", "external", "locked")):
    cfg, D = load_config(mode), out_dirs(mode)
    log = get_logger("e5_generalization", D["logs"])
    learner, _ = choose_base_learner(D)
    if "robustness" in parts: robustness(cfg, D, log, learner)
    if "temporal_family" in parts: temporal_and_family(cfg, D, log, learner)
    if "external" in parts: external(cfg, D, log, learner)
    if "locked" in parts: locked_test(cfg, D, log, learner, pseudo=(mode != "full"))


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    parts = sys.argv[2].split(",") if len(sys.argv) > 2 else ("robustness", "temporal_family", "external", "locked")
    run(mode, parts)
