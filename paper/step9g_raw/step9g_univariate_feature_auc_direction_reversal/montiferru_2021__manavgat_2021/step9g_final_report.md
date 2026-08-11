# Step9G Univariate Feature-AUC Direction-Reversal -- Final Report

- analysis_id: `b4e9cc7d61bbe457a8c4ab75360d2ee284572937056d2680b8d2638f86f752f0`
- source: `montiferru_2021`
- target: `manavgat_2021`
- primary population: burnable_tree_shrub_grass
- protected frozen inputs/references: unchanged

| feature | montiferru_2021_auc | montiferru_2021_ci | montiferru_2021_direction | manavgat_2021_auc | manavgat_2021_ci | manavgat_2021_direction | direction_reversal_status | step9_diagnostic_concordance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ndvi_mean | 0.5863 | [0.4501, 0.7044] | higher_values_rank_burned | 0.6359 | [0.5872, 0.6763] | higher_values_rank_burned | no_direction_reversal | False |
| elevation_mean | 0.5838 | [0.3953, 0.7623] | higher_values_rank_burned | 0.3741 | [0.2891, 0.4712] | lower_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| slope_mean | 0.6520 | [0.5060, 0.7705] | higher_values_rank_burned | 0.5310 | [0.4228, 0.6417] | higher_values_rank_burned | no_direction_reversal | False |
| lst_anomaly_mean | 0.3952 | [0.2851, 0.5345] | lower_values_rank_burned | 0.4824 | [0.4280, 0.5299] | lower_values_rank_burned | no_direction_reversal | False |
| current_lst_mean | 0.3705 | [0.2478, 0.5130] | lower_values_rank_burned | 0.5383 | [0.4518, 0.6205] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| current_tvdi_mean | 0.3555 | [0.2332, 0.4991] | lower_values_rank_burned | 0.5520 | [0.4602, 0.6411] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| tvdi_difference_mean | 0.3776 | [0.2821, 0.4965] | lower_values_rank_burned | 0.4494 | [0.3905, 0.5052] | lower_values_rank_burned | no_direction_reversal | False |
| downscaled_lst_mean | 0.3647 | [0.2403, 0.5111] | lower_values_rank_burned | 0.5521 | [0.4660, 0.6372] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| fused_lst_mean | 0.3705 | [0.2478, 0.5130] | lower_values_rank_burned | 0.5401 | [0.4543, 0.6219] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |

## Which features reverse direction between montiferru_2021 and manavgat_2021?
['elevation_mean', 'current_lst_mean', 'current_tvdi_mean', 'downscaled_lst_mean', 'fused_lst_mean']

## Which reversals are bootstrap-supported?
none

## Which features retain the same direction?
['ndvi_mean', 'slope_mean', 'lst_anomaly_mean', 'tvdi_difference_mean']

## Point reversals with uncertain intervals
['elevation_mean', 'current_lst_mean', 'current_tvdi_mean', 'downscaled_lst_mean', 'fused_lst_mean']

## Claim boundary

Feature-level univariate AUC direction reversals indicate that marginal feature-label relationships are not stable across the selected regions, a pattern consistent with concept/relationship shift. Target labels are used only for this diagnostic evaluation. This does NOT prove causality or establish concept shift as the only transfer-failure mechanism; AUC below 0.5 is a direction and is never inverted.
