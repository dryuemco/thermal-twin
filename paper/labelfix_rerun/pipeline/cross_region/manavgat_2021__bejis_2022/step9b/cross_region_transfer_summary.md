# Cross-Region Transfer Summary

- source: `manavgat_2021`
- target: `bejis_2022`
- model: `random_forest`

This evaluates whether the Step8 burned-area **association** model (baseline vs. baseline+thermal) generalizes across independent Mediterranean wildfire regions. It is NOT a 30 m fire prediction model and NOT an operational fire detection system.

All preprocessing (numeric median imputation, categorical landcover one-hot encoding) is fitted using SOURCE REGION ONLY. No target-derived imputation values, no pooled source+target fitting, no target fine-tuning or calibration, no coordinate or region-identity features.

Classification threshold selected using SOURCE REGION spatial-block CV out-of-fold predictions only (F1-optimal over a grid), never using target labels.

## Results

| direction | population | skipped | target_prevalence | baseline_auc | thermal_auc | delta_auc | delta_pr_auc | delta_brier | brier_improvement |
|---|---|---|---|---|---|---|---|---|---|
| manavgat_2021_to_bejis_2022 | burnable_tree_shrub_grass | no | 0.0724 | 0.3707 | 0.3964 | 0.0257 | 0.0022 | -0.0214 | 0.0214 |
| manavgat_2021_to_bejis_2022 | all_valid | no | 0.0700 | 0.3945 | 0.4144 | 0.0199 | 0.0018 | -0.0256 | 0.0256 |
| manavgat_2021_to_bejis_2022 | burnable_tree_shrub | no | 0.0800 | 0.3354 | 0.3722 | 0.0368 | 0.0031 | -0.0290 | 0.0290 |
| bejis_2022_to_manavgat_2021 | burnable_tree_shrub_grass | no | 0.1431 | 0.2966 | 0.3142 | 0.0176 | 0.0013 | -0.0261 | 0.0261 |
| bejis_2022_to_manavgat_2021 | all_valid | no | 0.1265 | 0.3690 | 0.3745 | 0.0055 | 0.0002 | -0.0210 | 0.0210 |
| bejis_2022_to_manavgat_2021 | burnable_tree_shrub | no | 0.1478 | 0.3112 | 0.3004 | -0.0108 | -0.0024 | -0.0202 | 0.0202 |

## Scope note

Cross-region transfer of the Step8 ~500 m MCD64A1-cell burned-area association model only. Not a 30 m fire prediction model, not an operational fire detection system, does not transfer the Step7 downscaling model itself.