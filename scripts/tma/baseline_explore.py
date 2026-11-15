"""baseline_explore.py: short exploration of baseline candidates (plan 13, exploratory). Single selection criterion:
mean out-of-group AUC on past-to-next-year transitions (complete site-years with >= 30 positives). Later burning
of the first-May maps is NOT used here.

Candidates
  pooled_z          the checkpoint-3 baseline (within-site-year z, history), refitted with 200 trees
  pooled_abs_lst    LST and NDVI/EVI not standardised (absolute values)
  pooled_site_z     standardised within the site over target years <= T (expanding), not within the site-year
  pooled_monthly    plus months since the last burn at the cut-off (monthly resolution)
  pooled_aqua       plus Aqua night LST (2003 on; missing earlier)
  local             a forest on the site's own target years <= T - 1 only (sites with >= 100 earlier positives
                    over >= 2 years with burning)
  blend_rank        rank average of the best pooled variant and local (where local exists)
  blend_w           weight on the local rank chosen on transitions of earlier years (expanding, grid 0..1)
  density_h_tau     kernel density of burns known at the cut-off (Gaussian, h in {1, 2, 5, 10} km; tau in
                    {none, 8 years}); the selected (h, tau) is the burn-density comparator of TMA
Also a descriptive analysis of repeated burning (writes reburn_*.csv).
Outputs in $THERMAL_TWIN_SCALEUP/analysis/tma/explore/.
"""
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
from scipy import ndimage
from scipy.stats import rankdata
from sklearn.ensemble import RandomForestClassifier

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "geonull"))
import geonull as G  # noqa: E402
import env_baseline as E  # noqa: E402

ROOT = E.ROOT
OUT = ROOT / "explore"
YEARS = list(range(2001, 2027))
ORIGIN_DAYS = {y: (pd.Timestamp(y, 5, 1) - pd.Timestamp(2000, 11, 1)).days for y in YEARS}
TREES = 200


def add_extra(P):
    parts = []
    for s, g in P.groupby("site"):
        with rasterio.open(ROOT / "extra" / f"{s}.tif") as r:
            a = r.read().astype("float64")
        a[~np.isfinite(a)] = np.nan
        k = (g.year - 2001).to_numpy()
        rr, cc = g.row.to_numpy(), g.col.to_numpy()
        last = a[3 * k, rr, cc]
        myd = a[3 * k + 1, rr, cc]
        lc = a[3 * k + 2, rr, cc]
        cut = g.year.map(ORIGIN_DAYS).to_numpy()
        months = np.where(last > 0, (cut - last) / 30.44, np.nan)
        parts.append(g.assign(months_since_burn=months, myd_night=myd, lc_prev=lc))
    return pd.concat(parts)


def site_z_expanding(P, cols):
    out = {c: np.full(len(P), np.nan) for c in cols}
    for s, g in P.groupby("site"):
        for T in sorted(g.year.unique()):
            ref = g[g.year <= T]
            cur = (P.site == s) & (P.year == T)
            for c in cols:
                sd = ref[c].std() or 1.0
                out[c][cur.to_numpy()] = (P.loc[cur, c] - ref[c].mean()) / sd
    for c in cols:
        P[f"{c}_sz"] = out[c]
    return P


def pooled_scores(P, TS, feats, grp_col="grp"):
    raw = np.full(len(P), np.nan)
    for T in range(2004, 2026):
        for g in range(E.GROUPS):
            tr = TS[(TS[grp_col] != g) & (TS.year <= T - 1)]
            te = ((P[grp_col] == g) & (P.year == T)).to_numpy()
            if not te.any() or tr.y.sum() < 50:
                continue
            m = RandomForestClassifier(TREES, min_samples_leaf=5, max_features="sqrt", random_state=E.SEED, n_jobs=30)
            m.fit(tr[feats].fillna(-999), tr.y, sample_weight=tr.w)
            raw[te] = m.predict_proba(P.loc[te, feats].fillna(-999))[:, 1]
    return raw


def local_scores(P, feats):
    raw = np.full(len(P), np.nan)
    for s, g in P.groupby("site"):
        for T in range(2004, 2026):
            tr = g[g.year <= T - 1]
            yrs = tr.groupby("year").y.sum()
            if tr.y.sum() < 100 or (yrs > 0).sum() < 2:
                continue
            te = ((P.site == s) & (P.year == T)).to_numpy()
            neg = tr[tr.y == 0].sample(min(20000, int((tr.y == 0).sum())), random_state=E.SEED)
            t2 = pd.concat([tr[tr.y == 1], neg])
            m = RandomForestClassifier(TREES, min_samples_leaf=5, max_features="sqrt", class_weight="balanced",
                                       random_state=E.SEED, n_jobs=30).fit(t2[feats].fillna(-999), t2.y)
            raw[te] = m.predict_proba(P.loc[te, feats].fillna(-999))[:, 1]
    return raw


def density_scores(P, h_km, tau):
    """Kernel density of target-year burns u <= T - 1 (and the Nov 2000 - Apr 2001 burns) on each site grid."""
    out = np.full(len(P), np.nan)
    cell = 0.0045814 * 111.32
    for s, g in P.groupby("site"):
        H, W = g.row.max() + 1, g.col.max() + 1
        grids = {}
        for u, gu in g[g.y == 1].groupby("year"):
            m = np.zeros((H, W))
            m[gu.row, gu.col] = 1.0
            grids[u] = m
        for T in range(2002, 2026):
            acc = np.zeros((H, W))
            for u, m in grids.items():
                if u <= T - 1:
                    acc += m * (1.0 if tau is None else np.exp(-(T - u) / tau))
            d = ndimage.gaussian_filter(acc, sigma=h_km / cell)
            cur = ((P.site == s) & (P.year == T)).to_numpy()
            out[cur] = d[P.row.to_numpy()[cur], P.col.to_numpy()[cur]]
    return out


def transitions(P, col):
    rows = []
    for (s, y), g in P[P[col].notna() & (P.incomplete == 0) & (P.year >= 2004)].groupby(["site", "year"]):
        if g.y.sum() >= 30 and (1 - g.y).sum() >= 30:
            rows.append({"site": s, "year": y, "auc": G.auc(g.y, g[col])})
    return pd.DataFrame(rows)


def main():
    OUT.mkdir(exist_ok=True)
    P = add_extra(E.load())
    groups = json.loads((HERE.parent / "scaleup" / "selection" / "site_groups.json").read_text())
    grp = {s: i for i, (_, ss) in enumerate(sorted(groups.items())) for s in ss}
    P["grp"] = P.site.map(grp)
    P = site_z_expanding(P, ["ndvi", "evi", "lst_day", "lst_night"])
    base = E.FEATS
    variants = {"pooled_z": base,
                "pooled_abs_lst": ["ndvi", "evi", "lst_day", "lst_night"] + base[4:],
                "pooled_site_z": ["ndvi_sz", "evi_sz", "lst_day_sz", "lst_night_sz"] + base[4:],
                "pooled_monthly": base + ["months_since_burn"],
                "pooled_aqua": base + ["myd_night"]}
    TS = E.training_sample(P)
    TS["grp"] = TS.site.map(grp)
    res = {}
    for name, feats in variants.items():
        P[name] = pooled_scores(P, TS, feats)
        tr = transitions(P, name)
        res[name] = tr
        print(name, round(tr.auc.mean(), 4), len(tr), flush=True)
    best = max((k for k in variants), key=lambda k: res[k].auc.mean())
    P["local"] = local_scores(P, base + ["months_since_burn"])
    res["local"] = transitions(P, "local")
    print("local", round(res["local"].auc.mean(), 4), len(res["local"]), flush=True)
    rk = lambda v: pd.Series(v).groupby([P.site.to_numpy(), P.year.to_numpy()]).rank(pct=True).to_numpy()  # noqa: E731
    P["r_best"], P["r_local"] = rk(P[best]), rk(P["local"])
    P["blend_rank"] = np.where(P.r_local.notna(), (P.r_best + P.r_local) / 2, np.nan)
    res["blend_rank"] = transitions(P, "blend_rank")
    # expanding learned weight
    bw = np.full(len(P), np.nan)
    wl = []
    sy = []
    for (s, y), g in P[P.r_local.notna() & P.r_best.notna() & (P.incomplete == 0)].groupby(["site", "year"]):
        if g.y.sum() >= 30 and (1 - g.y).sum() >= 30:
            sy.append((y, g.y.to_numpy(), g.r_local.to_numpy(), g.r_best.to_numpy()))
    for T in range(2005, 2026):
        hist = [x for x in sy if x[0] < T]
        best_w, best_a = 0.5, -1
        for w in np.linspace(0, 1, 11):
            a = np.mean([G.auc(yy, w * rl + (1 - w) * rb) for _, yy, rl, rb in hist]) if hist else np.nan
            if np.isfinite(a) and a > best_a:
                best_w, best_a = w, a
        cur = ((P.year == T) & P.r_local.notna()).to_numpy()
        bw[cur] = best_w * P.r_local.to_numpy()[cur] + (1 - best_w) * P.r_best.to_numpy()[cur]
        wl.append({"T": T, "w_local": best_w})
    P["blend_w"] = bw
    res["blend_w"] = transitions(P, "blend_w")
    for h in (1, 2, 5, 10):
        for tau in (None, 8):
            k = f"density_h{h}_tau{tau or 'inf'}"
            P[k] = density_scores(P, h, tau)
            res[k] = transitions(P, k)
            print(k, round(res[k].auc.mean(), 4), flush=True)
    keys = list(res)
    common = set.intersection(*[set(zip(res[k].site, res[k].year)) for k in ("local", best)])
    summ = {}
    for k in keys:
        t = res[k]
        tc = t[[(s, y) in common for s, y in zip(t.site, t.year)]]
        summ[k] = {"all_mean": float(t.auc.mean()), "all_n": int(len(t)), "common_mean": float(tc.auc.mean()), "common_n": int(len(tc))}
    dens = {k: v for k, v in summ.items() if k.startswith("density")}
    summ["selected_pooled_variant"] = best
    summ["selected_density"] = max(dens, key=lambda k: dens[k]["all_mean"])
    summ["blend_w_by_year"] = wl
    (OUT / "baseline_explore_summary.json").write_text(json.dumps(summ, indent=1), encoding="utf-8")
    pd.concat([v.assign(candidate=k) for k, v in res.items()]).to_csv(OUT / "baseline_explore_transitions.csv", index=False)
    keep = ["site", "year", "row", "col", "y", "incomplete"] + keys
    P[[c for c in keep if c in P]].to_parquet(OUT / "baseline_explore_scores.parquet", index=False)
    print(json.dumps({k: v for k, v in summ.items() if k != "blend_w_by_year"}, indent=1))
    reburn(P)


def reburn(P):
    """Descriptive: relative risk of burning in year T for cells burned in T-5..T-1, by previous-year land-cover
    class, by size of the earlier burn patch, and by frequency (>= 3 burns in 10 years)."""
    rows = []
    for s, g in P[(P.incomplete == 0) & (P.year >= 2006)].groupby("site"):
        H, W = g.row.max() + 1, g.col.max() + 1
        burned = {u: gu for u, gu in g[g.y == 1].groupby("year")}
        for T, gt in g.groupby("year"):
            prev = np.zeros((H, W))
            for u in range(T - 5, T):
                if u in burned:
                    prev[burned[u].row, burned[u].col] = 1
            lab, n = ndimage.label(prev, structure=np.ones((3, 3)))
            size = np.bincount(lab.ravel())
            pcell = prev[gt.row, gt.col] > 0
            psize = size[lab[gt.row, gt.col]] * (lab[gt.row, gt.col] > 0)
            lcc = gt.lc_prev.to_numpy()
            cls = np.where((lcc >= 1) & (lcc <= 5), "forest", np.where((lcc >= 6) & (lcc <= 10), "shrub_grass", "other"))
            freq = gt.burns_10y.to_numpy() >= 3
            rows.append(pd.DataFrame({"site": s, "year": T, "y": gt.y.to_numpy(), "recent": pcell, "cls": cls,
                                      "patch": np.where(~pcell, "none", np.where(psize <= 4, "small<=4", "large>4")),
                                      "frequent": freq}))
    D = pd.concat(rows, ignore_index=True)
    out = []
    for key in ("cls", "patch", "frequent"):
        for v, g in D.groupby(key):
            r1 = g[g.recent].y.mean() if g.recent.any() else np.nan
            r0 = g[~g.recent].y.mean() if key == "cls" else D[~D.recent].y.mean()   # within class, else overall
            out.append({"split": key, "level": str(v), "cells_recent": int(g.recent.sum()), "rate_recent": r1,
                        "rate_not_recent": r0, "relative_risk": r1 / r0 if r0 else np.nan})
    R = pd.DataFrame(out)
    base_rr = D[D.recent].y.mean() / D[~D.recent].y.mean()
    R.to_csv(OUT / "reburn_relative_risk.csv", index=False)
    print("overall relative risk recent vs not:", round(base_rr, 2))
    print(R.round(4).to_string())


if __name__ == "__main__":
    main()
