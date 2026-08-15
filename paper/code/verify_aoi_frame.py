"""
Independent check of Referee Q's central claim: that the elevation reversal and
much of the transfer matrix are artefacts of how each AOI rectangle was drawn.

Q's argument: the modelled populations contain large far fields (Manavgat 61 %
of cells more than 10 km from any burned cell, Montiferru 1.5 %), those far
fields sit at systematically different elevations, and a signed univariate AUC
computed over the whole rectangle therefore measures the rectangle rather than
the predictor-burning relationship. Restricting to a fixed collar around burned
area is claimed to make all five regions agree in sign.

Written from scratch, not adapted from the referee's script. Read-only with
respect to repo/.

Stage 1 here: geometry, far-field shares, and signed univariate AUC full frame
versus collar frame. The transfer matrix is stage 2 (verify_aoi_transfer.py).
"""
import sys

import numpy as np
import pandas as pd
from scipy import ndimage
from sklearn.metrics import roc_auc_score

REGIONS = ["manavgat_2021", "bejis_2022", "mugla_2021",
           "evia_2021_extended", "montiferru_2021"]
ROOT = "repo/outputs/experiments/{}/step8a/step8a_500m_modeling_dataset.parquet"
CELL_KM = 0.45  # same convention as paper/code/*.py

FEATS = ["elevation_mean", "slope_mean", "ndvi_mean", "current_lst_mean",
         "lst_anomaly_mean", "current_tvdi_mean", "tvdi_difference_mean",
         "downscaled_lst_mean", "fused_lst_mean"]


def load(reg):
    d = pd.read_parquet(ROOT.format(reg))
    d = d[(d.valid_for_modeling == True) &  # noqa: E712
          (d.burnable_tree_shrub_grass == True)].reset_index(drop=True)  # noqa: E712
    return d


def dist_to_burned_km(d):
    """Euclidean distance from every cell to the nearest burned cell, in km."""
    r0, c0 = int(d.row_500m.min()), int(d.col_500m.min())
    H = int(d.row_500m.max()) - r0 + 1
    W = int(d.col_500m.max()) - c0 + 1
    rr = (d.row_500m.to_numpy().astype(int) - r0)
    cc = (d.col_500m.to_numpy().astype(int) - c0)
    burned_grid = np.ones((H, W), dtype=bool)          # True = background
    b = d.burned.to_numpy() == 1
    burned_grid[rr[b], cc[b]] = False                  # False = seed
    dist_cells = ndimage.distance_transform_edt(burned_grid)
    return dist_cells[rr, cc] * CELL_KM


print("=" * 78)
print("STAGE 1a  AOI GEOMETRY: how much of each 'region' is far field?")
print("=" * 78)
print(f"{'region':22s} {'n':>7s} {'burned':>7s} {'med dist':>9s} {'>10km':>8s} {'max':>7s}")
store = {}
for reg in REGIONS:
    d = load(reg)
    dist = dist_to_burned_km(d)
    d["dist_km"] = dist
    store[reg] = d
    print(f"{reg:22s} {len(d):7d} {int(d.burned.sum()):7d} "
          f"{np.median(dist):8.1f}k {100*(dist>10).mean():7.1f}% {dist.max():6.1f}k")

print()
print("=" * 78)
print("STAGE 1b  ELEVATION BY DISTANCE BAND (Manavgat): is the far field uphill?")
print("=" * 78)
d = store["manavgat_2021"]
bands = [(0, 5), (5, 10), (10, 20), (20, 50), (50, 999)]
print(f"{'band':>12s} {'n':>7s} {'median elev':>12s}")
for lo, hi in bands:
    m = (d.dist_km >= lo) & (d.dist_km < hi)
    if m.sum():
        print(f"{f'{lo}-{hi} km':>12s} {int(m.sum()):7d} {d.elevation_mean[m].median():11.0f} m")
print(f"{'BURNED':>12s} {int((d.burned==1).sum()):7d} "
      f"{d.elevation_mean[d.burned == 1].median():11.0f} m")
print(f"AOI elevation max: {d.elevation_mean.max():.0f} m")

print()
print("=" * 78)
print("STAGE 1c  SIGNED UNIVARIATE AUC: full AOI vs collar-restricted")
print("   (positives are untouched by the collar; only far-field negatives drop)")
print("=" * 78)
rows = []
for collar in [None, 10, 5]:
    for reg in REGIONS:
        d = store[reg]
        sub = d if collar is None else d[d.dist_km <= collar]
        if sub.burned.nunique() < 2:
            continue
        for f in FEATS:
            v = sub[f]
            ok = v.notna()
            if ok.sum() < 50 or sub.burned[ok].nunique() < 2:
                continue
            rows.append({"collar": "full" if collar is None else f"<={collar}km",
                         "region": reg, "feature": f,
                         "auc": roc_auc_score(sub.burned[ok], v[ok]),
                         "n": int(ok.sum()), "pos": int(sub.burned[ok].sum())})
R = pd.DataFrame(rows)
for f in ["elevation_mean", "current_lst_mean", "lst_anomaly_mean", "current_tvdi_mean"]:
    print(f"\n--- {f} ---")
    piv = R[R.feature == f].pivot(index="collar", columns="region", values="auc")
    piv = piv.reindex(["full", "<=10km", "<=5km"])
    print(piv.reindex(columns=REGIONS).round(3).to_string())
    for c in ["full", "<=10km"]:
        if c in piv.index:
            v = piv.loc[c].dropna()
            print(f"    {c:8s} min {v.min():.3f} max {v.max():.3f}  "
                  f"straddles 0.5: {'YES' if (v.min()<0.5<v.max()) else 'no'}")

print()
print("=" * 78)
print("STAGE 1d  LST-ELEVATION COLLINEARITY (Q item 4)")
print("=" * 78)
print(f"{'region':22s} {'r(lst,elev)':>12s} {'r(tvdi,elev)':>13s} {'r(anom,elev)':>13s}")
for reg in REGIONS:
    d = store[reg]
    def r(a, b):
        m = d[a].notna() & d[b].notna()
        return np.corrcoef(d[a][m], d[b][m])[0, 1]
    print(f"{reg:22s} {r('current_lst_mean','elevation_mean'):12.3f} "
          f"{r('current_tvdi_mean','elevation_mean'):13.3f} "
          f"{r('lst_anomaly_mean','elevation_mean'):13.3f}")

R.to_csv(sys.argv[1], index=False)
print(f"\nwrote {sys.argv[1]}")
