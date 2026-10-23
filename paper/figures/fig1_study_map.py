#!/usr/bin/env python3
"""Figure 1 - study regions and study areas (2026-10-23 redraw).

(b), added 2026-10-23 in place of the supplement's Fig. S1: the five study areas on the ~500 m grid,
each at its own scale with a 10 km bar, in five classes (burned, 2 km scar frame, within 10 km of a
burned cell, beyond 10 km, not modelled). The classes come from paper/figures/data/fig1b_frames.npz,
written by fig1b_data.py in the project venv (this script runs where cartopy is, without the parquet
stack). Asserts: cells, burned cells and the share beyond 10 km equal the rows of Table 1 in
03_methods.md.

(a) Mercator map of Natural Earth 1:50m land and coastline; one filled blue dot per study area at
its centre, a plain label beside each, and Kozan 2023 (the gate's negative control) as an open
grey square. A two-entry key in the open sea south of Sicily explains the two marks, because
Fire Ecology wants keys in the graphic and not in the legend. No rectangles (the bounding boxes
are in Table S13), label boxes, leader lines, graticule lines or north arrow (north is up;
latitude and longitude are labelled on the frame); a 500 km scale bar, exact at 38 N as the
caption says. The earlier version is in the git history before 2026-10-23.

AOI bounds: paper/figures/data/fig1_aoi.json (step0 geojson / grid-derived, sha256 per source
inside; asserted here against Table S13).
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
import _style as Sty
import matplotlib.patheffects as pe

HERE = Path(__file__).resolve().parent
AOI = json.loads((HERE / "data" / "fig1_aoi.json").read_text())["aoi"]

BLUE = Sty.BLUE
GREY = "#767676"   # gate control only
LAND = "#EFEFEC"
COAST = "#9A9A9A"
FS_BODY, FS_SMALL = Sty.FS_BODY, Sty.FS_SMALL

CONTROL = "kozan_2023"

LABEL = {
    "manavgat_2021": "Manavgat 2021", "bejis_2022": "Bejís 2022",
    "mugla_2021": "Muğla 2021", "evia_2021_extended": "North Evia 2021",
    "montiferru_2021": "Montiferru 2021", "kozan_2023": "Kozan 2023",
}
# label position relative to the marker, in degrees (dx, dy, ha, va), chosen to sit in open sea
# or on land away from coastlines
ANCHOR = {
    "bejis_2022":         (0.5, 0.45, "left", "bottom"),
    "montiferru_2021":    (-0.55, -0.35, "right", "top"),
    "evia_2021_extended": (0.0, 0.6, "center", "bottom"),
    "mugla_2021":         (0.5, -0.7, "left", "top"),
    "manavgat_2021":      (-0.35, 0.6, "left", "bottom"),
    "kozan_2023":         (0.55, -0.45, "left", "top"),
}
# ---- asserts vs Table S13 (bounding boxes of the study regions) ----
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

# Kozan is not in Table S13 (it is not a study region), so it is cross-checked
# against an INDEPENDENT source: the frozen Step 2B DEM metadata AOI polygon,
# which comes from the region registry rather than from the step8a grid.
_KOZAN_STEP2B = (35.25828811820405, 37.00022858198274,
                 36.384265065162296, 37.899943297574104)
assert all(abs(g - e) < 5e-3 for g, e in zip(AOI[CONTROL]["bbox"], _KOZAN_STEP2B)), \
    (CONTROL, AOI[CONTROL]["bbox"], _KOZAN_STEP2B)
assert AOI[CONTROL]["role"] == "gate_control"

MM = 1 / 25.4
proj = ccrs.PlateCarree()           # coordinates of the data
mapproj = ccrs.Mercator()           # conformal, so shapes are not stretched east-west
Sty.apply()

# ---- (b) data: five classes per study area, from fig1b_data.py --------------------------------
import hashlib
import io
import re
import zipfile
B_REG = ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended", "montiferru_2021"]
B_NAME = {"manavgat_2021": "Manavgat", "bejis_2022": "Bejís", "mugla_2021": "Muğla",
          "evia_2021_extended": "North Evia", "montiferru_2021": "Montiferru"}
B_DATA = HERE / "data" / "fig1b_frames.npz"
with zipfile.ZipFile(B_DATA) as _z:
    B_CAT = {r: np.load(io.BytesIO(_z.read(f"{r}.npy")), allow_pickle=False) for r in B_REG}
    B_STATS = json.loads(_z.read("stats.json"))
# Table 1 (cells, burned, share beyond 10 km), as in fig1b_data.py
_EXPECT_B = {"manavgat_2021": (20511, 2935, 58.5), "bejis_2022": (15190, 1100, 63.1),
             "mugla_2021": (41730, 2911, 55.3), "evia_2021_extended": (9298, 2664, 43.7),
             "montiferru_2021": (2544, 539, 2.1)}
_t1 = (HERE.parent / "03_methods.md").read_text(encoding="utf-8")
for r in B_REG:
    s, cat = B_STATS[r], B_CAT[r]
    assert (s["cells"], s["burned"], s["beyond_10km_pct"]) == _EXPECT_B[r], (r, s)
    assert int((cat > 0).sum()) == s["cells"] and int((cat == 4).sum()) == s["burned"], r
    # the row of Table 1 in Methods prints the same cells, burned cells, prevalence and share
    row = re.search(rf"(?m)^\| {re.escape(LABEL[r])} .*$", _t1)
    assert row, f"Table 1 has no row for {LABEL[r]}"
    for v in (f"{s['cells']:,}", f"{s['burned']:,}", f"{s['burned'] / s['cells']:.3f}",
              f"{s['beyond_10km_pct']:.1f} %"):
        assert f" {v} |" in row.group(0), (r, v, row.group(0))
B_COLOURS = ["white", "#E6E6E6", "#A9CCE3", BLUE, Sty.INK]   # not modelled, beyond, within 10 km, frame, burned
B_KEY = ["burned", "2 km scar frame", "within 10 km", "beyond 10 km", "not modelled"]

# ---- canvas, in mm from the bottom: key row, scale bars, (b) panels and titles, then (a) ---------
EXTENT = [-6.0, 44.0, 33.2, 45.6]
_c = mapproj.transform_points(proj, np.array([EXTENT[0], EXTENT[1]]), np.array([EXTENT[2], EXTENT[3]]))
W_MM, L_MM, R_MM, B_MM, T_MM = Sty.WIDTH_MM, 12.0, 3.0, 9.0, 5.0
AX_W_MM = W_MM - L_MM - R_MM
AX_H_MM = AX_W_MM * (_c[1, 1] - _c[0, 1]) / (_c[1, 0] - _c[0, 0])
KEY_Y, BAR_Y, PB_Y0, PB_X0, PB_X1, PB_GAP = 3.5, 11.5, 13.5, 8.5, 168.5, 3.0
_km = {r: (B_STATS[r]["cols"] * B_STATS[r]["ew_km"], B_STATS[r]["rows"] * B_STATS[r]["ns_km"]) for r in B_REG}
PB_H = (PB_X1 - PB_X0 - PB_GAP * (len(B_REG) - 1)) / sum(w / h for w, h in _km.values())
PA_Y0 = PB_Y0 + PB_H + 1.0 + 3.5 + 1.5 + B_MM        # titles of (b), a gap, then the longitude labels of (a)
H_MM = PA_Y0 + AX_H_MM + T_MM

fig = plt.figure(figsize=(W_MM * MM, H_MM * MM))
ax = fig.add_axes([L_MM / W_MM, PA_Y0 / H_MM, AX_W_MM / W_MM, AX_H_MM / H_MM], projection=mapproj)
fig.text(0.5 / W_MM, (PA_Y0 + AX_H_MM + 1.0) / H_MM, "(a)", fontsize=FS_BODY, ha="left", va="bottom")
fig.text(0.5 / W_MM, (PB_Y0 + PB_H + 1.0) / H_MM, "(b)", fontsize=FS_BODY, ha="left", va="bottom")

from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
x = PB_X0
for r in B_REG:
    wkm, hkm = _km[r]
    w = PB_H * wkm / hkm
    bx = fig.add_axes([x / W_MM, PB_Y0 / H_MM, w / W_MM, PB_H / H_MM])
    bx.imshow(B_CAT[r], cmap=ListedColormap(B_COLOURS), vmin=-0.5, vmax=4.5, interpolation="nearest",
              extent=[0, wkm, hkm, 0])
    bx.set_xlim(0, wkm)
    bx.set_ylim(hkm, 0)
    bx.set_xticks([])
    bx.set_yticks([])
    for sp in bx.spines.values():
        sp.set_visible(True)
        sp.set_linewidth(0.6)
        sp.set_edgecolor(Sty.MUTED)
    bx.set_title(B_NAME[r], fontsize=FS_BODY, loc="left", pad=3)
    bar = w * 10.0 / wkm                               # 10 km at this panel's scale
    fig.add_artist(Line2D([x / W_MM, (x + bar) / W_MM], [BAR_Y / H_MM] * 2, color=Sty.INK, lw=1.2,
                          solid_capstyle="butt"))
    fig.text(x / W_MM, (BAR_Y - 1.0) / H_MM, "10 km", fontsize=FS_SMALL, ha="left", va="top")
    x += w + PB_GAP
fig.legend([Patch(facecolor=c, edgecolor=Sty.MUTED if c == "white" else c, linewidth=0.6)
            for c in B_COLOURS[::-1]], B_KEY, loc="center", bbox_to_anchor=(0.5, KEY_Y / H_MM),
           ncol=5, frameon=False, fontsize=FS_SMALL, handlelength=1.2, handleheight=1.0,
           handletextpad=0.4, columnspacing=1.8, borderaxespad=0.0)
ax.set_extent(EXTENT, crs=proj)

ax.add_feature(cfeature.NaturalEarthFeature("physical", "land", "50m"),
               facecolor=LAND, edgecolor="none", zorder=0)
ax.add_feature(cfeature.NaturalEarthFeature("physical", "coastline", "50m"),
               edgecolor=COAST, facecolor="none", linewidth=0.6, zorder=1)

halo = [pe.withStroke(linewidth=1.0, foreground="white")]   # thin: keeps text legible on a coastline
for reg, info in AOI.items():
    W, S, E, N = info["bbox"]
    control = reg == CONTROL
    col = GREY if control else BLUE
    cx, cy = (W + E) / 2, (S + N) / 2
    ax.plot([cx], [cy], marker="s" if control else "o", markersize=5.5,
            markerfacecolor="white" if control else col, markeredgecolor=col, markeredgewidth=1.1,
            transform=proj, zorder=4)
    dx, dy, ha, va = ANCHOR[reg]
    ax.text(cx + dx, cy + dy, LABEL[reg], fontsize=FS_BODY, ha=ha, va=va, transform=proj,
            color=GREY if control else Sty.INK, path_effects=halo, zorder=5)

# key in the open sea between Tunisia, Libya and Crete (no coastline north of 33.2 N there)
key = [Line2D([], [], marker="o", markersize=5.5, color=BLUE, lw=0),
       Line2D([], [], marker="s", markersize=5.5, markerfacecolor="white", markeredgecolor=GREY,
              markeredgewidth=1.1, lw=0)]
ax.legend(key, ["study area", "gate control, not modelled"], loc="lower left",
          bbox_to_anchor=(12.6, 33.8), bbox_transform=proj._as_mpl_transform(ax), frameon=False,
          fontsize=FS_SMALL, handletextpad=0.3, labelspacing=0.8, borderpad=0.0, borderaxespad=0.0)

gl = ax.gridlines(crs=proj, draw_labels=True, linewidth=0, xlocs=range(-5, 41, 5),
                  ylocs=range(34, 47, 2), zorder=2)
gl.top_labels = gl.right_labels = False
gl.xlabel_style = {"size": FS_SMALL}
gl.ylabel_style = {"size": FS_SMALL}
for sp in ax.spines.values():
    sp.set_linewidth(0.6)
    sp.set_edgecolor(Sty.MUTED)

# scale bar for 38 N (1 deg lon = 111.32*cos(38 deg) ~ 87.7 km); the caption states the latitude.
# In Mercator a degree of longitude has the same length at every latitude, so the bar can sit
# anywhere and still measure 500 km at 38 N.
km_per_deg = 111.32 * np.cos(np.deg2rad(38))
bar_km = 500
bar_deg = bar_km / km_per_deg
x0, y0 = -4.6, 44.6
ax.plot([x0, x0 + bar_deg], [y0, y0], color=Sty.INK, lw=1.2, transform=proj, zorder=5,
        solid_capstyle="butt")
ax.text(x0 + bar_deg / 2, y0 - 0.3, f"{bar_km} km", fontsize=FS_SMALL, ha="center", va="top",
        transform=proj, path_effects=halo, zorder=5)

problems = layout_check(fig, "Fig. 1 - study-area map",
                        min_gap_pt=6.0, min_font_pt=8.0)

fig.savefig(HERE / "fig1_study_map.pdf")
fig.savefig(HERE / "fig1_study_map.svg")
if "--preview" in sys.argv:
    fig.savefig(HERE / "fig1_study_map_preview.png", dpi=300)

# Natural Earth files actually read from the cartopy cache: sha256 and download time, so a
# later rebuild can tell whether it used the same basemap (added 2026-09-23).
import datetime
import hashlib
import shapely
import pyproj
_NE_DIR = Path(cartopy.config["data_dir"]) / "shapefiles" / "natural_earth" / "physical"
NE_FILES = {}
for _stem in ("ne_50m_land", "ne_50m_coastline"):
    for _ext in (".shp", ".shx", ".dbf"):
        _f = _NE_DIR / (_stem + _ext)
        NE_FILES[_f.name] = {
            "sha256": hashlib.sha256(_f.read_bytes()).hexdigest(),
            "downloaded": datetime.datetime.fromtimestamp(_f.stat().st_mtime).isoformat(timespec="seconds"),
        }

(HERE / "fig1_provenance.json").write_text(json.dumps({
    "figure": "Fig. 1 - study-area location map",
    "script": "paper/figures/fig1_study_map.py",
    "aoi_data": {"path": "paper/figures/data/fig1_aoi.json",
                 "sha256": hashlib.sha256((HERE / "data" / "fig1_aoi.json").read_bytes()).hexdigest(),
                 "note": "step0 geojson / 30m-grid-derived; sha256 per source inside"},
    "panel_b_data": {"path": "paper/figures/data/fig1b_frames.npz",
                     "sha256": hashlib.sha256(B_DATA.read_bytes()).hexdigest(),
                     "written_by": "paper/figures/fig1b_data.py (project venv, modelling datasets via _canonical.py)",
                     "stats": B_STATS},
    "basemap": {
        "dataset": "Natural Earth 1:50m physical: coastline + land",
        "fetched_via": f"cartopy {cartopy.__version__} downloader; files read from the cartopy cache",
        "note": "Natural Earth is public domain; version as shipped by NACIS CDN on the download date "
                "below (the cache files carry no version string)",
        "files": NE_FILES,
    },
    "geo_stack": {"cartopy": cartopy.__version__, "shapely": shapely.__version__,
                  "geos": shapely.geos_version_string, "pyproj": pyproj.__version__,
                  "proj": pyproj.proj_version_str},
    "reproducibility": (
        "Re-rendered 2026-09-23 and committed as the figure of record. The previous render "
        "(2026-08-08) could not be reproduced by this script with the Natural Earth files, the AOI "
        "file and the geo stack recorded here, although all three predate it; the cause was not "
        "identified. Its production environment is uncertain: its SVG dc:date reads 23:46 while "
        "the commit that added it is timed 20:49, which is inconsistent. The present render is "
        "deterministic in this environment (two consecutive rebuilds are identical once "
        "matplotlib ids are normalised). It differs from the previous one by two small paths at "
        "the top-left edge of the map, one land fill and its coastline; no AOI, marker or label "
        "is affected. An earlier commit message (67790d8) attributed the difference to cartopy "
        "re-fetching its coastline data; that was wrong, since the cache files date from "
        "2026-08-08."),
    "asserts": "all five AOI bboxes match Table S13 to 5e-3 deg; panel (b) cells, burned cells and the share beyond 10 km match Table 1",
    "design": "2026-10-23 redraw: one blue dot per study area (no regime grouping implied); no "
              "topography/satellite; Kozan 2023 as an open grey square with its own key entry, so its "
              "location is findable from the gate section without implying it entered any model; "
              "170 mm wide (SpringerOpen full page width), key inside the graphic",
    "kozan_bbox_source": "drive_new/kozan-legacy/step8a/step8a_dataset_stats.json (30 m reference-grid transform); "
                         "cross-checked in-script against the independent step2b_dem_metadata.json AOI polygon to 5e-3 deg",
    "palette": "Okabe-Ito blue (study) / neutral grey (control) on very light neutral land; greyscale-safe",
    "canvas_mm": [round(W_MM, 1), round(H_MM, 1)],
    "font_pt": {"body": FS_BODY, "minimum": FS_SMALL},
    "layout_check": "paper/figures/_layout_check.py; "
                    f"{len(problems)} problems at build time",
    "environment": f"matplotlib {matplotlib.__version__}, cartopy {cartopy.__version__}",
}, indent=1, ensure_ascii=False), encoding="utf-8")
print("fig1 written; cartopy", cartopy.__version__)
