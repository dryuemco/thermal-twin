# Step9G Univariate Feature-AUC Direction-Reversal -- Final Report

- analysis_id: `4c9a3af9db1748538bec8fe0f79838ed4cc23c978b7a882f419a141aa4644c05`
- source: `mugla_2021`
- target: `manavgat_2021`
- primary population: burnable_tree_shrub_grass
- protected frozen inputs/references: unchanged

| feature | mugla_2021_auc | mugla_2021_ci | mugla_2021_direction | manavgat_2021_auc | manavgat_2021_ci | manavgat_2021_direction | direction_reversal_status | step9_diagnostic_concordance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ndvi_mean | 0.6617 | [0.6156, 0.7035] | higher_values_rank_burned | 0.6359 | [0.5872, 0.6763] | higher_values_rank_burned | no_direction_reversal | False |
| elevation_mean | 0.6114 | [0.5319, 0.6904] | higher_values_rank_burned | 0.3741 | [0.2891, 0.4712] | lower_values_rank_burned | bootstrap_supported_direction_reversal | True |
| slope_mean | 0.6368 | [0.5819, 0.6864] | higher_values_rank_burned | 0.5310 | [0.4228, 0.6417] | higher_values_rank_burned | no_direction_reversal | False |
| lst_anomaly_mean | 0.4846 | [0.3945, 0.5661] | lower_values_rank_burned | 0.4824 | [0.4280, 0.5299] | lower_values_rank_burned | no_direction_reversal | False |
| current_lst_mean | 0.3248 | [0.2714, 0.3821] | lower_values_rank_burned | 0.5383 | [0.4518, 0.6205] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| current_tvdi_mean | 0.3358 | [0.2754, 0.3976] | lower_values_rank_burned | 0.5520 | [0.4602, 0.6411] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| tvdi_difference_mean | 0.4900 | [0.3964, 0.5747] | lower_values_rank_burned | 0.4494 | [0.3905, 0.5052] | lower_values_rank_burned | no_direction_reversal | False |
| downscaled_lst_mean | 0.3070 | [0.2532, 0.3658] | lower_values_rank_burned | 0.5521 | [0.4660, 0.6372] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| fused_lst_mean | 0.3252 | [0.2720, 0.3828] | lower_values_rank_burned | 0.5401 | [0.4543, 0.6219] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |

## Which features reverse direction between mugla_2021 and manavgat_2021?
['elevation_mean', 'current_lst_mean', 'current_tvdi_mean', 'downscaled_lst_mean', 'fused_lst_mean']

## Which reversals are bootstrap-supported?
['elevation_mean']

## Which features retain the same direction?
['ndvi_mean', 'slope_mean', 'lst_anomaly_mean', 'tvdi_difference_mean']

## Point reversals with uncertain intervals
['current_lst_mean', 'current_tvdi_mean', 'downscaled_lst_mean', 'fused_lst_mean']

## Claim boundary

Feature-level univariate AUC direction reversals indicate that marginal feature-label relationships are not stable across the selected regions, a pattern consistent with concept/relationship shift. Target labels are used only for this diagnostic evaluation. This does NOT prove causality or establish concept shift as the only transfer-failure mechanism; AUC below 0.5 is a direction and is never inverted.

## Report revision (report schema v2, report-only)

- report_schema_version: `step9g.univariate_feature_auc_direction_reversal.report.v2`
- regenerated_at: 2026-07-23T08:27:45.313124+00:00
- numerical_results_unchanged: True

Corrects two report-layer semantic defects without recomputing any numerical result. (1) integrated_interpretation previously repeated one identical generic sentence for every feature row regardless of reversal_status; it is now generated per row from reversal_status. (2) thermal_features_consistent_with_step9e previously could include elevation_mean (a baseline, not thermal, feature); it is now restricted to the frozen thermal-feature set (lst_anomaly_mean, current_lst_mean, current_tvdi_mean, tvdi_difference_mean, downscaled_lst_mean, fused_lst_mean). A new general features_consistent_with_step9e field lists any feature (thermal or baseline) whose Step9G point-direction-reversal flag agrees with the Step9E relationship-direction diagnostic. AUC, CI, bootstrap draws, direction labels, support_status, and reversal_status are unchanged (numerical_results_unchanged=true); analysis_id is preserved verbatim.

- features_consistent_with_step9e: ['elevation_mean', 'current_lst_mean', 'current_tvdi_mean', 'downscaled_lst_mean', 'fused_lst_mean']
- thermal_features_consistent_with_step9e: ['current_lst_mean', 'current_tvdi_mean', 'downscaled_lst_mean', 'fused_lst_mean']
