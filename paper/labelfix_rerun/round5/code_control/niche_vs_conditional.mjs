// Analysis 5 - are niche overlap (P(x|y=1)) and sign agreement (P(y|x)) the same quantity?
// (1) pair-level correlation between Schoener's D and the conditional indices, pair bootstrap CI
// (2) SUPPORTIVE partial rank correlations at direction level (transfer ~ conditional | niche, and reverse)
// (3) figure data for the two contrast pairs (Manavgat-Mugla vs Bejis-Montiferru)
// (4) combined-table counts for the manuscript sentence
import { readFileSync, writeFileSync } from 'fs';

const ROOT = process.env.R3ROOT; if (!ROOT) throw new Error('R3ROOT unset'); // ROUND3: was 'C:/Users/CORSAIR/projects/thermal-twin'
const REGIONS = ['manavgat_2021', 'bejis_2022', 'mugla_2021', 'evia_2021_extended', 'montiferru_2021'];
const NBOOT = 2000;
const SEED = 42;

function mulberry32(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
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
function partialSpearman(x, y, z) {
  const rxy = spearman(x, y), rxz = spearman(x, z), rzy = spearman(z, y);
  const den = Math.sqrt((1 - rxz * rxz) * (1 - rzy * rzy));
  return den === 0 ? NaN : (rxy - rxz * rzy) / den;
}
const q = (arr, p) => { const s = [...arr].sort((a, b) => a - b); const i = p * (s.length - 1); const lo = Math.floor(i), hi = Math.ceil(i); return s[lo] + (s[hi] - s[lo]) * (i - lo); };

const cond = JSON.parse(readFileSync(`${ROOT}/paper/conditional_similarity_transfer.json`, 'utf8'));
const niche = JSON.parse(readFileSync(`${ROOT}/paper/niche_overlap_transfer.json`, 'utf8'));
const allCsv = readFileSync(`${ROOT}/paper/all_diagnostics_vs_transfer.csv`, 'utf8').trim().split('\n').slice(1);

// ---------- pair-level dataset (10 pairs, symmetric) ----------
const nicheByPair = new Map(niche.per_pair.map(p => [[p.region_a, p.region_b].sort().join('|'), p]));
const condByPair = new Map();
for (const d of cond.per_direction) {
  const [s, t] = d.direction.split('_to_');
  condByPair.set([s, t].sort().join('|'), d);
}
const transferByDir = new Map(niche.per_direction.map(d => [d.direction, d.thermal_roc]));
const pairs = [...nicheByPair.keys()].map(k => {
  const n = nicheByPair.get(k), c = condByPair.get(k);
  const [a, b] = k.split('|');
  const dirs = [`${a}_to_${b}`, `${b}_to_${a}`];
  return {
    pair: k, region_a: a, region_b: b,
    schoener_d_mean1d: n.schoener_d_mean1d,
    agree_count_9: c.agree_count_9, cosine_9: c.cosine_9,
    n_supported: c.n_supported,
    agree_fraction_supported: c.agree_fraction_supported,
    cosine_supported: c.cosine_supported,
    mean_transfer: (transferByDir.get(dirs[0]) + transferByDir.get(dirs[1])) / 2,
    transfer_dirs: Object.fromEntries(dirs.map(d => [d, transferByDir.get(d)])),
  };
});

// ---------- (1) measure-vs-measure correlation, pair bootstrap ----------
function pairLevelCorr(xKey, yKey, seedOffset) {
  const data = pairs.filter(p => Number.isFinite(p[xKey]) && Number.isFinite(p[yKey]));
  const x = data.map(p => p[xKey]), y = data.map(p => p[yKey]);
  const rho = spearman(x, y);
  const rnd = mulberry32(SEED + seedOffset);
  const reps = [];
  for (let b = 0; b < NBOOT; b++) {
    const bx = [], by = [];
    for (let k = 0; k < data.length; k++) {
      const p = data[Math.floor(rnd() * data.length)];
      bx.push(p[xKey]); by.push(p[yKey]);
    }
    const r = spearman(bx, by);
    if (Number.isFinite(r)) reps.push(r);
  }
  return { x: xKey, y: yKey, n_pairs: data.length, spearman_rho: rho, ci95: [q(reps, 0.025), q(reps, 0.975)], n_valid_replicates: reps.length };
}
const measureVsMeasure = [
  pairLevelCorr('schoener_d_mean1d', 'agree_fraction_supported', 300),
  pairLevelCorr('schoener_d_mean1d', 'cosine_supported', 301),
  pairLevelCorr('schoener_d_mean1d', 'cosine_9', 302),
  pairLevelCorr('schoener_d_mean1d', 'agree_count_9', 303),
];

// ---------- (2) supportive partial rank correlations (direction level) ----------
const directions = niche.per_direction.map(d => {
  const c = condByPair.get([d.source, d.target].sort().join('|'));
  return { ...d, cosine_9: c.cosine_9, agree_fraction_supported: c.agree_fraction_supported };
});
function partialWithBoot(condKey, seedOffset) {
  const data = directions.filter(d => Number.isFinite(d[condKey]));
  const y = data.map(d => d.thermal_roc), x = data.map(d => d[condKey]), z = data.map(d => d.schoener_d_mean1d);
  const pKeys = [...new Set(data.map(d => [d.source, d.target].sort().join('|')))];
  const byPair = new Map(pKeys.map(k => [k, data.filter(d => [d.source, d.target].sort().join('|') === k)]));
  const point_cond_given_niche = partialSpearman(x, y, z);
  const point_niche_given_cond = partialSpearman(z, y, x);
  const rnd = mulberry32(SEED + seedOffset);
  const r1 = [], r2 = [];
  for (let b = 0; b < NBOOT; b++) {
    const bx = [], by = [], bz = [];
    for (let k = 0; k < pKeys.length; k++) {
      const p = pKeys[Math.floor(rnd() * pKeys.length)];
      for (const d of byPair.get(p)) { bx.push(d[condKey]); by.push(d.thermal_roc); bz.push(d.schoener_d_mean1d); }
    }
    const a = partialSpearman(bx, by, bz), c = partialSpearman(bz, by, bx);
    if (Number.isFinite(a)) r1.push(a);
    if (Number.isFinite(c)) r2.push(c);
  }
  return {
    conditional_measure: condKey, n_directions: data.length, n_pairs: pKeys.length,
    partial_conditional_given_niche: { rho: point_cond_given_niche, ci95: [q(r1, 0.025), q(r1, 0.975)], n_valid: r1.length },
    partial_niche_given_conditional: { rho: point_niche_given_cond, ci95: [q(r2, 0.025), q(r2, 0.975)], n_valid: r2.length },
  };
}
const partials = [partialWithBoot('cosine_9', 310), partialWithBoot('agree_fraction_supported', 311)];

// ---------- (3) contrast-pair figure data ----------
const CONTRAST = [['manavgat_2021', 'mugla_2021'], ['bejis_2022', 'montiferru_2021']];
// transfer CIs from step9c for the four contrast directions
function stepc(folder, dir) {
  const b = JSON.parse(readFileSync(`${ROOT}/drive_new/cross_region/${folder}/step9c/cross_region_bootstrap_metrics.json`, 'utf8'));
  const g = b.groups.find(g => g.transfer_direction === dir && g.population === 'burnable_tree_shrub_grass');
  const t = g.confidence_intervals.thermal_roc_auc;
  return [t.ci_2_5, t.ci_97_5];
}
const contrastMeta = {
  'manavgat_2021|mugla_2021': { folder: 'manavgat_2021__mugla_2021' },
  'bejis_2022|montiferru_2021': { folder: 'montiferru_2021__bejis_2022' },
};
const figure = [];
for (const [a, b] of CONTRAST) {
  const k = [a, b].sort().join('|');
  const n = nicheByPair.get(k), c = condByPair.get(k);
  const folder = contrastMeta[k].folder;
  const dirs = [`${a}_to_${b}`, `${b}_to_${a}`];
  figure.push({
    pair: `${a} ~ ${b}`,
    niche_overlap: { schoener_d_mean1d: n.schoener_d_mean1d, warren_i_mean1d: n.warren_i_mean1d, schoener_d_pca2d: n.schoener_d_pca2d, mahalanobis: n.mahalanobis_burned },
    conditional: { agree_count_9: c.agree_count_9, cosine_9: c.cosine_9, n_supported: c.n_supported, agree_fraction_supported: c.agree_fraction_supported, supported_features: c.supported_features },
    transfer: Object.fromEntries(dirs.map(d => [d, { auc: transferByDir.get(d), ci95: stepc(folder, d) }])),
    per_feature_signed_auc: Object.fromEntries(Object.keys(cond.signed_auc_by_region[a]).map(f => [f, {
      [a]: cond.signed_auc_by_region[a][f],
      [b]: cond.signed_auc_by_region[b][f],
      sign_agrees: Math.sign(cond.signed_auc_by_region[a][f].auc - 0.5) === Math.sign(cond.signed_auc_by_region[b][f].auc - 0.5),
      schoener_d_this_feature: n.per_feature_schoener_d[f],
    }])),
  });
}
writeFileSync(`${ROOT}/paper/figure_contrast_pairs.json`, JSON.stringify({
  meta: {
    created: '2026-08-08',
    purpose: 'Main-figure data: high-overlap/reversed-direction pair (Manavgat-Mugla) vs low-overlap/aligned-direction pair (Bejis-Montiferru)',
    signed_auc_source: cond.meta.provenance.signed_auc_source,
    niche_source: 'paper/niche_overlap_transfer.json', transfer_ci_source: 'drive_new/cross_region/<pair>/step9c',
    parquet_sha256_prefixes: niche.meta.measure_computation.parquet_sha256_prefixes,
  }, pairs: figure,
}, null, 1));
const figCsv = ['pair,feature,region,signed_auc,ci_low,ci_high,sign_agrees,schoener_d_this_feature'];
for (const fp of figure) for (const [f, v] of Object.entries(fp.per_feature_signed_auc)) {
  for (const reg of Object.keys(v).filter(x => !['sign_agrees', 'schoener_d_this_feature'].includes(x))) {
    figCsv.push([`"${fp.pair}"`, f, reg, v[reg].auc.toFixed(4), v[reg].lo.toFixed(4), v[reg].hi.toFixed(4), v.sign_agrees, v.schoener_d_this_feature].join(','));
  }
}
writeFileSync(`${ROOT}/paper/figure_contrast_pairs.csv`, figCsv.join('\n') + '\n');

// ---------- (4) combined-table counts ----------
const rows = allCsv.map(l => l.split(',').pop());
const nRows = allCsv.length;
const nExcl = rows.filter(v => v === 'true').length;
const nNC = allCsv.filter(l => l.includes('NaN') || l.includes('not computable')).length;
const counts = { total_diagnostic_rows: nRows, ci_excludes_zero: nExcl, ci_spans_zero: nRows - nExcl - nNC, not_computable: nNC };

// ---------- write analysis JSON/CSV ----------
const meta = {
  created: '2026-08-08',
  analysis: 'Analysis 5 - is niche overlap (P(x|y=1)) the same quantity as sign agreement (P(y|x)), and which predicts transfer?',
  primary_evidence_note: 'Primary evidence = the two contrast pairs (logical: high overlap + failed transfer AND low overlap + working transfer together show overlap is neither sufficient nor necessary, independent of n). Partial correlations are SUPPORTIVE ONLY (n=10/8 effective pairs).',
  environment: niche.meta.measure_computation.environment,
  bootstrap: 'pair resampling with replacement, 2000 replicates, mulberry32 seed 42 (+offsets), percentile 95% CI',
  parquet_sha256_prefixes: niche.meta.measure_computation.parquet_sha256_prefixes,
};
writeFileSync(`${ROOT}/paper/niche_vs_conditional.json`, JSON.stringify({
  meta, pair_level_dataset: pairs, measure_vs_measure: measureVsMeasure,
  partial_correlations_supportive: partials, combined_table_counts: counts,
}, null, 1));
const csv2 = ['kind,x,y,n,spearman_rho,ci_low,ci_high'];
for (const m of measureVsMeasure) csv2.push(['measure_vs_measure', m.x, m.y, m.n_pairs, m.spearman_rho.toFixed(4), m.ci95[0].toFixed(4), m.ci95[1].toFixed(4)].join(','));
for (const p of partials) {
  csv2.push(['partial_supportive', p.conditional_measure + '|schoener_d', 'transfer_auc', p.n_directions, p.partial_conditional_given_niche.rho.toFixed(4), p.partial_conditional_given_niche.ci95[0].toFixed(4), p.partial_conditional_given_niche.ci95[1].toFixed(4)].join(','));
  csv2.push(['partial_supportive', 'schoener_d|' + p.conditional_measure, 'transfer_auc', p.n_directions, p.partial_niche_given_conditional.rho.toFixed(4), p.partial_niche_given_conditional.ci95[0].toFixed(4), p.partial_niche_given_conditional.ci95[1].toFixed(4)].join(','));
}
writeFileSync(`${ROOT}/paper/niche_vs_conditional.csv`, csv2.join('\n') + '\n');

console.log('measure vs measure (pair level):');
for (const m of measureVsMeasure) console.log(`  D vs ${m.y.padEnd(26)} n=${m.n_pairs} rho=${m.spearman_rho.toFixed(3)} [${m.ci95[0].toFixed(3)},${m.ci95[1].toFixed(3)}]`);
console.log('partials (supportive):');
for (const p of partials) {
  console.log(`  [${p.conditional_measure}] cond|niche rho=${p.partial_conditional_given_niche.rho.toFixed(3)} [${p.partial_conditional_given_niche.ci95[0].toFixed(3)},${p.partial_conditional_given_niche.ci95[1].toFixed(3)}]  niche|cond rho=${p.partial_niche_given_conditional.rho.toFixed(3)} [${p.partial_niche_given_conditional.ci95[0].toFixed(3)},${p.partial_niche_given_conditional.ci95[1].toFixed(3)}]`);
}
console.log('combined table counts:', JSON.stringify(counts));
console.log('\npair-level quadrant view (D vs agree, mean transfer):');
for (const p of [...pairs].sort((a, b) => b.schoener_d_mean1d - a.schoener_d_mean1d)) {
  console.log(`  ${p.pair.padEnd(42)} D=${p.schoener_d_mean1d.toFixed(3)} agree=${p.agree_count_9}/9 sup=${p.agree_count_9 !== null ? (p.agree_fraction_supported === null ? 'NA' : p.agree_fraction_supported) : ''} meanAUC=${p.mean_transfer.toFixed(3)}`);
}
