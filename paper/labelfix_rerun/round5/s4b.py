"""S4b (EXPLORATORY; not a registered diagnostic, not a prediction; one region, one event).
Split Manavgat's corrected TSG burned cells by fire phase:
  early = burned under the corrected label but NOT under the frozen label (the fire's first four days,
          DOY 209-212; 2,151 cells expected)
  late  = burned under the frozen label (DOY >= 213; 784 cells expected)
Negatives are always all unburned TSG cells (17,576).
(1) Transfer ROC-AUC for the four Manavgat-TARGET directions on each subset, thermal and baseline, from the
    official re-freeze step9b predictions (no model is refitted). CIs come from the pipeline's own
    src.step9c_cross_region_block_bootstrap.bootstrap_one_group (1000 replicates, seed 42, target-block
    resampling), with blocks of 2 cells (the pipeline's target_spatial_block_id) and 10 cells (~5 km).
(2) Signed univariate AUC of the 9 features for each subset against the same negatives, 10-cell CI, with the
    same bootstrap function (the feature is passed as the score). Plus subset medians.
Usage: s4b.py"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd
from sklearn.metrics import roc_auc_score

TT = Path(r"C:\Users\CORSAIR\projects\thermal-twin"); OFF = TT / "refreeze/manavgat_2021"; OUT = TT / "rerun_labelfix/_round5"
sys.path.insert(0, str(OFF)); sys.dont_write_bytecode = True
import src.step9c_cross_region_block_bootstrap as s9c  # noqa: E402

FEAT = ["ndvi_mean", "elevation_mean", "slope_mean", "lst_anomaly_mean", "current_lst_mean", "current_tvdi_mean",
        "tvdi_difference_mean", "downscaled_lst_mean", "fused_lst_mean"]
POP = "burnable_tree_shrub_grass"
new = pd.read_parquet(OFF / "outputs/experiments/manavgat_2021/step8a/step8a_500m_modeling_dataset.parquet")
old = pd.read_parquet(TT / "drive_new/experiments/manavgat_2021/step8a/step8a_500m_modeling_dataset.parquet",
                      columns=["row_500m", "col_500m", "burned"]).rename(columns={"burned": "burned_frozen"})
m = new.merge(old, on=["row_500m", "col_500m"], how="left", validate="one_to_one")
m = m[m.valid_for_modeling & m[POP]].copy()
m["cell"] = "r" + m.row_500m.astype(int).astype(str) + "_c" + m.col_500m.astype(int).astype(str)
m["phase"] = np.where(m.burned == 0, "neg", np.where(m.burned_frozen == 1, "late", "early"))
assert not ((m.burned == 0) & (m.burned_frozen == 1)).any(), "a frozen positive became negative"
counts = m.phase.value_counts().to_dict()
doy = m[m.phase != "neg"].groupby("phase").burn_day_of_year.describe()[["min", "50%", "max"]]
b10 = (m.row_500m // 10).astype(int).astype(str) + "_" + (m.col_500m // 10).astype(int).astype(str)
m["block10"] = b10.values
print("subset counts", counts); print(doy)

SUBSETS = {"all": ("early", "late"), "early_doy209_212": ("early",), "late_doy213plus": ("late",)}


def boot(df, block_col, seed=42):
    d = df.rename(columns={block_col: "target_spatial_block_id"}) if block_col != "target_spatial_block_id" else df
    d = d.reset_index(drop=True)
    r = s9c.bootstrap_one_group(d, np.random.default_rng(seed))
    out = {}
    for k in ("baseline_roc_auc", "thermal_roc_auc", "delta_roc_auc"):
        lo, hi, _ = s9c._percentile_ci(r[k]); out[k] = (lo, hi)
    return out, len(r)


rows = []
DIRS = {"bejis_2022": "manavgat_2021__bejis_2022", "evia_2021_extended": "manavgat_2021__evia_2021_extended",
        "montiferru_2021": "montiferru_2021__manavgat_2021", "mugla_2021": "manavgat_2021__mugla_2021"}
for src_id, folder in DIRS.items():
    direction = f"{src_id}_to_manavgat_2021"
    p = pd.read_parquet(OFF / "outputs/cross_region" / folder / "step9b/cross_region_transfer_predictions.parquet")
    p = p[(p.transfer_direction == direction) & (p.population == POP)]
    p = p.merge(m[["cell", "phase", "block10"]], left_on="target_cell_id", right_on="cell", how="inner", validate="one_to_one")
    assert len(p) == len(m), (direction, len(p), len(m))
    met = json.loads((OFF / "outputs/cross_region" / folder / "step9b/cross_region_transfer_metrics.json").read_text(encoding="utf-8"))
    for name, phases in SUBSETS.items():
        s = p[(p.phase == "neg") | p.phase.isin(phases)].copy(); s["burned"] = (s.phase != "neg").astype(int)
        row = {"direction": direction, "subset": name, "n_pos": int(s.burned.sum()), "n_neg": int((s.burned == 0).sum())}
        for fam in ("thermal", "baseline"):
            row[f"{fam}_auc"] = float(roc_auc_score(s.burned, s[f"{fam}_probability"]))
        for tag, col in (("2cell", "target_spatial_block_id"), ("10cell", "block10")):
            ci, n = boot(s[["burned", "baseline_probability", "thermal_probability", col]], col)
            for k, (lo, hi) in ci.items():
                row[f"{k}_{tag}_lo"], row[f"{k}_{tag}_hi"] = lo, hi
            row[f"valid_reps_{tag}"] = n
        rows.append(row)
    full = [r for r in rows if r["direction"] == direction and r["subset"] == "all"][0]
    print(direction, "check vs step9b thermal (all 2,935):", round(full["thermal_auc"], 6))
tr = pd.DataFrame(rows); tr.to_csv(OUT / "s4b_phase_transfer_auc.csv", index=False)

# (2) univariate signed AUC per subset (10-cell CI); feature passed as both score columns
uni = []
for name, phases in SUBSETS.items():
    s = m[(m.phase == "neg") | m.phase.isin(phases)].copy(); s["burned"] = (s.phase != "neg").astype(int)
    for f in FEAT:
        d = pd.DataFrame({"burned": s.burned.values, "x": s[f].values, "block10": s.block10.values}).dropna()
        # step9c's metric helper also computes a Brier score, which needs scores in [0, 1]; the feature is
        # passed as its rank/(n+1), an order-preserving map, so every AUC (and bootstrap AUC) is unchanged.
        d["thermal_probability"] = d["baseline_probability"] = d.x.rank(method="average") / (len(d) + 1)
        a = float(roc_auc_score(d.burned, d.thermal_probability)); ci, n = boot(d, "block10")
        lo, hi = ci["thermal_roc_auc"]
        uni.append({"subset": name, "feature": f, "signed_auc": a, "ci10_lo": lo, "ci10_hi": hi, "valid_reps": n,
                    "supported": (lo > 0.5) or (hi < 0.5),
                    "median_burned_subset": float(s.loc[s.burned == 1, f].median()), "median_unburned": float(s.loc[s.burned == 0, f].median())})
un = pd.DataFrame(uni); un.to_csv(OUT / "s4b_phase_univariate_auc.csv", index=False)
json.dump({"counts": {k: int(v) for k, v in counts.items()}, "doy_by_phase": doy.to_dict(),
           "note": "Exploratory; one region, one event; not a registered diagnostic; mechanism proposal only."},
          open(OUT / "s4b_meta.json", "w"), indent=1, default=float)
pd.set_option("display.width", 250)
print(tr[["direction", "subset", "n_pos", "thermal_auc", "thermal_roc_auc_2cell_lo", "thermal_roc_auc_2cell_hi", "thermal_roc_auc_10cell_lo",
          "thermal_roc_auc_10cell_hi", "baseline_auc", "baseline_roc_auc_10cell_lo", "baseline_roc_auc_10cell_hi"]].round(3).to_string(index=False))
print(un.pivot(index="feature", columns="subset", values="signed_auc").round(3).to_string())
