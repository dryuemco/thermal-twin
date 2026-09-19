# Data availability in Google Earth Engine — verified live

Verified 2026-09-19 by live read-only queries (`ee.Initialize(project="thermaltwin")`):
`ee.data.getAsset` / `listAssets`, `size()`, `aggregate_min/max('system:time_start')`,
`first().bandNames()`, `first().select(0).projection().nominalScale()`. Dates are the
`system:time_start` of the first/last image present today (for monthly products the last date is
the first day of the last month). Scale is the nominal scale of band 0 in metres. Items marked
(web) come from catalogue pages, not from a live query.

## 1. Burned area

| Asset ID (works) | First – last image | Key bands | Scale | Cadence | Caveats |
|---|---|---|---|---|---|
| `MODIS/061/MCD64A1` | 2000-11-01 – 2026-07-01 (309 imgs) | BurnDate, Uncertainty, QA, FirstDay, LastDay | 463 m | monthly | Current label source. Covers 2015–2024 fully. |
| `ESA/CCI/FireCCI/5_1` | 2001-01-01 – **2020-12-01** (240 imgs) | BurnDate, ConfidenceLevel, LandCover, ObservedFlag | 250 m | monthly | **Ends Dec 2020.** `ESA/CCI/FireCCI/5_2` does not exist; the FireCCI folder holds only 5_1. |
| `NASA/VIIRS/002/VNP64A1` | 2012-03-01 – 2026-07-01 (173 imgs) | Burn_Date, Burn_Date_Uncertainty, QA, First_Day, Last_Day | 463 m | monthly | VIIRS burned area, same algorithm family as MCD64A1 (not independent of it). Covers 2015–2024. 173 images across ~14.3 years implies some months are missing; check gaps before use. |
| `JRC/GWIS/GlobFire/v2/FinalPerimeters` (table) | IDate 2000-03-04 – **2021-12-15** (23.3 M features) | IDate, FDate, Id | vector | per event | Derived from MCD64A1 (not independent). `.../DailyPerimeters/<year>` tables exist for 2000–2021. **Ends 2021.** |

## 2. Active fire

| Asset ID | First – last | Key bands | Scale | Cadence | Caveats |
|---|---|---|---|---|---|
| `FIRMS` | 2000-11-01 – 2026-09-17 (9415 imgs) | T21, confidence, line_number | 927 m (rasterised) | daily | MODIS-only rasterisation at 1 km; no VIIRS 375 m layer. |
| `MODIS/061/MOD14A1` | 2000-02-24 – 2026-09-13 | FireMask, MaxFRP, sample, QA | 927 m | daily | |
| `MODIS/061/MYD14A1` | 2002-07-04 – 2026-09-13 | same | 927 m | daily | |
| `NASA/VIIRS/002/VNP14A1` | 2012-01-19 – 2026-09-14 | FireMask, MaxFRP, QA, sample | 927 m | daily | Gridded at 1 km, **not 375 m**. `NOAA/VIIRS/001/VNP14A1` is deprecated (ends 2024-06-16). No 375 m VIIRS active-fire point product was found in the public catalogue. |

## 3. Weather / climate

| Asset ID | First – last | Relevant bands | Scale | Cadence | Caveats |
|---|---|---|---|---|---|
| `ECMWF/ERA5_LAND/DAILY_AGGR` | 1950-01-02 – 2026-09-11 | temperature_2m(_min/_max), dewpoint_temperature_2m(_min/_max), u/v_component_of_wind_10m(_min/_max), total_precipitation_sum, volumetric_soil_water_layer_1..4, total_evaporation_sum, potential_evaporation_sum | 11.1 km | daily | Complete for 2015–2024. No wind gust or relative-humidity band; compute RH from T and Td. |
| `ECMWF/ERA5_LAND/HOURLY` | 1950-01-01 – 2026-09-13 (672k imgs) | same variables (hourly, plus `*_hourly` de-accumulated precip/evap) | 11.1 km | hourly | Needed for noon-local FWI inputs. |
| `ECMWF/ERA5_LAND/MONTHLY_AGGR`, `ECMWF/ERA5_LAND/STATIC` | — | monthly aggregates; static high/low vegetation type/cover | 11.1 km | monthly / static | |
| `ECMWF/ERA5/HOURLY` | 1943-03-31 – 2026-09-13 | + instantaneous_10m_wind_gust, 100 m wind | 27.8 km | hourly | |
| `ECMWF/ERA5/DAILY` | 1979-01-02 – **2020-07-09** | mean/min/max_2m_air_temperature, dewpoint, total_precipitation, u/v wind | 27.8 km | daily | **Ended mid-2020; do not use.** (`ECMWF/ERA5/DAILY_AGGR_RAW` is empty.) |
| `projects/climate-engine-pro/assets/ce-merra2_fwi-daily` (GFWED, community) | 1980-04-01 – 2026-04-30 | FWI (only) | ~62 km (0.5°×0.625°) | daily | **The only FWI found in EE.** Only the final FWI band is present; there are no FFMC/DMC/DC/ISI/BUI bands. It is coarse and trails real time by about 5 months. Licence: NASA open data. No Copernicus CEMS/GEFF FWI exists in EE. |
| `IDAHO_EPSCOR/TERRACLIMATE` | 1958-01-01 – **2024-12-01** | vpd, pdsi, def (CWD), aet, pet, soil, pr, tmmx, tmmn, vs | 4.6 km | monthly | Ends exactly at 2024; covers the whole window. |
| `UCSB-CHG/CHIRPS/DAILY` | 1981-01-01 – 2026-08-31 | precipitation | 5.6 km | daily | Covers 50°S–50°N, so the whole study area (≤ 45°N) is inside. The land-only quality over Mediterranean terrain is modest. `UCSB-CHC/CHIRPS/V3/DAILY_SAT` also exists (1998–2026). |

## 4. Vegetation / fuel state

| Asset ID | First – last | Key bands | Scale | Cadence | Caveats |
|---|---|---|---|---|---|
| `MODIS/061/MOD13A1` | 2000-02-18 – 2026-08-29 | NDVI, EVI, SummaryQA, DetailedQA, sur_refl_b01/02/03/07 | 463 m | 16-day | Native 500 m grid. |
| `MODIS/061/MOD13Q1` | 2000-02-18 – 2026-08-13 | same | 232 m | 16-day | |
| `NASA/VIIRS/002/VNP13A1` | 2012-01-17 – 2026-08-21 | NDVI, EVI, EVI2, SWIR1-3, pixel_reliability | 463 m | 16-day | VIIRS continuity if MODIS Terra degrades. |
| `MODIS/061/MOD15A2H` | 2000-02-18 – 2026-09-06 | Lai_500m, Fpar_500m, FparLai_QC | 463 m | 8-day | |
| `MODIS/061/MOD16A2GF` | 2000-01-01 – **2025-12-27** | ET, PET, LE, PLE, ET_QC | 463 m | 8-day | Gap-filled annual release that lags by about a year. Covers 2015–2024. |
| `MODIS/061/MOD16A2` | **2021-01-01** – 2026-08-29 | same | 463 m | 8-day | **In EE, this v061 collection only starts in 2021.** Use GF for 2015–2020. |
| `MODIS/061/MOD44B` | 2000-03-05 – 2025-03-06 (annual) | Percent_Tree_Cover, Percent_NonTree_Vegetation, Percent_NonVegetated | 232 m | annual | Annual fuel-fraction proxy. |
| `LANDSAT/LC08/C02/T1_L2` | 2013-03-18 – 2026-09-12 | SR_B1–B7, ST_B10, QA_PIXEL | 30 m | 16-day | |
| `LANDSAT/LC09/C02/T1_L2` | 2021-10-31 – 2026-09-16 | same | 30 m | 16-day | |
| `COPERNICUS/S2_SR_HARMONIZED` | first image over the Mediterranean 2015-07-04; latest 2026-09-18 | B1–B12, SCL, MSK_CLDPRB, QA60 | 10–60 m | ~5-day | L2A coverage in 2015–2016 is sparse (Level-2A was processed systematically only from ~2017 onward), so S2 SR is unreliable for the 2015–2016 seasons. |
| Live fuel moisture | — | — | — | — | **No LFMC product in the public EE catalogue.** The only route is a proxy: NDII/NDWI from MODIS (for example `MODIS/061/MCD43A4_NDWI`), or an external product that has to be uploaded. |

## 5. Thermal

| Asset ID | First – last | Key bands | Scale | Cadence |
|---|---|---|---|---|
| `MODIS/061/MOD11A1` | 2000-02-24 – 2026-09-15 | LST_Day_1km, LST_Night_1km, QC_Day, QC_Night, Emis_31/32 | 927 m | daily |
| `MODIS/061/MYD11A1` | 2002-07-04 – 2026-09-14 | same | 927 m | daily |
| `MODIS/061/MOD11A2` | 2000-02-18 – 2026-09-06 | same (8-day, Clear_sky_days/nights) | 927 m | 8-day |
| `MODIS/061/MOD21A1D` / `NASA/VIIRS/002/VNP21A1D` | 2000 / 2012 – 2026-09 | LST_1KM, QC, emissivities | 927 m | daily |

Caveat: LST is 1 km, so a 500 m design has to resample or downscale it (as in the existing Step 5).

## 6. Land cover / fuel type / canopy

| Asset ID | Years available | Key bands | Scale | Caveats |
|---|---|---|---|---|
| `ESA/WorldCover/v100` | **2020 only** | Map | 10 m | |
| `ESA/WorldCover/v200` | **2021 only** | Map | 10 m | Two years only, and v100/v200 use different algorithms, so they are not a change series. |
| `COPERNICUS/Landcover/100m/Proba-V-C3/Global` | **2015–2019** | discrete_classification, tree/shrub/grass/crops/…-coverfraction, forest_type | 100 m | Ends 2019. |
| `MODIS/061/MCD12Q1` | **2001–2024** (annual) | LC_Type1..5, LC_Prop1..3, QC | 463 m | The only annual land cover that spans 2015–2024. |
| `COPERNICUS/CORINE/V20/100m/<year>` | 1990, 2000, 2006, 2012, **2018** | landcover | 100 m | Images, not a collection. The 2018 layer is the latest in EE (no CLC 2024/CLC+). Covers PT/ES/IT/GR/TR. |
| `users/nlang/ETH_GlobalCanopyHeight_2020_10m_v1` (+`...HeightSD...`) | 2020 (May–Sep) | b1 | 10 m | Single epoch. CC-BY 4.0. |
| `projects/meta-forest-monitoring-okw37/assets/CanopyHeight` | ~2018–2020 imagery | cover_code | 1.2 m | Tiled collection (170 tiles). Very heavy to aggregate to 500 m. |
| `UMD/hansen/global_forest_change_2025_v1_13` | latest (versions 2013 … 2025_v1_13 exist) | treecover2000, loss, lossyear, gain, datamask | 30 m | Tree cover is only for the year 2000. The per-year `lossyear` is the usable dynamic layer. The asset endTime metadata reads 2022-12-31; check the `lossyear` maximum before relying on 2023–2025. |

## 7. Terrain

| Asset ID | Bands | Scale | Caveats |
|---|---|---|---|
| `COPERNICUS/DEM/GLO30` | DEM, EDM, FLM, HEM, WBM | 30 m | Tiled collection (26,076 tiles); mosaic it first. A newer `COPERNICUS/DEM/GLO30_2024_1` and `GLO30_MOSAIC` also exist. |
| `NASA/NASADEM_HGT/001` | elevation, num, swb | 30 m | Single image. |

## 8. Human drivers

| Asset ID | Epochs / coverage | Key bands | Scale | Caveats |
|---|---|---|---|---|
| `JRC/GHSL/P2023A/GHS_POP` | 1975–2030 every 5 yr (2015, 2020, 2025 relevant) | population_count | 100 m | 2025/2030 are projections. Also available: GHS_BUILT_V/H/C, GHS_SMOD. |
| `JRC/GHSL/P2023A/GHS_BUILT_S` | same epochs | built_surface, built_surface_nres | 100 m | Good WUI proxy (distance to built-up). |
| `CIESIN/GPWv411/GPW_Population_Density` | 2000, 2005, 2010, 2015, 2020 | population_density | 927 m | Ends 2020. |
| `WorldPop/GP/100m/pop` | **2000–2020** annual (PRT/ESP/ITA/GRC/TUR present) | population | 93 m | **Ends 2020.** |
| `NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG` | 2014-01 – 2026-07 (151 imgs) | avg_rad, cf_cvg | 464 m | Stray-light corrected. Summer months at high latitude are sparse; not an issue at ≤ 45°N. |
| `NOAA/VIIRS/DNB/ANNUAL_V21` / `ANNUAL_V22` | 2013–2021 / 2022–2025 | average, median, average_masked, cvg | 464 m | Two versions must be stitched to cover 2015–2024. |
| `projects/sat-io/open-datasets/GRIP4/Europe` (community) | ~2018 reference, static (8.79 M segments) | GP_RTP (road type), … | vector | Accessible. CC-BY 4.0. Static, so it cannot vary by year. Türkiye may fall in the Europe or the Middle-East-Central-Asia table (check). |
| `CSP/HM/GlobalHumanModification` | **2016 only** | gHM | 1 km | |
| `projects/sat-io/open-datasets/GHM/HM_1990_2020_OVERALL_300M` / `HM_2022_300M` | 1990–2020 every 5 yr; 2022 | constant | 300 m | Community (Theobald et al. 2024 update). |

## 9. Administrative / ecoregion frames

| Asset ID | Size | Key properties | Caveats |
|---|---|---|---|
| `RESOLVE/ECOREGIONS/2017` | 848 features | ECO_NAME, ECO_ID, BIOME_NAME, BIOME_NUM, REALM | Mediterranean Forests biome is available for rule-based framing. |
| `FAO/GAUL/2015/level2` (also level0/1, `FAO/GAUL_SIMPLIFIED_500m/2015/*`) | 38,258 features | ADM0/1/2_NAME, *_CODE | 2015 boundaries. |
| NUTS (Eurostat) | **not found** in the public catalogue or the community catalogue | — | — | It would have to be uploaded as a user asset. GAUL level1/2 is the in-EE substitute, and NUTS would not cover Türkiye consistently anyway. |

## Consequences for a 2015–2024 multi-year design

1. **Burned-area labels:** MCD64A1 is the only 500 m product that is independent enough, complete for 2015–2024, and still current. FireCCI51 ends in 2020 and there is no FireCCI 5.2 in EE, so a second-product label check can only cover 2015–2020. VNP64A1 (2012–2026) and GlobFire (to 2021, built from MCD64A1) are not independent of MCD64A1, so they serve as robustness checks, not independent validation.
2. **No usable FWI:** the only FWI in EE is GFWED/MERRA-2, which carries the final FWI at about 62 km and none of its components. Either compute FWI components (FFMC/DMC/DC/ISI/BUI) from ERA5-Land hourly (noon-local T, Td→RH, 10 m wind, 24 h precip; 11 km, complete to 2026) or use TerraClimate VPD/CWD/PDSI monthly (4.6 km, ends 2024-12, which fits exactly). Do not use ERA5/DAILY (ends 2020-07).
3. **Static land cover:** the only annual land cover over 2015–2024 is MODIS MCD12Q1 (500 m, to 2024). WorldCover (2020/2021), CGLS-LC100 (2015–2019) and CORINE (2018) are single or partial epochs, so a pre-fire land-cover layer must either be MCD12Q1-of-the-year or a single static map, with that stated as a limitation.
4. **Human drivers are mostly static or 5-yearly:** WorldPop and GPW end in 2020. GHSL gives 2015/2020/2025 epochs, and GRIP4 and gHM are single epochs. Only VIIRS night lights is annual or monthly across the window, and it needs a V21/V22 stitch.
5. **Fuel moisture has no direct product:** use MODIS NDII/NDWI, LAI/FPAR, MOD16A2**GF** ET/PET (the non-GF MOD16A2 v061 starts only in 2021 in EE), and ERA5-Land soil water as proxies.
6. **Sentinel-2 is unreliable for the 2015–2016 seasons;** the MODIS/VIIRS 500 m stack (MOD13A1, MOD15A2H, MOD11A1) is uniform over the whole window. Landsat 9 starts in late 2021, so Landsat 8 alone gives uniform coverage.
7. The native resolutions differ (LST 1 km, ERA5-Land 11 km, TerraClimate 4.6 km, CHIRPS 5.6 km). At 500 m, many adjacent cells therefore share identical meteorology, which strengthens the case for spatial-block CV with blocks larger than the coarsest predictor.
