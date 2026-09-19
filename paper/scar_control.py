"""
Independent re-derivation of the leave-one-scar-out control.

A referee claims that holding out an entire burned connected component together
with a 2 km buffer, and fitting on the rest of the SAME region, returns about
0.549, which would be indistinguishable from the cross-region mean of 0.541 and
would mean there is no distance effect to speak of between 2 km and 2,800 km.

That claim is large enough that it is re-derived here from scratch rather than
taken on the referee's word, with an independently written component finder and
buffer, before any of it is allowed near the manuscript.

Read-only with respect to the repository.
"""
import json
import sys

import numpy as np
import pandas as pd
from scipy import ndimage
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "code"))
import _canonical  # noqa: E402  (labelfix re-run 2026-09-19: inputs via _canonical.load)

STAGING = sys.argv[1]  # output: {STAGING}/../verify_scar.json
REGIONS = ["manavgat_2021", "bejis_2022", "mugla_2021",
           "evia_2021_extended", "montiferru_2021"]
TH = ["ndvi_mean", "elevation_mean", "slope_mean", "landcover_dominant",
      "lst_anomaly_mean", "current_lst_mean", "current_tvdi_mean",
      "tvdi_difference_mean", "downscaled_lst_mean", "fused_lst_mean"]
CAT = "landcover_dominant"
KM_PER_CELL = 0.45          # about 0.51 N-S, 0.39-0.41 E-W; one figure is enough for a buffer
MIN_SCAR = 50
BUFFERS_KM = [2, 5, 10]


def build():
    num = [f for f in TH if f != CAT]
    tr = [("num", Pipeline([("imputer", SimpleImputer(strategy="median"))]), num),
          ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                            ("onehot", OneHotEncoder(handle_unknown="ignore"))]), [CAT])]
    return Pipeline([("preprocess", ColumnTransformer(tr)),
                     ("clf", RandomForestClassifier(n_estimators=300, min_samples_leaf=3,
                                                    class_weight="balanced",
                                                    random_state=42, n_jobs=4))])


def load(reg):
    df = _canonical.load(reg,
                         columns=["burned", "valid_for_modeling", "burnable_tree_shrub_grass",
                                  "row_500m", "col_500m"] + TH)
    return df[(df.valid_for_modeling == True) & (df.burnable_tree_shrub_grass == True)].reset_index(drop=True)  # noqa: E712


rows = []
for reg in REGIONS:
    df = load(reg)
    r0, c0 = df.row_500m.min(), df.col_500m.min()
    H = int(df.row_500m.max() - r0) + 1
    W = int(df.col_500m.max() - c0) + 1
    grid = np.zeros((H, W), dtype=np.uint8)
    rr = (df.row_500m - r0).to_numpy().astype(int)
    cc = (df.col_500m - c0).to_numpy().astype(int)
    grid[rr[df.burned == 1], cc[df.burned == 1]] = 1
    lab, nlab = ndimage.label(grid, structure=np.ones((3, 3)))          # 8-connectivity
    cell_lab = lab[rr, cc]
    sizes = pd.Series(cell_lab[df.burned.to_numpy() == 1]).value_counts()
    scars = [int(s) for s in sizes[sizes >= MIN_SCAR].index if s != 0]
    print(f"{reg:20s} components >= {MIN_SCAR} cells: {len(scars)}  sizes={list(sizes[sizes>=MIN_SCAR])[:6]}",
          flush=True)
    for s in scars:
        mask_scar = np.zeros_like(grid)
        mask_scar[lab == s] = 1
        for bkm in BUFFERS_KM:
            rad = max(1, int(round(bkm / KM_PER_CELL)))
            grown = ndimage.binary_dilation(mask_scar, iterations=rad)
            held = grown[rr, cc]
            tgt = df[held & (cell_lab == s) | (held & (df.burned == 0).to_numpy())]
            tgt = df[held]
            src = df[~held]
            if src.burned.nunique() < 2 or tgt.burned.nunique() < 2:
                continue
            _canonical.assert_no_leakage(TH)
            m = build().fit(src[TH], src.burned)
            auc = roc_auc_score(tgt.burned, m.predict_proba(tgt[TH])[:, 1])
            rows.append({"region": reg, "scar": s, "buffer_km": bkm,
                         "src_pos": int(src.burned.sum()), "tgt_pos": int(tgt.burned.sum()),
                         "tgt_n": int(len(tgt)), "auc": float(auc)})
            print(f"    scar {s:3d} buffer {bkm:2d} km  src_pos={int(src.burned.sum()):5d} "
                  f"tgt_pos={int(tgt.burned.sum()):5d}  AUC={auc:.4f}", flush=True)

print("\n=== leave-one-scar-out, by buffer ===")
for b in BUFFERS_KM:
    g = [r["auc"] for r in rows if r["buffer_km"] == b]
    if g:
        print(f"  {b:2d} km buffer: n={len(g):3d}  mean={np.mean(g):.4f}  "
              f"median={np.median(g):.4f}  range {min(g):.3f} to {max(g):.3f}")
print("\ncross-region reference (frozen): mean 0.541 over 20 directions at 306 to 2802 km")
json.dump(rows, open(f"{STAGING}/../verify_scar.json", "w"), indent=1)
