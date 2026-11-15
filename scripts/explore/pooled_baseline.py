"""pooled_baseline.py (exploratory, plan amendment 12): a leave-one-fire-out pooled random forest on predictors
z-scored within each fire, as a location-free baseline, against the local models of G1/G2 on the focal label, on
later burning to 2023 (G1 label) and on 2024-2026 burning (11.4 label). Uses only the 31 primary sites.
Writes $THERMAL_TWIN_SCALEUP/analysis/explore/pooled_baseline.csv."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
from scipy.stats import rankdata

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "geonull"))
sys.path.insert(0, str(HERE.parent / "scaleup"))
import geonull as G  # noqa: E402
import analysis_official as A  # noqa: E402
import claim4_transfer as C4  # noqa: E402

OUT = A.OUT / "explore"


def main():
    OUT.mkdir(exist_ok=True)
    F = A.load_fires()
    ids = [i for i in F if i != "montiferru_2021"]
    Z = {i: C4.scale(F[i].df, "z") for i in ids}
    rows = []
    for t in ids:
        parts = [Z[s].sample(min(C4.POOL_CAP, len(Z[s])), random_state=A.SEED) for s in ids if s != t]
        tr = pd.concat(parts, ignore_index=True)
        pooled = A.build(A.THERMAL).fit(tr[A.THERMAL], tr.burned).predict_proba(Z[t][A.THERMAL])[:, 1]
        D = np.load(A.OUT / "claim16_scores" / f"{t}.npz")
        y = D["y"]
        sc = {"pooled": pooled, "thermal": D["thermal"], "coord_rf": D["coord_rf"], "thermal_coord": D["thermal_coord"],
              "blend": (rankdata(pooled) + rankdata(D["thermal"])) / 2}
        r = {"fire": t, **{f"focal_{k}": G.auc(y, v) for k, v in sc.items()}}
        for lab_name, path, bi, ui in (("g1", A.OUT / "future" / f"{t}.tif", 0, 2), ("late", A.OUT / "late" / f"{t}.tif", 0, 1)):
            with rasterio.open(path) as rr:
                a = rr.read()
            lab, unm = a[bi][D["row"], D["col"]], a[ui][D["row"], D["col"]]
            pop = (unm <= 0.10) & (y == 0)
            yl = (lab >= 0.5).astype(int)
            ok = yl[pop].sum() >= 30 and (1 - yl[pop]).sum() >= 30
            for k, v in sc.items():
                r[f"{lab_name}_{k}"] = G.auc(yl[pop], v[pop]) if ok else np.nan
        rows.append(r)
        print(t, {k: round(v, 3) for k, v in r.items() if isinstance(v, float) and np.isfinite(v)}, flush=True)
    R = pd.DataFrame(rows)
    R.to_csv(OUT / "pooled_baseline.csv", index=False)
    for lab in ("focal", "g1", "late"):
        cols = [c for c in R if c.startswith(lab + "_")]
        print(lab, R[cols].mean().round(3).to_dict(), "n", int(R[cols[0]].notna().sum()))


if __name__ == "__main__":
    main()
