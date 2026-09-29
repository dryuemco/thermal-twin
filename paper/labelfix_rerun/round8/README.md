# Round 8: analyses added in response to the pre-submission review

All scripts run from the repository root with the environment in `ENVIRONMENT.md`, read the modelling
datasets through `paper/code/_canonical.py` (SHA-256 checked) and write only into this folder.

| Script | Question | Main outputs |
|---|---|---|
| `r8a_seed_replication.py` | Do the transfer results depend on the random-forest seed? Ten seeds, study areas as drawn and 10 km collar, both feature sets. Seed 42 reproduces the published matrix exactly. | `r8a_seed_auc.csv`, `r8a_summary.json`, `r8a_preds_full_seed42.npz` |
| `r8c_coral_variants.py` | CORAL with λ = 1, CORAL on two thermal principal components, and a placebo CORAL that aligns the source with a third region instead of the target. | `r8c_coral_variants.csv`, `r8c_summary.json` |
| `r8d_similarity_permutation.py` | Permutation (QAP) p-values for the twenty similarity measures; results without Manavgat; equivalence test of the as-drawn transfer gain under all resampling units. | `r8d_similarity_permutation.csv`, `r8d_summary.json` |
| `r8e_stratified_intervals.py` | Spatial-block bootstrap intervals for the stratified associations of Table S27. | `r8e_stratified_intervals.csv` |
| `r8b_buffered_within.py` | Capture of burned cells by within-region models; Bejís without the 48 cells that burned in the predictor window. | `r8b_summary.json` |
| `r8i_worldcover2020_fetch.py` | Fetches WorldCover v100 (2020) and v200 on each region's 30 m grid and aggregates them to the cells as step8a does. Needs Earth Engine and the gate-input rasters; v200 reproduces the pipeline exactly. | `r8i_worldcover_cells.csv.gz`, `r8i_fetch_summary.json` |
| `r8j_worldcover2020_effect.py` | Population, gate and model results with the 2020 map. | `r8j_summary.json`, `r8j_transfer_2020_vs_2021.csv` |
| `r8k_labels_aspect_fetch.py` | Fetches VIIRS VNP64A1 and MODIS MCD64A1 labels, aspect (northness, eastness) and Landsat 8 observation counts on the pipeline grid. MCD64A1 reproduces the dataset labels exactly. Needs Earth Engine. | `r8k_cells.csv.gz`, `r8k_landsat_observations.csv`, `r8k_fetch_summary.json` |
| `r8m_labels_aspect_effect.py` | Label agreement and model results with VNP64A1; thermal gain and LST sign with aspect. | `r8m_summary.json`, `r8m_transfer_vnp_vs_mcd.csv` |
| `r8n_aspect_gain_intervals.py` | Bootstrap intervals of the within-region gain with and without aspect. | `r8n_summary.json` |
| `r8l_statistics.py` | Crossed random effects, residual correlogram, fold-averaged AUC, PR lift, estimator intervals. | `r8l_summary.json` |
| `r8o_era5_descriptive.py` | Thermal channels against ERA5-Land weather anomalies, region level. | `r8o_summary.json` |
| `r8g_capture.py` | Capture of burned cells in the top 10 % and 20 % of transferred scores. | `r8g_capture_transfer.csv`, `r8g_summary.json` |

**A design that was tried and not used.** `r8b_buffered_within.py` also computes a leave-one-block-out
within-region reference (40-cell blocks, with and without a 10 km buffer). Its pooled ROC-AUC combines
predictions from different models, and because burned cells sit in one or two blocks, the pooled value
is dominated by calibration differences between these models (for example 0.054 in Bejís). It is
therefore not a valid reference and is not reported in the paper. The distance curve of Section S1.18,
which scores one model, answers the same question.
