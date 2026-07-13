"""
step10/metrics.py

ROC-AUC / PR-AUC ve univariate (isaretli) AUC yardimcilari.
"""

from __future__ import annotations

import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score


def roc_pr(y_true: np.ndarray, y_prob: np.ndarray) -> dict:
    """Tek-sinif ise None dondurur (AUC tanimsiz)."""
    y_true = np.asarray(y_true)
    y_prob = np.asarray(y_prob, dtype="float64")
    n_pos = int((y_true == 1).sum())
    n_neg = int((y_true == 0).sum())
    if n_pos == 0 or n_neg == 0:
        return {"roc_auc": None, "pr_auc": None, "positive_count": n_pos, "negative_count": n_neg}
    return {
        "roc_auc": float(roc_auc_score(y_true, y_prob)),
        "pr_auc": float(average_precision_score(y_true, y_prob)),
        "positive_count": n_pos,
        "negative_count": n_neg,
    }


def univariate_signed_auc(feature: np.ndarray, y: np.ndarray) -> dict:
    """Tek bir feature'in burned'a karsi ISARETLI ROC-AUC'si.

    AUC 0.5'in altina duserse ozelligin burned ile TERS iliskisi var demektir
    (yon reversal tespiti icin isaret KORUNUR; max(auc, 1-auc) YAPILMAZ).
    NaN feature degerleri o feature icin dislanir.
    """
    feature = np.asarray(feature, dtype="float64")
    y = np.asarray(y)
    mask = np.isfinite(feature)
    n_used = int(mask.sum())
    if n_used == 0:
        return {"auc": None, "n_used": 0, "positive_count": 0, "negative_count": 0}
    f, yy = feature[mask], y[mask]
    n_pos = int((yy == 1).sum())
    n_neg = int((yy == 0).sum())
    if n_pos == 0 or n_neg == 0:
        return {"auc": None, "n_used": n_used, "positive_count": n_pos, "negative_count": n_neg}
    return {
        "auc": float(roc_auc_score(yy, f)),
        "n_used": n_used,
        "positive_count": n_pos,
        "negative_count": n_neg,
    }
