"""claim5_lst_sign.py: claim 5 of docs/scaleup/ANALYSIS_PLAN.md, sign of the pre-fire LST relation.

Per fire (primary set, population of claim 1): AUC of current_lst_mean for the burned label (below 0.5
means cooler cells burned more) with a 10-cell block-bootstrap interval (500 resamples); the same AUC on
the residual of LST after (a) elevation, (b) elevation, NDVI and tree cover, (c) (b) plus northness and
eastness from the experiment DEM (30 m aspect averaged over each 500 m cell). The same for the
afternoon Aqua LST of aqua_lst_export.py. Reported as a secondary observation.

Run:  <venv-step10>/python claim5_lst_sign.py   (writes D:/ThermalTwin/scaleup/analysis/claim5_*)
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
from sklearn.linear_model import LinearRegression

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analysis_official as A  # noqa: E402

REPO_OUT = A.REPO / "outputs" / "experiments"
AQUA = A.OUT / "aqua_lst"
BLOCK = 17                       # 30 m pixels per 500 m cell side (step8a block_size_pixels)
CONTROLS = {"elev": ["elevation_mean"],
            "elev_ndvi_tree": ["elevation_mean", "ndvi_mean", "landcover_tree_cover_fraction"],
            "elev_ndvi_tree_aspect": ["elevation_mean", "ndvi_mean", "landcover_tree_cover_fraction", "northness", "eastness"]}


def dem_path(fid):
    if fid in A.PAPER_REGIONS:
        # the paper regions' DEM sits in one of these places depending on the pipeline version that wrote it
        for rel in ("data/dem/elevation.tif", "data/data/dem/elevation.tif", "step7b/aligned_inputs/elevation.tif"):
            if (REPO_OUT / fid / rel).exists():
                return REPO_OUT / fid / rel
        raise FileNotFoundError(fid)
    hits = list(A.SCALEUP.glob(f"w*/outputs/experiments/{fid}/data/dem/elevation.tif"))
    assert len(hits) == 1, (fid, hits)
    return hits[0]


def aspect_cells(fid, rr, cc):
    with rasterio.open(dem_path(fid)) as r:
        z = r.read(1).astype(float)
        if r.nodata is not None:
            z[z == r.nodata] = np.nan
        lat = r.transform.f + r.transform.e * r.height / 2
        dy = abs(r.transform.e) * 111320.0
        dx = r.transform.a * 111320.0 * np.cos(np.radians(lat))
    gy, gx = np.gradient(z, dy, dx)            # rows run south, so -gy is the northward slope
    asp = np.arctan2(-gx, gy)                  # downslope azimuth from north, clockwise
    north, east = np.cos(asp), np.sin(asp)
    H, W = z.shape
    hb, wb = -(-H // BLOCK), -(-W // BLOCK)
    out = []
    for a in (north, east):
        pad = np.full((hb * BLOCK, wb * BLOCK), np.nan)
        pad[:H, :W] = a
        out.append(np.nanmean(pad.reshape(hb, BLOCK, wb, BLOCK), axis=(1, 3))[rr, cc])
    return out


def block_boot(fn, blocks, B=500):
    ub, inv = np.unique(blocks, return_inverse=True)
    members = [np.where(inv == i)[0] for i in range(len(ub))]
    rng = np.random.default_rng(A.SEED)
    vals = []
    for _ in range(B):
        idx = np.concatenate([members[i] for i in rng.integers(0, len(ub), len(ub))])
        v = fn(idx)
        if np.isfinite(v):
            vals.append(v)
    return (float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))) if len(vals) >= 10 else (np.nan, np.nan)


def residual_auc(d, y, x, cols):
    k = np.isfinite(x) & d[cols].notna().all(axis=1).to_numpy()
    if k.sum() < 50 or y[k].min() == y[k].max():
        return np.nan
    res = x[k] - LinearRegression().fit(d.loc[k, cols], x[k]).predict(d.loc[k, cols])
    return A.auc(y[k], res)


def main():
    F = A.load_fires()
    ids = [i for i in F if i != "montiferru_2021"]
    rows = []
    for fid in ids:
        f = F[fid]
        d = f.df.copy()
        rr, cc = d.row_500m.to_numpy(int), d.col_500m.to_numpy(int)
        d["northness"], d["eastness"] = aspect_cells(fid, rr, cc)
        y = f.y
        sources = {"landsat_morning": d.current_lst_mean.to_numpy(float)}
        ap = AQUA / f"{fid}.tif"
        if ap.exists():
            with rasterio.open(ap) as r:
                sources["aqua_afternoon"] = r.read(1)[rr, cc].astype(float)
        row = {"fire": fid}
        blocks = f.blocks(10)
        for name, x in sources.items():
            ok = np.isfinite(x)
            row[f"{name}_auc"] = A.auc(y[ok], x[ok])
            row[f"{name}_lo"], row[f"{name}_hi"] = block_boot(lambda i: A.auc(y[i][ok[i]], x[i][ok[i]]), blocks)
            for tag, cols in CONTROLS.items():
                row[f"{name}_auc_given_{tag}"] = residual_auc(d, y, x, cols)
        if "aqua_afternoon" in sources:
            row["corr_morning_afternoon"] = float(pd.Series(sources["landsat_morning"]).corr(pd.Series(sources["aqua_afternoon"])))
        rows.append(row)
        print(fid, {k: round(v, 3) for k, v in row.items() if k.endswith("_auc")}, flush=True)
    R = pd.DataFrame(rows)
    R.to_csv(A.OUT / "claim5_lst_sign.csv", index=False)
    S = {}
    for name in ("landsat_morning", "aqua_afternoon"):
        if f"{name}_auc" not in R:
            continue
        g = R.dropna(subset=[f"{name}_auc"])
        S[name] = {"fires": int(len(g)), "auc": A.boot_mean(g[f"{name}_auc"]),
                   "cooler_burned": f"{int((g[f'{name}_auc'] < 0.5).sum())} of {len(g)}",
                   "cooler_interval_below_0.5": int((g[f"{name}_hi"] < 0.5).sum()),
                   "hotter_interval_above_0.5": int((g[f"{name}_lo"] > 0.5).sum()),
                   **{f"given_{t}": {"auc": A.boot_mean(g[f"{name}_auc_given_{t}"]),
                                     "cooler_burned": f"{int((g[f'{name}_auc_given_{t}'] < 0.5).sum())} of {int(g[f'{name}_auc_given_{t}'].notna().sum())}"}
                      for t in CONTROLS}}
    if "corr_morning_afternoon" in R:
        S["corr_morning_afternoon"] = A.boot_mean(R.corr_morning_afternoon)
    (A.OUT / "claim5_summary.json").write_text(json.dumps(S, indent=1, default=float), encoding="utf-8")
    print(json.dumps(S, indent=1, default=float))


if __name__ == "__main__":
    main()
