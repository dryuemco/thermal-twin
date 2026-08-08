#!/usr/bin/env python3
"""Shared data, asserts and styling for Figures 5, 6 and 7.

These three figures were originally one three-panel figure. Panel (a) needs the full column
width for its 12 direction labels, which squeezed the other two; split into
three separate figures each gets the full width and nothing is crowded.

The asserts live here so all three figures fail if the underlying numbers move,
exactly as they did when this was one script.
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "data" / "fig_data.json").read_text())

decomp = DATA["fig6_decomp"]
loro = DATA["fig6_loro"]
fdrop = {r["config"]: r for r in DATA["fig6_fdrop"]}

BLUE, ORANGE, GREY = "#0072B2", "#E69F00", "#666666"
FS_BODY = 9.0
FS_TICK = 8.0     # minimum across all three figures
MM = 1 / 25.4

LABEL = {"manavgat_2021": "Manavgat", "bejis_2022": "Bejís", "mugla_2021": "Muğla",
         "evia_2021_extended": "Evia", "montiferru_2021": "Montiferru"}

# recovery vs negative recovery must differ by more than hue: Okabe-Ito blue and
# orange are only ~2.3:1 apart in relative luminance, so they barely separate in
# greyscale print
RECOVERY_STYLE, NEGATIVE_STYLE = "solid", (0, (3.2, 1.6))


def dirlabel(d):
    s, t = d.split("_to_")
    return f"{LABEL[s]}→{LABEL[t]}"


# ---- asserts vs 04_results 4.3/4.6 -----------------------------------------
neg = [d for d in decomp if d["best_adapted"] < d["raw"]]
assert len(neg) == 7, f"expected 7 negative-recovery directions, got {len(neg)}"
_worst = min(decomp, key=lambda d: d["recovered_fraction"])
assert _worst["direction"] == "evia_2021_extended_to_manavgat_2021"
assert abs(_worst["recovered_fraction"] - (-0.8619)) < 5e-3
_by_t = {r["target"]: r for r in loro}
assert abs(_by_t["manavgat_2021"]["loro_raw"] - 0.469) < 5e-3
for _r in loro:
    assert _r["loro_raw"] < _r["best_pairwise"], \
        f"LORO must not beat best pairwise: {_r['target']}"
assert abs(fdrop["full"]["mean_within"] - 0.888) < 5e-3
assert abs(fdrop["full"]["mean_transfer"] - 0.541) < 5e-3
assert abs(fdrop["drop_both"]["mean_within"] - 0.807) < 5e-3
assert abs(fdrop["drop_both"]["mean_transfer"] - 0.556) < 5e-3


def style_axes(ax):
    ax.tick_params(labelsize=FS_TICK)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def chance_segment(ax, y0, y1):
    """Chance reference over the data rows only.

    Deliberately not axvline: an axvline spans the whole axes including any
    reserved legend band, and would run straight through the legend text.
    """
    ln, = ax.plot([0.5, 0.5], [y0, y1], color="black", lw=0.9, ls=(0, (4, 2)),
                  zorder=1)
    return ln


def save(fig, stem, preview):
    """Write preview + greyscale proof + SVG, then PDF last.

    PDF last so that a PDF left open in a viewer (which locks the file on
    Windows) still leaves the inspectable outputs on disk.
    """
    if preview:
        png = HERE / f"{stem}_preview.png"
        fig.savefig(png, dpi=300)
        rgb = plt.imread(png)[:, :, :3]
        grey = (0.2126 * rgb[:, :, 0] + 0.7152 * rgb[:, :, 1]
                + 0.0722 * rgb[:, :, 2])
        plt.imsave(HERE / f"{stem}_greyscale.png", grey, cmap="gray",
                   vmin=0.0, vmax=1.0)
    fig.savefig(HERE / f"{stem}.svg")
    try:
        fig.savefig(HERE / f"{stem}.pdf")
    except PermissionError:
        raise SystemExit(f"{stem}.pdf is locked - close it in your PDF viewer "
                         f"and re-run. PNG/SVG were written.")
