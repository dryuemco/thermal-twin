# Step9G Univariate Feature-AUC Direction-Reversal -- Final Report

- analysis_id: `3cc2420d467883c71f3bd000c7ab2174b12e0149a8f3f6e96359dcea53f8dc6e`
- source: `bejis_2022`
- target: `evia_2021`
- primary population: burnable_tree_shrub_grass
- protected frozen inputs/references: unchanged

| feature | bejis_2022_auc | bejis_2022_ci | bejis_2022_direction | evia_2021_auc | evia_2021_ci | evia_2021_direction | direction_reversal_status | step9_diagnostic_concordance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ndvi_mean | 0.5588 | [0.4972, 0.6193] | higher_values_rank_burned | 0.5310 | [0.3985, 0.6710] | higher_values_rank_burned | no_direction_reversal | False |
| elevation_mean | 0.6433 | [0.5583, 0.7290] | higher_values_rank_burned | 0.6472 | [0.4982, 0.7861] | higher_values_rank_burned | no_direction_reversal | False |
| slope_mean | 0.5208 | [0.4393, 0.6053] | higher_values_rank_burned | 0.5207 | [0.4008, 0.6504] | higher_values_rank_burned | no_direction_reversal | False |
| lst_anomaly_mean | 0.4180 | [0.3638, 0.4796] | lower_values_rank_burned | 0.5487 | [0.4583, 0.6382] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| current_lst_mean | 0.4767 | [0.4012, 0.5475] | lower_values_rank_burned | 0.4158 | [0.2766, 0.5450] | lower_values_rank_burned | no_direction_reversal | False |
| current_tvdi_mean | 0.5173 | [0.4290, 0.5952] | higher_values_rank_burned | 0.3752 | [0.2495, 0.4990] | lower_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| tvdi_difference_mean | 0.5125 | [0.4432, 0.5829] | higher_values_rank_burned | 0.5211 | [0.4376, 0.6040] | higher_values_rank_burned | no_direction_reversal | False |
| downscaled_lst_mean | 0.4836 | [0.4004, 0.5598] | lower_values_rank_burned | 0.4152 | [0.2723, 0.5535] | lower_values_rank_burned | no_direction_reversal | False |
| fused_lst_mean | 0.4806 | [0.4039, 0.5514] | lower_values_rank_burned | 0.4141 | [0.2759, 0.5439] | lower_values_rank_burned | no_direction_reversal | False |

## Which features reverse direction between bejis_2022 and evia_2021?
['lst_anomaly_mean', 'current_tvdi_mean']

## Which reversals are bootstrap-supported?
none

## Which features retain the same direction?
['ndvi_mean', 'elevation_mean', 'slope_mean', 'current_lst_mean', 'tvdi_difference_mean', 'downscaled_lst_mean', 'fused_lst_mean']

## Point reversals with uncertain intervals
['lst_anomaly_mean', 'current_tvdi_mean']

## Claim boundary

Feature-level univariate AUC direction reversals indicate that marginal feature-label relationships are not stable across the selected regions, a pattern consistent with concept/relationship shift. Target labels are used only for this diagnostic evaluation. This does NOT prove causality or establish concept shift as the only transfer-failure mechanism; AUC below 0.5 is a direction and is never inverted.
