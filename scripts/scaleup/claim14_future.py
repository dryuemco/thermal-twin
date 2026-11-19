"""claim14_future.py: G1a-G1c of plan amendment 9 (with 9.9). Fixed focal out-of-fold scores rescored against
later real burning; no refit except the coordinate RF (9.3) and the history RF (9.8, G1c).

Inputs: the cached focal scores of analysis_official.py (thermal and baseline RF, 5 km blocks), the future/<fire>.tif
rasters of future_label_export.py and claim8_sauc settings (geonull defaults).
Writes claim14_future_per_fire.csv, claim14_events.csv, claim14_history.csv and claim14_future_summary.json.
THERMAL_TWIN_LABEL_SUFFIX unset or empty selects original labels and names. Set it to _qa1 to read
future_qa1 and append _qa1 before each output extension. All other values are errors.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
from scipy import ndimage
from scipy.spatial import cKDTree
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "geonull"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from label_variant import SUFFIX, variant_name  # noqa: E402
import geonull as G  # noqa: E402
import analysis_official as A  # noqa: E402

FUT = A.OUT / variant_name("future")
MIN = 30
NB = 10_000


def focal_rf(f, features, tag):
    if SUFFIX:
        return np.load(f._cache(f"{tag}_rf_b10"))
    return f.oof(features, tag, "rf", 10)


def rf():
    return RandomForestClassifier(n_estimators=300, min_samples_leaf=3, class_weight="balanced", random_state=A.SEED,
                                  n_jobs=A.N_JOBS)


def oof(X, y, folds):
    o = np.full(len(y), np.nan)
    for tr, te in folds:
        o[te] = rf().fit(X[tr], y[tr]).predict_proba(X[te])[:, 1]
    return o


def choose(meas_t, meas_c):
    if not (np.isfinite(meas_t) and np.isfinite(meas_c)) or meas_t == meas_c:
        return None
    return "t" if meas_t > meas_c else "c"


def focal_measures(f, folds, s, null, pairs, z, sn):
    out = {"auc": G.auc(f.y, s), "cauc": G.calibrated_auc(f.y, s, null, pairs)["cauc"]}
    sa = G.standardised_auc(f.y, s, z)["sauc"]
    out["saucc"] = sa + 0.5 - max(0.5, sn) if np.isfinite(sn) else np.nan
    return out


def events(fut, year, rr, cc, shape):
    """8-connected components of future-burned cells per first-burn year; returns an event id per cell (-1 none)."""
    ev = np.full(len(fut), -1)
    nxt = 0
    for yr in np.unique(year[fut]):
        grid = np.zeros(shape, bool)
        sel = fut & (year == yr)
        grid[rr[sel], cc[sel]] = True
        lab, n = ndimage.label(grid, structure=np.ones((3, 3)))
        ev[sel] = lab[rr[sel], cc[sel]] - 1 + nxt
        nxt += n
    return ev


def loss_for(choice, ft, fc):
    best = max(ft, fc)
    return best - (ft if choice == "t" else fc if choice == "c" else min(ft, fc))


def main():
    F = A.load_fires()
    ids = [i for i in F if i != "montiferru_2021"]
    rows, evrows, hist, excluded = [], [], [], []
    for fid in ids:
        f = F[fid]
        with rasterio.open(FUT / f"{fid}.tif") as r:
            a = r.read()
        rr, cc = f.df.row_500m.to_numpy(int), f.df.col_500m.to_numpy(int)
        fut_all, fut_2y, unm, fyear, hist_pre = (a[i][rr, cc] for i in range(5))
        mapped = unm <= 0.10
        pop = mapped & (f.y == 0)                         # primary future population (9.2)
        pop_full = mapped
        yf = (fut_all >= 0.5).astype(int)
        yf2 = (fut_2y >= 0.5).astype(int)
        npos, nneg = int(yf[pop].sum()), int((1 - yf[pop]).sum())
        folds = f.folds(10)
        st = focal_rf(f, A.THERMAL, "thermal")
        sb = focal_rf(f, A.BASELINE, "baseline")
        null = f.null_oof(10)
        z = -null
        pairs = f.pwd_pairs(10)
        sn = G.standardised_auc(f.y, null, z)["sauc"]
        # G1c on every fire (focal event only)
        num = [c for c in A.THERMAL if c != A.CAT] + ["hist_pre"]
        d = f.df.copy()
        d["hist_pre"] = hist_pre
        sh = np.full(f.n, np.nan)
        for tr, te in folds:
            pre = ColumnTransformer([("num", SimpleImputer(strategy="median"), num),
                                     ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                                                       ("oh", OneHotEncoder(handle_unknown="ignore"))]), [A.CAT])])
            m = Pipeline([("p", pre), ("clf", rf())]).fit(d.iloc[tr][num + [A.CAT]], f.y[tr])
            sh[te] = m.predict_proba(d.iloc[te][num + [A.CAT]])[:, 1]
        hm = focal_measures(f, folds, sh, null, pairs, z, sn)
        tm = focal_measures(f, folds, st, null, pairs, z, sn)
        hist.append({"fire": fid, **{f"thermal_{k}": v for k, v in tm.items()}, **{f"thermal_hist_{k}": v for k, v in hm.items()},
                     "hist_only_auc": G.auc(f.y, hist_pre), "hist_cells": int((hist_pre >= 0.5).sum())})
        if npos < MIN or nneg < MIN:
            excluded.append({"fire": fid, "year": f.meta["year"], "future_burned": npos, "future_unburned": nneg,
                             "unmapped_cells": int((~mapped).sum()), "reason": "fewer than 30 future-burned cells"
                             if npos < MIN else "fewer than 30 future-unburned cells"})
            print(fid, "excluded", npos, flush=True)
            continue
        sc = oof(f.xy, f.y, folds)                             # coordinate RF (9.3)
        cm = focal_measures(f, folds, sc, null, pairs, z, sn)
        bm = focal_measures(f, folds, sb, null, pairs, z, sn)
        r = {"fire": fid, "year": f.meta["year"], "future_burned": npos, "future_unburned": nneg,
             "focal_burned": int(f.y.sum())}
        for name, (cand, cm_) in {"coord": (sc, cm), "baseline": (sb, bm)}.items():
            for popname, P, Y in (("primary", pop, yf), ("full", pop_full, yf), ("two_year", pop, yf2)):
                if Y[P].sum() < MIN:
                    continue
                ft, fc = G.auc(Y[P], st[P]), G.auc(Y[P], cand[P])
                r[f"{name}_{popname}_fut_thermal"], r[f"{name}_{popname}_fut_cand"] = ft, fc
                for meas in ("auc", "cauc", "saucc"):
                    ch = choose(tm[meas], cm_[meas])
                    r[f"{name}_{popname}_choice_{meas}"] = ch or "none"
                    r[f"{name}_{popname}_loss_{meas}"] = loss_for(ch, ft, fc)
        for meas in ("auc", "cauc", "saucc"):
            r[f"focal_thermal_{meas}"], r[f"focal_coord_{meas}"] = tm[meas], cm[meas]
        # events (9.7)
        ev = events(yf.astype(bool) & pop, np.round(fyear).astype(int), rr - rr.min(), cc - cc.min(),
                    (rr.max() - rr.min() + 1, cc.max() - cc.min() + 1))
        P = pop
        evs, cnt = np.unique(ev[P & (ev >= 0)], return_counts=True)
        r["events"], r["largest_event_share"] = int(len(evs)), float(cnt.max() / cnt.sum())
        r["future_years"] = int(len(np.unique(np.round(fyear[P & (yf == 1)]))))
        w = np.ones(P.sum())
        evP, yP = ev[P], yf[P]
        for e_, n_ in zip(evs, cnt):
            w[evP == e_] = 1.0 / n_
        w[yP == 0] = 1.0
        ft_w = roc_auc_score(yP, st[P], sample_weight=w)
        fc_w = roc_auc_score(yP, sc[P], sample_weight=w)
        r["coord_eventweighted_loss_auc"] = loss_for(choose(tm["auc"], cm["auc"]), ft_w, fc_w)
        r["coord_eventweighted_loss_cauc"] = loss_for(choose(tm["cauc"], cm["cauc"]), ft_w, fc_w)
        lo = []
        for e_ in evs:
            keep = ~(evP == e_)
            if yP[keep].sum() >= MIN:
                ft_, fc_ = G.auc(yP[keep], st[P][keep]), G.auc(yP[keep], sc[P][keep])
                lo.append(loss_for(choose(tm["auc"], cm["auc"]), ft_, fc_) - loss_for(choose(tm["cauc"], cm["cauc"]), ft_, fc_))
        r["loeo_D_min"], r["loeo_D_max"] = (float(min(lo)), float(max(lo))) if lo else (np.nan, np.nan)
        # G1b (9.8)
        scar = np.c_[f.xy[f.y == 1]]
        dscar = cKDTree(scar).query(f.xy)[0]
        r["g1b_future_auc_minus_dist_to_scar"] = G.auc(yP, -dscar[P])
        r["null_future_auc"] = G.auc(yP, null[P])
        rows.append(r)
        evrows.append({"fire": fid, "events": r["events"], "largest_event_share": r["largest_event_share"],
                       "future_years": r["future_years"]})
        print(fid, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()
                    if k.startswith("coord_primary_loss") or k in ("future_burned",)}, flush=True)
    R = pd.DataFrame(rows)
    R.to_csv(A.OUT / variant_name("claim14_future_per_fire.csv"), index=False)
    pd.DataFrame(evrows).to_csv(A.OUT / variant_name("claim14_events.csv"), index=False)
    pd.DataFrame(hist).to_csv(A.OUT / variant_name("claim14_history.csv"), index=False)
    S = {"eligible": int(len(R)), "excluded": excluded, "decision": decide(R, F, "coord_primary"),
         "sensitivity": {k: decide(R, F, k) for k in ("coord_full", "coord_two_year", "baseline_primary")}}
    S["sensitivity"]["coord_event_weighted"] = decide_cols(R, F, "coord_eventweighted_loss_auc", "coord_eventweighted_loss_cauc")
    S["leave_one_event_out_D"] = {"min_over_fires_min": float(R.loeo_D_min.min()), "max_over_fires_max": float(R.loeo_D_max.max())}
    S["g1b_future_auc_minus_dist_to_scar"] = A.boot_mean(R.g1b_future_auc_minus_dist_to_scar)
    S["relative_loss"] = {m: float(R[f"coord_primary_loss_{m}"].mean() /
                                   (R.coord_primary_fut_thermal - R.coord_primary_fut_cand).abs().mean())
                          for m in ("auc", "cauc", "saucc")}
    H = pd.DataFrame(hist)
    S["g1c_history"] = {k: A.boot_mean(H[k]) for k in ("thermal_auc", "thermal_hist_auc", "thermal_cauc", "thermal_hist_cauc",
                                                        "hist_only_auc")}
    (A.OUT / variant_name("claim14_future_summary.json")).write_text(json.dumps(S, indent=1, default=float), encoding="utf-8")
    print(json.dumps(S["decision"], indent=1, default=float))


def clusters(F, fires):
    """Fires whose study rectangles intersect form one cluster (9.5)."""
    box = {}
    for fid in fires:
        f = F[fid]
        lon, lat = f.df.lon, f.df.lat
        box[fid] = (lon.min(), lon.max(), lat.min(), lat.max())
    parent = {f: f for f in fires}

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x
    for i, a in enumerate(fires):
        for b in fires[i + 1:]:
            A_, B_ = box[a], box[b]
            if A_[0] <= B_[1] and B_[0] <= A_[1] and A_[2] <= B_[3] and B_[2] <= A_[3]:
                parent[find(a)] = find(b)
    return [find(f) for f in fires]


def decide_cols(R, F, ca, cb):
    g = R.dropna(subset=[ca, cb])
    D = (g[ca] - g[cb]).to_numpy()
    cl = np.array(clusters(F, g.fire.tolist()))
    u = np.unique(cl)
    rng = np.random.default_rng(42)
    bs = []
    for _ in range(NB):
        pick = rng.choice(u, len(u))
        idx = np.concatenate([np.where(cl == c)[0] for c in pick])
        bs.append(D[idx].mean())
    lo95, hi95 = np.percentile(bs, [2.5, 97.5])
    lo90, hi90 = np.percentile(bs, [5, 95])
    m = float(D.mean())
    verdict = ("advantage, practically important" if lo95 > 0 and m >= 0.01 else "advantage" if lo95 > 0
               else "equivalence" if lo90 >= -0.01 and hi90 <= 0.01 else "inconclusive")
    return {"fires": int(len(g)), "clusters": int(len(u)), "mean_D": m, "ci95": [float(lo95), float(hi95)],
            "ci90": [float(lo90), float(hi90)], "verdict": verdict}


def decide(R, F, prefix):
    return decide_cols(R, F, f"{prefix}_loss_auc", f"{prefix}_loss_cauc")


if __name__ == "__main__":
    main()
