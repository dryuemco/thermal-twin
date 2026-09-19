"""Three checks on Section 4.10, all raised against the section as written.

CHECK 1. The survival claim sets a 10 km-collar transfer mean (0.617) against a
full-rectangle, 1 km-blocking within-region reference (~0.87). Those are not the
same frame or the same blocking. Recompute the within-region reference ON the
collar and at the blocking the paper itself defends (5 km), so the gap is a
matched quantity.

CHECK 2. The paper withdrew the LST-anomaly reversal because Evia's own interval
includes 0.5 by 0.003. Table B3's note already commits the paper to a difference
interval on the pair as an instrument. Apply it under the collar: does the
Bejis-Evia difference exclude zero?

CHECK 3. Section 4.10 reads the agreed LST sign as fuel availability dominating
dryness, citing survival within NDVI deciles. The reciprocal test was not run:
does NDVI survive within LST deciles? If NDVI reverses and LST does not, the
reading is backwards.

Read-only with respect to repo/.
"""
import sys

import numpy as np
import pandas as pd
from scipy import ndimage
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
import _canonical


def _guard(X, y):
    """Methods 3.13: forbidden-column assertion on the exact columns passed to the model."""
    _canonical.assert_no_leakage(list(X.columns))
    return X, y


OUT = sys.argv[1]
REG = ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended", "montiferru_2021"]
TH = ["ndvi_mean", "elevation_mean", "slope_mean", "landcover_dominant", "lst_anomaly_mean",
      "current_lst_mean", "current_tvdi_mean", "tvdi_difference_mean",
      "downscaled_lst_mean", "fused_lst_mean"]
CAT = "landcover_dominant"
CELL_KM, SEED, NBOOT = 0.45, 42, 1000


def build():
    num = [f for f in TH if f != CAT]
    tr = [("num", Pipeline([("i", SimpleImputer(strategy="median"))]), num),
          ("cat", Pipeline([("i", SimpleImputer(strategy="most_frequent")),
                            ("o", OneHotEncoder(handle_unknown="ignore"))]), [CAT])]
    return Pipeline([("p", ColumnTransformer(tr)),
                     ("c", RandomForestClassifier(n_estimators=300, min_samples_leaf=3,
                                                  class_weight="balanced",
                                                  random_state=SEED, n_jobs=4))])


def load(r):
    d = _canonical.load(r)
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
    return d


data = {r: load(r) for r in REG}
rows = []

print("=" * 78)
print("CHECK 1  A MATCHED WITHIN-REGION REFERENCE")
print("  the paper compares 0.617 (10 km collar) against ~0.87 (full frame, 1 km blocking)")
print("=" * 78)
for collar in [None, 10, 5]:
    for blk in [2, 10]:
        vals = []
        for r in REG:
            d = data[r] if collar is None else data[r][data[r].dist_km <= collar]
            g = (d.row_500m // blk).astype(str) + "_" + (d.col_500m // blk).astype(str)
            oof = np.full(len(d), np.nan)
            try:
                for tr_i, te_i in StratifiedGroupKFold(5, shuffle=True, random_state=SEED).split(
                        d[TH], d.burned, groups=g):
                    oof[te_i] = build().fit(*_guard(d.iloc[tr_i][TH], d.iloc[tr_i].burned)) \
                        .predict_proba(d.iloc[te_i][TH])[:, 1]
                vals.append(roc_auc_score(d.burned, oof))
            except Exception as e:
                print("   skip", r, collar, blk, e)
        lbl = "full" if collar is None else f"{collar}km"
        m = float(np.mean(vals))
        rows.append({"check": "within", "frame": lbl, "blocking_cells": blk, "mean_within": m})
        print(f"  frame {lbl:6s} blocking {blk:2d} cells (~{blk*0.45:.1f} km): "
              f"within-region mean {m:.4f}   [{', '.join(f'{v:.3f}' for v in vals)}]")

print("\n  transfer means for reference: full 0.5400, 10 km collar 0.6166, 5 km collar 0.6077")

print()
print("=" * 78)
print("CHECK 2  DIFFERENCE INTERVALS ON THE LST ANOMALY, 10 km COLLAR")
print("  the paper's own Table B3 note names this instrument")
print("=" * 78)


def boot_auc_reps(sub, feat, blk=10, seed=SEED):
    d = sub.copy()
    d["block"] = (d.row_500m // blk).astype(str) + "_" + (d.col_500m // blk).astype(str)
    ok = d[feat].notna()
    y, x, b = d.burned[ok].to_numpy().astype(int), d[feat][ok].to_numpy(), d.block[ok].to_numpy()
    if len(np.unique(y)) < 2:
        return np.nan, np.array([])
    rng = np.random.default_rng(seed)
    u = np.unique(b)
    idx = {k: np.where(b == k)[0] for k in u}
    out = []
    for _ in range(NBOOT):
        pick = rng.choice(u, len(u), replace=True)
        i = np.concatenate([idx[k] for k in pick])
        if len(np.unique(y[i])) > 1:
            out.append(roc_auc_score(y[i], x[i]))
    return roc_auc_score(y, x), np.array(out)


FEAT = "lst_anomaly_mean"
reps = {}
for r in REG:
    sub = data[r][data[r].dist_km <= 10]
    pt, rp = boot_auc_reps(sub, FEAT)
    reps[r] = (pt, rp)
    print(f"  {r:22s} {pt:.3f} [{np.percentile(rp,2.5):.3f}, {np.percentile(rp,97.5):.3f}]")
print()
for i, a in enumerate(REG):
    for b in REG[i+1:]:
        pa, ra = reps[a]
        pb, rb = reps[b]
        n = min(len(ra), len(rb))
        diff = ra[:n] - rb[:n]
        lo, hi = np.percentile(diff, 2.5), np.percentile(diff, 97.5)
        opp = (pa - 0.5) * (pb - 0.5) < 0
        excl = lo > 0 or hi < 0
        rows.append({"check": "anomaly_diff", "region_a": a, "region_b": b,
                     "auc_a": pa, "auc_b": pb, "diff": pa - pb,
                     "diff_lo": lo, "diff_hi": hi,
                     "opposite_sides": bool(opp), "diff_excludes_0": bool(excl)})
        if opp:
            print(f"  {a[:12]:12s} {pa:.3f} vs {b[:12]:12s} {pb:.3f}  diff {pa-pb:+.3f} "
                  f"[{lo:+.3f}, {hi:+.3f}]  opposite sides, diff excludes 0: "
                  f"{'YES' if excl else 'no'}")

print()
print("=" * 78)
print("CHECK 3  RECIPROCAL STRATIFICATION: does NDVI survive within LST deciles?")
print("=" * 78)


def strat(sub, feat, by, nbin=10):
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
        w = (g.burned == 1).sum() * (g.burned == 0).sum()
        num += roc_auc_score(g.burned, g[feat]) * w
        den += w
    return num / den if den else np.nan


print(f"  {'region':22s} {'LST raw':>8s} {'LST|ndvi':>9s} {'NDVI raw':>9s} {'NDVI|lst':>9s} {'LST|dist':>9s}")
for r in REG:
    sub = data[r][data[r].dist_km <= 10]
    lr = roc_auc_score(sub.burned[sub.current_lst_mean.notna()],
                       sub.current_lst_mean[sub.current_lst_mean.notna()])
    ln = strat(sub, "current_lst_mean", "ndvi_mean")
    nr = roc_auc_score(sub.burned[sub.ndvi_mean.notna()], sub.ndvi_mean[sub.ndvi_mean.notna()])
    nl = strat(sub, "ndvi_mean", "current_lst_mean")
    ld = strat(sub, "current_lst_mean", "dist_km")
    rows.append({"check": "reciprocal", "region": r, "lst_raw": lr, "lst_given_ndvi": ln,
                 "ndvi_raw": nr, "ndvi_given_lst": nl, "lst_given_dist": ld})
    print(f"  {r:22s} {lr:8.3f} {ln:9.3f} {nr:9.3f} {nl:9.3f} {ld:9.3f}")
print("\n  (values below 0.5 mean higher predictor -> less burning)")

pd.DataFrame(rows).to_csv(OUT, index=False)
print(f"\nwrote {OUT}")
