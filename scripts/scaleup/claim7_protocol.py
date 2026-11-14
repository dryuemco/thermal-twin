"""claim7_protocol.py: the full protocol (null AUC, cAUC, distance bands) on the open datasets that ship
predictors (amendment 5, post hoc, asked for by the second review).

Splits and RF settings are those of claim7_open_data.py. The model scores are a random forest on the authors'
predictors (Korea: the authors' own settings; British Columbia, Italy: 300 trees, balanced; Mesogeos: the same on
the predictor values of each sample's last day), so the three numbers describe a predictor-based model on each
dataset's own split. Distances are in km; bands are the study's bands (0-0.5 ... >10 km) of the distance from each
negative to the nearest positive of the whole dataset. Alberta ships only the feature names
(model_feature_names.json), not their values, and is left out. Also written: the minimum distance from each
Alberta negative to a positive of the same year (the control buffer of the authors' sampling).

Writes claim7_protocol.csv, claim7_protocol_bands.csv and claim7_protocol.json in $THERMAL_TWIN_SCALEUP/analysis.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupKFold, train_test_split

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "geonull"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import geonull as G  # noqa: E402
import claim7_open_data as O  # noqa: E402


def run(name, xy, y, folds, score, protocol):
    r = G.evaluate(xy, y, folds, score)
    bands = [{"dataset": name, "band": m["band"], "negatives": m["negatives"], "auc_model": m["auc"], "auc_null": n["auc"]}
             for m, n in zip(r["bands_model"], r["bands_null"])]
    row = {"dataset": name, "protocol": protocol, "n": int(len(y)), "n_fire": int(y.sum()),
           **{k: r[k] for k in ("auc_model", "auc_null", "auc_pairs", "auc_null_pairs", "cauc", "pairs", "positives_kept")}}
    print(name, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in row.items()}, flush=True)
    return row, bands


def korea():
    d = pd.read_csv(O.ROOT / "korea" / "for_validation_rf.csv")
    feats = [c for c in d.columns if c not in ("OBJECTID", "Longitude", "Latitude", "Fire", "y_test", "rf_pred")]
    xy, y = O.km_xy(d.Longitude, d.Latitude), d.Fire.to_numpy().astype(int)
    tr, te = train_test_split(np.arange(len(d)), test_size=0.3, stratify=y, random_state=42)
    s = np.full(len(d), np.nan)
    m = RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")
    s[te] = m.fit(d.iloc[tr][feats], y[tr]).predict_proba(d.iloc[te][feats])[:, 1]
    keep = np.sort(np.r_[tr, te])
    return run("korea", xy, y, [(tr, te)], s, "random stratified 70/30 (authors)") if len(keep) == len(d) else None


def bc():
    out = []
    for p in sorted((O.ROOT / "bc" / "x").glob("training_points_70ha_seed*.csv"))[:1]:   # first sample file
        d = pd.read_csv(p)
        y, xy = d.Status.to_numpy().astype(int), O.km_xy(d.Longitude, d.Latitude)
        feats = [c for c in d.columns if c not in ("UniqueID", "Longitude", "Latitude", "Status")]
        folds = list(GroupKFold(10).split(xy, y, groups=O.bc_blocks(d.Latitude, d.Longitude)))
        s = np.full(len(d), np.nan)
        for tr, te in folds:
            s[te] = O.rf(d.iloc[tr][feats], y[tr], d.iloc[te][feats])
        out.append(run("bc", xy, y, folds, s, f"10-fold GroupKFold, 50 km blocks (authors), {p.stem}"))
    return out


def italy():
    import shapefile
    base = O.ROOT / "italy" / "x" / "explainable_wildfire_occurrences_Italy"
    d = pd.read_csv(base / "input" / "DataTable_for_XAI.csv")
    r = shapefile.Reader(str(base / "Grid_DataSet_with_SpatialCV" / "Grid_DataSet_with_SpatialCV"))
    xy = np.asarray([((s.bbox[0] + s.bbox[2]) / 2000, (s.bbox[1] + s.bbox[3]) / 2000) for s in r.shapes()])
    y = d.wildfires.astype(str).str.upper().eq("TRUE").to_numpy().astype(int)
    feats = list(d.columns[1:18])
    folds = [(np.where(d.cv != k)[0], np.where(d.cv == k)[0]) for k in sorted(d.cv.unique())]
    s = np.full(len(d), np.nan)
    for tr, te in folds:
        s[te] = O.rf(d.iloc[tr][feats], y[tr], d.iloc[te][feats])
    return run("italy", xy, y, folds, s, "spatial CV, authors' fold column")


def mesogeos():
    drop = {"time", "x", "y", "sample", "burned_areas", "ignition_points", "burned_area_has", "time_idx"}
    parts = []
    for f, lab in (("positives.csv", 1), ("negatives.csv", 0)):
        d = pd.read_csv(O.ROOT / "mesogeos" / f)
        d = d.sort_values("time").groupby("sample").tail(1)
        d["label"] = lab
        parts.append(d)
    d = pd.concat(parts, ignore_index=True)
    year = d.time.str[:4].astype(int).to_numpy()
    feats = [c for c in d.columns if c not in drop | {"label"}]
    tr, te = np.where(year <= 2019)[0], np.where(year >= 2021)[0]
    xy, y = O.km_xy(d.x, d.y), d.label.to_numpy().astype(int)
    s = np.full(len(d), np.nan)
    s[te] = O.rf(d.iloc[tr][feats], y[tr], d.iloc[te][feats])
    sel = np.r_[tr, te]
    tr2, te2 = np.arange(len(tr)), np.arange(len(tr), len(sel))
    return run("mesogeos", xy[sel], y[sel], [(tr2, te2)], s[sel], "temporal: train 2006-2019, test 2021-2022 (last day)")


def alberta_buffer():
    base = O.ROOT / "alberta" / "x" / "Alberta_Wildfire_Reproducibility_Package"
    d = pd.read_csv(base / "Alberta_model_inputs" / "model_ready" / "sample_metadata_model_2001_2021_buffer10km.csv")
    dmin = []
    for yr, g in d.groupby("YEAR"):
        xy = np.c_[g["col"] * 0.5, g["row"] * 0.5]
        pos, neg = xy[g.fire_label.to_numpy() == 1], xy[g.fire_label.to_numpy() == 0]
        if len(pos) and len(neg):
            dmin.append(cKDTree(pos).query(neg)[0])
    dmin = np.concatenate(dmin)
    return {"negatives": int(len(dmin)), "min_km": float(dmin.min()), "share_below_10km": float((dmin < 10).mean()),
            "median_km": float(np.median(dmin)), "control_buffer_km_column": sorted(d.control_buffer_km.unique().tolist())}


def main():
    rows, bands = [], []
    for res in [korea(), *bc(), italy(), mesogeos()]:
        rows.append(res[0]), bands.extend(res[1])
    R, B = pd.DataFrame(rows), pd.DataFrame(bands)
    R.to_csv(O.OUT / "claim7_protocol.csv", index=False)
    B.to_csv(O.OUT / "claim7_protocol_bands.csv", index=False)
    S = {"datasets": rows, "alberta_buffer": alberta_buffer()}
    (O.OUT / "claim7_protocol.json").write_text(json.dumps(S, indent=1, default=float), encoding="utf-8")
    print(B.to_string()), print(S["alberta_buffer"])


if __name__ == "__main__":
    main()
