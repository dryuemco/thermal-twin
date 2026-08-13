# 4. Results

> **Drafting note.** Every number below is taken from the verified fact sheet
> (`facts_results.md`, extracted 2026-08-08 from the complete `drive_new/` export) or from the
> analysis reports in `paper/` (`all_diagnostics_vs_transfer`, `regime_transfer_correlation`,
> `conditional_similarity_transfer`, `loro_pooled_transfer`, `feature_drop_transfer`,
> `niche_overlap_transfer`, `niche_vs_conditional`, `sklearn_version_sensitivity`,
> `signed_auc_bootstrap`, `figure_contrast_pairs.csv`). Tables 3–6 follow the outline's reserved
> numbering; lettered tables (R1–R10) are additional and will be renumbered at assembly. All
> intervals are 95% spatial-block bootstrap percentile intervals (Section 3.9) unless stated
> otherwise; "CI-supported" means the interval excludes the reference value (zero for
> differences, 0.5 for transfer AUCs).

## 4.1 Study regions and data summary

Five Mediterranean regions enter the analysis (Section 3.1, Table 1). Table R1 summarises cell counts, burned-cell counts
and prevalence for both analysis populations, together with the burned-landcover gate verdict of
Section 3.3.

**Table R1. Region summary (recap of Table 1; final numbering at assembly).** Counts from each
region's Step 8A dataset statistics; gate fractions from each region's burned-landcover gate
output. TSG = the primary natural-vegetation population (`burnable_tree_shrub_grass`).

| Region | Total cells | Valid cells | Burned | Prevalence (all valid) | TSG cells | Burned in TSG | TSG prevalence | Burned natural-veg fraction | Gate verdict |
|---|---|---|---|---|---|---|---|---|---|
| Manavgat 2021 | 24,150 | 24,087 | 796 | 0.033 | 20,555 | 784 | 0.038 | 0.984 | pass |
| Bejís 2022 | 15,759 | 15,759 | 1,103 | 0.070 | 15,190 | 1,100 | 0.072 | 0.991 | pass |
| Muğla 2021 | 73,098 | 73,045 | 3,073 | 0.042 | 41,772 | 2,952 | 0.071 | 0.958 | pass |
| North Evia 2021 (extended) | 22,925 | 22,906 | 2,803 | 0.122 | 9,309 | 2,675 | 0.287 | 0.945 | pass |
| Montiferru 2021 | 3,234 | 3,173 | 748 | 0.236 | 2,591 | 582 | 0.225 | 0.723 | pass |

All five regions pass the admissibility gate as wildfire candidates (burned natural-vegetation
fraction 0.723–0.991). Montiferru is the weakest pass, with a burned cropland fraction of 0.274;
its sensitivity to this composition is examined in Section 4.7b. The negative control behaves as
designed: in Kozan 2023 the gate classifies 542 burned cells as 0.017 natural vegetation and
0.983 cropland (533 of 542 burned cells cropland-dominant, 8 grassland, 1 tree cover), returning
the verdict *cropland-dominated control*, and the region is excluded from all modelling. The
separation is not marginal — the five admitted regions carry natural-vegetation fractions of
0.723–0.991 against the control's 0.017, so the 0.50 threshold falls in an empty interval rather
than between neighbouring cases. This establishes that the gate discriminates burned area produced
by natural-fuel combustion from burned area produced by post-harvest stubble burning, which
MCD64A1 itself does not distinguish, and that admission of the five study regions is a decision the
data supports rather than a selection made by hand.

North Evia is analysed on an extended AOI. Relative to the legacy 0.40°×0.40° box, the extended
0.80°×0.60° box (~3× the area, identical predictor and label windows) leaves the burned scar
essentially unchanged (2,789 → 2,803 burned cells) while cutting overall prevalence from 0.361 to
0.122 and TSG prevalence from 0.676 to 0.287. The effect of this choice on transfer is reported
in Section 4.7a.

## 4.2 Within-region: the thermal increment replicates in five regions

In every region, adding the six thermal predictors to the static baseline increases spatially
blocked out-of-fold ROC-AUC, and the increment's bootstrap interval excludes zero at every block
size tested (Table 3; [Fig. 3]).

**Table 3. Within-region baseline versus thermal performance and block-size robustness.**
Primary (TSG) population; spatially blocked 5-fold CV (Section 3.8); paired spatial-block
bootstrap, 1000 replicates. Block sizes 2/10/20 cells ≈ 1/5/10 km.

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

At the default 2-cell blocking, thermal ΔAUC ranges from +0.056 (Bejís) to +0.153 (Evia), with
ΔPR-AUC from +0.097 (Manavgat, [+0.071, +0.123]) to +0.300 (Evia, [+0.273, +0.329]); every
interval excludes zero. Absolute AUC declines as blocks coarsen, as expected when long-range
spatial structure is progressively withheld, but the increment itself does not erode toward
zero: at 20-cell (~10 km) blocking ΔAUC remains between +0.048 and +0.154 with all intervals
above zero. The same holds in the secondary all-valid population (Section 4.7f).

## 4.3 Cross-region transfer

Transfer is evaluated for all 20 ordered directions among the five regions, as raw source-only
application and under the two label-blind adaptations of Section 3.11 (Table 4; [Fig. 4]).

**Table 4. Cross-region transfer matrix, thermal model, TSG population.** Target ROC-AUC with
2-cell spatial-block bootstrap 95% CIs (1000 replicates). CORAL is applied after region-wise
z-scoring (λ = 10⁻⁵).

| Direction | Raw | Region-wise z-score | CORAL |
|---|---|---|---|
| Manavgat→Bejís | 0.326 [0.305, 0.349] | 0.477 [0.451, 0.502] | 0.511 [0.484, 0.534] |
| Bejís→Manavgat | 0.444 [0.408, 0.480] | 0.457 [0.420, 0.497] | 0.555 [0.528, 0.583] |
| Manavgat→Muğla | 0.470 [0.452, 0.488] | 0.431 [0.411, 0.449] | 0.443 [0.423, 0.462] |
| Muğla→Manavgat | 0.401 [0.378, 0.426] | 0.559 [0.531, 0.587] | 0.560 [0.535, 0.587] |
| Manavgat→Evia | 0.613 [0.593, 0.631] | 0.542 [0.520, 0.565] | 0.539 [0.518, 0.561] |
| Evia→Manavgat | 0.686 [0.653, 0.716] | 0.516 [0.489, 0.544] | 0.527 [0.500, 0.553] |
| Bejís→Muğla | 0.619 [0.601, 0.635] | 0.518 [0.501, 0.535] | 0.507 [0.489, 0.524] |
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
Evia→Bejís), and two intervals span 0.5. Even the best raw transfer (Evia→Manavgat, 0.686)
remains far below the target's own within-region thermal performance (0.870); across all
directions the raw deficit against the within-region reference is 0.184 to 0.592 AUC.

**The thermal block's transfer contribution is sign-unstable per direction.** Pairing each
direction's thermal model against the static baseline model under the same protocol (Table R6)
shows that the block worth +0.056 to +0.153 AUC inside every region is worth +0.004 on average
across regions: its paired contribution is CI-supported positive in 10 directions, CI-supported
negative in 7, and uncertain in 3. It is the swing factor at the chance line — adding the
thermal block drags three directions from a baseline at or above chance to below it
(Manavgat→Muğla 0.508 → 0.470; Bejís→Evia 0.531 → 0.383; Muğla→Manavgat 0.522 → 0.401) and
lifts one from below to above (Muğla→Bejís 0.451 → 0.583). In the Manavgat–Muğla pair the
baseline transfers at roughly chance and the thermal block pushes both directions below it; in
the Bejís–Muğla pair the thermal block is what carries transfer above chance in both directions.

**Table R6. Paired baseline-versus-thermal raw transfer contrast (final numbering at
assembly).** Target ROC-AUC per model; Δ = thermal − baseline computed on identical resampled
target blocks (2-cell blocks, 1000 replicates). Full 20-direction table with baseline and
thermal CIs in `baseline_vs_thermal_transfer.csv`; the seven CI-supported negative and ten
CI-supported positive directions are listed there. Selected rows:

| Direction | Baseline | Thermal | Δ [95% CI] | Support |
|---|---|---|---|---|
| Muğla→Bejís | 0.451 | 0.583 | +0.133 [+0.105, +0.158] | positive |
| Evia→Montiferru | 0.549 | 0.647 | +0.097 [+0.054, +0.138] | positive |
| Manavgat→Muğla | 0.508 | 0.470 | −0.038 [−0.051, −0.024] | negative |
| Muğla→Manavgat | 0.522 | 0.401 | −0.121 [−0.146, −0.098] | negative |
| Bejís→Evia | 0.531 | 0.383 | −0.148 [−0.168, −0.126] | negative |

**Label-blind adaptation compresses the matrix toward chance.** Under region-wise z-scoring the
20 directions span 0.431–0.630; under CORAL, 0.443–0.624 — roughly half the raw spread, with no
adapted direction exceeding 0.63 against within-region references of 0.859–0.918. Adaptation
raises the failing directions (e.g. Manavgat→Bejís 0.326 → 0.511 CORAL; Muğla→Manavgat 0.401 →
0.560) and simultaneously degrades every direction that already transferred (e.g. Evia→Manavgat
0.686 → 0.527 CORAL; Bejís→Muğla 0.619 → 0.518 z-score; Muğla→Evia 0.653 → 0.563). After the
best adaptation per direction the maximum is 0.630 (Montiferru→Evia, z-score), whereas raw
transfer reached 0.686, with three directions at or above 0.647.

**Table 5. Transfer-gap decomposition (four-AOI set, 12 directions).** Within = target's
within-region thermal AUC; best adapted = the better of z-score/CORAL; recovered fraction =
(adapted − raw)/(within − raw), signed and unclipped, with paired bootstrap CI (1000 replicates).
Montiferru directions are not part of this decomposition (per-pair absolute decompositions exist
without fraction CIs).

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
| Bejís→Muğla | 0.859 | 0.619 | 0.518 (z-score) | −0.42 [−0.51, −0.34] | **negative recovery** |

The decomposition ([Fig. 5]) shows both faces of the same behaviour. In the five directions
where raw transfer was below chance, the best label-blind method recovers at most 34% of the gap
to the within-region reference; the remaining (concept) fraction is at least 0.66 everywhere.
Seven directions show *negative* recovery — adaptation moves the score away from the
within-region reference, in the worst case (Evia→Manavgat) recovering −0.86 of the gap. In six
of the seven, raw transfer was already above chance and adaptation destroyed that advantage; in
the seventh (Manavgat→Muğla), raw transfer was below chance (0.470) and adaptation lowered it
further (0.443). Label-blind adaptation therefore does not act
as a repair mechanism: it compresses all directions toward chance, closing a minority of the
deficit where transfer fails and destroying performance where transfer works.

## 4.4 Transferability diagnostics: only conditional similarity orders transfer

Twenty candidate diagnostics from four families — marginal predictor-distribution measures
P(x), burned-niche overlap measures P(x|y=1), fire-regime (label-pattern) structure P(y), and
conditional feature–response direction P(y|x) — were each rank-correlated with the same target
quantity (raw thermal transfer AUC over the 20 ordered directions) under a common pair-based
bootstrap (Section 3.14.1). Table 6 gives the complete set.

**Table 6. All transferability diagnostics versus raw thermal transfer (20 ordered
directions).** Spearman ρ with pair-based bootstrap 95% CIs. Exp. = expected sign. Rows with n =
12 exist only for the four-AOI subset; the supported-features conditional rows use the 16
directions (8 pairs) with at least one CI-supported feature.

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

*Table note (power): the effective sample is 10 unordered pairs (6 for the 12-direction rows;
8 for the supported-conditional rows); the two directions of a pair are not independent and every
pair shares regions with three others. Intervals of width ±0.5–0.8 cannot rule out moderate true
correlations; null rows are "not shown to order transfer", not "shown not to".*

Of the 20 variants, exactly two have bootstrap intervals excluding zero, and both belong to the
conditional family: the sign-agreement fraction over CI-supported features (ρ = +0.84
[+0.58, +0.88]) and the cosine similarity of supported signed-AUC vectors (ρ = +0.81
[+0.33, +0.88]) (Section 3.14.4). These indices are computed from signed feature–response directions in *both* regions and
therefore require burned labels (or a labelled probe) in the target; unlike every P(x), P(x|y=1)
and P(y) row, they are not label-free.

The remaining families all fail to order the matrix. The domain classifier (Section 3.14.2) is
at ceiling for every pair (AUC 0.962–0.9999) — marginal shift is essentially total everywhere —
so it cannot discriminate outcomes ranging from 0.33 to 0.69. The canonical SDM niche-overlap
instruments (Schoener's D, Warren's I, Mahalanobis distance between burned-cell distributions;
Section 3.14.3) span ρ −0.23 to +0.24 with all intervals crossing zero. Fire-regime structure
(Section 3.14.5) has the *wrong-signed* point estimate (ρ +0.29): the most regime-similar pair
(Bejís–Evia, effective component count 1.0000 vs 1.0083) fails in both directions while the most
regime-different pair (Bejís–Muğla) transfers above chance. At pair level, niche overlap and
sign agreement are empirically distinct (ρ between them −0.36 to +0.45, all CIs spanning zero),
and in partial rank correlations the conditional index retains its association with transfer
with niche overlap held fixed (partial ρ +0.82 [+0.40, +0.88]) while niche overlap retains none
with the conditional index held fixed (−0.07 [−0.39, +0.37]).

## 4.5 The contrast pair: highest niche overlap fails, lowest niche overlap works

The clearest single view of the preceding table is a two-pair contrast ([Fig. 8]; per-feature
data in `figure_contrast_pairs.csv`). [Production note: the OUTLINE slot reserved for signed
univariate AUC per feature with CIs is realised by Fig. 8 — two panels of
per-feature signed AUC with ~5 km-block CIs, one per pair, annotated with the overlap and
transfer numbers below.]

**Table R2. The contrast pairs (final numbering at assembly).**

| | Manavgat ~ Muğla | Bejís ~ Montiferru |
|---|---|---|
| Schoener's D̄ (1-D, 9 features) | **0.826** — highest of all 10 pairs | **0.479** — lowest of all 10 pairs |
| Mahalanobis (burned centroids) | 2.71 (closest) | 8.11 (farthest) |
| Sign agreement (9 features) | 4/9; jointly supported features 2 (agreement 1/2), with a CI-supported elevation flip | 7/9; no jointly supported features — the two regions' supported sets do not intersect (Montiferru CIs wide) |
| Raw transfer, both directions | 0.470 [0.452, 0.488] and 0.401 [0.378, 0.426] — **both below chance** | 0.594 [0.560, 0.631] and 0.548 [0.521, 0.578] — **both above chance** |

Manavgat and Muğla are in the same country and fire year, roughly 200 km apart, and their burned
cells occupy the most similar environmental envelope of any pair in the matrix (per-feature D
0.77–0.89). Yet five of nine feature–response directions point opposite ways — elevation
(signed AUC 0.374 [0.289, 0.471] in Manavgat vs 0.611 [0.532, 0.690] in Muğla, disjoint CIs)
and all four absolute thermal channels (e.g. `current_lst_mean` 0.538 [0.452, 0.621] vs 0.325
[0.271, 0.382]) — and transfer is below chance in both directions with CI support. Bejís and
Montiferru sit at the opposite extreme: burned envelopes that barely overlap (per-feature D
0.23–0.77; the pair is the most dissimilar on every overlap measure), yet seven of nine
directions agree — the pair has no jointly supported features, because the two regions'
supported sets do not intersect, so the supported-agreement index is undefined for it — and
transfer is above chance in both directions with CI support. Where the envelope agrees but the direction reverses, transfer
fails; where the envelope disagrees but the direction agrees, transfer works.

## 4.6 Interventions: pooling and feature removal obey the same conservation

Two interventions test whether the diagnosis of Sections 4.3–4.5 yields a remedy. Both show the
same pattern: what transfer gains, the within-region model or the direction-aligned pairs pay
for.

**(a) Pooled multi-region training (leave-one-region-out).** Training on the pooled TSG
populations of four regions and testing on the held-out fifth (Section 3.15.1) does not rescue
transfer (Table R3).

**Table R3. LORO pooled training, thermal feature set, target ROC-AUC (final numbering at
assembly).**

| Held-out target | Best pairwise (source) | Mean pairwise | LORO raw | LORO region-z | Within (ceiling) |
|---|---|---|---|---|---|
| Manavgat | 0.686 (Evia) | 0.524 | 0.469 [0.412, 0.529] | 0.657 [0.543, 0.754] | 0.870 |
| Bejís | 0.583 (Muğla) | 0.476 | 0.417 [0.369, 0.467] | 0.472 [0.428, 0.516] | 0.918 |
| Muğla | 0.619 (Montiferru) | 0.571 | 0.552 [0.475, 0.625] | 0.522 [0.476, 0.569] | 0.859 |
| Evia (ext.) | 0.653 (Muğla) | 0.559 | 0.637 [0.592, 0.678] | 0.569 [0.520, 0.629] | 0.912 |
| Montiferru | 0.647 (Evia) | 0.576 | 0.601 [0.516, 0.683] | 0.523 [0.466, 0.570] | 0.883 |

The pooled thermal model never beats the best single-source pairwise transfer for any target
(shortfalls 0.02–0.22) and remains 0.22–0.50 AUC below the within-region ceiling. For two
targets (Manavgat, Bejís) the pooled model is below the pairwise mean and below chance.
Region-wise z-scoring of the pool raises only the into-Manavgat fold substantially
(0.469 → 0.657) and leaves Bejís below chance (0.417 → 0.472), while degrading the three folds
where raw pooling was least bad (Evia 0.637 → 0.569; Montiferru 0.601 → 0.523; Muğla
0.552 → 0.522). Pooled PR-AUC sits close to its no-skill base for every fold (e.g. Bejís 0.056
vs base 0.072); no fold achieves operationally useful ranking of burned cells. For three of five
targets the pooled *baseline* model matches or beats the pooled thermal one raw (Manavgat 0.563
vs 0.469; Muğla 0.562 vs 0.552; Montiferru 0.596 vs 0.601 ≈ tie), with thermal ahead only for
Evia (0.637 vs 0.597) and Bejís (0.417 vs 0.389).

**(b) Dropping the direction-reversing features.** Retraining without the two features with
CI-supported reversals (`elevation_mean`; `lst_anomaly_mean`; Section 3.15.2) trades
within-region skill for a near-zero mean transfer gain (Table R4).

**Table R4. Feature-removal trade-off (final numbering at assembly).** Means over 5 regions
(within, TSG OOF) and 20 directions (transfer); paired ~5 km-block bootstrap for per-direction
deltas. *Note: the CI-supported above-chance counts in this table use the feature-drop
analysis's ~5 km-block bootstrap and are therefore more conservative than the 2-cell-block
step10 intervals of Table 4, under which 12 of 20 raw directions are CI-supported above
chance; the coarser blocks widen the intervals without changing any point estimate.*

| Config | Mean within AUC | Mean transfer AUC | Directions >0.5 (point) | Directions >0.5 (CI-supported) |
|---|---|---|---|---|
| Full (reference) | **0.888** | 0.541 | 14 | 9 |
| Drop elevation | 0.827 | 0.546 | 17 | 9 |
| Drop lst_anomaly | 0.875 | 0.544 | 14 | 9 |
| Drop both | 0.807 | **0.556** | 17 | **10** |

Dropping both reversal features buys +0.014 mean transfer AUC and one additional CI-supported
above-chance direction at the price of −0.081 mean within-region AUC; the within-region cost of
removing elevation is bootstrap-supported in every region (largest Bejís −0.114
[−0.147, −0.079]). The transfer deltas land exactly where the reversal diagnosis points:
the three CI-supported gains are Manavgat→Bejís +0.118 [+0.048, +0.203], Evia→Bejís +0.075
[+0.023, +0.131] and Montiferru→Manavgat +0.057 [+0.017, +0.092]; the mean delta over the eight
Manavgat-involved directions is +0.025 against −0.009 over the other twelve — and Manavgat is
the elevation dissenter (signed AUC 0.374 vs 0.61–0.65 elsewhere). Conversely, the five
CI-supported losses (Evia→Manavgat −0.078; Manavgat→Evia −0.071; Muğla→Evia −0.038;
Montiferru→Bejís −0.036; Muğla→Bejís −0.026) occur precisely where elevation's direction is
shared and informative. `lst_anomaly` removal contributes only in the pair where it reverses
with support: Bejís→Evia (+0.046 alone; +0.063 [+0.026, +0.100] combined with elevation).
Identifying which pairs cross a reversal requires the target's signed directions, i.e. target
labels; applied label-free, the same removal degrades the five aligned directions.

## 4.7 Sensitivity analyses

**(a) Evia AOI and prevalence.** Repeating the raw transfer arms with the legacy (small,
prevalence 0.361; TSG prevalence 0.676) versus extended (prevalence 0.122; TSG prevalence 0.287)
Evia AOI (Section 3.16.1) leaves every qualitative conclusion unchanged: thermal raw transfer AUCs move by at most
0.070 (Evia→Bejís 0.378 → 0.448) and no direction changes side of chance (Manavgat→Evia
0.662 → 0.613; Evia→Manavgat 0.670 → 0.686; Bejís→Evia 0.397 → 0.383; Muğla→Evia 0.630 → 0.653;
Evia→Muğla 0.572 → 0.577). The 2.4-fold change in target prevalence does not create or destroy
any CI-supported transfer.

**(b) Montiferru cropland fringe.** Within-region, excluding grassland (tree+shrub population)
leaves the thermal increment essentially unchanged: ΔAUC 0.104 [0.075, 0.131] versus 0.101
[0.080, 0.125] for TSG (Section 3.16.2). Cross-region, the thermal-minus-baseline delta on the
target agrees in sign and support between the two populations for six of eight
Montiferru-involved directions; the two disagreements (Bejís→Montiferru, Montiferru→Muğla) move
from supported to uncertain, not to sign reversal. Montiferru's transfer behaviour is not driven
by its cropland/grassland fringe.

**(c) Window closure.** Shifting both ends of the predictor window earlier by 7 and 14 days
(window length preserved, fixed common cohort, shared folds; Section 3.16.3) leaves the
within-region thermal increment
bootstrap-supported in every region and every variant (Table R5). Nowhere does the increment
shrink toward zero; in Manavgat and Bejís it increases with earlier closure.

**Table R5. Window-closure sensitivity: thermal ΔAUC (TSG common cohort; final numbering at
assembly).**

| Region | Canonical | Close 7 d | Close 14 d |
|---|---|---|---|
| Manavgat | 0.074 [0.062, 0.085] | 0.101 [0.088, 0.114] | 0.094 [0.078, 0.109] |
| Bejís | 0.058 [0.048, 0.068] | 0.077 [0.068, 0.088] | 0.079 [0.068, 0.090] |
| Muğla | 0.115 [0.105, 0.125] | 0.114 [0.104, 0.124] | 0.128 [0.118, 0.137] |
| Evia (ext.) | 0.156 [0.144, 0.170] | 0.149 [0.136, 0.162] | 0.135 [0.124, 0.147] |
| Montiferru | 0.096 [0.074, 0.118] | 0.091 [0.068, 0.113] | 0.100 [0.077, 0.122] |

**(d) CORAL regularisation.** Over the available sweep — four directions (Bejís↔Muğla,
Manavgat↔Muğla), nine λ values from 0 to 10⁻¹ — the CORAL transfer AUC moves by at most 0.008
within any direction (e.g. Muğla→Manavgat 0.559–0.564; Manavgat→Muğla 0.443–0.451). No
CORAL-dependent conclusion for these directions is sensitive to λ in this range. The sweep does
not cover λ = 1 or the Montiferru/Evia directions.

**(e) scikit-learn version.** With byte-identical data, pipeline and seed, changing only the
library version from 1.9.0 to 1.7.2 moves raw transfer AUC by +0.021 (Montiferru→Bejís) and
+0.026 (Manavgat→Bejís) on the two probes tested — the same order as some reported effects —
while within-region AUCs reproduce to ~4 decimals across environments. All numbers in this
paper were produced under, or verified against, scikit-learn 1.9.0; the two probes reproduce to
four decimal places in the verification environment (difference 0.0000). Cross-region point
estimates therefore carry an implementation tolerance of roughly ±0.02–0.03 unless the exact
library version is fixed; the bootstrap intervals reported throughout are wider than this
jitter.

**(f) Analysis population.** In the secondary all-valid population the within-region thermal
increment is CI-supported in all five regions, with smaller deltas than in the primary
natural-vegetation population for the three high-increment regions: ΔAUC 0.059 [0.049, 0.068]
(Manavgat), 0.048 [0.040, 0.057] (Bejís), 0.072 [0.067, 0.078] (Muğla), 0.053 [0.049, 0.058]
(Evia), 0.075 [0.057, 0.094] (Montiferru), against TSG values of 0.067, 0.056, 0.116, 0.153 and
0.101 respectively. Absolute AUCs are higher in the mixed population (baseline 0.827–0.910),
consistent with land-cover composition contributing separable but non-thermal discrimination;
the within-region conclusion does not depend on the population choice.

## 4.8 The same geography, a second fire: direction reversal with place held constant

Every result above compares different places. Muğla admits a stricter test, because a second fire
event occurred inside the identical AOI on the identical analysis grid (Section 3.16.4): the 2021
event, with its 58-day predictor window closing on 28 July, and the 2022 event, whose matched
58-day window closes on 20 June. Region, bounding box, cell definition, feature registry and
processing chain are the same; only the event differs. The comparison is therefore
same-geography event-to-event, not clean temporal transfer — the 2022 fire ignites about five weeks
earlier in the season, so year and seasonal phase are confounded (Section 3.16.4) — but geography,
the explanation most often offered for between-region instability, is held fixed by construction.
The second Muğla event is deliberately kept out of the 20-direction matrix of Section 4.3, and that
exclusion is enforced and tested in the released code rather than merely asserted here: the
validator check `A07_mugla_2022_absent_from_default_analysis` passes on the executed diagnostic
output (Sections 3.16.4, 3.17).

The two events are structurally very different fires. Table R7 reports the burned-pattern
comparison on the primary population.

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

The 2021 season burned as a dispersed multi-fire complex — ten components, an effective count of
4.05, no single component holding a third of the area — spanning the region's full relief from near
sea level to 1,975 m. The 2022 event is one compact scar: two components, an effective count of
1.34, 85.2 % of burned cells in the largest, and confined to the low belt. Its highest burned cell
lies at 777 m, below the 2021 event's 95th percentile of 1,526 m, and its median elevation of 187 m
is a third of 2021's 563 m. The two fires occupy different parts of the same elevation gradient.

That difference propagates directly into the feature–label relationship. Table R8 gives the signed
univariate AUCs.

**Table R8. Signed univariate feature–burned AUC, Muğla 2021 versus 2022.** Raw AUC against
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
intervals are disjoint — 0.532 against 0.355 — with the difference at −0.317 [−0.414, −0.220]. The
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
reverse at all — NDVI keeps a bootstrap-supported positive direction in both events.

Transfer between the two events behaves unlike any between-region direction in the matrix, and it
does so asymmetrically (Table R9). Both directions stay *above* chance — the thermal intervals are
[0.513, 0.604] and [0.654, 0.685], neither touching 0.5 — where six of the twenty between-region
directions fell below it with interval support (Section 4.3). Holding geography fixed removes the
collapse.

**Table R9. Transfer between the two Muğla events.** Primary population, thermal and baseline
models, target ROC-AUC with 5 km spatial-block bootstrap 95 % CIs (Section 3.16.4). Within-region
references are each target's own frozen value at 2-cell blocking (Table 3 for 2021; the 2022
figure is its Step 8C point estimate, ΔAUC +0.078 [+0.061, +0.097]). The baseline and thermal
columns are point estimates on the full target; the ΔAUC column is the bootstrap mean reported
alongside its interval, so it differs from the difference of the two point estimates in the third
decimal (point ΔAUC −0.083 and +0.088 respectively). Both arms of this pair were reproduced
independently by the pipeline author to ≤1×10⁻⁷ (Section 3.16.4).

| Direction | Baseline | Thermal | ΔAUC (thermal − baseline) | Target's within-region thermal | Gap |
|---|---|---|---|---|---|
| Muğla 2021 → 2022 | 0.642 [0.606, 0.674] | 0.559 [0.513, 0.604] | **−0.082 [−0.127, −0.040]** | 0.942 | 0.383 |
| Muğla 2022 → 2021 | 0.581 [0.566, 0.598] | 0.670 [0.654, 0.685] | **+0.089 [+0.072, +0.104]** | 0.859 | 0.189 |

What does not survive is the thermal block's contribution, and its failure here is sharper than
anywhere else in the paper: **the same six predictors change the sign of their contribution
depending on which event is the source, and both signs are interval-supported.** Carried forward
from 2021 to 2022 they cost 0.082 AUC; carried back from 2022 to 2021 they buy 0.089. This is not
a case of a weak signal failing to travel. Within each event separately the thermal block helps and
its interval excludes zero — +0.116 in 2021 (Table 3) and +0.078 in 2022 — so the block is locally
informative in both, and still actively harmful in one direction between them.

The asymmetry follows the elevation reversal. A model fitted on 2021 learned a relationship whose
strongest static term points the wrong way for a fire confined below 777 m, and the thermal
channels it learned alongside that term were fitted under the same regime; applied to 2022 they
subtract skill from a baseline that already transfers at 0.642. In the reverse direction the 2022
model carries a relationship fitted on a narrow low-elevation slice, which the broader 2021 event
contains, and there the thermal block adds. The residual gap to the target's own within-region
performance remains large in both directions — 0.383 and 0.189 — so nothing here rescues transfer;
what it shows is that the direction of the thermal block's contribution is not a property of the
predictors but of the pair.

## 4.9 Regional meteorological context

Table R10 characterises the meteorological conditions of each region's predictor window against
its own 2017–2020 climatology (Section 3.17). Anomalies are reported in physical units only;
standardised anomalies are computed by the diagnostic but are not reported, for the reason given
in Section 3.17. The label window is not characterised here and is used nowhere in this paper: it
opens on the ignition date and runs 35–59 days into the autumn rains, so it describes conditions
during and after the fire rather than the conditions that preceded it.

**Table R10. Predictor-window meteorology against the 2017–2020 climatology.** ERA5-Land, AOI
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

The five predictor windows share a common signature of moderate dryness rather than extremity.
Every region is drier than its own climatology in relative humidity (−0.65 to −5.18 %), and four
of five are drier in precipitation, two of them substantially so (Evia −61.6 mm, Montiferru
−35.5 mm); Bejís is the exception, wetter than climatology by +36.3 mm. Temperature departures are
small in absolute terms, spanning −0.06 to +1.11 °C, and wind departures smaller still
(−0.21 to +0.34 m s⁻¹).

The one region-level contrast the analysis was run to test concerns Manavgat. Its predictor-window
temperature is −0.06 °C from its climatological mean — the only region at or below its own
baseline, and an anomaly small enough to be read as *at* the baseline — while the other four sit
0.31 to 1.11 °C above theirs. Its humidity deficit (−3.24 %) is mid-range among the five and its
precipitation is within 1.4 mm of climatology, the smallest precipitation departure in the set.
On none of the four variables is Manavgat the extreme member. The consequence for the
interpretation of its transfer behaviour is taken up in Section 5.7.

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
       784 and Bejís 1100 agree). Table R1 uses step8a counts; the §4.4/§4.5 analyses use the
       TSG∧valid counts. Difference is the valid_for_modeling intersection — footnote at
       assembly.
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
-->
