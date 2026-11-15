"""panel_build.py: TMA checkpoint 2, builds the cell-year panel of the 31 development sites from the exported
GeoTIFFs and reports support per site-year. Anomalies and burn history use earlier years only.

Population of site l in year y: cells of the site's grid with natural share >= 0.5 (map of 13.10), all four
MODIS predictors finite, and unmapped share <= 0.10 over the target months. Target: burn share >= 0.5.
Predictors at cut-off y: ndvi, evi, lst_day, lst_night; anomalies lst_*_anom = value minus the mean of the same
site-cell over the earlier years 2001..y-1 (missing when fewer than ANOM_MIN earlier years); elevation, slope;
burn history from the targets of earlier years (and the Nov 2000 - Apr 2001 burns): years since the last burn
(capped, with a censoring flag when no burn has been seen since November 2000), the number of burns in the
previous 10 target years, and a fuel deficit sum_u B_u exp(-(y - u) / TAU).
Writes panel.parquet and support.csv in $THERMAL_TWIN_SCALEUP/analysis/tma.
"""
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio

ROOT = Path(os.environ["THERMAL_TWIN_SCALEUP"]) / "analysis" / "tma"
YEARS = list(range(2001, 2027))
ANOM_MIN, TAU, BLOCK = 3, 8.0, 10
NAMES = ["ndvi", "evi", "lst_day", "lst_night", "burn", "unmapped", "natural"]


def read(p):
    with rasterio.open(p) as r:
        a = r.read().astype("float64")
    a[~np.isfinite(a)] = np.nan
    return a


def site_panel(site):
    d = ROOT / "panel" / site
    st = read(d / "static.tif")
    stack = {y: read(d / f"{y}.tif") for y in YEARS}
    h, w = st.shape[1:]
    rr, cc = np.mgrid[0:h, 0:w]
    rr, cc = rr.ravel(), cc.ravel()
    B = np.stack([(np.nan_to_num(stack[y][4].ravel()) >= 0.5).astype(float) for y in YEARS])   # target burns by year
    pre = np.nan_to_num(st[2].ravel()) >= 0.5
    rows = []
    for k, y in enumerate(YEARS):
        a = stack[y]
        v = {n: a[i].ravel() for i, n in enumerate(NAMES)}
        pop = (v["natural"] >= 0.5) & np.isfinite(v["ndvi"]) & np.isfinite(v["evi"]) & np.isfinite(v["lst_day"]) \
            & np.isfinite(v["lst_night"]) & (np.nan_to_num(v["unmapped"], nan=1.0) <= 0.10)
        past = B[:k]                                           # targets of earlier years (all end before 1 May y)
        seen = past.any(axis=0) | pre
        last = np.full(len(rr), np.nan)
        for j in range(k):
            last[past[j] > 0] = k - j
        last[np.isnan(last) & pre] = k + 0.5
        df = pd.DataFrame({"site": site, "year": y, "row": rr, "col": cc, "ndvi": v["ndvi"], "evi": v["evi"],
                           "lst_day": v["lst_day"], "lst_night": v["lst_night"], "elevation": st[0].ravel(),
                           "slope": st[1].ravel(), "years_since_burn": np.where(seen, last, k + 1.0),
                           "censored": (~seen).astype(int),
                           "burns_10y": past[max(0, k - 10):k].sum(axis=0) if k else 0.0,
                           "fuel_deficit": (past * np.exp(-(k - np.arange(k))[:, None] / TAU)).sum(axis=0) if k else 0.0,
                           "y": (np.nan_to_num(v["burn"]) >= 0.5).astype(int), "incomplete": int(y == 2026)})
        for n in ("lst_day", "lst_night", "ndvi"):
            prev = np.stack([stack[u][NAMES.index(n)].ravel() for u in YEARS[:k]]) if k else None
            cnt = np.isfinite(prev).sum(axis=0) if k else 0
            mean = np.nanmean(prev, axis=0) if k else np.nan
            df[f"{n}_anom"] = np.where(cnt >= ANOM_MIN, v[n] - mean, np.nan) if k else np.nan
        rows.append(df[pop])
    return pd.concat(rows, ignore_index=True)


def main():
    sites = sorted(p.name for p in (ROOT / "panel").iterdir() if p.is_dir())
    parts, sup = [], []
    for s in sites:
        P = site_panel(s)
        parts.append(P)
        for y, g in P.groupby("year"):
            blocks = (g.row // BLOCK).astype(str) + "_" + (g.col // BLOCK).astype(str)
            sup.append({"site": s, "year": y, "cells": len(g), "positives": int(g.y.sum()),
                        "blocks_with_positives": int(blocks[g.y == 1].nunique()),
                        "censored_share": float(g.censored.mean()),
                        "anom_missing_share": float(g.lst_day_anom.isna().mean()),
                        "incomplete": int(y == 2026)})
        print(s, len(P), flush=True)
    panel = pd.concat(parts, ignore_index=True)
    panel.to_parquet(ROOT / "panel.parquet", index=False)
    S = pd.DataFrame(sup)
    S.to_csv(ROOT / "support.csv", index=False)
    full = S[S.incomplete == 0]
    summ = {"sites": len(sites), "site_years": int(len(full)), "cells_total": int(len(panel)),
            "site_years_with_30_positives": int((full.positives >= 30).sum()),
            "site_years_with_any_positive": int((full.positives > 0).sum()),
            "per_site_years_with_30_positives": full[full.positives >= 30].groupby("site").size().reindex(sites, fill_value=0).to_dict(),
            "median_censored_share_2010": float(full[full.year == 2010].censored_share.median()),
            "median_censored_share_2020": float(full[full.year == 2020].censored_share.median())}
    (ROOT / "panel_summary.json").write_text(json.dumps(summ, indent=1), encoding="utf-8")
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    main()
