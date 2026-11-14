"""claim9_intervals.py: fire-level paired intervals and support sensitivity for the semi-synthetic runs and the
31 fires (plan amendment 7.2 and 7.3; reporting only, no decision rule).

7.2  For each fire, the agreement of each measure with the truth averaged over the 24 scenarios with b > 0;
     paired differences (sAUC_c - AUC, sAUC_c - cAUC) with a 95% interval from 2000 bootstrap resamples of fires
     (seed 42). Done for claim9 and, per rho, for claim10.
7.3  Support sensitivity: coverage 0.70 / 0.80 / 0.90, minimum 10 / 20 / 40 burned and unburned cells per
     stratum, stratum ratio 1.20 / 1.33 / 1.50, varied one at a time from the declared setting (0.80, 20, 1.33).
     On the 31 fires (5 km blocks, cached predictions): number of fires supported, mean sAUC_c of the thermal RF.
     On the claim10 runs (saved scores): agreement of sAUC_c with the truth for b > 0.
     Ranking agreement on the 31 fires: share of fires in which cAUC and sAUC_c rank the thermal and the baseline
     RF the same way, and the same for the pooled AUC.

Writes claim9_intervals.json.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "geonull"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import geonull as G  # noqa: E402
import analysis_official as A  # noqa: E402
import claim9_synthetic as C9  # noqa: E402

SETTINGS = {"declared": (0.80, 20, 1.33), "cov0.70": (0.70, 20, 1.33), "cov0.90": (0.90, 20, 1.33),
            "min10": (0.80, 10, 1.33), "min40": (0.80, 40, 1.33), "ratio1.20": (0.80, 20, 1.20), "ratio1.50": (0.80, 20, 1.50)}


def per_fire_agreement(R):
    R = R[R.b > 0].copy()
    R["truth"] = np.where(R.truth_env > R.truth_geo, "env", np.where(R.truth_env < R.truth_geo, "geo", "tie"))
    for m in ("auc", "cauc", "saucc"):
        R[f"ok_{m}"] = [C9.pick(r, m) == r["truth"] for r in R.to_dict("records")]
    g = R.groupby("fire")[["ok_auc", "ok_cauc", "ok_saucc"]].mean()
    return {"saucc_minus_auc": A.boot_mean(g.ok_saucc - g.ok_auc), "saucc_minus_cauc": A.boot_mean(g.ok_saucc - g.ok_cauc),
            "fires": int(len(g))}


def saucc(y, s, null, z, cov, mn, ratio):
    st = G.geometric_strata(ratio=ratio)
    a = G.standardised_auc(y, s, z, strata=st, min_pos=mn, min_neg=mn, min_coverage=cov)["sauc"]
    b = G.standardised_auc(y, null, z, strata=st, min_pos=mn, min_neg=mn, min_coverage=cov)["sauc"]
    return a + 0.5 - max(0.5, b) if np.isfinite(b) else np.nan


def main():
    out = {}
    p9 = A.OUT / "claim9_synthetic_runs.csv"
    if p9.exists():
        out["claim9"] = per_fire_agreement(pd.read_csv(p9))
    p10 = A.OUT / "claim10_persistent_runs.csv"
    if p10.exists():
        R10 = pd.read_csv(p10)
        out["claim10"] = {f"rho_{r}": per_fire_agreement(R10[R10.rho == r]) for r in sorted(R10.rho.unique())}
    # 7.3 on the 31 fires
    F = A.load_fires()
    ids = [i for i in F if i != "montiferru_2021"]
    real = {k: [] for k in SETTINGS}
    rank = {"cauc_vs_saucc_same": 0, "auc_vs_saucc_same": 0, "fires": 0}
    P = pd.read_csv(A.OUT / "claims12_per_fire.csv").set_index("fire")
    for fid in ids:
        f = F[fid]
        z = f.train_pos_dist(10)
        null = f.null_oof(10)
        st = f.oof(A.THERMAL, "thermal", "rf", 10)
        sb = f.oof(A.BASELINE, "baseline", "rf", 10)
        for k, (cov, mn, ratio) in SETTINGS.items():
            real[k].append(saucc(f.y, st, null, z, cov, mn, ratio))
        dt, db = saucc(f.y, st, null, z, *SETTINGS["declared"]), saucc(f.y, sb, null, z, *SETTINGS["declared"])
        if np.isfinite(dt) and np.isfinite(db):
            rank["fires"] += 1
            rank["cauc_vs_saucc_same"] += int(np.sign(P.loc[fid, "cauc_rf_thermal_b10"] - P.loc[fid, "cauc_rf_baseline_b10"]) == np.sign(dt - db))
            rank["auc_vs_saucc_same"] += int(np.sign(P.loc[fid, "auc_rf_thermal_b10"] - P.loc[fid, "auc_rf_baseline_b10"]) == np.sign(dt - db))
    out["support_real"] = {k: {"fires_supported": int(np.isfinite(v).sum()), "saucc_rf_thermal": A.boot_mean(v)} for k, v in real.items()}
    out["ranking_real_thermal_vs_baseline"] = rank
    # 7.3 on the claim10 saved scores
    npz = A.OUT / "claim10_scores"
    if npz.exists() and p10.exists():
        R10 = pd.read_csv(p10)
        syn = {}
        for k, (cov, mn, ratio) in SETTINGS.items():
            ok = {0.5: [], 0.8: []}
            for fi, fid in enumerate(ids):
                if not (npz / f"{fid}.npz").exists():
                    continue
                D = np.load(npz / f"{fid}.npz")
                f = F[fid]
                for key in [x for x in D.files if x.startswith("s")]:
                    env, geo, null, y1, y05, y08 = D[key].T
                    z = -null
                    e, g = saucc(y1, env, null, z, cov, mn, ratio), saucc(y1, geo, null, z, cov, mn, ratio)
                    pick = None if not (np.isfinite(e) and np.isfinite(g)) or e == g else ("env" if e > g else "geo")
                    for rho, y2 in ((0.5, y05), (0.8, y08)):
                        te, tg = G.auc(y2, env), G.auc(y2, geo)
                        truth = "env" if te > tg else ("geo" if te < tg else "tie")
                        ok[rho].append(pick == truth)
            syn[k] = {f"rho_{r}": float(np.mean(v)) if v else None for r, v in ok.items()}
        out["support_synthetic_claim10"] = syn
    (A.OUT / "claim9_intervals.json").write_text(json.dumps(out, indent=1, default=float), encoding="utf-8")
    print(json.dumps(out, indent=1, default=float)[:3000])


if __name__ == "__main__":
    main()
