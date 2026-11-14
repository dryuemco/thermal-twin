"""analysis_official.py: claims 1 and 2 of docs/scaleup/ANALYSIS_PLAN.md on the official scale-up outputs.

Claim 1  geographic null model (Hijmans 2012) against RF and HGB at 5, 10 and 20 km blocks, PR-AUC,
         calibrated AUC by pairwise distance sampling, buffered validation (Ploton et al. 2020).
Claim 2  fixed out-of-fold predictions re-scored on disjoint distance bands of the unburned cells,
         plus an environmental-distance version and landscape heterogeneity per band.

Reproduction gates (stop on failure): band AUC of the five paper regions against
paper/labelfix_rerun/geometry/a1_band_auc.csv (k = 0) within 0.0015; raw transfer among them against
Supplementary Table S8 within 0.002.

Run:  <venv-step10>/python analysis_official.py [--fires a,b,c]   (writes D:/ThermalTwin/scaleup/analysis)
"""
import argparse
import json
import math
import os
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from scipy import ndimage, stats
from scipy.spatial import cKDTree
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
REPO = Path(__file__).resolve().parents[2]
# THERMAL_TWIN_PAPER: the paper/ folder of the main branch (paper/code/_canonical.py and the frozen reference values);
# THERMAL_TWIN_SCALEUP: the run folder (worker clones w1..w3 with their outputs, analysis/ for results)
PAPER = Path(os.environ["THERMAL_TWIN_PAPER"])
SCALEUP = Path(os.environ["THERMAL_TWIN_SCALEUP"])
sys.path.insert(0, str(PAPER / "code"))
sys.path.insert(0, str(REPO))
import _canonical as C  # noqa: E402
from core import regions  # noqa: E402

OUT = SCALEUP / "analysis"
CACHE = OUT / "cache"
CACHE.mkdir(parents=True, exist_ok=True)

PAPER_REGIONS = ["manavgat_2021", "bejis_2022", "mugla_2021", "evia_2021_extended", "montiferru_2021"]
NAME = {"manavgat_2021": "Manavgat", "bejis_2022": "Bejís", "mugla_2021": "Muğla",
        "evia_2021_extended": "Evia", "montiferru_2021": "Montiferru"}
BBOX = {"manavgat_2021": (31.05, 36.72, 31.85, 37.35), "bejis_2022": (-1.05, 39.68, -0.35, 40.15),
        "mugla_2021": (27.10, 36.60, 28.90, 37.45), "evia_2021_extended": (23.05, 38.55, 23.85, 39.15),
        "montiferru_2021": (8.45, 40.05, 8.75, 40.27)}
BASELINE, THERMAL = list(C.BASELINE), list(C.THERMAL)
CAT = "landcover_dominant"
NUM = [f for f in THERMAL if f != CAT]
SEED, N_JOBS = 42, 30
CELL_DEG, M_PER_DEG = 0.0045814, 111319.49
BLOCKS = (10, 20, 40)                      # cells: about 5, 10, 20 km
BANDS = [(0, 0.5), (0.5, 1), (1, 2), (2, 5), (5, 10), (10, np.inf)]
BAND_NAMES = [f"{lo}-{hi}" for lo, hi in BANDS]
BUFFERS_KM = (0, 1, 2, 5, 10)
PWD_TOL, PWD_FLOOR_KM = 0.33, 0.51
MIN_BAND_NEG, MIN_TRAIN_POS, NBOOT = 20, 30, 2000
EXCLUDE_MISSING = ["px20_2021", "px12_2022", "px26_2021", "px03_2022"]   # plan section 1


def build(feats, kind="rf"):
    C.assert_no_leakage(feats)
    num = [f for f in feats if f != CAT]
    if kind == "rf":
        tr = [("num", Pipeline([("imputer", SimpleImputer(strategy="median"))]), num)]
        if CAT in feats:
            tr.append(("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                                        ("onehot", OneHotEncoder(handle_unknown="ignore"))]), [CAT]))
        return Pipeline([("preprocess", ColumnTransformer(tr)),
                         ("clf", RandomForestClassifier(n_estimators=300, min_samples_leaf=3, class_weight="balanced",
                                                        random_state=SEED, n_jobs=N_JOBS))])
    assert kind == "hgb"
    return HistGradientBoostingClassifier(max_iter=300, learning_rate=0.1, class_weight="balanced",
                                          categorical_features=[feats.index(CAT)] if CAT in feats else None,
                                          early_stopping=False, random_state=SEED)


def prep(df, feats, kind):
    if kind == "hgb" and CAT in feats:
        X = df[feats].copy()
        X[CAT] = X[CAT].fillna(-1).astype(int).replace(-1, np.nan)
        return X
    return df[feats]


def auc(y, s):
    y, s = np.asarray(y), np.asarray(s, float)
    ok = np.isfinite(s)
    y, s = y[ok], s[ok]
    return np.nan if len(y) == 0 or y.min() == y.max() else float(roc_auc_score(y, s))


def ap(y, s):
    y, s = np.asarray(y), np.asarray(s, float)
    ok = np.isfinite(s)
    y, s = y[ok], s[ok]
    return np.nan if len(y) == 0 or y.min() == y.max() else float(average_precision_score(y, s))


class Fire:
    def __init__(self, fid, full, lat, meta):
        self.id, self.meta = fid, meta
        r0, c0 = int(full.row_500m.min()), int(full.col_500m.min())
        H, W = int(full.row_500m.max()) - r0 + 1, int(full.col_500m.max()) - c0 + 1
        d = full[(full.valid_for_modeling == True) &  # noqa: E712
                 (full.burnable_tree_shrub_grass == True)].reset_index(drop=True)  # noqa: E712
        self.df = d
        self.rr = d.row_500m.to_numpy().astype(int) - r0
        self.cc = d.col_500m.to_numpy().astype(int) - c0
        self.y = d.burned.to_numpy().astype(int)
        grid = np.zeros((H, W), bool)
        grid[self.rr[self.y == 1], self.cc[self.y == 1]] = True
        km_ns = CELL_DEG * M_PER_DEG / 1000.0
        km_ew = km_ns * math.cos(math.radians(lat))
        self.dist = ndimage.distance_transform_edt(~grid, sampling=(km_ns, km_ew))[self.rr, self.cc]
        self.xy = np.c_[self.rr * km_ns, self.cc * km_ew]
        self.n, self.nb = len(d), int(self.y.sum())
        self.missing_any = float(d[NUM].isna().any(axis=1).mean())

    def blocks(self, k):
        d = self.df
        return ((d.row_500m // k).astype(int).astype(str) + "_" + (d.col_500m // k).astype(int).astype(str)).to_numpy()

    def folds(self, k):
        return list(StratifiedGroupKFold(5, shuffle=True, random_state=SEED).split(self.df[THERMAL], self.df.burned,
                                                                                   groups=self.blocks(k)))

    def _cache(self, tag):
        return CACHE / f"{self.id}_{tag}_{self.n}_{self.nb}.npy"

    def oof(self, feats, fs, kind, k):
        c = self._cache(f"{fs}_{kind}_b{k}")
        if c.exists():
            return np.load(c)
        o = np.full(self.n, np.nan)
        for tr, te in self.folds(k):
            m = build(feats, kind).fit(prep(self.df.iloc[tr], feats, kind), self.df.burned.iloc[tr])
            o[te] = m.predict_proba(prep(self.df.iloc[te], feats, kind))[:, 1]
        np.save(c, o)
        return o

    def null_oof(self, k):
        o = np.full(self.n, np.nan)
        for tr, te in self.folds(k):
            b = tr[self.y[tr] == 1]
            o[te] = -cKDTree(self.xy[b]).query(self.xy[te])[0]
        return o

    def train_pos_dist(self, k):
        """Distance of every cell to the nearest burned cell of its fold's training set."""
        d = np.full(self.n, np.nan)
        for tr, te in self.folds(k):
            b = tr[self.y[tr] == 1]
            d[te] = cKDTree(self.xy[b]).query(self.xy[te])[0]
        return d

    def pwd_pairs(self, k):
        """Pairwise distance sampling (Hijmans 2012) inside each test fold; returns the kept cell indices."""
        dtr = self.train_pos_dist(k)
        rng = np.random.default_rng(SEED)
        keep = []
        for _, te in self.folds(k):
            pos = te[self.y[te] == 1]
            neg = te[self.y[te] == 0]
            if len(pos) == 0 or len(neg) == 0:
                continue
            order = np.argsort(dtr[neg], kind="stable")
            nd = dtr[neg][order]
            used = np.zeros(len(neg), bool)
            for p in rng.permutation(pos):
                dp = dtr[p]
                j = int(np.searchsorted(nd, dp))
                lo, hi, best = j - 1, j, -1
                while lo >= 0 and used[lo]:
                    lo -= 1
                while hi < len(nd) and used[hi]:
                    hi += 1
                cands = [i for i in (lo, hi) if 0 <= i < len(nd)]
                if not cands:
                    break
                best = min(cands, key=lambda i: abs(nd[i] - dp))
                if abs(nd[best] - dp) <= PWD_TOL * max(dp, PWD_FLOOR_KM):
                    used[best] = True
                    keep += [p, neg[order[best]]]
        return np.array(keep, int)

    def buffered_oof(self, b_km, k=10):
        """THERMAL RF and null with training cells within b_km of any test cell removed (5 km block folds)."""
        c = self._cache(f"buffer{b_km}_b{k}")
        if c.exists():
            arr = np.load(c)
            return arr[0], arr[1], int(arr[2, 0])
        o_rf, o_null, skipped = np.full(self.n, np.nan), np.full(self.n, np.nan), 0
        for tr, te in self.folds(k):
            if b_km > 0:
                near = cKDTree(self.xy[te]).query(self.xy[tr], distance_upper_bound=b_km)[0] <= b_km
                tr = tr[~near]
            b = tr[self.y[tr] == 1]
            if len(b) < MIN_TRAIN_POS or (self.y[tr] == 0).sum() < MIN_TRAIN_POS:
                skipped += 1
                continue
            m = build(THERMAL).fit(self.df.iloc[tr][THERMAL], self.df.burned.iloc[tr])
            o_rf[te] = m.predict_proba(self.df.iloc[te][THERMAL])[:, 1]
            o_null[te] = -cKDTree(self.xy[b]).query(self.xy[te])[0]
        arr = np.vstack([o_rf, o_null, np.full(self.n, skipped)])
        np.save(c, arr)
        return o_rf, o_null, skipped


def find_scaleup(exp):
    hits = [p for p in SCALEUP.glob(f"w*/outputs/experiments/{exp}/step8a/step8a_500m_modeling_dataset.parquet")]
    assert len(hits) == 1, (exp, hits)
    return hits[0]


def load_fires(only=None):
    fires = {}
    for reg in PAPER_REGIONS:
        b = BBOX[reg]
        fires[reg] = Fire(reg, C.load(reg), (b[1] + b[3]) / 2,
                          {"set": "paper", "year": int(reg.split("_")[1]), "lon": (b[0] + b[2]) / 2, "lat": (b[1] + b[3]) / 2})
    b = BBOX["montiferru_2021"]
    fires["montiferru_2021_fullwindow"] = Fire("montiferru_2021_fullwindow",
                                               pd.read_parquet(find_scaleup("montiferru_2021_fullwindow")), (b[1] + b[3]) / 2,
                                               {"set": "paper", "year": 2021, "lon": (b[0] + b[2]) / 2, "lat": (b[1] + b[3]) / 2})
    for exp in regions.SCALEUP_EXPERIMENT_IDS:
        if exp.startswith("rp") or exp == "montiferru_2021_fullwindow":
            continue
        if only and exp not in only:
            continue
        txt = regions.EXPERIMENTS[exp]["display_name"]   # "... centre <lon> E <lat> N)", written by add_scaleup_registry.py
        m = re.search(r"centre ([\d.\-]+) E ([\d.\-]+) N", txt)
        lon, lat = float(m.group(1)), float(m.group(2))
        fires[exp] = Fire(exp, pd.read_parquet(find_scaleup(exp)), lat,
                          {"set": "scaleup", "year": int(exp.split("_")[1]), "lon": lon, "lat": lat})
    return fires


def table_s8():
    # committed copy of Supplementary Table S8 on the main branch (the same 20 values as the IJWF package)
    text = (PAPER / "supplementary.md").read_text(encoding="utf-8")
    rev = {v: k for k, v in NAME.items()}
    out = {(rev[s], rev[t]): float(v) for s, t, v in re.findall(r"(?m)^\| (\w+)→(\w+) \| (\d\.\d{3}) \[", text)}
    assert len(out) == 20, f"{len(out)} directions read from Table S8"
    return out


def gates(F):
    ref = pd.read_csv(PAPER / "labelfix_rerun" / "geometry" / "a1_band_auc.csv")
    ref = ref[ref.k == 0].set_index(["region", "band"]).auc
    worst = 0.0
    for reg in PAPER_REGIONS:
        f = F[reg]
        o = f.oof(THERMAL, "thermal", "rf", 10)
        for name, (lo, hi) in zip(BAND_NAMES, BANDS):
            neg = (f.y == 0) & (f.dist >= lo) & (f.dist < hi)
            if neg.sum() >= MIN_BAND_NEG:
                sel = (f.y == 1) | neg
                worst = max(worst, abs(auc(f.y[sel], o[sel]) - ref[(reg, name)]))
    print(f"gate 1 (bands of the five paper regions): largest difference {worst:.5f}", flush=True)
    assert worst <= 0.0015, "gate 1 failed"
    gate1 = worst
    s8, worst = table_s8(), 0.0
    models = {s: build(THERMAL).fit(F[s].df[THERMAL], F[s].df.burned) for s in PAPER_REGIONS}
    for (s, t), v in s8.items():
        worst = max(worst, abs(auc(F[t].y, models[s].predict_proba(F[t].df[THERMAL])[:, 1]) - v))
    print(f"gate 2 (raw transfer against Table S8): largest difference {worst:.5f}", flush=True)
    assert worst <= 0.002, "gate 2 failed"
    return {"gate1_band_max_diff": gate1, "gate2_transfer_max_diff": worst}


def mahalanobis_to_burned(f):
    X = f.df[NUM].copy()
    X = X.fillna(X.median())
    X = (X - X.mean()) / X.std(ddof=0).replace(0, 1)
    X = X.to_numpy()
    mu = X[f.y == 1].mean(axis=0)
    cov = np.cov(X[f.y == 1], rowvar=False) + 1e-6 * np.eye(X.shape[1])
    inv = np.linalg.pinv(cov)
    dd = X - mu
    return np.sqrt(np.einsum("ij,jk,ik->i", dd, inv, dd))


def analyse_fire(f):
    y = f.y
    row = {"fire": f.id, **f.meta, "cells": f.n, "burned": f.nb, "prevalence": f.nb / f.n, "missing_any": f.missing_any}
    scores = {}
    for k in BLOCKS:
        n_groups = len(np.unique(f.blocks(k)))
        row[f"groups_b{k}"] = n_groups
        if n_groups < 5:          # region too small for 5 folds at this block size: reported, not scored
            continue
        s = {"rf_thermal": f.oof(THERMAL, "thermal", "rf", k), "rf_baseline": f.oof(BASELINE, "baseline", "rf", k),
             "hgb_thermal": f.oof(THERMAL, "thermal", "hgb", k), "null": f.null_oof(k)}
        scores[k] = s
        for name, o in s.items():
            row[f"auc_{name}_b{k}"] = auc(y, o)
            row[f"ap_{name}_b{k}"] = ap(y, o)
        keep = f.pwd_pairs(k)
        row[f"pwd_pairs_b{k}"] = int(len(keep) // 2)
        row[f"pwd_share_pos_b{k}"] = len(keep) / 2 / max(f.nb, 1)
        if len(keep):
            an = auc(y[keep], s["null"][keep])
            row[f"pwd_auc_null_b{k}"] = an
            for name in ("rf_thermal", "rf_baseline", "hgb_thermal"):
                a = auc(y[keep], s[name][keep])
                row[f"pwd_auc_{name}_b{k}"] = a
                row[f"cauc_{name}_b{k}"] = a + 0.5 - max(0.5, an)
    for b in BUFFERS_KM:
        o_rf, o_null, skipped = f.buffered_oof(b)
        row[f"buf{b}_auc_rf_thermal"], row[f"buf{b}_auc_null"] = auc(y, o_rf), auc(y, o_null)
        row[f"buf{b}_folds_skipped"] = skipped
    # claim 2: disjoint distance bands, 5 km block predictions held fixed
    bands = []
    s = scores[10]
    for name, (lo, hi) in zip(BAND_NAMES, BANDS):
        neg = (y == 0) & (f.dist >= lo) & (f.dist < hi)
        sel = (y == 1) | neg
        r = {"fire": f.id, "set": f.meta["set"], "band": name, "negatives": int(neg.sum()),
             "prevalence": f.nb / max(sel.sum(), 1),
             "sd_elevation": float(f.df.elevation_mean[neg].std()) if neg.sum() > 1 else np.nan,
             "sd_ndvi": float(f.df.ndvi_mean[neg].std()) if neg.sum() > 1 else np.nan}
        for mname, o in s.items():
            r[f"auc_{mname}"] = auc(y[sel], o[sel]) if neg.sum() >= MIN_BAND_NEG else np.nan
            r[f"ap_{mname}"] = ap(y[sel], o[sel]) if neg.sum() >= MIN_BAND_NEG else np.nan
        bands.append(r)
    b = pd.DataFrame(bands)
    v = b.dropna(subset=["auc_rf_thermal"])
    row["bands_scored"] = len(v)
    row["rise_rf_thermal"] = float(v.auc_rf_thermal.iloc[-1] - v.auc_rf_thermal.iloc[0]) if len(v) >= 2 else np.nan
    row["rise_hgb_thermal"] = float(v.auc_hgb_thermal.iloc[-1] - v.auc_hgb_thermal.iloc[0]) if len(v) >= 2 else np.nan
    row["trend_rf_thermal"] = float(stats.spearmanr(range(len(v)), v.auc_rf_thermal).statistic) if len(v) >= 3 else np.nan
    # environmental distance quintiles of the unburned cells
    md = mahalanobis_to_burned(f)
    q = np.quantile(md[y == 0], [0.2, 0.4, 0.6, 0.8])
    env = []
    for i in range(5):
        lo = -np.inf if i == 0 else q[i - 1]
        hi = np.inf if i == 4 else q[i]
        neg = (y == 0) & (md >= lo) & (md < hi)
        sel = (y == 1) | neg
        env.append({"fire": f.id, "quintile": i + 1, "negatives": int(neg.sum()),
                    "auc_rf_thermal": auc(y[sel], s["rf_thermal"][sel]), "auc_null": auc(y[sel], s["null"][sel]),
                    "median_geo_km": float(np.median(f.dist[neg]))})
    e = pd.DataFrame(env)
    row["env_rise_rf_thermal"] = float(e.auc_rf_thermal.iloc[-1] - e.auc_rf_thermal.iloc[0])
    return row, b, e


def boot_mean(v, B=NBOOT, seed=SEED):
    v = np.asarray([x for x in v if np.isfinite(x)], float)
    if len(v) < 2:
        return {"n": int(len(v)), "mean": float(v.mean()) if len(v) else None}
    rng = np.random.default_rng(seed)
    bs = [v[rng.integers(0, len(v), len(v))].mean() for _ in range(B)]
    return {"n": int(len(v)), "mean": float(v.mean()), "lo": float(np.percentile(bs, 2.5)), "hi": float(np.percentile(bs, 97.5)),
            "median": float(np.median(v)), "min": float(v.min()), "max": float(v.max())}


def count(a, b):
    ok = np.isfinite(a) & np.isfinite(b)
    return f"{int((a[ok] > b[ok]).sum())} of {int(ok.sum())}"


def summarise(FR, BR, ER):
    S = {}
    for k in BLOCKS:
        FR = FR.reindex(columns=sorted(set(FR.columns) | {f"{p}_{m}_b{k}" for p in ("auc", "ap") for m in ("null", "rf_thermal", "rf_baseline", "hgb_thermal")}
                                       | {f"pwd_auc_null_b{k}", f"pwd_share_pos_b{k}"} | {f"cauc_{m}_b{k}" for m in ("rf_thermal", "rf_baseline", "hgb_thermal")}))
        S[f"blocks_{k}_cells"] = {
            "fires_too_small_for_this_block_size": FR.fire[FR[f"groups_b{k}"] < 5].tolist(),
            **{f"auc_{m}": boot_mean(FR[f"auc_{m}_b{k}"]) for m in ("null", "rf_thermal", "rf_baseline", "hgb_thermal")},
            **{f"ap_{m}": boot_mean(FR[f"ap_{m}_b{k}"]) for m in ("null", "rf_thermal", "rf_baseline", "hgb_thermal")},
            "null_beats_rf_thermal": count(FR[f"auc_null_b{k}"].to_numpy(), FR[f"auc_rf_thermal_b{k}"].to_numpy()),
            "null_beats_hgb_thermal": count(FR[f"auc_null_b{k}"].to_numpy(), FR[f"auc_hgb_thermal_b{k}"].to_numpy()),
            "pwd_auc_null": boot_mean(FR[f"pwd_auc_null_b{k}"]),
            **{f"cauc_{m}": boot_mean(FR[f"cauc_{m}_b{k}"]) for m in ("rf_thermal", "rf_baseline", "hgb_thermal")},
            "pwd_share_of_burned_kept": boot_mean(FR[f"pwd_share_pos_b{k}"]),
        }
    S["buffered"] = {f"{b}_km": {"auc_rf_thermal": boot_mean(FR[f"buf{b}_auc_rf_thermal"]), "auc_null": boot_mean(FR[f"buf{b}_auc_null"]),
                                 "null_beats_rf": count(FR[f"buf{b}_auc_null"].to_numpy(), FR[f"buf{b}_auc_rf_thermal"].to_numpy()),
                                 "folds_skipped_total": int(FR[f"buf{b}_folds_skipped"].sum())} for b in BUFFERS_KM}
    S["bands"] = {n: {**{f"auc_{m}": boot_mean(BR[BR.band == n][f"auc_{m}"]) for m in ("rf_thermal", "rf_baseline", "hgb_thermal", "null")},
                      "ap_rf_thermal": boot_mean(BR[BR.band == n].ap_rf_thermal), "prevalence": boot_mean(BR[BR.band == n].prevalence),
                      "rf_beats_null": count(BR[BR.band == n].auc_rf_thermal.to_numpy(), BR[BR.band == n].auc_null.to_numpy())}
                  for n in BAND_NAMES}
    S["rise"] = {"rf_thermal": boot_mean(FR.rise_rf_thermal), "hgb_thermal": boot_mean(FR.rise_hgb_thermal),
                 "fires_positive_rise_rf": f"{int((FR.rise_rf_thermal > 0).sum())} of {int(FR.rise_rf_thermal.notna().sum())}",
                 "fires_positive_rise_hgb": f"{int((FR.rise_hgb_thermal > 0).sum())} of {int(FR.rise_hgb_thermal.notna().sum())}",
                 "fires_positive_trend_rf": f"{int((FR.trend_rf_thermal > 0).sum())} of {int(FR.trend_rf_thermal.notna().sum())}"}
    S["environmental_quintiles"] = {int(qn): {"auc_rf_thermal": boot_mean(g.auc_rf_thermal), "auc_null": boot_mean(g.auc_null),
                                              "median_geo_km": boot_mean(g.median_geo_km)} for qn, g in ER.groupby("quintile")}
    S["env_rise_rf_thermal"] = boot_mean(FR.env_rise_rf_thermal)
    return S


def main():
    ap_ = argparse.ArgumentParser()
    ap_.add_argument("--fires", default="")
    args = ap_.parse_args()
    t0 = time.time()
    F = load_fires(set(args.fires.split(",")) if args.fires else None)
    g = gates(F)
    primary = [i for i in F if i != "montiferru_2021"]
    rows, bands, envs = [], [], []
    for fid in list(F):
        row, b, e = analyse_fire(F[fid])
        rows.append(row), bands.append(b), envs.append(e)
        print(f"  {fid:28s} n {row['cells']:6d} burned {row['burned']:5d}  null {row['auc_null_b10']:.3f}  rf {row['auc_rf_thermal_b10']:.3f}"
              f"  hgb {row['auc_hgb_thermal_b10']:.3f}  rise {row['rise_rf_thermal']:.3f}  ({time.time() - t0:.0f}s)", flush=True)
    FR, BR, ER = pd.DataFrame(rows), pd.concat(bands, ignore_index=True), pd.concat(envs, ignore_index=True)
    FR.to_csv(OUT / "claims12_per_fire.csv", index=False)
    BR.to_csv(OUT / "claims12_bands.csv", index=False)
    ER.to_csv(OUT / "claims12_env_quintiles.csv", index=False)
    S = {"plan": "docs/scaleup/ANALYSIS_PLAN.md (commit 067e676)", "sklearn": sklearn.__version__, "gates": g,
         "primary_fires": len(primary)}
    S["primary"] = summarise(FR[FR.fire.isin(primary)], BR[BR.fire.isin(primary)], ER[ER.fire.isin(primary)])
    ex = [i for i in primary if i not in EXCLUDE_MISSING]
    S["exclusion_sensitivity"] = {"fires": len(ex), **summarise(FR[FR.fire.isin(ex)], BR[BR.fire.isin(ex)], ER[ER.fire.isin(ex)])}
    S["seconds"] = round(time.time() - t0)
    (OUT / "claims12_summary.json").write_text(json.dumps(S, indent=1, ensure_ascii=False, default=float), encoding="utf-8")
    print(json.dumps(S["primary"]["blocks_10_cells"], indent=1, default=float))


if __name__ == "__main__":
    main()
