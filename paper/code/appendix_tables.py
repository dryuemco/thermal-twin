"""Appendix tables built from their source files, and checked against the manuscript.

Each table is a function that reads its source files and returns the exact markdown rows the
manuscript must print (3 dp unless the table prints otherwise). Modes, run from the repo root:

    python paper/code/appendix_tables.py            # check the corrected tables: every expected
                                                    # row must be printed and no other data row
                                                    # may be (a stale row fails the check)
    python paper/code/appendix_tables.py --write    # replace each table's data rows in place
    python paper/code/appendix_tables.py --frozen   # build the tables from the FROZEN sources and
                                                    # compare with the text: before --write this
                                                    # reproduces the printed frozen tables, which
                                                    # validates the method and exposes errors that
                                                    # predate the label correction
    python paper/code/appendix_tables.py --pin      # rewrite the source manifest (sha256)

Every corrected source file is listed with its sha256 in
paper/labelfix_rerun/round5/tables/SOURCES.sha256, and the check fails if a file is missing from
it or has changed. paper/figures/check_all.py runs the check.
"""
import hashlib
import itertools
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import ndimage, stats

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "paper"
R5 = P / "labelfix_rerun" / "round5"
TB = R5 / "tables"
LC = P / "labelfix_rerun" / "code"
MANIFEST = TB / "SOURCES.sha256"
sys.path.insert(0, str(P / "code"))
import _canonical  # noqa: E402

LABEL = "frozen" if "--frozen" in sys.argv else "corrected"
USED = set()

REG = ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended", "montiferru_2021"]
NAME = {"manavgat_2021": "Manavgat", "bejis_2022": "Bejís", "mugla_2021": "Muğla",
        "evia_2021_extended": "Evia", "montiferru_2021": "Montiferru"}
YEAR = {"manavgat_2021": "Manavgat 2021", "bejis_2022": "Bejís 2022", "mugla_2021": "Muğla 2021",
        "evia_2021_extended": "North Evia 2021", "montiferru_2021": "Montiferru 2021"}
FEAT = ["elevation_mean", "slope_mean", "ndvi_mean", "lst_anomaly_mean", "current_lst_mean",
        "current_tvdi_mean", "tvdi_difference_mean", "downscaled_lst_mean", "fused_lst_mean"]
PAIRS = ["manavgat_2021__bejis_2022", "manavgat_2021__mugla_2021", "manavgat_2021__evia_2021_extended",
         "montiferru_2021__manavgat_2021", "montiferru_2021__bejis_2022", "montiferru_2021__mugla_2021",
         "montiferru_2021__evia_2021_extended", "bejis_2022__mugla_2021", "bejis_2022__evia_2021_extended",
         "mugla_2021__evia_2021_extended"]
M = "−"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def f(corrected, frozen):
    """the source path for the active label, recorded for the manifest check"""
    p = Path(corrected if LABEL == "corrected" else frozen)
    if LABEL == "corrected":
        USED.add(p)
    return p


def s(v, nd=3):
    return f"{v:+.{nd}f}".replace("-", M)


# ---- sources ---------------------------------------------------------------------------------
def src_step9g():
    return f(TB / "step9g_multi_aoi_feature_stability.csv", TB / "frozen" / "step9g_multi_aoi_feature_stability.csv")


def src_pair(pair, name):
    return f(TB / "corrected" / pair / name, TB / "frozen" / pair / name)


def src_code(name):                      # paper/code outputs: labelfix_rerun/code vs the published paper/
    return f(LC / name, P / name)


def load_region(reg):
    # the parquet's sha256 is verified by _canonical itself (CANONICAL_SHA256 / CORRECTED),
    # so it is not repeated in this module's manifest
    lab = "corrected" if LABEL == "corrected" else "frozen"
    d = _canonical.load(reg, labels=lab)
    return d


# ---- Step9G per-region signed AUCs (B2, B3, B7) ------------------------------------------------
def step9g():
    d = pd.read_csv(src_step9g())
    out = {}
    for side in "ab":
        for _, r in d.iterrows():
            out[(r[f"experiment_{side}"], r.feature)] = (r[f"experiment_{side}_auc"],
                                                        r[f"experiment_{side}_ci_low"],
                                                        r[f"experiment_{side}_ci_high"])
    return out


def supported(v):
    return v[1] > 0.5 or v[2] < 0.5


def table_b2():
    g = step9g()
    rows = []
    for ft in FEAT:
        cells = []
        for r in REG:
            a, lo, hi = g[(r, ft)]
            cells.append(f"{f'**{a:.3f}**' if supported(g[(r, ft)]) else f'{a:.3f}'} [{lo:.3f}, {hi:.3f}]")
        rows.append(f"| `{ft}` | " + " | ".join(cells) + " |")
    return rows


def b3_sets():
    g = step9g()
    strict, point = [], 0
    for ft in FEAT:
        for a, b in itertools.combinations(REG, 2):
            va, vb = g[(a, ft)], g[(b, ft)]
            if (va[0] - 0.5) * (vb[0] - 0.5) < 0:
                if supported(va) and supported(vb):
                    strict.append((ft, *sorted((a, b), key=lambda x: g[(x, ft)][0])))
                else:
                    point += 1
    return g, strict, point


def holm():
    return pd.read_csv(f(P / "labelfix_rerun" / "inference" / "reversal_family_holm.csv",
                         P / "ems_analyses" / "inference" / "reversal_family_holm.csv"))


def table_b3():
    g, strict, _ = b3_sets()
    h = holm()
    h = h[h.frame == "full"]
    rows = []
    for ft, lo, hi in strict:
        r = h[(h.feature == ft) & (((h.region_a == lo) & (h.region_b == hi)) | ((h.region_a == hi) & (h.region_b == lo)))]
        assert len(r) == 1, (ft, lo, hi)
        r = r.iloc[0]
        assert bool(r.strict_supported_1000), (ft, lo, hi)
        sign = 1 if r.region_a == hi else -1
        d = sign * r["diff"]
        ci = sorted((sign * r.diff_lo_1000, sign * r.diff_hi_1000))
        assert abs(d - (g[(hi, ft)][0] - g[(lo, ft)][0])) < 1e-9
        rows.append(f"| `{ft}` | {NAME[lo]} | {g[(lo, ft)][0]:.3f} | {NAME[hi]} | {g[(hi, ft)][0]:.3f} | "
                    f"{s(d)} [{s(ci[0])}, {s(ci[1])}] |")
    return rows


# ---- B1: the twenty diagnostics ------------------------------------------------------------------
B1_ROWS = [
    ("agree_fraction_supported", "Agreement fraction, supported features", "P(y\\|x) conditional", "+"),
    ("cosine_supported", "Cosine, supported features", "P(y\\|x) conditional", "+"),
    ("cosine_9", "Cosine, all 9 features", "P(y\\|x) conditional", "+"),
    ("vector_spearman_9", "Vector Spearman, all 9", "P(y\\|x) conditional", "+"),
    ("agree_count_9", "Agreement count, all 9", "P(y\\|x) conditional", "+"),
    ("schoener_d_mean1d", "Schoener's D, 1-D mean", "P(x\\|y=1) niche", "+"),
    ("warren_i_mean1d", "Warren's I, 1-D mean", "P(x\\|y=1) niche", "+"),
    ("schoener_d_pca2d", "Schoener's D, PCA-2D", "P(x\\|y=1) niche", "+"),
    ("warren_i_pca2d", "Warren's I, PCA-2D", "P(x\\|y=1) niche", "+"),
    ("mahalanobis_burned", "Mahalanobis, burned centroids", "P(x\\|y=1) niche", "−"),
    ("domain_classifier_auc", "Domain-classifier AUC", "P(ix) marginal", "−"),
    ("target_mean_dissimilarity", "Predictor-space mean dissimilarity", "P(ix) marginal", "−"),
    ("target_p95_dissimilarity", "Predictor-space p95 dissimilarity", "P(ix) marginal", "−"),
    ("fraction_inside_weighted_aoa", "Fraction inside weighted AoA", "P(ix) marginal", "+"),
    ("unweighted_fraction_inside_support", "Fraction inside unweighted support", "P(ix) marginal", "+"),
    ("climate_distance", "Climatic distance", "P(ix) marginal", "−"),
    ("geographic_distance_km", "Geographic distance", "geographic", "−"),
    ("regime_dist_log_effn", "Regime distance, log effective-N", "P(y) structure", "−"),
    ("regime_dist_largest_share", "Regime distance, largest share", "P(y) structure", "−"),
    ("vector_spearman_supported", "Vector Spearman, supported (≥3 feats) ‡", "P(y\\|x) conditional", "+"),
]


def table_b1():
    d = pd.read_csv(f(R5 / "s6_diagnostics_20.csv", R5 / "s6_diagnostics_20.csv")).set_index("measure")
    sfx = "corrected" if LABEL == "corrected" else "frozen"
    rows = []
    for key, label, fam, exp in B1_ROWS:
        r = d.loc[key]
        n = int(r[f"n_directions_{sfx}"])
        rho = f"{s(r[f'spearman_rho_{sfx}'], 2)} [{s(r[f'spearman_ci_low_{sfx}'], 2)}, {s(r[f'spearman_ci_high_{sfx}'], 2)}]"
        if key == "vector_spearman_supported":
            verdict = "degenerate interval; not interpreted"
        else:
            verdict = "yes" if bool(r[f"ci_excludes_zero_{sfx}"]) else "no"
        rows.append(f"| {label} | {fam} | {exp} | {n} | {rho} | {verdict} |")
    return rows


# ---- B4: PR-AUC against the no-skill baseline (step9b, primary population) --------------------
def b4_values():
    out = {}
    for pair in PAIRS:
        m = json.loads(src_pair(pair, "step9b_metrics.json").read_text(encoding="utf-8"))
        for r in m["results"]:
            if r["population"] != "burnable_tree_shrub_grass":
                continue
            out[r["transfer_direction"]] = (r["thermal_metrics"]["roc_auc"], r["thermal_metrics"]["pr_auc"],
                                            r["target_burned_prevalence"])
    assert len(out) == 20
    return out


def table_b4():
    v = b4_values()
    order = sorted(v, key=lambda d: -(v[d][1] / v[d][2]))
    rows = []
    for d in order:
        roc, pr, base = v[d]
        a, b = d.split("_to_")
        lift = pr / base
        lf = f"**{lift:.2f}**" if (lift < 1 or lift > 2) else f"{lift:.2f}"
        rows.append(f"| {NAME[a]} → {NAME[b]} | {roc:.3f} | {pr:.3f} | {base:.3f} | {lf} |")
    mr, mp, mb = (np.mean([v[d][i] for d in v]) for i in range(3))
    ml = np.mean([v[d][1] / v[d][2] for d in v])
    rows.append(f"| **Mean** | **{mr:.3f}** | **{mp:.3f}** | **{mb:.3f}** | **{ml:.2f}** |")
    return rows


# ---- B5: Muğla 2021 versus 2022 (label-independent; bound anyway) --------------------------------
def table_b5():
    rel = "step9g_raw/step9g_univariate_feature_auc_direction_reversal/mugla_2021__mugla_2022_event_relative/step9g_direction_reversal_table.csv"
    p = f(P / rel, P / rel)                          # one file: the arm does not involve Manavgat
    d = pd.read_csv(p)
    return d  # rows are validated against the printed table in table_b5_rows


def table_b5_rows():
    d = table_b5()
    rows = []
    for _, r in d.iterrows():
        va = (r.mugla_2021_auc, r.mugla_2021_ci_low, r.mugla_2021_ci_high)
        vb = (r.mugla_2022_event_relative_auc, r.mugla_2022_event_relative_ci_low, r.mugla_2022_event_relative_ci_high)
        opposite = (va[0] - 0.5) * (vb[0] - 0.5) < 0
        strict = opposite and supported(va) and supported(vb)
        kind = "**bootstrap-supported**" if strict else ("point only" if opposite else "none")
        cell = lambda v: f"{v[0]:.3f} [{v[1]:.3f}, {v[2]:.3f}]"
        if strict:
            rows.append(f"| **{r.feature}** | **{cell(va)}** | **{cell(vb)}** | {kind} |")
        else:
            rows.append(f"| {r.feature} | {cell(va)} | {cell(vb)} | {kind} |")
    return rows


# ---- B6 and B8: counts and frame geometry, from the step8a tables --------------------------------
def region_frame(reg):
    d = load_region(reg)
    t = d[(d.valid_for_modeling == True) & (d.burnable_tree_shrub_grass == True)].reset_index(drop=True)  # noqa: E712
    r0, c0 = int(t.row_500m.min()), int(t.col_500m.min())
    H, W = int(t.row_500m.max()) - r0 + 1, int(t.col_500m.max()) - c0 + 1
    rr, cc = t.row_500m.to_numpy().astype(int) - r0, t.col_500m.to_numpy().astype(int) - c0
    bg = np.ones((H, W), bool)
    b = t.burned.to_numpy() == 1
    bg[rr[b], cc[b]] = False
    dist = ndimage.distance_transform_edt(bg)[rr, cc] * 0.45
    return d, t, dist


B6_BOLD = {"manavgat_2021", "bejis_2022", "montiferru_2021"}


def table_b6():
    rows = []
    for reg in REG:
        _, t, dist = region_frame(reg)
        share = 100 * float(np.mean(dist > 10))
        sh = f"{share:.1f} %"
        rows.append(f"| {NAME[reg]} | {len(t):,} | {int(t.burned.sum()):,} | {np.median(dist):.1f} km | "
                    f"{f'**{sh}**' if reg in B6_BOLD else sh} |")
    return rows


B8_NAME = {"manavgat_2021": "Manavgat 2021", "bejis_2022": "Bejís 2022", "mugla_2021": "Muğla 2021",
           "evia_2021_extended": "North Evia 2021 (extended)", "montiferru_2021": "Montiferru 2021"}


def table_b8():
    rows = []
    for reg in REG:
        d, t, _ = region_frame(reg)
        v = d[d.valid_for_modeling == True]  # noqa: E712
        gate = json.loads(f(TB / "corrected" / "gates" / f"{reg}.json", TB / "frozen" / "gates" / f"{reg}.json").read_text(encoding="utf-8"))
        nat = gate["burned_natural_vegetation_fraction"]
        verdict = "pass" if nat >= gate["thresholds"]["natural_threshold"] else "fail"
        bv, bt = int(v.burned.sum()), int(t.burned.sum())
        rows.append(f"| {B8_NAME[reg]} | {len(d):,} | {len(v):,} | {bv:,} | {bv / len(v):.3f} | {len(t):,} | {bt:,} | "
                    f"{bt / len(t):.3f} | {nat:.3f} | {verdict} |")
    return rows


# ---- B7: signed AUC, full frame against the 10 km collar ----------------------------------------
B7_ROWS = [("elevation_mean", "elevation"), ("current_lst_mean", "current LST"), ("current_tvdi_mean", "current TVDI")]


def table_b7():
    g = step9g()
    c = pd.read_csv(src_code("aoi_frame_auc_frozen_mugla.csv"))
    c = c[c.collar == "<=10km"]
    col = {(r.region, r.feature): r.auc for _, r in c.iterrows()}
    rows = []
    for ft, lab in B7_ROWS:
        for frame, vals in (("full frame", [g[(r, ft)][0] for r in REG]), ("10 km collar", [col[(r, ft)] for r in REG])):
            above = [v > 0.5 for v in vals]
            straddle = 0 < sum(above) < len(vals)
            # the printed convention: on a straddling row, Manavgat (the odd region) is in bold
            cells = [f"**{v:.3f}**" if (straddle and r == "manavgat_2021") else f"{v:.3f}" for v, r in zip(vals, REG)]
            name = f"{lab}, {frame}" + (" (Table B2)" if (ft == "elevation_mean" and frame == "full frame") else "")
            rows.append(f"| {name} | " + " | ".join(cells) + f" | {'**yes**' if straddle else 'no'} |")
    return rows


# ---- B9: the transfer matrix (step10) ------------------------------------------------------------
B9_ORDER = [("manavgat_2021", "bejis_2022"), ("bejis_2022", "manavgat_2021"), ("manavgat_2021", "mugla_2021"),
            ("mugla_2021", "manavgat_2021"), ("manavgat_2021", "evia_2021_extended"), ("evia_2021_extended", "manavgat_2021"),
            ("bejis_2022", "mugla_2021"), ("mugla_2021", "bejis_2022"), ("bejis_2022", "evia_2021_extended"),
            ("evia_2021_extended", "bejis_2022"), ("mugla_2021", "evia_2021_extended"), ("evia_2021_extended", "mugla_2021"),
            ("montiferru_2021", "manavgat_2021"), ("manavgat_2021", "montiferru_2021"), ("montiferru_2021", "bejis_2022"),
            ("bejis_2022", "montiferru_2021"), ("montiferru_2021", "mugla_2021"), ("mugla_2021", "montiferru_2021"),
            ("montiferru_2021", "evia_2021_extended"), ("evia_2021_extended", "montiferru_2021")]
B9_V = [("raw_source_only", "raw"), ("regionwise_zscore", "z"), ("coral_after_regionwise_zscore", "coral")]


def table_b9():
    pt, ci = {}, {}
    for pair in PAIRS:
        m = json.loads(src_pair(pair, "step10_metrics.json").read_text(encoding="utf-8"))
        b = pd.read_csv(src_pair(pair, "step10_bootstrap_summary.csv"))
        for d, var in m["point_metrics"].items():
            for key, short in B9_V:
                pt[(d, short)] = var[key]["thermal"]["roc_auc"]
                r = b[(b.direction == d) & (b.series == f"roc_auc__{key}_thermal")].iloc[0]
                ci[(d, short)] = (r.ci_2_5, r.ci_97_5)
    rows = []
    for a, b in B9_ORDER:
        d = f"{a}_to_{b}"
        cells = [f"{pt[(d, k)]:.3f} [{ci[(d, k)][0]:.3f}, {ci[(d, k)][1]:.3f}]" for _, k in B9_V]
        rows.append(f"| {NAME[a]}→{NAME[b]} | " + " | ".join(cells) + " |")
    return rows


# ---- B10: the contrast pairs ---------------------------------------------------------------------
def table_b10():
    cp = json.loads(f(R5 / "out_official" / "figure_contrast_pairs.json", P / "figure_contrast_pairs.json").read_text(encoding="utf-8"))
    cp = {p["pair"]: p for p in cp["pairs"]}
    L, R = cp["manavgat_2021 ~ mugla_2021"], cp["bejis_2022 ~ montiferru_2021"]
    ct = pd.read_csv(f(R5 / "collar" / "aoi_frame_transfer.csv", P / "aoi_frame_transfer_frozen_mugla.csv"))
    ct = ct[(ct.source_frame == "10km") & (ct.target_frame == "10km")].sort_values("thermal").reset_index(drop=True)
    cv = {r.direction: (r.thermal, i + 1) for i, r in ct.iterrows()}
    aoa = pd.read_csv(f(R5 / "collar" / "aoa_directed_pair_summary.csv", TB / "frozen" / "aoa_directed_pair_summary.csv")).set_index("direction")["fraction_inside_weighted_aoa"]
    fd = lambda p: sorted(v["schoener_d_this_feature"] for k, v in p["per_feature_signed_auc"].items())
    o = lambda n: f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"
    MM_, MG_, BM_, MB_ = ("manavgat_2021_to_mugla_2021", "mugla_2021_to_manavgat_2021",
                          "bejis_2022_to_montiferru_2021", "montiferru_2021_to_bejis_2022")
    tl, tr = L["transfer"], R["transfer"]
    return [
        f"| Schoener's *D*, mean 1-D | **{L['niche_overlap']['schoener_d_mean1d']:.3f}** (highest) | "
        f"**{R['niche_overlap']['schoener_d_mean1d']:.3f}** (lowest) |",
        f"| per-feature *D* | {fd(L)[0]:.2f} to {fd(L)[-1]:.2f} | {fd(R)[0]:.2f} to {fd(R)[-1]:.2f} |",
        f"| transfer, frames as drawn | {tl[MM_]['auc']:.3f}, {tl[MG_]['auc']:.3f} | {tr[BM_]['auc']:.3f}, {tr[MB_]['auc']:.3f} |",
        f"| transfer, 10 km collar | {cv[MM_][0]:.3f}, {cv[MG_][0]:.3f} | {cv[BM_][0]:.3f}, {cv[MB_][0]:.3f} |",
        f"| rank of 20 on the collar, from the bottom | {o(cv[MM_][1])}, {o(cv[MG_][1])} | {o(cv[BM_][1])}, {o(cv[MB_][1])} |",
        f"| target cells inside the AoA | {aoa[MM_]:.3f}, {aoa[MG_]:.3f} | — |",
    ]


# ---- A1–A4: the four evaluations of Section 4.3 ----------------------------------------------------
def table_a1():
    d = json.loads(src_code("positive_control.json").read_text(encoding="utf-8"))["splits"]
    rows = []
    for r in d:
        fmt = lambda v: "—" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{v:.3f}"
        th, bl = fmt(r.get("thermal_auc")), fmt(r.get("baseline_auc"))
        rows.append(f"| {r['region'].replace('_', ' ')} | {r['split_axis'].replace('_', '-')} | "
                    f"{r['direction'].replace('_', ' ')} | {r['source_positives']:,} | {r['target_positives']:,} | {th} | {bl} |")
    return rows


def a2_records():
    d = [r for r in json.loads(src_code("scar_control.json").read_text(encoding="utf-8")) if r["buffer_km"] == 2]
    return sorted(d, key=lambda r: (r["region"], r["src_pos"]))


def table_a2():
    return [f"| {r['region'].replace('_', ' ')} | {r['scar']} | {r['src_pos']:,} | {r['tgt_pos']:,} | {r['tgt_n']:,} | {r['auc']:.3f} |"
            for r in a2_records()]


def a3_groups():
    d = pd.DataFrame(json.loads(src_code("d_per_source.json").read_text(encoding="utf-8")))
    return d, d.groupby(["target_region", "scar"]).auc.agg(["mean", "min", "max"]).reset_index()


def table_a3():
    _, g = a3_groups()
    return [f"| {YEAR[r.target_region]} | {r.scar} | {r['mean']:.3f} | {r['min']:.3f} | {r['max']:.3f} | {r['max'] - r['min']:.3f} |"
            for _, r in g.iterrows()]


def a4_records():
    return json.loads(src_code("prevalence_control.json").read_text(encoding="utf-8"))


def table_a4():
    d = a4_records()
    # The producer (prevalence_control.py) stores these at 4 dp, so the table prints them at 4 dp:
    # rounding a stored ...5 to 3 dp would double-round and cannot be done unambiguously.
    # Cross-check: column A is the region's 5 km blocked thermal AUC, which Table 1 prints (block 10).
    fig = json.loads(f(P / "figures" / "data" / "fig_data_corrected.json", P / "figures" / "data" / "fig_data.json").read_text(encoding="utf-8"))["fig34"]
    for r in d:
        assert abs(r["A_region"] - fig[r["region"]]["10"]["thermal"]) < 5.1e-5, (r["region"], r["A_region"])
    rows = [f"| {YEAR[r['region']]} | {r['scar']} | {r['prevalence']:.2f} | {r['A_region']:.4f} | "
            f"{r['A_prime_prevalence_matched']:.4f} | {r['B_scar_area']:.4f} |" for r in d]
    mean = lambda k: np.mean([r[k] for r in d])
    rows.append(f"| **Mean** | | | **{mean('A_region'):.4f}** | **{mean('A_prime_prevalence_matched'):.4f}** | "
                f"**{mean('B_scar_area'):.4f}** |")
    return rows


def a4_differences():
    d = a4_records()
    out = {}
    for name, x, y in (("A-A'", "A_region", "A_prime_prevalence_matched"), ("A'-B", "A_prime_prevalence_matched", "B_scar_area")):
        v = np.array([r[x] - r[y] for r in d])
        h = stats.t.ppf(0.975, len(v) - 1) * v.std(ddof=1) / np.sqrt(len(v))
        out[name] = (v.mean(), v.mean() - h, v.mean() + h)
    return out


# ---- A5: the transfer-gap decomposition --------------------------------------------------------------
A5_METHOD = {"regionwise_zscore": "z-score", "coral_after_regionwise_zscore": "CORAL"}
A5_STATUS = {"supported_relative_recovery_but_chance_not_excluded": "recovery, chance not excluded",
             "supported_recovery_above_chance": "recovery above chance", "negative_recovery": "**negative recovery**"}


def a5_records():
    d = pd.read_csv(f(TB / "corrected" / "four_aoi_decomposition.csv", TB / "frozen" / "four_aoi_decomposition.csv"))
    d = d[(d.model_family == "thermal") & (d.metric == "roc_auc")]
    recs = []
    for dirn, g in d.groupby("direction"):
        z = g[g.adaptation_method == "regionwise_zscore"].iloc[0]
        c = g[g.adaptation_method == "coral_after_regionwise_zscore"].iloc[0]
        best = z if z.adapted_auc >= c.adapted_auc else c
        recs.append(best)
    return sorted(recs, key=lambda r: -r.recovered_fraction)


def table_a5():
    rows = []
    for r in a5_records():
        a, b = r.direction.split("_to_")
        rows.append(f"| {NAME[a]}→{NAME[b]} | {r.within_target_auc:.3f} | {r.raw_auc:.3f} | {r.adapted_auc:.3f} "
                    f"({A5_METHOD[r.adaptation_method]}) | {s(r.recovered_fraction, 2)} [{s(r.recovered_fraction_ci_low, 2)}, "
                    f"{s(r.recovered_fraction_ci_high, 2)}] | {A5_STATUS[r.recovery_status]} |")
    return rows


# ---- A6: LST-anomaly differences under the collar ------------------------------------------------------
def table_a6():
    h = holm()
    h = h[(h.frame == "collar10") & (h.feature == "lst_anomaly_mean")]
    h = h[h.opposite_sides & ((h.diff_lo_1000 > 0) | (h.diff_hi_1000 < 0))]
    h = h.reindex(h["diff"].abs().sort_values(ascending=False).index)
    return [f"| {NAME[r.region_a]} vs {NAME[r.region_b]} | {r.auc_a:.3f} | {r.auc_b:.3f} | {s(r['diff'])} | "
            f"[{s(r.diff_lo_1000)}, {s(r.diff_hi_1000)}] |" for _, r in h.iterrows()]


# ---- where each table lives -----------------------------------------------------------------------------
SUPP, A2F = P / "supplementary_appendices.md", P / "A2_diagnostics.md"
TABLES = {
    "B1": (SUPP, "**Table B1.", table_b1), "B2": (A2F, "**Table B2.", table_b2), "B3": (A2F, "**Table B3.", table_b3),
    "B4": (A2F, "**Table B4.", table_b4), "B5": (A2F, "**Table B5.", table_b5_rows), "B6": (A2F, "**Table B6.", table_b6),
    "B7": (A2F, "**Table B7.", table_b7), "B8": (A2F, "**Table B8.", table_b8), "B9": (A2F, "**Table B9.", table_b9),
    "B10": (SUPP, "**Table B10.", table_b10),
    "A1": (SUPP, "**Table A1.", table_a1), "A2": (SUPP, "**Table A2.", table_a2), "A3": (SUPP, "**Table A3.", table_a3),
    "A4": (SUPP, "**Table A4.", table_a4), "A5": (SUPP, "**Table A5.", table_a5), "A6": (SUPP, "**Table A6.", table_a6),
}


def data_block(text, anchor):
    i = text.index(anchor)
    j = text.index("\n|", i) + 1
    k = text.index("\n", text.index("\n", j) + 1) + 1
    e = k
    while text.startswith("|", e):
        e = text.index("\n", e) + 1
    return k, e


def read_manifest():
    if not MANIFEST.exists():
        return {}
    out = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        h, p = line.split("  ", 1)
        out[p] = h
    return out


def main():
    write, pin = "--write" in sys.argv, "--pin" in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    bad = 0
    for name, (path, anchor, fn) in TABLES.items():
        if only and name not in only:
            continue
        expected = fn()
        text = path.read_text(encoding="utf-8")
        k, e = data_block(text, anchor)
        current = text[k:e].rstrip("\n").split("\n")
        if write:
            path.write_text(text[:k] + "\n".join(expected) + "\n" + text[e:], encoding="utf-8")
            print(f"{name}: wrote {len(expected)} rows")
            continue
        missing = [r for r in expected if r not in current]
        extra = [r for r in current if r not in expected]
        ok = not missing and not extra
        bad += not ok
        print(f"{name}: {'PASS' if ok else 'FAIL'}  {len(expected)} rows  {len(missing)} missing, {len(extra)} stale"
              + ("  [frozen sources]" if LABEL == "frozen" else ""))
        for r in missing[:4]:
            print("   expected:", r)
        for r in extra[:4]:
            print("   printed :", r)
    if LABEL == "corrected" and not write:
        rel = {str(p.resolve().relative_to(ROOT)).replace("\\", "/"): p for p in USED}
        if pin:
            MANIFEST.write_text("".join(f"{sha(p)}  {r}\n" for r, p in sorted(rel.items())), encoding="utf-8")
            print(f"pinned {len(rel)} source files in {MANIFEST.relative_to(ROOT)}")
        else:
            man = read_manifest()
            for r, p in sorted(rel.items()):
                if man.get(r) != sha(p):
                    bad += 1
                    print(f"SOURCE: {r} {'not in manifest' if r not in man else 'sha256 changed'}")
            print(f"sources: {len(rel)} files checked against {MANIFEST.relative_to(ROOT)}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
