"""planned_outputs.py: outputs listed in docs/scaleup/ANALYSIS_PLAN.md that the first draft did not report
(amendment 5, asked for by the second review). Reads only existing outputs and rasters, fits nothing.

  firecci     agreement of MCD64A1 with FireCCI51 (confidence >= 50, share >= 0.5) in the fires the product covers,
              and the share of MCD64A1 unburned cells that FireCCI51 maps as burned, by band
  trend       Spearman correlation of the thermal RF's band AUC with the band order, per fire
  landscape   standard deviation of elevation and NDVI among the unburned cells of each band (mean over fires)
  nearband    paired RF minus null difference in the nearest band: mean, fire bootstrap interval, sign test

Writes planned_outputs.json in $THERMAL_TWIN_SCALEUP/analysis.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
from scipy.stats import binomtest, spearmanr
from sklearn.metrics import cohen_kappa_score

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analysis_official as A  # noqa: E402


def main():
    S = {}
    F = A.load_fires()
    rows, eb = [], []
    for fid in [i for i in F if i != "montiferru_2021"]:
        p = A.OUT / "s2" / f"{fid}.tif"
        with rasterio.open(p) as r:
            a = r.read()
        f = F[fid]
        cci = a[3][f.df.row_500m.to_numpy(int), f.df.col_500m.to_numpy(int)]
        if np.nanmax(cci) < 0:
            continue
        c = (cci >= 0.5).astype(int)
        rows.append({"fire": fid, "agreement": float((c == f.y).mean()), "kappa": float(cohen_kappa_score(f.y, c)),
                     "mcd_burned": int(f.y.sum()), "cci_burned": int(c.sum())})
        for name, (lo, hi) in zip(A.BAND_NAMES, A.BANDS):
            neg = (f.y == 0) & (f.dist >= lo) & (f.dist < hi)
            if neg.sum():
                eb.append({"fire": fid, "band": name, "cci_burned_share": float(c[neg].mean())})
    R, E = pd.DataFrame(rows), pd.DataFrame(eb)
    S["firecci"] = {"fires": R.fire.tolist(), "agreement": A.boot_mean(R.agreement), "kappa": A.boot_mean(R.kappa),
                    "unburned_mapped_burned_by_band": {n: float(E[E.band == n].cci_burned_share.mean()) for n in A.BAND_NAMES}}
    B = pd.read_csv(A.OUT / "claims12_bands.csv")
    B = B[B.fire != "montiferru_2021"]
    order = {n: i for i, n in enumerate(A.BAND_NAMES)}
    B["k"] = B.band.map(order)
    rho = B.dropna(subset=["auc_rf_thermal"]).groupby("fire").apply(lambda g: spearmanr(g.k, g.auc_rf_thermal)[0])
    S["trend"] = {"rho": A.boot_mean(rho), "fires_positive": f"{int((rho > 0).sum())} of {int(rho.notna().sum())}"}
    S["landscape"] = {n: {"sd_elevation_m": float(B[B.band == n].sd_elevation.mean()), "sd_ndvi": float(B[B.band == n].sd_ndvi.mean())}
                      for n in A.BAND_NAMES}
    n = B[B.band == A.BAND_NAMES[0]].dropna(subset=["auc_rf_thermal", "auc_null"])
    d = n.auc_rf_thermal - n.auc_null
    S["nearband"] = {"rf_minus_null": A.boot_mean(d), "fires_rf_ahead": f"{int((d > 0).sum())} of {len(d)}",
                     "sign_test_p": float(binomtest(int((d > 0).sum()), len(d)).pvalue)}
    (A.OUT / "planned_outputs.json").write_text(json.dumps(S, indent=1, default=float), encoding="utf-8")
    print(json.dumps(S, indent=1, default=float))


if __name__ == "__main__":
    main()
