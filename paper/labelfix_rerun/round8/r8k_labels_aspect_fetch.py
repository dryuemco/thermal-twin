"""R8k. Second burned-area product, terrain aspect and Landsat observation counts (reviewers 1-3).

For each region, on its 30 m reference grid (drive_new/experiments/<region>/gate_inputs/reference_30m.tif):
  * VIIRS VNP64A1 v002 and, as a control, MODIS MCD64A1 v061 burn dates inside the region's label
    window (pixels with a burn day of year outside the window are unburned). A cell is burned when
    any of its pixels is burned, as in step8a. The MCD64A1 cells are compared with the `burned`
    column of the released modelling datasets.
  * Northness and eastness (cosine and sine of aspect) from the Copernicus DEM GLO-30, cell means.
  * Landsat 8 Collection 2 Level-2 scene counts and the median number of clear observations per
    pixel (the pipeline's QA mask, src/step3_landsat_lst.py) for the predictor window and each of the
    four baseline windows.
Outputs: r8k_cells.csv.gz, r8k_landsat_observations.csv, r8k_fetch_summary.json.
Needs Earth Engine (project "thermaltwin") and the gate-input rasters; the outputs are released.
"""
import datetime as dt
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

EXP = ROOT.parent / "thermal-twin" / "drive_new" / "experiments"
REG = ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended", "montiferru_2021"]
B, TILE = 17, 1024
ee.Initialize(project="thermaltwin")


def fetch(img, band, tr, W, H, dtype):
    out = np.zeros((H, W), dtype=dtype)
    for r0 in range(0, H, TILE):
        for c0 in range(0, W, TILE):
            h, w = min(TILE, H - r0), min(TILE, W - c0)
            grid = {"dimensions": {"width": w, "height": h},
                    "affineTransform": {"scaleX": tr.a, "shearX": 0, "translateX": tr.c + c0 * tr.a,
                                        "shearY": 0, "scaleY": tr.e, "translateY": tr.f + r0 * tr.e},
                    "crsCode": "EPSG:4326"}
            a = ee.data.computePixels({"expression": img, "fileFormat": "NUMPY_NDARRAY", "grid": grid})
            out[r0:r0 + h, c0:c0 + w] = a[band]
    return out


def burn_image(coll, band, start, end):
    s, e = dt.date.fromisoformat(start), dt.date.fromisoformat(end)
    d0, d1 = s.timetuple().tm_yday, e.timetuple().tm_yday
    c = ee.ImageCollection(coll).filterDate(start[:8] + "01", (e + dt.timedelta(days=32)).isoformat()[:8] + "01").select(band)
    c = c.map(lambda i: i.updateMask(i.gte(d0).And(i.lte(d1))))
    return c.max().unmask(0).toInt16().rename("b")


def qa_clear(img):
    qa = img.select("QA_PIXEL")
    bad = (1 << 0) | (1 << 1) | (1 << 2) | (1 << 3) | (1 << 4) | (1 << 5)
    m = (qa.bitwiseAnd(bad).eq(0).And(qa.rightShift(8).bitwiseAnd(3).lt(2))
         .And(qa.rightShift(10).bitwiseAnd(3).lt(2)).And(qa.rightShift(12).bitwiseAnd(3).lt(2))
         .And(qa.rightShift(14).bitwiseAnd(3).lt(2)))
    return m.rename("clear").toInt16()


def cell_stats(arr, fn):
    H, W = arr.shape
    rows = []
    for r in range(0, H, B):
        for c in range(0, W, B):
            rows.append((r // B, c // B) + fn(arr[r:r + B, c:c + B]))
    return rows


dem = ee.ImageCollection("COPERNICUS/DEM/GLO30").select("DEM")
dem = dem.mosaic().setDefaultProjection(dem.first().projection())
asp = ee.Terrain.aspect(dem).multiply(np.pi / 180)
north = asp.cos().rename("n").toFloat()
east = asp.sin().rename("e").toFloat()

summary, parts, obs = {}, [], []
for reg in REG:
    g = EXP / reg / "gate_inputs"
    gm = json.load(open(g / "gate_inputs_metadata.json"))
    pm = json.load(open(EXP / reg / "predictor_export_metadata.json"))
    with rasterio.open(g / "reference_30m.tif") as ref:
        tr, W, H = ref.transform, ref.width, ref.height
    ls, le = gm["label_window"]
    vnp = fetch(burn_image("NASA/VIIRS/002/VNP64A1", "Burn_Date", ls, le), "b", tr, W, H, np.int16)
    mcd = fetch(burn_image("MODIS/061/MCD64A1", "BurnDate", ls, le), "b", tr, W, H, np.int16)
    nn = fetch(north, "n", tr, W, H, np.float32)
    ea = fetch(east, "e", tr, W, H, np.float32)
    burned = lambda blk: (int((blk > 0).any()),)  # noqa: E731
    mean = lambda blk: (float(np.nanmean(blk)) if np.isfinite(blk).any() else np.nan,)  # noqa: E731
    cols = {"vnp_burned": cell_stats(vnp, burned), "mcd_burned": cell_stats(mcd, burned),
            "northness": cell_stats(nn, mean), "eastness": cell_stats(ea, mean)}
    df = pd.DataFrame(cols["vnp_burned"], columns=["row_500m", "col_500m", "vnp_burned"])
    for k in ("mcd_burned", "northness", "eastness"):
        df[k] = [x[2] for x in cols[k]]
    df.insert(0, "region", reg)
    d = _canonical.load(reg)[["row_500m", "col_500m", "burned"]]
    j = d.merge(df, on=["row_500m", "col_500m"], how="left")
    summary[reg] = {"label_window": [ls, le],
                    "mcd_cells_agree_with_dataset": float((j.mcd_burned == j.burned).mean()),
                    "mcd_burned_cells": int(j.mcd_burned.sum()), "dataset_burned_cells": int(j.burned.sum()),
                    "vnp_burned_cells": int(j.vnp_burned.sum())}
    parts.append(df)
    # Landsat observations: predictor window and the same calendar window in each baseline year
    aoi = ee.Geometry.Rectangle(gm["aoi_bounds"])
    ps, pe = pm["predictor_start_date"], pm["predictor_end_date"]
    windows = [("current", ps, pe)] + [(f"baseline_{y}", f"{y}{ps[4:]}", f"{y}{pe[4:]}") for y in pm["baseline_years"]]
    for tag, s, e in windows:
        e1 = (dt.date.fromisoformat(e) + dt.timedelta(days=1)).isoformat()
        coll = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2").filterBounds(aoi).filterDate(s, e1)
        n = coll.size().getInfo()
        cnt = coll.map(qa_clear).sum().unmask(0)
        med = cnt.reduceRegion(ee.Reducer.percentile([10, 50, 90]), aoi, 300, maxPixels=1e9, bestEffort=True).getInfo()
        obs.append({"region": reg, "window": tag, "start": s, "end": e, "scenes": n,
                    "clear_obs_p10": med.get("clear_p10"), "clear_obs_median": med.get("clear_p50"),
                    "clear_obs_p90": med.get("clear_p90")})
    print(reg, summary[reg], [(o["window"], o["scenes"], o["clear_obs_median"]) for o in obs if o["region"] == reg], flush=True)

pd.concat(parts).to_csv(HERE / "r8k_cells.csv.gz", index=False)
pd.DataFrame(obs).to_csv(HERE / "r8k_landsat_observations.csv", index=False)
json.dump(summary, open(HERE / "r8k_fetch_summary.json", "w"), indent=1)
