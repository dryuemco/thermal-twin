# Pooled multi-region training (leave-one-region-out) — does pooling rescue transfer?

**What this is.** Pairwise transfers collapse; Dimarco et al. (2026) report successful LOCO-style
pooling with stationary predictors. This analysis trains on the pooled primary populations of four
regions and tests on the held-out fifth, for all five folds, baseline and thermal feature sets,
raw and region-wise z-scored variants — the LORO counterpart our pairwise matrix was missing.
Computed 2026-08-08.

**Result in one sentence: pooling does not rescue transfer — the pooled thermal model never beats
the best single-source pairwise transfer for any target, sits near (or below) the pairwise mean,
and remains 0.22–0.50 AUC below the within-region ceiling; region-wise z-scoring helps only the
fold it helped in the pairwise setting (→Manavgat) and hurts most others.**

## Implementation equivalence (why these numbers are comparable to Emrehan's)

The comparison table mixes our LORO numbers with Emrehan's pairwise (step9b) and within-region
(step8c) numbers, so implementation identity matters. With the initially available scikit-learn
1.7.2, reproducing two step9b transfers deviated by 0.021–0.026 — **version alone moves transfer
AUC by ~0.02–0.03**. A micromamba environment with **scikit-learn 1.9.0** (exact version in
Emrehan's step10 records; python 3.12, pandas 3.0.5, numpy 2.5.1) reproduces both probes to four
decimal places (Montiferru→Bejís 0.5483, Manavgat→Bejís 0.3258, diff 0.0000). All reported LORO
numbers come from that environment. Pipeline mirrors step9b/step8b: median imputation and one-hot
(`handle_unknown=ignore`) fit on the training pool; RF(300, msl=3, balanced, seed 42).
Region-wise z-score follows the Step10 definition (per-region mean/sd ddof=0, label-free,
target scaled by its own stats). Parquet sha256s match the step9b manifests (recorded in JSON).

## Main table — thermal feature set, target ROC-AUC (spatial-block bootstrap 95 % CI)

| Held-out target | Best pairwise (source) | Mean pairwise | LORO raw | LORO region-z | Within (ceiling) |
|---|---|---|---|---|---|
| Manavgat | 0.686 (Evia) | 0.524 | 0.469 [0.412, 0.529] | **0.657** [0.543, 0.754] | 0.870 |
| Bejís | 0.583 (Muğla) | 0.476 | 0.417 [0.369, 0.467] | 0.472 [0.428, 0.516] | 0.918 |
| Muğla | 0.619 (Montiferru) | 0.571 | 0.552 [0.475, 0.625] | 0.522 [0.476, 0.569] | 0.859 |
| Evia-ext | 0.653 (Muğla) | 0.559 | 0.637 [0.592, 0.678] | 0.569 [0.520, 0.629] | 0.912 |
| Montiferru | 0.647 (Evia) | 0.576 | 0.601 [0.516, 0.683] | 0.523 [0.466, 0.570] | 0.883 |

Full grid (baseline rows, PR-AUC with no-skill base, Brier) in the CSV/JSON. PR-AUC everywhere
sits close to its no-skill base (e.g. Bejís 0.056 vs 0.072 base; Evia 0.355 vs 0.287 base) —
no fold achieves operationally useful ranking of burned cells.

## Reading

1. **Pooling is not a rescue.** LORO raw never exceeds the best pairwise source (it loses to it
   by 0.02–0.22) and never approaches within-region (gaps 0.22–0.50). For two targets (Manavgat,
   Bejís) LORO raw is *below* the pairwise mean and below chance. Adding more regions with
   conflicting conditional structure does not average out concept shift; at best the pool
   matches its most compatible member, at worst incompatible members drag it under chance.
2. **The z-score pattern repeats the adaptation story.** Region-wise scaling helps exactly where
   pairwise z-scoring helped (into Manavgat: 0.469→0.657, its elevation dissent is partly a
   level-shift problem) and degrades the folds where raw pooling was least bad (Evia 0.637→0.569,
   Montiferru 0.601→0.523, Muğla 0.552→0.522). Same regression-toward-chance signature as
   Step10's pairwise CORAL/z results — label-free alignment destroys structure indiscriminately.
3. **Baseline vs thermal, pooled:** for 3 of 5 targets the pooled *baseline* model beats the
   pooled thermal one raw (Manavgat 0.563 vs 0.469; Bejís 0.389 vs 0.417 — thermal better here;
   Muğla 0.562 vs 0.552; Montiferru 0.596 vs 0.601 ≈ tie; Evia 0.597 vs 0.637 — thermal better).
   The thermal block is not reliably useful even with four-region pooling — consistent with the
   thesis that its skill is locally parameterised.
4. **Link to Analysis 1 (n=5, descriptive only).** Pool-mean conditional similarity (cosine₉) vs
   LORO raw AUC: Spearman ρ = 0.50; pool-max: ρ = 0.56. Direction is consistent with the
   hypothesis that a fold does less badly when its pool contains at least one conditionally
   aligned region (the two worst folds, Manavgat and Bejís, are the two whose pools contain a
   *negative*-similarity member and, for Manavgat, no aligned member at all: pool-max cosine
   −0.14 vs 0.49–0.90 elsewhere). But at n=5 folds ρ = 0.5 is indistinguishable from noise —
   this is a consistency observation, not a test result. Under z-scaling the linkage inverts
   (ρ −0.36 to −0.67), which fits point 2: scaling helps precisely the misaligned fold.
5. **Comparison to Dimarco et al.:** their pooled LOCO success used spatially stationary
   predictors; our pooled failure with dynamic thermal predictors is the cross-study contrast
   the thesis predicts, now measured in the same protocol family (LORO, spatial blocks).

## Files

- `paper/loro_pooled_transfer.json` — metadata (environment, equivalence check, provenance),
  per-target comparisons, all 20 LORO runs with CIs, conditional-similarity linkage.
- `paper/loro_pooled_transfer.csv` — flat run table with comparison columns.
- Scripts: `paper/loro_pooled.py` (training/eval), `paper/pairwise_check.py` (equivalence probe),
  `paper/loro_merge.mjs` (synthesis). Environment: WSL Ubuntu-22.04, micromamba `~/mm-thermal`.
