# Cross-Region Target-Region Spatial-Block Bootstrap

- source: `mugla_2021`
- target: `mugla_2022_event_relative`
- replicates requested: 1000
- random seed: 42

Percentile 95% confidence intervals from TARGET-REGION spatial-block bootstrap (blocks resampled with replacement; all rows in a sampled block are kept together). These are NOT classical p-values and the result is NOT described as statistically significant.

## Results

| direction | population | n_replicates | delta_auc CI | interp | delta_pr_auc CI | interp | delta_brier CI | interp | brier_improvement CI |
|---|---|---|---|---|---|---|---|---|---|
| mugla_2021_to_mugla_2022_event_relative | all_valid | 1000 | [-0.1129, -0.0577] | negative_bootstrap_support | [-0.0043, -0.0006] | negative_bootstrap_support | [-0.0207, -0.0185] | positive_bootstrap_support | [0.0185, 0.0207] |
| mugla_2021_to_mugla_2022_event_relative | burnable_tree_shrub | 1000 | [-0.1006, -0.0079] | negative_bootstrap_support | [-0.0029, 0.0010] | uncertain | [-0.0074, -0.0042] | positive_bootstrap_support | [0.0042, 0.0074] |
| mugla_2021_to_mugla_2022_event_relative | burnable_tree_shrub_grass | 1000 | [-0.1269, -0.0396] | negative_bootstrap_support | [-0.0035, 0.0001] | uncertain | [-0.0117, -0.0086] | positive_bootstrap_support | [0.0086, 0.0117] |
| mugla_2022_event_relative_to_mugla_2021 | all_valid | 1000 | [-0.0116, 0.0072] | uncertain | [0.0205, 0.0376] | positive_bootstrap_support | [-0.0046, -0.0034] | positive_bootstrap_support | [0.0034, 0.0046] |
| mugla_2022_event_relative_to_mugla_2021 | burnable_tree_shrub | 1000 | [0.0818, 0.1191] | positive_bootstrap_support | [0.0470, 0.0769] | positive_bootstrap_support | [-0.0104, -0.0078] | positive_bootstrap_support | [0.0078, 0.0104] |
| mugla_2022_event_relative_to_mugla_2021 | burnable_tree_shrub_grass | 1000 | [0.0721, 0.1040] | positive_bootstrap_support | [0.0458, 0.0708] | positive_bootstrap_support | [-0.0079, -0.0058] | positive_bootstrap_support | [0.0058, 0.0079] |

## Wording policy

- `positive_bootstrap_support`, `uncertain`, `negative_bootstrap_support` only.
- No classical p-values. No claim of statistical significance.