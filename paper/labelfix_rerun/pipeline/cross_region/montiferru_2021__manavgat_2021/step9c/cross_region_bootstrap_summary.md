# Cross-Region Target-Region Spatial-Block Bootstrap

- source: `montiferru_2021`
- target: `manavgat_2021`
- replicates requested: 1000
- random seed: 42

Percentile 95% confidence intervals from TARGET-REGION spatial-block bootstrap (blocks resampled with replacement; all rows in a sampled block are kept together). These are NOT classical p-values and the result is NOT described as statistically significant.

## Results

| direction | population | n_replicates | delta_auc CI | interp | delta_pr_auc CI | interp | delta_brier CI | interp | brier_improvement CI |
|---|---|---|---|---|---|---|---|---|---|
| manavgat_2021_to_montiferru_2021 | all_valid | 1000 | [-0.0443, 0.0158] | uncertain | [-0.0003, 0.0361] | uncertain | [-0.0456, -0.0246] | positive_bootstrap_support | [0.0246, 0.0456] |
| manavgat_2021_to_montiferru_2021 | burnable_tree_shrub | 1000 | [-0.0289, 0.0495] | uncertain | [0.0166, 0.0852] | positive_bootstrap_support | [-0.0743, -0.0454] | positive_bootstrap_support | [0.0454, 0.0743] |
| manavgat_2021_to_montiferru_2021 | burnable_tree_shrub_grass | 1000 | [-0.0466, 0.0126] | uncertain | [0.0008, 0.0401] | positive_bootstrap_support | [-0.0588, -0.0354] | positive_bootstrap_support | [0.0354, 0.0588] |
| montiferru_2021_to_manavgat_2021 | all_valid | 1000 | [0.0404, 0.0610] | positive_bootstrap_support | [0.0070, 0.0121] | positive_bootstrap_support | [-0.1170, -0.1078] | positive_bootstrap_support | [0.1078, 0.1170] |
| montiferru_2021_to_manavgat_2021 | burnable_tree_shrub | 1000 | [0.0804, 0.1085] | positive_bootstrap_support | [0.0110, 0.0183] | positive_bootstrap_support | [-0.1570, -0.1465] | positive_bootstrap_support | [0.1465, 0.1570] |
| montiferru_2021_to_manavgat_2021 | burnable_tree_shrub_grass | 1000 | [0.0533, 0.0796] | positive_bootstrap_support | [0.0087, 0.0145] | positive_bootstrap_support | [-0.1453, -0.1335] | positive_bootstrap_support | [0.1335, 0.1453] |

## Wording policy

- `positive_bootstrap_support`, `uncertain`, `negative_bootstrap_support` only.
- No classical p-values. No claim of statistical significance.