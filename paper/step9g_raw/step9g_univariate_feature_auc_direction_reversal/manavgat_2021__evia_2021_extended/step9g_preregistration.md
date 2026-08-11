# Step9G Univariate Feature-AUC Direction-Reversal Preregistration -- IMMUTABLE

- analysis_id: `166bc656dd9abf35e463437b77bb3d146f8c079178b0c8a744282dd2e8244c28`
- created_at: 2026-07-28T13:33:27.105782+00:00
- experiments: ['manavgat_2021', 'evia_2021_extended']
- primary population: burnable_tree_shrub_grass
- target: burned
- numeric features (fixed order): ['ndvi_mean', 'elevation_mean', 'slope_mean', 'lst_anomaly_mean', 'current_lst_mean', 'current_tvdi_mean', 'tvdi_difference_mean', 'downscaled_lst_mean', 'fused_lst_mean']
- block size: 10 cells (approximately_5_km), origin (0, 0)
- bootstrap: 1000 replicates, seed 42, 2.5/97.5 percentile CI, min valid 900

Raw feature values are passed directly to ROC-AUC; AUC below 0.5 is a direction, never inverted or relabeled as poor performance. No feature list, population, block scale, or status rule changes after results.
