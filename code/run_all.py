#!/usr/bin/env python
"""Reproduce the whole study.

    python run_all.py --mode quick   # ~10-15 min on 4 CPU cores: pipeline verification, writes code/_quick/
    python run_all.py --mode full    # complete study (several hours on 4 CPU cores), writes ../results ../figures ../tables

Stages are resumable: E1 caches each learner cell; E3 caches each target × feature set.
The locked test studies are touched only in --mode full (stage 'e5', part 'locked').
"""
import argparse, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

STAGES = [
    ("tests", [sys.executable, "-m", "pytest", "-q", "tests"]),
    ("e1", [sys.executable, "experiments/e1_benchmark.py", "{mode}"]),
    ("e3", [sys.executable, "experiments/e3_strata.py", "{mode}"]),
    ("e5", [sys.executable, "experiments/e5_generalization.py", "{mode}"]),
    ("e678", [sys.executable, "experiments/e6_e7_e8.py", "{mode}"]),
    ("e3b", [sys.executable, "experiments/e3b_adaptive.py", "{mode}"]),
    ("e9", [sys.executable, "experiments/e9_base_learners.py", "{mode}"]),
    ("e10", [sys.executable, "experiments/e10_duplicate_audit.py", "{mode}"]),
    ("e11", [sys.executable, "experiments/e11_overhead.py"]),
    ("analyze", [sys.executable, "-m", "src.statistics.analyze", "{mode}"]),
    ("tables", [sys.executable, "-m", "src.visualization.tables", "{mode}"]),
    ("figures", [sys.executable, "-m", "src.visualization.figures", "{mode}"]),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mode", choices=["quick", "full"], default="quick")
    ap.add_argument("--only", nargs="*", help="run only these stages", default=None)
    a = ap.parse_args()
    from src.utils import environment_info, out_dirs, dump
    D = out_dirs(a.mode)
    dump(environment_info(), os.path.join(D["logs"], "environment.json"))
    print("device:", environment_info()["device"])
    for name, cmd in STAGES:
        if a.only and name not in a.only:
            continue
        t = time.time()
        print(f"=== stage {name} ===", flush=True)
        r = subprocess.run([c.format(mode=a.mode) for c in cmd], cwd=HERE)
        print(f"=== stage {name} finished in {time.time() - t:.0f}s (exit {r.returncode}) ===", flush=True)
        if r.returncode != 0:
            sys.exit(r.returncode)


if __name__ == "__main__":
    main()
