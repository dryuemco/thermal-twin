# SPEC — EMS referee round, inference analyses (R2 majors 3–6)

Written 2026-09-19 **before any of the analyses below was run**. Nothing in this file is edited
after results are seen; any deviation forced by the data is recorded in `REPORT.md` under
"Deviations from SPEC", with its reason. Scripts: `paper/code/ems_inference_*.py`. Outputs in this
folder.

## Common to all analyses

- Data only via `paper/code/_canonical.py` (`load(region)`, SHA-256 verified; Muğla is the frozen
  copy). `assert_no_leakage(features)` is called before every fit.
- Population: primary natural vegetation (`valid_for_modeling` and `burnable_tree_shrub_grass`).
- Model, unchanged from the paper: median/most-frequent imputation inside the fit, one-hot land
  cover, `RandomForestClassifier(n_estimators=300, min_samples_leaf=3, class_weight="balanced",
  random_state=42)`, `n_jobs=4`. Feature sets `BASELINE` and `THERMAL` from `_canonical.py`.
- Increment = thermal ROC-AUC − baseline ROC-AUC on identical cells.
- Distance to burned: Euclidean distance transform on the region grid × 0.45 km (as in
  `verify_collar_increment.py`). "10 km collar" = cells with `dist_km <= 10`.
- Scar definition exactly as `scar_increment.py` / `verify_matched.py`: 8-connected burned
  components of ≥ 50 cells; held-out area = component dilated `round(2/0.45) = 4` iterations
  (default cross structure); arm skipped if source or target is single-class.
- Blocked CV exactly as `verify_matched.py`: `StratifiedGroupKFold(5, shuffle=True,
  random_state=42)`, groups = `row_500m // B`, `col_500m // B`.
- Bootstraps: seed 42, percentile intervals. Resampling replicate counts stated per analysis.

## Task 1 — frame-matched hardening ladder (`ems_inference_ladder.py`)

**1a. Scar frame (scar + 2 km), scar by scar.** For each scar with a leave-one-scar-out (LOSO) arm:

- rung **Blocked**: blocked-CV out-of-fold predictions for the whole region (scar included in
  training folds, as Table 2 row B), baseline and thermal, **scored on the scar-area cells only**.
  Primary blocking B = 10 cells (≈5 km, Table 2's blocking); secondary B = 2 cells (≈1 km, the
  blocking of the ladder's quoted "+0.056 to +0.153").
- rung **LOSO**: recomputed from canonical data (reproduction checked against
  `scar_increment.json`).
- rung **Foreign** (cross-region on the same cells): mean over the four foreign source regions of
  the increment of a full-frame source model on the scar-area cells (Table 2 row D, now paired).
- The half-split rung has no scar-frame analogue (its target is a half-region) and is **not
  computed on this frame**; stated as such.
- Primary estimand: mean over scars of the paired difference **Blocked − LOSO** (B = 10).
  Intervals, all reported:
  (i) scar-level Student t, df = n_scars − 1;
  (ii) region-clustered: CR1 cluster-robust SE of the scar mean, G = number of regions carrying
  scars, t with G − 1 df;
  (iii) region-cluster bootstrap (resample regions with their scars), 20,000 replicates.
  Also reported with the same three intervals: LOSO − Foreign, Blocked − Foreign.
- Pre-stated verdict rule: the ladder's decline "survives on a matched frame" between Blocked and
  LOSO only if the mean paired Blocked − LOSO is > 0 **and** the region-clustered interval (ii)
  excludes zero. If (ii) spans zero but (i) does not, the verdict is "not established once
  clustering by region is respected". If the point estimate is ≤ 0, "the decline does not appear on
  a matched frame".

**1b. The ladder on the 10 km collar, all four rungs**, each rung restricted to collar cells in
training and in scoring:

- Blocked: blocked CV on collar cells, B = 10 (primary) and B = 2; per-region increment; mean over
  five regions, Student t over regions (df 4).
- Half-split: the `positive_control.py` procedure on collar cells (median cut of the collar cells
  on each grid axis, both directions, split skipped if either half is single-class); mean over
  usable splits; t over the per-region means of the splits (df = regions with a usable split − 1).
- LOSO: source = collar cells outside the held-out area, target = held-out area (∩ collar; the
  number of target cells lost to the collar is reported, expected zero); mean over scars, t over
  scars.
- Cross-region: 10 km/10 km paired delta from frozen `aoi_frame_transfer_frozen_mugla.csv` (no
  refit), mean over 20 directions, pair-cluster bootstrap interval (Task 3).
- For like-for-like reading, the same four rungs are recomputed **as drawn** with the same code
  (blocked B = 10 and 2; half-split; LOSO; cross-region from the same frozen file).
- Monotonicity is read off the point estimates; no test is claimed for the ordering beyond the
  paired Blocked − LOSO contrasts, which are the only rungs scored on identical cells.

## Task 2 — equivalence / non-inferiority (`ems_inference_equivalence.py`)

**Margins, fixed now: ±0.02 and ±0.05 ROC-AUC.** TOST at α = 0.05 per side, i.e. equivalence is
declared when the two-sided 90 % interval lies inside (−m, +m).

- T = mean transfer increment over the 20 directions. Primary frame: 10 km/10 km (the frame the
  paper argues is correct); also as drawn (Table B9 deltas, `baseline_vs_thermal_transfer.csv` /
  `transfer_ci_blocksize.json`) and 5 km/5 km. 90 % intervals under every Task 3 unit; the
  pair-cluster bootstrap is the paper's unit and is listed first, but all are reported and no unit
  is chosen by result.
- W − T on matched frame and matched blocking: per target region r, W_r = within-region increment
  on the 10 km collar at B = 10 (from Task 1b), T_r = mean increment of the four directions into r
  on 10 km/10 km. Mean over five regions, Student t(4) (the paper's method for the 0.155
  shortfall). 90 % and 95 % intervals. Sensitivities: full frame (W at B = 10 as drawn vs as-drawn
  deltas from the frozen file's full/full rows) and 5 km collar (W from a 5 km-collar blocked CV at
  B = 10 vs 5 km/5 km deltas).
- Scar-frame variant: per scar, LOSO increment − Foreign increment (from Task 1a), t over scars and
  region-clustered.
- Statements, read mechanically: "no transfer gain larger than X" with X = upper end of the 90 %
  interval of T (one-sided 95 % bound); "transfer gain smaller than the within-region gain by at
  least Y" with Y = lower end of the 90 % interval of W − T (one-sided 95 % bound); each stated for
  every unit, and whether Y > 0.

## Task 3 — resampling units (`ems_inference_units.py`)

Quantities: Q1 as-drawn paired delta (20 deltas from `transfer_ci_blocksize.json` `point_delta`,
the source of Appendix A(o)'s table; cross-checked against `baseline_vs_thermal_transfer.csv`);
Q2 equalised 10 km paired delta and Q3 equalised 10 km mean thermal transfer AUC, both from
`aoi_frame_transfer_frozen_mugla.csv` (10km/10km rows). Units (95 % intervals; 20,000 bootstrap
replicates, seed 42):

1. directions, naive bootstrap (reference only);
2. unordered-pair cluster bootstrap (10 clusters; the paper's);
3. target-region cluster bootstrap (5 clusters of 4);
4. source-region cluster bootstrap (5 clusters of 4);
5. two-way: (a) pigeonhole bootstrap (Owen 2007): sources and targets resampled independently,
   direction (s, t), s ≠ t, weighted by multiplicity product, replicate dropped if total weight 0;
   (b) Cameron–Gelbach–Miller two-way cluster-robust variance V_src + V_tgt − V_direction (CR0
   components), t(4) interval, reported as undefined if V < 0; (c) dyadic-robust variance
   (Aronow, Samii & Assenova 2015): V = n⁻² Σ over ordered pairs of directions sharing at least one
   region (including d = d′) of e_d e_d′, e = y − ȳ, no finite-sample factor, t(4) interval;
6. leave-one-region-out jackknife (drop every direction involving the region; pseudo-values;
   t(4)), as in `referee2_numbers.mjs`.

Effective number of units: n_eff = n · (s²/n) / V_unit = s² / V_unit per unit (design effect); the
number of independent sampling units is stated as five regions. Verdict per unit: Q1, Q2 interval
excludes zero or not; Q3 excludes 0.5 or not. Report which verdicts change across units. The
Section 4.4 claim "under target-region clustering the +0.023 interval excludes zero" is re-derived.

## Task 4 — register and multiplicity (`ems_inference_multiplicity.py`)

**Register.** From `git log` of both worktrees / branches, the manuscript's own statements and any
pre-registration/protocol file: per arm, first dated appearance, whether it predates the first
cross-region result it could influence, planned or post hoc. Every analysis in this folder is post
hoc by construction (referee round, 2026-09-19).

**Reversal family (Holm, FWER 0.05).** Primary family R1 = 9 numeric features × 10 unordered region
pairs = 90 difference tests on the 10 km collar: signed univariate AUC per region, 10-cell
spatial-block bootstrap per region independently (`default_rng(42)` per region, skip single-class
replicates, difference of index-paired replicate vectors truncated to common length — exactly
`verify_matched_gap.py`), 20,000 replicates (the first 1,000 are the paper's draws; reproduction
of `matched_frame_gap.csv` and of the "nine of ninety" count at 1,000 is checked). p-values:
primary normal approximation z = difference / SD(replicate differences); secondary two-sided
percentile-bootstrap p = 2·min(P*(Δ ≤ 0), P*(Δ ≥ 0)) with floor 1/R. Holm over the 90; BH also
shown. Secondary families: R2 = the same 90 on the frame as drawn; R3 = the strict criterion as an
intersection–union test, p_pair = max(p_a, p_b) of the two regions' tests of AUC = 0.5 (normal
approximation), set to 1 when the point estimates are on the same side of 0.5, on both frames; Holm
over each 90.

**Diagnostic family (Benjamini–Hochberg, q = 0.05; q = 0.10 also shown).** The 19 computable rows
of `all_diagnostics_vs_transfer.csv` (the row "not computable" excluded). Spearman ρ recomputed
from the per-direction values in `regime_transfer_correlation.json`,
`conditional_similarity_transfer.json`, `niche_overlap_transfer.json` (reproduction against the
published ρ checked); unordered-pair cluster bootstrap, 20,000 replicates, seed 42; primary p =
2·min(P*(ρ* ≤ 0), P*(ρ* ≥ 0)), degenerate replicates dropped; secondary p = analytic Spearman p
under independence (anti-conservative given the dyadic dependence, shown only as a bound).
