"""EMS referee round, R2 major 4: equivalence / non-inferiority. SPEC Task 2.

Margins fixed in SPEC.md before computation: +-0.02 and +-0.05 ROC-AUC. TOST at alpha = 0.05 per
side == the two-sided 90 % interval inside (-m, +m).
Inputs: frozen per-direction deltas; within-region increments from ladder_raw.json.
"""
import json

import numpy as np
import pandas as pd

import ems_inference_common as E
from ems_inference_units import UNITS, intervals, quantities

MARGINS = (0.02, 0.05)
raw = json.load(open(E.OUTDIR / "ladder_raw.json"))
BL = pd.DataFrame(raw["blocked"])
LO = pd.DataFrame(raw["loso"])
FO = pd.DataFrame(raw["foreign"])
out = {"margins": MARGINS}

# ---------------------------------------------------------------- TOST on the transfer increment
Q = quantities()
tost = {}
for name in ("Q2_equalised10_delta", "Q1_asdrawn_delta", "S_equalised5_delta"):
    if name not in Q:  # Q1 omitted when its class-B input is absent (see units.quantities)
        tost[name] = {"skipped": "class-B input transfer_ci_blocksize.json absent"}
        continue
    y, s, t, _ = Q[name]
    iv90 = intervals(y, s, t, level=0.90)
    rows = {}
    for u in UNITS:
        lo, hi = iv90[u][0], iv90[u][1]
        if np.isnan(lo):
            rows[u] = {"ci90": [lo, hi], "undefined": True}
            continue
        rows[u] = {"ci90": [lo, hi],
                   "no_gain_larger_than_X": hi,
                   **{f"equivalent_within_{m}": bool(lo > -m and hi < m) for m in MARGINS}}
    tost[name] = {"mean": float(np.mean(y)), "units": rows}
out["tost_transfer_increment"] = tost

# ---------------------------------------------------------------- W - T, matched frame and blocking
af = pd.read_csv(E.PAPER / "aoi_frame_transfer_frozen_mugla.csv")
af["tgt"] = af.direction.str.split("_to_").str[1]
wt = {}
for wframe, (sf, tf) in (("10km", ("10km", "10km")), ("5km", ("5km", "5km")), ("full", ("full", "full"))):
    W = BL[(BL.frame == wframe) & (BL.B == 10)].set_index("region").increment
    T = af[(af.source_frame == sf) & (af.target_frame == tf)].groupby("tgt").delta.mean()
    D = (W - T).reindex(E.REGIONS)
    m, lo95, hi95 = E.t_ci(D.to_numpy(), 0.95)
    _, lo90, hi90 = E.t_ci(D.to_numpy(), 0.90)
    wt[wframe] = {"per_region": {E.SHORT[r]: {"W": float(W[r]), "T": float(T[r]), "W_minus_T": float(D[r])}
                                 for r in E.REGIONS},
                  "mean_W": float(W.mean()), "mean_T": float(T.mean()),
                  "mean_W_minus_T": m, "ci95_t4": [lo95, hi95], "ci90_t4": [lo90, hi90],
                  "smaller_by_at_least_Y": lo90}
out["within_minus_transfer_increment"] = wt

# ---------------------------------------------------------------- scar frame: LOSO vs foreign
fo = FO.groupby(["region", "scar"]).increment.mean().rename("foreign_inc").reset_index()
S = LO[LO.frame == "full"][["region", "scar", "increment"]].merge(fo, on=["region", "scar"])
d = (S.increment - S.foreign_inc).to_numpy()
cl = S.region.to_numpy()
m, a95, b95 = E.t_ci(d, 0.95)
_, a90, b90 = E.t_ci(d, 0.90)
_, c95a, c95b, _ = E.cr1_ci(d, cl, 0.95)
_, c90a, c90b, _ = E.cr1_ci(d, cl, 0.90)
out["scar_frame_loso_minus_foreign"] = {"mean": m, "t95": [a95, b95], "t90": [a90, b90],
                                        "cr1_95": [c95a, c95b], "cr1_90": [c90a, c90b],
                                        "n": int(len(d))}
fi = S.foreign_inc.to_numpy()
m, a90, b90 = E.t_ci(fi, 0.90)
_, c90a, c90b, _ = E.cr1_ci(fi, cl, 0.90)
out["scar_frame_foreign_increment_tost"] = {
    "mean": m, "t90": [a90, b90], "cr1_90": [c90a, c90b],
    **{f"equivalent_within_{mg}_t": bool(a90 > -mg and b90 < mg) for mg in MARGINS},
    **{f"equivalent_within_{mg}_cr1": bool(c90a > -mg and c90b < mg) for mg in MARGINS}}

json.dump(out, open(E.OUTDIR / "equivalence.json", "w"), indent=1, default=float)
print(json.dumps(out, indent=1, default=lambda v: round(float(v), 4)))
