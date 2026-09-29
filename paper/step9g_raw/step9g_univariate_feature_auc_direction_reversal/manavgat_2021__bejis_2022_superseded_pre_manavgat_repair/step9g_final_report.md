# Step9G Univariate Feature-AUC Direction-Reversal -- Final Report

- analysis_id: `87d4ec94021fed17446ce5e7870d4222154a131ce830535339a4f0d01c0c6ba7`
- primary population: burnable_tree_shrub_grass
- protected frozen inputs/references: unchanged

| feature | manavgat_auc | manavgat_ci | manavgat_direction | bejis_auc | bejis_ci | bejis_direction | direction_reversal_status | step9_diagnostic_concordance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ndvi_mean | 0.6359 | [0.5872, 0.6763] | higher_values_rank_burned | 0.5588 | [0.4972, 0.6193] | higher_values_rank_burned | no_direction_reversal | False |
| elevation_mean | 0.3741 | [0.2891, 0.4712] | lower_values_rank_burned | 0.6433 | [0.5583, 0.7290] | higher_values_rank_burned | bootstrap_supported_direction_reversal | True |
| slope_mean | 0.5310 | [0.4228, 0.6417] | higher_values_rank_burned | 0.5208 | [0.4393, 0.6053] | higher_values_rank_burned | no_direction_reversal | False |
| lst_anomaly_mean | 0.4824 | [0.4280, 0.5299] | lower_values_rank_burned | 0.4180 | [0.3638, 0.4796] | lower_values_rank_burned | no_direction_reversal | False |
| current_lst_mean | 0.5383 | [0.4518, 0.6205] | higher_values_rank_burned | 0.4767 | [0.4012, 0.5475] | lower_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| current_tvdi_mean | 0.5520 | [0.4602, 0.6411] | higher_values_rank_burned | 0.5173 | [0.4290, 0.5952] | higher_values_rank_burned | no_direction_reversal | False |
| tvdi_difference_mean | 0.4494 | [0.3905, 0.5052] | lower_values_rank_burned | 0.5125 | [0.4432, 0.5829] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| downscaled_lst_mean | 0.5521 | [0.4660, 0.6372] | higher_values_rank_burned | 0.4836 | [0.4004, 0.5598] | lower_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| fused_lst_mean | 0.5401 | [0.4543, 0.6219] | higher_values_rank_burned | 0.4806 | [0.4039, 0.5514] | lower_values_rank_burned | point_direction_reversal_interval_uncertain | True |

## Which features reverse direction between Manavgat and Bejis?
['elevation_mean', 'current_lst_mean', 'tvdi_difference_mean', 'downscaled_lst_mean', 'fused_lst_mean']

## Which reversals are bootstrap-supported?
['elevation_mean']

## Which features retain the same direction?
['ndvi_mean', 'slope_mean', 'lst_anomaly_mean', 'current_tvdi_mean']

## Point reversals with uncertain intervals
['current_lst_mean', 'tvdi_difference_mean', 'downscaled_lst_mean', 'fused_lst_mean']

## Claim boundary

Raw cross-region transfer was below chance; unsupervised adaptation recovered part of the discrimination loss; a large gap to within-region performance remained. Feature-level univariate AUC direction reversals indicate that marginal feature-label relationships are not stable across regions, a pattern consistent with residual concept/relationship shift. This does NOT prove causality and does NOT establish that concept shift is the only source of transfer failure; AUC below 0.5 is a direction, not poor performance, and is never inverted.

## Report revision (report schema v2, report-only)

- report_schema_version: `step9g.univariate_feature_auc_direction_reversal.report.v2`
- regenerated_at: 2026-07-23T08:27:40.563056+00:00
- numerical_results_unchanged: True

Corrects two report-layer semantic defects without recomputing any numerical result. (1) integrated_interpretation previously repeated one identical generic sentence for every feature row regardless of reversal_status; it is now generated per row from reversal_status. (2) thermal_features_consistent_with_step9e previously could include elevation_mean (a baseline, not thermal, feature); it is now restricted to the frozen thermal-feature set (lst_anomaly_mean, current_lst_mean, current_tvdi_mean, tvdi_difference_mean, downscaled_lst_mean, fused_lst_mean). A new general features_consistent_with_step9e field lists any feature (thermal or baseline) whose Step9G point-direction-reversal flag agrees with the Step9E relationship-direction diagnostic. AUC, CI, bootstrap draws, direction labels, support_status, and reversal_status are unchanged (numerical_results_unchanged=true); analysis_id is preserved verbatim.

- features_consistent_with_step9e: ['elevation_mean', 'current_lst_mean', 'tvdi_difference_mean', 'downscaled_lst_mean', 'fused_lst_mean']
- thermal_features_consistent_with_step9e: ['current_lst_mean', 'tvdi_difference_mean', 'downscaled_lst_mean', 'fused_lst_mean']
