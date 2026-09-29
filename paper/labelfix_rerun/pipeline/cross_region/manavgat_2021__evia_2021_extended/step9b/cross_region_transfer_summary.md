# Cross-Region Transfer Summary

- source: `manavgat_2021`
- target: `evia_2021_extended`
- model: `random_forest`

This evaluates whether the Step8 burned-area **association** model (baseline vs. baseline+thermal) generalizes across independent Mediterranean wildfire regions. It is NOT a 30 m fire prediction model and NOT an operational fire detection system.

All preprocessing (numeric median imputation, categorical landcover one-hot encoding) is fitted using SOURCE REGION ONLY. No target-derived imputation values, no pooled source+target fitting, no target fine-tuning or calibration, no coordinate or region-identity features.

Classification threshold selected using SOURCE REGION spatial-block CV out-of-fold predictions only (F1-optimal over a grid), never using target labels.

## Results

| direction | population | skipped | target_prevalence | baseline_auc | thermal_auc | delta_auc | delta_pr_auc | delta_brier | brier_improvement |
|---|---|---|---|---|---|---|---|---|---|
| manavgat_2021_to_evia_2021_extended | burnable_tree_shrub_grass | no | 0.2865 | 0.6226 | 0.6540 | 0.0314 | 0.0382 | -0.0083 | 0.0083 |
| manavgat_2021_to_evia_2021_extended | all_valid | no | 0.1217 | 0.8608 | 0.8200 | -0.0408 | 0.0158 | 0.0263 | -0.0263 |
| manavgat_2021_to_evia_2021_extended | burnable_tree_shrub | no | 0.3018 | 0.6140 | 0.6397 | 0.0258 | 0.0303 | -0.0102 | 0.0102 |
| evia_2021_extended_to_manavgat_2021 | burnable_tree_shrub_grass | no | 0.1431 | 0.7274 | 0.6769 | -0.0505 | 0.0290 | -0.0120 | 0.0120 |
| evia_2021_extended_to_manavgat_2021 | all_valid | no | 0.1265 | 0.7640 | 0.7204 | -0.0436 | 0.0457 | -0.0290 | 0.0290 |
| evia_2021_extended_to_manavgat_2021 | burnable_tree_shrub | no | 0.1478 | 0.7308 | 0.7109 | -0.0198 | 0.0558 | -0.0176 | 0.0176 |

## Scope note

Cross-region transfer of the Step8 ~500 m MCD64A1-cell burned-area association model only. Not a 30 m fire prediction model, not an operational fire detection system, does not transfer the Step7 downscaling model itself.