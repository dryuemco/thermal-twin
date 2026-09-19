# Burned-pattern audit -- manavgat_2021

analysis_id: `70a8e930cf82d130aced19ea508b0ce5ae7da19c73a5285d9063599dc53daafa`  
created_at: 2026-09-19T09:35:52.907340+00:00  
git_commit: 6d024bc72e8cfc2b6dd8e26e4f7748a15de54fee

## Canonical burned-landcover gate cross-validation

- Gate path: `C:\Users\CORSAIR\projects\thermal-twin\rerun_labelfix\pipeline\outputs\experiments\manavgat_2021\validation\labels\burned_landcover_gate.json`
- Gate SHA-256: `a26dcc5edd24df2cbc7513c4b18521b7a6a8711a91f196a4fe86ed8e08152441`
- Pre-label-burn exclusion rule: 'not_applied'
- Pre-label-excluded cell count: 0
- Cross-validated against audit analysis universe / burned count: True

## Primary population: all_valid_burned

### all_valid_burned

Canonical event-footprint population: Step8A rows that are canonical-analysis-eligible (Step8A 'analysis_eligible' column, i.e. NOT pre-label-burn-excluded -- see resolve_analysis_eligible_mask) with burned == 1 and valid (non-null) row_500m/col_500m grid coordinates. No land-cover restriction. Primary population for component count, patch-size distribution, elevation distribution, and land-cover composition.

- Total input rows: 24150
- Burned-cell count: 3046
- Spatially connected burned-cell components: 1
- Singleton components: 0 (0.0)
- Largest component: 3046 cells (fraction 1.0)
- Second-largest component: 0 cells (fraction 0.0)
- Top-3 components combined fraction: 1.0
- Component-share HHI (sum of squared component shares): 1.0
- Effective component count (1 / HHI): 1.0
- Component size (cells): min=3046, q25=3046.0, median=3046.0, mean=3046.0, q75=3046.0, q90=3046.0, q95=3046.0, max=3046
- Approximate total burned area: 761.5 km^2 (source: core.config.STEP8A_MCD64A1_NATIVE_CELL_SIZE_M (documented as an APPROXIMATION of the true native MCD64A1 sinusoidal-grid cell size, anchored to the Landsat/EPSG:4326 30 m reference predictor grid -- see src/step8a_prepare_500m_modeling_dataset.py module docstring).)

**AOI-edge diagnostics (descriptive only, never used to remove components):**
- Edge-touching components: 0 (0.0)
- Largest component touches edge: False

**Elevation (elevation_mean, burned cells):**
- valid=3046, missing=0, min=10.189586639404297, q05=43.49101543426514, q25=134.6347770690918, median=272.45252990722656, mean=391.5885774386375, q75=588.2844696044922, q95=1043.8276062011719, max=1591.611083984375, iqr=453.6496925354004, range=1581.4214973449707

**Land-cover composition (landcover_dominant, burned cells):**
- Observed classes: 7, dominant: tree_cover (code 10, fraction 0.7619829284307288)

**BurnDate** (descriptive only; never used to split/join/redefine components or to claim distinct-event identification): available, see component_summary.csv for per-component min/max/span/unique_count.

## Sensitivity analysis: burnable_tree_shrub_grass_burned

### burnable_tree_shrub_grass_burned

Natural-vegetation sensitivity population: the corrected primary population further restricted to rows where the existing Step8A 'burnable_tree_shrub_grass' boolean column is True. That frozen Step8A column is a COMBINED per-cell fraction rule -- (landcover_tree_cover_fraction + landcover_shrubland_fraction + landcover_grassland_fraction) >= burnable_threshold (STEP8A_BURNABLE_FRACTION_THRESHOLD) -- already computed in Step8A and reused verbatim here, never recomputed. It is NOT a dominant-land-cover selection: the 'landcover_dominant' column is no part of the selection rule (it is used only for descriptive land-cover composition reporting). A cell therefore qualifies whenever the three fractions SUM to at least the threshold even if its single dominant class is cropland/bare/other, and a cell whose dominant class is tree, shrubland or grassland is excluded if that sum falls below the threshold. Reported as a sensitivity analysis, never substituted for the primary population.

- Total input rows: 24150
- Burned-cell count: 2935
- Spatially connected burned-cell components: 2
- Singleton components: 1 (0.5)
- Largest component: 2934 cells (fraction 0.9996592844974447)
- Second-largest component: 1 cells (fraction 0.00034071550255536625)
- Top-3 components combined fraction: 1.0
- Component-share HHI (sum of squared component shares): 0.9993188011689966
- Effective component count (1 / HHI): 1.0006816631791642
- Component size (cells): min=1, q25=734.25, median=1467.5, mean=1467.5, q75=2200.75, q90=2640.7, q95=2787.35, max=2934
- Approximate total burned area: 733.75 km^2 (source: core.config.STEP8A_MCD64A1_NATIVE_CELL_SIZE_M (documented as an APPROXIMATION of the true native MCD64A1 sinusoidal-grid cell size, anchored to the Landsat/EPSG:4326 30 m reference predictor grid -- see src/step8a_prepare_500m_modeling_dataset.py module docstring).)

**AOI-edge diagnostics (descriptive only, never used to remove components):**
- Edge-touching components: 0 (0.0)
- Largest component touches edge: False

**Elevation (elevation_mean, burned cells):**
- valid=2935, missing=0, min=10.189586639404297, q05=51.541093063354495, q25=147.26025390625, median=286.5644836425781, mean=403.85461699861077, q75=599.9353332519531, q95=1050.2953369140616, max=1591.611083984375, iqr=452.6750793457031, range=1581.4214973449707

**Land-cover composition (landcover_dominant, burned cells):**
- Observed classes: 6, dominant: tree_cover (code 10, fraction 0.7908006814310051)

**BurnDate** (descriptive only; never used to split/join/redefine components or to claim distinct-event identification): available, see component_summary.csv for per-component min/max/span/unique_count.

## Final-model-population comparison: burnable_tree_shrub_grass_valid_for_modeling_burned

### burnable_tree_shrub_grass_valid_for_modeling_burned

Advisor-specific final-model-population morphology comparison. Selection contract, all conditions required simultaneously: analysis_eligible == True AND valid_for_modeling == True AND burnable_tree_shrub_grass == True AND burned == 1 AND non-null row_500m/col_500m. Both Step8A boolean columns are reused verbatim and never recomputed here (see the burnable_tree_shrub_grass_burned definition for the combined fraction rule behind 'burnable_tree_shrub_grass'). This population describes the morphology of the rows that actually reach the final model; it is an ADDITIONAL comparison only and does NOT replace, redefine, or otherwise alter the 'all_valid_burned' primary population or the 'burnable_tree_shrub_grass_burned' sensitivity population.

- Total input rows: 24150
- Burned-cell count: 2935
- Spatially connected burned-cell components: 2
- Singleton components: 1 (0.5)
- Largest component: 2934 cells (fraction 0.9996592844974447)
- Second-largest component: 1 cells (fraction 0.00034071550255536625)
- Top-3 components combined fraction: 1.0
- Component-share HHI (sum of squared component shares): 0.9993188011689966
- Effective component count (1 / HHI): 1.0006816631791642
- Component size (cells): min=1, q25=734.25, median=1467.5, mean=1467.5, q75=2200.75, q90=2640.7, q95=2787.35, max=2934
- Approximate total burned area: 733.75 km^2 (source: core.config.STEP8A_MCD64A1_NATIVE_CELL_SIZE_M (documented as an APPROXIMATION of the true native MCD64A1 sinusoidal-grid cell size, anchored to the Landsat/EPSG:4326 30 m reference predictor grid -- see src/step8a_prepare_500m_modeling_dataset.py module docstring).)

**AOI-edge diagnostics (descriptive only, never used to remove components):**
- Edge-touching components: 0 (0.0)
- Largest component touches edge: False

**Elevation (elevation_mean, burned cells):**
- valid=2935, missing=0, min=10.189586639404297, q05=51.541093063354495, q25=147.26025390625, median=286.5644836425781, mean=403.85461699861077, q75=599.9353332519531, q95=1050.2953369140616, max=1591.611083984375, iqr=452.6750793457031, range=1581.4214973449707

**Land-cover composition (landcover_dominant, burned cells):**
- Observed classes: 6, dominant: tree_cover (code 10, fraction 0.7908006814310051)

**BurnDate** (descriptive only; never used to split/join/redefine components or to claim distinct-event identification): available, see component_summary.csv for per-component min/max/span/unique_count.

## Limitations

- Connected components are a spatial fragmentation proxy. They must not be interpreted as a definitive count of independent wildfire events, because one event may appear as multiple disconnected components and multiple events may be spatially connected at the analysis resolution.
- Connected-component count is resolution-dependent (8-neighbour adjacency on the fixed 500 m Step8A grid); a coarser or finer grid would yield a different count for the same physical burned area.
- Results are sensitive to AOI clipping: a component that would be contiguous in a wider AOI can appear split, or vice versa, purely because of where the analysis extent was drawn.
- MCD64A1-scale cells are approximate spatial units, not exact ground-truth footprints (see CELL_AREA_KM2_SOURCE provenance).
- Component count is not a definitive fire-event count.
- Results are descriptive and do not explain cross-region transfer performance causally.
