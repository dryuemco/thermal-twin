"""multiyear_label_export.py: MCD64A1 burned shares for claim 6 (plan amendment 2) on each fire's 500 m grid.

  band 1  share of the cell burned at least once 2001-2023
  band 2  share burned at least once from 2001 to the year before the fire (history only)
  band 3  share burned inside the fire's own label window (check against the step8a label)
MODIS/061/MCD64A1, BurnDate > 0, native 500 m sinusoidal product aggregated by area mean.
Writes $THERMAL_TWIN_SCALEUP/analysis/multiyear/<fire>.tif
"""
import os
import sys
import urllib.request
from datetime import date
from pathlib import Path

import ee
import rasterio

sys.path.insert(0, str(Path(__file__).resolve().parent))
import s2_label_check_export as S  # noqa: E402  (grid_path, regions)

OUT = S.SCALEUP / "analysis" / "multiyear"
OUT.mkdir(parents=True, exist_ok=True)
MCD = "MODIS/061/MCD64A1"


def ever(start, end):
    col = ee.ImageCollection(MCD).filterDate(start, end)
    return col.map(lambda im: im.select("BurnDate").gt(0)).max().unmask(0)


def export(exp):
    e = S.regions.EXPERIMENTS[exp]
    ls, le = e["label_start_date"], e["label_end_date"]
    year = int(ls[:4])
    with rasterio.open(S.grid_path(exp)) as g:
        t, (h, w) = g.transform, g.shape
    proj = ee.ImageCollection(MCD).first().projection()
    d0, d1 = date.fromisoformat(ls), date.fromisoformat(le)
    win = ee.ImageCollection(MCD).filterDate(f"{year}-{d0.month:02d}-01", f"{year}-{d1.month:02d}-28").map(
        lambda im: im.select("BurnDate").gte(d0.timetuple().tm_yday).And(im.select("BurnDate").lte(d1.timetuple().tm_yday))
    ).max().unmask(0)
    bands = [ever("2001-01-01", "2024-01-01"), ever("2001-01-01", f"{year}-01-01"), win]
    img = ee.Image.cat([b.reproject(proj).reduceResolution(ee.Reducer.mean(), maxPixels=1024) for b in bands]).toFloat()
    url = img.getDownloadURL({"crs": "EPSG:4326", "crs_transform": [t.a, t.b, t.c, t.d, t.e, t.f],
                              "dimensions": f"{w}x{h}", "format": "GEO_TIFF"})
    with urllib.request.urlopen(url, timeout=1800) as resp, open(OUT / f"{exp}.tif", "wb") as f:
        f.write(resp.read())
    print(exp, "done", flush=True)


OUTP = S.SCALEUP / "analysis" / "multiyear_prospective"


def export_prospective(exp):
    """Amendment 5: share of the cell burned at least once from the first day of the label window to the end of
    2023, so that no burn before the predictor window enters the label (one band)."""
    e = S.regions.EXPERIMENTS[exp]
    with rasterio.open(S.grid_path(exp)) as g:
        t, (h, w) = g.transform, g.shape
    proj = ee.ImageCollection(MCD).first().projection()
    img = ever(e["label_start_date"], "2024-01-01").reproject(proj).reduceResolution(ee.Reducer.mean(), maxPixels=1024).toFloat()
    url = img.getDownloadURL({"crs": "EPSG:4326", "crs_transform": [t.a, t.b, t.c, t.d, t.e, t.f],
                              "dimensions": f"{w}x{h}", "format": "GEO_TIFF"})
    OUTP.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=1800) as resp, open(OUTP / f"{exp}.tif", "wb") as f:
        f.write(resp.read())
    print(exp, "prospective done", flush=True)


def main():
    ee.Initialize(project=os.environ["GEE_PROJECT"])
    args = [a for a in sys.argv[1:] if a != "--prospective"]
    prospective = "--prospective" in sys.argv[1:]
    fires = args or (S.PAPER + [x for x in S.regions.SCALEUP_EXPERIMENT_IDS if not x.startswith("rp")])
    for exp in fires:
        if prospective:
            if not (OUTP / f"{exp}.tif").exists():
                export_prospective(exp)
        elif not (OUT / f"{exp}.tif").exists():
            export(exp)


if __name__ == "__main__":
    main()
