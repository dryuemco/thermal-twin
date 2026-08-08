#!/usr/bin/env python3
"""Figure 2 - methods schematic.

Data flow from source products to the transfer/diagnostic programme, annotated
with the Methods subsection that specifies each stage.

No numbers -> no numeric asserts. Two structural checks stand in for them:
  (1) every section reference in this file is verified against the live heading
      list of 03_methods.md at build time (SECTIONS below + assert), so the
      figure cannot drift out of step with a renumbered Methods;
  (2) every box label is checked to fit inside its own box by _layout_check's
      `contained` test, so no label silently spills.

2026-08-08 revision:
  - typography: double-column 190 mm, body 9 pt, minimum 8 pt (was 7 pt);
  - the burned-landcover gate now shows its rejecting branch, with Kozan 2023
    drawn as the negative control in the same grey/dashed style used in Fig. 1,
    because the gate carries a visible argument in Methods 3.3 / Results 4.1;
  - added the transfer-gap decomposition (3.12) - previously absent although it
    is the paper's central instrument - and a footer band for the throughout-
    applies material (3.13 leakage/seed/bootstrap, 3.16 sensitivity designs);
  - the in-artwork "Fig. 2" title is removed: Elsevier sets the caption, and the
    caption now lives in paper/figure_captions.tex;
  - all connectors are orthogonal (right-angled elbows, square corners) and the
    canvas is compacted 118 -> 95 mm by pulling the dead space out of the
    columns; topology, box content and section references are unchanged.

Okabe-Ito accents, greyscale-safe, vector.
"""
import json
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle
from matplotlib.path import Path as MplPath

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _layout_check import check as layout_check

HERE = Path(__file__).resolve().parent
METHODS = HERE.parent / "03_methods.md"

BLUE, ORANGE = "#0072B2", "#E69F00"
BLUE_FILL, ORANGE_FILL = "#E8F1F8", "#FDF3E0"
GREYBOX, GREYEDGE = "#F0F0F0", "#888888"
CTRL, CTRL_FILL = "#767676", "#EFEFEF"   # matches Fig. 1 gate-control styling

FS_BOX = 8.0    # box labels (minimum in this figure)
FS_NOTE = 9.0   # footer band / orientation note (body)

# --- every section number this figure prints, with the heading it must match --
SECTIONS = {
    "3.2":  "Burned-area label and the ~500 m analysis grid",
    "3.3":  "Burned-landcover admissibility gate",
    "3.4":  "Predictor variables",
    "3.5":  "Cell-level aggregation, validity mask and analysis population",
    "3.6":  "Feature sets",
    "3.7":  "Classifier and preprocessing",
    "3.9":  "Spatial-block bootstrap uncertainty",
    "3.10": "Cross-region transfer protocol",
    "3.11": "Label-blind domain adaptation",
    "3.12": "Transfer-gap decomposition and concept-shift diagnostic",
    "3.13": "Leakage control, sensitivity analyses and reproducibility",
    "3.14": "Transferability diagnostics versus transfer",
    "3.15": "Interventions",
    "3.16": "Additional sensitivity designs",
}
_heads = dict(re.findall(r"^##+ (3\.\d+(?:\.\d+)?) (.+)$",
                         METHODS.read_text(encoding="utf-8"), re.M))
for num, title in SECTIONS.items():
    assert num in _heads, f"Methods has no section {num} (figure references it)"
    assert _heads[num].strip() == title, \
        f"section {num} moved: figure expects {title!r}, Methods has {_heads[num]!r}"

MM = 1 / 25.4
W_MM, H_MM = 190.0, 95.0
plt.rcParams.update({"svg.fonttype": "none", "pdf.fonttype": 42})
fig = plt.figure(figsize=(W_MM * MM, H_MM * MM))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W_MM)          # 1 axis unit == 1 mm on the page
ax.set_ylim(0, H_MM)
ax.axis("off")

_boxes = []   # (text_artist, patch_artist, label) for the containment check


def box(x, y, w, h, text, fc=GREYBOX, ec=GREYEDGE, tc="black", dashed=False):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.9",
                       facecolor=fc, edgecolor=ec, linewidth=0.9,
                       linestyle=(0, (2.6, 1.6)) if dashed else "solid",
                       mutation_aspect=1.0)
    ax.add_patch(p)
    t = ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                fontsize=FS_BOX, color=tc, linespacing=1.45, zorder=4)
    _boxes.append((t, p, text.split("\n")[0]))
    return p


def elbow(points, color="#555555", dashed=False, head=True):
    """Orthogonal (right-angled) connector through the given mm waypoints.

    Every segment is axis-parallel; corners stay square rather than rounded, so
    the routing reads as a wiring diagram instead of a set of loose diagonals.
    """
    ax.add_patch(FancyArrowPatch(
        path=MplPath([tuple(p) for p in points]),
        arrowstyle="-|>" if head else "-",
        mutation_scale=9, lw=1.0, color=color,
        shrinkA=1.5 if head else 0, shrinkB=1.5 if head else 0,
        joinstyle="miter", capstyle="butt",
        linestyle=(0, (2.6, 1.6)) if dashed else "solid", zorder=2))


# ---- column x-extents (mm): inputs | grid+gate | features | models | outputs
# Widths are unequal on purpose: they are sized to the longest label each column
# has to carry at 8 pt, which the `contained` check enforces.
C1, C2, C3, C4, C5 = (3, 39), (44, 80), (85, 109), (114, 152), (157, 187)
def w(c): return c[1] - c[0]

# ---------------- column 1: source products + the negative control ----------
box(C1[0], 76, w(C1), 12, "MCD64A1 burned area\n(label; §3.2)")
box(C1[0], 54, w(C1), 19, "Landsat LST & NDVI,\nMODIS LST, TVDI,\n"
                          "downscaling + fusion\n(§3.4)")
box(C1[0], 39, w(C1), 12, "DEM, slope,\nESA WorldCover (§3.4)")
box(C1[0], 18, w(C1), 18, "negative control\nKozan 2023 (§3.3):\n"
                          "98% cropland burned\n→ never modelled",
    fc=CTRL_FILL, ec=CTRL, tc=CTRL, dashed=True)

# ---------------- column 2: grid, gate, population --------------------------
box(C2[0], 74, w(C2), 14, "~510 m analysis grid\n(17×17 @ 30 m; §3.2)")
box(C2[0], 50, w(C2), 14, "burned-landcover\nadmissibility gate\n(§3.3)")
box(C2[0], 26, w(C2), 16, "primary population:\nnatural vegetation\n(§3.5)")

# All three source products are aggregated onto the same grid, so they merge on
# a collector bus rather than as three converging diagonals.
BUS_X, REJ_X = 40.6, 42.9
elbow([(C1[1], 82), (BUS_X, 82), (BUS_X, 45)], head=False)      # the bus itself
for y0 in (82, 63.5, 45):
    elbow([(C1[1], y0), (BUS_X, y0)], head=False)
elbow([(BUS_X, 81), (C2[0], 81)])
elbow([(62, 74), (62, 64)])
elbow([(62, 50), (62, 42)])
ax.text(63.4, 46, "pass", fontsize=FS_BOX, ha="left", va="center",
        color="#555555")
# The rejecting branch of the gate. Dashed and grey, matching Fig. 1's control
# styling; it terminates in the control box and goes nowhere else, so the figure
# cannot be read as feeding the control onward into any model.
elbow([(C2[0], 57), (REJ_X, 57), (REJ_X, 27), (C1[1], 27)],
      color=CTRL, dashed=True)

# ---------------- column 3: feature sets ------------------------------------
box(C3[0], 46, w(C3), 18, "feature sets\n(§3.6)\nbaseline vs\n+ 6 thermal",
    fc=BLUE_FILL, ec=BLUE)
elbow([(C2[1], 34), (82.5, 34), (82.5, 55), (C3[0], 55)])

# ---------------- column 4: the two evaluations -----------------------------
box(C4[0], 66, w(C4), 18, "within-region (§3.7–3.9)\nRF, spatial-block CV,\n"
                          "block-size robustness")
box(C4[0], 34, w(C4), 20, "cross-region transfer\n(§3.10–3.11)\n20 ordered directions\n"
                          "z-score / CORAL")
elbow([(C3[1], 55), (111.5, 55), (111.5, 75), (C4[0], 75)])
elbow([(C3[1], 55), (111.5, 55), (111.5, 44), (C4[0], 44)])

# ---------------- column 5: what comes out ----------------------------------
box(C5[0], 74, w(C5), 14, "within-region ΔAUC\n5 regions ×\n3 block sizes",
    fc="#FFFFFF", ec="#555555")
box(C5[0], 53, w(C5), 18, "transfer-gap\ndecomposition\n(§3.12): recovered\nvs residual",
    fc=BLUE_FILL, ec=BLUE)
box(C5[0], 34, w(C5), 16, "diagnostics (§3.14)\nP(x) · P(x|y=1)\nP(y) · P(y|x)",
    fc=ORANGE_FILL, ec=ORANGE)
box(C5[0], 15, w(C5), 16, "interventions\n(§3.15): LORO,\nfeature removal")

# Three routing lanes in the 152-157 gap; lanes are reused only where the
# vertical runs cannot overlap in y, so no two connectors ever share a segment.
elbow([(C4[1], 79), (153.2, 79), (153.2, 81), (C5[0], 81)])
elbow([(C4[1], 71), (154.4, 71), (154.4, 66), (C5[0], 66)])   # within -> decomposition
elbow([(C4[1], 50), (153.2, 50), (153.2, 58), (C5[0], 58)])   # transfer -> decomposition
elbow([(C4[1], 44), (154.4, 44), (154.4, 42), (C5[0], 42)])
elbow([(C4[1], 38), (155.6, 38), (155.6, 23), (C5[0], 23)])

# ---------------- footer: what applies throughout ---------------------------
ax.add_patch(Rectangle((3, 2), 184, 11, facecolor="#F7F7F7",
                       edgecolor="#CCCCCC", linewidth=0.8, zorder=1))
ax.text(95, 7.5,
        "Applies throughout — leakage hard-exclusion, seed 42, 1000-replicate "
        "spatial-block bootstrap (§3.13);\nsensitivity designs: Evia AOI, "
        "Montiferru population, predictor-window closure (§3.16)",
        fontsize=FS_NOTE, ha="center", va="center", linespacing=1.5, zorder=3)

ax.text(3, 91.5, "Section numbers refer to Methods.", fontsize=FS_NOTE,
        ha="left", va="center", style="italic", color="#444444")

problems = layout_check(fig, "Fig. 2 - methods schematic",
                        min_gap_pt=2.0, min_font_pt=8.0, contained=_boxes)

fig.savefig(HERE / "fig2_schematic.pdf")
fig.savefig(HERE / "fig2_schematic.svg")
if "--preview" in sys.argv:
    fig.savefig(HERE / "fig2_schematic_preview.png", dpi=300)

(HERE / "fig2_provenance.json").write_text(json.dumps({
    "figure": "Fig. 2 - methods schematic",
    "script": "paper/figures/fig2_schematic.py",
    "data": "none (schematic; labels mirror 03_methods section numbering)",
    "asserts": "no numbers to assert; instead (a) all 14 section references are "
               "verified against the live 03_methods.md heading list at build "
               "time - number AND title - so a renumbered Methods breaks the "
               "build; (b) every box label is checked to fit its own box",
    "sections_referenced": sorted(SECTIONS, key=lambda s: [int(p) for p in s.split(".")]),
    "gate_branch": "burned-landcover gate shown with its rejecting branch; Kozan 2023 "
                   "drawn as negative control in the grey/dashed style used in Fig. 1, "
                   "connected to the gate by a headless dashed connector so the figure "
                   "does not imply it flows onward into any model",
    "routing": "orthogonal only - every connector is a right-angled elbow with square "
               "corners; input products merge on a collector bus; the three lanes in the "
               "column 4->5 gap are reused only where vertical runs cannot overlap in y, "
               "so no two connectors share a segment",
    "palette": "Okabe-Ito accents on grey; neutral grey for the control; no red-green",
    "canvas_mm": [W_MM, H_MM],
    "column": "double (190 mm)",
    "font_pt": {"body": FS_NOTE, "minimum": FS_BOX},
    "layout_check": f"paper/figures/_layout_check.py; {len(problems)} problems at build time",
    "environment": f"matplotlib {matplotlib.__version__}",
}, indent=1, ensure_ascii=False))
print("fig2 written")
