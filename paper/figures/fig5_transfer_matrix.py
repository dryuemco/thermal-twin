#!/usr/bin/env python3
"""Figure 5 - cross-region transfer matrices: raw / region-wise z-score / CORAL.

Three 5x5 source-x-target heatmaps of thermal transfer ROC-AUC, diverging palette
centred exactly on chance (0.5) so below-chance directions are immediately visible,
and the compression of the adapted panels' colour range makes the
regression-toward-chance claim visual. PuOr palette (no red-green, CVD-safe);
every cell carries its value so the figure stays readable in greyscale.
Data: paper/figures/data/fig_data.json (sha256 per source inside).
Hard asserts tie the matrix to 04_results Table 4 and the 4.3 range claims.
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "data" / "fig_data.json").read_text())
fig5 = DATA["fig5"]

REGIONS = ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended", "montiferru_2021"]
SHORT = {"manavgat_2021": "Man.", "bejis_2022": "Bej.", "mugla_2021": "Muğ.",
         "evia_2021_extended": "Evia", "montiferru_2021": "Mont."}
VARIANTS = [("raw", "(a) Raw"), ("zscore", "(b) Region-wise z-score"),
            ("coral", "(c) CORAL")]

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
fig, axes = plt.subplots(1, 3, figsize=(190 * MM, 76 * MM))
plt.rcParams.update({"svg.fonttype": "none", "pdf.fonttype": 42})
norm = TwoSlopeNorm(vmin=0.30, vcenter=0.5, vmax=0.70)
cmap = plt.get_cmap("PuOr")

for ax, (key, title) in zip(axes, VARIANTS):
    M = np.full((5, 5), np.nan)
    for i, s in enumerate(REGIONS):
        for j, t in enumerate(REGIONS):
            if s != t:
                M[i, j] = fig5[f"{s}_to_{t}"][key]
    im = ax.imshow(M, cmap=cmap, norm=norm)
    for i in range(5):
        ax.add_patch(plt.Rectangle((i - 0.5, i - 0.5), 1, 1, facecolor="#BBBBBB",
                                   edgecolor="white", zorder=2))
        for j in range(5):
            if i != j:
                ax.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center",
                        fontsize=7, zorder=3,
                        color="black" if 0.38 < M[i, j] < 0.66 else "white")
    ax.set_xticks(range(5), [SHORT[r] for r in REGIONS], fontsize=7)
    ax.set_yticks(range(5), [SHORT[r] for r in REGIONS] if ax is axes[0] else [],
                  fontsize=7)
    ax.set_xlabel("target", fontsize=7.5)
    if ax is axes[0]:
        ax.set_ylabel("source", fontsize=7.5)
    ax.set_title(f"{title}\nrange {rng[key][0]:.3f}–{rng[key][1]:.3f}",
                 fontsize=8, pad=4)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)

cbar = fig.colorbar(im, ax=axes, fraction=0.025, pad=0.015)
cbar.set_label("thermal transfer ROC-AUC", fontsize=7.5)
cbar.ax.tick_params(labelsize=7)
cbar.ax.axhline(0.5, color="black", lw=1.0)
fig.text(0.005, 0.02,
         "Diverging palette centred on chance (0.5, black line on the colour bar); "
         "grey diagonal = within-region (not transfer). CIs in Table 4.",
         fontsize=7)
fig.subplots_adjust(left=0.075, right=0.88, top=0.86, bottom=0.20, wspace=0.12)

fig.savefig(HERE / "fig5_transfer_matrix.pdf")
fig.savefig(HERE / "fig5_transfer_matrix.svg")
if "--preview" in sys.argv:
    fig.savefig(HERE / "fig5_transfer_matrix_preview.png", dpi=220)

(HERE / "fig5_provenance.json").write_text(json.dumps({
    "figure": "Fig. 5 - transfer matrices raw/z/CORAL",
    "script": "paper/figures/fig5_transfer_matrix.py",
    "data": "paper/figures/data/fig_data.json (per-source sha256 inside; step10_metrics.json of all 10 pairs)",
    "asserts": "spot values vs 04 Table 4; panel ranges vs 4.3 claims (0.326-0.686 / 0.431-0.630 / 0.443-0.624)",
    "palette": "PuOr diverging, TwoSlopeNorm centred 0.5; values printed per cell for greyscale",
    "min_font_pt": 7.0,
    "environment": f"matplotlib {matplotlib.__version__}",
}, indent=1))
print("fig5 written; ranges", {k: (round(a, 3), round(b, 3)) for k, (a, b) in rng.items()})
