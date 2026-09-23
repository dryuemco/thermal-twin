# Step9G Univariate Feature-AUC Direction-Reversal -- Final Report

- analysis_id: `cc8f2299ae76963ef184f01e88c473be76952ca631fb9f33dfac26f3faa38e19`
- source: `manavgat_2021`
- target: `bejis_2022`
- primary population: burnable_tree_shrub_grass
- protected frozen inputs/references: unchanged

| feature | manavgat_auc | manavgat_ci | manavgat_direction | bejis_auc | bejis_ci | bejis_direction | direction_reversal_status | step9_diagnostic_concordance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ndvi_mean | 0.5640 | [0.4993, 0.6278] | higher_values_rank_burned | 0.5588 | [0.4972, 0.6193] | higher_values_rank_burned | no_direction_reversal | False |
| elevation_mean | 0.2320 | [0.1789, 0.2876] | lower_values_rank_burned | 0.6433 | [0.5583, 0.7290] | higher_values_rank_burned | bootstrap_supported_direction_reversal | True |
| slope_mean | 0.4002 | [0.3403, 0.4589] | lower_values_rank_burned | 0.5208 | [0.4393, 0.6053] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| lst_anomaly_mean | 0.5088 | [0.4598, 0.5604] | higher_values_rank_burned | 0.4180 | [0.3638, 0.4796] | lower_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| current_lst_mean | 0.6647 | [0.6081, 0.7187] | higher_values_rank_burned | 0.4767 | [0.4012, 0.5475] | lower_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| current_tvdi_mean | 0.6771 | [0.6218, 0.7329] | higher_values_rank_burned | 0.5173 | [0.4290, 0.5952] | higher_values_rank_burned | no_direction_reversal | False |
| tvdi_difference_mean | 0.4604 | [0.4095, 0.5099] | lower_values_rank_burned | 0.5125 | [0.4432, 0.5829] | higher_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| downscaled_lst_mean | 0.6832 | [0.6261, 0.7386] | higher_values_rank_burned | 0.4836 | [0.4004, 0.5598] | lower_values_rank_burned | point_direction_reversal_interval_uncertain | True |
| fused_lst_mean | 0.6662 | [0.6104, 0.7205] | higher_values_rank_burned | 0.4806 | [0.4039, 0.5514] | lower_values_rank_burned | point_direction_reversal_interval_uncertain | True |

## Which features reverse direction between manavgat_2021 and bejis_2022?
['elevation_mean', 'slope_mean', 'lst_anomaly_mean', 'current_lst_mean', 'tvdi_difference_mean', 'downscaled_lst_mean', 'fused_lst_mean']

## Which reversals are bootstrap-supported?
['elevation_mean']

## Which features retain the same direction?
['ndvi_mean', 'current_tvdi_mean']

## Point reversals with uncertain intervals
['slope_mean', 'lst_anomaly_mean', 'current_lst_mean', 'tvdi_difference_mean', 'downscaled_lst_mean', 'fused_lst_mean']

## Claim boundary

Raw cross-region transfer was below chance; unsupervised adaptation recovered part of the discrimination loss; a large gap to within-region performance remained. Feature-level univariate AUC direction reversals indicate that marginal feature-label relationships are not stable across regions, a pattern consistent with residual concept/relationship shift. This does NOT prove causality and does NOT establish that concept shift is the only source of transfer failure; AUC below 0.5 is a direction, not poor performance, and is never inverted.
