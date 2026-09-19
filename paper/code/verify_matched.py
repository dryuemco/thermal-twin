"""
Independent check of the two numbers a referee's matched analysis turns on.

CHECK 1, the matched distance test. Score the IDENTICAL held-out scar cells with
(C) a model fitted on the rest of the same region and (D) models fitted on each
foreign region. If C and D agree, distance independence is established on a
matched comparison rather than by setting an unmatched 0.552 beside 0.541.

CHECK 2, the matched seen-fire comparator. The manuscript compares 0.552 against
a region-wide blocked-CV 0.797, but those are different evaluation sets: the
scar-control cells are 62 per cent burned with every negative fire-adjacent.
Score a model that HAS the scar in its training data on exactly the scar-control
cells, and the comparison becomes like for like.

Read-only. Written independently of the referee's script.
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
from sklearn.model_selection import StratifiedGroupKFold
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
KM = 0.45
BUF = 2


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
    cell_lab = lab[rr, cc]
    sizes = pd.Series(cell_lab[df.burned.to_numpy() == 1]).value_counts()
    for s in [int(x) for x in sizes[sizes >= 50].index if x != 0]:
        m = np.zeros_like(g); m[lab == s] = 1
        held = ndimage.binary_dilation(m, iterations=max(1, round(BUF / KM)))[rr, cc]
        tgt, src = df[held], df[~held]
        if tgt.burned.nunique() < 2:
            continue
        prev = float(tgt.burned.mean())

        # C: same region, scar unseen
        c_auc = np.nan
        if src.burned.nunique() >= 2:
            mdl = build().fit(*_guard(src[TH], src.burned))
            c_auc = roc_auc_score(tgt.burned, mdl.predict_proba(tgt[TH])[:, 1])

        # D: foreign regions, same target cells
        ds = []
        for o in REGIONS:
            if o == reg:
                continue
            od = data[o]
            mdl = build().fit(*_guard(od[TH], od.burned))
            ds.append(roc_auc_score(tgt.burned, mdl.predict_proba(tgt[TH])[:, 1]))
        d_auc = float(np.mean(ds))

        # B: a model that HAS the scar, scored on the same cells, via blocked OOF
        blk = (df.row_500m // 10).astype(str) + "_" + (df.col_500m // 10).astype(str)
        oof = np.full(len(df), np.nan)
        skf = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)
        for tr_i, te_i in skf.split(df[TH], df.burned, groups=blk):
            mdl = build().fit(*_guard(df.iloc[tr_i][TH], df.iloc[tr_i].burned))
            oof[te_i] = mdl.predict_proba(df.iloc[te_i][TH])[:, 1]
        b_auc = roc_auc_score(tgt.burned, oof[held])
        a_auc = roc_auc_score(df.burned, oof)

        rows.append(dict(region=reg, scar=s, n=int(len(tgt)), prevalence=round(prev, 3),
                         A_region_blocked=round(a_auc, 4), B_seen_same_cells=round(b_auc, 4),
                         C_unseen_same_region=round(c_auc, 4), D_foreign=round(d_auc, 4)))
        print(f"{reg:20s} scar {s:3d}  n={len(tgt):5d} prev={prev:.2f}  "
              f"A={a_auc:.3f}  B={b_auc:.3f}  C={c_auc:.3f}  D={d_auc:.3f}", flush=True)

df = pd.DataFrame(rows)
print("\n=== MATCHED COMPARISONS, 2 km buffer, all on identical cells ===")
for k, lbl in [("A_region_blocked", "A  region-wide blocked CV (different cells)"),
               ("B_seen_same_cells", "B  blocked CV, scar SEEN, scar cells only"),
               ("C_unseen_same_region", "C  scar UNSEEN, same region"),
               ("D_foreign", "D  foreign region, 306-2802 km")]:
    v = df[k].dropna()
    se = v.std(ddof=1) / np.sqrt(len(v))
    print(f"  {lbl:46s} {v.mean():.4f}  [{v.mean()-1.96*se:.3f}, {v.mean()+1.96*se:.3f}]  n={len(v)}")
for a, b, lbl in [("B_seen_same_cells", "C_unseen_same_region", "B - C  fire-specific residual"),
                  ("C_unseen_same_region", "D_foreign", "C - D  distance effect")]:
    d = (df[a] - df[b]).dropna()
    se = d.std(ddof=1) / np.sqrt(len(d))
    print(f"  {lbl:46s} {d.mean():+.4f}  [{d.mean()-1.96*se:+.3f}, {d.mean()+1.96*se:+.3f}]")
df.to_json(f"{STAGING}/../verify_matched.json", orient="records", indent=1)
