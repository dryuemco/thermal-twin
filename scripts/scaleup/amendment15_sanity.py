"""Re-export one original future label to temporary scratch and compare every band.

THERMAL_TWIN_LABEL_SUFFIX must be unset or empty for this bit-0 check.
Run python amendment15_sanity.py <fire> with GEE_PROJECT and THERMAL_TWIN_SCALEUP set.
"""
import argparse
import os
from pathlib import Path
from tempfile import TemporaryDirectory

from label_variant import SUFFIX


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fire")
    args = parser.parse_args()
    if SUFFIX:
        parser.error("unset THERMAL_TWIN_LABEL_SUFFIX for the original bit-0 check")

    import ee
    import numpy as np
    import rasterio

    import future_label_export as future

    if args.fire not in future.S.regions.EXPERIMENTS:
        parser.error(f"unknown fire: {args.fire}")
    filename = f"{args.fire}.tif"
    with rasterio.open(future.OUT / filename) as stored, TemporaryDirectory(prefix="amendment15-") as scratch:
        ee.Initialize(project=os.environ["GEE_PROJECT"])
        future.export(args.fire, out=Path(scratch), qa_mask=1)
        with rasterio.open(Path(scratch) / filename) as exported:
            if (stored.shape, stored.count, stored.crs, stored.transform) != (
                exported.shape, exported.count, exported.crs, exported.transform
            ):
                raise SystemExit("The stored and scratch raster grids or band counts differ")
            matches = True
            for band in stored.indexes:
                old = stored.read(band).astype(np.float64)
                new = exported.read(band).astype(np.float64)
                equal = (old == new) | (np.isnan(old) & np.isnan(new))
                diff = np.zeros_like(old)
                diff[~equal] = np.abs(old[~equal] - new[~equal])
                maximum = np.nan_to_num(diff, nan=np.inf, posinf=np.inf).max()
                print(f"Band {band}: max absolute difference = {maximum:g}")
                matches &= bool(equal.all())
    if not matches:
        raise SystemExit("The scratch raster differs from the stored original")


if __name__ == "__main__":
    main()
