# Pre-registration: how far do wildfire susceptibility models travel across seasons and regions?

**Version:** 1.0-draft (2026-09-19). **Status: DRAFT — not yet binding.** It becomes binding when committed
to the public registration repository, tagged `prereg-v1.0`, and archived by Software Heritage (§17).

**Authors:** Emrehan Metin, Yunus Emre Coğurcu (Çukurova University). Target journal: *Environmental
Modelling & Software*.

**Companion documents, registered with this file and binding to the same degree:** `STUDY_DESIGN.md`
(v0.4), `PRODUCT_SPECS.md` (per-product bands, quality masks, scaling, compositing, aggregation),
`FWI_SPEC.md` and `fwi_reference_rows.csv` (Fire Weather Index implementation and its reference test),
`precision/PRECISION.md` and `precision/precision_analysis.py` (precision analysis). Where this file and a
companion disagree, this file governs.

---

## 1. What the authors have already seen (disclosure)

- A **pilot** on five hand-drawn regions (Manavgat 2021, Bejís 2022, Muğla 2021, North Evia 2021,
  Montiferru 2021), one fire season each, frozen at git tag `pilot-v1-frozen` of the analysis repository.
  Its results motivate this design. **Tiles intersecting the pilot's regions are excluded** (§4.5), so no
  outcome in this study has been seen.
- **Label-free** checks: Earth Engine dataset availability (`DATA_AVAILABILITY.md`) and product
  documentation (`PRODUCT_SPECS.md`).
- The FWI implementation's agreement with a published reference table (`FWI_SPEC.md`).
- **Not seen:** any burned-area count, predictor value or model outcome on any candidate tile of this
  study. The eligibility counts of §4 are computed only after this registration is archived, by the
  registered script.

## 2. Questions and pre-specified estimands

Notation: AUC = ROC-AUC on the evaluation population of a tile-season (§6). *T* = a target tile-season.

| Id | Question | Estimand | Role |
|---|---|---|---|
| **P1** | Spatial transfer gap | mean over targets of AUC(V1) − AUC(V3) | primary |
| **P2** | Temporal transfer gap | mean over targets of AUC(V1) − AUC(V2) | primary |
| **P3** | Temporal vs spatial | mean over targets of AUC(V2) − AUC(V3); **reported against its detectability bound** | primary |
| **P4** | Skill that travels | for each predictor group *g*: AUC(V3, all groups) − AUC(V3, all but *g*) | primary, family F1 (7 tests) |
| **P5** | Skill that stays local | for each group *g*: the same contrast under V1 | primary, family F2 (7 tests) |
| **P6** | Evaluation frame (Q1) | mean over tile-seasons of AUC(full tile, V1) − AUC(near-field frame, V1) | primary |
| S1 | Deployment skill | AUC of a model trained on all other tiles and seasons, tested on the held-out tile (pooled leave-one-tile-out) | secondary |
| S2 | Full transfer | mean AUC(V4) and AUC(V1) − AUC(V4) | secondary |
| S3 | Anticipation (Q4) | rank correlation over directions between the P1 gap and each pre-listed diagnostic (§9.3) | secondary, family F3 |
| S4 | Covariate vs concept shift | importance-weighted V3 minus V3; per-feature signed AUC reversals | secondary, family F4 |
| E | Anything else | labelled exploratory in the paper | exploratory |

Direction of interest is two-sided for every estimand; every estimand is reported with its interval,
whatever it shows.

## 3. Units, domain and grid

- **Study domain:** tile centroids inside the RESOLVE 2017 biome "Mediterranean Forests, Woodlands &
  Scrub" and inside Portugal, Spain, France, Monaco, Italy, Malta, Slovenia, Croatia, Bosnia and
  Herzegovina, Montenegro, Albania, Greece, Türkiye or Cyprus (FAO GAUL 2015 level 0, country of the
  centroid).
- **Tiles:** the grid of 0.5° × 0.5° cells in EPSG:4326 with edges at integer multiples of 0.5°. Tile id =
  `"{lon_min:+07.2f}_{lat_min:+06.2f}"`.
- **Analysis cells:** MODIS sinusoidal 463.3127 m cells (the MCD64A1 grid) whose centre falls in the tile.
- **Seasons:** 1 June – 31 October of year *y*, *y* ∈ 2015–2024; MCD64A1 day of year 152–304 (153–305 in
  2016, 2020, 2024).

## 4. Cohort rule

### 4.1 Evaluation population of a tile-season
Cells whose MCD12Q1 LC_Type1 class of year *y* − 1 is 1–10 (forests, shrublands, savannas, grasslands),
with a valid label (MCD64A1 QA: mapped), and with valid predictors under the rules of §5.4.

### 4.2 Tile-season eligibility (all must hold)
1. ≥ 100 burned cells in the evaluation population.
2. Burned cells in the evaluation population ≥ 50 % of all burned cells of the tile-season (the gate).
3. Evaluation population ≥ 80 % of the tile's cells that are MCD12Q1 classes 1–10.
4. ≥ 16 spatial blocks (§6.1) containing at least one burned evaluation cell.

### 4.3 Tile eligibility
≥ 3 eligible seasons in 2015–2024.

### 4.4 Separation
Selected tiles are pairwise at Chebyshev distance ≥ 2 in tile units (no shared edge or corner).

### 4.5 Exclusion
Tiles intersecting any pilot region bounding box (listed with coordinates in `STUDY_DESIGN.md` §2 source:
`repo/core/regions.py` at commit 6381f4c) are excluded.

### 4.6 Selection
Among eligible tiles, choose the set of **10 analysis tiles** that satisfies §4.4 and maximises, in
lexicographic order: (a) number of distinct countries; (b) number of distinct RESOLVE ecoregions
(of the centroid); (c) total eligible seasons, counting at most 5 per tile. The optimum is found by exact
search (integer programming or exhaustive enumeration); ties are broken by the lexicographically smallest
sorted list of tile ids. Each tile contributes its eligible seasons, all of them if ≤ 5, else the 5 most
recent.

**Hold-out:** from the remaining eligible tiles, 2 more are chosen, satisfying §4.4 against all selected
tiles, by the same objective computed on the 12-tile set (maximise new countries, then new ecoregions,
then eligible seasons; same tie-break). They are sealed (§14).

**Negative control:** the tile-season, from tiles satisfying §4.4 against all 12, with the most burned
cells among those that fail criterion 4.2.2 because at least 50 % of burned cells are MCD12Q1 class 12
(croplands). Carried as a control of the gate only; no model is fitted on it.

### 4.7 Fallback
If fewer than 12 tiles are eligible at 0.5°, the whole of §4 is applied at 1.0° (edges at integer
degrees) and the 0.5° count is reported. If fewer than 12 are eligible at 1.0°, all eligible tiles are
used, the hold-out is reduced to 1 tile if ≥ 11 are eligible and dropped otherwise, and this is recorded
as a deviation before any outcome is computed.

### 4.8 Precision update
Once the cohort and its seasons are fixed, and before any outcome, `precision_analysis.py` is re-run
with the actual number of tiles and seasons; its output is added to the registration repository as an
update and the P3 detectability bound (§10.4) is taken from it.

## 5. Labels and predictors

### 5.1 Label
Burned in season *y*: MCD64A1 BurnDate in the season's day-of-year range (§3), collection queried with
month-aligned bounds and filtered per pixel. A cell burned more than once in a season counts once.
MCD64A1 unmapped pixels are missing labels (excluded); special-condition pixels are unburned.

### 5.2 Predictors (window ends 31 May of year *y*; baselines = the five preceding years, cells burned in
a baseline year excluded from that year's baseline statistic)
| Group | Variables |
|---|---|
| G1 terrain | elevation; slope; northness = cos(aspect)·sin(slope); eastness = sin(aspect)·sin(slope); topographic position index (2 km radius) |
| G2 fuel / land cover | shares of MCD12Q1 (y − 1) forest (1–5), shrubland (6–7), savanna (8–9), grassland (10), cropland and mosaic (12, 14), built (13) over the 3 × 3 neighbourhood; MOD44B percent tree cover and percent non-tree vegetation (y − 1) |
| G3 vegetation and moisture proxies | NDVI and EVI median, 1 March – 31 May; NDVI anomaly (z-score vs baseline); LAI median; ΣET/ΣPET, 1 March – 31 May |
| G4 thermal | LST day median, 1 March – 31 May; LST day anomaly (z-score vs baseline) |
| G5 antecedent weather and drought | CHIRPS precipitation anomaly over the 3, 6 and 12 months to 31 May (ratio to baseline mean); ERA5-Land 2 m temperature and VPD anomaly, 1 March – 31 May; ERA5-Land soil water layer 1–3 (0–100 cm, depth-weighted) anomaly on 31 May; TerraClimate climatic water deficit, 12 months to May; FWI Drought Code and Duff Moisture Code on 31 May |
| G6 human access | GHSL population and built-up surface (latest epoch ≤ y − 1); distance to nearest GRIP4 road; VIIRS night-light level (y − 1) |
| G7 fire history | years since last burn (capped at 11) and number of burns in the 10 years to 31 May of *y*, from MCD64A1 |

Exact products, bands, quality masks, scale factors, minimum observation counts and aggregation to the
grid: `PRODUCT_SPECS.md`. FWI: `FWI_SPEC.md` (xclim 0.62.0, solar-noon values, continuous computation
from 2013-01-01).

### 5.3 Redundancy rule (applied once, on label-free pooled data of the 10 analysis tiles, before any outcome)
Compute Spearman correlations between all predictors. While any pair has |ρ| > 0.9, drop the member that
comes later in this priority order: G1, G7, G5, G3, G4, G2, G6, and within a group the later-listed
variable. The resulting list is recorded in the registration repository as an update before outcomes.

### 5.4 Validity and missing data
A cell is dropped from a tile-season if more than 3 of its predictors are missing. Remaining missing
values are imputed with the training-fold median (never using test or target data).

### 5.5 In-season explanatory arm (not a forecast)
Seasonal statistics of daily FWI (mean, 90th percentile, days with FWI > 38) and hot-dry-windy days,
June–October of *y*. Reported only as secondary explanation (S-series), never mixed into P1–P6 models.

## 6. Evaluation designs

### 6.1 Spatial blocks
Block size is fixed once, before outcomes, from label-free data: for each analysis tile-season, compute
the empirical semivariogram of the first three principal components of the standardised G1–G4, G6 and G7
predictors; fit an exponential model; take the practical range (95 % of sill). Block size = the median
practical range over tile-seasons, floored at 11.1 km (ERA5-Land resolution) and rounded up to a whole
number of cells. Blocks = square groups of cells on the analysis grid. Sensitivity: twice that size.

### 6.2 Designs
| Design | Training data | Test data |
|---|---|---|
| V1 within | the tile-season, 5-fold spatial-block cross-validation (StratifiedGroupKFold, shuffle, seed 42) | out-of-fold predictions for the tile-season |
| V2 temporal | all other eligible seasons of the same tile | the tile-season |
| V3 spatial | the same calendar year of another tile (ordered pairs of tiles sharing an eligible year) | the tile-season |
| V4 both | another tile, a different year | the tile-season |
| S1 deployment | all other analysis tiles, all their seasons | the tile, each season |

For V3 and V4 every ordered (source tile-season, target tile-season) pair satisfying the definition is
evaluated; target-level means average over its sources.

### 6.3 Models (hyperparameters fixed; nothing tuned on evaluation data)
- **Random forest (primary):** scikit-learn `RandomForestClassifier(n_estimators=300, max_depth=None,
  min_samples_leaf=3, max_features="sqrt", class_weight="balanced", random_state=42)`.
- **Gradient boosting:** `HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05,
  max_leaf_nodes=31, min_samples_leaf=20, l2_regularization=0.0, class_weight="balanced",
  early_stopping=False, random_state=42)`.
- **Penalised logistic regression:** standardisation fitted on training data, `SplineTransformer(
  n_knots=5, degree=3)` on each continuous predictor, `LogisticRegression(penalty="l2", C=1.0,
  class_weight="balanced", max_iter=5000)`.
P1–P6 use the random forest; the other two are reported for every primary estimand as a robustness
family (not multiplicity-corrected, not used to choose a result).

### 6.4 Leakage controls
Forbidden as predictors: every label and label-derived column, coordinates, tile and cell identifiers,
population flags. Asserted at every fit. No predictor uses data after 31 May of *y*, except the S-series
in-season arm.

## 7. Metrics
Primary: ROC-AUC. Also reported for every design: PR-AUC and its lift over prevalence; standardised
partial AUC for FPR ≤ 0.1 (McClish); share of burned cells in the top 10 % of scores; and, after
Platt recalibration fitted on a held-out 50 % of target blocks, Brier score and reliability curve on the
other 50 %. Prevalence is reported next to every metric.

## 8. Evaluation frame (P6)
Near-field frame of a tile-season = evaluation cells within 2 km (Euclidean, cell centres) of a burned
cell of that season, plus the burned cells. **This frame is label-conditioned: a diagnostic of how
scoring extent shapes AUC, not an achievable skill.** Controls, each reported: (a) edge exclusion (drop
cells within one and two cells of a burned/unburned boundary); (b) placebo frames of equal area placed
by rule in unburned evaluation cells (50 per tile-season, seed 42); (c) prevalence-matched random
subsamples of the full tile.

## 9. Secondary analyses
### 9.1 S1, S2 as defined in §2 and §6.2.
### 9.2 S4 covariate vs concept shift
Importance-weighted V3 (weights from a domain classifier trained on source vs target predictors, a
gradient-boosting model with the §6.3 settings, clipped at the 1st and 99th percentiles) minus
unweighted V3; per-feature univariate AUC per tile-season and its sign across tile pairs, with
tile-cluster intervals.
### 9.3 S3 anticipation diagnostics (family F3)
Over ordered tile pairs: (1) mean standardised Euclidean predictor distance; (2) domain-classifier AUC;
(3) share of target cells inside the source's area of applicability (Meyer & Pebesma 2021, weighted by
random-forest importance); (4) climate distance (aridity index, mean annual precipitation and
temperature); (5) geographic distance. Each correlated (Spearman) with the P1 gap.

## 10. Inference

### 10.1 Primary model
For contrasts over ordered tile pairs (P1, P3, P4, S2, S3), the per-pair outcome *y*ₛₜ is modelled as
*y*ₛₜ = μ + *a*ₛ + *b*ₜ + *c*₍ₛ,ₜ₎ + *e*ₛₜ with random source, target and **pair** effects (the pair effect
shared by both directions) and *e*ₛₜ with its sampling variance treated as known (from a spatial-block
bootstrap of the target, 1,000 replicates). Fitted by REML; interval for μ by t with *n*tiles − 1 degrees
of freedom. For per-tile contrasts (P2, P5, P6) the unit is the tile; interval by t over tile means.

### 10.2 Conservative check
Tile-cluster bootstrap resampling tiles in both source and target roles, 2,000 replicates, seed 42,
percentile interval. Reported next to every primary interval.

### 10.3 Other units
Pair-cluster bootstrap and leave-one-tile-out jackknife with t(*n*tiles − 1) are reported. A verdict that
depends on the unit is stated as such.

### 10.4 Equivalence and bounds
Margins ±0.02 and ±0.05 ROC-AUC. Equivalence is concluded when the 90 % interval lies inside the margin.
A contrast whose interval includes 0 is reported as "no effect larger than the interval's bound", never
as "no effect". **P3 is reported against the detectability bound from §4.8** (at 10 tiles about 0.12 at
80 % power under the registered variance assumptions).

### 10.5 Multiplicity
Holm, α = 0.05, within each family: F1 = P4 (7 groups), F2 = P5 (7 groups), F3 = S3 (5 diagnostics),
F4 = S4 per-feature reversals. P1, P2, P3 and P6 are single primary tests, each reported with its own
interval.

## 11. Planted-signal check (before real outcomes)
The full evaluation chain (§6–§10) is run once on synthetic labels generated on the real predictors with
a known within-tile signal and a known, different signal in another tile; the chain must recover the
planted V1 − V3 gap within its interval. The result is committed before any real outcome is computed.

## 12. Pre-declared sensitivity analyses
1. EFFIS perimeter labels (majority rule; any-burn as sub-sensitivity), all years.
2. FireCCI 5.1 labels, 2015–2020.
3. MCD64A1 special-condition pixels treated as missing.
4. Pilot LST quality rule instead of LST error ≤ 2 K.
5. Every contrast involving G4 on seasons 2015–2022 only (Terra orbit drift).
6. Season window July–September.
7. Block size twice the §6.1 value.
8. Population with MCD12Q1 class 14 (mosaic) added; population from WorldCover 2021 (static).
9. FWI at 12:00 UTC instead of solar noon; snow-affected cells excluded.
10. The other two model families (§6.3).
Sensitivities are reported whatever they show and are not used to choose a primary result.

## 13. Exclusions that are not outcomes
Tile-seasons can fail eligibility only by §4.2. After selection, no tile or season is removed for any
reason other than a data failure (a product missing for the window), which is recorded in
`DEVIATIONS.md` with the product and dates before outcomes are computed.

## 14. Hold-out tiles and negative control
The 2 hold-out tiles are exported and quality-checked with the others, but the code refuses to compute
any outcome on them until `HOLDOUT_UNSEAL` is committed, which requires the paper's results and
conclusions sections to be committed first. Once unsealed, P1–P6 and S1 are computed on them once and
reported as they come out. The negative-control tile is reported with its gate values only.

## 15. Outcome lock
The analysis code refuses to compute any outcome metric unless (a) the SHA-256 of this file and every
companion document matches the hashes recorded in the registration repository's tag `prereg-v1.0`, and
(b) the registered updates of §4.8 and §5.3 are present.

## 16. Deviations
`DEVIATIONS.md` in the analysis repository records every departure from this registration: date, what
changed, why, and whether any outcome had been computed at the time. The paper reports every entry.

## 17. Registration mechanics
This file and its companions are committed to a **public repository containing only the registration**,
tagged `prereg-v1.0` (annotated, never moved), pushed to GitHub, and submitted to Software Heritage
("save code now") for an independent timestamp. The analysis repository records the registration
commit hash. Updates (§4.8, §5.3) are added as new tags (`prereg-v1.0-update-N`) and archived the same way.

## 18. Timeline
Registration → infrastructure and tests (§11) → cohort selection → export and label-free checks (§4.8,
§5.3, §6.1) → updates archived → outcomes on the 10 analysis tiles → results and conclusions written →
hold-out unsealed → simulated review → co-author approval → submission. Target: about two months from
registration.
