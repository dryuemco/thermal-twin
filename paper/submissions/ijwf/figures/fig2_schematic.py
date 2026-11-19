#!/usr/bin/env python3
"""Figure 2 for the IJWF package: the methods schematic without Methods section numbers.

A copy of paper/figures/fig2_schematic.py, which is left as it is. The IJWF manuscript has unnumbered
headings (CSIRO template), so the small grey section numbers of the shared figure are not drawn and
the boxes are lower by the height of that line. The look, the box texts and the connectors are the
same. The layout check is imported from paper/figures and the style from _style_ijwf.py, which loads
the shared style with the sizes of the publisher's figure guide: 8 pt box titles and 7 pt box lines
(2026-11-11; 9 pt and 8 pt before). Each entry of a box now starts with a capital letter (sentence
case); a line that continues the entry above it keeps its lower case.

Run:  python paper/submissions/ijwf/figures/fig2_schematic.py
Writes fig2_schematic.pdf, .svg and _preview.png next to this file.
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
from matplotlib.path import Path as MplPath

sys.dont_write_bytecode = True                    # nothing is written into paper/figures, not even bytecode
HERE = Path(__file__).resolve().parent
SHARED = HERE.parents[2] / "figures"
sys.path[:0] = [str(HERE), str(SHARED)]
from _layout_check import check as layout_check   # noqa: E402
import _style_ijwf as S                           # noqa: E402

EDGE = "#9A9A9A"
CTRL = "#767676"   # Kozan 2023, as in Fig. 1

caps = (HERE.parent / "text" / "figure_captions.tex").read_text(encoding="utf-8")
cap2 = " ".join(caps[caps.index("fig2_schematic.pdf"):caps.index(r"\label{fig:pipeline}")].split())
assert "Section" not in cap2 and "grey numbers" not in cap2, "the IJWF caption of Fig. 2 still cites sections"

S.apply()
W_MM, H_MM = S.WIDTH_MM, 50.0
fig = plt.figure(figsize=(W_MM * S.MM, H_MM * S.MM))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W_MM)          # 1 axis unit == 1 mm on the page
ax.set_ylim(0, H_MM)
ax.axis("off")

_boxes = []   # (text_artist, patch_artist, label) for the containment check


def box(x, y, w, h, title, lines, line_colours=None):
    p = Rectangle((x, y), w, h, facecolor="white", edgecolor=EDGE, linewidth=0.7, zorder=1)
    ax.add_patch(p)
    t = ax.text(x + 2.2, y + h - 2.2, title, ha="left", va="top", fontsize=S.FS_BODY, zorder=4)
    _boxes.append((t, p, title))
    yy = y + h - 8.4
    for i, line in enumerate(lines):
        c = (line_colours or {}).get(i, S.INK)
        tl = ax.text(x + 2.2, yy, line, ha="left", va="top", fontsize=S.FS_SMALL, color=c, zorder=4)
        _boxes.append((tl, p, line))
        yy -= 4.1
    return p


def arrow(points):
    ax.add_patch(FancyArrowPatch(path=MplPath([tuple(q) for q in points]), arrowstyle="-|>",
                                 mutation_scale=8, lw=0.8, color=S.MUTED, shrinkA=0, shrinkB=0.6,
                                 joinstyle="miter", capstyle="butt", zorder=2))


C1, C2, C3, C4, C5 = (1, 34), (38.5, 71), (75.5, 105), (109.5, 139), (143.5, 169)
w = lambda c: c[1] - c[0]
MID, UP, LOW = 25.0, 38.5, 11.5          # centre lines of the main row and of the two evaluation boxes
H_MAIN, H_EVAL = 27.0, 19.0

box(C1[0], MID - H_MAIN / 2, w(C1), H_MAIN, "Inputs",
    ["MODIS burned area", "Landsat 8 LST, NDVI", "MODIS LST", "DEM, WorldCover"])
box(C2[0], MID - H_MAIN / 2, w(C2), H_MAIN, "Grid and gate",
    ["~500 m cells", "Natural vegetation", "Five regions pass", "Kozan 2023 fails"], {3: CTRL})
box(C3[0], MID - H_MAIN / 2, w(C3), H_MAIN, "Predictor sets",
    ["Baseline: terrain,", "land cover, NDVI", "Thermal: baseline", "+ six LST/TVDI"])
box(C4[0], UP - H_EVAL / 2, w(C4), H_EVAL, "Within regions", ["Spatial-block CV", "1, 5, 10 km blocks"])
box(C4[0], LOW - H_EVAL / 2, w(C4), H_EVAL, "Across regions", ["20 directions", "Raw and adapted"])
box(C5[0], MID - H_MAIN / 2, w(C5), H_MAIN, "Scored on", ["Whole region", "Scar frames", "Distance collars"])

arrow([(C1[1], MID), (C2[0], MID)])
arrow([(C2[1], MID), (C3[0], MID)])
XS = (C3[1] + C4[0]) / 2
arrow([(C3[1], MID), (XS, MID), (XS, UP), (C4[0], UP)])
arrow([(XS, MID), (XS, LOW), (C4[0], LOW)])
XE = (C4[1] + C5[0]) / 2
arrow([(C4[1], UP), (XE, UP), (XE, MID), (C5[0], MID)])
ax.plot([C4[1], XE, XE], [LOW, LOW, MID], color=S.MUTED, lw=0.8, zorder=2, solid_joinstyle="miter")

problems = layout_check(fig, "Fig. 2 - methods schematic (IJWF)", min_gap_pt=2.0, min_font_pt=S.FS_SMALL,
                        contained=_boxes)
sizes = S.font_sizes(fig)
S.save(fig, HERE, "fig2_schematic")

(HERE / "fig2_provenance.json").write_text(json.dumps({
    "figure": "Fig. 2 - methods schematic, IJWF package",
    "source": "copy of the shared Fig. 2 without the Methods section numbers (headings are unnumbered)",
    "ijwf_changes": "8 pt box titles and 7 pt box lines; sentence case: Natural vegetation, Five regions pass, "
                    "Baseline: terrain, Thermal: baseline, Spatial-block CV, Raw and adapted, Whole region, "
                    "Scar frames, Distance collars",
    "data": "none (schematic)",
    "canvas_mm": [W_MM, H_MM],
    "font_pt": {"body": S.FS_BODY, "minimum": S.FS_SMALL, "used": sizes},
    "layout_check": f"{len(problems)} problems at build time",
    "environment": f"matplotlib {matplotlib.__version__}",
}, indent=1, ensure_ascii=False), encoding="utf-8")
print("fig2 (IJWF) written;", len(problems), "layout problems")
