"""claim13_calibrated.py: semi-synthetic scenarios calibrated to the clustering of the real fires (plan 8.5).

Calibration (seed 50,000,000 + 1000 * fire index + grid index): for each fire and a in {0.5, 1, 2}, one draw for
each b in {2, 4, 8, 16} and L in {5, 10, 20, 40} km of the 6.2 design (5 km blocks); the (b, L) minimising
|null AUC - 0.958| / 0.05 + |kept share - 0.57| / 0.10 is retained. Main run (seed 60,000,000 + 100,000 * draw +
1000 * fire index + 10 * a index): three draws per fire and a at the retained (b, L), rho = 0 truth.
Comparison table of simulated against real fires: null AUC, kept share, sAUC support, burned share.

Writes claim13_calibration.csv, claim13_runs.csv and claim13_compare.json.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analysis_official as A  # noqa: E402
import claim9_synthetic as C9  # noqa: E402
import claim12_replicates as C12  # noqa: E402

A_GRID, B_GRID, L_GRID = (0.5, 1, 2), (2, 4, 8, 16), (5, 10, 20, 40)
T_NULL, T_KEPT = 0.958, 0.57


def main():
    F = A.load_fires()
    ids = [i for i in F if i != "montiferru_2021"]
    cal_p, run_p = A.OUT / "claim13_calibration.csv", A.OUT / "claim13_runs.csv"
    cal = pd.read_csv(cal_p) if cal_p.exists() else pd.DataFrame()
    runs = pd.read_csv(run_p) if run_p.exists() else pd.DataFrame()
    for fi, fid in enumerate(ids):
        f = F[fid]
        E = C9.zs(sum(s * C9.zs(f.df[c]) for c, s in C9.SIGNAL))
        prev = f.nb / f.n
        if not len(cal) or fid not in set(cal.fire):
            rows = []
            gi = 0
            for a in A_GRID:
                for b in B_GRID:
                    for L in L_GRID:
                        r = C12.one_run(f, E, prev, a, b, L, 10, 50_000_000 + 1000 * fi + gi)
                        gi += 1
                        rows.append({"fire": fid, "a": a, "b": b, "L": L, "auc_null": r["auc_null"],
                                     "kept_share": r["kept_share"],
                                     "loss": abs(r["auc_null"] - T_NULL) / 0.05 + abs(r["kept_share"] - T_KEPT) / 0.10})
            cal = pd.concat([cal, pd.DataFrame(rows)], ignore_index=True)
            cal.to_csv(cal_p, index=False)
        if len(runs) and fid in set(runs.fire):
            continue
        rows = []
        for ai, a in enumerate(A_GRID):
            g = cal[(cal.fire == fid) & (cal.a == a)].sort_values("loss").iloc[0]
            for d in range(3):
                r = C12.one_run(f, E, prev, a, g.b, g.L, 10, 60_000_000 + 100_000 * d + 1000 * fi + 10 * ai)
                rows.append({"fire": fid, "a": a, "b": g.b, "L": g.L, "draw": d, **r})
        runs = pd.concat([runs, pd.DataFrame(rows)], ignore_index=True)
        runs.to_csv(run_p, index=False)
        print(fid, "done", flush=True)
    real = pd.read_csv(A.OUT / "claims12_per_fire.csv")
    real = real[real.fire.isin(ids)]
    real_sauc = pd.read_csv(A.OUT / "claim8_sauc_per_fire.csv")
    real_sauc = real_sauc[(real_sauc.blocks == 10) & real_sauc.fire.isin(ids)]
    S = {"real": {"auc_null": float(real.auc_null_b10.mean()), "kept_share": float(real.pwd_share_pos_b10.mean()),
                  "sauc_supported": float(real_sauc.sauc_pos_rf_thermal.notna().mean()), "burned_share": float(real.prevalence.mean())},
         "simulated": {"auc_null": float(runs.auc_null.mean()), "kept_share": float(runs.kept_share.mean()),
                       "sauc_supported": float((runs.sauc_coverage >= 0.8).mean()),
                       "burned_share": float((runs.burned / runs.fire.map({i: F[i].n for i in ids})).mean())},
         "retained_bL": cal.loc[cal.groupby(["fire", "a"]).loss.idxmin(), ["fire", "a", "b", "L"]].to_dict("records")}
    (A.OUT / "claim13_compare.json").write_text(json.dumps(S, indent=1, default=float), encoding="utf-8")
    print(json.dumps({k: S[k] for k in ("real", "simulated")}, indent=1))


if __name__ == "__main__":
    main()
