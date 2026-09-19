# Step9G Univariate Feature-AUC Direction-Reversal -- Final Report

- analysis_id: `0539a418ce832ee296d1803cd3a435909723534def1a532df97079136636ca5e`
- source: `manavgat_2021`
- target: `mugla_2021`
- primary population: burnable_tree_shrub_grass
- protected frozen inputs/references: unchanged

| feature | manavgat_2021_auc | manavgat_2021_ci | manavgat_2021_direction | mugla_2021_auc | mugla_2021_ci | mugla_2021_direction | direction_reversal_status | step9_diagnostic_concordance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ndvi_mean | 0.5640 | [0.4993, 0.6278] | higher_values_rank_burned | 0.6617 | [0.6156, 0.7035] | higher_values_rank_burned | no_direction_reversal | False |
| elevation_mean | 0.2320 | [0.1789, 0.2876] | lower_values_rank_burned | 0.6114 | [0.5319, 0.6904] | higher_values_rank_burned | bootstrap_supported_direction_reversal | True |
| slope_mean | 0.4002 | [0.3403, 0.4589] | lower_values_rank_burned | 0.6368 | [0.5819, 0.6864] | higher_values_rank_burned | bootstrap_supported_direction_reversal | True |
| lst_anomaly_mean | 0.5088 | [0.4598, 0.5604] | higher_values_rank_burned | 0.4846 | [0.3945, 0.5661] | lower_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| current_lst_mean | 0.6647 | [0.6081, 0.7187] | higher_values_rank_burned | 0.3248 | [0.2714, 0.3821] | lower_values_rank_burned | bootstrap_supported_direction_reversal | True |
| current_tvdi_mean | 0.6771 | [0.6218, 0.7329] | higher_values_rank_burned | 0.3358 | [0.2754, 0.3976] | lower_values_rank_burned | bootstrap_supported_direction_reversal | True |
| tvdi_difference_mean | 0.4604 | [0.4095, 0.5099] | lower_values_rank_burned | 0.4900 | [0.3964, 0.5747] | lower_values_rank_burned | no_direction_reversal | False |
| downscaled_lst_mean | 0.6832 | [0.6261, 0.7386] | higher_values_rank_burned | 0.3070 | [0.2532, 0.3658] | lower_values_rank_burned | bootstrap_supported_direction_reversal | True |
| fused_lst_mean | 0.6662 | [0.6104, 0.7205] | higher_values_rank_burned | 0.3252 | [0.2720, 0.3828] | lower_values_rank_burned | bootstrap_supported_direction_reversal | True |

## Which features reverse direction between manavgat_2021 and mugla_2021?
['elevation_mean', 'slope_mean', 'lst_anomaly_mean', 'current_lst_mean', 'current_tvdi_mean', 'downscaled_lst_mean', 'fused_lst_mean']

## Which reversals are bootstrap-supported?
['elevation_mean', 'slope_mean', 'current_lst_mean', 'current_tvdi_mean', 'downscaled_lst_mean', 'fused_lst_mean']

## Which features retain the same direction?
['ndvi_mean', 'tvdi_difference_mean']

## Point reversals with uncertain intervals
['lst_anomaly_mean']

## Claim boundary

Feature-level univariate AUC direction reversals indicate that marginal feature-label relationships are not stable across the selected regions, a pattern consistent with concept/relationship shift. Target labels are used only for this diagnostic evaluation. This does NOT prove causality or establish concept shift as the only transfer-failure mechanism; AUC below 0.5 is a direction and is never inverted.
