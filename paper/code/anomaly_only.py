#!/usr/bin/env python3
"""Analysis 3 - effect of dropping direction-reversing features on transfer.

Configs (thermal model variants, feature order preserved from SHARED_THERMAL_MODEL_FEATURES):
  full        : all 10 features (reference; must reproduce step9b exactly)
  drop_elev   : minus elevation_mean
  drop_anom   : minus lst_anomaly_mean
  drop_both   : minus both (all bootstrap-supported reversal features, Analysis 1)

Transfers: all 20 ordered directions, source-only training on TSG primary population,
paired spatial-block bootstrap (10-cell ~5 km blocks on target, 1000 reps, seed 42) for
per-direction delta AUC (config minus full).
Within-region: step8b OOF spatial-block CV replicated exactly (StratifiedGroupKFold 5,
shuffle, seed 42, 2-cell blocks, per-population training); full config must reproduce
step8c TSG thermal AUC; within deltas get paired 10-cell block bootstrap CIs.
Hard asserts: full-config transfer must match step9b (<5e-4); full-config within must
match step8c (<1e-3). Any deviation -> abort.
"""
import json, sys, time
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.metrics import roc_auc_score

STAGING = sys.argv[1]
OUT = sys.argv[2]

REGIONS = ['manavgat_2021', 'bejis_2022', 'mugla_2021', 'evia_2021_extended', 'montiferru_2021']
THERMAL_FEATURES = ['ndvi_mean', 'elevation_mean', 'slope_mean', 'landcover_dominant',
                    'lst_anomaly_mean', 'current_lst_mean', 'current_tvdi_mean',
                    'tvdi_difference_mean', 'downscaled_lst_mean', 'fused_lst_mean']
CAT = 'landcover_dominant'
# Referee round 4, R3-M8. The two internally normalised dryness channels
# (lst_anomaly_mean, tvdi_difference_mean) are the ones that do NOT reverse sign
# between regions; the four absolute-surface-state channels are the ones that do.
# The introduction hypothesises that normalised channels should be more portable
# and the paper never tested it as a feature-set contrast. These configs test it.
BASELINE = ['ndvi_mean', 'elevation_mean', 'slope_mean', 'landcover_dominant']
ANOMALY_CHANNELS = ['lst_anomaly_mean', 'tvdi_difference_mean']
ABSOLUTE_CHANNELS = ['current_lst_mean', 'current_tvdi_mean',
                     'downscaled_lst_mean', 'fused_lst_mean']
CONFIGS = {
    'full': THERMAL_FEATURES,
    'drop_elev': [f for f in THERMAL_FEATURES if f != 'elevation_mean'],
    'drop_anom': [f for f in THERMAL_FEATURES if f != 'lst_anomaly_mean'],
    'drop_both': [f for f in THERMAL_FEATURES if f not in ('elevation_mean', 'lst_anomaly_mean')],
    'baseline_only': BASELINE,
    'anomaly_only': BASELINE + ANOMALY_CHANNELS,
    'absolute_only': BASELINE + ABSOLUTE_CHANNELS,
    # Referee E-M9. downscaled_lst and fused_lst come from a per-region model
    # whose own inputs include coordinates. A coordinate-smoothed surface is by
    # construction locally informative and non-portable, which is this paper's
    # result in miniature, so the increment must be shown to survive without it.
    'no_coord_channels': [f for f in THERMAL_FEATURES
                          if f not in ('downscaled_lst_mean', 'fused_lst_mean')],
}
SEED = 42
NBOOT = 1000

cmp_inputs = json.load(open(f'{STAGING}/comparison_inputs.json'))

def build_pipeline(feature_list):
    numeric = [f for f in feature_list if f != CAT]
    transformers = [('num', Pipeline([('imputer', SimpleImputer(strategy='median'))]), numeric)]
    if CAT in feature_list:
        transformers.append(('cat', Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore')),
        ]), [CAT]))
    return Pipeline([('preprocess', ColumnTransformer(transformers)),
                     ('clf', RandomForestClassifier(n_estimators=300, min_samples_leaf=3,
                                                    class_weight='balanced', random_state=SEED,
                                                    n_jobs=-1))])

def load_region(reg):
    df = pd.read_parquet(f'{STAGING}/{reg}.parquet',
                         columns=['burned', 'valid_for_modeling', 'burnable_tree_shrub_grass',
                                  'row_500m', 'col_500m'] + THERMAL_FEATURES)
    return df[(df.valid_for_modeling == True) & (df.burnable_tree_shrub_grass == True)].reset_index(drop=True)

data = {r: load_region(r) for r in REGIONS}
print('regions loaded', flush=True)

def block_ids(df, size):
    return ((df.row_500m.astype(int) // size).astype(str) + '_' +
            (df.col_500m.astype(int) // size).astype(str)).to_numpy()

def paired_block_bootstrap(y, prob_by_config, blocks, rng):
    """Resample 10-cell blocks once per replicate; compute AUC for every config and
    deltas vs full on the same index set (paired)."""
    uniq = np.unique(blocks)
    idx_by_block = {b: np.where(blocks == b)[0] for b in uniq}
    reps = {k: [] for k in prob_by_config}
    deltas = {k: [] for k in prob_by_config if k != 'full'}
    skipped = 0
    for _ in range(NBOOT):
        sel = rng.choice(uniq, size=len(uniq), replace=True)
        idx = np.concatenate([idx_by_block[b] for b in sel])
        yy = y[idx]
        if yy.min() == yy.max():
            skipped += 1
            continue
        aucs = {k: roc_auc_score(yy, p[idx]) for k, p in prob_by_config.items()}
        for k, v in aucs.items():
            reps[k].append(v)
        for k in deltas:
            deltas[k].append(aucs[k] - aucs['full'])
    ci = lambda a: [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))]
    return ({k: ci(v) for k, v in reps.items()},
            {k: ci(v) for k, v in deltas.items()},
            len(next(iter(reps.values()))), skipped)

# ---------------- transfers ----------------
print('=== transfers ===', flush=True)
transfer_rows = []
for src in REGIONS:
    fitted = {}
    for cfg, feats in CONFIGS.items():
        t0 = time.time()
        pipe = build_pipeline(feats)
        pipe.fit(data[src][feats], data[src].burned.astype(int))
        fitted[cfg] = pipe
        print(f'  fit {src} {cfg} ({time.time()-t0:.0f}s)', flush=True)
    for tgt in REGIONS:
        if tgt == src:
            continue
        y = data[tgt].burned.astype(int).to_numpy()
        probs = {cfg: fitted[cfg].predict_proba(data[tgt][CONFIGS[cfg]])[:, 1] for cfg in CONFIGS}
        aucs = {cfg: float(roc_auc_score(y, p)) for cfg, p in probs.items()}
        expected = cmp_inputs['transfer'][f'{src}_to_{tgt}']['thermal']
        if abs(aucs['full'] - expected) > 5e-4:
            raise SystemExit(f'ABORT: full-config transfer {src}->{tgt} = {aucs["full"]:.4f} '
                             f'vs step9b {expected:.4f} (diff {abs(aucs["full"]-expected):.4f})')
        rng = np.random.default_rng(SEED)
        cfg_ci, delta_ci, nval, nskip = paired_block_bootstrap(y, probs, block_ids(data[tgt], 10), rng)
        row = dict(direction=f'{src}_to_{tgt}', source=src, target=tgt,
                   auc={k: round(v, 6) for k, v in aucs.items()},
                   delta_vs_full={k: round(aucs[k] - aucs['full'], 6) for k in CONFIGS if k != 'full'},
                   auc_ci=cfg_ci, delta_ci=delta_ci, n_valid_reps=nval, n_skipped_reps=nskip,
                   step9b_check_diff=round(abs(aucs['full'] - expected), 6))
        transfer_rows.append(row)
        d = row['delta_vs_full']
        print(f'{src}->{tgt} full={aucs["full"]:.4f} dElev={d["drop_elev"]:+.4f}'
              f'[{delta_ci["drop_elev"][0]:+.3f},{delta_ci["drop_elev"][1]:+.3f}] '
              f'dAnom={d["drop_anom"]:+.4f} dBoth={d["drop_both"]:+.4f}'
              f'[{delta_ci["drop_both"][0]:+.3f},{delta_ci["drop_both"][1]:+.3f}]', flush=True)

# ---------------- within-region (step8b OOF replication) ----------------
print('=== within-region OOF CV ===', flush=True)
def make_folds(y, groups):
    for n in (5, 4, 3, 2):
        try:
            sgk = StratifiedGroupKFold(n_splits=n, shuffle=True, random_state=SEED)
            folds = list(sgk.split(np.zeros(len(y)), y, groups))
        except Exception:
            continue
        if all(y[te].sum() > 0 for _, te in folds):
            return folds, n
    raise SystemExit('no valid folds')

within_rows = []
for reg in REGIONS:
    df = data[reg]
    y = df.burned.astype(int).to_numpy()
    folds, n_used = make_folds(y, block_ids(df, 2))
    oof = {cfg: np.full(len(df), np.nan) for cfg in CONFIGS}
    for tr_idx, te_idx in folds:
        for cfg, feats in CONFIGS.items():
            pipe = build_pipeline(feats)
            pipe.fit(df.iloc[tr_idx][feats], y[tr_idx])
            oof[cfg][te_idx] = pipe.predict_proba(df.iloc[te_idx][feats])[:, 1]
    aucs = {cfg: float(roc_auc_score(y, oof[cfg])) for cfg in CONFIGS}
    expected = cmp_inputs['within'][reg]['thermal_auc']
    if abs(aucs['full'] - expected) > 1e-3:
        raise SystemExit(f'ABORT: within {reg} full OOF AUC {aucs["full"]:.4f} vs step8c '
                         f'{expected:.4f} (diff {abs(aucs["full"]-expected):.4f})')
    rng = np.random.default_rng(SEED)
    cfg_ci, delta_ci, nval, nskip = paired_block_bootstrap(y, oof, block_ids(df, 10), rng)
    within_rows.append(dict(region=reg, n_splits_used=n_used,
                            auc={k: round(v, 6) for k, v in aucs.items()},
                            delta_vs_full={k: round(aucs[k] - aucs['full'], 6) for k in CONFIGS if k != 'full'},
                            auc_ci=cfg_ci, delta_ci=delta_ci, n_valid_reps=nval, n_skipped_reps=nskip,
                            step8c_check_diff=round(abs(aucs['full'] - expected), 6)))
    d = within_rows[-1]['delta_vs_full']
    print(f'{reg} full={aucs["full"]:.4f} (step8c diff {abs(aucs["full"]-expected):.4f}) '
          f'dElev={d["drop_elev"]:+.4f} dAnom={d["drop_anom"]:+.4f} dBoth={d["drop_both"]:+.4f}', flush=True)

# ---------------- trade-off summary ----------------
summary = {}
for cfg in CONFIGS:
    tr_aucs = [r['auc'][cfg] for r in transfer_rows]
    summary[cfg] = dict(
        mean_within_auc=float(np.mean([r['auc'][cfg] for r in within_rows])),
        mean_transfer_auc=float(np.mean(tr_aucs)),
        n_dirs_point_above_chance=int(sum(a > 0.5 for a in tr_aucs)),
        n_dirs_ci_above_chance=int(sum(r['auc_ci'][cfg][0] > 0.5 for r in transfer_rows)),
        mean_transfer_delta_manavgat_dirs=float(np.mean([r['delta_vs_full'].get(cfg, 0.0) for r in transfer_rows
                                                         if 'manavgat_2021' in (r['source'], r['target'])])) if cfg != 'full' else 0.0,
        mean_transfer_delta_other_dirs=float(np.mean([r['delta_vs_full'].get(cfg, 0.0) for r in transfer_rows
                                                      if 'manavgat_2021' not in (r['source'], r['target'])])) if cfg != 'full' else 0.0,
    )

json.dump(dict(transfers=transfer_rows, within=within_rows, tradeoff=summary), open(OUT, 'w'), indent=1)
print('written', OUT, flush=True)
