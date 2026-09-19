# Burned-Landcover Gate (Step6B)

Diagnostic gate: summarizes the landcover composition of MCD64A1-burned ~500 m cells (`gate_level = 500m_reconstructed_mcd64a1_cell`). This does NOT train a model and does NOT stop the pipeline on a cropland-dominated result.

**Decision: `wildfire_candidate_pass`**

Reason: burned_tree_shrub_grass_count/burned_count=0.955 >= natural_threshold=0.5.

## Counts

| Metric | Value |
|---|---|
| total_valid_cells_or_pixels_considered | 24150 |
| burned_count | 3046 |
| unburned_count | 21104 |
| burned_tree_cover_count | 2321 |
| burned_shrubland_count | 28 |
| burned_grassland_count | 561 |
| burned_cropland_count | 54 |
| burned_tree_shrub_grass_count | 2910 |
| burned_tree_shrub_count | 2349 |
| burned_cropland_dominant_count | 54 |

## Fractions (denominator = burned_count)

| Metric | Value |
|---|---|
| burned_natural_vegetation_fraction | 0.9554 |
| burned_cropland_fraction | 0.0177 |
| burned_tree_shrub_fraction | 0.7712 |

## Burned cells: dominant landcover breakdown

| Dominant class | Burned cell count |
|---|---|
| tree_cover | 2321 |
| grassland | 561 |
| permanent_water | 80 |
| cropland | 54 |
| shrubland | 28 |
| bare_sparse_vegetation | 1 |
| built_up | 1 |

**downstream_authorized: `False`** (passing the gate does NOT authorize predictor/Step7/Step8/Step9/Step10; advisor review required).

## Thresholds used

- min_positives: 30
- natural_threshold: 0.5
- cropland_threshold: 0.5

## Inputs

- label_path: `C:\Users\CORSAIR\projects\thermal-twin\rerun_labelfix\pipeline\outputs\experiments\manavgat_2021\validation\labels\mcd64a1_raw.tif`
- aligned_label_path: `C:\Users\CORSAIR\projects\thermal-twin\rerun_labelfix\pipeline\outputs\experiments\manavgat_2021\validation\labels\mcd64a1_raw.tif`
- reference_path: `C:\Users\CORSAIR\projects\thermal-twin\rerun_labelfix\pipeline\outputs\experiments\manavgat_2021\gate_inputs\reference_30m.tif`
- landcover_path: `C:\Users\CORSAIR\projects\thermal-twin\rerun_labelfix\pipeline\outputs\experiments\manavgat_2021\gate_inputs\landcover_esa_worldcover_v200_aligned_to_reference.tif`
- label_start: `2021-07-28`
- label_end: `2021-08-31`
- predictor_start: `None`
- predictor_end: `None`
- pre_label_label_path: `None`
- aligned_pre_label_path: `None`
