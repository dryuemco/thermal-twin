"""Appendix tables built from their source files, and checked against the manuscript.

Each table is a function that reads its source file(s), whose sha256 is recorded in SOURCES, and
returns the exact markdown rows the manuscript must print (3 dp). Two modes:

    python paper/code/appendix_tables.py            # check: every expected row must appear
                                                    # verbatim, and the table must have no other
                                                    # data rows (so a stale row is caught)
    python paper/code/appendix_tables.py --write    # replace each table's data rows in place

Run from the repository root. Exit status 0 when every table matches. The check is also run by
paper/figures/check_all.py. Tables are added here one by one as the label-correction update of
the appendices proceeds (2026-09-23).
"""
import hashlib
import itertools
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "paper"
R5 = P / "labelfix_rerun" / "round5"
SOURCES = {
    "step9g": (R5 / "tables" / "step9g_multi_aoi_feature_stability.csv",
               "c864cd7dada65a175aaac3dde558b09c909541f7867265cbe55362f85370d0e9"),
    "reversal_holm": (P / "labelfix_rerun" / "inference" / "reversal_family_holm.csv", "71f36cb7e0d5886e72c31ab607f8a61f9a23d91434c32c506216c28ce93e6d66"),
    "s6": (R5 / "s6_diagnostics_20.csv", "a0d8b1cf21303467e4a77898c56a1cae6e1c8f5095ab9955000ef88127f9f4de"),
}
REG = ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended", "montiferru_2021"]
NAME = {"manavgat_2021": "Manavgat", "bejis_2022": "Bejís", "mugla_2021": "Muğla",
        "evia_2021_extended": "Evia", "montiferru_2021": "Montiferru"}
FEAT = ["elevation_mean", "slope_mean", "ndvi_mean", "lst_anomaly_mean", "current_lst_mean",
        "current_tvdi_mean", "tvdi_difference_mean", "downscaled_lst_mean", "fused_lst_mean"]
M = "−"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def src(key):
    path, expected = SOURCES[key]
    h = sha(path)
    if expected is not None:
        assert h == expected, f"{key}: sha256 {h[:12]} != recorded {expected[:12]}"
    return path


def s(v, nd=3):
    """signed, true minus"""
    return f"{v:+.{nd}f}".replace("-", M)


# ---- Step9G per-region signed AUCs (Table B2 and the strict criterion of B3) ------------------
def step9g():
    d = pd.read_csv(src("step9g"))
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
    for f in FEAT:
        cells = []
        for r in REG:
            a, lo, hi = g[(r, f)]
            pt = f"**{a:.3f}**" if supported(g[(r, f)]) else f"{a:.3f}"
            cells.append(f"{pt} [{lo:.3f}, {hi:.3f}]")
        rows.append(f"| `{f}` | " + " | ".join(cells) + " |")
    return rows


def b3_sets():
    g = step9g()
    strict, point = [], 0
    for f in FEAT:
        for a, b in itertools.combinations(REG, 2):
            va, vb = g[(a, f)], g[(b, f)]
            if (va[0] - 0.5) * (vb[0] - 0.5) < 0:
                if supported(va) and supported(vb):
                    lo, hi = sorted((a, b), key=lambda x: g[(x, f)][0])
                    strict.append((f, lo, hi))
                else:
                    point += 1
    return g, strict, point


def table_b3():
    g, strict, _ = b3_sets()
    h = pd.read_csv(src("reversal_holm"))
    h = h[h.frame == "full"]
    rows = []
    for f, lo, hi in strict:
        r = h[(h.feature == f) & (((h.region_a == lo) & (h.region_b == hi)) |
                                  ((h.region_a == hi) & (h.region_b == lo)))]
        assert len(r) == 1, (f, lo, hi)
        r = r.iloc[0]
        assert bool(r.strict_supported_1000), (f, lo, hi)        # the two sources agree
        sign = 1 if r.region_a == hi else -1                      # file diff = auc_a - auc_b
        d = sign * r["diff"]
        ci = sorted((sign * r.diff_lo_1000, sign * r.diff_hi_1000))
        assert abs(d - (g[(hi, f)][0] - g[(lo, f)][0])) < 1e-9
        rows.append(f"| `{f}` | {NAME[lo]} | {g[(lo, f)][0]:.3f} | {NAME[hi]} | {g[(hi, f)][0]:.3f} | "
                    f"{s(d)} [{s(ci[0])}, {s(ci[1])}] |")
    return rows


# ---- Table B1: the twenty diagnostics ------------------------------------------------------
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
    d = pd.read_csv(src("s6")).set_index("measure")
    rows = []
    for key, label, fam, exp in B1_ROWS:
        r = d.loc[key]
        n = int(r.n_directions_corrected)
        rho = f"{s(r.spearman_rho_corrected, 2)} [{s(r.spearman_ci_low_corrected, 2)}, {s(r.spearman_ci_high_corrected, 2)}]"
        if key == "vector_spearman_supported":
            assert n == 6 and bool(r.ci_excludes_zero_corrected)
            verdict = "degenerate interval; not interpreted"
        else:
            assert not bool(r.ci_excludes_zero_corrected), key
            verdict = "no"
        rows.append(f"| {label} | {fam} | {exp} | {n} | {rho} | {verdict} |")
    return rows


# ---- where each table lives ------------------------------------------------------------------
TABLES = {
    "B1": (P / "supplementary_appendices.md", "**Table B1.", table_b1),
    "B2": (P / "A2_diagnostics.md", "**Table B2.", table_b2),
    "B3": (P / "A2_diagnostics.md", "**Table B3.", table_b3),
}


def data_block(text, anchor):
    """(start, end) of the data rows of the first markdown table after the anchor."""
    i = text.index(anchor)
    j = text.index("\n|", i) + 1                      # header row
    k = text.index("\n", text.index("\n", j) + 1) + 1  # after the separator row
    e = k
    while text.startswith("|", e):
        e = text.index("\n", e) + 1
    return k, e


def main():
    write = "--write" in sys.argv
    bad = 0
    for name, (path, anchor, fn) in TABLES.items():
        expected = fn()
        text = path.read_text(encoding="utf-8")
        k, e = data_block(text, anchor)
        current = text[k:e].rstrip("\n").split("\n")
        if write:
            text = text[:k] + "\n".join(expected) + "\n" + text[e:]
            path.write_text(text, encoding="utf-8")
            print(f"{name}: wrote {len(expected)} rows")
            continue
        missing = [r for r in expected if r not in current]
        extra = [r for r in current if r not in expected]
        ok = not missing and not extra
        bad += not ok
        print(f"{name}: {'PASS' if ok else 'FAIL'}  {len(expected)} rows  "
              f"{len(missing)} missing, {len(extra)} stale")
        for r in missing[:3]:
            print("   expected:", r)
        for r in extra[:3]:
            print("   stale   :", r)
    print("sources:", {k: sha(v[0])[:12] for k, v in SOURCES.items()})
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
