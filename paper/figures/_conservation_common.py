#!/usr/bin/env python3
"""Shared data, asserts and styling for Figures 5, 6 and 7.

These three figures were originally one three-panel figure. Panel (a) needs the full column
width for its 12 direction labels, which squeezed the other two; split into
three separate figures each gets the full width and nothing is crowded.

The asserts live here so all three figures fail if the underlying numbers move,
exactly as they did when this was one script.
"""
import json
import re
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
# 2026-09-23: corrected Manavgat label (extract_fig_data.mjs on the official overlay)
DATA_PATH = HERE / "data" / "fig_data_corrected.json"
DATA = json.loads(DATA_PATH.read_text())

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


# ---- asserts (corrected label), zero tolerance at the printed 3 dp -----------
# Fig. 5: every arrow against Table B9 as printed, every within tick against Table 1
B9_NAME = {"Manavgat": "manavgat_2021", "Bejís": "bejis_2022", "Muğla": "mugla_2021",
           "Evia": "evia_2021_extended", "Montiferru": "montiferru_2021"}
_md = (HERE.parent / "A2_diagnostics.md").read_text(encoding="utf-8")
_md = _md[_md.index("**Table B9."):]
B9 = {f"{B9_NAME[s]}_to_{B9_NAME[t]}": {"raw": r, "zscore": z, "coral": c}
      for s, t, r, z, c in re.findall(
          r"^\| (\w+)→(\w+) \| ([0-9.]+) \[[^]]*\] \| ([0-9.]+) \[[^]]*\] \| ([0-9.]+) \[[^]]*\] \|$",
          _md, flags=re.M)}
assert len(B9) == 20
TABLE1_BLOCK2_THERMAL = {"manavgat_2021": "0.908", "bejis_2022": "0.918", "mugla_2021": "0.859",
                         "evia_2021_extended": "0.912"}
assert len(decomp) == 12
for _d in decomp:
    _b = B9[_d["direction"]]
    assert f"{_d['raw']:.3f}" == _b["raw"], (_d["direction"], _d["raw"], _b)
    _best = "zscore" if _d["best_method"] == "regionwise_zscore" else "coral"
    assert f"{_d['best_adapted']:.3f}" == _b[_best], (_d["direction"], _d["best_adapted"], _b)
    # same number read from two serialisations (decomposition CSV, step10 JSON): equal to 1e-12
    assert abs(_d["best_adapted"] - max(DATA["fig5"][_d["direction"]]["zscore"],
                                         DATA["fig5"][_d["direction"]]["coral"])) < 1e-12
    assert f"{_d['within']:.3f}" == TABLE1_BLOCK2_THERMAL[_d["direction"].split("_to_")[1]]
neg = [d for d in decomp if d["best_adapted"] < d["raw"]]
assert len(neg) == 7, f"expected 7 negative-recovery directions, got {len(neg)}"
assert all((d["recovered_fraction"] < 0) == (d in neg) for d in decomp)
_worst = min(decomp, key=lambda d: d["recovered_fraction"])
assert _worst["direction"] == "evia_2021_extended_to_manavgat_2021"
assert f"{_worst['recovered_fraction']:.3f}" == "-1.126", _worst["recovered_fraction"]
# compression toward chance: 11 of 12 move closer to 0.5; the exception is Manavgat -> Muğla
AWAY = [d["direction"] for d in decomp if abs(d["best_adapted"] - 0.5) >= abs(d["raw"] - 0.5)]
assert AWAY == ["manavgat_2021_to_mugla_2021"], AWAY
# Bejís -> Manavgat: the better method (CORAL) recovers; the z-score arm alone moves below chance
_bm = next(d for d in decomp if d["direction"] == "bejis_2022_to_manavgat_2021")
assert _bm["best_method"] == "coral_after_regionwise_zscore" and _bm["best_adapted"] > _bm["raw"]
assert B9["bejis_2022_to_manavgat_2021"]["zscore"] == "0.302"
# Fig. 6: LORO against A(n)(a) and the Fig. 6 caption
_by_t = {r["target"]: r for r in loro}
assert f"{_by_t['manavgat_2021']['loro_raw']:.3f}" == "0.426"
assert f"{_by_t['bejis_2022']['loro_raw']:.3f}" == "0.458"
assert f"{_by_t['evia_2021_extended']['loro_raw']:.3f}" == "0.715"
assert [r["target"] for r in loro if r["loro_raw"] > r["best_pairwise"]] == ["evia_2021_extended"], \
    "pooling beats the best single source for Evia only (A(n)(a))"
# Fig. 7: the four configurations as printed in A(n)
for _cfg, _w, _tr in (("full", "0.896", "0.527"), ("drop_elev", "0.840", "0.533"),
                      ("drop_anom", "0.883", "0.529"), ("drop_both", "0.820", "0.541")):
    assert f"{fdrop[_cfg]['mean_within']:.3f}" == _w and f"{fdrop[_cfg]['mean_transfer']:.3f}" == _tr, \
        (_cfg, fdrop[_cfg])


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
