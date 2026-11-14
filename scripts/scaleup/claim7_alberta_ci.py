"""claim7_alberta_ci.py: 95% interval of the geographic null model's AUC on the Alberta temporal test (claim 7).

Same split as claim7_open_data.py (train 2001-2014, test 2018-2021, 10 km control buffer). The interval comes
from 2000 bootstrap resamples of the test cells, the resampling the package uses for its own Table S3, whose
intervals for the four published models are copied beside it. No paired comparison is possible because the
package's test predictions carry no cell identifiers.

Run:  <venv-step10>/python -I claim7_alberta_ci.py   (writes D:/ThermalTwin/scaleup/analysis/claim7_alberta_ci.json)
"""
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from sklearn.metrics import roc_auc_score

SCALEUP = Path(os.environ["THERMAL_TWIN_SCALEUP"])
BASE = SCALEUP / "open_data/alberta/x/Alberta_Wildfire_Reproducibility_Package"
d = pd.read_csv(BASE / "Alberta_model_inputs" / "model_ready" / "sample_metadata_model_2001_2021_buffer10km.csv")
xy = np.c_[d["col"].to_numpy() * 0.5, d["row"].to_numpy() * 0.5]
y = d.fire_label.to_numpy()
tr, te = (d.YEAR <= 2014).to_numpy(), (d.YEAR >= 2018).to_numpy()
s = -cKDTree(xy[tr][y[tr] == 1]).query(xy[te])[0]
yt = y[te]
rng = np.random.default_rng(42)
bs = []
for _ in range(2000):
    i = rng.integers(0, len(yt), len(yt))
    if yt[i].min() != yt[i].max():
        bs.append(roc_auc_score(yt[i], s[i]))
pub = pd.read_csv(BASE / "supplementary_tables" / "Table_S3_model_performance_bootstrap_CI_2018_2021.csv")
out = {"null_auc": float(roc_auc_score(yt, s)), "null_lo": float(np.percentile(bs, 2.5)), "null_hi": float(np.percentile(bs, 97.5)),
       "published": {r.Model: {"auc": r.AUC, "lo": r.AUC_95CI_lower, "hi": r.AUC_95CI_upper} for r in pub.itertuples()}}
(SCALEUP / "analysis" / "claim7_alberta_ci.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print(json.dumps(out, indent=1))
