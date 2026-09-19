"""Pre-registered precision analysis for the multi-tile, multi-season study (STUDY_DESIGN.md s2, s6, s7).

Reads only frozen pilot artefacts under paper/labelfix_rerun/ (corrected Manavgat labels), estimates the
pilot's variance components, and projects expected 95 % interval half-widths, power, equivalence
probabilities and minimum detectable effects for the new design's primary contrasts.

Run:  <thermal-twin>/.venv-step10/Scripts/python.exe design/precision/precision_analysis.py
Seed 42 everywhere. No package beyond numpy / scipy / pandas. The crossed random-effects model is fitted by
REML implemented here directly (statsmodels is not installed): y_ij = mu + a_i + b_j + d_ij + e_ij with
a (source), b (target), d (dyad) Gaussian and e the known sampling error of direction ij.

Every number that is NOT estimated from the pilot is an ASSUMPTION and is declared in ASSUMPTIONS below
with its sensitivity range. Nothing here uses an outcome of the new study.
"""
from __future__ import annotations

import json
import math
import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import optimize, stats

SEED = 42
ROOT = Path(__file__).resolve().parents[2]            # thermal-twin-main
PILOT = ROOT / "paper" / "labelfix_rerun"
OUT = Path(__file__).resolve().parent

F_MATRIX = PILOT / "pipeline" / "_derived" / "matrix_corrected.csv"
F_BLOCKCI = PILOT / "round3" / "transfer_ci_blocksize.csv"
F_LARGE = PILOT / "pipeline" / "robustness" / "step8_large_block" / "manavgat_2021__bejis_2022"
F_LADDER = PILOT / "inference" / "ladder_summary.json"
F_LORO = PILOT / "code" / "loro_all.json"

REGIONS = ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended", "montiferru_2021"]
SHORT = {"Manavgat": "manavgat_2021", "Bejis": "bejis_2022", "Mugla": "mugla_2021",
         "Evia": "evia_2021_extended", "Montiferru": "montiferru_2021"}
Z975 = stats.norm.ppf(0.975)

# ----------------------------------------------------------------------------------------------------
# Assumptions (not estimable from the pilot). Central value first, then the sensitivity range.
# ----------------------------------------------------------------------------------------------------
ASSUMPTIONS = {
    "A1_temporal_sd_ratio_k": {
        "central": 1.0, "range": [0.5, 1.0, 1.5],
        "what": "SD of the true temporal transfer gap (V1 - V2) across tile-seasons, as a multiple k of the "
                "SD of the true spatial gap (V1 - V3) across directions estimated from the pilot. The pilot has "
                "one season per region, so k is NOT estimated. Pilot-internal proxy only: in the scar frame the "
                "leave-one-scar-out (same region, another fire) AUCs are about as dispersed as the foreign-region "
                "AUCs (ratio reported in pilot_variance_components.json), which argues against k << 1."},
    "A2_temporal_tile_share_pi": {
        "central": 0.5, "range": [0.5, 1.0],
        "what": "Share of the temporal-gap variance that is persistent per tile (does not average over "
                "seasons); the rest is season-specific and averages over the S seasons. pi = 1 is the worst case."},
    "A3_spatial_persistence": {
        "central": 1.0, "range": [1.0, 0.5],
        "what": "Share of the pilot's target and dyad variance that is persistent across seasons. The pilot "
                "cannot separate tile from tile-season, so the central choice treats all of it as persistent "
                "(conservative: season averaging does not shrink it)."},
    "A4_sampling_multiplier_g": {
        "central": 1.0, "range": [0.7, 1.0, 1.5, 2.0],
        "what": "Multiplier on the per-tile-season sampling SEs projected from the pilot (after the 5 km -> 10 km "
                "block-size scaling estimated from Manavgat and Bejis). >1 covers tiles with far fewer burned "
                "cells than the pilot AOIs (the gate admits >= 100; pilot targets had 539-2,935)."},
    "A5_rho_temporal_spatial": {
        "central": 0.0, "range": [0.0, 0.5],
        "what": "Correlation, across tiles, between a tile's temporal gap and its spatial (target) gap. Enters "
                "V2 - V3 only; positive values shrink its variance, so 0 is the conservative central value."},
    "A6_group_proxy": {
        "central": "pilot thermal-minus-baseline paired delta",
        "what": "Heterogeneity of a predictor group's paired contribution is taken from the pilot's only "
                "group contrast (6 thermal variables added to 4 baseline variables). The new study removes one "
                "of seven groups from a larger stack; its contributions may be smaller and less variable."},
    "A7_df": {
        "central": "t with T - 1 df",
        "what": "Model-based (crossed random-effects) intervals use the GLS variance of the mean at the stated "
                "components and a t quantile with T - 1 df (tile count), not Kenward-Roger. Checked by a REML "
                "plug-in simulation at T = 10."},
    "A8_constant_shift": {
        "central": "additive",
        "what": "Power and equivalence are computed by shifting the simulated null by the true effect (a common "
                "additive effect on every direction/tile; the heterogeneity does not change with the effect)."},
    "A9_pairwise_V3": {
        "central": "pairwise directions",
        "what": "V3 is projected as the mean over the T(T-1) pairwise directions, the only structure the pilot "
                "measures. Pooled leave-one-tile-out V3 averages sources and should be at least as precise."},
}

T_LIST = [8, 10, 12, 15]
S_LIST = [3, 4, 5]
EFFECTS = [0.02, 0.05, 0.10]
MARGINS = [0.02, 0.05]
NSIM = 2000
NBOOT = 1000
NPARBOOT = 1000
N_REML_CHECK = 300


# ----------------------------------------------------------------------------------------------------
# REML for the crossed source x target model with known sampling variances. Two specifications:
#   "crossed"      y_ij = mu + a_i + b_j + d_ij + e_ij                  (the design's s7 model)
#   "crossed_pair" y_ij = mu + a_i + b_j + p_{ij} + d_ij + e_ij         (p shared by i->j and j->i)
# The pair (unordered-dyad) term is added because the pilot's dyadic residuals are strongly reciprocal.
# ----------------------------------------------------------------------------------------------------
COMP = {"crossed": ["source", "target", "dyad"], "crossed_pair": ["source", "target", "pair", "dyad"]}


def design_kernels(src, tgt, R, model="crossed_pair"):
    Zs = np.eye(R)[src]; Zt = np.eye(R)[tgt]
    lo = np.minimum(src, tgt); hi = np.maximum(src, tgt)
    Kp = ((lo[:, None] == lo[None, :]) & (hi[:, None] == hi[None, :])).astype(float)
    K = [Zs @ Zs.T, Zt @ Zt.T]
    if model == "crossed_pair":
        K.append(Kp)
    return K


def build_V(sds, K, se2):
    V = np.diag(sds[-1] ** 2 + se2)
    for sd, k in zip(sds[:-1], K):
        V = V + sd ** 2 * k
    return V


def reml_nll(theta, y, K, se2):
    V = build_V(np.exp(theta), K, se2)
    try:
        L = np.linalg.cholesky(V)
    except np.linalg.LinAlgError:
        return 1e10
    one = np.ones_like(y)
    Vi1 = np.linalg.solve(L.T, np.linalg.solve(L, one))
    Viy = np.linalg.solve(L.T, np.linalg.solve(L, y))
    xtvx = one @ Vi1
    beta = (one @ Viy) / xtvx
    quad = y @ Viy - beta * (one @ Viy)
    return 0.5 * (2.0 * np.log(np.diag(L)).sum() + np.log(xtvx) + quad)


LOWER, UPPER = math.log(1e-4), math.log(0.6)


def reml_fit(y, src, tgt, se2, R, model="crossed_pair", nstart=None):
    K = design_kernels(src, tgt, R, model)
    names = COMP[model]; m = len(names)
    sd0 = max(np.std(y), 1e-3)
    starts = [np.full(m, 0.5)] + [np.where(np.arange(m) == j, 0.9, 0.1) for j in range(m)] + [np.full(m, 0.05)]
    if nstart:
        starts = starts[:nstart]
    best = None
    for f in starts:
        th0 = np.log(np.clip(f * sd0, 1.5e-4, 0.5))
        r = optimize.minimize(reml_nll, th0, args=(y, K, se2), method="L-BFGS-B", bounds=[(LOWER, UPPER)] * m)
        if best is None or r.fun < best.fun:
            best = r
    s = np.exp(best.x)
    s[s < 1.5e-4] = 0.0                                  # boundary -> reported as zero
    V = build_V(s, K, se2)
    Vi = np.linalg.inv(V)
    one = np.ones_like(y)
    xtvx = one @ Vi @ one
    beta = (one @ Vi @ y) / xtvx
    r = y - beta
    out = {"mu": beta, "se_mu": math.sqrt(1.0 / xtvx), "nll": best.fun}
    for nm, sd in zip(names, s):
        out[f"sd_{nm}"] = float(sd)
    out["blup_source"] = s[0] ** 2 * np.eye(R)[src].T @ Vi @ r
    out["blup_target"] = s[1] ** 2 * np.eye(R)[tgt].T @ Vi @ r
    out["blup_dyad"] = s[-1] ** 2 * Vi @ r
    return out


def all_pairs(T):
    pr = [(i, j) for i in range(T) for j in range(T) if i != j]
    return np.array([p[0] for p in pr]), np.array([p[1] for p in pr])


def gls_var_mean(T, cp):
    """Var of the GLS mean over the T(T-1) directions for known components."""
    src, tgt = all_pairs(T)
    K = design_kernels(src, tgt, T, "crossed_pair")
    V = build_V(np.array([cp["sd_s"], cp["sd_t"], cp["sd_p"], cp["sd_d"]]), K, np.full(len(src), cp["se_e"] ** 2))
    one = np.ones(len(src))
    return 1.0 / (one @ np.linalg.solve(V, one))


# ----------------------------------------------------------------------------------------------------
# 1. Pilot variance components
# ----------------------------------------------------------------------------------------------------
def sd_ci_chi2(x):
    x = np.asarray(x, float); n = len(x); s = x.std(ddof=1)
    lo = s * math.sqrt((n - 1) / stats.chi2.ppf(0.975, n - 1))
    hi = s * math.sqrt((n - 1) / stats.chi2.ppf(0.025, n - 1))
    return s, lo, hi


def load_pilot():
    m = pd.read_csv(F_MATRIX)
    b = pd.read_csv(F_BLOCKCI)
    b["source"] = b["direction"].str.split("_to_").str[0].map(SHORT)
    b["target"] = b["direction"].str.split("_to_").str[1].map(SHORT)
    df = m.merge(b[["source", "target", "point_roc_auc", "ci_10cell_lo", "ci_10cell_hi",
                    "ci_2cell_lo_reproduced", "ci_2cell_hi_reproduced", "delta_roc_auc",
                    "delta_ci_10cell_lo", "delta_ci_10cell_hi"]], on=["source", "target"], how="inner")
    assert len(df) == 20, len(df)
    assert np.max(np.abs(df["point_roc_auc"] - df["raw_thermal_roc"])) < 6e-5, "block-CI file != matrix"
    assert np.max(np.abs(df["delta_roc_auc"] - (df["raw_thermal_roc"] - df["raw_baseline_roc"]))) < 6e-5
    df["src_i"] = df["source"].map(REGIONS.index)
    df["tgt_i"] = df["target"].map(REGIONS.index)
    df["se10"] = (df["ci_10cell_hi"] - df["ci_10cell_lo"]) / (2 * Z975)
    df["se2"] = (df["raw_thermal_roc_hi"] - df["raw_thermal_roc_lo"]) / (2 * Z975)
    df["dse10"] = (df["delta_ci_10cell_hi"] - df["delta_ci_10cell_lo"]) / (2 * Z975)
    df["delta"] = df["raw_thermal_roc"] - df["raw_baseline_roc"]
    df["gap"] = df["within_thermal_roc"] - df["raw_thermal_roc"]
    return df


def large_block():
    rows = {}
    for r in ["manavgat_2021", "bejis_2022"]:
        for blk in (10, 20):
            t = pd.read_csv(F_LARGE / r / f"block_{blk}_cells" / "step8c_large_block_bootstrap_summary.csv")
            t = t.set_index("series")
            for s in ("auc_thermal", "auc_baseline", "delta_auc"):
                rows[(r, blk, s)] = ((t.loc[s, "ci_97_5"] - t.loc[s, "ci_2_5"]) / (2 * Z975), t.loc[s, "mean"])
    return rows


def pilot_components(df, rng):
    out = {"inputs": {"matrix": str(F_MATRIX.relative_to(ROOT)), "block_ci": str(F_BLOCKCI.relative_to(ROOT)),
                      "large_block": str(F_LARGE.relative_to(ROOT)), "ladder": str(F_LADDER.relative_to(ROOT)),
                      "loro": str(F_LORO.relative_to(ROOT))}}
    # --- within-region (V1 analogue) ---
    w = df.groupby("target").first()[["within_thermal_roc", "within_baseline_roc",
                                      "within_thermal_roc_lo", "within_thermal_roc_hi"]]
    w["inc"] = w["within_thermal_roc"] - w["within_baseline_roc"]
    lad = json.load(open(F_LADDER))["ladder_by_frame"]["full"]
    inc10 = pd.Series({SHORT[k]: v for k, v in lad["blocked_B10"]["per_region"].items()})
    lb = large_block()
    se_v1_b20 = float(np.mean([lb[(r, 20, "auc_thermal")][0] for r in ("manavgat_2021", "bejis_2022")]))
    se_v1_b10 = float(np.mean([lb[(r, 10, "auc_thermal")][0] for r in ("manavgat_2021", "bejis_2022")]))
    se_inc_b20 = float(np.mean([lb[(r, 20, "delta_auc")][0] for r in ("manavgat_2021", "bejis_2022")]))
    se_inc_b10 = float(np.mean([lb[(r, 10, "delta_auc")][0] for r in ("manavgat_2021", "bejis_2022")]))
    ratio_auc = se_v1_b20 / se_v1_b10
    ratio_inc = se_inc_b20 / se_inc_b10
    se_w2 = ((w["within_thermal_roc_hi"] - w["within_thermal_roc_lo"]) / (2 * Z975)).mean()

    def denoise(sd, se):
        return math.sqrt(max(sd ** 2 - se ** 2, 0.0))

    s, lo, hi = sd_ci_chi2(w["within_thermal_roc"])
    sb, lob, hib = sd_ci_chi2(w["within_baseline_roc"])
    si, loi, hii = sd_ci_chi2(w["inc"])
    si10, loi10, hii10 = sd_ci_chi2(inc10.values)
    out["within_region"] = {
        "per_region_block2": w.round(4).to_dict(orient="index"),
        "increment_block10_per_region": inc10.round(4).to_dict(),
        "sd_within_thermal_auc_block2": {"sd": s, "chi2_95ci": [lo, hi], "n": 5,
                                         "denoised_sd": denoise(s, se_w2), "mean_sampling_se_2cell": se_w2},
        "sd_within_baseline_auc_block2": {"sd": sb, "chi2_95ci": [lob, hib]},
        "sd_within_increment_block2": {"sd": si, "chi2_95ci": [loi, hii]},
        "sd_within_increment_block10": {"sd": si10, "chi2_95ci": [loi10, hii10],
                                        "denoised_sd": denoise(si10, se_inc_b10)},
        "sampling_se_within_auc_block10_mean_man_bej": se_v1_b10,
        "sampling_se_within_auc_block20_mean_man_bej": se_v1_b20,
        "sampling_se_within_increment_block10": se_inc_b10,
        "sampling_se_within_increment_block20": se_inc_b20,
        "se_ratio_block20_over_block10_auc": ratio_auc,
        "se_ratio_block20_over_block10_increment": ratio_inc,
        "note": "Only Manavgat and Bejis have within-region runs at 5 and 10 km blocks; the between-region SD "
                "of within AUC is from 1 km blocks (5 regions). chi2 intervals assume normality, n = 5.",
    }
    # --- sampling SE of a transfer direction ---
    out["direction_sampling_se"] = {
        "auc_se_10cell_median": float(df["se10"].median()),
        "auc_se_10cell_iqr": [float(df["se10"].quantile(.25)), float(df["se10"].quantile(.75))],
        "auc_se_2cell_median": float(df["se2"].median()),
        "ratio_10cell_over_2cell_median": float((df["se10"] / df["se2"]).median()),
        "delta_se_10cell_median": float(df["dse10"].median()),
        "note": "Spatial-block (10 cell ~ 5 km) bootstrap CIs from round3/transfer_ci_blocksize.csv; the 2-cell "
                "CIs in matrix_corrected.csv ignore autocorrelation and are ~3x too narrow.",
    }
    # --- crossed random-effects decomposition ---
    src = df["src_i"].to_numpy(); tgt = df["tgt_i"].to_numpy()
    series = {
        "raw_thermal_auc": (df["raw_thermal_roc"].to_numpy(), df["se10"].to_numpy() ** 2),
        "z_thermal_auc": (df["z_thermal_roc"].to_numpy(), df["se10"].to_numpy() ** 2),
        "coral_thermal_auc": (df["coral_thermal_roc"].to_numpy(), df["se10"].to_numpy() ** 2),
        "raw_baseline_auc": (df["raw_baseline_roc"].to_numpy(), df["se10"].to_numpy() ** 2),
        "delta_thermal_minus_baseline": (df["delta"].to_numpy(), df["dse10"].to_numpy() ** 2),
        "gap_within_minus_transfer": (df["gap"].to_numpy(), df["se10"].to_numpy() ** 2),
    }
    comps = {}
    for name, (y, se2) in series.items():
        comps[name] = {"mean": float(np.mean(y)), "sd_observed": float(np.std(y, ddof=1)),
                       "mean_sampling_var": float(np.mean(se2))}
        for model in ("crossed", "crossed_pair"):
            names = COMP[model]
            fit = reml_fit(y, src, tgt, se2, 5, model)
            sds = np.array([fit[f"sd_{n}"] for n in names])
            L = np.linalg.cholesky(build_V(sds, design_kernels(src, tgt, 5, model), se2))
            bs = []
            for _ in range(NPARBOOT):                      # parametric bootstrap of the components
                f = reml_fit(fit["mu"] + L @ rng.standard_normal(len(y)), src, tgt, se2, 5, model, nstart=3)
                bs.append([f[f"sd_{n}"] for n in names] + [f["se_mu"]])
            bs = np.array(bs)
            loro = {}                                      # leave-one-region-out refits (4 regions, 12 directions)
            for k, r in enumerate(REGIONS):
                keep = (src != k) & (tgt != k)
                remap = {old: new for new, old in enumerate([i for i in range(5) if i != k])}
                f = reml_fit(y[keep], np.array([remap[i] for i in src[keep]]),
                             np.array([remap[i] for i in tgt[keep]]), se2[keep], 4, model)
                loro[r] = {f"sd_{n}": f[f"sd_{n}"] for n in names}
            res = {"mu": float(fit["mu"]), "se_mu": fit["se_mu"], "neg_reml_loglik": float(fit["nll"]),
                   **{f"sd_{n}": fit[f"sd_{n}"] for n in names},
                   "sd_total_heterogeneity": float(np.sqrt((sds ** 2).sum())),
                   "param_boot_95ci": {f"sd_{n}": [float(np.quantile(bs[:, c], .025)),
                                                   float(np.quantile(bs[:, c], .975))] for c, n in enumerate(names)},
                   "param_boot_p80": {f"sd_{n}": float(np.quantile(bs[:, c], .80)) for c, n in enumerate(names)},
                   "param_boot_share_at_zero": {f"sd_{n}": float(np.mean(bs[:, c] == 0))
                                                for c, n in enumerate(names)},
                   "loro_refits": loro,
                   "loro_range": {f"sd_{n}": [min(v[f"sd_{n}"] for v in loro.values()),
                                              max(v[f"sd_{n}"] for v in loro.values())] for n in names},
                   "blup_target": dict(zip(REGIONS, map(float, fit["blup_target"]))),
                   "blup_source": dict(zip(REGIONS, map(float, fit["blup_source"])))}
            if model == "crossed":
                # descriptive SRM correlations from BLUPs (5 regions / 10 dyads: very noisy)
                dmap = {(src[k], tgt[k]): fit["blup_dyad"][k] for k in range(len(y))}
                dd = np.array([[dmap[(i, j)], dmap[(j, i)]] for i in range(5) for j in range(i + 1, 5)])
                res["descriptive_dyadic_reciprocity"] = (float(np.corrcoef(dd[:, 0], dd[:, 1])[0, 1])
                                                         if fit["sd_dyad"] > 0 else None)
                res["descriptive_source_target_corr"] = (
                    float(np.corrcoef(fit["blup_source"], fit["blup_target"])[0, 1])
                    if fit["sd_source"] > 0 and fit["sd_target"] > 0 else None)
            comps[name][model] = res
        comps[name]["lrt_pair_term"] = {
            "stat": 2 * (comps[name]["crossed"]["neg_reml_loglik"] - comps[name]["crossed_pair"]["neg_reml_loglik"]),
            "p_boundary_mixture": float(0.5 * stats.chi2.sf(max(2 * (comps[name]["crossed"]["neg_reml_loglik"]
                                        - comps[name]["crossed_pair"]["neg_reml_loglik"]), 0), 1))}
    out["crossed_re"] = comps
    out["crossed_re_method"] = ("REML implemented directly (scipy L-BFGS-B, multi-start, log-SD bounds [1e-4, 0.6]); "
                                "known sampling variance per direction = (10-cell ~5 km spatial-block CI width / 3.92)^2. "
                                "Two specifications: 'crossed' (source, target, dyad) and 'crossed_pair' (adds an "
                                "unordered-pair effect shared by i->j and j->i). Uncertainty: parametric bootstrap "
                                f"({NPARBOOT} refits from the fitted model) and leave-one-region-out refits.")
    # --- pilot-internal proxy for temporal heterogeneity (label-conditioned scar frame, 5 km blocks) ---
    ps = json.load(open(F_LADDER))["scar_frame"]["B10"]["per_scar"]
    loso = np.array([p["loso_th"] for p in ps]); frn = np.array([p["foreign_th"] for p in ps])
    out["temporal_proxy_scar_frame"] = {
        "n_scars": len(ps), "regions": sorted({p["region"] for p in ps}),
        "loso_thermal_auc_mean": float(loso.mean()), "loso_thermal_auc_sd": float(loso.std(ddof=1)),
        "foreign_thermal_auc_mean": float(frn.mean()), "foreign_thermal_auc_sd": float(frn.std(ddof=1)),
        "sd_ratio_loso_over_foreign": float(loso.std(ddof=1) / frn.std(ddof=1)),
        "caveat": "Another fire in the same region and SAME season, in a label-conditioned frame, 7 scars in 3 "
                  "regions. It is not temporal transfer; it only shows that 'same region, different event' "
                  "is not obviously less variable than 'different region'. Used to motivate k around 1, not to "
                  "estimate it.",
    }
    loro_all = json.load(open(F_LORO))
    lt = [d["roc_auc"] for d in loro_all if d["scaling"] == "raw" and d["feature_set"] == "thermal"]
    out["pooled_loro_check"] = {"raw_thermal_auc_by_target": lt, "sd": float(np.std(lt, ddof=1)),
                                "note": "Pooled leave-one-region-out V3; its SD across targets should be close "
                                        "to the REML target SD (plus sampling) if the target component dominates."}
    return out


# ----------------------------------------------------------------------------------------------------
# 2. Projection
# ----------------------------------------------------------------------------------------------------
def sim_matrix(rng, nsim, T, cp):
    """Direction matrix Y[i, j] (source i, target j) with source, target, unordered-pair, dyad and sampling
    terms; true mean 0 (location shifts are applied afterwards)."""
    a = rng.standard_normal((nsim, T, 1)) * cp["sd_s"]
    b = rng.standard_normal((nsim, 1, T)) * cp["sd_t"]
    p = rng.standard_normal((nsim, T, T)) * cp["sd_p"]
    p = np.triu(p, 1); p = p + np.transpose(p, (0, 2, 1))
    d = rng.standard_normal((nsim, T, T)) * math.sqrt(cp["sd_d"] ** 2 + cp["se_e"] ** 2)
    Y = a + b + p + d
    Y[:, np.arange(T), np.arange(T)] = 0.0
    return Y


def boot_two_way(rng, Y, B):
    """Tile-cluster bootstrap of the mean of a T x T direction matrix: tiles are resampled once and keep
    both roles; directions between two copies of the same tile are dropped. Percentile limits."""
    nsim, T, _ = Y.shape
    est = Y.sum((1, 2)) / (T * (T - 1))
    res = np.empty((nsim, 4))
    for k in range(nsim):
        idx = rng.integers(0, T, (B, T))
        W = (idx[:, :, None] == np.arange(T)).sum(1).astype(float)
        num = ((W @ Y[k]) * W).sum(1)
        den = W.sum(1) ** 2 - (W ** 2).sum(1)
        ok = den > 0
        res[k] = np.quantile(num[ok] / den[ok], [0.025, 0.975, 0.05, 0.95])
    return est, res


def boot_target_only(rng, Y, B):
    """Target-cluster bootstrap: resample target tiles, keep every source (ignores source/pair sharing)."""
    nsim, T, _ = Y.shape
    col = Y.sum(1) / (T - 1)
    return boot_one_way(rng, col, B)


def boot_one_way(rng, X, B):
    nsim, T = X.shape
    est = X.mean(1)
    res = np.empty((nsim, 4))
    for k in range(nsim):
        idx = rng.integers(0, T, (B, T))
        res[k] = np.quantile(X[k][idx].mean(1), [0.025, 0.975, 0.05, 0.95])
    return est, res


def summarise_boot(est, res):
    lo95, hi95, lo90, hi90 = res.T
    out = {"hw95": float(np.mean((hi95 - lo95) / 2)), "sd_estimate": float(np.std(est)),
           "coverage95": float(np.mean((lo95 <= 0) & (hi95 >= 0)))}
    for dlt in EFFECTS:
        out[f"power_{dlt:.2f}"] = float(np.mean((lo95 + dlt > 0) | (hi95 + dlt < 0)))
    for M in MARGINS:
        for dlt in (0.0, 0.02):
            out[f"p_equiv_M{M:.2f}_true{dlt:.2f}"] = float(np.mean((lo90 + dlt > -M) & (hi90 + dlt < M)))
    grid = np.arange(0.0, 0.40001, 0.0005)
    hit = [g for g in grid if np.mean((lo95 + g > 0) | (hi95 + g < 0)) >= 0.8]
    out["mde80"] = float(hit[0]) if hit else None
    return out


def power_t(d, se, df, tc):
    nc = d / se
    if nc > 35:
        return 1.0
    v = stats.nct.sf(tc, df, nc) + stats.nct.cdf(-tc, df, nc)
    return float(v) if np.isfinite(v) else float(stats.norm.sf(tc - nc))


def analytic(var_mean, df):
    se = math.sqrt(var_mean)
    tc = stats.t.ppf(0.975, df); t90 = stats.t.ppf(0.95, df)
    out = {"hw95": tc * se, "sd_estimate": se, "coverage95": None}
    for dlt in EFFECTS:
        out[f"power_{dlt:.2f}"] = power_t(dlt, se, df, tc)
    for M in MARGINS:
        for dlt in (0.0, 0.02):
            hi = (M - t90 * se - dlt) / se; lo = (-M + t90 * se - dlt) / se
            out[f"p_equiv_M{M:.2f}_true{dlt:.2f}"] = float(max(stats.t.cdf(hi, df) - stats.t.cdf(lo, df), 0.0))
    out["mde80"] = float(optimize.brentq(lambda d: power_t(d, se, df, tc) - 0.8, 1e-6, 20 * se))
    return out


def scenario_components(P, T, S, k=1.0, pi=0.5, persist=1.0, g=1.0, rho=0.0, comp_key="reml"):
    """Direction- or tile-level components after season averaging, for every primary contrast.
    Heterogeneity components come from the 'crossed_pair' REML fit (point or parametric-bootstrap p80)."""
    cr = P["crossed_re"]; wr = P["within_region"]; ds = P["direction_sampling_se"]
    names = COMP["crossed_pair"]

    def c(name):
        r = cr[name]["crossed_pair"]
        src = r if comp_key == "reml" else r["param_boot_p80"]
        return [src[f"sd_{n}"] for n in names]

    fs = math.sqrt(persist + (1 - persist) / S)            # SD factor for tile-season heterogeneity
    se_tr = ds["auc_se_10cell_median"] * wr["se_ratio_block20_over_block10_auc"] * g   # one direction-season
    se_dl = ds["delta_se_10cell_median"] * wr["se_ratio_block20_over_block10_increment"] * g
    se_v1 = wr["sampling_se_within_auc_block20_mean_man_bej"] * g
    se_inc = wr["sampling_se_within_increment_block20"] * g

    s3, t3, p3, d3 = c("raw_thermal_auc")
    sg, tg, pg, dg = c("gap_within_minus_transfer")
    sD, tD, pD, dD = c("delta_thermal_minus_baseline")
    spatial_total = math.sqrt(sg ** 2 + tg ** 2 + pg ** 2 + dg ** 2)
    temp_total = k * spatial_total
    v_tile_temp = pi * temp_total ** 2
    v_season_temp = (1 - pi) * temp_total ** 2
    se_12 = math.sqrt(se_v1 ** 2 + se_tr ** 2)              # paired V1 - V2, one tile-season (errors independent)
    w10 = wr["sd_within_increment_block10"]
    inc_tile = w10["denoised_sd"] if comp_key == "reml" else w10["chi2_95ci"][1]

    def dirc(s_, t_, p_, d_, se):
        return {"level": "direction", "sd_s": s_ * fs, "sd_t": t_, "sd_p": p_ * fs, "sd_d": d_ * fs,
                "se_e": se / math.sqrt(S)}

    comps = {
        "mean_V3": dirc(s3, t3 * fs, p3, d3, se_tr),
        "V1_minus_V3": dirc(sg, math.sqrt((tg * fs) ** 2 + se_v1 ** 2 / S), pg, dg, se_tr),
        "V2_minus_V3": dirc(sg, math.sqrt(max((tg * fs) ** 2 + v_tile_temp + (v_season_temp + se_tr ** 2) / S
                                              - 2 * rho * tg * fs * math.sqrt(v_tile_temp), 0.0)), pg, dg, se_tr),
        "group_contribution_V3": dirc(sD, tD * fs, pD, dD, se_dl),
        "V1_minus_V2": {"level": "tile", "sd_tile": math.sqrt(v_tile_temp + (v_season_temp + se_12 ** 2) / S)},
        "group_contribution_V1": {"level": "tile", "sd_tile": math.sqrt(inc_tile ** 2 + se_inc ** 2 / S)},
    }
    comps["_inputs"] = {"se_transfer_direction_season": se_tr, "se_delta_direction_season": se_dl,
                        "se_V1_tile_season": se_v1, "se_increment_tile_season": se_inc,
                        "spatial_gap_total_sd": spatial_total, "temporal_gap_total_sd": temp_total,
                        "increment_tile_sd": inc_tile}
    return comps


def evaluate(rng, comps, T, do_boot=True):
    rows = {}
    for name, cp in comps.items():
        if name.startswith("_"):
            continue
        if cp["level"] == "direction":
            rows[(name, "crossed_RE_model")] = analytic(gls_var_mean(T, cp), T - 1)
            if do_boot:
                Y = sim_matrix(rng, NSIM, T, cp)
                rows[(name, "tile_cluster_bootstrap")] = summarise_boot(*boot_two_way(rng, Y, NBOOT))
                rows[(name, "target_only_bootstrap")] = summarise_boot(*boot_target_only(rng, Y, NBOOT))
        else:
            rows[(name, "tile_RE_model")] = analytic(cp["sd_tile"] ** 2 / T, T - 1)
            if do_boot:
                X = rng.standard_normal((NSIM, T)) * cp["sd_tile"]
                rows[(name, "tile_cluster_bootstrap")] = summarise_boot(*boot_one_way(rng, X, NBOOT))
    return rows


def reml_plugin_check(rng, comps, T, nsim):
    """Fit the crossed model by REML on each simulated matrix (with and without the pair term) and form a
    t(T-1) interval from the plug-in GLS SE: realised coverage and half-width."""
    out = {}
    src, tgt = all_pairs(T)
    tc = stats.t.ppf(0.975, T - 1)
    for name in ("mean_V3", "V1_minus_V3", "group_contribution_V3"):
        cp = comps[name]
        Y = sim_matrix(rng, nsim, T, cp)
        se2 = np.full(len(src), cp["se_e"] ** 2)
        out[name] = {}
        for model in ("crossed_pair", "crossed"):
            hw, cov = [], []
            for k in range(nsim):
                f = reml_fit(Y[k][src, tgt], src, tgt, se2, T, model, nstart=3)
                h = tc * f["se_mu"]; hw.append(h); cov.append(abs(f["mu"]) <= h)
            out[name][model] = {"nsim": nsim, "mean_hw95": float(np.mean(hw)), "coverage95": float(np.mean(cov))}
    return out


def main():
    t0 = time.time()
    rng = np.random.default_rng(SEED)
    df = load_pilot()
    P = pilot_components(df, rng)
    (OUT / "pilot_variance_components.json").write_text(json.dumps(P, indent=1, default=float))
    rows = []
    for name, c in P["crossed_re"].items():
        if not isinstance(c, dict) or "crossed" not in c:
            continue
        for model in ("crossed", "crossed_pair"):
            r = c[model]
            row = {"outcome": name, "model": model, "mean": c["mean"], "sd_observed": c["sd_observed"],
                   "sampling_sd_rms": math.sqrt(c["mean_sampling_var"]), "mu": r["mu"], "se_mu": r["se_mu"],
                   "sd_total_het": r["sd_total_heterogeneity"]}
            for n in COMP[model]:
                row[f"sd_{n}"] = r[f"sd_{n}"]
                row[f"sd_{n}_pb_lo"], row[f"sd_{n}_pb_hi"] = r["param_boot_95ci"][f"sd_{n}"]
                row[f"sd_{n}_loro_min"], row[f"sd_{n}_loro_max"] = r["loro_range"][f"sd_{n}"]
            rows.append(row)
    pd.DataFrame(rows).to_csv(OUT / "pilot_variance_components.csv", index=False, float_format="%.5f")
    print(f"pilot components done {time.time()-t0:.0f}s", flush=True)

    # scenarios: central over T x S; one-at-a-time sensitivities at T = 10, S = 4; k range over T
    scen = [("central", T, S, {}) for T in T_LIST for S in S_LIST]
    sens = [("k=0.5", {"k": 0.5}), ("k=1.5", {"k": 1.5}), ("pi=1.0", {"pi": 1.0}),
            ("persist=0.5", {"persist": 0.5}), ("g=0.7", {"g": 0.7}), ("g=1.5", {"g": 1.5}),
            ("g=2.0", {"g": 2.0}), ("rho=0.5", {"rho": 0.5}),
            ("pessimistic_components_p80", {"comp_key": "p80"}),
            ("pessimistic_p80+k=1.5+g=1.5", {"comp_key": "p80", "k": 1.5, "g": 1.5})]
    scen += [(lab, 10, 4, kw) for lab, kw in sens]
    scen += [(lab, T, 4, kw) for lab, kw in [("k=0.5", {"k": 0.5}), ("k=1.5", {"k": 1.5})] for T in (8, 12, 15)]
    table, scen_inputs = [], {}
    for lab, T, S, kw in scen:
        comps = scenario_components(P, T, S, **kw)
        scen_inputs[f"{lab}|T{T}|S{S}"] = comps
        for (contrast, method), r in evaluate(rng, comps, T).items():
            table.append({"scenario": lab, "T": T, "S": S, "contrast": contrast, "method": method, **r})
        print(f"{lab} T={T} S={S} done {time.time()-t0:.0f}s", flush=True)
    tab = pd.DataFrame(table)
    tab.to_csv(OUT / "precision_table.csv", index=False, float_format="%.4f")
    tab.to_json(OUT / "precision_table.json", orient="records", indent=1)

    check = reml_plugin_check(rng, scenario_components(P, 10, 4), 10, N_REML_CHECK)
    central10 = tab[(tab.scenario == "central") & (tab["T"] == 10) & (tab.S == 4)]
    for name in check:
        a = central10[(central10.contrast == name) & (central10.method == "crossed_RE_model")]["hw95"].iloc[0]
        check[name]["analytic_hw95_known_components"] = float(a)
    res = {"seed": SEED, "nsim": NSIM, "nboot": NBOOT, "nparboot": NPARBOOT, "assumptions": ASSUMPTIONS,
           "scenario_components": scen_inputs, "reml_plugin_check_T10_S4": check,
           "runtime_s": time.time() - t0}
    (OUT / "precision_results.json").write_text(json.dumps(res, indent=1, default=float))
    print(json.dumps(check, indent=1))
    print(f"done {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
