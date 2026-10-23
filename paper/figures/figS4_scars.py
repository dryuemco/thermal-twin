#!/usr/bin/env python3
"""Fig. S4 - the evaluations of Section 3.3, scar by scar (Additional file 1, 2026-10-23).

One row per burned scar. (a) Thermal ROC-AUC of the same region model scored on the whole region
(A), on a random sample of region cells with the burned share of the scar area (A'), and on the
scar area (B); of a model fitted without the scar (C, leave-one-scar-out); and of models fitted on
each of the other four regions (D, mean and range over the four). (b) The thermal gain (thermal
minus baseline) under A, B, C and D at 5 km blocking, for the seven scars of Table 3. Replaces
former Tables S1, S3, S4, S5 and S26.

Data, under paper/labelfix_rerun/code/ and inference/: matched_holdout.json, prevalence_control.json,
d_per_source.json and ladder_summary.json.
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
SOURCES = ["code/matched_holdout.json", "code/prevalence_control.json", "code/d_per_source.json",
           "inference/ladder_summary.json"]
mh, pc, dps, lad = (load(p) for p in SOURCES)
NAME = {"manavgat_2021": "Manavgat", "bejis_2022": "Bejís", "mugla_2021": "Muğla",
        "evia_2021_extended": "North Evia", "montiferru_2021": "Montiferru"}
MULTI = {"mugla_2021", "montiferru_2021"}
key = lambda r, s: (r, int(s))
P = {key(x["region"], x["scar"]): x for x in pc}
D = {}
for x in dps:
    D.setdefault(key(x["target_region"], x["scar"]), []).append(x["auc"])
G = {key(x["region"], x["scar"]): x for x in lad["scar_frame"]["B10"]["per_scar"]}
rows = []
for x in mh:
    k = key(x["region"], x["scar"])
    assert abs(P[k]["A_region"] - x["A_region_blocked"]) < 1e-9 and abs(P[k]["B_scar_area"] - x["B_seen_same_cells"]) < 1e-9
    assert len(D[k]) == 4 and abs(sum(D[k]) / 4 - x["D_foreign"]) < 6e-5, k
    lab = f"{NAME[x['region']]}" + (f" scar {x['scar']}" if x["region"] in MULTI else "") + f", {x['n']:,} cells"
    rows.append({"k": k, "label": lab, "A": x["A_region_blocked"], "A2": P[k]["A_prime_prevalence_matched"],
                 "B": x["B_seen_same_cells"], "C": x["C_unseen_same_region"], "D": x["D_foreign"],
                 "Dlo": min(D[k]), "Dhi": max(D[k]), "g": G.get(k)})
assert len(rows) == 9 and sum(r["g"] is not None for r in rows) == 7
assert all((r["C"] is None) == (r["g"] is None) for r in rows)

# ---- the numbers the text of Section S2.1 prints ----
m = lambda vals: sum(vals) / len(vals)
A9, A29, B9 = m([r["A"] for r in rows]), m([r["A2"] for r in rows]), m([r["B"] for r in rows])
seven = [r for r in rows if r["g"]]
C7 = m([r["C"] for r in seven])
gm = {g: m([r["g"][g] for r in seven]) for g in ("regionwide_inc", "blk_inc", "loso_inc", "foreign_inc")}
assert [f"{v:.3f}" for v in (A9, A29, B9, C7)] == ["0.791", "0.793", "0.644", "0.546"], (A9, A29, B9, C7)
assert [f"{gm[g]:+.3f}" for g in gm] == ["+0.095", "+0.021", "+0.024", "+0.008"], gm
for g in gm:
    assert abs(gm[g] - lad["scar_frame"]["B10"]["means"][g]) < 1e-4      # per-scar values are stored at 4 dp
allD = [v for vs in D.values() for v in vs]
assert len(allD) == 36 and f"{m(allD):.3f}" == "0.556" and sum(v < 0.5 for v in allD) == 10

S.apply()
fig, (axA, axG) = plt.subplots(1, 2, figsize=(S.WIDTH_MM * S.MM, 82 * S.MM), sharey=True,
                               gridspec_kw={"width_ratios": [1.35, 1.0]})
ys = list(range(len(rows)))[::-1]
MK = {"A": ("o", S.INK, S.INK), "A2": ("o", "white", S.GREY), "B": ("s", S.BLUE, S.BLUE),
      "C": ("^", S.VERMILLION, S.VERMILLION), "D": ("D", S.GREY, S.GREY)}
arts, xa, xg = [], [], []
axA.axvline(0.5, color=S.RULE, lw=0.8, zorder=0)
axG.axvline(0.0, color=S.RULE, lw=0.8, zorder=0)
for r, y in zip(rows, ys):
    rng, = axA.plot([r["Dlo"], r["Dhi"]], [y, y], color=S.GREY, lw=0.8, zorder=1)
    arts.append((rng, f"{r['label']}:Drange")); xa += [r["Dlo"], r["Dhi"]]
    for k in ("A", "A2", "B", "C", "D"):
        if r[k] is None:
            continue
        mk, fc, ec = MK[k]
        p, = axA.plot(r[k], y, mk, ms=4.6, mfc=fc, mec=ec, mew=0.9, zorder=3)
        arts.append((p, f"{r['label']}:{k}")); xa.append(r[k])
    if r["g"]:
        for k, gk in (("A", "regionwide_inc"), ("B", "blk_inc"), ("C", "loso_inc"), ("D", "foreign_inc")):
            mk, fc, ec = MK[k]
            p, = axG.plot(r["g"][gk], y, mk, ms=4.6, mfc=fc, mec=ec, mew=0.9, zorder=3)
            arts.append((p, f"{r['label']}:g{k}")); xg.append(r["g"][gk])
axA.set_xlim(0.35, 0.95); axA.set_xticks([0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
axG.set_xlim(-0.2, 0.2); axG.set_xticks([-0.15, 0, 0.15], ["−0.15", "0", "+0.15"])
axA.set_title("(a) Thermal ROC-AUC"); axG.set_title("(b) Thermal gain, 5 km blocking")
axA.set_xlabel("ROC-AUC"); axG.set_xlabel("thermal minus baseline ROC-AUC")
for ax in (axA, axG):
    ax.tick_params(axis="y", length=0); ax.spines["left"].set_visible(False)
axA.set_yticks(ys, [r["label"] for r in rows]); axA.set_ylim(-0.6, len(rows) - 0.4)
assert_inside(axA, "Fig. S4a", xs=xa); assert_inside(axG, "Fig. S4b", xs=xg)
h = lambda k, lab: Line2D([], [], marker=MK[k][0], ls="", ms=4.6, mfc=MK[k][1], mec=MK[k][2], mew=0.9, label=lab)
fig.legend(handles=[h("A", "A  whole region"), h("A2", "A′  burned share of the scar"), h("B", "B  scar area"),
                    h("C", "C  scar withheld"),
                    Line2D([], [], marker="D", ms=4.6, color=S.GREY, lw=0.8, label="D  other regions, mean and range")],
           loc="upper left", bbox_to_anchor=(0.005, 0.995), ncol=3, handletextpad=0.3, columnspacing=1.0)
fig.subplots_adjust(left=0.245, right=0.975, top=0.79, bottom=0.13, wspace=0.08)
problems = layout_check(fig, "Fig. S4 - scars", min_gap_pt=2.0, min_font_pt=8.0, data_artists=arts)
S.save(fig, HERE, "figS4_scars")
fig.savefig(HERE / "figS4_scars.png", dpi=300)
(HERE / "figS4_provenance.json").write_text(json.dumps({
    "figure": "Fig. S4 - the evaluations of Section 3.3, scar by scar",
    "script": "paper/figures/figS4_scars.py",
    "data": {p: hashlib.sha256((LR / p).read_bytes()).hexdigest() for p in SOURCES},
    "asserts": "A and B agree between matched_holdout and prevalence_control; D is the mean of its four "
               "sources; nine-scar means 0.791 (A), 0.793 (A'), 0.644 (B), seven-scar C 0.546; gains +0.095, "
               "+0.021, +0.024, +0.008 equal the ladder means; 36 foreign scores, mean 0.556, ten below chance",
    "canvas_mm": [S.WIDTH_MM, 82],
    "layout_check": f"paper/figures/_layout_check.py; {len(problems)} problems at build time",
    "environment": f"matplotlib {matplotlib.__version__}",
}, indent=1, ensure_ascii=False), encoding="utf-8")
print("figS4 written")
TEXT = " ".join((HERE.parent / "supplementary.md").read_text(encoding="utf-8").split())
for s in ("Fig. S4", "0.793 against 0.791", "+0.095", "+0.021", "+0.024", "+0.008"):
    assert s in TEXT, f"Section S2.1 must state {s}"
