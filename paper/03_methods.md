# 3. Materials and methods

> **Drafting note.** Every constant, threshold, window and formula below was read from the
> executed pipeline source rather than reconstructed from memory; the governing source file is
> named in each subsection so that the manuscript text and the released code can be checked against
> each other. Quantities that could not be confirmed against an actual output file in the working
> copy at drafting time are marked `[TO VERIFY]`.

## 3.1 Study regions and temporal windows

Five Mediterranean-basin wildfire regions are analysed. Each is defined as a place-based rectangular
area of interest (AOI) in EPSG:4326, fixed **before** any burned-area label was inspected. The AOIs
are deliberately *not* clipped to fire perimeters, so that unburned cells surrounding each fire
constitute the negative class rather than being excluded by construction.

For each region the analysis is organised around two non-overlapping time windows. The **predictor
window** is the pre-fire period from which every dynamic predictor is composited. It ends the day
before the label window opens. The **label window** is the period in which a burned-area detection
counts as a positive label. Because the predictor window closes before the first day of the label
window, no predictor observation can post-date the fire it is used to predict. A separate set of
**baseline years** supplies the multi-year climatological reference against which thermal anomalies
are computed. These use the same calendar window as the predictor window, transported to earlier
years, with the fire year itself excluded.

**Table 1. Study regions.** Every value below is read directly from the experiment registry in
`repo/core/regions.py` at commit `48b56e7`, which now contains all five regions. AOI constants:
Manavgat `regions.py:222`, Bejís `:252`, Muğla `MUGLA_AOI_BBOX :59`, extended Evia
`NORTH_EVIA_EXTENDED_AOI_BBOX :106`, Montiferru `MONTIFERRU_AOI_BBOX :142`. Windows, baseline years
and roles from the `EXPERIMENTS` dictionary (`:332 to 790`; individual entries at `:352` Manavgat,
`:368` Bejís, `:391` Muğla, `:683` extended Evia, `:721` Montiferru). The registry was read by
importing `core.regions` and calling `get_experiment()` for each identifier rather than by parsing
the file, so the values are the ones the pipeline itself resolves. Muğla and Montiferru no longer
require the earlier reconstruction from the 30 m reference-grid transform: both are now declared
constants, and their declared corners agree with the previously grid-derived values (Muğla 27.0998,
36.5998, 28.9001, 37.4500 → 27.10, 36.60, 28.90, 37.45; Montiferru 8.4497, 40.0499, 8.7502, 40.2700
→ 8.45, 40.05, 8.75, 40.27) to the rounding shown.

| Region | Country | AOI bounding box (W, S, E, N) | Predictor (pre-fire) window | Label window | Baseline years | Role |
|---|---|---|---|---|---|---|
| Manavgat / Antalya 2021 | Türkiye | 31.05, 36.72, 31.85, 37.35 | 2021-06-01 → 2021-07-27 | 2021-07-28 → 2021-08-31 | 2017-2020 | anchor wildfire |
| Bejís / Castellón 2022 | Spain | −1.05, 39.68, −0.35, 40.15 | 2022-06-15 → 2022-08-14 | 2022-08-15 → 2022-09-30 | 2018-2021 | Mediterranean transfer wildfire |
| Muğla 2021 | Türkiye | 27.10, 36.60, 28.90, 37.45 | 2021-06-01 → 2021-07-28 | 2021-07-29 → 2021-09-15 | 2017-2020 | same-country, same-year transfer wildfire |
| North Evia (Euboea) 2021, extended AOI | Greece | 23.05, 38.55, 23.85, 39.15 | 2021-06-05 → 2021-08-02 | 2021-08-03 → 2021-09-30 | 2017-2020 | Mediterranean transfer wildfire |
| Montiferru (Sardinia) 2021 | Italy | 8.45, 40.05, 8.75, 40.27 | 2021-05-25 → 2021-07-23 | 2021-07-24 → 2021-08-31 | 2017-2020 | Mediterranean transfer wildfire |

North Evia is analysed on an **extended** 0.80° × 0.60° AOI. The legacy 0.40° × 0.40° box (23.12,
38.68, 23.52, 39.08; `repo/core/regions.py:67`) shares identical predictor and label windows and is
retained **only** as a sensitivity variant (Section 3.16.1).

Sample sizes, burned-cell counts and prevalences per region are reported in Table 1b, read from each
region's frozen Step 8A dataset statistics (`step8a_dataset_stats.json`) for all five regions.

The region set is constructed to separate two candidate explanations of transfer failure. Manavgat
and Muğla are in the same country, in the same fire year, roughly 200 km apart, and share a
baseline-year set; Bejís is in a different country, a different year, and about 2500 km away. If
transferability were governed by geographic and climatic proximity, the Manavgat↔Muğla pair should
transfer best. A **negative control** region (Kozan 2023, Türkiye), in which the burned area is
dominated by agricultural stubble burning rather than wildfire, exists in the pipeline registry and
is used only as a validity check on the admissibility gate described in Section 3.3. It is never
used as a transfer partner. Its role is described in Section 3.3 and its gate outcome is reported in
Section 4.1.

## 3.2 Burned-area label and the ~500 m analysis grid

The target variable is burned/unburned status derived from the MODIS MCD64A1 Collection 6
burned-area product, retrieved through Google Earth Engine. Active-fire detections (FIRMS) are never
used as a target.

**Grid reconstruction.** MCD64A1 is a ~500 m product on the MODIS sinusoidal grid, but it is
exported from Earth Engine onto the 30 m EPSG:4326 reference grid used by the rest of the pipeline
(`VALIDATION_LABEL_EXPORT_SCALE = 30`, `core/config.py:262`), which duplicates each native ~500 m
observation across a block of 30 m pixels sharing its value. The analysis grid is therefore
*reconstructed* rather than native: the 30 m reference grid is partitioned into non-overlapping
square blocks of `round(500 / 30) = 17 × 17` pixels (`step8a_prepare_500m_modeling_dataset.py:914 to
917`, using `STEP8A_MCD64A1_NATIVE_CELL_SIZE_M = 500.0` and `STEP8A_REFERENCE_PIXEL_SIZE_M = 30.0`,
`core/config.py:538 to 539`), giving a nominal cell edge of 510 m. This is an approximation of the
true MODIS sinusoidal cell: it is anchored to the Landsat/EPSG:4326 reference grid rather than to
the MODIS tile grid, and blocks at the AOI margin are truncated and therefore contain fewer than 289
constituent pixels. This is stated explicitly because it is a real, and reported, limitation of the
label geometry rather than an incidental implementation detail. Each cell is identified by its
integer block indices `row_500m = row_offset // 17`, `col_500m = col_offset // 17` (`step8a:920 to
936`). These indices are used to construct spatial cross-validation blocks and are never used as
predictors.

The 30 m reference grid itself is the Landsat current-period median LST raster produced upstream,
and every other continuous predictor is required to match it exactly in width, height, CRS and
affine transform. A mismatch is a hard error and the pipeline never silently resamples (`step8a:613
to 643`). The two exceptions are documented and use nearest-neighbour resampling only, because both
layers are categorical: land cover (`step8a:479 to 551`) and the MCD64A1 burn-date raster itself
(`step8a:768 to 814`).

**Label assignment.** Within each 17×17 block, only strictly positive burn-date day-of-year values
are considered; zeros and no-data are ignored. A cell is unburned by default. If positive values
exist, their modal day-of-year is taken as the cell's representative burn date, ties being broken in
favour of the smaller value. For the burned/unburned decision that means the conservative direction
(`step8a:939 to 951`). The representative day-of-year is then converted to a calendar date and
tested against the region's label window: if it falls inside the window the cell is labelled burned,
otherwise the cell is retained as **unburned** and flagged `out_of_window_burndate` (`step8a:1204 to
1248`). The fraction of positive sub-pixels agreeing with the modal date is recorded as a diagnostic
(`burn_date_pixel_agreement_fraction`) but no agreement threshold is imposed. A single in-window
positive sub-pixel is sufficient to label the cell burned.

The label never affects a cell's eligibility for modelling (Section 3.5). Unburned cells,
all-no-data blocks and out-of-window cells all remain in the dataset as the negative class.

**Pre-label burn exclusion.** Optionally, cells that already show a burn detection in the interval
between the start of the predictor window and the start of the label window are excluded from the
analysis universe entirely, so that a predictor window cannot be contaminated by an earlier fire
within the same season (`step8a:2592 to 2605`, using the exclusion manifest produced by the gate
step). Excluded cells are marked `analysis_eligible = False`; their raw labels are preserved for
audit but they never enter modelling.

## 3.3 Burned-landcover admissibility gate

Before any predictor modelling, each region passes through a gate
(`step6b_burned_landcover_gate.py`) that answers one question: **of the cells labelled burned, what
land cover dominates them?** The gate reads only the burn-date raster and the aligned land-cover
raster, and reuses Step8A's block size, cell-identity function and land-cover class map verbatim, so
its cells are identical to the modelling cells.

For each burned cell the modal ESA WorldCover class is taken. Regional fractions are then formed
with the total burned-cell count as denominator: a natural-vegetation fraction (tree cover 10 +
shrubland 20 + grassland 30) and a cropland fraction (class 40). The verdict rule is applied in
order (`step6b:172 to 211`):

1. fewer than `STEP6_BURNED_LANDCOVER_GATE_MIN_POSITIVES = 30` burned cells → *insufficient burned
   positives*;
2. natural-vegetation fraction ≥ 0.50 → **wildfire candidate, pass**;
3. cropland fraction ≥ 0.50 → *cropland-dominated control*;
4. otherwise → *mixed or uncertain*.

Thresholds are at `core/config.py:369 to 373`. The gate is diagnostic: a failing verdict does not
halt the pipeline, and the gate output always carries `downstream_authorized: False`, requiring
explicit review. Its role in this study is to establish that the regions entering the transfer
experiment are genuine forest-fire regions. Per-region verdicts and natural-vegetation fractions are
read from each region's frozen `burned_landcover_gate.json` and reported in Section 4.1.

**Negative control.** A gate that every candidate region passes carries no information, so the
threshold is calibrated against a region that should fail it. MCD64A1 does not distinguish the
combustion of natural fuel from the deliberate burning of harvest residue: both are detected as
burned area, and a model trained on the latter would be learning agricultural calendar rather than
fire-relevant dryness. Kozan 2023 (Adana province, Türkiye) was therefore processed through the
identical Step 1 to 6 pipeline as a negative control. It is not a wildfire region: its burned area
lies in the Çukurova agricultural plain and is dominated by post-harvest stubble burning. The gate
receives it blind. It sees only the burn-date raster and the land-cover raster, with no regional
label, and the verdict follows from rule 3 above. The control is reported in Section 4.1 and enters
no modelling, transfer or diagnostic analysis. No Kozan number appears anywhere else in this paper.

## 3.4 Predictor variables

All dynamic predictors are composited over the region's predictor window; static predictors are
time-invariant. Each is produced by a named upstream pipeline stage and delivered on the 30 m
reference grid.

**Optical greenness (NDVI).** Landsat Collection 2 Level-2 surface reflectance, scaled by 0.0000275
with an offset of −0.2, is used to compute NDVI = (NIR − Red)/(NIR + Red); pixels with a near-zero
denominator or values outside [−1, 1] are masked (`core/config.py:89 to 103`). The predictor-window
composite is a per-pixel **median**.

**Land surface temperature (Landsat).** The Landsat Level-2 surface temperature band is scaled by
0.00341802 with an offset of 149.0 K and converted to degrees Celsius. The predictor-window
composite is again a per-pixel median (`current_lst`, in °C). This raster also serves as the 30 m
reference grid.

**LST anomaly.** A z-score of the current-window LST median against the baseline-years distribution
for the same calendar window: `(current_median − baseline_mean) / baseline_std`
(`step5_preprocess_timeseries.py:837 to 847`). The anomaly is set to no-data where the baseline
standard deviation is below `STEP5_MIN_BASELINE_STD_CELSIUS = 1.0` °C, where fewer than
`STEP5_MIN_CURRENT_VALID_COUNT = 2` current observations exist, or where fewer than
`STEP5_MIN_BASELINE_VALID_COUNT = 3` baseline observations exist. The result is dimensionless.

**TVDI and TVDI difference.** The Temperature-Vegetation Dryness Index is computed in the LST-NDVI
feature space (`step5c_tvdi.py`). The NDVI range [0, 1] is divided into `TVDI_NDVI_BIN_COUNT = 20`
bins. Within each bin holding at least `TVDI_MIN_PIXELS_PER_BIN = 30` valid pixels, the wet and dry
edges are taken as the 2nd and 98th LST percentiles (`TVDI_WET_EDGE_PERCENTILE = 2.0`,
`TVDI_DRY_EDGE_PERCENTILE = 98.0`). TVDI is then `(LST − wet_edge) / (dry_edge − wet_edge)`, clamped
to [0, 1]. It is set to no-data where the edge span is below `MIN_TVDI_EDGE_SPAN_C = 1.0` °C
(`core/config.py:162 to 178`). `tvdi_difference` is the current-window TVDI minus the baseline-years
mean TVDI. A documented caveat applies to the latter: the baseline TVDI is formed from a single
baseline LST mean raster combined with per-year NDVI, so its inter-annual variation derives from
NDVI alone (`step5c_tvdi.py:480 to 486`).

**Downscaled and fused LST.** To mitigate Landsat's sparse thermal revisit, a MODIS→Landsat
downscaling model is trained on the predictor window and applied to the full 30 m grid (`step7c`,
`step7d`), yielding `downscaled_lst` in °C, clipped to configured physical bounds. The downscaling
stage is explicitly leakage-guarded: it never sees MCD64A1 or FIRMS labels, and is prevented from
ingesting the anomaly, TVDI or TVDI-difference layers as inputs (`step7d_predict_downscaled_lst.py:1
to 30`). A fused product (`fused_lst`, °C) then combines observed Landsat LST with downscaled LST as
**gap-fill only**. Valid observed pixels are never replaced or blended
(`step7e_fuse_landsat_downscaled_lst.py:1 to 26`). A companion source mask records, per pixel,
whether the fused value is observed, gap-filled or invalid. The corresponding per-cell fractions are
retained as sensitivity diagnostics and are **never** used as predictors.

**Terrain.** Elevation (m a.s.l.) and slope (degrees, from `ee.Terrain.slope`) are derived from the
Copernicus DEM GLO-30 (ESA, 30 m global digital surface model;
`https://dataspace.copernicus.eu/explore-data/data-collections/copernicus-contributing-missions/collections-description/COP-DEM`,
accessed 2026-08-08), accessed as the `COPERNICUS/DEM/GLO30` Earth Engine collection. USGS SRTMGL1
v003 is configured as a fallback should the preferred collection be unavailable (`core/config.py:61
to 80`). The frozen Step 2B metadata records `used_fallback: false` for every region, so all
reported elevation and slope values come from GLO-30 and the fallback was never exercised. Because
GLO-30 is a mosaicked collection without a fixed projection, slope is computed on the DEM's native
projection before reprojection, not after (`step2b_dem.py:148 to 159`). Both bands are exported at
30 m.

**Land cover.** ESA WorldCover v200 (10 m native, 2021 epoch), nearest-neighbour aligned to the 30 m
reference grid. Class codes: 10 tree cover, 20 shrubland, 30 grassland, 40 cropland, 50 built-up, 60
bare/sparse vegetation, 70 snow/ice, 80 permanent water, 90 herbaceous wetland, 95 mangroves, 100
moss/lichen.

## 3.5 Cell-level aggregation, validity mask and analysis population

**Aggregation.** For each continuous predictor and each 17×17 block, the mean, median, standard
deviation, valid-pixel count and valid-pixel fraction of the finite 30 m values are computed
(`step8a:954 to 963`). Modelling uses the block **mean** of each predictor. For land cover, the
modal class (`landcover_dominant`) and per-class area fractions are computed over valid land-cover
pixels within the block.

**Validity.** A cell is `valid_for_modeling` if and only if all four of the following hold
(`step8a:1399 to 1422`):

1. it is analysis-eligible, meaning it was not excluded as a pre-label burn;
2. at least `STEP8A_MIN_30M_VALID_FRACTION = 0.3` of its 30 m pixels have simultaneously finite
   NDVI, elevation and slope;
3. its aggregated NDVI, elevation and slope means are each finite;
4. it contains at least one valid land-cover pixel. Thermal predictors deliberately do **not** enter the validity test, so
that thermal data availability cannot silently reshape the population differently for the two
feature sets. The label likewise plays no part in the validity test. That is a design point made
explicit in the source, since requiring a valid burn date would collapse the dataset to burned-like
cells.

**Analysis population.** The **primary** population is natural vegetation: cells that are
`valid_for_modeling` and satisfy `burnable_tree_shrub_grass`, defined as a combined tree + shrubland
+ grassland **area fraction ≥ `STEP8A_BURNABLE_FRACTION_THRESHOLD` = 0.50** within the cell
(`step8a:1326 to 1329`). Cropland is explicitly excluded from every burnable mask and only ever
reported as its own fraction. Restricting to natural vegetation removes the confound in which
agricultural stubble burning and bare-surface thermal contrast could be mistaken for wildfire skill;
it is the scientifically defensible population for the transfer question, and, as the analysis
shows, the choice materially changes the conclusion. The mixed population of all valid cells
(`all_valid`) is retained throughout as a **secondary sensitivity** analysis, and both populations
are reported for every headline quantity.

Two definitional asymmetries are noted for transparency: the burnable mask is an **area-fraction**
test, whereas the admissibility gate of Section 3.3 uses the **modal** class; and the upstream
within-region pipeline's own configured primary population is `all_valid`
(`STEP8B_PRIMARY_POPULATION`, `core/config.py:559`), whereas the transfer analysis reported here
takes natural vegetation as primary. All comparisons in this paper are computed on the *same*
population and the *same* classifier configuration. This holds for the within-region reference,
naive transfer and adapted transfer alike, which is what makes the decomposition of Section 3.12
valid.

`burnable_tree_shrub_grass` is used exclusively as a population mask and is never a feature.

## 3.6 Feature sets

Two nested feature sets are compared (`step8b_train_baseline_vs_thermal_model.py:121 to 135`):

- **Baseline (4 predictors):** `ndvi_mean`, `elevation_mean`, `slope_mean`, `landcover_dominant`.
- **Thermal (10 predictors):** the baseline set plus `lst_anomaly_mean`, `current_lst_mean`,
  `current_tvdi_mean`, `tvdi_difference_mean`, `downscaled_lst_mean`, `fused_lst_mean`.

The thermal set is a strict superset of the baseline set, so the difference in performance between
them is attributable to the six thermal channels alone. `landcover_dominant` is the only categorical
predictor.

**Table 2** (feature dictionary: variable, source product, producing pipeline stage, unit, temporal
window, feature-set membership) is assembled from Section 3.4.

## 3.7 Classifier and preprocessing

All models are random forests with identical hyperparameters across the within-region, transfer and
adaptation experiments (`step8b:420 to 429`):

```
RandomForestClassifier(n_estimators=300, max_depth=None, min_samples_leaf=3,
                       class_weight="balanced", random_state=42, n_jobs=-1)
```

with scikit-learn defaults otherwise (`criterion="gini"`, `max_features="sqrt"`,
`min_samples_split=2`, bootstrap resampling of training rows). `class_weight="balanced"` compensates
for the strong class imbalance (burned prevalence of a few per cent). The configuration is chosen
once and never tuned against any evaluation the paper reports. A second, unweighted profile with
`min_samples_leaf=2` is retained solely as a sensitivity check.

Preprocessing is a scikit-learn `Pipeline` fitted **inside** each training fold (or, for transfer,
on the source region only), so that no imputation or encoding statistic is derived from evaluation
data (`step8b:449 to 467`): numeric predictors are median-imputed; `landcover_dominant` is
mode-imputed and one-hot encoded with `handle_unknown="ignore"`, so that a land-cover class present
in the evaluation set but absent from the training set produces an all-zero indicator row rather
than an error. This is what makes the one-hot column space consistent between regions in the
transfer experiments: it is fixed by the source region. No feature scaling is applied in the
within-region models, as the classifier is scale-invariant.

## 3.8 Spatial-block cross-validation and block-size robustness

Within-region evaluation uses **spatially blocked** cross-validation. Contiguous square blocks of `B
× B` analysis cells are formed at a fixed origin from the grid indices, `block_row = row_500m // B`,
`block_col = col_500m // B` (`step8b:277 to 306`), and the resulting block identifier is used as the
grouping variable in `StratifiedGroupKFold` with `n_splits = 5`, `shuffle=True` and `random_state =
42` (`step8b:309 to 414`; `core/config.py:554 to 556`). Blocks are therefore never split between
training and test folds, and class stratification is preserved across folds. Fold construction is
guarded: at least two test folds must contain a positive, and the pipeline is explicitly forbidden
from ever falling back to a random row-wise split.

Both feature sets are fitted on the **same folds**, so the baseline-versus-thermal comparison is
paired by construction. Out-of-fold predicted probabilities are assembled into a single vector per
feature set, covering every cell exactly once, and metrics are computed once on the concatenated
out-of-fold vector rather than averaged over folds (`step8b:519 to 690`).

**Block size and robustness.** The pipeline's default block size is `STEP8B_SPATIAL_BLOCK_SIZE_CELLS
= 2`, i.e. 2 × 2 cells ≈ 1 km. Because the appropriate blocking scale is not knowable a priori and
short-range spatial autocorrelation can survive fine blocking, the whole within-region analysis is
repeated at **B = 2, 10 and 20 cells (≈ 1, 5 and 10 km)**, on both populations. A thermal increment
that persists as blocks coarsen is evidence of genuine spatial generalisation rather than of
neighbour leakage. The trade-off is that coarser blocking also reduces the number of independent
groups available for cross-validation and for bootstrap resampling, which widens the intervals.

**Metrics.** Threshold-free discrimination is reported as ROC-AUC and PR-AUC (average precision);
the Brier score is computed as a calibration diagnostic. Threshold-dependent quantities (balanced
accuracy, precision, recall, F1) are recorded at a fixed 0.5 cut-off within regions but are not used
for the paper's claims (`step8b:480 to 503`). The primary quantity of interest is the paired
difference ΔAUC = AUC(thermal) − AUC(baseline) on the same out-of-fold predictions.

## 3.9 Spatial-block bootstrap uncertainty

Uncertainty is quantified by a **spatial-block bootstrap** operating on stored predictions, with no
refitting (`step8c_spatial_block_bootstrap_uncertainty.py`). The resampling unit is the spatial
block, not the cell: in each replicate, `n_blocks` blocks are drawn with replacement from the
`n_blocks` unique blocks, and a block drawn *k* times contributes all of its cells *k* times
(`step8c:278 to 351`). Resampling cells individually would treat spatially autocorrelated neighbours
as independent and produce intervals that are far too narrow. This was an error we made and
corrected during this study (Section 3.12).

The number of replicates is 1000 and the seed is 42 (`core/config.py:574 to 575`). Intervals are
**equal-tailed percentile** intervals at the 2.5th and 97.5th percentiles. No bias correction or
acceleration (BCa) is applied. Replicates in which a resample contains only one class are recorded
and excluded from the percentiles rather than silently redrawn. A warning is raised if more than 10%
of replicates are invalid.

The bootstrap is **paired**. Within each replicate, both the baseline and thermal probability
vectors are evaluated on the identical resampled index, and the difference is formed inside the
replicate. The interval is therefore on the distribution of the paired ΔAUC. The same paired
construction is used in the transfer experiments, where a single set of resampled target blocks per
replicate is shared by all probability series (within-region reference, raw transfer, z-scored
transfer, CORAL transfer) so that they remain directly comparable.

Following the pipeline's own reporting policy, no classical p-values or significance tests are
reported. A result is described as having **positive bootstrap support** when the 95% percentile
interval for ΔAUC excludes zero, and as **uncertain** otherwise. This is a statement about an
interval, not a hypothesis test.

Block sizes used for the bootstrap match the analysis they accompany: B = 2 for the transfer scores,
B matched to the cross-validation blocking (2, 10, 20) for the within-region robustness analysis,
and B = 10 (≈ 5 km) for the univariate concept-shift diagnostic of Section 3.12.

## 3.10 Cross-region transfer protocol

For each ordered pair of regions (source → target), a model is fitted on the **entire** source
region, using all cells in the analysis population with no held-out fold, and applied to the entire
target region. All ordered pairs among the completed regions are evaluated in both directions.

Every fitted component is derived from the source region only: the numeric imputation medians, the
categorical mode, the one-hot category vocabulary, and the random forest itself. The target region
enters the computation exactly once, at `predict_proba`. There is no pooled fitting, no
target-derived imputation, no target fine-tuning, no calibration on the target, and no coordinate or
region-identity feature (`step9b_run_cross_region_transfer.py:230 to 236, 370 to 381`). The
classifier, hyperparameters, seed and feature contract are imported from the within-region stage
rather than redefined, so the transfer model is the same model.

Feature harmonisation across regions requires no separate alignment step: the shared feature list is
frozen and validated by an audit stage that fails on any schema mismatch, and the source-fitted
one-hot encoder with `handle_unknown="ignore"` guarantees identical column ordering and dimension at
target-prediction time. Land-cover classes present in the target but not the source encode to zero.

Both source and target must contain at least 30 positive and 30 negative cells in the population
being evaluated, otherwise the pair is skipped.

**Target metrics** are threshold-free: ROC-AUC and PR-AUC, with spatial-block bootstrap intervals as
in Section 3.9, computed on the target region's blocks. A ROC-AUC below 0.5 is reported as such and
is interpreted as an anti-predictive transfer, in which the source-learned ordering is
systematically inverted in the target. It is not folded to `max(AUC, 1 − AUC)`. Both the baseline
and the thermal feature set are fitted and evaluated under this protocol for every ordered
direction, so the per-direction paired baseline-versus-thermal transfer contrast reported in the
Results is a read-only extraction from these frozen outputs, taking point estimates from the
transfer stage's `baseline_metrics`/`thermal_metrics`, and paired ΔAUC intervals from the transfer
bootstrap's `delta_roc_auc` field, which evaluates both probability series on identical resampled
target blocks as in Section 3.9 (extraction script `paper/baseline_vs_thermal.mjs`; no new models
fitted).

## 3.11 Label-blind domain adaptation

Three transfer variants are compared. All are strictly **label-blind**: the target frame is
structurally stripped of the response before adaptation, and an assertion fails the run if a label
column is present (`step10b_label_blind_adaptation.py:71 to 79`; `core/step10_shared.py:243 to
250`). No adaptation function accepts labels as an argument.

**(a) Raw.** The source-fitted model applied directly to untransformed target features (Section
3.10).

**(b) Region-wise z-score.** Each region's numeric features are standardised using **its own**
statistics: `z = (x − μ_region) / σ_region`, with the mean and standard deviation computed over
non-missing values only and `ddof = 0` (`step10_shared.py:145 to 173`). A near-constant feature (σ <
10⁻¹²) has its divisor set to 1 and the substitution is recorded. Missing values are filled with the
region's own mean, hence map to exactly zero after transformation. The categorical land-cover
predictor is left untouched. Source statistics come from source data and target statistics from
target data. The two regions are never pooled. The classifier is then refitted on the z-scored
source and applied to the z-scored target. This variant removes first- and second-order marginal
offsets between regions. It is the simplest possible self-calibration.

**(c) CORAL after region-wise z-score.** Starting from the z-scored features of (b), the source
covariance is aligned to the target covariance by the standard CORAL whitening-recolouring map
(`step10_shared.py:186 to 220`):

```
C_s = cov(X_s^z) + λI ,   C_t = cov(X_t^z) + λI
A   = C_s^(−1/2) · C_t^(1/2)
X_s* = X_s^z · A
```

with covariances computed at `ddof = 0` and matrix powers obtained by symmetric eigendecomposition
with eigenvalues floored at 10⁻¹². The regularisation is `STEP10_CORAL_LAMBDA = 1e-5`
(`core/config.py:697`). Critically, **the transform is applied to the source only**. The target
remains exactly as in (b). The classifier is refitted on the aligned source and applied to the
unchanged z-scored target.

**On the choice of λ.** The canonical CORAL formulation adds the identity (λ = 1) to each
covariance, but it is defined for unstandardised features. Here CORAL is applied *after* region-wise
standardisation, so each feature already has unit variance and adding the full identity doubles the
diagonal, imposing shrinkage strong enough to erase the covariance structure the alignment is meant
to exploit. With only nine numeric features and thousands of cells per region, the covariances are
well estimated and minimal regularisation is appropriate. Because this is a defensible but not
inevitable choice, λ sensitivity is assessed on the four Bejís↔Muğla and Manavgat↔Muğla directions
over a nine-value grid from 0 to 10⁻¹ (0, 10⁻⁸ … 10⁻¹). The resulting spread in transfer AUC is at
most 0.008 within any direction (Section 4.7d). The sweep does not extend to λ = 1 or to the
Montiferru and Evia directions, so conclusions for those directions rest on the default λ = 10⁻⁵
alone.

The order of operations for variant (c) is thus: region-wise z-score of both regions → CORAL
alignment of the source numerics only → the standard median-imputation + one-hot pipeline →
random-forest fit on source → prediction on target.

## 3.12 Transfer-gap decomposition and concept-shift diagnostic

**Decomposition.** For each ordered pair, the transfer deficit is decomposed against the target
region's own within-region performance:

- `total_gap      = AUC_within(target) − AUC_raw(source→target)`
- `recovered      = AUC_adapted(source→target) − AUC_raw(source→target)`
- `concept_remaining = AUC_within(target) − AUC_adapted(source→target)`

where `AUC_within` is the target region's own spatially blocked out-of-fold thermal ROC-AUC. All
three terms are computed on the **same population, same feature set, same classifier configuration
and same block size**, which is what makes them commensurable. A decomposition assembled from
components with differing populations or classifier settings would not be interpretable.

The `recovered` term is defined using the **best-performing label-blind method** among (b) and (c),
because the question it answers is "how much of the gap *can* label-free alignment close?", whose
answer is bounded by the best available label-free method. The weaker method's decomposition is
reported as a secondary row rather than discarded, since choosing the weaker method as the numerator
would understate the recoverable fraction and overstate concept shift.

**Concept-shift diagnostic.** To identify the mechanism behind the residual, a **signed** univariate
ROC-AUC is computed for every numeric feature against the burned label, independently in each
region's analysis population. The AUC is deliberately *not* folded to `max(AUC, 1 − AUC)`, so that
the direction of association is preserved: a value above 0.5 means higher feature values are
associated with burning, below 0.5 means the opposite. A feature is said to show a **point
reversal** when its univariate AUC falls on opposite sides of 0.5 in the two regions, and a
**bootstrap-supported reversal** only when the two regions' spatial-block bootstrap intervals are
additionally **disjoint**.

The block size for this diagnostic is B = 10 cells (≈ 5 km). An earlier version of the analysis used
B = 2 (≈ 1 km) and, by ignoring short-range spatial autocorrelation, produced intervals roughly four
times too narrow, which wrongly promoted several point reversals to bootstrap-supported. The
correction is reported here because it materially weakened one of the study's own claims: at the
appropriate blocking scale, far fewer reversals survive as statistically supported, and the
manuscript reports the conservative result.

The logical role of this diagnostic is specific. Region-wise standardisation and covariance
alignment can only translate, scale and rotate the feature distribution; neither can invert the sign
of a feature's association with the response. A bootstrap-supported reversal is therefore direct
evidence for a shift component that no label-free alignment can repair, and connects the empirical
decomposition to a mechanism.

## 3.13 Leakage control, sensitivity analyses and reproducibility

**Leakage control.** An explicit forbidden-column set is enforced at every model fit, and its
violation raises rather than warns (`step8b:140 to 159, 265 to 271, 450`). It contains the response
itself and every column carrying label information: `burn_date`, `burn_month`, `burn_day_of_year`,
`label_source`, `burn_date_pixel_agreement_fraction`, `out_of_window_burndate` It also contains
`lon`, `lat`, `cell_id`, `row_500m`, `col_500m`, the validity columns, and the fused-LST provenance
columns (`source_mask_majority`, `observed_fraction`, `gapfilled_fraction`,
`invalid_source_fraction`). The transfer stage additionally forbids `experiment_id`, `region_key`,
`spatial_block_id` and `fold_id`.

Coordinates are excluded because a fire scar is a spatially compact object: with longitude and
latitude available, a sufficiently flexible model can memorise the scar's location instead of
learning any relationship with the surface state. Grid indices are used only to construct
cross-validation blocks and bootstrap groups. The natural-vegetation mask is used only to define the
population. The fused-LST provenance fractions are retained for a sensitivity analysis, which
restricts performance to cells with a low gap-filled fraction, but never as predictors.

**Sensitivity analyses.** Every headline result is repeated across: two analysis populations
(natural vegetation, primary; all valid cells, secondary); two random-forest profiles (the primary
weighted `min_samples_leaf = 3` configuration and an unweighted `min_samples_leaf = 2` profile);
three spatial-block sizes for the within-region analysis (≈ 1, 5, 10 km); four CORAL regularisation
values; and both feature sets. Where a conclusion depends on one of these choices, the dependence is
reported rather than resolved by selecting the favourable setting.

**Reproducibility.** All randomness uses seed 42, covering model `random_state`, cross-validation
shuffling and bootstrap generators alike. The bootstrap uses 1000 replicates throughout. The
transfer and adaptation analysis is executed in a dedicated Python environment separate from the
upstream pipeline environment; because random-forest fits are not bit-identical across scikit-learn
versions, the analysis includes an explicit reproduction check in which the within-region models are
refitted in the new environment and compared against the frozen upstream outputs, and the
independently implemented adaptation is compared against the pipeline's own implementation. All
numbers reported in this paper were produced under, or verified against, scikit-learn 1.9.0: two
frozen transfer probes reproduce to four decimal places under 1.9.0 but move by +0.021 and +0.026
AUC under 1.7.2 with byte-identical data, pipeline and seed, so cross-region point estimates carry
an implementation tolerance of roughly ±0.02 to 0.03 unless the exact library version is fixed.
Within-region AUCs reproduce to ~4 decimals across versions (`paper/sklearn_version_sensitivity.md`;
probe script `paper/pairwise_check.py`).

The reproduction check was executed on the final five-region set by the pipeline author, and its
record is archived with this manuscript (`paper/reproduction_check/reproduction_check_5region.json`,
SHA-256 `7f7e41f5…09c8be`; commit `48b56e7`, Python 3.12.3, scikit-learn 1.9.0, pandas 3.0.2, NumPy
2.4.4, primary population `burnable_tree_shrub_grass`). Two families of comparison were re-executed
against the frozen outputs. The within-region arm refitted `step8b`'s baseline and thermal models on
the frozen Step 8A parquet of each of the five experiments and compared ROC-AUC and PR-AUC. All
twenty comparisons were produced, with a **maximum absolute difference of exactly 0**. The transfer
arm regenerated the label-blind CORAL predictions and re-evaluated them for all twenty directed
region pairs, again in both model families and both metrics. That is eighty comparisons over twenty
directions, none missing, with a **maximum absolute ROC-AUC difference of 1.6×10⁻⁷** (largest case
Montiferru→Manavgat, thermal: 0.6060780 against 0.6060778); sixty-nine of the eighty comparisons
were bit-identical and the remaining eleven differed by 1.6×10⁻⁷ or less.

The tolerance against which these differences are judged is not a criterion chosen for this report.
It is the repository's own pre-existing Step 10C fail-fast reproduction criterion, an absolute
difference of ≤ 1×10⁻⁶ defined in `src/step10c_paired_evaluation_bootstrap.py`. It is applied
unchanged, and the check record states this explicitly. Both arms fall inside it, the within-region
arm by exact equality. The reported `PASS` is a technical-completion status covering cohort
resolution, comparison coverage and input-hash agreement. The achieved numerical differences are
reported separately, as above, rather than folded into that status.

What this check does and does not establish should be stated plainly. Because it re-executes the
pipeline in the same library environment that produced the frozen outputs, the exact-zero
within-region agreement demonstrates determinism and the absence of undeclared state, meaning that
the recorded numbers are regenerable from the recorded inputs, hashes included. It does not
demonstrate robustness to a change of environment. The residual 10⁻⁷-scale differences in the
transfer arm arise from re-derived rather than re-read intermediate quantities, not from a different
library stack. Cross-version behaviour is established separately and is far coarser: the ±0.02 to
0.03 implementation tolerance quoted above, from the 1.9.0-against-1.7.2 probes. The two statements
are complementary and neither substitutes for the other.

Two further properties of the record are stated for completeness. First, the five-region cohort was
resolved by three independent routes. These are the experiment registry restricted to canonical
records (those carrying no `superseded_by` key, which drops the legacy Evia AOI of Section 3.16.1
and the superseded Muğla calendar-shift record) and with non-cohort roles removed, the ERA5-Land
diagnostic's `DEFAULT_EXPERIMENTS` constant, and the frozen multi-AOI synthesis manifest. All three
return the same ordered set (`routes_agree: true`). The two deliberate exclusions by role are Kozan
2023 as `negative_control` and the second Muğla event as `temporal_transfer_wildfire` (Sections 3.1,
3.3, 3.16.4). The roles and the supersession links are as recorded in `core/regions.py`. Second, two
unordered region pairs carry duplicate Step 10 namespaces on disk under reversed directory orderings
with distinct analysis identifiers (Bejís-Muğla and Manavgat-Muğla). The reference artefact was
selected by the frozen synthesis manifest rather than by directory listing, and the check record
names both the paths present and the one used for each pair. No file belonging to the upstream
pipeline or to previously frozen outputs was modified by this analysis.

**Data and code availability.** The satellite inputs are all public and are obtained through Google
Earth Engine. They are MODIS MCD64A1 Collection 6 burned area, MODIS land surface temperature,
Landsat Collection 2 Level-2 surface reflectance and surface temperature, Copernicus DEM GLO-30, and
ESA WorldCover v200. No data were collected by the authors and no restricted or licensed data were
used. The region definitions, date windows and thresholds given in this section are sufficient to
regenerate every input from these sources.

The full processing pipeline (Steps 1 to 10), its configuration constants, and the frozen numeric
outputs on which every reported number rests are publicly available at
`https://github.com/emrehann17/satellite-thermal-digital-twin`. The repository is the authoritative
source for the file and line references cited throughout this section. Analysis code is released
under the repository's stated licence (MIT). No digital object identifier is minted for this
release, and readers should cite the repository URL together with the commit identifier
corresponding to the version of record.

## 3.14 Transferability diagnostics versus transfer

To test whether any pre-transfer measure of region similarity predicts transfer outcome, twenty
candidate diagnostics from four families are each evaluated against the same target quantity under
one common correlation framework. The families are marginal predictor-distribution measures P(x),
burned-niche overlap P(x|y=1), fire-regime spatial structure P(y), and conditional feature-response
direction P(y|x).

### 3.14.1 Rank-correlation framework

The target quantity is the raw thermal transfer ROC-AUC of Section 3.10 on the natural-vegetation
population, over the 20 ordered directions (12 for measures available only on the four-region subset
excluding Montiferru). For each diagnostic, Spearman's ρ and Kendall's τ-b (tie-corrected) are
computed against the transfer AUCs. Uncertainty uses a **pair-based bootstrap**: the unordered
region pairs (10, or 6 for the subset) are resampled with replacement, and every sampled pair
contributes **both** of its ordered directions. The two directions of a pair share geography and
data, so they are never treated as independent draws. 2,000 replicates are used with equal-tailed
percentile 95% intervals; replicates yielding degenerate (undefined) rank correlations are excluded
and counted. All resampling is seeded from 42 with fixed per-measure offsets and implemented with
the mulberry32 PRNG in Node.js. It is fully deterministic, though not bit-identical to NumPy's
generator (`paper/regime_correlation.mjs`, `paper/niche_corr.mjs`,
`paper/conditional_similarity.mjs`). Because the effective sample is 10 (or 6) unordered pairs that
share member regions, power is low. A null result is reported as "not shown to order transfer",
never as "shown not to".

### 3.14.2 Marginal measures and the domain classifier

Six marginal diagnostics are consumed unchanged from the upstream marginal/area-of-applicability
audit (12 directed pairs, four-region subset;
`drive_new/diagnostics/marginal_aoa_completion/4b2a1c86…/comparison/marginal_diagnostics_with_transfer.csv`):
target mean and 95th-percentile predictor-space dissimilarity, fraction of target cells inside the
weighted area of applicability, and fraction inside the unweighted support (all directed), plus
climatic distance and geographic centroid geodesic distance (symmetric). Marginal separability is
additionally measured for all ten pairs by a **domain classifier** trained to distinguish source
from target cells. It uses the same 10-predictor feature contract
(`step9_shared_baseline_thermal_v1`), the step8b preprocessing pipeline reused unmodified, and the
random-forest configuration of Section 3.7, evaluated as spatially blocked out-of-fold ROC-AUC using
`StratifiedGroupKFold` over deterministic 10-cell (≈5 km) blocks namespaced per region (5 splits,
seed 42, strict zero-overlap folds), with a paired two-domain spatial-block bootstrap (1,000
replicates, seed 42, blocks resampled with replacement independently within each domain). Burned
labels are never used. Design read from
`drive_new/diagnostics/domain_classifier_audit/comparison/manifest.json` and the per-pair manifests.

### 3.14.3 Burned-niche overlap

Niche overlap compares the two regions' burned-cell feature distributions, P(x|y=1), using burned
cells of the primary population only (`valid_for_modeling` ∧ `burnable_tree_shrub_grass` ∧ `burned =
1`; no unburned variant by design). Schoener's D = 1 − ½Σ|p − q| and Warren's I = 1 − ½Σ(√p − √q)²
are computed in two ways. The first is per numeric feature on 1-D histograms with 50 shared bins
spanning the **global** range of all five regions' burned cells, averaged over the nine features,
and (b) on a 20 × 20 histogram over the first two components of a global PCA fitted to the pooled,
globally standardised (ddof = 0) burned cells of all five regions, with missing values imputed by
the pooled median. The Mahalanobis distance between standardised burned centroids uses the pooled
covariance ((n_a − 1)S_a + (n_b − 1)S_b)/(n_a + n_b − 2) over the nine features. All measures are
symmetric per unordered pair (`paper/niche_overlap.py`; correlation with transfer via
`paper/niche_corr.mjs`).

### 3.14.4 Conditional sign-agreement index

For each region a nine-dimensional vector of **signed** univariate AUCs (Section 3.12: the
probability that a burned cell carries the higher feature value; never folded about 0.5) is taken,
with its ≈5 km-block bootstrap intervals, from the upstream five-region feature-stability table
(`drive_new/diagnostics/multi_aoi_transfer_synthesis/<five-region
set>/multi_aoi_feature_stability.csv`, step9g family). Pair-level measures: sign-agreement count and
fraction (features whose AUC − 0.5 signs match), the Spearman correlation between the two vectors,
and the cosine similarity of the (AUC − 0.5) vectors. Each is also computed restricted to
**supported** features, which are those whose bootstrap interval excludes 0.5 in *both* regions.
Consistency is enforced: per-region vectors must be identical across every pair row, and the
supported-reversal set must reproduce the upstream `reversal_status` flags exactly
(`paper/conditional_similarity.mjs`). Unlike every marginal, niche and regime measure, this index
requires burned labels (or a labelled probe) in **both** regions: it diagnoses concept alignment and
is not a label-free deployment screen.

### 3.14.5 Fire-regime structure

Burned-area spatial structure, P(y), is summarised by connected components of burned
natural-vegetation cells, computed with 8-connectivity on the integer grid indices
`row_500m`/`col_500m`. Per region: component count, largest-component share, and the effective
component count, the inverse Simpson index of component size shares, 1/Σ s_k². The pair-level regime
distance is |Δ log(effective count)| (primary) and |Δ largest share| (secondary), both symmetric.
The implementation was verified to reproduce the upstream burned-pattern audit ("Rejim" table)
exactly in all five regions, for component counts and largest/second component sizes identically,
shares and effective counts to 1 × 10⁻⁴ (`paper/burned_components.mjs`).

## 3.15 Interventions

### 3.15.1 Pooled multi-region training (leave-one-region-out)

For each held-out target region, the other four regions' primary (natural-vegetation) populations
are pooled and a single model is trained on the pool and evaluated on the untouched target, for both
feature sets. The classifier is exactly that of Section 3.7, and preprocessing mirrors the transfer
stage: numeric medians fitted on the pooled training set, mode-filled land cover expanded to
indicator columns from the training vocabulary so that unseen target classes encode to zero. Two
variants are run: raw features, and region-wise z-score in which every region, the target included,
is standardised with its own mean and σ (ddof = 0, numeric features only), i.e. the label-free
definition of Section 3.11(b). Target metrics are ROC-AUC, PR-AUC (reported against its no-skill
base, the prevalence) and Brier, with a ≈5 km spatial-block bootstrap on the target (blocks
`row_500m//10` × `col_500m//10`, 1,000 replicates, NumPy `default_rng(42)`, single-class replicates
excluded) (`paper/loro_pooled.py`). The analysis was run under scikit-learn 1.9.0 only after two
frozen pairwise transfers were reproduced to four decimal places in the same environment
(`paper/pairwise_check.py`; Section 3.13).

### 3.15.2 Removal of direction-reversing features

Four thermal-model configurations are compared: full (all 10 predictors, order preserved from the
shared feature contract), minus `elevation_mean`, minus `lst_anomaly_mean`, and minus both. The two
features being exactly the bootstrap-supported reversal set under the supported-reversal criterion
of Section 3.14.4. The pipeline replicates step8b/step9b verbatim (same imputers, one-hot encoding,
classifier and seed), and **hard parity assertions** abort the run on any deviation of the full
configuration from the frozen outputs, with a tolerance of 5 × 10⁻⁴ against the 20 step9b transfer
AUCs and 1 × 10⁻³ against the step8c within-region out-of-fold AUCs. The observed deviations were
0.0000 everywhere. Within-region evaluation reuses the spatially blocked out-of-fold protocol of
Section 3.8 (2-cell blocks, `StratifiedGroupKFold`, seed 42). All deltas (configuration minus full)
are formed inside each replicate of a paired ≈5 km-block bootstrap (10-cell blocks, 1,000
replicates, `default_rng(42)`), so every interval is on the paired difference
(`paper/feature_drop.py`; report `paper/feature_drop_transfer.md`).

## 3.16 Additional sensitivity designs

### 3.16.1 Evia AOI (legacy versus extended)

North Evia exists in two AOI definitions with identical predictor and label windows: the legacy
0.40° × 0.40° box and the canonical extended 0.80° × 0.60° box (Table 1), whose ≈3× larger area
leaves the burned scar essentially unchanged while reducing prevalence substantially (Section 4.1).
Both AOIs were processed through the full pipeline, and both transfer arms (baseline and thermal,
Section 3.10) were run for every Evia-involved direction under each AOI
(`drive_new/cross_region/<pair>/step9b/cross_region_transfer_metrics.json` for the legacy and
extended pair folders). The extended AOI is canonical everywhere in this paper. The legacy AOI is
retained **only** to test whether AOI extent and the induced prevalence change alter any transfer
conclusion.

### 3.16.2 Montiferru tree+shrub population

Montiferru is the weakest admissibility-gate pass (burned cropland fraction 0.274), so a stricter
population variant excluding grassland is examined: `burnable_tree_shrub`, present alongside
`burnable_tree_shrub_grass` in the frozen within-region bootstrap populations
(`drive_new/experiments/montiferru_2021/step8c/step8c_bootstrap_metrics.json`,
`bootstrap_ci_by_population`) and in the transfer bootstrap groups of every Montiferru pair
(`drive_new/cross_region/montiferru_2021__*/step9c/cross_region_bootstrap_metrics.json`). The
within-region thermal ΔAUC and the eight Montiferru-involved cross-region thermal-versus-baseline
deltas are compared between the two populations, reading the frozen outputs only. No new models are
fitted for this check.

### 3.16.3 Predictor-window closure

A predictor-timing sensitivity, described here as documented in each region's frozen comparison
report
(`drive_new/diagnostics/window_closure_region/<region>/<hash>/_production/<region>/compare/report/window_closure_comparison.md`
for Bejís, Muğla, Evia-extended and Montiferru;
`drive_new/diagnostics/window_closure_sensitivity/manavgat_2021/compare/report/window_closure_comparison.md`
for Manavgat). Three variants are compared: canonical, closure 7 days earlier, and closure 14 days
earlier. move **both** ends of the predictor window together so the window length is preserved. The
label window is frozen and identical in every variant. One exact common cohort (the intersection of
analysis-eligible, primary-population, valid rows of every variant, after removing shared
pre-label-censored cells) and one shared spatial-fold assignment are used by all six evaluations
(two model families × three variants), with model family, feature registry, preprocessing,
hyper-parameters and seeds held fixed. Uncertainty is a paired spatial-block bootstrap on the model
stage's own replicate draws with identical block draws across variants (1,000 replicates, seed 42,
resampling unit `spatial_block_id`). The report states the analysis measures the closure date
jointly with its interaction with the fixed MODIS seasonal production policy, not the closure date
in isolation. Bejís, for scale: 12,814 cohort rows, 967 positives, 5 folds, 3,641 blocks. The shared
folds are blocked at the pipeline's default 2-cell edge (≈ 1 km): the analysis assigns block
identifiers with `add_spatial_block_id(cohort, spatial_block_size_cells)` and takes that value from
`STEP8B_SPATIAL_BLOCK_SIZE_CELLS = 2` (`repo/src/window_closure_sensitivity.py:8562`,
`repo/core/config.py:556`). The comparison report records fold and block counts but not the block
size, so this was read from the source rather than the report.

### 3.16.4 Same-geography event-to-event comparison (Muğla 2021 versus 2022)

Muğla is the one region for which a second fire event is analysed on the **identical** AOI and
analysis grid (`region_key = mugla_aoi`, the same bounding box and the same ~510 m cell definition),
which allows the direction of feature-label associations to be compared with geography held fixed.
The 2022 experiment is registered as `mugla_2022_event_relative` with windows anchored to its own
event: a 58-day predictor window (2022-04-24 → 2022-06-20) closing the day before ignition and a
49-day label window (2022-06-21 → 2022-08-08) opening on it, durations chosen to match the 2021
windows exactly (58 and 49 days).

**This is not a clean temporal-transfer design and is not presented as one.** The registry records
the reason explicitly: the 2022 event ignites roughly five weeks earlier in the season than the 2021
event, so calendar year and seasonal phase are confounded and no difference can be attributed to the
year alone. The registered claim is `same_geography_event_to_event`, and that is the claim made
here. The entry is deliberately kept out of the canonical five-AOI cohort by its
`temporal_transfer_wildfire` role so that a second year of an already-represented AOI cannot be
silently enrolled into the spatial comparisons. That exclusion is not merely a convention we
observe: it is enforced in code and tested. The ERA5-Land diagnostic's validator
(`scripts/validate_era5_land_regional_diagnostic.py`) carries two relevant checks, and they have
different reach. `A08_cohort_is_the_frozen_five` requires the executed cohort to equal the frozen
`DEFAULT_EXPERIMENTS` tuple exactly, as an ordered comparison, so *any* addition fails it, including
this experiment. `A07_mugla_2022_absent_from_default_analysis` is narrower than its name suggests:
it tests literal membership of the string `mugla_2022`, which is the registry's superseded
calendar-shift record, and would not by itself catch the `mugla_2022_event_relative` entry analysed
here. Both checks pass on the executed output (Section 3.17), but the guarantee for this experiment
rests on A08. The decision to keep this pair out of the 20-direction transfer matrix is therefore
verifiable in the released code rather than resting on the text of this paper. The same leakage-safe
pre-label exclusion applies as in every other region: cells that burned inside this experiment's own
predictor window are removed from the analysis universe rather than counted as unburned.

Two frozen diagnostics are read for this pair, both produced by the machinery already described and
neither refitting any model. Burned-pattern structure (component counts, effective component count,
component-size and elevation distributions, land-cover mix) follows Section 3.14.5, computed on the
primary population; outputs in `paper/mugla_temporal_raw/` with hashes in that directory's
`SHA256SUMS.txt`. Signed univariate direction reversal follows Section 3.12: for each of the nine
numeric features, the raw ROC-AUC of the feature against `burned` in each experiment, never folded
to max(AUC, 1 − AUC), so that a value below 0.5 is read as a direction rather than as weakness. Land
cover is excluded from the AUC analysis because its integer class codes carry no meaningful scalar
order, and is reported descriptively instead. Uncertainty is a spatial-block bootstrap on 10-cell (≈
5 km) blocks assigned before filtering, 1,000 replicates, seed 42, 2.5/97.5 percentile intervals. A
reversal counts as bootstrap-supported only when both experiments' intervals exclude 0.5 on opposite
sides. Outputs in `paper/step9g_raw/` with hashes alongside. Four pair directories in that export
carry a `_superseded_pre_manavgat_repair` suffix and are superseded. They are retained for the
record and are not read here.

Unlike every other transfer direction in this paper, the two arms of this pair were not present in
the frozen export delivered to us, which contained no `mugla_2021__mugla_2022_event_relative`
directory, so they were computed for this analysis. They were produced by running the project's own
unmodified `src/step9b_run_cross_region_transfer.py` and
`src/step9c_cross_region_block_bootstrap.py` at commit `48b56e7`. That is the same code and the same
protocol as Section 3.10 and Section 3.9, with `random_state = 42`, the primary RF configuration,
and the 1,000-replicate spatial-block bootstrap on `spatial_block_id`. The frozen Step 8A modelling
datasets of both experiments were the only inputs, hashed as read
(`paper/mugla_transfer_raw/SHA256SUMS.txt`). Because `repo/` is treated as read-only and the
pipeline resolves its paths from its own location, the run used a shadow project root containing a
copy of `core/`, `src/` and `scripts/` plus those two inputs, so nothing was written into the
pipeline repository or into the frozen output archive. The environment was Python 3.12.3 with
scikit-learn 1.9.0, pandas 3.0.5 and NumPy 2.5.2, matching the version to which every other transfer
number in this paper is fixed (Section 4.7e). One consequence is stated rather than hidden: the
metrics file records `git_commit: null`, because the shadow root is not itself a git repository.

**Independent execution of this pair.** These two directions were subsequently found to have been
run by the pipeline author as well, in a separate environment and before our own run, and that
export was supplied to us. The pair therefore rests on two independent executions rather than on one
performed by the authors of this manuscript. The two runs are separated in date, machine, code-tree
state and library stack. The pipeline author's run was produced on 2026-08-09 at commit `a07ea33`
under scikit-learn 1.9.0 with pandas 3.0.2 and NumPy 2.4.4, and ours on 2026-08-11 at commit
`48b56e7` under Python 3.12.3, scikit-learn 1.9.0, pandas 3.0.5 and NumPy 2.5.2. Both read the same
two frozen Step 8A parquets, identical by SHA-256 (`c4ab107d…` for 2021 and `7c545f4d…` for the 2022
event-relative experiment), and both used `random_state = 42`.

Agreement is to floating-point noise rather than to a stated tolerance. Across both directions and
both model families the transfer ROC-AUC and PR-AUC point estimates agree to **≤1×10⁻⁷**. The
2021→2022 direction is bit-identical in every reported metric, and the largest discrepancy anywhere
in the pair is 9.9×10⁻⁸. The 1,000-replicate spatial-block bootstrap reproduces to the same order,
with the ΔAUC interval bounds agreeing to ≤3.4×10⁻⁸. The agreement also holds below the metric
level: the two runs' per-cell prediction tables have identical row counts and columns, and across
all 295,402 predicted probabilities the largest absolute difference is 4.4×10⁻¹⁶, which is
double-precision round-off. The prediction files themselves therefore differ in SHA-256, because
last-place decimal digits change the serialised string length. The human-readable step9b and step9c
summary files of the two runs are byte-identical. The pipeline author's copy of these outputs is
archived alongside ours in `paper/mugla_transfer_raw/emrehan_run_20260809/` with hashes and
provenance in that directory's `SHA256SUMS.txt`. The interval-supported effects reported in Section
4.8 are in any case an order of magnitude larger than the ±0.02 to 0.03 cross-version tolerance of
Section 4.7e, so the conclusions do not rest on the exact point estimates.

## 3.17 Regional meteorological context (explanatory)

To characterise the meteorological conditions each region actually experienced, and specifically to
test the post hoc explanation that Manavgat's outlying transfer behaviour reflects meteorological
extremity (Section 5.7), an AOI-level ERA5-Land diagnostic was run outside the modelling pipeline
(`src/era5_land_regional_diagnostic.py`, with runner and validator in `scripts/`; outputs in
`drive_new/diagnostics/era5_land_regional/<analysis_id>/`). It is explanatory only: it produces a
table and exports no raster, and its outputs enter no feature set, no model and no transfer arm. The
module records this status in its own output (`is_model_predictor: false`). The candidate diagnostic
set of Section 3.14 was fixed before any diagnostic-versus-transfer correlation was computed, and no
meteorological measure is added to it; the reasoning is given in Section 5.7.

Hourly `temperature_2m`, `dewpoint_temperature_2m`, `u_component_of_wind_10m`,
`v_component_of_wind_10m` and `total_precipitation_hourly` are read from the ERA5-Land hourly
reanalysis [@MunozSabater2021] as the Earth Engine collection `ECMWF/ERA5_LAND/HOURLY`. Four
variables are derived per pixel and per hour, never from window means. They are temperature (K →
°C), relative humidity as 100·e_s(T_d)/e_s(T) using the ECMWF/Tetens saturation formula over water
for both terms (T₀ = 273.16 K, a₁ = 611.21 Pa, a₃ = 17.502, a₄ = 32.19 K), left unclipped and only
checked for finiteness; wind speed as √(u10² + v10²); and precipitation depth from the hourly
accumulation band (m → mm), the cumulative `total_precipitation` band never being used, so no
differencing of a running total is involved.

Each hourly field is reduced to one AOI value by an explicit pixel-area weighting, Σ(value ×
pixelArea) / Σ(pixelArea), with the denominator masked by that variable's own mask so that a
variable undefined over part of the AOI is not credited with that area. Both sums are evaluated on
ERA5-Land's native projection and transform with `bestEffort=False`. An unweighted mean is not used.
Window statistics are then computed over the resulting series of hourly regional means. These are
the window mean and maximum for temperature, humidity and wind, and additionally the window total
for precipitation. A reported maximum is therefore the most extreme regional hour, never the most
extreme individual pixel.

The observed windows are each region's own predictor and label windows taken from the experiment
registry (Section 3.1). No date is hard-coded in the diagnostic, and the registry's inclusive end
date is converted exactly once to Earth Engine's exclusive bound. Each statistic is referenced to a
climatology built by mapping the same calendar month-day window into the four reference years 2017
to 2020, computing each year's statistic independently, and taking their arithmetic mean and sample
standard deviation (ddof = 1). The standardised anomaly is (observed − climatological mean) /
climatological SD, written as null, and never as zero or infinity, when the climatological SD is
exactly zero. Every window, observed and climatological alike, must contain the exact contiguous
hourly UTC sequence (n_days_inclusive × 24 hours). A missing, duplicated, out-of-order, shifted or
extra hour fails the run rather than being sorted, interpolated, padded or dropped. The cohort is
the five canonical regions in a fixed order, Muğla 2022 being deliberately excluded, and the
scientific configuration is hashed into the output namespace identifier so that a changed cohort or
contract resolves to a different namespace rather than silently overwriting an existing result.

**Standardised anomalies are computed by the diagnostic but are not reported in this paper.** Two
properties of the climatology make them unsuitable for the comparative use a reader would put them
to. First, it spans only four years, so each standard deviation carries three degrees of freedom and
is correspondingly unstable. Second, and decisively, the resulting standard deviations are strongly
heterogeneous *between* regions: over the five predictor windows the climatological SD spans 0.41 to
1.13 °C for temperature, 1.09 to 6.58 % for relative humidity, 0.039 to 0.146 m s⁻¹ for wind speed
and 12.6 to 48.0 mm for precipitation total. The ratios are 2.7× to 6.0×, rising to 7.8× and 11.5×
for temperature and precipitation in the label windows. A standardised anomaly therefore denotes a
different physical departure in each region, and the cross-region comparison it invites is not
meaningful. Anomalies are reported in physical units throughout (Section 4.9). The instability is
not hypothetical: Bejís's label-window temperature and Muğla's predictor-window wind speed exceed
five standardised units on climatological SDs of 0.147 °C and 0.065 m s⁻¹, from physical anomalies
of only +0.83 °C and +0.34 m s⁻¹.

Correctness of the output was verified rather than assumed. The four files were obtained from the
pipeline author, and their SHA-256 hashes match those recorded in the accompanying manifest
(`paper/era5_raw/SHA256SUMS.txt`). The analysis identifier agrees across the manifest, the contract
and the containing namespace. The companion validator
(`scripts/validate_era5_land_regional_diagnostic.py`) was then **executed against this output in
`--mode actual`, and all 27 contract checks passed with none failed and none skipped**. Among them,
the climatological mean and sample SD reproduce from the four retained yearly realisations (A20);
observed windows and every climatological realisation are hourly complete (A25, A26). The
standardised anomaly is null exactly when the climatological SD is zero (A16). The CSV and JSON
summaries agree value by value (A17). The summary contains no infinite or missing quantity and no
`Infinity`/`NaN` literal (A18, A19). The manifest hashes and byte sizes match (A21). The cohort is
the frozen five with Muğla 2022 absent (A07, A08). The reference years and `sd_ddof = 1` are as
declared (A09, A10). The registry region keys and window dates agree with `core/regions.py` (A14);
and the namespace contains only the four expected files, no exported raster having leaked into it
(A24). The run was performed by the authors on 2026-08-11 under Python 3.12.3 with `earthengine-api`
1.7.39 installed solely to satisfy the module import chain. The validator opens no Earth Engine
session and requires no credentials. The repository was at commit `48b56e7` and the outputs staged
in a scratch namespace outside the repository via `--output-root`.

The manifest names commit `a07ea33`, at which neither the diagnostic source nor the Montiferru
registry entry yet exists. Both were first committed in `48b56e7`. The production run was therefore
made from a working tree carrying uncommitted changes, and the recorded commit identifies only the
last commit at run time. The code that actually ran can nevertheless be identified. The output
contains Montiferru with its registry windows, which `a07ea33` cannot supply. In that commit
`core/regions.py` gains that entry only in `48b56e7`, and it does so by pure addition (529 lines
inserted, none deleted), leaving the four regions common to both commits byte-identical.
`core/paths.py` and `core/config.py`, the diagnostic's only other internal dependencies, are
unchanged between the two commits. Every free-text semantics string hashed into the scientific
contract matches `48b56e7` verbatim, and the validator's registry check (A14) confirms that all five
regions' keys and window dates in the output agree with `48b56e7`'s registry. The working tree that
produced this output therefore carried the registry and diagnostic content of `48b56e7`, which is
the version described here and the version pinned as a submodule of the manuscript repository.

<!-- METHODS ROUND NOTES:

(a) Gap -> subsection mapping (gaps as numbered in 04_results.md DRAFT NOTES (b)):
    1  (Table 1: five regions, extended Evia, Montiferru)      -> §3.1 (Table 1 + caption + Evia
       note + Table 1b sentence updated; rest of §3.1 untouched)
    2  (diagnostic-vs-transfer rank-correlation framework)     -> §3.14.1
    3  (conditional sign-agreement / cosine indices)           -> §3.14.4
    4  (domain-classifier audit)                               -> §3.14.2
    5  (niche-overlap measures)                                -> §3.14.3
    6  (fire-regime structure metrics)                         -> §3.14.5
    7  (LORO pooled-training protocol)                         -> §3.15.1
    8  (feature-drop configurations and parity checks)         -> §3.15.2
    9  (legacy-vs-extended Evia AOI sensitivity)               -> §3.16.1
    10 (tree+shrub population variant, Montiferru)             -> §3.16.2
    11 (window-closure sensitivity design)                     -> §3.16.3
    Additionally: Table R6 paired baseline-vs-thermal transfer contrast -> single sentence at end
    of §3.10 (uses frozen step9b points + step9c delta_roc_auc; protocol already covered by
    §3.9-3.10); scikit-learn version tolerance -> single sentence in §3.13 Reproducibility.

(b) [TO VERIFY] markers in this file after this round:
    CLOSED 2026-08-11  §3.1  registry entries/line numbers — repo/ pulled (at 48b56e7, which
               contains all five regions) and core.regions IMPORTED and queried via
               get_experiment() rather than parsed. Every Table 1 bbox, window, baseline-year set
               and role matches. Caption line numbers corrected; the previous "lines 59, 142, 173"
               were wrong, not merely stale (they point at Muğla, Montiferru and a Kozan comment).
    CLOSED 2026-08-11  §3.16.3 block edge length — resolved from source, not from the report:
               the shared folds use add_spatial_block_id(..., spatial_block_size_cells) with
               STEP8B_SPATIAL_BLOCK_SIZE_CELLS = 2 (~1 km), at
               src/window_closure_sensitivity.py:8562 and core/config.py:556.
    CLOSED 2026-08-13  §3.13 reproduction tolerances for the FINAL five-region set. The pipeline
               author produced reproduction_check.json on 2026-08-11 (commit 48b56e7); it is
               archived at paper/reproduction_check/reproduction_check_5region.json, sha256
               7f7e41f5210ee32de7585bb89f8121fa2d127ee98e3aa03ef4351c608909c8be, and was read
               from source rather than from the covering mail. Achieved: within-region max
               |dROC-AUC| = 0 exactly (20/20 comparisons); CORAL max |dROC-AUC| = 1.6164523e-7
               (20/20 directions, 80 comparisons, 69 bit-identical, missing_directions empty).
               Judged against the repo own pre-existing 1e-6 Step10C fail-fast criterion, applied
               unchanged -- stated in the text, since it forecloses the "tolerance chosen to fit"
               objection. Cohort resolution (3 agreeing routes) and the duplicate Step10
               namespaces for Bejis-Mugla / Manavgat-Mugla also written into §3.13. The historical
               two-region figures (<=1e-4 within-region, +-0.002 CORAL) are superseded and gone.
               THIS FILE NOW HAS NO OPEN [TO VERIFY].
    CLOSED 2026-08-13  §3.16.4 -- not a marker, but the same round: the pipeline author supplied
               his own 2026-08-09 run (commit a07ea33) of the Mugla 2021<->2022 arms. Same input
               hashes, different pandas/numpy, agreement <=1e-7 and byte-identical summary .md.
               The paragraph claiming these two directions were authors-produced was replaced by
               an independent-execution paragraph. Archive:
               paper/mugla_transfer_raw/emrehan_run_20260809/.
    VERIFIED 2026-08-13  Repo-source checks of claims that were previously self-referential
               (read from repo/ at 48b56e7, not from the JSON/config that asserts them):
               - Tolerance: RAW_/WITHIN_REGION_REPRODUCTION_TOLERANCE = 1e-6 at
                 src/step10c_paired_evaluation_bootstrap.py:59-60, enforced by a raise at :373.
                 git log -S shows both introduced in commit bccc258 on 2026-07-13, four weeks
                 BEFORE the 2026-08-11 reproduction check, and never modified since. The
                 "pre-existing, not chosen for this report" claim in §3.13 is now source-backed.
               - Cohort route 1: core/regions.py has 9 entries; canonical = no superseded_by
                 (drops evia_2021 and mugla_2022), minus roles negative_control /
                 temporal_transfer_wildfire -> exactly the five. §3.13 amended to name the
                 supersession filter, which was doing real work and was not described.
               - CORRECTED §3.16.4: A07_mugla_2022_absent_from_default_analysis tests literal
                 membership of the string "mugla_2022" (the SUPERSEDED calendar-shift record) at
                 scripts/validate_era5_land_regional_diagnostic.py:317-321. It would NOT catch
                 mugla_2022_event_relative, which is the entry §3.16.4 is about. The real
                 guarantee is A08_cohort_is_the_frozen_five (exact ordered tuple equality with
                 DEFAULT_EXPERIMENTS). The paragraph overclaimed A07 and now states both.
               - S1 few-shot protocol claims verified in src/few_shot_recovery.py: tier
                 constants :125-127, blake2b seed derivation :324, sort-then-shuffle :719-720,
                 FORBIDDEN_UNCERTAINTY_TERMS :196.

    CLOSED 2026-08-08 (second round):
    §3.1  Kozan -- DECIDED IN. It now appears as a negative control in three places: a pointer in
          §3.1, a dedicated "Negative control" paragraph in §3.3 (why the gate needs a region that
          fails it; MCD64A1 does not separate stubble burning from wildfire; the gate sees Kozan
          blind), and the result in §4.1. It enters no modelling, transfer or diagnostic analysis.
    §3.3  gate verdicts -- resolved by pointing §3.3 to §4.1, where Table R1 carries the
          per-region verdicts and fractions read from each burned_landcover_gate.json. Kozan:
          542 burned cells, 0.017 natural vegetation, 0.983 cropland, verdict
          cropland_dominated_control (drive_new/kozan-legacy/step6/labels/burned_landcover_gate.json).
    §3.13 repository URL / DOI -- resolved as a "Data and code availability" statement naming
          https://github.com/emrehann17/satellite-thermal-digital-twin (public, MIT). NO DOI and
          no Zenodo deposit, by decision; the statement says so explicitly and asks readers to
          cite the URL plus commit id.
    §3.4  DEM source -- verified, not assumed. step2b_dem.py prefers GLO-30 and falls back to
          SRTMGL1 on exception, so the code alone does not settle it; the frozen
          step2b_dem_metadata.json records used_fallback=false, so GLO-30 ran and SRTM did not.
          Cited by ESA product-page URL + access date (the DataCite DOI 404s). Farr et al. 2007
          deliberately NOT cited.

(c) Candidate discrepancy points vs Emrehan's independent Methods narrative (places where our
    scripts made choices his implementation may not share):
    - PRNG: correlation-framework bootstrap uses mulberry32 in Node.js (deterministic, NOT
      NumPy-identical); LORO/feature-drop bootstraps use NumPy default_rng(42). CI bounds may
      differ in the 3rd decimal from a NumPy reimplementation of the pair bootstrap.
    - Pair-bootstrap design: unordered pairs resampled, both directions carried, 2000 replicates,
      per-measure seed offsets (regime 42+0.., conditional 42+100.., niche 42+200..); an
      independent implementation may resample ordered directions or use different offsets.
    - Niche overlap: 50 shared 1-D bins / 20x20 PC bins over GLOBAL (five-region pooled burned)
      ranges; PCA on pooled standardised burned cells (ddof=0), NaN -> pooled median; Mahalanobis
      pooled covariance uses np.cov default (ddof=1 per-region, then pooled). Different bin
      counts, per-pair ranges, or covariance conventions change all values.
    - Burned-cell counts for niche/regime/signed-AUC analyses are TSG AND valid_for_modeling
      (784/1100/2911/2664/539), not step8a's raw burned-in-TSG counts (784/1100/2952/2675/582);
      Table R1 uses the latter (04_results DRAFT NOTES conflict 4).
    - Regime metrics: 8-connectivity (not 4); effective count = inverse Simpson. Verified equal
      to Emrehan's Rejim table, so only the description, not the numbers, can diverge.
    - Supported-reversal criterion: both regions' CIs exclude 0.5 with opposite point signs
      (Emrehan's step9g reversal_status criterion; STRICTER than the "disjoint CIs" wording used
      for the two-region diagnostic in §3.12 — the two criteria coincide for the reported
      features but are not logically identical).
    - LORO preprocessing: manual indicator expansion of sorted training categories (equivalent
      to OneHotEncoder(handle_unknown='ignore') but independently implemented); region-wise z
      includes the target region scaled by its own stats; block ids built as string
      "row//10_col//10" at a fixed origin.
    - Feature-drop within-region folds: StratifiedGroupKFold with n_splits fallback 5->4->3->2
      if any test fold lacks positives (step8b itself forbids falling back to random rows; the
      fallback ladder is ours). In practice 5 splits were used (n_splits_used recorded).
    - Window-closure: §3.16.3 describes ONLY the bejis_2022 comparison report; other regions'
      reports assumed structurally identical (same schema window_closure_compare.v1). The
      report's §8 contains a boilerplate sentence referring to a "Manavgat-2021-style common
      cohort" inside the Bejís report; not quoted.
    - scikit-learn: all our reruns pinned to 1.9.0; 1.7.2 shifts transfer AUCs by +0.02..0.03
      (sklearn_version_sensitivity.md). If Emrehan reports numbers from another version, point
      estimates may differ by that order.
-->

