// Package Analysis 3 results into paper/feature_drop_transfer.{json,csv}
import { readFileSync, writeFileSync } from 'fs';

const ROOT = 'C:/Users/CORSAIR/projects/thermal-twin';
const S = process.argv[2];
const j = JSON.parse(readFileSync(`${S}/staging/feature_drop.json`, 'utf8'));
const CONFIGS = ['full', 'drop_elev', 'drop_anom', 'drop_both'];

const meta = {
  created: '2026-08-08',
  analysis: 'Analysis 3 - effect of dropping bootstrap-supported direction-reversing features (elevation_mean, lst_anomaly_mean; set fixed by Analysis 1) on cross-region transfer and within-region skill',
  configs: {
    full: 'all 10 thermal-model features (step9b reference)',
    drop_elev: 'minus elevation_mean',
    drop_anom: 'minus lst_anomaly_mean',
    drop_both: 'minus both reversal features',
  },
  population: 'valid_for_modeling AND burnable_tree_shrub_grass',
  model: 'RF(300, min_samples_leaf=3, class_weight=balanced, random_state=42), step8b/step9b pipeline (ColumnTransformer: median imputer on numerics in list order, most_frequent+one-hot handle_unknown=ignore on landcover)',
  environment: 'WSL Ubuntu-22.04, micromamba: python 3.12, scikit-learn 1.9.0 (exact Emrehan version), pandas 3.0.5, numpy 2.5.1',
  parity_asserts: {
    transfers: 'full-config AUC vs step9b enforced <5e-4 for all 20 directions (max observed diff in step9b_check_diff per row)',
    within: 'full-config OOF AUC vs step8c TSG thermal enforced <1e-3; observed diff 0.0000 in all five regions (StratifiedGroupKFold n=5, shuffle, seed 42, 2-cell blocks, per-population training replicating repo step8b)',
  },
  bootstrap: 'paired spatial-block bootstrap: 10-cell (~5 km) blocks on the evaluation region, 1000 replicates, numpy default_rng(42); same resampled blocks evaluate every config, delta = config - full per replicate; percentile 95% CI. Note: step8c\'s own within CIs use 2-cell blocks; our within delta CIs use 10-cell blocks for consistency with the transfer CIs.',
  provenance: {
    parquet_sha256_prefixes: { manavgat_2021: '054a1961', bejis_2022: '3dec785a', mugla_2021: 'c4ab107d', evia_2021_extended: 'bdce859c', montiferru_2021: 'ffb008f9' },
    reversal_feature_set_source: 'paper/conditional_similarity_transfer.json (bootstrap_supported_reversals)',
    reference_values: 'drive_new/cross_region/<pair>/step9b, drive_new/experiments/<region>/step8c',
  },
};

writeFileSync(`${ROOT}/paper/feature_drop_transfer.json`, JSON.stringify({ meta, ...j }, null, 1));

const lines = ['kind,name,config,auc,auc_ci_low,auc_ci_high,delta_vs_full,delta_ci_low,delta_ci_high,parity_check_diff'];
for (const r of j.transfers) for (const c of CONFIGS) {
  const d = c === 'full' ? ['', '', ''] : [r.delta_vs_full[c].toFixed(4), r.delta_ci[c][0].toFixed(4), r.delta_ci[c][1].toFixed(4)];
  lines.push(['transfer', r.direction, c, r.auc[c].toFixed(4), r.auc_ci[c][0].toFixed(4), r.auc_ci[c][1].toFixed(4), ...d, c === 'full' ? r.step9b_check_diff : ''].join(','));
}
for (const r of j.within) for (const c of CONFIGS) {
  const d = c === 'full' ? ['', '', ''] : [r.delta_vs_full[c].toFixed(4), r.delta_ci[c][0].toFixed(4), r.delta_ci[c][1].toFixed(4)];
  lines.push(['within', r.region, c, r.auc[c].toFixed(4), r.auc_ci[c][0].toFixed(4), r.auc_ci[c][1].toFixed(4), ...d, c === 'full' ? r.step8c_check_diff : ''].join(','));
}
writeFileSync(`${ROOT}/paper/feature_drop_transfer.csv`, lines.join('\n') + '\n');

// supported delta counts per config
for (const c of CONFIGS.slice(1)) {
  const pos = j.transfers.filter(r => r.delta_ci[c][0] > 0).map(r => r.direction);
  const neg = j.transfers.filter(r => r.delta_ci[c][1] < 0).map(r => r.direction);
  console.log(`${c}: supported gains ${pos.length} [${pos.join(', ')}]`);
  console.log(`${c}: supported losses ${neg.length} [${neg.join(', ')}]`);
}
console.log('max step9b parity diff:', Math.max(...j.transfers.map(r => r.step9b_check_diff)));
