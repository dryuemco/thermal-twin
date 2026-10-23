"""Shared look of the manuscript figures (2026-10-23 redraw).

One accent colour, grey for context, no gridlines, no boxes around labels, no explanatory text
inside the plot area; the caption carries the explanation. Colours are Okabe-Ito blue and
vermillion, which pass the CVD, normal-vision and 3:1 contrast checks of the dataviz validator
as a pair (worst CVD ΔE 21.9, normal-vision ΔE 31.2). Grey is used only for context (baseline,
reference lines), always with a second cue (open marker or a direct label).
"""
import matplotlib.pyplot as plt

MM = 1 / 25.4
WIDTH_MM = 170.0          # SpringerOpen full page width (85 mm half width, 225 mm maximum height)
BLUE = "#0072B2"          # thermal set; first region of a pair; above chance
VERMILLION = "#D55E00"    # second region of a pair; below chance
GREY = "#8C8C8C"          # baseline set, context marks
RULE = "#BDBDBD"          # chance and other reference lines
INK = "#222222"
MUTED = "#555555"
FS_BODY = 9.0
FS_SMALL = 8.0            # the minimum size in every figure


def apply():
    plt.rcParams.update({
        "svg.fonttype": "none", "pdf.fonttype": 42,
        "font.size": FS_BODY, "axes.labelsize": FS_BODY, "axes.titlesize": FS_BODY,
        "xtick.labelsize": FS_SMALL, "ytick.labelsize": FS_SMALL, "legend.fontsize": FS_SMALL,
        "axes.edgecolor": MUTED, "axes.linewidth": 0.6, "axes.labelcolor": INK, "text.color": INK,
        "xtick.color": MUTED, "ytick.color": MUTED, "xtick.labelcolor": INK, "ytick.labelcolor": INK,
        "xtick.major.width": 0.6, "ytick.major.width": 0.6, "xtick.major.size": 3.0,
        "ytick.major.size": 3.0, "axes.spines.top": False, "axes.spines.right": False,
        "axes.titlelocation": "left", "legend.frameon": False,
    })


def chance(ax, at=0.5, axis="x"):
    """A thin solid reference line at chance, drawn under the data."""
    line = ax.axvline if axis == "x" else ax.axhline
    return line(at, color=RULE, lw=0.8, zorder=0)


def save(fig, here, stem):
    """PDF and SVG always; with --preview also the 300 dpi PNG and its luminance proof."""
    import sys
    fig.savefig(here / f"{stem}.pdf")
    fig.savefig(here / f"{stem}.svg")
    if "--preview" in sys.argv:
        png = here / f"{stem}_preview.png"
        fig.savefig(png, dpi=300)
        rgb = plt.imread(png)[:, :, :3]
        grey = 0.2126 * rgb[:, :, 0] + 0.7152 * rgb[:, :, 1] + 0.0722 * rgb[:, :, 2]
        plt.imsave(here / f"{stem}_greyscale.png", grey, cmap="gray", vmin=0.0, vmax=1.0)
