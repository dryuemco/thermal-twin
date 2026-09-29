# Step9G Univariate Feature-AUC Direction-Reversal -- Final Report

- analysis_id: `b5327245715711ef86904c5af42976644c3d31203563a34a71e0e6c06fa17a9a`
- source: `mugla_2021`
- target: `evia_2021`
- primary population: burnable_tree_shrub_grass
- protected frozen inputs/references: unchanged

| feature | mugla_2021_auc | mugla_2021_ci | mugla_2021_direction | evia_2021_auc | evia_2021_ci | evia_2021_direction | direction_reversal_status | step9_diagnostic_concordance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ndvi_mean | 0.6617 | [0.6156, 0.7035] | higher_values_rank_burned | 0.5310 | [0.3985, 0.6710] | higher_values_rank_burned | no_direction_reversal | False |
| elevation_mean | 0.6114 | [0.5319, 0.6904] | higher_values_rank_burned | 0.6472 | [0.4982, 0.7861] | higher_values_rank_burned | no_direction_reversal | False |
| slope_mean | 0.6368 | [0.5819, 0.6864] | higher_values_rank_burned | 0.5207 | [0.4008, 0.6504] | higher_values_rank_burned | no_direction_reversal | False |
| lst_anomaly_mean | 0.4846 | [0.3945, 0.5661] | lower_values_rank_burned | 0.5487 | [0.4583, 0.6382] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| current_lst_mean | 0.3248 | [0.2714, 0.3821] | lower_values_rank_burned | 0.4158 | [0.2766, 0.5450] | lower_values_rank_burned | no_direction_reversal | False |
| current_tvdi_mean | 0.3358 | [0.2754, 0.3976] | lower_values_rank_burned | 0.3752 | [0.2495, 0.4990] | lower_values_rank_burned | no_direction_reversal | False |
| tvdi_difference_mean | 0.4900 | [0.3964, 0.5747] | lower_values_rank_burned | 0.5211 | [0.4376, 0.6040] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| downscaled_lst_mean | 0.3070 | [0.2532, 0.3658] | lower_values_rank_burned | 0.4152 | [0.2723, 0.5535] | lower_values_rank_burned | no_direction_reversal | False |
| fused_lst_mean | 0.3252 | [0.2720, 0.3828] | lower_values_rank_burned | 0.4141 | [0.2759, 0.5439] | lower_values_rank_burned | no_direction_reversal | False |

## Which features reverse direction between mugla_2021 and evia_2021?
['lst_anomaly_mean', 'tvdi_difference_mean']

## Which reversals are bootstrap-supported?
none

## Which features retain the same direction?
['ndvi_mean', 'elevation_mean', 'slope_mean', 'current_lst_mean', 'current_tvdi_mean', 'downscaled_lst_mean', 'fused_lst_mean']

## Point reversals with uncertain intervals
['lst_anomaly_mean', 'tvdi_difference_mean']

## Claim boundary

Feature-level univariate AUC direction reversals indicate that marginal feature-label relationships are not stable across the selected regions, a pattern consistent with concept/relationship shift. Target labels are used only for this diagnostic evaluation. This does NOT prove causality or establish concept shift as the only transfer-failure mechanism; AUC below 0.5 is a direction and is never inverted.
