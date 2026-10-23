#!/usr/bin/env python3
"""Fig. S1 - the within-region thermal gain under every check (Additional file 1, 2026-10-23).

One panel per region, one row per check. Each row compares the check (filled dot) with the
reference it was run against (open dot): most checks against the 5 km-blocked gain, the coordinate
and classifier checks against the 1 km-blocked gain of the random forest, and the window closures
against the pipeline's own window diagnostic. Whiskers are 95% block-bootstrap intervals where the
source gives one. This figure replaces the prose of former Sections S1.4, S1.7, S1.17 and S3.1.1
and the within-region rows of former Tables S21, S24, S25 and S35.

Data, all under paper/labelfix_rerun/: inference/ladder_summary.json (reference and collars),
round8/r8m_summary.json (VNP64A1), round8/r8j_summary.json (WorldCover 2020),
round8/r8n_summary.json (aspect), labels/r2_history.json (earlier burning),
round8/r8b_summary.json (Bejís pre-label cells), round3/no_coord_channels.json,
code/model_capacity.json and exports/window_closure_<region>/ (thermal_contributions.csv).
"""
import csv
import hashlib
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from _layout_check import check as layout_check, assert_inside
import _style as S

LR = HERE.parent / "labelfix_rerun"
REG = ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended", "montiferru_2021"]
NAME = {"manavgat_2021": "Manavgat", "bejis_2022": "Bejís", "mugla_2021": "Muğla",
        "evia_2021_extended": "North Evia", "montiferru_2021": "Montiferru"}
SHORT = {"manavgat_2021": "Manavgat", "bejis_2022": "Bejis", "mugla_2021": "Mugla",
         "evia_2021_extended": "Evia", "montiferru_2021": "Montiferru"}
load = lambda p: json.loads((LR / p).read_text(encoding="utf-8"))
SOURCES = ["inference/ladder_summary.json", "round8/r8m_summary.json", "round8/r8j_summary.json",
           "round8/r8n_summary.json", "labels/r2_history.json", "round8/r8b_summary.json",
           "round3/no_coord_channels.json", "code/model_capacity.json"]
ladder, r8m, r8j, r8n, r2, r8b, ncc, cap = (load(p) for p in SOURCES)


def window(region):
    sub = "compare/tables" if region == "manavgat_2021" else "tables"
    p = LR / "exports" / f"window_closure_{region}" / sub / "thermal_contributions.csv"
    SOURCES.append(str(p.relative_to(LR)).replace("\\", "/"))
    return {r["variant_id"]: float(r["contribution_delta"])
            for r in csv.DictReader(p.open(encoding="utf-8")) if r["metric"] == "roc_auc"}


# ---- references: the 5 km-blocked gain is stored in five outputs, which must agree ----
lad = ladder["ladder_by_frame"]
REF5 = {r: r8n[r]["without_aspect"]["gain"] for r in REG}
for r in REG:
    for other in (r8m["regions"][r]["within_mcd"]["gain"], r8j["regions"][r]["within_2021"]["gain"],
                  r2["within_B10"][r]["reference"]["delta"]):
        assert abs(other - REF5[r]) < 1e-9, (r, other, REF5[r])
    assert abs(lad["full"]["blocked_B10"]["per_region"][SHORT[r]] - REF5[r]) < 5e-5, r
assert [f"{REF5[r]:.3f}" for r in REG] == ["0.062", "0.045", "0.079", "0.148", "0.099"], REF5
W1 = {w["region"]: w for w in cap["withins"]}
NC = {w["region"]: w["auc"] for w in ncc["within"]}
REF1 = {r: W1[r]["rf_canonical_increment"] for r in REG}
for r in REG:
    assert abs(NC[r]["full"] - NC[r]["baseline_only"] - REF1[r]) < 1e-5, r
WIN = {r: window(r) for r in REG}

# ---- rows: (label, reference, check, interval of the check) ----
GROUPS = [
    ("Against the 5 km-blocked gain", [
        ("Only cells within 10 km of the fire", REF5,
         {r: lad["10km"]["blocked_B10"]["per_region"][SHORT[r]] for r in REG}, None),
        ("Only cells within 5 km of the fire", REF5,
         {r: lad["5km_blocked_B10"]["per_region"][SHORT[r]] for r in REG}, None),
        ("Labels from VNP64A1", REF5, {r: r8m["regions"][r]["within_vnp"]["gain"] for r in REG}, None),
        ("Land cover from WorldCover 2020", REF5,
         {r: r8j["regions"][r]["within_2020"]["gain"] for r in REG}, None),
        ("Aspect added to both sets", REF5, {r: r8n[r]["with_aspect"]["gain"] for r in REG},
         {r: r8n[r]["with_aspect"]["ci95"] for r in REG}),
        ("Cells burned in prior 5 years removed", REF5,
         {r: r2["within_B10"][r]["excluded"]["delta"] for r in REG},
         {r: r2["within_B10"][r]["excluded"]["delta_ci"] for r in REG}),
        ("Cells burned in predictor window removed", {"bejis_2022": r8b["bejis_prelabel"]["block10_all"]["gain"]},
         {"bejis_2022": r8b["bejis_prelabel"]["block10_without_prelabel"]["gain"]}, None),
    ]),
    ("Against the 1 km-blocked gain", [
        ("Coordinate-informed channels removed", REF1,
         {r: NC[r]["no_coord_channels"] - NC[r]["baseline_only"] for r in REG}, None),
        ("Random forest, depth 6, leaf 50", REF1, {r: W1[r]["rf_shallow_increment"] for r in REG}, None),
        ("Random forest, leaf 200", REF1, {r: W1[r]["rf_leaf200_increment"] for r in REG}, None),
        ("Penalised logistic regression", REF1, {r: W1[r]["logistic_increment"] for r in REG}, None),
    ]),
    ("Against the window diagnostic", [
        ("Predictor window closed 7 days earlier", {r: WIN[r]["canonical"] for r in REG},
         {r: WIN[r]["close_7d_earlier"] for r in REG}, None),
        ("Predictor window closed 14 days earlier", {r: WIN[r]["canonical"] for r in REG},
         {r: WIN[r]["close_14d_earlier"] for r in REG}, None),
    ]),
]
assert abs(r8b["bejis_prelabel"]["block10_all"]["gain"] - REF5["bejis_2022"]) < 1e-9

# ---- the two statements of Section S1.1, asserted ----
checks = [(lab, r, v) for _, rows in GROUPS for lab, _, var, _ in rows for r, v in var.items()]
assert min(v for _, _, v in checks) > 0, "the text says the gain stays above zero under every check"
ci_rows = [(lab, r, ci) for _, rows in GROUPS for lab, _, _, cis in rows if cis for r, ci in cis.items()]
spans = [(lab, r) for lab, r, ci in ci_rows if ci[0] <= 0]
assert spans == [("Aspect added to both sets", "montiferru_2021")], spans
assert f"{r8n['montiferru_2021']['with_aspect']['gain']:+.3f}" == "+0.020"
assert f"[{r8n['montiferru_2021']['with_aspect']['ci95'][0]:.3f}, +{r8n['montiferru_2021']['with_aspect']['ci95'][1]:.3f}]" \
    .replace("-", "−") == "[−0.025, +0.066]"

# ---- layout: label column, then one panel per region ----
S.apply()
rows, labels, ys, y = [], [], [], 0.0
for gname, grows in GROUPS:
    labels.append((y, gname, True))
    y -= 1.0
    for lab, ref, var, ci in grows:
        rows.append((y, lab, ref, var, ci))
        labels.append((y, lab, False))
        y -= 1.0
    y -= 0.35
y_min = y + 0.35

fig, axes = plt.subplots(1, 5, figsize=(S.WIDTH_MM * S.MM, 104 * S.MM), sharey=True)
data_artists, allx = [], []
for ax, r in zip(axes, REG):
    ax.axvline(0, color=S.RULE, lw=0.8, zorder=0)
    for yy, lab, ref, var, ci in rows:
        if r not in var:
            continue
        a, b = ref[r], var[r]
        ax.plot([a, b], [yy, yy], color=S.GREY, lw=0.8, zorder=1)
        p0, = ax.plot(a, yy, "o", ms=4.6, mfc="white", mec=S.GREY, mew=0.9, zorder=2)
        p1, = ax.plot(b, yy, "o", ms=4.6, color=S.BLUE, zorder=3)
        data_artists += [(p0, f"{r}:{lab}:ref"), (p1, f"{r}:{lab}")]
        allx += [a, b]
        if ci:
            w, = ax.plot(ci[r], [yy, yy], color=S.BLUE, lw=1.0, zorder=2)
            data_artists.append((w, f"{r}:{lab}:ci"))
            allx += list(ci[r])
    ax.set_title(NAME[r], loc="center")
    ax.set_xlim(-0.06, 0.22)
    ax.set_xticks([0, 0.1, 0.2], ["0", "0.1", "0.2"])
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    assert_inside(ax, f"Fig. S1 {r}", xs=[v for v in allx])
axes[0].set_yticks([l[0] for l in labels], [l[1] for l in labels])
for t, (_, _, head) in zip(axes[0].get_yticklabels(), labels):
    if head:
        t.set_color(S.MUTED)
        t.set_fontstyle("italic")
axes[0].set_ylim(y_min - 0.3, 0.6)
axes[2].set_xlabel("thermal minus baseline ROC-AUC")
fig.legend(handles=[Line2D([], [], marker="o", ls="", ms=4.6, mfc="white", mec=S.GREY, label="reference"),
                    Line2D([], [], marker="o", ls="", ms=4.6, color=S.BLUE, label="with the check"),
                    Line2D([], [], color=S.BLUE, lw=1.0, label="95% interval")],
           loc="upper left", bbox_to_anchor=(0.005, 0.995), ncol=3, handletextpad=0.3, columnspacing=1.2)
fig.subplots_adjust(left=0.37, right=0.99, top=0.88, bottom=0.10, wspace=0.12)

problems = layout_check(fig, "Fig. S1 - within-region checks", min_gap_pt=2.0, min_font_pt=8.0,
                        data_artists=data_artists)
S.save(fig, HERE, "figS1_within_checks")
fig.savefig(HERE / "figS1_within_checks.png", dpi=300)

(HERE / "figS1_provenance.json").write_text(json.dumps({
    "figure": "Fig. S1 - the within-region thermal gain under every check",
    "script": "paper/figures/figS1_within_checks.py",
    "data": {p: hashlib.sha256((LR / p).read_bytes()).hexdigest() for p in SOURCES},
    "asserts": "the 5 km reference equals across r8n, r8m, r8j, r2 and the ladder; the 1 km reference "
               "equals across model_capacity and no_coord_channels; every check keeps the gain above zero "
               "in every region; only the Montiferru aspect interval includes zero, as Section S1.1 states",
    "canvas_mm": [S.WIDTH_MM, 104],
    "layout_check": f"paper/figures/_layout_check.py; {len(problems)} problems at build time",
    "environment": f"matplotlib {matplotlib.__version__}",
}, indent=1, ensure_ascii=False), encoding="utf-8")
print("figS1 written;", len(rows), "rows; min gain under a check", round(min(v for _, _, v in checks), 4))
# the text of Section S1.1 states the one interval that includes zero
TEXT = " ".join((HERE.parent / "supplementary.md").read_text(encoding="utf-8").split())
for s in ("+0.020 [−0.025, +0.066]", "Fig. S1"):
    assert s in TEXT, f"Section S1.1 must state {s}"
