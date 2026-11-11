"""Every number that appears in the manuscript text is computed here from generated result files."""
from __future__ import annotations

import json, os, statistics
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
R = os.path.join(REPO, "results")
LBL = {"mean": "mean predictor", "ridge": "ridge regression", "knn": "k-nearest neighbours", "svr": "SVR", "mlp": "MLP",
       "rf": "random forest", "et": "extra trees", "hgb": "histogram gradient boosting", "lgbm": "LightGBM", "xgb": "XGBoost",
       "cat": "CatBoost", "gpboost": "GPBoost"}


def f1(x): return f"{x:.1f}"
def f2(x): return f"{x:.2f}"
def f3(x): return f"{x:.3f}"
def pfmt(p): return "< 0.001" if p < 0.001 else f"= {p:.3f}"


def compute() -> dict:
    v = {}
    # ---------------- literature corpus
    c = json.load(open(os.path.join(REPO, "supplementary", "literature", "pubmed_ml_hydrothermal_corpus.json")))["records"]
    prim = [r for r in c if not r["review"]]
    v["lit_n_primary"] = len(prim)
    v["lit_n_biortech"] = sum(r["journal"] == "Bioresour Technol" for r in prim)
    m = pd.read_csv(os.path.join(REPO, "supplementary", "literature", "literature_matrix_corpus.csv"))
    best = [max(map(float, s.split(";"))) for s in m["reported_R2"] if s != "n.s."]
    v["lit_median_r2"] = f2(statistics.median(best)); v["lit_n_r2"] = len(best)
    v["lit_n_grouped"] = int(sum(r["group_split"] for r in prim)); v["lit_n_uq"] = int(sum(r["uncertainty"] for r in prim))
    S = json.load(open(os.path.join(R, "statistics.json"))); M = json.load(open(os.path.join(R, "metrics.json")))
    ext = M.get("e5d_external_overlap_audit", {})
    v["ext_dups"] = ext.get("potential_duplicates_removed", "n/a"); v["ext_rows"] = ext.get("external_rows", "n/a")
    v["ext_pseudo"] = ext.get("pseudo_studies", "n/a")
    learner = M["strata_base_learner"]["learner"]; v["strata_learner_label"] = LBL[learner]; v["_learner"] = learner
    # ---------------- data
    for t in ["biooil", "solid"]:
        for sp in ["dev", "test"]:
            e = M.get(f"exclusions_{t}_{sp}")
            if e:
                v[f"n_{t}_{sp}"] = f"{e['rows_final']:,}"; v[f"s_{t}_{sp}"] = e["studies_final"]
    # ---------------- E1
    w = pd.DataFrame(M["e1"])
    for t in ["biooil", "solid"]:
        b = w[(w.target == t) & (w.features == "base")]
        bb = b.sort_values("rmse_grouped_study_cv").iloc[0]
        br = b.sort_values("rmse_random_row_cv").iloc[0]
        nontriv = b[~b.learner.isin(["mean"])]
        v[f"{t}_best_grouped_learner"] = LBL[bb.learner]
        v[f"{t}_best_grouped_rmse"] = f1(bb.rmse_grouped_study_cv); v[f"{t}_best_grouped_r2"] = f2(bb.r2_grouped_study_cv)
        v[f"{t}_best_random_learner"] = LBL[br.learner]
        v[f"{t}_best_random_rmse"] = f1(br.rmse_random_row_cv); v[f"{t}_best_random_r2"] = f2(br.r2_random_row_cv)
        v[f"{t}_ratio_min"] = f2(nontriv.optimism_ratio_rmse.min()); v[f"{t}_ratio_max"] = f2(nontriv.optimism_ratio_rmse.max())
        v[f"{t}_ratio_median"] = f2(nontriv.optimism_ratio_rmse.median())
        v[f"{t}_mean_rmse"] = f1(b[b.learner == "mean"].rmse_grouped_study_cv.iloc[0])
        v[f"{t}_r2_random_max"] = f2(nontriv.r2_random_row_cv.max()); v[f"{t}_r2_grouped_max"] = f2(nontriv.r2_grouped_study_cv.max())
        sl = b[b.learner == learner].iloc[0]
        v[f"{t}_strata_random_rmse"] = f1(sl.rmse_random_row_cv); v[f"{t}_strata_grouped_rmse"] = f1(sl.rmse_grouped_study_cv)
        v[f"{t}_strata_random_r2"] = f2(sl.r2_random_row_cv); v[f"{t}_strata_grouped_r2"] = f2(sl.r2_grouped_study_cv)
        v[f"{t}_strata_ratio"] = f2(sl.optimism_ratio_rmse)
        for ln in ["mlp", "gpboost", "ridge"]:
            r = b[b.learner == ln]
            if len(r):
                v[f"{t}_{ln}_grouped_rmse"] = f1(r.rmse_grouped_study_cv.iloc[0]); v[f"{t}_{ln}_random_rmse"] = f1(r.rmse_random_row_cv.iloc[0])
        pt = pd.DataFrame(S["e1_paired_tests"]); pt = pt[(pt.target == t) & (pt.features == "base")]
        v[f"{t}_n_learners_not_sig_vs_best"] = int((pt.p_holm >= 0.05).sum()); v[f"{t}_best_ref"] = LBL[pt.reference.iloc[0]]
        v[f"{t}_not_sig_list"] = ", ".join(LBL[x] for x in pt[pt.p_holm >= 0.05].learner)
    # ---------------- E3
    for t in ["biooil", "solid"]:
        e = S["e3"][t]
        h = e["heterogeneity"]["base"]; hp = e["heterogeneity"]["base+P"]
        v[f"{t}_share"] = f2(h["share_between"]); v[f"{t}_share_lo"] = f2(h["share_ci"][0]); v[f"{t}_share_hi"] = f2(h["share_ci"][1])
        v[f"{t}_tau"] = f1(np.sqrt(h["tau2"])); v[f"{t}_sigw"] = f1(np.sqrt(h["sigma2_w"]))
        v[f"{t}_share_P"] = f2(hp["share_between"]); v[f"{t}_tau_P"] = f1(np.sqrt(hp["tau2"]))
        pa = e["protocol_ablation"]; tt = pa["test_one_sided_base_plus_P_less"]
        v[f"{t}_P_med_base"] = f2(pa["median_study_rmse_base"]); v[f"{t}_P_med_baseP"] = f2(pa["median_study_rmse_baseP"])
        v[f"{t}_P_diff"] = f2(tt["median_diff"]); v[f"{t}_P_lo"] = f2(tt["ci_low"]); v[f"{t}_P_hi"] = f2(tt["ci_high"])
        v[f"{t}_P_p"] = pfmt(tt["p"]); v[f"{t}_P_rb"] = f2(tt["rank_biserial"]); v[f"{t}_P_n"] = tt["n"]
        v[f"{t}_P_pooled_base"] = f2(pa["pooled_rmse"]["base"]); v[f"{t}_P_pooled_baseP"] = f2(pa["pooled_rmse"]["baseP"])
        cv = pd.DataFrame(e["coverage"])
        for fs, tag in [("base+P", ""), ("base", "_b")]:
            for cal in ["RC", "SC"]:
                r = cv[(cv.features == fs) & (cv.calibration == cal) & (cv.alpha == 0.1)].iloc[0]
                v[f"{t}_cov_{cal}{tag}"] = f2(r.coverage_studies); v[f"{t}_covrows_{cal}{tag}"] = f2(r.coverage_rows)
                v[f"{t}_width_{cal}{tag}"] = f1(r.width); v[f"{t}_below80_{cal}{tag}"] = f"{100 * r.frac_studies_below_0_8:.0f}"
                v[f"{t}_cov_{cal}_lo{tag}"] = f2(r.coverage_studies_ci_seed1[0]); v[f"{t}_cov_{cal}_hi{tag}"] = f2(r.coverage_studies_ci_seed1[1])
        for al in [0.05, 0.2]:
            for cal in ["RC", "SC"]:
                r = cv[(cv.features == "base+P") & (cv.calibration == cal) & (cv.alpha == al)]
                if len(r):
                    v[f"{t}_cov_{cal}_a{int(al*100)}"] = f2(r.iloc[0].coverage_studies)
        ct = e["coverage_test_SC_vs_RC"]; v[f"{t}_covtest_p"] = pfmt(ct["p"]); v[f"{t}_covtest_diff"] = f2(ct["median_diff"])
        ks = pd.DataFrame(e["kshot_summary"]); ks = ks[ks.features == "base+P"]
        for _, r in ks.iterrows():
            key = f"{t}_k{int(r.k)}_{r['mode']}"
            v[key + "_rmse"] = f2(r.median_study_rmse); v[key + "_cov"] = f2(r.coverage_studies); v[key + "_width"] = f1(r.width)
            v[f"{t}_k_nstudies"] = int(r.n_studies)
        kt = pd.DataFrame(e["kshot_tests"]); kt = kt[kt.features == "base+P"]
        for _, r in kt.iterrows():
            v[f"{t}_kt_{r.comparison}_{int(r.k)}_p"] = pfmt(r.p_holm); v[f"{t}_kt_{r.comparison}_{int(r.k)}_d"] = f2(r.median_diff)
        v[f"{t}_lam_median"] = f2(e["inner_lambda"]["base+P"]["median"])
    # ---------------- meta-regression
    for mr in S.get("meta_regression", []):
        t = mr["target"]; v[f"{t}_mr_r2"] = f3(mr["loso_r2"]); v[f"{t}_mr_p"] = pfmt(mr["perm_p"]); v[f"{t}_mr_n"] = mr["n_studies"]
        v[f"{t}_offset_sd"] = f1(mr["offset_sd"])
        co = sorted(mr["coefficients"].items(), key=lambda kv: -abs(kv[1]))[:3]
        v[f"{t}_mr_top"] = ", ".join(f"{k.replace('P_', '').replace('_', ' ')} ({c:+.1f})" for k, c in co)
    return v


if __name__ == "__main__":
    for k, x in compute().items():
        print(k, "=", x)
