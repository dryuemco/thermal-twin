// Regime distance vs raw thermal transfer AUC — formal rank-correlation test,
// alongside Emrehan's marginal distance diagnostics and the domain-classifier AUC.
// Primary population = burnable_tree_shrub_grass (TSG). seed=42, pair-based bootstrap.
import { readFileSync, writeFileSync, existsSync, unlinkSync } from 'fs';

const ROOT = 'C:/Users/CORSAIR/projects/thermal-twin';
const REGIONS = ['manavgat_2021', 'bejis_2022', 'mugla_2021', 'evia_2021_extended', 'montiferru_2021'];
const FOUR_AOI = ['manavgat_2021', 'bejis_2022', 'mugla_2021', 'evia_2021_extended']; // Emrehan's marginal set
const POP = 'burnable_tree_shrub_grass';
const NBOOT = 2000;
const SEED = 42;

function mulberry32(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }

// ---------- small CSV parser (handles quoted fields with commas) ----------
function parseCSV(text) {
  const rows = []; let row = []; let cur = ''; let inQ = false;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (inQ) {
      if (ch === '"') { if (text[i + 1] === '"') { cur += '"'; i++; } else inQ = false; }
      else cur += ch;
    } else if (ch === '"') inQ = true;
    else if (ch === ',') { row.push(cur); cur = ''; }
    else if (ch === '\n') { row.push(cur.replace(/\r$/, '')); rows.push(row); row = []; cur = ''; }
    else cur += ch;
  }
  if (cur !== '' || row.length) { row.push(cur.replace(/\r$/, '')); rows.push(row); }
  const header = rows[0];
  return rows.slice(1).filter(r => r.length > 1 || (r.length === 1 && r[0] !== ''))
    .map(r => Object.fromEntries(header.map((h, i) => [h, r[i]])));
}

// ---------- rank statistics ----------
function avgRanks(x) {
  const idx = x.map((v, i) => i).sort((a, b) => x[a] - x[b]);
  const ranks = new Array(x.length);
  let i = 0;
  while (i < idx.length) {
    let j = i;
    while (j < idx.length && x[idx[j]] === x[idx[i]]) j++;
    const r = (i + 1 + j) / 2;
    for (let k = i; k < j; k++) ranks[idx[k]] = r;
    i = j;
  }
  return ranks;
}
function pearson(a, b) {
  const n = a.length;
  const ma = a.reduce((s, v) => s + v, 0) / n, mb = b.reduce((s, v) => s + v, 0) / n;
  let sab = 0, sa = 0, sb = 0;
  for (let i = 0; i < n; i++) { const da = a[i] - ma, db = b[i] - mb; sab += da * db; sa += da * da; sb += db * db; }
  if (sa === 0 || sb === 0) return NaN;
  return sab / Math.sqrt(sa * sb);
}
function spearman(x, y) { return pearson(avgRanks(x), avgRanks(y)); }
function kendallTauB(x, y) {
  const n = x.length;
  let C = 0, D = 0, Tx = 0, Ty = 0;
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) {
    const dx = Math.sign(x[i] - x[j]), dy = Math.sign(y[i] - y[j]);
    if (dx === 0 && dy === 0) continue;
    else if (dx === 0) Tx++;
    else if (dy === 0) Ty++;
    else if (dx === dy) C++;
    else D++;
  }
  const denom = Math.sqrt((C + D + Tx) * (C + D + Ty));
  if (denom === 0) return NaN;
  return (C - D) / denom;
}

// ---------- load transfer AUCs (canonical 20 directions, TSG, raw thermal) ----------
const pairFolders = ['manavgat_2021__bejis_2022', 'manavgat_2021__mugla_2021', 'manavgat_2021__evia_2021_extended',
  'montiferru_2021__manavgat_2021', 'montiferru_2021__bejis_2022', 'montiferru_2021__mugla_2021',
  'montiferru_2021__evia_2021_extended', 'bejis_2022__mugla_2021', 'bejis_2022__evia_2021_extended',
  'mugla_2021__evia_2021_extended'];
const transfer = new Map(); // direction -> {thermal_roc, thermal_ci, folder}
for (const folder of pairFolders) {
  const m = JSON.parse(readFileSync(`${ROOT}/drive_new/cross_region/${folder}/step9b/cross_region_transfer_metrics.json`, 'utf8'));
  const boot = JSON.parse(readFileSync(`${ROOT}/drive_new/cross_region/${folder}/step9c/cross_region_bootstrap_metrics.json`, 'utf8'));
  for (const r of m.results) {
    if (r.population !== POP || r.skipped) continue;
    const g = boot.groups.find(g => g.transfer_direction === r.transfer_direction && g.population === POP);
    const t = g && g.confidence_intervals.thermal_roc_auc;
    transfer.set(r.transfer_direction, {
      thermal_roc: r.thermal_metrics.roc_auc,
      thermal_ci: t ? [t.ci_2_5, t.ci_97_5] : null,
      folder,
    });
  }
}
const directions = [];
for (const s of REGIONS) for (const t of REGIONS) {
  if (s === t) continue;
  const key = `${s}_to_${t}`;
  if (!transfer.has(key)) throw new Error(`missing direction ${key}`);
  directions.push({ source: s, target: t, direction: key, ...transfer.get(key) });
}

// ---------- regime metrics (verified against Emrehan's Rejim tablosu) ----------
const comp = JSON.parse(readFileSync(`${ROOT}/paper/_tmp_burned_components.json`, 'utf8'));
for (const d of directions) {
  const s = comp[d.source], t = comp[d.target];
  d.regime_dist_log_effn = Math.abs(Math.log(s.effective_component_count) - Math.log(t.effective_component_count));
  d.regime_dist_largest_share = Math.abs(s.largest_share - t.largest_share);
}

// ---------- domain classifier AUC (symmetric per unordered pair) ----------
const dc = parseCSV(readFileSync(`${ROOT}/drive_new/diagnostics/domain_classifier_audit/comparison/multi_aoi_domain_classifier_comparison.csv`, 'utf8'));
const dcMap = new Map();
for (const r of dc) dcMap.set([r.experiment_a, r.experiment_b].sort().join('|'), parseFloat(r.spatial_block_domain_auc));
for (const d of directions) {
  d.domain_classifier_auc = dcMap.get([d.source, d.target].sort().join('|'));
  if (d.domain_classifier_auc == null) throw new Error(`missing domain clf for ${d.direction}`);
}

// ---------- Emrehan's marginal measures (12 directed, 4 AOI) ----------
const aoa = parseCSV(readFileSync(`${ROOT}/drive_new/diagnostics/marginal_aoa_completion/4b2a1c86c0c197c2a331c133d1120f9531ce385441d86af0d8c6154024417492/comparison/marginal_diagnostics_with_transfer.csv`, 'utf8'));
let maxAucDiff = 0;
for (const r of aoa) {
  const d = directions.find(d => d.direction === r.direction);
  if (!d) continue;
  d.target_mean_dissimilarity = parseFloat(r.target_mean_dissimilarity);
  d.target_p95_dissimilarity = parseFloat(r.target_p95_dissimilarity);
  d.fraction_inside_weighted_aoa = parseFloat(r.fraction_inside_weighted_aoa);
  d.climate_distance = parseFloat(r.climate_distance);
  d.geographic_distance_km = parseFloat(r.centroid_geodesic_distance_km);
  d.unweighted_fraction_inside_support = parseFloat(r.unweighted_fraction_target_cells_inside_support);
  maxAucDiff = Math.max(maxAucDiff, Math.abs(parseFloat(r.raw_thermal_roc_auc) - d.thermal_roc));
}

// ---------- correlation with pair-based bootstrap ----------
function pairKey(d) { return [d.source, d.target].sort().join('|'); }
function corrWithBoot(rows, xKey, seedOffset) {
  const data = rows.filter(d => Number.isFinite(d[xKey]));
  const x = data.map(d => d[xKey]), y = data.map(d => d.thermal_roc);
  const rho = spearman(x, y), tau = kendallTauB(x, y);
  const pairs = [...new Set(data.map(pairKey))];
  const byPair = new Map(pairs.map(p => [p, data.filter(d => pairKey(d) === p)]));
  const rnd = mulberry32(SEED + seedOffset);
  const rhos = [], taus = [];
  let degenerate = 0;
  for (let b = 0; b < NBOOT; b++) {
    const bx = [], by = [];
    for (let k = 0; k < pairs.length; k++) {
      const p = pairs[Math.floor(rnd() * pairs.length)];
      for (const d of byPair.get(p)) { bx.push(d[xKey]); by.push(d.thermal_roc); }
    }
    const r = spearman(bx, by), t = kendallTauB(bx, by);
    if (Number.isFinite(r) && Number.isFinite(t)) { rhos.push(r); taus.push(t); }
    else degenerate++;
  }
  const q = (arr, p) => { const s = [...arr].sort((a, b) => a - b); const i = p * (s.length - 1); const lo = Math.floor(i), hi = Math.ceil(i); return s[lo] + (s[hi] - s[lo]) * (i - lo); };
  return {
    n_directions: data.length, n_pairs: pairs.length,
    spearman_rho: rho, spearman_ci95: [q(rhos, 0.025), q(rhos, 0.975)],
    kendall_tau_b: tau, kendall_ci95: [q(taus, 0.025), q(taus, 0.975)],
    n_valid_replicates: rhos.length, n_degenerate_replicates: degenerate,
  };
}

const MEASURES = [
  { key: 'regime_dist_log_effn', label: 'Regime distance |Δ log effective component count| (primary)', expected: 'negative', directed: false, coverage: 'five_aoi' },
  { key: 'regime_dist_largest_share', label: 'Regime distance |Δ largest-component share| (secondary)', expected: 'negative', directed: false, coverage: 'five_aoi' },
  { key: 'domain_classifier_auc', label: 'Domain-classifier AUC (marginal separability)', expected: 'negative', directed: false, coverage: 'five_aoi' },
  { key: 'target_mean_dissimilarity', label: 'Predictor-space mean dissimilarity (Emrehan, weighted AoA)', expected: 'negative', directed: true, coverage: 'four_aoi' },
  { key: 'target_p95_dissimilarity', label: 'Predictor-space p95 dissimilarity (Emrehan)', expected: 'negative', directed: true, coverage: 'four_aoi' },
  { key: 'fraction_inside_weighted_aoa', label: 'Fraction of target inside weighted AoA (Emrehan)', expected: 'positive', directed: true, coverage: 'four_aoi' },
  { key: 'climate_distance', label: 'Climatic distance (Emrehan, TerraClimate)', expected: 'negative', directed: false, coverage: 'four_aoi' },
  { key: 'geographic_distance_km', label: 'Geographic centroid distance km (Emrehan)', expected: 'negative', directed: false, coverage: 'four_aoi' },
  { key: 'unweighted_fraction_inside_support', label: 'Fraction of target inside unweighted support (Emrehan)', expected: 'positive', directed: true, coverage: 'four_aoi' },
];

const fourAoiRows = directions.filter(d => FOUR_AOI.includes(d.source) && FOUR_AOI.includes(d.target));
const results = [];
let seedOffset = 0;
for (const m of MEASURES) {
  const full = corrWithBoot(directions, m.key, seedOffset++);
  const sub = corrWithBoot(fourAoiRows, m.key, seedOffset++);
  results.push({ ...m, full_set: full, four_aoi_subset: sub });
}

// ---------- write outputs ----------
const meta = {
  created: '2026-08-08',
  description: 'Rank correlation between candidate transferability diagnostics and raw thermal cross-region transfer ROC-AUC, with pair-based spatial bootstrap CIs.',
  population: POP,
  transfer_metric: 'raw thermal ROC-AUC on target region, source-only RF (step9b), TSG population',
  n_canonical_directions: directions.length,
  bootstrap: { scheme: 'resample unordered region pairs with replacement; each sampled pair contributes all its ordered directions', n_replicates: NBOOT, seed: SEED, prng: 'mulberry32 (not numpy-identical; procedure deterministic)', ci: 'equal-tailed percentile 95%' },
  regime_metric_definition: '8-connectivity connected components of burned TSG cells on row_500m/col_500m; effective component count = inverse Simpson of component size shares; distances are absolute differences (log effN; largest share), symmetric per pair',
  component_verification: 'all five regions match Emrehan Rejim tablosu exactly (count/largest/share/second/effN to 1e-4)',
  transfer_auc_crosscheck_vs_emrehan_aoa_table: { n_directions_compared: 12, max_abs_difference: maxAucDiff },
  provenance: {
    parquet_sha256_prefixes: { manavgat_2021: '054a1961', bejis_2022: '3dec785a', mugla_2021: 'c4ab107d', evia_2021_extended: 'bdce859c', montiferru_2021: 'ffb008f9' },
    transfer_source: 'drive_new/cross_region/<pair>/step9b + step9c (bidirectional, git a07ea337/0a3c5fe8/ab8fc5f5/5d55f6f4)',
    domain_classifier_source: 'drive_new/diagnostics/domain_classifier_audit/comparison/multi_aoi_domain_classifier_comparison.csv',
    marginal_measures_source: 'drive_new/diagnostics/marginal_aoa_completion/4b2a1c86.../comparison/marginal_diagnostics_with_transfer.csv (4 AOI, no Montiferru)',
  },
  honesty_notes: [
    'Effective sample is 10 unordered pairs (6 for four-AOI measures), not 20 (12) independent observations: the two directions of a pair share geography, and every pair shares its two member regions with three others. Power is very low; absence of significance is expected under both H0 and modest true effects.',
    'Emrehan four-AOI measures exclude Montiferru; five-AOI measures are also reported on the common four-AOI subset for direct comparison.',
    'Pre-registered expectation (stated before computation): regime distance will NOT significantly predict transfer, matching the failure of all four marginal measures; Bejís and Evia-extended are near-identical in regime (effN 1.000 vs 1.008) yet their transfers fail in both directions.',
  ],
  per_region_regime_metrics: Object.fromEntries(REGIONS.map(r => [r, {
    burned_cells: comp[r].burned_cells, component_count: comp[r].component_count,
    largest_component: comp[r].largest_component, largest_share: comp[r].largest_share,
    second_largest: comp[r].second_largest, effective_component_count: comp[r].effective_component_count,
  }])),
};

const perDirection = directions.map(d => ({
  direction: d.direction, source: d.source, target: d.target,
  raw_thermal_roc_auc: d.thermal_roc, thermal_roc_ci95: d.thermal_ci,
  regime_dist_log_effn: d.regime_dist_log_effn, regime_dist_largest_share: d.regime_dist_largest_share,
  domain_classifier_auc: d.domain_classifier_auc,
  target_mean_dissimilarity: d.target_mean_dissimilarity ?? null,
  target_p95_dissimilarity: d.target_p95_dissimilarity ?? null,
  fraction_inside_weighted_aoa: d.fraction_inside_weighted_aoa ?? null,
  climate_distance: d.climate_distance ?? null,
  geographic_distance_km: d.geographic_distance_km ?? null,
  unweighted_fraction_inside_support: d.unweighted_fraction_inside_support ?? null,
}));

writeFileSync(`${ROOT}/paper/regime_transfer_correlation.json`, JSON.stringify({ meta, per_direction: perDirection, correlations: results }, null, 2));

// CSV: correlation table
const csvLines = ['measure,label,expected_sign,directed,coverage,set,n_directions,n_pairs,spearman_rho,spearman_ci_low,spearman_ci_high,kendall_tau_b,kendall_ci_low,kendall_ci_high,n_valid_replicates'];
for (const r of results) for (const [set, c] of [['full', r.full_set], ['four_aoi_subset', r.four_aoi_subset]]) {
  csvLines.push([r.key, `"${r.label}"`, r.expected, r.directed, r.coverage, set, c.n_directions, c.n_pairs,
    c.spearman_rho.toFixed(4), c.spearman_ci95[0].toFixed(4), c.spearman_ci95[1].toFixed(4),
    c.kendall_tau_b.toFixed(4), c.kendall_ci95[0].toFixed(4), c.kendall_ci95[1].toFixed(4), c.n_valid_replicates].join(','));
}
writeFileSync(`${ROOT}/paper/regime_transfer_correlation.csv`, csvLines.join('\n') + '\n');

// console summary
console.log(`transfer AUC cross-check vs Emrehan AoA table: max |diff| = ${maxAucDiff.toExponential(2)} over 12 directions`);
console.log('\nmeasure                                  set        n   rho     [95% CI]            tau     [95% CI]');
for (const r of results) {
  for (const [set, c] of [['full', r.full_set], ['4-AOI', r.four_aoi_subset]]) {
    console.log(`${r.key.padEnd(40)} ${set.padEnd(9)} ${String(c.n_directions).padStart(3)} ${c.spearman_rho.toFixed(3).padStart(6)}  [${c.spearman_ci95[0].toFixed(3)},${c.spearman_ci95[1].toFixed(3)}]  ${c.kendall_tau_b.toFixed(3).padStart(6)}  [${c.kendall_ci95[0].toFixed(3)},${c.kendall_ci95[1].toFixed(3)}]`);
  }
}
unlinkSync(`${ROOT}/paper/_tmp_burned_components.json`);
