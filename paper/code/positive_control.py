"""
Positive control: does this transfer path register transfer it ought to register?

An external referee put one question above all others. Every transfer number in
the paper is a failure, so "nothing in this feature space travels" and "this
evaluation cannot detect travel" fit the evidence equally well. The paper has no
configuration where the harness is shown to succeed.

This supplies one. Within each region the cells are split in two by a straight
line, a model is fitted on one half and applied to the other with **no refit, no
recalibration and no threshold selection** -- the same label-free protocol the
cross-region arms use. The relationship is shared by construction: same region,
same season, same event, same processing chain. If the harness returns high AUC
here and near-chance across regions, the negative result is about the landscapes.
If it returns near-chance here too, the negative result is about the evaluation.

Two splits are run per region, east/west and north/south, because a single split
line could cut a region into halves that happen to differ.

The comparison is deliberately unfair to the paper's own thesis: a within-region
half-split is the easiest transfer task that can be posed, so it sets an upper
reference rather than a matched one.

Usage: positive_control.py <staging_dir> <out.json>
"""
import json
import sys

import numpy as np
import pandas as pd
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


STAGING, OUT = sys.argv[1], sys.argv[2]

REGIONS = ["manavgat_2021", "bejis_2022", "mugla_2021",
           "evia_2021_extended", "montiferru_2021"]
THERMAL = ["ndvi_mean", "elevation_mean", "slope_mean", "landcover_dominant",
           "lst_anomaly_mean", "current_lst_mean", "current_tvdi_mean",
           "tvdi_difference_mean", "downscaled_lst_mean", "fused_lst_mean"]
BASELINE = ["ndvi_mean", "elevation_mean", "slope_mean", "landcover_dominant"]
CAT = "landcover_dominant"
SEED = 42


def build(features):
    num = [f for f in features if f != CAT]
    tr = [("num", Pipeline([("imputer", SimpleImputer(strategy="median"))]), num)]
    if CAT in features:
        tr.append(("cat", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore"))]), [CAT]))
    return Pipeline([("preprocess", ColumnTransformer(tr)),
                     ("clf", RandomForestClassifier(
                         n_estimators=300, min_samples_leaf=3,
                         class_weight="balanced", random_state=SEED, n_jobs=4))])


def load(reg):
    df = _canonical.load(reg,
                         columns=["burned", "valid_for_modeling",
                                  "burnable_tree_shrub_grass", "row_500m", "col_500m"] + THERMAL)
    df = df[(df.valid_for_modeling == True) & (df.burnable_tree_shrub_grass == True)]  # noqa: E712
    return df.reset_index(drop=True)


results = []
for reg in REGIONS:
    df = load(reg)
    for axis, col in (("east_west", "col_500m"), ("north_south", "row_500m")):
        cut = df[col].median()
        a = df[df[col] <= cut]
        b = df[df[col] > cut]
        for src, tgt, name in ((a, b, "low_to_high"), (b, a, "high_to_low")):
            row = {"region": reg, "split_axis": axis, "direction": name,
                   "n_source": int(len(src)), "n_target": int(len(tgt)),
                   "source_positives": int(src.burned.sum()),
                   "target_positives": int(tgt.burned.sum())}
            if src.burned.nunique() < 2 or tgt.burned.nunique() < 2:
                row["skipped"] = "single_class"
                results.append(row)
                continue
            for label, feats in (("thermal", THERMAL), ("baseline", BASELINE)):
                m = build(feats).fit(*_guard(src[feats], src.burned))
                p = m.predict_proba(tgt[feats])[:, 1]
                row[f"{label}_auc"] = float(roc_auc_score(tgt.burned, p))
            results.append(row)
            print(f"{reg:20s} {axis:12s} {name:12s} "
                  f"thermal={row['thermal_auc']:.4f} baseline={row['baseline_auc']:.4f}",
                  flush=True)

ok = [r for r in results if "thermal_auc" in r]
summary = {
    "n_splits": len(ok),
    "thermal_mean": float(np.mean([r["thermal_auc"] for r in ok])),
    "thermal_min": float(np.min([r["thermal_auc"] for r in ok])),
    "thermal_max": float(np.max([r["thermal_auc"] for r in ok])),
    "baseline_mean": float(np.mean([r["baseline_auc"] for r in ok])),
    "above_0.7": int(sum(1 for r in ok if r["thermal_auc"] > 0.7)),
    "above_0.5": int(sum(1 for r in ok if r["thermal_auc"] > 0.5)),
}
print("\n=== SUMMARY ===")
for k, v in summary.items():
    print(f"  {k}: {v}")
json.dump({"splits": results, "summary": summary}, open(OUT, "w"), indent=1)
print(f"\nwrote {OUT}")
