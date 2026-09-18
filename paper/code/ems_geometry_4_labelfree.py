"""Analysis 4 (SPEC.md): label-free frame equalisation of the 20-direction transfer.

Target frames use no target label: a1 per-feature range trim, a2 area of applicability
(Meyer & Pebesma 2021, simplified, unweighted), b fixed 20 km (and 15 km) window around
the registry AOI centre. Reference arms full/full and 10km/10km (label-informed collar)
are recomputed in the same run. Also writes Analysis 5's per-direction transfer metrics.
"""
import math

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from sklearn.model_selection import StratifiedGroupKFold

import ems_geometry_common as G

Rs = G.load_regions()


def src_frame(R, tag):
    d = R.df
    if tag == "full":
        return np.ones(len(d), bool)
    if tag == "10km":
        return R.dist_collar <= 10
    if tag.startswith("win"):
        return window(R, float(tag[3:]))
    raise ValueError(tag)


def window(R, side_km):
    bb = G.BBOX[R.name]
    lonc, latc = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
    half = side_km / 2
    dlat = half / (G.M_PER_DEG / 1000)
    dlon = half / (G.M_PER_DEG / 1000 * math.cos(math.radians(latc)))
    return ((R.df.lat - latc).abs() <= dlat).to_numpy() & ((R.df.lon - lonc).abs() <= dlon).to_numpy()


def range_trim(S, T):
    keep = np.ones(len(T), bool)
    for f in G.NUMERIC:
        v = S[f].dropna()
        lo, hi = np.percentile(v, 1), np.percentile(v, 99)
        t = T[f].to_numpy()
        keep &= np.isnan(t) | ((t >= lo) & (t <= hi))
    keep &= T[G.CAT].isin(set(S[G.CAT].dropna().unique())).to_numpy() | T[G.CAT].isna().to_numpy()
    return keep


class AOA:
    def __init__(self, S, blocks):
        X = S[G.NUMERIC]
        self.med = X.median()
        Xi = X.fillna(self.med)
        self.mu, self.sd = Xi.mean(), Xi.std(ddof=0).replace(0, 1)
        Z = ((Xi - self.mu) / self.sd).to_numpy()
        folds = np.full(len(S), -1)
        for k, (_, te) in enumerate(StratifiedGroupKFold(5, shuffle=True, random_state=G.SEED).split(
                Z, S.burned, groups=blocks)):
            folds[te] = k
        di = np.empty(len(S))
        for k in range(5):
            tr = cKDTree(Z[folds != k])
            di[folds == k] = tr.query(Z[folds == k], k=1)[0]
        q1, q3 = np.percentile(di, [25, 75])
        self.thr = float(min(q3 + 1.5 * (q3 - q1), di.max()))
        self.tree = cKDTree(Z)

    def keep(self, T):
        Z = ((T[G.NUMERIC].fillna(self.med) - self.mu) / self.sd).to_numpy()
        return self.tree.query(Z, k=1)[0] <= self.thr


FRAMES = [  # name, source frame, target rule
    ("ref_full_full", "full", "full"), ("ref_10km_10km", "10km", "10km"),
    ("a1_trim_srcfull", "full", "trim"), ("a1_trim_src10km", "10km", "trim"),
    ("a2_aoa_srcfull", "full", "aoa"), ("a2_aoa_src10km", "10km", "aoa"),
    ("b_win20_win20", "win20", "win20"), ("b_full_win20", "full", "win20"), ("b_10km_win20", "10km", "win20"),
    ("b_win15_win15", "win15", "win15"),
]
models, aoas = {}, {}
for tag in sorted({f[1] for f in FRAMES}):
    for reg, R in Rs.items():
        m = src_frame(R, tag)
        S = R.df[m]
        if S.burned.nunique() < 2:
            print(f"source {reg} frame {tag}: single class, no model", flush=True)
            continue
        models[(reg, tag)] = {lbl: G.fit(fe, S, S.burned) for lbl, fe in (("thermal", G.THERMAL), ("baseline", G.BASELINE))}
        print(f"fitted {reg} {tag} n={len(S)} pos={int(S.burned.sum())}", flush=True)

rows, mrows, ret = [], [], []
for name, sf, tf in FRAMES:
    for s in G.REGIONS:
        if (s, sf) not in models:
            continue
        S = Rs[s].df[src_frame(Rs[s], sf)]
        if tf == "aoa" and (s, sf) not in aoas:
            aoas[(s, sf)] = AOA(S, Rs[s].block10[src_frame(Rs[s], sf)])
        for t in G.REGIONS:
            if s == t:
                continue
            RT = Rs[t]
            if tf in ("full", "10km") or tf.startswith("win"):
                keep = src_frame(RT, tf)
            elif tf == "trim":
                keep = range_trim(S, RT.df)
            else:
                keep = aoas[(s, sf)].keep(RT.df)
            T = RT.df[keep]
            row = {"frame": name, "source_frame": sf, "target_rule": tf, "source": s, "target": t,
                   "target_n": int(len(T)), "target_pos": int(T.burned.sum()),
                   "target_retained": float(keep.mean()), "target_pos_retained": float(T.burned.sum() / RT.y.sum())}
            if T.burned.nunique() == 2:
                sc = {lbl: models[(s, sf)][lbl].predict_proba(T[fe])[:, 1]
                      for lbl, fe in (("thermal", G.THERMAL), ("baseline", G.BASELINE))}
                row["thermal"] = G.auc(T.burned, sc["thermal"])
                row["baseline"] = G.auc(T.burned, sc["baseline"])
                row["delta"] = row["thermal"] - row["baseline"]
                for lbl in ("thermal", "baseline"):
                    mm = G.metric_set(T.burned.to_numpy(), sc[lbl])
                    mrows.append({"frame": name, "source": s, "target": t, "model": lbl, **mm})
            rows.append(row)
    print(f"frame {name} done", flush=True)

D = pd.DataFrame(rows)
D.to_csv(G.OUT / "a4_transfer_by_direction.csv", index=False)
pd.DataFrame(mrows).to_csv(G.OUT / "a5_transfer_metrics_by_direction.csv", index=False)
summ = []
for name, sf, tf in FRAMES:
    s = D[(D.frame == name)].dropna(subset=["thermal"])
    delta = {(a, b): v for a, b, v in zip(s.source, s.target, s.delta)}
    pc = G.pair_cluster_ci(delta) if len(delta) >= 4 else (np.nan, np.nan)
    tc = G.target_cluster_ci(delta) if len(delta) >= 4 else (np.nan, np.nan)
    summ.append({"frame": name, "source_frame": sf, "target_rule": tf, "directions": int(len(s)),
                 "mean_thermal": s.thermal.mean(), "above_0_5": int((s.thermal > 0.5).sum()),
                 "below_0_5": int((s.thermal < 0.5).sum()), "mean_baseline": s.baseline.mean(),
                 "mean_delta": s.delta.mean(), "delta_pair_cluster": list(pc), "delta_target_cluster": list(tc),
                 "median_target_retained": float(s.target_retained.median()),
                 "median_target_pos_retained": float(s.target_pos_retained.median()),
                 "median_target_prevalence": float((s.target_pos / s.target_n).median())})
G.dump({"frames": summ,
        "aoa_thresholds": {f"{k[0]}|{k[1]}": v.thr for k, v in aoas.items()},
        "window_counts": {f"{r}|{w}": {"n": int(window(R, w).sum()), "pos": int(R.y[window(R, w)].sum())}
                          for r, R in Rs.items() for w in (15.0, 20.0)}}, "a4_summary.json")
pd.set_option("display.width", 250)
print(pd.DataFrame(summ).round(4).to_string())
