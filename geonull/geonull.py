"""geonull: a predictor-free geographic reference for spatially cross-validated binary maps.

Three numbers can be added to any study that already has cell (or point) coordinates, a 0/1 label, a fold
assignment and out-of-fold scores of its own model:

1. ``null_scores``   the geographic null model of Hijmans (2012): minus the distance from each test cell to the
                     nearest positive cell of its fold's training set. Its AUC is the reference.
2. ``calibrated_auc`` Hijmans' calibrated AUC: positives and negatives of each test fold are paired so that both
                     lie at about the same distance from the training positives, and
                     cAUC = AUC_pairs + 0.5 - max(0.5, AUC_null,pairs).
4. ``standardised_auc`` the AUC within narrow geometric strata of that same distance, averaged over a target
                     distribution of it (by default where the positives are); reported only where the supported
                     strata cover at least 80% of the target. sAUC_c corrects it by the null model's sAUC.
3. ``band_auc``      the fixed out-of-fold scores rescored with the negatives restricted to distance bands from
                     the nearest positive (all positives kept in every band).

Coordinates must be in a metric unit (km by default for the tolerance floor). Only numpy, scipy and scikit-learn
are needed. ``evaluate`` runs all three. check_against_study.py compares them with the study code
(scripts/scaleup/analysis_official.py) on the 31 fires.
"""
from __future__ import annotations

import numpy as np
from scipy.spatial import cKDTree
from sklearn.metrics import roc_auc_score

DEFAULT_BANDS = ((0, 0.5), (0.5, 1), (1, 2), (2, 5), (5, 10), (10, np.inf))


def geometric_strata(first=0.51, ratio=1.33, upto=1000.0):
    """Strata [0, first), then [first * ratio^k, first * ratio^(k+1)), the relative tolerance of the cAUC."""
    e = [0.0, first]
    while e[-1] < upto:
        e.append(e[-1] * ratio)
    e[-1] = np.inf
    return tuple(zip(e[:-1], e[1:]))


DEFAULT_STRATA = geometric_strata()

__all__ = ["auc", "null_scores", "train_positive_distance", "matched_pairs", "calibrated_auc",
           "distance_to_positive", "band_auc", "stratum_auc", "standardised_auc", "geometric_strata", "evaluate",
           "DEFAULT_BANDS", "DEFAULT_STRATA"]


def auc(y, s):
    """ROC AUC over the finite scores; NaN when only one class is left."""
    y, s = np.asarray(y), np.asarray(s, float)
    ok = np.isfinite(s)
    y, s = y[ok], s[ok]
    return np.nan if len(y) == 0 or y.min() == y.max() else float(roc_auc_score(y, s))


def _check(xy, y, folds):
    xy, y = np.asarray(xy, float), np.asarray(y).astype(int)
    if xy.ndim != 2 or len(xy) != len(y):
        raise ValueError("xy must be an (n, d) array with one row per label")
    if set(np.unique(y)) - {0, 1}:
        raise ValueError("y must be 0/1")
    for tr, te in folds:
        if len(np.intersect1d(tr, te)):
            raise ValueError("a fold's training and test indices overlap")
    return xy, y


def train_positive_distance(xy, y, folds):
    """Distance of every test cell to the nearest positive of its fold's training set (NaN if never tested)."""
    xy, y = _check(xy, y, folds)
    d = np.full(len(y), np.nan)
    for tr, te in folds:
        b = np.asarray(tr)[y[tr] == 1]
        if len(b) == 0:
            raise ValueError("a training fold has no positive cell")
        d[te] = cKDTree(xy[b]).query(xy[te])[0]
    return d


def null_scores(xy, y, folds):
    """Out-of-fold scores of the geographic null model (higher = closer to a training positive)."""
    return -train_positive_distance(xy, y, folds)


def matched_pairs(xy, y, folds, tol=0.33, floor=0.51, seed=42):
    """Pairwise distance sampling inside each test fold (Hijmans 2012).

    Each positive, in random order, takes the unused negative whose training-positive distance is closest to its
    own; the pair is kept when the two distances differ by at most ``tol * max(d_positive, floor)``.
    Returns the kept indices (positive, negative, positive, negative, ...).
    """
    dtr = train_positive_distance(xy, y, folds)
    y = np.asarray(y).astype(int)
    rng = np.random.default_rng(seed)
    keep = []
    for _, te in folds:
        te = np.asarray(te)
        pos, neg = te[y[te] == 1], te[y[te] == 0]
        if len(pos) == 0 or len(neg) == 0:
            continue
        order = np.argsort(dtr[neg], kind="stable")
        nd = dtr[neg][order]
        used = np.zeros(len(neg), bool)
        for p in rng.permutation(pos):
            dp = dtr[p]
            j = int(np.searchsorted(nd, dp))
            lo, hi = j - 1, j
            while lo >= 0 and used[lo]:
                lo -= 1
            while hi < len(nd) and used[hi]:
                hi += 1
            cands = [i for i in (lo, hi) if 0 <= i < len(nd)]
            if not cands:
                break
            best = min(cands, key=lambda i: abs(nd[i] - dp))
            if abs(nd[best] - dp) <= tol * max(dp, floor):
                used[best] = True
                keep += [p, neg[order[best]]]
    return np.array(keep, int)


def calibrated_auc(y, score, null, pairs):
    """cAUC = AUC_pairs + 0.5 - max(0.5, AUC_null,pairs) on the matched pairs."""
    y = np.asarray(y)
    a, a0 = auc(y[pairs], np.asarray(score)[pairs]), auc(y[pairs], np.asarray(null)[pairs])
    return {"auc_pairs": a, "auc_null_pairs": a0, "cauc": a + 0.5 - max(0.5, a0),
            "pairs": int(len(pairs) // 2), "positives_kept": float((len(pairs) // 2) / max(1, int(y.sum())))}   # share of all positives in y


def distance_to_positive(xy, y):
    """Distance of every cell to the nearest positive cell (0 for positives); used to define the bands."""
    xy, y = np.asarray(xy, float), np.asarray(y).astype(int)
    return cKDTree(xy[y == 1]).query(xy)[0]


def band_auc(y, score, dist, bands=DEFAULT_BANDS, min_neg=20):
    """AUC of fixed scores with all positives and only the negatives whose ``dist`` falls in each band."""
    y, score, dist = np.asarray(y), np.asarray(score, float), np.asarray(dist, float)
    out = []
    for lo, hi in bands:
        neg = (y == 0) & (dist >= lo) & (dist < hi)
        sel = (y == 1) | neg
        out.append({"band": f"{lo}-{hi}", "negatives": int(neg.sum()),
                    "auc": auc(y[sel], score[sel]) if neg.sum() >= min_neg else np.nan})
    return out


def stratum_auc(y, score, z, strata=DEFAULT_STRATA, min_pos=20, min_neg=20):
    """AUC between the positives and negatives that share a stratum of the covariate z (distance to the nearest
    training positive). Returns one row per stratum with its counts and AUC (NaN when unsupported)."""
    y, score, z = np.asarray(y), np.asarray(score, float), np.asarray(z, float)
    out = []
    for lo, hi in strata:
        s = np.isfinite(z) & (z >= lo) & (z < hi) & np.isfinite(score)
        npos, nneg = int((y[s] == 1).sum()), int((y[s] == 0).sum())
        ok = npos >= min_pos and nneg >= min_neg
        out.append({"stratum": f"{lo}-{hi}", "positives": npos, "negatives": nneg, "supported": ok,
                    "auc": auc(y[s], score[s]) if ok else np.nan})
    return out


def standardised_auc(y, score, z, q=None, strata=DEFAULT_STRATA, min_pos=20, min_neg=20, min_coverage=0.8):
    """Distance-standardised AUC: sum_b q_b AUC_b over the supported strata, renormalised (covariate-adjusted
    AUC in the sense of Janes and Pepe 2009, with z as the covariate).

    q: weights per stratum; default (None) is the distribution of z among the positives. Returns sAUC (NaN when
    the supported strata carry less than min_coverage of q), the coverage and the stratum table.
    """
    rows = stratum_auc(y, score, z, strata, min_pos, min_neg)
    if q is None:
        y_, z_ = np.asarray(y), np.asarray(z, float)
        q = np.array([((y_ == 1) & (z_ >= lo) & (z_ < hi)).sum() for lo, hi in strata], float)
    q = np.asarray(q, float) / np.sum(q)
    sup = np.array([r["supported"] for r in rows])
    cov = float(q[sup].sum())
    a = np.array([r["auc"] for r in rows], float)
    val = float((q[sup] * a[sup]).sum() / cov) if cov > 0 else np.nan
    return {"sauc": val if cov >= min_coverage else np.nan, "sauc_any_coverage": val, "coverage": cov,
            "weights": q.tolist(), "strata": rows}


def evaluate(xy, y, folds, score, bands=DEFAULT_BANDS, tol=0.33, floor=0.51, seed=42, min_neg=20):
    """The three numbers for one study: model and null AUC, cAUC, and band AUCs of model and null."""
    null = null_scores(xy, y, folds)
    pairs = matched_pairs(xy, y, folds, tol, floor, seed)
    dist = distance_to_positive(xy, y)
    tested = np.unique(np.concatenate([np.asarray(te) for _, te in folds]))
    c = calibrated_auc(y, score, null, pairs)
    c["positives_kept"] = c["pairs"] / max(1, int(np.asarray(y)[tested].sum()))   # share of the TEST positives
    z = -null
    sm, sn = standardised_auc(y, score, z), standardised_auc(y, null, z)
    c.update({"sauc_model": sm["sauc"], "sauc_null": sn["sauc"], "sauc_coverage": sm["coverage"],
              "sauc_corrected": sm["sauc"] + 0.5 - max(0.5, sn["sauc"])})
    return {"auc_model": auc(y, score), "auc_null": auc(y, null), **c,
            "bands_model": band_auc(y, score, dist, bands, min_neg),
            "bands_null": band_auc(y, null, dist, bands, min_neg)}
