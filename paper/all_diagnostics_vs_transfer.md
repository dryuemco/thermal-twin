# All transferability diagnostics versus transfer — the combined table

**What this is.** Every candidate diagnostic computed in this project, against the same target
quantity (raw thermal transfer ROC-AUC, TSG population, source-only RF, 20 ordered directions),
with the same pair-based bootstrap (unordered pairs resampled, both directions carried,
2000 replicates, seed 42, percentile 95 % CI). Sources:
`regime_transfer_correlation.csv` (marginal + regime, full-set rows),
`conditional_similarity_transfer.csv` (conditional), `niche_overlap_transfer.csv` (SDM niche
overlap). Machine-readable version: `all_diagnostics_vs_transfer.csv`. Assembled 2026-08-08.

**One sentence: twenty diagnostic variants across four families — marginal P(x), niche-overlap
P(x|y=1), label-pattern P(y), and conditional P(y|x) — and the only intervals that exclude zero
belong to the conditional family's CI-supported variants.**

| Diagnostic | Family | Exp. | n | Spearman ρ [95 % CI] | 0 dışı? |
|---|---|---|---|---|---|
| **Agreement fraction, supported features** | **P(y·x) conditional** | + | 16 | **+0.84 [+0.58, +0.88]** | **✓** |
| **Cosine, supported features** | **P(y·x) conditional** | + | 16 | **+0.81 [+0.33, +0.88]** | **✓** |
| Cosine, all 9 features | P(y·x) conditional | + | 20 | +0.50 [−0.17, +0.83] | — |
| Vector Spearman, all 9 | P(y·x) conditional | + | 20 | +0.27 [−0.36, +0.77] | — |
| Agreement count, all 9 | P(y·x) conditional | + | 20 | +0.18 [−0.40, +0.72] | — |
| Schoener's D, 1D mean | P(x·y=1) niche | + | 20 | +0.24 [−0.45, +0.74] | — |
| Warren's I, 1D mean | P(x·y=1) niche | + | 20 | +0.22 [−0.42, +0.73] | — |
| Schoener's D, PCA-2D | P(x·y=1) niche | + | 20 | +0.10 [−0.51, +0.68] | — |
| Warren's I, PCA-2D | P(x·y=1) niche | + | 20 | −0.07 [−0.66, +0.49] | — |
| Mahalanobis, burned centroids | P(x·y=1) niche | − | 20 | −0.23 [−0.75, +0.44] | — |
| Domain-classifier AUC | P(x) marginal | − | 20 | −0.32 [−0.78, +0.33] | — |
| Predictor-space mean dissimilarity | P(x) marginal | − | 12 | −0.10 [−0.54, +0.43] | — |
| Predictor-space p95 dissimilarity | P(x) marginal | − | 12 | −0.08 [−0.59, +0.49] | — |
| Fraction inside weighted AoA | P(x) marginal | + | 12 | +0.22 [−0.48, +0.59] | — |
| Fraction inside unweighted support | P(x) marginal | + | 12 | +0.08 [−0.89, +0.63] | — |
| Climatic distance | P(x) marginal | − | 12 | +0.06 [−0.76, +0.79] | — |
| Geographic distance | geographic | − | 12 | −0.24 [−0.84, +0.73] | — |
| Regime distance, log effective-N | P(y) spatial structure | − | 20 | +0.29 [−0.38, +0.74] | — |
| Regime distance, largest share | P(y) spatial structure | − | 20 | +0.29 [−0.39, +0.72] | — |
| Vector Spearman, supported (≥3 feats) | P(y·x) conditional | + | 2 | not computable | — |

(Kendall τ-b for every row is in the CSV; conclusions identical.)

## Notes that must accompany this table

- **Power:** the effective sample is 10 unordered pairs (6 for the 12-direction marginal rows;
  8 for the supported-conditional rows). Wide CIs mean the null rows are "not shown to order
  transfer", not "shown not to". The conditional rows' significance survives despite the *same*
  low power, which is the point.
- **Label requirement asymmetry:** every P(x), P(x|y=1) and P(y) row is computable without
  target labels; the conditional rows require the target's signed feature–response directions
  (i.e. labels or a labelled probe). The fair statement is mechanistic — the failure mode lives
  in P(y|x) — not that a label-free predictor exists.
- **Supported-conditional caveats** (from `conditional_similarity_transfer.md`): near-binary
  index, denominators of 1–2 for most pairs, two Montiferru pairs drop out.
- Counterexample pairs that summarise the table: Manavgat–Muğla (top niche overlap, high
  geographic similarity, below-chance transfer both ways) versus Bejís–Montiferru /
  Bejís–Muğla (lowest niche overlap, above-chance transfer). Similarity of *where* things burn
  does not transfer; similarity of *which way* the response points does.
