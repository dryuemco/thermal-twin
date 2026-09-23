# Step8C: Spatial-Block Bootstrap Uncertainty for Step8B Delta Metrics

## What this step does

- Step8C estimates **uncertainty** for Step8B's `delta_auc` / `delta_pr_auc` point estimates using a **spatial-block bootstrap** over the same 500 m spatial blocks used for Step8B's cross-validation.
- It does **not retrain any model** -- it reuses Step8B's existing out-of-fold predictions.
- It does **not use 30 m pixels** (samples are Step8A's 500 m cells, inherited unchanged from Step8B).
- It does **not use FIRMS** anywhere.
- It does **not report a classical p-value or formal statistical significance** -- only whether the 95% bootstrap percentile interval excludes zero ("bootstrap-supported positive delta") or not ("point estimate positive but CI overlaps zero").

## Main result

- **all_valid** (point estimate delta_auc=`+0.0565`, delta_pr_auc=`+0.1658`): delta_auc 95% bootstrap CI=`[+0.0513, +0.0621]` -> **bootstrap-supported positive delta**; delta_pr_auc 95% bootstrap CI=`[+0.1453, +0.1855]` -> **bootstrap-supported positive delta** (n_bootstrap_successful=1000)
- **cropland_dominant** (point estimate delta_auc=`+0.0054`, delta_pr_auc=`-0.0662`): delta_auc 95% bootstrap CI=`[-0.0300, +0.0322]` -> **point estimate positive but CI overlaps zero**; delta_pr_auc 95% bootstrap CI=`[-0.1854, +0.0337]` -> **point estimate negative but CI overlaps zero** (n_bootstrap_successful=1000)

## Monthly lead-time bootstrap CI (existing OOF predictions, no monthly models trained)

- **all_valid**:
  - august (n_pos=686): delta_auc CI95=`[+0.0605, +0.0804]` (positive_bootstrap_support)
  - september: unavailable (positives (0) < min_month_positives (10))
  - october: unavailable (positives (0) < min_month_positives (10))
- **cropland_dominant**:
  - august: unavailable (positives (0) < min_month_positives (10))
  - september: unavailable (positives (0) < min_month_positives (10))
  - october: unavailable (positives (0) < min_month_positives (10))
- **burnable_tree_shrub_grass**:
  - august (n_pos=684): delta_auc CI95=`[+0.0659, +0.0895]` (positive_bootstrap_support)
  - september: unavailable (positives (0) < min_month_positives (10))
  - october: unavailable (positives (0) < min_month_positives (10))
- **burnable_tree_shrub**:
  - august (n_pos=618): delta_auc CI95=`[+0.0864, +0.1174]` (positive_bootstrap_support)
  - september: unavailable (positives (0) < min_month_positives (10))
  - october: unavailable (positives (0) < min_month_positives (10))

## Gap-fill sensitivity bootstrap (existing predictions only, no retraining)

- **all_valid**:
  - no_filter (n_rows=24087): delta_auc CI95=`[+0.0510, +0.0621]` (positive_bootstrap_support)
  - lt_0.25 (n_rows=23305): delta_auc CI95=`[+0.0526, +0.0639]` (positive_bootstrap_support)
  - lt_0.50 (n_rows=23680): delta_auc CI95=`[+0.0514, +0.0627]` (positive_bootstrap_support)
- **cropland_dominant**:
  - no_filter (n_rows=1260): delta_auc CI95=`[-0.0260, +0.0317]` (uncertain)
  - lt_0.25 (n_rows=1260): delta_auc CI95=`[-0.0262, +0.0337]` (uncertain)
  - lt_0.50 (n_rows=1260): delta_auc CI95=`[-0.0234, +0.0332]` (uncertain)

## Method

- Resampling unit: `spatial_block_id` (NOT individual rows). Each bootstrap iteration draws spatial blocks **with replacement**; if a block is drawn more than once, all of its rows are repeated that many times in the bootstrap sample.
- Bootstrap iterations where the resampled data contains only one class (`burned` all 0 or all 1) are skipped and excluded from the percentile/CI calculation (but recorded in `step8c_bootstrap_samples.csv` with `skipped=True`).

Full metrics: `step8c_bootstrap_metrics.json`

## Warnings

- all_valid: October burn_month positives are low (n=0 < 10); monthly October bootstrap CI unavailable.
- cropland_dominant: October burn_month positives are low (n=0 < 10); monthly October bootstrap CI unavailable.
- burnable_tree_shrub_grass: October burn_month positives are low (n=0 < 10); monthly October bootstrap CI unavailable.
- burnable_tree_shrub: October burn_month positives are low (n=0 < 10); monthly October bootstrap CI unavailable.
