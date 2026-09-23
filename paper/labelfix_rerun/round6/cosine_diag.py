"""Diagnose the full-frame supported-feature cosine disagreement:
verify_collar_increment.py (+0.698 corrected, +0.805 frozen) vs conditional_similarity.mjs (+0.493 corrected,
+0.805 frozen). Recomputes verify's full-frame side with its own signed() (imported logic copied verbatim:
10-cell block bootstrap, 1000 reps, seed 42) for both labels, and compares region x feature signed AUCs, support
flags, per-direction cosines and the transfer vectors against conditional_similarity_transfer.json.
Usage: cosine_diag.py <frozen|corrected>"""
import sys, json, os
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats
from sklearn.metrics import roc_auc_score
M = Path(r"C:\Users\CORSAIR\projects\thermal-twin-main\paper"); R5 = Path(__file__).parent
arm = sys.argv[1]
os.environ["THERMAL_TWIN_LABELS"] = arm
sys.path.insert(0, str(M / "code")); import _canonical  # noqa: E402
REG = ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended", "montiferru_2021"]
F9 = ["ndvi_mean", "elevation_mean", "slope_mean", "lst_anomaly_mean", "current_lst_mean", "current_tvdi_mean",
      "tvdi_difference_mean", "downscaled_lst_mean", "fused_lst_mean"]


def signed(sub, f, seed=42, NB=1000):  # verbatim logic of verify_collar_increment.signed
    ok = sub[f].notna(); y, x = sub.burned[ok].to_numpy(), sub[f][ok].to_numpy()
    blk = ((sub.row_500m // 10).astype(str) + "_" + (sub.col_500m // 10).astype(str))[ok].to_numpy()
    pt = roc_auc_score(y, x); rng = np.random.default_rng(seed); u = np.unique(blk)
    idx = {b: np.where(blk == b)[0] for b in u}; out = []
    for _ in range(NB):
        i = np.concatenate([idx[b] for b in rng.choice(u, len(u), replace=True)])
        if len(np.unique(y[i])) > 1: out.append(roc_auc_score(y[i], x[i]))
    lo, hi = np.percentile(out, 2.5), np.percentile(out, 97.5)
    return pt, lo, hi


rows = []
for r in REG:
    d = _canonical.load(r); d = d[(d.valid_for_modeling == True) & (d.burnable_tree_shrub_grass == True)].reset_index(drop=True)
    for f in F9:
        pt, lo, hi = signed(d, f); rows.append({"region": r, "feature": f, "v_auc": pt, "v_lo": lo, "v_hi": hi, "n_burned": int(d.burned.sum())})
V = pd.DataFrame(rows); V["v_sup"] = (V.v_lo > 0.5) | (V.v_hi < 0.5)
cs = json.load(open(R5 / f"out_{'control' if arm == 'frozen' else 'official'}/conditional_similarity_transfer.json"))
S = []
for r, feats in cs["signed_auc_by_region"].items():
    for f, v in feats.items():
        S.append({"region": r, "feature": f, "c_auc": v["auc"], "c_lo": v["lo"], "c_hi": v["hi"]})
C = pd.DataFrame(S); C["c_sup"] = (C.c_lo > 0.5) | (C.c_hi < 0.5)
J = V.merge(C, on=["region", "feature"])
J["auc_diff"] = (J.v_auc - J.c_auc).abs(); J["flag_disagree"] = J.v_sup != J.c_sup
print(f"[{arm}] n_burned by region:", V.groupby("region").n_burned.first().to_dict())
print(f"[{arm}] max |signed AUC verify - condsim| = {J.auc_diff.max():.2e}; support-flag disagreements: {int(J.flag_disagree.sum())}")
print(J[J.flag_disagree | (J.auc_diff > 1e-6)][["region", "feature", "v_auc", "c_auc", "v_lo", "v_hi", "c_lo", "c_hi", "v_sup", "c_sup"]].round(4).to_string(index=False))
# per-direction cosines and transfer vectors
pdirs = pd.DataFrame(cs["per_direction"])
tv_v = pd.read_csv((M / "labelfix_rerun/round3" if arm == "corrected" else M) / "baseline_vs_thermal_transfer.csv").set_index("direction").thermal_roc
print(f"[{arm}] condsim per_direction columns:", [c for c in pdirs.columns if "transfer" in c or "auc" in c.lower()][:6])
J.to_csv(R5 / f"cosine_diag_{arm}_signed.csv", index=False)
