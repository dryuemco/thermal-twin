"""claim9_synthetic.py: semi-synthetic experiment with known truth (plan amendment 6.2, strata of 6.3).

On the population cells of each of the 31 primary fires, a latent risk eta = a*E + b*S + N(0, 1) is drawn, with
E the standardised mean of NDVI (+), elevation (-), slope (+) and pre-fire LST (+), each standardised within the
fire, and S a unit-variance Gaussian random field with exponential correlation of length L km (spectral method on
the fire's raster, padded twice). Burned = the cells above the quantile that gives the fire's real burned share.

Two random forests (300 trees, min_samples_leaf 3, balanced) are fitted under the study's 5 km block design:
M_env on the four signal predictors plus two standard-normal noise predictors, M_geo on the cell coordinates.
Truth: the higher AUC of the same out-of-fold scores against a second label drawn with the same E and a new S
and new noise (what carries over to a new geometry of burning). Each measure (pooled AUC, calibrated AUC,
corrected sAUC with the burned cells' distance distribution) picks the model it scores higher; ties and
unsupported values count as wrong. Decision rule: plan 6.2.

Writes claim9_synthetic_runs.csv (one row per fire and scenario, resumable) and claim9_synthetic_summary.json.
Run:  python claim9_synthetic.py [fire ...]
"""
import itertools
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "geonull"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import geonull as G  # noqa: E402
import analysis_official as A  # noqa: E402

A_GRID, B_GRID, L_GRID = (0, 0.5, 1, 2), (0, 1, 2, 4), (2, 10)
SCEN = list(itertools.product(A_GRID, B_GRID, L_GRID))          # 32, index = position in this list
SIGNAL = [("ndvi_mean", 1), ("elevation_mean", -1), ("slope_mean", 1), ("current_lst_mean", 1)]
OUTCSV = A.OUT / "claim9_synthetic_runs.csv"


def zs(v):
    v = np.asarray(v, float)
    v = np.where(np.isfinite(v), v, np.nanmedian(v))
    return (v - v.mean()) / (v.std() or 1.0)


def grf(f, L, rng):
    """Unit-variance field with exponential covariance exp(-r/L) on the fire's raster, sampled at its cells."""
    km_ns = A.CELL_DEG * A.M_PER_DEG / 1000.0
    km_ew = km_ns * np.cos(np.radians(f.meta["lat"]))
    H, W = 2 * (f.rr.max() + 1), 2 * (f.cc.max() + 1)
    kx = np.fft.fftfreq(H, d=km_ns)
    ky = np.fft.fftfreq(W, d=km_ew)
    k2 = (kx[:, None] ** 2 + ky[None, :] ** 2) * (2 * np.pi) ** 2
    spec = 2 * np.pi * L ** 2 / (1 + k2 * L ** 2) ** 1.5           # 2D spectral density of exp(-r/L)
    noise = np.fft.fft2(rng.standard_normal((H, W)))
    field = np.real(np.fft.ifft2(noise * np.sqrt(spec)))
    v = field[f.rr, f.cc]
    return (v - v.mean()) / v.std()


def labels(eta, prev):
    return (eta > np.quantile(eta, 1 - prev)).astype(int)


def rf():
    return RandomForestClassifier(n_estimators=300, min_samples_leaf=3, class_weight="balanced",
                                  random_state=A.SEED, n_jobs=A.N_JOBS)


def run_fire(fi, fid, f, done):
    E = zs(sum(s * zs(f.df[c]) for c, s in SIGNAL))
    prev = f.nb / f.n
    out = []
    for si, (a, b, L) in enumerate(SCEN):
        if (fid, si) in done:
            continue
        rng = np.random.default_rng(1000 * fi + si)
        y1 = labels(a * E + b * grf(f, L, rng) + rng.standard_normal(f.n), prev)
        y2 = labels(a * E + b * grf(f, L, rng) + rng.standard_normal(f.n), prev)
        X_env = np.c_[[zs(f.df[c]) for c, _ in SIGNAL]].T
        X_env = np.c_[X_env, rng.standard_normal((f.n, 2))]
        X_geo = f.xy
        groups = f.blocks(10)
        from sklearn.model_selection import StratifiedGroupKFold
        folds = list(StratifiedGroupKFold(5, shuffle=True, random_state=A.SEED).split(X_env, y1, groups=groups))
        sc = {}
        for name, X in (("env", X_env), ("geo", X_geo)):
            o = np.full(f.n, np.nan)
            for tr, te in folds:
                o[te] = rf().fit(X[tr], y1[tr]).predict_proba(X[te])[:, 1]
            sc[name] = o
        null = G.null_scores(f.xy, y1, folds)
        pairs = G.matched_pairs(f.xy, y1, folds)
        z = -null
        sn = G.standardised_auc(y1, null, z)["sauc"]
        r = {"fire": fid, "scenario": si, "a": a, "b": b, "L": L, "burned": int(y1.sum())}
        for name, o in sc.items():
            r[f"truth_{name}"] = G.auc(y2, o)
            r[f"auc_{name}"] = G.auc(y1, o)
            r[f"cauc_{name}"] = G.calibrated_auc(y1, o, null, pairs)["cauc"]
            s = G.standardised_auc(y1, o, z)
            r[f"saucc_{name}"] = s["sauc"] + 0.5 - max(0.5, sn) if np.isfinite(sn) else np.nan
            r["sauc_coverage"] = s["coverage"]
        r["auc_null"], r["truth_null"] = G.auc(y1, null), G.auc(y2, null)
        out.append(r)
        print(fid, si, (a, b, L), {k: round(v, 3) for k, v in r.items() if k.startswith(("truth_", "auc_", "saucc_"))},
              flush=True)
    return out


def pick(r, m):
    e, g = r[f"{m}_env"], r[f"{m}_geo"]
    if not (np.isfinite(e) and np.isfinite(g)) or e == g:
        return None
    return "env" if e > g else "geo"


def summarise(R):
    R = R.copy()
    R["truth"] = np.where(R.truth_env > R.truth_geo, "env", np.where(R.truth_env < R.truth_geo, "geo", "tie"))
    for m in ("auc", "cauc", "saucc"):
        R[f"ok_{m}"] = [pick(r, m) == r["truth"] for r in R.to_dict("records")]
    per = R.groupby(["a", "b", "L"])[["ok_auc", "ok_cauc", "ok_saucc"]].mean().reset_index()
    per["truth_env_share"] = R.groupby(["a", "b", "L"]).truth.apply(lambda t: (t == "env").mean()).to_numpy()
    cl = per[per.b > 0]
    S = {"fires": int(R.fire.nunique()), "runs": int(len(R)),
         "agreement_b_positive": {m: float(cl[f"ok_{m}"].mean()) for m in ("auc", "cauc", "saucc")},
         "agreement_all": {m: float(per[f"ok_{m}"].mean()) for m in ("auc", "cauc", "saucc")},
         # reporting only (plan 6.6): scenarios without environmental signal (a = 0) have no meaningful truth
         "agreement_b_positive_a_zero": {m: float(cl[cl.a == 0][f"ok_{m}"].mean()) for m in ("auc", "cauc", "saucc")},
         "agreement_b_positive_a_positive": {m: float(cl[cl.a > 0][f"ok_{m}"].mean()) for m in ("auc", "cauc", "saucc")},
         "per_scenario": per.to_dict("records")}
    d_auc = S["agreement_b_positive"]["saucc"] - S["agreement_b_positive"]["auc"]
    d_cauc = S["agreement_b_positive"]["saucc"] - S["agreement_b_positive"]["cauc"]
    S["decision"] = {"saucc_minus_auc_pp": 100 * d_auc, "saucc_minus_cauc_pp": 100 * d_cauc,
                     "advantage_claimed": bool(d_auc >= 0.10 and d_cauc >= -0.02)}
    return S


def main():
    F = A.load_fires()
    ids = [i for i in F if i != "montiferru_2021"]
    only = sys.argv[1:] or ids
    prev = pd.read_csv(OUTCSV) if OUTCSV.exists() else pd.DataFrame()
    done = set(zip(prev.fire, prev.scenario)) if len(prev) else set()
    for fi, fid in enumerate(ids):
        if fid not in only:
            continue
        rows = run_fire(fi, fid, F[fid], done)
        if rows:
            prev = pd.concat([prev, pd.DataFrame(rows)], ignore_index=True)
            prev.to_csv(OUTCSV, index=False)
    if prev.fire.nunique() == len(ids) and len(prev) == len(ids) * len(SCEN):
        S = summarise(prev)
        (A.OUT / "claim9_synthetic_summary.json").write_text(json.dumps(S, indent=1, default=float), encoding="utf-8")
        print(json.dumps({k: S[k] for k in ("agreement_b_positive", "agreement_all", "decision")}, indent=1))


if __name__ == "__main__":
    main()
