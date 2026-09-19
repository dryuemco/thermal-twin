"""Shared definitions for the EMS-round evaluation-geometry analyses (ems_geometry_*.py).

Every definition here is copied from an existing script, named at each item, so the
new analyses use the paper's model, folds, scar, collar and distance conventions and
nothing re-invented. Spec: paper/ems_analyses/geometry/SPEC.md.
"""
from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import ndimage, stats
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _canonical as C  # noqa: E402

PAPER = HERE.parent
OUT = PAPER / "ems_analyses" / "geometry"
# Re-run redirection (labelfix re-run, 2026-09-19); defaults unchanged. PAPER_ARTEFACTS: where the
# paper/code artefacts read below live; EMS_OUT_ROOT: output root (…/geometry). Relative to the tree root.
if os.environ.get("PAPER_ARTEFACTS"):
    PAPER = HERE.parent.parent / os.environ["PAPER_ARTEFACTS"]
if os.environ.get("EMS_OUT_ROOT"):
    OUT = HERE.parent.parent / os.environ["EMS_OUT_ROOT"] / "geometry"
OUT.mkdir(parents=True, exist_ok=True)

REGIONS = ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended", "montiferru_2021"]
BASELINE = list(C.BASELINE)
THERMAL = list(C.THERMAL)
NUMERIC = [f for f in THERMAL if f != "landcover_dominant"]
CAT = "landcover_dominant"
SEED = 42
N_JOBS = 4
# pool_decomposition.py / scar_increment.py / frozen_mugla_verify_aoi_transfer.py
KM, BUF, MIN_SCAR = 0.45, 2, 50
DIL_IT = max(1, round(BUF / KM))          # = 4
# distance_curve.py
CELL_DEG, M_PER_DEG = 0.0045814, 111319.49
BBOX = {
    "manavgat_2021": (31.05, 36.72, 31.85, 37.35),
    "bejis_2022": (-1.05, 39.68, -0.35, 40.15),
    "mugla_2021": (27.10, 36.60, 28.90, 37.45),
    "evia_2021_extended": (23.05, 38.55, 23.85, 39.15),
    "montiferru_2021": (8.45, 40.05, 8.75, 40.27),
}


def build(feats):
    """scar_increment.py::build, n_jobs=4."""
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


def fit(feats, X, y):
    C.assert_no_leakage(feats)
    return build(feats).fit(X[feats], y)


class Region:
    """Population table plus its grid geometry. Grid arrays are indexed [row, col]
    relative to the full parquet's minimum row/col (the full table is a complete
    rectangle, checked below)."""

    def __init__(self, reg):
        self.name = reg
        full = C.load(reg)
        r0, c0 = int(full.row_500m.min()), int(full.col_500m.min())
        self.H = int(full.row_500m.max()) - r0 + 1
        self.W = int(full.col_500m.max()) - c0 + 1
        assert len(full) == self.H * self.W, "grid not rectangular"
        # edge mask: every burned cell in the label map, any population (SPEC Analysis 1)
        self.edge_mask = np.zeros((self.H, self.W), bool)
        fb = full[full.burned == 1]
        self.edge_mask[fb.row_500m.to_numpy().astype(int) - r0, fb.col_500m.to_numpy().astype(int) - c0] = True
        d = full[(full.valid_for_modeling == True) &  # noqa: E712
                 (full.burnable_tree_shrub_grass == True)].reset_index(drop=True)  # noqa: E712
        self.df = d
        self.rr = d.row_500m.to_numpy().astype(int) - r0
        self.cc = d.col_500m.to_numpy().astype(int) - c0
        self.y = d.burned.to_numpy().astype(int)
        self.pop_grid = np.zeros((self.H, self.W), bool)
        self.pop_grid[self.rr, self.cc] = True
        self.burn_grid = np.zeros((self.H, self.W), bool)       # population burned cells
        self.burn_grid[self.rr[self.y == 1], self.cc[self.y == 1]] = True
        # collar distance: frozen_mugla_verify_aoi_transfer.py (isotropic, 0.45 km/cell)
        self.dist_collar = ndimage.distance_transform_edt(~self.burn_grid)[self.rr, self.cc] * KM
        # band distance: distance_curve.py convention (anisotropic)
        lat = (BBOX[reg][1] + BBOX[reg][3]) / 2
        km_ns = CELL_DEG * M_PER_DEG / 1000.0
        km_ew = km_ns * math.cos(math.radians(lat))
        self.km_ns, self.km_ew = km_ns, km_ew
        self.dist_band = ndimage.distance_transform_edt(~self.burn_grid, sampling=(km_ns, km_ew))[self.rr, self.cc]
        self.block10 = (d.row_500m // 10).astype(str) + "_" + (d.col_500m // 10).astype(str)
        self.block10_codes = pd.factorize(self.block10)[0]

    # ---------------------------------------------------------------- scars
    def scars(self):
        """pool_decomposition.py: 8-connected components >= 50 cells, dilated 4x (cross)."""
        lab, _ = ndimage.label(self.burn_grid.astype(np.uint8), structure=np.ones((3, 3)))
        cl = lab[self.rr, self.cc]
        sizes = pd.Series(cl[self.y == 1]).value_counts()
        out = []
        for s in [int(x) for x in sizes[sizes >= MIN_SCAR].index if x != 0]:
            comp = lab == s
            held_grid = ndimage.binary_dilation(comp, iterations=DIL_IT)
            held = held_grid[self.rr, self.cc]
            if len(np.unique(self.y[held])) < 2:
                continue
            out.append({"scar": s, "comp": comp, "held": held, "size": int(comp.sum())})
        return out


def oof_row_a(R: Region, feats=None):
    """pool_decomposition.py: blocked 5-fold OOF, 10-cell blocks. Cached."""
    feats = feats or THERMAL
    tag = "thermal" if feats == THERMAL else "baseline"
    cache = OUT / "cache" / f"oof_{R.name}_{tag}.npy"
    if cache.exists():
        return np.load(cache)
    cache.parent.mkdir(exist_ok=True)
    df = R.df
    oof = np.full(len(df), np.nan)
    for tr_i, te_i in StratifiedGroupKFold(5, shuffle=True, random_state=SEED).split(
            df[feats], df.burned, groups=R.block10):
        oof[te_i] = fit(feats, df.iloc[tr_i], df.iloc[tr_i].burned).predict_proba(df.iloc[te_i][feats])[:, 1]
    np.save(cache, oof)
    return oof


def fold_ids(R: Region):
    f = np.full(len(R.df), -1)
    for k, (_, te_i) in enumerate(StratifiedGroupKFold(5, shuffle=True, random_state=SEED).split(
            R.df[THERMAL], R.df.burned, groups=R.block10)):
        f[te_i] = k
    return f


# ---------------------------------------------------------------- intervals
def block_boot(y, s, blocks, fn, B=1000, seed=SEED):
    """10-cell spatial-block bootstrap of fn(y, s). Returns (lo, hi, n_used)."""
    y, s, blocks = np.asarray(y), np.asarray(s), np.asarray(blocks)
    ub, inv = np.unique(blocks, return_inverse=True)
    members = [np.where(inv == i)[0] for i in range(len(ub))]
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(B):
        pick = rng.integers(0, len(ub), len(ub))
        idx = np.concatenate([members[i] for i in pick])
        yy = y[idx]
        if yy.min() == yy.max():
            continue
        vals.append(fn(yy, s[idx]))
    if len(vals) < 10:
        return np.nan, np.nan, len(vals)
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5)), len(vals)


def t_ci(v):
    v = np.asarray([x for x in v if np.isfinite(x)], float)
    n = len(v)
    if n < 2:
        return float(v.mean()) if n else np.nan, np.nan, np.nan, n
    h = stats.t.ppf(0.975, n - 1) * v.std(ddof=1) / np.sqrt(n)
    return float(v.mean()), float(v.mean() - h), float(v.mean() + h), n


def region_cluster_ci(values, regions):
    """Student t over region means of per-scar values."""
    s = pd.Series(values, index=regions).groupby(level=0).mean()
    return t_ci(s.to_numpy())


def pair_cluster_ci(delta: dict, B=20000, seed=SEED):
    """Appendix A(o): resample unordered region pairs, both directions together."""
    pairs = {}
    for (s, t), v in delta.items():
        pairs.setdefault(tuple(sorted((s, t))), []).append(v)
    keys = list(pairs)
    arr = [np.array(pairs[k]) for k in keys]
    rng = np.random.default_rng(seed)
    means = np.empty(B)
    for b in range(B):
        pick = rng.integers(0, len(keys), len(keys))
        means[b] = np.concatenate([arr[i] for i in pick]).mean()
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def target_cluster_ci(delta: dict, B=20000, seed=SEED):
    groups = {}
    for (s, t), v in delta.items():
        groups.setdefault(t, []).append(v)
    keys = list(groups)
    arr = [np.array(groups[k]) for k in keys]
    rng = np.random.default_rng(seed)
    means = np.empty(B)
    for b in range(B):
        pick = rng.integers(0, len(keys), len(keys))
        means[b] = np.concatenate([arr[i] for i in pick]).mean()
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


# ---------------------------------------------------------------- metrics
def auc(y, s):
    y = np.asarray(y)
    if y.min() == y.max():
        return np.nan
    return float(roc_auc_score(y, s))


def capture(y, s, q):
    y, s = np.asarray(y), np.asarray(s)
    k = int(math.ceil(q * len(y)))
    order = np.argsort(-s, kind="stable")
    return float(y[order[:k]].sum() / max(y.sum(), 1))


def metric_set(y, s):
    y, s = np.asarray(y), np.asarray(s)
    pi = float(y.mean())
    out = {"n": int(len(y)), "positives": int(y.sum()), "prevalence": pi, "auc": auc(y, s)}
    if y.min() == y.max():
        return out
    ap = float(average_precision_score(y, s))
    out.update(ap=ap, ap_lift=ap / pi, pauc01=float(roc_auc_score(y, s, max_fpr=0.1)))
    for q in (0.1, 0.2):
        c = capture(y, s, q)
        ceil = min(1.0, q / pi)
        out[f"cap{int(q*100)}"] = c
        out[f"cap{int(q*100)}_norm"] = (c - q) / (ceil - q) if ceil > q else np.nan
    return out


def dump(obj, name):
    def conv(o):
        if isinstance(o, (np.floating,)):
            return None if not np.isfinite(o) else float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, float) and not np.isfinite(o):
            return None
        raise TypeError(type(o))
    txt = json.dumps(obj, indent=1, default=conv, allow_nan=True).replace("NaN", "null")
    (OUT / name).write_text(txt, encoding="utf-8")


def load_regions():
    return {r: Region(r) for r in REGIONS}
