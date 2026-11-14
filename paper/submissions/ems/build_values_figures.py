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
# buffered validation: test cells and fires that remain scored (skipped folds leave their test cells unscored)
MS["buffers"] = {}
for b, tag in ((1, "One"), (2, "Two"), (5, "Five"), (10, "Ten")):
    scored = total = fires = 0
    for r in _fr.itertuples():
        hits = list((AN / "cache").glob(f"{r.fire}_buffer{b}_b10_*.npy"))
        assert len(hits) == 1, f"expected one buffer cache file for {r.fire} at {b} km, found {len(hits)}"
        o = np.load(hits[0])[0]
        assert len(o) == r.cells, (r.fire, b, len(o), r.cells)       # one prediction slot per population cell
        n_ok = int(np.isfinite(o).sum())
        scored, total, fires = scored + n_ok, total + len(o), fires + (n_ok > 0)
    MS["buffers"][f"{b}_km"] = {"cells_scored": scored, "cells_total": total, "fires_with_scored_cells": fires}
    put(f"bufCellsPct{tag}", 100 * scored / total, 0), put(f"bufFires{tag}", fires)
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

MS["note"] = ("Statistics computed by build_values_figures.py from the analysis outputs. transfer_fire_level supersedes "
              "the direction-level intervals in claim4_summary.json (plan amendment 3). label_variants: near, far and rise "
              "are means over the same fires (those with both bands scored); far is the farthest band beyond 0.5 km with "
              "at least 20 unburned cells, and far_band_used counts which band that was.")


def _git(path):
    import subprocess
    r = subprocess.run(["git", "-C", str(path), "rev-parse", "HEAD"], capture_output=True, text=True)
    d = subprocess.run(["git", "-C", str(path), "status", "--porcelain"], capture_output=True, text=True)
    return {"commit": r.stdout.strip(), "uncommitted_changes": bool(d.stdout.strip())}


def _sha(p):
    import hashlib
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


MS["provenance"] = {
    "analysis_checkout": _git(REPO), "build_checkout": _git(HERE),
    "bootstrap": {"resamples": 2000, "seed": 42, "unit": "fire (node bootstrap for transfer directions)"},
    "inputs_sha256": {p.name: _sha(p) for p in sorted(AN.glob("*.json")) + sorted(AN.glob("*.csv"))},
}
(HERE / "manuscript_statistics.json").write_text(json.dumps(MS, indent=1), encoding="utf-8")
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
