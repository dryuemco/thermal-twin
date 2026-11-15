"""panel_export.py: TMA checkpoint 2 (plan amendment 13), the MODIS predictor-label panel of the 31 development
sites on their existing 500 m fire grids. One GeoTIFF per site and target year y (cut-off 1 May y):

  ndvi, evi    mean of the MOD13A1 v061 composites whose whole 16-day interval lies inside the 58 days before
               1 May y (three per year; SummaryQA <= 1), scaled, averaged onto the grid cell
  lst_day,     mean MOD11A1 v061 LST_Day_1km and LST_Night_1km (K) over the same 58 days (QC bits 0-1 <= 1: LST produced; good or other quality)
  lst_night
  burn         share of the cell area with an MCD64A1 BurnDate from 1 May y to 30 April y+1 (area-weighted)
  unmapped     mean share of the target months whose MCD64A1 QA bit 0 is 0 or masked
  natural      share of the cell in MCD12Q1 LC_Type1 classes 1-10 in the map of year y-1 (for y = 2001, and for
               years without a published y-1 map, the latest map before y; flagged in the metadata)
plus one static file per site with elevation and slope (Copernicus GLO-30, mean onto the grid) and the burned
share from November 2000 to 30 April 2001 (history start).
Reflectance and LST are averaged and burn shares area-weighted onto the existing grid (crs_transform of the
site's 500 m grid), so later-burning evaluation and the earlier models use the same cells. Target year 2026
(May 2026 to April 2027) is filled only to the last published MCD64A1 month and is marked incomplete.
Writes $THERMAL_TWIN_SCALEUP/analysis/tma/panel/<site>/<y>.tif, static.tif and meta.json.
"""
import json
import os
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
from pathlib import Path

import ee
import rasterio

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scaleup"))
import s2_label_check_export as S  # noqa: E402

OUT = S.SCALEUP / "analysis" / "tma" / "panel"
YEARS = range(2001, 2027)
LC_YEARS = range(2001, 2026)


def grid(site):
    with rasterio.open(S.grid_path(site)) as g:
        t, (h, w) = g.transform, g.shape
    return [t.a, t.b, t.c, t.d, t.e, t.f], h, w


def fetch(img, tr, h, w, path):
    url = img.toFloat().getDownloadURL({"crs": "EPSG:4326", "crs_transform": tr, "dimensions": f"{w}x{h}", "format": "GEO_TIFF"})
    with urllib.request.urlopen(url, timeout=1800) as r, open(path, "wb") as f:
        f.write(r.read())


def year_image(y):
    cut = date(y, 5, 1)
    w0 = cut - timedelta(days=58)
    m13 = ee.ImageCollection("MODIS/061/MOD13A1").filterDate(w0.isoformat(), cut.isoformat())
    m13 = m13.filter(ee.Filter.lte("system:time_start", ee.Date((cut - timedelta(days=16)).isoformat()).millis()))
    m13 = m13.filter(ee.Filter.gte("system:time_start", ee.Date(w0.isoformat()).millis()))
    vi = m13.map(lambda im: im.select(["NDVI", "EVI"]).updateMask(im.select("SummaryQA").lte(1)).multiply(0.0001)).mean()
    m11 = ee.ImageCollection("MODIS/061/MOD11A1").filterDate(w0.isoformat(), cut.isoformat())
    lst = m11.map(lambda im: ee.Image.cat(
        im.select("LST_Day_1km").updateMask(im.select("QC_Day").bitwiseAnd(3).lte(1)),
        im.select("LST_Night_1km").updateMask(im.select("QC_Night").bitwiseAnd(3).lte(1))).multiply(0.02)).mean()
    t0, t1 = cut, date(y + 1, 4, 30)
    mcd = ee.ImageCollection("MODIS/061/MCD64A1").filterDate(t0.isoformat(), (t1 + timedelta(days=1)).isoformat())
    burn = mcd.map(lambda im: im.select("BurnDate").gt(0).unmask(0)).max().unmask(0)
    unm = mcd.map(lambda im: im.select("QA").unmask(0).bitwiseAnd(1).eq(0)).mean()
    lcy = max(min(y - 1, max(LC_YEARS)), 2001)
    lc = ee.ImageCollection("MODIS/061/MCD12Q1").filterDate(f"{lcy}-01-01", f"{lcy + 1}-01-01").first().select("LC_Type1")
    nat = lc.gte(1).And(lc.lte(10))
    proj = ee.ImageCollection("MODIS/061/MCD64A1").first().projection()
    agg = lambda im: im.reproject(proj).reduceResolution(ee.Reducer.mean(), maxPixels=1024)  # noqa: E731
    lst_r = lst.reproject(ee.ImageCollection("MODIS/061/MOD11A1").first().projection())
    return ee.Image.cat(agg(vi.select("NDVI")).rename("ndvi"), agg(vi.select("EVI")).rename("evi"),
                        lst_r.select("LST_Day_1km").rename("lst_day"), lst_r.select("LST_Night_1km").rename("lst_night"),
                        agg(burn).rename("burn"), agg(unm).rename("unmapped"), agg(nat).rename("natural")), lcy


def static_image():
    dem = ee.ImageCollection("COPERNICUS/DEM/GLO30").select("DEM").mosaic().setDefaultProjection("EPSG:4326", None, 30)
    slope = ee.Terrain.slope(dem)
    pre = ee.ImageCollection("MODIS/061/MCD64A1").filterDate("2000-11-01", "2001-05-01").map(
        lambda im: im.select("BurnDate").gt(0).unmask(0)).max().unmask(0)
    proj = ee.ImageCollection("MODIS/061/MCD64A1").first().projection()
    return ee.Image.cat(dem.reduceResolution(ee.Reducer.mean(), maxPixels=65535).rename("elevation"),
                        slope.reduceResolution(ee.Reducer.mean(), maxPixels=65535).rename("slope"),
                        pre.reproject(proj).reduceResolution(ee.Reducer.mean(), maxPixels=1024).rename("burn_pre2001"))


def site_job(site):
    tr, h, w = grid(site)
    d = OUT / site
    d.mkdir(parents=True, exist_ok=True)
    meta = {"site": site, "grid": [h, w], "lc_year_used": {}, "incomplete_target_years": [2026]}
    if not (d / "static.tif").exists():
        fetch(static_image(), tr, h, w, d / "static.tif")
    for y in YEARS:
        img, lcy = year_image(y)
        meta["lc_year_used"][y] = lcy
        if not (d / f"{y}.tif").exists():
            fetch(img, tr, h, w, d / f"{y}.tif")
    meta["lc_fallback_years"] = [y for y, l in meta["lc_year_used"].items() if l != y - 1]
    (d / "meta.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    print(site, "done", flush=True)


def main():
    ee.Initialize(project=os.environ["GEE_PROJECT"])
    sites = sys.argv[1:] or (S.PAPER + [x for x in S.regions.SCALEUP_EXPERIMENT_IDS if not x.startswith("rp")])
    with ThreadPoolExecutor(6) as ex:
        list(ex.map(site_job, sites))


if __name__ == "__main__":
    main()
