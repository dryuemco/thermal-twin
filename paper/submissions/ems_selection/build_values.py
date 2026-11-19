"""build_values.py: writes values.tex, supp_selection_tables.tex, manuscript_statistics.json, the figures and the
graphical abstract of the selection manuscript from the result files of branch scaleup-31fires.

Every result quoted in manuscript.tex and supplementary.tex comes from values.tex (written here) or from
values_frozen.tex (the generated values file of the 14 November 2026 build of the 31-fire analysis, copied
unchanged from ../ems/values.tex). Protocol constants (block size, thresholds, seeds, grids) are written in the text.

Inputs (read only):
  $THERMAL_TWIN_REPO/results/scaleup/claim14/claim14_future_summary.json, claim14_future_per_fire.csv, claim14_events.csv
  $THERMAL_TWIN_REPO/results/scaleup/claim15/claim15_summary.json, claim15_followup.json
  $THERMAL_TWIN_REPO/results/scaleup/claim16/claim16_summary.json, claim16_per_fire.csv, claim16_scores/*.npz
  $THERMAL_TWIN_REPO/results/scaleup/claim12/claim12_summary.json, claim12_runs_b10.csv, claim12_runs_b40.csv, claim13_runs.csv
  $THERMAL_TWIN_REPO/results/scaleup/label_counts_11a.json, claim14/claim14_history.csv, claim15/claim15_g2_per_fire.csv
  fires_table_source.tex (first table only, the list of the 31 fires)

Run:  python build_values.py      (Python 3.12, numpy, matplotlib; THERMAL_TWIN_REPO defaults to the sibling checkout)
"""
import csv
import hashlib
import json
import math
import os
import re
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
REPO = Path(os.environ.get("THERMAL_TWIN_REPO", HERE.parents[3] / "thermal-twin" / "repo"))
RES = REPO / "results" / "scaleup"
FIG = HERE / "figures"
FIG.mkdir(exist_ok=True)
COUNTRIES = REPO / "scripts" / "scaleup" / "selection" / "fire_countries.json"

# Later-burning labels: "_qa1" = corrected valid-data mask (plan amendment 15, primary); "" = original labels.
SFX = os.environ.get("THERMAL_TWIN_LABEL_SUFFIX", "_qa1")
assert SFX in ("", "_qa1"), SFX


def rp(claim, name, sfx=None):
    """Result file of claim 14, 15 or 16 for a label variant (folder and file name carry the suffix)."""
    s = SFX if sfx is None else sfx
    return RES / f"{claim}{s}" / f"{Path(name).stem}{s}{Path(name).suffix}"


LABEL_FILES = [("claim14", "claim14_future_summary.json"), ("claim14", "claim14_future_per_fire.csv"),
               ("claim14", "claim14_events.csv"), ("claim15", "claim15_summary.json"),
               ("claim15", "claim15_followup.json"), ("claim16", "claim16_summary.json"),
               ("claim16", "claim16_per_fire.csv")]
INPUTS = [rp(c, n, s) for s in sorted({SFX, ""}) for c, n in LABEL_FILES] + [
    RES / "claim16" / "claim16_scores_manifest.json",
    RES / "claim12" / "claim12_summary.json",
    RES / "claim12" / "claim13_runs.csv",
    RES / "claim12" / "claim12_runs_b10.csv",
    RES / "claim12" / "claim12_runs_b40.csv",
    RES / "label_counts_11a.json",
    COUNTRIES,
    rp("claim14", "claim14_history.csv"),
    rp("claim15", "claim15_g2_per_fire.csv"),
    HERE / "fires_table_source.tex",
    HERE / "values_frozen.tex",
]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def jload(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def repo_commit(repo):
    git = repo / ".git"
    if git.is_file():
        git = git.parent / git.read_text().strip().removeprefix("gitdir: ")
    if not git.exists():
        return None
    common = git / "commondir"
    common = git / common.read_text().strip() if common.exists() else git
    head = (git / "HEAD").read_text().strip()
    while head.startswith("ref: "):
        ref = head.removeprefix("ref: ")
        loose = next((d / ref for d in (git, common) if (d / ref).is_file()), None)
        if loose is not None:
            head = loose.read_text().strip()
        else:
            packed = (common / "packed-refs").read_text().splitlines()
            head = next(line.split()[0] for line in packed
                        if line and line[0] not in "#^" and line.split()[1] == ref)
    assert re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", head), head
    return head


def rows(p):
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


V = {}


def put(name, value, fmt=None):
    assert re.fullmatch(r"s[A-Za-z]+", name), name
    assert name not in V, name
    if fmt is not None:
        value = format(value, fmt)
    V[name] = str(value)


def f3(x):
    return format(x, ".3f")


def ci(name, d, keys=("mean", "lo", "hi")):
    put(name, f3(d[keys[0]]))
    put(name + "Lo", f3(d[keys[1]]))
    put(name + "Hi", f3(d[keys[2]]))


def count(s):
    """'14 of 18' -> 14"""
    return int(s.split(" of ")[0])


# ---------------------------------------------------------------- frozen values (31-fire build of 14 November)
frozen = dict(re.findall(r"\\newcommand\{\\(v\w+)\}\{(.*?)\}\s*$",
                         (HERE / "values_frozen.tex").read_text(encoding="utf-8"), re.M))

# ---------------------------------------------------------------- window A: later burning to 2023 (G1, G2)
c14 = jload(rp("claim14", "claim14_future_summary.json"))
c15 = jload(rp("claim15", "claim15_summary.json"))
c15f = jload(rp("claim15", "claim15_followup.json"))
pf14 = rows(rp("claim14", "claim14_future_per_fire.csv"))
ev14 = {r["fire"]: r for r in rows(rp("claim14", "claim14_events.csv"))}
# original labels, for the comparison table and the checks against the frozen build
o14 = jload(rp("claim14", "claim14_future_summary.json", ""))
o15 = jload(rp("claim15", "claim15_summary.json", ""))
o16 = jload(rp("claim16", "claim16_summary.json", ""))

put("sAElig", c14["eligible"])
put("sAExcl", len(c14["excluded"]))
fiveA = sum(1 for r in pf14 if int(r["year"]) <= 2019)
put("sAEarly", fiveA)  # eligible fires from 2017-2019

PAIRS = {"Crf": "coord_rf", "Knn": "coord_knn", "Tc": "thermal_coord", "Td": "thermal_dist"}
PAIR_LABELS = {"coord_rf": "Coordinate-only RF", "coord_knn": "Coordinate-only kNN",
               "thermal_coord": "Thermal RF + coordinates", "thermal_dist": "Thermal RF + distance"}
MEASURES = ("auc", "cauc", "saucc")
for tag, key in PAIRS.items():
    d = c15[key]
    put(f"sA{tag}ChAuc", count(d["chooses_location_model_auc"]))
    put(f"sA{tag}ChCauc", count(d["chooses_location_model_cauc"]))
    put(f"sA{tag}ChSauc", count(d["chooses_location_model_saucc"]))
    put(f"sA{tag}Better", count(d["thermal_better"]))
    ci(f"sA{tag}Diff", d["future_diff_thermal_minus_cand"])
    put(f"sA{tag}LossAuc", f3(d["loss_auc"]))
    put(f"sA{tag}LossCauc", f3(d["loss_cauc"]))
    put(f"sA{tag}LossSauc", f3(d["loss_saucc"]))
    put(f"sA{tag}Rel", format(d["relative_loss_auc"], ".2f"))
    put(f"sA{tag}Rule", "met" if d["transfer_failure_rule_10_1"] else "not met")

put("sACrfCoordBetter", c14["eligible"] - count(c15["coord_rf"]["thermal_better"]))
dA = c14["decision"]
put("sADMean", format(dA["mean_D"], ".4f"))
put("sADLo", format(dA["ci90"][0], ".4f"))
put("sADHi", format(dA["ci90"][1], ".4f"))
put("sADVerdict", dA["verdict"])
put("sADTwoYear", format(c14["sensitivity"]["coord_two_year"]["mean_D"], ".4f"))
put("sADEvent", format(c14["sensitivity"]["coord_event_weighted"]["mean_D"], ".4f"))
put("sALoeoMin", format(c14["leave_one_event_out_D"]["min_over_fires_min"], ".3f"))
put("sALoeoMax", format(c14["leave_one_event_out_D"]["max_over_fires_max"], ".3f"))
put("sAUnsupSauc", sum(1 for r in pf14 if r["focal_coord_saucc"] == "" or r["focal_thermal_saucc"] == ""))

# means of focal and later AUC on the window-A fires
fa = np.array([[float(r["focal_thermal_auc"]), float(r["focal_coord_auc"]),
                float(r["focal_thermal_cauc"]), float(r["focal_coord_cauc"]),
                float(r["coord_primary_fut_thermal"]), float(r["coord_primary_fut_cand"])] for r in pf14])
put("sAFocTherm", f3(fa[:, 0].mean()))
put("sAFocCoord", f3(fa[:, 1].mean()))
put("sAFocThermC", f3(fa[:, 2].mean()))
put("sAFocCoordC", f3(fa[:, 3].mean()))
put("sALateTherm", f3(fa[:, 4].mean()))
put("sALateCoord", f3(fa[:, 5].mean()))
put("sAFocCoordMin", f3(fa[:, 1].min()))

# thermal against baseline RF (secondary comparison of amendment 9)
bt = [(float(r["baseline_primary_fut_thermal"]), float(r["baseline_primary_fut_cand"]),
       r["baseline_primary_choice_auc"], float(r["baseline_primary_loss_auc"])) for r in pf14]
put("sABaseChoseTherm", sum(1 for x in bt if x[2] == "t"))
put("sABaseBetter", sum(1 for x in bt if x[1] > x[0]))
put("sABaseLossAuc", f3(np.mean([x[3] for x in bt])))
put("sABaseLate", f3(np.mean([x[1] for x in bt])))
d_base = c14["sensitivity"]["baseline_primary"]
put("sABaseD", d_base["mean_D"], ".4f")
put("sABaseDLo", d_base["ci90"][0], ".4f")
put("sABaseDHi", d_base["ci90"][1], ".4f")
put("sABaseDVerdict", d_base["verdict"])
put("sAFullTherm", np.mean([float(r["coord_full_fut_thermal"]) for r in pf14]), ".3f")
put("sAFullCoord", np.mean([float(r["coord_full_fut_cand"]) for r in pf14]), ".3f")

# future events in window A
evs = [int(ev14[r["fire"]]["events"]) for r in pf14]
lshare = [float(ev14[r["fire"]]["largest_event_share"]) for r in pf14]
put("sAEventsMed", int(np.median(evs)))
put("sAEventsMin", min(evs))
put("sAEventsMax", max(evs))
put("sALargestMed", round(100 * float(np.median(lshare))))

# G1b: distance to the focal scar as a score for later burning
g1b = c14["g1b_future_auc_minus_dist_to_scar"]
ci("sAScar", g1b)
put("sAScarMin", f3(g1b["min"]))
put("sAScarMax", f3(g1b["max"]))
full = c14["sensitivity"]["coord_full"]
put("sADFull", format(full["mean_D"], ".4f"))
put("sADFullLo", format(full["ci90"][0], ".4f"))
put("sADFullHi", format(full["ci90"][1], ".4f"))
put("sATwoYearFires", c14["sensitivity"]["coord_two_year"]["fires"])

# G1c: burn history before the focal window, AUC on the focal event
put("sHistFocal", f3(c14["g1c_history"]["hist_only_auc"]["mean"]))
put("sHistTherm", c14["g1c_history"]["thermal_auc"]["mean"], ".3f")
put("sHistThermHist", c14["g1c_history"]["thermal_hist_auc"]["mean"], ".3f")

# G5 sensitivities (coordinate RF)
g5 = c15["g5"]["coord_rf"]
loco = list(c15f["coord_rf"]["leave_one_country_out"].values())
put("sACountries", len(c15f["countries"]))
put("sALocoMin", f3(min(loco)))
put("sALocoMax", f3(max(loco)))
put("sALoyoMin", f3(min(g5["leave_one_year_out"].values())))
put("sALoyoMax", f3(max(g5["leave_one_year_out"].values())))
put("sALofoMin", f3(g5["leave_one_fire_out_min_max"][0]))
put("sALofoMax", f3(g5["leave_one_fire_out_min_max"][1]))
put("sANoLargestFires", g5["largest_event_removed"]["fires"])
put("sANoLargest", f3(g5["largest_event_removed"]["mean_diff"]))
put("sANoLargestBetter", g5["largest_event_removed"]["thermal_better"])
loco_tc = list(c15f["thermal_coord"]["leave_one_country_out"].values())
put("sATcLocoMin", f3(min(loco_tc)))
put("sATcLocoMax", f3(max(loco_tc)))
ci("sATdD", c15f["thermal_dist_D"])

# repeat pairs (G1d), descriptive
pairs_rp = c15["g1d"]
put("sRpN", len(pairs_rp))
put("sRpCoordChosen", sum(1 for p in pairs_rp if p["earlier_choice_pooled_auc"] == "coord"))
put("sRpThermBetter", sum(1 for p in pairs_rp if p["later_auc_thermal"] > p["later_auc_coord"]))

# ---------------------------------------------------------------- window B: 2024 to September 2026 (11.4)
c16 = jload(rp("claim16", "claim16_summary.json"))
pf16 = rows(rp("claim16", "claim16_per_fire.csv"))
put("sBElig", c16["eligible"])
put("sBSec", len(c16["secondary_fires"]))
put("sBNotElig", len(c16["not_eligible"]))
inA = {r["fire"] for r in pf14}
inB = {r["fire"] for r in pf16 if r["eligible"] == "True"}
put("sBOverlap", len(inA & inB))
put("sAOnly", len(inA - inB))

for tag, key in PAIRS.items():
    d = c16["rule_10_1"][key]["primary"]
    put(f"sB{tag}ChAuc", d["pooled_auc_chooses_location"])
    put(f"sB{tag}ChCauc", d["cauc_chooses_location"])
    put(f"sB{tag}ChSauc", d["saucc_chooses_location"])
    put(f"sB{tag}Better", d["thermal_better"])
    put(f"sB{tag}Diff", f3(d["mean"]))
    put(f"sB{tag}DiffLo", f3(d["ci95"][0]))
    put(f"sB{tag}DiffHi", f3(d["ci95"][1]))
    put(f"sB{tag}LossAuc", f3(d["loss"]["auc"]))
    put(f"sB{tag}LossCauc", f3(d["loss"]["cauc"]))
    put(f"sB{tag}LossSauc", f3(d["loss"]["saucc"]))
    put(f"sB{tag}P", format(d["p_holm"], ".3f"))
    put(f"sB{tag}Rule", "met" if d["transfer_failure"] else "not met")
    s = c16["rule_10_1"][key]["secondary"]
    put(f"sBS{tag}Diff", f3(s["mean"]))
    put(f"sBS{tag}DiffLo", f3(s["ci95"][0]))
    put(f"sBS{tag}DiffHi", f3(s["ci95"][1]))
    put(f"sBS{tag}Better", s["thermal_better"])
    put(f"sBS{tag}ChAuc", s["pooled_auc_chooses_location"])
    put(f"sBS{tag}Rule", "met" if s["transfer_failure"] else "not met")

dB = c16["rule_9_5"]["primary"]
put("sBDMean", format(dB["mean"], ".4f"))
put("sBDLo", format(dB["ci90"][0], ".4f"))
put("sBDHi", format(dB["ci90"][1], ".4f"))
put("sBDVerdict", dB["verdict"])
put("sBDSame", dB["same_choice"])
put("sBSDVerdict", c16["rule_9_5"]["secondary"]["verdict"])

late = np.array([[float(r["late_thermal"]), float(r["coord_rf_late"])] for r in pf16 if r["eligible"] == "True"])
put("sBLateTherm", f3(late[:, 0].mean()))
put("sBLateCoord", f3(late[:, 1].mean()))
put("sBBaseLate", np.mean([float(r["baseline_late"]) for r in pf16 if r["eligible"] == "True"]), ".3f")


# focal pooled AUC of every frozen score set (claim16_scores, recomputed with the seeds and folds of G1/G2)
def auc(y, s):
    y = np.asarray(y).astype(bool)
    s = np.asarray(s, dtype=float)
    order = np.argsort(s, kind="mergesort")
    ss = s[order]
    ranks = np.empty(len(s))
    i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and ss[j + 1] == ss[i]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2 + 1
        i = j + 1
    n1 = y.sum()
    n0 = len(y) - n1
    return (ranks[y].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)


man = jload(RES / "claim16" / "claim16_scores_manifest.json")
focal = {}
for fire, h in man.items():
    p = RES / "claim16" / "claim16_scores" / f"{fire}.npz"
    assert sha(p) == h, fire
    z = np.load(p)
    focal[fire] = {k: auc(z["y"], z[k]) for k in ("thermal", "coord_rf", "null")}
# check against the G1 per-fire table (same seeds and folds)
for r in pf14:
    assert abs(focal[r["fire"]]["thermal"] - float(r["focal_thermal_auc"])) < 1e-9, r["fire"]
    assert abs(focal[r["fire"]]["coord_rf"] - float(r["focal_coord_auc"])) < 1e-9, r["fire"]
put("sAllCoordChose", sum(1 for f in focal.values() if f["coord_rf"] > f["thermal"]))
put("sAllN", len(focal))
put("sAllFocCoord", f3(np.mean([f["coord_rf"] for f in focal.values()])))
put("sAllFocTherm", f3(np.mean([f["thermal"] for f in focal.values()])))
put("sAllFocNull", f3(np.mean([f["null"] for f in focal.values()])))
put("sAllCoordBeatsNull", sum(1 for f in focal.values() if f["coord_rf"] > f["null"]))

# ---------------------------------------------------------------- simulations (claims 12 and 13)
c12 = jload(RES / "claim12" / "claim12_summary.json")
for tag, key in (("Ten", "blocks_10"), ("Forty", "blocks_40"), ("Cal", "calibrated")):
    a = c12[key]["all"]
    put(f"sSim{tag}Runs", f"{a['runs']:,}")
    put(f"sSim{tag}Truth", format(a["truth_env"], ".2f"))
    for m, mt in (("auc", "Auc"), ("cauc", "Cauc"), ("saucc", "Sauc")):
        put(f"sSim{tag}Bal{mt}", format(a[m]["balanced_acc"], ".2f"))
        put(f"sSim{tag}Pref{mt}", format(a[m]["preference_env"], ".2f"))
        put(f"sSim{tag}Loss{mt}", f3(a[m]["auc_loss"]))
    put(f"sSim{tag}LossEnv", f3(a["always_env"]["auc_loss"]))
for tag, fn in (("Ten", "claim12_runs_b10.csv"), ("Forty", "claim12_runs_b40.csv")):
    put(f"sSim{tag}AllRuns", f"{len(rows(RES / 'claim12' / fn)):,}")
put("sSimTenFires", c12["blocks_10"]["fires"])
put("sSimTenDraws", c12["blocks_10"]["draws"])
put("sSimFortyFires", c12["blocks_40"]["fires"])
put("sSimTenNull", f3(c12["blocks_10"]["auc_null_mean"]))
cmp_ = c12["calibrated"]["compare"]
put("sCalNullReal", f3(cmp_["real"]["auc_null"]))
put("sCalNullSim", f3(cmp_["simulated"]["auc_null"]))
put("sCalKeptReal", round(100 * cmp_["real"]["kept_share"]))
put("sCalKeptSim", round(100 * cmp_["simulated"]["kept_share"]))
put("sCalSupReal", round(100 * cmp_["real"]["sauc_supported"]))
put("sCalSupSim", round(100 * cmp_["simulated"]["sauc_supported"]))
r13 = rows(RES / "claim12" / "claim13_runs.csv")
env_won = sum(1 for r in r13 if float(r["truth_env"]) > float(r["truth_geo"]))
put("sCalEnvWon", env_won)
put("sCalCaucEnv", sum(1 for r in r13 if float(r["cauc_env"]) > float(r["cauc_geo"])))
put("sCalCaucEnvRight", sum(float(r["cauc_env"]) > float(r["cauc_geo"])
                           and float(r["truth_env"]) > float(r["truth_geo"]) for r in r13))
put("sCalAucEnv", sum(1 for r in r13 if float(r["auc_env"]) > float(r["auc_geo"])))

# ---------------------------------------------------------------- consistency with the frozen build
oc = o15["coord_rf"]
checks = {  # the frozen 14 November build used the original labels
    "vgCrfDiff": f3(oc["future_diff_thermal_minus_cand"]["mean"]), "vgCrfLossAuc": f3(oc["loss_auc"]),
    "vgCrfChAuc": str(count(oc["chooses_location_model_auc"])), "vgCrfChCauc": str(count(oc["chooses_location_model_cauc"])),
    "vgCrfBetter": str(count(oc["thermal_better"])),
    "vgKnnDiff": f3(o15["coord_knn"]["future_diff_thermal_minus_cand"]["mean"]),
    "vgEligible": str(o14["eligible"]), "vgScar": f3(o14["g1b_future_auc_minus_dist_to_scar"]["mean"]),
    "vgHistAuc": f3(o14["g1c_history"]["hist_only_auc"]["mean"]),
    "vCalBalAuc": V["sSimCalBalAuc"], "vMcBalCauc": V["sSimTenBalCauc"],
}
mism = {k: (frozen[k], v) for k, v in checks.items() if k in frozen and frozen[k] != v}
assert not mism, mism


# ---------------------------------------------------------------- original against corrected labels (amendment 15)
def cmp_rows(a14, a15, a16):
    out = [("Window A: eligible fires", str(a14["eligible"]))]
    for key, lab in (("coord_rf", "coordinate-only RF"), ("coord_knn", "coordinate-only kNN"),
                     ("thermal_coord", "thermal RF + coordinates"), ("thermal_dist", "thermal RF + distance")):
        d = a15[key]
        m = d["future_diff_thermal_minus_cand"]
        out.append((f"Window A, {lab}: difference [95\\% interval]; rule",
                    f"{f3(m['mean'])} [{f3(m['lo'])}, {f3(m['hi'])}]; {'met' if d['transfer_failure_rule_10_1'] else 'not met'}"))
    d = a14["decision"]
    out.append(("Window A: $D$ [90\\% interval]", f"{d['mean_D']:.4f} [{d['ci90'][0]:.4f}, {d['ci90'][1]:.4f}]"))
    out.append(("Window A: pooled-AUC loss, coordinate-only RF", f3(a15["coord_rf"]["loss_auc"])))
    out.append(("Window B: eligible fires", str(a16["eligible"])))
    for key, lab in (("coord_rf", "coordinate-only RF"), ("coord_knn", "coordinate-only kNN"),
                     ("thermal_coord", "thermal RF + coordinates"), ("thermal_dist", "thermal RF + distance")):
        d = a16["rule_10_1"][key]["primary"]
        if key == "thermal_dist":
            for subset in ("primary", "secondary"):
                h = a16["rule_10_1"][key][subset]
                lo, hi = h["ci95"]
                rule = "met" if h["transfer_failure"] else "not met"
                p = f"; {h['p_holm']:.4f}" if subset == "primary" else ""
                stat = "; Holm $p$" if subset == "primary" else ""
                out.append((f"Window B, {lab} ({subset}): difference [95\\% interval]; rule{stat}",
                            f"{h['mean']:.4f} [{lo:.4f}, {hi:.4f}]; {rule}{p}"))
            continue
        out.append((f"Window B, {lab}: difference [95\\% interval]; rule",
                    f"{f3(d['mean'])} [{f3(d['ci95'][0])}, {f3(d['ci95'][1])}]; {'met' if d['transfer_failure'] else 'not met'}"))
    d = a16["rule_9_5"]["primary"]
    out.append(("Window B: $D$ [90\\% interval]", f"{d['mean']:.4f} [{d['ci90'][0]:.4f}, {d['ci90'][1]:.4f}]"))
    out.append(("Window B: pooled-AUC loss, coordinate-only RF", f3(a16["rule_10_1"]["coord_rf"]["primary"]["loss"]["auc"])))
    return out


CMP = list(zip(cmp_rows(o14, o15, o16), cmp_rows(c14, c15, c16))) if SFX else []
if SFX:
    oa = rows(rp("claim14", "claim14_future_per_fire.csv", "")) + o14["excluded"]
    ob = rows(rp("claim16", "claim16_per_fire.csv", ""))
    for window, prefix, original, corrected in (
        ("A", "future", oa, pf14 + c14["excluded"]),
        ("B", "late", ob, pf16),
    ):
        assert len(original) == len(corrected) == len(focal)
        assert {r["fire"] for r in original} == {r["fire"] for r in corrected} == set(focal)
        burned, unburned = f"{prefix}_burned", f"{prefix}_unburned"
        original_total = sum(int(r[burned]) + int(r[unburned]) for r in original)
        removed = original_total - sum(int(r[burned]) + int(r[unburned]) for r in corrected)
        removed_burned = sum(int(r[burned]) for r in original) - sum(int(r[burned]) for r in corrected)
        put(f"sQaCells{window}", f"{removed:,}")
        put(f"sQaBurned{window}", f"{removed_burned:,}")
        put(f"sQaPct{window}", 100 * removed / original_total, ".1f")
    put("sOBTdP", format(o16["rule_10_1"]["thermal_dist"]["primary"]["p_holm"], ".4f"))
    put("sBTdPfour", format(c16["rule_10_1"]["thermal_dist"]["primary"]["p_holm"], ".4f"))
    put("sOACrfLossAuc", f3(o15["coord_rf"]["loss_auc"]))
    put("sOBCrfLossAuc", f3(o16["rule_10_1"]["coord_rf"]["primary"]["loss"]["auc"]))

# ---------------------------------------------------------------- registered analyses
def triple(values):
    return " / ".join(map(f3, values))


def interval(mean, bounds):
    return f"{mean:.4f} [{bounds[0]:.4f}, {bounds[1]:.4f}]"


def decision(result, key="mean_D"):
    return f"$D$ {interval(result[key], result['ci90'])} (90\\%); {result['verdict']}"


def loss_text(records, prefix, t, c):
    losses = np.array([np.mean([float(r[f"{prefix}_loss_{m}"]) for r in records]) for m in MEASURES])
    gap = np.mean([abs(float(r[t]) - float(r[c])) for r in records])
    return f"$L$ {triple(losses)}; relative $L$ {triple(losses / gap)}"


def span(values):
    return f"{f3(min(values))} to {f3(max(values))}"


def omitted_loss_range(losses, groups):
    means = np.array([losses[groups != group].mean(axis=0) for group in np.unique(groups)])
    return f"$L$ {triple(means.min(axis=0))} to {triple(means.max(axis=0))}"


def register_rows():
    main, here = "Reported in main text", "Reported here"
    add_rows = []

    def add(item, status, result):
        add_rows.append((item, status, result))

    pooled, cauc, strat = [np.mean([float(r[f"coord_primary_loss_{m}"]) for r in pf14]) for m in MEASURES]
    loss = loss_text(pf14, "coord_primary", "coord_primary_fut_thermal", "coord_primary_fut_cand")
    add("9.4 G1 measures", here, f"{loss}; pooled minus stratified {pooled-strat:.4f}, cAUC minus stratified {cauc-strat:.4f}.")
    add("9.5 G1 decision", main, decision(c14["decision"]))
    add("9.7 Later events", main, f"Median {V['sAEventsMed']} events ({V['sAEventsMin']}--{V['sAEventsMax']}); "
        f"median largest-event share {V['sALargestMed']}\\%. Event years in the Claim 14 events CSV.")
    for key, lab in (("coord_event_weighted", "equal event weights"), ("coord_two_year", "two-year horizon"),
                     ("coord_full", "full population"), ("baseline_primary", "baseline RF")):
        d = c14["sensitivity"][key]
        detail = ""
        if key == "baseline_primary":
            detail = "; " + loss_text(pf14, key, f"{key}_fut_thermal", f"{key}_fut_cand")
        elif key == "coord_full":
            detail = f"; later AUC {V['sAFullTherm']} thermal / {V['sAFullCoord']} coordinate RF"
        add(f"9.7 {lab}", here if key == "baseline_primary" else main, f"{d['fires']} fires; {decision(d)}{detail}.")

    # Replace one fire's contribution to mean D at a time.
    means = [c14["decision"]["mean_D"] +
             (float(r[k]) - float(r["coord_primary_loss_auc"]) + float(r["coord_primary_loss_cauc"])) / len(pf14)
             for r in pf14 for k in ("loeo_D_min", "loeo_D_max") if r[k]]
    add("9.7 Leave one event out", here, f"Mean $D$ {min(means):.4f} to {max(means):.4f}; "
        f"per-fire $D$ {V['sALoeoMin']} to {V['sALoeoMax']}.")
    scar = c14["g1b_future_auc_minus_dist_to_scar"]
    add("9.8 G1b Scar distance", main, "Later AUC " + interval(scar["mean"], (scar["lo"], scar["hi"])))
    h = c14["g1c_history"]
    history = rows(rp("claim14", "claim14_history.csv"))
    supported = [[float(r[k]) for r in history if r[k]] for k in ("thermal_saucc", "thermal_hist_saucc")]
    add("9.8 G1c Burn history", here, f"Thermal / thermal + history: pooled {V['sHistTherm']} / {V['sHistThermHist']}; "
        f"cAUC {triple(h[k]['mean'] for k in ('thermal_cauc', 'thermal_hist_cauc'))}; stratified "
        f"{triple(np.mean(v) for v in supported)} on {len(supported[0])} / {len(supported[1])} fires; "
        f"history-only AUC {V['sHistFocal']}.")
    add("9.8 G1d Repeat pairs", main, r"Later AUC and chronology in Table~\ref{tab:s-pairs}.")

    for key in ("thermal_coord", "thermal_dist", "coord_knn"):
        d = c15[key]
        diff = d["future_diff_thermal_minus_cand"]
        choices = " / ".join(str(count(d[f"chooses_location_model_{m}"])) for m in MEASURES)
        rule = "met" if d["transfer_failure_rule_10_1"] else "not met"
        add(f"10.1 {PAIR_LABELS[key]}", main,
            f"Choices {choices}; $L$ {triple(d[f'loss_{m}'] for m in MEASURES)}; "
            f"relative $L$ {triple(d[f'relative_loss_{m}'] for m in MEASURES)}; "
            f"$\\Delta$ {interval(diff['mean'], (diff['lo'], diff['hi']))}; rule {rule}.")

    records = rows(rp("claim15", "claim15_g2_per_fire.csv"))
    for key in ("coord_rf", "thermal_coord"):
        g5 = c15["g5"][key]
        losses = np.array([[float(r[f"{key}_loss_{m}"]) for m in MEASURES] for r in records])
        checks = []
        for col in ("country", "year", "fire"):
            groups = np.array([r[col] for r in records])
            diffs = (g5["leave_one_fire_out_min_max"] if col == "fire" else g5[f"leave_one_{col}_out"].values())
            checks.append(f"Omit {col}: $\\Delta$ {span(diffs)}, {omitted_loss_range(losses, groups)}.")
        largest = g5["largest_event_removed"]
        event_losses = []
        for r in records:
            if not r["fut_thermal_nolargest"] or not r[f"{key}_fut_nolargest"]:
                continue
            t, c = float(r["fut_thermal_nolargest"]), float(r[f"{key}_fut_nolargest"])
            if not (math.isfinite(t) and math.isfinite(c)):
                continue
            selected = {"t": t, "c": c, "none": min(t, c)}
            event_losses.append([max(t, c) - selected[r[f"{key}_choice_{m}"]] for m in MEASURES])
        assert len(event_losses) == largest["fires"]
        checks.append(f"Largest-event check: $\\Delta$ {f3(largest['mean_diff'])}, "
                      f"$L$ {triple(np.mean(event_losses, axis=0))}, {largest['fires']} fires.")
        add(f"10.2 G5 {PAIR_LABELS[key]}", here, r"\newline ".join(checks))

    matches = " / ".join(str(p["shared_cells"]) for p in pairs_rp)
    add("10.3 G1d Models and grid match", here, f"Exact grid matches: {matches}. "
        r"Pooled choices and later AUC in Table~\ref{tab:s-pairs}. Earlier cAUC and stratified choices: no result file found.")
    countries = jload(COUNTRIES)
    groups = np.array([countries[r["fire"]] for r in records])
    for key in ("coord_rf", "thermal_coord", "thermal_dist", "coord_knn"):
        diff = c15f[key]["leave_one_country_out"]
        losses = np.array([[float(r[f"{key}_loss_{m}"]) for m in MEASURES] for r in records])
        assert set(groups) == diff.keys()
        add(f"10.5 Countries: {PAIR_LABELS[key]}", here,
            f"LSIB leave-one-country-out $\\Delta$ {span(diff.values())}; {omitted_loss_range(losses, groups)}.")
    add("10.5 G1d Half-cell overlap", here, r"Recount with separate denominator in Table~\ref{tab:s-pairs}.")
    d = c15f["thermal_dist_D"]
    add("10.5 Distance hybrid $D$", main, f"$D$ {interval(d['mean'], (d['lo'], d['hi']))} (95\\%); descriptive.")

    counts = jload(RES / "label_counts_11a.json")
    sites = [esc(fire) for fire, d in counts.items() if d["supported"]]
    missing = "Not run (no result file found)"
    add("11.2 Forward selection", missing, f"Support file flags {len(sites)}/{len(counts)} sites. "
        "Plan 11.2a describes a smaller subset after the per-year cell threshold. No fitted selector output.")
    add("11.2 Older-label comparator", missing, "Five-year comparator, ten-year and buffer sensitivities.")
    add("11.3 Sequence simulation", "Not run (replaced by 13.4)", "No result file found for the 11.3 design.")

    for subset in ("primary", "secondary"):
        sample = [r for r in pf16 if r["eligible"] == "True"
                  and (subset == "primary" or r["fire"] in c16["secondary_fires"])]
        for key, label in PAIR_LABELS.items():
            d = c16["rule_10_1"][key][subset]
            choices = " / ".join(str(d[f"{m}_chooses_location"]) for m in ("pooled_auc", "cauc", "saucc"))
            rule = "met" if d["transfer_failure"] else "not met"
            loss = loss_text(sample, key, "late_thermal", key + "_late")
            add(f"11.4 {subset}: {label}", main if subset == "primary" else here,
                f"Choices {choices}; {loss}; $\\Delta$ {interval(d['mean'], d['ci95'])}; Holm $p$ {d['p_holm']:.4f}; rule {rule}.")
        d = c16["rule_9_5"][subset]
        add(f"11.4 {subset}: rule 9.5", main if subset == "primary" else here,
            f"{decision(d, 'mean')}; Holm $p$ {d['p_holm']:.4f}; same choice in {d['same_choice']}/{d['fires']}.")
        prior = sum(int(r["pop_burned_2017_2023"]) for r in sample)
        total = sum(int(r["late_burned"]) + int(r["late_unburned"]) for r in sample)
        add(f"11.4 {subset}: prior burning", here, f"{prior:,}/{total:,} population cells burned in 2017--2023.")

    if SFX:
        old_a = {r["fire"] for r in oa} - {r["fire"] for r in o14["excluded"]}
        old_b = {r["fire"] for r in ob if r["eligible"] == "True"}
        changes = len(inA ^ old_a) + len(inB ^ old_b)
        add("15 Valid-data mask (15.2)", main, f"A removed {V['sQaCellsA']} cells ({V['sQaBurnedA']} burned); "
            f"B removed {V['sQaCellsB']} ({V['sQaBurnedB']} burned); {changes} eligibility changes. "
            r"Label comparison in Table~\ref{tab:s-qa}.")
    return add_rows


# ---------------------------------------------------------------- values.tex
lines = ["% written by build_values.py, do not edit"]
lines += [f"\\newcommand{{\\{k}}}{{{v}}}" for k, v in sorted(V.items())]
(HERE / "values.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")

# ---------------------------------------------------------------- supplementary tables
fires_tab = (HERE / "fires_table_source.tex").read_text(encoding="utf-8")
first = re.search(r"\\begin\{table\}.*?\\end\{table\}", fires_tab, re.S).group(0)
first = first.replace("in the order of the rows of Fig.~1 from the top", "ordered by the AUC of the thermal random forest")
first = first.replace("\\label{tab:s-fires}", "\\label{tab:s-fires}")

esc = lambda s: s.replace("_", "\\_")  # noqa: E731
pB = {r["fire"]: r for r in pf16}
out = [first, ""]
out.append("\\begin{table}[p]\\centering\\caption{Focal-event pooled AUC and AUC on later burning of the thermal "
           "random forest (T) and the coordinate-only random forest (C), per fire. Window A: later burning to the end "
           "of 2023 (primary future population). Window B: January 2024 to September 2026, frozen focal scores. "
           "A dash marks a fire that was not eligible in that window (fewer than 30 later-burned cells).}"
           "\\label{tab:s-perfire}\\footnotesize\\begin{tabular}{lrrrrrr}\\toprule")
out.append("Fire & Focal T & Focal C & A: later T & A: later C & B: later T & B: later C \\\\\\midrule")
a_by = {r["fire"]: r for r in pf14}
for fire in sorted(focal, key=lambda f: -focal[f]["thermal"]):
    fo = focal[fire]
    a = a_by.get(fire)
    b = pB.get(fire)
    ca = (f3(float(a["coord_primary_fut_thermal"])), f3(float(a["coord_primary_fut_cand"]))) if a else ("--", "--")
    cb = (f3(float(b["late_thermal"])), f3(float(b["coord_rf_late"]))) if b and b["eligible"] == "True" else ("--", "--")
    out.append(f"{esc(fire)} & {f3(fo['thermal'])} & {f3(fo['coord_rf'])} & {ca[0]} & {ca[1]} & {cb[0]} & {cb[1]} \\\\")
out.append("\\bottomrule\\end{tabular}\\end{table}")
if CMP:
    out.append("")
    out.append("\\begin{table}[p]\\centering\\caption{Main later-burning results with the original labels, whose "
               "unmapped mask used the land/water bit of the MCD64A1 quality layer, and with the corrected labels of "
               "plan amendment 15, which use the valid-data bit. The corrected results are the ones reported in the "
               "main text. Differences are thermal RF minus candidate; rule is the transfer-failure rule.}"
               "\\label{tab:s-qa}\\footnotesize\\begin{tabular}{L{7.4cm}L{4.2cm}L{4.2cm}}\\toprule")
    out.append("Quantity & Original labels & Corrected labels \\\\\\midrule")
    for (lab, ov), (_, nv) in CMP:
        out.append(f"{lab} & {ov} & {nv} \\\\")
    out.append("\\bottomrule\\end{tabular}\\end{table}")

plan_rows = register_rows()
plan_columns = r"\scriptsize\begin{tabular}{L{5cm}L{3.6cm}L{\dimexpr\linewidth-8.6cm-6\tabcolsep\relax}}\toprule"
plan_header = r"Plan item & Status & Key result \\ \midrule"
out.extend([
    r"\begin{landscape}",
    r"\begin{table}[p]\centering",
    r"\caption{Registered analyses in amendments 9, 10, 11 and 15. Choices, loss ($L$) and relative loss "
    r"use the order pooled AUC, cAUC, stratified cAUC. Choices count fires selecting the location candidate. "
    r"$\Delta$ is thermal minus candidate later AUC, with 95\% intervals where shown. "
    r"Results use the label variant of this build.}\label{tab:s-plan}",
    plan_columns, plan_header,
])
split = next(i for i, (item, _, _) in enumerate(plan_rows) if item.startswith("11.4"))
for index, (item, status, result) in enumerate(plan_rows):
    if index == split:
        out.extend([
            r"\bottomrule\end{tabular}\end{table}\clearpage",
            r"\begin{table}[p]\centering",
            r"{\small Table \ref{tab:s-plan} continued\par\medskip}",
            plan_columns, plan_header,
        ])
    out.append(f"{item} & {status} & {result} \\\\")
out.extend([r"\bottomrule\end{tabular}\end{table}", r"\end{landscape}"])

shared = {(p["earlier"], p["later"]): p for p in c15f["g1d_shared"]}
out.extend([
    r"\begin{table}[p]\centering",
    r"\caption{G1d repeat fires. The earlier fire supplies the training data and the pooled-AUC choice. "
    r"Scored and burned counts describe the later AUC evaluation. The spatial-overlap fraction counts "
    r"later-fire cell centres within half a cell of an earlier-fire cell centre, over all later-fire cells "
    r"in the overlap check.}\label{tab:s-pairs}",
    r"\footnotesize\begin{tabular}{L{3.2cm}llrrrL{1.7cm}rr}\toprule",
    r"Earlier fire & Later fire & Dates & Scored & Burned & Shared / total & Pooled choice "
    r"& \shortstack[r]{Thermal\\AUC} & \shortstack[r]{Coord.\\AUC} \\ \midrule",
])
for p in pairs_rp:
    overlap = shared[p["earlier"], p["later"]]
    dates = r"\shortstack[l]{" + r"\\".join(p["dates"]) + "}"
    choice = {"coord": "Coordinate RF", "thermal": "Thermal RF"}[p["earlier_choice_pooled_auc"]]
    out.append(f"{esc(p['earlier'])} & {esc(p['later'])} & {dates} & {p['later_cells']:,} & "
               f"{p['later_burned']:,} & {overlap['shared_cells_half_cell']:,}/{overlap['later_cells_total']:,} & "
               f"{choice} & {f3(p['later_auc_thermal'])} & {f3(p['later_auc_coord'])} \\\\")
out.append(r"\bottomrule\end{tabular}\end{table}")

(HERE / "supp_selection_tables.tex").write_text("% written by build_values.py, do not edit\n" + "\n".join(out) + "\n",
                                                encoding="utf-8")

# ---------------------------------------------------------------- figures
from matplotlib.lines import Line2D

BLUE, ORANGE = "#2a78d6", "#eb6834"
AQUA, YELLOW, MAGENTA = "#1baf7a", "#eda100", "#e87ba4"
INK, MUTED, GRID = "#1f1f1e", "#6b6b66", "#e4e3de"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 8, "text.color": INK,
    "axes.edgecolor": MUTED, "axes.labelcolor": INK, "axes.linewidth": 0.6,
    "xtick.color": INK, "ytick.color": INK, "pdf.fonttype": 42,
})

WINDOWS = (
    ("Later burning to 2023", "o", INK, INK),
    ("Later burning 2024 to Sep 2026", "s", "none", INK),
)
DOUBLE_COLUMN = 14 / 2.54
PREVIEW = FIG / "preview"
PREVIEW.mkdir(exist_ok=True)


def clean(ax, grid_axis="y"):
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_axisbelow(True)
    ax.grid(axis=grid_axis, color=GRID, lw=0.5)
    ax.tick_params(length=3, width=0.6)


def window_legend(fig, counts=None):
    handles = [
        Line2D([], [], linestyle="none", marker=marker, markersize=5,
               markerfacecolor=face, markeredgecolor=edge,
               label=f"{label} ({counts[i]} fires)" if counts else label)
        for i, (label, marker, face, edge) in enumerate(WINDOWS)
    ]
    fig.legend(handles=handles, loc="upper center", ncol=2, frameon=False,
               handletextpad=0.4, columnspacing=1.3)


def save_figure(fig, name):
    fig.savefig(FIG / f"{name}.pdf")
    fig.savefig(PREVIEW / f"{name}.png", dpi=300)
    plt.close(fig)


# Figure 1: focal AUC difference against later AUC difference, per fire and window
xa = [focal[r["fire"]]["thermal"] - focal[r["fire"]]["coord_rf"] for r in pf14]
ya = [float(r["coord_primary_fut_thermal"]) - float(r["coord_primary_fut_cand"]) for r in pf14]
fb = [r for r in pf16 if r["eligible"] == "True"]
xb = [focal[r["fire"]]["thermal"] - focal[r["fire"]]["coord_rf"] for r in fb]
yb = [float(r["late_thermal"]) - float(r["coord_rf_late"]) for r in fb]

fig, ax = plt.subplots(figsize=(DOUBLE_COLUMN, 3.45))
fig.subplots_adjust(left=0.16, right=0.97, bottom=0.19, top=0.87)
clean(ax, "both")
ax.axhline(0, color=MUTED, lw=0.8)
ax.axvline(0, color=MUTED, lw=0.8)
ax.set_xlim(math.floor((min(xa + xb) - 0.015) / 0.05) * 0.05, 0.05)
ax.set_ylim(-0.28, 0.65)
ax.set_xticks(np.arange(ax.get_xlim()[0], 0.051, 0.05).round(2))
ax.set_yticks(np.arange(-0.2, 0.61, 0.2).round(1))
ax.set_xlabel("Focal-event pooled AUC difference")
ax.set_ylabel("Later-burning AUC difference")
fig.text(0.565, 0.038, "Differences are thermal RF minus coordinate-only RF",
         ha="center")

# Place overlapping markers in display space and link displaced markers to their data positions.
original_points = ax.transData.transform(np.column_stack((xa + xb, ya + yb)))
display_points = original_points.copy()
marker_spacing = 8 * fig.dpi / 72
zero = ax.transData.transform((0, 0))
angles = np.arange(16) * (2 * np.pi / 16)
directions = np.column_stack((np.cos(angles), np.sin(angles)))
for i, point in enumerate(original_points):
    others = np.delete(display_points, i, axis=0)
    if np.min(np.linalg.norm(others - point, axis=1)) >= marker_spacing:
        continue
    # Try the shortest displacement first, keeping the marker inside the axes.
    for radius in np.arange(0.25, 5, 0.25) * marker_spacing:
        options = point + radius * directions
        inside = ((options >= ax.bbox.min + marker_spacing / 2)
                  & (options <= ax.bbox.max - marker_spacing / 2)).all(axis=1)
        clear = (np.linalg.norm(options[:, None] - others, axis=2) >= marker_spacing).all(axis=1)
        same_quadrant = (((options - zero) * (point - zero)) >= 0).all(axis=1)
        valid = options[inside & clear & same_quadrant]
        if len(valid):
            display_points[i] = valid[0]
            break

positions = ax.transData.inverted().transform(display_points)
for source, shifted, moved in zip(zip(xa + xb, ya + yb), positions,
                                  (original_points != display_points).any(axis=1)):
    if moved:
        ax.plot([source[0], shifted[0]], [source[1], shifted[1]], color=MUTED, lw=0.5)
for points, (_, marker, face, edge) in zip(np.split(positions, [len(xa)]), WINDOWS):
    ax.scatter(*points.T, s=25, marker=marker, facecolors=face, edgecolors=edge,
               linewidths=0.85, zorder=3)
window_legend(fig, (len(xa), len(xb)))
save_figure(fig, "Figure_1")

# Figure 2: later AUC difference by candidate and window, with 95% fire-bootstrap intervals
labels = {"Crf": "Coordinate-only RF", "Knn": "Coordinate-only kNN",
          "Tc": "Thermal RF + coordinates", "Td": "Thermal RF + distance\nto training burns"}
fig, ax = plt.subplots(figsize=(DOUBLE_COLUMN, 2.65))
fig.subplots_adjust(left=0.39, right=0.97, bottom=0.21, top=0.85)
clean(ax, "x")
ypos = np.arange(len(labels))[::-1]
for y, tag in zip(ypos, labels):
    for window, offset, (_, marker, face, edge) in zip("AB", (0.17, -0.17), WINDOWS):
        if window == "A":
            result = c15[PAIRS[tag]]["future_diff_thermal_minus_cand"]
            mean, low, high = (result[k] for k in ("mean", "lo", "hi"))
        else:
            result = c16["rule_10_1"][PAIRS[tag]]["primary"]
            mean, (low, high) = result["mean"], result["ci95"]
        ax.errorbar(mean, y + offset, xerr=[[mean - low], [high - mean]],
                    fmt=marker, markersize=4.5, markerfacecolor=face,
                    markeredgecolor=edge, markeredgewidth=0.85,
                    ecolor=MUTED, elinewidth=0.9, capsize=2, zorder=3)
ax.axvline(0, color=MUTED, lw=0.8)
ax.set_yticks(ypos, list(labels.values()))
ax.tick_params(axis="y", length=0, pad=5)
ax.set_ylim(-0.5, len(labels) - 0.5)
ax.set_xticks([-0.05, 0, 0.05, 0.10, 0.15, 0.20])
ax.set_xlim(-0.055, 0.22)
ax.set_xlabel("Later-burning AUC difference\nThermal RF minus candidate")
window_legend(fig)
save_figure(fig, "Figure_2")

# Figure 3: simulation, balanced accuracy of the choice by measure and setting
fig, ax = plt.subplots(figsize=(DOUBLE_COLUMN, 2.65))
fig.subplots_adjust(left=0.14, right=0.98, bottom=0.25, top=0.85)
clean(ax)
settings = [
    ("Ten", "Nominal\n5 km blocks"),
    ("Forty", "Nominal\n20 km blocks"),
    ("Cal", "Tuned to observed fires\n5 km blocks"),
]
measures = [
    ("Auc", "Pooled AUC", AQUA, "o"),
    ("Cauc", "cAUC", YELLOW, "s"),
    ("Sauc", "Stratified cAUC", MAGENTA, "D"),
]
x0 = np.arange(len(settings))
for j, (measure, label, color, marker) in enumerate(measures):
    vals = [float(V[f"sSim{setting}Bal{measure}"]) for setting, _ in settings]
    ax.scatter(x0 + (j - 1) * 0.19, vals, s=35, color=color, marker=marker,
               edgecolors=INK, linewidths=0.65, label=label, zorder=3)
ax.axhline(0.5, color=MUTED, lw=0.9, ls="--")
ax.set_yticks([0.4, 0.5, 0.6, 0.7, 0.8])
ax.set_ylim(0.4, 0.8)
ax.set_xticks(x0, [label for _, label in settings])
ax.set_xlim(-0.5, len(settings) - 0.5)
ax.set_ylabel("Balanced accuracy\nof model choice")
fig.legend(*ax.get_legend_handles_labels(), loc="upper center", ncol=3, frameon=False)
save_figure(fig, "Figure_3")

# Graphical abstract: paired mean AUCs for the focal event and the two later windows
fig, ax = plt.subplots(figsize=(13 / 2.54, 3.05), dpi=300)
fig.subplots_adjust(left=0.15, right=0.98, bottom=0.23, top=0.76)
clean(ax)
panels = [
    ("Focal event\nWindow A fires", "sAFoc"),
    ("Later burning\nto 2023", "sALate"),
    ("Later burning\n2024 to Sep 2026", "sBLate"),
]
for offset, model, suffix, color, marker in (
    (-0.16, "Thermal RF", "Therm", BLUE, "o"),
    (0.16, "Coordinate-only RF", "Coord", ORANGE, "s"),
):
    vals = [float(V[key + suffix]) for _, key in panels]
    points = np.arange(len(panels)) + offset
    ax.scatter(points, vals, s=42, color=color, marker=marker,
               edgecolors=INK, linewidths=0.65, label=model, zorder=3)
    for x, value in zip(points, vals):
        ax.annotate(f"{value:.2f}", (x, value), xytext=(0, 6), textcoords="offset points",
                    ha="center", va="bottom", fontsize=9)
ax.set_xticks(np.arange(len(panels)), [label for label, _ in panels], fontsize=9)
ax.set_xlim(-0.5, len(panels) - 0.5)
ax.set_yticks([0.4, 0.6, 0.8, 1.0], ["0.4", "0.6", "0.8", "1.0"], fontsize=9)
ax.set_ylim(0.4, 1.09)
ax.set_ylabel(f"Mean AUC ({V['sAElig']} and {V['sBElig']} fires,\n{V['sBOverlap']} of them in both)", fontsize=9)
fig.suptitle("Coordinates led on the focal event, then fell behind", fontsize=11, y=0.97)
fig.legend(*ax.get_legend_handles_labels(), loc="upper center", bbox_to_anchor=(0.5, 0.88),
           ncol=2, fontsize=9, frameon=False)
fig.savefig(HERE / "graphical_abstract.png")
plt.close(fig)

# ---------------------------------------------------------------- provenance
stats = {
    "inputs": {str(p.relative_to(REPO) if REPO in p.parents else p.relative_to(HERE.parent)): sha(p) for p in INPUTS},
    "repo_head": repo_commit(REPO),
    "label_variant": "corrected (_qa1)" if SFX else "original",
    "focal_auc_recomputed": {f: {k: round(v, 6) for k, v in d.items()} for f, d in focal.items()},
    "frozen_checks": sorted(checks),
}
(HERE / "manuscript_statistics.json").write_text(json.dumps(stats, indent=1), encoding="utf-8")
print(len(V), "values;", "frozen checks passed:", len([k for k in checks if k in frozen]))
