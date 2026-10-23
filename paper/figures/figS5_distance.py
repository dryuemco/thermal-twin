#!/usr/bin/env python3
"""Fig. S5 - within-region skill by distance from the training cells (Additional file 1, 2026-10-23).

A model fitted on one half of a region scores the other half; target cells are binned by their
distance from the training cells, and each dot is the unweighted mean ROC-AUC over the bins of that
distance class in the five regions (the number of bins is under each class). The last dot is the mean
of the twenty cross-region directions, 306 to 2,802 km apart. Replaces former Table S32.

Data: paper/labelfix_rerun/round7/r7h_distance_curve.csv (summary of round3/distance_curve.json).
"""
import csv
import hashlib
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _layout_check import check as layout_check, assert_inside
import _style as S

SRC = HERE.parent / "labelfix_rerun" / "round7" / "r7h_distance_curve.csv"
rows = list(csv.DictReader(SRC.open(encoding="utf-8")))
near = [r for r in rows if r["bin_lo_km"] != "cross"]
cross = [r for r in rows if r["bin_lo_km"] == "cross"][0]
auc = [float(r["mean_auc"]) for r in near]
assert len(near) == 6 and [r["bins"] for r in near] == ["18", "16", "11", "6", "3", "1"]
# the main text quotes the first three classes and the cross-region mean
R04 = " ".join((HERE.parent / "04_results.md").read_text(encoding="utf-8").split())
for s in ("0.709 within 5 km", "0.570 at 5 to 10 km", "0.519 at 10 to 20 km"):
    assert s in R04, s
assert f"{float(cross['mean_auc']):.3f}" == "0.527" and cross["bins"] == "20"
assert min(int(r["min_pos"]) for r in near) == 1 and max(int(r["max_pos"]) for r in near) == 1067

S.apply()
fig, ax = plt.subplots(figsize=(110 * S.MM, 52 * S.MM))
xs = list(range(len(near)))
xc = len(near) + 0.8
S.chance(ax, axis="y")
ln, = ax.plot(xs, auc, color=S.BLUE, lw=1.0, zorder=2)
pt, = ax.plot(xs, auc, "o", ms=4.6, color=S.BLUE, zorder=3)
cr, = ax.plot(xc, float(cross["mean_auc"]), "o", ms=4.6, mfc="white", mec=S.BLUE, mew=1.0, zorder=3)
ticks = [f"{r['bin_lo_km']}–{r['bin_hi_km']}\n{r['bins']}" for r in near] + ["306–2,802\n20"]
ax.set_xticks(xs + [xc], ticks)
ax.text(xc, float(cross["mean_auc"]) + 0.03, "across\nregions", ha="center", va="bottom",
        fontsize=S.FS_SMALL, color=S.MUTED, linespacing=1.0)
ax.set_xlim(-0.5, xc + 0.6)
ax.set_ylim(0.40, 0.75); ax.set_yticks([0.4, 0.5, 0.6, 0.7])
ax.set_ylabel("mean ROC-AUC")
ax.set_xlabel("distance from the training cells (km); number of bins")
ax.tick_params(axis="x", length=0)
assert_inside(ax, "Fig. S5", xs=xs + [xc], ys=auc + [float(cross["mean_auc"])])
fig.subplots_adjust(left=0.14, right=0.98, top=0.95, bottom=0.33)
problems = layout_check(fig, "Fig. S5 - distance", min_gap_pt=2.0, min_font_pt=8.0,
                        data_artists=[(ln, "curve"), (pt, "bins"), (cr, "cross-region")])
S.save(fig, HERE, "figS5_distance")
fig.savefig(HERE / "figS5_distance.png", dpi=300)
(HERE / "figS5_provenance.json").write_text(json.dumps({
    "figure": "Fig. S5 - within-region skill by distance from the training cells",
    "script": "paper/figures/figS5_distance.py",
    "data": {"path": "paper/labelfix_rerun/round7/r7h_distance_curve.csv",
             "sha256": hashlib.sha256(SRC.read_bytes()).hexdigest()},
    "asserts": "bin counts 18/16/11/6/3/1; 0.709, 0.570 and 0.519 as quoted in 04_results.md; cross-region "
               "mean 0.527 over 20 directions; 1 to 1,067 burned cells per bin",
    "canvas_mm": [110, 52],
    "layout_check": f"paper/figures/_layout_check.py; {len(problems)} problems at build time",
    "environment": f"matplotlib {matplotlib.__version__}",
}, indent=1, ensure_ascii=False), encoding="utf-8")
print("figS5 written")
TEXT = " ".join((HERE.parent / "supplementary.md").read_text(encoding="utf-8").split())
assert "Fig. S5" in TEXT, "Section S2.2 must cite Fig. S5"
