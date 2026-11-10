"""Create the LOCKED study-level test split (run once, before any modelling).

Unit of splitting = source publication (DOI).  20 % of studies are held out
as an untouched final test set.  The seed was fixed before any model was fit.
"""
import hashlib, json, os
import numpy as np, pandas as pd

LOCK_SEED = 20261110
TEST_FRACTION = 0.20
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
RAW = os.path.join(ROOT, "data", "raw", "htt_radar_v1", "master_dataset.csv")
OUT = os.path.join(ROOT, "config", "locked_test_studies.json")

def main():
    if os.path.exists(OUT):
        raise SystemExit(f"{OUT} exists; the locked split must never be regenerated.")
    raw = open(RAW, "rb").read()
    d = pd.read_csv(RAW, low_memory=False)
    dois = np.array(sorted(d["DOI"].astype(str).unique()))
    rng = np.random.default_rng(LOCK_SEED)
    n_test = int(round(TEST_FRACTION * len(dois)))
    test = sorted(rng.choice(dois, size=n_test, replace=False).tolist())
    rec = dict(seed=LOCK_SEED, test_fraction=TEST_FRACTION, n_studies=len(dois), n_test_studies=len(test),
               n_test_rows=int(d["DOI"].isin(test).sum()), n_rows=len(d),
               dataset_sha256=hashlib.sha256(raw).hexdigest(), test_studies=test)
    json.dump(rec, open(OUT, "w"), indent=1)
    print({k: v for k, v in rec.items() if k != "test_studies"})

if __name__ == "__main__":
    main()
