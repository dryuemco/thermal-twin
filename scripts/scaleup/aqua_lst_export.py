"""aqua_lst_export.py: afternoon land surface temperature for claim 5 of docs/scaleup/ANALYSIS_PLAN.md.

MODIS/061/MYD11A1 (Aqua, overpass about 13:30), LST_Day_1km, the pipeline's QC rule (QC_Day bits 0-1 == 0
and bits 2-3 == 0, LST > 0), mean in degrees C over the fire's predictor window, pixels with fewer than
3 accepted days set to NaN; written on the fire's 500 m step8a grid.
  band 1  mean afternoon LST (C)      band 2  number of accepted days
Writes $THERMAL_TWIN_SCALEUP/analysis/aqua_lst/<fire>.tif
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

OUT = S.SCALEUP / "analysis" / "aqua_lst"
OUT.mkdir(parents=True, exist_ok=True)


def accepted(im):
    qc = im.select("QC_Day")
    ok = qc.bitwiseAnd(3).eq(0).And(qc.rightShift(2).bitwiseAnd(3).eq(0)).And(im.select("LST_Day_1km").gt(0))
    return im.select("LST_Day_1km").multiply(0.02).subtract(273.15).updateMask(ok)


def export(exp):
    e = S.regions.EXPERIMENTS[exp]
    ps, pe = e["predictor_start_date"], e["predictor_end_date"]
    end = (date.fromisoformat(pe) + timedelta(days=1)).isoformat()
    with rasterio.open(S.grid_path(exp)) as g:
        t, (h, w) = g.transform, g.shape
    col = ee.ImageCollection("MODIS/061/MYD11A1").filterDate(ps, end).map(accepted)
    n = col.count()
    img = ee.Image.cat([col.mean().updateMask(n.gte(3)), n]).toFloat()
    url = img.getDownloadURL({"crs": "EPSG:4326", "crs_transform": [t.a, t.b, t.c, t.d, t.e, t.f],
                              "dimensions": f"{w}x{h}", "format": "GEO_TIFF"})
    with urllib.request.urlopen(url, timeout=1800) as resp, open(OUT / f"{exp}.tif", "wb") as f:
        f.write(resp.read())
    print(exp, "done", flush=True)


def main():
    ee.Initialize(project=os.environ.get("GEE_PROJECT", "thermaltwin"))
    fires = sys.argv[1:] or (S.PAPER + [x for x in S.regions.SCALEUP_EXPERIMENT_IDS if not x.startswith("rp")])
    for exp in fires:
        if not (OUT / f"{exp}.tif").exists():
            export(exp)


if __name__ == "__main__":
    main()
