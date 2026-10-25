#!/usr/bin/env python3
"""Figure 2 - methods schematic (2026-10-23 redraw).

Five columns, left to right: inputs, grid and gate, the two predictor sets, the two evaluations
(within regions, across regions) and the evaluation frames they are scored on. White boxes with
a hairline edge, one heading and a few short lines each, the Methods section in small grey type,
straight or right-angled connectors. The earlier version (14 boxes, coloured fills, a footer band
and a rejecting branch for the gate) is in the git history before 2026-10-23.

No numbers -> no numeric asserts. Structural checks: (1) every section number printed here is
a live Methods heading with the expected title, and the printed set equals SECTIONS; (2) every
section reference in the caption is a live heading next to its topic word; (3) every text fits
its box.
"""
import json
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
from matplotlib.path import Path as MplPath

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _layout_check import check as layout_check
import _style as S

HERE = Path(__file__).resolve().parent
METHODS = HERE.parent / "03_methods.md"

EDGE = "#9A9A9A"
CTRL = "#767676"   # Kozan 2023, as in Fig. 1

# --- every section number this figure prints, with the heading it must match --
SECTIONS = {
    "2.2": 'Burned-area label and the ~500 m analysis grid',
    "2.3": 'Burned-landcover admissibility gate',
    "2.4": 'Predictor variables',
    "2.5": 'Cell aggregation, validity and analysis populations',
    "2.6": 'Classifier',
    "2.7": 'Spatial-block cross-validation and bootstrap uncertainty',
    "2.8": 'Cross-region transfer protocol',
    "2.9": 'Label-free domain adaptation',
    "2.12": 'Evaluation frames and controls on the transfer path',
}
_heads = dict(re.findall(r"^##+ (2\.\d+(?:\.\d+)?) (.+)$",
                         METHODS.read_text(encoding="utf-8"), re.M))
for num, title in SECTIONS.items():
    assert num in _heads, f"Methods has no section {num} (figure references it)"
    assert _heads[num].strip() == title, \
        f"section {num} moved: figure expects {title!r}, Methods has {_heads[num]!r}"


# (1b) the section numbers the boxes print are recorded by box() and must equal SECTIONS exactly
# (checked after the boxes are drawn), so a box cannot cite a section the table does not vouch for.
# The boxes print bare numbers; the caption says they are Methods sections. The section sign is
# never used, in the figure or in the caption (author's rule, 2026-10-23).

# (1c) the caption: every "Section a.b" must be a live Methods heading, and must sit next to a
# word from that heading's topic, so a renumbered section cannot survive under an old number
# (the caption once cited "decomposition (3.12)" and "sensitivity designs (3.16)" after the split).
CAPTION_TOPIC = {"2.13": r"leakage|seed|bootstrap"}
_caps = (HERE.parent / "figure_captions.tex").read_text(encoding="utf-8")
_cap2 = " ".join(_caps[_caps.index("fig2_schematic.pdf"):_caps.index(r"\label{fig:pipeline}")].split())
assert "\u00a7" not in _cap2 and "\\S" not in _cap2, "Fig. 2 caption uses the section sign"
CAPTION_REFS = re.findall(r"Sections? (\d+\.\d+)", _cap2)
assert CAPTION_REFS, "Fig. 2 caption cites no section"
for m in re.finditer(r"Sections? (\d+\.\d+)", _cap2):
    num = m.group(1)
    assert num in _heads, f"caption cites Section {num}, which Methods does not have"
    assert num in CAPTION_TOPIC, f"caption cites Section {num}; add its topic to CAPTION_TOPIC"
    before = _cap2[max(0, m.start() - 90):m.start()]
    assert re.search(CAPTION_TOPIC[num], before, re.I), \
        f"caption cites Section {num} ({_heads[num]!r}) next to {before[-60:]!r}"

S.apply()
W_MM, H_MM = S.WIDTH_MM, 58.0
fig = plt.figure(figsize=(W_MM * S.MM, H_MM * S.MM))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W_MM)          # 1 axis unit == 1 mm on the page
ax.set_ylim(0, H_MM)
ax.axis("off")

_boxes = []   # (text_artist, patch_artist, label) for the containment check
PRINTED_REFS = []


def box(x, y, w, h, title, lines, refs, line_colours=None):
    """refs: the Methods section numbers of this box, printed as bare numbers."""
    PRINTED_REFS.extend(refs)
    refs = ", ".join(refs)
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
    tr = ax.text(x + 2.2, y + 1.8, refs, ha="left", va="bottom", fontsize=S.FS_SMALL, color=S.MUTED, zorder=4)
    _boxes.append((tr, p, refs))
    return p


def arrow(points):
    ax.add_patch(FancyArrowPatch(path=MplPath([tuple(q) for q in points]), arrowstyle="-|>",
                                 mutation_scale=8, lw=0.8, color=S.MUTED, shrinkA=0, shrinkB=0.6,
                                 joinstyle="miter", capstyle="butt", zorder=2))


C1, C2, C3, C4, C5 = (1, 34), (38.5, 71), (75.5, 105), (109.5, 139), (143.5, 169)
w = lambda c: c[1] - c[0]

box(C1[0], 13, w(C1), 32, "Inputs", ["MODIS burned area", "Landsat 8 LST, NDVI", "MODIS LST",
                                     "DEM, WorldCover"], ["2.2", "2.4"])
box(C2[0], 13, w(C2), 32, "Grid and gate", ["~500 m cells", "natural vegetation", "five regions pass",
                                            "Kozan 2023 fails"], ["2.2", "2.3", "2.5"], {3: CTRL})
box(C3[0], 13, w(C3), 32, "Predictor sets", ["baseline: terrain,", "land cover, NDVI", "thermal: baseline",
                                             "+ six LST/TVDI"], ["2.4", "2.6"])
box(C4[0], 31, w(C4), 23, "Within regions", ["spatial-block CV", "1, 5, 10 km blocks"], ["2.7"])
box(C4[0], 4, w(C4), 23, "Across regions", ["20 directions", "raw and adapted"], ["2.8", "2.9"])
box(C5[0], 13, w(C5), 32, "Scored on", ["whole region", "scar frames", "distance collars"], ["2.12"])
assert set(PRINTED_REFS) == set(SECTIONS), (sorted(set(PRINTED_REFS)), sorted(SECTIONS))

arrow([(C1[1], 29), (C2[0], 29)])
arrow([(C2[1], 29), (C3[0], 29)])
XS = (C3[1] + C4[0]) / 2
arrow([(C3[1], 29), (XS, 29), (XS, 42.5), (C4[0], 42.5)])
arrow([(XS, 29), (XS, 15.5), (C4[0], 15.5)])
XE = (C4[1] + C5[0]) / 2
arrow([(C4[1], 42.5), (XE, 42.5), (XE, 29), (C5[0], 29)])
ax.plot([C4[1], XE, XE], [15.5, 15.5, 29], color=S.MUTED, lw=0.8, zorder=2, solid_joinstyle="miter")

problems = layout_check(fig, "Fig. 2 - methods schematic", min_gap_pt=2.0, min_font_pt=8.0,
                        contained=_boxes)
fig.savefig(HERE / "fig2_schematic.pdf")
fig.savefig(HERE / "fig2_schematic.svg")
if "--preview" in sys.argv:
    fig.savefig(HERE / "fig2_schematic_preview.png", dpi=300)

(HERE / "fig2_provenance.json").write_text(json.dumps({
    "figure": "Fig. 2 - methods schematic",
    "script": "paper/figures/fig2_schematic.py",
    "data": "none (schematic; labels mirror 03_methods section numbering)",
    "asserts": "no numbers to assert; every printed section number is a live Methods heading with its "
               "title and the printed set equals SECTIONS; every caption section reference is a live heading"
               "next to its topic word; every text fits its box",
    "printed_section_references": len(PRINTED_REFS),
    "caption_section_references": CAPTION_REFS,
    "sections_referenced": sorted(SECTIONS, key=lambda s: [int(p) for p in s.split(".")]),
    "design": "2026-10-23 redraw: five columns, white boxes, one accent-free palette; Kozan 2023 in grey text",
    "canvas_mm": [W_MM, H_MM],
    "font_pt": {"body": S.FS_BODY, "minimum": S.FS_SMALL},
    "layout_check": f"paper/figures/_layout_check.py; {len(problems)} problems at build time",
    "environment": f"matplotlib {matplotlib.__version__}",
}, indent=1, ensure_ascii=False), encoding="utf-8")
print("fig2 written")
