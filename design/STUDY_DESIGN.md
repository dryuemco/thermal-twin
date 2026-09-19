# Study design — transferable wildfire susceptibility models (DRAFT v0.4, 2026-09-19)

**Status: draft for the authors' approval. Nothing here has been run.** Data sources are confirmed
against `DATA_AVAILABILITY.md` (live Earth Engine checks, 2026-09-19); the only remaining [DATA] item is
EFFIS, which is outside Earth Engine. Once approved, this becomes the basis of the pre-registration (`PREREGISTRATION.md`), which is
committed, tagged, pushed and independently archived before any outcome is computed (§9).

The pilot (`paper/PILOT_FROZEN.md`, tag `pilot-v1-frozen`) motivates the decisions below; the pilot
lesson each one answers is given in brackets. §11 maps every known threat to validity to its safeguard.

## 0. Contribution statement (fixed now, so the paper cannot drift)

Wildfire susceptibility models are routinely validated inside the region and season they were fitted
in, then used elsewhere and later. The study contributes, **in one pre-registered design on
rule-defined regions**: (i) a measurement of how much the evaluation frame alone changes reported skill;
(ii) separate estimates of the transfer gap's temporal part (another season, same region) and spatial
part (another region), which single-season multi-region studies cannot make, with their difference
reported against a pre-registered detectability bound (§7); (iii) which
predictor groups carry skill that travels; (iv) an open, tested research infrastructure that makes all
of this reproducible and extensible to other regions and hazards. The pilot's findings are cited as the
motivation, not re-used as evidence.

## 1. Questions

- **Q1 Evaluation design.** How much does the choice of evaluation frame (extent, negative pool) change
  reported skill, and which frame answers which user question?
- **Q2 Transferability.** How well does a model transfer (a) to another fire season in the same region,
  (b) to another region, (c) to both, relative to within-season skill?
- **Q3 Drivers.** Which predictor groups carry skill that travels, and which carry skill that is local?
- **Q4 Anticipation (secondary).** Can the size of a transfer gap be anticipated before target labels
  exist, from covariate distance, area of applicability or climate-regime descriptors? (45 region pairs,
  against 8 effective pairs in the pilot.)

## 2. Units and cohort [lessons 1, 2]

- **Region = a fixed tile of a fixed grid.** 0.5° × 0.5° over the northern Mediterranean rim (about
  55 × 44 km at 38° N). Geometry fixed before any label or predictor is looked at.
- **Pre-declared fallback:** if fewer than 12 tiles (10 analysis + 2 hold-out) are eligible at 0.5°,
  the rule is applied at 1.0° instead. Eligibility counts are design quantities, not outcomes, so this
  choice is made without seeing any model result, and the count at each size is reported.
- **Season = 1 June – 31 October of year *y*, 2015–2024.**
- **Tile-season eligibility** (design validity only, never a model quantity): ≥ 100 burned
  natural-vegetation cells in the season; burned natural-vegetation share ≥ 0.50 (the pilot's gate);
  valid predictor coverage ≥ 80 % of the tile; ≥ 16 positive-carrying spatial blocks at the primary
  block size (the pilot's floor for a meaningful block bootstrap).
- **Tile eligibility:** ≥ 3 eligible seasons in 2015–2024.
- **Separation:** selected tiles are at least one tile apart (no shared edge or corner), so no fire and
  no spatially autocorrelated neighbourhood spans a training and a test region.
- **Pilot independence:** tiles intersecting the pilot's AOIs are excluded.
- **Selection rule** (written, committed and archived before it is applied; deterministic, ties by tile
  id): maximise distinct countries, then distinct ecoregions (`RESOLVE/ECOREGIONS/2017`), then number of
  eligible seasons. Target **10 analysis tiles**, up to 5 seasons each (all if ≤ 5, else the 5 most
  recent).
- **External hold-out:** the same rule then selects **2 further tiles** that are sealed: their outcomes
  are computed once, after every analysis on the 10 is final and the paper's conclusions are written,
  to test whether the conclusions hold out of sample.
- **Negative control:** 1 cropland-dominated tile (fails the gate) is carried as a control, as Kozan was
  in the pilot, to show the gate separates agricultural burning from wildfire.

## 3. Grid, labels and label quality [lessons 4, 7]

- **Analysis grid = the MODIS sinusoidal 463 m grid of MCD64A1;** the label is never resampled. All
  predictors are aggregated onto it with the kernel and statistic declared per variable.
- **Label:** burned in season *y* per `MODIS/061/MCD64A1` BurnDate (month-aligned collection query plus a
  pixel-level day-of-year filter). A cell burned more than once in a season counts once. **Unit tests**
  cover windows that start mid-month, span months and cross years.
- **Primary population:** cells whose dominant land-cover class in **MODIS MCD12Q1 of year *y* − 1**
  (annual, native 463 m grid) is forest, shrubland, savanna or grassland. Land cover mapped *before*
  the season is essential: the pilot defined its 2021 fires' population with WorldCover 2021, which may
  be mapped from post-fire imagery. WorldCover 2021 is a static sensitivity.
- **Cell rule:** MCD64A1 is native to the grid, so each cell is one burned/unburned pixel and needs no
  rule. For FireCCI (250 m) and EFFIS perimeters the primary rule is majority of the cell burned, with
  any-burn as sensitivity. MCD64A1 unmapped pixels (QA) become missing labels, not negatives; the
  season is DOY 152–304 (153–305 in leap years).
- **Independent validation of the label:** EFFIS burnt-area perimeters (EU and Türkiye, all study years)
  rasterised to the grid; agreement reported per tile-season, and the headline estimands re-computed on
  EFFIS labels as a sensitivity. [DATA: EFFIS is not in Earth Engine; obtained from the EFFIS download
  service and hashed into the manifest.]
- **Second satellite product:** FireCCI 5.1 is independent of MCD64A1 but ends in 2020, so it checks
  2015–2020 only. VIIRS VNP64A1 and GlobFire share MCD64A1's algorithm family or are built from it, so
  they are robustness checks, not independent validation. Active-fire agreement uses MOD14A1/MYD14A1 fire classes 8–9 (Earth Engine's `FIRMS` is the
  near-real-time feed and not science quality).

## 4. Predictors [lessons 3, 6]

All forecast predictors are observable **before the season opens** (windows ending 31 May of year *y*).
Anomaly baselines use the five preceding years only, never year *y*, and exclude cells burned in those
years from the baseline statistic. Quality masks (LST QC bits, cloud masks) are fixed per product at
registration (the pilot applied a QC rule to part of its cohort only).

| Group | Variables (final list fixed at registration) | Source [DATA] |
|---|---|---|
| G1 terrain | elevation, slope, northness, eastness, topographic position (2 km radius) | `COPERNICUS/DEM/GLO30_2024_1` (acquired 2010–2015, before every season) |
| G2 fuel / land cover | class fractions over the 3 × 3 neighbourhood (year *y* − 1), tree cover (MOD44B of year *y* − 1) | MCD12Q1, MOD44B |
| G3 pre-season vegetation and moisture proxies | NDVI/EVI level and anomaly, LAI/FPAR, ET/PET ratio (no live fuel moisture product exists) | MOD13A1, MOD15A2H, MOD16A2GF |
| G4 pre-season thermal | LST day level and anomaly (two channels), MOD11A1 with LST error ≤ 2 K (pilot's stricter rule as sensitivity) | MOD11A1 |
| G5 antecedent weather and drought | 3/6/12-month precipitation anomaly, temperature and VPD anomaly, soil-water anomaly, climatic water deficit, **Drought Code and Duff Moisture Code on 31 May** | ERA5-Land (daily, hourly), TerraClimate (to 2024-12), CHIRPS |
| G6 human access | population and built-up (latest GHSL epoch ≤ *y* − 1, never projections), distance to roads, night-light level of *y* − 1 (level only: the V21/V22 version break at 2021/2022 has no overlap year) | GHSL P2023A, GRIP4, VIIRS DNB |
| G7 fire history | years since last burn, burns in the previous 10 years, including January–May of *y* (all before the season opens) | MCD64A1 |

- **Redundancy check before registration:** pairwise correlations and variance inflation within and
  across groups on label-free data; any pair above |r| = 0.9 is reduced to one variable, by a rule
  written first.
- **In-season explanatory arm (G8)**, season weather extremes (hot-dry-windy days, seasonal FWI), is
  reported separately and never mixed into the forecast model.
- **Fire Weather Index system:** no usable FWI exists in Earth Engine at this scale (GFWED is ~62 km and
  final FWI only). The FWI codes are computed from ERA5-Land hourly noon values with an implementation
  tested against published reference values.
- **Canopy height excluded:** the ETH 2020 map is built from 2020 imagery and shows 2015–2020 burns in
  their post-fire state, the same leakage the design rejects WorldCover for.
- **Terra orbit drift:** Terra's overpass drifts earlier from 2022, which biases daytime LST anomalies
  low in 2023–2024 independently of dryness. Every contrast involving G4 is repeated on seasons
  2015–2022 only.
- **Precipitation:** CHIRPS (5.6 km, gauge-corrected) is primary for antecedent totals; ERA5-Land hourly
  feeds the FWI codes. (ERA5-Land's daily aggregate spans 23:00–23:00 UTC and is not used for FWI.)
- **Aggregation to 463 m:** MOD11 (927 m) takes the parent pixel; MOD44B (232 m) the mean of 2 × 2;
  finer products an area-weighted mean; coarse climate the nearest native pixel, FWI computed on the
  native 0.1° grid first. Full per-product rules: `PRODUCT_SPECS.md`.
- **Sensors:** MODIS/VIIRS 500 m throughout; Sentinel-2 is unreliable before 2017 and Landsat 9 starts
  late 2021, so neither enters the primary stack.
- **Tile-level regime descriptors** for Q4: aridity index and a fuel-limited versus drought-limited
  classification, computed from climate only.

## 5. Models [fixed in advance]

Random forest (primary; the pilot's configuration), histogram gradient boosting, and penalised logistic
regression with spline terms. Hyperparameters fixed at registration; nothing tuned on an evaluation
fold. Class weighting balanced. Seed 42; thread-level nondeterminism tolerance (pilot: ≤ 1.3e-5)
declared and checked.

## 6. Evaluation designs and estimands [lesson 5]

| Design | Train | Test | Estimand |
|---|---|---|---|
| V1 within | tile-season, spatial blocks | held-out blocks | within-season skill |
| V2 temporal | other seasons of the tile | held-out season | temporal transfer |
| V3 spatial | other tiles, same seasons (pooled and pairwise) | held-out tile | spatial transfer |
| V4 both | other tiles, other seasons | held-out tile-season | full transfer |

- **Block size** from the empirical autocorrelation range of the predictors (label-free), with a floor
  at the coarsest predictor's resolution (ERA5-Land, 11 km) so no weather pixel spans a training and a
  test block; a fixed 10 km sensitivity is reported.
- **Primary metric:** ROC-AUC on the full tile population. Also PR-AUC lift over prevalence, partial AUC
  (FPR ≤ 0.1), top-10 % capture, and calibration (reliability, Brier) after recalibration. Per-tile
  prevalence is reported next to every metric.
- **Q1 frames:** full tile (primary); distance bands and near-field collars reported only as
  **label-conditioned diagnostics**, with placebo collars and edge exclusion (the pilot's checks).
- **Primary contrasts:** V1 − V2, V1 − V3, V2 − V3; each predictor group's contribution to V1 and V3 by
  paired group ablation, and grouped permutation importance.
- **Planted-signal check:** the full evaluation chain is run once on synthetic labels with a known
  transfer gap, to show it recovers the gap before it is run on real labels.

## 7. Inference [lesson 5]

- Independent units: tiles (10) and tile-seasons (30–50). **Primary model for the transfer matrix: a
  crossed source × target random-effects model with a random pair effect shared by both directions of a
  pair** (the pilot's transfer heterogeneity is reciprocal; without the pair term, simulated coverage is
  0.90–0.92). Conservative check: tile-cluster bootstrap resampling tiles in both roles. Target-only
  resampling is not used (coverage 0.79–0.90). Per-tile contrasts use t or bias-corrected intervals.
  Every other unit is reported, and verdicts that depend on the unit are stated as such.
- **Precision analysis (`precision/PRECISION.md`):** at 10 tiles the minimum detectable effects at 80 %
  power are about 0.07 for V1 − V3, 0.10 for V1 − V2, 0.12 for V2 − V3 and 0.02 for a predictor group's
  contribution to V3. **V2 − V3 is therefore reported as a bound, not as evidence of no difference.**
  The temporal variance is an assumption (the pilot had one season per region); the analysis is re-run
  once the eligible seasons are known, before outcomes, and its update is registered.
- Equivalence margins ±0.02 and ±0.05 ROC-AUC fixed at registration; nulls reported as bounds.
- Multiplicity: Holm within each pre-declared family (group ablations; per-feature reversals; Q4
  diagnostics).
- Covariate versus concept shift: importance-weighted transfer and a domain classifier for the covariate
  part; per-feature signed AUC with tile-cluster intervals for the conditional part.

## 8. Infrastructure [lesson 4]

A new repository owned by the authors (private until submission, then public with a Zenodo DOI):
- Config-driven (one YAML per tile-season), installable Python package, pinned environment (lock file
  and container).
- Earth Engine export module with the query logic unit-tested; every artefact recorded in a manifest
  with SHA-256; analysis reads only manifest-verified inputs.
- Leakage assertion at every fit; forbidden columns declared in one place.
- **Outcome lock:** the code refuses to compute any outcome metric, or to touch the sealed hold-out
  tiles, unless the committed pre-registration's hash matches the archived tag.
- Continuous integration: unit tests, the planted-signal end-to-end run on a small synthetic tile.
- Verified components of the pilot pipeline (the fixed MCD64A1 query, the gate, block assignment) are
  reused with attribution to their author.
- Data licences and attribution recorded per source.

## 9. Pre-registration and deviations

- `PREREGISTRATION.md` (cohort rule, tile separation, hold-out and control tiles, grid, season, label
  rules, predictors and quality masks, redundancy rule, models, designs, estimands, metrics, primary
  unit, margins, multiplicity families, precision analysis) is committed and given an annotated tag.
- **Independent timestamp without an account:** Software Heritage archives only public repositories,
  and the code stays private until submission, so the registration lives in a **separate public
  repository that holds only the registration documents**. Its tag is pushed to GitHub and the
  repository is submitted to **Software Heritage** ("save code now"), which archives it with its own
  timestamp. The main repository records the registration's commit hash, and the outcome lock checks it.
  The tag is never moved or rewritten. (OSF remains available if the authors later prefer it.)
- `DEVIATIONS.md`: any departure from the registration is recorded with date, reason and whether it was
  made before or after any outcome was seen; the paper reports every entry.

## 10. Sequence

1. Approve this design. 2. Confirm data availability [DATA]. 3. Write, commit, tag, push and archive
`PREREGISTRATION.md`. 4. Build and test the infrastructure on synthetic data (planted-signal check).
5. Apply the cohort rule (10 analysis tiles, 2 sealed hold-out tiles, 1 negative-control tile).
6. Export; run label-free quality and redundancy checks. 7. Lock. 8. Compute outcomes on the 10.
9. Write the paper. 10. Unseal the hold-out tiles; report them as they come out. 11. Simulated review
panel on the manuscript before submission. 12. Co-author approval and submission to EMS (~8,000 words,
~6 figures), with the pilot cited as the motivation.

## 11. Threats to validity and their safeguards

| Threat | Safeguard |
|---|---|
| Frame drawn around the fire | Fixed-grid tiles; label-conditioned frames only as diagnostics (§2, §6) |
| Region confounded with event weather | 3–5 seasons per tile; V2 vs V3 (§2, §6) |
| Missing drivers | Weather, human and fire-history groups (§4) |
| Label defects | Native grid, unit-tested query, EFFIS and FireCCI checks, cell-rule sensitivity (§3) |
| Population defined with post-fire land cover | Land cover of year *y* − 1 (MCD12Q1) (§3) |
| Coarse weather shared across blocks | Block-size floor at 11 km (§6) |
| Small fires missed by MODIS | EFFIS agreement per tile-season; stated as a scope limit (§3) |
| Temporal leakage | Pre-season windows; baselines exclude year *y*; fire history from prior seasons only (§4) |
| Spatial leakage between regions | One-tile separation; spatial blocking within tiles (§2, §6) |
| Redundant predictors inflating a group | Redundancy rule before registration (§4) |
| Inconsistent quality screening | Masks fixed per product for all tiles (§4) |
| Prevalence differences across tiles | Prevalence reported; prevalence-robust metrics (§6) |
| Overfitting through tuning | Hyperparameters fixed; no tuning on evaluation folds (§5) |
| Forking paths after results | Pre-registration, outcome lock, deviations log (§8, §9) |
| Resampling unit chosen by result | Primary unit fixed; all units reported (§7) |
| Nulls read as absence | Precision analysis and equivalence margins (§7) |
| Multiple comparisons | Holm within declared families (§7) |
| Conclusions specific to the cohort | Sealed hold-out tiles; negative-control tile; scope stated as Mediterranean (§2) |
| Pipeline error | Tests, manifest hashes, planted-signal check, CI (§6, §8) |
| Irreproducibility | Pinned environment, container, public code and data with DOI (§8) |
| Pre-registration edited later | Tag pushed and archived by Software Heritage; never moved (§9) |
| Novelty questioned | Contribution statement fixed first (§0) |

## 12. Open decisions for the authors

- Grid size (0.5° proposed) and season window (June–October proposed); one alternative of each is
  pre-declared as a sensitivity.
- Emrehan's role in the new study, and authorship.
- Target submission date, which sets whether the cohort can grow beyond 10 + 2 tiles.
