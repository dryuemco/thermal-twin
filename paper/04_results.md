# 4. Results

> **Rewritten 2026-08-14 in the split.** This section was 14,841 words and fifteen tables. It now
> reports the three findings of Section 1.4 and the evidence they rest on, in six tables. The
> sensitivity analyses of the observational layer moved to the companion paper; the remaining
> supporting tables move to the supplement. Every table below is carried verbatim from the
> pre-split text, so no number was retyped.

## 4.1 Study regions and the admissibility gate

All five candidate regions pass the burned-landcover gate as wildfire candidates, and the negative
control fails it as intended. Kozan 2023 returns a natural-vegetation fraction of 0.017 against the
0.50 threshold and the verdict *cropland-dominated control*, and is excluded from all modelling. The
separation is not marginal: the five admitted regions carry natural-vegetation fractions of 0.723 to
0.991, so the threshold falls in an empty interval rather than between neighbouring cases. This
establishes that the gate discriminates burned area produced by natural-fuel combustion from burned
area produced by post-harvest stubble burning, which MCD64A1 does not distinguish.

**Table R1. Region summary (recap of Table 1; final numbering at assembly).** Counts from each
region's Step 8A dataset statistics; gate fractions from each region's burned-landcover gate output.
TSG = the primary natural-vegetation population. The TSG columns use the canonical modelled
population, `burnable_tree_shrub_grass` **and** `valid_for_modeling == True`, which is the
population every model in this paper was fitted and scored on.

| Region | Total cells | Valid cells | Burned | Prevalence (all valid) | TSG cells | Burned in TSG | TSG prevalence | Burned natural-veg fraction | Gate verdict |
|---|---|---|---|---|---|---|---|---|---|
| Manavgat 2021 | 24,150 | 24,087 | 796 | 0.033 | 20,511 | 784 | 0.038 | 0.984 | pass |
| Bejís 2022 | 15,759 | 15,759 | 1,103 | 0.070 | 15,190 | 1,100 | 0.072 | 0.991 | pass |
| Muğla 2021 | 73,098 | 73,045 | 3,026 | 0.041 | 41,730 | 2,911 | 0.070 | 0.958 | pass |
| North Evia 2021 (extended) | 22,925 | 22,906 | 2,788 | 0.122 | 9,298 | 2,664 | 0.287 | 0.945 | pass |
| Montiferru 2021 | 3,234 | 3,173 | 697 | 0.220 | 2,544 | 539 | 0.212 | 0.723 | pass |

North Evia is analysed on an extended AOI. Relative to the legacy box, the extended box leaves the
burned scar essentially unchanged while cutting overall prevalence from 0.361 to 0.122 and TSG
prevalence from 0.676 to 0.287. The effect of that choice on transfer is reported in Section 4.7a.

## 4.2 Within-region: the thermal increment replicates in five regions

In every region, adding the six thermal predictors to the baseline increases spatially blocked
out-of-fold ROC-AUC. The increment's bootstrap interval excludes zero in all five regions at 1 km
and at 5 km blocking, which are the two scales this design supports as intervals. At 10 km the point
estimates hold, from +0.048 to +0.154, but they rest on 6 to 33 positive-carrying blocks and are
reported as indicative rather than as intervals, for the reason given in the table note.

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
6**, out of 60, 48, 167, 50 and 12. No bootstrap replicate was invalid at any block size except
Bejís at 20 cells, where 5 of 1000 were single-class — which is the symptom of the six
positive-carrying blocks just reported, and a further reason to read that row as indicative. An
equal-tailed percentile interval built on six positive-carrying blocks has no meaningful coverage,
and Montiferru at 20 cells additionally feeds only 12 groups into a 5-fold grouped split, so its
models train on about ten blocks each. **The 20-cell row of this table should be read as indicative
rather than as an interval.** The 10-cell row, where every region has 16 to 70 positive-carrying
blocks, is the coarsest blocking this design supports properly, and the increment holds there in all
five regions. Source: `paper/referee2_numbers.md`, block C, counted from the frozen per-cell
prediction tables.

This is the first half of the trade-off. It is not itself novel, and it is reported because the
second half is measured against it.

## 4.3 Cross-region transfer, and what label-free adaptation does to it

**Raw transfer is heterogeneous and includes anti-predictive directions.** Raw target AUC spans
0.326 to 0.686. Twelve of 20 directions are above chance with CI support, six are *below* chance
with CI support (both directions of Manavgat↔Bejís and Manavgat↔Muğla, plus Bejís→Evia and
Evia→Bejís), and two intervals span 0.5. Even the best raw transfer (Evia→Manavgat, 0.686) remains
far below the target's own within-region thermal performance (0.870); across all directions the raw
deficit against the within-region reference is 0.184 to 0.592 AUC. Those counts belong to the 2-cell
blocking of Table 4. At the more conservative 10-cell (~5 km) blocking the same points give 9 above,
4 below and 7 uncertain, with no direction changing side of the chance line (Section 4.7g). Four of
the six below-chance directions keep their support there: Manavgat→Bejís, Muğla→Manavgat, Bejís→Evia
and Evia→Bejís. Bejís→Manavgat and Manavgat→Muğla lose it and carry no verdict. The qualitative
statement is unchanged. The counts should not be read as exact.

**The static baseline does not transfer either.** This is the control for the interpretation the
rest of the paper invites, and it constrains that interpretation sharply. Running the same twenty
directions with the terrain, fuel and greenness baseline alone gives a mean target AUC of **0.537**,
against **0.541** for the thermal model. The predictor class that this paper's framing treats as the
portable one — static attributes of a place, the class Dimarco et al. transfer successfully — is
itself barely above chance here. The paired per-direction contrast is reported in Section 4.6b; what
matters at this point is that the transfer failure documented below is not specific to the dynamic
block. Adding pre-fire thermal state to a baseline that does not travel produces a model that does
not travel.

**The thermal block's paired contribution to transfer, with its interval.** Differencing the two
matrices direction by direction gives a mean of **+0.004**. The directions are not independent —
each region appears in eight of the twenty — so the interval depends on what is treated as the
resampling unit, and all four units the design permits give the same answer:

| Resampling unit | n | 95 % interval on the mean paired contribution |
|---|---:|---|
| Directions, naive | 20 | [−0.027, +0.034] |
| Unordered pairs, cluster bootstrap | 10 | [−0.028, +0.036] |
| Unordered pairs, t on pair means | 10 | [−0.034, +0.042] |
| Regions, leave-one-out jackknife | 5 | [−0.037, +0.046] |

Every interval spans zero and the point estimate is a small fraction of each width. The per-region
jackknife also shows how little the mean is anchored: holding out Manavgat, Bejís, Muğla, Evia and
Montiferru in turn gives +0.0148, +0.0021, +0.0065, **−0.0081** and +0.0060, so **dropping Evia alone
reverses the sign of the headline**. Within-direction sampling variability is not propagated into
any of these four; they resample between directions only.

**Table 4. Cross-region transfer matrix, thermal model, TSG population.** Target ROC-AUC with 2-cell
spatial-block bootstrap 95% CIs (1000 replicates). CORAL is applied after region-wise z-scoring (λ =
10⁻⁵).

| Direction | Raw | Region-wise z-score | CORAL |
|---|---|---|---|
| Manavgat→Bejís | 0.326 [0.305, 0.349] | 0.477 [0.451, 0.502] | 0.511 [0.484, 0.534] |
| Bejís→Manavgat | 0.444 [0.408, 0.480] | 0.457 [0.420, 0.497] | 0.555 [0.528, 0.583] |
| Manavgat→Muğla | 0.470 [0.451, 0.488] | 0.431 [0.411, 0.449] | 0.443 [0.423, 0.461] |
| Muğla→Manavgat | 0.401 [0.378, 0.426] | 0.559 [0.531, 0.587] | 0.560 [0.535, 0.587] |
| Manavgat→Evia | 0.613 [0.593, 0.631] | 0.542 [0.520, 0.565] | 0.539 [0.518, 0.561] |
| Evia→Manavgat | 0.686 [0.653, 0.716] | 0.516 [0.489, 0.544] | 0.527 [0.500, 0.553] |
| Bejís→Muğla | 0.618 [0.601, 0.635] | 0.518 [0.501, 0.535] | 0.507 [0.489, 0.524] |
| Muğla→Bejís | 0.583 [0.561, 0.607] | 0.535 [0.512, 0.557] | 0.560 [0.538, 0.581] |
| Bejís→Evia | 0.383 [0.363, 0.402] | 0.532 [0.509, 0.551] | 0.499 [0.479, 0.518] |
| Evia→Bejís | 0.448 [0.426, 0.470] | 0.549 [0.524, 0.575] | 0.549 [0.525, 0.573] |
| Muğla→Evia | 0.653 [0.636, 0.671] | 0.561 [0.543, 0.580] | 0.563 [0.545, 0.582] |
| Evia→Muğla | 0.577 [0.560, 0.593] | 0.501 [0.485, 0.518] | 0.530 [0.515, 0.546] |
| Montiferru→Manavgat | 0.567 [0.539, 0.594] | 0.573 [0.538, 0.609] | 0.606 [0.574, 0.639] |
| Manavgat→Montiferru | 0.533 [0.488, 0.580] | 0.586 [0.540, 0.629] | 0.592 [0.550, 0.631] |
| Montiferru→Bejís | 0.548 [0.521, 0.578] | 0.574 [0.552, 0.596] | 0.569 [0.548, 0.591] |
| Bejís→Montiferru | 0.594 [0.560, 0.631] | 0.550 [0.500, 0.601] | 0.574 [0.530, 0.621] |
| Montiferru→Muğla | 0.619 [0.604, 0.634] | 0.576 [0.562, 0.589] | 0.565 [0.550, 0.579] |
| Muğla→Montiferru | 0.531 [0.495, 0.568] | 0.587 [0.549, 0.624] | 0.584 [0.547, 0.623] |
| Montiferru→Evia | 0.586 [0.565, 0.606] | 0.630 [0.611, 0.649] | 0.624 [0.605, 0.641] |
| Evia→Montiferru | 0.647 [0.608, 0.682] | 0.568 [0.528, 0.609] | 0.581 [0.539, 0.623] |

**Label-blind adaptation compresses the matrix toward chance rather than repairing it.** Under
region-wise z-scoring the twenty directions span 0.431 to 0.630 and under CORAL 0.443 to 0.624,
roughly half the raw spread, with no adapted direction exceeding 0.631 against within-region
references of 0.859 to 0.918. Adaptation raises the failing directions and degrades most of those
that already transferred. Taking the better of the two adaptations per direction, 14 of the 20 end
closer to chance than they began and 6 end further from it; five of those six involve Montiferru,
the smallest and last-added region, and move upward, while the sixth is Manavgat→Muğla moving
downward from 0.470 to 0.443. The 14 to 6 split should be read at the precision of limitation (x) in
Section 5.9, since Bejís→Manavgat is counted as compressed on a margin of 0.001.

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

In the six directions where raw transfer was below chance, the best label-free method recovers at
most 34 % of the gap to the within-region reference, so the remaining conditional fraction is at
least 0.66 everywhere. Seven directions show *negative* recovery, meaning adaptation moves the score
away from the reference; in six of those raw transfer was already above chance and adaptation
destroyed that advantage. Label-free alignment therefore does not act as a repair mechanism.

## 4.4 Transferability diagnostics: only conditional similarity orders transfer

Twenty candidate diagnostics from four families were each rank-correlated with the same target
quantity, the raw thermal transfer AUC over the twenty ordered directions, under one common
pair-based bootstrap.

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

**Only two diagnostics have intervals excluding zero, and both are conditional.** The stronger is
the sign-agreement fraction over interval-supported features, at ρ = +0.84 [+0.58, +0.88]; the
cosine variant reaches +0.81. Every marginal measure fails, including area-of-applicability-style
dissimilarity in predictor space, climatic distance and geographic distance, and so do the
niche-overlap and regime families. The learned domain classifier is at ceiling, separating source
from target at AUC ≥ 0.96 for every pair, which makes it useless as an ordering instrument precisely
because it always succeeds.

Two limits are stated with the result rather than after it. The conditional index is evaluated at
its own design size: its tie structure caps the achievable Spearman at +0.861, the observed +0.840
therefore sits essentially on that ceiling, and the exact one-sided permutation p is 0.0060, the
smallest this tie structure can produce, against a Bonferroni threshold of 0.0026 over the nineteen
computed variants. No outcome of this diagnostic could have cleared family-wise correction on ten
effective pairs. And signed associations require burned labels in both regions, so the family that
works is not available before deployment while the family that fails is.

A third limit is a selection rather than a sample-size issue, and it is the sharpest of the three.
The two rows that clear zero are the *supported-feature* variants, where the feature subset is
chosen by whether two regions' bootstrap intervals happen to be disjoint — a data-dependent
selection made on the same data, with no correction. Their unselected counterparts over all nine
features are ρ = +0.50 [−0.17, +0.83] for the cosine and ρ = +0.18 [−0.40, +0.72] for the agreement
count, both spanning zero. The result lives in the selection step, and is reported as such.

**The families are compared on unequal samples, and equalising them does not change the ordering.**
The marginal, applicability, climatic and geographic rows sit on twelve directions, because those
diagnostics exist only for the four-region subset; the supported-conditional rows sit on sixteen and
the rest on twenty. A reader may reasonably ask whether "the marginal family fails" is a statement
about power rather than about diagnostics. Recomputing every row on the common twelve directions
answers it: the published values reproduce to 4.8 × 10⁻⁵, the conditional rows still lead at +0.87
[+0.65, +0.88] and +0.85 [+0.43, +0.88], and every marginal row still spans zero. The ordering is not
an artefact of unequal samples.

## 4.5 The contrast pair: similarity is not sufficient

The clearest single view of Table 6 needs no ranking at all. Manavgat and Muğla lie in the same
country and fire year, 307 km apart by the centroid geodesic distance this paper uses as a
diagnostic (their nearest boundaries are 191 km apart), and their burned cells occupy the most
similar
environmental envelope of any pair in the matrix, with per-feature Schoener's D of 0.77 to 0.89. Yet
five of nine feature-response directions point opposite ways, including elevation, whose signed AUC
is 0.374 [0.289, 0.471] in Manavgat against 0.611 [0.532, 0.690] in Muğla with disjoint intervals,
and all four absolute thermal channels. Transfer is below chance in both directions at the point
estimate, 0.470 and 0.401. Both directions also sit deep inside the nominal area of applicability,
at 0.875 and 0.531 of target cells inside the weighted region.

Bejís and Montiferru sit at the opposite extreme, with burned envelopes that barely overlap and the
most dissimilar values on every overlap measure, and they transfer above chance in both directions.
That half of the contrast rests on point estimates, since neither direction carries a verdict at
5 km blocking, and the marginal applicability audit was never produced for Montiferru. The claim is
one of *sufficiency*: similarity does not guarantee transfer, and dissimilarity does not preclude
it. Established by coexisting counterexamples, it does not depend on the number of pairs available.

## 4.6 Interventions: pooling and feature removal obey the same conservation

**(a) Pooled multi-region training.** Training on the pooled populations of four regions and testing
on the held-out fifth does not rescue transfer. At the point estimate the pooled thermal model never
beats the best single-source pairwise transfer for any target, with shortfalls of 0.02 to 0.22, and
it remains 0.28 to 0.50 AUC below the within-region ceiling. For two targets it falls below the
pairwise mean and below chance, though only Bejís is below chance with interval support, at 0.417
[0.369, 0.467].

**(b) Removing the direction-reversing features.** The two predictors whose signed association
reverses between regions are **`elevation_mean` and `lst_anomaly_mean`**. Retraining without them
costs **−0.081** of mean within-region AUC, supported in every region (per-region deltas −0.060,
−0.130, −0.074, −0.063, −0.079, every interval entirely below zero), and changes mean transfer by
**+0.014 [−0.017, +0.045]**, which spans zero.

Two qualifications belong with those numbers rather than after them. First, the debit is not the
thermal block's. Dropping elevation alone accounts for −0.061 of it (0.888 → 0.827) and dropping the
LST anomaly alone for −0.013 (0.888 → 0.875), so roughly three quarters of the cost is the removal
of a **baseline** terrain variable, not of a thermal channel. Second, both figures are
post-selection: the two predictors were chosen because they reverse, using the same data on which
the −0.081 and the +0.014 are then estimated, and no correction for that selection is applied.

| Configuration | Mean within-region AUC | Mean transfer AUC |
|---|---|---|
| full | 0.888 | 0.541 |
| drop `elevation_mean` | 0.827 | 0.546 |
| drop `lst_anomaly_mean` | 0.875 | 0.544 |
| drop both | 0.807 | 0.556 |

What this measures, stated at the strength it supports, is a local cost with no compensating
transfer gain. It does not measure an exchange, because the transfer side is a null on both arms:
the thermal block's own contribution to transfer is +0.004 with an interval spanning zero
(Section 4.3), and removing the reversing predictors returns +0.014 with an interval spanning zero.
Two nulls on the portability axis do not constitute a price paid.

## 4.7 Sensitivity analyses

**(a) Evia AOI and prevalence.** Repeating the raw transfer arms with the legacy, high-prevalence
Evia box leaves every qualitative conclusion unchanged: thermal raw transfer AUCs move by at most a
up to 0.07 — the largest is Evia→Bejís, 0.378 to 0.448 — and no direction changes side of the
chance line.

**(d) CORAL regularisation.** Over nine λ values from 0 to 10⁻¹ on four directions, CORAL transfer
AUC moves by at most 0.014 within any direction and 0.008 within the thermal family, so no
CORAL-dependent conclusion here is sensitive to λ in that range. The companion paper reports the
canonical λ = 1, which the released sweep omits.

**(g) Blocking scale.** Recomputing the transfer quantities at 10-cell (≈ 5 km) blocking from the
frozen per-cell predictions widens the intervals and moves the verdict counts, from ten positive,
seven negative and three uncertain at 1 km to six, four and ten at 5 km. Coarser blocking therefore
removes support from six verdicts and adds none.

The point estimates are unchanged, but that is an identity rather than a result and should not be
offered as robustness: the blocking scale is the bootstrap *resampling unit*, and each point
estimate is computed once over all target cells, so no choice of block size could have moved one.
What the comparison does establish is the direction of the fragility — every verdict that changes,
changes towards "no verdict" — and that no direction crosses the chance line under the widened
intervals. The counts are the fragile part of this paper. The sign pattern is not thereby shown to
be robust; it is simply not tested by this particular variation.

## 4.8 The same geography, a second fire: reversal with place held constant

Every result above compares different places. Muğla admits a stricter test, because a second fire
occurred inside the identical AOI on the identical analysis grid: the 2021 event, with its predictor
window closing on 28 July, and the 2022 event, whose matched window closes on 20 June. Region,
bounding box, cell definition, feature registry and processing chain are the same. What the design
holds fixed is place; what it does not hold fixed is season, since the 2022 fire ignites about six
weeks earlier, nor population, since the 2022 arm is defined by removing the 2021 scar.

**Table R8. Signed univariate feature-burned AUC, Muğla 2021 versus 2022.** Raw AUC against
`burned`, never folded to max(AUC, 1 − AUC); 10-cell (≈ 5 km) spatial-block bootstrap, 1,000
replicates, seed 42 (Section 3.14). Analysis population 41,730 rows / 2,911 burned (2021) and
38,790 rows / 331 burned (2022). **Positive-carrying 5 km blocks: 70 for the 2021 arm and 11 for the
2022 arm.** Table 3's note sets sixteen as the floor this design supports at that blocking, so the
2022 intervals here fall below the paper's own standard and are read as indicative, exactly as the
20-cell row of Table 3 is. The 2022 arm is additionally a single compact scar, so its eleven blocks
are contiguous. Read from
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

**Elevation reverses with bootstrap support.** In 2021 higher ground burned preferentially, at 0.611
with its interval entirely above 0.5; in 2022 lower ground did, at 0.296 with its interval entirely
below. The two intervals are disjoint, 0.532 against 0.355, and the difference is −0.317 [−0.414,
−0.220]. The same predictor, the same region, the same grid, and an association that points the
opposite way in two fires eleven months apart. The four absolute thermal channels change side as
well, from bootstrap-supported lower-values-burn in 2021 to higher-values-burn point estimates in
2022.

Two structural properties must be read alongside these numbers, because they have no analogue in the
twenty-direction matrix. The two arms are not disjoint samples: they share 38,789 of the 2022 arm's
38,790 cells, and elevation, slope and land cover are identical to the digit across all 73,098 grid
cells, so only NDVI and the six thermal channels carry new information between them. And the removal
is the target's own positive class, so in the 2022 to 2021 direction not one target positive is
present in the source training population while 38,789 of 38,819 target negatives are, and
membership of the source training set alone separates the 2021 target's classes at ROC-AUC 0.9996.
We therefore cannot bound what that asymmetry does to the two transfer numbers, only state that a
direction with this structure is not comparable to the twenty between-region directions. The
elevation reversal is the finding; the structural asymmetry is a competing explanation this design
cannot exclude. The known part of the bias runs the safe way: the removed cells are high, with a
median of 563 m, and unburned in 2022, so removing them raises the 2022 elevation AUC and makes the
reversal smaller rather than larger.

## 4.9 What target labels cost: the recovery curve

Everything above measures a failure; this prices it. If the residual gap is conditional and
label-free alignment cannot close it, the missing resource is target-conditional information, and
the direct way to supply it is target labels. The frozen few-shot diagnostic answers how many for
three regions in all six ordered directions, using one 10-cell (≈ 5 km) spatial block as the unit of
labelling effort, budgets of 0 to 32 blocks drawn under a fixed tier order with seeds independent of
any result, and ten repeats per budget. Recovery is read against a matched target-only ceiling of
0.777 to 0.824 under the same folds and blocking.

Thirty-two labelled blocks recover **85 to 89 % of the target's own ceiling in three of the six
directions**, two of which started below chance and the third at 0.583; 51 to 57 % in two more,
which are the directions where the conditional gap is widest; and 30 % in the sixth. That budget is
7 to 20 % of the target's natural-vegetation population, so it is a real answer to "what do we do"
and not a cheap one. At small budgets the same intervention damages the direction that already
transfers best without any labels. Six directions in three regions cannot support a general label
budget and none is offered.
