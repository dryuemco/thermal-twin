"""
Does Contribution 3's winning diagnostic survive frame equalisation?

Section 4.4's only diagnostic with an interval excluding zero is
`agree_fraction_supported`: the fraction of features whose signed univariate AUC
points the same way in source and target, counted over features that are
interval-supported in both. Section 4.9 has just shown that those signed AUCs are
substantially frame artefacts. If the diagnostic was reading the frame, then once
frames are equalised it should lose its variance and its correlation with transfer.

A referee claims exactly that: value 1.0 in every direction under the collar,
variance zero, so nothing left to correlate. This checks it from scratch, and
also recomputes a continuous alternative (cosine similarity over all nine signed
AUCs) which does not depend on the support test.

Read-only with respect to repo/.
"""
import sys

import numpy as np
import pandas as pd
from scipy import ndimage, stats
from sklearn.metrics import roc_auc_score
import _canonical

OUT = sys.argv[1]
REGIONS = ["manavgat_2021", "bejis_2022", "mugla_2021",
           "evia_2021_extended", "montiferru_2021"]
FEATS = ["ndvi_mean", "elevation_mean", "slope_mean", "current_lst_mean",
         "lst_anomaly_mean", "current_tvdi_mean", "tvdi_difference_mean",
         "downscaled_lst_mean", "fused_lst_mean"]
CELL_KM, BLOCK, NBOOT, SEED = 0.45, 10, 1000, 42
import os
# Artefacts this script reads or writes that are themselves regenerated from the
# canonical inputs. Default "paper" is the published location; the canonical re-run
# sets PAPER_ARTEFACTS=paper/canonical_rerun so nothing published is overwritten.
ART = os.environ.get("PAPER_ARTEFACTS", "paper")


def load(reg):
    d = _canonical.load(reg)
    d = d[(d.valid_for_modeling == True) &  # noqa: E712
          (d.burnable_tree_shrub_grass == True)].reset_index(drop=True)  # noqa: E712
    r0, c0 = int(d.row_500m.min()), int(d.col_500m.min())
    H = int(d.row_500m.max()) - r0 + 1
    W = int(d.col_500m.max()) - c0 + 1
    rr = d.row_500m.to_numpy().astype(int) - r0
    cc = d.col_500m.to_numpy().astype(int) - c0
    bg = np.ones((H, W), dtype=bool)
    b = d.burned.to_numpy() == 1
    bg[rr[b], cc[b]] = False
    d["dist_km"] = ndimage.distance_transform_edt(bg)[rr, cc] * CELL_KM
    d["block"] = (d.row_500m // BLOCK).astype(str) + "_" + (d.col_500m // BLOCK).astype(str)
    return d


def signed_auc_ci(sub, f, seed=SEED):
    ok = sub[f].notna()
    y, x, blk = sub.burned[ok].to_numpy(), sub[f][ok].to_numpy(), sub.block[ok].to_numpy()
    if len(np.unique(y)) < 2:
        return np.nan, np.nan, np.nan
    pt = roc_auc_score(y, x)
    rng = np.random.default_rng(seed)
    uniq = np.unique(blk)
    idx = {b: np.where(blk == b)[0] for b in uniq}
    out = []
    for _ in range(NBOOT):
        pick = rng.choice(uniq, len(uniq), replace=True)
        i = np.concatenate([idx[b] for b in pick])
        if len(np.unique(y[i])) > 1:
            out.append(roc_auc_score(y[i], x[i]))
    return pt, float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))


data = {r: load(r) for r in REGIONS}

# signed AUCs + support flags, per frame
prof = {}
for frame in ["full", "collar10"]:
    for reg in REGIONS:
        sub = data[reg] if frame == "full" else data[reg][data[reg].dist_km <= 10]
        for f in FEATS:
            pt, lo, hi = signed_auc_ci(sub, f)
            prof[(frame, reg, f)] = (pt, (lo > 0.5) or (hi < 0.5))
    print(f"profiled {frame}", flush=True)

# transfer vectors
tr = pd.read_csv("paper/baseline_vs_thermal_transfer.csv")
tr_full = {r.direction: r.thermal_roc for _, r in tr.iterrows()}
ac = pd.read_csv(f"{ART}/aoi_frame_transfer.csv")
ac = ac[(ac.source_frame == "10km") & (ac.target_frame == "10km")]
tr_collar = {r.direction: r.thermal for _, r in ac.iterrows()}

rows = []
for frame, tvec in [("full", tr_full), ("collar10", tr_collar)]:
    recs = []
    for s in REGIONS:
        for t in REGIONS:
            if s == t:
                continue
            both = [f for f in FEATS
                    if prof[(frame, s, f)][1] and prof[(frame, t, f)][1]]
            if both:
                agree = np.mean([(prof[(frame, s, f)][0] - 0.5) *
                                 (prof[(frame, t, f)][0] - 0.5) > 0 for f in both])
            else:
                agree = np.nan
            vs = np.array([prof[(frame, s, f)][0] - 0.5 for f in FEATS])
            vt = np.array([prof[(frame, t, f)][0] - 0.5 for f in FEATS])
            cos = float(vs @ vt / (np.linalg.norm(vs) * np.linalg.norm(vt)))
            recs.append({"frame": frame, "direction": f"{s}_to_{t}",
                         "n_supported_both": len(both),
                         "agree_fraction_supported": agree,
                         "cosine_9": cos,
                         "transfer": tvec.get(f"{s}_to_{t}", np.nan)})
    D = pd.DataFrame(recs)
    rows.append(D)
    print(f"\n{'='*70}\nFRAME = {frame}\n{'='*70}")
    a = D.dropna(subset=["agree_fraction_supported", "transfer"])
    print(f"  agree_fraction_supported: defined in {len(a)}/20 directions")
    print(f"    distinct values: {sorted(a.agree_fraction_supported.unique())}")
    print(f"    variance: {a.agree_fraction_supported.var():.6f}")
    if a.agree_fraction_supported.nunique() > 1:
        rho, p = stats.spearmanr(a.agree_fraction_supported, a.transfer)
        print(f"    Spearman rho vs transfer = {rho:+.4f}  (p={p:.4f}, n={len(a)})")
    else:
        print("    *** DEGENERATE: no variance, correlation undefined ***")
    c = D.dropna(subset=["cosine_9", "transfer"])
    rho, p = stats.spearmanr(c.cosine_9, c.transfer)
    print(f"  cosine_9 vs transfer: rho = {rho:+.4f}  (p={p:.4f}, n={len(c)})")
    print(f"    mean supported-in-both features per direction: {D.n_supported_both.mean():.2f}")

pd.concat(rows).to_csv(OUT, index=False)
print(f"\nwrote {OUT}")
