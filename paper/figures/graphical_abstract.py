#!/usr/bin/env python3
"""Graphical abstract for Fire (MDPI; optional, displayed online beneath the abstract).

Rebuilt 2026-09-30 from the Ecological Informatics version (archived with its TIFF in
paper/archive/ei_graphical_abstract/), whose values predated the reviewer rounds (frame cost
0.133 [0.059, 0.207] on seven scars; the text now reports 0.160 [0.090, 0.230] with the region as
the unit). Every number is parsed from the manuscript at build time rather than typed here, so the
figure cannot drift from the text: if a value moves or its sentence is reworded, a parse or an
assert fails and nothing is written.

Three panels, one per finding of the abstract: C1 the evaluation-area cost (Section 4.3), C2 the
thermal gain within regions against transfer on the original and on comparable study areas
(Table 1 at 5 km blocking; Table 3), C3 the contrast pairs (Section 4.5; the same files and
checks as Fig. 8). C3 shows two pairs only and C2 combines two tables, so the graphical abstract
repeats no figure of the paper, as MDPI asks.

MDPI: PNG, JPEG or TIFF, at least 560 x 1100 px (h x w), no "Graphical Abstract" heading, clear
fonts, decimal points. Written at 140 x 70 mm, 300 dpi (1654 x 827 px), PNG and TIFF; text at
8 pt or more under the shared layout checker.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _layout_check import check as layout_check, assert_inside
RESULTS = (HERE.parent / "04_results.md").read_text(encoding="utf-8")
FLAT = " ".join(RESULTS.split())
ABSTRACT = " ".join((HERE.parent / "00_abstract.md").read_text(encoding="utf-8").split())
M = "−"  # the text uses a true minus

BLUE, ORANGE, GREY = "#0072B2", "#E69F00", "#666666"
MM = 1 / 25.4


def num(s):
    return float(s.replace(M, "-").replace("+", ""))


# ---- within region, 5 km blocking: Table 1, block = 10 cells ----------------
# Continuation rows leave the region cell empty ("| | 10 | ..."), so the region
# cell is matched with optional whitespace and carried forward.
ROW = re.compile(r"^\|\s*([^|]*?)\s*\| (\d+) \| [\d.]+ \| [\d.]+ \| ([+−][\d.]+) \| "
                 r"\[([+−][\d.]+), ([+−][\d.]+)\] \|")
rows, region = {}, None
for line in RESULTS.splitlines():
    m = ROW.match(line)
    if not m:
        continue
    region = m.group(1) or region
    if m.group(2) == "10":
        rows[region] = tuple(num(g) for g in m.groups()[2:])
assert len(rows) == 5, f"expected 5 regions at 10 cells, got {sorted(rows)}"
within = sorted(rows.values())
assert all(lo > 0 for _, lo, _ in within), "a 5 km within-region interval includes zero"

# ---- transfer: Table 3, as drawn and on the 10 km collar ---------------------
def table3(label):
    m = re.search(rf"^\| {label} \| [\d.]+ \| [\d.]+ \| ([+−][\d.]+) \[([+−][\d.]+), ([+−][\d.]+)\] \|",
                  RESULTS, re.M)
    assert m, f"Table 3 row '{label}' not found"
    return tuple(num(g) for g in m.groups())


xreg, equal = table3("As drawn"), table3("10 km collar")
assert xreg == (0.007, -0.020, 0.038) and equal == (0.024, -0.004, 0.049), (xreg, equal)
assert xreg[1] < 0 < xreg[2] and equal[1] < 0 < equal[2]

# ---- evaluation-area cost, region as the unit (Section 4.3) ------------------
m = re.search(r"With the region as the unit, the change then costs \*\*\+(\S+) \[\+(\S+), \+(\S+)\]\*\* over five regions",
              FLAT)
assert m, "Section 4.3 frame-cost sentence not found verbatim"
frame = tuple(float(g) for g in m.groups())
assert frame == (0.160, 0.090, 0.230), frame

# ---- the contrast pairs: the same data and checks as Fig. 8 ------------------
R5 = HERE.parent / "labelfix_rerun" / "round5"
CP_PATH = R5 / "out_official" / "figure_contrast_pairs.json"
S7_PATH = R5 / "s7_contrast_pair.json"
_cp = {p["pair"]: p for p in json.loads(CP_PATH.read_text(encoding="utf-8"))["pairs"]}
_s7 = json.loads(S7_PATH.read_text(encoding="utf-8"))["official"]
HI, LO = _cp["manavgat_2021 ~ mugla_2021"], _cp["bejis_2022 ~ montiferru_2021"]
T_HI = (HI["transfer"]["manavgat_2021_to_mugla_2021"]["auc"], HI["transfer"]["mugla_2021_to_manavgat_2021"]["auc"])
T_LO = (LO["transfer"]["bejis_2022_to_montiferru_2021"]["auc"], LO["transfer"]["montiferru_2021_to_bejis_2022"]["auc"])
D_HI, D_LO = HI["niche_overlap"]["schoener_d_mean1d"], LO["niche_overlap"]["schoener_d_mean1d"]
assert tuple(f"{v:.3f}" for v in T_HI) == ("0.438", "0.345"), T_HI
assert tuple(f"{v:.3f}" for v in T_LO) == ("0.594", "0.548"), T_LO
assert f"{D_HI:.2f}" == "0.80" and f"{D_LO:.2f}" == "0.48", (D_HI, D_LO)
assert all(v == 1 for k, v in _s7["niche_ranks_of_10"]["Man-Mug"].items() if k.startswith("rank_"))
assert all(v == 10 for k, v in _s7["niche_ranks_of_10"]["Bej-Mont"].items() if k.startswith("rank_"))
assert max(T_HI) < 0.5 < min(T_LO)
assert "*D* = 0.80)" in FLAT and "at 0.438 and 0.345" in FLAT and "(*D* = 0.48)" in FLAT and "at 0.594 and 0.548" in FLAT

# ---- the abstract states the same values ------------------------------------
for s in (f"{frame[0]:.3f} [{frame[1]:.3f}, {frame[2]:.3f}]", f"+{within[0][0]:.3f} to +{within[-1][0]:.3f}",
          "+0.007 [−0.020, +0.038]", "+0.024 [−0.004, +0.049]", "the most similar pair of regions failed in both directions"):
    assert s in ABSTRACT, f"abstract lacks '{s}'"

# ---- figure: three panels at 140 x 70 mm ------------------------------------
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8,
                     "svg.fonttype": "none", "pdf.fonttype": 42})
W_MM, H_MM = 140.0, 70.0
fig = plt.figure(figsize=(W_MM * MM, H_MM * MM))
FT = 0.955                                   # panel-title top

# C1: evaluation area
X1 = 0.015
fig.text(X1, FT, "Evaluation area", fontsize=9, fontweight="bold", va="top")
fig.text(X1, 0.80, "Same model, scored on\nthe burn scar and a 2 km\ncollar instead of the\nwhole region, loses",
         fontsize=8, va="top", linespacing=1.25)
fig.text(X1, 0.49, f"{frame[0]:.3f}\nROC-AUC", fontsize=11, fontweight="bold", color=ORANGE, va="top",
         linespacing=1.1)
fig.text(X1, 0.28, f"95% CI [{frame[1]:.3f}, {frame[2]:.3f}]\nfive regions", fontsize=8, color=GREY,
         va="top", linespacing=1.25)

# C2: local skill, weak transfer
X2 = 0.265
fig.text(X2, FT, "Local skill, weak transfer", fontsize=9, fontweight="bold", va="top")
ax = fig.add_axes([0.425, 0.30, 0.19, 0.46])
lo, hi = within[0][0], within[-1][0]
ax.plot([lo, hi], [2, 2], color=BLUE, lw=4, solid_capstyle="butt", alpha=0.35)
for v, a, b in within:
    ax.plot(v, 2, "o", color=BLUE, ms=3.0, zorder=3)
for y, (v, a, b) in ((1, xreg), (0, equal)):
    ax.plot([a, b], [y, y], color=GREY, lw=1.2)
    ax.plot(v, y, "o", color=ORANGE, ms=4.0, zorder=3)
ax.plot([0, 0], [-0.5, 2.5], color="black", lw=0.8, ls=(0, (3, 2)))
ax.set_yticks([2, 1, 0], ["Within region", "Transfer", "Transfer,\ncomparable areas"], fontsize=8)
ax.set_ylim(-0.6, 2.6)
ax.set_xlim(-0.04, 0.17)
ax.set_xticks([0.0, 0.1])
ax.set_xlabel("ΔROC-AUC from the\nthermal predictors", fontsize=8)
ax.tick_params(axis="x", labelsize=8)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0)
assert_inside(ax, "GA panel C2", xs=[tr[0] for tr in within] + [*xreg, *equal])

# C3: similarity does not predict transfer
X3 = 0.655
fig.text(X3, FT, "Similarity does not\npredict transfer", fontsize=9, fontweight="bold", va="top",
         linespacing=1.1)
fig.text(X3, 0.80, "at the point estimates", fontsize=8, color=GREY, va="top")
bx = fig.add_axes([0.845, 0.30, 0.135, 0.40])
for y, (a, b), col in ((1, T_HI, ORANGE), (0, T_LO, BLUE)):
    bx.plot([a, b], [y, y], "o", color=col, ms=4.0, zorder=3)
bx.plot([0.5, 0.5], [-0.5, 1.5], color="black", lw=0.8, ls=(0, (3, 2)))
bx.set_yticks([1, 0], [f"Most similar pair,\nD̄ {D_HI:.2f}: {T_HI[0]:.3f}, {T_HI[1]:.3f}",
                       f"Least similar pair,\nD̄ {D_LO:.2f}: {T_LO[0]:.3f}, {T_LO[1]:.3f}"], fontsize=8)
bx.set_ylim(-0.6, 1.6)
bx.set_xlim(0.30, 0.66)
bx.set_xticks([0.4, 0.6])   # chance (0.5) is the dashed line
bx.set_xlabel("transfer\nROC-AUC", fontsize=8)
bx.tick_params(axis="x", labelsize=8)
for s in ("top", "right", "left"):
    bx.spines[s].set_visible(False)
bx.tick_params(axis="y", length=0)
assert_inside(bx, "GA panel C3", xs=[*T_HI, *T_LO])

fig.text(0.015, 0.045, "Measure transfer skill in the target region before a model is used there.",
         fontsize=8, style="italic", color=GREY)

problems = layout_check(fig, "Graphical abstract", min_gap_pt=2.0, min_font_pt=8.0)
assert not problems, problems

out = HERE / "graphical_abstract"
fig.savefig(out.with_suffix(".png"), dpi=300)
fig.savefig(out.with_suffix(".tif"), dpi=300, pil_kwargs={"compression": "tiff_lzw"})
_rgb = plt.imread(out.with_suffix(".png"))[:, :, :3]
H_PX, W_PX = _rgb.shape[:2]
assert W_PX >= 1100 and H_PX >= 560, (W_PX, H_PX)                   # MDPI minimum (w x h)
(HERE / "graphical_abstract_provenance.json").write_text(json.dumps({
    "figure": "Graphical abstract (Fire, MDPI: optional)",
    "script": "paper/figures/graphical_abstract.py",
    "panels": ["C1 evaluation area", "C2 local skill, weak transfer", "C3 similarity does not predict transfer"],
    "data": {"04_results.md": "Table 1 (block 10), Table 3 (as drawn, 10 km collar), the Section 4.3 "
                              "frame-cost sentence, the Section 4.5 contrast-pair sentence (parsed at build time)",
             "00_abstract.md": "the same values, checked",
             "contrast_pairs": {"path": "paper/labelfix_rerun/round5/out_official/figure_contrast_pairs.json",
                                "sha256": hashlib.sha256(CP_PATH.read_bytes()).hexdigest()},
             "s7": {"path": "paper/labelfix_rerun/round5/s7_contrast_pair.json",
                    "sha256": hashlib.sha256(S7_PATH.read_bytes()).hexdigest()}},
    "within_region_5km": {k: v[0] for k, v in rows.items()},
    "transfer_as_drawn": xreg, "transfer_10km_collar": equal, "frame_cost_region_unit": frame,
    "contrast_pair": {"most_similar_Man_Mug": {"D_bar": round(D_HI, 3), "transfer": [round(v, 4) for v in T_HI]},
                      "least_similar_Bej_Mont": {"D_bar": round(D_LO, 3), "transfer": [round(v, 4) for v in T_LO]}},
    "mdpi_spec": {"minimum_px_h_w": [560, 1100], "formats": ["PNG", "JPEG", "TIFF"]},
    "canvas_mm": [W_MM, H_MM], "pixels_w_h": [int(W_PX), int(H_PX)], "font_pt": {"minimum": 8.0},
    "layout_check": f"paper/figures/_layout_check.py; {len(problems)} problems at build time",
}, indent=1, ensure_ascii=False), encoding="utf-8")
print("wrote", out.with_suffix(".png").name, out.with_suffix(".tif").name, f"{W_PX}x{H_PX} px")
