# Referee round: verified numbers

Frozen extraction, 2026-08-13. Every value below was read from a file under `drive_new/` or
`paper/`, and the source path plus column name is given with each block. No number here was
computed by a new model run. Nothing under `repo/`, `drive_new/` or any existing `step8*` and
`step9*` output was modified. Two later agents cite this file when editing the manuscript.

Regions and their identifiers: Manavgat 2021 (`manavgat_2021`), Bejís 2022 (`bejis_2022`),
Muğla 2021 (`mugla_2021`), North Evia 2021 extended (`evia_2021_extended`, shown as "Evia"),
Montiferru 2021 (`montiferru_2021`). All numbers are for the primary population, natural vegetation
(`burnable_tree_shrub_grass` with `valid_for_modeling == True`).

---

## 1. Area of applicability per direction (12 directed pairs, four-region subset)

**Source file (single):**

```
drive_new/diagnostics/marginal_aoa_completion/4f3ac830327d7ec6f581abbb5161686710894a68db9d2a59b9b4948d166d033f/comparison/marginal_diagnostics_with_transfer.csv
```

Columns used, by header name: `direction`, `fraction_inside_weighted_aoa`,
`unweighted_fraction_target_cells_inside_support`, `target_mean_dissimilarity`,
`target_p95_dissimilarity`, `raw_thermal_roc_auc`, `raw_thermal_pr_auc`.

The file holds 12 data rows and 21 columns. Column 5, `primary_selection`, is a quoted JSON
string that contains commas, so the file must be read with a quote-aware parser. Splitting on
commas shifts every column after it. The values below were parsed with a quote-aware reader and
selected by header name, not by position.

Sanity checks passed. Manavgat to Muğla gives a weighted AoA fraction of 0.8752 with a raw
thermal ROC-AUC of 0.4702. Muğla to Bejís gives 0.0050 with 0.5832.

**Table A1. Area of applicability and raw thermal transfer, 12 directions.** Weighted AoA =
`fraction_inside_weighted_aoa`. Unweighted support = `unweighted_fraction_target_cells_inside_support`.
Mean and p95 dissimilarity = `target_mean_dissimilarity` and `target_p95_dissimilarity`.

| Direction | Weighted AoA | Unweighted support | Mean dissim. | p95 dissim. | Raw thermal ROC-AUC | Raw thermal PR-AUC |
|---|---|---|---|---|---|---|
| Manavgat to Bejís | 0.1976 | 0.9156 | 0.2787 | 0.4574 | 0.3964 | 0.0542 |
| Manavgat to Muğla | 0.8758 | 0.9640 | 0.1378 | 0.2347 | 0.4377 | 0.0595 |
| Manavgat to Evia | 0.7349 | 0.9425 | 0.1643 | 0.2923 | 0.6540 | 0.4065 |
| Bejís to Manavgat | 0.2207 | 0.7486 | 0.3651 | 0.6871 | 0.3142 | 0.0978 |
| Bejís to Muğla | 0.1998 | 0.7638 | 0.3199 | 0.4933 | 0.6185 | 0.0925 |
| Bejís to Evia | 0.1705 | 0.6534 | 0.3378 | 0.5257 | 0.3828 | 0.2258 |
| Muğla to Manavgat | 0.5305 | 0.9702 | 0.2322 | 0.5502 | 0.3450 | 0.1007 |
| Muğla to Bejís | 0.0050 | 0.9076 | 0.4663 | 0.8550 | 0.5832 | 0.0883 |
| Muğla to Evia | 0.5810 | 0.9510 | 0.2013 | 0.4326 | 0.6534 | 0.3788 |
| Evia to Manavgat | 0.4067 | 0.8995 | 0.3495 | 0.7555 | 0.6769 | 0.3209 |
| Evia to Bejís | 0.0729 | 0.8562 | 0.4863 | 0.8844 | 0.4480 | 0.0592 |
| Evia to Muğla | 0.6310 | 0.9590 | 0.2469 | 0.5116 | 0.5768 | 0.0856 |

Range of the weighted AoA fraction: 0.0050 (Muğla to Bejís) to 0.8752 (Manavgat to Muğla).
Range of the unweighted support fraction: 0.6534 (Bejís to Evia) to 0.9702 (Muğla to Manavgat).

Points that matter for the referee round.

- The Manavgat and Muğla pair is the strongest available counterexample to applicability
  screening. Manavgat to Muğla sits at 0.8752 weighted AoA and 0.9640 unweighted support, the
  highest weighted value in the table, and still transfers below chance at 0.4702. The reverse
  direction sits at 0.5305 weighted and 0.9702 unweighted, the highest unweighted value in the
  table, and transfers at 0.4010. Both directions of the pair are below chance.
- The two quantities disagree sharply. Muğla to Bejís has almost no weighted applicability
  (0.0050) yet transfers above chance at 0.5832. Seven of the other eleven directions in this
  table transfer worse than it does.
- Unweighted support is high everywhere (0.65 to 0.97) while weighted AoA spans nearly the whole
  unit interval. Any claim about applicability must say which of the two is meant.
- The four-region subset excludes Montiferru. The eight missing directions are listed in
  Section 2 below.

Cross-check. For all 12 directions the `raw_thermal_roc_auc` and `raw_thermal_pr_auc` values in
this file agree with the multi-AOI synthesis matrix of Section 2 to within 5.6e-17 (ROC-AUC) and
8.3e-17 (PR-AUC). The two files are consistent.

---

## 2. PR-AUC for the full transfer matrix (20 directed pairs)

**Answer: yes, PR-AUC exists for all 20 directions, for all three transfer states, for both
model families, with bootstrap intervals. Nothing is missing.**

**Source file (single, preferred):**

```
drive_new/diagnostics/multi_aoi_transfer_synthesis/bejis_2022__evia_2021_extended__manavgat_2021__montiferru_2021__mugla_2021/multi_aoi_transfer_matrix.csv
```

120 data rows = 20 directions x 2 model families (`model_family`: `baseline`, `thermal`) x 3
transfer states (`adaptation_method`: `raw_source_only`, `regionwise_zscore`,
`coral_after_regionwise_zscore`). `primary_population` is `burnable_tree_shrub_grass` on every
row. Columns used: `source_experiment_id`, `target_experiment_id`, `model_family`,
`adaptation_method`, `pr_auc`, `pr_auc_ci_low`, `pr_auc_ci_high`, `roc_auc`, `target_row_count`,
`target_burned_count`.

The per-pair files carry the same values and can be used for spot checks:
`drive_new/cross_region/<pair>/step9b/cross_region_transfer_metrics.json` for the raw state
(`results[].thermal_metrics.pr_auc` and `.baseline_metrics.pr_auc`), and
`drive_new/cross_region/<pair>/step10/step10_metrics.json` for all three states
(`point_metrics.<direction>.<state>.<family>.pr_auc`). Ten pair folders each hold both
directions, which is how 20 directions come from 10 folders. Use `step10/`, not
`step10_superseded_pre_manavgat_repair/`.

**Table A2. Thermal PR-AUC, all 20 directions, three transfer states.** Column `pr_auc` with
`pr_auc_ci_low` and `pr_auc_ci_high`. No-skill = the target region prevalence of Table A4.

| Direction | No-skill | Raw | z-score | CORAL |
|---|---|---|---|---|
| Manavgat to Bejís | 0.072 | 0.054 [0.048, 0.061] | 0.060 [0.053, 0.067] | 0.062 [0.054, 0.070] |
| Manavgat to Muğla | 0.070 | 0.060 [0.055, 0.065] | 0.057 [0.053, 0.062] | 0.057 [0.053, 0.062] |
| Manavgat to Evia | 0.287 | 0.407 [0.376, 0.439] | 0.320 [0.292, 0.349] | 0.303 [0.278, 0.330] |
| Manavgat to Montiferru | 0.212 | 0.243 [0.205, 0.292] | 0.209 [0.177, 0.246] | 0.203 [0.172, 0.240] |
| Bejís to Manavgat | 0.143 | 0.098 [0.090, 0.105] | 0.102 [0.094, 0.111] | 0.116 [0.107, 0.125] |
| Bejís to Muğla | 0.070 | 0.093 [0.085, 0.102] | 0.069 [0.064, 0.075] | 0.069 [0.064, 0.075] |
| Bejís to Evia | 0.287 | 0.226 [0.209, 0.243] | 0.291 [0.270, 0.313] | 0.275 [0.256, 0.296] |
| Bejís to Montiferru | 0.212 | 0.289 [0.236, 0.349] | 0.254 [0.208, 0.310] | 0.297 [0.241, 0.357] |
| Muğla to Manavgat | 0.143 | 0.101 [0.094, 0.108] | 0.135 [0.125, 0.146] | 0.134 [0.123, 0.145] |
| Muğla to Bejís | 0.072 | 0.088 [0.077, 0.102] | 0.072 [0.064, 0.082] | 0.078 [0.069, 0.089] |
| Muğla to Evia | 0.287 | 0.379 [0.350, 0.409] | 0.293 [0.273, 0.315] | 0.294 [0.274, 0.316] |
| Muğla to Montiferru | 0.212 | 0.214 [0.182, 0.250] | 0.276 [0.226, 0.330] | 0.274 [0.229, 0.327] |
| Evia to Manavgat | 0.143 | 0.321 [0.295, 0.351] | 0.111 [0.102, 0.119] | 0.114 [0.105, 0.122] |
| Evia to Bejís | 0.072 | 0.059 [0.053, 0.067] | 0.077 [0.067, 0.087] | 0.075 [0.066, 0.084] |
| Evia to Muğla | 0.070 | 0.086 [0.078, 0.093] | 0.066 [0.061, 0.072] | 0.072 [0.066, 0.078] |
| Evia to Montiferru | 0.212 | 0.283 [0.239, 0.331] | 0.236 [0.201, 0.277] | 0.238 [0.202, 0.279] |
| Montiferru to Manavgat | 0.143 | 0.113 [0.104, 0.122] | 0.119 [0.109, 0.130] | 0.125 [0.115, 0.136] |
| Montiferru to Bejís | 0.072 | 0.093 [0.077, 0.115] | 0.082 [0.072, 0.093] | 0.080 [0.071, 0.092] |
| Montiferru to Muğla | 0.070 | 0.089 [0.082, 0.096] | 0.080 [0.074, 0.087] | 0.085 [0.077, 0.094] |
| Montiferru to Evia | 0.287 | 0.317 [0.293, 0.341] | 0.330 [0.308, 0.355] | 0.326 [0.303, 0.350] |

**Table A3. Baseline (static) PR-AUC, all 20 directions, three transfer states.** Same columns,
`model_family` = `baseline`.

| Direction | No-skill | Raw | z-score | CORAL |
|---|---|---|---|---|
| Manavgat to Bejís | 0.072 | 0.052 [0.046, 0.059] | 0.053 [0.047, 0.060] | 0.053 [0.047, 0.060] |
| Manavgat to Muğla | 0.070 | 0.065 [0.060, 0.071] | 0.061 [0.056, 0.066] | 0.064 [0.059, 0.069] |
| Manavgat to Evia | 0.287 | 0.368 [0.342, 0.396] | 0.307 [0.283, 0.333] | 0.324 [0.298, 0.352] |
| Manavgat to Montiferru | 0.212 | 0.225 [0.191, 0.265] | 0.214 [0.181, 0.251] | 0.208 [0.175, 0.244] |
| Bejís to Manavgat | 0.143 | 0.096 [0.089, 0.104] | 0.096 [0.089, 0.104] | 0.098 [0.090, 0.105] |
| Bejís to Muğla | 0.070 | 0.094 [0.085, 0.104] | 0.082 [0.075, 0.090] | 0.084 [0.076, 0.092] |
| Bejís to Evia | 0.287 | 0.282 [0.262, 0.304] | 0.328 [0.303, 0.353] | 0.336 [0.311, 0.361] |
| Bejís to Montiferru | 0.212 | 0.227 [0.191, 0.268] | 0.239 [0.197, 0.289] | 0.247 [0.204, 0.297] |
| Muğla to Manavgat | 0.143 | 0.114 [0.105, 0.122] | 0.144 [0.133, 0.157] | 0.144 [0.133, 0.156] |
| Muğla to Bejís | 0.072 | 0.064 [0.056, 0.074] | 0.085 [0.074, 0.097] | 0.096 [0.083, 0.110] |
| Muğla to Evia | 0.287 | 0.344 [0.318, 0.372] | 0.289 [0.269, 0.311] | 0.297 [0.276, 0.320] |
| Muğla to Montiferru | 0.212 | 0.283 [0.234, 0.338] | 0.370 [0.308, 0.434] | 0.343 [0.280, 0.406] |
| Evia to Manavgat | 0.143 | 0.292 [0.269, 0.318] | 0.149 [0.139, 0.160] | 0.144 [0.133, 0.155] |
| Evia to Bejís | 0.072 | 0.054 [0.048, 0.061] | 0.069 [0.060, 0.081] | 0.070 [0.061, 0.082] |
| Evia to Muğla | 0.070 | 0.082 [0.074, 0.091] | 0.067 [0.061, 0.073] | 0.069 [0.064, 0.075] |
| Evia to Montiferru | 0.212 | 0.258 [0.216, 0.303] | 0.225 [0.191, 0.262] | 0.231 [0.197, 0.270] |
| Montiferru to Manavgat | 0.143 | 0.101 [0.094, 0.110] | 0.146 [0.133, 0.160] | 0.166 [0.152, 0.180] |
| Montiferru to Bejís | 0.072 | 0.114 [0.094, 0.140] | 0.084 [0.074, 0.095] | 0.082 [0.072, 0.093] |
| Montiferru to Muğla | 0.070 | 0.124 [0.112, 0.139] | 0.141 [0.125, 0.161] | 0.127 [0.114, 0.143] |
| Montiferru to Evia | 0.287 | 0.296 [0.275, 0.318] | 0.311 [0.289, 0.334] | 0.294 [0.274, 0.316] |

Read against the no-skill line, raw thermal PR-AUC has an interval entirely above target
prevalence in 11 of 20 directions, entirely below in 7, and straddling it in 2.
The absolute PR-AUC values are small in most directions because prevalence is low. PR-AUC must
never be read without its no-skill line, which changes by a factor of about 7.5 across targets.

### Target prevalence in the primary population

**Source (preferred):** `target_row_count` and `target_burned_count` in the multi-AOI matrix
above, which are identical on every row for a given target. **Confirmed independently** against
`drive_new/experiments/<region>/step8a/step8a_dataset_stats.json`.

**Table A4. Prevalence of burned cells in the modelled natural-vegetation population.**

| Target region | Cells | Burned | Prevalence (no-skill PR-AUC) |
|---|---|---|---|
| Manavgat | 20511 | 2935 | 0.1431 |
| Bejís | 15190 | 1100 | 0.0724 |
| Muğla | 41730 | 2911 | 0.0698 |
| Evia | 9298 | 2664 | 0.2865 |
| Montiferru | 2544 | 539 | 0.2119 |

**This disagrees with Table R1 of `paper/04_results.md` for three regions.** Table R1 reports
the columns "TSG cells" and "Burned in TSG" as 20,555 / 784 (Manavgat), 15,190 / 1,100 (Bejís),
41,772 / 2,952 (Muğla), 9,309 / 2,675 (Evia), 2,591 / 582 (Montiferru). Those come from the
Step 8A fields `burnable_tree_shrub_grass_count` and
`burned_count_within_each_burnable_mask.burnable_tree_shrub_grass`, which are counted over all
grid rows including rows with `valid_for_modeling == False`. Montiferru's own Step 8A file says
so in a field named `burnable_count_population_semantics`:

> LEGACY field: counted over ALL grid rows, including valid_for_modeling == False. Retained
> unchanged for backward compatibility. Do NOT report it as the modeling population.

> canonical_downstream_population: burnable_tree_shrub_grass AND valid_for_modeling == True
> -- this is what Step8B/Step9/Step10 and the multi-AOI synthesis actually consume

**Table A5. Table R1 legacy counts against the modelled population.** Legacy from
`burnable_tree_shrub_grass_count` and `burned_count_within_each_burnable_mask`; modelled from
`burnable_tree_shrub_grass_count_valid_for_modeling` (recorded only for Montiferru) and
`burned_count_within_primary_burnable_mask`, confirmed by `target_row_count` and
`target_burned_count` in the multi-AOI matrix.

| Region | Table R1 cells | Modelled cells | Table R1 burned | Modelled burned | Table R1 prevalence | Modelled prevalence |
|---|---|---|---|---|---|---|
| Manavgat | 20555 | 20511 | 784 | 2935 | 0.038 | 0.1431 |
| Bejís | 15190 | 15190 | 1100 | 1100 | 0.072 | 0.0724 |
| Muğla | 41772 | 41730 | 2952 | 2911 | 0.071 | 0.0698 |
| Evia | 9309 | 9298 | 2675 | 2664 | 0.287 | 0.2865 |
| Montiferru | 2591 | 2544 | 582 | 539 | 0.225 | 0.2119 |

Manavgat and Bejís agree on burned counts. Muğla, Evia and Montiferru do not. Montiferru is the
largest error: Table R1 gives 582 burned of 2,591 (0.225) where the modelled population is 539 of
2,544 (0.212). Every model result in the paper for these regions was fitted and scored on the
modelled counts, so Table R1 misdescribes the population that produced them. The fix is to Table
R1, not to any result.

### Directions covered by the area-of-applicability file

The AoA file of Section 1 covers 12 of these 20 directions. The eight it does not cover all
involve Montiferru:

- Manavgat to Montiferru (`manavgat_2021_to_montiferru_2021`)
- Bejís to Montiferru (`bejis_2022_to_montiferru_2021`)
- Muğla to Montiferru (`mugla_2021_to_montiferru_2021`)
- Evia to Montiferru (`evia_2021_extended_to_montiferru_2021`)
- Montiferru to Manavgat (`montiferru_2021_to_manavgat_2021`)
- Montiferru to Bejís (`montiferru_2021_to_bejis_2022`)
- Montiferru to Muğla (`montiferru_2021_to_mugla_2021`)
- Montiferru to Evia (`montiferru_2021_to_evia_2021_extended`)

No area-of-applicability output was found for Montiferru in any direction. Any statement about
applicability must be scoped to the four-region subset.

---

## 3. Baseline (static) transfer summary

**Source file (single):**

```
paper/baseline_vs_thermal_transfer.csv
```

20 rows, one per direction. Columns used: `baseline_roc`, `baseline_ci_low`, `baseline_ci_high`,
`thermal_roc`, `thermal_ci_low`, `thermal_ci_high`, `delta_roc`. That file is itself a read-only
extraction from frozen `drive_new/cross_region/<pair>/step9b` points and `step9c` target
spatial-block bootstrap intervals, primary population, 1000 replicates, seed 42, as recorded in
`paper/baseline_vs_thermal.mjs` and `paper/baseline_vs_thermal_transfer.json`.

Raw transfer, no adaptation. Chance is 0.5.

**Table A6. Raw transfer ROC-AUC summary over the 20 directions.**

| Quantity | Baseline (static) | Thermal |
|---|---|---|
| Mean ROC-AUC | 0.5194 | 0.5267 |
| Minimum | 0.2966 (Bejís to Manavgat) | 0.3142 (Bejís to Manavgat) |
| Maximum | 0.7274 (Evia to Manavgat) | 0.6769 (Evia to Manavgat) |
| Directions below 0.5 at the point estimate | 7 of 20 | 7 of 20 |
| Directions with the CI entirely below 0.5 | 7 of 20 | 7 of 20 |
| Directions with the CI entirely above 0.5 | 11 of 20 | 11 of 20 |
| Directions with the CI crossing 0.5 | 2 of 20 | 2 of 20 |

**Mean thermal minus baseline delta: +0.00733**, which rounds to +0.004 as reported in
Section 4.3. This is the mean of the `delta_roc` column. Each row of that column is the paired
difference computed on identical resampled target blocks, not a difference of two independent
estimates. It agrees with the difference of the two column means (0.52672 minus
0.51938 = 0.00733).

For both models the point-estimate count and the CI-entirely-below count are the same number.
Every direction that is below chance at the point estimate is below chance with its whole
interval. No direction is ambiguously below chance.

Baseline below chance with the whole interval (4 directions):

- Manavgat to Bejís: 0.3707 [0.349, 0.394]
- Manavgat to Muğla: 0.4656 [0.445, 0.483]
- Bejís to Manavgat: 0.2966 [0.279, 0.315]
- Muğla to Manavgat: 0.4223 [0.408, 0.438]
- Muğla to Bejís: 0.4507 [0.427, 0.477]
- Evia to Bejís: 0.3917 [0.368, 0.414]
- Montiferru to Manavgat: 0.3379 [0.319, 0.357]

Thermal below chance with the whole interval (6 directions):

- Manavgat to Bejís: 0.3964 [0.372, 0.423]
- Manavgat to Muğla: 0.4377 [0.419, 0.455]
- Bejís to Manavgat: 0.3142 [0.298, 0.331]
- Bejís to Evia: 0.3828 [0.364, 0.403]
- Muğla to Manavgat: 0.3450 [0.332, 0.359]
- Evia to Bejís: 0.4480 [0.427, 0.469]
- Montiferru to Manavgat: 0.4041 [0.385, 0.423]

Paired delta support, from the `delta_interpretation` column:
positive in 12 directions,
negative in 7,
uncertain in 1.
This matches the counts already in `paper/04_results.md` Section 4.3 (10 positive, 7 negative, 3
uncertain) and the stated mean of +0.004.

---

## 4. What this supports and what it does not

1. Supports Section 5.3. The Manavgat and Muğla counterexample now has its literal AoA number.
   Manavgat to Muğla is at 0.875 weighted AoA and 0.964 unweighted support and still transfers at
   0.470; the reverse is at 0.531 and 0.970 and transfers at 0.401.
2. Closes a flagged gap. `paper/05_discussion.md` line 538 says the literal AoA-inside number for
   that pair "must come from Emrehan's AoA table [TO VERIFY]". It is verified here.
3. Supports Section 4.3. The mean paired delta is +0.0042 and the support counts are 10 positive,
   7 negative and 3 uncertain, exactly as written.
4. Supports Section 4.3 line 119. The six below-chance thermal directions named there are the six
   found here, and two thermal intervals span 0.5, as stated. The matching baseline figures (4
   below chance, 12 above, 4 spanning) are new and appear nowhere in Section 4.
5. Contradiction found, Table R1. Its TSG cell and burned counts are the Step 8A legacy fields,
   counted before the `valid_for_modeling` filter. Muğla, Evia and Montiferru are wrong against
   the population every model actually used. Montiferru is worst: 582 of 2,591 reported against
   539 of 2,544 modelled. Montiferru TSG prevalence should read 0.212, not 0.225.
6. Does not support any general AoA claim. The AoA file covers 12 of 20 directions and has
   nothing for Montiferru. Statements must be scoped to the four-region subset.
7. Does not support "low applicability predicts poor transfer". Muğla to Bejís has the lowest
   weighted AoA in the table (0.005) and transfers above chance (0.583). This is consistent with
   the null AoA ordering already reported in Table 6.
8. Nothing else here contradicts Sections 4.3, 4.4 or 5.3.

---

## Source files, in full

| Block | Path |
|---|---|
| Section 1 | `drive_new/diagnostics/marginal_aoa_completion/4f3ac830327d7ec6f581abbb5161686710894a68db9d2a59b9b4948d166d033f/comparison/marginal_diagnostics_with_transfer.csv` |
| Section 2, matrix | `drive_new/diagnostics/multi_aoi_transfer_synthesis/bejis_2022__evia_2021_extended__manavgat_2021__montiferru_2021__mugla_2021/multi_aoi_transfer_matrix.csv` |
| Section 2, per-pair raw | `drive_new/cross_region/<pair>/step9b/cross_region_transfer_metrics.json` |
| Section 2, per-pair adapted | `drive_new/cross_region/<pair>/step10/step10_metrics.json` |
| Section 2, prevalence | `drive_new/experiments/<region>/step8a/step8a_dataset_stats.json` |
| Section 3 | `paper/baseline_vs_thermal_transfer.csv` |
| Section 4 cross-reference | `paper/04_results.md`, `paper/05_discussion.md` |

Machine-readable companion: `paper/referee_round_numbers.csv`. Both files are regenerated by
`node paper/referee_round_numbers.mjs`, which reads only the sources listed above and writes only
these two files.
