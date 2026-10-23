#!/usr/bin/env python3
"""Figure 4 - raw cross-region transfer matrix (2026-10-23 redraw).

One 5x5 source-by-target heatmap of thermal transfer ROC-AUC, coloured on a diverging scale
centred on chance (vermillion below 0.5, blue above, near-white at 0.5), with the value printed
in every cell. A value printed in bold has a 10-cell (about 5 km) target-block interval that
excludes 0.5. The adapted results, formerly panels (b) and (c), are shown as Fig. 5. A key to
the right of the matrix gives the colour scale and the meaning of bold, because Fire Ecology wants
keys in the graphic and not in the legend; the canvas is the 170 mm full page width.

The earlier three-panel version (PuOr, hatching below chance, corner dots for interval support)
is in the git history before 2026-10-23.

Data: paper/figures/data/fig_data_corrected.json (corrected Manavgat label; sha256 per source
inside). Hard asserts tie all 60 values of Table S16 (supplementary.md) to the data at zero
tolerance (3 dp), the three ranges to 04 Section 3.5, and the below-chance count to Table 4.
"""
import json
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _layout_check import check as layout_check, best_text_colour
import _style as S

HERE = Path(__file__).resolve().parent
DATA_PATH = HERE / "data" / "fig_data_corrected.json"
DATA = json.loads(DATA_PATH.read_text())
fig5 = DATA["fig5"]

REGIONS = ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended", "montiferru_2021"]
NAME = {"manavgat_2021": "Manavgat", "bejis_2022": "Bejís", "mugla_2021": "Muğla",
        "evia_2021_extended": "North Evia", "montiferru_2021": "Montiferru"}
MIN_CONTRAST = 4.5   # WCAG AA for normal text

# ---- asserts: all 60 cells vs Table B9 as printed (zero tolerance at 3 dp) ----
B9_NAME = {"Manavgat": "manavgat_2021", "Bejís": "bejis_2022", "Muğla": "mugla_2021",
           "Evia": "evia_2021_extended", "Montiferru": "montiferru_2021"}
b9_md = (HERE.parent / "supplementary.md").read_text(encoding="utf-8")
b9_md = b9_md[b9_md.index("**Table S16."):]
b9_rows = re.findall(r"^\| (\w+)→(\w+) \| ([0-9.]+) \[[^]]*\] \| ([0-9.]+) \[[^]]*\] \| ([0-9.]+) \[[^]]*\] \|$",
                     b9_md, flags=re.M)
assert len(b9_rows) == 20, f"Table B9 rows parsed: {len(b9_rows)}"
n_checked = 0
for s, tg, raw_s, z_s, c_s in b9_rows:
    d = f"{B9_NAME[s]}_to_{B9_NAME[tg]}"
    for key, printed in (("raw", raw_s), ("zscore", z_s), ("coral", c_s)):
        assert f"{fig5[d][key]:.3f}" == printed, f"Table B9 {d} {key}: {fig5[d][key]:.4f} vs {printed}"
        n_checked += 1
assert n_checked == 60 and len(fig5) == 20
vals = {k: [fig5[d][k] for d in fig5] for k in ("raw", "zscore", "coral")}
rng = {k: (min(v), max(v)) for k, v in vals.items()}
# 04 Section 4.5: raw 0.314 to 0.677; z-score 0.302 to 0.630; CORAL 0.406 to 0.624
assert tuple(f"{x:.3f}" for x in rng["raw"]) == ("0.314", "0.677"), rng["raw"]
assert tuple(f"{x:.3f}" for x in rng["zscore"]) == ("0.302", "0.630"), rng["zscore"]
assert tuple(f"{x:.3f}" for x in rng["coral"]) == ("0.406", "0.624"), rng["coral"]
# Table 4 / 4.5: seven of twenty raw directions below chance at the point estimate
BELOW = {k: sorted(d for d in fig5 if fig5[d][k] < 0.5) for k in ("raw", "zscore", "coral")}
assert len(BELOW["raw"]) == 7, BELOW["raw"]

# 10-cell (~5 km) interval support of the raw directions: the value of a direction whose
# target-block interval excludes 0.5 is printed in bold (Table 4: 9 above, 6 below)
import pandas as _pd
_ci = _pd.read_csv(HERE.parent / "labelfix_rerun/round5/out_official/transfer_ci_blocksize.csv")
_nm = {"manavgat": "manavgat_2021", "bejis": "bejis_2022", "mugla": "mugla_2021",
       "evia": "evia_2021_extended", "montiferru": "montiferru_2021"}
SUPPORT10 = {}
for _, _r in _ci.iterrows():
    _s, _t = _r.direction.lower().replace("ğ", "g").split("_to_")
    if _r.verdict_10cell in ("above", "below"):
        SUPPORT10[f"{_nm[_s]}_to_{_nm[_t]}"] = _r.verdict_10cell
assert sum(v == "above" for v in SUPPORT10.values()) == 9 and sum(v == "below" for v in SUPPORT10.values()) == 6, SUPPORT10
for _d, _v in SUPPORT10.items():
    assert (fig5[_d]["raw"] > 0.5) == (_v == "above"), _d

S.apply()
# layout in mm: row labels | 88 mm square matrix | key
W_MM, H_MM = S.WIDTH_MM, 102.0
MX, MY, MS = 26.0, 3.0, 88.0                    # matrix left, bottom, side
KX = 124.0                                      # key column
fig = plt.figure(figsize=(W_MM * S.MM, H_MM * S.MM))
ax = fig.add_axes([MX / W_MM, MY / H_MM, MS / W_MM, MS / H_MM])
norm = TwoSlopeNorm(vmin=0.30, vcenter=0.5, vmax=0.70)
# every value must fall inside the colour norm, or it is painted with the clipped end colour
assert all(norm.vmin < v < norm.vmax for v in vals["raw"]), rng
cmap = LinearSegmentedColormap.from_list("below_above", [S.VERMILLION, "#F7F7F7", S.BLUE])

M = np.full((5, 5), np.nan)
for i, s in enumerate(REGIONS):
    for j, t in enumerate(REGIONS):
        if s != t:
            M[i, j] = fig5[f"{s}_to_{t}"]["raw"]
edges = np.arange(6) - 0.5
im = ax.pcolormesh(edges, edges, np.ma.masked_invalid(M), cmap=cmap, norm=norm,
                   edgecolors="white", linewidth=1.5)
ax.set_xlim(-0.5, 4.5); ax.set_ylim(4.5, -0.5); ax.set_aspect("equal")
contrast_log = []
for i in range(5):
    ax.add_patch(plt.Rectangle((i - 0.5, i - 0.5), 1, 1, facecolor="white", edgecolor="white",
                               linewidth=1.5, zorder=2))
    for j in range(5):
        if i == j:
            continue
        colour, ratio = best_text_colour(cmap(norm(M[i, j])))
        contrast_log.append((REGIONS[i], REGIONS[j], round(float(M[i, j]), 4), colour, round(ratio, 2)))
        bold = f"{REGIONS[i]}_to_{REGIONS[j]}" in SUPPORT10
        ax.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center", fontsize=S.FS_BODY, color=colour,
                fontweight="bold" if bold else "normal", zorder=3)

ax.set_xticks(range(5), [NAME[r] for r in REGIONS])
ax.set_yticks(range(5), [NAME[r] for r in REGIONS])
ax.xaxis.set_ticks_position("top"); ax.xaxis.set_label_position("top")
ax.set_xlabel("target region", labelpad=7)
ax.set_ylabel("source region", labelpad=4)
ax.tick_params(length=0)
for s in ax.spines.values():
    s.set_visible(False)

worst = min(contrast_log, key=lambda r: r[-1])
assert worst[-1] >= MIN_CONTRAST, f"cell label contrast {worst[-1]}:1 below {MIN_CONTRAST}:1 at {worst}"
print(f"[contrast] worst cell-label ratio {worst[-1]}:1 ({worst[0]}->{worst[1]} = {worst[2]})")

# key: colour scale, then the bold convention
cax = fig.add_axes([KX / W_MM, 50.0 / H_MM, 4.0 / W_MM, 38.0 / H_MM])
cbar = fig.colorbar(im, cax=cax, ticks=[0.3, 0.4, 0.5, 0.6, 0.7])
cbar.ax.set_yticklabels(["0.3", "0.4", "0.5, chance", "0.6", "0.7"])
cbar.ax.tick_params(length=2.0, width=0.6, labelsize=S.FS_SMALL)
cbar.outline.set_linewidth(0.6)
cbar.outline.set_edgecolor(S.MUTED)
fig.text(KX / W_MM, 91.0 / H_MM, "ROC-AUC", fontsize=S.FS_BODY, ha="left", va="bottom")
for y, sample, weight, meaning in ((40.0, "0.65", "bold", "interval excludes 0.5"),
                                   (34.0, "0.52", "normal", "interval includes 0.5")):
    fig.text(KX / W_MM, y / H_MM, sample, fontsize=S.FS_BODY, fontweight=weight, ha="left", va="center")
    fig.text((KX + 9.0) / W_MM, y / H_MM, meaning, fontsize=S.FS_SMALL, ha="left", va="center")

problems = layout_check(fig, "Fig. 4 - raw transfer matrix", min_gap_pt=2.0, min_font_pt=8.0)
S.save(fig, HERE, "fig4_transfer_matrix")

(HERE / "fig4_provenance.json").write_text(json.dumps({
    "figure": "Fig. 4 - raw cross-region transfer matrix",
    "script": "paper/figures/fig4_transfer_matrix.py",
    "data": {"path": "paper/figures/data/fig_data_corrected.json",
             "sha256": __import__("hashlib").sha256(DATA_PATH.read_bytes()).hexdigest(),
             "note": "step10_metrics.json of all 10 pairs, corrected-label overlay; per-source sha256 inside"},
    "asserts": "all 60 values of Table S16 equal the data at 3 dp, zero tolerance; ranges "
               "0.314-0.677 / 0.302-0.630 / 0.406-0.624 (04 3.5); 7 raw directions below chance and "
               "9 above / 6 below with interval support (Table 4); every value inside the colour norm "
               f"0.30-0.70; worst cell-label contrast >= {MIN_CONTRAST}:1",
    "below_chance": BELOW,
    "contrast": {"threshold": MIN_CONTRAST, "worst_ratio": worst[-1],
                 "worst_cell": f"{worst[0]}->{worst[1]} = {worst[2]}"},
    "design": "2026-10-23 redraw: raw panel only; vermillion-white-blue diverging scale centred on 0.5; "
              "values in every cell; bold = 10-cell interval excludes 0.5; empty diagonal; key with colour bar "
              "and the bold convention inside the graphic",
    "canvas_mm": [W_MM, H_MM],
    "font_pt": {"body": S.FS_BODY, "minimum": S.FS_SMALL},
    "layout_check": f"paper/figures/_layout_check.py; {len(problems)} problems at build time",
    "environment": f"matplotlib {matplotlib.__version__}",
}, indent=1, ensure_ascii=False), encoding="utf-8")
print("fig4 written; below chance", {k: len(v) for k, v in BELOW.items()})
