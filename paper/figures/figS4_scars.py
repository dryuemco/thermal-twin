#!/usr/bin/env python3
"""Fig. S4 - the evaluations of Section 3.3, scar by scar (Online Resource 1, redrawn 2026-10-25).

Two panels with the same layout. The horizontal axis runs through the four evaluations of Section 3.3
in order (A whole region, B scar area, C scar withheld, D other regions). Each thin grey line is one
burned scar and the dark line is the mean, whose value is printed under each design. (a) Thermal ROC-AUC for the nine scars (seven have a row C).
(b) The thermal gain (thermal minus baseline) at 5 km blocking for the seven scars of Table 3.

The 2026-10-23 version drew five marker types per scar row (A, A', B, C, D with its range) and the
authors found it too dense. The prevalence-matched control A' is no longer drawn. Its nine-scar mean is
stated in Section S2.1 and asserted below, as before.

Data, under paper/labelfix_rerun/code/ and inference/, are matched_holdout.json, prevalence_control.json,
d_per_source.json and ladder_summary.json.
"""
import hashlib
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.patheffects as pe
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
D9 = m([r["D"] for r in rows])
gm = {g: m([r["g"][g] for r in seven]) for g in ("regionwide_inc", "blk_inc", "loso_inc", "foreign_inc")}
assert [f"{v:.3f}" for v in (A9, A29, B9, C7)] == ["0.791", "0.793", "0.644", "0.546"], (A9, A29, B9, C7)
assert [f"{gm[g]:+.3f}" for g in gm] == ["+0.095", "+0.021", "+0.024", "+0.008"], gm
for g in gm:
    assert abs(gm[g] - lad["scar_frame"]["B10"]["means"][g]) < 1e-4      # per-scar values are stored at 4 dp
allD = [v for vs in D.values() for v in vs]
assert len(allD) == 36 and f"{m(allD):.3f}" == "0.556" and sum(v < 0.5 for v in allD) == 10
assert f"{D9:.3f}" == "0.556"                                              # four sources per scar, so equal

# ---- drawing ----
S.apply()
DESIGNS = ["A", "B", "C", "D"]
TICKS = ["A\nwhole\nregion", "B\nscar\narea", "C\nscar\nwithheld", "D\nother\nregions"]
GAIN = {"A": "regionwide_inc", "B": "blk_inc", "C": "loso_inc", "D": "foreign_inc"}
SCAR = dict(color="#B4B4B4", lw=0.8, marker="o", ms=2.6, mfc="#B4B4B4", mec="#B4B4B4", zorder=2)
MEAN = dict(color=S.INK, lw=1.6, marker="o", ms=5.2, mfc=S.INK, mec="white", mew=0.8, zorder=4)
halo = [pe.withStroke(linewidth=2.2, foreground="white")]

fig, (axA, axG) = plt.subplots(1, 2, figsize=(S.WIDTH_MM * S.MM, 86 * S.MM),
                               gridspec_kw={"width_ratios": [1.0, 1.0]})
arts, ya, yg = [], [], []


def draw(ax, series, means, fmt, ys):
    """One grey polyline per scar (broken where a design is missing) and the mean on top. The mean
    values go under the design names, so no label sits on a line."""
    for name, vals in series:
        seg = []
        for i, v in enumerate(vals + [None]):
            if v is None:
                if seg:
                    ln, = ax.plot([p[0] for p in seg], [p[1] for p in seg], **SCAR)
                    arts.append((ln, name))
                seg = []
            else:
                seg.append((i, v)); ys.append(v)
    ln, = ax.plot(range(4), means, **MEAN)
    arts.append((ln, "mean"))
    ax.set_xticks(range(4), [lab + "\n" + fmt(v) for lab, v in zip(TICKS, means)])
    ax.set_xlim(-0.35, 3.35)
    ax.tick_params(axis="x", length=0)


S.chance(axA, 0.5, axis="y")
draw(axA, [(r["label"], [r[d] for d in DESIGNS]) for r in rows], [A9, B9, C7, D9], lambda v: f"{v:.3f}", ya)
axA.set_ylim(0.38, 0.92); axA.set_yticks([0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
axA.set_ylabel("thermal ROC-AUC")
axA.set_title("(a) ROC-AUC, nine scars")

S.chance(axG, 0.0, axis="y")
draw(axG, [(r["label"], [r["g"][GAIN[d]] for d in DESIGNS]) for r in seven],
     [gm[GAIN[d]] for d in DESIGNS], lambda v: f"{v:+.3f}", yg)
axG.set_ylim(-0.2, 0.2); axG.set_yticks([-0.15, 0, 0.15], ["−0.15", "0", "+0.15"])
axG.set_ylabel("thermal minus baseline ROC-AUC")
axG.set_title("(b) Thermal gain, seven scars")

fig.legend(handles=[Line2D([], [], **{k: v for k, v in SCAR.items() if k != "zorder"}, label="one scar"),
                    Line2D([], [], **{k: v for k, v in MEAN.items() if k != "zorder"},
                           label="mean (value under each design)")],
           loc="upper right", bbox_to_anchor=(0.995, 0.999), ncol=2, handlelength=2.2, columnspacing=1.2)
assert_inside(axA, "Fig. S4a", ys=ya); assert_inside(axG, "Fig. S4b", ys=yg)
fig.subplots_adjust(left=0.075, right=0.985, top=0.86, bottom=0.215, wspace=0.28)
problems = layout_check(fig, "Fig. S4 - scars", min_gap_pt=2.0, min_font_pt=8.0, data_artists=arts)
S.save(fig, HERE, "figS4_scars")
fig.savefig(HERE / "figS4_scars.png", dpi=300)
(HERE / "figS4_provenance.json").write_text(json.dumps({
    "figure": "Fig. S4 - the evaluations of Section 3.3, scar by scar",
    "script": "paper/figures/figS4_scars.py",
    "data": {p: hashlib.sha256((LR / p).read_bytes()).hexdigest() for p in SOURCES},
    "asserts": "A and B agree between matched_holdout and prevalence_control; D is the mean of its four "
               "sources; nine-scar means 0.791 (A), 0.793 (A'), 0.644 (B), 0.556 (D), seven-scar C 0.546; gains "
               "+0.095, +0.021, +0.024, +0.008 equal the ladder means; 36 foreign scores, mean 0.556, ten below chance",
    "design": "2026-10-25 redraw, one grey line per scar across the four evaluations and the mean in dark ink; "
              "A' and the range of D are stated in Section S2.1 and no longer drawn",
    "canvas_mm": [S.WIDTH_MM, 86],
    "layout_check": f"paper/figures/_layout_check.py; {len(problems)} problems at build time",
    "environment": f"matplotlib {matplotlib.__version__}",
}, indent=1, ensure_ascii=False), encoding="utf-8")
print("figS4 written")
TEXT = " ".join((HERE.parent / "supplementary.md").read_text(encoding="utf-8").split())
for s in ("Fig. S4", "0.793 against 0.791", "+0.095", "+0.021", "+0.024", "+0.008"):
    assert s in TEXT, f"Section S2.1 must state {s}"
