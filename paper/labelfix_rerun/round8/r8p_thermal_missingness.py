"""R8p. Missing thermal values in the primary population (Section 3.5).

Share of natural-vegetation cells with at least one missing thermal channel, and the ROC-AUC of this
missingness flag against `burned` (0.5 = unrelated). Also the share among all valid cells, which is
the figure an earlier draft quoted (6 % to 58 %; Evia's is high because of sea and coast cells).
"""
import json
import sys
from pathlib import Path

from sklearn.metrics import roc_auc_score

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "paper" / "code"))
import _canonical  # noqa: E402

T = ["lst_anomaly_mean", "current_lst_mean", "current_tvdi_mean", "tvdi_difference_mean",
     "downscaled_lst_mean", "fused_lst_mean"]
out = {}
for reg in ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended", "montiferru_2021"]:
    d = _canonical.load(reg)
    v = d[d.valid_for_modeling == True]  # noqa: E712
    p = v[v.burnable_tree_shrub_grass == True]  # noqa: E712
    miss = p[T].isna().any(axis=1)
    out[reg] = {"share_primary": float(miss.mean()), "share_all_valid": float(v[T].isna().any(axis=1).mean()),
                "auc_missing_vs_burned": float(roc_auc_score(p.burned, miss))}
json.dump(out, open(HERE / "r8p_summary.json", "w"), indent=1)
print(json.dumps(out, indent=1))
