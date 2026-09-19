#!/usr/bin/env python3
"""Analysis 2 - Leave-one-region-out (LORO) pooled multi-region training.

For each held-out target region: pool the other four regions' primary populations
(valid_for_modeling AND burnable_tree_shrub_grass), train RF (300 trees, msl=3,
class_weight=balanced, seed 42), evaluate on the held-out region.
Feature sets: baseline / thermal. Scaling variants: raw / regionwise z-score
(per-region mean/sd ddof=0 over primary rows, numeric features only, target scaled
with its own stats - label-free, Step10 definition).
Preprocessing mirrors Emrehan step9b: numeric median imputation (fit on training pool),
categorical landcover one-hot with handle_unknown=ignore.
Metrics on target: ROC-AUC, PR-AUC (with no-skill base = prevalence), Brier.
Spatial-block bootstrap 95% CI on target (blocks row_500m//10 x col_500m//10 ~5km,
1000 reps, numpy default_rng(42)).
"""
import json, sys, time
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "code"))
import _canonical  # noqa: E402  (labelfix re-run 2026-09-19: inputs via _canonical.load)

STAGING = sys.argv[1]
OUT = sys.argv[2]
ONLY = sys.argv[3] if len(sys.argv) > 3 else None  # optional single fold for timing

REGIONS = ['manavgat_2021', 'bejis_2022', 'mugla_2021', 'evia_2021_extended', 'montiferru_2021']
BASE_NUM = ['ndvi_mean', 'elevation_mean', 'slope_mean']
THERM_NUM = BASE_NUM + ['lst_anomaly_mean', 'current_lst_mean', 'current_tvdi_mean',
                        'tvdi_difference_mean', 'downscaled_lst_mean', 'fused_lst_mean']
CAT = 'landcover_dominant'
NBOOT = 1000
SEED = 42

def load_region(reg):
    df = _canonical.load(reg,
                         columns=['burned', 'valid_for_modeling', 'burnable_tree_shrub_grass',
                                  'row_500m', 'col_500m', CAT] + THERM_NUM)
    df = df[(df.valid_for_modeling == True) & (df.burnable_tree_shrub_grass == True)].copy()
    df['region'] = reg
    df['block'] = (df.row_500m // 10).astype(int).astype(str) + '_' + (df.col_500m // 10).astype(int).astype(str)
    return df

def zscore_regionwise(df, num_cols):
    out = df.copy()
    for reg, g in df.groupby('region'):
        mu = g[num_cols].mean()
        sd = g[num_cols].std(ddof=0).replace(0, 1.0)
        out.loc[g.index, num_cols] = (g[num_cols] - mu) / sd
    return out

def build_xy(train, test, num_cols):
    med = train[num_cols].median()
    Xtr_num = train[num_cols].fillna(med)
    Xte_num = test[num_cols].fillna(med)
    tr_cat = train[CAT].astype('object')
    te_cat = test[CAT].astype('object')
    mode = tr_cat.mode().iloc[0]
    tr_cat = tr_cat.fillna(mode); te_cat = te_cat.fillna(mode)
    cats = sorted(tr_cat.unique())  # handle_unknown=ignore -> unseen target cats all-zero
    Xtr_cat = pd.DataFrame({f'lc_{c}': (tr_cat == c).astype(float) for c in cats}, index=train.index)
    Xte_cat = pd.DataFrame({f'lc_{c}': (te_cat == c).astype(float) for c in cats}, index=test.index)
    Xtr = pd.concat([Xtr_num, Xtr_cat], axis=1)
    Xte = pd.concat([Xte_num, Xte_cat], axis=1)
    return Xtr.to_numpy(float), train.burned.astype(int).to_numpy(), Xte.to_numpy(float), test.burned.astype(int).to_numpy()

def metrics(y, p):
    return dict(roc_auc=float(roc_auc_score(y, p)),
                pr_auc=float(average_precision_score(y, p)),
                brier=float(brier_score_loss(y, p)),
                prevalence=float(y.mean()))

def block_bootstrap_ci(y, p, blocks, rng):
    uniq = np.unique(blocks)
    idx_by_block = {b: np.where(blocks == b)[0] for b in uniq}
    rocs, prs, briers = [], [], []
    skipped = 0
    for _ in range(NBOOT):
        sel = rng.choice(uniq, size=len(uniq), replace=True)
        idx = np.concatenate([idx_by_block[b] for b in sel])
        yy, pp = y[idx], p[idx]
        if yy.min() == yy.max():
            skipped += 1
            continue
        rocs.append(roc_auc_score(yy, pp))
        prs.append(average_precision_score(yy, pp))
        briers.append(brier_score_loss(yy, pp))
    q = lambda a: [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))]
    return dict(roc_auc_ci=q(rocs), pr_auc_ci=q(prs), brier_ci=q(briers),
                n_valid=len(rocs), n_skipped=skipped)

print('loading regions...', flush=True)
data = {r: load_region(r) for r in REGIONS}
for r, df in data.items():
    print(f'  {r}: n={len(df)} burned={int(df.burned.sum())} prev={df.burned.mean():.4f}', flush=True)

results = []
targets = [ONLY] if ONLY else REGIONS
for target in targets:
    pool_regions = [r for r in REGIONS if r != target]
    train_all = pd.concat([data[r] for r in pool_regions], ignore_index=False)
    test_all = data[target]
    for scaling in ['raw', 'regionwise_z']:
        if scaling == 'regionwise_z':
            combined = pd.concat([train_all, test_all])
            combined = zscore_regionwise(combined, THERM_NUM)
            tr = combined[combined.region != target]
            te = combined[combined.region == target]
        else:
            tr, te = train_all, test_all
        for feats_name, num_cols in [('baseline', BASE_NUM), ('thermal', THERM_NUM)]:
            t0 = time.time()
            Xtr, ytr, Xte, yte = build_xy(tr, te, num_cols)
            _canonical.assert_no_leakage(num_cols + [CAT])
            rf = RandomForestClassifier(n_estimators=300, min_samples_leaf=3,
                                        class_weight='balanced', random_state=SEED, n_jobs=4)
            rf.fit(Xtr, ytr)
            p = rf.predict_proba(Xte)[:, 1]
            m = metrics(yte, p)
            rng = np.random.default_rng(SEED)
            ci = block_bootstrap_ci(yte, p, te.block.to_numpy(), rng)
            dt = time.time() - t0
            row = dict(target=target, pool='+'.join(pool_regions), scaling=scaling,
                       feature_set=feats_name, n_train=len(ytr), n_test=len(yte),
                       train_prevalence=float(ytr.mean()), **m, **ci, seconds=round(dt, 1))
            results.append(row)
            print(f'{target} {scaling:12s} {feats_name:8s} AUC={m["roc_auc"]:.4f} '
                  f'[{ci["roc_auc_ci"][0]:.4f},{ci["roc_auc_ci"][1]:.4f}] PR={m["pr_auc"]:.4f} '
                  f'(no-skill {m["prevalence"]:.3f}) Brier={m["brier"]:.4f} ({dt:.0f}s)', flush=True)

with open(OUT, 'w') as f:
    json.dump(results, f, indent=1)
print('written', OUT, flush=True)
