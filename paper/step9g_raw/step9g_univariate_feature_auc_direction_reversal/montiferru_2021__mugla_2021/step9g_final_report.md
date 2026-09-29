# Step9G Univariate Feature-AUC Direction-Reversal -- Final Report

- analysis_id: `fe88bb9567a915c2a30092a10e921d80079f9a0ab2196bc097fba5fd126b41b4`
- source: `montiferru_2021`
- target: `mugla_2021`
- primary population: burnable_tree_shrub_grass
- protected frozen inputs/references: unchanged

| feature | montiferru_2021_auc | montiferru_2021_ci | montiferru_2021_direction | mugla_2021_auc | mugla_2021_ci | mugla_2021_direction | direction_reversal_status | step9_diagnostic_concordance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ndvi_mean | 0.5863 | [0.4501, 0.7044] | higher_values_rank_burned | 0.6617 | [0.6156, 0.7035] | higher_values_rank_burned | no_direction_reversal | False |
| elevation_mean | 0.5838 | [0.3953, 0.7623] | higher_values_rank_burned | 0.6114 | [0.5319, 0.6904] | higher_values_rank_burned | no_direction_reversal | False |
| slope_mean | 0.6520 | [0.5060, 0.7705] | higher_values_rank_burned | 0.6368 | [0.5819, 0.6864] | higher_values_rank_burned | no_direction_reversal | False |
| lst_anomaly_mean | 0.3952 | [0.2851, 0.5345] | lower_values_rank_burned | 0.4846 | [0.3945, 0.5661] | lower_values_rank_burned | no_direction_reversal | False |
| current_lst_mean | 0.3705 | [0.2478, 0.5130] | lower_values_rank_burned | 0.3248 | [0.2714, 0.3821] | lower_values_rank_burned | no_direction_reversal | False |
| current_tvdi_mean | 0.3555 | [0.2332, 0.4991] | lower_values_rank_burned | 0.3358 | [0.2754, 0.3976] | lower_values_rank_burned | no_direction_reversal | False |
| tvdi_difference_mean | 0.3776 | [0.2821, 0.4965] | lower_values_rank_burned | 0.4900 | [0.3964, 0.5747] | lower_values_rank_burned | no_direction_reversal | False |
| downscaled_lst_mean | 0.3647 | [0.2403, 0.5111] | lower_values_rank_burned | 0.3070 | [0.2532, 0.3658] | lower_values_rank_burned | no_direction_reversal | False |
| fused_lst_mean | 0.3705 | [0.2478, 0.5130] | lower_values_rank_burned | 0.3252 | [0.2720, 0.3828] | lower_values_rank_burned | no_direction_reversal | False |

## Which features reverse direction between montiferru_2021 and mugla_2021?
none

## Which reversals are bootstrap-supported?
none

## Which features retain the same direction?
['ndvi_mean', 'elevation_mean', 'slope_mean', 'lst_anomaly_mean', 'current_lst_mean', 'current_tvdi_mean', 'tvdi_difference_mean', 'downscaled_lst_mean', 'fused_lst_mean']

## Point reversals with uncertain intervals
none

## Claim boundary

Feature-level univariate AUC direction reversals indicate that marginal feature-label relationships are not stable across the selected regions, a pattern consistent with concept/relationship shift. Target labels are used only for this diagnostic evaluation. This does NOT prove causality or establish concept shift as the only transfer-failure mechanism; AUC below 0.5 is a direction and is never inverted.
