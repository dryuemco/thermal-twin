#!/usr/bin/env python3
"""Figure 6 - interventions obey the same conservation.

(a) Label-blind adaptation, four-AOI decomposition (12 directions): raw (open) ->
    best-adapted (filled) along the AUC axis; within-region reference as grey tick.
    Directions where adaptation moves AWAY from the within reference (negative
    recovery, 7/12) in orange; recoveries in blue. Compression toward chance visible.
(b) LORO pooled training per held-out target: pooled model never beats the best
    pairwise source; within ceiling far right.
(c) Feature removal: mean within vs mean transfer for the four configurations -
    the trade-off line (what transfer gains, within-region skill pays).
Okabe-Ito, greyscale-safe, vector, min font 7 pt.
Data: paper/figures/data/fig_data.json. Asserts vs 04_results 4.3/4.6.
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "data" / "fig_data.json").read_text())
decomp = DATA["fig6_decomp"]
loro = DATA["fig6_loro"]
fdrop = {r["config"]: r for r in DATA["fig6_fdrop"]}

BLUE, ORANGE, GREY = "#0072B2", "#E69F00", "#666666"
LABEL = {"manavgat_2021": "Manavgat", "bejis_2022": "Bejís", "mugla_2021": "Muğla",
         "evia_2021_extended": "Evia", "montiferru_2021": "Montiferru"}
def dirlabel(d):
    s, t = d.split("_to_")
    return f"{LABEL[s]}→{LABEL[t]}"

# ---- asserts vs 04_results ----
neg = [d for d in decomp if d["best_adapted"] < d["raw"]]
assert len(neg) == 7, f"expected 7 negative-recovery directions, got {len(neg)}"
worst = min(decomp, key=lambda d: d["recovered_fraction"])
assert worst["direction"] == "evia_2021_extended_to_manavgat_2021"
assert abs(worst["recovered_fraction"] - (-0.8619)) < 5e-3
by_t = {r["target"]: r for r in loro}
assert abs(by_t["manavgat_2021"]["loro_raw"] - 0.469) < 5e-3
for r in loro:
    assert r["loro_raw"] < r["best_pairwise"], f"LORO must not beat best pairwise: {r['target']}"
assert abs(fdrop["full"]["mean_within"] - 0.888) < 5e-3
assert abs(fdrop["full"]["mean_transfer"] - 0.541) < 5e-3
assert abs(fdrop["drop_both"]["mean_within"] - 0.807) < 5e-3
assert abs(fdrop["drop_both"]["mean_transfer"] - 0.556) < 5e-3

MM = 1 / 25.4
fig = plt.figure(figsize=(190 * MM, 95 * MM))
plt.rcParams.update({"svg.fonttype": "none", "pdf.fonttype": 42})
gs = fig.add_gridspec(1, 3, width_ratios=[1.5, 1.0, 0.95],
                      left=0.185, right=0.972, top=0.90, bottom=0.115, wspace=0.44)
axA = fig.add_subplot(gs[0, 0])
axB = fig.add_subplot(gs[0, 1])
axC = fig.add_subplot(gs[0, 2])

# (a) decomposition
order = sorted(decomp, key=lambda d: d["raw"])
for y, d in enumerate(order):
    colour = ORANGE if d["best_adapted"] < d["raw"] else BLUE
    axA.annotate("", xy=(d["best_adapted"], y), xytext=(d["raw"], y),
                 arrowprops=dict(arrowstyle="-|>", color=colour, lw=1.5,
                                 mutation_scale=8, shrinkA=0, shrinkB=0))
    axA.plot(d["raw"], y, marker="o", mfc="white", mec=colour, ms=4.5, zorder=3)
    axA.plot([d["within"], d["within"]], [y - 0.32, y + 0.32], color=GREY, lw=1.6,
             zorder=2)
axA.axvline(0.5, color="black", lw=0.8, ls=(0, (4, 2)))
axA.set_yticks(range(len(order)), [dirlabel(d["direction"]) for d in order],
               fontsize=7)
axA.set_xlim(0.28, 0.97)
axA.set_xlabel("thermal ROC-AUC", fontsize=8)
axA.set_title("(a) Adaptation compresses toward chance\n"
              "raw ○ → best adapted; grey | = within",
              fontsize=8, loc="left")
axA.text(0.505, len(order) - 0.4, "chance", fontsize=7, style="italic",
         ha="left", va="top")
hB = plt.Line2D([], [], color=BLUE, lw=2)
hO = plt.Line2D([], [], color=ORANGE, lw=2)
axA.legend([hB, hO], ["recovery (5)", "negative recovery (7)"], fontsize=7,
           frameon=False, loc="lower right", handlelength=1.2)

# (b) LORO
ysB = list(range(len(loro)))[::-1]
for r, y in zip(loro, ysB):
    axB.plot([r["loro_raw"], r["best_pairwise"]], [y, y], color="#BBBBBB", lw=1.0,
             zorder=1)
    axB.plot(r["best_pairwise"], y, marker="D", mfc="white", mec=BLUE, ms=4.5,
             zorder=3)
    axB.plot(r["loro_raw"], y, marker="o", mfc=ORANGE, mec=ORANGE, ms=4.5, zorder=3)
    axB.plot([r["within"], r["within"]], [y - 0.28, y + 0.28], color=GREY, lw=1.6)
axB.axvline(0.5, color="black", lw=0.8, ls=(0, (4, 2)))
axB.set_yticks(ysB, [LABEL[r["target"]] for r in loro], fontsize=7.5)
axB.set_xlim(0.35, 0.99)
axB.set_xlabel("thermal ROC-AUC", fontsize=8)
axB.set_title("(b) Pooling never beats the\nbest single source", fontsize=8,
              loc="left")
hP = plt.Line2D([], [], marker="D", mfc="white", mec=BLUE, ls="", ms=4.5)
hL = plt.Line2D([], [], marker="o", color=ORANGE, ls="", ms=4.5)
hW = plt.Line2D([], [], color=GREY, lw=1.6)
axB.legend([hL, hP, hW], ["LORO pooled", "best pairwise", "within"], fontsize=7,
           frameon=False, loc="lower right", handlelength=1.0)

# (c) feature drop trade-off
CFG = [("full", "full"), ("drop_anom", "− LST anomaly"),
       ("drop_elev", "− elevation"), ("drop_both", "− both")]
xs = [fdrop[c]["mean_within"] for c, _ in CFG]
ys = [fdrop[c]["mean_transfer"] for c, _ in CFG]
path = ["full", "drop_anom", "drop_elev", "drop_both"]
axC.plot([fdrop[c]["mean_within"] for c in path],
         [fdrop[c]["mean_transfer"] for c in path],
         color="#BBBBBB", lw=1.0, zorder=1)
for (c, lab), x, y in zip(CFG, xs, ys):
    filled = c in ("full", "drop_both")
    axC.plot(x, y, marker="o", ms=5.5, mfc=(BLUE if filled else "white"), mec=BLUE,
             zorder=3)
    dx, dy = (-0.0035, 0.0012) if c != "full" else (0.002, -0.0022)
    ha = "right" if c != "full" else "left"
    axC.text(x + dx, y + dy, lab, fontsize=7, ha=ha, va="bottom")
axC.set_xlabel("mean within AUC (5 regions)", fontsize=8)
axC.set_ylabel("mean transfer AUC (20 directions)", fontsize=8)
axC.set_title("(c) Feature removal:\nzero-sum trade-off", fontsize=8, loc="left")
axC.set_xlim(0.795, 0.90)
axC.set_ylim(0.536, 0.562)
for ax in (axA, axB, axC):
    ax.tick_params(labelsize=7.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

fig.savefig(HERE / "fig6_conservation.pdf")
fig.savefig(HERE / "fig6_conservation.svg")
if "--preview" in sys.argv:
    fig.savefig(HERE / "fig6_conservation_preview.png", dpi=220)

(HERE / "fig6_provenance.json").write_text(json.dumps({
    "figure": "Fig. 6 - interventions obey the same conservation (adaptation, LORO, feature drop)",
    "script": "paper/figures/fig6_conservation.py",
    "data": "paper/figures/data/fig_data.json (four_aoi_decomposition.csv, loro_pooled_transfer.json, feature_drop_transfer.json; sha256 inside)",
    "asserts": "7/12 negative recovery, worst Evia->Manavgat -0.862; LORO never beats best pairwise (5 targets), Manavgat 0.469; feature-drop means 0.888/0.541 -> 0.807/0.556",
    "palette": "Okabe-Ito blue/orange + grey; markers distinct; no red-green",
    "min_font_pt": 7.0,
    "environment": f"matplotlib {matplotlib.__version__}",
}, indent=1))
print("fig6 written; negative recovery:", len(neg), "of", len(decomp))
