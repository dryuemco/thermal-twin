# 3. Materials and methods

> **Drafting note.** Every constant, threshold, window and formula below was read from the
> executed pipeline source rather than reconstructed from memory; the governing source file is
> named in each subsection so that the manuscript text and the released code can be checked against
> each other. Quantities that could not be confirmed against an actual output file in the working
> copy at drafting time are marked `[TO VERIFY]`.

## 3.1 Study regions and temporal windows

Four Mediterranean-basin wildfire regions are analysed. Each is defined as a place-based rectangular
area of interest (AOI) in EPSG:4326, fixed **before** any burned-area label was inspected; the AOIs
are deliberately *not* clipped to fire perimeters, so that unburned cells surrounding each fire
constitute the negative class rather than being excluded by construction.

For each region the analysis is organised around two non-overlapping time windows. The **predictor
window** is the pre-fire period from which every dynamic predictor is composited; it ends the day
before the label window opens. The **label window** is the period in which a burned-area detection
counts as a positive label. Because the predictor window closes before the first day of the label
window, no predictor observation can post-date the fire it is used to predict. A separate set of
**baseline years** supplies the multi-year climatological reference against which thermal anomalies
are computed; these use the same calendar window as the predictor window, transported to earlier
years, with the fire year itself excluded.

**Table 1. Study regions.** Region registry, AOI geometry and windows read from
`repo/core/regions.py` (AOI constants at lines 59, 67, 142, 173; experiment registry at lines
232–344).

| Region | Country | AOI bounding box (W, S, E, N) | Predictor (pre-fire) window | Label window | Baseline years | Role |
|---|---|---|---|---|---|---|
| Manavgat / Antalya 2021 | Türkiye | 31.05, 36.72, 31.85, 37.35 | 2021-06-01 → 2021-07-27 | 2021-07-28 → 2021-08-31 | 2017–2020 | anchor wildfire |
| Bejís / Castellón 2022 | Spain | −1.05, 39.68, −0.35, 40.15 | 2022-06-15 → 2022-08-14 | 2022-08-15 → 2022-09-30 | 2018–2021 | Mediterranean transfer wildfire |
| Muğla 2021 | Türkiye | 27.10, 36.60, 28.90, 37.45 | 2021-06-01 → 2021-07-28 | 2021-07-29 → 2021-09-15 | 2017–2020 | same-country, same-year transfer wildfire |
| North Evia (Euboea) 2021 | Greece | 23.12, 38.68, 23.52, 39.08 | 2021-06-05 → 2021-08-02 | 2021-08-03 → 2021-09-30 | 2017–2020 | Mediterranean transfer wildfire `[TO VERIFY: inclusion — processing incomplete at drafting time]` |

Sample sizes, burned-cell counts and prevalences per region are reported in Table 1b `[TO VERIFY:
Manavgat and Bejís counts are available from the frozen Step8A outputs; Muğla and North Evia counts
must be taken from the completed runs and re-verified before submission]`.

The region set is constructed to separate two candidate explanations of transfer failure. Manavgat
and Muğla are in the same country, in the same fire year, roughly 200 km apart, and share a
baseline-year set; Bejís is in a different country, a different year, and about 2500 km away. If
transferability were governed by geographic and climatic proximity, the Manavgat↔Muğla pair should
transfer best. A **negative control** region (Kozan 2023, Türkiye), in which the burned area is
dominated by agricultural stubble burning rather than wildfire, exists in the pipeline registry and
is used only as a validity check on the admissibility gate described in Section 3.3; it is never
used as a transfer partner. `[TO VERIFY: final decision on whether Kozan appears in the manuscript.]`

## 3.2 Burned-area label and the ~500 m analysis grid

The target variable is burned/unburned status derived from the MODIS MCD64A1 Collection 6 burned-area
product, retrieved through Google Earth Engine. Active-fire detections (FIRMS) are never used as a
target.

**Grid reconstruction.** MCD64A1 is a ~500 m product on the MODIS sinusoidal grid, but it is
exported from Earth Engine onto the 30 m EPSG:4326 reference grid used by the rest of the pipeline
(`VALIDATION_LABEL_EXPORT_SCALE = 30`, `core/config.py:262`), which duplicates each native ~500 m
observation across a block of 30 m pixels sharing its value. The analysis grid is therefore
*reconstructed* rather than native: the 30 m reference grid is partitioned into non-overlapping
square blocks of `round(500 / 30) = 17 × 17` pixels
(`step8a_prepare_500m_modeling_dataset.py:914–917`, using
`STEP8A_MCD64A1_NATIVE_CELL_SIZE_M = 500.0` and `STEP8A_REFERENCE_PIXEL_SIZE_M = 30.0`,
`core/config.py:538–539`), giving a nominal cell edge of 510 m. This is an approximation of the true
MODIS sinusoidal cell: it is anchored to the Landsat/EPSG:4326 reference grid rather than to the
MODIS tile grid, and blocks at the AOI margin are truncated and therefore contain fewer than 289
constituent pixels. This is stated explicitly because it is a real, and reported, limitation of the
label geometry rather than an incidental implementation detail. Each cell is identified by its
integer block indices `row_500m = row_offset // 17`, `col_500m = col_offset // 17`
(`step8a:920–936`); these indices are used to construct spatial cross-validation blocks and are
never used as predictors.

The 30 m reference grid itself is the Landsat current-period median LST raster produced upstream,
and every other continuous predictor is required to match it exactly in width, height, CRS and
affine transform; a mismatch is a hard error and the pipeline never silently resamples
(`step8a:613–643`). The two exceptions are documented and use nearest-neighbour resampling only,
because both layers are categorical: land cover (`step8a:479–551`) and the MCD64A1 burn-date raster
itself (`step8a:768–814`).

**Label assignment.** Within each 17×17 block, only strictly positive burn-date day-of-year values
are considered; zeros and no-data are ignored. A cell is unburned by default. If positive values
exist, their modal day-of-year is taken as the cell's representative burn date, ties being broken
in favour of the smaller value — which, for the burned/unburned decision, means the conservative
direction (`step8a:939–951`). The representative day-of-year is then converted to a calendar date
and tested against the region's label window: if it falls inside the window the cell is labelled
burned, otherwise the cell is retained as **unburned** and flagged `out_of_window_burndate`
(`step8a:1204–1248`). The fraction of positive sub-pixels agreeing with the modal date is recorded
as a diagnostic (`burn_date_pixel_agreement_fraction`) but no agreement threshold is imposed; a
single in-window positive sub-pixel is sufficient to label the cell burned.

The label never affects a cell's eligibility for modelling (Section 3.5). Unburned cells,
all-no-data blocks and out-of-window cells all remain in the dataset as the negative class.

**Pre-label burn exclusion.** Optionally, cells that already show a burn detection in the interval
between the start of the predictor window and the start of the label window are excluded from the
analysis universe entirely, so that a predictor window cannot be contaminated by an earlier fire
within the same season (`step8a:2592–2605`, using the exclusion manifest produced by the gate step).
Excluded cells are marked `analysis_eligible = False`; their raw labels are preserved for audit but
they never enter modelling.

## 3.3 Burned-landcover admissibility gate

Before any predictor modelling, each region passes through a gate
(`step6b_burned_landcover_gate.py`) that answers one question: **of the cells labelled burned, what
land cover dominates them?** The gate reads only the burn-date raster and the aligned land-cover
raster, and reuses Step8A's block size, cell-identity function and land-cover class map verbatim, so
its cells are identical to the modelling cells.

For each burned cell the modal ESA WorldCover class is taken. Regional fractions are then formed
with the total burned-cell count as denominator: a natural-vegetation fraction (tree cover 10 +
shrubland 20 + grassland 30) and a cropland fraction (class 40). The verdict rule is applied in
order (`step6b:172–211`):

1. fewer than `STEP6_BURNED_LANDCOVER_GATE_MIN_POSITIVES = 30` burned cells → *insufficient burned
   positives*;
2. natural-vegetation fraction ≥ 0.50 → **wildfire candidate — pass**;
3. cropland fraction ≥ 0.50 → *cropland-dominated control*;
4. otherwise → *mixed or uncertain*.

Thresholds are at `core/config.py:369–373`. The gate is diagnostic: a failing verdict does not halt
the pipeline, and the gate output always carries `downstream_authorized: False`, requiring explicit
review. Its role in this study is to establish that the regions entering the transfer experiment are
genuine forest-fire regions and that the negative control is not. `[TO VERIFY: gate verdicts and
natural-vegetation fractions for all four regions, from each region's `burned_landcover_gate.json`.]`

## 3.4 Predictor variables

All dynamic predictors are composited over the region's predictor window; static predictors are
time-invariant. Each is produced by a named upstream pipeline stage and delivered on the 30 m
reference grid.

**Optical greenness (NDVI).** Landsat Collection 2 Level-2 surface reflectance, scaled by
0.0000275 with an offset of −0.2, is used to compute NDVI = (NIR − Red)/(NIR + Red); pixels with a
near-zero denominator or values outside [−1, 1] are masked (`core/config.py:89–103`). The
predictor-window composite is a per-pixel **median**.

**Land surface temperature (Landsat).** The Landsat Level-2 surface temperature band is scaled by
0.00341802 with an offset of 149.0 K and converted to degrees Celsius. The predictor-window
composite is again a per-pixel median (`current_lst`, in °C); this raster also serves as the 30 m
reference grid.

**LST anomaly.** A z-score of the current-window LST median against the baseline-years
distribution for the same calendar window: `(current_median − baseline_mean) / baseline_std`
(`step5_preprocess_timeseries.py:837–847`). The anomaly is set to no-data where the baseline
standard deviation is below `STEP5_MIN_BASELINE_STD_CELSIUS = 1.0` °C, where fewer than
`STEP5_MIN_CURRENT_VALID_COUNT = 2` current observations exist, or where fewer than
`STEP5_MIN_BASELINE_VALID_COUNT = 3` baseline observations exist. The result is dimensionless.

**TVDI and TVDI difference.** The Temperature–Vegetation Dryness Index is computed in the LST–NDVI
feature space (`step5c_tvdi.py`): the NDVI range [0, 1] is divided into
`TVDI_NDVI_BIN_COUNT = 20` bins; within each bin with at least `TVDI_MIN_PIXELS_PER_BIN = 30`
valid pixels, the wet and dry edges are taken as the 2nd and 98th LST percentiles
(`TVDI_WET_EDGE_PERCENTILE = 2.0`, `TVDI_DRY_EDGE_PERCENTILE = 98.0`); TVDI is then
`(LST − wet_edge) / (dry_edge − wet_edge)`, clamped to [0, 1], and set to no-data where the edge
span is below `MIN_TVDI_EDGE_SPAN_C = 1.0` °C (`core/config.py:162–178`). `tvdi_difference` is the
current-window TVDI minus the baseline-years mean TVDI. A documented caveat applies to the latter:
the baseline TVDI is formed from a single baseline LST mean raster combined with per-year NDVI, so
its inter-annual variation derives from NDVI alone (`step5c_tvdi.py:480–486`).

**Downscaled and fused LST.** To mitigate Landsat's sparse thermal revisit, a MODIS→Landsat
downscaling model is trained on the predictor window and applied to the full 30 m grid
(`step7c`, `step7d`), yielding `downscaled_lst` in °C, clipped to configured physical bounds. The
downscaling stage is explicitly leakage-guarded: it never sees MCD64A1 or FIRMS labels, and is
prevented from ingesting the anomaly, TVDI or TVDI-difference layers as inputs
(`step7d_predict_downscaled_lst.py:1–30`). A fused product (`fused_lst`, °C) then combines observed
Landsat LST with downscaled LST as **gap-fill only** — valid observed pixels are never replaced or
blended (`step7e_fuse_landsat_downscaled_lst.py:1–26`). A companion source mask records, per pixel,
whether the fused value is observed, gap-filled or invalid; the corresponding per-cell fractions are
retained as sensitivity diagnostics and are **never** used as predictors.

**Terrain.** Elevation (m a.s.l.) and slope (degrees, from `ee.Terrain.slope`) are derived from the
Copernicus GLO-30 DEM, with SRTMGL1 as a configured fallback (`core/config.py:61–80`), exported at
30 m.

**Land cover.** ESA WorldCover v200 (10 m native, 2021 epoch), nearest-neighbour aligned to the 30 m
reference grid. Class codes: 10 tree cover, 20 shrubland, 30 grassland, 40 cropland, 50 built-up,
60 bare/sparse vegetation, 70 snow/ice, 80 permanent water, 90 herbaceous wetland, 95 mangroves,
100 moss/lichen.

## 3.5 Cell-level aggregation, validity mask and analysis population

**Aggregation.** For each continuous predictor and each 17×17 block, the mean, median, standard
deviation, valid-pixel count and valid-pixel fraction of the finite 30 m values are computed
(`step8a:954–963`). Modelling uses the block **mean** of each predictor. For land cover, the modal
class (`landcover_dominant`) and per-class area fractions are computed over valid land-cover pixels
within the block.

**Validity.** A cell is `valid_for_modeling` if and only if all of the following hold
(`step8a:1399–1422`): it is analysis-eligible (not excluded as a pre-label burn); at least
`STEP8A_MIN_30M_VALID_FRACTION = 0.3` of its 30 m pixels have simultaneously finite NDVI, elevation
and slope; its aggregated NDVI, elevation and slope means are each finite; and it contains at least
one valid land-cover pixel. Thermal predictors deliberately do **not** enter the validity test, so
that thermal data availability cannot silently reshape the population differently for the two
feature sets. The label likewise plays no part in the validity test — a design point made explicit
in the source, since requiring a valid burn date would collapse the dataset to burned-like cells.

**Analysis population.** The **primary** population is natural vegetation: cells that are
`valid_for_modeling` and satisfy `burnable_tree_shrub_grass`, defined as a combined tree +
shrubland + grassland **area fraction ≥ `STEP8A_BURNABLE_FRACTION_THRESHOLD` = 0.50** within the
cell (`step8a:1326–1329`). Cropland is explicitly excluded from every burnable mask and only ever
reported as its own fraction. Restricting to natural vegetation removes the confound in which
agricultural stubble burning and bare-surface thermal contrast could be mistaken for wildfire skill;
it is the scientifically defensible population for the transfer question, and — as the analysis
shows — the choice materially changes the conclusion. The mixed population of all valid cells
(`all_valid`) is retained throughout as a **secondary sensitivity** analysis, and both populations
are reported for every headline quantity.

Two definitional asymmetries are noted for transparency: the burnable mask is an **area-fraction**
test, whereas the admissibility gate of Section 3.3 uses the **modal** class; and the upstream
within-region pipeline's own configured primary population is `all_valid`
(`STEP8B_PRIMARY_POPULATION`, `core/config.py:559`), whereas the transfer analysis reported here
takes natural vegetation as primary. All comparisons in this paper — within-region reference,
naive transfer and adapted transfer alike — are computed on the *same* population and the *same*
classifier configuration, which is what makes the decomposition of Section 3.12 valid.

`burnable_tree_shrub_grass` is used exclusively as a population mask and is never a feature.

## 3.6 Feature sets

Two nested feature sets are compared (`step8b_train_baseline_vs_thermal_model.py:121–135`):

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
adaptation experiments (`step8b:420–429`):

```
RandomForestClassifier(n_estimators=300, max_depth=None, min_samples_leaf=3,
                       class_weight="balanced", random_state=42, n_jobs=-1)
```

with scikit-learn defaults otherwise (`criterion="gini"`, `max_features="sqrt"`,
`min_samples_split=2`, bootstrap resampling of training rows). `class_weight="balanced"` compensates
for the strong class imbalance (burned prevalence of a few per cent). The configuration is chosen
once and never tuned against any evaluation the paper reports; a second, unweighted profile with
`min_samples_leaf=2` is retained solely as a sensitivity check.

Preprocessing is a scikit-learn `Pipeline` fitted **inside** each training fold (or, for transfer,
on the source region only), so that no imputation or encoding statistic is derived from evaluation
data (`step8b:449–467`): numeric predictors are median-imputed; `landcover_dominant` is
mode-imputed and one-hot encoded with `handle_unknown="ignore"`, so that a land-cover class present
in the evaluation set but absent from the training set produces an all-zero indicator row rather
than an error. This is what makes the one-hot column space consistent between regions in the
transfer experiments: it is fixed by the source region. No feature scaling is applied in the
within-region models, as the classifier is scale-invariant.

## 3.8 Spatial-block cross-validation and block-size robustness

Within-region evaluation uses **spatially blocked** cross-validation. Contiguous square blocks of
`B × B` analysis cells are formed at a fixed origin from the grid indices,
`block_row = row_500m // B`, `block_col = col_500m // B` (`step8b:277–306`), and the resulting block
identifier is used as the grouping variable in `StratifiedGroupKFold` with `n_splits = 5`,
`shuffle=True` and `random_state = 42` (`step8b:309–414`; `core/config.py:554–556`). Blocks are
therefore never split between training and test folds, and class stratification is preserved across
folds. Fold construction is guarded: at least two test folds must contain a positive, and the
pipeline is explicitly forbidden from ever falling back to a random row-wise split.

Both feature sets are fitted on the **same folds**, so the baseline-versus-thermal comparison is
paired by construction. Out-of-fold predicted probabilities are assembled into a single vector per
feature set, covering every cell exactly once, and metrics are computed once on the concatenated
out-of-fold vector rather than averaged over folds (`step8b:519–690`).

**Block size and robustness.** The pipeline's default block size is
`STEP8B_SPATIAL_BLOCK_SIZE_CELLS = 2`, i.e. 2 × 2 cells ≈ 1 km. Because the appropriate blocking
scale is not knowable a priori and short-range spatial autocorrelation can survive fine blocking,
the whole within-region analysis is repeated at **B = 2, 10 and 20 cells (≈ 1, 5 and 10 km)**, on
both populations. A thermal increment that persists as blocks coarsen is evidence of genuine spatial
generalisation rather than of neighbour leakage; the trade-off is that coarser blocking also reduces
the number of independent groups available for cross-validation and for bootstrap resampling, which
widens the intervals.

**Metrics.** Threshold-free discrimination is reported as ROC-AUC and PR-AUC (average precision);
the Brier score is computed as a calibration diagnostic. Threshold-dependent quantities (balanced
accuracy, precision, recall, F1) are recorded at a fixed 0.5 cut-off within regions but are not used
for the paper's claims (`step8b:480–503`). The primary quantity of interest is the paired difference
ΔAUC = AUC(thermal) − AUC(baseline) on the same out-of-fold predictions.

## 3.9 Spatial-block bootstrap uncertainty

Uncertainty is quantified by a **spatial-block bootstrap** operating on stored predictions, with no
refitting (`step8c_spatial_block_bootstrap_uncertainty.py`). The resampling unit is the spatial
block, not the cell: in each replicate, `n_blocks` blocks are drawn with replacement from the
`n_blocks` unique blocks, and a block drawn *k* times contributes all of its cells *k* times
(`step8c:278–351`). Resampling cells individually would treat spatially autocorrelated neighbours as
independent and produce intervals that are far too narrow — an error we made and corrected during
this study (Section 3.12).

The number of replicates is 1000 and the seed is 42 (`core/config.py:574–575`). Intervals are
**equal-tailed percentile** intervals at the 2.5th and 97.5th percentiles; no bias correction or
acceleration (BCa) is applied. Replicates in which a resample contains only one class are recorded
and excluded from the percentiles rather than silently redrawn; a warning is raised if more than
10% of replicates are invalid.

The bootstrap is **paired**: within each replicate, both the baseline and thermal probability
vectors are evaluated on the identical resampled index and the difference is formed inside the
replicate, so the interval is on the distribution of the paired ΔAUC. The same paired construction
is used in the transfer experiments, where a single set of resampled target blocks per replicate is
shared by all probability series (within-region reference, raw transfer, z-scored transfer, CORAL
transfer) so that they remain directly comparable.

Following the pipeline's own reporting policy, no classical p-values or significance tests are
reported. A result is described as having **positive bootstrap support** when the 95% percentile
interval for ΔAUC excludes zero, and as **uncertain** otherwise; this is a statement about an
interval, not a hypothesis test.

Block sizes used for the bootstrap match the analysis they accompany: B = 2 for the transfer scores,
B matched to the cross-validation blocking (2, 10, 20) for the within-region robustness analysis,
and B = 10 (≈ 5 km) for the univariate concept-shift diagnostic of Section 3.12.

## 3.10 Cross-region transfer protocol

For each ordered pair of regions (source → target), a model is fitted on the **entire** source
region — all cells in the analysis population, no held-out fold — and applied to the entire target
region. All ordered pairs among the completed regions are evaluated in both directions.

Every fitted component is derived from the source region only: the numeric imputation medians, the
categorical mode, the one-hot category vocabulary, and the random forest itself. The target region
enters the computation exactly once, at `predict_proba`. There is no pooled fitting, no
target-derived imputation, no target fine-tuning, no calibration on the target, and no coordinate or
region-identity feature (`step9b_run_cross_region_transfer.py:230–236, 370–381`). The classifier,
hyperparameters, seed and feature contract are imported from the within-region stage rather than
redefined, so the transfer model is the same model.

Feature harmonisation across regions requires no separate alignment step: the shared feature list is
frozen and validated by an audit stage that fails on any schema mismatch, and the source-fitted
one-hot encoder with `handle_unknown="ignore"` guarantees identical column ordering and dimension at
target-prediction time. Land-cover classes present in the target but not the source encode to zero.

Both source and target must contain at least 30 positive and 30 negative cells in the population
being evaluated, otherwise the pair is skipped.

**Target metrics** are threshold-free: ROC-AUC and PR-AUC, with spatial-block bootstrap intervals as
in Section 3.9, computed on the target region's blocks. A ROC-AUC below 0.5 is reported as such and
is interpreted as an anti-predictive transfer — the source-learned ordering is systematically
inverted in the target — rather than being folded to `max(AUC, 1 − AUC)`.

## 3.11 Label-blind domain adaptation

Three transfer variants are compared. All are strictly **label-blind**: the target frame is
structurally stripped of the response before adaptation, and an assertion fails the run if a label
column is present (`step10b_label_blind_adaptation.py:71–79`; `core/step10_shared.py:243–250`). No
adaptation function accepts labels as an argument.

**(a) Raw.** The source-fitted model applied directly to untransformed target features
(Section 3.10).

**(b) Region-wise z-score.** Each region's numeric features are standardised using **its own**
statistics: `z = (x − μ_region) / σ_region`, with the mean and standard deviation computed over
non-missing values only and `ddof = 0` (`step10_shared.py:145–173`). A near-constant feature
(σ < 10⁻¹²) has its divisor set to 1 and the substitution is recorded. Missing values are filled
with the region's own mean, hence map to exactly zero after transformation. The categorical
land-cover predictor is left untouched. Source statistics come from source data and target
statistics from target data; the two regions are never pooled. The classifier is then refitted on
the z-scored source and applied to the z-scored target. This variant removes first- and second-order
marginal offsets between regions — the simplest possible self-calibration.

**(c) CORAL after region-wise z-score.** Starting from the z-scored features of (b), the source
covariance is aligned to the target covariance by the standard CORAL whitening–recolouring map
(`step10_shared.py:186–220`):

```
C_s = cov(X_s^z) + λI ,   C_t = cov(X_t^z) + λI
A   = C_s^(−1/2) · C_t^(1/2)
X_s* = X_s^z · A
```

with covariances computed at `ddof = 0` and matrix powers obtained by symmetric eigendecomposition
with eigenvalues floored at 10⁻¹². The regularisation is `STEP10_CORAL_LAMBDA = 1e-5`
(`core/config.py:697`). Critically, **the transform is applied to the source only**; the target
remains exactly as in (b). The classifier is refitted on the aligned source and applied to the
unchanged z-scored target.

**On the choice of λ.** The canonical CORAL formulation adds the identity (λ = 1) to each
covariance, but it is defined for unstandardised features. Here CORAL is applied *after* region-wise
standardisation, so each feature already has unit variance and adding the full identity doubles the
diagonal, imposing shrinkage strong enough to erase the covariance structure the alignment is meant
to exploit. With only nine numeric features and thousands of cells per region, the covariances are
well estimated and minimal regularisation is appropriate. Because this is a defensible but not
inevitable choice, λ is swept over {10⁻⁵, 10⁻³, 10⁻¹, 1} and the sensitivity of every
CORAL-dependent conclusion is reported explicitly rather than left implicit.

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
and same block size**, which is what makes them commensurable; a decomposition assembled from
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
violation raises rather than warns (`step8b:140–159, 265–271, 450`). It contains the response
itself and every column carrying label information — `burn_date`, `burn_month`,
`burn_day_of_year`, `label_source`, `burn_date_pixel_agreement_fraction`, `out_of_window_burndate`
— together with `lon`, `lat`, `cell_id`, `row_500m`, `col_500m`, the validity columns, and the
fused-LST provenance columns (`source_mask_majority`, `observed_fraction`, `gapfilled_fraction`,
`invalid_source_fraction`). The transfer stage additionally forbids `experiment_id`, `region_key`,
`spatial_block_id` and `fold_id`.

Coordinates are excluded because a fire scar is a spatially compact object: with longitude and
latitude available, a sufficiently flexible model can memorise the scar's location instead of
learning any relationship with the surface state. Grid indices are used only to construct
cross-validation blocks and bootstrap groups. The natural-vegetation mask is used only to define the
population. The fused-LST provenance fractions are retained for a sensitivity analysis — performance
restricted to cells with a low gap-filled fraction — but never as predictors.

**Sensitivity analyses.** Every headline result is repeated across: two analysis populations
(natural vegetation, primary; all valid cells, secondary); two random-forest profiles (the primary
weighted `min_samples_leaf = 3` configuration and an unweighted `min_samples_leaf = 2` profile);
three spatial-block sizes for the within-region analysis (≈ 1, 5, 10 km); four CORAL regularisation
values; and both feature sets. Where a conclusion depends on one of these choices, the dependence is
reported rather than resolved by selecting the favourable setting.

**Reproducibility.** All randomness uses seed 42 — model `random_state`, cross-validation shuffling
and bootstrap generators alike — and the bootstrap uses 1000 replicates throughout. The transfer and
adaptation analysis is executed in a dedicated Python environment separate from the upstream
pipeline environment; because random-forest fits are not bit-identical across scikit-learn versions,
the analysis includes an explicit reproduction check in which the within-region models are refitted
in the new environment and compared against the frozen upstream outputs, and the independently
implemented adaptation is compared against the pipeline's own implementation. `[TO VERIFY: quote the
achieved reproduction tolerances for the final region set from `reproduction_check.json`; the
two-region check agreed to ≤1×10⁻⁴ for within-region AUCs and to ±0.002 for CORAL transfer scores,
but this must be re-established once all regions are included.]` No file belonging to the upstream
pipeline or to previously frozen outputs was modified by this analysis.

Code, configuration and frozen numeric outputs are released with the paper `[TO VERIFY: repository
URL and archival DOI]`.
