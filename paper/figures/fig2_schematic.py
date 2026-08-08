#!/usr/bin/env python3
"""Figure 2 - methods schematic.

Data flow from source products to the transfer/diagnostic programme, annotated with
the Methods subsection that specifies each stage. No numbers -> no numeric asserts;
box labels are tied to 03_methods section numbering (checked by eye at assembly).
Okabe-Ito accents, greyscale-safe, vector, min font 7 pt.
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

HERE = Path(__file__).resolve().parent
BLUE, ORANGE, GREYBOX = "#0072B2", "#E69F00", "#F0F0F0"

MM = 1 / 25.4
fig, ax = plt.subplots(figsize=(190 * MM, 84 * MM))
plt.rcParams.update({"svg.fonttype": "none", "pdf.fonttype": 42})
ax.set_xlim(0, 100)
ax.set_ylim(0, 56)
ax.axis("off")


def box(x, y, w, h, text, fc=GREYBOX, ec="#888888", fs=7, weight="normal",
        tc="black"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.6",
                                facecolor=fc, edgecolor=ec, linewidth=0.8))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            fontweight=weight, color=tc)


def arrow(x1, y1, x2, y2, color="#555555"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=9, lw=1.1, color=color,
                                 shrinkA=1, shrinkB=1))


# column 1 - inputs
box(1, 44, 20, 9, "MCD64A1 burned area\n(label; §3.2)")
box(1, 30, 20, 11, "Landsat LST/NDVI,\nMODIS LST + TVDI,\ndownscaling & fusion\n(§3.4)")
box(1, 18, 20, 9, "DEM, slope,\nESA WorldCover (§3.4)")

# column 2 - grid, gate, population
box(27, 37, 21, 10, "~510 m cell grid\n(17×17 @ 30 m; §3.2)")
box(27, 24, 21, 9, "burned-landcover\ngate (§3.3)")
box(27, 11, 21, 9, "primary population:\nnatural vegetation (§3.5)")
for y in (48.5, 35.5, 22.5):
    pass
arrow(21, 48.5, 27, 43)
arrow(21, 35.5, 27, 41)
arrow(21, 22.5, 27, 40)
arrow(37.5, 37, 37.5, 33)
arrow(37.5, 24, 37.5, 20)

# column 3 - models
box(54, 40, 22, 12,
    "feature sets (§3.6):\nstatic baseline\nvs + 6 thermal", fc="#E8F1F8",
    ec=BLUE)
box(54, 24, 22, 10, "within-region:\nRF + spatial-block CV,\nblock robustness (§3.7–3.9)")
box(54, 8, 22, 10, "transfer: source-only,\n20 ordered directions;\nz-score / CORAL (§3.10–3.11)")
arrow(48, 15.5, 54, 14)
arrow(65, 40, 65, 34)
arrow(65, 24, 65, 18)

# column 4 - outputs / diagnostics
box(82, 40, 17, 12, "ΔAUC within,\n5 regions ×\n3 block sizes", fc="#FFFFFF",
    ec="#555555")
box(82, 22, 17, 12,
    "diagnostics (§3.14):\nP(x) · P(x|y=1) ·\nP(y) · P(y|x)", fc="#FDF3E0",
    ec=ORANGE)
box(82, 5, 17, 11, "interventions (§3.15):\nLORO pooling,\nfeature removal")
arrow(76, 29, 82, 46)
arrow(76, 13, 82, 28)
arrow(76, 11, 82, 10)

ax.text(1, 54.8, "Fig. 2  Pipeline and evaluation programme (section numbers = Methods)",
        fontsize=8, fontweight="bold", va="center")

fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
fig.savefig(HERE / "fig2_schematic.pdf")
fig.savefig(HERE / "fig2_schematic.svg")
if "--preview" in sys.argv:
    fig.savefig(HERE / "fig2_schematic_preview.png", dpi=220)

(HERE / "fig2_provenance.json").write_text(json.dumps({
    "figure": "Fig. 2 - methods schematic",
    "script": "paper/figures/fig2_schematic.py",
    "data": "none (schematic; labels mirror 03_methods section numbering)",
    "asserts": "none (no numbers)",
    "palette": "Okabe-Ito accents on grey; no red-green",
    "min_font_pt": 7.0,
    "environment": f"matplotlib {matplotlib.__version__}",
}, indent=1))
print("fig2 written")
