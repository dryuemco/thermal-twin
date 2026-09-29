# Step9E: Cross-Region Distribution-Shift and Relationship-Shift Audit

- source: `mugla_2021`
- target: `mugla_2022_event_relative`
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
| downscaled_lst_mean | -1.8220748699073412 | 2.7643553275169226 | 2.910785211763236 | 1.1875135881539312 | 0.37145693461166696 | high_shift |
| fused_lst_mean | -1.6648822319343959 | 2.3972199768513565 | 2.4769373465882323 | 1.0809141417527421 | 0.30961588038154164 | high_shift |
| current_lst_mean | -1.6563113336585233 | 2.3837788965412177 | 2.449100141310432 | 1.0750222220862982 | 0.30563490002596727 | high_shift |
| tvdi_difference_mean | -1.3131336629260542 | 1.6518831648055985 | 2.6010693511953864 | 1.3667183815033466 | 0.4066013971485704 | high_shift |
| lst_anomaly_mean | -1.0133135546880692 | 1.0371853864036358 | 1.2549325400457885 | 1.0229593724595598 | 0.19371395311921266 | high_shift |
| current_tvdi_mean | -0.4718925744399425 | 0.2226680515020407 | 0.23796732423951383 | 0.3500969142399772 | 0.061828096598286156 | moderate_shift |
| ndvi_mean | 0.07631167920809574 | 0.041828449909850046 | 0.03865507678948557 | 0.08071004348470481 | 0.01237432327919567 | low_shift |
| slope_mean | -0.035165174535213575 | 0.0011928065058353513 | 0.0011811233197756266 | 0.026610063219900938 | 0.019077081722093325 | low_shift |
| elevation_mean | -0.03381561073013315 | 0.0018908977931444497 | 0.0018565729508918162 | 0.021975301044680682 | 0.018458365558133537 | low_shift |

## Strongest missingness differences

| feature | source missing fraction | target missing fraction | gap |
|---|---|---|---|
| downscaled_lst_mean | 0.0 | 0.01317349832431039 | 0.01317349832431039 |
| lst_anomaly_mean | 0.03213515456506111 | 0.02557360144367105 | 0.006561553121390059 |
| tvdi_difference_mean | 0.006110711718188354 | 0.007295694766692447 | 0.0011849830485040928 |
| current_tvdi_mean | 0.006110711718188354 | 0.007218355246197474 | 0.00110764352800912 |
| current_lst_mean | 0.006110711718188354 | 0.007218355246197474 | 0.00110764352800912 |

## Landcover differences (primary population)

- total variation distance: 0.004432779576435887
- Jensen-Shannon divergence: 2.1682413864305036e-05
- target categories unseen in source: []
- source categories unseen in target: []

## Features with a label-relationship direction flip (primary population)

| feature | relationship_flip_score | raw AUC below 0.5 in one region only |
|---|---|---|
| current_lst_mean | 2 | True |
| current_tvdi_mean | 3 | True |
| downscaled_lst_mean | 2 | True |
| elevation_mean | 3 | True |
| fused_lst_mean | 3 | True |
| lst_anomaly_mean | 1 | False |
| tvdi_difference_mean | 1 | False |

## Prediction probability scale

- ranking reversal suspected (any direction/model, primary population): False
- rows/models where predictions collapse below the source-selected threshold:
  - mugla_2022_event_relative_to_mugla_2021 / thermal: fraction above threshold = 0.0

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