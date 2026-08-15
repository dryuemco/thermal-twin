"""
Is the A-to-B drop caused by prevalence, or by the composition of the negatives?

The manuscript claims the latter, on the theoretical ground that ROC-AUC does not
depend on class balance at fixed class-conditional distributions. A referee is
right that the claim needs a control rather than an assertion, and the control is
cheap: take the SAME fitted model and the SAME predictions, and score them on

  A   the whole region
  A'  a random region subsample matched to the scar area's burned fraction
  B   the scar area, whose negatives are all fire-adjacent

If prevalence were the cause, A' would fall to B. If the negative pool is the
cause, A' stays at A and only B falls.

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
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

_R="repo/outputs/experiments/{}/step8a/step8a_500m_modeling_dataset.parquet"
_F="repo/outputs/experiments/mugla_2021/step8a/step8a/step8a_500m_modeling_dataset.parquet"
def _path(reg): return _F if reg=="mugla_2021" else _R.format(reg)
OUTJSON = sys.argv[1]
REGIONS = ["manavgat_2021", "bejis_2022", "mugla_2021",
           "evia_2021_extended", "montiferru_2021"]
TH = ["ndvi_mean", "elevation_mean", "slope_mean", "landcover_dominant",
      "lst_anomaly_mean", "current_lst_mean", "current_tvdi_mean",
      "tvdi_difference_mean", "downscaled_lst_mean", "fused_lst_mean"]
CAT = "landcover_dominant"
KM, BUF, MIN_SCAR, DRAWS = 0.45, 2, 50, 20
RNG = np.random.default_rng(42)


def build():
    num = [f for f in TH if f != CAT]
    tr = [("num", Pipeline([("imputer", SimpleImputer(strategy="median"))]), num),
          ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                            ("onehot", OneHotEncoder(handle_unknown="ignore"))]), [CAT])]
    return Pipeline([("preprocess", ColumnTransformer(tr)),
                     ("clf", RandomForestClassifier(n_estimators=300, min_samples_leaf=3,
                                                    class_weight="balanced",
                                                    random_state=42, n_jobs=-1))])


def load(reg):
    d = pd.read_parquet(_path(reg),
                        columns=["burned", "valid_for_modeling", "burnable_tree_shrub_grass",
                                 "row_500m", "col_500m"] + TH)
    return d[(d.valid_for_modeling == True) & (d.burnable_tree_shrub_grass == True)].reset_index(drop=True)  # noqa: E712


rows = []
for reg in REGIONS:
    df = load(reg)
    blk = (df.row_500m // 10).astype(str) + "_" + (df.col_500m // 10).astype(str)
    oof = np.full(len(df), np.nan)
    for tr_i, te_i in StratifiedGroupKFold(5, shuffle=True, random_state=42).split(
            df[TH], df.burned, groups=blk):
        oof[te_i] = build().fit(df.iloc[tr_i][TH], df.iloc[tr_i].burned) \
            .predict_proba(df.iloc[te_i][TH])[:, 1]
    a_auc = roc_auc_score(df.burned, oof)

    r0, c0 = df.row_500m.min(), df.col_500m.min()
    H, W = int(df.row_500m.max() - r0) + 1, int(df.col_500m.max() - c0) + 1
    g = np.zeros((H, W), np.uint8)
    rr = (df.row_500m - r0).to_numpy().astype(int)
    cc = (df.col_500m - c0).to_numpy().astype(int)
    g[rr[df.burned == 1], cc[df.burned == 1]] = 1
    lab, _ = ndimage.label(g, structure=np.ones((3, 3)))
    cl = lab[rr, cc]
    sizes = pd.Series(cl[df.burned.to_numpy() == 1]).value_counts()
    y = df.burned.to_numpy()
    pos_all, neg_all = np.where(y == 1)[0], np.where(y == 0)[0]

    for s in [int(x) for x in sizes[sizes >= MIN_SCAR].index if x != 0]:
        m = np.zeros_like(g); m[lab == s] = 1
        held = ndimage.binary_dilation(m, iterations=max(1, round(BUF / KM)))[rr, cc]
        if df.burned[held].nunique() < 2:
            continue
        b_auc = roc_auc_score(df.burned[held], oof[held])
        npos, nneg = int(y[held].sum()), int((~y[held].astype(bool)).sum())
        prev = npos / (npos + nneg)

        # A': random region cells at the SAME prevalence, negatives drawn from anywhere
        draws = []
        for _ in range(DRAWS):
            if npos > len(pos_all) or nneg > len(neg_all):
                continue
            pi = RNG.choice(pos_all, npos, replace=False)
            ni = RNG.choice(neg_all, nneg, replace=False)
            idx = np.concatenate([pi, ni])
            draws.append(roc_auc_score(y[idx], oof[idx]))
        # NEGATIVES ONLY: region positives at the same count, the scar's own negatives
        neg_scar = np.where(held & (y == 0))[0]
        dn = []
        for _ in range(DRAWS):
            if npos > len(pos_all): continue
            pi = RNG.choice(pos_all, npos, replace=False)
            idx = np.concatenate([pi, neg_scar])
            dn.append(roc_auc_score(y[idx], oof[idx]))
        # POSITIVES ONLY: the scar's own positives, region negatives at the same count
        pos_scar = np.where(held & (y == 1))[0]
        dp = []
        for _ in range(DRAWS):
            if nneg > len(neg_all): continue
            ni = RNG.choice(neg_all, nneg, replace=False)
            idx = np.concatenate([pos_scar, ni])
            dp.append(roc_auc_score(y[idx], oof[idx]))
        rows.append({"region": reg, "scar": s, "prevalence": round(prev, 3),
                     "A_region": round(a_auc, 4),
                     "A_prime_prevalence_matched": round(float(np.mean(draws)), 4),
                     "C_negatives_only": round(float(np.mean(dn)), 4) if dn else None,
                     "D_positives_only": round(float(np.mean(dp)), 4) if dp else None,
                     "B_scar_area": round(b_auc, 4)})
        print(f"{reg:20s} scar {s:3d}  prev={prev:.2f}  A={a_auc:.3f}  "
              f"A'={np.mean(draws):.3f}  B={b_auc:.3f}", flush=True)

d = pd.DataFrame(rows)
print("\n=== IS THE DROP PREVALENCE, OR THE NEGATIVE POOL? ===")
for c, lbl in [("A_region", "A   whole region"),
               ("A_prime_prevalence_matched", "A'  random cells, scar's prevalence"),
               ("B_scar_area", "B   scar area, fire-adjacent negatives")]:
    print(f"  {lbl:42s} {d[c].mean():.4f}")
for a, b, lbl in [("A_region", "A_prime_prevalence_matched", "A - A'  prevalence alone"),
                  ("C_negatives_only", "A_prime_prevalence_matched", "C - A'  NEGATIVE pool alone"),
                  ("D_positives_only", "A_prime_prevalence_matched", "D - A'  POSITIVE pool alone"),
                  ("B_scar_area", "A_prime_prevalence_matched", "B - A'  both pools (published)")]:
    v = (d[a] - d[b]); se = v.std(ddof=1) / np.sqrt(len(v))
    t = stats.t.ppf(0.975, len(v) - 1) * se
    print(f"  {lbl:42s} {v.mean():+.4f}  [{v.mean()-t:+.4f}, {v.mean()+t:+.4f}]")
d.to_json(OUTJSON, orient="records", indent=1)
