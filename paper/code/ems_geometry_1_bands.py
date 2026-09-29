"""Analysis 1 (SPEC.md): distance-band AUC with scar-edge exclusion.

Row-A OOF thermal scores. Positives: population burned cells surviving k erosions of the
label-map burned mask; negatives: population unburned cells beyond k cells (Chebyshev) of
any label-map burned cell. Bands on band-convention distance (distance_curve.py).
Also A_k - B_k per scar.
"""
import numpy as np
import pandas as pd
from scipy import ndimage

import ems_geometry_common as G

BANDS = [(0, 0.5), (0.5, 1), (1, 2), (2, 5), (5, 10), (10, np.inf)]
S3 = np.ones((3, 3), bool)
rows, scar_rows = [], []
for reg in G.REGIONS:
    R = G.Region(reg)
    oof = G.oof_row_a(R)
    scars = R.scars()
    for k in (0, 1, 2):
        if k == 0:
            keep_pos = R.y == 1
            keep_neg = R.y == 0
        else:
            core = ndimage.binary_erosion(R.edge_mask, structure=S3, iterations=k, border_value=1)
            near = ndimage.binary_dilation(R.edge_mask, structure=S3, iterations=k)
            keep_pos = (R.y == 1) & core[R.rr, R.cc]
            keep_neg = (R.y == 0) & ~near[R.rr, R.cc]
        keep = keep_pos | keep_neg
        bands = [("all", -1, np.inf)] + [(f"{lo}-{hi}", lo, hi) for lo, hi in BANDS]
        for name, lo, hi in bands:
            negsel = keep_neg & (R.dist_band >= lo) & (R.dist_band < hi) if lo >= 0 else keep_neg
            sel = keep_pos | negsel
            nneg = int(negsel.sum())
            row = {"region": reg, "k": k, "band": name, "positives": int(keep_pos.sum()), "negatives": nneg}
            if nneg >= 20 and keep_pos.sum() > 0:
                row["auc"] = G.auc(R.y[sel], oof[sel])
                lo_, hi_, nb = G.block_boot(R.y[sel], oof[sel], R.block10_codes[sel], G.auc)
                row.update(ci_lo=lo_, ci_hi=hi_, boot_used=nb)
            rows.append(row)
        a_k = G.auc(R.y[keep], oof[keep])
        for sc in scars:
            h = sc["held"] & keep
            b_k = G.auc(R.y[h], oof[h])
            scar_rows.append({"region": reg, "scar": sc["scar"], "k": k, "A": a_k, "B": b_k,
                              "A_minus_B": a_k - b_k, "B_pos": int(R.y[h].sum()),
                              "B_neg": int((R.y[h] == 0).sum())})
        print(reg, k, "done", flush=True)

D = pd.DataFrame(rows)
S = pd.DataFrame(scar_rows)
D.to_csv(G.OUT / "a1_band_auc.csv", index=False)
S.to_csv(G.OUT / "a1_frame_cost_edge_excluded.csv", index=False)

summ = {"bands_mean_over_regions": [], "frame_cost": []}
for k in (0, 1, 2):
    for name in ["all"] + [f"{lo}-{hi}" for lo, hi in BANDS]:
        v = D[(D.k == k) & (D.band == name)]["auc"].dropna()
        m, lo, hi, n = G.t_ci(v)
        summ["bands_mean_over_regions"].append({"k": k, "band": name, "mean_auc": m, "t_lo": lo, "t_hi": hi, "n_regions": n})
    s = S[S.k == k]
    for label, sub in (("nine_scars", s), ("eight_scars_table2", s[s.region != "bejis_2022"])):
        m, lo, hi, n = G.t_ci(sub.A_minus_B)
        mc, loc, hic, nc = G.region_cluster_ci(sub.A_minus_B.to_numpy(), sub.region.to_numpy())
        summ["frame_cost"].append({"k": k, "set": label, "mean_A": sub.A.mean(), "mean_B": sub.B.mean(),
                                   "A_minus_B": m, "scar_t": [lo, hi], "n": n,
                                   "region_cluster_mean": mc, "region_cluster_t": [loc, hic], "n_regions": nc})
G.dump(summ, "a1_summary.json")
pd.set_option("display.width", 200)
print(D.pivot_table(index=["region", "band"], columns="k", values="auc").round(3).to_string())
print(pd.DataFrame(summ["bands_mean_over_regions"]).round(3).to_string())
print(pd.DataFrame(summ["frame_cost"]).round(4).to_string())
