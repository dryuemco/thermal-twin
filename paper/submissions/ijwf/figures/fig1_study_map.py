#!/usr/bin/env python3
"""Figure 1 - study regions and study areas (2026-10-23 redraw).

IJWF copy (2026-11-11) of paper/figures/fig1_study_map.py, which is left as it is. The data and the
asserts are those of the shared script and are read from the shared paths (paper/figures/data,
paper/03_methods.md). Changed for the publisher's figure guide: part labels and the titles of (b)
8 pt, map labels, graticule labels, scale bars and keys 7 pt (_style_ijwf.py), sentence case in the
two keys, and the labels of (a) placed again so that each belongs to one marker only (see ANCHOR;
the placement is measured and asserted after drawing). Markers, colours, extent and (b) are as shared.
Writes fig1_study_map.pdf, .svg, _preview.png and fig1_provenance.json next to this file.
Needs cartopy, which the project environments do not have; it uses the Natural Earth files of the
cartopy cache and downloads nothing when they are there.

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

sys.dont_write_bytecode = True                    # nothing is written into paper/figures, not even bytecode
HERE = Path(__file__).resolve().parent            # paper/submissions/ijwf/figures: every output goes here
SHARED = HERE.parents[2] / "figures"              # paper/figures: read only
PAPER = SHARED.parent                             # paper: Table 1 in 03_methods.md
sys.path[:0] = [str(HERE), str(SHARED)]
from _layout_check import check as layout_check, _gap_pt   # noqa: E402
import _style_ijwf as Sty                                  # noqa: E402
import matplotlib.patheffects as pe

AOI = json.loads((SHARED / "data" / "fig1_aoi.json").read_text())["aoi"]

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
# map text where it differs from LABEL (LABEL also finds the Table 1 rows, so it keeps one line)
MAP_LABEL = {"montiferru_2021": "Montiferru\n2021", "mugla_2021": "Muğla\n2021",
             "manavgat_2021": "Manavgat\n2021"}
# label position relative to the marker, in degrees (dx, dy, ha, va). IJWF placement of 2026-11-11: a
# label touches no marker, has its own marker next to it and every other marker well away, and needs
# no leader line. The asserts after the layout check measure this on the drawn figure.
ANCHOR = {
    "bejis_2022":         (0.5, 0.45, "left", "bottom"),       # as shared
    # below Sardinia on two lines, as shared since 2026-10-25: to the left of the dot the label sat under
    # "Bejís 2022" and read as a second label of the Bejís dot
    "montiferru_2021":    (0.0, -1.35, "center", "top"),
    # above its dot as shared, 0.35 deg further west to stay 6 pt clear of the Muğla label
    "evia_2021_extended": (-0.35, 0.6, "center", "bottom"),
    # Muğla, Manavgat and Kozan lie 3.5 and 4.4 deg apart, less than the width of a one-line label, so a
    # label beside or below one dot reached the next (shared figure: "Manavgat 2021" ran up to the Kozan
    # square, "Muğla 2021" lay under both dots). The two study areas now have two-line labels above
    # their own dots, on land east of the Aegean coast where no coastline crosses them (Rhodes and the
    # bays of the south coast are under the dots). Both are a little east of centre: the Muğla label to
    # clear the coast, the Manavgat label to keep 6 pt from it.
    "mugla_2021":         (0.45, 0.55, "center", "bottom"),
    "manavgat_2021":      (0.95, 0.55, "center", "bottom"),
    # to the right of its square, on land, with no marker further east
    "kozan_2023":         (0.6, 0.0, "left", "center"),
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
B_DATA = SHARED / "data" / "fig1b_frames.npz"
with zipfile.ZipFile(B_DATA) as _z:
    B_CAT = {r: np.load(io.BytesIO(_z.read(f"{r}.npy")), allow_pickle=False) for r in B_REG}
    B_STATS = json.loads(_z.read("stats.json"))
# Table 1 (cells, burned, share beyond 10 km), as in fig1b_data.py
_EXPECT_B = {"manavgat_2021": (20511, 2935, 58.5), "bejis_2022": (15190, 1100, 63.1),
             "mugla_2021": (41730, 2911, 55.3), "evia_2021_extended": (9298, 2664, 43.7),
             "montiferru_2021": (2544, 539, 2.1)}
_t1 = (PAPER / "03_methods.md").read_text(encoding="utf-8")
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
B_KEY = ["Burned", "2 km scar frame", "Within 10 km", "Beyond 10 km", "Not modelled"]

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
MARK, TEXT = {}, {}                                         # kept for the placement check below
for reg, info in AOI.items():
    W, S, E, N = info["bbox"]
    control = reg == CONTROL
    col = GREY if control else BLUE
    cx, cy = (W + E) / 2, (S + N) / 2
    MARK[reg], = ax.plot([cx], [cy], marker="s" if control else "o", markersize=5.5,
                         markerfacecolor="white" if control else col, markeredgecolor=col, markeredgewidth=1.1,
                         transform=proj, zorder=4)
    dx, dy, ha, va = ANCHOR[reg]
    TEXT[reg] = ax.text(cx + dx, cy + dy, MAP_LABEL.get(reg, LABEL[reg]), fontsize=FS_SMALL, ha=ha, va=va,
                        multialignment="center", transform=proj,
                        color=GREY if control else Sty.INK, path_effects=halo, zorder=5)

# key in the open sea between Tunisia, Libya and Crete (no coastline north of 33.2 N there)
key = [Line2D([], [], marker="o", markersize=5.5, color=BLUE, lw=0),
       Line2D([], [], marker="s", markersize=5.5, markerfacecolor="white", markeredgecolor=GREY,
              markeredgewidth=1.1, lw=0)]
key_a = ax.legend(key, ["Study area", "Gate control, not modelled"], loc="lower left",
                  bbox_to_anchor=(12.6, 33.8), bbox_transform=proj._as_mpl_transform(ax), frameon=False,
                  fontsize=FS_SMALL, handletextpad=0.3, labelspacing=0.92, borderpad=0.0, borderaxespad=0.0)
# labelspacing 0.92, not the shared 0.8: it is in units of the font size, and 0.8 of 7 pt left the two
# entries 5.6 pt apart, under the 6 pt of the layout check (0.92 gives the 6.4 pt of the shared figure)

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
bar_a, = ax.plot([x0, x0 + bar_deg], [y0, y0], color=Sty.INK, lw=1.2, transform=proj, zorder=5,
                 solid_capstyle="butt")
ax.text(x0 + bar_deg / 2, y0 - 0.3, f"{bar_km} km", fontsize=FS_SMALL, ha="center", va="top",
        transform=proj, path_effects=halo, zorder=5)

problems = layout_check(fig, "Fig. 1 - study-area map",
                        min_gap_pt=6.0, min_font_pt=FS_SMALL)
sizes = Sty.font_sizes(fig)

# ---- the labels of (a), measured on the drawn figure (gaps between bounding boxes, in points) --------
# A label keeps clear of its own marker and is nearer to it than to anything else: every other marker
# is at least 9 pt and at least two and a half times as far away, and the key and the scale bar are
# 6 pt away or more. The 6 pt between any two texts is part of the layout check above.
_r = fig.canvas.get_renderer()
PLACEMENT = {}
for reg, t in TEXT.items():
    tb = t.get_window_extent(_r)
    own = _gap_pt(tb, MARK[reg].get_window_extent(_r), fig.dpi)
    other = {m: _gap_pt(tb, a.get_window_extent(_r), fig.dpi) for m, a in MARK.items() if m != reg}
    near = min(other, key=other.get)
    key_gap = _gap_pt(tb, key_a.get_window_extent(_r), fig.dpi)
    bar_gap = _gap_pt(tb, bar_a.get_window_extent(_r), fig.dpi)
    assert 1.5 <= own <= 15.0, f"{LABEL[reg]}: {own:.1f} pt from its own marker"
    assert other[near] >= max(9.0, 2.5 * own), f"{LABEL[reg]}: {other[near]:.1f} pt from the marker of {near}"
    assert min(key_gap, bar_gap) >= 6.0, f"{LABEL[reg]}: {key_gap:.1f} pt from the key, {bar_gap:.1f} pt from the bar"
    PLACEMENT[LABEL[reg]] = {"anchor_deg": list(ANCHOR[reg]), "own_marker_pt": round(own, 1),
                             "nearest_other_marker": LABEL[near], "nearest_other_marker_pt": round(other[near], 1)}
    print(f"  label {LABEL[reg]:<16} own marker {own:5.1f} pt, next marker ({LABEL[near]}) {other[near]:6.1f} pt")

Sty.save(fig, HERE, "fig1_study_map")

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
# the basemap of this copy against the one recorded for the shared figure (read only)
_shared_ne = json.loads((SHARED / "fig1_provenance.json").read_text(encoding="utf-8"))["basemap"]["files"]
SAME_BASEMAP = ({k: v["sha256"] for k, v in NE_FILES.items()}
                == {k: v["sha256"] for k, v in _shared_ne.items()})

(HERE / "fig1_provenance.json").write_text(json.dumps({
    "figure": "Fig. 1 - study-area location map, IJWF package",
    "script": "paper/submissions/ijwf/figures/fig1_study_map.py",
    "source": "copy of paper/figures/fig1_study_map.py with the same data and asserts",
    "ijwf_changes": "part labels and titles of (b) 8 pt; map labels (9 pt in the shared figure), graticule "
                    "labels, scale bars and keys 7 pt; sentence case in the two keys (Study area, Gate control, "
                    "not modelled, Burned, Within 10 km, Beyond 10 km, Not modelled); labels of (a) placed again, "
                    "see label_placement",
    "label_placement": {
        "rule": "gaps between bounding boxes in points, asserted at build time: 1.5 to 15 pt to the own marker, "
                "every other marker at least 9 pt and two and a half times as far away, key and scale bar at "
                "least 6 pt away, any two texts at least 6 pt apart (layout check)",
        "labels": PLACEMENT},
    "aoi_data": {"path": "paper/figures/data/fig1_aoi.json",
                 "sha256": hashlib.sha256((SHARED / "data" / "fig1_aoi.json").read_bytes()).hexdigest(),
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
        "same_files_as_shared_figure": SAME_BASEMAP,
    },
    "geo_stack": {"cartopy": cartopy.__version__, "shapely": shapely.__version__,
                  "geos": shapely.geos_version_string, "pyproj": pyproj.__version__,
                  "proj": pyproj.proj_version_str},
    "reproducibility": (
        "Drawn for the IJWF package on 2026-11-11 in a separate environment with cartopy (the project "
        "environments have none), from the Natural Earth files of the cartopy cache. "
        "same_files_as_shared_figure compares their sha256 with those in paper/figures/fig1_provenance.json. "
        "The history of the shared render is recorded there and is not repeated here."),
    "asserts": "all five AOI bboxes match Table S13 to 5e-3 deg; panel (b) cells, burned cells and the share beyond 10 km match Table 1",
    "design": "2026-10-23 redraw: one blue dot per study area (no regime grouping implied); no "
              "topography/satellite; Kozan 2023 as an open grey square with its own key entry, so its "
              "location is findable from the gate section without implying it entered any model; "
              "170 mm wide (SpringerOpen full page width), key inside the graphic",
    "kozan_bbox_source": "drive_new/kozan-legacy/step8a/step8a_dataset_stats.json (30 m reference-grid transform); "
                         "cross-checked in-script against the independent step2b_dem_metadata.json AOI polygon to 5e-3 deg",
    "palette": "Okabe-Ito blue (study) / neutral grey (control) on very light neutral land; greyscale-safe",
    "canvas_mm": [round(W_MM, 1), round(H_MM, 1)],
    "font_pt": {"body": FS_BODY, "minimum": FS_SMALL, "used": sizes},
    "layout_check": "paper/figures/_layout_check.py; "
                    f"{len(problems)} problems at build time",
    "environment": f"matplotlib {matplotlib.__version__}, cartopy {cartopy.__version__}",
}, indent=1, ensure_ascii=False), encoding="utf-8")
print("fig1 written; cartopy", cartopy.__version__, "; same Natural Earth files as the shared figure:", SAME_BASEMAP)
