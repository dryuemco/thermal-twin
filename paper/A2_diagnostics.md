# Appendix B. All twenty transferability diagnostics

Section 4.4 summarises this table by family. The full ranking is given here because the negative
result is the point: a reader should be able to see every candidate that was tried, not only the
families' best members, and to check that no diagnostic was dropped after it failed.

**Table B1. All transferability diagnostics versus raw thermal transfer (20 ordered directions).**
Spearman ρ with pair-based bootstrap 95 % CIs. Exp. = expected sign. Rows with n = 12 exist only for
the four-AOI subset, because those diagnostics were never produced for Montiferru. The
supported-features conditional rows use the 16 directions (8 pairs) with at least one CI-supported
feature.

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

*Table note.* A null row means the diagnostic was **not shown to order transfer** on this design, not
that it was shown incapable of ordering it. With ten effective region pairs the power is low, and the
intervals are wide enough to admit moderate true correlations in either direction. The last row is
retained rather than deleted because it was computed: on two directions the statistic has no
meaningful value, and reporting that is more honest than dropping the variant.

**Reading the two rows that clear zero.** Both are supported-feature variants, where the predictor
subset is chosen by whether two regions' bootstrap intervals happen to be disjoint. That is a
data-dependent selection made on the same data, uncorrected. Their all-nine-feature counterparts are
in the table and both span zero. The result lives in the selection step, and Section 4.4 says so.

**Equal-sample check.** The families sit on unequal samples: marginal, applicability, climatic and
geographic rows on twelve directions, the supported-conditional rows on sixteen, the rest on twenty.
Recomputing every row on the common twelve directions reproduces the published values to
4.8 × 10⁻⁵ and leaves the ordering unchanged — the conditional rows still lead at +0.87 [+0.65, +0.88]
and +0.85 [+0.43, +0.88], every marginal row still spans zero. Source:
`paper/diagnostics_common_subset.md`.

## B2. The signed univariate associations the reversal claim rests on

Section 4.6b drops two predictors because their signed association with burning reverses between
regions with bootstrap support on the frames as drawn. Section 4.9 shows that both supported
elevation reversals disappear once the frames are equalised, so this table is the evidence for the
feature-removal arm and for the narrowed claim of Contribution 4, not for a general reversal
mechanism. It was computed for the frozen analysis and is reproduced here because the claim
is otherwise asserted rather than shown.

**Table B2. Signed univariate AUC of each predictor against `burned`, by region.** Primary
natural-vegetation population; 10-cell (~5 km) spatial-block bootstrap, 1000 replicates, seed 42.
The AUC is never folded to max(AUC, 1 − AUC), so a value below 0.5 means lower values rank burned
and is a direction rather than weakness. **Bold** marks a region whose own interval excludes 0.5.

| Feature | Manavgat | Bejís | Muğla | Evia | Montiferru |
|---|---|---|---|---|---|
| `elevation_mean` | **0.374** [0.289, 0.471] | **0.643** [0.558, 0.729] | **0.611** [0.532, 0.690] | 0.541 [0.448, 0.626] | 0.584 [0.395, 0.762] |
| `slope_mean` | 0.531 [0.423, 0.642] | 0.521 [0.439, 0.605] | **0.637** [0.582, 0.686] | 0.487 [0.418, 0.554] | **0.652** [0.506, 0.771] |
| `ndvi_mean` | **0.636** [0.587, 0.676] | 0.559 [0.497, 0.619] | **0.662** [0.616, 0.704] | **0.639** [0.575, 0.701] | 0.586 [0.450, 0.704] |
| `lst_anomaly_mean` | 0.482 [0.428, 0.530] | **0.418** [0.364, 0.480] | 0.485 [0.395, 0.566] | **0.640** [0.567, 0.710] | 0.395 [0.285, 0.535] |
| `current_lst_mean` | 0.538 [0.452, 0.621] | 0.477 [0.401, 0.547] | **0.325** [0.271, 0.382] | **0.377** [0.301, 0.456] | 0.370 [0.248, 0.513] |
| `current_tvdi_mean` | 0.552 [0.460, 0.641] | 0.517 [0.429, 0.595] | **0.336** [0.275, 0.398] | **0.362** [0.285, 0.442] | **0.356** [0.233, 0.499] |
| `tvdi_difference_mean` | 0.449 [0.391, 0.505] | 0.512 [0.443, 0.583] | 0.490 [0.396, 0.575] | 0.519 [0.444, 0.589] | **0.378** [0.282, 0.497] |
| `downscaled_lst_mean` | 0.552 [0.466, 0.637] | 0.484 [0.400, 0.560] | **0.307** [0.253, 0.366] | **0.377** [0.297, 0.459] | 0.365 [0.240, 0.511] |
| `fused_lst_mean` | 0.540 [0.454, 0.622] | 0.481 [0.404, 0.551] | **0.325** [0.272, 0.383] | **0.376** [0.300, 0.456] | 0.370 [0.248, 0.513] |

**What counts as a reversal.** A pair of regions is called a reversal only when their signed
associations point to opposite sides of 0.5 **and each region's own interval excludes 0.5**. That is
stricter than requiring the two regions' intervals to be disjoint, and the difference matters: for
`current_lst_mean` between Manavgat and Muğla the two intervals are disjoint, but Manavgat's own
interval, [0.452, 0.621], includes 0.5, so Manavgat has no established direction to reverse from.
That pair is a point reversal, not a supported one.

**Table B3. The cross-region reversals that meet the stricter criterion.** Difference intervals are
from the same paired bootstrap.

| Feature | Region A | AUC | Region B | AUC | Difference [95 % CI] |
|---|---|---:|---|---:|---|
| `elevation_mean` | Manavgat | 0.374 | Bejís | 0.643 | +0.269 [+0.138, +0.397] |
| `elevation_mean` | Manavgat | 0.374 | Muğla | 0.611 | +0.235 [+0.102, +0.360] |
| `lst_anomaly_mean` | Bejís | 0.418 | Evia | 0.640 | +0.221 [+0.123, +0.313] |

Three pair-level reversals across **two** features, which is why Section 3.12 removes exactly those
two. Twenty-nine further pairs reverse at the point estimate only, spread across eight of the nine
features, and they are not counted. The conservative criterion costs the paper findings rather than
manufacturing them: a difference interval on the pair, which is the instrument Section 4.8 uses,
would support more reversals than the three listed here.

## B4. The transfer matrix in precision-recall terms

ROC-AUC is reported throughout the main text for comparability with the susceptibility literature.
A susceptibility surface is used as a ranked area budget, so precision-recall is the operational
quantity, and at target prevalences of 3.8 to 28.7 % the two can differ sharply. Read from the same
frozen step9b exports as Table 4.

**Table B4. Thermal transfer, PR-AUC against the no-skill baseline.** The baseline is the target's
burned prevalence. Lift is PR-AUC divided by that baseline; a lift of 1 is no better than random
ranking. Ordered by lift.

| Direction | ROC-AUC | PR-AUC | No-skill | Lift |
|---|---:|---:|---:|---:|
| Evia → Manavgat | 0.686 | 0.094 | 0.038 | **2.45** |
| Bejís → Montiferru | 0.594 | 0.289 | 0.212 | 1.36 |
| Evia → Montiferru | 0.647 | 0.283 | 0.212 | 1.34 |
| Bejís → Muğla | 0.619 | 0.093 | 0.070 | 1.33 |
| Muğla → Evia | 0.653 | 0.379 | 0.287 | 1.32 |
| Montiferru → Bejís | 0.548 | 0.093 | 0.072 | 1.28 |
| Montiferru → Muğla | 0.619 | 0.089 | 0.070 | 1.27 |
| Evia → Muğla | 0.577 | 0.086 | 0.070 | 1.23 |
| Muğla → Bejís | 0.583 | 0.088 | 0.072 | 1.22 |
| Manavgat → Evia | 0.613 | 0.343 | 0.287 | 1.20 |
| Manavgat → Montiferru | 0.533 | 0.243 | 0.212 | 1.15 |
| Montiferru → Manavgat | 0.567 | 0.043 | 0.038 | 1.11 |
| Montiferru → Evia | 0.586 | 0.317 | 0.287 | 1.11 |
| Muğla → Montiferru | 0.531 | 0.214 | 0.212 | 1.01 |
| Bejís → Manavgat | 0.444 | 0.034 | 0.038 | **0.90** |
| Manavgat → Muğla | 0.470 | 0.063 | 0.070 | **0.90** |
| Evia → Bejís | 0.448 | 0.059 | 0.072 | **0.82** |
| Bejís → Evia | 0.383 | 0.226 | 0.287 | **0.79** |
| Muğla → Manavgat | 0.401 | 0.029 | 0.038 | **0.75** |
| Manavgat → Bejís | 0.326 | 0.049 | 0.072 | **0.67** |
| **Mean** | **0.541** | **0.156** | **0.136** | **1.16** |

Six directions fall below their own no-skill baseline, and only one exceeds twice it. The six are the
same six that are below chance on ROC-AUC, which is what a reversed ranking predicts in either
metric. Section 4.9 shows that this count is largely a property of the evaluation frames rather than
of a reversed predictor-burning relationship.
