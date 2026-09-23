#!/usr/bin/env python3
"""Figure 7 - removing direction-reversing features costs within-region skill; the transfer
change is near zero.

Mean within-region AUC (5 regions) against mean transfer AUC (20 directions) for
four feature configurations. Along the connecting path the within-region mean falls and
the transfer mean rises at every step, but the transfer change from the full set to
removing both, +0.014, has a pair-t interval over the ten region pairs of
[-0.028, +0.056], which spans zero. So the figure shows a measured local cost and no
measurable transfer gain, not an exchange.

2026-09-23 revision (corrected Manavgat label): the four means are 0.896/0.883/0.840/0.820
(within) and 0.527/0.529/0.533/0.541 (transfer), asserted against Appendix A(n) at zero
tolerance; the pair-t interval is computed here (it had no persisted producer) and
asserted against the printed text; the same computation reproduces the frozen
[-0.017, +0.045]. The title and the in-figure note no longer say "zero-sum" or "transfer
gained". The transfer-change interval is drawn as a whisker at the "- both" point about the
full-set level (dotted, no change), with the y axis opened to 0.49-0.59 so it shows whole.

Each configuration has its own marker and is named in a fixed legend, so no
label position depends on a data value (the labels previously sat next to their
points and crowded them). Split out of the former three-panel conservation figure.

Data: paper/figures/data/fig_data_corrected.json and paper/labelfix_rerun/round3/
feature_drop_transfer.json (per-direction deltas). Asserts here and in _conservation_common.py.
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
from scipy import stats

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _layout_check import check as layout_check, assert_inside
from _conservation_common import (HERE, MM, BLUE, FS_BODY, FS_TICK, fdrop,
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


# ---- the transfer change and its interval: pair-t over the ten unordered region pairs ----
def pair_t(path):
    f = json.loads(Path(path).read_text(encoding="utf-8"))
    d = {x["direction"]: x["delta_vs_full"]["drop_both"] for x in f["transfers"]}
    pairs = {}
    for k, v in d.items():
        pairs.setdefault(tuple(sorted(k.split("_to_"))), []).append(v)
    m = np.array([np.mean(v) for v in pairs.values()])
    h = stats.t.ppf(0.975, len(m) - 1) * m.std(ddof=1) / np.sqrt(len(m))
    assert len(d) == 20 and len(m) == 10
    return float(np.mean(list(d.values()))), float(m.mean() - h), float(m.mean() + h)


FDROP_SRC = HERE.parent / "labelfix_rerun" / "round3" / "feature_drop_transfer.json"
DELTA, DLO, DHI = pair_t(FDROP_SRC)
_frozen = pair_t(HERE.parent / "feature_drop_transfer.json")
assert tuple(f"{v:+.3f}" for v in _frozen) == ("+0.014", "-0.017", "+0.045"), _frozen  # frozen text
PRINTED = f"+{DELTA:.3f} [{DLO:.3f}, +{DHI:.3f}]".replace("-", "\u2212")
assert PRINTED == "+0.014 [\u22120.028, +0.056]", PRINTED
_r04 = " ".join((HERE.parent / "04_results.md").read_text(encoding="utf-8").split())
_d05 = " ".join((HERE.parent / "05_discussion.md").read_text(encoding="utf-8").split())
assert PRINTED in _r04 and PRINTED in _d05, "04 / 05 must print the same interval"
assert DLO < 0 < DHI, "the caption says the transfer change spans zero"
assert abs(DELTA - (fdrop["drop_both"]["mean_transfer"] - fdrop["full"]["mean_transfer"])) < 1e-6

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
ax.set_title("Feature removal costs within-region skill; the transfer change is near zero",
             fontsize=FS_BODY, loc="left")
# The transfer change of "- both" drawn with its interval, so that the reader sees it span
# zero before reading any caption: a whisker at the "- both" within value, running from the
# full-set transfer level plus the lower bound to plus the upper bound, and a dotted line at
# the full-set level marking "no change". The y axis is opened to show the whole interval;
# the points compress, which is the message (the transfer change is not measurable).
FULL_T = fdrop["full"]["mean_transfer"]
X_BOTH = fdrop["drop_both"]["mean_within"]
Y_LO, Y_HI = FULL_T + DLO, FULL_T + DHI
assert Y_LO < FULL_T < Y_HI, "the interval must contain the no-change level"
ref, = ax.plot([0.795, 0.900], [FULL_T, FULL_T], color="#777777", lw=0.9, ls=(0, (1.5, 1.5)),
               zorder=0)
wk, = ax.plot([X_BOTH, X_BOTH], [Y_LO, Y_HI], color=BLUE, lw=1.3, zorder=2)
for yy in (Y_LO, Y_HI):
    ax.plot([X_BOTH - 0.0022, X_BOTH + 0.0022], [yy, yy], color=BLUE, lw=1.3, zorder=2)
data_artists += [(ref, "no-change level"), (wk, "transfer-change CI")]
handles += [plt.Line2D([], [], color=BLUE, lw=1.3, marker="_", ms=7,
                       label="− both: 95% CI of the\ntransfer change"),
            plt.Line2D([], [], color="#777777", lw=0.9, ls=(0, (1.5, 1.5)),
                       label="no change (full set)")]

ax.set_xlim(0.795, 0.900)
ax.set_ylim(0.49, 0.59)
ax.set_xticks([0.80, 0.82, 0.84, 0.86, 0.88, 0.90])
ax.set_yticks([0.50, 0.52, 0.54, 0.56, 0.58])
style_axes(ax)
assert_inside(ax, "Fig. 7", xs=_w + [X_BOTH], ys=_t + [Y_LO, Y_HI])

fig.legend(handles=handles, fontsize=FS_TICK, frameon=False, loc="center left",
           bbox_to_anchor=(0.675, 0.55), handlelength=1.4, labelspacing=1.1,
           handletextpad=0.7, title="feature configuration",
           title_fontsize=FS_TICK)
fig.text(0.675, 0.30,
         "left along the path =\nwithin-region skill lost;\ntransfer change near zero,\n"
         + f"+{DELTA:.3f} [{DLO:.3f}, +{DHI:.3f}]".replace("-", "\u2212"),
         fontsize=FS_TICK, va="top", ha="left", color="#444444", linespacing=1.6)

problems = layout_check(fig, "Fig. 7 - feature-removal trade-off", min_gap_pt=2.0,
                        min_font_pt=8.0, data_artists=data_artists)
save(fig, "fig7_feature_drop", "--preview" in sys.argv)

(HERE / "fig7_provenance.json").write_text(json.dumps({
    "figure": "Fig. 7 - feature removal costs within-region skill; the transfer change is near zero",
    "script": "paper/figures/fig7_feature_drop.py",
    "data": {"path": "paper/figures/data/fig_data_corrected.json",
             "sha256": hashlib.sha256((HERE / "data" / "fig_data_corrected.json").read_bytes()).hexdigest(),
             "deltas": "paper/labelfix_rerun/round3/feature_drop_transfer.json",
             "deltas_sha256": hashlib.sha256(FDROP_SRC.read_bytes()).hexdigest()},
    "asserts": "the four means 0.896/0.883/0.840/0.820 (within) and 0.527/0.529/0.533/0.541 "
               "(transfer) equal Appendix A(n) at 3 dp (_conservation_common.py); within strictly "
               "decreasing and transfer strictly increasing along full -> -anomaly -> -elevation -> "
               "-both; transfer change +0.014, pair-t over ten region pairs [-0.028, +0.056], found "
               "verbatim in 04 and 05 and spanning zero; the same computation reproduces the frozen "
               "[-0.017, +0.045]; every value inside the axes",
    "transfer_change": {"delta": round(DELTA, 4), "pair_t_95": [round(DLO, 4), round(DHI, 4)],
                        "unit": "ten unordered region pairs, direction deltas averaged within a pair"},
    "labels": "one marker per configuration named in a fixed legend column to the right; "
              "no label position depends on a data value",
    "canvas_mm": [190, 92],
    "column": "double (190 mm)",
    "font_pt": {"body": FS_BODY, "minimum": FS_TICK},
    "layout_check": f"paper/figures/_layout_check.py; {len(problems)} problems at build time",
    "environment": f"matplotlib {matplotlib.__version__}",
}, indent=1, ensure_ascii=False))
print("fig7 written; within", [round(v, 4) for v in _w],
      "transfer", [round(v, 4) for v in _t])
