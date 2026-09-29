"""Arm B guard: the regenerated MODIS must carry nodata -9999 (the screened chain), and is compared pixel by pixel
with the screened raster left by the 2026-08-14 run in repo/outputs (read-only). Usage: qc_check_screened.py <new_dir> <old_dir>"""
import sys, numpy as np, rasterio
from pathlib import Path
new, old = Path(sys.argv[1]), Path(sys.argv[2]); ok = True
for f in ("modis_lst_mean_celsius.tif", "modis_lst_std_celsius.tif", "modis_valid_observation_count.tif"):
    with rasterio.open(new / f) as a, rasterio.open(old / f) as b:
        x, y = a.read(1), b.read(1)
        same = a.profile["transform"] == b.profile["transform"] and x.shape == y.shape and np.array_equal(x, y, equal_nan=True)
        print(f, "nodata new", a.nodata, "| pixel-identical to 2026-08-14 screened raster:", same)
        if f != "modis_valid_observation_count.tif" and a.nodata != -9999: ok = False
sys.exit(0 if ok else 1)
