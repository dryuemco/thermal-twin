# Product specifications: quality masks, class mapping, compositing and aggregation

Status: **FINAL v1.0 (2026-09-19), companion to PREREGISTRATION.md v1.1; where they differ
PREREGISTRATION.md governs.** Nothing here has been run on labels or outcomes.

**How to read this document.** Each rule is tagged:
- **[SRC]**: taken from the official product documentation or the Earth Engine (EE) catalogue/STAC band
  metadata. The URL and section are given.
- **[EE-CHK]**: confirmed by a read-only EE query on 2026-09-19 (`ee.Initialize(project="thermaltwin")`).
  No exports were run.
- **[DESIGN]**: a registered rule of this study. It is not in any product document, so the text gives the
  reason. These are the parts of this document that bind us.

EE band metadata is cited as the STAC record
`https://storage.googleapis.com/earthengine-stac/catalog/<folder>/<ID>.json`, which is the source of the
catalogue page `https://developers.google.com/earth-engine/datasets/catalog/<ID>` ("Bands" table).

Registered sensitivity analyses are listed once, in §19. Everything else in this document is the primary
rule.

---

## 0. Conventions that hold for every product

### 0.1 Tiles and analysis grid [DESIGN + SRC + EE-CHK]
- **Tiles [DESIGN]:** the primary tile is **1.0° × 1.0° in EPSG:4326, with edges at integer degrees**.
  The 0.5° tiling (edges at integer multiples of 0.5°) is used only to report an eligibility count; no
  analysis is run on it.
- **Analysis cells:** MODIS sinusoidal 463.3127 m cells (the MCD64A1 grid) whose centre falls in the tile
  (PREREGISTRATION.md §3).
- **Neighbourhood rule [DESIGN]:** every neighbourhood or distance computation (G1 TPI, G1 slope/aspect
  edges, G2 3 × 3 shares, G6 road distance) uses data outside the tile. No value is computed from a
  tile-clipped raster.
- **Grid [SRC + EE-CHK]:** CRS `SR-ORG:6974` (MODIS sinusoidal, sphere R = 6 371 007.181 m). Cell size
  w = T/2400 = **463.31271653 m**, with x_min = −20 015 109.354 m and y_max = 10 007 554.677 m.
  Sources: MCD64 User Guide C6.1, Appendix B (https://lpdaac.usgs.gov/documents/1006/MCD64_User_Guide_V61.pdf);
  MCD12 User Guide C6.1 §2 (https://lpdaac.usgs.gov/documents/1409/MCD12_User_Guide_V61.pdf).
- EE-CHK, native transforms:
  - MCD64A1, MCD12Q1, MOD13A1, MOD15A2H, MOD16A2GF and VNP64A1 all use scale 463.3127165279165 m, and
    their origins differ only by whole multiples of 2400 cells. They are **the same grid**, so no
    resampling is needed.
  - MOD11A1 and MOD14A1/MYD14A1 use 926.6254331 m with an origin 1.8 mm from the 463 m origin. So
    **every 463 m cell lies wholly inside one 1 km cell** (2 × 2 nesting).
  - MOD44B uses 231.656 m, so **each 463 m cell contains exactly 2 × 2 MOD44B pixels**.
  - The following are on other grids and use the kernels of §0.2: ERA5-Land (EPSG:4326, 0.1°, origin
    −180.05/90.05), TerraClimate (1/24°), CHIRPS (0.05°), GLO-30 (1″), GHSL (Mollweide 100 m), VIIRS DNB
    (15″) and FireCCI51 (0.0022457°).

### 0.2 Kernels [DESIGN]
| Case | Kernel | Why |
|---|---|---|
| Same 463 m grid | none (native) | Identical grid, so nothing to resample. |
| Coarser product nested exactly (1 km MODIS) | **parent value**: each 463 m cell takes the value of the 1 km pixel that contains it | Exact containment. Bilinear would mix neighbouring 1 km retrievals with different QC states and dates, and would make up sub-kilometre detail that is not there. |
| Finer product (30 m, 100 m, 15″, 250 m) | **area-weighted mean** of the fine pixels over the cell footprint (EE `reduceResolution(mean)` onto the 463 m grid; for GHSL, a sum converted to a density, §12) | Preserves the cell mean. It is the only kernel that is consistent with a label defined on the whole cell. |
| Coarse continuous climate fields (ERA5-Land 11 km, TerraClimate 4.6 km, CHIRPS 5.6 km) | **nearest** (the coarse pixel that contains the cell centre). If that pixel is masked (sea), take the mean of the valid pixels in its 3 × 3 neighbourhood, otherwise leave the cell missing | Keeps the product's own values and effective resolution. Bilinear would imply a sub-pixel gradient the product does not resolve, and would blur the fact that many 463 m cells share one weather value (the reason for the 11 km block-size floor, STUDY_DESIGN §6). Non-linear derived quantities (FWI codes, VPD) are computed on the native grid **before** assignment. |

**Order of operations [DESIGN]:** quality mask → temporal composite on the product's **native** grid →
spatial aggregation to 463 m. We never composite after resampling.

### 0.3 Windows, leap years and anomalies [DESIGN; DOY table from SRC]
- Season *y* = 1 June to 31 October *y*. In day-of-year (DOY) that is **152–304 in common years and
  153–305 in leap years**. From the MCD64 User Guide C6.1 §3.1.1, Table 2: June starts on DOY 152 (153 in
  a leap year), and November starts on DOY 305 (306). The leap years in the study are **2016, 2020 and
  2024**. Implementations derive the DOY from calendar dates and never hard-code 152–304.
- Pre-season predictor window: every window ends on **31 May *y*** (inclusive). The surface-state window
  is **1 March to 31 May *y*** (92 days). Precipitation uses 3, 6 and 12 months ending on 31 May (§10).
- A product composite period counts towards a window only if its **whole period lies inside the window**,
  judged by the image's `system:time_start` and `system:time_end`.
- **Baseline** = the five preceding years' same window, *b* ∈ {*y*−5, …, *y*−1}. Each baseline level is
  computed with the identical window and rule.
  - Difference anomaly = level(*y*) − mean of the baseline levels.
  - z-score anomaly = (level(*y*) − mean of the baseline levels) / standard deviation of the baseline
    levels.
  - Which form each variable uses is stated in its section.
  - **Burned-cell exclusion (surface products only: MOD13A1, MOD15A2H, MOD16A2GF, MOD11A1)** [DESIGN,
    implementing STUDY_DESIGN §4]: for each cell, baseline year *b* is dropped if MCD64A1 mapped the cell
    burned at any date from 1 June *b*−1 to 31 May *b*.
  - At least 3 of the 5 baseline years must remain, otherwise the anomaly is missing.
  - Climate fields (ERA5-Land, TerraClimate, CHIRPS) are not burn-filtered, because a fire does not alter
    their values.
- **Minimum observation counts (registered, final):** MOD13A1 ≥ 2 accepted composites (§3); MOD15A2H
  ≥ 3 accepted periods (§4); MOD16A2GF every period present (§6); MOD11A1 ≥ 5 accepted days (§7);
  baseline ≥ 3 of 5 years (above).

### 0.4 Temporal-validation rule for MCD64A1-derived predictors [DESIGN]
For V2 training seasons (PREREGISTRATION.md §6), G7 (§1) and the baseline burned-cell exclusion masks
(§0.3) are recomputed with the **target season's MCD64A1 treated as unobserved**: the months June–October
of the target season contribute no burn to any training season's G7 value or baseline mask.

---

## 1. MCD64A1 v6.1: label and fire history (`MODIS/061/MCD64A1`)

**Bands [SRC]:** `BurnDate` (DOY 1–366), `Uncertainty` (days), `QA` (8-bit), `FirstDay`, `LastDay`.
- In the HDF product, BurnDate 0 = unburned land, −1 = unmapped because of insufficient data, and −2 =
  water. Source: MCD64 User Guide C6.1 §3.1.2, https://lpdaac.usgs.gov/documents/1006/MCD64_User_Guide_V61.pdf.
- **EE-CHK: in EE, BurnDate is masked wherever it is not a burn date.** Over a North Evia and sea window
  for August 2021, only DOY 214–226 were unmasked. So 0, −1 and −2 **cannot be told apart from BurnDate**
  and are read from `QA`, which is unmasked everywhere. QA values observed: 0 (water), 1 (land, not
  valid = unmapped), 3 (land, valid), 7, 11, 103 and 131.

**QA bits** [SRC: the same guide §3.1.2 and the EE STAC `MODIS_061_MCD64A1.json`]:
| Bit(s) | Meaning |
|---|---|
| 0 | 1 = land, 0 = water |
| 1 | 1 = sufficient valid data (water cells always 0) |
| 2 | 1 = mapping period shortened (the whole month could not be mapped reliably) |
| 3 | 1 = cell relabelled during contextual relabelling |
| 4 | spare |
| 5–7 | special condition code for unburned cells: 0 none/NA; 1 valid observations too sparse in time; 2 too few training observations or poor separability; 3 apparent burn date at the limits of the time series; 4 apparent water contamination; 5 persistent hot spot; 6–7 reserved |

**Scale and offset:** none.

**Label rule "burned in season *y*" [DESIGN, built on SRC]:**
1. Select the 5 monthly images with `system:time_start` in [*y*-06-01, *y*-11-01). This is the
   month-aligned query.
2. In each image, accept a burn if BurnDate is unmasked and BurnDate is in the season DOY range
   **152–304 (153–305 in 2016, 2020, 2024)**. This pixel-level filter is redundant for dates inside the
   month but guards against off-month dates.
3. `burned = 1` if any of the 5 images has an accepted burn. A cell that burned twice counts once.
4. **Water:** QA bit 0 = 0 in any season month → the cell is excluded from every population.
5. **Unmapped:** the cell is not burned and QA bit 1 = 0 in at least one season month → the label is
   **missing**. The cell is excluded and counted per tile-season.
6. **Unburned with a special condition code** (bits 5–7 ≠ 0) is **unburned**. The algorithm
   deliberately classified such cells as unburned, and code 5 (persistent hot spot, i.e. industrial
   sources) is a valid unburned case. The counts per code are reported.
7. **Shortened mapping period** (bit 2 = 1) and relabelled cells (bit 3 = 1) are kept.
8. `Uncertainty` is not used as a filter. Its median among burned cells is reported per tile-season.

**Unit tests** (STUDY_DESIGN §3) cover: windows that start mid-month; windows that span months; a
window that crosses a year boundary; the leap-year DOY shift (2016, 2020, 2024); masked BurnDate with QA
= 1 (unmapped) versus QA = 3 (unburned); and a water cell.

**Cell rule [SRC + DESIGN]:**
- MCD64A1 decides burned or unburned for each whole 463 m grid cell ("the date of burn … for 500-m grid
  cells", Guide §2), and our analysis cell *is* that grid cell. The MCD64A1 label is therefore the
  product's **native** per-cell decision. No majority or any-burn rule is applied to MCD64A1; no sub-cell
  burned fraction exists in it.
- The majority rule (burned fraction of the cell ≥ 0.5), with any-burn (fraction > 0) as its variant,
  applies **only** to the sub-cell reference labels: FireCCI 5.1 fractions (§17) and EFFIS perimeters
  (§19).

**Fire history G7 [DESIGN]:** uses the same QA handling (water, unmapped, special condition) applied to
every month, not only June–October, from January 2001 through May *y*.
- `years_since_last_burn` = *y* − the latest calendar year with an accepted MCD64A1 burn in the cell dated
  before 1 June *y*, **capped at 14**. A cell never burned since 2001 takes 14. A burn in January–May *y*
  gives 0.
- `n_burn_years` = the number of **distinct calendar years** with an accepted burn in the cell from
  **1 January *y* − 10 to 31 May *y***.
- A cell that is unmapped (QA bit 1 = 0) and not burned in a month contributes no burn for that month.
  The number of such months is reported.
- For V2 training seasons, G7 is recomputed under §0.4.

**Caveats [SRC]:**
- Global Stage-3 validation: 40.2 % commission and 72.6 % omission error, driven by small burns
  (Guide §7). Small Mediterranean fires will be missed; this is a scope limit.
- Burns in cropland are low confidence (Guide §8.1). This supports the natural-vegetation population.
- The August 2020 Aqua outage is not expected to degrade the product significantly, because Terra kept
  working (Guide §8.3.1).
- Collection 6.1 is consistent with C6 (Guide §1.1).
- EE-CHK: 120 of 120 monthly images are present for 2015–2024.

---

## 2. MCD12Q1 v6.1: population and G2 land-cover shares (`MODIS/061/MCD12Q1`)

**Scheme [DESIGN]:** **`LC_Type1` (IGBP)**, from the image for year ***y* − 1**. The EE images run from
2001 to 2024 (EE-CHK), so *y* − 1 = 2014…2023 are all available. IGBP is used because it is the only
legacy scheme with separate forest, shrubland, savanna, grassland, cropland and cropland-mosaic classes.
Classes are defined in the MCD12 User Guide C6.1, Table 3, and the EE STAC `MODIS_061_MCD12Q1.json`.
**Scale:** none. **Fill:** 255.

**Class mapping [SRC codes; DESIGN groups]:**
| IGBP code | Class (SRC definition, abridged) | Group | Population |
|---|---|---|---|
| 1–5 | Evergreen needleleaf, evergreen broadleaf, deciduous needleleaf, deciduous broadleaf, mixed forests (tree cover > 60 %, canopy > 2 m) | forest | included |
| 6 | Closed shrublands (woody perennials 1–2 m, > 60 % cover) | shrubland | included |
| 7 | Open shrublands (10–60 % cover) | shrubland | included |
| 8 | Woody savannas (tree cover 30–60 %) | savanna | included |
| 9 | Savannas (tree cover 10–30 %) | savanna | included |
| 10 | Grasslands (herbaceous < 2 m) | grassland | included |
| 11 | Permanent wetlands | — | excluded |
| 12 | Croplands (≥ 60 % cultivated) | cropland and mosaic | excluded (negative-control material) |
| 13 | Urban and built-up (≥ 30 % impervious) | built | excluded |
| 14 | Cropland/natural vegetation mosaics (40–60 % cultivation) | cropland and mosaic | excluded (added only in the §19 sensitivity) |
| 15 | Permanent snow and ice | — | excluded |
| 16 | Barren | — | excluded |
| 17 | Water bodies | water | excluded |

**Primary population:** LC_Type1(*y*−1) ∈ {1, …, 10} **and** QC ∈ {0, 8, 9}.

**QC band [SRC, Table 11 of the guide / EE STAC]:**
| Value | Meaning | Treatment |
|---|---|---|
| 0 | classified land | accepted |
| 1 | unclassified land, labelled barren | excluded |
| 2 | classified water | excluded |
| 3 | unclassified water | excluded |
| 4 | sea ice switched to water | excluded |
| 5 | misclassified water switched to the secondary label | excluded |
| 6 | omitted snow/ice | excluded |
| 7 | misclassified snow/ice | excluded |
| 8 | backfilled label | accepted |
| 9 | forest type changed (climate-based) | accepted |

EE-CHK: an Attica window showed QC 0, 2, 4, 5 and 9, with QC 9 on about 10 % of cells, so accepting 9
matters. The number of cells excluded by QC is reported.

**"Dominant class" [SRC + DESIGN]:** MCD12Q1 is native on the analysis grid and carries one class per
cell. The "dominant class" in STUDY_DESIGN §2–3 is that cell's class; no aggregation is involved.

**G2 class shares [DESIGN]:**
- For each analysis cell, the share of each group listed in PREREGISTRATION.md §5.2 (forest 1–5,
  shrubland 6–7, savanna 8–9, grassland 10, cropland and mosaic 12 and 14, built 13) among the cells of
  its **3 × 3 neighbourhood (1.39 km)** in the LC_Type1 map of *y* − 1.
- Computed on the **full MCD12Q1 grid**: neighbourhood cells outside the tile are used.
- Shares are **of land cells**: water (class 17) is excluded from the denominator.
- Plus MOD44B percent tree cover and percent non-tree vegetation of *y* − 1 (§5).

**Caveats [SRC, guide §1 and §2.2]:**
- The authors "urge users not to use the product to determine post-classification land cover change".
  So no year-to-year LC-change feature is built from it.
- "Some grassland areas are classified as savannas." This weakens the savanna/grassland distinction; we
  therefore report groups, not single classes.
- Wetlands are under-represented.
- [DESIGN note] The year *y*−1 map is built from a full year of reflectance. Cells burned in season *y*−1
  can therefore be relabelled (for example forest → grassland or savanna). This is pre-season information
  and not leakage, but the population drifts after large fires. The number of cells that change group
  between *y*−2 and *y*−1 is reported.

---

## 3. MOD13A1 v6.1: NDVI and EVI (`MODIS/061/MOD13A1`), G3

**Bands [SRC]:** `NDVI`, `EVI` (int16, valid range −2000…10000, **scale 0.0001**, no offset), `SummaryQA`,
`DetailedQA`, `DayOfYear`. Sources: MOD13 User Guide C6 §5.2, Table 1
(https://lpdaac.usgs.gov/documents/103/MOD13_User_Guide_V6.pdf) and the EE STAC.

**Quality** [SRC: guide §5.5, Tables 4–5; EE STAC]:
- `SummaryQA` (pixel reliability): 0 good; 1 marginal ("useful, but look at other QA"); 2 snow/ice;
  3 cloudy; −1 fill.
- `DetailedQA`:
| Bits | Meaning |
|---|---|
| 0–1 | MODLAND QA |
| 2–5 | VI usefulness (0 highest … 12 lowest; 13 not useful; 14 L1B faulty; 15 not processed) |
| 6–7 | aerosol quantity |
| 8 | adjacent cloud |
| 9 | BRDF correction (always 0 in practice) |
| 10 | mixed clouds |
| 11–13 | land/water (1 = land) |
| 14 | possible snow/ice |
| 15 | possible shadow |

**Accept rule [DESIGN]:** a composite value is accepted if **all** of the following hold:
- SummaryQA ∈ {0, 1};
- DetailedQA bits 11–13 = 1 (land);
- bit 10 = 0;
- bit 14 = 0;
- bit 15 = 0.

Rationale: the guide says SummaryQA 1 is "useful, but look at other QA". The rule does exactly that by
removing mixed clouds, snow and shadow. EE-CHK on a sample May 2020 composite (Attica): SummaryQA
0 = 6 828, 1 = 900, 3 = 112 cells.

**Composite and variables [DESIGN]:**
- The 16-day composites whose whole period falls within 1 March – 31 May *y* (≈ 5 composites).
- Per-cell **median** of the accepted values: `ndvi_median`, `evi_median`.
- **Minimum 2 accepted composites**, otherwise the cell is missing.
- `ndvi_anomaly_z` = z-score anomaly of `ndvi_median` against the baseline (§0.3), with the burned-cell
  exclusion.
- Spatial: native.

**Caveats [SRC, guide §5.1]:** each value is a CV-MVC composite. Adjacent pixels may come from different
days and viewing geometries. The composite day is in `DayOfYear`, which is reported but not used.

---

## 4. MOD15A2H v6.1: LAI (`MODIS/061/MOD15A2H`), G3

**Bands [SRC]:** `Lai_500m` (**scale 0.1**, m²/m²), uint8 with valid range 0–100 and fill values 249–255
(each fill value names a non-vegetated land-cover reason); `FparLai_QC`. `Fpar_500m` is **not used**.
Sources: MOD15 User Guide C6 §6, Table 4, Table 6 (https://lpdaac.usgs.gov/documents/624/MOD15_User_Guide_V6.pdf)
and the EE STAC. EE-CHK: in a window with sea and urban cells no value > 100 appeared, i.e. the fill
values are masked in EE.

**FparLai_QC bits** [SRC, guide Table 5, the same layout as MOD16 ET_QC in the MOD16 guide §6.2.1]:
| Bits | Meaning |
|---|---|
| 0 | MODLAND: 0 good (main algorithm), 1 other (back-up or fill) |
| 1 | sensor |
| 2 | dead detector |
| 3–4 | cloud state: 0 clear, 1 cloudy, 2 mixed, 3 not defined (assumed clear) |
| 5–7 | SCF_QC: 0 main RT without saturation; 1 main RT with saturation; 2 and 3 empirical back-up; 4 not produced |

The guide calls SCF_QC "the key indicator of retrieval quality", and says the main algorithm gives the
best retrievals (§3, §6.1).

**Accept rule [DESIGN]:** all of the following:
- bit 0 = 0;
- bit 2 = 0;
- bits 3–4 ∈ {0, 3};
- bits 5–7 ∈ {0, 1}.

EE-CHK (Attica, May 2020): QC values 0, 8 (cloudy), 16 (mixed), 97 (back-up) and 157 (not produced / fill).

**Composite and variable [DESIGN]:**
- The 8-day periods fully inside 1 March – 31 May (≈ 11).
- `lai_median` = per-cell **median** of the accepted values.
- **Minimum 3 accepted periods**, otherwise the cell is missing.
- Spatial: native.

**Caveat:** Mediterranean dense evergreen canopies can hit saturation (SCF_QC = 1). These values are
kept, because the guide rates them "good, very usable".

---

## 5. MOD44B v6.1: vegetation continuous fields (`MODIS/061/MOD44B`), G2

**Bands [SRC]:** `Percent_Tree_Cover`, `Percent_NonTree_Vegetation`, `Percent_NonVegetated` (%, no
scale). Valid 0–100, 200 = water, 253 = fill. Source: MOD44B User Guide C6.1 §4.1–4.3
(https://lpdaac.usgs.gov/documents/1494/MOD44B_User_Guide_V61.pdf). EE-CHK: the maximum in a window
including sea was 80, so water and fill are masked in EE. Variables used: `Percent_Tree_Cover` and
`Percent_NonTree_Vegetation`.

**Temporal definition [SRC, guide §3.4]:** the product dated YYYY065 is made "with data from YYYY065 –
(YYYY+1)064".
- **Rule [DESIGN]:** use the image dated ***y* − 1** (EE index `(y−1)_03_0x`). It covers 6 March *y*−1 to
  about 5 March *y*, so it ends before the 31 May window end. The image dated *y* includes the season and
  is not used.
- EE-CHK: images exist through `2025_03_06`.

**Quality [SRC]:** `Quality` bits 0–7 flag which of the 8 annual input composites were bad (cloud, high
aerosol, shadow, view zenith > 45°), for DOY 065–097, 113–145, 161–193, 209–241, 257–289, 305–337,
353–017 and 033–045. `Cloud` bits give the same breakdown for cloud only.
- **Rule [DESIGN]:** no masking, because this is an annual model output. The number of bad inputs per
  cell is reported.

**Spatial [DESIGN]:** a 231.656 m grid nested 2 × 2 in the analysis grid. The value is the **mean of the
valid child pixels** among the 4 (equal area); the cell is missing only if none is valid. The number of
cells with fewer than 4 valid children is reported.

**Caveats [SRC, guide §5]:** in C6.1, "areas with sparse vegetation are not retrieved and populated with
fill value of '0'". So 0 % tree cover is ambiguous in sparse areas. Validation is limited to Maryland and
Brazil sites (guide §6), so there is no Mediterranean validation.

---

## 6. MOD16A2GF v6.1: ET and PET (`MODIS/061/MOD16A2GF`), G3

**Bands [SRC]:**
- `ET` and `PET`: 8-day **sum**, kg m⁻² per 8 days, **scale 0.1**.
- `LE` and `PLE`: scale 10 000 (not used).
- `ET_QC`.
- Valid range −32 767…32 700. Fill values: 32 767 (_FillValue), 32 766 (water/salt), 32 765 (barren or
  sparse), 32 764 (snow/ice), 32 763 (wetland), 32 762 (urban), 32 761 (unclassified).
- Source: MOD16 User Guide C6.1 §6.2.1, Table 6.1 (https://lpdaac.usgs.gov/documents/931/MOD16_User_Guide_V61.pdf).
- EE-CHK: fill values are masked in EE. In an Attica window with sea and urban cells, 48 % of pixels
  were unmasked and the ET maximum was 284.

**Quality [SRC, same section]:** `ET_QC` is inherited from MOD15A2H and has the same bits. The guide
states: "For the improved and reprocessed MOD16A2 [gap-filled], users may ignore QC data layer because
cloud-contaminated LAI/FPAR gaps have been temporally filled … QC just denotes if filled LAI/FPAR were
used as inputs."
- **Rule [DESIGN, following SRC]:** no QC mask; accept every unmasked value. The share of periods with
  bit 0 = 1 is reported per tile-season.

**Variable and composite [DESIGN]:**
- `et_pet_ratio` = Σ ET / Σ PET over the 8-day periods fully inside 1 March – 31 May *y*.
- Every period must be present (the product is gap-filled); otherwise the value is missing.
- The ratio is missing if Σ PET ≤ 0.
- Spatial: native.

**Caveats [SRC]:**
- The last composite of each year is 5 or 6 days long (guide §6.2.1). It does not fall in the window.
- GF is released after the year ends (guide §3.2.1.2). Its availability (to 2025-12-27, per
  DATA_AVAILABILITY) covers 2015–2024.
- ET is not computed for urban and barren cells. These are outside the natural-vegetation population.

---

## 7. MOD11A1 v6.1: land surface temperature (`MODIS/061/MOD11A1`), G4, and why not MOD11A2

**Bands [SRC]:**
- `LST_Day_1km`: uint16, valid from 7500, **scale 0.02 K**, offset 0.
- `QC_Day`: uint8.
- `Day_view_time`: scale 0.1 h, in local solar time.
- `Day_view_angle`: offset −65°.
- Sources: MOD11 User Guide C6 §3.2 Table 9 and §3.5 Table 13
  (https://lpdaac.usgs.gov/documents/118/MOD11_User_Guide_V6.pdf) and the EE STAC.
- Conversion: LST(°C) = DN × 0.02 − 273.15.
- Only the **day** observation is used.

**QC_Day bits** [SRC, Table 13]:
| Bits | Meaning |
|---|---|
| 0–1 | mandatory QA: 00 produced, good; 01 produced, other quality (examine detailed QA); 10 not produced, cloud; 11 not produced, other reasons |
| 2–3 | data quality: 00 good, 01 other |
| 4–5 | emissivity error: ≤ 0.01 / ≤ 0.02 / ≤ 0.04 / > 0.04 |
| 6–7 | LST error: ≤ 1 K / ≤ 2 K / ≤ 3 K / > 3 K |

**Accept rule [DESIGN]:** a daily value is accepted if it was produced (bits 0–1 ∈ {00, 01}) **and** its
**LST error is ≤ 2 K** (bits 6–7 ∈ {00, 01}).
- This rule is fixed at registration. It was **not** chosen from a retention count. The retained fraction
  under this rule and under the pilot rule is measured label-free across all candidate tiles and
  **reported only**; it is not used to choose or change the rule.
- EE-CHK, one May 2020 Attica scene: 26 pixels had QC = 0, but 107 had QC = 65 (01 "other quality" with
  LST error ≤ 2 K).
- The pilot rule (`repo/core/config.py` STEP7_MODIS_QC_*, attributed to E. Metin: bits 0–1 = 00 **and**
  bits 2–3 = 00) is a registered sensitivity (§19).

**Composite and variables [DESIGN]:**
- Daily images in 1 March – 31 May *y*.
- `lst_day_median` = per-pixel **median** of the accepted day LST.
- **Minimum 5 accepted days**, otherwise missing.
- Computed on the **1 km grid**, then each 463 m cell takes its **parent 1 km value** (§0.2).
- `lst_day_anomaly_z` = z-score anomaly against the baseline (§0.3; form as in PREREGISTRATION.md §5.2),
  with the burned-cell exclusion.
- The pilot's downscaled or fused LST is **not** used.

**Why MOD11A1, not MOD11A2 [SRC]:**
- MOD11A2 is "a simple average of all the corresponding MOD11A1 LST pixels … without any filtering for
  specific QA bits". Its "QA values are set based on what majority of input daily QA values are"
  (EE catalogue description; MOD11 guide §4.1 "a simple average method").
- So a per-observation quality rule **cannot be applied** to MOD11A2, and an 8-day value can include
  "other quality" days that its QC byte does not reveal.
- MOD11A1 lets us fix the mask ourselves (STUDY_DESIGN §4). The extra cost is only compute.

**Terra orbit drift [SRC + DESIGN]:**
- [SRC, NASA Terra orbit page, https://terra.nasa.gov/about/terras-orbit-changes/terra-orbital-drift-information]
  Terra has been drifting to an earlier equatorial crossing time (about 10:15 MLT by October 2022, then a
  free drift, still earlier). Morning LST falls as the overpass moves earlier, which can produce an
  artificial negative day-LST anomaly in 2023–2024 relative to earlier baselines, independent of dryness.
- **Registered response:** every contrast involving G4 is repeated on seasons 2015–2022 only (§19).
- The median `Day_view_time` per tile-season is reported **descriptively**. It is not used to filter
  observations.
- The same drift affects MOD13A1 and MOD15A2H through illumination, but less directly.

**Other caveats [SRC]:**
- [guide §3.1] At latitudes > 30° a day's value comes from one clear-sky observation, chosen for the
  smaller view zenith angle. The data day is in UTC.
- [guide §2.1] The level-3 cloud threshold is ≥ 95 % confidence over land ≤ 2000 m and ≥ 66 % above
  2000 m. Mountain tiles therefore carry more residual cloud.

---

## 8. ERA5-Land DAILY_AGGR and HOURLY: temperature, VPD, soil water and FWI codes (G5)

**Assets [SRC, EE STAC]:** `ECMWF/ERA5_LAND/HOURLY` and `ECMWF/ERA5_LAND/DAILY_AGGR`. Both are EPSG:4326 on
a regular 0.1° grid. ERA5-Land is native TCo1279 (~9 km), delivered on a 0.1° grid (ECMWF ERA5-Land
documentation, "Spatial grid", https://confluence.ecmwf.int/display/CKB/ERA5-Land%3A+data+documentation).
Units: temperatures in K, wind in m s⁻¹, precipitation in **m**, volumetric soil water in m³ m⁻³. No
scale factor.

**Time and accumulation conventions:**
- [SRC, ECMWF docs "Accumulations"] Accumulations run from 00 UTC to the step. The value at validity time
  00 UTC is the total of the **previous** day.
- [SRC, EE HOURLY description] EE adds `*_hourly` bands "computed as the difference between two
  consecutive forecast steps".
- **EE-CHK:** `total_precipitation_hourly` at validity time *h* is the precipitation in (*h*−1 h, *h*].
  Verified: the sum of the hourly values over 01…24 UTC equals the accumulated total at the next 00 UTC.
- **EE-CHK: DAILY_AGGR `total_precipitation_sum` for day *D* equals the sum of the hourly bands at
  validity times 00…23 of *D*, i.e. the window (*D*−1 23:00, *D* 23:00] UTC.** The catalogue text says
  the daily sum is taken from "the first hour's data of the following day"; the data show a one-hour
  offset instead (checked on 2020-01-01, -05, -06 and 2020-02-05 at 38.6° N 23.0° E). It is not used for
  FWI (FWI_SPEC.md §3.4) and precipitation predictors come from CHIRPS (§10).
- **EE-CHK:** non-flow daily bands (e.g. `temperature_2m`, `dewpoint_temperature_2m`) are the mean of the
  24 hourly instants 00…23 UTC.
- [SRC, EE description] Flow bands can hold small negative values caused by GRIB packing.
  **Rule [DESIGN]:** clamp negative precipitation to 0.

**Saturation vapour pressure [SRC; ECMWF IFS Documentation Cy41r2, Part IV §7.2.1(b), Tetens over water;
identical to FWI_SPEC.md §3.2]:** e_s(X) = 611.21 · exp(17.502 · (X − 273.16)/(X − 32.19)) Pa, with X in K.

**G5 ERA5-Land variables [DESIGN]:**
- `t2m_anomaly`: mean DAILY_AGGR `temperature_2m` over 1 March – 31 May *y*, difference anomaly against
  the baseline (§0.3).
- `vpd_anomaly`: daily VPD = e_s(`temperature_2m`) − e_s(`dewpoint_temperature_2m`) from DAILY_AGGR,
  computed on the native 0.1° grid; mean over 1 March – 31 May *y*; difference anomaly against the
  baseline. TerraClimate `vpd` is **not used**.
- `soil_water_anomaly`: depth-weighted mean of `volumetric_soil_water_layer_1`, `_2`, `_3` with weights
  7, 21 and 72 (layer depths **0–7, 7–28 and 28–100 cm**, [SRC, verified on the EE catalogue page
  `ECMWF_ERA5_LAND_DAILY_AGGR`]); mean over **1 March – 31 May *y***; difference anomaly against the
  baseline.
- `fwi_dc` and `fwi_dmc` on 31 May *y*: computed per FWI_SPEC.md (below).
- Grid: nearest (§0.2), after computation on the native grid.
- The evaporation components are **not used**; EE and ECMWF document that three of them have swapped
  values (EE description, ECMWF "Known issues").

**FWI codes (Drought Code and Duff Moisture Code on 31 May) [binding: FWI_SPEC.md]:**
FWI_SPEC.md governs every detail of the FWI computation; the summary here does not override it.
- Implementation: xclim 0.62.0 `cffwis_indices` in its pinned environment, with published constant 147.2
  (FWI_SPEC.md §1–2).
- Observation hour, per **ERA5-Land pixel**: `h_UTC = floor(12.5 − lon/15)` (local mean solar noon rounded
  to the whole UTC hour; no civil time zones, no DST). Instantaneous T2m, Td2m, u10, v10 at `h_UTC`.
- RH = 100 · e_s(Td)/e_s(T), clipped to [0, 100]. Wind = 3.6 · √(u² + v²) km/h. Rain = 1000 · Σ
  `total_precipitation_hourly` over the 24 hourly images ending at `h_UTC` of day *d*, negatives clamped
  to 0.
- **Continuous computation from 2013-01-01** with start values **FFMC 85, DMC 6, DC 15**, run without
  interruption through 2024-12-31. No seasonal restarts, no shut-down, no overwintering, no dry start.
- Day-length factors: the standard Canadian tables (FWI_SPEC.md §3.5); latitude ≥ 30° N asserted.
- **Convergence check** (FWI_SPEC.md T6): a second run started on **2012-01-01**; on every 31 May
  2015–2024 and every cell, |ΔDC| ≤ 1.0, |ΔDMC| ≤ 0.1 and |ΔFFMC| ≤ 0.1. If any cell fails, the start is
  moved one year earlier and the check repeated, as FWI_SPEC.md T6 specifies; the final start date is
  reported.
- Tests T1–T7 of FWI_SPEC.md §4 must pass before any FWI number is used.
- Computed on the native 0.1° grid, then assigned by **nearest** ERA5-Land pixel centre.
- Snow flag `fwi_snow_flag` as in FWI_SPEC.md §3.7.

---

## 9. TerraClimate (`IDAHO_EPSCOR/TERRACLIMATE`): climatic water deficit (G5)

**Band [SRC, EE STAC]:** `def` (climatic water deficit), mm, **scale 0.1**. Grid 1/24° (~4.6 km N–S).
Monthly. `vpd` and `pdsi` are **not used**.

EE-CHK: the images run to 2024-12, and every 2023–2024 image has `status` = "permanent".

**Rule [DESIGN]:**
- `cwd_anomaly`: sum of `def` over June *y*−1 – May *y* (the 12 months to May), difference anomaly
  against the baseline (§0.3).
- Grid: nearest, with the 3 × 3 valid-neighbour fill at coasts (§0.2).

**Caveats [SRC, EE description and https://www.climatologylab.org/terraclimate.html]:**
- Temporal variability is inherited from CRU TS4 and JRA-55, so the product "will not capture temporal
  variability at finer scales than parent datasets".
- The water-balance model is "very simple".
- Trends are inherited from the parents.
- Citation: Abatzoglou et al. 2018, *Scientific Data*.

---

## 10. CHIRPS daily (`UCSB-CHG/CHIRPS/DAILY`): precipitation anomalies (G5)

**Band [SRC, EE STAC]:** `precipitation`, mm/day, float, no scale. Grid 0.05°, covering 50° S–50° N
(https://www.chc.ucsb.edu/data/chirps).

**Rule [DESIGN]:** CHIRPS is the precipitation source for the G5 anomalies; ERA5-Land precipitation is
used only inside the FWI codes.
- 3-, 6- and 12-month totals ending on 31 May *y*: Σ of the daily values.
- `precip_anomaly_3m`, `_6m`, `_12m` = the total minus the baseline mean of the same window, **as a
  difference in mm**. The percentage (ratio) form is not used.
- Grid: nearest (§0.2).

**Caveat [SRC, CHC page]:** satellite estimates "suffer from biases due to complex terrain" and
underestimate extremes. Mediterranean orography is exactly this case.

---

## 11. Copernicus GLO-30 (`COPERNICUS/DEM/GLO30_2024_1`): terrain (G1)

**Asset [EE-CHK]:** EE flags `COPERNICUS/DEM/GLO30` as deprecated, superseded by
**`COPERNICUS/DEM/GLO30_2024_1`** (26 475 tiles, bands DEM, EDM, FLM, HEM, WBM). The registered asset is
`COPERNICUS/DEM/GLO30_2024_1`.
- Band `DEM`: metres, float, no scale, on a 1″ grid.

**Product facts [SRC: Copernicus DEM Product Handbook v5.0, §1.1 and §1.2.1–1.2.3, Table 2,
https://dataspace.copernicus.eu/sites/default/files/media/files/2024-06/geo1988-copernicusdem-spe-002_producthandbook_i5.0.pdf]:**
- It is a **Digital Surface Model** that includes buildings and vegetation.
- Vertical datum EGM2008. Absolute vertical accuracy < 4 m (LE90).
- GLO-30 latitude spacing is 1″; longitude spacing varies by latitude band.
- EE temporal extent: TanDEM-X acquisitions from 2010-12 to 2015-01 (EE STAC). This **predates every
  season**, so post-fire canopy loss cannot leak into terrain.

**Computation [DESIGN; the EE catalogue notes that the collection needs a reprojection for slope]:**
1. Mosaic the tiles over the analysis tile buffered by at least the TPI radius (§0.1 neighbourhood
   rule), and mask `WBM` > 0 (ocean, lake, river).
2. `setDefaultProjection` to the native 1″ EPSG:4326 projection.
3. `ee.Terrain.slope` / `ee.Terrain.aspect` at 30 m.
4. Aggregate each 30 m quantity to 463 m by **area-weighted mean**:
   - elevation;
   - slope (degrees);
   - northness = cos(aspect)·sin(slope) and eastness = sin(aspect)·sin(slope) (PREREGISTRATION.md §5.2),
     averaged as components;
   - **TPI** = the cell's mean elevation minus the mean elevation of the 463 m cells within a **2 km
     radius**, using cells outside the tile.
5. Cells with > 50 % water pixels are left missing.

---

## 12. GHSL P2023A POP and BUILT_S (`JRC/GHSL/P2023A/GHS_POP`, `.../GHS_BUILT_S`), G6

**Bands [SRC, EE STAC]:**
- `population_count`: persons per 100 m cell.
- `built_surface`: m² per 100 m cell.
- Grid: World Mollweide at 100 m.
- EE-CHK: epochs 1975 … 2030 in 5-year steps.

**Epoch rule [DESIGN]:** E(*y*) = the latest epoch **≤ *y* − 1**. Projection epochs are never used.
| Season *y* | Epoch |
|---|---|
| 2015 | 2010 |
| 2016–2020 | 2015 |
| 2021–2024 | 2020 |

Epochs 2025 and 2030 are **projections** [SRC: GHSL Data Package 2023, §2.1 and the comparison table,
https://ghsl.jrc.ec.europa.eu/documents/GHSL_Data_Package_2023.pdf].

**Caveat [SRC, same report §2.1]:** built-up surface is observed only for the epochs 1975, 1990, 2000,
2014 and 2018. The 2010, 2015 and 2020 layers are spatio-temporally interpolated or extrapolated. GHS-POP
is disaggregated from GPWv4.11 census data (EE description). The variables are effectively near-static.

**Aggregation [DESIGN]:**
- built fraction = area-weighted Σ `built_surface` / cell area (214 659 m²);
- population density (persons/km²) = area-weighted Σ `population_count` / 0.214659 km²;
- both enter the model as log(1 + x).

---

## 13. GRIP4 roads (`projects/sat-io/open-datasets/GRIP4/Europe`, community catalogue), G6

**EE-CHK:**
- Properties: `GP_RTP` (road type), `GP_RSY` (source year, e.g. 1997), `GP_RRG`, `GP_REX`, `GP_RSE`,
  `GP_RSI`, `GP_RCY`, `gp_gripreg`.
- **Türkiye (Antalya, İzmir) is in the `Europe` table**; the `Middle-East-Central-Asia` table returned 0
  features there. So only the Europe table is used.

**Road types [SRC, GLOBIO download page, https://www.globio.info/download-grip-dataset]:** type 1
highways, 2 primary, 3 secondary, 4 tertiary, 5 local. Citation: Meijer et al. 2018, *Environ. Res.
Lett.* 13, 064006. Licence CC-BY 4.0 (https://gee-community-catalog.org/projects/grip/).

**Rule [DESIGN]:**
- `dist_road_m` = the geodesic distance from the 463 m cell centre to the nearest segment of **any type
  (1–5)** (EE `FeatureCollection.distance`, searchRadius 20 km, maxError 10 m).
- The collection is filtered to the tile buffered by 20 km, so roads outside the tile count.
- Distances are capped at 20 km.

**Limitation:** GRIP4 is static and assembled from national sources of different vintages (`GP_RSY`
differs by country). Road completeness is therefore partly a **country-source artefact aligned with
regions**, which matters for spatial transfer (Q3). This is stated as a limitation of the study.

---

## 14. VIIRS DNB annual V21 and V22 (`NOAA/VIIRS/DNB/ANNUAL_V21`, `ANNUAL_V22`), G6

**EE-CHK:**
- V21 holds 2013–2021 and V22 holds 2022–2025.
- Both have identical bands: `average`, `average_masked`, `cf_cvg`, `cvg`, `maximum`, `median`,
  `median_masked`, `minimum`.
- Grid 15″ (~464 m).

**Bands [SRC, EE STAC and descriptions]:**
- Radiance is in nW sr⁻¹ cm⁻², with no scale.
- Background is zeroed using a 3 × 3 data-range threshold, and high and low outliers (fires) are
  removed using the 12-month median.
- `cf_cvg` is the "total number of observations that went into each pixel … can be used to identify
  areas with low numbers of observations".
- EOG product page: https://eogdata.mines.edu/products/vnl/.

**Rule [DESIGN]:**
- For season *y*, use the annual composite of **year *y* − 1**. The year-*y* composite contains the
  season, and its fires or outages, so it is not used.
- *y* − 1 ≤ 2021 → V21; *y* − 1 ≥ 2022 → V22.
- Band `average_masked`, entered as log(1 + x), **level only** (no anomaly).
- `cf_cvg` = 0 → missing; the per-tile minimum of `cf_cvg` is reported.
- Aggregation: area-weighted mean.

**Caveat:** the version switch coincides exactly with the 2021/2022 year boundary, and EE holds no overlap
year, so a version effect is confounded with time. This is why only the level is used. A label-free
comparison of the tile distributions for 2021 versus 2022 is reported descriptively.

---

## 15. Canopy height: not used

ETH global canopy height 2020 (`users/nlang/ETH_GlobalCanopyHeight_2020_10m_v1`) is **removed from the
model**. It is built from May–September 2020 imagery, so for every season *y* ≤ 2020 burned cells appear
in their **post-fire** state, the same defect for which STUDY_DESIGN §3 rejected WorldCover 2021 as a
predictor. MOD44B *y*−1 (§5) carries tree cover.

---

## 16. VNP64A1 v002 (`NASA/VIIRS/002/VNP64A1`): label agreement (descriptive)

**Bands and QA [SRC, EE STAC]:** `Burn_Date`, `Burn_Date_Uncertainty`, `QA`, `First_Day`, `Last_Day`. The
QA layout is identical to MCD64A1 (§1). The EE page links the V1 guide
(https://lpdaac.usgs.gov/documents/1330/VNP64A1_User_Guide_V1.pdf).

**EE-CHK:** the grid is identical to MCD64A1 (463.3127 m, aligned origin). All 120 months of 2015–2024
are present.

**Rule:** exactly the MCD64A1 label rule of §1 with the renamed bands. Agreement with MCD64A1 is reported
per tile-season (burned cells in either, both, and the Dice coefficient). It is a descriptive check, not
a sensitivity analysis, and not an independent label (same algorithm family).

---

## 17. FireCCI 5.1 (`ESA/CCI/FireCCI/5_1`): reference label, 2015–2020 (sensitivity)

**Bands [SRC]:**
- `BurnDate`: DOY of first detection. In the files, −1 = not observed and −2 = not burnable; in EE the
  band is 1–366.
- `ConfidenceLevel`: probability of burned, 0–100.
- `ObservedFlag`: −1 not observed, −2 not burnable.
- `LandCover`.
- Grid 0.0022457331° (~250 m).
- Sources: Fire_cci PUG-MODIS v1.0 §2.4.1–2.4.2
  (https://climate.esa.int/media/documents/Fire_cci_D4.2.1_PUG-MODIS_v1.0_zOQQ88o.pdf) and the EE STAC.

**Rule [DESIGN]:**
1. For each 250 m pixel, burned in *y* = a BurnDate within the §0.3 season DOY range in any of the
   June–October *y* images. The product's own classification is used, with no ConfidenceLevel threshold,
   because the PUG defines CL as a probability attached to that classification.
2. Pixels with ObservedFlag −1 in any season month are "unobserved".
3. On the 463 m grid:
   - burned fraction = area-weighted mean of the pixel burned indicator;
   - unobserved fraction likewise.
4. **Majority label** = burned fraction ≥ 0.5; any-burn variant = fraction > 0.
5. Cells with an unobserved fraction > 0.5 are left missing.
6. Seasons 2015–2020 only (the product ends in 2020-12).

---

## 18. Active fire: MOD14A1/MYD14A1 (`MODIS/061/MOD14A1`, `MODIS/061/MYD14A1`), descriptive

EE's `FIRMS` is the LANCE near-real-time product, and "the data in the near-real-time dataset are not
considered to be of science quality" (EE FIRMS description). **`FIRMS` is not used.**

**Rule [DESIGN]:** the science-quality `MODIS/061/MOD14A1` and `MODIS/061/MYD14A1` `FireMask`.
- Classes [SRC: MODIS C6/C6.1 Active Fire User's Guide §5.1.1 Table 3 and §5.2.1,
  https://modis-fire.umd.edu/files/MODIS_C6_C6.1_Fire_User_Guide_1.0.pdf]: 3 water, 4 cloud,
  5 non-fire land, 6 unknown, 7 fire low, **8 fire nominal, 9 fire high**.
- Guide §8.4.2: users wanting fewer false alarms "may wish to consider only nominal- and high-confidence
  fire pixels".
- fire = FireMask ∈ {8, 9} on any day of the season, in either product.
- The grid is 1 km nested 2 × 2, so each cell uses its parent pixel.
- Metric: the share of MCD64A1-burned cells whose parent pixel had ≥ 1 fire in the season window.

---

## 19. Sensitivities (registered)

This is the complete list of product-level sensitivity analyses. Each is reported whatever it shows and is
not used to choose a primary result.

1. **MCD64A1 special-condition cells as missing:** unburned cells with QA bits 5–7 ≠ 0 in any season month
   get a missing label (§1, rule 6).
2. **FireCCI 5.1 labels, seasons 2015–2020** (§17): majority rule, with any-burn as its variant.
3. **EFFIS perimeter labels:** perimeters rasterised to the burned fraction of each 463 m cell; majority
   rule (fraction ≥ 0.5), with any-burn (fraction > 0) as its variant.
4. **MOD13A1 SummaryQA = 0 only** (§3).
5. **Pilot LST rule** (§7): QC_Day bits 0–1 = 00 and bits 2–3 = 00.
6. **G4 on 2015–2022:** every contrast involving G4 repeated on seasons 2015–2022 only (Terra drift, §7).
7. **TPI radius 10 km** (§11).
8. **GRIP4 road types 1–3 only** (§13).
9. **MCD12Q1 class 14 added** to the population (§2).
10. **WorldCover 2021 population** (static), as in PREREGISTRATION.md §12.
11. **FWI at 12:00 UTC** everywhere instead of `h_UTC` (FWI_SPEC.md §3.1).
12. **FWI start 2012-01-01**, as the convergence check of FWI_SPEC.md T6 (§8).
13. **Snow-affected cells excluded:** cells with `fwi_snow_flag` = 1 (FWI_SPEC.md §3.7).

---

## 20. Freezing

- Every Earth Engine asset ID used, together with its `system:version` and the image IDs used from it, is
  recorded in the export manifest at export time.
- The SHA-256 of every exported file is recorded in the same manifest at export time.
- After the outcome lock, no file is re-exported, except for a registered data failure (PREREGISTRATION.md
  §13), which is recorded before outcomes are computed.

---

## 21. Decisions (closed)

| ID | Topic | Final rule |
|---|---|---|
| D1 | Cell rule for labels | MCD64A1 is native per cell; no majority/any-burn rule for it. Majority (any-burn variant) applies to FireCCI 5.1 fractions and EFFIS perimeters only (§1, §17, §19). |
| D2 | G2 land-cover shares | Group shares over the 3 × 3 neighbourhood on the full MCD12Q1 *y*−1 grid, of land cells (water excluded), plus MOD44B tree and non-tree vegetation cover of *y*−1 (§2, §5). |
| D3 | MOD11A1 QC rule | Primary: produced and LST error ≤ 2 K, fixed at registration; retention counts reported only. Pilot rule is a sensitivity (§7, §19). |
| D4 | Terra orbit drift | Every G4 contrast repeated on 2015–2022; view time reported descriptively only (§7, §19). |
| D5 | FWI noon | `h_UTC = floor(12.5 − lon/15)` per ERA5-Land pixel; 12:00 UTC as sensitivity (§8, FWI_SPEC.md §3.1). |
| D6 | G7 fire history | Years since last burn to before 1 June *y*, capped at 14; distinct burn years 1 Jan *y*−10 to 31 May *y*; V2 recomputation with the target season unobserved (§0.4, §1). |
| D7 | Precipitation source | CHIRPS difference anomalies (mm) for 3/6/12 months to 31 May; ERA5-Land precipitation only inside FWI (§10). |
| D8 | DEM asset | `COPERNICUS/DEM/GLO30_2024_1` (§11). |
| D9 | Canopy height | Removed from the model (§15). |
| D10 | Active fire | MOD14A1/MYD14A1 FireMask 8–9; `FIRMS` not used (§18). |
| D11 | Windows, counts, radius | Surface window 1 March – 31 May *y*; baseline = five preceding years; minimum counts as in §0.3; TPI 2 km (10 km sensitivity); tile 1.0° (§0.1, §0.3, §11). |
| D12 | ERA5-Land soil layers | Layers 1–3 = 0–7, 7–28, 28–100 cm, verified on the EE catalogue page; depth-weighted, March–May mean anomaly (§8). |
