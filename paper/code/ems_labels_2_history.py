"""Request 2 (R3): earlier-year fire screening, all five regions.

MCD64A1 (MODIS/061/MCD64A1, Earth Engine, read-only computePixels) over the five complete
calendar years before the event year, on each region's exact 30 m reference grid, clipped
to the pipeline's region geometry. A cell is flagged when >= 1 sub-pixel burned (the
pipeline's pre-label rule). The event-year gap [Y-01-01, predictor_start) is counted with
the pipeline's own build_raw_burndate_image, not modelled.

Reruns with the five-year cells removed from TSG (source and target alike):
  (a) within-region increment, B = 10 (reference + excluded)
  (b) 20-direction as-drawn transfer, baseline/thermal, paired delta (B = 10 and 2)
  (c) signed AUC of the absolute thermal channels on the 10 km collar and full frame

Usage: python ems_labels_2_history.py <cache_dir>
"""
import sys
from datetime import date, timedelta
from pathlib import Path

import ems_labels_common as E
import numpy as np
import pandas as pd
from scipy import ndimage
from sklearn.metrics import roc_auc_score

CACHE = Path(sys.argv[1]); CACHE.mkdir(parents=True, exist_ok=True)
SIGN_FEATS = ["current_lst_mean", "downscaled_lst_mean", "fused_lst_mean", "current_tvdi_mean"]
res = {"counts": {}, "within_B10": {}, "transfer": {}, "sign": {}}


def history_bits(reg, years):
    f = CACHE / f"{reg}_hist_{years[0]}_{years[-1]}.npy"
    if f.exists():
        return np.load(f)
    ee = E.ee_init()
    geom = E.region_geometry(reg)
    col = ee.ImageCollection("MODIS/061/MCD64A1").filterBounds(geom).select("BurnDate")
    acc = ee.Image.constant(0)
    for k, yr in enumerate(years):
        yc = col.filterDate(f"{yr}-01-01", f"{yr + 1}-01-01")
        b = yc.map(lambda i: i.gt(0).unmask(0)).max().unmask(0)
        acc = acc.add(b.multiply(2 ** k))
    img = acc.rename("bits").clip(geom)
    a = E.fetch(img, reg, "bits")
    np.save(f, a)
    return a


def gap_image(reg, x):
    ps = date.fromisoformat(x["predictor_start_date"])
    start, end = f"{ps.year}-01-01", (ps - timedelta(days=1)).isoformat()
    f = CACHE / f"{reg}_gap.npy"
    if not f.exists():
        img = E.s6().build_raw_burndate_image(E.region_geometry(reg), start, end)
        np.save(f, E.fetch(img, reg, "BurnDate"))
    return np.load(f), [start, end]


# --------------------------------------------------------------------------- counts
data_ref, data_exc = {}, {}
for reg in E.REGIONS:
    x = E.experiment(reg)
    Y = int(x["predictor_start_date"][:4])
    years = list(range(Y - 5, Y))
    bits = history_bits(reg, years)
    nod = bits == E.NODATA
    b0 = np.where(nod, 0, bits)
    flag_any = E.any_positive(np.where(nod, E.NODATA, (b0 > 0).astype("int16")))
    gap, gapwin = gap_image(reg, x)
    flag_gap = E.any_positive(gap)
    d = E.tsg(reg)
    full = E.C.load(reg, columns=["row_500m", "col_500m", "valid_for_modeling"])
    d["hist5"] = E.cell_values(d, flag_any).astype(bool)
    d["gap"] = E.cell_values(d, flag_gap).astype(bool)
    per_year = {}
    for k, yr in enumerate(years):
        fy = E.any_positive(np.where(nod, E.NODATA, ((b0 >> k) & 1).astype("int16")))
        per_year[yr] = {"cells_all": int(fy.sum()), "cells_tsg": int(E.cell_values(d, fy).sum())}
    c = {"years": years, "baseline_years_registered": x["baseline_years"],
         "per_year": per_year,
         "cells_all_grid": int(E.cell_values(full, flag_any).sum()),
         "cells_valid_for_modeling": int((E.cell_values(full, flag_any).astype(bool)
                                          & full.valid_for_modeling.to_numpy()).sum()),
         "cells_tsg": int(d.hist5.sum()), "tsg_total": int(len(d)),
         "tsg_hist5_and_label_burned": int((d.hist5 & (d.burned == 1)).sum()),
         "tsg_burned_total": int(d.burned.sum()),
         "event_year_gap_window": gapwin,
         "gap_cells_tsg": int(d.gap.sum()), "gap_cells_tsg_not_in_hist5": int((d.gap & ~d.hist5).sum())}
    res["counts"][reg] = c
    E.log(reg, c)
    d.loc[d.hist5 | d.gap, ["cell_id", "row_500m", "col_500m", "burned", "hist5", "gap"]].to_csv(
        E.OUT / f"r2_history_cells_{reg}.csv", index=False)
    data_ref[reg] = d.drop(columns=["hist5", "gap"])
    data_exc[reg] = d[~d.hist5].drop(columns=["hist5", "gap"]).reset_index(drop=True)
E.dump(res, "r2_history.json")

# --------------------------------------------------------------------------- (c) sign
def collar_dist(d):
    r0, c0 = int(d.row_500m.min()), int(d.col_500m.min())
    H, W = int(d.row_500m.max()) - r0 + 1, int(d.col_500m.max()) - c0 + 1
    rr, cc = d.row_500m.to_numpy().astype(int) - r0, d.col_500m.to_numpy().astype(int) - c0
    bg = np.ones((H, W), dtype=bool)
    b = d.burned.to_numpy() == 1
    bg[rr[b], cc[b]] = False
    return ndimage.distance_transform_edt(bg)[rr, cc] * E.CELL_KM


for arm, data in (("reference", data_ref), ("excluded", data_exc)):
    res["sign"][arm] = {}
    for reg in E.REGIONS:
        d = data[reg].copy()
        d["dist_km"] = collar_dist(d)
        out = {}
        for frame, sub in (("collar10", d[d.dist_km <= 10]), ("full", d)):
            for f in SIGN_FEATS:
                s = sub[sub[f].notna()]
                auc = roc_auc_score(s.burned, s[f])
                ci = E.block_bootstrap_ci(s.burned.to_numpy(), s[f].to_numpy(),
                                          E.add_spatial_block_id(s, 10).to_numpy())
                out[f"{frame}:{f}"] = {"auc": auc, "ci": ci["roc_auc_ci95"], "n": int(len(s))}
        res["sign"][arm][reg] = out
        E.log(arm, reg, {k: round(v["auc"], 3) for k, v in out.items()})
E.dump(res, "r2_history.json")

# --------------------------------------------------------------------------- (a) within
for reg in E.REGIONS:
    r0, r1 = E.within(data_ref[reg], 10), E.within(data_exc[reg], 10)
    res["within_B10"][reg] = {"reference": r0, "excluded": r1}
    E.log(reg); E.log("  ref ", E.fmt_within(r0)); E.log("  excl", E.fmt_within(r1))
    E.dump(res, "r2_history.json")

# --------------------------------------------------------------------------- (b) transfer
frozen = pd.read_csv(E.TREE / "paper" / "baseline_vs_thermal_transfer.csv")
for arm, data in (("reference", data_ref), ("excluded", data_exc)):
    E.log("transfer", arm)
    m = transfer_df = E.transfer_matrix(data)
    summ = {"mean_baseline": float(m.baseline.mean()), "mean_thermal": float(m.thermal.mean()),
            "mean_delta": float(m.delta.mean())}
    for B in (10, 2):
        s = m[f"support_B{B}"]
        summ[f"B{B}_positive"] = int((s == "positive_bootstrap_support").sum())
        summ[f"B{B}_negative"] = int((s == "negative_bootstrap_support").sum())
        summ[f"B{B}_uncertain"] = int((s == "uncertain_ci_overlaps_zero").sum())
    res["transfer"][arm] = {"summary": summ, "directions": m.to_dict(orient="records")}
    E.log(arm, summ)
    m.to_csv(E.OUT / f"r2_transfer_{arm}.csv", index=False)
    E.dump(res, "r2_history.json")
E.log("frozen columns:", list(frozen.columns))
E.log("done")
