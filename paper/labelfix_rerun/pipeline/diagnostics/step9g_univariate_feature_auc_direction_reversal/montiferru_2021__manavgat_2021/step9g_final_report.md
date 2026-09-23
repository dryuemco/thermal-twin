# Step9G Univariate Feature-AUC Direction-Reversal -- Final Report

- analysis_id: `16ba1398e0f98d591929c71442d6e435f12d86fa7f7ec712bd21f6b6e4795f6a`
- source: `montiferru_2021`
- target: `manavgat_2021`
- primary population: burnable_tree_shrub_grass
- protected frozen inputs/references: unchanged

| feature | montiferru_2021_auc | montiferru_2021_ci | montiferru_2021_direction | manavgat_2021_auc | manavgat_2021_ci | manavgat_2021_direction | direction_reversal_status | step9_diagnostic_concordance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ndvi_mean | 0.5863 | [0.4501, 0.7044] | higher_values_rank_burned | 0.5640 | [0.4993, 0.6278] | higher_values_rank_burned | no_direction_reversal | False |
| elevation_mean | 0.5838 | [0.3953, 0.7623] | higher_values_rank_burned | 0.2320 | [0.1789, 0.2876] | lower_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| slope_mean | 0.6520 | [0.5060, 0.7705] | higher_values_rank_burned | 0.4002 | [0.3403, 0.4589] | lower_values_rank_burned | bootstrap_supported_direction_reversal | True |
| lst_anomaly_mean | 0.3952 | [0.2851, 0.5345] | lower_values_rank_burned | 0.5088 | [0.4598, 0.5604] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| current_lst_mean | 0.3705 | [0.2478, 0.5130] | lower_values_rank_burned | 0.6647 | [0.6081, 0.7187] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| current_tvdi_mean | 0.3555 | [0.2332, 0.4991] | lower_values_rank_burned | 0.6771 | [0.6218, 0.7329] | higher_values_rank_burned | bootstrap_supported_direction_reversal | True |
| tvdi_difference_mean | 0.3776 | [0.2821, 0.4965] | lower_values_rank_burned | 0.4604 | [0.4095, 0.5099] | lower_values_rank_burned | no_direction_reversal | False |
| downscaled_lst_mean | 0.3647 | [0.2403, 0.5111] | lower_values_rank_burned | 0.6832 | [0.6261, 0.7386] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| fused_lst_mean | 0.3705 | [0.2478, 0.5130] | lower_values_rank_burned | 0.6662 | [0.6104, 0.7205] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |

## Which features reverse direction between montiferru_2021 and manavgat_2021?
['elevation_mean', 'slope_mean', 'lst_anomaly_mean', 'current_lst_mean', 'current_tvdi_mean', 'downscaled_lst_mean', 'fused_lst_mean']

## Which reversals are bootstrap-supported?
['slope_mean', 'current_tvdi_mean']

## Which features retain the same direction?
['ndvi_mean', 'tvdi_difference_mean']

## Point reversals with uncertain intervals
['elevation_mean', 'lst_anomaly_mean', 'current_lst_mean', 'downscaled_lst_mean', 'fused_lst_mean']

## Claim boundary

Feature-level univariate AUC direction reversals indicate that marginal feature-label relationships are not stable across the selected regions, a pattern consistent with concept/relationship shift. Target labels are used only for this diagnostic evaluation. This does NOT prove causality or establish concept shift as the only transfer-failure mechanism; AUC below 0.5 is a direction and is never inverted.
