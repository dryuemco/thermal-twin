#!/usr/bin/env python3
"""Figure 6 - pooled training beats the mean single source only for Evia (2026-10-23 redraw).

Leave-one-region-out: for each held-out target, the mean of the four single-source models
(open grey circle) and the model trained on the other four regions together (filled blue dot
with its 95% spatial-block interval). The best single source, which needs target labels to
choose, and the within-region ceiling are no longer drawn; both are in Section S4.4.
The earlier version is in the git history before 2026-10-23.

Data: paper/figures/data/fig_data_corrected.json and round7/r7d_pooled_vs_single.csv.
Asserts here and in _conservation_common.py.
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _layout_check import check as layout_check, assert_inside
from _conservation_common import HERE, LABEL, loro
import _style as S

# ---- asserts vs Section S4.4, the Fig. 6 caption and round7, zero tolerance ----------
# 2026-09-29 (internal review F61): the benchmark is the MEAN of the four single-source models;
# the best single source is kept as an oracle marker, since choosing it uses target labels.
import csv
BY = {r["target"]: r for r in loro}
_R7D = HERE.parent / "labelfix_rerun" / "round7" / "r7d_pooled_vs_single.csv"
MEAN = {row["target"]: float(row["mean_single"]) for row in csv.DictReader(open(_R7D, encoding="utf-8"))}
for _t, _r in BY.items():   # the pooled and best-single values of the two sources agree
    _row = next(x for x in csv.DictReader(open(_R7D, encoding="utf-8")) if x["target"] == _t)
    assert abs(float(_row["pooled"]) - _r["loro_raw"]) < 1e-9, _t
    assert abs(float(_row["best_single_oracle"]) - _r["best_pairwise"]) < 1e-6, _t
_supp = (HERE.parent / "supplementary.md").read_text(encoding="utf-8")
_an = " ".join(_supp[_supp.index("## S4.4 "):
                     _supp.index("## S4.5 ")].split())
_cap = " ".join((HERE.parent / "figure_captions.tex").read_text(encoding="utf-8").split())
_ev, _mv, _bj = BY["evia_2021_extended"], BY["manavgat_2021"], BY["bejis_2022"]
fmt_ci = lambda r: f"{r['loro_raw']:.3f} [{r['loro_raw_ci'][0]:.3f}, {r['loro_raw_ci'][1]:.3f}]"
_evm = MEAN["evia_2021_extended"]
assert f"{fmt_ci(_ev)} against a mean of {_evm:.3f}" in _an, fmt_ci(_ev)
assert f"{fmt_ci(_ev)} against {_evm:.3f}" in _cap
assert f"best single source only for Evia ({_ev['best_pairwise']:.3f})" in _an
assert fmt_ci(_mv) in _an, fmt_ci(_mv)
WINS = [t for t, r in BY.items() if r["loro_raw"] > MEAN[t]]
assert WINS == ["evia_2021_extended"], WINS
assert [t for t, r in BY.items() if r["loro_raw"] > r["best_pairwise"]] == ["evia_2021_extended"]
assert _mv["loro_raw_ci"][1] < 0.5, "Manavgat pooled interval must lie entirely below chance"
BELOW_CI = [t for t, r in BY.items() if r["loro_raw_ci"][1] < 0.5]
assert BELOW_CI == ["manavgat_2021"], BELOW_CI       # caption: only Manavgat's interval
SHORT = sorted(MEAN[t] - r["loro_raw"] for t, r in BY.items() if t not in WINS)
GAPS = sorted(r["within"] - r["loro_raw"] for r in loro)
assert f"by {SHORT[0]:.3f} to {SHORT[-1]:.3f}" in _an, SHORT
assert f"{GAPS[0]:.2f} to {GAPS[-1]:.2f} AUC below the within-region ceiling" in _an, GAPS
assert f"(0.426 and 0.458)" in _cap and f"{_mv['loro_raw']:.3f}" == "0.426" and f"{_bj['loro_raw']:.3f}" == "0.458"

S.apply()
fig, ax = plt.subplots(figsize=(S.WIDTH_MM * S.MM, 62 * S.MM))
S.chance(ax)
data_artists = []
ys = list(range(len(loro)))[::-1]
for r, y in zip(loro, ys):
    m = MEAN[r["target"]]
    ci, = ax.plot(r["loro_raw_ci"], [y, y], color=S.BLUE, lw=1.0, zorder=2)
    mm, = ax.plot(m, y, marker="o", ms=5.0, mfc="white", mec=S.GREY, mew=1.1, lw=0, zorder=3)
    mp, = ax.plot(r["loro_raw"], y, marker="o", ms=5.5, color=S.BLUE, lw=0, zorder=4)
    data_artists += [(mm, f"mean:{r['target']}"), (mp, f"pooled:{r['target']}"), (ci, f"ci:{r['target']}")]

ax.set_yticks(ys, [LABEL[r["target"]] if r["target"] != "evia_2021_extended" else "North Evia" for r in loro])
ax.tick_params(axis="y", length=0)
ax.spines["left"].set_visible(False)
ax.set_ylim(-0.6, len(loro) - 0.4)
ax.set_xlim(0.35, 0.80)
ax.set_xticks([0.4, 0.5, 0.6, 0.7, 0.8])
ax.set_xlabel("ROC-AUC in the held-out target region")
assert_inside(ax, "Fig. 6", xs=[v for r in loro for v in (r["loro_raw"], *r["loro_raw_ci"], MEAN[r["target"]])])

handles = [plt.Line2D([], [], marker="o", ms=5.0, mfc="white", mec=S.GREY, mew=1.1, lw=0),
           plt.Line2D([], [], marker="o", ms=5.5, color=S.BLUE, lw=1.0)]
ax.legend(handles, ["mean of the four single-source models", "pooled model, 95% interval"],
          loc="upper right", bbox_to_anchor=(1.0, 1.02), handletextpad=0.4, labelspacing=0.3)
fig.subplots_adjust(left=0.13, right=0.98, top=0.97, bottom=0.18)

problems = layout_check(fig, "Fig. 6 - pooled training", min_gap_pt=2.0, min_font_pt=8.0,
                        data_artists=data_artists)
S.save(fig, HERE, "fig6_loro")

(HERE / "fig6_provenance.json").write_text(json.dumps({
    "figure": "Fig. 6 - pooled training beats the mean single source only for Evia",
    "script": "paper/figures/fig6_loro.py",
    "data": {"path": "paper/figures/data/fig_data_corrected.json",
             "sha256": __import__("hashlib").sha256(
                 (HERE / "data" / "fig_data_corrected.json").read_bytes()).hexdigest(),
             "note": "loro_pooled_transfer.json from paper/labelfix_rerun/round3 (corrected label); "
                     "mean single source from round7/r7d_pooled_vs_single.csv"},
    "asserts": "pooled beats the mean single source only for Evia, 0.715 [0.668, 0.757] against 0.569, "
               "and the oracle best source (0.654) likewise; Manavgat pooled 0.426 [0.369, 0.486], the "
               "only interval entirely below chance; shortfalls and ceiling gaps as printed in Section "
               "S4.4; caption numbers found verbatim; every value inside the x axis",
    "design": "2026-10-23 redraw: mean single source (open grey) to pooled (filled blue, with interval); "
              "oracle source and within-region ceiling left to Section S4.4",
    "canvas_mm": [S.WIDTH_MM, 62],
    "font_pt": {"body": S.FS_BODY, "minimum": S.FS_SMALL},
    "layout_check": f"paper/figures/_layout_check.py; {len(problems)} problems at build time",
    "environment": f"matplotlib {matplotlib.__version__}",
}, indent=1, ensure_ascii=False), encoding="utf-8")
print("fig6 written; pooled beats the mean single source only for", WINS, "; interval below chance:", BELOW_CI)
