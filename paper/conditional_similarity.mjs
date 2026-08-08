// Analysis 1 — conditional similarity (signed-AUC agreement) as a formal transfer predictor.
// Moreno-Torres 2012 framing: marginal P(x) similarity failed (8 measures); does P(y|x)
// similarity — direction/shape of univariate feature-response relations — order transfer?
// Candidate set FIXED in advance: (a) sign-agreement count, (b) Spearman between the two
// 9-dim signed-AUC vectors, (c) cosine similarity of (AUC-0.5) vectors; plus the same three
// restricted to features whose 95% CI excludes 0.5 in BOTH regions of the pair.
import { readFileSync, writeFileSync } from 'fs';
import { createHash } from 'crypto';

const ROOT = 'C:/Users/CORSAIR/projects/thermal-twin';
const REGIONS = ['manavgat_2021', 'bejis_2022', 'mugla_2021', 'evia_2021_extended', 'montiferru_2021'];
const POP = 'burnable_tree_shrub_grass';
const NBOOT = 2000;
const SEED = 42;
const FEATURES = ['ndvi_mean', 'elevation_mean', 'slope_mean', 'lst_anomaly_mean', 'current_lst_mean',
  'current_tvdi_mean', 'tvdi_difference_mean', 'downscaled_lst_mean', 'fused_lst_mean'];

function mulberry32(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
function parseCSV(text) {
  const rows = []; let row = []; let cur = ''; let inQ = false;
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (inQ) { if (ch === '"') { if (text[i + 1] === '"') { cur += '"'; i++; } else inQ = false; } else cur += ch; }
    else if (ch === '"') inQ = true;
    else if (ch === ',') { row.push(cur); cur = ''; }
    else if (ch === '\n') { row.push(cur.replace(/\r$/, '')); rows.push(row); row = []; cur = ''; }
    else cur += ch;
  }
  if (cur !== '' || row.length) { row.push(cur.replace(/\r$/, '')); rows.push(row); }
  const header = rows[0];
  return rows.slice(1).filter(r => r.length > 1).map(r => Object.fromEntries(header.map((h, i) => [h, r[i]])));
}
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
function spearman(x, y) { return pearson(avgRanks(x), avgRanks(y)); }
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
function cosine(a, b) {
  let ab = 0, aa = 0, bb = 0;
  for (let i = 0; i < a.length; i++) { ab += a[i] * b[i]; aa += a[i] * a[i]; bb += b[i] * b[i]; }
  if (aa === 0 || bb === 0) return NaN;
  return ab / Math.sqrt(aa * bb);
}

// ---------- signed AUC per region (from Emrehan's 5-AOI feature stability table) ----------
const srcPath = `${ROOT}/drive_new/diagnostics/multi_aoi_transfer_synthesis/bejis_2022__evia_2021_extended__manavgat_2021__montiferru_2021__mugla_2021/multi_aoi_feature_stability.csv`;
const srcBytes = readFileSync(srcPath);
const srcSha = createHash('sha256').update(srcBytes).digest('hex');
const fs_ = parseCSV(srcBytes.toString('utf8'));
const signed = {}; // region -> feature -> {auc, lo, hi}
function put(region, feature, auc, lo, hi) {
  signed[region] = signed[region] || {};
  const prev = signed[region][feature];
  if (prev && (Math.abs(prev.auc - auc) > 1e-9 || Math.abs(prev.lo - lo) > 1e-9)) {
    throw new Error(`inconsistent signed AUC for ${region}/${feature} across pair rows`);
  }
  signed[region][feature] = { auc, lo, hi };
}
for (const r of fs_) {
  put(r.experiment_a, r.feature, +r.experiment_a_auc, +r.experiment_a_ci_low, +r.experiment_a_ci_high);
  put(r.experiment_b, r.feature, +r.experiment_b_auc, +r.experiment_b_ci_low, +r.experiment_b_ci_high);
}
for (const reg of REGIONS) for (const f of FEATURES) {
  if (!signed[reg] || !signed[reg][f]) throw new Error(`missing signed AUC ${reg}/${f}`);
}

// ---------- pair-level conditional similarity ----------
function pairMeasures(a, b) {
  const va = FEATURES.map(f => signed[a][f].auc - 0.5);
  const vb = FEATURES.map(f => signed[b][f].auc - 0.5);
  const agree = FEATURES.filter((f, i) => Math.sign(va[i]) === Math.sign(vb[i]) && va[i] !== 0 && vb[i] !== 0).length;
  // restricted: CI excludes 0.5 in BOTH regions (each side's sign established)
  const supIdx = FEATURES.map((f, i) => i).filter(i => {
    const f = FEATURES[i];
    const A = signed[a][f], B = signed[b][f];
    return (A.lo > 0.5 || A.hi < 0.5) && (B.lo > 0.5 || B.hi < 0.5);
  });
  const supFeatures = supIdx.map(i => FEATURES[i]);
  const supAgreeList = supIdx.filter(i => Math.sign(va[i]) === Math.sign(vb[i]));
  const sa = supIdx.map(i => va[i]), sb = supIdx.map(i => vb[i]);
  return {
    agree_count_9: agree,
    vector_spearman_9: spearman(va, vb),
    cosine_9: cosine(va, vb),
    n_supported: supIdx.length,
    supported_features: supFeatures,
    agree_count_supported: supAgreeList.length,
    agree_fraction_supported: supIdx.length ? supAgreeList.length / supIdx.length : NaN,
    vector_spearman_supported: supIdx.length >= 3 ? spearman(sa, sb) : NaN,
    cosine_supported: supIdx.length >= 1 ? cosine(sa, sb) : NaN,
  };
}

// consistency check vs RESULTS_INVENTORY §5b.1 (three-pair agreement counts)
const check = [
  ['bejis_2022', 'mugla_2021', 7],
  ['manavgat_2021', 'mugla_2021', 4],
  ['manavgat_2021', 'bejis_2022', 4],
];
for (const [a, b, exp] of check) {
  const got = pairMeasures(a, b).agree_count_9;
  if (got !== exp) throw new Error(`agreement count mismatch ${a}~${b}: got ${got}, expected ${exp} (RESULTS_INVENTORY 5b.1) — STOP`);
}

// bootstrap-supported direction reversals (both CIs exclude 0.5, opposite sides) — needed by Analysis 3
const supportedReversals = [];
for (let i = 0; i < REGIONS.length; i++) for (let j = i + 1; j < REGIONS.length; j++) {
  for (const f of FEATURES) {
    const A = signed[REGIONS[i]][f], B = signed[REGIONS[j]][f];
    const aSideEst = A.lo > 0.5 ? 1 : (A.hi < 0.5 ? -1 : 0);
    const bSideEst = B.lo > 0.5 ? 1 : (B.hi < 0.5 ? -1 : 0);
    if (aSideEst !== 0 && bSideEst !== 0 && aSideEst !== bSideEst) {
      supportedReversals.push({ feature: f, region_a: REGIONS[i], region_b: REGIONS[j], auc_a: A.auc, ci_a: [A.lo, A.hi], auc_b: B.auc, ci_b: [B.lo, B.hi] });
    }
  }
}
// cross-check vs Emrehan's reversal_status flags in the same CSV
const emrehanSupported = fs_.filter(r => r.reversal_status === 'bootstrap_supported_direction_reversal')
  .map(r => `${r.feature}|${[r.experiment_a, r.experiment_b].sort().join('~')}`).sort();
const oursSupported = supportedReversals.map(r => `${r.feature}|${[r.region_a, r.region_b].sort().join('~')}`).sort();
if (JSON.stringify(emrehanSupported) !== JSON.stringify(oursSupported)) {
  throw new Error(`supported-reversal set mismatch vs Emrehan flags:\nEmrehan: ${emrehanSupported.join(', ')}\nOurs: ${oursSupported.join(', ')} — STOP`);
}

// ---------- transfer AUCs (20 canonical directions, TSG, raw thermal) ----------
const pairFolders = ['manavgat_2021__bejis_2022', 'manavgat_2021__mugla_2021', 'manavgat_2021__evia_2021_extended',
  'montiferru_2021__manavgat_2021', 'montiferru_2021__bejis_2022', 'montiferru_2021__mugla_2021',
  'montiferru_2021__evia_2021_extended', 'bejis_2022__mugla_2021', 'bejis_2022__evia_2021_extended',
  'mugla_2021__evia_2021_extended'];
const transfer = new Map();
for (const folder of pairFolders) {
  const m = JSON.parse(readFileSync(`${ROOT}/drive_new/cross_region/${folder}/step9b/cross_region_transfer_metrics.json`, 'utf8'));
  for (const r of m.results) if (r.population === POP && !r.skipped) transfer.set(r.transfer_direction, r.thermal_metrics.roc_auc);
}
const directions = [];
for (const s of REGIONS) for (const t of REGIONS) {
  if (s === t) continue;
  const d = { source: s, target: t, direction: `${s}_to_${t}`, thermal_roc: transfer.get(`${s}_to_${t}`) };
  if (d.thermal_roc == null) throw new Error(`missing transfer ${d.direction}`);
  Object.assign(d, pairMeasures(s, t));
  directions.push(d);
}

// ---------- correlation with pair-based bootstrap (identical framework to regime analysis) ----------
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
  const q = (arr, p) => { const s = [...arr].sort((a, b) => a - b); const i = p * (s.length - 1); const lo = Math.floor(i), hi = Math.ceil(i); return s[lo] + (s[hi] - s[lo]) * (i - lo); };
  return { n_directions: data.length, n_pairs: pairs.length,
    spearman_rho: rho, spearman_ci95: [q(rhos, 0.025), q(rhos, 0.975)],
    kendall_tau_b: tau, kendall_ci95: [q(taus, 0.025), q(taus, 0.975)],
    n_valid_replicates: rhos.length, n_degenerate_replicates: degenerate };
}

const MEASURES = [
  { key: 'agree_count_9', label: 'Sign-agreement count, all 9 features', expected: 'positive' },
  { key: 'vector_spearman_9', label: 'Signed-AUC vector Spearman, all 9 features', expected: 'positive' },
  { key: 'cosine_9', label: 'Signed-AUC (AUC-0.5) cosine similarity, all 9 features', expected: 'positive' },
  { key: 'agree_fraction_supported', label: 'Sign-agreement fraction, features with both CIs excluding 0.5', expected: 'positive' },
  { key: 'vector_spearman_supported', label: 'Signed-AUC vector Spearman, supported features only (n>=3)', expected: 'positive' },
  { key: 'cosine_supported', label: 'Signed-AUC cosine, supported features only', expected: 'positive' },
];
const results = [];
let so = 100; // distinct seed offsets from the regime run
for (const m of MEASURES) results.push({ ...m, full_set: corrWithBoot(directions, m.key, so++) });

// ---------- outputs ----------
const meta = {
  created: '2026-08-08',
  analysis: 'Analysis 1 — conditional similarity (signed univariate AUC agreement) vs raw thermal transfer ROC-AUC',
  theoretical_frame: 'Moreno-Torres et al. 2012: covariate shift = P(x) change, concept shift = P(y|x) change. The eight marginal (P(x)-side) diagnostics fail (paper/regime_transfer_correlation.*); these six candidates measure P(y|x) direction similarity.',
  candidate_set_fixed_in_advance: true,
  population: POP,
  transfer_metric: 'raw thermal ROC-AUC on target, source-only RF (step9b), TSG, 20 ordered directions',
  bootstrap: { scheme: 'unordered pairs resampled with replacement, both directions carried', n_replicates: NBOOT, seed: SEED, prng: 'mulberry32', ci: 'equal-tailed percentile 95%' },
  provenance: {
    signed_auc_source: { path: srcPath.replace(ROOT + '/', ''), sha256: srcSha },
    transfer_source: 'drive_new/cross_region/<pair>/step9b/cross_region_transfer_metrics.json (bidirectional)',
    consistency_checks: [
      'per-region signed AUC identical across every pair row it appears in (enforced)',
      'agreement counts reproduce RESULTS_INVENTORY 5b.1: Bejis~Mugla 7/9, Manavgat~Mugla 4/9, Manavgat~Bejis 4/9 (enforced)',
      'supported-reversal set matches Emrehan reversal_status flags exactly (enforced)',
    ],
  },
  supported_reversal_criterion: 'both regions CIs exclude 0.5, point estimates on opposite sides (Emrehan step9g criterion; stricter than disjoint-CIs)',
  bootstrap_supported_reversals: supportedReversals,
  reversal_feature_set_for_analysis3: [...new Set(supportedReversals.map(r => r.feature))],
};
const perDirection = directions.map(d => ({
  direction: d.direction, raw_thermal_roc_auc: d.thermal_roc,
  agree_count_9: d.agree_count_9, vector_spearman_9: d.vector_spearman_9, cosine_9: d.cosine_9,
  n_supported: d.n_supported, supported_features: d.supported_features,
  agree_count_supported: d.agree_count_supported, agree_fraction_supported: d.agree_fraction_supported,
  vector_spearman_supported: Number.isFinite(d.vector_spearman_supported) ? d.vector_spearman_supported : null,
  cosine_supported: Number.isFinite(d.cosine_supported) ? d.cosine_supported : null,
}));
writeFileSync(`${ROOT}/paper/conditional_similarity_transfer.json`, JSON.stringify({ meta, signed_auc_by_region: signed, per_direction: perDirection, correlations: results }, null, 2));

const csv = ['measure,label,expected_sign,n_directions,n_pairs,spearman_rho,spearman_ci_low,spearman_ci_high,kendall_tau_b,kendall_ci_low,kendall_ci_high,n_valid_replicates'];
for (const r of results) {
  const c = r.full_set;
  csv.push([r.key, `"${r.label}"`, r.expected, c.n_directions, c.n_pairs,
    c.spearman_rho.toFixed(4), c.spearman_ci95[0].toFixed(4), c.spearman_ci95[1].toFixed(4),
    c.kendall_tau_b.toFixed(4), c.kendall_ci95[0].toFixed(4), c.kendall_ci95[1].toFixed(4), c.n_valid_replicates].join(','));
}
writeFileSync(`${ROOT}/paper/conditional_similarity_transfer.csv`, csv.join('\n') + '\n');

console.log('supported reversals:', JSON.stringify(meta.bootstrap_supported_reversals.map(r => `${r.feature}: ${r.region_a}~${r.region_b}`)));
console.log('reversal feature set for Analysis 3:', meta.reversal_feature_set_for_analysis3.join(', '));
console.log('\nper-pair conditional similarity (symmetric):');
const seen = new Set();
for (const d of directions) {
  const k = pairKey(d);
  if (seen.has(k)) continue; seen.add(k);
  console.log(`${k.padEnd(40)} agree=${d.agree_count_9}/9 vecSp=${d.vector_spearman_9.toFixed(3)} cos=${d.cosine_9.toFixed(3)} | sup n=${d.n_supported} agree=${d.agree_count_supported}/${d.n_supported} cosSup=${Number.isFinite(d.cosine_supported) ? d.cosine_supported.toFixed(3) : 'NA'} | meanAUC(dirs)=${(directions.filter(x => pairKey(x) === k).reduce((s, x) => s + x.thermal_roc, 0) / 2).toFixed(3)}`);
}
console.log('\nmeasure                                   n   rho     [95% CI]            tau     [95% CI]');
for (const r of results) {
  const c = r.full_set;
  console.log(`${r.key.padEnd(40)} ${String(c.n_directions).padStart(3)} ${c.spearman_rho.toFixed(3).padStart(6)}  [${c.spearman_ci95[0].toFixed(3)},${c.spearman_ci95[1].toFixed(3)}]  ${c.kendall_tau_b.toFixed(3).padStart(6)}  [${c.kendall_ci95[0].toFixed(3)},${c.kendall_ci95[1].toFixed(3)}]`);
}
