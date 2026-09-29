"""R8b. A within-region reference that excludes the neighbourhood of the test cells
(reviewer 1, M2), the capture metric for within-region models, and the Bejís pre-label
sensitivity (reviewers 1 and 2).

Within-region reference. Each region is divided into large blocks of 40 x 40 cells (about 20 km
north-south). Each block is held out in turn and predicted by a model fitted on the other cells.
  LOBO           training = all cells outside the held-out block
  LOBO-10km      training = cells more than 10 km from every cell of the held-out block
Predictions are pooled over blocks and scored with one ROC-AUC. A block is skipped when its
training set has fewer than 30 burned cells; skipped cells are reported. Frames: the study area as
drawn and the 10 km collar (training and test both restricted to the collar). The unbuffered 5-fold
blocked cross-validation of the paper (10-cell blocks, seed 42) is recomputed as a check.

Capture metric: share of burned cells among the 10 % and 20 % highest-scored cells, from the
blocked cross-validation predictions (random expectation 0.10 and 0.20 of the burned cells,
i.e. a capture of 10 % and 20 %).

Bejís pre-label sensitivity: the 49 cells that burned in the predictor window
(labels/r1_prelabel_cells_bejis_2022.csv) are removed; the within-region gain (2- and 10-cell
blocks) and the eight transfer directions that involve Bejís are recomputed.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import ndimage
from sklearn.metrics import roc_auc_score

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "paper" / "code"))
import ems_inference_common as E  # noqa: E402

E.N_JOBS = 8
TH, BA = E.THERMAL, E.BASELINE
LB, BUF_KM, MIN_POS = 40, 10.0, 30


def full_load(r):
    d = E.C.load(r)
    d = d[(d.valid_for_modeling == True) & (d.burnable_tree_shrub_grass == True)].reset_index(drop=True)  # noqa: E712
    r0, c0 = int(d.row_500m.min()), int(d.col_500m.min())
    H, W = int(d.row_500m.max()) - r0 + 1, int(d.col_500m.max()) - c0 + 1
    rr, cc = d.row_500m.to_numpy().astype(int) - r0, d.col_500m.to_numpy().astype(int) - c0
    bg = np.ones((H, W), dtype=bool)
    b = d.burned.to_numpy() == 1
    bg[rr[b], cc[b]] = False
    d["dist_km"] = ndimage.distance_transform_edt(bg)[rr, cc] * E.CELL_KM
    d["_r"], d["_c"], d.attrs["shape"] = rr, cc, (H, W)
    return d


def dist_to_set(d, mask):
    H, W = d.attrs["shape"]
    g = np.ones((H, W), dtype=bool)
    g[d._r.to_numpy()[mask], d._c.to_numpy()[mask]] = False
    return ndimage.distance_transform_edt(g)[d._r.to_numpy(), d._c.to_numpy()] * E.CELL_KM


def lobo(d, feats, buffer_km):
    blk = (d.row_500m // LB).astype(str) + "_" + (d.col_500m // LB).astype(str)
    pred = np.full(len(d), np.nan)
    skipped = 0
    for g in blk.unique():
        te = (blk == g).to_numpy()
        tr = ~te
        if buffer_km:
            tr &= dist_to_set(d, te) > buffer_km
        if d.burned[tr].sum() < MIN_POS or (d.burned[tr] == 0).sum() < MIN_POS:
            skipped += int(te.sum())
            continue
        pred[te] = E.fit(feats, d[tr]).predict_proba(d.loc[te, feats])[:, 1]
    ok = ~np.isnan(pred)
    y = d.burned.to_numpy()[ok]
    auc = float(roc_auc_score(y, pred[ok])) if len(np.unique(y)) == 2 else float("nan")
    return auc, {"cells_scored": int(ok.sum()), "cells_skipped": skipped,
                 "burned_scored": int(y.sum()), "burned_total": int(d.burned.sum())}


def capture(y, s):
    y, s = np.asarray(y), np.asarray(s)
    o = np.argsort(-s)
    out = {}
    for q in (0.10, 0.20):
        k = int(round(q * len(s)))
        out[f"top{int(q * 100)}"] = float(y[o[:k]].sum() / y.sum())
    return out


res = {"within": [], "bejis_prelabel": {}}
data = {r: full_load(r) for r in E.REGIONS}
for r in E.REGIONS:
    for frame in ("full", "10km"):
        d = data[r] if frame == "full" else data[r][data[r].dist_km <= 10].reset_index(drop=True)
        if frame == "10km":
            d.attrs["shape"] = data[r].attrs["shape"]
        row = {"region": r, "frame": frame}
        for lbl, fe in (("thermal", TH), ("baseline", BA)):
            oof = E.blocked_oof(d, fe, 10)
            row[f"cv10_{lbl}"] = float(roc_auc_score(d.burned, oof))
            if frame == "full":
                row[f"capture_{lbl}"] = capture(d.burned, oof)
            for buf, tag in ((0, "lobo"), (BUF_KM, "lobo10km")):
                a, info = lobo(d, fe, buf)
                row[f"{tag}_{lbl}"] = a
                row[f"{tag}_{lbl}_info"] = info
        res["within"].append(row)
        print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in row.items() if "info" not in k}, flush=True)

# shortfall of collar transfer against the buffered collar reference, by target
A = pd.read_csv(ROOT / "paper/labelfix_rerun/round5/collar/aoi_frame_transfer.csv")
col = A[(A.source_frame == "10km") & (A.target_frame == "10km")].copy()
col["target"] = col.direction.str.split("_to_").str[1]
tmean = col.groupby("target").thermal.mean()
W = pd.DataFrame([w for w in res["within"] if w["frame"] == "10km"]).set_index("region")
gap = {}
for ref in ("cv10_thermal", "lobo_thermal", "lobo10km_thermal"):
    x = (W[ref] - tmean.reindex(W.index)).to_numpy()
    m, lo, hi = E.t_ci(x)
    gap[ref] = {"mean_reference": float(W[ref].mean()), "mean_shortfall": float(m),
                "ci95": [float(lo), float(hi)], "per_target": dict(zip(W.index, np.round(x, 4)))}
res["collar_shortfall"] = gap
print(json.dumps(gap, indent=1))

# Bejís pre-label sensitivity
pre = pd.read_csv(ROOT / "paper/labelfix_rerun/labels/r1_prelabel_cells_bejis_2022.csv")
bj = data["bejis_2022"]
key = bj.row_500m.astype(int).astype(str) + "_" + bj.col_500m.astype(int).astype(str)
drop = key.isin(pre.row_500m.astype(str) + "_" + pre.col_500m.astype(str)).to_numpy()
bj2 = bj[~drop].reset_index(drop=True)
bp = {"cells_removed": int(drop.sum()), "burned_among_removed": int(bj.burned[drop].sum())}
for B in (2, 10):
    for name, dd in (("all", bj), ("without_prelabel", bj2)):
        th = roc_auc_score(dd.burned, E.blocked_oof(dd, TH, B))
        ba = roc_auc_score(dd.burned, E.blocked_oof(dd, BA, B))
        bp[f"block{B}_{name}"] = {"thermal": float(th), "baseline": float(ba), "gain": float(th - ba)}
tr = []
for other in [r for r in E.REGIONS if r != "bejis_2022"]:
    o = data[other]
    for name, b in (("all", bj), ("without_prelabel", bj2)):
        for src, tgt, sn, tn in ((b, o, "bejis_2022", other), (o, b, other, "bejis_2022")):
            th = roc_auc_score(tgt.burned, E.fit(TH, src).predict_proba(tgt[TH])[:, 1])
            ba = roc_auc_score(tgt.burned, E.fit(BA, src).predict_proba(tgt[BA])[:, 1])
            tr.append({"set": name, "direction": f"{sn}_to_{tn}", "thermal": th, "baseline": ba, "delta": th - ba})
T = pd.DataFrame(tr)
bp["transfer"] = T.to_dict(orient="records")
bp["transfer_max_abs_change_thermal"] = float((T[T.set == "all"].set_index("direction").thermal
                                               - T[T.set == "without_prelabel"].set_index("direction").thermal).abs().max())
bp["transfer_mean_delta"] = T.groupby("set").delta.mean().to_dict()
res["bejis_prelabel"] = bp
print(json.dumps({k: v for k, v in bp.items() if k != "transfer"}, indent=1))
json.dump(res, open(HERE / "r8b_summary.json", "w"), indent=1, default=float)
