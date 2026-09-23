# Cross-Region Target-Region Spatial-Block Bootstrap

- source: `manavgat_2021`
- target: `evia_2021`
- replicates requested: 1000
- random seed: 42

Percentile 95% confidence intervals from TARGET-REGION spatial-block bootstrap (blocks resampled with replacement; all rows in a sampled block are kept together). These are NOT classical p-values and the result is NOT described as statistically significant.

## Results

| direction | population | n_replicates | delta_auc CI | interp | delta_pr_auc CI | interp | delta_brier CI | interp | brier_improvement CI |
|---|---|---|---|---|---|---|---|---|---|
| evia_2021_to_manavgat_2021 | all_valid | 1000 | [-0.0987, -0.0707] | negative_bootstrap_support | [-0.0167, 0.0127] | uncertain | [-0.0051, 0.0034] | uncertain | [-0.0034, 0.0051] |
| evia_2021_to_manavgat_2021 | burnable_tree_shrub | 1000 | [-0.1349, -0.0965] | negative_bootstrap_support | [-0.0517, -0.0170] | negative_bootstrap_support | [0.0496, 0.0621] | negative_bootstrap_support | [-0.0621, -0.0496] |
| evia_2021_to_manavgat_2021 | burnable_tree_shrub_grass | 1000 | [-0.1764, -0.1409] | negative_bootstrap_support | [-0.0591, -0.0287] | negative_bootstrap_support | [0.0497, 0.0599] | negative_bootstrap_support | [-0.0599, -0.0497] |
| manavgat_2021_to_evia_2021 | all_valid | 1000 | [-0.0671, -0.0413] | negative_bootstrap_support | [-0.0288, 0.0104] | uncertain | [0.0090, 0.0190] | negative_bootstrap_support | [-0.0190, -0.0090] |
| manavgat_2021_to_evia_2021 | burnable_tree_shrub | 1000 | [-0.0482, 0.0041] | uncertain | [-0.0063, 0.0354] | uncertain | [-0.0133, 0.0074] | uncertain | [-0.0074, 0.0133] |
| manavgat_2021_to_evia_2021 | burnable_tree_shrub_grass | 1000 | [-0.0276, 0.0155] | uncertain | [0.0016, 0.0394] | positive_bootstrap_support | [-0.0136, 0.0050] | uncertain | [-0.0050, 0.0136] |

## Wording policy

- `positive_bootstrap_support`, `uncertain`, `negative_bootstrap_support` only.
- No classical p-values. No claim of statistical significance.