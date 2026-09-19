# Step8B: Baseline vs Baseline+Thermal Burned-Area Modeling

## What this step does

- Step8B is the **determining experiment** requested by the supervisor: does adding thermal/dryness features improve burned-area discrimination beyond baseline non-thermal features?
- It compares **Model A (baseline)**: elevation + slope + landcover + NDVI, against **Model B (baseline + thermal)**: Model A + current TVDI + LST anomaly + TVDI difference + downscaled/fused thermal features.
- It uses the **Step8A 500 m MCD64A1-grid dataset** -- each sample is one native ~500 m modeling cell, **never a 30 m pixel**.
- **MCD64A1 is the target label; FIRMS is never used as a target.**
- **Spatial-block cross-validation** (`StratifiedGroupKFold` over 500 m cell blocks) is used throughout; **no random row-wise split is ever performed.**
- **No statistical significance test is implemented** for delta metrics in this run -- results are point estimates only.

## Populations

- `all_valid` is the **primary analysis**, because the cropland-excluded burnable mask (`burnable_tree_shrub_grass`) has too few burned positives to be a reliable primary population.
- `cropland_dominant` is evaluated because the large majority of burned cells in this AOI/window are cropland-dominant.
- `burnable_tree_shrub_grass` and `burnable_tree_shrub` are **diagnostic/sensitivity only** and are skipped by default if burned positives are below the minimum threshold.

## Lead-time (monthly) evaluation

- Lead-time is evaluated using **out-of-fold predictions from the single full Aug-Oct model**, stratified by `burn_month` (August/September/October) -- **no separate monthly models are trained.**

## Key result: delta AUC

- **all_valid** (n_pos=3046, n_neg=21041, folds=5): AUC baseline=`0.8647` -> thermal=`0.9212` (delta_auc=`+0.0565`); PR-AUC baseline=`0.4811` -> thermal=`0.6469` (delta_pr_auc=`+0.1658`); **thermal_improves**
- **cropland_dominant** (n_pos=54, n_neg=1206, folds=5): AUC baseline=`0.8898` -> thermal=`0.8953` (delta_auc=`+0.0054`); PR-AUC baseline=`0.3004` -> thermal=`0.2342` (delta_pr_auc=`-0.0662`); **neutral**
- **burnable_tree_shrub_grass** (n_pos=2935, n_neg=17576, folds=5): AUC baseline=`0.8412` -> thermal=`0.9081` (delta_auc=`+0.0669`); PR-AUC baseline=`0.4699` -> thermal=`0.6456` (delta_pr_auc=`+0.1757`); **thermal_improves**
- **burnable_tree_shrub** (n_pos=2297, n_neg=13241, folds=5): AUC baseline=`0.7893` -> thermal=`0.8861` (delta_auc=`+0.0969`); PR-AUC baseline=`0.3651` -> thermal=`0.5863` (delta_pr_auc=`+0.2212`); **thermal_improves**

## Monthly lead-time metrics

- **all_valid**:
  - august (n_pos=686): AUC baseline=`0.8171` -> thermal=`0.8872` (delta_auc=`+0.0701`)
  - september: unavailable (month september has too few positives (0 < 10))
  - october: unavailable (month october has too few positives (0 < 10))
- **cropland_dominant**:
  - august: unavailable (month august has too few positives (0 < 10))
  - september: unavailable (month september has too few positives (0 < 10))
  - october: unavailable (month october has too few positives (0 < 10))
- **burnable_tree_shrub_grass**:
  - august (n_pos=684): AUC baseline=`0.7870` -> thermal=`0.8649` (delta_auc=`+0.0779`)
  - september: unavailable (month september has too few positives (0 < 10))
  - october: unavailable (month october has too few positives (0 < 10))
- **burnable_tree_shrub**:
  - august (n_pos=618): AUC baseline=`0.7507` -> thermal=`0.8525` (delta_auc=`+0.1018`)
  - september: unavailable (month september has too few positives (0 < 10))
  - october: unavailable (month october has too few positives (0 < 10))

## Gap-fill sensitivity (existing predictions only, no retraining)

- **all_valid**:
  - gapfilled_fraction < 0.25 (n=23305): AUC baseline=`0.8602` -> thermal=`0.9184` (delta_auc=`+0.0582`)
  - gapfilled_fraction < 0.5 (n=23680): AUC baseline=`0.8625` -> thermal=`0.9198` (delta_auc=`+0.0573`)
- **cropland_dominant**:
  - gapfilled_fraction < 0.25 (n=1260): AUC baseline=`0.8898` -> thermal=`0.8953` (delta_auc=`+0.0054`)
  - gapfilled_fraction < 0.5 (n=1260): AUC baseline=`0.8898` -> thermal=`0.8953` (delta_auc=`+0.0054`)

## Feature importance

- Feature importance is extracted from the final model refit on the whole population (per population, per model). **This is descriptive only -- not a causal attribution.**

Full metrics: `step8b_model_comparison_metrics.json`

## Warnings

- October burn_month positives are low (n=0 < 10); October metrics may be null.
