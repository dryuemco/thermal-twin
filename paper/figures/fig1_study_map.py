#!/usr/bin/env python3
"""Figure 1 - study-area location map (plain, Mediterranean basin).

Natural Earth 1:50m coastline, five AOI rectangles (single colour - no regime
implication), region + year labels, approximate scale bar. No topography, no
satellite background; country borders omitted (kept plain per design decision).
Kozan (negative control) deliberately not shown - it appears in Methods only.
AOI bounds: paper/figures/data/fig1_aoi.json (step0 geojson / grid-derived,
sha256 per source inside; asserted here against 03_methods Table 1).
Okabe-Ito, greyscale-safe, vector, min font 7 pt.
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

HERE = Path(__file__).resolve().parent
AOI = json.loads((HERE / "data" / "fig1_aoi.json").read_text())["aoi"]

BLUE = "#0072B2"  # single colour for every AOI - no regime grouping implied
LABEL = {
    "manavgat_2021": "Manavgat 2021", "bejis_2022": "Bejís 2022",
    "mugla_2021": "Muğla 2021", "evia_2021_extended": "Evia 2021",
    "montiferru_2021": "Montiferru 2021",
}
# label anchor offsets (deg): keep text clear of coast/rectangles
OFFSET = {
    "manavgat_2021": (0.3, -1.55, "center", "top"),
    "bejis_2022": (0.0, 0.75, "center", "bottom"),
    "mugla_2021": (-0.4, 1.35, "center", "bottom"),
    "evia_2021_extended": (-2.5, 0.55, "center", "bottom"),
    "montiferru_2021": (0.15, 0.85, "center", "bottom"),
}

# ---- asserts vs 03_methods Table 1 ----
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

MM = 1 / 25.4
proj = ccrs.PlateCarree()
fig = plt.figure(figsize=(190 * MM, 78 * MM))
plt.rcParams.update({"svg.fonttype": "none", "pdf.fonttype": 42})
ax = fig.add_axes([0.045, 0.06, 0.945, 0.92], projection=proj)
ax.set_extent([-5.5, 34.5, 33.5, 45.2], crs=proj)

coast = cfeature.NaturalEarthFeature("physical", "coastline", "50m")
ax.add_feature(coast, edgecolor="#666666", facecolor="none", linewidth=0.6)

for reg, info in AOI.items():
    W, S, E, N = info["bbox"]
    ax.add_patch(plt.Rectangle((W, S), E - W, N - S, facecolor=BLUE, alpha=0.25,
                               edgecolor=BLUE, linewidth=1.4,
                               transform=proj, zorder=3))
    dx, dy, ha, va = OFFSET[reg]
    cx, cy = (W + E) / 2, (S + N) / 2
    tx, ty = cx + dx, (N if dy > 0 else S) + dy
    ax.annotate(LABEL[reg], xy=(cx, cy), xytext=(tx, ty),
                fontsize=7.5, ha=ha, va=va, transform=proj,
                arrowprops=dict(arrowstyle="-", lw=0.6, color="#555555",
                                shrinkA=0, shrinkB=2), zorder=4)

gl = ax.gridlines(draw_labels=True, linewidth=0.3, color="#CCCCCC",
                  xlocs=range(-5, 36, 5), ylocs=range(34, 46, 2))
gl.top_labels = gl.right_labels = False
gl.xlabel_style = {"size": 7}
gl.ylabel_style = {"size": 7}

# approximate scale bar at 38 N (1 deg lon = 111.32*cos(38 deg) ~ 87.7 km)
km_per_deg = 111.32 * np.cos(np.deg2rad(38))
bar_km = 500
bar_deg = bar_km / km_per_deg
x0, y0 = -4.6, 34.3
ax.plot([x0, x0 + bar_deg], [y0, y0], color="black", lw=1.6, transform=proj)
for xe in (x0, x0 + bar_deg):
    ax.plot([xe, xe], [y0 - 0.12, y0 + 0.12], color="black", lw=1.2,
            transform=proj)
ax.text(x0 + bar_deg / 2, y0 + 0.25, f"{bar_km} km (at 38°N)", fontsize=7,
        ha="center", transform=proj)

fig.savefig(HERE / "fig1_study_map.pdf")
fig.savefig(HERE / "fig1_study_map.svg")
if "--preview" in sys.argv:
    fig.savefig(HERE / "fig1_study_map_preview.png", dpi=220)

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
    "design": "single AOI colour (no regime grouping implied); no topography/satellite; Kozan control omitted by design",
    "palette": "Okabe-Ito blue on neutral grey land; greyscale-safe",
    "min_font_pt": 7.0,
    "environment": f"matplotlib {matplotlib.__version__}, cartopy {cartopy.__version__}",
}, indent=1))
print("fig1 written; cartopy", cartopy.__version__)
