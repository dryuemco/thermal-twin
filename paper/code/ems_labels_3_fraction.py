"""Request 3 (R3): burned-fraction threshold.

f = in-window positive 30 m sub-pixels / non-nodata sub-pixels in the 17x17 block of the
frozen local mcd64a1_raw.tif. f is the share of the reconstructed cell covered by the
footprints of MODIS pixels flagged burned (the 30 m raster is a nearest-neighbour
duplication of ~463 m MCD64A1 pixels); it is not a sub-500 m burned fraction.
Rerun: burned := f >= 0.5, 0 < f < 0.5 dropped, f = 0 unburned; B = 2 and 10.
"""
import ems_labels_common as E
import numpy as np
import pandas as pd

res = {}
for reg in E.REGIONS:
    a = E.read_local(reg, "mcd64a1_raw.tif")
    pos = E.block_count((a > 0) & (a != E.NODATA))
    valid = E.block_count(a != E.NODATA)
    with np.errstate(invalid="ignore", divide="ignore"):
        frac = np.where(valid > 0, pos / valid, np.nan)
    d = E.tsg(reg)
    d["frac"] = E.cell_values(d, frac)
    d["n_valid_sub"] = E.cell_values(d, valid)
    chk = int(((d.frac > 0).astype(int) != d.burned).sum())
    fb = d.frac[d.burned == 1]
    info = {"tsg_cells": int(len(d)), "burned": int(d.burned.sum()),
            "label_rule_disagreements": chk,
            "cells_with_nodata_subpixels": int((d.n_valid_sub < 289).sum()),
            "burned_frac_quantiles": fb.quantile([0, .1, .25, .5, .75, .9, 1]).round(4).tolist(),
            "burned_frac_eq_1": int((fb == 1).sum()),
            "burned_ge_0.5": int((fb >= 0.5).sum()),
            "burned_lt_0.5_dropped": int((fb < 0.5).sum()),
            "distinct_frac_values_burned": int(fb.round(6).nunique())}
    E.log(reg, info)
    new = d[(d.frac == 0) | (d.frac >= 0.5)].copy()
    new["burned"] = (new.frac >= 0.5).astype(int)
    info["runs"] = {}
    for B in (2, 10):
        r0, r1 = E.within(d, B), E.within(new.reset_index(drop=True), B)
        info["runs"][f"B{B}"] = {"reference": r0, "frac_ge_50": r1}
        E.log("  ref  ", E.fmt_within(r0)); E.log("  f>=.5", E.fmt_within(r1))
    res[reg] = info
    E.dump(res, "r3_fraction.json")
E.log("done")
