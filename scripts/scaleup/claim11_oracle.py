"""claim11_oracle.py: oracle truth on the fixed claim10 scores (plan 8.2). No model is refitted.

For each fire and claim10 scenario, E and S1 are regenerated from the claim10 seeds (S1 is the first draw of the
claim10 generator, so it is reproduced exactly; checked against the saved training label y1). For each rho in
RHOS, K = 50 second labels eta2 = a*E + b*(rho*S1 + sqrt(1 - rho^2)*S_new) + noise (same burned share) are drawn
with seed 20,000,000 + 1000 * fire index + scenario index, in the order rho, k. Per run and rho: expected truth
AUC of M_env and M_geo, the oracle truth (higher expected AUC), rank stability (share of draws won by M_env), and
for each measure (choice taken from claim10_persistent_runs.csv) the expected AUC loss of its choice.

Writes claim11_oracle_runs.csv and claim11_oracle_summary.json.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analysis_official as A  # noqa: E402
import claim9_synthetic as C9  # noqa: E402
import claim10_persistent as C10  # noqa: E402

RHOS = (-0.5, -0.25, 0.0, 0.25, 0.5, 0.7, 0.8, 0.9)
K = 50
MEAS = ("auc", "cauc", "saucc")


def fast_auc(rank, y):
    n1 = y.sum()
    n0 = len(y) - n1
    return (rank[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)


def main():
    F = A.load_fires()
    ids = [i for i in F if i != "montiferru_2021"]
    M = pd.read_csv(A.OUT / "claim10_persistent_runs.csv")
    M = M[M.rho == 0.0].set_index(["fire", "scenario"])
    rows = []
    for fi, fid in enumerate(ids):
        f = F[fid]
        D = np.load(A.OUT / "claim10_scores" / f"{fid}.npz")
        E = C9.zs(sum(s * C9.zs(f.df[c]) for c, s in C9.SIGNAL))
        prev = f.nb / f.n
        for si, (a, b, L) in C10.SCEN:
            env, geo, null, y1 = D[f"s{si}"][:, :4].T
            rng = np.random.default_rng(10_000_000 + 1000 * fi + si)
            S1 = C9.grf(f, L, rng)
            check = C9.labels(a * E + b * S1 + rng.standard_normal(f.n), prev)
            assert (check == y1).all(), (fid, si)
            r_env, r_geo = rankdata(env), rankdata(geo)
            rng2 = np.random.default_rng(20_000_000 + 1000 * fi + si)
            m = M.loc[(fid, si)]
            for rho in RHOS:
                ae, ag = np.empty(K), np.empty(K)
                for k in range(K):
                    S2 = rho * S1 + np.sqrt(1 - rho ** 2) * C9.grf(f, L, rng2)
                    y2 = C9.labels(a * E + b * S2 + rng2.standard_normal(f.n), prev)
                    ae[k], ag[k] = fast_auc(r_env, y2), fast_auc(r_geo, y2)
                exp_e, exp_g = ae.mean(), ag.mean()
                r = {"fire": fid, "scenario": si, "a": a, "b": b, "L": L, "rho": rho, "exp_auc_env": exp_e,
                     "exp_auc_geo": exp_g, "oracle": "env" if exp_e > exp_g else "geo",
                     "stability_env_wins": float((ae > ag).mean())}
                best = max(exp_e, exp_g)
                for meas in MEAS:
                    e, g = m[f"{meas}_env"], m[f"{meas}_geo"]
                    c = None if not (np.isfinite(e) and np.isfinite(g)) or e == g else ("env" if e > g else "geo")
                    r[f"choice_{meas}"] = c or "none"
                    r[f"loss_{meas}"] = best - (exp_e if c == "env" else exp_g if c == "geo" else min(exp_e, exp_g))
                r["loss_always_env"], r["loss_always_geo"] = best - exp_e, best - exp_g
                rows.append(r)
        print(fid, "done", flush=True)
    R = pd.DataFrame(rows)
    R.to_csv(A.OUT / "claim11_oracle_runs.csv", index=False)
    S = {}
    for rho, g in R.groupby("rho"):
        d = {"runs": int(len(g)), "oracle_env": float((g.oracle == "env").mean()),
             "stability_mean": float(np.mean(np.maximum(g.stability_env_wins, 1 - g.stability_env_wins))),
             "exp_auc_diff_env_minus_geo": A.boot_mean(g.exp_auc_env - g.exp_auc_geo)}
        for meas in (*MEAS, "always_env", "always_geo"):
            d[f"loss_{meas}"] = float(g[f"loss_{meas}"].mean())
            d[f"relative_loss_{meas}"] = float(g[f"loss_{meas}"].mean() / (g.exp_auc_env - g.exp_auc_geo).abs().mean())
            if meas in MEAS:
                c = g[f"choice_{meas}"]
                ok = (c == g.oracle).to_numpy()
                rec = [ok[(g.oracle == k).to_numpy()].mean() for k in ("env", "geo") if (g.oracle == k).any()]
                d[f"agree_{meas}"], d[f"balanced_acc_{meas}"] = float(ok.mean()), float(np.mean(rec))
        S[str(rho)] = d
    (A.OUT / "claim11_oracle_summary.json").write_text(json.dumps(S, indent=1, default=float), encoding="utf-8")
    for rho, d in S.items():
        print(rho, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in d.items() if not isinstance(v, dict)})


if __name__ == "__main__":
    main()
