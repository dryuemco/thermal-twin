"""Request 1 (R3): pre-label burn exclusion for Manavgat and Bejis.

The local label rasters are DOY-masked to the label window, so a pre-label burn is
recorded as 0 there. The pre-label raster the pipeline would have exported is rebuilt
from Earth Engine with the pipeline's own build_raw_burndate_image, on the exact 30 m
reference grid, after two validation gates (SPEC.md):
  V1  the label-window image reproduces local mcd64a1_raw.tif (Manavgat, Bejis)
  V2  the pre-label image reproduces local mcd64a1_prelabel_raw.tif and the recorded
      exclusion sets (Mugla 49, Evia 16, Montiferru 61)
Then counts the Manavgat/Bejis cells and, if any TSG cell is affected, reruns the
within-region comparison at B = 2 and 10.

Usage: python ems_labels_1_prelabel.py <cache_dir>
"""
import sys
from datetime import date, timedelta
from pathlib import Path

import ems_labels_common as E
import numpy as np
import pandas as pd

CACHE = Path(sys.argv[1]); CACHE.mkdir(parents=True, exist_ok=True)
res = {"validation": {}, "counts": {}, "reruns": {}}


def get(region, start, end, tag):
    f = CACHE / f"{region}_{tag}.npy"
    if f.exists():
        return np.load(f)
    img = E.s6().build_raw_burndate_image(E.region_geometry(region), start, end)
    a = E.fetch(img, region, "BurnDate")
    np.save(f, a)
    return a


def compare(a, b):
    both_nd = (a == E.NODATA) & (b == E.NODATA)
    mism = (a != b) & ~both_nd
    pos_a, pos_b = (a > 0), (b > 0)
    return {"pixels": int(a.size), "mismatch": int(mism.sum()),
            "positive_ee": int(pos_a.sum()), "positive_local": int(pos_b.sum()),
            "positive_agree": int((pos_a & pos_b).sum()),
            "nodata_ee": int((a == E.NODATA).sum()), "nodata_local": int((b == E.NODATA).sum())}


# ---- V1: label window reproduces the local label raster
for reg in ["manavgat_2021", "bejis_2022"]:
    x = E.experiment(reg)
    a = get(reg, x["label_start_date"], x["label_end_date"], "labelwin")
    c = compare(a, E.read_local(reg, "mcd64a1_raw.tif"))
    res["validation"][f"V1_{reg}"] = c
    E.log("V1", reg, c)

# ---- V2: pre-label window reproduces the local pre-label raster and exclusion sets
for reg in ["mugla_2021", "evia_2021_extended", "montiferru_2021"]:
    x = E.experiment(reg)
    w = x.get("pre_label_burn_window") or [x["predictor_start_date"], x["predictor_end_date"]]
    a = get(reg, w[0], w[1], "prelabel")
    c = compare(a, E.read_local(reg, "mcd64a1_prelabel_raw.tif"))
    flag = E.any_positive(a)
    d = E.C.load(reg, columns=["row_500m", "col_500m", "pre_label_burn_excluded"])
    mine = E.cell_values(d, flag).astype(bool)
    rec = d.pre_label_burn_excluded.to_numpy().astype(bool)
    c.update({"cells_flagged_ee": int(mine.sum()), "cells_recorded": int(rec.sum()),
              "cells_agree": int((mine & rec).sum()), "cells_disagree": int((mine != rec).sum())})
    res["validation"][f"V2_{reg}"] = c
    E.log("V2", reg, c)

# ---- burned label reproduced from local raster (cell rule check, used again in request 3)
for reg in E.REGIONS:
    d = E.C.load(reg, columns=["row_500m", "col_500m", "burned"])
    f = E.cell_values(d, E.any_positive(E.read_local(reg, "mcd64a1_raw.tif"))).astype(int)
    res["validation"][f"label_rule_{reg}"] = {"cells": int(len(d)),
                                             "disagree": int((f != d.burned.to_numpy()).sum())}
    E.log("label rule", reg, res["validation"][f"label_rule_{reg}"])

# ---- Request 1 proper
for reg in ["manavgat_2021", "bejis_2022"]:
    x = E.experiment(reg)
    w = x.get("pre_label_burn_window") or [x["predictor_start_date"], x["predictor_end_date"]]
    a = get(reg, w[0], w[1], "prelabel")
    flag = E.any_positive(a)
    d = E.C.load(reg)
    d["pre_label_ee"] = E.cell_values(d, flag).astype(bool)
    tsg = (d.valid_for_modeling == True) & (d.burnable_tree_shrub_grass == True)  # noqa: E712
    vals, cnt = np.unique(a[a > 0], return_counts=True)
    doy2iso = lambda v: (date(int(w[0][:4]), 1, 1) + timedelta(int(v) - 1)).isoformat()  # noqa: E731
    cnts = {
        "window": w,
        "positive_subpixels": int((a > 0).sum()),
        "positive_doys": {doy2iso(v): int(n) for v, n in zip(vals, cnt)},
        "cells_all": int(d.pre_label_ee.sum()),
        "cells_valid_for_modeling": int((d.pre_label_ee & d.valid_for_modeling).sum()),
        "cells_tsg": int((d.pre_label_ee & tsg).sum()),
        "cells_tsg_also_label_burned": int((d.pre_label_ee & tsg & (d.burned == 1)).sum()),
    }
    res["counts"][reg] = cnts
    E.log("R1", reg, cnts)
    d.loc[d.pre_label_ee, ["cell_id", "row_500m", "col_500m", "burned", "valid_for_modeling",
                           "burnable_tree_shrub_grass"]].to_csv(
        E.OUT / f"r1_prelabel_cells_{reg}.csv", index=False)
    if cnts["cells_tsg"] > 0:
        base = d[tsg].reset_index(drop=True)
        excl = d[tsg & ~d.pre_label_ee].reset_index(drop=True)
        res["reruns"][reg] = {}
        for B in (2, 10):
            r0, r1 = E.within(base, B), E.within(excl, B)
            res["reruns"][reg][f"B{B}"] = {"reference": r0, "excluded": r1}
            E.log("  ref ", E.fmt_within(r0)); E.log("  excl", E.fmt_within(r1))

E.dump(res, "r1_prelabel.json")
E.log("wrote r1_prelabel.json")
