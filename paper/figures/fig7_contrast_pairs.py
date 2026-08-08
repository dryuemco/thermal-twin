#!/usr/bin/env python3
"""Figure 7 (main figure) - the contrast pairs (sufficiency counterexample).

Primary claim (panel headers): burned-niche overlap vs transfer verdict -
(a) Manavgat-Mugla, highest overlap (D-bar 0.83), both directions below chance;
(b) Bejis-Montiferru, lowest overlap (D-bar 0.48), both directions above chance.

Secondary, honest layer: per region-feature, arrowheads are FILLED where that
region's 95% CI excludes 0.5 (a supported direction) and OPEN where it does not.
The supported-agreement index is defined only on features filled in BOTH regions:
two in (a) (NDVI, Elevation), none in (b) - the two regions' supported sets do not
intersect - which is why pair (b) drops out of the supported-index sample. The
figure thereby shows the main claim and the index's limited coverage at once.

Data: paper/figure_contrast_pairs.json (sha256 in the provenance sidecar).
Hard asserts tie every headline number to 04_results 4.5.

2026-08-08 revision:
  - body 9 pt, minimum 8 pt (was 7 pt); canvas 190 x 102 mm (was 190 x 112);
  - THE TWO REGIONS no longer differ by hue alone. Okabe-Ito blue and orange
    are only ~2.30:1 apart in relative luminance, so in greyscale they nearly
    merge. The arrowhead-fill channel is already spoken for (it carries CI
    support and must not be touched), so the region is carried by LINE STYLE:
    solid for the first region of the pair, dashed for the second. Colour,
    line style and vertical offset now all encode it;
  - the chance reference is a segment over the data rows only, not an axvline,
    so it cannot run through the legend sitting in the reserved band below;
  - x ticks are set explicitly on both the arrow axes and the Schoener D side
    axes: matplotlib otherwise keeps a locator tick just outside the view whose
    label artist still has a position and collides as a phantom;
  - the three in-artwork footnotes moved to the caption (Elsevier sets the
    caption, and the caption must stand alone anyway).
"""
import hashlib
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _layout_check import check as layout_check, contrast_ratio, relative_luminance

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "figure_contrast_pairs.json"

COL_A = "#0072B2"  # Okabe-Ito blue  (first region of pair)
COL_B = "#E69F00"  # Okabe-Ito orange (second region)
STYLE_A, STYLE_B = "solid", (0, (3.0, 1.5))   # the non-colour region cue
SHADE = "#D6D6D6"  # sign-disagreement row shading (achromatic by design)
BAR = "#8F8F8F"    # Schoener D side bars

FS_BODY = 9.0
FS_SMALL = 8.0     # minimum in this figure

FEATURE_ORDER = [  # grouped: static / anomaly-referenced / absolute thermal
    ("ndvi_mean", "NDVI"),
    ("slope_mean", "Slope"),
    ("elevation_mean", "Elevation"),
    ("lst_anomaly_mean", "LST anomaly"),
    ("tvdi_difference_mean", "TVDI difference"),
    ("current_lst_mean", "Current LST"),
    ("current_tvdi_mean", "Current TVDI"),
    ("downscaled_lst_mean", "Downscaled LST"),
    ("fused_lst_mean", "Fused LST"),
]
GROUP_BREAKS = {3, 5}
REGION_LABEL = {
    "manavgat_2021": "Manavgat", "mugla_2021": "Muğla",
    "bejis_2022": "Bejís", "montiferru_2021": "Montiferru",
}
DBAR = "D̄"
NDASH = "–"

raw = SRC.read_bytes()
sha = hashlib.sha256(raw).hexdigest()
data = json.loads(raw)
pairs = {p["pair"]: p for p in data["pairs"]}
P_LEFT = pairs["manavgat_2021 ~ mugla_2021"]
P_RIGHT = pairs["bejis_2022 ~ montiferru_2021"]


def supported(v):
    return v["lo"] > 0.5 or v["hi"] < 0.5


def jointly_supported(pair, a, b):
    per = pair["per_feature_signed_auc"]
    return [k for k, _ in FEATURE_ORDER if supported(per[k][a]) and supported(per[k][b])]


JS_LEFT = jointly_supported(P_LEFT, "manavgat_2021", "mugla_2021")
JS_RIGHT = jointly_supported(P_RIGHT, "bejis_2022", "montiferru_2021")

# ---- hard asserts: figure must match the manuscript text ----
assert abs(P_LEFT["niche_overlap"]["schoener_d_mean1d"] - 0.826) < 5e-4
assert abs(P_RIGHT["niche_overlap"]["schoener_d_mean1d"] - 0.479) < 5e-4
assert JS_LEFT == ["ndvi_mean", "elevation_mean"], JS_LEFT
assert JS_RIGHT == [], JS_RIGHT
tl, tr = P_LEFT["transfer"], P_RIGHT["transfer"]
assert abs(tl["manavgat_2021_to_mugla_2021"]["auc"] - 0.4702) < 5e-4
assert abs(tl["mugla_2021_to_manavgat_2021"]["auc"] - 0.4010) < 5e-4
assert abs(tr["bejis_2022_to_montiferru_2021"]["auc"] - 0.5937) < 5e-4
assert abs(tr["montiferru_2021_to_bejis_2022"]["auc"] - 0.5483) < 5e-4
for direction, rec in {**tl, **tr}.items():
    lo, hi = rec["ci95"]
    assert hi < 0.5 or lo > 0.5, f"{direction} must be CI-supported off chance"

# the region cue must not rest on hue alone
HUE_CONTRAST = contrast_ratio((0x00 / 255, 0x72 / 255, 0xB2 / 255),
                              (0xE6 / 255, 0x9F / 255, 0x00 / 255))
assert STYLE_A != STYLE_B, "regions need a non-colour cue"
# the sign-disagreement shading is achromatic, so greyscale cannot weaken it;
# check it is nonetheless dark enough to read against white
SHADE_RGB = tuple(int(SHADE[i:i + 2], 16) / 255 for i in (1, 3, 5))
SHADE_CONTRAST = contrast_ratio(SHADE_RGB, (1.0, 1.0, 1.0))

MM = 1 / 25.4
FIG_W, FIG_H = 190 * MM, 102 * MM
plt.rcParams.update({
    "font.size": FS_SMALL, "axes.labelsize": FS_BODY,
    "xtick.labelsize": FS_SMALL, "ytick.labelsize": FS_BODY,
    "svg.fonttype": "none", "pdf.fonttype": 42,
})

fig = plt.figure(figsize=(FIG_W, FIG_H))
gs = fig.add_gridspec(
    1, 4, width_ratios=[1.0, 0.22, 1.0, 0.22],
    left=0.158, right=0.988, top=0.775, bottom=0.115, wspace=0.07,
)

data_artists = []


def y_positions():
    ys, y = [], 0.0
    for i in range(len(FEATURE_ORDER)):
        ys.append(y)
        y -= 1.0
        if (i + 1) in GROUP_BREAKS:
            y -= 0.45
    return ys


def draw_panel(ax_main, ax_bar, pair, region_a, region_b, panel_tag,
               header, line2, line3, line4, show_ylabels):
    ys = y_positions()
    per = pair["per_feature_signed_auc"]
    off = 0.20
    for (fkey, _), y in zip(FEATURE_ORDER, ys):
        rec = per[fkey]
        if not rec["sign_agrees"]:
            ax_main.axhspan(y - 0.5, y + 0.5, color=SHADE, zorder=0)
            ax_bar.axhspan(y - 0.5, y + 0.5, color=SHADE, zorder=0)
        for region, colour, style, dy in ((region_a, COL_A, STYLE_A, +off),
                                          (region_b, COL_B, STYLE_B, -off)):
            v = rec[region]
            auc, lo, hi = v["auc"], v["lo"], v["hi"]
            yline = y + dy
            w, = ax_main.plot([lo, hi], [yline, yline], color=colour, lw=0.9,
                              solid_capstyle="butt", alpha=0.6, zorder=2)
            data_artists.append((w, f"ci:{panel_tag}:{fkey}:{region}"))
            for cap in (lo, hi):
                ax_main.plot([cap, cap], [yline - 0.11, yline + 0.11],
                             color=colour, lw=0.9, alpha=0.6, zorder=2)
            head = "-|>" if supported(v) else "->"
            arr = FancyArrowPatch(
                (0.5, yline), (auc, yline), arrowstyle=head,
                mutation_scale=8, lw=1.7, color=colour, linestyle=style,
                zorder=3, shrinkA=0, shrinkB=0)
            ax_main.add_patch(arr)
        b = ax_bar.barh(y, per[fkey]["schoener_d_this_feature"], height=0.62,
                        color=BAR, zorder=2)
        data_artists.append((b[0], f"D:{panel_tag}:{fkey}"))

    # chance as a segment over the data rows only - an axvline would span the
    # reserved legend band below and cross the legend text
    ch, = ax_main.plot([0.5, 0.5], [ys[-1] - 0.6, ys[0] + 0.6], color="black",
                       lw=0.9, ls=(0, (4, 2)), zorder=1)
    data_artists.append((ch, f"chance:{panel_tag}"))

    ax_main.set_xlim(0.18, 0.82)
    ax_main.set_xticks([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    ax_main.set_ylim(ys[-1] - 2.6, ys[0] + 0.85)
    ax_main.set_yticks(ys)
    ax_main.set_yticklabels([f for _, f in FEATURE_ORDER] if show_ylabels else [])
    ax_main.set_xlabel("signed AUC: P(x higher on burned)", fontsize=FS_BODY)
    ax_bar.set_xlim(0, 1)
    ax_bar.set_ylim(ax_main.get_ylim())
    ax_bar.set_yticks([])
    ax_bar.set_xticks([0, 1])
    ax_bar.set_xticklabels(["0", "1"])
    ax_bar.set_xlabel("Schoener D", fontsize=FS_SMALL)
    for s in ("top", "right"):
        ax_main.spines[s].set_visible(False)
        ax_bar.spines[s].set_visible(False)

    ax_main.text(0, 1.255, f"({panel_tag}) {header}", transform=ax_main.transAxes,
                 fontsize=FS_BODY, fontweight="bold", va="bottom")
    for k, line in enumerate((line2, line3, line4)):
        ax_main.text(0, 1.175 - 0.080 * k, line, transform=ax_main.transAxes,
                     fontsize=FS_SMALL, va="bottom")

    hA = Line2D([], [], color=COL_A, lw=1.8, ls=STYLE_A)
    hB = Line2D([], [], color=COL_B, lw=1.8, ls=STYLE_B)
    ax_main.legend([hA, hB], [REGION_LABEL[region_a], REGION_LABEL[region_b]],
                   loc="lower left", bbox_to_anchor=(0.0, 0.0), ncol=2,
                   frameon=False, fontsize=FS_SMALL, handlelength=2.4,
                   columnspacing=1.8, handletextpad=0.6, borderpad=0.0)


axL = fig.add_subplot(gs[0, 0])
axLb = fig.add_subplot(gs[0, 1])
axR = fig.add_subplot(gs[0, 2])
axRb = fig.add_subplot(gs[0, 3])

nl = P_LEFT["niche_overlap"]
nr = P_RIGHT["niche_overlap"]
draw_panel(
    axL, axLb, P_LEFT, "manavgat_2021", "mugla_2021", "a",
    f"Manavgat{NDASH}Muğla",
    f"Schoener {DBAR} = {nl['schoener_d_mean1d']:.2f} — highest overlap",
    "transfer 0.470 / 0.401 — both below chance",
    f"jointly supported features: {len(JS_LEFT)} (NDVI, Elevation)",
    show_ylabels=True,
)
draw_panel(
    axR, axRb, P_RIGHT, "bejis_2022", "montiferru_2021", "b",
    f"Bejís{NDASH}Montiferru",
    f"Schoener {DBAR} = {nr['schoener_d_mean1d']:.2f} — lowest overlap",
    "transfer 0.594 / 0.548 — both above chance",
    f"jointly supported features: {len(JS_RIGHT)} — sets disjoint",
    show_ylabels=False,
)

print(f"[greyscale] region hue contrast {HUE_CONTRAST:.2f}:1 (weak) -> line style "
      f"carries the region; sign-disagreement shading is achromatic, "
      f"{SHADE_CONTRAST:.2f}:1 against white")

problems = layout_check(fig, "Fig. 7 - contrast pairs", min_gap_pt=2.0,
                        min_font_pt=8.0, data_artists=data_artists)

if "--preview" in sys.argv:
    png = HERE / "fig7_contrast_pairs_preview.png"
    fig.savefig(png, dpi=300)
    rgb = plt.imread(png)[:, :, :3]
    grey = (0.2126 * rgb[:, :, 0] + 0.7152 * rgb[:, :, 1] + 0.0722 * rgb[:, :, 2])
    plt.imsave(HERE / "fig7_contrast_pairs_greyscale.png", grey, cmap="gray",
               vmin=0.0, vmax=1.0)
fig.savefig(HERE / "fig7_contrast_pairs.svg")
try:
    fig.savefig(HERE / "fig7_contrast_pairs.pdf")
except PermissionError:
    raise SystemExit("fig7_contrast_pairs.pdf is locked - close it and re-run.")

(HERE / "fig7_provenance.json").write_text(json.dumps({
    "figure": "Fig. 7 - contrast pairs (main figure; sufficiency counterexample)",
    "script": "paper/figures/fig7_contrast_pairs.py",
    "source": {"path": "paper/figure_contrast_pairs.json", "sha256": sha},
    "outputs": ["fig7_contrast_pairs.pdf", "fig7_contrast_pairs.svg"],
    "asserts": ("D-bar means 0.826/0.479; jointly supported features exactly "
                "[NDVI, Elevation] in (a) and [] in (b); four transfer AUCs and "
                "CI-off-chance checks; region cue asserted non-colour; "
                "enforced at build time"),
    "encoding": ("panel headers: overlap + transfer verdict primary; arrowhead fill = "
                 "per-region CI excludes 0.5 (untouched); region = colour AND line "
                 "style AND vertical offset; supported-index coverage limit stated "
                 "in the header line and the caption"),
    "greyscale": {
        "region_hue_contrast": round(HUE_CONTRAST, 2),
        "note": "blue vs orange separate by only this ratio in greyscale, so the region is "
                "also carried by line style (solid = first region, dashed = second). The "
                "arrowhead-fill channel was left alone because it encodes CI support.",
        "shade_contrast_vs_white": round(SHADE_CONTRAST, 2),
        "shade_note": "the sign-disagreement row shading is achromatic, so a luminance "
                      "greyscale conversion leaves it unchanged by construction",
        "proof": "fig7_contrast_pairs_greyscale.png",
    },
    "palette": "Okabe-Ito blue #0072B2 / orange #E69F00; greyscale-distinct via line style; no red-green",
    "canvas_mm": [190, 102],
    "column": "double (190 mm)",
    "font_pt": {"body": FS_BODY, "minimum": FS_SMALL},
    "layout_check": f"paper/figures/_layout_check.py; {len(problems)} problems at build time; "
                    f"{len(data_artists)} data artists registered",
    "environment": f"matplotlib {matplotlib.__version__}",
}, indent=1, ensure_ascii=False))
print(f"fig7 written; source sha256 {sha[:12]}...; "
      f"jointly supported a={JS_LEFT} b={JS_RIGHT}; all asserts passed")
