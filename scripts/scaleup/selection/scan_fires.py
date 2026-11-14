"""scan_fires.py: rule-based list of large Mediterranean wildfires, 2017 to 2023, from MCD64A1 on Earth Engine.

Pilot helper for the scale-up test (not part of the pipeline, writes only next to itself).

Rule
1. For each year, cells that MCD64A1 marks as burned and that MCD12Q1 (IGBP) classes as natural vegetation
   (classes 1 to 10) are counted on a 0.1 degree grid over the Mediterranean (lon -10 to 37, lat 30 to 46).
2. Grid cells with at least MIN_CELL burned pixels are joined into clusters (8-connected). A cluster is a
   candidate when it holds at least MIN_CLUSTER burned pixels (about 21.5 ha each).
3. For every candidate, the burn dates inside its box are read. The event is the run of burn dates without
   a gap longer than GAP days that holds the most pixels. Its first date is the anchor.
4. Windows follow the rule already used in the pipeline for mugla_2022_event_relative: a 58-day predictor
   window that ends the day before the anchor, a 49-day label window that starts on the anchor, and the four
   previous years as baseline.
5. The rectangle is the bounds of the pixels dated inside the label window plus MARGIN degrees on every
   side, rounded outward to 0.01 degree.

Output: candidates.json (one record per candidate, largest first).
"""
import datetime as dt
import json
import math
import sys
from pathlib import Path

import ee
import numpy as np
from scipy import ndimage

sys.stdout.reconfigure(encoding="utf-8")
ee.Initialize(project="thermaltwin")
HERE = Path(__file__).resolve().parent
LON0, LAT0, LON1, LAT1 = -10.0, 30.0, 37.0, 46.0
STEP = 0.1
YEARS = range(2017, 2024)
MIN_CELL, MIN_CLUSTER, GAP, MARGIN = 15, 450, 5, 0.15
PX = 463.3127
REGION = ee.Geometry.BBox(LON0, LAT0, LON1, LAT1)
EXISTING = {  # the five study areas already processed (bbox), to tag candidates that fall inside them
    "manavgat_2021": (31.05, 36.72, 31.85, 37.35), "bejis_2022": (-1.05, 39.68, -0.35, 40.15),
    "mugla_2021": (27.10, 36.60, 28.90, 37.45), "evia_2021_extended": (23.05, 38.55, 23.85, 39.15),
    "montiferru_2021": (8.45, 40.05, 8.75, 40.27),
}


def burned_natural(year):
    burn = (ee.ImageCollection("MODIS/061/MCD64A1").filterDate(f"{year}-01-01", f"{year + 1}-01-01")
            .select("BurnDate").max())
    lc = ee.ImageCollection("MODIS/061/MCD12Q1").filterDate(f"{min(year, 2023)}-01-01", f"{min(year, 2023) + 1}-01-01").first().select("LC_Type1")
    natural = lc.gte(1).And(lc.lte(10))
    return burn, burn.gt(0).unmask(0).And(natural.unmask(0))


def grid_counts(year):
    _, mask = burned_natural(year)
    n_lon, n_lat = round((LON1 - LON0) / STEP), round((LAT1 - LAT0) / STEP)
    img = (mask.reduceResolution(ee.Reducer.sum().unweighted(), maxPixels=2048)
           .reproject(crs="EPSG:4326", crsTransform=[STEP, 0, LON0, 0, -STEP, LAT1]).rename("n"))
    out = np.zeros((n_lat, n_lon))
    half = n_lon // 2                                           # two requests keep each response small
    for j0, j1 in ((0, half), (half, n_lon)):
        box = ee.Geometry.BBox(LON0 + j0 * STEP, LAT0, LON0 + j1 * STEP, LAT1)
        arr = img.sampleRectangle(region=box, defaultValue=0).get("n").getInfo()
        a = np.array(arr, dtype=float)
        out[:a.shape[0], j0:j0 + a.shape[1]] = a[:n_lat, :j1 - j0]
    return out


def event(year, box):
    burn, _ = burned_natural(year)
    geom = ee.Geometry.BBox(*box)
    hist = burn.reduceRegion(ee.Reducer.frequencyHistogram(), geom, scale=PX, maxPixels=1e9).get("BurnDate").getInfo() or {}
    days = sorted((int(float(k)), int(v)) for k, v in hist.items() if float(k) > 0)
    if not days:
        return None
    runs, cur = [], [days[0]]
    for d, n in days[1:]:
        if d - cur[-1][0] <= GAP:
            cur.append((d, n))
        else:
            runs.append(cur)
            cur = [(d, n)]
    runs.append(cur)
    best = max(runs, key=lambda r: sum(n for _, n in r))
    total, in_run = sum(n for _, n in days), sum(n for _, n in best)
    anchor = dt.date(year, 1, 1) + dt.timedelta(best[0][0] - 1)
    last = dt.date(year, 1, 1) + dt.timedelta(best[-1][0] - 1)
    label_end = anchor + dt.timedelta(48)
    d0, d1 = best[0][0], (label_end - dt.date(year, 1, 1)).days + 1
    m = burn.gte(d0).And(burn.lte(d1))
    r = ee.Image.pixelLonLat().updateMask(m).reduceRegion(ee.Reducer.minMax(), geom, scale=PX, maxPixels=1e9).getInfo()
    lo = lambda v: math.floor((v - MARGIN) * 100) / 100
    hi = lambda v: math.ceil((v + MARGIN) * 100) / 100
    aoi = (lo(r["longitude_min"]), lo(r["latitude_min"]), hi(r["longitude_max"]), hi(r["latitude_max"]))
    return {"anchor": str(anchor), "event_last_burn": str(last), "event_pixels": in_run, "year_pixels_in_box": total,
            "event_share": round(in_run / total, 3),
            "predictor_start": str(anchor - dt.timedelta(58)), "predictor_end": str(anchor - dt.timedelta(1)),
            "label_start": str(anchor), "label_end": str(label_end),
            "baseline_years": [year - 4, year - 3, year - 2, year - 1],
            "scar_bounds": [round(r[k], 4) for k in ("longitude_min", "latitude_min", "longitude_max", "latitude_max")],
            "aoi": aoi, "aoi_deg": [round(aoi[2] - aoi[0], 2), round(aoi[3] - aoi[1], 2)]}


cands = []
for year in YEARS:
    g = grid_counts(year)
    lab, n = ndimage.label(g >= MIN_CELL, structure=np.ones((3, 3)))
    for k in range(1, n + 1):
        sel = lab == k
        tot = float(g[sel].sum())
        if tot < MIN_CLUSTER:
            continue
        rows, cols = np.where(sel)
        box = (LON0 + cols.min() * STEP - 0.05, LAT1 - (rows.max() + 1) * STEP - 0.05,
               LON0 + (cols.max() + 1) * STEP + 0.05, LAT1 - rows.min() * STEP + 0.05)
        cands.append({"year": year, "grid_pixels": int(tot), "search_box": [round(v, 2) for v in box]})
    print(year, "clusters kept:", sum(c["year"] == year for c in cands), flush=True)

out = []
for c in sorted(cands, key=lambda c: -c["grid_pixels"]):
    e = event(c["year"], c["search_box"])
    if e is None:
        continue
    cx, cy = (e["aoi"][0] + e["aoi"][2]) / 2, (e["aoi"][1] + e["aoi"][3]) / 2
    inside = [k for k, b in EXISTING.items() if b[0] <= cx <= b[2] and b[1] <= cy <= b[3]]
    rec = {**c, **e, "inside_existing_study_area": inside}
    out.append(rec)
    print(f"{c['year']} px {e['event_pixels']:5d} ({e['event_pixels'] * 21.47 / 1000:6.1f} kha) share {e['event_share']:.2f} "
          f"anchor {e['anchor']} aoi {e['aoi']} {inside}", flush=True)
out.sort(key=lambda r: -r["event_pixels"])
(HERE / "candidates.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print("candidates:", len(out))
