"""Manuscript tables generated from statistics.json / metrics.json / result CSVs (CSV + Markdown)."""
from __future__ import annotations

import json, os, sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.utils import out_dirs, load_config
from src.statistics.analyze import LEARNER_LABEL
from src.data.load import load_target

TL = {"biooil": "Bio-oil", "solid": "Solid"}


def fmt_p(p):
    return "<0.001" if p < 0.001 else f"{p:.3f}"


def write(df, D, name, caption):
    df.to_csv(os.path.join(D["tables"], f"{name}.csv"), index=False)
    with open(os.path.join(D["tables"], f"{name}.md"), "w") as f:
        f.write(f"**{caption}**\n\n" + df.to_markdown(index=False) + "\n")


def run(mode="full"):
    cfg, D = load_config(mode), out_dirs(mode)
    S = json.load(open(os.path.join(D["results"], "statistics.json")))
    M = json.load(open(os.path.join(D["results"], "metrics.json")))
    a = cfg["alpha"]

    # Table 1 — data
    rows = []
    for t in ["biooil", "solid"]:
        for sp in ["dev", "test"]:
            ds = load_target(t, sp)
            rows.append({"Target": TL[t], "Split": {"dev": "Development", "test": "Locked test"}[sp], "Runs": len(ds.y),
                         "Studies": len(set(ds.groups)), "Median runs/study": int(pd.Series(ds.groups).value_counts().median()),
                         "Yield mean ± SD (wt%)": f"{ds.y.mean():.1f} ± {ds.y.std():.1f}",
                         "Excluded (carbon basis / missing inputs / single-run study)":
                             f"{ds.exclusions['excluded_carbon_basis']} / {ds.exclusions['excluded_missing_core_inputs']} / {ds.exclusions['excluded_single_row_studies']}"})
    write(pd.DataFrame(rows), D, "table1_data", "Table 1. Data used for each target after pre-specified exclusions.")

    # Table 2 — benchmark random vs grouped (base features)
    w = pd.read_csv(os.path.join(D["tables"], "table_e1_benchmark_wide.csv"))
    rows = []
    for _, r in w[w.features == "base"].iterrows():
        rows.append({"Target": TL[r.target], "Learner": LEARNER_LABEL[r.learner],
                     "Random CV RMSE": round(r.rmse_random_row_cv, 2), "Random CV R²": round(r.r2_random_row_cv, 3),
                     "Grouped CV RMSE": round(r.rmse_grouped_study_cv, 2), "Grouped CV R²": round(r.r2_grouped_study_cv, 3),
                     "RMSE ratio (grouped/random)": round(r.optimism_ratio_rmse, 2)})
    t2 = pd.DataFrame(rows).sort_values(["Target", "Grouped CV RMSE"])
    write(t2, D, "table2_benchmark", "Table 2. Random-row versus study-grouped cross-validation on development studies (base features; grouped CV averaged over 3 seeds).")

    # Table 3 — heterogeneity, protocol ablation, meta-regression
    rows = []
    mr = {m["target"]: m for m in S.get("meta_regression", [])}
    for t in ["biooil", "solid"]:
        e = S["e3"][t]; h = e["heterogeneity"]["base"]; pa = e["protocol_ablation"]
        tst = pa["test_one_sided_base_plus_P_less"]
        rows.append({"Target": TL[t], "τ² (between)": round(h["tau2"], 1), "σ²w (within)": round(h["sigma2_w"], 1),
                     "Between-study share [95% CI]": f"{h['share_between']:.2f} [{h['share_ci'][0]:.2f}, {h['share_ci'][1]:.2f}]",
                     "Median study RMSE base → base+P": f"{pa['median_study_rmse_base']:.2f} → {pa['median_study_rmse_baseP']:.2f}",
                     "Δ median [95% CI]; p (one-sided)": f"{tst['median_diff']:.2f} [{tst['ci_low']:.2f}, {tst['ci_high']:.2f}]; {fmt_p(tst['p'])}",
                     "Rank-biserial": round(tst["rank_biserial"], 2),
                     "Meta-regression LOSO R² (perm. p)": f"{mr[t]['loso_r2']:.3f} ({fmt_p(mr[t]['perm_p'])})" if t in mr else "n/a"})
    write(pd.DataFrame(rows), D, "table3_heterogeneity", "Table 3. Decomposition of out-of-study error and contribution of work-up/reporting descriptors (P).")

    # Table 4 — coverage
    rows = []
    for t in ["biooil", "solid"]:
        for c in S["e3"][t]["coverage"]:
            if c["features"] != "base+P":
                continue
            rows.append({"Target": TL[t], "Setting": "Development CV (unseen studies)", "α": c["alpha"], "Calibration": c["calibration"],
                         "Coverage (rows)": round(c["coverage_rows"], 3), "Coverage (studies)": round(c["coverage_studies"], 3),
                         "Width (wt%)": round(c["width"], 1), "Studies <0.8 coverage": round(c["frac_studies_below_0_8"], 2)})
    for key, setting in [("e5a_locked_test_coverage", "Locked test"), ("e5bc_temporal_family_coverage", None), ("e5d_external_coverage", "External 4TU")]:
        df = pd.DataFrame(M.get(key, []))
        if df.empty:
            continue
        if "features" in df:
            df = df[df.features == "base+P"] if key != "e5d_external_coverage" else df[df.tag == "external_4TU"]
        g = df.groupby(["target", "tag", "alpha", "calibration"], as_index=False)[["coverage_rows", "coverage_studies", "width", "frac_studies_below_80"]].mean()
        for _, r in g.iterrows():
            rows.append({"Target": TL[r.target], "Setting": setting or {"temporal": "Temporal (≤2018 → >2018)", "family_out": "Leave-family-out (mean)"}[r.tag],
                         "α": r.alpha, "Calibration": r.calibration, "Coverage (rows)": round(r.coverage_rows, 3),
                         "Coverage (studies)": round(r.coverage_studies, 3), "Width (wt%)": round(r.width, 1), "Studies <0.8 coverage": round(r.frac_studies_below_80, 2)})
    t4 = pd.DataFrame(rows)
    write(t4[t4["α"] == a], D, "table4_coverage", f"Table 4. Empirical coverage of {int(100*(1-a))}% prediction intervals: row-calibrated (RC) vs study-calibrated (SC).")
    write(t4, D, "tableS_coverage_all_alpha", "Table S. Coverage for all α levels and settings.")

    # Table 5 — k-shot
    rows = []
    for t in ["biooil", "solid"]:
        ks = pd.DataFrame(S["e3"][t]["kshot_summary"]); ks = ks[ks.features == "base+P"]
        tests = pd.DataFrame(S["e3"][t]["kshot_tests"]); tests = tests[tests.features == "base+P"]
        for _, r in ks.sort_values(["k", "mode"]).iterrows():
            tt = tests[(tests.k == r.k) & (tests.comparison == "eb_vs_raw")]
            rows.append({"Target": TL[t], "k": int(r.k), "Offset": {"none": "—", "raw": "raw mean", "eb": "EB shrinkage"}[r["mode"]],
                         "Median study RMSE": round(r.median_study_rmse, 2), "Coverage (studies)": round(r.coverage_studies, 3),
                         "Width (wt%)": round(r.width, 1), "Studies": int(r.n_studies),
                         "EB vs raw: Δ median; p_Holm": (f"{tt.iloc[0]['median_diff']:.2f}; {fmt_p(tt.iloc[0]['p_holm'])}" if (r["mode"] == "eb" and len(tt)) else "")})
    write(pd.DataFrame(rows), D, "table5_kshot", "Table 5. k-shot adaptation to a new study (studies with ≥ 11 runs; 20 random support sets per study).")

    # Table 6 — locked test
    lt = pd.DataFrame(M.get("e5a_locked_test_metrics", []))
    if not lt.empty:
        lt = lt[lt.features == "base"].copy()
        lt["Learner"] = lt.learner.map(LEARNER_LABEL); lt["Target"] = lt.target.map(TL)
        out = lt[["Target", "Learner", "n", "n_studies", "rmse", "r2", "median_study_rmse"]].rename(
            columns={"n": "Runs", "n_studies": "Studies", "rmse": "RMSE", "r2": "R²", "median_study_rmse": "Median study RMSE"}).round(3)
        write(out.sort_values(["Target", "RMSE"]), D, "table6_locked_test", "Table 6. Single evaluation on the 38 locked test studies (models trained on all development studies, base features).")
    # Table 7 — temporal / family / external
    rows = []
    for key in ["e5bc_temporal_family_metrics", "e5d_external_metrics"]:
        df = pd.DataFrame(M.get(key, []))
        if df.empty:
            continue
        if key == "e5bc_temporal_family_metrics":
            fam = df[df.scheme == "family_out"].groupby(["target", "features"], as_index=False)[["rmse", "r2", "median_study_rmse"]].mean().assign(scheme="family_out (mean over families)")
            df = pd.concat([df[df.scheme == "temporal"], fam])
        for _, r in df.iterrows():
            rows.append({"Target": TL[r.target], "Features": r.features, "Scheme": r.scheme, "RMSE": round(r.rmse, 2), "R²": round(r.r2, 3),
                         "Median study RMSE": round(r.median_study_rmse, 2)})
    if rows:
        write(pd.DataFrame(rows), D, "table7_generalisation", "Table 7. Temporal, feedstock-family and external generalisation of the STRATA base learner.")
    # Table 8 — efficiency
    ef = pd.DataFrame(M.get("e6_efficiency", []))
    if not ef.empty:
        ef["Learner"] = ef.learner.map(LEARNER_LABEL)
        write(ef[["Learner", "fit_s", "predict_ms_per_1000_rows", "peak_rss_increase_MB", "model_size_MB"]].round(3).rename(
            columns={"fit_s": "Fit time (s)", "predict_ms_per_1000_rows": "Predict (ms / 1000 rows)", "peak_rss_increase_MB": "Peak RSS increase (MB)",
                     "model_size_MB": "Serialized size (MB)"}), D, "table8_efficiency", "Table 8. Computational cost (bio-oil, development set, single thread). Peak RSS increase is measured relative to the process peak after data loading.")
    # Table S — paired tests of learners
    pt = pd.DataFrame(S.get("e1_paired_tests", []))
    if not pt.empty:
        pt = pt[["target", "features", "learner", "reference", "n", "median_diff", "ci_low", "ci_high", "rank_biserial", "p", "p_holm"]].round(4)
        write(pt, D, "tableS_paired_learner_tests", "Table S. Per-study RMSE of each learner vs the best learner under grouped CV (Wilcoxon, Holm).")

    # ---- supplementary tables
    from src.utils import REPO
    lit = pd.read_csv(os.path.join(REPO, "supplementary", "literature", "literature_matrix_corpus.csv"))
    write(lit[["year", "venue", "first_author", "doi", "problem", "methods", "validation", "reported_R2", "uncertainty", "physics_constraints"]].rename(
        columns={"year": "Year", "venue": "Journal", "first_author": "First author", "doi": "DOI", "problem": "Target(s)", "methods": "Methods",
                 "validation": "Validation (abstract)", "reported_R2": "R² in abstract", "uncertainty": "UQ", "physics_constraints": "Physics"}),
          D, "tableS1_literature", "Table S1. PubMed-indexed ML studies of hydrothermal conversion (abstract-level screening; n.s. = not stated in abstract).")
    sens_p = os.path.join(D["results"], "e7_sensitivity.csv")
    if os.path.exists(sens_p):
        se = pd.read_csv(sens_p)
        o = se[se.analysis == "outer_folds_alpha"].groupby(["target", "features", "outer_folds", "alpha", "calibration"], as_index=False)[["coverage_studies", "width", "rmse"]].mean()
        o["target"] = o.target.map(TL)
        write(o.round(3).rename(columns={"coverage_studies": "Coverage (studies)", "width": "Width (wt%)", "rmse": "RMSE"}), D, "tableS3_sensitivity_alpha_folds",
              "Table S3. Sensitivity of coverage and accuracy to α and to the number of outer folds (seed 11).")
        k = se[se.analysis == "tau2_estimator"].groupby(["target", "features", "estimator", "k"], as_index=False)[["rmse", "coverage", "width"]].median()
        k["target"] = k.target.map(TL)
        write(k.round(3).rename(columns={"rmse": "Median study RMSE", "coverage": "Median study coverage", "width": "Width (wt%)"}), D, "tableS4_sensitivity_tau2",
              "Table S4. k-shot results with method-of-moments vs REML estimates of the between-study variance.")
        tu = se[se.analysis == "tuning"][["target", "features", "config", "rmse", "r2", "median_study_rmse"]].copy(); tu["target"] = tu.target.map(TL)
        write(tu.round(3), D, "tableS5_sensitivity_tuning", "Table S5. Study-grouped CV of the STRATA base learner with tuned vs library-default hyper-parameters.")
    ea = os.path.join(D["results"], "e8_error_analysis.csv")
    if os.path.exists(ea):
        e = pd.read_csv(ea); e["target"] = e.target.map(TL)
        write(e.round(2), D, "tableS6_error_analysis", "Table S6. Out-of-study errors by subgroup (seed-averaged outer-fold predictions, base features).")
    ad = os.path.join(D["results"], "e3b_adaptive_summary.csv")
    if os.path.exists(ad):
        x = pd.read_csv(ad); x["target"] = x.target.map(TL)
        write(x.round(3), D, "tableS7_adaptive", "Table S7. Exploratory (post hoc): constant-width vs locally adaptive study-calibrated intervals (α = 0.1, base+P).")
    wP = w[w.features == "base+P"]
    rows = [{"Target": TL[r.target], "Learner": LEARNER_LABEL[r.learner], "Random CV RMSE": round(r.rmse_random_row_cv, 2),
             "Grouped CV RMSE": round(r.rmse_grouped_study_cv, 2), "Grouped CV R²": round(r.r2_grouped_study_cv, 3)} for _, r in wP.iterrows()]
    write(pd.DataFrame(rows).sort_values(["Target", "Grouped CV RMSE"]), D, "tableS2_benchmark_baseP", "Table S2. Benchmark with base + protocol (P) features.")

    e9p = os.path.join(D["results"], "e9_base_learners.csv")
    if os.path.exists(e9p):
        e9 = pd.read_csv(e9p); k9 = pd.read_csv(os.path.join(D["results"], "e9_base_learners_kshot.csv"))
        piv = e9.pivot_table(index=["target", "learner"], columns="calibration", values=["coverage_studies", "width"]).reset_index()
        piv.columns = ["Target", "Base learner", "Coverage RC", "Coverage SC", "Width RC (wt%)", "Width SC (wt%)"]
        rm = e9[e9.calibration == "SC"].set_index(["target", "learner"])[["rmse", "median_study_rmse"]]
        k3 = k9[k9.k == 3].set_index(["target", "learner"])["median_study_rmse"]
        piv["Pooled RMSE"] = [rm.loc[(a, b), "rmse"] for a, b in zip(piv["Target"], piv["Base learner"])]
        piv["Median study RMSE k=0"] = [rm.loc[(a, b), "median_study_rmse"] for a, b in zip(piv["Target"], piv["Base learner"])]
        piv["Median study RMSE k=3 (EB)"] = [k3.loc[(a, b)] for a, b in zip(piv["Target"], piv["Base learner"])]
        piv["Target"] = piv["Target"].map(TL); piv["Base learner"] = piv["Base learner"].map(LEARNER_LABEL)
        write(piv.round(3), D, "tableS10_base_learners", "Table S10. STRATA with different base learners (development study-folds, seed 11, base + P features, α = 0.1). The mean predictor is the 'no-ML' reference.")


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "full")
