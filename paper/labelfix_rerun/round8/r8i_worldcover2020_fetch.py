"""R8i. Pre-fire land cover (ESA WorldCover v100, 2020) on the pipeline's own cells (reviewers 1 and 3).

The pipeline uses WorldCover v200 (2021 images), which is post-fire for the four 2021 events. This
script fetches v100 (2020) and, as a control, v200 from Earth Engine on each region's 30 m reference
grid (the grid of drive_new/experiments/<region>/gate_inputs/reference_30m.tif, EPSG:4326), and
aggregates both to the ~500 m cells exactly as step8a does (17 x 17 pixel blocks from the grid
origin, dominant class = most frequent valid class with ties to the lowest code, fractions over
valid pixels, natural vegetation = tree + shrub + grass fraction >= 0.5).

Checks written to r8i_fetch_summary.json:
  * the fetched v200 raster against the pipeline's aligned v200 raster, pixel by pixel;
  * the v200 cell values against the landcover columns of the released modelling datasets.
Output: r8i_worldcover_cells.csv.gz (one row per cell with both years).

Needs Earth Engine access (project "thermaltwin") and the gate_inputs rasters, which are not in this
repository; the output table is released so that r8j runs without them.
"""
import json
import sys
from pathlib import Path

import ee
import numpy as np
import pandas as pd
import rasterio

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "paper" / "code"))
import _canonical  # noqa: E402

GATE = ROOT.parent / "thermal-twin" / "drive_new" / "experiments"
REG = ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended", "montiferru_2021"]
B, TILE = 17, 1024
TREE, SHRUB, GRASS, CROP = 10, 20, 30, 40
ee.Initialize(project="thermaltwin")


def fetch(img, tr, W, H):
    out = np.zeros((H, W), dtype=np.uint8)
    for r0 in range(0, H, TILE):
        for c0 in range(0, W, TILE):
            h, w = min(TILE, H - r0), min(TILE, W - c0)
            grid = {"dimensions": {"width": w, "height": h},
                    "affineTransform": {"scaleX": tr.a, "shearX": 0, "translateX": tr.c + c0 * tr.a,
                                        "shearY": 0, "scaleY": tr.e, "translateY": tr.f + r0 * tr.e},
                    "crsCode": "EPSG:4326"}
            a = ee.data.computePixels({"expression": img, "fileFormat": "NUMPY_NDARRAY", "grid": grid})
            out[r0:r0 + h, c0:c0 + w] = a["Map"]
    return out


def cells(arr):
    H, W = arr.shape
    rows = []
    for r in range(0, H, B):
        for c in range(0, W, B):
            v = arr[r:r + B, c:c + B].ravel()
            v = v[v != 0]
            if v.size == 0:
                rows.append((r // B, c // B, np.nan, np.nan, np.nan, 0))
                continue
            u, n = np.unique(v, return_counts=True)
            dom = int(u[int(np.argmax(n))])
            tsg = float(np.isin(v, (TREE, SHRUB, GRASS)).mean())
            crop = float((v == CROP).mean())
            rows.append((r // B, c // B, dom, tsg, crop, int(v.size)))
    return pd.DataFrame(rows, columns=["row_500m", "col_500m", "dominant", "tsg_fraction", "crop_fraction", "n_valid"])


summary, parts = {}, []
v100 = ee.ImageCollection("ESA/WorldCover/v100").first().select("Map").unmask(0)
v200 = ee.ImageCollection("ESA/WorldCover/v200").first().select("Map").unmask(0)
for reg in REG:
    g = GATE / reg / "gate_inputs"
    with rasterio.open(g / "reference_30m.tif") as ref:
        tr, W, H = ref.transform, ref.width, ref.height
    with rasterio.open(g / "landcover_esa_worldcover_v200_aligned_to_reference.tif") as al:
        aligned = al.read(1)
    a200 = fetch(v200, tr, W, H)
    a100 = fetch(v100, tr, W, H)
    c200, c100 = cells(a200), cells(a100)
    m = c200.merge(c100, on=["row_500m", "col_500m"], suffixes=("_2021", "_2020"))
    m.insert(0, "region", reg)
    d = _canonical.load(reg)[["row_500m", "col_500m", "landcover_dominant", "valid_for_modeling",
                              "burnable_tree_shrub_grass", "burned"]]
    j = d.merge(m, on=["row_500m", "col_500m"], how="left")
    summary[reg] = {
        "grid": [H, W],
        "pixel_agreement_fetched_v200_vs_pipeline_aligned": float((a200 == aligned).mean()),
        "cells": int(len(d)),
        "cell_dominant_agreement_v200_vs_dataset": float((j.dominant_2021 == j.landcover_dominant).mean()),
        "cell_burnable_agreement_v200_vs_dataset": float(((j.tsg_fraction_2021 >= 0.5) == j.burnable_tree_shrub_grass).mean()),
    }
    print(reg, summary[reg], flush=True)
    parts.append(m)

pd.concat(parts).to_csv(HERE / "r8i_worldcover_cells.csv.gz", index=False)
json.dump(summary, open(HERE / "r8i_fetch_summary.json", "w"), indent=1)
