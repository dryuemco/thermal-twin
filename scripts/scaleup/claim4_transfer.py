"""claim4_transfer.py: claim 4 of docs/scaleup/ANALYSIS_PLAN.md, fire-to-fire transfer and pooling.

Primary set (31 fires). For every ordered pair (930 directions): THERMAL RF trained on the whole source
fire and scored on the target with raw predictors, within-fire z-scores, within-fire min-max scaling
(Dimarco et al. 2026) and the BASELINE set; the raw score is also given on the target's nearest
(0-0.5 km) and farthest (>10 km, or farthest band with >= 20 unburned cells) distance bands.
Similarity measures (distance, same year, domain-classifier AUC, mean shift) with Spearman's rho and a
fire-resampling interval. Leave-one-fire-out pooling (4000 cells per source, seed 42) and the learning
curve over 2, 5, 10, 15, 20, 30 source fires, three draws each. Source and target means stand in for
the mixed model (statsmodels is not installed in the analysis environment).

Run:  python claim4_transfer.py   (writes $THERMAL_TWIN_SCALEUP/analysis/claim4_*)
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_predict

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analysis_official as A  # noqa: E402

POOL_CAP, CURVE_K, CURVE_REPS = 4000, (2, 5, 10, 15, 20, 30), 3


def scale(df, how):
    z = df.copy()
    x = df[A.NUM]
    if how == "z":
        z[A.NUM] = (x - x.mean()) / x.std(ddof=0).replace(0, 1)
    elif how == "minmax":
        z[A.NUM] = (x - x.min()) / (x.max() - x.min()).replace(0, 1)
    return z


def haversine(a, b):
    p1, p2 = math.radians(a["lat"]), math.radians(b["lat"])
    h = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(b["lon"] - a["lon"]) / 2) ** 2
    return 2 * 6371.0 * math.asin(math.sqrt(h))


def node_boot_rho(D, x, y, ids, B=2000):
    rng = np.random.default_rng(A.SEED)
    pos = {f: i for i, f in enumerate(ids)}
    s_i, t_i = D.source.map(pos).to_numpy(), D.target.map(pos).to_numpy()
    xv, yv = D[x].to_numpy(float), D[y].to_numpy(float)
    ok = np.isfinite(xv) & np.isfinite(yv)
    out = []
    for _ in range(B):
        c = np.bincount(rng.integers(0, len(ids), len(ids)), minlength=len(ids))
        w = (c[s_i] * c[t_i]) * ok
        if (w > 0).sum() < 6:
            continue
        idx = np.repeat(np.arange(len(D)), w)
        out.append(stats.spearmanr(xv[idx], yv[idx]).statistic)
    return {"rho": float(stats.spearmanr(xv[ok], yv[ok]).statistic),
            "lo": float(np.nanpercentile(out, 2.5)), "hi": float(np.nanpercentile(out, 97.5))}


def band_masks(f):
    near = (f.y == 1) | ((f.y == 0) & (f.dist < 0.5))
    far = None
    for lo, hi in reversed(A.BANDS):
        neg = (f.y == 0) & (f.dist >= lo) & (f.dist < hi)
        if neg.sum() >= A.MIN_BAND_NEG:
            far = (f.y == 1) | neg
            break
    return near, far


def main():
    F = A.load_fires()
    ids = [i for i in F if i != "montiferru_2021"]
    S = {k: {i: scale(F[i].df, k) for i in ids} for k in ("z", "minmax")}
    masks = {i: band_masks(F[i]) for i in ids}
    rows = []
    for s in ids:
        src = F[s].df
        m_raw = A.build(A.THERMAL).fit(src[A.THERMAL], src.burned)
        m_base = A.build(A.BASELINE).fit(src[A.BASELINE], src.burned)
        m_z = A.build(A.THERMAL).fit(S["z"][s][A.THERMAL], src.burned)
        m_mm = A.build(A.THERMAL).fit(S["minmax"][s][A.THERMAL], src.burned)
        for t in ids:
            if s == t:
                continue
            y = F[t].y
            p = m_raw.predict_proba(F[t].df[A.THERMAL])[:, 1]
            near, far = masks[t]
            rows.append({"source": s, "target": t, "raw": A.auc(y, p),
                         "raw_near": A.auc(y[near], p[near]), "raw_far": A.auc(y[far], p[far]) if far is not None else np.nan,
                         "baseline": A.auc(y, m_base.predict_proba(F[t].df[A.BASELINE])[:, 1]),
                         "zscore": A.auc(y, m_z.predict_proba(S["z"][t][A.THERMAL])[:, 1]),
                         "minmax": A.auc(y, m_mm.predict_proba(S["minmax"][t][A.THERMAL])[:, 1])})
        print("  source", s, "done", flush=True)
    T = pd.DataFrame(rows)

    # similarity measures (label-free)
    sub = {i: F[i].df[A.NUM].sample(min(1500, F[i].n), random_state=A.SEED) for i in ids}
    dom = {}
    for a_i, a in enumerate(ids):
        for b in ids[a_i + 1:]:
            X = pd.concat([sub[a], sub[b]])
            X = X.fillna(X.median())
            lab = np.r_[np.zeros(len(sub[a])), np.ones(len(sub[b]))]
            pr = cross_val_predict(RandomForestClassifier(100, min_samples_leaf=5, random_state=A.SEED, n_jobs=A.N_JOBS), X, lab,
                                   cv=StratifiedKFold(3, shuffle=True, random_state=A.SEED), method="predict_proba")[:, 1]
            dom[(a, b)] = dom[(b, a)] = float(A.roc_auc_score(lab, pr))
    mu = {i: F[i].df[A.NUM].mean() for i in ids}
    sd = {i: F[i].df[A.NUM].std(ddof=0) for i in ids}
    T["distance_km"] = [haversine(F[s].meta, F[t].meta) for s, t in zip(T.source, T.target)]
    T["same_year"] = [int(F[s].meta["year"] == F[t].meta["year"]) for s, t in zip(T.source, T.target)]
    T["domain_auc"] = [dom[(s, t)] for s, t in zip(T.source, T.target)]
    T["mean_shift"] = [float(((mu[s] - mu[t]).abs() / np.sqrt((sd[s] ** 2 + sd[t] ** 2) / 2)).mean()) for s, t in zip(T.source, T.target)]
    T.to_csv(A.OUT / "claim4_transfer.csv", index=False)

    def pooled(target, sources, how):
        parts = []
        for s in sources:
            d = S[how][s] if how else F[s].df
            parts.append(d.sample(min(POOL_CAP, len(d)), random_state=A.SEED))
        tr = pd.concat(parts, ignore_index=True)
        m = A.build(A.THERMAL).fit(tr[A.THERMAL], tr.burned)
        d = S[how][target] if how else F[target].df
        return m.predict_proba(d[A.THERMAL])[:, 1]

    prow = []
    for t in ids:
        src = [i for i in ids if i != t]
        y = F[t].y
        near, far = masks[t]
        r = {"target": t, "single_mean": float(T[T.target == t].raw.mean()), "single_best": float(T[T.target == t].raw.max())}
        for tag, how in (("pooled_raw", None), ("pooled_z", "z"), ("pooled_minmax", "minmax")):
            p = pooled(t, src, how)
            r[tag] = A.auc(y, p)
            r[tag + "_near"] = A.auc(y[near], p[near])
            r[tag + "_far"] = A.auc(y[far], p[far]) if far is not None else np.nan
        prow.append(r)
        print(f"  pooled into {t}: raw {r['pooled_raw']:.3f} z {r['pooled_z']:.3f} minmax {r['pooled_minmax']:.3f}", flush=True)
    P = pd.DataFrame(prow)
    P.to_csv(A.OUT / "claim4_pooled_lofo.csv", index=False)

    crow = []
    for k in CURVE_K:
        k_eff = min(k, len(ids) - 1)
        for rep in range(CURVE_REPS if k_eff < len(ids) - 1 else 1):
            for t in ids:
                pool = [i for i in ids if i != t]
                src = list(np.random.default_rng(1000 * k + 10 * rep + ids.index(t)).choice(pool, k_eff, replace=False))
                crow.append({"k": k_eff, "rep": rep, "target": t, "pooled_z": A.auc(F[t].y, pooled(t, src, "z"))})
        print("  curve k =", k_eff, "done", flush=True)
    Cv = pd.DataFrame(crow)
    Cv.to_csv(A.OUT / "claim4_curve.csv", index=False)

    Sm = {"directions": int(len(T)),
          **{m: A.boot_mean(T[m]) for m in ("raw", "raw_near", "raw_far", "baseline", "zscore", "minmax")},
          "share_raw_above_0.6": float((T.raw > 0.6).mean()), "share_raw_below_0.5": float((T.raw < 0.5).mean()),
          "thermal_minus_baseline": A.boot_mean(T.raw - T.baseline),
          "source_mean_raw_sd": float(T.groupby("source").raw.mean().std()), "target_mean_raw_sd": float(T.groupby("target").raw.mean().std()),
          "similarity_spearman": {m: node_boot_rho(T, m, "raw", ids) for m in ("distance_km", "same_year", "domain_auc", "mean_shift")},
          "near_pairs_under_150_km": {"directions": int((T.distance_km < 150).sum()), "raw": A.boot_mean(T[T.distance_km < 150].raw)},
          "pooled": {c: A.boot_mean(P[c]) for c in P.columns if c != "target"},
          "pooled_z_targets_above_0.6": int((P.pooled_z > 0.6).sum()),
          "curve": {int(k): A.boot_mean(g.groupby("target").pooled_z.mean()) for k, g in Cv.groupby("k")}}
    (A.OUT / "claim4_summary.json").write_text(json.dumps(Sm, indent=1, default=float), encoding="utf-8")
    print(json.dumps({k: Sm[k] for k in ("raw", "raw_near", "raw_far", "zscore", "minmax")}, indent=1, default=float))


if __name__ == "__main__":
    main()
