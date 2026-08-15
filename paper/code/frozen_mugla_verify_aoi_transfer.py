"""
Stage 2 of the Referee Q check: does the transfer matrix survive frame equalisation?

Q claims that restricting both source and target populations to cells within a
fixed collar of burned area - which drops zero positives and only far-field
negatives - lifts mean target AUC from 0.541 (14/20 above chance) to 0.613
(19/20), and that the six anti-predictive directions largely disappear.

If true, the paper's "six directions anti-predictive with interval support"
claim does not survive, and the transfer null must be restated on an equalised
frame. The qualitative claim (0.61 against within-region ~0.87) would survive.

Reference arm reproduces the frozen full-frame matrix as a correctness check.
Read-only with respect to repo/.
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

OUT = sys.argv[1]
REGIONS = ["manavgat_2021", "bejis_2022", "mugla_2021",
           "evia_2021_extended", "montiferru_2021"]
_R = "repo/outputs/experiments/{}/step8a/step8a_500m_modeling_dataset.parquet"
_FROZEN_MUGLA = "repo/outputs/experiments/mugla_2021/step8a/step8a/step8a_500m_modeling_dataset.parquet"
class _Root(str):
    def format(self, reg):
        return _FROZEN_MUGLA if reg == "mugla_2021" else _R.format(reg)
ROOT = _Root(_R)
TH = ["ndvi_mean", "elevation_mean", "slope_mean", "landcover_dominant",
      "lst_anomaly_mean", "current_lst_mean", "current_tvdi_mean",
      "tvdi_difference_mean", "downscaled_lst_mean", "fused_lst_mean"]
BASE = ["ndvi_mean", "elevation_mean", "slope_mean", "landcover_dominant"]
CAT = "landcover_dominant"
CELL_KM, SEED = 0.45, 42


def build(feats):
    num = [f for f in feats if f != CAT]
    tr = [("num", Pipeline([("imputer", SimpleImputer(strategy="median"))]), num),
          ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                            ("onehot", OneHotEncoder(handle_unknown="ignore"))]), [CAT])]
    return Pipeline([("preprocess", ColumnTransformer(tr)),
                     ("clf", RandomForestClassifier(n_estimators=300, min_samples_leaf=3,
                                                    class_weight="balanced",
                                                    random_state=SEED, n_jobs=-1))])


def load(reg):
    d = pd.read_parquet(ROOT.format(reg))
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


data = {r: load(r) for r in REGIONS}
for r in REGIONS:
    d = data[r]
    print(f"{r:22s} full n={len(d):6d}  <=10km n={int((d.dist_km<=10).sum()):6d}  "
          f"positives kept {int(d.burned[d.dist_km<=10].sum())}/{int(d.burned.sum())}", flush=True)

FRAMES = [("full", "full"), ("full", "10km"), ("10km", "full"), ("10km", "10km"), ("5km", "5km")]


def frame(d, tag):
    return d if tag == "full" else d[d.dist_km <= (10 if tag == "10km" else 5)]


rows = []
for sf, tf in FRAMES:
    fitted = {}
    for src in REGIONS:
        s = frame(data[src], sf)
        fitted[src] = {lbl: build(fe).fit(s[fe], s.burned)
                       for lbl, fe in (("thermal", TH), ("baseline", BASE))}
    for src in REGIONS:
        for tgt in REGIONS:
            if src == tgt:
                continue
            t = frame(data[tgt], tf)
            row = {"source_frame": sf, "target_frame": tf,
                   "direction": f"{src}_to_{tgt}"}
            for lbl, fe in (("thermal", TH), ("baseline", BASE)):
                row[lbl] = float(roc_auc_score(
                    t.burned, fitted[src][lbl].predict_proba(t[fe])[:, 1]))
            row["delta"] = row["thermal"] - row["baseline"]
            rows.append(row)
    sub = pd.DataFrame([r for r in rows if r["source_frame"] == sf and r["target_frame"] == tf])
    print(f"\n=== frame src={sf} tgt={tf} ===", flush=True)
    print(f"  mean thermal AUC {sub.thermal.mean():.4f}   above chance "
          f"{int((sub.thermal>0.5).sum())}/20   below {int((sub.thermal<0.5).sum())}", flush=True)
    print(f"  mean baseline AUC {sub.baseline.mean():.4f}   paired delta "
          f"{sub.delta.mean():+.4f}", flush=True)

D = pd.DataFrame(rows)
print("\n" + "=" * 74)
print("SUMMARY")
print("=" * 74)
print(f"{'src frame':>10s} {'tgt frame':>10s} {'mean AUC':>9s} {'>0.5':>6s} {'baseline':>9s} {'delta':>8s}")
for sf, tf in FRAMES:
    s = D[(D.source_frame == sf) & (D.target_frame == tf)]
    print(f"{sf:>10s} {tf:>10s} {s.thermal.mean():9.4f} {int((s.thermal>0.5).sum()):4d}/20 "
          f"{s.baseline.mean():9.4f} {s.delta.mean():+8.4f}")

ref = D[(D.source_frame == "full") & (D.target_frame == "full")]
print("\nREFERENCE ARM vs frozen values (paper Table 4: mean 0.541, 14/20):")
print(f"  reproduced mean {ref.thermal.mean():.4f}, above chance {int((ref.thermal>0.5).sum())}/20")
mb = ref[ref.direction == "manavgat_2021_to_bejis_2022"].thermal.iloc[0]
print(f"  manavgat->bejis {mb:.4f}  (frozen 0.326)")

print("\nPER-DIRECTION, full/full vs 10km/10km:")
a = D[(D.source_frame == "full") & (D.target_frame == "full")].set_index("direction").thermal
b = D[(D.source_frame == "10km") & (D.target_frame == "10km")].set_index("direction").thermal
cmp = pd.DataFrame({"full": a, "collar10": b})
cmp["change"] = cmp.collar10 - cmp.full
print(cmp.sort_values("full").round(3).to_string())
print(f"\n  directions below chance: full {int((cmp.full<0.5).sum())}, "
      f"collar10 {int((cmp.collar10<0.5).sum())}")

D.to_csv(OUT, index=False)
json.dump({"summary": [{"source_frame": sf, "target_frame": tf,
                        "mean_thermal": float(D[(D.source_frame == sf) & (D.target_frame == tf)].thermal.mean()),
                        "above_chance": int((D[(D.source_frame == sf) & (D.target_frame == tf)].thermal > 0.5).sum()),
                        "mean_baseline": float(D[(D.source_frame == sf) & (D.target_frame == tf)].baseline.mean()),
                        "mean_delta": float(D[(D.source_frame == sf) & (D.target_frame == tf)].delta.mean())}
                       for sf, tf in FRAMES]},
          open(OUT.replace(".csv", ".json"), "w"), indent=1)
print(f"\nwrote {OUT}")
