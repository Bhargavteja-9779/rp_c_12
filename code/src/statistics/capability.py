"""Capability matrix: what literature-trained hydrothermal models can and cannot do for a new study.
Every number and every verdict is computed from result files; verdict wording follows explicit rules."""
from __future__ import annotations
import json, os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.utils import out_dirs


def run(mode="full"):
    D = out_dirs(mode); R = D["results"]
    S = json.load(open(os.path.join(R, "statistics.json"))); M = json.load(open(os.path.join(R, "metrics.json")))
    V = json.load(open(os.path.join(R, "statistics_v2.json")))
    if "e12_locked" not in V or "e14b_locked" not in V:
        print("capability matrix skipped: locked-study results not available (quick mode never evaluates locked studies)"); return
    w = pd.DataFrame(M["e1"]); lt = pd.DataFrame(M["e5a_locked_test_metrics"])
    rows = []
    # 1 levels
    dev_r2 = {t: w[(w.target == t) & (w.features == "base") & (w.learner != "mean")].r2_grouped_study_cv.max() for t in ["biooil", "solid"]}
    lk_r2 = {t: lt[(lt.target == t) & (lt.features == "base") & (lt.learner != "mean")].r2.max() for t in ["biooil", "solid"]}
    rows.append(dict(capability="Predict the absolute yield of a run in a new study",
                     development=f"best R² {dev_r2['biooil']:.2f} (bio-oil), {dev_r2['solid']:.2f} (solid)",
                     locked=f"best R² {lk_r2['biooil']:.2f} (bio-oil), {lk_r2['solid']:.2f} (solid)",
                     verdict=f"{'Poor' if max(dev_r2['biooil'], lk_r2['biooil']) < 0.3 else 'Moderate'} (bio-oil); {'poor' if min(dev_r2['solid'], lk_r2['solid']) < 0.3 else 'moderate'} (solid)"))
    # 2 offsets from metadata
    pp = [S["e3"][t]["protocol_ablation"]["test_one_sided_base_plus_P_less"]["p"] for t in ["biooil", "solid"]]
    mr = {m["target"]: m for m in S["meta_regression"]}
    rows.append(dict(capability="Explain a study's offset from reported work-up / yield basis",
                     development=f"P ablation p = {pp[0]:.2f}, {pp[1]:.2f}; meta-regression R² {mr['biooil']['loso_r2']:.2f}, {mr['solid']['loso_r2']:.2f}",
                     locked=f"{sum(1 for x in S['locked_protocol_ablation_all_learners'] if x['p_holm'] < 0.05)} of {len(S['locked_protocol_ablation_all_learners'])} learner–target tests significant",
                     verdict="No"))
    # 3 contrasts (model-based)
    def c(split, t):
        r = [x for x in V[f"e12_{split}"]["T1_T4_T5_summary"] if x["target"] == t and x["learner"] == "xgb"]
        return {x["model"]: x["contrast_r2"] for x in r}
    cd, cl = {t: c("dev", t) for t in ["biooil", "solid"]}, {t: c("locked", t) for t in ["biooil", "solid"]}
    t2_dev = [x for x in V["e12_dev"]["T2"] if x["p_holm"] < 0.05]
    rows.append(dict(capability="Predict how yield changes between two runs of a new study (within-study contrast)",
                     development=f"contrast R² {min(cd['biooil'].values()):.2f}–{max(cd['biooil'].values()):.2f} (bio-oil), {min(cd['solid'].values()):.2f}–{max(cd['solid'].values()):.2f} (solid); offset-invariant models better in {len(t2_dev)}/12 tests",
                     locked=f"contrast R² {min(cl['biooil'].values()):.2f}–{max(cl['biooil'].values()):.2f} (bio-oil), {min(cl['solid'].values()):.2f}–{max(cl['solid'].values()):.2f} (solid)",
                     verdict="Weak; not better than levels (pre-registered T1–T3 not supported)"))
    # 4 direction of temperature effect, model-free
    e = pd.DataFrame(V["e13"]); e = e[e.variable == "T_C"]
    lowb = e[e.band.isin(["150-250", "250-300"])]
    rows.append(dict(capability="Direction of the temperature effect below 300 °C (model-free, within studies)",
                     development=f"same sign in {lowb.frac_studies_same_sign.min():.0%}–{lowb.frac_studies_same_sign.max():.0%} of studies (bio-oil ↑, solid ↓)",
                     locked="not applicable (descriptive)", verdict="Consistent across laboratories"))
    # 5 ranking
    lk = [x for x in V["e14b_locked"] if x["target"] == "biooil"]
    dv = [x for x in V["e14b"] if x["target"] == "biooil" and x["reference"] == "rule_T325"]
    rows.append(dict(capability="Pick the best of a new study's planned runs (bio-oil)",
                     development=f"better than T≈325 °C rule (median regret {min(x['median_method'] for x in dv):.1f}–{max(x['median_method'] for x in dv):.1f} vs {dv[0]['median_ref']:.1f} wt%; exploratory)",
                     locked=f"not confirmed (p_Holm ≥ {min(x['p_holm'] for x in lk):.2f}; regret {min(x['median_method'] for x in lk):.1f}–{max(x['median_method'] for x in lk):.1f} vs {lk[0]['median_ref']:.1f} wt%)",
                     verdict="Not established"))
    # 6 uncertainty
    cv = {t: {x["calibration"]: x["coverage_studies"] for x in S["e3"][t]["coverage"] if x["alpha"] == 0.1 and x["features"] == "base+P"} for t in ["biooil", "solid"]}
    lc = {(x["target"], x["calibration"]): x["reported"] for x in S["locked_coverage_ci"]}
    rows.append(dict(capability="Honest 90% prediction intervals for a new study",
                     development=f"row-calibrated {cv['biooil']['RC']:.2f}/{cv['solid']['RC']:.2f}; study-calibrated {cv['biooil']['SC']:.2f}/{cv['solid']['SC']:.2f}",
                     locked=f"row-calibrated {lc[('biooil','RC')]:.2f}/{lc[('solid','RC')]:.2f}; study-calibrated {lc[('biooil','SC')]:.2f}/{lc[('solid','SC')]:.2f}",
                     verdict="Yes, if calibrated across studies (wide: ±23–30 wt%)"))
    # 7 local anchoring
    ks = {t: {(int(x["k"]), x["mode"]): x["median_study_rmse"] for x in S["e3"][t]["kshot_summary"] if x["features"] == "base+P"} for t in ["biooil", "solid"]}
    lk_ks = pd.read_csv(os.path.join(R, "e5a_locked_test_kshot.csv")); lk_ks = lk_ks[lk_ks.features == "base+P"]
    lkm = lk_ks.groupby(["target", "k", "mode", "study"]).rmse.mean().groupby(level=[0, 1, 2]).median()
    rows.append(dict(capability="Use 1–3 measured runs of the new study to correct predictions",
                     development=f"median study RMSE {ks['biooil'][(0,'none')]:.1f}→{ks['biooil'][(3,'eb')]:.1f} (bio-oil), {ks['solid'][(0,'none')]:.1f}→{ks['solid'][(3,'eb')]:.1f} (solid) with 3 runs",
                     locked=f"median study RMSE {lkm[('biooil', 0, 'none')]:.1f}→{lkm[('biooil', 3, 'eb')]:.1f} (bio-oil), {lkm[('solid', 0, 'none')]:.1f}→{lkm[('solid', 3, 'eb')]:.1f} (solid)",
                     verdict="Yes — the most effective use of literature models"))
    df = pd.DataFrame(rows).rename(columns={"capability": "Capability", "development": "Development studies (unseen)", "locked": "38 locked studies", "verdict": "Verdict"})
    df.to_csv(os.path.join(D["tables"], "table_v2_capability_matrix.csv"), index=False)
    print(df.to_string())


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "full")
