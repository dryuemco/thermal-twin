"""claim7_open_data.py: claim 7 of docs/scaleup/ANALYSIS_PLAN.md (amendment 2), re-analysis of open datasets.

For each dataset the authors' split is rebuilt from their code or package, the geographic null model
(score = minus the distance to the nearest TRAINING fire sample) is scored on the same test samples,
and a random forest on the authors' predictors (where the package has them) is run on the same split
as a reproduction check. The AUC the paper reports is copied from the package files.

Datasets ($THERMAL_TWIN_SCALEUP/open_data, downloaded 14 Nov 2026, CC BY 4.0 / MIT):
  korea     Heo, Zenodo 10.5281/zenodo.18408642: random stratified 70/30, random_state 42 (rf_code.txt)
  alberta   Zenodo 10.5281/zenodo.23008173: temporal (train 2001-2014, test 2018-2021) and 5-fold
            spatial blocks of 100 km (2001-2014); 10 km control buffer (main protocol)
  bc        Khan et al., Zenodo 10.5281/zenodo.21910108: 10-fold GroupKFold on 50 km lat/lon blocks
            (compute_block_ids in src/c8c11_non_pso_cli.py), 70 ha points, seeds 42 ... 909
  italy, mesogeos: added when their files are unpacked

Run:  python -I claim7_open_data.py   (writes $THERMAL_TWIN_SCALEUP/analysis/claim7_*)
"""
import json
import os
import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupKFold, train_test_split

ROOT = Path(os.environ["THERMAL_TWIN_SCALEUP"]) / "open_data"
OUT = Path(os.environ["THERMAL_TWIN_SCALEUP"]) / "analysis"
SEED = 42


def km_xy(lon, lat):
    lat0 = float(np.nanmean(lat))
    return np.c_[np.asarray(lon) * 111.32 * math.cos(math.radians(lat0)), np.asarray(lat) * 110.57]


def null_scores(xy_train, y_train, xy_test):
    pos = xy_train[np.asarray(y_train) == 1]
    return -cKDTree(pos).query(xy_test)[0]


def auc(y, s):
    return float(roc_auc_score(y, s))


def rf(Xtr, ytr, Xte):
    m = RandomForestClassifier(n_estimators=300, class_weight="balanced", random_state=SEED, n_jobs=30)
    return m.fit(Xtr.fillna(Xtr.median()), ytr).predict_proba(Xte.fillna(Xtr.median()))[:, 1]


def korea():
    d = pd.read_csv(ROOT / "korea" / "for_validation_rf.csv")
    feats = [c for c in d.columns if c not in ("OBJECTID", "Longitude", "Latitude", "Fire", "y_test", "rf_pred")]
    xy = km_xy(d.Longitude, d.Latitude)
    idx = np.arange(len(d))
    tr, te = train_test_split(idx, test_size=0.3, stratify=d.Fire, random_state=42)
    y = d.Fire.to_numpy()
    # authors' own RF settings (rf_code.txt) to check that this file and split are the ones behind 0.829
    m = RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")
    a_rep = auc(y[te], m.fit(d.iloc[tr][feats], y[tr]).predict_proba(d.iloc[te][feats])[:, 1])
    a_null = auc(y[te], null_scores(xy[tr], y[tr], xy[te]))
    return [{"dataset": "korea", "protocol": "random stratified 70/30 (authors)", "n_fire": int(y.sum()),
             "n_nonfire": int((y == 0).sum()), "reported_auc": 0.829, "reported_model": "RF",
             "reproduced_rf_auc": a_rep, "null_auc": a_null, "features": len(feats)}]


def alberta():
    base = ROOT / "alberta" / "x" / "Alberta_Wildfire_Reproducibility_Package"
    d = pd.read_csv(base / "Alberta_model_inputs" / "model_ready" / "sample_metadata_model_2001_2021_buffer10km.csv")
    xy = np.c_[d["col"].to_numpy() * 0.5, d["row"].to_numpy() * 0.5]      # 500 m grid cells, km
    y = d.fire_label.to_numpy()
    rows = []
    tr = (d.YEAR <= 2014).to_numpy()
    te = (d.YEAR >= 2018).to_numpy()
    rep = pd.read_csv(base / "Alberta_main_temporal_results" / "temporal_generalization_results.csv")
    rep_te = rep[rep.Split.str.startswith("Independent")].set_index("Model").AUC
    rows.append({"dataset": "alberta", "protocol": "temporal: train 2001-2014, test 2018-2021 (authors)",
                 "n_fire": int(y[te].sum()), "n_nonfire": int((y[te] == 0).sum()),
                 "reported_auc": float(rep_te.max()), "reported_model": str(rep_te.idxmax()),
                 "null_auc": auc(y[te], null_scores(xy[tr], y[tr], xy[te]))})
    tr2 = (d.YEAR <= 2017).to_numpy()
    rows.append({"dataset": "alberta", "protocol": "temporal: train 2001-2017, test 2018-2021",
                 "n_fire": int(y[te].sum()), "n_nonfire": int((y[te] == 0).sum()),
                 "reported_auc": float(rep_te.max()), "reported_model": str(rep_te.idxmax()),
                 "null_auc": auc(y[te], null_scores(xy[tr2], y[tr2], xy[te]))})
    sub = d[d.YEAR <= 2014].reset_index(drop=True)
    xs, ys = np.c_[sub["col"] * 0.5, sub["row"] * 0.5], sub.fire_label.to_numpy()
    o = np.full(len(sub), np.nan)
    fold_auc = []
    for trf, tef in GroupKFold(5).split(xs, ys, groups=sub.spatial_block_100km):
        o[tef] = null_scores(xs[trf], ys[trf], xs[tef])
        fold_auc.append(auc(ys[tef], o[tef]))
    cv = pd.read_csv(base / "Alberta_spatial_block_cv_results" / "spatial_block_5fold_results_by_fold.csv")
    best = cv.groupby("Model").AUC.mean()
    rows.append({"dataset": "alberta", "protocol": "5-fold spatial blocks of 100 km, 2001-2014 (fold rule re-created)",
                 "n_fire": int(ys.sum()), "n_nonfire": int((ys == 0).sum()), "reported_auc": float(best.max()),
                 "reported_model": str(best.idxmax()), "null_auc": float(np.mean(fold_auc)), "null_auc_pooled": auc(ys, o)})
    return rows


def bc_blocks(lat, lon, grid_km=50.0):
    lat, lon = np.asarray(lat, float), np.asarray(lon, float)
    lat_mean = np.nanmean(lat)
    deg_lat = grid_km / 111.0
    deg_lon = grid_km / (111.0 * max(0.2, math.cos(math.radians(lat_mean))))
    gx = np.floor(lon / deg_lon).astype(np.int64)
    gy = np.floor(lat / deg_lat).astype(np.int64)
    gx_off = gx - gx.min()
    return gy * (gx_off.max() + 1) + gx_off


def bc():
    rows = []
    for p in sorted((ROOT / "bc" / "x").glob("training_points_70ha_seed*.csv")):
        d = pd.read_csv(p)
        y = d.Status.to_numpy().astype(int)
        xy = km_xy(d.Longitude, d.Latitude)
        groups = bc_blocks(d.Latitude, d.Longitude)
        feats = [c for c in d.columns if c not in ("UniqueID", "Longitude", "Latitude", "Status")]
        o_null, o_rf = np.full(len(d), np.nan), np.full(len(d), np.nan)
        for tr, te in GroupKFold(10).split(xy, y, groups=groups):
            o_null[te] = null_scores(xy[tr], y[tr], xy[te])
            o_rf[te] = rf(d.iloc[tr][feats], y[tr], d.iloc[te][feats])
        rows.append({"dataset": "bc", "sample": p.stem, "protocol": "10-fold GroupKFold, 50 km blocks (authors)",
                     "n_fire": int(y.sum()), "n_nonfire": int((y == 0).sum()), "reported_auc": 0.92,
                     "reported_model": "PSO-BiLSTM", "rf_auc_same_folds": auc(y, o_rf), "null_auc": auc(y, o_null)})
        print(p.stem, rows[-1]["null_auc"], rows[-1]["rf_auc_same_folds"], flush=True)
    return rows


def italy():
    """Cilli et al. 2022 (Sci Rep, doi 10.1038/s41598-022-20347-9), Zenodo record 10003397. Coordinates are the
    bounding-box centres of the grid shapefile (UTM 32N, metres); the row order of the table is checked
    against the shapefile (elevation and fold column must match row for row)."""
    import shapefile  # pyshp
    base = ROOT / "italy" / "x" / "explainable_wildfire_occurrences_Italy"
    d = pd.read_csv(base / "input" / "DataTable_for_XAI.csv")
    r = shapefile.Reader(str(base / "Grid_DataSet_with_SpatialCV" / "Grid_DataSet_with_SpatialCV"))
    names = [f[0] for f in r.fields[1:]]
    i_dtm, i_cv = names.index("dtm_mean_1"), names.index("cv")
    xy, dtm, cvs = [], [], []
    for sr in r.iterShapeRecords():
        b = sr.shape.bbox
        xy.append(((b[0] + b[2]) / 2 / 1000, (b[1] + b[3]) / 2 / 1000))
        dtm.append(sr.record[i_dtm]), cvs.append(sr.record[i_cv])
    xy = np.asarray(xy)
    order_ok = bool(np.allclose(np.asarray(dtm, float), d.Elevation.to_numpy(float), equal_nan=True)
                    and (np.asarray(cvs) == d.cv.to_numpy()).all())
    assert order_ok, "table and shapefile rows are not in the same order"
    y = d.wildfires.astype(str).str.upper().eq("TRUE").to_numpy().astype(int)
    feats = [c for c in d.columns[1:18]]
    o_null, o_rf = np.full(len(d), np.nan), np.full(len(d), np.nan)
    for k in sorted(d.cv.unique()):
        te = (d.cv == k).to_numpy()
        o_null[te] = null_scores(xy[~te], y[~te], xy[te])
        o_rf[te] = rf(d.loc[~te, feats], y[~te], d.loc[te, feats])
    return [{"dataset": "italy", "protocol": f"spatial CV, authors' fold column ({d.cv.nunique()} folds)",
             "n_fire": int(y.sum()), "n_nonfire": int((y == 0).sum()), "reported_auc": 0.813,
             "reported_model": "RF (median of 100 runs)", "rf_auc_same_folds": auc(y, o_rf), "null_auc": auc(y, o_null),
             "row_order_checked": order_ok}]


def mesogeos():
    """Kondylatos et al. 2023 (NeurIPS), Zenodo 10.5281/zenodo.17201754, track A. One row per sample (its last
    day); split by year as in the benchmark loader: train 2006-2019, validation 2020, test 2021-2022. The
    paper reports AUPRC only, so the null model's AUPRC is given beside its AUC."""
    from sklearn.metrics import average_precision_score
    parts = []
    for f, lab in (("positives.csv", 1), ("negatives.csv", 0)):
        d = pd.read_csv(ROOT / "mesogeos" / f, usecols=["time", "x", "y", "sample"])
        d = d.sort_values("time").groupby("sample").tail(1)
        d["label"] = lab
        parts.append(d)
    d = pd.concat(parts, ignore_index=True)
    d["year"] = d.time.str[:4].astype(int)
    xy = km_xy(d.x, d.y)
    y = d.label.to_numpy()
    tr = (d.year <= 2019).to_numpy()
    te = (d.year >= 2021).to_numpy()
    s = null_scores(xy[tr], y[tr], xy[te])
    return [{"dataset": "mesogeos", "protocol": "temporal: train 2006-2019, test 2021-2022 (benchmark)",
             "n_fire": int(y[te].sum()), "n_nonfire": int((y[te] == 0).sum()), "reported_auc": np.nan,
             "reported_auprc": "0.853-0.858", "reported_model": "LSTM / Transformer (benchmark)",
             "null_auc": auc(y[te], s), "null_auprc": float(average_precision_score(y[te], s)),
             "test_prevalence": float(y[te].mean())}]


def main():
    rows = korea() + alberta() + bc() + italy() + mesogeos()
    T = pd.DataFrame(rows)
    T.to_csv(OUT / "claim7_open_data.csv", index=False)
    pd.set_option("display.width", 250)
    print(T.drop(columns=[c for c in ("sample",) if c in T]).to_string())
    (OUT / "claim7_open_data.json").write_text(json.dumps(rows, indent=1, default=float), encoding="utf-8")


if __name__ == "__main__":
    main()
