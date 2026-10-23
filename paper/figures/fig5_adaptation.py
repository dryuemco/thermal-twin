#!/usr/bin/env python3
"""Figure 5 - label-free adaptation moves transfer toward chance (2026-10-23 redraw).

All 20 ordered directions, sorted by raw transfer ROC-AUC. In each panel a row joins the raw
value (open grey circle) to the adapted value (filled blue dot): (a) region-wise z-score,
(b) CORAL after region-wise z-score. Neither method uses target labels.

The earlier version showed the 12 directions of the pipeline's gap decomposition with an
arrow to the better of the two methods, a choice that uses target labels, plus CORAL crosses
and within-region ticks; it is in the git history before 2026-10-23. The decomposition and its
asserts stay in _conservation_common.py and Section S1.10.

Data: paper/figures/data/fig_data_corrected.json. Asserts: all 60 values against Table S16
(via _conservation_common.py); the means, ranges and counts printed in 04 Section 3.5 and in
the caption.
"""
import json
import statistics
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _layout_check import check as layout_check, assert_inside
from _conservation_common import HERE, DATA, B9, LABEL
import _style as S

NAME = {**LABEL, "evia_2021_extended": "North Evia"}


def dirlabel(d):
    s, t = d.split("_to_")
    return f"{NAME[s]}→{NAME[t]}"

T = DATA["fig5"]
assert len(T) == 20
for _d, _row in T.items():                      # every plotted value as printed in Table S16
    for _k in ("raw", "zscore", "coral"):
        assert f"{_row[_k]:.3f}" == B9[_d][_k], (_d, _k)

MEAN = {k: statistics.mean(r[k] for r in T.values()) for k in ("raw", "zscore", "coral")}
CLOSER = {k: sum(abs(r[k] - 0.5) < abs(r["raw"] - 0.5) for r in T.values()) for k in ("zscore", "coral")}
# 04 Section 3.5: CORAL moved 16 of 20 closer to chance and the mean fell from 0.527 to 0.517;
# the caption adds the z-score count and mean
assert (f"{MEAN['raw']:.3f}", f"{MEAN['coral']:.3f}", f"{MEAN['zscore']:.3f}") == ("0.527", "0.517", "0.510"), MEAN
assert CLOSER == {"zscore": 13, "coral": 16}, CLOSER
RANGE = {k: (min(r[k] for r in T.values()), max(r[k] for r in T.values())) for k in ("zscore", "coral")}
assert tuple(f"{v:.3f}" for v in RANGE["zscore"]) == ("0.302", "0.630")
assert tuple(f"{v:.3f}" for v in RANGE["coral"]) == ("0.406", "0.624")

S.apply()
fig, axes = plt.subplots(1, 2, figsize=(S.WIDTH_MM * S.MM, 118 * S.MM), sharey=True)
order = sorted(T, key=lambda d: T[d]["raw"])
data_artists = []
for ax, (key, title) in zip(axes, (("zscore", "(a) Region-wise z-score"), ("coral", "(b) Region-wise z-score + CORAL"))):
    S.chance(ax)
    for y, d in enumerate(order):
        raw, ad = T[d]["raw"], T[d][key]
        seg, = ax.plot([raw, ad], [y, y], color="#CFCFCF", lw=1.4, solid_capstyle="butt", zorder=1)
        r, = ax.plot(raw, y, marker="o", ms=4.5, mfc="white", mec=S.GREY, mew=1.0, lw=0, zorder=2)
        a, = ax.plot(ad, y, marker="o", ms=4.5, color=S.BLUE, lw=0, zorder=3)
        data_artists += [(r, f"raw:{d}"), (a, f"{key}:{d}")]
    ax.set_title(title)
    ax.set_xlim(0.28, 0.72)
    ax.set_xticks([0.3, 0.4, 0.5, 0.6, 0.7])
    assert_inside(ax, f"Fig. 5 {key}", xs=[T[d][k] for d in order for k in ("raw", key)])
axes[0].set_yticks(range(len(order)), [dirlabel(d) for d in order])
axes[0].set_ylim(-0.7, len(order) - 0.3)
axes[1].tick_params(axis="y", left=False)
axes[1].spines["left"].set_visible(False)

handles = [plt.Line2D([], [], marker="o", ms=4.5, mfc="white", mec=S.GREY, mew=1.0, lw=0),
           plt.Line2D([], [], marker="o", ms=4.5, color=S.BLUE, lw=0)]
axes[0].legend(handles, ["raw transfer", "after adaptation"], loc="lower right",
               handletextpad=0.3, labelspacing=0.3, borderaxespad=0.2)
fig.supxlabel("ROC-AUC in the target region", fontsize=S.FS_BODY, y=0.005)
fig.subplots_adjust(left=0.22, right=0.985, top=0.95, bottom=0.095, wspace=0.08)

problems = layout_check(fig, "Fig. 5 - adaptation", min_gap_pt=2.0, min_font_pt=8.0,
                        data_artists=data_artists)
S.save(fig, HERE, "fig5_adaptation")

(HERE / "fig5_provenance.json").write_text(json.dumps({
    "figure": "Fig. 5 - label-free adaptation moves transfer toward chance",
    "script": "paper/figures/fig5_adaptation.py",
    "data": {"path": "paper/figures/data/fig_data_corrected.json",
             "sha256": __import__("hashlib").sha256(
                 (HERE / "data" / "fig_data_corrected.json").read_bytes()).hexdigest(),
             "note": "step10_metrics.json of all 10 pairs, corrected-label overlay; sha256 inside"},
    "asserts": "all 60 plotted values equal Table S16 at 3 dp; means raw 0.527, z-score 0.510, "
               "CORAL 0.517; 13 (z-score) and 16 (CORAL) of 20 directions closer to chance; ranges "
               "0.302-0.630 and 0.406-0.624; the decomposition asserts in _conservation_common.py",
    "design": "2026-10-23 redraw: 20 directions, raw (open grey) to adapted (filled blue), one panel per "
              "method; no target-label choice of method",
    "canvas_mm": [S.WIDTH_MM, 118],
    "font_pt": {"body": S.FS_BODY, "minimum": S.FS_SMALL},
    "layout_check": f"paper/figures/_layout_check.py; {len(problems)} problems at build time",
    "environment": f"matplotlib {matplotlib.__version__}",
}, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"fig5 written; closer to chance {CLOSER}; means { {k: round(v, 3) for k, v in MEAN.items()} }")
