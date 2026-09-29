"""R8j. Effect of using pre-fire land cover (WorldCover v100, 2020) instead of v200 (2021).

Input: r8i_worldcover_cells.csv.gz (cell values of both years, built by r8i) and the released
modelling datasets. For each region:
  * how many valid cells, and how many burned cells, change natural-vegetation membership
    (tree + shrub + grass >= 0.5) or dominant class between the two maps;
  * the gate fraction (share of burned cells with natural vegetation >= 0.5) under both maps;
  * the within-region thermal gain (10-cell blocks, as Table 1) and the raw transfer matrix
    (study areas as drawn, both feature sets) refitted with the 2020 population and the 2020
    dominant class as the land-cover predictor.
Everything else (predictors, labels, model, seed, folds) is unchanged.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "paper" / "code"))
import ems_inference_common as E  # noqa: E402

E.N_JOBS = 8
REG = E.REGIONS
TH, BA = E.THERMAL, E.BASELINE
C = pd.read_csv(HERE / "r8i_worldcover_cells.csv.gz")


def pops(reg):
    d = E.C.load(reg)
    d = d[d.valid_for_modeling == True].merge(C[C.region == reg], on=["row_500m", "col_500m"], how="left")  # noqa: E712
    d["pop2021"] = d.burnable_tree_shrub_grass.astype(bool)
    d["pop2020"] = d.tsg_fraction_2020 >= 0.5
    return d


out, data21, data20 = {"regions": {}}, {}, {}
for reg in REG:
    d = pops(reg)
    b = d.burned == 1
    info = {
        "valid_cells": int(len(d)),
        "population_2021": int(d.pop2021.sum()), "population_2020": int(d.pop2020.sum()),
        "population_both": int((d.pop2021 & d.pop2020).sum()),
        "burned_valid": int(b.sum()),
        "burned_in_pop_2021": int((b & d.pop2021).sum()), "burned_in_pop_2020": int((b & d.pop2020).sum()),
        "burned_leave_population": int((b & d.pop2021 & ~d.pop2020).sum()),
        "burned_enter_population": int((b & ~d.pop2021 & d.pop2020).sum()),
        "unburned_leave_population": int((~b & d.pop2021 & ~d.pop2020).sum()),
        "unburned_enter_population": int((~b & ~d.pop2021 & d.pop2020).sum()),
        "dominant_changed_valid": float((d.dominant_2020 != d.dominant_2021).mean()),
        "dominant_changed_burned": float((d.dominant_2020[b] != d.dominant_2021[b]).mean()),
        "burned_dominant_transitions_top": {
            f"{int(a)}->{int(c)}": int(n) for (a, c), n in
            d[b & (d.dominant_2020 != d.dominant_2021)].groupby(["dominant_2020", "dominant_2021"]).size()
            .sort_values(ascending=False).head(5).items()},
        "gate_fraction_2021": float((d.tsg_fraction_2021[b] >= 0.5).mean()),
        "gate_fraction_2020": float((d.tsg_fraction_2020[b] >= 0.5).mean()),
    }
    p21 = d[d.pop2021].reset_index(drop=True)
    p20 = d[d.pop2020].reset_index(drop=True).copy()
    p20["landcover_dominant"] = p20.dominant_2020
    data21[reg], data20[reg] = p21, p20
    for tag, dd in (("2021", p21), ("2020", p20)):
        th = roc_auc_score(dd.burned, E.blocked_oof(dd, TH, 10))
        ba = roc_auc_score(dd.burned, E.blocked_oof(dd, BA, 10))
        info[f"within_{tag}"] = {"thermal": th, "baseline": ba, "gain": th - ba}
    out["regions"][reg] = info
    print(reg, json.dumps({k: v for k, v in info.items() if k != "burned_dominant_transitions_top"}, default=float), flush=True)

rows = []
for tag, D in (("2021", data21), ("2020", data20)):
    fits = {s: {lbl: E.fit(fe, D[s]) for lbl, fe in (("thermal", TH), ("baseline", BA))} for s in REG}
    for s in REG:
        for t in REG:
            if s == t:
                continue
            r = {"landcover": tag, "direction": f"{s}_to_{t}"}
            for lbl, fe in (("thermal", TH), ("baseline", BA)):
                r[lbl] = float(roc_auc_score(D[t].burned, fits[s][lbl].predict_proba(D[t][fe])[:, 1]))
            r["delta"] = r["thermal"] - r["baseline"]
            rows.append(r)
T = pd.DataFrame(rows)
T.to_csv(HERE / "r8j_transfer_2020_vs_2021.csv", index=False)
ref = pd.read_csv(ROOT / "paper/labelfix_rerun/round5/collar/aoi_frame_transfer.csv")
ref = ref[(ref.source_frame == "full") & (ref.target_frame == "full")].set_index("direction")
t21 = T[T.landcover == "2021"].set_index("direction")
out["transfer_2021_reproduction_max_abs_diff"] = float((t21.thermal - ref.thermal.reindex(t21.index)).abs().max())
for tag in ("2021", "2020"):
    s = T[T.landcover == tag]
    out[f"transfer_{tag}"] = {"mean_thermal": float(s.thermal.mean()), "mean_baseline": float(s.baseline.mean()),
                              "mean_delta": float(s.delta.mean()), "below_chance": int((s.thermal < 0.5).sum())}
a = T[T.landcover == "2021"].set_index("direction")
b = T[T.landcover == "2020"].set_index("direction")
out["transfer_max_abs_change_thermal"] = float((a.thermal - b.thermal).abs().max())
out["transfer_directions_changing_side"] = [d for d in a.index if (a.thermal[d] < 0.5) != (b.thermal[d] < 0.5)]
json.dump(out, open(HERE / "r8j_summary.json", "w"), indent=1, default=float)
print(json.dumps({k: v for k, v in out.items() if k != "regions"}, indent=1))
