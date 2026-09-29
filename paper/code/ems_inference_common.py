"""Shared pieces for the EMS-round inference analyses (paper/ems_analyses/inference).

Everything here is copied from existing paper/code scripts so that model, folds, scar definition
and collar are identical to the published arms:
  build()          scar_increment.py / verify_collar_increment.py (n_jobs lowered to 4)
  load()           verify_collar_increment.py, but reading via _canonical.load (SHA-verified)
  scars()          scar_increment.py / verify_matched.py
  blocked_oof()    verify_matched.py / verify_collar_increment.py
"""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import ndimage
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

import _canonical as C

REGIONS = list(C.REGIONS)
BASELINE, THERMAL = C.BASELINE, C.THERMAL
CAT = "landcover_dominant"
CELL_KM, SEED, BUF_KM, MIN_SCAR = 0.45, 42, 2, 50
N_JOBS = 4
PAPER = Path(__file__).resolve().parents[1]
OUTDIR = PAPER / "ems_analyses" / "inference"
# Re-run redirection (labelfix re-run, 2026-09-19); defaults unchanged. PAPER_ARTEFACTS: where the
# paper-level inputs live; EMS_OUT_ROOT: output root (…/inference). Relative to the tree root.
if os.environ.get("PAPER_ARTEFACTS"):
    PAPER = Path(__file__).resolve().parents[2] / os.environ["PAPER_ARTEFACTS"]
if os.environ.get("EMS_OUT_ROOT"):
    OUTDIR = Path(__file__).resolve().parents[2] / os.environ["EMS_OUT_ROOT"] / "inference"
    OUTDIR.mkdir(parents=True, exist_ok=True)
SHORT = {"manavgat_2021": "Manavgat", "bejis_2022": "Bejis", "mugla_2021": "Mugla",
         "evia_2021_extended": "Evia", "montiferru_2021": "Montiferru"}


def build(feats):
    C.assert_no_leakage(feats)
    num = [f for f in feats if f != CAT]
    tr = [("num", Pipeline([("imputer", SimpleImputer(strategy="median"))]), num)]
    if CAT in feats:
        tr.append(("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                                    ("onehot", OneHotEncoder(handle_unknown="ignore"))]), [CAT]))
    return Pipeline([("preprocess", ColumnTransformer(tr)),
                     ("clf", RandomForestClassifier(n_estimators=300, min_samples_leaf=3,
                                                    class_weight="balanced",
                                                    random_state=SEED, n_jobs=N_JOBS))])


def fit(feats, df):
    C.assert_no_leakage(feats)
    return build(feats).fit(df[feats], df.burned)


def load(r):
    cols = ["burned", "valid_for_modeling", "burnable_tree_shrub_grass",
            "row_500m", "col_500m"] + THERMAL
    d = C.load(r, columns=cols)
    d = d[(d.valid_for_modeling == True) &  # noqa: E712
          (d.burnable_tree_shrub_grass == True)].reset_index(drop=True)  # noqa: E712
    r0, c0 = int(d.row_500m.min()), int(d.col_500m.min())
    H = int(d.row_500m.max()) - r0 + 1
    W = int(d.col_500m.max()) - c0 + 1
    rr = d.row_500m.to_numpy().astype(int) - r0
    cc = d.col_500m.to_numpy().astype(int) - c0
    bg = np.ones((H, W), dtype=bool)
    b = d.burned.to_numpy() == 1
    bg[rr[b], cc[b]] = False
    d["dist_km"] = ndimage.distance_transform_edt(bg)[rr, cc] * CELL_KM
    return d


def scars(df):
    """Yield (scar_label, held_mask) exactly as scar_increment.py."""
    r0, c0 = df.row_500m.min(), df.col_500m.min()
    H, W = int(df.row_500m.max() - r0) + 1, int(df.col_500m.max() - c0) + 1
    g = np.zeros((H, W), np.uint8)
    rr = (df.row_500m - r0).to_numpy().astype(int)
    cc = (df.col_500m - c0).to_numpy().astype(int)
    g[rr[df.burned == 1], cc[df.burned == 1]] = 1
    lab, _ = ndimage.label(g, structure=np.ones((3, 3)))
    cl = lab[rr, cc]
    sizes = pd.Series(cl[df.burned.to_numpy() == 1]).value_counts()
    for s in [int(x) for x in sizes[sizes >= MIN_SCAR].index if x != 0]:
        m = np.zeros_like(g)
        m[lab == s] = 1
        held = ndimage.binary_dilation(m, iterations=max(1, round(BUF_KM / CELL_KM)))[rr, cc]
        yield s, held


def blocked_oof(d, feats, B):
    C.assert_no_leakage(feats)
    g = (d.row_500m // B).astype(str) + "_" + (d.col_500m // B).astype(str)
    oof = np.full(len(d), np.nan)
    for tr_i, te_i in StratifiedGroupKFold(5, shuffle=True, random_state=SEED).split(
            d[feats], d.burned, groups=g):
        oof[te_i] = fit(feats, d.iloc[tr_i]).predict_proba(d.iloc[te_i][feats])[:, 1]
    return oof


# ----------------------------------------------------------------- small-sample statistics
from scipy import stats as _st  # noqa: E402


def t_ci(x, level=0.95):
    x = np.asarray(x, float)
    n = len(x)
    m = x.mean()
    if n < 2:
        return m, np.nan, np.nan
    h = _st.t.ppf(0.5 + level / 2, n - 1) * x.std(ddof=1) / np.sqrt(n)
    return m, m - h, m + h


def cr1_ci(x, clusters, level=0.95):
    """Cluster-robust (CR1) interval on the unit-weighted mean, t with G-1 df."""
    x = np.asarray(x, float)
    cl = np.asarray(clusters)
    n = len(x)
    m = x.mean()
    e = x - m
    gs = np.unique(cl)
    G = len(gs)
    if G < 2:
        return m, np.nan, np.nan, np.nan
    v = G / (G - 1) * sum(e[cl == g].sum() ** 2 for g in gs) / n ** 2
    h = _st.t.ppf(0.5 + level / 2, G - 1) * np.sqrt(v)
    return m, m - h, m + h, float(np.sqrt(v))


def cluster_boot_ci(x, clusters, R=20000, seed=SEED, level=0.95):
    x = np.asarray(x, float)
    cl = np.asarray(clusters)
    gs = np.unique(cl)
    idx = [np.where(cl == g)[0] for g in gs]
    rng = np.random.default_rng(seed)
    out = np.empty(R)
    for b in range(R):
        pick = rng.integers(0, len(gs), len(gs))
        ii = np.concatenate([idx[k] for k in pick])
        out[b] = x[ii].mean()
    a = (1 - level) / 2
    return x.mean(), float(np.percentile(out, 100 * a)), float(np.percentile(out, 100 * (1 - a)))
