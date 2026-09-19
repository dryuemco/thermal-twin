"""
Skill against separation distance: does cross-region transfer sit on the
continuation of the within-region extrapolation curve?

The positive control showed that skill falls from about 0.86 to about 0.57
without leaving a region, as soon as the held-out area is contiguous rather than
interleaved. That leaves regional difference confounded with spatial
extrapolation. This separates them, as far as this design allows.

WITHIN REGION. Each region is cut in half by a straight line, a model is fitted
on one half and applied to the other with no refit. Because the cut is a
straight line, a target cell's distance to the nearest training cell is exactly
its distance to that line, so no nearest-neighbour search is needed. Target
cells are binned by that distance and an AUC is computed per bin. This traces
skill against separation using ONE fitted model per split, so the curve is not
confounded by refitting.

ACROSS REGIONS. The twenty frozen transfer AUCs are placed at the geodesic
distance between their AOI centroids, computed from the bounding boxes in
core/regions.py.

The honest limitation is stated in the output: the within-region distances span
a few tens of km and the cross-region distances span hundreds to thousands, so
the two ranges do not overlap and the comparison is an extrapolation of the
within-region curve, not an interpolation.

Usage: distance_curve.py <staging_dir> <out.json>
"""
import json
import math
import sys

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
import _canonical


def _guard(X, y):
    """Methods 3.13: forbidden-column assertion on the exact columns passed to the model."""
    _canonical.assert_no_leakage(list(X.columns))
    return X, y


STAGING, OUT = sys.argv[1], sys.argv[2]

# (lon_min, lat_min, lon_max, lat_max), read from repo/core/regions.py
BBOX = {
    "manavgat_2021": (31.05, 36.72, 31.85, 37.35),
    "bejis_2022": (-1.05, 39.68, -0.35, 40.15),
    "mugla_2021": (27.10, 36.60, 28.90, 37.45),
    "evia_2021_extended": (23.05, 38.55, 23.85, 39.15),
    "montiferru_2021": (8.45, 40.05, 8.75, 40.27),
}
REGIONS = list(BBOX)
THERMAL = ["ndvi_mean", "elevation_mean", "slope_mean", "landcover_dominant",
           "lst_anomaly_mean", "current_lst_mean", "current_tvdi_mean",
           "tvdi_difference_mean", "downscaled_lst_mean", "fused_lst_mean"]
CAT = "landcover_dominant"
CELL_DEG = 0.0045814          # the analysis cell step, both axes
M_PER_DEG = 111319.49
SEED = 42


def haversine_km(a, b):
    lon1, lat1 = a
    lon2, lat2 = b
    r = 6371.0088
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1
    dl = math.radians(lon2 - lon1)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))


def centroid(bb):
    return ((bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2)


def build():
    num = [f for f in THERMAL if f != CAT]
    tr = [("num", Pipeline([("imputer", SimpleImputer(strategy="median"))]), num),
          ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                            ("onehot", OneHotEncoder(handle_unknown="ignore"))]), [CAT])]
    return Pipeline([("preprocess", ColumnTransformer(tr)),
                     ("clf", RandomForestClassifier(n_estimators=300, min_samples_leaf=3,
                                                    class_weight="balanced",
                                                    random_state=SEED, n_jobs=4))])


def load(reg):
    df = _canonical.load(reg,
                         columns=["burned", "valid_for_modeling", "burnable_tree_shrub_grass",
                                  "row_500m", "col_500m"] + THERMAL)
    return df[(df.valid_for_modeling == True) & (df.burnable_tree_shrub_grass == True)].reset_index(drop=True)  # noqa: E712


BINS = [0, 5, 10, 20, 40, 80, 160]
within = []
for reg in REGIONS:
    df = load(reg)
    lat = centroid(BBOX[reg])[1]
    km_ns = CELL_DEG * M_PER_DEG / 1000.0
    km_ew = km_ns * math.cos(math.radians(lat))
    for axis, col, km in (("east_west", "col_500m", km_ew), ("north_south", "row_500m", km_ns)):
        cut = df[col].median()
        for name, src_mask in (("low_to_high", df[col] <= cut), ("high_to_low", df[col] > cut)):
            src = df[src_mask]
            tgt = df[~src_mask]
            if src.burned.nunique() < 2 or tgt.burned.nunique() < 2:
                continue
            m = build().fit(*_guard(src[THERMAL], src.burned))
            p = m.predict_proba(tgt[THERMAL])[:, 1]
            d = (tgt[col] - cut).abs() * km
            for lo, hi in zip(BINS[:-1], BINS[1:]):
                sel = (d >= lo) & (d < hi)
                y = tgt.burned[sel]
                if sel.sum() < 50 or y.nunique() < 2:
                    continue
                within.append({"region": reg, "axis": axis, "direction": name,
                               "bin_lo_km": lo, "bin_hi_km": hi,
                               "median_km": float(d[sel].median()),
                               "n": int(sel.sum()), "positives": int(y.sum()),
                               "auc": float(roc_auc_score(y, p[sel.to_numpy()]))})
            print(f"{reg:20s} {axis:12s} {name:12s} bins done", flush=True)

ref = json.load(open(f"{STAGING}/comparison_inputs.json"))["transfer"]
cross = []
for s in REGIONS:
    for t in REGIONS:
        if s == t:
            continue
        k = f"{s}_to_{t}"
        if k not in ref:
            continue
        cross.append({"source": s, "target": t,
                      "distance_km": round(haversine_km(centroid(BBOX[s]), centroid(BBOX[t])), 1),
                      "auc": round(ref[k]["thermal"], 4)})

print("\n=== WITHIN-REGION: AUC by separation from the training half ===")
print(f"{'bin (km)':>12s} {'n bins':>7s} {'mean AUC':>9s} {'min':>7s} {'max':>7s}")
for lo, hi in zip(BINS[:-1], BINS[1:]):
    g = [w["auc"] for w in within if w["bin_lo_km"] == lo]
    if g:
        print(f"{f'{lo}-{hi}':>12s} {len(g):7d} {np.mean(g):9.3f} {min(g):7.3f} {max(g):7.3f}")

print("\n=== CROSS-REGION: AUC by centroid separation ===")
for c in sorted(cross, key=lambda x: x["distance_km"]):
    print(f"  {c['source'][:12]:13s}-> {c['target'][:12]:13s} {c['distance_km']:8.0f} km   {c['auc']:.4f}")
print(f"\ncross-region distance range: {min(c['distance_km'] for c in cross):.0f} to "
      f"{max(c['distance_km'] for c in cross):.0f} km, n={len(cross)}")
wk = [w["median_km"] for w in within]
print(f"within-region distance range: {min(wk):.1f} to {max(wk):.1f} km, n={len(within)} bins")

json.dump({"within": within, "cross": cross}, open(OUT, "w"), indent=1)
print(f"\nwrote {OUT}")
