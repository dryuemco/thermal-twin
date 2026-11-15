"""data_audit.py: checkpoint 1 of plan amendment 13 (TMA data audit). Reads only collection metadata and composite
dates on Earth Engine; no label of any site is read and no model is fitted.

For each product: Earth Engine id and version, first and last image, image count. For MOD13A1 / MYD13A1 (16-day):
for each year 2001-2026 the composites whose whole observation interval (start to start + 15 days) lies inside the
predictor window (the 58 days before 1 May), and a pixel-level check on a sample box that the DayOfYear band never
exceeds the interval end. For MOD11A1 / MYD11A1 (daily): the number of days available in each year's window.
Writes data_audit.json and data_audit.md in $THERMAL_TWIN_SCALEUP/analysis/tma.
"""
import json
import os
from datetime import date, timedelta
from pathlib import Path

import ee

OUT = Path(os.environ["THERMAL_TWIN_SCALEUP"]) / "analysis" / "tma"
PRODUCTS = {"MOD13A1": "MODIS/061/MOD13A1", "MYD13A1": "MODIS/061/MYD13A1", "MOD11A1": "MODIS/061/MOD11A1",
            "MYD11A1": "MODIS/061/MYD11A1", "MCD64A1": "MODIS/061/MCD64A1", "DEM": "COPERNICUS/DEM/GLO30"}
YEARS = range(2001, 2027)


def window(y):
    cut = date(y, 5, 1)
    return cut - timedelta(days=58), cut                      # [start, cut) : 58 days ending 30 April


def main():
    ee.Initialize(project=os.environ["GEE_PROJECT"])
    OUT.mkdir(parents=True, exist_ok=True)
    box = ee.Geometry.BBox(-8.0, 40.0, -7.5, 40.5)            # sample box (central Portugal) for the pixel check
    S = {"products": {}, "mod13_windows": {}, "mod11_days": {}}
    for k, cid in PRODUCTS.items():
        c = ee.ImageCollection(cid)
        S["products"][k] = {"id": cid, "first": ee.Date(c.aggregate_min("system:time_start")).format("YYYY-MM-dd").getInfo(),
                            "last": ee.Date(c.aggregate_max("system:time_start")).format("YYYY-MM-dd").getInfo(),
                            "images": c.size().getInfo()}
        print(k, S["products"][k], flush=True)
    for k in ("MOD13A1", "MYD13A1"):
        c = ee.ImageCollection(PRODUCTS[k])
        per = {}
        for y in YEARS:
            w0, cut = window(y)
            starts = c.filterDate((w0 - timedelta(days=20)).isoformat(), cut.isoformat()).aggregate_array("system:time_start").getInfo()
            used, rejected = [], []
            for ms in starts:
                s = date(1970, 1, 1) + timedelta(milliseconds=ms)
                e = s + timedelta(days=15)
                (used if (s >= w0 and e < cut) else rejected).append(f"{s}..{e}")
            chk = None
            if used:
                s0 = date.fromisoformat(used[-1].split("..")[0])
                im = c.filterDate(s0.isoformat(), (s0 + timedelta(days=1)).isoformat()).first().select("DayOfYear")
                mx = im.reduceRegion(ee.Reducer.max(), box, 500, maxPixels=1e8).get("DayOfYear").getInfo()
                end_doy = (s0 + timedelta(days=15)).timetuple().tm_yday
                chk = {"last_used_composite": used[-1], "max_DayOfYear": mx, "interval_end_doy": end_doy,
                       "ok": mx is None or mx <= end_doy}
            per[y] = {"used": used, "rejected": rejected, "pixel_check": chk}
        S["mod13_windows"][k] = per
        print(k, "windows done", flush=True)
    for k in ("MOD11A1", "MYD11A1"):
        c = ee.ImageCollection(PRODUCTS[k])
        S["mod11_days"][k] = {y: c.filterDate(window(y)[0].isoformat(), window(y)[1].isoformat()).size().getInfo() for y in YEARS}
        print(k, "days done", flush=True)
    (OUT / "data_audit.json").write_text(json.dumps(S, indent=1, default=str), encoding="utf-8")
    L = ["# TMA data audit (checkpoint 1)", "", "| Product | Earth Engine id | First | Last | Images |", "|---|---|---|---|---|"]
    L += [f"| {k} | {v['id']} | {v['first']} | {v['last']} | {v['images']} |" for k, v in S["products"].items()]
    L += ["", "MOD13A1 composites fully inside the 58-day window before 1 May (per year): "
          + ", ".join(f"{y}: {len(v['used'])}" for y, v in S["mod13_windows"]["MOD13A1"].items()),
          "", "Pixel check failures: " + str([y for k in S["mod13_windows"] for y, v in S["mod13_windows"][k].items()
                                               if v["pixel_check"] and not v["pixel_check"]["ok"]]),
          "", "MOD11A1 days per window: " + ", ".join(f"{y}: {n}" for y, n in S["mod11_days"]["MOD11A1"].items()),
          "", "MYD11A1 days per window: " + ", ".join(f"{y}: {n}" for y, n in S["mod11_days"]["MYD11A1"].items())]
    (OUT / "data_audit.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
