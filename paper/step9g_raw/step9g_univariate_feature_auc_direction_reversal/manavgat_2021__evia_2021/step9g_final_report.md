# Step9G Univariate Feature-AUC Direction-Reversal -- Final Report

- analysis_id: `6fdbfe2103bcd532af89059ccebee5fa1434683c60897a8cbc37a40bafc168f4`
- source: `manavgat_2021`
- target: `evia_2021`
- primary population: burnable_tree_shrub_grass
- protected frozen inputs/references: unchanged

| feature | manavgat_2021_auc | manavgat_2021_ci | manavgat_2021_direction | evia_2021_auc | evia_2021_ci | evia_2021_direction | direction_reversal_status | step9_diagnostic_concordance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ndvi_mean | 0.6359 | [0.5872, 0.6763] | higher_values_rank_burned | 0.5310 | [0.3985, 0.6710] | higher_values_rank_burned | no_direction_reversal | False |
| elevation_mean | 0.3741 | [0.2891, 0.4712] | lower_values_rank_burned | 0.6472 | [0.4982, 0.7861] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| slope_mean | 0.5310 | [0.4228, 0.6417] | higher_values_rank_burned | 0.5207 | [0.4008, 0.6504] | higher_values_rank_burned | no_direction_reversal | False |
| lst_anomaly_mean | 0.4824 | [0.4280, 0.5299] | lower_values_rank_burned | 0.5487 | [0.4583, 0.6382] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| current_lst_mean | 0.5383 | [0.4518, 0.6205] | higher_values_rank_burned | 0.4158 | [0.2766, 0.5450] | lower_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| current_tvdi_mean | 0.5520 | [0.4602, 0.6411] | higher_values_rank_burned | 0.3752 | [0.2495, 0.4990] | lower_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| tvdi_difference_mean | 0.4494 | [0.3905, 0.5052] | lower_values_rank_burned | 0.5211 | [0.4376, 0.6040] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| downscaled_lst_mean | 0.5521 | [0.4660, 0.6372] | higher_values_rank_burned | 0.4152 | [0.2723, 0.5535] | lower_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| fused_lst_mean | 0.5401 | [0.4543, 0.6219] | higher_values_rank_burned | 0.4141 | [0.2759, 0.5439] | lower_values_rank_burned | point_direction_reversal_interval_uncertain | True |

## Which features reverse direction between manavgat_2021 and evia_2021?
['elevation_mean', 'lst_anomaly_mean', 'current_lst_mean', 'current_tvdi_mean', 'tvdi_difference_mean', 'downscaled_lst_mean', 'fused_lst_mean']

## Which reversals are bootstrap-supported?
none

## Which features retain the same direction?
['ndvi_mean', 'slope_mean']

## Point reversals with uncertain intervals
['elevation_mean', 'lst_anomaly_mean', 'current_lst_mean', 'current_tvdi_mean', 'tvdi_difference_mean', 'downscaled_lst_mean', 'fused_lst_mean']

## Claim boundary

Feature-level univariate AUC direction reversals indicate that marginal feature-label relationships are not stable across the selected regions, a pattern consistent with concept/relationship shift. Target labels are used only for this diagnostic evaluation. This does NOT prove causality or establish concept shift as the only transfer-failure mechanism; AUC below 0.5 is a direction and is never inverted.

## Report revision (report schema v2, report-only)

- report_schema_version: `step9g.univariate_feature_auc_direction_reversal.report.v2`
- regenerated_at: 2026-07-23T08:27:49.962875+00:00
- numerical_results_unchanged: True

Corrects two report-layer semantic defects without recomputing any numerical result. (1) integrated_interpretation previously repeated one identical generic sentence for every feature row regardless of reversal_status; it is now generated per row from reversal_status. (2) thermal_features_consistent_with_step9e previously could include elevation_mean (a baseline, not thermal, feature); it is now restricted to the frozen thermal-feature set (lst_anomaly_mean, current_lst_mean, current_tvdi_mean, tvdi_difference_mean, downscaled_lst_mean, fused_lst_mean). A new general features_consistent_with_step9e field lists any feature (thermal or baseline) whose Step9G point-direction-reversal flag agrees with the Step9E relationship-direction diagnostic. AUC, CI, bootstrap draws, direction labels, support_status, and reversal_status are unchanged (numerical_results_unchanged=true); analysis_id is preserved verbatim.

- features_consistent_with_step9e: ['elevation_mean', 'lst_anomaly_mean', 'current_lst_mean', 'current_tvdi_mean', 'tvdi_difference_mean', 'downscaled_lst_mean', 'fused_lst_mean']
- thermal_features_consistent_with_step9e: ['lst_anomaly_mean', 'current_lst_mean', 'current_tvdi_mean', 'tvdi_difference_mean', 'downscaled_lst_mean', 'fused_lst_mean']
