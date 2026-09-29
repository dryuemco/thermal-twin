"""[post-hoc] Calibrations for reading the exclusion arms (SPEC.md Addendum B).
(1) fold-draw spread: reference TSG population, CV splitter seed 1..10, RF fixed at 42.
(2) random-removal null for request 1: 48 random unflagged Bejis TSG cells removed, 20 draws.
Point ΔAUC only (no bootstrap).
"""
import ems_labels_common as E
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score


def delta(df, B, seed=42):
    E.C.assert_no_leakage(E.C.THERMAL)
    blocks = E.add_spatial_block_id(df, B).to_numpy()
    o = E.within_cv.run_oof(df, blocks, seed=seed)
    return roc_auc_score(o["y"], o["oof_thermal"]) - roc_auc_score(o["y"], o["oof_baseline"])


res = {"fold_seed_spread": {}, "random_removal_bejis": {}}
for reg in E.REGIONS:
    d = E.tsg(reg)
    for B in ((2, 10) if reg in ("manavgat_2021", "bejis_2022") else (10,)):
        v = [delta(d, B, s) for s in range(1, 11)]
        res["fold_seed_spread"][f"{reg}_B{B}"] = {"deltas": v, "min": min(v), "max": max(v),
                                                  "sd": float(np.std(v, ddof=1))}
        E.log(reg, B, f"min {min(v):+.4f} max {max(v):+.4f} sd {np.std(v, ddof=1):.4f}")
        E.dump(res, "r6_calibration.json")

flag = pd.read_csv(E.OUT / "r1_prelabel_cells_bejis_2022.csv")
d = E.tsg("bejis_2022")
key = set(zip(flag.row_500m, flag.col_500m))
pool = np.array([i for i, (r, c) in enumerate(zip(d.row_500m, d.col_500m)) if (r, c) not in key])
rng = np.random.default_rng(42)
draws = [rng.choice(pool, 48, replace=False) for _ in range(20)]
for B in (2, 10):
    v = [delta(d.drop(index=idx).reset_index(drop=True), B) for idx in draws]
    res["random_removal_bejis"][f"B{B}"] = {"deltas": v, "min": min(v), "max": max(v),
                                           "sd": float(np.std(v, ddof=1))}
    E.log("random removal", B, f"min {min(v):+.4f} max {max(v):+.4f} sd {np.std(v, ddof=1):.4f}")
    E.dump(res, "r6_calibration.json")
E.log("done")
