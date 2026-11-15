"""extra_export.py: extra panel layers for the baseline exploration (plan 13, exploratory). One GeoTIFF per site with,
for each target year y (cut-off 1 May y), three bands on the site's 500 m grid:
  lastburn_y  days from 2000-11-01 to the latest MCD64A1 burn date before 1 May y (max over the 500 m pixels in the
              cell; 0 if none), so months since the last burn can be computed at the cut-off
  myd_night_y mean MYD11A1 v061 LST_Night_1km (K) over the 58 days before 1 May y (QC bits 0-1 <= 1)
  lc_y        MCD12Q1 LC_Type1 class (mode) of the map of year y - 1 (latest published map before y if missing)
Writes $THERMAL_TWIN_SCALEUP/analysis/tma/extra/<site>.tif
"""
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
from pathlib import Path

import ee

sys.path.insert(0, str(Path(__file__).resolve().parent))
import panel_export as PE  # noqa: E402

OUT = PE.OUT.parent / "extra"
ORIGIN = date(2000, 11, 1)


def year_bands(y):
    cut = date(y, 5, 1)
    w0 = cut - timedelta(days=58)
    mcd = ee.ImageCollection("MODIS/061/MCD64A1").filterDate(ORIGIN.isoformat(), cut.isoformat())

    def days(im):
        d = ee.Date(im.get("system:time_start"))
        y0 = ee.Date.fromYMD(d.get("year"), 1, 1)
        base = y0.difference(ee.Date(ORIGIN.isoformat()), "day")
        bd = im.select("BurnDate")
        return bd.add(base).subtract(1).updateMask(bd.gt(0).And(bd.add(base).subtract(1).lt(
            ee.Date(cut.isoformat()).difference(ee.Date(ORIGIN.isoformat()), "day")))).toFloat()
    last = mcd.map(days).max().unmask(0)
    proj = ee.ImageCollection("MODIS/061/MCD64A1").first().projection()
    last = last.reproject(proj).reduceResolution(ee.Reducer.max(), maxPixels=1024).rename(f"lastburn_{y}")
    myd = ee.ImageCollection("MODIS/061/MYD11A1").filterDate(w0.isoformat(), cut.isoformat()).map(
        lambda im: im.select("LST_Night_1km").updateMask(im.select("QC_Night").bitwiseAnd(3).lte(1)).multiply(0.02)).mean()
    if y < 2003:                                    # Aqua starts in July 2002: no full window before 2003
        myd = ee.Image.constant(0).toFloat().updateMask(ee.Image.constant(0))
    myd = myd.reproject(ee.ImageCollection("MODIS/061/MOD11A1").first().projection()).rename(f"myd_night_{y}")
    lcy = max(min(y - 1, max(PE.LC_YEARS)), 2001)
    lc = ee.ImageCollection("MODIS/061/MCD12Q1").filterDate(f"{lcy}-01-01", f"{lcy + 1}-01-01").first().select("LC_Type1")
    lc = lc.reproject(proj).reduceResolution(ee.Reducer.mode(), maxPixels=1024).rename(f"lc_{y}")
    return [last, myd, lc]


def site_job(site):
    if (OUT / f"{site}.tif").exists():
        return
    tr, h, w = PE.grid(site)
    img = ee.Image.cat([b for y in PE.YEARS for b in year_bands(y)])
    PE.fetch(img, tr, h, w, OUT / f"{site}.tif")
    print(site, "done", flush=True)


def main():
    ee.Initialize(project=os.environ["GEE_PROJECT"])
    OUT.mkdir(parents=True, exist_ok=True)
    sites = sys.argv[1:] or sorted(p.name for p in PE.OUT.iterdir() if p.is_dir())
    with ThreadPoolExecutor(6) as ex:
        list(ex.map(site_job, sites))


if __name__ == "__main__":
    main()
