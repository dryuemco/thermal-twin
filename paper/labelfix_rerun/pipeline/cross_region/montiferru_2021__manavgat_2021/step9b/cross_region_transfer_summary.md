# Cross-Region Transfer Summary

- source: `montiferru_2021`
- target: `manavgat_2021`
- model: `random_forest`

This evaluates whether the Step8 burned-area **association** model (baseline vs. baseline+thermal) generalizes across independent Mediterranean wildfire regions. It is NOT a 30 m fire prediction model and NOT an operational fire detection system.

All preprocessing (numeric median imputation, categorical landcover one-hot encoding) is fitted using SOURCE REGION ONLY. No target-derived imputation values, no pooled source+target fitting, no target fine-tuning or calibration, no coordinate or region-identity features.

Classification threshold selected using SOURCE REGION spatial-block CV out-of-fold predictions only (F1-optimal over a grid), never using target labels.

## Results

| direction | population | skipped | target_prevalence | baseline_auc | thermal_auc | delta_auc | delta_pr_auc | delta_brier | brier_improvement |
|---|---|---|---|---|---|---|---|---|---|
| montiferru_2021_to_manavgat_2021 | burnable_tree_shrub_grass | no | 0.1431 | 0.3379 | 0.4041 | 0.0662 | 0.0116 | -0.1395 | 0.1395 |
| montiferru_2021_to_manavgat_2021 | all_valid | no | 0.1265 | 0.4081 | 0.4582 | 0.0501 | 0.0095 | -0.1125 | 0.1125 |
| montiferru_2021_to_manavgat_2021 | burnable_tree_shrub | no | 0.1478 | 0.3249 | 0.4191 | 0.0943 | 0.0147 | -0.1518 | 0.1518 |
| manavgat_2021_to_montiferru_2021 | burnable_tree_shrub_grass | no | 0.2119 | 0.5340 | 0.5178 | -0.0162 | 0.0180 | -0.0470 | 0.0470 |
| manavgat_2021_to_montiferru_2021 | all_valid | no | 0.2197 | 0.5528 | 0.5386 | -0.0142 | 0.0165 | -0.0351 | 0.0351 |
| manavgat_2021_to_montiferru_2021 | burnable_tree_shrub | no | 0.2269 | 0.4940 | 0.5037 | 0.0097 | 0.0478 | -0.0605 | 0.0605 |

## Scope note

Cross-region transfer of the Step8 ~500 m MCD64A1-cell burned-area association model only. Not a 30 m fire prediction model, not an operational fire detection system, does not transfer the Step7 downscaling model itself.