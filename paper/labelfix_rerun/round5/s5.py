"""S5: paired thermal-minus-baseline transfer contrast (Table R6) for the 8 Manavgat directions, with 2-cell
(step9c, R6) and 10-cell (~5 km) paired delta CIs, and the 20-direction verdict summary; frozen (control arm,
= published to rounding) vs corrected (official). Inputs: out_{control,official}/baseline_vs_thermal_transfer.json
and transfer_ci_blocksize.json produced by the unchanged round-3 aggregators on the two overlays."""
import json
from pathlib import Path
import pandas as pd
R5 = Path(r"C:\Users\CORSAIR\projects\thermal-twin\rerun_labelfix\_round5")
S = {"manavgat_2021": "Man", "bejis_2022": "Bej", "mugla_2021": "Mug", "evia_2021_extended": "Evia", "montiferru_2021": "Mont"}
out = {}
for arm in ("control", "official"):
    r6 = pd.DataFrame(json.load(open(R5 / f"out_{arm}/baseline_vs_thermal_transfer.json"))["per_direction"])
    r6["d2_lo"], r6["d2_hi"] = r6.delta_ci.str[0], r6.delta_ci.str[1]
    t = pd.DataFrame(json.load(open(R5 / f"out_{arm}/transfer_ci_blocksize.json")))[["direction", "point_delta", "d10d_lo", "d10d_hi", "dv10"]]
    out[arm] = r6[["direction", "baseline_roc", "thermal_roc", "delta_roc", "d2_lo", "d2_hi", "delta_interpretation"]].merge(t, on="direction")
arms = out["control"].merge(out["official"], on="direction", suffixes=("_frozen", "_corrected"))
arms["dir"] = arms.direction.map(lambda d: "→".join(S[x] for x in d.split("_to_")))
arms.to_csv(R5 / "s5_paired_delta_20.csv", index=False)
man = arms[arms.direction.str.contains("manavgat")]
lines = ["| Direction | Δ frozen [2-cell] | Δ corrected [2-cell] | 2-cell verdict | Δ corrected [10-cell] | 10-cell verdict |", "|---|---|---|---|---|---|"]
for _, r in man.iterrows():
    lines.append(f"| {r.dir} | {r.delta_roc_frozen:+.4f} [{r.d2_lo_frozen:+.4f}, {r.d2_hi_frozen:+.4f}] | {r.delta_roc_corrected:+.4f} [{r.d2_lo_corrected:+.4f}, {r.d2_hi_corrected:+.4f}] | "
                 f"{r.delta_interpretation_frozen} → {r.delta_interpretation_corrected} | {r.point_delta_corrected:+.4f} [{r.d10d_lo_corrected:+.4f}, {r.d10d_hi_corrected:+.4f}] | {r.dv10_frozen} → {r.dv10_corrected} |")
summ = {}
for arm in ("frozen", "corrected"):
    v2 = arms[f"delta_interpretation_{arm}"].map(lambda s: "positive" if s.startswith("positive") else "negative" if s.startswith("negative") else "uncertain")
    v10 = arms[f"dv10_{arm}"]
    summ[arm] = {"mean_delta": round(float(arms[f"delta_roc_{arm}"].mean()), 4),
                 "2cell_pos_neg_unc": [int((v2 == k).sum()) for k in ("positive", "negative", "uncertain")],
                 "10cell_verdicts": v10.value_counts().to_dict(),
                 "delta_range": [round(float(arms[f"delta_roc_{arm}"].min()), 4), round(float(arms[f"delta_roc_{arm}"].max()), 4)],
                 "n_positive_point": int((arms[f"delta_roc_{arm}"] > 0).sum())}
json.dump(summ, open(R5 / "s5_summary.json", "w"), indent=1)
(R5 / "s5_manavgat_8.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines)); print(json.dumps(summ, indent=1))
