#!/usr/bin/env python3
"""Figure 6c - removing direction-reversing features is a zero-sum trade-off.

Mean within-region AUC (5 regions) against mean transfer AUC (20 directions) for
four feature configurations. Moving left along the connecting path buys transfer
skill and pays for it in within-region skill; the two move in opposite
directions throughout.

Each configuration has its own marker and is named in a fixed legend, so no
label position depends on a data value (the labels previously sat next to their
points and crowded them). Split out of the former three-panel Fig. 6.

Data: paper/figures/data/fig_data.json. Asserts in _fig6_common.py.
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _layout_check import check as layout_check
from _fig6_common import (HERE, MM, BLUE, FS_BODY, FS_TICK, fdrop,
                          style_axes, save)

CFG = [("full", "full (all features)", "o", True),
       ("drop_anom", "− LST anomaly", "s", False),
       ("drop_elev", "− elevation", "^", False),
       ("drop_both", "− both", "D", True)]
PATH = ["full", "drop_anom", "drop_elev", "drop_both"]

# the trade-off claim itself: within falls monotonically along the path while
# transfer rises monotonically. Asserted so the figure cannot quietly contradict
# the sentence it illustrates.
_w = [fdrop[c]["mean_within"] for c in PATH]
_t = [fdrop[c]["mean_transfer"] for c in PATH]
assert all(a > b for a, b in zip(_w, _w[1:])), f"within not monotone along path: {_w}"
assert all(a < b for a, b in zip(_t, _t[1:])), f"transfer not monotone along path: {_t}"

plt.rcParams.update({"svg.fonttype": "none", "pdf.fonttype": 42})
fig = plt.figure(figsize=(190 * MM, 92 * MM))
# plot on the left, legend in its own column on the right: at 190 mm there is
# room for a real key, so nothing has to sit near a data point
ax = fig.add_axes([0.085, 0.145, 0.560, 0.775])

ax.plot(_w, _t, color="#BBBBBB", lw=1.3, zorder=1)
data_artists = []
handles = []
for cfg, lab, mk, filled in CFG:
    pt, = ax.plot(fdrop[cfg]["mean_within"], fdrop[cfg]["mean_transfer"], marker=mk,
                  ms=7.0, mfc=(BLUE if filled else "white"), mec=BLUE, mew=1.4,
                  zorder=3, ls="")
    data_artists.append((pt, f"cfg:{cfg}"))
    handles.append(plt.Line2D([], [], marker=mk, ms=7.0,
                              mfc=(BLUE if filled else "white"), mec=BLUE,
                              mew=1.4, ls="", label=lab))

ax.set_xlabel("mean within-region ROC-AUC (5 regions)", fontsize=FS_BODY)
ax.set_ylabel("mean transfer ROC-AUC (20 directions)", fontsize=FS_BODY)
ax.set_title("Feature removal is a zero-sum trade-off", fontsize=FS_BODY, loc="left")
ax.set_xlim(0.795, 0.900)
ax.set_ylim(0.5395, 0.5580)
ax.set_xticks([0.80, 0.82, 0.84, 0.86, 0.88, 0.90])
ax.set_yticks([0.540, 0.545, 0.550, 0.555])
style_axes(ax)

fig.legend(handles=handles, fontsize=FS_TICK, frameon=False, loc="center left",
           bbox_to_anchor=(0.675, 0.55), handlelength=1.4, labelspacing=1.1,
           handletextpad=0.7, title="feature configuration",
           title_fontsize=FS_TICK)
fig.text(0.675, 0.30,
         "left along the path =\ntransfer gained,\nwithin-region skill paid",
         fontsize=FS_TICK, va="top", ha="left", color="#444444", linespacing=1.6)

problems = layout_check(fig, "Fig. 6c - feature-removal trade-off", min_gap_pt=2.0,
                        min_font_pt=8.0, data_artists=data_artists)
save(fig, "fig6c_feature_drop", "--preview" in sys.argv)

(HERE / "fig6c_provenance.json").write_text(json.dumps({
    "figure": "Fig. 6c - feature removal is a zero-sum trade-off",
    "script": "paper/figures/fig6c_feature_drop.py",
    "data": "paper/figures/data/fig_data.json (feature_drop_transfer.json; sha256 inside)",
    "asserts": "means 0.888/0.541 (full) -> 0.807/0.556 (drop both) (_fig6_common.py); "
               "within strictly decreasing AND transfer strictly increasing along the "
               "full -> -anomaly -> -elevation -> -both path, i.e. the trade-off the "
               "caption claims is checked, not just drawn",
    "labels": "one marker per configuration named in a fixed legend column to the right; "
              "no label position depends on a data value",
    "canvas_mm": [190, 92],
    "column": "double (190 mm)",
    "font_pt": {"body": FS_BODY, "minimum": FS_TICK},
    "layout_check": f"paper/figures/_layout_check.py; {len(problems)} problems at build time",
    "environment": f"matplotlib {matplotlib.__version__}",
}, indent=1, ensure_ascii=False))
print("fig6c written; within", [round(v, 4) for v in _w],
      "transfer", [round(v, 4) for v in _t])
