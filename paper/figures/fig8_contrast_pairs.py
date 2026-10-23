#!/usr/bin/env python3
"""Figure 8 - the contrast pairs (2026-10-23 redraw).

(a) Manavgat and Muğla, the most similar pair (highest niche overlap), whose transfer is below
chance in both directions; (b) Bejís and Montiferru, the least similar pair, whose transfer is
above chance in both directions. For each of the nine numeric predictors, a dot per region at
its signed univariate AUC with its 95% spatial-block interval; the dot is filled where the
interval excludes 0.5 and open where it does not. First region blue, second near-black, with a
small vertical offset as a second cue (vermillion is kept for "below chance" in Fig. 4).

The earlier version (arrows from 0.5, open/filled arrowheads, dashed second region, shaded
disagreement rows, Schoener D side bars and three header lines per panel) is in the git history
before 2026-10-23; the per-feature D values are in Table S7.

Data: paper/labelfix_rerun/round5/out_official/figure_contrast_pairs.json, the corrected
Manavgat label. Hard asserts tie every headline number to the abstract, Section S3.4 and round5/s7.
"""
import hashlib
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _layout_check import check as layout_check, assert_inside
import _style as S

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "labelfix_rerun" / "round5" / "out_official" / "figure_contrast_pairs.json"
S7 = HERE.parent / "labelfix_rerun" / "round5" / "s7_contrast_pair.json"


FEATURE_ORDER = [  # grouped: static / anomaly-referenced / absolute thermal
    ("ndvi_mean", "NDVI"),
    ("slope_mean", "slope"),
    ("elevation_mean", "elevation"),
    ("lst_anomaly_mean", "LST anomaly"),
    ("tvdi_difference_mean", "TVDI difference"),
    ("current_lst_mean", "current LST"),
    ("current_tvdi_mean", "current TVDI"),
    ("downscaled_lst_mean", "downscaled LST"),
    ("fused_lst_mean", "fused LST"),
]
GROUP_BREAKS = {3, 5}
REGION_LABEL = {
    "manavgat_2021": "Manavgat", "mugla_2021": "Muğla",
    "bejis_2022": "Bejís", "montiferru_2021": "Montiferru",
}
DBAR = "D̄"
NDASH = " and "

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
assert data["meta"]["parquet_sha256_prefixes"]["manavgat_2021"] != "054a1961", "frozen-label file"
assert abs(P_LEFT["niche_overlap"]["schoener_d_mean1d"] - 0.799) < 5e-4
assert abs(P_RIGHT["niche_overlap"]["schoener_d_mean1d"] - 0.479) < 5e-4
assert JS_LEFT == ["slope_mean", "elevation_mean", "current_lst_mean", "current_tvdi_mean",
                   "downscaled_lst_mean", "fused_lst_mean"], JS_LEFT
assert JS_RIGHT == [], JS_RIGHT
assert not any(P_LEFT["per_feature_signed_auc"][k]["sign_agrees"] for k in JS_LEFT)
AGREE_LEFT = sum(P_LEFT["per_feature_signed_auc"][k]["sign_agrees"] for k, _ in FEATURE_ORDER)
AGREE_RIGHT = sum(P_RIGHT["per_feature_signed_auc"][k]["sign_agrees"] for k, _ in FEATURE_ORDER)
assert (AGREE_LEFT, AGREE_RIGHT) == (2, 7), (AGREE_LEFT, AGREE_RIGHT)
tl, tr = P_LEFT["transfer"], P_RIGHT["transfer"]
assert abs(tl["manavgat_2021_to_mugla_2021"]["auc"] - 0.438) < 5e-4    # abstract
assert abs(tl["mugla_2021_to_manavgat_2021"]["auc"] - 0.345) < 5e-4    # abstract
assert abs(tr["bejis_2022_to_montiferru_2021"]["auc"] - 0.5937) < 5e-4
assert abs(tr["montiferru_2021_to_bejis_2022"]["auc"] - 0.5483) < 5e-4
for direction, rec in {**tl, **tr}.items():
    lo, hi = rec["ci95"]
    assert hi < 0.5 or lo > 0.5, f"{direction} must be CI-supported off chance (2-cell)"
# the caption's 5 km statement: only Mugla -> Manavgat keeps support at 10-cell blocking
V10 = {d: r["v10"] for d, r in json.loads(S7.read_text(encoding="utf-8"))["official"]["transfer"].items()}
assert V10 == {"manavgat_2021_to_mugla_2021": "uncertain", "mugla_2021_to_manavgat_2021": "below",
               "bejis_2022_to_montiferru_2021": "uncertain",
               "montiferru_2021_to_bejis_2022": "uncertain"}, V10

# ---- Appendix D Table B10 and Appendix A(s): bound to this figure's source and to Table 4's --
# (2026-09-23) Every B10 cell is asserted at the printed 3 dp: D-bar, per-feature D and as-drawn
# transfer against figure_contrast_pairs.json (this figure's source); collar transfer, collar
# ranks and the A(s) collar extremes against round5/collar/aoi_frame_transfer.csv (Table 4's
# source, regen_transfer_ci.py); the AoA shares against round5/collar/aoa_directed_pair_summary.csv.
import pandas as _pd
_COL = HERE.parent / "labelfix_rerun" / "round5" / "collar"
_ct = _pd.read_csv(_COL / "aoi_frame_transfer.csv")
_ct = _ct[(_ct.source_frame == "10km") & (_ct.target_frame == "10km")].sort_values("thermal").reset_index(drop=True)
assert len(_ct) == 20 and f"{_ct.thermal.mean():.3f}" == "0.589"          # Table 4, 10 km / 10 km
_cv = {r.direction: (r.thermal, r.thermal_ci_lo, r.thermal_ci_hi, i + 1) for i, r in _ct.iterrows()}
_aoa = _pd.read_csv(_COL / "aoa_directed_pair_summary.csv").set_index("direction")["fraction_inside_weighted_aoa"]
_fd = lambda p: sorted(p["per_feature_signed_auc"][k]["schoener_d_this_feature"] for k, _ in FEATURE_ORDER)
_ord = lambda n: f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"
MM_, MG_, BM_, MB_ = ("manavgat_2021_to_mugla_2021", "mugla_2021_to_manavgat_2021",
                      "bejis_2022_to_montiferru_2021", "montiferru_2021_to_bejis_2022")
B10_EXPECTED = [
    f"| Schoener's *D*, mean 1-D | **{P_LEFT['niche_overlap']['schoener_d_mean1d']:.3f}** (highest) | "
    f"**{P_RIGHT['niche_overlap']['schoener_d_mean1d']:.3f}** (lowest) |",
    f"| per-feature *D* | {_fd(P_LEFT)[0]:.2f} to {_fd(P_LEFT)[-1]:.2f} | {_fd(P_RIGHT)[0]:.2f} to {_fd(P_RIGHT)[-1]:.2f} |",
    f"| transfer, frames as drawn | {tl[MM_]['auc']:.3f}, {tl[MG_]['auc']:.3f} | {tr[BM_]['auc']:.3f}, {tr[MB_]['auc']:.3f} |",
    f"| transfer, 10 km collar | {_cv[MM_][0]:.3f}, {_cv[MG_][0]:.3f} | {_cv[BM_][0]:.3f}, {_cv[MB_][0]:.3f} |",
    f"| rank of 20 on the collar, from the bottom | {_ord(_cv[MM_][3])}, {_ord(_cv[MG_][3])} | "
    f"{_ord(_cv[BM_][3])}, {_ord(_cv[MB_][3])} |",
    f"| target cells inside the AoA | {_aoa[MM_]:.3f}, {_aoa[MG_]:.3f} | n/a |",
]
_supp = (HERE.parent / "supplementary.md").read_text(encoding="utf-8")
for _row in B10_EXPECTED:
    assert _row in _supp, f"Table B10 row not as computed: {_row}"
_as = " ".join(_supp[_supp.index("## S3.4 "):_supp.index("## S3.5 ")].split())   # former A(s)
_lo, _hi = _ct.iloc[0], _ct.iloc[-1]
for _s in (f"{tl[MM_]['auc']:.3f} and {tl[MG_]['auc']:.3f} as drawn",
           f"{_cv[MM_][0]:.3f} and {_cv[MG_][0]:.3f} under the collar",
           f"[{_cv[MG_][1]:.3f}, {_cv[MG_][2]:.3f}], excludes chance",
           f"Manavgat to Bejís at {_lo.thermal:.3f}", f"Muğla to Evia at {_hi.thermal:.3f}",
           f"seven of nine feature-response directions point opposite ways",
           f"all six features supported in both regions have opposite signs"):
    assert _s in _as, f"A(s) does not state: {_s}"
assert _lo.direction == "manavgat_2021_to_bejis_2022" and _hi.direction == "mugla_2021_to_evia_2021_extended"
assert _cv[MG_][2] < 0.5 < _cv[MM_][2]          # only Mugla -> Manavgat excludes chance on the collar
assert 9 - AGREE_LEFT == 7 and len(JS_LEFT) == 6

# x range: every CI must lie inside it (Manavgat elevation reaches 0.179 on the corrected label)
XLIM = (0.15, 0.82)
for p_ in (P_LEFT, P_RIGHT):
    for fk, _ in FEATURE_ORDER:
        for rk, v in p_["per_feature_signed_auc"][fk].items():
            if isinstance(v, dict):
                assert XLIM[0] < v["lo"] and v["hi"] < XLIM[1], (fk, rk, v)

S.apply()
fig, (axL, axR) = plt.subplots(1, 2, figsize=(S.WIDTH_MM * S.MM, 96 * S.MM), sharey=True)
data_artists = []


def y_positions():
    ys, y = [], 0.0
    for i in range(len(FEATURE_ORDER)):
        ys.append(y)
        y -= 1.0
        if (i + 1) in GROUP_BREAKS:
            y -= 0.45
    return ys


YS = y_positions()


def draw_panel(ax, pair, region_a, region_b, tag, title, subtitle):
    per = pair["per_feature_signed_auc"]
    S.chance(ax)
    for (fkey, _), y in zip(FEATURE_ORDER, YS):
        for region, colour, dy in ((region_a, S.BLUE, +0.16), (region_b, S.INK, -0.16)):
            v = per[fkey][region]
            ci, = ax.plot([v["lo"], v["hi"]], [y + dy, y + dy], color=colour, lw=1.0, zorder=2)
            pt, = ax.plot(v["auc"], y + dy, marker="o", ms=5.0, lw=0, mec=colour, mew=1.1,
                          mfc=colour if supported(v) else "white", zorder=3)
            data_artists.extend([(ci, f"ci:{tag}:{fkey}:{region}"), (pt, f"auc:{tag}:{fkey}:{region}")])
    ax.set_title(f"({tag}) {title}, {subtitle}", fontsize=S.FS_BODY)
    ax.set_xlim(XLIM)
    ax.set_xticks([0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8])
    handles = [Line2D([], [], marker="o", ms=5.0, color=S.BLUE, lw=1.0),
               Line2D([], [], marker="o", ms=5.0, color=S.INK, lw=1.0)]
    ax.legend(handles, [REGION_LABEL[region_a], REGION_LABEL[region_b]], loc="lower left",
              bbox_to_anchor=(0.0, -0.02), handletextpad=0.4, labelspacing=0.3)
    assert_inside(ax, f"Fig. 8{tag}", xs=[per[f][r][k] for f, _ in FEATURE_ORDER
                                          for r in (region_a, region_b) for k in ("lo", "auc", "hi")])


nl, nr = P_LEFT["niche_overlap"], P_RIGHT["niche_overlap"]
draw_panel(axL, P_LEFT, "manavgat_2021", "mugla_2021", "a", "Most similar pair",
           f"D̄ = {nl['schoener_d_mean1d']:.2f}")
draw_panel(axR, P_RIGHT, "bejis_2022", "montiferru_2021", "b", "Least similar pair",
           f"D̄ = {nr['schoener_d_mean1d']:.2f}")
# filled/open key in the empty lower right of panel (b); the region legend stays at lower left
axR.add_artist(axR.get_legend())
fill_key = [Line2D([], [], marker="o", ms=5.0, lw=0, mec=S.INK, mew=1.1, mfc=S.INK),
            Line2D([], [], marker="o", ms=5.0, lw=0, mec=S.INK, mew=1.1, mfc="white")]
axR.legend(fill_key, ["excludes 0.5", "includes 0.5"], title="95% interval", loc="lower right",
           bbox_to_anchor=(1.0, -0.02), handletextpad=0.4, labelspacing=0.3, alignment="left",
           title_fontsize=S.FS_SMALL)
axL.set_yticks(YS, [f for _, f in FEATURE_ORDER])
axL.set_ylim(YS[-1] - 2.0, YS[0] + 0.6)
axL.tick_params(axis="y", length=0)
for ax in (axL, axR):
    ax.spines["left"].set_visible(False)
axR.tick_params(axis="y", left=False)
fig.supxlabel("signed AUC (above 0.5: higher on burned cells)", fontsize=S.FS_BODY, y=0.015)
fig.subplots_adjust(left=0.15, right=0.985, top=0.93, bottom=0.13, wspace=0.08)

problems = layout_check(fig, "Fig. 8 - contrast pairs", min_gap_pt=2.0, min_font_pt=8.0,
                        data_artists=data_artists)
S.save(fig, HERE, "fig8_contrast_pairs")

(HERE / "fig8_provenance.json").write_text(json.dumps({
    "figure": "Fig. 8 - contrast pairs",
    "script": "paper/figures/fig8_contrast_pairs.py",
    "source": {"path": "paper/labelfix_rerun/round5/out_official/figure_contrast_pairs.json", "sha256": sha},
    "asserts": ("corrected-label source (Manavgat parquet prefix is not the frozen 054a1961); "
                "D-bar means 0.799/0.479; jointly supported features exactly the six "
                "[slope, elevation, current LST, current TVDI, downscaled LST, fused LST] in (a), "
                "all opposite in sign, and [] in (b); sign agreement 2/9 and 7/9; four transfer "
                "AUCs (0.438, 0.345 from the abstract; 0.594, 0.548) and 2-cell CI-off-chance "
                "checks; 10-cell verdicts from round5/s7 (only Mugla->Manavgat supported); Table S7 "
                "rows and Section S3.4 statements; every plotted value inside the axes"),
    "s7": {"path": "paper/labelfix_rerun/round5/s7_contrast_pair.json",
           "sha256": hashlib.sha256(S7.read_bytes()).hexdigest()},
    "design": "2026-10-23 redraw: dot + interval per region and feature, filled = interval excludes 0.5; "
              "region = colour and vertical offset; no arrows, shading or side bars",
    "canvas_mm": [S.WIDTH_MM, 96],
    "font_pt": {"body": S.FS_BODY, "minimum": S.FS_SMALL},
    "layout_check": f"paper/figures/_layout_check.py; {len(problems)} problems at build time",
    "environment": f"matplotlib {matplotlib.__version__}",
}, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"fig8 written; source sha256 {sha[:12]}...; jointly supported a={JS_LEFT} b={JS_RIGHT}; all asserts passed")
