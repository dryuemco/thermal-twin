"""rstar_precheck.py: R* pre-check of plan 14.2 on task G-C. Exploratory.

Events: on each site's buffered grid, burned cells of a calendar year joined by 8-connectivity when their burn dates
differ by at most 7 days; area from the cell size at the site's latitude; start = earliest burn date. Large summer
event: area >= 100 ha and start from 1 June to 30 September.
G-C target for cut-off T (1 May T): population cells of the panel in year T burned in large summer events of the
calendar years T and T + 1. Compared on it (AUC within site-year; >= 30 positives and negatives):
  (i)  R1, burn density from all burns known at the cut-off (h = 2 km, no decay; as in the protocol)
  (ii) density (h = 2 km, no decay) from cells of past large summer events only (calendar years <= T - 1)
Wildfire version: cells burned 3 or more times in the 10 earlier target years removed.
Writes rstar_precheck.csv and rstar_precheck_summary.json in $THERMAL_TWIN_SCALEUP/analysis/tma/dev/.
"""
import json
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
from scipy import ndimage

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "geonull"))
sys.path.insert(0, str(HERE))
import geonull as G  # noqa: E402
import tma_dev as D  # noqa: E402

EV = D.ROOT / "events"
CELL = 0.0045814 * 111.32


def events_mask(doy, year, lat):
    """Boolean grid of cells in large summer events for one calendar year."""
    H, W = doy.shape
    burned = doy > 0
    idx = -np.ones((H, W), int)
    idx[burned] = np.arange(burned.sum())
    parent = np.arange(burned.sum())

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    rr, cc = np.where(burned)
    for dr, dc in ((0, 1), (1, -1), (1, 0), (1, 1)):
        r2, c2 = rr + dr, cc + dc
        ok = (r2 >= 0) & (r2 < H) & (c2 >= 0) & (c2 < W)
        a, b = (rr[ok], cc[ok]), (r2[ok], c2[ok])
        both = burned[b] & (np.abs(doy[a] - doy[b]) <= 7)
        for i, j in zip(idx[a][both], idx[b][both]):
            ri, rj = find(i), find(j)
            if ri != rj:
                parent[ri] = rj
    roots = np.array([find(i) for i in range(len(parent))])
    area_ha = CELL * CELL * np.cos(np.radians(lat)) * 100
    df = pd.DataFrame({"root": roots, "doy": doy[burned]})
    ev = df.groupby("root").agg(n=("doy", "size"), start=("doy", "min"))
    jun1 = date(year, 6, 1).timetuple().tm_yday
    sep30 = date(year, 9, 30).timetuple().tm_yday
    big = ev[(ev.n * area_ha >= 100) & (ev.start >= jun1) & (ev.start <= sep30)].index
    out = np.zeros((H, W), bool)
    out[rr, cc] = np.isin(roots, big)
    return out


def main():
    S = D.load()
    rows = []
    for site, g in S.groupby("site"):
        with rasterio.open(EV / f"{site}.tif") as r:
            doy = r.read().astype(float)
            lat = r.transform.f + r.transform.e * r.height / 2
        meta = json.loads((EV / f"{site}.json").read_text())
        b = meta["buffer_cells"]
        big = {2001 + k: events_mask(doy[k], 2001 + k, lat) for k in range(doy.shape[0])}
        for T in range(D.T_FIRST, 2026):
            cur = g[g.year == T]
            if cur.empty:
                continue
            r0, c0 = cur.row.to_numpy() + b, cur.col.to_numpy() + b
            tgt = (big[T][r0, c0] | big.get(T + 1, np.zeros_like(big[T]))[r0, c0]).astype(int)
            past = np.zeros_like(doy[0])
            for u in range(2001, T):
                past += big[u]
            dens2 = ndimage.gaussian_filter(past, sigma=2.0 / CELL)[r0, c0]
            r1 = cur.density_h2_tauinf.to_numpy()
            for tg, keep in (("all", np.ones(len(cur), bool)), ("wildfire", (cur.burns_10y.fillna(0) < 3).to_numpy())):
                yy = tgt[keep]
                if yy.sum() < 30 or (1 - yy).sum() < 30 or not np.isfinite(r1[keep]).all():
                    continue
                rows.append({"site": site, "T": T, "target": tg, "positives": int(yy.sum()),
                             "auc_r1": G.auc(yy, r1[keep]), "auc_large_summer": G.auc(yy, dens2[keep])})
        print(site, flush=True)
    R = pd.DataFrame(rows)
    R.to_csv(D.OUT / "rstar_precheck.csv", index=False)
    summ = {}
    for tg, g in R.groupby("target"):
        d = g.auc_large_summer - g.auc_r1
        summ[tg] = {"site_years": int(len(g)), "sites": int(g.site.nunique()), "auc_r1": float(g.auc_r1.mean()),
                    "auc_large_summer": float(g.auc_large_summer.mean()), "diff": float(d.mean()),
                    "large_summer_better": int((d > 0).sum())}
    summ["full_rstar_tried"] = bool(summ.get("all", {}).get("diff", 0) >= 0.01)
    (D.OUT / "rstar_precheck_summary.json").write_text(json.dumps(summ, indent=1), encoding="utf-8")
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    main()
