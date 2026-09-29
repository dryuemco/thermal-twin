"""Round 7h (2026-09-29): the Section S1.18 distance table on the corrected label, summarised from
labelfix_rerun/round3/distance_curve.json (half-region models, target cells binned by separation;
unweighted means over bins, as the section defines them). Output: round7/r7h_distance_curve.csv
"""
import json
from pathlib import Path

import pandas as pd

H = Path(__file__).resolve().parent
d = json.load(open(H.parent / "round3" / "distance_curve.json", encoding="utf-8"))
w = pd.DataFrame(d["within"])
w = w[w.auc.notna()]
t = (w.groupby(["bin_lo_km", "bin_hi_km"])
     .agg(bins=("auc", "size"), mean_auc=("auc", "mean"), min_pos=("positives", "min"), max_pos=("positives", "max"))
     .reset_index())
c = pd.DataFrame(d["cross"])
col = "auc" if "auc" in c.columns else [k for k in c.columns if "auc" in k][0]
t.loc[len(t)] = {"bin_lo_km": "cross", "bin_hi_km": "region", "bins": len(c), "mean_auc": c[col].mean(),
                 "min_pos": None, "max_pos": None}
t.to_csv(H / "r7h_distance_curve.csv", index=False)
print(t.round(3).to_string())
print("positives per bin range:", int(w.positives.min()), int(w.positives.max()))
