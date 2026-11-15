"""event_export.py: burn dates for event extraction (plan 14.2, R* pre-check and task G-C). For each site, on its 500 m
grid extended by BUF cells on every side (so that events are not cut at the study rectangle), one band per calendar
year 2001-2026: the earliest MCD64A1 BurnDate (day of year) among the 500 m pixels of the cell, 0 if none.
Writes $THERMAL_TWIN_SCALEUP/analysis/tma/events/<site>.tif and <site>.json (offset of the original grid).
"""
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import ee

sys.path.insert(0, str(Path(__file__).resolve().parent))
import panel_export as PE  # noqa: E402

OUT = PE.OUT.parent / "events"
BUF = 22                                     # cells, about 10 km


def site_job(site):
    if (OUT / f"{site}.tif").exists():
        return
    tr, h, w = PE.grid(site)
    tr2 = [tr[0], tr[1], tr[2] - BUF * tr[0], tr[3], tr[4], tr[5] - BUF * tr[4]]
    proj = ee.ImageCollection("MODIS/061/MCD64A1").first().projection()
    bands = []
    for y in range(2001, 2027):
        bd = ee.ImageCollection("MODIS/061/MCD64A1").filterDate(f"{y}-01-01", f"{y + 1}-01-01").map(
            lambda im: im.select("BurnDate").updateMask(im.select("BurnDate").gt(0))).min()
        bands.append(bd.reproject(proj).reduceResolution(ee.Reducer.min(), maxPixels=1024).unmask(0).rename(f"doy_{y}"))
    PE.fetch(ee.Image.cat(bands), tr2, h + 2 * BUF, w + 2 * BUF, OUT / f"{site}.tif")
    (OUT / f"{site}.json").write_text(json.dumps({"buffer_cells": BUF, "rows": h, "cols": w}), encoding="utf-8")
    print(site, "done", flush=True)


def main():
    ee.Initialize(project=os.environ["GEE_PROJECT"])
    OUT.mkdir(parents=True, exist_ok=True)
    sites = sys.argv[1:] or sorted(p.name for p in PE.OUT.iterdir() if p.is_dir())
    with ThreadPoolExecutor(6) as ex:
        list(ex.map(site_job, sites))


if __name__ == "__main__":
    main()
