"""IJWF (CSIRO Publishing) look of the manuscript figures.

The shared style, paper/figures/_style.py, is loaded as it is and is not edited. Only what the
publisher's figure guide asks for is changed here (template/Tables-and-figures.pdf, pages 2 to 5):

  Fonts   axis labels, panel titles and part labels 8 pt (the guide's maximum); tick labels, legends
          and data labels 7 pt; nothing below 5 pt. The shared style has 9 pt and 8 pt.
  Graphs  one x and one y axis line of about 1.0 pt and not below 0.7 pt. The shared style has 0.6 pt.
  Files   save() writes the PDF, the SVG and the 300 dpi preview PNG, always, and only into this folder.

Colours, the chance line and everything else come from the shared module. The IJWF copies of the
figure scripts import this module in place of _style.
"""
import importlib.util
import sys
from pathlib import Path

import matplotlib.pyplot as plt

sys.dont_write_bytecode = True                      # no __pycache__ entry is written into paper/figures

OUT = Path(__file__).resolve().parent               # paper/submissions/ijwf/figures, the only folder written
SHARED = OUT.parents[2] / "figures"                 # paper/figures, read only

_spec = importlib.util.spec_from_file_location("_style_shared_for_ijwf", SHARED / "_style.py")
_shared = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_shared)
_shared.FS_BODY = 8.0                               # apply() of the shared module reads these two at call time
_shared.FS_SMALL = 7.0

MM, WIDTH_MM = _shared.MM, _shared.WIDTH_MM
BLUE, VERMILLION, GREY, RULE, INK, MUTED = (_shared.BLUE, _shared.VERMILLION, _shared.GREY, _shared.RULE,
                                            _shared.INK, _shared.MUTED)
FS_BODY, FS_SMALL = _shared.FS_BODY, _shared.FS_SMALL
FS_FLOOR = 5.0                                      # the guide's absolute minimum
AXIS_LW = 0.8                                       # axis lines and ticks, pt
chance = _shared.chance


def apply():
    _shared.apply()
    plt.rcParams.update({"font.family": "sans-serif", "axes.grid": False, "axes.linewidth": AXIS_LW,
                         "xtick.major.width": AXIS_LW, "ytick.major.width": AXIS_LW})


def font_sizes(fig):
    """Sizes (pt) of every visible text of the drawn figure, sorted. Stops if one is outside the guide."""
    from _layout_check import _cartopy_gridline_texts, _walk_texts   # the walk of the shared layout check
    fig.canvas.draw()
    texts, seen = [], set()
    _walk_texts(fig, texts, seen)
    _cartopy_gridline_texts(fig, texts, seen)
    sizes = sorted({round(float(t.get_fontsize()), 2) for t in texts})
    bad = [(t.get_text(), t.get_fontsize()) for t in texts
           if not FS_SMALL - 1e-6 <= t.get_fontsize() <= FS_BODY + 1e-6]
    assert not bad and sizes[0] >= FS_FLOOR, f"text outside {FS_SMALL} to {FS_BODY} pt: {bad[:5]}"
    assert all("&" not in t.get_text() for t in texts), "the guide wants 'and', not '&'"
    return sizes


def save(fig, here, stem):
    """PDF, SVG and the 300 dpi preview PNG, always, and only into the IJWF figures folder."""
    here = Path(here).resolve()
    assert here == OUT, f"the IJWF figures are written to {OUT} only, not to {here}"
    fig.savefig(here / f"{stem}.pdf")
    fig.savefig(here / f"{stem}.svg")
    fig.savefig(here / f"{stem}_preview.png", dpi=300)
