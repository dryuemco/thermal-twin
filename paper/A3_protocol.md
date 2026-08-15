# Appendix C. Protocol detail

These protocols are given here in full rather than in Methods, because each is a specification a
reader needs only when checking the corresponding result, and none is needed to follow the
argument. Sections 3.2, 3.3, 3.11 and 3.15 state in summary what each does.

## C.1 Burned-area label, the reconstructed analysis grid, and the admissibility gate

Labels come from MODIS MCD64A1 Collection 6.1 (`MODIS/061/MCD64A1`) retrieved through Google Earth
Engine [@Gorelick2017], whose omission and commission characteristics [@Boschetti2019] bound every
model here. The product is exported onto the 30 m EPSG:4326 reference grid used by the rest of the
pipeline, which duplicates each native ~500 m observation across the 30 m pixels beneath it.

The analysis grid is therefore **reconstructed rather than native**: the 30 m grid is partitioned
into non-overlapping blocks of `round(500 / 30) = 17 × 17` pixels, giving a nominal cell edge of
510 m, and each cell is identified by its integer block indices `row_500m` and `col_500m`. This
approximates the MODIS sinusoidal cell rather than reproducing it, being anchored to the
Landsat/EPSG:4326 reference grid, and marginal blocks are truncated. The cell is square in degrees
but not on the ground, about 510 m north to south and 390 to 407 m east to west, so its area is
0.199 to 0.208 km² against a MODIS cell's 0.250 km²; every block-size label in this paper is
therefore the north-south dimension. The companion paper develops what follows from that.

A cell's representative burn date is the **mode** of the positive sub-pixel day-of-year values in
the block, tested against the region's label window. Because the exported raster carries no
out-of-window positives, in this dataset a single in-window positive sub-pixel makes the cell burned.
The fraction of positive sub-pixels agreeing with the modal date is recorded as
`burn_date_pixel_agreement_fraction` but no agreement threshold is imposed. The label never affects a
cell's eligibility for modelling: unburned, all-no-data and out-of-window cells all remain as the
negative class.

Two safeguards are recorded rather than assumed. Cells that burned inside a region's own predictor
window are removed from its analysis universe rather than counted as unburned, which ran for Muğla,
Evia and Montiferru, is recorded as not run for Manavgat and has no recorded status for Bejís.
Burning in earlier years is screened for no region in the five-region cohort; the only historical
exclusion in the study removes the 2021 Muğla scar from the 2022 event-relative experiment of
Section 3.15.

Before any modelling each region passes a gate that answers one question: of the cells labelled
burned, what fraction is dominated by natural vegetation? A region is admitted as a wildfire
candidate when that fraction reaches 0.50 and at least 30 burned cells are present, and is rejected
as a cropland-dominated control when the cropland fraction reaches 0.50 instead. The gate uses ESA
WorldCover classes aggregated to the same reconstructed cells. Its purpose is to separate burned area
produced by natural-fuel combustion from burned area produced by post-harvest stubble burning, which
MCD64A1 does not distinguish. Verdicts are reported in Section 4.1.

## C.2 Transferability diagnostics versus transfer

Twenty candidate diagnostics from five families are each rank-correlated against the same target
quantity, the raw thermal transfer AUC over the twenty ordered directions, under one common
pair-based bootstrap. The families are marginal predictor-distribution measures P(x), burned-niche
overlap P(x|y=1), fire-regime label-pattern structure P(y), and conditional feature-response
direction P(y|x).

The **marginal** family includes area-of-applicability-style dissimilarity in scaled,
importance-weighted predictor space [@Meyer2021; @Meyer2022; @Ludwig2023], climatic and geographic
distance, and a learned domain classifier trained to separate source from target cells. The
**niche-overlap** family includes Schoener's D [@Schoener1968] and Warren's I [@Warren2008] over the burned cells of each region.
The **regime** family includes burned-patch component counts and effective component counts. The
**conditional** family is the sign-agreement index: the fraction of predictors whose signed
univariate association points the same way in both regions, computed over all predictors and over
the subset whose associations are individually interval-supported.

Two properties of this design are stated in advance because they bound what it can show. The
candidate set was fixed in a project analysis log before the correlations were computed; that log is
not a formal pre-registration and no independent timestamped registration exists. And with five
regions the effective sample is ten unordered pairs, so nineteen computed variants are evaluated at
that power with no family-wise error control claimed; where a diagnostic clears an interval test but
not a Bonferroni threshold, both are reported.

## C.3 Same-geography event-to-event comparison (Muğla 2021 versus 2022)

Muğla is the one region for which a second fire event is analysed on the identical AOI and analysis
grid, which allows the direction of feature-label associations to be compared with geography held
fixed. The 2022 experiment is registered with windows anchored to its own event: a 58-day predictor
window closing the day before ignition and a 49-day label window opening on it, matching the 2021
durations exactly.

**This is not a clean temporal-transfer design and is not presented as one.** The 2022 event ignites
about six weeks earlier in the season than the 2021 event, so calendar year and seasonal phase are
confounded and no difference can be attributed to the year alone. The registered claim is
same-geography event-to-event. The pair is deliberately kept out of the twenty-direction matrix, and
that exclusion is enforced in released code rather than merely asserted here.

Two further properties bound the comparison. A historical-burn exclusion applies to the 2022 arm
alone, masking every cell that burned in 2021 so the previous year's scar does not enter the
following year's analysis: it removes 3,073 cells, of which 2,941 belong to the primary population,
taking it from 41,730 rows to 38,790, a drop of 7.0 %. The two arms therefore share 38,789 of 38,790
cells and three byte-identical static predictors, and in the 2022-to-2021 direction every target
positive lies outside the source training population. Section 4.10 states what follows for how these
two numbers may be read.

**Table C1. Study regions, areas of interest and temporal windows.** Bounding boxes are in EPSG:4326,
as registered. Window lengths in brackets are inclusive day counts. The baseline years are the four
window-symmetric years preceding each predictor window.

| Region | Bounding box (lon min, lat min, lon max, lat max) | Predictor window | Label window | Baseline years |
|---|---|---|---|---|
| Manavgat 2021 (Türkiye) | 31.05, 36.72, 31.85, 37.35 | 2021-06-01 to 2021-07-27 (57 d) | 2021-07-28 to 2021-08-31 (35 d) | 2017, 2018, 2019, 2020 |
| Bejís 2022 (Spain) | -1.05, 39.68, -0.35, 40.15 | 2022-06-15 to 2022-08-14 (61 d) | 2022-08-15 to 2022-09-30 (47 d) | 2018, 2019, 2020, 2021 |
| Muğla 2021 (Türkiye) | 27.1, 36.6, 28.9, 37.45 | 2021-06-01 to 2021-07-28 (58 d) | 2021-07-29 to 2021-09-15 (49 d) | 2017, 2018, 2019, 2020 |
| North Evia 2021 (Greece) | 23.05, 38.55, 23.85, 39.15 | 2021-06-05 to 2021-08-02 (59 d) | 2021-08-03 to 2021-09-30 (59 d) | 2017, 2018, 2019, 2020 |
| Montiferru 2021 (Italy) | 8.45, 40.05, 8.75, 40.27 | 2021-05-25 to 2021-07-23 (60 d) | 2021-07-24 to 2021-08-31 (39 d) | 2017, 2018, 2019, 2020 |

## 3.4 Predictor variables

Ten predictors are used, four baseline and six thermal, all summarised per cell over the predictor
window, through the chain shown in Fig. 2. All optical and thermal predictors come from Landsat 8 Collection 2 Level-2
(`LANDSAT/LC08/C02/T1_L2`), quality-screened per pixel from the `QA_PIXEL` band with the water bit
deliberately preserved; the coarse-resolution thermal input is `MODIS/061/MOD11A1`.

- **NDVI**, the predictor-window median of Landsat surface reflectance, is the baseline's one
  time-varying member.
- **Elevation** and **slope** come from the Copernicus DEM GLO-30.
- **Land cover** is ESA WorldCover v200 [@Zanaga2022], entering as the dominant class code.
- **Current LST**, the predictor-window median of Landsat surface temperature in °C.
- **LST anomaly**, a z-score of the current-window LST median against the four baseline years,
  set to no-data where the baseline standard deviation is below 1.0 °C or observations are too few.
- **TVDI** and **TVDI difference**. The Temperature-Vegetation Dryness Index [@Sandholt2002] is
  computed in the LST-NDVI feature space, with wet and dry edges taken as the 2nd and 98th LST
  percentiles within each of twenty NDVI bins and the index clamped to [0, 1]. The edges are
  percentiles of the LST values a given scene contains, so they are fitted per AOI and per window,
  and a TVDI of 0.5 denotes a different physical moisture state in each region. The companion paper
  reports what that scene dependence does and does not explain. **TVDI difference** is the raw
  anomaly of that index against the same four window-symmetric baseline years used for the LST
  anomaly: `tvdi_difference = current_tvdi − mean(baseline_tvdi)`, in index units rather than
  standard deviations, which is why it is reported alongside the z-scored channel rather than in
  place of it.
- **Downscaled LST** and **fused LST**. A MODIS-to-Landsat downscaling model is trained on the
  predictor window and applied to the full 30 m grid. The fused product equals observed Landsat LST
  wherever that is valid, and the downscaled surface only where it is not. Gap-filling therefore
  never replaces or blends a valid observation. The gap-filled share is 0.11 % to 9.70 % by region. The
  downscaler's own inputs include coordinates, which is the one route by which a coordinate-derived
  surface re-enters a feature set from which Section 3.14 excludes coordinates. Appendix A(g)
  reports the increment without these two channels.
