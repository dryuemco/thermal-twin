# Label-quality and predictor analyses (referee R3): specification

Written 2026-09-19 **before any of the four analyses was run**. Facts established while writing
this, and nothing else, are listed under "Pre-run facts". No outcome (count, AUC, delta) had been
computed when this file was written. Anything decided after a result was seen is marked
**[post-hoc]** in REPORT.md.

## Pre-run facts (inspection only)

- `drive_new/experiments/<region>/validation/labels/mcd64a1_raw.tif` is **DOY-masked to the label
  window** for all five regions. `repo/src/step6_validate_fire_relation.py::build_raw_burndate_image`
  sets every BurnDate outside `[label_start, label_end]` to 0, and the stored values confirm it
  (Manavgat 213–241 against a window of DOY 209–243; Bejís 227–237 against 227–273). **A pre-label
  burn is therefore invisible in the local Manavgat and Bejís products**: they record it as 0, the
  same as unburned. Request 1 cannot be answered from local data and is answered from Earth Engine.
- Muğla, North Evia (extended) and Montiferru have a separate `mcd64a1_prelabel_raw.tif`
  and a `pre_label_excluded_cells.parquet`. Manavgat and Bejís have neither. Manavgat's parquet
  carries `pre_label_burn_excluded`, all False. Bejís's parquet has no such column.
- All label rasters sit on the 30 m EPSG:4326 reference grid (`gate_inputs/reference_30m.tif`,
  identical transform and shape). The ~500 m cell is a 17 × 17 block of that grid, with truncated
  edge blocks (`row_500m = row_off // 17`).
- The upstream pre-label rule (`step6b_burned_landcover_gate.py`, around line 560) excludes a cell
  when **any** sub-pixel in its 17 × 17 block has a positive pre-label BurnDate. The label rule
  (`step8a`, around lines 1190–1265) marks a cell burned when the **mode** of its positive
  sub-pixel DOYs falls inside the label window. For a raster that holds only in-window
  positives, as both products do, the two rules are identical: a cell is flagged if and only if it
  has at least one positive sub-pixel.

## Shared machinery (all analyses)

- **Data:** `paper/code/_canonical.py::load(region)`, SHA-256 verified. `assert_no_leakage()` is
  called on every feature list before every fit.
- **Population:** primary natural vegetation (TSG): `valid_for_modeling & burnable_tree_shrub_grass`.
- **Within-region model and CV:** imported, not reimplemented: `step10/within_cv.py::run_oof`
  (StratifiedGroupKFold, 5 folds, shuffle, seed 42, blocks `row_500m//B`, `col_500m//B`) and
  `step10/spatial_bootstrap.py::delta_block_bootstrap_ci` (paired, 1000 replicates, seed 42, same
  B blocks). This is the code that produced Table 1. The RF is the paper's (300 trees, unlimited
  depth, `min_samples_leaf=3`, balanced, `random_state=42`). `n_jobs` is set to 4, which does not
  change a random forest's output. **Reference arm first:** each run recomputes the unmodified
  population and must reproduce Table 1 (±0.001) before any modified arm is read.
- **Transfer (request 2):** the pipeline used by `paper/code/verify_aoi_transfer.py`. Median and
  most-frequent imputers plus one-hot are fitted on the source only. The model is fitted on the
  whole source TSG population and scored on the whole target TSG population. No target label is
  used. Paired thermal − baseline delta per direction. The interval is a target spatial-block
  bootstrap (`delta_block_bootstrap_ci`, 1000 replicates, seed 42) at B = 10, the scale the paper
  defends, with B = 2 also reported for comparability with Table R6. **Reference arm first:** the
  20 unmodified directions must reproduce `paper/baseline_vs_thermal_transfer.csv` points to
  ±0.002.
- **Earth Engine:** `ee.Initialize(project="thermaltwin")`, read-only `ee.data.computePixels`. No
  export task is ever started. The label image is built by **importing**
  `build_raw_burndate_image` from `repo/src/step6_validate_fire_relation.py`, run with bytecode
  writing disabled so nothing is written into `repo/`. The region geometry is imported from
  `core.regions.get_region_for_experiment`. Pixels are requested on the exact affine transform and
  shape of the local `mcd64a1_raw.tif` (nearest neighbour, which is Earth Engine's default and the
  pipeline's), unmasked to −32768 as the pipeline's GeoTIFFs are, and tiled under the request-size
  limit.
- **Validation of the Earth Engine route before use (hard gate):**
  (V1) the label-window image for Manavgat and Bejís must reproduce the local `mcd64a1_raw.tif`
  pixel for pixel; (V2) the pre-label image for Muğla, Evia and Montiferru must reproduce the local
  `mcd64a1_prelabel_raw.tif` and the recorded exclusion counts of 49, 16 and 61. If either fails
  materially, the Earth Engine results are reported as unvalidated and no model is rerun on them.

## Analysis 1: pre-label burn exclusion, Manavgat and Bejís

- **Window:** `pre_label_burn_window` if registered, otherwise the predictor window. That is the
  fallback `export_raw_mcd64a1_prelabel_labels` itself uses. Manavgat 2021-06-01..2021-07-27;
  Bejís 2022-06-15..2022-08-14.
- **Count:** cells with ≥ 1 positive sub-pixel, reported for all grid cells, for
  `valid_for_modeling` cells, and for TSG cells, with how many of them are also labelled burned.
- **If the TSG count is > 0:** rerun the baseline-vs-thermal comparison at B = 2 and B = 10 with
  those cells removed, and report baseline AUC, thermal AUC, ΔAUC with its CI, and the change
  against the reference arm. **If it is 0:** no rerun, since the population is unchanged.
- **Deliverable:** the exact corrected §3.2 sentence.

## Analysis 2: earlier-year fire screening, all five regions

- **Years:** the five calendar years before the event year, Y−5..Y−1: the four registered
  baseline years plus one earlier. Manavgat, Muğla, Evia and Montiferru use 2016–2020; Bejís uses
  2017–2021. All are complete calendar years.
- **Image:** `MODIS/061/MCD64A1` filtered to [Y−5-01-01, Y-01-01). Per calendar year, a pixel is
  burned if any monthly `BurnDate > 0`, and the year bits are packed into one integer. Per-year
  counts and the union are reported.
- **Cell rule:** the same as the pre-label rule: ≥ 1 positive sub-pixel in the 17 × 17 block.
- **Also counted, not modelled:** the gap from Y-01-01 to the day before predictor_start, which
  neither the baseline years nor the pre-label window covers. It is built with the pipeline's own
  `build_raw_burndate_image` on that window.
- **Reruns with the union-of-five-years cells removed from TSG:**
  (a) within-region increment at B = 10, all five regions (reference arm plus exclusion arm);
  (b) the 20-direction as-drawn transfer, baseline and thermal, exclusion applied to source and
  target: the mean baseline AUC, mean thermal AUC and mean paired delta over 20 directions, with
  CI-supported positive and negative counts at B = 10 and B = 2;
  (c) the "hotter surfaces burned less" sign: signed AUC of `current_lst_mean` (the "LST raw" of
  Appendix A(k)), and also of `downscaled_lst_mean`, `fused_lst_mean` and `current_tvdi_mean`, on
  the 10 km collar exactly as `verify_matched_gap.py` defines it (distance to the nearest burned
  TSG cell × 0.45 km, recomputed after exclusion) and on the full frame. The 95 % interval is a
  10-cell block bootstrap (1000 replicates, seed 42). **"Survives"** means the point estimate
  stays below 0.5 in all five regions. Interval support is reported separately.

## Analysis 3: burned-fraction threshold

- **Recoverable?** From the local 30 m `mcd64a1_raw.tif`: for each 17 × 17 block, f = (number of
  sub-pixels with in-window BurnDate > 0) / (number of non-nodata sub-pixels). A check comes
  first: `f > 0` must equal the parquet `burned` for every cell. **Interpretation stated in
  advance:** the 30 m raster is a nearest-neighbour duplication of 463 m MODIS sinusoidal pixels,
  so f is the share of the reconstructed cell's area covered by the footprints of MODIS pixels
  flagged burned. It is **not** a sub-500 m burned fraction, which MCD64A1 does not carry.
- **Rerun:** burned := f ≥ 0.5; cells with 0 < f < 0.5 are dropped as ambiguous; unburned := f = 0.
  Within-region increment at B = 2 and B = 10, all five regions, against the reference arm. The
  number of dropped cells and the number of positives lost are reported.

## Analysis 4: effective dimensionality of the thermal block

- **Per region, TSG population:** the 6 × 6 Pearson correlation matrix of the six thermal channels
  on complete cases, and a PCA of the standardised channels (correlation-matrix PCA) on complete
  cases, giving the explained-variance ratios and the components needed for 90 % and 95 %.
  Secondary: the same PCA after median imputation, which is what the classifier sees.
- **`fused_lst_mean == current_lst_mean`:** exact float equality among rows where both are finite,
  plus the counts where exactly one is missing and where both are, and the maximum absolute
  difference.

## Verdict rules (fixed in advance)

- The within-region increment "holds" if the ΔAUC 95 % CI still excludes 0 at the scale it did
  in Table 1. "Materially changed" means |Δ(ΔAUC)| ≥ 0.01 or a change in CI support.
- The transfer thesis ("the thermal block nets to about zero in transfer") holds if the mean paired
  delta stays within ±0.02 of zero and positive and negative CI-supported directions both remain.

---

## Addendum A (2026-09-19, written after validation gate V1 failed for Manavgat, before any analysis below was run)

**What V1 found:** the Earth Engine label-window image reproduces Bejís's frozen `mcd64a1_raw.tif`
exactly (0 mismatches in 4,535,255 pixels). For Manavgat every frozen positive is reproduced, but
Earth Engine has **624,130 further positive sub-pixels, every one dated DOY 209–212
(28–31 July 2021)**. The frozen raster holds no value below DOY 213 (1 August). This is the defect
that `_mcd64a1_collection_query_bounds` in `step6_validate_fire_relation.py` documents and fixes:
a `filterDate(label_start, …)` with a label start that is not the 1st of the month silently drops
that month's image. It was observed for Bejís and corrected there. The frozen Manavgat label
predates the fix. Muğla (first value 210 = label start), Evia (215) and Montiferru (205) start
exactly on their label-start DOY, so none of them is affected. V2 passed exactly in all three
regions: 0 pixel mismatches, and 49/49, 16/16 and 61/61 excluded cells.

**Consequence for the gate:** the Earth Engine route is validated, since V1 Bejís and V2 pass
exactly and V1 Manavgat agrees on every pixel the frozen raster has. The Manavgat discrepancy is
a defect in the frozen product, not in the route. Requests 1–4 proceed on the frozen labels as
specified, because they ask about the paper's data as it stands.

**Added analysis 5 (not requested; reported because it is a label-quality defect of the kind R3 is
about):** Manavgat with the full label window (2021-07-28..08-31) rebuilt by the pipeline's own
function (the V1 image). The cell rule is unchanged: ≥ 1 in-window positive sub-pixel.
- The number of cells that change from 0 to 1 (all, `valid_for_modeling`, TSG), and the
  new TSG prevalence.
- Within-region increment at B = 2 and 10, reference against corrected.
- Signed univariate AUC of the nine numeric predictors, full TSG frame, 10-cell block bootstrap
  (1000 replicates, seed 42). The same instrument as Table B3, so the Manavgat elevation reversal
  (0.374) can be read against it.
- The 20-direction transfer (baseline and thermal, paired delta) with corrected Manavgat labels.
  Other regions are unchanged.
`valid_for_modeling` and the population are label-independent, so no cell enters or leaves.

## Addendum B (2026-09-19, [post-hoc]: written after the Bejís request-1 rerun had been seen)

Removing 48 of 15,190 Bejís cells moved the 10-cell ΔAUC from +0.045 to +0.062. That is more than
48 cells plausibly carry, which suggests that re-drawing the folds, not the cells removed, drives
much of the change: StratifiedGroupKFold reassigns blocks to folds whenever the population
changes. To read every exclusion arm against the right yardstick, two calibrations are run. Neither
changes any primary number.
- **Fold-draw spread:** each region's reference population at B = 10 (and B = 2 for Manavgat and
  Bejís), with the CV splitter seed set to 1..10 and the RF kept at `random_state = 42`. Reported:
  the ΔAUC range and SD.
- **Random-removal null for request 1:** 48 TSG cells drawn at random from Bejís's unflagged cells
  and removed, 20 draws (numpy seed 42), at B = 2 and B = 10. Reported: where the observed change
  falls in that distribution.
