# 3. Data and methods

> **Rewritten 2026-08-14 in the split.** This section was 15,407 words. It is now written to let a
> reader replicate the three findings of Section 1.4 and to carry every number Section 4 cites, and
> nothing else. The observational layer beneath it, meaning predictor provenance, compositing,
> quality screening, index normalisation, label omission and the version and reproduction audits, is
> the subject of the companion paper and is summarised here only where a Paper 1 claim depends on it.
> The released repository remains the authoritative source for file and line references.

## 3.1 Study regions and temporal windows

Five Mediterranean wildfire regions are analysed: Manavgat 2021 and Muğla 2021 in Türkiye, Bejís
2022 in Spain, North Evia 2021 in Greece and Montiferru 2021 in Sardinia. Each is a place-based
rectangular area of interest in EPSG:4326, defined from place coverage rather than from a fire
perimeter, and not tuned on burned prevalence, gate outcome or any model metric. One AOI choice was
label-informed and is stated as such: the North Evia box was extended after the legacy box was found
to carry an atypically high burned prevalence, the extended geometry was then defined from place
anchors, and the legacy variant is retained as a sensitivity (Section 4.7a). The AOIs are
deliberately not clipped to fire perimeters, so that unburned cells surrounding each fire form the
negative class rather than being excluded by construction. A sixth region, Kozan 2023, is carried as
a negative control and is excluded from all modelling by the gate of Section 3.3.

Each region has two non-overlapping windows. The **predictor window** closes the day before the
**label window** opens, so no predictor observation can post-date the first labelled burning. Window
lengths are matched within a region and vary between them with the event: 56 to 60 days for
predictors and 35 to 49 days for labels. A four-year baseline of window-symmetric composites
precedes each predictor window and supplies the climatological reference for the anomaly channels.
Region identifiers, bounding boxes, window dates and baseline years are registered in
`core/regions.py` and are reproduced in Table 1.

## 3.2 Burned-area label and the ~500 m analysis grid

Labels come from MODIS MCD64A1 Collection 6.1 [@Giglio2018] retrieved through Google Earth Engine
[@Gorelick2017], whose omission and commission characteristics [@Boschetti2019] bound every model
here. The analysis grid is **reconstructed rather than native**: the pipeline's 30 m EPSG:4326
reference grid is partitioned into 17 x 17 blocks, giving a nominal 510 m cell that approximates
rather than reproduces the MODIS cell, and is square in degrees but not on the ground. A cell's burn
date is the mode of its positive sub-pixel day-of-year values, tested against the region's label
window; the label never affects a cell's eligibility for modelling. Two safeguards are recorded
rather than assumed: cells burning inside a region's own predictor window are removed, which ran for
three of five regions, and burning in earlier years is screened for none. Appendix C.1 gives the
full specification, including what follows from the grid's shape.

## 3.3 Burned-landcover admissibility gate

Before any modelling each region passes a gate asking what fraction of its burned cells is dominated
by natural vegetation, using ESA WorldCover classes on the same cells. A region is admitted at 0.50
with at least 30 burned cells, and rejected as a cropland-dominated control at 0.50 cropland. The
purpose is to separate burned area produced by natural-fuel combustion from post-harvest stubble
burning, which MCD64A1 does not distinguish. Verdicts are in Section 4.1; the full rule is in
Appendix C.1.

## 3.4 Predictor variables

Ten predictors are used, four baseline and six thermal, all summarised per cell over the predictor
window. All optical and thermal predictors come from Landsat 8 Collection 2 Level-2
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
  predictor window and applied to the full 30 m grid; the fused product equals observed Landsat LST
  wherever that is valid and the downscaled surface only where it is not, so gap-filling never
  replaces or blends a valid observation. The gap-filled share is 0.11 % to 9.70 % by region. The
  downscaler's own inputs include coordinates, which is the one route by which a coordinate-derived
  surface re-enters a feature set from which Section 3.13 excludes coordinates; the companion paper
  measures what the increment is worth without these two channels.

## 3.5 Cell aggregation, validity and analysis populations

Cell-level values are means over the ~510 m cell, computed from valid 30 m pixels only, with the
valid fraction recorded. A cell is `valid_for_modeling` when it meets a 30 % valid-pixel floor and no
thermal channel is missing. Two populations are then defined. The **primary** population is natural
vegetation, cells whose combined tree, shrub and grass fraction reaches 0.50, which excludes
cropland from every burnable mask. The **secondary** population is all valid cells, reported
throughout as a sensitivity. Every headline result is given for both.

## 3.6 Feature sets and classifier

Two nested feature sets are compared. The **baseline** set is NDVI, elevation, slope and land cover.
The **thermal** set is the baseline plus the six thermal channels. Land cover is one-hot encoded and
numeric features are standardised inside the fitting pipeline. The classifier is a random forest
[@Breiman2001] with 300 trees, unlimited depth, `min_samples_leaf = 3`, balanced class weights and
`random_state = 42`, identical for every region, population, feature set and transfer direction, so
that no comparison in this paper is confounded by a model choice.

## 3.7 Spatial-block cross-validation and bootstrap uncertainty

Cross-validation is spatially blocked. Blocks are squares of the analysis grid formed as
`row_500m // B` by `col_500m // B`, and folds are drawn over whole blocks, so no block is split
between training and test. Five folds are used. The block size B is reported at 2, 10 and 20 cells,
about 1, 5 and 10 km, for the within-region analysis.

Uncertainty is a spatial-block bootstrap: blocks are resampled with replacement, 1000 replicates,
seed 42, with 2.5 and 97.5 percentiles as the interval. Because it is blocks that are resampled,
what bounds an interval's reliability is the number of blocks carrying at least one burned cell, and
those counts are reported alongside the intervals. Where a verdict rests on too few such blocks it
is stated as indicative rather than as an interval.

## 3.8 Cross-region transfer protocol

For each ordered pair of regions the model is fitted on the source population and applied to the
target population with **no target label used at any point**: no refitting, no threshold selection,
no calibration. Both the baseline and the thermal feature set are transferred, so that the thermal
block's contribution is a paired difference within a direction rather than a comparison across
directions. All twenty ordered directions among the five regions are computed.

## 3.9 Label-blind domain adaptation

Two label-free remedies are tested on every direction, in both feature sets.

**Region-wise z-score.** Each region's numeric features are standardised using its own statistics,
source statistics from source data and target statistics from target data, never pooled. The
classifier is refitted on the z-scored source and applied to the z-scored target. This removes
first- and second-order marginal offsets.

**CORAL after region-wise z-score.** Starting from the z-scored features, the source covariance is
aligned to the target covariance by the standard whitening-recolouring map [@Sun2016], with
regularisation λ = 10⁻⁵ and eigenvalues floored at 10⁻¹². Critically **the transform is applied to
the source only**; the target is left exactly as it is. The classifier is refitted on the aligned
source. Neither variant sees a target label, and both are verified label-blind at run time.

λ sensitivity was assessed over nine values from 0 to 10⁻¹ on four directions in both feature
families, moving transfer AUC by at most 0.014 in any direction and 0.008 within the thermal family.
The canonical λ = 1 lies outside the released sweep; the companion paper reports it.

## 3.10 Transfer-gap decomposition and the concept-shift diagnostic

For each direction the gap between the target's own within-region skill and the raw transfer result
is split into a part the best label-free adaptation recovers and a part it does not, with the
recovered fraction defined as (adapted − raw) / (within − raw), signed and unclipped, and its
interval from the same paired bootstrap. The recovered part bounds what covariate-level correction
can achieve; the remainder is the conditional residual.

The mechanism is diagnosed by **signed univariate association**. For each numeric predictor the raw
ROC-AUC of that predictor against `burned` is computed in each region and never folded to
max(AUC, 1 − AUC), so a value below 0.5 is read as a direction rather than as weakness. A reversal is
called bootstrap-supported only when the two regions' intervals are disjoint, under the same 10-cell
spatial-block bootstrap.

## 3.11 Transferability diagnostics versus transfer

Twenty candidate diagnostics from four families are computed for every region pair and
rank-correlated (Spearman) against observed raw transfer AUC, under one bootstrap framework that
resamples unordered region pairs with both of their ordered directions travelling together. The
families are marginal predictor-space measures P(x), including area-of-applicability dissimilarity,
climatic and geographic distance and a learned domain classifier; burned-niche overlap P(x|y=1);
burn-pattern regime distance P(y); and conditional direction agreement P(y|x). No family-wise error
control is claimed, and the number of variants computed within each family is reported with the
result. Appendix C.1 gives the full specification of each diagnostic and of the bootstrap.

## 3.12 Interventions

**Pooled multi-region training.** Leave-one-region-out: the model is trained on the pooled primary
populations of the other four regions and evaluated on the held-out region, with folds blocked as
before. This asks whether pooling recovers what single-source transfer loses.

**Removal of direction-reversing features.** The two predictors whose signed association reverses
between regions with bootstrap support are **`elevation_mean`** (Manavgat against Bejís and against
Muğla) and **`lst_anomaly_mean`** (Bejís against Evia). They are dropped and everything is refitted,
within-region and across every direction, and the two are also dropped singly so the cost can be
attributed. This measures what the removal costs locally and what it returns on transfer on the same
footing. Note that the two features are selected by the same reversal analysis against which the
result is then read, so both quantities are post-selection estimates and no correction for that
selection is applied.

## 3.13 Leakage control

An explicit forbidden-column set is enforced at every model fit. Coordinates (`lon`, `lat`, `row`,
`col` and their normalised forms), every burn-date and label-provenance column, and the agreement
fraction are excluded from all feature sets, and the enforcement runs as an assertion rather than a
convention. The natural-vegetation mask is used only to define the population, never as a predictor.
Spatial blocking prevents a cell from sharing a fold with its own neighbours.

**Reproducibility.** All randomness uses seed 42 and the bootstrap uses 1000 replicates throughout.
The transfer and adaptation analysis runs in an environment separate from the upstream pipeline's,
so every within-region model was refitted there and compared against the frozen upstream output, and
the independently implemented adaptation against the pipeline's own; the within-region comparisons
agree exactly and the twenty transfer directions to within 1.6×10⁻⁷. Because random-forest fits are
not bit-identical across library versions, all numbers here were produced under, or verified
against, scikit-learn 1.9.0, and cross-region point estimates carry an implementation tolerance of
about ±0.02 to 0.03 if that version is not fixed. The companion paper reports the version
sensitivity and the reproduction check in full.

**Sensitivity analyses.** Every headline result is repeated across two analysis populations, three
spatial-block sizes, the CORAL regularisation sweep and both feature sets. Where a conclusion
depends on one of those choices, the dependence is reported rather than resolved by choosing the
favourable setting.

## 3.14 Same-geography event-to-event comparison (Mugla 2021 versus 2022)

Mugla admits a comparison in which place is held fixed and the event varies: a second fire burned
inside the identical AOI, on the identical analysis grid, eleven months after the first. Signed
univariate AUCs are computed for both arms under the same 10-cell spatial-block bootstrap used
elsewhere. Season, year and population all differ between the arms, since the 2022 arm is defined by
removing the 2021 scar, and Section 4.8 reports what that costs. Appendix C.2 gives the window
dates, the population construction and the asymmetry audit.
