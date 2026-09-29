"""R8d and R8f. Permutation inference for the similarity measures, a sensitivity without Manavgat,
and the equivalence test on the as-drawn transfer gain (reviewer 2, M2 and M10; reviewer 1, M8).

No model is fitted. Inputs are the released per-direction files of round 5:
  round5/out_official/regime_transfer_correlation.json    (marginal and regime measures)
  round5/out_official/conditional_similarity_transfer.json (conditional measures)
  round5/out_official/niche_overlap_transfer.json          (niche overlap)
  round5/collar/aoi_frame_transfer.csv                     (per-direction paired gains)

Permutation test (QAP / Mantel type): the five region labels of the transfer matrix are permuted
against the fixed measure matrix, all 120 permutations; the two-sided p-value is the share of
permutations with |rho| at least the observed |rho|. Directions where a measure is undefined are
dropped before permuting. The smallest attainable p-value is therefore 1/120 at best.
"""
import itertools
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "paper" / "code"))
R5 = ROOT / "paper/labelfix_rerun/round5"
REG = ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended", "montiferru_2021"]

reg = json.load(open(R5 / "out_official/regime_transfer_correlation.json"))["per_direction"]
con = json.load(open(R5 / "out_official/conditional_similarity_transfer.json"))["per_direction"]
nic = json.load(open(R5 / "out_official/niche_overlap_transfer.json"))["per_direction"]
T = {r["direction"]: dict(r) for r in reg}
for r in con + nic:
    T[r["direction"]].update({k: v for k, v in r.items() if k not in ("direction", "source", "target")})
D = pd.DataFrame(T.values())
D["source"] = D.direction.str.split("_to_").str[0]
D["target"] = D.direction.str.split("_to_").str[1]
y_col = "raw_thermal_roc_auc"

MEASURES = ["regime_dist_log_effn", "regime_dist_largest_share", "domain_classifier_auc",
            "target_mean_dissimilarity", "target_p95_dissimilarity", "fraction_inside_weighted_aoa",
            "climate_distance", "geographic_distance_km", "unweighted_fraction_inside_support",
            "agree_count_9", "vector_spearman_9", "cosine_9", "agree_fraction_supported",
            "cosine_supported", "vector_spearman_supported", "schoener_d_mean1d", "warren_i_mean1d",
            "schoener_d_pca2d", "warren_i_pca2d", "mahalanobis_burned"]
MEASURES = [m for m in MEASURES if m in D.columns]

Y = {(s, t): v for s, t, v in zip(D.source, D.target, D[y_col])}


def qap(m):
    sub = D[["source", "target", m]].dropna()
    x = sub[m].to_numpy(float)
    obs = spearmanr(x, [Y[(s, t)] for s, t in zip(sub.source, sub.target)]).statistic
    rhos = []
    for perm in itertools.permutations(range(5)):
        mp = {REG[i]: REG[perm[i]] for i in range(5)}
        yp = [Y[(mp[s], mp[t])] for s, t in zip(sub.source, sub.target)]
        rhos.append(spearmanr(x, yp).statistic)
    rhos = np.array(rhos)
    p = float(np.mean(np.abs(rhos) >= abs(obs) - 1e-12))
    return len(sub), float(obs), p


def no_manavgat(m):
    sub = D[(D.source != "manavgat_2021") & (D.target != "manavgat_2021")][[m, y_col]].dropna()
    if len(sub) < 4 or sub[m].nunique() < 2:
        return len(sub), None
    return len(sub), float(spearmanr(sub[m], sub[y_col]).statistic)


rows = []
for m in MEASURES:
    n, rho, p = qap(m)
    n2, rho2 = no_manavgat(m)
    rows.append({"measure": m, "n_directions": n, "spearman_rho": round(rho, 4),
                 "qap_p_two_sided": round(p, 4), "n_without_manavgat": n2,
                 "rho_without_manavgat": None if rho2 is None else round(rho2, 4)})
P = pd.DataFrame(rows)
P.to_csv(HERE / "r8d_similarity_permutation.csv", index=False)
print(P.to_string(index=False))

# transfer means without Manavgat, both frames
A = pd.read_csv(R5 / "collar/aoi_frame_transfer.csv")
nm = {}
for tag in ("full", "10km"):
    s = A[(A.source_frame == tag) & (A.target_frame == tag)]
    s2 = s[~s.direction.str.contains("manavgat")]
    nm[tag] = {"mean_thermal_all": float(s.thermal.mean()), "mean_thermal_without_manavgat": float(s2.thermal.mean()),
               "mean_delta_all": float(s.delta.mean()), "mean_delta_without_manavgat": float(s2.delta.mean()),
               "below_chance_without_manavgat": int((s2.thermal < 0.5).sum()), "n_without_manavgat": int(len(s2))}

# R8f: equivalence (TOST, 90 % intervals) on the as-drawn paired gain, all units
import ems_inference_units as U  # noqa: E402
s = A[(A.source_frame == "full") & (A.target_frame == "full")]
src = s.direction.str.split("_to_").str[0].to_numpy()
tgt = s.direction.str.split("_to_").str[1].to_numpy()
iv90 = U.intervals(s.delta.to_numpy(), src, tgt, level=0.90)
iv95 = U.intervals(s.delta.to_numpy(), src, tgt, level=0.95)
tost = {}
for u in U.UNITS:
    lo, hi = iv90[u][0], iv90[u][1]
    ok = not (np.isnan(lo) or np.isnan(hi))
    tost[u] = {"ci90": [lo, hi], "ci95": [iv95[u][0], iv95[u][1]],
               "equivalent_within_0.05": bool(ok and lo > -0.05 and hi < 0.05),
               "equivalent_within_0.02": bool(ok and lo > -0.02 and hi < 0.02),
               "undefined": not ok}
out = {"qap": rows, "without_manavgat_transfer": nm,
       "tost_asdrawn_delta": {"mean": float(s.delta.mean()), "units": tost}}
json.dump(out, open(HERE / "r8d_summary.json", "w"), indent=1, default=float)
print(json.dumps(nm, indent=1))
print(json.dumps(out["tost_asdrawn_delta"], indent=1, default=float))
