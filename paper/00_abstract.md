# Abstract


Pre-fire thermal dryness separates a fire year from a normal year. Models built on it are rarely
tested outside the region they were fitted in. Five Mediterranean wildfire regions were analysed
here, on about 500 m cells, with MCD64A1 labels and spatially blocked validation. Six pre-fire
thermal predictors were added to a terrain, fuel and greenness baseline.

**The local skill does not travel, and almost all of it is lost before the region changes.**
Within-region ROC-AUC rose by +0.056 to +0.153 in every region. Across twenty ordered transfer directions the same
block contributed +0.004 [−0.028, +0.036]. That is not distinguishable from zero, and its sign
changes from pair to pair. The static baseline transferred no better, at 0.537 against 0.541. Three evaluations on **identical
cells** locate the failure. A model that has the held-out burn scar in its training data scores
0.627; withholding that scar gives 0.552; and a model fitted 306 to 2,802 km away gives 0.559. The
fire-specific residual is +0.082 [−0.011, +0.175] and the effect of the 2,800 km is **−0.003
[−0.075, +0.069]**. The failure is therefore a property of contiguous spatial holdout, not of
separation distance and not of crossing a region boundary. Two thirds of the apparent collapse from
a region-wide 0.782 is the evaluation area itself, which is 34 to 87 % burned with every negative
fire-adjacent. Two predictors
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
