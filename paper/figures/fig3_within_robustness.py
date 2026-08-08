#!/usr/bin/env python3
"""Figure 3 - within-region thermal increment and block-size robustness.

(a) Baseline vs thermal ROC-AUC per region at the default 2-cell (~1 km) blocking
    (dumbbells), with the paired-delta and its 95% CI in an aligned numeric
    column on the right (forest-plot convention).
(b) Absolute thermal AUC vs block size (2/10/20 cells ~ 1/5/10 km): declines.
(c) Thermal ΔAUC vs block size with 95% CIs: stays above zero everywhere.

Okabe-Ito colours + distinct markers (greyscale-safe); vector.
Data: paper/figures/data/fig_data.json. Asserts vs 04_results Table 3.

2026-08-08 typography/space revision:
  - body 9 pt, minimum 8 pt (was 7 pt); canvas 190 x 92 mm (was 190 x 72);
  - panel (a): the delta labels used to be placed relative to each thermal point
    and ran off the axes (the Evia label was clipped mid-bracket). They now sit
    in a fixed, aligned column with its own header, outside the plotted range,
    so label length can never collide with a data point;
  - panel (c): the five regions are dodged horizontally by DODGE cells so the
    whiskers separate. The dodge is cosmetic - all five share the same three
    block sizes - and is stated in the caption;
  - the per-panel legend in (b) moved to a shared horizontal legend under the
    figure, freeing the panel interior.
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _layout_check import check as layout_check

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "data" / "fig_data.json").read_text())
fig34 = DATA["fig34"]

REGIONS = ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended", "montiferru_2021"]
LABEL = {"manavgat_2021": "Manavgat", "bejis_2022": "Bejís", "mugla_2021": "Muğla",
         "evia_2021_extended": "Evia (ext.)", "montiferru_2021": "Montiferru"}
# Okabe-Ito, no red-green pair; distinct markers for greyscale
COLOUR = {"manavgat_2021": "#0072B2", "bejis_2022": "#E69F00", "mugla_2021": "#56B4E9",
          "evia_2021_extended": "#009E73", "montiferru_2021": "#CC79A7"}
MARKER = {"manavgat_2021": "o", "bejis_2022": "s", "mugla_2021": "^",
          "evia_2021_extended": "D", "montiferru_2021": "v"}
BLOCKS = ["2", "10", "20"]
BLOCK_LABEL = {"2": "2\n~1 km", "10": "10\n~5 km", "20": "20\n~10 km"}

FS_BODY = 9.0    # axis labels, titles, numeric column
FS_TICK = 8.0    # tick labels, legend, column header  (minimum in this figure)
DODGE = 0.15     # panel (c) horizontal offset per region, in x-units (cosmetic)

# ---- asserts vs 04_results Table 3 ----
assert abs(fig34["manavgat_2021"]["2"]["baseline"] - 0.8027) < 5e-4
assert abs(fig34["manavgat_2021"]["2"]["thermal"] - 0.8696) < 5e-4
assert abs(fig34["evia_2021_extended"]["2"]["delta"] - 0.1533) < 5e-4
assert abs(fig34["montiferru_2021"]["20"]["delta"] - 0.1262) < 5e-4
assert abs(fig34["mugla_2021"]["10"]["delta"] - 0.0793) < 5e-4
for reg in REGIONS:
    for b in BLOCKS:
        lo, hi = fig34[reg][b]["delta_ci"]
        assert lo > 0, f"delta CI must exclude zero: {reg} block {b}"
# the dodge must not reorder or merge block groups: half-spread < half-spacing
assert (len(REGIONS) - 1) / 2 * DODGE < 0.5, "dodge too wide - groups would merge"

MM = 1 / 25.4
plt.rcParams.update({"svg.fonttype": "none", "pdf.fonttype": 42})
fig, (axA, axB, axC) = plt.subplots(
    1, 3, figsize=(190 * MM, 92 * MM), width_ratios=[1.88, 1.0, 1.0])

data_artists = []   # (artist, name) pairs handed to the collision checker

# ---------------- (a) dumbbells at block 2, numeric column on the right -----
# The numeric column starts beyond the largest plotted AUC and is LEFT-aligned,
# so its x-position is fixed by the column, never by the data. Right-aligning it
# (the first attempt) made the start of each label depend on its own width and
# pushed the widest ones back onto the Bejís and Evia markers.
X_DATA_MAX = max(fig34[r]["2"]["thermal"] for r in REGIONS)
X_DELTA, X_CI = 0.985, 1.113
assert X_DELTA > X_DATA_MAX + 0.02, "numeric column would sit on the data"

ys = list(range(len(REGIONS)))[::-1]
for reg, y in zip(REGIONS, ys):
    d = fig34[reg]["2"]
    c = COLOUR[reg]
    ln, = axA.plot([d["baseline"], d["thermal"]], [y, y], color=c, lw=1.8, zorder=2)
    m_base, = axA.plot(d["baseline"], y, marker=MARKER[reg], mfc="white", mec=c,
                       ms=6.0, mew=1.3, zorder=3)
    m_therm, = axA.plot(d["thermal"], y, marker=MARKER[reg], mfc=c, mec=c,
                        ms=6.0, zorder=3)
    data_artists += [(ln, f"dumbbell:{LABEL[reg]}"),
                     (m_base, f"baseline-marker:{LABEL[reg]}"),
                     (m_therm, f"thermal-marker:{LABEL[reg]}")]
    axA.text(X_DELTA, y, f"+{d['delta']:.3f}", fontsize=FS_BODY, va="center",
             ha="left")
    axA.text(X_CI, y, f"[{d['delta_ci'][0]:.3f}, {d['delta_ci'][1]:.3f}]",
             fontsize=FS_BODY, va="center", ha="left", color="#444444")

axA.text(X_DELTA, len(REGIONS) - 0.28, "ΔAUC", fontsize=FS_TICK, ha="left",
         va="bottom", color="#444444")
axA.text(X_CI, len(REGIONS) - 0.28, "[95% CI]", fontsize=FS_TICK, ha="left",
         va="bottom", color="#444444")

axA.set_yticks(ys, [LABEL[r] for r in REGIONS], fontsize=FS_BODY)
axA.set_xlim(0.70, 1.345)
axA.set_ylim(-0.75, len(REGIONS) + 0.30)
axA.set_xticks([0.70, 0.80, 0.90])
axA.spines["bottom"].set_bounds(0.70, X_DATA_MAX)
axA.set_xlabel("ROC-AUC (2-cell blocks)", fontsize=FS_BODY)
axA.set_title("(a) Baseline vs thermal", fontsize=FS_BODY, loc="left")

# ---------------- (b) absolute thermal AUC, (c) delta, both vs block size ---
x = list(range(len(BLOCKS)))
offsets = [(i - (len(REGIONS) - 1) / 2) * DODGE for i in range(len(REGIONS))]

for reg, off in zip(REGIONS, offsets):
    c, m = COLOUR[reg], MARKER[reg]
    axB.plot(x, [fig34[reg][b]["thermal"] for b in BLOCKS], color=c, marker=m,
             ms=5.0, lw=1.5)
    deltas = [fig34[reg][b]["delta"] for b in BLOCKS]
    err = [[fig34[reg][b]["delta"] - fig34[reg][b]["delta_ci"][0] for b in BLOCKS],
           [fig34[reg][b]["delta_ci"][1] - fig34[reg][b]["delta"] for b in BLOCKS]]
    axC.errorbar([xi + off for xi in x], deltas, yerr=err, color=c, marker=m,
                 ms=5.0, lw=1.5, capsize=2.5, elinewidth=1.0)

for ax, title, ylab in ((axB, "(b) Thermal AUC", "thermal ROC-AUC"),
                        (axC, "(c) ΔAUC stays > 0",
                         "ΔAUC (thermal − baseline)")):
    ax.set_xticks(x, [BLOCK_LABEL[b] for b in BLOCKS], fontsize=FS_TICK)
    ax.set_title(title, fontsize=FS_BODY, loc="left")
    ax.set_ylabel(ylab, fontsize=FS_BODY)
    ax.set_xlabel("block size (cells)", fontsize=FS_BODY)
    ax.set_xlim(-0.55, len(BLOCKS) - 0.45)

axC.axhline(0, color="black", lw=0.9, ls=(0, (4, 2)), zorder=1)
axC.set_ylim(-0.012, 0.245)
# Ticks are set explicitly on both value axes. Matplotlib otherwise keeps a
# locator tick just outside the view (e.g. -0.05), whose label artist still has
# a position and shows up as a phantom collision against the shared legend.
axC.set_yticks([0.00, 0.05, 0.10, 0.15, 0.20])
axB.set_yticks([0.70, 0.75, 0.80, 0.85, 0.90])

for ax in (axA, axB, axC):
    ax.tick_params(labelsize=FS_TICK)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
axA.tick_params(axis="y", labelsize=FS_BODY)

# ---------------- shared legend under the panels ----------------------------
handles = [Line2D([], [], color=COLOUR[r], marker=MARKER[r], ms=5.0, lw=1.5,
                  label=LABEL[r]) for r in REGIONS]
fig.legend(handles=handles, loc="lower center", ncol=len(REGIONS),
           fontsize=FS_TICK, frameon=False, handlelength=1.8,
           columnspacing=1.4, bbox_to_anchor=(0.5, 0.012))

fig.subplots_adjust(left=0.118, right=0.99, top=0.935, bottom=0.255, wspace=0.32)

problems = layout_check(fig, "Fig. 3 - within-region robustness",
                        min_gap_pt=2.0, min_font_pt=8.0,
                        data_artists=data_artists)

fig.savefig(HERE / "fig3_within_robustness.pdf")
fig.savefig(HERE / "fig3_within_robustness.svg")
if "--preview" in sys.argv:
    fig.savefig(HERE / "fig3_within_robustness_preview.png", dpi=300)

(HERE / "fig3_provenance.json").write_text(json.dumps({
    "figure": "Figure 3 - within-region increment and block robustness",
    "script": "paper/figures/fig3_within_robustness.py",
    "data": "paper/figures/data/fig_data.json (step8c + robustness outputs; per-source sha256 inside)",
    "asserts": "spot values vs 04 Table 3; every delta CI lower bound > 0 (15 region-block "
               "cells); dodge half-spread < half block spacing so groups cannot merge",
    "panel_a_labels": "delta and 95% CI in a fixed aligned column at x=1.005/1.055, outside "
                      "the plotted range (ticks and bottom spine stop at 0.96); label text is "
                      "checked against every dumbbell artist by the collision checker",
    "panel_c_dodge": {"cells": DODGE, "note": "cosmetic horizontal offset so whiskers separate; "
                                              "all five regions share the same three block sizes; "
                                              "stated in the caption"},
    "palette": "Okabe-Ito 5-colour + distinct markers for greyscale; no red-green pair",
    "canvas_mm": [190, 92],
    "column": "double (190 mm)",
    "font_pt": {"body": FS_BODY, "minimum": FS_TICK},
    "layout_check": f"paper/figures/_layout_check.py; {len(problems)} problems at build time",
    "environment": f"matplotlib {matplotlib.__version__}",
}, indent=1, ensure_ascii=False))
print("fig3 written; all 15 delta CIs exclude zero")
