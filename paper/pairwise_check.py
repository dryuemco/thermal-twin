#!/usr/bin/env python3
"""Cross-check: reproduce two of Emrehan's step9b pairwise raw thermal transfers
with this environment's sklearn, to validate preprocessing equivalence before
trusting LORO comparisons. Expected: montiferru->bejis 0.5483, manavgat->bejis 0.3258."""
import sys
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

STAGING = sys.argv[1]
THERM = ['ndvi_mean', 'elevation_mean', 'slope_mean', 'lst_anomaly_mean', 'current_lst_mean',
         'current_tvdi_mean', 'tvdi_difference_mean', 'downscaled_lst_mean', 'fused_lst_mean']
CAT = 'landcover_dominant'

def load(reg):
    df = pd.read_parquet(f'{STAGING}/{reg}.parquet',
                         columns=['burned', 'valid_for_modeling', 'burnable_tree_shrub_grass', CAT] + THERM)
    return df[(df.valid_for_modeling == True) & (df.burnable_tree_shrub_grass == True)].copy()

def run(src, tgt, expected):
    tr, te = load(src), load(tgt)
    med = tr[THERM].median()
    Xtr_num, Xte_num = tr[THERM].fillna(med), te[THERM].fillna(med)
    mode = tr[CAT].mode().iloc[0]
    tr_cat = tr[CAT].fillna(mode).astype(object)
    te_cat = te[CAT].fillna(mode).astype(object)
    cats = sorted(tr_cat.unique())
    Xtr = pd.concat([Xtr_num] + [pd.Series((tr_cat == c).astype(float), name=f'lc_{c}') for c in cats], axis=1)
    Xte = pd.concat([Xte_num] + [pd.Series((te_cat == c).astype(float), name=f'lc_{c}') for c in cats], axis=1)
    rf = RandomForestClassifier(n_estimators=300, min_samples_leaf=3, class_weight='balanced',
                                random_state=42, n_jobs=-1)
    rf.fit(Xtr.to_numpy(float), tr.burned.astype(int))
    auc = roc_auc_score(te.burned.astype(int), rf.predict_proba(Xte.to_numpy(float))[:, 1])
    print(f'{src} -> {tgt}: ours={auc:.4f} emrehan={expected:.4f} diff={abs(auc-expected):.4f}')

run('montiferru_2021', 'bejis_2022', 0.5483)
run('manavgat_2021', 'bejis_2022', 0.3258)
