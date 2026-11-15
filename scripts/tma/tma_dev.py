"""tma_dev.py: TMA checkpoint 4 (plan 13.2, 13.3, 13.12), development on the 31 sites. Exploratory.

Baseline f: the learned-weight blend of baseline_explore.py (pooled forest with monthly burn history + local forest;
where the local forest is missing, the pooled rank), Platt-calibrated per target year T on target years < T.
TMA, per site l:
  1 bases phi: Gaussian radial bases on square lattices of spacing s and width s, s in SCALES km, over the site grid
  2 for every complete target year t >= 2005: penalised logistic fit y ~ offset(logit p_E) + alpha + phi'a,
    ridge LAMBDA on a; a_hat_t and V_t = deff * H^-1, the model-based covariance inflated by the block design effect
    deff = tr(sandwich over 5 km blocks) / tr(H^-1), at least 1
  3 variance components per scale (sigma_P^2, sigma_U^2) by moments from the sites outside the site's geographic
    group and target years <= T - 1
  4 BLUP P_hat(l, T) = [C_P^-1 + sum_{t<=T-1} (C_U + V_t)^-1]^-1 sum (C_U + V_t)^-1 a_hat_t
  5 score S_gamma = logit p_E(T) + gamma phi' P_hat, gamma in GAMMAS, chosen for (group, T) by mean transition AUC
    of the sites outside the group over target years <= T - 1
Ablations: raw mean residual (gamma = 1), ungated BLUP (gamma = 1), gate on the raw mean.
Comparators read or fitted here: burn density (h = 2 km), f alone, pooled forest + density feature, local forest +
coordinates + distance to earlier burns, standard spatial model (pooled-year penalised logistic with persistent
bases and year intercepts, penalty chosen on earlier transitions).
Evaluation: transitions (complete site-years >= 30 positives) and the first-May map after the focal fire against
later burning, each for target (i) all burns and (ii) the wildfire target of 13.12; honesty of TMA's gate estimate.
Outputs in $THERMAL_TWIN_SCALEUP/analysis/tma/dev/.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
from scipy import ndimage
from scipy.spatial import cKDTree
from sklearn.ensemble import RandomForestClassifier

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "geonull"))
sys.path.insert(0, str(HERE.parent / "scaleup"))
import geonull as G  # noqa: E402
import env_baseline as E  # noqa: E402
import baseline_explore as BX  # noqa: E402
from s2_label_check_export import grid_path, regions  # noqa: E402

ROOT = E.ROOT
OUT = ROOT / "dev"
SCALES = (5.0, 10.0, 20.0)
LAMBDA = 1.0
GAMMAS = (0.0, 0.25, 0.5, 1.0)
T_FIRST = 2005
EPS = 1e-4


def logit(p):
    p = np.clip(p, EPS, 1 - EPS)
    return np.log(p / (1 - p))


# ---------------------------------------------------------------- data
def load():
    S = pd.read_parquet(ROOT / "explore" / "baseline_explore_scores.parquet",
                        columns=["site", "year", "row", "col", "y", "incomplete", "pooled_monthly", "blend_w", "local",
                                 "density_h2_tauinf"])
    S = S[S.year >= T_FIRST - 1].reset_index(drop=True)
    import os
    if os.environ.get("TMA_SITES"):
        S = S[S.site.isin(os.environ["TMA_SITES"].split(","))].reset_index(drop=True)
    P = pd.read_parquet(ROOT / "panel.parquet", columns=["site", "year", "row", "col", "burns_10y"])
    S = S.merge(P, on=["site", "year", "row", "col"], how="left")
    rk = S.groupby(["site", "year"]).pooled_monthly.rank(pct=True)
    S["f_rank"] = S.blend_w.where(S.blend_w.notna(), rk)
    S["f_fallback"] = S.blend_w.isna().astype(int)
    return S


def calibrate(S):
    """Platt map of f_rank per target year T, fitted on complete target years < T (all sites)."""
    from sklearn.linear_model import LogisticRegression
    pe = np.full(len(S), np.nan)
    for T in sorted(S.year.unique()):
        hist = S[(S.year < T) & (S.incomplete == 0) & S.f_rank.notna()]
        cur = ((S.year == T) & S.f_rank.notna()).to_numpy()
        if len(hist) < 1000 or hist.y.sum() < 50 or not cur.any():
            continue
        lr = LogisticRegression().fit(hist[["f_rank"]], hist.y)
        pe[cur] = lr.predict_proba(S.loc[cur, ["f_rank"]])[:, 1]
    S["logit_pe"] = logit(pe)
    return S


def site_km(site):
    with rasterio.open(grid_path(site)) as g:
        lat = g.transform.f + g.transform.e * g.height / 2
    ns = 0.0045814 * 111.32
    return ns, ns * np.cos(np.radians(lat))


def bases(site, rows, cols, extent):
    ns, ew = site_km(site)
    x, y = cols * ew, rows * ns
    H, W = extent
    out = []
    for s in SCALES:
        cx = np.arange(0, W * ew + s, s)
        cy = np.arange(0, H * ns + s, s)
        C = np.array([(a, b) for a in cx for b in cy])
        d2 = (x[:, None] - C[:, 0]) ** 2 + (y[:, None] - C[:, 1]) ** 2
        out.append(np.exp(-d2 / (2 * s * s)))
    sizes = [o.shape[1] for o in out]
    return np.hstack(out), sizes


# ---------------------------------------------------------------- per site-year residual fit
def fit_year(Phi, off, y, blocks, lam=LAMBDA, it=25):
    K = Phi.shape[1]
    a, alpha = np.zeros(K), logit(max(y.mean(), 1e-4)) - off.mean()
    X = np.hstack([np.ones((len(y), 1)), Phi])
    th = np.r_[alpha, a]
    pen = np.r_[0.0, np.full(K, lam)]
    for _ in range(it):
        eta = off + X @ th
        p = 1 / (1 + np.exp(-eta))
        g = X.T @ (y - p) - pen * th
        Hm = (X * (p * (1 - p))[:, None]).T @ X + np.diag(pen) + 1e-8 * np.eye(K + 1)
        step = np.linalg.solve(Hm, g)
        th = th + step
        if np.max(np.abs(step)) < 1e-6:
            break
    eta = off + X @ th
    p = 1 / (1 + np.exp(-eta))
    Hm = (X * (p * (1 - p))[:, None]).T @ X + np.diag(pen) + 1e-8 * np.eye(K + 1)
    Hi = np.linalg.inv(Hm)
    r = (y - p)[:, None] * X
    gb = pd.DataFrame(r).groupby(blocks).sum().to_numpy()
    meat = gb.T @ gb
    Vs = (Hi @ meat @ Hi)[1:, 1:]
    Hia = Hi[1:, 1:]
    # the block sandwich is rank-deficient when blocks < bases; block dependence enters as a scalar design effect
    deff = max(1.0, float(np.trace(Vs) / np.trace(Hia)))
    Hp = Hm[1:, 1:] - np.diag(pen[1:])                       # information of a without the ridge
    return th[1:], deff * Hia, Hp


def residual_fits(S):
    fits = {}
    for site, g in S[(S.incomplete == 0) & (S.year >= T_FIRST) & S.logit_pe.notna()].groupby("site"):
        allg = S[S.site == site]
        extent = (allg.row.max() + 1, allg.col.max() + 1)
        for t, gt in g.groupby("year"):
            Phi, sizes = bases(site, gt.row.to_numpy(), gt.col.to_numpy(), extent)
            blocks = (gt.row // 10).astype(str) + "_" + (gt.col // 10).astype(str)
            fits[(site, t)] = fit_year(Phi, gt.logit_pe.to_numpy(), gt.y.to_numpy().astype(float), blocks.to_numpy())
        fits[(site, "sizes")] = sizes
        fits[(site, "extent")] = extent
        print(site, "residual fits", flush=True)
    return fits


def variance_components(fits, sites, T):
    """Per scale k: sigma_U^2 = mean within-site variance of a_hat over years minus mean diag V; sigma_P^2 = variance
    of site means minus (sigma_U^2 + mean diag V) / n_years; floored at 1e-4. Each site uses its own basis sizes."""
    nsc = len(SCALES)
    within, vdiag, means, nyrs = [[] for _ in range(nsc)], [[] for _ in range(nsc)], [[] for _ in range(nsc)], [[] for _ in range(nsc)]
    for s in sites:
        yrs = [t for (ss, t) in fits if ss == s and isinstance(t, (int, np.integer)) and t <= T - 1]
        if len(yrs) < 2:
            continue
        sz = fits[(s, "sizes")]
        A = np.stack([fits[(s, t)][0] for t in yrs])
        Vd = np.stack([np.diag(fits[(s, t)][1]) for t in yrs])
        for k in range(nsc):
            lo, hi = sum(sz[:k]), sum(sz[:k + 1])
            within[k].append(A[:, lo:hi].var(axis=0, ddof=1).mean())
            vdiag[k].append(Vd[:, lo:hi].mean())
            means[k].append(A[:, lo:hi].mean(axis=0).var())
            nyrs[k].append(len(yrs))
    out = []
    for k in range(nsc):
        if not within[k]:
            out.append((1e-2, 1e-2))
            continue
        su = max(np.mean(within[k]) - np.mean(vdiag[k]), 1e-4)
        sp = max(np.mean(means[k]) - (su + np.mean(vdiag[k])) / np.mean(nyrs[k]), 1e-4)
        out.append((sp, su))
    return out


def blup(fits, site, T, comps, raw=False):
    sizes = fits[(site, "sizes")]
    yrs = [t for (ss, t) in fits if ss == site and isinstance(t, (int, np.integer)) and t <= T - 1]
    K = sum(sizes)
    if not yrs:
        return np.zeros(K)
    if raw:
        return np.mean([fits[(site, t)][0] for t in yrs], axis=0)
    cp = np.concatenate([np.full(n, comps[i][0]) for i, n in enumerate(sizes)])
    cu = np.concatenate([np.full(n, comps[i][1]) for i, n in enumerate(sizes)])
    A = np.diag(1 / cp)
    b = np.zeros(K)
    for t in yrs:
        a, V, _ = fits[(site, t)]
        Wt = np.linalg.inv(np.diag(cu) + V)
        A += Wt
        b += Wt @ a
    return np.linalg.solve(A, b)


# ---------------------------------------------------------------- comparators
def pooled_density_scores(S):
    P = BX.add_extra(E.load())
    P = P[P.year >= T_FIRST - 1].merge(S[["site", "year", "row", "col", "density_h2_tauinf"]], on=["site", "year", "row", "col"], how="left")
    groups = json.loads((HERE.parent / "scaleup" / "selection" / "site_groups.json").read_text())
    grp = {s: i for i, (_, ss) in enumerate(sorted(groups.items())) for s in ss}
    P["grp"] = P.site.map(grp)
    TS = E.training_sample(P)
    TS["grp"] = TS.site.map(grp)
    feats = E.FEATS + ["months_since_burn", "density_h2_tauinf"]
    sc = BX.pooled_scores(P, TS, feats)
    return P[["site", "year", "row", "col"]].assign(pooled_density=sc)


def coord_dist_scores(S):
    out = np.full(len(S), np.nan)
    for site, g in S.groupby("site"):
        ns, ew = site_km(site)
        xy = np.c_[g.col * ew, g.row * ns]
        for T in range(T_FIRST, 2026):
            tr = g[(g.year <= T - 1) & (g.incomplete == 0)]
            if tr.y.sum() < 100:
                continue
            te = (g.year == T).to_numpy()
            burned_before = g[(g.year <= T - 1) & (g.y == 1)]
            xb = np.c_[burned_before.col * ew, burned_before.row * ns]
            tree = cKDTree(xb)
            dist = tree.query(xy)[0]
            # distance for a training year u uses burns of years <= u - 1 only
            dtr = np.full(len(g), np.nan)
            for u in sorted(tr.year.unique()):
                bu = g[(g.year <= u - 1) & (g.y == 1)]
                if len(bu):
                    mu = (g.year == u).to_numpy()
                    dtr[mu] = cKDTree(np.c_[bu.col * ew, bu.row * ns]).query(xy[mu])[0]
            X = np.c_[xy, np.nan_to_num(dtr, nan=99.0)]
            trm = ((g.year <= T - 1) & (g.incomplete == 0)).to_numpy()
            neg = np.where(trm & (g.y == 0).to_numpy())[0]
            pos = np.where(trm & (g.y == 1).to_numpy())[0]
            rng = np.random.default_rng(42)
            neg = rng.choice(neg, min(20000, len(neg)), replace=False)
            idx = np.r_[pos, neg]
            m = RandomForestClassifier(200, min_samples_leaf=5, class_weight="balanced", random_state=42, n_jobs=30)
            m.fit(X[idx], g.y.to_numpy()[idx])
            Xte = np.c_[xy[te], dist[te]]
            out[g.index[te]] = m.predict_proba(Xte)[:, 1]
    return out


def standard_persistent(fits, site, T, lam):
    """Persistent spatial smooth with year intercepts, no transient term: the joint penalised logistic estimate of the
    persistent coefficients, approximated from the yearly fits by a_P = (sum_t H_t + lam I)^-1 sum_t H_t a_hat_t
    (model-based information H_t, not the block-robust covariance)."""
    yrs = [t for (ss, t) in fits if ss == site and isinstance(t, (int, np.integer)) and t <= T - 1]
    K = sum(fits[(site, "sizes")])
    if not yrs:
        return np.zeros(K)
    A = lam * np.eye(K)
    b = np.zeros(K)
    for t in yrs:
        a, _, Hp = fits[(site, t)]
        A += Hp
        b += Hp @ a
    return np.linalg.solve(A, b)


# ---------------------------------------------------------------- evaluation helpers
def wildfire_keep(g):
    """Rows of one site-year kept for target (ii): drop cells burned >= 3 times in the 10 earlier target years and
    burned cells of this year in patches of <= 4 cells."""
    keep = (g.burns_10y.fillna(0) < 3).to_numpy().copy()
    if g.y.sum():
        H, W = g.row.max() + 1, g.col.max() + 1
        m = np.zeros((H, W), bool)
        b = g[g.y == 1]
        m[b.row, b.col] = True
        lab, n = ndimage.label(m, structure=np.ones((3, 3)))
        size = np.bincount(lab.ravel())
        small = (g.y == 1).to_numpy() & (size[lab[g.row, g.col]] <= 4)
        keep &= ~small
    return keep


def transitions(S, cols):
    rows = []
    for (s, y), g in S[(S.incomplete == 0) & (S.year >= T_FIRST + 1)].groupby(["site", "year"]):
        kw = wildfire_keep(g)
        for tgt, mask in (("all", np.ones(len(g), bool)), ("wildfire", kw)):
            yy = g.y.to_numpy()[mask]
            if yy.sum() < 30 or (1 - yy).sum() < 30:
                continue
            r = {"site": s, "year": y, "target": tgt}
            for c in cols:
                v = g[c].to_numpy()[mask]
                r[c] = G.auc(yy, v) if np.isfinite(v).all() else np.nan
            rows.append(r)
    return pd.DataFrame(rows)


def later(S, cols):
    rows = []
    for s, g in S.groupby("site"):
        fy = int(regions.EXPERIMENTS[s]["label_start_date"][:4])
        T0 = fy + 1
        m = g[g.year == T0].set_index(["row", "col"])
        scar = g[(g.year == fy) & (g.y == 1)].set_index(["row", "col"]).index
        m = m[~m.index.isin(scar)]
        if not len(m):
            continue
        for hz, hi in (("all", 2026), ("two_year", T0 + 1)):
            fut = g[(g.year >= T0) & (g.year <= hi)]
            lab = fut.groupby(["row", "col"]).y.max().reindex(m.index).fillna(0)
            # wildfire target: drop cells frequent at T0 and cells whose later burns were all in small patches
            big = []
            for _, gu in fut.groupby("year"):
                kw = wildfire_keep(gu)
                big.append(gu[(gu.y == 1).to_numpy() & kw].set_index(["row", "col"]).index)
            bigidx = big[0].append(big[1:]) if big else pd.Index([])
            lab_w = pd.Series(m.index.isin(bigidx).astype(int), index=m.index)
            keep_w = (m.burns_10y.fillna(0) < 3) & ~((lab == 1) & (lab_w == 0))
            for tgt, L, K in (("all", lab, np.ones(len(m), bool)), ("wildfire", lab_w, keep_w.to_numpy())):
                yy = L.to_numpy()[K]
                r = {"site": s, "T0": T0, "horizon": hz, "target": tgt, "positives": int(yy.sum())}
                ok = yy.sum() >= 30 and (1 - yy).sum() >= 30
                for c in cols:
                    v = m[c].to_numpy()[K]
                    r[c] = G.auc(yy, v) if ok and np.isfinite(v).all() else np.nan
                rows.append(r)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- main
def main():
    OUT.mkdir(parents=True, exist_ok=True)
    S = calibrate(load())
    groups = json.loads((HERE.parent / "scaleup" / "selection" / "site_groups.json").read_text())
    grp = {s: i for i, (_, ss) in enumerate(sorted(groups.items())) for s in ss}
    S["grp"] = S.site.map(grp)
    fits = residual_fits(S)
    sites = sorted(S.site.unique())
    # TMA scores for every site-year T, every gamma, BLUP and raw
    comp_cache = {}
    LAMS = (0.3, 1.0, 3.0, 10.0, 30.0)
    for name in ("blup", "raw"):
        for gm in GAMMAS:
            S[f"tma_{name}_g{gm}"] = np.nan
    for lam in LAMS:
        S[f"std_l{lam}"] = np.nan
    for site, g in S.groupby("site"):
        extent = fits[(site, "extent")]
        for T in range(T_FIRST + 1, 2027):
            cur = g[(g.year == T)]
            if cur.empty or cur.logit_pe.isna().all():
                continue
            key = (grp[site], T)
            if key not in comp_cache:
                comp_cache[key] = variance_components(fits, [s for s in sites if grp[s] != grp[site]], T)
            Phi, _ = bases(site, cur.row.to_numpy(), cur.col.to_numpy(), extent)
            pb, pr = Phi @ blup(fits, site, T, comp_cache[key]), Phi @ blup(fits, site, T, None, raw=True)
            for gm in GAMMAS:
                S.loc[cur.index, f"tma_blup_g{gm}"] = cur.logit_pe.to_numpy() + gm * pb
                S.loc[cur.index, f"tma_raw_g{gm}"] = cur.logit_pe.to_numpy() + gm * pr
            for lam in LAMS:
                S.loc[cur.index, f"std_l{lam}"] = cur.logit_pe.to_numpy() + Phi @ standard_persistent(fits, site, T, lam)
        print(site, "TMA scores", flush=True)
    # gate: per (group, T) choose gamma by mean transition AUC of other groups' sites, years <= T - 1
    TRg = transitions(S, [f"tma_blup_g{gm}" for gm in GAMMAS] + [f"tma_raw_g{gm}" for gm in GAMMAS] + [f"std_l{l}" for l in LAMS])
    TRg = TRg[TRg.target == "all"]
    TRg["grp"] = TRg.site.map(grp)
    S["tma"] = np.nan
    S["tma_gate_raw"] = np.nan
    S["standard_spatial"] = np.nan
    gate_log = []
    for (gidx, T), cur in S.groupby(["grp", "year"]):
        h = TRg[(TRg.grp != gidx) & (TRg.year <= T - 1)]
        if h.empty:
            continue
        gb = max(GAMMAS, key=lambda gm: h[f"tma_blup_g{gm}"].mean())
        gr = max(GAMMAS, key=lambda gm: h[f"tma_raw_g{gm}"].mean())
        S.loc[cur.index, "tma"] = S.loc[cur.index, f"tma_blup_g{gb}"]
        S.loc[cur.index, "tma_gate_raw"] = S.loc[cur.index, f"tma_raw_g{gr}"]
        lb = max(LAMS, key=lambda l: h[f"std_l{l}"].mean())
        S.loc[cur.index, "standard_spatial"] = S.loc[cur.index, f"std_l{lb}"]
        gate_log.append({"grp": int(gidx), "T": int(T), "gamma_blup": gb, "gamma_raw": gr,
                         "estimated_auc_blup": float(h[f"tma_blup_g{gb}"].mean())})
    S["tma_ungated"] = S["tma_blup_g1.0"]
    S["tma_raw_mean"] = S["tma_raw_g1.0"]
    S["f_only"] = S.logit_pe
    S["density"] = S.density_h2_tauinf
    print("comparators", flush=True)
    PD = pooled_density_scores(S)
    S = S.merge(PD, on=["site", "year", "row", "col"], how="left")
    S["coord_dist_forest"] = coord_dist_scores(S)
    cols = ["tma", "tma_ungated", "tma_raw_mean", "tma_gate_raw", "f_only", "density", "pooled_density",
            "coord_dist_forest", "standard_spatial"]
    TR = transitions(S, cols)
    LT = later(S, cols)
    TR.to_csv(OUT / "tma_transitions.csv", index=False)
    LT.to_csv(OUT / "tma_later.csv", index=False)
    pd.DataFrame(gate_log).to_csv(OUT / "tma_gate_log.csv", index=False)
    S[["site", "year", "row", "col", "y", "incomplete", "f_fallback"] + cols].to_parquet(OUT / "tma_scores.parquet", index=False)
    summ = {}
    for name, D in (("transitions", TR), ("later", LT)):
        for keys, g in D.groupby(["target"] + (["horizon"] if name == "later" else [])):
            kk = name + "_" + "_".join(map(str, keys if isinstance(keys, tuple) else (keys,)))
            cc = g.dropna(subset=cols)
            summ[kk] = {"n_common": int(len(cc)), **{c: float(cc[c].mean()) for c in cols},
                        **{f"{c}_n": int(g[c].notna().sum()) for c in cols}}
    (OUT / "tma_dev_summary.json").write_text(json.dumps(summ, indent=1), encoding="utf-8")
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    main()
