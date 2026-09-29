"""Round 7e (2026-09-29): summary tables for Sections S1.6-S1.8 and S1.14 of the Supplementary
Material, computed from the corrected-label outputs so that no summary is transcribed by hand.

Inputs (read-only): labelfix_rerun/round3/no_coord_channels.json (feature-set arms, re-run on the
corrected label in round 3) and labelfix_rerun/code/model_capacity.json (four estimators).
Output: round7/r7e_supplement_tables.json and .md.
"""
import json
from pathlib import Path

import numpy as np

H = Path(__file__).resolve().parent
LF = H.parent
nc = json.load(open(LF / "round3" / "no_coord_channels.json", encoding="utf-8"))
mc = json.load(open(LF / "code" / "model_capacity.json", encoding="utf-8"))
out, md = {}, []

# Feature-set arms (S1.6, S1.7, S1.14)
arms = ["full", "baseline_only", "anomaly_only", "absolute_only", "no_coord_channels",
        "drop_elev", "drop_anom", "drop_both"]
t = {a: np.array([d["auc"][a] for d in nc["transfers"]]) for a in arms}
w = {a: np.array([d["auc"][a] for d in nc["within"]]) for a in arms}
out["arms"] = {a: {"mean_transfer": t[a].mean(), "dirs_above_0.5": int((t[a] > 0.5).sum()),
                   "mean_within": w[a].mean()} for a in arms}
norm_minus_abs = t["anomaly_only"] - t["absolute_only"]
out["normalised_minus_absolute"] = {"mean": norm_minus_abs.mean(), "positive": int((norm_minus_abs > 0).sum()),
                                    "min": norm_minus_abs.min(), "max": norm_minus_abs.max()}
inc_full = {d["region"]: d["auc"]["full"] - d["auc"]["baseline_only"] for d in nc["within"]}
inc_nc = {d["region"]: d["auc"]["no_coord_channels"] - d["auc"]["baseline_only"] for d in nc["within"]}
out["no_coord_increment"] = {r: {"full": inc_full[r], "without": inc_nc[r], "retained": inc_nc[r] / inc_full[r]}
                             for r in inc_full}
out["no_coord_increment_mean"] = {"full": float(np.mean(list(inc_full.values()))),
                                  "without": float(np.mean(list(inc_nc.values())))}
out["feature_drop_within_cost_mean"] = {a: float(w[a].mean() - w["full"].mean()) for a in ["drop_elev", "drop_anom", "drop_both"]}
out["feature_drop_within_cost_by_region"] = {d["region"]: {a: d["delta_vs_full"][a] for a in ["drop_elev", "drop_anom", "drop_both"]}
                                             for d in nc["within"]}
out["feature_drop_within_ci_by_region"] = {d["region"]: d["delta_ci"]["drop_both"] for d in nc["within"]}

# Model capacity (S1.8)
cap = {}
for est in ["rf_canonical", "rf_shallow", "rf_leaf200", "logistic"]:
    th = np.array([d[f"{est}_thermal"] for d in mc["transfers"]])
    inc = np.array([d[f"{est}_increment"] for d in mc["transfers"]])
    wth = np.array([d[f"{est}_thermal"] for d in mc["withins"]])
    winc = np.array([d[f"{est}_increment"] for d in mc["withins"]])
    cap[est] = {"within_thermal": wth.mean(), "within_increment": winc.mean(), "transfer_thermal": th.mean(),
                "transfer_increment": inc.mean(), "above_chance": int((th > 0.5).sum())}
out["model_capacity"] = cap

json.dump(out, open(H / "r7e_supplement_tables.json", "w"), indent=1, default=float)
md.append("| Feature set | Mean transfer AUC | Directions > 0.5 | Mean within-region AUC |\n|---|---:|---:|---:|")
for a in ["baseline_only", "anomaly_only", "absolute_only", "no_coord_channels", "full"]:
    x = out["arms"][a]
    md.append(f"| {a} | {x['mean_transfer']:.4f} | {x['dirs_above_0.5']} | {x['mean_within']:.4f} |")
md.append("\n| Region | Increment, full | Without the two channels | Retained |\n|---|---:|---:|---:|")
for r, x in out["no_coord_increment"].items():
    md.append(f"| {r} | {x['full']:+.3f} | {x['without']:+.3f} | {100 * x['retained']:.0f} % |")
md.append("\n| Estimator | Within thermal | Within increment | Transfer thermal | Transfer increment | Above chance |\n|---|---:|---:|---:|---:|---:|")
for e, x in cap.items():
    md.append(f"| {e} | {x['within_thermal']:.3f} | {x['within_increment']:+.3f} | {x['transfer_thermal']:.3f} | "
              f"{x['transfer_increment']:+.3f} | {x['above_chance']} of 20 |")
(H / "r7e_supplement_tables.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print("\n".join(md))
print(json.dumps({k: out[k] for k in ["normalised_minus_absolute", "no_coord_increment_mean", "feature_drop_within_cost_mean"]}, indent=1, default=float))
