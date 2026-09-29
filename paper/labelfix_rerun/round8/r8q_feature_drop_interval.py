"""R8q. Pair-cluster bootstrap interval for the transfer effect of removing both reversing features
(Section S1.14, Fig. 7), with the primary resampling unit of Section 3.7 (ten unordered region pairs,
1000 replicates, seed 42 as in paper/code/ems_inference_units.py). Input:
paper/labelfix_rerun/round3/feature_drop_transfer.json (delta of drop_both against the full set).
"""
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "paper" / "code"))
import ems_inference_units as U  # noqa: E402

T = json.load(open(ROOT / "paper/labelfix_rerun/round3/feature_drop_transfer.json"))["transfers"]
y = np.array([r["delta_vs_full"]["drop_both"] for r in T])
src = np.array([r["source"] for r in T])
tgt = np.array([r["target"] for r in T])
iv = U.intervals(y, src, tgt, level=0.95, R=1000)
out = {"mean": float(y.mean()), "pair_cluster_ci95": [float(iv["pair_cluster_boot"][0]), float(iv["pair_cluster_boot"][1])],
       "replicates": 1000, "rng": "ems_inference_units.intervals, seed 42 + 1"}
json.dump(out, open(HERE / "r8q_summary.json", "w"), indent=1)
print(out)
