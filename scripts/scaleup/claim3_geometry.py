"""claim3_geometry.py: second view of the Sentinel-2 check (plan amendment 4, post hoc, asked for by the review).

The main check (claim3_label_check.py) keeps the distance bands of the MCD64A1 label. Here, for the two
variants that change which cells are burned (a: the Sentinel-2 label; c: MCD64A1 with missed cells
relabelled burned), the bands are recomputed from the variant's own burned cells. Predictions stay fixed.
For every variant and threshold the nearest band, the farthest band beyond 0.5 km and their rise are given
for each fire, together with the paired difference from the MCD64A1 reference on the same fires and the
same valid cells.

Writes claim3_geometry_per_fire.csv and claim3_geometry_summary.json in $THERMAL_TWIN_SCALEUP/analysis.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
from scipy.spatial import cKDTree

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analysis_official as A  # noqa: E402
from claim3_label_check import VALID_MIN  # noqa: E402

S2 = A.OUT / "s2"


def near_far(y, s, dist):
    near_neg = (y == 0) & (dist < 0.5)
    near = A.auc(y[(y == 1) | near_neg], s[(y == 1) | near_neg]) if near_neg.sum() >= A.MIN_BAND_NEG else np.nan
    far = np.nan
    for lo, hi in reversed(A.BANDS[1:]):
        neg = (y == 0) & (dist >= lo) & (dist < hi)
        if neg.sum() >= A.MIN_BAND_NEG:
            far = A.auc(y[(y == 1) | neg], s[(y == 1) | neg])
            break
    return near, far


def main():
    F = A.load_fires()
    ids = [i for i in F if i != "montiferru_2021"]
    rows = []
    for fid in ids:
        f = F[fid]
        with rasterio.open(S2 / f"{fid}.tif") as r:
            a = r.read()
        rr, cc = f.df.row_500m.to_numpy(int), f.df.col_500m.to_numpy(int)
        valid = a[2][rr, cc]
        s = f.oof(A.THERMAL, "thermal", "rf", 10)
        for th, band in (("010", 0), ("027", 1)):
            x = a[band][rr, cc]
            ok = np.isfinite(x) & (valid >= VALID_MIN)
            y0 = f.y[ok]
            xy, sc = f.xy[ok], s[ok]
            d0 = f.dist[ok]
            ref_near, ref_far = near_far(y0, sc, d0)
            for vname, yv in (("a_s2_label", (x[ok] >= 0.5).astype(int)), ("c_relabel", np.where((y0 == 0) & (x[ok] >= 0.5), 1, y0))):
                if yv.sum() == 0:
                    continue
                dv = cKDTree(xy[yv == 1]).query(xy)[0]          # bands from the variant's own burned cells
                v_near_fixed, v_far_fixed = near_far(yv, sc, d0)
                v_near_new, v_far_new = near_far(yv, sc, dv)
                rows.append({"fire": fid, "threshold": th, "variant": vname, "ref_near": ref_near, "ref_far": ref_far,
                             "fixed_near": v_near_fixed, "fixed_far": v_far_fixed,
                             "recomputed_near": v_near_new, "recomputed_far": v_far_new})
        print(fid, "done", flush=True)
    R = pd.DataFrame(rows)
    for c in ("ref", "fixed", "recomputed"):
        R[f"{c}_rise"] = R[f"{c}_far"] - R[f"{c}_near"]
    R.to_csv(A.OUT / "claim3_geometry_per_fire.csv", index=False)
    S = {}
    for (th, vn), g in R.groupby(["threshold", "variant"]):
        both = g[["ref_near", "ref_far", "recomputed_near", "recomputed_far", "fixed_near", "fixed_far"]].notna().all(axis=1)
        h = g[both]
        S[f"{vn}_{th}"] = {
            "fires": int(both.sum()),
            **{f"{c}_{k}": A.boot_mean(h[f"{c}_{k}"]) for c in ("ref", "fixed", "recomputed") for k in ("near", "far", "rise")},
            "fixed_minus_ref_near": A.boot_mean(h.fixed_near - h.ref_near), "fixed_minus_ref_far": A.boot_mean(h.fixed_far - h.ref_far),
            "recomputed_minus_ref_rise": A.boot_mean(h.recomputed_rise - h.ref_rise),
            "recomputed_rise_positive": f"{int((h.recomputed_rise > 0).sum())} of {int(len(h))}",
        }
    (A.OUT / "claim3_geometry_summary.json").write_text(json.dumps(S, indent=1, default=float), encoding="utf-8")
    print(json.dumps(S, indent=1, default=float))


if __name__ == "__main__":
    main()
