// Windows-side data extractor for Figures 3-6 (WSL cannot resolve the drive_new
// symlink, so all drive_new reads happen here). Output: paper/figures/data/fig_data.json
// with a sha256 for every source file read.
import { createHash } from 'crypto';
import { mkdirSync, readFileSync, writeFileSync } from 'fs';

const ROOT = process.env.R3ROOT; if (!ROOT) throw new Error('R3ROOT unset'); // ROUND3: was 'C:/Users/CORSAIR/projects/thermal-twin'
const REGIONS = ['manavgat_2021', 'bejis_2022', 'mugla_2021', 'evia_2021_extended', 'montiferru_2021'];
const POP = 'burnable_tree_shrub_grass';
const sources = {};
function read(pathRel) {
  const buf = readFileSync(`${ROOT}/${pathRel}`);
  sources[pathRel] = createHash('sha256').update(buf).digest('hex');
  return buf.toString('utf8');
}
const readJson = p => JSON.parse(read(p));

// ---------- fig 3/4: within-region + block robustness ----------
const ROBUST_PATHS = {
  manavgat_2021: b => [`drive_new/experiments/manavgat_2021/robustness/step8_big_blocks_v2/block_${b}_cells/step8b_metrics.json`,
                       `drive_new/experiments/manavgat_2021/robustness/step8_big_blocks_v2/block_${b}_cells/bootstrap_summary.json`],
  bejis_2022: b => [`drive_new/robustness/step8_large_block/manavgat_2021__bejis_2022/bejis_2022/block_${b}_cells/step8b_large_block_metrics.json`,
                    `drive_new/robustness/step8_large_block/manavgat_2021__bejis_2022/bejis_2022/block_${b}_cells/step8c_large_block_bootstrap_summary.json`],
  mugla_2021: b => [`drive_new/experiments/mugla_2021/robustness/step8_big_blocks/block_${b}_cells/step8b_metrics.json`,
                    `drive_new/experiments/mugla_2021/robustness/step8_big_blocks/block_${b}_cells/bootstrap_summary.json`],
  evia_2021_extended: b => [`drive_new/experiments/evia_2021_extended/robustness/step8_big_blocks/block_${b}_cells/step8b_metrics.json`,
                            `drive_new/experiments/evia_2021_extended/robustness/step8_big_blocks/block_${b}_cells/bootstrap_summary.json`],
  montiferru_2021: b => [`drive_new/experiments/montiferru_2021/robustness/step8_big_blocks/block_${b}_cells/step8b_metrics.json`,
                         `drive_new/experiments/montiferru_2021/robustness/step8_big_blocks/block_${b}_cells/bootstrap_summary.json`],
};
const fig34 = {};
for (const reg of REGIONS) {
  const s8c = readJson(`drive_new/experiments/${reg}/step8c/step8c_bootstrap_metrics.json`);
  const p = s8c.overall_point_estimates_from_predictions[POP];
  const ci = s8c.bootstrap_ci_by_population[POP].delta_auc;
  const blocks = { 2: { baseline: p.auc_baseline, thermal: p.auc_thermal, delta: p.delta_auc, delta_ci: [ci.p2_5, ci.p97_5] } };
  for (const b of [10, 20]) {
    const [mPath, bPath] = ROBUST_PATHS[reg](b);
    const m = readJson(mPath);
    const bt = readJson(bPath);
    if (m.primary_population && m.primary_population !== POP) throw new Error(`pop mismatch ${mPath}`);
    blocks[b] = { baseline: m.baseline_roc_auc, thermal: m.thermal_roc_auc, delta: m.delta_roc_auc,
                  delta_ci: [bt.series.delta_auc.ci_2_5, bt.series.delta_auc.ci_97_5] };
  }
  fig34[reg] = blocks;
}

// ---------- fig 5: 20-direction raw/z/CORAL thermal transfer ----------
const pairFolders = ['manavgat_2021__bejis_2022', 'manavgat_2021__mugla_2021', 'manavgat_2021__evia_2021_extended',
  'montiferru_2021__manavgat_2021', 'montiferru_2021__bejis_2022', 'montiferru_2021__mugla_2021',
  'montiferru_2021__evia_2021_extended', 'bejis_2022__mugla_2021', 'bejis_2022__evia_2021_extended',
  'mugla_2021__evia_2021_extended'];
const fig5 = {};
for (const folder of pairFolders) {
  const m = readJson(`drive_new/cross_region/${folder}/step10/step10_metrics.json`);
  for (const [dir, variants] of Object.entries(m.point_metrics)) {
    fig5[dir] = {
      raw: variants.raw_source_only.thermal.roc_auc,
      zscore: variants.regionwise_zscore.thermal.roc_auc,
      coral: variants.coral_after_regionwise_zscore.thermal.roc_auc,
      within_target: variants.within.thermal.roc_auc,
    };
  }
}

// ---------- fig 6a: four-AOI decomposition (thermal, roc_auc) ----------
const csv = read('drive_new/diagnostics/four_aoi_transfer_decomposition/bejis_2022__evia_2021_extended__manavgat_2021__mugla_2021/four_aoi_decomposition.csv');
const [hdr, ...rows] = csv.trim().split('\n');
const cols = hdr.split(',');
const idx = Object.fromEntries(cols.map((c, i) => [c, i]));
const decompByDir = {};
for (const line of rows) {
  const v = line.split(',');
  if (v[idx.model_family] !== 'thermal' || v[idx.metric] !== 'roc_auc') continue;
  const dir = v[idx.direction];
  decompByDir[dir] = decompByDir[dir] || { direction: dir, within: +v[idx.within_target_auc], raw: +v[idx.raw_auc], methods: {} };
  decompByDir[dir].methods[v[idx.adaptation_method]] = {
    adapted: +v[idx.adapted_auc],
    recovered_fraction: +v[idx.recovered_fraction],
    recovered_ci: [+v[idx.recovered_fraction_ci_low], +v[idx.recovered_fraction_ci_high]],
    status: v[idx.recovery_status],
  };
}
const fig6_decomp = Object.values(decompByDir).map(d => {
  const best = d.methods.regionwise_zscore.adapted >= d.methods.coral_after_regionwise_zscore.adapted
    ? ['regionwise_zscore', d.methods.regionwise_zscore]
    : ['coral_after_regionwise_zscore', d.methods.coral_after_regionwise_zscore];
  return { direction: d.direction, within: d.within, raw: d.raw,
           best_method: best[0], best_adapted: best[1].adapted,
           recovered_fraction: best[1].recovered_fraction, recovered_ci: best[1].recovered_ci,
           status: best[1].status };
});

// ---------- fig 6b/6c from frozen paper outputs ----------
const loro = JSON.parse(read('paper/loro_pooled_transfer.json'));
const fdrop = JSON.parse(read('paper/feature_drop_transfer.json'));
const fig6_loro = loro.per_target.map(t => ({
  target: t.target, best_pairwise: t.best_pairwise_thermal, mean_pairwise: t.mean_pairwise_thermal,
  loro_raw: t.loro_raw_thermal.roc_auc, loro_raw_ci: t.loro_raw_thermal.roc_auc_ci,
  loro_z: t.loro_z_thermal.roc_auc, within: t.within_thermal,
}));
const fig6_fdrop = Object.entries(fdrop.tradeoff).map(([cfg, v]) => ({
  config: cfg, mean_within: v.mean_within_auc, mean_transfer: v.mean_transfer_auc,
  dirs_ci_above: v.n_dirs_ci_above_chance,
}));

mkdirSync(`${ROOT}/paper/figures/data`, { recursive: true });
writeFileSync(`${ROOT}/paper/figures/data/fig_data.json`, JSON.stringify({
  meta: { created: '2026-08-08', extractor: 'paper/figures/extract_fig_data.mjs',
          population: POP, sources },
  fig34, fig5, fig6_decomp, fig6_loro, fig6_fdrop,
}, null, 1));
console.log(`written fig_data.json; ${Object.keys(sources).length} source files hashed`);
console.log('fig5 directions:', Object.keys(fig5).length, '| decomp rows:', fig6_decomp.length);
