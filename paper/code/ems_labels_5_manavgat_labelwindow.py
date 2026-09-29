"""Added analysis 5 (SPEC.md Addendum A; not requested): the frozen Manavgat label omits
every burn dated 28-31 July 2021 (DOY 209-212), because it predates the month-aligned
collection-query fix in repo/src/step6_validate_fire_relation.py. Rebuild the full
label window with the pipeline's own build_raw_burndate_image (validated route) and
measure what the correction does.

Usage: python ems_labels_5_manavgat_labelwindow.py <cache_dir>
"""
import sys
from pathlib import Path

import ems_labels_common as E
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

CACHE = Path(sys.argv[1]); CACHE.mkdir(parents=True, exist_ok=True)
REG = "manavgat_2021"
NUM9 = [f for f in E.C.THERMAL if f != "landcover_dominant"]
x = E.experiment(REG)
f = CACHE / f"{REG}_labelwin.npy"
if not f.exists():
    img = E.s6().build_raw_burndate_image(E.region_geometry(REG), x["label_start_date"],
                                          x["label_end_date"])
    np.save(f, E.fetch(img, REG, "BurnDate"))
a = np.load(f)
local = E.read_local(REG, "mcd64a1_raw.tif")
flag = E.any_positive(a)
full = E.C.load(REG)
full["burned_fix"] = E.cell_values(full, flag).astype(int)
tsg = (full.valid_for_modeling == True) & (full.burnable_tree_shrub_grass == True)  # noqa: E712
u, c = np.unique(a[(a > 0) & (local == 0)], return_counts=True)
res = {"window": [x["label_start_date"], x["label_end_date"]],
       "missing_subpixels_by_doy": dict(zip(u.tolist(), c.tolist())),
       "subpixels_frozen": int((local > 0).sum()), "subpixels_full_window": int((a > 0).sum()),
       "frozen_positive_not_in_ee": int(((local > 0) & (a <= 0)).sum()),
       "cells": {}}
for name, m in (("all", np.ones(len(full), bool)), ("valid_for_modeling", full.valid_for_modeling.to_numpy()),
                ("tsg", tsg.to_numpy())):
    s = full[m]
    res["cells"][name] = {"n": int(len(s)), "burned_frozen": int(s.burned.sum()),
                          "burned_full_window": int(s.burned_fix.sum()),
                          "gained": int(((s.burned == 0) & (s.burned_fix == 1)).sum()),
                          "lost": int(((s.burned == 1) & (s.burned_fix == 0)).sum())}
E.log(res)
d0 = full[tsg].reset_index(drop=True)
d1 = d0.copy(); d1["burned"] = d1["burned_fix"]
d0 = d0.drop(columns="burned_fix"); d1 = d1.drop(columns="burned_fix")

# signed univariate AUC, 10-cell block bootstrap
res["signed_auc"] = {}
for arm, d in (("frozen", d0), ("full_window", d1)):
    out = {}
    for feat in NUM9:
        s = d[d[feat].notna()]
        ci = E.block_bootstrap_ci(s.burned.to_numpy(), s[feat].to_numpy(),
                                  E.add_spatial_block_id(s, 10).to_numpy())
        out[feat] = {"auc": roc_auc_score(s.burned, s[feat]), "ci": ci["roc_auc_ci95"]}
    res["signed_auc"][arm] = out
    E.log(arm, {k: (round(v["auc"], 3), [round(z, 3) for z in v["ci"]]) for k, v in out.items()})
E.dump(res, "r5_manavgat_labelwindow.json")

res["within"] = {}
for B in (2, 10):
    r0, r1 = E.within(d0, B), E.within(d1, B)
    res["within"][f"B{B}"] = {"frozen": r0, "full_window": r1}
    E.log("  frozen", E.fmt_within(r0)); E.log("  fixed ", E.fmt_within(r1))
    E.dump(res, "r5_manavgat_labelwindow.json")

# transfer with corrected Manavgat, other regions unchanged
data = {r: (d1 if r == REG else E.tsg(r)) for r in E.REGIONS}
m = E.transfer_matrix(data)
m.to_csv(E.OUT / "r5_transfer_manavgat_full_window.csv", index=False)
summ = {"mean_baseline": float(m.baseline.mean()), "mean_thermal": float(m.thermal.mean()),
        "mean_delta": float(m.delta.mean())}
for B in (10, 2):
    s = m[f"support_B{B}"]
    summ[f"B{B}_positive"] = int((s == "positive_bootstrap_support").sum())
    summ[f"B{B}_negative"] = int((s == "negative_bootstrap_support").sum())
res["transfer_summary"] = summ
E.log(summ)
E.dump(res, "r5_manavgat_labelwindow.json")
E.log("done")
