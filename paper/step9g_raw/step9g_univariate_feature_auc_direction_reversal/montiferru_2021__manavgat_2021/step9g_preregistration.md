# Step9G Univariate Feature-AUC Direction-Reversal Preregistration -- IMMUTABLE

- analysis_id: `b4e9cc7d61bbe457a8c4ab75360d2ee284572937056d2680b8d2638f86f752f0`
- created_at: 2026-08-05T13:28:05.171091+00:00
- experiments: ['montiferru_2021', 'manavgat_2021']
- primary population: burnable_tree_shrub_grass
- target: burned
- numeric features (fixed order): ['ndvi_mean', 'elevation_mean', 'slope_mean', 'lst_anomaly_mean', 'current_lst_mean', 'current_tvdi_mean', 'tvdi_difference_mean', 'downscaled_lst_mean', 'fused_lst_mean']
- block size: 10 cells (approximately_5_km), origin (0, 0)
- bootstrap: 1000 replicates, seed 42, 2.5/97.5 percentile CI, min valid 900

Raw feature values are passed directly to ROC-AUC; AUC below 0.5 is a direction, never inverted or relabeled as poor performance. No feature list, population, block scale, or status rule changes after results.
