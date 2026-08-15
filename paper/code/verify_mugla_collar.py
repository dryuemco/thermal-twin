"""Hold the Muğla two-event arm to the same frame test as everything else.

Section 4.10 withdraws every cross-region sign reversal on the ground that the
evaluation frames are not comparable. The two-event arm was exempted on the
ground that "the frame is fixed by construction". The AOI is fixed, but the
evaluation frame in Section 4.10's sense is not: the 2022 arm is one compact
scar of ~331 burned cells inside a ~38,790-cell box, which is a larger far field
than any cross-region arm. If the collar removes the cross-region reversals it
may remove this one too, and the asymmetry has to be tested rather than asserted.

The 2022 arm's own step8a export is not in this tree, but it can be reconstructed:
elevation, slope and land cover are identical across the two arms to the digit
(Section 4.9), so the 2021 parquet supplies the predictors and the frozen
component-membership export supplies the 2022 burned mask.

Read-only with respect to repo/.
"""
import sys

import numpy as np
import pandas as pd
from scipy import ndimage
from sklearn.metrics import roc_auc_score

OUT = sys.argv[1]
PARQ = "repo/outputs/experiments/mugla_2021/step8a/step8a_500m_modeling_dataset.parquet"
AUDIT = ("paper/mugla_temporal_raw/burned_pattern_audit_mugla_2021__mugla_2022_event_relative"
         "/experiments/{}/component_membership.parquet")
CELL_KM, BLOCK, NBOOT, SEED = 0.45, 10, 1000, 42
FEATS = ["elevation_mean", "slope_mean", "ndvi_mean", "current_lst_mean",
         "current_tvdi_mean", "lst_anomaly_mean", "tvdi_difference_mean"]

d = pd.read_parquet(PARQ)
d = d[(d.valid_for_modeling == True) &  # noqa: E712
      (d.burnable_tree_shrub_grass == True)].reset_index(drop=True)  # noqa: E712
print(f"Muğla primary population: {len(d)} cells, {int(d.burned.sum())} burned in 2021")

memb = {}
for arm in ("mugla_2021", "mugla_2022_event_relative"):
    m = pd.read_parquet(AUDIT.format(arm))
    pops = sorted(m.population.unique())
    pick = [p for p in pops if "burnable" in p and "burned" in p] or [p for p in pops if "burned" in p]
    memb[arm] = m[m.population == pick[0]][["row_500m", "col_500m"]].drop_duplicates()
    print(f"  {arm:28s} population '{pick[0]}': {len(memb[arm])} burned cells")

key = lambda f: set(zip(f.row_500m.astype(int), f.col_500m.astype(int)))
b21, b22 = key(memb["mugla_2021"]), key(memb["mugla_2022_event_relative"])
cells = list(zip(d.row_500m.astype(int), d.col_500m.astype(int)))
d["burned_2021"] = [c in b21 for c in cells]
d["burned_2022"] = [c in b22 for c in cells]
print(f"\nmatched onto the primary population: 2021 {int(d.burned_2021.sum())}, "
      f"2022 {int(d.burned_2022.sum())}")

# the 2022 arm is the 2021 arm with the 2021 scar removed
arm22 = d[~d.burned_2021].reset_index(drop=True)
arm21 = d.copy()
print(f"2022 arm after removing the 2021 scar: {len(arm22)} cells, "
      f"{int(arm22.burned_2022.sum())} burned")


def add_dist(f, lab):
    r0, c0 = int(f.row_500m.min()), int(f.col_500m.min())
    H = int(f.row_500m.max()) - r0 + 1
    W = int(f.col_500m.max()) - c0 + 1
    rr = f.row_500m.to_numpy().astype(int) - r0
    cc = f.col_500m.to_numpy().astype(int) - c0
    bg = np.ones((H, W), dtype=bool)
    b = f[lab].to_numpy().astype(bool)
    bg[rr[b], cc[b]] = False
    f = f.copy()
    f["dist_km"] = ndimage.distance_transform_edt(bg)[rr, cc] * CELL_KM
    f["block"] = (f.row_500m // BLOCK).astype(str) + "_" + (f.col_500m // BLOCK).astype(str)
    return f


def boot(y, x, blk, seed=SEED):
    ok = ~pd.isna(x)
    y, x, blk = np.asarray(y)[ok].astype(int), np.asarray(x)[ok], np.asarray(blk)[ok]
    if len(np.unique(y)) < 2:
        return np.nan, np.nan, np.nan
    pt = roc_auc_score(y, x)
    rng = np.random.default_rng(seed)
    u = np.unique(blk)
    idx = {b: np.where(blk == b)[0] for b in u}
    out = []
    for _ in range(NBOOT):
        pick = rng.choice(u, len(u), replace=True)
        i = np.concatenate([idx[b] for b in pick])
        if len(np.unique(y[i])) > 1:
            out.append(roc_auc_score(y[i], x[i]))
    return pt, float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))


rows = []
for name, f, lab in [("2021", add_dist(arm21, "burned_2021"), "burned_2021"),
                     ("2022", add_dist(arm22, "burned_2022"), "burned_2022")]:
    far = 100 * (f.dist_km > 10).mean()
    print(f"\n=== {name} arm: {len(f)} cells, {int(f[lab].sum())} burned, "
          f"{far:.1f} % beyond 10 km, median {np.median(f.dist_km):.1f} km ===")
    for frame, sub in [("full", f), ("collar10", f[f.dist_km <= 10])]:
        for feat in FEATS:
            pt, lo, hi = boot(sub[lab], sub[feat], sub.block)
            if np.isnan(pt):
                continue
            excl = (lo > 0.5) or (hi < 0.5)
            rows.append({"arm": name, "frame": frame, "feature": feat, "auc": pt,
                         "ci_lo": lo, "ci_hi": hi, "excludes_0.5": bool(excl)})
            if feat == "elevation_mean":
                print(f"  {frame:9s} elevation {pt:.3f} [{lo:.3f}, {hi:.3f}]  "
                      f"excludes 0.5: {'YES' if excl else 'no'}")

R = pd.DataFrame(rows)
print("\n" + "=" * 74)
print("DOES THE TWO-EVENT ELEVATION REVERSAL SURVIVE THE COLLAR?")
print("=" * 74)
for frame in ("full", "collar10"):
    e = R[(R.frame == frame) & (R.feature == "elevation_mean")]
    if len(e) == 2:
        a, b = e.iloc[0], e.iloc[1]
        opposite = (a.auc - 0.5) * (b.auc - 0.5) < 0
        both = bool(a["excludes_0.5"] and b["excludes_0.5"])
        print(f"  {frame:9s} 2021 {a.auc:.3f} [{a.ci_lo:.3f},{a.ci_hi:.3f}]   "
              f"2022 {b.auc:.3f} [{b.ci_lo:.3f},{b.ci_hi:.3f}]")
        print(f"            opposite sides of 0.5: {opposite};  both intervals exclude 0.5: {both}"
              f"  ->  {'BOOTSTRAP-SUPPORTED REVERSAL' if (opposite and both) else 'not supported'}")
R.to_csv(OUT, index=False)
print(f"\nwrote {OUT}")
