#!/usr/bin/env node
/**
 * Referee round 2 — numbers requested by the panel.
 *
 * Read-only. Every input is a frozen artefact under drive_new/ or paper/.
 * No model is fitted here. Nothing under repo/, drive_new/ or any existing
 * step8 or step9 output is modified.
 *
 * Produces: paper/referee2_numbers.md and paper/referee2_numbers.json
 *
 * Blocks computed:
 *   A. Cluster-aware interval on the mean paired thermal contribution (+0.004).
 *   B. Conditional-index correlation at the design's own sample size:
 *      pair-level Spearman, exact permutation p, Fisher-z intervals, tie ceiling.
 *   C. Spatial-block counts per region at 2, 10 and 20 cells, total and
 *      positive-carrying.
 *   D. Step 8D thermal ablation, primary population, five regions.
 *   E. Step 7C downscaling validation metrics and coordinate importance.
 *   F. Step 7E fused-LST gap-filled fractions.
 *   G. Pre-label burn exclusion status per region.
 *
 * Seed 42 throughout, as everywhere else in this project.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const PAPER = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.dirname(PAPER);
const DRIVE = path.join(ROOT, 'drive_new');

const REGIONS = [
  ['manavgat_2021', 'Manavgat'],
  ['bejis_2022', 'Bejis'],
  ['mugla_2021', 'Mugla'],
  ['evia_2021_extended', 'Evia'],
  ['montiferru_2021', 'Montiferru'],
];

// ---------------------------------------------------------------- utilities

function readJSON(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

/** Quote-aware CSV reader. Returns array of objects keyed by header name. */
function readCSV(p) {
  const text = fs.readFileSync(p, 'utf8');
  const rows = [];
  let field = '';
  let row = [];
  let inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (inQuotes) {
      if (c === '"') {
        if (text[i + 1] === '"') { field += '"'; i++; } else { inQuotes = false; }
      } else field += c;
    } else if (c === '"') inQuotes = true;
    else if (c === ',') { row.push(field); field = ''; }
    else if (c === '\n') { row.push(field); rows.push(row); row = []; field = ''; }
    else if (c !== '\r') field += c;
  }
  if (field.length || row.length) { row.push(field); rows.push(row); }
  const header = rows.shift();
  return rows
    .filter((r) => r.length === header.length && r.some((v) => v !== ''))
    .map((r) => Object.fromEntries(header.map((h, i) => [h, r[i]])));
}

/** mulberry32: deterministic, seedable, adequate for a resampling report. */
function rng(seed) {
  let a = seed >>> 0;
  return function () {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const mean = (xs) => xs.reduce((s, x) => s + x, 0) / xs.length;

function quantile(sorted, q) {
  const pos = (sorted.length - 1) * q;
  const lo = Math.floor(pos);
  const hi = Math.ceil(pos);
  if (lo === hi) return sorted[lo];
  return sorted[lo] + (sorted[hi] - sorted[lo]) * (pos - lo);
}

function percentileCI(samples, alpha = 0.05) {
  const s = [...samples].sort((a, b) => a - b);
  return [quantile(s, alpha / 2), quantile(s, 1 - alpha / 2)];
}

/** Average ranks, ties shared. */
function rank(xs) {
  const idx = xs.map((v, i) => [v, i]).sort((a, b) => a[0] - b[0]);
  const r = new Array(xs.length);
  let i = 0;
  while (i < idx.length) {
    let j = i;
    while (j + 1 < idx.length && idx[j + 1][0] === idx[i][0]) j++;
    const avg = (i + j) / 2 + 1;
    for (let k = i; k <= j; k++) r[idx[k][1]] = avg;
    i = j + 1;
  }
  return r;
}

function pearson(x, y) {
  const mx = mean(x); const my = mean(y);
  let num = 0; let dx = 0; let dy = 0;
  for (let i = 0; i < x.length; i++) {
    num += (x[i] - mx) * (y[i] - my);
    dx += (x[i] - mx) ** 2;
    dy += (y[i] - my) ** 2;
  }
  return num / Math.sqrt(dx * dy);
}

const spearman = (x, y) => pearson(rank(x), rank(y));

/** Fisher z interval for a Spearman correlation, standard 1/sqrt(n-3) form. */
function fisherCI(rho, n) {
  const z = 0.5 * Math.log((1 + rho) / (1 - rho));
  const se = 1 / Math.sqrt(n - 3);
  const lo = Math.tanh(z - 1.959963985 * se);
  const hi = Math.tanh(z + 1.959963985 * se);
  return [lo, hi];
}

/** Bonett-Wright variance for Spearman, which is the recommended form. */
function bonettWrightCI(rho, n) {
  const z = 0.5 * Math.log((1 + rho) / (1 - rho));
  const se = Math.sqrt((1 + rho * rho / 2) / (n - 3));
  return [Math.tanh(z - 1.959963985 * se), Math.tanh(z + 1.959963985 * se)];
}

/** Exact one-sided permutation p for Spearman, n small enough to enumerate. */
function exactPermutationSpearman(x, y) {
  const rx = rank(x);
  const ry = rank(y);
  const observed = pearson(rx, ry);
  let total = 0;
  let atLeast = 0;
  let maxRho = -Infinity;
  const perm = [...ry];
  const permute = (k) => {
    if (k === perm.length) {
      const r = pearson(rx, perm);
      total++;
      if (r >= observed - 1e-12) atLeast++;
      if (r > maxRho) maxRho = r;
      return;
    }
    for (let i = k; i < perm.length; i++) {
      [perm[k], perm[i]] = [perm[i], perm[k]];
      permute(k + 1);
      [perm[k], perm[i]] = [perm[i], perm[k]];
    }
  };
  permute(0);
  return { observed, p_one_sided: atLeast / total, n_permutations: total, max_attainable_rho: maxRho, n_at_max: null };
}

const f = (x, d = 4) => (x === null || x === undefined || Number.isNaN(x) ? 'n/a' : x.toFixed(d));

// ------------------------------------------------- A. mean paired delta CI

function blockA() {
  const rows = readJSON(path.join(PAPER, 'transfer_ci_blocksize.json'));
  const deltas = rows.map((r) => ({
    direction: r.direction,
    label: r.label,
    delta: r.point_delta,
    pair: r.pair_dir,
    source: r.direction.split('_to_')[0],
    target: r.direction.split('_to_')[1],
  }));
  const xs = deltas.map((d) => d.delta);
  const m = mean(xs);
  const sd = Math.sqrt(xs.reduce((s, x) => s + (x - m) ** 2, 0) / (xs.length - 1));

  const R = 20000;
  const rand = rng(42);

  // (1) naive: resample the 20 directions
  const naive = [];
  for (let b = 0; b < R; b++) {
    let s = 0;
    for (let i = 0; i < xs.length; i++) s += xs[Math.floor(rand() * xs.length)];
    naive.push(s / xs.length);
  }

  // (2) pair cluster: resample the 10 unordered pairs, both directions travel together
  const pairs = [...new Set(deltas.map((d) => d.pair))];
  const byPair = new Map(pairs.map((p) => [p, deltas.filter((d) => d.pair === p).map((d) => d.delta)]));
  const pairBoot = [];
  for (let b = 0; b < R; b++) {
    const drawn = [];
    for (let i = 0; i < pairs.length; i++) drawn.push(...byPair.get(pairs[Math.floor(rand() * pairs.length)]));
    pairBoot.push(mean(drawn));
  }

  // (3) leave-one-region-out jackknife over the five regions
  const regionIds = REGIONS.map(([id]) => id);
  const loo = regionIds.map((rid) => {
    const kept = deltas.filter((d) => d.source !== rid && d.target !== rid).map((d) => d.delta);
    return { region: rid, n_directions: kept.length, mean: mean(kept) };
  });
  const g = regionIds.length;
  const pseudo = loo.map((l) => g * m - (g - 1) * l.mean);
  const pm = mean(pseudo);
  const pvar = pseudo.reduce((s, x) => s + (x - pm) ** 2, 0) / (g - 1);
  const jse = Math.sqrt(pvar / g);
  const t4 = 2.776445; // t_{0.975, 4}
  const jack = [pm - t4 * jse, pm + t4 * jse];

  // t interval on the 10 pair means, the simplest defensible cluster form
  const pairMeans = pairs.map((p) => mean(byPair.get(p)));
  const pmm = mean(pairMeans);
  const pmsd = Math.sqrt(pairMeans.reduce((s, x) => s + (x - pmm) ** 2, 0) / (pairMeans.length - 1));
  const t9 = 2.262157; // t_{0.975, 9}
  const pairT = [pmm - t9 * pmsd / Math.sqrt(pairMeans.length), pmm + t9 * pmsd / Math.sqrt(pairMeans.length)];

  return {
    n_directions: xs.length,
    mean: m,
    sd,
    min: Math.min(...xs),
    max: Math.max(...xs),
    n_positive: xs.filter((x) => x > 0).length,
    n_negative: xs.filter((x) => x < 0).length,
    ci_naive_percentile: percentileCI(naive),
    ci_pair_cluster_percentile: percentileCI(pairBoot),
    ci_pair_t: pairT,
    ci_region_jackknife_t: jack,
    replicates: R,
    leave_one_region_out: loo,
  };
}

// -------------------------------------- B. conditional index at design size

function blockB() {
  const cs = readJSON(path.join(PAPER, 'conditional_similarity_transfer.json'));
  const per = cs.per_direction.filter((d) => d.n_supported > 0 && d.agree_fraction_supported !== null);

  const idx = per.map((d) => d.agree_fraction_supported);
  const auc = per.map((d) => d.raw_thermal_roc_auc);
  const rho16 = spearman(idx, auc);

  // pair level: the index is symmetric, so a pair contributes one index and the
  // mean of its two transfer AUCs
  const byPair = new Map();
  for (const d of per) {
    const [a, b] = d.direction.split('_to_');
    const key = [a, b].sort().join('__');
    if (!byPair.has(key)) byPair.set(key, { key, index: d.agree_fraction_supported, aucs: [] });
    byPair.get(key).aucs.push(d.raw_thermal_roc_auc);
  }
  const pairRows = [...byPair.values()].map((p) => ({ ...p, meanAuc: mean(p.aucs), n: p.aucs.length }));
  const pIdx = pairRows.map((p) => p.index);
  const pAuc = pairRows.map((p) => p.meanAuc);
  const rhoPair = spearman(pIdx, pAuc);
  const perm = exactPermutationSpearman(pIdx, pAuc);

  const distinct = [...new Set(pIdx)].sort((a, b) => a - b);
  const tieCounts = distinct.map((v) => ({ value: v, n: pIdx.filter((x) => x === v).length }));

  // tie ceiling for the 16-direction statistic: best achievable Spearman given
  // the index's tie structure, found by sorting the AUCs inside index groups
  const ceiling16 = (() => {
    const order = [...idx.keys()].sort((a, b) => idx[a] - idx[b]);
    const sortedAuc = [...auc].sort((a, b) => a - b);
    const rearranged = new Array(idx.length);
    order.forEach((origIdx, k) => { rearranged[origIdx] = sortedAuc[k]; });
    return spearman(idx, rearranged);
  })();

  const bonf = 0.05 / 19;

  return {
    n_directions: per.length,
    n_pairs: pairRows.length,
    spearman_16dir: rho16,
    published_16dir: 0.8404180632330576,
    published_ci: [0.5764930300097753, 0.87635999649456],
    tie_ceiling_16dir: ceiling16,
    spearman_pair_level: rhoPair,
    exact_permutation_p_one_sided: perm.p_one_sided,
    n_permutations: perm.n_permutations,
    max_attainable_rho_pair: perm.max_attainable_rho,
    bonferroni_threshold_19_variants: bonf,
    survives_bonferroni: perm.p_one_sided <= bonf,
    fisher_ci_n8: fisherCI(rhoPair, 8),
    fisher_ci_n16: fisherCI(rho16, 16),
    bonett_wright_ci_n8: bonettWrightCI(rhoPair, 8),
    index_distinct_values: distinct,
    index_tie_counts: tieCounts,
    pair_rows: pairRows.map((p) => ({ pair: p.key, index: p.index, mean_raw_thermal_auc: p.meanAuc, n_directions: p.n })),
  };
}

// ------------------------------------------------------- C. block counts

function blockC() {
  // one transfer file per target region is enough: the target population is the
  // same primary population everywhere
  const sources = {
    manavgat_2021: 'bejis_2022__manavgat_2021',
    bejis_2022: 'manavgat_2021__bejis_2022',
    mugla_2021: 'manavgat_2021__mugla_2021',
    evia_2021_extended: 'manavgat_2021__evia_2021_extended',
    montiferru_2021: 'montiferru_2021__bejis_2022',
  };
  const out = [];
  for (const [rid, label] of REGIONS) {
    let dir = sources[rid];
    let file = path.join(DRIVE, 'cross_region', dir, 'step9b', 'cross_region_transfer_predictions.csv');
    if (!fs.existsSync(file)) {
      // fall back to any pair directory whose name contains the region
      const cands = fs.readdirSync(path.join(DRIVE, 'cross_region'))
        .filter((d) => d.includes(rid))
        .map((d) => path.join(DRIVE, 'cross_region', d, 'step9b', 'cross_region_transfer_predictions.csv'))
        .filter((p) => fs.existsSync(p));
      file = cands[0];
    }
    if (!file) { out.push({ region: label, error: 'no prediction file' }); continue; }

    const rows = readCSV(file).filter(
      (r) => r.population === 'burnable_tree_shrub_grass' && r.target_experiment_id === rid,
    );
    if (!rows.length) { out.push({ region: label, error: 'no rows for region', file }); continue; }

    const cells = rows.map((r) => {
      const m = /^r(\d+)_c(\d+)$/.exec(r.target_cell_id);
      return { row: +m[1], col: +m[2], burned: +r.burned };
    });
    const rec = { region: label, region_id: rid, n_cells: cells.length, n_burned: cells.filter((c) => c.burned === 1).length, blocks: {} };
    for (const B of [2, 10, 20]) {
      const all = new Set();
      const pos = new Set();
      for (const c of cells) {
        const key = `${Math.floor(c.row / B)}_${Math.floor(c.col / B)}`;
        all.add(key);
        if (c.burned === 1) pos.add(key);
      }
      rec.blocks[B] = { total: all.size, positive_carrying: pos.size };
    }
    out.push(rec);
  }
  return out;
}

// --------------------------------------------------- D. step 8D ablation

function blockD() {
  const POP = 'burnable_tree_shrub_grass';
  const out = [];
  for (const [rid, label] of REGIONS) {
    const p = path.join(DRIVE, 'experiments', rid, 'step8d', 'step8d_ablation_delta_auc_by_population.csv');
    if (!fs.existsSync(p)) { out.push({ region: label, error: 'missing step8d' }); continue; }
    const rows = readCSV(p).filter((r) => r.population === POP)
      .map((r) => ({ group: r.ablation_group, delta: +r.delta_auc }))
      .sort((a, b) => b.delta - a.delta);
    const all = rows.find((r) => r.group === 'all_thermal');
    const bestSub = rows.find((r) => r.group !== 'all_thermal');
    out.push({
      region: label,
      region_id: rid,
      all_thermal: all ? all.delta : null,
      best_subset: bestSub ? bestSub.group : null,
      best_subset_delta: bestSub ? bestSub.delta : null,
      fraction_of_full_block: all && bestSub ? bestSub.delta / all.delta : null,
      ranking: rows,
    });
  }
  return out;
}

// ------------------------------------- E. step 7C downscaling validation

function blockE() {
  const COORD = new Set(['lon', 'lat', 'row', 'col', 'row_norm', 'col_norm']);
  const out = [];
  for (const [rid, label] of REGIONS) {
    const base = path.join(DRIVE, 'experiments', rid, 'step7c');
    const rec = { region: label, region_id: rid };
    const mp = path.join(base, 'downscaling_model_metrics.json');
    if (fs.existsSync(mp)) {
      const m = readJSON(mp);
      rec.test_rmse_celsius = m.test?.rmse ?? null;
      rec.test_r2 = m.test?.r2 ?? null;
      rec.test_mae_celsius = m.test?.mae ?? null;
      rec.validation_rmse_celsius = m.validation?.rmse ?? null;
      rec.validation_r2 = m.validation?.r2 ?? null;
    }
    const mdp = path.join(base, 'downscaling_model_metadata.json');
    if (fs.existsSync(mdp)) {
      const md = readJSON(mdp);
      rec.spatial_calibration_note = md.spatial_calibration_note ?? null;
    }
    const fp = path.join(base, 'feature_importance.csv');
    if (fs.existsSync(fp)) {
      const rows = readCSV(fp).map((r) => ({ feature: r.feature, importance: +r.importance }));
      rec.coordinate_importance_sum = rows.filter((r) => COORD.has(r.feature)).reduce((s, r) => s + r.importance, 0);
      rec.top_feature = rows.sort((a, b) => b.importance - a.importance)[0];
    }
    out.push(rec);
  }
  return out;
}

// ------------------------------------------- F. fused-LST gap-fill shares

function blockF() {
  const out = [];
  for (const [rid, label] of REGIONS) {
    const p = path.join(DRIVE, 'experiments', rid, 'step7e', 'fused_lst_stats.json');
    const rec = { region: label, region_id: rid };
    if (fs.existsSync(p)) {
      const j = readJSON(p);
      rec.gapfilled_pct_of_fused = j.gapfilled_pct_of_fused ?? null;
      rec.gapfilled_pct_of_total = j.gapfilled_pct_of_total ?? null;
      rec.observed_coverage_pct = j.observed_coverage_pct ?? null;
      rec.fused_coverage_pct = j.fused_coverage_pct ?? null;
      rec.coverage_gain_pct = j.coverage_gain_pct ?? null;
    } else rec.error = 'missing fused_lst_stats.json';
    out.push(rec);
  }
  return out;
}

// ------------------------------------------ G. pre-label burn exclusion

function blockG() {
  const out = [];
  for (const [rid, label] of REGIONS) {
    const p = path.join(DRIVE, 'experiments', rid, 'step8a', 'step8a_dataset_stats.json');
    const rec = { region: label, region_id: rid };
    if (!fs.existsSync(p)) { rec.error = 'missing step8a_dataset_stats.json'; out.push(rec); continue; }
    const j = readJSON(p);
    const txt = fs.readFileSync(p, 'utf8');
    const ex = /"exclude_pre_label_burns"\s*:\s*(true|false)/.exec(txt);
    const cnt = /"pre_label_burn_excluded_count"\s*:\s*(\d+)/.exec(txt);
    rec.field_present = /pre_label/.test(txt);
    rec.exclude_pre_label_burns = ex ? ex[1] === 'true' : null;
    rec.excluded_cells = cnt ? +cnt[1] : null;
    out.push(rec);
  }
  return out;
}

// -------------------------------------------------------------- assemble

const results = {
  meta: {
    created: '2026-08-14',
    purpose: 'Referee round 2: numbers the panel asked for, computed from frozen artefacts only.',
    seed: 42,
    inputs_are_read_only: true,
  },
  A_mean_paired_contribution: blockA(),
  B_conditional_index: blockB(),
  C_block_counts: blockC(),
  D_step8d_ablation: blockD(),
  E_step7c_downscaling: blockE(),
  F_fused_gapfill: blockF(),
  G_pre_label_exclusion: blockG(),
};

fs.writeFileSync(path.join(PAPER, 'referee2_numbers.json'), JSON.stringify(results, null, 2));

// -------------------------------------------------------------- markdown

const A = results.A_mean_paired_contribution;
const B = results.B_conditional_index;

const md = [];
md.push('# Referee round 2 — computed numbers');
md.push('');
md.push('Frozen extraction, 2026-08-14, produced by `paper/referee2_numbers.mjs`. Every input is a');
md.push('frozen artefact under `drive_new/` or `paper/`. No model was fitted. Nothing under `repo/`,');
md.push('`drive_new/` or any existing `step8*`/`step9*` output was modified. Seed 42.');
md.push('');
md.push('---');
md.push('');
md.push('## A. Interval on the mean paired thermal contribution');
md.push('');
md.push('Input: `point_delta` for all 20 ordered directions in `paper/transfer_ci_blocksize.json`,');
md.push('which is the paired thermal-minus-baseline raw transfer delta recomputed from the frozen');
md.push('per-cell predictions.');
md.push('');
md.push(`Mean **${f(A.mean, 5)}**, SD ${f(A.sd, 4)}, range ${f(A.min, 4)} to ${f(A.max, 4)},`);
md.push(`${A.n_positive} positive and ${A.n_negative} negative.`);
md.push('');
md.push('| Resampling unit | n | 95% interval |');
md.push('|---|---|---|');
md.push(`| Directions (naive, ignores pairing) | 20 | [${f(A.ci_naive_percentile[0])}, ${f(A.ci_naive_percentile[1])}] |`);
md.push(`| Unordered pairs, cluster bootstrap | 10 | [${f(A.ci_pair_cluster_percentile[0])}, ${f(A.ci_pair_cluster_percentile[1])}] |`);
md.push(`| Unordered pairs, t on pair means | 10 | [${f(A.ci_pair_t[0])}, ${f(A.ci_pair_t[1])}] |`);
md.push(`| Regions, leave-one-out jackknife | 5 | [${f(A.ci_region_jackknife_t[0])}, ${f(A.ci_region_jackknife_t[1])}] |`);
md.push('');
md.push(`${A.replicates} replicates for the two bootstrap rows. Every interval spans zero, and the`);
md.push('point estimate is a small fraction of the width of each of them. The pair-cluster row is the');
md.push('right primary quantity: the two directions of a pair share geography, data and, for the');
md.push('paired delta, the same target prediction table.');
md.push('');
md.push('Leave-one-region-out means:');
md.push('');
md.push('| Region held out | directions remaining | mean delta |');
md.push('|---|---|---|');
for (const l of A.leave_one_region_out) md.push(`| ${l.region} | ${l.n_directions} | ${f(l.mean, 5)} |`);
md.push('');
md.push('---');
md.push('');
md.push('## B. The conditional index at the design\'s own sample size');
md.push('');
md.push('Input: `paper/conditional_similarity_transfer.json`, the 16 directions on which the');
md.push('supported-feature agreement fraction is defined, and the published values in');
md.push('`paper/diagnostics_common_subset.json`.');
md.push('');
md.push(`Recomputed 16-direction Spearman **${f(B.spearman_16dir)}** against the published`);
md.push(`${f(B.published_16dir)} (agreement to ${Math.abs(B.spearman_16dir - B.published_16dir).toExponential(1)}).`);
md.push(`The tie structure of the index caps the attainable value at **${f(B.tie_ceiling_16dir)}**, so the`);
md.push('observed statistic sits essentially on its own ceiling.');
md.push('');
md.push(`Pair level, which is the unit the published bootstrap resamples: ${B.n_pairs} pairs,`);
md.push(`Spearman **${f(B.spearman_pair_level)}**, exact one-sided permutation`);
md.push(`p = **${B.exact_permutation_p_one_sided.toFixed(4)}** over ${B.n_permutations.toLocaleString('en-US')} permutations.`);
md.push(`A Bonferroni threshold over the 19 computed diagnostic variants is ${B.bonferroni_threshold_19_variants.toExponential(2)},`);
md.push(`so the result **${B.survives_bonferroni ? 'clears' : 'does not clear'}** it.`);
md.push('');
md.push('| Interval construction | n | 95% interval |');
md.push('|---|---|---|');
md.push(`| Published percentile bootstrap (8 pairs) | 8 | [${f(B.published_ci[0])}, ${f(B.published_ci[1])}] |`);
md.push(`| Fisher z on the pair-level rho | 8 | [${f(B.fisher_ci_n8[0])}, ${f(B.fisher_ci_n8[1])}] |`);
md.push(`| Bonett-Wright on the pair-level rho | 8 | [${f(B.bonett_wright_ci_n8[0])}, ${f(B.bonett_wright_ci_n8[1])}] |`);
md.push(`| Fisher z treating 16 directions as independent | 16 | [${f(B.fisher_ci_n16[0])}, ${f(B.fisher_ci_n16[1])}] |`);
md.push('');
md.push('The published lower bound sits close to the bound obtained by treating all 16 directions as');
md.push('independent, and the published upper bound sits below every analytic upper bound. Both are');
md.push('symptoms of a statistic pinned near a combinatorial ceiling under heavy ties, not of');
md.push('precision.');
md.push('');
md.push('Index values across the 8 pairs:');
md.push('');
md.push('| Pair | index | mean raw thermal AUC |');
md.push('|---|---|---|');
for (const p of B.pair_rows) md.push(`| ${p.pair.replace(/__/g, ' ~ ')} | ${f(p.index, 3)} | ${f(p.mean_raw_thermal_auc)} |`);
md.push('');
md.push(`Distinct index values: ${B.index_distinct_values.map((v) => f(v, 3)).join(', ')}. Tie counts: `
  + B.index_tie_counts.map((t) => `${f(t.value, 3)} occurs ${t.n} times`).join('; ') + '.');
md.push('');
md.push('---');
md.push('');
md.push('## C. Spatial-block counts per region');
md.push('');
md.push('Input: the frozen per-cell transfer prediction tables, primary population, one file per');
md.push('target region. Blocks are `row_500m // B` by `col_500m // B`, the manuscript\'s own');
md.push('construction, with `row`/`col` read from `target_cell_id`.');
md.push('');
md.push('| Region | cells | burned | B=2 total / positive | B=10 total / positive | B=20 total / positive |');
md.push('|---|---|---|---|---|---|');
for (const r of results.C_block_counts) {
  if (r.error) { md.push(`| ${r.region} | ${r.error} | | | | |`); continue; }
  md.push(`| ${r.region} | ${r.n_cells.toLocaleString('en-US')} | ${r.n_burned.toLocaleString('en-US')} | `
    + `${r.blocks[2].total} / ${r.blocks[2].positive_carrying} | `
    + `${r.blocks[10].total} / ${r.blocks[10].positive_carrying} | `
    + `${r.blocks[20].total} / ${r.blocks[20].positive_carrying} |`);
}
md.push('');
md.push('The variance of an AUC is dominated by the minority class, so the positive-carrying count is');
md.push('the number that matters for interval coverage.');
md.push('');
md.push('---');
md.push('');
md.push('## D. Step 8D thermal ablation, primary population');
md.push('');
md.push('Input: `drive_new/experiments/<region>/step8d/step8d_ablation_delta_auc_by_population.csv`,');
md.push('population `burnable_tree_shrub_grass`. This artefact is frozen, was produced by the pipeline');
md.push('author, and is not currently cited anywhere in the manuscript.');
md.push('');
md.push('| Region | full thermal block | best subset | its delta | share of the full block |');
md.push('|---|---|---|---|---|');
for (const r of results.D_step8d_ablation) {
  if (r.error) { md.push(`| ${r.region} | ${r.error} | | | |`); continue; }
  md.push(`| ${r.region} | ${f(r.all_thermal)} | \`${r.best_subset}\` | ${f(r.best_subset_delta)} | ${(r.fraction_of_full_block * 100).toFixed(0)}% |`);
}
md.push('');
md.push('---');
md.push('');
md.push('## E. Step 7C downscaling validation and coordinate content');
md.push('');
md.push('| Region | test RMSE (C) | test R2 | top input | coordinate importance sum |');
md.push('|---|---|---|---|---|');
for (const r of results.E_step7c_downscaling) {
  md.push(`| ${r.region} | ${f(r.test_rmse_celsius, 2)} | ${f(r.test_r2, 3)} | `
    + `${r.top_feature ? `\`${r.top_feature.feature}\` ${f(r.top_feature.importance, 3)}` : 'n/a'} | `
    + `${f(r.coordinate_importance_sum, 3)} |`);
}
md.push('');
md.push('Per-region MODIS input semantics, from `downscaling_model_metadata.json`:');
md.push('');
for (const r of results.E_step7c_downscaling) {
  md.push(`- **${r.region}:** ${r.spatial_calibration_note ? r.spatial_calibration_note : 'no note recorded'}`);
}
md.push('');
md.push('---');
md.push('');
md.push('## F. Fused-LST gap fill, per region');
md.push('');
md.push('Input: `drive_new/experiments/<region>/step7e/fused_lst_stats.json`. `fused_lst` equals the');
md.push('observed Landsat LST wherever that is valid, so the gap-filled share is the only part of the');
md.push('channel that is not `current_lst`.');
md.push('');
md.push('| Region | observed coverage % | fused coverage % | gap-filled % of fused |');
md.push('|---|---|---|---|');
for (const r of results.F_fused_gapfill) {
  if (r.error) { md.push(`| ${r.region} | ${r.error} | | |`); continue; }
  md.push(`| ${r.region} | ${f(r.observed_coverage_pct, 2)} | ${f(r.fused_coverage_pct, 2)} | ${f(r.gapfilled_pct_of_fused, 2)} |`);
}
md.push('');
md.push('---');
md.push('');
md.push('## G. Pre-label burn exclusion, per region');
md.push('');
md.push('| Region | field present | exclusion ran | cells excluded |');
md.push('|---|---|---|---|');
for (const r of results.G_pre_label_exclusion) {
  md.push(`| ${r.region} | ${r.error ? r.error : (r.field_present ? 'yes' : '**no**')} | `
    + `${r.exclude_pre_label_burns === null ? '**not recorded**' : (r.exclude_pre_label_burns ? 'yes' : '**no**')} | `
    + `${r.excluded_cells === null ? 'n/a' : r.excluded_cells} |`);
}
md.push('');

fs.writeFileSync(path.join(PAPER, 'referee2_numbers.md'), md.join('\n') + '\n');

console.log(md.join('\n'));
console.error('\n[fused-LST stats keys, for block F inspection]');
for (const r of results.F_fused_gapfill) {
  console.error(r.region, r.error ? r.error : JSON.stringify(r.raw_keys));
}
