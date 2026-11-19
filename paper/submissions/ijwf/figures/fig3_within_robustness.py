#!/usr/bin/env python3
"""Figure 3 - within-region thermal gain by block size (2026-10-23 redraw).

IJWF copy (2026-11-11) of paper/figures/fig3_within_robustness.py, which is left as it is. The data
and the asserts are those of the shared script and are read from the shared paths. Changed for the
publisher's figure guide: 8 pt and 7 pt text and 0.8 pt axis lines (_style_ijwf.py), part labels
(a) to (e) before the region names, and sentence case in the axis label and the two direct labels.
Writes fig3_within_robustness.pdf, .svg, _preview.png and fig3_provenance.json next to this file.

One small panel per region. Each panel shows the spatially blocked ROC-AUC of the baseline set
(grey, open markers) and the thermal set (blue, filled) at blocks of 2, 10 and 20 cells
(about 1, 5 and 10 km); the light band between them is the thermal gain. The intervals of the
gain are in Table 2 and are not repeated here.

The earlier three-panel version (dumbbells with a numeric column, a thermal-AUC panel and a
dodged delta panel with five colours) is in the git history before 2026-10-23.

Data: paper/figures/data/fig_data_corrected.json (corrected Manavgat label; extracted by
extract_fig_data.mjs from the official overlay rerun_labelfix/_round5/ov_official).
Asserts: every cell of 04_results Table 2 (45 values plus 15 intervals, to the printed 3 dp).
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.dont_write_bytecode = True                    # nothing is written into paper/figures, not even bytecode
HERE = Path(__file__).resolve().parent            # paper/submissions/ijwf/figures: every output goes here
SHARED = HERE.parents[2] / "figures"              # paper/figures: read only
sys.path[:0] = [str(HERE), str(SHARED)]
from _layout_check import check as layout_check, assert_inside   # noqa: E402
import _style_ijwf as S                                          # noqa: E402

DATA_PATH = SHARED / "data" / "fig_data_corrected.json"
DATA = json.loads(DATA_PATH.read_text())
fig34 = DATA["fig34"]

REGIONS = ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended", "montiferru_2021"]
LABEL = {"manavgat_2021": "Manavgat", "bejis_2022": "Bejís", "mugla_2021": "Muğla",
         "evia_2021_extended": "North Evia", "montiferru_2021": "Montiferru"}
BLOCKS = ["2", "10", "20"]
KM = {"2": "1", "10": "5", "20": "10"}

# ---- asserts vs 04_results Table 2: baseline, thermal, delta, CI low, CI high ----
TABLE1 = {
    "manavgat_2021": {"2": (0.841, 0.908, 0.067, 0.060, 0.073), "10": (0.820, 0.882, 0.062, 0.040, 0.082),
                      "20": (0.798, 0.845, 0.047, 0.016, 0.081)},
    "bejis_2022": {"2": (0.862, 0.918, 0.056, 0.048, 0.065), "10": (0.779, 0.824, 0.045, 0.018, 0.069),
                   "20": (0.739, 0.795, 0.057, 0.031, 0.090)},
    "mugla_2021": {"2": (0.743, 0.859, 0.116, 0.106, 0.125), "10": (0.698, 0.777, 0.079, 0.050, 0.105),
                   "20": (0.673, 0.733, 0.061, 0.030, 0.094)},
    "evia_2021_extended": {"2": (0.759, 0.912, 0.153, 0.142, 0.166), "10": (0.716, 0.864, 0.148, 0.119, 0.182),
                           "20": (0.679, 0.833, 0.154, 0.124, 0.189)},
    "montiferru_2021": {"2": (0.781, 0.883, 0.101, 0.080, 0.125), "10": (0.620, 0.720, 0.099, 0.017, 0.186),
                        "20": (0.555, 0.681, 0.126, 0.053, 0.228)},
}
for reg, rows in TABLE1.items():
    for b, want in rows.items():
        v = fig34[reg][b]
        got = (v["baseline"], v["thermal"], v["delta"], v["delta_ci"][0], v["delta_ci"][1])
        for i, (g, w) in enumerate(zip(got, want)):
            assert round(g, 3) == w, f"Table 2 mismatch {reg} block {b} col {i}: {g:.5f} vs {w}"
for reg in REGIONS:
    for b in BLOCKS:
        lo, hi = fig34[reg][b]["delta_ci"]
        assert lo > 0, f"delta CI must exclude zero: {reg} block {b}"

# ---------------- figure ------------------------------------------------------------------
S.apply()
fig, axes = plt.subplots(1, len(REGIONS), figsize=(S.WIDTH_MM * S.MM, 62 * S.MM), sharey=True)
x = list(range(len(BLOCKS)))
data_artists = []
for ax, reg, part in zip(axes, REGIONS, "abcde"):
    base = [fig34[reg][b]["baseline"] for b in BLOCKS]
    therm = [fig34[reg][b]["thermal"] for b in BLOCKS]
    ax.fill_between(x, base, therm, color=S.BLUE, alpha=0.12, lw=0, zorder=1)
    lb, = ax.plot(x, base, color=S.GREY, lw=1.2, marker="o", ms=4.0, mfc="white", mec=S.GREY,
                  mew=1.0, zorder=2)
    lt, = ax.plot(x, therm, color=S.BLUE, lw=1.5, marker="o", ms=4.0, zorder=3)
    data_artists += [(lb, f"baseline:{LABEL[reg]}"), (lt, f"thermal:{LABEL[reg]}")]
    ax.set_title(f"({part}) {LABEL[reg]}", loc="left")   # part label at the top left of each panel
    ax.set_xticks(x, [KM[b] for b in BLOCKS])
    ax.set_xlim(-0.3, len(BLOCKS) - 0.7)
    assert_inside(ax, f"Fig. 3 {LABEL[reg]}", ys=base + therm)

axes[0].set_ylim(0.50, 0.975)
axes[0].set_yticks([0.5, 0.6, 0.7, 0.8, 0.9])
axes[0].set_ylabel("ROC-AUC")
for ax in axes[1:]:
    ax.tick_params(axis="y", left=False)
    ax.spines["left"].set_visible(False)

# direct labels in the first panel, centred on the 5 km column
# (the collision checker takes a line's whole bounding box, so the labels clear each line's range)
top = max(fig34["manavgat_2021"][b]["thermal"] for b in BLOCKS)
bottom = min(fig34["manavgat_2021"][b]["baseline"] for b in BLOCKS)
axes[0].text(1, top + 0.02, "Thermal", color=S.BLUE, fontsize=S.FS_SMALL, ha="center", va="bottom")
axes[0].text(1, bottom - 0.02, "Baseline", color=S.MUTED, fontsize=S.FS_SMALL, ha="center", va="top")

fig.supxlabel("Block size (km)", fontsize=S.FS_BODY, y=0.02)
fig.subplots_adjust(left=0.085, right=0.99, top=0.88, bottom=0.2, wspace=0.12)

problems = layout_check(fig, "Fig. 3 - within-region gain by block size",
                        min_gap_pt=2.0, min_font_pt=S.FS_SMALL, data_artists=data_artists)
sizes = S.font_sizes(fig)
S.save(fig, HERE, "fig3_within_robustness")

(HERE / "fig3_provenance.json").write_text(json.dumps({
    "figure": "Figure 3 - within-region thermal gain by block size, IJWF package",
    "script": "paper/submissions/ijwf/figures/fig3_within_robustness.py",
    "source": "copy of paper/figures/fig3_within_robustness.py with the same data and asserts",
    "ijwf_changes": "8 pt and 7 pt text, 0.8 pt axis lines; part labels (a) to (e) before the region names; "
                    "sentence case: Block size (km), Thermal, Baseline",
    "data": {"path": "paper/figures/data/fig_data_corrected.json",
             "sha256": __import__("hashlib").sha256(DATA_PATH.read_bytes()).hexdigest(),
             "note": "step8c + robustness outputs of the corrected-label overlay; per-source sha256 inside"},
    "asserts": "all 75 printed values of 04 Table 2 equal the source rounded to 3 dp, zero tolerance; "
               "every delta CI lower bound > 0 (15 region-block cells); every plotted value inside its axis view",
    "design": "2026-10-23 redraw: small multiples, baseline grey/open, thermal blue/filled, gain as a light band; "
              "intervals left to Table 2",
    "canvas_mm": [S.WIDTH_MM, 62],
    "font_pt": {"body": S.FS_BODY, "minimum": S.FS_SMALL, "used": sizes},
    "layout_check": f"paper/figures/_layout_check.py; {len(problems)} problems at build time",
    "environment": f"matplotlib {matplotlib.__version__}",
}, indent=1, ensure_ascii=False), encoding="utf-8")
print("fig3 written; all 15 delta CIs exclude zero")
