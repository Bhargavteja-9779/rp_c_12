"""Publication figures generated exclusively from result files (PNG 300 dpi + PDF).

Palette: validated categorical slots 1-3 (blue #2a78d6, orange #eb6834, aqua #1baf7a; all-pairs CVD ΔE ≥ 9.2)
plus neutral grey. Aqua (contrast < 3:1) is always paired with a distinct marker and a direct label.
"""
from __future__ import annotations

import json, os, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.utils import out_dirs, load_config
from src.statistics.analyze import LEARNER_LABEL

BLUE, ORANGE, AQUA, GREY, INK, MUTED = "#2a78d6", "#eb6834", "#1baf7a", "#8a8984", "#0b0b0b", "#52514e"
TARGET_LABEL = {"biooil": "Bio-oil yield", "solid": "Solid yield"}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "axes.titlesize": 9, "axes.labelsize": 8,
                     "axes.edgecolor": MUTED, "axes.linewidth": 0.6, "xtick.color": MUTED, "ytick.color": MUTED,
                     "axes.grid": True, "grid.color": "#e4e3df", "grid.linewidth": 0.5, "legend.frameon": False,
                     "axes.spines.top": False, "axes.spines.right": False, "savefig.dpi": 300, "lines.linewidth": 1.5})


def save(fig, D, name):
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(D["figures"], f"{name}.{ext}"), bbox_inches="tight")
    plt.close(fig)


# ------------------------------------------------------------------ Fig 1 workflow (method schematic, no data)
def fig_workflow(D):
    fig, ax = plt.subplots(figsize=(7.2, 2.6)); ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 36)
    boxes = [(1, 20, 17, 13, "Curated literature DB\n3,693 runs · 188 studies\n(RADAR4Chem v1.0.0)"),
             (21, 20, 17, 13, "Locked split by study\n38 test studies\n(created before modelling)"),
             (41, 20, 17, 13, "Features\nbase: feedstock + conditions\nP: work-up & reporting"),
             (61, 20, 17, 13, "12 learners, equal budget\nrandom-row CV vs\nstudy-grouped CV"),
             (81, 20, 18, 13, "STRATA\nstudy-calibrated conformal\n+ k-shot EB offset"),
             (21, 2, 17, 13, "Heterogeneity\ndecomposition (τ², σ²w)\nmeta-regression"),
             (41, 2, 17, 13, "Generalisation\nlocked test · temporal\nfamily-out · external 4TU"),
             (61, 2, 17, 13, "Robustness, cost,\nsensitivity, error\nanalysis"),
             (81, 2, 18, 13, "Study-level statistics\nWilcoxon + Holm\ncluster bootstrap")]
    for x, y, w, h, t in boxes:
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.2", fc="#f3f2ee", ec=MUTED, lw=0.6))
        ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=6.5, color=INK)
    for x0, x1 in [(18, 21), (38, 41), (58, 61), (78, 81)]:
        ax.annotate("", (x1, 26.5), (x0, 26.5), arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))
    for xc in [29.5, 49.5, 69.5, 89.5]:
        ax.annotate("", (xc, 15.3), (xc, 19.7), arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.6))
    save(fig, D, "fig01_workflow")


# ------------------------------------------------------------------ Fig 2 dataset overview
def fig_dataset(D):
    from src.data.load import load_target
    fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.3))
    for i, (t, c) in enumerate([("biooil", BLUE), ("solid", ORANGE)]):
        ds = load_target(t, "dev")
        n = pd.Series(ds.groups).value_counts()
        axs[0].hist(n, bins=np.logspace(np.log10(2), np.log10(n.max() + 1), 15), histtype="step", color=c, lw=1.5, label=TARGET_LABEL[t])
        axs[1].hist(ds.y, bins=np.arange(0, 101, 5), histtype="step", color=c, lw=1.5, label=TARGET_LABEL[t])
    axs[0].set_xscale("log"); axs[0].set_xlabel("Runs per source study (development)"); axs[0].set_ylabel("Studies"); axs[0].legend(fontsize=6.5)
    axs[1].set_xlabel("Yield (wt%)"); axs[1].set_ylabel("Runs")
    from src.data.load import read_raw
    r = read_raw(); y = r.groupby("DOI")["year"].first()
    axs[2].hist(y, bins=np.arange(1980, 2028, 2), color=GREY, rwidth=0.85)
    axs[2].axvline(2018.5, color=MUTED, lw=0.8, ls="--"); axs[2].text(2018, axs[2].get_ylim()[1] * 0.9, "temporal\nsplit", fontsize=6, ha="right", color=MUTED)
    axs[2].set_xlabel("Publication year of source study"); axs[2].set_ylabel("Studies")
    for a, l in zip(axs, "abc"):
        a.set_title(f"({l})", loc="left", fontsize=8)
    fig.tight_layout(); save(fig, D, "fig02_dataset")


# ------------------------------------------------------------------ Fig 3 random vs grouped (dumbbell)
def fig_optimism(D):
    w = pd.read_csv(os.path.join(D["tables"], "table_e1_benchmark_wide.csv"))
    w = w[w.features == "base"]
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.0), sharey=True)
    order = w[w.target == "biooil"].sort_values("rmse_grouped_study_cv")["learner"].tolist()
    for ax, t in zip(axs, ["biooil", "solid"]):
        s = w[w.target == t].set_index("learner").loc[order]
        yv = np.arange(len(order))
        ax.hlines(yv, s["rmse_random_row_cv"], s["rmse_grouped_study_cv"], color="#cfcec9", lw=1.2)
        ax.plot(s["rmse_random_row_cv"], yv, "o", color=ORANGE, ms=5, label="Random row 5-fold CV")
        ax.plot(s["rmse_grouped_study_cv"], yv, "s", color=BLUE, ms=5, label="Study-grouped 10-fold CV")
        ax.set_yticks(yv, [LEARNER_LABEL[l] for l in order]); ax.invert_yaxis()
        ax.set_xlabel("RMSE (wt%)"); ax.set_title(TARGET_LABEL[t], loc="left")
    axs[0].legend(loc="lower right", fontsize=6.5)
    fig.tight_layout(); save(fig, D, "fig03_random_vs_grouped")


# ------------------------------------------------------------------ Fig 4 study offsets (caterpillar)
def fig_offsets(D, S):
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.6))
    for ax, t in zip(axs, ["biooil", "solid"]):
        p = pd.read_csv(os.path.join(D["pred"], f"e3_{t}__base.csv.gz"))
        p["r"] = p["y"] - p["pred"]
        g = p.groupby("study")["r"].agg(["mean", "std", "size"]).sort_values("mean")
        x = np.arange(len(g))
        se = g["std"].fillna(0) / np.sqrt(g["size"])
        ax.vlines(x, g["mean"] - 1.96 * se, g["mean"] + 1.96 * se, color="#cfcec9", lw=0.8)
        ax.plot(x, g["mean"], "o", ms=2.5, color=BLUE)
        ax.axhline(0, color=MUTED, lw=0.6)
        h = S["e3"][t]["heterogeneity"]["base"]
        ax.text(0.02, 0.95, f"between-study share = {h['share_between']:.2f}\n(95% CI {h['share_ci'][0]:.2f}–{h['share_ci'][1]:.2f})",
                transform=ax.transAxes, va="top", fontsize=6.5, color=INK)
        ax.set_xlabel("Development study (sorted)"); ax.set_ylabel("Mean out-of-study residual (wt%)")
        ax.set_title(TARGET_LABEL[t], loc="left")
    fig.tight_layout(); save(fig, D, "fig04_study_offsets")


# ------------------------------------------------------------------ Fig 5 coverage across settings
def fig_coverage(D, S, M, alpha=0.1):
    rows = []
    for t in ["biooil", "solid"]:
        for c in S["e3"][t]["coverage"]:
            if c["alpha"] == alpha and c["features"] == "base+P":
                rows.append(dict(setting="Dev. CV\n(unseen studies)", target=t, cal=c["calibration"], cov=c["coverage_studies"]))
    for key, label in [("e5a_locked_test_coverage", "Locked test\n(38 studies)"), ("e5bc_temporal_family_coverage", None), ("e5d_external_coverage", "External\n4TU HTC")]:
        for r in M.get(key, []):
            if r["alpha"] != alpha or r.get("features") not in ("base+P", "base"):
                continue
            if key == "e5d_external_coverage" and r["tag"] != "external_4TU":
                continue
            if key != "e5d_external_coverage" and r.get("features") != "base+P":
                continue
            lab = label or {"temporal": "Temporal\n(≤2018→≥2019)", "family_out": "Feedstock\nfamily-out"}[r["tag"]]
            rows.append(dict(setting=lab, target=r["target"], cal=r["calibration"], cov=r["coverage_studies"]))
    df = pd.DataFrame(rows).groupby(["setting", "target", "cal"], as_index=False)["cov"].mean()
    order = ["Dev. CV\n(unseen studies)", "Locked test\n(38 studies)", "Temporal\n(≤2018→≥2019)", "Feedstock\nfamily-out", "External\n4TU HTC"]
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.9), sharey=True, gridspec_kw={"width_ratios": [4, 5]})
    for ax, t in zip(axs, ["biooil", "solid"]):
        settings = [o for o in order if o in set(df[df.target == t]["setting"])]
        x = np.arange(len(settings))
        for off, cal, col, mk, lab in [(-0.12, "RC", ORANGE, "o", "Row-calibrated (RC)"), (0.12, "SC", BLUE, "s", "Study-calibrated (SC)")]:
            v = [df[(df.setting == s) & (df.target == t) & (df.cal == cal)]["cov"].mean() for s in settings]
            ax.plot(x + off, v, mk, color=col, ms=5, label=lab, ls="none")
        ax.axhline(1 - alpha, color=MUTED, lw=0.8, ls="--"); ax.text(len(settings) - 0.5, 1 - alpha + 0.005, "nominal 0.90", fontsize=6, ha="right", color=MUTED)
        ax.set_xticks(x, settings, fontsize=6); ax.set_title(TARGET_LABEL[t], loc="left"); ax.set_xlim(-0.5, len(settings) - 0.5)
        ax.set_ylabel("Study-weighted coverage of 90% intervals")
    axs[0].legend(loc="lower left", fontsize=6.5)
    fig.tight_layout(); save(fig, D, "fig05_coverage")


# ------------------------------------------------------------------ Fig 6 k-shot
def fig_kshot(D, S):
    fig, axs = plt.subplots(2, 2, figsize=(7.2, 4.4), sharex=True)
    for j, t in enumerate(["biooil", "solid"]):
        ks = pd.DataFrame(S["e3"][t]["kshot_summary"]); ks = ks[ks.features == "base+P"]
        k0 = ks[ks.k == 0].iloc[0]
        for mode, col, mk, lab in [("raw", ORANGE, "o", "Raw mean offset"), ("eb", BLUE, "s", "Empirical-Bayes offset (STRATA)")]:
            s = pd.concat([k0.to_frame().T, ks[ks["mode"] == mode]]).sort_values("k")
            axs[0, j].plot(s["k"].astype(int), s["median_study_rmse"].astype(float), marker=mk, color=col, ms=4, label=lab)
            axs[1, j].plot(s["k"].astype(int), s["width"].astype(float), marker=mk, color=col, ms=4, label=lab)
        axs[0, j].set_title(TARGET_LABEL[t], loc="left"); axs[0, j].set_ylabel("Median per-study RMSE (wt%)")
        axs[1, j].set_ylabel("Width of 90% interval (wt%)"); axs[1, j].set_xlabel("k labelled runs from the new study")
    axs[0, 0].legend(fontsize=6.5)
    fig.tight_layout(); save(fig, D, "fig06_kshot")


# ------------------------------------------------------------------ Fig 7 robustness
def fig_robustness(D, alpha=0.1):
    r = pd.read_csv(os.path.join(D["results"], "e4_robustness.csv")); r = r[r.features == "base+P"]
    cols = [(t, e) for t in ["biooil", "solid"] for e in ["feature_noise", "training_studies"]]
    fig, axs = plt.subplots(2, 4, figsize=(7.2, 3.8), sharex="col")
    for j, (t, exp) in enumerate(cols):
        s = r[(r.target == t) & (r.experiment == exp)]
        g = s[s.calibration == "SC"].groupby("level")["rmse"].agg(["mean", "std"])
        axs[0, j].errorbar(g.index, g["mean"], yerr=g["std"], fmt="-o", color=GREY, ms=3.5, capsize=2, lw=1.2)
        for cal, col, mk, lab in [("RC", ORANGE, "o", "RC"), ("SC", BLUE, "s", "SC")]:
            c = s[s.calibration == cal].groupby("level")["coverage_studies"].mean()
            axs[1, j].plot(c.index, c.values, "-" + mk, color=col, ms=3.5, label=lab)
        axs[1, j].axhline(1 - alpha, color=MUTED, ls="--", lw=0.7); axs[1, j].set_ylim(0.4, 1.0)
        axs[0, j].set_title(f"{TARGET_LABEL[t]}\n{'feature noise' if exp == 'feature_noise' else 'training studies'}", loc="left", fontsize=7)
        axs[1, j].set_xlabel("noise (× SD)" if exp == "feature_noise" else "fraction of studies", fontsize=7)
    axs[0, 0].set_ylabel("RMSE (wt%)"); axs[1, 0].set_ylabel("Coverage (study-weighted)")
    axs[1, 0].legend(fontsize=6.5, loc="lower left")
    fig.tight_layout(); save(fig, D, "fig07_robustness")


# ------------------------------------------------------------------ Fig 8 efficiency
def fig_efficiency(D):
    e = pd.read_csv(os.path.join(D["results"], "e6_efficiency.csv"))
    w = pd.read_csv(os.path.join(D["tables"], "table_e1_benchmark_wide.csv"))
    w = w[(w.target == "biooil") & (w.features == "base")].set_index("learner")
    e = e.set_index("learner").join(w["rmse_grouped_study_cv"])
    fig, ax = plt.subplots(figsize=(3.5, 2.8))
    ax.plot(e["fit_s"], e["rmse_grouped_study_cv"], "o", color=BLUE, ms=5)
    for l, r in e.iterrows():
        ax.annotate(LEARNER_LABEL[l], (r["fit_s"], r["rmse_grouped_study_cv"]), fontsize=6, xytext=(3, 2), textcoords="offset points", color=INK)
    ax.set_xscale("log"); ax.set_xlabel("Fit time on development set, 1 thread (s)"); ax.set_ylabel("Study-grouped CV RMSE, bio-oil (wt%)")
    fig.tight_layout(); save(fig, D, "fig08_efficiency")


# ------------------------------------------------------------------ Fig 9 error analysis by extraction solvent
def fig_error(D):
    e = pd.read_csv(os.path.join(D["results"], "e8_error_analysis.csv"))
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.8), sharey=False)
    for ax, t in zip(axs, ["biooil", "solid"]):
        s = e[(e.target == t) & (e.dimension == "extraction_solvent") & (e.n_studies >= 3)].sort_values("bias")
        y = np.arange(len(s))
        ax.hlines(y, 0, s["bias"], color="#cfcec9", lw=1.2); ax.plot(s["bias"], y, "o", color=BLUE, ms=5)
        ax.axvline(0, color=MUTED, lw=0.6)
        ax.set_yticks(y, [f"{l} (n={n}, {k} studies)" for l, n, k in zip(s["level"], s["n"], s["n_studies"])], fontsize=6.3)
        ax.set_xlabel("Mean out-of-study residual (observed − predicted, wt%)"); ax.set_title(TARGET_LABEL[t] + " — by extraction solvent", loc="left")
    fig.tight_layout(); save(fig, D, "fig09_error_by_solvent")


# ------------------------------------------------------------------ Fig 10 parity random vs grouped (best learner)
def fig_parity(D, learner):
    fig, axs = plt.subplots(1, 4, figsize=(7.2, 2.0), sharex=True, sharey=True)
    i = 0
    for t in ["biooil", "solid"]:
        p = pd.read_csv(os.path.join(D["pred"], f"e1_{t}__base__{learner}.csv.gz"))
        for col, lab, c in [("random", "random CV", ORANGE), ("grouped_11", "grouped CV", BLUE)]:
            ax = axs[i]; i += 1
            ax.plot(p["y"], p[col], ".", ms=1.5, color=c, alpha=0.5)
            ax.plot([0, 100], [0, 100], color=MUTED, lw=0.6)
            rm = float(np.sqrt(np.mean((p["y"] - p[col]) ** 2)))
            ax.set_title(f"{TARGET_LABEL[t]}, {lab}\nRMSE {rm:.1f}", loc="left", fontsize=6.8)
            ax.set_xlabel("Observed (wt%)")
    axs[0].set_ylabel("Predicted (wt%)")
    fig.tight_layout(); save(fig, D, "fig10_parity")


# ------------------------------------------------------------------ graphical abstract (from results)
def graphical_abstract(D, S, M):
    w = pd.read_csv(os.path.join(D["tables"], "table_e1_benchmark_wide.csv"))
    b = w[(w.target == "biooil") & (w.features == "base")].sort_values("rmse_grouped_study_cv").iloc[0]
    cov = {c["calibration"]: c["coverage_studies"] for c in S["e3"]["biooil"]["coverage"] if c["alpha"] == 0.1 and c["features"] == "base+P"}
    fig, axs = plt.subplots(1, 3, figsize=(6.7, 2.0), gridspec_kw={"width_ratios": [1, 1, 1.1]})
    axs[0].bar([0, 1], [b["r2_random_row_cv"], b["r2_grouped_study_cv"]], color=[ORANGE, BLUE], width=0.6)
    axs[0].set_xticks([0, 1], ["random\nsplit", "new\nstudy"]); axs[0].set_ylabel("R² (bio-oil yield)"); axs[0].set_title("Accuracy is overstated", loc="left", fontsize=7.5)
    axs[1].bar([0, 1], [cov["RC"], cov["SC"]], color=[ORANGE, BLUE], width=0.6); axs[1].axhline(0.9, color=MUTED, ls="--", lw=0.8)
    axs[1].set_xticks([0, 1], ["row-\ncalibrated", "study-\ncalibrated"]); axs[1].set_ylim(0.5, 1); axs[1].set_ylabel("Coverage (90% PI)")
    axs[1].set_title("Intervals for a new study", loc="left", fontsize=7.5)
    ks = pd.DataFrame(S["e3"]["biooil"]["kshot_summary"]); ks = ks[(ks.features == "base+P") & (ks["mode"].isin(["none", "eb"]))].sort_values("k")
    axs[2].plot(ks["k"], ks["median_study_rmse"], "-s", color=BLUE, ms=4)
    axs[2].set_xlabel("k runs from the new study"); axs[2].set_ylabel("Median RMSE (wt%)"); axs[2].set_title("A few local runs help", loc="left", fontsize=7.5)
    fig.tight_layout(); save(fig, D, "graphical_abstract")


def run(mode="full"):
    D = out_dirs(mode)
    S = json.load(open(os.path.join(D["results"], "statistics.json")))
    M = json.load(open(os.path.join(D["results"], "metrics.json")))
    learner = json.load(open(os.path.join(D["results"], "strata_base_learner.json")))["learner"]
    for f, args in [(fig_workflow, (D,)), (fig_dataset, (D,)), (fig_optimism, (D,)), (fig_offsets, (D, S)), (fig_coverage, (D, S, M)),
                    (fig_kshot, (D, S)), (fig_robustness, (D,)), (fig_efficiency, (D,)), (fig_error, (D,)), (fig_parity, (D, learner)),
                    (graphical_abstract, (D, S, M))]:
        try:
            f(*args)
        except Exception as e:
            print(f"figure {f.__name__} failed: {e}")


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "full")
