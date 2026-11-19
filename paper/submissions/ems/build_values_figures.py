"""build_values_figures.py: numbers and figures of the EMS manuscript, read from the analysis outputs.

Every result of this study quoted in manuscript.tex is a macro from values.tex, which this script writes from
the JSON and CSV files the analysis scripts produce (scripts/scaleup on branch scaleup-31fires of the analysis
repository; plan docs/scaleup/ANALYSIS_PLAN.md). Method settings, numbers quoted from the literature and the
highlights are written in the text. Figures go to figures/ as PDF.

Inputs (both required): the analysis output folder, given by the environment variable THERMAL_TWIN_ANALYSIS,
and a checkout of branch scaleup-31fires for the fire windows, given by THERMAL_TWIN_REPO. Statistics computed
here, not in the analysis scripts, are also written to manuscript_statistics.json.

Run:  python build_values_figures.py
"""
import json
import math
import os
import sys
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

AN = Path(os.environ["THERMAL_TWIN_ANALYSIS"])
REPO = Path(os.environ["THERMAL_TWIN_REPO"])
MS = {}      # statistics computed here (not in the analysis scripts), written to manuscript_statistics.json
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


def boot(v, B=2000, seed=42):
    """Mean over fires with a percentile interval from B bootstrap resamples of fires."""
    v = np.asarray([x for x in v if np.isfinite(x)], float)
    rng = np.random.default_rng(seed)
    bs = [v[rng.integers(0, len(v), len(v))].mean() for _ in range(B)]
    return {"mean": float(v.mean()), "lo": float(np.percentile(bs, 2.5)), "hi": float(np.percentile(bs, 97.5))}


def node_boot(T, col, B=2000, seed=42):
    """Mean over source-target directions with fires as the resampling unit: in each resample a direction
    is counted once per copy of its source fire and once per copy of its target fire."""
    ids = sorted(set(T.source) | set(T.target))
    pos = {f: i for i, f in enumerate(ids)}
    s_i, t_i = T.source.map(pos).to_numpy(), T.target.map(pos).to_numpy()
    x = T[col].to_numpy(float)
    ok = np.isfinite(x)
    rng = np.random.default_rng(seed)
    bs = []
    for _ in range(B):
        c = np.bincount(rng.integers(0, len(ids), len(ids)), minlength=len(ids))
        w = c[s_i] * c[t_i] * ok
        if w.sum():
            bs.append(float((w * np.nan_to_num(x)).sum() / w.sum()))
    return {"mean": float(x[ok].mean()), "lo": float(np.percentile(bs, 2.5)), "hi": float(np.percentile(bs, 97.5))}


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
ci("pwdRfFive", boot(_fr.pwd_auc_rf_thermal_b10))
put("pwdKeptFive", 100 * _fr.pwd_share_pos_b10.mean(), 0)
ci("caucDiff", boot(_fr.cauc_rf_thermal_b10 - _fr.cauc_rf_baseline_b10))
put("prevMean", 100 * _fr.prevalence.mean(), 1)
put("prevMin", 100 * _fr.prevalence.min(), 1), put("prevMax", 100 * _fr.prevalence.max(), 1)
MS["paired_pairs_rf_auc_5km"] = boot(_fr.pwd_auc_rf_thermal_b10)
MS["cauc_thermal_minus_baseline_5km"] = boot(_fr.cauc_rf_thermal_b10 - _fr.cauc_rf_baseline_b10)
# buffered validation coverage, from the versioned analysis output (never from the prediction cache)
BC_ = load("buffer_coverage.json")
for b, tag in ((1, "One"), (2, "Two"), (5, "Five"), (10, "Ten")):
    v = BC_["buffers"][f"{b}_km"]
    assert set(v["per_fire"]) == set(_fr.fire), "buffer coverage does not cover the primary fires"
    assert all(v["per_fire"][r.fire]["cells"] == r.cells for r in _fr.itertuples()), "population sizes differ"
    put(f"bufCellsPct{tag}", 100 * v["cells_scored"] / v["cells_total"], 0), put(f"bufFires{tag}", v["fires_with_scored_cells"])
# robustness of claim 1 (amendment 4)
RB1 = load("claim1_robustness_summary.json")
# combined model: the version whose training distance mimics the test geometry (claim1_combined.py)
CB = load("claim1_combined_summary.json")
ci("combAuc", CB["auc_combined"]), put("combWins", CB["combined_beats_null"])
ci("combNear", CB["near_combined"]), ci("combNearNull", CB["near_null"]), ci("combNearRf", CB["near_rf"])
put("combNearWins", CB["near_combined_beats_null"])
ci("combMinusNull", CB["combined_minus_null"]), ci("combNearMinusNull", CB["near_combined_minus_null"])
ci("naiveAuc", RB1["combined"]["auc_combined"])
ci("fwNull", RB1["foldwise"]["null"]), ci("fwRf", RB1["foldwise"]["rf"]), put("fwWins", RB1["foldwise"]["null_beats_rf"])
_dw = [int(v["null_beats_rf"].split()[0]) for v in RB1["designs"].values()]
put("designMinWins", min(_dw)), put("designN", len(_dw))
F20 = RB1["folds20"]
_f20 = pd.read_csv(AN / "claim1_folds20.csv")
put("ftFolds", len(_f20)), put("ftOneBlock", int((_f20.blocks == 1).sum())), put("ftNoBurn", int((_f20.burned == 0).sum()))
put("ftMinBlocks", F20["min_blocks"]), put("ftMinBurned", F20["min_burned"]), put("ftMinUnburned", F20["min_unburned"])
_mt = RB1["matching"]
_cm = [v["cauc"]["mean"] for v in _mt.values()]
put("caucSensMin", min(_cm)), put("caucSensMax", max(_cm))
_ks = [v["kept_share"]["mean"] for v in _mt.values()]
put("keptSensMin", 100 * min(_ks), 0), put("keptSensMax", 100 * max(_ks), 0)
ci("distKept", RB1["matching_distances_main"]["kept_burned_median_km"], 2)
ci("distDropped", RB1["matching_distances_main"]["dropped_burned_median_km"], 2)
# windows: rule for the 26 added fires, the earlier study's own windows for the five earlier regions
sys.path.insert(0, str(REPO))
from datetime import date  # noqa: E402
from core import regions  # noqa: E402


def days(a, b):
    return (date.fromisoformat(b) - date.fromisoformat(a)).days + 1


_earlier = ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended", "montiferru_2021_fullwindow"]
_added = [i for i in _fr.fire if i not in _earlier]
_pd = [days(regions.EXPERIMENTS[i]["predictor_start_date"], regions.EXPERIMENTS[i]["predictor_end_date"]) for i in _added]
_ld = [days(regions.EXPERIMENTS[i]["label_start_date"], regions.EXPERIMENTS[i]["label_end_date"]) for i in _added]
assert len(set(_pd)) == 1 and len(set(_ld)) == 1, (set(_pd), set(_ld))
put("predDays", _pd[0]), put("labelDays", _ld[0])
_pe = [days(regions.EXPERIMENTS[i]["predictor_start_date"], regions.EXPERIMENTS[i]["predictor_end_date"]) for i in _earlier]
_le = [days(regions.EXPERIMENTS[i]["label_start_date"], regions.EXPERIMENTS[i]["label_end_date"]) for i in _earlier]
put("predDaysEarlyMin", min(_pe)), put("predDaysEarlyMax", max(_pe))
put("labelDaysEarlyMin", min(_le)), put("labelDaysEarlyMax", max(_le))
put("nAdded", len(_added))
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
for b, t in names.items():
    ci(f"lerrLoose{t}", {k: 100 * v for k, v in S3["label_error_010"][b]["unburned_share_above_0.5"].items() if k in ("mean", "lo", "hi")}, 1)
put("lerrTenFarBand", f"{100 * S3['label_error_010']['10-inf']['unburned_share_above_0.5']['mean']:.1f}")
for th, ttag in (("027", ""), ("010", "Loose")):
    for vname, tag in (("b_drop_ambiguous", "Drop"), ("c_relabel", "Relabel"), ("a_s2_label", "Stwo")):
        v = S3[f"variant_{vname}_{th}"]["rf_thermal"]
        ci(f"near{tag}{ttag}", v["near_band_auc_variant"])
        ci(f"closed{tag}{ttag}", {k: 100 * x for k, x in v["share_of_gap_closed"].items() if k in ("mean", "lo", "hi")}, 0)
put("nearMcd", S3["variant_b_drop_ambiguous_027"]["rf_thermal"]["near_band_auc_mcd64a1"]["mean"])
put("farMcd", S3["variant_b_drop_ambiguous_027"]["rf_thermal"]["far_band_auc_mcd64a1"]["mean"])
put("firecciFires", S3["firecci_fires"])
put("sTwoExcluded", S3["cells_excluded"]), put("sTwoUsed", f"{S3['cells_used']:,}")
# near and farthest band and their rise under every label variant (rf_thermal, fixed predictions)
RB = pd.read_csv(AN / "claim3_rescored_bands.csv", dtype={"threshold": str})
RB["threshold"] = RB.threshold.str.zfill(3)
RB = RB[RB.model == "rf_thermal"]
_bandcols = list(names)
MS["label_variants"] = {}
_outer = _bandcols[1:]          # the farthest band is chosen among the bands beyond 0.5 km
for (th, vn), g in RB.groupby(["threshold", "variant"]):
    near = g["0-0.5"].to_numpy(float)
    far_band = g[_outer].apply(lambda r: r.dropna().index[-1] if r.notna().any() else None, axis=1)
    far = np.array([g.loc[i, b] if b is not None else np.nan for i, b in far_band.items()], float)
    both = np.isfinite(near) & np.isfinite(far)            # every mean below is over the same fires
    rise = far - near
    tag = {"mcd64a1": "Mcd", "b_drop_ambiguous": "Drop", "c_relabel": "Relabel", "a_s2_label": "Stwo"}[vn] + ("" if th == "027" else "Loose")
    st = {"fires": int(both.sum()), "fires_without_near_band": int((~np.isfinite(near)).sum()),
          "fires_without_far_band": int((~np.isfinite(far)).sum()),
          "far_band_used": {str(k): int(v) for k, v in far_band[both].value_counts().items()},
          "near": boot(near[both]), "far": boot(far[both]), "rise": boot(rise[both]),
          "fires_positive_rise": int((rise[both] > 0).sum())}
    put(f"vnoNear{tag}", st["fires_without_near_band"])
    MS["label_variants"][f"{vn}_{th}"] = st
    ci(f"vfar{tag}", st["far"]), ci(f"vrise{tag}", st["rise"]), put(f"vrisePos{tag}", f"{st['fires_positive_rise']} of {st['fires']}"), put(f"vriseN{tag}", st["fires"])

# Sentinel-2 check with bands recomputed from each variant's own burned cells (amendment 4)
G3 = load("claim3_geometry_summary.json")
for vn, vt in (("a_s2_label", "Stwo"), ("c_relabel", "Relabel")):
    for th, tt in (("027", ""), ("010", "Loose")):
        v = G3[f"{vn}_{th}"]
        ci(f"geo{vt}{tt}Rise", v["recomputed_rise"]), put(f"geo{vt}{tt}Pos", v["recomputed_rise_positive"])
        ci(f"geo{vt}{tt}Near", v["recomputed_near"]), ci(f"geo{vt}{tt}Far", v["recomputed_far"])
        ci(f"fix{vt}{tt}DNear", v["fixed_minus_ref_near"]), ci(f"fix{vt}{tt}DFar", v["fixed_minus_ref_far"])

# ---------------------------------------------------------------- claim 6
S6 = load("claim6_summary.json")
put("histSkipped", ", ".join(s["fire"].replace("_", "\\_") for s in S6["skipped"]))
put("histSkippedBurned", ", ".join(str(s["burned"]) for s in S6["skipped"]))
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
put("meRepPr", str(me.reported_auprc).replace("-", "--"))
put("bcRep", float(bc.reported_auc.iloc[0]), 2)
ACI = load("claim7_alberta_ci.json")
ci("alNullCi", {"mean": ACI["null_auc"], "lo": ACI["null_lo"], "hi": ACI["null_hi"]})
_best = max(ACI["published"].items(), key=lambda kv: kv[1]["auc"])
put("alBestName", _best[0]), ci("alBestCi", {"mean": _best[1]["auc"], "lo": _best[1]["lo"], "hi": _best[1]["hi"]})
put("alTempRep", _best[1]["auc"])      # the package's own bootstrap table (Table S3), the source with intervals
put("alDiff", ACI["null_auc"] - _best[1]["auc"])

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
    T4 = pd.read_csv(AN / "claim4_transfer.csv")
    put("trDirections", S4["directions"])
    for m, t in (("raw", "Raw"), ("raw_near", "Near"), ("raw_far", "Far"), ("baseline", "Base"), ("zscore", "Z"), ("minmax", "Minmax")):
        ci(f"tr{t}", node_boot(T4, m))       # amendment 3: fires as the resampling unit
    T4["thermal_minus_baseline"] = T4.raw - T4.baseline
    ci("trThermMinusBase", node_boot(T4, "thermal_minus_baseline"))
    # these fire-level intervals replace the direction-level ones in claim4_summary.json
    MS["transfer_fire_level"] = {m: node_boot(T4, m) for m in ("raw", "raw_near", "raw_far", "baseline", "zscore", "minmax",
                                                              "thermal_minus_baseline")}
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

# ---------------------------------------------------------------- route B (plan amendments 6-10)
def cnt(s):
    return int(str(s).split()[0])


S8 = load("claim8_sauc_summary.json")
_b = S8["blocks_10_cells"]
ci("saucNull", _b["sauc_pos_null"]), ci("saucRf", _b["sauc_pos_rf_thermal"]), ci("saucCRf", _b["saucc_pos_rf_thermal"])
put("saucSupported", cnt(_b["supported_pos_rf_thermal"]))
_ns = S8["margin_identity"]["negative_share_by_band"]
put("negFarPct", 100 * (_ns["5-10"] + _ns["10-inf"]), 0), put("negNearPct", 100 * (_ns["0-0.5"] + _ns["0.5-1"]), 0)
_m = S8["margins_deg"]
for k, t in (("0.05", "A"), ("0.10", "B"), ("0.15", "C")):
    put(f"margin{t}Rf", _m[k]["mean"]), put(f"margin{t}Null", _m[f"null_{k}"]["mean"])
I9 = load("claim9_intervals.json")
_sr = {k: v for k, v in I9["support_real"].items()}
put("supMin", min(v["fires_supported"] for v in _sr.values())), put("supMax", max(v["fires_supported"] for v in _sr.values()))
put("supSaucMin", min(v["saucc_rf_thermal"]["mean"] for v in _sr.values())), put("supSaucMax", max(v["saucc_rf_thermal"]["mean"] for v in _sr.values()))
S9 = load("claim9_synthetic_summary.json")
put("ruleAuc", S9["decision"]["saucc_minus_auc_pp"], 1), put("ruleCauc", S9["decision"]["saucc_minus_cauc_pp"], 1)
put("ruleAucThirty", S9["without_first_fire"]["decision"]["saucc_minus_auc_pp"], 1)
put("ruleCaucThirty", S9["without_first_fire"]["decision"]["saucc_minus_cauc_pp"], 1)
S12 = load("claim12_summary.json")
for key, tag in (("blocks_10", "Mc"), ("blocks_40", "Tw"), ("calibrated", "Cal")):
    a = S12[key]["all"]
    put(f"{tag}TruthEnv", a["truth_env"], 2)
    for m, mt in (("auc", "Auc"), ("cauc", "Cauc"), ("saucc", "Sauc")):
        put(f"{tag}Pref{mt}", a[m]["preference_env"], 2), put(f"{tag}Bal{mt}", a[m]["balanced_acc"], 2)
        put(f"{tag}Loss{mt}", a[m]["auc_loss"], 3), put(f"{tag}Rel{mt}", a[m]["relative_loss"], 2)
    for q, qt in (("cauc_minus_auc", "CA"), ("saucc_minus_auc", "SA"), ("saucc_minus_cauc", "SC")):
        ci(f"{tag}D{qt}", a["agreement_diffs_fire_bootstrap"][q], 3)
put("McDraws", S12["blocks_10"]["draws"])
_cc = S12["calibrated"]["compare"]
put("calNullSim", _cc["simulated"]["auc_null"]), put("calNullReal", _cc["real"]["auc_null"])
put("calKeptSim", _cc["simulated"]["kept_share"], 2), put("calKeptReal", _cc["real"]["kept_share"], 2)
S14 = load("claim14_future_summary.json")
put("gEligible", S14["eligible"]), put("gExcluded", len(S14["excluded"]))
_d = S14["decision"]
put("gD", _d["mean_D"], 4), put("gDLo", _d["ci90"][0], 4), put("gDHi", _d["ci90"][1], 4), put("gVerdict", _d["verdict"])
ci("gHistAuc", S14["g1c_history"]["hist_only_auc"]), ci("gThermHist", S14["g1c_history"]["thermal_hist_auc"])
ci("gScar", S14["g1b_future_auc_minus_dist_to_scar"])
F14 = pd.read_csv(AN / "claim14_future_per_fire.csv")
put("gEventsMedian", int(F14.events.median())), put("gLargestMedian", 100 * F14.largest_event_share.median(), 0)
put("gFutTherm", F14.coord_primary_fut_thermal.mean()), put("gFutCoord", F14.coord_primary_fut_cand.mean())
put("gBaseAucChoice", int((F14.baseline_primary_choice_auc == "t").sum()))
put("gBaseCaucChoice", int((F14.baseline_primary_choice_cauc == "t").sum()))
put("gBaseLossAuc", F14.baseline_primary_loss_auc.mean()), put("gBaseLossCauc", F14.baseline_primary_loss_cauc.mean())
put("gBaseBetter", int((F14.baseline_primary_fut_thermal > F14.baseline_primary_fut_cand).sum()))
ci("gBaseDiff", boot(F14.baseline_primary_fut_thermal - F14.baseline_primary_fut_cand))
put("gBaseSaucChoice", int((F14.baseline_primary_choice_saucc == "t").sum()))
put("gBaseLossSauc", F14.baseline_primary_loss_saucc.mean())
MS["g1_baseline_future_diff_fire_bootstrap"] = boot(F14.baseline_primary_fut_thermal - F14.baseline_primary_fut_cand)
put("gTwoYear", (F14.coord_two_year_fut_thermal - F14.coord_two_year_fut_cand).mean())
put("gFullPop", (F14.coord_full_fut_thermal - F14.coord_full_fut_cand).mean())
S15 = load("claim15_summary.json")
for key, tag in (("coord_rf", "Crf"), ("coord_knn", "Knn"), ("thermal_coord", "Tc"), ("thermal_dist", "Td")):
    v = S15[key]
    ci(f"g{tag}Diff", v["future_diff_thermal_minus_cand"])
    put(f"g{tag}Better", cnt(v["thermal_better"]))
    for m, mt in (("auc", "Auc"), ("cauc", "Cauc"), ("saucc", "Sauc")):
        put(f"g{tag}Ch{mt}", cnt(v[f"chooses_location_model_{m}"])), put(f"g{tag}Loss{mt}", v[f"loss_{m}"])
    put(f"g{tag}Rel", v["relative_loss_auc"], 2)
F15 = pd.read_csv(AN / "claim15_g2_per_fire.csv")
put("gCrfUnsup", int((F15.coord_rf_choice_saucc == "none").sum()))
_g5 = S15["g5"]
put("gLofoMin", _g5["coord_rf"]["leave_one_fire_out_min_max"][0]), put("gLofoMax", _g5["coord_rf"]["leave_one_fire_out_min_max"][1])
put("gLoyoMin", min(_g5["coord_rf"]["leave_one_year_out"].values())), put("gLoyoMax", max(_g5["coord_rf"]["leave_one_year_out"].values()))
put("gNoLargest", _g5["coord_rf"]["largest_event_removed"]["mean_diff"])
put("gNoLargestBetter", _g5["coord_rf"]["largest_event_removed"]["thermal_better"])
put("gNoLargestFires", _g5["coord_rf"]["largest_event_removed"]["fires"])
put("gTcLoyoMin", min(_g5["thermal_coord"]["leave_one_year_out"].values()))
FU = load("claim15_followup.json")
put("gCountries", len(FU["countries"]))
put("gLocoMin", min(FU["coord_rf"]["leave_one_country_out"].values())), put("gLocoMax", max(FU["coord_rf"]["leave_one_country_out"].values()))
put("gTcLocoMin", min(FU["thermal_coord"]["leave_one_country_out"].values()))
ci("gTdD", FU["thermal_dist_D"])
_rp = [p for p in S15["g1d"] if p["earlier"] == "rp01_2020"][0]
put("rpThermal", _rp["later_auc_thermal"]), put("rpCoord", _rp["later_auc_coord"])
_sh = {p["earlier"]: p for p in FU["g1d_shared"]}
put("rpShared", f"{_sh['rp01_2020']['shared_cells_half_cell']:,}"), put("rpCells", f"{_sh['rp01_2020']['later_cells_total']:,}")
MS["route_b_sources"] = ["claim8_sauc_summary.json", "claim9_intervals.json", "claim9_synthetic_summary.json", "claim12_summary.json",
                         "claim14_future_summary.json", "claim14_future_per_fire.csv", "claim15_summary.json",
                         "claim15_g2_per_fire.csv", "claim15_followup.json"]

# fire selection counts, from the committed selection outputs of the analysis branch
SEL = REPO / "scripts" / "scaleup" / "selection"
_cands = json.loads((SEL / "candidates.json").read_text(encoding="utf-8"))
_pass = [r for r in _cands if 5 <= int(r["anchor"][5:7]) <= 10 and r["event_share"] >= 0.9 and max(r["aoi_deg"]) <= 1.1]
put("selCandidates", len(_cands)), put("selPass", len(_pass))
put("selKept", len(json.loads((SEL / "batch_candidates.json").read_text(encoding="utf-8"))))
put("selRepeat", len(json.loads((SEL / "repeat_candidates.json").read_text(encoding="utf-8"))))

MS["note"] = ("Statistics computed by build_values_figures.py from the analysis outputs. transfer_fire_level supersedes "
              "the direction-level intervals in claim4_summary.json (plan amendment 3). label_variants: near, far and rise "
              "are means over the same fires (those with both bands scored); far is the farthest band beyond 0.5 km with "
              "at least 20 unburned cells, and far_band_used counts which band that was.")


def _git(path, only=()):
    """HEAD commit and whether tracked source files differ from it (only: limit the check to these paths, so the
    outputs this script writes do not count)."""
    import subprocess
    r = subprocess.run(["git", "-C", str(path), "rev-parse", "HEAD"], capture_output=True, text=True)
    d = subprocess.run(["git", "-C", str(path), "status", "--porcelain", "--untracked-files=no", "--", *only],
                       capture_output=True, text=True)
    return {"commit": r.stdout.strip(), "uncommitted_changes": bool(d.stdout.strip())}


def _sha(p):
    import hashlib
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


MS["provenance"] = {
    "analysis_checkout": _git(REPO),
    "build_checkout": _git(HERE, ("build_values_figures.py", "make_highlights.py", "manuscript.tex", "references.bib")),
    "bootstrap": {"resamples": 2000, "seed": 42, "unit": "fire (node bootstrap for transfer directions)"},
    "inputs_sha256": {p.name: _sha(p) for p in sorted(AN.glob("*.json")) + sorted(AN.glob("*.csv"))},
}
(HERE / "manuscript_statistics.json").write_text(json.dumps(MS, indent=1), encoding="utf-8")
(HERE / "values.tex").write_text("% written by build_values_figures.py, do not edit\n" +
                                 "".join(f"\\newcommand{{\\v{k}}}{{{v}}}\n" for k, v in sorted(V.items())), encoding="utf-8")
print(len(V), "values")

# ---------------------------------------------------------------- supplementary tables (supp_tables.tex)
def f3(x):
    return "--" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x:.3f}"


def civ(d, nd=3):
    return f"{d['mean']:.{nd}f} [{d['lo']:.{nd}f}, {d['hi']:.{nd}f}]"


ST = []
# S1: the fires, in the order of Figure 1
_fr1 = _fr.sort_values("auc_rf_thermal_b10", ascending=False).reset_index(drop=True)
ST.append("\\begin{table}[p]\\centering\\caption{The 31 fires, in the order of the rows of Fig.~1 from the top. Window: first and "
          "last day of the label window. Cells and burned: population cells and burned cells. AUC with 5~km blocks.}"
          "\\label{tab:s-fires}\\footnotesize\\begin{tabular}{rllrrrcc}\\toprule\n"
          "Row & Fire & Label window & Cells & Burned & Burned \\% & Random forest & Null model \\\\\\midrule\n")
for i, r in _fr1.iterrows():
    e = regions.EXPERIMENTS[r.fire]
    ST.append(f"{i + 1} & {r.fire.replace('_', chr(92) + '_')} & {e['label_start_date']} to {e['label_end_date']} & {int(r.cells):,} & "
              f"{int(r.burned):,} & {100 * r.prevalence:.1f} & {r.auc_rf_thermal_b10:.3f} & {r.auc_null_b10:.3f} \\\\\n")
ST.append("\\bottomrule\\end{tabular}\\end{table}\n\n")
# S2: robustness of claim 1
ST.append("\\begin{table}[p]\\centering\\caption{Robustness of the comparison with the geographic null model (5~km blocks unless "
          "stated). Means over fires with 95\\% bootstrap intervals over fires; wins are counts of fires.}\\label{tab:s-robust}"
          "\\footnotesize\\begin{tabular}{L{5.2cm}L{6.4cm}L{3.6cm}}\\toprule Check & Result & Null model wins \\\\\\midrule\n")
ST.append(f"Pooled out-of-fold AUC, null / forest & {civ(P['blocks_10_cells']['auc_null'])} / {civ(P['blocks_10_cells']['auc_rf_thermal'])} & {P['blocks_10_cells']['null_beats_rf_thermal']} \\\\\n")
ST.append(f"Within-fold AUC, null / forest & {civ(RB1['foldwise']['null'])} / {civ(RB1['foldwise']['rf'])} & {RB1['foldwise']['null_beats_rf']} \\\\\n")
for k, v in RB1["designs"].items():
    sh, sd = k.replace("shift", "").split("_seed")
    ST.append(f"Blocks shifted by {sh} cells, fold seed {sd} & {civ(v['auc_null'])} / {civ(v['auc_rf'])} & {v['null_beats_rf']} \\\\\n")
ST.append(f"Forest with distance feature, all cells & {civ(CB['auc_combined'])} & combined beats null in {CB['combined_beats_null']} \\\\\n")
ST.append(f"Forest with distance feature, 0--0.5 km band & {civ(CB['near_combined'])} (null {civ(CB['near_null'])}) & combined beats null in {CB['near_combined_beats_null']} \\\\\n")
ST.append(f"Same, training distance to all other burned training cells & {civ(RB1['combined']['auc_combined'])} & combined beats null in {RB1['combined']['combined_beats_null']} \\\\\n")
ST.append("\\midrule\\multicolumn{3}{L{15.2cm}}{Calibrated AUC of the forest by matching tolerance and order of the burned cells} \\\\\n")
for k, v in RB1["matching"].items():
    t, sd = k.replace("tol", "").split("_seed")
    ST.append(f"Tolerance {t}, order seed {sd} & cAUC {civ(v['cauc'])} & kept {100 * v['kept_share']['mean']:.0f}\\% of burned cells \\\\\n")
ST.append(f"\\midrule\\multicolumn{{3}}{{L{{15.2cm}}}}{{20~km design, {F20['fires']} fires, {len(_f20)} test folds: median {F20['median_blocks']:.0f} "
          f"blocks per fold, {int((_f20.blocks == 1).sum())} folds with one block, {int((_f20.burned == 0).sum())} with no burned cell, "
          f"at least {F20['min_unburned']} unburned cells}} \\\\\n")
ST.append("\\bottomrule\\end{tabular}\\end{table}\n\n")
# S3: Sentinel-2 check, fixed and recomputed bands, same fires
ST.append("\\begin{table}[p]\\centering\\caption{Sentinel-2 check of the thermal random forest. Fixed: distance bands of the MCD64A1 "
          "label. Recomputed: bands from the variant's own burned cells. Paired differences from the MCD64A1 reference are over the same "
          "fires and valid cells. Means over fires with 95\\% bootstrap intervals.}\\label{tab:s-labels}\\footnotesize"
          "\\begin{tabular}{L{3.4cm}L{3.6cm}L{3.6cm}L{4.4cm}}\\toprule Variant, threshold & Near band, fixed minus reference & Far band, fixed minus reference & "
          "Rise, recomputed bands \\\\\\midrule\n")
for vn, vl in (("a_s2_label", "Sentinel-2 label"), ("c_relabel", "Missed cells relabelled")):
    for th in ("010", "027"):
        v = G3[f"{vn}_{th}"]
        ST.append(f"{vl}, {int(th) / 100:.2f} & {civ(v['fixed_minus_ref_near'])} & {civ(v['fixed_minus_ref_far'])} & "
                  f"{civ(v['recomputed_rise'])}, positive in {v['recomputed_rise_positive']} \\\\\n")
ST.append("\\bottomrule\\end{tabular}\\end{table}\n\n")
# S4: published datasets, what was compared
_rows = [
    ("Alberta, temporal", T7[(T7.dataset == "alberta")].iloc[0], "AUC on the 2018--2021 test cells; package bootstrap table",
     "AUC on the same cells"),
    ("British Columbia", None, "As reported (10-fold spatial CV)", "Pooled out-of-fold AUC, mean over 10 point samples"),
    ("Mesogeos", T7[T7.dataset == "mesogeos"].iloc[0], "Benchmark AUPRC on test years", "Average precision on the same samples"),
    ("South Korea", T7[T7.dataset == "korea"].iloc[0], "AUC on the 30\\% test split", "AUC on the same split"),
    ("Alberta, blocks", T7[(T7.dataset == "alberta")].iloc[2], "Mean of fold AUC", "Mean of fold AUC, folds from the block rule"),
    ("Italy", T7[T7.dataset == "italy"].iloc[0], "Median of 100 runs", "Pooled out-of-fold AUC of one run"),
]
ST.append("\\begin{table}[p]\\centering\\caption{Published datasets: size of the evaluated set, prevalence and how each score "
          "is summarised.}\\label{tab:s-open}\\footnotesize\\begin{tabular}{lrrL{3.6cm}L{3.6cm}}\\toprule Dataset & Fire & Non-fire & "
          "Published score & Our score \\\\\\midrule\n")
for name, r, pub, ours in _rows:
    if r is None:
        nf, nn = int(bc.n_fire.mean()), int(bc.n_nonfire.mean())
    else:
        nf, nn = int(r.n_fire), int(r.n_nonfire)
    ST.append(f"{name} & {nf:,} & {nn:,} & {pub} & {ours} \\\\\n")
ST.append("\\bottomrule\\end{tabular}\\end{table}\n")
(HERE / "supp_tables.tex").write_text("% written by build_values_figures.py, do not edit\n" + "".join(ST), encoding="utf-8")

# ---------------------------------------------------------------- figures
FR = pd.read_csv(AN / "claims12_per_fire.csv")
FR = FR[FR.fire != "montiferru_2021"]
BR = pd.read_csv(AN / "claims12_bands.csv")
BR = BR[BR.fire != "montiferru_2021"]

# Fig. 1: per-fire AUC of the null model and the thermal RF at three block sizes
fig, axs = plt.subplots(1, 3, figsize=(7.2, 3.0), sharey=True)
_order = FR.sort_values("auc_rf_thermal_b10").fire.tolist()       # one order, from the 5 km design, in all panels
_row = {f: i for i, f in enumerate(_order)}
for ax, k, title in zip(axs, (10, 20, 40), ("5 km blocks", "10 km blocks", "20 km blocks")):
    g = FR.dropna(subset=[f"auc_null_b{k}"])
    yy = g.fire.map(_row).to_numpy()
    ax.hlines(yy, g[f"auc_rf_thermal_b{k}"], g[f"auc_null_b{k}"], color="#bbbbbb", lw=0.8)
    for m, dy in (("rf_thermal", -0.2), ("null", 0.2)):          # small vertical offset keeps equal scores visible
        ax.plot(g[f"auc_{m}_b{k}"], yy + dy, MRK[m], color=COL[m], ms=3.5, label=LAB[m])
    ax.set_title(title)
    ax.set_xlabel("ROC AUC")
    ax.set_xlim(min(0.45, float(np.floor(10 * FR[[f"auc_rf_thermal_b{kk}" for kk in (10, 20, 40)]].min().min()) / 10)), 1.0)
    ax.axvline(0.5, color="#888888", lw=0.5, ls=":")
    ax.set_yticks([])
axs[0].set_ylabel("Fires, ordered by random-forest AUC at 5 km")
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

# graphical abstract: its own wide layout, 5:2 (7.5 x 3 in at 200 dpi = 1500 x 600 px), two models only
# 5 x 2 in at 300 dpi = 1500 x 600 px (Elsevier: 5:2, at least 300 dpi); fonts sized for that print width
with plt.rc_context({"font.size": 8, "axes.labelsize": 8, "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "legend.fontsize": 7.5}):
    fig, ax = plt.subplots(figsize=(5.0, 2.0))
    for m, lab in (("null", "Predictor-free geographic model"), ("rf_thermal", "Random forest")):
        mean = [P["bands"][b][f"auc_{m}"]["mean"] for b in order]
        ax.plot(xs, mean, marker=MRK[m], color=COL[m], ms=4.5, lw=1.4, label=lab)
    ax.set_xticks(xs, ["0-0.5", "0.5-1", "1-2", "2-5", "5-10", ">10"])
    ax.set_xlabel("Distance of unburned test cells from the fire (km)")
    ax.set_ylabel("AUC, mean of 31 fires")
    ax.set_ylim(0.55, 1.02)
    ax.legend(frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(HERE / "graphical_abstract.png", dpi=300)
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
ax.set_ylabel("Unburned cells at least\nhalf burned in Sentinel-2 (%)")
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(FIG / "Figure_3.pdf")
plt.close(fig)

# Fig. 4: open datasets, reported AUC and the null model's AUC under the authors' protocol
rows = [("Alberta, temporal test", float(al.iloc[0].reported_auc), float(al.iloc[0].null_auc)),
        ("British Columbia, 50 km blocks", float(bc.reported_auc.iloc[0]), float(bc.null_auc.mean())),
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

# Figure_later: within-fire choice against later burning, 18 fires, two pairs
G2T = pd.read_csv(AN / "claim15_g2_per_fire.csv")
fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.2), sharey=True)
for ax, cand, lab in ((axs[0], "coord_rf", "Random forest on coordinates"), (axs[1], "thermal_coord", "Thermal forest plus coordinates")):
    g = G2T.sort_values("fut_thermal").reset_index(drop=True)
    yy = np.arange(len(g))
    ax.hlines(yy, g.fut_thermal, g[f"{cand}_fut"], color="#bbbbbb", lw=0.8)
    ax.plot(g.fut_thermal, yy + 0.15, MRK["rf_thermal"], color=COL["rf_thermal"], ms=3.5, label="Random forest, thermal set")
    ax.plot(g[f"{cand}_fut"], yy - 0.15, "D", color="#D55E00", ms=3.5, label=lab)
    ax.axvline(0.5, color="#888888", lw=0.5, ls=":")
    ax.set_xlabel("ROC AUC on later burning")
    ax.set_title(lab)
    ax.set_yticks([])
    ax.legend(frameon=False, loc="lower right", fontsize=6)
axs[0].set_ylabel("Fires, ordered by the thermal forest")
fig.tight_layout()
fig.savefig(FIG / "Figure_later.pdf")
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
    ax.axhline(S4["zscore"]["mean"], color="#0072B2", ls="--", lw=0.8, label="Single source fire, z-scored predictors")
    ax.axhline(S4["baseline"]["mean"], color="#E69F00", ls="-.", lw=0.8, label="Single source fire, baseline set")
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
