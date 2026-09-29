# Cross-Region Transfer Summary

- source: `mugla_2021`
- target: `manavgat_2021`
- model: `random_forest`

This evaluates whether the Step8 burned-area **association** model (baseline vs. baseline+thermal) generalizes across independent Mediterranean wildfire regions. It is NOT a 30 m fire prediction model and NOT an operational fire detection system.

All preprocessing (numeric median imputation, categorical landcover one-hot encoding) is fitted using SOURCE REGION ONLY. No target-derived imputation values, no pooled source+target fitting, no target fine-tuning or calibration, no coordinate or region-identity features.

Classification threshold selected using SOURCE REGION spatial-block CV out-of-fold predictions only (F1-optimal over a grid), never using target labels.

## Results

| direction | population | skipped | target_prevalence | baseline_auc | thermal_auc | delta_auc | delta_pr_auc | delta_brier | brier_improvement |
|---|---|---|---|---|---|---|---|---|---|
| mugla_2021_to_manavgat_2021 | burnable_tree_shrub_grass | no | 0.1431 | 0.4223 | 0.3450 | -0.0773 | -0.0130 | 0.0008 | -0.0008 |
| mugla_2021_to_manavgat_2021 | all_valid | no | 0.1265 | 0.5021 | 0.4383 | -0.0639 | -0.0127 | -0.0258 | 0.0258 |
| mugla_2021_to_manavgat_2021 | burnable_tree_shrub | no | 0.1478 | 0.4037 | 0.3653 | -0.0384 | -0.0069 | -0.0130 | 0.0130 |
| manavgat_2021_to_mugla_2021 | burnable_tree_shrub_grass | no | 0.0698 | 0.4656 | 0.4377 | -0.0279 | -0.0057 | 0.0014 | -0.0014 |
| manavgat_2021_to_mugla_2021 | all_valid | no | 0.0414 | 0.6770 | 0.6576 | -0.0194 | -0.0054 | 0.0026 | -0.0026 |
| manavgat_2021_to_mugla_2021 | burnable_tree_shrub | no | 0.0737 | 0.4737 | 0.4453 | -0.0284 | -0.0068 | 0.0049 | -0.0049 |

## Scope note

Cross-region transfer of the Step8 ~500 m MCD64A1-cell burned-area association model only. Not a 30 m fire prediction model, not an operational fire detection system, does not transfer the Step7 downscaling model itself.