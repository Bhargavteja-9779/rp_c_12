"""v3 analyses (PROTOCOL Addendum D): E15 summaries and tests, E16/E17 tables. Writes results/statistics_v3.json and tables."""
from __future__ import annotations

import json, os, sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.statistics.stats import paired_comparison, holm
from src.utils import out_dirs, dump

TL = {"biooil": "Bio-oil yield", "solid": "Solid yield"}
SL = {"dev": "Development (unseen studies)", "locked": "Locked studies", "external": "External 4TU (independent)"}
ORD = {"design": "screening design", "reported": "reported order", "random": "random"}


def summarise(d):
    g = d.groupby(["target", "order", "k", "strategy", "study"])[["rmse", "mae", "coverage", "width", "n_query"]].mean().reset_index()
    rows = []
    for key, q in g.groupby(["target", "order", "k", "strategy"]):
        w = 1 / q.n_query
        rows.append(dict(zip(["target", "order", "k", "strategy"], key), median_rmse=float(q.rmse.median()), median_mae=float(q.mae.median()),
                         coverage=float((q.coverage * q.n_query * w).sum() / (q.n_query * w).sum()), width=float(q.width.mean()), n_studies=int(len(q))))
    return pd.DataFrame(rows), g


def tests(g):
    out = []
    for (t, o), q in g.groupby(["target", "order"]):
        fam = []
        for k in sorted(q.k.unique()):
            if k == 0:
                continue
            p = q[q.k == k].pivot_table(index="study", columns="strategy", values="rmse")
            for ref in ["A", "C"]:
                x = p[["B", ref]].dropna()
                fam.append(dict(target=t, order=o, k=int(k), comparison=f"B_vs_{ref}", **{kk: v for kk, v in paired_comparison(x["B"].values, x[ref].values).items()
                                                                                          if kk in ("n", "p", "median_diff", "ci_low", "ci_high", "rank_biserial")}))
        for r, pa in zip(fam, holm([r["p"] for r in fam])):
            r["p_holm"] = float(pa)
        out.extend(fam)
    return out


def case_table(D):
    c = pd.read_csv(os.path.join(D["results"], "e17_case_study.csv")); sel = json.load(open(os.path.join(D["stats"], "e17_selection.json")))
    rows = []
    for t in ["biooil", "solid"]:
        q = c[(c.target == t) & (c.k.isin([0, 1, 2, 3, 5, 10]))]
        for r in q.itertuples():
            rows.append({"Case (locked study)": f"{TL[t]}: {sel[t]['feedstock']}, {sel[t]['process']} ({sel[t]['n_runs']} runs)", "Runs measured k": int(r.k),
                         "Runs predicted": int(r.n_remaining), "RMSE A (wt%)": r.rmse_A, "RMSE B (wt%)": r.rmse_B,
                         "RMSE C (wt%)": (r.rmse_C if r.k > 0 else np.nan), "Coverage B": r.cov_B, "Half-width B (wt%)": r.halfwidth_B,
                         "Regret A/B (wt%)": r.regret_A, "Regret random (wt%)": r.regret_random})
    pd.DataFrame(rows).round(2).to_csv(os.path.join(D["tables"], "table_v3_case_study.csv"), index=False)


def capability_v3(D, S):
    f = os.path.join(D["tables"], "table_v2_capability_matrix.csv")
    if not os.path.exists(f) or "e15_locked_summary" not in S:
        return
    cm = pd.read_csv(f)
    def med(st, t, k, m):
        s = pd.DataFrame(S[f"e15_{st}_summary"]); s = s[(s.target == t) & (s.order == "design") & (s.k == k) & (s.strategy == m)]
        return float(s.median_rmse.iloc[0])
    def sig(st, t, k, comp, sign):
        T = [x for x in S[f"e15_{st}_tests"] if x["target"] == t and x["order"] == "design" and x["k"] == k and x["comparison"] == comp]
        return bool(T and T[0]["p_holm"] < 0.05 and np.sign(T[0]["median_diff"]) == sign)
    lb_better_C = sig("locked", "biooil", 3, "B_vs_C", 1)
    new = [dict(Capability="Combine 1–3 screening-design runs with the literature model (STRATA, B) instead of using them alone (C)",
                **{"Development studies (unseen)": f"k = 3: B {med('dev','biooil',3,'B'):.1f} vs C {med('dev','biooil',3,'C'):.1f} (bio-oil), {med('dev','solid',3,'B'):.1f} vs C {med('dev','solid',3,'C'):.1f} wt% (solid); B better at every k",
                   "38 locked studies": f"k = 3: B {med('locked','biooil',3,'B'):.1f} vs C {med('locked','biooil',3,'C'):.1f} (bio-oil{', C better' if lb_better_C else ''}), B {med('locked','solid',3,'B'):.1f} vs C {med('locked','solid',3,'C'):.1f} wt% (solid, n.s.)",
                   "Verdict": "Usually yes; not for locked bio-oil studies, where local runs alone were better"}),
           dict(Capability="Flag in advance a study for which the literature model will mislead (applicability-domain score)",
                **{"Development studies (unseen)": f"Spearman ρ with error {S['e16']['biooil']['dev_spearman_ad_vs_rmse']:.2f} (bio-oil), {S['e16']['solid']['dev_spearman_ad_vs_rmse']:.2f} (solid)",
                   "38 locked studies": f"pre-registered threshold flagged {S['e16']['biooil']['locked_flagged']} and {S['e16']['solid']['locked_flagged']} studies",
                   "Verdict": "Ranks risk, but the pre-registered threshold detected no failing study"})]
    cm = pd.concat([cm, pd.DataFrame(new)], ignore_index=True)
    cm.loc[cm.Capability.str.startswith("Use 1–3 measured runs"), "Verdict"] = "Yes — error and interval width fall with each run"
    cm.to_csv(os.path.join(D["tables"], "table_v3_capability_matrix.csv"), index=False)


def prisma_table(D):
    L = os.path.join(os.path.dirname(D["tables"].rstrip("/")), "supplementary", "literature")
    f = os.path.join(L, "prisma_counts.json")
    if not os.path.exists(f):
        return
    p = json.load(open(f)); raw = json.load(open(os.path.join(L, "search_records_raw.json")))
    rows = [("Run date", p["run_date"]), ("PubMed query (title/abstract, publication date 2015-01-01 to run date)", raw["pubmed_query"]),
            ("OpenAlex query (title_and_abstract.search)", raw["openalex_query"] + " — not retrievable on the run date (anonymous API requests refused, HTTP 429); 0 records"),
            ("Crossref queries (query.bibliographic, journal articles, 200 records each)", "; ".join(raw["crossref_queries"])),
            ("Records identified", f"PubMed {p['identified']['PubMed']}; OpenAlex {p['identified']['OpenAlex']}; Crossref {p['identified']['Crossref']} (total {p['identified_total']})"),
            ("After de-duplication (DOI, else normalised title)", p["after_deduplication"]),
            ("Excluded: no machine-learning or no hydrothermal term in title/abstract (E1)", p["excluded_no_ml_or_no_hydrothermal_term"]),
            ("Excluded: review or non-primary (E2)", p["excluded_review_or_non_primary"]), ("Excluded: no predicted yield or property (E3)", p["excluded_no_prediction_target"]),
            ("Excluded: outside 2015–run date (E4)", p["excluded_outside_window"]),
            ("Included primary studies", f"{p['included']} ({p['included_with_abstract']} with an abstract; {p['included_in_bioresource_technology']} in Bioresource Technology)"),
            ("Included abstracts mentioning grouped / external validation", p["included_mentioning_grouped_or_external"]),
            ("Included abstracts mentioning uncertainty quantification", p["included_mentioning_uncertainty"])]
    pd.DataFrame(rows, columns=["Step", "Value"]).to_csv(os.path.join(D["tables"], "tableS_v3_prisma.csv"), index=False)


def run(mode="full"):
    D = out_dirs(mode); R = D["results"]; S = {}
    allsum = []
    for st in ["dev", "locked", "external"]:
        f = os.path.join(R, f"e15_deploy_{st}.csv")
        if not os.path.exists(f):
            continue
        s, g = summarise(pd.read_csv(f)); s["setting"] = st; allsum.append(s)
        S[f"e15_{st}_summary"] = s.to_dict("records"); S[f"e15_{st}_tests"] = tests(g)
    A = pd.concat(allsum)
    # main table: design order, k in {0,1,3,5}
    m = A[(A.order == "design") & (A.k.isin([0, 1, 3, 5]))].copy()
    m = m[~((m.k == 0) & (m.strategy != "A"))]
    m["Setting"] = m.setting.map(SL); m["Target"] = m.target.map(TL)
    m["Strategy"] = m.strategy.map({"A": "A · literature only", "B": "B · STRATA (literature + local runs)", "C": "C · local runs only"})
    t = m[["Setting", "Target", "k", "Strategy", "n_studies", "median_rmse", "median_mae", "coverage", "width"]].rename(
        columns={"k": "Local runs k", "n_studies": "Studies", "median_rmse": "Median RMSE (wt%)", "median_mae": "Median MAE (wt%)",
                 "coverage": "Coverage of 90% PI", "width": "PI width (wt%)"}).round(2)
    order_s = {SL["dev"]: 0, SL["locked"]: 1, SL["external"]: 2}
    t = t.sort_values(["Setting", "Target", "Local runs k", "Strategy"], key=lambda c: c.map(order_s) if c.name == "Setting" else c)
    t.to_csv(os.path.join(D["tables"], "table_v3_deployment.csv"), index=False)
    s2 = A[A.order != "design"].copy(); s2["setting"] = s2.setting.map(SL); s2["target"] = s2.target.map(TL); s2["order"] = s2.order.map(ORD)
    s2.round(2).to_csv(os.path.join(D["tables"], "table_v3_deployment_other_orders.csv"), index=False)
    T = pd.DataFrame([dict(setting=SL[k.split("_")[1]], **r) for k in S if k.endswith("_tests") for r in S[k]])
    T["target"] = T.target.map(TL); T["order"] = T.order.map(ORD)
    T.round(4).to_csv(os.path.join(D["tables"], "table_v3_deployment_tests.csv"), index=False)
    # decision support table
    dec = json.load(open(os.path.join(D["stats"], "e16_decision.json")))
    rows = []
    for tg in ["biooil", "solid"]:
        d = dec[tg]
        rows.append({"Target": TL[tg], "Item": "Applicability-domain score vs out-of-study error (development; Spearman ρ)",
                     "Result": f"ρ = {d['dev_spearman_ad_vs_rmse']:.2f} (p = {d['dev_spearman_p']:.1e}; {d['dev_n']} studies)"})
        rows.append({"Target": TL[tg], "Item": "Pre-registered threshold (95th percentile of development scores) on locked studies",
                     "Result": f"{d['locked_flagged']} of {d['locked_n_studies']} locked studies flagged (max score {d['locked_max_score']:.2f} vs threshold {d['ad_threshold']:.2f}); test D1 not possible"})
        rows.append({"Target": TL[tg], "Item": "Exploratory: score vs error on locked studies (Spearman ρ)",
                     "Result": f"ρ = {d['locked_exploratory_spearman_ad_vs_rmse']:.2f} (p = {d['locked_exploratory_spearman_p']:.2f}; {d['locked_eval_studies']} studies)"})
        hw = d["dev_halfwidth_by_k"]
        rows.append({"Target": TL[tg], "Item": "STRATA 90% half-width after k local runs (development; k = 0, 1, 2, 3, 5)",
                     "Result": ", ".join(f"±{hw[str(k)]:.1f}" for k in [0, 1, 2, 3, 5]) + " wt%"})
        for r in d["runs_needed"]:
            res = (f"k = {r['k_needed']} (development median RMSE {r['dev_median_rmse']:.1f}; locked coverage {r['locked_coverage']:.2f}, median RMSE {r['locked_median_rmse']:.1f})"
                   if r["k_needed"] is not None else "not reached within 5 local runs")
            rows.append({"Target": TL[tg], "Item": f"Local runs needed for a 90% half-width ≤ ±{r['tolerance_halfwidth']} wt%", "Result": res})
    pd.DataFrame(rows).to_csv(os.path.join(D["tables"], "table_v3_decision.csv"), index=False)
    S["e16"] = dec
    S["e17_selection"] = json.load(open(os.path.join(D["stats"], "e17_selection.json")))
    case_table(D); capability_v3(D, S); prisma_table(D)
    dump(S, os.path.join(R, "statistics_v3.json"))
    print(t.to_string())


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "full")
