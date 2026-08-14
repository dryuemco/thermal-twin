# TVDI edges refitted without sea, and a common-edge TVDI

Answers referee round 3 Tier 2.1, and computes the pooled common-edge index that
`03_methods.md` and `05_discussion.md` promised and had never run.

Produced on this machine with the rebuilt environment (`ENVIRONMENT.md`): Python 3.12.10,
NumPy 2.4.4, pandas 3.0.2. The binning, percentile and clamp primitives are **imported from
the pipeline itself** (`src.step5c_tvdi`, `src.step5_preprocess_timeseries` at `48b56e7`), so the
only difference between arms is which pixels enter the percentile fit.

## Arms

- **scene, all pixels** , the frozen pipeline behaviour: 2nd/98th LST percentile per NDVI bin
  over every valid pixel of the scene, sea included.
- **scene, land only** , identical, restricted to ESA WorldCover classes 10/20/30/40/60.
- **pooled, land only** , one set of edges fitted once over the land pixels of all five regions
  (26,237,200 pixels), so a TVDI of 0.5 denotes the same physical dryness in every region.

## Validation, before any new number is read

| Region | max abs wet-edge diff | max abs dry-edge diff | bin pixel-count diff | cell aggregate vs frozen `current_tvdi_mean` |
|---|---|---|---|---|
| Bejis 2022 | 7.1e-15 | 7.1e-15 | 0 | 1.6e-07 |
| Montiferru 2021 | 3.6e-15 | 7.1e-15 | 0 | 1.4e-07 |
| Manavgat 2021 | 3.6e-15 | 7.1e-15 | 0 | 1.8e-07 |
| Mugla 2021 | 3.6e-15 | 7.1e-15 | 0 | 1.6e-07 |
| North Evia 2021 (ext.) | 3.6e-15 | 7.1e-15 | 0 | 1.4e-07 |

The all-pixel arm reproduces every frozen edge to floating-point noise with **exactly equal** bin
pixel counts, and the cell-aggregated index reproduces the frozen `current_tvdi_mean` column to
1.8e-07, which is float32 storage precision. The signed AUC of the recomputed all-pixel arm equals
the archived `raw_univariate_auc` in all five regions. The spatial-block bootstrap reproduces the
archived intervals as well (Manavgat and Bejis to four decimals, the others to about 0.005).

## Result: signed univariate AUC of `current_tvdi_mean` against `burned`

Primary natural-vegetation population. Raw AUC, never folded to max(AUC, 1-AUC), so a value below
0.5 is a direction. 10-cell (~5 km) spatial-block bootstrap, 1000 replicates, seed 42,
2.5/97.5 percentile, at step9g's own registered specification.

| Region | water share | scene, all pixels | scene, land only | pooled, land only |
|---|---:|---|---|---|
| Bejis 2022 | 0.1 % | 0.517 [0.429, 0.595] | 0.519 [0.431, 0.597] | 0.503 [0.416, 0.578] |
| Montiferru 2021 | 7.4 % | **0.356** [0.233, 0.499] | 0.353 [0.229, 0.500] | 0.356 [0.232, 0.500] |
| Manavgat 2021 | 8.3 % | 0.552 [0.460, 0.641] | 0.558 [0.465, 0.646] | 0.565 [0.469, 0.656] |
| Mugla 2021 | 38.9 % | **0.336** [0.276, 0.401] | **0.351** [0.288, 0.424] | **0.341** [0.280, 0.408] |
| North Evia 2021 (ext.) | 57.6 % | **0.362** [0.280, 0.440] | **0.379** [0.298, 0.458] | **0.378** [0.297, 0.455] |

Bold marks an interval that excludes 0.5. 

## Reading

**The sea does enter the edge fit, and it moves the index, by an amount that scales with each
AOI's sea fraction.** Removing water shifts the signed AUC by +0.017 in Evia (57.6 % water) and
+0.016 in Mugla (38.9 %), against +0.006 in Manavgat (8.3 %), -0.002 in Montiferru (7.4 %) and
+0.002 in Bejis (0.1 %). The mechanism referee 2 identified is therefore real and measurable.

**It does not explain the reversal.** Every region keeps its side of 0.5 under both re-runs. The
two regions where higher TVDI ranks burned cells stay above 0.5; the three where lower TVDI does
stay below, and Mugla and Evia keep intervals entirely below 0.5. One verdict changes and it
changes on a knife edge: Montiferru's upper bound moves from 0.4991 to 0.5004, a shift of 0.0013,
which is the instability already documented as limitation (x).

**A common physical scale does not remove it either.** With one set of edges for all five regions,
so that a TVDI of 0.5 means the same dryness everywhere, Manavgat still points one way (0.566) and
Mugla and Evia still point the other with bootstrap support (0.341 and 0.378). This was the
analysis named as the one that would separate the index's scene dependence from concept shift.
It separates them, and it does not favour scene dependence.

## Limits

1. Only `current_tvdi_mean` is re-derived. `tvdi_difference_mean` needs the four baseline-year
   TVDI surfaces refitted as well and was not run.
2. The pooled arm pools the current-window LST of five regions observed on different dates. A
   common edge in this sense is a common statistical scale over the pooled sample, not a
   radiometrically harmonised one.
3. Land is defined by the ESA WorldCover class of the 30 m pixel. Mixed coastal pixels classified
   as land still contain water.
4. The bootstrap resamples 10-cell blocks, as step9g does; Montiferru has few positive-carrying
   blocks and its interval should be read with that in mind.

## Provenance

Inputs, per region: `step5/current_period_median_celsius.tif`,
`data/ndvi_current_period/current_ndvi_median.tif`,
`gate_inputs/landcover_esa_worldcover_v200_aligned_to_reference.tif`, all verified to share the
reference grid, and `step8a/step8a_500m_modeling_dataset.csv` for the labels and the population
mask. Frozen comparators: `step5c/tvdi_edge_diagnostics.csv` and
`diagnostics/step9g_univariate_feature_auc_direction_reversal/*/step9g_univariate_auc_by_region.csv`.
Machine-readable results: `paper/tvdi_land_refit.json`.