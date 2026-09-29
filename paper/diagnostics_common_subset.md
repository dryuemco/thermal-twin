# Table 6 recomputed on a common subset of transfer directions

**What this is.** Table 6 of the Results ranks twenty candidate transferability diagnostics against
the same target quantity, raw thermal transfer ROC-AUC (TSG population, source-only RF). The rows
are not all computed on the same sample. The marginal, area-of-applicability, climatic and
geographic rows sit on 12 directions, because those diagnostics were only produced for the four
region subset without Montiferru. The supported-conditional rows sit on 16 directions. Everything
else sits on 20. A referee can therefore ask whether "the marginal family fails and the conditional
family succeeds" is really a statement about statistical power, since the marginal rows carry the
smallest sample by construction. This note removes that confound by recomputing every diagnostic on
one common set of directions.

Machine-readable versions: `diagnostics_common_subset.csv` and `diagnostics_common_subset.json`.
Code: `diagnostics_common_subset.mjs`. Assembled 2026-08-13.

**Framework.** Unchanged from the published analyses. Spearman rho and Kendall tau-b against raw
thermal transfer ROC-AUC. Pair-based bootstrap: the unordered region pairs are resampled with
replacement, and every sampled pair contributes both of its ordered directions. 2000 replicates,
mulberry32 seeded from 42 with the per-measure offsets already in use (regime 42+0 upward,
conditional 42+100 upward, niche 42+200 upward). Equal-tailed percentile 95 % intervals. Replicates
in which a correlation is undefined are dropped and counted. No new modelling was done. The
per-direction diagnostic values were taken from the existing
`regime_transfer_correlation.json`, `conditional_similarity_transfer.json` and
`niche_overlap_transfer.json`.

## 1. Reproduction check

Before any rerun, all twenty published rows were recomputed at their original sample size with
their original seed offsets, and compared against `all_diagnostics_vs_transfer.csv`.

- **All 20 rows reproduce.** Largest absolute difference across all six reported statistics of all
  twenty rows (Spearman rho, its two interval bounds, Kendall tau-b, its two bounds) is
  **4.8e-05**. That is below the 5e-05 rounding error of the published four decimal CSV, so the
  agreement is exact to the precision at which the numbers were published.
- The recomputed sample size matches the published one on 20 of 20 rows, including the
  `vector_spearman_supported` row that is reported as not computable at n = 2.
- The three rows named as targets:

| Row | Published | Recomputed | Agreement |
|---|---|---|---|
| Agreement fraction, supported (n = 16) | +0.8404 [+0.5765, +0.8764] | +0.8404 [+0.5765, +0.8764] | exact to 4 dp |
| Domain-classifier AUC (n = 20) | -0.3170 [-0.7754, +0.3276] | -0.3170 [-0.7754, +0.3276] | exact to 4 dp |
| Fraction inside weighted AoA (n = 12) | +0.2168 [-0.4823, +0.5870] | +0.2168 [-0.4823, +0.5870] | exact to 4 dp |

One bookkeeping point found during the check, worth recording because it is visible in the
manuscript. The six four-region diagnostics appear twice in the published files under two seed
offsets of the same bootstrap. `regime_correlation.mjs` computed a "full" variant (offset 2i) and a
"four_aoi_subset" variant (offset 2i+1). The data are identical, only the random stream differs.
`all_diagnostics_vs_transfer.csv` carries the full variant, while the rendered table in
`all_diagnostics_vs_transfer.md` carries the subset variant. That is why the fraction inside
weighted AoA reads [-0.50, +0.60] in the CSV and [-0.48, +0.59] in the markdown. Both variants were
reproduced here, the second to a largest absolute difference of 4.6e-05. The point estimates are
identical and no conclusion depends on the difference. The reruns below use the full variant offset
for every measure, so that one offset rule applies to all twenty rows.

## 2. Primary rerun: 12 directions, 6 unordered pairs, four regions

This is the set on which the marginal, AoA, climatic and geographic diagnostics exist, that is the
four regions with Montiferru excluded. Every other diagnostic has been brought down onto it.

| Diagnostic | Family | Exp. | n | Spearman rho [95 % CI] | Excludes 0? |
|---|---|---|---|---|---|
| **Agreement fraction, supported features** | **P(y\|x) conditional** | + | 12 | **+0.87 [+0.65, +0.88]** | **yes** |
| **Cosine, supported features** | **P(y\|x) conditional** | + | 12 | **+0.85 [+0.43, +0.88]** | **yes** |
| Cosine, all 9 features | P(y\|x) conditional | + | 12 | +0.55 [-0.41, +0.84] | no |
| Vector Spearman, all 9 | P(y\|x) conditional | + | 12 | +0.10 [-0.79, +0.84] | no |
| Agreement count, all 9 | P(y\|x) conditional | + | 12 | +0.05 [-0.83, +0.84] | no |
| Schoener's D, 1D mean | P(x\|y=1) niche | + | 12 | +0.37 [-0.72, +0.84] | no |
| Warren's I, 1D mean | P(x\|y=1) niche | + | 12 | +0.37 [-0.72, +0.84] | no |
| Schoener's D, PCA-2D | P(x\|y=1) niche | + | 12 | +0.40 [-0.73, +0.88] | no |
| Warren's I, PCA-2D | P(x\|y=1) niche | + | 12 | +0.40 [-0.73, +0.88] | no |
| Mahalanobis, burned centroids | P(x\|y=1) niche | - | 12 | -0.23 [-0.84, +0.72] | no |
| Domain-classifier AUC | P(x) marginal | - | 12 | -0.35 [-0.85, +0.65] | no |
| Predictor-space mean dissimilarity | P(x) marginal | - | 12 | -0.10 [-0.59, +0.46] | no |
| Predictor-space p95 dissimilarity | P(x) marginal | - | 12 | -0.08 [-0.58, +0.47] | no |
| Fraction inside weighted AoA | P(x) marginal | + | 12 | +0.22 [-0.50, +0.60] | no |
| Fraction inside unweighted support | P(x) marginal | + | 12 | +0.08 [-0.92, +0.61] | no |
| Climatic distance | P(x) marginal | - | 12 | +0.06 [-0.70, +0.79] | no |
| Geographic distance | geographic | - | 12 | -0.24 [-0.84, +0.72] | no |
| Regime distance, log effective-N | P(y) spatial structure | - | 12 | +0.35 [-0.43, +0.84] | no |
| Regime distance, largest share | P(y) spatial structure | - | 12 | +0.35 [-0.53, +0.84] | no |
| Vector Spearman, supported (3 or more feats) | P(y\|x) conditional | + | 2 | not computable | no |

Kendall tau-b agrees on every row. The two supported-conditional rows give tau-b +0.74
[+0.57, +0.79] and +0.72 [+0.39, +0.79]. No other row has a tau-b interval that excludes zero.
Full tau-b values are in the CSV.

**Reduced n, stated openly.** Nineteen of the twenty diagnostics are defined on all 12 directions
of this subset. One is not. `vector_spearman_supported` needs at least three jointly supported
features, and only the Muğla and Evia pair reaches that threshold, so it rests on 2 directions from
1 unordered pair. Every bootstrap replicate is then degenerate, all 2000 of them, and no interval
exists. This is the same failure as in the published table and it is not caused by the subsetting.
The row is kept in the table so that the count of twenty is honest, but it carries no information
either way.

The supported-conditional index itself is defined on all 12 directions here. The two pairs that
drop out of it in the full set, Manavgat with Montiferru and Bejís with Montiferru, involve
Montiferru and so are already outside this subset.

Degenerate replicate counts are small elsewhere: 29 of 2000 for the supported agreement fraction,
5 of 2000 for the supported cosine, and 3 or fewer for every other computable row.

## 3. Secondary rerun: 16 directions, 8 unordered pairs

This is the set on which the supported-conditional index is defined, that is all pairs except
Manavgat with Montiferru and Bejís with Montiferru.

| Diagnostic | Family | Exp. | n | Spearman rho [95 % CI] | Excludes 0? |
|---|---|---|---|---|---|
| **Agreement fraction, supported features** | **P(y\|x) conditional** | + | 16 | **+0.84 [+0.58, +0.88]** | **yes** |
| **Cosine, supported features** | **P(y\|x) conditional** | + | 16 | **+0.81 [+0.33, +0.88]** | **yes** |
| Cosine, all 9 features | P(y\|x) conditional | + | 16 | +0.53 [-0.23, +0.83] | no |
| Vector Spearman, all 9 | P(y\|x) conditional | + | 16 | +0.27 [-0.39, +0.80] | no |
| Agreement count, all 9 | P(y\|x) conditional | + | 16 | +0.16 [-0.45, +0.78] | no |
| Schoener's D, 1D mean | P(x\|y=1) niche | + | 16 | +0.35 [-0.52, +0.80] | no |
| Warren's I, 1D mean | P(x\|y=1) niche | + | 16 | +0.35 [-0.49, +0.79] | no |
| Schoener's D, PCA-2D | P(x\|y=1) niche | + | 16 | +0.14 [-0.60, +0.82] | no |
| Warren's I, PCA-2D | P(x\|y=1) niche | + | 16 | -0.03 [-0.67, +0.61] | no |
| Mahalanobis, burned centroids | P(x\|y=1) niche | - | 16 | -0.28 [-0.81, +0.50] | no |
| Domain-classifier AUC | P(x) marginal | - | 16 | -0.40 [-0.84, +0.27] | no |
| Predictor-space mean dissimilarity | P(x) marginal | - | 12 | -0.10 [-0.59, +0.46] | no |
| Predictor-space p95 dissimilarity | P(x) marginal | - | 12 | -0.08 [-0.58, +0.47] | no |
| Fraction inside weighted AoA | P(x) marginal | + | 12 | +0.22 [-0.50, +0.60] | no |
| Fraction inside unweighted support | P(x) marginal | + | 12 | +0.08 [-0.92, +0.61] | no |
| Climatic distance | P(x) marginal | - | 12 | +0.06 [-0.70, +0.79] | no |
| Geographic distance | geographic | - | 12 | -0.24 [-0.84, +0.72] | no |
| Regime distance, log effective-N | P(y) spatial structure | - | 16 | +0.25 [-0.46, +0.76] | no |
| Regime distance, largest share | P(y) spatial structure | - | 16 | +0.25 [-0.47, +0.75] | no |
| Vector Spearman, supported (3 or more feats) | P(y\|x) conditional | + | 2 | not computable | no |

**This subset is not fully common, and that must be said.** The 16-direction set contains four
directions that involve Montiferru, namely the Muğla and Montiferru pair and the Evia and
Montiferru pair. Emrehan's five marginal measures and the geographic distance were never computed
for Montiferru, so they cannot be lifted onto those directions. Six rows therefore remain at n = 12
in this table, shown as such. This is a gap in the input data, not a choice made here. The
12-direction rerun in section 2 is the only genuinely like-for-like comparison of all four families,
and it should be treated as the primary one.

## 4. Reading

**The headline survives.** On the 12-direction common subset, where every family is on exactly the
same 6 unordered pairs and the same 12 ordered directions, the two supported-conditional rows are
still the only rows whose intervals exclude zero. Their point estimates are marginally higher than
in the published table, +0.87 and +0.85 against +0.84 and +0.81, and their lower bounds are
slightly further from zero, +0.65 and +0.43 against +0.58 and +0.33. Every one of the other
eighteen rows spans zero. The 16-direction rerun gives the same picture for the eleven rows that
can be moved onto it.

**Power was not what separated the families.** The concern was that the marginal rows sat on 12
directions while the conditional rows sat on 16 or 20, so the marginal failures could be a sample
size artefact. Bringing the conditional and niche and regime rows down to the same 12 directions
does not rescue any marginal row, and it does not cost the supported-conditional rows their
significance. Moving in the other direction, up to 16, likewise changes nothing. The contrast
between the P(y|x) family and the P(x) family is not produced by unequal n.

**What did move, and what it means.** Some null rows shift in point estimate when the sample
changes, which is expected at this size. The niche PCA-2D measures rise from +0.10 and -0.07 at
n = 20 to +0.40 at n = 12, and the regime measures from +0.29 to +0.35. Their intervals widen at the
same time and still cover zero comfortably. The ranking of the null rows by point estimate is
therefore unstable and should not be read as a league table. The only stable feature of the ranking
is the gap between the two supported-conditional rows and everything else.

**The caveats that do not go away.** Removing the power confound does not remove the others, and
they were already recorded in `conditional_similarity_transfer.md`. The supported index is close to
binary. On the 12-direction subset it takes only three values, 0 for four directions, 0.5 for two,
and 1 for six, and its denominator is 1 or 2 supported features for most pairs. A coarse three
valued predictor can order twelve points well by chance more easily than a continuous one, and the
bootstrap does not fully price that in. The index also needs the target region's signed
feature-response directions, so it needs target labels or a labelled probe, whereas every P(x),
P(x|y=1) and P(y) row is label-free. The fair claim remains the mechanistic one. The failure mode
of transfer lives in P(y|x), not in P(x). It is not a claim that a label-free predictor of transfer
has been found. Neither is it a claim that the marginal diagnostics have been shown not to order
transfer. With 6 unordered pairs they were never going to be able to show it, and that limit
applies equally to the conditional rows, which cleared it anyway.
