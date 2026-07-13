"""
step10/spatial_bootstrap.py

Target-bolge tahminleri uzerinde spatial-block bootstrap ile ROC-AUC / PR-AUC
%95 guven araligi. step8c ile ayni mantik: yeniden ORNEKLEME BIRIMI
spatial_block_id'dir (satir DEGIL). Bir blok birden fazla cekilirse tum
satirlari o kadar tekrarlanir. Tek-sinif iterasyonlar atlanir.
"""

from __future__ import annotations

import numpy as np

from sklearn.metrics import average_precision_score, roc_auc_score

from config10 import CI_LOWER, CI_UPPER, N_BOOTSTRAP, SEED
from metrics import roc_pr


def block_bootstrap_ci(
    y: np.ndarray,
    y_prob: np.ndarray,
    block_ids: np.ndarray,
    n_bootstrap: int = N_BOOTSTRAP,
    seed: int = SEED,
) -> dict:
    """spatial_block_id uzerinden bloklari degistirerek ornekleyip her
    iterasyonda ROC-AUC ve PR-AUC hesaplar; 2.5/50/97.5 persentillerini
    dondurur."""
    y = np.asarray(y)
    y_prob = np.asarray(y_prob, dtype="float64")
    block_ids = np.asarray(block_ids)

    unique_blocks = np.unique(block_ids)
    block_to_idx = {b: np.where(block_ids == b)[0] for b in unique_blocks}
    n_blocks = len(unique_blocks)

    rng = np.random.default_rng(seed)
    roc_vals: list[float] = []
    pr_vals: list[float] = []
    n_skipped = 0

    for _ in range(n_bootstrap):
        sampled = rng.choice(unique_blocks, size=n_blocks, replace=True)
        idx = np.concatenate([block_to_idx[b] for b in sampled])
        yb = y[idx]
        if len(np.unique(yb)) < 2:
            n_skipped += 1
            continue
        m = roc_pr(yb, y_prob[idx])
        roc_vals.append(m["roc_auc"])
        pr_vals.append(m["pr_auc"])

    def _ci(vals: list[float]) -> dict:
        if not vals:
            return {"mean": None, "p2_5": None, "p50": None, "p97_5": None}
        arr = np.asarray(vals, dtype="float64")
        lo, med, hi = np.percentile(arr, [CI_LOWER, 50.0, CI_UPPER])
        return {
            "mean": float(arr.mean()),
            "p2_5": float(lo),
            "p50": float(med),
            "p97_5": float(hi),
        }

    return {
        "n_bootstrap_requested": n_bootstrap,
        "n_bootstrap_successful": len(roc_vals),
        "n_bootstrap_skipped": n_skipped,
        "n_blocks": int(n_blocks),
        "roc_auc": _ci(roc_vals),
        "pr_auc": _ci(pr_vals),
        "roc_auc_ci95": [_ci(roc_vals)["p2_5"], _ci(roc_vals)["p97_5"]],
        "pr_auc_ci95": [_ci(pr_vals)["p2_5"], _ci(pr_vals)["p97_5"]],
    }


def delta_block_bootstrap_ci(
    y: np.ndarray,
    prob_baseline: np.ndarray,
    prob_thermal: np.ndarray,
    block_ids: np.ndarray,
    n_bootstrap: int = N_BOOTSTRAP,
    seed: int = SEED,
) -> dict:
    """step8c ile ayni mantik: her bootstrap iterasyonunda spatial bloklar
    degistirilerek ornekelenir; ayni ornek uzerinde delta_auc = AUC(thermal) -
    AUC(baseline) ve delta_pr_auc hesaplanir. delta metriklerinin %95 CI'si ve
    P(delta>0) dondurulur. Tek-sinif iterasyonlar atlanir."""
    y = np.asarray(y)
    pb = np.asarray(prob_baseline, dtype="float64")
    pt = np.asarray(prob_thermal, dtype="float64")
    block_ids = np.asarray(block_ids)

    # OOF NaN olan satirlari dis birak (her satir bir folddan tahmin almali).
    valid = np.isfinite(pb) & np.isfinite(pt)
    y, pb, pt, block_ids = y[valid], pb[valid], pt[valid], block_ids[valid]

    unique_blocks = np.unique(block_ids)
    block_to_idx = {b: np.where(block_ids == b)[0] for b in unique_blocks}
    n_blocks = len(unique_blocks)

    rng = np.random.default_rng(seed)
    d_auc: list[float] = []
    d_pr: list[float] = []
    n_skipped = 0

    for _ in range(n_bootstrap):
        sampled = rng.choice(unique_blocks, size=n_blocks, replace=True)
        idx = np.concatenate([block_to_idx[b] for b in sampled])
        yb = y[idx]
        if len(np.unique(yb)) < 2:
            n_skipped += 1
            continue
        auc_b = roc_auc_score(yb, pb[idx])
        auc_t = roc_auc_score(yb, pt[idx])
        pr_b = average_precision_score(yb, pb[idx])
        pr_t = average_precision_score(yb, pt[idx])
        d_auc.append(float(auc_t - auc_b))
        d_pr.append(float(pr_t - pr_b))

    def _ci(vals: list[float]) -> dict:
        if not vals:
            return {"mean": None, "p2_5": None, "p50": None, "p97_5": None, "prob_gt_0": None}
        arr = np.asarray(vals, dtype="float64")
        lo, med, hi = np.percentile(arr, [CI_LOWER, 50.0, CI_UPPER])
        return {
            "mean": float(arr.mean()),
            "p2_5": float(lo),
            "p50": float(med),
            "p97_5": float(hi),
            "prob_gt_0": float((arr > 0).mean()),
        }

    da, dp = _ci(d_auc), _ci(d_pr)

    def _interp(ci: dict) -> str:
        if ci["p2_5"] is None:
            return "unavailable"
        if ci["p2_5"] > 0:
            return "positive_bootstrap_support"
        if ci["p97_5"] < 0:
            return "negative_bootstrap_support"
        return "uncertain_ci_overlaps_zero"

    return {
        "n_bootstrap_requested": n_bootstrap,
        "n_bootstrap_successful": len(d_auc),
        "n_bootstrap_skipped": n_skipped,
        "n_blocks": int(n_blocks),
        "delta_auc": da,
        "delta_pr_auc": dp,
        "delta_auc_ci95": [da["p2_5"], da["p97_5"]],
        "delta_pr_auc_ci95": [dp["p2_5"], dp["p97_5"]],
        "delta_auc_interpretation": _interp(da),
        "delta_pr_auc_interpretation": _interp(dp),
    }
