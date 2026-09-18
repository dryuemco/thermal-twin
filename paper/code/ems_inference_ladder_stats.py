"""Task 1 statistics from ladder_raw.json (written by ems_inference_ladder.py). SPEC Task 1."""
import json

import numpy as np
import pandas as pd

import ems_inference_common as E
from ems_inference_units import intervals

raw = json.load(open(E.OUTDIR / "ladder_raw.json"))
BL = pd.DataFrame(raw["blocked"])
BS = pd.DataFrame(raw["blocked_scar"])
LO = pd.DataFrame(raw["loso"])
HS = pd.DataFrame(raw["halfsplit"])
FO = pd.DataFrame(raw["foreign"])
out = {}


def three(x, cl):
    m, lo, hi = E.t_ci(x)
    _, clo, chi, _ = E.cr1_ci(x, cl)
    _, blo, bhi = E.cluster_boot_ci(x, cl)
    return {"mean": m, "n": int(len(x)), "G": int(len(np.unique(cl))),
            "t_scar": [lo, hi], "cr1_region_tG-1": [clo, chi], "region_cluster_boot": [blo, bhi]}


# --- reproduction checks
ref = pd.DataFrame(json.load(open(E.PAPER / "scar_increment.json")))
m = LO[LO.frame == "full"].merge(ref, on=["region", "scar"], suffixes=("", "_ref"))
out["repro_loso_vs_scar_increment_json_maxabs"] = float((m.increment - m.increment_ref).abs().max())
mh = json.load(open(E.PAPER / "matched_holdout.json"))
mh = pd.DataFrame(mh)
bt = BS[BS.B == 10].merge(mh, on=["region", "scar"])
out["repro_rowB_thermal_vs_matched_holdout_maxabs"] = float((bt.thermal - bt.B_seen_same_cells).abs().max())

# --- 1a scar frame
fo = FO.groupby(["region", "scar"]).agg(foreign_inc=("increment", "mean"),
                                        foreign_th=("thermal", "mean"),
                                        foreign_base=("baseline", "mean")).reset_index()
lo = LO[LO.frame == "full"][["region", "scar", "baseline", "thermal", "increment"]].rename(
    columns={"baseline": "loso_base", "thermal": "loso_th", "increment": "loso_inc"})
res1a = {}
for B in (10, 2):
    b = BS[BS.B == B][["region", "scar", "baseline", "thermal", "increment"]].rename(
        columns={"baseline": "blk_base", "thermal": "blk_th", "increment": "blk_inc"})
    region_wide = BL[(BL.frame == "full") & (BL.B == B)][["region", "increment"]].rename(
        columns={"increment": "regionwide_inc"})
    T = b.merge(lo, on=["region", "scar"]).merge(fo, on=["region", "scar"]).merge(region_wide, on="region")
    T["blk_minus_loso"] = T.blk_inc - T.loso_inc
    T["loso_minus_foreign"] = T.loso_inc - T.foreign_inc
    T["blk_minus_foreign"] = T.blk_inc - T.foreign_inc
    T["regionwide_minus_blkscar"] = T.regionwide_inc - T.blk_inc
    cl = T.region.to_numpy()
    res1a[f"B{B}"] = {
        "per_scar": T.round(4).to_dict("records"),
        "means": {c: float(T[c].mean()) for c in ("regionwide_inc", "blk_inc", "loso_inc", "foreign_inc")},
        "blk_minus_loso": three(T.blk_minus_loso.to_numpy(), cl),
        "loso_minus_foreign": three(T.loso_minus_foreign.to_numpy(), cl),
        "blk_minus_foreign": three(T.blk_minus_foreign.to_numpy(), cl),
        "regionwide_minus_blkscar": three(T.regionwide_minus_blkscar.to_numpy(), cl),
        "blk_inc": three(T.blk_inc.to_numpy(), cl),
        "loso_inc": three(T.loso_inc.to_numpy(), cl),
        "foreign_inc": three(T.foreign_inc.to_numpy(), cl),
    }
# Bejis blocked-on-scar (no LOSO pair) reported separately
res1a["bejis_blocked_scar_unpaired"] = BS[BS.region == "bejis_2022"].round(4).to_dict("records")
out["scar_frame"] = res1a

# --- 1b ladder by frame
af = pd.read_csv(E.PAPER / "aoi_frame_transfer_frozen_mugla.csv")
af["src"] = af.direction.str.split("_to_").str[0]
af["tgt"] = af.direction.str.split("_to_").str[1]
lad = {}
for tag, ftag in (("full", ("full", "full")), ("10km", ("10km", "10km"))):
    L = {}
    for B in (10, 2):
        x = BL[(BL.frame == tag) & (BL.B == B)]
        mm, a, b = E.t_ci(x.increment)
        L[f"blocked_B{B}"] = {"mean": mm, "t_regions": [a, b],
                              "per_region": dict(zip(x.region.map(E.SHORT), x.increment.round(4)))}
    h = HS[(HS.frame == tag) & HS.increment.notna()]
    rm = h.groupby("region").increment.mean()
    mm, a, b = E.t_ci(rm.to_numpy())
    L["halfsplit"] = {"mean_over_splits": float(h.increment.mean()), "n_splits": int(len(h)),
                      "n_positive": int((h.increment > 0).sum()),
                      "mean_of_region_means": mm, "t_region_means": [a, b],
                      "cr1_splits_by_region": list(E.cr1_ci(h.increment.to_numpy(), h.region.to_numpy())[1:3])}
    l = LO[LO.frame == tag]
    mm, a, b = E.t_ci(l.increment)
    L["loso"] = {"mean": mm, "t_scars": [a, b], "n": int(len(l)),
                 "cr1_region": list(E.cr1_ci(l.increment.to_numpy(), l.region.to_numpy())[1:3]),
                 "target_cells_lost_to_collar": int(l.target_cells_lost_to_collar.sum())}
    c = af[(af.source_frame == ftag[0]) & (af.target_frame == ftag[1])]
    iv = intervals(c.delta.to_numpy(), c.src.to_numpy(), c.tgt.to_numpy())
    L["cross_region"] = {"mean": float(c.delta.mean()), "pair_cluster_boot": iv["pair_cluster_boot"][:2],
                         "loro_jackknife_t4": iv["loro_jackknife_t4"][:2],
                         "target_cluster_boot": iv["target_cluster_boot"][:2]}
    lad[tag] = L
x5 = BL[(BL.frame == "5km") & (BL.B == 10)]
lad["5km_blocked_B10"] = {"mean": float(x5.increment.mean()),
                          "per_region": dict(zip(x5.region.map(E.SHORT), x5.increment.round(4)))}
out["ladder_by_frame"] = lad

json.dump(out, open(E.OUTDIR / "ladder_summary.json", "w"), indent=1, default=float)
print(json.dumps({k: v for k, v in out.items() if k != "scar_frame"}, indent=1, default=float))
for B in ("B10", "B2"):
    s = out["scar_frame"][B]
    print("\n", B, "means", {k: round(v, 4) for k, v in s["means"].items()})
    for k in ("blk_minus_loso", "loso_minus_foreign", "blk_minus_foreign", "regionwide_minus_blkscar"):
        print("  ", k, {kk: (np.round(vv, 4) if not isinstance(vv, int) else vv) for kk, vv in s[k].items()})
