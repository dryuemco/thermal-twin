# Step9E: Cross-Region Distribution-Shift and Relationship-Shift Audit

- source: `manavgat_2021`
- target: `bejis_2022`
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
| tvdi_difference_mean | 1.2507742846770902 | 1.5137450200391214 | 1.4623515818021369 | 1.2335766015537548 | 0.11045163050893711 | high_shift |
| downscaled_lst_mean | 0.9607721205384939 | 1.6433626107305979 | 0.9103102612957386 | 0.5561858411041681 | 0.04114549045424622 | high_shift |
| current_lst_mean | 0.9047701925284859 | 1.346281642546677 | 0.8035513802267417 | 0.5286343451428075 | 0.025924409878564605 | high_shift |
| fused_lst_mean | 0.9019781143824159 | 1.3849433907817557 | 0.8190019546283293 | 0.5195545678442337 | 0.02468729427254773 | high_shift |
| lst_anomaly_mean | 0.6763101447262053 | 1.255016760247757 | 1.0960822040545988 | 0.5919996057449032 | 0.001266713581984518 | moderate_shift |
| slope_mean | -0.6293894430905174 | 0.4404053458869541 | 0.40162876294434 | 0.4391287343862156 | 0.0069782751810401585 | moderate_shift |
| ndvi_mean | -0.1967595960620139 | 0.08586749061546382 | 0.08152489269225166 | 0.14811789750489038 | 0.004147465437788018 | low_shift |
| current_tvdi_mean | -0.07167049265034965 | 0.13962572135105017 | 0.13131294035336288 | 0.11789269746648016 | 0.004775549188156638 | low_shift |
| elevation_mean | -0.03879631439042065 | 1.7254326538837985 | 0.549071473649495 | 0.20332536948692898 | 0.0 | low_shift |

## Strongest missingness differences

| feature | source missing fraction | target missing fraction | gap |
|---|---|---|---|
| lst_anomaly_mean | 0.017210277412120327 | 0.06451612903225806 | 0.047305851620137736 |
| current_tvdi_mean | 0.00292525961679099 | 0.035023041474654376 | 0.03209778185786338 |
| current_lst_mean | 0.00292525961679099 | 0.035023041474654376 | 0.03209778185786338 |
| tvdi_difference_mean | 0.0029740139437375067 | 0.035023041474654376 | 0.03204902753091687 |
| ndvi_mean | 0.0 | 0.0 | 0.0 |

## Landcover differences (primary population)

- total variation distance: 0.22479479451431336
- Jensen-Shannon divergence: 0.0617160123071124
- target categories unseen in source: []
- source categories unseen in target: []

## Features with a label-relationship direction flip (primary population)

| feature | relationship_flip_score | raw AUC below 0.5 in one region only |
|---|---|---|
| current_lst_mean | 3 | True |
| downscaled_lst_mean | 2 | True |
| elevation_mean | 3 | True |
| fused_lst_mean | 3 | True |
| lst_anomaly_mean | 2 | True |
| slope_mean | 3 | True |
| tvdi_difference_mean | 3 | True |

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