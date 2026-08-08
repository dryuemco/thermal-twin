#!/usr/bin/env python3
"""Figure 7 (main figure) - the contrast pairs (sufficiency counterexample).

Primary claim (titles): burned-niche overlap vs transfer verdict -
(a) Manavgat-Mugla, highest overlap (D-bar 0.83), both directions below chance;
(b) Bejis-Montiferru, lowest overlap (D-bar 0.48), both directions above chance.

Secondary, honest layer: per region-feature, arrowheads are FILLED where that
region's 95% CI excludes 0.5 (a supported direction) and OPEN where it does not.
The supported-agreement index is defined only on features filled in BOTH regions:
two in (a) (NDVI, Elevation), none in (b) - the two regions' supported sets do not
intersect - which is why pair (b) drops out of the supported-index sample. The
figure thereby shows the main claim and the index's limited coverage at once.

Okabe-Ito colours (no red-green), distinct in greyscale; minimum font 7 pt;
vector output (PDF + SVG). Data: paper/figure_contrast_pairs.json (sha256 in the
provenance sidecar). Hard asserts tie every headline number to 04_results 4.5.
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

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "figure_contrast_pairs.json"

COL_A = "#0072B2"  # Okabe-Ito blue  (first region of pair)
COL_B = "#E69F00"  # Okabe-Ito orange (second region)
SHADE = "#DBDBDB"  # sign-disagreement row shading
BAR = "#9A9A9A"    # Schoener D side bars

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
DBAR = "D̄"  # D with combining macron
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

MM = 1 / 25.4
FIG_W, FIG_H = 190 * MM, 112 * MM
plt.rcParams.update({
    "font.size": 8, "axes.labelsize": 8,
    "xtick.labelsize": 7.5, "ytick.labelsize": 8,
    "svg.fonttype": "none", "pdf.fonttype": 42,
})

fig = plt.figure(figsize=(FIG_W, FIG_H))
gs = fig.add_gridspec(
    1, 4, width_ratios=[1.0, 0.24, 1.0, 0.24],
    left=0.135, right=0.985, top=0.790, bottom=0.170, wspace=0.06,
)


def y_positions():
    ys, y = [], 0.0
    for i in range(len(FEATURE_ORDER)):
        ys.append(y)
        y -= 1.0
        if (i + 1) in GROUP_BREAKS:
            y -= 0.45
    return ys


def draw_panel(ax_main, ax_bar, pair, region_a, region_b, panel_tag,
               title, sub1, sub2, show_ylabels):
    ys = y_positions()
    per = pair["per_feature_signed_auc"]
    off = 0.185
    for (fkey, _), y in zip(FEATURE_ORDER, ys):
        rec = per[fkey]
        if not rec["sign_agrees"]:
            ax_main.axhspan(y - 0.5, y + 0.5, color=SHADE, zorder=0)
            ax_bar.axhspan(y - 0.5, y + 0.5, color=SHADE, zorder=0)
        for region, colour, dy in ((region_a, COL_A, +off), (region_b, COL_B, -off)):
            v = rec[region]
            auc, lo, hi = v["auc"], v["lo"], v["hi"]
            yline = y + dy
            ax_main.plot([lo, hi], [yline, yline], color=colour, lw=0.9,
                         solid_capstyle="butt", alpha=0.55, zorder=2)
            for cap in (lo, hi):
                ax_main.plot([cap, cap], [yline - 0.10, yline + 0.10],
                             color=colour, lw=0.9, alpha=0.55, zorder=2)
            style = "-|>" if supported(v) else "->"
            ax_main.add_patch(FancyArrowPatch(
                (0.5, yline), (auc, yline), arrowstyle=style,
                mutation_scale=7.5, lw=1.7, color=colour, zorder=3,
                shrinkA=0, shrinkB=0,
            ))
        ax_bar.barh(y, per[fkey]["schoener_d_this_feature"], height=0.62,
                    color=BAR, zorder=2)
    ax_main.axvline(0.5, color="black", lw=0.8, ls=(0, (4, 2)), zorder=1)
    ax_main.set_xlim(0.18, 0.82)
    ax_main.set_xticks([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    ax_main.set_ylim(ys[-1] - 0.75, ys[0] + 0.75)
    ax_main.set_yticks(ys)
    ax_main.set_yticklabels([f for _, f in FEATURE_ORDER] if show_ylabels else [])
    ax_main.set_xlabel("Signed AUC  P(x higher on burned cell)")
    ax_main.text(0.502, ys[0] + 0.72, "chance", fontsize=7,
                 ha="left", va="bottom", style="italic")
    ax_bar.set_xlim(0, 1)
    ax_bar.set_ylim(ax_main.get_ylim())
    ax_bar.set_yticks([])
    ax_bar.set_xticks([0, 0.5, 1])
    ax_bar.set_xticklabels(["0", "", "1"])
    ax_bar.set_xlabel("Schoener D", fontsize=7.5)
    for s in ("top", "right"):
        ax_main.spines[s].set_visible(False)
        ax_bar.spines[s].set_visible(False)
    ax_main.text(0, 1.240, f"({panel_tag}) " + title,
                 transform=ax_main.transAxes, fontsize=7.6, fontweight="bold",
                 va="bottom")
    ax_main.text(0, 1.148, sub1, transform=ax_main.transAxes, fontsize=7,
                 va="bottom")
    ax_main.text(0, 1.058, sub2, transform=ax_main.transAxes, fontsize=7,
                 va="bottom")
    # region legend: inside the axes' guaranteed-empty upper-left corner,
    # away from all title/caption text
    hA = Line2D([], [], color=COL_A, lw=3)
    hB = Line2D([], [], color=COL_B, lw=3)
    ax_main.legend([hA, hB], [REGION_LABEL[region_a], REGION_LABEL[region_b]],
                   loc="upper left", bbox_to_anchor=(0.005, 0.995),
                   frameon=False, fontsize=7, handlelength=1.1,
                   labelspacing=0.25, borderaxespad=0.0)


def transfer_sub(pair, a, b):
    t = pair["transfer"]
    d1, d2 = t[f"{a}_to_{b}"], t[f"{b}_to_{a}"]
    return (f"transfer {d1['auc']:.3f} [{d1['ci95'][0]:.3f}, {d1['ci95'][1]:.3f}] "
            f"and {d2['auc']:.3f} [{d2['ci95'][0]:.3f}, {d2['ci95'][1]:.3f}]")


axL = fig.add_subplot(gs[0, 0])
axLb = fig.add_subplot(gs[0, 1])
axR = fig.add_subplot(gs[0, 2])
axRb = fig.add_subplot(gs[0, 3])

nl = P_LEFT["niche_overlap"]
nr = P_RIGHT["niche_overlap"]
draw_panel(
    axL, axLb, P_LEFT, "manavgat_2021", "mugla_2021", "a",
    f"Manavgat{NDASH}Muğla: {DBAR} {nl['schoener_d_mean1d']:.2f}, "
    "below chance both ways",
    transfer_sub(P_LEFT, "manavgat_2021", "mugla_2021"),
    "jointly supported features: 2 (NDVI, Elevation)",
    show_ylabels=True,
)
draw_panel(
    axR, axRb, P_RIGHT, "bejis_2022", "montiferru_2021", "b",
    f"Bejís{NDASH}Montiferru: {DBAR} {nr['schoener_d_mean1d']:.2f}, "
    "above chance both ways",
    transfer_sub(P_RIGHT, "bejis_2022", "montiferru_2021"),
    "jointly supported: 0 — sets disjoint; Montiferru CIs wide",
    show_ylabels=False,
)

fig.text(0.135, 0.068,
         "Arrows: signed AUC from chance (0.5); whiskers: 95% ~5 km spatial-block "
         "bootstrap CI.  Shaded rows: signs disagree.",
         fontsize=7.0)
fig.text(0.135, 0.038,
         "Filled arrowhead: that region's CI excludes 0.5 (a supported direction); "
         "open arrowhead: it does not.",
         fontsize=7.0)
fig.text(0.135, 0.008,
         "The supported-agreement index uses only features filled in both regions "
         "— two in (a), none in (b).  Grey bars: Schoener's D.",
         fontsize=7.0)

out_pdf = HERE / "fig7_contrast_pairs.pdf"
out_svg = HERE / "fig7_contrast_pairs.svg"
fig.savefig(out_pdf)
fig.savefig(out_svg)
if "--preview" in sys.argv:
    fig.savefig(HERE / "fig7_contrast_pairs_preview.png", dpi=220)

(HERE / "fig7_provenance.json").write_text(json.dumps({
    "figure": "Fig. 7 - contrast pairs (main figure; sufficiency counterexample)",
    "script": "paper/figures/fig7_contrast_pairs.py",
    "source": {"path": "paper/figure_contrast_pairs.json", "sha256": sha},
    "outputs": ["fig7_contrast_pairs.pdf", "fig7_contrast_pairs.svg"],
    "asserts": ("D-bar means 0.826/0.479; jointly supported features exactly "
                "[NDVI, Elevation] in (a) and [] in (b); four transfer AUCs and "
                "CI-off-chance checks; enforced at build time"),
    "encoding": ("titles: overlap + transfer verdict primary; arrowhead fill = "
                 "per-region CI excludes 0.5; supported-index coverage limit "
                 "stated in caption"),
    "palette": "Okabe-Ito blue #0072B2 / orange #E69F00; greyscale-distinct; no red-green",
    "min_font_pt": 7.0,
    "environment": f"matplotlib {matplotlib.__version__}",
}, indent=1))
print(f"written {out_pdf.name}, {out_svg.name}; source sha256 {sha[:12]}...; "
      f"jointly supported a={JS_LEFT} b={JS_RIGHT}; all asserts passed")
