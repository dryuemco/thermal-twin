# Multi-AOI burned-pattern comparison

analysis_id: `e23db6963806b2f708b4c8d8b1de494feb90ba6e5ca758f7073369b13453ee3b` (order-invariant)  
created_at: 2026-08-09T11:48:58.515988+00:00  
selection_mode: explicit  
requested_experiment_ids: ['mugla_2021', 'mugla_2022_event_relative']  
resolved_experiment_ids: ['mugla_2021', 'mugla_2022_event_relative']  
allow_superseded_sensitivity: False  
superseded_pairs: []

## mugla_2021

Canonical burned-landcover gate cross-validated: `/home/emrehan-metin/satellite-thermal-digital-twin/outputs/experiments/mugla_2021/validation/labels/burned_landcover_gate.json` (sha256 acadc06206952d9ca4a9effd9b1262bff00e057bbc4442f0cc1f1078855322bc); pre-label-excluded cells: 49; exclusion rule: 'valid nonzero BurnDate calendar date < label_start (2021-07-29)'.

### all_valid_burned (primary)

Canonical event-footprint population: Step8A rows that are canonical-analysis-eligible (Step8A 'analysis_eligible' column, i.e. NOT pre-label-burn-excluded -- see resolve_analysis_eligible_mask) with burned == 1 and valid (non-null) row_500m/col_500m grid coordinates. No land-cover restriction. Primary population for component count, patch-size distribution, elevation distribution, and land-cover composition.

- Total input rows: 73098
- Burned-cell count: 3026
- Spatially connected burned-cell components: 9
- Singleton components: 0 (0.0)
- Largest component: 969 cells (fraction 0.3202247191011236)
- Second-largest component: 741 cells (fraction 0.24487772637144745)
- Top-3 components combined fraction: 0.786186384666226
- Component-share HHI (sum of squared component shares): 0.24442472355688896
- Effective component count (1 / HHI): 4.091239157184742
- Component size (cells): min=11, q25=18.0, median=29.0, mean=336.22222222222223, q75=669.0, q90=786.6, q95=877.8, max=969
- Approximate total burned area: 756.5 km^2 (source: core.config.STEP8A_MCD64A1_NATIVE_CELL_SIZE_M (documented as an APPROXIMATION of the true native MCD64A1 sinusoidal-grid cell size, anchored to the Landsat/EPSG:4326 30 m reference predictor grid -- see src/step8a_prepare_500m_modeling_dataset.py module docstring).)

**AOI-edge diagnostics (descriptive only, never used to remove components):**
- Edge-touching components: 2 (0.2222222222222222)
- Largest component touches edge: False

**Elevation (elevation_mean, burned cells):**
- valid=3026, missing=0, min=0.0, q05=34.974090576171875, q25=245.4825325012207, median=539.2785949707031, mean=652.5278950425184, q75=1054.6731872558594, q95=1521.1829528808594, max=1974.5574951171875, iqr=809.1906547546387, range=1974.5574951171875

**Land-cover composition (landcover_dominant, burned cells):**
- Observed classes: 7, dominant: tree_cover (code 10, fraction 0.8896232650363516)

**BurnDate** (descriptive only; never used to split/join/redefine components or to claim distinct-event identification): available, see component_summary.csv for per-component min/max/span/unique_count.

### burnable_tree_shrub_grass_burned (sensitivity)

Natural-vegetation sensitivity population: the corrected primary population further restricted to rows where the existing Step8A 'burnable_tree_shrub_grass' boolean column is True. That frozen Step8A column is a COMBINED per-cell fraction rule -- (landcover_tree_cover_fraction + landcover_shrubland_fraction + landcover_grassland_fraction) >= burnable_threshold (STEP8A_BURNABLE_FRACTION_THRESHOLD) -- already computed in Step8A and reused verbatim here, never recomputed. It is NOT a dominant-land-cover selection: the 'landcover_dominant' column is no part of the selection rule (it is used only for descriptive land-cover composition reporting). A cell therefore qualifies whenever the three fractions SUM to at least the threshold even if its single dominant class is cropland/bare/other, and a cell whose dominant class is tree, shrubland or grassland is excluded if that sum falls below the threshold. Reported as a sensitivity analysis, never substituted for the primary population.

- Total input rows: 73098
- Burned-cell count: 2911
- Spatially connected burned-cell components: 10
- Singleton components: 1 (0.1)
- Largest component: 914 cells (fraction 0.31398144967365166)
- Second-largest component: 738 cells (fraction 0.2535211267605634)
- Top-3 components combined fraction: 0.7870147715561663
- Component-share HHI (sum of squared component shares): 0.24664131279958829
- Effective component count (1 / HHI): 4.054470796676968
- Component size (cells): min=1, q25=11.0, median=22.5, mean=291.1, q75=616.25, q90=755.5999999999999, q95=834.7999999999998, max=914
- Approximate total burned area: 727.75 km^2 (source: core.config.STEP8A_MCD64A1_NATIVE_CELL_SIZE_M (documented as an APPROXIMATION of the true native MCD64A1 sinusoidal-grid cell size, anchored to the Landsat/EPSG:4326 30 m reference predictor grid -- see src/step8a_prepare_500m_modeling_dataset.py module docstring).)

**AOI-edge diagnostics (descriptive only, never used to remove components):**
- Edge-touching components: 2 (0.2)
- Largest component touches edge: False

**Elevation (elevation_mean, burned cells):**
- valid=2911, missing=0, min=1.621870517730713, q05=84.3343620300293, q25=267.44482421875, median=563.0870361328125, mean=676.69252126506, q75=1075.4190063476562, q95=1525.7365112304688, max=1974.5574951171875, iqr=807.9741821289062, range=1972.9356245994568

**Land-cover composition (landcover_dominant, burned cells):**
- Observed classes: 7, dominant: tree_cover (code 10, fraction 0.9247681209206459)

**BurnDate** (descriptive only; never used to split/join/redefine components or to claim distinct-event identification): available, see component_summary.csv for per-component min/max/span/unique_count.

### burnable_tree_shrub_grass_valid_for_modeling_burned (final-model population)

Advisor-specific final-model-population morphology comparison. Selection contract, all conditions required simultaneously: analysis_eligible == True AND valid_for_modeling == True AND burnable_tree_shrub_grass == True AND burned == 1 AND non-null row_500m/col_500m. Both Step8A boolean columns are reused verbatim and never recomputed here (see the burnable_tree_shrub_grass_burned definition for the combined fraction rule behind 'burnable_tree_shrub_grass'). This population describes the morphology of the rows that actually reach the final model; it is an ADDITIONAL comparison only and does NOT replace, redefine, or otherwise alter the 'all_valid_burned' primary population or the 'burnable_tree_shrub_grass_burned' sensitivity population.

- Total input rows: 73098
- Burned-cell count: 2911
- Spatially connected burned-cell components: 10
- Singleton components: 1 (0.1)
- Largest component: 914 cells (fraction 0.31398144967365166)
- Second-largest component: 738 cells (fraction 0.2535211267605634)
- Top-3 components combined fraction: 0.7870147715561663
- Component-share HHI (sum of squared component shares): 0.24664131279958829
- Effective component count (1 / HHI): 4.054470796676968
- Component size (cells): min=1, q25=11.0, median=22.5, mean=291.1, q75=616.25, q90=755.5999999999999, q95=834.7999999999998, max=914
- Approximate total burned area: 727.75 km^2 (source: core.config.STEP8A_MCD64A1_NATIVE_CELL_SIZE_M (documented as an APPROXIMATION of the true native MCD64A1 sinusoidal-grid cell size, anchored to the Landsat/EPSG:4326 30 m reference predictor grid -- see src/step8a_prepare_500m_modeling_dataset.py module docstring).)

**AOI-edge diagnostics (descriptive only, never used to remove components):**
- Edge-touching components: 2 (0.2)
- Largest component touches edge: False

**Elevation (elevation_mean, burned cells):**
- valid=2911, missing=0, min=1.621870517730713, q05=84.3343620300293, q25=267.44482421875, median=563.0870361328125, mean=676.69252126506, q75=1075.4190063476562, q95=1525.7365112304688, max=1974.5574951171875, iqr=807.9741821289062, range=1972.9356245994568

**Land-cover composition (landcover_dominant, burned cells):**
- Observed classes: 7, dominant: tree_cover (code 10, fraction 0.9247681209206459)

**BurnDate** (descriptive only; never used to split/join/redefine components or to claim distinct-event identification): available, see component_summary.csv for per-component min/max/span/unique_count.

## mugla_2022_event_relative

Canonical burned-landcover gate cross-validated: `/home/emrehan-metin/satellite-thermal-digital-twin/outputs/experiments/mugla_2022_event_relative/validation/labels/burned_landcover_gate.json` (sha256 a307cceaac22fa5e194fa6251e84e1d5a63950c8fcf1a1a0a506264038eb2008); pre-label-excluded cells: 0; exclusion rule: 'valid nonzero BurnDate calendar date < label_start (2022-06-21)'.

### all_valid_burned (primary)

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

### burnable_tree_shrub_grass_burned (sensitivity)

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

### burnable_tree_shrub_grass_valid_for_modeling_burned (final-model population)

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
