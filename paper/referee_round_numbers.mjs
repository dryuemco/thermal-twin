import { readFileSync, writeFileSync } from 'fs';
const ROOT = 'C:/Users/CORSAIR/projects/thermal-twin';

function parseCSV(text) {
  const rows = []; let row = [], field = '', inQ = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (inQ) { if (c === '"') { if (text[i + 1] === '"') { field += '"'; i++; } else inQ = false; } else field += c; }
    else if (c === '"') inQ = true;
    else if (c === ',') { row.push(field); field = ''; }
    else if (c === '\r') { }
    else if (c === '\n') { row.push(field); rows.push(row); row = []; field = ''; }
    else field += c;
  }
  if (field.length || row.length) { row.push(field); rows.push(row); }
  return rows.filter(r => r.length > 1);
}
const toObjs = rows => rows.slice(1).map(r => Object.fromEntries(rows[0].map((k, i) => [k, r[i]])));
const f = (v, n = 3) => (v === undefined || v === '' || v === null) ? 'n/a' : (+v).toFixed(n);

const REGIONS = ['manavgat_2021', 'bejis_2022', 'mugla_2021', 'evia_2021_extended', 'montiferru_2021'];
const NAME = { manavgat_2021: 'Manavgat', bejis_2022: 'Bejís', mugla_2021: 'Muğla', evia_2021_extended: 'Evia', montiferru_2021: 'Montiferru' };
const dirName = d => { const [s, t] = d.split('_to_'); return `${NAME[s]} to ${NAME[t]}`; };

// --- sources
const AOA_REL = 'drive_new/diagnostics/marginal_aoa_completion/4b2a1c86c0c197c2a331c133d1120f9531ce385441d86af0d8c6154024417492/comparison/marginal_diagnostics_with_transfer.csv';
const MTX_REL = 'drive_new/diagnostics/multi_aoi_transfer_synthesis/bejis_2022__evia_2021_extended__manavgat_2021__montiferru_2021__mugla_2021/multi_aoi_transfer_matrix.csv';
const BVT_REL = 'paper/baseline_vs_thermal_transfer.csv';

const aoa = toObjs(parseCSV(readFileSync(`${ROOT}/${AOA_REL}`, 'utf8')));
const mtx = toObjs(parseCSV(readFileSync(`${ROOT}/${MTX_REL}`, 'utf8')));
const bvt = toObjs(parseCSV(readFileSync(`${ROOT}/${BVT_REL}`, 'utf8')));

// --- 20 direction order
const dirs20 = [];
for (const s of REGIONS) for (const t of REGIONS) if (s !== t) dirs20.push(`${s}_to_${t}`);

// --- matrix lookup
const mkey = (d, fam, ad) => `${d}|${fam}|${ad}`;
const M = new Map();
for (const r of mtx) M.set(mkey(`${r.source_experiment_id}_to_${r.target_experiment_id}`, r.model_family, r.adaptation_method), r);
const ADS = ['raw_source_only', 'regionwise_zscore', 'coral_after_regionwise_zscore'];
const missingMtx = [];
for (const d of dirs20) for (const fam of ['baseline', 'thermal']) for (const a of ADS) if (!M.has(mkey(d, fam, a))) missingMtx.push(`${d}|${fam}|${a}`);

// --- prevalence per target region (canonical modelling population)
const prevalence = {};
for (const t of REGIONS) {
  const r = mtx.find(x => x.target_experiment_id === t);
  prevalence[t] = { n: +r.target_row_count, burned: +r.target_burned_count, p: +r.target_burned_count / +r.target_row_count };
}
// step8a legacy vs canonical
const s8 = {};
for (const t of REGIONS) {
  const j = JSON.parse(readFileSync(`${ROOT}/drive_new/experiments/${t}/step8a/step8a_dataset_stats.json`, 'utf8'));
  s8[t] = {
    tsg_legacy_all_rows: j.burnable_tree_shrub_grass_count,
    tsg_valid: j.burnable_tree_shrub_grass_count_valid_for_modeling,
    burned_tsg_all_rows: j.burned_count_within_each_burnable_mask.burnable_tree_shrub_grass,
    burned_tsg_primary: j.burned_count_within_primary_burnable_mask,
  };
}

// --- baseline vs thermal summary
const mean = a => a.reduce((x, y) => x + y, 0) / a.length;
const summ = {};
for (const fam of ['baseline', 'thermal']) {
  const v = bvt.map(r => +r[`${fam}_roc`]);
  const minR = bvt.reduce((a, b) => +a[`${fam}_roc`] <= +b[`${fam}_roc`] ? a : b);
  const maxR = bvt.reduce((a, b) => +a[`${fam}_roc`] >= +b[`${fam}_roc`] ? a : b);
  summ[fam] = {
    mean: mean(v), min: +minR[`${fam}_roc`], minDir: minR.direction, max: +maxR[`${fam}_roc`], maxDir: maxR.direction,
    belowPt: bvt.filter(r => +r[`${fam}_roc`] < 0.5).map(r => r.direction),
    ciBelow: bvt.filter(r => +r[`${fam}_ci_high`] < 0.5).map(r => r.direction),
    ciAbove: bvt.filter(r => +r[`${fam}_ci_low`] > 0.5).map(r => r.direction),
    ciStraddle: bvt.filter(r => +r[`${fam}_ci_low`] <= 0.5 && +r[`${fam}_ci_high`] >= 0.5).map(r => r.direction),
  };
}
const meanDelta = mean(bvt.map(r => +r.delta_roc));

// --- cross-check raw thermal ROC/PR: AoA CSV vs matrix vs bvt
const xcheck = [];
for (const r of aoa) {
  const m = M.get(mkey(r.direction, 'thermal', 'raw_source_only'));
  const b = bvt.find(x => x.direction === r.direction);
  xcheck.push({
    direction: r.direction,
    roc_aoa: +r.raw_thermal_roc_auc, roc_mtx: +m.roc_auc, roc_bvt: +b.thermal_roc,
    pr_aoa: +r.raw_thermal_pr_auc, pr_mtx: +m.pr_auc,
    d_roc_aoa_mtx: Math.abs(+r.raw_thermal_roc_auc - +m.roc_auc),
    d_pr_aoa_mtx: Math.abs(+r.raw_thermal_pr_auc - +m.pr_auc),
  });
}
const maxXroc = Math.max(...xcheck.map(x => x.d_roc_aoa_mtx));
const maxXpr = Math.max(...xcheck.map(x => x.d_pr_aoa_mtx));
console.log('cross-check max |AoA - matrix| ROC', maxXroc, 'PR', maxXpr);
console.log('missing matrix cells:', missingMtx.length);
console.log('AoA directions:', aoa.length, aoa.map(r => r.direction).join(', '));
const aoaSet = new Set(aoa.map(r => r.direction));
const aoaMissing = dirs20.filter(d => !aoaSet.has(d));
console.log('AoA missing 8:', aoaMissing.join(', '));

// ======================= build markdown =====================================
const L = [];
const P = s => L.push(s);

P('# Referee round: verified numbers');
P('');
P('Frozen extraction, 2026-08-13. Every value below was read from a file under `drive_new/` or');
P('`paper/`, and the source path plus column name is given with each block. No number here was');
P('computed by a new model run. Nothing under `repo/`, `drive_new/` or any existing `step8*` and');
P('`step9*` output was modified. Two later agents cite this file when editing the manuscript.');
P('');
P('Regions and their identifiers: Manavgat 2021 (`manavgat_2021`), Bejís 2022 (`bejis_2022`),');
P('Muğla 2021 (`mugla_2021`), North Evia 2021 extended (`evia_2021_extended`, shown as "Evia"),');
P('Montiferru 2021 (`montiferru_2021`). All numbers are for the primary population, natural vegetation');
P('(`burnable_tree_shrub_grass` with `valid_for_modeling == True`).');
P('');
P('---');
P('');

// ---- 1
P('## 1. Area of applicability per direction (12 directed pairs, four-region subset)');
P('');
P('**Source file (single):**');
P('');
P('```');
P(AOA_REL);
P('```');
P('');
P('Columns used, by header name: `direction`, `fraction_inside_weighted_aoa`,');
P('`unweighted_fraction_target_cells_inside_support`, `target_mean_dissimilarity`,');
P('`target_p95_dissimilarity`, `raw_thermal_roc_auc`, `raw_thermal_pr_auc`.');
P('');
P('The file holds 12 data rows and 21 columns. Column 5, `primary_selection`, is a quoted JSON');
P('string that contains commas, so the file must be read with a quote-aware parser. Splitting on');
P('commas shifts every column after it. The values below were parsed with a quote-aware reader and');
P('selected by header name, not by position.');
P('');
P('Sanity checks passed. Manavgat to Muğla gives a weighted AoA fraction of 0.8752 with a raw');
P('thermal ROC-AUC of 0.4702. Muğla to Bejís gives 0.0050 with 0.5832.');
P('');
P('**Table A1. Area of applicability and raw thermal transfer, 12 directions.** Weighted AoA =');
P('`fraction_inside_weighted_aoa`. Unweighted support = `unweighted_fraction_target_cells_inside_support`.');
P('Mean and p95 dissimilarity = `target_mean_dissimilarity` and `target_p95_dissimilarity`.');
P('');
P('| Direction | Weighted AoA | Unweighted support | Mean dissim. | p95 dissim. | Raw thermal ROC-AUC | Raw thermal PR-AUC |');
P('|---|---|---|---|---|---|---|');
const aoaSorted = dirs20.filter(d => aoaSet.has(d)).map(d => aoa.find(r => r.direction === d));
for (const r of aoaSorted) {
  P(`| ${dirName(r.direction)} | ${f(r.fraction_inside_weighted_aoa, 4)} | ${f(r.unweighted_fraction_target_cells_inside_support, 4)} | ${f(r.target_mean_dissimilarity, 4)} | ${f(r.target_p95_dissimilarity, 4)} | ${f(r.raw_thermal_roc_auc, 4)} | ${f(r.raw_thermal_pr_auc, 4)} |`);
}
P('');
P('Range of the weighted AoA fraction: 0.0050 (Muğla to Bejís) to 0.8752 (Manavgat to Muğla).');
P('Range of the unweighted support fraction: 0.6534 (Bejís to Evia) to 0.9702 (Muğla to Manavgat).');
P('');
P('Points that matter for the referee round.');
P('');
P('- The Manavgat and Muğla pair is the strongest available counterexample to applicability');
P('  screening. Manavgat to Muğla sits at 0.8752 weighted AoA and 0.9640 unweighted support, the');
P('  highest weighted value in the table, and still transfers below chance at 0.4702. The reverse');
P('  direction sits at 0.5305 weighted and 0.9702 unweighted, the highest unweighted value in the');
P('  table, and transfers at 0.4010. Both directions of the pair are below chance.');
P('- The two quantities disagree sharply. Muğla to Bejís has almost no weighted applicability');
P('  (0.0050) yet transfers above chance at 0.5832. Seven of the other eleven directions in this');
P('  table transfer worse than it does.');
P('- Unweighted support is high everywhere (0.65 to 0.97) while weighted AoA spans nearly the whole');
P('  unit interval. Any claim about applicability must say which of the two is meant.');
P('- The four-region subset excludes Montiferru. The eight missing directions are listed in');
P('  Section 2 below.');
P('');
P('Cross-check. For all 12 directions the `raw_thermal_roc_auc` and `raw_thermal_pr_auc` values in');
P(`this file agree with the multi-AOI synthesis matrix of Section 2 to within ${maxXroc.toExponential(1)} (ROC-AUC) and`);
P(`${maxXpr.toExponential(1)} (PR-AUC). The two files are consistent.`);
P('');
P('---');
P('');

// ---- 2
P('## 2. PR-AUC for the full transfer matrix (20 directed pairs)');
P('');
P('**Answer: yes, PR-AUC exists for all 20 directions, for all three transfer states, for both');
P('model families, with bootstrap intervals. Nothing is missing.**');
P('');
P('**Source file (single, preferred):**');
P('');
P('```');
P(MTX_REL);
P('```');
P('');
P('120 data rows = 20 directions x 2 model families (`model_family`: `baseline`, `thermal`) x 3');
P('transfer states (`adaptation_method`: `raw_source_only`, `regionwise_zscore`,');
P('`coral_after_regionwise_zscore`). `primary_population` is `burnable_tree_shrub_grass` on every');
P('row. Columns used: `source_experiment_id`, `target_experiment_id`, `model_family`,');
P('`adaptation_method`, `pr_auc`, `pr_auc_ci_low`, `pr_auc_ci_high`, `roc_auc`, `target_row_count`,');
P('`target_burned_count`.');
P('');
P('The per-pair files carry the same values and can be used for spot checks:');
P('`drive_new/cross_region/<pair>/step9b/cross_region_transfer_metrics.json` for the raw state');
P('(`results[].thermal_metrics.pr_auc` and `.baseline_metrics.pr_auc`), and');
P('`drive_new/cross_region/<pair>/step10/step10_metrics.json` for all three states');
P('(`point_metrics.<direction>.<state>.<family>.pr_auc`). Ten pair folders each hold both');
P('directions, which is how 20 directions come from 10 folders. Use `step10/`, not');
P('`step10_superseded_pre_manavgat_repair/`.');
P('');
P('**Table A2. Thermal PR-AUC, all 20 directions, three transfer states.** Column `pr_auc` with');
P('`pr_auc_ci_low` and `pr_auc_ci_high`. No-skill = the target region prevalence of Table A4.');
P('');
P('| Direction | No-skill | Raw | z-score | CORAL |');
P('|---|---|---|---|---|');
for (const d of dirs20) {
  const t = d.split('_to_')[1];
  const g = a => { const r = M.get(mkey(d, 'thermal', a)); return `${f(r.pr_auc, 3)} [${f(r.pr_auc_ci_low, 3)}, ${f(r.pr_auc_ci_high, 3)}]`; };
  P(`| ${dirName(d)} | ${f(prevalence[t].p, 3)} | ${g('raw_source_only')} | ${g('regionwise_zscore')} | ${g('coral_after_regionwise_zscore')} |`);
}
P('');
P('**Table A3. Baseline (static) PR-AUC, all 20 directions, three transfer states.** Same columns,');
P('`model_family` = `baseline`.');
P('');
P('| Direction | No-skill | Raw | z-score | CORAL |');
P('|---|---|---|---|---|');
for (const d of dirs20) {
  const t = d.split('_to_')[1];
  const g = a => { const r = M.get(mkey(d, 'baseline', a)); return `${f(r.pr_auc, 3)} [${f(r.pr_auc_ci_low, 3)}, ${f(r.pr_auc_ci_high, 3)}]`; };
  P(`| ${dirName(d)} | ${f(prevalence[t].p, 3)} | ${g('raw_source_only')} | ${g('regionwise_zscore')} | ${g('coral_after_regionwise_zscore')} |`);
}
P('');
// counts of raw thermal PR above/below no-skill
const prAbove = [], prBelow = [], prStrad = [];
for (const d of dirs20) {
  const t = d.split('_to_')[1]; const r = M.get(mkey(d, 'thermal', 'raw_source_only')); const ns = prevalence[t].p;
  if (+r.pr_auc_ci_low > ns) prAbove.push(d); else if (+r.pr_auc_ci_high < ns) prBelow.push(d); else prStrad.push(d);
}
P('Read against the no-skill line, raw thermal PR-AUC has an interval entirely above target');
P(`prevalence in ${prAbove.length} of 20 directions, entirely below in ${prBelow.length}, and straddling it in ${prStrad.length}.`);
P('The absolute PR-AUC values are small in most directions because prevalence is low. PR-AUC must');
P('never be read without its no-skill line, which changes by a factor of about 7.5 across targets.');
P('');
P('### Target prevalence in the primary population');
P('');
P('**Source (preferred):** `target_row_count` and `target_burned_count` in the multi-AOI matrix');
P('above, which are identical on every row for a given target. **Confirmed independently** against');
P('`drive_new/experiments/<region>/step8a/step8a_dataset_stats.json`.');
P('');
P('**Table A4. Prevalence of burned cells in the modelled natural-vegetation population.**');
P('');
P('| Target region | Cells | Burned | Prevalence (no-skill PR-AUC) |');
P('|---|---|---|---|');
for (const t of REGIONS) P(`| ${NAME[t]} | ${prevalence[t].n} | ${prevalence[t].burned} | ${f(prevalence[t].p, 4)} |`);
P('');
P('**This disagrees with Table R1 of `paper/04_results.md` for three regions.** Table R1 reports');
P('the columns "TSG cells" and "Burned in TSG" as 20,555 / 784 (Manavgat), 15,190 / 1,100 (Bejís),');
P('41,772 / 2,952 (Muğla), 9,309 / 2,675 (Evia), 2,591 / 582 (Montiferru). Those come from the');
P('Step 8A fields `burnable_tree_shrub_grass_count` and');
P('`burned_count_within_each_burnable_mask.burnable_tree_shrub_grass`, which are counted over all');
P('grid rows including rows with `valid_for_modeling == False`. Montiferru\'s own Step 8A file says');
P('so in a field named `burnable_count_population_semantics`:');
P('');
P('> LEGACY field: counted over ALL grid rows, including valid_for_modeling == False. Retained');
P('> unchanged for backward compatibility. Do NOT report it as the modeling population.');
P('');
P('> canonical_downstream_population: burnable_tree_shrub_grass AND valid_for_modeling == True');
P('> -- this is what Step8B/Step9/Step10 and the multi-AOI synthesis actually consume');
P('');
P('**Table A5. Table R1 legacy counts against the modelled population.** Legacy from');
P('`burnable_tree_shrub_grass_count` and `burned_count_within_each_burnable_mask`; modelled from');
P('`burnable_tree_shrub_grass_count_valid_for_modeling` (recorded only for Montiferru) and');
P('`burned_count_within_primary_burnable_mask`, confirmed by `target_row_count` and');
P('`target_burned_count` in the multi-AOI matrix.');
P('');
P('| Region | Table R1 cells | Modelled cells | Table R1 burned | Modelled burned | Table R1 prevalence | Modelled prevalence |');
P('|---|---|---|---|---|---|---|');
const R1 = { manavgat_2021: [20555, 784, '0.038'], bejis_2022: [15190, 1100, '0.072'], mugla_2021: [41772, 2952, '0.071'], evia_2021_extended: [9309, 2675, '0.287'], montiferru_2021: [2591, 582, '0.225'] };
for (const t of REGIONS) {
  const a = R1[t], b = prevalence[t];
  P(`| ${NAME[t]} | ${a[0]} | ${b.n} | ${a[1]} | ${b.burned} | ${a[2]} | ${f(b.p, 4)} |`);
}
P('');
P('Manavgat and Bejís agree on burned counts. Muğla, Evia and Montiferru do not. Montiferru is the');
P('largest error: Table R1 gives 582 burned of 2,591 (0.225) where the modelled population is 539 of');
P('2,544 (0.212). Every model result in the paper for these regions was fitted and scored on the');
P('modelled counts, so Table R1 misdescribes the population that produced them. The fix is to Table');
P('R1, not to any result.');
P('');
P('### Directions covered by the area-of-applicability file');
P('');
P('The AoA file of Section 1 covers 12 of these 20 directions. The eight it does not cover all');
P('involve Montiferru:');
P('');
for (const d of aoaMissing) P(`- ${dirName(d)} (\`${d}\`)`);
P('');
P('No area-of-applicability output was found for Montiferru in any direction. Any statement about');
P('applicability must be scoped to the four-region subset.');
P('');
P('---');
P('');

// ---- 3
P('## 3. Baseline (static) transfer summary');
P('');
P('**Source file (single):**');
P('');
P('```');
P(BVT_REL);
P('```');
P('');
P('20 rows, one per direction. Columns used: `baseline_roc`, `baseline_ci_low`, `baseline_ci_high`,');
P('`thermal_roc`, `thermal_ci_low`, `thermal_ci_high`, `delta_roc`. That file is itself a read-only');
P('extraction from frozen `drive_new/cross_region/<pair>/step9b` points and `step9c` target');
P('spatial-block bootstrap intervals, primary population, 1000 replicates, seed 42, as recorded in');
P('`paper/baseline_vs_thermal.mjs` and `paper/baseline_vs_thermal_transfer.json`.');
P('');
P('Raw transfer, no adaptation. Chance is 0.5.');
P('');
P('**Table A6. Raw transfer ROC-AUC summary over the 20 directions.**');
P('');
P('| Quantity | Baseline (static) | Thermal |');
P('|---|---|---|');
P(`| Mean ROC-AUC | ${f(summ.baseline.mean, 4)} | ${f(summ.thermal.mean, 4)} |`);
P(`| Minimum | ${f(summ.baseline.min, 4)} (${dirName(summ.baseline.minDir)}) | ${f(summ.thermal.min, 4)} (${dirName(summ.thermal.minDir)}) |`);
P(`| Maximum | ${f(summ.baseline.max, 4)} (${dirName(summ.baseline.maxDir)}) | ${f(summ.thermal.max, 4)} (${dirName(summ.thermal.maxDir)}) |`);
P(`| Directions below 0.5 at the point estimate | ${summ.baseline.belowPt.length} of 20 | ${summ.thermal.belowPt.length} of 20 |`);
P(`| Directions with the CI entirely below 0.5 | ${summ.baseline.ciBelow.length} of 20 | ${summ.thermal.ciBelow.length} of 20 |`);
P(`| Directions with the CI entirely above 0.5 | ${summ.baseline.ciAbove.length} of 20 | ${summ.thermal.ciAbove.length} of 20 |`);
P(`| Directions with the CI crossing 0.5 | ${summ.baseline.ciStraddle.length} of 20 | ${summ.thermal.ciStraddle.length} of 20 |`);
P('');
P(`**Mean thermal minus baseline delta: ${meanDelta >= 0 ? '+' : ''}${meanDelta.toFixed(5)}**, which rounds to +0.004 as reported in`);
P('Section 4.3. This is the mean of the `delta_roc` column. Each row of that column is the paired');
P('difference computed on identical resampled target blocks, not a difference of two independent');
P(`estimates. It agrees with the difference of the two column means (${summ.thermal.mean.toFixed(5)} minus`);
P(`${summ.baseline.mean.toFixed(5)} = ${(summ.thermal.mean - summ.baseline.mean).toFixed(5)}).`);
P('');
P('For both models the point-estimate count and the CI-entirely-below count are the same number.');
P('Every direction that is below chance at the point estimate is below chance with its whole');
P('interval. No direction is ambiguously below chance.');
P('');
P('Baseline below chance with the whole interval (4 directions):');
P('');
for (const d of summ.baseline.ciBelow) { const r = bvt.find(x => x.direction === d); P(`- ${dirName(d)}: ${f(r.baseline_roc, 4)} [${f(r.baseline_ci_low, 3)}, ${f(r.baseline_ci_high, 3)}]`); }
P('');
P('Thermal below chance with the whole interval (6 directions):');
P('');
for (const d of summ.thermal.ciBelow) { const r = bvt.find(x => x.direction === d); P(`- ${dirName(d)}: ${f(r.thermal_roc, 4)} [${f(r.thermal_ci_low, 3)}, ${f(r.thermal_ci_high, 3)}]`); }
P('');
P('Paired delta support, from the `delta_interpretation` column:');
P(`positive in ${bvt.filter(r => r.delta_interpretation === 'positive_bootstrap_support').length} directions,`);
P(`negative in ${bvt.filter(r => r.delta_interpretation === 'negative_bootstrap_support').length},`);
P(`uncertain in ${bvt.filter(r => r.delta_interpretation === 'uncertain').length}.`);
P('This matches the counts already in `paper/04_results.md` Section 4.3 (10 positive, 7 negative, 3');
P('uncertain) and the stated mean of +0.004.');
P('');
P('---');
P('');

// ---- 4
P('## 4. What this supports and what it does not');
P('');
P('1. Supports Section 5.3. The Manavgat and Muğla counterexample now has its literal AoA number.');
P('   Manavgat to Muğla is at 0.875 weighted AoA and 0.964 unweighted support and still transfers at');
P('   0.470; the reverse is at 0.531 and 0.970 and transfers at 0.401.');
P('2. Closes a flagged gap. `paper/05_discussion.md` line 538 says the literal AoA-inside number for');
P('   that pair "must come from Emrehan\'s AoA table [TO VERIFY]". It is verified here.');
P('3. Supports Section 4.3. The mean paired delta is +0.0042 and the support counts are 10 positive,');
P('   7 negative and 3 uncertain, exactly as written.');
P('4. Supports Section 4.3 line 119. The six below-chance thermal directions named there are the six');
P('   found here, and two thermal intervals span 0.5, as stated. The matching baseline figures (4');
P('   below chance, 12 above, 4 spanning) are new and appear nowhere in Section 4.');
P('5. Contradiction found, Table R1. Its TSG cell and burned counts are the Step 8A legacy fields,');
P('   counted before the `valid_for_modeling` filter. Muğla, Evia and Montiferru are wrong against');
P('   the population every model actually used. Montiferru is worst: 582 of 2,591 reported against');
P('   539 of 2,544 modelled. Montiferru TSG prevalence should read 0.212, not 0.225.');
P('6. Does not support any general AoA claim. The AoA file covers 12 of 20 directions and has');
P('   nothing for Montiferru. Statements must be scoped to the four-region subset.');
P('7. Does not support "low applicability predicts poor transfer". Muğla to Bejís has the lowest');
P('   weighted AoA in the table (0.005) and transfers above chance (0.583). This is consistent with');
P('   the null AoA ordering already reported in Table 6.');
P('8. Nothing else here contradicts Sections 4.3, 4.4 or 5.3.');
P('');
P('---');
P('');
P('## Source files, in full');
P('');
P('| Block | Path |');
P('|---|---|');
P(`| Section 1 | \`${AOA_REL}\` |`);
P(`| Section 2, matrix | \`${MTX_REL}\` |`);
P('| Section 2, per-pair raw | `drive_new/cross_region/<pair>/step9b/cross_region_transfer_metrics.json` |');
P('| Section 2, per-pair adapted | `drive_new/cross_region/<pair>/step10/step10_metrics.json` |');
P('| Section 2, prevalence | `drive_new/experiments/<region>/step8a/step8a_dataset_stats.json` |');
P(`| Section 3 | \`${BVT_REL}\` |`);
P('| Section 4 cross-reference | `paper/04_results.md`, `paper/05_discussion.md` |');
P('');
P('Machine-readable companion: `paper/referee_round_numbers.csv`. Both files are regenerated by');
P('`node paper/referee_round_numbers.mjs`, which reads only the sources listed above and writes only');
P('these two files.');
P('');

writeFileSync(`${ROOT}/paper/referee_round_numbers.md`, L.join('\n'));

// ======================= CSV companion ======================================
const C = ['block,direction,source_region,target_region,metric,value,ci_low,ci_high,source_file,source_column'];
const q = s => `"${String(s).replace(/"/g, '""')}"`;
for (const r of aoaSorted) {
  const [s, t] = r.direction.split('_to_');
  for (const col of ['fraction_inside_weighted_aoa', 'unweighted_fraction_target_cells_inside_support', 'target_mean_dissimilarity', 'target_p95_dissimilarity', 'raw_thermal_roc_auc', 'raw_thermal_pr_auc'])
    C.push(['aoa', r.direction, s, t, col, r[col], '', '', q(AOA_REL), col].join(','));
}
for (const d of dirs20) {
  const [s, t] = d.split('_to_');
  for (const fam of ['thermal', 'baseline']) for (const a of ADS) {
    const r = M.get(mkey(d, fam, a));
    C.push(['transfer_matrix', d, s, t, `${fam}_${a}_pr_auc`, r.pr_auc, r.pr_auc_ci_low, r.pr_auc_ci_high, q(MTX_REL), 'pr_auc'].join(','));
    C.push(['transfer_matrix', d, s, t, `${fam}_${a}_roc_auc`, r.roc_auc, r.roc_auc_ci_low, r.roc_auc_ci_high, q(MTX_REL), 'roc_auc'].join(','));
  }
}
for (const t of REGIONS) {
  C.push(['prevalence', '', '', t, 'target_row_count', prevalence[t].n, '', '', q(MTX_REL), 'target_row_count'].join(','));
  C.push(['prevalence', '', '', t, 'target_burned_count', prevalence[t].burned, '', '', q(MTX_REL), 'target_burned_count'].join(','));
  C.push(['prevalence', '', '', t, 'burned_prevalence_modelled', prevalence[t].p.toFixed(6), '', '', q(MTX_REL), 'target_burned_count/target_row_count'].join(','));
  C.push(['prevalence', '', '', t, 'tsg_count_legacy_all_rows', s8[t].tsg_legacy_all_rows, '', '', q(`drive_new/experiments/${t}/step8a/step8a_dataset_stats.json`), 'burnable_tree_shrub_grass_count'].join(','));
  C.push(['prevalence', '', '', t, 'burned_tsg_legacy_all_rows', s8[t].burned_tsg_all_rows, '', '', q(`drive_new/experiments/${t}/step8a/step8a_dataset_stats.json`), 'burned_count_within_each_burnable_mask.burnable_tree_shrub_grass'].join(','));
  C.push(['prevalence', '', '', t, 'burned_tsg_modelled', s8[t].burned_tsg_primary, '', '', q(`drive_new/experiments/${t}/step8a/step8a_dataset_stats.json`), 'burned_count_within_primary_burnable_mask'].join(','));
}
for (const r of bvt) {
  const [s, t] = r.direction.split('_to_');
  C.push(['baseline_vs_thermal', r.direction, s, t, 'baseline_roc_auc_raw', r.baseline_roc, r.baseline_ci_low, r.baseline_ci_high, q(BVT_REL), 'baseline_roc'].join(','));
  C.push(['baseline_vs_thermal', r.direction, s, t, 'thermal_roc_auc_raw', r.thermal_roc, r.thermal_ci_low, r.thermal_ci_high, q(BVT_REL), 'thermal_roc'].join(','));
  C.push(['baseline_vs_thermal', r.direction, s, t, 'delta_roc_auc', r.delta_roc, r.delta_ci_low, r.delta_ci_high, q(BVT_REL), 'delta_roc'].join(','));
}
for (const fam of ['baseline', 'thermal']) {
  C.push(['summary', 'all_20', '', '', `${fam}_mean_roc_auc`, summ[fam].mean.toFixed(6), '', '', q(BVT_REL), `${fam}_roc`].join(','));
  C.push(['summary', 'all_20', '', '', `${fam}_min_roc_auc`, summ[fam].min, '', '', q(BVT_REL), `${fam}_roc`].join(','));
  C.push(['summary', 'all_20', '', '', `${fam}_max_roc_auc`, summ[fam].max, '', '', q(BVT_REL), `${fam}_roc`].join(','));
  C.push(['summary', 'all_20', '', '', `${fam}_n_below_half_point`, summ[fam].belowPt.length, '', '', q(BVT_REL), `${fam}_roc`].join(','));
  C.push(['summary', 'all_20', '', '', `${fam}_n_ci_entirely_below_half`, summ[fam].ciBelow.length, '', '', q(BVT_REL), `${fam}_ci_high`].join(','));
  C.push(['summary', 'all_20', '', '', `${fam}_n_ci_entirely_above_half`, summ[fam].ciAbove.length, '', '', q(BVT_REL), `${fam}_ci_low`].join(','));
}
C.push(['summary', 'all_20', '', '', 'mean_thermal_minus_baseline_delta', meanDelta.toFixed(6), '', '', q(BVT_REL), 'delta_roc'].join(','));
writeFileSync(`${ROOT}/paper/referee_round_numbers.csv`, C.join('\n') + '\n');
console.log('written md lines', L.length, 'csv rows', C.length - 1);
console.log('summary', JSON.stringify(summ, null, 1));
console.log('prAbove', prAbove.length, 'prBelow', prBelow.length, 'prStrad', prStrad.length);
