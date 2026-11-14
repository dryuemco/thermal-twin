"""claim1_robustness.py: robustness checks of claim 1 asked for by the review (plan amendment 4, post hoc).

For every fire of the primary set, 5 km design unless stated:
  combined  THERMAL predictors plus the distance to the nearest burned training cell, in the same folds
            (training cells: distance to the nearest OTHER burned training cell), against the null model alone;
            whole population and nearest distance band
  foldwise  AUC within each test fold, mean weighted by fold size, for the null model and the thermal RF
  designs   block grid shifted by half a block (5 cells) and fold seeds 7 and 2026, with and without the shift:
            null model against the thermal RF, refitted in each design
  folds20   per-fold counts of blocks, burned and unburned cells in the 20 km design
  matching  calibrated AUC for tolerances 0.20, 0.33 and 0.50 and three orders of the burned cells (seeds 42,
            1, 2); kept burned and unburned cells and the distance to the nearest training burn of kept and
            dropped burned cells
Writes claim1_robustness_per_fire.csv, claim1_robustness_designs.csv, claim1_folds20.csv,
claim1_matching.csv and claim1_robustness_summary.json in $THERMAL_TWIN_SCALEUP/analysis.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from sklearn.model_selection import StratifiedGroupKFold

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analysis_official as A  # noqa: E402

DIST = "dist_to_training_burn"
DESIGNS = [(0, 7), (0, 2026), (5, 42), (5, 7), (5, 2026)]      # (block shift in cells, fold seed); (0, 42) is the main design
TOLS, ORDER_SEEDS = (0.20, 0.33, 0.50), (42, 1, 2)


def folds(f, k, shift=0, seed=A.SEED):
    d = f.df
    g = (((d.row_500m + shift) // k).astype(int).astype(str) + "_" + ((d.col_500m + shift) // k).astype(int).astype(str)).to_numpy()
    return list(StratifiedGroupKFold(5, shuffle=True, random_state=seed).split(d[A.THERMAL], d.burned, groups=g)), g


def null_and_rf(f, fl):
    o_null, o_rf = np.full(f.n, np.nan), np.full(f.n, np.nan)
    for tr, te in fl:
        b = tr[f.y[tr] == 1]
        o_null[te] = -cKDTree(f.xy[b]).query(f.xy[te])[0]
        m = A.build(A.THERMAL).fit(f.df.iloc[tr][A.THERMAL], f.df.burned.iloc[tr])
        o_rf[te] = m.predict_proba(f.df.iloc[te][A.THERMAL])[:, 1]
    return o_null, o_rf


def combined(f, fl):
    o = np.full(f.n, np.nan)
    feats = A.THERMAL + [DIST]
    for tr, te in fl:
        b = tr[f.y[tr] == 1]
        tree = cKDTree(f.xy[b])
        d_tr = tree.query(f.xy[tr], k=2)[0]
        dist_tr = np.where(f.y[tr] == 1, d_tr[:, 1], d_tr[:, 0])     # a burned training cell is not its own neighbour
        Xtr = f.df.iloc[tr].copy()
        Xtr[DIST] = dist_tr
        Xte = f.df.iloc[te].copy()
        Xte[DIST] = tree.query(f.xy[te])[0]
        m = A.build(feats).fit(Xtr[feats], Xtr.burned)
        o[te] = m.predict_proba(Xte[feats])[:, 1]
    return o


def pairs(f, fl, s_rf, s_null, tol, seed):
    dtr = np.full(f.n, np.nan)
    for tr, te in fl:
        b = tr[f.y[tr] == 1]
        dtr[te] = cKDTree(f.xy[b]).query(f.xy[te])[0]
    rng = np.random.default_rng(seed)
    keep, kept_pos = [], []
    for _, te in fl:
        pos, neg = te[f.y[te] == 1], te[f.y[te] == 0]
        if not len(pos) or not len(neg):
            continue
        order = np.argsort(dtr[neg], kind="stable")
        nd, used = dtr[neg][order], np.zeros(len(neg), bool)
        for p in rng.permutation(pos):
            dp = dtr[p]
            j = int(np.searchsorted(nd, dp))
            lo, hi = j - 1, j
            while lo >= 0 and used[lo]:
                lo -= 1
            while hi < len(nd) and used[hi]:
                hi += 1
            c = [i for i in (lo, hi) if 0 <= i < len(nd)]
            if not c:
                break
            best = min(c, key=lambda i: abs(nd[i] - dp))
            if abs(nd[best] - dp) <= tol * max(dp, A.PWD_FLOOR_KM):
                used[best] = True
                keep += [p, neg[order[best]]]
                kept_pos.append(p)
    keep = np.array(keep, int)
    kp = np.zeros(f.n, bool)
    kp[np.array(kept_pos, int)] = True
    a_null = A.auc(f.y[keep], s_null[keep]) if len(keep) else np.nan
    a_rf = A.auc(f.y[keep], s_rf[keep]) if len(keep) else np.nan
    burned = f.y == 1
    return {"pairs": int(len(keep) // 2), "kept_share": float(kp[burned].mean()),
            "auc_rf_pairs": a_rf, "auc_null_pairs": a_null, "cauc": a_rf + 0.5 - max(0.5, a_null),
            "dist_kept_burned_median_km": float(np.median(dtr[burned & kp])) if (burned & kp).any() else np.nan,
            "dist_dropped_burned_median_km": float(np.median(dtr[burned & ~kp])) if (burned & ~kp).any() else np.nan}


def main():
    F = A.load_fires()
    ids = [i for i in F if i != "montiferru_2021"]
    rows, drows, f20, mrows = [], [], [], []
    for fid in ids:
        f = F[fid]
        fl, _ = folds(f, 10)
        s_rf, s_null = f.oof(A.THERMAL, "thermal", "rf", 10), f.null_oof(10)
        o_c = combined(f, fl)
        near = (f.y == 1) | ((f.y == 0) & (f.dist < 0.5))
        w = np.array([len(te) for _, te in fl], float)
        fold_rf = np.array([A.auc(f.y[te], s_rf[te]) for _, te in fl])
        fold_null = np.array([A.auc(f.y[te], s_null[te]) for _, te in fl])
        okf = np.isfinite(fold_rf) & np.isfinite(fold_null)
        rows.append({"fire": fid, "auc_null": A.auc(f.y, s_null), "auc_rf": A.auc(f.y, s_rf), "auc_combined": A.auc(f.y, o_c),
                     "near_null": A.auc(f.y[near], s_null[near]), "near_rf": A.auc(f.y[near], s_rf[near]),
                     "near_combined": A.auc(f.y[near], o_c[near]),
                     "foldwise_null": float(np.average(fold_null[okf], weights=w[okf])),
                     "foldwise_rf": float(np.average(fold_rf[okf], weights=w[okf])), "folds_scored": int(okf.sum())})
        for shift, seed in DESIGNS:
            fl2, _ = folds(f, 10, shift, seed)
            on, orf = null_and_rf(f, fl2)
            drows.append({"fire": fid, "shift": shift, "seed": seed, "auc_null": A.auc(f.y, on), "auc_rf": A.auc(f.y, orf)})
        if len(np.unique(f.blocks(40))) >= 5:
            fl40, g40 = folds(f, 40)
            for i, (_, te) in enumerate(fl40):
                f20.append({"fire": fid, "fold": i, "blocks": int(len(np.unique(g40[te]))),
                            "burned": int((f.y[te] == 1).sum()), "unburned": int((f.y[te] == 0).sum())})
        for tol in TOLS:
            for sd in ORDER_SEEDS:
                mrows.append({"fire": fid, "tol": tol, "order_seed": sd, **pairs(f, fl, s_rf, s_null, tol, sd)})
        print(fid, round(rows[-1]["auc_null"], 3), round(rows[-1]["auc_rf"], 3), round(rows[-1]["auc_combined"], 3), flush=True)
    R, D, P20, M = pd.DataFrame(rows), pd.DataFrame(drows), pd.DataFrame(f20), pd.DataFrame(mrows)
    for name, t in (("claim1_robustness_per_fire", R), ("claim1_robustness_designs", D), ("claim1_folds20", P20), ("claim1_matching", M)):
        t.to_csv(A.OUT / f"{name}.csv", index=False)
    S = {
        "combined": {"auc_combined": A.boot_mean(R.auc_combined), "auc_null": A.boot_mean(R.auc_null),
                     "combined_beats_null": A.count(R.auc_combined.to_numpy(), R.auc_null.to_numpy()),
                     "near_combined": A.boot_mean(R.near_combined), "near_null": A.boot_mean(R.near_null),
                     "near_combined_beats_null": A.count(R.near_combined.to_numpy(), R.near_null.to_numpy()),
                     "combined_minus_null": A.boot_mean(R.auc_combined - R.auc_null),
                     "near_combined_minus_null": A.boot_mean(R.near_combined - R.near_null)},
        "foldwise": {"null": A.boot_mean(R.foldwise_null), "rf": A.boot_mean(R.foldwise_rf),
                     "null_beats_rf": A.count(R.foldwise_null.to_numpy(), R.foldwise_rf.to_numpy())},
        "designs": {f"shift{s}_seed{sd}": {"null_beats_rf": A.count(g.auc_null.to_numpy(), g.auc_rf.to_numpy()),
                                           "auc_null": A.boot_mean(g.auc_null), "auc_rf": A.boot_mean(g.auc_rf)}
                    for (s, sd), g in D.groupby(["shift", "seed"])},
        "folds20": {"fires": int(P20.fire.nunique()), "min_blocks": int(P20.blocks.min()), "min_burned": int(P20.burned.min()),
                    "min_unburned": int(P20.unburned.min()), "median_blocks": float(P20.blocks.median())},
        "matching": {f"tol{t}_seed{s}": {"cauc": A.boot_mean(g.cauc), "kept_share": A.boot_mean(g.kept_share),
                                         "auc_null_pairs": A.boot_mean(g.auc_null_pairs)}
                     for (t, s), g in M.groupby(["tol", "order_seed"])},
        "matching_distances_main": {"kept_burned_median_km": A.boot_mean(M[(M.tol == 0.33) & (M.order_seed == 42)].dist_kept_burned_median_km),
                                    "dropped_burned_median_km": A.boot_mean(M[(M.tol == 0.33) & (M.order_seed == 42)].dist_dropped_burned_median_km)},
    }
    (A.OUT / "claim1_robustness_summary.json").write_text(json.dumps(S, indent=1, default=float), encoding="utf-8")
    print(json.dumps(S, indent=1, default=float))


if __name__ == "__main__":
    main()
