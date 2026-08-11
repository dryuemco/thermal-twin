# Step9G Univariate Feature-AUC Direction-Reversal -- Final Report

- analysis_id: `ea95fd9ae0804091112afe2bdeabc0681fb889a06ca97b9eb7f0b6b94d6acb35`
- source: `bejis_2022`
- target: `evia_2021_extended`
- primary population: burnable_tree_shrub_grass
- protected frozen inputs/references: unchanged

| feature | bejis_2022_auc | bejis_2022_ci | bejis_2022_direction | evia_2021_extended_auc | evia_2021_extended_ci | evia_2021_extended_direction | direction_reversal_status | step9_diagnostic_concordance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ndvi_mean | 0.5588 | [0.4972, 0.6193] | higher_values_rank_burned | 0.6391 | [0.5749, 0.7006] | higher_values_rank_burned | no_direction_reversal | False |
| elevation_mean | 0.6433 | [0.5583, 0.7290] | higher_values_rank_burned | 0.5406 | [0.4484, 0.6261] | higher_values_rank_burned | no_direction_reversal | False |
| slope_mean | 0.5208 | [0.4393, 0.6053] | higher_values_rank_burned | 0.4865 | [0.4177, 0.5540] | lower_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| lst_anomaly_mean | 0.4180 | [0.3638, 0.4796] | lower_values_rank_burned | 0.6401 | [0.5671, 0.7102] | higher_values_rank_burned | bootstrap_supported_direction_reversal | True |
| current_lst_mean | 0.4767 | [0.4012, 0.5475] | lower_values_rank_burned | 0.3765 | [0.3013, 0.4559] | lower_values_rank_burned | no_direction_reversal | False |
| current_tvdi_mean | 0.5173 | [0.4290, 0.5952] | higher_values_rank_burned | 0.3619 | [0.2852, 0.4422] | lower_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| tvdi_difference_mean | 0.5125 | [0.4432, 0.5829] | higher_values_rank_burned | 0.5191 | [0.4444, 0.5889] | higher_values_rank_burned | no_direction_reversal | False |
| downscaled_lst_mean | 0.4836 | [0.4004, 0.5598] | lower_values_rank_burned | 0.3765 | [0.2969, 0.4593] | lower_values_rank_burned | no_direction_reversal | False |
| fused_lst_mean | 0.4806 | [0.4039, 0.5514] | lower_values_rank_burned | 0.3757 | [0.3002, 0.4556] | lower_values_rank_burned | no_direction_reversal | False |

## Which features reverse direction between bejis_2022 and evia_2021_extended?
['slope_mean', 'lst_anomaly_mean', 'current_tvdi_mean']

## Which reversals are bootstrap-supported?
['lst_anomaly_mean']

## Which features retain the same direction?
['ndvi_mean', 'elevation_mean', 'current_lst_mean', 'tvdi_difference_mean', 'downscaled_lst_mean', 'fused_lst_mean']

## Point reversals with uncertain intervals
['slope_mean', 'current_tvdi_mean']

## Claim boundary

Feature-level univariate AUC direction reversals indicate that marginal feature-label relationships are not stable across the selected regions, a pattern consistent with concept/relationship shift. Target labels are used only for this diagnostic evaluation. This does NOT prove causality or establish concept shift as the only transfer-failure mechanism; AUC below 0.5 is a direction and is never inverted.
