# Manavgat 2021 label correction (label window 28–31 July)

The corrected table in this directory is the **primary** Manavgat 2021 data for the paper.
The frozen export is still available through `_canonical.load(region, labels="frozen")`.
The machine-readable record of every check below is in `labelfix_verification.json`.

## 1. Defect

The Manavgat label window in `repo/core/regions.py` (`EXPERIMENTS["manavgat_2021"]`) is
**2021-07-28 → 2021-08-31**, which is DOY 209–243. The frozen raw BurnDate raster
`drive_new/experiments/manavgat_2021/validation/labels/mcd64a1_raw.tif` contains only
DOY 213–241: values {0, 213–221, 241}. Every MCD64A1 burn dated 28–31 July 2021
(DOY 209–212) is missing, and these are the fire's first four days. Because those
pixels are 0 in the raster, the frozen table treats the affected cells as unburned
negatives.

## 2. Cause

`repo/src/step6_validate_fire_relation.py` used to query the monthly MCD64A1 collection
with `filterDate(label_start, label_end)`. Each monthly image has
`system:time_start` on the 1st of its month. The July 2021 image (time_start 2021-07-01)
therefore fell outside [2021-07-28, 2021-08-31] and was silently dropped. Only the
August image was read, and it holds no July BurnDates.

- The fix is repo commit **`183be42`** (2026-07-11 01:34 +0300). It added
  `_mcd64a1_collection_query_bounds`, which month-aligns the query to
  [2021-07-01, 2021-09-01), and made `build_raw_burndate_image` mask each image by
  DOY to the scientific window.
- The frozen Manavgat raster was exported on **2026-07-08** (file dates of
  `mcd64a1_raw.tif`, `mcd64a1_burned.tif` and `burned_landcover_gate.json`), before the
  fix. It was never re-exported. The frozen step8a table (2026-07-28) was built from it.

## 3. Procedure

Script: `paper/code/manavgat_labelfix.py`. It imports the pipeline functions and
does not reimplement them.

| Stage | What is imported / used |
|---|---|
| EE rebuild | `repo/src/step6_validate_fire_relation.build_raw_burndate_image(get_region_for_experiment("manavgat_2021"), "2021-07-28", "2021-08-31")`, via `paper/code/ems_labels_common.s6()` / `region_geometry()`. Collection `MODIS/061/MCD64A1`, query window 2021-07-01 → 2021-09-01 (exclusive), per-image DOY mask 209–243, max composite, clipped to the AOI. |
| Read on the frozen grid | `ems_labels_common.fetch()`: read-only `ee.data.computePixels`, `unmask(-32768).toInt16()`, in 800-row chunks on the frozen raster's own affine grid. No Drive export. The same route was validated pixel-exact against the frozen rasters of other regions in the r5 analysis (`paper/ems_analyses/labels/`). |
| Grid | EPSG:4326, 2970 × 2338 px, transform (0.00026949458523585647, 0, 31.049818637949205, 0, −0.00026949458523585647, 37.350063051593054), int16, nodata −32768, 256×256 tiles, deflate. Read from `mcd64a1_raw.tif`. The written file's profile equals the frozen one key for key. |
| Binary mask | `raw > 0` written as uint8 with nodata 0, which matches the pipeline's `raw_image.gt(0)` export and the frozen `mcd64a1_burned.tif` profile. In the frozen pair, burned == (raw > 0) holds exactly. |
| 500 m labels | `repo/src/step8a_prepare_500m_modeling_dataset.build_dataset` (the inline label block at L1190–1265, using `compute_cell_identity`, `mode_and_agreement`, `doy_to_month_and_date`, and `make_tile_grid`), plus `inspect_label_raster`. Inputs: reference `gate_inputs/reference_30m.tif` (same grid), landcover `gate_inputs/landcover_esa_worldcover_v200_aligned_to_reference.tif`, block size 17, no pre-label or historical exclusion (none for Manavgat). Only the label columns are taken from this run. |
| Gate | `repo/src/step6b_burned_landcover_gate.compute_gate` with thresholds from `core/config.py` (min_positives 30, natural 0.5, cropland 0.5), and the same reference and landcover. |

Safeguards: `PYTHONDONTWRITEBYTECODE=1` and `sys.dont_write_bytecode`. The pipeline's
`core.io_utils.setup_logger`, which writes `repo/logs/*.log`, is replaced before import
by a logger that only writes to the stream. The number of files in `repo/logs` was 130
both before and after the runs. Temporary directories are used for the
`output_dir` arguments. Nothing was written to `repo/` or `drive_new/`.

## 4. Raster verification

| Check | Result |
|---|---|
| Fresh EE read == cached read (`eecache/manavgat_2021_labelwin.npy`, r5) | identical |
| Frozen positive pixels | 179,667 |
| (a) Frozen positive pixels with the same value in the corrected raster | 179,667 (0 changed) |
| Nodata pixels (frozen / corrected) | 0 / 0 |
| Positive pixels removed | 0 |
| (b) Added pixels (frozen 0 → corrected > 0) | 624,130, all DOY 209–212 |
| Added by DOY | 209: 41,641 · 210: 380,662 · 211: 117,283 · 212: 84,544 |
| Corrected positive pixels | 803,797 |

## 5. Control: step8a code path on the frozen raster

The label columns were compared against the canonical parquet (SHA-256 `054a1961…`),
matched by `cell_id`, with row and column indices asserted equal. Floats were compared
bit for bit and NaN == NaN.

| Column | Disagreements |
|---|---|
| burned | 0 |
| burn_date | 0 |
| burn_month | 0 |
| burn_day_of_year | 0 |
| label_source | 0 |
| burn_date_pixel_agreement_fraction | 0 |
| out_of_window_burndate | 0 |

**The control passes.** As a grid-alignment check, the same call also reproduces all 10
landcover-derived columns (`landcover_*`, `burnable_*`) with 0 disagreements.

Label-derived columns: the seven above are the only columns that depend on the label
raster. `pre_label_burn_excluded`, `analysis_eligible` and `valid_for_modeling` depend
on the pre-label manifest (none for Manavgat) and on predictor QA, never on the label
(step8a: "The label NEVER makes a cell invalid-for-modeling").

## 6. Corrected table: per-column comparison with the canonical file

`step8a_500m_modeling_dataset_labelfix.parquet` has 24,150 rows and 79 columns, in the
same order and with the same dtypes as the canonical file. It was re-read from disk and
compared bit for bit:

- **72 non-label columns are identical** to the canonical file (0 differing cells each),
  including every feature, `valid_for_modeling` and `burnable_tree_shrub_grass`.
- The 7 label columns equal the step8a recomputation on the corrected raster. The
  number of cells differing from the frozen labels is: burned 2,250; burn_date 2,360;
  burn_month 2,360; burn_day_of_year 2,360; burn_date_pixel_agreement_fraction 2,465;
  label_source 0; out_of_window_burndate 0.

The 2,360 date changes are 2,250 newly burned cells plus 110 previously burned cells.
In those 110 cells the modal positive DOY is now a July day (step8a takes the mode of
the positive DOYs). No burned cell becomes unburned.

## 7. Counts

| Population | n | burned (frozen) | burned (corrected) | prevalence frozen → corrected | gained | lost |
|---|---|---|---|---|---|---|
| all cells | 24,150 | 796 | 3,046 | 3.30% → 12.61% | 2,250 | 0 |
| all_valid (`valid_for_modeling`) | 24,087 | 796 | 3,046 | 3.30% → 12.65% | 2,250 | 0 |
| natural vegetation (valid ∧ `burnable_tree_shrub_grass`, primary) | 20,511 | 784 | 2,935 | 3.82% → 14.31% | 2,151 | 0 |

Burned cells by `burn_day_of_year`, as the cell's modal positive DOY:

| DOY (date) | all_valid frozen | all_valid corrected | nat. veg. frozen | nat. veg. corrected |
|---|---|---|---|---|
| 209 (28 Jul) | 0 | 158 | 0 | 136 |
| 210 (29 Jul) | 0 | 1,429 | 0 | 1,359 |
| 211 (30 Jul) | 0 | 433 | 0 | 418 |
| 212 (31 Jul) | 0 | 340 | 0 | 338 |
| 213 | 247 | 191 | 242 | 190 |
| 214 | 205 | 171 | 198 | 170 |
| 215 | 231 | 217 | 231 | 217 |
| 216 | 68 | 68 | 68 | 68 |
| 217 | 17 | 17 | 17 | 17 |
| 218 | 6 | 4 | 6 | 4 |
| 219 | 9 | 9 | 9 | 9 |
| 220 | 6 | 6 | 6 | 6 |
| 221 | 2 | 2 | 2 | 2 |
| 241 | 5 | 1 | 5 | 1 |
| **total** | **796** | **3,046** | **784** | **2,935** |

By month (corrected): July 2,360 and August 686 (all_valid); July 2,251 and August 684
(natural vegetation). The frozen table has only August burns. Step8a's own
`burn_month_counts` has fixed keys {8, 9, 10}; it gains a key 7 through `.get()`. This
affects only the stats JSON, which is not rewritten here.

## 8. Burned-landcover gate (step6b, recomputed)

Control: `compute_gate` on the frozen raster reproduces all 20 compared fields of the
frozen `burned_landcover_gate.json` exactly (counts, fractions, decision, reason and
thresholds).

| Field | Frozen | Corrected |
|---|---|---|
| burned_count / unburned_count | 796 / 23,354 | 3,046 / 21,104 |
| burned tree / shrub / grass / cropland (dominant) | 708 / 1 / 74 / 2 | 2,321 / 28 / 561 / 54 |
| burned permanent_water / bare / built_up | 10 / 1 / 0 | 80 / 1 / 1 |
| burned_natural_vegetation_fraction (tree+shrub+grass) | 0.9837 | 0.9554 |
| burned_tree_shrub_fraction | 0.8907 | 0.7712 |
| burned_cropland_fraction | 0.0025 | 0.0177 |
| **decision** | **wildfire_candidate_pass** | **wildfire_candidate_pass** |

The gate verdict is unchanged. The natural-vegetation fraction is 0.955, well above the
0.5 threshold.

## 9. Files and hashes (SHA-256)

| File | SHA-256 |
|---|---|
| frozen `drive_new/.../validation/labels/mcd64a1_raw.tif` | `74b600bdb8b451ef2b9f9962a0de1e67cf1d8f4666de4687d56ab8c4218b861e` |
| frozen `drive_new/.../validation/labels/mcd64a1_burned.tif` | `47bfe5316236ebfc73825f1a4e507f8ab5393cb9ceda6f7c6c200e4153c3bc94` |
| frozen canonical `drive_new/.../step8a/step8a_500m_modeling_dataset.parquet` | `054a1961fc0582a33d36413263668b63074b21ae8b03d12269b6e228787f3439` |
| `mcd64a1_raw_labelfix.tif` | `8940e7060dfdba1099366bfcdf773ac4e96249840a33e82474744386614d6341` |
| `mcd64a1_burned_labelfix.tif` | `9d6427b36264e11e38354a88bf31f605d42e67282368134b229db3b78a6b5973` |
| `step8a_500m_modeling_dataset_labelfix.parquet` | `e4ab8b85df0d3a0b15f7404050b10ea062dd164f474b7791324ffdec0daa4d49` |

Reproducibility: two runs, one with a fresh EE read and one from the cache, produced
byte-identical rasters and parquet (identical hashes). `labelfix_verification.json` is
the record of the fresh-EE run.

## 10. Registration (`paper/code/_canonical.py`)

- `load(region, columns=None, labels=None)` and `path(region, labels=None)`.
- `labels` is `"corrected"` (default) or `"frozen"`. If the argument is omitted,
  `$THERMAL_TWIN_LABELS` is used, and the default is `"corrected"`. An explicit argument
  takes precedence over the environment variable.
- `CORRECTED` maps `manavgat_2021` to this parquet and its hash. Every other region
  returns its frozen file under both settings.
- Every file returned is SHA-256 verified, including the corrected one; a mismatch
  raises `ProvenanceError`.

## 11. Regenerate

From `C:\Users\CORSAIR\projects\thermal-twin-main` in PowerShell:

```powershell
$env:PYTHONDONTWRITEBYTECODE = "1"
C:\Users\CORSAIR\projects\thermal-twin\.venv-step10\Scripts\python.exe paper\code\manavgat_labelfix.py --cache <cache_dir> --fresh
```

`--fresh` reads from Earth Engine (`ee.Initialize(project="thermaltwin")`, read-only
`computePixels`). If `<cache_dir>\manavgat_2021_labelwin.npy` exists, the fresh read
must equal it; otherwise the read is saved there. Without `--fresh`, the cached array is
used. The script stops before writing the table if the raster checks or the control
fail.
