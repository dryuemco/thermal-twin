#!/usr/bin/env python3
"""Fig. S2 - mean cross-region transfer under every check (Additional file 1, 2026-10-23).

Rows share two panels: (a) mean thermal transfer ROC-AUC over the twenty directions (twelve without
Manavgat), (b) the mean paired thermal gain in transfer, thermal minus baseline, with its
pair-cluster 95% interval where one was computed. The ten-seed row is a range, not an interval.
For the feature sets the gain is measured against the baseline-only model. This figure replaces
former Tables S23 and S25 and the transfer rows of former Tables S21 and S35.

Data, under paper/labelfix_rerun/: code/transfer_delta_ci.json (reference), round8/r8l_summary.json
(classifiers), round8/r8a_summary.json (seeds), round7/sklearn152/compare_vs_1_9_0.json,
round3/no_coord_channels.json (feature sets), round8/r8m_summary.json (VNP64A1),
round8/r8j_summary.json (WorldCover 2020), labels/r2_history.json (earlier burning),
geometry/a4_summary.json (target cells chosen without labels), round8/r8d_summary.json.
"""
import hashlib
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _layout_check import check as layout_check, assert_inside
import _style as S

LR = HERE.parent / "labelfix_rerun"
load = lambda p: json.loads((LR / p).read_text(encoding="utf-8"))
SOURCES = ["code/transfer_delta_ci.json", "round8/r8l_summary.json", "round8/r8a_summary.json",
           "round7/sklearn152/compare_vs_1_9_0.json", "round3/no_coord_channels.json",
           "round8/r8m_summary.json", "round8/r8j_summary.json", "labels/r2_history.json",
           "geometry/a4_summary.json", "round8/r8d_summary.json"]
tdc, r8l, r8a, skl, ncc, r8m, r8j, r2, a4, r8d = (load(p) for p in SOURCES)

cap = r8l["model_capacity"]
ref_gain = tdc["results"]["as drawn"]
REF_T, REF_G = cap["rf_canonical_thermal"]["mean"], ref_gain["mean"]
assert abs(cap["rf_canonical_increment"]["mean"] - REF_G) < 1e-6
assert f"{REF_T:.3f}" == "0.527" and f"{REF_G:+.3f}" == "+0.007"
tr = ncc["tradeoff"]
BASE_T = tr["baseline_only"]["mean_transfer_auc"]
fr = {f["frame"]: f for f in a4["frames"]}
assert abs(fr["ref_full_full"]["mean_thermal"] - REF_T) < 1e-9
seed_t, seed_g = r8a["frames"]["full"]["mean_thermal_range_over_seeds"], r8a["frames"]["full"]["mean_delta_range_over_seeds"]
wm = r8d["without_manavgat_transfer"]["full"]
ex = r2["transfer"]["excluded"]["summary"]

# (label, mean transfer or (lo, hi), gain or (lo, hi), gain interval or None)
GROUPS = [
    ("As drawn", [("Random forest of the main text", REF_T, REF_G, ref_gain["B1000"]["ci_pair_cluster"])]),
    ("Classifier and software", [
        ("Random forest, depth 6, leaf 50", cap["rf_shallow_thermal"]["mean"], cap["rf_shallow_increment"]["mean"],
         cap["rf_shallow_increment"]["pair_cluster_ci95"]),
        ("Random forest, leaf 200", cap["rf_leaf200_thermal"]["mean"], cap["rf_leaf200_increment"]["mean"],
         cap["rf_leaf200_increment"]["pair_cluster_ci95"]),
        ("Penalised logistic regression", cap["logistic_thermal"]["mean"], cap["logistic_increment"]["mean"],
         cap["logistic_increment"]["pair_cluster_ci95"]),
        ("Ten random-forest seeds (range)", tuple(seed_t), tuple(seed_g), None),
        ("scikit-learn 1.5.2 instead of 1.9.0", skl["full/full"]["mean_thermal_152_190"][0],
         skl["full/full"]["mean_delta_152_190"][0], None),
    ]),
    ("Predictors", [
        ("Baseline and the two anomaly channels", tr["anomaly_only"]["mean_transfer_auc"],
         tr["anomaly_only"]["mean_transfer_auc"] - BASE_T, None),
        ("Baseline and the four absolute channels", tr["absolute_only"]["mean_transfer_auc"],
         tr["absolute_only"]["mean_transfer_auc"] - BASE_T, None),
        ("Coordinate-informed channels removed", tr["no_coord_channels"]["mean_transfer_auc"],
         tr["no_coord_channels"]["mean_transfer_auc"] - BASE_T, None),
    ]),
    ("Labels and land cover", [
        ("Labels from VNP64A1", r8m["transfer_vnp"]["mean_thermal"], r8m["transfer_vnp"]["mean_delta"], None),
        ("Land cover from WorldCover 2020", r8j["transfer_2020"]["mean_thermal"], r8j["transfer_2020"]["mean_delta"], None),
        ("Cells burned in prior 5 years removed", ex["mean_thermal"], ex["mean_delta"], None),
    ]),
    ("Target cells, chosen without target labels", [
        ("Inside the source's predictor range", fr["a1_trim_srcfull"]["mean_thermal"],
         fr["a1_trim_srcfull"]["mean_delta"], fr["a1_trim_srcfull"]["delta_pair_cluster"]),
        ("Inside the source's area of applicability", fr["a2_aoa_srcfull"]["mean_thermal"],
         fr["a2_aoa_srcfull"]["mean_delta"], fr["a2_aoa_srcfull"]["delta_pair_cluster"]),
        ("20 km square at the study-area centre", fr["b_win20_win20"]["mean_thermal"],
         fr["b_win20_win20"]["mean_delta"], fr["b_win20_win20"]["delta_pair_cluster"]),
    ]),
    ("Regions", [("Without Manavgat (12 directions)", wm["mean_thermal_without_manavgat"],
                  wm["mean_delta_without_manavgat"], None)]),
]
assert abs(tr["baseline_only"]["mean_transfer_auc"] - 0.5193836) < 1e-6

# ---- the statements of Section S1.2, asserted ----
pts = [(lab, t) for _, rows in GROUPS[1:] for lab, t, _, _ in rows if not isinstance(t, tuple)]
lo = min(pts, key=lambda x: x[1]); hi = max(pts, key=lambda x: x[1])
assert (lo[0], f"{lo[1]:.3f}") == ("Penalised logistic regression", "0.481"), lo
assert (hi[0], f"{hi[1]:.3f}") == ("Without Manavgat (12 directions)", "0.566"), hi
cis = [ci for _, rows in GROUPS for _, _, _, ci in rows if ci]
assert len(cis) == 7 and all(c[0] < 0 < c[1] for c in cis), "every gain interval includes zero"
assert [f"{v:.3f}" for v in seed_t] == ["0.525", "0.530"] and [f"{v:+.3f}" for v in seed_g] == ["+0.005", "+0.008"]

# ---- figure ----
S.apply()
rows, ticks, y = [], [], 0.0
for gname, grows in GROUPS:
    ticks.append((y, gname, True)); y -= 1.0
    for lab, t, g, ci in grows:
        rows.append((y, lab, t, g, ci)); ticks.append((y, lab, False)); y -= 1.0
    y -= 0.35
fig, (axT, axG) = plt.subplots(1, 2, figsize=(S.WIDTH_MM * S.MM, 124 * S.MM), sharey=True)
arts, xt, xg = [], [], []
axT.axvline(0.5, color=S.RULE, lw=0.8, zorder=0); axT.axvline(REF_T, color=S.RULE, lw=0.6, ls=(0, (2, 2)), zorder=0)
axG.axvline(0.0, color=S.RULE, lw=0.8, zorder=0); axG.axvline(REF_G, color=S.RULE, lw=0.6, ls=(0, (2, 2)), zorder=0)
for yy, lab, t, g, ci in rows:
    for ax, v, xs in ((axT, t, xt), (axG, g, xg)):
        if isinstance(v, tuple):
            a, = ax.plot(v, [yy, yy], color=S.BLUE, lw=3.2, solid_capstyle="butt", zorder=2)
            xs += list(v)
        else:
            a, = ax.plot(v, yy, "o", ms=4.6, color=S.BLUE, zorder=3)
            xs.append(v)
        arts.append((a, f"{lab}:{ax is axG}"))
    if ci:
        w, = axG.plot(ci, [yy, yy], color=S.BLUE, lw=1.0, zorder=2)
        arts.append((w, f"{lab}:ci")); xg += list(ci)
axT.set_xlim(0.46, 0.60); axT.set_xticks([0.46, 0.50, 0.54, 0.58])
axG.set_xlim(-0.07, 0.07); axG.set_xticks([-0.06, -0.03, 0, 0.03, 0.06], ["−0.06", "−0.03", "0", "+0.03", "+0.06"])
axT.set_title("(a) Mean transfer"); axG.set_title("(b) Thermal gain in transfer")
axT.set_xlabel("ROC-AUC"); axG.set_xlabel("thermal minus baseline ROC-AUC")
for ax in (axT, axG):
    ax.tick_params(axis="y", length=0); ax.spines["left"].set_visible(False)
axT.set_yticks([t[0] for t in ticks], [t[1] for t in ticks])
for lab, (_, _, head) in zip(axT.get_yticklabels(), ticks):
    if head:
        lab.set_color(S.MUTED); lab.set_fontstyle("italic")
axT.set_ylim(y + 0.35 - 0.4, 0.6)
assert_inside(axT, "Fig. S2a", xs=xt); assert_inside(axG, "Fig. S2b", xs=xg)
fig.legend(handles=[Line2D([], [], marker="o", ls="", ms=4.6, color=S.BLUE, label="mean"),
                    Line2D([], [], color=S.BLUE, lw=1.0, label="95% interval"),
                    Line2D([], [], color=S.BLUE, lw=3.2, label="range over seeds"),
                    Line2D([], [], color=S.RULE, lw=0.6, ls=(0, (2, 2)), label="as drawn")],
           loc="upper left", bbox_to_anchor=(0.005, 0.995), ncol=4, handletextpad=0.4, columnspacing=1.2)
fig.subplots_adjust(left=0.37, right=0.98, top=0.89, bottom=0.09, wspace=0.10)
problems = layout_check(fig, "Fig. S2 - transfer checks", min_gap_pt=2.0, min_font_pt=8.0, data_artists=arts)
S.save(fig, HERE, "figS2_transfer_checks")
fig.savefig(HERE / "figS2_transfer_checks.png", dpi=300)
(HERE / "figS2_provenance.json").write_text(json.dumps({
    "figure": "Fig. S2 - mean cross-region transfer under every check",
    "script": "paper/figures/figS2_transfer_checks.py",
    "data": {p: hashlib.sha256((LR / p).read_bytes()).hexdigest() for p in SOURCES},
    "asserts": "reference 0.527 and +0.007 agree across three outputs; the lowest check is the penalised "
               "logistic regression (0.481) and the highest the twelve directions without Manavgat (0.566); "
               "all seven gain intervals include zero; seed ranges 0.525-0.530 and +0.005 to +0.008",
    "canvas_mm": [S.WIDTH_MM, 124],
    "layout_check": f"paper/figures/_layout_check.py; {len(problems)} problems at build time",
    "environment": f"matplotlib {matplotlib.__version__}",
}, indent=1, ensure_ascii=False), encoding="utf-8")
print("figS2 written;", len(rows), "rows")
TEXT = " ".join((HERE.parent / "supplementary.md").read_text(encoding="utf-8").split())
for s in ("from 0.481", "to 0.566", "Fig. S2"):
    assert s in TEXT, f"Section S1.2 must state {s}"
