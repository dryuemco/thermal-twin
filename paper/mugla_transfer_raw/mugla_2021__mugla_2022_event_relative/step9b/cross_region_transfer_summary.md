# Cross-Region Transfer Summary

- source: `mugla_2021`
- target: `mugla_2022_event_relative`
- model: `random_forest`

This evaluates whether the Step8 burned-area **association** model (baseline vs. baseline+thermal) generalizes across independent Mediterranean wildfire regions. It is NOT a 30 m fire prediction model and NOT an operational fire detection system.

All preprocessing (numeric median imputation, categorical landcover one-hot encoding) is fitted using SOURCE REGION ONLY. No target-derived imputation values, no pooled source+target fitting, no target fine-tuning or calibration, no coordinate or region-identity features.

Classification threshold selected using SOURCE REGION spatial-block CV out-of-fold predictions only (F1-optimal over a grid), never using target labels.

## Results

| direction | population | skipped | target_prevalence | baseline_auc | thermal_auc | delta_auc | delta_pr_auc | delta_brier | brier_improvement |
|---|---|---|---|---|---|---|---|---|---|
| mugla_2021_to_mugla_2022_event_relative | burnable_tree_shrub_grass | no | 0.0085 | 0.6421 | 0.5588 | -0.0833 | -0.0018 | -0.0102 | 0.0102 |
| mugla_2021_to_mugla_2022_event_relative | all_valid | no | 0.0047 | 0.7966 | 0.7105 | -0.0861 | -0.0026 | -0.0195 | 0.0195 |
| mugla_2021_to_mugla_2022_event_relative | burnable_tree_shrub | no | 0.0096 | 0.6040 | 0.5485 | -0.0555 | -0.0011 | -0.0058 | 0.0058 |
| mugla_2022_event_relative_to_mugla_2021 | burnable_tree_shrub_grass | no | 0.0698 | 0.5809 | 0.6692 | 0.0883 | 0.0575 | -0.0069 | 0.0069 |
| mugla_2022_event_relative_to_mugla_2021 | all_valid | no | 0.0414 | 0.7518 | 0.7498 | -0.0019 | 0.0289 | -0.0040 | 0.0040 |
| mugla_2022_event_relative_to_mugla_2021 | burnable_tree_shrub | no | 0.0737 | 0.5482 | 0.6495 | 0.1013 | 0.0611 | -0.0092 | 0.0092 |

## Scope note

Cross-region transfer of the Step8 ~500 m MCD64A1-cell burned-area association model only. Not a 30 m fire prediction model, not an operational fire detection system, does not transfer the Step7 downscaling model itself.