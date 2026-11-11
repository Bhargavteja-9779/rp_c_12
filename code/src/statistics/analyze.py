"""Turn experiment outputs into statistics.json, metrics.json, raw_results.csv and manuscript tables.

Every number used in the manuscript is produced here (or in the experiment CSVs) — nothing is typed by hand.
"""
from __future__ import annotations

import json, os, sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.statistics.stats import paired_comparison, holm, cluster_bootstrap_ci
from src.models.strata import variance_components
from src.utils import out_dirs, load_config, dump

LEARNER_LABEL = {"mean": "Mean", "ridge": "Ridge", "knn": "k-NN", "svr": "SVR", "mlp": "MLP", "rf": "Random forest",
                 "et": "Extra trees", "hgb": "HistGB", "lgbm": "LightGBM", "xgb": "XGBoost", "cat": "CatBoost", "gpboost": "GPBoost"}


def per_study_rmse(df, pred_col):
    return df.groupby("study").apply(lambda t: float(np.sqrt(np.mean((t["y"] - t[pred_col]) ** 2))), include_groups=False)


def e1_stats(D, cfg):
    e1 = pd.read_csv(os.path.join(D["results"], "e1_benchmark.csv"))
    agg = (e1.groupby(["target", "features", "learner", "scheme"])
             .agg(rmse=("rmse", "mean"), rmse_sd=("rmse", "std"), mae=("mae", "mean"), r2=("r2", "mean"), r2_sd=("r2", "std"),
                  median_study_rmse=("median_study_rmse", "mean"), fit_s=("fit_s", "mean"), n=("n", "first"), n_studies=("n_studies", "first"))
             .reset_index())
    wide = agg.pivot_table(index=["target", "features", "learner"], columns="scheme", values=["rmse", "r2", "median_study_rmse"]).reset_index()
    wide.columns = ["_".join([c for c in col if c]) for col in wide.columns]
    wide["optimism_ratio_rmse"] = wide["rmse_grouped_study_cv"] / wide["rmse_random_row_cv"]
    # paired per-study comparison: random-CV vs grouped-CV per-study RMSE is not meaningful (same rows, different
    # models); instead compare learners under grouped CV against the best learner, per study, seed-averaged.
    tests = []
    for (t, fs), sub in wide.groupby(["target", "features"]):
        best = sub.sort_values("rmse_grouped_study_cv").iloc[0]["learner"]
        ps = {}
        for ln in sub["learner"]:
            f = os.path.join(D["pred"], f"e1_{t}__{fs}__{ln}.csv.gz")
            p = pd.read_csv(f)
            gcols = [c for c in p.columns if c.startswith("grouped_")]
            ps[ln] = pd.concat([per_study_rmse(p, c) for c in gcols], axis=1).mean(axis=1)
        comps = []
        for ln in ps:
            if ln == best:
                continue
            a, b = ps[ln].align(ps[best], join="inner")
            comps.append(dict(target=t, features=fs, learner=ln, reference=best, **paired_comparison(a.values, b.values)))
        adj = holm([c["p"] for c in comps])
        for c, pa in zip(comps, adj):
            c["p_holm"] = float(pa)
        tests.extend(comps)
    return agg, wide, pd.DataFrame(tests)


def e3_stats(D, cfg):
    out = {}
    a = cfg["alpha"]
    for target in ["biooil", "solid"]:
        ps = {}
        for fs in ["base", "base+P"]:
            p = pd.read_csv(os.path.join(D["pred"], f"e3_{target}__{fs}.csv.gz"))
            ps[fs] = p
        # --- RQ2 heterogeneity decomposition of outer-fold residuals (seed-averaged predictions) ---
        het = {}
        for fs, p in ps.items():
            q = p.groupby("idx", as_index=False).agg(y=("y", "first"), pred=("pred", "mean"), study=("study", "first"))
            r = (q["y"] - q["pred"]).to_numpy()
            vc = variance_components(r, q["study"].to_numpy())
            df = pd.DataFrame({"r": r, "study": q["study"]})
            lo, hi = cluster_bootstrap_ci(df, lambda d: variance_components(d["r"].to_numpy(), d["study"].to_numpy())["share_between"],
                                          n_boot=cfg["bootstrap"], seed=0)
            het[fs] = dict(**{k: v for k, v in vc.items() if k != "lam"}, share_ci=[lo, hi])
        # --- RQ3 ablation of protocol descriptors (per-study RMSE, seed-averaged) ---
        prs = {}
        for fs, p in ps.items():
            prs[fs] = pd.concat([per_study_rmse(g, "pred") for _, g in p.groupby("seed")], axis=1).mean(axis=1)
        x, y = prs["base+P"].align(prs["base"], join="inner")
        abl = paired_comparison(x.values, y.values, alternative="less")
        abl_two = paired_comparison(x.values, y.values, alternative="two-sided")
        # --- RQ4 coverage RC vs SC on outer folds (per seed, then mean; study-cluster CI on seed 1) ---
        cov = {}
        for fs, p in ps.items():
            for c in ["RC", "SC"]:
                for al in cfg["alphas"]:
                    col = f"q{c}_{al}"
                    vals = []
                    for s, g in p.groupby("seed"):
                        hit = (np.abs(g["y"] - g["pred"]) <= g[col]).astype(float)
                        w = 1 / g["study"].map(g["study"].value_counts())
                        vals.append(dict(rows=float(hit.mean()), studies=float((w * hit).sum() / w.sum()), width=float(2 * g[col].mean())))
                    g0 = p[p["seed"] == p["seed"].min()].copy()
                    g0["hit"] = (np.abs(g0["y"] - g0["pred"]) <= g0[col]).astype(float)
                    g0["w"] = 1 / g0["study"].map(g0["study"].value_counts())
                    lo, hi = cluster_bootstrap_ci(g0[["study", "hit", "w"]], lambda d: float((d["w"] * d["hit"]).sum() / d["w"].sum()),
                                                  n_boot=cfg["bootstrap"], seed=0)
                    per = g0.groupby("study")["hit"].mean()
                    cov[f"{fs}|{c}|{al}"] = dict(features=fs, calibration=c, alpha=al,
                                                 coverage_rows=float(np.mean([v["rows"] for v in vals])),
                                                 coverage_studies=float(np.mean([v["studies"] for v in vals])),
                                                 coverage_studies_ci_seed1=[lo, hi],
                                                 width=float(np.mean([v["width"] for v in vals])),
                                                 frac_studies_below_0_8=float((per < 0.8).mean()))
        # paired per-study coverage SC vs RC (alpha = cfg alpha, base+P features, seed-averaged)
        p = ps["base+P"]
        hits = {}
        for c in ["RC", "SC"]:
            col = f"q{c}_{a}"
            hits[c] = p.assign(h=(np.abs(p["y"] - p["pred"]) <= p[col]).astype(float)).groupby("study")["h"].mean()
        cov_test = paired_comparison(hits["SC"].values, hits["RC"].values, alternative="greater")
        # --- RQ5 k-shot ---
        ks_rows = []
        for fs in ["base", "base+P"]:
            k = pd.read_csv(os.path.join(D["results"], f"e3_kshot_{target}__{fs}.csv"))
            kk = k.groupby(["study", "k", "mode"]).agg(rmse=("rmse", "mean"), coverage=("coverage", "mean"), width=("width", "mean")).reset_index()
            w = 1 / kk.groupby(["k", "mode"])["study"].transform("count")
            summ = kk.groupby(["k", "mode"]).agg(median_study_rmse=("rmse", "median"), mean_study_rmse=("rmse", "mean"),
                                                 coverage_studies=("coverage", "mean"), width=("width", "mean"), n_studies=("study", "nunique")).reset_index()
            summ["features"] = fs
            ks_rows.append(summ)
            # tests: eb vs raw per k; eb(k) vs none(0)
            base0 = kk[(kk.k == 0)].set_index("study")["rmse"]
            tests = []
            for kv in sorted(kk.k.unique()):
                if kv == 0:
                    continue
                e = kk[(kk.k == kv) & (kk["mode"] == "eb")].set_index("study")["rmse"]
                r_ = kk[(kk.k == kv) & (kk["mode"] == "raw")].set_index("study")["rmse"]
                ea, ra = e.align(r_, join="inner")
                tests.append(dict(features=fs, k=int(kv), comparison="eb_vs_raw", **paired_comparison(ea.values, ra.values)))
                ea, za = e.align(base0, join="inner")
                tests.append(dict(features=fs, k=int(kv), comparison="eb_vs_k0", **paired_comparison(ea.values, za.values)))
            adj = holm([t_["p"] for t_ in tests])
            for t_, pa in zip(tests, adj):
                t_["p_holm"] = float(pa)
            out.setdefault(target, {}).setdefault("kshot_tests", []).extend(tests)
        vcs = {fs: pd.read_csv(os.path.join(D["results"], f"e3_varcomp_{target}__{fs}.csv")) for fs in ["base", "base+P"]}
        out.setdefault(target, {}).update(dict(
            heterogeneity=het,
            protocol_ablation=dict(test_one_sided_base_plus_P_less=abl, test_two_sided=abl_two,
                                   median_study_rmse_base=float(prs["base"].median()), median_study_rmse_baseP=float(prs["base+P"].median()),
                                   pooled_rmse=dict(base=float(np.sqrt(np.mean((ps["base"]["y"] - ps["base"]["pred"]) ** 2))),
                                                    baseP=float(np.sqrt(np.mean((ps["base+P"]["y"] - ps["base+P"]["pred"]) ** 2))))),
            coverage=list(cov.values()),
            coverage_test_SC_vs_RC=cov_test,
            kshot_summary=pd.concat(ks_rows).to_dict("records"),
            inner_lambda={fs: dict(median=float(v["lam"].replace(np.inf, np.nan).median()),
                                   share_between_median=float(v["share_between"].median())) for fs, v in vcs.items()},
        ))
    return out


def run(mode="full"):
    cfg, D = load_config(mode), out_dirs(mode)
    S, M = {}, {}
    agg, wide, tests = e1_stats(D, cfg)
    agg.to_csv(os.path.join(D["tables"], "table_e1_benchmark_long.csv"), index=False)
    wide.to_csv(os.path.join(D["tables"], "table_e1_benchmark_wide.csv"), index=False)
    tests.to_csv(os.path.join(D["stats"], "e1_paired_tests.csv"), index=False)
    S["e1_paired_tests"] = tests.to_dict("records")
    M["e1"] = wide.to_dict("records")
    S["e3"] = e3_stats(D, cfg)
    # copy-through of other statistics
    for f in ["meta_regression.json"]:
        fp = os.path.join(D["stats"], f)
        if os.path.exists(fp):
            S[f.replace(".json", "")] = json.load(open(fp))
    for f in ["e5a_locked_test_metrics.csv", "e5a_locked_test_coverage.csv", "e5bc_temporal_family_metrics.csv", "e5bc_temporal_family_coverage.csv",
              "e5d_external_metrics.csv", "e5d_external_coverage.csv", "e6_efficiency.csv"]:
        fp = os.path.join(D["results"], f)
        if os.path.exists(fp):
            M[f.replace(".csv", "")] = pd.read_csv(fp).to_dict("records")
    for f in ["strata_base_learner.json", "e5d_external_overlap_audit.json", "exclusions_biooil_dev.json", "exclusions_solid_dev.json",
              "exclusions_biooil_test.json", "exclusions_solid_test.json"]:
        fp = os.path.join(D["results"], f)
        if os.path.exists(fp):
            M[f.replace(".json", "")] = json.load(open(fp))
    # locked-test paired tests (per-study RMSE): each learner vs best, and protocol ablation for every learner
    fp = os.path.join(D["pred"], "e5a_locked_test_predictions.csv.gz")
    if os.path.exists(fp):
        lp = pd.read_csv(fp)
        lt = []
        for (t, ln), g in lp.groupby(["target", "learner"]):
            a = per_study_rmse(g[g.features == "base+P"], "pred"); b = per_study_rmse(g[g.features == "base"], "pred")
            a, b = a.align(b, join="inner")
            lt.append(dict(target=t, learner=ln, comparison="base+P_vs_base", **paired_comparison(a.values, b.values)))
        adj = holm([x["p"] for x in lt])
        for x, pa in zip(lt, adj):
            x["p_holm"] = float(pa)
        S["locked_protocol_ablation_all_learners"] = lt

    # locked test: study-cluster bootstrap CI for coverage (STRATA learner, base+P) and post-hoc sensitivity excluding
    # the single study with the largest squared-error share (reported as post hoc)
    fc = os.path.join(D["results"], "e5a_locked_test_coverage.csv")
    if os.path.exists(fp) and os.path.exists(fc):
        lc = pd.read_csv(fc); learner = json.load(open(os.path.join(D["results"], "strata_base_learner.json")))["learner"]
        cis = []
        for t in ["biooil", "solid"]:
            g = lp[(lp.target == t) & (lp.features == "base+P") & (lp.learner == learner)].copy()
            for cal in ["RC", "SC"]:
                row = lc[(lc.target == t) & (lc.features == "base+P") & (lc.alpha == cfg["alpha"]) & (lc.calibration == cal)].iloc[0]
                g["hit"] = (np.abs(g["y"] - g["pred"]) <= row["width"] / 2).astype(float)
                g["w"] = 1 / g["study"].map(g["study"].value_counts())
                est = float((g["w"] * g["hit"]).sum() / g["w"].sum())
                lo, hi = cluster_bootstrap_ci(g[["study", "hit", "w"]], lambda d: float((d["w"] * d["hit"]).sum() / d["w"].sum()), n_boot=cfg["bootstrap"], seed=0)
                cis.append(dict(target=t, calibration=cal, coverage_studies_recomputed=est, reported=float(row["coverage_studies"]), ci_low=lo, ci_high=hi,
                                n_studies=int(g["study"].nunique())))
        S["locked_coverage_ci"] = cis
        sens = []
        for (t, fs, ln), g in lp.groupby(["target", "features", "learner"]):
            r = g["y"] - g["pred"]
            sse = (r ** 2).groupby(g["study"]).sum()
            top = sse.idxmax(); keep = g["study"] != top
            sens.append(dict(target=t, features=fs, learner=ln, excluded_study=top, excluded_sse_share=float(sse.max() / sse.sum()),
                             rmse_all=float(np.sqrt(np.mean(r ** 2))), rmse_excl=float(np.sqrt(np.mean(r[keep] ** 2))),
                             r2_excl=float(1 - np.sum(r[keep] ** 2) / np.sum((g["y"][keep] - g["y"][keep].mean()) ** 2))))
        pd.DataFrame(sens).to_csv(os.path.join(D["stats"], "locked_sensitivity_exclude_top_study.csv"), index=False)
        S["locked_sensitivity_exclude_top_study"] = sens
    dump(S, os.path.join(D["results"], "statistics.json"))
    dump(M, os.path.join(D["results"], "metrics.json"))
    # raw_results.csv: concatenation of every per-run row from all experiments
    parts = []
    for f in sorted(os.listdir(D["results"])):
        if f.endswith(".csv") and f.startswith("e"):
            d = pd.read_csv(os.path.join(D["results"], f)); d.insert(0, "source_file", f); parts.append(d)
    pd.concat(parts, ignore_index=True).to_csv(os.path.join(D["results"], "raw_results.csv"), index=False)
    return S, M


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "full")
