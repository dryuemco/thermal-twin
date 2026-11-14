"""build_values_figures.py: numbers and figures of the EMS manuscript, read from the analysis outputs.

Every number quoted in manuscript.tex is a macro from values.tex, which this script writes from the JSON and
CSV files in D:/ThermalTwin/scaleup/analysis (scripts/scaleup in the analysis repository, plan commit
067e676). Nothing in the text is typed by hand. Figures go to figures/ as PDF.

Run:  <venv-step10>/python build_values_figures.py
"""
import json
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

AN = Path("D:/ThermalTwin/scaleup/analysis")
HERE = Path(__file__).resolve().parent
FIG = HERE / "figures"
FIG.mkdir(exist_ok=True)
plt.rcParams.update({"font.size": 8, "axes.titlesize": 8, "axes.labelsize": 8, "legend.fontsize": 7,
                     "xtick.labelsize": 7, "ytick.labelsize": 7, "pdf.fonttype": 42})
# Okabe-Ito palette, one colour per model across all figures
COL = {"null": "#000000", "rf_thermal": "#0072B2", "hgb_thermal": "#009E73", "rf_baseline": "#E69F00"}
MRK = {"null": "s", "rf_thermal": "o", "hgb_thermal": "^", "rf_baseline": "D"}
LAB = {"null": "Geographic null model", "rf_thermal": "Random forest, thermal set",
       "hgb_thermal": "Gradient boosting, thermal set", "rf_baseline": "Random forest, baseline set"}

V = {}


def put(name, x, nd=3):
    V[name] = f"{x:.{nd}f}" if isinstance(x, float) else str(x)


def ci(name, d, nd=3):
    put(name, d["mean"], nd)
    put(name + "Lo", d["lo"], nd)
    put(name + "Hi", d["hi"], nd)


def load(n):
    return json.loads((AN / n).read_text(encoding="utf-8"))


# ---------------------------------------------------------------- claims 1 and 2
S12 = load("claims12_summary.json")
P = S12["primary"]
put("nFires", S12["primary_fires"])
put("gateBand", f"{S12['gates']['gate1_band_max_diff']:.4f}")
put("gateTransfer", f"{S12['gates']['gate2_transfer_max_diff']:.4f}")
for k, tag in ((10, "Five"), (20, "Ten"), (40, "Twenty")):
    B = P[f"blocks_{k}_cells"]
    for m, mt in (("null", "Null"), ("rf_thermal", "Rf"), ("rf_baseline", "Base"), ("hgb_thermal", "Hgb")):
        ci(f"auc{mt}{tag}", B[f"auc_{m}"])
        ci(f"ap{mt}{tag}", B[f"ap_{m}"])
    put(f"nullWins{tag}", B["null_beats_rf_thermal"])
    put(f"nullWinsHgb{tag}", B["null_beats_hgb_thermal"])
    ci(f"pwdNull{tag}", B["pwd_auc_null"])
    ci(f"cauc{tag}", B["cauc_rf_thermal"])
    ci(f"caucBase{tag}", B["cauc_rf_baseline"])
    ci(f"caucHgb{tag}", B["cauc_hgb_thermal"])
for b, tag in (("1_km", "One"), ("2_km", "Two"), ("5_km", "Five"), ("10_km", "Ten")):
    ci(f"bufRf{tag}", P["buffered"][b]["auc_rf_thermal"])
    ci(f"bufNull{tag}", P["buffered"][b]["auc_null"])
    put(f"bufSkip{tag}", P["buffered"][b]["folds_skipped_total"])
    put(f"bufWins{tag}", P["buffered"][b]["null_beats_rf"])
names = {"0-0.5": "A", "0.5-1": "B", "1-2": "C", "2-5": "D", "5-10": "E", "10-inf": "F"}
for b, t in names.items():
    ci(f"band{t}Rf", P["bands"][b]["auc_rf_thermal"])
    ci(f"band{t}Null", P["bands"][b]["auc_null"])
    put(f"band{t}RfWins", P["bands"][b]["rf_beats_null"])
    ci(f"band{t}Prev", P["bands"][b]["prevalence"])
ci("rise", P["rise"]["rf_thermal"])
put("riseFires", P["rise"]["fires_positive_rise_rf"])
put("riseFiresHgb", P["rise"]["fires_positive_rise_hgb"])
ci("envQone", P["environmental_quintiles"]["1"]["auc_rf_thermal"])
ci("envQfive", P["environmental_quintiles"]["5"]["auc_rf_thermal"])
ci("envRise", P["env_rise_rf_thermal"])
put("caucGain", P["blocks_10_cells"]["cauc_rf_thermal"]["mean"] - P["blocks_10_cells"]["cauc_rf_baseline"]["mean"], 2)
put("caucGap", P["blocks_10_cells"]["auc_rf_thermal"]["mean"] - P["blocks_10_cells"]["cauc_rf_thermal"]["mean"], 2)
put("bufFolds", 5 * S12["primary_fires"])
_fr = pd.read_csv(AN / "claims12_per_fire.csv")
_fr = _fr[_fr.fire != "montiferru_2021"]
put("cellsMin", f"{int(_fr.cells.min()):,}"), put("cellsMax", f"{int(_fr.cells.max()):,}")
put("burnedMin", f"{int(_fr.burned.min()):,}"), put("burnedMax", f"{int(_fr.burned.max()):,}")
E = S12["exclusion_sensitivity"]
put("exclCount", S12["primary_fires"] - E["fires"])
put("exclFires", E["fires"])
put("exclNullWins", E["blocks_10_cells"]["null_beats_rf_thermal"])
ci("exclRise", E["rise"]["rf_thermal"])

# ---------------------------------------------------------------- claim 3
S3 = load("claim3_summary.json")
le = S3["label_error_027"]
for b, t in names.items():
    ci(f"lerr{t}", {k: 100 * v for k, v in le[b]["unburned_share_above_0.5"].items() if k in ("mean", "lo", "hi")}, 1)
put("lerrTenFarBand", f"{100 * S3['label_error_010']['10-inf']['unburned_share_above_0.5']['mean']:.1f}")
for vname, tag in (("b_drop_ambiguous", "Drop"), ("c_relabel", "Relabel"), ("a_s2_label", "Stwo")):
    v = S3[f"variant_{vname}_027"]["rf_thermal"]
    ci(f"near{tag}", v["near_band_auc_variant"])
    ci(f"closed{tag}", {k: 100 * x for k, x in v["share_of_gap_closed"].items() if k in ("mean", "lo", "hi")}, 0)
put("nearMcd", S3["variant_b_drop_ambiguous_027"]["rf_thermal"]["near_band_auc_mcd64a1"]["mean"])
put("firecciFires", S3["firecci_fires"])

# ---------------------------------------------------------------- claim 6
S6 = load("claim6_summary.json")
put("aggAgree", 100 * S6["aggregation_check"]["agreement"]["mean"], 1)
put("aggKappa", S6["aggregation_check"]["kappa"]["mean"], 2)
A6 = S6["all_2001_2023"]
ci("myNull", A6["auc_null_b10"])
ci("myRf", A6["auc_rf_thermal_b10"])
ci("myNullTen", A6["auc_null_b20"])
ci("myRfTen", A6["auc_rf_thermal_b20"])
put("myWins", A6["null_beats_rf_b10"])
put("myWinsTen", A6["null_beats_rf_b20"])
ci("myCauc", A6["cauc_rf_thermal_b10"])
ci("myRise", A6["rise_rf_thermal"])
put("myRiseFires", A6["fires_positive_rise"])
ci("myBurned", {k: 100 * v for k, v in A6["burned_share"].items() if k in ("mean", "lo", "hi")}, 1)
H6 = S6["history_before_fire"]
put("histWins", H6["null_beats_rf_b10"])
ci("histNull", H6["auc_null_b10"])
ci("histRf", H6["auc_rf_thermal_b10"])

# ---------------------------------------------------------------- claim 7
T7 = pd.read_csv(AN / "claim7_open_data.csv")
bc = T7[T7.dataset == "bc"]
put("bcNull", float(bc.null_auc.mean()))
put("bcNullMin", float(bc.null_auc.min()))
put("bcNullMax", float(bc.null_auc.max()))
put("bcRf", float(bc.rf_auc_same_folds.mean()))
ko = T7[T7.dataset == "korea"].iloc[0]
put("koNull", float(ko.null_auc)), put("koRf", float(ko.reproduced_rf_auc)), put("koRep", float(ko.reported_auc))
al = T7[T7.dataset == "alberta"]
put("alTempNull", float(al.iloc[0].null_auc)), put("alTempRep", float(al.iloc[0].reported_auc))
put("alTempNullSeventeen", float(al.iloc[1].null_auc))
put("alBlockNull", float(al.iloc[2].null_auc)), put("alBlockRep", float(al.iloc[2].reported_auc))
it = T7[T7.dataset == "italy"].iloc[0]
put("itNull", float(it.null_auc)), put("itRf", float(it.rf_auc_same_folds)), put("itRep", float(it.reported_auc))
put("itFolds", int(str(it.protocol).split("(")[1].split()[0]))
me = T7[T7.dataset == "mesogeos"].iloc[0]
put("meNull", float(me.null_auc)), put("meNullPr", float(me.null_auprc)), put("mePrev", float(me.test_prevalence))

# ---------------------------------------------------------------- claim 5
S5 = load("claim5_summary.json")
L, Q = S5["landsat_morning"], S5["aqua_afternoon"]
ci("lstAuc", L["auc"]); put("lstCool", L["cooler_burned"]); put("lstCoolCi", L["cooler_interval_below_0.5"])
put("lstHotCi", L["hotter_interval_above_0.5"])
ci("lstAucCtl", L["given_elev_ndvi_tree_aspect"]["auc"]); put("lstCoolCtl", L["given_elev_ndvi_tree_aspect"]["cooler_burned"])
ci("aquaAuc", Q["auc"]); put("aquaCool", Q["cooler_burned"])
ci("aquaAucCtl", Q["given_elev_ndvi_tree_aspect"]["auc"]); put("aquaCoolCtl", Q["given_elev_ndvi_tree_aspect"]["cooler_burned"])
ci("lstCorr", S5["corr_morning_afternoon"], 2)

# ---------------------------------------------------------------- claim 4 (when available)
if (AN / "claim4_summary.json").exists():
    S4 = load("claim4_summary.json")
    put("trDirections", S4["directions"])
    for m, t in (("raw", "Raw"), ("raw_near", "Near"), ("raw_far", "Far"), ("baseline", "Base"), ("zscore", "Z"), ("minmax", "Minmax")):
        ci(f"tr{t}", S4[m])
    put("trAboveSix", f"{100 * S4['share_raw_above_0.6']:.1f}")
    put("trBelowHalf", f"{100 * S4['share_raw_below_0.5']:.1f}")
    for m, t in (("distance_km", "Dist"), ("same_year", "Year"), ("domain_auc", "Dom"), ("mean_shift", "Shift")):
        r = S4["similarity_spearman"][m]
        put(f"rho{t}", r["rho"], 2), put(f"rho{t}Lo", r["lo"], 2), put(f"rho{t}Hi", r["hi"], 2)
    for m, t in (("pooled_raw", "PoolRaw"), ("pooled_z", "PoolZ"), ("pooled_minmax", "PoolMinmax"),
                 ("pooled_z_near", "PoolZNear"), ("pooled_z_far", "PoolZFar"), ("single_mean", "Single")):
        ci(f"tr{t}", S4["pooled"][m])
    cv = S4["curve"]
    ks = sorted(int(k) for k in cv)
    put("curveFirst", cv[str(ks[0])]["mean"]), put("curveTen", cv["10"]["mean"]), put("curveLast", cv[str(ks[-1])]["mean"])
    put("curveLastK", ks[-1])

(HERE / "values.tex").write_text("% written by build_values_figures.py, do not edit\n" +
                                 "".join(f"\\newcommand{{\\v{k}}}{{{v}}}\n" for k, v in sorted(V.items())), encoding="utf-8")
print(len(V), "values")

# ---------------------------------------------------------------- figures
FR = pd.read_csv(AN / "claims12_per_fire.csv")
FR = FR[FR.fire != "montiferru_2021"]
BR = pd.read_csv(AN / "claims12_bands.csv")
BR = BR[BR.fire != "montiferru_2021"]

# Fig. 1: per-fire AUC of the null model and the thermal RF at three block sizes
fig, axs = plt.subplots(1, 3, figsize=(7.2, 3.0), sharey=True)
for ax, k, title in zip(axs, (10, 20, 40), ("5 km blocks", "10 km blocks", "20 km blocks")):
    g = FR.dropna(subset=[f"auc_null_b{k}"]).sort_values(f"auc_rf_thermal_b{k}").reset_index(drop=True)
    yy = np.arange(len(g))
    ax.hlines(yy, g[f"auc_rf_thermal_b{k}"], g[f"auc_null_b{k}"], color="#bbbbbb", lw=0.8)
    for m in ("rf_thermal", "null"):
        ax.plot(g[f"auc_{m}_b{k}"], yy, MRK[m], color=COL[m], ms=3.5, label=LAB[m])
    ax.set_title(title)
    ax.set_xlabel("ROC AUC")
    ax.set_xlim(0.45, 1.0)
    ax.axvline(0.5, color="#888888", lw=0.5, ls=":")
    ax.set_yticks([])
axs[0].set_ylabel("Fires, ordered by random-forest AUC")
fig.legend(*axs[0].get_legend_handles_labels(), loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, -0.02))
fig.tight_layout(rect=(0, 0.07, 1, 1))
fig.savefig(FIG / "Figure_1.pdf")
plt.close(fig)

# Fig. 2: distance bands, mean over fires with fire-bootstrap interval, plus per-fire RF lines
order = list(names)
xs = np.arange(len(order))
fig, ax = plt.subplots(figsize=(3.6, 3.0))
for f, g in BR.groupby("fire"):
    g = g.set_index("band").reindex(order)
    ax.plot(xs, g.auc_rf_thermal, color=COL["rf_thermal"], alpha=0.12, lw=0.6)
off = {"null": -0.12, "rf_baseline": -0.04, "rf_thermal": 0.04, "hgb_thermal": 0.12}
for m in ("null", "rf_baseline", "rf_thermal", "hgb_thermal"):
    mean = [P["bands"][b][f"auc_{m}"]["mean"] for b in order]
    lo = [P["bands"][b][f"auc_{m}"]["lo"] for b in order]
    hi = [P["bands"][b][f"auc_{m}"]["hi"] for b in order]
    ax.errorbar(xs + off[m], mean, yerr=[np.subtract(mean, lo), np.subtract(hi, mean)], color=COL[m], marker=MRK[m],
                ms=3.5, lw=1, capsize=1.5, label=LAB[m])
ax.set_xticks(xs, ["0-0.5", "0.5-1", "1-2", "2-5", "5-10", ">10"])
ax.set_xlabel("Distance of unburned cells from the burned area (km)")
ax.set_ylabel("ROC AUC")
ax.set_ylim(0.45, 1.01)
ax.legend(frameon=False, loc="lower right")
fig.tight_layout()
fig.savefig(FIG / "Figure_2.pdf")
plt.close(fig)

# Fig. 3: label check, share of MCD64A1-unburned cells that Sentinel-2 maps as at least half burned, by band
fig, ax = plt.subplots(figsize=(3.6, 2.6))
for th, mk, lab in (("027", "o", "dNBR >= 0.27"), ("010", "s", "dNBR >= 0.10")):
    d = S3[f"label_error_{th}"]
    mean = [100 * d[b]["unburned_share_above_0.5"]["mean"] for b in order]
    lo = [100 * d[b]["unburned_share_above_0.5"]["lo"] for b in order]
    hi = [100 * d[b]["unburned_share_above_0.5"]["hi"] for b in order]
    ax.errorbar(xs, mean, yerr=[np.subtract(mean, lo), np.subtract(hi, mean)], marker=mk, ms=3.5, lw=1, capsize=1.5,
                color="#0072B2" if th == "027" else "#D55E00", label=lab)
ax.set_xticks(xs, ["0-0.5", "0.5-1", "1-2", "2-5", "5-10", ">10"])
ax.set_xlabel("Distance of unburned cells from the burned area (km)")
ax.set_ylabel("Unburned cells mapped burned by Sentinel-2 (%)")
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(FIG / "Figure_3.pdf")
plt.close(fig)

# Fig. 4: open datasets, reported AUC and the null model's AUC under the authors' protocol
rows = [("Alberta, temporal test", float(al.iloc[0].reported_auc), float(al.iloc[0].null_auc)),
        ("British Columbia, 50 km blocks", 0.92, float(bc.null_auc.mean())),
        ("Korea, random 70/30", float(ko.reported_auc), float(ko.null_auc)),
        ("Alberta, 100 km blocks", float(al.iloc[2].reported_auc), float(al.iloc[2].null_auc)),
        ("Italy, regional blocks", float(it.reported_auc), float(it.null_auc))]
fig, ax = plt.subplots(figsize=(4.4, 2.8))
yy = np.arange(len(rows))[::-1]
for y, (lab, rep, nul) in zip(yy, rows):
    ax.hlines(y, min(rep, nul), max(rep, nul), color="#bbbbbb", lw=0.8)
ax.plot([r[1] for r in rows], yy, "o", color="#CC79A7", ms=4, label="Published model")
ax.plot([r[2] for r in rows], yy, MRK["null"], color=COL["null"], ms=4, label=LAB["null"])
ax.set_yticks(yy, [r[0] for r in rows])
ax.set_xlabel("ROC AUC on the authors' test data")
ax.set_xlim(0.45, 1.0)
ax.axvline(0.5, color="#888888", lw=0.5, ls=":")
fig.legend(*ax.get_legend_handles_labels(), frameon=False, loc="lower center", ncol=2, bbox_to_anchor=(0.5, 0.0))
fig.tight_layout(rect=(0, 0.08, 1, 1))
fig.savefig(FIG / "Figure_4.pdf")
plt.close(fig)

# Fig. 5: transfer learning curve (when available)
if (AN / "claim4_curve.csv").exists():
    Cv = pd.read_csv(AN / "claim4_curve.csv")
    S4 = load("claim4_summary.json")
    ks = sorted(int(k) for k in S4["curve"])
    mean = [S4["curve"][str(k)]["mean"] for k in ks]
    lo = [S4["curve"][str(k)]["lo"] for k in ks]
    hi = [S4["curve"][str(k)]["hi"] for k in ks]
    fig, ax = plt.subplots(figsize=(3.6, 2.6))
    ax.errorbar(ks, mean, yerr=[np.subtract(mean, lo), np.subtract(hi, mean)], marker="o", color=COL["rf_thermal"], ms=3.5,
                lw=1, capsize=1.5, label="Pooled random forest, z-scored predictors")
    ax.axhline(S4["raw"]["mean"], color="#888888", ls="--", lw=0.8, label="Single source fire, raw predictors")
    ax.axhline(0.5, color="#888888", ls=":", lw=0.5)
    ax.set_xticks(ks)
    ax.set_xlabel("Number of source fires")
    ax.set_ylabel("ROC AUC on the held-out fire")
    ax.set_ylim(0.45, 0.75)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(FIG / "Figure_5.pdf")
    plt.close(fig)
print("figures written")
