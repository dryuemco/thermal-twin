"""yearly_burn_export.py: share of each 500 m cell burned in each calendar year 2013-2026 (MCD64A1 v061, BurnDate > 0,
one band per year, the last year up to the last published month), on each fire's grid. For label counts before
amendment 11 (past events and later burning); no model is scored.
Writes $THERMAL_TWIN_SCALEUP/analysis/yearly/<fire>.tif
"""
import os
import sys
import urllib.request
from pathlib import Path

import ee
import rasterio

sys.path.insert(0, str(Path(__file__).resolve().parent))
import s2_label_check_export as S  # noqa: E402

OUT = S.SCALEUP / "analysis" / "yearly"
MCD = "MODIS/061/MCD64A1"
YEARS = list(range(2013, 2027))


def export(exp):
    with rasterio.open(S.grid_path(exp)) as g:
        t, (h, w) = g.transform, g.shape
    proj = ee.ImageCollection(MCD).first().projection()
    bands = []
    for y in YEARS:
        b = ee.ImageCollection(MCD).filterDate(f"{y}-01-01", f"{y + 1}-01-01").map(
            lambda im: im.select("BurnDate").gt(0).unmask(0)).max().unmask(0)
        bands.append(b.reproject(proj).reduceResolution(ee.Reducer.mean(), maxPixels=1024).rename(f"y{y}"))
    img = ee.Image.cat(bands).toFloat()
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
