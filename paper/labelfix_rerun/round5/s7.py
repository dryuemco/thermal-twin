"""S7: contrast pair (Man-Mug vs Bej-Mont) from the OFFICIAL outputs: four transfer AUCs with 2-cell (step9c) and
10-cell CIs, niche-overlap ranks over the 10 pairs on five measures, sign agreement. Frozen = control arm (identical
to the 09-19 frozen arm). Inputs: out_{official,control}/{figure_contrast_pairs,transfer_ci_blocksize,niche_overlap_transfer}.json"""
import json
from pathlib import Path
import pandas as pd
R5 = Path(__file__).parent
S = {"manavgat_2021": "Man", "bejis_2022": "Bej", "mugla_2021": "Mug", "evia_2021_extended": "Evia", "montiferru_2021": "Mont"}
FOUR = ["manavgat_2021_to_mugla_2021", "mugla_2021_to_manavgat_2021", "bejis_2022_to_montiferru_2021", "montiferru_2021_to_bejis_2022"]
MEAS = ["schoener_d_mean1d", "warren_i_mean1d", "schoener_d_pca2d", "warren_i_pca2d", "mahalanobis_burned"]
res = {}
for arm in ("control", "official"):
    t = {r["direction"]: r for r in json.load(open(R5 / f"out_{arm}/transfer_ci_blocksize.json"))}
    fc = json.load(open(R5 / f"out_{arm}/figure_contrast_pairs.json"))
    auc = {d: {"auc": t[d]["point"], "ci2": [t[d]["b2_lo"], t[d]["b2_hi"]], "ci10": [t[d]["b10_lo"], t[d]["b10_hi"]], "v2": t[d]["v2"], "v10": t[d]["v10"]} for d in FOUR}
    npairs = pd.DataFrame(json.load(open(R5 / f"out_{arm}/niche_overlap_transfer.json"))["per_pair"])
    npairs["pair"] = npairs.region_a.map(S) + "-" + npairs.region_b.map(S)
    for k in MEAS:
        npairs["rank_" + k] = npairs[k].rank(ascending=("mahal" in k)).astype(int)
    ranks = npairs.set_index("pair")[["rank_" + k for k in MEAS] + MEAS].loc[["Man-Mug", "Bej-Mont"]].to_dict("index")
    cond = {p["pair"]: {"agree_count_9": p["conditional"]["agree_count_9"], "cosine_9": round(p["conditional"]["cosine_9"], 3)} for p in fc["pairs"]}
    res[arm] = {"transfer": auc, "niche_ranks_of_10": ranks, "sign_agreement": cond}
json.dump(res, open(R5 / "s7_contrast_pair.json", "w"), indent=1, default=float)
for arm in ("control", "official"):
    print("==", "FROZEN" if arm == "control" else "CORRECTED (official)")
    for d, v in res[arm]["transfer"].items():
        n = "->".join(S[x] for x in d.split("_to_"))
        print(f"  {n:9s} {v['auc']:.3f}  2-cell [{v['ci2'][0]:.3f}, {v['ci2'][1]:.3f}] {v['v2']:9s}  10-cell [{v['ci10'][0]:.3f}, {v['ci10'][1]:.3f}] {v['v10']}")
    for p, r in res[arm]["niche_ranks_of_10"].items():
        print("  niche ranks", p, [r["rank_" + k] for k in MEAS])
    print("  sign agreement", res[arm]["sign_agreement"])
