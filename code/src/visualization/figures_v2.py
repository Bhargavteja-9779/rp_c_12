"""v2 figures (trend atlas, levels vs contrasts, ranking regret, graphical abstract v2) — all from result files."""
from __future__ import annotations

import json, os, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.utils import out_dirs
from src.visualization.figures import BLUE, ORANGE, AQUA, GREY, INK, MUTED, save  # shared style (rcParams set on import)

TL = {"biooil": "Bio-oil yield", "solid": "Solid yield", "hhv_biooil": "Bio-oil HHV", "c_biooil": "Bio-oil carbon"}


def fig_trend_atlas(D):
    e = pd.read_csv(os.path.join(D["results"], "e13_empirical_trends.csv")); e = e[e.variable == "T_C"]
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.8), sharey=False)
    for ax, t in zip(axs, ["biooil", "solid"]):
        s = e[e.target == t].reset_index(drop=True)
        x = np.arange(len(s))
        ax.axhline(0, color=MUTED, lw=0.6)
        ax.errorbar(x, s.median_slope, yerr=[s.median_slope - s.slope_ci_low, s.slope_ci_high - s.median_slope], fmt="s", color=BLUE, ms=5, capsize=3, lw=1.2)
        for xi, r in s.iterrows():
            ax.annotate(f"{r.frac_studies_same_sign:.0%} same sign\n{int(r.n_studies)} studies", (xi, r.slope_ci_high), xytext=(0, 4),
                        textcoords="offset points", ha="center", fontsize=5.8, color=INK)
        ax.set_xticks(x, [f"{b} °C" for b in s.band], fontsize=6.5)
        ax.set_ylabel("Within-study yield change per +10 °C (wt%)"); ax.set_title(TL[t], loc="left")
        lo, hi = ax.get_ylim(); ax.set_ylim(lo, hi + 0.25 * (hi - lo))
    fig.tight_layout(); save(fig, D, "fig11_trend_atlas")


def fig_levels_vs_contrasts(D):
    S = json.load(open(os.path.join(D["results"], "statistics_v2.json")))
    rows = []
    for split, lab in [("dev", "dev"), ("locked", "locked"), ("dev_quality", "dev"), ("locked_quality", "locked")]:
        for r in S.get(f"e12_{split}", {}).get("T1_T4_T5_summary", []):
            if r["learner"] == "xgb":
                rows.append(dict(target=r["target"], setting=lab, model=r["model"], contrast=r["contrast_r2"], level=r.get("level_r2_same_studies")))
    df = pd.DataFrame(rows)
    targets = [t for t in ["biooil", "solid", "hhv_biooil", "c_biooil"] if t in set(df.target)]
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.8), sharey=True)
    for ax, st in zip(axs, ["dev", "locked"]):
        x = np.arange(len(targets))
        lv = [df[(df.target == t) & (df.setting == st) & (df.model == "A")].level.mean() for t in targets]
        ax.plot(x - 0.2, lv, "o", color=GREY, ms=6, label="Levels (A)")
        for off, m, col, mk in [(-0.05, "A", ORANGE, "s"), (0.1, "W", AQUA, "^"), (0.25, "PD", BLUE, "D")]:
            cv = [df[(df.target == t) & (df.setting == st) & (df.model == m)].contrast.mean() for t in targets]
            ax.plot(x + off, cv, mk, color=col, ms=5, label=f"Contrasts ({m})")
        ax.axhline(0, color=MUTED, lw=0.6)
        ax.set_xticks(x, [TL[t] for t in targets], fontsize=6.5, rotation=15)
        ax.set_title("Development (unseen studies)" if st == "dev" else "Locked test studies", loc="left")
    axs[0].set_ylabel("R² for unseen studies"); axs[0].legend(fontsize=6, loc="lower left")
    fig.tight_layout(); save(fig, D, "fig12_levels_vs_contrasts")


def fig_ranking(D):
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.8))
    for ax, sfx, title in [(axs[0], "", "Development (exploratory)"), (axs[1], "_locked", "Locked test (confirmatory)")]:
        f = os.path.join(D["results"], f"e14b_ranking_heuristics{sfx}.csv")
        if not os.path.exists(f):
            continue
        K = pd.read_csv(f)
        P = K.groupby(["target", "study", "method"]).regret.mean().unstack(); rnd = K.groupby(["target", "study"]).random.mean()
        labels, vals, cols = [], [], []
        for t in ["biooil", "solid"]:
            g = P.loc[t]
            rule = "rule_T325" if t == "biooil" else "rule_lowest_T"
            for name, v, c in [("PD", g["PD"], BLUE), ("W", g["W"], AQUA), ("A", g["A"], ORANGE),
                               ("rule: T≈325 °C" if t == "biooil" else "rule: lowest T", g[rule], GREY), ("random", rnd.loc[t], "#cfcec9")]:
                labels.append(f"{'Bio-oil' if t == 'biooil' else 'Solid'} · {name}"); vals.append(v.dropna().values); cols.append(c)
        y = np.arange(len(labels))[::-1]
        for yi, v, c in zip(y, vals, cols):
            q1, med, q3 = np.percentile(v, [25, 50, 75])
            ax.hlines(yi, q1, q3, color=c, lw=3, alpha=0.6); ax.plot(med, yi, "o", color=c, ms=5)
        ax.set_yticks(y, labels, fontsize=6.3); ax.set_xlabel("Regret of the chosen run (wt%): median and IQR over studies")
        ax.set_title(title, loc="left")
    fig.tight_layout(); save(fig, D, "fig13_ranking_regret")


def graphical_abstract_v2(D):
    w = pd.read_csv(os.path.join(D["tables"], "table_e1_benchmark_wide.csv"))
    b = w[(w.target == "biooil") & (w.features == "base")].sort_values("rmse_grouped_study_cv").iloc[0]
    e = pd.read_csv(os.path.join(D["results"], "e13_empirical_trends.csv")); e = e[(e.variable == "T_C") & (e.target == "biooil")].reset_index(drop=True)
    K = pd.read_csv(os.path.join(D["results"], "e14b_ranking_heuristics_locked.csv")); K = K[K.target == "biooil"]
    P = K.groupby(["study", "method"]).regret.mean().unstack(); rnd = K.groupby("study").random.mean()
    fig, axs = plt.subplots(1, 3, figsize=(6.64, 2.66))
    axs[0].bar([0, 1], [b["r2_random_row_cv"], b["r2_grouped_study_cv"]], color=[ORANGE, BLUE], width=0.6)
    axs[0].set_xticks([0, 1], ["random\nsplit", "new\nstudy"]); axs[0].set_ylim(0, 1); axs[0].set_ylabel("R², bio-oil yield level")
    axs[0].set_title("Levels do not transfer", loc="left", fontsize=7.5)
    x = np.arange(len(e)); axs[1].axhline(0, color=MUTED, lw=0.6)
    axs[1].errorbar(x, e.median_slope, yerr=[e.median_slope - e.slope_ci_low, e.slope_ci_high - e.median_slope], fmt="s", color=BLUE, ms=4, capsize=2)
    axs[1].set_xticks(x, [s.replace("-", "–") for s in e.band], fontsize=6); axs[1].set_xlabel("°C"); axs[1].set_ylabel("Δ yield per +10 °C (wt%)")
    axs[1].set_title("Trend directions agree", loc="left", fontsize=7.5)
    meds = [P["PD"].median(), P["rule_T325"].median(), rnd.median()]
    axs[2].bar([0, 1, 2], meds, color=[BLUE, GREY, "#cfcec9"], width=0.6)
    axs[2].set_xticks([0, 1, 2], ["model", "rule of\nthumb", "random"]); axs[2].set_ylabel("Median regret (wt%)")
    axs[2].set_title("Choosing conditions\n(locked studies)", loc="left", fontsize=7.5)
    fig.tight_layout(); save(fig, D, "graphical_abstract_v2")


def run(mode="full"):
    D = out_dirs(mode)
    for f in (fig_trend_atlas, fig_levels_vs_contrasts, fig_ranking, graphical_abstract_v2):
        try:
            f(D)
        except Exception as ex:
            print(f"{f.__name__} failed: {ex}")


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "full")
