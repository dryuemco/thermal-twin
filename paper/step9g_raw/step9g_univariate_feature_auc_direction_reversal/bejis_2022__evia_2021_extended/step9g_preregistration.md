# Step9G Univariate Feature-AUC Direction-Reversal Preregistration -- IMMUTABLE

- analysis_id: `ea95fd9ae0804091112afe2bdeabc0681fb889a06ca97b9eb7f0b6b94d6acb35`
- created_at: 2026-07-28T08:50:24.872930+00:00
- experiments: ['bejis_2022', 'evia_2021_extended']
- primary population: burnable_tree_shrub_grass
- target: burned
- numeric features (fixed order): ['ndvi_mean', 'elevation_mean', 'slope_mean', 'lst_anomaly_mean', 'current_lst_mean', 'current_tvdi_mean', 'tvdi_difference_mean', 'downscaled_lst_mean', 'fused_lst_mean']
- block size: 10 cells (approximately_5_km), origin (0, 0)
- bootstrap: 1000 replicates, seed 42, 2.5/97.5 percentile CI, min valid 900

Raw feature values are passed directly to ROC-AUC; AUC below 0.5 is a direction, never inverted or relabeled as poor performance. No feature list, population, block scale, or status rule changes after results.
