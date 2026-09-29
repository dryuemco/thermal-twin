# Step9G Univariate Feature-AUC Direction-Reversal -- Final Report

- analysis_id: `1862489bb81cfe4e097e88eaae64aad5f959c0d444da1aff61755a7e14653ae7`
- source: `montiferru_2021`
- target: `evia_2021_extended`
- primary population: burnable_tree_shrub_grass
- protected frozen inputs/references: unchanged

| feature | montiferru_2021_auc | montiferru_2021_ci | montiferru_2021_direction | evia_2021_extended_auc | evia_2021_extended_ci | evia_2021_extended_direction | direction_reversal_status | step9_diagnostic_concordance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ndvi_mean | 0.5863 | [0.4501, 0.7044] | higher_values_rank_burned | 0.6391 | [0.5749, 0.7006] | higher_values_rank_burned | no_direction_reversal | False |
| elevation_mean | 0.5838 | [0.3953, 0.7623] | higher_values_rank_burned | 0.5406 | [0.4484, 0.6261] | higher_values_rank_burned | no_direction_reversal | False |
| slope_mean | 0.6520 | [0.5060, 0.7705] | higher_values_rank_burned | 0.4865 | [0.4177, 0.5540] | lower_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| lst_anomaly_mean | 0.3952 | [0.2851, 0.5345] | lower_values_rank_burned | 0.6401 | [0.5671, 0.7102] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| current_lst_mean | 0.3705 | [0.2478, 0.5130] | lower_values_rank_burned | 0.3765 | [0.3013, 0.4559] | lower_values_rank_burned | no_direction_reversal | False |
| current_tvdi_mean | 0.3555 | [0.2332, 0.4991] | lower_values_rank_burned | 0.3619 | [0.2852, 0.4422] | lower_values_rank_burned | no_direction_reversal | False |
| tvdi_difference_mean | 0.3776 | [0.2821, 0.4965] | lower_values_rank_burned | 0.5191 | [0.4444, 0.5889] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| downscaled_lst_mean | 0.3647 | [0.2403, 0.5111] | lower_values_rank_burned | 0.3765 | [0.2969, 0.4593] | lower_values_rank_burned | no_direction_reversal | False |
| fused_lst_mean | 0.3705 | [0.2478, 0.5130] | lower_values_rank_burned | 0.3757 | [0.3002, 0.4556] | lower_values_rank_burned | no_direction_reversal | False |

## Which features reverse direction between montiferru_2021 and evia_2021_extended?
['slope_mean', 'lst_anomaly_mean', 'tvdi_difference_mean']

## Which reversals are bootstrap-supported?
none

## Which features retain the same direction?
['ndvi_mean', 'elevation_mean', 'current_lst_mean', 'current_tvdi_mean', 'downscaled_lst_mean', 'fused_lst_mean']

## Point reversals with uncertain intervals
['slope_mean', 'lst_anomaly_mean', 'tvdi_difference_mean']

## Claim boundary

Feature-level univariate AUC direction reversals indicate that marginal feature-label relationships are not stable across the selected regions, a pattern consistent with concept/relationship shift. Target labels are used only for this diagnostic evaluation. This does NOT prove causality or establish concept shift as the only transfer-failure mechanism; AUC below 0.5 is a direction and is never inverted.
