#!/usr/bin/env python3
"""Graphical abstract for Ecological Informatics (encouraged, not required).

(The target journal was recorded as Environmental Modelling & Software until 2026-09-23.)

Every number is parsed from paper/04_results.md at build time rather than typed
here, so the figure cannot drift from the Results: if a value moves or its
sentence is reworded, a parse or an assert fails and nothing is written.

Three panels, one per contribution: C1 the evaluation-geometry result (Section 4.3), C2 the
thermal block's increment under holdouts of increasing hardness (Section 4.3), C3 the contrast
pair (Contribution 3; Fig. 8), whose values come from the same files and checks as Fig. 8.

Elsevier sizing: at least 531 x 1328 px (h x w), readable at 5 x 13 cm, 300 dpi; TIFF, EPS or
PDF. Written at exactly 130 x 50 mm and 300 dpi, as PDF and TIFF (PNG preview).

2026-09-23 revision (corrected Manavgat label): every parse now targets the rewritten 04
(frame cost 0.133 [+0.059, +0.207]; half-split +0.028; leave-one-scar-out +0.024
[-0.040, +0.089]; across regions +0.007 [-0.021, +0.037]; equalised transfer 0.527 -> 0.589;
baseline 0.519 vs 0.527). The house minimum of 8 pt is applied (the previous build used
6.5-7.5 pt) and the shared layout checker now runs, which it did not before. Every plotted
value is asserted inside its axis.
A third panel (2026-09-23) carries the contrast pair, which the abstract and Highlight 5
state and the previous graphical abstract never showed. To fit three panels at 8 pt in
13 x 5 cm, the baseline-control and equal-frame lines leave the graphical abstract; both stay
in the abstract text.
"""
import hashlib
import json
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _layout_check import check as layout_check, assert_inside
RESULTS = (HERE.parent / "04_results.md").read_text(encoding="utf-8")
M = "−"  # the Results use a true minus

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
assert abs(within[0][0] - 0.045) < 1e-9 and abs(within[-1][0] - 0.148) < 1e-9

# ---- the hardening ladder: the Section 4.3 summary sentence -----------------
m = re.search(r"is \+(\S+) on\s+a\s+within-region\s+half-split,\s+\*\*\+(\S+)\s+\[(\S+),\s+(\S+)\]\*\*"
              r"\s+under\s+leave-one-scar-out,\s+and\s+\+(\S+)\s+\[(\S+),\s+(\S+)\]\s+across\s+regions", RESULTS)
assert m, "Section 4.3 hardening sentence not found verbatim"
half = num(m.group(1))
loso = (num(m.group(2)), num(m.group(3)), num(m.group(4)))
xreg = (num(m.group(5)), num(m.group(6)), num(m.group(7)))
assert half == 0.028 and loso == (0.024, -0.040, 0.089) and xreg == (0.007, -0.021, 0.037), \
    (half, loso, xreg)

# ---- evaluation geometry and the baseline control ----------------------------
m = re.search(r"That change alone costs \*\*(\S+) \[\+(\S+), \+(\S+)\]\*\*", RESULTS)
assert m, "Section 4.3 frame-cost sentence not found verbatim"
frame = tuple(float(g) for g in m.groups())
assert frame == (0.133, 0.059, 0.207), frame
# equalised transfer (Table 3) and the as-drawn baseline control (Section 4.5)
FLAT = " ".join(RESULTS.split())
assert "| full | full (**Table B9**) | 0.527 |" in FLAT and "| **10 km** | **10 km** | **0.589** |" in FLAT
assert "at a mean of **0.519** against **0.527** for the thermal model" in FLAT

# ---- the contrast pair (Contribution 3): the same data and checks as Fig. 8 ----------------
R5 = HERE.parent / "labelfix_rerun" / "round5"
CP_PATH = R5 / "out_official" / "figure_contrast_pairs.json"
S7_PATH = R5 / "s7_contrast_pair.json"
_cp = {p["pair"]: p for p in json.loads(CP_PATH.read_text(encoding="utf-8"))["pairs"]}
_s7 = json.loads(S7_PATH.read_text(encoding="utf-8"))["official"]
HI, LO = _cp["manavgat_2021 ~ mugla_2021"], _cp["bejis_2022 ~ montiferru_2021"]
T_HI = (HI["transfer"]["manavgat_2021_to_mugla_2021"]["auc"], HI["transfer"]["mugla_2021_to_manavgat_2021"]["auc"])
T_LO = (LO["transfer"]["bejis_2022_to_montiferru_2021"]["auc"], LO["transfer"]["montiferru_2021_to_bejis_2022"]["auc"])
D_HI, D_LO = HI["niche_overlap"]["schoener_d_mean1d"], LO["niche_overlap"]["schoener_d_mean1d"]
# as Fig. 8: values, and the ranks of 10 on all five overlap measures
assert tuple(f"{v:.3f}" for v in T_HI) == ("0.438", "0.345"), T_HI
assert tuple(f"{v:.3f}" for v in T_LO) == ("0.594", "0.548"), T_LO
assert f"{D_HI:.2f}" == "0.80" and f"{D_LO:.2f}" == "0.48", (D_HI, D_LO)
assert all(v == 1 for k, v in _s7["niche_ranks_of_10"]["Man-Mug"].items() if k.startswith("rank_"))
assert all(v == 10 for k, v in _s7["niche_ranks_of_10"]["Bej-Mont"].items() if k.startswith("rank_"))
assert max(T_HI) < 0.5 < min(T_LO)
# the abstract's contrast sentence and Highlight 5 carry the same values
_abs = " ".join((HERE.parent / "00_abstract.md").read_text(encoding="utf-8").split())
assert "neither sufficient nor necessary" in _abs and "(0.438, 0.345)" in _abs and "(0.594, 0.548)" in _abs
_hl = (HERE.parent / "highlights.md").read_text(encoding="utf-8")
assert "Highest niche-overlap pair fails both ways; lowest-overlap pair transfers both ways" in _hl

# ---- figure: three panels, C1 | C2 | C3, at 130 x 50 mm (Elsevier's 13 x 5 cm) -------------
# Every text is at least 8 pt at print size and the shared layout checker must pass.
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8,
                     "svg.fonttype": "none", "pdf.fonttype": 42})
W_MM, H_MM = 130.0, 50.0
fig = plt.figure(figsize=(W_MM * MM, H_MM * MM))
FT = 0.955                                   # panel-title baseline (top of text)

# C1: evaluation geometry -------------------------------------------------------------------
X1 = 0.015
fig.text(X1, FT, "Evaluation\ngeometry", fontsize=9, fontweight="bold", va="top", linespacing=1.1)
fig.text(X1, 0.665, "Same model, scored\nat the fire, not\nregion-wide, costs", fontsize=8, va="top",
         linespacing=1.2)
fig.text(X1, 0.395, f"{frame[0]:.3f} AUC", fontsize=11, fontweight="bold", color=ORANGE, va="top")
fig.text(X1, 0.255, f"95% CI\n[{frame[1]:.3f}, {frame[2]:.3f}]", fontsize=8, color=GREY, va="top",
         linespacing=1.2)

# C2: local skill does not travel -------------------------------------------------------------
X2 = 0.255
fig.text(X2, FT, "Local skill\ndoes not travel", fontsize=9, fontweight="bold", va="top", linespacing=1.1)
ax = fig.add_axes([0.415, 0.305, 0.185, 0.395])
labels = ["Within region", "Half-split", "Scar withheld", "Across regions"]
lo, hi = within[0][0], within[-1][0]
ax.plot([lo, hi], [3, 3], color=BLUE, lw=4, solid_capstyle="butt", alpha=0.35)
for v, a, b in within:
    ax.plot(v, 3, "o", color=BLUE, ms=3.0, zorder=3)
ax.plot(half, 2, "o", color=BLUE, ms=4.0, zorder=3)
for y, (v, a, b) in ((1, loso), (0, xreg)):
    ax.plot([a, b], [y, y], color=GREY, lw=1.2)
    ax.plot(v, y, "o", color=ORANGE, ms=4.0, zorder=3)
ax.plot([0, 0], [-0.5, 3.5], color="black", lw=0.8, ls=(0, (3, 2)))
ax.set_yticks([3, 2, 1, 0], labels, fontsize=8)
ax.set_ylim(-0.6, 3.6)
ax.set_xlim(-0.06, 0.17)
ax.set_xticks([0.0, 0.1])
ax.set_xlabel("Δ AUC, thermal block", fontsize=8)
ax.tick_params(axis="x", labelsize=8)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0)
assert_inside(ax, "GA panel C2", xs=[tr[0] for tr in within] + [half, *loso, *xreg])

# C3: similarity is neither sufficient nor necessary ------------------------------------------
X3 = 0.655
fig.text(X3, FT, "Similarity: neither\nsufficient nor necessary", fontsize=9, fontweight="bold",
         va="top", linespacing=1.1)
bx = fig.add_axes([0.845, 0.305, 0.135, 0.395])
for y, (a, b), col in ((1, T_HI, ORANGE), (0, T_LO, BLUE)):
    bx.plot([a, b], [y, y], "o", color=col, ms=4.0, zorder=3)
bx.plot([0.5, 0.5], [-0.5, 1.5], color="black", lw=0.8, ls=(0, (3, 2)))
bx.set_yticks([1, 0], [f"Most similar, D̄ {D_HI:.2f}\n{T_HI[0]:.3f} / {T_HI[1]:.3f}",
                       f"Least similar, D̄ {D_LO:.2f}\n{T_LO[0]:.3f} / {T_LO[1]:.3f}"], fontsize=8)
bx.set_ylim(-0.6, 1.6)
bx.set_xlim(0.30, 0.66)
bx.set_xticks([0.4, 0.6])   # chance (0.5) is the dashed line
bx.set_xlabel("transfer AUC", fontsize=8)
fig.text(X3, 0.775, "at the point estimates", fontsize=8, color=GREY, va="top")
bx.tick_params(axis="x", labelsize=8)
for s in ("top", "right", "left"):
    bx.spines[s].set_visible(False)
bx.tick_params(axis="y", length=0)
assert_inside(bx, "GA panel C3", xs=[*T_HI, *T_LO])

fig.text(0.015, 0.035, "Measure transfer skill on the target region before relying on a model there.",
         fontsize=8, style="italic", color=GREY)

problems = layout_check(fig, "Graphical abstract", min_gap_pt=2.0, min_font_pt=8.0)
assert not problems, problems

out = HERE / "graphical_abstract"
fig.savefig(out.with_suffix(".png"), dpi=300)
fig.savefig(out.with_suffix(".tif"), dpi=300, pil_kwargs={"compression": "tiff_lzw"})
fig.savefig(out.with_suffix(".pdf"))
_rgb = plt.imread(out.with_suffix(".png"))[:, :, :3]
H_PX, W_PX = _rgb.shape[:2]
assert W_PX >= 1328 and H_PX >= 531, (W_PX, H_PX)                 # Elsevier minimum (w x h)
assert abs(W_MM - 130) < 1e-9 and abs(H_MM - 50) < 1e-9            # 13 x 5 cm at 300 dpi
plt.imsave(HERE / "graphical_abstract_greyscale.png",
           0.2126 * _rgb[:, :, 0] + 0.7152 * _rgb[:, :, 1] + 0.0722 * _rgb[:, :, 2],
           cmap="gray", vmin=0.0, vmax=1.0)
(HERE / "graphical_abstract_provenance.json").write_text(json.dumps({
    "figure": "Graphical abstract (Ecological Informatics: encouraged, not required)",
    "script": "paper/figures/graphical_abstract.py",
    "panels": ["C1 evaluation geometry", "C2 local skill does not travel",
               "C3 similarity neither sufficient nor necessary"],
    "data": {"04_results.md": "Table 1 (block 10), the Section 4.3 hardening sentence, the frame-cost "
                              "sentence, Table 3 and the Section 4.5 baseline control (parsed at build time)",
             "contrast_pairs": {"path": "paper/labelfix_rerun/round5/out_official/figure_contrast_pairs.json",
                                "sha256": hashlib.sha256(CP_PATH.read_bytes()).hexdigest()},
             "s7": {"path": "paper/labelfix_rerun/round5/s7_contrast_pair.json",
                    "sha256": hashlib.sha256(S7_PATH.read_bytes()).hexdigest()}},
    "within_region_5km": {k: v[0] for k, v in rows.items()},
    "half_split": half, "leave_one_scar_out": loso, "across_regions": xreg,
    "frame_cost": frame,
    "contrast_pair": {"most_similar_Man_Mug": {"D_bar": round(D_HI, 3), "transfer": [round(v, 4) for v in T_HI]},
                      "least_similar_Bej_Mont": {"D_bar": round(D_LO, 3), "transfer": [round(v, 4) for v in T_LO]},
                      "note": "point estimates, as the abstract states; at 5 km blocking only Mugla->"
                              "Manavgat is interval-supported (Fig. 8 caption)"},
    "asserts": "every 04 number parsed and checked; contrast-pair values, D-bar and ranks as in Fig. 8; "
               "abstract sentence and Highlight 5 carry the same values; every plotted value inside its "
               "axis; layout checker 0 problems at >= 8 pt; pixel size >= 1328 x 531",
    "elsevier_spec": {"minimum_px_w_h": [1328, 531], "display_cm": [13, 5], "dpi": 300,
                      "formats_accepted": ["TIFF", "EPS", "PDF"], "written": ["PDF", "TIFF", "PNG (preview)"]},
    "canvas_mm": [W_MM, H_MM], "pixels_w_h": [int(W_PX), int(H_PX)],
    "font_pt": {"minimum": 8.0},
    "layout_check": f"paper/figures/_layout_check.py; {len(problems)} problems at build time",
    "greyscale": "graphical_abstract_greyscale.png",
}, indent=1, ensure_ascii=False), encoding="utf-8")
print("wrote", out.with_suffix(".pdf").name, out.with_suffix(".tif").name, f"{W_PX}x{H_PX} px")
