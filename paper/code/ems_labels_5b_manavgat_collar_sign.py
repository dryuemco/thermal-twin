"""[post-hoc] Addendum A follow-up: the Appendix A(k) LST sign for Manavgat on the 10 km
collar (verify_matched_gap.py definition), frozen labels vs full-label-window labels.
Usage: python ems_labels_5b_manavgat_collar_sign.py <cache_dir>
"""
import sys
from pathlib import Path

import ems_labels_common as E
import numpy as np
from scipy import ndimage
from sklearn.metrics import roc_auc_score

a = np.load(Path(sys.argv[1]) / "manavgat_2021_labelwin.npy")
d0 = E.tsg("manavgat_2021")
d1 = d0.copy(); d1["burned"] = E.cell_values(d1, E.any_positive(a)).astype(int)
res = {}
for arm, d in (("frozen", d0), ("full_window", d1)):
    r0, c0 = int(d.row_500m.min()), int(d.col_500m.min())
    H, W = int(d.row_500m.max()) - r0 + 1, int(d.col_500m.max()) - c0 + 1
    rr, cc = d.row_500m.to_numpy().astype(int) - r0, d.col_500m.to_numpy().astype(int) - c0
    bg = np.ones((H, W), bool); b = d.burned.to_numpy() == 1; bg[rr[b], cc[b]] = False
    sub = d[ndimage.distance_transform_edt(bg)[rr, cc] * E.CELL_KM <= 10]
    res[arm] = {"n_collar": int(len(sub))}
    for f in ("current_lst_mean", "current_tvdi_mean", "elevation_mean", "ndvi_mean"):
        s = sub[sub[f].notna()]
        ci = E.block_bootstrap_ci(s.burned.to_numpy(), s[f].to_numpy(),
                                  E.add_spatial_block_id(s, 10).to_numpy())
        res[arm][f] = {"auc": roc_auc_score(s.burned, s[f]), "ci": ci["roc_auc_ci95"]}
    E.log(arm, res[arm])
E.dump(res, "r5b_manavgat_collar_sign.json")
