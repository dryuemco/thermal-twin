"""S4a: is Manavgat still the outlier? Signed univariate AUC (9 features, 10-cell ~5 km spatial-block bootstrap
CI, Step9G) for all five regions; Manavgat under the frozen label (control tree) and the corrected label
(official re-freeze tree). Plus Manavgat's mean raw transfer as a source over its four modern directions.
Reads only Step9G / Step10 outputs; computes nothing new. Usage: s4a.py"""
import json
from pathlib import Path
import pandas as pd
TT = Path(r"C:\Users\CORSAIR\projects\thermal-twin"); OUT = TT / "rerun_labelfix/_round5"
S9G = "outputs/diagnostics/step9g_univariate_feature_auc_direction_reversal"
TREES = {"frozen": TT / "refreeze/_control_frozenlabel", "corrected": TT / "refreeze/manavgat_2021"}
PAIR_FOR = {"manavgat_2021": "manavgat_2021__bejis_2022", "bejis_2022": "manavgat_2021__bejis_2022",
            "mugla_2021": "manavgat_2021__mugla_2021", "evia_2021_extended": "manavgat_2021__evia_2021_extended",
            "montiferru_2021": "montiferru_2021__manavgat_2021"}
FEAT = ["ndvi_mean", "elevation_mean", "slope_mean", "lst_anomaly_mean", "current_lst_mean", "current_tvdi_mean",
        "tvdi_difference_mean", "downscaled_lst_mean", "fused_lst_mean"]
rows = []
for arm, tree in TREES.items():
    for reg, pair in PAIR_FOR.items():
        d = pd.read_csv(tree / S9G / pair / "step9g_univariate_auc_by_region.csv")
        d = d[d.experiment_id == reg]
        for _, r in d.iterrows():
            rows.append({"arm": arm, "region": reg, "feature": r.feature, "auc": r.raw_univariate_auc, "ci_low": r.auc_ci_low,
                         "ci_high": r.auc_ci_high, "n_burned": r.n_burned_complete, "burned_median": r.burned_median, "unburned_median": r.unburned_median, "source_pair": pair})
df = pd.DataFrame(rows)
df["side"] = df.auc.map(lambda a: "+" if a > 0.5 else "-")
df["supported"] = (df.ci_low > 0.5) | (df.ci_high < 0.5)
df.to_csv(OUT / "s4a_signed_auc_long.csv", index=False)
# outlier test per feature: does Manavgat sit on the opposite side of 0.5 from ALL four other regions?
res = []
for f in FEAT:
    for arm in TREES:
        m = df[(df.arm == arm) & (df.region == "manavgat_2021") & (df.feature == f)].iloc[0]
        o = df[(df.arm == "corrected") & (df.region != "manavgat_2021") & (df.feature == f)]  # others identical in both arms
        others_sides = sorted(set(o.side)); alone = len(others_sides) == 1 and others_sides[0] != m.side
        res.append({"feature": f, "arm": arm, "manavgat_auc": round(m.auc, 3), "manavgat_ci": f"[{m.ci_low:.3f}, {m.ci_high:.3f}]",
                    "manavgat_supported": bool(m.supported), "others_auc_range": f"{o.auc.min():.3f}-{o.auc.max():.3f}",
                    "others_sides": "".join(others_sides), "manavgat_alone_on_opposite_side": alone})
pd.DataFrame(res).to_csv(OUT / "s4a_outlier_by_feature.csv", index=False)
# others identical across arms (label of other regions unchanged): G2-style check
chk = df[df.region != "manavgat_2021"].pivot_table(index=["region", "feature"], columns="arm", values="auc")
g2 = float((chk.frozen - chk.corrected).abs().max())
# Manavgat as source: mean raw thermal transfer over its 4 modern directions
src = {}
for arm, csv in (("frozen", "matrix8_frozen.csv"), ("corrected", "matrix8_official.csv")):
    m = pd.read_csv(TT / "refreeze/_runners" / csv)
    s = m[m.direction.str.startswith("manavgat_2021_to_")]
    src[arm] = {"raw_thermal_mean": round(float(s.raw_thermal_roc.mean()), 4), "raw_baseline_mean": round(float(s.raw_baseline_roc.mean()), 4),
                "per_direction": dict(zip(s.direction, s.raw_thermal_roc.round(4)))}
json.dump({"g2_other_regions_max_abs_diff": g2, "manavgat_as_source": src}, open(OUT / "s4a_summary.json", "w"), indent=1)
print(pd.DataFrame(res).to_string(index=False)); print("G2 other regions max|diff|", g2); print(json.dumps(src, indent=1))
