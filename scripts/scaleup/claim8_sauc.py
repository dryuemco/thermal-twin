"""claim8_sauc.py: distance-standardised AUC on the 31 fires (plan amendment 6.1 with the strata of 6.3).

z = distance of each test cell to the nearest burned cell of its fold's training set. For every fire, block size
(5, 10, 20 km) and model (null, thermal RF, baseline RF, thermal HGB), sAUC under three target distributions:
  pos     the burned test cells' z in that fire (primary)
  uniform equal weight on the strata that hold burned test cells
  ref     the burned test cells' z pooled over the 31 fires (same Q for every fire)
plus coverage, and the corrected sAUC_c = sAUC + 0.5 - max(0.5, sAUC of the null model). Out-of-fold predictions
come from the cache of analysis_official.py (nothing is refitted).

Also, the margin identity of 6.1: the pooled AUC of the thermal RF (5 km) as the weighted mean of its band AUCs
and the AUC under study-rectangle margins of 0.05, 0.10 and 0.15 degree.

Writes claim8_sauc_per_fire.csv and claim8_sauc_summary.json in $THERMAL_TWIN_SCALEUP/analysis.
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

MODELS = {"null": None, "rf_thermal": (A.THERMAL, "thermal", "rf"), "rf_baseline": (A.BASELINE, "baseline", "rf"),
          "hgb_thermal": (A.THERMAL, "thermal", "hgb")}
ST = G.DEFAULT_STRATA


def zpos_counts(y, z):
    return np.array([((y == 1) & (z >= lo) & (z < hi)).sum() for lo, hi in ST], float)


def main():
    F = A.load_fires()
    ids = [i for i in F if i != "montiferru_2021"]
    cache = {}
    for fid in ids:
        f = F[fid]
        for k in A.BLOCKS:
            if len(np.unique(f.blocks(k))) < 5:
                continue
            z = f.train_pos_dist(k)
            s = {m: (f.null_oof(k) if v is None else f.oof(v[0], v[1], v[2], k)) for m, v in MODELS.items()}
            cache[(fid, k)] = (f.y, z, s)
    qref = {k: sum(zpos_counts(y, z) for (fid, kk), (y, z, _) in cache.items() if kk == k) for k in A.BLOCKS}
    rows = []
    for (fid, k), (y, z, s) in cache.items():
        qp = zpos_counts(y, z)
        qu = (qp > 0).astype(float)
        r = {"fire": fid, "blocks": k}
        for qn, q in (("pos", qp), ("uniform", qu), ("ref", qref[k])):
            res = {m: G.standardised_auc(y, s[m], z, q=q) for m in MODELS}
            for m, v in res.items():
                r[f"sauc_{qn}_{m}"], r[f"cov_{qn}_{m}"] = v["sauc"], v["coverage"]
            for m in MODELS:
                if m != "null":
                    r[f"saucc_{qn}_{m}"] = res[m]["sauc"] + 0.5 - max(0.5, res["null"]["sauc"])
        for m in MODELS:
            r[f"auc_{m}"] = G.auc(y, s[m])
        rows.append(r)
        if k == 10:
            print(fid, {c: round(r[c], 3) for c in ("auc_rf_thermal", "auc_null", "sauc_pos_rf_thermal",
                                                     "sauc_pos_null", "saucc_pos_rf_thermal", "cov_pos_rf_thermal")}, flush=True)
    R = pd.DataFrame(rows)
    R.to_csv(A.OUT / "claim8_sauc_per_fire.csv", index=False)
    S = {"strata_km": [[lo, (hi if np.isfinite(hi) else None)] for lo, hi in ST], "min_support": [20, 20], "min_coverage": 0.8}
    for k in A.BLOCKS:
        g = R[R.blocks == k]
        d = {"fires": int(len(g))}
        for qn in ("pos", "uniform", "ref"):
            for m in MODELS:
                d[f"sauc_{qn}_{m}"] = A.boot_mean(g[f"sauc_{qn}_{m}"])
                d[f"supported_{qn}_{m}"] = f"{int(g[f'sauc_{qn}_{m}'].notna().sum())} of {len(g)}"
                d[f"coverage_{qn}_{m}"] = A.boot_mean(g[f"cov_{qn}_{m}"])
                if m != "null":
                    d[f"saucc_{qn}_{m}"] = A.boot_mean(g[f"saucc_{qn}_{m}"])
            d[f"rf_thermal_beats_null_{qn}"] = A.count(g[f"sauc_{qn}_rf_thermal"].to_numpy(), g[f"sauc_{qn}_null"].to_numpy())
            d[f"thermal_minus_baseline_{qn}"] = A.boot_mean(g[f"sauc_{qn}_rf_thermal"] - g[f"sauc_{qn}_rf_baseline"])
        S[f"blocks_{k}_cells"] = d
    # margin identity (thermal RF, 5 km)
    B = pd.read_csv(A.OUT / "claims12_bands.csv")
    B = B[B.fire.isin(ids)]
    ident = []
    for fid, g in B.groupby("fire"):
        if g.auc_rf_thermal.notna().all():
            w = g.negatives / g.negatives.sum()
            ident.append(float((w * g.auc_rf_thermal).sum()))
    P = pd.read_csv(A.OUT / "claims12_per_fire.csv").set_index("fire")
    full = [P.loc[fid, "auc_rf_thermal_b10"] for fid, g in B.groupby("fire") if g.auc_rf_thermal.notna().all()]
    S["margin_identity"] = {"fires": len(ident), "max_abs_diff": float(np.max(np.abs(np.subtract(ident, full)))),
                            "negative_share_by_band": (B.groupby("band").negatives.sum() / B.negatives.sum()).to_dict()}
    V = pd.read_csv(A.OUT / "claim1_validity_per_fire.csv")
    S["margins_deg"] = {"0.05": A.boot_mean(V["m0.05_auc_rf"]), "0.10": A.boot_mean(V["m0.1_auc_rf"]),
                        "0.15": A.boot_mean(V["auc_rf"]), "null_0.05": A.boot_mean(V["m0.05_auc_null"]),
                        "null_0.10": A.boot_mean(V["m0.1_auc_null"]), "null_0.15": A.boot_mean(V["auc_null"])}
    (A.OUT / "claim8_sauc_summary.json").write_text(json.dumps(S, indent=1, default=float), encoding="utf-8")
    for k in A.BLOCKS:
        d = S[f"blocks_{k}_cells"]
        print(k, {c: (round(d[c]["mean"], 3) if isinstance(d[c], dict) and d[c].get("mean") is not None else d[c])
                  for c in ("sauc_pos_null", "sauc_pos_rf_thermal", "saucc_pos_rf_thermal", "supported_pos_rf_thermal",
                            "coverage_pos_rf_thermal", "rf_thermal_beats_null_pos", "sauc_ref_rf_thermal")})


if __name__ == "__main__":
    main()
