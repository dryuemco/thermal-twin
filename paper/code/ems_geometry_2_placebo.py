"""Analysis 2 (SPEC.md): placebo collars.

For each real scar, its exact shape (one of 8 dihedral orientations) is placed where its
dilated footprint (B's rule: cross structure, 4 iterations) touches no burned cell and
>=80 % of the footprint is population. The population cells in the dilated footprint form
a placebo negative pool, scored against the scar's real B positives with row-A OOF scores.
"""
import numpy as np
import pandas as pd
from scipy import ndimage, stats
from scipy.signal import fftconvolve

import ems_geometry_common as G

N_PLACE, POP_FRAC, MIN_POOL = 50, 0.8, 50
rng = np.random.default_rng(G.SEED)


def orientations(shape):
    out, seen = [], set()
    for flip in (False, True):
        s = shape[:, ::-1] if flip else shape
        for r in range(4):
            o = np.rot90(s, r)
            key = (o.shape, o.tobytes())
            if key not in seen:
                seen.add(key)
                out.append(np.ascontiguousarray(o))
    return out


def corr_count(grid, kern):
    """Number of kernel cells overlapping True cells of grid, for each valid top-left offset."""
    c = fftconvolve(grid.astype(float), kern[::-1, ::-1].astype(float), mode="valid")
    return np.rint(c).astype(int)


rows, place_rows = [], []
for reg in G.REGIONS:
    R = G.Region(reg)
    oof = G.oof_row_a(R)
    a = G.auc(R.y, oof)
    forbidden = ndimage.binary_dilation(R.edge_mask, iterations=G.DIL_IT)
    pos_idx_grid = -np.ones((R.H, R.W), int)
    pos_idx_grid[R.rr, R.cc] = np.arange(len(R.y))
    for sc in R.scars():
        comp = sc["comp"]
        rs, cs = np.where(comp)
        shape = comp[rs.min():rs.max() + 1, cs.min():cs.max() + 1]
        size = int(shape.sum())
        cands = []
        for oi, o in enumerate(orientations(shape)):
            if o.shape[0] > R.H or o.shape[1] > R.W:
                continue
            bad = corr_count(forbidden, o)
            popc = corr_count(R.pop_grid, o)
            ok = (bad == 0) & (popc >= POP_FRAC * size)
            for i, j in zip(*np.where(ok)):
                cands.append((oi, int(i), int(j)))
        orients = orientations(shape)
        pos = R.y[sc["held"]] == 1
        pos_scores = oof[sc["held"]][pos]
        b = G.auc(R.y[sc["held"]], oof[sc["held"]])
        order = rng.permutation(len(cands)) if cands else []
        used = []
        for ci in order:
            if len(used) >= N_PLACE:
                break
            oi, i, j = cands[ci]
            o = orients[oi]
            fp = np.zeros((R.H, R.W), bool)
            fp[i:i + o.shape[0], j:j + o.shape[1]] = o
            dil = ndimage.binary_dilation(fp, iterations=G.DIL_IT)
            idx = pos_idx_grid[dil & R.pop_grid]
            assert (R.y[idx] == 0).all()
            if len(idx) < MIN_POOL:
                continue
            yy = np.r_[np.ones(len(pos_scores)), np.zeros(len(idx))]
            ss = np.r_[pos_scores, oof[idx]]
            p_auc = G.auc(yy, ss)
            dmed = float(np.median(R.dist_collar[idx]))
            # post-hoc sensitivity (SPEC Deviations D1): collar ring only, footprint interior excluded
            cidx = pos_idx_grid[dil & ~fp & R.pop_grid]
            c_auc = G.auc(np.r_[np.ones(len(pos_scores)), np.zeros(len(cidx))],
                          np.r_[pos_scores, oof[cidx]]) if len(cidx) >= 20 else np.nan
            used.append((p_auc, dmed, len(idx), c_auc))
            place_rows.append({"region": reg, "scar": sc["scar"], "orientation": oi, "row": i, "col": j,
                               "pool_n": len(idx), "collar_only_n": len(cidx), "median_dist_km": dmed,
                               "placebo_auc": p_auc, "placebo_collar_only_auc": c_auc})
        pa = np.array([u[0] for u in used]) if used else np.array([np.nan])
        dd = np.array([u[1] for u in used]) if used else np.array([np.nan])
        rho = stats.spearmanr(pa, dd).statistic if len(used) >= 5 else np.nan
        real_neg = int((R.y[sc["held"]] == 0).sum())
        rows.append({"region": reg, "scar": sc["scar"], "scar_cells": size, "B_positives": int(pos.sum()),
                     "B_negatives": real_neg, "valid_candidates": len(cands), "placements": len(used),
                     "A": a, "B": b, "placebo_mean": float(np.nanmean(pa)),
                     "placebo_collar_only_mean": float(np.nanmean([u[3] for u in used])) if used else np.nan,
                     "placebo_p2_5": float(np.nanpercentile(pa, 2.5)) if used else np.nan,
                     "placebo_p97_5": float(np.nanpercentile(pa, 97.5)) if used else np.nan,
                     "share_placebo_le_B": float(np.mean(pa <= b)) if used else np.nan,
                     "placebo_median_dist_km": float(np.nanmedian(dd)),
                     "placebo_pool_median_n": float(np.median([u[2] for u in used])) if used else np.nan,
                     "spearman_auc_vs_dist": rho})
        print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in rows[-1].items()}, flush=True)

D = pd.DataFrame(rows)
P = pd.DataFrame(place_rows)
D.to_csv(G.OUT / "a2_placebo_by_scar.csv", index=False)
P.to_csv(G.OUT / "a2_placebo_placements.csv", index=False)
summ = {}
for label, sub in (("nine_scars", D), ("eight_scars_table2", D[D.region != "bejis_2022"])):
    sub = sub[sub.placements > 0]
    out = {"n_scars_with_placebos": int(len(sub))}
    for name, v in (("A_minus_placebo", sub.A - sub.placebo_mean), ("placebo_minus_B", sub.placebo_mean - sub.B),
                    ("A_minus_B", sub.A - sub.B)):
        m, lo, hi, n = G.t_ci(v)
        mc, loc, hic, nc = G.region_cluster_ci(v.to_numpy(), sub.region.to_numpy())
        out[name] = {"mean": m, "scar_t": [lo, hi], "region_cluster_mean": mc, "region_cluster_t": [loc, hic],
                     "n_regions": nc}
    v = sub.A - sub.placebo_collar_only_mean
    m, lo, hi, n = G.t_ci(v)
    out["A_minus_placebo_collar_only"] = {"mean": m, "scar_t": [lo, hi]}
    out["share_of_cost_reproduced_collar_only"] = float(v.mean() / (sub.A - sub.B).mean())
    out["share_of_cost_reproduced"] = float((sub.A - sub.placebo_mean).mean() / (sub.A - sub.B).mean())
    out["mean_A"], out["mean_B"], out["mean_placebo"] = sub.A.mean(), sub.B.mean(), sub.placebo_mean.mean()
    summ[label] = out
G.dump(summ, "a2_summary.json")
pd.set_option("display.width", 250)
print(D.round(3).to_string())
import json; print(json.dumps(summ, indent=1, default=float))
