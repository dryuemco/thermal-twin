#!/usr/bin/env python3
"""Figure 6b - pooled multi-region training never beats the best single source.

Leave-one-region-out: for each held-out target, the pooled model (orange circle)
against the best pairwise source (open blue diamond), with the within-region
ceiling as a grey tick. The pooled point is left of the pairwise point in every
one of the five targets - asserted, not merely drawn.

Split out of the former three-panel Fig. 6 so the panel gets the full column
width; at ~34 mm it needed a two-line title and its legend overflowed the axes.

Data: paper/figures/data/fig_data.json. Asserts in _fig6_common.py.
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _layout_check import check as layout_check
from _fig6_common import (HERE, MM, BLUE, ORANGE, GREY, FS_BODY, FS_TICK,
                          LABEL, loro, style_axes, chance_segment, save)

plt.rcParams.update({"svg.fonttype": "none", "pdf.fonttype": 42})
fig = plt.figure(figsize=(190 * MM, 78 * MM))
ax = fig.add_axes([0.135, 0.215, 0.850, 0.700])

data_artists = []
ys = list(range(len(loro)))[::-1]
for r, y in zip(loro, ys):
    ax.plot([r["loro_raw"], r["best_pairwise"]], [y, y], color="#BBBBBB", lw=1.2,
            zorder=1)
    mp, = ax.plot(r["best_pairwise"], y, marker="D", mfc="white", mec=BLUE,
                  ms=6.0, mew=1.3, zorder=3)
    ml, = ax.plot(r["loro_raw"], y, marker="o", mfc=ORANGE, mec=ORANGE, ms=6.0,
                  zorder=3)
    tb, = ax.plot([r["within"], r["within"]], [y - 0.24, y + 0.24], color=GREY,
                  lw=2.0, zorder=2)
    data_artists += [(mp, f"pairwise:{r['target']}"), (ml, f"loro:{r['target']}"),
                     (tb, f"within:{r['target']}")]

N = len(loro)
data_artists.append((chance_segment(ax, -0.55, N - 0.45), "chance"))

ax.set_yticks(ys, [LABEL[r["target"]] for r in loro], fontsize=FS_BODY)
ax.set_xlim(0.35, 0.99)
ax.set_ylim(-1.85, N - 0.4)
ax.set_xticks([0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
ax.set_xlabel("thermal ROC-AUC on the held-out target", fontsize=FS_BODY)
ax.set_title("Pooling every other region never beats the best single source",
             fontsize=FS_BODY, loc="left")
style_axes(ax)

hL = plt.Line2D([], [], marker="o", color=ORANGE, ls="", ms=6.0)
hP = plt.Line2D([], [], marker="D", mfc="white", mec=BLUE, ls="", ms=6.0, mew=1.3)
hW = plt.Line2D([], [], color=GREY, lw=0, marker="|", ms=10, mew=2.0)
hC = plt.Line2D([], [], color="black", lw=0.9, ls=(0, (4, 2)))
ax.legend([hL, hP, hW, hC],
          ["LORO pooled", "best pairwise source", "within-region ceiling",
           "chance (0.5)"],
          fontsize=FS_TICK, frameon=False, loc="lower left",
          bbox_to_anchor=(0.0, 0.0), ncol=4, handlelength=1.6,
          columnspacing=1.8, handletextpad=0.6, borderpad=0.0)

problems = layout_check(fig, "Fig. 6b - LORO pooling", min_gap_pt=2.0,
                        min_font_pt=8.0, data_artists=data_artists)
save(fig, "fig6b_loro", "--preview" in sys.argv)

(HERE / "fig6b_provenance.json").write_text(json.dumps({
    "figure": "Fig. 6b - pooled (LORO) training never beats the best single source",
    "script": "paper/figures/fig6b_loro.py",
    "data": "paper/figures/data/fig_data.json (loro_pooled_transfer.json; sha256 inside)",
    "asserts": "loro_raw < best_pairwise for all five targets; Manavgat pooled 0.469 "
               "(_fig6_common.py)",
    "legend": "in a reserved band below the plotted rows; chance drawn as a segment over the "
              "data rows only",
    "canvas_mm": [190, 78],
    "column": "double (190 mm)",
    "font_pt": {"body": FS_BODY, "minimum": FS_TICK},
    "layout_check": f"paper/figures/_layout_check.py; {len(problems)} problems at build time; "
                    f"{len(data_artists)} data artists registered",
    "environment": f"matplotlib {matplotlib.__version__}",
}, indent=1, ensure_ascii=False))
print("fig6b written; LORO below best pairwise in all", len(loro), "targets")
