# Multi-AOI burned-pattern comparison

analysis_id: `1f6245a3ccff1cf115c54f547509f1206954d9391892748e131ab5540cdb9a47` (order-invariant)  
created_at: 2026-09-19T09:35:53.101119+00:00  
selection_mode: all_enabled  
requested_experiment_ids: ['bejis_2022', 'evia_2021', 'evia_2021_extended', 'kozan_2023', 'manavgat_2021', 'montiferru_2021', 'mugla_2021', 'mugla_2022', 'mugla_2022_event_relative']  
resolved_experiment_ids: ['bejis_2022', 'evia_2021_extended', 'manavgat_2021', 'montiferru_2021', 'mugla_2021']  
allow_superseded_sensitivity: False  
superseded_pairs: []

**Excluded from resolution:**
- evia_2021: superseded_by_evia_2021_extended
- kozan_2023: negative_control
- mugla_2022: superseded_by_mugla_2022_event_relative
- mugla_2022_event_relative: temporal_transfer_wildfire

## bejis_2022

Canonical burned-landcover gate cross-validated: `C:\Users\CORSAIR\projects\thermal-twin\rerun_labelfix\pipeline\outputs\experiments\bejis_2022\validation\labels\burned_landcover_gate.json` (sha256 8e4658283070d67a6d882aca00c1d89af072ad433f3cdfbae28f338a2394a65d); pre-label-excluded cells: 0; exclusion rule: None.

### all_valid_burned (primary)

Canonical event-footprint population: Step8A rows that are canonical-analysis-eligible (Step8A 'analysis_eligible' column, i.e. NOT pre-label-burn-excluded -- see resolve_analysis_eligible_mask) with burned == 1 and valid (non-null) row_500m/col_500m grid coordinates. No land-cover restriction. Primary population for component count, patch-size distribution, elevation distribution, and land-cover composition.

- Total input rows: 15759
- Burned-cell count: 1103
- Spatially connected burned-cell components: 1
- Singleton components: 0 (0.0)
- Largest component: 1103 cells (fraction 1.0)
- Second-largest component: 0 cells (fraction 0.0)
- Top-3 components combined fraction: 1.0
- Component-share HHI (sum of squared component shares): 1.0
- Effective component count (1 / HHI): 1.0
- Component size (cells): min=1103, q25=1103.0, median=1103.0, mean=1103.0, q75=1103.0, q90=1103.0, q95=1103.0, max=1103
- Approximate total burned area: 275.75 km^2 (source: core.config.STEP8A_MCD64A1_NATIVE_CELL_SIZE_M (documented as an APPROXIMATION of the true native MCD64A1 sinusoidal-grid cell size, anchored to the Landsat/EPSG:4326 30 m reference predictor grid -- see src/step8a_prepare_500m_modeling_dataset.py module docstring).)

**AOI-edge diagnostics (descriptive only, never used to remove components):**
- Edge-touching components: 0 (0.0)
- Largest component touches edge: False

**Elevation (elevation_mean, burned cells):**
- valid=1103, missing=0, min=563.2320556640625, q05=689.7145324707031, q25=820.2522888183594, median=935.1641235351562, mean=956.7014550825519, q75=1076.7398071289062, q95=1308.5318847656245, max=1556.3822021484375, iqr=256.4875183105469, range=993.150146484375

**Land-cover composition (landcover_dominant, burned cells):**
- Observed classes: 4, dominant: shrubland (code 20, fraction 0.557570262919311)

**BurnDate** (descriptive only; never used to split/join/redefine components or to claim distinct-event identification): available, see component_summary.csv for per-component min/max/span/unique_count.

### burnable_tree_shrub_grass_burned (sensitivity)

Natural-vegetation sensitivity population: the corrected primary population further restricted to rows where the existing Step8A 'burnable_tree_shrub_grass' boolean column is True. That frozen Step8A column is a COMBINED per-cell fraction rule -- (landcover_tree_cover_fraction + landcover_shrubland_fraction + landcover_grassland_fraction) >= burnable_threshold (STEP8A_BURNABLE_FRACTION_THRESHOLD) -- already computed in Step8A and reused verbatim here, never recomputed. It is NOT a dominant-land-cover selection: the 'landcover_dominant' column is no part of the selection rule (it is used only for descriptive land-cover composition reporting). A cell therefore qualifies whenever the three fractions SUM to at least the threshold even if its single dominant class is cropland/bare/other, and a cell whose dominant class is tree, shrubland or grassland is excluded if that sum falls below the threshold. Reported as a sensitivity analysis, never substituted for the primary population.

- Total input rows: 15759
- Burned-cell count: 1100
- Spatially connected burned-cell components: 1
- Singleton components: 0 (0.0)
- Largest component: 1100 cells (fraction 1.0)
- Second-largest component: 0 cells (fraction 0.0)
- Top-3 components combined fraction: 1.0
- Component-share HHI (sum of squared component shares): 1.0
- Effective component count (1 / HHI): 1.0
- Component size (cells): min=1100, q25=1100.0, median=1100.0, mean=1100.0, q75=1100.0, q90=1100.0, q95=1100.0, max=1100
- Approximate total burned area: 275.0 km^2 (source: core.config.STEP8A_MCD64A1_NATIVE_CELL_SIZE_M (documented as an APPROXIMATION of the true native MCD64A1 sinusoidal-grid cell size, anchored to the Landsat/EPSG:4326 30 m reference predictor grid -- see src/step8a_prepare_500m_modeling_dataset.py module docstring).)

**AOI-edge diagnostics (descriptive only, never used to remove components):**
- Edge-touching components: 0 (0.0)
- Largest component touches edge: False

**Elevation (elevation_mean, burned cells):**
- valid=1100, missing=0, min=563.2320556640625, q05=689.6211334228516, q25=820.6147918701172, median=935.1695251464844, mean=957.0277708296343, q75=1076.9376525878906, q95=1308.8982238769531, max=1556.3822021484375, iqr=256.32286071777344, range=993.150146484375

**Land-cover composition (landcover_dominant, burned cells):**
- Observed classes: 4, dominant: shrubland (code 20, fraction 0.5590909090909091)

**BurnDate** (descriptive only; never used to split/join/redefine components or to claim distinct-event identification): available, see component_summary.csv for per-component min/max/span/unique_count.

### burnable_tree_shrub_grass_valid_for_modeling_burned (final-model population)

Advisor-specific final-model-population morphology comparison. Selection contract, all conditions required simultaneously: analysis_eligible == True AND valid_for_modeling == True AND burnable_tree_shrub_grass == True AND burned == 1 AND non-null row_500m/col_500m. Both Step8A boolean columns are reused verbatim and never recomputed here (see the burnable_tree_shrub_grass_burned definition for the combined fraction rule behind 'burnable_tree_shrub_grass'). This population describes the morphology of the rows that actually reach the final model; it is an ADDITIONAL comparison only and does NOT replace, redefine, or otherwise alter the 'all_valid_burned' primary population or the 'burnable_tree_shrub_grass_burned' sensitivity population.

- Total input rows: 15759
- Burned-cell count: 1100
- Spatially connected burned-cell components: 1
- Singleton components: 0 (0.0)
- Largest component: 1100 cells (fraction 1.0)
- Second-largest component: 0 cells (fraction 0.0)
- Top-3 components combined fraction: 1.0
- Component-share HHI (sum of squared component shares): 1.0
- Effective component count (1 / HHI): 1.0
- Component size (cells): min=1100, q25=1100.0, median=1100.0, mean=1100.0, q75=1100.0, q90=1100.0, q95=1100.0, max=1100
- Approximate total burned area: 275.0 km^2 (source: core.config.STEP8A_MCD64A1_NATIVE_CELL_SIZE_M (documented as an APPROXIMATION of the true native MCD64A1 sinusoidal-grid cell size, anchored to the Landsat/EPSG:4326 30 m reference predictor grid -- see src/step8a_prepare_500m_modeling_dataset.py module docstring).)

**AOI-edge diagnostics (descriptive only, never used to remove components):**
- Edge-touching components: 0 (0.0)
- Largest component touches edge: False

**Elevation (elevation_mean, burned cells):**
- valid=1100, missing=0, min=563.2320556640625, q05=689.6211334228516, q25=820.6147918701172, median=935.1695251464844, mean=957.0277708296343, q75=1076.9376525878906, q95=1308.8982238769531, max=1556.3822021484375, iqr=256.32286071777344, range=993.150146484375

**Land-cover composition (landcover_dominant, burned cells):**
- Observed classes: 4, dominant: shrubland (code 20, fraction 0.5590909090909091)

**BurnDate** (descriptive only; never used to split/join/redefine components or to claim distinct-event identification): available, see component_summary.csv for per-component min/max/span/unique_count.

## evia_2021_extended

Canonical burned-landcover gate cross-validated: `C:\Users\CORSAIR\projects\thermal-twin\rerun_labelfix\pipeline\outputs\experiments\evia_2021_extended\validation\labels\burned_landcover_gate.json` (sha256 b90b51603b13927d88aa2577219f84a7b76cb800e332ae2c8bb555fb7087466d); pre-label-excluded cells: 16; exclusion rule: 'valid nonzero BurnDate calendar date < label_start (2021-08-03)'.

### all_valid_burned (primary)

Canonical event-footprint population: Step8A rows that are canonical-analysis-eligible (Step8A 'analysis_eligible' column, i.e. NOT pre-label-burn-excluded -- see resolve_analysis_eligible_mask) with burned == 1 and valid (non-null) row_500m/col_500m grid coordinates. No land-cover restriction. Primary population for component count, patch-size distribution, elevation distribution, and land-cover composition.

- Total input rows: 22925
- Burned-cell count: 2788
- Spatially connected burned-cell components: 2
- Singleton components: 0 (0.0)
- Largest component: 2777 cells (fraction 0.9960545193687231)
- Second-largest component: 11 cells (fraction 0.003945480631276901)
- Top-3 components combined fraction: 1.0
- Component-share HHI (sum of squared component shares): 0.9921401723722698
- Effective component count (1 / HHI): 1.0079220939203952
- Component size (cells): min=11, q25=702.5, median=1394.0, mean=1394.0, q75=2085.5, q90=2500.4, q95=2638.7, max=2777
- Approximate total burned area: 697.0 km^2 (source: core.config.STEP8A_MCD64A1_NATIVE_CELL_SIZE_M (documented as an APPROXIMATION of the true native MCD64A1 sinusoidal-grid cell size, anchored to the Landsat/EPSG:4326 30 m reference predictor grid -- see src/step8a_prepare_500m_modeling_dataset.py module docstring).)

**AOI-edge diagnostics (descriptive only, never used to remove components):**
- Edge-touching components: 0 (0.0)
- Largest component touches edge: False

**Elevation (elevation_mean, burned cells):**
- valid=2788, missing=0, min=0.0, q05=29.152962779998777, q25=139.42678833007812, median=254.09134674072266, mean=290.47260561289744, q75=418.96949768066406, q95=650.8449798583985, max=927.2442626953125, iqr=279.54270935058594, range=927.2442626953125

**Land-cover composition (landcover_dominant, burned cells):**
- Observed classes: 8, dominant: tree_cover (code 10, fraction 0.9006456241032998)

**BurnDate** (descriptive only; never used to split/join/redefine components or to claim distinct-event identification): available, see component_summary.csv for per-component min/max/span/unique_count.

### burnable_tree_shrub_grass_burned (sensitivity)

Natural-vegetation sensitivity population: the corrected primary population further restricted to rows where the existing Step8A 'burnable_tree_shrub_grass' boolean column is True. That frozen Step8A column is a COMBINED per-cell fraction rule -- (landcover_tree_cover_fraction + landcover_shrubland_fraction + landcover_grassland_fraction) >= burnable_threshold (STEP8A_BURNABLE_FRACTION_THRESHOLD) -- already computed in Step8A and reused verbatim here, never recomputed. It is NOT a dominant-land-cover selection: the 'landcover_dominant' column is no part of the selection rule (it is used only for descriptive land-cover composition reporting). A cell therefore qualifies whenever the three fractions SUM to at least the threshold even if its single dominant class is cropland/bare/other, and a cell whose dominant class is tree, shrubland or grassland is excluded if that sum falls below the threshold. Reported as a sensitivity analysis, never substituted for the primary population.

- Total input rows: 22925
- Burned-cell count: 2664
- Spatially connected burned-cell components: 2
- Singleton components: 0 (0.0)
- Largest component: 2653 cells (fraction 0.9958708708708709)
- Second-largest component: 11 cells (fraction 0.004129129129129129)
- Top-3 components combined fraction: 1.0
- Component-share HHI (sum of squared component shares): 0.9917758411564719
- Effective component count (1 / HHI): 1.008292356500576
- Component size (cells): min=11, q25=671.5, median=1332.0, mean=1332.0, q75=1992.5, q90=2388.8, q95=2520.9, max=2653
- Approximate total burned area: 666.0 km^2 (source: core.config.STEP8A_MCD64A1_NATIVE_CELL_SIZE_M (documented as an APPROXIMATION of the true native MCD64A1 sinusoidal-grid cell size, anchored to the Landsat/EPSG:4326 30 m reference predictor grid -- see src/step8a_prepare_500m_modeling_dataset.py module docstring).)

**AOI-edge diagnostics (descriptive only, never used to remove components):**
- Edge-touching components: 0 (0.0)
- Largest component touches edge: False

**Elevation (elevation_mean, burned cells):**
- valid=2664, missing=0, min=2.779559850692749, q05=52.81842174530029, q25=149.2527961730957, median=262.8730926513672, mean=301.9793722779006, q75=432.52899169921875, q95=657.4498168945312, max=927.2442626953125, iqr=283.27619552612305, range=924.4647028446198

**Land-cover composition (landcover_dominant, burned cells):**
- Observed classes: 7, dominant: tree_cover (code 10, fraction 0.9425675675675675)

**BurnDate** (descriptive only; never used to split/join/redefine components or to claim distinct-event identification): available, see component_summary.csv for per-component min/max/span/unique_count.

### burnable_tree_shrub_grass_valid_for_modeling_burned (final-model population)

Advisor-specific final-model-population morphology comparison. Selection contract, all conditions required simultaneously: analysis_eligible == True AND valid_for_modeling == True AND burnable_tree_shrub_grass == True AND burned == 1 AND non-null row_500m/col_500m. Both Step8A boolean columns are reused verbatim and never recomputed here (see the burnable_tree_shrub_grass_burned definition for the combined fraction rule behind 'burnable_tree_shrub_grass'). This population describes the morphology of the rows that actually reach the final model; it is an ADDITIONAL comparison only and does NOT replace, redefine, or otherwise alter the 'all_valid_burned' primary population or the 'burnable_tree_shrub_grass_burned' sensitivity population.

- Total input rows: 22925
- Burned-cell count: 2664
- Spatially connected burned-cell components: 2
- Singleton components: 0 (0.0)
- Largest component: 2653 cells (fraction 0.9958708708708709)
- Second-largest component: 11 cells (fraction 0.004129129129129129)
- Top-3 components combined fraction: 1.0
- Component-share HHI (sum of squared component shares): 0.9917758411564719
- Effective component count (1 / HHI): 1.008292356500576
- Component size (cells): min=11, q25=671.5, median=1332.0, mean=1332.0, q75=1992.5, q90=2388.8, q95=2520.9, max=2653
- Approximate total burned area: 666.0 km^2 (source: core.config.STEP8A_MCD64A1_NATIVE_CELL_SIZE_M (documented as an APPROXIMATION of the true native MCD64A1 sinusoidal-grid cell size, anchored to the Landsat/EPSG:4326 30 m reference predictor grid -- see src/step8a_prepare_500m_modeling_dataset.py module docstring).)

**AOI-edge diagnostics (descriptive only, never used to remove components):**
- Edge-touching components: 0 (0.0)
- Largest component touches edge: False

**Elevation (elevation_mean, burned cells):**
- valid=2664, missing=0, min=2.779559850692749, q05=52.81842174530029, q25=149.2527961730957, median=262.8730926513672, mean=301.9793722779006, q75=432.52899169921875, q95=657.4498168945312, max=927.2442626953125, iqr=283.27619552612305, range=924.4647028446198

**Land-cover composition (landcover_dominant, burned cells):**
- Observed classes: 7, dominant: tree_cover (code 10, fraction 0.9425675675675675)

**BurnDate** (descriptive only; never used to split/join/redefine components or to claim distinct-event identification): available, see component_summary.csv for per-component min/max/span/unique_count.

## manavgat_2021

Canonical burned-landcover gate cross-validated: `C:\Users\CORSAIR\projects\thermal-twin\rerun_labelfix\pipeline\outputs\experiments\manavgat_2021\validation\labels\burned_landcover_gate.json` (sha256 a26dcc5edd24df2cbc7513c4b18521b7a6a8711a91f196a4fe86ed8e08152441); pre-label-excluded cells: 0; exclusion rule: 'not_applied'.

### all_valid_burned (primary)

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

### burnable_tree_shrub_grass_burned (sensitivity)

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

### burnable_tree_shrub_grass_valid_for_modeling_burned (final-model population)

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

## montiferru_2021

Canonical burned-landcover gate cross-validated: `C:\Users\CORSAIR\projects\thermal-twin\rerun_labelfix\pipeline\outputs\experiments\montiferru_2021\validation\labels\burned_landcover_gate.json` (sha256 92ac140fbfa72dedd0c72f0d0de6db1d720c0b672000d2e68a40fe3f60e8beaa); pre-label-excluded cells: 61; exclusion rule: 'valid nonzero BurnDate calendar date < label_start (2021-07-24)'.

### all_valid_burned (primary)

Canonical event-footprint population: Step8A rows that are canonical-analysis-eligible (Step8A 'analysis_eligible' column, i.e. NOT pre-label-burn-excluded -- see resolve_analysis_eligible_mask) with burned == 1 and valid (non-null) row_500m/col_500m grid coordinates. No land-cover restriction. Primary population for component count, patch-size distribution, elevation distribution, and land-cover composition.

- Total input rows: 3234
- Burned-cell count: 697
- Spatially connected burned-cell components: 2
- Singleton components: 0 (0.0)
- Largest component: 690 cells (fraction 0.9899569583931134)
- Second-largest component: 7 cells (fraction 0.010043041606886656)
- Top-3 components combined fraction: 1.0
- Component-share HHI (sum of squared component shares): 0.980115642155662
- Effective component count (1 / HHI): 1.0202877670645112
- Component size (cells): min=7, q25=177.75, median=348.5, mean=348.5, q75=519.25, q90=621.7, q95=655.85, max=690
- Approximate total burned area: 174.25 km^2 (source: core.config.STEP8A_MCD64A1_NATIVE_CELL_SIZE_M (documented as an APPROXIMATION of the true native MCD64A1 sinusoidal-grid cell size, anchored to the Landsat/EPSG:4326 30 m reference predictor grid -- see src/step8a_prepare_500m_modeling_dataset.py module docstring).)

**AOI-edge diagnostics (descriptive only, never used to remove components):**
- Edge-touching components: 1 (0.5)
- Largest component touches edge: False

**Elevation (elevation_mean, burned cells):**
- valid=697, missing=0, min=60.605690002441406, q05=156.37876586914064, q25=234.07696533203125, median=348.96966552734375, mean=416.2836999003822, q75=575.7138061523438, q95=874.7770751953125, max=1017.4007568359375, iqr=341.6368408203125, range=956.7950668334961

**Land-cover composition (landcover_dominant, burned cells):**
- Observed classes: 5, dominant: tree_cover (code 10, fraction 0.5911047345767575)

**BurnDate** (descriptive only; never used to split/join/redefine components or to claim distinct-event identification): available, see component_summary.csv for per-component min/max/span/unique_count.

### burnable_tree_shrub_grass_burned (sensitivity)

Natural-vegetation sensitivity population: the corrected primary population further restricted to rows where the existing Step8A 'burnable_tree_shrub_grass' boolean column is True. That frozen Step8A column is a COMBINED per-cell fraction rule -- (landcover_tree_cover_fraction + landcover_shrubland_fraction + landcover_grassland_fraction) >= burnable_threshold (STEP8A_BURNABLE_FRACTION_THRESHOLD) -- already computed in Step8A and reused verbatim here, never recomputed. It is NOT a dominant-land-cover selection: the 'landcover_dominant' column is no part of the selection rule (it is used only for descriptive land-cover composition reporting). A cell therefore qualifies whenever the three fractions SUM to at least the threshold even if its single dominant class is cropland/bare/other, and a cell whose dominant class is tree, shrubland or grassland is excluded if that sum falls below the threshold. Reported as a sensitivity analysis, never substituted for the primary population.

- Total input rows: 3234
- Burned-cell count: 539
- Spatially connected burned-cell components: 8
- Singleton components: 2 (0.25)
- Largest component: 416 cells (fraction 0.7717996289424861)
- Second-largest component: 55 cells (fraction 0.10204081632653061)
- Top-3 components combined fraction: 0.9628942486085343
- Component-share HHI (sum of squared component shares): 0.6144581630932016
- Effective component count (1 / HHI): 1.6274501016732674
- Component size (cells): min=1, q25=2.5, median=7.5, mean=67.375, q75=49.75, q90=163.29999999999995, q95=289.6499999999998, max=416
- Approximate total burned area: 134.75 km^2 (source: core.config.STEP8A_MCD64A1_NATIVE_CELL_SIZE_M (documented as an APPROXIMATION of the true native MCD64A1 sinusoidal-grid cell size, anchored to the Landsat/EPSG:4326 30 m reference predictor grid -- see src/step8a_prepare_500m_modeling_dataset.py module docstring).)

**AOI-edge diagnostics (descriptive only, never used to remove components):**
- Edge-touching components: 0 (0.0)
- Largest component touches edge: False

**Elevation (elevation_mean, burned cells):**
- valid=539, missing=0, min=60.605690002441406, q05=153.2969207763672, q25=237.66597747802734, median=424.2523193359375, mean=456.7148911116959, q75=652.3868713378906, q95=905.9338012695312, max=1017.4007568359375, iqr=414.7208938598633, range=956.7950668334961

**Land-cover composition (landcover_dominant, burned cells):**
- Observed classes: 4, dominant: tree_cover (code 10, fraction 0.764378478664193)

**BurnDate** (descriptive only; never used to split/join/redefine components or to claim distinct-event identification): available, see component_summary.csv for per-component min/max/span/unique_count.

### burnable_tree_shrub_grass_valid_for_modeling_burned (final-model population)

Advisor-specific final-model-population morphology comparison. Selection contract, all conditions required simultaneously: analysis_eligible == True AND valid_for_modeling == True AND burnable_tree_shrub_grass == True AND burned == 1 AND non-null row_500m/col_500m. Both Step8A boolean columns are reused verbatim and never recomputed here (see the burnable_tree_shrub_grass_burned definition for the combined fraction rule behind 'burnable_tree_shrub_grass'). This population describes the morphology of the rows that actually reach the final model; it is an ADDITIONAL comparison only and does NOT replace, redefine, or otherwise alter the 'all_valid_burned' primary population or the 'burnable_tree_shrub_grass_burned' sensitivity population.

- Total input rows: 3234
- Burned-cell count: 539
- Spatially connected burned-cell components: 8
- Singleton components: 2 (0.25)
- Largest component: 416 cells (fraction 0.7717996289424861)
- Second-largest component: 55 cells (fraction 0.10204081632653061)
- Top-3 components combined fraction: 0.9628942486085343
- Component-share HHI (sum of squared component shares): 0.6144581630932016
- Effective component count (1 / HHI): 1.6274501016732674
- Component size (cells): min=1, q25=2.5, median=7.5, mean=67.375, q75=49.75, q90=163.29999999999995, q95=289.6499999999998, max=416
- Approximate total burned area: 134.75 km^2 (source: core.config.STEP8A_MCD64A1_NATIVE_CELL_SIZE_M (documented as an APPROXIMATION of the true native MCD64A1 sinusoidal-grid cell size, anchored to the Landsat/EPSG:4326 30 m reference predictor grid -- see src/step8a_prepare_500m_modeling_dataset.py module docstring).)

**AOI-edge diagnostics (descriptive only, never used to remove components):**
- Edge-touching components: 0 (0.0)
- Largest component touches edge: False

**Elevation (elevation_mean, burned cells):**
- valid=539, missing=0, min=60.605690002441406, q05=153.2969207763672, q25=237.66597747802734, median=424.2523193359375, mean=456.7148911116959, q75=652.3868713378906, q95=905.9338012695312, max=1017.4007568359375, iqr=414.7208938598633, range=956.7950668334961

**Land-cover composition (landcover_dominant, burned cells):**
- Observed classes: 4, dominant: tree_cover (code 10, fraction 0.764378478664193)

**BurnDate** (descriptive only; never used to split/join/redefine components or to claim distinct-event identification): available, see component_summary.csv for per-component min/max/span/unique_count.

## mugla_2021

Canonical burned-landcover gate cross-validated: `C:\Users\CORSAIR\projects\thermal-twin\rerun_labelfix\pipeline\outputs\experiments\mugla_2021\validation\labels\burned_landcover_gate.json` (sha256 acadc06206952d9ca4a9effd9b1262bff00e057bbc4442f0cc1f1078855322bc); pre-label-excluded cells: 49; exclusion rule: 'valid nonzero BurnDate calendar date < label_start (2021-07-29)'.

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

## Limitations

- Connected components are a spatial fragmentation proxy. They must not be interpreted as a definitive count of independent wildfire events, because one event may appear as multiple disconnected components and multiple events may be spatially connected at the analysis resolution.
- Connected-component count is resolution-dependent (8-neighbour adjacency on the fixed 500 m Step8A grid); a coarser or finer grid would yield a different count for the same physical burned area.
- Results are sensitive to AOI clipping: a component that would be contiguous in a wider AOI can appear split, or vice versa, purely because of where the analysis extent was drawn.
- MCD64A1-scale cells are approximate spatial units, not exact ground-truth footprints (see CELL_AREA_KM2_SOURCE provenance).
- Component count is not a definitive fire-event count.
- Results are descriptive and do not explain cross-region transfer performance causally.
