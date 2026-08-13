# 4. Results

> **Drafting note.** Every number below is taken from the verified fact sheet
> (`facts_results.md`, extracted 2026-08-08 from the complete `drive_new/` export) or from the
> analysis reports in `paper/` (`all_diagnostics_vs_transfer`, `regime_transfer_correlation`,
> `conditional_similarity_transfer`, `loro_pooled_transfer`, `feature_drop_transfer`,
> `niche_overlap_transfer`, `niche_vs_conditional`, `sklearn_version_sensitivity`,
> `signed_auc_bootstrap`, `figure_contrast_pairs.csv`), or from the three verified reports of the
> 2026-08-13 referee round (`referee_round_numbers.md`, `transfer_ci_blocksize.md`,
> `diagnostics_common_subset.md`). Tables 3–6 follow the outline's reserved
> numbering; lettered tables (R1–R13) are additional and will be renumbered at assembly. All
> intervals are 95% spatial-block bootstrap percentile intervals (Section 3.9) unless stated
> otherwise; "CI-supported" means the interval excludes the reference value (zero for
> differences, 0.5 for transfer AUCs).

## 4.1 Study regions and data summary

Five Mediterranean regions enter the analysis (Section 3.1, Table 1). Table R1 summarises cell
counts, burned-cell counts and prevalence for both analysis populations, together with the
burned-landcover gate verdict of Section 3.3.

**Table R1. Region summary (recap of Table 1; final numbering at assembly).** Counts from each
region's Step 8A dataset statistics; gate fractions from each region's burned-landcover gate output.
TSG = the primary natural-vegetation population. The TSG columns use the canonical modelled
population, `burnable_tree_shrub_grass` **and** `valid_for_modeling == True`, which is the
population every model in this paper was fitted and scored on.

| Region | Total cells | Valid cells | Burned | Prevalence (all valid) | TSG cells | Burned in TSG | TSG prevalence | Burned natural-veg fraction | Gate verdict |
|---|---|---|---|---|---|---|---|---|---|
| Manavgat 2021 | 24,150 | 24,087 | 796 | 0.033 | 20,511 | 784 | 0.038 | 0.984 | pass |
| Bejís 2022 | 15,759 | 15,759 | 1,103 | 0.070 | 15,190 | 1,100 | 0.072 | 0.991 | pass |
| Muğla 2021 | 73,098 | 73,045 | 3,073 | 0.042 | 41,730 | 2,911 | 0.070 | 0.958 | pass |
| North Evia 2021 (extended) | 22,925 | 22,906 | 2,803 | 0.122 | 9,298 | 2,664 | 0.287 | 0.945 | pass |
| Montiferru 2021 | 3,234 | 3,173 | 748 | 0.236 | 2,544 | 539 | 0.212 | 0.723 | pass |

An earlier version of this table read its TSG columns from the Step 8A fields
`burnable_tree_shrub_grass_count` and `burned_count_within_each_burnable_mask`. Those are legacy
fields counted over all grid rows, before the `valid_for_modeling` filter, and Montiferru's own
statistics file labels the first of them "LEGACY field ... Do NOT report it as the modeling
population". The counts above are the post-filter ones
(`burnable_tree_shrub_grass_count_valid_for_modeling` and
`burned_count_within_primary_burnable_mask`), cross-checked against the `target_row_count` and
`target_burned_count` fields of the multi-AOI transfer matrix. The correction changes Manavgat,
Muğla, Evia and Montiferru, and moves Montiferru's TSG prevalence from 0.225 to 0.212. **No modelled
result changes.** Every model in this paper was already fitted and scored on the post-filter
population, so the correction is to the description of that population and not to any number derived
from it. Source: `paper/referee_round_numbers.md`, Tables A4 and A5.

All five regions pass the admissibility gate as wildfire candidates (burned natural-vegetation
fraction 0.723 to 0.991). Montiferru is the weakest pass, with a burned cropland fraction of 0.274;
its sensitivity to this composition is examined in Section 4.7b. The negative control behaves as
designed: in Kozan 2023 the gate classifies 542 burned cells as 0.017 natural vegetation and 0.983
cropland (533 of 542 burned cells cropland-dominant, 8 grassland, 1 tree cover), returning the
verdict *cropland-dominated control*, and the region is excluded from all modelling. The separation
is not marginal. The five admitted regions carry natural-vegetation fractions of 0.723 to 0.991
against the control's 0.017, so the 0.50 threshold falls in an empty interval rather than between
neighbouring cases. This establishes that the gate discriminates burned area produced by
natural-fuel combustion from burned area produced by post-harvest stubble burning, which MCD64A1
itself does not distinguish, and that admission of the five study regions is a decision the data
supports rather than a selection made by hand.

North Evia is analysed on an extended AOI. Relative to the legacy 0.40°×0.40° box, the extended
0.80°×0.60° box (~3× the area, identical predictor and label windows) leaves the burned scar
essentially unchanged (2,789 → 2,803 burned cells) while cutting overall prevalence from 0.361 to
0.122 and TSG prevalence from 0.676 to 0.287. The effect of this choice on transfer is reported in
Section 4.7a.

## 4.2 Within-region: the thermal increment replicates in five regions

In every region, adding the six thermal predictors to the baseline increases spatially
blocked out-of-fold ROC-AUC, and the increment's bootstrap interval excludes zero at every block
size tested (Table 3; [Fig. 3]).

**Table 3. Within-region baseline versus thermal performance and block-size robustness.** Primary
(TSG) population; spatially blocked 5-fold CV (Section 3.8); paired spatial-block bootstrap, 1000
replicates. Block sizes 2/10/20 cells ≈ 1/5/10 km.

| Region | Block (≈ scale) | Baseline AUC | Thermal AUC | ΔAUC | ΔAUC 95% CI |
|---|---|---|---|---|---|
| Manavgat 2021 | 2 (~1 km) | 0.803 | 0.870 | +0.067 | [+0.055, +0.079] |
| | 10 (~5 km) | 0.748 | 0.797 | +0.050 | [+0.023, +0.077] |
| | 20 (~10 km) | 0.683 | 0.731 | +0.048 | [+0.014, +0.085] |
| Bejís 2022 | 2 (~1 km) | 0.862 | 0.918 | +0.056 | [+0.048, +0.065] |
| | 10 (~5 km) | 0.779 | 0.825 | +0.045 | [+0.018, +0.069] |
| | 20 (~10 km) | 0.739 | 0.795 | +0.057 | [+0.031, +0.090] |
| Muğla 2021 | 2 (~1 km) | 0.743 | 0.859 | +0.116 | [+0.106, +0.125] |
| | 10 (~5 km) | 0.698 | 0.777 | +0.079 | [+0.050, +0.105] |
| | 20 (~10 km) | 0.673 | 0.733 | +0.061 | [+0.030, +0.094] |
| North Evia 2021 (ext.) | 2 (~1 km) | 0.759 | 0.912 | +0.153 | [+0.142, +0.166] |
| | 10 (~5 km) | 0.716 | 0.864 | +0.148 | [+0.119, +0.183] |
| | 20 (~10 km) | 0.679 | 0.833 | +0.154 | [+0.124, +0.189] |
| Montiferru 2021 | 2 (~1 km) | 0.781 | 0.883 | +0.101 | [+0.080, +0.125] |
| | 10 (~5 km) | 0.620 | 0.720 | +0.100 | [+0.017, +0.186] |
| | 20 (~10 km) | 0.555 | 0.681 | +0.126 | [+0.053, +0.228] |

*Table note (resampling units).* The bootstrap resamples spatial blocks, so what bounds an
interval's reliability is the number of blocks that carry at least one burned cell. Those counts
fall quickly as blocks coarsen. At 2 cells they are 235 (Manavgat), 302 (Bejís), 843 (Muğla), 716
(Evia) and 192 (Montiferru), out of 5 439, 3 967, 11 316, 2 566 and 743 blocks. At 10 cells they are
28, 19, 70, 41 and 16, out of 237, 176, 576, 155 and 35. At 20 cells they are **12, 6, 33, 15 and
6**, out of 60, 48, 167, 50 and 12. No bootstrap replicate was invalid at any block size. An
equal-tailed percentile interval built on six positive-carrying blocks has no meaningful coverage,
and Montiferru at 20 cells additionally feeds only 12 groups into a 5-fold grouped split, so its
models train on about ten blocks each. **The 20-cell row of this table should be read as indicative
rather than as an interval.** The 10-cell row, where every region has 16 to 70 positive-carrying
blocks, is the coarsest blocking this design supports properly, and the increment holds there in all
five regions. Source: `paper/referee2_numbers.md`, block C, counted from the frozen per-cell
prediction tables.

At the default 2-cell blocking, thermal ΔAUC ranges from +0.056 (Bejís) to +0.153 (Evia), with
ΔPR-AUC from +0.097 (Manavgat, [+0.071, +0.123]) to +0.300 (Evia, [+0.273, +0.329]). Every interval
excludes zero. Absolute AUC declines as blocks coarsen, as expected when long-range spatial
structure is progressively withheld, but the increment itself does not erode toward zero: at 20-cell
(~10 km) blocking ΔAUC remains between +0.048 and +0.154 with all intervals above zero. The same
holds in the secondary all-valid population (Section 4.7f).

## 4.3 Cross-region transfer

Transfer is evaluated for all 20 ordered directions among the five regions, as raw source-only
application and under the two label-blind adaptations of Section 3.11 (Table 4; [Fig. 4]).

**Table 4. Cross-region transfer matrix, thermal model, TSG population.** Target ROC-AUC with 2-cell
spatial-block bootstrap 95% CIs (1000 replicates). CORAL is applied after region-wise z-scoring (λ =
10⁻⁵).

| Direction | Raw | Region-wise z-score | CORAL |
|---|---|---|---|
| Manavgat→Bejís | 0.326 [0.305, 0.349] | 0.477 [0.451, 0.502] | 0.511 [0.484, 0.534] |
| Bejís→Manavgat | 0.444 [0.408, 0.480] | 0.457 [0.420, 0.497] | 0.555 [0.528, 0.583] |
| Manavgat→Muğla | 0.470 [0.451, 0.488] | 0.431 [0.411, 0.449] | 0.443 [0.423, 0.462] |
| Muğla→Manavgat | 0.401 [0.378, 0.426] | 0.559 [0.531, 0.587] | 0.560 [0.535, 0.587] |
| Manavgat→Evia | 0.613 [0.593, 0.631] | 0.542 [0.520, 0.565] | 0.539 [0.518, 0.561] |
| Evia→Manavgat | 0.686 [0.653, 0.716] | 0.516 [0.489, 0.544] | 0.527 [0.500, 0.553] |
| Bejís→Muğla | 0.618 [0.601, 0.635] | 0.518 [0.501, 0.535] | 0.507 [0.489, 0.524] |
| Muğla→Bejís | 0.583 [0.561, 0.607] | 0.535 [0.513, 0.557] | 0.560 [0.538, 0.581] |
| Bejís→Evia | 0.383 [0.363, 0.402] | 0.532 [0.509, 0.551] | 0.499 [0.479, 0.518] |
| Evia→Bejís | 0.448 [0.426, 0.470] | 0.550 [0.524, 0.575] | 0.549 [0.525, 0.574] |
| Muğla→Evia | 0.653 [0.636, 0.671] | 0.561 [0.543, 0.580] | 0.563 [0.545, 0.582] |
| Evia→Muğla | 0.577 [0.560, 0.593] | 0.501 [0.485, 0.518] | 0.530 [0.515, 0.546] |
| Montiferru→Manavgat | 0.567 [0.539, 0.594] | 0.573 [0.538, 0.609] | 0.606 [0.574, 0.639] |
| Manavgat→Montiferru | 0.533 [0.488, 0.580] | 0.586 [0.540, 0.629] | 0.592 [0.550, 0.631] |
| Montiferru→Bejís | 0.548 [0.521, 0.578] | 0.574 [0.552, 0.596] | 0.569 [0.548, 0.591] |
| Bejís→Montiferru | 0.594 [0.560, 0.631] | 0.550 [0.500, 0.601] | 0.574 [0.530, 0.621] |
| Montiferru→Muğla | 0.619 [0.604, 0.634] | 0.576 [0.562, 0.589] | 0.565 [0.550, 0.579] |
| Muğla→Montiferru | 0.531 [0.495, 0.568] | 0.587 [0.549, 0.624] | 0.584 [0.547, 0.623] |
| Montiferru→Evia | 0.586 [0.565, 0.606] | 0.630 [0.611, 0.649] | 0.624 [0.605, 0.641] |
| Evia→Montiferru | 0.647 [0.608, 0.682] | 0.568 [0.528, 0.609] | 0.582 [0.539, 0.624] |

**Raw transfer is heterogeneous and includes anti-predictive directions.** Raw target AUC spans
0.326 to 0.686. Twelve of 20 directions are above chance with CI support, six are *below* chance
with CI support (both directions of Manavgat↔Bejís and Manavgat↔Muğla, plus Bejís→Evia and
Evia→Bejís), and two intervals span 0.5. Even the best raw transfer (Evia→Manavgat, 0.686) remains
far below the target's own within-region thermal performance (0.870); across all directions the raw
deficit against the within-region reference is 0.184 to 0.592 AUC. Those counts belong to the 2-cell
blocking of Table 4. At the more conservative 10-cell (~5 km) blocking the same points give 9 above,
4 below and 7 uncertain, with no direction changing side of the chance line (Section 4.7g, Table
R13). Four of the six below-chance directions keep their support there: Manavgat→Bejís,
Muğla→Manavgat, Bejís→Evia and Evia→Bejís. Bejís→Manavgat and Manavgat→Muğla lose it and carry no
verdict. The qualitative statement is unchanged. The counts should not be read as exact.

**Precision-recall performance must be read against the target's own prevalence.** Prevalence varies
by a factor of about 7.5 across the five targets (0.038 to 0.287; Table R1), so a raw PR-AUC is
uninterpretable without its no-skill line. Table R11 gives raw thermal PR-AUC for all 20 directions
beside that line.

**Table R11. Raw transfer PR-AUC, thermal model, TSG population (final numbering at assembly).**
Target PR-AUC with bootstrap 95% CIs, against the target's own prevalence as the no-skill value.
Read from the multi-AOI transfer matrix
(`multi_aoi_transfer_matrix.csv`, `model_family = thermal`, `adaptation_method = raw_source_only`)
via `paper/referee_round_numbers.md`, Tables A2 and A4. The adapted arms exist in the same file and
are not reproduced here.

| Direction | No-skill | Raw PR-AUC [95% CI] | Direction | No-skill | Raw PR-AUC [95% CI] |
|---|---|---|---|---|---|
| Manavgat→Bejís | 0.072 | 0.049 [0.043, 0.055] | Muğla→Evia | 0.287 | 0.379 [0.350, 0.409] |
| Manavgat→Muğla | 0.070 | 0.063 [0.058, 0.068] | Muğla→Montiferru | 0.212 | 0.214 [0.182, 0.250] |
| Manavgat→Evia | 0.287 | 0.343 [0.318, 0.369] | Evia→Manavgat | 0.038 | 0.094 [0.076, 0.117] |
| Manavgat→Montiferru | 0.212 | 0.243 [0.202, 0.292] | Evia→Bejís | 0.072 | 0.059 [0.053, 0.067] |
| Bejís→Manavgat | 0.038 | 0.034 [0.029, 0.042] | Evia→Muğla | 0.070 | 0.086 [0.078, 0.093] |
| Bejís→Muğla | 0.070 | 0.093 [0.085, 0.102] | Evia→Montiferru | 0.212 | 0.283 [0.239, 0.331] |
| Bejís→Evia | 0.287 | 0.226 [0.209, 0.243] | Montiferru→Manavgat | 0.038 | 0.042 [0.036, 0.049] |
| Bejís→Montiferru | 0.212 | 0.289 [0.236, 0.349] | Montiferru→Bejís | 0.072 | 0.093 [0.077, 0.115] |
| Muğla→Manavgat | 0.038 | 0.029 [0.025, 0.033] | Montiferru→Muğla | 0.070 | 0.089 [0.082, 0.096] |
| Muğla→Bejís | 0.072 | 0.088 [0.077, 0.102] | Montiferru→Evia | 0.287 | 0.317 [0.293, 0.341] |

The raw thermal PR-AUC interval lies entirely above the target's prevalence in 11 of 20 directions,
entirely below it in 5, and straddles it in 4. This neither rescues nor destroys the transfer
picture. It does show that the two metrics do not always return the same verdict. Montiferru→Manavgat
is above chance on ROC-AUC at 2-cell blocking, yet its PR-AUC interval straddles the target
prevalence (0.042 [0.036, 0.049] against 0.038). Bejís→Manavgat is the same disagreement from the
other side, below chance on ROC-AUC at 2-cell blocking with a PR-AUC interval that straddles. Both
target Manavgat, the lowest-prevalence region in the set, and both lose their ROC-AUC verdict at
10-cell blocking (Section 4.7g). The PR-AUC intervals here are the 2-cell ones and were not
recomputed at the coarser blocking. The absolute values stay small wherever prevalence is small:
into the three low-prevalence targets (Manavgat, Bejís, Muğla) the best raw PR-AUC of any direction
is 0.094, so none of those directions ranks burned cells well enough for operational triage.

**The baseline itself transfers only a little above chance.** Over the 20 directions the
baseline model's mean raw transfer ROC-AUC is 0.5371, ranging from 0.3322 (Manavgat→Bejís) to 0.6758
(Evia→Manavgat), with four directions whose interval lies entirely below chance. The thermal model's
mean is 0.5414, ranging from 0.3258 to 0.6858, with six such directions. The mean paired delta is
+0.00424. Neither model family is portable in any useful sense. The mean gap between the two
families is +0.004, against a mean shortfall of about 0.35 AUC from within-region performance (mean
within 0.888 versus mean transfer 0.541; Table R4). Source: `paper/referee_round_numbers.md`,
Table A6, from `paper/baseline_vs_thermal_transfer.csv`.

That mean needs an interval, and its interval spans zero. The 20 directions are not 20 independent
observations. They are built from five datasets, so each region enters eight of the twenty terms,
and the two directions of a pair share geography, data and the same target prediction table. The
standard deviation of the 20 paired deltas is 0.0713. Resampling the 10 unordered pairs as clusters
gives a 95% interval of [−0.028, +0.036] around the mean of +0.004; a t interval on the 10 pair
means gives [−0.034, +0.042]; a leave-one-region-out jackknife on the five regions gives [−0.037,
+0.046]. Ignoring the clustering entirely gives [−0.027, +0.034], which is barely narrower, because
the width is set by the spread across directions rather than by the count. The pair-cluster interval
is the primary one. The point estimate is therefore a small fraction of the width of its own
interval, and the correct reading of +0.004 is not "a small positive contribution" but "no
contribution that this design can distinguish from zero, in either direction". Source:
`paper/referee2_numbers.md`, block A, computed from the paired deltas in
`paper/transfer_ci_blocksize.json` with 20 000 replicates and seed 42.

**The thermal block's transfer contribution is sign-unstable per direction.** Pairing each
direction's thermal model against the baseline model under the same protocol (Table R6) shows
that the block worth +0.056 to +0.153 AUC inside every region is worth +0.004 on average across
regions: its paired contribution is CI-supported positive in 10 directions, CI-supported negative in
7, and uncertain in 3. That split is the 2-cell one, and it should be read as approximate. At
10-cell blocking it becomes 5 to 6 positive, 3 to 4 negative and 10 to 11 uncertain, and even at
2-cell the boundary between 10 and 11 positive turns on a single bound of −0.00045 (Section 4.7g).
What does not depend on the blocking is the sign instability itself: 12 point deltas are positive
and 8 negative at both scales, and no point estimate changes sign. It is the swing factor at the
chance line. Adding the thermal block drags
three directions from a baseline at or above chance to below it (Manavgat→Muğla 0.508 → 0.470;
Bejís→Evia 0.531 → 0.383; Muğla→Manavgat 0.522 → 0.401) and lifts one from below to above
(Muğla→Bejís 0.451 → 0.583). In the Manavgat-Muğla pair the baseline transfers at roughly chance and
the thermal block pushes both directions below it; in the Bejís-Muğla pair the thermal block is what
carries transfer above chance in both directions.

**Table R6. Paired baseline-versus-thermal raw transfer contrast (final numbering at assembly).**
Target ROC-AUC per model; Δ = thermal − baseline computed on identical resampled target blocks
(2-cell blocks, 1000 replicates). Full 20-direction table with baseline and thermal CIs in
`baseline_vs_thermal_transfer.csv`. The seven CI-supported negative and ten CI-supported positive
directions are listed there. Selected rows:

| Direction | Baseline | Thermal | Δ [95% CI] | Support |
|---|---|---|---|---|
| Muğla→Bejís | 0.451 | 0.583 | +0.133 [+0.105, +0.158] | positive |
| Evia→Montiferru | 0.549 | 0.647 | +0.097 [+0.054, +0.138] | positive |
| Manavgat→Muğla | 0.508 | 0.470 | −0.038 [−0.051, −0.024] | negative |
| Muğla→Manavgat | 0.522 | 0.401 | −0.121 [−0.146, −0.098] | negative |
| Bejís→Evia | 0.531 | 0.383 | −0.148 [−0.168, −0.126] | negative |

**Label-blind adaptation compresses the matrix toward chance.** Under region-wise z-scoring the 20
directions span 0.431 to 0.630, and under CORAL 0.443 to 0.624. That is roughly half the raw spread,
with no adapted direction exceeding 0.63 against within-region references of 0.859 to 0.918.
Adaptation raises the failing directions (e.g. Manavgat→Bejís 0.326 → 0.511 CORAL; Muğla→Manavgat
0.401 → 0.560) and degrades most of the directions that already transferred (e.g. Evia→Manavgat
0.686 → 0.527 CORAL; Bejís→Muğla 0.618 → 0.518 z-score; Muğla→Evia 0.653 → 0.563). The degradation
is the majority case, not the universal one. Of the 12 directions whose raw interval lies above
chance, the better of the two adaptations lowers 9 and raises 3, and all three exceptions have
Montiferru as their source (Montiferru→Manavgat 0.567 → 0.606, Montiferru→Bejís 0.548 → 0.574,
Montiferru→Evia 0.586 → 0.630). Two further directions whose raw interval spans chance are also
raised, and both have Montiferru as their target. Inside the four-AOI subset that carries the
decomposition of Section 4.3a, which contains no Montiferru direction, all six above-chance
directions are degraded without exception. After the best adaptation per direction the maximum is
0.630 (Montiferru→Evia, z-score), whereas raw transfer reached 0.686, with three directions at or
above 0.647. The compression is therefore the general effect, and Montiferru, the smallest and
last-added region, is where it does not hold.

**Table 5. Transfer-gap decomposition (four-AOI set, 12 directions).** Within = target's
within-region thermal AUC; best adapted = the better of z-score/CORAL; recovered fraction = (adapted
− raw)/(within − raw), signed and unclipped, with paired bootstrap CI (1000 replicates). Montiferru
directions are not part of this decomposition (per-pair absolute decompositions exist without
fraction CIs). The status column asks whether the *adapted* value clears chance and uses the 2-cell
adapted intervals of Table 4. The adapted arms were not recomputed at the coarser blocking of
Section 4.7g, which covers the raw arm and the paired delta only.

| Direction | Within | Raw | Best adapted (method) | Recovered fraction [CI] | Status |
|---|---|---|---|---|---|
| Manavgat→Bejís | 0.918 | 0.326 | 0.511 (CORAL) | +0.31 [+0.28, +0.34] | recovery, chance not excluded |
| Bejís→Manavgat | 0.870 | 0.444 | 0.555 (CORAL) | +0.26 [+0.18, +0.34] | recovery above chance |
| Muğla→Manavgat | 0.870 | 0.401 | 0.560 (CORAL) | +0.34 [+0.28, +0.40] | recovery above chance |
| Bejís→Evia | 0.912 | 0.383 | 0.532 (z-score) | +0.28 [+0.23, +0.32] | recovery above chance |
| Evia→Bejís | 0.918 | 0.448 | 0.550 (z-score) | +0.22 [+0.16, +0.27] | recovery above chance |
| Manavgat→Muğla | 0.859 | 0.470 | 0.443 (CORAL) | −0.07 [−0.12, −0.03] | **negative recovery** |
| Muğla→Bejís | 0.918 | 0.583 | 0.560 (CORAL) | −0.07 [−0.16, +0.01] | **negative recovery** |
| Manavgat→Evia | 0.912 | 0.613 | 0.542 (z-score) | −0.23 [−0.32, −0.14] | **negative recovery** |
| Evia→Manavgat | 0.870 | 0.686 | 0.527 (CORAL) | −0.86 [−1.18, −0.60] | **negative recovery** |
| Evia→Muğla | 0.859 | 0.577 | 0.530 (CORAL) | −0.17 [−0.22, −0.11] | **negative recovery** |
| Muğla→Evia | 0.912 | 0.653 | 0.563 (CORAL) | −0.35 [−0.43, −0.27] | **negative recovery** |
| Bejís→Muğla | 0.859 | 0.618 | 0.518 (z-score) | −0.42 [−0.51, −0.34] | **negative recovery** |

The decomposition ([Fig. 5]) shows both faces of the same behaviour. In the five directions where
raw transfer was below chance, the best label-blind method recovers at most 34% of the gap to the
within-region reference. The remaining (concept) fraction is at least 0.66 everywhere. Seven
directions show *negative* recovery, meaning that adaptation moves the score away from the
within-region reference, in the worst case (Evia→Manavgat) recovering −0.86 of the gap. In six of
the seven, raw transfer was already above chance and adaptation destroyed that advantage; in the
seventh (Manavgat→Muğla), raw transfer was below chance (0.470) and adaptation lowered it further
(0.443). Label-blind adaptation therefore does not act as a repair mechanism: it compresses all
directions toward chance, closing a minority of the deficit where transfer fails and destroying
performance where transfer works.

## 4.4 Transferability diagnostics: only conditional similarity orders transfer

Twenty candidate diagnostics from four families were each rank-correlated with the same target
quantity. The families are marginal predictor-distribution measures P(x), burned-niche overlap
measures P(x|y=1), fire-regime (label-pattern) structure P(y), and conditional feature-response
direction P(y|x). Each was rank-correlated with the same target quantity, the raw thermal transfer
AUC over the 20 ordered directions, under a common pair-based bootstrap (Section 3.14.1). Table 6
gives the complete set.

**Table 6. All transferability diagnostics versus raw thermal transfer (20 ordered directions).**
Spearman ρ with pair-based bootstrap 95% CIs. Exp. = expected sign. Rows with n = 12 exist only for
the four-AOI subset. The supported-features conditional rows use the 16 directions (8 pairs) with at
least one CI-supported feature.

| Diagnostic | Family | Exp. | n dir | Spearman ρ [95% CI] | CI excludes 0 |
|---|---|---|---|---|---|
| **Agreement fraction, supported features** | **P(y\|x) conditional** | + | 16 | **+0.84 [+0.58, +0.88]** | **yes** |
| **Cosine, supported features** | **P(y\|x) conditional** | + | 16 | **+0.81 [+0.33, +0.88]** | **yes** |
| Cosine, all 9 features | P(y\|x) conditional | + | 20 | +0.50 [−0.17, +0.83] | no |
| Vector Spearman, all 9 | P(y\|x) conditional | + | 20 | +0.27 [−0.36, +0.77] | no |
| Agreement count, all 9 | P(y\|x) conditional | + | 20 | +0.18 [−0.40, +0.72] | no |
| Schoener's D, 1-D mean | P(x\|y=1) niche | + | 20 | +0.24 [−0.45, +0.74] | no |
| Warren's I, 1-D mean | P(x\|y=1) niche | + | 20 | +0.22 [−0.42, +0.73] | no |
| Schoener's D, PCA-2D | P(x\|y=1) niche | + | 20 | +0.10 [−0.51, +0.68] | no |
| Warren's I, PCA-2D | P(x\|y=1) niche | + | 20 | −0.07 [−0.66, +0.49] | no |
| Mahalanobis, burned centroids | P(x\|y=1) niche | − | 20 | −0.23 [−0.75, +0.44] | no |
| Domain-classifier AUC | P(x) marginal | − | 20 | −0.32 [−0.78, +0.33] | no |
| Predictor-space mean dissimilarity | P(x) marginal | − | 12 | −0.10 [−0.54, +0.43] | no |
| Predictor-space p95 dissimilarity | P(x) marginal | − | 12 | −0.08 [−0.59, +0.49] | no |
| Fraction inside weighted AoA | P(x) marginal | + | 12 | +0.22 [−0.48, +0.59] | no |
| Fraction inside unweighted support | P(x) marginal | + | 12 | +0.08 [−0.89, +0.63] | no |
| Climatic distance | P(x) marginal | − | 12 | +0.06 [−0.76, +0.79] | no |
| Geographic distance | geographic | − | 12 | −0.24 [−0.84, +0.73] | no |
| Regime distance, log effective-N | P(y) structure | − | 20 | +0.29 [−0.38, +0.74] | no |
| Regime distance, largest share | P(y) structure | − | 20 | +0.29 [−0.39, +0.72] | no |
| Vector Spearman, supported (≥3 feats) | P(y\|x) conditional | + | 2 | not computable | — |

*Table note (power): the effective sample is 10 unordered pairs (6 for the 12-direction rows; 8 for
the supported-conditional rows). The two directions of a pair are not independent and every pair
shares regions with three others. Intervals of width ±0.5 to 0.8 cannot rule out moderate true
correlations; null rows are "not shown to order transfer", not "shown not to".*

*Table note (count and provenance): twenty variants were specified and nineteen were computed. The
twentieth, vector Spearman over supported features, needs at least three jointly supported features
and only one pair reaches that threshold, so it rests on n = 2, every bootstrap replicate is
degenerate and no interval exists. It is listed so that the count of twenty is honest and it carries
no information either way. The six four-region rows exist in the published outputs under two seed
offsets of the same pair-based bootstrap, with identical data and identical point estimates; the
rows above quote the rendered `all_diagnostics_vs_transfer.md` variant, which is why the weighted-AoA
interval reads [−0.48, +0.59] here and [−0.50, +0.60] in the companion CSV. Nothing in the paper
depends on the difference.*

Of the 20 variants, exactly two have bootstrap intervals excluding zero, and both belong to the
conditional family: the sign-agreement fraction over CI-supported features (ρ = +0.84 [+0.58,
+0.88]) and the cosine similarity of supported signed-AUC vectors (ρ = +0.81 [+0.33, +0.88])
(Section 3.14.4). These indices are computed from signed feature-response directions in *both*
regions and therefore require burned labels (or a labelled probe) in the target. So do two of the
three families that fail. Burned-niche overlap is defined on the burned cells of both regions
(Section 3.14.3) and fire-regime structure on the target's burned map (Section 3.14.5), so both
consume the target's labels exactly as the conditional index does. Only the marginal P(x) family,
which includes the area-of-applicability rows, the domain classifier and the climatic and geographic
distances, is computable before any target label exists. That makes the comparison sharper rather
than weaker: niche overlap and the conditional index are built from the same labelled information
and only the conditional one orders the matrix. It also means the one family a practitioner could
run before deployment is the family that fails.

*How strong is the supported-conditional result?* It is the paper's one positive diagnostic finding
and it should be read at the size of the design that produced it. Three things bound it. First, the
index is nearly binary: over the 8 pairs on which it is defined it takes three distinct values (0,
0.5 and 1), and five of the eight pairs share the value 1. The tie structure caps the attainable
16-direction Spearman at +0.861, and the observed +0.840 therefore sits essentially on its own
ceiling, which is why the published interval is narrow. That narrowness reflects heavy ties under
pair resampling, not precision. Second, at the pair level, which is the unit the bootstrap
resamples, ρ = +0.866 with an exact one-sided permutation p of 0.0060 over all 40 320 permutations,
and 0.0060 is the *smallest* p this tie structure can produce. A Bonferroni threshold over the 19
computed variants is 0.0026, so no outcome of this diagnostic could have cleared a family-wise
correction on this pair set, whatever the data had been. The design has no headroom, which is a
stronger statement than the absence of a correction. Third, the restriction to CI-supported features
is a data-dependent selection made from the same bootstrap intervals, and it is executed once rather
than inside each replicate, so the published interval is conditional on a fixed selection rather
than propagating it. The unrestricted variant over all nine features reaches ρ = +0.50 with an
interval spanning zero (Table 6), so the restriction is what separates a positive result from a null
one. The finding stands as a mechanism diagnosis. It does not stand as a validated instrument.
Source: `paper/referee2_numbers.md`, block B.

The remaining families all fail to order the matrix. The domain classifier (Section 3.14.2) is at
ceiling for every pair (AUC 0.962 to 0.9999), so marginal shift is essentially total everywhere. A
marginal instrument at ceiling cannot discriminate outcomes ranging from 0.33 to 0.69. The canonical
SDM niche-overlap instruments (Schoener's D, Warren's I, Mahalanobis distance between burned-cell
distributions; Section 3.14.3) span ρ −0.23 to +0.24 with all intervals crossing zero. Fire-regime
structure (Section 3.14.5) has the *wrong-signed* point estimate (ρ +0.29): the most regime-similar
pair (Bejís-Evia, effective component count 1.0000 vs 1.0083) fails in both directions while the
most regime-different pair (Bejís-Muğla) transfers above chance. At pair level, niche overlap and
sign agreement are empirically distinct (ρ between them −0.36 to +0.45, all CIs spanning zero), and
in partial rank correlations the conditional index retains its association with transfer with niche
overlap held fixed (partial ρ +0.82 [+0.40, +0.88]) while niche overlap retains none with the
conditional index held fixed (−0.07 [−0.39, +0.37]).

*Common-subset check.* The rows of Table 6 rest on unequal samples (n = 12, 16 and 20), so a referee
may read the marginal family's failure as a power artefact. It is not. Recomputed on the common
12-direction, 6-pair four-region subset, on which every family is defined, the two
supported-conditional rows are still the only rows whose intervals exclude zero, and both are
slightly stronger there: ρ = +0.87 [+0.65, +0.88] for the agreement fraction and +0.85 [+0.43,
+0.88] for the cosine. All eighteen other rows span zero. The same holds on the 16-direction subset
for the eleven rows that can be moved onto it. In the same check all twenty published rows were
reproduced at their original sample size to a largest absolute difference of 4.8e-05, below the
rounding of the published four-decimal file. Source: `paper/diagnostics_common_subset.md`.

**A high applicability fraction does not protect a direction.** Table 6 asks whether the
area-of-applicability fraction *orders* transfer, and it does not. That is a separate question from
the one Sections 1 and 2 raise, which is whether a model can sit well inside its nominal area of
applicability and still perform at or below chance. That is a sufficiency claim, so a single pair
settles it. Table R12 gives the per-direction audit.

**Table R12. Area of applicability and raw thermal transfer, 12 directions (final numbering at
assembly).** Weighted AoA = fraction of target cells inside the importance-weighted area of
applicability; unweighted support = fraction inside the unweighted predictor-space support. Raw
thermal target ROC-AUC repeated from Table 4 with its 2-cell interval. The marginal audit exists
only for the four-region subset, so no Montiferru direction appears. Read from
`marginal_diagnostics_with_transfer.csv` via `paper/referee_round_numbers.md`, Table A1.

| Direction | Weighted AoA | Unweighted support | Raw thermal AUC [95% CI] |
|---|---|---|---|
| Manavgat→Muğla | **0.8752** | **0.9640** | 0.470 [0.451, 0.488] |
| Manavgat→Evia | 0.7444 | 0.9425 | 0.613 [0.593, 0.631] |
| Evia→Muğla | 0.6310 | 0.9590 | 0.577 [0.560, 0.593] |
| Muğla→Evia | 0.5810 | 0.9510 | 0.653 [0.636, 0.671] |
| Muğla→Manavgat | 0.5305 | 0.9702 | 0.401 [0.378, 0.426] |
| Evia→Manavgat | 0.4067 | 0.8995 | 0.686 [0.653, 0.716] |
| Manavgat→Bejís | 0.2646 | 0.9156 | 0.326 [0.305, 0.349] |
| Bejís→Manavgat | 0.2207 | 0.7486 | 0.444 [0.408, 0.480] |
| Bejís→Muğla | 0.1998 | 0.7638 | 0.618 [0.601, 0.635] |
| Bejís→Evia | 0.1705 | 0.6534 | 0.383 [0.363, 0.402] |
| Evia→Bejís | 0.0729 | 0.8562 | 0.448 [0.426, 0.470] |
| Muğla→Bejís | **0.0050** | 0.9076 | 0.583 [0.561, 0.607] |

The counterexample pair is at the top and the bottom of the table. Manavgat→Muğla carries the
highest weighted applicability of the twelve, 0.8752, and 0.9640 of target cells inside the
unweighted support, and it transfers at 0.470, below chance. Its reverse direction, at 0.5305
weighted and the highest unweighted value in the table, 0.9702, transfers at 0.401, also below
chance. Muğla→Bejís sits at the other extreme, with essentially no weighted applicability at 0.0050,
and transfers above chance at 0.583. Two of these three keep their verdict at both blocking scales:
Muğla→Manavgat stays below chance ([0.353, 0.455] at 10-cell) and Muğla→Bejís stays above it
([0.532, 0.636]). Manavgat→Muğla is supported below chance at 2-cell blocking only and carries no
verdict at 10-cell, [0.415, 0.524] (Section 4.7g). The three point estimates do not depend on the
blocking. A model may therefore be
almost wholly inside its nominal area of applicability and still be anti-predictive, and almost
wholly outside it and still work. This is the same sufficiency logic used for niche overlap in
Section 4.5, and it is stated as a counterexample pair rather than as a correlation. The correlation
question is answered separately and negatively in Table 6 (ρ = +0.22 [−0.48, +0.59] for the weighted
fraction, n = 12).

Two limits belong with this table. First, the two applicability quantities disagree sharply: the
unweighted support fraction is high everywhere (0.65 to 0.97) while the weighted fraction spans
almost the whole unit interval, so any claim about applicability must say which is meant. Second,
the marginal audit was produced only for the four-region subset. No area-of-applicability output
exists for Montiferru in any direction, so the eight Montiferru directions carry no applicability
number and none is implied for them here.

## 4.5 The contrast pair: highest niche overlap fails, lowest niche overlap works

The clearest single view of Table 6 is a two-pair contrast ([Fig. 8]; per-feature data
in `figure_contrast_pairs.csv`). [Production note: the OUTLINE slot reserved for signed univariate
AUC per feature with CIs is realised by Fig. 8, in two panels of per-feature signed AUC with ~5
km-block CIs, one per pair, annotated with the overlap and transfer numbers below.]

**Table R2. The contrast pairs (final numbering at assembly).**

| | Manavgat ~ Muğla | Bejís ~ Montiferru |
|---|---|---|
| Schoener's D̄ (1-D, 9 features) | **0.826** — highest of all 10 pairs | **0.479** — lowest of all 10 pairs |
| Mahalanobis (burned centroids) | 2.71 (closest) | 8.11 (farthest) |
| Sign agreement (9 features) | 4/9; jointly supported features 2 (agreement 1/2), with a CI-supported elevation flip | 7/9; no jointly supported features — the two regions' supported sets do not intersect (Montiferru CIs wide) |
| Raw transfer, both directions | 0.470 and 0.401 — **both below chance at the point estimate** | 0.594 and 0.548 — **both above chance at the point estimate** |
| Interval support, 2-cell (~1 km) | both supported: [0.451, 0.488] and [0.378, 0.426] | both supported: [0.560, 0.631] and [0.521, 0.578] |
| Interval support, 10-cell (~5 km) | Muğla→Manavgat still supported [0.353, 0.455]; Manavgat→Muğla no verdict [0.415, 0.524] | neither supported: [0.467, 0.687] and [0.479, 0.636] |

Manavgat and Muğla are in the same country and fire year, roughly 200 km apart, and their burned
cells occupy the most similar environmental envelope of any pair in the matrix (per-feature D 0.77
to 0.89). Yet five of nine feature-response directions point opposite ways. They are elevation
(signed AUC 0.374 [0.289, 0.471] in Manavgat vs 0.611 [0.532, 0.690] in Muğla, disjoint CIs) and all
four absolute thermal channels (e.g. `current_lst_mean` 0.538 [0.452, 0.621] vs 0.325 [0.271,
0.382]). Transfer is below chance in both directions at the point estimate, 0.470 and 0.401. Bejís
and Montiferru sit at the opposite extreme: burned envelopes that barely overlap (per-feature D 0.23
to 0.77; the pair is the most dissimilar on every overlap measure), yet seven of nine directions
agree. The pair has no jointly supported features, because the two regions' supported sets do not
intersect, so the supported-agreement index is undefined for it. Transfer is nevertheless above
chance in both directions at the point estimate, 0.594 and 0.548. Where the envelope agrees but the
direction reverses, transfer fails; where the envelope disagrees but the direction agrees, transfer
works.

The contrast is stated at the point estimate because the point estimate does not depend on the
blocking scale and the argument lives there. The interval support is weaker than the points and is
given in full in Table R2. At 2-cell blocking all four directions are supported. At the conservative
10-cell blocking of Section 4.7g only Muğla→Manavgat keeps its support, at [0.353, 0.455] below
chance; Manavgat→Muğla widens to [0.415, 0.524] and carries no verdict, and both Bejís-Montiferru
directions widen across 0.5 and carry no verdict either. No direction changes side of the chance
line at either blocking, so the reversal of ordering between the two pairs survives the coarser
bootstrap while the per-direction verdicts do not.

The marginal applicability audit points the same way for the half of the contrast it covers. Both
Manavgat-Muğla directions sit deep inside the nominal area of applicability, at 0.8752 and 0.5305 of
target cells inside the weighted region and 0.9640 and 0.9702 inside the unweighted support (Table
R12), and both transfer below chance at the point estimate, with Muğla→Manavgat supported at both
blockings and Manavgat→Muğla at 1 km only. The Bejís-Montiferru half cannot be given a matching
number, because the marginal audit was never produced for Montiferru. The contrast pair is therefore
complete on niche overlap and on sign agreement, and one-sided on applicability.

## 4.6 Interventions: pooling and feature removal obey the same conservation

Two interventions test whether the diagnosis of Sections 4.3 to 4.5 yields a remedy. Both show the
same pattern: what transfer gains, the within-region model or the direction-aligned pairs pay for.

**(a) Pooled multi-region training (leave-one-region-out).** Training on the pooled TSG populations
of four regions and testing on the held-out fifth (Section 3.15.1) does not rescue transfer (Table
R3).

**Table R3. LORO pooled training, thermal feature set, target ROC-AUC (final numbering at
assembly).**

| Held-out target | Best pairwise (source) | Mean pairwise | LORO raw | LORO region-z | Within (ceiling) |
|---|---|---|---|---|---|
| Manavgat | 0.686 (Evia) | 0.524 | 0.469 [0.412, 0.529] | 0.657 [0.543, 0.754] | 0.870 |
| Bejís | 0.583 (Muğla) | 0.476 | 0.417 [0.369, 0.467] | 0.472 [0.428, 0.516] | 0.918 |
| Muğla | 0.619 (Montiferru) | 0.571 | 0.552 [0.475, 0.625] | 0.522 [0.476, 0.569] | 0.859 |
| Evia (ext.) | 0.653 (Muğla) | 0.559 | 0.637 [0.592, 0.678] | 0.569 [0.520, 0.629] | 0.912 |
| Montiferru | 0.647 (Evia) | 0.576 | 0.601 [0.516, 0.683] | 0.523 [0.466, 0.570] | 0.883 |

At the point estimate the pooled thermal model never beats the best single-source pairwise transfer
for any target (shortfalls 0.02 to 0.22) and remains 0.28 to 0.50 AUC below the within-region
ceiling. For two targets (Manavgat, Bejís) the pooled model falls below the pairwise mean and below
chance, though only Bejís is below chance with interval support (0.417 [0.369, 0.467]); Manavgat's
0.469 is a point estimate whose interval [0.412, 0.529] spans 0.5. Region-wise z-scoring of the pool
raises only the into-Manavgat fold substantially (0.469 → 0.657) and leaves Bejís at 0.472 [0.428,
0.516], still below chance at the point estimate but no longer with interval support, while
degrading the three folds where raw pooling was least bad
(Evia 0.637 → 0.569; Montiferru 0.601 → 0.523; Muğla 0.552 → 0.522). Pooled PR-AUC sits close to its
no-skill base in the three low-prevalence folds (Manavgat 0.034 vs base 0.038; Bejís 0.056 vs 0.072;
Muğla 0.089 vs 0.070). In the two high-prevalence folds it sits about a quarter above the base in
relative terms (Evia 0.355 vs 0.287; Montiferru 0.265 vs 0.212), which is a real but small margin
and does not change the ROC picture. No fold achieves operationally useful ranking of burned cells.
For two of five targets the pooled *baseline* model beats the pooled thermal one raw (Manavgat 0.563
vs 0.469; Muğla 0.562 vs 0.552); for Montiferru the two are within 0.006 (0.596 vs 0.601); thermal
is ahead for Evia (0.637 vs 0.597) and Bejís (0.417 vs 0.389).

**(b) Dropping the direction-reversing features.** Retraining without the two features with
CI-supported reversals (`elevation_mean`; `lst_anomaly_mean`; Section 3.15.2) trades within-region
skill for a near-zero mean transfer gain (Table R4).

**Table R4. Feature-removal trade-off (final numbering at assembly).** Means over 5 regions (within,
TSG OOF) and 20 directions (transfer); paired ~5 km-block bootstrap for per-direction deltas. *Note:
the CI-supported above-chance counts in this table use the feature-drop analysis's ~5 km-block
bootstrap and are therefore more conservative than the 2-cell-block step10 intervals of Table 4,
under which 12 of 20 raw directions are CI-supported above chance. The coarser blocks widen the
intervals without changing any point estimate. Section 4.7g recomputes the Table 4 quantities at the
same ~5 km blocking and independently returns 9 of 20 above chance, so the two counts are the same
result at two blocking scales and not a disagreement.*

| Config | Mean within AUC | Mean transfer AUC | Directions >0.5 (point) | Directions >0.5 (CI-supported) |
|---|---|---|---|---|
| Full (reference) | **0.888** | 0.541 | 14 | 9 |
| Drop elevation | 0.827 | 0.546 | 17 | 9 |
| Drop lst_anomaly | 0.875 | 0.544 | 14 | 9 |
| Drop both | 0.807 | **0.556** | 17 | **10** |

Dropping both reversal features buys +0.014 mean transfer AUC and one additional CI-supported
above-chance direction at the price of −0.081 mean within-region AUC. The within-region cost of
removing elevation is bootstrap-supported in every region (largest Bejís −0.114 [−0.147, −0.079]).
The transfer deltas land exactly where the reversal diagnosis points: the three CI-supported gains
are Manavgat→Bejís +0.118 [+0.048, +0.203], Evia→Bejís +0.075 [+0.023, +0.131] and
Montiferru→Manavgat +0.057 [+0.017, +0.092]. The mean delta over the eight Manavgat-involved
directions is +0.025 against −0.009 over the other twelve. Manavgat is the elevation dissenter
(signed AUC 0.374 vs 0.61 to 0.65 elsewhere). Conversely, the five CI-supported losses
(Evia→Manavgat −0.078; Manavgat→Evia −0.071; Muğla→Evia −0.038; Montiferru→Bejís −0.036; Muğla→Bejís
−0.026) occur precisely where elevation's direction is shared and informative. `lst_anomaly` removal
contributes only in the pair where it reverses with support: Bejís→Evia (+0.046 alone; +0.063
[+0.026, +0.100] combined with elevation). Identifying which pairs cross a reversal requires the
target's signed directions, i.e. target labels; applied label-free, the same removal degrades the
five aligned directions.

## 4.7 Sensitivity analyses

**(a) Evia AOI and prevalence.** Repeating the raw transfer arms with the legacy (small, prevalence
0.361; TSG prevalence 0.676) versus extended (prevalence 0.122; TSG prevalence 0.287) Evia AOI
(Section 3.16.1) leaves every qualitative conclusion unchanged: thermal raw transfer AUCs move by at
most 0.070 (Evia→Bejís 0.378 → 0.448) and no direction changes side of chance (Manavgat→Evia 0.662 →
0.613; Evia→Manavgat 0.670 → 0.686; Bejís→Evia 0.397 → 0.383; Muğla→Evia 0.630 → 0.653; Evia→Muğla
0.572 → 0.577). The 2.4-fold change in target prevalence does not create or destroy any CI-supported
transfer.

**(b) Montiferru cropland fringe.** Within-region, excluding grassland (tree+shrub population)
leaves the thermal increment essentially unchanged: ΔAUC 0.104 [0.075, 0.131] versus 0.101 [0.080,
0.125] for TSG (Section 3.16.2). Cross-region, the thermal-minus-baseline delta on the target agrees
in sign and support between the two populations for six of eight Montiferru-involved directions. The
two disagreements (Bejís→Montiferru, Montiferru→Muğla) move from supported to uncertain, not to sign
reversal. Montiferru's transfer behaviour is not driven by its cropland/grassland fringe.

**(c) Window closure.** Shifting both ends of the predictor window earlier by 7 and 14 days (window
length preserved, fixed common cohort, shared folds; Section 3.16.3) leaves the within-region
thermal increment bootstrap-supported in every region and every variant (Table R5). Nowhere does the
increment shrink toward zero; in Manavgat and Bejís it increases with earlier closure. That increase
has a mechanism, and the window-closure report states it: the closure date is shifted against a
fixed production policy, so moving the window changes which acquisition dates enter the median
composite and how many clear observations back each pixel. With about seven usable dates in a
window, a 7 or 14 day shift is a change of one or two dates. The signature fits: across the same
comparison the baseline moves by +0.002 to +0.003 while the thermal family moves by +0.022 ROC-AUC,
so the shift acts almost entirely on the thermal channels, exactly as the compositing sensitivity of
(i) predicts. This does not weaken the pre-fire reading. Contamination by early fire signal would
push the increment the other way, and it does not appear. It does mean the increment is partly a
function of how the composite is built, which is the same conclusion (i) reaches from a different
direction.

**Table R5. Window-closure sensitivity: thermal ΔAUC (TSG common cohort; final numbering at
assembly).**

| Region | Canonical | Close 7 d | Close 14 d |
|---|---|---|---|
| Manavgat | 0.074 [0.062, 0.085] | 0.101 [0.088, 0.114] | 0.094 [0.078, 0.109] |
| Bejís | 0.058 [0.048, 0.068] | 0.077 [0.068, 0.088] | 0.079 [0.068, 0.090] |
| Muğla | 0.115 [0.105, 0.125] | 0.114 [0.104, 0.124] | 0.128 [0.118, 0.137] |
| Evia (ext.) | 0.156 [0.144, 0.170] | 0.149 [0.136, 0.162] | 0.135 [0.124, 0.147] |
| Montiferru | 0.096 [0.074, 0.118] | 0.091 [0.068, 0.113] | 0.100 [0.077, 0.122] |

**(d) CORAL regularisation.** The available sweep covers four directions (Bejís↔Muğla,
Manavgat↔Muğla) and nine λ values from 0 to 10⁻¹. Over that sweep the CORAL transfer AUC moves by at
most 0.008 within any direction (e.g. Muğla→Manavgat 0.559 to 0.564; Manavgat→Muğla 0.443 to 0.451).
No CORAL-dependent conclusion for these directions is sensitive to λ in this range. The sweep does
not cover λ = 1 or the Montiferru/Evia directions. It should be read for what it is. With nine
predictors and thousands of cells, a λ of 10⁻¹ is still far too small to bite on the covariance
estimate, so a movement of at most 0.008 across the range establishes numerical stability of the
alignment map rather than robustness to regularisation. The superseded two-region run, which did
include λ = 1, is the only evidence in this project about what heavy regularisation does, and there
it removed the effect (Section 3.11).

**(e) scikit-learn version.** With byte-identical data, pipeline and seed, changing only the library
version from 1.9.0 to 1.7.2 moves raw transfer AUC by +0.021 (Montiferru→Bejís) and +0.026
(Manavgat→Bejís) on the two probes tested, which is the same order as some reported effects.
Within-region AUCs, by contrast, reproduce to ~4 decimals across environments. All numbers in this
paper were produced under, or verified against, scikit-learn 1.9.0. The two probes reproduce to four
decimal places in the verification environment (difference 0.0000). Cross-region point estimates
therefore carry an implementation tolerance of roughly ±0.02 to 0.03 unless the exact library
version is fixed. The bootstrap intervals reported throughout are wider than this jitter.

**(f) Analysis population.** In the secondary all-valid population the within-region thermal
increment is CI-supported in all five regions, with smaller deltas than in the primary
natural-vegetation population for the three high-increment regions: ΔAUC 0.059 [0.049, 0.068]
(Manavgat), 0.048 [0.040, 0.057] (Bejís), 0.072 [0.067, 0.078] (Muğla), 0.053 [0.049, 0.058] (Evia),
0.075 [0.057, 0.094] (Montiferru), against TSG values of 0.067, 0.056, 0.116, 0.153 and 0.101
respectively. Absolute AUCs are higher in the mixed population (baseline 0.827 to 0.910), consistent
with land-cover composition contributing separable but non-thermal discrimination; the within-region
conclusion does not depend on the population choice.

**(g) Blocking scale of the transfer intervals.** Table 4 and Table R6 report 2-cell (~1 km) blocks,
while Section 3.12 argues that 2-cell blocking ignores short-range spatial autocorrelation and gives
intervals that are too narrow. The transfer quantities were therefore recomputed at 10-cell (~5 km)
blocking from the frozen per-cell predictions, with the resampling rule copied from the published
code, 1000 replicates and seed 42. The implementation was validated first: point estimates reproduce
the frozen values to 1.1e-16, the recomputed 2-cell bounds match the published ones to a mean
absolute difference of about 0.001 and a worst single case of 0.0055, and all 20 verdicts agree at
2-cell. Point estimates do not depend on the blocking and none of them moves. The recomputation
covers the raw thermal arm and the paired delta only; the z-score and CORAL columns of Table 4 were
not repeated at the coarser blocking. Source: `paper/transfer_ci_blocksize.md`.

**Table R13. Transfer verdict counts at two blocking scales (final numbering at assembly).** Level =
raw thermal transfer ROC-AUC against chance (Table 4). Delta = paired thermal-minus-baseline
contribution against zero (Table R6). Twenty directions in each row.

| Quantity | Blocking | Supported one way | Supported the other | Uncertain |
|---|---|---|---|---|
| Level, versus chance | 2-cell (~1 km), published | 12 above | 6 below | 2 |
| Level, versus chance | 10-cell (~5 km) | 9 above | 4 below | 7 |
| Delta, versus zero | 2-cell (~1 km), published | 10 positive | 7 negative | 3 |
| Delta, versus zero | 10-cell (~5 km) | 6 positive | 4 negative | 10 |

Leading with the conservative blocking: 9 of 20 directions are above chance with CI support, 4 are
below chance with CI support, and 7 carry no verdict. For the paired delta, 6 directions are
CI-supported positive, 4 CI-supported negative and 10 uncertain. Five directions change verdict on
the level and seven on the delta, and every one of those changes runs from supported to uncertain.
No direction moves the other way, from uncertain to supported. Intervals widen by a factor of 2.1 to 3.6 (median 2.8) for the levels and 1.5 to 3.4 (median 2.3)
for the deltas. The "roughly four times too narrow" figure of Section 3.12 belongs to the univariate
reversal diagnostic and is not the right number for these intervals.

**The robust statement is the one that matters.** No direction changes side of the chance line and
no point estimate changes sign. The point deltas still run from −0.148 to +0.132, with 12 positive
and 8 negative at both blockings, and the below-chance directions stay far from 0.5 (Manavgat→Bejís
[0.266, 0.388] at 10-cell). The pattern is therefore robust to the blocking choice; the exact counts
are not.

The counts should accordingly be read as approximate, because a seed sweep over five random streams
moves several verdicts. On the level, the above-chance count is 9 at every seed and the below-chance
count is 3 or 4, with Evia→Bejís on the boundary (its 10-cell upper bound lands between 0.497 and
0.504 across seeds), so that direction is better described as at the chance line than below it. On
the delta, the honest 10-cell statement is 5 to 6 positive, 3 to 4 negative and 10 to 11 uncertain,
with Manavgat→Muğla and Evia→Montiferru on the boundary. The published 2-cell delta split of 10, 7
and 3 is itself decided by one bound: Bejís→Manavgat has a lower bound of −0.00045, and a different
random stream gives 11 positive, 7 negative and 2 uncertain. Four directions in total should never
be quoted as though their verdict were firm: Bejís→Manavgat at 2-cell on the delta, Manavgat→Muğla
and Evia→Montiferru at 10-cell on the delta, and Evia→Bejís at 10-cell on the level.

**(h) Which thermal channel carries the increment.** The thermal block is six predictors, but they
are not six independent measurements. `fused_lst` equals the observed Landsat LST wherever that is
valid, and the gap-filled share is 2.15% (Manavgat), 9.70% (Bejís), 0.59% (Muğla), 0.90% (Evia) and
0.11% (Montiferru), so outside Bejís the two channels are near-copies of each other; Table R8 shows
the consequence directly, with signed univariate AUCs of 0.325 versus 0.325 in one arm and 0.515
versus 0.519 in the other. `downscaled_lst` is a fitted surface whose dominant input differs by
region: the MODIS context layer in Manavgat (importance 0.525) and Evia (0.593), NDVI in Bejís
(0.482) and Montiferru (0.666), and **slope in Muğla (0.777)**, where it is largely a re-expression
of a predictor the baseline already contains. The pipeline's Step 8D ablation, run on the primary
population with the same folds, quantifies the redundancy: a single subgroup recovers most of the
whole block's increment in every region.

**Table R14. Thermal-block ablation, primary population, ΔAUC against the baseline (final numbering
at assembly).** Source: `drive_new/experiments/<region>/step8d/step8d_ablation_delta_auc_by_population.csv`.

| Region | Full thermal block | Best subgroup | Its ΔAUC | Share of the full block |
|---|---|---|---|---|
| Manavgat | +0.067 | TVDI pair | +0.065 | 96% |
| Bejís | +0.056 | fused + downscaled | +0.040 | 71% |
| Muğla | +0.116 | TVDI pair | +0.089 | 77% |
| Evia (ext.) | +0.153 | LST anomaly | +0.125 | 81% |
| Montiferru | +0.101 | TVDI pair | +0.100 | 99% |

The dryness pair (`current_tvdi_mean`, `tvdi_difference_mean`) is the best subgroup in three of five
regions and recovers 96% and 99% of the full block in Manavgat and Montiferru. This matters twice.
It converts "the thermal block" from an opaque bundle into a statement about which physical quantity
carries the increment, and it means the six reversal tests of Section 4.4 are not six independent
probes of concept shift. Source: `paper/referee2_numbers.md`, blocks D, E and F.

**(i) Landsat compositing.** The current-period LST composite is a median over the clear
acquisitions inside the predictor window, and how those acquisitions are weighted is a choice. Three
controlled chains exist for Manavgat, on an identical cohort with identical folds and an identical
baseline, differing only in that raster: the production scene-weighted reference gives ΔAUC +0.064
[+0.052, +0.075], a date-balanced variant gives +0.084 [+0.072, +0.098], and an overlap-harmonised
date-balanced variant gives +0.045 [+0.033, +0.057]. The baseline AUC is identical to six decimal
places across all three (0.804362), so the entire spread sits in the thermal block, and both paired
comparisons against the production chain have intervals excluding zero (+0.021 [+0.012, +0.031] and
−0.040 [−0.050, −0.029]). The mechanism is documented in the same export: at boundaries where the
number of contributing clear acquisitions changes, the residual seam analysis finds excess jumps of
0.850 °C [0.812, 0.890] in the current-minus-baseline field and 0.526 °C [0.503, 0.551] in the
anomaly z-score, with the final attribution `current_support_dominant`. Manavgat's window is backed
by seven acquisition dates from two alternating Landsat paths, so a cell inside the path overlap
rests on seven dates and a cell outside it on three or four.

Two limits on this axis are stated by the source reports themselves and are adopted here: the A/B
was run for one AOI only, the alternative chains are candidates rather than production, and no
non-inferiority claim is made for them. The conclusion drawn here is correspondingly narrow. **The
within-region increment carries a compositing tolerance of roughly ±0.02 AUC, which is the same
order as the scikit-learn tolerance of (e) and wider than the 2-cell interval of Table 3.** It does
not approach the increment itself, which stays bootstrap-supported and positive under all three
chains. It has been audited in one region, and the other four are unaudited on this axis.

## 4.8 The same geography, a second fire: direction reversal with place held constant

Every result above compares different places. Muğla admits a stricter test, because a second fire
event occurred inside the identical AOI on the identical analysis grid (Section 3.16.4): the 2021
event, with its 58-day predictor window closing on 28 July, and the 2022 event, whose matched 58-day
window closes on 20 June. Region, bounding box, cell definition, feature registry and processing
chain are the same; only the event differs. The comparison is therefore same-geography
event-to-event, not clean temporal transfer. The 2022 fire ignites about five weeks earlier in the
season, so year and seasonal phase are confounded (Section 3.16.4). Geography, the explanation most
often offered for between-region instability, is held fixed by construction. The second Muğla event
is deliberately kept out of the 20-direction matrix of Section 4.3, and that exclusion is enforced
and tested in the released code rather than merely asserted here. The check that carries the
guarantee is `A08_cohort_is_the_frozen_five`, which compares the executed cohort against the frozen
`DEFAULT_EXPERIMENTS` tuple as an ordered equality, so any addition fails it. The neighbouring check
`A07_mugla_2022_absent_from_default_analysis` is narrower than its name suggests: it tests literal
membership of the string `mugla_2022` and would not by itself catch the `mugla_2022_event_relative`
entry analysed here. Both pass on the executed diagnostic output, but the guarantee rests on A08
(Sections 3.16.4, 3.17).

The two events are structurally very different fires. Table R7 reports the burned-pattern comparison
on the primary population.

**Table R7. Burned-pattern structure of the two Muğla events.** Primary population
(`burnable_tree_shrub_grass` ∧ `valid_for_modeling`), 8-connectivity components (Section 3.14.5).
Read from `paper/mugla_temporal_raw/.../multi_aoi_burned_pattern_comparison.csv`.

| Quantity | Muğla 2021 | Muğla 2022 |
|---|---|---|
| Burned cells | 2,911 | 331 |
| Connected components | 10 | 2 |
| Largest component (cells, share) | 914 (31.4 %) | 282 (85.2 %) |
| Second component (cells, share) | 738 (25.4 %) | 49 (14.8 %) |
| Effective component count | 4.054 | 1.337 |
| Component size, median | 22.5 | 165.5 |
| Elevation, median | 563 m | 187 m |
| Elevation, q95 | 1,526 m | 437 m |
| Elevation, maximum | 1,975 m | 777 m |
| Land-cover classes observed | 7 | 2 |
| Dominant class (share) | tree cover (0.925) | tree cover (0.979) |

The 2021 season burned as a dispersed multi-fire complex, with ten components, an effective count of
4.05 and no single component holding a third of the area. It spanned the region's full relief from
near sea level to 1,975 m. The 2022 event is one compact scar: two components, an effective count of
1.34, 85.2 % of burned cells in the largest, and confined to the low belt. Its highest burned cell
lies at 777 m, below the 2021 event's 95th percentile of 1,526 m, and its median elevation of 187 m
is a third of 2021's 563 m. The two fires occupy different parts of the same elevation gradient.

That difference propagates directly into the feature-label relationship. Table R8 gives the signed
univariate AUCs.

**Table R8. Signed univariate feature-burned AUC, Muğla 2021 versus 2022.** Raw AUC against
`burned`, never folded to max(AUC, 1 − AUC); 10-cell (≈ 5 km) spatial-block bootstrap, 1,000
replicates, seed 42 (Section 3.16.4). Analysis population 41,730 rows / 2,911 burned (2021) and
38,790 rows / 331 burned (2022). Read from
`paper/step9g_raw/.../mugla_2021__mugla_2022_event_relative/step9g_direction_reversal_table.csv`.

| Feature | 2021 AUC [95 % CI] | 2022 AUC [95 % CI] | Reversal |
|---|---|---|---|
| **elevation_mean** | **0.611 [0.532, 0.690]** | **0.296 [0.230, 0.355]** | **bootstrap-supported** |
| current_lst_mean | 0.325 [0.271, 0.382] | 0.515 [0.434, 0.580] | point only |
| current_tvdi_mean | 0.336 [0.275, 0.398] | 0.594 [0.475, 0.674] | point only |
| downscaled_lst_mean | 0.307 [0.253, 0.366] | 0.508 [0.435, 0.571] | point only |
| fused_lst_mean | 0.325 [0.272, 0.383] | 0.519 [0.436, 0.583] | point only |
| ndvi_mean | 0.662 [0.616, 0.704] | 0.707 [0.624, 0.777] | none |
| slope_mean | 0.637 [0.582, 0.686] | 0.558 [0.468, 0.634] | none |
| lst_anomaly_mean | 0.485 [0.395, 0.566] | 0.380 [0.249, 0.502] | none |
| tvdi_difference_mean | 0.490 [0.396, 0.575] | 0.397 [0.265, 0.514] | none |

Elevation reverses with bootstrap support. In 2021 higher cells burn preferentially (AUC 0.611,
interval entirely above 0.5); in 2022 lower cells do (0.296, interval entirely below), and the two
intervals are disjoint, 0.532 against 0.355, with the difference at −0.317 [−0.414, −0.220]. The
same predictor, the same region, the same grid, and an association that points the opposite way in
two fires eleven months apart.

The four absolute thermal channels also change side, from bootstrap-supported *lower*-values-burn in
2021 to *higher*-values-burn point estimates in 2022, and each AUC difference is itself
interval-supported (for example current_lst +0.188 [+0.084, +0.272]). **These reversals are
nonetheless not bootstrap-supported and are not claimed as such.** With 331 burned cells the 2022
intervals are wide, and all four straddle 0.5 (current_lst [0.434, 0.580]), so the 2022 direction is
not established even though the shift from 2021 is. We follow the diagnostic's own conservative
classification: one bootstrap-supported reversal, elevation; four point-level reversals in the
thermal block. The two anomaly-referenced channels and the two remaining static predictors do not
reverse at all, and NDVI keeps a bootstrap-supported positive direction in both events.

Transfer between the two events behaves unlike any between-region direction in the matrix, and it
does so asymmetrically (Table R9). Both directions stay *above* chance, with thermal intervals of
[0.513, 0.604] and [0.654, 0.685], neither touching 0.5. Those intervals use 5 km blocking, and at
that blocking four of the twenty between-region directions fall below chance with interval support,
six at the 1 km blocking of Table 4 (Sections 4.3, 4.7g). Holding geography fixed removes the
collapse.

**Table R9. Transfer between the two Muğla events.** Primary population, thermal and baseline
models, target ROC-AUC with 5 km spatial-block bootstrap 95 % CIs (Section 3.16.4). Within-region
references are each target's own frozen value at 2-cell blocking (Table 3 for 2021; the 2022 figure
is its Step 8C point estimate, ΔAUC +0.078 [+0.061, +0.097]). The baseline and thermal columns are
point estimates on the full target. The ΔAUC column is the bootstrap mean reported alongside its
interval, so it differs from the difference of the two point estimates in the third decimal (point
ΔAUC −0.083 and +0.088 respectively). Both arms of this pair were reproduced independently by the
pipeline author to ≤1×10⁻⁷ (Section 3.16.4).

| Direction | Baseline | Thermal | ΔAUC (thermal − baseline) | Target's within-region thermal | Gap |
|---|---|---|---|---|---|
| Muğla 2021 → 2022 | 0.642 [0.606, 0.674] | 0.559 [0.513, 0.604] | **−0.082 [−0.127, −0.040]** | 0.942 | 0.383 |
| Muğla 2022 → 2021 | 0.581 [0.566, 0.598] | 0.670 [0.654, 0.685] | **+0.089 [+0.072, +0.104]** | 0.859 | 0.189 |

What does not survive is the thermal block's contribution, and its failure here is sharper than
anywhere else in the paper: **the same six predictors change the sign of their contribution
depending on which event is the source, and both signs are interval-supported.** Carried forward
from 2021 to 2022 they cost 0.082 AUC; carried back from 2022 to 2021 they buy 0.089. This is not a
case of a weak signal failing to travel. Within each event separately the thermal block helps and
its interval excludes zero, at +0.116 in 2021 (Table 3) and +0.078 in 2022. The block is therefore
locally informative in both, and still actively harmful in one direction between them.

The asymmetry follows the elevation reversal. A model fitted on 2021 learned a relationship whose
strongest static term points the wrong way for a fire confined below 777 m, and the thermal channels
it learned alongside that term were fitted under the same regime; applied to 2022 they subtract
skill from a baseline that already transfers at 0.642. In the reverse direction the 2022 model
carries a relationship fitted on a narrow low-elevation slice, which the broader 2021 event
contains, and there the thermal block adds. The residual gap to the target's own within-region
performance remains large in both directions, at 0.383 and 0.189, so nothing here rescues transfer;
what it shows is that the direction of the thermal block's contribution is not a property of the
predictors but of the pair.

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

## 4.10 What target labels cost: the recovery curve

Everything above measures a failure. This section prices it. If the residual gap is conditional, and
label-free alignment cannot close it, then the missing resource is target-conditional information,
and the direct way to supply it is target labels. The question is how many.

The frozen few-shot diagnostic answers it for three regions in all six ordered directions (Manavgat,
Bejís and Muğla; Evia and Montiferru are absent from that export). The unit of labelling effort is
one 10-cell (≈ 5 km) spatial block, which is the same large-block machinery used for the
conservative intervals of Section 4.7g and a plausible unit of survey effort. Budgets are 0, 1, 2,
4, 8, 16 and 32 blocks, nested, drawn under a fixed tier order with a seed derived from the
direction and fold and independent of any result. Each budget is repeated ten times with different
draws. The ceiling is the target-only model under the same folds and the same blocking, so recovery
fractions are read against a matched ceiling of 0.777 to 0.824 rather than against the ≈ 1 km
within-region values of Table 3. The interval quoted in the supplement is a selection interval
across repeats, not a bootstrap. The full design, the per-budget table and seven stated limits are
Supplementary S1.

**Thirty-two labelled blocks recover 85 to 89 % of the target ceiling in four of the six
directions**, from starting points at or below chance: Manavgat→Bejís 0.326 → 0.772 against a
ceiling of 0.824, Muğla→Bejís 0.583 → 0.789, Bejís→Manavgat 0.444 → 0.743 against 0.797, and
Manavgat→Muğla and Muğla→Manavgat reaching 51 and 57 %. The failure this paper documents is
therefore expensive rather than structural. It is a shortage of target-conditional information, and
target labels are exactly that.

Two qualifications belong with that number and neither is small. **That budget is not modest.**
Thirty-two blocks carry 2 700 to 3 000 labelled cells, 7 to 20 % of the target's natural-vegetation
population, and for Bejís the top budget already contains 880 of the region's 1 100 burned cells.
The narrow selection intervals at the largest budgets reflect a nearly exhausted selection pool
rather than a well-estimated quantity (Supplementary S1, limit 4). **And a small budget hurts the
one direction that already works.** Bejís→Muğla transfers above chance raw (0.618) and is the
direction few-shot recalibration helps least: the curve is negative at 1, 2, 4 and 8 blocks (−0.043
to −0.021 AUC), only overtakes raw at 16 blocks, and reaches 30 % at 32, the worst of the six. This
is the same asymmetry that label-blind adaptation shows in Section 4.3, arrived at by a different
route: where a source model already carries a usable conditional relationship, a small target sample
perturbs it before it can replace it.

No label budget is proposed here. Six directions across three regions cannot support a
recommendation, and the recovery curve is a price list for the specific AOIs measured, not a design
rule. What it establishes is the shape of the cost: recovery is achievable, it is slowest where the
concept gap is widest, and at small budgets it is not free.

<!-- DRAFT NOTES:

(a) CLOSED 2026-08-13. The [PENDING] added 2026-08-11 in §4.8 read: "the Muğla 2021 ↔ 2022
    transfer AUCs do not exist yet (no such pair in drive_new/cross_region/)". They were then
    computed for this analysis (§3.16.4) and now appear in Table R9. On 2026-08-13 the pipeline
    author supplied his OWN earlier run of the same two arms (produced 2026-08-09, commit
    a07ea33, pandas 3.0.2 / numpy 2.4.4 against our pandas 3.0.5 / numpy 2.5.2, same
    scikit-learn 1.9.0, same input hashes): every point metric and bootstrap bound agrees to
    <=1e-7 and the step9b/step9c summary .md files are byte-identical. Archived at
    paper/mugla_transfer_raw/emrehan_run_20260809/ with SHA256SUMS.txt. Table R9 caption also
    gained a note that its delta column is the bootstrap mean, not the difference of the two
    point estimates. Every number that IS in this draft traces
    to facts_results.md, a paper/ analysis report, or — for §4.8 and §4.9, added 2026-08-11 —
    directly to hashed raw files under paper/mugla_temporal_raw/, paper/step9g_raw/ and
    paper/era5_raw/. Those three sources are outside the facts_results.md extraction and were
    each read from source and hash-verified; see 05_discussion DRAFT NOTES (a)5 and (a)7.

(b) METHODS GAPS — ALL 11 RESOLVED 2026-08-08: described in 03_methods §3.14.1–.5, §3.15.1–.2,
    §3.16.1–.3 and the §3.1 Table 1 update; inline [METHODS GAP] markers in this file replaced
    with the real section references. Mapping in 03_methods' METHODS ROUND NOTES comment.
    Original list retained below for the record:
    1. §4.1 — 03_methods §3.1 Table 1 lists four regions with the LEGACY Evia AOI
       (23.12, 38.68, 23.52, 39.08); must add Montiferru 2021 and the extended Evia AOI
       (23.05, 38.55, 23.85, 39.15) and update Table 1b counts (now available, Table R1).
    2. §4.4 — diagnostic-vs-transfer rank-correlation framework (pair-based bootstrap, both
       directions carried, 2000 replicates, seed 42, percentile CI) not in Methods.
    3. §4.4 — conditional sign-agreement / cosine indices over signed univariate AUC vectors,
       incl. the supported-feature restriction (both regions' CIs exclude 0.5).
    4. §4.4 — domain-classifier audit (source-vs-target spatial-block OOF AUC).
    5. §4.4 — niche-overlap measures (Schoener's D, Warren's I, 1-D shared bins, PCA-2D,
       Mahalanobis on burned centroids).
    6. §4.4 — fire-regime structure metrics (8-connectivity components, effective component
       count, largest-component share, regime distance).
    7. §4.6a — LORO pooled-training protocol.
    8. §4.6b — feature-drop configurations and parity checks.
    9. §4.7a — legacy-vs-extended Evia AOI sensitivity design.
    10. §4.7b — tree+shrub population variant (Montiferru cropland sensitivity).
    11. §4.7c — window-closure sensitivity design (both ends shifted earlier, length preserved,
        common cohort, shared folds).

(c) CONFLICTS between sources (both values kept out of the text where unresolved; the drafted
    text uses the drive_new/facts_results.md value in each case):
    1. Raw-transfer directions above chance with CI support: 12/20 under the step10 2-cell-block
       CIs (facts_results.md §5, drive_new/cross_region/<pair>/step10/) vs 9/20 under the
       feature-drop analysis's ~5 km-block paired bootstrap (paper/feature_drop_transfer.md,
       trade-off table). Not numerically contradictory (different bootstrap block sizes) but the
       two counts appear in §4.3 vs Table R4 — RESOLVED during coordinator review: reconciling
       footnote added to the Table R4 caption (coarser blocks widen intervals, points unchanged).
       FULLY CLOSED 2026-08-13: paper/transfer_ci_blocksize.md recomputes the Table 4 quantities
       at both blockings from the frozen per-cell predictions and returns 12/6/2 at 2-cell and
       9/4/7 at 10-cell, direction by direction. The 9 is now sourced rather than inherited from
       the feature-drop table. Both counts are reported in §4.7g (Table R13) with the 10-cell one
       leading, and the Table R4 footnote now says the two are one result at two scales.
    2. CLAUDE.md two-region step10 numbers vs drive_new (post-Manavgat-repair) step10:
       e.g. Manavgat→Bejís raw 0.3245 (CLAUDE.md) vs 0.3258 (facts §5); CORAL 0.5108 vs 0.5105;
       Bejís→Manavgat raw 0.4444 vs 0.4435, z 0.4520 vs 0.4573, CORAL 0.5571 vs 0.5553.
       Draft uses drive_new values throughout.
    3. CORAL λ sweep — RESOLVED 2026-08-08 during coordinator review: §3.11's sweep paragraph
       was amended to the actual drive_new coverage (4 directions Bejís↔Muğla + Manavgat↔Muğla,
       nine-value grid 0…1e-1, spread ≤0.008, no λ=1, Montiferru/Evia directions rest on the
       default λ=1e-5 alone). RE-CHECK this paragraph in the Methods-update round alongside the
       11 METHODS GAPS.
    4. Burned-in-TSG counts: step8a stats (facts §1: Muğla 2952, Evia 2675, Montiferru 582) vs
       analysis population TSG∧valid (regime/niche/signed-AUC reports: 2911, 2664, 539; Manavgat
       784 and Bejís 1100 agree). Table R1 used step8a counts; the §4.4/§4.5 analyses use the
       TSG∧valid counts. RESOLVED 2026-08-13, not deferred to assembly: the legacy fields were
       the wrong ones to print. Montiferru's own step8a_dataset_stats.json says of
       burnable_tree_shrub_grass_count, verbatim, "LEGACY field: counted over ALL grid rows,
       including valid_for_modeling == False ... Do NOT report it as the modeling population",
       and names burnable_tree_shrub_grass AND valid_for_modeling == True as the canonical
       downstream population. Table R1's TSG columns now carry the post-filter counts, verified
       three ways: burnable_tree_shrub_grass_count_valid_for_modeling (Montiferru only),
       burned_count_within_primary_burnable_mask (all five), and target_row_count /
       target_burned_count in the multi-AOI transfer matrix (all five). Montiferru TSG prevalence
       0.225 -> 0.212. No modelled number moves; the models were always fitted on the corrected
       population.
       NOTE for assembly: the task brief for this round stated that "Manavgat and Bejís are
       already correct". That holds for the BURNED counts (784, 1100) but not for Manavgat's CELL
       count, which was 20,555 legacy against 20,511 modelled. The verified source
       (referee_round_numbers.md Table A5, confirmed against target_row_count) was followed and
       Manavgat's cell count was corrected too. Its prevalence rounds to 0.038 either way.
    5. Signed-AUC CI bounds: paper/signed_auc_bootstrap.md (3-region, partial export, mulberry32
       RNG) differs by ~0.01 from paper/figure_contrast_pairs.csv (Emrehan's
       multi_aoi_feature_stability, drive_new) — e.g. elevation Manavgat [0.292, 0.469] vs
       [0.2891, 0.4712]. §4.5 quotes figure_contrast_pairs.csv. signed_auc_bootstrap.md is also
       flagged [BLOCKED: Evia] and 3-region only; it was used here only as corroboration, never
       as a number source.
    6. LORO z-score into Bejís: task brief said z-scoring "hurts the rest" outside Manavgat, but
       loro_pooled_transfer.md shows Bejís 0.417 → 0.472 (a rise, still below chance). §4.6a
       states the source file's numbers.

  Style: British English (-ise/-our), matching 01–03. Prose word count (excluding tables,
  notes and this comment): ~2,150.

ADDENDUM (2026-08-08, coordinator): Table R6 (paired baseline-vs-thermal transfer contrast)
    added to §4.3 from paper/baseline_vs_thermal_transfer.* — read-only extraction of frozen
    step9b points + step9c paired delta CIs (delta_roc_auc field, thermal − baseline on
    identical resampled target blocks). No new model runs; no new methods gap (protocol covered
    by §3.9–3.10). Full 20-direction table in the CSV; §4.3 shows five selected rows.

ADDENDUM (2026-08-13, internal referee round, Results). Eleven items. Sources: the three
    verified reports produced the same day — paper/referee_round_numbers.md (+ .csv),
    paper/transfer_ci_blocksize.md (+ .csv), paper/diagnostics_common_subset.md (+ .csv). No new
    model was fitted; nothing under repo/, drive_new/ or any step8*/step9* output was touched.
    Three new lettered tables: R11 (§4.3, raw transfer PR-AUC), R12 (§4.4, area of applicability),
    R13 (§4.7g, blocking-scale verdict counts). Lettered range in the header note is now R1–R13.

    1. Table R1 TSG columns corrected to the modelled (post-valid_for_modeling) population, with
       a sentence naming the definition and an explicit statement that no modelled result moves.
       See conflict 4 above, now CLOSED. Manavgat 20,555 -> 20,511 cells; Muğla 41,772/2,952 ->
       41,730/2,911; Evia 9,309/2,675 -> 9,298/2,664; Montiferru 2,591/582 -> 2,544/539 and
       prevalence 0.225 -> 0.212. Bejís unchanged. §4.1 and the rest of the file were swept; no
       prose repeated the legacy figures.
    2. Two mis-rounded Table 4 cells fixed against step10_bootstrap_summary.csv: Bejís→Muğla raw
       point 0.619 -> 0.618 (stored 0.61847) and Manavgat→Muğla raw lower bound 0.452 -> 0.451
       (stored 0.45145). Echoes fixed in the §4.3 adaptation sentence, in Table 5's raw column
       and in Table R2's raw-transfer row. Table 5's recovered fraction still rounds to −0.42.
       Note that Montiferru→Muğla 0.619 and the §4.6a "0.619 (Montiferru)" best-pairwise entry
       are a DIFFERENT direction and are correct as printed.
    3. §4.4 gained the area-of-applicability audit (Table R12, 12 directions) and §4.5 now
       references it. Decisive rows: Manavgat→Muğla 0.8752 weighted / 0.9640 unweighted at 0.470
       [0.451, 0.488]; Muğla→Manavgat 0.5305 / 0.9702 at 0.401; Muğla→Bejís 0.0050 weighted at
       0.583. Stated as a sufficiency counterexample, not a correlation. Montiferru has no AoA
       output in any direction and §4.4 and §4.5 both say so; the Bejís-Montiferru half of the
       contrast pair is explicitly left without an applicability number.
    4. §4.3 gained Table R11, raw thermal PR-AUC for all 20 directions beside each target's
       prevalence. Summary as reported: interval entirely above prevalence in 11 of 20, entirely
       below in 5, straddling in 4. Counted independently from Table A2 of
       referee_round_numbers.md and it agrees.
    5. §4.3 gained the baseline's own transfer summary: mean 0.5371, range 0.3322 to 0.6758, four
       directions CI-entirely-below chance; thermal 0.5414, 0.3258 to 0.6858, six such; mean
       paired delta +0.00424.
    6. New §4.7g reports both blockings for the level and the paired delta, leading with the
       10-cell counts (level 9/4/7; delta 6/4/10), with the validation figures (points to 1.1e-16,
       worst bound 0.0055, 20/20 verdict agreement at 2-cell) and the widening factors. A summary
       sentence was added to each of the two §4.3 paragraphs it bears on. The robust statement —
       no direction changes side of chance, no point estimate changes sign — is given its own
       bolded lead.
    7. Count fragility stated as ranges with the borderline directions named: Bejís→Manavgat
       (2-cell delta, bound −0.00045), Manavgat→Muğla and Evia→Montiferru (10-cell delta),
       Evia→Bejís (10-cell level). Honest 10-cell delta statement is 5 to 6 / 3 to 4 / 10 to 11.
    8. §4.8 validator claim corrected: the guarantee is A08_cohort_is_the_frozen_five (ordered
       tuple equality against DEFAULT_EXPERIMENTS), not A07, which tests literal membership of
       the string "mugla_2022" and cannot catch "mugla_2022_event_relative". Verified in
       repo/scripts/validate_era5_land_regional_diagnostic.py lines 318-326 at 48b56e7. §4.8 now
       matches §3.16.4, which already had it right.
    9. §4.6a hedged: Manavgat's LORO raw 0.469 [0.412, 0.529] spans 0.5 and is now marked as a
       point estimate; only Bejís (0.417 [0.369, 0.467]) is below chance with support. The
       z-scored Bejís fold 0.472 [0.428, 0.516] likewise spans 0.5 and is now stated as such. The
       "never beats the best pairwise" sentence is now explicitly a point-estimate comparison.
    10. Table 6 gained a second note: nineteen of twenty variants computed (vector Spearman over
       supported features is not computable at n = 2); Table 6 quotes the
       all_diagnostics_vs_transfer.MD seed variant, which is why weighted AoA reads [−0.48, +0.59]
       here and [−0.50, +0.60] in the companion CSV, with identical point estimates. §4.4 gained
       the common-subset check (12-direction rerun: the two supported-conditional rows are still
       the only ones excluding zero, at +0.87 [+0.65, +0.88] and +0.85 [+0.43, +0.88], all
       eighteen others spanning zero; published rows reproduced to 4.8e-05).
    11. Checked: §4 nowhere quoted §3.12's "roughly four times too narrow" for the transfer
       intervals, so nothing had to be removed. §4.7g now states the measured factors instead
       (2.1 to 3.6 for levels, 1.5 to 3.4 for deltas) and says the four belongs to the univariate
       diagnostic.

    12. FOLLOW-UP the same day, after the Discussion agent found the knock-on. §4.5 and Table R2
       asserted interval support on both halves of the contrast pair, which holds only at 2-cell
       blocking. Every verdict below re-read from transfer_ci_blocksize.md lines 124 to 139, not
       assumed. Manavgat→Muğla 2-cell [0.451, 0.488] below / 10-cell [0.415, 0.524] UNCERTAIN;
       Muğla→Manavgat [0.378, 0.426] below / [0.353, 0.455] below (supported at both);
       Bejís→Montiferru [0.560, 0.631] above / [0.467, 0.687] UNCERTAIN; Montiferru→Bejís
       [0.521, 0.578] above / [0.479, 0.636] UNCERTAIN. Changes:
       - Table R2's single "Raw transfer" row split into three: point estimates (blocking
         independent), 2-cell support, 10-cell support.
       - §4.5 prose now states the contrast at the point estimate and carries a new paragraph
         giving the support status at both blockings. Register matched to the Discussion.
       - §4.5's applicability paragraph no longer says "both transfer below chance with interval
         support"; it now names Muğla→Manavgat as supported at both and Manavgat→Muğla at 1 km.
       - §4.4's Table R12 discussion reworded: the three headline directions keep their point
         estimates, and the verdict status is given per direction and per blocking.
       - §4.3's parenthetical list of the six below-chance directions now says which four keep
         support at 5 km (Manavgat→Bejís, Muğla→Manavgat, Bejís→Evia, Evia→Bejís) and which two
         do not (Bejís→Manavgat, Manavgat→Muğla).
       TWO FURTHER CASES FOUND, not on the coordinator's list:
       - §4.3, the new PR-AUC paragraph said Montiferru→Manavgat is "above chance on ROC-AUC with
         interval support" and Bejís→Manavgat "below chance ... with interval support". Both are
         2-cell only: Montiferru→Manavgat 10-cell [0.497, 0.644] and Bejís→Manavgat 10-cell
         [0.345, 0.562] are both uncertain. Now qualified, and the paragraph states that the
         PR-AUC intervals themselves are 2-cell and were not recomputed.
       - §4.8 compared its own 5 km Muğla-pair intervals against the 2-cell count of six
         below-chance between-region directions. Now gives four at 5 km and six at 1 km, so the
         comparison is like for like.
       Checked and deliberately left: Table 5's "recovery above chance" status column rests on
       2-cell ADAPTED intervals, which §4.7g does not cover; a caption sentence now says so
       rather than restating verdicts that were never recomputed. §4.6b's CI-supported gains and
       losses are already on a ~5 km bootstrap. §4.3's "drags three directions ... to below it"
       and §4.5's decomposition sentences are point-level and carry no support claim.

    NOT CHANGED, with reasons. (i) The abstract, introduction and discussion all carry the
    "10 positive, 7 negative, 3 uncertain" split; those files belong to other agents this round
    and §4.7g gives them the wording they need. (ii) The z-score and CORAL columns of Table 4 were
    not recomputed at 10-cell blocking; transfer_ci_blocksize.md covers only the raw thermal arm,
    and §4.7g says so by scope rather than claiming coverage it does not have. (iii) Table R1's
    "Burned natural-veg fraction" and gate verdict columns come from the gate output, not from the
    step8a burnable counts, and were left untouched. (iv) Adapted-arm PR-AUC (Tables A2 and A3 of
    referee_round_numbers.md) exists but is not printed; Table R11's caption points at it.
-->
