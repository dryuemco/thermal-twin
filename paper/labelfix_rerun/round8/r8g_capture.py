"""R8g. Capture metric for transfer (reviewer 3, M6): the share of a target's burned cells that falls
in the 10 % and 20 % highest-scored cells. A random ranking captures 10 % and 20 %.

Inputs: per-cell seed-42 predictions on the study areas as drawn (r8a_preds_full_seed42.npz, which
reproduce the published transfer matrix exactly) and the within-region capture from r8b_summary.json.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
P = np.load(HERE / "r8a_preds_full_seed42.npz")
REG = ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended", "montiferru_2021"]


def capture(y, s, q):
    o = np.argsort(-s, kind="stable")
    k = int(round(q * len(s)))
    return float(y[o[:k]].sum() / y.sum())


rows = []
for src in REG:
    for tgt in REG:
        if src == tgt:
            continue
        y = P[f"labels__{tgt}"]
        r = {"direction": f"{src}_to_{tgt}"}
        for lbl in ("thermal", "baseline"):
            s = P[f"{src}_to_{tgt}__{lbl}"]
            r[f"{lbl}_top10"] = capture(y, s, 0.10)
            r[f"{lbl}_top20"] = capture(y, s, 0.20)
        rows.append(r)
T = pd.DataFrame(rows)
T.to_csv(HERE / "r8g_capture_transfer.csv", index=False)
W = json.load(open(HERE / "r8b_summary.json"))["within"]
wf = [w for w in W if w["frame"] == "full"]
summary = {
    "transfer_thermal_top10_mean": float(T.thermal_top10.mean()),
    "transfer_thermal_top20_mean": float(T.thermal_top20.mean()),
    "transfer_thermal_top10_range": [float(T.thermal_top10.min()), float(T.thermal_top10.max())],
    "transfer_thermal_top10_below_random": int((T.thermal_top10 < 0.10).sum()),
    "transfer_thermal_top20_below_random": int((T.thermal_top20 < 0.20).sum()),
    "transfer_baseline_top10_mean": float(T.baseline_top10.mean()),
    "within_thermal_top10": {w["region"]: w["capture_thermal"]["top10"] for w in wf},
    "within_thermal_top20": {w["region"]: w["capture_thermal"]["top20"] for w in wf},
    "within_thermal_top10_mean": float(np.mean([w["capture_thermal"]["top10"] for w in wf])),
    "within_thermal_top20_mean": float(np.mean([w["capture_thermal"]["top20"] for w in wf])),
}
json.dump(summary, open(HERE / "r8g_summary.json", "w"), indent=1)
print(json.dumps(summary, indent=1))
