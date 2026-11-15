"""protocol_dev.py: checkpoint 2 of amendment 14, the protocol table on the development data (plan 14.1, 14.9).
Exploratory. Tasks G-A (transitions), G-B (first-May map after the focal fire against later burning), G-C (large
summer events of the next two summers); targets all burns and wildfire; references R1 (2 km burn density), R0 (site
climatology) and RM (logistic combination of R0 and R1); Platt calibration out of group on outcomes known at the
cut-off; delta AUC, BSS, LSS, AP, top-10% capture; honesty; cluster bootstrap.
Outputs in $THERMAL_TWIN_SCALEUP/analysis/tma/dev/ (protocol_dev_*).
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
from scipy import ndimage
from scipy.special import expit
from sklearn.metrics import average_precision_score

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "geonull"))
sys.path.insert(0, str(HERE.parent / "scaleup"))
sys.path.insert(0, str(HERE))
import geonull as G  # noqa: E402
import tma_dev as D  # noqa: E402
import env_baseline as E  # noqa: E402
import baseline_explore as BX  # noqa: E402
import rstar_precheck as RS  # noqa: E402
from s2_label_check_export import grid_path, regions  # noqa: E402

OUT = D.OUT
SC16 = D.ROOT.parent / "claim16_scores"
G1_FIRES = D.ROOT.parent / "claim14_future_per_fire.csv"
KEYS = ["site", "year", "row", "col"]
NB, SEED, PER_UNIT, EPS = 10000, 42, 1000, 1e-4
CELL = 0.0045814 * 111.32
GC_LAST = 2024
MODELS = {                                   # name: (column, scale for Platt)
    "pooled_forest": ("pooled_monthly", "prob"),
    "local_forest": ("local", "prob"),
    "learned_blend": ("f_only", "logit"),
    "tma": ("tma", "logit"),
    "tma_cell": ("tma_cell", "logit"),
    "standard_spatial": ("standard_spatial", "logit"),
    "coord_dist_forest": ("coord_dist_forest", "prob"),
    "pooled_forest_density_rank": ("pooled_density_rank", "prob"),
    "large_summer_density": ("ls_density", "dens"),
    "R1": ("density", "dens"),
}


def to_x(v, scale):
    v = np.asarray(v, float)
    if scale == "prob":
        p = np.clip(v, EPS, 1 - EPS)
        return np.log(p / (1 - p))
    if scale == "dens":
        return np.log(v + 1e-3)
    return v


# ---------------------------------------------------------------- scores
def load():
    S = pd.read_parquet(OUT / "tma_scores.parquet", columns=KEYS + ["y", "incomplete", "tma", "f_only", "density",
                                                                   "coord_dist_forest", "standard_spatial"])
    B = pd.read_parquet(D.ROOT / "explore" / "baseline_explore_scores.parquet", columns=KEYS + ["pooled_monthly", "local"])
    P = pd.read_parquet(D.ROOT / "panel.parquet", columns=KEYS + ["burns_10y"])
    S = S.merge(B, on=KEYS, how="left").merge(P, on=KEYS, how="left")
    groups = json.loads((HERE.parent / "scaleup" / "selection" / "site_groups.json").read_text())
    grp = {s: i for i, (_, ss) in enumerate(sorted(groups.items())) for s in ss}
    S["grp"] = S.site.map(grp)
    return S.sort_values(KEYS).reset_index(drop=True), grp


def tma_cell(S, grp):
    """TMA-cell scores of plan 13.14 for the configuration its gate chose per (group, T)."""
    gl = pd.read_csv(OUT / "tma_cell_gate_log.csv")
    choice = {(int(r.grp), int(r.T)): r.choice for r in gl.itertuples()}
    out = np.full(len(S), np.nan)
    pe = expit(S.f_only.to_numpy())
    for site, g in S.groupby("site"):
        H, W = g.row.max() + 1, g.col.max() + 1
        O, Ex = {}, {}
        for t, gt in g[(g.incomplete == 0) & g.f_only.notna() & (g.year >= D.T_FIRST)].groupby("year"):
            m = np.zeros((H, W))
            m[gt.row, gt.col] = gt.y.to_numpy()
            O[t] = ndimage.gaussian_filter(m, sigma=2.0 / CELL)
            m = np.zeros((H, W))
            m[gt.row, gt.col] = pe[gt.index]
            Ex[t] = ndimage.gaussian_filter(m, sigma=2.0 / CELL)
        for T in range(D.T_FIRST + 1, 2027):
            c = choice.get((grp[site], T))
            cur = g[g.year == T]
            if c is None or cur.empty or cur.f_only.isna().all():
                continue
            k, tau, gm = c.split("_")[1:]
            k, gm = float(k[1:]), float(gm[1:])
            tau = None if tau == "tinf" else float(tau[1:])
            ts = [t for t in O if t <= T - 1]
            rr, cc = cur.row.to_numpy(), cur.col.to_numpy()
            if ts:
                w = {t: 1.0 if tau is None else np.exp(-(T - t) / tau) for t in ts}
                so = sum(w[t] * O[t] for t in ts)[rr, cc]
                se = sum(w[t] * Ex[t] for t in ts)[rr, cc]
                lrr = np.log((so + k) / (se + k))
            else:
                lrr = np.zeros(len(cur))
            out[cur.index] = cur.f_only.to_numpy() + gm * lrr
        print(site, "TMA-cell", flush=True)
    return out


def pooled_density_rank(S, grp):
    cache = OUT / "protocol_pooled_density_rank.parquet"
    if cache.exists():
        return S.merge(pd.read_parquet(cache), on=KEYS, how="left").pooled_density_rank.to_numpy()
    P = BX.add_extra(E.load())
    P = P[P.year >= D.T_FIRST - 1].merge(S[KEYS + ["density"]].rename(columns={"density": "density_h2_tauinf"}),
                                         on=KEYS, how="left")
    P["density_rank"] = P.groupby(["site", "year"]).density_h2_tauinf.rank(pct=True)
    P["grp"] = P.site.map(grp)
    TS = E.training_sample(P)
    TS["grp"] = TS.site.map(grp)
    P["pooled_density_rank"] = BX.pooled_scores(P, TS, E.FEATS + ["months_since_burn", "density_rank"])
    P[KEYS + ["pooled_density_rank"]].to_parquet(cache, index=False)
    print("pooled forest + density rank", flush=True)
    return S.merge(P[KEYS + ["pooled_density_rank"]], on=KEYS, how="left").pooled_density_rank.to_numpy()


def events(S):
    """Large-summer-event grids per site and calendar year (original grid), and the density of past large summer
    events (calendar years <= T - 1, h = 2 km) for every row."""
    big, dens = {}, np.full(len(S), np.nan)
    for site, g in S.groupby("site"):
        with rasterio.open(RS.EV / f"{site}.tif") as r:
            doy = r.read().astype(float)
            lat = r.transform.f + r.transform.e * r.height / 2
        b = json.loads((RS.EV / f"{site}.json").read_text())["buffer_cells"]
        bg = {2001 + k: RS.events_mask(doy[k], 2001 + k, lat) for k in range(doy.shape[0])}
        big[site] = {y: m[b:-b, b:-b] for y, m in bg.items()}
        for T, cur in g.groupby("year"):
            past = np.zeros(doy.shape[1:])
            for u in range(2001, T):
                past += bg[u]
            d = ndimage.gaussian_filter(past, sigma=2.0 / CELL)
            dens[cur.index] = d[cur.row.to_numpy() + b, cur.col.to_numpy() + b]
        print(site, "events", flush=True)
    return big, dens


def climatology(S):
    P = pd.read_parquet(D.ROOT / "panel.parquet", columns=["site", "year", "y", "incomplete"])
    r = P[P.incomplete == 0].groupby(["site", "year"]).y.mean().reset_index()
    out = {}
    for s, g in r.groupby("site"):
        for T in range(2002, 2027):
            h = g[g.year <= T - 1]
            out[(s, T)] = h.y.mean() if len(h) else np.nan
    return S.set_index(["site", "year"]).index.map(out).to_numpy(dtype=float)


def thermal(S):
    out = np.full(len(S), np.nan)
    within = {}
    sup = set(pd.read_csv(G1_FIRES).fire)
    for site in sup:
        T0 = int(regions.EXPERIMENTS[site]["label_start_date"][:4]) + 1
        d = np.load(SC16 / f"{site}.npz")
        within[site] = G.auc(d["y"], d["thermal"])
        cur = S[(S.site == site) & (S.year == T0)]
        f = pd.Series(d["thermal"], index=pd.MultiIndex.from_arrays([d["row"], d["col"]]))
        out[cur.index] = f.reindex(pd.MultiIndex.from_arrays([cur.row, cur.col])).to_numpy()
        print(site, "thermal coverage", float(np.isfinite(out[cur.index]).mean()), flush=True)
    return out, within


# ---------------------------------------------------------------- labels and units
def label_grids(S):
    """Per site: any-burn and wildfire-patch burn grids per target year (population cells), and the wildfire keep
    mask of G-A rows."""
    Y, Yb = {}, {}
    kw = np.zeros(len(S), bool)
    for site, g in S.groupby("site"):
        H, W = g.row.max() + 1, g.col.max() + 1
        Y[site], Yb[site] = {}, {}
        for t, gt in g.groupby("year"):
            k = D.wildfire_keep(gt)
            kw[gt.index] = k
            a = np.zeros((H, W), bool)
            a[gt.row, gt.col] = gt.y.to_numpy() == 1
            bb = np.zeros((H, W), bool)
            sel = (gt.y.to_numpy() == 1) & k
            bb[gt.row.to_numpy()[sel], gt.col.to_numpy()[sel]] = True
            Y[site][t], Yb[site][t] = a, bb
    return Y, Yb, kw


def window(grids, site, a, b, shape):
    out = np.zeros(shape, bool)
    for t in range(a, b + 1):
        if t in grids[site]:
            out |= grids[site][t]
    return out


def gb_labels(g, Y, Yb, site, u, h, tg):
    """Label and keep mask of the rows g (one site, cut-off u) for horizon h (years u .. u + h - 1)."""
    shape = Y[site][u].shape
    rr, cc = g.row.to_numpy(), g.col.to_numpy()
    lab = window(Y, site, u, u + h - 1, shape)[rr, cc]
    if tg == "all":
        return lab.astype(int), np.ones(len(g), bool)
    labw = window(Yb, site, u, u + h - 1, shape)[rr, cc]
    keep = (g.burns_10y.fillna(0).to_numpy() < 3) & ~(lab & ~labw)
    return labw.astype(int), keep


def gc_labels(g, big, site, T, tg):
    rr, cc = g.row.to_numpy(), g.col.to_numpy()
    lab = (big[site][T][rr, cc] | big[site][T + 1][rr, cc]).astype(int)
    keep = np.ones(len(g), bool) if tg == "all" else g.burns_10y.fillna(0).to_numpy() < 3
    return lab, keep


# ---------------------------------------------------------------- calibration
def platt(X, y):
    X1 = np.c_[np.ones(len(y)), X]
    th = np.zeros(X1.shape[1])
    th[0] = np.log(max(y.mean(), 1e-6) / max(1 - y.mean(), 1e-6))
    for _ in range(50):
        p = expit(X1 @ th)
        Hm = (X1 * (p * (1 - p))[:, None]).T @ X1 + 1e-6 * np.eye(len(th))
        step = np.linalg.solve(Hm, X1.T @ (y - p))
        th += step
        if np.max(np.abs(step)) < 1e-8:
            break
    return th


def predict(th, X):
    return np.clip(expit(th[0] + X @ th[1:]), EPS, 1 - EPS)


# ---------------------------------------------------------------- metrics
def top10(y, s, rng):
    n10 = int(np.ceil(0.1 * len(y)))
    o = np.lexsort((rng.random(len(y)), -s))
    return y[o[:n10]].sum() / y.sum()


def losses(y, p):
    return np.mean((p - y) ** 2), np.mean(-(y * np.log(p) + (1 - y) * np.log(1 - p)))


def clusters(sites):
    box = {}
    for s in sites:
        with rasterio.open(grid_path(s)) as g:
            box[s] = g.bounds
    parent = {s: s for s in sites}

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x
    for i, a in enumerate(sites):
        for b in sites[i + 1:]:
            A, B = box[a], box[b]
            if A.left <= B.right and B.left <= A.right and A.bottom <= B.top and B.bottom <= A.top:
                parent[find(a)] = find(b)
    return {s: find(s) for s in sites}


# ---------------------------------------------------------------- tasks
def build_units(S, Y, Yb, kw, big):
    """List of (task, target, horizon, unit dict with row index, labels, keep, cal key, cut-off)."""
    units = []
    for site, g in S.groupby("site"):
        fy = int(regions.EXPERIMENTS[site]["label_start_date"][:4])
        T0 = fy + 1
        for T, cur in g.groupby("year"):
            idx = cur.index.to_numpy()
            if T >= D.T_FIRST + 1 and cur.incomplete.iloc[0] == 0:
                for tg, keep in (("all", np.ones(len(cur), bool)), ("wildfire", kw[idx])):
                    units.append(dict(task="G-A", target=tg, horizon="", site=site, T=T, idx=idx, y=cur.y.to_numpy(),
                                      keep=keep, key=(T,)))
            if D.T_FIRST <= T <= GC_LAST:
                for tg in ("all", "wildfire"):
                    lab, keep = gc_labels(cur, big, site, T, tg)
                    units.append(dict(task="G-C", target=tg, horizon="", site=site, T=T, idx=idx, y=lab, keep=keep,
                                      key=(T,)))
            if T == T0:
                scar = window(Y, site, fy, fy, Y[site][T0].shape)[cur.row.to_numpy(), cur.col.to_numpy()]
                m = cur[~scar]
                for hz, h in (("all", 2027 - T0), ("two_year", 2)):
                    for tg in ("all", "wildfire"):
                        lab, keep = gb_labels(m, Y, Yb, site, T0, h, tg)
                        units.append(dict(task="G-B", target=tg, horizon=hz, site=site, T=T0, idx=m.index.to_numpy(),
                                          y=lab, keep=keep, key=(T0, h)))
    return units


def history(S, Y, Yb, kw, big, samp, grp_id, task, tg, key, sites_by_grp):
    """Calibration history: sampled rows of sites outside the group with outcomes known at the cut-off."""
    idx, lab = [], []
    for site in [s for g_, ss in sites_by_grp.items() if g_ != grp_id for s in ss]:
        for (s, u), (rows, g) in samp.get(site, {}).items():
            if task == "G-A":
                if not (D.T_FIRST <= u <= key[0] - 1) or g.incomplete.iloc[0]:
                    continue
                y, keep = g.y.to_numpy(), (np.ones(len(g), bool) if tg == "all" else kw[rows])
            elif task == "G-B":
                T0, h = key
                if not (D.T_FIRST <= u and u + h - 1 <= T0 - 1):
                    continue
                y, keep = gb_labels(g, Y, Yb, site, u, h, tg)
            else:
                if not (D.T_FIRST <= u <= key[0] - 2):
                    continue
                y, keep = gc_labels(g, big, site, u, tg)
            idx.append(rows[keep])
            lab.append(y[keep])
    if not idx:
        return None, None
    return np.concatenate(idx), np.concatenate(lab)


def main():
    S, grp = load()
    print("loaded", len(S), flush=True)
    S["tma_cell"] = tma_cell(S, grp)
    S["pooled_density_rank"] = pooled_density_rank(S, grp)
    big, S["ls_density"] = events(S)
    S["clim"] = climatology(S)
    S["thermal"], within = thermal(S)
    Y, Yb, kw = label_grids(S)
    print("labels", flush=True)
    sites = sorted(S.site.unique())
    sites_by_grp = {}
    for s in sites:
        sites_by_grp.setdefault(grp[s], []).append(s)
    cl = clusters(sites)
    rng = np.random.default_rng(SEED)
    samp = {}
    for (s, u), g in S.groupby(["site", "year"]):
        rows = np.sort(rng.choice(g.index.to_numpy(), min(PER_UNIT, len(g)), replace=False))
        samp.setdefault(s, {})[(s, u)] = (rows, S.loc[rows, ["row", "col", "y", "incomplete", "burns_10y"]])
    X = {m: to_x(S[c].to_numpy(), sc) for m, (c, sc) in MODELS.items()}
    X["R0"] = to_x(S.clim.to_numpy(), "prob")
    units = build_units(S, Y, Yb, kw, big)
    print("units", len(units), flush=True)

    cal, cal_log = {}, []
    rows, rng_t = [], np.random.default_rng(SEED)
    for u in units:
        gid = grp[u["site"]]
        ck = (u["task"], u["target"], gid) + u["key"]
        if ck not in cal:
            hi, hy = history(S, Y, Yb, kw, big, samp, gid, u["task"], u["target"], u["key"], sites_by_grp)
            th = {}
            if hi is not None and hy.sum() >= 50:
                for m in list(MODELS) + ["R0"]:
                    ok = np.isfinite(X[m][hi])
                    if ok.sum() > 1000 and hy[ok].sum() >= 50:
                        th[m] = platt(X[m][hi][ok, None], hy[ok].astype(float))
                ok = np.isfinite(X["R1"][hi]) & np.isfinite(X["R0"][hi])
                if ok.sum() > 1000:
                    th["RM"] = platt(np.c_[X["R0"][hi][ok], X["R1"][hi][ok]], hy[ok].astype(float))
            cal[ck] = th
            cal_log.append({"task": ck[0], "target": ck[1], "grp": gid, "key": str(u["key"]),
                            "n_hist": 0 if hi is None else int(len(hi)), "pos_hist": 0 if hy is None else int(hy.sum()),
                            **{f"slope_{m}": float(v[-1]) for m, v in th.items() if m != "RM"}})
        th = cal[ck]
        if "R1" not in th or "R0" not in th or "RM" not in th:
            continue
        idx, y, keep = u["idx"], u["y"], u["keep"]
        r1x, r0x = X["R1"][idx], X["R0"][idx]
        cands = [m for m in MODELS if m in th] + (["thermal"] if u["task"] == "G-B" else [])
        for m in cands:
            mx = S.thermal.to_numpy()[idx] if m == "thermal" else X[m][idx]
            ok = keep & np.isfinite(mx) & np.isfinite(r1x) & np.isfinite(r0x)
            yy = y[ok]
            if yy.sum() < 30 or (1 - yy).sum() < 30:
                continue
            r = {"task": u["task"], "target": u["target"], "horizon": u["horizon"], "site": u["site"], "T": u["T"],
                 "cluster": cl[u["site"]], "grp": gid, "model": m, "cells": int(ok.sum()), "positives": int(yy.sum()),
                 "coverage": float(ok.sum() / keep.sum()), "prevalence": float(yy.mean()),
                 "auc_m": G.auc(yy, mx[ok]), "auc_r1": G.auc(yy, r1x[ok]),
                 "ap_m": average_precision_score(yy, mx[ok]), "ap_r1": average_precision_score(yy, r1x[ok]),
                 "top10_m": top10(yy, mx[ok], rng_t), "top10_r1": top10(yy, r1x[ok], rng_t)}
            if m != "thermal":
                pm = predict(th[m], mx[ok, None])
                pr1 = predict(th["R1"], r1x[ok, None])
                pr0 = predict(th["R0"], r0x[ok, None])
                prm = predict(th["RM"], np.c_[r0x[ok], r1x[ok]])
                for nm, p in (("m", pm), ("r1", pr1), ("r0", pr0), ("rm", prm)):
                    r[f"bs_{nm}"], r[f"ls_{nm}"] = losses(yy, p)
            rows.append(r)
        if len(rows) % 2000 < len(cands):
            print(len(rows), "unit rows", flush=True)
    U = pd.DataFrame(rows)
    U.to_csv(OUT / "protocol_dev_units.csv", index=False)
    pd.DataFrame(cal_log).to_csv(OUT / "protocol_dev_calibration.csv", index=False)

    # honesty: estimate available at the cut-off minus realised AUC
    hon = []
    GA = U[U.task == "G-A"]
    for r in U.itertuples():
        base = GA[(GA.target == r.target) & (GA.model == r.model)] if r.task in ("G-A", "G-B") else \
            U[(U.task == "G-C") & (U.target == r.target) & (U.model == r.model)]
        lim = r.T - 1 if r.task in ("G-A", "G-B") else r.T - 2
        known = base[base["T"] <= lim]
        cross = known[known.grp != r.grp].auc_m
        own = known[known.site == r.site].auc_m
        h = {"task": r.task, "target": r.target, "horizon": r.horizon, "site": r.site, "T": r.T, "cluster": r.cluster,
             "model": r.model, "realised": r.auc_m,
             "cross_site": cross.mean() - r.auc_m if len(cross) else np.nan,
             "own_history": own.mean() - r.auc_m if len(own) else np.nan}
        if r.model == "thermal":
            h["within_event"] = within[r.site] - r.auc_m
        hon.append(h)
    Hn = pd.DataFrame(hon)
    Hn.to_csv(OUT / "protocol_dev_honesty_units.csv", index=False)

    # table with cluster bootstrap
    rng_b = np.random.default_rng(SEED)
    out, hout = [], []
    for (task, tg, hz, m), g in U.groupby(["task", "target", "horizon", "model"], sort=False):
        cs = sorted(g.cluster.unique())
        ci = g.cluster.map({c: i for i, c in enumerate(cs)}).to_numpy()
        C = np.stack([np.bincount(rng_b.choice(len(cs), len(cs)), minlength=len(cs)) for _ in range(NB)])

        def csum(v):
            return np.bincount(ci, weights=np.nan_to_num(v), minlength=len(cs))

        def stat(num, den, ratio):
            pt = num.sum() / den.sum()
            bs = (C @ num) / (C @ den)
            pt, bs = (1 - pt, 1 - bs) if ratio else (pt, bs)
            lo, hi = np.nanpercentile(bs, [2.5, 97.5])
            return float(pt), float(lo), float(hi)
        r = {"task": task, "target": tg, "horizon": hz, "model": m, "units": int(len(g)), "clusters": len(cs),
             "sites": int(g.site.nunique()), "coverage": float(g.coverage.mean()), "auc_m": float(g.auc_m.mean()),
             "auc_r1": float(g.auc_r1.mean()), "ap_m": float(g.ap_m.mean()), "ap_r1": float(g.ap_r1.mean()),
             "prevalence": float(g.prevalence.mean()), "top10_m": float(g.top10_m.mean()),
             "top10_r1": float(g.top10_r1.mean())}
        n = csum(np.ones(len(g)))
        r["dauc"], r["dauc_lo"], r["dauc_hi"] = stat(csum((g.auc_m - g.auc_r1).to_numpy()), n, False)
        r["model_better_units"] = int((g.auc_m > g.auc_r1).sum())
        if m != "thermal":
            for loss in ("bs", "ls"):
                for ref in ("r1", "r0", "rm"):
                    k = f"{'bss' if loss == 'bs' else 'lss'}_{ref}"
                    r[k], r[k + "_lo"], r[k + "_hi"] = stat(csum(g[f"{loss}_m"].to_numpy()),
                                                            csum(g[f"{loss}_{ref}"].to_numpy()), True)
            for ref in ("r0", "rm"):
                k = f"bss_r1_vs_{ref}"
                r[k] = float(1 - g.bs_r1.sum() / g[f"bs_{ref}"].sum())
        out.append(r)
        h = Hn[(Hn.task == task) & (Hn.target == tg) & (Hn.horizon == hz) & (Hn.model == m)]
        hr = {"task": task, "target": tg, "horizon": hz, "model": m}
        for est in ("cross_site", "own_history", "within_event"):
            if est in h and h[est].notna().any():
                v = h[est].dropna()
                hr[f"{est}_n"] = int(len(v))
                hr[f"{est}_mean"] = float(v.mean())
                hr[f"{est}_mae"] = float(v.abs().mean())
        hout.append(hr)
    T = pd.DataFrame(out)
    T.to_csv(OUT / "protocol_dev_table.csv", index=False)
    pd.DataFrame(hout).to_csv(OUT / "protocol_dev_honesty.csv", index=False)
    neg = {k: int(sum(1 for c in cal.values() if k in c and c[k][-1] <= 0)) for k in list(MODELS) + ["R0"]}
    rep = {}
    ref = pd.read_csv(OUT / "tma_cell_transitions.csv")
    ref = ref[ref.target == "all"]
    for m, col in (("tma_cell", "tma_cell"), ("pooled_forest_density_rank", "pooled_density_rank"), ("R1", "density")):
        a = U[(U.task == "G-A") & (U.target == "all") & (U.model == m)].merge(
            ref[["site", "year", col]], left_on=["site", "T"], right_on=["site", "year"]).dropna(subset=[col])
        rep[m] = {"n": int(len(a)), "max_abs_diff": float((a.auc_m - a[col]).abs().max())}
    summ = {"units_rows": int(len(U)), "clusters": len(set(cl.values())), "negative_platt_slopes": neg,
            "reproduces_checkpoint_1": rep,
            "thermal_within_event_auc": within,
            "ga_all": T[(T.task == "G-A") & (T.target == "all")][["model", "units", "auc_m", "dauc", "dauc_lo",
                                                                   "dauc_hi"]].to_dict("records")}
    (OUT / "protocol_dev_summary.json").write_text(json.dumps(summ, indent=1, default=float), encoding="utf-8")
    pd.set_option("display.width", 250)
    print(T[["task", "target", "horizon", "model", "units", "auc_m", "auc_r1", "dauc", "dauc_lo", "dauc_hi",
             "bss_r1", "lss_r1", "bss_r0", "top10_m", "top10_r1"]].round(3).to_string())


if __name__ == "__main__":
    main()
