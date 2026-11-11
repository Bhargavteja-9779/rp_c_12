"""E11 (review round 6): measured STRATA overhead — wall-clock of the bare base learner vs the full STRATA
procedure (inner grouped + inner random 5-fold OOF, quantiles, variance components, k-shot quantiles for all k),
both on all development studies of each target, n_jobs = 1 and 4."""
import os, sys, time
import pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.data.load import load_target
from src.evaluation.core import restore
from src.models.registry import Learner
from src.models.strata import kshot_quantile
from src.utils import out_dirs, load_config
from experiments.common import choose_base_learner, load_cell, nested_fit

MODE = sys.argv[1] if len(sys.argv) > 1 else "full"
cfg, D = load_config(MODE), out_dirs(MODE); learner, _ = choose_base_learner(D); rows = []
for t in ["biooil", "solid"]:
    ds = load_target(t, "dev"); X = ds.X[ds.base_features + ds.protocol_features]; params = load_cell(D, t, "base+P", learner)["params"]
    for nj in [1, 4]:
        t0 = time.perf_counter(); Learner(learner, restore(params), n_jobs=nj).fit(X, ds.y, ds.groups); base = time.perf_counter() - t0
        t0 = time.perf_counter()
        nf = nested_fit(learner, params, X, ds.y, ds.groups, X.iloc[:5], inner_k=5, n_jobs=nj, alphas=[0.1])
        for k in cfg["k_values"]:
            kshot_quantile(nf["res_sc"], nf["g_cal"], k, nf["vc"]["lam"], "eb", 0.1, n_draws=cfg["kshot_draws"])
        rows.append(dict(target=t, learner=learner, n_jobs=nj, base_fit_s=base, strata_total_s=time.perf_counter() - t0))
        print(rows[-1])
pd.DataFrame(rows).to_csv(os.path.join(D["results"], "e11_overhead.csv"), index=False)
