# FWI_SPEC — Canadian Fire Weather Index System from ERA5-Land

Binding specification for STUDY_DESIGN §4 (G5: Drought Code and Duff Moisture Code on 31 May;
G8: seasonal FWI, in-season explanatory arm only). Written 2026-09-19. Every number marked
**[verified]** was reproduced in a throwaway environment on that date; everything else is a
convention fixed here, with its reason.

## 1. Canonical definition and reference implementations

| Source | Role | URL (fetched 2026-09-19) | What was checked |
|---|---|---|---|
| Van Wagner, C.E. 1987. *Development and structure of the Canadian Forest Fire Weather Index System.* Can. For. Serv., For. Tech. Rep. 35 | Canonical definition of the system | https://cfs.nrcan.gc.ca/pubwarehouse/pdfs/19927.pdf (redirects to NRCan OSTR); Wayback copy truncated at 1 MB | Not read in full. Its equations are reproduced in the two reports below, which were read in full. |
| Van Wagner, C.E.; Pickett, T.L. 1985. *Equations and FORTRAN program for the Canadian Forest Fire Weather Index System.* For. Tech. Rep. 33 | Standard equations (1984 version), FORTRAN standard program F-32, **FWI test data 13 Apr – 31 May** | https://ostrnrcan-dostrncan.canada.ca/entities/publication/29706108-2891-4e5d-a59a-a77c96bc507c ; PDF via https://web.archive.org/web/2020id_/https://cfs.nrcan.gc.ca/pubwarehouse/pdfs/19973.pdf (sha256 64620cb7…e13b) | Equations 1–30. Table 1 (Le) and Table 2 (Lf). Restrictions (T floors −1.1/−2.8 °C, V ≥ 0, Pr/Dr ≥ 0). Start-up values 85/6/15. Constant 147.2. Sample input page (49 days). The sample-output page is a rotated scan that the text extractor cannot read, so the output values come from Wang et al. 2015 below. |
| Wang, Y.; Anderson, K.R.; Suddaby, R.M. 2015. *Updated source code for calculating fire danger indices in the Canadian Forest Fire Weather Index System.* Inf. Rep. NOR-X-424 | Updated code in FORTRAN 95, C, C++, Python, Java and SAS. **Table 7 = the VW&P 1985 test data with its outputs** | https://cfs.nrcan.gc.ca/publications?id=36461 ; https://publications.gc.ca/collections/collection_2016/rncan-nrcan/Fo133-1-424-eng.pdf (returned HTTP 502 on 2026-09-19); PDF via https://web.archive.org/web/2020id_/https://cfs.nrcan.gc.ca/pubwarehouse/pdfs/36461.pdf (sha256 2f0fdf37…e598) | Table 7 transcribed from the PDF's text layer into `fwi_reference_rows.csv`. The report says (p. 3) that the six new codes gave output "identical with those produced by the FORTRAN 77 source code". All six codes use 147.2. Its inputs match the VW&P 1985 sample-input page. |
| R package **cffdrs 1.9.2** (CRAN, 2025-08-21; GPL-2) | Reference implementation maintained by the Canadian Forest Service | https://cran.r-project.org/package=cffdrs ; https://cran.r-project.org/src/contrib/cffdrs_1.9.2.tar.gz (sha256 0152f98d…42d5); https://github.com/cffdrs/cffdrs_r | Read `R/fine_fuel_moisture_code.r`, `duff_moisture_code.r`, `drought_code.r`, `initial_spread_index.r`, `buildup_index.r`, `fire_weather_index.r`, `fwi.r`, `data/test_fwi.csv`, `tests/testthat/data/fwi_01.csv` and `NEWS.md`. |
| Python **xclim** `xclim.indices.fire` (`_cffwis.py`) | Candidate Python implementation | https://pypi.org/project/xclim/0.62.0/ ; https://github.com/Ouranosinc/xclim ; https://xclim.readthedocs.io/ | Installed and executed (see §5). Source read: day-length tables, FFMC, DMC, DC, ISI, BUI, FWI, and the always-on/start-up logic in `_fire_weather_calc`. |

**Two findings about cffdrs.** Both are reasons not to use the cffdrs test files as the reference.

1. **FFMC constant.** cffdrs 1.9.2 changed the FFMC moisture constant from the published 147.2 to
   the exact value 250·59.5/101 = 147.27723 (`NEWS.md`: "Calculating exact FFMC coefficient rather
   than hard coding"). Van Wagner & Pickett (1985) Eq. 1/10 and all six codes in Wang et al. (2015)
   use 147.2. **[verified]** With 147.27723 the published Table 7 is reproduced at one decimal for
   only 22/49 FFMC, 28/49 ISI and 18/49 FWI values. The largest errors are 0.13 (FFMC), 0.23 (ISI) and
   0.29 (FWI). DMC, DC and BUI are unaffected.
2. **Test data.** cffdrs's `data/test_fwi.csv` has 48 rows, ending on 30 May, and gives 11.0 °C for
   10 May where VW&P (1985) and Wang et al. (2015) give 11.5 °C. Its expected outputs
   (`tests/testthat/data/fwi_01.csv`) are regression values from cffdrs itself, not published
   values. **[verified]** An independent pure-Python port of cffdrs 1.9.2 reproduces `fwi_01.csv`
   at 4 significant digits on 48/48 rows for FFMC, DMC, ISI, BUI and FWI. DC agrees within
   rounding (|d| ≤ 0.005).

The reference for this study is therefore the **published** table: Wang et al. 2015 Table 7, which
is the VW&P 1985 test data.

## 2. Recommended implementation

**xclim 0.62.0, `xclim.indices.fire.cffwis_indices`**, in its own pinned environment. Do not
install it into `.venv-step10`.

Pinned set, as tested on Windows 11 with CPython 3.12.10: `xclim==0.62.0 numba==0.67.0
llvmlite==0.49.0 numpy==2.5.3 xarray==2026.7.0 pandas==3.0.6 scipy==1.18.1 dask==2026.8.0
Pint==0.26.1 cf_xarray==0.11.3 boltons==26.2.0 Bottleneck==1.6.0 cftime==1.6.5 pyarrow==25.0.1`.
On Windows, set `NUMBA_CACHE_DIR` to a short path: with a long site-packages path, numba's cache
write fails with `FileNotFoundError` at import.

Why xclim:
- It uses the published constants and equations (147.2; VW&P Eqs. 1–30).
- **[verified]** It reproduces all 294 published values: 49 rows × FFMC, DMC, DC, ISI, BUI and FWI
  each equal Table 7 after rounding to one decimal (§5).
- **[verified]** It is bit-identical, to within 3e-14, with an independent line-by-line port of the
  equations using 147.2. This is a second implementation that agrees with the first.
- It is vectorised with numba over xarray grids, which suits 11 km ERA5-Land grids over ten years.

The DMC rain branch has a GFWED alternative that is commented out in the source. The active branch
is the cffdrs form, `wmi = 20 + 280/exp(0.023·P0)` and `43.43·(5.6348 − ln(wmr − 20))`.

Canonical call, with nothing else set:
```python
dc, dmc, ffmc, isi, bui, fwi = xclim.indices.fire.cffwis_indices(
    tas=T_noon_degC, pr=P24_mm, sfcWind=W_noon_kmh, hurs=RH_noon_pct, lat=lat_deg_north,
    season_method=None, overwintering=False, dry_start=None,
    ffmc_start=85, dmc_start=6, dc_start=15)
```
Units attributes must be `degC`, `mm/d`, `km/h`, `%` and `degrees_north`. Time must be one chunk,
because the recursion runs along time. DSR, if wanted, is `0.0272·FWI^1.77`.

## 3. Conventions (all binding)

**3.1 Observation time: noon local standard time, by longitude.** The FWI system expects weather at
12:00 local standard time (VW&P 1985). Use local *mean solar* noon, rounded to the whole UTC hour,
at each ERA5-Land pixel centre:

  `h_UTC = floor(12.5 − lon/15)` → 13 UTC for lon ≤ −7.5 (western Portugal), 12 UTC for
  −7.5 < lon ≤ 7.5, 11 UTC for 7.5 < lon ≤ 22.5, 10 UTC for 22.5 < lon ≤ 37.5, 9 UTC for 37.5 < lon ≤ 52.5
  (eastern Türkiye).

Legal time zones and DST are deliberately not used. Spain keeps CET while its solar time is close
to UTC, and Türkiye has been on UTC+3 year-round since 2016, so civil "noon" would shift the
observation hour arbitrarily by country. The rule depends only on longitude and has no seasonal
jump. T2m, Td2m, u10 and v10 are the **instantaneous** ERA5-Land values in the image whose
`system:time_start` equals day *d* at `h_UTC`. Sensitivity run: a fixed 12 UTC everywhere.

**3.2 Relative humidity from T2m and Td2m.** Use saturation vapour pressure over water,
Buck (1981), in the form used by the ECMWF IFS:
`e_s(T) = 611.21 · exp(17.502 · (T − 273.16)/(T − 32.19))` with T in K, and
`RH = 100 · e_s(Td)/e_s(T)`, **clipped to [0, 100]**. This equals
`xclim.indices.relative_humidity(tas, tdps, method="buck81", ice_thresh=None, invalid_values="clip")`
**[verified]** to 4 decimals on 7 test cases. Over-water saturation is used at all temperatures.
The clip is mandatory. **[verified]** xclim does not clamp: with RH = 100.5, FFMC, ISI and FWI
become NaN, and because FFMC is recursive the NaN would propagate for the rest of the series.

**3.3 Wind.** `W = 3.6 · sqrt(u10² + v10²)` in km/h, from the instantaneous 10 m components at
`h_UTC`. No gust, height or terrain correction is applied. ERA5-Land wind is a grid-box mean and is
expected to be biased low in complex terrain; this is recorded as a limitation, not corrected.

**3.4 Precipitation: 24 h ending at the observation hour.** `P24(d) = 1000 · Σ total_precipitation_hourly`
over the 24 images with `system:time_start` in {d−1 at h_UTC+1 h, …, d at h_UTC}. Negative values
are clipped to 0. Units are m → mm. Total precipitation (rain plus snow water equivalent, as it
falls) is the FWI rain input.

**[verified]** in Earth Engine on 2026-09-19 at (−8.0, 41.5) for 1–3 Nov 2019: an image stamped *t*
holds the accumulation over (t − 1 h, t] (ECMWF convention). The `total_precipitation` image at
00 UTC holds the full previous UTC day, and `total_precipitation_hourly` equals the difference of
consecutive accumulations.

`ECMWF/ERA5_LAND/DAILY_AGGR` `total_precipitation_sum` for day D equals the sum of hourly images
stamped D 00:00…D 23:00, that is (D−1 23:00, D 23:00]. **[verified]** 0.045267 m both ways. It is
therefore not a noon-ending window and **must not be used for FWI**.

**3.5 Day-length factors.** Use the latitude of the pixel centre. The whole study area lies at
≥ 30° N; assert this in code. Both xclim and cffdrs then use the original Canadian tables of
VW&P 1985. These tables are exact duplicates of the ones exercised by the reference test.
- DMC Le (Jan–Dec): 6.5, 7.5, 9.0, 12.8, 13.9, 13.9, 12.4, 10.9, 9.4, 8.0, 7.0, 6.0.
  xclim applies it for 30 ≤ lat ≤ 90; cffdrs for lat > 30.
- DC Lf (Jan–Dec): −1.6, −1.6, −1.6, 0.9, 3.8, 5.8, 6.4, 5.0, 2.4, 0.4, −1.6, −1.6.
  xclim applies it for lat ≥ 15; cffdrs for lat > 20.

No latitude-specific table exists between 30° and 46° N. The 46° N table slightly overstates summer
drying at 36–42° N, which is recorded as a limitation. The 20–30° N variants (xclim `DAY_LENGTHS[3]`,
cffdrs `ell02`) are **not** used.

**3.6 Start-up and overwintering.**
- Compute continuously, every day of the year ("always-on": `season_method=None`, no shut-down,
  no overwintering, no dry start).
- Start once, on **2013-01-01**, with FFMC 85, DMC 6 and DC 15.
- Run without interruption through 2024-12-31.

This gives two full winters of spin-up before the first predictor date (2015-05-31). The Canadian
season start/shut-down and overwintering rules were built for boreal climates, where snowpack
stops computation. In most of the Mediterranean, winter rain, not snow, resets the DC. Continuous
computation lets that rain do so. It also avoids a start date that would itself be a tunable choice.

**3.7 Snow and frozen periods.** No shut-down. The temperature floors of the equations handle
frozen days: DMC uses T = −1.1 °C, so no drying; DC uses T = −2.8 °C, and V ≥ 0 gives no drying in
January–March. Snowfall enters P24 as water equivalent on the day it falls. That is an
approximation, because melt is actually delayed.

Flag: `fwi_snow_flag = 1` for cells where ERA5-Land `snow_depth` > 0.01 m at `h_UTC` on any day
from 1 to 31 May of year *y*. Primary results are reported with and without the flagged cells.

**3.8 Outputs used by the study.**
- **G5.** DC and DMC for **31 May of year y**, computed from weather up to and including the noon
  observation of 31 May. A label window that starts on or after 1 June is therefore disjoint from
  the predictor.
- **G8.** The daily FWI series. The seasonal aggregation (for example mean, or days above a
  threshold) is fixed in STUDY_DESIGN at registration, not here.

Values are computed on the 11 km ERA5-Land grid and then assigned to 500 m cells by nearest ERA5-Land
pixel centre. The codes are nonlinear, so interpolate the **outputs**, never the inputs, and do it
the same way everywhere. Missing inputs are not allowed: land pixels only. A NaN input propagates
through the recursion, so it is a hard failure, not something to fill.

## 4. Test plan (must pass before any FWI number is used)

| ID | Test | Data | Pass criterion |
|---|---|---|---|
| T1 | Published reference | `design/fwi_reference_rows.csv` columns `ffmc…fwi` (49 rows, 13 Apr – 31 May 1985; Wang et al. 2015 Table 7 = VW&P 1985 test data). Start 85/6/15, lat 40 and 46, always-on, inputs taken as noon values directly | For all 294 values, the output rounded to 1 decimal equals the printed value, **and** \|output − printed\| ≤ 0.051 (half a printed unit, plus 0.001 for the FORTRAN single-precision carry-over) |
| T2 | Pin regression | Same CSV, columns `xclim0620_*` (xclim 0.62.0 output, 4 dp) | \|d\| ≤ 1e-4 on all 294 values. A failure means the pinned stack changed. |
| T3 | Adapters | Hand values: RH(T=20, Td=10 °C) = 52.5198; RH(30, 5) = 20.5553; RH(35, −5) = 7.4964; RH(10, 9.5) = 96.7008; RH(15, 15) = 100; RH(25, 26) = 100 (clipped). Wind (u, v) = (3, 4) m/s → 18.0 km/h. `h_UTC` at lon −9.0 / −7.5 / −7.4 / 0 / 7.5 / 7.6 / 23 / 44 → 13 / 13 / 12 / 12 / 12 / 11 / 10 / 9 | Exact to 1e-4 |
| T4 | Precipitation window | EE, pixel at (−8.0, 41.5), `h_UTC` = 13: P24 for 2019-11-02 = **30.904 mm** (the 12 UTC window would give 33.196 mm). The sum of hourly values stamped 2019-11-01 00…23 UTC = DAILY_AGGR 2019-11-01 = 45.267 mm | \|d\| ≤ 0.01 mm |
| T5 | Edge cases | Inputs with RH > 100 before the clip, T < −2.8 °C, P24 = 0 for 60 days, DMC = DC = 0 | No NaN after the clip; BUI = 0 when DMC = DC = 0; codes ≥ 0 |
| T6 | Spin-up convergence | Full grid; a second run started 2012-01-01 | On every 31 May 2015–2024 and every cell: \|ΔDC\| ≤ 1.0, \|ΔDMC\| ≤ 0.1, \|ΔFFMC\| ≤ 0.1. If any cell fails, move the start one year earlier and repeat; report the final start date. |
| T7 | Latitude domain | Grid | `min(lat) ≥ 30`, so §3.5 holds |

## 5. Status of the demonstration (2026-09-19)

Environment: throwaway venv in the session scratchpad; CPython 3.12.10; the pins in §2 (xclim 0.62.0).

- **T1 passed.** 294/294 values match the published Table 7 after rounding.
  - Largest deviations: FFMC 0.0494 (row 29), DMC 0.0498 (row 44), DC 0.0499 (row 43),
    ISI 0.0500 (row 12), BUI 0.0496 (row 29), FWI 0.0498 (row 46).
  - The result is identical at lat 40 and lat 46.
- **Independent check passed.** A line-by-line port with 147.2 agrees with xclim to 3e-14.
- **Discrimination check.** The same port with cffdrs 1.9.2's constant 147.27723 fails T1 (§1).
  T1 can therefore tell the two conventions apart.
- **T3 RH values passed**, and the T4 values were derived, from Earth Engine on 2026-09-19. The other
  T3 values, T4 as an automated test, and T5–T7 belong to the production pipeline; they are
  specified here and have not yet been run.
