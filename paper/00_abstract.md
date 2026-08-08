# Abstract

> **Drafting note.** Every number traces to `04_results.md`; structural rules applied: the
> load-bearing sentence is the contrast-pair evidence (exempt from sample-size objections); the
> narrative is a diagnostic question asked and answered, not a negative result; the label
> requirement of the conditional index is stated explicitly. ~260 words; trim to the journal's
> limit at submission.

Pre-fire thermal dryness — land surface temperature, its climatological anomalies and
thermal–optical dryness indices — describes the dynamic state that distinguishes a fire year
from an ordinary one, yet fire-susceptibility models built on such predictors are rarely tested
outside the region that trained them. Across five Mediterranean wildfire regions (Türkiye,
Spain, Greece, Italy; ~500 m cells, MCD64A1 burned-area labels, spatially blocked validation),
adding six pre-fire thermal predictors to a static terrain-and-fuel baseline raised
within-region ROC-AUC by +0.06 to +0.15 in every region, robust to coarser spatial blocking and
to earlier closure of the predictor window. Across regions, the same predictor block contributed
+0.004 on average over the twenty ordered transfer directions — improving ten with bootstrap
support and degrading seven — and label-blind adaptation (region-wise standardisation, CORAL)
compressed every direction towards chance. We therefore asked which pre-transfer diagnostic
anticipates this failure. Twenty candidates spanning marginal predictor-space distances, learned
domain separability, canonical niche-overlap statistics (Schoener's D, Warren's I, Mahalanobis
distance) and burn-pattern regime distances all failed to order transfer performance. The region
pair with the highest burned-niche overlap failed in both directions, while the pair with the
lowest overlap transferred in both: environmental-envelope similarity is neither sufficient nor
necessary for transfer. The only diagnostics whose bootstrap intervals excluded zero measured
conditional direction agreement — whether each predictor's signed association with burning
points the same way in both regions (Spearman ρ = 0.84). Because signed associations require
burned labels in both regions, this is a mechanism diagnosis and a labelled-probe instrument,
not a label-free screen. Transferability of dynamic-state fire models must be measured — and
measured conditionally: envelope overlap does not price it.
