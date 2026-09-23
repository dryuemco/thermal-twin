# Step10 Preregistration (IMMUTABLE)

- analysis_id: `a382046d5453412ea0145ce4ee057b9dfb8394160d7eac32551db26a51fb19ef`
- created_at: 2026-09-19T09:04:08.339526+00:00
- git_commit: 6d024bc72e8cfc2b6dd8e26e4f7748a15de54fee
- source: `manavgat_2021` / target: `mugla_2021`
- directions: ['manavgat_2021_to_mugla_2021', 'mugla_2021_to_manavgat_2021']
- primary_population: `burnable_tree_shrub_grass`

## Primary estimand

delta_roc_auc_thermal = regionwise_zscore(thermal).roc_auc - raw_source_only(thermal).roc_auc

## Secondary estimands

- delta_pr_auc_thermal = regionwise_zscore(thermal).pr_auc - raw_source_only(thermal).pr_auc
- delta_roc_auc_coral_minus_raw_thermal
- delta_roc_auc_coral_minus_zscore_thermal
- baseline_model_results (raw/zscore/coral, roc_auc + pr_auc)
- target_within_region_step8b_oof_metric_minus_adapted_transfer_metric

## Adaptation methods (fixed)

### `raw_source_only`
Reuses Step9B's exact preprocessing (build_pipeline: source-fitted median imputer + one-hot encoder) and model fit; no additional transform. Must reproduce Step9B metrics within 1e-6.

### `regionwise_zscore`
z = (x - region_mean) / region_std, computed independently per region.

### `coral_after_regionwise_zscore`
CORAL (Sun & Saenko) applied to numeric features AFTER regionwise z-score. Cs=cov(Xs_z)+lambda*I, Ct=cov(Xt_z)+lambda*I, A=Cs^(-1/2) @ Ct^(1/2) via symmetric eigendecomposition, Xs_coral = Xs_z @ A, Xt_coral = Xt_z (target unchanged).

## Bootstrap

- replicates: 1000
- CI: 2.5/97.5 percentile
- random_state: 42
- min_valid_replicates: 900

## Prohibited actions

- new_regions
- new_feature_subsets
- feature_selection
- hyperparameter_tuning
- new_model_types
- deep_adaptation
- target_label_calibration
- target_label_threshold_fitting
- prediction_inversion
- post_hoc_acceptance_criteria

## Note

This preregistration is IMMUTABLE once created. `--force` may overwrite downstream Step10B-D outputs, but never this file or `analysis_id`. A scientific configuration change requires a new analysis (new output directory), not an overwrite.