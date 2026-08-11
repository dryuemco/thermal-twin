# Step9G Univariate Feature-AUC Direction-Reversal -- Final Report

- analysis_id: `36ea8da48e31bc4353b212e984196bce53df857e09667512eb1bc3cbb94a7ce7`
- source: `mugla_2021`
- target: `mugla_2022_event_relative`
- primary population: burnable_tree_shrub_grass
- protected frozen inputs/references: unchanged

| feature | mugla_2021_auc | mugla_2021_ci | mugla_2021_direction | mugla_2022_event_relative_auc | mugla_2022_event_relative_ci | mugla_2022_event_relative_direction | direction_reversal_status | step9_diagnostic_concordance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ndvi_mean | 0.6617 | [0.6156, 0.7035] | higher_values_rank_burned | 0.7071 | [0.6239, 0.7768] | higher_values_rank_burned | no_direction_reversal | False |
| elevation_mean | 0.6114 | [0.5319, 0.6904] | higher_values_rank_burned | 0.2959 | [0.2298, 0.3547] | lower_values_rank_burned | bootstrap_supported_direction_reversal | True |
| slope_mean | 0.6368 | [0.5819, 0.6864] | higher_values_rank_burned | 0.5577 | [0.4676, 0.6340] | higher_values_rank_burned | no_direction_reversal | False |
| lst_anomaly_mean | 0.4846 | [0.3945, 0.5661] | lower_values_rank_burned | 0.3799 | [0.2487, 0.5015] | lower_values_rank_burned | no_direction_reversal | False |
| current_lst_mean | 0.3248 | [0.2714, 0.3821] | lower_values_rank_burned | 0.5155 | [0.4335, 0.5797] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| current_tvdi_mean | 0.3358 | [0.2754, 0.3976] | lower_values_rank_burned | 0.5935 | [0.4754, 0.6739] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| tvdi_difference_mean | 0.4900 | [0.3964, 0.5747] | lower_values_rank_burned | 0.3970 | [0.2654, 0.5135] | lower_values_rank_burned | no_direction_reversal | False |
| downscaled_lst_mean | 0.3070 | [0.2532, 0.3658] | lower_values_rank_burned | 0.5082 | [0.4348, 0.5706] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| fused_lst_mean | 0.3252 | [0.2720, 0.3828] | lower_values_rank_burned | 0.5186 | [0.4363, 0.5829] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |

## Which features reverse direction between mugla_2021 and mugla_2022_event_relative?
['elevation_mean', 'current_lst_mean', 'current_tvdi_mean', 'downscaled_lst_mean', 'fused_lst_mean']

## Which reversals are bootstrap-supported?
['elevation_mean']

## Which features retain the same direction?
['ndvi_mean', 'slope_mean', 'lst_anomaly_mean', 'tvdi_difference_mean']

## Point reversals with uncertain intervals
['current_lst_mean', 'current_tvdi_mean', 'downscaled_lst_mean', 'fused_lst_mean']

## Claim boundary

Feature-level univariate AUC direction reversals indicate that marginal feature-label relationships are not stable across the selected regions, a pattern consistent with concept/relationship shift. Target labels are used only for this diagnostic evaluation. This does NOT prove causality or establish concept shift as the only transfer-failure mechanism; AUC below 0.5 is a direction and is never inverted.
