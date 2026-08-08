#!/usr/bin/env python3
"""Figure 5 - label-blind adaptation compresses every direction toward chance.

Four-AOI decomposition, 12 ordered directions: raw (open circle) -> best-adapted
(arrow head), with the within-region reference as a grey tick. Directions where
adaptation moves AWAY from the within reference (negative recovery, 7/12) are
orange AND dashed; recoveries are blue AND solid, so the class survives
greyscale print where the two hues differ by only ~2.3:1 in luminance.

Split out of the former three-panel conservation figure: 12 direction labels plus a wide AUC
axis need the full column width, and sharing a row with two other panels forced
cramped legends and two-line titles.

Data: paper/figures/data/fig_data.json. Asserts in _conservation_common.py.
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _layout_check import check as layout_check, contrast_ratio
from _conservation_common import (HERE, MM, BLUE, ORANGE, GREY, FS_BODY, FS_TICK,
                          RECOVERY_STYLE, NEGATIVE_STYLE, decomp, neg,
                          dirlabel, style_axes, chance_segment, save)

HUE_ONLY_CONTRAST = contrast_ratio((0x00 / 255, 0x72 / 255, 0xB2 / 255),
                                   (0xE6 / 255, 0x9F / 255, 0x00 / 255))

plt.rcParams.update({"svg.fonttype": "none", "pdf.fonttype": 42})
fig = plt.figure(figsize=(190 * MM, 108 * MM))
ax = fig.add_axes([0.205, 0.175, 0.780, 0.760])

data_artists = []
order = sorted(decomp, key=lambda d: d["raw"])
for y, d in enumerate(order):
    negative = d["best_adapted"] < d["raw"]
    colour = ORANGE if negative else BLUE
    style = NEGATIVE_STYLE if negative else RECOVERY_STYLE
    ax.annotate("", xy=(d["best_adapted"], y), xytext=(d["raw"], y),
                arrowprops=dict(arrowstyle="-|>", color=colour, lw=1.6,
                                linestyle=style, mutation_scale=10,
                                shrinkA=0, shrinkB=0))
    m, = ax.plot(d["raw"], y, marker="o", mfc="white", mec=colour, ms=5.5,
                 mew=1.3, zorder=3)
    tick, = ax.plot([d["within"], d["within"]], [y - 0.30, y + 0.30], color=GREY,
                    lw=2.0, zorder=2)
    data_artists += [(m, f"raw:{d['direction']}"), (tick, f"within:{d['direction']}")]

N = len(order)
data_artists.append((chance_segment(ax, -0.6, N - 0.4), "chance"))

ax.set_yticks(range(N), [dirlabel(d["direction"]) for d in order], fontsize=FS_TICK)
ax.set_xlim(0.28, 0.97)
ax.set_ylim(-2.35, N - 0.35)
ax.set_xticks([0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
ax.set_xlabel("thermal transfer ROC-AUC", fontsize=FS_BODY)
ax.set_title("Label-blind adaptation compresses every direction toward chance",
             fontsize=FS_BODY, loc="left")
style_axes(ax)

hRec = plt.Line2D([], [], color=BLUE, lw=1.8, ls=RECOVERY_STYLE)
hNeg = plt.Line2D([], [], color=ORANGE, lw=1.8, ls=NEGATIVE_STYLE)
hWit = plt.Line2D([], [], color=GREY, lw=0, marker="|", ms=10, mew=2.0)
hCha = plt.Line2D([], [], color="black", lw=0.9, ls=(0, (4, 2)))
ax.legend([hRec, hNeg, hWit, hCha],
          ["recovery (5)", "negative recovery (7)",
           "within-region reference", "chance (0.5)"],
          fontsize=FS_TICK, frameon=False, loc="lower left",
          bbox_to_anchor=(0.0, 0.0), ncol=4, handlelength=1.9,
          columnspacing=1.1, handletextpad=0.5, borderpad=0.0)

print(f"[greyscale] blue-vs-orange hue contrast {HUE_ONLY_CONTRAST:.2f}:1 - "
      f"line style carries the class redundantly")
problems = layout_check(fig, "Fig. 5 - adaptation", min_gap_pt=2.0,
                        min_font_pt=8.0, data_artists=data_artists)
save(fig, "fig5_adaptation", "--preview" in sys.argv)

(HERE / "fig5_provenance.json").write_text(json.dumps({
    "figure": "Fig. 5 - label-blind adaptation compresses toward chance",
    "script": "paper/figures/fig5_adaptation.py",
    "data": "paper/figures/data/fig_data.json (four_aoi_decomposition.csv; sha256 inside)",
    "asserts": "7/12 negative recovery; worst Evia->Manavgat recovered fraction -0.862 "
               "(_conservation_common.py)",
    "greyscale": {
        "hue_only_contrast": round(HUE_ONLY_CONTRAST, 2),
        "note": "Okabe-Ito blue (relative luminance 0.151) vs orange (0.413) separate by only "
                "this ratio, below the 3:1 WCAG non-text minimum, so the two classes also "
                "differ by line style (solid vs dashed); proof in fig5_adaptation_greyscale.png",
    },
    "legend": "in a reserved band below the plotted rows; the chance reference is a segment "
              "over the data rows only, never an axvline, so it cannot cross legend text",
    "canvas_mm": [190, 108],
    "column": "double (190 mm)",
    "font_pt": {"body": FS_BODY, "minimum": FS_TICK},
    "layout_check": f"paper/figures/_layout_check.py; {len(problems)} problems at build time; "
                    f"{len(data_artists)} data artists registered",
    "environment": f"matplotlib {matplotlib.__version__}",
}, indent=1, ensure_ascii=False))
print(f"fig5 written; negative recovery {len(neg)} of {len(decomp)}")
