"""Shared machinery for the ems_labels_* analyses (referee R3, label quality).

Everything model-related is IMPORTED from step10 (the code that produced Table 1) and
everything label-related is IMPORTED from the upstream pipeline in repo/ (read-only;
bytecode writing is disabled before import so nothing is written into repo/).
See paper/ems_analyses/labels/SPEC.md.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # never write __pycache__ into repo/ or step10/

import json
import os
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
TREE = HERE.parents[1]                      # thermal-twin-main
OUT = TREE / "paper" / "ems_analyses" / "labels"
UPSTREAM = Path(r"C:\Users\CORSAIR\projects\thermal-twin")
REPO = UPSTREAM / "repo"
FROZEN = UPSTREAM / "drive_new" / "experiments"

sys.path.insert(0, str(HERE))
sys.path.insert(0, str(TREE / "step10"))

import _canonical as C  # noqa: E402
import within_cv  # noqa: E402
from spatial_bootstrap import delta_block_bootstrap_ci, block_bootstrap_ci  # noqa: E402,F401
from data_io import add_spatial_block_id  # noqa: E402

# n_jobs=4 on a shared machine; RF output does not depend on n_jobs.
within_cv.STEP8B_RF_PARAMS["n_jobs"] = 4

REGIONS = list(C.REGIONS)
BLOCK = 17
CELL_KM = 0.45
NODATA = -32768


def log(*a):
    print(*a, flush=True)


# ----------------------------------------------------------------------------- data
def tsg(region: str, columns=None) -> pd.DataFrame:
    d = C.load(region, columns=columns)
    return d[(d.valid_for_modeling == True) &  # noqa: E712
             (d.burnable_tree_shrub_grass == True)].reset_index(drop=True)  # noqa: E712


def experiment(region: str) -> dict:
    sys.path.insert(0, str(REPO))
    from core.regions import EXPERIMENTS
    return EXPERIMENTS[region]


# ----------------------------------------------------------------------------- blocks
def block_reduce(arr: np.ndarray, fn) -> np.ndarray:
    """Apply fn over every 17x17 block of a 30 m array, edge blocks truncated,
    returning a (n_rows_500m, n_cols_500m) array. fn gets a 2-D block."""
    H, W = arr.shape
    nr, nc = -(-H // BLOCK), -(-W // BLOCK)
    out = np.zeros((nr, nc), dtype="float64")
    for i in range(nr):
        for j in range(nc):
            out[i, j] = fn(arr[i * BLOCK:(i + 1) * BLOCK, j * BLOCK:(j + 1) * BLOCK])
    return out


def any_positive(arr: np.ndarray) -> np.ndarray:
    """Cell flag: >= 1 sub-pixel with value > 0 (nodata excluded)."""
    pos = (arr > 0) & (arr != NODATA)
    H, W = pos.shape
    nr, nc = -(-H // BLOCK), -(-W // BLOCK)
    pad = np.zeros((nr * BLOCK, nc * BLOCK), dtype=bool)
    pad[:H, :W] = pos
    return pad.reshape(nr, BLOCK, nc, BLOCK).any(axis=(1, 3))


def block_count(mask: np.ndarray) -> np.ndarray:
    H, W = mask.shape
    nr, nc = -(-H // BLOCK), -(-W // BLOCK)
    pad = np.zeros((nr * BLOCK, nc * BLOCK), dtype="int64")
    pad[:H, :W] = mask
    return pad.reshape(nr, BLOCK, nc, BLOCK).sum(axis=(1, 3))


def cell_values(df: pd.DataFrame, grid: np.ndarray) -> np.ndarray:
    return grid[df.row_500m.to_numpy().astype(int), df.col_500m.to_numpy().astype(int)]


# ----------------------------------------------------------------------------- earth engine
_EE = False


def ee_init():
    global _EE
    import ee
    if not _EE:
        ee.Initialize(project="thermaltwin")
        _EE = True
    return ee


def s6():
    """The upstream Step6 module, imported read-only."""
    sys.path.insert(0, str(REPO))
    ee_init()
    import src.step6_validate_fire_relation as m
    return m


def region_geometry(region: str):
    sys.path.insert(0, str(REPO))
    ee_init()
    from core.regions import get_region_for_experiment
    return get_region_for_experiment(region)


def local_grid(region: str):
    import rasterio
    with rasterio.open(FROZEN / region / "validation/labels/mcd64a1_raw.tif") as s:
        return s.transform, s.width, s.height


def fetch(image, region: str, band: str, chunk_rows: int = 800) -> np.ndarray:
    """computePixels of a single-band int16 image on the region's exact 30 m reference
    grid (the local mcd64a1_raw.tif transform), masked pixels -> -32768. Read-only."""
    ee = ee_init()
    T, W, H = local_grid(region)
    img = image.select([band]).unmask(NODATA).toInt16()
    out = np.empty((H, W), dtype="int16")
    for r0 in range(0, H, chunk_rows):
        h = min(chunk_rows, H - r0)
        req = {
            "expression": img,
            "fileFormat": "NUMPY_NDARRAY",
            "grid": {
                "dimensions": {"width": W, "height": h},
                "affineTransform": {"scaleX": T.a, "shearX": T.b, "translateX": T.c,
                                    "shearY": T.d, "scaleY": T.e,
                                    "translateY": T.f + r0 * T.e},
                "crsCode": "EPSG:4326",
            },
        }
        for attempt in range(4):
            try:
                a = ee.data.computePixels(req)
                break
            except Exception as exc:  # noqa: BLE001
                if attempt == 3:
                    raise
                log(f"    retry {attempt + 1}: {str(exc)[:120]}")
        out[r0:r0 + h] = a[band]
    return out


def read_local(region: str, name: str) -> np.ndarray:
    import rasterio
    with rasterio.open(FROZEN / region / "validation/labels" / name) as s:
        return s.read(1)


# ----------------------------------------------------------------------------- models
def within(df: pd.DataFrame, B: int) -> dict:
    """Baseline vs thermal, spatially blocked OOF (step10 code) + paired block bootstrap."""
    C.assert_no_leakage(C.BASELINE)
    C.assert_no_leakage(C.THERMAL)
    blocks = add_spatial_block_id(df, B).to_numpy()
    o = within_cv.run_oof(df, blocks)
    from sklearn.metrics import roc_auc_score
    b = roc_auc_score(o["y"], o["oof_baseline"])
    t = roc_auc_score(o["y"], o["oof_thermal"])
    ci = delta_block_bootstrap_ci(o["y"], o["oof_baseline"], o["oof_thermal"], blocks)
    pos_blocks = int(pd.Series(o["y"]).groupby(blocks).max().sum())
    return {"B": B, "n": int(len(df)), "n_pos": int(o["y"].sum()), "n_blocks": o["n_blocks"],
            "n_pos_blocks": pos_blocks, "baseline": b, "thermal": t, "delta": t - b,
            "delta_ci": ci["delta_auc_ci95"], "support": ci["delta_auc_interpretation"]}


def fmt_within(r: dict) -> str:
    lo, hi = r["delta_ci"]
    return (f"B={r['B']:2d} n={r['n']:6d} pos={r['n_pos']:5d} posblk={r['n_pos_blocks']:4d} "
            f"base={r['baseline']:.4f} therm={r['thermal']:.4f} "
            f"d={r['delta']:+.4f} [{lo:+.4f},{hi:+.4f}] {r['support']}")


def transfer_pipeline(feats):
    from sklearn.compose import ColumnTransformer
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.impute import SimpleImputer
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder
    C.assert_no_leakage(feats)
    cat = "landcover_dominant"
    num = [f for f in feats if f != cat]
    tr = [("num", Pipeline([("imputer", SimpleImputer(strategy="median"))]), num),
          ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                            ("onehot", OneHotEncoder(handle_unknown="ignore"))]), [cat])]
    return Pipeline([("preprocess", ColumnTransformer(tr)),
                     ("clf", RandomForestClassifier(n_estimators=300, min_samples_leaf=3,
                                                    class_weight="balanced",
                                                    random_state=42, n_jobs=4))])


def transfer_matrix(data: dict) -> pd.DataFrame:
    """20 ordered directions, baseline and thermal, fitted on the whole source."""
    from sklearn.metrics import roc_auc_score
    preds = {}
    for s in REGIONS:
        for lbl, feats in (("baseline", C.BASELINE), ("thermal", C.THERMAL)):
            m = transfer_pipeline(feats).fit(data[s][feats], data[s].burned)
            for t in REGIONS:
                if t != s:
                    preds[(s, t, lbl)] = m.predict_proba(data[t][feats])[:, 1]
    rows = []
    for s in REGIONS:
        for t in REGIONS:
            if s == t:
                continue
            y = data[t].burned.to_numpy()
            pb, pt = preds[(s, t, "baseline")], preds[(s, t, "thermal")]
            row = {"source": s, "target": t, "baseline": roc_auc_score(y, pb),
                   "thermal": roc_auc_score(y, pt)}
            row["delta"] = row["thermal"] - row["baseline"]
            for B in (10, 2):
                ci = delta_block_bootstrap_ci(y, pb, pt, add_spatial_block_id(data[t], B).to_numpy())
                row[f"delta_ci_B{B}"] = ci["delta_auc_ci95"]
                row[f"support_B{B}"] = ci["delta_auc_interpretation"]
            rows.append(row)
            log(f"    {s:>20s} -> {t:20s} base={row['baseline']:.4f} therm={row['thermal']:.4f} "
                f"d={row['delta']:+.4f} B10 {row['support_B10']}")
    return pd.DataFrame(rows)


def dump(obj, name: str):
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / name, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
