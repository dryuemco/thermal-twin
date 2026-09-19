# Cross-Region Target-Region Spatial-Block Bootstrap

- source: `manavgat_2021`
- target: `evia_2021_extended`
- replicates requested: 1000
- random seed: 42

Percentile 95% confidence intervals from TARGET-REGION spatial-block bootstrap (blocks resampled with replacement; all rows in a sampled block are kept together). These are NOT classical p-values and the result is NOT described as statistically significant.

## Results

| direction | population | n_replicates | delta_auc CI | interp | delta_pr_auc CI | interp | delta_brier CI | interp | brier_improvement CI |
|---|---|---|---|---|---|---|---|---|---|
| evia_2021_extended_to_manavgat_2021 | all_valid | 1000 | [-0.0589, -0.0299] | negative_bootstrap_support | [0.0251, 0.0646] | positive_bootstrap_support | [-0.0329, -0.0249] | positive_bootstrap_support | [0.0249, 0.0329] |
| evia_2021_extended_to_manavgat_2021 | burnable_tree_shrub | 1000 | [-0.0359, -0.0032] | negative_bootstrap_support | [0.0336, 0.0779] | positive_bootstrap_support | [-0.0217, -0.0137] | positive_bootstrap_support | [0.0137, 0.0217] |
| evia_2021_extended_to_manavgat_2021 | burnable_tree_shrub_grass | 1000 | [-0.0662, -0.0344] | negative_bootstrap_support | [0.0096, 0.0524] | positive_bootstrap_support | [-0.0158, -0.0090] | positive_bootstrap_support | [0.0090, 0.0158] |
| manavgat_2021_to_evia_2021_extended | all_valid | 1000 | [-0.0508, -0.0308] | negative_bootstrap_support | [-0.0001, 0.0331] | uncertain | [0.0233, 0.0289] | negative_bootstrap_support | [-0.0289, -0.0233] |
| manavgat_2021_to_evia_2021_extended | burnable_tree_shrub | 1000 | [0.0087, 0.0429] | positive_bootstrap_support | [0.0113, 0.0521] | positive_bootstrap_support | [-0.0169, -0.0039] | positive_bootstrap_support | [0.0039, 0.0169] |
| manavgat_2021_to_evia_2021_extended | burnable_tree_shrub_grass | 1000 | [0.0162, 0.0454] | positive_bootstrap_support | [0.0217, 0.0553] | positive_bootstrap_support | [-0.0141, -0.0020] | positive_bootstrap_support | [0.0020, 0.0141] |

## Wording policy

- `positive_bootstrap_support`, `uncertain`, `negative_bootstrap_support` only.
- No classical p-values. No claim of statistical significance.