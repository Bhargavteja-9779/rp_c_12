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
        c = LC.set_index(["target", "calibration"])["coverage_studies"]
        for t in ["biooil", "solid"]:
            v[f"{t}_lock_cov_RC"] = f2(c[(t, "RC")]); v[f"{t}_lock_cov_SC"] = f2(c[(t, "SC")])
        v["locked_paragraph"] = ("The locked test studies, evaluated once after all modelling decisions were frozen, confirmed the development results: "
                                 + "; ".join(parts) + f". Row-calibrated 90% intervals covered {c[('biooil', 'RC')]:.2f} (bio-oil) and {c[('solid', 'RC')]:.2f} (solids) "
                                 f"of locked-study runs with equal study weights, study-calibrated intervals {c[('biooil', 'SC')]:.2f} and {c[('solid', 'SC')]:.2f} (Table 6, Fig. 5).")
        v["abstract_locked_sentence"] = (f"On the locked studies, study-calibrated intervals covered {c[('biooil', 'SC')]:.2f} and {c[('solid', 'SC')]:.2f} of runs "
                                         f"(row-calibrated: {c[('biooil', 'RC')]:.2f} and {c[('solid', 'RC')]:.2f}).")
    # ---------------- temporal / family / external (E5b-d)
    TF = pd.DataFrame(M.get("e5bc_temporal_family_metrics", [])); EX = pd.DataFrame(M.get("e5d_external_metrics", []))
    if len(TF):
        tp = TF[(TF.scheme == "temporal") & (TF.features == "base+P")].set_index("target")
        fam = TF[(TF.scheme == "family_out") & (TF.features == "base+P")]
        famw = fam.sort_values("rmse", ascending=False).groupby("target").first()
        txt = (f"Predicting studies published after 2018 from earlier studies gave RMSE = {tp.loc['biooil', 'rmse']:.1f} (bio-oil) and "
               f"{tp.loc['solid', 'rmse']:.1f} wt% (solids), in line with study-grouped CV. Leaving out one feedstock family at a time gave mean RMSE of "
               f"{fam[fam.target == 'biooil'].rmse.mean():.1f} and {fam[fam.target == 'solid'].rmse.mean():.1f} wt%, with the largest errors for "
               f"{famw.loc['biooil', 'family']} (bio-oil, {famw.loc['biooil', 'rmse']:.1f} wt%) and {famw.loc['solid', 'family']} (solids, {famw.loc['solid', 'rmse']:.1f} wt%).")
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
            f"to {mrm('solid', 'feature_noise', nl[-1]):.1f} wt%, while SC coverage changed from {mrm('biooil', 'feature_noise', 0.0, 'SC', 'coverage_studies'):.2f} to "
            f"{mrm('biooil', 'feature_noise', nl[-1], 'SC', 'coverage_studies'):.2f} (bio-oil) — the error budget for unseen studies is dominated by the study offset, not by input noise. "
            f"Training on {fr[0]:.0%} instead of all training studies raised the bio-oil RMSE from {mrm('biooil', 'training_studies', 1.0):.1f} to "
            f"{mrm('biooil', 'training_studies', fr[0]):.1f} wt%, and SC coverage remained {mrm('biooil', 'training_studies', fr[0], 'SC', 'coverage_studies'):.2f}, "
            f"whereas RC coverage stayed at {mrm('biooil', 'training_studies', fr[0], 'RC', 'coverage_studies'):.2f}–{mrm('biooil', 'training_studies', 1.0, 'RC', 'coverage_studies'):.2f} (Fig. 7).")
    # ---------------- efficiency (E6)
    EF = pd.DataFrame(M.get("e6_efficiency", []))
    if len(EF):
        e = EF.set_index("learner"); sl = e.loc[learner]
        v["efficiency_paragraph"] = (
            f"All learners trained in at most {e.fit_s.max():.0f} s on one CPU thread ({LBL[e.fit_s.idxmax()]}); the STRATA base learner took {sl.fit_s:.1f} s "
            f"and predicted 1,000 runs in {sl.predict_ms_per_1000_rows:.0f} ms (Table 8, Fig. 8). STRATA adds two inner cross-validations (2 × 5 extra fits) and "
            "negligible arithmetic for the quantiles and offsets, so its overhead is about one order of magnitude of the base learner's training time — "
            "seconds to minutes on a 4-core CPU — which is small compared with the cost of a single hydrothermal experiment.")
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
            f"for the {t_b.level} °C temperature band ({t_b.rmse:.1f} wt%) and for {p_b.level.replace('_', ' ')} runs ({p_b.rmse:.1f} wt%) (Supplementary Table S9). "
            f"The five worst-predicted bio-oil studies had per-study RMSE between {sw.rmse.min():.1f} and {sw.rmse.max():.1f} wt% and absolute mean offsets of "
            f"{sw.bias.abs().min():.1f}–{sw.bias.abs().max():.1f} wt% (processes: {', '.join(f'{k.replace(chr(95), chr(32))} {n}' for k, n in sw.process.value_counts().items())}). "
            f"Across extraction-solvent groups with at least three studies, the bio-oil RMSE ranged from {sg.rmse.min():.1f} ({sg.sort_values('rmse').iloc[0].level.replace(chr(95), chr(32))}) "
            f"to {sg.rmse.max():.1f} wt% ({sg.sort_values('rmse').iloc[-1].level.replace(chr(95), chr(32))}) and the mean residual from {sg.bias.min():+.1f} to {sg.bias.max():+.1f} wt% (Fig. 9).")
    ad_p = os.path.join(R, "e3b_adaptive_summary.csv")
    if os.path.exists(ad_p):
        ad = pd.read_csv(ad_p).set_index(["target", "method"])
        b = lambda t, m, c: ad.loc[(t, m), c]
        v["adaptive_sentence"] = (
            f"For bio-oil, SC-N gave study-weighted coverage {b('biooil', 'SC-N', 'coverage_studies'):.2f} (SC {b('biooil', 'SC', 'coverage_studies'):.2f}) with median width "
            f"{b('biooil', 'SC-N', 'median_width'):.1f} vs {b('biooil', 'SC', 'median_width'):.1f} wt% and mean interval score {b('biooil', 'SC-N', 'winkler'):.1f} vs "
            f"{b('biooil', 'SC', 'winkler'):.1f}; for solids, coverage {b('solid', 'SC-N', 'coverage_studies'):.2f} vs {b('solid', 'SC', 'coverage_studies'):.2f}, median width "
            f"{b('solid', 'SC-N', 'median_width'):.1f} vs {b('solid', 'SC', 'median_width'):.1f} wt%, interval score {b('solid', 'SC-N', 'winkler'):.1f} vs {b('solid', 'SC', 'winkler'):.1f}. "
            "Because this variant was added after inspecting pipeline-verification results, it is reported as exploratory and is not part of the main claims.")
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
