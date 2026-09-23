# Cross-Region Target-Region Spatial-Block Bootstrap

- source: `manavgat_2021`
- target: `mugla_2021`
- replicates requested: 1000
- random seed: 42

Percentile 95% confidence intervals from TARGET-REGION spatial-block bootstrap (blocks resampled with replacement; all rows in a sampled block are kept together). These are NOT classical p-values and the result is NOT described as statistically significant.

## Results

| direction | population | n_replicates | delta_auc CI | interp | delta_pr_auc CI | interp | delta_brier CI | interp | brier_improvement CI |
|---|---|---|---|---|---|---|---|---|---|
| manavgat_2021_to_mugla_2021 | all_valid | 1000 | [-0.0262, -0.0121] | negative_bootstrap_support | [-0.0080, -0.0032] | negative_bootstrap_support | [0.0010, 0.0042] | negative_bootstrap_support | [-0.0042, -0.0010] |
| manavgat_2021_to_mugla_2021 | burnable_tree_shrub | 1000 | [-0.0408, -0.0167] | negative_bootstrap_support | [-0.0103, -0.0038] | negative_bootstrap_support | [0.0022, 0.0076] | negative_bootstrap_support | [-0.0076, -0.0022] |
| manavgat_2021_to_mugla_2021 | burnable_tree_shrub_grass | 1000 | [-0.0396, -0.0161] | negative_bootstrap_support | [-0.0083, -0.0034] | negative_bootstrap_support | [-0.0014, 0.0041] | uncertain | [-0.0041, 0.0014] |
| mugla_2021_to_manavgat_2021 | all_valid | 1000 | [-0.0750, -0.0526] | negative_bootstrap_support | [-0.0153, -0.0101] | negative_bootstrap_support | [-0.0298, -0.0217] | positive_bootstrap_support | [0.0217, 0.0298] |
| mugla_2021_to_manavgat_2021 | burnable_tree_shrub | 1000 | [-0.0533, -0.0228] | negative_bootstrap_support | [-0.0098, -0.0040] | negative_bootstrap_support | [-0.0180, -0.0079] | positive_bootstrap_support | [0.0079, 0.0180] |
| mugla_2021_to_manavgat_2021 | burnable_tree_shrub_grass | 1000 | [-0.0894, -0.0652] | negative_bootstrap_support | [-0.0157, -0.0106] | negative_bootstrap_support | [-0.0037, 0.0055] | uncertain | [-0.0055, 0.0037] |

## Wording policy

- `positive_bootstrap_support`, `uncertain`, `negative_bootstrap_support` only.
- No classical p-values. No claim of statistical significance.