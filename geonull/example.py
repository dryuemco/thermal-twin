"""Minimal use of geonull: a grid with one burned patch, a block cross-validation and a noisy model."""
import numpy as np
from sklearn.model_selection import GroupKFold

import geonull as G

r, c = np.mgrid[0:60, 0:60]
xy = np.c_[r.ravel(), c.ravel()].astype(float)                 # cell centres in km
y = (np.hypot(xy[:, 0] - 30, xy[:, 1] - 30) < 12).astype(int)  # burned cells
blocks = (xy[:, 0] // 5).astype(int) * 100 + (xy[:, 1] // 5).astype(int)
folds = list(GroupKFold(5).split(xy, y, blocks))
score = y * 0.3 + np.random.default_rng(0).random(len(y))     # a weak model's out-of-fold scores

res = G.evaluate(xy, y, folds, score)
print(f"model AUC {res['auc_model']:.3f}  null AUC {res['auc_null']:.3f}  cAUC {res['cauc']:.3f}")
for m, n in zip(res["bands_model"], res["bands_null"]):
    print(f"band {m['band']:>8} km  negatives {m['negatives']:5d}  model {m['auc']:.3f}  null {n['auc']:.3f}")
