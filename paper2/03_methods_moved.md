# Paper 2: sections carried whole from Paper 1

Moved 2026-08-14 in the split. Verbatim; rewritten in place once Paper 2's own
structure is settled. Each retains its original heading so its provenance is
obvious.


---

<!-- from paper/03_methods.md -->

## 3.17 Regional meteorological context (explanatory)

To characterise the meteorological conditions each region actually experienced, and specifically to
test the post hoc explanation that Manavgat's outlying transfer behaviour reflects meteorological
extremity (Section 5.7), an AOI-level ERA5-Land diagnostic was run outside the modelling pipeline
(`src/era5_land_regional_diagnostic.py`, with runner and validator in `scripts/`; outputs in
`drive_new/diagnostics/era5_land_regional/<analysis_id>/`). It is explanatory only: it produces a
table and exports no raster, and its outputs enter no feature set, no model and no transfer arm. The
module records this status in its own output (`is_model_predictor: false`). The candidate diagnostic
set of Section 3.14 was fixed before any diagnostic-versus-transfer correlation was computed, on the
provenance set out in Section 3.14.1, and no meteorological measure is added to it. The reasoning is
given in Section 5.7.

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
declared (A09, A10). The registry region keys and window dates agree with `core/regions.py` (A14).
The namespace contains only the four expected files, with no exported raster leaking into it (A24). The run was performed by the authors on 2026-08-11 under Python 3.12.3 with `earthengine-api`
1.7.39 installed solely to satisfy the module import chain. The validator opens no Earth Engine
session and requires no credentials. The repository was at commit `48b56e7` and the outputs staged
in a scratch namespace outside the repository via `--output-root`.

The manifest names commit `a07ea33`, at which neither the diagnostic source nor the Montiferru
registry entry yet exists. Both were first committed in `48b56e7`. The production run was therefore
made from a working tree carrying uncommitted changes, and the recorded commit identifies only the
last commit at run time. The code that actually ran can nevertheless be identified. The output
contains Montiferru with its registry windows, which `a07ea33` cannot supply. `core/regions.py`
gains that entry only in `48b56e7`, and it does so by pure addition (529 lines inserted, none
deleted), leaving the four regions common to both commits byte-identical.
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



---

<!-- from paper/03_methods.md -->

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


---

<!-- from paper/03_methods.md -->

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


---

<!-- from paper/03_methods.md -->

### 3.16.3 Predictor-window closure

A predictor-timing sensitivity, described here as documented in each region's frozen comparison
report
(`drive_new/diagnostics/window_closure_region/<region>/<hash>/_production/<region>/compare/report/window_closure_comparison.md`
for Bejís, Muğla, Evia-extended and Montiferru;
`drive_new/diagnostics/window_closure_sensitivity/manavgat_2021/compare/report/window_closure_comparison.md`
for Manavgat). Three variants are compared: canonical, closure 7 days earlier, and closure 14 days
earlier. The shifted variants move **both** ends of the predictor window together, so the window
length is preserved. The label window is frozen and identical in every variant. One exact common
cohort (the intersection of analysis-eligible, primary-population, valid rows of every variant,
after removing shared pre-label-censored cells) and one shared spatial-fold assignment are used by
all six evaluations (two model families × three variants), with model family, feature registry,
preprocessing, hyper-parameters and seeds held fixed. Uncertainty is a paired spatial-block
bootstrap on the model stage's own replicate draws with identical block draws across variants (1,000
replicates, seed 42, resampling unit `spatial_block_id`). The report states the analysis measures
the closure date jointly with its interaction with the fixed MODIS seasonal production policy, not
the closure date in isolation. Bejís, for scale: 12,814 cohort rows, 967 positives, 5 folds, 3,641
blocks. The shared folds are blocked at the pipeline's default 2-cell edge (≈ 1 km): the analysis
assigns block identifiers with `add_spatial_block_id(cohort, spatial_block_size_cells)` and takes
that value from `STEP8B_SPATIAL_BLOCK_SIZE_CELLS = 2`
(`repo/src/window_closure_sensitivity.py:8562`, `repo/core/config.py:556`). The comparison report
records fold and block counts but not the block size, so this was read from the source rather than
the report.


---

<!-- from paper/04_results.md -->

## 4.9 Regional meteorological context

Table R10 characterises the meteorological conditions of each region's predictor window against its
own 2017 to 2020 climatology (Section 3.17). Anomalies are reported in physical units only;
standardised anomalies are computed by the diagnostic but are not reported, for the reason given in
Section 3.17. The label window is not characterised here and is used nowhere in this paper: it opens
on the ignition date and runs 35 to 59 days into the autumn rains, so it describes conditions during
and after the fire rather than the conditions that preceded it.

**Table R10. Predictor-window meteorology against the 2017 to 2020 climatology.** ERA5-Land, AOI
pixel-area-weighted regional means; temperature, humidity and wind are window means, precipitation
is the window total (Section 3.17). Anomaly = observed − climatological mean, in the variable's own
units. Values read from `paper/era5_raw/<analysis_id>/era5_land_regional_summary.json`.

| Region | Window (days) | Temp. (°C) | ΔT (°C) | RH (%) | ΔRH (%) | Wind (m s⁻¹) | ΔWind (m s⁻¹) | Precip. total (mm) | ΔPrecip. (mm) |
|---|---|---|---|---|---|---|---|---|---|
| Manavgat 2021 | 57 | 22.72 | **−0.06** | 54.05 | −3.24 | 1.80 | +0.07 | 48.08 | −1.38 |
| Bejís 2022 | 61 | 24.05 | +0.92 | 55.40 | −0.65 | 2.02 | +0.02 | 81.53 | +36.32 |
| Muğla 2021 | 58 | 25.28 | +0.31 | 51.61 | −5.18 | 2.97 | +0.34 | 27.70 | −8.99 |
| North Evia 2021 (extended) | 59 | 25.73 | +1.11 | 59.64 | −3.25 | 2.06 | −0.21 | 19.72 | −61.58 |
| Montiferru 2021 | 60 | 22.58 | +0.48 | 64.17 | −2.84 | 2.22 | +0.11 | 14.95 | −35.54 |

The five predictor windows share a common signature of moderate dryness rather than extremity. Every
region is drier than its own climatology in relative humidity (−0.65 to −5.18 %), and four of five
are drier in precipitation, two of them substantially so (Evia −61.6 mm, Montiferru −35.5 mm); Bejís
is the exception, wetter than climatology by +36.3 mm. Temperature departures are small in absolute
terms, spanning −0.06 to +1.11 °C, and wind departures smaller still (−0.21 to +0.34 m s⁻¹).

The one region-level contrast the analysis was run to test concerns Manavgat. Its predictor-window
temperature is −0.06 °C from its climatological mean, while the other four sit 0.31 to 1.11 °C above
theirs. It is the only region at or below its own baseline, and the anomaly is small enough to be
read as *at* the baseline. Its humidity deficit (−3.24 %) is mid-range among the five and its
precipitation is within 1.4 mm of climatology, the smallest precipitation departure in the set. On
none of the four variables is Manavgat the extreme member. The consequence for the interpretation of
its transfer behaviour is taken up in Section 5.7.


---

<!-- from paper/05_discussion.md -->

## 5.7 The meteorological-extremity explanation, tested and not supported

Manavgat is the region whose behaviour most resists the account given above. It supplies the
reversal partner in the sharpest contrast pair (Section 5.2), it is where feature removal buys
almost all of its transfer gain (+0.025 mean delta over Manavgat-involved directions against −0.009
elsewhere, Section 5.5), and it is the target of the worst negative recovery under adaptation
(Evia→Manavgat, −0.86 of the gap). The most natural post hoc explanation is meteorological: that
Manavgat 2021 was an exceptionally extreme fire season, so that its thermal predictors were driven
by a regional weather anomaly the other regions did not share, and the resulting mapping from
dryness to burning was correspondingly idiosyncratic.

We tested that explanation and it was not supported. The ERA5-Land regional diagnostic (Sections
3.17, 4.9) characterises each region's predictor window against its own 2017 to 2020 climatology,
and Manavgat is not the meteorologically extreme member of the set. Its predictor-window temperature
sits 0.06 °C *below* its climatological mean, while the other four regions run 0.31 to 1.11 °C warm.
It is the only region at or below its own baseline, and the departure is small enough that the
honest reading is simply that Manavgat burned under climatologically ordinary temperatures. Its
humidity deficit of 3.24 % is mid-range among the five, its wind departure of +0.07 m s⁻¹ is the
second smallest, and its precipitation total is within 1.4 mm of climatology, the smallest
precipitation departure in the set. On none of the four variables is Manavgat the extreme member; on
two it is the least anomalous. Whatever makes its transfer behaviour atypical, regional
meteorological extremity in the predictor window is not it.

We report this as a failed prediction rather than as a result, and it carries the same status as the
stated regime null of Section 5.6: an expectation on record, tested, and not borne out. The two
failures are informative in the same limited way. They remove candidate explanations without
supplying one.

The reader may reasonably ask why meteorology, once measured, is not simply added to the diagnostic
set of Section 4.4 as a further measure of region similarity. It is not added because the candidate
set was fixed before any diagnostic-versus-transfer correlation was computed. Twenty variants across
four families were specified, and only two of them, both conditional, ordered the transfer matrix.
Appending another measure after seeing the rest fail would be a search over the diagnostic space,
and any correlation it returned on ten pairs would be uninterpretable. The measurement is reported
for what it is, namely a descriptive
characterisation of the regions and a test of one specific explanation. It is kept out of the
ordering analysis by construction.

Two cautions attach to the reading of Section 4.9, and they are the reason it reports physical units
rather than standardised ones. The first concerns the climatology. It spans four years, and the
standard deviations it yields differ between regions by factors of 2.7 to 6.0 in the predictor
windows, so a standardised anomaly measures a different physical departure in each region and
invites a cross-region comparison that the quantity cannot support (Section 3.17). The failure mode
is concrete rather than theoretical. Bejís's label-window temperature reaches 5.7 standardised units
on a physical anomaly of +0.83 °C. Its four reference years, 19.64, 19.95, 19.94 and 19.91 °C, agree
to within a third of a degree and yield a climatological SD of 0.147 °C. Muğla's predictor-window
wind speed reaches 5.3 units on +0.34 m s⁻¹ over an SD of 0.065 m s⁻¹. That these are artefacts of a
near-degenerate denominator rather than genuine extremes is settled by comparison: Evia's label
window closes on the same calendar day as Bejís's and is twelve days longer, so any
seasonal-composition explanation would apply to it at least as strongly, yet its comparable +0.67 °C
anomaly yields 1.9 standardised units against an SD of 0.351 °C. The physical anomalies of the two
regions are similar; only their denominators differ.

The second caution is that the label window is not fire weather: it opens on the ignition date and
runs 35 to 59 days into the autumn rains, so it describes conditions during and after the fire
rather than those that preceded it. Only predictor-window values are used anywhere in this paper,
and the label-window figures quoted immediately above serve solely to demonstrate the instability of
the standardised scale.

