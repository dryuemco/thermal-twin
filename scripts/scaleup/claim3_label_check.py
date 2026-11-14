"""claim3_label_check.py: claim 3 of docs/scaleup/ANALYSIS_PLAN.md, MCD64A1 label error near the fire edge.

Inputs: the Sentinel-2 / FireCCI51 shares from s2_label_check_export.py and the cached out-of-fold
predictions of analysis_official.py (5 km blocks; the models are NOT refitted, only the evaluation
labels change). Bands are the claim 2 bands (distance of an unburned cell to the nearest MCD64A1
burned cell of the same fire).

Per band: share of MCD64A1-unburned cells with Sentinel-2 burned share above 0.05, 0.25 and 0.5; share
of MCD64A1-burned cells with share below 0.1. Re-scoring variants (plan): (a) Sentinel-2 label, burned
if share >= 0.5; (b) MCD64A1 label, unburned cells with share > 0.05 dropped; (c) MCD64A1 label,
unburned cells with share >= 0.5 relabelled burned. Primary threshold dNBR >= 0.10, sensitivity 0.27.
Decision rule: mean over fires of the share of the near-to-far gap closed by a variant in the 0-0.5 km
band; above 0.5 means claim 2 is rewritten as a label-error finding.

Run:  <venv-step10>/python claim3_label_check.py   (writes D:/ThermalTwin/scaleup/analysis/claim3_*)
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analysis_official as A  # noqa: E402

S2 = A.OUT / "s2"
VALID_MIN = 0.5      # amendment 3: minimum share of valid 20 m Sentinel-2 pixels for a cell to enter the check
MODELS = ("rf_thermal", "hgb_thermal", "null")


def band_auc(y, s, dist, name_lo_hi):
    lo, hi = name_lo_hi
    neg = (y == 0) & (dist >= lo) & (dist < hi)
    if neg.sum() < A.MIN_BAND_NEG or (y == 1).sum() == 0:
        return np.nan
    sel = (y == 1) | neg
    return A.auc(y[sel], s[sel])


def main():
    F = A.load_fires()
    primary = [i for i in F if i != "montiferru_2021"]
    err_rows, band_rows, fire_rows = [], [], []
    for fid in primary:
        f = F[fid]
        src = "montiferru_2021_fullwindow" if fid == "montiferru_2021_fullwindow" else fid
        p = S2 / f"{src}.tif"
        if not p.exists():
            print(fid, "no Sentinel-2 file, skipped", flush=True)
            continue
        with rasterio.open(p) as r:
            a = r.read()
        rr, cc = f.df.row_500m.to_numpy(int), f.df.col_500m.to_numpy(int)
        sh = {"010": a[0][rr, cc], "027": a[1][rr, cc]}
        valid, cci = a[2][rr, cc], a[3][rr, cc]
        y, dist = f.y, f.dist
        s = {"rf_thermal": f.oof(A.THERMAL, "thermal", "rf", 10), "hgb_thermal": f.oof(A.THERMAL, "thermal", "hgb", 10),
             "null": f.null_oof(10)}
        fr = {"fire": fid, "cells": f.n, "burned": f.nb, "s2_valid_share_median": float(np.nanmedian(valid)),
              "cells_valid_below_half": int((valid < 0.5).sum()), "firecci_available": bool(np.nanmax(cci) >= 0)}
        for th, x in sh.items():
            # amendment 3: a cell enters the check only if at least half of its 20 m pixels have a valid dNBR;
            # shares are shares of the observed part of the cell
            ok = np.isfinite(x) & (valid >= VALID_MIN)
            fr[f"burned_cells_share_below_0.1_{th}"] = float((x[(y == 1) & ok] < 0.1).mean())
            fr[f"cells_used_{th}"], fr[f"cells_excluded_{th}"] = int(ok.sum()), int((~ok).sum())
            for name, (lo, hi) in zip(A.BAND_NAMES, A.BANDS):
                neg_all = (y == 0) & (dist >= lo) & (dist < hi)
                neg = neg_all & ok
                if neg.sum() == 0:
                    continue
                er = {"fire": fid, "threshold": th, "band": name, "unburned_cells": int(neg.sum()),
                      "unburned_cells_excluded": int((neg_all & ~ok).sum())}
                for c in (0.05, 0.25, 0.5):
                    er[f"unburned_share_above_{c}"] = float(((x[neg] >= c) if c == 0.5 else (x[neg] > c)).mean())   # 0.5: same rule as the label (at least half)
                if th == "010" and fr["firecci_available"]:
                    er["unburned_firecci_share_above_0.5"] = float((cci[neg] > 0.5).mean())
                err_rows.append(er)
            # every variant, the MCD64A1 reference included, is scored on the same valid cells
            variants = {
                "mcd64a1": (y, ok),
                "a_s2_label": ((x >= 0.5).astype(int), ok),
                "b_drop_ambiguous": (y, ok & ~((y == 0) & (x > 0.05))),
                "c_relabel": (np.where((y == 0) & (x >= 0.5), 1, y), ok),
            }
            for vname, (yv, keep) in variants.items():
                if th == "027" and vname == "mcd64a1":
                    continue
                for m in MODELS:
                    br = {"fire": fid, "threshold": th, "variant": vname, "model": m}
                    for name, lohi in zip(A.BAND_NAMES, A.BANDS):
                        br[name] = band_auc(yv[keep], s[m][keep], dist[keep], lohi)
                    br["whole"] = A.auc(yv[keep], s[m][keep])
                    band_rows.append(br)
        fire_rows.append(fr)
        print(fid, "done", flush=True)

    E, B, FR = pd.DataFrame(err_rows), pd.DataFrame(band_rows), pd.DataFrame(fire_rows)
    E.to_csv(A.OUT / "claim3_label_error_by_band.csv", index=False)
    B.to_csv(A.OUT / "claim3_rescored_bands.csv", index=False)
    FR.to_csv(A.OUT / "claim3_per_fire.csv", index=False)

    def far(row):
        v = [row[n] for n in A.BAND_NAMES if np.isfinite(row[n])]
        return v[-1] if v else np.nan

    S = {"fires": len(FR), "cells_valid_below_half_total": int(FR.cells_valid_below_half.sum()),
         "firecci_fires": int(FR.firecci_available.sum()),
         "cells_used": int(FR.cells_used_010.sum()), "cells_excluded": int(FR.cells_excluded_010.sum()),
         "unburned_used_by_band": {n: int(E[(E.threshold == "010") & (E.band == n)].unburned_cells.sum()) for n in A.BAND_NAMES},
         "unburned_excluded_by_band": {n: int(E[(E.threshold == "010") & (E.band == n)].unburned_cells_excluded.sum()) for n in A.BAND_NAMES},
         "gap_closed_definition": "mean over fires of (near-band AUC of the variant - near-band AUC of MCD64A1) / "
                                  "(farthest-band AUC of MCD64A1 - near-band AUC of MCD64A1), all on the valid cells"}
    for th in ("010", "027"):
        e = E[E.threshold == th]
        S[f"label_error_{th}"] = {n: {c: A.boot_mean(e[e.band == n][c]) for c in
                                     ("unburned_share_above_0.05", "unburned_share_above_0.25", "unburned_share_above_0.5")}
                                 for n in A.BAND_NAMES}
        S[f"burned_cells_share_below_0.1_{th}"] = A.boot_mean(FR[f"burned_cells_share_below_0.1_{th}"])
        base = B[(B.threshold == "010") & (B.variant == "mcd64a1")].set_index(["fire", "model"])
        for vname in ("a_s2_label", "b_drop_ambiguous", "c_relabel"):
            v = B[(B.threshold == th) & (B.variant == vname)].set_index(["fire", "model"])
            out = {}
            for m in MODELS:
                bm, vm = base.xs(m, level="model"), v.xs(m, level="model")
                near_b, near_v = bm["0-0.5"], vm["0-0.5"]
                far_b = bm.apply(far, axis=1)
                closed = (near_v - near_b) / (far_b - near_b)
                out[m] = {"near_band_auc_mcd64a1": A.boot_mean(near_b), "near_band_auc_variant": A.boot_mean(near_v),
                          "far_band_auc_mcd64a1": A.boot_mean(far_b),
                          "bands_variant": {n: A.boot_mean(vm[n]) for n in A.BAND_NAMES},
                          "share_of_gap_closed": A.boot_mean(closed),
                          "decision_rewrite_claim2": bool(np.nanmean(closed) > 0.5) if m == "rf_thermal" else None}
            S[f"variant_{vname}_{th}"] = out
    (A.OUT / "claim3_summary.json").write_text(json.dumps(S, indent=1, ensure_ascii=False, default=float), encoding="utf-8")
    print(json.dumps({k: S[k] for k in ("fires", "cells_valid_below_half_total", "firecci_fires")}, indent=1))


if __name__ == "__main__":
    main()
