"""Fig. S1: the five study areas at cell level (reviewers 1 and 3).

Each panel shows one study area on the ~500 m grid: elevation of the natural-vegetation cells
(grey shading), cells outside that population (white), burned cells (red), and the 5 km and 10 km
distance collars (dashed and solid lines; distance to the nearest burned cell at 0.45 km per grid
step, as in Section 3.12). Data: the released modelling datasets through paper/code/_canonical.py.
Run from the repository root.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.colors import ListedColormap  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
from scipy import ndimage  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "code"))
import _canonical  # noqa: E402

REG = [("manavgat_2021", "Manavgat 2021"), ("bejis_2022", "Bejís 2022"), ("mugla_2021", "Muğla 2021"),
       ("evia_2021_extended", "North Evia 2021"), ("montiferru_2021", "Montiferru 2021")]
CELL_KM = 0.45
plt.rcParams.update({"font.size": 8, "pdf.fonttype": 42, "svg.fonttype": "none"})
fig, axes = plt.subplots(2, 3, figsize=(7.1, 5.2))
for ax, (reg, name) in zip(axes.flat, REG):
    d = _canonical.load(reg)
    r0, c0 = int(d.row_500m.min()), int(d.col_500m.min())
    H, W = int(d.row_500m.max()) - r0 + 1, int(d.col_500m.max()) - c0 + 1
    rr, cc = d.row_500m.to_numpy().astype(int) - r0, d.col_500m.to_numpy().astype(int) - c0
    pop = ((d.valid_for_modeling == True) & (d.burnable_tree_shrub_grass == True)).to_numpy()  # noqa: E712
    elev = np.full((H, W), np.nan)
    elev[rr[pop], cc[pop]] = d.elevation_mean.to_numpy()[pop]
    burned = np.zeros((H, W), bool)
    b = pop & (d.burned.to_numpy() == 1)
    burned[rr[b], cc[b]] = True
    dist = ndimage.distance_transform_edt(~burned) * CELL_KM
    ext = [0, W * 0.40, H * 0.51, 0]      # approximate km: east-west 0.40 km, north-south 0.51 km per cell
    ax.imshow(elev, cmap="Greys", extent=ext, interpolation="nearest")
    ax.imshow(np.where(burned, 1.0, np.nan), cmap=ListedColormap(["#D55E00"]), extent=ext, interpolation="nearest")
    yy = (np.arange(H) + 0.5) * 0.51
    xx = (np.arange(W) + 0.5) * 0.40
    ax.contour(xx, yy, dist, levels=[5], colors="#0072B2", linewidths=0.7, linestyles="--")
    ax.contour(xx, yy, dist, levels=[10], colors="#0072B2", linewidths=0.9)
    # scar frames of Table 2: 8-connected scars of >= 50 burned cells plus a collar of 4 grid steps
    # (Manhattan distance), as in Section 3.12
    lab, _ = ndimage.label(burned, structure=np.ones((3, 3)))
    sizes = np.bincount(lab.ravel())
    big = np.isin(lab, [k for k in range(1, len(sizes)) if sizes[k] >= 50])
    frame = ndimage.distance_transform_cdt(~big, metric="taxicab") <= 4
    ax.contour(xx, yy, frame.astype(float), levels=[0.5], colors="black", linewidths=0.6, linestyles=":")
    edge = int(burned[0, :].sum() + burned[-1, :].sum() + burned[:, 0].sum() + burned[:, -1].sum())
    print(f"{reg}: burned cells on the study-area edge = {edge}")
    ax.set_title(name, fontsize=8.5)
    ax.set_xlabel("km", fontsize=7)
    ax.set_ylabel("km", fontsize=7)
    ax.tick_params(labelsize=6.5)
axes.flat[-1].axis("off")
axes.flat[-1].legend(handles=[Patch(color="#D55E00", label="burned cells"),
                              Patch(facecolor="0.55", label="natural vegetation\n(shade = elevation)"),
                              Patch(facecolor="white", edgecolor="0.6", label="outside the population"),
                              Line2D([], [], color="#0072B2", ls="--", lw=0.8, label="5 km collar"),
                              Line2D([], [], color="#0072B2", lw=1.0, label="10 km collar"),
                              Line2D([], [], color="black", ls=":", lw=0.8, label="scar frame (2 km)")],
                     loc="center", frameon=False, fontsize=7.5)
fig.tight_layout()
for ext_ in ("png", "pdf"):
    fig.savefig(HERE / f"figS1_study_areas.{ext_}", dpi=300)
print("figS1 written")
