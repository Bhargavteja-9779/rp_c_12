"""E10 (review round 5): cross-study duplicate audit of the primary database.

A run that appears in two source studies (e.g. the same experiment reported twice) would leak information
across study-grouped folds. Runs are keyed on feedstock C/H/O/N/ash, temperature, residence time, solid
loading and the target yield (rounded); keys shared by >1 DOI are reported, and the main bio-oil and solid
results are re-evaluated with all such runs removed.
"""
import os, sys, json
import numpy as np, pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data.load import load_target
from src.evaluation.core import grouped_folds, oof_predict, summary, restore
from src.models.strata import variance_components
from src.utils import out_dirs, load_config, dump
from experiments.common import choose_base_learner, load_cell


def keys(ds):
    X = ds.X
    k = pd.DataFrame({"C": X.feed_C.round(0), "H": X.feed_H.round(0), "O": X.feed_O.round(0), "N": X.feed_N.round(1), "A": X.feed_ash.round(0),
                      "T": X.T_C.round(-1), "t": X.log_t_min.round(1), "L": X.solid_loading_wt_pct.round(0), "y": np.round(ds.y, 0)})
    return k.fillna(-999).astype(float).round(1).astype(str).agg("|".join, axis=1)


def run(mode="full"):
    cfg, D = load_config(mode), out_dirs(mode)
    learner, _ = choose_base_learner(D)
    out = {}
    for t in ["biooil", "solid"]:
        ds = load_target(t, "dev")
        k = keys(ds)
        n_doi = pd.Series(ds.groups).groupby(k.values).nunique()
        dupkeys = set(n_doi[n_doi > 1].index)
        dup = k.isin(dupkeys).to_numpy()
        pairs = pd.DataFrame({"k": k[dup].values, "doi": ds.groups[dup]}).groupby("k")["doi"].apply(lambda s: sorted(set(s)))
        res = dict(n_rows=int(len(k)), n_cross_study_duplicate_rows=int(dup.sum()), n_keys=int(len(dupkeys)),
                   studies_involved=sorted(set(ds.groups[dup])), example_pairs=[list(x) for x in pairs.head(10)])
        if dup.any():
            d2 = ds.subset(~dup)
            X = d2.X[d2.base_features]; params = restore(load_cell(D, t, "base", learner)["params"])
            p, _, _ = oof_predict(learner, params, X, d2.y, d2.groups, grouped_folds(d2.groups, k=cfg["outer_folds"], seed=cfg["outer_seeds"][0]), n_jobs=cfg["n_jobs"])
            vc = variance_components(d2.y - p, d2.groups)
            res["without_duplicates"] = dict(**summary(d2.y, p, d2.groups), share_between=vc["share_between"])
        out[t] = res
        print(t, {kk: vv for kk, vv in res.items() if kk not in ("studies_involved", "example_pairs")})
    # locked-test rows that duplicate development rows (counted only; the locked results are not re-evaluated)
    out["locked_vs_dev"] = {}
    for t in ["biooil", "solid"]:
        dev, te = load_target(t, "dev"), load_target(t, "test")
        m = keys(te).isin(set(keys(dev))).to_numpy()
        out["locked_vs_dev"][t] = dict(locked_rows=int(len(m)), locked_rows_matching_dev=int(m.sum()), locked_studies_involved=sorted(set(te.groups[m])))
    # like-for-like reference: same learner/seed/folds WITH duplicates (from E1)
    e1 = pd.read_csv(os.path.join(D["results"], "e1_benchmark.csv"))
    r = e1[(e1.features == "base") & (e1.learner == learner) & (e1.scheme == "grouped_study_cv") & (e1.seed == cfg["outer_seeds"][0])]
    out["reference_with_duplicates_seed11"] = {row.target: dict(rmse=float(row.rmse), median_study_rmse=float(row.median_study_rmse)) for row in r.itertuples()}
    dump(out, os.path.join(D["results"], "e10_duplicate_audit.json"))


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "full")
