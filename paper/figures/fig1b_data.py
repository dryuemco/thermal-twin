#!/usr/bin/env python3
"""Data for Fig. 1b - the five study areas at cell level (2026-10-23).

Fig. 1 is drawn in the WSL environment that has cartopy but not the parquet stack, so this script
reads the released modelling datasets (through paper/code/_canonical.py, which checks each file's
SHA-256) in the project venv and writes one small file, paper/figures/data/fig1b_frames.npz, that
fig1_study_map.py reads. Each region becomes a grid of five classes:

    0  not modelled (outside the natural-vegetation population)
    1  modelled, more than 10 km from any burned cell
    2  modelled and unburned, within 10 km of a burned cell (the 10 km distance collar)
    3  modelled and unburned, inside a 2 km scar frame (Section 2.12)
    4  burned

Distances follow Section 2.12: 0.45 km per grid step, Euclidean, to the nearest burned cell of the
population; a scar is an 8-connected group of at least 50 burned cells and its frame reaches 4 grid
steps (taxicab). Asserts: cells and burned cells equal Table S15 (and Table 1), and the share of cells
beyond 10 km equals Table S13 (and Table 1) to 0.1 %. The archive is written with fixed timestamps,
so a rebuild from the same data is byte-identical.
"""
import io
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
from scipy import ndimage

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "code"))
import _canonical  # noqa: E402

REGIONS = ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended", "montiferru_2021"]
CELL_KM, COLLAR_KM, SCAR_MIN, FRAME_STEPS = 0.45, 10.0, 50, 4
NS_KM = 17 * 0.00026949458523585647 * 111.32        # 17 pixels of the 30 m reference grid, north-south
# Table S15 (cells, burned cells of the natural-vegetation population) and Table S13 (share beyond 10 km)
EXPECT = {"manavgat_2021": (20511, 2935, 58.5), "bejis_2022": (15190, 1100, 63.1),
          "mugla_2021": (41730, 2911, 55.3), "evia_2021_extended": (9298, 2664, 43.7),
          "montiferru_2021": (2544, 539, 2.1)}

arrays, stats = {}, {}
for reg in REGIONS:
    d = _canonical.load(reg)
    r0, c0 = int(d.row_500m.min()), int(d.col_500m.min())
    H, W = int(d.row_500m.max()) - r0 + 1, int(d.col_500m.max()) - c0 + 1
    rr = d.row_500m.to_numpy().astype(int) - r0
    cc = d.col_500m.to_numpy().astype(int) - c0
    assert np.corrcoef(rr, d.lat.to_numpy())[0, 1] < 0, f"{reg}: row 0 is not the northern edge"
    pop = ((d.valid_for_modeling == True) & (d.burnable_tree_shrub_grass == True)).to_numpy()  # noqa: E712
    P = np.zeros((H, W), bool)
    P[rr[pop], cc[pop]] = True
    B = np.zeros((H, W), bool)
    b = pop & (d.burned.to_numpy() == 1)
    B[rr[b], cc[b]] = True

    dist = ndimage.distance_transform_edt(~B) * CELL_KM
    lab, _ = ndimage.label(B, structure=np.ones((3, 3)))
    sizes = np.bincount(lab.ravel())
    big = np.isin(lab, [k for k in range(1, len(sizes)) if sizes[k] >= SCAR_MIN])
    frame = ndimage.distance_transform_cdt(~big, metric="taxicab") <= FRAME_STEPS

    cat = np.zeros((H, W), np.uint8)
    cat[P] = 1
    cat[P & (dist <= COLLAR_KM)] = 2
    cat[P & frame & ~B] = 3
    cat[B] = 4

    n_cells, n_burned = int(P.sum()), int(B.sum())
    beyond = 100 * float((dist[P] > COLLAR_KM).mean())
    want = EXPECT[reg]
    assert (n_cells, n_burned) == want[:2], (reg, n_cells, n_burned, want)
    assert abs(beyond - want[2]) < 0.05 + 1e-9, (reg, round(beyond, 2), want[2])
    ew_km = NS_KM * float(np.cos(np.deg2rad(d.lat.mean())))
    arrays[reg] = cat
    stats[reg] = {"rows": H, "cols": W, "ns_km": NS_KM, "ew_km": ew_km, "cells": n_cells,
                  "burned": n_burned, "beyond_10km_pct": round(beyond, 1),
                  "scars_ge_50": int((sizes[1:] >= SCAR_MIN).sum()),
                  "edge_burned": int(B[0, :].sum() + B[-1, :].sum() + B[:, 0].sum() + B[:, -1].sum())}
    print(f"{reg}: {H}x{W} cells, {n_cells} modelled, {n_burned} burned, {beyond:.1f} % beyond 10 km, "
          f"{stats[reg]['scars_ge_50']} scars, {stats[reg]['edge_burned']} burned cells on the edge")

# npz with fixed member timestamps (np.savez stamps the current time)
out = HERE / "data" / "fig1b_frames.npz"
buf = io.BytesIO()
with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
    for reg in REGIONS:
        arr = io.BytesIO()
        np.lib.format.write_array(arr, arrays[reg], allow_pickle=False)
        z.writestr(zipfile.ZipInfo(f"{reg}.npy", date_time=(1980, 1, 1, 0, 0, 0)), arr.getvalue(),
                   compress_type=zipfile.ZIP_DEFLATED)
    z.writestr(zipfile.ZipInfo("stats.json", date_time=(1980, 1, 1, 0, 0, 0)),
               json.dumps(stats, indent=1, sort_keys=True), compress_type=zipfile.ZIP_DEFLATED)
out.write_bytes(buf.getvalue())
print(f"wrote {out.relative_to(HERE.parent.parent)}")
