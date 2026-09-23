#!/usr/bin/env python3
"""Figure 1 - study-area location map (plain, Mediterranean basin).

Natural Earth 1:50m coastline + land, five study AOI rectangles (single colour -
no regime implication among study regions), region + year labels, approximate
scale bar. No topography, no satellite background; country borders omitted (kept
plain per design decision).

Kozan 2023 IS drawn, in a deliberately different style (grey, dashed edge, open
square marker, role stated in the label) and separated in the legend, because it
is discussed in Methods 3.3 and Results 4.1 and a reader who meets it there will
look for its location. The style difference carries the point that it is a gate
negative control and entered no model, transfer or diagnostic.

AOI bounds: paper/figures/data/fig1_aoi.json (step0 geojson / grid-derived,
sha256 per source inside; asserted here against 03_methods Table 1).
Okabe-Ito, greyscale-safe, vector.

2026-08-08 typography/space revision: double-column 190 mm, body 9 pt, minimum
8 pt; extent widened east so the Manavgat label is no longer clipped by the
frame; label anchors moved off the coastline; very light land fill and a white
text halo so no label competes with a coast line. Layout verified by
_layout_check.py (no overlaps, no clipping, no text below 8 pt).
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _layout_check import check as layout_check

HERE = Path(__file__).resolve().parent
AOI = json.loads((HERE / "data" / "fig1_aoi.json").read_text())["aoi"]

BLUE = "#0072B2"  # single colour for every STUDY AOI - no regime grouping implied
GREY = "#767676"  # gate control only - visually separated from the study set
LAND = "#F4F4F2"  # very light neutral fill: gives labels a surface to sit on
COAST = "#7A7A7A"

FS_BODY = 9.0     # region labels
FS_SMALL = 8.0    # graticule labels, scale bar, legend  (minimum in this figure)

CONTROL = "kozan_2023"

LABEL = {
    "manavgat_2021": "Manavgat 2021", "bejis_2022": "Bejís 2022",
    "mugla_2021": "Muğla 2021", "evia_2021_extended": "Evia 2021",
    "montiferru_2021": "Montiferru 2021",
    # two lines: the single-line form is ~10 deg wide at this scale and cannot
    # be placed without either clipping the frame or crowding Manavgat
    "kozan_2023": "Kozan 2023\n(gate control)",
}
# Absolute label anchors in data degrees (x, y, ha, va). Chosen to sit in open
# water or empty land away from coastlines, with a leader line back to the AOI.
ANCHOR = {
    "bejis_2022":        (-3.05, 42.20, "center", "bottom"),
    "montiferru_2021":   ( 6.10, 43.10, "center", "bottom"),
    "evia_2021_extended":(19.60, 41.90, "center", "bottom"),
    "mugla_2021":        (25.10, 35.10, "center", "top"),
    "manavgat_2021":     (32.60, 35.10, "center", "top"),
    "kozan_2023":        (35.60, 39.10, "center", "bottom"),
}

# ---- asserts vs 03_methods Table 1 (study regions) ----
EXPECT = {
    "manavgat_2021": (31.05, 36.72, 31.85, 37.35),
    "bejis_2022": (-1.05, 39.68, -0.35, 40.15),
    "mugla_2021": (27.10, 36.60, 28.90, 37.45),
    "evia_2021_extended": (23.05, 38.55, 23.85, 39.15),
    "montiferru_2021": (8.45, 40.05, 8.75, 40.27),
}
for reg, exp in EXPECT.items():
    got = AOI[reg]["bbox"]
    assert all(abs(g - e) < 5e-3 for g, e in zip(got, exp)), (reg, got, exp)

# Kozan is not in Table 1 (it is not a study region), so it is cross-checked
# against an INDEPENDENT source: the frozen Step 2B DEM metadata AOI polygon,
# which comes from the region registry rather than from the step8a grid.
_KOZAN_STEP2B = (35.25828811820405, 37.00022858198274,
                 36.384265065162296, 37.899943297574104)
assert all(abs(g - e) < 5e-3 for g, e in zip(AOI[CONTROL]["bbox"], _KOZAN_STEP2B)), \
    (CONTROL, AOI[CONTROL]["bbox"], _KOZAN_STEP2B)
assert AOI[CONTROL]["role"] == "gate_control"

MM = 1 / 25.4
proj = ccrs.PlateCarree()
plt.rcParams.update({"svg.fonttype": "none", "pdf.fonttype": 42})

# Canvas sized to the map's own aspect. PlateCarree holds an equal aspect, so a
# canvas taller than the data ratio is padded with an empty band above and below
# the map rather than with usable space; the axes box is therefore computed from
# the extent instead of guessed.
EXTENT = [-6.0, 39.4, 33.2, 45.6]
W_MM, L_MM, R_MM, B_MM, T_MM = 190.0, 12.0, 3.0, 11.0, 3.5
AX_W_MM = W_MM - L_MM - R_MM
AX_H_MM = AX_W_MM * (EXTENT[3] - EXTENT[2]) / (EXTENT[1] - EXTENT[0])
H_MM = AX_H_MM + B_MM + T_MM

fig = plt.figure(figsize=(W_MM * MM, H_MM * MM))
ax = fig.add_axes([L_MM / W_MM, B_MM / H_MM, AX_W_MM / W_MM, AX_H_MM / H_MM],
                  projection=proj)
ax.set_extent(EXTENT, crs=proj)

ax.add_feature(cfeature.NaturalEarthFeature("physical", "land", "50m"),
               facecolor=LAND, edgecolor="none", zorder=0)
ax.add_feature(cfeature.NaturalEarthFeature("physical", "coastline", "50m"),
               edgecolor=COAST, facecolor="none", linewidth=0.6, zorder=1)

halo = dict(boxstyle="round,pad=0.22", facecolor="white", alpha=0.82,
            edgecolor="none")

for reg, info in AOI.items():
    W, S, E, N = info["bbox"]
    control = reg == CONTROL
    col = GREY if control else BLUE
    # AOIs are small at basin scale: draw the true box, then a marker so the
    # location is findable without exaggerating the footprint. The control gets
    # a dashed edge, a grey hue and a square marker - three redundant cues, so
    # the distinction survives greyscale printing and colour-blind readers.
    ax.add_patch(plt.Rectangle(
        (W, S), E - W, N - S, facecolor=col, alpha=0.30 if not control else 0.16,
        edgecolor=col, linewidth=1.2,
        linestyle=(0, (2.4, 1.4)) if control else "solid",
        transform=proj, zorder=3))
    cx, cy = (W + E) / 2, (S + N) / 2
    ax.plot([cx], [cy], marker="s" if control else "o", markersize=6.5,
            markerfacecolor="none", markeredgecolor=col, markeredgewidth=1.1,
            transform=proj, zorder=3)

    tx, ty, ha, va = ANCHOR[reg]
    ax.annotate(LABEL[reg], xy=(cx, cy), xytext=(tx, ty),
                fontsize=FS_BODY, ha=ha, va=va, transform=proj,
                color=GREY if control else "black",
                bbox=halo, zorder=5, linespacing=1.25,
                arrowprops=dict(arrowstyle="-", lw=0.7, color=col if control else "#555555",
                                linestyle="dashed" if control else "solid",
                                shrinkA=0, shrinkB=5))

# ---- legend: two categories, stated in words -------------------------------
n_study = sum(1 for r in AOI if r != CONTROL)
handles = [
    Line2D([], [], marker="o", linestyle="none", markersize=6.5,
           markerfacecolor="none", markeredgecolor=BLUE, markeredgewidth=1.1,
           label=f"Study region (n = {n_study})"),
    Line2D([], [], marker="s", linestyle="none", markersize=6.5,
           markerfacecolor="none", markeredgecolor=GREY, markeredgewidth=1.1,
           label="Gate control (not modelled)"),
]
leg = ax.legend(handles=handles, loc="lower left",
                bbox_to_anchor=(0.245, 0.035), fontsize=FS_SMALL,
                frameon=True, framealpha=0.9, edgecolor="#BBBBBB",
                borderpad=0.6, labelspacing=1.0, handletextpad=0.7)
leg.get_frame().set_linewidth(0.6)
leg.set_zorder(6)

gl = ax.gridlines(draw_labels=True, linewidth=0.3, color="#CFCFCF",
                  xlocs=range(-5, 40, 5), ylocs=range(34, 47, 2), zorder=2)
gl.top_labels = gl.right_labels = False
gl.xlabel_style = {"size": FS_SMALL}
gl.ylabel_style = {"size": FS_SMALL}

# approximate scale bar at 38 N (1 deg lon = 111.32*cos(38 deg) ~ 87.7 km)
km_per_deg = 111.32 * np.cos(np.deg2rad(38))
bar_km = 500
bar_deg = bar_km / km_per_deg
x0, y0 = -4.35, 43.85
ax.plot([x0, x0 + bar_deg], [y0, y0], color="black", lw=1.6, transform=proj,
        zorder=5)
for xe in (x0, x0 + bar_deg):
    ax.plot([xe, xe], [y0 - 0.16, y0 + 0.16], color="black", lw=1.2,
            transform=proj, zorder=5)
ax.text(x0 + bar_deg / 2, y0 + 0.35, f"{bar_km} km (at 38°N)",
        fontsize=FS_SMALL, ha="center", va="bottom", transform=proj,
        bbox=halo, zorder=5)

problems = layout_check(fig, "Fig. 1 - study-area map",
                        min_gap_pt=6.0, min_font_pt=8.0)

fig.savefig(HERE / "fig1_study_map.pdf")
fig.savefig(HERE / "fig1_study_map.svg")
if "--preview" in sys.argv:
    fig.savefig(HERE / "fig1_study_map_preview.png", dpi=300)

(HERE / "fig1_provenance.json").write_text(json.dumps({
    "figure": "Fig. 1 - study-area location map",
    "script": "paper/figures/fig1_study_map.py",
    "aoi_data": "paper/figures/data/fig1_aoi.json (step0 geojson / 30m-grid-derived; sha256 per source inside)",
    "basemap": {
        "dataset": "Natural Earth 1:50m physical: coastline + land",
        "fetched_via": f"cartopy {cartopy.__version__} downloader at build time",
        "note": "Natural Earth is public domain; version as shipped by NACIS CDN at build date 2026-08-08",
    },
    "asserts": "all five AOI bboxes match 03_methods Table 1 to 5e-3 deg",
    "design": "single AOI colour across the five study regions (no regime grouping implied); "
              "no topography/satellite; Kozan 2023 drawn as gate control in a distinct style "
              "(grey + dashed edge + square marker + role in label + separate legend entry) so "
              "its location is findable from Methods 3.3 / Results 4.1 without implying it "
              "entered any model",
    "kozan_bbox_source": "drive_new/kozan-legacy/step8a/step8a_dataset_stats.json (30 m reference-grid transform); "
                         "cross-checked in-script against the independent step2b_dem_metadata.json AOI polygon to 5e-3 deg",
    "palette": "Okabe-Ito blue (study) / neutral grey (control) on very light neutral land; greyscale-safe",
    "legend": ["Study region (n = 5)", "Gate control (not modelled)"],
    "canvas_mm": [round(W_MM, 1), round(H_MM, 1)],
    "column": "double (190 mm)",
    "font_pt": {"body": FS_BODY, "minimum": FS_SMALL},
    "layout_check": "paper/figures/_layout_check.py; "
                    f"{len(problems)} problems at build time",
    "environment": f"matplotlib {matplotlib.__version__}, cartopy {cartopy.__version__}",
}, indent=1, ensure_ascii=False), encoding="utf-8")
print("fig1 written; cartopy", cartopy.__version__)
