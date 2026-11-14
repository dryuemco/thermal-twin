"""claim1_combined.py: does the forest add information to the distance to training burns? (amendment 4, post hoc)

The naive version in claim1_robustness.py gives every training cell its distance to the nearest OTHER burned
training cell. Inside one fire that distance is nearly always one cell, while a test cell in a held-out block
is measured to burns outside its block, so the feature has a different distribution at training and test time.
Here the training feature mimics the test geometry: the training cells of an outer fold are split again by
the same 5 km blocks into five inner folds, and a training cell gets its distance to the nearest burned
training cell of the OTHER inner folds. Test cells get their distance to the nearest burned training cell,
as the null model does. Same outer folds, model and predictors as claim 1.

Writes claim1_combined_per_fire.csv and claim1_combined_summary.json in $THERMAL_TWIN_SCALEUP/analysis.
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


def main():
    F = A.load_fires()
    ids = [i for i in F if i != "montiferru_2021"]
    rows = []
    for fid in ids:
        f = F[fid]
        blocks = f.blocks(10)
        s_null, s_rf = f.null_oof(10), f.oof(A.THERMAL, "thermal", "rf", 10)
        o = np.full(f.n, np.nan)
        feats = A.THERMAL + [DIST]
        for tr, te in f.folds(10):
            d_tr = np.full(len(tr), np.nan)
            inner = StratifiedGroupKFold(5, shuffle=True, random_state=A.SEED).split(tr, f.y[tr], groups=blocks[tr])
            for itr, ite in inner:
                b = tr[itr][f.y[tr[itr]] == 1]
                if len(b):
                    d_tr[ite] = cKDTree(f.xy[b]).query(f.xy[tr[ite]])[0]
            bt = tr[f.y[tr] == 1]
            Xtr = f.df.iloc[tr].copy()
            Xtr[DIST] = d_tr
            Xte = f.df.iloc[te].copy()
            Xte[DIST] = cKDTree(f.xy[bt]).query(f.xy[te])[0]
            m = A.build(feats).fit(Xtr[feats], Xtr.burned)
            o[te] = m.predict_proba(Xte[feats])[:, 1]
        near = (f.y == 1) | ((f.y == 0) & (f.dist < 0.5))
        rows.append({"fire": fid, "auc_null": A.auc(f.y, s_null), "auc_rf": A.auc(f.y, s_rf), "auc_combined": A.auc(f.y, o),
                     "near_null": A.auc(f.y[near], s_null[near]), "near_rf": A.auc(f.y[near], s_rf[near]),
                     "near_combined": A.auc(f.y[near], o[near])})
        print(fid, {k: round(v, 3) for k, v in rows[-1].items() if k != "fire"}, flush=True)
    R = pd.DataFrame(rows)
    R.to_csv(A.OUT / "claim1_combined_per_fire.csv", index=False)
    S = {"auc_combined": A.boot_mean(R.auc_combined), "auc_null": A.boot_mean(R.auc_null), "auc_rf": A.boot_mean(R.auc_rf),
         "combined_minus_null": A.boot_mean(R.auc_combined - R.auc_null),
         "combined_beats_null": A.count(R.auc_combined.to_numpy(), R.auc_null.to_numpy()),
         "near_combined": A.boot_mean(R.near_combined), "near_null": A.boot_mean(R.near_null), "near_rf": A.boot_mean(R.near_rf),
         "near_combined_minus_null": A.boot_mean(R.near_combined - R.near_null),
         "near_combined_beats_null": A.count(R.near_combined.to_numpy(), R.near_null.to_numpy())}
    (A.OUT / "claim1_combined_summary.json").write_text(json.dumps(S, indent=1, default=float), encoding="utf-8")
    print(json.dumps(S, indent=1, default=float))


if __name__ == "__main__":
    main()
