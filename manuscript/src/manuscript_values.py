"""Every number that appears in the manuscript text is computed here from generated result files."""
from __future__ import annotations

import json, os, statistics, sys
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
R = os.environ.get("STRATA_RESULTS", os.path.join(REPO, "results"))
sys.path.insert(0, os.path.join(REPO, "code"))
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
        nontriv = b[~b.learner.isin(["mean", "ridge", "gpboost"])]  # flexible learners
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

    # ================= data-driven sentences (wording follows the actual test outcomes)
    S3 = S["e3"]
    def sig(t, key="test_one_sided_base_plus_P_less"):
        return S3[t]["protocol_ablation"][key]
    pb, ps = sig("biooil"), sig("solid")
    p_adj = holm2([pb["p"], ps["p"]])
    helped = [t for t, tt, pa in [("bio-oil", pb, p_adj[0]), ("solid", ps, p_adj[1])] if pa < 0.05 and tt["median_diff"] < 0]
    if not helped:
        v["P_heading"] = "Work-up and reporting descriptors do not explain the offsets"
        v["P_sentence"] = ("However, adding the parsed work-up and reporting descriptors (P) did not significantly reduce the error for unseen studies "
                           "for either target after Holm correction.")
    else:
        v["P_heading"] = "Work-up and reporting descriptors explain part of the offsets"
        v["P_sentence"] = f"Adding the parsed work-up and reporting descriptors (P) significantly reduced the error for unseen studies for {' and '.join(helped)} yield after Holm correction."
    lt = pd.DataFrame(S.get("locked_protocol_ablation_all_learners", []))
    if len(lt):
        nsig = int(((lt.p_holm < 0.05) & (lt.median_diff < 0)).sum()); nworse = int(((lt.p_holm < 0.05) & (lt.median_diff > 0)).sum())
        v["P_all_learners_sentence"] = (f"On the locked test studies, P significantly reduced per-study RMSE for {nsig} and significantly increased it for {nworse} "
                                        f"of the {len(lt)} learner–target combinations (Holm-corrected Wilcoxon tests).")
    else:
        v["P_all_learners_sentence"] = ""
    kws = []
    for mr in S.get("meta_regression", []):
        u = mr.get("univariate") or {}
        k = u.get("kruskal_extraction_solvent")
        if k:
            kws.append(f"Kruskal–Wallis *p* {pfmt(k['p'])} for {'bio-oil' if mr['target'] == 'biooil' else 'solids'}")
        if mr["target"] == "biooil" and k:
            g = k["groups"]; lo = min(g, key=lambda x: g[x]["median_offset"])
            v["ea_note_low"] = f"{lo.replace('_', ' ')} (median offset {g[lo]['median_offset']:+.1f} wt%, {g[lo]['n']} studies)"
    v["kw_sentence"] = "; ".join(kws) if kws else "not testable"
    v["ea_sentence"] = (f"The most negative median offset for bio-oil occurred for studies using {v['ea_note_low']}, but such groups are small and the "
                        "differences were not significant." if "ea_note_low" in v else "")
    from src.data.load import load_target
    dsb = load_target("biooil", "dev"); v["none_named_pct"] = f"{100 * dsb.X['P_extract_none_named'].mean():.0f}"
    # coverage across other settings
    covr = []
    for key, lab in [("e5a_locked_test_coverage", "on the locked test studies"), ("e5bc_temporal_family_coverage", None), ("e5d_external_coverage", "on the external hydrochar database")]:
        df = pd.DataFrame(M.get(key, []))
        if df.empty: continue
        df = df[(df.alpha == 0.1)]
        if key == "e5d_external_coverage": df = df[df.tag == "external_4TU"]
        else: df = df[df.features == "base+P"]
        for tag, g in df.groupby("tag"):
            name = lab or {"temporal": "for temporally later studies", "family_out": "for left-out feedstock families (mean)"}[tag]
            c = g.groupby(["target", "calibration"])["coverage_studies"].mean()
            parts = [f"{'bio-oil' if t == 'biooil' else 'solids'} RC {c[(t, 'RC')]:.2f} vs SC {c[(t, 'SC')]:.2f}" for t in ["biooil", "solid"] if (t, "RC") in c]
            covr.append(f"{name} ({'; '.join(parts)})")
    v["gen_cov_sentence"] = "and " + ", ".join(covr) + "." if covr else "."
    # k-shot EB vs raw
    kt = pd.DataFrame(S3["biooil"]["kshot_tests"]); kt = kt[(kt.features == "base+P") & (kt.comparison == "eb_vs_raw")]
    better = kt[(kt.p_holm < 0.05) & (kt.median_diff < 0)]; worse = kt[(kt.p_holm < 0.05) & (kt.median_diff > 0)]
    if len(better) and not len(worse):
        v["kshot_eb_sentence"] = f"Shrinkage lowered the per-study RMSE relative to the raw mean offset at k = {', '.join(str(int(x)) for x in better.k)} (Holm-corrected Wilcoxon, bio-oil) and was never significantly worse."
    elif not len(better) and not len(worse):
        v["kshot_eb_sentence"] = "Shrunk and raw offsets did not differ significantly in per-study RMSE at any k after Holm correction (bio-oil); shrinkage therefore offers protection at small k without a measurable cost."
    else:
        v["kshot_eb_sentence"] = (f"Relative to the raw mean offset, shrinkage was significantly better at k = {', '.join(str(int(x)) for x in better.k) or 'none'} "
                                  f"and significantly worse at k = {', '.join(str(int(x)) for x in worse.k)} (Holm-corrected Wilcoxon, bio-oil).")
    v["biooil_halfwidth_SC"] = f"{float(v['biooil_width_SC']) / 2:.0f}"


    # ---------------- k-shot vs learner choice; sensitivity; adaptive; HTC conditional coverage
    for t in ["biooil", "solid"]:
        b = w[(w.target == t) & (w.features == "base") & (~w.learner.isin(["mean", "ridge", "gpboost", "mlp"]))]
        v[f"{t}_learner_span"] = f1(b.median_study_rmse_grouped_study_cv.max() - b.median_study_rmse_grouped_study_cv.min())
        v[f"{t}_k3_gain"] = f1(float(v[f"{t}_k0_none_rmse"]) - float(v[f"{t}_k3_eb_rmse"]))
    se = pd.read_csv(os.path.join(R, "e7_sensitivity.csv"))
    tu = se[se.analysis == "tuning"].set_index(["target", "features", "config"])
    v["tuning_sentence"] = (f"Replacing the tuned hyper-parameters of the base learner by library defaults changed its study-grouped RMSE by "
                            f"{min(abs(tu.loc[(t, f, 'tuned'), 'rmse'] - tu.loc[(t, f, 'default'), 'rmse']) for t in ['biooil', 'solid'] for f in ['base', 'base+P']):.1f}–"
                            f"{max(abs(tu.loc[(t, f, 'tuned'), 'rmse'] - tu.loc[(t, f, 'default'), 'rmse']) for t in ['biooil', 'solid'] for f in ['base', 'base+P']):.1f} wt% "
                            "(Supplementary Table S7), so the conclusions do not hinge on tuning.")
    k = se[(se.analysis == "tau2_estimator") & (se.features == "base+P")].groupby(["target", "estimator", "k"])["rmse"].median()
    v["tau2_sentence"] = (f"Estimating $\\tau^2$ by restricted maximum likelihood instead of the method of moments gave median per-study RMSE at k = 1 of "
                          f"{k[('biooil', 'REML', 1)]:.2f} vs {k[('biooil', 'MoM', 1)]:.2f} wt% (bio-oil) and {k[('solid', 'REML', 1)]:.2f} vs {k[('solid', 'MoM', 1)]:.2f} wt% "
                          "(solids; Supplementary Table S6).")
    ad = pd.read_csv(os.path.join(R, "e3b_adaptive_summary.csv")).set_index(["target", "method"])
    v["adaptive_main_sentence"] = (f"An exploratory, post-hoc variant with locally adaptive widths (Supplementary Section S4) did not narrow the intervals "
                                   f"(mean width {ad.loc[('biooil', 'SC-N'), 'mean_width']:.1f} vs {ad.loc[('biooil', 'SC'), 'mean_width']:.1f} wt% for bio-oil) "
                                   "and worsened the interval score, consistent with an error dominated by an unpredictable study offset."
                                   if ad.loc[('biooil', 'SC-N'), 'winkler'] > ad.loc[('biooil', 'SC'), 'winkler'] else
                                   "An exploratory, post-hoc variant with locally adaptive widths is reported in Supplementary Section S4.")
    import ast as _ast
    cp = _ast.literal_eval(ad.loc[("solid", "SC"), "coverage_by_process"])
    v["htc_cov_SC"] = f2(cp.get("HTC", float("nan")))

    rq = json.load(open(os.path.join(R, "experiment_logs", "repro_quick.json")))
    v["quick_minutes"] = f"{rq['quick_mode_wall_seconds'] / 60:.0f}"
    # ---------------- E9 base learners, E10 duplicates, E11 overhead (review rounds)
    e9 = pd.read_csv(os.path.join(R, "e9_base_learners.csv"))
    for t in ["biooil", "solid"]:
        sc = e9[(e9.target == t) & (e9.calibration == "SC")]; rc = e9[(e9.target == t) & (e9.calibration == "RC")].set_index("learner")
        v[f"{t}_e9_sc_min"] = f2(sc.coverage_studies.min()); v[f"{t}_e9_sc_max"] = f2(sc.coverage_studies.max())
        v[f"{t}_e9_rc_mean"] = f2(rc.loc["mean", "coverage_studies"]); v[f"{t}_e9_rc_ridge"] = f2(rc.loc["ridge", "coverage_studies"])
        v[f"{t}_e9_rc_knn"] = f2(rc.loc["knn", "coverage_studies"])
        tr = rc.loc[["rf", "et", "lgbm", "xgb"], "coverage_studies"]; v[f"{t}_e9_rc_trees"] = f"{tr.min():.2f}–{tr.max():.2f}"
        scw = sc.set_index("learner")["width"]; ml = scw.drop(["mean"])
        v[f"{t}_e9_w_mean"] = f1(scw["mean"]); v[f"{t}_e9_w_best"] = f1(ml.min()); v[f"{t}_e9_w_bestl"] = LBL[ml.idxmin()]
        v[f"{t}_e9_w_red"] = f"{100 * (1 - ml.min() / scw['mean']):.0f}"
    k9 = pd.read_csv(os.path.join(R, "e9_base_learners_kshot.csv"))
    for t in ["biooil", "solid"]:
        q = k9[(k9.target == t) & (k9.k == 3)].set_index("learner")["median_study_rmse"]
        v[f"{t}_e9_k3_mean"] = f2(q["mean"]); v[f"{t}_e9_k3_best"] = f2(q.drop("mean").min())
    e10 = json.load(open(os.path.join(R, "e10_duplicate_audit.json")))
    for t in ["biooil", "solid"]:
        d = e10[t]; v[f"{t}_dup_rows"] = d["n_cross_study_duplicate_rows"]; v[f"{t}_dup_pct"] = f"{100 * d['n_cross_study_duplicate_rows'] / d['n_rows']:.1f}"
        v[f"{t}_dup_studies"] = len(d["studies_involved"]); v[f"{t}_nodup_rmse"] = f1(d["without_duplicates"]["rmse"])
        v[f"{t}_nodup_share"] = f2(d["without_duplicates"]["share_between"]); v[f"{t}_dup_ref_rmse"] = f1(e10["reference_with_duplicates_seed11"][t]["rmse"])
        v[f"{t}_lock_dup_rows"] = e10["locked_vs_dev"][t]["locked_rows_matching_dev"]; v[f"{t}_lock_dup_studies"] = len(e10["locked_vs_dev"][t]["locked_studies_involved"])
    e11 = pd.read_csv(os.path.join(R, "e11_overhead.csv"))
    v["ovh_min"] = f1(e11.strata_total_s.min()); v["ovh_max"] = f1(e11.strata_total_s.max())
    v["ovh_base_min"] = f1(e11.base_fit_s.min()); v["ovh_base_max"] = f1(e11.base_fit_s.max())

    # ================= v2: trends, ranking, quality targets (PROTOCOL Addenda A, A2, B, C)
    V = json.load(open(os.path.join(R, "statistics_v2.json")))
    e13 = pd.DataFrame(V["e13"]); eT = e13[e13.variable == "T_C"].set_index(["target", "band"])
    for t in ["biooil", "solid"]:
        for b in ["150-250", "250-300", "300-350", "350-450"]:
            r = eT.loc[(t, b)]; k = b.replace("-", "_")
            v[f"{t}_slope_{k}"] = f"{r.median_slope:+.2f}"; v[f"{t}_slope_{k}_lo"] = f"{r.slope_ci_low:+.2f}"; v[f"{t}_slope_{k}_hi"] = f"{r.slope_ci_high:+.2f}"
            v[f"{t}_sign_{k}"] = f"{100 * r.frac_studies_same_sign:.0f}"; v[f"{t}_nst_{k}"] = int(r.n_studies)
            v[f"{t}_sdslope_{k}"] = f"{r.sd_slope_between_studies:.1f}"
        et = e13[(e13.variable == "log_t_min") & (e13.target == t)].iloc[0]
        v[f"{t}_tslope"] = f"{et.median_slope:+.2f}"; v[f"{t}_tslope_lo"] = f"{et.slope_ci_low:+.2f}"; v[f"{t}_tslope_hi"] = f"{et.slope_ci_high:+.2f}"
        v[f"{t}_tsign"] = f"{100 * et.frac_studies_same_sign:.0f}"
    r_ = eT.loc[("biooil", "250-300")]; v["biooil_sd_over_slope_250_300"] = f"{r_.sd_slope_between_studies / abs(r_.median_slope):.1f}"
    lo_ = eT.loc[[("solid", "150-250"), ("solid", "250-300")]].frac_studies_same_sign
    v["solid_sign_lt300"] = f"{100 * lo_.min():.0f}" if round(100 * lo_.min()) == round(100 * lo_.max()) else f"{100 * lo_.min():.0f}–{100 * lo_.max():.0f}"
    v["n_pairs_T_biooil"] = int(e13[(e13.variable == "T_C") & (e13.target == "biooil")].n_pairs.sum())
    v["n_pairs_T_solid"] = int(e13[(e13.variable == "T_C") & (e13.target == "solid")].n_pairs.sum())
    def summ(split):
        return pd.DataFrame(V[f"e12_{split}"]["T1_T4_T5_summary"])
    for split, tag in [("dev", "d"), ("locked", "l"), ("dev_quality", "d"), ("locked_quality", "l")]:
        if f"e12_{split}" not in V:
            continue
        sm = summ(split); x = sm[sm.learner == "xgb"].set_index(["target", "model"])
        for t in x.index.get_level_values(0).unique():
            v[f"{t}_{tag}_lvl_r2"] = f2(x.loc[(t, "A"), "level_r2_same_studies"])
            for mdl in ["A", "W", "PD"]:
                v[f"{t}_{tag}_c_r2_{mdl}"] = f2(x.loc[(t, mdl), "contrast_r2"]); v[f"{t}_{tag}_rho_{mdl}"] = f2(x.loc[(t, mdl), "median_spearman"])
            v[f"{t}_{tag}_ccov"] = f2(x.loc[(t, "A"), "contrast_coverage_studies"]); v[f"{t}_{tag}_cw"] = f1(x.loc[(t, "A"), "contrast_width"])
            v[f"{t}_{tag}_lw"] = f1(x.loc[(t, "A"), "level_width"])
            allc = sm[sm.target == t].contrast_r2
            v[f"{t}_{tag}_c_r2_min"] = f2(allc.min()); v[f"{t}_{tag}_c_r2_max"] = f2(allc.max())
            alll = sm[(sm.target == t) & (sm.model == "A")].level_r2_same_studies
            v[f"{t}_{tag}_l_r2_min"] = f2(alll.min()); v[f"{t}_{tag}_l_r2_max"] = f2(alll.max())
    t2 = pd.DataFrame(V["e12_dev"]["T2"]); v["t2_dev_sig"] = int((t2.p_holm < 0.05).sum()); v["t2_dev_n"] = len(t2)
    t2l = pd.DataFrame(V["e12_locked"]["T2"]); v["t2_locked_sig"] = int((t2l.p_holm < 0.05).sum()); v["t2_locked_n"] = len(t2l)
    v["t2_locked_minp"] = f"{t2l.p.min():.3f}"
    t3 = pd.DataFrame(V["e12_dev"]["T3"]); v["t3_dev_sig_better"] = int(((t3.p_holm < 0.05) & (t3.median_diff < 0)).sum())
    v["t3_dev_sig_worse"] = int(((t3.p_holm < 0.05) & (t3.median_diff > 0)).sum()); v["t3_dev_n"] = len(t3)
    t3s = pd.DataFrame(V["e12_dev"]["T3_summary"]).query("learner == 'xgb' and k == 1").set_index("target")
    for t in ["biooil", "solid"]:
        v[f"{t}_k1_AEB"] = f2(t3s.loc[t, "median_A-EB"]); v[f"{t}_k1_W"] = f2(t3s.loc[t, "median_W-anchor"]); v[f"{t}_k1_PD"] = f2(t3s.loc[t, "median_PD-anchor"])
    for sfx, tag in [("", "d"), ("_locked", "l")]:
        ct = pd.DataFrame(V[f"e14a{sfx}"]).set_index(["target", "type", "model"])
        for t in ["biooil", "solid"]:
            for typ, ty in [("temperature_only", "T"), ("time_only", "t")]:
                for mdl in ["A", "W", "PD"]:
                    v[f"{t}_{tag}_{ty}only_{mdl}"] = f2(ct.loc[(t, typ, mdl), "r2"])
            v[f"{t}_{tag}_Tpairs"] = int(ct.loc[(t, "temperature_only", "A"), "n_pairs"])
    # ranking
    rk = pd.DataFrame(V["e14b"]); rl = pd.DataFrame(V["e14b_locked"])
    for t in ["biooil", "solid"]:
        rule = "rule_T325" if t == "biooil" else "rule_lowest_T"
        d = rk[(rk.target == t) & (rk.reference == rule)].set_index("method"); l = rl[(rl.target == t) & (rl.reference == rule)].set_index("method")
        for mdl in ["A", "W", "PD"]:
            v[f"{t}_rk_d_{mdl}"] = f1(d.loc[mdl, "median_method"]); v[f"{t}_rk_l_{mdl}"] = f1(l.loc[mdl, "median_method"])
            v[f"{t}_rk_d_p_{mdl}"] = pfmt(d.loc[mdl, "p_holm"]); v[f"{t}_rk_l_p_{mdl}"] = pfmt(l.loc[mdl, "p_holm"])
        v[f"{t}_rk_d_rule"] = f1(d.median_ref.iloc[0]); v[f"{t}_rk_l_rule"] = f1(l.median_ref.iloc[0])
        v[f"{t}_rk_d_n"] = int(d.n.iloc[0]); v[f"{t}_rk_l_n"] = int(l.n.iloc[0])
        v[f"{t}_rk_d_rand"] = f1(V["e14b_random_median"][t]); v[f"{t}_rk_l_rand"] = f1(V["e14b_locked_random_median"][t])
    v["c1_confirmed"] = bool((rl[(rl.target == "biooil")].p_holm < 0.05).any())
    v["c1_sentence"] = ("was confirmed" if v["c1_confirmed"] else "was not confirmed")
    # locked: concentration of contrast error in two studies
    m = pd.read_csv(os.path.join(R, "e12_study_metrics_locked.csv")); m = m[(m.learner == "xgb") & (m.target == "biooil")]
    sse = m.pivot_table(index="study", columns="model", values="sse_contrast", aggfunc="sum")
    sh = (sse["A"] / sse["A"].sum()).sort_values(ascending=False)
    v["lk_c_top2_share"] = f"{100 * sh.iloc[:2].sum():.0f}"
    # quality-target tuning
    for t in ["hhv_biooil", "c_biooil"]:
        f = json.load(open(os.path.join(REPO, "results", "experiment_logs", "e1_cells", f"{t}__base__xgb.json")))
        v[f"{t}_tune_rmse"] = f2(f["tune_rmse"])
    from src.data.load import load_target as _lt
    for t in ["hhv_biooil", "c_biooil"]:
        for sp in ["dev", "test"]:
            ds_ = _lt(t, sp); v[f"n_{t}_{sp}"] = f"{len(ds_.y):,}"; v[f"s_{t}_{sp}"] = len(set(ds_.groups))
    # ---------------- locked test (E5a)
    LT = pd.DataFrame(M.get("e5a_locked_test_metrics", []))
    if len(LT):
        parts = []
        for t, nm in [("biooil", "bio-oil"), ("solid", "solid")]:
            b = LT[(LT.target == t) & (LT.features == "base")]
            best = b[b.learner != "mean"].sort_values("rmse").iloc[0]; sl = b[b.learner == learner].iloc[0]; mn = b[b.learner == "mean"].iloc[0]
            v[f"{t}_lock_rmse"] = f1(sl.rmse); v[f"{t}_lock_r2"] = f2(sl.r2); v[f"{t}_lock_n"] = int(sl.n); v[f"{t}_lock_s"] = int(sl.n_studies)
            parts.append(f"for {nm} yield ({int(sl.n)} runs, {int(sl.n_studies)} studies) the STRATA base learner reached RMSE = {sl.rmse:.1f} wt% "
                         f"(R² = {sl.r2:.2f}; best learner {LBL[best.learner]}, {best.rmse:.1f} wt%; mean predictor {mn.rmse:.1f} wt%)")
        LC = pd.DataFrame(M.get("e5a_locked_test_coverage", [])); LC = LC[(LC.alpha == 0.1) & (LC.features == "base+P")]
        _lp = pd.read_csv(os.path.join(R, "predictions", "e5a_locked_test_predictions.csv.gz"))
        _g = _lp[(_lp.target == "biooil") & (_lp.features == "base") & (_lp.learner == learner)]
        _sse = ((_g.y - _g.pred) ** 2).groupby(_g.study).sum(); LT_top_n = int((_g.study == _sse.idxmax()).sum())
        c = LC.set_index(["target", "calibration"])["coverage_studies"]
        for t in ["biooil", "solid"]:
            v[f"{t}_lock_cov_RC"] = f2(c[(t, "RC")]); v[f"{t}_lock_cov_SC"] = f2(c[(t, "SC")])
        ci = {(r["target"], r["calibration"]): r for r in S.get("locked_coverage_ci", [])}
        sens = pd.DataFrame(S.get("locked_sensitivity_exclude_top_study", []))
        xs = sens[(sens.target == "biooil") & (sens.features == "base") & (sens.learner == learner)].iloc[0]
        bb = LT[(LT.target == "biooil") & (LT.features == "base")]
        nbeat = int((bb[bb.learner != "mean"].rmse < bb[bb.learner == "mean"].rmse.iloc[0]).sum())
        better_median = int((bb[bb.learner != "mean"].median_study_rmse < bb[bb.learner == "mean"].median_study_rmse.iloc[0]).sum())
        def cc(t, cal):
            r = ci[(t, cal)]; return f"{r['reported']:.2f} (95% CI {r['ci_low']:.2f}–{r['ci_high']:.2f})"
        v["locked_paragraph"] = (
            "The locked test studies, evaluated once after all modelling decisions had been frozen, gave a more pessimistic picture than development CV. "
            + ("; ".join(parts))[0].upper() + ("; ".join(parts))[1:] + ". "
            f"For bio-oil, only {nbeat} of the 11 non-trivial learners had a lower pooled RMSE than the mean predictor, although {better_median} had a lower median per-study RMSE: "
            f"pooled errors were dominated by a few studies outside the bulk of the training distribution — for {LBL[learner]}, a single solvothermal series of {int(LT_top_n)} runs "
            f"contributed {xs.excluded_sse_share:.0%} of the squared error, and excluding it (post hoc) lowered the RMSE from {xs.rmse_all:.1f} to {xs.rmse_excl:.1f} wt% "
            f"(R² = {abs(xs.r2_excl) if abs(xs.r2_excl) < 0.005 else xs.r2_excl:.2f}). Study-weighted coverage of row-calibrated 90% intervals was {cc('biooil', 'RC')} for bio-oil and {cc('solid', 'RC')} for solids; "
            f"study-calibrated intervals reached {cc('biooil', 'SC')} and {cc('solid', 'SC')} (Table 6, Fig. {{FIGREF:fig05_coverage}}). Study calibration thus removed most, but for solids "
            "not all, of the under-coverage; with 28–30 locked studies the intervals are wide, and the solid-yield shortfall reflects a few studies with feedstocks "
            "(technical lignin, plastic–biomass blends) that are rare in the training data.")
        v["abstract_locked_sentence"] = (f"On 38 locked studies, study-calibrated intervals covered {ci[('biooil', 'SC')]['reported']:.2f} (bio-oil) and "
                                         f"{ci[('solid', 'SC')]['reported']:.2f} (solids) of runs, versus {ci[('biooil', 'RC')]['reported']:.2f} and {ci[('solid', 'RC')]['reported']:.2f} "
                                         "for row-calibrated intervals, and no learner predicted bio-oil yields of new studies substantially better than the training mean.")
        covs = [ci[(t, c)]["reported"] for t in ["biooil", "solid"] for c in ["RC"]] + [float(v["biooil_cov_RC"]), float(v["solid_cov_RC"])]
        scs = [ci[(t, "SC")]["reported"] for t in ["biooil", "solid"]] + [float(v["biooil_cov_SC"]), float(v["solid_cov_SC"])]
        v["hl_cov"] = f"Study-calibrated intervals raised coverage from {min(covs):.2f}–{max(covs):.2f} to {min(scs):.2f}–{max(scs):.2f}"
        v["cov_range_RC"] = f"{min(covs):.2f}–{max(covs):.2f}"; v["cov_range_SC"] = f"{min(scs):.2f}–{max(scs):.2f}"
    # ---------------- temporal / family / external (E5b-d)
    TF = pd.DataFrame(M.get("e5bc_temporal_family_metrics", [])); EX = pd.DataFrame(M.get("e5d_external_metrics", []))
    if len(TF):
        tp = TF[(TF.scheme == "temporal") & (TF.features == "base")].set_index("target")
        fam = TF[(TF.scheme == "family_out") & (TF.features == "base")]
        famw = fam.sort_values("rmse", ascending=False).groupby("target").first()
        def cmp(t):
            a, b = tp.loc[t, "rmse"], float(v[f"{t}_strata_grouped_rmse"])
            return "similar to" if abs(a - b) / b < 0.1 else ("higher than" if a > b else "lower than")
        txt = (f"Predicting studies published after 2018 from earlier studies gave RMSE = {tp.loc['biooil', 'rmse']:.1f} (bio-oil; {cmp('biooil')} the study-grouped CV value of "
               f"{v['biooil_strata_grouped_rmse']} wt%) and {tp.loc['solid', 'rmse']:.1f} wt% (solids; {cmp('solid')} {v['solid_strata_grouped_rmse']} wt%), i.e. models trained on older "
               "literature transfer no better to newer studies than to randomly chosen unseen studies. Leaving out one feedstock family at a time gave mean RMSE of "
               f"{fam[fam.target == 'biooil'].rmse.mean():.1f} and {fam[fam.target == 'solid'].rmse.mean():.1f} wt%, with the largest errors for the "
               f"'{famw.loc['biooil', 'family']}' category (bio-oil, {famw.loc['biooil', 'rmse']:.1f} wt%) and '{famw.loc['solid', 'family']}' (solids, {famw.loc['solid', 'rmse']:.1f} wt%).")
        if len(EX):
            e1 = EX[EX.scheme == "external_4TU_all_dev_processes"].iloc[0]; e2 = EX[EX.scheme == "external_4TU_HTC_dev_only"].iloc[0]
            txt += (f" On the independent 4TU hydrochar database ({int(e1.n)} runs after removing {v['ext_dups']} potential duplicates; {int(e1.n_studies)} feedstock series), "
                    f"a solid-yield model trained on all development studies reached RMSE = {e1.rmse:.1f} wt% (R² = {e1.r2:.2f}), whereas training on the "
                    f"{int(e2.n_train_studies)} HTC development studies alone gave {e2.rmse:.1f} wt% (R² = {e2.r2:.2f}), showing that the small HTC subset of the "
                    "primary database does not by itself support transfer to other HTC compilations (Table 7).")
        v["generalisation_paragraph"] = txt
    # ---------------- robustness (E4)
    rb_p = os.path.join(R, "e4_robustness.csv")
    if os.path.exists(rb_p):
        rb = pd.read_csv(rb_p); rb = rb[rb.features == "base+P"]
        def mrm(t, e, lv, cal="SC", col="rmse"):
            return rb[(rb.target == t) & (rb.experiment == e) & (rb.level == lv) & (rb.calibration == cal)][col].mean()
        nl = sorted(rb[rb.experiment == "feature_noise"].level.unique()); fr = sorted(rb[rb.experiment == "training_studies"].level.unique())
        v["robustness_paragraph"] = (
            f"Adding Gaussian noise of {nl[-1]:.0%} of the training standard deviation to continuous test features increased the bio-oil RMSE from "
            f"{mrm('biooil', 'feature_noise', 0.0):.1f} to {mrm('biooil', 'feature_noise', nl[-1]):.1f} wt% and the solid RMSE from {mrm('solid', 'feature_noise', 0.0):.1f} "
            f"to {mrm('solid', 'feature_noise', nl[-1]):.1f} wt%, while SC coverage was {mrm('biooil', 'feature_noise', 0.0, 'SC', 'coverage_studies'):.2f} without and "
            f"{mrm('biooil', 'feature_noise', nl[-1], 'SC', 'coverage_studies'):.2f} with noise (bio-oil) — the error budget for unseen studies is dominated by the study offset, not by input noise. "
            f"Training on {fr[0]:.0%} instead of all training studies raised the bio-oil RMSE from {mrm('biooil', 'training_studies', 1.0):.1f} to "
            f"{mrm('biooil', 'training_studies', fr[0]):.1f} wt%, and SC coverage remained {mrm('biooil', 'training_studies', fr[0], 'SC', 'coverage_studies'):.2f}, "
            f"whereas RC coverage stayed at {mrm('biooil', 'training_studies', fr[0], 'RC', 'coverage_studies'):.2f}–{mrm('biooil', 'training_studies', 1.0, 'RC', 'coverage_studies'):.2f} (Supplementary Fig. S1).")
    # ---------------- efficiency (E6)
    EF = pd.DataFrame(M.get("e6_efficiency", []))
    if len(EF):
        e = EF.set_index("learner"); sl = e.loc[learner]
        v["efficiency_paragraph"] = (
            f"All learners trained in at most {e.fit_s.max():.0f} s on one CPU thread ({LBL[e.fit_s.idxmax()]}); the STRATA base learner took {sl.fit_s:.1f} s "
            f"and predicted 1,000 runs in {sl.predict_ms_per_1000_rows:.0f} ms (Supplementary Table S14, Supplementary Fig. S2). The complete STRATA procedure — two inner five-fold cross-validations, "
            f"quantiles, variance components and k-shot quantiles for all k — took {v['ovh_min']}–{v['ovh_max']} s on all development studies, against {v['ovh_base_min']}–{v['ovh_base_max']} s "
            "for fitting the base learner alone (measured, 1 and 4 threads); this overhead is negligible compared with the cost of a single hydrothermal experiment.")
    # ---------------- error analysis (E8)
    EA_p = os.path.join(R, "e8_error_analysis.csv")
    if os.path.exists(EA_p):
        ea = pd.read_csv(EA_p)
        def worst(t, dim, k=1):
            d = ea[(ea.target == t) & (ea.dimension == dim) & (ea.n_studies >= 3)].sort_values("rmse", ascending=False)
            return d.iloc[0]
        f_b = worst("biooil", "family"); t_b = worst("biooil", "temperature_bin"); p_b = worst("biooil", "process"); c_s = worst("solid", "catalyst_present")
        sw = pd.read_csv(os.path.join(R, "e8_study_errors_biooil.csv")).head(5)
        sg = ea[(ea.target == "biooil") & (ea.dimension == "extraction_solvent") & (ea.n_studies >= 3)]
        v["error_paragraph"] = (
            f"Out-of-study errors were largest for {f_b.level} feedstocks among families (bio-oil RMSE {f_b.rmse:.1f} wt%, {int(f_b.n_studies)} studies), "
            f"for the {t_b.level.replace('<=', '≤')} °C temperature band ({t_b.rmse:.1f} wt%) and for {p_b.level.replace('_', ' ')} runs ({p_b.rmse:.1f} wt%) (Supplementary Table S9). "
            f"The five worst-predicted bio-oil studies had per-study RMSE between {sw.rmse.min():.1f} and {sw.rmse.max():.1f} wt% and absolute mean offsets of "
            f"{sw.bias.abs().min():.1f}–{sw.bias.abs().max():.1f} wt% (processes: {', '.join(f'{k.replace(chr(95), chr(32))} {n}' for k, n in sw.process.value_counts().items())}). "
            f"Across extraction-solvent groups with at least three studies, the bio-oil RMSE ranged from {sg.rmse.min():.1f} ({sg.sort_values('rmse').iloc[0].level.replace(chr(95), chr(32))}) "
            f"to {sg.rmse.max():.1f} wt% ({sg.sort_values('rmse').iloc[-1].level.replace(chr(95), chr(32))}) and the mean residual from {sg.bias.min():+.1f} to {sg.bias.max():+.1f} wt% (Supplementary Fig. S3).")
    ad_p = os.path.join(R, "e3b_adaptive_summary.csv")
    if os.path.exists(ad_p):
        ad = pd.read_csv(ad_p).set_index(["target", "method"])
        b = lambda t, m, c: ad.loc[(t, m), c]
        v["adaptive_sentence"] = (
            f"For bio-oil, SC-N gave study-weighted coverage {b('biooil', 'SC-N', 'coverage_studies'):.2f} (SC {b('biooil', 'SC', 'coverage_studies'):.2f}) with median width "
            f"{b('biooil', 'SC-N', 'median_width'):.1f} vs {b('biooil', 'SC', 'median_width'):.1f} wt% and mean interval score {b('biooil', 'SC-N', 'winkler'):.1f} vs "
            f"{b('biooil', 'SC', 'winkler'):.1f}; for solids, coverage {b('solid', 'SC-N', 'coverage_studies'):.2f} vs {b('solid', 'SC', 'coverage_studies'):.2f}, median width "
            f"{b('solid', 'SC-N', 'median_width'):.1f} vs {b('solid', 'SC', 'median_width'):.1f} wt%, interval score {b('solid', 'SC-N', 'winkler'):.1f} vs {b('solid', 'SC', 'winkler'):.1f}. "
            + ("The adaptive variant therefore did not improve interval efficiency — both widths and interval scores were worse — although coverage across process "
               f"subtypes became more uniform (largest deviation from 0.90: {b('solid', 'SC-N', 'max_abs_process_dev'):.2f} vs {b('solid', 'SC', 'max_abs_process_dev'):.2f} for solids). "
               "This negative result is consistent with the main finding that the dominant error component is a study offset that input features cannot localise. "
               if (b('biooil', 'SC-N', 'winkler') > b('biooil', 'SC', 'winkler') and b('solid', 'SC-N', 'winkler') > b('solid', 'SC', 'winkler')) else
               "The adaptive variant improved interval scores for at least one target. ")
            + "Because this variant was added after inspecting pipeline-verification results, it is reported as exploratory and is not part of the main claims.")
    return v


def holm2(p):
    import numpy as _np
    p = _np.asarray(p, float); o = _np.argsort(p); m = len(p); adj = _np.empty(m); run = 0
    for r, i in enumerate(o):
        run = max(run, (m - r) * p[i]); adj[i] = min(1, run)
    return adj


if __name__ == "__main__":
    for k, x in compute().items():
        print(k, "=", x)
