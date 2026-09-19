"""
Decompose the foreign-region arm by source, rather than averaging it.

A referee's point is sharp and specific. Row D of the ladder averages four
foreign models per scar. But this paper's own finding is that transfer is
pair-specific and sign-unstable, running from 0.326 to 0.686 across the
twenty-direction matrix, so averaging a below-chance source with an above-chance
one returns about 0.5 by construction. If that is what row D is doing, then
"crossing a region boundary costs nothing" is an artefact of the aggregation and
not a result.

This reports every scar x source combination separately, so the spread behind
the pooled 0.555 is visible.

Read-only with respect to the repository.
"""
import json
import sys

import numpy as np
import pandas as pd
from scipy import ndimage
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
import _canonical


def _guard(X, y):
    """Methods 3.13: forbidden-column assertion on the exact columns passed to the model."""
    _canonical.assert_no_leakage(list(X.columns))
    return X, y


STAGING = sys.argv[1]
REGIONS = ["manavgat_2021", "bejis_2022", "mugla_2021",
           "evia_2021_extended", "montiferru_2021"]
TH = ["ndvi_mean", "elevation_mean", "slope_mean", "landcover_dominant",
      "lst_anomaly_mean", "current_lst_mean", "current_tvdi_mean",
      "tvdi_difference_mean", "downscaled_lst_mean", "fused_lst_mean"]
CAT = "landcover_dominant"
KM, BUF, MIN_SCAR = 0.45, 2, 50


def build():
    num = [f for f in TH if f != CAT]
    tr = [("num", Pipeline([("imputer", SimpleImputer(strategy="median"))]), num),
          ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                            ("onehot", OneHotEncoder(handle_unknown="ignore"))]), [CAT])]
    return Pipeline([("preprocess", ColumnTransformer(tr)),
                     ("clf", RandomForestClassifier(n_estimators=300, min_samples_leaf=3,
                                                    class_weight="balanced",
                                                    random_state=42, n_jobs=4))])


def load(reg):
    d = _canonical.load(reg,
                        columns=["burned", "valid_for_modeling", "burnable_tree_shrub_grass",
                                 "row_500m", "col_500m"] + TH)
    return d[(d.valid_for_modeling == True) & (d.burnable_tree_shrub_grass == True)].reset_index(drop=True)  # noqa: E712


data = {r: load(r) for r in REGIONS}
models = {r: build().fit(*_guard(data[r][TH], data[r].burned)) for r in REGIONS}
print("five source models fitted\n", flush=True)

rows = []
for reg in REGIONS:
    df = data[reg]
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
        tgt = df[held]
        if tgt.burned.nunique() < 2:
            continue
        for src in REGIONS:
            if src == reg:
                continue
            a = roc_auc_score(tgt.burned, models[src].predict_proba(tgt[TH])[:, 1])
            rows.append({"target_region": reg, "scar": s, "source": src, "auc": float(a)})
        got = [r for r in rows if r["target_region"] == reg and r["scar"] == s]
        v = [r["auc"] for r in got]
        print(f"{reg:20s} scar {s:3d}  " +
              "  ".join(f"{r['source'][:8]}={r['auc']:.3f}" for r in got) +
              f"   mean={np.mean(v):.3f}  spread={max(v)-min(v):.3f}", flush=True)

d = pd.DataFrame(rows)
print("\n=== ROW D DECOMPOSED BY SOURCE ===")
print(f"  combinations: {len(d)}   pooled mean: {d.auc.mean():.4f}")
print(f"  overall range: {d.auc.min():.3f} to {d.auc.max():.3f}")
print(f"  below chance: {(d.auc < 0.5).sum()} of {len(d)}")
print("\n  per-scar spread (max minus min across the four sources):")
sp = d.groupby(["target_region", "scar"]).auc.agg(["mean", "min", "max"])
sp["spread"] = sp["max"] - sp["min"]
print(sp.round(3).to_string())
print(f"\n  mean per-scar spread: {sp.spread.mean():.3f}")
print("\n  per-source mean over all scars:")
print(d.groupby("source").auc.agg(["mean", "min", "max", "count"]).round(3).to_string())
d.to_json(f"{STAGING}/../d_per_source.json", orient="records", indent=1)
