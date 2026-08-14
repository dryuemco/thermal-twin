# Abstract


Pre-fire thermal dryness separates a fire year from a normal year. Models built on it are rarely
tested outside the region they were fitted in. Five Mediterranean wildfire regions were analysed
here, on about 500 m cells, with MCD64A1 labels and spatially blocked validation. Six pre-fire
thermal predictors were added to a terrain, fuel and greenness baseline.

**The local skill does not travel, and almost all of it is lost before the region changes.**
Within-region ROC-AUC rose by +0.056 to +0.153 in every region under blocked cross-validation, but
only +0.022 [−0.032, +0.077] when a whole burn scar is withheld. Across twenty ordered transfer directions the same
block contributed +0.004 [−0.028, +0.036]. That is not distinguishable from zero, and its sign
changes from pair to pair. The static baseline transferred no better, at 0.537 against 0.541. In precision-recall terms the
transfer is worse than those figures suggest: PR-AUC averages 0.156 against a no-skill baseline of
0.136, and six of the twenty directions fall below their own baseline. Three evaluations on **identical
cells** locate the failure. A model that has the held-out burn scar in its training data scores
0.634; withholding that scar gives 0.552; and a model fitted 306 to 2,802 km away gives 0.555, though that last is a mean over four foreign
models whose individual results run from 0.374 to 0.724. The
fire-specific residual is +0.082 [−0.011, +0.175] and the effect of the 2,800 km is **−0.003
[−0.075, +0.069]**. Neither withholding the fire nor crossing the region boundary produced a detectable
difference, and both rows sit close to chance, so neither can be attributed a cost here. Two thirds of the apparent collapse from
a region-wide 0.776 is the evaluation area itself, whose negatives are all fire-adjacent and
therefore the hardest in the region. Two predictors
reverse their association between regions: elevation and the LST anomaly. Removing them cost −0.081
of within-region skill, supported in every region and mostly due to elevation. It changed transfer
by +0.014 [−0.017, +0.045]. Both figures are post-selection estimates. A local cost is measured. No
compensating transfer gain is.

**The failure is invisible to the diagnostics that can be run before deployment.** Twenty candidate
diagnostics were rank-correlated against observed transfer. Only two had intervals excluding zero,
and both were conditional. The stronger one measures agreement in the sign of each predictor's
association (Spearman ρ = 0.84 over sixteen directions). No marginal measure was shown to order the
matrix, including predictor-space dissimilarity. At the point estimates, the pair with the highest
burned-niche overlap failed in both directions, while the lowest transferred in both. Signed
associations need labels on both sides. The family that works is therefore the one a practitioner
does not have.

**The mechanism of the residual is a reversal of sign.** Predictors do not merely weaken across
regions. Two reverse the direction of their association with burning, with bootstrap support. A distance in predictor space cannot see that. The same
reversal appears inside one study area, between two fires eleven months apart on an identical grid.
That arm rests on one fire and eleven positive-carrying blocks, so it corroborates rather than
establishes.

Label-free alignment pushed fourteen of twenty directions towards chance rather than repairing them.
Transfer skill has to be measured, not inferred from similarity. The price is target labels:
thirty-two labelled 5 km blocks recovered 85 to 89 % of the target's matched ceiling in three of six
directions.
