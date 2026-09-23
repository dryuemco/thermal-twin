#!/usr/bin/env python3
"""Figure 6 - pooled multi-region training beats the best single source only for Evia.

Leave-one-region-out: for each held-out target, the pooled model (orange circle, with its
95% CI) against the best pairwise source (open blue diamond), with the within-region
ceiling as a grey tick.

2026-09-23 revision (corrected Manavgat label): the pooled point lies LEFT of the pairwise
point for four targets and RIGHT of it for Evia, 0.715 [0.668, 0.757] against 0.654, whose
interval excludes the pairwise value; Manavgat's pooled interval lies entirely below chance
(0.426 [0.369, 0.486]). The pooled 95% interval is now drawn, because both statements rest
on it. Every printed number is asserted against Appendix A(n)(a) and the caption.

Split out of the former three-panel conservation figure so the panel gets the full column
width; at ~34 mm it needed a two-line title and its legend overflowed the axes.

Data: paper/figures/data/fig_data_corrected.json. Asserts here and in _conservation_common.py.
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _layout_check import check as layout_check, assert_inside
from _conservation_common import (HERE, MM, BLUE, ORANGE, GREY, FS_BODY, FS_TICK,
                          LABEL, loro, style_axes, chance_segment, save)

# ---- asserts vs Appendix A(n)(a) and the Fig. 6 caption, zero tolerance -------
BY = {r["target"]: r for r in loro}
_supp = (HERE.parent / "supplementary_appendices.md").read_text(encoding="utf-8")
_an = " ".join(_supp[_supp.index("**(a) Pooled multi-region training**"):
                     _supp.index("**(b) Removing the direction-reversing features.**")].split())
_cap = " ".join((HERE.parent / "figure_captions.tex").read_text(encoding="utf-8").split())
_ev, _mv, _bj = BY["evia_2021_extended"], BY["manavgat_2021"], BY["bejis_2022"]
fmt_ci = lambda r: f"{r['loro_raw']:.3f} [{r['loro_raw_ci'][0]:.3f}, {r['loro_raw_ci'][1]:.3f}]"
assert f"{fmt_ci(_ev)} against {_ev['best_pairwise']:.3f}" in _an, fmt_ci(_ev)
assert f"{fmt_ci(_ev)} against {_ev['best_pairwise']:.3f}" in _cap
assert fmt_ci(_mv) in _an, fmt_ci(_mv)
WINS = [t for t, r in BY.items() if r["loro_raw"] > r["best_pairwise"]]
assert WINS == ["evia_2021_extended"] and _ev["loro_raw_ci"][0] > _ev["best_pairwise"], WINS
assert _mv["loro_raw_ci"][1] < 0.5, "Manavgat pooled interval must lie entirely below chance"
BELOW_CI = [t for t, r in BY.items() if r["loro_raw_ci"][1] < 0.5]
assert BELOW_CI == ["manavgat_2021"], BELOW_CI       # caption: only Manavgat's interval
SHORT = sorted(r["best_pairwise"] - r["loro_raw"] for t, r in BY.items() if t not in WINS)
GAPS = sorted(r["within"] - r["loro_raw"] for r in loro)
assert f"shortfalls of {SHORT[0]:.2f} to {SHORT[-1]:.2f}" in _an, SHORT
assert f"{GAPS[0]:.2f} to {GAPS[-1]:.2f} AUC below the within-region ceiling" in _an, GAPS
assert f"(Manavgat {_mv['loro_raw']:.3f}, Bej\\'is {_bj['loro_raw']:.3f})" in _cap
assert f"reaches {_mv['best_pairwise']:.3f} and {_bj['best_pairwise']:.3f}" in _cap

plt.rcParams.update({"svg.fonttype": "none", "pdf.fonttype": 42})
fig = plt.figure(figsize=(190 * MM, 78 * MM))
ax = fig.add_axes([0.135, 0.215, 0.850, 0.700])

data_artists = []
ys = list(range(len(loro)))[::-1]
for r, y in zip(loro, ys):
    ax.plot([r["loro_raw"], r["best_pairwise"]], [y, y], color="#BBBBBB", lw=1.2,
            zorder=1)
    mp, = ax.plot(r["best_pairwise"], y, marker="D", mfc="white", mec=BLUE,
                  ms=6.0, mew=1.3, zorder=3)
    # the interval sits just below the row so it never overlays the grey connector (in
    # greyscale the two would print as the same light grey)
    yc = y - 0.17
    ci, = ax.plot(r["loro_raw_ci"], [yc, yc], color=ORANGE, lw=1.1, zorder=2)
    for cap in r["loro_raw_ci"]:
        ax.plot([cap, cap], [yc - 0.07, yc + 0.07], color=ORANGE, lw=1.1, zorder=2)
    ml, = ax.plot(r["loro_raw"], y, marker="o", mfc=ORANGE, mec=ORANGE, ms=6.0,
                  zorder=3)
    data_artists.append((ci, f"loro-ci:{r['target']}"))
    tb, = ax.plot([r["within"], r["within"]], [y - 0.24, y + 0.24], color=GREY,
                  lw=2.0, zorder=2)
    data_artists += [(mp, f"pairwise:{r['target']}"), (ml, f"loro:{r['target']}"),
                     (tb, f"within:{r['target']}")]

N = len(loro)
data_artists.append((chance_segment(ax, -0.55, N - 0.45), "chance"))

ax.set_yticks(ys, [LABEL[r["target"]] for r in loro], fontsize=FS_BODY)
ax.set_xlim(0.35, 0.99)
ax.set_ylim(-1.85, N - 0.4)
ax.set_xticks([0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
ax.set_xlabel("thermal ROC-AUC on the held-out target", fontsize=FS_BODY)
ax.set_title("Pooling every other region beats the best single source only for Evia",
             fontsize=FS_BODY, loc="left")
style_axes(ax)
assert_inside(ax, "Fig. 6", xs=[v for r in loro for v in (r["loro_raw"], *r["loro_raw_ci"], r["best_pairwise"], r["within"])])

hL = plt.Line2D([], [], marker="o", color=ORANGE, ls="", ms=6.0)
hP = plt.Line2D([], [], marker="D", mfc="white", mec=BLUE, ls="", ms=6.0, mew=1.3)
hW = plt.Line2D([], [], color=GREY, lw=0, marker="|", ms=10, mew=2.0)
hC = plt.Line2D([], [], color="black", lw=0.9, ls=(0, (4, 2)))
ax.legend([hL, hP, hW, hC],
          ["LORO pooled (95% CI)", "best pairwise source", "within-region ceiling",
           "chance (0.5)"],
          fontsize=FS_TICK, frameon=False, loc="lower left",
          bbox_to_anchor=(0.0, 0.0), ncol=4, handlelength=1.6,
          columnspacing=1.8, handletextpad=0.6, borderpad=0.0)

problems = layout_check(fig, "Fig. 6 - LORO pooling", min_gap_pt=2.0,
                        min_font_pt=8.0, data_artists=data_artists)
save(fig, "fig6_loro", "--preview" in sys.argv)

(HERE / "fig6_provenance.json").write_text(json.dumps({
    "figure": "Fig. 6 - pooled (LORO) training beats the best single source only for Evia",
    "script": "paper/figures/fig6_loro.py",
    "data": {"path": "paper/figures/data/fig_data_corrected.json",
             "sha256": __import__("hashlib").sha256(
                 (HERE / "data" / "fig_data_corrected.json").read_bytes()).hexdigest(),
             "note": "loro_pooled_transfer.json from paper/labelfix_rerun/round3 (corrected label); "
                     "sha256 inside"},
    "asserts": "pooled beats the best pairwise source only for Evia, 0.715 [0.668, 0.757] against "
               "0.654, interval excluding it; Manavgat pooled 0.426 [0.369, 0.486], the only interval "
               "entirely below chance; shortfalls 0.09-0.25 and ceiling gaps 0.20-0.48; every "
               "number found verbatim in Appendix A(n)(a) or the caption; every value inside the "
               "x axis (and _conservation_common.py)",
    "legend": "in a reserved band below the plotted rows; chance drawn as a segment over the "
              "data rows only",
    "canvas_mm": [190, 78],
    "column": "double (190 mm)",
    "font_pt": {"body": FS_BODY, "minimum": FS_TICK},
    "layout_check": f"paper/figures/_layout_check.py; {len(problems)} problems at build time; "
                    f"{len(data_artists)} data artists registered",
    "environment": f"matplotlib {matplotlib.__version__}",
}, indent=1, ensure_ascii=False), encoding="utf-8")
print("fig6 written; pooled beats best pairwise only for", WINS, "; interval below chance:", BELOW_CI)
