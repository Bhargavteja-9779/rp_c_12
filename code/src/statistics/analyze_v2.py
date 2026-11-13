"""v2 analyses: E12 (T1–T5) for all splits, E13 trend table, E14 tests (dev exploratory; locked confirmatory C1),
quality targets (A2) and the capability matrix. Writes results/statistics_v2.json and tables/table_v2_*.csv."""
from __future__ import annotations

import json, os, sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.statistics import analyze_trends
from src.statistics.stats import paired_comparison, holm
from src.utils import out_dirs, dump


def ranking_tests(K, confirmatory=False):
    P = K.groupby(["target", "study", "method"]).regret.mean().unstack()
    rnd = K.groupby(["target", "study"]).random.mean()
    tests = []
    for t, g in P.groupby(level=0):
        g = g.droplevel(0)
        rule = "rule_T325" if t == "biooil" else "rule_lowest_T"
        for m in ["A", "W", "PD"]:
            for ref in ([rule] if confirmatory else [c for c in g.columns if c.startswith("rule") and g[c].notna().any()] + ["random"]):
                b = rnd.loc[t] if ref == "random" else g[ref]
                a, b = g[m].align(b, join="inner")
                alt = "less" if (confirmatory and t == "biooil") else "two-sided"
                tests.append(dict(target=t, method=m, reference=ref, n=int(len(a)), median_method=float(a.median()), median_ref=float(b.median()),
                                  alternative=alt, **{k: v for k, v in paired_comparison(a.values, b.values, alternative=alt).items()
                                                      if k in ("p", "median_diff", "ci_low", "ci_high", "rank_biserial")}))
    fam = [x for x in tests if x["target"] == "biooil"] if confirmatory else tests
    for x, p in zip(fam, holm([x["p"] for x in fam])):
        x["p_holm"] = float(p)
    return tests


def contrast_types(R):
    s = R.groupby(["target", "model", "type", "seed"]).agg(sse=("sse", "sum"), ss=("ss", "sum"), n=("n", "sum")).reset_index()
    s["r2"] = 1 - s.sse / s.ss
    return s.groupby(["target", "type", "model"]).agg(r2=("r2", "mean"), n_pairs=("n", "mean")).reset_index()


def run(mode="full"):
    D = out_dirs(mode); S = {}
    for split in ["dev", "locked", "dev_quality", "locked_quality"]:
        if os.path.exists(os.path.join(D["results"], f"e12_study_metrics_{split}.csv")):
            S[f"e12_{split}"] = analyze_trends.run(mode, split)
    e13 = pd.read_csv(os.path.join(D["results"], "e13_empirical_trends.csv")); S["e13"] = e13.to_dict("records")
    for sfx, conf in [("", False), ("_locked", True)]:
        f = os.path.join(D["results"], f"e14b_ranking_heuristics{sfx}.csv")
        if os.path.exists(f):
            K = pd.read_csv(f)
            S[f"e14b{sfx}"] = ranking_tests(K, confirmatory=conf)
            S[f"e14b{sfx}_medians"] = K.groupby(["target", "study", "method"]).regret.mean().unstack().groupby(level=0).median().reset_index().to_dict("records")
            S[f"e14b{sfx}_random_median"] = K.groupby(["target", "study"]).random.mean().groupby(level=0).median().to_dict()
        f = os.path.join(D["results"], f"e14a_contrast_types{sfx}.csv")
        if os.path.exists(f):
            S[f"e14a{sfx}"] = contrast_types(pd.read_csv(f)).to_dict("records")
    dump(S, os.path.join(D["results"], "statistics_v2.json"))
    # ---------------- tables
    TL = {"biooil": "Bio-oil yield", "solid": "Solid yield", "hhv_biooil": "Bio-oil HHV", "c_biooil": "Bio-oil C"}
    e = e13.copy(); e["Target"] = e.target.map(TL)
    e["Variable"] = e.variable.map({"T_C": "Temperature", "log_t_min": "Residence time"})
    e["Median slope [95% CI]"] = [f"{a:+.2f} [{b:+.2f}, {c:+.2f}]" for a, b, c in zip(e.median_slope, e.slope_ci_low, e.slope_ci_high)]
    e[["Target", "Variable", "unit", "band", "n_studies", "n_pairs", "Median slope [95% CI]", "frac_studies_same_sign", "sd_slope_between_studies"]].rename(
        columns={"unit": "Unit", "band": "Band (°C)", "n_studies": "Studies", "n_pairs": "Pairs", "frac_studies_same_sign": "Studies with same sign",
                 "sd_slope_between_studies": "Between-study SD of slope"}).round(2).to_csv(os.path.join(D["tables"], "table_v2_empirical_trends.csv"), index=False)
    rows = []
    for split, lab in [("dev", "Development (unseen studies)"), ("locked", "Locked test"), ("dev_quality", "Development (unseen studies)"), ("locked_quality", "Locked test")]:
        if f"e12_{split}" not in S:
            continue
        for r in S[f"e12_{split}"]["T1_T4_T5_summary"]:
            if r["learner"] != "xgb":
                continue
            rows.append({"Target": TL[r["target"]], "Setting": lab, "Model": r["model"], "Level R²": r.get("level_r2_same_studies"),
                         "Contrast R²": r["contrast_r2"], "Median within-study Spearman": r.get("median_spearman"),
                         "Contrast interval coverage": r.get("contrast_coverage_studies"), "Contrast interval width": r.get("contrast_width"),
                         "Level interval width": r.get("level_width")})
    pd.DataFrame(rows).round(3).to_csv(os.path.join(D["tables"], "table_v2_levels_vs_contrasts.csv"), index=False)
    rk = []
    for sfx, lab in [("", "Development (exploratory)"), ("_locked", "Locked test (confirmatory)")]:
        for x in S.get(f"e14b{sfx}", []):
            if x["reference"] == "random":
                continue
            rk.append({"Setting": lab, "Target": TL[x["target"]], "Model": x["method"], "Rule of thumb": x["reference"].replace("rule_", ""), "Studies": x["n"],
                       "Median regret, model (wt%)": x["median_method"], "Median regret, rule (wt%)": x["median_ref"],
                       "Median paired difference [95% CI]": f"{x['median_diff']:+.2f} [{x['ci_low']:+.2f}, {x['ci_high']:+.2f}]",
                       "p (Holm)": x.get("p_holm", x["p"]), "Test": x["alternative"]})
    pd.DataFrame(rk).round(4).to_csv(os.path.join(D["tables"], "table_v2_ranking.csv"), index=False)
    return S


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "full")
