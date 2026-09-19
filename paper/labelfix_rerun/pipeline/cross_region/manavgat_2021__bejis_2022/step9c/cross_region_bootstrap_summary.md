# Cross-Region Target-Region Spatial-Block Bootstrap

- source: `manavgat_2021`
- target: `bejis_2022`
- replicates requested: 1000
- random seed: 42

Percentile 95% confidence intervals from TARGET-REGION spatial-block bootstrap (blocks resampled with replacement; all rows in a sampled block are kept together). These are NOT classical p-values and the result is NOT described as statistically significant.

## Results

| direction | population | n_replicates | delta_auc CI | interp | delta_pr_auc CI | interp | delta_brier CI | interp | brier_improvement CI |
|---|---|---|---|---|---|---|---|---|---|
| bejis_2022_to_manavgat_2021 | all_valid | 1000 | [-0.0047, 0.0157] | uncertain | [-0.0014, 0.0018] | uncertain | [-0.0232, -0.0188] | positive_bootstrap_support | [0.0188, 0.0232] |
| bejis_2022_to_manavgat_2021 | burnable_tree_shrub | 1000 | [-0.0217, 0.0004] | uncertain | [-0.0043, -0.0007] | negative_bootstrap_support | [-0.0232, -0.0171] | positive_bootstrap_support | [0.0171, 0.0232] |
| bejis_2022_to_manavgat_2021 | burnable_tree_shrub_grass | 1000 | [0.0065, 0.0291] | positive_bootstrap_support | [-0.0004, 0.0030] | uncertain | [-0.0286, -0.0235] | positive_bootstrap_support | [0.0235, 0.0286] |
| manavgat_2021_to_bejis_2022 | all_valid | 1000 | [0.0048, 0.0344] | positive_bootstrap_support | [0.0004, 0.0031] | positive_bootstrap_support | [-0.0282, -0.0228] | positive_bootstrap_support | [0.0228, 0.0282] |
| manavgat_2021_to_bejis_2022 | burnable_tree_shrub | 1000 | [0.0195, 0.0541] | positive_bootstrap_support | [0.0016, 0.0047] | positive_bootstrap_support | [-0.0319, -0.0263] | positive_bootstrap_support | [0.0263, 0.0319] |
| manavgat_2021_to_bejis_2022 | burnable_tree_shrub_grass | 1000 | [0.0101, 0.0420] | positive_bootstrap_support | [0.0009, 0.0037] | positive_bootstrap_support | [-0.0239, -0.0188] | positive_bootstrap_support | [0.0188, 0.0239] |

## Wording policy

- `positive_bootstrap_support`, `uncertain`, `negative_bootstrap_support` only.
- No classical p-values. No claim of statistical significance.