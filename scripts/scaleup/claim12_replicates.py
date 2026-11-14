"""claim12_replicates.py: Monte Carlo replicates (plan 8.3) and the 20 km design (plan 8.4) of the semi-synthetic
experiment of 6.2. Same latent risk, label rule, models and measures as claim9_synthetic.py; rho = 0 truth.

  python claim12_replicates.py                 five draws per fire and scenario, 5 km blocks (8.3)
  python claim12_replicates.py --blocks 40     one draw, 20 km blocks (8.4)

Writes claim12_runs_b<blocks>.csv (resumable; one row per fire, scenario and draw).
"""
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


def one_run(f, E, prev, a, b, L, k, seed):
    rng = np.random.default_rng(seed)
    y1 = C9.labels(a * E + b * C9.grf(f, L, rng) + rng.standard_normal(f.n), prev)
    y2 = C9.labels(a * E + b * C9.grf(f, L, rng) + rng.standard_normal(f.n), prev)
    X_env = np.c_[np.c_[[C9.zs(f.df[c]) for c, _ in C9.SIGNAL]].T, rng.standard_normal((f.n, 2))]
    folds = list(StratifiedGroupKFold(5, shuffle=True, random_state=A.SEED).split(X_env, y1, groups=f.blocks(k)))
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
    r = {"burned": int(y1.sum()), "auc_null": G.auc(y1, null), "kept_share": len(pairs) / 2 / max(1, y1.sum()),
         "truth_null": G.auc(y2, null)}
    for name, o in sc.items():
        s = G.standardised_auc(y1, o, z)
        r.update({f"truth_{name}": G.auc(y2, o), f"auc_{name}": G.auc(y1, o),
                  f"cauc_{name}": G.calibrated_auc(y1, o, null, pairs)["cauc"],
                  f"saucc_{name}": s["sauc"] + 0.5 - max(0.5, sn) if np.isfinite(sn) else np.nan,
                  "sauc_coverage": s["coverage"]})
    return r


def main():
    k = int(sys.argv[sys.argv.index("--blocks") + 1]) if "--blocks" in sys.argv else 10
    draws, base = (5, 30_000_000) if k == 10 else (1, 40_000_000)
    out = A.OUT / f"claim12_runs_b{k}.csv"
    F = A.load_fires()
    ids = [i for i in F if i != "montiferru_2021"]
    prev_df = pd.read_csv(out) if out.exists() else pd.DataFrame()
    done = set(zip(prev_df.fire, prev_df.scenario, prev_df.draw)) if len(prev_df) else set()
    skipped = []
    for fi, fid in enumerate(ids):
        f = F[fid]
        if len(np.unique(f.blocks(k))) < 5:
            skipped.append(fid)
            continue
        E = C9.zs(sum(s * C9.zs(f.df[c]) for c, s in C9.SIGNAL))
        rows = []
        for d in range(draws):
            for si, (a, b, L) in enumerate(C9.SCEN):
                if (fid, si, d) in done:
                    continue
                r = one_run(f, E, f.nb / f.n, a, b, L, k, base + 100_000 * d + 1000 * fi + si)
                rows.append({"fire": fid, "scenario": si, "draw": d, "a": a, "b": b, "L": L, "blocks": k, **r})
        if rows:
            prev_df = pd.concat([prev_df, pd.DataFrame(rows)], ignore_index=True)
            prev_df.to_csv(out, index=False)
        print(fid, "done", len(prev_df), flush=True)
    print("skipped (fewer than five blocks):", skipped)


if __name__ == "__main__":
    main()
