"""claim10_persistent.py: semi-synthetic experiment with a partly persistent spatial field (plan amendment 7).

Same landscapes, latent risk, label rule, models, folds and measures as claim9_synthetic.py, for the 24
scenarios with b > 0. The truth label is drawn with the same E and S2 = rho * S1 + sqrt(1 - rho^2) * S_new
(S_new independent, same L) and new noise, for rho in {0, 0.5, 0.8} (0 is the within-run reference). The training label, the folds and the fitted
models are the same for both rho (one fit per fire and scenario, two truth labels), so the measures are
identical across rho and only the truth changes.

The out-of-fold scores, the null scores and both labels of every run are saved (npz per fire) so that the
support settings of 7.3 can be varied without refitting.

Writes claim10_persistent_runs.csv, claim10_scores/<fire>.npz and claim10_persistent_summary.json.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "geonull"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import geonull as G  # noqa: E402
import analysis_official as A  # noqa: E402
import claim9_synthetic as C9  # noqa: E402

RHOS = (0.0, 0.5, 0.8)        # 0.0: within-run reference with the same fits (plan 7.1)
SCEN = [(i, s) for i, s in enumerate(C9.SCEN) if s[1] > 0]           # 24, scenario index as in claim9
OUTCSV = A.OUT / "claim10_persistent_runs.csv"
NPZ = A.OUT / "claim10_scores"


def run_fire(fi, fid, f, done):
    E = C9.zs(sum(s * C9.zs(f.df[c]) for c, s in C9.SIGNAL))
    prev = f.nb / f.n
    out, store = [], {}
    for si, (a, b, L) in SCEN:
        if (fid, si) in done:
            continue
        rng = np.random.default_rng(10_000_000 + 1000 * fi + si)
        S1 = C9.grf(f, L, rng)
        y1 = C9.labels(a * E + b * S1 + rng.standard_normal(f.n), prev)
        Snew = C9.grf(f, L, rng)
        noise2 = rng.standard_normal(f.n)
        y2 = {rho: C9.labels(a * E + b * (rho * S1 + np.sqrt(1 - rho ** 2) * Snew) + noise2, prev) for rho in RHOS}
        X_env = np.c_[np.c_[[C9.zs(f.df[c]) for c, _ in C9.SIGNAL]].T, rng.standard_normal((f.n, 2))]
        folds = list(StratifiedGroupKFold(5, shuffle=True, random_state=A.SEED).split(X_env, y1, groups=f.blocks(10)))
        sc = {}
        for name, X in (("env", X_env), ("geo", f.xy)):
            o = np.full(f.n, np.nan)
            for tr, te in folds:
                o[te] = C9.rf().fit(X[tr], y1[tr]).predict_proba(X[te])[:, 1]
            sc[name] = o
        null = G.null_scores(f.xy, y1, folds)
        pairs = G.matched_pairs(f.xy, y1, folds)
        z = -null
        sn = G.standardised_auc(y1, null, z)["sauc"]
        meas = {}
        for name, o in sc.items():
            s = G.standardised_auc(y1, o, z)
            meas.update({f"auc_{name}": G.auc(y1, o), f"cauc_{name}": G.calibrated_auc(y1, o, null, pairs)["cauc"],
                         f"saucc_{name}": s["sauc"] + 0.5 - max(0.5, sn) if np.isfinite(sn) else np.nan})
        for rho in RHOS:
            r = {"fire": fid, "scenario": si, "a": a, "b": b, "L": L, "rho": rho, **meas,
                 "truth_env": G.auc(y2[rho], sc["env"]), "truth_geo": G.auc(y2[rho], sc["geo"])}
            out.append(r)
        store[f"s{si}"] = np.c_[sc["env"], sc["geo"], null, y1, y2[0.0], y2[0.5], y2[0.8]]
        print(fid, si, (a, b, L), {k: round(v, 3) for k, v in out[-1].items() if k.startswith(("truth_", "saucc_"))}, flush=True)
    if store:
        NPZ.mkdir(exist_ok=True)
        old = dict(np.load(NPZ / f"{fid}.npz")) if (NPZ / f"{fid}.npz").exists() else {}
        np.savez_compressed(NPZ / f"{fid}.npz", folds_note=np.array("columns: env, geo, null, y1, y2_rho0, y2_rho0.5, y2_rho0.8"),
                            **old, **store)
    return out


def main():
    F = A.load_fires()
    ids = [i for i in F if i != "montiferru_2021"]
    prev = pd.read_csv(OUTCSV) if OUTCSV.exists() else pd.DataFrame()
    done = set(zip(prev.fire, prev.scenario)) if len(prev) else set()
    for fi, fid in enumerate(ids):
        rows = run_fire(fi, fid, F[fid], done)
        if rows:
            prev = pd.concat([prev, pd.DataFrame(rows)], ignore_index=True)
            prev.to_csv(OUTCSV, index=False)
    if len(prev) == len(ids) * len(SCEN) * len(RHOS):
        S = {}
        for rho in RHOS:
            S[f"rho_{rho}"] = C9.summarise(prev[prev.rho == rho].drop(columns="rho"))
            S[f"rho_{rho}"]["without_first_fire"] = {k: v for k, v in C9.summarise(
                prev[(prev.rho == rho) & (prev.fire != ids[0])].drop(columns="rho")).items() if k != "per_scenario"}
        (A.OUT / "claim10_persistent_summary.json").write_text(json.dumps(S, indent=1, default=float), encoding="utf-8")
        print(json.dumps({k: v["decision"] for k, v in S.items()}, indent=1))


if __name__ == "__main__":
    main()
