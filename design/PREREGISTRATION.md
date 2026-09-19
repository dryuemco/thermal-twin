# Pre-registration: how far do wildfire susceptibility models travel across seasons and regions?

**Version 1.2 (2026-09-19). Status: DRAFT — not yet binding.** Binding when both authors have approved
it, it has been committed to the public registration repository, tagged `prereg-v1.0`, and archived by
Software Heritage (§19). Revised after two adversarial reviews; the first review's item numbers (B1–B5, M1–M11, m1–m13)
and the second's (R2-1 … R2-23) are cited where a rule answers one.

**Authors and roles.** Emrehan Metin (Earth Engine exports and data pipeline); Yunus Emre Coğurcu
(analysis, statistics, writing; sole holder of the hold-out unseal step, §15). Both approve this
registration before it is archived. Target journal: *Environmental Modelling & Software*.

**This file is the single binding source.** Every rule that decides a result is stated here. Technical
annexes give implementation detail only and are registered with this file: `PRODUCT_SPECS.md` (v1.0
final: bands, quality masks, scaling, compositing, aggregation), `FWI_SPEC.md` and
`fwi_reference_rows.csv` (Fire Weather Index implementation and reference test), `precision/`
(precision analysis code and report). `STUDY_DESIGN.md` is the rationale, not a source of rules. Where an
annex differs from this file, this file governs, and the difference is recorded as an erratum in the
registration repository before any outcome. (B5)

---

## 1. What the authors have already seen (disclosure) (B1, m12)

1. **Pilot.** Five hand-drawn regions (Manavgat 2021, Bejís 2022, Muğla 2021 and 2022, North Evia 2021
   legacy and extended, Montiferru 2021) and a negative control (Kozan 2023), one season each; full model
   outcomes. Frozen at tag `pilot-v1-frozen` of the analysis repository.
2. **Pipeline test region** `dogu_akdeniz` (33.8–36.7° E, 36.0–38.0° N), used in early pipeline tests.
3. **Candidate-fire list of an abandoned extension trial** (branch `ten-region-trial`, commit
   `21d8f52e250cee22ec527d07788e6fb83558737c`, file `trial/candidate_fires.csv`, SHA-256
   `c635a83c42b7c781c6c6f345c21aada2d729496094af0433ab8d1febba6a492f`): MCD64A1 connected-component burned
   counts, natural-vegetation shares, centroids and burn days for 41 connected components (1–4,707 cells)
   in Spain, Greece, Portugal and Italy, 2019–2023; also the trial's country-year screen (burned cells and
   natural share for eight rim countries, 2019–2023), its selection rule `trial/PREREGISTRATION.md`
   (SHA-256 `d60093e69e39ffa7b4e19377ef021e7572569bb817a7b10ed3c79188c4427d93`) and its selection
   `trial/selected_regions.json` (SHA-256 `2b8be23a2b6f9f1ebc542018e1f3509dc79813803e7311ac07b390a35c0d36dc`:
   Portugal 2019, Portugal 2020, Italy 2021, Spain 2022, Greece 2023). **No model outcome was computed on
   any of them.** (R2-7)
4. **Pre-season predictors computed for one trial AOI** (Portugal 2019, Vila de Rei; bbox −8.388 to
   −6.764° E, 39.439 to 40.520° N), pipeline steps 1–3 and the Step 4 Drive exports (18 tasks: Landsat and
   MODIS LST, NDVI, WorldCover, DEM); no label-based analysis, no model. (R2-7)
5. **Label-free checks:** dataset availability, product documentation, the FWI reference test.

**Consequences.** Tiles intersecting items 1, 2 and 4 are excluded (§4.5). Tiles containing the item-3
fires are not excluded: the authors saw burned-area sizes of single seasons, which the eligibility rule
(§4.2) computes anyway, and no quantity related to any estimand of §2. Mediterranean fire years are
public knowledge, so which tiles will be eligible is partly foreseeable; the cohort rule is deterministic
(§4.6) so that this knowledge cannot steer it.

## 2. Questions, users and estimands

**Use case (EMS "relevance to user needs").** A pre-season susceptibility map, built from data available
on 31 May, used by fire-management agencies to prioritise prevention and pre-positioning for the coming
season. The decision-relevant metric is the share of the season's burned area captured by the top 10 % of
scores (§7), reported next to ROC-AUC.

Notation: *t* = target tile, *s* = source tile, *y* = season year; AUC = ROC-AUC on the evaluation
population (§4.1). Estimands are defined at the unit of their inference model (§11) (M2):

| Id | Question | Definition | Role |
|---|---|---|---|
| **P1** | Spatial transfer gap | μ of the §11.1 model for *d*ₛₜ = mean over shared retained years *y* of [AUC_V1(*t*, *y*) − AUC_V3(*s*→*t*, *y*)] | primary |
| **P2** | Temporal transfer gap | mean over tiles of each tile's unweighted mean over its seasons of AUC_V1 − AUC_V2 | primary |
| **P3** | Temporal vs spatial | μ of the §11.1 model for mean over shared years of [AUC_V2(*t*, *y*) − AUC_V3(*s*→*t*, *y*)]; decision rule in §11.4 | primary |
| **P4** | Skill that travels | for each group *g* (G1–G7): μ of the §11.1 model for mean over shared years of [AUC_V3(all) − AUC_V3(all but *g*)] | primary, family F1 |
| **P5** | Skill that stays local | for each group *g*: tile-level mean of AUC_V1(all) − AUC_V1(all but *g*) | primary, family F2 |
| **P6** | Evaluation frame | tile-level mean of AUC_V1(full population) − AUC_V1(near-field frame, §8) | primary |
| S1 | Deployment | tile-level mean AUC of pooled leave-one-tile-out (§6.2) | secondary |
| S2 | Full transfer | as P1 with V4 in place of V3 | secondary |
| S3 | Anticipation | Spearman ρ over ordered pairs between *d*ₛₜ and each diagnostic of §10.3 | secondary, family F3 |
| S4 | Covariate vs concept shift | §10.2 | secondary, family F4 |
| S5 | Group alone | as P4 with single-group models: AUC_V3(only *g*) | secondary, family F5 |
| E | Anything else | labelled exploratory | exploratory |

The unweighted mean of *d*ₛₜ over pairs is reported next to every model-based μ. All tests two-sided.

## 3. Domain, tiles, grid and seasons (m11)

- **Tiles:** 1.0° × 1.0° cells of EPSG:4326 with edges at integer degrees; id `"{lon_min:+04d}_{lat_min:+03d}"`.
- **Domain:** a tile is in the domain if ≥ 50 % of its land area (FAO GAUL 2015 level 0) lies in the
  RESOLVE 2017 biome "Mediterranean Forests, Woodlands & Scrub" and its largest-land-share country is one
  of Portugal, Spain, France, Monaco, Italy, Malta, Slovenia, Croatia, Bosnia and Herzegovina,
  Montenegro, Albania, Greece, Türkiye, Cyprus. GAUL's disputed areas count with the territory GAUL
  assigns them. (Land-share rules keep coastal tiles that a centroid rule would drop.)
- **Analysis cells:** MODIS sinusoidal 463.3127 m cells (the MCD64A1 grid) whose centre lies in the tile.
  Neighbourhood predictors (§5.2) use cells outside the tile.
- **Seasons:** 1 June – 31 October; MCD64A1 day of year 152–304 (153–305 in 2016, 2020, 2024);
  *y* ∈ 2015–2024.
- **0.5° tiles** are evaluated for eligibility only and the count is reported.

## 4. Cohort rule

### 4.1 Evaluation population of a tile-season
Cells with MCD12Q1 LC_Type1 of year *y* − 1 in classes 1–10, a mapped MCD64A1 label (QA), and valid
predictors (§4.2 item 3 for eligibility; §5.4 after selection).

### 4.2 Tile-season eligibility (all must hold) (B2, B3, m10)
1. ≥ 100 burned cells in the evaluation population.
2. Gate: burned cells of MCD12Q1 classes 1–10 (year *y* − 1) ≥ 50 % of the season's burned land cells
   with a mapped label (water excluded from the denominator). (R2-15)
3. ≥ 80 % of the tile's land cells of MCD12Q1 classes 1–10 (year *y* − 1) have valid predictors, where a
   cell is valid if at most 3 of the **full §5.2 list** (before §5.3) are missing.
4. ≥ 6 spatial blocks (§6.1, fixed size) contain at least one burned evaluation cell. Blocks with fewer
   than 50 land cells are merged into the adjacent block of the same block-row. (R2-16)

### 4.3 Tile eligibility
≥ 3 eligible seasons in 2015–2024. Retained seasons: all eligible seasons if ≤ 5, else the 5 most recent.

### 4.4 Separation
Selected tiles are pairwise at Chebyshev distance ≥ 2 in tile units (no shared edge or corner).

### 4.5 Exclusion (B1)
Tiles whose interior intersects the interior of any of these boxes (lon_min, lat_min, lon_max, lat_max)
are excluded (R2-9):
Manavgat (31.05, 36.72, 31.85, 37.35); Bejís (−1.05, 39.68, −0.35, 40.15); Muğla (27.10, 36.60, 28.90,
37.45); North Evia (23.05, 38.55, 23.85, 39.15; covers the legacy box); Montiferru (8.45, 40.05, 8.75,
40.27); Kozan (35.254, 37.001, 36.386, 37.899; 50 km buffer of 35.82° E, 37.45° N); `dogu_akdeniz`
(33.8, 36.0, 36.7, 38.0); Portugal 2019 trial AOI (−8.388, 39.439, −6.764, 40.520).

### 4.6 Selection (B4)
Among eligible tiles, choose **10 analysis tiles** satisfying §4.4 and the **overlap constraint**: every
selected tile shares at least one retained season with at least 3 other selected tiles. Maximise, in
lexicographic order: (a) distinct countries; (b) distinct RESOLVE ecoregions (the ecoregion with the
largest share of the tile); (c) total retained seasons; (d) number of ordered pairs with ≥ 1 shared
retained season. Solved exactly (integer programming, or exhaustive search if ≤ 10⁷ candidate sets);
ties broken by the lexicographically smallest sorted list of tile ids.

**Hold-out:** 2 further tiles satisfying §4.4 against all selected tiles and sharing ≥ 1 retained season
with ≥ 3 analysis tiles, chosen by the same objective evaluated on the 12-tile set, same tie-break.

**Negative control (M7, R2-3):** among domain tiles not excluded by §4.5, satisfying §4.4 against all
selected tiles, with ≥ 100 burned land cells in at least one season 2015–2024 (a label count; no model
output), the tile with the highest share of MCD12Q1 (2020) classes 12 + 14 among its land cells; ties by
smallest tile id. Reported: whether the §4.2.2 gate rejects each of its seasons. No model.

### 4.7 Fallback and abandonment (M9, m13)
If no 12-tile set satisfies §4.4 and §4.6, the largest feasible set size *n* is determined for analysis
and hold-out tiles jointly: if *n* = 11, 10 analysis tiles and 1 hold-out; if *n* ≤ 10, all *n* are analysis
tiles and there is no hold-out; among sets of size *n*, the §4.6 objective and tie-break apply. This is
recorded before any outcome. **If fewer than 6 analysis tiles can be selected, the confirmatory study is
abandoned** and the eligibility report is published in the registration repository. Separation, block
size and all thresholds are unchanged. The number of eligible tiles by country is published with update 1
(§4.8). (R2-11, R2-23)

### 4.8 Registered updates before any outcome (M3)
After selection and export, and before any outcome: (a) the §5.3 predictor list; (b) the realised
pair-incidence matrix (shared retained seasons); (c) `precision_analysis.py`, changed only to accept the
realised incidence matrix, re-run with the pilot variance components of `precision/PRECISION.md` and a
temporal-variance ratio k = 1.5 (the least favourable registered value); each simulated study draws
σ²ₛₜ from a simulated 1,000-replicate joint bootstrap, applies the 10th-percentile floor and fits the
§11.1 REML model; coverage is computed separately for P1, P3 and P4 (R2-5). These are
committed as `prereg-v1.0-update-1` and archived. **If the simulated coverage of the §11.1 interval for
P1, P3 or P4 is below 0.93, the tile-cluster bootstrap (§11.2) becomes primary for that estimand (a switch
for P1 also applies to S2, for P4 also to S5).** The P3 detectability
bound of §11.4 is taken from (c).

## 5. Labels and predictors

### 5.1 Label
MCD64A1 BurnDate within the season's day-of-year range, collection queried with month-aligned bounds and
filtered per pixel; a cell burned more than once counts once. Unmapped (QA) = missing label (excluded);
special-condition = unburned. The query is covered by unit tests, run in continuous integration before
any export, for windows that start mid-month, span month boundaries and cross calendar years; the
pilot's label defect was a query of this kind.

### 5.2 Predictors (window ends 31 May of *y*; anomaly baselines = the same window in the five preceding
years, a baseline year's value excluded for cells burned between 1 June of the previous year and 31 May
of that year) (M5)
| Group | Variables |
|---|---|
| G1 terrain | elevation; slope; northness = cos(aspect)·sin(slope); eastness = sin(aspect)·sin(slope); topographic position index, 2 km radius (GLO-30 `GLO30_2024_1`) |
| G2 fuel / land cover | shares over the 3 × 3 neighbourhood of land cells, MCD12Q1 (*y* − 1): forest (1–5), shrubland (6–7), savanna (8–9), grassland (10), cropland and mosaic (12, 14), built (13); MOD44B tree cover and non-tree vegetation cover (*y* − 1) |
| G3 vegetation | NDVI median and EVI median, 1 March – 31 May; NDVI anomaly (z-score vs baseline); LAI median; ΣET/ΣPET, 1 March – 31 May |
| G4 thermal | MOD11A1 LST day median, 1 March – 31 May, QC: LST error ≤ 2 K; LST day anomaly (z-score vs baseline) |
| G5 weather and drought | CHIRPS precipitation difference (mm) from the baseline mean, 3, 6 and 12 months to 31 May; ERA5-Land 2 m temperature anomaly and VPD anomaly (from temperature and dewpoint), March–May mean; ERA5-Land soil water, depth-weighted layers 1–3 (0–100 cm), March–May mean anomaly; TerraClimate climatic water deficit, 12 months to May; FWI Drought Code and Duff Moisture Code on 31 May |
| G6 human access | GHSL population and built-up surface, latest epoch ≤ *y* − 1 (no projections); distance to nearest GRIP4 road (all types); VIIRS night-light level of *y* − 1 |
| G7 fire history | years since last burn = *y* − latest calendar year with an MCD64A1 burn before 1 June *y*, capped at 14; burn count = distinct calendar years with a burn from 1 January *y* − 10 to 31 May *y* |

**Anomalies (z-scores):** z = (x − m)/sd, where m and sd (ddof = 1) are taken over the baseline years with a
valid value for the cell; the anomaly is missing if fewer than 3 baseline years are valid, or if sd is
below a floor (NDVI 0.01; LST 0.5 K). ERA5-Land and TerraClimate anomalies and the CHIRPS precipitation
terms are differences from the baseline mean, not z-scores, with the same baseline and 3-year
minimum (R2-21). VPD is computed from
ERA5-Land daily-mean 2 m temperature and dewpoint (Buck 1981 saturation vapour pressure, as in
`FWI_SPEC.md`), then averaged over 1 March – 31 May.

FWI: xclim 0.62.0, solar-noon hour per ERA5-Land pixel = floor(12.5 − lon/15) UTC, 24 h precipitation
ending at that hour, continuous from 2013-01-01 with start values 85/6/15, relative humidity clipped to
0–100 (`FWI_SPEC.md`). If the convergence test T6 of `FWI_SPEC.md` fails, the start moves one year
earlier, and sensitivity 12 (§12) uses a start one year before the final primary start (R2-12). Canopy height is not used (the ETH map is built from 2020 imagery, post-fire for
2015–2020). ESA WorldCover is not a predictor for the same reason (its 2020 and 2021 maps are post-fire
for earlier seasons); it enters only sensitivity 10 as an alternative population definition. Limitations stated in the paper: GHSL epochs interpolate between observations (post-season
information within an epoch; m9); GRIP4 source years differ by country.

### 5.3 Redundancy rule (label-free; once, after selection) (m1)
Data: all retained tile-seasons of the 10 analysis tiles pooled, one row per cell-season. Compute
Spearman correlations. Process pairs in descending |ρ|: while any pair has |ρ| > 0.9, drop the member
that comes later in the order G1, G7, G5, G3, G4, G2, G6 (within a group, the later-listed variable),
then recompute. The final list is registered update §4.8(a). Group membership for P4/P5 follows the
final list; a group left empty is dropped from F1 and F2 and recorded.

### 5.4 Validity and missing data
After §5.3, a cell is dropped from a tile-season if more than 3 of the final predictors are missing; the
cells lost relative to §4.2 are counted and reported, and eligibility is not re-evaluated (B3). Remaining
missing values: training-fold median imputation (never test or target data).

### 5.5 Temporal leakage in V2 (M1)
For V2, the predictors of every training season *y*′ ≠ *y* are recomputed with season *y*'s MCD64A1 treated
as unobserved: G7 counts and the baseline burn masks ignore burns dated in season *y*. Sensitivities:
(i) V2 with past seasons only (*y*′ < *y*); (ii) V2 scored only on test blocks that are spatially disjoint
from the blocks used in training (training restricted to the other blocks), which removes site
memorisation.

### 5.6 In-season explanatory arm (not a forecast)
June–October of *y*, from the same solar-noon ERA5-Land values as the FWI: daily FWI mean and 90th
percentile; days with FWI > 38; **hot-dry-windy days** = days with noon 2 m temperature ≥ 30 °C,
relative humidity ≤ 30 % and 10 m wind ≥ 20 km/h. Reported as secondary explanation only, never in
P1–P6 models.

## 6. Evaluation designs

### 6.1 Spatial blocks (B2, m2)
Fixed now: square blocks of **24 × 24 analysis cells (11.12 km)**, the lattice anchored at the MODIS
sinusoidal grid origin; partial blocks at tile edges are blocks. The 11.12 km floor matches ERA5-Land
resolution. After selection, the empirical semivariogram range is computed and reported (first three
principal components of the standardised final G1–G4, G6, G7 predictors; Matheron estimator; 20 equal lag
bins to 50 km; random sample of 5,000 cells per tile-season, seed 42; exponential model by weighted least
squares; practical range at 95 % of sill). If the median range exceeds 11.12 km, blocks of that range rounded up to a whole number of cells are a
sensitivity. Sensitivity 2: 48 × 48 cells.

### 6.2 Designs (m7, m8)
| Design | Training | Test |
|---|---|---|
| V1 within | the tile-season; 5-fold spatial-block CV (StratifiedGroupKFold, shuffle, seed 42) | out-of-fold predictions of the tile-season; AUC computed once on pooled out-of-fold predictions |
| V2 temporal | the tile's other retained seasons (with §5.5) | the tile-season |
| V3 spatial | source tile, same calendar year *y* (pairs sharing retained season *y*) | the target tile-season *y* |
| V4 both | source tile, each of its retained seasons *y*′ ≠ *y* | the target tile-season; AUCs averaged over *y*′, then over target seasons (R2-10) |
| S1 deployment | all other analysis tiles, all retained seasons | each retained season of the held-out tile |

A target tile with no V3 source contributes to P2, P5, P6 and S1 only; this is reported. Training size
differs by design (V1 ~80 % of one season; V2 up to four seasons; V3 one season); sensitivity: V2 and V3
training data subsampled at random (seed 42) to the V1 training size.

### 6.3 Models (fixed; nothing tuned on evaluation data)
- Random forest (primary): `RandomForestClassifier(n_estimators=300, max_depth=None, min_samples_leaf=3,
  max_features="sqrt", class_weight="balanced", random_state=42)`.
- Gradient boosting: `HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, max_leaf_nodes=31,
  min_samples_leaf=20, l2_regularization=0.0, class_weight="balanced", early_stopping=False,
  random_state=42)`.
- Penalised logistic regression: training-fitted standardisation; `SplineTransformer(n_knots=5,
  degree=3)` per continuous predictor; `LogisticRegression(l1_ratio=0, C=1.0, class_weight="balanced",
  max_iter=5000)`.
P1–P6 use the random forest; the other two are reported for every primary estimand as robustness (not
multiplicity-corrected, not used to choose a result).
**Software (M9):** Python 3.12, scikit-learn, numpy, scipy, pandas, xclim 0.62.0 and the Earth Engine
client at the exact versions of the lock file committed with this registration (`requirements-lock.txt`,
SHA-256 recorded at tag time); container image digest recorded before outcomes.

### 6.4 Leakage controls
Forbidden as predictors, asserted at every fit: all label and label-derived columns, coordinates, tile,
block and cell identifiers, population flags. No predictor uses data after 31 May of *y* (§5.6 excepted).

## 7. Metrics (M11)
Primary: ROC-AUC. Also: PR-AUC and lift over prevalence; standardised partial AUC for FPR ≤ 0.1 (McClish);
**share of burned cells in the top 10 % of scores (the decision metric of §2)**; Brier score of raw
scores. **Target-oracle recalibration** (labelled as such): Platt scaling fitted on 50 % of the target's
blocks (split stratified by positive-carrying blocks, seed 42), Brier score and reliability on the other
50 %. Prevalence reported next to every metric.

## 8. Evaluation frame (P6) (m4)
AUC_V1(near-field) is the AUC of the full-population V1 pooled out-of-fold predictions evaluated on the
near-field cells only; no model is refitted; placebo and prevalence-matched frames are scored the same
way (R2-4). Near-field frame of a tile-season: evaluation cells whose centre is within 2 km of a burned
cell's centre,
plus the burned cells. **Label-conditioned: a diagnostic of how scoring extent shapes AUC, not an
achievable skill.** Controls: (a) edge exclusion, cells within 1 and within 2 cells of a burned/unburned
boundary removed; (b) placebo frames: the season's burned components, each rotated by a uniformly random
multiple of 90° and translated to a uniformly random position whose footprint lies entirely in unburned
evaluation cells, 50 placements per tile-season (seed 42), each scored with the real positives; (c) 200
prevalence-matched random subsamples of the full population (seed 42).

## 9. Planted-signal check (before real outcomes) (M4)
Generator (R2-2): predictors are z-scored per tile over its retained seasons; labels ~
Bernoulli(logit⁻¹(α + Σ β·x)) with β = 1.0 for elevation, slope, NDVI anomaly, LST anomaly and the
12-month precipitation difference (if §5.3 removed one of these, the retained predictor with the highest
|ρ| to it takes its place), 0 elsewhere, and α set per tile-season to reproduce its real prevalence; in
the three analysis tiles with the smallest ids the NDVI and LST coefficients change sign; in each tile's
most recent season the NDVI coefficient is halved. **Planted value** of each checked quantity = the mean
point estimate over 200 generator replicates (seeds 1000–1199) run through the full pipeline. **Check:**
50 separate replicates (seeds 42–91). **Pass:** for V1 − V3, V1 − V2 and the G4 contribution to V3, the 95 %
interval covers the planted value in ≥ 44 of 50 replicates; and the G4 contribution to V3 has opposite
signs in sign-reversed and non-reversed target tiles in ≥ 45 of 50 replicates. **On failure:** both
authors review the code; a defect found is fixed, recorded in `DEVIATIONS.md` and the check re-run. If no
defect is found, the failure is recorded in `DEVIATIONS.md`, the tile-cluster bootstrap (§11.2) becomes
primary for all pair-level estimands, and that record satisfies §16(b). No analysis choice registered
here may change because of the check. Results committed before any real outcome.

## 10. Secondary analyses
### 10.1 S1, S2, S5 as in §2 and §6.2.
### 10.2 S4 covariate vs concept shift
Importance-weighted V3 (weights from a domain classifier: the §6.3 gradient-boosting settings, source vs
target predictors, weights clipped at the 1st and 99th percentiles) minus unweighted V3. Per-feature
univariate AUC per tile-season; for each feature, the mean pairwise sign agreement (both AUCs on the same
side of 0.5) across tile pairs, tested against 0.5 by a tile-cluster bootstrap (2,000 replicates, seed
42) (R2-17). Family F4 = the final predictor list of §5.3.
### 10.3 S3 anticipation diagnostics (F3) (M10)
Over ordered tile pairs: mean standardised Euclidean predictor distance; domain-classifier AUC; share of
target cells inside the source's area of applicability (Meyer & Pebesma 2021, random-forest importance
weights); climate distance (aridity index, mean annual precipitation and temperature, standardised);
geographic distance between tile centres. p-values by tile-label permutation (QAP), 10,000
permutations, seed 42.

## 11. Inference

### 11.1 Primary model (M3)
For pair-level outcomes (P1, P3, P4, S2, S5): *y*ₛₜ = μ + *a*ₛ + *b*ₜ + *c*₍ₛ,ₜ₎ + *e*ₛₜ, with random source,
target and pair effects (the pair effect shared by both directions) and *e*ₛₜ ~ N(0, σ²ₛₜ) with σ²ₛₜ
estimated by a **joint paired spatial-block bootstrap**: 1,000 replicates resampling the target's blocks
with replacement, computing both AUCs of the contrast (and their difference) on the same resampled
blocks from fixed predictions; σ²ₛₜ floored at the 10th percentile across pairs. REML fit; interval for μ
by t with *n*tiles − 1 degrees of freedom. Per-tile outcomes (P2, P5, P6, S1): t interval over tile means,
each tile mean the unweighted mean over its retained seasons.

### 11.2 Conservative check
Tile-cluster bootstrap resampling tiles in both source and target roles, 2,000 replicates, seed 42,
percentile interval; reported next to every primary interval (primary instead of §11.1 if §4.8(c)
triggers).

### 11.3 Other units
Pair-cluster bootstrap and leave-one-tile-out jackknife with t(*n*tiles − 1), reported. A verdict that
depends on the unit is stated as such.

### 11.4 Equivalence, bounds and the P3 decision rule (m5)
Margins ±0.02 and ±0.05 ROC-AUC; equivalence when the 90 % interval lies inside the margin. An interval
including 0 is reported as "no effect larger than the interval's bound". **P3 is "undetected" if its 95 %
interval contains 0 and its 90 % interval does not lie inside ±0.05; it is then reported with the 80 %-power
minimum detectable effect of §4.8(c) at k = 1.5, never as "no difference". If its 90 % interval lies inside
±0.05, P3 is reported as equivalent at ±0.05.** (R2-1)

### 11.5 Multiplicity (m6)
Holm, α = 0.05, within F1 (P4), F2 (P5), F3 (S3), F4 (S4), F5 (S5), on p-values of the primary inference
model. P1, P2, P3 and P6 are four separate primary questions, each answered by its own interval; they are
not a family and are not corrected jointly, because each is reported in full whatever it shows and none
is selected from the others.

## 12. Pre-declared sensitivity analyses (M6)
1. EFFIS perimeter labels (majority rule; any-burn as sub-sensitivity). 2. FireCCI 5.1 labels, 2015–2020 (majority rule; any-burn as sub-sensitivity).
3. MCD64A1 special-condition pixels as missing. 4. MOD13 SummaryQA = 0 only. 5. Pilot LST QC rule.
6. Every contrast involving G4 on seasons 2015–2022 (Terra orbit drift). 7. TPI radius 10 km. 8. GRIP4
road types 1–3 only. 9. Population with MCD12Q1 class 14 added. 10. Population from WorldCover 2021 (classes 10 tree cover, 20 shrubland, 30 grassland, by cell majority).
11. FWI at 12:00 UTC. 12. FWI started one year before the final primary start (2012-01-01 if the §5.2 convergence test passes
at the first attempt). 13. Snow-affected cells excluded. 14. Block size from
the semivariogram (if > 11.12 km) and 48 × 48 cells. 15. Season window July–September. 16. The other two
model families. 17. V2 variants of §5.5. 18. Training-size-matched V2 and V3 (§6.2).
The cohort and retained seasons are fixed by the primary rule. In a sensitivity, a tile-season with < 20
burned evaluation cells or < 5 positive-carrying blocks is dropped and counted; an estimand is computed if
≥ 6 tiles remain, otherwise reported as not estimable. Sensitivities are reported whatever they show and
never used to choose a primary result.
**EFFIS (M9):** the EFFIS burnt-area perimeters are obtained from the EFFIS data service; the version date
and SHA-256 are recorded in the manifest before the outcome lock; perimeters with a fire date inside the season window
are rasterised to the analysis grid by majority of cell area (R2-18). If EFFIS cannot be obtained before the lock, sensitivity 1 is
dropped and recorded before any outcome.

## 13. Data failures and exclusions (M9)
A **data failure** is a product with zero valid observations in its window for more than 20 % of the
evaluation cells of a tile-season. It is recorded in `DEVIATIONS.md` with product and dates, before
outcomes. Every model uses every product, so the tile-season is removed from all designs; pairs that
lose all shared seasons leave P1, P3 and P4; the §12 estimability rule (≥ 6 tiles) applies (R2-8). No
tile or season is removed for any other reason after selection.

## 14. Freezing of data (M9)
Every Earth Engine asset ID with its `system:version` and image IDs, and the SHA-256 of every exported
file, is recorded in the manifest at export. After the outcome lock there is no re-export, except for a
registered data failure.

## 15. Hold-out tiles (M8)
Hold-out tiles are exported and quality-checked with the others. They are **targets only**: V1, V2 and
V3/V4 with the 10 analysis tiles as sources, S1 with all 10 as training data. Before unsealing, the
SHA-256 of the committed results and conclusions sections of the manuscript is pushed as annotated tag
`prereg-v1.0-unseal` to the public registration repository and archived by Software Heritage; the code
refuses to compute any outcome on hold-out tiles until that tag exists and its hashes match. Once
unsealed, for each hold-out tile *h*: P1_h = mean over analysis sources *s* sharing a season of *d*ₛ,ₕ;
P3_h and P4_h analogously; P2_h, P5_h and P6_h at tile level; intervals by a 1,000-replicate target-block
bootstrap (seed 42). **A conclusion "replicates"** if each hold-out point estimate lies inside the 95 %
prediction interval for a new target from the §11.1 fit (per-tile estimands: mean ± t₀.₉₇₅,ₙ₋₁·SD·√(1 + 1/n)
over analysis tiles). Both outcomes are reported, as they come out (R2-6).

## 16. Outcome lock
The analysis code refuses to compute any outcome metric unless (a) the SHA-256 of this file and every
annex matches the hashes recorded at tag `prereg-v1.0` in the registration repository, and (b) update
`prereg-v1.0-update-1` (§4.8) is present and its planted-signal results (§9) pass.

## 17. Deviations
`DEVIATIONS.md` records every departure: date, what changed, why, and whether any outcome had been
computed. The paper reports every entry.

## 18. Scope and limitations stated in advance
The claims are about Mediterranean fire seasons 2015–2024 at 463 m. Small fires missed by MCD64A1 are
quantified by the EFFIS comparison but not recovered. Ignition causes and suppression effort are not
observed; human access enters only through proxies. In-season weather is excluded from the forecast by
design. With 10 tiles, P3 differences below the §4.8 detectability bound cannot be resolved.

## 19. Registration mechanics
Both authors approve the final text. It is committed with its annexes to a public repository containing
only the registration, tagged `prereg-v1.0` (annotated, never moved), pushed to GitHub, and submitted to
Software Heritage ("save code now") for an independent timestamp. The analysis repository records the
registration commit hash. Updates are added as new tags (`prereg-v1.0-update-N`, `prereg-v1.0-unseal`)
archived the same way. Errata to annexes (§ header) are tagged the same way before any outcome.

## 20. Timeline
Approval and archiving → infrastructure and tests → selection → export and label-free checks → update 1
archived (§4.8) → planted-signal check (§9) → outcomes on the analysis tiles → results and conclusions
committed → unseal tag → hold-out outcomes → simulated review → co-author approval → submission. Target:
about two months from archiving.
