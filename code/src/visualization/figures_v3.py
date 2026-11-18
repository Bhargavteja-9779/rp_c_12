"""v3 figures (deployment curves, case studies, STRATA-Lab workflow, predicted vs observed with intervals) from result files."""
from __future__ import annotations

import json, os, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.utils import out_dirs
from src.visualization.figures import BLUE, ORANGE, AQUA, GREY, INK, MUTED, save

TL = {"biooil": "Bio-oil yield", "solid": "Solid yield"}
STY = {"A": (GREY, "o", "A · literature only"), "B": (BLUE, "s", "B · STRATA"), "C": (ORANGE, "^", "C · local runs only")}


def fig_deployment(D):
    S = json.load(open(os.path.join(D["results"], "statistics_v3.json")))
    panels = [("dev", "biooil"), ("dev", "solid"), ("locked", "biooil"), ("locked", "solid"), ("external", "solid")]
    title = {"dev": "Development", "locked": "Locked", "external": "External 4TU"}
    fig, axs = plt.subplots(2, 5, figsize=(7.2, 3.9), sharex=True)
    for j, (st, t) in enumerate(panels):
        s = pd.DataFrame(S[f"e15_{st}_summary"]); s = s[(s.target == t) & (s.order == "design")]
        for m, (c, mk, lab) in STY.items():
            q = s[s.strategy == m].sort_values("k")
            if m != "A":
                q = q[q.k > 0]
            axs[0, j].plot(q.k, q.median_rmse, "-" + mk, color=c, ms=3.5, lw=1.2, label=lab)
            axs[1, j].plot(q.k, q.width / 2, "-" + mk, color=c, ms=3.5, lw=1.2)
        axs[0, j].set_title(f"{title[st]}\n{TL[t]}", loc="left", fontsize=7)
        axs[1, j].set_xlabel("local runs k", fontsize=7); axs[1, j].set_xticks([0, 1, 2, 3, 5])
    axs[0, 0].set_ylabel("Median per-study RMSE (wt%)", fontsize=7); axs[1, 0].set_ylabel("90% half-width (wt%)", fontsize=7)
    axs[0, 0].legend(fontsize=5.5, loc="upper right")
    fig.tight_layout(); save(fig, D, "fig14_deployment")


def fig_case(D):
    r = pd.read_csv(os.path.join(D["pred"], "e17_case_runs.csv.gz")); sel = json.load(open(os.path.join(D["stats"], "e17_selection.json")))
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.0))
    for ax, t in zip(axs, ["biooil", "solid"]):
        q0 = r[(r.target == t) & (r.k == 0)]; q3 = r[(r.target == t) & (r.k == 3)]
        x0 = q0["T"].to_numpy() + np.random.default_rng(0).uniform(-2, 2, len(q0))
        ax.errorbar(x0 - 2, q0.A, yerr=q0.q_A, fmt="o", color=GREY, ms=2.5, lw=0.6, alpha=0.6, label="A · literature, k = 0")
        ax.errorbar(x0 + 2, q3.B, yerr=q3.q_B, fmt="s", color=BLUE, ms=2.5, lw=0.6, alpha=0.6, label="B · STRATA, k = 3")
        ax.axhspan(q3.C.iloc[0] - q3.q_C.iloc[0], q3.C.iloc[0] + q3.q_C.iloc[0], color=ORANGE, alpha=0.08, lw=0)
        ax.axhline(q3.C.iloc[0], color=ORANGE, lw=1.0, ls="--", label="C · local mean, k = 3")
        ax.plot(x0, q0.y, "k.", ms=4, label="observed")
        m = q3.measured.to_numpy()
        ax.plot(x0[m], q0.y.to_numpy()[m], "o", mfc="none", mec=INK, ms=8, mew=1.0, label="measured (k = 3)")
        s = sel[t]
        ax.set_title(f"{TL[t]}: {s['feedstock'][:28]} ({s['process']})", loc="left", fontsize=7)
        ax.set_xlabel("Temperature (°C)"); ax.set_ylabel("Yield (wt%)")
    axs[0].legend(fontsize=5.5, loc="upper left")
    fig.tight_layout(); save(fig, D, "fig15_case_study")


def fig_workflow(D):
    fig, ax = plt.subplots(figsize=(7.2, 2.4)); ax.axis("off"); ax.set_xlim(0, 100); ax.set_ylim(0, 30)
    steps = ["1 Feedstock &\nconditions\n(composition,\nT, t, loading)", "2 Literature\nprediction\n(A)", "3 Uncertainty &\napplicability\n(study-calibrated\nPI, domain score)",
             "4 Local anchoring\n(1–3 designed runs;\nSTRATA B, compared\nwith local only C)", "5 Plan next runs\n(screen within\nPI; no fine\noptimisation)", "6 Decision report\n(predictions, PI,\nruns needed,\nlimitations)"]
    for i, t in enumerate(steps):
        x = 1 + i * 16.5
        ax.add_patch(FancyBboxPatch((x, 6), 14.5, 18, boxstyle="round,pad=0.3,rounding_size=1.2", fc="#eef4fc" if i in (2, 3) else "#f3f2ee", ec=MUTED, lw=0.6))
        ax.text(x + 7.25, 15, t, ha="center", va="center", fontsize=5.8, color=INK)
        if i < 5:
            ax.annotate("", (x + 16.3, 15), (x + 14.9, 15), arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))
    ax.text(50, 2, "Evidence from this study: steps 3–4 validated retrospectively on development, locked and external studies; step 5 limited to screening.",
            ha="center", fontsize=6, color=MUTED)
    save(fig, D, "fig16_strata_lab_workflow")


def fig_pred_obs(D):
    r = pd.read_csv(os.path.join(D["pred"], "e15_locked_design_runs.csv.gz"))
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.0))
    for ax, t in zip(axs, ["biooil", "solid"]):
        q0 = r[(r.target == t) & (r.k == 0)]; q3 = r[(r.target == t) & (r.k == 3)]
        ax.errorbar(q0.y, q0.A, yerr=q0.q_A, fmt="o", color=GREY, ms=2, lw=0.3, alpha=0.35, label="A · k = 0")
        ax.errorbar(q3.y + 0.4, q3.B, yerr=q3.q_B, fmt="s", color=BLUE, ms=2, lw=0.3, alpha=0.5, label="B · k = 3")
        ax.plot([0, 100], [0, 100], color=MUTED, lw=0.6)
        cA = float(np.mean(np.abs(q0.y - q0.A) <= q0.q_A)); cB = float(np.mean(np.abs(q3.y - q3.B) <= q3.q_B))
        ax.set_title(f"{TL[t]}, locked studies (query runs)\nrun-level coverage A {cA:.2f}, B {cB:.2f}", loc="left", fontsize=7)
        ax.set_xlabel("Observed (wt%)"); ax.set_ylabel("Predicted ± 90% PI (wt%)"); ax.set_xlim(0, 100); ax.set_ylim(-30, 130)
    axs[0].legend(fontsize=6, loc="upper left")
    fig.tight_layout(); save(fig, D, "fig17_pred_obs_intervals")


def graphical_abstract_v3(D):
    """Three panels: random split vs new study; study- vs row-calibrated coverage; deployment curve (development bio-oil)."""
    w = pd.read_csv(os.path.join(D["tables"], "table_e1_benchmark_wide.csv"))
    b = w[(w.target == "biooil") & (w.features == "base")].sort_values("rmse_grouped_study_cv").iloc[0]
    S = json.load(open(os.path.join(D["results"], "statistics.json")))
    cv = {x["calibration"]: x["coverage_studies"] for x in S["e3"]["biooil"]["coverage"] if x["alpha"] == 0.1 and x["features"] == "base+P"}
    V = json.load(open(os.path.join(D["results"], "statistics_v3.json")))
    s = pd.DataFrame(V["e15_dev_summary"]); s = s[(s.target == "biooil") & (s.order == "design")]
    fig, axs = plt.subplots(1, 3, figsize=(6.64, 2.66), gridspec_kw={"width_ratios": [1, 1, 1.5]})
    axs[0].bar([0, 1], [b["rmse_random_row_cv"], b["rmse_grouped_study_cv"]], color=[ORANGE, BLUE], width=0.6)
    axs[0].set_xticks([0, 1], ["random\nsplit", "new\nstudy"]); axs[0].set_ylabel("RMSE, bio-oil yield (wt%)")
    axs[0].set_title("1  Random splits\nhide the gap", loc="left", fontsize=7.5)
    axs[1].bar([0, 1], [cv["RC"], cv["SC"]], color=[ORANGE, BLUE], width=0.6); axs[1].axhline(0.9, color=INK, ls="--", lw=0.7)
    axs[1].set_xticks([0, 1], ["row-\ncalibrated", "study-\ncalibrated"]); axs[1].set_ylim(0, 1); axs[1].set_ylabel("Coverage of 90% interval")
    axs[1].set_title("2  Honest intervals\nfor a new study", loc="left", fontsize=7.5)
    for m, (c, mk, lab) in STY.items():
        q = s[s.strategy == m].sort_values("k")
        if m != "A":
            q = q[q.k > 0]
        axs[2].plot(q.k, q.median_rmse, "-" + mk, color=c, ms=4, lw=1.4, label=lab)
    axs[2].set_xticks([0, 1, 2, 3, 5]); axs[2].set_xlabel("local runs measured (screening design)"); axs[2].set_ylabel("Median per-study RMSE (wt%)")
    axs[2].set_title("3  A few local runs: anchor,\nbut compare with local-only", loc="left", fontsize=7.5); axs[2].legend(fontsize=6, frameon=False)
    fig.tight_layout(); save(fig, D, "graphical_abstract_v3")


def run(mode="full"):
    D = out_dirs(mode)
    for f in (fig_deployment, fig_case, fig_workflow, fig_pred_obs, graphical_abstract_v3):
        try:
            f(D)
        except Exception as e:
            print(f"{f.__name__} failed: {e}")


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "full")
