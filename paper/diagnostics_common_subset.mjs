// Common-subset rerun of the twenty transferability diagnostics (Table 6).
// The published table mixes n = 12, n = 16 and n = 20 rows, so "marginal fails,
// conditional succeeds" is partly confounded with sample size. Here every
// diagnostic is recomputed on one common set of directions.
//
// Framework is copied verbatim from regime_correlation.mjs / conditional_similarity.mjs /
// niche_corr.mjs: Spearman rho and Kendall tau-b against raw thermal transfer ROC-AUC,
// pair-based bootstrap (unordered pairs resampled with replacement, every sampled pair
// contributing BOTH ordered directions), 2000 replicates, equal-tailed percentile 95 % CI,
// mulberry32 seeded 42 + per-measure offset (regime 0.., conditional 100.., niche 200..),
// degenerate replicates dropped and counted.
//
// Inputs are the per-direction blocks of the three published JSONs. No new modelling.
import { readFileSync, writeFileSync } from 'fs';

const ROOT = 'C:/Users/CORSAIR/projects/thermal-twin';
const REGIONS = ['manavgat_2021', 'bejis_2022', 'mugla_2021', 'evia_2021_extended', 'montiferru_2021'];
const FOUR_AOI = ['manavgat_2021', 'bejis_2022', 'mugla_2021', 'evia_2021_extended'];
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
  if (sa === 0 || sb === 0) return NaN;
  return sab / Math.sqrt(sa * sb);
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

// ---------- merge the three published per-direction blocks ----------
const regimeJ = JSON.parse(readFileSync(`${ROOT}/paper/regime_transfer_correlation.json`, 'utf8'));
const condJ = JSON.parse(readFileSync(`${ROOT}/paper/conditional_similarity_transfer.json`, 'utf8'));
const nicheJ = JSON.parse(readFileSync(`${ROOT}/paper/niche_overlap_transfer.json`, 'utf8'));
const byDir = new Map();
for (const r of regimeJ.per_direction) byDir.set(r.direction, { ...r, thermal_roc: r.raw_thermal_roc_auc });
let maxAucDiff = 0;
for (const r of condJ.per_direction) {
  const d = byDir.get(r.direction);
  maxAucDiff = Math.max(maxAucDiff, Math.abs(d.thermal_roc - r.raw_thermal_roc_auc));
  Object.assign(d, { agree_count_9: r.agree_count_9, vector_spearman_9: r.vector_spearman_9, cosine_9: r.cosine_9,
    n_supported: r.n_supported, agree_fraction_supported: r.agree_fraction_supported,
    vector_spearman_supported: r.vector_spearman_supported, cosine_supported: r.cosine_supported });
}
for (const r of nicheJ.per_direction) {
  const d = byDir.get(r.direction);
  maxAucDiff = Math.max(maxAucDiff, Math.abs(d.thermal_roc - r.thermal_roc));
  for (const k of ['schoener_d_mean1d', 'warren_i_mean1d', 'schoener_d_pca2d', 'warren_i_pca2d', 'mahalanobis_burned']) d[k] = r[k];
}
if (maxAucDiff > 1e-12) throw new Error(`transfer AUC disagreement across source files: ${maxAucDiff}`);

// canonical direction order (same nested loop as every published script)
const directions = [];
for (const s of REGIONS) for (const t of REGIONS) {
  if (s === t) continue;
  const d = byDir.get(`${s}_to_${t}`);
  if (!d) throw new Error(`missing direction ${s}_to_${t}`);
  directions.push(d);
}
if (directions.length !== 20) throw new Error('expected 20 directions');

// ---------- correlation with pair-based bootstrap (verbatim) ----------
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
  const q = (arr, p) => { if (!arr.length) return NaN; const s = [...arr].sort((a, b) => a - b); const i = p * (s.length - 1); const lo = Math.floor(i), hi = Math.ceil(i); return s[lo] + (s[hi] - s[lo]) * (i - lo); };
  return { n_directions: data.length, n_pairs: pairs.length, seed_offset: seedOffset,
    spearman_rho: rho, spearman_ci95: [q(rhos, 0.025), q(rhos, 0.975)],
    kendall_tau_b: tau, kendall_ci95: [q(taus, 0.025), q(taus, 0.975)],
    n_valid_replicates: rhos.length, n_degenerate_replicates: degenerate };
}

// ---------- the twenty measures, with the seed offsets already used ----------
// regime_correlation.mjs walked its 9 measures with seedOffset++ twice each:
// measure i -> full = 2i, four_aoi_subset = 2i+1. conditional 100+i. niche 200+i.
const MEASURES = [
  { key: 'agree_fraction_supported', label: 'Agreement fraction, supported features', family: 'P(y|x) conditional', expected: '+', offset: 103, published_n: 16 },
  { key: 'cosine_supported', label: 'Cosine, supported features', family: 'P(y|x) conditional', expected: '+', offset: 105, published_n: 16 },
  { key: 'cosine_9', label: 'Cosine, all 9 features', family: 'P(y|x) conditional', expected: '+', offset: 102, published_n: 20 },
  { key: 'vector_spearman_9', label: 'Vector Spearman, all 9', family: 'P(y|x) conditional', expected: '+', offset: 101, published_n: 20 },
  { key: 'agree_count_9', label: 'Agreement count, all 9', family: 'P(y|x) conditional', expected: '+', offset: 100, published_n: 20 },
  { key: 'schoener_d_mean1d', label: "Schoener's D, 1D mean", family: 'P(x|y=1) niche', expected: '+', offset: 200, published_n: 20 },
  { key: 'warren_i_mean1d', label: "Warren's I, 1D mean", family: 'P(x|y=1) niche', expected: '+', offset: 201, published_n: 20 },
  { key: 'schoener_d_pca2d', label: "Schoener's D, PCA-2D", family: 'P(x|y=1) niche', expected: '+', offset: 202, published_n: 20 },
  { key: 'warren_i_pca2d', label: "Warren's I, PCA-2D", family: 'P(x|y=1) niche', expected: '+', offset: 203, published_n: 20 },
  { key: 'mahalanobis_burned', label: 'Mahalanobis, burned centroids', family: 'P(x|y=1) niche', expected: '-', offset: 204, published_n: 20 },
  { key: 'domain_classifier_auc', label: 'Domain-classifier AUC', family: 'P(x) marginal', expected: '-', offset: 4, published_n: 20 },
  { key: 'target_mean_dissimilarity', label: 'Predictor-space mean dissimilarity', family: 'P(x) marginal', expected: '-', offset: 6, published_n: 12 },
  { key: 'target_p95_dissimilarity', label: 'Predictor-space p95 dissimilarity', family: 'P(x) marginal', expected: '-', offset: 8, published_n: 12 },
  { key: 'fraction_inside_weighted_aoa', label: 'Fraction inside weighted AoA', family: 'P(x) marginal', expected: '+', offset: 10, published_n: 12 },
  { key: 'unweighted_fraction_inside_support', label: 'Fraction inside unweighted support', family: 'P(x) marginal', expected: '+', offset: 16, published_n: 12 },
  { key: 'climate_distance', label: 'Climatic distance', family: 'P(x) marginal', expected: '-', offset: 12, published_n: 12 },
  { key: 'geographic_distance_km', label: 'Geographic distance', family: 'geographic', expected: '-', offset: 14, published_n: 12 },
  { key: 'regime_dist_log_effn', label: 'Regime distance, log effective-N', family: 'P(y) spatial structure', expected: '-', offset: 0, published_n: 20 },
  { key: 'regime_dist_largest_share', label: 'Regime distance, largest share', family: 'P(y) spatial structure', expected: '-', offset: 2, published_n: 20 },
  { key: 'vector_spearman_supported', label: 'Vector Spearman, supported (>=3 feats)', family: 'P(y|x) conditional', expected: '+', offset: 104, published_n: 2 },
];

// ---------- verification: reproduce published rows at their original n ----------
function readCsv(path) {
  const [h, ...rows] = readFileSync(path, 'utf8').trim().split('\n');
  const cols = h.split(',');
  return rows.map(r => {
    const out = []; let cur = '', inQ = false;
    for (const ch of r) { if (inQ) { if (ch === '"') inQ = false; else cur += ch; } else if (ch === '"') inQ = true; else if (ch === ',') { out.push(cur); cur = ''; } else cur += ch; }
    out.push(cur);
    return Object.fromEntries(cols.map((c, i) => [c, out[i]]));
  });
}
const published = new Map(readCsv(`${ROOT}/paper/all_diagnostics_vs_transfer.csv`).map(r => [r.measure, r]));
const repro = [];
for (const m of MEASURES) {
  const c = corrWithBoot(directions, m.key, m.offset);
  const p = published.get(m.key);
  const fields = [['spearman_rho', c.spearman_rho], ['spearman_ci_low', c.spearman_ci95[0]], ['spearman_ci_high', c.spearman_ci95[1]],
    ['kendall_tau_b', c.kendall_tau_b], ['kendall_ci_low', c.kendall_ci95[0]], ['kendall_ci_high', c.kendall_ci95[1]]];
  let worst = 0, allNaN = true;
  for (const [f, v] of fields) {
    const pv = parseFloat(p[f]);
    if (Number.isNaN(pv) && Number.isNaN(v)) continue;
    allNaN = false;
    worst = Math.max(worst, Math.abs(pv - v));
  }
  repro.push({ measure: m.key, published_n: +p.n_directions, recomputed_n: c.n_directions,
    n_match: +p.n_directions === c.n_directions, max_abs_diff: allNaN ? null : worst,
    published: { rho: +p.spearman_rho, lo: +p.spearman_ci_low, hi: +p.spearman_ci_high },
    recomputed: { rho: c.spearman_rho, lo: c.spearman_ci95[0], hi: c.spearman_ci95[1] } });
}
// the four-AOI measures were displayed in all_diagnostics_vs_transfer.md using the
// "four_aoi_subset" seed variant (offset 2i+1), not the "full" variant in the CSV.
// Reproduce that variant too, so both published renderings are covered.
const subVariant = [];
for (const m of MEASURES.filter(m => m.published_n === 12)) {
  const c = corrWithBoot(directions, m.key, m.offset + 1);
  subVariant.push({ measure: m.key, seed_offset: m.offset + 1, n: c.n_directions,
    rho: c.spearman_rho, ci: c.spearman_ci95, tau: c.kendall_tau_b, tau_ci: c.kendall_ci95 });
}
const regimeCsv = readCsv(`${ROOT}/paper/regime_transfer_correlation.csv`).filter(r => r.set === 'four_aoi_subset');
let subWorst = 0;
for (const s of subVariant) {
  const p = regimeCsv.find(r => r.measure === s.measure);
  for (const [a, b] of [[s.rho, p.spearman_rho], [s.ci[0], p.spearman_ci_low], [s.ci[1], p.spearman_ci_high],
    [s.tau, p.kendall_tau_b], [s.tau_ci[0], p.kendall_ci_low], [s.tau_ci[1], p.kendall_ci_high]]) {
    subWorst = Math.max(subWorst, Math.abs(a - parseFloat(b)));
  }
}
const reproWorst = Math.max(...repro.filter(r => r.max_abs_diff != null).map(r => r.max_abs_diff));
console.log(`reproduction: ${repro.length} published rows, max |diff| = ${reproWorst.toExponential(2)}; n matches on ${repro.filter(r => r.n_match).length}/${repro.length}`);
console.log(`four-AOI subset seed variant: ${subVariant.length} rows, max |diff| = ${subWorst.toExponential(2)}`);
if (reproWorst > 5e-5 || subWorst > 5e-5) throw new Error('reproduction failed — STOP');

// ---------- the two common subsets ----------
const setA = directions.filter(d => FOUR_AOI.includes(d.source) && FOUR_AOI.includes(d.target)); // 12 dirs / 6 pairs
const setB = directions.filter(d => Number.isFinite(d.agree_fraction_supported));                // 16 dirs / 8 pairs
if (setA.length !== 12 || setB.length !== 16) throw new Error(`unexpected subset sizes ${setA.length}/${setB.length}`);

function runSet(rows, tag) {
  const out = [];
  for (const m of MEASURES) {
    const c = corrWithBoot(rows, m.key, m.offset);
    const nMissing = rows.length - c.n_directions;
    out.push({ subset: tag, ...m, ...c, n_subset_directions: rows.length, n_undefined_directions: nMissing,
      computable: Number.isFinite(c.spearman_rho) && Number.isFinite(c.spearman_ci95[0]),
      excludes_zero: Number.isFinite(c.spearman_ci95[0]) && Number.isFinite(c.spearman_ci95[1]) &&
        ((c.spearman_ci95[0] > 0 && c.spearman_ci95[1] > 0) || (c.spearman_ci95[0] < 0 && c.spearman_ci95[1] < 0)) });
  }
  return out;
}
const resA = runSet(setA, 'four_region_12dir');
const resB = runSet(setB, 'supported_16dir');

// ---------- outputs ----------
const fmt = v => (Number.isFinite(v) ? (v >= 0 ? '+' : '') + v.toFixed(2) : 'NA');
const fmt4 = v => (Number.isFinite(v) ? v.toFixed(4) : '');
const csv = ['subset,measure,label,family,expected_sign,published_n,n_directions,n_pairs,n_undefined_directions,seed_offset,spearman_rho,spearman_ci_low,spearman_ci_high,kendall_tau_b,kendall_ci_low,kendall_ci_high,n_valid_replicates,n_degenerate_replicates,ci_excludes_zero'];
for (const r of [...resA, ...resB]) {
  csv.push([r.subset, r.key, `"${r.label}"`, `"${r.family}"`, r.expected, r.published_n, r.n_directions, r.n_pairs,
    r.n_undefined_directions, r.seed_offset, fmt4(r.spearman_rho), fmt4(r.spearman_ci95[0]), fmt4(r.spearman_ci95[1]),
    fmt4(r.kendall_tau_b), fmt4(r.kendall_ci95[0]), fmt4(r.kendall_ci95[1]), r.n_valid_replicates,
    r.n_degenerate_replicates, r.computable ? r.excludes_zero : 'NA'].join(','));
}
// reproduction block appended as its own section of the CSV
csv.push('');
csv.push('check,measure,published_n,recomputed_n,published_rho,recomputed_rho,published_ci_low,recomputed_ci_low,published_ci_high,recomputed_ci_high,max_abs_diff');
for (const r of repro) {
  csv.push(['reproduction', r.measure, r.published_n, r.recomputed_n, fmt4(r.published.rho), fmt4(r.recomputed.rho),
    fmt4(r.published.lo), fmt4(r.recomputed.lo), fmt4(r.published.hi), fmt4(r.recomputed.hi),
    r.max_abs_diff == null ? 'NA' : r.max_abs_diff.toExponential(2)].join(','));
}
writeFileSync(`${ROOT}/paper/diagnostics_common_subset.csv`, csv.join('\n') + '\n');

writeFileSync(`${ROOT}/paper/diagnostics_common_subset.json`, JSON.stringify({
  meta: {
    created: '2026-08-13',
    purpose: 'Recompute every Table 6 diagnostic on a common set of transfer directions, so that the marginal-versus-conditional contrast is not confounded with sample size.',
    framework: 'identical to regime_correlation.mjs / conditional_similarity.mjs / niche_corr.mjs',
    bootstrap: { scheme: 'unordered pairs resampled with replacement, both ordered directions carried', n_replicates: NBOOT, seed: SEED, prng: 'mulberry32', ci: 'equal-tailed percentile 95%' },
    seed_offsets: 'per measure, as already published: regime 42+2i (full-set variant), conditional 42+100+i, niche 42+200+i',
    subsets: {
      four_region_12dir: { regions: FOUR_AOI, n_directions: 12, n_pairs: 6, note: 'the set on which the marginal, AoA, climatic and geographic diagnostics exist (Montiferru excluded)' },
      supported_16dir: { n_directions: 16, n_pairs: 8, note: 'the set on which the supported-conditional index is defined (Manavgat~Montiferru and Bejis~Montiferru have no jointly supported feature)' },
    },
    inputs: ['paper/regime_transfer_correlation.json', 'paper/conditional_similarity_transfer.json', 'paper/niche_overlap_transfer.json'],
    transfer_metric: 'raw thermal ROC-AUC on target, source-only RF (step9b), TSG population',
  },
  reproduction_check: { published_rows: repro, four_aoi_seed_variant: subVariant, max_abs_diff_published_csv: reproWorst, max_abs_diff_four_aoi_variant: subWorst },
  four_region_12dir: resA,
  supported_16dir: resB,
}, null, 1));

// ---------- console ----------
for (const [tag, res] of [['SUBSET A — 12 directions / 6 pairs (four regions)', resA], ['SUBSET B — 16 directions / 8 pairs (supported set)', resB]]) {
  console.log(`\n${tag}`);
  console.log('measure                              fam            n  pairs  rho     [95% CI]           excl0');
  for (const r of res) {
    console.log(`${r.key.padEnd(36)} ${r.family.slice(0, 12).padEnd(14)} ${String(r.n_directions).padStart(2)} ${String(r.n_pairs).padStart(5)}  ${fmt(r.spearman_rho).padStart(6)}  [${fmt(r.spearman_ci95[0])},${fmt(r.spearman_ci95[1])}]  ${r.computable ? (r.excludes_zero ? 'YES' : '-') : 'not computable'}`);
  }
}
