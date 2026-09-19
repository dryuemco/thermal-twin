# Step9G Univariate Feature-AUC Direction-Reversal -- Final Report

- analysis_id: `15bda8fc40e9587effb0e8a5cfc2cb8b1cc5f6ab94635d6b0f9bdb10336a0460`
- source: `manavgat_2021`
- target: `evia_2021_extended`
- primary population: burnable_tree_shrub_grass
- protected frozen inputs/references: unchanged

| feature | manavgat_2021_auc | manavgat_2021_ci | manavgat_2021_direction | evia_2021_extended_auc | evia_2021_extended_ci | evia_2021_extended_direction | direction_reversal_status | step9_diagnostic_concordance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ndvi_mean | 0.5640 | [0.4993, 0.6278] | higher_values_rank_burned | 0.6391 | [0.5749, 0.7006] | higher_values_rank_burned | no_direction_reversal | False |
| elevation_mean | 0.2320 | [0.1789, 0.2876] | lower_values_rank_burned | 0.5406 | [0.4484, 0.6261] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| slope_mean | 0.4002 | [0.3403, 0.4589] | lower_values_rank_burned | 0.4865 | [0.4177, 0.5540] | lower_values_rank_burned | no_direction_reversal | False |
| lst_anomaly_mean | 0.5088 | [0.4598, 0.5604] | higher_values_rank_burned | 0.6401 | [0.5671, 0.7102] | higher_values_rank_burned | no_direction_reversal | False |
| current_lst_mean | 0.6647 | [0.6081, 0.7187] | higher_values_rank_burned | 0.3765 | [0.3013, 0.4559] | lower_values_rank_burned | bootstrap_supported_direction_reversal | True |
| current_tvdi_mean | 0.6771 | [0.6218, 0.7329] | higher_values_rank_burned | 0.3619 | [0.2852, 0.4422] | lower_values_rank_burned | bootstrap_supported_direction_reversal | True |
| tvdi_difference_mean | 0.4604 | [0.4095, 0.5099] | lower_values_rank_burned | 0.5191 | [0.4444, 0.5889] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| downscaled_lst_mean | 0.6832 | [0.6261, 0.7386] | higher_values_rank_burned | 0.3765 | [0.2969, 0.4593] | lower_values_rank_burned | bootstrap_supported_direction_reversal | True |
| fused_lst_mean | 0.6662 | [0.6104, 0.7205] | higher_values_rank_burned | 0.3757 | [0.3002, 0.4556] | lower_values_rank_burned | bootstrap_supported_direction_reversal | True |

## Which features reverse direction between manavgat_2021 and evia_2021_extended?
['elevation_mean', 'current_lst_mean', 'current_tvdi_mean', 'tvdi_difference_mean', 'downscaled_lst_mean', 'fused_lst_mean']

## Which reversals are bootstrap-supported?
['current_lst_mean', 'current_tvdi_mean', 'downscaled_lst_mean', 'fused_lst_mean']

## Which features retain the same direction?
['ndvi_mean', 'slope_mean', 'lst_anomaly_mean']

## Point reversals with uncertain intervals
['elevation_mean', 'tvdi_difference_mean']

## Claim boundary

Feature-level univariate AUC direction reversals indicate that marginal feature-label relationships are not stable across the selected regions, a pattern consistent with concept/relationship shift. Target labels are used only for this diagnostic evaluation. This does NOT prove causality or establish concept shift as the only transfer-failure mechanism; AUC below 0.5 is a direction and is never inverted.
