"""
Is the transfer failure a property of the predictors, or of an unregularised model?

Every number in this paper comes from one random forest: 300 trees, unlimited
depth, min_samples_leaf 3. That is the configuration most able to encode local
structure and least able to extrapolate, so "these predictors do not travel" is
entangled with "this fitted model does not travel". Holding the model fixed is
right for the internal comparisons and does not license the external claim.

Three additional estimators are run over the same twenty directions and the same
five within-region folds:

  rf_shallow   depth 6, min_samples_leaf 50   a deliberately regularised forest
  rf_leaf200   unlimited depth, leaf 200      regularisation by leaf size alone
  logistic     L2 penalised, standardised     an extrapolating linear model

If transfer stays near 0.54 across all of them, the negative result is a
property of the predictors and not of the estimator. If a regularised model
transfers better, that is a finding and the paper's framing has to change.

Read-only with respect to the repository.
"""
import json
import sys

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import _canonical


def _guard(X, y):
    """Methods 3.13: forbidden-column assertion on the exact columns passed to the model."""
    _canonical.assert_no_leakage(list(X.columns))
    return X, y


STAGING, OUT = sys.argv[1], sys.argv[2]
REGIONS = ["manavgat_2021", "bejis_2022", "mugla_2021",
           "evia_2021_extended", "montiferru_2021"]
TH = ["ndvi_mean", "elevation_mean", "slope_mean", "landcover_dominant",
      "lst_anomaly_mean", "current_lst_mean", "current_tvdi_mean",
      "tvdi_difference_mean", "downscaled_lst_mean", "fused_lst_mean"]
BASE = ["ndvi_mean", "elevation_mean", "slope_mean", "landcover_dominant"]
CAT = "landcover_dominant"
SEED = 42

CLFS = {
    "rf_canonical": lambda: RandomForestClassifier(n_estimators=300, min_samples_leaf=3,
                                                   class_weight="balanced",
                                                   random_state=SEED, n_jobs=4),
    "rf_shallow": lambda: RandomForestClassifier(n_estimators=300, max_depth=6,
                                                 min_samples_leaf=50, class_weight="balanced",
                                                 random_state=SEED, n_jobs=4),
    "rf_leaf200": lambda: RandomForestClassifier(n_estimators=300, min_samples_leaf=200,
                                                 class_weight="balanced",
                                                 random_state=SEED, n_jobs=4),
    "logistic": lambda: LogisticRegression(penalty="l2", C=1.0, max_iter=2000,
                                           class_weight="balanced", random_state=SEED),
}


def build(name, feats):
    num = [f for f in feats if f != CAT]
    steps = [("imputer", SimpleImputer(strategy="median"))]
    if name == "logistic":
        steps.append(("scale", StandardScaler()))
    tr = [("num", Pipeline(steps), num),
          ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                            ("onehot", OneHotEncoder(handle_unknown="ignore"))]), [CAT])]
    return Pipeline([("preprocess", ColumnTransformer(tr)), ("clf", CLFS[name]())])


def load(reg):
    d = _canonical.load(reg,
                        columns=["burned", "valid_for_modeling", "burnable_tree_shrub_grass",
                                 "row_500m", "col_500m"] + TH)
    return d[(d.valid_for_modeling == True) & (d.burnable_tree_shrub_grass == True)].reset_index(drop=True)  # noqa: E712


data = {r: load(r) for r in REGIONS}
transfers, withins = [], []

for src in REGIONS:
    s = data[src]
    fitted = {n: {f: build(n, feats).fit(*_guard(s[feats], s.burned))
                  for f, feats in (("thermal", TH), ("baseline", BASE))} for n in CLFS}
    print(f"fitted {src}", flush=True)
    for tgt in REGIONS:
        if tgt == src:
            continue
        t = data[tgt]
        row = {"source": src, "target": tgt}
        for n in CLFS:
            for f, feats in (("thermal", TH), ("baseline", BASE)):
                row[f"{n}_{f}"] = float(roc_auc_score(
                    t.burned, fitted[n][f].predict_proba(t[feats])[:, 1]))
            row[f"{n}_increment"] = row[f"{n}_thermal"] - row[f"{n}_baseline"]
        transfers.append(row)
        print("  -> " + tgt + "  " + "  ".join(
            f"{n}={row[n+'_thermal']:.3f}" for n in CLFS), flush=True)

for reg in REGIONS:
    df = data[reg]
    blk = (df.row_500m // 2).astype(str) + "_" + (df.col_500m // 2).astype(str)
    row = {"region": reg}
    for n in CLFS:
        for f, feats in (("thermal", TH), ("baseline", BASE)):
            oof = np.full(len(df), np.nan)
            for tr_i, te_i in StratifiedGroupKFold(5, shuffle=True, random_state=SEED).split(
                    df[feats], df.burned, groups=blk):
                oof[te_i] = build(n, feats).fit(*_guard(df.iloc[tr_i][feats], df.iloc[tr_i].burned)) \
                    .predict_proba(df.iloc[te_i][feats])[:, 1]
            row[f"{n}_{f}"] = float(roc_auc_score(df.burned, oof))
        row[f"{n}_increment"] = row[f"{n}_thermal"] - row[f"{n}_baseline"]
    withins.append(row)
    print(f"within {reg}: " + "  ".join(f"{n}={row[n+'_thermal']:.3f}" for n in CLFS), flush=True)

T, W = pd.DataFrame(transfers), pd.DataFrame(withins)
print("\n=== MODEL CAPACITY ===")
print(f"{'estimator':14s} {'within thermal':>14s} {'within incr':>12s} "
      f"{'transfer thermal':>17s} {'transfer incr':>14s} {'>0.5':>6s}")
for n in CLFS:
    print(f"{n:14s} {W[n+'_thermal'].mean():14.4f} {W[n+'_increment'].mean():+12.4f} "
          f"{T[n+'_thermal'].mean():17.4f} {T[n+'_increment'].mean():+14.4f} "
          f"{int((T[n+'_thermal'] > 0.5).sum()):5d}/20")
json.dump({"transfers": transfers, "withins": withins}, open(OUT, "w"), indent=1)
print(f"\nwrote {OUT}")
