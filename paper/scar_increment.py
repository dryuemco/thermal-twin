"""
Does the thermal increment survive fire-level holdout?

Section 4.2 reports the within-region increment (+0.056 to +0.153) under blocked
cross-validation, which Section 4.3 shows is a regime that overstates performance
on a fire the model has not seen. A referee's point is sharp: the paper never
measures its own headline quantity under the evaluation it argues is the honest
one, and the answer would either confirm the increment or reveal it as an
artefact of interleaved holdout. Either result is worth having.

This runs the baseline and thermal feature sets through the leave-one-scar-out
arm and reports the paired difference per scar, with a t interval over scars,
which is that arm's resampling unit.

Read-only with respect to the repository.
"""
import json
import sys

import numpy as np
import pandas as pd
from scipy import ndimage, stats
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

STAGING = sys.argv[1]
REGIONS = ["manavgat_2021", "bejis_2022", "mugla_2021",
           "evia_2021_extended", "montiferru_2021"]
BASELINE = ["ndvi_mean", "elevation_mean", "slope_mean", "landcover_dominant"]
THERMAL = BASELINE + ["lst_anomaly_mean", "current_lst_mean", "current_tvdi_mean",
                      "tvdi_difference_mean", "downscaled_lst_mean", "fused_lst_mean"]
CAT = "landcover_dominant"
KM, BUF, MIN_SCAR = 0.45, 2, 50


def build(feats):
    num = [f for f in feats if f != CAT]
    tr = [("num", Pipeline([("imputer", SimpleImputer(strategy="median"))]), num)]
    if CAT in feats:
        tr.append(("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                                    ("onehot", OneHotEncoder(handle_unknown="ignore"))]), [CAT]))
    return Pipeline([("preprocess", ColumnTransformer(tr)),
                     ("clf", RandomForestClassifier(n_estimators=300, min_samples_leaf=3,
                                                    class_weight="balanced",
                                                    random_state=42, n_jobs=-1))])


def load(reg):
    d = pd.read_parquet(f"{STAGING}/{reg}.parquet",
                        columns=["burned", "valid_for_modeling", "burnable_tree_shrub_grass",
                                 "row_500m", "col_500m"] + THERMAL)
    return d[(d.valid_for_modeling == True) & (d.burnable_tree_shrub_grass == True)].reset_index(drop=True)  # noqa: E712


rows = []
for reg in REGIONS:
    df = load(reg)
    r0, c0 = df.row_500m.min(), df.col_500m.min()
    H, W = int(df.row_500m.max() - r0) + 1, int(df.col_500m.max() - c0) + 1
    g = np.zeros((H, W), np.uint8)
    rr = (df.row_500m - r0).to_numpy().astype(int)
    cc = (df.col_500m - c0).to_numpy().astype(int)
    g[rr[df.burned == 1], cc[df.burned == 1]] = 1
    lab, _ = ndimage.label(g, structure=np.ones((3, 3)))
    cl = lab[rr, cc]
    sizes = pd.Series(cl[df.burned.to_numpy() == 1]).value_counts()
    for s in [int(x) for x in sizes[sizes >= MIN_SCAR].index if x != 0]:
        m = np.zeros_like(g); m[lab == s] = 1
        held = ndimage.binary_dilation(m, iterations=max(1, round(BUF / KM)))[rr, cc]
        tgt, src = df[held], df[~held]
        if tgt.burned.nunique() < 2 or src.burned.nunique() < 2:
            continue
        out = {"region": reg, "scar": s, "src_pos": int(src.burned.sum()),
               "tgt_pos": int(tgt.burned.sum())}
        for lbl, feats in (("baseline", BASELINE), ("thermal", THERMAL)):
            mdl = build(feats).fit(src[feats], src.burned)
            out[lbl] = float(roc_auc_score(tgt.burned, mdl.predict_proba(tgt[feats])[:, 1]))
        out["increment"] = out["thermal"] - out["baseline"]
        rows.append(out)
        print(f"{reg:20s} scar {s:3d}  baseline={out['baseline']:.4f}  "
              f"thermal={out['thermal']:.4f}  increment={out['increment']:+.4f}", flush=True)

d = pd.DataFrame(rows)
inc = d.increment
n = len(inc); se = inc.std(ddof=1) / np.sqrt(n)
t = stats.t.ppf(0.975, n - 1) * se
print("\n=== THERMAL INCREMENT UNDER LEAVE-ONE-SCAR-OUT ===")
print(f"  n = {n} scars")
print(f"  baseline mean {d.baseline.mean():.4f}   thermal mean {d.thermal.mean():.4f}")
print(f"  increment     {inc.mean():+.4f}  t-95% [{inc.mean()-t:+.4f}, {inc.mean()+t:+.4f}]")
print(f"  positive in {(inc > 0).sum()} of {n};  range {inc.min():+.4f} to {inc.max():+.4f}")
mg = d[d.region == "mugla_2021"]
if len(mg) > 1:
    i2 = mg.increment; s2 = i2.std(ddof=1) / np.sqrt(len(i2))
    t2 = stats.t.ppf(0.975, len(i2) - 1) * s2
    print(f"  Muğla only (n={len(i2)}): {i2.mean():+.4f}  [{i2.mean()-t2:+.4f}, {i2.mean()+t2:+.4f}]")
print("\n  for comparison: blocked-CV within-region increment +0.056 to +0.153;")
print("                  half-split increment +0.027; cross-region +0.004")
d.to_json(f"{STAGING}/../scar_increment.json", orient="records", indent=1)
