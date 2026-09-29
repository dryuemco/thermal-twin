"""R8a. Random-forest seed replication of the transfer matrix (reviewers 1 and 2).

The published transfer numbers come from one fitted forest per source (random_state = 42). This
script refits every source model with ten seeds (42 and 1 to 9) on two frames, the study areas as
drawn and the 10 km collar, for the thermal and the baseline feature sets. Model, features,
population and frames are those of paper/code/verify_aoi_transfer.py.

Outputs (in this folder):
  r8a_seed_auc.csv        one row per seed, frame and direction: thermal, baseline, delta
  r8a_summary.json        seed-42 reproduction check, between-seed spread, seed-averaged and
                          ensemble (averaged-prediction) results, sign stability
  r8a_preds_full_seed42.npz   per-cell seed-42 predictions on the as-drawn frame (for R8g)
Run from the repository root: python paper/labelfix_rerun/round8/r8a_seed_replication.py
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import ndimage
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "paper" / "code"))
import _canonical  # noqa: E402

REGIONS = ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended", "montiferru_2021"]
TH = ["ndvi_mean", "elevation_mean", "slope_mean", "landcover_dominant",
      "lst_anomaly_mean", "current_lst_mean", "current_tvdi_mean",
      "tvdi_difference_mean", "downscaled_lst_mean", "fused_lst_mean"]
BASE = ["ndvi_mean", "elevation_mean", "slope_mean", "landcover_dominant"]
CAT = "landcover_dominant"
CELL_KM = 0.45
SEEDS = [42, 1, 2, 3, 4, 5, 6, 7, 8, 9]
FRAMES = ["full", "10km"]


def build(feats, seed):
    _canonical.assert_no_leakage(feats)
    num = [f for f in feats if f != CAT]
    tr = [("num", Pipeline([("imputer", SimpleImputer(strategy="median"))]), num),
          ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                            ("onehot", OneHotEncoder(handle_unknown="ignore"))]), [CAT])]
    return Pipeline([("preprocess", ColumnTransformer(tr)),
                     ("clf", RandomForestClassifier(n_estimators=300, min_samples_leaf=3,
                                                    class_weight="balanced",
                                                    random_state=seed, n_jobs=4))])


def load(reg):
    d = _canonical.load(reg)
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


def frame(d, tag):
    return d if tag == "full" else d[d.dist_km <= 10].reset_index(drop=True)


data = {r: load(r) for r in REGIONS}
rows, ens, preds42 = [], {}, {}
for fr in FRAMES:
    for seed in SEEDS:
        fitted = {}
        for src in REGIONS:
            s = frame(data[src], fr)
            fitted[src] = {lbl: build(fe, seed).fit(s[fe], s.burned)
                           for lbl, fe in (("thermal", TH), ("baseline", BASE))}
        for src in REGIONS:
            for tgt in REGIONS:
                if src == tgt:
                    continue
                t = frame(data[tgt], fr)
                row = {"frame": fr, "seed": seed, "direction": f"{src}_to_{tgt}"}
                for lbl, fe in (("thermal", TH), ("baseline", BASE)):
                    p = fitted[src][lbl].predict_proba(t[fe])[:, 1]
                    row[lbl] = float(roc_auc_score(t.burned, p))
                    key = (fr, row["direction"], lbl)
                    ens[key] = ens.get(key, 0) + p / len(SEEDS)
                    if fr == "full" and seed == 42:
                        preds42[f"{src}_to_{tgt}__{lbl}"] = p.astype(np.float32)
                row["delta"] = row["thermal"] - row["baseline"]
                rows.append(row)
        sub = pd.DataFrame([r for r in rows if r["frame"] == fr and r["seed"] == seed])
        print(f"frame {fr} seed {seed}: mean thermal {sub.thermal.mean():.4f} "
              f"baseline {sub.baseline.mean():.4f} delta {sub.delta.mean():+.4f}", flush=True)

D = pd.DataFrame(rows)
D.to_csv(HERE / "r8a_seed_auc.csv", index=False)
for tgt in REGIONS:
    preds42[f"labels__{tgt}"] = data[tgt].burned.to_numpy().astype(np.int8)
np.savez_compressed(HERE / "r8a_preds_full_seed42.npz", **preds42)

ref = pd.read_csv(ROOT / "paper/labelfix_rerun/round5/collar/aoi_frame_transfer.csv")
summary = {"seeds": SEEDS, "frames": {}}
for fr, tag in (("full", "full"), ("10km", "10km")):
    s = D[D.frame == fr]
    s42 = s[s.seed == 42].set_index("direction")
    r = ref[(ref.source_frame == tag) & (ref.target_frame == tag)].set_index("direction")
    repro = float((s42.thermal - r.thermal.reindex(s42.index)).abs().max())
    per_dir = s.groupby("direction").agg(th_mean=("thermal", "mean"), th_sd=("thermal", "std"),
                                         th_min=("thermal", "min"), th_max=("thermal", "max"),
                                         d_mean=("delta", "mean"), d_sd=("delta", "std"))
    side = s.assign(above=s.thermal > 0.5).groupby("direction").above.agg(["min", "max"])
    ens_rows = []
    for dname in per_dir.index:
        tgt = dname.split("_to_")[1]
        y = frame(data[tgt], fr).burned
        th = roc_auc_score(y, ens[(fr, dname, "thermal")])
        ba = roc_auc_score(y, ens[(fr, dname, "baseline")])
        ens_rows.append({"direction": dname, "thermal": th, "baseline": ba, "delta": th - ba})
    E = pd.DataFrame(ens_rows)
    by_seed = s.groupby("seed").agg(th=("thermal", "mean"), de=("delta", "mean"))
    summary["frames"][fr] = {
        "seed42_max_abs_diff_vs_published": repro,
        "mean_thermal_by_seed": {int(k): float(v) for k, v in by_seed.th.items()},
        "mean_delta_by_seed": {int(k): float(v) for k, v in by_seed.de.items()},
        "mean_thermal_range_over_seeds": [float(by_seed.th.min()), float(by_seed.th.max())],
        "mean_delta_range_over_seeds": [float(by_seed.de.min()), float(by_seed.de.max())],
        "direction_thermal_sd_median": float(per_dir.th_sd.median()),
        "direction_thermal_sd_max": float(per_dir.th_sd.max()),
        "direction_thermal_range_max": float((per_dir.th_max - per_dir.th_min).max()),
        "direction_delta_sd_median": float(per_dir.d_sd.median()),
        "direction_delta_sd_max": float(per_dir.d_sd.max()),
        "directions_changing_side_of_chance": [d for d in side.index if side.loc[d, "min"] != side.loc[d, "max"]],
        "ensemble_mean_thermal": float(E.thermal.mean()),
        "ensemble_mean_baseline": float(E.baseline.mean()),
        "ensemble_mean_delta": float(E.delta.mean()),
        "ensemble_below_chance": int((E.thermal < 0.5).sum()),
        "ensemble_per_direction": E.round(6).to_dict(orient="records"),
    }
json.dump(summary, open(HERE / "r8a_summary.json", "w"), indent=1)
print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "ensemble_per_direction"}
                  for k, v in summary["frames"].items()}, indent=1))
