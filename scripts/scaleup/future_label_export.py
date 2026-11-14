"""future_label_export.py: future and history labels for G1 (plan amendment 9.2 and 9.8) on each fire's 500 m grid.

Bands (MODIS/061/MCD64A1, BurnDate; monthly images dated on the first of the month):
  1 fut_all     share of the cell with a BurnDate after label_end and on or before 2023-12-31
  2 fut_2y      the same, up to label_end + 730 days
  3 unmapped    mean share of months in the full horizon whose QA bit 0 (valid data) is 0 or masked
  4 fut_year    first year with a future burn (0 if none; mode of the 500 m pixels)
  5 hist_pre    share burned at least once from 2001-01-01 to the day before predictor_start
Writes $THERMAL_TWIN_SCALEUP/analysis/future/<fire>.tif
"""
import os
import sys
import urllib.request
from datetime import date, timedelta
from pathlib import Path

import ee
import rasterio

sys.path.insert(0, str(Path(__file__).resolve().parent))
import s2_label_check_export as S  # noqa: E402

OUT = S.SCALEUP / "analysis" / "future"
MCD = "MODIS/061/MCD64A1"


def month_start(d):
    return date(d.year, d.month, 1)


def next_month(d):
    return date(d.year + (d.month == 12), d.month % 12 + 1, 1)


def burned_between(d_after, d_to):
    """Pixel burned on a day > d_after and <= d_to (both dates), from BurnDate of the monthly images."""
    imgs = []
    m = month_start(d_after)
    while m <= d_to:
        nm = next_month(m)
        im = ee.ImageCollection(MCD).filterDate(m.isoformat(), nm.isoformat()).first().select("BurnDate")
        lo = d_after.timetuple().tm_yday if (m.year, m.month) == (d_after.year, d_after.month) else 0
        hi = d_to.timetuple().tm_yday if (m.year, m.month) == (d_to.year, d_to.month) else 400
        imgs.append(im.gt(lo).And(im.lte(hi)).unmask(0))
        m = nm
    return ee.ImageCollection(imgs).max()


def export(exp):
    e = S.regions.EXPERIMENTS[exp]
    le, ps = date.fromisoformat(e["label_end_date"]), date.fromisoformat(e["predictor_start_date"])
    end = date(2023, 12, 31)
    with rasterio.open(S.grid_path(exp)) as g:
        t, (h, w) = g.transform, g.shape
    proj = ee.ImageCollection(MCD).first().projection()
    col = ee.ImageCollection(MCD).filterDate(month_start(le).isoformat(), "2024-01-01")
    # BurnDate is masked on unburned land in Earth Engine; valid data = bit 0 of QA (plan 9.9)
    unm = col.map(lambda im: im.select("QA").unmask(0).bitwiseAnd(1).eq(0)).mean()
    years = col.map(lambda im: im.select("BurnDate").gt(0).multiply(ee.Number.parse(im.date().format("YYYY"))).toInt16().selfMask())
    fut_all = burned_between(le, end)
    fut_year = years.min().unmask(0).updateMask(fut_all).unmask(0)   # approx: first burn year of the horizon
    bands = [fut_all, burned_between(le, min(end, le + timedelta(days=730))), unm, fut_year,
             burned_between(date(2000, 12, 31), ps - timedelta(days=1))]
    reduced = [b.reproject(proj).reduceResolution(ee.Reducer.mean(), maxPixels=1024) for b in bands[:3]]
    reduced.append(bands[3].reproject(proj).reduceResolution(ee.Reducer.mode(), maxPixels=1024))
    reduced.append(bands[4].reproject(proj).reduceResolution(ee.Reducer.mean(), maxPixels=1024))
    img = ee.Image.cat(reduced).toFloat()
    url = img.getDownloadURL({"crs": "EPSG:4326", "crs_transform": [t.a, t.b, t.c, t.d, t.e, t.f],
                              "dimensions": f"{w}x{h}", "format": "GEO_TIFF"})
    OUT.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=1800) as resp, open(OUT / f"{exp}.tif", "wb") as f:
        f.write(resp.read())
    print(exp, "done", flush=True)


def main():
    ee.Initialize(project=os.environ["GEE_PROJECT"])
    fires = sys.argv[1:] or (S.PAPER + [x for x in S.regions.SCALEUP_EXPERIMENT_IDS if not x.startswith("rp")])
    for exp in fires:
        if not (OUT / f"{exp}.tif").exists():
            export(exp)


if __name__ == "__main__":
    main()
