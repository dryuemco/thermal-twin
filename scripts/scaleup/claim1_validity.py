"""claim1_validity.py: validity checks of claims 1 and 2 asked for by the second review (amendment 5, post hoc).

margin     the fixed 5 km out-of-fold predictions rescored on the cells inside the bounding box of the burned
           cells plus 0.05 and 0.10 degree (the study rectangles use 0.15 degree); null model against the
           thermal RF
landcover  the thermal RF refitted without land cover (WorldCover 2021 postdates 20 of the fires), same folds
envbands   distance bands rescored with the unburned cells restricted to the middle three quintiles of their
           Mahalanobis distance to the burned cells (thermal numeric predictors, standardised within the fire,
           covariance of the burned cells), so that environmental similarity is held roughly constant across bands

Writes claim1_validity_per_fire.csv, claim1_envbands.csv and claim1_validity_summary.json in
$THERMAL_TWIN_SCALEUP/analysis.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analysis_official as A  # noqa: E402

MARGINS = (0.05, 0.10)
NOLC = [f for f in A.THERMAL if f != A.CAT]


def main():
    F = A.load_fires()
    ids = [i for i in F if i != "montiferru_2021"]
    rows, eb = [], []
    for fid in ids:
        f = F[fid]
        y = f.y
        s_rf, s_null = f.oof(A.THERMAL, "thermal", "rf", 10), f.null_oof(10)
        r = {"fire": fid, "year": f.meta["year"]}
        lon, lat = f.df.lon.to_numpy(), f.df.lat.to_numpy()
        for m in MARGINS:
            box = ((lon >= lon[y == 1].min() - m) & (lon <= lon[y == 1].max() + m) &
                   (lat >= lat[y == 1].min() - m) & (lat <= lat[y == 1].max() + m))
            r[f"m{m}_cells_share"] = float(box.mean())
            r[f"m{m}_auc_rf"], r[f"m{m}_auc_null"] = A.auc(y[box], s_rf[box]), A.auc(y[box], s_null[box])
        o = np.full(f.n, np.nan)
        for tr, te in f.folds(10):
            m_ = A.build(NOLC).fit(f.df.iloc[tr][NOLC], f.df.burned.iloc[tr])
            o[te] = m_.predict_proba(f.df.iloc[te][NOLC])[:, 1]
        r["auc_rf_nolc"], r["auc_null"], r["auc_rf"] = A.auc(y, o), A.auc(y, s_null), A.auc(y, s_rf)
        md = A.mahalanobis_to_burned(f)
        q1, q4 = np.quantile(md[y == 0], [0.2, 0.8])
        mid = (y == 0) & (md >= q1) & (md < q4)
        for name, (lo, hi) in zip(A.BAND_NAMES, A.BANDS):
            neg = mid & (f.dist >= lo) & (f.dist < hi)
            sel = (y == 1) | neg
            eb.append({"fire": fid, "band": name, "negatives": int(neg.sum()),
                       "auc_rf": A.auc(y[sel], s_rf[sel]) if neg.sum() >= A.MIN_BAND_NEG else np.nan,
                       "auc_null": A.auc(y[sel], s_null[sel]) if neg.sum() >= A.MIN_BAND_NEG else np.nan})
        rows.append(r)
        print(fid, {k: round(v, 3) for k, v in r.items() if isinstance(v, float)}, flush=True)
    R, E = pd.DataFrame(rows), pd.DataFrame(eb)
    R.to_csv(A.OUT / "claim1_validity_per_fire.csv", index=False)
    E.to_csv(A.OUT / "claim1_envbands.csv", index=False)
    late = R[R.year >= 2022]
    S = {"margins": {str(m): {"cells_share": A.boot_mean(R[f"m{m}_cells_share"]), "auc_rf": A.boot_mean(R[f"m{m}_auc_rf"]),
                              "auc_null": A.boot_mean(R[f"m{m}_auc_null"]),
                              "null_beats_rf": A.count(R[f"m{m}_auc_null"].to_numpy(), R[f"m{m}_auc_rf"].to_numpy())}
                     for m in MARGINS},
         "no_landcover": {"auc_rf_nolc": A.boot_mean(R.auc_rf_nolc), "auc_rf": A.boot_mean(R.auc_rf),
                          "null_beats_rf_nolc": A.count(R.auc_null.to_numpy(), R.auc_rf_nolc.to_numpy()),
                          "nolc_minus_rf": A.boot_mean(R.auc_rf_nolc - R.auc_rf)},
         "fires_2022_2023": {"fires": int(len(late)), "auc_rf": A.boot_mean(late.auc_rf), "auc_null": A.boot_mean(late.auc_null),
                             "null_beats_rf": A.count(late.auc_null.to_numpy(), late.auc_rf.to_numpy())},
         "envbands": {n: {"auc_rf": A.boot_mean(E[E.band == n].auc_rf), "auc_null": A.boot_mean(E[E.band == n].auc_null),
                          "fires": int(E[E.band == n].auc_rf.notna().sum())} for n in A.BAND_NAMES}}
    v = E.dropna(subset=["auc_rf"]).sort_values(["fire", "band"], key=lambda c: c.map({n: i for i, n in enumerate(A.BAND_NAMES)}) if c.name == "band" else c)
    rise = v.groupby("fire").auc_rf.agg(lambda a: a.iloc[-1] - a.iloc[0] if len(a) >= 2 else np.nan)
    S["envbands_rise"] = {"rise": A.boot_mean(rise), "fires_positive": f"{int((rise > 0).sum())} of {int(rise.notna().sum())}"}
    (A.OUT / "claim1_validity_summary.json").write_text(json.dumps(S, indent=1, default=float), encoding="utf-8")
    print(json.dumps(S, indent=1, default=float))


if __name__ == "__main__":
    main()
