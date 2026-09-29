"""R8m. Effect of a second burned-area product (VIIRS VNP64A1) and of terrain aspect.

Input: r8k_cells.csv.gz (built by r8k) and the released modelling datasets. Primary population and
all model settings are unchanged.
  Labels: agreement of VNP64A1 and MCD64A1 burned cells (Jaccard index, cells burned in one product
  only); the within-region thermal gain (10-cell blocks); the raw transfer matrix with VNP64A1 labels
  (both feature sets); signed elevation AUC per region under both labels.
  Aspect: northness and eastness (cell means of cos and sin of aspect) added to both feature sets;
  within-region gain (10-cell blocks); signed LST AUC within northness deciles.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "paper" / "code"))
import ems_inference_common as E  # noqa: E402

E.N_JOBS = 8
REG = E.REGIONS
TH, BA = E.THERMAL, E.BASELINE
ASP = ["northness", "eastness"]
K = pd.read_csv(HERE / "r8k_cells.csv.gz")


def load(reg):
    d = E.C.load(reg)
    d = d[(d.valid_for_modeling == True) & (d.burnable_tree_shrub_grass == True)]  # noqa: E712
    return d.merge(K[K.region == reg], on=["row_500m", "col_500m"], how="left").reset_index(drop=True)


def strat(s, feat, by, nbin=10):
    s = s[[feat, by, "burned"]].dropna()
    s = s.assign(bin=pd.qcut(s[by], nbin, labels=False, duplicates="drop"))
    num = den = 0.0
    for _, g in s.groupby("bin"):
        if g.burned.nunique() < 2:
            continue
        w = (g.burned == 1).sum() * (g.burned == 0).sum()
        num += roc_auc_score(g.burned, g[feat]) * w
        den += w
    return num / den


out = {"regions": {}}
data_mcd, data_vnp = {}, {}
for reg in REG:
    d = load(reg)
    m, v = d.burned == 1, d.vnp_burned == 1
    info = {"cells": int(len(d)), "mcd_burned": int(m.sum()), "vnp_burned": int(v.sum()),
            "both": int((m & v).sum()), "mcd_only": int((m & ~v).sum()), "vnp_only": int((~m & v).sum()),
            "jaccard": float((m & v).sum() / (m | v).sum()),
            "elevation_auc_mcd": float(roc_auc_score(m, d.elevation_mean)),
            "elevation_auc_vnp": float(roc_auc_score(v, d.elevation_mean)),
            "lst_auc_raw": float(roc_auc_score(m, d.current_lst_mean.fillna(d.current_lst_mean.median()))),
            "lst_auc_within_northness": float(strat(d, "current_lst_mean", "northness"))}
    dv = d.copy()
    dv["burned"] = dv.vnp_burned.astype(int)
    data_mcd[reg], data_vnp[reg] = d, dv
    for tag, dd in (("mcd", d), ("vnp", dv)):
        th = roc_auc_score(dd.burned, E.blocked_oof(dd, TH, 10))
        ba = roc_auc_score(dd.burned, E.blocked_oof(dd, BA, 10))
        info[f"within_{tag}"] = {"thermal": th, "baseline": ba, "gain": th - ba}
    th = roc_auc_score(d.burned, E.blocked_oof(d, TH + ASP, 10))
    ba = roc_auc_score(d.burned, E.blocked_oof(d, BA + ASP, 10))
    info["within_with_aspect"] = {"thermal": th, "baseline": ba, "gain": th - ba}
    out["regions"][reg] = info
    print(reg, json.dumps(info, default=float), flush=True)

rows = []
for tag, D in (("mcd", data_mcd), ("vnp", data_vnp)):
    fits = {s: {lbl: E.fit(fe, D[s]) for lbl, fe in (("thermal", TH), ("baseline", BA))} for s in REG}
    for s in REG:
        for t in REG:
            if s == t:
                continue
            r = {"labels": tag, "direction": f"{s}_to_{t}"}
            for lbl, fe in (("thermal", TH), ("baseline", BA)):
                r[lbl] = float(roc_auc_score(D[t].burned, fits[s][lbl].predict_proba(D[t][fe])[:, 1]))
            r["delta"] = r["thermal"] - r["baseline"]
            rows.append(r)
T = pd.DataFrame(rows)
T.to_csv(HERE / "r8m_transfer_vnp_vs_mcd.csv", index=False)
ref = pd.read_csv(ROOT / "paper/labelfix_rerun/round5/collar/aoi_frame_transfer.csv")
ref = ref[(ref.source_frame == "full") & (ref.target_frame == "full")].set_index("direction")
a = T[T.labels == "mcd"].set_index("direction")
b = T[T.labels == "vnp"].set_index("direction")
out["transfer_mcd_reproduction_max_abs_diff"] = float((a.thermal - ref.thermal.reindex(a.index)).abs().max())
for tag, s in (("mcd", a), ("vnp", b)):
    out[f"transfer_{tag}"] = {"mean_thermal": float(s.thermal.mean()), "mean_baseline": float(s.baseline.mean()),
                              "mean_delta": float(s.delta.mean()), "below_chance": int((s.thermal < 0.5).sum())}
out["transfer_max_abs_change_thermal"] = float((a.thermal - b.thermal).abs().max())
out["transfer_directions_changing_side"] = [d for d in a.index if (a.thermal[d] < 0.5) != (b.thermal[d] < 0.5)]
json.dump(out, open(HERE / "r8m_summary.json", "w"), indent=1, default=float)
print(json.dumps({k: v for k, v in out.items() if k != "regions"}, indent=1))
