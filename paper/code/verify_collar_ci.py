"""
Two checks on Section 4.9, both raised by a referee against the section as written.

CHECK 1. Section 4.9 says "one reversal survives" for lst_anomaly_mean under the
10 km collar, quoting point estimates only. But Section 3.10 defines a reversal
as bootstrap-supported ONLY when each region's own interval excludes 0.5. The
collar arm therefore has not been held to the paper's own criterion. This runs
the same 10-cell spatial-block bootstrap used everywhere else.

CHECK 2. Section 4.9 reports "all five regions agree in sign on elevation, on
LST and on TVDI" as the reassuring outcome of equalisation, without saying WHAT
sign. For LST the agreed sign is below 0.5, i.e. hotter pre-fire surface
associated with LESS burning, which contradicts the moisture-stress framing of
Section 1.2. This reports the direction explicitly and tests whether it is a
lapse-rate or greenness artefact by stratifying within elevation and NDVI
deciles.

Read-only with respect to repo/.
"""
import json
import sys

import numpy as np
import pandas as pd
from scipy import ndimage
from sklearn.metrics import roc_auc_score

OUT = sys.argv[1]
REGIONS = ["manavgat_2021", "bejis_2022", "mugla_2021",
           "evia_2021_extended", "montiferru_2021"]
ROOT = "repo/outputs/experiments/{}/step8a/step8a_500m_modeling_dataset.parquet"
FEATS = ["elevation_mean", "current_lst_mean", "current_tvdi_mean",
         "lst_anomaly_mean", "tvdi_difference_mean", "ndvi_mean"]
CELL_KM, BLOCK, NBOOT, SEED = 0.45, 10, 1000, 42


def load(reg):
    d = pd.read_parquet(ROOT.format(reg))
    d = d[(d.valid_for_modeling == True) &  # noqa: E712
          (d.burnable_tree_shrub_grass == True)].reset_index(drop=True)  # noqa: E712
    r0, c0 = int(d.row_500m.min()), int(d.col_500m.min())
    H = int(d.row_500m.max()) - r0 + 1
    W = int(d.col_500m.max()) - c0 + 1
    rr = d.row_500m.to_numpy().astype(int) - r0
    cc = d.col_500m.to_numpy().astype(int) - c0
    bg = np.ones((H, W), dtype=bool)
    b = d.burned.to_numpy() == 1
    bg[rr[b], cc[b]] = False
    d["dist_km"] = ndimage.distance_transform_edt(bg)[rr, cc] * CELL_KM
    d["block"] = ((d.row_500m // BLOCK).astype(str) + "_" + (d.col_500m // BLOCK).astype(str))
    return d


def block_boot_auc(y, x, blocks, nboot=NBOOT, seed=SEED):
    """Spatial-block bootstrap CI on a signed univariate AUC."""
    rng = np.random.default_rng(seed)
    ok = ~pd.isna(x)
    y, x, blocks = np.asarray(y)[ok], np.asarray(x)[ok], np.asarray(blocks)[ok]
    uniq = np.unique(blocks)
    idx_by_block = {b: np.where(blocks == b)[0] for b in uniq}
    point = roc_auc_score(y, x) if len(np.unique(y)) > 1 else np.nan
    out = []
    for _ in range(nboot):
        pick = rng.choice(uniq, len(uniq), replace=True)
        idx = np.concatenate([idx_by_block[b] for b in pick])
        if len(np.unique(y[idx])) < 2:
            continue
        out.append(roc_auc_score(y[idx], x[idx]))
    if not out:
        return point, np.nan, np.nan
    return point, float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))


data = {r: load(r) for r in REGIONS}

print("=" * 82)
print("CHECK 1  COLLAR ARM UNDER THE PAPER'S OWN REVERSAL CRITERION (3.10)")
print("  bootstrap-supported requires EACH region's own interval to exclude 0.5")
print("=" * 82)
rows = []
for f in FEATS:
    print(f"\n--- {f} ---")
    for reg in REGIONS:
        d = data[reg]
        sub = d[d.dist_km <= 10]
        pt, lo, hi = block_boot_auc(sub.burned, sub[f], sub.block)
        excl = (lo > 0.5) or (hi < 0.5)
        side = "above" if pt > 0.5 else "below"
        rows.append({"check": "collar_ci", "feature": f, "region": reg,
                     "auc": pt, "ci_lo": lo, "ci_hi": hi,
                     "interval_excludes_0.5": bool(excl), "side": side})
        print(f"  {reg:22s} {pt:.3f} [{lo:.3f}, {hi:.3f}]  {side:5s}  "
              f"excludes 0.5: {'YES' if excl else 'no '}")

print()
print("=" * 82)
print("CHECK 2  WHAT SIGN DO THE FIVE REGIONS AGREE ON, AND IS IT A PROXY?")
print("  signed AUC < 0.5 means HIGHER value associated with LESS burning")
print("=" * 82)


def stratified_auc(sub, feat, by, nbin=10):
    """Pool within-stratum concordance: rank feat inside deciles of `by`."""
    s = sub[[feat, by, "burned"]].dropna()
    if s.burned.nunique() < 2:
        return np.nan
    try:
        s["bin"] = pd.qcut(s[by], nbin, labels=False, duplicates="drop")
    except ValueError:
        return np.nan
    num = den = 0.0
    for _, g in s.groupby("bin"):
        if g.burned.nunique() < 2:
            continue
        a = roc_auc_score(g.burned, g[feat])
        w = (g.burned == 1).sum() * (g.burned == 0).sum()
        num += a * w
        den += w
    return num / den if den else np.nan


for f in ["current_lst_mean", "current_tvdi_mean", "lst_anomaly_mean"]:
    print(f"\n--- {f} ---")
    print(f"  {'region':22s} {'collar':>8s} {'| elev':>8s} {'| ndvi':>8s} {'r(f,elev)':>10s} {'r(f,ndvi)':>10s}")
    for reg in REGIONS:
        d = data[reg]
        sub = d[d.dist_km <= 10]
        raw = roc_auc_score(sub.burned[sub[f].notna()], sub[f][sub[f].notna()])
        se = stratified_auc(sub, f, "elevation_mean")
        sn = stratified_auc(sub, f, "ndvi_mean")
        m1 = sub[f].notna() & sub.elevation_mean.notna()
        m2 = sub[f].notna() & sub.ndvi_mean.notna()
        re_ = np.corrcoef(sub[f][m1], sub.elevation_mean[m1])[0, 1]
        rn = np.corrcoef(sub[f][m2], sub.ndvi_mean[m2])[0, 1]
        rows.append({"check": "stratified", "feature": f, "region": reg,
                     "collar_auc": raw, "auc_within_elev_decile": se,
                     "auc_within_ndvi_decile": sn, "r_elev": re_, "r_ndvi": rn})
        print(f"  {reg:22s} {raw:8.3f} {se:8.3f} {sn:8.3f} {re_:10.3f} {rn:10.3f}")

print()
print("=" * 82)
print("CHECK 3  HOW MANY INDEPENDENT THERMAL AXES ARE THERE? (collar frame)")
print("=" * 82)
TH6 = ["current_lst_mean", "downscaled_lst_mean", "fused_lst_mean",
       "current_tvdi_mean", "lst_anomaly_mean", "tvdi_difference_mean"]
for reg in REGIONS:
    sub = data[reg][data[reg].dist_km <= 10][TH6].dropna()
    c = sub.corr()
    print(f"\n  {reg}  (n={len(sub)})")
    print("   r(lst,fused)={:.2f}  r(lst,downscaled)={:.2f}  r(lst,tvdi)={:.2f}  "
          "r(anom,tvdi_diff)={:.2f}".format(
              c.loc["current_lst_mean", "fused_lst_mean"],
              c.loc["current_lst_mean", "downscaled_lst_mean"],
              c.loc["current_lst_mean", "current_tvdi_mean"],
              c.loc["lst_anomaly_mean", "tvdi_difference_mean"]))

pd.DataFrame(rows).to_csv(OUT, index=False)
print(f"\nwrote {OUT}")
