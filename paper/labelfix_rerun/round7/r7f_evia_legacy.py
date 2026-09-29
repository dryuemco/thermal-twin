"""Round 7f (2026-09-29): Section S1.1, the legacy Evia box against the extended one, on the corrected
Manavgat label. Thermal raw transfer ROC-AUC per direction from the step9b per-cell predictions
(primary population): Manavgat pairs from the corrected pipeline tree, the others from drive_new.
Output: round7/r7f_evia_legacy.csv and .json.
"""
import hashlib
import json
import os
from pathlib import Path

import pandas as pd
from sklearn.metrics import roc_auc_score

H = Path(__file__).resolve().parent
LF = H.parent                                                        # paper/labelfix_rerun
DRIVE = H.parents[3] / "thermal-twin" / "drive_new" / "cross_region"  # projects/thermal-twin/drive_new
PAIRS = {("manavgat_2021", LF / "pipeline" / "cross_region"), ("bejis_2022", DRIVE), ("mugla_2021", DRIVE)}
rows, sha = [], {}
for other, root in sorted(PAIRS, key=lambda x: x[0]):
    for evia in ["evia_2021", "evia_2021_extended"]:
        f = root / f"{other}__{evia}" / "step9b" / "cross_region_transfer_predictions.csv"
        sha[Path(os.path.abspath(f)).as_posix().split("projects/")[-1]] = hashlib.sha256(f.read_bytes()).hexdigest()
        d = pd.read_csv(f)
        d = d[d.population == "burnable_tree_shrub_grass"]
        for direction, g in d.groupby("transfer_direction"):
            rows.append({"other": other, "evia_box": evia, "direction": direction,
                         "thermal_roc": roc_auc_score(g.burned, g.thermal_probability)})
r = pd.DataFrame(rows)
r["to_evia"] = r.direction.str.contains("_to_evia")
p = r.pivot_table(index=["other", "to_evia"], columns="evia_box", values="thermal_roc").reset_index()
p["change"] = p["evia_2021"] - p["evia_2021_extended"]
p["crosses_0.5"] = (p["evia_2021"] - 0.5) * (p["evia_2021_extended"] - 0.5) < 0
p.to_csv(H / "r7f_evia_legacy.csv", index=False)
json.dump({"inputs_sha256": sha, "max_abs_change": float(p.change.abs().max()),
           "n_crossing_chance": int(p["crosses_0.5"].sum())}, open(H / "r7f_evia_legacy.json", "w"), indent=1)
print(p.round(3).to_string())
