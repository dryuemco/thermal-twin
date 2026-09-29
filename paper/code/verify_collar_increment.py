"""Three checks raised by a final science referee.

ITEM 6. Table 9 claims BOTH diagnostics that cleared zero become degenerate on
the collar. The two that cleared zero are agree_fraction_supported (+0.84) and
the SUPPORTED-SUBSET cosine (+0.81). What was actually recomputed was
agree_fraction_supported and cosine over ALL NINE features, which never cleared
zero. So one of the two claims is untested. Compute the supported-subset cosine
on the collar.

ITEM 9. The within-region thermal increment is never established on the
equalised frame, though the paper argues that frame is the correct one. Run the
baseline arm on the collar so the increment can be stated there.

ITEM 4. The 0.155 matched shortfall carries no interval anywhere. Compute one,
paired by target region.

Read-only with respect to repo/.
"""
import sys

import numpy as np
import pandas as pd
from scipy import ndimage, stats
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
BASE = ["ndvi_mean", "elevation_mean", "slope_mean", "landcover_dominant"]
FEATS9 = [f for f in TH if f != "landcover_dominant"]
CAT = "landcover_dominant"
CELL_KM, SEED, NB = 0.45, 42, 1000
import os
# Artefacts this script reads or writes that are themselves regenerated from the
# canonical inputs. Default "paper" is the published location; the canonical re-run
# sets PAPER_ARTEFACTS=paper/canonical_rerun so nothing published is overwritten.
ART = os.environ.get("PAPER_ARTEFACTS", "paper")


def build(fe):
    num = [f for f in fe if f != CAT]
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

print("=" * 76)
print("ITEM 9  WITHIN-REGION INCREMENT ON THE EQUALISED FRAME")
print("=" * 76)
for collar in [None, 10, 5]:
    lbl = "full" if collar is None else f"{collar}km"
    incs = []
    for r in REG:
        d = data[r] if collar is None else data[r][data[r].dist_km <= collar]
        g = (d.row_500m // 10).astype(str) + "_" + (d.col_500m // 10).astype(str)
        got = {}
        for name, fe in (("thermal", TH), ("baseline", BASE)):
            oof = np.full(len(d), np.nan)
            for tr_i, te_i in StratifiedGroupKFold(5, shuffle=True, random_state=SEED).split(
                    d[fe], d.burned, groups=g):
                oof[te_i] = build(fe).fit(*_guard(d.iloc[tr_i][fe], d.iloc[tr_i].burned)) \
                    .predict_proba(d.iloc[te_i][fe])[:, 1]
            got[name] = roc_auc_score(d.burned, oof)
        inc = got["thermal"] - got["baseline"]
        incs.append(inc)
        rows.append({"check": "increment", "frame": lbl, "region": r,
                     "thermal": got["thermal"], "baseline": got["baseline"], "increment": inc})
        print(f"  {lbl:5s} {r:22s} thermal {got['thermal']:.3f}  baseline {got['baseline']:.3f}  "
              f"increment {inc:+.3f}")
    print(f"  {lbl:5s} MEAN increment {np.mean(incs):+.4f}  "
          f"(positive in {sum(1 for i in incs if i>0)}/5)\n")

print("=" * 76)
print("ITEM 4  AN INTERVAL ON THE MATCHED SHORTFALL, PAIRED BY TARGET REGION")
print("=" * 76)
tr_c = pd.read_csv(f"{ART}/aoi_frame_transfer.csv")
tr_c = tr_c[(tr_c.source_frame == "10km") & (tr_c.target_frame == "10km")]
tr_c["tgt"] = tr_c.direction.str.split("_to_").str[1]
within = {r["region"]: r["thermal"] for r in rows if r["check"] == "increment" and r["frame"] == "10km"}
diffs = []
for r in REG:
    w = within[r]
    t = tr_c[tr_c.tgt == r].thermal.mean()
    diffs.append(w - t)
    print(f"  {r:22s} within {w:.3f}  mean transfer in {t:.3f}  shortfall {w-t:+.3f}")
d = np.array(diffs)
se = d.std(ddof=1) / np.sqrt(len(d))
tcrit = stats.t.ppf(0.975, len(d) - 1) * se
print(f"\n  mean shortfall {d.mean():+.4f}  [{d.mean()-tcrit:+.4f}, {d.mean()+tcrit:+.4f}]  "
      f"(t over {len(d)} target regions)")
rows.append({"check": "shortfall", "mean": float(d.mean()),
             "lo": float(d.mean()-tcrit), "hi": float(d.mean()+tcrit), "n": len(d)})

print()
print("=" * 76)
print("ITEM 6  THE SUPPORTED-SUBSET COSINE ON THE COLLAR (never tested)")
print("=" * 76)


def signed(sub, f, seed=SEED):
    ok = sub[f].notna()
    y, x = sub.burned[ok].to_numpy(), sub[f][ok].to_numpy()
    blk = ((sub.row_500m // 10).astype(str) + "_" + (sub.col_500m // 10).astype(str))[ok].to_numpy()
    if len(np.unique(y)) < 2:
        return np.nan, False
    pt = roc_auc_score(y, x)
    rng = np.random.default_rng(seed)
    u = np.unique(blk)
    idx = {b: np.where(blk == b)[0] for b in u}
    out = []
    for _ in range(NB):
        pick = rng.choice(u, len(u), replace=True)
        i = np.concatenate([idx[b] for b in pick])
        if len(np.unique(y[i])) > 1:
            out.append(roc_auc_score(y[i], x[i]))
    lo, hi = np.percentile(out, 2.5), np.percentile(out, 97.5)
    return pt, bool(lo > 0.5 or hi < 0.5)


# Full-frame support flags come from the pipeline's Step9G signed-AUC CIs (5-AOI synthesis), the same source as
# Table B2 and the registered diagnostic family (conditional_similarity.mjs). Before 2026-09-23 this script
# used its own bootstrap for the full frame too. The two bootstraps are both valid 10-cell block resamples with
# different RNG streams. Under the corrected Manavgat label they disagree on one knife-edge flag (Manavgat
# ndvi_mean: [0.5022, 0.6237] here vs [0.4993, 0.6278] in Step9G), and that single flag moved the full-frame
# rho from +0.493 to +0.698. The collar has no Step9G run, so it keeps this script's bootstrap.
SYNTH = ("drive_new/diagnostics/multi_aoi_transfer_synthesis/"
         "bejis_2022__evia_2021_extended__manavgat_2021__montiferru_2021__mugla_2021/multi_aoi_feature_stability.csv")
_fs = pd.read_csv(SYNTH)
S9G = {}
for side in ("a", "b"):
    for _, rr in _fs.iterrows():
        lo, hi = rr[f"experiment_{side}_ci_low"], rr[f"experiment_{side}_ci_high"]
        S9G[(rr[f"experiment_{side}"], rr["feature"])] = bool(lo > 0.5 or hi < 0.5)

for frame, collar in [("full", None), ("collar10", 10)]:
    prof = {}
    for r in REG:
        sub = data[r] if collar is None else data[r][data[r].dist_km <= collar]
        for f in FEATS9:
            prof[(r, f)] = signed(sub, f)
            if collar is None:
                prof[(r, f)] = (prof[(r, f)][0], S9G[(r, f)])
    tv = {}
    src = pd.read_csv("paper/baseline_vs_thermal_transfer.csv") if frame == "full" else tr_c
    col = "thermal_roc" if frame == "full" else "thermal"
    for _, rr in src.iterrows():
        tv[rr["direction"]] = rr[col]
    recs = []
    for s in REG:
        for t in REG:
            if s == t:
                continue
            both = [f for f in FEATS9 if prof[(s, f)][1] and prof[(t, f)][1]]
            if not both:
                continue
            vs = np.array([prof[(s, f)][0] - 0.5 for f in both])
            vt = np.array([prof[(t, f)][0] - 0.5 for f in both])
            cos = float(vs @ vt / (np.linalg.norm(vs) * np.linalg.norm(vt)))
            recs.append({"direction": f"{s}_to_{t}", "cos_supported": cos,
                         "transfer": tv.get(f"{s}_to_{t}", np.nan), "k": len(both)})
    D = pd.DataFrame(recs).dropna()
    nuniq = D.cos_supported.nunique()
    print(f"  {frame:9s} defined in {len(D)}/20 directions, {nuniq} distinct values, "
          f"variance {D.cos_supported.var():.6f}")
    if nuniq > 1:
        rho, pv = stats.spearmanr(D.cos_supported, D.transfer)
        print(f"            Spearman rho vs transfer = {rho:+.4f} (p={pv:.4f})")
    else:
        print("            *** DEGENERATE: no variance, correlation undefined ***")
    rows.append({"check": "cos_supported", "frame": frame, "n": len(D),
                 "distinct": int(nuniq), "variance": float(D.cos_supported.var())})

pd.DataFrame(rows).to_csv(OUT, index=False)
print(f"\nwrote {OUT}")
