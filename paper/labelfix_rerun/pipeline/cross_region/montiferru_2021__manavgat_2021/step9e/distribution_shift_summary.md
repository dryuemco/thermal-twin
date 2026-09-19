# Step9E: Cross-Region Distribution-Shift and Relationship-Shift Audit

- source: `montiferru_2021`
- target: `manavgat_2021`
- primary population: `burnable_tree_shrub_grass`

> The original Step9 evaluation showed asymmetric or partial cross-region support for the thermal predictor set. Step9E examines the feature-distribution, probability-scale, and feature-label relationship shifts associated with this mixed result.

## Diagnosis categories

`high_shift`, `probability_scale_shift`, `ranking_reversal_suspected`, `relationship_direction_instability`

## Likely contributors to poor cross-region discrimination

- Feature distributions differ between regions for one or more shared predictors (elevated standardized mean difference / PSI / normalized Wasserstein distance).
- The direction of the association between one or more features and burned status is not consistent between the two regions (mean/median/rank-effect direction flips).
- Predicted probabilities on the target region are concentrated below the source-selected threshold or diverge from the target's observed prevalence.
- Diagnostic evidence is consistent with (but does not prove) a ranking-orientation reversal on the target region for at least one model/direction/population.

## Top globally shifted features (primary population)

| feature | smd | psi (source->target) | psi (target->source) | norm. wasserstein (source IQR) | outside-source-support fraction | category |
|---|---|---|---|---|---|---|
| slope_mean | 1.500853183795167 | 1.8424406588548445 | 2.2620663021413283 | 1.3736359971324066 | 0.2947686607186388 | high_shift |
| elevation_mean | 1.0695121829123462 | 1.2450874276967947 | 5.17951835672188 | 1.1544901631428428 | 0.5043147579347667 | high_shift |
| tvdi_difference_mean | 0.8725134558068084 | 0.7449531640698785 | 1.0580234735308665 | 0.8363220584446476 | 0.1591687041564792 | high_shift |
| ndvi_mean | -0.6581314635618933 | 0.8739706380140726 | 0.48377133409188267 | 0.39951532553324626 | 0.09229194090975575 | moderate_shift |
| current_tvdi_mean | -0.5576344814360088 | 0.3219952693463719 | 0.3310029294170677 | 0.3766908165411648 | 0.06381106058383454 | moderate_shift |
| lst_anomaly_mean | 0.27244506005000485 | 0.5414796265317388 | 1.8525861107335895 | 0.8009911444104414 | 0.2803849588252803 | moderate_shift |
| downscaled_lst_mean | -0.025260771671703233 | 0.20630527059551235 | 0.1770781020307589 | 0.10821666007646635 | 0.014138754814489786 | low_shift |
| fused_lst_mean | -0.006853278361652239 | 0.15098158293181071 | 0.1313362707509655 | 0.09428870985049768 | 0.022475744722344107 | low_shift |
| current_lst_mean | -0.003816066960322579 | 0.14621221909274287 | 0.13234185073283064 | 0.09318977183070638 | 0.023666324385115643 | low_shift |

## Strongest missingness differences

| feature | source missing fraction | target missing fraction | gap |
|---|---|---|---|
| lst_anomaly_mean | 0.0 | 0.017210277412120327 | 0.017210277412120327 |
| tvdi_difference_mean | 0.0 | 0.0029740139437375067 | 0.0029740139437375067 |
| current_tvdi_mean | 0.0 | 0.00292525961679099 | 0.00292525961679099 |
| current_lst_mean | 0.0 | 0.00292525961679099 | 0.00292525961679099 |
| downscaled_lst_mean | 0.0011792452830188679 | 0.0 | 0.0011792452830188679 |

## Landcover differences (primary population)

- total variation distance: 0.06617485739359368
- Jensen-Shannon divergence: 0.009166485906174623
- target categories unseen in source: ['60']
- source categories unseen in target: []

## Features with a label-relationship direction flip (primary population)

| feature | relationship_flip_score | raw AUC below 0.5 in one region only |
|---|---|---|
| current_lst_mean | 3 | True |
| current_tvdi_mean | 3 | True |
| downscaled_lst_mean | 3 | True |
| elevation_mean | 3 | True |
| fused_lst_mean | 3 | True |
| lst_anomaly_mean | 2 | True |
| slope_mean | 3 | True |

## Prediction probability scale

- ranking reversal suspected (any direction/model, primary population): True
- no probability collapse below threshold flagged.

## Interpretation rules

- Step9E is a post-hoc diagnostic analysis.
- It does not alter the original cross-region evaluation (Step9A-D outputs are read-only inputs here and are never modified).
- Target labels are inspected only to diagnose relationship shift after the transfer evaluation was completed.
- Any new normalization or feature-selection strategy suggested by Step9E must be evaluated as a new experiment.
- It must not be validated on the same target regions and then described as an unbiased transfer result.
- A third independent region or nested evaluation design is required for a stronger follow-up generalization claim.

## Never claimed by this report

- statistical significance
- causal explanation
- successful operational transfer
- corrected transfer performance

## Scope note

This is a POST-HOC diagnostic audit of the existing Step9B/Step9C cross-region transfer evaluation. It does not retrain any model, does not modify Step9B predictions or Step9C bootstrap outputs, and does not change the reported Step9 conclusion.