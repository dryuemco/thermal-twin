"""Tests of geonull with synthetic data whose answer is known. Run: python -m pytest geonull -q"""
import numpy as np
import pytest
from sklearn.model_selection import GroupKFold

import geonull as G


def blob(n_side=60, radius=12, seed=0):
    """A square grid (1 km cells) with one circular burned patch: geography alone separates the classes."""
    r, c = np.mgrid[0:n_side, 0:n_side]
    xy = np.c_[r.ravel(), c.ravel()].astype(float)
    y = (np.hypot(xy[:, 0] - n_side / 2, xy[:, 1] - n_side / 2) < radius).astype(int)
    groups = (xy[:, 0] // 5).astype(int) * 100 + (xy[:, 1] // 5).astype(int)
    folds = list(GroupKFold(5).split(xy, y, groups))
    return xy, y, folds, np.random.default_rng(seed)


def test_null_is_high_on_a_contiguous_patch():
    xy, y, folds, _ = blob()
    assert G.auc(y, G.null_scores(xy, y, folds)) > 0.95


def test_null_never_sees_test_positives():
    xy, y, folds, _ = blob()
    d = G.train_positive_distance(xy, y, folds)
    for tr, te in folds:
        te_pos = te[y[te] == 1]
        # every test positive is at a positive distance (it is not its own training positive)
        assert np.all(d[te_pos] > 0)


def test_matched_pairs_balance_distance_and_null_is_near_half():
    xy, y, folds, _ = blob()
    p = G.matched_pairs(xy, y, folds)
    assert len(p) % 2 == 0 and len(p) > 0
    d = G.train_positive_distance(xy, y, folds)
    dp, dn = d[p[0::2]], d[p[1::2]]
    assert np.all(np.abs(dp - dn) <= 0.33 * np.maximum(dp, 0.51) + 1e-12)
    null = G.null_scores(xy, y, folds)
    assert abs(G.auc(y[p], null[p]) - 0.5) < 0.1


def test_cauc_formula():
    y = np.array([1, 0, 1, 0, 1, 0])
    pairs = np.arange(6)
    score = np.array([0.9, 0.1, 0.8, 0.2, 0.3, 0.7])     # AUC 8/9
    null = np.array([3, 1, 1, 3, 2, 2], float)          # AUC 0.5 -> cAUC = AUC
    r = G.calibrated_auc(y, score, null, pairs)
    assert r["cauc"] == pytest.approx(8 / 9)
    null2 = np.array([3, 1, 3, 1, 3, 1], float)         # AUC 1 -> cAUC = AUC - 0.5
    assert G.calibrated_auc(y, score, null2, pairs)["cauc"] == pytest.approx(8 / 9 - 0.5)


def test_band_assignment_and_min_negatives():
    y = np.array([1, 1, 0, 0, 0, 0])
    dist = np.array([0, 0, 0.2, 0.7, 3.0, 12.0])
    score = np.array([0.9, 0.8, 0.85, 0.1, 0.2, 0.0])
    b = {r["band"]: r for r in G.band_auc(y, score, dist, min_neg=1)}
    assert b["0-0.5"]["negatives"] == 1 and b["0-0.5"]["auc"] == pytest.approx(0.5)
    assert b["0.5-1"]["auc"] == 1.0 and b["10-inf"]["negatives"] == 1
    assert np.isnan(G.band_auc(y, score, dist, min_neg=2)[0]["auc"])


def test_a_model_using_only_noise_has_cauc_near_half():
    xy, y, folds, rng = blob()
    r = G.evaluate(xy, y, folds, rng.random(len(y)))
    assert abs(r["auc_model"] - 0.5) < 0.05 and abs(r["cauc"] - 0.5) < 0.1
    assert r["auc_null"] > 0.95


def test_overlapping_folds_are_refused():
    xy, y, _, _ = blob(20, 5)
    with pytest.raises(ValueError):
        G.null_scores(xy, y, [(np.arange(10), np.arange(5, 15))])


def test_standardised_auc_weights_and_coverage():
    # two strata; model perfect in the first, chance-free reversed in the second
    y = np.r_[np.ones(30), np.zeros(30), np.ones(10), np.zeros(30)]
    z = np.r_[np.full(60, 0.2), np.full(40, 3.0)]
    s = np.r_[np.full(30, 1.0), np.full(30, 0.0), np.full(10, 0.0), np.full(30, 1.0)]
    r = G.standardised_auc(y, s, z, strata=G.DEFAULT_BANDS, min_pos=5, min_neg=5)
    assert r["weights"][0] == pytest.approx(0.75) and r["weights"][3] == pytest.approx(0.25)
    assert r["sauc"] == pytest.approx(0.75)
    r2 = G.standardised_auc(y, s, z, strata=G.DEFAULT_BANDS, min_pos=20, min_neg=5)       # second stratum unsupported, coverage 0.75
    assert r2["coverage"] == pytest.approx(0.75) and np.isnan(r2["sauc"]) and r2["sauc_any_coverage"] == 1.0


def test_null_sauc_near_half_on_a_patch():
    xy, y, folds, _ = blob()
    null = G.null_scores(xy, y, folds)
    r = G.standardised_auc(y, null, -null, min_pos=5, min_neg=5)
    assert G.auc(y, null) > 0.95 and r["coverage"] > 0.95 and abs(r["sauc"] - 0.5) < 0.05
    coarse = G.standardised_auc(y, null, -null, strata=G.DEFAULT_BANDS, min_pos=5, min_neg=5)
    assert coarse["sauc"] > 0.8          # why the strata must be narrow (plan amendment 6.3)


def test_pooled_auc_is_weighted_band_mean():
    xy, y, folds, rng = blob()
    s = rng.random(len(y)) + 0.5 * y
    d = G.distance_to_positive(xy, y)
    b = G.band_auc(y, s, d, min_neg=1)
    w = np.array([r["negatives"] for r in b], float)
    a = np.array([r["auc"] for r in b])
    ok = w > 0
    assert (w[ok] / w[ok].sum() * a[ok]).sum() == pytest.approx(G.auc(y, s), abs=1e-12)
