# 3. Materials and methods

> **Drafting note.** Every constant, threshold, window and formula below was read from the
> executed pipeline source rather than reconstructed from memory; the governing source file is
> named in each subsection so that the manuscript text and the released code can be checked against
> each other. Quantities that could not be confirmed against an actual output file in the working
> copy at drafting time are marked `[TO VERIFY]`.

## 3.1 Study regions and temporal windows

Five Mediterranean-basin wildfire regions are analysed. Each is defined as a place-based rectangular
area of interest (AOI) in EPSG:4326. Each AOI is defined from place coverage rather than from a fire
perimeter, and none is tuned on burned prevalence, on the gate outcome or on any model metric. One
AOI choice was label-informed and is stated as such: the North Evia box was extended after the
legacy box was found to carry an atypically high burned prevalence, the extended geometry was then
defined from place anchors, and the legacy variant is retained as a sensitivity (Section 4.1). The AOIs are deliberately *not* clipped to fire perimeters, so that unburned cells surrounding
each fire constitute the negative class rather than being excluded by construction.

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
retained **only** as a sensitivity variant (Section 4.7a).

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

The target variable is burned/unburned status derived from the MODIS MCD64A1 Collection 6.1
burned-area product (`MODIS/061/MCD64A1`), retrieved through Google Earth Engine [@Gorelick2017]. Collection 6.1 is
a reprocessing of the Collection 6 product described by Giglio et al. [@Giglio2018] and validated by
Boschetti et al. [@Boschetti2019]. Active-fire detections (FIRMS) are never used as a target.

**Grid reconstruction.** MCD64A1 is a ~500 m product on the MODIS sinusoidal grid, but it is
exported from Earth Engine onto the 30 m EPSG:4326 reference grid used by the rest of the pipeline
(`VALIDATION_LABEL_EXPORT_SCALE = 30`, `core/config.py:262`), which duplicates each native ~500 m
observation across a block of 30 m pixels sharing its value. The analysis grid is therefore
*reconstructed* rather than native: the 30 m reference grid is partitioned into non-overlapping
square blocks of `round(500 / 30) = 17 × 17` pixels (`step8a_prepare_500m_modeling_dataset.py:914 to
917`, using `STEP8A_MCD64A1_NATIVE_CELL_SIZE_M = 500.0` and `STEP8A_REFERENCE_PIXEL_SIZE_M = 30.0`,
`core/config.py:538 to 539`), giving a nominal cell edge of 510 m.

**That cell is square in degrees but not on the ground, and this is stated here because the paper's
central robustness argument is about spatial scale.** Every predictor raster is exported at
`scale: 30` in `EPSG:4326` (each region's `predictor_export_metadata.json`), so the reference pixel
is a step in degrees, 30 / 111,319.49 = 0.00026949°, and the analysis cell is 17 times that,
0.0045814°, in both axes. On the ground the cell is about 510 m north to south everywhere, but only
407 m east to west at Manavgat and Muğla, 397 m at Evia, 391 m at Bejís and 390 m at Montiferru.
Cell area is 0.199 to 0.208 km² against the MODIS cell's 0.250 km², so the analysis cell is about
17 % to 20 % smaller. The derivation is checkable rather than nominal: dividing each AOI's span by
0.0045814° and rounding outward reproduces every frozen cell count exactly, at 175 × 138 = 24,150
for Manavgat, 153 × 103 = 15,759 for Bejís, 393 × 186 = 73,098 for Muğla, 175 × 131 = 22,925 for
Evia and 66 × 49 = 3,234 for Montiferru. Two consequences follow. Every block-size label in this
paper is the north-south dimension: a 10-cell block is about 5.1 km by 3.9 to 4.1 km and a 20-cell
block about 10.2 km by 7.8 to 8.1 km, so spatial blocking is systematically weaker in longitude than
the labels suggest. And because the cell is smaller than a MODIS cell and not aligned with it, a
typical cell draws on more than one MODIS cell, which dilates the labelled burned footprint relative
to MCD64A1 and is the quantitative form of the label-geometry concern in Section 5.11(xiv).

The reconstruction is an approximation of the true MODIS sinusoidal cell in two further respects: it
is anchored to the Landsat/EPSG:4326 reference grid rather than to the MODIS tile grid, and blocks
at the AOI margin are truncated and therefore contain fewer than 289 constituent pixels. This is stated explicitly because it is a real, and reported, limitation of the
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
otherwise the cell is retained as **unburned** and flagged `out_of_window_burndate` (`step8a:1217 to
1261`). The fraction of positive sub-pixels agreeing with the modal date is recorded as a diagnostic
(`burn_date_pixel_agreement_fraction`) but no agreement threshold is imposed. Only the modal date is
tested, so the rule is not an "any positive sub-pixel" rule in general: a block whose positive
sub-pixels were, say, one in-window and two out-of-window would be labelled unburned. In this
dataset the two rules coincide, because the exported label raster carries no out-of-window positives
at all. Every region's `label_raster_diagnostics` records `count_positive` equal to
`count_in_label_doy_range` exactly. So for this export, and only because of that clipping, a single
in-window positive sub-pixel is sufficient to label the cell burned.

The label never affects a cell's eligibility for modelling (Section 3.5). Unburned cells,
all-no-data blocks and out-of-window cells all remain in the dataset as the negative class.

**Pre-label burn exclusion.** Optionally, cells that already show a burn detection in the interval
between the start of the predictor window and the start of the label window are excluded from the
analysis universe entirely, so that a predictor window cannot be contaminated by an earlier fire
within the same season (`step8a:967 to 1025` reads the exclusion manifest produced by the gate step,
`step8a:3059 to 3072` resolves it for the run, and `step8a:1179 to 1188` applies it per cell). Excluded cells are marked `analysis_eligible = False`; their raw labels are preserved for
audit but they never enter modelling.

This safeguard is optional in the pipeline and it did not run everywhere, which the reader needs in
order to weigh it. From the frozen dataset statistics, it ran for Muğla (49 cells excluded), Evia
(16) and Montiferru (61). For Manavgat the flag is recorded as false and no cell was excluded. For
Bejís the field is absent from the export altogether, so no status is recorded either way. The
exposure this leaves is bounded by how many cells carry an MCD64A1 detection inside the predictor
window in those two regions, and that count has not been produced; it is listed as an open item in
Section 5.11. Two further limits belong here. The exported label raster is clipped to the label
window in every region, so a pre-label detection is not recoverable from the label raster itself and
the reported count of zero out-of-window burn dates is a property of the export rather than an
empirical finding. Burning in earlier years is not screened for any region in the five-region
cohort, so a cell that burned in a previous year enters the analysis with a baseline climatology
computed partly over its own post-fire state. The historical-exclusion module is opted into exactly
once in the registry, for the `mugla_2022_event_relative` experiment of Section 3.16.4, where it
removes the 2021 scar. Muğla 2021 is the source of that mask rather than a beneficiary of it, and
the 2022 event-relative experiment is not one of the five regions of Table 1.

## 3.3 Burned-landcover admissibility gate

Before any predictor modelling, each region passes through a gate
(`step6b_burned_landcover_gate.py`) that answers one question: **of the cells labelled burned, what
land cover dominates them?** The gate reads only the burn-date raster and the aligned land-cover
raster, and reuses Step8A's block size, cell-identity function and land-cover class map verbatim, so
its cells are identical to the modelling cells.

For each burned cell the modal ESA WorldCover class is taken. Regional fractions are then formed
with the total burned-cell count as denominator: a natural-vegetation fraction (tree cover 10 +
shrubland 20 + grassland 30) and a cropland fraction (class 40). The verdict rule is applied in
order (`step6b:198 to 219`):

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

**Observations behind the composites.** The optical and thermal predictors come from one sensor and
one collection: Landsat 8 Collection 2 Level-2 (`LANDSAT/LC08/C02/T1_L2`). Landsat 9 is not used in
any region, including Bejís 2022, where it was operational. Quality screening is applied per pixel
from the `QA_PIXEL` band, masking fill, dilated cloud, cirrus, cloud, cloud shadow and snow, with
medium and high confidence bits treated as masked; the water bit is deliberately preserved
(`step3_landsat_lst.py:67 to 98`). The `ST_QA` per-pixel surface-temperature uncertainty band is
available in this collection and is not used, so no per-pixel LST uncertainty enters the analysis.
The coarse-resolution thermal input is `MODIS/061/MOD11A1`, the Terra daytime 1 km LST product;
Aqua is not used.

A predictor-window composite therefore rests on however many clear acquisitions that window
contained, and the pipeline's floor is low: `STEP5_MIN_CURRENT_VALID_COUNT = 2`, so a cell's median
may rest on two clear observations. The number is region-specific and, within a region, position-
specific. For Manavgat, the only region with a frozen acquisition inventory, the 57-day window holds
seven distinct dates from 14 scenes on two alternating WRS-2 paths, so a cell inside the path
overlap is backed by seven dates and a cell outside it by three or four. Section 4.7i shows what
this variation does to the within-region increment, and Section 5.11 lists the per-region inventory
as an open item, since it exists for Manavgat alone.

**Optical greenness (NDVI).** Landsat Collection 2 Level-2 surface reflectance, scaled by 0.0000275
with an offset of −0.2, is used to compute NDVI = (NIR − Red)/(NIR + Red); pixels with a near-zero
denominator or values outside [−1, 1] are masked (`core/config.py:89 to 103`). The predictor-window
composite is a per-pixel **median**.

**Land surface temperature (Landsat).** The Landsat Level-2 surface temperature band is scaled by
0.00341802 with an offset of 149.0 K (`core/config.py:86 to 87`) and converted to degrees Celsius. The predictor-window
composite is again a per-pixel median (`current_lst`, in °C). This raster also serves as the 30 m
reference grid.

**LST anomaly.** A z-score of the current-window LST median against the baseline-years distribution
for the same calendar window: `(current_median − baseline_mean) / baseline_std`
(`step5_preprocess_timeseries.py:899 to 905`). The anomaly is set to no-data where the baseline
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

A second property of TVDI matters for the transfer analysis and is stated here so that Section 5.2
can be read against it. The wet and dry edges are percentiles of the LST values that a given scene
contains, so they are fitted per AOI and per window. A TVDI of 0.5 therefore denotes a different
physical moisture state in each region, set by whatever dryness range that AOI happened to span on
those dates, and the AOIs differ widely in size and relief (Montiferru 0.30° × 0.22° against Muğla
1.80° × 0.85°). TVDI is normalised in a statistical sense, not in a physical one. A common-edge
version of the index, fitted once across the pooled land pixels of all five regions so that a TVDI
of 0.5 denotes the same dryness everywhere, was computed for this paper and is reported in Section
4.7k. It does not remove the reversal, so scene-fitted edges are a controlled-for factor here rather
than an open competing explanation.

**Sea water enters the edge fit, and the extent of the resulting problem was measured rather than
assumed.** Because the water bit is preserved and the AOIs are not clipped to the coastline, sea
pixels take part in the percentile fit. Two of the five AOIs are largely marine: water-dominant
cells are 57.6 % of Evia's grid and 38.9 % of Muğla's, against 0.1 % for the one inland AOI, Bejís.
The frozen per-bin edge diagnostics show the consequence directly. In Evia the three lowest NDVI
bins carry dry edges of 28.8 to 29.9 °C, which is Aegean sea-surface temperature and not a land dry
edge, whereas Bejís's lowest bins sit near 49 °C. That contamination is confined to the bins the sea
occupies. From NDVI bin 4 upward Evia's dry edge runs from 44 to 47.5 °C, in the same range as
Bejís's 41 to 49 °C, and neither the wet nor the dry edge orders across the five regions by sea
fraction: in the vegetated bins the lowest wet edge belongs to Montiferru, at 7.4 % water, and the
highest to Bejís, at 0.1 %.

The question that matters is whether the modelled population occupies the contaminated bins, and it
does not. Not one cell of the primary natural-vegetation population in any region has a mean NDVI
below 0.15, and 0.01 % or less lies below 0.20; the 5th percentile of that population's NDVI is
0.376 in Evia and 0.290 to 0.383 elsewhere. Nor is there evidence of the saturation such a
mis-normalisation would produce: the share of primary-population cells at the upper clamp is 0.5 %
in Evia, 0.5 % in Muğla and 0.4 % in Manavgat, against 0.1 % in Bejís, with the distribution well
spread in every region. That check is made on 500 m cell means, so it bounds rather than excludes the
effect on individual 30 m pixels, and it does not license the all-valid population, where sea cells
are present in bulk (Section 4.7f).

**The clean test was then run.** The edges were refitted on land pixels alone, and a third set was
fitted once over the pooled land pixels of all five regions, which is the common-edge index promised
below. Both re-runs import the pipeline's own binning, percentile and clamp functions, so the only
difference between arms is which pixels enter the percentile. The all-pixel arm reproduces every
frozen edge to floating-point noise with exactly equal bin pixel counts, and its cell-aggregated
index reproduces the frozen `current_tvdi_mean` column to 1.8×10⁻⁷, which is float32 storage
precision. Section 4.7k reports the outcome: sea in the edge fit does move the index, by an amount
that scales with each AOI's sea fraction, and it does not change any region's direction.

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

Three properties of this step are reported here because a reader cannot otherwise judge what the two
derived channels are. First, the downscaling model is validated, on spatially blocked 64 × 64
train/validation/test splits, each against a MODIS-baseline control. Test RMSE is 2.04 °C (R² 0.866)
for Manavgat, 1.75 °C (0.795) for Bejís, 1.65 °C (0.956) for Muğla, 1.80 °C (0.866) for Evia and
1.83 °C (0.909) for Montiferru. Second, the downscaler's own inputs include `lon`, `lat`, `row`,
`col` and their normalised forms. Their summed importance is 0.123 (Manavgat), 0.122 (Bejís), 0.097
(Evia), 0.066 (Montiferru) and 0.035 (Muğla), so `downscaled_lst`, and `fused_lst` on its gap-filled
share, carry a smooth coordinate-derived component. The downscaler never sees a fire label, so this
is not label leakage, but Section 3.13 excludes coordinates from the fire model and this is the one
route by which a coordinate-derived surface re-enters it. The dominant input also differs by region:
the MODIS context layer in Manavgat (0.525) and Evia (0.593), NDVI in Bejís (0.482) and Montiferru
(0.666), and slope in Muğla (0.777), where the channel is largely a re-expression of a baseline
predictor. Third, **the MODIS input is screened to two different standards across the cohort.** All
five regions use single-season predictor-window MODIS summary layers, each matched to its own
window, as recorded in every region's `data/modis/modis_metadata.json`. What differs is quality
control. Evia and Montiferru apply a `QC_Day` bit rule and require at least three valid daily
observations per pixel, and they write an explicit nodata sentinel of −9999. Manavgat, Bejís and
Muğla apply no quality mask and declare no nodata value, so cells with nothing to report are
encoded as exact 0.0 °C. The screening was added to the export script on 2026-07-23, after the
first three regions had already been exported, so the cohort is split by export date rather than by
design.

The zero-fill was measured for this paper rather than inferred, and it is not distributed as the
nodata signature alone would suggest. Counting exact zeros in each region's MODIS mean layer gives
518 of 6,390 pixels for Manavgat (8.11 %), **7,347 of 19,190 for Muğla (38.29 %)** and **none at all
for Bejís**. Both non-zero fractions are above the pipeline's own 5 % suspicious-zero guard
(`STEP7B_MODIS_SUSPICIOUS_ZERO_FRACTION`), and Muğla's is more than four times Manavgat's. The two
regions that apply the QC rule contain no exact zeros, because they carry an explicit −9999
sentinel instead. What the zeros are is also settled by the counts: 8.11 % against a water-dominant
cell share of 8.3 % in Manavgat, and 38.29 % against 38.9 % in Muğla, while inland Bejís has 0.1 %
water and no zeros. The zero-fill is therefore the sea rather than missing observation, and it is
absent from the one AOI with no coastline. This matters because
`downscaled_lst` and `fused_lst` rest on these layers, and Section 4.7h reports how much of the
thermal increment those two channels carry. Section 5.11 records it as an untested candidate
explanation.

A note on provenance, because the frozen export contradicts itself here. Manavgat's Step 7C and 7D
metadata describe the same raster as a four-year summer-mean context layer. That string is a stale
literal: at the pinned commit it is emitted only for the Kozan negative control, and the conditional
that restricts it was committed on 2026-07-10, one day after Manavgat's Step 7C ran. Manavgat is the
only region carrying it, and the region's own `modis_metadata.json`, written by the exporting run
three hours earlier, states the single-season predictor window and says in as many words that the
layer is not a multi-year baseline. The `modis_metadata.json` record is the one taken as
authoritative here.

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

**Land cover.** ESA WorldCover v200 [@Zanaga2022] (10 m native, 2021 epoch), nearest-neighbour aligned to the 30 m
reference grid. The 2021 epoch is applied unchanged to every region, including Bejís 2022, so for
that region the land-cover layer precedes the fire year by one growing season. Class codes: 10 tree cover, 20 shrubland, 30 grassland, 40 cropland, 50 built-up, 60
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
4. it contains at least one valid land-cover pixel.

Thermal predictors deliberately do **not** enter the validity test, so that thermal data
availability cannot silently reshape the population differently for the two feature sets. The label
likewise plays no part in the validity test. That is a design point made explicit in the source,
since requiring a valid burn date would collapse the dataset to burned-like cells.

**Analysis population.** The **primary** population is natural vegetation: cells that are
`valid_for_modeling` and satisfy `burnable_tree_shrub_grass`, defined as a combined tree + shrubland
+ grassland **area fraction ≥ `STEP8A_BURNABLE_FRACTION_THRESHOLD` = 0.50** within the cell
(`step8a:1339 to 1342`). Cropland is explicitly excluded from every burnable mask and only ever
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

**Table 2. Feature dictionary.** Every modelled predictor, its source product, the pipeline stage
that produces it, its unit, whether it is composited over the predictor window or time-invariant,
and its feature-set membership. Cell-level values are means over the ~510 m cell, except
`landcover_dominant`, which is the modal class. Specifications are in Section 3.4.

| Predictor | Source product | Stage | Unit | Temporal | Baseline | Thermal |
|---|---|---|---|---|---|---|
| `ndvi_mean` | Landsat C2 L2 surface reflectance | step4 | dimensionless | window median | yes | yes |
| `elevation_mean` | Copernicus DEM GLO-30 | step2b | m a.s.l. | static | yes | yes |
| `slope_mean` | Copernicus DEM GLO-30 | step2b | degrees | static | yes | yes |
| `landcover_dominant` | ESA WorldCover v200 (2021 epoch) | step2c | class code | static | yes | yes |
| `current_lst_mean` | Landsat C2 L2 surface temperature | step3 | °C | window median | no | yes |
| `lst_anomaly_mean` | Landsat C2 L2, against baseline years | step5 | z-score | window vs climatology | no | yes |
| `current_tvdi_mean` | Landsat C2 L2 LST and NDVI | step5c | dimensionless, [0, 1] | window | no | yes |
| `tvdi_difference_mean` | Landsat C2 L2, against baseline years | step5c | dimensionless | window vs climatology | no | yes |
| `downscaled_lst_mean` | MOD11A1 downscaled on Landsat predictors | step7c, step7d | °C | window | no | yes |
| `fused_lst_mean` | Landsat LST, gap-filled from downscaled | step7e | °C | window | no | yes |

Three properties of this table matter for the interpretation and are established elsewhere in this
paper. The four baseline predictors are static apart from `ndvi_mean`, which is a predictor-window
median composite. The six thermal predictors are not six independent measurements: `fused_lst_mean`
equals `current_lst_mean` outside a gap-filled share of 0.11 % to 9.70 %, and `downscaled_lst_mean`
is a fitted surface whose dominant input differs by region (Section 4.7h). Those same two channels
carry a smooth coordinate-derived component inherited from the downscaler's inputs, which is the one
route by which coordinates re-enter a feature set that otherwise excludes them (Section 3.4, Section
3.13).

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
C_s = cov(X_s^z) + lambda*I ,   C_t = cov(X_t^z) + lambda*I
A    = C_s^(-1/2) * C_t^(1/2)
X_s* = X_s^z * A
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
inevitable choice, λ sensitivity was assessed, and the exact scope of that assessment is stated
here. Nine λ values were run: 0, 10⁻⁸, 10⁻⁷, 10⁻⁶, 10⁻⁵, 10⁻⁴, 10⁻³, 10⁻² and 10⁻¹. They were run
on four transfer directions, Bejís↔Muğla 2021 and Manavgat↔Muğla 2021, in both the baseline and the
thermal family. The frozen configuration records this grid and records λ = 10⁻⁵ as the
implementation's canonical value
(`drive_new/diagnostics/coral_lambda_sensitivity/b74d643e…/lambda_grid.csv` and `config.json`). The
Manavgat↔Bejís directions were not re-run over the grid, and the configuration marks them
`contextual_only_not_rerun`. The resulting spread in transfer AUC is at most 0.014 within any
direction, and at most 0.008 within the thermal family; the three widest spreads are all
baseline-family rows (Section 4.7d).

**Why the released sweep stops short of λ = 1.** The canonical value is the one value that sweep does
not contain, and the omission is deliberate rather than accidental. In the canonical formulation the identity is added to
the covariance of unstandardised features, where it acts as a mild ridge relative to feature scale.
Here every feature has already been given unit variance by the region-wise z-score of variant (b).
Adding the full identity therefore doubles each diagonal entry and halves the relative weight of
every off-diagonal term. The alignment map is pushed towards the identity and the covariance
structure that CORAL exists to transport is largely erased. A λ = 1 arm would mostly measure how the
pipeline behaves when CORAL is effectively switched off. It would not measure how sensitive the
reported result is to reasonable regularisation, which is what the sweep is for.

**The λ = 1 arm was subsequently computed for this paper, and the argument above turns out to
overstate the case.** The released sweep tool cannot be extended: its λ grid is a fixed token
sequence and the module asserts its own fit count at import, so the arm was produced instead by
driving the pipeline's own primitives (`fit_coral_alignment`, `apply_coral`, the region-wise
z-score, and Step 8B's pipeline builder) in the order `step10b` calls them. λ = 10⁻¹ was recomputed
alongside as a control and reproduces the frozen sweep to 4.4×10⁻⁹ over all eight rows, seven of
them exactly. At λ = 1 no direction changes side of the chance line, and the largest movement is an
*improvement*, Muğla→Manavgat thermal from 0.559 to 0.574. Heavy regularisation therefore does not
switch CORAL off in this region set, as the scale argument predicted it would. Including λ = 1
widens the spread over the grid to at most 0.019 in any direction and 0.016 within the thermal
family, against 0.014 and 0.008 over the released grid. Section 4.7d reports this.

An earlier two-region version of this study, using Manavgat and Bejís alone, ran λ at 10⁻⁵, 10⁻³,
10⁻¹ and 1, and there the one direction whose interval sat above chance lost that status at λ = 1.
That analysis is superseded throughout by the five-region analysis, its region set is different, and
the four directions of the sweep do not include Bejís↔Manavgat, so the two results are not in direct
contradiction. Nothing further is drawn from it. The sweep also does not cover the Montiferru and Evia directions, so
conclusions for those directions rest on the default λ = 10⁻⁵ alone.

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
`label_source`, `burn_date_pixel_agreement_fraction` and `out_of_window_burndate`. It also contains
`lon`, `lat`, `cell_id`, `row_500m`, `col_500m`, the validity columns, and the fused-LST provenance
columns (`source_mask_majority`, `observed_fraction`, `gapfilled_fraction`,
`invalid_source_fraction`). The transfer stage additionally forbids `experiment_id`, `region_key`,
`spatial_block_id` and `fold_id`.

Coordinates are excluded because a fire scar is a spatially compact object: with longitude and
latitude available, a sufficiently flexible model can memorise the scar's location instead of
learning any relationship with the surface state. Grid indices are used only to construct
cross-validation blocks and bootstrap groups. The natural-vegetation mask is used only to define the
population. The fused-LST provenance fractions are retained as diagnostics, never as predictors.
They are reported per region in Section 4.7h, where the gap-filled share is 0.11 % to 9.70 % of the
fused product. A performance sensitivity restricted to cells with a low gap-filled fraction **was
run** for this paper and is reported in Section 4.7m. It matters most for Bejís, whose 9.70 % is an
order of magnitude above the other four regions, and Bejís is indeed where it moves the increment
most, from +0.056 to +0.043, while the increment keeps bootstrap support in all five regions.

**Sensitivity analyses.** Every headline result is repeated across: two analysis populations
(natural vegetation, primary; all valid cells, secondary); three spatial-block sizes for the
within-region analysis (≈ 1, 5, 10 km); nine CORAL regularisation values from 0 to 10⁻¹ on the four
directions covered by the sweep (Section 3.11); both feature sets. Where a conclusion depends on
one of these choices, the dependence is reported rather than resolved by selecting the favourable
setting. Two axes named in earlier drafts are not part of this set and should not be read as
covered. The unweighted `min_samples_leaf = 2` random-forest profile was defined as a secondary
configuration but no result from it is reported in Section 4 or Section 5, and the CORAL sweep does
not include λ = 1 in the five-region export.

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

That check was run by the pipeline author, and the script behind it is not in the released
repository, so a reader cannot re-execute it (Section 5.11 states this). We therefore repeated part
of it independently, using only code a reader does have. The environment was rebuilt from scratch on
a different operating system, Windows 11 rather than Linux, pinning the three libraries that govern
the fits to the versions the check records (NumPy 2.4.4, pandas 3.0.2, scikit-learn 1.9.0) on Python
3.12.10, and `src/step8b_train_baseline_vs_thermal_model.py` was executed unmodified at commit
`48b56e7` against the frozen Step 8A parquet of two regions. Every numeric field of the resulting
`step8b_model_comparison_metrics.json` was compared against the archived one: 142 fields for Manavgat
with a maximum absolute difference of 6.9×10⁻¹⁸, in a Brier score, and 168 fields for Montiferru with
a maximum absolute difference of **exactly 0**. No field differed by more than 10⁻⁹, and every
reported ROC-AUC agreed to sixteen significant digits, including the Table 3 values for Manavgat
(baseline 0.8027358197042693, thermal 0.8696419777927898). The within-region results of this paper
are therefore reproducible from the released code and the archived data alone, on different hardware
and a different operating system, once the library versions are fixed. This does not extend to the
transfer arm, whose reproduction-check script remains unavailable.

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
records (those carrying no `superseded_by` key, which drops the legacy Evia AOI
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
Earth Engine. They are MODIS MCD64A1 Collection 6.1 burned area, MODIS land surface temperature,
Landsat Collection 2 Level-2 surface reflectance and surface temperature, Copernicus DEM GLO-30, and
ESA WorldCover v200. No data were collected by the authors and no restricted or licensed data were
used. The region definitions, date windows and thresholds given in this section are sufficient to
regenerate every input from these sources.

The full processing pipeline (Steps 1 to 10), its configuration constants, and the frozen numeric
outputs on which every reported number rests are publicly available at
`https://github.com/emrehann17/satellite-thermal-digital-twin`. The repository is the authoritative
source for the file and line references cited throughout this section. Analysis code is released
under the repository's stated licence (MIT).

Three limits on that release are stated here rather than left for a reader to discover. First, **no
digital object identifier is minted and no archival deposit exists**, and the repository carries no
tags, so "the version of record" is a commit identifier on a moving branch head rather than a
citable snapshot. Readers should cite the repository URL together with commit `48b56e7`, which is
the state against which every file and line reference in this section was checked. Second, **the
code that produced the reproduction check of this section is not in the released tree at that
commit.** The check's own record marks `scripts/run_reproduction_check.py` and
`src/reproduction_validation/` as untracked, and neither is present at `48b56e7`. The check's output
artefact is archived with this paper and its 100 recorded values were independently verified against
the 20 frozen artefacts they reference, but a reader cannot regenerate it from the repository.
Third, **the commit recorded for the few-shot export (`19d825b`) is not reachable** in the published
history, although the module it names, `src/few_shot_recovery.py`, is present at `48b56e7` and
predates the run. A fourth, smaller discrepancy belongs to the companion paper: the ERA5-Land
diagnostic's manifest names a commit at which the diagnostic source does not yet exist, so that
production run was made from an uncommitted working tree.

None of these affects a number in this paper, each was verified rather than assumed, and every
affected artefact is archived in frozen form. They do bound the sense in which this negative result
is independently re-checkable, and the paper claims no more than that bound allows.

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

**Provenance of the candidate set and of the stated expectations.** Three things were fixed before
the correlations were computed, and each is on record in the project's analysis documents. First,
the candidate variants of each family were listed in advance, together with the expected sign of
each, and the analysis records state this for the conditional family
(`paper/conditional_similarity_transfer.md`), the niche family (`paper/niche_overlap_transfer.md`)
and the marginal and regime families (`paper/regime_transfer_correlation.md`). Second, the null
expectation for fire-regime distance, that it would not order transfer, was written down before the
regime correlation was run and is recorded in `paper/regime_transfer_correlation.md`. Third, the
directional hypothesis behind the whole comparison, that conditional measures would order transfer
where marginal measures would not, comes from the project's direction document
(`paper/POSITIONING.md`, Section 5), which sets it out as the analysis still to perform. These are
entries in a project analysis log. They are **not** a formal pre-registration. No independent
timestamped public registration exists, and the records entered version control on the same day the
diagnostics were computed, 2026-08-08. The claim made here is therefore the narrow one: the
candidates and their expected signs were fixed in advance under the project's own honesty rule, and
they are on record in named files. A reader who wants a stronger guarantee than an internal log
should read the regime and conditional results at that reduced strength.

**Multiplicity.** Twenty candidate variants are correlated against the same target quantity. One of
them, the signed-AUC vector Spearman restricted to CI-supported features, is not computable, because
only two directions retain three or more jointly supported features. Nineteen variants are therefore
computed. They share the same transfer AUCs and an effective sample of ten unordered pairs, or six
for the measures available only on the four-region subset. Two intervals exclude zero, both in the
conditional family. **No multiplicity correction is applied, and no family-wise error control is
claimed.** The two surviving intervals must not be read as significance at a controlled error rate.
What can be said in mitigation is limited but real. The families and their variants were specified
in advance rather than searched over, so the twenty are a fixed list and not the survivors of a
wider hunt. The conditional-versus-marginal contrast is a directional hypothesis stated before
computation, so the two surviving variants are the ones that hypothesis pointed at rather than an
arbitrary pair picked after the fact. Neither point substitutes for an error-rate correction, and
none is offered.

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
replicates, seed 42, blocks resampled with replacement independently within each domain). The domain
classifier itself never uses burned labels. Design read from
`drive_new/diagnostics/domain_classifier_audit/comparison/manifest.json` and the per-pair manifests.

One qualification applies to the weighted area-of-applicability rows, and the upstream module states
it in its own source: the predictor weights are importances from a random forest fitted on the
**source** region's `burned` label, so the weighted index is not label-blind in the absolute sense.
It is blind to the *target's* labels, which is the property that matters for pre-deployment
screening, and that is the sense in which the marginal family is called label-free in this paper.
The unweighted support fraction, the dissimilarity quantiles, the climatic and geographic distances
and the domain classifier use no label at all.

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
(`paper/conditional_similarity.mjs`). This index requires burned labels (or a labelled probe) in
**both** regions: it diagnoses concept alignment and is not a label-free deployment screen.

The same is true of two of the three families it is compared against, and the paper's taxonomy is
stated here once so that no section overstates the contrast. Burned-niche overlap (Section 3.14.3)
is defined on the burned cells of both regions, and fire-regime structure (Section 3.14.5) on the
target's burned map, so both require the target's labels exactly as this index does. Only the
marginal P(x) family, comprising the area-of-applicability rows, the domain classifier and the
climatic and geographic distances, is computable before any target label exists. The correct split
is therefore **target-label-free** (marginal) against **target-label-requiring** (P(x|y=1), P(y) and
P(y|x)), not conditional against everything else. This sharpens rather than softens the comparison
in Section 4.4: niche overlap and the conditional index are built from the same labelled
information, and only the conditional one orders the transfer matrix. It also means the single
family that a practitioner could run before deployment is the family that fails.

### 3.14.5 Fire-regime structure

Burned-area spatial structure, P(y), is summarised by connected components of burned
natural-vegetation cells, computed with 8-connectivity on the integer grid indices
`row_500m`/`col_500m`. Per region: component count, largest-component share, and the effective
component count, the inverse Simpson index of component size shares, 1/Σ s_k². The pair-level regime
distance is |Δ log(effective count)| (primary) and |Δ largest share| (secondary), both symmetric.
The implementation was verified to reproduce the upstream burned-pattern audit ("Rejim" table)
exactly in all five regions: component counts and largest and second component sizes match
identically, and shares and effective counts match to 1 × 10⁻⁴ (`paper/burned_components.mjs`).

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
shared feature contract), minus `elevation_mean`, minus `lst_anomaly_mean`, and minus both. Those
two features are exactly the bootstrap-supported reversal set under the supported-reversal criterion
of Section 3.14.4, which is why they and no others are removed. The pipeline replicates step8b/step9b verbatim (same imputers, one-hot encoding,
classifier and seed), and **hard parity assertions** abort the run on any deviation of the full
configuration from the frozen outputs, with a tolerance of 5 × 10⁻⁴ against the 20 step9b transfer
AUCs and 1 × 10⁻³ against the step8c within-region out-of-fold AUCs. The observed deviations were
0.0000 everywhere. Within-region evaluation reuses the spatially blocked out-of-fold protocol of
Section 3.8 (2-cell blocks, `StratifiedGroupKFold`, seed 42). All deltas (configuration minus full)
are formed inside each replicate of a paired ≈5 km-block bootstrap (10-cell blocks, 1,000
replicates, `default_rng(42)`), so every interval is on the paired difference
(`paper/feature_drop.py`; report `paper/feature_drop_transfer.md`).

## 3.16 Additional sensitivity designs

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
here. Both checks pass on the executed output, but the guarantee for this experiment
rests on A08. The decision to keep this pair out of the 20-direction transfer matrix is therefore
verifiable in the released code rather than resting on the text of this paper. The pre-label burn
exclusion of Section 3.2 ran for both arms of this pair: cells that burned inside an experiment's
own predictor window are removed from its analysis universe rather than counted as unburned. That is
the same safeguard used for Evia and Montiferru, and it is a stricter treatment than the two regions
where it did not run (Manavgat, and Bejís where no status is recorded). It removed 49 cells from the
2021 arm and none from the 2022 arm.

**A second and much larger exclusion applies to the 2022 arm alone, and it defines that arm's
population.** The registry sets `exclude_historical_burns` for `mugla_2022_event_relative` only, with
`mugla_2021` as the source and a frozen expected count of 3,073. The mask is every cell with
`burned = 1` in the 2021 canonical Step 8A artefact, without any further restriction by land cover,
eligibility or modelling validity. Applied to the 2022 arm it removes 3,073 cells, of which 2,941
belong to the primary natural-vegetation population. The primary population therefore falls from
41,730 rows in the 2021 arm to 38,790 in the 2022 arm, a drop of 7.0 %, and the removed cells are
the 2021 scar itself: 2,911 of the 2,941 are 2021 burned cells, with a median elevation of 563 m and
a maximum of 1,975 m. The design intent is to stop the previous year's burn scar, which carries an
altered surface, from entering the following year's analysis. The consequence for how these two
transfer directions may be read is set out in Section 4.8, and it is the reason they are reported
separately from the 20-direction matrix rather than inside it.

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
