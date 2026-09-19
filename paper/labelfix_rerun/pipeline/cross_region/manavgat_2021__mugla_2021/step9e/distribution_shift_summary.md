# Step9E: Cross-Region Distribution-Shift and Relationship-Shift Audit

- source: `manavgat_2021`
- target: `mugla_2021`
- primary population: `burnable_tree_shrub_grass`

> Thermal incremental cross-region transfer was not supported in the original Step9 evaluation. Step9E examines whether feature-distribution shift, probability-scale shift, or region-dependent feature-label relationships are consistent with this result.

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
| current_tvdi_mean | 0.9019288329054103 | 1.2758797304445455 | 0.8053345841429838 | 0.4672867966651663 | 0.012778782399035564 | high_shift |
| elevation_mean | -0.7229873898207724 | 0.651637281858261 | 0.5694032203041033 | 0.3573190640621776 | 0.017397555715312724 | moderate_shift |
| downscaled_lst_mean | 0.6283475574393943 | 0.47061873233888146 | 0.4138641142801535 | 0.39783297495341613 | 0.046705008387251376 | moderate_shift |
| fused_lst_mean | 0.5826892728752419 | 0.37812214418556833 | 0.34310066422819135 | 0.3718955668131456 | 0.03973160795590702 | moderate_shift |
| current_lst_mean | 0.5799533389924263 | 0.3705520755794024 | 0.3352365158463426 | 0.37358571220424763 | 0.039710669077757686 | moderate_shift |
| slope_mean | -0.3324475754302461 | 0.13279394627119956 | 0.13277228074895991 | 0.2437824272070353 | 0.024011502516175412 | moderate_shift |
| tvdi_difference_mean | 0.18817230892037212 | 0.6480833828587504 | 0.36110276113312145 | 0.3375387606035785 | 0.00019288728149487644 | low_shift |
| lst_anomaly_mean | 0.1393088595855093 | 0.1411363259219766 | 0.12159460737562097 | 0.2055724057555769 | 0.0026244769615489365 | low_shift |
| ndvi_mean | 0.03342521759878719 | 0.00894592044544864 | 0.005918055004239834 | 0.036442696484519095 | 0.021806853582554516 | low_shift |

## Strongest missingness differences

| feature | source missing fraction | target missing fraction | gap |
|---|---|---|---|
| lst_anomaly_mean | 0.017210277412120327 | 0.03213515456506111 | 0.014924877152940781 |
| current_tvdi_mean | 0.00292525961679099 | 0.006110711718188354 | 0.0031854521013973637 |
| current_lst_mean | 0.00292525961679099 | 0.006110711718188354 | 0.0031854521013973637 |
| tvdi_difference_mean | 0.0029740139437375067 | 0.006110711718188354 | 0.003136697774450847 |
| ndvi_mean | 0.0 | 0.0 | 0.0 |

## Landcover differences (primary population)

- total variation distance: 0.14475309333236033
- Jensen-Shannon divergence: 0.022263545837404593
- target categories unseen in source: ['90']
- source categories unseen in target: []

## Features with a label-relationship direction flip (primary population)

| feature | relationship_flip_score | raw AUC below 0.5 in one region only |
|---|---|---|
| current_lst_mean | 3 | True |
| current_tvdi_mean | 3 | True |
| downscaled_lst_mean | 3 | True |
| elevation_mean | 3 | True |
| fused_lst_mean | 3 | True |
| lst_anomaly_mean | 3 | True |
| slope_mean | 3 | True |
| tvdi_difference_mean | 1 | False |

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