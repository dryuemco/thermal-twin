# Step9E: Cross-Region Distribution-Shift and Relationship-Shift Audit

- source: `manavgat_2021`
- target: `evia_2021`
- primary population: `burnable_tree_shrub_grass`

> The original Step9 evaluation showed asymmetric or partial cross-region support for the thermal predictor set. Step9E examines the feature-distribution, probability-scale, and feature-label relationship shifts associated with this mixed result.

## Diagnosis categories

`high_shift`, `probability_scale_shift`, `relationship_direction_instability`

## Likely contributors to poor cross-region discrimination

- Feature distributions differ between regions for one or more shared predictors (elevated standardized mean difference / PSI / normalized Wasserstein distance).
- The direction of the association between one or more features and burned status is not consistent between the two regions (mean/median/rank-effect direction flips).
- Predicted probabilities on the target region are concentrated below the source-selected threshold or diverge from the target's observed prevalence.

## Top globally shifted features (primary population)

| feature | smd | psi (source->target) | psi (target->source) | norm. wasserstein (source IQR) | outside-source-support fraction | category |
|---|---|---|---|---|---|---|
| elevation_mean | -1.3633635229532715 | 4.638680624870301 | 1.5211996122840166 | 0.5872832600050572 | 0.01444500760263558 | high_shift |
| ndvi_mean | 0.9235654156799099 | 0.7934417982369568 | 0.8602924727490214 | 0.6079516211877996 | 0.12696401419158643 | high_shift |
| lst_anomaly_mean | 0.7449315122263769 | 1.1320617951881191 | 0.8790089498407043 | 0.6171563224227368 | 0.0005246589716684155 | moderate_shift |
| slope_mean | -0.442067823030569 | 0.34171417040931407 | 0.34724975602518937 | 0.30854812848732344 | 0.0225544855549924 | moderate_shift |
| tvdi_difference_mean | 0.28401912648625843 | 0.27601071882521844 | 0.24924753198302046 | 0.3386882959171359 | 0.0007639419404125286 | moderate_shift |
| current_tvdi_mean | 0.22402576189764395 | 0.14186676915671037 | 0.12818888992333644 | 0.13057312042054417 | 0.006875477463712758 | moderate_shift |
| downscaled_lst_mean | -0.1943250391291123 | 0.16410716765748484 | 0.14852725977572195 | 0.15922178981680749 | 0.008671257332313186 | low_shift |
| current_lst_mean | -0.1896764881704777 | 0.14705950145521654 | 0.13802796809573573 | 0.16034915948388698 | 0.005092946269416858 | low_shift |
| fused_lst_mean | -0.1865161908242934 | 0.15004693842498118 | 0.14475337327451904 | 0.15856282066686908 | 0.0063355296502787635 | low_shift |

## Strongest missingness differences

| feature | source missing fraction | target missing fraction | gap |
|---|---|---|---|
| lst_anomaly_mean | 0.017210277412120327 | 0.03395843892549417 | 0.01674816151337384 |
| downscaled_lst_mean | 0.0 | 0.0063355296502787635 | 0.0063355296502787635 |
| current_tvdi_mean | 0.00292525961679099 | 0.00481500253421186 | 0.00188974291742087 |
| current_lst_mean | 0.00292525961679099 | 0.00481500253421186 | 0.00188974291742087 |
| tvdi_difference_mean | 0.0029740139437375067 | 0.00481500253421186 | 0.0018409885904743534 |

## Landcover differences (primary population)

- total variation distance: 0.17220020864282015
- Jensen-Shannon divergence: 0.029505252644505053
- target categories unseen in source: []
- source categories unseen in target: []

## Features with a label-relationship direction flip (primary population)

| feature | relationship_flip_score | raw AUC below 0.5 in one region only |
|---|---|---|
| current_lst_mean | 3 | True |
| current_tvdi_mean | 3 | True |
| downscaled_lst_mean | 3 | True |
| elevation_mean | 3 | True |
| fused_lst_mean | 3 | True |
| lst_anomaly_mean | 1 | False |
| slope_mean | 3 | True |
| tvdi_difference_mean | 3 | True |

## Prediction probability scale

- ranking reversal suspected (any direction/model, primary population): False
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