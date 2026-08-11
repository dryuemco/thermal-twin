# Step9G Univariate Feature-AUC Direction-Reversal -- Final Report

- analysis_id: `166bc656dd9abf35e463437b77bb3d146f8c079178b0c8a744282dd2e8244c28`
- source: `manavgat_2021`
- target: `evia_2021_extended`
- primary population: burnable_tree_shrub_grass
- protected frozen inputs/references: unchanged

| feature | manavgat_2021_auc | manavgat_2021_ci | manavgat_2021_direction | evia_2021_extended_auc | evia_2021_extended_ci | evia_2021_extended_direction | direction_reversal_status | step9_diagnostic_concordance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ndvi_mean | 0.6359 | [0.5872, 0.6763] | higher_values_rank_burned | 0.6391 | [0.5749, 0.7006] | higher_values_rank_burned | no_direction_reversal | False |
| elevation_mean | 0.3741 | [0.2891, 0.4712] | lower_values_rank_burned | 0.5406 | [0.4484, 0.6261] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| slope_mean | 0.5310 | [0.4228, 0.6417] | higher_values_rank_burned | 0.4865 | [0.4177, 0.5540] | lower_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| lst_anomaly_mean | 0.4824 | [0.4280, 0.5299] | lower_values_rank_burned | 0.6401 | [0.5671, 0.7102] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| current_lst_mean | 0.5383 | [0.4518, 0.6205] | higher_values_rank_burned | 0.3765 | [0.3013, 0.4559] | lower_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| current_tvdi_mean | 0.5520 | [0.4602, 0.6411] | higher_values_rank_burned | 0.3619 | [0.2852, 0.4422] | lower_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| tvdi_difference_mean | 0.4494 | [0.3905, 0.5052] | lower_values_rank_burned | 0.5191 | [0.4444, 0.5889] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| downscaled_lst_mean | 0.5521 | [0.4660, 0.6372] | higher_values_rank_burned | 0.3765 | [0.2969, 0.4593] | lower_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| fused_lst_mean | 0.5401 | [0.4543, 0.6219] | higher_values_rank_burned | 0.3757 | [0.3002, 0.4556] | lower_values_rank_burned | point_direction_reversal_interval_uncertain | True |

## Which features reverse direction between manavgat_2021 and evia_2021_extended?
['elevation_mean', 'slope_mean', 'lst_anomaly_mean', 'current_lst_mean', 'current_tvdi_mean', 'tvdi_difference_mean', 'downscaled_lst_mean', 'fused_lst_mean']

## Which reversals are bootstrap-supported?
none

## Which features retain the same direction?
['ndvi_mean']

## Point reversals with uncertain intervals
['elevation_mean', 'slope_mean', 'lst_anomaly_mean', 'current_lst_mean', 'current_tvdi_mean', 'tvdi_difference_mean', 'downscaled_lst_mean', 'fused_lst_mean']

## Claim boundary

Feature-level univariate AUC direction reversals indicate that marginal feature-label relationships are not stable across the selected regions, a pattern consistent with concept/relationship shift. Target labels are used only for this diagnostic evaluation. This does NOT prove causality or establish concept shift as the only transfer-failure mechanism; AUC below 0.5 is a direction and is never inverted.
