"""Round 7g (2026-09-29): pair-bootstrap intervals for the two similarity diagnostics that were
recomputed on the 10 km collar (readiness audit F07). Port of corrWithBoot() in
round5/code_control/conditional_similarity.mjs: unordered region pairs resampled with replacement,
both directions carried, mulberry32(42 + offset), 2000 replicates, equal-tailed linear percentiles.
Offsets follow that script's MEASURES order (cosine_9 = 102, agree_fraction_supported = 103).

Input: round6/diag_collar/official_diagnostics_collar_frame.csv (frames "full" and "collar10").
Control: the full-frame values must reproduce round5/out_official/conditional_similarity_transfer.json.
Output: round7/r7g_collar_diagnostics.json
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata

H = Path(__file__).resolve().parent
LF = H.parent
SEED, NBOOT = 42, 2000
OFFSET = {"cosine_9": 102, "agree_fraction_supported": 103}


def mulberry32(a):
    a &= 0xFFFFFFFF

    def imul(x, y):
        return ((x & 0xFFFFFFFF) * (y & 0xFFFFFFFF)) & 0xFFFFFFFF

    def nxt():
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = imul(a ^ (a >> 15), 1 | a)
        t = ((t + imul(t ^ (t >> 7), 61 | t)) & 0xFFFFFFFF) ^ t
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return nxt


def spearman(x, y):
    rx, ry = rankdata(x), rankdata(y)
    if rx.std() == 0 or ry.std() == 0:
        return np.nan
    return float(np.corrcoef(rx, ry)[0, 1])


def q(arr, p):
    s = np.sort(arr)
    i = p * (len(s) - 1)
    lo, hi = int(np.floor(i)), int(np.ceil(i))
    return float(s[lo] + (s[hi] - s[lo]) * (i - lo))


def corr_with_boot(d, key):
    d = d[np.isfinite(d[key])]
    x, y = d[key].to_numpy(), d.transfer.to_numpy()
    pk = d.direction.map(lambda s: "|".join(sorted(s.split("_to_"))))
    pairs = list(dict.fromkeys(pk))
    by = {p: np.flatnonzero((pk == p).to_numpy()) for p in pairs}
    rnd = mulberry32(SEED + OFFSET[key])
    rhos = []
    for _ in range(NBOOT):
        idx = np.concatenate([by[pairs[int(rnd() * len(pairs))]] for _ in range(len(pairs))])
        r = spearman(x[idx], y[idx])
        if np.isfinite(r):
            rhos.append(r)
    return {"n_directions": int(len(d)), "n_pairs": len(pairs), "spearman_rho": spearman(x, y),
            "ci95": [q(rhos, 0.025), q(rhos, 0.975)], "n_valid": len(rhos)}


src = pd.read_csv(LF / "round6" / "diag_collar" / "official_diagnostics_collar_frame.csv")
out = {f: {k: corr_with_boot(src[src.frame == f].reset_index(drop=True), k) for k in OFFSET}
       for f in ["full", "collar10"]}
ref = json.load(open(LF / "round5" / "out_official" / "conditional_similarity_transfer.json", encoding="utf-8"))
out["control_reference_full_frame"] = {m["key"]: {"rho": m["full_set"]["spearman_rho"], "ci95": m["full_set"]["spearman_ci95"]}
                                       for m in ref["correlations"] if m["key"] in OFFSET}
json.dump(out, open(H / "r7g_collar_diagnostics.json", "w"), indent=1)
print(json.dumps(out, indent=1))
