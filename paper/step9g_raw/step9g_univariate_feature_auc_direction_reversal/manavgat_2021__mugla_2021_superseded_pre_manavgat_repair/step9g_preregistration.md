# Step9G Univariate Feature-AUC Direction-Reversal Preregistration -- IMMUTABLE

- analysis_id: `e8cef4bcf7b05ef55003fe89f0f89147ea61ac5e9aaa34cb412723dfd24abb89`
- created_at: 2026-07-21T10:37:43.782334+00:00
- experiments: ['manavgat_2021', 'mugla_2021']
- primary population: burnable_tree_shrub_grass
- target: burned
- numeric features (fixed order): ['ndvi_mean', 'elevation_mean', 'slope_mean', 'lst_anomaly_mean', 'current_lst_mean', 'current_tvdi_mean', 'tvdi_difference_mean', 'downscaled_lst_mean', 'fused_lst_mean']
- block size: 10 cells (approximately_5_km), origin (0, 0)
- bootstrap: 1000 replicates, seed 42, 2.5/97.5 percentile CI, min valid 900

Raw feature values are passed directly to ROC-AUC; AUC below 0.5 is a direction, never inverted or relabeled as poor performance. No feature list, population, block scale, or status rule changes after results.
