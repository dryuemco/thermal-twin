"""R8n. Paired spatial-block bootstrap intervals for the within-region thermal gain with and without
terrain aspect in both feature sets (10-cell blocks for folds and bootstrap, 1000 replicates, seed 42).
Input: r8k_cells.csv.gz (northness, eastness) and the released modelling datasets.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "paper" / "code"))
import ems_inference_common as E  # noqa: E402

E.N_JOBS = 8
K = pd.read_csv(HERE / "r8k_cells.csv.gz")
ASP = ["northness", "eastness"]
out = {}
for reg in E.REGIONS:
    d = E.C.load(reg)
    d = d[(d.valid_for_modeling == True) & (d.burnable_tree_shrub_grass == True)]  # noqa: E712
    d = d.merge(K[K.region == reg], on=["row_500m", "col_500m"], how="left").reset_index(drop=True)
    y = d.burned.to_numpy()
    blk = ((d.row_500m // 10).astype(str) + "_" + (d.col_500m // 10).astype(str)).to_numpy()
    ub, inv = np.unique(blk, return_inverse=True)
    groups = [np.flatnonzero(inv == k) for k in range(len(ub))]
    res = {}
    for tag, extra in (("without_aspect", []), ("with_aspect", ASP)):
        th = E.blocked_oof(d, E.THERMAL + extra, 10)
        ba = E.blocked_oof(d, E.BASELINE + extra, 10)
        rng = np.random.default_rng(42)
        reps = []
        for _ in range(1000):
            idx = np.concatenate([groups[i] for i in rng.integers(0, len(groups), len(groups))])
            if y[idx].min() == y[idx].max():
                continue
            reps.append(roc_auc_score(y[idx], th[idx]) - roc_auc_score(y[idx], ba[idx]))
        g = roc_auc_score(y, th) - roc_auc_score(y, ba)
        lo, hi = np.percentile(reps, [2.5, 97.5])
        res[tag] = {"thermal": float(roc_auc_score(y, th)), "baseline": float(roc_auc_score(y, ba)),
                    "gain": float(g), "ci95": [float(lo), float(hi)]}
    out[reg] = res
    print(reg, json.dumps(res), flush=True)
json.dump(out, open(HERE / "r8n_summary.json", "w"), indent=1)
