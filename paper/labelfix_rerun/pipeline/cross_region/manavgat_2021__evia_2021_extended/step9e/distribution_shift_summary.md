# Step9E: Cross-Region Distribution-Shift and Relationship-Shift Audit

- source: `manavgat_2021`
- target: `evia_2021_extended`
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
| elevation_mean | -1.285913006611338 | 2.476786050400035 | 1.3956431386196768 | 0.564263253289874 | 0.014411701441170145 | high_shift |
| ndvi_mean | 0.5940498189991963 | 0.3799386428265855 | 0.42083619018235113 | 0.40891092940414886 | 0.09711765971176597 | moderate_shift |
| lst_anomaly_mean | 0.49427165415563573 | 0.5952843155811807 | 0.5304961314161948 | 0.4423134487955694 | 0.0048807542983915694 | moderate_shift |
| slope_mean | -0.34536203286227013 | 0.14347486529228648 | 0.14418895746612947 | 0.25621976899925536 | 0.02097225209722521 | moderate_shift |
| current_tvdi_mean | 0.2804160165714652 | 0.11299636311350596 | 0.10315368464266182 | 0.16519313466475555 | 0.01509433962264151 | moderate_shift |
| tvdi_difference_mean | 0.19604117444189115 | 0.30117641934980416 | 0.2539939002504539 | 0.3045941083504158 | 0.004744958481613285 | low_shift |
| fused_lst_mean | 0.08620348513265426 | 0.03700324577087505 | 0.036822822337951026 | 0.05690749496517767 | 0.02484405248440525 | low_shift |
| downscaled_lst_mean | 0.08123178675914762 | 0.04573925509289599 | 0.04610423882596886 | 0.05702238819527542 | 0.03310751748251748 | low_shift |
| current_lst_mean | 0.08106318557240996 | 0.0354779003041823 | 0.035614722530302415 | 0.05404855829155575 | 0.024150943396226414 | low_shift |

## Strongest missingness differences

| feature | source missing fraction | target missing fraction | gap |
|---|---|---|---|
| downscaled_lst_mean | 0.0 | 0.015702301570230157 | 0.015702301570230157 |
| lst_anomaly_mean | 0.017210277412120327 | 0.030436653043665305 | 0.013226375631544978 |
| current_tvdi_mean | 0.00292525961679099 | 0.0024736502473650247 | 0.00045160936942596546 |
| current_lst_mean | 0.00292525961679099 | 0.0024736502473650247 | 0.00045160936942596546 |
| tvdi_difference_mean | 0.0029740139437375067 | 0.002688750268875027 | 0.0002852636748624797 |

## Landcover differences (primary population)

- total variation distance: 0.12490095630317155
- Jensen-Shannon divergence: 0.015617144329675368
- target categories unseen in source: ['90']
- source categories unseen in target: []

## Features with a label-relationship direction flip (primary population)

| feature | relationship_flip_score | raw AUC below 0.5 in one region only |
|---|---|---|
| current_lst_mean | 3 | True |
| current_tvdi_mean | 3 | True |
| downscaled_lst_mean | 3 | True |
| elevation_mean | 2 | True |
| fused_lst_mean | 3 | True |
| lst_anomaly_mean | 1 | False |
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