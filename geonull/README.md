# geonull

A predictor-free geographic reference for spatially cross-validated binary maps, in one Python file
(`geonull.py`, needs numpy, scipy and scikit-learn).

Given cell or point coordinates in km, a 0/1 label, the folds of an existing study and the out-of-fold scores
of its model, `evaluate` returns

- the AUC of the model and of the geographic null model of Hijmans (2012), which scores each test cell by minus
  its distance to the nearest positive of the fold's training set;
- the calibrated AUC (cAUC) on distance-matched pairs of positives and negatives, with the share of test
  positives kept;
- the AUC of the fixed scores by distance band of the negatives (0-0.5, 0.5-1, 1-2, 2-5, 5-10, >10 km by
  default), for the model and for the null model.

```python
import geonull as G
res = G.evaluate(xy_km, y, folds, oof_scores)
print(res["auc_model"], res["auc_null"], res["cauc"])
```

`example.py` runs it on a synthetic grid. `test_geonull.py` tests the null scores, the matching, the cAUC
formula and the band assignment against cases with known answers (`python -m pytest geonull -q`).
`check_against_study.py` compares the functions with the study code on the 31 fires of the paper; the largest
difference in null AUC, cAUC and band AUC is below 1e-15.

Hijmans R.J. 2012. Cross-validation of species distribution models: removing spatial sorting bias and
calibration with a null model. Ecology 93, 679-688.
