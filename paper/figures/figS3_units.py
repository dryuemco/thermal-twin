#!/usr/bin/env python3
"""Fig. S3 - the paired thermal contribution to transfer by resampling unit (Additional file 1).

Two panels share their rows: (a) the study areas as drawn, (b) the 10 km collar. Each row is one
resampling unit: the dot is the mean paired contribution over the twenty directions and the line
its 95% interval (20,000 replicates where resampled). The pair-cluster bootstrap, the primary unit
of the main text, is drawn in blue. This figure replaces former Tables S29 and S31 and the
crossed-random-effects row of former Table S35 (2026-10-23).

Data, under paper/labelfix_rerun/: round8/r8d_summary.json (as drawn, all bootstrap units and the
jackknife), inference/units.json (collar), code/transfer_delta_ci.json (pair-t intervals) and
round8/r8l_summary.json (crossed random effects).
"""
import hashlib
import json
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _layout_check import check as layout_check, assert_inside
import _style as S

LR = HERE.parent / "labelfix_rerun"
load = lambda p: json.loads((LR / p).read_text(encoding="utf-8"))
SOURCES = ["round8/r8d_summary.json", "inference/units.json", "code/transfer_delta_ci.json", "round8/r8l_summary.json"]
r8d, units, tdc, r8l = (load(p) for p in SOURCES)
A = r8d["tost_asdrawn_delta"]
C = units["Q2_equalised10_delta"]
MEAN = {"a": A["mean"], "b": C["mean"]}
assert abs(MEAN["a"] - tdc["results"]["as drawn"]["mean"]) < 1e-9
assert abs(MEAN["b"] - tdc["results"]["equalised 10 km"]["mean"]) < 1e-9
ROWS = [("Directions, naive bootstrap", "naive_directions_boot"),
        ("Region pairs, cluster bootstrap", "pair_cluster_boot"),
        ("Region pairs, Student t", "pair_t"),
        ("Target region, cluster bootstrap", "target_cluster_boot"),
        ("Source region, cluster bootstrap", "source_cluster_boot"),
        ("Source and target, pigeonhole", "pigeonhole_boot"),
        ("One region left out, jackknife t", "loro_jackknife_t4"),
        ("Crossed random effects, t", "crossed")]


def interval(frame, key):
    if key == "pair_t":
        return tdc["results"]["as drawn" if frame == "a" else "equalised 10 km"]["ci_pair_t"]
    if key == "crossed":
        return r8l["crossed_random_effects"]["full" if frame == "a" else "10km"]["ci95_t4"]
    return A["units"][key]["ci95"] if frame == "a" else C[key][:2]


CI = {f: {k: interval(f, k) for _, k in ROWS} for f in "ab"}
for f in "ab":
    for k, (lo, hi) in CI[f].items():
        assert not (math.isnan(lo) or math.isnan(hi)) and lo < MEAN[f] < hi, (f, k)
# the two two-way estimators are undefined (negative variance), as the caption says
assert all(math.isnan(v) for k in ("cgm_twoway_t4", "dyadic_robust_t4") for v in A["units"][k]["ci95"] + C[k][:2])
# Section S1.3: every interval includes zero as drawn; on the collar exactly the two region clusters exclude it
assert all(lo < 0 < hi for lo, hi in CI["a"].values())
excl = [k for k, (lo, hi) in CI["b"].items() if lo > 0]
assert excl == ["target_cluster_boot", "source_cluster_boot"], excl
fmt = lambda v: f"{v:+.3f}".replace("-", "−")
assert [fmt(v) for v in CI["b"]["target_cluster_boot"]] == ["+0.010", "+0.040"]
assert [fmt(v) for v in CI["b"]["pair_cluster_boot"]] == ["−0.003", "+0.051"]

S.apply()
fig, axes = plt.subplots(1, 2, figsize=(S.WIDTH_MM * S.MM, 62 * S.MM), sharey=True)
ys = list(range(len(ROWS)))[::-1]
arts, title = [], {"a": "(a) Study areas as drawn", "b": "(b) 10 km collar"}
for ax, f in zip(axes, "ab"):
    ax.axvline(0, color=S.RULE, lw=0.8, zorder=0)
    xs = []
    for (lab, k), y in zip(ROWS, ys):
        col = S.BLUE if k == "pair_cluster_boot" else S.GREY
        w, = ax.plot(CI[f][k], [y, y], color=col, lw=1.2, zorder=2)
        d, = ax.plot(MEAN[f], y, "o", ms=4.6, color=col, zorder=3)
        arts += [(w, f"{f}:{k}:ci"), (d, f"{f}:{k}")]
        xs += list(CI[f][k])
    ax.set_xlim(-0.06, 0.08)
    ax.set_xticks([-0.04, 0, 0.04, 0.08], ["−0.04", "0", "+0.04", "+0.08"])
    ax.set_title(title[f])
    ax.set_xlabel("thermal minus baseline ROC-AUC")
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    assert_inside(ax, f"Fig. S3{f}", xs=xs + [MEAN[f]])
axes[0].set_yticks(ys, [lab for lab, _ in ROWS])
axes[0].set_ylim(-0.6, len(ROWS) - 0.4)
fig.legend(handles=[Line2D([], [], color=S.BLUE, lw=1.2, marker="o", ms=4.6, label="primary unit of the main text"),
                    Line2D([], [], color=S.GREY, lw=1.2, marker="o", ms=4.6, label="other units")],
           loc="upper left", bbox_to_anchor=(0.005, 0.995), ncol=2, handletextpad=0.4, columnspacing=1.4)
fig.subplots_adjust(left=0.30, right=0.965, top=0.80, bottom=0.17, wspace=0.12)
problems = layout_check(fig, "Fig. S3 - resampling units", min_gap_pt=2.0, min_font_pt=8.0, data_artists=arts)
S.save(fig, HERE, "figS3_units")
fig.savefig(HERE / "figS3_units.png", dpi=300)
(HERE / "figS3_provenance.json").write_text(json.dumps({
    "figure": "Fig. S3 - the paired thermal contribution to transfer by resampling unit",
    "script": "paper/figures/figS3_units.py",
    "data": {p: hashlib.sha256((LR / p).read_bytes()).hexdigest() for p in SOURCES},
    "asserts": "means agree across sources; the two-way estimators are undefined; as drawn every interval "
               "includes zero; on the collar exactly the target- and source-region clusters exclude zero",
    "canvas_mm": [S.WIDTH_MM, 62],
    "layout_check": f"paper/figures/_layout_check.py; {len(problems)} problems at build time",
    "environment": f"matplotlib {matplotlib.__version__}",
}, indent=1, ensure_ascii=False), encoding="utf-8")
print("figS3 written")
TEXT = " ".join((HERE.parent / "supplementary.md").read_text(encoding="utf-8").split())
for s in ("Fig. S3", "[+0.010, +0.040]"):
    assert s in TEXT, f"Section S1.3 must state {s}"
