"""R8l. Statistical checks requested by reviewer 2 that need no new data.

  1. Crossed random-effects model for the paired thermal gain in transfer: delta_st = mu + a_s + b_t + e,
     with source and target random intercepts (statsmodels MixedLM, variance components), on the
     study areas as drawn and on the 10 km collar.
  2. Residual spatial autocorrelation: correlogram (Moran-type correlation of out-of-fold residuals
     y - p between cell pairs) by distance class, from the within-region 5-fold blocked CV (10-cell
     blocks) of the thermal model; the range is the first distance class where the correlation
     falls below 0.05.
  3. Fold-averaged within-region AUC against the pooled out-of-fold AUC (10-cell blocks).
  4. Median precision-recall lift in transfer, from round7/r7a_pr_auc_10cell.csv.
  5. Pair-cluster intervals for the mean transfer AUC and mean gain of the four estimators of
     Section S1.8, from code/model_capacity.json.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import optimize, stats
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "paper" / "code"))
import ems_inference_common as E  # noqa: E402
import ems_inference_units as U  # noqa: E402

E.N_JOBS = 8
out = {}

# 1. crossed random effects
A = pd.read_csv(ROOT / "paper/labelfix_rerun/round5/collar/aoi_frame_transfer.csv")
out["crossed_random_effects"] = {}


def reml_crossed(y, src, tgt):
    """REML fit of y = mu + a_src + b_tgt + e with independent normal random intercepts."""
    y = np.asarray(y, float)
    n = len(y)
    X = np.ones((n, 1))
    Zs = (src[:, None] == np.unique(src)[None, :]).astype(float)
    Zt = (tgt[:, None] == np.unique(tgt)[None, :]).astype(float)
    Ks, Kt = Zs @ Zs.T, Zt @ Zt.T

    def nll(th):
        vs, vt, ve = np.exp(th)
        V = vs * Ks + vt * Kt + ve * np.eye(n)
        Vi = np.linalg.inv(V)
        XVX = X.T @ Vi @ X
        beta = np.linalg.solve(XVX, X.T @ Vi @ y)
        r = y - X @ beta
        return 0.5 * (np.linalg.slogdet(V)[1] + np.linalg.slogdet(XVX)[1] + r @ Vi @ r)

    best = min((optimize.minimize(nll, np.log([a, b, c]), method="Nelder-Mead",
                                  options={"xatol": 1e-8, "fatol": 1e-10, "maxiter": 20000})
                for a in (1e-5, 1e-3) for b in (1e-5, 1e-3) for c in (1e-4, 1e-3)), key=lambda r: r.fun)
    vs, vt, ve = np.exp(best.x)
    V = vs * Ks + vt * Kt + ve * np.eye(n)
    Vi = np.linalg.inv(V)
    se = float(np.sqrt(1 / (X.T @ Vi @ X)[0, 0]))
    mu = float((X.T @ Vi @ y)[0] / (X.T @ Vi @ X)[0, 0])
    q = stats.t.ppf(0.975, 4)          # conservative: df = number of regions - 1
    return {"mean": mu, "se": se, "ci95_t4": [mu - q * se, mu + q * se],
            "var_source": float(vs), "var_target": float(vt), "var_residual": float(ve)}


for tag in ("full", "10km"):
    s = A[(A.source_frame == tag) & (A.target_frame == tag)]
    src = s.direction.str.split("_to_").str[0].to_numpy()
    tgt = s.direction.str.split("_to_").str[1].to_numpy()
    out["crossed_random_effects"][tag] = reml_crossed(s.delta.to_numpy(), src, tgt)

# 2 and 3. correlogram of residuals and fold-averaged AUC
BINS = [0, 1, 2, 5, 10, 20, 40]
out["correlogram"], out["fold_vs_pooled"] = {}, {}
rng = np.random.default_rng(42)
for reg in E.REGIONS:
    d = E.load(reg)
    feats = E.THERMAL
    g = (d.row_500m // 10).astype(str) + "_" + (d.col_500m // 10).astype(str)
    oof = np.full(len(d), np.nan)
    fold_auc = []
    for tr_i, te_i in StratifiedGroupKFold(5, shuffle=True, random_state=E.SEED).split(d[feats], d.burned, groups=g):
        p = E.fit(feats, d.iloc[tr_i]).predict_proba(d.iloc[te_i][feats])[:, 1]
        oof[te_i] = p
        yt = d.burned.to_numpy()[te_i]
        if len(np.unique(yt)) == 2:
            fold_auc.append(roc_auc_score(yt, p))
    y = d.burned.to_numpy()
    out["fold_vs_pooled"][reg] = {"pooled": float(roc_auc_score(y, oof)), "fold_mean": float(np.mean(fold_auc)),
                                  "fold_min": float(np.min(fold_auc)), "fold_max": float(np.max(fold_auc)),
                                  "folds_with_both_classes": len(fold_auc)}
    res = y - oof
    res = (res - res.mean()) / res.std()
    xy = np.c_[d.row_500m.to_numpy() * 0.51, d.col_500m.to_numpy() * 0.40]
    n = len(d)
    i = rng.integers(0, n, 400_000)
    j = rng.integers(0, n, 400_000)
    dist = np.hypot(*(xy[i] - xy[j]).T)
    prod = res[i] * res[j]
    corr = []
    for lo, hi in zip(BINS[:-1], BINS[1:]):
        m = (dist > lo) & (dist <= hi)
        corr.append({"km": f"{lo}-{hi}", "pairs": int(m.sum()), "corr": float(prod[m].mean()) if m.any() else None})
    rng_km = next((c["km"] for c in corr if c["corr"] is not None and c["corr"] < 0.05), "> 40")
    out["correlogram"][reg] = {"bins": corr, "first_bin_below_0.05": rng_km}
    print(reg, out["fold_vs_pooled"][reg], rng_km, [round(c["corr"], 3) if c["corr"] is not None else None for c in corr], flush=True)

# 4. median PR lift
pr = pd.read_csv(ROOT / "paper/labelfix_rerun/round7/r7a_pr_auc_10cell.csv")
lift = pr.pr_auc / pr.prevalence
out["pr_lift"] = {"median": float(lift.median()), "mean": float(lift.mean()), "min": float(lift.min()), "max": float(lift.max())}

# 5. model capacity intervals
mc = pd.DataFrame(json.load(open(ROOT / "paper/labelfix_rerun/code/model_capacity.json"))["transfers"])
out["model_capacity"] = {}
for est in ("rf_canonical", "rf_shallow", "rf_leaf200", "logistic"):
    for q in ("thermal", "increment"):
        iv = U.intervals(mc[f"{est}_{q}"].to_numpy(), mc.source.to_numpy(), mc.target.to_numpy(), level=0.95, R=1000)
        out["model_capacity"][f"{est}_{q}"] = {"mean": float(iv["mean"]), "pair_cluster_ci95": list(iv["pair_cluster_boot"][:2])}

json.dump(out, open(HERE / "r8l_summary.json", "w"), indent=1, default=float)
print(json.dumps({k: v for k, v in out.items() if k not in ("correlogram",)}, indent=1, default=float))
