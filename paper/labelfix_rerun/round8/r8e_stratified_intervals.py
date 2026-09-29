"""R8e. Spatial-block bootstrap intervals for the stratified associations of Table S27
(reviewer 2, M9).

The point values are those of round7/r7b_lst_given_terrain.csv and code/matched_frame_gap.csv:
signed AUC of current LST (and NDVI) against burned, raw, within deciles of a second variable
(pairs pooled, weighted by the number of burned-unburned pairs), and after removing the region's
linear dependence of LST on elevation. Intervals: 10-cell spatial blocks resampled with
replacement, 1000 replicates, seed 42; replicates with one class are dropped. The detrending slope
is fitted once on the full region, as in round 7.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import ndimage
from sklearn.metrics import roc_auc_score

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "paper" / "code"))
import _canonical  # noqa: E402

REG = ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended", "montiferru_2021"]
CELL_KM, B, R, SEED = 0.45, 10, 1000, 42


def load(r):
    d = _canonical.load(r)
    d = d[(d.valid_for_modeling == True) & (d.burnable_tree_shrub_grass == True)].reset_index(drop=True)  # noqa: E712
    r0, c0 = int(d.row_500m.min()), int(d.col_500m.min())
    H, W = int(d.row_500m.max()) - r0 + 1, int(d.col_500m.max()) - c0 + 1
    rr, cc = d.row_500m.to_numpy().astype(int) - r0, d.col_500m.to_numpy().astype(int) - c0
    bg = np.ones((H, W), dtype=bool)
    b = d.burned.to_numpy() == 1
    bg[rr[b], cc[b]] = False
    d["dist_km"] = ndimage.distance_transform_edt(bg)[rr, cc] * CELL_KM
    return d


def strat(s, feat, by, nbin=10):
    s = s[[feat, by, "burned"]].dropna()
    if s.burned.nunique() < 2:
        return np.nan
    try:
        s = s.assign(bin=pd.qcut(s[by], nbin, labels=False, duplicates="drop"))
    except ValueError:
        return np.nan
    num = den = 0.0
    for _, g in s.groupby("bin"):
        if g.burned.nunique() < 2:
            continue
        w = (g.burned == 1).sum() * (g.burned == 0).sum()
        num += roc_auc_score(g.burned, g[feat]) * w
        den += w
    return num / den if den else np.nan


def auc(s, feat):
    s = s[[feat, "burned"]].dropna()
    return roc_auc_score(s.burned, s[feat]) if s.burned.nunique() == 2 else np.nan


STATS = {
    "lst_raw": lambda s: auc(s, "current_lst_mean"),
    "lst_within_elevation": lambda s: strat(s, "current_lst_mean", "elevation_mean"),
    "lst_detrended_on_elevation": lambda s: auc(s, "lst_detrended"),
    "lst_within_ndvi": lambda s: strat(s, "current_lst_mean", "ndvi_mean"),
    "lst_within_distance": lambda s: strat(s, "current_lst_mean", "dist_km"),
    "ndvi_raw": lambda s: auc(s, "ndvi_mean"),
    "ndvi_within_lst": lambda s: strat(s, "ndvi_mean", "current_lst_mean"),
}

rows = []
rng = np.random.default_rng(SEED)
for r in REG:
    d = load(r)
    ok = d.current_lst_mean.notna() & d.elevation_mean.notna()
    slope, icpt = np.polyfit(d.elevation_mean[ok], d.current_lst_mean[ok], 1)
    d["lst_detrended"] = d.current_lst_mean - (slope * d.elevation_mean + icpt)
    for frame, sub in (("full", d), ("10km", d[d.dist_km <= 10].reset_index(drop=True))):
        blk = (sub.row_500m // B).astype(str) + "_" + (sub.col_500m // B).astype(str)
        groups = [np.flatnonzero(blk.to_numpy() == g) for g in blk.unique()]
        point = {k: f(sub) for k, f in STATS.items()}
        reps = {k: [] for k in STATS}
        for _ in range(R):
            idx = np.concatenate([groups[i] for i in rng.integers(0, len(groups), len(groups))])
            bs = sub.iloc[idx]
            if bs.burned.nunique() < 2:
                continue
            for k, f in STATS.items():
                reps[k].append(f(bs))
        for k in STATS:
            v = np.array([x for x in reps[k] if not np.isnan(x)])
            lo, hi = np.percentile(v, [2.5, 97.5])
            rows.append({"region": r, "frame": frame, "statistic": k, "auc": point[k],
                         "ci_low": lo, "ci_high": hi, "excludes_0.5": bool(lo > 0.5 or hi < 0.5),
                         "n_blocks": len(groups), "n_valid_reps": int(len(v))})
        print(r, frame, {k: round(point[k], 3) for k in STATS}, flush=True)

T = pd.DataFrame(rows)
T.to_csv(HERE / "r8e_stratified_intervals.csv", index=False)
chk = pd.read_csv(ROOT / "paper/labelfix_rerun/round7/r7b_lst_given_terrain.csv")
diffs = []
for _, c in chk.iterrows():
    for k in ("lst_raw", "lst_within_elevation", "lst_detrended_on_elevation"):
        v = T[(T.region == c.region) & (T.frame == c.frame) & (T.statistic == k)].auc.iloc[0]
        diffs.append(abs(v - c[k]))
json.dump({"max_abs_diff_vs_round7_r7b": float(max(diffs)), "replicates": R, "block_cells": B, "seed": SEED},
          open(HERE / "r8e_summary.json", "w"), indent=1)
print("max diff vs r7b", max(diffs))
