"""Does the leave-one-scar-out result depend on how the held-out patch is defined?

Section 4.3 asserts robustness "at 0.543 to 0.565 across minimum component sizes
from 25 to 200 cells and under both 4- and 8-connectivity". A referee found that
no code in this repository varies either parameter: every script hard-codes
MIN_SCAR = 50 and 8-connectivity. The claim therefore had no computation behind
it. This runs it.

Two parameters are swept on the leave-one-scar-out arm (row C of Table 2):
  minimum component size  25, 50, 100, 200 cells
  connectivity            4 (von Neumann) and 8 (Moore)

If the reported range holds, the sentence is supported and can stay. If it does
not, the sentence is withdrawn and replaced by what the sweep shows.

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
KM, BUF, SEED = 0.45, 2, 42

CONN = {8: np.ones((3, 3), dtype=int),
        4: np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=int)}


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
    return d[(d.valid_for_modeling == True) &  # noqa: E712
             (d.burnable_tree_shrub_grass == True)].reset_index(drop=True)  # noqa: E712


data = {r: load(r) for r in REG}
rows = []

for conn in (8, 4):
    for minsize in (25, 50, 100, 200):
        per_scar = []
        for reg in REG:
            df = data[reg]
            r0, c0 = int(df.row_500m.min()), int(df.col_500m.min())
            H = int(df.row_500m.max()) - r0 + 1
            W = int(df.col_500m.max()) - c0 + 1
            g = np.zeros((H, W), np.uint8)
            rr = df.row_500m.to_numpy().astype(int) - r0
            cc = df.col_500m.to_numpy().astype(int) - c0
            b = df.burned.to_numpy() == 1
            g[rr[b], cc[b]] = 1
            lab, _ = ndimage.label(g, structure=CONN[conn])
            cl = lab[rr, cc]
            sizes = pd.Series(cl[b]).value_counts()
            for s in [int(x) for x in sizes[sizes >= minsize].index if x != 0]:
                m = np.zeros_like(g)
                m[lab == s] = 1
                held = ndimage.binary_dilation(m, iterations=max(1, round(BUF / KM)))[rr, cc]
                tgt, src = df[held], df[~held]
                if tgt.burned.nunique() < 2 or src.burned.nunique() < 2:
                    continue
                mdl = build().fit(*_guard(src[TH], src.burned))
                auc = roc_auc_score(tgt.burned, mdl.predict_proba(tgt[TH])[:, 1])
                per_scar.append(auc)
                rows.append({"connectivity": conn, "min_component_cells": minsize,
                             "region": reg, "component": s, "n_target": int(len(tgt)),
                             "auc": float(auc)})
        mean = float(np.mean(per_scar)) if per_scar else np.nan
        print(f"  {conn}-conn  min {minsize:3d} cells   {len(per_scar):2d} scars   "
              f"mean row-C AUC {mean:.4f}", flush=True)

D = pd.DataFrame(rows)
print("\n" + "=" * 70)
print("DOES ROW C DEPEND ON HOW THE HELD-OUT PATCH IS DEFINED?")
print("=" * 70)
summ = D.groupby(["connectivity", "min_component_cells"]).auc.agg(["count", "mean"])
print(summ.round(4).to_string())
lo, hi = summ["mean"].min(), summ["mean"].max()
print(f"\n  range of the mean across all eight settings: {lo:.4f} to {hi:.4f}")
print(f"  manuscript claims: 0.543 to 0.565")
print(f"  published row C (min 50, 8-connectivity): 0.552")
D.to_csv(OUT, index=False)
print(f"\nwrote {OUT}")
