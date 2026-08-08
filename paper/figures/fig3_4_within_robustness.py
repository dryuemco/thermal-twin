#!/usr/bin/env python3
"""Figures 3+4 combined - within-region thermal increment and block-size robustness.

(a) Baseline vs thermal ROC-AUC per region at the default 2-cell (~1 km) blocking
    (dumbbells) with the paired-delta CI annotated.
(b) Absolute thermal AUC vs block size (2/10/20 cells ~ 1/5/10 km): declines.
(c) Thermal ΔAUC vs block size with 95% CIs: stays above zero everywhere.
Okabe-Ito colours + distinct markers (greyscale-safe); vector; min font 7 pt.
Data: paper/figures/data/fig_data.json. Asserts vs 04_results Table 3.
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

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
BLOCK_LABEL = {"2": "2 (~1 km)", "10": "10 (~5 km)", "20": "20 (~10 km)"}

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

MM = 1 / 25.4
fig, (axA, axB, axC) = plt.subplots(
    1, 3, figsize=(190 * MM, 72 * MM), width_ratios=[1.15, 1.0, 1.0])
plt.rcParams.update({"svg.fonttype": "none", "pdf.fonttype": 42})

# (a) dumbbells at block 2
ys = list(range(len(REGIONS)))[::-1]
for reg, y in zip(REGIONS, ys):
    d = fig34[reg]["2"]
    c = COLOUR[reg]
    axA.plot([d["baseline"], d["thermal"]], [y, y], color=c, lw=1.6, zorder=2)
    axA.plot(d["baseline"], y, marker=MARKER[reg], mfc="white", mec=c, ms=5.5,
             zorder=3)
    axA.plot(d["thermal"], y, marker=MARKER[reg], mfc=c, mec=c, ms=5.5, zorder=3)
    axA.text(d["thermal"] + 0.012, y,
             f"+{d['delta']:.3f} [{d['delta_ci'][0]:.3f}, {d['delta_ci'][1]:.3f}]",
             fontsize=7, va="center")
axA.set_yticks(ys, [LABEL[r] for r in REGIONS], fontsize=8)
axA.set_xlim(0.70, 1.045)
axA.set_xticks([0.70, 0.75, 0.80, 0.85, 0.90, 0.95])
axA.set_xlabel("ROC-AUC (2-cell blocks)", fontsize=8)
axA.set_title("(a) Baseline (open) vs thermal (filled)", fontsize=8, loc="left")
axA.tick_params(labelsize=7.5)

# (b) absolute thermal AUC vs block size; (c) delta vs block size
x = range(len(BLOCKS))
for reg in REGIONS:
    c = COLOUR[reg]
    m = MARKER[reg]
    axB.plot(x, [fig34[reg][b]["thermal"] for b in BLOCKS], color=c, marker=m,
             ms=4.5, lw=1.4, label=LABEL[reg])
    deltas = [fig34[reg][b]["delta"] for b in BLOCKS]
    err = [[fig34[reg][b]["delta"] - fig34[reg][b]["delta_ci"][0] for b in BLOCKS],
           [fig34[reg][b]["delta_ci"][1] - fig34[reg][b]["delta"] for b in BLOCKS]]
    axC.errorbar(x, deltas, yerr=err, color=c, marker=m, ms=4.5, lw=1.4,
                 capsize=2, elinewidth=0.9)
for ax, title, ylab in ((axB, "(b) Thermal AUC declines",
                         "thermal ROC-AUC"),
                        (axC, "(c) ΔAUC survives coarser blocks",
                         "ΔAUC (thermal − baseline)")):
    ax.set_xticks(list(x), [BLOCK_LABEL[b] for b in BLOCKS], fontsize=7)
    ax.set_title(title, fontsize=8, loc="left")
    ax.set_ylabel(ylab, fontsize=8)
    ax.tick_params(labelsize=7.5)
axC.axhline(0, color="black", lw=0.8, ls=(0, (4, 2)))
axC.set_ylim(-0.01, 0.24)
axB.legend(fontsize=7, frameon=False, handlelength=1.4, labelspacing=0.3,
           loc="lower left")
for ax in (axA, axB, axC):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
fig.subplots_adjust(left=0.105, right=0.965, top=0.90, bottom=0.145, wspace=0.42)

fig.savefig(HERE / "fig3_4_within_robustness.pdf")
fig.savefig(HERE / "fig3_4_within_robustness.svg")
if "--preview" in sys.argv:
    fig.savefig(HERE / "fig3_4_within_robustness_preview.png", dpi=220)

(HERE / "fig3_4_provenance.json").write_text(json.dumps({
    "figure": "Figs 3+4 combined - within-region increment and block robustness",
    "script": "paper/figures/fig3_4_within_robustness.py",
    "data": "paper/figures/data/fig_data.json (step8c + robustness outputs; per-source sha256 inside)",
    "asserts": "spot values vs 04 Table 3; every delta CI lower bound > 0 (15 region-block cells)",
    "palette": "Okabe-Ito 5-colour + distinct markers for greyscale; no red-green pair",
    "min_font_pt": 7.0,
    "environment": f"matplotlib {matplotlib.__version__}",
}, indent=1))
print("fig3_4 written; all 15 delta CIs exclude zero")
