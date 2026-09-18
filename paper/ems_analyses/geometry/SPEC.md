# Evaluation-geometry analyses requested by referees (EMS round) — specification

Written 2026-09-19T01:16+03:00, **before any of the analyses below was run**. No code for them existed
when this was written. Any later deviation is recorded in the "Deviations" section at the end, with its
reason and the time it was made; nothing above that section is edited after results were seen.

What was seen before writing: the manuscript (Methods 3.6-3.8, 3.12; Results 4.3-4.4; Appendix
passages on Table B6 and A(o)), the existing scripts in `paper/code/`, and cell/positive counts of the
canonical tables. No new AUC, placement or transfer value had been computed.

## Common definitions (copied from the existing scripts, not re-invented)

- **Data**: `paper/code/_canonical.py::load(region)` (SHA-256-verified frozen exports), five regions.
  `assert_no_leakage(features)` is called before every fit.
- **Population**: `valid_for_modeling == True & burnable_tree_shrub_grass == True`, index reset
  (as in `pool_decomposition.py`, `scar_increment.py`, `frozen_mugla_verify_aoi_transfer.py`).
- **Model**: the `build(feats)` of `scar_increment.py` — median / most-frequent imputation inside the
  pipeline, one-hot land cover, `RandomForestClassifier(n_estimators=300, min_samples_leaf=3,
  class_weight="balanced", random_state=42)`; only `n_jobs=4` differs (does not change the fit).
- **Row A scores**: out-of-fold thermal predictions from `StratifiedGroupKFold(5, shuffle=True,
  random_state=42)` over blocks `row_500m//10, col_500m//10` (≈5 km), exactly as
  `pool_decomposition.py`. One OOF vector per region is computed once and reused by Analyses 1, 2, 3, 5.
- **Scars and row B**: 8-connected components (3x3 structure) of population burned cells; components
  with ≥50 cells; held area = `binary_dilation(component, iterations=round(2/0.45)=4)` with scipy's
  default (cross) structure; B = AUC of the row-A OOF scores on the held area. Nine scars; the eight of
  Table 2 exclude Bejís. Both sets are reported.
- **Collar distance (10 km collar, far-field share)**: Euclidean distance transform to the nearest
  population burned cell × 0.45 km per cell, as `frozen_mugla_verify_aoi_transfer.py`.
- **Band distance (Analysis 1 only, as instructed)**: the `distance_curve.py` convention — anisotropic
  EDT with 0.0045814° × 111.31949 km = 0.5100 km N-S and 0.5100·cos(latitude of AOI centre) km E-W.
- **Spatial-block bootstrap** (region-level intervals): resample 10-cell blocks with replacement, 1000
  replicates, `default_rng(42)`, 2.5/97.5 percentiles; replicates with one class are skipped and counted.
- **Scar-level intervals**: Student *t* over scars, plus a region-clustered version (Student *t* over
  region means of the per-scar values), since region-level quantities repeat across scars.
- **Transfer delta intervals**: the pair-cluster bootstrap of Appendix A(o) (resample the ten
  unordered region pairs with replacement, both directions travel together, 20000 replicates, seed 42,
  percentile interval), and the target-region cluster bootstrap as the alternative unit. Implementation
  is validated by recomputing `paper/equalised_delta_interval.json` from
  `paper/aoi_frame_transfer_frozen_mugla.csv` before use.
- **Reproduction gates** (checked before interpreting anything): region-wide A per region and B per
  scar against `paper/pool_decomposition.json`; full/full and 10km/10km transfer against
  `paper/aoi_frame_transfer_frozen_mugla.csv` (0.541, 14/20; 0.616, 19/20). Differences are reported,
  not fixed by adjustment.

## Analysis 1 — Distance-band AUC with edge exclusion (R2)

- Scores: row-A OOF thermal scores, per region.
- **Edge mask**: every cell of the full parquet (any population) with `burned == 1` — the label map,
  so a natural-vegetation burned cell next to a burned cropland cell is not treated as an edge.
- **Exclusion depth k ∈ {0, 1, 2} cells** (Chebyshev, 3x3 structure): positives kept = population
  burned cells that survive k erosions of the edge mask (grid border treated as burned, i.e. an AOI
  border is not a scar edge); negatives kept = population unburned cells not within k cells
  (k dilations, 3x3) of any edge-mask cell.
- **Bands** on negatives by band distance to the nearest population burned cell: [0,0.5), [0.5,1),
  [1,2), [2,5), [5,10), [10,∞) km, plus "all negatives". Each band: AUC of all kept positives vs
  kept negatives in the band; reported when the band has ≥20 negatives. Region-level 10-cell block
  bootstrap interval; cross-region mean with *t* interval over regions.
- **Frame cost under exclusion**: A_k (all kept cells) and B_k per scar (kept cells in the held area);
  mean A_k − B_k over nine and over eight scars, scar-*t* and region-clustered intervals.
- **Supports the paper** if at k = 2 the A_k − B_k interval still excludes zero with a point estimate
  of at least about two thirds of the k = 0 value, and near-field bands (0.5–2 km) remain clearly below
  the far-field band. **Weakens** it if A_k − B_k falls below about half its k = 0 value or its interval
  covers zero at k = 1 or 2 — the cost would then be substantially label noise at scar edges.

## Analysis 2 — Placebo collars (R2)

- For each of the nine scars: footprint = the component's exact cell shape. Candidate placements =
  every (dihedral orientation among the 8, translation) keeping the footprint inside the grid such that
  (i) the dilated footprint (same rule as B: cross structure, 4 iterations) contains **no** burned cell
  of the edge mask of Analysis 1, and (ii) ≥80 % of footprint cells are population cells. Placebo pool =
  population cells in the dilated footprint (all unburned by construction); a placement needs ≥50 such
  cells.
- 50 placements per scar drawn uniformly without replacement from all valid candidates,
  `default_rng(42)` consumed scar by scar in region order; if fewer than 50 are valid, all are used and
  the count is reported.
- Placebo AUC = real B positives of that scar (held-area burned cells) vs placebo pool, row-A OOF scores.
- Reported per scar: A, B, mean placebo P̄ with its 2.5–97.5 % placement range, share of placebos ≤ B,
  median distance of placebo pools to the nearest burned cell. Across scars: A − P̄ and P̄ − B with
  scar-*t* and region-clustered intervals; share of the cost reproduced, (A − P̄)/(A − B). Secondary:
  within-scar Spearman correlation of placebo AUC with placebo distance.
- **Supports** the fire-adjacency attribution if P̄ − B > 0 with its interval excluding zero and the
  placebo reproduces at most about a third of A − B. **Weakens** it if placebos reproduce about two
  thirds or more of A − B (any compact local negative pool produces the cost; the mechanism would be
  compactness/spatial locality, not proximity to the fire). In between is reported as partial.

## Analysis 3 — Frame cost vs far-field share (R2)

- Unit values: A − B per scar (k = 0 of Analysis 1). Predictor: the region's share of population
  cells with collar distance > 10 km (Table B6 convention; the band convention reported alongside).
- Fits: (i) OLS over nine scars, slope with Student *t* interval (n − 2 df) — stated as
  pseudo-replicated because the predictor has only five distinct values; (ii) **primary**: OLS of the
  region mean A − B on share over five regions, *t* interval with 3 df; (iii) Spearman ρ at region
  level. Secondary region-level measure: A − A_10km (row-A scores on the 10 km collar) against share.
- **Supports** the far-field account if the region-level slope is positive with an interval excluding
  zero. With five units an interval covering zero is the expected outcome and is reported as
  "not established", not as absence of effect. A clearly negative slope **weakens** it.

## Analysis 4 — Label-free frame equalisation of the 20-direction transfer (R2, R3)

No target label is used to define any target frame below. Source labels are available to a deployer and
may define the source frame.

- **a1 range trim**: keep target cells whose every non-missing numeric thermal-set feature (nine) lies
  in the source training frame's per-feature [1st, 99th] percentile, and whose land-cover class occurs
  in the source training frame. Same retained cells for thermal and baseline models.
- **a2 area of applicability** (Meyer & Pebesma 2021, simplified, unweighted): nine numeric features,
  imputed with source medians and standardised by source mean/sd; training dissimilarity of each source
  cell = Euclidean distance to its nearest source cell in a different fold of the source's own 5-fold
  blocked split (10-cell blocks, seed 42); threshold = min(Q75 + 1.5·IQR, max) of those distances;
  target cell kept if its nearest source-cell distance ≤ threshold.
- **b centre window**: cells within a 20 km × 20 km square centred on the registry bounding-box centre
  (the `BBOX` in `distance_curve.py`), using the cell `lon`/`lat` for the frame only (never as
  features). 20 km is the largest round size that fits inside the smallest AOI (Montiferru ≈25 km).
  Sensitivity: 15 km. Caveat stated in advance: the boxes were drawn around known fires (Methods 3.1;
  Evia's extension was label-informed), so the centre is label-free at evaluation time but not
  fire-ignorant.
- Source frames: a1, a2 — source full (primary) and source 10 km collar (secondary; trimming statistics
  taken from that source frame). b — source window → target window (primary, fully label-free on both
  sides), source full → target window and source 10 km → target window (secondary).
- Reference arms recomputed in the same run: full/full, 10km/10km.
- Reported per frame: mean thermal AUC, above/below 0.5 counts, mean baseline AUC, mean paired delta
  with pair-cluster and target-region-cluster intervals, retained target cells/positives/prevalence.
- **Supports** the paper's use of the equalised frame if label-free frames recover most of the lift
  (mean thermal AUC ≥ about 0.59, ≥17/20 above chance). **Weakens** the practical reading if they stay
  near 0.541: then 0.616 is reachable only with target labels and must be presented strictly as a
  diagnostic. For the portability null: a pair-cluster delta interval excluding zero on a label-free
  frame weakens the null; one spanning zero is consistent with it.

## Analysis 5 — Prevalence-robust metrics on every frame (R2)

- Within-region, row-A OOF thermal scores, frames: region-wide; scar + 2 km (per scar, nine); 10 km
  collar (per region). Transfer: full/full, 10km/10km and every Analysis 4 frame (per direction,
  averaged over 20).
- Metrics: prevalence π; average precision (AP) and lift AP/π; burned fraction captured in the top
  10 % and 20 % of cells by score (stable descending sort) and its normalised form
  (capture − q)/(min(1, q/π) − q), because raw capture has a ceiling of q/π when π > q and is therefore
  **not** prevalence-independent; McClish-standardised partial ROC-AUC at FPR ≤ 0.1
  (`roc_auc_score(max_fpr=0.1)`). Stated in advance: AP lift also has ceiling 1/π, so only pAUC and
  normalised capture are comparable across frames of very different prevalence.
- Intervals: region-level frames 10-cell block bootstrap (1000, seed 42); scar frames scar-*t*.
- **Supports** the frame-cost claim if pAUC and normalised capture also fall from region-wide to
  scar + collar with scar intervals excluding zero. **Weakens** it if the fall appears only in ROC-AUC
  or only in prevalence-bound metrics.

## Deviations

- **D1 (2026-09-19, after Analysis 2's primary result was seen).** Added a collar-only placebo
  variant: negatives are the population cells in the dilated pseudo-scar *minus* its footprint, so the
  pool is a ring like B's collar rather than interior plus ring. Reason: the referee's wording is
  "collars", and the primary pool (interior + ring) is two to five times larger than B's negative set.
  Placements, seed and rng consumption are unchanged; the primary result is still reported as primary.
