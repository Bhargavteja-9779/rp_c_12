"""Paths, configuration, device detection and logging helpers."""
from __future__ import annotations

import json, logging, os, platform, sys, time
import numpy as np
import yaml

CODE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPO = os.path.abspath(os.path.join(CODE, ".."))


def out_dirs(mode: str) -> dict:
    """Full mode writes to the repository-level results/figures/tables; quick mode to code/_quick/ (never mixed)."""
    base = REPO if mode == "full" else os.path.join(CODE, "_quick")
    d = {k: os.path.join(base, k) for k in ["results", "figures", "tables"]}
    d["logs"] = os.path.join(d["results"], "experiment_logs")
    d["pred"] = os.path.join(d["results"], "predictions")
    d["stats"] = os.path.join(d["results"], "statistics")
    for v in d.values():
        os.makedirs(v, exist_ok=True)
    return d


def load_config(mode: str) -> dict:
    return yaml.safe_load(open(os.path.join(CODE, "config", "default.yaml")))[mode]


def detect_device() -> str:
    """CPU / CUDA / Apple-Silicon MPS detection (only TabPFN can use an accelerator)."""
    try:
        import torch
        if torch.cuda.is_available():
            return "cuda"
        if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
            return "mps"
    except Exception:
        pass
    return "cpu"


def environment_info() -> dict:
    import sklearn, scipy, pandas
    info = dict(python=sys.version.split()[0], platform=platform.platform(), processor=platform.processor(),
                cpu_count=os.cpu_count(), device=detect_device(), numpy=np.__version__, pandas=pandas.__version__,
                sklearn=sklearn.__version__, scipy=scipy.__version__)
    for m in ["lightgbm", "xgboost", "catboost", "gpboost", "tabpfn", "torch"]:
        try:
            info[m] = __import__(m).__version__
        except Exception:
            info[m] = None
    return info


def get_logger(name: str, logdir: str) -> logging.Logger:
    lg = logging.getLogger(name); lg.setLevel(logging.INFO)
    if not lg.handlers:
        fmt = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
        for h in (logging.StreamHandler(sys.stdout), logging.FileHandler(os.path.join(logdir, f"{name}.log"))):
            h.setFormatter(fmt); lg.addHandler(h)
    return lg


def dump(obj, path):
    def conv(o):
        if isinstance(o, (np.integer,)): return int(o)
        if isinstance(o, (np.floating,)): return None if not np.isfinite(o) else float(o)
        if isinstance(o, np.ndarray): return o.tolist()
        return str(o)
    with open(path, "w") as f:
        json.dump(obj, f, indent=1, default=conv)


class Timer:
    def __enter__(self):
        self.t = time.perf_counter(); return self
    def __exit__(self, *a):
        self.s = time.perf_counter() - self.t
