# Fire-regime distance versus transfer performance — formal rank-correlation test

**What this is.** The C4/§5 program (POSITIONING.md) asks whether any label-free, pre-transfer
diagnostic orders observed cross-region transfer performance. Emrehan's four marginal measures do
not (Spearman |ρ| 0.06–0.24, four AOIs). This analysis adds two candidates that were still
untested — **fire-regime distance** (burned-patch structure) and the **domain-classifier AUC** —
and puts all of them in one table against the same target quantity, each with a pair-based
bootstrap 95 % CI. Computed 2026-08-08 from the complete five-region export (`drive_new/`).

**Result in one sentence: no diagnostic in the table — marginal, climatic, geographic,
domain-classifier or regime-based — orders raw thermal transfer performance; every 95 % CI spans
zero, and the regime pair that is nearly identical (Bejís–Evia-extended) fails in both directions
while the regime pair that is most different (Bejís–Muğla) is the only one that transfers.**

---

## Method

- **Transfer quantity:** raw thermal ROC-AUC on the target region (source-only RF, step9b),
  primary population `burnable_tree_shrub_grass`, all **20 ordered directions** among the five
  canonical regions. Every direction carries a 1000-replicate spatial-block bootstrap CI (step9c).
  Cross-check: the 12 directions shared with Emrehan's AoA comparison table agree to 3×10⁻⁸.
- **Regime metrics:** 8-connectivity connected components of burned TSG cells on
  `row_500m`/`col_500m`, computed here independently from the five step8a parquets (sha256 match
  the step9b manifests). **All five regions reproduce Emrehan's Rejim tablosu exactly**
  (component count, largest, share, second-largest, effective count to 1e-4).
- **Regime distance (symmetric per pair):** primary = |Δ log effective component count|
  (inverse-Simpson); secondary = |Δ largest-component share|.
- **Domain-classifier AUC:** spatial-block OOF AUC of a source-vs-target region classifier
  (Emrehan's `domain_classifier_audit`, all 10 pairs, 0.962–0.9999).
- **Correlation:** Spearman ρ and Kendall τ-b between each diagnostic and transfer AUC.
  **Pair-based bootstrap CI:** unordered region pairs resampled with replacement (10 pairs; 6 for
  the four-AOI measures), each sampled pair contributing both of its ordered directions;
  2000 replicates, seed 42, percentile 95 % CI. PRNG `mulberry32` (procedure deterministic,
  not bit-identical to NumPy).
- **Pre-registered expectation** (stated before computation, per the project's honesty rule):
  regime distance would *not* predict transfer, because all four of Emrehan's measures fail and
  because Bejís and Evia-extended are nearly identical in regime yet their transfers collapse.

## Per-region regime metrics (verified)

| Region | Burned TSG cells | Components | Largest | Share | 2nd | Effective N |
|---|---|---|---|---|---|---|
| Manavgat | 784 | 15 | 690 | 88.01 % | 32 | 1.2872 |
| Bejís | 1 100 | 1 | 1 100 | 100 % | 0 | 1.0000 |
| Muğla | 2 911 | 10 | 914 | 31.40 % | 738 | 4.0545 |
| Evia-extended | 2 664 | 2 | 2 653 | 99.59 % | 11 | 1.0083 |
| Montiferru | 539 | 8 | 416 | 77.18 % | 55 | 1.6275 |

One compact contiguous burn (Bejís, Evia-ext), one fragmented multi-fire landscape (Muğla),
two intermediate (Manavgat, Montiferru).

## Correlation table — every interval spans zero

Full set = 20 ordered directions (10 pairs); Emrehan's marginal measures exist only for the four
AOIs without Montiferru (12 directions, 6 pairs). For the five-AOI measures the common four-AOI
subset is also shown so all rows are comparable on the same basis.

| Diagnostic | Expected sign | Set | n dir | Spearman ρ [95 % CI] | Kendall τ-b [95 % CI] |
|---|---|---|---|---|---|
| **Regime distance, log effective-N (primary)** | − | full | 20 | **+0.290** [−0.379, +0.739] | +0.195 [−0.295, +0.583] |
| | | 4-AOI | 12 | +0.353 [−0.533, +0.839] | +0.286 [−0.373, +0.752] |
| **Regime distance, largest-share (secondary)** | − | full | 20 | +0.290 [−0.389, +0.722] | +0.195 [−0.306, +0.566] |
| | | 4-AOI | 12 | +0.353 [−0.533, +0.839] | +0.286 [−0.373, +0.752] |
| **Domain-classifier AUC** | − | full | 20 | −0.317 [−0.775, +0.328] | −0.238 [−0.625, +0.228] |
| | | 4-AOI | 12 | −0.353 [−0.839, +0.653] | −0.286 [−0.752, +0.515] |
| Predictor-space mean dissimilarity (Emrehan) | − | 4-AOI | 12 | −0.105 [−0.543, +0.426] | −0.030 [−0.444, +0.400] |
| Predictor-space p95 dissimilarity (Emrehan) | − | 4-AOI | 12 | −0.084 [−0.587, +0.486] | 0.000 [−0.444, +0.444] |
| Fraction inside weighted AoA (Emrehan) | + | 4-AOI | 12 | +0.217 [−0.482, +0.587] | +0.091 [−0.345, +0.310] |
| Climatic distance (Emrehan) | − | 4-AOI | 12 | +0.057 [−0.762, +0.793] | +0.032 [−0.636, +0.633] |
| Geographic distance (Emrehan) | − | 4-AOI | 12 | −0.240 [−0.837, +0.733] | −0.159 [−0.714, +0.633] |
| Fraction inside unweighted support (Emrehan) | + | 4-AOI | 12 | +0.077 [−0.886, +0.630] | +0.030 [−0.743, +0.539] |

Point estimates for Emrehan's six measures reproduce his `ranking_summary.csv` exactly; the CIs
are new. The two regime definitions are rank-identical on the 4-AOI subset and nearly so on the
full set — they measure the same ordering.

## Reading the result honestly

1. **Regime distance does not predict transfer, and its point estimate has the *wrong* sign.**
   More regime-different pairs transfer *better* (ρ +0.29), driven by Bejís–Muğla: the largest
   regime distance in the set (log effN 0 vs 1.40) and the only interval-supported successful
   transfer (0.62 / 0.58). Meanwhile **Bejís–Evia-extended, the most regime-similar pair in the
   set (effN 1.0000 vs 1.0083, largest-share 100 % vs 99.6 %), is among the worst** (0.383 and
   0.448, both CIs below 0.5). Regime similarity is therefore demonstrably not sufficient — the
   same counterexample structure the geographic-similarity result has.
2. **The domain classifier is the sharpest version of the marginal blind spot.** Every one of the
   ten pairs is separable at AUC 0.962–0.9999 — marginal shift is essentially total everywhere —
   yet transfer outcomes range from 0.33 to 0.69. A diagnostic that is at ceiling for every pair
   cannot order outcomes; its rank correlation (−0.32, CI spanning zero) confirms the ordering it
   does induce (via the tiny variation below ceiling) is uninformative.
3. **No measure in the table works.** This completes the marginal side of the C4 contrast with
   two additional families (regime structure, learned separability) and strengthens the claim
   that the failure mode is conditional: the only diagnostic that separates the transferring pair
   from the failing pairs remains the signed-direction agreement count (7/9 vs 4/9,
   RESULTS_INVENTORY §5b.1).
4. **Power is very low, and this cuts both ways.** The effective sample is 10 unordered pairs
   built from 5 regions (6 pairs from 4 for the Emrehan rows); the two directions of a pair are
   not independent, and every pair shares regions with three others. CIs of width ±0.5–0.8 cannot
   rule out moderate true correlations in either direction. The defensible claim is *"none of
   these diagnostics demonstrably orders transfer, and the regime/geographic similarity
   counterexamples show similarity is not sufficient"* — not *"these diagnostics are proven
   useless"*.
5. Per the honesty rule, no further distance measures were tried after these results; the
   candidate set was fixed before the correlations were computed.

## Files

- `paper/regime_transfer_correlation.json` — metadata, provenance (sha256s, sources), per-region
  regime metrics, all 20 per-direction rows (transfer AUC + CI + every diagnostic), full
  correlation results with replicate counts.
- `paper/regime_transfer_correlation.csv` — the correlation table, flat.
- Scripts: `paper/burned_components.mjs`, `paper/regime_correlation.mjs` (Node + `hyparquet`;
  no Python on this machine). Note the copies in `paper/` reference the session scratchpad's
  `node_modules` only for `hyparquet`; any npm install of `hyparquet` next to them reproduces.
