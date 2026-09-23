// Merge LORO results with pairwise/within comparisons and Analysis-1 conditional similarity.
import { readFileSync, writeFileSync } from 'fs';

const ROOT = process.env.R3ROOT; if (!ROOT) throw new Error('R3ROOT unset'); // ROUND3: was 'C:/Users/CORSAIR/projects/thermal-twin'
const S = process.argv[2]; // staging dir
const REGIONS = ['manavgat_2021', 'bejis_2022', 'mugla_2021', 'evia_2021_extended', 'montiferru_2021'];

const loro = JSON.parse(readFileSync(`${S}/loro_all.json`, 'utf8'));
const cmp = JSON.parse(readFileSync(`${S}/comparison_inputs.json`, 'utf8'));

function avgRanks(x) {
  const idx = x.map((v, i) => i).sort((a, b) => x[a] - x[b]);
  const ranks = new Array(x.length); let i = 0;
  while (i < idx.length) { let j = i; while (j < idx.length && x[idx[j]] === x[idx[i]]) j++; const r = (i + 1 + j) / 2; for (let k = i; k < j; k++) ranks[idx[k]] = r; i = j; }
  return ranks;
}
function pearson(a, b) {
  const n = a.length, ma = a.reduce((s, v) => s + v, 0) / n, mb = b.reduce((s, v) => s + v, 0) / n;
  let sab = 0, sa = 0, sb = 0;
  for (let i = 0; i < n; i++) { const da = a[i] - ma, db = b[i] - mb; sab += da * db; sa += da * da; sb += db * db; }
  return (sa === 0 || sb === 0) ? NaN : sab / Math.sqrt(sa * sb);
}
const spearman = (x, y) => pearson(avgRanks(x), avgRanks(y));

const perTarget = [];
for (const t of REGIONS) {
  const pool = REGIONS.filter(r => r !== t);
  const pw = pool.map(s => ({ source: s, thermal: cmp.transfer[`${s}_to_${t}`].thermal, baseline: cmp.transfer[`${s}_to_${t}`].baseline }));
  const th = pw.map(p => p.thermal);
  const get = (scaling, fs) => loro.find(r => r.target === t && r.scaling === scaling && r.feature_set === fs);
  const cond = pool.map(s => cmp.conditional_by_pair[[s, t].sort().join('|')]);
  const mean = a => a.reduce((x, y) => x + y, 0) / a.length;
  perTarget.push({
    target: t,
    pool,
    pairwise_thermal: Object.fromEntries(pw.map(p => [p.source, p.thermal])),
    best_pairwise_thermal: Math.max(...th),
    best_pairwise_source: pw.find(p => p.thermal === Math.max(...th)).source,
    mean_pairwise_thermal: mean(th),
    loro_raw_thermal: get('raw', 'thermal'),
    loro_z_thermal: get('regionwise_z', 'thermal'),
    loro_raw_baseline: get('raw', 'baseline'),
    loro_z_baseline: get('regionwise_z', 'baseline'),
    within_thermal: cmp.within[t].thermal_auc,
    within_baseline: cmp.within[t].baseline_auc,
    pool_conditional: {
      mean_cosine_9: mean(cond.map(c => c.cosine_9)),
      max_cosine_9: Math.max(...cond.map(c => c.cosine_9)),
      mean_agree_count_9: mean(cond.map(c => c.agree_count_9)),
      max_agree_count_9: Math.max(...cond.map(c => c.agree_count_9)),
    },
  });
}

// n=5 rank correlations (descriptive only) between pool conditional similarity and LORO AUC
const xs = {
  mean_cosine_9: perTarget.map(p => p.pool_conditional.mean_cosine_9),
  max_cosine_9: perTarget.map(p => p.pool_conditional.max_cosine_9),
  mean_agree_count_9: perTarget.map(p => p.pool_conditional.mean_agree_count_9),
  max_agree_count_9: perTarget.map(p => p.pool_conditional.max_agree_count_9),
};
const ys = {
  loro_raw_thermal: perTarget.map(p => p.loro_raw_thermal.roc_auc),
  loro_z_thermal: perTarget.map(p => p.loro_z_thermal.roc_auc),
};
const linkage = [];
for (const [xk, xv] of Object.entries(xs)) for (const [yk, yv] of Object.entries(ys)) {
  linkage.push({ x: xk, y: yk, spearman_rho_n5: +spearman(xv, yv).toFixed(3) });
}

const meta = {
  created: '2026-08-08',
  analysis: 'Analysis 2 - leave-one-region-out pooled multi-region training vs pairwise transfer, within-region ceiling, and Analysis-1 conditional similarity',
  environment: 'WSL Ubuntu-22.04, micromamba env: python 3.12, scikit-learn 1.9.0 (exact match to Emrehan step10 records), pandas 3.0.5, numpy 2.5.1, pyarrow 25.0.0',
  implementation_check: 'two pairwise step9b transfers reproduced to 4 decimal places with this environment (montiferru->bejis 0.5483, manavgat->bejis 0.3258, diff 0.0000). With sklearn 1.7.2 the same code deviated by 0.021-0.026 -> exact version matching is required and was used.',
  model: 'RandomForestClassifier(n_estimators=300, min_samples_leaf=3, class_weight=balanced, random_state=42)',
  preprocessing: 'numeric median imputation fit on pooled training set; landcover one-hot fit on training (unknown target categories -> all-zero); regionwise z-score = per-region mean/sd (ddof=0) over primary rows, numeric features only, target scaled with its own stats (label-free, Step10 definition)',
  population: 'valid_for_modeling AND burnable_tree_shrub_grass',
  bootstrap: 'target spatial-block bootstrap, blocks (row_500m//10, col_500m//10) ~5 km, 1000 replicates, numpy default_rng(42), percentile 95% CI',
  provenance: {
    parquet_sha256_prefixes: { manavgat_2021: '054a1961', bejis_2022: '3dec785a', mugla_2021: 'c4ab107d', evia_2021_extended: 'bdce859c', montiferru_2021: 'ffb008f9' },
    pairwise_and_within_sources: 'drive_new/cross_region/<pair>/step9b (thermal raw, TSG), drive_new/experiments/<region>/step8c point estimates (TSG)',
    conditional_similarity_source: 'paper/conditional_similarity_transfer.json (Analysis 1)',
  },
  linkage_note: 'n=5 targets -> rank correlations are descriptive only; no bootstrap CI is meaningful at n=5',
};

writeFileSync(`${ROOT}/paper/loro_pooled_transfer.json`, JSON.stringify({ meta, per_target: perTarget, all_loro_runs: loro, conditional_linkage: linkage }, null, 2));

const csv = ['target,scaling,feature_set,n_train,n_test,roc_auc,roc_ci_low,roc_ci_high,pr_auc,no_skill,brier,best_pairwise_thermal,mean_pairwise_thermal,within_thermal'];
for (const r of loro) {
  const p = perTarget.find(p => p.target === r.target);
  csv.push([r.target, r.scaling, r.feature_set, r.n_train, r.n_test, r.roc_auc.toFixed(4),
    r.roc_auc_ci[0].toFixed(4), r.roc_auc_ci[1].toFixed(4), r.pr_auc.toFixed(4), r.prevalence.toFixed(4),
    r.brier.toFixed(4), p.best_pairwise_thermal.toFixed(4), p.mean_pairwise_thermal.toFixed(4), p.within_thermal.toFixed(4)].join(','));
}
writeFileSync(`${ROOT}/paper/loro_pooled_transfer.csv`, csv.join('\n') + '\n');

console.log('target             bestPW  meanPW  LOROraw [CI]            LOROz   within  | meanCos maxCos');
for (const p of perTarget) {
  const lr = p.loro_raw_thermal, lz = p.loro_z_thermal;
  console.log(`${p.target.padEnd(18)} ${p.best_pairwise_thermal.toFixed(4)}  ${p.mean_pairwise_thermal.toFixed(4)}  ${lr.roc_auc.toFixed(4)} [${lr.roc_auc_ci[0].toFixed(3)},${lr.roc_auc_ci[1].toFixed(3)}] ${lz.roc_auc.toFixed(4)}  ${p.within_thermal.toFixed(4)} | ${p.pool_conditional.mean_cosine_9.toFixed(3).padStart(6)} ${p.pool_conditional.max_cosine_9.toFixed(3).padStart(6)}`);
}
console.log('\nlinkage (n=5, descriptive):');
for (const l of linkage) console.log(`  ${l.x} vs ${l.y}: rho=${l.spearman_rho_n5}`);
