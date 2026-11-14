"""s2_label_check_export.py: Sentinel-2 dNBR reference for claim 3 of docs/scaleup/ANALYSIS_PLAN.md.

For every fire of the primary set, on the fire's own 500 m step8a grid (step8a_500m_grid_burned_label.tif):
  band 1  share of valid 20 m Sentinel-2 pixels with dNBR >= 0.10 (Key and Benson 2006, lower bound of low severity)
  band 2  share with dNBR >= 0.27 (sensitivity threshold)
  band 3  share of 20 m pixels with a valid dNBR
  band 4  FireCCI51 burned share (250 m, burn date inside the label window, confidence >= 50), -1 where
          the product does not cover the year
Fixed rules (plan, claim 3): COPERNICUS/S2_SR_HARMONIZED, SCL classes 0, 1, 3, 8, 9, 10, 11 masked,
pre = median NBR over the predictor window, post = median NBR over the 30 days after label_end, or over
60 days where a pixel has fewer than 3 valid observations in 30; NBR = (B8 - B12) / (B8 + B12).

Writes D:/ThermalTwin/scaleup/analysis/s2/<fire>.tif and <fire>.json (image counts).
Run:  <venv-step10>/python s2_label_check_export.py [fire ...]
"""
import json
import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
from pathlib import Path

import ee
import numpy as np
import rasterio
import rasterio.io  # noqa: F401  (MemoryFile)

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from core import regions  # noqa: E402

SCALEUP = Path("D:/ThermalTwin/scaleup")
PAPER_OUT = REPO / "outputs" / "experiments"
OUT = SCALEUP / "analysis" / "s2"
OUT.mkdir(parents=True, exist_ok=True)
PAPER = ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended"]
MASK_SCL = (0, 1, 3, 8, 9, 10, 11)
TILE, WORKERS = 24, 12          # 24 x 24 cells (about 12 km) per request, 12 requests at a time


def grid_path(exp):
    if exp in PAPER:
        return PAPER_OUT / exp / "step8a" / "step8a_500m_grid_burned_label.tif"
    hits = list(SCALEUP.glob(f"w*/outputs/experiments/{exp}/step8a/step8a_500m_grid_burned_label.tif"))
    assert len(hits) == 1, (exp, hits)
    return hits[0]


def nbr(img):
    scl = img.select("SCL")
    m = scl.neq(MASK_SCL[0])
    for c in MASK_SCL[1:]:
        m = m.And(scl.neq(c))
    return img.normalizedDifference(["B8", "B12"]).rename("nbr").updateMask(m)


def export(exp):
    e = regions.EXPERIMENTS[exp]
    ps, pe = e["predictor_start_date"], e["predictor_end_date"]
    ls, le = e["label_start_date"], e["label_end_date"]
    with rasterio.open(grid_path(exp)) as g:
        t, (h, w) = g.transform, g.shape
    west, north = t.c, t.f
    east, south = west + t.a * w, north + t.e * h
    aoi = ee.Geometry.Rectangle([west, south, east, north], "EPSG:4326", False)
    col = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterBounds(aoi)
    d_le = date.fromisoformat(le)
    end30 = (d_le + timedelta(days=31)).isoformat()
    end60 = (d_le + timedelta(days=61)).isoformat()
    after = (d_le + timedelta(days=1)).isoformat()
    pre_c = col.filterDate(ps, (date.fromisoformat(pe) + timedelta(days=1)).isoformat()).map(nbr)
    p30 = col.filterDate(after, end30).map(nbr)
    p60 = col.filterDate(after, end60).map(nbr)
    post = p30.median().where(p30.count().lt(3), p60.median())
    dnbr = pre_c.median().subtract(post)
    valid = dnbr.mask().reduce(ee.Reducer.min()).rename("valid")
    b10 = dnbr.gte(0.10).rename("b10")
    b27 = dnbr.gte(0.27).rename("b27")
    p20 = col.first().select("B12").projection()
    native = ee.Image.cat([b10, b27]).reproject(p20)
    frac = native.reduceResolution(ee.Reducer.mean(), maxPixels=4096)
    vfrac = valid.unmask(0).reproject(p20).reduceResolution(ee.Reducer.mean(), maxPixels=4096)
    year = int(ls[:4])
    cci = ee.ImageCollection("ESA/CCI/FireCCI/5_1").filterDate(f"{year}-01-01", f"{year + 1}-01-01")
    n_cci = cci.size().getInfo()
    if n_cci:
        doy_lo = date.fromisoformat(ls).timetuple().tm_yday
        doy_hi = d_le.timetuple().tm_yday
        cci_b = cci.map(lambda im: im.select("BurnDate").gte(doy_lo).And(im.select("BurnDate").lte(doy_hi))
                        .And(im.select("ConfidenceLevel").gte(50))).max().unmask(0)
        cci_frac = cci_b.reproject(cci.first().projection()).reduceResolution(ee.Reducer.mean(), maxPixels=4096).rename("cci")
    else:
        cci_frac = ee.Image.constant(-1).rename("cci")   # product does not cover the year
    img = ee.Image.cat([frac.select("b10"), frac.select("b27"), vfrac, cci_frac]).toFloat()
    # one whole-grid request did not finish in 45 minutes, so the grid is fetched in tiles, in parallel
    tiles = [(r0, c0, min(TILE, h - r0), min(TILE, w - c0)) for r0 in range(0, h, TILE) for c0 in range(0, w, TILE)]

    def fetch(tile):
        r0, c0, th, tw = tile
        url = img.getDownloadURL({"crs": "EPSG:4326",
                                  "crs_transform": [t.a, t.b, t.c + c0 * t.a, t.d, t.e, t.f + r0 * t.e],
                                  "dimensions": f"{tw}x{th}", "format": "GEO_TIFF"})
        for attempt in range(4):
            try:
                with urllib.request.urlopen(url, timeout=900) as resp:
                    data = resp.read()
                with rasterio.MemoryFile(data) as mf, mf.open() as src:
                    return tile, src.read()
            except Exception as exc:  # noqa: BLE001
                if attempt == 3:
                    raise
                print(f"  {exp} tile {tile} retry after {type(exc).__name__}", flush=True)
                time.sleep(30)

    full = np.full((4, h, w), np.nan, np.float32)
    with ThreadPoolExecutor(WORKERS) as pool:
        for (r0, c0, th, tw), arr in pool.map(fetch, tiles):
            full[:, r0:r0 + th, c0:c0 + tw] = arr
    dst = OUT / f"{exp}.tif"
    with rasterio.open(dst, "w", driver="GTiff", height=h, width=w, count=4, dtype="float32", crs="EPSG:4326",
                       transform=t, nodata=np.nan) as out:
        out.write(full)
        out.descriptions = ("s2_burned_share_dnbr010", "s2_burned_share_dnbr027", "s2_valid_share", "firecci51_burned_share")
    info = {"experiment": exp, "predictor_window": [ps, pe], "label_window": [ls, le],
            "pre_images": pre_c.size().getInfo(), "post30_images": p30.size().getInfo(), "post60_images": p60.size().getInfo(),
            "firecci51_images": n_cci, "grid": [h, w]}
    (OUT / f"{exp}.json").write_text(json.dumps(info, indent=1), encoding="utf-8")
    print(exp, info, flush=True)


def main():
    ee.Initialize(project=os.environ.get("GEE_PROJECT", "thermaltwin"))
    fires = sys.argv[1:] or (PAPER + [x for x in regions.SCALEUP_EXPERIMENT_IDS if not x.startswith("rp")])
    for exp in fires:
        if (OUT / f"{exp}.tif").exists():
            print(exp, "exists, skipped", flush=True)
            continue
        export(exp)


if __name__ == "__main__":
    main()
