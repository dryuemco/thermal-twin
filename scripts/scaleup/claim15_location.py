"""claim15_location.py: G2 (plan 10.1), G5 (10.2) and G1d (10.3). Exploratory.

Writes claim15_g2_per_fire.csv and claim15_summary.json (including G5 and G1d).
THERMAL_TWIN_LABEL_SUFFIX unset or empty selects original inputs and names. Set it to _qa1 to read
future_qa1 and the suffixed Claim 14 CSV, and append _qa1 before each output extension. Other values are errors.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
from scipy.spatial import cKDTree
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "geonull"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from label_variant import variant_name  # noqa: E402
import geonull as G  # noqa: E402
import analysis_official as A  # noqa: E402
import claim14_future as C14  # noqa: E402
from s2_label_check_export import regions  # noqa: E402

NUM = [c for c in A.THERMAL if c != A.CAT]
NB = 10_000


def pipe(extra):
    pre = ColumnTransformer([("num", SimpleImputer(strategy="median"), NUM + extra),
                             ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                                               ("oh", OneHotEncoder(handle_unknown="ignore"))]), [A.CAT])])
    return Pipeline([("p", pre), ("clf", C14.rf())])


def oof_extra(f, folds, extra_fn, names):
    o = np.full(f.n, np.nan)
    for tr, te in folds:
        d_tr, d_te = f.df.iloc[tr].copy(), f.df.iloc[te].copy()
        e_tr, e_te = extra_fn(tr, te)
        for i, n in enumerate(names):
            d_tr[n], d_te[n] = e_tr[:, i], e_te[:, i]
        m = pipe(names).fit(d_tr[NUM + names + [A.CAT]], f.y[tr])
        o[te] = m.predict_proba(d_te[NUM + names + [A.CAT]])[:, 1]
    return o


def dist_feature(f):
    blocks = f.blocks(10)

    def fn(tr, te):
        d_tr = np.full(len(tr), np.nan)
        for itr, ite in StratifiedGroupKFold(5, shuffle=True, random_state=A.SEED).split(tr, f.y[tr], groups=blocks[tr]):
            b = tr[itr][f.y[tr[itr]] == 1]
            if len(b):
                d_tr[ite] = cKDTree(f.xy[b]).query(f.xy[tr[ite]])[0]
        bt = tr[f.y[tr] == 1]
        return d_tr[:, None], cKDTree(f.xy[bt]).query(f.xy[te])[0][:, None]
    return fn


def knn_oof(f, folds):
    o = np.full(f.n, np.nan)
    for tr, te in folds:
        o[te] = KNeighborsClassifier(25, weights="distance").fit(f.xy[tr], f.y[tr]).predict_proba(f.xy[te])[:, 1]
    return o


def boot(d, groups):
    d, groups = np.asarray(d, float), np.asarray(groups)
    u = np.unique(groups)
    rng = np.random.default_rng(42)
    bs = [d[np.concatenate([np.where(groups == c)[0] for c in rng.choice(u, len(u))])].mean() for _ in range(NB)]
    return {"mean": float(d.mean()), "lo": float(np.percentile(bs, 2.5)), "hi": float(np.percentile(bs, 97.5))}


def main():
    F = A.load_fires()
    E = pd.read_csv(A.OUT / variant_name("claim14_future_per_fire.csv"))
    ids = E.fire.tolist()
    rows = []
    for fid in ids:
        f = F[fid]
        with rasterio.open(C14.FUT / f"{fid}.tif") as r:
            a = r.read()
        rr, cc = f.df.row_500m.to_numpy(int), f.df.col_500m.to_numpy(int)
        fut_all, unm, fyear = a[0][rr, cc], a[2][rr, cc], a[3][rr, cc]
        pop = (unm <= 0.10) & (f.y == 0)
        yf = (fut_all >= 0.5).astype(int)
        folds = f.folds(10)
        null = f.null_oof(10)
        z, pairs = -null, f.pwd_pairs(10)
        sn = G.standardised_auc(f.y, null, z)["sauc"]
        st = C14.focal_rf(f, A.THERMAL, "thermal")
        cands = {"coord_rf": C14.oof(f.xy, f.y, folds),
                 "thermal_coord": oof_extra(f, folds, lambda tr, te: (f.xy[tr], f.xy[te]), ["x_km", "y_km"]),
                 "thermal_dist": oof_extra(f, folds, dist_feature(f), ["dist_train_burn"]),
                 "coord_knn": knn_oof(f, folds)}
        tm = C14.focal_measures(f, folds, st, null, pairs, z, sn)
        ft = G.auc(yf[pop], st[pop])
        # largest future event removed (10.2)
        ev = C14.events(yf.astype(bool) & pop, np.round(fyear).astype(int), rr - rr.min(), cc - cc.min(),
                        (rr.max() - rr.min() + 1, cc.max() - cc.min() + 1))
        evs, cnt = np.unique(ev[pop & (ev >= 0)], return_counts=True)
        keep = pop & ~(ev == evs[np.argmax(cnt)]) if len(evs) > 1 else pop
        r = {"fire": fid, "year": f.meta["year"], "country": regions.EXPERIMENTS[fid]["country"],
             "fut_thermal": ft, "fut_thermal_nolargest": G.auc(yf[keep], st[keep]) if yf[keep].sum() >= 30 else np.nan}
        for name, s in cands.items():
            cm = C14.focal_measures(f, folds, s, null, pairs, z, sn)
            fc = G.auc(yf[pop], s[pop])
            r[f"{name}_fut"] = fc
            r[f"{name}_fut_nolargest"] = G.auc(yf[keep], s[keep]) if yf[keep].sum() >= 30 else np.nan
            for meas in ("auc", "cauc", "saucc"):
                ch = C14.choose(tm[meas], cm[meas])
                r[f"{name}_choice_{meas}"] = ch or "none"
                r[f"{name}_loss_{meas}"] = C14.loss_for(ch, ft, fc)
                r[f"{name}_focal_{meas}"] = cm[meas]
        rows.append(r)
        print(fid, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items() if k.endswith(("_fut", "choice_auc"))}, flush=True)
    R = pd.DataFrame(rows)
    R.to_csv(A.OUT / variant_name("claim15_g2_per_fire.csv"), index=False)
    cl = C14.clusters(F, R.fire.tolist())
    S = {}
    for name in ("coord_rf", "thermal_coord", "thermal_dist", "coord_knn"):
        d = R.fut_thermal - R[f"{name}_fut"]
        b = boot(d, cl)
        chosen = int((R[f"{name}_choice_auc"] == "c").sum())
        S[name] = {"future_diff_thermal_minus_cand": b, "thermal_better": f"{int((d > 0).sum())} of {len(d)}",
                   **{f"chooses_location_model_{m}": f"{int((R[f'{name}_choice_{m}'] == 'c').sum())} of {len(R)}" for m in ("auc", "cauc", "saucc")},
                   **{f"loss_{m}": float(R[f"{name}_loss_{m}"].mean()) for m in ("auc", "cauc", "saucc")},
                   **{f"relative_loss_{m}": float(R[f"{name}_loss_{m}"].mean() / d.abs().mean()) for m in ("auc", "cauc", "saucc")},
                   "transfer_failure_rule_10_1": bool(chosen >= 12 and b["lo"] > 0)}
    # G5 (10.2)
    g5 = {}
    for name in ("coord_rf", "thermal_coord"):
        d = (R.fut_thermal - R[f"{name}_fut"]).to_numpy()
        out = {}
        for col in ("country", "year"):
            out[f"leave_one_{col}_out"] = {str(k): float(d[(R[col] != k).to_numpy()].mean()) for k in R[col].unique()}
        lofo = [float(np.delete(d, i).mean()) for i in range(len(d))]
        out["leave_one_fire_out_min_max"] = [min(lofo), max(lofo)]
        dn = (R.fut_thermal_nolargest - R[f"{name}_fut_nolargest"]).dropna()
        out["largest_event_removed"] = {"fires": int(len(dn)), "mean_diff": float(dn.mean()), "thermal_better": int((dn > 0).sum())}
        g5[name] = out
    S["g5"] = g5
    S["g1d"] = repeat_pairs(F)
    (A.OUT / variant_name("claim15_summary.json")).write_text(json.dumps(S, indent=1, default=float), encoding="utf-8")
    print(json.dumps({k: v for k, v in S.items() if k != "g5"}, indent=1, default=float)[:4000])
    print(json.dumps(g5, indent=1, default=float)[:2500])


def repeat_pairs(F):
    out = []
    for early, late in (("rp01_2020", "px17_2022"), ("px16_2022", "rp02_2023"), ("evia_2021_extended", "rp03_2023")):
        rec = {"earlier": early, "later": late}
        try:
            T = {}
            for k in (early, late):
                if k in F:
                    T[k] = F[k]
                else:
                    full = pd.read_parquet(A.find_scaleup(k))
                    T[k] = A.Fire(k, full, float(full.lat.mean()), {"year": int(k[-4:])})
        except Exception as exc:                     # later fire without an analysis table
            rec["missing"] = str(exc)[:120]
            out.append(rec)
            continue
        e, l = T[early], T[late]
        rec["dates"] = [regions.EXPERIMENTS[early]["label_start_date"], regions.EXPERIMENTS[late]["label_start_date"]]
        ke = set(zip(e.df.lon.round(5), e.df.lat.round(5)))
        kl = list(zip(l.df.lon.round(5), l.df.lat.round(5)))
        rec["shared_cells"] = int(sum(k in ke for k in kl))
        rec["later_burned"], rec["later_cells"] = int(l.y.sum()), int(l.n)
        m = A.build(A.THERMAL).fit(e.df[A.THERMAL], e.y)
        s_t = m.predict_proba(l.df[A.THERMAL])[:, 1]
        km = lambda d: np.c_[d.lon.to_numpy() * 111.32 * np.cos(np.radians(d.lat.mean())), d.lat.to_numpy() * 110.57]  # noqa: E731
        s_c = C14.rf().fit(km(e.df), e.y).predict_proba(km(l.df))[:, 1]
        rec["later_auc_thermal"], rec["later_auc_coord"] = G.auc(l.y, s_t), G.auc(l.y, s_c)
        folds = e.folds(10)
        st, sc = C14.focal_rf(e, A.THERMAL, "thermal"), C14.oof(e.xy, e.y, folds)
        rec["earlier_focal_auc_thermal"], rec["earlier_focal_auc_coord"] = G.auc(e.y, st), G.auc(e.y, sc)
        rec["earlier_choice_pooled_auc"] = "thermal" if rec["earlier_focal_auc_thermal"] > rec["earlier_focal_auc_coord"] else "coord"
        out.append(rec)
    return out


if __name__ == "__main__":
    main()
