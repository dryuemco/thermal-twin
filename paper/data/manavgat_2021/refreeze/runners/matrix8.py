"""The 8 modern Manavgat transfer directions (raw / z-score / CORAL; thermal and baseline) with the step10
2-cell bootstrap CIs, from an outputs root. Same extraction as rerun_labelfix/_runners/matrix.py, restricted to
the pairs that contain Manavgat. Usage: matrix8.py <outputs_root> <out_csv>"""
import sys
from pathlib import Path
import pandas as pd
PAIR = {"bejis_2022": "manavgat_2021__bejis_2022", "evia_2021_extended": "manavgat_2021__evia_2021_extended",
        "montiferru_2021": "montiferru_2021__manavgat_2021", "mugla_2021": "manavgat_2021__mugla_2021"}
METHODS = {"raw_source_only": "raw", "regionwise_zscore": "z", "coral_after_regionwise_zscore": "coral"}
root, out = Path(sys.argv[1]), Path(sys.argv[2]); rows = []
for other, folder in PAIR.items():
    d = root / "cross_region" / folder / "step10"
    m, b = pd.read_csv(d / "step10_metrics.csv"), pd.read_csv(d / "step10_bootstrap_summary.csv")
    for s, t in (("manavgat_2021", other), (other, "manavgat_2021")):
        dr = f"{s}_to_{t}"; mm, bb = m[m.direction == dr], b[b.direction == dr]
        row = {"direction": dr, "positive_count": int(mm.positive_count.iloc[0])}
        for meth, short in METHODS.items():
            for fam in ("thermal", "baseline"):
                r = mm[(mm.method == meth) & (mm.model_family == fam)]
                row[f"{short}_{fam}_roc"] = float(r.roc_auc.iloc[0])
                ser = bb[bb.series == f"roc_auc__{meth}_{fam}"]
                row[f"{short}_{fam}_lo"], row[f"{short}_{fam}_hi"] = float(ser.ci_2_5.iloc[0]), float(ser.ci_97_5.iloc[0])
        rows.append(row)
pd.DataFrame(rows).to_csv(out, index=False)
print("MATRIX8_DONE", len(rows))
