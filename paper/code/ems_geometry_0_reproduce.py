"""Reproduction gates for the ems_geometry analyses (SPEC.md, "Reproduction gates").

1. Row-A OOF thermal scores per region (cached for Analyses 1, 2, 3, 5); A and B per
   scar compared with paper/pool_decomposition.json.
2. Pair-cluster and target-cluster bootstrap implementations compared with
   paper/equalised_delta_interval.json, recomputed from aoi_frame_transfer_frozen_mugla.csv.
"""
import json

import numpy as np
import pandas as pd

import ems_geometry_common as G

ref = pd.DataFrame(json.load(open(G.PAPER / "pool_decomposition.json")))
rows = []
for reg in G.REGIONS:
    R = G.Region(reg)
    oof = G.oof_row_a(R)
    a = G.auc(R.y, oof)
    for sc in R.scars():
        b = G.auc(R.y[sc["held"]], oof[sc["held"]])
        r = ref[(ref.region == reg) & (ref.scar == sc["scar"])]
        rows.append({"region": reg, "scar": sc["scar"], "A": a, "B": b,
                     "A_ref": float(r.A_region.iloc[0]) if len(r) else None,
                     "B_ref": float(r.B_scar_area.iloc[0]) if len(r) else None})
        print(rows[-1], flush=True)
d = pd.DataFrame(rows)
d["dA"], d["dB"] = d.A - d.A_ref, d.B - d.B_ref
print(d.round(4).to_string())
print(f"mean A {d.A.mean():.4f} (ref {d.A_ref.mean():.4f}); mean B {d.B.mean():.4f} (ref {d.B_ref.mean():.4f}); "
      f"mean A-B {(d.A-d.B).mean():.4f} (ref {(d.A_ref-d.B_ref).mean():.4f})")

# pair-cluster check
T = pd.read_csv(G.PAPER / "aoi_frame_transfer_frozen_mugla.csv")
eq = json.load(open(G.PAPER / "equalised_delta_interval.json"))["results"]
chk = {}
for tag, (sf, tf) in {"as drawn": ("full", "full"), "equalised 10 km": ("10km", "10km"),
                      "equalised 5 km": ("5km", "5km")}.items():
    s = T[(T.source_frame == sf) & (T.target_frame == tf)]
    delta = {tuple(k.split("_to_")): v for k, v in zip(s.direction, s.thermal - s.baseline)}
    chk[tag] = {"mean": float(np.mean(list(delta.values()))),
                "pair_cluster": G.pair_cluster_ci(delta), "pair_cluster_ref": eq[tag]["ci_pair_cluster"],
                "target_cluster": G.target_cluster_ci(delta), "target_cluster_ref": eq[tag]["ci_target_region_cluster"]}
    print(tag, chk[tag])
G.dump({"row_A_B": rows, "pair_cluster_check": chk}, "reproduction_gates.json")
