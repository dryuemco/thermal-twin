"""Check that geonull reproduces the study code (scripts/scaleup/analysis_official.py) on the 31 fires.

Needs the study data (THERMAL_TWIN_PAPER, THERMAL_TWIN_SCALEUP). For every fire, the null AUC, the cAUC of the
thermal random forest (5 km blocks) and its band AUCs are computed with geonull from the cached out-of-fold
predictions and compared with claims12_per_fire.csv and claims12_bands.csv. Prints the largest absolute difference.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "scripts" / "scaleup"))
import geonull as G  # noqa: E402
import analysis_official as A  # noqa: E402


def main():
    F = A.load_fires()
    P = pd.read_csv(A.OUT / "claims12_per_fire.csv").set_index("fire")
    B = pd.read_csv(A.OUT / "claims12_bands.csv")
    worst = {"auc_null": 0.0, "cauc": 0.0, "band": 0.0}
    for fid, f in F.items():
        folds = f.folds(10)
        s = f.oof(A.THERMAL, "thermal", "rf", 10)
        r = G.evaluate(f.xy, f.y, folds, s, bands=A.BANDS, tol=A.PWD_TOL, floor=A.PWD_FLOOR_KM, seed=A.SEED,
                       min_neg=A.MIN_BAND_NEG)
        worst["auc_null"] = max(worst["auc_null"], abs(r["auc_null"] - P.loc[fid, "auc_null_b10"]))
        worst["cauc"] = max(worst["cauc"], abs(r["cauc"] - P.loc[fid, "cauc_rf_thermal_b10"]))
        # bands: geonull measures distance to the nearest burned cell from cell centres; the study uses a
        # distance transform on the same grid, so both are exact cell-centre distances
        dist = f.dist
        for m in G.band_auc(f.y, s, dist, A.BANDS, A.MIN_BAND_NEG):
            ref = B[(B.fire == fid) & (B.band == m["band"])].auc_rf_thermal
            if len(ref) and np.isfinite(m["auc"]) and np.isfinite(ref.iloc[0]):
                worst["band"] = max(worst["band"], abs(m["auc"] - ref.iloc[0]))
    print({k: f"{v:.2e}" for k, v in worst.items()})


if __name__ == "__main__":
    main()
