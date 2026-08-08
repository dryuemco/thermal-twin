// Analysis 4: correlate SDM niche-overlap measures with transfer AUC (identical
// pair-bootstrap framework as regime/conditional analyses) and build the combined
// all-diagnostics table.
import { readFileSync, writeFileSync } from 'fs';

const ROOT = 'C:/Users/CORSAIR/projects/thermal-twin';
const S = process.argv[2];
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
function kendallTauB(x, y) {
  const n = x.length; let C = 0, D = 0, Tx = 0, Ty = 0;
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
    const dx = Math.sign(x[i] - x[j]), dy = Math.sign(y[i] - y[j]);
    if (dx === 0 && dy === 0) continue; else if (dx === 0) Tx++; else if (dy === 0) Ty++;
    else if (dx === dy) C++; else D++;
  }
  const den = Math.sqrt((C + D + Tx) * (C + D + Ty));
  return den === 0 ? NaN : (C - D) / den;
}

const niche = JSON.parse(readFileSync(`${S}/staging/niche_measures.json`, 'utf8'));
const cmp = JSON.parse(readFileSync(`${S}/staging/comparison_inputs.json`, 'utf8'));
const byPairKey = new Map(niche.pairs.map(p => [[p.region_a, p.region_b].sort().join('|'), p]));

const MEASURE_KEYS = ['schoener_d_mean1d', 'warren_i_mean1d', 'schoener_d_pca2d', 'warren_i_pca2d', 'mahalanobis_burned'];
const directions = [];
for (const s of REGIONS) for (const t of REGIONS) {
  if (s === t) continue;
  const d = { source: s, target: t, direction: `${s}_to_${t}`, thermal_roc: cmp.transfer[`${s}_to_${t}`].thermal };
  const pm = byPairKey.get([s, t].sort().join('|'));
  for (const k of MEASURE_KEYS) d[k] = pm[k];
  directions.push(d);
}

function pairKey(d) { return [d.source, d.target].sort().join('|'); }
function corrWithBoot(rows, xKey, seedOffset) {
  const data = rows.filter(d => Number.isFinite(d[xKey]));
  const x = data.map(d => d[xKey]), y = data.map(d => d.thermal_roc);
  const rho = spearman(x, y), tau = kendallTauB(x, y);
  const pairs = [...new Set(data.map(pairKey))];
  const byPair = new Map(pairs.map(p => [p, data.filter(d => pairKey(d) === p)]));
  const rnd = mulberry32(SEED + seedOffset);
  const rhos = [], taus = []; let degenerate = 0;
  for (let b = 0; b < NBOOT; b++) {
    const bx = [], by = [];
    for (let k = 0; k < pairs.length; k++) {
      const p = pairs[Math.floor(rnd() * pairs.length)];
      for (const d of byPair.get(p)) { bx.push(d[xKey]); by.push(d.thermal_roc); }
    }
    const r = spearman(bx, by), t = kendallTauB(bx, by);
    if (Number.isFinite(r) && Number.isFinite(t)) { rhos.push(r); taus.push(t); } else degenerate++;
  }
  const q = (arr, p) => { const s2 = [...arr].sort((a, b) => a - b); const i = p * (s2.length - 1); const lo = Math.floor(i), hi = Math.ceil(i); return s2[lo] + (s2[hi] - s2[lo]) * (i - lo); };
  return { n_directions: data.length, n_pairs: pairs.length,
    spearman_rho: rho, spearman_ci95: [q(rhos, 0.025), q(rhos, 0.975)],
    kendall_tau_b: tau, kendall_ci95: [q(taus, 0.025), q(taus, 0.975)],
    n_valid_replicates: rhos.length, n_degenerate_replicates: degenerate };
}

const MEASURES = [
  { key: 'schoener_d_mean1d', label: "Schoener's D, mean of 9 1D overlaps", expected: 'positive' },
  { key: 'warren_i_mean1d', label: "Warren's I, mean of 9 1D overlaps", expected: 'positive' },
  { key: 'schoener_d_pca2d', label: "Schoener's D, PCA 2D histogram", expected: 'positive' },
  { key: 'warren_i_pca2d', label: "Warren's I, PCA 2D histogram", expected: 'positive' },
  { key: 'mahalanobis_burned', label: 'Mahalanobis distance, burned centroids', expected: 'negative' },
];
const results = [];
let so = 200;
for (const m of MEASURES) results.push({ ...m, full_set: corrWithBoot(directions, m.key, so++) });

const meta = {
  created: '2026-08-08',
  analysis: 'Analysis 4 - canonical SDM niche-overlap measures (P(x|y=1)) vs raw thermal transfer ROC-AUC',
  candidate_set_fixed_in_advance: true,
  measure_computation: niche.meta,
  transfer_metric: 'raw thermal ROC-AUC on target, source-only RF (step9b), TSG, 20 ordered directions',
  bootstrap: { scheme: 'unordered pairs resampled with replacement, both directions carried', n_replicates: NBOOT, seed: SEED, prng: 'mulberry32', ci: 'equal-tailed percentile 95%', note: 'identical framework/seed policy as regime_transfer_correlation and conditional_similarity_transfer' },
};
writeFileSync(`${ROOT}/paper/niche_overlap_transfer.json`, JSON.stringify({ meta, per_pair: niche.pairs, per_direction: directions, correlations: results }, null, 1));

const csv = ['measure,label,expected_sign,n_directions,n_pairs,spearman_rho,spearman_ci_low,spearman_ci_high,kendall_tau_b,kendall_ci_low,kendall_ci_high,n_valid_replicates'];
for (const r of results) {
  const c = r.full_set;
  csv.push([r.key, `"${r.label}"`, r.expected, c.n_directions, c.n_pairs,
    c.spearman_rho.toFixed(4), c.spearman_ci95[0].toFixed(4), c.spearman_ci95[1].toFixed(4),
    c.kendall_tau_b.toFixed(4), c.kendall_ci95[0].toFixed(4), c.kendall_ci95[1].toFixed(4), c.n_valid_replicates].join(','));
}
writeFileSync(`${ROOT}/paper/niche_overlap_transfer.csv`, csv.join('\n') + '\n');

// ---------- combined all-diagnostics table ----------
function readCsv(path) {
  const [h, ...rows] = readFileSync(path, 'utf8').trim().split('\n');
  const cols = h.split(',');
  return rows.map(r => {
    const vals = r.match(/("[^"]*"|[^,]*)/g).filter((_, i, a) => true);
    // simple split honoring quotes
    const out = []; let cur = '', inQ = false;
    for (const ch of r) {
      if (inQ) { if (ch === '"') inQ = false; else cur += ch; }
      else if (ch === '"') inQ = true;
      else if (ch === ',') { out.push(cur); cur = ''; }
      else cur += ch;
    }
    out.push(cur);
    return Object.fromEntries(cols.map((c, i) => [c, out[i]]));
  });
}
const SIDE = {
  target_mean_dissimilarity: 'P(x) marginal', target_p95_dissimilarity: 'P(x) marginal',
  fraction_inside_weighted_aoa: 'P(x) marginal', climate_distance: 'P(x) marginal',
  geographic_distance_km: 'geographic', unweighted_fraction_inside_support: 'P(x) marginal',
  domain_classifier_auc: 'P(x) marginal', regime_dist_log_effn: 'P(y) spatial structure',
  regime_dist_largest_share: 'P(y) spatial structure',
  agree_count_9: 'P(y|x) conditional', vector_spearman_9: 'P(y|x) conditional', cosine_9: 'P(y|x) conditional',
  agree_fraction_supported: 'P(y|x) conditional', vector_spearman_supported: 'P(y|x) conditional',
  cosine_supported: 'P(y|x) conditional',
  schoener_d_mean1d: 'P(x|y=1) niche overlap', warren_i_mean1d: 'P(x|y=1) niche overlap',
  schoener_d_pca2d: 'P(x|y=1) niche overlap', warren_i_pca2d: 'P(x|y=1) niche overlap',
  mahalanobis_burned: 'P(x|y=1) niche overlap',
};
const regime = readCsv(`${ROOT}/paper/regime_transfer_correlation.csv`).filter(r => r.set === 'full');
const conditional = readCsv(`${ROOT}/paper/conditional_similarity_transfer.csv`);
const nicheRows = readCsv(`${ROOT}/paper/niche_overlap_transfer.csv`);
const all = [];
for (const r of regime) all.push({ measure: r.measure, label: r.label, side: SIDE[r.measure] || '?', expected: r.expected_sign, n: r.n_directions, rho: r.spearman_rho, rlo: r.spearman_ci_low, rhi: r.spearman_ci_high, tau: r.kendall_tau_b, tlo: r.kendall_ci_low, thi: r.kendall_ci_high });
for (const r of conditional) all.push({ measure: r.measure, label: r.label, side: SIDE[r.measure] || '?', expected: r.expected_sign, n: r.n_directions, rho: r.spearman_rho, rlo: r.spearman_ci_low, rhi: r.spearman_ci_high, tau: r.kendall_tau_b, tlo: r.kendall_ci_low, thi: r.kendall_ci_high });
for (const r of nicheRows) all.push({ measure: r.measure, label: r.label, side: SIDE[r.measure] || '?', expected: r.expected_sign, n: r.n_directions, rho: r.spearman_rho, rlo: r.spearman_ci_low, rhi: r.spearman_ci_high, tau: r.kendall_tau_b, tlo: r.kendall_ci_low, thi: r.kendall_ci_high });
const excl = r => (parseFloat(r.rlo) > 0 && parseFloat(r.rhi) > 0) || (parseFloat(r.rlo) < 0 && parseFloat(r.rhi) < 0);
const outCsv = ['measure,label,side,expected_sign,n_directions,spearman_rho,spearman_ci_low,spearman_ci_high,kendall_tau_b,kendall_ci_low,kendall_ci_high,ci_excludes_zero'];
for (const r of all) outCsv.push([r.measure, `"${r.label}"`, `"${r.side}"`, r.expected, r.n, r.rho, r.rlo, r.rhi, r.tau, r.tlo, r.thi, excl(r)].join(','));
writeFileSync(`${ROOT}/paper/all_diagnostics_vs_transfer.csv`, outCsv.join('\n') + '\n');

console.log('niche correlations:');
for (const r of results) {
  const c = r.full_set;
  console.log(`${r.key.padEnd(24)} n=${c.n_directions} rho=${c.spearman_rho.toFixed(3)} [${c.spearman_ci95[0].toFixed(3)},${c.spearman_ci95[1].toFixed(3)}] tau=${c.kendall_tau_b.toFixed(3)} [${c.kendall_ci95[0].toFixed(3)},${c.kendall_ci95[1].toFixed(3)}]`);
}
console.log(`\ncombined table rows: ${all.length}; CI-excluding-zero rows:`);
for (const r of all.filter(excl)) console.log(`  ${r.measure} (${r.side}) rho=${r.rho} [${r.rlo},${r.rhi}]`);
