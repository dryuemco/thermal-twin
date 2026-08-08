// POSITIONING §3 table: baseline vs thermal RAW transfer per ordered direction, with the
// paired spatial-block bootstrap delta CI. Read-only extraction from Emrehan's frozen
// step9b (points) + step9c (target-block bootstrap CIs incl. delta_roc_auc). TSG population.
import { readFileSync, writeFileSync } from 'fs';

const ROOT = 'C:/Users/CORSAIR/projects/thermal-twin';
const REGIONS = ['manavgat_2021', 'bejis_2022', 'mugla_2021', 'evia_2021_extended', 'montiferru_2021'];
const POP = 'burnable_tree_shrub_grass';
const pairFolders = ['manavgat_2021__bejis_2022', 'manavgat_2021__mugla_2021', 'manavgat_2021__evia_2021_extended',
  'montiferru_2021__manavgat_2021', 'montiferru_2021__bejis_2022', 'montiferru_2021__mugla_2021',
  'montiferru_2021__evia_2021_extended', 'bejis_2022__mugla_2021', 'bejis_2022__evia_2021_extended',
  'mugla_2021__evia_2021_extended'];

const rows = new Map();
for (const folder of pairFolders) {
  const m = JSON.parse(readFileSync(`${ROOT}/drive_new/cross_region/${folder}/step9b/cross_region_transfer_metrics.json`, 'utf8'));
  const b = JSON.parse(readFileSync(`${ROOT}/drive_new/cross_region/${folder}/step9c/cross_region_bootstrap_metrics.json`, 'utf8'));
  for (const r of m.results) {
    if (r.population !== POP || r.skipped) continue;
    const g = b.groups.find(g => g.transfer_direction === r.transfer_direction && g.population === POP);
    const ci = g.confidence_intervals;
    rows.set(r.transfer_direction, {
      direction: r.transfer_direction,
      baseline_roc: r.baseline_metrics.roc_auc,
      thermal_roc: r.thermal_metrics.roc_auc,
      delta_roc: r.delta_metrics.delta_auc,
      baseline_ci: [ci.baseline_roc_auc.ci_2_5, ci.baseline_roc_auc.ci_97_5],
      thermal_ci: [ci.thermal_roc_auc.ci_2_5, ci.thermal_roc_auc.ci_97_5],
      delta_ci: [ci.delta_roc_auc.ci_2_5, ci.delta_roc_auc.ci_97_5],
      delta_interpretation: ci.delta_roc_auc.interpretation,
      n_replicates: g.n_successful_replicates,
      folder,
    });
  }
}

const ordered = [];
for (const s of REGIONS) for (const t of REGIONS) {
  if (s === t) continue;
  const r = rows.get(`${s}_to_${t}`);
  if (!r) throw new Error(`missing ${s}_to_${t}`);
  ordered.push(r);
}

const pos = ordered.filter(r => r.delta_ci[0] > 0);
const neg = ordered.filter(r => r.delta_ci[1] < 0);
const unc = ordered.filter(r => r.delta_ci[0] <= 0 && r.delta_ci[1] >= 0);
const mean = a => a.reduce((x, y) => x + y, 0) / a.length;
// swing framing: directions where thermal crosses 0.5 relative to baseline
const dragBelow = ordered.filter(r => r.baseline_roc >= 0.5 && r.thermal_roc < 0.5);
const liftAbove = ordered.filter(r => r.baseline_roc < 0.5 && r.thermal_roc >= 0.5);

const meta = {
  created: '2026-08-08',
  purpose: 'POSITIONING §3 direct evidence: per-direction paired baseline-vs-thermal raw transfer contrast. The thermal block is the swing factor: where it gains within-region it can push transfer below chance, and vice versa.',
  population: POP,
  source: 'drive_new/cross_region/<pair>/step9b (points) + step9c (target spatial-block bootstrap, 1000 replicates, seed 42, paired delta = thermal - baseline on identical resampled blocks)',
  no_new_model_runs: true,
  summary: {
    mean_baseline: mean(ordered.map(r => r.baseline_roc)),
    mean_thermal: mean(ordered.map(r => r.thermal_roc)),
    mean_delta: mean(ordered.map(r => r.delta_roc)),
    delta_ci_positive: pos.map(r => r.direction),
    delta_ci_negative: neg.map(r => r.direction),
    delta_ci_uncertain_count: unc.length,
    thermal_drags_below_chance: dragBelow.map(r => r.direction),
    thermal_lifts_above_chance: liftAbove.map(r => r.direction),
  },
};
writeFileSync(`${ROOT}/paper/baseline_vs_thermal_transfer.json`, JSON.stringify({ meta, per_direction: ordered }, null, 1));

const csv = ['direction,baseline_roc,baseline_ci_low,baseline_ci_high,thermal_roc,thermal_ci_low,thermal_ci_high,delta_roc,delta_ci_low,delta_ci_high,delta_interpretation'];
for (const r of ordered) csv.push([r.direction, r.baseline_roc.toFixed(4), r.baseline_ci[0].toFixed(4), r.baseline_ci[1].toFixed(4),
  r.thermal_roc.toFixed(4), r.thermal_ci[0].toFixed(4), r.thermal_ci[1].toFixed(4),
  r.delta_roc.toFixed(4), r.delta_ci[0].toFixed(4), r.delta_ci[1].toFixed(4), r.delta_interpretation].join(','));
writeFileSync(`${ROOT}/paper/baseline_vs_thermal_transfer.csv`, csv.join('\n') + '\n');

for (const r of ordered) console.log(`${r.direction.padEnd(46)} base=${r.baseline_roc.toFixed(4)} thermal=${r.thermal_roc.toFixed(4)} d=${r.delta_roc >= 0 ? '+' : ''}${r.delta_roc.toFixed(4)} [${r.delta_ci[0].toFixed(3)},${r.delta_ci[1].toFixed(3)}] ${r.delta_interpretation}`);
console.log(`\nmeans: base=${meta.summary.mean_baseline.toFixed(4)} thermal=${meta.summary.mean_thermal.toFixed(4)} delta=${meta.summary.mean_delta.toFixed(4)}`);
console.log(`delta CI>0: ${pos.length} [${pos.map(r => r.direction).join(', ')}]`);
console.log(`delta CI<0: ${neg.length} [${neg.map(r => r.direction).join(', ')}]`);
console.log(`uncertain: ${unc.length}`);
console.log(`thermal drags below 0.5: ${dragBelow.map(r => r.direction).join(', ') || 'none'}`);
console.log(`thermal lifts above 0.5: ${liftAbove.map(r => r.direction).join(', ') || 'none'}`);
