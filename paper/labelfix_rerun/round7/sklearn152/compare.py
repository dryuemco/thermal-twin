"""Compare the frame-transfer matrix under scikit-learn 1.5.2 (this folder) with the paper's 1.9.0
output (round5/collar/aoi_frame_transfer.csv). Same script (paper/code/regen_transfer_ci.py), same
corrected inputs; only the scikit-learn/pandas/numpy versions differ (see regen_transfer_ci.log)."""
import json
from pathlib import Path
import pandas as pd
H = Path(__file__).resolve().parent
a = pd.read_csv(H / "aoi_frame_transfer.csv")
b = pd.read_csv(H.parents[1] / "round5" / "collar" / "aoi_frame_transfer.csv")
k = ["source_frame", "target_frame", "direction"]
m = a.merge(b, on=k, suffixes=("_152", "_190"))
out = {}
for fr in [("full", "full"), ("10km", "10km"), ("5km", "5km")]:
    s = m[(m.source_frame == fr[0]) & (m.target_frame == fr[1])]
    sup = lambda v: (int(s[f"ci_above_0.5_{v}"].sum()), int(s[f"ci_below_0.5_{v}"].sum()))
    out["/".join(fr)] = {
        "max_abs_diff_thermal": float((s.thermal_152 - s.thermal_190).abs().max()),
        "max_abs_diff_baseline": float((s.baseline_152 - s.baseline_190).abs().max()),
        "max_abs_diff_delta": float((s.delta_152 - s.delta_190).abs().max()),
        "mean_thermal_152_190": [float(s.thermal_152.mean()), float(s.thermal_190.mean())],
        "mean_delta_152_190": [float(s.delta_152.mean()), float(s.delta_190.mean())],
        "supported_above_below_152": sup("152"), "supported_above_below_190": sup("190")}
json.dump(out, open(H / "compare_vs_1_9_0.json", "w"), indent=1)
print(json.dumps(out, indent=1))
