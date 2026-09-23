"""
What the QC screening does downstream, arm A (unscreened) against arm B
(screened), for Manavgat.

The quantity that matters for the companion paper's limitation (viii) is NOT
the within-region increment but the SIGNED univariate AUC of each predictor
against burning, because the paper's mechanism is a reversal in that sign and
the screening's induced change is elevation-correlated at +0.615. If screening
moves elevation's signed AUC materially, an elevation-correlated preprocessing
artefact is a live competing explanation for the reversal. If it does not, that
candidate is closed.

Signed AUC is never folded to max(AUC, 1-AUC), matching the pipeline.
Intervals are 10-cell (~5 km) spatial-block bootstraps, 1000 replicates,
seed 42 -- the same construction the paper uses.

Read-only with respect to the repository; writes only its own report.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

W = Path("C:/Users/CORSAIR/projects/thermal-twin/refreeze/_qc_work/manavgat_2021")  # refreeze copy: corrected label
FEATURES = [
    "elevation_mean", "slope_mean", "ndvi_mean",
    "lst_anomaly_mean", "current_lst_mean", "current_tvdi_mean",
    "tvdi_difference_mean", "downscaled_lst_mean", "fused_lst_mean",
]
POP = "burnable_tree_shrub_grass"
BLOCK = 10
N_BOOT = 1000
SEED = 42


def load(arm):
    df = pd.read_parquet(W / arm / "step8a" / "step8a_500m_modeling_dataset.parquet")
    df = df[df["valid_for_modeling"] == True]  # noqa: E712
    if POP in df.columns:
        df = df[df[POP] == True]  # noqa: E712
    return df.reset_index(drop=True)


def signed_auc(y, x):
    ok = np.isfinite(x)
    if ok.sum() < 10 or len(np.unique(y[ok])) < 2:
        return np.nan
    return roc_auc_score(y[ok], x[ok])


def block_boot(df, feat):
    y = df["burned"].to_numpy().astype(int)
    x = df[feat].to_numpy().astype(float)
    blk = (df["row_500m"] // BLOCK).astype(str) + "_" + (df["col_500m"] // BLOCK).astype(str)
    blocks = blk.to_numpy()
    uniq = np.unique(blocks)
    idx_by_block = {b: np.where(blocks == b)[0] for b in uniq}
    rng = np.random.default_rng(SEED)
    out = []
    for _ in range(N_BOOT):
        pick = rng.choice(uniq, size=len(uniq), replace=True)
        idx = np.concatenate([idx_by_block[b] for b in pick])
        v = signed_auc(y[idx], x[idx])
        if np.isfinite(v):
            out.append(v)
    if not out:
        return (np.nan, np.nan)
    return (float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5)))


report = {}
arms = {}
for arm in ("armA", "armB"):
    df = load(arm)
    arms[arm] = df
    blk = (df["row_500m"] // BLOCK).astype(str) + "_" + (df["col_500m"] // BLOCK).astype(str)
    report[arm] = {
        "cells": int(len(df)),
        "burned": int(df["burned"].sum()),
        "positive_carrying_blocks_5km": int(blk[df["burned"] == 1].nunique()),
        "features": {},
    }
    for f in FEATURES:
        if f not in df.columns:
            report[arm]["features"][f] = {"status": "absent"}
            continue
        y = df["burned"].to_numpy().astype(int)
        pt = signed_auc(y, df[f].to_numpy().astype(float))
        lo, hi = block_boot(df, f)
        report[arm]["features"][f] = {"auc": pt, "ci": [lo, hi],
                                      "nan_fraction": float(df[f].isna().mean())}

print(f"{'':24s}  {'ARM A (unscreened)':>28s}   {'ARM B (screened)':>28s}   {'shift':>8s}")
print(f"{'population':24s}  {report['armA']['cells']:12d} cells {report['armA']['burned']:6d} burned"
      f"   {report['armB']['cells']:12d} cells {report['armB']['burned']:6d} burned")
print(f"{'5km pos-carrying blocks':24s}  {report['armA']['positive_carrying_blocks_5km']:28d}"
      f"   {report['armB']['positive_carrying_blocks_5km']:28d}")
print("-" * 100)
for f in FEATURES:
    a = report["armA"]["features"][f]
    b = report["armB"]["features"][f]
    if a.get("status") == "absent" or b.get("status") == "absent":
        print(f"{f:24s}  {'ABSENT':>28s}")
        continue
    sa = f"{a['auc']:.3f} [{a['ci'][0]:.3f},{a['ci'][1]:.3f}]"
    sb = f"{b['auc']:.3f} [{b['ci'][0]:.3f},{b['ci'][1]:.3f}]"
    d = b["auc"] - a["auc"]
    flag = "  <-- crosses 0.5" if (a["auc"] - 0.5) * (b["auc"] - 0.5) < 0 else ""
    print(f"{f:24s}  {sa:>28s}   {sb:>28s}   {d:+8.4f}{flag}")

(W.parent / "qc_compare_manavgat_corrected.json").write_text(
    json.dumps(report, indent=2), encoding="utf-8")
print("\nwrote qc_compare_manavgat.json")
