"""R8c. CORAL variants and a placebo control (reviewer 2, M7).

Thermal feature set, twenty ordered directions, study areas as drawn, primary population. The
transfer routine is step10/transfer.py (median imputation per region, region-wise z-score, CORAL on
the source only, random forest with the primary settings). Variants:
  coral_1e-5   the published setting (reproduction check against round5/matrix20_official.csv)
  coral_1      lambda = 1, the value of the original CORAL formulation
  coral_pc2    the six thermal channels are replaced by two principal components. The components
               are fitted, without labels, on the z-scored thermal channels of the source and applied
               to both regions; CORAL (lambda = 1e-5) then runs on the five numeric features.
  placebo      the source is recoloured to the covariance of a third region instead of the target
               (mean over the three other regions). If this also moves transfer toward chance, the
               movement is not specific to aligning with the target.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import OneHotEncoder

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "step10"))
sys.path.insert(0, str(ROOT / "paper" / "code"))
import _canonical  # noqa: E402
from adaptation import _standardize, _sym_matrix_power, adapt_numeric  # noqa: E402
from config10 import CORAL_EIGVAL_FLOOR, TRANSFER_RF_PARAMS_PRIMARY  # noqa: E402
from transfer import _impute_by_own_median  # noqa: E402

REG = ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended", "montiferru_2021"]
NUM = ["ndvi_mean", "elevation_mean", "slope_mean", "lst_anomaly_mean", "current_lst_mean",
       "current_tvdi_mean", "tvdi_difference_mean", "downscaled_lst_mean", "fused_lst_mean"]
THERM = NUM[3:]
CAT = ["landcover_dominant"]
_canonical.assert_no_leakage(NUM + CAT)


def load(r):
    d = _canonical.load(r)
    return d[(d.valid_for_modeling == True) & (d.burnable_tree_shrub_grass == True)].reset_index(drop=True)  # noqa: E712


data = {r: load(r) for r in REG}
Z = {r: _standardize(_impute_by_own_median(data[r][NUM])[0]) for r in REG}   # region-wise z-score


def coral_to(xs_z, cov_target, lam):
    d = xs_z.shape[1]
    cs = np.atleast_2d(np.cov(xs_z, rowvar=False, ddof=0)) + lam * np.eye(d)
    ct = cov_target + lam * np.eye(d)
    return xs_z @ (_sym_matrix_power(cs, -0.5, CORAL_EIGVAL_FLOOR) @ _sym_matrix_power(ct, 0.5, CORAL_EIGVAL_FLOOR))


def fit_score(xs_num, xt_num, src, tgt):
    enc = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    xs = np.hstack([xs_num, enc.fit_transform(data[src][CAT].astype("object"))])
    xt = np.hstack([xt_num, enc.transform(data[tgt][CAT].astype("object"))])
    clf = RandomForestClassifier(**TRANSFER_RF_PARAMS_PRIMARY).fit(xs, data[src].burned.astype(int))
    return float(roc_auc_score(data[tgt].burned.astype(int), clf.predict_proba(xt)[:, 1]))


def pc2(src, tgt):
    ti = [NUM.index(c) for c in THERM]
    oi = [i for i in range(len(NUM)) if i not in ti]
    zs, zt = Z[src], Z[tgt]
    vals, vecs = np.linalg.eigh(np.cov(zs[:, ti], rowvar=False, ddof=0))
    load2 = vecs[:, np.argsort(vals)[::-1][:2]]
    xs = np.hstack([zs[:, oi], zs[:, ti] @ load2])
    xt = np.hstack([zt[:, oi], zt[:, ti] @ load2])
    xs_a, xt_a = adapt_numeric(xs, xt, "coral", coral_lambda=1e-5)
    return xs_a, xt_a


rows = []
ref = pd.read_csv(ROOT / "paper/labelfix_rerun/round5/matrix20_official.csv").set_index("direction")
for src in REG:
    for tgt in REG:
        if src == tgt:
            continue
        dn = f"{src}_to_{tgt}"
        xs_raw = _impute_by_own_median(data[src][NUM])[0]
        xt_raw = _impute_by_own_median(data[tgt][NUM])[0]
        row = {"direction": dn, "raw_published": float(ref.loc[dn, "raw_thermal_roc"]),
               "coral_published": float(ref.loc[dn, "coral_thermal_roc"])}
        for lam, key in ((1e-5, "coral_1e-5"), (1.0, "coral_1")):
            xs_a, xt_a = adapt_numeric(xs_raw, xt_raw, "coral", coral_lambda=lam)
            row[key] = fit_score(xs_a, xt_a, src, tgt)
        row["coral_pc2"] = fit_score(*pc2(src, tgt), src, tgt)
        placebo = []
        for third in REG:
            if third in (src, tgt):
                continue
            ct3 = np.atleast_2d(np.cov(Z[third], rowvar=False, ddof=0))
            placebo.append(fit_score(coral_to(Z[src], ct3, 1e-5), Z[tgt], src, tgt))
        row["placebo_mean"] = float(np.mean(placebo))
        row["placebo_values"] = [round(v, 4) for v in placebo]
        rows.append(row)
        print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in row.items()}, flush=True)

P = pd.DataFrame(rows)
P.drop(columns="placebo_values").to_csv(HERE / "r8c_coral_variants.csv", index=False)


def closer(col):
    return int((np.abs(P[col] - 0.5) < np.abs(P.raw_published - 0.5)).sum())


summary = {"reproduction_max_abs_diff_coral_1e-5": float((P["coral_1e-5"] - P.coral_published).abs().max()),
           "means": {c: float(P[c].mean()) for c in ["raw_published", "coral_1e-5", "coral_1", "coral_pc2", "placebo_mean"]},
           "closer_to_chance_than_raw": {c: closer(c) for c in ["coral_1e-5", "coral_1", "coral_pc2", "placebo_mean"]},
           "below_chance": {c: int((P[c] < 0.5).sum()) for c in ["raw_published", "coral_1e-5", "coral_1", "coral_pc2", "placebo_mean"]},
           "corr_raw_distance_vs_change": {c: float(np.corrcoef(np.abs(P.raw_published - 0.5), P[c] - P.raw_published)[0, 1])
                                           for c in ["coral_1e-5", "coral_1", "coral_pc2", "placebo_mean"]}}
json.dump(summary, open(HERE / "r8c_summary.json", "w"), indent=1)
print(json.dumps(summary, indent=1))
