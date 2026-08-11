# Burned-pattern audit -- mugla_2022_event_relative

analysis_id: `5c5e9b3d2aebdd838dbea975f0eabedba4b08670856cb3d4094182e4baf7f849`  
created_at: 2026-08-09T11:48:58.487777+00:00  
git_commit: a07ea33743f4e45963e52c50e706683f1eee164d

## Canonical burned-landcover gate cross-validation

- Gate path: `/home/emrehan-metin/satellite-thermal-digital-twin/outputs/experiments/mugla_2022_event_relative/validation/labels/burned_landcover_gate.json`
- Gate SHA-256: `a307cceaac22fa5e194fa6251e84e1d5a63950c8fcf1a1a0a506264038eb2008`
- Pre-label-burn exclusion rule: 'valid nonzero BurnDate calendar date < label_start (2022-06-21)'
- Pre-label-excluded cell count: 0
- Cross-validated against audit analysis universe / burned count: True

## Primary population: all_valid_burned

### all_valid_burned

Canonical event-footprint population: Step8A rows that are canonical-analysis-eligible (Step8A 'analysis_eligible' column, i.e. NOT pre-label-burn-excluded -- see resolve_analysis_eligible_mask) with burned == 1 and valid (non-null) row_500m/col_500m grid coordinates. No land-cover restriction. Primary population for component count, patch-size distribution, elevation distribution, and land-cover composition.

- Total input rows: 73098
- Burned-cell count: 332
- Spatially connected burned-cell components: 2
- Singleton components: 0 (0.0)
- Largest component: 282 cells (fraction 0.8493975903614458)
- Second-largest component: 50 cells (fraction 0.15060240963855423)
- Top-3 components combined fraction: 1.0
- Component-share HHI (sum of squared component shares): 0.7441573523007694
- Effective component count (1 / HHI): 1.343801814103189
- Component size (cells): min=50, q25=108.0, median=166.0, mean=166.0, q75=224.0, q90=258.8, q95=270.4, max=282
- Approximate total burned area: 83.0 km^2 (source: core.config.STEP8A_MCD64A1_NATIVE_CELL_SIZE_M (documented as an APPROXIMATION of the true native MCD64A1 sinusoidal-grid cell size, anchored to the Landsat/EPSG:4326 30 m reference predictor grid -- see src/step8a_prepare_500m_modeling_dataset.py module docstring).)

**AOI-edge diagnostics (descriptive only, never used to remove components):**
- Edge-touching components: 0 (0.0)
- Largest component touches edge: False

**Elevation (elevation_mean, burned cells):**
- valid=332, missing=0, min=15.509711265563965, q05=50.046105575561526, q25=117.61468887329102, median=187.44332122802734, mean=211.59281489073513, q75=274.08702850341797, q95=446.2915939331052, max=777.0230102539062, iqr=156.47233963012695, range=761.5132989883423

**Land-cover composition (landcover_dominant, burned cells):**
- Observed classes: 2, dominant: tree_cover (code 10, fraction 0.9789156626506024)

**BurnDate** (descriptive only; never used to split/join/redefine components or to claim distinct-event identification): available, see component_summary.csv for per-component min/max/span/unique_count.

## Sensitivity analysis: burnable_tree_shrub_grass_burned

### burnable_tree_shrub_grass_burned

Natural-vegetation sensitivity population: the corrected primary population further restricted to rows where the existing Step8A 'burnable_tree_shrub_grass' boolean column is True. That frozen Step8A column is a COMBINED per-cell fraction rule -- (landcover_tree_cover_fraction + landcover_shrubland_fraction + landcover_grassland_fraction) >= burnable_threshold (STEP8A_BURNABLE_FRACTION_THRESHOLD) -- already computed in Step8A and reused verbatim here, never recomputed. It is NOT a dominant-land-cover selection: the 'landcover_dominant' column is no part of the selection rule (it is used only for descriptive land-cover composition reporting). A cell therefore qualifies whenever the three fractions SUM to at least the threshold even if its single dominant class is cropland/bare/other, and a cell whose dominant class is tree, shrubland or grassland is excluded if that sum falls below the threshold. Reported as a sensitivity analysis, never substituted for the primary population.

- Total input rows: 73098
- Burned-cell count: 332
- Spatially connected burned-cell components: 2
- Singleton components: 0 (0.0)
- Largest component: 282 cells (fraction 0.8493975903614458)
- Second-largest component: 50 cells (fraction 0.15060240963855423)
- Top-3 components combined fraction: 1.0
- Component-share HHI (sum of squared component shares): 0.7441573523007694
- Effective component count (1 / HHI): 1.343801814103189
- Component size (cells): min=50, q25=108.0, median=166.0, mean=166.0, q75=224.0, q90=258.8, q95=270.4, max=282
- Approximate total burned area: 83.0 km^2 (source: core.config.STEP8A_MCD64A1_NATIVE_CELL_SIZE_M (documented as an APPROXIMATION of the true native MCD64A1 sinusoidal-grid cell size, anchored to the Landsat/EPSG:4326 30 m reference predictor grid -- see src/step8a_prepare_500m_modeling_dataset.py module docstring).)

**AOI-edge diagnostics (descriptive only, never used to remove components):**
- Edge-touching components: 0 (0.0)
- Largest component touches edge: False

**Elevation (elevation_mean, burned cells):**
- valid=332, missing=0, min=15.509711265563965, q05=50.046105575561526, q25=117.61468887329102, median=187.44332122802734, mean=211.59281489073513, q75=274.08702850341797, q95=446.2915939331052, max=777.0230102539062, iqr=156.47233963012695, range=761.5132989883423

**Land-cover composition (landcover_dominant, burned cells):**
- Observed classes: 2, dominant: tree_cover (code 10, fraction 0.9789156626506024)

**BurnDate** (descriptive only; never used to split/join/redefine components or to claim distinct-event identification): available, see component_summary.csv for per-component min/max/span/unique_count.

## Final-model-population comparison: burnable_tree_shrub_grass_valid_for_modeling_burned

### burnable_tree_shrub_grass_valid_for_modeling_burned

Advisor-specific final-model-population morphology comparison. Selection contract, all conditions required simultaneously: analysis_eligible == True AND valid_for_modeling == True AND burnable_tree_shrub_grass == True AND burned == 1 AND non-null row_500m/col_500m. Both Step8A boolean columns are reused verbatim and never recomputed here (see the burnable_tree_shrub_grass_burned definition for the combined fraction rule behind 'burnable_tree_shrub_grass'). This population describes the morphology of the rows that actually reach the final model; it is an ADDITIONAL comparison only and does NOT replace, redefine, or otherwise alter the 'all_valid_burned' primary population or the 'burnable_tree_shrub_grass_burned' sensitivity population.

- Total input rows: 73098
- Burned-cell count: 331
- Spatially connected burned-cell components: 2
- Singleton components: 0 (0.0)
- Largest component: 282 cells (fraction 0.851963746223565)
- Second-largest component: 49 cells (fraction 0.14803625377643503)
- Top-3 components combined fraction: 1.0
- Component-share HHI (sum of squared component shares): 0.747756957311452
- Effective component count (1 / HHI): 1.3373329264571256
- Component size (cells): min=49, q25=107.25, median=165.5, mean=165.5, q75=223.75, q90=258.7, q95=270.34999999999997, max=282
- Approximate total burned area: 82.75 km^2 (source: core.config.STEP8A_MCD64A1_NATIVE_CELL_SIZE_M (documented as an APPROXIMATION of the true native MCD64A1 sinusoidal-grid cell size, anchored to the Landsat/EPSG:4326 30 m reference predictor grid -- see src/step8a_prepare_500m_modeling_dataset.py module docstring).)

**AOI-edge diagnostics (descriptive only, never used to remove components):**
- Edge-touching components: 0 (0.0)
- Largest component touches edge: False

**Elevation (elevation_mean, burned cells):**
- valid=331, missing=0, min=15.509711265563965, q05=50.0146484375, q25=117.5499038696289, median=187.43203735351562, mean=210.03516242439292, q75=273.1589050292969, q95=437.4031677246094, max=777.0230102539062, iqr=155.60900115966797, range=761.5132989883423

**Land-cover composition (landcover_dominant, burned cells):**
- Observed classes: 2, dominant: tree_cover (code 10, fraction 0.9788519637462235)

**BurnDate** (descriptive only; never used to split/join/redefine components or to claim distinct-event identification): available, see component_summary.csv for per-component min/max/span/unique_count.

## Limitations

- Connected components are a spatial fragmentation proxy. They must not be interpreted as a definitive count of independent wildfire events, because one event may appear as multiple disconnected components and multiple events may be spatially connected at the analysis resolution.
- Connected-component count is resolution-dependent (8-neighbour adjacency on the fixed 500 m Step8A grid); a coarser or finer grid would yield a different count for the same physical burned area.
- Results are sensitive to AOI clipping: a component that would be contiguous in a wider AOI can appear split, or vice versa, purely because of where the analysis extent was drawn.
- MCD64A1-scale cells are approximate spatial units, not exact ground-truth footprints (see CELL_AREA_KM2_SOURCE provenance).
- Component count is not a definitive fire-event count.
- Results are descriptive and do not explain cross-region transfer performance causally.
