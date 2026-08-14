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
