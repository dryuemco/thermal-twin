"""Analysis 5 (SPEC.md): prevalence-robust metrics on every frame.

Within-region: row-A OOF thermal scores on region-wide, scar + 2 km (per scar) and the
10 km collar. Transfer: summarises a5_transfer_metrics_by_direction.csv written by
ems_geometry_4_labelfree.py.
"""
import numpy as np
import pandas as pd

import ems_geometry_common as G

METRICS = ["auc", "pauc01", "ap", "ap_lift", "cap10", "cap10_norm", "cap20", "cap20_norm"]
reg_rows, scar_rows = [], []
for reg in G.REGIONS:
    R = G.Region(reg)
    oof = G.oof_row_a(R)
    frames = {"region_wide": np.ones(len(R.y), bool), "collar_10km": R.dist_collar <= 10}
    region_vals = {}
    for fname, m in frames.items():
        row = {"region": reg, "frame": fname, **G.metric_set(R.y[m], oof[m])}
        region_vals[fname] = row
        for met in ("pauc01", "ap_lift", "cap10_norm", "cap20_norm"):
            fn = {"pauc01": lambda y, s: G.metric_set(y, s)["pauc01"],
                  "ap_lift": lambda y, s: G.metric_set(y, s)["ap_lift"],
                  "cap10_norm": lambda y, s: G.metric_set(y, s)["cap10_norm"],
                  "cap20_norm": lambda y, s: G.metric_set(y, s)["cap20_norm"]}[met]
            lo, hi, _ = G.block_boot(R.y[m], oof[m], R.block10_codes[m], fn, B=1000)
            row[f"{met}_lo"], row[f"{met}_hi"] = lo, hi
        reg_rows.append(row)
        print(reg, fname, {k: round(row[k], 3) for k in METRICS}, flush=True)
    for sc in R.scars():
        h = sc["held"]
        row = {"region": reg, "scar": sc["scar"], **G.metric_set(R.y[h], oof[h])}
        for met in METRICS:
            row[f"drop_{met}"] = region_vals["region_wide"][met] - row[met]
        scar_rows.append(row)

Rg, S = pd.DataFrame(reg_rows), pd.DataFrame(scar_rows)
Rg.to_csv(G.OUT / "a5_within_region_frames.csv", index=False)
S.to_csv(G.OUT / "a5_within_scar_frames.csv", index=False)
summ = {"within_scar_drop": {}, "within_means": {}, "transfer": {}}
for label, sub in (("nine_scars", S), ("eight_scars_table2", S[S.region != "bejis_2022"])):
    summ["within_scar_drop"][label] = {}
    for met in METRICS:
        m, lo, hi, n = G.t_ci(sub[f"drop_{met}"])
        mc, loc, hic, nc = G.region_cluster_ci(sub[f"drop_{met}"].to_numpy(), sub.region.to_numpy())
        summ["within_scar_drop"][label][met] = {"mean_region_wide_minus_scar": m, "scar_t": [lo, hi],
                                                "region_cluster": [loc, hic], "mean_scar_value": sub[met].mean(),
                                                "n": n}
    summ["within_scar_drop"][label]["mean_scar_prevalence"] = sub.prevalence.mean()
for fname in ("region_wide", "collar_10km"):
    sub = Rg[Rg.frame == fname]
    summ["within_means"][fname] = {met: G.t_ci(sub[met])[:3] for met in METRICS + ["prevalence"]}
T = pd.read_csv(G.OUT / "a5_transfer_metrics_by_direction.csv")
for (fr, mdl), sub in T.groupby(["frame", "model"]):
    summ["transfer"][f"{fr}|{mdl}"] = {met: float(sub[met].mean()) for met in METRICS + ["prevalence"]}
    summ["transfer"][f"{fr}|{mdl}"]["directions"] = int(len(sub))
    summ["transfer"][f"{fr}|{mdl}"]["pauc01_above_0_5"] = int((sub.pauc01 > 0.5).sum())
G.dump(summ, "a5_summary.json")
pd.set_option("display.width", 250)
print(Rg[["region", "frame", "prevalence"] + METRICS].round(3).to_string())
print(S[["region", "scar", "prevalence"] + METRICS].round(3).to_string())
for label in summ["within_scar_drop"]:
    print(label)
    for met in METRICS:
        v = summ["within_scar_drop"][label][met]
        print(f"  {met:11s} drop {v['mean_region_wide_minus_scar']:+.3f} scar-t [{v['scar_t'][0]:+.3f},{v['scar_t'][1]:+.3f}]"
              f" region-cl [{v['region_cluster'][0]:+.3f},{v['region_cluster'][1]:+.3f}]")
tt = pd.DataFrame(summ["transfer"]).T
print(tt.round(3).to_string())
