#!/usr/bin/env python3
"""Figure 7 - removing the reversing features costs within-region skill and gives no
measurable transfer gain (2026-10-23 redraw).

Two dot plots that share their rows, one per feature set: (a) mean within-region ROC-AUC over
the five regions at 1 km blocking, (b) mean transfer ROC-AUC over the 20 directions. Both axes
span 0.12 AUC, so the two changes can be compared by eye. The whisker in (b) is the pair-t 95%
interval over the ten region pairs of the change from the full set to removing both, placed
about the full-set level; the thin vertical line marks that level. The earlier scatter-path
version with a side legend is in the git history before 2026-10-23.

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
from _conservation_common import HERE, fdrop
import _style as S

ROW = {"full": "all ten predictors", "drop_anom": "without LST anomaly",
       "drop_elev": "without elevation", "drop_both": "without both"}
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

FULL_T = fdrop["full"]["mean_transfer"]
FULL_W = fdrop["full"]["mean_within"]
Y_LO, Y_HI = FULL_T + DLO, FULL_T + DHI
assert Y_LO < FULL_T < Y_HI, "the interval must contain the no-change level"

S.apply()
fig, (axW, axT) = plt.subplots(1, 2, figsize=(S.WIDTH_MM * S.MM, 52 * S.MM), sharey=True)
ys = list(range(len(PATH)))[::-1]
data_artists = []
for ax, key, ref in ((axW, "mean_within", FULL_W), (axT, "mean_transfer", FULL_T)):
    ax.axvline(ref, color=S.RULE, lw=0.8, zorder=0)
    for c, y in zip(PATH, ys):
        pt, = ax.plot(fdrop[c][key], y, marker="o", ms=5.5, color=S.BLUE, lw=0, zorder=3)
        data_artists.append((pt, f"{key}:{c}"))
y_both = ys[PATH.index("drop_both")]
wk, = axT.plot([Y_LO, Y_HI], [y_both, y_both], color=S.BLUE, lw=1.0, zorder=2)
data_artists.append((wk, "transfer-change CI"))
# key for the whisker, above its right end (the journal wants keys in the graphic)
axT.text(Y_HI, y_both + 0.24, "95% interval\nof the change", fontsize=S.FS_SMALL, color=S.MUTED,
         ha="right", va="bottom", linespacing=1.1)

axW.set_xlim(0.79, 0.91); axW.set_xticks([0.80, 0.84, 0.88])
axT.set_xlim(0.48, 0.60); axT.set_xticks([0.48, 0.52, 0.56, 0.60])
axW.set_title("(a) Within regions")
axT.set_title("(b) Across regions")
for ax in (axW, axT):
    ax.set_xlabel("mean ROC-AUC")
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
axW.set_yticks(ys, [ROW[c] for c in PATH])
axW.set_ylim(-0.6, len(PATH) - 0.4)
assert_inside(axW, "Fig. 7a", xs=_w)
assert_inside(axT, "Fig. 7b", xs=_t + [Y_LO, Y_HI])
fig.subplots_adjust(left=0.2, right=0.98, top=0.86, bottom=0.24, wspace=0.12)

problems = layout_check(fig, "Fig. 7 - feature removal", min_gap_pt=2.0, min_font_pt=8.0,
                        data_artists=data_artists)
S.save(fig, HERE, "fig7_feature_drop")

(HERE / "fig7_provenance.json").write_text(json.dumps({
    "figure": "Fig. 7 - feature removal costs within-region skill and gives no measurable transfer gain",
    "script": "paper/figures/fig7_feature_drop.py",
    "data": {"path": "paper/figures/data/fig_data_corrected.json",
             "sha256": hashlib.sha256((HERE / "data" / "fig_data_corrected.json").read_bytes()).hexdigest(),
             "deltas": "paper/labelfix_rerun/round3/feature_drop_transfer.json",
             "deltas_sha256": hashlib.sha256(FDROP_SRC.read_bytes()).hexdigest()},
    "asserts": "the four means 0.896/0.883/0.840/0.820 (within) and 0.527/0.529/0.533/0.541 "
               "(transfer) equal Section S1.14 at 3 dp (_conservation_common.py); within strictly "
               "decreasing and transfer strictly increasing along the rows; transfer change +0.014, "
               "pair-t over ten region pairs [-0.028, +0.056], found verbatim in 04 and 05 and spanning "
               "zero; the same computation reproduces the frozen [-0.017, +0.045]; every value inside the axes",
    "transfer_change": {"delta": round(DELTA, 4), "pair_t_95": [round(DLO, 4), round(DHI, 4)],
                        "unit": "ten unordered region pairs, direction deltas averaged within a pair"},
    "design": "2026-10-23 redraw: two dot plots sharing rows, equal 0.12 AUC axis spans",
    "canvas_mm": [S.WIDTH_MM, 52],
    "font_pt": {"body": S.FS_BODY, "minimum": S.FS_SMALL},
    "layout_check": f"paper/figures/_layout_check.py; {len(problems)} problems at build time",
    "environment": f"matplotlib {matplotlib.__version__}",
}, indent=1, ensure_ascii=False), encoding="utf-8")
print("fig7 written; within", [round(v, 4) for v in _w], "transfer", [round(v, 4) for v in _t])
