# Step9G Univariate Feature-AUC Direction-Reversal -- Final Report

- analysis_id: `a2fb005b47a3cdd0153ae2db263e578a60d8869d2e00337c9f9220bc14968a47`
- source: `manavgat_2021`
- target: `evia_2021`
- primary population: burnable_tree_shrub_grass
- protected frozen inputs/references: unchanged

| feature | manavgat_2021_auc | manavgat_2021_ci | manavgat_2021_direction | evia_2021_auc | evia_2021_ci | evia_2021_direction | direction_reversal_status | step9_diagnostic_concordance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ndvi_mean | 0.5640 | [0.4993, 0.6278] | higher_values_rank_burned | 0.5310 | [0.3985, 0.6710] | higher_values_rank_burned | no_direction_reversal | False |
| elevation_mean | 0.2320 | [0.1789, 0.2876] | lower_values_rank_burned | 0.6472 | [0.4982, 0.7861] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| slope_mean | 0.4002 | [0.3403, 0.4589] | lower_values_rank_burned | 0.5207 | [0.4008, 0.6504] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| lst_anomaly_mean | 0.5088 | [0.4598, 0.5604] | higher_values_rank_burned | 0.5487 | [0.4583, 0.6382] | higher_values_rank_burned | no_direction_reversal | False |
| current_lst_mean | 0.6647 | [0.6081, 0.7187] | higher_values_rank_burned | 0.4158 | [0.2766, 0.5450] | lower_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| current_tvdi_mean | 0.6771 | [0.6218, 0.7329] | higher_values_rank_burned | 0.3752 | [0.2495, 0.4990] | lower_values_rank_burned | bootstrap_supported_direction_reversal | True |
| tvdi_difference_mean | 0.4604 | [0.4095, 0.5099] | lower_values_rank_burned | 0.5211 | [0.4376, 0.6040] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| downscaled_lst_mean | 0.6832 | [0.6261, 0.7386] | higher_values_rank_burned | 0.4152 | [0.2723, 0.5535] | lower_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| fused_lst_mean | 0.6662 | [0.6104, 0.7205] | higher_values_rank_burned | 0.4141 | [0.2759, 0.5439] | lower_values_rank_burned | point_direction_reversal_interval_uncertain | True |

## Which features reverse direction between manavgat_2021 and evia_2021?
['elevation_mean', 'slope_mean', 'current_lst_mean', 'current_tvdi_mean', 'tvdi_difference_mean', 'downscaled_lst_mean', 'fused_lst_mean']

## Which reversals are bootstrap-supported?
['current_tvdi_mean']

## Which features retain the same direction?
['ndvi_mean', 'lst_anomaly_mean']

## Point reversals with uncertain intervals
['elevation_mean', 'slope_mean', 'current_lst_mean', 'tvdi_difference_mean', 'downscaled_lst_mean', 'fused_lst_mean']

## Claim boundary

Feature-level univariate AUC direction reversals indicate that marginal feature-label relationships are not stable across the selected regions, a pattern consistent with concept/relationship shift. Target labels are used only for this diagnostic evaluation. This does NOT prove causality or establish concept shift as the only transfer-failure mechanism; AUC below 0.5 is a direction and is never inverted.
