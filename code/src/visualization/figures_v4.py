"""v4 figures (within-study meta-analysis, PROTOCOL Addendum E) and tables, from result files only."""
from __future__ import annotations

import json, os, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.utils import out_dirs
from src.visualization.figures import BLUE, ORANGE, AQUA, GREY, INK, MUTED, save

OUT_L = {"biooil": "Bio-oil yield (wt%)", "solid": "Solid yield (wt%)", "aqueous": "Aqueous-phase yield (wt%)", "gas": "Gas yield (wt%)",
         "hhv_biooil": "Bio-oil HHV (MJ/kg)", "energy_biooil": "Energy recovery to bio-oil (%)", "n_biooil": "Bio-oil N (wt%)"}
LEV_L = {"<250 °C": "T +10 °C (<250 °C)", "250–300 °C": "T +10 °C (250–300 °C)", "300–350 °C": "T +10 °C (300–350 °C)", "≥350 °C": "T +10 °C (≥350 °C)",
         "alkali_carbonate": "Alkali carbonate", "alkali_hydroxide": "Alkali hydroxide", "acid": "Acid", "metal_supported": "Metal / supported metal",
         "other": "Other catalyst", "water_alcohol": "Water–alcohol (vs water)", "alcohol": "Alcohol (vs water)", "water_with_donor": "Water + H-donor (vs water)",
         "other_organic": "Other organic (vs water)"}
ORDER = ["T|<250 °C", "T|250–300 °C", "T|300–350 °C", "T|≥350 °C", "t|all", "load|all", "cat|alkali_carbonate", "cat|alkali_hydroxide", "cat|metal_supported",
         "cat|acid", "cat|other", "med|water_alcohol", "med|alcohol", "med|water_with_donor", "med|other_organic"]


def label(f, lv):
    if f == "t":
        return "Residence time ×2"
    if f == "load":
        return "Solid loading +10 pp"
    return LEV_L.get(lv, lv)


def meta(D):
    return pd.read_csv(os.path.join(D["results"], "e18_meta_dev.csv"))


def fig_evidence(D):
    M = meta(D); M["row"] = M.factor + "|" + M.level
    rows = [r for r in ORDER if r in set(M.row)]; cols = list(OUT_L)
    K = M.pivot_table(index="row", columns="outcome", values="k").reindex(index=rows, columns=cols)
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    im = ax.imshow(np.log1p(K.fillna(0).to_numpy()), cmap="Blues", aspect="auto", vmin=0, vmax=np.log1p(70))
    for i in range(K.shape[0]):
        for j in range(K.shape[1]):
            v = K.iat[i, j]
            ax.text(j, i, "" if np.isnan(v) else int(v), ha="center", va="center", fontsize=6.5, color="white" if (not np.isnan(v) and v > 25) else INK)
    ax.set_yticks(range(len(rows)), [label(*r.split("|")) for r in rows], fontsize=6.5)
    short = {"biooil": "Bio-oil\nyield", "solid": "Solid\nyield", "aqueous": "Aqueous\nyield", "gas": "Gas\nyield", "hhv_biooil": "Bio-oil\nHHV",
             "energy_biooil": "Energy\nrecovery", "n_biooil": "Bio-oil\nN"}
    ax.set_xticks(range(len(cols)), [short[c] for c in cols], fontsize=6.3, rotation=0)
    ax.set_title("Number of studies contributing within-study contrasts (development studies; blank: < 5)", loc="left", fontsize=7.5)
    ax.grid(False); fig.tight_layout(); save(fig, D, "fig18_evidence_map")


def forest(ax, q, title, xlabel="Effect (wt%): mean, 95% CI (blue), 95% prediction interval (grey)"):
    q = q.copy(); q["row"] = q.factor + "|" + q.level; q = q.set_index("row").reindex([r for r in ORDER if r in set(q.factor + "|" + q.level)])
    y = np.arange(len(q))[::-1]
    ax.axvline(0, color=MUTED, lw=0.6)
    ax.hlines(y, q.pi_lo, q.pi_hi, color=GREY, lw=0.8, alpha=0.6)
    ax.hlines(y, q.ci_lo, q.ci_hi, color=BLUE, lw=2.4)
    ax.plot(q.mu, y, "D", color=INK, ms=3)
    for yy, (_, r) in zip(y, q.iterrows()):
        ax.text(1.01, yy, f"k={int(r.k)}  I²={r.I2:.0%}  P(>0)={r.p_benefit:.2f}", transform=ax.get_yaxis_transform(), fontsize=5.3, va="center", color=MUTED)
    ax.set_yticks(y, [label(f, lv) for f, lv in (r.split("|") for r in q.index)], fontsize=6.5)
    ax.set_title(title, loc="left", fontsize=7.5); ax.set_xlabel(xlabel, fontsize=6.3)


def fig_atlas(D):
    M = meta(D)
    fig, axs = plt.subplots(2, 2, figsize=(7.2, 5.6), gridspec_kw={"height_ratios": [5, 9]})
    for j, o in enumerate(["biooil", "solid"]):
        q = M[M.outcome == o]
        c = q[q.factor.isin(["T", "t"])]; a = q[q.factor.isin(["load", "cat", "med"])]
        forest(axs[0, j], c, f"{OUT_L[o]} — conditions", "wt% per +10 °C or per doubling of time")
        forest(axs[1, j], a, f"{OUT_L[o]} — loading, catalysts, media", "wt% (vs uncatalysed or water; per +10 pp loading)")
        axs[0, j].set_xlim(-8, 8)
        lim = min(np.nanmax(np.abs(a[["pi_lo", "pi_hi"]].to_numpy())), 45); axs[1, j].set_xlim(-lim, lim)
    fig.tight_layout(w_pad=7, h_pad=1.2); save(fig, D, "fig19_effect_atlas")


def fig_phases(D):
    M = meta(D)
    items = [("T", "250–300 °C", "+10 °C at 250–300 °C"), ("T", "300–350 °C", "+10 °C at 300–350 °C"), ("cat", "alkali_carbonate", "Alkali carbonate"),
             ("cat", "alkali_hydroxide", "Alkali hydroxide"), ("cat", "metal_supported", "Metal / supported")]
    outs = [("biooil", BLUE), ("solid", ORANGE), ("aqueous", AQUA), ("gas", GREY)]
    fig, ax = plt.subplots(figsize=(7.0, 3.0)); w = 0.2
    for j, (o, c) in enumerate(outs):
        for i, (f, lv, _) in enumerate(items):
            r = M[(M.outcome == o) & (M.factor == f) & (M.level == lv)]
            if r.empty:
                continue
            r = r.iloc[0]; x = i + (j - 1.5) * w
            ax.bar(x, r.mu, w, color=c, label=OUT_L[o].split(" (")[0] if i == 0 else None)
            ax.errorbar(x, r.mu, yerr=[[r.mu - r.ci_lo], [r.ci_hi - r.mu]], color=INK, lw=0.7, capsize=1.5)
    ax.axhline(0, color=MUTED, lw=0.6); ax.set_xticks(range(len(items)), [t for *_, t in items], fontsize=7)
    ax.set_ylabel("Within-study effect (wt%)"); ax.legend(fontsize=6.5, ncol=4, loc="lower left", frameon=False)
    ax.set_title("Redistribution of products (mean effect with 95% CI; each phase estimated from the studies that report it)", loc="left", fontsize=7.5)
    fig.tight_layout(); save(fig, D, "fig20_phase_redistribution")


def fig_lab_vs_process(D, tau_ml):
    M = meta(D); L = json.load(open(os.path.join(D["stats"], "e18_lab_effect_mixedlm.json")))
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.9), sharex=True)
    for ax, o in zip(axs, ["biooil", "solid"]):
        g = lambda f, lv: M[(M.outcome == o) & (M.factor == f) & (M.level == lv)]
        rows = []
        r = g("T", "250–300 °C").iloc[0]; rows.append(("+50 °C within 250–300 °C", abs(5 * r.mu), 5 * r.ci_lo, 5 * r.ci_hi))
        for lv, nm in [("alkali_carbonate", "Alkali carbonate"), ("metal_supported", "Metal / supported catalyst"), ("alkali_hydroxide", "Alkali hydroxide")]:
            r = g("cat", lv).iloc[0]; rows.append((nm, abs(r.mu), r.ci_lo, r.ci_hi))
        r = g("t", "all").iloc[0]; rows.append(("Residence time ×2", abs(r.mu), r.ci_lo, r.ci_hi))
        labs = [("Laboratory offset SD (ML out-of-study)", tau_ml[o]), ("Laboratory offset SD (mixed model)", L[o]["tau"])]
        names = [n for n, *_ in rows] + [n for n, _ in labs]; vals = [v for _, v, *_ in rows] + [v for _, v in labs]
        cols = [BLUE] * len(rows) + [ORANGE] * len(labs)
        y = np.arange(len(names))[::-1]
        ax.barh(y, vals, color=cols, height=0.6)
        ax.set_yticks(y, names, fontsize=6.3); ax.set_title(OUT_L[o], loc="left", fontsize=7.5)
        ax.set_xlabel("|Effect| or SD (wt%)", fontsize=7)
    fig.tight_layout(); save(fig, D, "fig21_lab_vs_process")


def fig_pooled(D):
    P = pd.read_csv(os.path.join(D["results"], "e18_pooled_vs_meta_dev.csv"))
    models = ["pooled linear", "pooled XGBoost", "study fixed-effects linear"]
    fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.7), sharex=True, sharey=True)
    for ax, m in zip(axs, models):
        q = P[P.model == m]
        for o, c in [("biooil", BLUE), ("solid", ORANGE)]:
            z = q[q.outcome == o]
            ax.errorbar(z.mu, z.effect, xerr=[z.mu - z.ci_lo, z.ci_hi - z.mu], fmt="o", color=c, ms=3, lw=0.6, label="bio-oil" if o == "biooil" else "solid")
        lim = 20; ax.plot([-lim, lim], [-lim, lim], color=MUTED, lw=0.6); ax.axhline(0, color=MUTED, lw=0.4); ax.axvline(0, color=MUTED, lw=0.4)
        ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_title(m, loc="left", fontsize=7.5)
        ax.set_xlabel("Within-study meta-analytic effect", fontsize=6.5)
    axs[0].set_ylabel("Effect implied by pooled model", fontsize=6.5); axs[0].legend(fontsize=6)
    fig.tight_layout(); save(fig, D, "fig22_pooled_vs_meta")


def fig_locked(D):
    M = meta(D); L = pd.read_csv(os.path.join(D["results"], "e18_locked_contrasts.csv"))
    S = L.groupby(["outcome", "factor", "level", "study"]).effect.mean().reset_index()
    items = [("biooil", "T", "250–300 °C"), ("biooil", "T", "300–350 °C"), ("biooil", "cat", "metal_supported"), ("biooil", "cat", "alkali_carbonate"),
             ("solid", "T", "<250 °C"), ("solid", "T", "250–300 °C"), ("solid", "T", "300–350 °C"), ("solid", "cat", "metal_supported"), ("biooil", "t", "all"), ("solid", "t", "all")]
    fig, ax = plt.subplots(figsize=(7.0, 3.6)); y0 = len(items)
    for i, (o, f, lv) in enumerate(items):
        y = y0 - i; r = M[(M.outcome == o) & (M.factor == f) & (M.level == lv)].iloc[0]
        ax.hlines(y, r.pi_lo, r.pi_hi, color=GREY, lw=0.8, alpha=0.6); ax.hlines(y, r.ci_lo, r.ci_hi, color=BLUE, lw=2.4); ax.plot(r.mu, y, "D", color=INK, ms=3)
        s = S[(S.outcome == o) & (S.factor == f) & (S.level == lv)].effect
        ax.plot(s, np.full(len(s), y - 0.28), "o", mfc="none", mec=ORANGE, ms=3.5, mew=0.8)
    ax.axvline(0, color=MUTED, lw=0.6)
    ax.set_yticks([y0 - i for i in range(len(items))], [f"{OUT_L[o].split(' (')[0]}: {label(f, lv)}" for o, f, lv in items], fontsize=6.3)
    ax.set_xlabel("Effect (wt% per step)", fontsize=7); ax.set_xlim(-30, 30)
    ax.set_title("Development meta-analysis (mean, 95% CI, 95% PI) vs effects in held-out locked studies (orange circles)", loc="left", fontsize=7.2)
    fig.tight_layout(); save(fig, D, "fig23_locked_replication")


def graphical_abstract_v4(D, tau_ml):
    M = meta(D)
    fig, axs = plt.subplots(1, 2, figsize=(6.64, 2.66), gridspec_kw={"width_ratios": [1.5, 1]})
    q = M[(M.outcome == "biooil") & M.factor.isin(["T", "cat"]) & ~M.level.isin(["other", "acid"])]
    forest(axs[0], q, "Within-study effects on bio-oil yield (150 studies)")
    for t in axs[0].texts:
        t.set_fontsize(4.8)
    axs[0].set_xlim(-25, 35); axs[0].set_xlabel("wt%", fontsize=6.5)
    r = M[(M.outcome == "biooil") & (M.factor == "cat") & (M.level == "alkali_carbonate")].iloc[0]
    rt = M[(M.outcome == "biooil") & (M.factor == "T") & (M.level == "250–300 °C")].iloc[0]
    axs[1].bar([0, 1, 2], [5 * rt.mu, r.mu, tau_ml["biooil"]], color=[BLUE, BLUE, ORANGE], width=0.6)
    axs[1].set_xticks([0, 1, 2], ["+50 °C\n(250–300)", "alkali\ncarbonate", "laboratory\neffect (SD)"], fontsize=6.5)
    axs[1].set_ylabel("Bio-oil yield (wt%)", fontsize=7); axs[1].set_title("Laboratory effects rival\nprocess effects", loc="left", fontsize=7.5)
    fig.tight_layout(); save(fig, D, "graphical_abstract_v4")


def fig_design(D):
    """Real-data illustration: bio-oil yield vs temperature in the development studies with the longest single-factor temperature series."""
    from src.meta.within_study import frame, cell_keys
    F = frame("dev"); q = F[F.biooil.notna() & F["T"].notna()].copy(); q["cell"] = cell_keys(q, "T").values
    nT = q.groupby("cell")["T"].nunique(); cells = nT[nT >= 4].index
    best = q[q.cell.isin(cells)].groupby("cell").agg(study=("study", "first"), n=("T", "nunique")).sort_values("n", ascending=False).drop_duplicates("study").head(10)
    fig, ax = plt.subplots(figsize=(5.0, 3.2)); cmap = plt.get_cmap("tab10"); at300 = []
    for i, c in enumerate(best.index):
        z = q[q.cell == c].groupby("T").biooil.mean()
        ax.plot(z.index, z.values, "-o", color=cmap(i % 10), ms=2.5, lw=1)
        if 300 in z.index:
            at300.append(z.loc[300])
    ax.set_xlabel("Temperature (°C)"); ax.set_ylabel("Bio-oil yield (wt%)")
    ax.set_title(f"Single-factor temperature series of {len(best)} studies (one line each;\nall other conditions constant within a line)", loc="left", fontsize=7.5)
    fig.tight_layout(); save(fig, D, "fig24_within_study_design")
    return dict(n=len(best), lo300=float(min(at300)), hi300=float(max(at300)), n300=len(at300))


# ------------------------------------------------------------------ tables
def tables(D, tau_ml):
    T = D["tables"]; M = meta(D)
    def fmt(r, digits=1):
        f = f"{{:.{digits}f}}"
        return dict(Effect=f.format(r.mu), **{"95% CI": f"{f.format(r.ci_lo)} to {f.format(r.ci_hi)}", "95% PI": f"{f.format(r.pi_lo)} to {f.format(r.pi_hi)}"},
                    k=int(r.k), Contrasts=int(r.n_contrasts), **{"I²": f"{r.I2:.0%}", "P(increase)": f"{r.p_benefit:.2f}"})
    def build(outs, digits):
        rows = []
        for o in outs:
            q = M[M.outcome == o].copy(); q["row"] = q.factor + "|" + q.level
            q = q.set_index("row").reindex([r for r in ORDER if r in set(q.factor + "|" + q.level)])
            for _, r in q.iterrows():
                rows.append(dict(Outcome=OUT_L[o], Change=label(r.factor, r.level), **fmt(r, digits)))
        return pd.DataFrame(rows)
    build(["biooil", "solid"], 1).to_csv(os.path.join(T, "table_v4_meta_primary.csv"), index=False)
    build(["aqueous", "gas", "hhv_biooil", "energy_biooil"], 1).to_csv(os.path.join(T, "table_v4_meta_secondary.csv"), index=False)
    build(["n_biooil"], 2).to_csv(os.path.join(T, "table_v4_meta_nitrogen.csv"), index=False)
    FR = pd.read_csv(os.path.join(D["results"], "e18_feedstock_dev.csv"))
    FR = FR.assign(Outcome=FR.outcome.map(OUT_L), Component=FR.term.str.replace("feed_", "").str.replace("N", "nitrogen").str.capitalize(),
                   **{"Effect per +10 wt%": FR.coef_per_10wt.round(2), "95% CI": FR.ci_lo.round(2).astype(str) + " to " + FR.ci_hi.round(2).astype(str),
                      "p": FR.p.map(lambda p: "<0.001" if p < 0.001 else f"{p:.3f}"), "Studies": FR.n_studies, "Cells": FR.n_cells})
    FR[["Outcome", "Component", "Effect per +10 wt%", "95% CI", "p", "Studies", "Cells"]].to_csv(os.path.join(T, "table_v4_feedstock.csv"), index=False)
    E = json.load(open(os.path.join(D["stats"], "e18_dev.json")))
    pd.DataFrame([dict(Model=r["model"], **{"Items compared": r["n_items"], "Meta effects with CI excluding 0": r["n_sig_meta"],
                                             "Sign reversals (of those)": r["n_sign_reversal_sig"], "Spearman ρ": round(r["spearman"], 2),
                                             "Outside meta-analytic 95% CI": f"{r['share_outside_ci']:.0%}", "Median |difference| (wt%)": round(r["median_abs_diff"], 2)})
                  for r in E["pooled_summary"]]).to_csv(os.path.join(T, "table_v4_pooled.csv"), index=False)
    Lk = json.load(open(os.path.join(D["stats"], "e18_locked.json")))
    mr = Lk["median_rmse"]
    pd.DataFrame([{"Predictor of locked within-study changes": n, "Median per-study RMSE (wt%)": round(mr[k], 2),
                   "Sign agreement": (f"{Lk['sign_agreement_meta']:.2f}" if k == "pred_meta" else (f"{Lk['sign_agreement_xgb']:.2f}" if k == "pred_xgb" else "—")),
                   "One-sided Wilcoxon vs meta (Holm p)": ("—" if k == "pred_meta" else f"{Lk['meta_vs_xgb']['p_holm'] if k == 'pred_xgb' else Lk['meta_vs_zero']['p_holm']:.2f}")}
                  for n, k in [("Meta-analytic mean effect", "pred_meta"), ("Pooled XGBoost (counterfactual difference)", "pred_xgb"), ("No change (zero)", "pred_zero")]]
                 ).to_csv(os.path.join(T, "table_v4_locked.csv"), index=False)
    Mo = pd.read_csv(os.path.join(D["results"], "e18_moderators_dev.csv"))
    Mo = Mo.assign(Outcome=Mo.outcome.map(OUT_L), Catalyst=Mo.level.map(LEV_L), Moderator=Mo.moderator,
                   **{"Group A (k)": Mo.group_a + " (" + Mo.k_a.astype(str) + ")", "Effect A": Mo.mu_a.round(2), "Group B (k)": Mo.group_b + " (" + Mo.k_b.astype(str) + ")",
                      "Effect B": Mo.mu_b.round(2), "p": Mo.p.round(3), "p (Holm)": Mo.p_holm.round(3)})
    Mo[["Outcome", "Catalyst", "Moderator", "Group A (k)", "Effect A", "Group B (k)", "Effect B", "p", "p (Holm)"]].to_csv(os.path.join(T, "table_v4_moderators.csv"), index=False)
    Bt = pd.read_csv(os.path.join(D["results"], "e18_bootstrap_dev.csv")); M = M.merge(Bt, on=["outcome", "factor", "level"], how="left")
    S = M.assign(Outcome=M.outcome.map(OUT_L), Change=[label(f, lv) for f, lv in zip(M.factor, M.level)],
                 **{"REML": M.mu.round(2), "Paule–Mandel": M.mu_pm.round(2), "One per study (median)": M.mu_median_estimator.round(2),
                    "Leave-one-study-out range": M.loo_min.round(2).astype(str) + " to " + M.loo_max.round(2).astype(str),
                    "Egger p": M.egger_p.map(lambda p: "—" if pd.isna(p) else f"{p:.2f}"),
                    "Study-bootstrap 95% CI": M.boot_lo.round(2).astype(str) + " to " + M.boot_hi.round(2).astype(str)})
    S[["Outcome", "Change", "REML", "Paule–Mandel", "One per study (median)", "Leave-one-study-out range", "Study-bootstrap 95% CI", "Egger p"]].to_csv(os.path.join(T, "table_v4_sensitivity.csv"), index=False)
    RR = pd.read_csv(os.path.join(D["results"], "e18_response_ratios_dev.csv"))
    RR.assign(Outcome=RR.outcome.map(OUT_L), Catalyst=RR.level.map(LEV_L), k=RR.k, **{"Relative change (%)": RR.rel_pct.round(1),
              "95% CI": RR.rel_lo.round(1).astype(str) + " to " + RR.rel_hi.round(1).astype(str), "95% PI": RR.pi_lo.round(0).astype(int).astype(str) + " to " + RR.pi_hi.round(0).astype(int).astype(str),
              "I²": (100 * RR.I2).round(0).astype(int).astype(str) + "%"})[["Outcome", "Catalyst", "k", "Relative change (%)", "95% CI", "95% PI", "I²"]].to_csv(os.path.join(T, "table_v4_relative.csv"), index=False)
    caps = {
        "table_v4_relative": "Table X. Catalyst effects on a relative scale (response ratio: ratio of the mean outcome with catalyst to that without, pooled on the log scale and back-transformed to a percentage change). Post-hoc analysis added during internal review.",
        "table_v4_meta_primary": "Table X. Within-study meta-analysis of process effects on bio-oil and solid yields (development studies). Effect: random-effects mean change (REML, Hartung–Knapp–Sidik–Jonkman CI); PI: 95% prediction interval for the effect in a new study; k: studies; I²: share of variance due to between-study heterogeneity; P(increase): probability that the change increases the outcome in a new study, from the predictive distribution. Temperature effects per +10 °C in the stated band; catalysts vs uncatalysed runs and media vs water at otherwise identical conditions.",
        "table_v4_meta_secondary": "Table X. Within-study meta-analysis for the aqueous and gas phases, bio-oil higher heating value (measured values only) and energy recovery to bio-oil (yield × bio-oil HHV / feed HHV). Definitions as in the primary table.",
        "table_v4_meta_nitrogen": "Table X. Within-study meta-analysis for the nitrogen content of bio-oil (wt%).",
        "table_v4_feedstock": "Table X. Feedstock composition effects estimated from runs of the same study at identical conditions that differ only in feedstock (within-cell regression with cell fixed effects; cluster-robust standard errors by study). Coefficients per +10 wt% of the component, adjusted for the other components.",
        "table_v4_pooled": "Table X. Agreement of effects implied by pooled models fitted to all development runs (partial dependence for XGBoost; coefficients for linear models) with the within-study meta-analytic effects (26 factor-level items for bio-oil and solid yields).",
        "table_v4_locked": "Table X. Pre-registered confirmatory test on the 38 locked studies: prediction of their within-study changes (all factors, bio-oil and solid yields) by the development meta-analytic mean effect, by a pooled XGBoost model and by 'no change'.",
        "table_v4_moderators": "Table X. Pre-specified moderator analyses of catalyst effects (temperature of the cell, process subtype, feedstock lignin content); differences between subgroup means with z-tests, Holm-corrected within outcome × factor.",
        "table_v4_sensitivity": "Table X. Sensitivity of the meta-analytic means to the τ² estimator, to using one contrast per study and to leaving out single studies; 95% CI from 2,000 bootstrap resamples of studies (post hoc); Egger-type test for small-study effects (≥ 10 studies).",
    }
    for k, v in caps.items():
        open(os.path.join(T, f"{k}.md"), "w").write(f"**{v}**\n")


def run(mode="full"):
    D = out_dirs(mode)
    S = json.load(open(os.path.join(D["results"], "statistics.json")))
    tau_ml = {t: float(S["e3"][t]["heterogeneity"]["base"]["tau2"]) ** 0.5 for t in ["biooil", "solid"]}
    for f in (fig_evidence, fig_atlas, fig_phases, fig_pooled, fig_locked):
        f(D)
    json.dump(fig_design(D), open(os.path.join(D['stats'], 'fig24_design.json'), 'w'))
    fig_lab_vs_process(D, tau_ml); graphical_abstract_v4(D, tau_ml); tables(D, tau_ml)


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "full")
