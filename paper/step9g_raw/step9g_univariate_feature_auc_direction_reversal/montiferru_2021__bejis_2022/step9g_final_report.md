# Step9G Univariate Feature-AUC Direction-Reversal -- Final Report

- analysis_id: `319e400a3910f0f777c5b1bb5f701b5b1c3bc816a81ec920824f2fcbd7b9bd94`
- source: `montiferru_2021`
- target: `bejis_2022`
- primary population: burnable_tree_shrub_grass
- protected frozen inputs/references: unchanged

| feature | montiferru_2021_auc | montiferru_2021_ci | montiferru_2021_direction | bejis_2022_auc | bejis_2022_ci | bejis_2022_direction | direction_reversal_status | step9_diagnostic_concordance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ndvi_mean | 0.5863 | [0.4501, 0.7044] | higher_values_rank_burned | 0.5588 | [0.4972, 0.6193] | higher_values_rank_burned | no_direction_reversal | False |
| elevation_mean | 0.5838 | [0.3953, 0.7623] | higher_values_rank_burned | 0.6433 | [0.5583, 0.7290] | higher_values_rank_burned | no_direction_reversal | False |
| slope_mean | 0.6520 | [0.5060, 0.7705] | higher_values_rank_burned | 0.5208 | [0.4393, 0.6053] | higher_values_rank_burned | no_direction_reversal | False |
| lst_anomaly_mean | 0.3952 | [0.2851, 0.5345] | lower_values_rank_burned | 0.4180 | [0.3638, 0.4796] | lower_values_rank_burned | no_direction_reversal | False |
| current_lst_mean | 0.3705 | [0.2478, 0.5130] | lower_values_rank_burned | 0.4767 | [0.4012, 0.5475] | lower_values_rank_burned | no_direction_reversal | False |
| current_tvdi_mean | 0.3555 | [0.2332, 0.4991] | lower_values_rank_burned | 0.5173 | [0.4290, 0.5952] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| tvdi_difference_mean | 0.3776 | [0.2821, 0.4965] | lower_values_rank_burned | 0.5125 | [0.4432, 0.5829] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| downscaled_lst_mean | 0.3647 | [0.2403, 0.5111] | lower_values_rank_burned | 0.4836 | [0.4004, 0.5598] | lower_values_rank_burned | no_direction_reversal | False |
| fused_lst_mean | 0.3705 | [0.2478, 0.5130] | lower_values_rank_burned | 0.4806 | [0.4039, 0.5514] | lower_values_rank_burned | no_direction_reversal | False |

## Which features reverse direction between montiferru_2021 and bejis_2022?
['current_tvdi_mean', 'tvdi_difference_mean']

## Which reversals are bootstrap-supported?
none

## Which features retain the same direction?
['ndvi_mean', 'elevation_mean', 'slope_mean', 'lst_anomaly_mean', 'current_lst_mean', 'downscaled_lst_mean', 'fused_lst_mean']

## Point reversals with uncertain intervals
['current_tvdi_mean', 'tvdi_difference_mean']

## Claim boundary

Feature-level univariate AUC direction reversals indicate that marginal feature-label relationships are not stable across the selected regions, a pattern consistent with concept/relationship shift. Target labels are used only for this diagnostic evaluation. This does NOT prove causality or establish concept shift as the only transfer-failure mechanism; AUC below 0.5 is a direction and is never inverted.
