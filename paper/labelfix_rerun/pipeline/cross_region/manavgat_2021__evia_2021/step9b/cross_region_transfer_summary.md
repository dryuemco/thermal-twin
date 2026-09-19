# Cross-Region Transfer Summary

- source: `manavgat_2021`
- target: `evia_2021`
- model: `random_forest`

This evaluates whether the Step8 burned-area **association** model (baseline vs. baseline+thermal) generalizes across independent Mediterranean wildfire regions. It is NOT a 30 m fire prediction model and NOT an operational fire detection system.

All preprocessing (numeric median imputation, categorical landcover one-hot encoding) is fitted using SOURCE REGION ONLY. No target-derived imputation values, no pooled source+target fitting, no target fine-tuning or calibration, no coordinate or region-identity features.

Classification threshold selected using SOURCE REGION spatial-block CV out-of-fold predictions only (F1-optimal over a grid), never using target labels.

## Results

| direction | population | skipped | target_prevalence | baseline_auc | thermal_auc | delta_auc | delta_pr_auc | delta_brier | brier_improvement |
|---|---|---|---|---|---|---|---|---|---|
| manavgat_2021_to_evia_2021 | burnable_tree_shrub_grass | no | 0.6749 | 0.6279 | 0.6221 | -0.0058 | 0.0203 | -0.0045 | 0.0045 |
| manavgat_2021_to_evia_2021 | all_valid | no | 0.3590 | 0.8895 | 0.8352 | -0.0543 | -0.0089 | 0.0143 | -0.0143 |
| manavgat_2021_to_evia_2021 | burnable_tree_shrub | no | 0.6941 | 0.6047 | 0.5823 | -0.0224 | 0.0150 | -0.0031 | 0.0031 |
| evia_2021_to_manavgat_2021 | burnable_tree_shrub_grass | no | 0.1431 | 0.7013 | 0.5432 | -0.1581 | -0.0439 | 0.0548 | -0.0548 |
| evia_2021_to_manavgat_2021 | all_valid | no | 0.1265 | 0.7522 | 0.6680 | -0.0842 | -0.0015 | -0.0010 | 0.0010 |
| evia_2021_to_manavgat_2021 | burnable_tree_shrub | no | 0.1478 | 0.6985 | 0.5827 | -0.1159 | -0.0349 | 0.0563 | -0.0563 |

## Scope note

Cross-region transfer of the Step8 ~500 m MCD64A1-cell burned-area association model only. Not a 30 m fire prediction model, not an operational fire detection system, does not transfer the Step7 downscaling model itself.