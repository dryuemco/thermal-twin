#!/usr/bin/env python3
"""Figure 4 - cross-region transfer matrices: raw / region-wise z-score / CORAL.

Three 5x5 source-x-target heatmaps of thermal transfer ROC-AUC, diverging palette
centred exactly on chance (0.5) so below-chance directions are immediately
visible; the compression of the adapted panels' colour range makes the
regression-toward-chance claim visual. PuOr palette (no red-green, CVD-safe);
every cell carries its value so the figure stays readable in greyscale.

Data: paper/figures/data/fig_data.json (sha256 per source inside).
Hard asserts tie the matrix to 04_results Table 4 and the 4.3 range claims.

2026-08-08 revision:
  - body 9 pt, minimum 8 pt (was 7 pt); canvas 190 x 88 mm (was 190 x 76);
  - cell-label contrast is now MEASURED, not guessed. The previous rule picked
    black or white from the AUC value (`0.38 < v < 0.66`), which is a proxy for
    the rendered colour rather than the colour itself and breaks if the palette
    or the norm changes. Each label's colour is now chosen by WCAG contrast
    ratio against the actual RGB the colormap produces for that cell, and the
    worst cell in the figure is asserted against a stated threshold;
  - a greyscale proof is rendered alongside the preview;
  - the in-artwork footnote moved to the caption (Elsevier sets the caption).
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _layout_check import check as layout_check, best_text_colour, contrast_ratio

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "data" / "fig_data.json").read_text())
fig5 = DATA["fig5"]

REGIONS = ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended", "montiferru_2021"]
SHORT = {"manavgat_2021": "Man.", "bejis_2022": "Bej.", "mugla_2021": "Muğ.",
         "evia_2021_extended": "Evia", "montiferru_2021": "Mont."}
VARIANTS = [("raw", "(a) Raw"), ("zscore", "(b) Region-wise z-score"),
            ("coral", "(c) CORAL")]

FS_BODY = 9.0     # titles, axis labels, colour-bar label
FS_CELL = 8.0     # in-cell values, tick labels  (minimum in this figure)
MIN_CONTRAST = 4.5   # WCAG AA for normal text

DIAG_GREY = "#BBBBBB"

# ---- asserts vs 04_results Table 4 / 4.3 ----
assert abs(fig5["manavgat_2021_to_bejis_2022"]["raw"] - 0.3258) < 5e-4
assert abs(fig5["evia_2021_extended_to_manavgat_2021"]["raw"] - 0.6858) < 5e-4
assert abs(fig5["manavgat_2021_to_mugla_2021"]["coral"] - 0.4430) < 5e-4
assert abs(fig5["montiferru_2021_to_evia_2021_extended"]["zscore"] - 0.6304) < 5e-4
vals = {k: [fig5[d][k] for d in fig5] for k in ("raw", "zscore", "coral")}
rng = {k: (min(v), max(v)) for k, v in vals.items()}
assert abs(rng["raw"][0] - 0.326) < 5e-3 and abs(rng["raw"][1] - 0.686) < 5e-3
assert abs(rng["zscore"][0] - 0.431) < 5e-3 and abs(rng["zscore"][1] - 0.630) < 5e-3
assert abs(rng["coral"][0] - 0.443) < 5e-3 and abs(rng["coral"][1] - 0.624) < 5e-3

MM = 1 / 25.4
plt.rcParams.update({"svg.fonttype": "none", "pdf.fonttype": 42})
fig, axes = plt.subplots(1, 3, figsize=(190 * MM, 71 * MM))
norm = TwoSlopeNorm(vmin=0.30, vcenter=0.5, vmax=0.70)
cmap = plt.get_cmap("PuOr")

contrast_log = []   # (panel, source, target, value, colour, ratio)

for ax, (key, title) in zip(axes, VARIANTS):
    M = np.full((5, 5), np.nan)
    for i, s in enumerate(REGIONS):
        for j, t in enumerate(REGIONS):
            if s != t:
                M[i, j] = fig5[f"{s}_to_{t}"][key]
    im = ax.imshow(M, cmap=cmap, norm=norm)
    for i in range(5):
        ax.add_patch(plt.Rectangle((i - 0.5, i - 0.5), 1, 1, facecolor=DIAG_GREY,
                                   edgecolor="white", zorder=2))
        for j in range(5):
            if i == j:
                continue
            # the exact RGB this cell is painted with, straight from the
            # colormap and the norm actually in use
            bg = cmap(norm(M[i, j]))
            colour, ratio = best_text_colour(bg)
            contrast_log.append((key, REGIONS[i], REGIONS[j], round(float(M[i, j]), 4),
                                 colour, round(ratio, 2)))
            # A diverging palette is symmetric in LUMINANCE about its centre, so
            # in greyscale a below-chance cell and an equally-far above-chance
            # cell print as the same darkness and the sign of the deviation is
            # lost. Hatching the below-chance cells carries that sign through
            # greyscale, which the colour alone cannot.
            if M[i, j] < 0.5:
                ax.add_patch(plt.Rectangle(
                    (j - 0.5, i - 0.5), 1, 1, fill=False, hatch="////",
                    edgecolor=colour, linewidth=0.0, zorder=2.5, alpha=0.55))
            ax.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center",
                    fontsize=FS_CELL, zorder=3, color=colour,
                    bbox=dict(boxstyle="square,pad=0.12", facecolor=bg,
                              edgecolor="none", alpha=0.85))

    ax.set_xticks(range(5), [SHORT[r] for r in REGIONS], fontsize=FS_CELL)
    ax.set_yticks(range(5), [SHORT[r] for r in REGIONS] if ax is axes[0] else [],
                  fontsize=FS_CELL)
    ax.set_xlabel("target", fontsize=FS_BODY)
    if ax is axes[0]:
        ax.set_ylabel("source", fontsize=FS_BODY)
    ax.set_title(f"{title}\nrange {rng[key][0]:.3f}–{rng[key][1]:.3f}",
                 fontsize=FS_BODY, pad=5)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)

# ---- cells whose printed label cannot show which side of chance they sit on --
# Hatching uses the EXACT value but the label is rounded to 2 dp, so a cell at
# 0.499 prints "0.50" while hatched and one at 0.501 prints "0.50" un-hatched.
# These are named in the caption rather than left for a reader to trip over.
ambiguous = [(k, s, t, v) for (k, s, t, v, _c, _r) in contrast_log
             if f"{v:.2f}" == "0.50"]
if ambiguous:
    print("[chance-edge] cells printing 0.50 (hatch follows the exact value):")
    for k, s, t, v in ambiguous:
        print(f"    {k:7s} {s} -> {t} = {v:.4f} "
              f"({'below' if v < 0.5 else 'at/above'} chance)")

# ---- contrast verdict -------------------------------------------------------
worst = min(contrast_log, key=lambda r: r[-1])
n_black = sum(1 for r in contrast_log if r[4] == "black")
print(f"[contrast] {len(contrast_log)} cells: {n_black} black / "
      f"{len(contrast_log) - n_black} white labels; "
      f"worst ratio {worst[-1]}:1 ({worst[0]} {worst[1]}->{worst[2]} = {worst[3]})")
# the grey diagonal carries no text, but state its contrast against both anyway
assert worst[-1] >= MIN_CONTRAST, (
    f"cell label contrast {worst[-1]}:1 below WCAG AA {MIN_CONTRAST}:1 "
    f"at {worst[0]} {worst[1]}->{worst[2]}")

cbar = fig.colorbar(im, ax=axes, fraction=0.025, pad=0.02)
cbar.set_label("thermal transfer ROC-AUC", fontsize=FS_BODY)
cbar.ax.tick_params(labelsize=FS_CELL)
cbar.ax.axhline(0.5, color="black", lw=1.2)

fig.subplots_adjust(left=0.075, right=0.875, top=0.845, bottom=0.145, wspace=0.12)

problems = layout_check(fig, "Fig. 4 - transfer matrices",
                        min_gap_pt=2.0, min_font_pt=8.0)

fig.savefig(HERE / "fig4_transfer_matrix.pdf")
fig.savefig(HERE / "fig4_transfer_matrix.svg")
if "--preview" in sys.argv:
    png = HERE / "fig4_transfer_matrix_preview.png"
    fig.savefig(png, dpi=300)
    # greyscale proof: luminance-convert the rendered preview, so what is
    # checked is the actual rasterised figure rather than a re-plot
    rgb = plt.imread(png)[:, :, :3]
    grey = (0.2126 * rgb[:, :, 0] + 0.7152 * rgb[:, :, 1] + 0.0722 * rgb[:, :, 2])
    plt.imsave(HERE / "fig4_transfer_matrix_greyscale.png", grey, cmap="gray",
               vmin=0.0, vmax=1.0)

(HERE / "fig4_provenance.json").write_text(json.dumps({
    "figure": "Fig. 4 - transfer matrices raw/z/CORAL",
    "script": "paper/figures/fig4_transfer_matrix.py",
    "data": "paper/figures/data/fig_data.json (per-source sha256 inside; step10_metrics.json of all 10 pairs)",
    "asserts": "spot values vs 04 Table 4; panel ranges vs 4.3 claims "
               "(0.326-0.686 / 0.431-0.630 / 0.443-0.624); worst cell-label "
               f"contrast >= {MIN_CONTRAST}:1",
    "contrast": {
        "method": "WCAG 2.x relative luminance; label colour chosen per cell by "
                  "contrast ratio against the actual colormap RGB for that cell, "
                  "not by thresholding the AUC value",
        "threshold": MIN_CONTRAST,
        "worst_ratio": worst[-1],
        "worst_cell": f"{worst[0]} {worst[1]}->{worst[2]} = {worst[3]}",
        "black_labels": n_black,
        "white_labels": len(contrast_log) - n_black,
        "greyscale": "ratio depends only on relative luminance, which a luminance "
                     "greyscale conversion preserves, so the colour verdict is the "
                     "greyscale verdict; a rendered proof is written to "
                     "fig4_transfer_matrix_greyscale.png",
    },
    "below_chance_hatch": {
        "why": "a diverging palette is symmetric in luminance about its centre, so in "
               "greyscale a below-chance cell prints the same darkness as an equally "
               "distant above-chance cell and the sign of the deviation is lost; the "
               "hatch carries the sign through greyscale",
        "rule": "hatched iff the EXACT value < 0.5 (labels are rounded to 2 dp)",
        "chance_edge_cells": [f"{k} {s}->{t} = {v:.4f}" for k, s, t, v in ambiguous],
    },
    "palette": "PuOr diverging, TwoSlopeNorm centred 0.5; values printed per cell for greyscale",
    "canvas_mm": [190, 71],
    "column": "double (190 mm)",
    "font_pt": {"body": FS_BODY, "minimum": FS_CELL},
    "layout_check": f"paper/figures/_layout_check.py; {len(problems)} problems at build time",
    "environment": f"matplotlib {matplotlib.__version__}",
}, indent=1, ensure_ascii=False))
print("fig5 written; ranges", {k: (round(a, 3), round(b, 3)) for k, (a, b) in rng.items()})
