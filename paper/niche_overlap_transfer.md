# SDM niche-overlap measures versus transfer — the canonical P(x|y=1) instruments also fail

**What this is.** Reviewers from the SDM/ENM tradition will ask whether *niche overlap* — the
field's canonical transferability instrument — explains our transfer matrix. This analysis
computes the three canonical measures (Schoener's D, Warren's Hellinger-based I, Mahalanobis
distance) between regional **burned-cell** feature distributions, i.e. P(x | y=1), and correlates
them with the 20 ordered raw thermal transfer AUCs in the identical pair-bootstrap framework used
for every other diagnostic. Candidate set fixed in advance; no unburned variant computed (by
design — these are presence-distribution measures). Computed 2026-08-08.

**Result in one sentence: all five niche-overlap variants fail to order transfer (Spearman ρ
−0.23 to +0.24, every 95 % CI spanning zero) — and the failure has the same instructive shape as
the geographic one: the pair with the *highest* univariate niche overlap (Manavgat–Muğla,
D̄₁ = 0.83) transfers below chance in both directions, while the pair with the *lowest* overlap in
the whole matrix (Bejís–Montiferru, D̄₁ = 0.48, PCA-2D D = 0.07, Mahalanobis 8.1) transfers above
chance both ways.**

## Method

- **Distributions:** burned cells of the primary population (TSG ∧ valid), 9 numeric features;
  n = 784 / 1 100 / 2 911 / 2 664 / 539 (Manavgat/Bejís/Muğla/Evia-ext/Montiferru). Parquet
  sha256s match the step9b manifests (recorded in JSON).
- **Schoener's D** = 1 − ½Σ|p−q|; **Warren's I** = 1 − ½Σ(√p−√q)². 1D: 50 shared bins per
  feature over the global range of all five regions' burned cells; reported as the 9-feature
  mean. Multivariate: 20×20 histogram on the first two PCs of a global PCA (fit on pooled
  standardized burned cells; NaN → pooled median, counts in JSON).
- **Mahalanobis:** distance between standardized burned-cell centroids, pooled covariance.
- **Correlation:** Spearman/Kendall vs raw thermal transfer AUC, 20 directions, pair-based
  bootstrap (10 pairs, 2000 reps, seed 42) — framework, code path and seed policy identical to
  `regime_transfer_correlation` and `conditional_similarity_transfer`.
- Environment: python 3.12, scikit-learn 1.9.0, numpy 2.5.1, pandas 3.0.5 (recorded in JSON).

## Per-pair niche overlap (higher = more similar; Mahalanobis: lower = more similar)

| Pair | D̄ (1D) | Ī (1D) | D (PCA-2D) | I (PCA-2D) | Mahalanobis | Mean transfer AUC |
|---|---|---|---|---|---|---|
| Manavgat–Muğla | **0.826** | **0.961** | **0.647** | **0.854** | **2.71** | 0.436 ↓ |
| Muğla–Evia | 0.730 | 0.925 | 0.604 | 0.825 | 3.26 | 0.615 |
| Manavgat–Evia | 0.709 | 0.915 | 0.584 | 0.815 | 3.03 | 0.649 |
| Muğla–Montiferru | 0.689 | 0.863 | 0.371 | 0.544 | 3.60 | 0.575 |
| Manavgat–Montiferru | 0.679 | 0.873 | 0.352 | 0.555 | 4.76 | 0.550 |
| Evia–Montiferru | 0.648 | 0.861 | 0.297 | 0.487 | 4.57 | 0.616 |
| Bejís–Muğla | 0.581 | 0.834 | 0.438 | 0.693 | 6.05 | 0.601 ↑ |
| Manavgat–Bejís | 0.575 | 0.831 | 0.345 | 0.568 | 5.54 | 0.385 ↓ |
| Bejís–Evia | 0.524 | 0.752 | 0.357 | 0.571 | 7.49 | 0.415 ↓ |
| Bejís–Montiferru | **0.479** | **0.717** | **0.065** | **0.124** | **8.11** | 0.571 ↑ |

## Correlations — every interval spans zero

| Measure | Expected | n | Spearman ρ [95 % CI] | Kendall τ-b [95 % CI] |
|---|---|---|---|---|
| Schoener's D, 1D mean | + | 20 | +0.24 [−0.45, +0.74] | +0.15 [−0.35, +0.56] |
| Warren's I, 1D mean | + | 20 | +0.22 [−0.42, +0.73] | +0.15 [−0.32, +0.55] |
| Schoener's D, PCA-2D | + | 20 | +0.10 [−0.51, +0.68] | +0.07 [−0.39, +0.52] |
| Warren's I, PCA-2D | + | 20 | −0.07 [−0.66, +0.49] | −0.07 [−0.50, +0.35] |
| Mahalanobis (distance) | − | 20 | −0.23 [−0.75, +0.44] | −0.17 [−0.60, +0.33] |

## Reading

1. **The canonical SDM instruments join the failure list.** Niche overlap measures where burned
   cells *sit* in environmental space; our transfer failures are driven by which way the
   response *points* (signed-AUC reversals). Two regions can burn in nearly the same envelope
   (Manavgat–Muğla: overlap top of the table on every measure) while the sign of the
   response differs — the definition of a conditional, not marginal, failure.
2. **Bejís is the illustration in the other direction.** Its burned envelope is the most
   dissimilar of any region's (bottom three rows), because it burns high (935 m median) in
   shrubland; yet Bejís–Muğla is the matrix's only interval-supported working pair. Where the
   envelope disagrees but the direction agrees (7/9), transfer works; where the envelope agrees
   but the direction reverses (Manavgat–Muğla, 4/9 with supported flips), it fails.
3. **Power caveat, as everywhere:** 10 effective pairs; CIs are wide, and these results do not
   prove niche overlap useless — they show it does not order this matrix, while the conditional
   index does (see the combined table in `all_diagnostics_vs_transfer.md`).

## Files

- `paper/niche_overlap_transfer.json` — measure computation metadata (binning, PCA, NaN counts,
  environment, sha256s), per-pair values incl. per-feature D, per-direction rows, correlations.
- `paper/niche_overlap_transfer.csv` — correlation table, flat.
- Combined table: `paper/all_diagnostics_vs_transfer.{csv,md}`.
- Scripts: `paper/niche_overlap.py`, `paper/niche_corr.mjs`.
