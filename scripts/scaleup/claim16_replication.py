"""claim16_replication.py: plan 11.4, replication of G1/G2 on burning from 2024-01-01 to the last published month.

Original workflow:
  python claim16_replication.py freeze    focal out-of-fold scores of every candidate on all 30 primary sites,
                                          written to claim16_scores/<fire>.npz with a sha256 manifest, BEFORE any
                                          2024-2026 label exists on disk
  python claim16_replication.py export    the 2024-2026 label and its QA share (Earth Engine)
  python claim16_replication.py evaluate  rules 9.5 and 10.1 on the primary and secondary sets, Holm across sets
Candidates and settings are those of G1/G2 (claim14_future.py, claim15_location.py); the scores are recomputed with
the same seeds and folds and then frozen.

THERMAL_TWIN_LABEL_SUFFIX unset or empty uses QA bit 0 (land/water). Set it to _qa1 to use QA bit 1
(valid data), export/read labels in analysis/late_qa1 and suffix the evaluation outputs.
Both evaluations verify the original frozen scores against the original manifest and use the original
Claim 14 CSV to identify sites whose G1 scores had already been seen.
Freeze requires an empty or unset suffix. All other suffix values are errors.
"""
import hashlib
import json
import os
import sys
import urllib.request
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "geonull"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from label_variant import QA_MASK, SUFFIX, variant_name  # noqa: E402
import geonull as G  # noqa: E402
import analysis_official as A  # noqa: E402
import claim14_future as C14  # noqa: E402
import claim15_location as C15  # noqa: E402

SC = A.OUT / "claim16_scores"
LAB = A.OUT / variant_name("late")
CANDS = ("coord_rf", "coord_knn", "thermal_coord", "thermal_dist")
START, END = date(2024, 1, 1), date(2026, 9, 30)


def primary_ids(F):
    return [i for i in F if i != "montiferru_2021"]


def freeze():
    if SUFFIX:
        raise SystemExit("freeze requires THERMAL_TWIN_LABEL_SUFFIX to be unset or empty")
    F = A.load_fires()
    SC.mkdir(exist_ok=True)
    man = {}
    for fid in primary_ids(F):
        f = F[fid]
        folds = f.folds(10)
        s = {"thermal": f.oof(A.THERMAL, "thermal", "rf", 10), "baseline": f.oof(A.BASELINE, "baseline", "rf", 10),
             "null": f.null_oof(10), "coord_rf": C14.oof(f.xy, f.y, folds), "coord_knn": C15.knn_oof(f, folds),
             "thermal_coord": C15.oof_extra(f, folds, lambda tr, te: (f.xy[tr], f.xy[te]), ["x_km", "y_km"]),
             "thermal_dist": C15.oof_extra(f, folds, C15.dist_feature(f), ["dist_train_burn"])}
        p = SC / f"{fid}.npz"
        np.savez_compressed(p, y=f.y, row=f.df.row_500m.to_numpy(int), col=f.df.col_500m.to_numpy(int), **s)
        man[fid] = hashlib.sha256(p.read_bytes()).hexdigest()
        print(fid, "frozen", flush=True)
    (A.OUT / "claim16_scores_manifest.json").write_text(json.dumps(man, indent=1), encoding="utf-8")


def export():
    import ee
    import rasterio
    import future_label_export as X
    ee.Initialize(project=os.environ["GEE_PROJECT"])
    LAB.mkdir(exist_ok=True)
    F = A.load_fires()
    for fid in primary_ids(F):
        if (LAB / f"{fid}.tif").exists():
            continue
        with rasterio.open(X.S.grid_path(fid)) as g:
            t, (h, w) = g.transform, g.shape
        proj = ee.ImageCollection(X.MCD).first().projection()
        col = ee.ImageCollection(X.MCD).filterDate(START.isoformat(), "2026-10-01")
        burned = X.burned_between(date(2023, 12, 31), END)
        # QA bit 0 is land/water (original); bit 1 is valid data (Amendment 15).
        unm = col.map(lambda im: im.select("QA").unmask(0).bitwiseAnd(QA_MASK).eq(0)).mean()
        img = ee.Image.cat([b.reproject(proj).reduceResolution(ee.Reducer.mean(), maxPixels=1024) for b in (burned, unm)]).toFloat()
        url = img.getDownloadURL({"crs": "EPSG:4326", "crs_transform": [t.a, t.b, t.c, t.d, t.e, t.f],
                                  "dimensions": f"{w}x{h}", "format": "GEO_TIFF"})
        with urllib.request.urlopen(url, timeout=1800) as resp, open(LAB / f"{fid}.tif", "wb") as fh:
            fh.write(resp.read())
        print(fid, "exported", flush=True)


def holm(p):
    order = np.argsort(p)
    adj = np.empty(len(p))
    run = 0.0
    for k, i in enumerate(order):
        run = max(run, min(1.0, (len(p) - k) * p[i]))
        adj[i] = run
    return adj


def boot_p(d, groups, B=10_000):
    """Mean, 95% and 90% intervals, and the one-sided bootstrap p for mean > 0, over geographic clusters."""
    d, groups = np.asarray(d, float), np.asarray(groups)
    u = np.unique(groups)
    rng = np.random.default_rng(42)
    bs = np.array([d[np.concatenate([np.where(groups == c)[0] for c in rng.choice(u, len(u))])].mean() for _ in range(B)])
    return {"mean": float(d.mean()), "ci95": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))],
            "ci90": [float(np.percentile(bs, 5)), float(np.percentile(bs, 95))], "p_gt0": float((bs <= 0).mean()),
            "fires": int(len(d)), "clusters": int(len(u))}


def evaluate():
    import rasterio
    F = A.load_fires()
    man = json.loads((A.OUT / "claim16_scores_manifest.json").read_text())
    # The secondary set excludes sites whose G1 scores had already been seen (plan 11.4).
    g1 = set(pd.read_csv(A.OUT / "claim14_future_per_fire.csv").fire)
    rows = []
    for fid in primary_ids(F):
        p = SC / f"{fid}.npz"
        if hashlib.sha256(p.read_bytes()).hexdigest() != man[fid]:
            raise ValueError(f"scores of {fid} changed after freezing")
        D = np.load(p)
        f = F[fid]
        with rasterio.open(LAB / f"{fid}.tif") as r:
            a = r.read()
        lab, unm = a[0][D["row"], D["col"]], a[1][D["row"], D["col"]]
        with rasterio.open(A.OUT / "yearly" / f"{fid}.tif") as r:
            yr = r.read()
        b1723 = (yr[4:11][:, D["row"], D["col"]] >= 0.5).any(axis=0)      # bands 2017-2023
        pop = (unm <= 0.10) & (D["y"] == 0)
        yl = (lab >= 0.5).astype(int)
        npos, nneg = int(yl[pop].sum()), int((1 - yl[pop]).sum())
        r = {"fire": fid, "in_g1": fid in g1, "late_burned": npos, "late_unburned": nneg,
             "pop_burned_2017_2023": int((pop & b1723).sum())}
        if npos < 30 or nneg < 30:
            r["eligible"] = False
            rows.append(r)
            continue
        r["eligible"] = True
        null, z = D["null"], -D["null"]
        pairs = f.pwd_pairs(10)
        sn = G.standardised_auc(D["y"], null, z)["sauc"]
        tm = C14.focal_measures(f, None, D["thermal"], null, pairs, z, sn)
        ft = G.auc(yl[pop], D["thermal"][pop])
        r["late_thermal"] = ft
        for cand in CANDS + ("baseline",):
            cm = C14.focal_measures(f, None, D[cand], null, pairs, z, sn)
            fc = G.auc(yl[pop], D[cand][pop])
            r[f"{cand}_late"] = fc
            for meas in ("auc", "cauc", "saucc"):
                ch = C14.choose(tm[meas], cm[meas])
                r[f"{cand}_choice_{meas}"] = ch or "none"
                r[f"{cand}_loss_{meas}"] = C14.loss_for(ch, ft, fc)
        rows.append(r)
        print(fid, "evaluated", flush=True)
    R = pd.DataFrame(rows)
    R.to_csv(A.OUT / variant_name("claim16_per_fire.csv"), index=False)
    E = R[R.eligible]
    sets = {"primary": E, "secondary": E[~E.in_g1]}
    S = {"eligible": int(len(E)), "secondary_fires": sets["secondary"].fire.tolist(),
         "not_eligible": R[~R.eligible][["fire", "late_burned"]].to_dict("records")}
    # rule 9.5 (coordinate RF pair), Holm across the two sets
    r95 = {k: boot_p(v.coord_rf_loss_auc - v.coord_rf_loss_cauc, C14.clusters(F, v.fire.tolist())) for k, v in sets.items() if len(v) >= 2}
    if r95:
        adj = holm(np.array([v["p_gt0"] for v in r95.values()]))
        for (k, v), pa in zip(r95.items(), adj):
            lo95, hi95 = v["ci95"]
            lo90, hi90 = v["ci90"]
            v["p_holm"] = float(pa)
            v["verdict"] = ("advantage, practically important" if pa < 0.025 and v["mean"] >= 0.01 else "advantage" if pa < 0.025
                            else "equivalence" if lo90 >= -0.01 and hi90 <= 0.01 else "inconclusive")
            v["same_choice"] = int((sets[k].coord_rf_choice_auc == sets[k].coord_rf_choice_cauc).sum())
    S["rule_9_5"] = r95
    # rule 10.1 per candidate, Holm across the two sets
    r101 = {}
    for cand in CANDS:
        res = {}
        for k, v in sets.items():
            if len(v) < 2:
                continue
            b = boot_p(v.late_thermal - v[f"{cand}_late"], C14.clusters(F, v.fire.tolist()))
            b["pooled_auc_chooses_location"] = int((v[f"{cand}_choice_auc"] == "c").sum())
            b["cauc_chooses_location"] = int((v[f"{cand}_choice_cauc"] == "c").sum())
            b["saucc_chooses_location"] = int((v[f"{cand}_choice_saucc"] == "c").sum())
            b["thermal_better"] = int((v.late_thermal > v[f"{cand}_late"]).sum())
            b["loss"] = {m: float(v[f"{cand}_loss_{m}"].mean()) for m in ("auc", "cauc", "saucc")}
            res[k] = b
        if res:
            adj = holm(np.array([v["p_gt0"] for v in res.values()]))
            for (k, v), pa in zip(res.items(), adj):
                n = v["fires"]
                v["p_holm"] = float(pa)
                v["transfer_failure"] = bool(v["pooled_auc_chooses_location"] >= int(np.ceil(12 / 18 * n)) and pa < 0.025)
        r101[cand] = res
    S["rule_10_1"] = r101
    (A.OUT / variant_name("claim16_summary.json")).write_text(json.dumps(S, indent=1, default=float), encoding="utf-8")
    print(json.dumps(S, indent=1, default=float)[:6000])


if __name__ == "__main__":
    {"freeze": freeze, "export": export, "evaluate": evaluate}[sys.argv[1]]()
